# Đợt bổ sung kho 3 — lưu trú · đi lại · ăn gần — tài liệu thiết kế (NHÁP bản 2, chờ User duyệt một lần)

Người viết: E · 21:13 12/11/2026 (`date`) · A giao sau khi User chốt 20:54 12/11/2026: "chỗ nào Huế TRIPO hơn thì học; phần nào cần dữ liệu thì tìm, cào, bổ sung". Review: C.
Khuôn theo spec sửa kho cũ `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` và đợt giờ mở cửa 05/11 (`data/sua_kho_2026-11-05_gio/tools/chay.sh`).
**Mức rủi ro: cao** (thêm nội dung vào kho curated + dựng lại chỉ mục + **nguồn dữ liệu mới từ ngoài**) ⇒ User duyệt spec này một lần; từng bảng dữ liệu vào kho User xem lướt trước khi ghi.

**Bản 2 (21:31 12/11/2026, `date`):** sửa theo review của C (`2026-11-12-bo-sung-kho-dot-3-design_review.md`: 3 major, 7 minor) **và** mức lịch trình User chốt tối 12/11 (A báo): lịch "đủ 4 phần, 1 lịch" — tham quan · **ăn uống theo buổi** · **lưu trú** · **buổi tối** (+ ảnh, bản đồ) ⇒ đợt này là đường găng của phần ăn uống + lưu trú; **khuyến nghị Q3 đổi chiều** (nêu rõ ở mục 2). Bảng "Chỗ đổi" cuối file.

## Căn cứ để review
- Lỗi đã đếm: `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` (lưu trú, ăn gần) · `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` mục 3e (đi lại) · `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v5.md` (chỗ TRIPO hơn).
- Nguồn dữ liệu: `report_agent/2026-11-12_ra_khoang_cach/e_nguon_luu_tru.md`; dữ liệu đã tải (private) `data/luu_tru_2026-11-12/` (`bien_ban.json`); dữ liệu "ăn gần" của C (private) `data/sua_kho_2026-11-12_an_gan/`.
- Luật kho: `session_prompt/Session_Prompt.md` §5 (curated Markdown, sao lưu, không enrich bằng web khi chưa duyệt phạm vi); quy trình dựng lại: `guides/full_corpus_rag.md` mục "Build lại index".

## 1. Mục tiêu
Ba loại câu khách du lịch hỏi tự nhiên mà kho hôm nay **không có dữ liệu** (đã đếm), làm trong **một** lần dựng lại chỉ mục:

| Phần | Lỗi đã đếm | Thêm gì vào kho |
|---|---|---|
| **(a) Cơ sở lưu trú** | câu hỏi cơ sở cụ thể: 3 / 4 kho từ chối; TRIPO có danh mục | bài **theo khu × loại** từ danh mục chính thức — không giá, không liên hệ |
| **(b) Đi lại / thuê xe** | 4 / 6 kho từ chối; 2 / 6 không nơi nào trả lời (thuê xe, giá dịch vụ) | 1–2 bài dịch vụ đi lại — hình thức, nơi tìm, lưu ý; **không giá cứng** |
| **(c) Ăn gần một điểm** | 5 / 6 câu không đủ dùng từ kho | câu định vị cho bài quán có toạ độ **chắc** + một bài "ăn gì quanh các điểm tham quan chính" |

Không đổi: chunker, model, lời dặn, luật closed-world, câu từ chối chuẩn. Không thêm công cụ.

