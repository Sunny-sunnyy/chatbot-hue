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
