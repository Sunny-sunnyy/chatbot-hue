"""Lõi chung của trợ lý (Phase 9; đổi tên + thêm `tim_kho` / sổ nguồn / log ở B0): tìm kho (`tim_kho`) → dựng ngữ cảnh → sinh → kiểm citation.

`POST /api/chat` (`api/routes/chat.py`) và bộ đánh giá (`evaluation/full_corpus_eval.py` `answer_case`) cùng gọi `answer_query`;
`POST /api/chat/stream` gọi chung `prepare_answer` (phần trước model) và `check_citations`, chỉ phần sinh là stream
(spec streaming `2026-10-31-streaming-design.md` §3, §4.8). Phase 9 B0 (plan `docs/superpowers/plans/2026-11-02-phase-9-b0-plan.md`):
đường trả lời giữ y RAG 1–8 — code gọi `tim_kho` bằng câu gốc, sinh một lần; định tuyến (B1) và vòng công cụ do model gọi (B2) chưa có.

Ranh giới (plan B0 D3, test `tests/test_assistant_boundary.py`): module này **không** import SDK / client mạng; mọi lần gọi OpenAI nằm ở
`llm/generator_openai_full_corpus.py`. Lõi giữ chính sách (tuyến, công cụ, sổ nguồn, tiền mỗi lượt) bằng hàm Python thường.

Lõi chỉ làm các bước và ném lỗi có kiểu; nó **không** quyết phản hồi. Mỗi nơi gọi tự giữ cách của mình (spec streaming §4.8):
route đổi lỗi ra mã HTTP, chuẩn hóa `[Nguồn n]` → `[n]`, trả 500 khi citation hỏng, ghi `EvidenceRecorder`; bộ đánh giá
giữ chữ gốc, giữ chữ khi citation hỏng, đổi mọi lỗi thành `row["error"]`.
"""
import asyncio
import dataclasses
import time
from dataclasses import dataclass, field
from pathlib import Path

import json
import logging
import re
import unicodedata
from collections.abc import Sequence
from itertools import zip_longest
from typing import Literal

import anyio

from core import so_vet
from ingestion.source_state import discover_full_corpus_files
from core.schema import (CitationIntegrityError, GenerationError, GeneratorNotReadyError, RetrievalDependencyError,
                         RetrievedDocument)
from llm.answer_stream import AnswerTextStream
from llm.citations import CITATION_PATTERN, check_sentence_citations, select_cited_sources
from llm import lich_trinh as lt
from llm import lich_trinh_v2 as lt2
from llm import luu_tru_lich as ltl
from llm import quan_lich as ql
from llm import tra_web as tw
from llm import thoi_tiet as tt
from llm import ngay_lich as nl
from llm import su_kien as sk
from llm.lam_thay import nho_lam_thay
from llm import gan_diem as gd
from llm import goi_y_luu_tru as gylt
from llm import khoang_cach as kc
from llm import liet_ke as lk
from llm import mua_nang as mn
from llm import so_sanh as ss
from llm import the_noi as thn
from llm import tinh_ve as tv
from llm.danh_sach import CAU_DANH_SACH, hoi_ve_mot_noi, xin_danh_sach
from llm.len_lich import CAU_DAN_TRANG, nho_len_lich
from llm.luu_y_nguon import dong_tam_ngung, nhan_nguon
from llm.do_so import do_ngay_di
from llm.hoi_lai import TRUONG_THEO_LOAI, the_hoi_lai
from llm.full_corpus_prompt import (THOI_TIET_BAO_LU_MO_TA, CAU_LAM_THAY, CAU_Y_THIEU, INSUFFICIENT_ANSWER, LICH_TRINH_LUAT, MAY_HAVE_CHANGED_NOTICE, OUT_OF_SCOPE_ANSWER, REFUSAL_ANSWERS, TIM_KHO_MO_TA, TOOL_DA_DU_LICH,
                                   TOOL_LIMIT_TEXT, TOOL_NO_NEW_TEXT, VIET_LAI_NHIEU_Y_TEXT, build_assistant_input, them_kiem_du_bang_chung, today_line)
from llm.generator_openai_full_corpus import CallLog, GeneratedText
from llm.pricing import cost_usd
from retrieval.full_corpus_context import LICH_TRINH_TOOL_OVERHEAD, FullCorpusContextBuilder, PackedContext, PackedSource

logger = logging.getLogger("chat")  # cùng logger với route: dòng `chat_stream_drain` giữ tên + khuôn như trước B1

# Tuyến (spec Phase 9 §3). B0: mọi câu `tro_ly_hue` = đường RAG 1–8. B1: luật khẩn cấp + định tuyến chọn một trong 4.
ROUTE_TRO_LY_HUE = "tro_ly_hue"
ROUTE_TRO_CHUYEN = "tro_chuyen"
ROUTE_NGOAI_PHAM_VI = "ngoai_pham_vi"
ROUTE_KHAN_CAP = "khan_cap"
# H4c (B1 D8): nguồn trích thuộc vé / điểm đến / lễ hội ⇒ dòng "có thể đã thay đổi".
NOTICE_SOURCE_PREFIXES = ("travel/tickets/", "travel/places/", "festivals/", "travel/services/Lưu trú ở Huế")  # bài lưu trú: hạng có thể đã đổi (ghi kho 14/11)
MODEL_SEARCH_LIMIT = 2  # B2 D5: số lần MODEL gọi `tim_kho` được tìm thật (lần tìm đầu của code không tính); lần 3 ⇒ TOOL_LIMIT_TEXT
SEARCH_VARIANTS = ("v0", "v1", "v2", "v3")  # B2a: lần tìm đầu (plan D1)
STREAM_DRAIN_SECONDS = 0.5  # ngắt giữa chừng: sau `result.cancel()` đọc nốt tối đa chừng này giây (spec streaming §4.5 bước 3)


# Các ô của biểu mẫu "Lên kế hoạch" bản 2 (spec §3.1); thứ tự = thứ tự trên biểu mẫu
O_BIEU_MAU_V2 = ("so_ngay", "nguoi_lon", "tre_em", "lon_tuoi", "kieu_di", "so_thich", "ngay_di", "ngan_sach")


@dataclass(frozen=True)
class AssistantFlags:
    """Cờ từng phần B1 (plan D9, `settings.yaml` khối `assistant:`); tắt cả 4 ⇒ chuỗi gửi model như B0.
    B2 (plan B2 D1): `lan_tim_dau` — v0 câu gốc · v1 / v3 câu tìm do định tuyến viết (cần `router`) · v2 trợ lý tự gọi `tim_kho`;
    `tim_them` — sau lần tìm đầu của code, trợ lý được gọi `tim_kho` thêm (B2b). `v0` + `tim_them` tắt ⇒ chuỗi gửi model như B1."""
    router: bool = False
    today_line: bool = False
    may_have_changed_notice: bool = False
    lan_tim_dau: str = "v0"
    # 21/11/2026 (bậc 5, đếm sổ vết: cổng từ khoá bỏ sót 4 / 60 câu cần công cụ): chế độ ĐƯA ba công cụ thời tiết / ngày / khoảng cách cho trợ lý —
    # "tu_khoa" (mặc định, như trước: chỉ khi câu cuối / câu liền trước có từ khoá) | "luon" (mọi lượt của tuyến trợ lý Huế; model tự quyết có gọi không).
    # Chọn theo provider: `assistant.cong_cong_cu` cho đường OpenAI, `full_corpus_generation.bedrock.cong_cong_cu` khi provider là bedrock.
    cong_cong_cu: str = "tu_khoa"
    # Bậc 1b (21/11/2026): số lần MODEL được tìm kho thật trong một lượt — khoá `assistant.so_lan_tim_kho`, mặc định = `MODEL_SEARCH_LIMIT` như trước;
    # mở thành cấu hình để bộ đo thử nới. (Số vòng công cụ: `assistant.so_vong_cong_cu`, generator đọc.)
    so_lan_tim_kho: int = MODEL_SEARCH_LIMIT
    tim_them: bool = False
    # B3 (plan B3 D7): nhớ hội thoại trong một cuộc trò chuyện — tắt tới khi giao diện nhiều lượt xong (D8); chỉ nhớ câu hỏi khi `nho_cau_tra_loi` tắt
    # 20/11/2026: `nho_cau_tra_loi` bật = chỉ câu trả lời của lượt LIỀN TRƯỚC vào lịch sử (`api/conversations.py` `chi_dap_lien_truoc`); lõi không đọc cờ này
    nho_hoi_thoai: bool = False
    nho_cau_tra_loi: bool = True
    # 22/11/2026 (soát khác hãng, điểm "cuộc đã lập lịch thì không nhớ câu trả lời"): cuộc ĐÃ LƯU lịch — câu hỏi THƯỜNG cũng được giữ câu trả lời cho
    # lượt kế (`api/conversations.py` `dap_duoc_nho`: chỉ chặn lượt thật sự sửa lịch hoặc câu trả lời có TRÍCH nguồn lịch), và bản chạy lại khi lượt
    # bị rút (`answer_turn_stream_parallel`) phủ cả cuộc đó. Tắt ⇒ như trước: cuộc có lịch không giữ đáp, không chạy lại.
    nho_dap_cuoc_co_lich: bool = False
    # B5 (plan B5 bản 7 D1): công cụ `lich_trinh` — tắt tới khi đạt luật ghi trước; cần bảng điểm User duyệt (`bang_lich`, nạp ở rìa)
    lich_trinh: bool = False
    bang_lich: "lt.Bang | None" = field(default=None, compare=False, repr=False)
    # Cổng đợt 1 (spec `2026-11-06-giao-dien-cong-dot-1-design.md` D3 / D4): lượt từ biểu mẫu "Lên kế hoạch" — code xếp lịch bằng giá trị nút; tách khỏi
    # `lich_trinh` (câu gõ tự do). TẮT tới khi đạt Q-F; cần bảng điểm (không cần vòng công cụ: lượt biểu mẫu sinh một lần, không công cụ)
    lich_trinh_bieu_mau: bool = False
    # Bản đồ lịch trình (plan `2026-11-08-ban-do-lich-trinh-plan.md`): toạ độ do code gắn vào dữ liệu giao diện của lịch (không vào chuỗi gửi model);
    # bật ⇒ CSP cho ảnh tile OSM (`api/app.py`). Cần bảng điểm + bảng toạ độ (`toa_do_lich`, nạp ở rìa)
    ban_do_lich: bool = False
    toa_do_lich: "dict | None" = field(default=None, compare=False, repr=False)
    # Thí nghiệm tốc độ #6 (plan 2026-11-04-phase-9-toc-do-song-song): đường stream chạy phần `tro_ly_hue` cùng lúc định tuyến; tắt = như cũ
    song_song_tra_loi: bool = False
    # B6 (plan B6 bản 3 D10): cổng web sau câu trả lời kho — TẮT tới khi đạt luật ghi trước; cần định tuyến + vòng công cụ
    tra_web: bool = False
    # B5b (plan B5b bản 2 D11): thời tiết Huế (Open-Meteo) — TẮT tới khi đạt luật ghi trước; `du_bao` = hàm lấy dự báo (nạp ở rìa; test truyền
    # phản hồi ghi sẵn)
    thoi_tiet: bool = False
    # 17/11 (plan `2026-11-17-cau-bao-plan.md`, BẬT 17/11): câu bão / lũ — công cụ `thoi_tiet` khi câu có từ thời tiết hoặc từ nguy hiểm thời tiết
    # (`tt.co_tu_khoa_luot_rong`; bản "mọi lượt" đã lùi theo luật 2.5), thêm `loai` do model chọn; lượt `bao_lu` (model chọn hoặc lưới từ khoá rộng khớp)
    # ⇒ model không nhận số, code nối khối cố định
    bao_lu_cong_cu: bool = False
    # Phase 9 T1 (plan `2026-11-08-phase-9-t1-ngay-plan.md`): công cụ `ngay_lich` (code tính ngày + đổi âm ↔ dương) — chỉ đưa khi câu có từ chỉ ngày
    ngay_lich: bool = False
    # 12/11 (plan `2026-11-12-het-luot-tim-plan.md`): model đã dùng hết `MODEL_SEARCH_LIMIT` lần tìm thật ⇒ lượt gọi model kế tiếp không còn công cụ
    # `tim_kho` (bớt một lượt gọi chỉ để nhận chữ "đã hết lượt"). TẮT tới khi đo đạt; tắt ⇒ gọi generator y như trước.
    het_luot_bo_cong_cu: bool = False
    # 22/11/2026: câu tìm do MODEL viết gộp nhiều nơi / nhiều ý ("giá vé Đại Nội và Lăng Tự Đức…", "…; người cao tuổi giảm…") ⇒ ngoài lần tìm cả câu như
    # hiện nay, mỗi phần được tìm riêng và 2 đoạn đầu của nó được NỐI THÊM (đúng cơ chế `tim_theo_ve`). Không đổi chữ gửi model ngoài kết quả công cụ dài
    # hơn; câu tìm một phần và công tắc tắt ⇒ y như trước. Lý do + số đếm: `tests/test_tach_cau_tim_model.py`.
    tach_cau_tim_model: bool = False
    # 22/11/2026: model đã tự tìm kho (ít nhất một lần) mà chữ nó nộp KHÔNG có mã nguồn nào (chữ giữ chỗ: "placeholder", "tìm kho", "Tôi cần tìm thêm…" —
    # nó còn muốn tìm tiếp trong khi công cụ đã bị cất; hoặc dòng "chưa có" kèm lời giải thích không nguồn) ⇒ thay cho màn hình lỗi: gọi MỘT lần viết không công cụ trên mọi Bằng chứng lượt đã gom; vẫn không có
    # mã ⇒ câu từ chối cố định. Không chạm lượt nào đang qua kiểm. Lý do + số đo: `tests/test_het_luot_viet_lai.py`. TẮT ⇒ như trước.
    het_luot_viet_lai: bool = False
    # 22/11/2026 — số đo phiên E: lưới viết lại nổ 9 / 114 lượt, chữ giữ chỗ của bản viết đầu đứng 17–25 giây rồi mới được thay. Bật ⇒ lượt có công cụ
    # mà generator báo chữ về MỘT lần ở cuối (`chu_ve_mot_lan` — lớp dịch Bedrock) giữ chữ tới sau phép kiểm nguồn: qua ⇒ phát y như cũ (muộn cỡ mili
    # giây); viết lại ⇒ chỉ phát bản viết lại; bị rút ⇒ không phát chữ nào. Đường chữ chạy dần thật (OpenAI) không giữ. Test: `test_giu_chu_toi_kiem.py`.
    giu_chu_toi_kiem: bool = False
    so_vet: bool = False  # sổ vết debug có nội dung, chỉ máy local (`core/so_vet.py`); bật bằng `HUE_SO_VET=true`
    # Việc agent (3) 14/11 (plan `2026-11-14-cau-nhieu-y-plan.md`): câu nhiều ý — lời dặn theo ý + cổng web mở cả khi có dòng `CAU_Y_THIEU`
    cau_nhieu_y: bool = False
    # 19/11 (plan private `data/phase_9/s09_code/PLAN.md`): CODE nối vào dòng ghi chú một câu "tạm ngừng khi lũ / lệnh cấm / thời tiết xấu" chép
    # nguyên văn từ nguồn câu trả lời ĐÃ TRÍCH khi câu trả lời chưa nêu (`llm/luu_y_nguon.py`). Không model, không đổi chuỗi gửi model. TẮT tới khi đạt.
    noi_dong_tam_ngung: bool = False
    # 19/11 (plan private `data/tu_choi_khuon_2026-11-19/PLAN.md`): câu NHỜ TRỢ LÝ TỰ LÀM việc hệ thống không có (`llm/lam_thay.py`, hàm thuần đọc
    # câu người dùng) mà câu trả lời đã là câu từ chối khuôn ⇒ code thay bằng câu nói thật giới hạn (`CAU_LAM_THAY`), kết thúc `lam_thay`, không mở
    # mục web. Không model, không đổi chuỗi gửi model. TẮT tới khi đạt tiêu chí ghi trước.
    noi_that_lam_thay: bool = False
    # 20/11 (report `report_agent/2026-11-20/c_danh_sach_noi_that.md`): câu XIN DANH SÁCH (`llm/danh_sach.py`, hàm thuần đọc câu người dùng) có nguồn kho
    # ⇒ code nối vào dòng ghi chú một câu nói thật "danh sách có thể chưa đủ". Không model, không đổi chuỗi gửi model, không đổi chữ câu trả lời.
    danh_sach_noi_that: bool = False
    # 20/11 (report `report_agent/2026-11-20/e_len_lich_dan_trang.md`): câu NHỜ LẬP LỊCH nhiều ngày gõ trong ô chat (`llm/len_lich.py`, hàm thuần) ⇒ code
    # nối vào dòng ghi chú một câu trỏ sang trang Lên kế hoạch. Không model, không đổi chuỗi gửi model, không đổi chữ câu trả lời. Cần `lich_trinh_bieu_mau`.
    len_lich_dan_trang: bool = False
    # 15/11 (plan `2026-11-15-cau-noi-tiep-web-plan.md`): lượt CÓ lịch sử mà model đã tự tìm kho ⇒ phần web dùng câu tìm kho cuối model viết (có tên
    # nơi lấy từ lượt trước) thay câu người dùng gõ — câu hỏi tiếp "mở cửa mấy giờ" không còn ra web trần. TẮT tới khi đo đạt; cần `tra_web`
    web_cau_noi_tiep: bool = False
    # 21/11/2026 (đếm trên ba lượt mốc 12 vai + mẫu 68 dòng dò kho): lượt nhiều ý có dòng "Tư liệu chưa có thông tin về…" mở mục web ở 64 / 79 lượt (model
    # đang chạy) và 44 / 71 (model cũ), nhưng mục web đáp đúng điều thiếu chỉ ở 1 / 66 dòng mẫu, và lượt có mục web chậm hơn khoảng 4,5–10 giây. Cờ bật:
    # mục web CHỈ mở khi cả câu trả lời là câu từ chối (luật gốc D1); lượt đã trả lời được một phần giữ nguyên dòng "chưa có", không tra web, và (như
    # trước) không được lưu vào bộ nhớ đệm câu trả lời. TẮT tới khi đo trên cả hai model và chủ dự án chọn (đổi thứ người dùng thấy); cần cờ tra_web.
    web_chi_khi_tu_choi: bool = False
    # 22/11/2026 (S2; đếm 0 đồng `data/thu_bedrock_2026-11-21/b_buoc_4/chua_co/KET_QUA.md` mục 7, 8): tin NHIỀU Ý ⇒ lần tìm đầu, ngoài các đoạn
    # tìm bằng cả tin như cũ (giữ nguyên, không bớt đoạn nào), thêm `SO_DOAN_MOI_VE` đoạn đầu của lần tìm riêng TỪNG VẾ HỎI. Lý do: tìm bằng
    # nguyên một tin nhiều vế thì đoạn kho của vế phụ hay không vào ngữ cảnh ⇒ model ghi nhầm "Tư liệu chưa có thông tin về…". Không model,
    # không đổi lời dặn. Tin một ý / cờ `cau_nhieu_y` tắt / câu tìm do định tuyến viết ⇒ chuỗi gửi model y như cũ. TẮT tới khi một lượt thật đạt.
    tim_theo_ve: bool = False
    # 22/11/2026 (đếm trên 364 tin nhiều ý đã ghi: 26 % số vế tìm là mẩu CỤT không có chủ thể — "mất bao lâu?", "ko phải 5", "giờ mở cửa ko?" — có ở 65 % số
    # tin; đọc tay 28 đoạn chúng kéo về: 20 không liên quan tới tin): cờ con của `tim_theo_ve` — vế cụt KHÔNG được tìm riêng; lần tìm bằng cả tin và các vế
    # còn lại giữ nguyên. Tắt ⇒ danh sách vế y như cũ.
    tim_ve_bo_cut: bool = False
    # 19/11 (plan private `data/hoi_tiep_goi_y_2026-11-19/PLAN.md`): lịch sử chỉ nhớ câu hỏi ⇒ hỏi tiếp "địa chỉ quán đó" model không biết quán nào.
    # Bật: code ghi TÊN BÀI các nguồn đã trích là bài riêng của một nơi vào chỗ tin trợ lý của lịch sử (`llm/ten_goi_y.py`). TẮT tới khi đo đạt.
    nho_ten_goi_y: bool = False
    # 20/11 (plan `report_agent/2026-11-20/b_cache_cau_tra_loi_plan.md`): người khác gõ ĐÚNG câu đó ở lượt đầu một cuộc mới ⇒ route trả lại bản đã
    # lưu, không tìm kho / gọi model (`api/cache_tra_loi.py`). Lõi không đọc cờ này — chỉ nơi dựng app. TẮT tới khi review + lượt thật đạt.
    cache_cau_tra_loi: bool = False
    # "Lên kế hoạch" đợt 1 (plan `2026-11-12-len-ke-hoach-dot-1-plan.md`, spec bản 3.3 §5c.8): biểu mẫu bốn nhóm + hợp đồng `truong` mới — một cờ cho
    # cả đợt, TẮT tới khi đạt nghiệm thu; cần `lich_trinh_bieu_mau`. `len_ke_hoach_o_hien` = các ô biểu mẫu hiện (`/api/tinh_nang`): ô chưa có tác
    # dụng với bộ xếp đang dùng thì chưa hiện (spec N1)
    len_ke_hoach_v2: bool = False
    len_ke_hoach_o_hien: tuple[str, ...] = ()
    bang_lich_v2: "lt2.BangV2 | None" = field(default=None, compare=False, repr=False)  # bảng v8 (`assistant.lich_trinh_bang_v2`), nạp khi cờ bật
    # sở thích dưới sàn "có tác dụng" của mô phỏng (plan §3 (b)) ⇒ ô ẩn; test khoá danh sách này khớp kết quả mô phỏng trên bảng đang dùng
    len_ke_hoach_so_thich_an: tuple[str, ...] = ()
    # "Lên kế hoạch" đợt 2 (B) (plan `2026-11-13-len-ke-hoach-dot-2-plan.md`): ảnh tự host cho từng điểm của lịch bản 2 (không vào chuỗi gửi model);
    # cần cờ bản 2 + bảng ảnh (`assistant.lich_trinh_bang_anh`, nạp + kiểm lúc khởi động)
    anh_lich: bool = False
    # Sửa lịch bằng lời trên lịch bản 2 (plan `2026-11-14-sua-lich-v2-plan.md`): cuộc có lịch đã lưu + câu có từ sửa ⇒ một lần gọi hiểu ý ⇒ code áp.
    # TẮT tới khi đạt Q3 + Q5; cần cờ bản 2. Tắt ⇒ không chạm (chuỗi gửi model giống byte).
    sua_lich_v2: bool = False
    # Plan 2026-11-17-chua-ho-tro-plan.md: lần hiểu ý có thêm hành động `chua_ho_tro` (câu sửa mà bộ hành động chưa làm được ⇒ lịch giữ nguyên +
    # câu cố định của code, không rơi sang đường thường). TẮT tới khi đạt S1–S3; cần cờ sua_lich_v2. Tắt ⇒ chuỗi gửi model giống byte.
    sua_lich_chua_ho_tro: bool = False
    # Lượt đo cuối 18/11 (sửa lịch bằng lời 7 / 10): model trả `chua_ho_tro` cho câu "dời hai điểm, mỗi điểm một buổi" ⇒ code đọc câu và áp hai lần
    # dời (`sua_lich_v2.doi_buoi_tu_cau`). TẮT tới khi đạt tiêu chí ghi trước; cần cờ sua_lich_chua_ho_tro. Không đổi chuỗi gửi model.
    sua_lich_doi_cho_code: bool = False
    # 21/11/2026 (phiên trình duyệt trên Sonnet: "dời Đại Nội sang buổi tối ngày 1" ⇒ "Chưa rõ ngày / buổi"; tái hiện 18 lượt: Sonnet 5 / 9, luna đổi thành
    # "chiều" 2 / 9): lần hiểu ý dùng khuôn + lời dặn cho `buoi` nhận "toi"; code trả lời thật (điểm ban ngày ⇒ lý do + chỗ dời được). TẮT tới khi đo
    # trên cả hai model; cần cờ sua_lich_chua_ho_tro. Tắt ⇒ chuỗi gửi model giống byte.
    sua_lich_buoi_toi: bool = False
    # 20/11 (plan `report_agent/2026-11-20/c_doi_cho_ngay_plan.md`): "đổi chỗ ngày 1 với ngày 2" — code đọc cặp ngày (danh sách cho phép) rồi hoán đổi nội dung
    # hai ngày qua đúng đường xếp-rồi-kiểm (`sua_lich_v2.doi_cho_ngay`). TẮT tới khi đạt; cần `sua_lich_v2`. Không đổi chuỗi gửi model.
    sua_lich_doi_cho_ngay: bool = False
    # 21/11/2026 (người dùng mô phỏng: 4 / 4 tin vừa sửa lịch vừa hỏi, cả hai model — lịch được sửa, phần hỏi bị bỏ không một lời): lần hiểu ý có thêm
    # hành động `hoi_them`; code thêm một dòng cố định "phần câu hỏi chưa trả lời, bạn gửi riêng" vào khối thay đổi của lịch. Lượt sửa vẫn KHÔNG trả lời
    # câu hỏi đó. TẮT tới khi đo trên cả hai model; cần cờ sua_lich_chua_ho_tro. Tắt ⇒ chuỗi gửi model giống byte.
    sua_lich_kem_hoi: bool = False
    # 21/11/2026 (bản hẹp của "hỏi lại khi thiếu thông tin"; người dùng mô phỏng, vai sửa lịch, cả hai model: nhờ "thêm X" ⇒ code tự thế chỗ một điểm đang
    # có, 5 / 8 lượt sửa lịch của lượt mốc; bộ áp trên 144 lịch mẫu: 33–63 % lệnh thêm rơi vào thế chỗ): lệnh THÊM chỉ làm được bằng cách thế chỗ ⇒ lịch
    # giữ nguyên + dòng nói điểm nào thay được ("bạn nhắn: thay Y bằng X"); lệnh thêm bị luật xếp chặn ⇒ lý do + chỗ làm được. TẮT tới khi đo và chủ dự
    # án chọn (đổi thứ người dùng thấy); cần cờ sua_lich_v2. Tắt ⇒ bộ áp chạy y như cũ.
    sua_lich_them_khong_the: bool = False
    # 23/11/2026 (chủ dự án chọn "cho ngày dày thêm" sau khi nghe số: 0 / 14.725 lệnh thêm làm được trên lịch vừa xếp): lệnh THÊM mà luật xếp chặn chỉ
    # vì NHỊP ĐI (số điểm một buổi, quỹ phút) ⇒ vẫn thêm; ngày đó dài ra (buổi chiều lùi theo buổi sáng, giữ bữa trưa 60 phút, chiều kết trước 18:00),
    # dòng báo nói ngày dày hơn nhịp đã chọn. Giờ mở cửa, luật khu, luật của đoàn có trẻ nhỏ / người lớn tuổi không nới. TẮT tới khi đo; cần
    # sua_lich_them_khong_the (phần gợi ý "thêm vào buổi khác" nằm trong câu của cờ đó). Tắt ⇒ bộ áp chạy y như cũ với lịch chưa có ngày nào dày.
    sua_lich_them_day: bool = False
    # BẢN THỬ 23/11/2026 — KHÔNG MỞ khi chủ dự án chưa quyết (đổi luật khu của lịch): lệnh THÊM một điểm còn vướng luật khu (ngày quá hai khu, hai khu
    # không kề) ⇒ vẫn thêm khi mỗi chặng sang khu không kề ≤ 60 phút theo bảng khoảng cách; giờ cộng đúng số phút đó; dòng báo nêu chặng + số phút.
    # Đếm trước khi làm (đoàn thường, có trần giờ): chỉ nới nhịp 30 % lệnh "thêm X" làm được ⇒ thêm phần này 82 %. Cần sua_lich_them_day + khoang_cach.
    sua_lich_them_khu: bool = False
    # 23/11/2026 (chủ dự án: đoàn có trẻ nhỏ / người lớn tuổi TỰ XIN "thêm <điểm>" thì "cho thêm, có dòng báo"): ngày đoàn đó xin thêm được vượt mức
    # "một điểm một buổi, hai điểm một ngày" tới các trần `lich_trinh_v2.HAN_CHE_*` (ba điểm một ngày, hai điểm một buổi, sáng kết ≤ 13:00, chiều kết
    # ≤ 17:00); luật khu KHÔNG nới cho đoàn này; lịch xếp BAN ĐẦU của đoàn không đổi. Đếm 72 lịch của đoàn: 0 ⇒ 22 % lệnh "thêm X". Cần sua_lich_them_day.
    sua_lich_them_han_che: bool = False
    # 23/11/2026 (chủ dự án, sau khi tự test: "thiếu thông tin — ngày nào, buổi nào — thì hỏi lại kèm gợi ý và câu 'hay để mình tự xếp'; trợ lý chỉ tự làm
    # khi người dùng bảo; không làm được thì không 'từ chối' mà giải thích và đưa lối đi"): lệnh "thêm <điểm>" thiếu ngày hoặc buổi ⇒ lịch đứng yên + một
    # câu hỏi do code viết + nút (chỗ gợi ý, các chỗ đặt được khác, "Xếp giúp mình"); lệnh đủ ngày + buổi mà thêm thẳng được ⇒ làm luôn; không thêm
    # được ⇒ câu thường + nút lối đi; điểm khu xa ⇒ nói thật + nút mở biểu mẫu. Cần sua_lich_them_khong_the. TẮT tới khi phiên điều phối mở.
    sua_lich_hoi_truoc: bool = False
    # 24/11/2026, BẢN THỬ (phiên điều phối chọn từ việc đọc repo; chủ dự án cho thử trên nhánh, chưa gộp, chưa mở): nút "Hoàn tác lần sửa này" dưới thẻ của
    # lượt sửa lịch — cuộc giữ MỘT bản lưu trước lần sửa cuối (RAM), `POST /api/lich/hoan_tac` đặt lịch về bản đó (không gọi model); chỉ một bước, chỉ khi
    # lịch chưa đổi thêm (`api/conversations.py` `hoan_tac`, `api/routes/hoan_tac.py`). Căn cứ: lệnh bỏ nay bỏ luôn không hỏi lại. Cần sua_lich_v2.
    sua_lich_hoan_tac: bool = False
    # 23/11/2026 (chủ dự án nêu: buổi tối của đoàn có trẻ nhỏ đang bỏ trống). `toi_nhe`: đoàn có trẻ nhỏ / người lớn tuổi được MỘT hoạt động tối nhẹ gần trung
    # tâm mỗi tối không phải ngày đi xa, lấy từ khoá `toi_nhe` của bảng điểm, không lặp (đếm 960 tổ hợp: 720 tổ hợp / 2.160 tối đang trống ⇒ 1.710 tối có hoạt
    # động). `bo_toi_de_trong`: lệnh bỏ hoạt động tối ⇒ tối đó để trống, các tối khác giữ nguyên (xem `sua_lich_v2.ap`). Cả hai TẮT tới khi chủ dự án quyết.
    toi_nhe: bool = False
    bo_toi_de_trong: bool = False
    # 23/11/2026 (chủ dự án, khi được hỏi "bỏ hoạt động tối thì để trống hay lấp": "nên hỏi lại người dùng đổi hoạt động hay là để trống"): lệnh bỏ một
    # hoạt động BUỔI TỐI mà chưa nói cách ⇒ lịch giữ nguyên, code hỏi lại hai lựa chọn; "đổi" ⇒ thay đúng tối đó (các tối khác được ghim, không dồn hàng,
    # không lặp); "để trống" ⇒ tối đó trống. Thay cho `bo_toi_de_trong` (không bật cùng). TẮT tới khi đo đạt.
    bo_toi_hoi_lai: bool = False
    # 23/11/2026 (phần nối của lời chủ dự án "đi uống cà phê ở quán nào đó"): người dùng GỌI TÊN hoạt động tối muốn có ("tối ngày 1 đi cà phê HANOK",
    # "thay phố Tây bằng Ca Huế") ⇒ code đặt đúng mục đó vào tối đó bằng ghim, tối khác + ban ngày giữ nguyên; mục đang ở tối khác ⇒ hai tối đổi chỗ;
    # không làm được ⇒ câu nói thật lý do. Đếm 5.216 lệnh trên lưới: 0 ⇒ 86 % làm được. Không đổi khuôn / lời dặn. Cần `bo_toi_hoi_lai`. TẮT tới khi đo đạt.
    toi_goi_ten: bool = False
    # Lịch đã lưu của cuộc vào LƯỢT HỎI THƯỜNG (plan private data/lich_da_luu_2026-11-19/PLAN.md): cuộc có lịch + tuyến `tro_ly_hue` ⇒ code nối một nguồn
    # "Lịch bạn đang có" (lịch + số giờ do code tính) sau ngữ cảnh kho; lượt biểu mẫu / lượt sửa / trò chuyện / câu cố định không nhận. TẮT tới khi
    # đo đạt; cần cờ sua_lich_v2 (route chỉ nạp lịch khi cờ đó bật) + tim_them. Tắt ⇒ chuỗi gửi model giống byte.
    lich_vao_hoi_thuong: bool = False
    # Gợi ý nơi ở trong lịch bản 2 (plan `2026-11-14-luu-tru-trong-lich-plan.md`): khu cả chuyến + ≤ 5 cơ sở do code chọn, `lich["o_dau"]`
    # (không vào tin nhắn gửi model). TẮT tới khi đạt; cần cờ bản 2 + bảng lưu trú (`assistant.lich_trinh_bang_luu_tru`, kiểm lúc khởi động)
    luu_tru_lich: bool = False
    luu_tru_bang: "dict | None" = field(default=None, compare=False, repr=False)
    # Quán ăn gợi ý trong lịch bản 2 (plan `2026-11-14-quan-trong-lich-plan.md`): ≤ 2 quán cùng cụm mỗi bữa do code chọn, `lich["an"]`
    # (không vào tin nhắn gửi model). TẮT tới khi đạt; cần cờ bản 2 + bảng quán (`assistant.lich_trinh_bang_quan`) + toạ độ điểm (`lich_trinh_toa_do`)
    quan_lich: bool = False
    # 23/11/2026: bữa trưa của lịch lấy trước điểm có quán CÓ BÀI TRONG KHO trên đường người đi (`quan_lich.an_uong`, `kho_truoc`). Đếm 960 tổ hợp biểu
    # mẫu + các lịch sau lệnh thêm: số ở runbook 10.2. Cần `quan_lich`. TẮT tới khi phiên điều phối mở cùng `sua_lich_them_khu`.
    quan_trua_kho_truoc: bool = False
    quan_bang: "dict | None" = field(default=None, compare=False, repr=False)
    quan_toa_do: "dict | None" = field(default=None, compare=False, repr=False)
    anh_lich_bang: "dict | None" = field(default=None, compare=False, repr=False)
    du_bao: "object | None" = field(default=None, compare=False, repr=False)
    # 16/11 (plan `2026-11-16-khoang-cach-plan.md`): công cụ `khoang_cach` — km / phút giữa hai điểm bảng lịch, tra bảng dựng sẵn (code tính, model chọn
    # mã); chỉ đưa khi câu có từ khoá khoảng cách. TẮT tới khi đo đạt; cần `tim_them` + bảng (`assistant.khoang_cach_bang`, nạp ở rìa)
    khoang_cach: bool = False
    khoang_cach_bang: "kc.BangKhoangCach | None" = field(default=None, compare=False, repr=False)
    # 20/11 (plan `report_agent/2026-11-20/c_su_kien_theo_ngay_plan.md`): câu vừa nêu một khoảng ngày vừa hỏi lễ hội / sự kiện ⇒ code tra bảng chép từ kho
    # (`assistant.su_kien_bang`, nạp ở rìa), đổi ngày âm ⇒ dương, đăng một nguồn trước lần gọi model đầu (`llm/su_kien.py`). TẮT tới khi đo đạt; cần `tim_them`.
    # 21/11/2026 (plan `report_agent/2026-11-21/b_bac_1_vong_cong_cu_plan.md` phần 1a; người dùng mô phỏng: 5 / 44 lượt luna chạm trần vòng ở câu 3–5 ý có "bao xa"
    # + nơi không có trong bảng khoảng cách ⇒ câu từ chối trống): vòng cuối cùng của lượt có công cụ gửi KHÔNG kèm công cụ ⇒ model viết từ bằng chứng đã có.
    vong_cuoi_chi_viet: bool = False
    # cùng ngày: công cụ khoảng cách khi không có số cho cặp nơi ⇒ thêm một dòng trạng thái (đừng gọi lại cho cặp này, vẫn trả lời các ý khác)
    khoang_cach_trang_thai: bool = False
    su_kien_theo_ngay: bool = False
    su_kien_bang: "tuple[dict, ...] | None" = field(default=None, compare=False, repr=False)
    # 21/11/2026 (plan `report_agent/2026-11-21/b_cong_cu_liet_ke_plan.md`): công cụ `liet_ke_bai` — code liệt kê BÀI của kho theo nhóm / cụm từ cho câu xin
    # danh sách và câu "nơi nào có đặc điểm X" (tìm theo đoạn chỉ chạm 1–3 trên 6–39 bài đúng loại). Mục lục nạp ở rìa từ chính các file của kho. TẮT tới khi
    # đo đạt; tắt ⇒ danh sách công cụ gửi model giống byte.
    liet_ke_bai: bool = False
    muc_luc: "tuple[lk.Bai, ...] | None" = field(default=None, compare=False, repr=False)
    # 22/11/2026 (việc X10; lý do + số đếm: `llm/the_noi.py`, test `tests/test_the_noi.py`): THẺ NƠI — ở tin nhiều ý có chữ hỏi hẹp (giờ, địa chỉ…), sau
    # mỗi lần tìm kho code gắn cho từng nơi được nhắc đúng tên mà bài riêng chưa có trong sổ nguồn một nguồn chép dòng địa chỉ / giờ từ chính bài đó (+ hàng
    # vé lẻ) ⇒ model thôi ghi "tư liệu chưa có giờ mở cửa…" cho thứ kho có. Không gọi model, không tìm thêm. Bảng thẻ nạp ở rìa từ các file của kho; không có
    # bảng ⇒ không làm gì. TẮT ⇒ chuỗi gửi model giống byte; tin một ý / tin không có chữ hỏi hẹp ⇒ giống byte cả khi mở.
    the_noi: bool = False
    the_noi_bang: "thn.Bang | None" = field(default=None, compare=False, repr=False)
    # 17/11 (plan `2026-11-17-khoang-cach-tinh-san-plan.md`): câu đang gõ có từ khoá + đúng hai tên điểm của bảng ⇒ code tra bảng và nối nguồn khoảng
    # cách TRƯỚC lần gọi model đầu, lượt đó không đưa công cụ `khoang_cach` (bớt một lần gọi model ≈ 1,8 s trên đường chữ đầu). TẮT tới khi đo đạt
    khoang_cach_tinh_san: bool = False
    # 21/11/2026 (mục đã chốt "gần X có gì ăn"; plan private `data/thu_bedrock_2026-11-21/c_muc_5/PLAN_P1.md`): công cụ `gan_diem` — code tính những gì Ở
    # GẦN một điểm của bảng khoảng cách: quán ăn / cà phê CÓ BÀI KHO trong 2 km (bảng quán của thẻ lịch, đường chim bay) hoặc các điểm tham quan gần nhất
    # (bảng khoảng cách). Lượt mốc 12 vai: "trưa gần Đại Nội có quán nào" ra "tư liệu không nói quán nào gần" 4 / 5 lượt dù có 17 quán kho trong 2 km.
    # Chỉ đưa khi câu có từ "gần / quanh / cạnh…" (hoặc cổng công cụ ở chế độ luôn đưa). TẮT tới khi đo; cần khoang_cach + bảng quán và toạ độ điểm của
    # thẻ lịch (hai bảng đó nạp khi `quan_lich` hoặc cờ này bật, và cần bảng lịch bản 2).
    gan_diem: bool = False
    # 23/11/2026: công cụ "gần một điểm" in giờ hoạt động theo bài kho cạnh tên quán (`gio_kho` của bảng quán bản 4; quán kho không ghi giờ thì không in).
    # Vì sao: "…trưa ăn gì gần đó?" hai lần được trả lời bằng một quán kho ghi chỉ mở 18h–23h (22 và 23/11) — công cụ xếp theo khoảng cách, model
    # không thấy giờ. TẮT tới khi đo bật ↔ tắt; cần `gan_diem`. Tắt ⇒ chữ công cụ như cũ từng byte.
    gan_diem_gio: bool = False
    # 19/11 (plan private `data/xuat_lich_dep_2026-11-19/PLAN.md`): `GET /api/lich/pptx` — tải lịch đã lưu của cuộc thành PowerPoint (code điền
    # khuôn, không model). TẮT tới khi đạt; cần `sua_lich_v2` (chỉ cờ đó mới lưu lịch của cuộc) và thư viện `python-pptx`.
    xuat_pptx: bool = False
    # BẢN THỬ (nhánh thu-b-so-tay, 24/11/2026 — chủ dự án chọn 21:21 sau khi xem hai hồ sơ mẫu; KHÔNG mở trước khi chủ dự án xem trong giao diện): sổ tay
    # cho chuyến đi dựng từ lịch đang lưu của cuộc — `POST /api/so_tay` (`api/routes/so_tay.py`, `llm/so_tay.py`). Tắt ⇒ đường API trả 404, `/api/tinh_nang`
    # không có khoá, không gì khác đổi.
    so_tay: bool = False
    # BẢN THỬ (nhánh thu-b-ho-so-chu-de, 24/11/2026 — chủ dự án chọn 22:19 "chọn chủ đề từ danh sách"; KHÔNG mở trước khi chủ dự án xem trong giao diện):
    # hồ sơ theo chủ đề — `GET /api/ho_so/chu_de`, `POST /api/ho_so` (`api/routes/ho_so.py`, `llm/ho_so_chu_de.py`). Tắt ⇒ hai đường trả 404, `/api/tinh_nang`
    # không có khoá, không gì khác đổi.
    ho_so_chu_de: bool = False
    # Dải "Hồ sơ theo chủ đề" trên Trang chủ (dưới 5 ô "Khám phá theo lĩnh vực"): chỉ gửi qua `/api/tinh_nang` khi `ho_so_chu_de` cũng bật (gói deploy
    # chỉ ép `ho_so_chu_de: false` nên tự ẩn theo mà không lỗi khởi động).
    chu_de_trang_chu: bool = False
    # Đợt 1A (27/11/2026, mặc định tắt): chống gọi lặp trùng tham số cho 5 công cụ phụ trợ + trả phản hồi chỉ mã nguồn [N] đã tra, gắn `lap: True`.
    chong_lap_cong_cu: bool = False
    # Đợt 1A (27/11/2026, mặc định tắt): khi chạm `max_turns` mà `trace.documents` đã có bằng chứng nguồn, gọi viết lại MỘT lần tắt toàn bộ tool.
    cuu_max_turns: bool = False
    # Đợt 1B (27/11/2026, mặc định tắt): siết ranh giới `router` ↔ `tro_chuyen` và buộc `tro_chuyen` từ chối đúng khuôn nếu lọt câu hỏi ngoài phạm vi.
    siet_tro_chuyen: bool = False
    # Đợt 2 (27/11/2026, mặc định tắt): công cụ `goi_y_phuong_an_mua_nang` — gợi ý điểm trong nhà / có mái che theo buổi & cụm khi mưa / nắng nóng.
    goi_y_mua_nang: bool = False
    # Đợt 2 (27/11/2026, mặc định tắt): công cụ `so_sanh_diem_den` — so sánh thực dụng 2–3 điểm từ bảng điểm + thẻ nơi + khoảng cách.
    so_sanh_diem_den: bool = False
    # Đợt 4A (27/11/2026, mặc định tắt): Sufficient Context ICLR 2025 — phân biệt đoạn nhắc tên nơi với đoạn chứa đúng dữ kiện trả lời.
    kiem_du_bang_chung: bool = False
    # Đợt 4A (27/11/2026, mặc định tắt): nhắc bước còn lại (`<nhac_vong>` khi còn <= 2 lượt) + giữ nguyên mảng `tools` cố định không rút bằng `is_enabled`.
    canh_bao_vong_con_lai: bool = False
    # Đợt 4A (27/11/2026, mặc định tắt): Actionable Feedback khi viết lại lỗi citation + rút gọn `mua_nang` + Tool Use Examples + vá ca trượt Đợt 2.
    toi_uu_dot2_va_viet_lai: bool = False
    # Đợt 7 Nhịp 2B (28/11/2026, mặc định tắt trong code): hậu kiểm trích dẫn cấp câu (`verdict_meta_exempt`) + tối đa 1 lần `_goi_viet_lai` định hướng.
    kiem_trich_dan_cau: bool = False
    # Đợt 5 Phần A (28/11/2026, mặc định tắt): .ics v2 (GET /api/lich/ics + VTIMEZONE Asia/Ho_Chi_Minh), deep link OTA 3 sàn + mẫu hỏi phòng.
    xuat_nang_cao: bool = False
    # Đợt 5 Phần A (28/11/2026, mặc định tắt): Slide Designer Agent + .pptx v2 (3 theme, 9 layout, đo tràn chữ, center-crop PIL).
    slide_designer: bool = False
    slide_designer_cfg: dict | None = field(default=None, compare=False, repr=False)
    # Đợt 6 (28/11/2026, mặc định tắt): công cụ `tinh_ve_va_gio_tham_quan` & `goi_y_luu_tru`.
    tinh_ve_tham_quan: bool = False
    goi_y_luu_tru: bool = False

    def __post_init__(self) -> None:
        if self.tinh_ve_tham_quan and not self.tim_them:
            raise ValueError("assistant.tinh_ve_tham_quan needs assistant.tim_them: true")
        if self.goi_y_luu_tru and not (self.tim_them and self.luu_tru_bang is not None):
            raise ValueError("assistant.goi_y_luu_tru needs assistant.tim_them and the lodging table (assistant.lich_trinh_bang_luu_tru)")
        if self.siet_tro_chuyen:
            pass
        if self.xuat_nang_cao and not self.sua_lich_v2:
            raise ValueError("assistant.xuat_nang_cao needs assistant.sua_lich_v2: true")
        if self.slide_designer:
            import importlib.util
            if not self.sua_lich_v2 or importlib.util.find_spec("pptx") is None:
                raise ValueError("assistant.slide_designer needs assistant.sua_lich_v2: true and the python-pptx package (uv sync)")
        if self.goi_y_mua_nang and not (self.tim_them and self.thoi_tiet and self.du_bao is not None and self.bang_lich_v2 is not None):
            raise ValueError("assistant.goi_y_mua_nang needs assistant.tim_them, assistant.thoi_tiet and assistant.len_ke_hoach_v2 (the v2 schedule table)")
        if self.so_sanh_diem_den and not (self.tim_them and self.bang_lich_v2 is not None):
            raise ValueError("assistant.so_sanh_diem_den needs assistant.tim_them and assistant.len_ke_hoach_v2 (the v2 schedule table)")
        if self.xuat_pptx:
            import importlib.util
            if not self.sua_lich_v2 or importlib.util.find_spec("pptx") is None:
                raise ValueError("assistant.xuat_pptx needs assistant.sua_lich_v2: true and the python-pptx package (uv sync)")
        if self.lan_tim_dau not in SEARCH_VARIANTS:
            raise ValueError(f"assistant.lan_tim_dau must be one of {SEARCH_VARIANTS}")
        if self.lan_tim_dau in ("v1", "v3") and not self.router:
            raise ValueError("assistant.lan_tim_dau v1 / v3 needs assistant.router: true (search text is written by the router)")
        if self.lich_trinh and (not self.tim_them or self.bang_lich is None):
            raise ValueError("assistant.lich_trinh needs assistant.tim_them: true and the itinerary table (assistant.lich_trinh_bang)")
        if self.lich_trinh_bieu_mau and self.bang_lich is None:
            raise ValueError("assistant.lich_trinh_bieu_mau needs the itinerary table (assistant.lich_trinh_bang)")
        if self.ban_do_lich and (self.bang_lich is None or self.toa_do_lich is None):
            raise ValueError("assistant.ban_do_lich needs the itinerary table and assistant.lich_trinh_toa_do")
        if self.tra_web and not (self.router and self.tim_them):
            raise ValueError("assistant.tra_web needs assistant.router: true and assistant.tim_them: true")
        if self.ngay_lich and not self.tim_them:
            raise ValueError("assistant.ngay_lich needs assistant.tim_them: true (tool loop)")
        if self.khoang_cach and (not self.tim_them or self.khoang_cach_bang is None):
            raise ValueError("assistant.khoang_cach needs assistant.tim_them: true and the distance table (assistant.khoang_cach_bang)")
        if self.khoang_cach_tinh_san and not self.khoang_cach:
            raise ValueError("assistant.khoang_cach_tinh_san needs assistant.khoang_cach: true")
        if self.gan_diem and not (self.khoang_cach and self.quan_bang is not None and self.quan_toa_do is not None):
            raise ValueError("assistant.gan_diem needs assistant.khoang_cach: true, the restaurant table (assistant.lich_trinh_bang_quan) and the point "
                             "coordinates (assistant.lich_trinh_toa_do) — both are loaded with assistant.len_ke_hoach_v2")
        if self.thoi_tiet and (not self.tim_them or self.du_bao is None):
            raise ValueError("assistant.thoi_tiet needs assistant.tim_them: true and a forecast function")
        if self.liet_ke_bai and (not self.tim_them or self.muc_luc is None):
            raise ValueError("assistant.liet_ke_bai needs assistant.tim_them: true and the article index (loaded from the knowledge base)")
        if self.ho_so_chu_de and not (self.liet_ke_bai and self.the_noi and self.muc_luc is not None):
            raise ValueError("assistant.ho_so_chu_de needs assistant.liet_ke_bai (the article index) and assistant.the_noi (the place-card table)")
        if self.so_tay and not (self.sua_lich_v2 and self.len_ke_hoach_v2 and self.the_noi):
            raise ValueError("assistant.so_tay needs assistant.sua_lich_v2 (the saved schedule), assistant.len_ke_hoach_v2 and assistant.the_noi (the place-card table)")
        if self.bao_lu_cong_cu and not self.thoi_tiet:
            raise ValueError("assistant.bao_lu_cong_cu needs assistant.thoi_tiet: true")
        if self.len_ke_hoach_v2 and (not self.lich_trinh_bieu_mau or self.bang_lich_v2 is None):
            raise ValueError("assistant.len_ke_hoach_v2 needs assistant.lich_trinh_bieu_mau: true and the v2 table (assistant.lich_trinh_bang_v2)")
        if self.sua_lich_v2 and not self.len_ke_hoach_v2:
            raise ValueError("assistant.sua_lich_v2 needs assistant.len_ke_hoach_v2: true")
        if self.sua_lich_chua_ho_tro and not self.sua_lich_v2:
            raise ValueError("assistant.sua_lich_chua_ho_tro needs assistant.sua_lich_v2: true")
        if self.sua_lich_doi_cho_code and not self.sua_lich_chua_ho_tro:
            raise ValueError("assistant.sua_lich_doi_cho_code needs assistant.sua_lich_chua_ho_tro: true")
        if self.sua_lich_buoi_toi and not self.sua_lich_chua_ho_tro:
            raise ValueError("assistant.sua_lich_buoi_toi needs assistant.sua_lich_chua_ho_tro: true")
        if self.sua_lich_kem_hoi and not self.sua_lich_chua_ho_tro:
            raise ValueError("assistant.sua_lich_kem_hoi needs assistant.sua_lich_chua_ho_tro: true")
        if self.toi_nhe and (self.bang_lich_v2 is None or not self.bang_lich_v2.toi_nhe):
            raise ValueError("assistant.toi_nhe needs assistant.len_ke_hoach_v2: true and a schedule table that carries the `toi_nhe` list")
        if self.bo_toi_de_trong and not self.sua_lich_v2:
            raise ValueError("assistant.bo_toi_de_trong needs assistant.sua_lich_v2: true")
        if self.toi_goi_ten and not self.bo_toi_hoi_lai:
            raise ValueError("assistant.toi_goi_ten needs assistant.bo_toi_hoi_lai: true")
        if self.bo_toi_hoi_lai and (self.bo_toi_de_trong or not (self.sua_lich_v2 and self.sua_lich_chua_ho_tro and self.sua_lich_buoi_toi
                                                                 and self.sua_lich_kem_hoi and self.sua_lich_them_khong_the)):
            raise ValueError("assistant.bo_toi_hoi_lai needs sua_lich_v2, sua_lich_chua_ho_tro, sua_lich_buoi_toi, sua_lich_kem_hoi and "
                             "sua_lich_them_khong_the on, and bo_toi_de_trong off")
        if self.sua_lich_hoan_tac and not self.sua_lich_v2:
            raise ValueError("assistant.sua_lich_hoan_tac needs assistant.sua_lich_v2: true")
        if self.sua_lich_them_khong_the and not self.sua_lich_v2:
            raise ValueError("assistant.sua_lich_them_khong_the needs assistant.sua_lich_v2: true")
        if self.sua_lich_them_day and not self.sua_lich_them_khong_the:
            raise ValueError("assistant.sua_lich_them_day needs assistant.sua_lich_them_khong_the: true")
        if self.sua_lich_hoi_truoc and not self.sua_lich_them_khong_the:
            raise ValueError("assistant.sua_lich_hoi_truoc needs assistant.sua_lich_them_khong_the: true")
        if self.sua_lich_them_han_che and not self.sua_lich_them_day:
            raise ValueError("assistant.sua_lich_them_han_che needs assistant.sua_lich_them_day: true")
        if self.sua_lich_them_khu and not (self.sua_lich_them_day and self.khoang_cach):
            raise ValueError("assistant.sua_lich_them_khu needs assistant.sua_lich_them_day and assistant.khoang_cach: true")
        if self.lich_vao_hoi_thuong and not (self.sua_lich_v2 and self.tim_them):
            raise ValueError("assistant.lich_vao_hoi_thuong needs assistant.sua_lich_v2: true and assistant.tim_them: true")
        if self.anh_lich and (not self.len_ke_hoach_v2 or self.anh_lich_bang is None):
            raise ValueError("assistant.anh_lich needs assistant.len_ke_hoach_v2: true and the photo table (assistant.lich_trinh_bang_anh)")
        if self.luu_tru_lich and (not self.len_ke_hoach_v2 or self.luu_tru_bang is None):
            raise ValueError("assistant.luu_tru_lich needs assistant.len_ke_hoach_v2: true and the lodging table (assistant.lich_trinh_bang_luu_tru)")
        if self.quan_trua_kho_truoc and not self.quan_lich:
            raise ValueError("assistant.quan_trua_kho_truoc needs assistant.quan_lich: true")
        if self.quan_lich and (not self.len_ke_hoach_v2 or self.quan_bang is None):
            raise ValueError("assistant.quan_lich needs assistant.len_ke_hoach_v2: true and the restaurant table (assistant.lich_trinh_bang_quan)")
        if self.cong_cong_cu not in ("tu_khoa", "luon", "linh_hoat"):
            raise ValueError(f"cong_cong_cu must be 'tu_khoa', 'luon' or 'linh_hoat', got {self.cong_cong_cu!r}")
        if not set(self.len_ke_hoach_o_hien) <= set(O_BIEU_MAU_V2):
            raise ValueError(f"assistant.len_ke_hoach_o_hien must be a subset of {O_BIEU_MAU_V2}")

    @classmethod
    def from_settings(cls, settings: dict) -> "AssistantFlags":
        config = settings.get("assistant") or {}
        values = {name: bool(config.get(name, cls.__dataclass_fields__[name].default)) for name in BOOL_FIELDS}
        # chỉ nạp khi một trong hai cờ lịch bật (clone không có `data/` vẫn chạy cờ tắt)
        bang = nap_bang_lich(settings) if values["lich_trinh"] or values["lich_trinh_bieu_mau"] else None
        bang_v2 = lt2.nap_bang_v2(BACKEND_DIR / config["lich_trinh_bang_v2"]) if (
            values["len_ke_hoach_v2"] or values["goi_y_mua_nang"] or values["so_sanh_diem_den"]
            or values["tinh_ve_tham_quan"] or values["goi_y_luu_tru"]
        ) else None
        if bang_v2 is not None and not values["toi_nhe"]:  # công tắc tắt ⇒ bộ xếp không thấy danh sách hoạt động tối nhẹ của bảng (luật cũ, khung giống byte)
            bang_v2 = dataclasses.replace(bang_v2, toi_nhe=())
        # toạ độ nạp theo bảng rộng nhất đang dùng: bảng v8 (bản 2, chứa mọi id của v3) khi cờ bản 2 bật, không thì bảng v3 — một dict theo id
        bang_toa_do = bang_v2 or bang
        toa_do = lt.nap_toa_do(BACKEND_DIR / config["lich_trinh_toa_do"], bang_toa_do) if values["ban_do_lich"] and bang_toa_do is not None else None
        sinh = settings.get("full_corpus_generation") or {}
        cong = (sinh.get("bedrock") or {}) if sinh.get("provider") == "bedrock" else config  # cổng công cụ chọn theo provider đang chạy
        muc_luc = lk.nap_muc_luc(*discover_full_corpus_files(settings)) if values["liet_ke_bai"] or values["the_noi"] else None
        bang_kc = kc.nap_bang(BACKEND_DIR / config["khoang_cach_bang"], BACKEND_DIR / config["lich_trinh_bang_v2"]) if values["khoang_cach"] else None
        # công tắc `sua_lich_them_khu` (bản thử): phút đi giữa hai khu không kề cho bộ sửa lịch; tắt ⇒ None ⇒ dấu `khu_them` không có tác dụng
        lt2.dat_phut_khu(lt2.bu_phut_khu(bang_v2, kc.bang_phut(bang_kc)) if values["sua_lich_them_khu"] and bang_kc is not None and bang_v2 is not None else None)
        return cls(**values, lan_tim_dau=str(config.get("lan_tim_dau", "v0")), cong_cong_cu=str(cong.get("cong_cong_cu", "tu_khoa")), so_lan_tim_kho=int(config.get("so_lan_tim_kho", MODEL_SEARCH_LIMIT)),
                   bang_lich=bang, toa_do_lich=toa_do,
                   du_bao=tt.lay_du_bao if values["thoi_tiet"] else None,
                   khoang_cach_bang=bang_kc,
                   su_kien_bang=sk.nap_bang(BACKEND_DIR / config["su_kien_bang"]) if values["su_kien_theo_ngay"] else None,
                   muc_luc=muc_luc if values["liet_ke_bai"] else None,
                   the_noi_bang=thn.dung_bang(muc_luc) if values["the_noi"] else None,
                   len_ke_hoach_o_hien=tuple(config.get("len_ke_hoach_o_hien") or ()),
                   len_ke_hoach_so_thich_an=tuple(config.get("len_ke_hoach_so_thich_an") or ()),
                   bang_lich_v2=bang_v2,
                   anh_lich_bang=lt2.nap_bang_anh(BACKEND_DIR / config["lich_trinh_bang_anh"], bang_v2) if values["anh_lich"] and bang_v2 else None,
                   luu_tru_bang=ltl.nap_bang_luu_tru(BACKEND_DIR / config["lich_trinh_bang_luu_tru"], bang_v2.cum)
                   if (values["luu_tru_lich"] or values["goi_y_luu_tru"]) and bang_v2 else None,
                   quan_bang=ql.nap_bang_quan(BACKEND_DIR / config["lich_trinh_bang_quan"], bang_v2.cum) if (values["quan_lich"] or values["gan_diem"]) and bang_v2 else None,
                   quan_toa_do=lt.nap_toa_do(BACKEND_DIR / config["lich_trinh_toa_do"], bang_v2) if (values["quan_lich"] or values["gan_diem"]) and bang_v2 else None,
                   slide_designer_cfg=dict(settings.get("slide_designer_cfg") or config.get("slide_designer_cfg")
                                           or {"model": "gpt-6-luna", "use_llm": False, "max_retries": 1, "timeout_seconds": 30, "fallback_code_only": True, "reasoning_effort": "low"}))

    @property
    def so_thich_hien(self) -> tuple[str, ...]:
        """Sở thích hiện trên biểu mẫu bản 2: loại đủ điểm trong bảng (≥ 4) trừ loại dưới sàn mô phỏng."""
        if self.bang_lich_v2 is None:
            return ()
        return tuple(s for s in self.bang_lich_v2.loai_hien if s not in self.len_ke_hoach_so_thich_an)

    @property
    def uses_tools(self) -> bool:
        """Tuyến `tro_ly_hue` đi vòng công cụ (trợ lý có `tim_kho`) thay vì sinh một lần."""
        return self.lan_tim_dau == "v2" or self.tim_them


