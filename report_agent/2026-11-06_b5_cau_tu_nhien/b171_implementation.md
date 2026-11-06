# Implementation Report: Phase 9 B5 — B171 sửa 2 loại lỗi lịch trình bằng code (L-a, L-b)

Người làm: B (Claude Code, Opus 5.5)
Date: 11:22 06/11/2026 (`date`)
Canonical guide: plan B5 `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 (D2, D2b, D4, D4b, D8); việc B171 trong `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN 06/11".

## 1. Phạm vi

A giao (06/11): sửa bằng **code** hai loại lỗi mà 2 agent chấm thấy trên bộ kín B5 (A mô tả ở mức loại; B **không** đọc `data/phase_9/b5/kin/`, `data/phase_9/b5_v2/`, `bo_do_b5/cau_sealed.jsonl`):
- **L-a:** điểm lấp ngoài sở thích dù bảng còn điểm hợp sở thích (trái điều kiện lấp D2, có dính luật cụm kề) + câu lý do do code nối không đúng sự thật.
- **L-b:** người dùng xin một buổi (vd buổi tối) mà luật code không xếp (vd đi cùng trẻ nhỏ) ⇒ code nối câu "không xếp … vì …"; kiểm cuối bắt lời model nói ngược khung.
- Ghi nhận, không sửa: "đi dày" ít tác dụng vì bảng điểm thiếu thời lượng.

Nhánh **`p9-b5-sua`** từ `main` `0a9e0f3`, commit **`d5028d4`** (đã push). Cờ `lich_trinh` vẫn **tắt**. Lượt có phí chỉ trên bộ đã thấy + 4 câu B tự viết.

## 2. Thay đổi chính (`backend/llm/lich_trinh.py`, 1 dòng `assistant.py`, test)

**L-a — nguyên nhân (tái tạo 0 USD, `data/phase_9/b171/tools/tai_tao_la.py`):** `xep` chọn điểm buổi sáng theo thứ tự bảng, không nhìn buổi chiều. Ví dụ sở thích thiên nhiên 2 ngày: sáng ngày 2 chọn một điểm mà mọi điểm thiên nhiên còn lại đều không cùng cụm / cụm kề ⇒ chiều lấp một lăng (di tích). Trong khi đó một cụm khác có ba điểm thiên nhiên chưa dùng. Quét 120 tổ hợp (4 số ngày × 3 người đi cùng × 2 kiểu đi × 5 sở thích): **18 ca** lấp khi số điểm hợp sở thích đi được ban ngày ≥ số suất sáng + chiều, tất cả ở sở thích thiên nhiên. Câu "Kho chỉ có k điểm hợp sở thích…" lấy k = **mọi** điểm hợp sở thích (kể cả phố đêm chỉ đi được buổi tối) ⇒ có ca k ≥ số suất mà vẫn nói "chỉ có".
- **Sửa 1 (`chon_sang`):** buổi sáng ưu tiên điểm hợp sở thích **còn bạn đi buổi chiều**, tức còn một điểm hợp sở thích khác cùng cụm / cụm kề; không có thì chọn như cũ. **Điểm người dùng nêu vẫn đứng trước** (lượt sửa đầu làm rơi Bạch Mã / Thác Nhị Hồ người dùng nêu — test cũ bắt được, đã sửa).
- **Sửa 2 (câu lý do đúng sự thật):** k = số điểm hợp sở thích **đi được buổi sáng / chiều**. Có hai câu cố định, chọn theo `lap_vi` (trường mới của khung):
  - `it_diem` (k < số suất): "Kho chỉ có k điểm hợp sở thích của bạn **đi được buổi sáng / chiều** nên mình thêm điểm di tích tiêu biểu: …".
  - `khong_cung_huong` (k ≥ số suất nhưng vẫn phải lấp): "Các điểm hợp sở thích còn lại của bạn không cùng hướng với lịch trong ngày nên mình thêm điểm di tích tiêu biểu: …".