## 2. Quyết định cần User chốt (mỗi câu có khuyến nghị; A hỏi từng câu)
- **Q1 — Lưu trú vào kho dạng gì.** (a) **Bài Markdown theo khu + một bảng có cấu trúc sinh từ cùng dữ liệu** (khuyến nghị): bài cho đường hỏi đáp (có trích dẫn); bảng `data/…/luu_tru_theo_cum.json` cho **lịch trình** (code chọn 2–3 cơ sở theo cụm của lịch — spec biểu mẫu của C). Một nguồn, hai dạng, sinh bằng cùng script. *Khi nào sai:* ~300 tên riêng làm nhiễu tầng tìm của câu khác — tiêu chí §6 đo; *mất gì nếu chọn khác:* (b) bảng do code đọc + công cụ lọc ⇒ chính xác hơn nhưng là công cụ mới (plan + đo riêng, không còn là "bổ sung kho").
- **Q2 — Lấy cơ sở nào.** (a) **Chỉ cơ sở có hạng sao hoặc "đạt chuẩn phục vụ khách du lịch"** (khuyến nghị — ít mà chắc); (b) mọi bản ghi kể cả "cơ sở tự đăng ký" (nhiều hơn, chất lượng không đều). **Số thật đã tải (21:12–21:15 12/11/2026, 73 trang, `data/luu_tru_2026-11-12/bien_ban.json`): 316 cơ sở** — loại hình: khách sạn 306 · biệt thự du lịch 6 · nhà nghỉ 2 · khác 2 (**0 homestay / nhà ở có phòng cho thuê** ⇒ danh mục này gần như chỉ có khách sạn); hạng: 5 sao 11 · 4 sao 13 · 3 sao 8 · 2 sao 31 · 1 sao 49 · "đạt chuẩn phục vụ khách du lịch" 39 · "khác" 138 · không ghi 27; nguồn nhập đọc được: cơ quan nhà nước 191 · tự đăng ký 9 · chưa đọc được nhãn 116. **Đếm lại sau review (nhãn nguồn đọc trực tiếp từ HTML thô): cơ quan nhà nước nhập 191 (có hạng sao 35 · "đạt chuẩn" 37 · khác / không ghi 119) · cơ sở tự đăng ký 9 · không có nhãn nguồn 116 (có hạng sao 77 · đạt chuẩn 2 · khác 37).** ⇒ định nghĩa (a) sửa thành **"có hạng sao hoặc đạt chuẩn, bất kể nhãn nguồn" = 151 cơ sở** (112 có sao + 39 đạt chuẩn); (b) = 316. Số 151 của bản 1 đúng theo định nghĩa này, không đúng theo chữ "do cơ quan quản lý nhập" — đã sửa chữ.
- **Q3 — Quán cho các cụm kho đang thiếu (Đại Nội, Thiên Mụ…).** Kho chỉ có 1 quán có toạ độ quanh Đại Nội, 0 quanh Thiên Mụ và các lăng; dữ liệu mở có 276 cơ sở / 1 km quanh Đại Nội, 174 quanh Thiên Mụ, **0 quanh các lăng**. **Khuyến nghị ĐỔI so với bản 1** vì User đã chốt lịch phải có "ăn uống theo buổi": **(b) thêm quán từ dữ liệu mở cho các cụm thiếu, theo luật chọn ghi trước, có nhãn** (khuyến nghị): tối đa **6 quán / cụm** cho cụm có < 3 quán kho; chọn theo thứ tự (i) trùng tên với món / quán kho đã nhắc, (ii) gần điểm tham quan của cụm nhất, (iii) có đủ tên + số nhà + đường; **chỉ lấy tên · địa chỉ · toạ độ** (không điện thoại, email, mã số thuế); mỗi dòng ghi "theo dữ liệu mở của thành phố (bản 08/2026), **chưa kiểm chất lượng / còn mở cửa hay không**"; User xem lướt từng dòng. *Khi nào sai:* quán đã đóng / kém ⇒ lịch gợi ý sai — giảm bằng nhãn + link bản đồ để người dùng tự kiểm. *Chọn khác mất gì:* (a) không thêm ⇒ ngày ở cụm Đại Nội / Thiên Mụ **không có dòng bữa ăn** (spec biểu mẫu khi đó phải ẩn phần ăn uống ở các ngày ấy). **Khu lăng: dữ liệu mở cũng 0** ⇒ cả hai phương án đều nói thật "khu này chưa có quán trong dữ liệu; cụm gần nhất có quán là …, cách ~x km".
- **Q4 — Toạ độ ước (22 / 29 toạ độ quán kho là ước từ số nhà kề; sai số trung vị 107 m, 95 % ≤ 522 m).** (a) **Hai mức dùng** (khuyến nghị, theo review): toạ độ **chắc / vừa (7 bài)** ⇒ được ghi khoảng cách ("cách <điểm> khoảng 0,3 km"); toạ độ **ước** ⇒ chỉ dùng ở mức **"cùng cụm"** (gán cụm khi quán cách tâm cụm < bán kính cụm − 522 m; sát ranh ⇒ không gán), **không ghi mét**. (b) chỉ dùng 7 bài chắc ⇒ quá ít cho lịch. **Chốt sau lượt tra toạ độ bổ sung** (A đang lo phần tra địa chỉ ngoài) — số bài mỗi mức ghi vào phiếu trước khi User duyệt.
- **Q5 — Mức giá lưu trú.** (a) **Không ghi mức giá** (khuyến nghị — nguồn không có; quyết định 05/11 "không nói giá phòng"); (b) ghi "mức ước theo hạng" bằng luật cố định (1–2 sao / nhà nghỉ = bình dân · 3 sao = tầm trung · 4–5 sao = cao cấp) kèm nhãn "ước theo hạng, không phải giá".

