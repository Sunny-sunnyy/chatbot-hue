# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 18:24 15/11/2026 (A, kết phiên chiều 15/11). Trước: 14:42 15/11/2026 (A, kết phiên 15/11). Trước: 22:35 14/11/2026 (A, kết phiên tối 14/11). Trước: 17:40 14/11/2026 (A, kết phiên chiều 14/11). Trước: 09:45 14/11/2026 (A, mở phiên 14/11). Trước: 22:40 13/11/2026 (A, kết phiên 13/11).
Nguyên văn handoff trong phiên 13/11 (mọi quyết định theo giờ, bàn nhóm, vòng tự soi 1): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-13.md`; 12/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-12.md`. Nhật ký: `bao_cao_he_thong/nhat_ky/2026-11-13_lich_trinh_kho_3.md`.

## PHIÊN SAU ĐỌC TRƯỚC (A viết 18:24 15/11/2026, KẾT PHIÊN CHIỀU 15/11 — User: "kết phiên để reset context, tôi bật lại 4 phiên mới để tiếp tục hoàn thiện dự án; nhiệm vụ, câu hỏi để ở session tiếp theo; cập nhật các file .md đầy đủ để A, B, C, D, E nắm ngữ cảnh")

**Phiên chiều 15/11 đã kết** (mở 15:08, kết 18:24 15/11/2026; User vắng khoảng 16:20–17:47, A tự điều phối, không hỏi lúc vắng). A `hue-rag-60` · B `hue-rag-cb` · C `hue-rag-51` · E `hue-rag-ab`, cả bốn Claude Code (Fable 5.2), trực tiếp; D không mở. **Quyền phiên HẾT HẠN** ⇒ A mới hỏi lại User một câu (chiều 15/11: "như sáng 15/11" = A tự điều phối, A commit / push, B / C / E push nhánh riêng, tự tra / cào / ghi kho khi việc cần, không hỏi khi User vắng, tiền không trần cứng nhưng dùng hiệu quả, lúc vắng ≈ 1 USD). Mỗi session đọc mục đầu `sessions/STATUS_<X>.md` "PHIÊN SAU ĐỌC TRƯỚC (KẾT PHIÊN CHIỀU 15/11)". Nguyên văn phiên chiều (mọi quyết định theo giờ, số đo, review, vòng tự soi 1 + 2): `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-15_chieu.md`; phiên sáng–trưa: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-15.md`. Nhật ký: `bao_cao_he_thong/nhat_ky/2026-11-15_do_bu_mua.md`. **D** (khi User muốn học): bài `bai_hoc/25` (đổi hạng chỗ ở + đổi ngày đi bằng lời, thẻ Nơi ở chỉ hiện khi hỏi, chuyện review bắt lỗi "chữ giống ngày"), `23` (lịch 41 điểm, lượt thật nhỏ bắt đoạn mô tả nghèo), bài tra web (câu hỏi nối tiếp — B viết lúc kết phiên).

### Hệ thống lúc kết phiên (main đã push — xem `git log -1`; mọi nhánh chiều nay đã merge)
- **Kho** không đổi: 263 bài / 9.425 đoạn, record `1b53af26b662`, T1 `aa34d4215f15`.
- **Lịch "Lên kế hoạch":** bảng điểm **v9 — 41 điểm** (`data/phase_9/lich_trinh/diem_v9.json` md5 `eb6cfd95df6b`; +7: Từ Hiếu, Trường Tiền, Hải Vân, Bến Ngự [cờ thời lượng 1 nguồn — User giữ], làng nón Tây Hồ, An Hiên, Lập An); toạ độ v9 `f6068ff37d61`; `KHUNG_HUE` kinh độ tới 108,25 (cả `frontend/src/toaDo.js`); ảnh lịch **40 / 41** (bảng ảnh v5 md5 `5ed8f32903a9`; loader nhận `nguon: "user"` không kèm trang); ngoại lệ test đơn điệu "khám phá có nhiều ngày cụm xa hơn hẳn" (A duyệt; 1 / 320 tổ hợp, trần 6). **Buổi để trống không hiện** (giao diện + chữ chép / .txt; nhóm trẻ em / lớn tuổi còn một dòng ở Ghi chú của lịch; ngày đi xa không có dòng giải thích — User chọn không thêm). **Khối "Nơi ở gợi ý" chỉ hiện khi người dùng hỏi** = tham số lịch có mức hạng (chọn ở biểu mẫu hoặc nói bằng lời); chưa hỏi ⇒ một dòng link sang `#/cho-o`; lịch mẫu có sẵn hạng 2–3 sao. Bảng lưu trú **v6** (`data/anh_user_2026-11-15_ghep/bang_luu_tru_lich_v6.json` md5 `44d7b14d8fce`): 136 cơ sở (gộp hai dòng trùng), **67 có ảnh** (10 ảnh User đưa, 1 ảnh đã che số điện thoại).
- **Sửa lịch bằng lời** (cờ `sua_lich_v2`): thêm **`doi_hang_o`** (đổi hạng chỗ ở; enum 3 mức; code áp, không chạy lại bộ xếp; không nêu hạng ⇒ hỏi lại; xét sau cùng trên khung cuối lượt; hạng đặt nhầm trong hành động khác được tách ra) và **`doi_ngay_di`** (không tham số — code đọc ngày từ chữ người dùng `do_so.ngay_tu_cau`; giữ chỗ nếu đúng luật, không thì xếp lại và câu báo nêu rõ; ngoài 7 ngày ⇒ "chưa xét mưa"; ngày đã qua / quá 180 ngày / 2 ngày / mơ hồ ⇒ không đổi + lý do). Chưa làm: ngày tương đối ("dời 2 hôm"), ngày âm / "dịp Tết", xin chỗ ở không nêu hạng ⇒ hiện mọi hạng.
- **Chat:** cờ **`web_cau_noi_tiep` BẬT** (User, 17:50 15/11/2026): lượt có lịch sử + model đã tìm kho + không phải lượt nhiều ý ⇒ câu gửi tra web = câu tìm kho cuối model viết (qua bộ lọc `cau_tim_web`; rỗng sau lọc ⇒ câu gõ). A thử ca gốc của User: mục web nói đúng nơi kèm giờ. Giao diện: bỏ dòng "Các bước…" sau câu trả lời (lúc chờ một dòng bước đang chạy; hằng `HIEN_BUOC_LUC_CHO` trong `chat.jsx`), bỏ dòng báo gửi ảnh cạnh nút Hỏi bằng ảnh (trang Giới thiệu vẫn nêu), nút "Sửa — điền lại biểu mẫu" cuộn tới biểu mẫu.
- **Ảnh:** Khám phá **260 / 263** (3 bài User chọn để trống: lễ Kỳ yên, lễ Tiến Xuân ngưu, ca kịch); ảnh tĩnh phục vụ ở `/static/anh/…` (không phải `/anh/…`).
- **Đo / log:** mỗi dòng `chat_metrics` có `git_sha` + `scripts/dem_chat_metrics.py --sha <mã|HEAD>` (W79); `scripts/commit_push.sh "<lời commit>" <file>…` in `ĐÃ PUSH <sha> origin/<nhánh>` (W81; merge thì `git push` + `ls-remote`). Bộ chấm Q5b (`data/len_ke_hoach_v2_2026-11-13/tools/q5b_tron.py`) sửa: vế "không mất phần khẩn cấp" chưa từng đo trước 15/11 ⇒ nay đọc định tuyến (16 / 16 ở lần đầu) + lưu chữ trả lời. Nhãn chuỗi S07 của bộ đã thấy đổi theo bảng v9 (`chuoi_da_thay.jsonl` md5 `eacb8ebdcb91`; bản cũ `…truoc_v9.jsonl`).
- **Luật mới (User duyệt 18:01 15/11/2026):** W82 bộ câu dò ≥ 20 cho code đọc chữ người dùng + luật dừng ghi trước; W83 phép kiểm harness phải có ca đối chứng ra "có"; W84 đổi bảng dữ liệu ⇒ quét nhãn + mô phỏng không model trước merge (`Session_Prompt.md` §8, `WORKFLOW.md` §3.4, sổ vòng 33). Không duyệt: sửa `START_SESSION.md` "A báo tên terminal trước".
- **Tốc độ:** User chọn BỎ "tra web sớm", GÁC "gộp câu tìm" (plan `docs/superpowers/plans/2026-11-15-toc-do-web-som-gop-tim-plan.md` = hồ sơ). Câu thường đạt sàn; đường tìm thêm + web vẫn chậm (~6 s chữ đầu, ~15 s cả câu có web) — giới hạn đã biết.
- **Docker nháp** (`data/phase_12/deploy_nhap/`, private): E đã trỏ 3 bảng v9 + ảnh lịch v5 + lưu trú v6; chưa build image.
- **Tiền phiên chiều 15/11 (theo sha / file từng session, CHƯA ai tính lại tổng):** ≈ 0,45 USD — C 0,335 (đổi hạng 0,210 · nơi ở khi hỏi 0,003 · đổi ngày đi 0,123) · B 0,095 · E 0,020 · A ≈ 0,002. Cả ngày 15/11 ≈ 1,0 USD. Phase 9 ước ≈ 7,6 USD (7,1 lúc kết phiên trưa + chiều; ước, chưa review). Không trần cứng (User).