BACKEND_DIR = Path(__file__).resolve().parents[1]  # đường dẫn trong settings tương đối theo `backend/`


def nap_bang_lich(settings: dict) -> "lt.Bang":
    """Bảng điểm lịch trình (B5 D2) từ `assistant.lich_trinh_bang` (tương đối theo `backend/`, như các đường dẫn khác của settings)."""
    return lt.nap_bang(BACKEND_DIR / settings["assistant"]["lich_trinh_bang"])


BOOL_FIELDS = tuple(name for name in AssistantFlags.__dataclass_fields__
                    if name not in ("lan_tim_dau", "cong_cong_cu", "so_lan_tim_kho", "bang_lich", "toa_do_lich", "du_bao", "len_ke_hoach_o_hien", "bang_lich_v2",
                                     "len_ke_hoach_so_thich_an", "anh_lich_bang", "luu_tru_bang", "quan_bang", "quan_toa_do",
                                     "khoang_cach_bang", "su_kien_bang", "muc_luc", "the_noi_bang", "slide_designer_cfg"))


def elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 1)


@dataclass
class AnswerTrace:
    """Một lượt đã đi tới đâu. Lõi điền dần từng bước, nên khi một bước ném lỗi nơi gọi vẫn đọc được các bước trước
    (route: số đo `chat_metrics` của lần lỗi; bộ đánh giá: `top_chunk_ids`, `context_sources`, token của dòng lỗi)."""

    documents: list[RetrievedDocument] | None = None  # toàn bộ kết quả tìm, đúng thứ tự
    search_ms: float | None = None
    dense_ms: float | None = None
    packed: PackedContext | None = None
    context_ms: float | None = None
    generated: GeneratedText | None = None  # None khi ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
    generation_ms: float | None = None
    answer: str | None = None  # chữ gốc của model (chưa chuẩn hóa citation) hoặc câu từ chối chuẩn
    cited: tuple[PackedSource, ...] | None = None  # nguồn được trích; chỉ có khi citation hợp lệ
    citation_ms: float | None = None
    citation_error: CitationIntegrityError | None = None  # citation hỏng: không ném, để mỗi nơi tự xử (spec §4.8 khác biệt 2)
    route: str = ROUTE_TRO_LY_HUE
    # Sổ nguồn của cả lượt: mọi kiểm citation đọc từ đây. B0 một lần tìm ⇒ sổ = nguồn của ngữ cảnh, giữ nguyên số [n];
    # đánh số nối khi tìm nhiều lần (B2b) và phần web [w n] (B6) để plan bậc đó (plan B0 D4).
    so_nguon: list[PackedSource] = field(default_factory=list)
    tools: list[dict] = field(default_factory=list)  # mỗi lần chạy công cụ: {"name", "ms"}
    llm_calls: list[dict] = field(default_factory=list)  # mỗi lần gọi model (generator `CallLog`) + `route` của lần gọi
    # B1: câu trả lời cố định (không qua kiểm citation) ⇒ outcome riêng: "out_of_scope" / "refusal_no_sources" (phương án B G: bỏ "emergency")
    fixed_outcome: str | None = None
    emergency_by: str | None = None  # "router" — định tuyến chọn khan_cap (phương án B G: câu vẫn đi agent Huế, không câu soạn sẵn)
    route_error: str | None = None  # định tuyến lỗi ⇒ đi `tro_ly_hue`
    routing_ms: float | None = None
    today: str | None = None  # dòng ngày đã gửi model (D7) — log chỉ ghi phần ngày
    notice: str | None = None  # dòng H4c (D8)
    luu_y_nguon: str | None = None  # cờ `noi_dong_tam_ngung`: câu an toàn chép từ nguồn, đã nằm trong `notice`; route tách ra để giao diện vẽ nổi
    # B2: câu tìm định tuyến viết (V1 / V3) — chỉ trong RAM, KHÔNG log (chữ người dùng); số câu + cờ rỗng thì log được
    cau_tim: list[str] | None = None
    cau_tim_rong: bool = False
    model_searches: int = 0  # số lần model gọi `tim_kho` (D5 trần)
    model_queries: list[str] = field(default_factory=list)  # câu tìm model viết khi gọi `tim_kho` — KHÔNG log
    context_parts: list[str] = field(default_factory=list)  # chữ ngữ cảnh mỗi lần tìm — đếm ngân sách chung (D5)
    seen_ids: list[str] = field(default_factory=list)  # chunk_id đã vào ngữ cảnh — lần tìm sau bỏ trùng (D5)
    tool_error: Exception | None = None  # lỗi tìm / ngữ cảnh trong công cụ: SDK có thể bọc lại ⇒ lõi ném lại đúng lỗi gốc
    # B3: lịch sử cuộc trò chuyện của lượt này ((câu hỏi, câu trả lời đã cắt), …) — route đọc từ kho; rỗng = không nhớ (B2). KHÔNG log.
    history: tuple[tuple[str, str], ...] = ()
    # cờ `nho_cau_tra_loi` (22/11/2026): route đặt khi ô cuối của `history` đang mang CÂU TRẢ LỜI liền trước — đây là chính lịch sử đó với ô ấy về dòng ghi
    # chú / rỗng (như khi cờ tắt). Lượt bị rút vì lỗi trích dẫn thì `answer_turn_stream_parallel` chạy lại MỘT lần bằng lịch sử này. None = không có gì để lùi.
    lich_su_khong_dap: tuple[tuple[str, str], ...] | None = None
    # B4 D4: lượt ghép mang giá trị trường từ nút (`truong`, `{}` = "Trả lời luôn"); lần tìm đầu dùng câu gốc (m-3) thay vì câu ghép
    truong: dict | None = None
    search_query: str | None = None
    bieu_mau: bool = False  # cổng đợt 1 D3: lượt từ biểu mẫu "Lên kế hoạch" (route đặt; `truong` có đủ giá trị nút, `so_ngay` bắt buộc)
    clarify: dict | None = None  # dữ liệu thẻ hỏi lại (B5 D15: do code của `lich_trinh` dựng)
    # B5: lượt đưa công cụ `lich_trinh` (đếm ngân sách cộng LICH_TRINH_TOOL_OVERHEAD — D16); kết quả lần xếp (khung, số nguồn mỗi điểm…);
    # bước tiến độ đã làm (D14, mã + số / tên điểm — không chữ người dùng); mã vi phạm kiểm cuối (D8). KHÔNG log chữ.
    lich_offered: bool = False
    lich_calls: int = 0
    lich: dict | None = None
    buoc_lich: list[dict] = field(default_factory=list)
    lich_kiem: list[str] | None = None
    # "Lên kế hoạch" bản 2 (`llm/len_ke_hoach.py`): {"lich", "loi_khung", "cau", "loi_cau", "so_cau_du_phong", "loi_model"?}; None = không phải lượt bản 2
    lich_v2: dict | None = None
    # Sửa lịch bản 2: `lich_luu` = lịch đã lưu của cuộc (route nạp khi cờ bật); `sua_chon` = {cu, moi} khi người dùng bấm nút thẻ chọn;
    # `sua` = kết quả áp của lượt (số đếm cho log — không chữ)
    lich_luu: dict | None = None
    sua_chon: dict | None = None
    # cờ `sua_lich_them_khong_the`: câu code đã gợi ý ở lượt ngay trước (route nạp) · câu code gợi ý ở lượt này (route nhớ cho đúng một lượt kế)
    goi_y_sua: tuple = ()
    goi_y_moi: tuple = ()
    sua: dict | None = None
    sua_dong: tuple = ()  # lượt sửa lịch: các dòng do CODE viết ở đầu thẻ (`sua_lich_v2.thay_doi`) — route ghi vào ô lịch sử của lượt (`ghi_chu_sua_lich`); KHÔNG log
    # #6 (plan D2): phần `tro_ly_hue` chạy trước định tuyến rồi bị bỏ vì tuyến khác — số lần, USD (lần gọi xong = usage thật; lần bị huỷ
    # giữa chừng không có usage ⇒ cộng token vào bộ dựng đếm × giá vào = cận dưới), cờ bị huỷ giữa chừng. Chỉ số đếm, không chữ.
    n_tra_loi_bo: int = 0
    usd_bo: float | None = None
    bo_huy_giua: bool | None = None
    # B6: kết quả cổng web — {"outcome", "text", "nguon", "n_ket_qua", "n_ma", "kiem", "usd_serper"}; None = cổng không mở. Chữ web chỉ ở đây
    # (không vào `answer`) ⇒ lịch sử nhớ (`answer`) không bao giờ chứa chữ web (D7). KHÔNG log chữ.
    web: dict | None = None
    # câu nhiều ý vòng 2 (plan 2026-11-14-cau-nhieu-y-v2): cờ bật VÀ câu người dùng có ≥ 2 vế hỏi (`so_y`) ⇒ luật theo ý; khác ⇒ y như cờ tắt
    nhieu_y: bool = False
    chi_y_thieu: bool = False  # chốt (a): câu trả lời chỉ còn dòng CAU_Y_THIEU ⇒ code đã đổi thành INSUFFICIENT_ANSWER
    nho_len_lich: bool = False  # cờ `len_lich_dan_trang`: câu của lượt khớp khuôn nhờ lập lịch nhiều ngày (`_before_model`)
    xin_danh_sach: str | None = None  # cờ `danh_sach_noi_that`: câu người dùng của lượt khi nó khớp khuôn xin danh sách (`_before_model`); KHÔNG log
    lam_thay: str | None = None  # cờ `noi_that_lam_thay`: loại việc "làm thay" code đọc từ câu người dùng (`lam_thay.nho_lam_thay`); None ⇒ lượt như cũ
    # B5b: ngữ cảnh code dò ở câu này (bão / lũ, ngoài 7 ngày, có buổi, có đưa công cụ) · kết quả công cụ `thoi_tiet` (trạng thái, khối số liệu code
    # in) · phần code nối sau chữ model · số thời tiết ngoài tập cho phép (D8). KHÔNG log chữ.
    thoi_tiet_ctx: dict | None = None
    bao_lu_lan_dau: bool = False  # lần chạy lại (`answer_turn_stream_parallel`): lần đầu của lượt model đã tự gọi công cụ thời tiết loại bão / lũ
    thoi_tiet: dict | None = None
    thoi_tiet_noi: str | None = None
    thoi_tiet_dau: str | None = None  # cờ `bao_lu_cong_cu`: câu cố định code đặt TRƯỚC chữ model (lưới khớp, model không gọi công cụ)
    thoi_tiet_kiem: list[str] | None = None
    khoang_cach: list[dict] | None = None  # mỗi lần gọi `khoang_cach`: mã hai điểm + các dòng code dựng (chỉ RAM; log chỉ ghi mã)
    khoang_cach_kiem: list[str] | None = None
    gan_diem: list[dict] | None = None  # mỗi lần gọi `gan_diem`: mã điểm + loại + các dòng code dựng (chỉ RAM; log chỉ ghi mã, loại, số kết quả)
    # 21/11/2026: phép kiểm số (thời tiết / khoảng cách) trượt ⇒ gỡ câu chứa số lạ thay vì rút cả câu trả lời. Ghi lại để đếm: các số lạ theo loại,
    # nấc (1 = gỡ câu, phần còn lại vẫn có nguồn · 2 = không còn gì dùng được ⇒ câu từ chối cố định), số ký tự đã gỡ. None = lượt không trượt.
    kiem_so_go: dict | None = None
    # cờ `liet_ke_bai`: mã nguồn "mục lục" đã đăng ⇒ các bài nó liệt kê (chỉ RAM). `set_notice` dùng để bài CÓ TÊN trong câu trả lời vẫn kéo theo dòng "có thể đã
    # thay đổi" và dòng cảnh báo tạm ngừng của chính bài đó, dù câu trả lời trích mục lục thay cho bài (review 21/11: một lượt mất dòng ghi chú).
    muc_luc_bai: dict = field(default_factory=dict)
    the_noi: list[str] = field(default_factory=list)  # công tắc `the_noi`: tên các nơi đã được gắn thẻ trong lượt (đếm trần; sổ vết ghi để soát nhầm nơi)
    tinh_ve: list[dict] | None = None
    goi_y_luu_tru: list[dict] | None = None
    cuu_max_turns: dict | None = None  # Đợt 1A (`cuu_max_turns`): {"thanh_cong": bool} khi lượt chạm `max_turns` có nguồn đã đi đường viết lại không tool
    # Sổ vết debug (`core/so_vet.py`): nội dung chỉ giữ trong RAM của lượt — `tim` (từng lần tìm), `web` (câu gửi tra web + sổ web), `sua`
    # (hành động model hiểu), `loi`. Route ghi ra file CHỈ khi cờ `so_vet` bật; không vào `chat_metrics`, không vào chuỗi gửi model.
    vet: dict = field(default_factory=dict)


