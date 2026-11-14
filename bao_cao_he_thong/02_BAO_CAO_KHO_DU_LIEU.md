# 02 — Kho dữ liệu: chatbot biết những gì

Cập nhật 20:32 14/11/2026: sáu lần ghi kho ngày 14/11 (lần 6: 13 lễ hội / phong tục + 3 nghệ thuật ⇒ **263 bài / 9.425 đoạn**; bài nháp quét trùng bộ câu chấm trước khi ghi). Trước — 19:41 14/11/2026: năm lần ghi kho ngày 14/11 (lần 5: 10 món + 13 địa điểm / di tích trợ lý từng từ chối / trả lời mỏng ⇒ **247 bài / 9.032 đoạn**). Trước — 18:06 14/11/2026: bốn lần ghi kho ngày 14/11 (lần 4: 8 quán ăn ở Thủy Xuân / Kim Long / Đầm Chuồn ⇒ **224 bài / 8.644 đoạn**; trước: 16:18 — lần 3: 4 bài nơi chưa có bài + giờ Đại Nội theo mùa ⇒ 216 bài / 8.603 đoạn). Bản cũ xem trong lịch sử phiên bản — git. Tả kho **đang dùng**. Số chung (số đoạn, điểm chất lượng, từ chối nhầm)
ở bảng "Số chính" của [README](README.md); từ khó (chỉ mục, sàn, Golden…) ở "Từ hay gặp" cùng chỗ. Bước trước: [01 — luồng chạy](01_LUONG_HOAT_DONG_HE_THONG.md) ·
bước sau: [03 — chia đoạn](03_BAO_CAO_CHIA_DOAN.md).

## Kho gồm gì

**263 bài Markdown tiếng Việt** (lần ghi kho 6, 20:21 14/11/2026: +13 lễ hội / phong tục + 3 nghệ thuật (hò Huế, lý Huế, ca kịch Huế); record `af5e225c497e`; report `report_agent/2026-11-12_ra_khoang_cach/b_ghi_kho_6_implementation.md`; lần ghi kho 5, 19:34 14/11/2026: +10 món / đặc sản (tré, vả trộn, tôm chua, mít trộn, bánh in, rượu Minh Mạng, cháo hến, cơm sen, nem công chả phượng, bánh su sê) + 8 di tích + 5 địa điểm; record `106fe0842b8e`; report `report_agent/2026-11-12_ra_khoang_cach/b_ghi_kho_5_implementation.md`; lần ghi kho 4, 17:51 14/11/2026: +8 bài quán — Thủy Xuân 3, Kim Long 2, Đầm Chuồn 3 nhà chòi; không giá; record `944858b9972a`; report `report_agent/2026-11-12_ra_khoang_cach/b_ghi_kho_4_implementation.md`; lần ghi kho 3, 16:05 14/11/2026: +4 bài cầu Trường Tiền, Ga Huế, chùa Từ Hiếu, nhà vườn An Hiên + giờ Đại Nội theo mùa; lần 2 sáng cùng ngày: +5 bài lưu trú; report `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_3_implementation.md`, `e_ghi_kho_luu_tru_implementation.md`) — toàn bộ những gì chatbot "biết" (ngoài ngày, thời tiết và mục web ghi riêng):