### Việc đầu phiên sau — THEO THỨ TỰ
1. **A:** hỏi quyền phiên (một câu có đáp án) ⇒ cùng lượt giao các việc 2–4 (đã có trong handoff, không chờ "làm đi") ⇒ mở server cho User thử (`cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8010`; server của A mất khi đóng phiên) ⇒ hỏi User các câu ở "Câu hỏi cho User", mỗi lần một câu bằng hộp chọn có đáp án khuyến nghị (User nhắc, A ghi nhận 17:50 15/11/2026: "hỏi tôi kèm các đáp án đề xuất").
2. **B — phần code của W84** (0 USD, ~10 dòng trong `data/`): harness Q3 sửa lịch tự chạy mô phỏng nhãn không model trước lượt có phí và dừng nếu < n / n (`data/phase_9/bo_do_sua_lich/tools/mo_phong_v2.py` đã theo bảng settings; bản có chọn bảng `data/nhan_cu_v9_2026-11-15/mo_phong_bang.py`). Kèm: `tools/kiem_bo.py` của bộ sửa lịch mở cả file kín ⇒ tách phần kiểm bộ đã thấy để session chạy được mà không chạm file kín.
3. **E — dữ liệu lịch còn hở** (0 USD trừ khi tra web): bữa ở làng nón Tây Hồ (144 bữa mô phỏng) + Hải Vân tối (72) chưa có quán / ghi chú — kho không nói ⇒ tra nguồn công khai, có căn cứ mới viết (theo luật sửa kho / ghi chú); ảnh Hải Vân hiện là đoàn tàu trên sườn núi ⇒ tìm ảnh cửa ải / cung đèo đạt luật chọn ảnh; chợ Bến Ngự thời lượng 1 nguồn (trang 403) ⇒ tìm nguồn thứ hai.
4. **C — dọn nợ nhỏ vùng sửa lịch bằng lời** (0 USD, code + test; mỗi cái có test): `doi_tham_so` rỗng hẳn còn im lặng ⇒ có dòng báo; dòng báo "Đã đổi số trẻ em" nói thêm khi lịch xếp lại; cập nhật bảng "trường nào sửa được bằng lời" (`report_agent/2026-11-12_ra_khoang_cach/c_dem_sua_lich_truong.md`). Áp W82 nếu chạm hàm đọc chữ.
5. **User tiếp tục tự thử** phần B (Lên kế hoạch) và C (Khám phá, Giới thiệu, Trang chủ) của danh sách thử — bản lưu `data/huong_dan_test_user_2026-11-15.md` (private; A gửi lại trong chat nếu User cần); lỗi User báo ⇒ A ghi handoff + giao.
6. **Sau đó (ứng viên, chờ User chọn hướng — câu (1) dưới):** (a) bậc sửa lịch kế: ngày tương đối + xin chỗ ở không nêu hạng ⇒ hiện mọi hạng (đổi lời dặn ⇒ đo H / D + Q3 ngay + Q5 + Q5b; ≈ 0,15–0,25 USD / bậc; áp W82); (b) tốc độ câu hỏi tiếp: lần tìm kho đầu dùng câu cụt, trượt 6 / 7 ⇒ luôn tốn thêm một lần gọi model (B đếm; chưa có plan; ghép câu bằng code đã bỏ vì phá câu đổi chủ đề); (c) mốc đóng code 25–30/12: B7 lượt đo cuối (bộ kín 7 câu ngày, thước "thiếu cảnh báo mới", dự phòng demo mất mạng), deploy AWS (checklist ở "Câu hỏi A còn nợ"), giọng nói (nhánh `p10-giong-noi`), bản đồ lịch (cờ `ban_do_lich` tắt).