async def search_into_trace(queries: list[str], *, cau_hoi: str, retrieval_service, context_builder, trace: AnswerTrace,
                            today: str | None = None, instructions: str | None = None, by: str = "code",
                            ve_them: Sequence[str] = ()) -> PackedContext:
    """Một lần tìm của lượt: tìm `queries` (1 câu ⇒ `search`; nhiều ⇒ `search_many`, B2 V3) → dựng ngữ cảnh → nối sổ nguồn.
    Ngân sách token đếm bằng `cau_hoi` (câu thật gửi model — B2 D3) + ngữ cảnh các lần trước (`trace.context_parts`) + `instructions` của
    đường trợ lý (B2 D5); lần sau đánh số tiếp, bỏ đoạn đã có. Lần đầu điền `trace.documents` / `trace.packed` (như B1); thời gian cộng dồn.
    `ve_them` (cờ `tim_theo_ve` ở lần tìm ĐẦU; cờ `tach_cau_tim_model` ở lần tìm của model — các phần của câu tìm gộp): mỗi vế tìm riêng một lần, lấy `SO_DOAN_MOI_VE` đoạn đầu, đoạn nào chưa có thì NỐI SAU các
    đoạn của lần tìm chính — các đoạn của lần tìm chính giữ nguyên chữ, thứ tự và số nguồn. Rỗng ⇒ đúng như trước.
    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm)."""
    tool_started = time.perf_counter()
    first = trace.packed is None
    packed = result = None
    n_them = None
    try:
        started = time.perf_counter()
        if len(queries) == 1:
            result = await asyncio.to_thread(retrieval_service.search, queries[0])
        else:
            result = await asyncio.to_thread(retrieval_service.search_many, queries)
        search_ms = elapsed_ms(started)
        dense_ms = result.trace.timings_ms.get("dense_ms")  # trace giữ 3 chữ số; làm tròn 1 chữ số như các trường *_ms khác
        dense_ms = None if dense_ms is None else round(dense_ms, 1)
        if first:  # ghi ngay (như B1): ngữ cảnh lỗi sau đó thì nơi gọi vẫn đọc được số đo + kết quả tìm
            trace.documents, trace.search_ms, trace.dense_ms = result.documents, search_ms, dense_ms
        else:
            trace.search_ms = round((trace.search_ms or 0) + search_ms, 1)
            trace.dense_ms = None if dense_ms is None else round((trace.dense_ms or 0) + dense_ms, 1)

        started = time.perf_counter()
        packed = await asyncio.to_thread(
            context_builder.build, cau_hoi, result.documents, today=today, first_id=len(trace.so_nguon) + 1,
            prior_context="\n\n".join(trace.context_parts), skip_ids=frozenset(trace.seen_ids),
            instructions=instructions, history=trace.history,
            n_tool_items=2 * trace.model_searches if by == "model" else 0,
            extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD if trace.lich_offered else 0,
        )
        context_ms = elapsed_ms(started)
        # lần tìm ĐẦU: lần tìm chính không ra nguồn nào ⇒ giữ đường từ chối cũ, không tìm theo vế. Lần tìm của MODEL (cờ `tach_cau_tim_model`): các phần
        # của câu tìm gộp vẫn được tìm kể cả khi cả câu không mang về đoạn mới nào.
        if ve_them and (packed.sources if first else by == "model"):
            started = time.perf_counter()
            theo_ve = await asyncio.to_thread(lambda: [retrieval_service.search(ve).documents[:SO_DOAN_MOI_VE] for ve in ve_them])
            if first:
                search_ms = round(search_ms + elapsed_ms(started), 1)
                trace.search_ms = search_ms
            else:
                trace.search_ms = round((trace.search_ms or 0) + elapsed_ms(started), 1)
            # xoay vòng theo hạng: đoạn đứng đầu của mọi vế trước, rồi tới đoạn thứ hai — vế nào cũng có phần trước khi vế khác lấy thêm
            ung_vien = list({doan.id: doan for hang in zip_longest(*theo_ve) for doan in hang if doan is not None}.values())  # hai vế ra cùng một đoạn ⇒ một lần
            started = time.perf_counter()
            phu = await asyncio.to_thread(
                context_builder.build, cau_hoi, ung_vien, today=today, first_id=len(trace.so_nguon) + len(packed.sources) + 1,
                prior_context="\n\n".join([*trace.context_parts, packed.text]),
                skip_ids=frozenset([*trace.seen_ids, *packed.document_ids]), instructions=instructions, history=trace.history,
                n_tool_items=2 * trace.model_searches if by == "model" else 0,
                extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD if trace.lich_offered else 0, max_documents=len(ung_vien),
            )
            context_ms = round(context_ms + elapsed_ms(started), 1)
            n_them = len(phu.sources)
            if phu.sources:
                packed = PackedContext(f"{packed.text}\n\n{phu.text}" if packed.text else phu.text, packed.sources + phu.sources, phu.input_tokens,
                                       packed.document_ids + phu.document_ids)
        if first:
            trace.packed, trace.context_ms = packed, context_ms
        else:
            trace.context_ms = round((trace.context_ms or 0) + context_ms, 1)
        trace.so_nguon.extend(packed.sources)
        trace.context_parts.append(packed.text)
        trace.seen_ids.extend(packed.document_ids)
        return packed
    finally:
        entry = {"name": "tim_kho", "ms": elapsed_ms(tool_started)}
        if not first or by == "model" or len(queries) > 1:  # B2: thêm số đo cho lần tìm thêm / do model / nhiều câu; lần tìm đầu một câu giữ như B1
            entry.update(by=by, n_queries=len(queries), n_new=None if packed is None else len(packed.sources))
        if ve_them:  # log chỉ số đếm: số vế tìm riêng, số đoạn nối thêm (None = lỗi trước khi tới bước đó)
            entry.update(n_ve=len(ve_them), n_them_ve=n_them)
        trace.tools.append(entry)
        trace.vet.setdefault("tim", []).append(so_vet.vet_tim(queries, by, None if result is None else result.documents, packed))


async def tim_kho(cau_tim: str, *, retrieval_service, context_builder, trace: AnswerTrace, today: str | None = None,
                  cau_hoi: str | None = None) -> None:
    """Công cụ tìm kho: tìm `cau_tim` → dựng ngữ cảnh, ghi vào `trace` + sổ nguồn. Tham số vị trí là phần model thấy (chỉ `cau_tim`);
    top-k, collection, pool, giới hạn token nằm trong `retrieval_service` / `context_builder` do code dựng (plan B0 D2). `cau_hoi` (B2 D3):
    câu thật gửi model để đếm ngân sách — None ⇒ chính `cau_tim` (B0 / B1)."""
    await search_into_trace([cau_tim], cau_hoi=cau_tim if cau_hoi is None else cau_hoi, retrieval_service=retrieval_service,
                            context_builder=context_builder, trace=trace, today=today)


TRAN_PHAN_CAU_TIM = 3  # nhiều nhất bấy nhiêu phần được tìm riêng cho một câu tìm của model ⇒ thêm nhiều nhất 6 đoạn mỗi lần gọi công cụ
_NOI_CAU_TIM = re.compile(r"\s*;\s*|\s+và\s+|\s*\+\s*")


def cac_phan_cau_tim(cau_tim: str) -> tuple[str, ...]:
    """Cờ `tach_cau_tim_model`: các phần của một câu tìm GỘP do model viết — cắt ở dấu ";", chữ "và", dấu "+"; phần dưới 6 ký tự bỏ. Dưới hai phần ⇒ ()
    (câu tìm một phần không tìm thêm gì). Cắt hỏng (vị ngữ rơi sang phần kia) chỉ tốn vài đoạn thừa: lần tìm cả câu vẫn chạy nguyên như cũ."""
    phan = list(dict.fromkeys(p.strip() for p in _NOI_CAU_TIM.split(cau_tim) if len(p.strip()) >= 6))
    return tuple(phan[:TRAN_PHAN_CAU_TIM]) if len(phan) >= 2 else ()


def the_noi_sau_tim(trace: AnswerTrace, flags: "AssistantFlags", query: str) -> str:
    """Công tắc `the_noi`, gọi ngay sau MỖI lần tìm kho của lượt (lần đầu của code lẫn lần của model): đăng thẻ của các nơi vừa có tên trong ngữ cảnh
    (cả nguồn do công cụ liệt kê / gần-một-điểm dựng trước đó — 22 / 22 cặp ở tin nhiều ý đã ghi có tên tới từ hai công cụ này rồi mới tới một lần tìm)
    thành nguồn của sổ nguồn, trả chữ các nguồn ấy để nối sau kết quả tìm. "" = không có gì để gắn / không thuộc cổng (tin một ý, tin không có chữ hỏi
    hẹp, công tắc tắt, không có bảng) ⇒ nơi gọi không nối gì, chuỗi gửi model giữ nguyên."""
    if not (flags.the_noi and flags.the_noi_bang is not None and trace.nhieu_y and thn.HOI_HEP.search(query)):
        return ""
    bang = flags.the_noi_bang
    noi, ve = thn.the_moi(bang, "\n\n".join(trace.context_parts), frozenset(src.source for src in trace.so_nguon), thn.TRAN_THE - len(trace.the_noi))
    nguon = [(n.ten, (thn.MUC_THE,), n.dong, n.rel) for n in noi if n.dong]
    if ve:  # hàng vé lẻ chép từ bài vé ⇒ nguồn của bài vé (mã nguồn mở đúng bài chứa con số)
        nguon.append((bang.ve_tieu_de, (thn.MUC_VE,), (bang.ve_dau, *ve), bang.ve_rel))
    if not nguon:
        return ""
    dau = len(trace.so_nguon) + 1
    the = [PackedSource(id=dau + i, title=ten, heading_path=muc, excerpts=dong, source=rel) for i, (ten, muc, dong, rel) in enumerate(nguon)]
    trace.so_nguon.extend(the)
    trace.the_noi.extend(n.ten for n in noi)
    # thẻ chỉ chép 1–2 dòng ⇒ câu "tạm ngừng khi lũ / bão" của bài không nằm trong chữ thẻ; ghi bài của thẻ để `set_notice` soi cả bài khi câu trả lời trích
    # thẻ và nêu tên nơi — đúng cách của công cụ liệt kê / gần một điểm (soát của phiên C 22/11: 2 / 113 nơi có thẻ có câu đó, 0 / 2 nằm trong dòng thẻ)
    trace.muc_luc_bai.update({src.id: (n.bai,) for src, n in zip(the, (n for n in noi if n.dong))})
    chu = "\n\n".join(FullCorpusContextBuilder._block(src) for src in the)
    trace.context_parts.append(chu)  # lần tìm sau đếm ngân sách cả chữ thẻ; lần viết lại của lưới (`_viet_lai_het_luot`) mang thẻ theo
    return chu


def tool_for_turn(query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None, instructions: str,
                  search_limit: int = MODEL_SEARCH_LIMIT, tach_cau_tim: bool = False, the_noi_fn=None):
    """Hàm `tim_kho` của **một lượt** cho trợ lý có công cụ (B2 D5): generator bọc thành công cụ SDK (lõi không import SDK — T-3).
    Model chỉ thấy `cau_tim`; trần `MODEL_SEARCH_LIMIT` đếm ở đây; lần vượt ⇒ chữ "đã hết lượt", không tìm. Lỗi tìm / ngữ cảnh: ghi
    `trace.tool_error` rồi ném (lõi ném lại đúng lỗi gốc ⇒ route ra câu lỗi như B1, không đưa lỗi cho model).
    `the_noi_fn` (công tắc `the_noi`): hàm không tham số trả chữ thẻ nơi mới sau lần tìm này — nối SAU kết quả tìm; None ⇒ y như trước."""

    async def tim_kho(cau_tim: str) -> str:
        """Tìm thêm Bằng chứng trong kho tri thức Huế bằng một câu tìm đứng một mình; trả các nguồn mới đánh số tiếp theo.

        Args:
            cau_tim: câu tìm đứng một mình cho phần thông tin còn thiếu.
        """
        trace.model_searches += 1
        trace.model_queries.append(cau_tim)  # chỉ RAM / file private của harness — không log (chữ do model viết từ câu người dùng)
        if trace.lich is not None:  # B5 vòng chỉnh 1 (a): đã có khung lịch + đoạn từng điểm ⇒ không tìm thật, bảo model viết ngay (chặn bằng code)
            trace.tools.append({"name": "tim_kho", "ms": 0.0, "by": "model", "n_queries": 0, "n_new": 0, "sau_lich": True})
            return TOOL_DA_DU_LICH
        if trace.model_searches > search_limit:
            trace.tools.append({"name": "tim_kho", "ms": 0.0, "by": "model", "n_queries": 0, "n_new": 0, "het_luot": True})
            return TOOL_LIMIT_TEXT
        try:
            phan = cac_phan_cau_tim(cau_tim) if tach_cau_tim else ()
            packed = await search_into_trace([cau_tim], cau_hoi=query, retrieval_service=retrieval_service, context_builder=context_builder,
                                             trace=trace, today=today, instructions=instructions, by="model", **({"ve_them": phan} if phan else {}))
        except RetrievalDependencyError as exc:
            trace.tool_error = exc
            raise
        the = the_noi_fn() if the_noi_fn is not None else ""
        if the:  # lần tìm không ra đoạn mới vẫn có thể làm lộ tên nơi cần thẻ (tên tới từ công cụ khác) ⇒ chỉ trả thẻ, không kèm câu "không có nguồn mới"
            return f"{packed.text}\n\n{the}" if packed.text else the
        return packed.text or TOOL_NO_NEW_TEXT

    tim_kho.__doc__ = f"{TIM_KHO_MO_TA}\n\nArgs:\n    cau_tim: câu tìm đứng một mình cho phần thông tin còn thiếu.\n"
    return tim_kho

    return tim_kho


def _the_noi_kwargs(trace: AnswerTrace, flags: "AssistantFlags", query: str) -> dict:
    """Tham số thêm cho `tool_for_turn` — chỉ truyền khi công tắc `the_noi` mở (tắt ⇒ gọi y như trước; test thay `tool_for_turn` không cần tham số mới)."""
    return {"the_noi_fn": lambda: the_noi_sau_tim(trace, flags, query)} if flags.the_noi else {}


def bai_da_tim(trace: AnswerTrace) -> list[dict]:
    """Các BÀI kho đã có đoạn thật trong sổ nguồn của lượt — tên hiển thị + đường dẫn bài, không trùng, theo thứ tự vào ngữ cảnh. Đi kèm sự kiện
    `searched` của lõi stream để giao diện hiện "đã tìm thấy" trong lúc chờ (22/11/2026: tin dài im 17–20 giây sau lần tìm cuối, màn hình chỉ có một dòng).
    KHÔNG tính nguồn do code dựng: thẻ nơi (16 nơi mỗi lượt ở tin gia đình, phần lớn không ai hỏi), mục lục, gần một điểm, khoảng cách, lịch, thời tiết —
    chúng không phải "bài vừa tìm thấy". Đây là bài ĐÃ TÌM THẤY, chưa chắc được trích trong câu trả lời: giao diện phải ghi nhãn đúng như vậy."""
    bai = {}
    for src in trace.so_nguon:
        if src.source.endswith(".md") and src.heading_path not in ((thn.MUC_THE,), (thn.MUC_VE,)):
            bai.setdefault(src.source, src.title)
    return [{"title": ten, "source": rel} for rel, ten in bai.items()]


# Mọi công cụ của trợ lý, một chỗ (test ranh giới khoá tên + tham số; B2 bọc `function_tool` từ đây).
TOOLS = {"tim_kho": tim_kho}


def _history_kwargs(trace: AnswerTrace) -> dict:
    """`history=` chỉ truyền khi có lịch sử: lượt không lịch sử gọi generator y như B2 (generator thay thế trong test không cần tham số này)."""
    return {"history": trace.history} if trace.history else {}


def _assistant_instructions(generator, trace: AnswerTrace, nhieu_y: bool = False, kiem_du_bang_chung: bool = False) -> str:
    """Lời dặn trợ lý thật sự gửi ở lượt này (có câu dặn lịch sử khi có lịch sử — B3 D3) — để đếm ngân sách đúng chuỗi gửi (D5).
    B5: công cụ `lich_trinh` không đổi lời dặn (D7). Không lịch sử ⇒ đọc thẳng thuộc tính (generator thay thế trong test không cần hàm).
    Cờ `cau_nhieu_y` (việc agent (3) 14/11): lời dặn theo ý của đúng bản agent sẽ gửi."""
    if nhieu_y:
        loi_dan = (generator.assistant_history_agent_nhieu_y if trace.history else generator.assistant_agent_nhieu_y).instructions
    else:
        loi_dan = generator.assistant_instructions_for(trace.history) if trace.history else generator.assistant_instructions
    return them_kiem_du_bang_chung(loi_dan) if kiem_du_bang_chung else loi_dan


def lich_trinh_for_turn(query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None, instructions: str, bang,
                        du_bao=None):
    """Hàm `lich_trinh` của **một lượt** (plan B5 bản 7 D1, D6, D14, D15): generator bọc thành công cụ SDK (lõi không import SDK).
    Model chỉ trích trường; **code** chốt số ngày (thiếu ⇒ trả dữ liệu thẻ hỏi lại — `tool_use_behavior` dừng lượt), xếp, kiểm luật, lấy một
    đoạn kho đúng file cho mỗi điểm vào sổ nguồn, rồi trả chữ khung + đoạn mới cho model viết lời. Trần ≤ 1 lần / câu."""

    async def lich_trinh(so_ngay: lt.SoNgay | None, di_cung: lt.DiCung | None, kieu_di: lt.KieuDi | None, so_thich: lt.SoThich | None,
                         them_diem: list[str] | None) -> "str | dict":
        """Xếp lịch tham quan.

        Args:
            so_ngay: số ngày người dùng nói (1, 2, 3, 4+); chưa nói thì null.
            di_cung: người đi cùng nếu người dùng nói; chưa nói thì null.
            kieu_di: thong_tha hoặc day_lich nếu người dùng nói; chưa nói thì null.
            so_thich: sở thích chính nếu người dùng nói; chưa nói thì null.
            them_diem: tên điểm người dùng muốn ghé, đúng chữ người dùng gõ (tối đa 3); không có thì null.
        """
        started = time.perf_counter()
        trace.lich_calls += 1
        entry = {"name": "lich_trinh"}
        try:
            if trace.lich_calls > 1:
                entry["het_luot"] = True
                return "Lịch đã xếp ở lần gọi trước trong lượt này; hãy viết câu trả lời theo khung đó."
            truong = trace.truong
            so_ngay_chot, tam = lt.chot_so_ngay(truong, so_ngay, query)
            if so_ngay_chot is None:  # D15 (4) / D12 (b): code hỏi lại — chỉ số ngày
                entry["hoi_lai"] = True
                return the_hoi_lai("lich_trinh", ["so_ngay"], trace.search_query or query)
            tu_nut = truong or {}
            ts = lt.ThamSo(so_ngay=so_ngay_chot, di_cung=di_cung or tu_nut.get("di_cung"), kieu_di=kieu_di or tu_nut.get("kieu_di"),
                           so_thich=so_thich or tu_nut.get("so_thich"), them_diem=tuple(them_diem or ()), so_ngay_tam=tam,
                           hoi_toi=lt.hoi_buoi_toi(query))
            khung = lt.xep(bang, ts)
            n_xep = len(lt.diem_trong_khung(khung))
            packed, nguon, nguon_ve = await _lay_nguon_lich(bang, khung, query, retrieval_service, context_builder, trace, today, instructions)
            loi = lt.kiem_khung(bang, khung)
            trace.lich = {"khung": khung, "nguon": nguon, "nguon_ve": nguon_ve, "loi_khung": loi}
            if du_bao is not None:  # B5b D9 / D10: dòng dự báo theo ngày đi + "nếu mưa" + bậc thang — chỉ thêm vào ghi chú, khung không đổi
                trace.lich["them_dong"] = await _dong_thoi_tiet_lich(bang, khung, query, du_bao, trace)
            # D14 (a): bước = việc code đã làm xong, đúng thứ tự (`kiem_luat_ok` chỉ khi khung 0 lỗi)
            trace.buoc_lich += [{"buoc": "xep_xong", "n_diem": n_xep},
                                {"buoc": "kiem_luat_ok"} if not loi else {"buoc": "kiem_luat_loi", "n_loi": len(loi)},
                                *({"buoc": "bo_diem", "diem": k["diem"], "ly_do": lt.CAU_KHONG_XEP[k["ma_luat"]].format(diem=k["diem"])}
                                  for k in khung["khong_xep"]),
                                {"buoc": "lay_nguon", "n_doan": len(packed.sources)}]
            entry.update(n_diem=len(lt.diem_trong_khung(khung)), n_new=len(packed.sources), n_khong_xep=len(khung["khong_xep"]))
            chu = lt.khung_chu(bang, khung, nguon, LICH_TRINH_LUAT, nguon_ve)
            trace.context_parts.append(chu)  # lần tìm thêm sau đó (nếu có) đếm cả chữ khung
            return f"{chu}\n\n{packed.text}" if packed.text else chu
        finally:
            entry["ms"] = elapsed_ms(started)
            trace.tools.append(entry)

    return lich_trinh


hom_nay_vn = tt.hom_nay_vn  # một chỗ tính "hôm nay" giờ Việt Nam cho lịch + thời tiết (cache dự báo dùng cùng hàm)


async def _dong_thoi_tiet_lich(bang, khung: dict, query: str, du_bao, trace: AnswerTrace) -> list[str]:
    """B5b D9: lịch có ngày đi trong 7 ngày (code dò — `do_so.do_ngay_di`) ⇒ một dòng dự báo / ngày của lịch + "Nếu mưa: thay <điểm ngoài trời> bằng
    <điểm trong nhà cùng cụm>" khi khả năng mưa ≥ 60 % (cột `trong_nha` của bảng; thiếu cột ⇒ không gợi ý). API lỗi ⇒ một câu cố định, 0 số. Không dò
    được ngày ⇒ không dòng nào (lịch như B5). D10: `bac_thang: nhieu` + người lớn tuổi ⇒ "X có nhiều bậc thang (theo kho)"."""
    ids = lt.diem_trong_khung(khung)
    dong = [f"{bang.theo_id[i]['ten']} có nhiều bậc thang (theo kho)." for i in ids
            if khung["tham_so"].get("di_cung") == "nguoi_lon_tuoi" and bang.theo_id[i].get("bac_thang") == "nhieu"]
    if do_ngay_di(query, hom_nay_vn()) is None:
        return dong
    kq = await du_bao()
    # lưu riêng ở `trace.lich` — không đè kết quả công cụ `thoi_tiet` nếu model cũng gọi trong lượt này
    trace.lich["thoi_tiet"] = {"trang_thai": kq.trang_thai, "loi": kq.loi, "ms": kq.ms, "tu_cache": kq.tu_cache}
    trace.tools.append({"name": "thoi_tiet", "ms": kq.ms, "by": "code", "trang_thai": kq.trang_thai, "loi": kq.loi})
    if kq.trang_thai != "ok":
        return dong + [tt.CAU_LOI]
    bat_dau = do_ngay_di(query, kq.ngay[0]["ngay"])  # ngày theo lịch của API (giờ Việt Nam) — tất định theo bản ghi API
    if bat_dau is None:
        return dong
    co = set(ids)
    for k, ngay in enumerate(khung["ngay"]):
        n = bat_dau + k
        if n >= tt.SO_NGAY:
            break
        d = kq.ngay[n]
        dong.append(f"Ngày {ngay['ngay']} — {tt.dong_ngay(d)}.")
        if d["xs"] is not None and d["xs"] >= tt.NGUONG_MUA:
            ngoai = [i for b in lt.BUOI for i in ngay["buoi"][b] if bang.theo_id[i].get("trong_nha") == "ngoai_troi"]
            for i in ngoai:
                thay = next((x["id"] for x in bang.diem if x.get("trong_nha") in ("trong_nha", "ca_hai") and x["cum"] == bang.theo_id[i]["cum"]
                             and x["id"] not in co), None)
                if thay is not None:
                    dong.append(f"Nếu mưa ngày {ngay['ngay']}: có thể thay {bang.theo_id[i]['ten']} bằng {bang.theo_id[thay]['ten']} (trong nhà).")
                    break
    return dong + [tt.dong_nguon(kq)]


def _nguon_thoi_tiet(trace: AnswerTrace, title: str, excerpts: tuple[str, ...]) -> str:
    """E17 (A chọn): kết quả công cụ thời tiết là **một nguồn thật** trong sổ nguồn (id tiếp theo, khuôn như đoạn kho) ⇒ model trích [k] như mọi
    nguồn; bộ kiểm citation giữ nguyên như `main` (không miễn [n]). Trả chữ nguồn cho model; đếm vào ngân sách như lần tìm thêm."""
    src = PackedSource(id=len(trace.so_nguon) + 1, title=title, heading_path=(tt.MUC_NGUON,), excerpts=excerpts, source=tt.NGUON_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.thoi_tiet["nguon_id"] = src.id
    return chu


def _phan_hoi_lap(ma_nguon: int | None, hanh_dong: str) -> str:
    """Actionable Feedback khi model gọi lặp trùng tham số (cờ `chong_lap_cong_cu`)."""
    if ma_nguon is not None:
        return (f"Trạng thái: đã tra {hanh_dong} với đúng tham số này ở nguồn [{ma_nguon}] phía trên. "
                f"Không gọi lặp lại nữa; hãy dùng ngay bằng chứng đã có ở nguồn [{ma_nguon}] để viết câu trả lời.")
    return (f"Trạng thái: đã {hanh_dong} với đúng tham số này ở lần gọi trước nhưng không có kết quả. "
            "Không gọi lặp lại nữa; hãy dùng ngay bằng chứng đã có để viết câu trả lời (hoặc trả câu không đủ thông tin nếu thiếu).")


def thoi_tiet_for_turn(trace: AnswerTrace, du_bao, chong_lap: bool = False):
    """Hàm `thoi_tiet` của **một lượt** (B5b D3, D5, D7): model chỉ gửi số ngày (0–6); code lấy dự báo, dựng khối số liệu cố định. ≤ 1 lần / câu."""
    Ngay = Literal[0, 1, 2, 3, 4, 5, 6]
    da_goi: dict[tuple, int | None] = {}

    async def thoi_tiet(tu_ngay: Ngay, den_ngay: Ngay) -> str:
        """Lấy dự báo thời tiết Huế theo ngày.

        Args:
            tu_ngay: ngày đầu, tính từ hôm nay (0 = hôm nay, 1 = mai, … 6).
            den_ngay: ngày cuối, tính từ hôm nay (0–6); một ngày thì bằng tu_ngay.
        """
        if (trace.thoi_tiet_ctx or {}).get("dau_hieu_thoi_tiet") is False:
            trace.tools.append({"name": "thoi_tiet", "ms": 0.0, "chan_khong_thoi_tiet": True})
            return (
                "Trạng thái: câu hỏi hiện tại không liên quan đến thời tiết hay thiên tai/bão lũ. "
                "Không dùng công cụ thời tiết cho câu này; hãy trả lời phần còn lại từ bằng chứng đã có."
            )
        khoa = ("du_bao", int(tu_ngay), int(den_ngay))
        if chong_lap and khoa in da_goi:
            trace.tools.append({"name": "thoi_tiet", "ms": 0.0, "lap": True})
            return _phan_hoi_lap(da_goi[khoa], "dự báo thời tiết")
        entry = {"name": "thoi_tiet"}
        try:
            if trace.thoi_tiet is not None:
                entry["het_luot"] = True
                return "Đã lấy dự báo ở lần gọi trước trong lượt này; hãy viết câu trả lời."
            kq = await du_bao()
            trace.thoi_tiet = {"trang_thai": kq.trang_thai, "loi": kq.loi, "ms": kq.ms, "tu_cache": kq.tu_cache, "khoi": None}
            entry.update(ms=kq.ms, trang_thai=kq.trang_thai, loi=kq.loi)
            if kq.trang_thai != "ok":
                out = _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON_LOI, (tt.CAU_LOI,))
                da_goi[khoa] = trace.thoi_tiet.get("nguon_id")
                return out
            tuan_sau = (trace.thoi_tiet_ctx or {}).get("tuan_sau")
            if tuan_sau:  # câu "tuần sau": khoảng ngày do code tính, bỏ số ngày model gửi
                tu_ngay, den_ngay = tuan_sau
            khoi = tt.khoi_du_bao(kq, tu_ngay, den_ngay, bool(trace.thoi_tiet_ctx and trace.thoi_tiet_ctx["buoi"]), tuan_sau=bool(tuan_sau))
            trace.thoi_tiet.update(khoi=khoi, n_ngay=abs(den_ngay - tu_ngay) + 1)
            out = _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON, tuple(x for x in khoi.splitlines()[1:] if x))  # bỏ dòng tiêu đề; còn dòng ngày + dòng ghi công / giờ
            da_goi[khoa] = trace.thoi_tiet.get("nguon_id")
            return out
        finally:
            entry.setdefault("ms", 0.0)
            trace.tools.append(entry)

    if (trace.thoi_tiet_ctx or {}).get("bao_lu_cong_cu"):
        return _thoi_tiet_bao_lu(trace, du_bao, thoi_tiet, chong_lap=chong_lap)
    return thoi_tiet


