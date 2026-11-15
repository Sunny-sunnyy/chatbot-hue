# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 22:35 14/11/2026 (A, kết phiên tối 14/11). Trước: 17:40 14/11/2026 (A, kết phiên chiều 14/11). Trước: 09:45 14/11/2026 (A, mở phiên 14/11). Trước: 22:40 13/11/2026 (A, kết phiên 13/11).
Nguyên văn handoff trong phiên 13/11 (mọi quyết định theo giờ, bàn nhóm, vòng tự soi 1): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-13.md`; 12/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-12.md`. Nhật ký: `bao_cao_he_thong/nhat_ky/2026-11-13_lich_trinh_kho_3.md`.

## PHIÊN 15/11 (mở 09:33 15/11/2026)

- Terminal: A `hue-rag-26` · B `hue-rag-b2` · C `hue-rag-f9` · E `hue-rag-3e` — cả bốn Claude Code, trực tiếp; D không mở. Kiểm nhanh khớp (main `6c7c01b`, hooks, Qdrant 1 collection 9.425).
- **Quyền phiên 15/11 (User chọn "như tối 14/11", A ghi nhận 09:38 15/11/2026):** A tự điều phối, A commit / push, B / C / E push nhánh riêng, tự tra / cào / ghi kho / ingest, không hỏi khi User vắng, tiền không trần cứng nhưng dùng hiệu quả. Hết hạn cuối phiên.
- Giao 09:38: **B** mục 0 đo bù 65 câu · **C** việc 3(iii) đếm bữa vùng nam xa (0 USD) · **E** rảnh, chờ câu User về 14 bài trống ảnh / câu (a).
- Câu User thêm (từ E): 14 bài trống ảnh — chấp nhận ô màu hay tìm tay; có ghi luật chọn ảnh vào luật chung không.
- **Xong 09:41 — B đo bù 65 câu: ĐẠT** (từ chối 2 ⇒ 1, 0 lỗi trích dẫn, 56 cùng ý + 1 tốt lên; 0,029 USD; A tính lại khớp). Kết luận "không tụt" của ghi kho 4–6 giờ đúng trên mọi câu đổi top 10 ⇒ mục 0 "Việc đầu phiên sau" ĐÓNG. Mẫu TIEU_CHI ghi kho: câu chạm = mọi câu đổi top 10 (B sửa `cau_cham.py` ở lần ghi kho kế).
- **C 3(iii) đếm nam xa: không cào quán** (4,8 % bữa; kho: không quán). A duyệt ghi chú ăn uống 2 điểm ở thẻ bữa (0 USD) ⇒ E review.
- **(a) ngưỡng mưa:** User chọn PA3 nhưng hỏi "số nghĩa là gì / nhóm bàn chưa / sao không dùng API thời tiết Huế" ⇒ A giải thích (đã dùng Open-Meteo), chờ User xác nhận lại rồi mới giao C.
- **User trả lời (A ghi 10:15 15/11/2026):** (a) ngưỡng mưa: chưa chốt — "trao đổi nhóm / Codex tra xem đâu là ngưỡng" ⇒ B tra + so 3 model Codex (sol / terra / luna, chấm mù) ⇒ C, E phản biện ⇒ A trình một khuyến nghị · (c) Codex: User muốn mặc định terra hoặc luna, sol chỉ cho nghiên cứu sâu ⇒ chờ kết quả so 3 model · (b) **bàn thiết kế trang khách sạn theo khu + hỏi ngân sách chỗ ở** (C viết plan 1 trang, B / E phản biện, trình User trước khi code) · (g) 14 bài trống ảnh: **E tìm thêm một lượt** (dừng 30 phút không thêm), còn thiếu ⇒ danh sách cho User tự tìm · (d) **W76–W78 duyệt ⇒ áp** · (f) **dọn nhánh + 4 worktree AGY: xoá** (lệnh `/tmp/don_nhanh_15_11.sh`, User `!`) · (e) nhớ sở thích: User chưa chọn bàn.
- **User chốt (A ghi 10:28 15/11/2026):** (a) **ngưỡng mưa = xếp lại lịch khi ≥ 60 % VÀ ≥ 6 mm** (đầu cấp "Mưa" QCVN 84:2024 Phụ lục B — A mở văn bản gốc kiểm); dòng "Nếu mưa" giữ ≥ 60 % · (c) **Codex mặc định `gpt-6.1-terra` medium**, sol chỉ khi sâu (script + `Session_Prompt.md` §9 đã sửa) · (b) **plan khách sạn bản 2 DUYỆT sha `b5d8bc184090`**: cả hai, ngân sách trước; trang chỉ mở từ ô "Nơi ở".
- Giao 10:28: **C** ngưỡng 6 mm (nhánh nhỏ) ⇒ rồi trang chỗ ở (bảng v3: gộp La Perle, Places 2 cơ sở) · **B** nhánh ngân sách (5 chỗ chạm B đã liệt kê) · **E** review cả hai + ảnh 14 bài. **Máy:** A docker-images-src bật bộ Capitol (~5–6 GB, 15–20 phút) từ 10:27 ⇒ nhóm không chạy test rộng / server / Playwright tới khi A báo xong.

