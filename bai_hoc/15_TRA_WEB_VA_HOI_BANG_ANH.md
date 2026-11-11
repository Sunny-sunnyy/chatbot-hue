# Bài 15 — Khi sổ không có: tra web, và hỏi bằng ảnh

*Cập nhật lần cuối: 14:48, ngày 11/11/2026 · sửa một câu nói về việc chưa làm (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Tra web — **mới** | **`tra_web`** (dịch vụ **Serper**, tìm Google) | Khi kho không có, code tìm web **một lần** rồi model viết một mục riêng. |
| Cổng web — **mới** | **`web_gate_open`** | Điều kiện để được tra web: câu về Huế, kho đã trả câu từ chối, không lỗi gì khác. |
| Mục web | **"Từ web (chưa kiểm)"** | Phần trả lời từ web, tách riêng khỏi phần trả lời từ kho. |
| Sổ link — **mới** | mã **`[w n]`** | Mỗi kết quả web có một số; model chỉ được trích các số có trong sổ. |
| Hỏi bằng ảnh — **mới** | **`nhan_anh`** (cờ `anh.bat: true`) | Người dùng gửi ảnh; model gợi tối đa 3 tên trong một danh sách 42 mục; người dùng bấm xác nhận rồi mới trả lời. |
| Rào chắn | **guardrail** | Chỗ code chặn trước khi chữ tới người dùng. |

---

*Bài 14 kể những việc dễ nhầm do code làm. Bài này kể hai đường mở rộng ra ngoài cuốn sổ: **tra web** khi kho không có, và **hỏi bằng ảnh** khi người dùng không
biết tên thứ mình đang nhìn. Cả hai đều chạm vào luật chính "chỉ nói điều kho có", nên phải có rào chắn rõ.*

## Quay lại người hướng dẫn viên

Khách hỏi một chuyện cuốn sổ không có: *"Khách sạn nào gần cầu Trường Tiền?"*. Người hướng dẫn viên cẩn thận trả lời theo hai bước:
1. **nói thật**: "sổ của mình không có thông tin này";
2. rồi **mở điện thoại tra giúp**, nhưng nói rõ: "đây là mình vừa tra trên mạng, **chưa kiểm**, anh xem kỹ lại nhé". Họ không đọc lại link lạ, không đọc giá
   tiền không thấy trên trang, và với chuyện bão lũ thì chỉ khách tới nguồn chính thức.

Khách đưa điện thoại có một tấm ảnh: *"Đây là chỗ nào vậy?"*. Họ nhìn ảnh, đoán **vài tên có thể**, rồi hỏi lại: "có phải là chỗ này không?". Khách gật đầu, họ
mới mở sổ ra kể. Họ không kể ngay theo đoán của mình.

## Tra web: chỉ khi kho không có, và tách riêng

**Khi nào được tra.** Cổng web chỉ mở khi đủ mọi điều kiện:
- câu được xếp loại **về Huế**;
- phần trả lời từ kho đã ra **đúng câu từ chối cố định** (bài 8);
- không có lỗi ghi nguồn, lỗi công cụ, không có lịch trình, và chưa tra lần nào;
- cờ `tra_web` đang bật.

Kho trả lời được thì **không tra**. Câu ngoài chủ đề thì **không tra**. Phần chạy song song lúc xếp loại (bài 12) cũng không được tra.

**Code làm gì:**
- **Dựng câu tìm**: từ câu hỏi, bỏ số điện thoại và email nếu có, cắt còn tối đa 120 ký tự, thêm chữ "Huế". Chỉ câu tìm này được gửi ra Serper.
- Gọi Serper **một lần**, hạn **5 giây**, không thử lại, lấy tối đa **5 kết quả**. Mỗi kết quả vào **sổ link** với một số `[w 1]`, `[w 2]`…
- Model viết một mục riêng **"Từ web (chưa kiểm)"** từ các đoạn trích đó, trích bằng `[w n]`.
- **Code kiểm trước khi hiện:**
  - mọi `[w n]` phải có trong sổ;
  - **chặn** link do model tự viết, mã trang web thô, dạng `href=`;
  - **số tiền** model viết phải có nguyên văn trong đoạn trích;
  - câu về **chỗ ở** thì không được nêu số tiền nào;
  - câu cần thông tin **"ngay lúc này"** (giá hôm nay, đang mở cửa không…) mà có con số thì thay bằng câu "chưa xác minh";
  - câu về **thiên tai** thì thay hẳn bằng câu cố định trỏ tới nguồn chính thức và 112. Model không được viết.
- Giao diện hiện mục web **tách khỏi** phần trả lời từ kho, dưới nhãn "Từ web (chưa kiểm)". Link trong mục web lấy từ sổ link, trang web **không bao giờ tạo
  link từ chữ của model**.

**Kết quả:**
- Bộ câu kín (05/11): **0 / 7** câu khẳng định thông tin chưa kiểm như thật; **7 / 7** câu có mục web hữu ích.
- Tốc độ: mục web tới sau khoảng **13 giây** (trung vị), so với câu kho thường khoảng 3 giây. Chậm, nhưng chỉ xảy ra với câu kho không có.
- Tiền: khoảng **0,0018 USD** một câu có tra web, gồm Serper và model.

**Đường ra mới.** Tra web là lần đầu chatbot gửi chữ của người dùng (đã dựng thành câu tìm) ra một dịch vụ ngoài OpenAI. Anh đã chấp nhận điều này khi duyệt
thiết kế Phase 9.

## Hỏi bằng ảnh: gợi ý, chờ xác nhận

**Cách chạy:**
1. Người dùng chụp hoặc chọn ảnh. Máy chủ kiểm trước khi đọc: chỉ nhận **JPEG, PNG, WEBP**, tối đa **10 MB**, không quá 40 triệu điểm ảnh, phải gửi từ đúng trang
   web của chatbot. Sai thì trả lỗi ngay.
2. Ảnh được **xoá thông tin kèm theo** (vị trí chụp, máy chụp), **thu nhỏ** còn cạnh dài 1.024 điểm ảnh, rồi gửi cho gpt-6-luna kèm **danh sách 42 điểm / món dễ
   nhận ra bằng ảnh**. Danh sách do code lập từ kho. Không kèm chữ của người dùng, không kèm lịch sử. Máy chủ **không lưu ảnh**.
3. Model chỉ được trả **tối đa 3 mã trong danh sách**, hoặc "không nhận ra". Code kiểm lại mã có trong danh sách thật.
4. Giao diện hiện **gợi ý (có thể sai)** với các nút tên. Người dùng **bấm đúng tên** ⇒ thành một câu hỏi thường, đi đường trả lời từ kho. **Không bấm thì không
   trả lời gì.**

**Vì sao phải chờ xác nhận.** Đo trên bộ ảnh (05/11): tên đúng nằm trong 3 gợi ý ở **22 / 25 ảnh**, đạt ngưỡng đặt trước (22). Nhưng với **ảnh không phải ở Huế**,
model vẫn gán một tên Huế cho **2 / 5 ảnh**, vượt ngưỡng cho phép (tối đa 1). Theo thước đặt trước thì kết quả **âm**. Anh quyết giữ tính năng nhưng ở dạng
**gợi ý có xác nhận**: model đoán nhầm thì người dùng không bấm, không có câu trả lời sai nào được viết ra.

**Tốc độ và tiền:** đoán mất khoảng **3 giây** ở trung vị, nhưng câu chậm 6–9 giây (chưa đạt mức 5 giây); khoảng 0,0004 USD một ảnh.

## Một chuyện thật: rào chắn bằng code bắt được điều lời dặn không bắt

**Tra web, vòng đầu.** Ở 2 câu, mục web **khẳng định như thật** lịch cúp điện và mức lũ lấy từ một trang chưa kiểm. Đây đúng loại lỗi nặng nhất (sai cảnh báo an
toàn). Cách sửa không phải dặn model "cẩn thận hơn", mà thêm **luật bằng code**: câu thiên tai thì thay bằng câu cố định; câu "ngay lúc này" có số thì thay bằng
"chưa xác minh". Review sau đó còn bắt thêm hai lỗ: link dạng mã trang web thô lọt qua bộ lọc, và bộ dò thiên tai thiếu chữ "lụt", "áp thấp". Cả hai được vá
bằng code.

**Hỏi bằng ảnh.** Thử cả cách không dùng model lớn: một model nhận ảnh chạy trên máy (SigLIP 2). Cách tốt nhất của nó được 20 / 25 ảnh đúng, nhưng gán tên Huế
cho **cả 5 / 5** ảnh không phải Huế, kể cả một ảnh con mèo. Bỏ. Còn thử ảnh có dán chữ kiểu "ra lệnh" cho model: 1 / 3 ảnh lừa được model ở mọi lượt. Đây là
thêm một lý do để **không trả lời khi người dùng chưa xác nhận**.

## Khi nào hỏng

- **Mục web có thể sai hoặc cũ** dù đã ghi "chưa kiểm". Địa chỉ, số điện thoại trong mục web chưa được kiểm là có trong đoạn trích hay không.
- **Mục web chậm** (khoảng 13 giây).
- **Luật "ngay lúc này" có thể chặn nhầm** nếu dò quá rộng (ví dụ chữ "đang").
- **Ảnh:** các lăng, các điện trông giống nhau dễ nhầm; ảnh có chữ lừa có thể đánh lừa model; chưa giới hạn số ảnh mỗi người; câu chậm chưa đạt 5 giây.
- Bản đóng gói để đưa lên mạng (bài 18) đặt tra web **tắt**.

## Ba điều chính

1. **Tra web chỉ khi kho đã từ chối**, một lần, 5 giây. Mục **"Từ web (chưa kiểm)"** tách riêng. **Code chặn** link lạ, số tiền không có trong đoạn trích, câu
   "ngay lúc này", và thay câu thiên tai bằng câu cố định. Bộ kín: 0 / 7 câu khẳng định thông tin chưa kiểm.
2. **Hỏi bằng ảnh = gợi ý tối đa 3 tên, chờ người dùng bấm xác nhận.** Đúng trong 3 gợi ý 22 / 25 ảnh, nhưng gán nhầm tên Huế cho ảnh ngoài, nên phải xác nhận.
   Ảnh không lưu, đã xoá thông tin kèm theo.
3. Chuyện thật: những lỗi nguy hiểm nhất (khẳng định lũ, cúp điện) được chặn bằng **luật trong code**, không bằng lời dặn.

**Bài sau:** Bài 16 — Kể đồ án trong 2–3 phút (bản đủ), cùng chỗ còn yếu và hướng sửa.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Cổng web: `backend/llm/assistant.py` `web_gate_open`; cờ `tra_web: true`: `backend/config/settings.yaml` [code]
- Tra web: `backend/llm/tra_web.py` (dựng câu tìm, Serper một lần, `tra_web_timeout_seconds: 5`, ≤ 5 kết quả, kiểm `[w n]`, chặn link / HTML, số tiền ⊂ đoạn trích, lưu trú 0 tiền, `la_cau_thoi_gian_thuc`, `la_cau_thien_tai`) [code]; nhãn mục web: `frontend/src/pages.jsx` [code]
- Bộ kín web 0 / 7, 7 / 7; khoảng 13 s; khoảng 0,0018 USD; hai câu cúp điện / lũ vòng đầu; review bắt link thô và thiếu "lụt / áp thấp" (05/11): `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` [đã chạy]
- Đường ra Serper anh chấp nhận: spec Phase 9 §7; `session_prompt/Project_Status.md` §6 [quyết định của anh]
- Hỏi bằng ảnh: `backend/api/routes/anh.py` (kiểu ảnh, 10 MB `max_bytes`, kiểm trước khi đọc, Origin), `backend/llm/nhan_anh.py` (danh sách tên, ≤ 3 mã / `khong_nhan_ra`, kiểm lại mã, thu nhỏ `canh_dai`, xoá EXIF) [code, xem 11/11]; danh sách 42 mục: `data/phase_10/anh/danh_sach_ten.json` (riêng tư; đếm 11/11) [đã chạy]
- Ảnh: 22 / 25 trong 3 gợi ý, ảnh ngoài Huế 2 / 5; SigLIP 2 20 / 25 và 5 / 5; ảnh chữ lừa 1 / 3; khoảng 3 s, câu chậm 6–9 s; khoảng 0,0004 USD / ảnh: `bao_cao_he_thong/08_BAO_CAO_HOI_BANG_ANH.md` (05/11) [đã chạy]
- "Khách sạn gần cầu Trường Tiền" là câu tự đặt.

- **Sửa 14:48 11/11/2026:** theo luật anh chốt ("phần chưa xong thì không đưa vào bài học"), gỡ đoạn tả việc chưa làm xong: câu "đang chờ anh quyết lúc deploy" → tả đúng bản đóng gói đã dựng (`HUE_TRA_WEB` "false" trong `data/phase_12/deploy_nhap/compose.yml`).

</details>
