# STATUS_B — ghi đè 18:50 21/11/2026, phiên tối 21/11 (giờ `date`; chủ dự án vắng tới 21:30)

Phiên B = phiên thực thi: viết / sửa code sản phẩm và đọc nhánh của phiên khác. Sổ việc: `session_prompt/VIEC_DANG_MO.md`; hiện trạng: `session_prompt/HIEN_TRANG.md`.
Từ dùng: *cờ* = một dòng bật / tắt trong `backend/config/settings.yaml` · *lượt thật* = gọi model thật qua code sản phẩm · *sàn* = điều kiện không được tụt · *phiên đo* = phiên chạy bộ thước trên cả hai model ·
*lần hiểu ý* = lời gọi model riêng đọc tin sửa lịch và trả danh sách hành động có tên · *bộ mù* = bộ tin thử do người không viết code soạn.

1. **Đang dở:** bản sửa số 1 của bước 4 khối A — tin vừa sửa lịch vừa hỏi (phiên điều phối giao 18:3x). Nhánh `origin/p9-b-sua-lich-kem-hoi` `8af83f0` (rẽ từ `cf1a70c3`, bản phiên đo ghim cho lượt mốc; hai commit: code + test `7ba6cfc`, report `8af83f0`),
   cờ `sua_lich_kem_hoi` TẮT, CHƯA gộp. Đã có: test 7 đạt (đã thấy đỏ) · cờ tắt giống cây chính từng byte (7 mã băm) · lượt đo 264 lời gọi trên bộ mù — model đang chạy đạt mọi dòng ghi trước; model cũ đạt phần lợi và hai sàn, dòng
   "ý sửa y như bên tắt" là CHƯA RÕ theo tiêu chí ghi trước · một chuỗi qua đường chat thật mỗi model đạt. CÒN: phiên C đọc diff + chạy phép đóng dòng "chưa rõ" (4 tin chỉ sửa × 10 mỗi bên, model cũ) ⇒ phiên điều phối gộp cờ tắt ⇒ nhìn giao diện ⇒ quyết bật.
   Report đủ: `report_agent/2026-11-21/b_sua_lich_kem_hoi.md` (trên nhánh). Số, tiêu chí, dữ liệu thô (riêng tư): `data/thu_bedrock_2026-11-21/b_buoc_4/kem_hoi/` (`TIEU_CHI.md`, `KET_QUA.md`, `luot_1/`, `luot_2_lap_M16_M01/`, `chuoi_route/`).
   Bốn nhánh code cũ của B vẫn ĐỨNG CHỜ, chưa gộp: `p9-b-vong-cuoi-chi-viet` `e9a14c12` (đã đẩy, origin khớp máy) · `p9-b-vong-cuoi-chu-2` `13efd6f3` · `p9-b-cong-cu-ban-2` `5eecd76f` · `p9-b-nho-cau-tra-loi` `8a3049b6`.
2. **Đã soạn / đã review, chưa gộp:** nhánh tài liệu này (`p9-b-status-toi-2111`, chỉ file này) chờ một phiên khác đọc rồi gộp. B đã ĐỌC và trả kết quả: `origin/p9-e-trang-theo-doi` (trang theo dõi — một điểm major nhỏ về cột "Lỗi", phiên đo đã sửa ở
   `3c226787`, B chạy lại và kết luận gộp được; file review riêng tư `data/thu_bedrock_2026-11-21/b_review_e/TRANG_THEO_DOI.md`) · commit cuối của nhánh bỏ dòng ghi nguồn bản đồ (đã gộp). B sẽ là người đọc bản sửa số 2 do phiên C viết (chặn lời gọi công cụ trùng + dòng trạng thái của công cụ khoảng cách).
3. **Việc kế + "xong khi":** (a) trả lời phiên C nếu review bản sửa số 1 có điểm cần sửa — tái hiện từng điểm trước khi sửa; (b) đọc bản sửa số 2 của phiên C khi có nhánh; (c) bản sửa kế của bước 4 do phiên điều phối chọn sau lượt mốc.
   Khi một nhánh đứng chờ được mở lại: gộp main mới nhất vào nhánh, chạy lại phép "cờ tắt giống từng byte" và các file test chạm đường đổi TRƯỚC mọi bước khác.