- **Kết quả:** quét 120 tổ hợp: **18 ⇒ 6 ca**. 6 ca còn lại đều là "thiên nhiên 4 ngày": 8 điểm cho 8 suất, nhưng hai cụm có số điểm lẻ lại không kề nhau ⇒ **không thể** xếp đủ (chứng minh bằng đếm cụm, report trước §2). Lịch dùng 7 / 8 điểm, câu lý do là `khong_cung_huong`. So bản cũ ↔ mới trên **1.728** tổ hợp, kể cả 6 mẫu `them_diem` (`data/phase_9/b171/tools/so_khung_cu_moi.py`): **168 ca đổi, đều là sở thích thiên nhiên.** Lấp 1 ⇒ 0: 108 ca; 2 ⇒ 1: 36 ca; 1 ⇒ 1 (đổi chỗ): 24 ca. Không ca nào bỏ thêm điểm người dùng nêu, không ca nào ít điểm hơn; `kiem_khung` = 0 lỗi ở cả 1.728 ca.
- **Lệch nhỏ so với chữ D2 (B tự quyết, A xem):** D2 viết "không đủ điểm hợp sở thích ⇒ lấp". Ở 6 ca không thể xếp đủ, B **vẫn lấp có nhãn** với câu "không cùng hướng" thay vì để trống một buổi. Lý do: buổi trống không có câu giải thích còn tệ hơn với du khách. Muốn để trống thì đổi một nhánh.

**L-b:**
- `hoi_buoi_toi(cau)`: bộ dò câu xin buổi tối (code dò trên câu người dùng, như `do_so_ngay`). Mẫu: "buổi tối", "tối đi / ăn / chơi / có / thì…", "ăn tối", "chiều và tối", "ban đêm", "về đêm", "phố / chợ đêm". Không khớp: "N ngày N đêm", "tối đa / ưu / thiểu". Bộ dò cố ý rộng: nhận nhầm chỉ thêm một câu **đúng sự thật**, và chỉ khi khung không có buổi tối. `ThamSo.hoi_toi` + `tham_so.hoi_toi`; `assistant.py` truyền `hoi_toi=lt.hoi_buoi_toi(query)`.
- `xep`: xin buổi tối mà khung không có buổi tối nào ⇒ `khong_xep` thêm `{"diem": "buổi tối", "ma_luat": …}` với 3 mã luật mới, câu cố định do code nối vào khối "Ghi chú của lịch" (D2b / D4b):
  - `toi_tre_em` — đi cùng trẻ nhỏ, lịch chỉ xếp sáng và chiều;
  - `toi_lon_tuoi` — đi cùng người lớn tuổi, như trên;
  - `toi_khong_diem` — bảng điểm chưa có điểm buổi tối hợp sở thích của bạn.
  `kiem_khung` thêm mã `toi_khong_bao` (xin buổi tối, khung không có, thiếu câu lý do) + một test cố tình vi phạm.
- `khung_chu`: chỉ ở lượt có mã trên, khung gửi model có thêm dòng `DONG_KHUNG_TOI` ("Buổi tối: không xếp — không gợi ý hoạt động buổi tối."). Lượt khác chữ khung giữ nguyên.
- `kiem_cuoi` mã mới **`toi_ngoai_khung`** — chỉ chạy khi code đã từ chối buổi tối. Bắt (a) dòng lịch mở bằng nhãn tối, trừ dòng phủ định / khuyên nghỉ; (b) câu nhắc tối / đêm có "được / có thể" mà không có "không / chưa / đừng / tránh / nghỉ". Hỏng ⇒ rút lại như citation hỏng (D8).

## 3. Cách đã chạy thật

Từ `backend/` của worktree `/tmp/b_b5sua` (`p9-b5-sua`), `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag …`:
- Test: `python -m pytest tests/test_b5_lich_trinh.py -q`; thêm `test_assistant_boundary.py`, `test_chat_stream.py`.
- Q1 (cờ tắt, không mạng): `env -u OPENAI_API_KEY -u SERPER_API_KEY OPENAI_API_KEY=capture-only … python ../data/phase_9/b2_chay/tools/capture_all.py ../data/phase_9/b171/q1/nhanh_d5028d4.jsonl` ⇒ `cmp` với `data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl` (bản C bắt).
- Có phí: `--env-file /home/minhhieu/hue_rag/.env python ../data/phase_9/b5/tools/chay_b5.py chay ../data/phase_9/b171/bo_chay.jsonl ../data/phase_9/b171/da_thay_d5028d4.jsonl`. Bộ chạy = 13 câu đã thấy `bo_do_b5/cau_da_thay.jsonl` + 4 câu B tự viết `data/phase_9/b171/cau_tu_viet.jsonl`: T1 sở thích thiên nhiên 2 ngày (L-a); T2 trẻ nhỏ + xin buổi tối; T3 người lớn tuổi + câu hỏi có / không về một hoạt động buổi tối; T4 một mình + di tích + xin buổi tối. Rồi `chay_b5.py dem …`.
- Thử một biến (T3): chạy lại ×3; bỏ dòng khung ×2 (`data/phase_9/b171/tools/chay_khong_dong_toi.py`); đổi chữ dòng khung ×2 (đã trả về bản đầu, không giữ).

