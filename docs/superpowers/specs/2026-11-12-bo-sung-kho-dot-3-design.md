# Đợt bổ sung kho 3 — lưu trú · đi lại · ăn gần — tài liệu thiết kế (NHÁP bản 1, chờ User duyệt một lần)

Người viết: E · 21:13 12/11/2026 (`date`) · A giao sau khi User chốt 20:54 12/11/2026: "chỗ nào Huế TRIPO hơn thì học; phần nào cần dữ liệu thì tìm, cào, bổ sung". Review: C.
Khuôn theo spec sửa kho cũ `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` và đợt giờ mở cửa 05/11 (`data/sua_kho_2026-11-05_gio/tools/chay.sh`).
**Mức rủi ro: cao** (thêm nội dung vào kho curated + dựng lại chỉ mục + **nguồn dữ liệu mới từ ngoài**) ⇒ User duyệt spec này một lần; từng bảng dữ liệu vào kho User xem lướt trước khi ghi.

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
- **Q1 — Lưu trú vào kho dạng gì.** (a) **Bài Markdown theo khu** (khuyến nghị): mỗi khu một bài, trong bài chia theo loại hình + hạng; tầng tìm hiện tại dùng được ngay, có trích dẫn như mọi bài. *Khi nào sai:* ~300 tên riêng làm nhiễu tầng tìm của câu khác — tiêu chí §6 đo; *mất gì nếu chọn khác:* (b) bảng do code đọc + công cụ lọc ⇒ chính xác hơn nhưng là công cụ mới (plan + đo riêng, không còn là "bổ sung kho").
- **Q2 — Lấy cơ sở nào.** (a) **Chỉ bản ghi "cơ quan nhà nước quản lý nhập" + có hạng hoặc loại rõ** (khuyến nghị — ít mà chắc); (b) mọi bản ghi kể cả "cơ sở tự đăng ký" (nhiều hơn, chất lượng không đều). **Số thật đã tải (21:12–21:15 12/11/2026, 73 trang, `data/luu_tru_2026-11-12/bien_ban.json`): 316 cơ sở** — loại hình: khách sạn 306 · biệt thự du lịch 6 · nhà nghỉ 2 · khác 2 (**0 homestay / nhà ở có phòng cho thuê** ⇒ danh mục này gần như chỉ có khách sạn); hạng: 5 sao 11 · 4 sao 13 · 3 sao 8 · 2 sao 31 · 1 sao 49 · "đạt chuẩn phục vụ khách du lịch" 39 · "khác" 138 · không ghi 27; nguồn nhập đọc được: cơ quan nhà nước 191 · tự đăng ký 9 · chưa đọc được nhãn 116. ⇒ (a) cho khoảng **151 cơ sở có hạng sao hoặc "đạt chuẩn"**; (b) cho 316.
- **Q3 — Quán gần Đại Nội / chùa Thiên Mụ.** Kho chỉ có 1 quán có toạ độ quanh Đại Nội, 0 quanh Thiên Mụ và các lăng; dữ liệu mở có 276 cơ sở / 1 km quanh Đại Nội, 174 quanh Thiên Mụ, **0 quanh các lăng**. (a) **Không thêm quán mới từ dữ liệu mở ở đợt này** (khuyến nghị): dữ liệu mở chỉ có tên + địa chỉ + toạ độ, giờ / giá 2 / 6.794 bản ghi, không biết quán còn mở hay ngon — thêm vào là hạ chuẩn "kho đã kiểm"; thay bằng bài tổng hợp ở (c) nói thật "quanh lăng không có quán trong dữ liệu, nên ăn ở khu …". (b) thêm ≤ 10 quán / điểm cho 2 điểm, ghi nhãn "theo dữ liệu mở của thành phố, chưa kiểm" — cần luật chọn (đề xuất: chỉ cơ sở trùng tên với bài kho hoặc có ≥ 2 nguồn công khai nhắc tới) và User xem từng dòng.
- **Q4 — Toạ độ ước.** 22 / 29 toạ độ quán là **ước từ số nhà kề** (sai số trung vị 107 m, 95 % ≤ 522 m). (a) **Chỉ ghi câu định vị cho toạ độ "chắc" / "vừa" (7 bài)** (khuyến nghị); bài toạ độ ước chỉ ghi **tên đường + khu** (đã có trong địa chỉ), không ghi khoảng cách. (b) ghi cả 29 bài, làm tròn tới 0,5 km và dùng chữ "khoảng" — sai số 522 m vẫn có thể đổi "0,5 km" thành "1 km".
- **Q5 — Mức giá lưu trú.** (a) **Không ghi mức giá** (khuyến nghị — nguồn không có; quyết định 05/11 "không nói giá phòng"); (b) ghi "mức ước theo hạng" bằng luật cố định (1–2 sao / nhà nghỉ = bình dân · 3 sao = tầm trung · 4–5 sao = cao cấp) kèm nhãn "ước theo hạng, không phải giá".

