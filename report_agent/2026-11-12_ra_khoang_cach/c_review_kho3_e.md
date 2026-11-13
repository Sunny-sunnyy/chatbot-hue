# Review: kho 3 — bài nháp "Đi lại ở Huế" + phiếu khu lưu trú (việc của E)

Decision: **changes_requested** (1 major ở phiếu lưu trú; bài đi lại: 0 blocker / 0 major, 4 minor)
Người kiểm: C (`hue-rag-eb`, Claude Code)
Date: 20:02 13/11/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` (A duyệt) · luật kho `session_prompt/Session_Prompt.md` §5
Nhãn cơ sở (L-a…L-e): tên / địa chỉ thật chỉ ở file private `data/luu_tru_2026-11-12/nhan_review_c_13_11.md` (sửa 13/11 — bản đầu của file này lỡ ghi tên / địa chỉ cơ sở lấy từ `data/`).
Implementation report: `session_prompt/sessions/STATUS_E.md` (mục 19:52, 19:55 13/11) · `data/luu_tru_2026-11-12/buoc_0_gan_khu.md` mục "Bản 3"

## 1. Phạm vi đã review

- (a) `data/sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue.md` (private, CHƯA vào kho) + bảng dữ kiện `…_DANG_DO.md` + nguồn Codex `data/tra_cuu_cli/2026-11-12_e-di-lai-hue/ket_qua.md`.
- (b) `data/luu_tru_2026-11-12/phieu_khu_luu_tru_cho_user.md` + `tools/gan_khu_v2.py`, `tools/gan_khu_v3.py` + kết quả `luu_tru_theo_cum_nhap*.json`.
- Git: cả hai thư mục nằm trong `data/` (private, không có git) ⇒ không có diff; review trên file hiện có. Không chạm kho, 0 USD.

## 2. Findings

### Phiếu khu lưu trú

**M-1 (major) — "151 cơ sở có hạng" là 151 DÒNG, chỉ 143 cơ sở khác nhau (tên + địa chỉ chuẩn hoá).**
- Vị trí: phiếu dòng 3–4 ("xếp 151 cơ sở…", "83 / 151", "149 / 151"); spec kho 3 Q2 "151 cơ sở có hạng / đạt chuẩn"; `luu_tru_theo_cum_nhap_v3.json`.
- Bằng chứng [Chạy]: trong 151 dòng `co_hang`: 151 `ma_nguon` khác nhau nhưng 143 cặp (tên, địa chỉ) khác nhau, 140 tên khác nhau. 8 cặp lặp: 7 khách sạn có một dòng hạng sao (1–2 sao) **và** một dòng "Đạt chuẩn phục vụ khách du lịch" cùng tên + địa chỉ (danh mục Cục Du lịch xếp hai lần ở hai loại), 1 khu nghỉ dưỡng 5 sao ở Lăng Cô hai mã liền nhau. Thêm 3 tên có hai địa chỉ gần như trùng (vd hai số nhà viết đảo thứ tự trên cùng đường; một dòng có thêm tên phường) ⇒ cần xem tay. Cả 316: 293 cặp khác nhau.
- Tác động: số báo User sai (đúng bẫy "đếm dòng thay vì đếm cơ sở" vòng tự soi 2 ghi); bài lưu trú sinh từ bảng sẽ liệt kê một khách sạn hai lần với hai hạng khác nhau (người đọc không biết hạng nào đúng). Tỉ lệ gán (98 %) không đổi đáng kể vì các cặp lặp cùng khu.
- Tiêu chí đóng: script khử trùng theo (tên chuẩn hoá, địa chỉ chuẩn hoá) — giữ dòng hạng sao, bỏ dòng "đạt chuẩn" trùng (hoặc nêu quy tắc khác); 3 cặp địa chỉ gần trùng đọc tay; phiếu + biên bản + spec (A sửa dòng Q2) ghi số cơ sở thật kèm lệnh tính lại.

**m-1 (minor) — bảng A xếp "Hương An" vào khu (2) Phía tây yên tĩnh (Kim Long, Thuỷ Xuân).** Hương An nằm phía tây bắc dọc Quốc lộ 1 (bến xe phía Bắc ở 132 Lý Thái Tổ, p. Hương An — KH 155/2026). Không phải lỗi máy, nhưng là ô User nên được gợi ý xem; ghi một chữ "cần xem" cạnh ô.

**Đã kiểm, không có finding:** 67 dòng gán bằng OSM (đọc tay cả 67, kỹ ~12 đường của lõi hai bờ): địa chỉ đều "Thành phố Huế", đường đều thuộc lõi hai bờ — khớp. Rủi ro C dò thêm: khung lọc OSM là cả tỉnh (`KHUNG` 16,0–16,8 / 107–108) nên đường trùng tên ở thị xã khác có thể lọt — với 151 dòng này **không xảy ra** (0 / 67 địa chỉ ghi thị xã / huyện), và đoạn > 2 km bị bỏ qua chứ không kéo khu. Dòng cơ sở L-a để "cần xem" là đúng (đường dài, 6 đoạn lõi / 3 đoạn tây). Một địa chỉ chỉ ghi tên huyện bị tách nhầm thành tên đường nhưng rơi vào "chưa xác định" ⇒ vô hại, đã nằm ở bảng D.

### Bài nháp "Đi lại ở Huế"

Luật kho §5: bắt đầu bằng `#` ✓ · không giá (chỉ câu "hỏi rõ giá trước") ✓ · không số điện thoại ✓ · không giờ tàu (chỉ "khoảng 3 giờ" là thời lượng, có trong kho) ✓ · không mục rỗng ✓ · `## Nguồn dữ liệu` tối giản ✓. Đối chiếu từng ý: các ý không có trong bảng dữ kiện của E đều tìm thấy trong kho qua `scripts/grep_kb.sh` (8 ý, ở mức loại: địa chỉ ga · xe điện trong Đại Nội · điểm đón và lộ trình xe buýt tham quan · xích lô và lời mời chào · khoảng cách và đường tới một lăng · bến và mùa ngừng của thuyền rồng · thời lượng tàu du lịch · quy định xe máy qua hầm).