## 4. Kết quả quan sát

- **Test [Chạy]:** `test_b5_lich_trinh.py` + `test_assistant_boundary.py` + `test_chat_stream.py` **236 passed**. Phần mới: quét 120 tổ hợp "câu lấp đúng sự thật", thiên nhiên 1–3 ngày không lấp, bộ dò buổi tối 9 ca, L-b đủ mã + dòng khung + kiểm cuối (đúng / ngược / khung không từ chối), một lượt nối qua lõi thật.
- **Q1 [Chạy]: 228 / 228 giống byte `main`** (cờ `lich_trinh` tắt ⇒ chuỗi gửi model không đổi).
- **Lượt có phí 17 câu [Chạy] — 0,011375 USD:**
  - gọi lịch 14 / 14 câu đủ trường; ngoài Huế từ chối 3 / 3; `loi_khung` 0; ghi chú thiếu 0; lệch nhãn 0; `clarify` / `max_turns` 0.
  - **L-a:** L3 (thiên nhiên 3 ngày) lấp **1 ⇒ 0** so với lượt v3 cũ. T1 lấp 0. L2 / L5 / L6 vẫn lấp có nhãn, `lap_vi = it_diem` (đúng: k < số suất).
  - **L-b:** 4 câu xin buổi tối (L4 phố đêm + người lớn tuổi, T2, T3, T4) ⇒ 4 / 4 có đúng mã + câu lý do trong câu trả lời. Ở 13 câu còn lại, model không nói ngược khung.
  - **Rút lại 1 / 17: T3.**
- **T3 — câu hỏi có / không về một hoạt động buổi tối, người lớn tuổi [Chạy, 7 lượt]:**

  | Biến thể | Lượt | Model từ chối cả lịch (⇒ thiếu trích dẫn ⇒ rút) | Model nói ngược khung (⇒ `toi_ngoai_khung` ⇒ rút) | Đạt |
  |---|---|---|---|---|
  | có dòng khung (bản giữ) | 4 | 4 | 0 | 0 |
  | bỏ dòng khung | 2 | 1 | 1 | 0 |
  | dòng khung chữ khác ("vẫn viết đủ lịch, không nói về buổi tối") | 2 | 2 | 0 | 0 |

  ⇒ Dòng khung **không** phải nguyên nhân duy nhất. Với dạng câu này, model hoặc trả nguyên câu từ chối kho (câu hỏi phụ không có trong tài liệu), hoặc trả lời "được". Phần code của L-b chạy đúng: có câu lý do, và kiểm cuối bắt được lần nói ngược. Nhưng người dùng nhận "Thử lại" thay vì một lịch.
- **Tiền B171: 0,017869 / 0,02 USD** (17 câu 0,011375 + T3 thêm 6 lượt 0,006494). Dữ liệu private: `data/phase_9/b171/`.

## 5. Lỗi và giới hạn