| Chủ đề | Số bài | Gồm |
|---|---:|---|
| Món ăn | 109 | đặc sản Huế (14/11 tối thêm 10 món trợ lý từng từ chối / trả lời mỏng), nhà hàng / quán (từ 14/11 tối thêm 8 quán cho vùng lịch thiếu quán), quán cà phê, một bài hướng dẫn chung |
| Di tích | 39 | Đại Nội, Kinh thành (14/11 tối thêm 8 bài: chùa, phủ, nhà thờ, di tích), các lăng, chùa (có chùa Từ Hiếu từ 14/11), đàn tế, di sản (Nhã nhạc, Mộc bản…) |
| Lễ hội | 40 | lễ hội, ngày hội, phong tục Huế (14/11 tối thêm 13: Tết, cúng Âm hồn, Trung thu, Vu Lan, Đoan Ngọ…), lễ tế theo năm |
| Nghệ thuật biểu diễn | 15 | chương trình biểu diễn, ca Huế, hò Huế, lý Huế, ca kịch Huế (14/11 tối), đêm nhạc |
| Du lịch | 60 | địa điểm (14/11 tối thêm 5: cồn, làng, cầu; biển, đầm phá, chợ, phố đi bộ, suối, đèo, không gian nghệ thuật; từ 14/11 cầu Trường Tiền, Ga Huế, nhà vườn An Hiên), lịch trình mẫu, chi phí, vé, đi lại, 5 bài lưu trú (140 cơ sở 3–5 sao và khác theo khu) |

- Mỗi bài viết theo **mẫu riêng của chủ đề** (vd bài món ăn có mô tả, nơi ăn, giá, giờ), câu văn tự nhiên, đọc riêng một bài vẫn hiểu.
- Phần lớn bài có mục "Nguồn dữ liệu" ghi nơi lấy thông tin — trang công khai: cổng thông tin của tỉnh, báo, trang du lịch, văn bản pháp luật… (khoảng 76 trang web khác nhau).
- Kho **không** đưa lên kho mã công khai (GitHub) — nội dung giữ riêng trên máy; vì vậy sửa bài nào cũng phải sao lưu bản gốc trước.
- Ngoài 263 bài: 3 file "danh mục biên soạn" (danh sách tên dùng lúc soạn bài) bị **loại khỏi** chatbot vì không phải bài để trả lời; và một file nhỏ 3 quy tắc —
  vd câu lưu ý chung đầu một bài vé được gắn kèm vào mọi đoạn giá của bài đó, để đoạn nào được tìm ra cũng mang theo lưu ý.

## Chatbot chỉ chạy khi chỉ mục khớp kho

Mỗi lần dựng chỉ mục, máy ghi một "phiếu" chứa **vân tay** của từng bài (đổi một chữ là vân tay đổi). Lúc khởi động, chatbot so vân tay với kho hiện tại — sửa bài
mà chưa dựng lại chỉ mục ⇒ **từ chối chạy**, để không trả lời bằng nội dung cũ.

## Đã sửa những đợt nào, vì sao

Trước khi sửa, ngày 25/10 tám agent đọc mọi dòng có con số / mốc thời gian trong kho và lập danh sách **139 điểm đáng ngờ** (mâu thuẫn giữa hai bài, thông tin có thể cũ).
Mỗi điểm có thể phải sửa ở nhiều chỗ (vd một tên phường xuất hiện ở nhiều bài) ⇒ số "chỗ sửa" lớn hơn số điểm.