## 3. Nội dung từng phần

### (a) Lưu trú
- **Nguồn:** Cơ sở dữ liệu du lịch quốc gia (Cục Du lịch Quốc gia Việt Nam), bộ lọc "Thành phố Huế"; đã tải 12/11/2026 (316 cơ sở; **chỉ** tên · loại hình · xếp hạng · địa chỉ · nguồn nhập). Đối chiếu hạng 4–5 sao với danh sách của ngành du lịch thành phố (nhập tay, ghi nguồn).
- **Gán khu — sửa theo số đếm thật:** địa chỉ trong danh mục **gần như không có phường / xã** (3 / 316 có "phường", 11 có "xã"; đa số chỉ "số nhà + đường, Thành phố Huế") ⇒ không gán khu theo phường được. Cách làm: ước toạ độ từ **số nhà + tên đường** bằng đúng phương pháp "số nhà kề" C đã dựng cho quán (bộ dữ liệu mở 6.794 cơ sở có toạ độ) ⇒ gán vào **cụm của bảng lịch trình** (cùng tên cụm với bảng điểm, để lịch và hỏi đáp dùng chung) ⇒ gom 3 nhóm khu mà kho đã dùng ở mục "nên ở khu nào". **Bước 0 đếm (0 USD):** tỉ lệ gán được cụm; cơ sở không gán được ⇒ nhóm "chưa xác định khu" (vẫn vào bài tổng theo hạng, không vào bài theo khu). Dưới 70 % gán được ⇒ báo A trước khi soạn.
- **Vị trí file — sửa M-1:** đặt trong thư mục **đã được quét** `travel/services/` (tên file bắt đầu "Lưu trú ở Huế — …") ⇒ **không sửa `include_globs`**, không sửa danh sách chừa Docker. (Thư mục mới `travel/lodging/` của bản 1 sẽ **không vào chỉ mục** mà build vẫn chạy xong — C bắt đúng.)
- **Dạng bài — sửa M-2 (đã chạy thử bộ chia đoạn, chỉ đọc, bài mẫu tự đặt):** (i) dạng "mỗi cơ sở một mục danh sách" ⇒ **mỗi dòng một đoạn**, đoạn có kèm tên bài + tên mục (14 dòng ⇒ 14 đoạn, 0 lỗi) — tốt cho câu hỏi một cơ sở, **kém cho câu danh sách** (11 khách sạn 5 sao = 11 đoạn, ngữ cảnh chỉ 10); (ii) dạng **đoạn văn liệt kê**: 8 cơ sở / đoạn vừa (617 ký tự), 14 cơ sở / đoạn **lỗi** (vượt token, không cắt câu được). ⇒ **Chọn: đoạn văn liệt kê, tối đa 6 cơ sở / đoạn**, mỗi đoạn mở bằng câu tự đủ nghĩa "Khách sạn <hạng> ở <khu> (theo danh mục ngành du lịch, lấy ngày 12/11/2026), phần k / n: …". Gồm:
  - **một bài tổng** "Lưu trú ở Huế — khách sạn xếp hạng 3–5 sao" (32 cơ sở ⇒ ~6 đoạn; trả lời câu "khách sạn 5 sao / 4 sao nào");
  - **một bài mỗi nhóm khu** (3 nhóm + "chưa xác định khu"), mục theo hạng (4–5 sao · 3 sao · 1–2 sao · đạt chuẩn · [chưa xếp hạng — chỉ khi Q2 = (b)]); đầu bài một đoạn "khu này hợp với ai" **chép ý từ bài cẩm nang có sẵn**.
  - Ước số đoạn thêm: Q2 (a) 151 cơ sở ⇒ ~35–45 đoạn; Q2 (b) 316 ⇒ ~70–85 đoạn (trên 8.435) — nhỏ hơn nhiều so với bản 1 (+150–320) ⇒ rủi ro chen tầng tìm thấp hơn.