- **Việc tiếp (bàn nhóm, User chốt 11:12 15/11/2026):** đếm 0 USD xong — kho tự mâu thuẫn: Bảo tàng Cổ vật đã khớp; **Tây Sơn 1786 ↔ 1788 còn lệch ⇒ User duyệt "ghi cả hai mốc"** (C sửa 2 câu / 2 bài, sao lưu `meta/`, E review diff trước dựng, dựng lại, đo câu đổi top 10) · tốc độ: đường tìm thêm 20,6 % lượt (83 / 402, chữ đầu p50 ~7–9 s), câu thường p95 5,9 s (B đếm, E tính lại khớp) ⇒ **User duyệt "viết plan, đo mốc trước"** (B viết plan; đo mốc chỉ SAU khi dựng chỉ mục xong — không đo latency chồng việc nặng).

### Vòng tự soi 1 — phiên 15/11 (A chốt 10:55 15/11/2026; B, C, E đều gửi)
**Áp ngay trong phiên** (làm nhẹ, không hạ sàn; kết phiên A đề xuất thành luật qua `improve-workflow`):
1. Cổng server thật sau merge **chỉ khi nhánh chạm đường chat / model, route API, hoặc cấu hình nạp lúc khởi động**; nhánh chỉ đổi ảnh / chữ / hằng số thuần / giao diện tĩnh ⇒ build + test file chạm (C, E).
2. Người review **không chạy lại test** người làm đã chạy, trừ nhánh đổi cờ `settings.yaml` (luật có / không env) (E, B). Nhánh hàm thuần ≤ ~30–50 dòng có mô phỏng 3.840 khung ⇒ đọc diff + dữ liệu.
3. Biên bản review nhánh ≤ ~50 dòng code: **≤ 5 dòng** (kết luận · đã đọc gì · finding) (E).
4. Plan nhẹ (≤ 0,2 USD): **một** người phản biện (C).
5. Playwright: tác giả chạy một lần; không chạy cho thay đổi chỉ một đoạn chữ (B, C).
6. So nhiều model / chấm mù: **chỉ khi đổi mặc định**, không lặp cho mỗi đề (cả nhóm).
7. Finding về "chuỗi gửi model" phải chỉ ra hàm dựng chuỗi đó (B — 1 major sai lượt plan).
8. Số trong plan **đếm trên khung thật**, không ước bằng tổ hợp (C: "12 ⇒ 36 cơ sở" thật ra 13 ⇒ 32 — A đã chuyển số chưa kiểm cho User, đính chính).
**A tự nhận:** xin thêm bảng 5 ↔ 6 mm trên 2 thước sau khi nhóm đã chốt — không đổi kết luận (C); mở vòng tự soi muộn (~10:53).
**GIỮ (bắt lỗi thật):** review đọc DỮ LIỆU (câu Bạch Mã rộng hơn kho, nhãn "1 sao" gồm Đạt chuẩn, trưa Nhị Hồ 0 / 3.840, La Perle trùng, key "Như Phú") · người thứ hai nhìn ảnh (Kỳ yên) · mở trang nguồn đọc chú thích ảnh · liệt kê mọi chỗ chạm khi thêm trường qua sửa lịch · thước so cố định, không trùng ngưỡng đang thử · đếm trước khi xây (nam xa) · băm 3.840 khung "không chọn ⇒ như cũ" · đo bù câu đổi top 10.

## PHIÊN SAU ĐỌC TRƯỚC (A viết 22:35 14/11/2026, KẾT PHIÊN TỐI 14/11 — User: "để các nhiệm vụ, câu hỏi cho session tiếp theo")

**Phiên tối 14/11 đã kết** (mở 17:45, User vắng từ 17:49, về lúc kết phiên). A `hue-rag-fb` · B `hue-rag-62` · C `hue-rag-eb` · E `hue-rag-1f`, cả bốn Claude Code (Opus 5.5), trực tiếp; D không mở. **Quyền phiên HẾT HẠN** ⇒ A mới hỏi lại User một câu (tối 14/11 có: "như 14/11" = A tự điều phối, A commit / push, B / C / E push nhánh riêng, tự tra / cào / ghi kho / ingest, không hỏi khi User vắng, tiền không trần cứng nhưng dùng hiệu quả). Mỗi session đọc mục đầu `sessions/STATUS_<X>.md` "PHIÊN SAU ĐỌC TRƯỚC". **D** (học cùng User, chưa mở 14/11): gợi ý bài để giảng khi User muốn — `bai_hoc/22` (6 lần ghi kho, hỏi thử trước khi viết), `25` (khách sạn chọn theo hạng, quán, mục web), `24` (ảnh: người giao nhìn lại 100 %); không có STATUS_D — tạo từ mẫu `sessions/README.md` khi mở. Nguyên văn phiên tối (quyết định theo giờ, tiến độ, vòng tự soi 1): `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-14_toi.md`; phiên sáng + chiều: `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-14.md`. Nhật ký: `bao_cao_he_thong/nhat_ky/2026-11-14_ghi_kho_3_bai.md`.