def _thoi_tiet_bao_lu(trace: AnswerTrace, du_bao, cu, chong_lap: bool = False):
    """Bản công cụ của cờ `bao_lu_cong_cu` (plan 17/11 §2): thêm `loai` (bắt buộc). `du_bao` ⇒ y như bản cũ (`cu`). `bao_lu` (hoặc lưới code đã
    khớp) ⇒ cả lượt là lượt bão / lũ: code lấy dự báo, ghi khối có nhãn "không phải tin bão" vào `trace.thoi_tiet["khoi"]` NGAY TRONG lần gọi này (đường
    stream giữ chữ khi câu có thể là câu từ chối), model chỉ nhận một nguồn KHÔNG có số (`tt.KET_QUA_BAO_LU`)."""
    Ngay = Literal[0, 1, 2, 3, 4, 5, 6]
    Loai = Literal["du_bao", "bao_lu"]
    da_goi: dict[tuple, int | None] = {}

    async def thoi_tiet(loai: Loai, tu_ngay: Ngay, den_ngay: Ngay) -> str:
        ctx = trace.thoi_tiet_ctx
        if ctx is not None and ctx.get("dau_hieu_thoi_tiet") is False:
            trace.tools.append({"name": "thoi_tiet", "loai": loai, "ms": 0.0, "chan_khong_thoi_tiet": True})
            return (
                "Trạng thái: câu hỏi hiện tại không liên quan đến thời tiết hay thiên tai/bão lũ. "
                "Không dùng công cụ thời tiết cho câu này; hãy trả lời phần còn lại từ bằng chứng đã có."
            )
        khoa = (str(loai).strip().casefold(), int(tu_ngay), int(den_ngay))
        if chong_lap and khoa in da_goi:
            trace.tools.append({"name": "thoi_tiet", "loai": loai, "ms": 0.0, "lap": True})
            return _phan_hoi_lap(da_goi[khoa], "dự báo thời tiết")
        if loai == "bao_lu":
            ctx["bao_lu"] = ctx["bao_lu_model"] = True  # một lần bao_lu thì cả lượt là bao_lu (plan m-4)
        if ctx["bao_lu"] and trace.thoi_tiet is not None and not trace.thoi_tiet.get("bao_lu") and trace.thoi_tiet.get("khoi"):
            # soát 18/11: lưới không khớp, model gọi `du_bao` TRƯỚC (đã nhận số) rồi mới gọi `bao_lu`. Số đã gửi thì không lấy lại được; từ đây vẫn phải
            # là lượt bão: khối nối dưới câu trả lời có nhãn "không phải tin bão", lần gọi này trả lời dặn không số thay cho câu "đã lấy"
            trace.thoi_tiet.update(bao_lu=True, khoi=f"{tt.CAU_KHONG_PHAI_TIN_BAO}\n\n{trace.thoi_tiet['khoi']}")
            trace.tools.append({"name": "thoi_tiet", "loai": "bao_lu", "ms": 0.0, "sau_du_bao": True})
            out = _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON_BAO_LU, (tt.KET_QUA_BAO_LU,))
            da_goi[khoa] = trace.thoi_tiet.get("nguon_id")
            return out
        if not ctx["bao_lu"] or trace.thoi_tiet is not None:
            return await cu(tu_ngay, den_ngay)  # lần gọi thứ hai ⇒ câu "đã lấy" của bản cũ (hoặc `chong_lap` trong `cu` nếu trùng `du_bao`)
        entry = {"name": "thoi_tiet", "loai": "bao_lu"}
        try:
            kq = await du_bao()
            trace.thoi_tiet = {"trang_thai": kq.trang_thai, "loi": kq.loi, "ms": kq.ms, "tu_cache": kq.tu_cache, "khoi": None, "bao_lu": True}
            entry.update(ms=kq.ms, trang_thai=kq.trang_thai, loi=kq.loi)
            if kq.trang_thai != "ok":
                out = _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON_LOI, (tt.CAU_LOI,))
                da_goi[khoa] = trace.thoi_tiet.get("nguon_id")
                return out
            if ctx.get("tuan_sau"):  # như bản cũ: câu "tuần sau" ⇒ khoảng ngày do code tính
                tu_ngay, den_ngay = ctx["tuan_sau"]
            khoi = tt.khoi_du_bao(kq, tu_ngay, den_ngay, bool(ctx["buoi"]), tuan_sau=bool(ctx.get("tuan_sau")))
            trace.thoi_tiet.update(khoi=f"{tt.CAU_KHONG_PHAI_TIN_BAO}\n\n{khoi}", n_ngay=abs(den_ngay - tu_ngay) + 1)
            out = _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON_BAO_LU, (tt.KET_QUA_BAO_LU,))
            da_goi[khoa] = trace.thoi_tiet.get("nguon_id")
            return out
        finally:
            entry.setdefault("ms", 0.0)
            trace.tools.append(entry)

    thoi_tiet.mo_ta = THOI_TIET_BAO_LU_MO_TA  # generator đọc mô tả này thay `THOI_TIET_MO_TA`
    return thoi_tiet


def ngay_lich_for_turn(trace: AnswerTrace, query: str = "", chong_lap: bool = False):
    """Hàm `ngay_lich` của **một lượt** (T1): model chỉ gửi loại lịch + số; code tính, dựng chữ, đăng thành **một nguồn** trong sổ nguồn (như
    `_nguon_thoi_tiet` — câu chỉ có ngày vẫn trích được [n]). ≤ 2 lần / câu (lần thứ 3 ⇒ câu nhắc, không tính)."""
    LoaiLich = Literal["hom_nay", "duong", "am"]
    da_goi: dict[tuple, int | None] = {}

    async def ngay_lich(loai: LoaiLich, ngay: int, thang: int, nam: int, thang_nhuan: bool) -> str:
        """Hôm nay theo giờ Việt Nam và đổi ngày dương ↔ âm lịch Việt Nam.

        Args:
            loai: "hom_nay" (chỉ hôm nay), "duong" (đổi ngày dương sang âm) hoặc "am" (đổi ngày âm sang dương).
            ngay: ngày cần đổi (0 khi loai là "hom_nay").
            thang: tháng cần đổi (0 khi loai là "hom_nay").
            nam: năm cần đổi; 0 = người dùng không nêu năm (công cụ trả lần gần nhất đã qua và lần sắp tới).
            thang_nhuan: true nếu là tháng âm nhuận.
        """
        lan = sum(t["name"] == "ngay_lich" for t in trace.tools)
        entry = {"name": "ngay_lich", "ms": 0.0, "loai": loai, "nam": nam}  # 09/11: `nam` để biết model gửi năm nào (chỉ số, không chữ)
        trace.tools.append(entry)
        loai_chuan = str(loai).strip().casefold()
        khoa = ("hom_nay",) if loai_chuan == "hom_nay" else (loai_chuan, int(ngay), int(thang), int(nam), bool(thang_nhuan))
        if chong_lap and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "đổi ngày âm/dương")
        if lan >= 2:
            entry["het_luot"] = True
            return "Đã đổi ngày ở các lần gọi trước trong lượt này; hãy viết câu trả lời."
        # (i) A 08/11: khoảng "tuần này / tuần sau / tháng này" do code ghi — xét câu cuối + câu hỏi liền trước (như bộ dò)
        cau = " ".join([query] + ([trace.history[-1][0]] if trace.history else []))
        dong = nl.ket_qua(loai, ngay, thang, nam, thang_nhuan, cau=cau).splitlines()
        src = PackedSource(id=len(trace.so_nguon) + 1, title=nl.TIEU_DE_NGUON, heading_path=(nl.MUC_NGUON,), excerpts=tuple(dong), source=nl.NGUON_SOURCE)
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    return ngay_lich


def khoang_cach_for_turn(trace: AnswerTrace, bang: "kc.BangKhoangCach", trang_thai: bool = False, chong_lap: bool = False):
    """Hàm `khoang_cach` của **một lượt** (plan 16/11): model chỉ gửi MÃ hai điểm (enum, `khac` = nơi ngoài danh sách); code tra bảng, dựng dòng,
    đăng thành **một nguồn** trong sổ nguồn (như `ngay_lich_for_turn`). ≤ 3 lần / câu (câu hỏi nhiều cặp); lần thứ 4 ⇒ câu nhắc."""
    Ma = Literal[tuple(bang.ids) + (kc.KHAC,)]
    da_goi: dict[tuple, int | None] = {}

    async def khoang_cach(diem_a: Ma, diem_b: Ma) -> str:
        entry = {"name": "khoang_cach", "ms": 0.0, "diem_a": diem_a, "diem_b": diem_b}  # mã điểm do model chọn (không chữ người dùng)
        trace.tools.append(entry)
        khoa = (str(diem_a).strip().casefold(), str(diem_b).strip().casefold())
        if chong_lap and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "tra khoảng cách")
        if trace.khoang_cach is not None and len(trace.khoang_cach) >= 3:
            entry["het_luot"] = True
            return "Đã tra khoảng cách ở các lần gọi trước trong lượt này; hãy viết câu trả lời."
        dong = kc.ket_qua(bang, diem_a, diem_b)
        trace.khoang_cach = (trace.khoang_cach or []) + [{"diem_a": diem_a, "diem_b": diem_b, "dong": dong}]
        src = PackedSource(id=len(trace.so_nguon) + 1, title=kc.TIEU_DE_NGUON, heading_path=(kc.MUC_NGUON,), excerpts=dong, source=kc.NGUON_SOURCE)
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        if trang_thai and len(dong) == 1:  # `kc.ket_qua` trả đúng MỘT dòng khi không có số (nơi ngoài danh sách / cặp chưa có / hai mã trùng)
            entry["khong_co"] = True
            return f"{kc.TRANG_THAI_KHONG_CO}\n\n{chu}"
        return chu

    khoang_cach.__doc__ = kc.mo_ta_cong_cu(bang)
    return khoang_cach


def gan_diem_for_turn(trace: AnswerTrace, bang: "kc.BangKhoangCach", quan_theo_cum: dict, toa_do: dict, bai_theo_rel: dict | None = None,
                      bai_diem: dict | None = None, in_gio: bool = False, chong_lap: bool = False):
    """Hàm `gan_diem` của **một lượt** (cờ `gan_diem`): model chỉ gửi MÃ một điểm (enum của bảng khoảng cách, `khac` = nơi ngoài danh sách) + loại; code
    tính (`llm/gan_diem.py`), đăng thành **một nguồn** trong sổ nguồn (như `khoang_cach_for_turn`). ≤ 3 lần / câu; lần thứ 4 ⇒ câu nhắc. Các dòng code
    dựng vào `trace.gan_diem` ⇒ số km / phút trong đó thuộc tập "số code dựng" của phép kiểm số sau khi viết."""
    Ma = Literal[tuple(bang.ids) + (kc.KHAC,)]
    Loai = Literal[gd.LOAI]
    da_goi: dict[tuple, int | None] = {}

    async def gan_diem(diem: Ma, loai: Loai) -> str:
        entry = {"name": "gan_diem", "ms": 0.0, "diem": diem, "loai": loai}  # mã điểm + loại do model chọn (không chữ người dùng)
        trace.tools.append(entry)
        khoa = (str(diem).strip().casefold(), str(loai).strip().casefold())
        if chong_lap and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "tìm điểm ở gần")
        if trace.gan_diem is not None and len(trace.gan_diem) >= 3:
            entry["het_luot"] = True
            return "Đã tra những gì ở gần ở các lần gọi trước trong lượt này; hãy viết câu trả lời."
        dong, n = gd.ket_qua(bang, quan_theo_cum, toa_do, diem, loai, in_gio=in_gio)
        entry["n"] = n
        trace.gan_diem = (trace.gan_diem or []) + [{"diem": diem, "loai": loai, "dong": dong}]
        src = PackedSource(id=len(trace.so_nguon) + 1, title=gd.tieu_de(bang, diem, loai), heading_path=(gd.MUC_NGUON,), excerpts=dong, source=gd.NGUON_SOURCE)
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        # K5 (soát khác hãng 22/11): bài kho của từng nơi vừa kể, mang TÊN NƠI như nguồn in ⇒ `set_notice` nối câu an toàn / dòng "có thể đã thay đổi"
        # của bài khi câu trả lời nêu tên nơi đó — đúng cách của công cụ liệt kê (`muc_luc_bai`). Không có mục lục (cờ `liet_ke_bai` tắt) ⇒ như cũ.
        if bai_theo_rel:
            trace.muc_luc_bai[src.id] = tuple(dataclasses.replace(bai_theo_rel[rel], tieu_de=ten)
                                              for ten, rel in gd.noi_co_bai(bang, quan_theo_cum, toa_do, bai_diem or {}, diem, loai) if rel in bai_theo_rel)
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    gan_diem.__doc__ = gd.mo_ta_cong_cu(bang)
    gan_diem.mo_ta_ngan = gd.mo_ta_ngan
    return gan_diem


def liet_ke_for_turn(trace: AnswerTrace, muc_luc: "tuple[lk.Bai, ...]", chong_lap: bool = False):
    """Hàm `liet_ke_bai` của **một lượt**: model gửi nhóm (enum) + cụm từ; code lọc mục lục kho, đăng danh sách thành **một nguồn** trong sổ nguồn (như
    `khoang_cach_for_turn`) ⇒ tên nơi lấy từ danh sách trích được [n] và qua bộ kiểm trích nguồn hiện có. Không bài nào khớp ⇒ chỉ dòng trạng thái, không
    đăng nguồn. ≤ `lk.SO_LAN_MOI_LUOT` lần / câu. Sổ vết ghi nhóm + số cụm từ + số bài, không ghi chữ model viết."""
    Nhom = Literal[tuple(lk.NHOM) + (lk.TAT_CA,)]
    da_goi: dict[tuple, int | None] = {}  # (nhóm, cụm từ đã chuẩn) ⇒ mã nguồn đã đăng (None = lần đó không có bài khớp)

    async def liet_ke_bai(nhom: Nhom, cum_tu: list[str]) -> str:
        """Liệt kê bài của kho theo nhóm, lọc theo cụm từ.

        Args:
            nhom: nhóm bài — quan_an (quán ăn), quan_ca_phe (quán cà phê), mon_dac_san (món đặc sản), le_hoi (lễ hội), di_tich (di tích: lăng, chùa, cung
                điện, bảo tàng…), nghe_thuat (nghệ thuật biểu diễn), diem_den (điểm đến: bãi biển, chợ, làng, núi, phố…), dich_vu (dịch vụ du lịch), ve
                (vé); tat_ca khi không chắc nhóm.
            cum_tu: 0 đến 3 cụm từ ngắn, có dấu; bài được giữ khi tên hoặc nội dung chứa ít nhất một cụm. Mảng rỗng = mọi bài của nhóm.
        """
        lan = sum(t["name"] == "liet_ke_bai" for t in trace.tools)
        entry = {"name": "liet_ke_bai", "ms": 0.0, "nhom": nhom, "n_cum_tu": len(cum_tu)}
        trace.tools.append(entry)
        cuoi = "\n\n" + lk.LAN_CUOI if lan == lk.SO_LAN_MOI_LUOT - 1 else ""
        if chong_lap:
            cum_chuan = tuple(sorted(dict.fromkeys(
                c for c in (lk.chuan(x) for x in cum_tu[:lk.TOI_DA_CUM_TU]) if c and len(c) <= lk.CUM_TU_DAI_NHAT
            )))
            khoa_chuan = (str(nhom).strip().casefold(), cum_chuan)
            if khoa_chuan in da_goi:
                entry["lap"] = True
                return _phan_hoi_lap(da_goi[khoa_chuan], "liệt kê bài") + cuoi
        if lan >= lk.SO_LAN_MOI_LUOT:
            entry["het_luot"] = True
            return "Trạng thái: đã dùng hết lượt của công cụ này trong câu — viết câu trả lời từ Bằng chứng đã có."
        kq = lk.loc(muc_luc, nhom, cum_tu)
        entry.update(n_bai=kq.tong, n_o_ten=kq.o_ten)
        # lượt thật 21/11 (luna): model gọi lại Y NGUYÊN nhóm + cụm từ, rồi xin lần thứ ba ⇒ tốn hai vòng, một lượt chạm trần vòng và thành câu từ chối.
        # Lời gọi trùng ⇒ không đăng nguồn lần hai, chỉ dòng trỏ về kết quả đã có; lần dùng cuối ⇒ nói rõ là lần cuối (model không xin thêm một vòng vô ích).
        khoa = (str(nhom).strip().casefold(), tuple(sorted(kq.cum_tu))) if chong_lap else (nhom, kq.cum_tu)
        if khoa in da_goi:
            entry["lap"] = True
            return (_phan_hoi_lap(da_goi[khoa], "liệt kê bài") if chong_lap else lk.trang_thai_lap(da_goi[khoa])) + cuoi
        if kq.tong == 0:
            da_goi[khoa] = None
            return lk.trang_thai(kq) + cuoi
        src = PackedSource(id=len(trace.so_nguon) + 1, title=lk.TIEU_DE_NGUON, heading_path=(lk.muc_nguon(nhom, kq),), excerpts=kq.dong, source=lk.NGUON_SOURCE)
        trace.so_nguon.append(src)
        trace.muc_luc_bai[src.id] = kq.bai
        da_goi[khoa] = src.id
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return f"{lk.trang_thai(kq)}\n\n{chu}{cuoi}"

    # generator hỏi hàm này trước MỖI lần gọi model (như `con_luot_fn` của `tim_kho`): đã dùng đủ số lần ⇒ lần gọi đó không gửi công cụ nữa. Lượt thật
    # 21/11 (luna): lần xin thứ ba chỉ nhận dòng "hết lượt" nhưng ăn mất vòng viết ⇒ chạm trần vòng ⇒ câu từ chối.
    liet_ke_bai.con_luot = lambda: sum(t["name"] == "liet_ke_bai" for t in trace.tools) < lk.SO_LAN_MOI_LUOT
    return liet_ke_bai


def mua_nang_for_turn(trace: AnswerTrace, query: str, bang: "lt2.BangV2", bang_kc: "kc.BangKhoangCach | None", du_bao,
                      bai_theo_rel: dict | None = None, chong_lap: bool = False, toi_uu: bool = False):
    """Hàm `goi_y_phuong_an_mua_nang` của **một lượt** (Đợt 2, cờ `goi_y_mua_nang`): chặn tuyệt đối khi là lượt bão/lũ hoặc ngày chọn có mưa
    >= 100 mm/ngày; dùng chung `du_bao` (cache 30p Open-Meteo), lọc `diem_v16` trong nhà / mái che theo buổi & cụm, đăng tối đa 5 điểm
    thành 1 nguồn `[n]`, gắn `trace.muc_luc_bai[src.id]` để giữ cảnh báo tạm ngừng/thay đổi."""
    TinhHuong = Literal[mn.TINH_HUONG]
    DiemGoc = Literal[tuple(bang.theo_id) + (mn.KHONG_RO,)]
    Buoi = Literal[mn.BUOI_LUA_CHON]
    Ngay = Literal[0, 1, 2, 3, 4, 5, 6]
    da_goi: dict[tuple, int | None] = {}

    async def goi_y_phuong_an_mua_nang(tinh_huong: TinhHuong, diem_goc: DiemGoc = mn.KHONG_RO, buoi: Buoi = "ca_ngay",
                                       ngay: Ngay | None = None) -> str:
        lan = sum(t["name"] == "goi_y_phuong_an_mua_nang" for t in trace.tools)
        entry = {"name": "goi_y_phuong_an_mua_nang", "ms": 0.0, "tinh_huong": tinh_huong, "diem_goc": diem_goc, "buoi": buoi, "ngay": ngay}
        trace.tools.append(entry)
        ngay_chuan = int(ngay) if ngay is not None else None
        khoa = (str(tinh_huong).strip().casefold(), str(diem_goc).strip().casefold(), str(buoi).strip().casefold(), ngay_chuan)
        if chong_lap and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "gợi ý điểm tránh mưa/nắng")
        if lan >= mn.SO_LAN_MOI_LUOT:
            entry["het_luot"] = True
            return "Trạng thái: đã dùng hết lượt của công cụ gợi ý mưa/nắng trong câu — hãy viết câu trả lời từ Bằng chứng đã có."
        ctx = trace.thoi_tiet_ctx or {}
        if _la_luot_nguy_hiem_bao_lu(query, trace):
            trace.thoi_tiet_ctx = {**ctx, "bao_lu": True, "bao_lu_model": True}
            entry["bao_lu"] = True
            return mn.CAU_CHAN_BAO_LU
        kq_du_bao = None
        if du_bao is not None and (ngay_chuan is not None or tt.co_tu_khoa_luot_rong(query, trace.history)):
            kq_du_bao = await du_bao()
        started = time.perf_counter()
        dong, chon, nguy_hiem = mn.ket_qua(bang, bang_kc, tinh_huong, diem_goc, buoi, ngay_chuan, kq_du_bao=kq_du_bao, hom_nay=hom_nay_vn(), toi_uu=toi_uu)
        entry["ms"] = elapsed_ms(started)
        if nguy_hiem:
            trace.thoi_tiet_ctx = {**ctx, "bao_lu": True, "bao_lu_model": True}
            entry["bao_lu"] = True
            return mn.CAU_CHAN_BAO_LU
        entry["n_ket_qua"] = len(chon)
        if not chon:
            da_goi[khoa] = None
            return dong[0]
        src = PackedSource(id=len(trace.so_nguon) + 1, title=mn.TIEU_DE_NGUON, heading_path=(mn.MUC_NGUON,), excerpts=dong, source=mn.NGUON_SOURCE)
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        if bai_theo_rel:
            trace.muc_luc_bai[src.id] = tuple(
                dataclasses.replace(bai_theo_rel[d["nguon"]], tieu_de=d["ten"])
                for d in chon if d.get("nguon") in bai_theo_rel
            )
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    goi_y_phuong_an_mua_nang.__doc__ = mn.mo_ta_cong_cu(bang)
    goi_y_phuong_an_mua_nang.mo_ta_ngan = mn.mo_ta_ngan
    goi_y_phuong_an_mua_nang.mo_ta_toi_uu = mn.mo_ta_cong_cu(bang, toi_uu=True)
    return goi_y_phuong_an_mua_nang


def so_sanh_for_turn(trace: AnswerTrace, bang: "lt2.BangV2", bang_kc: "kc.BangKhoangCach | None", the_noi_bang: "thn.Bang | None",
                     bai_theo_rel: dict | None = None, chong_lap: bool = False, toi_uu: bool = False):
    """Hàm `so_sanh_diem_den` của **một lượt** (Đợt 2, cờ `so_sanh_diem_den`): so sánh 2–3 điểm enum từ `diem_v16`, đọc giờ/vé nguyên văn từ
    `the_noi_bang` (tuyệt đối không dùng `gio_mo_cua`) và khoảng cách từ `khoang_cach_bang`, đăng thành 1 nguồn `[n]`."""
    Ma = Literal[tuple(bang.theo_id)]
    MaTuyChon = Literal[tuple(bang.theo_id) + (ss.KHONG_CO,)]
    da_goi: dict[tuple, int | None] = {}
    bai_map = bai_theo_rel or ({n.rel: n.bai for n in the_noi_bang.noi} if the_noi_bang is not None else {})

    async def so_sanh_diem_den(diem_1: Ma, diem_2: Ma, diem_3: MaTuyChon = ss.KHONG_CO) -> str:
        lan = sum(t["name"] == "so_sanh_diem_den" for t in trace.tools)
        entry = {"name": "so_sanh_diem_den", "ms": 0.0, "diem_1": diem_1, "diem_2": diem_2, "diem_3": diem_3}
        trace.tools.append(entry)
        ids_chuan = ss.chuan_danh_sach_ma(bang, (diem_1, diem_2, diem_3))
        khoa = tuple(sorted(ids_chuan))
        if chong_lap and khoa and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "so sánh điểm đến")
        if lan >= ss.SO_LAN_MOI_LUOT:
            entry["het_luot"] = True
            return "Trạng thái: đã dùng hết lượt của công cụ so sánh trong câu — hãy viết câu trả lời từ Bằng chứng đã có."
        started = time.perf_counter()
        dong, chon = ss.ket_qua(bang, bang_kc, the_noi_bang, (diem_1, diem_2, diem_3), toi_uu=toi_uu)
        entry["ms"] = elapsed_ms(started)
        entry["n_ket_qua"] = len(chon)
        if not chon:
            return ss.CAU_THIEU_DIEM
        src = PackedSource(id=len(trace.so_nguon) + 1, title=ss.TIEU_DE_NGUON, heading_path=(ss.MUC_NGUON,), excerpts=dong, source=ss.NGUON_SOURCE)
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        if bai_map:
            trace.muc_luc_bai[src.id] = tuple(
                dataclasses.replace(bai_map[d["nguon"]], tieu_de=d["ten"])
                for d in chon if d.get("nguon") in bai_map
            )
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    so_sanh_diem_den.__doc__ = ss.mo_ta_cong_cu(bang)
    so_sanh_diem_den.mo_ta_ngan = ss.mo_ta_ngan
    so_sanh_diem_den.mo_ta_toi_uu = ss.mo_ta_cong_cu(bang, toi_uu=True)
    return so_sanh_diem_den


def tinh_ve_for_turn(trace: AnswerTrace, bang: "lt2.BangV2 | None" = None, the_noi_bang: "thn.Bang | None" = None,
                     bai_theo_rel: dict | None = None, chong_lap: bool = False, toi_uu: bool = False):
    """Hàm `tinh_ve_va_gio_tham_quan` của **một lượt** (Đợt 6, cờ `tinh_ve_tham_quan`): tính chính xác vé lẻ 12 điểm Quần thể vs combo tối ưu,
    tách riêng Hải Vân Quan, trẻ em, giảm 50% công dân VN >=60t, 5 ngày lễ miễn phí và kiểm kịp giờ đóng cửa."""
    Diem = Literal[tv.DIEM_IDS]
    da_goi: dict[tuple, int | None] = {}
    bai_map = bai_theo_rel or ({n.rel: n.bai for n in the_noi_bang.noi} if the_noi_bang is not None else {})

    async def tinh_ve_va_gio_tham_quan(
        diem: list[Diem],
        ngay: str = "",
        gio_bat_dau: str = "",
        so_nguoi_lon: int = 1,
        so_tre_7_12: int = 0,
        so_tre_duoi_7: int = 0,
        so_nguoi_cao_tuoi_vn: int = 0,
        la_cong_dan_vn: bool = True,
        cu_tru_hue: bool = False,
    ) -> str:
        """Tính vé tham quan Huế (lẻ vs tuyến gộp tối ưu) và kiểm tra ngày nghỉ / kịp giờ đóng cửa.

        Args:
            diem: danh sách mã điểm muốn tính vé (enum mã điểm chuẩn).
            ngay: ngày đi (YYYY-MM-DD hoặc DD/MM/YYYY, bỏ trống nếu chưa rõ).
            gio_bat_dau: giờ dự kiến bắt đầu (HH:MM, bỏ trống nếu chưa rõ).
            so_nguoi_lon: số người lớn 13–59 tuổi (hoặc >=60t nước ngoài; đặt 0 nếu đoàn chỉ gồm người cao tuổi VN).
            so_tre_7_12: số trẻ em 7–12 tuổi (nếu biết cao dưới 1,2 m thì tính vào `so_tre_duoi_7`).
            so_tre_duoi_7: số trẻ em dưới 7 tuổi hoặc cao dưới 1,2 m.
            so_nguoi_cao_tuoi_vn: số công dân Việt Nam từ đủ 60 tuổi trở lên (giảm 50% ở các điểm áp dụng).
            la_cong_dan_vn: True nếu là công dân Việt Nam, False nếu khách quốc tế.
            cu_tru_hue: True nếu có thường trú tại Huế (ảnh hưởng giá Lê Bá Đảng / Sốnglab).
        """
        lan = sum(t["name"] == "tinh_ve_va_gio_tham_quan" for t in trace.tools)
        diem_list = [str(x).strip() for x in (diem or ()) if str(x).strip()]
        entry = {"name": "tinh_ve_va_gio_tham_quan", "ms": 0.0, "n_diem": len(diem_list)}
        trace.tools.append(entry)
        khoa = (
            tuple(sorted(x.casefold() for x in diem_list)),
            (ngay or "").strip(),
            (gio_bat_dau or "").strip(),
            int(so_nguoi_lon),
            int(so_tre_7_12),
            int(so_tre_duoi_7),
            int(so_nguoi_cao_tuoi_vn),
            bool(la_cong_dan_vn),
            bool(cu_tru_hue),
        )
        if chong_lap and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "tính vé và giờ tham quan")
        if lan >= 3:
            entry["het_luot"] = True
            return "Trạng thái: đã tính vé ở các lần gọi trước trong lượt này; hãy viết câu trả lời từ Bằng chứng đã có."
        started = time.perf_counter()
        text_out, sources = tv.ket_qua(
            diem_list,
            ngay=ngay,
            gio_bat_dau=gio_bat_dau,
            so_nguoi_lon=so_nguoi_lon,
            so_tre_7_12=so_tre_7_12,
            so_tre_duoi_7=so_tre_duoi_7,
            so_nguoi_cao_tuoi_vn=so_nguoi_cao_tuoi_vn,
            la_cong_dan_vn=la_cong_dan_vn,
            cu_tru_hue=cu_tru_hue,
            bang_v2=bang,
            the_noi_bang=the_noi_bang,
        )
        entry["ms"] = elapsed_ms(started)
        trace.tinh_ve = (trace.tinh_ve or []) + [{"diem": diem_list, "ngay": ngay, "gio_bat_dau": gio_bat_dau}]
        src_rel = sources[0]
        src = PackedSource(
            id=len(trace.so_nguon) + 1,
            title=tv.TEN_NGUON.get(src_rel, "Vé tham quan Huế"),
            heading_path=("Bảng tính vé và giờ tham quan",),
            excerpts=tuple(line for line in text_out.splitlines() if line.strip()),
            source=src_rel,
        )
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        if bai_map:
            trace.muc_luc_bai[src.id] = tuple(bai_map[s] for s in sources if s in bai_map)
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    tinh_ve_va_gio_tham_quan.__doc__ = tv.mo_ta_cong_cu(toi_uu=False)
    tinh_ve_va_gio_tham_quan.mo_ta_toi_uu = tv.mo_ta_cong_cu(toi_uu=True)
    return tinh_ve_va_gio_tham_quan


def goi_y_luu_tru_for_turn(trace: AnswerTrace, bang_luu_tru: dict, bang: "lt2.BangV2 | None" = None,
                           chong_lap: bool = False, toi_uu: bool = False, query: str = ""):
    """Hàm `goi_y_luu_tru` của **một lượt** (Đợt 6, cờ `goi_y_luu_tru`): gợi ý tối đa 5 cơ sở từ bảng 136 cơ sở kèm OTA deep links và nhãn cứng."""
    Khu = Literal[gylt.KHU_LUA_CHON]
    Hang = Literal[gylt.HANG_LUA_CHON]
    DiemGan = Literal[(tuple(bang.theo_id) + ("khong",)) if bang is not None else ("khong",)]
    da_goi: dict[tuple, int | None] = {}

    async def goi_y_luu_tru(
        khu: Khu = "bat_ky",
        gan_diem: DiemGan = "khong",
        hang_sao: Hang = "tat_ca",
        ngay_nhan: str = "",
        ngay_tra: str = "",
        so_khach: int = 2,
    ) -> str:
        """Gợi ý cơ sở lưu trú Huế theo khu vực, hạng sao hoặc gần điểm tham quan, kèm link tìm phòng OTA.

        Args:
            khu: khu vực (`trung_tam` hai bờ sông Hương/Kinh thành, `phia_tay` Kim Long/Thủy Xuân, `ven_bien_bac` Thuận An/Phá Tam Giang/Đầm Chuồn, `ven_bien_nam` Lăng Cô/Chân Mây/Đầm Lập An, `bat_ky`).
            gan_diem: mã điểm tham quan cần ở gần (hoặc `khong`).
            hang_sao: phân hạng (`cao` = 4–5★, `vua` = 2–3★, `binh_dan` = 1★/nhà nghỉ/Đạt chuẩn, `tat_ca`).
            ngay_nhan: ngày nhận phòng (YYYY-MM-DD hoặc DD/MM/YYYY, nếu có).
            ngay_tra: ngày trả phòng (YYYY-MM-DD hoặc DD/MM/YYYY, nếu có).
            so_khach: số khách lưu trú (mặc định 2).
        """
        if _la_luot_nguy_hiem_bao_lu(query, trace):
            trace.tools.append({"name": "goi_y_luu_tru", "ms": 0.0, "chan_bao_lu": True})
            return (
                "Trạng thái: lượt này đang hỏi về bão/lũ hoặc ngập lụt — không dùng gợi ý lưu trú lúc này; "
                "hãy trả lời theo cảnh báo an toàn chính thức và số 112."
            )
        lan = sum(t["name"] == "goi_y_luu_tru" for t in trace.tools)
        entry = {"name": "goi_y_luu_tru", "ms": 0.0, "khu": khu, "gan_diem": gan_diem, "hang_sao": hang_sao}
        trace.tools.append(entry)
        khoa = (
            str(khu).strip().casefold(),
            str(gan_diem).strip().casefold(),
            str(hang_sao).strip().casefold(),
            (ngay_nhan or "").strip(),
            (ngay_tra or "").strip(),
            int(so_khach),
        )
        if chong_lap and khoa in da_goi:
            entry["lap"] = True
            return _phan_hoi_lap(da_goi[khoa], "gợi ý lưu trú")
        if lan >= 3:
            entry["het_luot"] = True
            return "Trạng thái: đã tra gợi ý lưu trú ở các lần gọi trước trong lượt này; hãy viết câu trả lời từ Bằng chứng đã có."
        started = time.perf_counter()
        text_out, du_lieu = gylt.ket_qua_co_kieu(
            bang_luu_tru,
            bang,
            khu=khu,
            gan_diem=gan_diem,
            hang_sao=hang_sao,
            ngay_nhan=ngay_nhan,
            ngay_tra=ngay_tra,
            so_khach=so_khach,
        )
        n = len(du_lieu["co_so"])
        entry["ms"] = elapsed_ms(started)
        entry["n_ket_qua"] = n
        trace.goi_y_luu_tru = (trace.goi_y_luu_tru or []) + [{"khu": khu, "gan_diem": gan_diem, "hang_sao": hang_sao, "n": n, "du_lieu": du_lieu}]
        src = PackedSource(
            id=len(trace.so_nguon) + 1,
            title=gylt.TIEU_DE_NGUON,
            heading_path=(gylt.MUC_NGUON,),
            excerpts=tuple(line for line in text_out.splitlines() if line.strip()),
            source=gylt.NGUON_SOURCE,
        )
        trace.so_nguon.append(src)
        da_goi[khoa] = src.id
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    goi_y_luu_tru.__doc__ = gylt.mo_ta_cong_cu(bang, toi_uu=toi_uu)
    goi_y_luu_tru.mo_ta_ngan = gylt.mo_ta_ngan
    return goi_y_luu_tru