### User chốt lúc kết phiên (A ghi nhận 18:31 15/11/2026)
- **Xong ở local trước, deploy sau** ("tôi muốn hoàn thành ở local mới tính deploy"); **quyển báo cáo, slide, kịch bản demo làm SONG SONG với giai đoạn deploy** — không xếp vào giai đoạn local, không dùng làm lý do cắt / hoãn tính năng. A ước (không phải số đo) phần local xong ≈ 80–85 %; còn: User thử hết 26 mục + sửa lỗi phát sinh · lượt đo cuối B7 để đóng Phase 9 · quyết giọng nói (Phase 10, nhánh `p10-giong-noi`) + bản đồ lịch (Phase 11, cờ `ban_do_lich` tắt) · các chỗ hở đã biết. Phiên sau câu (1) "hướng làm tiếp" = User chốt "xong ở local" gồm những gì ⇒ A lập danh sách đóng.

### Giới hạn đã nhận trong phiên chiều (không báo lại như lỗi mới)
- Hàm đọc ngày: luật theo danh sách từ không kín — có thể sót chữ giống ngày (câu báo luôn in ngày + thứ); 1 câu từ chối nhầm ("đi ngày 3/12 giờ nào cũng được"); "tuần sau" theo tuần lịch; dd/mm đã qua không nêu năm ⇒ năm sau (thường báo ngoài 180 ngày); "dịp Tết âm lịch" đi đường thường. Bộ dò của E: `data/review_sua_ngay_di_2026-11-15/do_34.py` + `do_19.py` (chạy lại khi sửa hàm).
- Đổi hạng: lượt 3 ý có đổi hạng ⇒ "Chưa làm: đổi hạng chỗ ở" (code áp tối đa 2 / lượt); câu "có em bé + xin 3 sao" ⇒ hai hành động.
- Web nối tiếp: câu hỏi tiếp NHIỀU Ý vẫn tra web bằng câu gõ; mục web dao động theo lượt (cùng ca: lượt đo 2 / 2 câu cố định, lượt sau có giờ); tên người dùng mới đo 0 / 4 lượt, không có bộ lọc tên; chi tiết lượt trước (vd một ngày) có thể ra web ⇒ **xét lại cờ trước bản công khai và nếu bật `nho_cau_tra_loi`**; bộ kiểm số: không chặn nhầm vì cách viết giờ (0 / 85) ⇒ không xây chuẩn hoá giờ.
- Chuỗi Q3 S06 chập chờn ở thẻ chọn (từ 14/11). Ảnh: Momiji có dấu nước to (User chọn); 2 ảnh khách sạn nhỏ / dẹt. Các số cũ về ô Nơi ở (95,3 % ô có ảnh; 8.962 / 15.360 lượt đổi…) đo lúc lịch luôn có khối ⇒ lịch sử.