1. **T3 (dạng câu hỏi có / không về buổi tối không xếp) ⇒ rút lại 7 / 7 lượt** (cả 3 biến thể). Đây là hành vi model trước lời dặn, code không tự sửa được. Cần A chọn (mục 6).
2. Kiểm "nói ngược" (b) dựa trên từ: lọt câu khẳng định không dùng "được / có thể" (vd "tối ghé chợ đêm nhé"). Bắt nhầm câu có "có thể" mà không phủ định thì sẽ rút lại. Chỉ chạy khi code đã từ chối buổi tối, nên phạm vi ảnh hưởng hẹp. Lượt có phí: 0 lần bắt nhầm ở 4 câu áp dụng.
3. Bộ dò buổi tối không bắt cách nói ngoài mẫu [Chạy, probe]: "khuya đi đâu chơi" ⇒ không bắt (⇒ không có câu lý do, như trước khi sửa); "lúc 8 giờ tối đi đâu" ⇒ bắt (qua "tối đi").
4. Lấp ở 6 ca "thiên nhiên 4 ngày" là không tránh được với bảng v3 + luật cụm kề hiện tại; bảng v5 (5 điểm mới) có thể đổi.
5. "Đi dày" ít tác dụng vì bảng chỉ 4 / 28 điểm có thời lượng (ghi nhận, không sửa — như A dặn).
6. Nhánh `p9-sua-lich` (C rebase) cũng sửa vòng lặp `xep` (điểm giữ chỗ / điểm đã bỏ) ⇒ khi merge cả hai sẽ có xung đột nhỏ ở `xep` (chỗ chọn buổi sáng). Ai merge sau giải quyết; `chon_sang` cần tôn trọng `loai` / `giu` (đã có qua `used` / `dung_duoc`).

## 6. Bàn giao cho người kiểm (C) + câu cần A chọn

- Đọc: diff `main…p9-b5-sua` (3 file); mục 2–4 ở trên. Chạy lại: test 0 USD; `tai_tao_la.py`, `so_khung_cu_moi.py` (0 USD; cần bản `main` của `lich_trinh.py` chép ra `/tmp/b171_cu/llm/lich_trinh_cu.py`); Q1.
- **A chọn cho T3** (B đề xuất, chưa làm):
  - (a) Ghi giới hạn, đi tiếp. Dạng câu "có / không về buổi tối không xếp" ra "Thử lại". Mất: một loại câu tự nhiên hỏng hẳn.
  - (b) **Code dựng lời lịch tối thiểu từ khung** khi lượt có khung mà chữ model đúng bằng câu từ chối: mỗi điểm một dòng "Sáng: tên [n]", cộng khối ghi chú. Giống cách sửa M-1 của B5b, tất định, có trích dẫn. Mất: lời kém tự nhiên ở đúng ca đó; không xử lý ca model nói "được" (ca đó vẫn rút lại).
  - (c) Sửa lời dặn D7 cho phép model trả lời ngắn câu hỏi phụ bằng câu "hệ thống đã ghi lý do", rồi viết lịch. Đây là bậc chỉnh lời dặn ⇒ theo luật cần bộ kín, nhiều lượt, tốn tiền hơn.
  B nghiêng **(b)**: đã có phép thử, chi phí 0 USD / câu, cùng khuôn với B5b M-1.

**Giải thích ngắn:** lịch "thích thiên nhiên" trước đây hay chèn một lăng vào buổi chiều dù vẫn còn bãi biển / đầm phá chưa đi. Nguyên nhân: code chọn buổi sáng mà không nhìn trước buổi chiều. Giờ code ưu tiên điểm còn "bạn đi chiều", và câu giải thích khi phải chèn di tích luôn nói đúng lý do. Khi khách xin buổi tối mà lịch không xếp (đi cùng trẻ nhỏ / người lớn tuổi, hoặc không có điểm tối hợp sở thích), code tự ghi một câu nói rõ vì sao, và chặn câu trả lời nào hứa buổi tối trái với lịch. Còn một dạng câu (hỏi "tối có … được không?") khiến model bỏ cả lịch; cần A chọn cách xử lý.


## 7. Sửa theo review C + T3 (b) — phiên tối 06/11 (21:15 06/11/2026 `date`)

Nhánh `p9-b5-sua` **rebase lên `main` `d38b05a`** (đã có B5b `db77f32`; A dặn rebase trước khi C kiểm), không xung đột ⇒ 3 commit: `15402dd` (B171 nháp, = `d5028d4` cũ) · **`27b56cb`** (M-1 / m-1 / m-2) · **`a08d2e9`** (T3 b) · **`fd16732`** (dòng khung tối cho người đọc, A quyết) · **`b0e52f8`** (review C vòng 2 M-2). Push `--force-with-lease=p9-b5-sua:d5028d4`, rồi push thường tới `b0e52f8`. Cờ `lich_trinh` vẫn tắt.

