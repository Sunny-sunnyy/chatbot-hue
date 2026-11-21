# STATUS_C — ghi đè 17:58 21/11/2026 (giờ `date`; phiên C mở 15:36 21/11, cả nhóm vừa soát toàn bộ file luật + trạng thái)

1. **Đang dở:**
   - Sổ việc khối A, vai "xếp nhóm lỗi" (bước 1 của bảng bước) — CHƯA bắt đầu. Điểm xuất phát đã có, đừng đọc lại từ đầu: bảng loại hỏng × model C đã đọc tay cả 24 phiên ở `data/thu_bedrock_2026-11-21/c_nguoi_dung_mo_phong/KET_QUA.md`
     mục (a); việc còn là gom từ TRIỆU CHỨNG sang NGUYÊN NHÂN, kèm số lượt từng model + mã vai / lượt + sửa ở lớp nào. Thuộc bước này: đọc tay năm chuỗi "hỏi tiếp trên con số" của mục [8] (đã chạy đủ bốn ô, cột máy sạch, CHƯA
     đọc — `data/thu_bedrock_2026-11-21/c_muc_8/so/`).
   - Sổ việc khối C mục [8] (cờ `nho_cau_tra_loi`, nhánh của B `origin/p9-b-nho-cau-tra-loi` `8a3049b`, chậm main 97 commit lúc ghi) — ĐỨNG CHỜ theo quyết định 16:14 21/11. Phần C đã đo + bảng bốn sàn + phần chưa phủ:
     `data/thu_bedrock_2026-11-21/c_muc_8/KET_QUA_MUC_8.md` (riêng tư); bảng CHƯA gửi B. Cây đo `/tmp/hr_c_nho` còn (detached, có symlink `data`).
   - Phép đếm 0 đồng "lần tìm đầu lạc đề ở lượt có lịch sử" (điều phối giao 15:13 21/11, trước khi gác) — CHƯA đếm; không nằm trong khối A ⇒ đứng chờ. Đã dò: nguồn đánh số nối tiếp qua các lần tìm
     (`backend/llm/assistant.py`, `first_id=len(trace.so_nguon)+1`) ⇒ "không trích nguồn nào ≤ 10" đọc được từ số trích trong câu trả lời.
2. **Đã soạn / đã review, chưa gộp** (đều ĐỨNG CHỜ theo quyết định 16:14 21/11): `origin/p9-c-suy-luan-dinh-tuyen` `881ddb7` (khoá mức suy luận của bước định tuyến, mặc định không đổi; bỏ nhánh nếu phiên đo thấy không khác)
   · `origin/p9-c-doi-cho-ngay` `d12c42e` (sổ việc khối C mục [11]) · `origin/p9-c-phuc-hoi-sau-kiem` `70c9f44` (hồ sơ, không gộp).
3. **Việc kế + "xong khi":** sổ việc `session_prompt/VIEC_DANG_MO.md` khối A, hàng bước 1 — bắt đầu NGAY khi mở phiên, xong khi bảng nhiều nhất sáu nhóm nguyên nhân tới phiên điều phối. Sổ việc trỏ về đây cho LỆNH CHẠY LẠI 12 VAI (việc của vai đo,
   bước 0), từ `backend/` của cây muốn đo:
   `HUE_BEDROCK_MODEL=global.anthropic.claude-opus-5-5 HUE_BEDROCK_CREDS_FILE=<đường dẫn riêng tư — data/thu_bedrock_2026-11-21/GIAO_VIEC.md> HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --no-sync --env-file ../.env python ../data/thu_bedrock_2026-11-21/c_nguoi_dung_mo_phong/chay.py <luna|s_high> <thư mục ra MỚI> [mã vai,…]`
   ⇒ ghi `<thư mục ra>/luot_<nhánh>.jsonl` + `meta_<nhánh>.json`, không ghi đè; in một phiên để đọc: từ thư mục bộ chạy `python3 xem.py <luna|s_high> V01 … [--dai N]` (đọc cứng thư mục `phien/`).
   **Hai chỗ PHẢI sửa trong `chay.py` hàm `main` trước lượt đầu (chưa sửa; sổ việc giao C sửa, vai đo chạy thử một vai mỗi nhánh):** (a) hiện chỉ có `if NHANH == "s_high": … provider = "bedrock"`; nhánh `luna` lấy nguyên cấu hình đang có — cấu hình nay là `bedrock` ⇒ chạy
   `luna` sẽ lặng lẽ thành chạy model mới, hai cột giống nhau ⇒ thêm nhánh đặt rõ `provider = "openai"`; (b) ghi đè tắt bộ nhớ đệm câu trả lời ngay trên dict cấu hình đó (`s["assistant"]["cache_cau_tra_loi"] = False`),
   không sửa `settings.yaml` ở cây chính. Sửa xong chạy thử MỘT vai mỗi nhánh và nhìn `meta_<nhánh>.json` trường `provider` trước khi chạy cả 12 vai.