## 3. Nội dung từng phần

### (a) Lưu trú
- **Nguồn:** Cơ sở dữ liệu du lịch quốc gia (Cục Du lịch Quốc gia Việt Nam), bộ lọc "Thành phố Huế"; tải 12/11/2026 bằng script gửi thưa; **chỉ** tên · loại hình · xếp hạng · địa chỉ · nguồn nhập. Đối chiếu hạng 4–5 sao với danh sách 21 cơ sở của ngành du lịch thành phố (nhập tay, ghi nguồn).
- **Dạng bài** (`travel/lodging/`, thư mục mới): một bài mỗi khu — khu lấy từ **phường / xã trong địa chỉ**, gom thành 3 nhóm khu mà kho đã dùng ở mục "nên ở khu nào" (lõi đô thị hai bờ sông Hương · phía tây yên tĩnh · ven biển / đầm phá) + nhóm "khác". Trong bài: mục theo loại hình (khách sạn · nhà nghỉ · nhà ở có phòng cho thuê · căn hộ / biệt thự), mỗi cơ sở **một dòng**: tên — hạng (nếu có) — địa chỉ. Đầu bài: một đoạn "khu này hợp với ai" **chép ý từ bài cẩm nang có sẵn**, không viết thêm nhận xét về từng cơ sở.
- **Bắt buộc trong bài:** dòng "Danh sách theo danh mục của Cục Du lịch Quốc gia Việt Nam, lấy ngày 12/11/2026; hạng sao theo danh mục, có thể đã đổi; **không gồm giá phòng** — xem giá và đặt phòng ở trang đặt phòng." Mục `## Nguồn dữ liệu` tối giản.
- **Cấm:** giá, điện thoại, email, tên chủ cơ sở, nhận xét chất lượng, link đặt phòng.
- **Giới hạn đã thấy của nguồn:** không có homestay / nhà dân (0 bản ghi) ⇒ câu hỏi homestay vẫn dựa vào các mục có sẵn trong bài điểm tham quan + thẻ "khu nên ở + link bản đồ"; ghi rõ trong bài "danh mục chủ yếu là khách sạn đã đăng ký với ngành du lịch".
- **Luật chia đoạn:** mỗi dòng cơ sở là một mục danh sách ⇒ chunker hiện tại cắt mỗi dòng một đoạn mang tên bài + tên mục (khu, loại) — không đổi chunker. Kiểm trước: số đoạn tăng bao nhiêu (ước +150–320 trên 8.435, theo Q2).

### (b) Đi lại / thuê xe
- **1 bài chắc chắn + 1 bài tuỳ dữ liệu** (`travel/services/`): **"Đi lại ở Huế"** — từ sân bay / ga / bến xe vào trung tâm (các hình thức: xe buýt sân bay, taxi, xe công nghệ, xe đưa đón), đi tới nhóm lăng phía tây nam (taxi / thuê xe máy / thuyền / xe tham quan), đi trong nội thành (xích lô, xe đạp, đi bộ), lưu ý an toàn (đường đèo, mùa mưa, giấy tờ khi thuê xe máy). **"Thuê xe ở Huế"** chỉ viết nếu tìm được ≥ 2 nguồn công khai đáng tin cho từng ý.
- **Nguồn đề xuất (User duyệt phạm vi enrich bằng web):** cổng / trang chính quyền thành phố và Sở Du lịch, trang Cảng hàng không Phú Bài, trang ga Huế / Đường sắt Việt Nam, trang Trung tâm Bảo tồn Di tích (xe điện, thuyền), quy định pháp luật về giấy phép lái xe; bổ sung từ **đoạn có sẵn trong kho** (kho đã nhắc "thuê xe" ở 9 bài, "taxi" ở 23 bài — gom lại, ghi nguồn bài). Không lấy từ mạng xã hội / trang đại lý.
- **Không giá cứng:** không ghi số tiền thuê xe / cước; chỉ "giá thay đổi theo mùa và nhà cung cấp — hỏi trước khi thuê". Số điện thoại tổng đài hãng: không ghi (cũ nhanh).
- Mỗi ý trong bài ghi nguồn + ngày xem ở `## Nguồn dữ liệu`; web mâu thuẫn kho ⇒ ghi cả hai, báo A.