**M-1 — kiểm "nói ngược buổi tối" bắt nhầm lời hợp khung.** Sửa `_noi_nguoc_toi`: cả hai luật (dòng mở bằng nhãn tối; câu nhắc tối / đêm + "được / có thể") bỏ qua câu có từ phủ định **hoặc** lời không phải hoạt động: nghỉ, tự do, khách sạn, ngủ, thư giãn, chuẩn bị; "trời tối" không tính là buổi tối.
- **Lệch so với cách A / C đề xuất (B tự quyết, A xem):** đề xuất là "chỉ bắt khi câu có tên điểm của bảng". B chạy thử [Chạy]: 6 / 6 câu nói ngược trong ca dò của C **không có tên điểm nào** ("Tối: ăn chè.", "Tối ghé chợ đêm nhé.", "Đêm có thể dạo cầu Trường Tiền."…) ⇒ luật tên điểm bắt 0 / 6, trái tiêu chí đóng (6 / 6). Tên điểm bảng ở đầu dòng lịch đã được kiểm `diem_ngoai_khung` (D8 (1)) bắt sẵn. Nên B giữ luật theo từ, thêm danh sách "không phải hoạt động".
- 16 ca dò của C vào test (`test_l_b_evening_contradiction_probe`): **16 / 16** [Chạy]. Trên code cũ cùng test hỏng đúng 5 ca bắt nhầm.
- **Lượt có phí: 4 câu xin buổi tối (L4, T2, T3, T4) × 1 = 0,002843 USD ⇒ 0 / 4 rút lại**, `lich_kiem` rỗng cả 4 (`data/phase_9/b171/m1_9037b91.jsonl`; commit lúc chạy `9037b91` = `27b56cb` trước rebase).

**m-1 — bộ dò xin buổi tối.** Thêm "tối muốn / tối thích", "chơi / đi / dạo đêm", "khuya"; "3 ngày 2 đêm", "tối đa 2 điểm" vẫn không bắt. 6 ca test mới [Chạy]; trên code cũ hỏng 4 ca.

**m-2 — "k điểm hợp sở thích".** `hop_ngay` chỉ đếm điểm **đúng sở thích** đi được buổi ngày; điểm người dùng nêu mà không hợp sở thích không tính nữa. Ví dụ ẩm thực 2 ngày + Lăng Tự Đức: cách đếm cũ ra 4, mới ra 3. 1 test [Chạy]. Phép quét 0 USD không đổi: `tai_tao_la.py` 120 ca, L-a còn 6; `so_khung_cu_moi.py` (so với `origin/main`) 1.728 ca, đổi 168, đều thiên nhiên [Chạy].

**T3 = (b) (A chốt).** Lượt có khung lịch mà chữ model đúng bằng câu từ chối ⇒ code dựng lời lịch tối thiểu từ khung (`lt.loi_lich_toi_thieu`: tiêu đề ngày, mỗi điểm một dòng "Sáng: tên [n]"). Lõi ghép dòng "Mình hiểu" + khối ghi chú như thường; chữ code dựng vẫn đi qua kiểm cuối + kiểm citation. Chỗ sửa:
- `assistant.py` `_finish_generated`: nhánh có lịch; `trace.lich["chu_thay"]` đánh dấu đã thay.
- Đường stream: giữ chữ như B5b. Điều kiện giữ mở rộng "có dự báo **hoặc có khung lịch**". Hàm `_chu_giu_lai` dùng chung cho lịch / dự báo, phát chữ thay + dòng "Mình hiểu" nếu chưa phát.
- Lượt lịch bình thường chỉ giữ tới ký tự đầu khác câu từ chối ⇒ không thêm độ trễ thấy được.
- Test `test_t3_refusal_with_frame_becomes_code_built_itinerary` (thường + stream; có ca model viết lịch thật ⇒ không thay) [Chạy]; bỏ phần sửa `assistant.py` ⇒ 2 / 2 hỏng.
- **Lượt có phí T3 × 3 = 0,002337 USD ⇒ 3 / 3 ra lịch, 0 rút lại** (`data/phase_9/b171/t3b_lan{1,2,3}.jsonl`). Lượt 2 model trả nguyên câu từ chối ⇒ code thay; lượt 1, 3 model tự viết lịch đúng khung, không hứa buổi tối. Trước sửa: 7 / 7 rút lại.