### Vòng tự soi 2 chiều 15/11 (A chốt 17:03; B, C, E đều gửi) — đã thành W82–W84
GIỮ: reviewer tự viết câu dò gọi thẳng hàm thuần · lượt thật nhỏ sau mô phỏng · tái tạo trên đúng đường người dùng trước khi sửa · đếm 0 USD trước khi xây · agent con đối chiếu bài học · chạy lại chuỗi trượt trên main để quy nguyên nhân. LÀM NHẸ: một review / nhánh (hai chỉ khi đổi thứ gửi ra ngoài / an toàn, giao cùng lúc) · bộ hồi quy Q3 chạy ngay sau bộ câu chính · gom tài liệu một lần cuối chuỗi việc. BỎ: bộ "câu lạ đúng phạm vi" do A viết (24 / 24 đúng, không bắt gì) ⇒ câu phá 0 USD. Chi tiết: `SO_CAI_TIEN_CACH_LAM.md` vòng 33.
**Bẫy phiên chiều:** C sửa thêm sau khi A đã nhận giới hạn ⇒ hồi quy · A giao hai review lần lượt cho một nhánh · A nói trước với User "sẽ tự bật cờ" rồi đổi ý sau review · A ước tiền Q5 qua server lệch 10 lần (B hỏi lại) · A kiểm ảnh ở `/anh/…` thay vì `/static/anh/…` (tưởng 404) · phép kiểm Q5b luôn ra 0 không ai hỏi · nhãn S07 cũ sau bảng v9 · C tả kết quả từ trí nhớ (ghi ngược bớt / thêm) · E rebase sau khi đã push · lệnh `--kin` lộ nhãn qua traceback (giữ đuôi `2>/dev/null | tail -1`) · main đổi sha giữa lúc chạy đo (so `git diff -- backend`).