- **Bảng cho lịch trình** (cùng script, private): `luu_tru_theo_cum.json` — `ten`, `loai_hinh`, `xep_hang`, `dia_chi`, `cum`, `muc_toa_do` (chắc / ước), `ma_nguon`. Trường khớp với spec biểu mẫu của C (hai bên nhắn thẳng khi đổi tên trường).
- **Bắt buộc trong bài:** dòng "Danh sách theo danh mục của Cục Du lịch Quốc gia Việt Nam, lấy ngày 12/11/2026; hạng theo danh mục, có thể đã đổi; **không gồm giá phòng**; danh mục chủ yếu là **khách sạn đã đăng ký với ngành du lịch** — chưa gồm homestay / nhà dân." Mục `## Nguồn dữ liệu` tối giản.
- **Cấm:** giá, điện thoại, email, tên chủ cơ sở, nhận xét chất lượng, link đặt phòng.
- **Kết cục mong muốn ghi trước cho hai loại câu khó (K4):** câu "khách sạn **giá rẻ**" ⇒ trả lời bằng nhóm 1–2 sao / đạt chuẩn của khu được hỏi + câu "kho không có giá phòng" (không nêu số tiền); câu **homestay** ⇒ kho từ chối phần danh sách (danh mục không có) — người dùng vẫn có thẻ "khu nên ở + link bản đồ" và các mục homestay sẵn có trong bài điểm tham quan.
- **Một dòng code thuộc spec này:** thêm tiền tố file lưu trú vào danh sách nguồn kích dòng "có thể đã thay đổi" (`backend/llm/assistant.py` `NOTICE_SOURCE_PREFIXES`) + 1 test.

### (b) Đi lại / thuê xe
- **1 bài chắc chắn + 1 bài tuỳ dữ liệu** (`travel/services/`): **"Đi lại ở Huế"** — từ sân bay / ga / bến xe vào trung tâm (các hình thức: xe buýt sân bay, taxi, xe công nghệ, xe đưa đón), đi tới nhóm lăng phía tây nam (taxi / thuê xe máy / thuyền / xe tham quan), đi trong nội thành (xích lô, xe đạp, đi bộ), lưu ý an toàn (đường đèo, mùa mưa, giấy tờ khi thuê xe máy). **"Thuê xe ở Huế"** chỉ viết nếu tìm được ≥ 2 nguồn công khai đáng tin cho từng ý.
- **Nguồn đề xuất (User duyệt phạm vi enrich bằng web):** cổng / trang chính quyền thành phố và Sở Du lịch, trang Cảng hàng không Phú Bài, trang ga Huế / Đường sắt Việt Nam, trang Trung tâm Bảo tồn Di tích (xe điện, thuyền), quy định pháp luật về giấy phép lái xe; bổ sung từ **đoạn có sẵn trong kho** (kho đã nhắc "thuê xe" ở 9 bài, "taxi" ở 23 bài — gom lại, ghi nguồn bài). Không lấy từ mạng xã hội / trang đại lý.
- **Không giá cứng:** không ghi số tiền thuê xe / cước; chỉ "giá thay đổi theo mùa và nhà cung cấp — hỏi trước khi thuê". Số điện thoại tổng đài hãng: không ghi (cũ nhanh).
- Mỗi ý trong bài ghi nguồn + ngày xem ở `## Nguồn dữ liệu`; web mâu thuẫn kho ⇒ ghi cả hai, báo A.