### (c) Ăn gần một điểm
- **Câu định vị cho bài quán** (`foods/restaurants/`, `foods/cafes/`): thêm **một dòng** "Vị trí: cách <điểm tham quan> khoảng <x> theo đường chim bay." theo bảng đề xuất của C — phạm vi theo Q4 (khuyến nghị: 7 bài toạ độ chắc / vừa; làm tròn 50 m dưới 300 m, 0,1 km từ 300 m). Bài đã có câu định vị: không thêm.
- **Một bài tổng hợp mới** `foods/an-gan-diem-tham-quan.md`: mỗi điểm tham quan chính một mục — "quanh <điểm> kho có các quán: … (tên bài kho)" lập **từ chính bảng khoảng cách**; với **khu lăng và chùa Thiên Mụ** ghi đúng sự thật dữ liệu: "trong dữ liệu chưa có quán sát khu này; khách thường ăn ở <khu gần nhất có quán trong kho> trước hoặc sau khi tham quan" — câu này nằm **trong kho** (có trích dẫn), không phải câu cố định trong code.
- Không sửa nội dung khác của bài quán.

## 4. Các bước (người làm ↔ người kiểm khác nhau; bước 3–7 làm liền một lần)
0. **Bộ "trước":** Golden 176 + an toàn 32 đã có từ B7 giữa kỳ (cùng code `dfd0c96`) — dùng lại nếu `backend/` không đổi tới lúc làm; đổi ⇒ chạy lại (≈ 0,08 USD). Ba bộ câu mới (§6) chạy "trước" 1 lượt (≈ 0,03).
1. **Soạn** (E): bài lưu trú sinh **bằng script** từ bảng sạch (không gõ tay tên cơ sở); bài đi lại soạn tay từ nguồn đã duyệt; câu định vị áp bằng script từ bảng của C. Mỗi file mới / sửa có diff.
2. **User xem lướt** bảng lưu trú (theo khu) + bài đi lại + danh sách câu định vị ⇒ duyệt / sửa. **C review** diff: luật curated, không giá / liên hệ, mỗi ý bài đi lại có nguồn.
3. **Sao lưu:** file quán bị sửa ⇒ `knowledge-base-hue/meta/backup_dot_3_2026-11-12/`; snapshot Qdrant; chép build record + sparse state ra `data/sua_kho_2026-11-12_dot_3/backup/`.
4. **Ghi kho** + **chia đoạn thử, chỉ đọc**: 0 lỗi, mỗi đoạn vừa 3 tokenizer; test mẫu chunker (không file mẫu nào bị chạm — xác nhận).
5. **Dựng lại tại chỗ:** xoá đủ ba đích (collection, build record, sparse state) rồi build (CPU, ~vài chục phút); script có bước 0 kiểm khoá + tự lùi như `chay.sh` 05/11.
6. **Kiểm sau build:** `/health` 5 / 5; cổng ổn định; **T1 mới** (158 câu) ⇒ so từng câu với T1 cũ `64656a87c109`.
7. **Nhãn đoạn đúng v6:** chỉ thêm dòng / thêm file ⇒ trích dẫn cũ tìm lại nguyên văn; `chunk_id` dồn ở file quán bị thêm dòng ⇒ dựng v6 bằng công cụ có sẵn, 0 trích dẫn mất.
8. **Đo "sau"** (§6) ⇒ chấm cùng lượt mù với "trước".
9. **Báo cáo + bài học:** sổ ghi việc (khâu kho, chia đoạn, tìm), `bai_hoc/` bài 1 + bảng tổng bài 19, `Project_Status.md` §4 (số file, số đoạn, sha).
**Dừng + lùi:** chia đoạn lỗi / build lỗi / `/health` không đạt / sàn §6 vỡ ⇒ xoá file mới, chép lại file quán từ bản sao, khôi phục snapshot + build record + sparse state, khởi động lại, cổng ổn định. Lùi là **toàn bộ đợt** hoặc **bỏ riêng phần gây vỡ sàn rồi dựng lại** (A quyết theo số đo).

## 5. Thứ tự với việc khác
- Plan **"khu nên ở + link bản đồ"** (đã duyệt, chưa code) làm **trước hoặc song song** — không phụ thuộc đợt này; sau đợt này danh sách "mục kho về lưu trú" của plan đó thêm các bài `travel/lodging/` (một dòng cấu hình).
- Làm sau khi nhánh "hết lượt tìm" merge (đổi hành vi tìm thêm ⇒ bộ "trước" phải đo trên code đã merge).
- **Trước lượt B7 cuối** (lượt cuối đo trên kho đã bổ sung).