### User tự làm (lệnh `!`, chạy khi tiện từ `/home/minhhieu/hue_rag`)
**(1) Đếm trên bộ kín sửa lịch** (bảng v9 làm một nhãn bộ đã thấy bị cũ; bộ kín có thể dính — không session nào được mở). Hai lệnh chỉ in số đếm (B thử trên file giả; A đọc script: `--kin` chỉ in một dòng). **Giữ nguyên đuôi `2>/dev/null | tail -1`:**
```
grep -c -i -E "từ hiếu|trường tiền|tràng tiền|hải vân|bến ngự|tây hồ|an hiên|lập an" /home/minhhieu/hue_rag/data/phase_9/bo_do_sua_lich/chuoi_sealed.jsonl
cd /home/minhhieu/hue_rag/backend && BANG_FILE=diem_v9.json PYTHONPATH=/home/minhhieu/hue_rag/backend uv run python /home/minhhieu/hue_rag/data/nhan_cu_v9_2026-11-15/mo_phong_bang.py /home/minhhieu/hue_rag/backend /home/minhhieu/hue_rag/data/phase_9/bo_do_sua_lich/chuoi_sealed.jsonl --kin 2>/dev/null | tail -1; echo "ma thoat: ${PIPESTATUS[0]}"
```
Cách đọc: lệnh 1 = số dòng nhắc 7 nơi mới; lệnh 2 in "k / n chuỗi khớp" + "ma thoat: 0" — k < n ⇒ có nhãn kín cũ (báo A; A xếp người được phép sửa); không có dòng đếm + "ma thoat: 1" ⇒ công cụ lỗi, không lộ gì.
**(2) Xoá nhánh đã merge** (A liệt kê bằng `git branch -r --merged origin/main` lúc kết phiên chiều; gồm cả 14 nhánh của phiên trưa chưa xoá):
```
git worktree prune
git push origin --delete p9-anh-14-bai p9-anh-chat p9-anh-chat-hoi p9-anh-kp-user p9-anh-ks-user p9-anh-ks-w78 p9-anh-lavela p9-anh-sua-qc p9-anh-tay-ho p9-bo-buoi-trong p9-cho-o p9-commit-push p9-diem-v9 p9-gd-3-sua p9-hang-o-m12 p9-luu-tru-v5 p9-mua-6mm p9-ngan-sach-o p9-nhan-mua p9-o-khi-hoi p9-phia-bien p9-rao-so-ngay p9-sua-hang-o p9-sua-ngay-di p9-tai-lieu-hang-o p9-tai-lieu-ngay-di p9-tai-lieu-v9 p9-the-ks-chat p9-tuan-sau p9-w79-sha p9-web-noi-tiep
git branch -d p9-anh-14-bai p9-anh-chat p9-anh-chat-hoi p9-anh-kp-user p9-anh-ks-user p9-anh-ks-w78 p9-anh-lavela p9-anh-sua-qc p9-anh-tay-ho p9-bo-buoi-trong p9-cho-o p9-commit-push p9-diem-v9 p9-gd-3-sua p9-hang-o-m12 p9-luu-tru-v5 p9-mua-6mm p9-ngan-sach-o p9-nhan-mua p9-o-khi-hoi p9-phia-bien p9-rao-so-ngay p9-sua-hang-o p9-sua-ngay-di p9-tai-lieu-hang-o p9-tai-lieu-ngay-di p9-tai-lieu-v9 p9-the-ks-chat p9-tuan-sau p9-w79-sha p9-web-noi-tiep
git branch -D p9-tim-song-song p9-tran-tim-1 p9-web-so-0 && git push origin --delete p9-tim-song-song p9-tran-tim-1 p9-web-so-0
```
(`p9-tim-song-song`, `p9-tran-tim-1` đã có tag `hoso/…`; `p9-web-so-0` bỏ, kết quả ở report. Giữ: `p10-giong-noi`, `p9-b5c`, `p9-sua-lich`, `p9-toc-do-6`. Nhánh nào `git branch -d` báo không có ở máy thì bỏ qua.)
**(3) `.env`:** sửa 1 dòng tên biến có khoảng trắng (`docker --env-file` từ chối) + gỡ dòng `EXA_API_KEY` (từ 13/11).

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