### Hệ thống lúc kết phiên (main đã push — xem `git log -1`; mọi nhánh tối nay đã merge)
- **Kho: 263 file / 9.425 đoạn** (record `af5e225c497e`, sparse `4888dc70d01f`, T1 `aa34d4215f15`; Qdrant 1 collection 9.425 điểm). Tối nay 3 lần ghi (cả ngày 6 lần, 204 ⇒ 263): **lần 4** 8 quán (Thủy Xuân / Kim Long / Đầm Chuồn) · **lần 5** 10 món (tré, vả trộn, tôm chua, mít trộn, bánh in, rượu Minh Mạng, cháo hến, cơm sen, nem công chả phượng, bánh su sê) + 13 địa điểm / di tích (chùa Báo Quốc, nhà thờ Phủ Cam, Cồn Hến, chùa Thuyền Tôn, phủ Tuy Lý Vương, làng nón Tây Hồ, làng Kim Long, chùa Quốc Ân, Thành Lồi, chùa Ba La Mật, cầu Bạch Hổ, Lục Bộ, cầu Dã Viên) · **lần 6** 13 lễ hội / phong tục (Tết, cúng Âm hồn, Trung thu, Vu Lan, Đoan Ngọ, Truyền Lô, diều, tế Thai Dương phu nhân, Ariêu Ping, Tiến Xuân ngưu, chẩn tế, Thanh minh Phù Bài, Kỳ yên) + 3 nghệ thuật (hò Huế, lý Huế, ca kịch Huế). Chọn bài bằng **hỏi thử trợ lý trước** — chỉ viết thứ bị từ chối / trả lời mỏng. Mỗi lần: câu chạm không tụt, ngoài kho 0 / 18, an toàn 32 không đổi lớp, câu thử 100 % trả lời bằng bài mới. Report `report_agent/2026-11-12_ra_khoang_cach/b_ghi_kho_{4,5,6}_implementation.md`.
- **Ảnh:** Khám phá **249 / 263** (hiện cạnh câu trả lời **196**, `kc` 53 gồm 20 ảnh bài chủ đề); 14 bài trống có lý do (report `e_anh_v4*`, `e_anh_nang_kc`, `e_anh_kho5`, `e_anh_kho6`). Lịch **33 / 34** (Thuận An: ảnh duy nhất có trẻ em đồ bơi ⇒ bỏ). Thẻ bữa có ảnh quán (quán kho + 5 quán bản đồ mở từng hiện).
- **Lịch — quán:** bảng quán 468 dòng (md5 `ab481586d46f`); bữa có quán kho **69,1 %** (Thủy Xuân 62,6 · Kim Long 57,2 · biển / đầm 48,5 · nam xa 0); bỏ 1 quán đã đóng (hiện 324 / 3.840 lịch).
- **Lịch — khách sạn:** `chon_co_so` hạng cao trước (trước theo tên abc ⇒ 5 sao 0 / 6.108 lượt cao cấp) ⇒ 3.036 / 3.036 lịch trung tâm có 5 sao + 3 sao; ảnh **71 / 140** (97,6 % ô hiện ra có ảnh); link Bản đồ + Tìm phòng; toạ độ Places 82 / 140; bảng `data/khach_san_2026-11-14/bang_luu_tru_lich_v2.json` (md5 `039c3adebb9b`); test "mọi đường ảnh có file". Chỉ ~12 / 140 cơ sở từng hiện trong lịch.
- **Mục web:** luật số ngoài đoạn trích cho qua **năm** 19xx / 20xx người dùng gõ (giờ / ngày / số nhà / tiền vẫn chặt) ⇒ bị thay câu cố định 21 ⇒ 10 / 76.
- **Bài học + sổ:** `bai_hoc/01`, `22` (lần 4–6), `24`, `25` cập nhật, mỗi lần agent con kiểm độc lập (biên bản `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_*`); sổ `02`, `07`, `01`, README, nhật ký.
- **Đếm rồi không làm:** mưa — thêm điểm trong nhà cứu ~3,6 %, đổi ngày ≤ 13,7 % (mùa mưa 8–21 %) (`report_agent/2026-11-12_ra_khoang_cach/c_dem_mua.md`) · thẻ chọn chỗ theo ngày / buổi (log 20 dòng, dưới ngưỡng) · nhãn xác minh / bản đồ đồng bộ (thấp).
- **Codex:** gói ChatGPT của User **hết lượt lúc 19:12** (thông báo "try again at 8:38 PM") — nhóm chuyển Serper + tự đọc trang từ đó.
- **Tiền tối nay (ước, cộng tin báo, CHƯA review):** B ≈ 0,45 · E ≈ 0,18 · C ≈ 0,10 · A ≈ 0,01 ⇒ **≈ 0,75 USD**; cả ngày 14/11 ≈ 2,45; Phase 9 ≈ 7,1 (không trần cứng theo lời User).