### (c) Ăn uống gần điểm tham quan — cho hỏi đáp **và** cho dòng bữa ăn của lịch
- **Một bảng nguồn `quan_theo_cum.json`** (private, User xem lướt): mỗi quán — `ten`, `dia_chi`, `cum`, `nguon` (`kho` / `du_lieu_mo`), `muc_toa_do` (`chac` / `vua` / `uoc`), `bai_kho` (nếu là bài kho), `diem_gan` + `khoang_cach_m` (**chỉ khi** mức chắc / vừa). Quán kho: 29 bài có toạ độ (7 chắc / vừa + 22 ước) + số bài tra thêm; quán dữ liệu mở: theo Q3.
- **Điểm mốc:** ngoài điểm tham quan của bảng lịch trình, thêm **3–5 mốc không phải điểm tham quan** mà khách hay lấy làm chuẩn (cầu, ga, chợ, bến xe — danh sách chốt ở phiếu; một câu đã đếm hỏi quanh một cây cầu).
- **Câu định vị cho bài quán kho** (`foods/restaurants/`, `foods/cafes/`): thêm **một dòng**; mức chắc / vừa ⇒ "Vị trí: cách <mốc> khoảng <x>" (làm tròn 50 m dưới 300 m, 0,1 km từ 300 m); mức ước ⇒ "Vị trí: thuộc khu <tên cụm>, gần <mốc chính của cụm>" (**không số mét**). Bài đã có câu định vị: không thêm.
- **Một bài tổng hợp mới** `foods/Ăn gì gần các điểm tham quan ở Huế.md`, sinh **từ bảng**: mỗi cụm / mốc một mục, đoạn văn liệt kê ≤ 6 quán (cùng luật chia đoạn như lưu trú); quán từ dữ liệu mở đứng mục con riêng có nhãn "chưa kiểm". **Cụm không có quán** (khu lăng): ghi **dữ kiện tính được**, không ghi nhận định — "Trong dữ liệu chưa có quán sát khu <cụm>. Cụm gần nhất có quán trong kho là <cụm>, cách khoảng <x> km." (thay câu "khách thường ăn ở …" của bản 1 vì không có nguồn). Câu này nằm **trong kho**, có trích dẫn.
- **Chạy thử trước khi chốt ngưỡng K6 (0 USD):** in số quán mỗi mục theo Q3 / Q4 đã chọn; mục < 2 quán ghi rõ. Ngưỡng K6 dưới đây áp cho phương án khuyến nghị; User chọn khác ⇒ A chốt lại số **trước** khi ghi kho.

### (d) Buổi tối (thêm ở bản 2 theo mức User chốt)
Lịch cần điểm / hoạt động buổi tối; bảng lịch trình hiện có 3 điểm chỉ buổi tối + 1 điểm cả ba buổi. Kho **đã có** bài về phố đi bộ (3 bài ghi rõ thứ hoạt động), bài vé biểu diễn / trải nghiệm sông Hương (có khung giờ tối), bài nghệ thuật trình diễn ⇒ **không thêm nội dung kho ở đợt này**; việc cần làm là đưa các hoạt động đó thành **dòng của bảng điểm** (cột thứ hoạt động, giờ) — thuộc phiếu bảng điểm + spec biểu mẫu của C. Spec này chỉ ghi phụ thuộc; nếu C đếm ra < 5 hoạt động tối có căn cứ kho ⇒ bổ sung kho ở một đợt sau, có phiếu riêng.

