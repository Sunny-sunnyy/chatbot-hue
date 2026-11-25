# STATUS_A — ghi đè 14:48 25/11/2026 (giờ `date`) — phiên A (`agy` CLI) đang làm việc trực tiếp với chủ dự án.

**Mục đích:** ảnh chụp bàn giao gọn của phiên điều phối A (`WORKFLOW.md` §8), để sau `/compact` hoặc khi mở phiên `/swarm` mới đọc một lần là bắt nhịp ngay.

1. **Đã xong (tới 14:48 25/11/2026):**
   - Nhánh dọn sổ `p15-a-don-so-2511` đã gộp lên `main` (`6d371ecb`, thêm nhắc nhở ở `914cc396`), worktree `/tmp/hr_a_don_so` đã gỡ sạch.
   - Đã báo gọn kết quả đêm 24 ⇒ 25/11 và thống nhất xong với chủ dự án **4 quyết định chiều 25/11** (`data/loi_user/2026-11-25.md`):
     1. **Nút "Hoàn tác lần sửa này"** (`thu-b-hoan-tac` + `thu-c-hoan-tac`): gộp + mở ở máy demo sau sửa ~3 dòng câu dải đầu, review chéo và kiểm nhanh 390 px / thêm-dời-tối.
     2. **Dải "Hồ sơ theo chủ đề" ở Trang chủ** (`thu-c-trang-chu-chu-de`): gộp + mở dưới 5 ô, đổi tiêu đề 5 ô thành **"Khám phá theo lĩnh vực"**.
     3. **6 ứng viên tính năng từ 25 repo ngoài:** không thêm lúc này, chốt gọn ở 2 bản thử trên.
     4. **5 việc nhỏ bộ `deploy/`:** làm 4 việc đầu (bó quyền Docker, nhắc Caddyfile, kiểm giả IP, đoạn "vì sao không CI/CD") — không thêm lịch tự dừng máy EC2.
2. **Đang chạy ngay khi bật `/swarm` (bảng chi tiết ở `VIEC_DANG_MO.md` mục A.2):**
   - **B:** hoàn thiện backend + mở tính năng Hoàn tác & Dải Trang chủ + sửa nợ chú thích cũ nếu chạm file; review chéo 4 việc nhỏ `deploy/` của C.
   - **C:** sửa ~3 dòng câu dải đầu `LenKeHoach.jsx`, đổi tiêu đề 5 ô `TrangChu.jsx`, dựng `dist` tạm + chạy 1 lượt thật kiểm Hoàn tác & Dải Trang chủ; làm 4 việc nhỏ `deploy/`.
   - **E:** review chéo code Hoàn tác + Dải Trang chủ; chạy test chạm + 1 lượt cả bộ test trên `main` sau khi gộp xong.
   - **D:** 1 hàng nhỏ bài 23 + `PL_C`; đọc diff vòng cải tiến 24/11 của A; cập nhật giáo trình cho 2 tính năng mới sau khi gộp.
   - **A:** viết vòng cải tiến 24/11 + tổng kết đợt thử 3 ngày (`SO_CAI_TIEN_CACH_LAM.md`); bật Qdrant trước việc server/chỉ mục; điều phối và gộp `main` + dựng lại `frontend/dist` cây chính.
3. **Việc kế chờ chủ dự án (KHÔNG giục):**
   - Chủ dự án tự test lại khi muốn ⇒ thuê GPU huấn luyện model nhận ảnh (`goi_may_thue.tar`, 93 lớp).
   - Bốn bài kho chưa có giờ mở cửa (chờ URL ngoài nếu chủ dự án gửi).
4. **Việc nội bộ còn nợ của A:**
   - Vòng cải tiến cách làm ngày 24/11 + tổng kết đợt thử 3 ngày (21–23/11) dựa trên `SO_CAI_TIEN_CACH_LAM.md` và 6 bẫy mục 5 dưới.
5. **Đầu vào vòng cải tiến từ tối+đêm 24/11 (giữ nguyên để xét, chưa bỏ):**
   - Câu hỏi có dòng mở ngoặc về việc KHÁC làm câu trả lời chủ dự án thành 3 nghĩa ⇒ một ô chọn chỉ nói MỘT việc.
   - Giao "số nguồn bấm được" khi quên quyết định đã bỏ `[n]` trong chữ (lặp lần 2 trong một buổi) ⇒ tra `HIEN_TRANG.md` mục 4 phần "Giao diện" + xem tính năng gần nhất TRƯỚC khi giao.
   - Tóm repo từ README dẫn tới nói sai thực tế code ⇒ gắn nhãn rõ "theo README, chưa đọc code".
   - Mở `so_tay` trước khi kiểm "cảnh báo an toàn của kho có tới không" (gặp lần đầu) ⇒ đưa vào bước kiểm trước khi mở tính năng viết về nơi tham quan.
   - Ghi giờ ước vào file tài liệu 3 lần (`date` trước khi ghi).
   - Nhãn ô thiếu "Kho tư liệu chưa có" nói quá về kho ⇒ chỉ dùng chữ đó khi code thật sự biết kho thiếu.
6. **Thứ đang chạy / rác / trạng thái máy (14:48 25/11/2026):**
   - `main` tại `914cc396` (cộng commit sổ chiều 25/11), 0 server, 0 cổng 80xx đang mở, 0 worktree tạm.
   - **Qdrant đang TẮT** (`Connection refused` cổng `6335`) ⇒ trước khi bật server hoặc chạy việc đụng chỉ mục, chạy `docker compose up -d qdrant` và kiểm đủ **9.536 điểm**.
7. **Bẫy mới khi chuyển sang `agy` CLI + `/swarm` (25/11/2026):**
   - `scripts/commit_push.sh` từ chối symlink trỏ tới thư mục (`.agents/skills`) ⇒ stage tường minh khi cần.
   - `data/bo_nho_agent/MEMORY.md` nằm ngoài git ở cây chính ⇒ trong `workspace: "share"` đọc bằng đường dẫn tuyệt đối `/home/minhhieu/hue_rag/data/bo_nho_agent/MEMORY.md`.
   - Trong `/swarm`, lệnh `kill` xoá luôn workspace của worker ⇒ chỉ `kill` sau khi nhánh đã push lên `origin` hoặc gộp vào `main`.