def _nguon_khoang_cach_san(trace: AnswerTrace, bang: "kc.BangKhoangCach", cap: tuple[str, str]) -> str:
    """Khoảng cách tính sẵn: cặp điểm do CODE đọc từ câu đang gõ (`kc.cap_tinh_san`) ⇒ tra bảng, đăng thành một nguồn y như kết quả công cụ
    `khoang_cach` (`trace.khoang_cach` có dòng ⇒ bước kiểm số sau khi sinh chạy như cũ). Log chỉ ghi mã điểm, không chữ người dùng."""
    dong = kc.ket_qua(bang, *cap)
    trace.khoang_cach = [{"diem_a": cap[0], "diem_b": cap[1], "dong": dong}]
    src = PackedSource(id=len(trace.so_nguon) + 1, title=kc.TIEU_DE_NGUON, heading_path=(kc.MUC_NGUON,), excerpts=dong, source=kc.NGUON_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.tools.append({"name": "khoang_cach_san", "ms": 0.0, "diem_a": cap[0], "diem_b": cap[1]})
    return chu


def _nguon_su_kien(trace: AnswerTrace, dong: list[str]) -> str:
    """Cờ `su_kien_theo_ngay`: các dòng code tra từ bảng lễ hội / hoạt động theo ngày, đăng thành **một nguồn** (mẫu `_nguon_lich_san`). Log chỉ số dòng."""
    src = PackedSource(id=len(trace.so_nguon) + 1, title=sk.TIEU_DE_NGUON, heading_path=(sk.MUC_NGUON,), excerpts=tuple(dong), source=sk.NGUON_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.tools.append({"name": "su_kien_san", "ms": 0.0, "n_dong": len(dong)})
    return chu


def _nguon_lich_san(trace: AnswerTrace, query: str) -> str:
    """T1 nhanh (plan `2026-11-10-phase-9-t1-nhanh-plan.md` D2): S5 09/11 câu ngày gọi model 2–4 lần vì model phải gọi `ngay_lich` rồi mới viết ⇒
    code tính sẵn hôm nay / mai / tuần / ngày âm nêu trong câu và trong đoạn kho lần tìm đầu, đăng thành **một nguồn** (như kết quả `ngay_lich`), nối
    sau ngữ cảnh. Log chỉ số đếm (số dòng, số ngày âm), không chữ."""
    started = time.perf_counter()
    cau = " ".join([query] + ([trace.history[-1][0]] if trace.history else []))  # như `ngay_lich_for_turn`: câu cuối + câu hỏi liền trước
    dong, n_am = nl.lich_san(cau, trace.packed.text)
    src = PackedSource(id=len(trace.so_nguon) + 1, title=nl.TIEU_DE_NGUON, heading_path=(nl.MUC_NGUON,), excerpts=tuple(dong), source=nl.NGUON_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.tools.append({"name": "lich_san", "ms": elapsed_ms(started), "n_dong": len(dong), "n_am": n_am})
    return chu


def chu_cua_model(trace: AnswerTrace) -> str:
    """Câu trả lời bỏ phần code nối sau chữ model (khối / câu thời tiết B5b) — cờ `refusal` của log tính trên phần này (review C m-1)."""
    answer, noi, dau = trace.answer or "", trace.thoi_tiet_noi, trace.thoi_tiet_dau
    answer = answer[: -len(noi) - 2] if noi and answer.endswith(f"\n\n{noi}") else answer
    return answer[len(dau) + 2:] if dau and answer.startswith(f"{dau}\n\n") else answer


def _khop_luoi_cuoi(query: str, flags: "AssistantFlags | None", history=()) -> bool:
    """Chính câu người dùng HOẶC câu hỏi liền trước khớp lưới bão / lũ (như `tt.la_luot_bao_lu` của đường thường — câu hỏi tiếp "thế có nên đi không"
    sau một câu bão vẫn là lượt bão; thừa hơn sót)."""
    if flags is None or not (flags.thoi_tiet and flags.bao_lu_cong_cu):
        return False
    return _luot_bao_lu(query, history)


def _luot_bao_lu(query: str, history=()) -> bool:
    """Câu này HOẶC câu hỏi liền trước là câu bão / lũ: danh sách rộng của `tt`, "cảnh báo" + một từ thời tiết, hoặc "dông". MỘT chỗ xét cho lưới cuối
    (`_khop_luoi_cuoi`) và cho mục web (`cong_web`) — hai nơi lệch nhau thì mục web để model viết ngay cạnh câu 112 (soát khác hãng 18/11, hai lần)."""
    return tt.la_luot_bao_lu(query, history)  # 21/11: "dông" nay nằm trong danh sách của `tt` (kèm loại trừ "dông dài", "Dông Ba") — không còn mẫu riêng ở đây


def luoi_cuoi_bao(query: str, trace: AnswerTrace, flags: "AssistantFlags | None") -> bool:
    """Lưới cuối (18/11, gọi ở route ngay trước khi gửi kết quả): câu người dùng gõ (hoặc câu hỏi liền trước) khớp lưới bão / lũ mà câu trả lời, mục web và dòng ghi chú
    đều chưa có câu bản tin chính thức + 112 ⇒ đặt câu đó vào dòng ghi chú (`notice`). Vì sao ở đây: câu 112 chỉ được nối trong `_thoi_tiet_cuoi`;
    lượt kết thúc sớm / đi đường khác (xếp ngoài phạm vi, trò chuyện, ngữ cảnh rỗng, sửa lịch) không tới đó. Dùng `notice` chứ không nối vào chữ:
    lượt có lịch giao diện không vẽ chữ trả lời, và chữ không đổi thì cờ từ chối / bộ đếm / lịch sử giữ nguyên. Trả True khi đã thêm."""
    # 22/11 (soát khác hãng): cả lượt mà MODEL đã tự gọi công cụ loại bão / lũ (câu gõ không khớp lưới) — như `loi_bao_luoi_cuoi` đã nhìn
    if not (_khop_luoi_cuoi(query, flags, trace.history) or (trace.thoi_tiet_ctx or {}).get("bao_lu_model")) or trace.clarify is not None:
        return False
    da_co = (trace.answer or "") + ((trace.web or {}).get("text") or "") + (trace.notice or "")
    if tt.CAU_BAO_LU in da_co or tw.THIEN_TAI_TEXT in da_co:
        return False
    trace.notice = f"{tt.CAU_BAO_LU} {trace.notice}" if trace.notice else tt.CAU_BAO_LU
    return True


def loi_bao_luoi_cuoi(query: str, message: str, flags: "AssistantFlags | None", history=(), thoi_tiet_ctx: dict | None = None) -> str:
    """Cùng lưới cho LỜI BÁO LỖI (model / tìm kho lỗi, câu trả lời bị rút lại): lượt bão / lũ mà không trả lời được vẫn phải chỉ bản tin chính thức + 112.
    Lượt bão / lũ = câu khớp lưới HOẶC model đã tự gọi công cụ thời tiết loại bão / lũ trong lượt này (`thoi_tiet_ctx["bao_lu_model"]`) rồi mới lỗi."""
    luot_bao_lu = _khop_luoi_cuoi(query, flags, history) or bool((thoi_tiet_ctx or {}).get("bao_lu_model"))
    if not luot_bao_lu or tt.CAU_BAO_LU in message:
        return message
    return f"{message}\n\n{tt.CAU_BAO_LU}"


def _giu_dau_bao_lu(trace: AnswerTrace, bo: AnswerTrace) -> None:
    """Soát khác hãng 22/11 (A6): `bo` là trace của đường trả lời thường vừa bị HUỶ (tin hoá ra là lệnh sửa lịch). Model ở đường đó đã tự gọi công cụ
    thời tiết loại bão / lũ ⇒ dấu `bao_lu_model` sang trace của lượt sửa, để lưới cuối (`luoi_cuoi_bao`) vẫn gắn câu bản tin chính thức + 112 dù câu
    gõ không trúng lưới chữ. Chỉ chép đúng dấu đó; đường thường chưa kịp gọi công cụ thì không có gì để chép (giới hạn: runbook 10.2)."""
    if (bo.thoi_tiet_ctx or {}).get("bao_lu_model"):
        trace.thoi_tiet_ctx = {**(trace.thoi_tiet_ctx or {}), "bao_lu_model": True}


def _can_dau_bao_lu(trace: AnswerTrace) -> bool:
    """Cờ `bao_lu_cong_cu`: CHÍNH câu đang hỏi khớp lưới bão / lũ nhưng model không gọi `thoi_tiet` (trả lời từ kho) và lượt không có lịch ⇒ cần
    câu `CAU_DAU_BAO_LU` trước. Câu hỏi tiếp chỉ khớp nhờ câu liền trước ⇒ không (review E M-1: câu hỏi tiếp không liên quan bị đặt câu đầu)."""
    ctx = trace.thoi_tiet_ctx or {}
    return bool(ctx.get("bao_lu_cong_cu") and ctx.get("bao_lu_cau")) and trace.thoi_tiet is None and trace.lich is None


def _la_luot_nguy_hiem_bao_lu(query: str, trace: AnswerTrace) -> bool:
    """Phép xét nguy hiểm bão/lũ dùng chung cho chặn tool lưu trú/mưa nắng và hậu kiểm lượt."""
    ctx = trace.thoi_tiet_ctx or {}
    return bool(
        (query and tt.la_luot_bao_lu(query, trace.history))
        or trace.bao_lu_lan_dau
        or ctx.get("bao_lu")
        or ctx.get("bao_lu_model")
    )


def _thoi_tiet_cuoi(trace: AnswerTrace) -> None:
    """B5b, sau lần sinh và sau phép kiểm số (`_so_la` — D8), cờ bật, mọi câu tuyến `tro_ly_hue`: code nối khối số liệu (hoặc câu lỗi) · câu bão / lũ
    (D6) · câu "chỉ có dự báo 7 ngày" (D3)."""
    ctx = trace.thoi_tiet_ctx or {}
    tool = trace.thoi_tiet
    if tool is not None and tool["khoi"] and (trace.answer or "").strip() == INSUFFICIENT_ANSWER:
        trace.answer = tt.CAU_DAN_BAO_LU if tool.get("bao_lu") else tt.CAU_DAN_DU_BAO  # review C M-1: có dự báo mà model từ chối ⇒ không để câu từ chối đứng trước số liệu
        tool["thay_tu_choi"] = True
    if _can_dau_bao_lu(trace) and (trace.answer or "").strip() != INSUFFICIENT_ANSWER:
        trace.thoi_tiet_dau = tt.CAU_DAU_BAO_LU
        trace.answer = f"{tt.CAU_DAU_BAO_LU}\n\n{trace.answer}"
    noi = []
    if tool is not None:
        noi.append(tool["khoi"] or tt.CAU_LOI)
    if ctx.get("bao_lu") or ctx.get("bao_lu_model") or trace.bao_lu_lan_dau:
        noi.append(tt.CAU_BAO_LU)
    if ctx.get("ngoai_7") and ctx.get("tu_khoa"):
        noi.append(tt.CAU_NGOAI_7_NGAY)
    trace.thoi_tiet_noi = "\n\n".join(noi) or None
    if trace.thoi_tiet_noi:
        trace.answer = f"{trace.answer}\n\n{trace.thoi_tiet_noi}"


def _do_dai_bang_chung(doc: RetrievedDocument) -> int:
    """Số ký tự bằng chứng của một đoạn — đúng phần đi vào ngữ cảnh (`evidence_parts`, như `FullCorpusContextBuilder._source`)."""
    return sum(len(part["text"].strip()) for part in doc.metadata.get("evidence_parts") or []
               if isinstance(part, dict) and isinstance(part.get("text"), str))


async def _lay_nguon_lich(bang, khung: dict, query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None,
                          instructions: str, nhap: str | None = None, lay_ve: bool = True, max_doan: int | None = None,
                          tim_mo_ta: str | None = None, doan_chon: dict | None = None):
    """D6: mỗi điểm trong khung — `retrieval_service.search(<tên điểm>)` (đọc Qdrant, không ghi), chọn **đúng 1 đoạn** = đoạn có bằng chứng dài
    nhất trong top-10 có `source` = file nguồn của điểm (cổng đợt 1 S1, A chốt: "đoạn đầu" hay chỉ là dòng tên — 11/28 điểm < 80 ký tự — nên
    luật "kèm một ý ngắn lấy từ tài liệu" không viết được ⇒ model từ chối; bằng nhau ⇒ đoạn đứng trước); đoạn đã có trong sổ nguồn ⇒ dùng lại số [n] cũ; không có đoạn đúng file ⇒ bỏ điểm (mã `khong_co_doan_nguon`).
    Có điểm Quần thể ⇒ thêm 1 đoạn file vé chứa khung giờ (D5 (a)). Đoạn mới dựng ngữ cảnh nối sổ nguồn; vượt ngân sách ⇒ bớt ngày cuối (iii).
    Lỗi tìm / ngữ cảnh ⇒ `trace.tool_error` rồi ném (như `tim_kho`). Lịch bản 2: `nhap` = bản nháp tin nhắn của nó (đếm ngân sách), `lay_ve=False`
    (giờ gợi ý do code in — không cần đoạn file vé); mặc định ⇒ đúng như đường cũ. `tim_mo_ta` (lịch bản 2, vòng chỉnh nghiệm thu 13/11): tìm bằng
    "<tên> <tim_mo_ta>", lấy đoạn xếp hạng cao nhất cùng file NẾU đoạn đó nhắc tên điểm (đoạn tả điểm — luật cũ hay chọn đoạn "bằng chứng" như lăng
    lân cận / quy tắc ứng xử ⇒ model trả câu rỗng); không có ⇒ luật cũ."""
    try:
        da_co = {doc_id: i + 1 for i, doc_id in enumerate(trace.seen_ids)}  # sổ nguồn đánh số liền từ 1, song song `seen_ids`
        cho: dict[str, list[str]] = {}  # chunk_id mới ⇒ điểm dùng đoạn đó
        moi: list[RetrievedDocument] = []
        nguon: dict[str, int] = {}

        async def chon_doan(cau: str, source: str, chua: str | None = None) -> RetrievedDocument | None:
            result = await asyncio.to_thread(retrieval_service.search, cau)
            cung_file = [d for d in result.documents[:10] if d.metadata.get("source") == source and (chua is None or chua in d.text)]
            return max(cung_file, key=_do_dai_bang_chung, default=None)

        async def doan_mo_ta(d: dict) -> RetrievedDocument | None:
            result = await asyncio.to_thread(retrieval_service.search, f"{d['ten']} {tim_mo_ta}")
            ten = [lt.chuan_ten(t) for t in (d["ten"], *d["ten_khac"])]
            return next((x for x in result.documents[:10] if x.metadata.get("source") == d["nguon"]
                         and any(t in lt.chuan_ten(x.text) for t in ten)), None)

        for id_ in dict.fromkeys(lt.diem_trong_khung(khung)):  # hoạt động tối lặp lại ⇒ tìm một lần
            d = bang.theo_id[id_]
            # bản 2: đoạn mô tả chọn sẵn trong bảng (cột `doan_mo_ta`) đứng trước; không có ⇒ đoạn tả điểm tìm được ⇒ luật cũ
            doc = (doan_chon or {}).get(id_) or (await doan_mo_ta(d) if tim_mo_ta else None) or await chon_doan(d["ten"], d["nguon"])
            if doc is None:
                lt.bo_diem(khung, id_, d["ten"], "khong_co_doan_nguon")
            elif doc.id in da_co:
                nguon[id_] = da_co[doc.id]
            else:
                if doc.id not in cho:
                    moi.append(doc)
                cho.setdefault(doc.id, []).append(id_)
        ve = None
        if lay_ve and any(bang.theo_id[i]["quan_the"] for i in lt.diem_trong_khung(khung)):
            ve = await chon_doan(lt.VE_CAU_TIM, lt.VE_NGUON, chua="17h30")
            if ve is not None and ve.id not in da_co and ve.id not in cho:
                moi.append(ve)
        # chữ khung cũng vào model ⇒ đếm vào ngân sách bằng bản nháp (số nguồn tạm) — D6 (iii)
        if nhap is None:
            nhap = lt.khung_chu(bang, khung, dict.fromkeys(lt.diem_trong_khung(khung), 0), LICH_TRINH_LUAT, 0)
        packed = await asyncio.to_thread(
            context_builder.build, query, moi, today=today, first_id=len(trace.so_nguon) + 1,
            prior_context="\n\n".join([*trace.context_parts, nhap]),
            skip_ids=frozenset(trace.seen_ids), instructions=instructions, history=trace.history,
            n_tool_items=2 * (trace.model_searches + 1), extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD,
            max_documents=max_doan,
        )
    except RetrievalDependencyError as exc:
        trace.tool_error = exc
        raise
    so = dict(zip(packed.document_ids, (src.id for src in packed.sources)))
    for doc_id, ids in cho.items():
        for id_ in ids:
            if doc_id in so:
                nguon[id_] = so[doc_id]
    while khung["ngay"] and any(i not in nguon for i in lt.diem_trong_khung(khung)):  # điểm có đoạn không vào được ngữ cảnh (vượt trần SỐ ĐOẠN của lượt, hoặc đoạn rỗng) ⇒ bớt từ ngày cuối
        lt.cat_ngay_cuoi(khung)
    nguon = {i: nguon[i] for i in lt.diem_trong_khung(khung)}
    nguon_ve = None if ve is None else (da_co.get(ve.id) or so.get(ve.id))
    trace.so_nguon.extend(packed.sources)
    trace.context_parts.append(packed.text)
    trace.seen_ids.extend(packed.document_ids)
    return packed, nguon, nguon_ve


def record_llm_calls(trace: AnswerTrace, calls, call_route: str | None = None) -> None:
    """Nối các lần gọi model đã xong vào `trace.llm_calls`, mỗi mục gắn tuyến của **lần gọi** (`router` / `tro_chuyen` / `tro_ly_hue`)."""
    trace.llm_calls.extend({"route": call_route or trace.route, **call} for call in calls)


def turn_usd(trace: AnswerTrace) -> float | None:
    """USD của cả lượt = cộng từng lần gọi. Không gọi model (câu cố định, từ chối trước model, lỗi trước bước sinh) ⇒ 0; đã gọi mà không có
    mục nào (ngắt / lỗi giữa chừng — không có usage) ⇒ None, không đoán."""
    serper = (trace.web or {}).get("usd_serper", 0.0)  # B6: lượt tra web (lần gọi model mục web đã nằm trong `llm_calls`)
    if trace.llm_calls:
        return sum(call["usd"] for call in trace.llm_calls) + serper
    return serper if trace.generation_ms is None and trace.routing_ms is None else None


async def prepare_answer(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                         today: str | None = None, instructions: str | None = None, ve_them: Sequence[str] = ()) -> None:
    """Phần trước model của tuyến `tro_ly_hue`: lần tìm đầu của code → ngữ cảnh. `ve_them`: xem `search_into_trace` (cờ `tim_theo_ve`). Câu tìm = câu gốc (V0) hoặc câu định tuyến viết
    (`trace.cau_tim`, B2 V1 / V3); ngân sách luôn đếm bằng câu gốc (B2 D3). `instructions`: lời dặn trợ lý khi lượt đi vòng công cụ (B2b).
    Ngữ cảnh không có nguồn ⇒ `trace.answer` = câu từ chối chuẩn (không gọi model). Còn lại cần model: `generator=None` nghĩa là
    chưa sẵn sàng ⇒ `GeneratorNotReadyError`. `recorder` chỉ route truyền (spec §4.8 khác biệt 4).

    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `GeneratorNotReadyError`."""
    await search_into_trace(trace.cau_tim or [trace.search_query or query], cau_hoi=query, retrieval_service=retrieval_service, context_builder=context_builder,
                            trace=trace, today=today, instructions=instructions, ve_them=ve_them)
    if recorder:
        recorder.record_packed_context(trace.packed)

    if not trace.packed.sources:
        if recorder:
            recorder.record_fallback()
        trace.answer = INSUFFICIENT_ANSWER  # từ chối trước khi gọi model
        trace.fixed_outcome = "refusal_no_sources"
        return

    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")


def check_citations(trace: AnswerTrace) -> None:
    """Kiểm citation của `trace.answer` (chữ gốc model) với sổ nguồn. Kiểm trên chữ gốc: regex citation nhận cả `[n]` lẫn
    `[Nguồn n]` nên kết quả giống hệt kiểm sau chuẩn hóa. Hỏng ⇒ ghi `trace.citation_error`, không ném."""
    started = time.perf_counter()
    try:
        trace.cited = select_cited_sources(trace.answer, trace.so_nguon)
        trace.citation_ms = elapsed_ms(started)
    except CitationIntegrityError as exc:
        trace.citation_error = exc


TEN_VIET_LAI = "viet_lai_het_luot"  # tên mục `trace.tools` của lần viết lại (sổ số đo: chỉ tên + thời gian + kết cục, không chữ)
TEN_CUU_MAX_TURNS = "cuu_max_turns"  # tên mục `trace.tools` của lần viết lại cứu chạm trần vòng (Đợt 1A)
_LOI_KHONG_MA_NGUON = "Grounded answer has no citation"  # đầu lời lỗi của `llm/citations.py`


def _dat_tu_choi_max_turns(trace: AnswerTrace, flags: AssistantFlags | None) -> None:
    """Đặt câu từ chối cố định `max_turns` kèm câu bản tin bão/lũ nếu thuộc lượt bão/lũ."""
    _set_fixed(trace, INSUFFICIENT_ANSWER, "max_turns")
    trace.thoi_tiet_noi = None
    trace.thoi_tiet_dau = None
    ctx = trace.thoi_tiet_ctx or {}
    if flags is not None and flags.thoi_tiet and (ctx.get("bao_lu") or ctx.get("bao_lu_model") or trace.bao_lu_lan_dau):
        # review tích hợp 18/11 #1: lượt bão / lũ chạm trần lượt trả về TRƯỚC `_thoi_tiet_cuoi`, cổng web cũng đóng ⇒ câu 112 phải đi cùng
        trace.thoi_tiet_noi = tt.CAU_BAO_LU
        trace.answer = f"{trace.answer}\n\n{tt.CAU_BAO_LU}"


def _chan_doan_viet_lai(citation_error: CitationIntegrityError | None, n_nguon: int) -> str | None:
    """Actionable Feedback 1 dòng khi bản nháp trước trượt kiểm citation (Đợt 4A, cờ `toi_uu_dot2_va_viet_lai`)."""
    if citation_error is None:
        return None
    if str(citation_error).startswith(_LOI_KHONG_MA_NGUON):
        return (
            f"Lưu ý sửa lỗi (bản nháp trước trượt kiểm: chưa gắn mã nguồn [n]): mọi nhận định lấy từ Bằng chứng trên "
            f"PHẢI gắn đúng mã [1]..[{n_nguon}] ngay sau câu; nếu Bằng chứng không đủ thì trả đúng câu không đủ thông tin "
            "(không viết thêm câu giải thích không nguồn)."
        )
    return (
        f"Lưu ý sửa lỗi (bản nháp trước trượt kiểm: {citation_error}): chỉ dùng mã [1]..[{n_nguon}] có trong Bằng chứng trên; "
        "nếu trả câu không đủ thông tin thì không gắn mã nguồn nào."
    )


async def _goi_viet_lai(query: str, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None,
                        call_log: "CallLog | None", *, chan_doan: str | None = None) -> None:
    """Chạy MỘT lần viết lại không công cụ trên mọi Bằng chứng đã gom của lượt, rồi qua `_finish_generated`."""
    rieng = CallLog() if call_log is None else None
    context = "\n\n".join(trace.context_parts) + (f"\n\n{VIET_LAI_NHIEU_Y_TEXT}" if trace.nhieu_y else "")
    if chan_doan:
        context = f"{context}\n\n{chan_doan}"
    kwargs = {"call_log": rieng or call_log} if today is None else {"call_log": rieng or call_log, "today": today}
    if flags.kiem_du_bang_chung:
        kwargs["kiem_du_bang_chung"] = True
    trace.fixed_outcome = None
    trace.answer = None
    trace.thoi_tiet_noi = None
    trace.thoi_tiet_dau = None
    trace.citation_error, trace.cited = None, ()
    try:
        trace.generated = await generator.generate_answer(query, context, **kwargs, **_history_kwargs(trace))
    finally:
        if rieng is not None:
            record_llm_calls(trace, rieng.calls, ROUTE_TRO_LY_HUE)
    _finish_generated(trace, flags, query)


async def _viet_lai_het_luot(query: str, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None, call_log: "CallLog | None") -> bool:
    """Công tắc `het_luot_viet_lai`, gọi ngay sau `_finish_generated` của lượt có công cụ. Chỉ khi: lỗi kiểm là "không có mã nguồn nào" VÀ model đã tự
    tìm kho ÍT NHẤT MỘT lần VÀ lượt không phải câu cố định / lượt có lịch. (Bản đầu đòi "đã dùng HẾT lượt tìm"; lượt thật 22/11 với trần 3 lần: model
    tìm 2 lần rồi tự dừng, viết hai dòng "chưa có" kèm một đoạn giải thích không nguồn ⇒ lọt lưới ⇒ màn hình lỗi. Lượt model KHÔNG tìm lần nào — kiểu
    chép lại câu trả lời nhớ — vẫn không thuộc lưới này: đã có bản chạy lại của `answer_turn_stream_parallel`.) Viết MỘT lần bằng đường không công cụ (`generate_answer`) trên mọi khối Bằng chứng
    lượt đã gom (`trace.context_parts` — số nguồn giữ nguyên), kiểm lại như thường; vẫn không có mã ⇒ câu từ chối cố định. Trả True khi đã viết lại
    (đường stream phải thay chữ đã hiện). `call_log` None ⇒ tự ghi tiền của lần gọi thêm (đường không stream đã ghi sổ trước đó)."""
    if not (flags.het_luot_viet_lai and trace.citation_error is not None and str(trace.citation_error).startswith(_LOI_KHONG_MA_NGUON)
            and trace.model_searches >= 1 and trace.fixed_outcome is None and trace.lich is None):
        return False
    started = time.perf_counter()
    chan_doan = _chan_doan_viet_lai(trace.citation_error, len(trace.so_nguon)) if flags.toi_uu_dot2_va_viet_lai else None
    await _goi_viet_lai(query, generator, trace, flags, today, call_log, **({"chan_doan": chan_doan} if chan_doan else {}))
    con_loi = trace.citation_error is not None and str(trace.citation_error).startswith(_LOI_KHONG_MA_NGUON)
    if con_loi:  # lần viết lại cũng không trích nguồn nào ⇒ không có gì đứng được ⇒ câu từ chối cố định (khối dự báo / câu 112 vẫn do `_thoi_tiet_cuoi` nối)
        trace.citation_error, trace.answer, trace.cited = None, INSUFFICIENT_ANSWER, ()
        if flags.thoi_tiet:
            _thoi_tiet_cuoi(trace)
    trace.tools.append({"name": TEN_VIET_LAI, "ms": elapsed_ms(started), "tu_choi": con_loi})
    return True


async def _cuu_max_turns(query: str, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None,
                          call_log: "CallLog | None") -> bool:
    """Đợt 1A (`cuu_max_turns`): khi `hit_max_turns=True` mà `trace.documents` đã có bằng chứng nguồn, gọi viết lại MỘT lần tắt toàn bộ tool
    (`generate_answer` qua `_goi_viet_lai` + `check_citations` + kiểm an toàn). Vẫn rỗng / lỗi kiểm / lỗi gọi model ⇒ giữ sàn 0 bịa nguồn bằng cách
    trả về câu từ chối cố định `max_turns` như cũ. Trả True chỉ khi cứu thành công (đường stream phát `delta` mới)."""
    if not (flags.cuu_max_turns and trace.fixed_outcome == "max_turns" and trace.lich is None
            and trace.documents and trace.so_nguon and any(p.strip() for p in trace.context_parts)):
        return False
    started = time.perf_counter()
    thanh_cong = False
    try:
        await _goi_viet_lai(query, generator, trace, flags, today, call_log)
        if trace.citation_error is None and (trace.answer or "").strip():
            thanh_cong = True
        else:
            trace.citation_error = None
            _dat_tu_choi_max_turns(trace, flags)
    except GenerationError:
        trace.citation_error = None
        _dat_tu_choi_max_turns(trace, flags)
    trace.cuu_max_turns = {"thanh_cong": thanh_cong}
    trace.tools.append({"name": TEN_CUU_MAX_TURNS, "ms": elapsed_ms(started), "thanh_cong": thanh_cong})
    return thanh_cong


TEN_VIET_LAI_CAU = "cit_cau_viet_lai"


async def _viet_lai_trich_dan_cau(query: str, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None,
                                   call_log: "CallLog | None") -> bool:
    """Đợt 7 Nhịp 2B (`H2.1b`, cờ `kiem_trich_dan_cau`): câu trả lời hợp lệ đã có mã trích dẫn (không phải từ chối / bão lũ / làm thay / lịch)
    nhưng còn câu nhận định thiếu `[n]` ⇒ gọi `_goi_viet_lai` tối đa 1 lần với phản hồi định hướng; lỗi hoặc biến thành từ chối thì giữ nguyên bản gốc."""
    ans = (trace.answer or "").strip()
    if (
        not (flags.kiem_trich_dan_cau and flags.uses_tools)
        or trace.fixed_outcome is not None
        or trace.citation_error is not None
        or trace.lich is not None
        or trace.lich_v2 is not None
        or not ans
        or ans in REFUSAL_ANSWERS
        or not trace.cited
        or not trace.so_nguon
        or not any(p.strip() for p in trace.context_parts)
        or _la_luot_nguy_hiem_bao_lu(query, trace)
        or bool(trace.vet.get("p1_xoa_luu_tru"))
    ):
        return False
    cc = check_sentence_citations(ans)
    if cc["passed"]:
        return False
    snap = (
        trace.answer,
        trace.cited,
        trace.citation_error,
        trace.generated,
        trace.fixed_outcome,
        trace.thoi_tiet_noi,
        trace.thoi_tiet_dau,
        trace.chi_y_thieu,
        trace.thoi_tiet_kiem,
        trace.khoang_cach_kiem,
        trace.kiem_so_go,
        trace.lich_kiem,
        trace.clarify,
    )
    started = time.perf_counter()
    n_src = len(trace.so_nguon)
    chan_doan = (
        f"Lưu ý sửa lỗi (bản nháp trước còn {cc['missing_count']} câu nhận định chưa gắn mã nguồn [n]): "
        f"mọi câu nêu nhận định lấy từ Bằng chứng trên PHẢI kết bằng đúng mã [1]..[{n_src}] ngay cuối câu đó "
        "(không gom mã ở cuối đoạn); không thêm giải thích hay lời khuyên ngoài Bằng chứng; "
        "ý nào Bằng chứng không nêu thì bỏ hoặc xuất đúng câu từ chối."
    )
    restored = False
    try:
        await _goi_viet_lai(query, generator, trace, flags, today, call_log, chan_doan=chan_doan)
    except GenerationError:
        restored = True
    new_ans = (trace.answer or "").strip()
    tu_choi = new_ans in REFUSAL_ANSWERS
    cc2 = check_sentence_citations(new_ans) if (not restored and new_ans) else cc
    if (
        restored
        or trace.citation_error is not None
        or trace.fixed_outcome is not None
        or not new_ans
        or tu_choi
        or not trace.cited
        or cc2["missing_count"] > cc["missing_count"]
    ):
        (
            trace.answer,
            trace.cited,
            trace.citation_error,
            trace.generated,
            trace.fixed_outcome,
            trace.thoi_tiet_noi,
            trace.thoi_tiet_dau,
            trace.chi_y_thieu,
            trace.thoi_tiet_kiem,
            trace.khoang_cach_kiem,
            trace.kiem_so_go,
            trace.lich_kiem,
            trace.clarify,
        ) = snap
        restored = True
        cc2 = cc
    else:
        trace.vet["cit_cau_viet_lai"] = True
    trace.tools.append({
        "name": TEN_VIET_LAI_CAU,
        "ms": elapsed_ms(started),
        "restored": restored,
        "tu_choi": tu_choi,
        "before_missing": cc["missing_count"],
        "after_missing": cc2["missing_count"],
        "after_passed": cc2["passed"],
    })
    return not restored


def _doan_bai(bai) -> tuple[str, ...]:
    """Các đoạn chữ của một bài mục lục đưa cho `dong_tam_ngung`: từng dòng rời TRƯỚC (như cũ), rồi cả bài nối dòng làm lưới sau. Soát khác hãng
    22/11/2026: câu an toàn nằm trên HAI dòng vật lý của file ("…thuyền có thể phải dừng chạy khi nước sông dâng cao hoặc có lệnh cấm xuất bến") thì không
    dòng rời nào tự đủ ý ⇒ bài đi qua công cụ liệt kê / gần một điểm / thẻ nơi mất dòng lưu ý mà đường tìm kho vẫn có. Chỉ dùng bản nối dòng một mình là
    sai: nó làm đổi câu của các bài đang ra đúng (phiên đo chạy 267 bài: cách này bằng đúng bài gốc 267 / 267)."""
    return tuple(bai.dong) + ("\n".join(bai.dong),)


def set_notice(trace: AnswerTrace, flags: AssistantFlags) -> None:
    """H4c (D8): câu trả lời kho có nguồn được trích thuộc vé / điểm đến / lễ hội ⇒ dòng cố định. Chữ câu trả lời không đổi.
    Khoảng cách (16/11): câu trả lời TRÍCH nguồn khoảng cách mà chữ model không nhắc "kẹt xe" ⇒ code nối câu ghi chú của nguồn vào dòng cố định —
    ghi chú là phần bắt buộc đi cùng số ước, model bỏ nó ở ~35 % câu (đếm 4 lượt đo: 33 / 52 câu có), cả đường công cụ lẫn đường tính sẵn."""
    dong = []
    # cờ `liet_ke_bai`: câu trả lời trích nguồn "mục lục" ⇒ bài nào của mục lục đó CÓ TÊN trong câu trả lời được coi như bài đã trích khi xét hai dòng ghi chú
    # dưới (rỗng khi cờ tắt / không trích mục lục ⇒ `notice` y như trước)
    tra_loi = (trace.answer or "").casefold()
    bai_neu = [bai for src in (trace.cited or ()) if src.source in (lk.NGUON_SOURCE, gd.NGUON_SOURCE, mn.NGUON_SOURCE, ss.NGUON_SOURCE) or src.heading_path == (thn.MUC_THE,)  # bài của từng nơi công cụ nêu / thẻ nơi
               for bai in trace.muc_luc_bai.get(src.id, ()) if bai.tieu_de.casefold() in tra_loi]
    # câu an toàn của nguồn đã trích đứng TRƯỚC các ghi chú thường; cờ tắt ⇒ `notice` y như trước. Lượt có lịch (biểu mẫu, sửa lịch, công cụ lịch) KHÔNG
    # nhận: chưa có dữ liệu đo, và "một dòng mỗi câu trả lời" là tuỳ tiện với lịch nhiều điểm (review E 19/11)
    if flags.noi_dong_tam_ngung and trace.cited and not trace.bieu_mau and trace.lich is None and trace.lich_v2 is None:
        trace.luu_y_nguon = dong_tam_ngung(trace.answer or "", [(nhan_nguon(src.title, src.heading_path), src.excerpts) for src in trace.cited]
                                           + [(bai.tieu_de, _doan_bai(bai)) for bai in bai_neu])
        if trace.luu_y_nguon:
            dong.append(trace.luu_y_nguon)
    # Soát khác hãng 22/11 (G7): nguồn "gần một điểm" loại ĐIỂM THAM QUAN cũng in km + phút theo đường đi (dòng cuối của nó là chính câu ghi chú này) ⇒
    # cùng luật; đếm trên lượt thật: 5 / 14 lượt nêu km + phút mà bỏ ý "chưa tính kẹt xe". Loại quán (đường chim bay) không có dòng đó ⇒ không nối.
    if (trace.cited and "kẹt xe" not in (trace.answer or "").casefold()
            and any(src.source == kc.NGUON_SOURCE or (src.source in (gd.NGUON_SOURCE, mn.NGUON_SOURCE, ss.NGUON_SOURCE) and kc.CAU_GHI_CHU in src.excerpts) for src in trace.cited)):
        dong.append(kc.CAU_GHI_CHU)
    # câu xin danh sách: chỉ lượt hỏi đáp thường có nguồn kho — không lượt lịch, không câu có dòng ý thiếu (lượt mở mục web), không câu về MỘT nơi.
    # Lượt sửa lịch / biểu mẫu không qua `_before_model` ⇒ `xin_danh_sach` luôn None ở đó
    if (trace.xin_danh_sach and trace.cited and not trace.bieu_mau and trace.lich is None and trace.lich_v2 is None
            and not co_y_thieu(trace.answer or "") and not hoi_ve_mot_noi(trace.xin_danh_sach, [src.title for src in trace.cited])):
        dong.append(CAU_DANH_SACH)
    if flags.may_have_changed_notice and trace.cited and (any(src.source.startswith(NOTICE_SOURCE_PREFIXES) for src in trace.cited)
                                                           or any(bai.rel.startswith(NOTICE_SOURCE_PREFIXES) for bai in bai_neu)):
        dong.append(MAY_HAVE_CHANGED_NOTICE)
    # câu nhờ lập lịch nhiều ngày ở lượt hỏi đáp thường (kể cả khi kho không trả lời được) ⇒ trỏ sang trang Lên kế hoạch; đứng CUỐI dòng ghi chú
    if trace.nho_len_lich and not trace.bieu_mau and trace.lich is None and trace.lich_v2 is None:
        dong.append(CAU_DAN_TRANG)
    if trace.goi_y_luu_tru and gylt.NHAN not in (trace.answer or "") and gylt.NHAN not in " ".join(dong):
        dong.append(gylt.NHAN)
    if dong:
        trace.notice = " ".join(dong)


def _nguon_lich_dang_co(trace: AnswerTrace, bang: "lt2.BangV2") -> str:
    """Cờ `lich_vao_hoi_thuong`: lịch đã lưu của cuộc + số giờ code tính, đăng thành **một nguồn** (mẫu `_nguon_lich_san`), nối sau ngữ cảnh.
    Log chỉ số đếm (số ngày, số dòng), không chữ."""
    started = time.perf_counter()
    dong = lt2.dong_lich_dang_co(bang, trace.lich_luu)
    src = PackedSource(id=len(trace.so_nguon) + 1, title=lt2.TIEU_DE_NGUON_LICH, heading_path=(lt2.MUC_NGUON_LICH,), excerpts=tuple(dong),
                       source=lt2.NGUON_LICH_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.tools.append({"name": "lich_dang_co", "ms": elapsed_ms(started), "n_ngay": len(trace.lich_luu["khung"]["ngay"]), "n_dong": len(dong)})
    return chu


async def _before_model(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder, today: str | None,
                        flags: AssistantFlags) -> str | None:
    """Phần trước lần gọi model của tuyến `tro_ly_hue`. Trả tin nhắn user cho trợ lý có công cụ (None = đường sinh một lần như B1).
    V2: không tìm trước (chỉ cần generator). Còn lại: `prepare_answer` (có thể đặt câu từ chối khi ngữ cảnh rỗng ⇒ `fixed_outcome`)."""
    trace.nhieu_y = flags.cau_nhieu_y and so_y(query) >= 2
    trace.lam_thay = nho_lam_thay(query) if flags.noi_that_lam_thay else None
    trace.xin_danh_sach = query if flags.danh_sach_noi_that and xin_danh_sach(query) else None
    trace.nho_len_lich = flags.len_lich_dan_trang and flags.lich_trinh_bieu_mau and nho_len_lich(query)
    if flags.lan_tim_dau == "v2":
        if generator is None:
            raise GeneratorNotReadyError("generator is not ready")
        return build_assistant_input(query, None, today)
    trace.lich_offered = flags.lich_trinh and generator is not None  # D16: mọi lượt có công cụ khi cờ bật (cờ cần `tim_them`)
    instructions = _assistant_instructions(generator, trace, trace.nhieu_y, flags.kiem_du_bang_chung) if (flags.tim_them and generator is not None) else None
    # cờ `tim_theo_ve`: chỉ tin nhiều ý, và chỉ khi câu tìm là câu gốc (câu tìm do định tuyến viết đã là câu tách sẵn)
    ve_them = cac_ve_tim(query, flags.tim_ve_bo_cut) if flags.tim_theo_ve and trace.nhieu_y and not trace.cau_tim else ()
    # chỉ truyền thêm khi có vế để tìm ⇒ tin một ý / cờ tắt gọi `prepare_answer` y như trước (bảng test 22/11: một test thay hàm này bằng hàm
    # dựng sẵn 8 tham số đã đỏ khi tham số mới được truyền theo vị trí ở MỌI lượt)
    await prepare_answer(query, retrieval_service, context_builder, generator, trace, recorder, today, instructions, **({"ve_them": ve_them} if ve_them else {}))
    # ngữ cảnh rỗng ⇒ câu từ chối do code đặt; câu nhờ làm thay vẫn nhận câu nói thật. `thoi_tiet_ctx` chưa có ở bước này (đặt sau, trong
    # `_lich_extra`) ⇒ xét thẳng lưới bão / lũ trên câu người dùng (review B m1): lượt bão – lũ giữ câu từ chối cũ + các lớp an toàn của nó
    if trace.fixed_outcome == "refusal_no_sources" and not _khop_luoi_cuoi(query, flags, trace.history):
        _noi_that_lam_thay(trace, trace.answer)
    if not flags.tim_them:
        return None
    context = trace.packed.text
    if flags.ngay_lich and trace.fixed_outcome is None and nl.co_tu_ngay_luot(query, trace.history):
        context = f"{context}\n\n{_nguon_lich_san(trace, query)}"  # T1 nhanh D2: lượt có từ chỉ ngày ⇒ lịch code tính trước lần gọi model đầu
    su_kien = sk.dong_nguon(query, flags.su_kien_bang) if flags.su_kien_theo_ngay and flags.su_kien_bang and trace.fixed_outcome is None else None
    if su_kien:  # cổng hẹp do code đọc câu gõ; câu không qua cổng ⇒ chuỗi gửi model y như cờ tắt
        context = f"{context}\n\n{_nguon_su_kien(trace, su_kien)}"
    cap = kc.cap_tinh_san(query, flags.khoang_cach_bang) if flags.khoang_cach_tinh_san and trace.fixed_outcome is None else None
    if cap:
        context = f"{context}\n\n{_nguon_khoang_cach_san(trace, flags.khoang_cach_bang, cap)}"
    if flags.lich_vao_hoi_thuong and trace.lich_luu is not None and trace.fixed_outcome is None:  # lượt biểu mẫu không qua hàm này
        context = f"{context}\n\n{_nguon_lich_dang_co(trace, flags.bang_lich_v2)}"
    the = the_noi_sau_tim(trace, flags, query) if trace.fixed_outcome is None else ""  # sau các nguồn code dựng ở trên: bộ dò đọc cả chúng
    if the:
        context = f"{context}\n\n{the}"
    return build_assistant_input(query, context, today)


def _noi_that_lam_thay(trace: AnswerTrace, text: str) -> bool:
    """Cờ `noi_that_lam_thay`: câu người dùng là câu nhờ làm thay (`trace.lam_thay`, đặt ở `_before_model` khi cờ bật) VÀ câu trả lời đúng bằng câu
    từ chối khuôn ⇒ câu nói thật của loại đó, kết thúc cố định `lam_thay` (không kiểm citation; `web_gate_open` đóng vì không phải kết thúc thường).
    Câu trả lời khác câu khuôn ⇒ không đụng. Lượt có lịch / có dự báo / khớp lưới bão – lũ ⇒ không thay: các lớp code nối ở đó giữ nguyên."""
    ctx = trace.thoi_tiet_ctx or {}
    if (trace.lam_thay is None or (text or "").strip() != INSUFFICIENT_ANSWER or trace.lich is not None or trace.thoi_tiet is not None
            or ctx.get("bao_lu") or ctx.get("bao_lu_cau") or ctx.get("luoi_cuoi")):  # `luoi_cuoi`: cả "dông" — như lưới cuối và nơi thay thứ nhất
        return False
    _set_fixed(trace, CAU_LAM_THAY[trace.lam_thay], "lam_thay")
    trace.tools.append({"name": "lam_thay", "ms": 0.0, "loai": trace.lam_thay})  # log: mã loại, không chữ
    return True


_DONG_DANH_SACH = re.compile(r"^\s*(?:[-*•–]|\d+[.)]|#{1,6})\s")  # dòng gạch đầu dòng / đánh số / tiêu đề: gỡ là gỡ cả dòng
_RANH_CAU = re.compile(r"(?<=[.!?…])\s+(?!\[)")  # ranh giữa hai câu trong một dòng; không tách trước "[n]" đứng sau dấu chấm (trích dẫn của câu vừa xong)
_VIET_TAT_CUOI = re.compile(r"(?:^|[\s(])(?:[A-ZĐ]{1,3}|Tp|Th)\.$")  # "TP.", "Q.", "TT.", "Tp." — không phải hết câu ("Huế." vẫn là hết câu)
_DONG_DAN = re.compile(r":\s*(?:\[(?:Nguồn\s*)?\d+\]\s*)*$")  # dòng kết thúc bằng ":" (có thể kèm [n] sau dấu hai chấm)


def go_cau_chua(text: str, vi_tri: list[tuple[int, int]]) -> str:
    """Gỡ khỏi `text` CÂU chứa mỗi khoảng ký tự trong `vi_tri` (dòng gạch đầu dòng / tiêu đề: câu trong phần thân; thân không còn gì ⇒ mất cả dòng;
    dòng dẫn "…:" không còn danh sách theo sau ⇒ gỡ luôn). Phần còn lại giữ nguyên chữ và thứ tự. Hàm thuần — không biết gì về loại kiểm."""
    if not vi_tri:
        return text
    cac_dong = text.split("\n")
    out: list[tuple[int, str]] = []  # (số thứ tự dòng gốc, chữ còn lại)
    pos = 0
    for i, dong in enumerate(cac_dong):
        dau = pos
        pos += len(dong) + 1
        if not any(a < dau + len(dong) and b > dau for a, b in vi_tri):
            out.append((i, dong))
            continue
        # dòng gạch đầu dòng / tiêu đề: giữ ký hiệu đầu dòng, gỡ câu trong phần thân như dòng văn thường; thân không còn gì ⇒ mất cả dòng. (Lượt thật
        # 21/11: một gạch đầu dòng ba câu của Sonnet chỉ có câu cuối chứa số tự tính — gỡ cả dòng làm mất hai câu có nguồn đứng trước.)
        dau_dong = _DONG_DANH_SACH.match(dong)
        than = dau_dong.end() if dau_dong else 0
        # ranh câu = sau dấu kết câu + khoảng trắng; KHÔNG cắt sau chữ viết tắt ("TP. Huế" — review phiên B: phần còn lại cụt thành "Từ TP.")
        moc = [than] + [m.end() for m in _RANH_CAU.finditer(dong, than) if not _VIET_TAT_CUOI.search(dong[:m.start()])] + [len(dong)]
        con = "".join(dong[x:y] for x, y in zip(moc, moc[1:]) if not any(a < dau + y and b > dau + x for a, b in vi_tri)).strip()
        if con:
            out.append((i, dong[:than] + con))

    def dong_ke(dongs: list[str]) -> str:
        return next((d for d in dongs if d.strip()), "")

    giu = []
    for k, (i, dong) in enumerate(out):
        # dòng dẫn "…:" mà trong chữ gốc đứng trước một danh sách, nay không còn dòng danh sách nào theo sau ⇒ gỡ luôn (không để "Hai cách đi [2]:" trơ trọi)
        if (_DONG_DAN.search(dong) and _DONG_DANH_SACH.match(dong_ke(cac_dong[i + 1:]))
                and not _DONG_DANH_SACH.match(dong_ke([d for _, d in out[k + 1:]]))):
            continue
        giu.append(dong)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(giu)).strip()


def _so_la(trace: AnswerTrace, text: str, flags: AssistantFlags | None, query: str) -> list[tuple[str, str, int, int]]:
    """Phép kiểm số (D8): (loại kiểm, số, đầu, cuối) của mọi số thời tiết / khoảng cách trong chữ model nằm NGOÀI tập cho phép. Tập cho phép = số code
    in (khối dự báo, dòng khoảng cách) ∪ số trong đoạn kho được trích ∪ — từ 21/11/2026 — số ĐỨNG KÈM ĐƠN VỊ của đúng phép kiểm đó trong câu hỏi của
    lượt này và câu hỏi liền trước: người dùng nhắc một con số ("63 % thì mưa nhiều không", "2 mm là mưa phùn à") thì model được nhắc theo (5 / 7 lượt
    bị rút oan ở lượt người dùng mô phỏng). Số KHÔNG kèm đơn vị trong câu hỏi (ngày tháng, số người, số tiền) không vào tập. Cách so số không đổi:
    2 khác 2,1."""
    cau_hoi = [query] + [cau for cau, _ in trace.history[-1:]]
    out: list[tuple[str, str, int, int]] = []
    if flags is not None and flags.thoi_tiet:
        tool = trace.thoi_tiet
        cho_phep = tt.tap_so(tool["khoi"]) if tool and tool["khoi"] else set()
        cho_phep |= tt.tap_so(" ".join(e for src in (trace.cited or ()) if src.source != lt2.NGUON_LICH_SOURCE for e in src.excerpts))  # nguồn lịch (giờ, phút) không mở rộng số thời tiết
        cho_phep |= {s for cau in cau_hoi for s in tt.so_kem_don_vi(cau)}
        out += [("thoi_tiet", s, a, b) for s, a, b in tt.vi_tri_so_thoi_tiet(text) if s not in cho_phep]
    so_code = [d for k in (trace.khoang_cach or []) + (trace.gan_diem or []) for d in k["dong"]]  # cờ `gan_diem` tắt ⇒ chỉ có phần khoảng cách, như cũ
    if so_code:  # số km / phút trong chữ model ⊂ số code dựng ∪ số trong đoạn kho được trích ∪ số kèm đơn vị cùng loại trong câu hỏi
        theo_loai = kc.tap_so_theo_loai(" ".join(so_code))  # số code dựng: km ↔ thời gian tách riêng
        chung = kc.tap_so(" ".join(e for src in (trace.cited or ()) if src.source not in (kc.NGUON_SOURCE, gd.NGUON_SOURCE, lt2.NGUON_LICH_SOURCE)
                                   for e in src.excerpts))  # đoạn kho: mọi số
        hoi = [kc.tap_so_theo_loai(cau) for cau in cau_hoi]  # câu hỏi: chỉ số kèm đơn vị, tách km ↔ thời gian ("đoàn 15 người" không mở "15 km")
        # Nguồn lịch (cờ `lich_vao_hoi_thuong`): chỉ nhận số CÓ ĐƠN VỊ thời gian do code in ("8 giờ", "15 phút") vào tập thời gian — phép này xét mọi
        # số kèm đơn vị thời gian trong chữ model nên thiếu thì câu nêu đúng số giờ của lịch bị rút (review B M1); không nhận mọi số của nguồn lịch
        # (giờ đồng hồ "10:30" sẽ cho qua "30 phút" bịa), không nới tập km
        lich_tg = kc.tap_so_theo_loai(" ".join(e for src in (trace.cited or ()) if src.source == lt2.NGUON_LICH_SOURCE for e in src.excerpts))["tg"]
        cho_phep_kc = {loai: tap | chung | (lich_tg if loai == "tg" else set()) | {s for h in hoi for s in h[loai]} for loai, tap in theo_loai.items()}
        out += [("khoang_cach", s, a, b) for loai, s, a, b in kc.vi_tri_so_khoang_cach(text) if s not in cho_phep_kc[loai]]
    return out


def _go_so_la(trace: AnswerTrace, text: str, flags: AssistantFlags | None, query: str, la: list[tuple[str, str, int, int]]) -> str:
    """Phép kiểm số trượt ở lượt KHÔNG có lịch ⇒ không rút cả câu trả lời. Nấc 1: gỡ câu / dòng chứa số lạ; phần còn lại còn trích dẫn, qua bộ kiểm
    trích dẫn và không còn số lạ ⇒ đó là câu trả lời. Nấc 2: không còn gì dùng được ⇒ câu từ chối cố định (khối dự báo / câu bản tin chính thức vẫn
    do `_thoi_tiet_cuoi` nối). Trả chữ model sau xử lý; ghi `trace.kiem_so_go` để số đo và sổ vết đếm được từng lần trượt."""
    goc = unicodedata.normalize("NFC", text)  # vị trí của `la` tính trên chữ đã chuẩn NFC
    moi = go_cau_chua(goc, [(a, b) for _, _, a, b in la])
    trace.kiem_so_go = {"thoi_tiet": [s for loai, s, _, _ in la if loai == "thoi_tiet"], "khoang_cach": [s for loai, s, _, _ in la if loai == "khoang_cach"],
                        "nac": 1, "so_ky_tu_go": len(goc) - len(moi)}
    if moi and CITATION_PATTERN.search(moi):
        trace.answer = moi
        check_citations(trace)
        if trace.citation_error is None and not _so_la(trace, moi, flags, query):
            return moi
        trace.citation_error = None  # phần còn lại không đứng được ⇒ xuống nấc 2, không báo lỗi
    trace.kiem_so_go["nac"] = 2
    trace.answer, trace.cited = INSUFFICIENT_ANSWER, ()
    return INSUFFICIENT_ANSWER


def _vet_go_so_la(trace: AnswerTrace, text: str) -> None:
    """Sổ vết debug (riêng tư, không phải `chat_metrics`): chữ model TRƯỚC khi gỡ — để đọc lại model đã viết gì ở lượt phép kiểm số trượt."""
    if trace.kiem_so_go is not None:
        trace.vet["kiem_so_go"] = {**trace.kiem_so_go, "chu_model": text}


def _la_luot_thuong(trace: AnswerTrace) -> bool:
    """Lượt hỏi đáp thường — không dựng lịch bằng công cụ, không biểu mẫu "Lên kế hoạch", không lịch bản 2 (cùng điều kiện `set_notice` dùng). Chỉ lượt
    thường mới được phục hồi sau khi kiểm trượt (gỡ câu / câu từ chối cố định); lượt lịch giữ kết cục rút lại như trước."""
    return not trace.bieu_mau and trace.lich is None and trace.lich_v2 is None


def kiem_so_sau_khi_viet(trace: AnswerTrace, text: str, flags: AssistantFlags | None, query: str = "") -> None:
    """Phép kiểm số của một lượt, sau bộ kiểm trích dẫn và trước phần code nối: ghi số lạ theo loại vào `trace.thoi_tiet_kiem` / `khoang_cach_kiem`
    (như trước); có số lạ ⇒ lượt có lịch vẫn bị rút lại như cũ, lượt thường thì gỡ câu / xuống câu từ chối cố định (`_go_so_la`)."""
    la = _so_la(trace, text, flags, query)
    if flags is not None and flags.thoi_tiet:
        trace.thoi_tiet_kiem = [s for loai, s, _, _ in la if loai == "thoi_tiet"]
    if trace.khoang_cach or trace.gan_diem:
        trace.khoang_cach_kiem = [s for loai, s, _, _ in la if loai == "khoang_cach"]
    if not la or trace.citation_error is not None:
        return
    if not _la_luot_thuong(trace):  # lượt có lịch: chữ do code ghép với khung ⇒ giữ cách cũ (rút lại), không gỡ từng câu
        loai, kiem = ("weather", trace.thoi_tiet_kiem) if trace.thoi_tiet_kiem else ("distance", trace.khoang_cach_kiem)
        trace.citation_error = CitationIntegrityError(f"{loai} numbers without source: {len(kiem)}")
    else:
        _go_so_la(trace, text, flags, query, la)
        _vet_go_so_la(trace, text)


_CO_PHONG_LUU_TRU = re.compile(
    r"\b(?:còn\s+(?:\d+\s+)?phòng(?:\s+trống)?|hết\s+phòng|đã\s+hết\s+phòng|phòng\s+còn\s+trống|còn\s+chỗ\s+trống|đảm\s+bảo\s+còn\s+phòng)\b",
    re.IGNORECASE,
)
_PHU_DINH_PHONG = re.compile(
    r"(?:chưa\s+kiểm(?:\s+tra)?|không\s+(?:có\s+thông\s+tin|kiểm\s+tra(?:\s+được)?|rõ)|chưa\s+rõ|tự\s+kiểm\s+tra|kiểm\s+tra\s+(?:trực\s+tiếp|lại|trên))[^.!?\n]{0,40}$",
    re.IGNORECASE,
)
_GIA_TIEN_LUU_TRU = re.compile(r"(\d[\d.,]*)\s*(?:đồng|vnd|vnđ|k\b|triệu|tr\b|usd|\$|đ(?:/|\b))", re.IGNORECASE)


def _kiem_tra_luu_tru(trace: AnswerTrace, text: str) -> None:
    """Hậu kiểm lượt dùng `goi_y_luu_tru`: chặn bịa giá phòng hoặc tình trạng còn phòng kể cả khi model gắn mã `[1]`."""
    if not trace.goi_y_luu_tru or trace.citation_error is not None:
        return
    t = unicodedata.normalize("NFC", text or "")
    for m in _CO_PHONG_LUU_TRU.finditer(t):
        if not _PHU_DINH_PHONG.search(t[:m.start()]):
            trace.citation_error = CitationIntegrityError("lodging availability without source")
            return
    nguon_kb = " ".join(
        e for src in (trace.cited or ()) if src.source != gylt.NGUON_SOURCE for e in src.excerpts
    )
    so_tien_kb = {re.sub(r"[.,]", "", g.group(1)) for g in _GIA_TIEN_LUU_TRU.finditer(nguon_kb)}
    for g in _GIA_TIEN_LUU_TRU.finditer(t):
        if re.sub(r"[.,]", "", g.group(1)) not in so_tien_kb:
            trace.citation_error = CitationIntegrityError("lodging price without source")
            return


def luu_tru_cho_giao_dien(trace: AnswerTrace) -> dict | None:
    """Dữ liệu lưu trú có kiểu (`goi_y_luu_tru`) để UI tự dựng thẻ + 3 link OTA + nhãn cứng không phụ thuộc chữ model."""
    if (
        not trace.goi_y_luu_tru
        or trace.citation_error is not None
        or trace.fixed_outcome is not None
        or trace.lich is not None
        or trace.lich_v2 is not None
    ):
        return None
    for item in reversed(trace.goi_y_luu_tru):
        du_lieu = item.get("du_lieu") if isinstance(item, dict) else None
        if isinstance(du_lieu, dict) and du_lieu.get("co_so"):
            return du_lieu
    return None


def _finish_generated(trace: AnswerTrace, flags: AssistantFlags | None = None, query: str = "") -> None:
    """Sau lần sinh: dừng ở thẻ hỏi lại (B5 D15) ⇒ lượt hỏi lại (không chữ, không kiểm citation); chạm `max_turns` (cờ generator, B2 D5) ⇒ câu
    từ chối cố định `max_turns`; lượt có lịch ⇒ ghép dòng "Mình hiểu" + chữ model + khối ghi chú (D12, D4b) rồi kiểm citation + kiểm cuối (D8);
    còn lại ⇒ kiểm citation trên sổ nguồn (cờ `lich_trinh` bật mà chữ có dạng lịch ⇒ kiểm cuối với khung rỗng, D8 (7))."""
    clarify = getattr(trace.generated, "clarify", None)
    if clarify is not None:
        trace.clarify = clarify
        _set_fixed(trace, "", "hoi_lai")
        return
    if getattr(trace.generated, "bao_vong_cuoi", False) and trace.tools:  # cờ `vong_cuoi_chi_viet`: dấu đếm (như `khong_co` của công cụ khoảng cách) — công cụ
        trace.tools[-1]["bao_vong_cuoi"] = True                             # chạy sau cùng của lượt là công cụ mang dòng báo (sau nó không còn công cụ nào)
    if getattr(trace.generated, "hit_max_turns", False):  # getattr: generator thay thế trong test chỉ có `text` (như route, B68 m-4)
        _dat_tu_choi_max_turns(trace, flags)
        return
    text = bo_cau_tu_choi_cuoi(trace.generated.text)
    if trace.nhieu_y and chi_y_thieu(text):  # chốt (a) vòng 2: không ý nào có Bằng chứng ⇒ đúng câu từ chối cũ (đi đường từ chối + cổng web cũ)
        text, trace.chi_y_thieu = INSUFFICIENT_ANSWER, True
    if _noi_that_lam_thay(trace, text):
        return
    if trace.lich is not None:
        bang, khung, nguon = flags.bang_lich, trace.lich["khung"], trace.lich["nguon"]
        if text.strip() == INSUFFICIENT_ANSWER:  # B171 T3 (b): có khung mà model từ chối ⇒ code dựng lời lịch tối thiểu (stream: `_chu_giu_lai`)
            text = trace.lich["chu_thay"] = lt.loi_lich_toi_thieu(bang, khung, nguon)
        loi = lt.kiem_cuoi(bang, text, khung, nguon)
        trace.lich["minh_hieu"] = lt.dong_minh_hieu(khung)
        trace.lich["ghi_chu"] = lt.khoi_ghi_chu(bang, khung, nguon, trace.lich.get("them_dong", ()))
        trace.lich["nhac_lai"] = lt.dem_nhac_lai(bang, text, khung)
        trace.answer = "\n\n".join(part for part in (trace.lich["minh_hieu"], text, trace.lich["ghi_chu"]) if part)
    else:
        loi = lt.kiem_cuoi(flags.bang_lich, text, None) if flags is not None and flags.lich_trinh and lt.co_dang_lich(text) else []
        trace.answer = text
    check_citations(trace)
    if trace.lich is not None or loi:
        trace.lich_kiem = loi
    if loi and trace.citation_error is None:  # D8: hỏng ⇒ xử như citation hỏng hôm nay (rút lại + lời báo + "Thử lại")
        trace.citation_error = CitationIntegrityError("itinerary check failed: " + ",".join(loi))
    if trace.goi_y_luu_tru and _la_luot_nguy_hiem_bao_lu(query, trace):
        # P1: model gọi `goi_y_luu_tru` trước khi gọi `thoi_tiet("bao_lu")` trong cùng một lượt ⇒ xoá gợi ý lưu trú, xoá NGUON_SOURCE và giữ cảnh báo bão/lũ
        trace.goi_y_luu_tru = None
        trace.so_nguon = [s for s in trace.so_nguon if s.source != gylt.NGUON_SOURCE]
        trace.cited = tuple(s for s in (trace.cited or ()) if s.source != gylt.NGUON_SOURCE)
        text = trace.answer = tt.CAU_DAN_BAO_LU
        trace.citation_error = None
        trace.vet["p1_xoa_luu_tru"] = True
    kiem_so_sau_khi_viet(trace, text, flags, query)
    _kiem_tra_luu_tru(trace, text)
    if flags is not None and flags.thoi_tiet:
        _thoi_tiet_cuoi(trace)


def lich_cho_giao_dien(trace: AnswerTrace, flags: AssistantFlags, cau_goc: str) -> dict | None:
    """D11 + D12 (a): dữ liệu có cấu trúc cho giao diện khi lượt có lịch — link bản đồ (code dựng) + thẻ "Sửa" chọn sẵn tham số đã dùng
    (`cau_goc` = câu người dùng gõ, không phải câu ghép; "Gửi" của thẻ = câu ghép B4 D4). Lịch bản 2 ⇒ khung + câu cuối (giao diện vẽ từ khung)."""
    if trace.lich_v2 is not None:
        v = trace.lich_v2
        return {"phien_ban": 2, "lich": v["lich"], "cau": v["cau"], "so_cau_du_phong": v.get("so_cau_du_phong")}
    if trace.lich is None:
        return None
    khung = trace.lich["khung"]
    ts = khung["tham_so"]
    sua = the_hoi_lai("lich_trinh", list(TRUONG_THEO_LOAI["lich_trinh"]), cau_goc)
    sua["chon"] = {k: ts[k] for k in TRUONG_THEO_LOAI["lich_trinh"] if ts[k] and not (k == "so_ngay" and ts["so_ngay_tam"])}
    return {"ban_do": lt.ban_do(flags.bang_lich, khung, flags.toa_do_lich if flags.ban_do_lich else None), "sua": sua}


async def answer_query(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                       today: str | None = None, flags: AssistantFlags | None = None) -> None:
    """Tuyến `tro_ly_hue` không stream: lần tìm đầu (theo `flags.lan_tim_dau`) → sinh một lần, hoặc trợ lý có công cụ (`flags.uses_tools`)
    → `check_citations`, điền `trace`. Lỗi đi ra nguyên kiểu như `prepare_answer`, thêm `GenerationError` (sinh); lỗi tìm trong công cụ
    ra đúng lỗi gốc."""
    flags = flags or AssistantFlags()
    tool_prompt = await _before_model(query, retrieval_service, context_builder, generator, trace, recorder, today, flags)
    if trace.fixed_outcome is not None:
        return

    started = time.perf_counter()
    call_log = CallLog()
    try:
        if flags.uses_tools:
            instructions = _assistant_instructions(generator, trace, trace.nhieu_y, flags.kiem_du_bang_chung)
            tool_fn = tool_for_turn(query, retrieval_service, context_builder, trace, today, instructions, flags.so_lan_tim_kho,
                                    tach_cau_tim=flags.tach_cau_tim_model, **_the_noi_kwargs(trace, flags, query))
            extra = _lich_extra(query, retrieval_service, context_builder, trace, today, instructions, flags)
            try:
                trace.generated = await generator.generate_with_tools(tool_prompt, tool_fn, call_log, **_history_kwargs(trace), **extra)
            except GenerationError:
                if trace.tool_error is not None:
                    raise trace.tool_error from None
                raise
        else:
            # `today` chỉ truyền khi có: generator thay thế trong test route chỉ nhận (query, context)
            kwargs = {"call_log": call_log} if today is None else {"call_log": call_log, "today": today}
            if flags.kiem_du_bang_chung:
                kwargs["kiem_du_bang_chung"] = True
            trace.generated = await generator.generate_answer(query, trace.packed.text, **kwargs, **_history_kwargs(trace))
    finally:
        trace.generation_ms = elapsed_ms(started)  # có cả khi model lỗi (route log `generation_failed` kèm thời gian)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)  # cả khi lượt lỗi sau phản hồi (review C128 m-1)
    if recorder:
        recorder.record_generation_result(trace.generated)
    _finish_generated(trace, flags, query)
    if flags.uses_tools:
        await _cuu_max_turns(query, generator, trace, flags, today, None)
        await _viet_lai_het_luot(query, generator, trace, flags, today, None)
        await _viet_lai_trich_dan_cau(query, generator, trace, flags, today, None)


def _lich_extra(query, retrieval_service, context_builder, trace, today, instructions, flags) -> dict:
    """Cờ `lich_trinh` bật ⇒ công cụ thứ hai cho generator; B5b: cờ `thoi_tiet` bật ⇒ code dò ngữ cảnh thời tiết của câu, và **chỉ khi** câu cuối /
    câu hỏi liền trước có từ khoá ⇒ thêm công cụ `thoi_tiet` (D4). Cờ tắt ⇒ {} (generator gọi y như trước — Q1)."""
    extra = {}
    luon = flags.cong_cong_cu in ("luon", "linh_hoat")  # đưa công cụ ở mọi lượt (giữ các rào cứng: ngoài 7 ngày, bão/lũ, số tính sẵn)
    if flags.cong_cong_cu == "linh_hoat":
        extra["linh_hoat"] = True
    lap_kw = {"chong_lap": True} if flags.chong_lap_cong_cu else {}
    if flags.lich_trinh:
        extra["lich_trinh_fn"] = lich_trinh_for_turn(query, retrieval_service, context_builder, trace, today, instructions, flags.bang_lich,
                                                     flags.du_bao if flags.thoi_tiet else None)
    if flags.thoi_tiet:
        tu_khoa, ngoai_7 = tt.co_tu_khoa_luot(query, trace.history), tt.ngoai_7_ngay(query, hom_nay_vn())
        # vòng chỉnh 1 (A duyệt, sửa D3): câu ngoài 7 ngày ⇒ KHÔNG đưa công cụ (không số dự báo nào để model chép) — code nối câu cố định
        trace.thoi_tiet_ctx = {"bao_lu": tt.la_cau_bao_lu(query), "ngoai_7": ngoai_7, "buoi": tt.co_buoi(query), "tu_khoa": tu_khoa,
                               "co_cong_cu": (tu_khoa or luon) and not ngoai_7}
        if flags.bao_lu_cong_cu:  # plan 17/11 (đã lùi theo luật 2.5): cổng = từ thời tiết + từ nguy hiểm thời tiết (câu cuối / câu liền trước); lưới rộng
            tu_khoa = tt.co_tu_khoa_luot_rong(query, trace.history)
            trace.thoi_tiet_ctx.update(bao_lu=tt.la_luot_bao_lu(query, trace.history), bao_lu_cau=tt.la_cau_bao_lu_rong(query),
                                       bao_lu_cong_cu=True, bao_lu_model=trace.bao_lu_lan_dau, luoi_cuoi=_luot_bao_lu(query, trace.history),
                                       tu_khoa=tu_khoa, co_cong_cu=(tu_khoa or luon) and not ngoai_7)
        tuan_sau = tt.ngay_tuan_sau(query, hom_nay_vn())
        if tuan_sau and not ngoai_7:  # rà nợ 15/11: "tuần sau" có phần trong 7 ngày ⇒ code đặt khoảng ngày (không có ⇒ khoá vắng, như trước)
            trace.thoi_tiet_ctx["tuan_sau"] = tuan_sau
        if trace.thoi_tiet_ctx["co_cong_cu"]:
            trace.thoi_tiet_ctx["dau_hieu_thoi_tiet"] = tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem(query, trace.history)
            extra["thoi_tiet_fn"] = thoi_tiet_for_turn(trace, flags.du_bao, **lap_kw)
    # như thời tiết — lượt không có từ khoá ⇒ danh sách công cụ như cũ (Q1); số đã tính sẵn trước lần gọi đầu (`trace.khoang_cach`) ⇒ không đưa công cụ
    if flags.khoang_cach and trace.khoang_cach is None and (luon or kc.co_tu_khoa_luot(query, trace.history)):
        extra["khoang_cach_fn"] = khoang_cach_for_turn(trace, flags.khoang_cach_bang, flags.khoang_cach_trang_thai, **lap_kw)
    if flags.ngay_lich and (luon or nl.co_tu_ngay_luot(query, trace.history)):  # T1: như thời tiết — lượt không có từ chỉ ngày ⇒ danh sách công cụ như cũ (Q1)
        extra["ngay_lich_fn"] = ngay_lich_for_turn(trace, query, **lap_kw)
    bai_theo_rel = {bai.rel: bai for bai in flags.muc_luc or ()}
    if flags.gan_diem and (luon or gd.co_tu_khoa_luot(query, trace.history)):  # cờ tắt / lượt không có từ "gần…" ⇒ không truyền, danh sách công cụ như cũ
        extra["gan_diem_fn"] = gan_diem_for_turn(trace, flags.khoang_cach_bang, flags.quan_bang, flags.quan_toa_do or {},
                                                 bai_theo_rel,
                                                 {i: d["nguon"] for i, d in flags.bang_lich_v2.theo_id.items()} if flags.bang_lich_v2 else {},
                                                 in_gio=flags.gan_diem_gio, **lap_kw)
    if flags.liet_ke_bai and flags.muc_luc is not None:  # cờ tắt ⇒ không truyền, danh sách công cụ như cũ
        extra["liet_ke_fn"] = liet_ke_for_turn(trace, flags.muc_luc, **lap_kw)
    if flags.goi_y_mua_nang and flags.bang_lich_v2 is not None and not _la_luot_nguy_hiem_bao_lu(query, trace) and (luon or mn.co_tu_khoa_luot(query, trace.history)):
        mn_kw = {**lap_kw, **({"toi_uu": True} if flags.toi_uu_dot2_va_viet_lai else {})}
        extra["mua_nang_fn"] = mua_nang_for_turn(trace, query, flags.bang_lich_v2, flags.khoang_cach_bang, flags.du_bao,
                                                 bai_theo_rel, **mn_kw)
    if flags.so_sanh_diem_den and flags.bang_lich_v2 is not None and (luon or ss.co_tu_khoa_luot(query, trace.history)):
        ss_kw = {**lap_kw, **({"toi_uu": True} if flags.toi_uu_dot2_va_viet_lai else {})}
        extra["so_sanh_fn"] = so_sanh_for_turn(trace, flags.bang_lich_v2, flags.khoang_cach_bang, flags.the_noi_bang,
                                               bai_theo_rel, **ss_kw)
    if flags.tinh_ve_tham_quan:
        tv_kw = {**lap_kw, **({"toi_uu": True} if flags.toi_uu_dot2_va_viet_lai else {})}
        extra["tinh_ve_fn"] = tinh_ve_for_turn(trace, flags.bang_lich_v2, flags.the_noi_bang, bai_theo_rel, **tv_kw)
    if flags.goi_y_luu_tru and flags.luu_tru_bang is not None and not _la_luot_nguy_hiem_bao_lu(query, trace):
        lt_kw = {**lap_kw, **({"toi_uu": True} if flags.toi_uu_dot2_va_viet_lai else {})}
        extra["goi_y_luu_tru_fn"] = goi_y_luu_tru_for_turn(trace, flags.luu_tru_bang, flags.bang_lich_v2, query=query, **lt_kw)
    if flags.het_luot_bo_cong_cu:  # hết lượt tìm thật ⇒ generator ẩn `tim_kho` ở lượt gọi model kế tiếp (cờ tắt ⇒ không truyền, gọi y như trước)
        extra["con_luot_fn"] = lambda: trace.model_searches < flags.so_lan_tim_kho
    if trace.nhieu_y:  # lời dặn theo ý (cờ tắt / câu một ý ⇒ không truyền, gọi y như trước)
        extra["nhieu_y"] = True
    if flags.vong_cuoi_chi_viet:  # cờ tắt ⇒ không truyền, công cụ không có điều kiện bật mới (giống byte)
        extra["vong_cuoi_chi_viet"] = True
    if flags.kiem_du_bang_chung:
        extra["kiem_du_bang_chung"] = True
    if flags.canh_bao_vong_con_lai:
        extra["canh_bao_vong_con_lai"] = True
    if flags.toi_uu_dot2_va_viet_lai:
        extra["toi_uu_dot2_va_viet_lai"] = True
    return extra


# ---------- Biểu mẫu "Lên kế hoạch" (cổng đợt 1, spec D3) ----------

async def _xep_bieu_mau(query: str, retrieval_service, context_builder, trace: AnswerTrace, flags: AssistantFlags, today: str | None) -> str:
    """D3: **code** gọi `lich_trinh` với giá trị nút ở cả 4 trường (không định tuyến, model không chọn công cụ, không lần tìm đầu). Trả ngữ cảnh
    cho lần sinh không công cụ = đúng chuỗi công cụ trả ở đường câu tự do (chữ khung có `LICH_TRINH_LUAT` + đoạn nguồn của các điểm).
    `instructions=None`: ngân sách đếm như đường sinh một lần (lời dặn trả lời) — đúng lần gọi của lượt này."""
    t = trace.truong
    lich_trinh = lich_trinh_for_turn(query, retrieval_service, context_builder, trace, today, None, flags.bang_lich,
                                     flags.du_bao if flags.thoi_tiet else None)
    return await lich_trinh(t["so_ngay"], t.get("di_cung"), t.get("kieu_di"), t.get("so_thich"), None)


async def answer_bieu_mau(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags) -> None:
    """Lượt biểu mẫu không stream (`POST /api/chat`): code xếp ⇒ một lần sinh **không công cụ** bằng agent biểu mẫu (luật lịch trong lời dặn +
    mức suy luận thấp — V5 X1c) ⇒ kiểm như lượt có lịch (`_finish_generated`).
    Lỗi tìm / ngữ cảnh / sinh đi ra nguyên kiểu như `answer_query`."""
    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")
    today = _today(flags, trace)
    if flags.len_ke_hoach_v2:  # bản 2: khung + câu theo mục (`llm/len_ke_hoach.py`); cờ tắt ⇒ đường dưới y như cũ
        from llm import len_ke_hoach  # import muộn: module đó import lõi này
        await len_ke_hoach.answer_v2(query, retrieval_service, context_builder, generator, trace, flags, today)
        set_notice(trace, flags)
        return
    context = await _xep_bieu_mau(query, retrieval_service, context_builder, trace, flags, today)
    started = time.perf_counter()
    call_log = CallLog()
    try:
        trace.generated = await generator.generate_answer(query, context, today=today, call_log=call_log, bieu_mau=True,
                                                          **_history_kwargs(trace))
    finally:
        trace.generation_ms = elapsed_ms(started)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)
    _finish_generated(trace, flags, query)
    set_notice(trace, flags)


# ---------- Một lượt có định tuyến (Phase 9 B1, plan D1, D6) ----------

def _set_fixed(trace: AnswerTrace, text: str, outcome: str) -> None:
    trace.answer, trace.cited, trace.fixed_outcome = text, (), outcome


async def _pick_route(query: str, generator, trace: AnswerTrace, flags: AssistantFlags) -> None:
    """Định tuyến (model) ⇒ câu cố định cho `ngoai_pham_vi`; `khan_cap` đi agent Huế (phương án B của bậc G, spec bản 13 §12.2: bỏ câu soạn sẵn
    khẩn cấp, giữ 4 tuyến). Còn lại để `trace.route` cho bước sau."""
    if flags.router and generator is not None:
        started = time.perf_counter()
        call_log = CallLog()
        try:
            if flags.lan_tim_dau in ("v1", "v3"):  # B2 D2: định tuyến viết luôn câu tìm (cùng một lần gọi)
                trace.route, queries = await generator.route_search(query, call_log, flags.lan_tim_dau)
                trace.cau_tim = [q.strip() for q in queries if q.strip()] or None
                trace.cau_tim_rong = trace.cau_tim is None  # rỗng ⇒ tìm bằng câu gốc, đếm được
            else:
                trace.route = await generator.route(query, call_log, **_history_kwargs(trace))
        except GenerationError:
            trace.route, trace.route_error = ROUTE_TRO_LY_HUE, "router_failed"  # lỗi ⇒ đường cũ (D3)
        finally:
            trace.routing_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, "router")
    if trace.route == ROUTE_KHAN_CAP:  # phương án B G: không câu soạn sẵn — trả lời như câu về Huế; log giữ dấu định tuyến đã chọn khẩn cấp
        trace.route, trace.emergency_by = ROUTE_TRO_LY_HUE, "router"
    elif trace.route == ROUTE_NGOAI_PHAM_VI:
        _set_fixed(trace, OUT_OF_SCOPE_ANSWER, "out_of_scope")


def _today(flags: AssistantFlags, trace: AnswerTrace) -> str | None:
    trace.today = today_line() if flags.today_line else None
    return trace.today


# ---------- Cổng web (Phase 9 B6, plan B6 bản 3 D1–D9) ----------

def web_gate_open(trace: AnswerTrace, flags: AssistantFlags, tim_web) -> bool:
    """D1 — luật mở cổng, **một chỗ** cho cả 3 đường: câu trả lời kho đúng bằng câu từ chối "không đủ thông tin" (so sau `strip()` như cờ
    `refusal`; không mở với câu ngoài phạm vi) ∧ outcome thường (model tự từ chối, hoặc ngữ cảnh rỗng `refusal_no_sources`) — không chạm trần,
    không lỗi công cụ, không hỏi lại ∧ tuyến `tro_ly_hue` (khẩn cấp / ngoài phạm vi / trò chuyện không mở) ∧ chưa tra ∧ lượt không có lịch ∧
    không phải lượt ghép từ nút (D8) ∧ cờ bật ∧ nơi gọi có hàm tra (bộ đánh giá không truyền ⇒ không tra)."""
    return (flags.tra_web and tim_web is not None and trace.web is None and trace.route == ROUTE_TRO_LY_HUE
            and trace.fixed_outcome in (None, "refusal_no_sources") and trace.citation_error is None and trace.tool_error is None
            and trace.clarify is None and trace.lich is None and trace.truong is None
            and ((trace.answer or "").strip() == INSUFFICIENT_ANSWER
                 # cờ `web_chi_khi_tu_choi`: lượt nhiều ý đã trả lời được một phần KHÔNG mở cổng web nữa (dòng "Tư liệu chưa có thông tin về…" vẫn còn nguyên)
                 or (trace.nhieu_y and not flags.web_chi_khi_tu_choi and co_y_thieu(trace.answer or ""))))


_CO_TRICH = re.compile(r"\[(?:Nguồn\s*)?\d+\]")


def co_y_thieu(answer: str) -> bool:
    """Cờ `cau_nhieu_y`: câu trả lời có ít nhất một dòng mở đầu ĐÚNG hằng `CAU_Y_THIEU` (sau khoảng trắng / gạch đầu dòng) và dòng đó KHÔNG có
    trích dẫn [n] / [Nguồn n] — model đánh dấu ý kho không có ⇒ mở cổng web cho phần thiếu (truy vấn vẫn từ câu người dùng, D2 — lượt nhiều ý luôn dùng câu gõ, kể cả khi cờ `web_cau_noi_tiep` bật)."""
    for dong in answer.splitlines():
        d = dong.strip().lstrip("-*•").strip()
        if d.startswith(CAU_Y_THIEU) and not _CO_TRICH.search(d):
            return True
    return False


def so_y_thieu(answer: str) -> int:
    """Số dòng "Tư liệu chưa có thông tin về: …" của câu trả lời (cùng phép nhận dòng với `co_y_thieu`: đầu dòng, không kèm trích dẫn) — cho dòng số đo:
    MỘT con số, không chữ. 21/11/2026: ở lượt mốc 12 vai, 86 % lượt nhiều ý của model đang chạy có dòng này; trước đó muốn biết phải đọc tay."""
    return sum(1 for dong in answer.splitlines() if (d := dong.strip().lstrip("-*•").strip()).startswith(CAU_Y_THIEU) and not _CO_TRICH.search(d))


def ve_y_thieu(query: str, answer: str) -> str:
    """Vế của câu người dùng ứng với các dòng "Tư liệu chưa có thông tin về: …": mỗi dòng ⇒ vế có nhiều từ chung nhất (hoà / 0 từ chung ⇒ bỏ qua
    dòng đó). Ghép các vế chọn được theo thứ tự trong câu; không chọn được / chọn hết ⇒ "" (mục web viết cho cả câu như trước). Chỉ trả chữ của
    người dùng."""
    thieu = [d[len(CAU_Y_THIEU):] for d in map(_dong_y_thieu, answer.splitlines()) if d.startswith(CAU_Y_THIEU) and not _CO_TRICH.search(d)]
    ve = [p.strip() for v in re.split(r"[,;?]", query) if v.strip() for p in _LIEN_TU.split(v) if _la_ve_hoi(p)]
    tu = lambda t: set(re.findall(r"\w+", t.casefold()))
    # từ đã có ở phần trả lời (dòng không phải ý thiếu, vd tên nơi) không tính ⇒ dòng ý thiếu nhắc lại tên nơi không làm hoà điểm (review B m-1)
    da_tra_loi = tu(" ".join(d for d in answer.splitlines() if not _dong_y_thieu(d).startswith(CAU_Y_THIEU)))
    chon = set()
    for t in thieu:
        tu_thieu = (tu(t) - da_tra_loi) or tu(t)
        diem = [len(tu(v) & tu_thieu) for v in ve]
        if diem and max(diem) > 0 and diem.count(max(diem)) == 1:
            chon.add(diem.index(max(diem)))
    if len(ve) < 2 or not chon or len(chon) == len(ve):
        return ""
    return "; ".join(ve[i].rstrip("?").strip() for i in sorted(chon))


def _dong_y_thieu(d: str) -> str:
    return d.strip().lstrip("-*•").strip()


def bo_cau_tu_choi_cuoi(text: str) -> str:
    """21/11/2026 (phiên đo, 1 / 3 lượt stream của một câu kho chỉ có một phần): model viết phần tìm được, có [n], rồi NỐI nguyên câu từ chối khuôn ở
    cuối ⇒ bộ kiểm trích nguồn coi là "câu từ chối mà có citation" ⇒ người dùng thấy lỗi sau khi chữ đã ra. Câu kết thúc bằng câu khuôn mà phần đứng
    trước có ít nhất một [n] ⇒ gỡ câu khuôn, giữ phần có nguồn (phần đó vẫn qua kiểm trích nguồn như mọi câu). Mọi trường hợp khác ⇒ nguyên chữ:
    đúng câu khuôn, câu khuôn nằm giữa, hoặc phần đứng trước không có nguồn (vẫn là lỗi như cũ)."""
    goc = text.rstrip()
    if goc == INSUFFICIENT_ANSWER or not goc.endswith(INSUFFICIENT_ANSWER):
        return text
    truoc = goc[: -len(INSUFFICIENT_ANSWER)].rstrip()
    return truoc if CITATION_PATTERN.search(truoc) and INSUFFICIENT_ANSWER not in truoc else text


def chi_y_thieu(answer: str) -> bool:
    """Chốt (a) vòng 2: mọi dòng có chữ đều mở đầu bằng `CAU_Y_THIEU` (không ý nào có Bằng chứng) ⇒ True. Câu rỗng ⇒ False."""
    dong = [_dong_y_thieu(d) for d in answer.splitlines() if d.strip()]
    return bool(dong) and all(d.startswith(CAU_Y_THIEU) for d in dong)


def _con_la_y_thieu(giu: str) -> bool:
    """Stream: chữ giữ lại tới giờ VẪN có thể thành câu chỉ-dòng-ý-thiếu (mọi dòng đủ đã là dòng thiếu; dòng đang dở là khúc đầu / dòng thiếu)."""
    *du, do = [_dong_y_thieu(d) for d in giu.splitlines()] or [""]
    return all(not d or d.startswith(CAU_Y_THIEU) for d in du) and (do.startswith(CAU_Y_THIEU) or CAU_Y_THIEU.startswith(do))


# 21/11/2026 (phiên đo đếm, 0 đồng): "bao xa" chưa được coi là từ hỏi ⇒ câu "A đến B bao xa, vào đó có mất vé không" đếm MỘT ý ⇒ không dùng lời dặn theo ý
# ⇒ cả hai model từ chối cả câu. Thêm "bao xa", "thì sao" và "ai" CHỈ trong cụm hỏi hẹp ("thờ ai", "do ai", "là ai", "của ai"). KHÔNG nhận "ai" / "sao" trần,
# kể cả ở cuối vế: review cùng ngày đặt 12 câu một ý sau khi đọc khuôn ⇒ 7 câu bị đếm nhầm ("khách sạn 4 sao, …", "nhà không có ai, …").
_VE_HOI = re.compile(r"(?<!\w)(bao nhiêu|gì|nào|đâu|mấy|bao lâu|bao xa|bao giờ|khi nào|tại sao|vì sao|thế nào|ra sao|thì sao|(?:là|do|thờ|của) ai)(?!\w)", re.IGNORECASE)
_CUOI_HOI = re.compile(r"(?<!\w)(không|chưa|nhỉ|vậy|hả)\s*$", re.IGNORECASE)
_LIEN_TU = re.compile(r"\s+(?:và|còn|với)\s+", re.IGNORECASE)


def _la_ve_hoi(v: str) -> bool:
    return bool(_VE_HOI.search(v) or _CUOI_HOI.search(v))


def so_y(cau: str) -> int:
    """Vòng 2 (b): số vế hỏi của câu người dùng — tách theo , ; ? rồi theo "và / còn / với"; một vế là ý hỏi khi có từ hỏi hoặc kết thúc bằng
    tiểu từ hỏi. Tách theo liên từ (14/11 chiều: câu "… mấy giờ và gần đó có … nào không?" đếm 1 ⇒ bị từ chối cả câu) chỉ thêm vế khi chính
    phần đó có từ hỏi ⇒ "bún bò và bánh khoái giá bao nhiêu" vẫn là 1. Đếm thiếu ⇒ về luật cũ (an toàn)."""
    return sum(_la_ve_hoi(p) for v in re.split(r"[,;?]", cau) if v.strip() for p in _LIEN_TU.split(v))


SO_DOAN_MOI_VE = 2  # cờ `tim_theo_ve`: số đoạn đầu lấy từ lần tìm riêng của mỗi vế hỏi (đếm 0 đồng 21/11: 2, 3, 4 đoạn mỗi vế cho cùng kết quả)
TRAN_SO_VE_TIM = 6  # nhiều nhất bấy nhiêu lần tìm thêm một lượt (65 tin nhiều ý của ba lượt mốc: nhiều nhất 6 vế) ⇒ thêm nhiều nhất 12 đoạn
# Từ hỏi cho riêng việc TÌM — rộng hơn `_VE_HOI` có chủ ý: nhận cả kiểu gõ tắt ("ko", "bn", "j", "đc ko") và từ hỏi trần ("sao", "ai").
_TU_HOI_TIM = re.compile(r"(?<!\w)(không|ko|k|hok|bao nhiêu|bn|mấy|nào|gì|j|đâu|sao|ai|khi nào|bao lâu|bao xa|bao giờ|chưa|hả|nhỉ|à|vậy)(?!\w)|\?", re.IGNORECASE)


# Cờ `tim_ve_bo_cut`: vế CỤT = không có gì để neo lần tìm — không tên riêng viết hoa, và sau khi bỏ từ hỏi / từ đệm (`_TU_DEM_VE`) cùng từ thuộc tính chung
# (`_TU_CHUNG_VE`: giờ, mở cửa, giá, vé, xa, gần…) còn dưới HAI từ mang nội dung. Tìm riêng một vế như vậy chỉ kéo về "giờ mở cửa" / "giá vé" của một nơi
# bất kỳ. Tên gõ thường ("đại nội", "bún bò") tự là hai từ mang nội dung ⇒ không cần bảng tên nơi.
_TU_DEM_VE = frozenset("""không ko k hok kh khong bao nhiêu bn mấy nào gì j đâu sao ai khi chưa hả nhỉ à vậy ạ nha nhé nhe á ơi ok oke okie thì là mà có được đc dc phải của
cho với và còn hay hoặc ở tại trong ngoài trên dưới ra vào về đi đến tới từ qua lại nữa thôi luôn rồi đã đang sẽ cũng chỉ vẫn rất lắm quá hơn nhất mình tôi em anh chị bạn
tớ nhà ta họ nó này đó kia đấy ấy thế nên cần muốn thấy biết xem giúp hộ dùm giùm một hai ba bốn các những vài cái lúc nếu như để vs ủa ừ ờ hỏi nốt tiện""".split())
_TU_CHUNG_VE = frozenset("""giờ mở cửa đóng giá vé tiền phí địa đường xa gần lâu mất xe km phút tiếng ngày hôm nay mai sáng trưa chiều tối đêm tuần tháng năm điểm nơi chỗ
tên số thông tin chi tiết cụ thể khác thêm""".split())
# Chủ thể đi lại / dịch vụ chỉ một hai từ mà từ của nó nằm trong hai tập trên ("xe", "vé", "tiền", "đêm"…) hoặc đứng một mình ("taxi", "wifi") — vế có
# một cụm này tự tìm được (lượt đọc của phiên khác 22/11: 15 / 25 vế kiểu "vé xe buýt bao nhiêu", "chợ đêm mở mấy giờ", "taxi bao nhiêu tiền" bị coi là cụt).
_CHU_DE_VE = re.compile(r"(?<!\w)(?:xe buýt|xe bus|xe ôm|xe máy|xe đạp|xe điện|xe khách|xích lô|thuê xe|gửi xe|đỗ xe|đậu xe|vé tàu|tàu hỏa|tàu hoả|máy bay|sân bay|bến xe|nhà ga"
                        r"|taxi|grab|thuyền|chợ đêm|đổi tiền|atm|wifi|homestay|khách sạn|nhà nghỉ|trong nhà|ngoài trời|ăn chay|ăn khuya|ăn sáng|ăn trưa|ăn tối)(?!\w)", re.IGNORECASE)


def _ve_cut(ve: str) -> bool:
    tu = re.findall(r"\w+", unicodedata.normalize("NFC", ve))
    thuong = [w.casefold() for w in tu]
    if _CHU_DE_VE.search(unicodedata.normalize("NFC", ve)):
        return False
    khong_noi_dung = lambda w: w in _TU_DEM_VE or w in _TU_CHUNG_VE or w.isdigit()
    ten_dau = (tu and tu[0][0].isupper() and len(tu[0]) >= 3 and not khong_noi_dung(thuong[0])
               and not (len(tu) > 1 and thuong[1] in ("đó", "này", "ấy", "kia", "nào")))  # "Lăng đó…", "Lịch này…" không phải tên
    if any(w[0].isupper() for w in tu[1:]) or ten_dau:
        return False  # tên riêng viết hoa; từ ĐẦU vế chỉ tính khi không phải từ đệm / từ chung viết hoa đầu câu ("Trên đó…", "Bao nhiêu km")
    return sum(not khong_noi_dung(w) for w in thuong) < 2


def cac_ve_tim(cau: str, bo_cut: bool = False) -> list[str]:
    """Các vế của một tin nhiều ý dùng làm CÂU TÌM riêng (cờ `tim_theo_ve`); bỏ vế trùng, nhiều nhất `TRAN_SO_VE_TIM` vế.
    KHÁC `so_y` có chủ ý — hàm này không quyết tin có nhiều ý hay không: cắt cả ở dấu chấm / chấm than / xuống dòng (giữ dấu ? ở cuối vế; dấu chấm /
    phẩy nằm NGAY TRƯỚC một chữ số thì không cắt — "200.000", "1,5 km"; soát khác hãng 22/11: câu tìm từng cụt thành "000 có gồm …"), nhận từ
    hỏi gõ tắt. Lý do: nhận nhầm một vế chỉ tốn hai đoạn thừa, còn bỏ sót một vế là mất đoạn kho của vế đó. Đếm 0 đồng 22/11/2026 trên 8 dòng
    "Tư liệu chưa có thông tin về…" SAI của model đang chạy: đoạn kho đúng vào ngữ cảnh 1 / 8 (tắt) ⇒ 3 / 8 nếu tách như `so_y` ⇒ 5 / 8 với cách này."""
    ve = [p.strip(" ,;.!\n") for v in re.split(r"(?<=[;?!\n])|(?<=[,.])(?!\d)", cau) if v.strip() for p in _LIEN_TU.split(v) if len(p.strip(" ,;?.!\n")) >= 8]
    return list(dict.fromkeys(v for v in ve if _TU_HOI_TIM.search(v) and not (bo_cut and _ve_cut(v))))[:TRAN_SO_VE_TIM]


def cau_cho_web(query: str, trace: AnswerTrace, flags: AssistantFlags | None) -> str:
    """Câu dùng cho phần web. Mặc định: câu người dùng gõ ở lượt này (D2). Cờ `web_cau_noi_tiep` + lượt có lịch sử + model đã tự tìm kho ⇒ câu tìm kho
    CUỐI model viết: model đã ghép chủ thể của lượt trước vào đó (đo 15/11: 9 / 9 lần nêu đúng tên), còn câu gõ thì cụt. Lượt đầu / model không tìm /
    câu tìm rỗng / lượt nhiều ý ⇒ như cũ."""
    # Lượt nhiều ý giữ câu gõ: câu tìm cuối của model có thể thuộc vế kho ĐÃ trả lời, còn mục web phải viết cho vế thiếu (review E M-1; chưa đo)
    if flags is not None and flags.web_cau_noi_tiep and trace.history and not trace.nhieu_y and trace.model_queries:
        cau = trace.model_queries[-1]
        if tw.cau_tim_web(cau).strip().casefold() != "huế":  # rỗng SAU bộ lọc (chỉ có dấu cách / số điện thoại / email) ⇒ không tra web bằng mỗi chữ "Huế"
            return cau
    return query


# Link chính thức của mục web câu cố định thiên tai (cùng hai địa chỉ với `tt.CAU_BAO_LU`); `id` chữ để không trùng số w n của sổ web
NGUON_CHINH_THUC = [
    {"id": "nchmf", "title": "Trung tâm Dự báo khí tượng thủy văn quốc gia — bản tin chính thức", "link": tt.NCHMF_URL, "domain": "nchmf.gov.vn", "ngay": None},
    {"id": "lu_quet", "title": "Cổng cảnh báo lũ quét, sạt lở", "link": tt.LU_QUET_URL, "domain": "luquetsatlo.nchmf.gov.vn", "ngay": None},
]


async def cong_web(query: str, generator, trace: AnswerTrace, tim_web, flags: AssistantFlags | None = None) -> None:
    """Sau khi cổng mở: truy vấn do code dựng từ câu hỏi lượt này (D2; cờ `web_cau_noi_tiep` + lượt có lịch sử ⇒ từ câu tìm kho cuối model viết —
    `cau_cho_web`, chữ model có chi tiết của lượt trước đi ra ngoài) ⇒ một lần tra (D3) ⇒ một lần gọi model riêng viết mục web (D4) ⇒ kiểm
    cuối (D5). Kết quả vào `trace.web`; câu trả lời kho (`trace.answer`) giữ nguyên. Tra lỗi / 0 kết quả / model lỗi / kiểm hỏng ⇒ câu cố định
    (không đoán, không thử lại). Lần tra ghi một mục `tools` (ms, trạng thái, số kết quả, USD — không chữ)."""
    cau_web = cau_cho_web(query, trace, flags)
    tu_model = cau_web != query
    xet = f"{cau_web} {query}" if tu_model else query  # luật chặn theo câu hỏi (thiên tai, thời gian thực, lưu trú) xét CẢ hai câu ⇒ chỉ chặt hơn
    cau_serper = tw.cau_tim_web(cau_web)
    kq = await tim_web(cau_serper)
    trace.vet["web"] = {"cau_gui_tra_web": cau_serper, "so_web": list(kq.so_web)}
    trace.tools.append({"name": "tra_web", "ms": kq.ms, "trang_thai": kq.trang_thai, "loi": kq.loi, "n_ket_qua": len(kq.so_web),
                        "usd": kq.usd, **({"cau_tu_model": True} if tu_model else {})})  # chỉ cờ, không chữ
    web = {"outcome": "web_loi", "text": tw.WEB_LOI_TEXT, "nguon": [], "n_ket_qua": len(kq.so_web), "n_ma": 0, "kiem": None,
           "usd_serper": kq.usd}
    trace.web = web
    if kq.trang_thai == "rong":
        web.update(outcome="web_rong", text=tw.WEB_RONG_TEXT)
    if kq.trang_thai != "ok":
        return
    # vòng chỉnh 1: câu thiên tai ⇒ không gọi model; câu cố định (NCHMF / chính quyền / 112) + link nguồn do code.
    # 18/11 (soát khác hãng): thêm MỌI lượt mà lưới cuối coi là lượt bão / lũ — cùng hàm `_luot_bao_lu` (câu này hoặc câu hỏi LIỀN TRƯỚC; cả "cảnh báo" +
    # từ thời tiết) — "vậy có nên ra biển không" sau một câu bão là lượt bão; thừa hơn sót. Luật này của mục web không theo cờ (như trước).
    # Hai địa chỉ chính thức do code đặt lên đầu danh sách link — câu cố định chỉ có tên cơ quan + 112, link Serper có thể toàn báo thường.
    # 22/11 (soát khác hãng): cả lượt mà model đã tự gọi công cụ thời tiết loại bão / lũ rồi từ chối — câu gõ không có từ nào của hai lưới trên.
    if tw.la_cau_thien_tai(xet) or _luot_bao_lu(xet, trace.history) or (trace.thoi_tiet_ctx or {}).get("bao_lu_model"):
        web.update(outcome="thien_tai", text=tw.THIEN_TAI_TEXT, nguon=NGUON_CHINH_THUC + list(kq.so_web))
        return
    call_log = CallLog()
    # câu nhiều ý: model viết mục web cho đúng vế ý thiếu (không viết lại ý kho đã trả lời — 14/11: số giờ web khác kho); Serper vẫn nhận cả câu
    ve = ve_y_thieu(query, trace.answer or "") if trace.nhieu_y else ""
    hoi_web = f"{cau_web} (chỉ viết cho phần: {ve} — phần còn lại đã có câu trả lời từ kho)" if ve else cau_web
    try:
        generated = await generator.generate_web_section(tw.dau_vao_model(hoi_web, kq.so_web), call_log)
    except GenerationError:
        web["kiem"] = ["model_loi"]
        return
    finally:
        record_llm_calls(trace, call_log.calls, "tra_web")
    trace.vet["web"]["chu_model"] = generated.text  # cả khi rào chặn (mục bị thay câu cố định) — để biết model đã viết gì
    text, suc_khoe = tw.tach_suc_khoe(generated.text)  # bỏ dấu sức khoẻ TRƯỚC mọi kiểm; câu cố định nối ở cuối, sau mọi nhánh
    loi = tw.kiem_muc_web(text, kq.so_web, tw.la_cau_luu_tru(xet), tw.la_cau_thoi_gian_thuc(xet), cau_hoi=query)
    web["kiem"] = loi
    if loi == ["so_thoi_gian_thuc"]:  # vòng chỉnh 1: câu thời gian thực có số / ngày giờ ⇒ câu cố định "chưa xác minh" + link nguồn
        web.update(outcome="chua_xac_minh", text=tw.CHUA_XAC_MINH_TEXT, nguon=list(kq.so_web))
    elif loi:  # D5 (iv): bỏ mục model viết, giữ câu từ chối của kho + câu cố định
        web.update(outcome="khong_tin_cay", text=tw.WEB_KHONG_TIN_CAY_TEXT)
    else:
        ma = tw.ma_da_dung(text)
        web.update(outcome="co_muc", text=text.strip(), n_ma=len(ma),
                   nguon=[s for s in kq.so_web if s["id"] in ma])  # chỉ nguồn được trích, đúng số w n của sổ
    if suc_khoe:
        web.update(text=f"{web['text']}\n\n{tw.SUC_KHOE_TEXT}", suc_khoe=True)


async def _web_stream(query: str, generator, trace: AnswerTrace, flags: AssistantFlags, tim_web):
    """Đường stream: cổng mở ⇒ trạng thái "đang tra web…" rồi tra. Mục web không stream từng chữ — phải kiểm cuối (D5) trước khi hiện; route
    gửi cả mục một sự kiện `web` sau `sources`."""
    if web_gate_open(trace, flags, tim_web):
        yield "status", {"stage": "tra_web"}
        await cong_web(query, generator, trace, tim_web, flags)


async def answer_turn(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                      recorder=None, tim_web=None) -> None:
    """Một lượt không stream (`POST /api/chat`, `answer_case`): luật khẩn cấp ⇒ định tuyến ⇒ trả lời theo tuyến ⇒ cổng web (B6; `tim_web` do route
    truyền, None ⇒ không tra). Lỗi như `answer_query`. Lượt biểu mẫu (D3) ⇒ `answer_bieu_mau` (không định tuyến, không web)."""
    if trace.bieu_mau:
        await answer_bieu_mau(query, retrieval_service, context_builder, generator, trace, flags)
        return
    await _pick_route(query, generator, trace, flags)
    if trace.fixed_outcome is not None:
        return
    if trace.route == ROUTE_TRO_CHUYEN:
        started = time.perf_counter()
        call_log = CallLog()
        try:
            trace.generated = await generator.generate_chat(query, call_log, **_history_kwargs(trace))
        finally:
            trace.generation_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, ROUTE_TRO_CHUYEN)
        trace.answer, trace.cited = trace.generated.text, ()  # trò chuyện không có sổ nguồn, không kiểm citation (D4)
        return
    await answer_query(query, retrieval_service, context_builder, generator, trace, recorder, _today(flags, trace), flags)
    set_notice(trace, flags)
    if web_gate_open(trace, flags, tim_web):
        await cong_web(query, generator, trace, tim_web, flags)