### Việc đầu phiên sau — THEO THỨ TỰ
0. **B — ĐO BÙ ghi kho 4 / 5 / 6 (không cần User, làm ngay khi giao, ≈ 0,02 USD):** luật "đo đúng chỗ đổi" (User 15:03 14/11) tính câu chạm = **mọi câu có top 10 T1 đổi**, nhưng TIEU_CHI kho 4–6 (chép kho 3) chỉ chạy lại câu có ĐOẠN BÀI MỚI trong top 10 ⇒ đã bỏ sót: kho 4 đổi 9 chạy 3 · kho 5 đổi 35 chạy 3 · kho 6 đổi 42 chạy 2 (đổi do trọng số từ khoá ⇒ ngữ cảnh gửi model khác). Chạy 1 lượt Golden trên **65 / 158 câu** có top 10 hiện tại khác lượt đủ 176 câu sau ghi kho 2 (B đếm 0 USD lúc kết phiên; danh sách `data/sua_kho_2026-11-14_ghi_kho_6/bu_doi.json`; 0 câu ngoài kho trong tập; ×1 ≈ 0,02 USD, ~3 phút, 0 server). **Lệnh:** viết script / lệnh MỚI, kết quả vào thư mục mới `data/sua_kho_2026-11-14_do_bu/` — KHÔNG dùng `data/sua_kho_2026-11-14_ghi_kho_6/tools/do_sau.sh` (không nhận danh sách câu, lấy từ `cau_cham.json`, ghi đè `ghi_kho_6/sau/`). Chỉ 65 câu Golden: an toàn 32 + 18 ngoài kho đã chạy trên đúng kho 6 (0 đổi lớp, 0 / 18) ⇒ không chạy lại. Mốc = lượt đủ 176 câu sau ghi kho 2 (`data/sua_kho_2026-11-14_ghi_kho_2/sau/golden.jsonl`) — gồm cả đổi do kho 3, cố ý (kho 3 cũng chỉ chạy 2 câu chạm). Sàn như TIEU_CHI (từ chối nhầm ≤ mốc + 1, 0 lỗi trích dẫn mới); "câu đổi" = chữ trả lời khác mốc ⇒ agent con chấm mù cùng ý / khác ý. Không đạt ⇒ báo A (A xem câu tụt; lui = gỡ bài gây tụt + dựng lại, sao lưu `meta/`); sửa mẫu TIEU_CHI ghi kho: câu chạm = mọi câu đổi top 10. Kết luận "không tụt" của 3 lần ghi tối 14/11 hiện **chỉ đúng trên câu có đoạn bài mới**. Xong ⇒ A sửa `bai_hoc/22` + sổ `02` theo số mới. (B tự bắt lúc kết phiên; C phản biện; lệnh mẫu sai do agent con đọc thử bắt.)
1. **A:** hỏi quyền phiên (một câu) ⇒ cùng lượt giao việc có sẵn (mục 3). Rồi hỏi User các câu dưới, **mỗi lần một câu**, đáp án = đa số nhóm (đã bàn):
   - (a) **Ngưỡng mưa của lịch** — số: `report_agent/2026-11-12_ra_khoang_cach/c_dem_mua.md` phần 3–4 (ERA5: hiện hành báo 218 ngày, đúng 56 %, thừa 96; ≥ 60 % & ≥ 5 mm báo 111, đúng 86 %, thừa 16, sót 23 %). **Khuyến nghị phương án 3** (B, C, E): xếp lại lịch khi ≥ 60 % VÀ ≥ 5 mm; dòng "Nếu mưa" giữ ≥ 60 % (27 / 29 ngày bỏ sót vẫn có nhắc). Đổi spec đã duyệt ⇒ cần User. Code: dict `mua` đưa vào `xep_v2` ở `backend/llm/len_ke_hoach.py` (~dòng 88); dòng "Nếu mưa" đọc db ≥ 60 % (~dòng 57) — không chạm. 1 hằng số + test, 0 USD.
   - (b) **Trang / danh sách khách sạn theo khu** — 71 ảnh khách sạn nhưng lịch chỉ gợi ~12 cơ sở ⇒ phần lớn chưa có chỗ hiện. Làm hay không (chưa bàn nhóm — bàn trước khi hỏi).
   - (c) **Giới hạn Codex cho agent** — gói ChatGPT của User hết lượt tối 14/11; đề xuất: agent ưu tiên Serper cho lượt tra hàng loạt, Codex cho câu tra sâu; hoặc trần N lượt / phiên.
   - (d) **Vòng cải tiến 31** (`SO_CAI_TIEN_CACH_LAM.md`, W76–W78) — mỗi lần một câu.
   - (e) **Nhớ sở thích có kiểm soát** (đợt agent kế — các ứng viên khác đã đếm / gác) — dữ liệu người dùng mới, đụng `nho_cau_tra_loi: false`.
   - (f) Dọn nhánh (lệnh dưới, User `!`) + 4 worktree antigravity-cli (`~/.gemini/antigravity-cli/.../worktrees/subagent-Monuments-Reviewer-*`) — giữ hay `git worktree remove`.
2. **Theo câu trả lời:** (a) đồng ý ⇒ C (đã đếm) code nhánh nhỏ ⇒ E review ⇒ A merge; (b) đồng ý ⇒ bàn nhóm thiết kế ⇒ plan.
3. **Việc có sẵn, không cần User:** (i) 14 bài Khám phá còn trống ảnh + 53 `kc` — chỉ làm khi có nguồn mới (Codex đã hồi lượt), dừng nếu 30 phút không thêm được; (ii) **ý chờ cũ** (mục "Ý chờ" dưới); (iii) bảng quán vùng nam xa (Bạch Mã / Nhị Hồ) 0 % — đếm xem lịch có bữa nào ở đó không trước khi tìm quán; (iv) cờ hết lượt tìm: đếm lại ~21/11 (`data/ra_harness_2026-11-13/dem2.py`).
4. **Ý chờ (đếm trước khi xây):** tìm thêm là điểm nghẽn tốc độ (chữ đầu 5,2–7,9 s khi model tìm thêm) — chỉ khi User muốn tối ưu tốc độ; chữ đầu mục web p50 ~9 s.
5. **Hướng sản phẩm (User 14/11):** trợ lý / agent. Đợt agent kế: nhóm đã đếm — mưa không xây (dữ liệu), thẻ chọn chỗ gác, nhãn / bản đồ thấp ⇒ chỉ còn "nhớ sở thích" chờ User.

