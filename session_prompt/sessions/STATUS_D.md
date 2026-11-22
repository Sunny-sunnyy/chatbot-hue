# STATUS D — ghi đè 09:59 22/11/2026 (giờ `date`). Vai: phiên giảng, viết giáo trình; làm việc trực tiếp với chủ dự án.

Terminal phiên này: `hue-rag-85`. Nhánh `p9-d-giao-trinh`, worktree `/tmp/hr_d_giaotrinh` (mất khi máy khởi động lại ⇒ tạo lại từ `origin/p9-d-giao-trinh`).

## Đang làm
- **Viết GIÁO TRÌNH** `bai_hoc/giao_trinh/` (sổ việc khối E). Mục lục + khuôn bài: `bai_hoc/giao_trinh/00_GIAO_TRINH.md` — chín chặng, 41 bài chính, 6 phụ lục, năm ví dụ thật dùng suốt bộ.
- **Chủ dự án đã trả lời (22/11, hộp tick, từng câu):** mở đầu bằng 3 bài nền ngắn · bộ cũ vướng cả bốn chỗ (không ghép được bức tranh, quá nhiều chi tiết thi công, thiếu cấu hình + kết quả so sánh, ẩn dụ che cơ chế) ⇒ bỏ ẩn dụ, thân bài sạch chi tiết thi công, mỗi bài có "Cấu hình đang chạy" + "Đã so" · nhịp: bài mẫu rồi viết tiếp theo chặng, gộp chặng nào chủ dự án đọc chặng đó · phần khó nhất theo chủ dự án là trợ lý + xếp lịch + harness ⇒ bài mẫu thứ ba là bài 21 (harness).
- **Cách làm đã chốt với phiên điều phối:** D tự chốt dàn bài; gộp theo chặng 4–6 bài; mỗi bài qua một agent con ngữ cảnh mới đối chiếu số với code / số đo trước khi gộp (biên bản ở `data/hoc_cung_D/kiem/`, riêng tư).

## Trạng thái từng bài
- Đã viết + đã qua đối chiếu độc lập: 00 (mục lục), 02 (RAG là gì), 10 (embedding), 21 (harness).
- Đã viết nháp, CHƯA xong đối chiếu: 07 (kho), 08 (cắt đoạn), 09 (metadata), 11 (BM25), 12 (Qdrant).
- Kế tiếp theo thứ tự: chặng 3 (bài 13–16) ⇒ chặng 0–1 còn lại (bài 1, 3, 4, 5, 6) ⇒ chặng 4 (đo). Chặng 5–6 (trợ lý, lên kế hoạch) và chặng 7 viết sau khi phần đang đổi lắng.

## Ghi chép riêng tư (không commit)
- `data/hoc_cung_D/BAN_VOI_A_VA_D_BEN_KIA.md` — lời chủ dự án, trả lời của phiên điều phối, hai lượt phản biện của phiên D dự án kia (chỉ hình thức).
- `data/hoc_cung_D/vi_du_*_vet.json` — năm lượt chạy thật dùng làm ví dụ; `vet_tim_ba_vi_du.json` — điểm từng tầng của bước tìm (chạy riêng bước tìm, 0 đồng) bằng `data/hoc_cung_D/tools/vet_tim.py`.

## Đang khai báo sửa
- `bai_hoc/giao_trinh/` (chỉ thư mục này) + file này.

## Bài học cách làm đã gặp thật trong phiên (ghi một lần)
- Nhãn ví dụ "kho không có" phải được dò chứng minh bằng `scripts/grep_kb.sh` trước khi dùng: ví dụ đầu tiên D chọn hoá ra kho có, chỉ là bước tìm bỏ sót (agent kiểm bắt được).
- Đọc hàm lõi chưa đủ: phải đọc cả lớp gọi nó (route chat stream) — câu "kiểm rồi mới hiện" sai với đường người dùng thật.
- Câu ở "Ý chính" / "Những điều cần nhớ" phải đứng được trước mọi dòng của bảng "Đã so" trong cùng bài.

## Việc dở / câu hỏi cho phiên điều phối
- Mỗi đợt D nhắn phiên điều phối tên file + biên bản; phiên điều phối đọc diff, gộp, thêm dòng trỏ ở `bai_hoc/README.md`.