## 6. Tiêu chí nghiệm thu (ghi trước)
| # | Tiêu chí | Bộ | Mức |
|---|---|---|---|
| K1 | Không làm hỏng câu cũ | Golden 176 trước ↔ sau, chấm cùng lượt mù | Đủ / Đúng TB theo cặp ≥ −0,1; câu tụt ≤ 4; từ chối nhầm ≤ trước + 1; 0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật / trích dẫn mới |
| K2 | An toàn | 32 câu ×1 (ca mới ⇒ thủ tục sinh lại 3 lần, hai người chấm cùng gắn) | 4 số như mọi bậc |
| K3 | Tầng tìm câu cũ không bị tên cơ sở chen | T1 158 câu: số câu có **đoạn lưu trú mới** lọt vào 10 đoạn đầu | ≤ 5 câu, và 0 câu mất đoạn đúng (nhãn v6) vì bị chen |
| K4 | Lưu trú | 12 câu của plan lưu trú (4 cơ sở cụ thể + 2 khu + 6 mới) | câu cơ sở cụ thể được kho trả lời có trích dẫn: ≥ 3 / 4 (trước: 1 / 4 một phần); **0 câu nêu giá phòng**; 0 câu nêu cơ sở không có trong bài |
| K5 | Đi lại | 6 câu của lượt đếm 12/11 + 6 câu mới (người viết ≠ E) | kho trả lời đủ dùng ≥ 8 / 12 (trước: 2 / 6); 0 số tiền cước / giá thuê trong câu trả lời |
| K6 | Ăn gần | 6 câu của lượt đếm + 6 câu mới (2 câu hỏi quanh lăng / chùa) | đủ dùng ≥ 7 / 12 (trước: 1 / 6); câu quanh lăng / chùa: trả lời đúng "không có quán sát đó, ăn ở khu …" có trích dẫn, **không bịa tên quán** (0 tên ngoài kho) |
| K7 | Kho sạch | mọi file mới / sửa | 0 giá phòng, 0 điện thoại / email, 0 YAML frontmatter, có `## Nguồn dữ liệu` + ngày lấy; hook pre-commit không liên quan (kho không commit) |
| K8 | Tốc độ / tiền (theo dõi) | log | USD / câu và thời gian tìm không tăng quá nhiễu (kho +3–4 % đoạn) |
"Đủ dùng" chấm bằng 2 người chấm mù, tính khi cả hai cùng gắn. Không bộ kín (đợt dữ liệu, không chỉnh lời dặn).

## 7. Rà khung AI FDE — phần nguồn dữ liệu mới (`agent-security-review`)
| Mục | Hiện trạng / thiết kế | Khớp · rủi ro |
|---|---|---|
| Nguồn ngoài đi vào kho | danh mục cơ quan nhà nước (HTML công khai, không điều khoản cấm, không `robots.txt`); dữ liệu mở thành phố (đã tải 08/2026); trang chính quyền cho bài đi lại | khớp — mỗi nguồn ghi tên + ngày trong bài |
| Chữ từ ngoài là dữ liệu | tên + địa chỉ cơ sở đi vào ngữ cảnh model ⇒ **có thể chứa chữ lạ** (cơ sở tự đăng ký tự gõ tên) | rủi ro thấp–vừa: script lọc ký tự điều khiển, cắt tên > 120 ký tự, loại dòng có URL / số điện thoại / chữ kiểu mệnh lệnh; User xem lướt bảng; Q2 (a) chỉ lấy bản ghi do cơ quan quản lý nhập |
| Dữ liệu cá nhân | không lấy điện thoại / email / tên người; tên hộ kinh doanh có thể trùng tên người ("Nhà nghỉ <tên>") | chấp nhận như tên biển hiệu công khai; không ghép thêm trường nào |
| Giá / thông tin cũ nhanh | không giá; hạng sao có nhãn ngày; dòng "có thể đã đổi" (cơ chế có sẵn theo thư mục nguồn) | thêm `travel/lodging/` vào danh sách thư mục kích dòng nhắc (một dòng code — nằm trong plan lưu trú) |
| Đường ra mới | không — không công cụ, không link mới từ kho | khớp |
| Closed-world | bài mới vẫn là nguồn duy nhất; câu hỏi cơ sở không có trong bài ⇒ từ chối / web như cũ | K4 đo "0 cơ sở ngoài bài" |
| Đo hai chiều | K4–K6 (được việc) ↔ K1–K3 (không hỏng việc cũ) | khớp |
| Lùi được | §4 "Dừng + lùi" | khớp |

## 8. Quyền, tiền, giờ
- **Quyền cần User duyệt qua spec này:** thêm file vào curated corpus (thư mục mới `travel/lodging/`, 1–2 bài `travel/services/`, 1 bài `foods/`); sửa ≤ 29 bài quán (một dòng mỗi bài); enrich bằng web cho bài đi lại trong danh sách nguồn §3 (b); xoá + dựng lại **đúng một** collection runtime; tạo nhãn v6. Không sửa Golden (chỉ thêm bộ câu mới ở `data/`).
- **Tiền:** dựng lại 0 USD (model nhúng chạy máy). Đo: Golden "sau" 0,07 + an toàn 0,02 + ba bộ mới trước / sau 36 câu × 2 × ≈ 0,001 ≈ 0,07 ⇒ **≈ 0,16; trần đợt 0,25 USD**. Chấm: agent con.
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