### Vòng tự soi 2 (kết phiên tối 14/11)
B, C, E đều gửi; A chốt (đề xuất luật ở `SO_CAI_TIEN_CACH_LAM.md` vòng 31 — chờ User). **GIỮ (bắt lỗi thật):** hỏi thử trợ lý trước khi viết bài kho (11 / 21 món, 28 / 42 nơi, 8 / 24 lễ không cần viết) · đếm "người dùng thấy gì, bao nhiêu lần" trước khi bổ sung dữ liệu (quán đã đóng ở 324 lịch; 15 / ~420 quán OSM từng hiện; 5 sao 0 / 6.108) · người giao nhìn lại 100 % ảnh sẽ hiện (5 ảnh cả hai agent cùng chọn vẫn sai; trẻ em đồ bơi Thuận An; 10 ảnh "luật nguồn"; biển có số điện thoại) · review chéo bài kho + `overlap_scan` trên NHÁP (cụm Golden ở ca kịch Huế; miếu ↔ đàn; "sẽ tái hiện" viết như đã diễn) · script so số thân bài ↔ nguồn đã lưu (480 số / 3 gói, 0 lạ, < 1 phút — nên mặc định khi review bài kho) · soát tay khớp tên Places (nhà hàng cùng tên, chi nhánh "2") · người giao kiểm lại finding của agent con · kiểm hai nguồn có thật độc lập (archive-api trả lại đúng số dự báo ⇒ "đúng 100 %" giả). **THỪA / LÀM NHẸ:** lượt 2 ảnh khách sạn (+5 ảnh, 0 ô hiện ra đổi — giữ vì lời User) · Places cho 140 cơ sở trước khi đếm cơ sở hiện · lượt thử 30 quán ngẫu nhiên trước khi đếm quán hiện · 2 agent chọn ảnh cho nhóm ≤ 15 ⇒ 1 agent / tự chọn + nhìn lại · Playwright khi chỉ đổi ảnh / cờ `kc` (trừ loại ảnh mới lần đầu) · review vòng 2 cho sửa ≤ 2–3 chỗ chữ ⇒ grep xác nhận / A merge thẳng · bảng chi tiết "câu đổi top 10" trong report (giữ 1 dòng — số này quyết câu chạy có phí). **Bẫy:** sửa bảng `data/` main đang trỏ tại chỗ trước merge (B) · `uv run` trong worktree tạo `.venv` mới (B, C — luật có ở `Project_Status.md` §8: `--project /home/minhhieu/hue_rag`) · ước tiền hỏi thử như 1 lần gọi (E ×2,4; ≈ 0,0006 USD / câu) · script dựng ảnh không xoá file cũ ⇒ đếm file mồ côi · chia việc gửi chéo (B ↔ E 2 lần) · A gửi sha đoán trước khi đọc kết quả.

### User tự làm (lệnh `!`, chạy khi tiện từ `/home/minhhieu/hue_rag` — A đã liệt kê theo `git branch -r --merged origin/main` lúc 22:35 14/11/2026)
```
git tag hoso/p9-web-suy-luan origin/p9-web-suy-luan && git push origin hoso/p9-web-suy-luan
git worktree prune
git branch -d p9-anh-kc p9-anh-kho3 p9-anh-kho5 p9-anh-kho6 p9-anh-kp p9-anh-lich p9-anh-lich-thieu p9-anh-quan p9-anh-tra-loi p9-anh-tu-hieu p9-anh-v3 p9-anh-v4 p9-anh-v4b p9-cau-nhieu-y p9-gd-anh-e p9-gd-anh-gt p9-gd-h1 p9-gd-h1-b p9-gt-song p9-khach-san p9-khach-san-anh2 p9-len-ke-hoach-v2 p9-lich-mau-an-o p9-lich-mau-quan-kho p9-lich-truong-gd p9-lkh-nhan p9-luu-tru-lich p9-o-toi p9-quan-an-truoc p9-quan-bo-da-dong p9-quan-kho-cum p9-quan-kho-them p9-quan-kho4-bang p9-quan-lich p9-so-y-va p9-sua-lich-tre p9-sua-lich-v2 p9-tien-ruoi p9-tien-web p9-web-so-cau-hoi p9-web-y-thieu
git push origin --delete p9-anh-kc p9-anh-kho3 p9-anh-kho5 p9-anh-kho6 p9-anh-kp p9-anh-lich p9-anh-lich-thieu p9-anh-quan p9-anh-tra-loi p9-anh-tu-hieu p9-anh-v3 p9-anh-v4 p9-anh-v4b p9-cau-nhieu-y p9-gd-anh-e p9-gd-anh-gt p9-gd-h1 p9-gt-song p9-khach-san p9-khach-san-anh2 p9-len-ke-hoach-v2 p9-lich-mau-an-o p9-lich-mau-quan-kho p9-lich-truong-gd p9-lkh-nhan p9-luu-tru-lich p9-o-toi p9-quan-an-truoc p9-quan-bo-da-dong p9-quan-kho-cum p9-quan-kho4-bang p9-quan-lich p9-so-y-va p9-sua-lich-tre p9-sua-lich-v2 p9-tien-ruoi p9-tien-web p9-web-so-cau-hoi p9-web-y-thieu
git branch -D p9-web-suy-luan p9-hue-thoi-ky && git push origin --delete p9-web-suy-luan p9-hue-thoi-ky
```
(Nhánh `p9-hue-thoi-ky` B xác nhận nội dung đã ở main (14/11). `git branch -d` từ chối nhánh còn gắn worktree ⇒ session chủ gỡ worktree trước. Giữ: `p10-giong-noi`, `p9-b5c`, `p9-sua-lich`, `p9-toc-do-6` (hồ sơ cũ). 4 nhánh `subagent-Monuments-Reviewer-*` gắn worktree antigravity-cli — câu (f). Còn từ 13/11: gỡ dòng `EXA_API_KEY` trong `.env`.)

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