- **m-2** — `## Nguồn dữ liệu` thiếu các bài kho thật sự dùng: *Vịnh Lăng Cô* (tàu ~3 giờ), *Đèo Hải Vân* (hầm), *Đồi Vọng Cảnh* (mưa nhiều tháng 10–11), *heritage-guides* / bài thuyền rồng. Đóng: thêm tên bài.
- **m-3** — "mua vé được cho từng chặng" chỉ có nguồn Codex (bài báo 2024), không thấy trong kho, E không ghi đã mở. Đóng: mở trang ĐSVN kiểm, hoặc bỏ cụm này.
- **m-4** — "khách thường đi taxi hoặc xe đưa đón đặt trước" không có nguồn (chính bảng của E ghi taxi / xe đưa đón sân bay "chưa xác nhận"). Đóng: viết nhẹ hơn ("có thể đi taxi hoặc xe đưa đón đặt trước") hoặc bỏ "thường".
- **m-5** — xe buýt sân bay: câu đúng theo nguồn 2024 và viết đúng thì quá khứ, nhưng nguồn Codex còn có phụ lục QĐ 696/QĐ-UBND 23/02/2026 liệt kê điểm dừng xe buýt phục vụ khách đi sân bay (không chứng minh có tuyến chạy). Đóng: thêm "chưa thấy thông báo tuyến chạy lại" hoặc ghi ngày nguồn trong câu; để A quyết có cần tra lại không.
- Ghi chú (không phải finding, báo A theo §5 "web mâu thuẫn kho"): kho ghi Ga Huế **số 2** Bùi Thị Xuân; trang vi.wikipedia «Ga Huế» C mở 12/11 ghi **số 1** (mốc ga trong `dung_quan_theo_cum.py` của C). Bài theo kho — đúng luật; không tự chọn một phía.

## 3. Cách người kiểm chạy lại thật

- `python3 -I data/luu_tru_2026-11-12/tools/gan_khu_v2.py && python3 -I data/luu_tru_2026-11-12/tools/gan_khu_v3.py` (sao lưu 2 file kết quả vào `/tmp/c_rv/` trước).
- Ca dò của C (cách khác người làm): đếm khác nhau theo `ma_nguon` / tên / (tên + địa chỉ) chuẩn hoá; liệt kê tên trùng có địa chỉ khác; lọc địa chỉ có tên thị xã / huyện trong 67 dòng OSM.
- `scripts/grep_kb.sh` cho mọi ý của bài đi lại (không grep thẳng kho).
- WebFetch 3 ý chính: (1) `tuongtac.hue.gov.vn/…a161839.html` — "kể từ ngày 01/4/2024" chấm dứt, "chưa có đơn vị kinh doanh vận tải tham gia", xử lý 30/09/2024 ✓; (2) toàn văn Luật 36/2024/QH15 trên xaydungchinhsach.chinhphu.vn — Điều 34 (xe gắn máy ≤ 50 cm³ / ≤ 4 kW / ≤ 50 km/h), Điều 57.1 (A1 đến 125 cm³ / 11 kW; A trên mức đó), Điều 59.1 (16 tuổi xe gắn máy; 18 tuổi A1, A), Điều 57.8.b (GPLX quốc tế kèm GPLX quốc gia đúng hạng, còn hạn) ✓; (3) PDF phụ lục KH 155/KH-UBND 23/3/2026 (đọc bằng `pdftotext`) — Bến xe phía Nam 97 An Dương Vương, p. An Cựu; phía Bắc 132 Lý Thái Tổ, p. Hương An; cả hai do Công ty CP Bến xe Huế quản lý ✓.