## 4. Các bước (người làm ↔ người kiểm khác nhau; bước 3–7 làm liền một lần)
0. **Bộ "trước":** tới lúc làm sẽ có ≥ 3 nhánh chạm đường trả lời đã merge (hết lượt tìm, Exa, lưu trú) ⇒ **chạy lại** Golden 176 + an toàn 32 trên `main` lúc đó (≈ 0,09 USD), không dùng lại số B7 giữa kỳ. Ba bộ câu mới (§6) chạy "trước" 1 lượt (≈ 0,04). **Bước đếm 0 USD trước khi soạn:** tỉ lệ gán cụm cho cơ sở lưu trú; số quán mỗi cụm / mốc.
1. **Soạn** (E): bài lưu trú sinh **bằng script** từ bảng sạch (không gõ tay tên cơ sở); bài đi lại soạn tay từ nguồn đã duyệt; câu định vị áp bằng script từ bảng của C. Mỗi file mới / sửa có diff.
2. **User xem lướt** bảng lưu trú (theo khu) + bài đi lại + danh sách câu định vị ⇒ duyệt / sửa. **C review** diff: luật curated, không giá / liên hệ, mỗi ý bài đi lại có nguồn.
3. **Sao lưu:** file quán bị sửa ⇒ `knowledge-base-hue/meta/backup_dot_3_2026-11-12/`; snapshot Qdrant; chép build record + sparse state ra `data/sua_kho_2026-11-12_dot_3/backup/`.
4. **Ghi kho** + **chia đoạn thử, chỉ đọc**: 0 lỗi, mỗi đoạn vừa 3 tokenizer; test mẫu chunker (không file mẫu nào bị chạm — xác nhận).
5. **Dựng lại tại chỗ:** xoá đủ ba đích (collection, build record, sparse state) rồi build (CPU, ~vài chục phút); script có bước 0 kiểm khoá + tự lùi như `chay.sh` 05/11.
6. **Kiểm sau build:** `/health` 5 / 5; cổng ổn định; **đếm đoạn theo nguồn trong chỉ mục: số đoạn của mỗi file mới = số đoạn chia thử, và ≠ 0** (bắt lỗi "file không được quét"); **T1 mới** (158 câu) ⇒ so từng câu với T1 cũ `64656a87c109`, tách hai nhóm: câu có đoạn mới lọt vào 10 đoạn đầu · câu đổi 10 đoạn đầu **không** do đoạn mới (phải bằng 0 — khác 0 ⇒ dừng, tìm nguyên nhân).
7. **Nhãn đoạn đúng v6:** chỉ thêm dòng / thêm file ⇒ trích dẫn cũ tìm lại nguyên văn; `chunk_id` dồn ở file quán bị thêm dòng ⇒ dựng v6 bằng công cụ có sẵn, 0 trích dẫn mất.
8. **Đo "sau"** (§6) ⇒ chấm cùng lượt mù với "trước".
9. **Báo cáo + bài học:** sổ ghi việc (khâu kho, chia đoạn, tìm), `bai_hoc/` bài 1 + bảng tổng bài 19, `Project_Status.md` §4 (số file, số đoạn, sha).
**Dừng + lùi:** chia đoạn lỗi / build lỗi / `/health` không đạt / sàn §6 vỡ ⇒ xoá file mới, chép lại file quán từ bản sao, khôi phục snapshot + build record + sparse state, khởi động lại, cổng ổn định. Lùi là **toàn bộ đợt** hoặc **bỏ riêng phần gây vỡ sàn rồi dựng lại** (A quyết theo số đo).

## 5. Thứ tự với việc khác
- Plan **"khu nên ở + link bản đồ"** (đã duyệt, chưa code) làm **trước hoặc song song** — không phụ thuộc đợt này; sau đợt này danh sách "mục kho về lưu trú" của plan đó thêm các bài "Lưu trú ở Huế — …" trong `travel/services/` (một dòng cấu hình).
- Làm sau khi nhánh "hết lượt tìm" merge (đổi hành vi tìm thêm ⇒ bộ "trước" phải đo trên code đã merge).
- **Trước lượt B7 cuối** (lượt cuối đo trên kho đã bổ sung).

