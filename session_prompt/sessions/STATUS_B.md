# STATUS_B — ghi đè 17:58 21/11/2026, sửa mục 2, 5–7 lúc 18:11 21/11/2026 — KẾT PHIÊN theo lời chủ dự án (giờ `date`)

Phiên B = phiên thực thi: viết / sửa code sản phẩm và đọc nhánh của phiên khác. Sổ việc: `session_prompt/VIEC_DANG_MO.md`; hiện trạng: `session_prompt/HIEN_TRANG.md`.
Từ dùng: *cờ* = một dòng bật / tắt trong `backend/config/settings.yaml` · *lượt thật* = gọi model thật qua code sản phẩm · *sàn* = điều kiện không được tụt · *phiên đo* = phiên chạy bộ thước trên cả hai model.

1. **Đang dở:** KHÔNG có việc xây nào đang dở. Việc đầu của B = khối A của sổ việc (đuổi một con số sản phẩm); vai của B trong bảng bước: **bước 4** — sửa lần lượt hai nhóm lỗi đứng đầu (nhóm lỗi nằm ở phần
   phiên C viết thì C sửa), và ĐỌC bản sửa không do B viết. B không nhận bước 2 (soát tích hợp) cho các nhánh chính B viết ngày 21/11 (lớp nối model mới, công cụ liệt kê bài, sửa lịch buổi tối). Trong lúc chờ: chỉ
   việc 0 đồng (đọc, đếm, nêu hướng). Bốn nhánh code của B đều **ĐỨNG CHỜ theo quyết định 16:14 21/11** (chỉ làm tiếp khi nằm trong hai nhóm lỗi đầu — khối A, dòng "Ba việc ĐỨNG CHỜ"), CHƯA gộp:
   - `p9-b-vong-cuoi-chi-viet` — origin `d1e8ac93`; ở máy `e9a14c12` CHƯA đẩy (đã gộp main lúc đó + ghép với công cụ liệt kê bài). Ba cờ tắt. Bản chữ 1 của dòng báo hết lượt tìm không đạt sàn câu ngoài tỉnh (số ở sổ việc).
   - `p9-b-vong-cuoi-chu-2` `13efd6f3` = `d1e8ac93` + một commit thêm vế "Bằng chứng không nói về điều được hỏi thì trả câu không đủ thông tin" vào hai dòng báo. Phiên đo đã đo xong, kết quả CHƯA ai đọc.
   - `p9-b-cong-cu-ban-2` `5eecd76f` — mô tả công cụ bản 2 sau khoá `assistant.cong_cu_ban` (đang đặt 1); `tests/test_cong_cu_ban.py` 10 đạt; khoá = 1 giống từng byte bản chụp trước khi sửa. Lượt thật CHƯA chạy lượt nào
     (script + tiêu chí riêng tư: `data/thu_bedrock_2026-11-21/tools/b_do_cong_cu_ban.py`, `…/ket_qua/b_cong_cu_ban/TIEU_CHI.md`). Report trên nhánh: `report_agent/2026-11-21/b_cong_cu_ban_2.md`.
   - `p9-b-nho-cau-tra-loi` `8a3049b6` — cờ `nho_cau_tra_loi` tắt; phần còn lại ghi ở khối C mục [8] của sổ việc.
2. **Đã soạn / đã review, chưa gộp:** chỉ nhánh `p9-b-quyen-ban-thu` (trả quyền tự dựng bản thử vào `AGENTS.md` + `START_SESSION.md` theo lời chủ dự án 18:04; phiên C đã đọc READY trên `4e7ef4b`, gồm cả câu "người đọc chạy lại lệnh kiểm của một dòng xong" trong skill review; chờ phiên điều phối gộp). B đã ĐỌC nhánh
   `p9-e-bo-dong-ghi-nguon-ban-do` `d138b68` (bỏ dòng ghi nguồn trên hai bản đồ) — [chỉ đọc code, CHƯA chạy gì]: gộp được; hai điểm nhỏ đã gửi phiên đo: `bai_hoc/VIEC_MOI_XONG.md` dòng 252 còn
   nói "dưới bản đồ có dòng chữ nhỏ ghi nguồn" · chú thích và lề dưới 60 px ở `BanDoLich.jsx`, `TrangBanDo.jsx` là của dòng đã bỏ. Nhánh đó còn chờ lượt nhìn trình duyệt + dựng lại dist cây chính. Mọi nhánh luật / skill / hướng dẫn B viết chiều 21/11 đã ở main (nhánh cuối: `p9-b-soat-luat-huong-dan`
   `6960e3f7`, nằm trong main `83bbb54a`).
3. **Việc kế + "xong khi":** khối A của sổ việc, bước 4 — "xong khi" và luật đo ghi ở đó. Khi một nhánh đứng chờ được mở lại: gộp main mới nhất vào nhánh, chạy lại phép "cờ tắt giống từng byte" và các file test chạm đường
   đổi TRƯỚC mọi bước khác.