4. **Ai chờ mình ↔ mình chờ ai:** phiên điều phối chờ bảng nhóm nguyên nhân (phiên sau). C không chờ ai.
5. **Câu treo:** giới hạn phép kiểm số: số model TÍNH ĐÚNG vẫn bị gỡ; số người dùng gõ không kèm đơn vị thì lời
   đính chính bị gỡ · nhánh liệt kê bài: trích "mục lục" làm mất dòng cảnh báo sinh từ nguồn bài — điều kiện trước khi bật.
6. **Thứ đang chạy / rác** (kiểm lúc ghi): 0 tiến trình, 0 cổng 80xx, 0 agent con. `git worktree list` phần của C: `/tmp/hr_c_nho` (GIỮ — mục [8]) · `/tmp/hr_c_dinh_tuyen` (nhánh chưa gộp) · `/tmp/hr_c_rv_bedrock`,
   `/tmp/hr_c_thinking` (detached, cây review / thử cũ — gỡ được) · `/tmp/hr_c_status` (nhánh sổ này). Chín cây của các nhánh đã gộp C đã gỡ lúc ghi. Thư mục `/tmp/hr_c_bedrock_doc` (không phải worktree; script chụp lời gọi) còn.
   Riêng tư dưới `data/` (không vào git, KHÔNG xoá): `thu_bedrock_2026-11-21/c_*` (mười thư mục) · `ban_cach_lam_viec_2026-11-21/C*.md`, `…/soat_toan_bo/C_danh_sach_trang_thai.md`. Tiền đo chiều 21/11: mục 5 của `KET_QUA_MUC_8.md`.
7. **Bẫy của phiên:**
   - Bộ chạy trong tiến trình (`chay.py`, `chay_8.py`): mọi CỜ lấy từ `settings.yaml` của cây đang đứng, chỉ thứ script ghi đè mới đổi ⇒ trước mỗi lượt in ra cấu hình thật đang dùng (model, cờ) rồi mới tin tên cột.
   - Đọc DIFF không thấy phần ngoài diff: hôm nay C đề nghị thêm một câu mà hai dòng ngay trên (không nằm trong diff) đã nói đủ ⇒ trước khi đề nghị THÊM chữ, grep cả file.
   - Chữ luật mới phải so với BẢNG QUYỀN chủ dự án đã duyệt, không chỉ so với nhau: một quyền ngoài bảng (tự dựng bản thử) đi qua bốn phiên đọc mới bị bắt.
   - Bảng phân loại do một người làm sau khi đã có giả thuyết: phép phân loại mù sửa "9 / 9" thành "7 + 2" ⇒ số dùng để quyết thì ghi nhãn "một người phân loại" hoặc nhờ phân loại mù.
   - Giờ ghi vào file lấy bằng `date` NGAY lúc ghi: hôm nay hai lần C ghi giờ ước lệch 2 phút, phải sửa lại.
   - Gộp main vào nhánh cũ có thể hỏng mà không báo xung đột (nhánh bỏ một dòng import, main thêm code dùng nó ⇒ 25 test hỏng) ⇒ sau MỌI lần gộp chạy lại các file test chạm đường đó.
   - Lưới chữ (regex) trên câu người dùng: loại trừ theo "chữ đứng trước" không hội tụ ⇒ dùng điều kiện dương, và cần hai lượt câu của NGƯỜI KHÁC (bộ mù + bộ sau khi đọc mẫu).
   - Tìm trong kho chỉ bằng `scripts/grep_kb.sh`, cờ viết RỜI (`-l -i -F`) — viết dính cho kết quả "0 bài" giả.
