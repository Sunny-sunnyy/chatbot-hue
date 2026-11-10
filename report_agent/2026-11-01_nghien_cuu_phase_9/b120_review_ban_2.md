# B120 — review bản 2 `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md`

B, 16:15 01/11/2026 (`date`). Việc: A nhờ qua tin nhắn (B120). B không sửa file của A.

## Lần 1 (16:15 01/11/2026): **blocked** — bản 2 chưa có trên đĩa
- Bản đang có: 78 dòng, sửa lúc 15:29:49; dòng 3 vẫn ghi "bản 1 (SƠ BỘ)… chưa có kết quả ChatGPT". Bản này **không có** mục 3 "thử TRIPO", mục 4 "ChatGPT đã kiểm", mục 6 "lịch".
- Commit gần nhất chạm file: `37ee946`. `git status` không thấy file đổi; tìm trên máy không thấy bản khác cùng tên mới hơn `c117_kiem_chatgpt.md`.
- Đã chạy trên bản đang có: `overlap_scan` **0 trùng**; tên dự án khác **0**.
- Căn cứ đã đọc sẵn: `tripo/b119_kham_pha.md` (B viết), `c117_kiem_chatgpt.md` (33 dòng). Chờ A lưu bản 2 rồi review tiếp.

## Lần 2 (16:16 01/11/2026): review bản 2 (dòng 3 "16:13 … bản 2", 113 dòng)
**Kiểm đã chạy:** `overlap_scan` **0 trùng**; tên dự án khác **0** [Chạy]; đối chiếu §3 với `tripo/b119_kham_pha.md` §2–§3, §4 với `c117_kiem_chatgpt.md` từng dòng.

**Kết luận: `ready_for_user_confirmation`** — **0 blocker · 0 major** · 2 minor (không chặn).

- **(1) Bảng 10 câu §3 khớp b119, không nói quá.** Câu 2 "từ chối nhầm" và câu 8 "nhiều file kho ghi quy định này" là phần A tự kiểm kho, có ghi "(A kiểm)" ⇒ ghi đúng người kiểm. Câu 8 tóm tắt ghi "nói ngược kho" (không nói TRIPO sai) + §7 "chưa đối chiếu web" ⇒ đúng mức. Biểu mẫu lịch trình (dòng 52–54) khớp b119 §3.
- **(2) §4 khớp c117** ở cả 9 dòng: R01 (GPT-5 mini đúng; 6 ngôn ngữ / dưới 3 giây sai chỗ); Booking 37.325 / 6 % / 12 %; Peranakan; HeriStepAI; Luật AI Điều 11.1 + 3.5; Luật dữ liệu cá nhân; Klook; ALCE gộp 2 bài; Adaptive-RAG. Phần "(suy ra)" tách đúng. §2 "6 đúng hết, 3 sai một phần" khớp.
- **(3) Repo public:** đạt (quét máy + đọc). Mô tả kho chỉ ở mức "kho có / ghi", không chép nội dung; 10 câu là câu A tự viết, không phải Golden.

**Minor:**
- **m-1:** §3 câu 4 ghi "**đúng** khoảng ngày" cho cả hai bên — b119 chỉ ghi "khớp nhau", chưa ai đối chiếu nguồn chính thức ⇒ nên ghi "khớp nhau".
- **m-2:** §4 dòng Luật AI — c117 nói C đọc điều khoản qua **bản dịch tiếng Anh "chỉ để tham khảo"** (PDF gốc là ảnh scan) và "cần người hiểu luật xác nhận, C không kết luận" về Điều 3.5. Bản 2 bỏ hai lưu ý này ⇒ nên thêm 1 cụm.