| Đợt | Sửa gì | Vì sao | Kết quả (đo lại trên Golden, chấm mù) |
|---|---|---|---|
| Đợt 1 (28/10) | 51 điểm ⇒ 123 chỗ / 65 bài — chủ yếu tên phường mới sau sắp xếp hành chính 01/07/2025 (giữ tên cũ trong ngoặc), vài con số mâu thuẫn giữa hai bài | chỉ sửa khi **ngay trong kho có căn cứ** | không làm hỏng; điểm Đủ ý −0,008, Đúng không đổi |
| Đợt 2 (30/10) | 20 điểm ⇒ 123 chỗ / 40 bài — bỏ cấp "quận"; sửa theo nguồn ngoài **bạn cho phép tra** (đọc nguyên văn, một agent khác đọc lại khớp); **làm yếu** câu không chắc (bỏ con số / chi tiết); không thêm khẳng định mới, không xoá câu cảnh báo | luật bạn đặt 29/10 cho điểm không đủ căn cứ trong kho | không làm hỏng; Đủ ý +0,008, Đúng không đổi; bộ an toàn không có lỗi mới |
| Giờ mở cửa (05/11) | thêm một dòng giờ chung + "có thể thay đổi theo mùa" vào 11 bài điểm tham quan của Quần thể Cố đô | câu "mấy giờ mở cửa" hay bị hỏi mà kho thiếu; giờ lấy từ bài vé **đã có trong kho** | trả đúng giờ có nguồn; 1 câu Golden lần đầu từ chối, chạy lại 2 lần đều đúng ⇒ bạn chọn giữ, theo dõi |
| Ghi kho (14/11) | thêm **3 bài**: bảo tàng cổ vật cung đình, không gian lưu niệm họa sĩ Lê Bá Đảng, "Đi lại ở Huế" (sân bay, ga, bến xe, đi trong nội thành, đi lăng, bằng lái xe máy, tàu Huế – Đà Nẵng, mùa mưa); **sửa 4 chỗ** theo nguồn ở 3 bài cũ (người lập không gian lưu niệm; số nhà khu trưng bày trên đường Lê Lợi — sửa ở cả hai bài nhắc tới, để kho không tự mâu thuẫn; bảo tàng nằm bờ Bắc, không thuộc "Nam sông Hương") | 2 điểm trong lịch trình có bài quá mỏng; câu hỏi đi lại hay gặp mà kho thiếu | không làm hỏng ⇒ bạn chọn giữ: Đủ ý +0,03, Đúng +0,04; từ chối nhầm 3 ⇒ 5, nhưng hai câu thêm có lần tìm giống hệt trước và chạy lại gần như luôn trả lời (do model viết khác mỗi lần); bộ an toàn không tệ đi; 6 câu đi lại đếm 12/11 dùng được 2 ⇒ 4 |

| Ghi kho lần 2 (14/11 sáng) | **5 bài lưu trú** theo khu (danh mục Cục Du lịch Quốc gia 139 cơ sở + 1 theo tin thành phố); câu trả lời trích bài lưu trú kèm dòng "có thể đã thay đổi" | câu hỏi chỗ ở trước chỉ có mục web | lưu trú 11 / 12 câu đạt, 0 câu nêu giá; ngoài kho bị trả lời 0 |
| Ghi kho lần 3 (14/11 chiều) | **4 bài** nơi hay được nhắc mà chưa có bài riêng (cầu Trường Tiền, Ga Huế, chùa Từ Hiếu, nhà vườn An Hiên) + dòng giờ Đại Nội theo mùa (hè / đông, giờ ngừng bán vé; tham quan đêm chỉ theo chương trình riêng). Nguồn mâu thuẫn ⇒ ghi "nguồn ghi A hoặc B"; review C 1 major + 3 minor đã sửa trước khi dựng | đếm trước: nơi được nhắc ở nhiều bài mà không có bài riêng | đo câu chạm (2 câu Golden + 18 ngoài kho + an toàn 32 + 7 câu thử): ngoài kho bị trả lời 0 / 18, an toàn 0 đổi lớp, 4 nơi mới hết từ chối; ≈ 0,030 USD |

(Hai đợt trùng con số 123 chỗ là ngẫu nhiên — đếm riêng từng đợt.) Kho **đúng hơn, thận trọng hơn**, nhưng điểm chấm **không tăng**: chỉ khoảng 1 / 6 câu Golden chạm chỗ
sửa, và đáp án mẫu hầu như không hỏi đúng tên phường hay chi tiết đã bỏ.

## Còn thiếu gì

- **Kho có, nhưng tìm không ra** mới là lỗi chính: rà 18 câu Golden bị từ chối / thiếu ý (01/11, trước khi trợ lý được "tìm thêm") ⇒ cả 18 do đoạn đúng có trong kho nhưng không
  lọt vào 10 đoạn đưa model. Sau khi có "tìm thêm", số từ chối nhầm đã giảm — xem README; cách tìm ở [06](06_BAO_CAO_TIM_KIEM.md).