**Câu B hỏi (6 ca "thiên nhiên 4 ngày") — A chốt 06/11 tối:** giữ lấp có nhãn, đúng lựa chọn D2 (lấp có nhãn thay vì để ngày trống); câu "không cùng hướng" đúng sự thật là đủ.

**Kiểm sau rebase [Chạy]:**
- Test rộng không key (29 file, trừ 3 file cần key / model): **695 passed, 3 failed + 1 error**, đều loại đã biết:
  - 2 cần `OPENAI_API_KEY`: `test_phase6_settings::…key…`, `test_api_chat::test_health…lifespan`;
  - 2 `test_static_ui` cần bản build giao diện (B không sửa `frontend/`, không build trong worktree).
- `test_b5_lich_trinh.py` 239 passed.
- **Q1: 228 / 228 giống byte** `data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl` (`data/phase_9/b171/q1_sua/nhanh_sau_rebase.jsonl`). `main` mới có B5b cờ tắt, A đã kiểm giống byte lúc merge.

**Dòng khung buổi tối viết cho người dùng (A quyết 06/11 tối, `fd16732`, 21:21 06/11/2026 `date`).** Trước: "Buổi tối: không xếp — không gợi ý hoạt động buổi tối." — model chép nguyên vào câu trả lời 4 / 4 lượt, nửa sau là lời dặn model. Nay `DONG_KHUNG_TOI` theo mã luật, không còn lời dặn, không thêm lời dặn mới:
- `toi_tre_em`: "Buổi tối: để trống — đi cùng trẻ nhỏ nên lịch chỉ xếp buổi sáng và chiều."
- `toi_lon_tuoi`: "Buổi tối: để trống — đi cùng người lớn tuổi nên lịch chỉ xếp buổi sáng và chiều."
- `toi_khong_diem`: "Buổi tối: để trống — bảng điểm của mình chưa có điểm buổi tối hợp sở thích của bạn."
- Kiểm nói ngược thêm "để trống" vào danh sách "không phải hoạt động" (dòng trẻ nhỏ / người lớn tuổi không có từ phủ định ⇒ nếu không thêm, model chép dòng là bị rút). Test: 3 dòng không bị kiểm cuối bắt, không chứa "gợi ý" [Chạy].
- **Lượt có phí [Chạy]:** 4 câu xin tối × 1 (0,003112 USD) + T3 × 1 thêm (0,000803) ⇒ **5 / 5 ra lịch, 0 rút lại, 0 lượt chép lời dặn**. T2, T4 chép dòng mới (đọc được). L4 không nhắc buổi tối. T3 cả 2 lượt model trả câu từ chối ⇒ code thay bằng lời lịch (T3 b). File: `data/phase_9/b171/dong_toi_4cau.jsonl`, `dong_toi_t3_them.jsonl`.
- Test `test_b5_lich_trinh` + `test_b5b_thoi_tiet` + `test_chat_stream` + `test_assistant_boundary` **346 passed**; Q1 228 / 228 giống byte (`data/phase_9/b171/q1_sua/nhanh_fd16732.jsonl`) [Chạy].
- Ghi nhận: lý do buổi tối nay hiện **hai lần** khi model chép dòng khung — trong lịch và trong khối ghi chú (câu `CAU_KHONG_XEP`). Lặp nhưng đúng, không lạ; muốn bỏ một chỗ ⇒ đổi khối ghi chú (code), A quyết.