4. **Ai chờ mình ↔ mình chờ ai:** B chờ phiên C (đọc `7ba6cfc` + phép × 10) và phiên điều phối (gộp, xếp lượt nhìn giao diện). Phiên C chờ B đọc bản sửa số 2 khi viết xong. Không ai khác đang chờ B.
5. **Câu treo:** B không có câu nào cho chủ dự án. Đã nêu phiên điều phối, do phiên điều phối cân: bật cờ `sua_lich_kem_hoi` là đổi chữ người dùng thấy ở lượt sửa lịch (B coi là sửa lỗi đã tái hiện) · bản nháp thiết kế mục [7] "agent đề xuất sửa kho":
   B đề nghị cửa "tự kiểm" kiểm tại chính link nguồn bài đã ghi trước khi tìm web (tải trang là một đường ra mới — xét có thuộc hàng "hỏi trước" không). Còn nguyên từ phiên trước: hook quét trùng + `Session_Prompt.md` §5 chờ chữ "được" của chủ dự án; lý do của luật cứng 3 trong `AGENTS.md` còn nhắc "bộ câu mẫu".
6. **Thứ đang chạy / rác:** 0 tiến trình, 0 server, 0 agent con của B; B không bật container nào. Worktree của B (`git worktree list` lúc ghi): `/tmp/hr_b_kemhoi` (`p9-b-sua-lich-kem-hoi`; có ba symlink `data`, `knowledge-base-hue`, `frontend/dist` trỏ về cây chính — không commit) — GIỮ tới khi gộp ·
   bốn worktree nhánh đứng chờ `/tmp/hr_b_bac1`, `/tmp/hr_b_ban2`, `/tmp/hr_b_chu2`, `/tmp/hr_b_nho` — GIỮ · `/tmp/hr_b_status` (nhánh này) gỡ sau khi gộp. Đã gỡ trong phiên: `/tmp/hr_b_quyen`, hai worktree review trang theo dõi.
   `/tmp` bị dọn cũng không mất gì (mọi commit ở nhánh cùng tên). File riêng tư B tạo phiên này, GIỮ: `data/thu_bedrock_2026-11-21/b_buoc_4/` (`LOP_SUA.md` — bảng loại hỏng ↔ bản sửa đã có trên main; `kem_hoi/`), `…/b_review_e/`, `…/tools/b_do_kem_hoi.py`, `…/tools/b_chuoi_kem_hoi.py`.
   Tiền B tiêu phiên tối 21/11 theo file kết quả: Bedrock 1,53 USD (lượt đo 132 lời gọi + 2 lời gọi thử) + 0,07 USD (chuỗi qua đường chat) · OpenAI 0,017 USD. B đã ước lượt đo 0,5–1 USD — thấp hơn số thật.
7. **Bẫy của phiên:**
   (a) Ước tiền lời gọi hiểu ý trên model đang chạy: mức suy luận high ⇒ khoảng 0,011 USD mỗi lời gọi (không phải cỡ lời gọi của model cũ); chạy thử vài lời gọi rồi mới báo con số ước.
   (b) B trả lời phiên điều phối theo trí nhớ rằng nhánh vòng-cuối có sẵn phần "chặn lời gọi trùng" — sai (nhánh có ba cờ `vong_cuoi_chi_viet`, `bao_het_luot_tim`, `khoang_cach_trang_thai`; phần chặn trùng đã bị bỏ ở plan); mở lại diff rồi đính chính ở tin kế. Nói về nhánh cũ thì grep trước.
   (c) Mốc nhiễu tính từ BA lượt lặp bên tắt ra 0 trong khi 10 lượt lặp cho thấy bên tắt tự khác mình 2–3 / 10 ⇒ tiêu chí "y như bên tắt" phải ghi mốc nhiễu từ ít nhất 10 lượt, hoặc so với đáp án ghi sẵn thay vì so hai bên với nhau.
   (d) `pkill -f <tên script>` giết luôn chính lệnh shell đang gọi nó (dòng lệnh chứa chuỗi đó); dừng tiến trình nền của mình bằng mã tiến trình.
   (e) Chạy script để trong `/tmp` bằng `python <đường dẫn>` thì thư mục của script (không phải `backend/`) vào đường tìm module ⇒ `No module named 'llm'`; đặt `PYTHONPATH=$PWD` hoặc đưa code qua đầu vào chuẩn.
   (f) Còn hiệu lực từ trước: `scripts/grep_kb.sh` nhận cờ TÁCH RỜI (`-i -l`) · đổi nhà cung cấp model thì in thân gửi thật của lượt CÓ lịch sử · nhánh mô tả công cụ bản 2 và nhánh vòng-cuối cùng sửa dòng công cụ ngày lịch trong `_assistant_for` ⇒ nhánh gộp sau có một chỗ ghép một dòng ·
   chạy test trong worktree: `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv run --no-sync …` + nối ba symlink (dòng "Quan sát môi trường" của sổ việc) · câu luật nào TRAO quyền phải kèm lời chủ dự án + giờ.

Sổ cũ nguyên văn: `git log -p -- session_prompt/sessions/STATUS_B.md` và `session_prompt/archive/STATUS_B_LICH_SU_*`.