## Câu hỏi cho User (hỏi mỗi lần một câu, bằng hộp chọn có đáp án khuyến nghị — đáp án = đa số nhóm; cập nhật 18:24 15/11/2026)

**Đầu phiên sau (chưa hỏi):** (0) quyền phiên. (1) **Hướng làm tiếp sau các việc nhỏ đã giao** — chọn một / xếp thứ tự: (a) bậc sửa lịch bằng lời kế (ngày tương đối "dời 2 hôm"; xin chỗ ở không nêu hạng ⇒ hiện mọi hạng; ≈ 0,15–0,25 USD / bậc); (b) tốc độ câu hỏi tiếp (lần tìm đầu dùng câu cụt, trượt 6 / 7 — cần plan + đo); (c) dồn sức cho mốc đóng code 25–30/12: B7 lượt đo cuối + deploy AWS; (d) tiếp tục để User thử và sửa lỗi phát sinh là chính. Nhóm chưa bàn câu này — A bàn B / C / E trước khi khuyến nghị. (2) **Kết quả 2 lệnh đếm bộ kín** (mục "User tự làm"): k < n ⇒ ai được phép sửa nhãn kín. (3) Lỗi / góp ý User gặp khi thử tiếp phần B, C của danh sách thử. (4) Góp ý `bai_hoc/` (bài 23, 25 và bài tra web vừa thêm).
**User tự làm:** 3 việc ở mục "User tự làm" phía trên (đếm bộ kín · xoá nhánh · `.env`).
**Đã trả lời chiều 15/11 (không hỏi lại):** quyền "như sáng 15/11" · chợ Bến Ngự giữ, có cờ · sửa lịch bằng lời: làm cả hai bậc (hạng sao ⇒ ngày đi) — ĐÃ XONG · bỏ dòng báo gửi ảnh cạnh nút · bỏ dòng "Các bước" sau câu trả lời · nút Sửa biểu mẫu — đã sửa · câu hỏi nối tiếp: câu web = câu tìm model viết, **BẬT** · buổi để trống không hiện · Nơi ở chỉ hiện khi người dùng hỏi · User tự tìm ảnh: 10 khách sạn (cơ sở thứ 11 bỏ) + 8 Khám phá (ghép 5, **3 để trống**) · tốc độ: bỏ "tra web sớm", gác "gộp câu tìm" · W82–W84 duyệt; sửa `START_SESSION.md` không chọn · ngày đi xa không thêm ghi chú buổi tối. **Trước đó 15/11:** mưa ≥ 60 % & ≥ 6 mm · Codex mặc định terra · nhớ sở thích: KHÔNG làm · ảnh lưu file + bảng mã bài · Tây Sơn ghi cả hai mốc · câu ngoài kho giá vé đi lại = giới hạn đã nhận · gộp cơ sở trùng, giữ Villa Louise · thêm 7 nơi vào lịch — ĐÃ XONG.
**Cũ còn mở:** (Q-DP, **khi tới deploy AWS** — không hỏi sớm): tra web trên bản công khai (kèm xét lại cờ `web_cau_noi_tiep`) · dòng báo gửi ảnh cạnh nút (bản công khai cần lại) · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền (HUE_SITE phải là tên miền https) · xoá ảnh docker cũ · dòng © OSM nếu bản công khai cần đúng giấy phép. **Không gấp:** vị trí Bảo tàng Cổ vật kho tự mâu thuẫn; xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên; quyển báo cáo + slide + kịch bản demo ⇒ **làm song song giai đoạn deploy** (User 18:31 15/11/2026); nhãn cũ câu "hôm nay âm lịch" trong bộ 30/10.