**Review C vòng 2 — M-2 "N ngày N đêm" (`b0e52f8`, 21:26 06/11/2026 `date`).** Kiểm nói ngược tính "đêm" trong "3 ngày 2 đêm" là nhắc buổi tối ⇒ "Lịch 3 ngày 2 đêm này bạn có thể đi chậm rãi." bị bắt nhầm, rút cả lịch. Sửa:
- "<số> đêm" (chữ số hoặc một…năm) không tính là nhắc buổi tối, cùng chỗ với "trời tối".
- Luật (b) xét **từng vế câu** (tách cả `,` `;`) ⇒ "Chiều về sớm kịp bữa tối, bạn có thể đi chậm." không còn bắt nhầm (B tự quyết sửa thay vì ghi giới hạn).
- 5 ca mới vào test: 3 không bắt, 2 câu có dấu phẩy vẫn bắt ("Buổi tối, bạn có thể ghé chợ đêm.", "Nếu còn sức, tối bạn có thể dạo phố."); 16 ca dò + 6 ca bộ dò cũ vẫn đạt.
- Chấm lại **0 USD** mọi chữ model đã lưu của B171 (26 lượt: 17 câu `da_thay_d5028d4` + M-1 + T3 + dòng tối) bằng kiểm cuối mới: không lượt nào thêm lỗi. Lượt T3 cũ `thieu_trich_dan` nay đạt, vì code thay câu từ chối.
- **Lượt có phí — câu "3 ngày 2 đêm + xin tối" (B tự viết, A dặn thêm):**
  - Bản đầu (T5, `data/phase_9/b171/cau_t5.jsonl`, 0,000465 USD): chỉ hỏi "buổi tối đi đâu được không" ⇒ model trả lời thẳng câu hỏi, **không gọi `lich_trinh`**. Lỗi ở cách B viết câu (không có ý xin lịch), không phải lỗi code.
  - Viết lại có "Lên lịch giúp mình…" (T5b, `cau_t5b.jsonl`, 0,001415 USD) ⇒ gọi lịch đủ tham số (3 ngày, người lớn tuổi, di tích, `hoi_toi`), mã `toi_lon_tuoi`, `lich_kiem` rỗng, không rút lại (`t5b_m2.jsonl`).
  - **Quan sát:** model viết một dòng "Buổi tối: có thể nghỉ hoặc đi bộ ngắn…" (dè dặt, có trích dẫn, khuyên nghỉ). Dòng này lọt kiểm vì có chữ "nghỉ" — đúng giới hạn 3 bên dưới, nay thấy trên lượt thật. Không sửa: chặn thêm sẽ cần hiểu nghĩa câu, hoặc đổi lời dặn ⇒ A quyết.
- Test `test_b5_lich_trinh` + `test_b5b_thoi_tiet` + `test_chat_stream` + `test_assistant_boundary` **351 passed**; Q1 228 / 228 giống byte (`q1_sua/nhanh_b0e52f8.jsonl`) [Chạy].

**Tiền B171: 0,028844 / 0,04 USD** (trước 0,017869 + M-1 0,002843 + T3 0,002337 + dòng tối 0,003915 + T5 / T5b 0,00188).

**Giới hạn / ghi nhận (không sửa):**
1. ~~Model chép nguyên dòng khung có lời dặn~~ ⇒ đã sửa (`fd16732`, mục trên).
2. Lời lịch code dựng (T3) không có giờ / mô tả điểm, chỉ tên + [n] + khối ghi chú: đúng phạm vi (b), kém tự nhiên hơn chữ model.
3. Kiểm nói ngược vẫn dựa trên từ: lọt câu hứa buổi tối không dùng "được / có thể" và không mở dòng bằng "tối" (vd "Bạn ghé chợ đêm sau bữa tối nhé"). Lời có chữ nghỉ / khách sạn đi kèm một hoạt động (vd "tối nghỉ ở khách sạn rồi ra phố đi bộ") cũng lọt.
4. **Ghi chú merge với `p9-sua-lich` (C dặn):** `tham_so` có thêm khoá `hoi_toi`, `xep` có `chon_sang` ⇒ người gộp sau phải để `chon_sang` tôn trọng `giu` / `loai` (đi qua `used` / `dung_duoc`), và `ThamSo(**…)` dựng lại từ khung đã lưu phải nhận `hoi_toi`.

**Bàn giao C:** diff `origin/main…p9-b5-sua` (commit `27b56cb`, `a08d2e9` = vòng 2 C đã kiểm; mới: `fd16732`, `b0e52f8`; `15402dd` = bản C review vòng 1). Chạy lại: `tests/test_b5_lich_trinh.py` (+ `test_b5b_thoi_tiet.py`, `test_chat_stream.py` vì đổi đường stream chung với B5b), ca dò của C, Q1, 2 phép quét 0 USD.