async def answer_turn_stream(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                             recorder=None, tim_web=None):
    """Cùng thứ tự `answer_turn` nhưng phát sự kiện: `("status", dict)` / `("delta", str)`. Kết thúc ⇒ `trace` đủ để route dựng `sources` /
    `error` / `notice` / `done`. Hạn giờ model bọc cả vòng đọc (spec streaming §4.3); tự dừng đọc (hết giờ / ngắt) ⇒ `cancel()` + đọc nốt
    trong vùng che (spec §4.5). Lỗi đi ra nguyên kiểu (route đổi thành sự kiện `error`)."""
    result = call_log = tool_state = None
    pending_generating = False
    cong_cu = None  # tên công cụ của lần gọi đang chạy (gọi lần lượt, `parallel_tool_calls=False`) — B5 D14 (b): mỗi công cụ một loại trạng thái
    da_phat_buoc = 0  # số bước `trace.buoc_lich` đã phát
    da_noi_dau = False  # D12 (a): dòng "Mình hiểu" đi liền trước chữ đầu của model
    dau_bao_lu = False  # cờ `bao_lu_cong_cu`: câu cố định trước chữ model (`_can_dau_bao_lu`)
    giu_chu: str | bool | None = None  # review C M-1: None = chưa có chữ; "" / chuỗi = đang giữ; False = không giữ
    call_route = None
    cho_kiem: str | None = None  # công tắc `giu_chu_toi_kiem`: chuỗi = chữ model đang gom, chờ phép kiểm nguồn; None = không gom (phát ngay như cũ)

    def chu_phat(text: str) -> str | None:
        """Một mảnh chữ của model ⇒ chữ phát ra lúc này; None = còn giữ (chừng nào còn có thể là câu từ chối). Dùng cho từng mảnh trong vòng đọc
        và, khi công tắc `giu_chu_toi_kiem` gom chữ, cho cả chuỗi đã gom sau phép kiểm — cùng một đường nên chữ người dùng thấy không đổi."""
        nonlocal giu_chu, dau_bao_lu, da_noi_dau
        if giu_chu is None:  # review C M-1: đã có dự báo / khung lịch (B171 T3) ⇒ giữ chữ chừng nào còn có thể là câu từ chối
            giu_chu = "" if ((flags.thoi_tiet and trace.thoi_tiet and trace.thoi_tiet["khoi"]) or trace.lich is not None
                             or trace.nhieu_y or _can_dau_bao_lu(trace) or trace.lam_thay is not None) else False
            dau_bao_lu = _can_dau_bao_lu(trace)  # giữ chữ tới khi biết không phải câu từ chối rồi mới đặt câu đầu
        if giu_chu is not False:
            giu_chu += text
            if (INSUFFICIENT_ANSWER.startswith(giu_chu.lstrip()) or (trace.nhieu_y and _con_la_y_thieu(giu_chu))
                    # câu nhờ làm thay: câu khuôn kèm khoảng trắng cuối vẫn phải giữ — bước sau so bằng `strip()` rồi thay cả câu
                    or (trace.lam_thay is not None and INSUFFICIENT_ANSWER.startswith(giu_chu.strip()))):
                return None
            text, giu_chu = giu_chu, False
            if dau_bao_lu:
                text, dau_bao_lu = f"{tt.CAU_DAU_BAO_LU}\n\n{text}", False
        if trace.lich is not None and not da_noi_dau:
            da_noi_dau = True
            text = f"{lt.dong_minh_hieu(trace.lich['khung'])}\n\n{text}"
        return text

    # Việc nhỏ (12) 08/11 — review streaming 31/10 m-1: huỷ theo "luồng model còn sống" thay vì liệt kê lỗi. Mọi cách rời vòng đọc khi luồng chưa
    # hết (hết giờ, người dùng ngắt, lỗi trong code của mình) ⇒ `cancel()`; luồng tự hết hoặc chính luồng báo lỗi (lần chạy đã dừng) ⇒ không.
    stream_live = False
    try:
        if not trace.bieu_mau:  # D3: lượt biểu mẫu không định tuyến
            if flags.router and generator is not None:
                yield "status", {"stage": "routing"}
            await _pick_route(query, generator, trace, flags)
            if trace.fixed_outcome is not None:
                yield "delta", trace.answer
                return
        if trace.bieu_mau:
            # D3: code xếp ngay (bước tiến độ như đường công cụ — D14) rồi một lần sinh không công cụ; phần sau vòng đọc dùng chung
            # (giữ chữ khi còn có thể là câu từ chối, dòng "Mình hiểu", kiểm cuối, khối ghi chú)
            if generator is None:
                raise GeneratorNotReadyError("generator is not ready")
            if flags.len_ke_hoach_v2:  # bản 2: sự kiện lich_khung / lich_cau / lich_xong (`llm/len_ke_hoach.py`); cờ tắt ⇒ y như cũ
                from llm import len_ke_hoach
                async for event in len_ke_hoach.stream_v2(query, retrieval_service, context_builder, generator, trace, flags, _today(flags, trace)):
                    yield event
                set_notice(trace, flags)
                return
            yield "status", {"stage": "lich_trinh", "buoc": "dang_xep"}
            today = _today(flags, trace)
            context = await _xep_bieu_mau(query, retrieval_service, context_builder, trace, flags, today)
            for buoc in trace.buoc_lich:
                yield "status", {"stage": "lich_trinh", **buoc}
            yield "status", {"stage": "generating"}
            call_route = ROUTE_TRO_LY_HUE
            result, call_log = generator.start_answer_stream(query, context, today, bieu_mau=True, **_history_kwargs(trace))
        elif trace.route == ROUTE_TRO_CHUYEN:
            yield "status", {"stage": "generating"}
            call_route = ROUTE_TRO_CHUYEN
            result, call_log = generator.start_chat_stream(query, **_history_kwargs(trace))
        else:
            today = _today(flags, trace)
            tool_prompt = await _before_model(query, retrieval_service, context_builder, generator, trace, recorder, today, flags)
            if trace.packed is not None:  # V2 không tìm trước (B2 D5): `searching` / `searched` đến từ lần gọi công cụ
                yield "status", {"stage": "searched", "n_sources": len(trace.packed.sources), "bai": bai_da_tim(trace)}
            if trace.fixed_outcome is not None:  # ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
                yield "delta", trace.answer
                async for event in _web_stream(query, generator, trace, flags, tim_web):  # B6: đúng ca "kho không có"
                    yield event
                return
            call_route = ROUTE_TRO_LY_HUE
            if flags.uses_tools:
                # B3 D9 (b): vòng công cụ ⇒ "đang viết" phát ngay trước chữ đầu (không trước các lượt `tim_kho`)
                pending_generating = True
                instructions = _assistant_instructions(generator, trace, trace.nhieu_y, flags.kiem_du_bang_chung)
                tool_fn = tool_for_turn(query, retrieval_service, context_builder, trace, today, instructions, flags.so_lan_tim_kho,
                                    tach_cau_tim=flags.tach_cau_tim_model, **_the_noi_kwargs(trace, flags, query))
                extra = _lich_extra(query, retrieval_service, context_builder, trace, today, instructions, flags)
                result, call_log, tool_state = generator.start_tools_stream(tool_prompt, tool_fn, **_history_kwargs(trace), **extra)
                if flags.giu_chu_toi_kiem and getattr(generator, "chu_ve_mot_lan", False):
                    cho_kiem = ""
            else:
                yield "status", {"stage": "generating"}
                stream_kwargs = {"kiem_du_bang_chung": True} if flags.kiem_du_bang_chung else {}
                result, call_log = generator.start_answer_stream(query, trace.packed.text, trace.today, **_history_kwargs(trace), **stream_kwargs)

        started, generator_started = time.perf_counter(), time.monotonic()
        extractor = AnswerTextStream()
        events = result.stream_events()
        stream_live = True
        deadline = asyncio.get_running_loop().time() + generator.timeout
        try:
            while True:
                try:
                    async with asyncio.timeout_at(deadline):
                        event = await anext(events)
                except StopAsyncIteration:
                    stream_live = False
                    break
                except TimeoutError:
                    raise
                except Exception:
                    stream_live = False  # lỗi của chính luồng (SDK / provider): lần chạy đã dừng, đọc nốt sẽ ném lại lỗi đó
                    raise
                if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
                    text = extractor.feed(event.data.delta)
                    if text:
                        if pending_generating:
                            pending_generating = False
                            yield "status", {"stage": "generating"}
                        if cho_kiem is not None:  # công tắc `giu_chu_toi_kiem`: gom, phát sau phép kiểm nguồn (cuối hàm)
                            cho_kiem += text
                            continue
                        text = chu_phat(text)
                        if text is not None:
                            yield "delta", text
                elif event.type == "run_item_stream_event" and event.name == "tool_called":  # thẻ công cụ (B2 D7): lượt gọi không có chữ
                    cong_cu = getattr(getattr(event.item, "raw_item", None), "name", None)
                    if cong_cu == "lich_trinh":  # D14: "đang xếp lịch…" khi code bắt đầu chạy — không phát "đang tìm" (m-6)
                        yield "status", {"stage": "lich_trinh", "buoc": "dang_xep"}
                    elif cong_cu == "thoi_tiet":  # B5b: "đang xem dự báo…" (không phải "đang tìm kho")
                        yield "status", {"stage": "thoi_tiet"}
                    elif cong_cu in ("khoang_cach", "gan_diem", "so_sanh_diem_den", "ngay_lich", "liet_ke_bai"):
                        yield "status", {"stage": cong_cu}
                    elif cong_cu == "goi_y_phuong_an_mua_nang":
                        yield "status", {"stage": "goi_y_mua_nang"}
                    elif cong_cu == "tinh_ve_va_gio_tham_quan":
                        yield "status", {"stage": "tinh_ve"}
                    elif cong_cu == "goi_y_luu_tru":
                        yield "status", {"stage": "goi_y_luu_tru"}
                    else:
                        yield "status", {"stage": "searching"}
                elif event.type == "run_item_stream_event" and event.name == "tool_output":
                    if cong_cu == "lich_trinh":  # D14 (b): phát các bước code vừa làm xong, đúng thứ tự
                        for buoc in trace.buoc_lich[da_phat_buoc:]:
                            yield "status", {"stage": "lich_trinh", **buoc}
                        da_phat_buoc = len(trace.buoc_lich)
                    elif cong_cu not in (
                        "thoi_tiet", "ngay_lich", "khoang_cach", "gan_diem",
                        "goi_y_phuong_an_mua_nang", "so_sanh_diem_den",
                        "tinh_ve_va_gio_tham_quan", "goi_y_luu_tru", "liet_ke_bai",
                    ):  # B5b / T1 / Đợt 2 / Đợt 6: không phải "đã tìm kho"
                        yield "status", {"stage": "searched", "n_sources": len(trace.so_nguon), "bai": bai_da_tim(trace)}
        except Exception as exc:
            if trace.tool_error is not None:  # lỗi tìm trong công cụ: SDK có thể bọc lại ⇒ ném đúng lỗi gốc (route ra câu lỗi như B1)
                raise trace.tool_error from None
            # hết lượt tìm (cờ `het_luot_bo_cong_cu`): model vẫn xin `tim_kho` đã ẩn ⇒ không phải lỗi 500 — câu từ chối cố định như chạm `max_turns`
            if tool_state is None or not generator.xin_cong_cu_da_an(exc, tool_state):
                raise
        finally:
            trace.generation_ms = elapsed_ms(started)

        trace.generated = generator.finish_answer_stream(result, call_log, generator_started, tool_state)
        if call_route == ROUTE_TRO_CHUYEN:
            trace.answer, trace.cited = trace.generated.text, ()
        else:
            _finish_generated(trace, flags, query)
            da_phat_viet_lai = False
            if tool_state is not None and await _cuu_max_turns(query, generator, trace, flags, today, call_log):
                giu_chu = False
                cho_kiem = None
                if pending_generating:
                    pending_generating = False
                    yield "status", {"stage": "generating"}
                yield "delta", trace.answer.removesuffix(f"\n\n{trace.thoi_tiet_noi}") if trace.thoi_tiet_noi else trace.answer
                da_phat_viet_lai = True
            if tool_state is not None and await _viet_lai_het_luot(query, generator, trace, flags, today, call_log):
                # chữ giữ chỗ của lần đầu đã hiện (hoặc đang bị giữ) ⇒ thay bằng chữ của lần viết lại; khối dự báo code nối vẫn phát riêng ở dưới.
                # Công tắc `giu_chu_toi_kiem` đang gom ⇒ chữ giữ chỗ chưa hề hiện ⇒ bản viết lại là chữ đầu tiên, phát như một mảnh thường
                giu_chu = False
                if trace.citation_error is None:  # soát khác hãng 22/11 (A2): bản viết lại còn lỗi kiểm (mã nguồn lạ) ⇒ không phát, route báo lỗi như thường
                    yield "thay_chu" if cho_kiem is None else "delta", trace.answer.removesuffix(f"\n\n{trace.thoi_tiet_noi}") if trace.thoi_tiet_noi else trace.answer
                    da_phat_viet_lai = True
                cho_kiem = None
            if tool_state is not None and await _viet_lai_trich_dan_cau(query, generator, trace, flags, today, call_log):
                giu_chu = False
                if cho_kiem is None:
                    if pending_generating:
                        pending_generating = False
                        yield "status", {"stage": "generating"}
                    yield "thay_chu", trace.answer.removesuffix(f"\n\n{trace.thoi_tiet_noi}") if trace.thoi_tiet_noi else trace.answer
                    da_phat_viet_lai = True
            if trace.fixed_outcome is not None:  # chạm `max_turns`: không có chữ model nào ⇒ câu từ chối thành một `delta` (B2 D5)
                # soát khác hãng 22/11 (Neon #1, Carbon 4.2.3): bản viết lại là câu từ chối khuôn ở câu nhờ làm thay ⇒ `_finish_generated` trong lưới viết
                # lại đã đổi thành câu nói thật (kết thúc cố định `lam_thay`) và nhánh trên VỪA phát nó ⇒ không phát lần hai
                if trace.answer and not da_phat_viet_lai:  # lượt hỏi lại: không chữ ⇒ route gửi `clarify`
                    yield "delta", trace.answer
                return
            if (cho_kiem or (cho_kiem is not None and (trace.vet.get("p1_xoa_luu_tru") or trace.vet.get("cit_cau_viet_lai")))) and trace.citation_error is None:  # chữ đã gom qua phép kiểm ⇒ phát bằng đúng đường của một mảnh chữ; bị rút ⇒ không phát
                # soát khác hãng 22/11 (A1): phép kiểm số đã gỡ câu có số lạ ⇒ phát chữ ĐÃ gỡ (chữ model của `trace.answer`), không phát chữ gốc đã gom
                thay = trace.kiem_so_go is not None or bool(trace.vet.get("p1_xoa_luu_tru")) or bool(trace.vet.get("cit_cau_viet_lai"))
                text = chu_phat(chu_cua_model(trace) if thay else cho_kiem)
                if text is not None:
                    yield "delta", text
            if giu_chu:  # chữ giữ lại đến hết = câu từ chối (đã thay) hoặc một khúc đầu của nó
                yield "delta", _chu_giu_lai(trace, giu_chu, da_noi_dau)
            if trace.lich is not None and trace.citation_error is None and trace.lich["ghi_chu"]:
                yield "delta", f"\n\n{trace.lich['ghi_chu']}"  # D4b: khối ghi chú do code nối, sau phần model
            if trace.thoi_tiet_noi and trace.citation_error is None:
                yield "delta", f"\n\n{trace.thoi_tiet_noi}"  # B5b: khối số liệu / câu cố định do code nối, sau phần model
            set_notice(trace, flags)
            async for event in _web_stream(query, generator, trace, flags, tim_web):
                yield event
    finally:
        if call_log is not None:
            record_llm_calls(trace, call_log.calls, call_route)
        if result is not None and stream_live:
            # dừng lần gọi model rồi đọc nốt bằng iterator mới, trong vùng che có hạn giờ (spec streaming §4.5). Không dựa `result.is_complete`.
            result.cancel()
            drain_started = time.perf_counter()
            with anyio.CancelScope(shield=True):
                with anyio.move_on_after(STREAM_DRAIN_SECONDS) as drain_scope:
                    async for _ in result.stream_events():
                        pass
            logger.info("chat_stream_drain %s", json.dumps({"finished": not drain_scope.cancelled_caught,
                                                             "ms": elapsed_ms(drain_started)}))