## 6. Tiêu chí nghiệm thu (ghi trước)
| # | Tiêu chí | Bộ | Mức |
|---|---|---|---|
| K1 | Không làm hỏng câu cũ | Golden 176 trước ↔ sau, chấm cùng lượt mù | Đủ / Đúng TB theo cặp ≥ −0,1; câu tụt ≤ 4; từ chối nhầm ≤ trước + 1; 0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật / trích dẫn mới |
| K2 | An toàn | 32 câu ×1 (ca mới ⇒ thủ tục sinh lại 3 lần, hai người chấm cùng gắn) | 4 số như mọi bậc |
| K3 | Tầng tìm câu cũ không bị đoạn mới chen | T1 158 câu: số câu có **đoạn mới** (lưu trú / quán dữ liệu mở / đi lại) lọt vào 10 đoạn đầu; số câu đổi 10 đoạn đầu không do đoạn mới | ≤ 5 câu, 0 câu mất đoạn đúng (nhãn v6) vì bị chen; nhóm thứ hai = 0 |
| K4a | Lưu trú — **câu danh sách theo hạng / khu** ("khách sạn 4–5 sao nào", "khách sạn ở khu …") | 6 câu (2 câu cơ sở cụ thể đã đếm thuộc loại này + 4 mới) | kho trả lời có trích dẫn, tên nêu ra đều có trong bài: ≥ 5 / 6 |
| K4b | Lưu trú — **câu "gần điểm X"** | 4 câu (2 đã đếm + 2 mới) | ≥ 2 / 4 trả lời đúng khu của điểm X (phụ thuộc tỉ lệ gán cụm — ngưỡng thấp có chủ ý) |
| K4c | Lưu trú — câu "giá rẻ" · câu homestay · mọi câu | 2 câu + cả bộ | đúng kết cục ghi trước ở §3 (a); **0 câu nêu giá phòng**; 0 cơ sở ngoài bài |
| K5 | Đi lại | 6 câu của lượt đếm 12/11 + 6 câu mới (người viết ≠ E) | kho trả lời đủ dùng ≥ 8 / 12 (trước: 2 / 6); 0 số tiền cước / giá thuê trong câu trả lời |
| K6 | Ăn gần | 6 câu của lượt đếm + 6 câu mới (2 câu quanh lăng, 1 câu quanh một mốc không phải điểm tham quan) | đủ dùng ≥ 7 / 12 (trước: 1 / 6) — **ngưỡng áp cho Q3 (b) + Q4 (a); chốt lại sau bước đếm số quán mỗi mục nếu User chọn khác**; câu quanh lăng: trả lời đúng dữ kiện "chưa có quán sát khu này; cụm gần nhất …" có trích dẫn; **0 tên quán ngoài bảng**; quán dữ liệu mở khi được nêu phải kèm ý "chưa kiểm" |
| K7 | Kho sạch | mọi file mới / sửa | 0 giá phòng, 0 điện thoại / email, 0 YAML frontmatter, có `## Nguồn dữ liệu` + ngày lấy; hook pre-commit không liên quan (kho không commit) |
| K8 | Tốc độ / tiền (theo dõi) | log | USD / câu và thời gian tìm không tăng quá nhiễu (kho +3–4 % đoạn) |
"Đủ dùng" chấm bằng 2 người chấm mù, tính khi cả hai cùng gắn. Không bộ kín (đợt dữ liệu, không chỉnh lời dặn).

## 7. Rà khung AI FDE — phần nguồn dữ liệu mới (`agent-security-review`)
| Mục | Hiện trạng / thiết kế | Khớp · rủi ro |
|---|---|---|
| Nguồn ngoài đi vào kho | danh mục cơ quan nhà nước (HTML công khai, không điều khoản cấm, không `robots.txt`); **dữ liệu mở thành phố (đã tải 08/2026) — bản 2 lấy cả tên + địa chỉ quán**; trang chính quyền cho bài đi lại | khớp — mỗi nguồn ghi tên + ngày trong bài; file dữ liệu mở về quán có **điện thoại, email, mã số thuế** ⇒ script chỉ đọc 3 cột (tên, địa chỉ, toạ độ), test khẳng định bảng ra không có chuỗi số ≥ 9 chữ số / ký tự `@` |
| Chữ từ ngoài là dữ liệu | tên + địa chỉ cơ sở đi vào ngữ cảnh model ⇒ **có thể chứa chữ lạ** (cơ sở tự đăng ký tự gõ tên) | rủi ro thấp–vừa: script lọc ký tự điều khiển, cắt tên > 120 ký tự, loại dòng có URL / số điện thoại / chữ kiểu mệnh lệnh; User xem lướt bảng; Q2 (a) chỉ lấy bản ghi do cơ quan quản lý nhập |
| Dữ liệu cá nhân | không lấy điện thoại / email / tên người; tên hộ kinh doanh có thể trùng tên người ("Nhà nghỉ <tên>") | chấp nhận như tên biển hiệu công khai; không ghép thêm trường nào |
| Giá / thông tin cũ nhanh | không giá; hạng sao có nhãn ngày; dòng "có thể đã đổi" (cơ chế có sẵn theo thư mục nguồn) | thêm tiền tố file lưu trú (`travel/services/Lưu trú ở Huế`) vào danh sách nguồn kích dòng nhắc (một dòng code — thuộc spec này, §3 (a)) |
| Đường ra mới | không — không công cụ, không link mới từ kho | khớp |
| Closed-world | bài mới vẫn là nguồn duy nhất; câu hỏi cơ sở không có trong bài ⇒ từ chối / web như cũ | K4 đo "0 cơ sở ngoài bài" |
| Đo hai chiều | K4–K6 (được việc) ↔ K1–K3 (không hỏng việc cũ) | khớp |
| Lùi được | §4 "Dừng + lùi" | khớp |