| # | Ý | Trạng thái |
|---|---|---|
| 1–7, 12 | Kiểm giá "…000đ" / "triệu"; không đủ điểm ⇒ câu cố định; `khong_xep` + lý do từ mã luật; dòng giả định do code nối; test cố tình vi phạm; dòng "Mình hiểu…"; cột `ten_khac`; lời dặn không dùng địa danh thật làm ví dụ | vào B5 (`d66f6a3`) |
| 8 | Sửa lịch nhiều lượt (`sua_lich` hành động có tên, khung giữ ở server, Đã đổi / Giữ nguyên, ≤ 2 hành động / lượt) | code trên `p9-sua-lich` `79b3d9c` (rebase lên B5b + B171, giữ `hoi_toi` / lý do buổi tối — C208); harness đo E review ready; **hoãn** (cần cờ `lich_trinh` câu tự do) |
| 9 | Bộ chuỗi sửa lịch pass^k | bộ `data/phase_9/bo_do_sua_lich/` (10 + 5 kín; nhãn đã thấy S03 / S08 sửa theo B171 — C208); plan chọn pass^2; pilot = S01 + S06 (A đồng ý) |
| 10 | Cột trong nhà / bậc thang ⇒ phương án ngày mưa | **User đã trả lời phiếu gộp 12/11** ⇒ vào bảng đề xuất `data/phase_9/lich_trinh/diem_v8_de_xuat.json` + spec "Lên kế hoạch" bản 3.3 (phiếu v6 / v7 cũ không còn chờ) |
| 11 | `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — theo dõi | C210 06/11: code không dò "3N2D" / "4n3d" / "2 hôm" / "cuối tuần" nhưng model tự gửi đúng số 5 / 5; biểu mẫu bỏ vấn đề này |
| 13, 14 | Ưu tiên theo lĩnh vực; đoạn gần trùng | đếm 0 USD xong — không mở thí nghiệm (C179) |
| 15–17 | Nhãn lỗi tự động; "0 lỗi trên n ca" + luật ba; dự phòng demo mất mạng | B7 |
| 18 | Router gắn cờ ⇒ code gọi `lich_trinh` | không cần (Q2a đạt) |

**Không làm** (đã cân): lọc cộng tác / rating, TSP, GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới, nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.


## Câu hỏi cho User (hỏi mỗi lần một câu — đáp án = đa số nhóm; cập nhật 22:35 14/11/2026)

**Đầu phiên sau:** xem "Việc đầu phiên sau" mục 1 (quyền ⇒ ngưỡng mưa ⇒ trang khách sạn ⇒ giới hạn Codex ⇒ vòng cải tiến 31 ⇒ nhớ sở thích ⇒ dọn nhánh + worktree AGY).
**Đã trả lời tối 14/11 (không hỏi lại):** quyền "như 14/11" · W73–W75 áp · ưu tiên ảnh + khách sạn + dữ liệu đầy đủ (đảo "khách sạn không cào điểm / ảnh"; giữ không giá phòng) · Qdrant / collection mới được nếu cần.
**Đã trả lời 14/11 (không hỏi lại):** câu nhiều ý v2 bật · 132 ảnh web giữ trong repo, gỡ mọi chữ ghi công · giờ Đại Nội ghi cả hai theo mùa · màn "Huế qua các thời kỳ" làm · W70–W72 áp · ảnh dưới câu trả lời + gói dữ liệu đa số nhóm · Codex `gpt-6.1-sol` medium · ghi kho khi User vắng · không dòng © OSM · khu ở giữ luật buổi tối · dọn nhánh: tag + xoá · "giao diện ổn rồi".

**Cũ còn mở:** góp ý `bai_hoc/` (khi User đã đọc). (Q-DP, **khi tới deploy AWS** — không hỏi sớm): tra web trên bản công khai · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền (HUE_SITE phải là tên miền https) · xoá ảnh docker cũ · dòng © OSM nếu bản công khai cần đúng giấy phép. **Không gấp:** vị trí Bảo tàng Cổ vật kho tự mâu thuẫn; lệch năm Tây Sơn đóng đô 1786 ↔ 1788 giữa 2 bài kho (màn thời kỳ chỉ nêu 1788); xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo; nhãn cũ câu "hôm nay âm lịch" trong bộ 30/10.

## Câu hỏi A còn nợ (không cần User)

- **09/11:** T1 đã bật (xong lượt xác nhận + lượt sau G); giới hạn T1: "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); allow-list thêm bảng lưu trú v2 `data/khach_san_2026-11-14/bang_luu_tru_lich_v2.json` (ĐÃ merge 14/11 tối; thay bảng `data/luu_tru_2026-11-14_lich/bang_luu_tru_lich.json`) + bảng quán `bang_quan_lich_v1.json` md5 `ab481586d46f` + ảnh `frontend/public/anh/khach_san/`; build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên tối 14/11 (mở 17:45, kết 22:35 14/11/2026):** A `hue-rag-fb` · B `hue-rag-62` · C `hue-rag-eb` · E `hue-rag-1f` — cả bốn Claude Code, trực tiếp; D không mở.

**Phiên 14/11 (mở 09:42, mở lại 14:44 + 14:55; kết 17:40 14/11/2026):** sáng A `hue-rag-7b` · B `hue-rag-22` · C `hue-rag-b4` · E `hue-rag-c4`; chiều A `hue-rag-ad` · B `hue-rag-6b` · C `hue-rag-c1` · E `hue-rag-14` — cả bốn Claude Code, trực tiếp.

**Phiên 13/11 (mở 19:46 13/11/2026):** A `hue-rag-43` · B `hue-rag-83` · C `hue-rag-eb` · E `hue-rag-e8` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); `/tmp` mất sau khởi động lại máy (worktree B dựng lại).

**Phiên 12/11 (mở 18:40 12/11/2026):** A `hue-rag-7d` · B `hue-rag-1b` · C `hue-rag-e1` · E `hue-rag-33` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên chiều 11/11 (mở 13:39 11/11/2026):** A `hue-rag-2f` — chỉ A (B / C / E không mở; 8 terminal khác là dự án khác). Qdrant tắt. Việc: bàn `bai_hoc/` với User.

**Phiên 11/11 (mở 08:18 11/11/2026):** A `hue-rag-96` — chỉ A (B / C / E không mở). Qdrant tắt lúc mở.

**Phiên 10/11 (mở 19:02 10/11/2026):** A `hue-rag-55` · B `hue-rag-05` · C `hue-rag-4f` · E `hue-rag-e4` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Quyền phiên tối 14/11 HẾT HẠN (22:35 14/11/2026, kết phiên).** Phiên sau A hỏi lại. (Tối 14/11: "như 14/11"; User vắng 17:49 ⇒ "tiếp tục phát triển; câu cần User gác lại".)
- **Quyền phiên 14/11 HẾT HẠN (17:40 14/11/2026, kết phiên).**
**Trần tiền HIỆN HÀNH (đọc dòng này, mọi con số 4,0 / 4,2 / 4,3 / 4,6 / 6,0 bên dưới là lịch sử):** **không trần cứng** (User 14/11: "không lo tiền, dùng hiệu quả, không phung phí"; giữ ở tối 14/11) — phiên sau A hỏi lại cùng quyền phiên; Phase 9 đã dùng ≈ 7,1 USD (ước, cộng tin báo, chưa review; trần cũ 6,0 của 13/11 đã vượt theo lời User).

- **Quyền phiên 12/11 HẾT HẠN (22:23 12/11/2026, kết phiên).** Trần Phase 9 A ghi tạm 4,6 trong phiên (User "vẫn duyệt chi phí API"); Phase 9 ≈ 4,61 ⇒ phiên sau xin trần mới.
- **Phiên 12/11 (User chọn "như 10/11", A ghi nhận 18:45 12/11/2026):** A tự điều phối, giao ngay việc có sẵn trong handoff, A tự commit / push, B / C / E push nhánh riêng, trần Phase 9 4,2 (≈ 3,88 đã dùng), việc cần User duyệt thì gác. Hết hạn cuối phiên.
  **Thêm (19:01 12/11/2026) User đi nghỉ, trở lại ~20:30:** "cứ tiếp tục làm việc; vẫn duyệt chi phí API; **không hỏi khi User vắng**; làm tiếp không cần hỏi" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User"; tiền ghi thật từ log, vượt trần 4,3 chỉ khi cần cho việc đã giao và báo lại.
- **Quyền phiên chiều 11/11 HẾT HẠN (16:24 11/11/2026, kết phiên).**
- **Phiên chiều 11/11 (User chọn "như sáng 11/11", A ghi nhận 13:41 11/11/2026):** A sửa `bai_hoc/` theo góp ý, tự commit / push; trần Phase 9 4,2; việc cần User duyệt thì gác. Hết hạn cuối phiên.
- **Quyền phiên 11/11 (sáng) HẾT HẠN (10:43 11/11/2026, kết phiên).**
- **Phiên 11/11 (User chọn "như 10/11", A ghi nhận 08:20 11/11/2026):** như 10/11 dưới đây (A tự điều phối, tự commit / push, B / C / E push nhánh riêng, trần Phase 9 4,2, việc cần User duyệt thì gác, không hỏi khi User vắng). Hết hạn cuối phiên.
- **Phiên 10/11 (User chọn "như 09/11 + trần 4,2", A ghi nhận 19:05 10/11/2026):** như 09/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác; tiền API thoải mái nhưng ưu tiên tốc độ, không test vô nghĩa). **Trần Phase 9 nâng 4,0 ⇒ 4,2 USD** (cho 2 việc tốc độ, quỹ B7 0,35 giữ riêng). Hết hạn cuối phiên.
  **Thêm (19:12 10/11/2026) User:** "hạn chế test các phần không cần thiết, không over-engineer, muốn đẩy nhanh quá trình; chi phí API vẫn duyệt; các session cùng trao đổi, thảo luận để đề xuất, chốt phương án" ⇒ A mở vòng tự soi 1 ngay (plan B / E là kết quả đầu); tiền không còn là lý do giữ bộ đo — thời gian là thước.
  **Thêm (19:15 10/11/2026) User đi nghỉ:** "tiếp tục điều phối, phát triển, triển khai, ghi báo cáo đầy đủ; câu cần User chốt thì gác lại, triển khai phần khác; **không đưa câu hỏi lúc User vắng** (treo việc)" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User".
- **Phiên 09/11 (User chọn "như 08/11", A ghi nhận 20:13 09/11/2026):** A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác. Trần Phase 9 nâng 4,0. Hết hạn cuối phiên.
  **Thêm (20:21 09/11/2026) User:** "thoải mái tiền API cho triển khai, phát triển nhưng phải đảm bảo tốc độ; không làm những thứ vô nghĩa hay test những thứ mất thời gian; 4 bạn trao đổi, thảo luận cùng nhau để đưa ra phương pháp, hướng xử lý phù hợp" ⇒ ưu tiên tốc độ làm; cắt test / đo không phục vụ sàn chất lượng; B / C / E bàn thẳng với nhau, A chốt khi lệch phạm vi.
- Spec Phase 9 file hiện tại sha `01b7476a3eb1` ≠ bản duyệt `5557f0fd7650` do commit `442f758` (bỏ mốc ngày theo User 08/11; sàn + tiền không đổi) ⇒ sửa chữ, không cần duyệt lại (A ghi 20:13 09/11/2026).
- **Quyền phiên 08/11 HẾT HẠN (12:50 08/11/2026, kết phiên).** (User 11:06: ~13:00 dừng; User 12:50 08/11/2026: để nhiệm vụ / câu hỏi cho phiên sau.)
- **Phiên 08/11 (User chọn "như 07/11", A ghi nhận 09:22 08/11/2026):** như 07/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, khoá Serper cho tra cứu, việc cần User duyệt thì gác). Hết hạn cuối phiên. Giao lúc mở: B ảnh cổng (`p11-anh-cong`), C review ảnh, E rà "Câu hỏi A còn nợ" (chỉ đọc).
- **Phiên 07/11 (User chọn "như 06/11", A ghi nhận 11:55 07/11/2026):** A tự điều phối — giao ngay việc có sẵn trong handoff, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5. Hết hạn cuối phiên.
  **Thêm (12:30 07/11/2026, User đi nghỉ):** "tiếp tục nghiên cứu, triển khai, phát triển, đánh giá, viết báo cáo đầy đủ; việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; làm việc khác; tự do nghiên cứu, gọi Codex tra cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau". Trần tiền như trên (≤ 1 USD / phiên). **(12:31 07/11/2026) User: "trần tiền tôi vẫn duyệt nếu quá 1$, có thể thoải mái thực nghiệm"** ⇒ vượt 1 USD / phiên được; A vẫn ghi tiền thật từ log mỗi việc + báo tổng ở nhật ký.
- Phiên tối 06/11 — hết hạn 22:41 06/11/2026. Tiền phiên ≈ 0,027 USD.
- **Tiền Phase 9: trần 4,0 USD** (User nâng, A ghi nhận 20:15 09/11/2026; dự phóng việc chờ ≈ 0,55: G 0,12 · T1 0,04 · T3 0,05–0,1 · T2 0,21 · T4 0,12; quỹ B7 0,35 giữ riêng). Trước: 3,5 (User nâng 10:38 08/11/2026; trước 2,5) (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
- **Đã duyệt, không hết hạn theo phiên:** spec giao diện cổng đợt 1 bản 2 `ff3c317ec88b` (User 11:56 07/11/2026); plan G2 giọng nói `92ec551531fd` (A duyệt sau review 2 vòng, 06/11 tối); spec Phase 10 bản 4 `784d6f7abd9f` (sherpa-onnx, tải model ≤ 300 MB, thu 40 câu; Web Speech bỏ); tải SigLIP 2 + collection ảnh (11:42 05/11); luật S-AT mới (20:14 05/11); cache câu trả lời ⇒ Phase 12 (20:27 05/11); bật `tra_web` (21:15 05/11).
- **User (09:00 05/11/2026):** cần công cụ / nghiên cứu / tải / khoá mới ⇒ tự nghiên cứu (0 USD, thông tin công khai) + đề xuất; thêm công cụ / thư viện lớn / tải model / khoá / tài khoản mới vẫn trình User trước (`Session_Prompt.md` §4).
- **Phase 9 (spec):** Serper dùng luôn (User chấp nhận rủi ro điều khoản); gói npm giao diện như đã duyệt 02/11; dữ liệu công khai dùng cho học tập, không kiểm giấy phép (05/11).
- **Thường trực:** A commit / push — hỏi User trước (luật chung), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (`WORKFLOW.md` §9.6); B / C / E không commit trừ khi việc ghi rõ; duyệt cho A = duyệt cho B / C / E; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. **(12:32 07/11/2026) User: khoá `SERPER_API_KEY` dùng được cho tra cứu nghiên cứu** (gọi qua `uv run --env-file /home/minhhieu/hue_rag/.env …`, không đọc / in khoá; chỉ câu tra thông tin công khai; 0,001 USD / lượt, ghi số lượt). Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper: 0,001 USD / lượt. Open-Meteo: 0.

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | bộ kín 40 câu — **đã dùng** 01/11 | `7f97d4c10b2b` |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối Phase 1–8 (mốc của Phase 9) | — |
| `data/phase_9/` | bộ đo B4 / B5 / B5c / B6 / sửa lịch, bảng điểm v3 / v4, toạ độ, kết quả đo | — |
| `data/phase_10/anh/` | bộ ảnh đo, danh sách tên, patch `p10-anh`, E9 | — |
| `data/sua_kho_2026-11-05_gio/` | sửa kho giờ mở cửa: lệnh `tools/chay.sh`, sao lưu record / sparse | — |
| `data/nguon_mo_huegov_2026-08-05/` | dữ liệu mở Huế (có file dữ liệu cá nhân ⚠ — không vào kho / báo cáo) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C / E sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file); review ≤ 2 vòng.
- **Bộ an toàn 32 câu luôn báo đủ 4 số** (đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời).
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (tự viết); `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server bằng TaskStop (không `pkill -f`); (3) chạm tìm / chia đoạn: T1 giống byte; (4) 3 chỗ báo cáo (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Đang dựng chỉ mục / đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant.** Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ. `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 06/11 sáng + tối nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`.

- Phiên tối 05/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`.
- Phiên 05/11 sáng–chiều nguyên văn (C173–C197, B156–B163, E1–E8, quyết định theo giờ, merge B4b / B5 / #6, B5c âm): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`.
- Phiên 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`, `…_2026-11-03_toi.md`; 02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
