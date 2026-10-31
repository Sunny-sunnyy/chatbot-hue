# TỔNG HỢP đợt 2026-10-31 — spec streaming câu trả lời

Viết 12:42 31/10/2026 (A, kết phiên 31/10). Trạng thái: **MỞ** — spec bản 4 `cf1ae9ef6c2c` review đạt; còn 1 câu User (mục tiêu "chữ đầu tiên") + User duyệt sha; chưa code.
Dữ liệu (private): `data/tinh_nang_moi_2026-10-27/` (nháp v2 / v3, C97, B99, B104, kết quả thô Codex review), kết quả ChatGPT `gửi chatgpt/2026-10-28/kết quả nghiên cứu/`.

## Mục tiêu
Chữ trả lời hiện dần thay vì chờ trắng (câu dài hôm nay p95 7,6 s > yêu cầu 5 s), giữ bảo đảm citation và lỗi tệ nhất User chốt 28/10 (sai cảnh báo an toàn).

## Quyết định theo giờ (giờ A ghi nhận bằng `date`)
- 10:23 — giao diện mới (React / Next…) bàn **sau Phase 8**, gộp nội dung AI FDE; spec này chỉ API + sửa tối thiểu `frontend/` JS thuần.
- 10:32–10:46 — A: lỗi trước luồng chọn cách (b) (endpoint thường, `StreamingResponse` tự dựng); ép `response.incomplete` bằng tham số thật không phải lỗi giả (≤ 0,001 USD).
- Trước 11:02 (giờ A không ghi lúc đó; trước B102 vòng 2) — A: không thêm chỗ nối chỉ dùng khi test (giao diện D3 (a), luồng đứt ⇒ giới hạn).
- 11:26 — **User chốt D1 = PA1** (chữ hiện ngay + tiến độ thật, kiểm citation cuối như hôm nay).
- 11:44 — **User chốt D2 = (a)**: sàn p50 ≤ 3 s / p95 ≤ 5 s cho "tới chữ trả lời đầu tiên trên trình duyệt"; tới đủ câu chỉ theo dõi.
- 11:48 — **User chốt D3 = phương án 1**: kiểm cuối hỏng ⇒ rút lại; lỗi / đứt giữa chừng ⇒ xóa hết; lời báo + "Thử lại". A đặt D5 = 1 % / tuần; không nút "Dừng".
- 11:52 — A: câu từ chối cùng sàn 3 / 5 s, đo tới lúc biết chắc là từ chối, báo riêng.

## Chuỗi việc + review
| Việc | Ai | Kết quả |
|---|---|---|
| B99 kiểm nguồn kết quả ChatGPT | B | 21 / 22 URL mở, 0 ý bị nguồn nói ngược, 3 ý "suy ra", #3314 đã sửa (A tự kiểm 2 ý) |
| C97 đối chiếu với code + nháp v2 | C | JSON `output_type` vẫn stream trên SDK đã cài; từ chối gần như luôn do model viết; FastAPI có sẵn SSE; 14 mục nháp cần sửa — B100: 1 major (generator SSE + lỗi trước `yield` ⇒ 200 thân rỗng, probe thật) ⇒ ready |
| C98 nháp v3 (D1 theo propose-options) | C | B102: 1 major (hứa test không tạo được bằng đường thật) ⇒ ready |
| C100 spec | C | B105: 1 major (anyio hủy mọi `await` trong `finally` khi ngắt ⇒ log trước mọi await + `CancelScope(shield=True)`) ⇒ ready; **Codex review một lần (W33)**: 2 minor mới (bắt riêng `CancelledError`; 422 trước handler không có dòng log) ⇒ bản 4 ready |
| Tra Codex "chữ đầu tiên" | A | không có chuẩn ngành; Nielsen 1 s; API công khai p50 vài trăm ms – ~1,1 s; Codex suy ra mục tiêu 1,5 / 3 s (A WebFetch kiểm 2 ý) |

Tiền: 0 USD paid (Codex theo gói tài khoản).

## Kết quả W33 (Codex review)
Dương nhỏ: 2 minor thật mà review Claude bỏ sót; không bắt được lỗi cần chạy thư viện (worktree không có `.venv`); 58 s, 14 lệnh đọc trong worktree, 0 lệnh ra ngoài.

## Còn mở / bước tiếp
1. User trả lời Q1 (A khuyên: sàn 3 / 5 s giữ + mục tiêu báo cáo 1,5 / 3 s) ⇒ A điền `TBD` ⇒ B kiểm phần đổi.
2. User duyệt sha bản cuối ⇒ commit ⇒ code S1 (gom lõi chung, T1 giống byte) ⇒ S2–S4; đo C1–C7 trên trình duyệt thật.
3. Giới hạn chính (spec §10): lỗi nghĩa không bắt ở phương án nào; giao diện D3 (a) + luồng đứt chưa kiểm bằng đường thật; nhánh 503 / 409 / 500 / 502 chỉ test logic.