## 8. Quyền, tiền, giờ
- **Quyền cần User duyệt qua spec này:** thêm file vào curated corpus (≤ 5 bài lưu trú + 1–2 bài đi lại trong `travel/services/`, 1 bài `foods/` — **đều ở thư mục đã quét, không sửa `include_globs`**); sửa bài quán kho (một dòng định vị mỗi bài có toạ độ); **đưa tên + địa chỉ quán từ dữ liệu mở vào kho có nhãn** (Q3 (b)); một dòng code `NOTICE_SOURCE_PREFIXES` + test; enrich bằng web cho bài đi lại trong danh sách nguồn §3 (b); xoá + dựng lại **đúng một** collection runtime; tạo nhãn v6. Không sửa Golden (chỉ thêm bộ câu mới ở `data/`).
- **Tiền:** dựng lại 0 USD (model nhúng chạy máy). Đo: Golden trước + sau 0,15 + an toàn trước + sau 0,04 + ba bộ mới trước / sau 36 câu × 2 × ≈ 0,001 ≈ 0,07 ⇒ **≈ 0,26; trần đợt 0,35 USD** (bản 1 ghi 0,25 — thiếu lượt "trước" phải chạy lại). Chấm: agent con.
- **Giờ (ước thô):** soạn + script 2–3 giờ · User xem lướt 20–30 phút · dựng lại ~30–40 phút máy · đo + chấm + báo cáo 2 giờ. Trong lúc dựng lại, chatbot không khởi động lại được.

## 9. Rủi ro
| Rủi ro | Giảm bằng |
|---|---|
| ~300 tên cơ sở làm nhiễu tìm kiếm câu khác | K3 + K1; lùi riêng phần (a) nếu vỡ; Q2 (a) giảm số dòng |
| Danh mục có cơ sở đã đóng cửa / hạng cũ | nhãn ngày + "có thể đã đổi"; đối chiếu 21 cơ sở 4–5 sao; không khẳng định "đang hoạt động" |
| Model ghép giá từ bài chi phí vào câu lưu trú | K4 "0 giá phòng"; nếu thấy ⇒ sửa bằng luật code đã có (`gia_luu_tru`) mở rộng sang câu kho — việc riêng |
| Câu định vị sai vì toạ độ ước | Q4 (a) chỉ dùng toạ độ chắc |
| Bài đi lại lệch thực tế (tuyến xe đổi) | chỉ ý có ≥ 1 nguồn chính thức; không giá, không số điện thoại; ghi ngày |
| Trộn ba phần vào một lần dựng ⇒ khó biết phần nào gây lỗi | K3 đếm theo nguồn đoạn; lùi theo phần |

## Chỗ đổi bản 2
| Nguồn | Sửa ở |
|---|---|
| C M-1 thư mục mới không được quét | §3 (a) "Vị trí file" (đặt trong `travel/services/`), §4 bước 6 (đếm đoạn theo nguồn ≠ 0), §8 quyền |
| C M-2 dạng bài chưa chạy thử; câu danh sách / gần điểm | §3 (a) "Dạng bài" (kết quả chạy thử bộ chia đoạn; đoạn văn ≤ 6 cơ sở; bài tổng 3–5 sao), kết cục ghi trước cho câu giá rẻ / homestay, K4 tách a / b / c |
| C M-3 ăn gần chưa chắc đạt | Q4 hai mức (ước ⇒ chỉ "cùng cụm"), §3 (c) (điểm mốc thêm, dữ kiện thay nhận định, chạy thử số quán trước khi chốt K6), K6 |
| C minor: số 151 · tỉ lệ gán khu · T1 tách nhóm · dòng code dòng nhắc · bộ "trước" chạy lại, tiền | Q2 (đếm lại nhãn nguồn), §3 (a) "Gán khu" (địa chỉ không có phường ⇒ ước từ số nhà + đường; bước đếm), bước 6 + K3, §3 (a) dòng code, bước 0 + §8 (0,26; trần 0,35) |
| Mức lịch trình User chốt (đủ 4 phần) | Q1 (bài + bảng cho lịch), **Q3 đổi khuyến nghị sang thêm quán từ dữ liệu mở có nhãn**, §3 (c) bảng `quan_theo_cum.json`, §3 (d) buổi tối (phụ thuộc bảng điểm, không thêm kho) |
