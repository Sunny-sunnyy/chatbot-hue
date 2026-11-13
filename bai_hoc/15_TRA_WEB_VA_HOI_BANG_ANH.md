# Bài 15 — Khi sổ không có: tra web, và hỏi bằng ảnh

*Cập nhật lần cuối: 20:37, ngày 13/11/2026 · sửa theo kiểm độc lập; thêm chuyện thật thứ hai: thử Exa cho tra web rồi giữ Serper; ghi ngày cho số tốc độ mục web (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Tra web | **`tra_web`** (dịch vụ **Serper**, tìm Google) | Khi kho không có, code tìm web **một lần** rồi model viết một mục riêng (đã gặp ở bài 12). |
| Cổng web — **mới** | **`web_gate_open`** | Điều kiện để được tra web: câu về Huế, kho đã trả câu từ chối, không lỗi gì khác. |
| Mục web | **"Từ web (chưa kiểm)"** | Phần trả lời từ web, tách riêng khỏi phần trả lời từ kho. |
| Sổ link — **mới** | mã **`[w n]`** | Mỗi kết quả web có một số; model chỉ được trích các số có trong sổ. |
| Hỏi bằng ảnh | **`nhan_anh`** (cờ `anh.bat: true`) | Người dùng gửi ảnh; model gợi tối đa 3 tên trong một danh sách 42 mục; người dùng bấm xác nhận rồi mới trả lời (đã gặp ở bài 12). |
| Rào chắn | **guardrail** | Chỗ code chặn trước khi chữ tới người dùng. |
| Exa — **mới** | dịch vụ tìm web **Exa** (`highlights`) | Một dịch vụ tìm web khác, trả **đoạn trích nguyên văn trong trang**, chọn theo câu hỏi. Đã thử 12/11, không dùng. |

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
- Tốc độ (bộ kín, 05/11): mục web tới sau khoảng **13 giây** (trung vị), so với câu kho thường khoảng 3 giây. Chậm, nhưng chỉ xảy ra với câu kho không có.
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

## Chuyện thật thứ hai: thử Exa, đo riêng thì đạt, qua máy chủ thật thì không

**Vì sao thử.** Mình đếm trên log máy chủ (từ 05/11): **73 lượt** có tra web. Có mục web ở **44 lượt (60 %)**; 13 lượt (18 %) ra "chưa xác minh" do luật "ngay lúc
này" (cố ý); 14 lượt (19 %) bị luật kiểm **bỏ cả mục** vì không tin cậy; Serper không lỗi lần nào, tra mất khoảng 2 giây. Giả thuyết: Serper chỉ đưa **tiêu đề và
một đoạn trích ngắn**, trung vị 147 ký tự mỗi kết quả, và 32 % kết quả là trang mạng xã hội. Câu hỏi giá, giờ cần con số nằm trong trang, không nằm trong 147 ký
tự đó, nên model hay viết số theo trí nhớ, rồi luật kiểm số tiền bỏ mục. Exa trả **đoạn trích nguyên văn từ trong trang, chọn theo câu hỏi**, và lọc được tên
miền. Đổi lại, Exa đắt hơn (khoảng 0,007 USD một lượt, Serper 0,001), chưa ai đo công khai với tiếng Việt, và gói thường cho phép họ dùng câu tìm để cải thiện
sản phẩm.

**Bước 1: đo riêng bước tra.** Một thí nghiệm ngoài máy chủ gọi đúng phần viết mục web và luật kiểm của chatbot, **chỉ thay dịch vụ tra**. Bộ đo 42 câu tự viết,
đã thấy, gồm ba loại: câu cần web, câu hỏi kèm hai ý, câu về chỗ ở và quán gần. Luật ghi trước: đếm số câu có mục web **đúng và trả lời được câu hỏi**, do **2
người chấm mù** cùng gắn; Exa phải hơn Serper ít nhất 5 câu. Kết quả: Serper **17**, Exa **25** ⇒ đạt (cần 22). Exa còn tra nhanh hơn (câu chậm 2,2 giây so với
3,1) và không trích trang mạng xã hội nào (Serper: 24 / 91 nguồn). Nhưng kết quả **nhạy**: 5 mục của Exa trích một trang tổng hợp do chính Exa tạo, không ghi
dữ liệu gốc. Bỏ 5 mục đó thì Exa còn 20, dưới ngưỡng. Bản Exa loại hẳn mạng xã hội cũng chỉ được 20.

**Bước 2: code sau cờ.** Thiết kế **Exa trước, Serper dự phòng**: Exa có hạn 3 giây; Exa lỗi, hết giờ hoặc không ra kết quả thì gọi Serper một lần với thời gian
còn lại; tối đa 40 lượt Exa mỗi ngày; thiếu khoá Exa thì dùng Serper. Cờ mặc định vẫn là Serper.

**Bước 3: đo qua máy chủ thật**, cùng 42 câu, mỗi bên một lượt. Luật ghi trước: Exa phải hơn Serper ít nhất 3 câu. Kết quả: Exa **14**, Serper **13** (cần 16)
⇒ **không đạt**. Các sàn đo bằng code đều qua (cờ tắt y như cũ, khoá sai thì Serper đỡ, tra vẫn nhanh hơn: câu chậm 2,26 so với 2,82 giây); phần chấm an
toàn chỉ làm được một phần vì công cụ đo không lưu chữ mục web. Vì vậy **giữ Serper**; phần
code Exa không vào bản chính, chỉ giữ làm hồ sơ.

**Vì sao hai lần đo khác nhau.** Quan sát: qua máy chủ, chỉ những câu **kho đã từ chối** mới được tra (khoảng 30 / 42 câu), nên ít chỗ để Exa hơn Serper. Đoạn
trích dài hơn làm model viết nhiều con số hơn, nên luật kiểm bỏ mục nhiều hơn (13 lượt "không tin cậy" so với 10). Còn nhiễu giữa hai ngày chạy thì là giả
thuyết, chưa tách được vì mỗi bên chỉ chạy một lượt.

**Bài học:** **đo trên đường người dùng thật trước.** Đo riêng một bước bỏ qua cổng web và luật kiểm phía sau, nên thấy lợi mà người dùng không nhận được.
Tiền cả việc: khoảng **0,195 USD** thật (khoảng 4.900 đồng), cộng khoảng 0,82 USD tín dụng dùng thử miễn phí của Exa.

## Khi nào hỏng

- **Mục web có thể sai hoặc cũ** dù đã ghi "chưa kiểm". Địa chỉ, số điện thoại trong mục web chưa được kiểm là có trong đoạn trích hay không.
- **Mục web chậm**: khoảng 13 giây tới mục web (bộ kín, 05/11); trên 42 câu tự viết qua máy chủ 12/11, khoảng 18 giây ở trung vị.
- **Một con số không khớp là mất cả mục.** Khoảng 1 / 3 lượt tra mất mục web vì luật kiểm số (đo 12/11, cả với Serper lẫn Exa). Luật này cố ý chặt; chưa thử
  cách chỉ bỏ câu có số sai.
- **Luật "ngay lúc này" có thể chặn nhầm** nếu dò quá rộng (ví dụ chữ "đang").
- **Ảnh:** các lăng, các điện trông giống nhau dễ nhầm; ảnh có chữ lừa có thể đánh lừa model; chưa giới hạn số ảnh mỗi người; câu chậm chưa đạt 5 giây.
- Bản đóng gói để đưa lên mạng (bài 18) đặt tra web **tắt**.

## Ba điều chính

1. **Tra web chỉ khi kho đã từ chối**, một lần, 5 giây. Mục **"Từ web (chưa kiểm)"** tách riêng. **Code chặn** link lạ, số tiền không có trong đoạn trích, câu
   "ngay lúc này", và thay câu thiên tai bằng câu cố định. Bộ kín: 0 / 7 câu khẳng định thông tin chưa kiểm.
2. **Hỏi bằng ảnh = gợi ý tối đa 3 tên, chờ người dùng bấm xác nhận.** Đúng trong 3 gợi ý 22 / 25 ảnh, nhưng gán nhầm tên Huế cho ảnh ngoài, nên phải xác nhận.
   Ảnh không lưu, đã xoá thông tin kèm theo.
3. Chuyện thật: những lỗi nguy hiểm nhất (khẳng định lũ, cúp điện) được chặn bằng **luật trong code**, không bằng lời dặn. Thử đổi Serper sang Exa: đo riêng
   bước tra thì đạt (25 so với 17) nhưng nhạy, qua máy chủ thật thì không (14 so với 13) ⇒ giữ Serper.

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
- Exa (12/11): 73 lượt log, 44 / 13 / 14, 0 lỗi Serper, 147 ký tự, 32 % mạng xã hội, giá 0,007 ↔ 0,001, điều khoản dùng dữ liệu: `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` §1–2; thí nghiệm 17 / 25 / 20, p95 3,1 / 2,2, mạng xã hội 24 / 91 ↔ 0 / 109, độ nhạy 25 ⇒ 20 khi loại trang tổng hợp của Exa: cùng file §5, §6, §6b; server thật 13 / 14 (cần ≥ 16), không tin cậy 10 / 13, tra p95 2,82 / 2,26, tới sự kiện web 17,9 / 16,9 s, ≈ 30 / 42 câu được tra, 13 / 30 và 10 / 29 lượt mất mục do luật kiểm, ≈ 0,195 USD + ≈ 0,82 tín dụng: §7 [đã chạy]; kiểm thí nghiệm: `…/e_exa_review.md`; kiểm code (Exa trước 3 s, Serper dự phòng, 40 lượt / ngày): `…/e_exa_code_review.md`; nhánh `p9-tra-web-exa` không merge (`tra_web.py` trên `main` không có Exa), tag `hoso/p9-tra-web-exa` [code, theo bản ghi số liệu 13/11]. Bản ghi số liệu: `data/hoc_cung_user_2026-11-10/fact_viec_12_11.md` (riêng tư)
- **Sửa 20:22 13/11/2026:** số "khoảng 13 giây" ghi rõ là bộ kín 05/11, thêm số 12/11 qua máy chủ (khác bộ câu, khác cách đo).

- **Sửa 14:48 11/11/2026:** theo luật anh chốt ("phần chưa xong thì không đưa vào bài học"), gỡ đoạn tả việc chưa làm xong: câu "đang chờ anh quyết lúc deploy" → tả đúng bản đóng gói đã dựng (`HUE_TRA_WEB` "false" trong `data/phase_12/deploy_nhap/compose.yml`).
- **Sửa 20:37 13/11/2026** theo kiểm độc lập (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_13_11.md`, riêng tư): bảng từ còn 3 từ mới: "Tra web", "Hỏi bằng ảnh" đã gặp ở bài 12.

</details>