def _chu_giu_lai(trace: AnswerTrace, giu: str, da_noi_dau: bool) -> str:
    """Stream: chữ model giữ lại tới hết ⇒ chữ phát ra — lời lịch code dựng (B171 T3) / câu dẫn dự báo (B5b M-1) / chính chữ đó; lượt có lịch
    chưa phát chữ nào ⇒ dòng "Mình hiểu" đi trước (D12 (a))."""
    if trace.lich is not None and trace.lich.get("chu_thay"):
        chu = trace.lich["chu_thay"]
    elif trace.thoi_tiet and trace.thoi_tiet.get("thay_tu_choi"):
        chu = tt.CAU_DAN_BAO_LU if trace.thoi_tiet.get("bao_lu") else tt.CAU_DAN_DU_BAO
    elif trace.chi_y_thieu:  # chốt (a) vòng 2: chữ giữ lại chỉ gồm dòng ý thiếu ⇒ câu từ chối chuẩn
        chu = INSUFFICIENT_ANSWER
    else:
        chu = giu
    return f"{lt.dong_minh_hieu(trace.lich['khung'])}\n\n{chu}" if trace.lich is not None and not da_noi_dau else chu


_SPEC_END = object()  # dấu hết hàng đợi của phần chạy trước (#6)
# Trường của trace do route đặt **trước** khi gọi lõi (chat.py `_start_conversation`, `_model_query`) — phần chạy trước phải nhận đủ (B161 M-1)
ROUTE_INPUTS = ("history", "truong", "search_query", "bao_lu_lan_dau")