## 4. Kết quả quan sát

- Tái lập: **149 / 151 (98 %)** dòng có hạng gán được khu; cả 316: 310 (98 %) — khớp số E báo; md5 hai file kết quả trùng bản E (`44c21cd65876`, `07e26100cefb`) ⇒ chạy lại không đổi dữ liệu.
- Khử trùng: 151 dòng ⇒ 143 cơ sở (M-1).
- Bài đi lại: 3 / 3 ý kiểm trên trang gốc khớp; 0 vi phạm luật kho; 4 minor về nguồn / cách viết.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại bộ chia đoạn thử của E cho bài đi lại (E báo 12 đoạn / 0 lỗi; bài không đổi từ lúc đó — dùng lại, không gọi là lần chạy mới).
- Không kiểm ngoài đời các khách sạn còn hoạt động; không xem ảnh / bản đồ.

## 6. Decision và bước tiếp theo

**changes_requested** cho phiếu lưu trú (M-1: khử trùng rồi in lại số trước khi đưa User). Bài đi lại: sửa m-2…m-5 trong một lượt khi ghi kho, không cần vòng review riêng. E sửa ⇒ C kiểm lại phần đổi (số cơ sở, phiếu dòng 3–4, bảng C cột "Số cơ sở").

## 7. Kiểm lại phần sửa (vòng 2) — 20:06 13/11/2026 (`date`)

Decision: **ready_for_user_confirmation** (M-1, m-1…m-5 đóng; 0 finding mới).

- **M-1 đóng.** Chạy lại `python3 -I data/luu_tru_2026-11-12/tools/gan_khu_v2.py && python3 -I data/luu_tru_2026-11-12/tools/gan_khu_v3.py`: in "316 dòng ⇒ 292 cơ sở; có hạng 151 dòng ⇒ 142 cơ sở", gán **140 / 142 (98 %)**; chạy lại không đổi file (md5 v3 trước = sau). Ca dò của C trên file kết quả: 292 dòng = 292 cặp (tên, địa chỉ) khác nhau; 142 dòng có hạng = 142 cặp; tổng `ma_trung` 24 = 316 − 292 ✓. Dòng giữ là dòng hạng sao (vd cơ sở L-b giữ mã hạng sao, mã "đạt chuẩn" vào `ma_trung`) ✓. Cơ sở L-c gộp (cùng số nhà, một dòng có thêm tên phường) — hợp lý. L-d (hai số nhà viết đảo thứ tự) và L-e (hai số nhà gần nhau cùng đường) để User chọn ở bảng E mới — đúng cách (không tự đoán).
- Phiếu: dòng 3–4 ghi 142 cơ sở + giải thích 151 dòng; bảng C "23 đường, 63 cơ sở" khớp file (64 dòng gán theo OSM − 1 dòng "cần xem" ở bảng D).
- **m-1 đóng:** Hương An tách dòng riêng, ghi "cần xem" (hiện 0 cơ sở ghi phường này).
- **m-2 đóng:** E chỉ ra hai ý đã có nguồn — kiểm: "đỉnh điểm tháng 10 – 11" có trong `heritages/heritage-guides.md` (bài Cẩm nang, đã có trong danh sách nguồn; qua `grep_kb.sh`); "khoảng 3 giờ" có trên trang ĐSVN (WebFetch, dưới). Thêm bài Đèo Hải Vân ✓. Phần C nêu ở vòng 1 là thiếu sót của C.
- **m-3 đóng:** WebFetch `ketnoidisan.dsvn.vn` 20:06 13/11/2026: trang liệt kê 6 hành trình mua vé (Huế – Lăng Cô, Lăng Cô – Đà Nẵng, Huế – Đà Nẵng và chiều ngược) + "khoảng 3 giờ đồng hồ"; bảng giờ trên trang không thống nhất (vd HĐ1 7:05–10:10 ↔ 07:45–10:35) ⇒ bài không ghi giờ là đúng.
- **m-4 đóng:** "có thể đi taxi hoặc xe đưa đón đặt trước". **m-5 đóng:** thêm "tới tháng 11/2026 chưa thấy thông báo tuyến chạy lại".
- Không chạy lại bộ chia đoạn (E báo 12 đoạn / 0 lỗi sau sửa — dùng lại, không gọi là lần chạy mới).
- md5 lúc kiểm: d736f5a6c21e  luu_tru_2026-11-12/luu_tru_theo_cum_nhap_v3.json;2f4772b5f3c3  luu_tru_2026-11-12/phieu_khu_luu_tru_cho_user.md;1ccfc5f639d6  sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue.md;
- Còn mở (không thuộc review): lệch Ga Huế số 2 (kho) ↔ số 1 (vi.wikipedia) — A quyết; A sửa số ở spec kho 3 Q2 (151 ⇒ 142).
