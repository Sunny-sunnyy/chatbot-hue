# 02 — Kho dữ liệu: chatbot biết những gì

Cập nhật 10/11/2026 (bản mẫu sắp xếp lại; bản cũ xem trong lịch sử phiên bản — git). Tả kho **đang dùng**. Số chung (số đoạn, điểm chất lượng, từ chối nhầm)
ở bảng "Số chính" của [README](README.md); từ khó (chỉ mục, sàn, Golden…) ở "Từ hay gặp" cùng chỗ. Bước trước: [01 — luồng chạy](01_LUONG_HOAT_DONG_HE_THONG.md) ·
bước sau: [03 — chia đoạn](03_BAO_CAO_CHIA_DOAN.md).

## Kho gồm gì

**204 bài Markdown tiếng Việt** — toàn bộ những gì chatbot "biết" (ngoài ngày, thời tiết và mục web ghi riêng):

| Chủ đề | Số bài | Gồm |
|---|---:|---|
| Món ăn | 91 | đặc sản Huế, nhà hàng / quán, quán cà phê, một bài hướng dẫn chung |
| Di tích | 29 | Đại Nội, Kinh thành, các lăng, chùa, đàn tế, di sản (Nhã nhạc, Mộc bản…) |
| Lễ hội | 27 | lễ hội, ngày hội, lễ tế theo năm |
| Nghệ thuật biểu diễn | 12 | chương trình biểu diễn, ca Huế, đêm nhạc |
| Du lịch | 45 | địa điểm (biển, đầm phá, chợ, phố đi bộ, suối, đèo), lịch trình mẫu, chi phí, vé |

- Mỗi bài viết theo **mẫu riêng của chủ đề** (vd bài món ăn có mô tả, nơi ăn, giá, giờ), câu văn tự nhiên, đọc riêng một bài vẫn hiểu.
- Phần lớn bài có mục "Nguồn dữ liệu" ghi nơi lấy thông tin — trang công khai: cổng thông tin của tỉnh, báo, trang du lịch, văn bản pháp luật… (khoảng 76 trang web khác nhau).
- Kho **không** đưa lên kho mã công khai (GitHub) — nội dung giữ riêng trên máy; vì vậy sửa bài nào cũng phải sao lưu bản gốc trước.
- Ngoài 204 bài: 3 file "danh mục biên soạn" (danh sách tên dùng lúc soạn bài) bị **loại khỏi** chatbot vì không phải bài để trả lời; và một file nhỏ 3 quy tắc —
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

(Hai đợt trùng con số 123 chỗ là ngẫu nhiên — đếm riêng từng đợt.) Kho **đúng hơn, thận trọng hơn**, nhưng điểm chấm **không tăng**: chỉ khoảng 1 / 6 câu Golden chạm chỗ
sửa, và đáp án mẫu hầu như không hỏi đúng tên phường hay chi tiết đã bỏ.

## Còn thiếu gì

- **Kho có, nhưng tìm không ra** mới là lỗi chính: rà 18 câu Golden bị từ chối / thiếu ý (01/11, trước khi trợ lý được "tìm thêm") ⇒ cả 18 do đoạn đúng có trong kho nhưng không
  lọt vào 10 đoạn đưa model. Sau khi có "tìm thêm", số từ chối nhầm đã giảm — xem README; cách tìm ở [06](06_BAO_CAO_TIM_KIEM.md).
- **Kho thiếu thật** (đếm trên 15 câu "về Huế mà kho không có" của bộ đo tra web): ăn uống theo nhu cầu cụ thể, giờ / vé / giá của điểm ngoài Quần thể (chợ, phố, chùa),
  lễ hội theo ngày cụ thể, lưu trú. Hiện bù bằng mục web "chưa kiểm"; thêm vào kho cần nguồn ngoài + bạn duyệt.
- Vài chỗ còn "chờ tra ngoài" (bài đã tự ghi là chưa chắc). Giá, giờ, lịch có thể cũ dần — câu trả lời trích bài vé, địa điểm, lễ hội có kèm dòng "thông tin có thể đã thay đổi".
- **Dữ liệu mở của tỉnh** (bộ số liệu tỉnh công bố, tải về 05/08; giờ ghi năm 2024): có 180 di tích (nhiều hơn kho) — 179 có toạ độ, dùng cho bản đồ; danh sách quán ăn
  (tên, địa chỉ); giờ của một số điểm. Có file chứa thông tin cá nhân ⇒ **không** đưa vào kho / báo cáo. Giờ 2024 của bộ này lệch bài vé trong kho ⇒ đợt 05/11 không dùng.

## Khi sửa kho thì phải làm gì

1. Sao lưu bài gốc (và chỉ mục cũ nếu còn giá trị).
2. Ghi **sàn** trước khi sửa (luật "không làm hỏng": không thêm câu ngoài kho bị trả lời, không thêm lỗi an toàn…) và bộ câu sẽ đo.
3. Sửa bằng máy: mỗi câu cũ phải xuất hiện **đúng một lần** trong bài thì máy mới thay — để không sửa nhầm chỗ khác; người khác đối chiếu từng chỗ với bản sao lưu.
4. Xoá chỉ mục cũ rồi dựng lại (vài phút). Lệnh xoá do bạn tự chạy — agent không được tự xoá dữ liệu.
5. Đo lại "trước ↔ sau", ghi kết quả — kể cả kết quả xấu.
6. Đáp án mẫu Golden nào nhắc chỗ vừa sửa ⇒ sửa theo, bạn duyệt phần đổi.

**Bạn cần quyết (không gấp):** giữ hay xoá bản sao lưu của các đợt sửa · xoá collection thử ảnh trong Qdrant (xem [05](05_BAO_CAO_LUU_TRU_QDRANT.md)).

## Đã thử, không dùng

- Model vector lớn (Qwen3-8B) dựng chỉ mục trên kho đã sửa (30/10): tìm kém hơn, chậm hơn ⇒ giữ model nhỏ — [91 — so sánh phương án](91_BAO_CAO_SO_SANH_PHUONG_AN.md).

## Đọc chi tiết

- Thiết kế sửa kho + dựng lại chỉ mục: `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md`
- Đợt 1, đợt 2, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` (đợt 2: `sua_kho_dot2_implementation.md`; đợt 1: `sua_kho_b9_implementation.md`)
- Rà toàn kho 25/10: `report_agent/2026-10-25_ra_soat_noi_dung_kho/` · giờ mở cửa 05/11: `report_agent/2026-11-05_sua_kho_gio/c192_implementation.md`
- Dựng lại chỉ mục (lệnh, bẫy): `guides/full_corpus_rag.md` mục "Build lại index". Cho người sửa sau: mã đoạn đánh số theo thứ tự trong bài ⇒ xoá một dòng giữa bài làm
  số dồn lại (đợt 2 đã phải đo bù); agent chỉ tìm trong kho qua `scripts/grep_kb.sh` (không đọc lọt bộ câu đánh giá nằm cạnh kho).