TEN_CHAY_LAI = "chay_lai_khong_dap"  # tên mục `trace.tools` của lượt đã chạy lại (sổ số đo: chỉ tên + đầu lời lỗi của lần đầu do code đặt, không chữ)


async def answer_turn_stream_parallel(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                                      recorder=None, tim_web=None):
    """Đường stream của một lượt (`_luot_stream`) + MỘT lần chạy lại hẹp cho cờ `nho_cau_tra_loi` (22/11/2026).
    Vì sao: lịch sử mang câu trả lời liền trước ⇒ với tin kiểu "sửa lại thứ bạn vừa viết" model chép lại lời cũ của nó mà không trích nguồn nào ⇒ bộ kiểm
    trích dẫn rút cả câu ⇒ người dùng thấy màn hình lỗi (lượt đo 22/11: 3 / 7 lần; cờ tắt thì là câu từ chối). Sàn "lịch sử không làm nguồn" vẫn giữ —
    thứ sửa ở đây chỉ là đoạn kết: lượt bị rút mà lịch sử ĐANG mang câu trả lời (`trace.lich_su_khong_dap` có) ⇒ gỡ chữ đã hiện (`thay_chu` rỗng), chạy lại
    cả lượt với lịch sử như khi cờ tắt, lấy kết quả lần hai làm kết quả của lượt — tệ nhất là y như bên cờ tắt. Lần hai cũng bị rút ⇒ lỗi như cũ (không
    lặp). Không chạy lại: lượt không mang câu trả lời nhớ, lượt không bị rút, câu cố định, lượt SỬA lịch; cuộc có lịch đã lưu thì chỉ chạy lại câu hỏi thường khi cờ `nho_dap_cuoc_co_lich` bật (lần hai đi thẳng đường thường — xem dưới), cờ tắt ⇒ không chạy lại như trước."""
    khong_dap = trace.lich_su_khong_dap  # đọc TRƯỚC khi chạy: bước gộp trace phụ của đường song song ghi đè mọi trường không phải đầu vào của route
    async for event in _luot_stream(query, retrieval_service, context_builder, generator, trace, flags, recorder, tim_web):
        yield event
    if khong_dap is None or trace.citation_error is None or trace.fixed_outcome is not None:
        return
    co_lich = trace.lich_luu is not None
    # Cuộc có lịch đã lưu: chỉ chạy lại khi cờ `nho_dap_cuoc_co_lich` bật và lần đầu KHÔNG phải lượt sửa lịch (không bấm thẻ chọn, bước hiểu ý không ra
    # hành động nào) — lượt sửa có chữ do code dựng, không thuộc bản chạy lại này.
    if co_lich and not (flags.nho_dap_cuoc_co_lich and trace.sua_chon is None and not (trace.sua or {}).get("n_hanh_dong")):
        return
    lai = AnswerTrace(**{name: getattr(trace, name) for name in ROUTE_INPUTS})
    lai.history = khong_dap
    if co_lich and flags.lich_vao_hoi_thuong:  # lần hai vẫn thấy lịch đã lưu như đường thường của cuộc đó (`_sua_song_song`)
        lai.lich_luu = trace.lich_luu
    # Cuộc có lịch: lần hai đi THẲNG đường trả lời thường — KHÔNG gọi lại bước hiểu ý sửa lịch (lần đầu đã kết luận đây không phải câu sửa; gọi lại là
    # có thể hiểu / áp một lệnh sửa lần hai). Cuộc không có lịch: như cũ.
    chay_lai = _answer_core if co_lich else _luot_stream
    giu_cua_luot = ("sua", "lich_luu", "sua_chon") if co_lich else ()  # phần của bước hiểu ý lần đầu + lịch của cuộc: trace chính giữ (như `_sua_song_song`)
    vet_sua = trace.vet.get("sua") if co_lich else None
    ctx_lan_dau = trace.thoi_tiet_ctx if (trace.thoi_tiet_ctx or {}).get("bao_lu_model") else None  # lần đầu model đã tự gọi công cụ loại bão / lũ
    lai.bao_lu_lan_dau = ctx_lan_dau is not None  # dấu đi VÀO lần hai: lưới cuối và cổng web của lần hai coi đây là lượt bão / lũ dù model không gọi lại
    goi_lan_dau, loi_lan_dau = list(trace.llm_calls), str(trace.citation_error).split(":", 1)[0]
    yield "thay_chu", ""  # chữ chưa trích nguồn của lần đầu đã hiện ⇒ gỡ ngay, người dùng thấy lại các dòng tiến độ
    try:
        async for event in chay_lai(query, retrieval_service, context_builder, generator, lai, flags, recorder, tim_web):
            yield event
    finally:  # kể cả khi người dùng ngắt giữa lần hai: trace của lượt nhận mọi thứ lần hai đã làm; tiền = cả hai lần
        for item in dataclasses.fields(AnswerTrace):
            if item.name not in (*ROUTE_INPUTS, "lich_su_khong_dap", *giu_cua_luot):
                setattr(trace, item.name, getattr(lai, item.name))
        if vet_sua is not None:  # sổ vết: giữ phần hiểu ý sửa lịch của lần đầu
            trace.vet = {**trace.vet, "sua": vet_sua}
        if ctx_lan_dau is not None:
            # Soát khác hãng 22/11: tín hiệu an toàn model đã thấy ở lần đầu phải sống hết lượt — lần hai không gọi công cụ đó rồi cũng lỗi thì lời báo
            # lỗi (`loi_bao_luoi_cuoi`) vẫn phải có câu bản tin chính thức + 112. Khoá của lần hai thắng; chỉ `bao_lu_model` được giữ từ lần đầu.
            trace.thoi_tiet_ctx = {**ctx_lan_dau, **(trace.thoi_tiet_ctx or {}), "bao_lu_model": True}
        trace.llm_calls = goi_lan_dau + list(lai.llm_calls)
        trace.tools = [*trace.tools, {"name": TEN_CHAY_LAI, "ms": 0.0, "loi_lan_dau": loi_lan_dau}]


async def _luot_stream(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                       recorder=None, tim_web=None):
    """Thí nghiệm tốc độ #6 (plan `2026-11-04-phase-9-toc-do-song-song-plan.md`). Cờ `song_song_tra_loi` tắt (hoặc định tuyến không chạy /
    câu tìm do định tuyến viết) ⇒ đúng `answer_turn_stream`. Bật ⇒ (i) định tuyến và (ii) phần của tuyến `tro_ly_hue`
    chạy cùng lúc. (ii) chính là `answer_turn_stream` với `router` tắt trên **trace phụ** (đi thẳng lần tìm đầu câu gốc + lần gọi trợ lý —
    đầu vào hai lần gọi model không phụ thuộc tuyến). Sự kiện của (ii) giữ trong hàng đợi tới khi có tuyến:
    `tro_ly_hue` ⇒ xả hàng đợi, gộp trace phụ vào trace chính (D1); tuyến khác ⇒ huỷ (ii), bỏ trace phụ, đi đường của tuyến đó (D2, D3).
    B6: (ii) **không** tra web (chưa biết tuyến — câu trò chuyện không được ra Serper); cổng web chạy trên trace chính **sau khi gộp**."""
    if flags.sua_lich_v2 and trace.lich_luu is not None and not trace.bieu_mau and generator is not None:
        async for event in _sua_song_song(query, retrieval_service, context_builder, generator, trace, flags, recorder, tim_web):
            yield event
        return
    async for event in _answer_core(query, retrieval_service, context_builder, generator, trace, flags, recorder, tim_web):
        yield event


async def _sua_song_song(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                         recorder=None, tim_web=None):
    """Sửa lịch bản 2 — cuộc có lịch đã lưu. Lần "hiểu ý" + định tuyến chạy SONG SONG với CẢ đường trả lời thường (đo 14/11: chờ hiểu ý trước
    làm chữ đầu câu thường +1,9 s, phạm sàn p50 ≤ 3 s). Sự kiện của đường thường giữ trong hàng đợi tới khi biết kết quả:
    câu sửa (không khẩn cấp) ⇒ huỷ đường thường (tiền phần bị huỷ ghi vào `llm_calls` + `usd_bo`), phát lượt sửa; còn lại ⇒ xả hàng đợi, gộp
    trace phụ. Khẩn cấp thắng (review E B-1). Lượt bấm nút thẻ chọn ⇒ không chạy đường thường."""
    from llm import len_ke_hoach  # import muộn: module đó import lõi này
    if trace.sua_chon is not None:
        kq = await len_ke_hoach.hieu_va_ap(query, generator, trace, flags)
        yield "status", {"stage": "sua_lich"}
        async for event in len_ke_hoach.stream_sua(query, retrieval_service, context_builder, generator, trace, flags, kq):
            yield event
        set_notice(trace, flags)  # như lượt biểu mẫu bản 2: lịch sau khi sửa vẫn trích bài điểm đến ⇒ giữ dòng "có thể đã thay đổi"
        return
    phu = AnswerTrace(**{k: getattr(trace, k) for k in ROUTE_INPUTS})
    if flags.lich_vao_hoi_thuong:  # đường thường của cuộc có lịch thấy lịch (tầng 1 / 2 — tầng 2 ở `_answer_core`)
        phu.lich_luu = trace.lich_luu
    hang: asyncio.Queue = asyncio.Queue()
    da_quyet = asyncio.Event()

    async def tim_web_cho(cau: str):
        """Review E m-1: tra web của đường thường CHỜ biết không phải lượt sửa — lượt sửa huỷ đường thường trong lúc chờ ⇒ chữ người dùng
        không ra Serper ở lượt sửa."""
        await da_quyet.wait()
        return await tim_web(cau)

    async def chay_thuong() -> None:
        try:
            async for event in _answer_core(query, retrieval_service, context_builder, generator, phu, flags, recorder,
                                            tim_web_cho if tim_web is not None else None):
                hang.put_nowait(("su_kien", event))
            hang.put_nowait(("xong", None))
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # lỗi của đường thường đi ra đúng chỗ người đọc hàng đợi (nếu đó không phải lượt sửa)
            hang.put_nowait(("loi", exc))

    viec = asyncio.create_task(chay_thuong())

    async def huy() -> None:
        if not viec.done():
            viec.cancel()
        await asyncio.gather(viec, return_exceptions=True)

    async def cho_dinh_tuyen() -> None:
        """Khẩn cấp lấy từ CHÍNH lần định tuyến của đường thường (trace phụ) — không gọi định tuyến lần hai (đo 14/11: lần thứ hai
        +0,0001 USD / câu). `_pick_route` ghi `routing_ms` ở `finally` ⇒ chờ mốc đó (hoặc đường thường xong / lỗi)."""
        while flags.router and phu.routing_ms is None and not viec.done():
            await asyncio.sleep(0.03)

    try:
        kq, _ = await asyncio.gather(len_ke_hoach.hieu_va_ap(query, generator, trace, flags), cho_dinh_tuyen())
    except BaseException:
        await huy()
        raise
    khan_cap = phu.emergency_by == "router"
    if kq is not None and not khan_cap:  # lượt sửa ⇒ bỏ phần đường thường đã chạy
        await huy()
        trace.llm_calls += phu.llm_calls
        trace.usd_bo = round(sum(c.get("usd") or 0 for c in phu.llm_calls), 6) or None
        yield "status", {"stage": "sua_lich"}  # review E m-1: chỉ hiện khi đúng là lượt sửa
        async for event in len_ke_hoach.stream_sua(query, retrieval_service, context_builder, generator, trace, flags, kq):
            yield event
        _giu_dau_bao_lu(trace, phu)
        set_notice(trace, flags)
        return
    da_quyet.set()  # không phải lượt sửa ⇒ đường thường được tra web (nếu cổng mở)
    sua, goi_truoc = trace.sua, list(trace.llm_calls)
    try:
        while True:
            loai, x = await hang.get()
            if loai == "xong":
                break
            if loai == "loi":
                raise x
            yield x
    finally:
        await huy()
        for item in dataclasses.fields(AnswerTrace):  # trace chính nhận mọi thứ đường thường đã làm; giữ phần của lượt sửa
            if item.name not in ("llm_calls", "sua", "lich_luu", "sua_chon", "vet"):
                setattr(trace, item.name, getattr(phu, item.name))
        trace.vet = {**phu.vet, **trace.vet}  # sổ vết: giữ `vet["sua"]` của lần hiểu ý (ghi trên trace chính) — đúng lượt "câu sửa bị coi là câu thường"
        trace.llm_calls = goi_truoc + phu.llm_calls
        trace.sua = {**(sua or {}), "khan_cap": khan_cap} if sua is not None or khan_cap else None


async def _answer_core(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                       recorder=None, tim_web=None):
    """Thân của `answer_turn_stream_parallel` (đường trả lời thường, có / không chạy song song định tuyến — #6)."""
    if trace.bieu_mau or not (flags.song_song_tra_loi and flags.router and generator is not None and flags.lan_tim_dau == "v0"):
        # lượt biểu mẫu (cổng D3): không định tuyến ⇒ không có gì để chạy song song
        async for event in answer_turn_stream(query, retrieval_service, context_builder, generator, trace, flags, recorder, tim_web):
            yield event
        return

    # B6: bản cờ của phần chạy song song / đường trò chuyện tắt cả `tra_web` (cờ này cần `router`; cổng web chạy bằng `flags` gốc sau khi gộp)
    without_router = dataclasses.replace(flags, router=False, tra_web=False)
    # B161 M-1: trace phụ mang **mọi đầu vào route đặt trước khi gọi lõi** (lịch sử B3; giá trị nút + câu gốc của lượt ghép B4b / B5) — chép
    # từng trường (không `dataclasses.replace`: sẽ dùng chung list sổ nguồn / công cụ giữa hai trace)
    spec = AnswerTrace(**{name: getattr(trace, name) for name in ROUTE_INPUTS})
    if flags.lich_vao_hoi_thuong:  # tầng 2 / 2: `_before_model` (nơi nối nguồn lịch) chạy trên `spec`, không phải trên trace gọi vào
        spec.lich_luu = trace.lich_luu
    queue: asyncio.Queue = asyncio.Queue()

    async def run_spec() -> None:
        try:
            async for event in answer_turn_stream(query, retrieval_service, context_builder, generator, spec, without_router):
                queue.put_nowait(event)
        finally:
            queue.put_nowait(_SPEC_END)

    yield "status", {"stage": "routing"}
    task = asyncio.create_task(run_spec())
    keep = merged = False
    finished_before_route = False
    try:
        await _pick_route(query, generator, trace, flags)
        keep = trace.route == ROUTE_TRO_LY_HUE and trace.fixed_outcome is None
        if keep:
            while (event := await queue.get()) is not _SPEC_END:
                yield event
            await task  # lỗi của (ii) đi ra nguyên kiểu như đường cũ
            _merge_spec(trace, spec, recorder)
            merged = True
            async for event in _web_stream(query, generator, trace, flags, tim_web):  # B6: sau khi gộp (tuyến đã chắc là `tro_ly_hue`)
                yield event
            return
        finished_before_route = task.done()
        task.cancel()  # huỷ ngay: lần gọi bị bỏ không giữ chữ đầu của tuyến khác (sàn KC)
        if trace.fixed_outcome is not None:
            yield "delta", trace.answer
            return
        # `tro_chuyen`: định tuyến đã xong ⇒ đường cũ của tuyến này, không định tuyến lại
        async for event in answer_turn_stream(query, retrieval_service, context_builder, generator, trace, without_router, recorder, tim_web):
            yield event
    finally:
        if not task.done():
            task.cancel()
        # Việc nhỏ (7) 08/11: người dùng ngắt ⇒ Starlette huỷ kiểu anyio (mọi lần chờ trong vùng bị huỷ lại) ⇒ không che thì `gather` bị huỷ, bỏ qua
        # bước gộp dưới ⇒ `chat_metrics` mất `llm_calls` / USD của (ii) (tái tạo: `data/phase_11/viec_nho_e/do_dung_song_song.py`).
        with anyio.CancelScope(shield=True):
            await asyncio.gather(task, return_exceptions=True)  # (ii) tự ghi `llm_calls` + đọc nốt trong `finally` của nó; lỗi của (ii) bị bỏ (D3)
        if keep and not merged:  # lỗi / ngắt trước khi gộp xong ⇒ gộp ở đây như trước B6
            _merge_spec(trace, spec, recorder)
        elif not keep:
            usd = sum(call["usd"] for call in spec.llm_calls)
            trace.n_tra_loi_bo, trace.bo_huy_giua = 1, not finished_before_route
            if trace.bo_huy_giua and spec.generation_ms is not None and spec.packed is not None:
                usd += cost_usd(spec.packed.input_tokens, 0, provider=getattr(generator, "provider", "openai"))  # lần gọi bị huỷ không có usage ⇒ cận dưới (plan D2)
            trace.usd_bo = usd


def _merge_spec(trace: AnswerTrace, spec: AnswerTrace, recorder) -> None:
    """Tuyến `tro_ly_hue` ⇒ trace chính nhận mọi thứ (ii) đã làm; giữ phần định tuyến của trace chính; `llm_calls` = định tuyến rồi trả lời."""
    keep_own = {"route", "route_error", "routing_ms", "emergency_by", "llm_calls", "sua", *ROUTE_INPUTS}  # `sua`: số đếm lần hiểu ý sửa lịch
    vet_rieng = trace.vet
    for item in dataclasses.fields(AnswerTrace):
        if item.name not in keep_own:
            setattr(trace, item.name, getattr(spec, item.name))
    trace.vet = {**spec.vet, **vet_rieng}
    if "tim" in spec.vet and "tim" in vet_rieng:  # hai nhánh đều có lần tìm ⇒ nối, không ghi đè (review B m-1)
        trace.vet["tim"] = vet_rieng["tim"] + spec.vet["tim"]
    trace.llm_calls = trace.llm_calls + spec.llm_calls
    if recorder and trace.packed is not None:  # như `prepare_answer` của đường cũ (recorder chỉ route truyền)
        recorder.record_packed_context(trace.packed)
        # câu nói thật thay cho câu từ chối do ngữ cảnh rỗng vẫn là "từ chối trước model" — đếm như đường không song song (review B m2)
        if trace.fixed_outcome == "refusal_no_sources" or (trace.fixed_outcome == "lam_thay" and not trace.packed.sources):
            recorder.record_fallback()
