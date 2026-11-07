# Implementation Report: S1 — backend cổng du lịch đợt 1

Người làm: B (Claude Code, Opus 5.5)
Date: 12:43 07/11/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` (User duyệt bản `ff3c317ec88b`, 11:56 07/11) §2 D3 / D4 / D6 / D7, §5 S1.
Nhánh `p11-cong-dot-1` (từ `main` `eb68458`): `1c31ce4` (S1) + `0cb0b0a` (sửa chọn đoạn — A chốt (e)). Worktree `/tmp/b_cong`.

## 1. Phạm vi

Đã làm đủ D3, D4, D6, D7 và test của S1. D3 chạy đúng về code, nhưng lượt thật thì model còn từ chối (mục 4). A đã dừng D3 để chờ C đo X1 rồi User chọn.

## 2. Thay đổi chính

- **D3 — lượt biểu mẫu** (`backend/llm/assistant.py`):
  - hàm mới `_xep_bieu_mau` + `answer_bieu_mau`; nhánh `trace.bieu_mau` trong `answer_turn` / `answer_turn_stream`;
  - `answer_turn_stream_parallel` bỏ phần song song #6 khi là lượt biểu mẫu;
  - code gọi hàm `lich_trinh` có sẵn với giá trị nút ở cả 4 trường, không định tuyến, không lần tìm đầu, rồi sinh **một lần, không công cụ**;
  - khung + `LICH_TRINH_LUAT` + đoạn nguồn của mỗi điểm nằm trong ngữ cảnh do code dựng;
  - phần sau vòng đọc dùng chung với đường cũ: giữ chữ khi chữ đầu có thể là câu từ chối, dòng "Mình hiểu", kiểm cuối D8, khối ghi chú, lời lịch tối thiểu khi model từ chối.
- **D3 — route** (`backend/api/routes/chat.py`):
  - `ChatRequest.bieu_mau`: thiếu `truong.so_ngay` ⇒ 422; cờ tắt ⇒ 404;
  - câu gốc cố định `CAU_BIEU_MAU` + `ghep_cau`; chữ `query` trình duyệt gửi kèm **không dùng**.
- **D4:** cờ `assistant.lich_trinh_bieu_mau` (tắt; nạp bảng điểm, không cần vòng công cụ).
- **D6** (`backend/api/routes/cong.py` mới, nạp trong lifespan sau bước kiểm build record):
  - `/api/kham_pha`;
  - `/api/kham_pha/bai?id=` — chỉ nhận đúng mã có trong danh sách; `..` / `evaluation/` / `sealed` ⇒ 404;
  - `/api/thoi_tiet` — cờ `thoi_tiet` tắt ⇒ 404; lỗi ⇒ chỉ trả trạng thái, không số;
  - `/api/tinh_nang` — chỉ boolean.
- **D7:** `SourceResponse.bai_id` có ở cả 2 route.
- **(e) — đổi luật B5 D6, A chốt:** `_lay_nguon_lich` chọn, trong top-10 cùng file của điểm, đoạn có bằng chứng dài nhất (thay vì đoạn đầu tiên). Hàm này dùng chung với lịch câu tự do, cờ đó đang tắt.

## 3. Cách đã chạy thật

Lệnh chạy từ `backend/` của worktree:
- **Q1** — `capture_all.py`, 0 USD:
  - mốc `main` chạy lại trên HEAD (`data/phase_11/cong_dot_1/q1/main_eb68458.jsonl`, sha `dba1f578eef1` — trùng mốc cũ của C207);
  - so với 3 lần chạy trên nhánh: cờ tắt, cờ bật (sửa tạm `settings.yaml` rồi trả lại), sau (e).
- **Q1m lượt biểu mẫu:** `data/phase_11/cong_dot_1/tools/q1m_bieu_mau.py` — TestClient + lifespan thật, 6 tổ hợp × 2 route × 2 lần.
- **Pytest:** `tests/test_cong_dot_1.py` (20 test mới) + bộ rộng không khoá (mọi file trừ 3 file cần mạng / model).
- **Server thật** (`uvicorn`, `.env`):
  - cổng ổn định ở cổng 8861 (cờ như `main`);
  - lượt biểu mẫu thật ở cổng 8862 (`tools/app_bieu_mau.py`, bật cờ trên bản sao settings).
- **Thử khả thi cách (a)** "lượt công cụ dựng sẵn": `tools/thu_cach_a.py`.

## 4. Kết quả quan sát

- **Q1:** 228/228 giống byte ở cả 3 lần.
- **Q1m:** mỗi lượt đúng 1 lần gọi model; `/api/chat` = stream (so sau khi bỏ cờ `stream`); 2 lần chạy cùng sha; chữ gõ kèm không lọt tới model; 0 công cụ; 6 tổ hợp cho 6 sha khác nhau.
- **Test:** 20/20 đạt. Bộ rộng 723 đạt, 1 hỏng + 1 lỗi đúng là 2 test cần khoá OpenAI (như `main`). Sau (e): test cong + b5 + b5b 349 đạt.
- **Thử phá có chủ đích (0 USD):** cho ra giá trị sai ở một trường ⇒ test tổ hợp hỏng; bỏ đoạn rẽ khỏi đường song song ⇒ 4 test stream hỏng.
- **Cổng ổn định:** `/` 200; `/health` 5/5; câu trong kho (stream) ⇒ success, 9 nguồn đều có `bai_id`; câu ngoài kho ⇒ ngoài phạm vi; 2 dòng `chat_metrics`; 0 câu hỏi trong log; `/api/kham_pha` 204 bài; mã `..` ⇒ 404; lượt biểu mẫu khi cờ tắt ⇒ 404.
- **Q-F phần tất định:** 120 tổ hợp nút ⇒ khung nhận đúng cả 4 giá trị, 0 hỏi lại, 0 công cụ, 1 lần gọi mỗi lượt.
- **Lượt biểu mẫu THẬT** — model trả câu từ chối ⇒ code dựng lời lịch tối thiểu (khung trơn; theo Q-F tính là trượt):
  - trước (e): 5/5 từ chối;
  - cách (a): 3/3 từ chối;
  - sau (e): 2/3 từ chối, 1/3 model tự viết.
  - Kiểm cuối qua ở mọi lượt.
- **Nguyên nhân đã đo** (của phần trước (e)): ở 11/28 điểm, đoạn được chọn chỉ là dòng tên (< 80 ký tự), nên luật "kèm một ý ngắn lấy từ tài liệu" không viết được. Sau (e): 0/28 điểm dưới 80 ký tự (ngắn nhất 396).
- **Chưa có nguyên nhân đã chứng minh** cho 2/3 lượt còn từ chối sau (e). C đang đo X1.
- **Tiền S1:** 0,0041 USD (cổng 0,0010 · 5 lượt biểu mẫu 0,0009 · cách (a) 0,0009 · pilot sau (e) 0,0012).

## 5. Lỗi và giới hạn

- D3 chưa đạt với model thật (mục 4) ⇒ cờ `lich_trinh_bieu_mau` để tắt.
- 3/120 tổ hợp (từ 4 ngày + ẩm thực) bị cắt còn 3 ngày do trần 10 nguồn mỗi lượt. Code trước (e) cũng y hệt (đã so) ⇒ ngoài phạm vi, ghi lại để biết.
- Ngân sách ngữ cảnh của lượt biểu mẫu đếm bằng lời dặn trả lời (`instructions=None`), cộng thêm phần đệm công cụ của `_lay_nguon_lich` ⇒ đếm dư một chút, an toàn.

## 6. Bàn giao cho người kiểm

- Đọc trước: diff `eb68458..0cb0b0a` thư mục `backend/`, rồi `tests/test_cong_dot_1.py`.
- Chạy lại: Q1 (`capture_all.py` ⇒ `cmp` với `main_eb68458.jsonl`), `q1m_bieu_mau.py`, file test.
- S3 dùng `tools/app_bieu_mau.py` (server bật cờ).
- Chữ model của các lượt thật để ở `data/phase_11/cong_dot_1/pilot_e/` và `thu_cach_a/` (private).

**Giải thích ngắn:** biểu mẫu "Lên kế hoạch" gửi giá trị nút thẳng cho code xếp lịch, không qua model chọn, nên lịch luôn đúng lựa chọn người dùng. Phần model viết lời theo khung thì còn hay từ chối. Đã sửa một nguyên nhân (đoạn tài liệu quá ngắn); phần còn lại chờ C đo cách khác rồi User chọn. Các API đọc bài kho / thời tiết / cờ không gọi model.