## Câu hỏi A còn nợ (không cần User)

- **Rà 15/11 (B, `report_agent/2026-11-12_ra_khoang_cach/b_ra_no_cu.md`, 0 USD):** mọi mục nợ 09/11 + "cũ còn mở" đã hết / bỏ / thành giới hạn ghi ở sổ khâu — xoá khỏi đây; 3 mục còn thật: số mục web "8/11 ↔ 08/11" (sửa xong, đếm 0 / 76 cứu ⇒ BỎ), thời tiết "tuần sau" (sửa, merge `5738e8d`), bảng sổ S41–S44 (A sửa `cdd4e60`). Giới hạn giữ: lịch không dời theo giờ tới / về; luật số mục web "1:23" trùng "123" (lỏng, hiếm); USD lượt bị Dừng là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); allow-list thêm bảng lưu trú v2 `data/khach_san_2026-11-14/bang_luu_tru_lich_v2.json` (ĐÃ merge 14/11 tối; thay bảng `data/luu_tru_2026-11-14_lich/bang_luu_tru_lich.json`) + bảng quán `bang_quan_lich_v1.json` md5 `ab481586d46f` + ảnh `frontend/public/anh/khach_san/`; build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Thêm chiều 15/11 (18:24 15/11/2026):** checklist deploy — xét lại cờ `web_cau_noi_tiep` + dòng báo gửi ảnh cạnh nút cho bản công khai; Docker nháp đã trỏ bảng v9 / toạ độ v9 / ảnh lịch v5 / lưu trú v6 (E), chưa build; `git_sha` trong Docker ra `khong_ro`. Theo dõi: đếm lượt `cau_tu_model` + đọc tay câu tra web khi người dùng nêu tên; đếm lượt đổi ngày đi bị người dùng đổi lại ngay; phần code W84 (harness Q3 tự mô phỏng) chưa làm; `tools/kiem_bo.py` bộ sửa lịch mở cả file kín.
- **Còn mở:** B7 lúc đóng code (dự phòng demo mất mạng, đề cương, ý #15–#17); checklist deploy thêm: 5 file bảng + symlink `frontend/public` ⇒ `dist` + dockerignore 263 bài (E đã sửa trong `data/phase_12/deploy_nhap/`, C review ready; test so settings ↔ danh sách CHUA — làm lúc deploy); `.env` 1 dòng tên biến có khoảng trắng (User).

## Session

**Phiên chiều 15/11 (mở 15:08, kết 18:24 15/11/2026; User vắng khoảng 16:20–17:47):** A `hue-rag-60` · B `hue-rag-cb` · C `hue-rag-51` · E `hue-rag-ab` — cả bốn Claude Code (Fable 5.2), trực tiếp; D không mở. Qdrant 1 collection 9.425 điểm. Server thử của User ở cổng 8010 do A mở (tắt lúc kết phiên).

**Phiên 15/11 (mở 09:33, kết 14:42 15/11/2026; User vắng 11:42–14:38):** A `hue-rag-26` · B `hue-rag-b2` · C `hue-rag-f9` · E `hue-rag-3e` — cả bốn Claude Code, trực tiếp; D không mở. Qdrant 1 collection 9.425 điểm. Hai lượt máy cho A `docker-images-src` (dự án khác của User) 10:28–10:31 và lượt 2 tới 10:47 (giờ phiên kia báo) — nhóm ngừng việc nặng trong lúc đó.

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

- **Quyền phiên chiều 15/11 HẾT HẠN (18:24 15/11/2026, kết phiên).** Phiên sau A hỏi lại. (Chiều 15/11: "như sáng 15/11"; lúc vắng không hỏi, ≈ 1 USD; dùng ≈ 0,45.)
- **Quyền phiên 15/11 HẾT HẠN (14:42 15/11/2026, kết phiên).** Phiên sau A hỏi lại. (15/11: "như tối 14/11"; lúc vắng trần ≈ 1 USD, "quá thì vẫn duyệt, miễn hiệu quả"; đạt tiêu chí ghi trước ⇒ bật.)
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
| `data/phase_9/lich_trinh/diem_v9.json` · `diem_toa_do_v9.json` · `bang_anh_v5.json` | bảng điểm lịch 41 điểm · toạ độ · ảnh lịch 40 / 41 (đang chạy) | md5 `eb6cfd95df6b` · `f6068ff37d61` · `5ed8f32903a9` |
| `data/anh_user_2026-11-15_ghep/bang_luu_tru_lich_v6.json` | bảng lưu trú 136 cơ sở, 67 có ảnh (đang chạy) | md5 `44d7b14d8fce` |
| `data/anh_user_2026-11-15/` | ảnh User tự tìm (10 khách sạn + 8 Khám phá; 3 ảnh không dùng) | — |
| `data/sua_lich_hang_2026-11-15/` · `data/sua_lich_ngay_2026-11-15/` · `data/cau_noi_tiep_2026-11-15/` | bộ câu + kết quả đo: đổi hạng chỗ ở · đổi ngày đi · câu hỏi nối tiếp (bộ quyết A viết) | — |
| `data/review_sua_hang_o_2026-11-15/` · `data/review_web_noi_tiep_2026-11-15/` · `data/review_sua_ngay_di_2026-11-15/` | review độc lập (2 của agent con A) + 2 bộ câu dò hàm đọc ngày của E | — |
| `data/nhan_cu_v9_2026-11-15/` | rà nhãn bộ đo sau bảng v9, công cụ mô phỏng có chọn bảng, lệnh đếm bộ kín | — |
| `data/huong_dan_test_user_2026-11-15.md` | danh sách 26 mục User tự thử hệ thống (A viết) | — |
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