4. **Ai chờ mình ↔ mình chờ ai:** B chờ phiên điều phối giao bước 4; quyết định đang chờ là "sửa hai nhóm lỗi nào trước" (kết quả bước 1 của khối A). Không ai đang chờ B review.
5. **Câu treo:** mọi câu chờ chủ dự án nằm ở `HIEN_TRANG.md` mục 3 — gồm các câu gác 21/11 từ việc của B (câu "có cho một phiên tự dựng bản thử không chờ giao không" chủ dự án ĐÃ trả lời 18:04 21/11: "có nhé" — trần ghi ở
   `AGENTS.md` mục "Cách nhìn việc"; B chưa dựng bản nào). Việc của B đang CHỜ chữ "được" của chủ dự án, chưa sửa gì: hook quét trùng + `Session_Prompt.md` §5 theo đề xuất nhóm 21/11 (chặn cứng câu kín; thôi chặn chép kho /
   câu mẫu vào tài liệu; máy quét file kho mới với câu mẫu + câu kín thay bước quét tay) — thử hook bằng ca cố ý vi phạm. Của B, chưa ghi ở chỗ nào khác (đã nêu phiên điều phối; B không sửa vì là luật cứng): lý do của luật cứng 3 trong `AGENTS.md` còn nhắc "bộ câu mẫu" dù bộ câu mẫu đã
   vào repo công khai từ 20/11.
6. **Thứ đang chạy / rác:** 0 tiến trình, 0 server, 0 agent con của B; container B không bật cái nào (Qdrant của dự án `hue_rag-qdrant-1` đang chạy, không phải do B bật — không đụng). Worktree của B (`git worktree list` lúc ghi) — GIỮ vì nhánh đứng chờ: `/tmp/hr_b_bac1` (`p9-b-vong-cuoi-chi-viet` `e9a14c12`),
   `/tmp/hr_b_ban2` (`p9-b-cong-cu-ban-2` `5eecd76f`), `/tmp/hr_b_chu2` (`p9-b-vong-cuoi-chu-2` `13efd6f3`), `/tmp/hr_b_nho` (`p9-b-nho-cau-tra-loi` `8a3049b6`); `/tmp/hr_b_quyen` (nhánh `p9-b-quyen-ban-thu`, luật về bản thử tự dựng) gỡ sau khi gộp. `/tmp` bị dọn
   cũng không mất gì: mọi commit nằm ở nhánh cùng tên của kho chính (dựng lại: `git worktree add /tmp/hr_b_bac1 p9-b-vong-cuoi-chi-viet`). Thư mục riêng tư B tạo, GIỮ: `data/thu_bedrock_2026-11-21/tools/b_*.py`,
   `…/ket_qua/b_*`, `…/b_review_c/`; `data/ban_cach_lam_viec_2026-11-21/B.md` và `…/soat_toan_bo/B_luat_huong_dan.md`. Cần chạy model đang dùng: đường dẫn file khoá lấy theo `HIEN_TRANG.md` mục 1, đặt vào biến
   `HUE_BEDROCK_CREDS_FILE` ngay trên dòng lệnh, không in nội dung. Tiền B tiêu 21/11 theo file kết quả: từ 15:36 là 0 USD; trước đó 5,71 USD có ghi (lịch sử tách lượt 0,28 · sửa lịch buổi tối 0,82 · công cụ liệt kê 3,21 ·
   nhớ câu trả lời 1,40) + khoảng 1,75 USD ước cho 56 lượt không ghi tiền.
7. **Bẫy của phiên:**
   (a) Chiều 21/11 nhóm — B có đọc và đồng ý — đã viết vào `AGENTS.md` một quyền chủ dự án chưa hề chọn (tự dựng bản thử không chờ giao); phiên điều phối bắt được, B gỡ ở `6960e3f7`; tới 18:04 chủ dự án mới trao quyền đó, B ghi lại vào luật kèm lời và giờ. Câu luật nào TRAO quyền phải kèm
   lời chủ dự án + giờ; không có thì là đề nghị, ghi ở `HIEN_TRANG.md` mục 3.
   (b) Gọt luật có thể THÊM nghĩa: B lỡ thêm `data/` vào danh sách "sao lưu trước khi sửa / xoá" (ngược lựa chọn 20/11) và làm rơi một điều kiện khi gộp hai câu của skill review ⇒ đọc diff bản gọt theo cả hai chiều
   (chữ mới thêm, điều kiện bị mất).
   (c) Hai lần ghi vào lời commit "cỡ không tăng" khi thật ra tăng 10–31 byte; ba lần hụt mốc byte được đặt ⇒ chạy `wc -c` trước khi viết câu khẳng định; hụt mốc thì báo số thật, không cắt luật đang dùng cho đủ số.
   (d) Thêm một lần ghi giờ bằng tay (file riêng tư) — giờ ghi vào file lấy bằng `date`.
   (e) Còn hiệu lực từ sáng 21/11: `scripts/grep_kb.sh` nhận cờ TÁCH RỜI (`-i -l`); viết dính `-il` thì script dừng và phép đếm ra số 0 giả · đổi nhà cung cấp model thì in thân gửi thật của lượt CÓ lịch sử, không chỉ
   lượt đầu (`backend/llm/bedrock_model.py`) · số đổi theo giờ không được nằm trong thứ được nhớ (mục [8]) · nhánh mô tả công cụ bản 2 và nhánh vòng-cuối cùng sửa dòng công cụ ngày lịch trong `_assistant_for` của
   `backend/llm/generator_openai_full_corpus.py` ⇒ nhánh gộp sau có MỘT chỗ ghép một dòng · chạy test trong worktree: dòng "Quan sát môi trường" của sổ việc.

Sổ cũ nguyên văn: `git log -p -- session_prompt/sessions/STATUS_B.md` và `session_prompt/archive/STATUS_B_LICH_SU_*`.
