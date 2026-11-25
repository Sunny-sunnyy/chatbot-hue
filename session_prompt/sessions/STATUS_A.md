# STATUS_A — ghi đè 14:03 25/11/2026 (giờ `date`) — phiên A (`agy` CLI) đang làm việc trực tiếp với chủ dự án.

**Mục đích:** ảnh chụp bàn giao gọn của phiên điều phối A (`WORKFLOW.md` §8), để sau `/compact` hoặc khi mở phiên `/swarm` mới đọc một lần là bắt nhịp ngay.

1. **Đã xong (đêm 24 ⇒ 25/11 và sáng/trưa 25/11):**
   - `main` tại `a8ca8758` (trước khi gộp nhánh dọn sổ `p15-a-don-so-2511`): chuyển xong quy trình sang Gemini (`agy` CLI) + `/swarm` (`.agents/skills -> ../skills`, 32 file memory Claude sang `data/bo_nho_agent/claude_memory/` + `MEMORY.md`, Playwright MCP ở `~/.gemini/config/mcp_config.json`, kiểm thử mở phiên ngữ cảnh sạch đạt).
   - Sản phẩm ở máy demo: **61 tính năng mở / 6 tắt**, kho **269 bài / 9.536 đoạn**, `frontend/dist` `23:25 24/11/2026`, giáo trình **44 bài + 9 phụ lục** (`ff459ed7`), cả bộ test **2.391 ca đạt / 0 đỏ** (`8ac85219` + `22109ade`). Đêm qua đã gộp & mở `so_tay` (kèm sửa cảnh báo `784ca0a8`) và `ho_so_chu_de` (`658c199d`); các phiên B, C, D, E đều đã dừng sạch từ đêm qua.
2. **Đang ở nhánh riêng chờ chủ dự án chọn (KHÔNG gộp, KHÔNG mở):**
   - Nút **"Hoàn tác lần sửa này"**: `origin/thu-b-hoan-tac` `34af509` + `origin/thu-c-hoan-tac` `ae54841` (lượt thật chung đạt, ảnh `data/x15_phan_ai_2026-11-23/c_ho_so/luot_that_hoan_tac/`). Nếu chọn gộp: sửa ~3 dòng dải đầu cột lịch ở `LenKeHoach.jsx`.
   - **Dải chủ đề ở Trang chủ**: `origin/thu-c-trang-chu-chu-de` `b7794fe` (ảnh `…/c_ho_so/anh_trang_chu/`), kèm câu đổi tiêu đề 5 ô lĩnh vực ("Khám phá theo chủ đề" ⇒ "Khám phá theo lĩnh vực"?).
   - **Kết quả đọc sâu 25 repo:** `data/x22_doc_repo_2026-11-24/TOM_TAT.md` (6 ứng viên chưa dựng · 5 việc nhỏ bộ deploy `CACH_DEPLOY.md` · đề bài AI khác hãng `DE_BAI_3.md`).
3. **Việc kế trình chủ dự án theo thứ tự (mỗi lần 1 câu có ô chọn, `HIEN_TRANG.md` mục 3):**
   - *Nhịp mở phiên:* đầu phiên A bàn và chốt việc với chủ dự án trước (chưa cần bật `/swarm`); ngay khi chốt xong và có việc xây / đo / review chéo song song thì A **chủ động nhắc chủ dự án gõ `/swarm`** để A gọi `b`, `c`, `e`.
   1. Báo gọn `so_tay` + `ho_so_chu_de` đã mở ở máy demo (hướng dẫn thử `data/test_cuoi/TEST_2411_TRUA.md` mục 4–5).
   2. Đưa ảnh + hỏi gộp/mở từng bản thử (Hoàn tác · dải Trang chủ).
   3. Trình tóm tắt đọc sâu 25 repo để chọn ứng viên dựng tiếp + 5 việc nhỏ deploy.
   4. Khi chủ dự án test lại xong (không giục) ⇒ thuê GPU huấn luyện model nhận ảnh (`goi_may_thue.tar`, 93 lớp).
4. **Việc nội bộ còn nợ của A (tự làm, cần 1 phiên khác đọc diff):**
   - **Vòng cải tiến cách làm ngày 24/11 + tổng kết đợt thử 3 ngày (21–23/11):** các ứng viên & sự cố đã ghi ở `SO_CAI_TIEN_CACH_LAM.md`; xem xét thêm 6 bẫy tối+đêm 24/11 ở mục 5 dưới.
   - Đẩy và gộp nhánh dọn sổ `p15-a-don-so-2511` sau kiểm độc lập.
5. **Đầu vào vòng cải tiến từ tối+đêm 24/11 (giữ nguyên để xét, chưa bỏ):**
   - Câu hỏi có dòng mở ngoặc về việc KHÁC làm câu trả lời chủ dự án thành 3 nghĩa ⇒ một ô chọn chỉ nói MỘT việc.
   - Giao "số nguồn bấm được" khi quên quyết định đã bỏ `[n]` trong chữ (lặp lần 2 trong một buổi) ⇒ tra `HIEN_TRANG.md` mục 4 phần "Giao diện" + xem tính năng gần nhất TRƯỚC khi giao.
   - Tóm repo từ README dẫn tới nói sai thực tế code ⇒ gắn nhãn rõ "theo README, chưa đọc code".
   - Mở `so_tay` trước khi kiểm "cảnh báo an toàn của kho có tới không" (gặp lần đầu) ⇒ đưa vào bước kiểm trước khi mở tính năng viết về nơi tham quan.
   - Ghi giờ ước vào file tài liệu 3 lần (`date` trước khi ghi).
   - Nhãn ô thiếu "Kho tư liệu chưa có" nói quá về kho ⇒ chỉ dùng chữ đó khi code thật sự biết kho thiếu.
6. **Thứ đang chạy / rác / trạng thái máy (14:03 25/11/2026):**
   - 0 server, 0 cổng 80xx đang mở, 0 worktree tạm ngoài `/tmp/hr_a_don_so` của nhánh này.
   - **Qdrant đang TẮT** (`Connection refused` ở cổng `6335` lúc `13:15`) ⇒ trước khi bật server hoặc chạy việc đụng chỉ mục, chạy `docker compose up -d qdrant` và kiểm đủ **9.536 điểm**.
   - 21 thư mục clone repo ngoài `/tmp/hr_a_repo_*` và `/tmp/claude-1000/` đã mất theo lần máy khởi động lại trước `13:15`.
7. **Bẫy mới khi chuyển sang `agy` CLI + `/swarm` (25/11/2026):**
   - `scripts/commit_push.sh` từ chối symlink trỏ tới thư mục (`.agents/skills` báo `[ -d "$f" ]` đúng) ⇒ commit symlink phải stage từng file tường minh và để `.githooks/pre-commit` chạy tự nhiên (không `--no-verify`).
   - File `data/bo_nho_agent/MEMORY.md` nằm ở cây chính ngoài git ⇒ trong `workspace: "share"` hoặc worktree `/tmp/`, đọc theo đường dẫn tuyệt đối `/home/minhhieu/hue_rag/data/bo_nho_agent/MEMORY.md` nếu bản sao không có `data/`.
   - Trong `/swarm`, lệnh `kill` xoá luôn workspace của worker ⇒ chỉ `kill` sau khi nhánh đã push lên `origin` hoặc gộp vào `main`.