- **Kho thiếu thật** (đếm trên 15 câu "về Huế mà kho không có" của bộ đo tra web): ăn uống theo nhu cầu cụ thể, giờ / vé / giá của điểm ngoài Quần thể (chợ, phố, chùa),
  lễ hội theo ngày cụ thể (lưu trú đã có 5 bài từ 14/11). Hiện bù bằng mục web "chưa kiểm"; thêm vào kho cần nguồn ngoài + bạn duyệt.
- **Giờ Đại Nội theo mùa** lấy từ trang du lịch (Vinpearl, 10/06/2025), chưa thấy văn bản của Trung tâm Bảo tồn; 11 bài lăng / điện khác vẫn ghi khung giờ chung.
- Vài chỗ còn "chờ tra ngoài" (bài đã tự ghi là chưa chắc). Giá, giờ, lịch có thể cũ dần — câu trả lời trích bài vé, địa điểm, lễ hội có kèm dòng "thông tin có thể đã thay đổi".
- **Dữ liệu mở của tỉnh** (bộ số liệu tỉnh công bố, tải về 05/08; giờ ghi năm 2024): có 180 di tích (nhiều hơn kho) — 179 có toạ độ, dùng cho bản đồ; danh sách quán ăn
  (tên, địa chỉ); giờ của một số điểm. Có file chứa thông tin cá nhân ⇒ **không** đưa vào kho / báo cáo. Giờ 2024 của bộ này lệch bài vé trong kho ⇒ đợt 05/11 không dùng.

## Khi sửa kho thì phải làm gì

1. Sao lưu bài gốc (và chỉ mục cũ nếu còn giá trị).
2. Ghi **sàn** trước khi sửa (luật "không làm hỏng": không thêm câu ngoài kho bị trả lời, không thêm lỗi an toàn…) và bộ câu sẽ đo.
3. Sửa bằng máy: mỗi câu cũ phải xuất hiện **đúng một lần** trong bài thì máy mới thay — để không sửa nhầm chỗ khác; người khác đối chiếu từng chỗ với bản sao lưu.
4. Xoá chỉ mục cũ rồi dựng lại (vài phút). Dựng lại chỉ mục nằm trong gói bạn đã duyệt ⇒ kịch bản của agent tự xoá chỉ mục cũ và dựng lại (lần 14/11 làm vậy); xoá file / collection **ngoài** gói đã duyệt ⇒ bạn tự chạy lệnh.
5. Đo lại "trước ↔ sau", ghi kết quả — kể cả kết quả xấu.
6. Đáp án mẫu Golden nào nhắc chỗ vừa sửa ⇒ sửa theo, bạn duyệt phần đổi.

**Bạn cần quyết (không gấp):** giữ hay xoá bản sao lưu của các đợt sửa.

## Đã thử, không dùng

- Model vector lớn (Qwen3-8B) dựng chỉ mục trên kho đã sửa (30/10): tìm kém hơn, chậm hơn ⇒ giữ model nhỏ — [91 — so sánh phương án](91_BAO_CAO_SO_SANH_PHUONG_AN.md).

## Đọc chi tiết

- Thiết kế sửa kho + dựng lại chỉ mục: `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md`
- Đợt 1, đợt 2, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` (đợt 2: `sua_kho_dot2_implementation.md`; đợt 1: `sua_kho_b9_implementation.md`)
- Rà toàn kho 25/10: `report_agent/2026-10-25_ra_soat_noi_dung_kho/` · giờ mở cửa 05/11: `report_agent/2026-11-05_sua_kho_gio/c192_implementation.md`
- Ghi kho 14/11: `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md` (review: `c_review_ghi_kho_14_11.md`, `c_review_e_ghi_kho_report.md` cùng thư mục)
- Dựng lại chỉ mục (lệnh, bẫy): `guides/full_corpus_rag.md` mục "Build lại index". Cho người sửa sau: mã đoạn đánh số theo thứ tự trong bài ⇒ xoá một dòng giữa bài làm
  số dồn lại (đợt 2 đã phải đo bù); agent chỉ tìm trong kho qua `scripts/grep_kb.sh` (không đọc lọt bộ câu đánh giá nằm cạnh kho).
