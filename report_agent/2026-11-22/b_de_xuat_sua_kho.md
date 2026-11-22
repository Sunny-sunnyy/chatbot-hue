# Lệnh đề xuất sửa kho khi một giá đổi + lệnh duyệt (Phase 12, mục [7], nửa của phiên B)

Viết 08:43 22/11/2026 (giờ `date`). Nhánh `p9-b-de-xuat-sua-kho`, tách từ main `4653fddb`. Người viết: phiên B. Chưa ai đọc lại.

**Từ dùng:** *kho* = các bài Markdown trong `knowledge-base-hue/` · *chỉ mục* = bản đã chia đoạn + vector của kho trong Qdrant, chatbot tìm trên đó · *lần xuất hiện* = một chỗ một con số đứng trong một dòng (một dòng có thể có nhiều lần) · *file vá* = file ghi "dòng này đổi thành dòng kia", áp bằng `git apply` · *bản chép kho* = một bản repo riêng ở thư mục tạm để thử, không phải kho thật · *phán* = model trả lời "đúng / không / không rõ" cho một chỗ.

Quyết định đang chờ kết quả này: chủ dự án đã chọn (22:22 21/11) "lệnh chạy tay + cập nhật riêng bài đã sửa". Việc này là nửa lệnh; nửa cập nhật chỉ mục do phiên C làm (`ingestion.cap_nhat_rieng`, nhánh khác).

## 1. Người giữ kho làm được gì / chưa làm được gì

| Việc | Trạng thái |
|---|---|
| Hỏi kho "nơi X đang được ghi những mức giá nào" (`--noi`), 0 đồng, không model | Làm được [máy kiểm] |
| Gõ một lệnh báo "mức giá này từ A thành B, nguồn Z" ⇒ nhận bản đề xuất đọc được + file vá; kho không đổi | Làm được [máy kiểm, hai ca thật trên bản chép] |
| Bản đề xuất tách ba nhóm: sẽ sửa · không rõ, bạn xem · không phải giá này; mỗi chỗ sửa hiện bài, câu cũ ⇒ câu mới, vì sao | Làm được [máy kiểm; người viết đọc] |
| Bản đề xuất nhắc các câu có "tổng / tiết kiệm" có thể tính từ giá cũ, và bảng dữ liệu ngoài kho nào còn ghi giá cũ / chép câu vừa đổi | Làm được [máy kiểm] — chỉ NHẮC, không tự tính lại |
| Duyệt bằng một lệnh: kiểm kho chưa đổi từ lúc đề xuất ⇒ áp ⇒ lưu bản ghi git | Làm được [máy kiểm trên nhánh tạm của bản chép, qua cả hook kiểm trước khi ghi] |
| Sau khi duyệt, chỉ mục tự cập nhật cho riêng bài đã sửa | CHƯA — chờ nhánh của C; code gọi đã viết theo giao diện C báo, chưa chạy lần nào |
| Lệnh tự đi tra web để phát hiện giá đổi (đường phụ) | CHƯA làm |
| Sửa giờ mở cửa, số điện thoại, hay câu chữ | Không làm — lệnh chỉ thay MỘT con số tiền |

## 2. Dữ liệu thật đã làm đổi thiết kế so với bản nháp tối 21/11

1. Con số 200.000 nằm ở 37 lần / 14 bài (268 bài được quét = 265 bài trong chỉ mục + 3 file kiểm kê). Vé Đại Nội chỉ là 9 lần; còn lại là vé gộp hai lăng (cũng 200.000, cùng bài), giá một điểm tham quan khác, giá quán ăn, đầu của khoảng dự toán, và một con số đếm tờ văn bản ⇒ ca "giống mà không phải" có sẵn trong kho.
2. Ô bảng ghi số trơn không đơn vị ⇒ bộ nhận số tiền đang có (`llm.so_tien.tim_so_tien`, đòi có đơn vị) không dùng được ⇒ viết bộ tìm theo GIÁ TRỊ (`ops/sua_kho.py`): nhóm nghìn có / không đơn vị, "200k", "200 nghìn"; số dài hơn chứa nó ("1.200.000") không tính.
3. Đơn vị xét là từng lần xuất hiện, không phải từng dòng — một dòng có thể mang cùng con số cho hai nơi.
4. Có câu mang con số tính từ giá cũ (tổng của hai vé, mức tiết kiệm của vé gộp) ⇒ code không tính lại; bản đề xuất đánh dấu.
5. Có dòng viết MỘT con số cho nhiều nơi (ba lăng cùng 150.000 trên một dòng) ⇒ thay con số là đổi luôn giá nơi khác ⇒ luật trong lời dặn: xếp "không rõ", để người sửa câu.
6. Bảng điểm của trang Lên kế hoạch KHÔNG mang giá vé (bản nháp ghi có): ở ca thật, 8 bảng dữ liệu của trợ lý có 0 lần ghi 200.000 và 0 câu chép bị đổi.

## 3. Chia việc code ↔ model

- **Code:** dò bài kho bằng đúng bộ dò lúc dựng chỉ mục · tìm mọi lần xuất hiện theo giá trị · gom chữ quanh con số (tên bài, đường mục, dòng cha theo thụt lề, hàng đầu bảng) · dựng dòng mới bằng cách thay đúng chuỗi số, giữ kiểu viết · thêm một dòng vào mục "Nguồn dữ liệu" của mỗi bài được sửa (mục này bộ chia đoạn bỏ qua) · dựng file vá · tự chạy `git apply --check`.
- **Model:** MỘT lời gọi, không công cụ, không lịch sử; đầu ra có khuôn: mỗi mã ⇒ `dung / khong / khong_ro` + một câu lý do. Model không viết chữ nào vào kho. Mã model bịa, mã trả hai phán đoán khác nhau, mã bị bỏ sót ⇒ "không rõ" + ghi vào "điều lạ".
- **Người:** đọc bản đề xuất, chạy lệnh duyệt. Lệnh đề xuất không có đường ghi vào kho.
- Đi qua `generator.responses_model` + `generator._run` (khuôn `llm/nhan_anh.py`) ⇒ theo công tắc model của hệ thống, có hạn giờ (180 giây cho lời gọi này), có ghi tiền. Không công tắc mới trong `settings.yaml`, không đường API, không chạy trong server.

## 4. Số đo (model đang chạy: Claude Sonnet 5.5 trên Bedrock; bản chép kho ở main `07d3df02`)

Đáp án gắn tay TRƯỚC khi chạy, bằng cách đọc từng dòng có con số đó.

| Ca | Lần xuất hiện | Đáp án tay | Model phán | File vá |
|---|---|---|---|---|
| Vé vào cổng Đại Nội, người lớn: 200.000 ⇒ 250.000 | 37 lần / 14 bài | 9 đúng (6 bài, một là file kiểm kê) · 28 không | 9 đúng — trùng đủ 9 · 1 không rõ (một ví dụ cộng dự toán không nêu hạng mục — không sửa là đúng) · 27 không | Ba lần chạy (hai lần trước, một lần sau khi thêm luật ở mục 2.5): giống nhau từng byte |
| Vé Lăng Tự Đức, người lớn: 150.000 ⇒ 180.000 | 51 lần / 13 bài | 1 đúng · 3 "con số dùng chung cho nhiều lăng" · 47 không | 1 đúng · 3 không rõ, đúng ba chỗ đó, lý do nêu rõ dùng chung cho lăng nào · 47 không | Một lần chạy |

- Sai nơi (sửa giá của nơi khác): 0 / 10 chỗ được đưa vào file vá ở hai ca. Sót: 0 / 10.
- Lệnh duyệt trên bản chép, ca Đại Nội: 6 bài đổi, 9 dòng giá thay, 12 dòng thêm cho nguồn (4 bài đã có mục nguồn: mỗi bài một dòng; 2 bài chưa có: mỗi bài bốn dòng gồm tiêu đề mục); các dòng 200.000 của vé gộp hai lăng và của điểm tham quan khác còn nguyên; `git status` của kho thật: rỗng.
- Duyệt lần hai cùng đề xuất: bị từ chối ("các bài đã đổi từ lúc lập đề xuất").
- Thời gian một lần đề xuất: khoảng 22 giây. Tiền: 0,045 · 0,044 · 0,062 · 0,053 = **0,20 USD** cho bốn lần gọi (Bedrock). OpenAI: 0.
- Test: `tests/test_sua_kho.py` 12 ca đạt, không env, model là phản hồi dựng sẵn (chỉ kiểm phần code). Đã thấy đỏ một lần: bỏ dấu "không có xuống dòng cuối file" trong file vá ⇒ 2 ca đỏ (kho thật có 2 bài không có xuống dòng cuối file).

## 5. Rà theo hai skill (cập nhật bảng mục 5, 6 của bản nháp cho đường "chủ dự án báo")

| Mục | Hiện trạng | Khớp / lệch |
|---|---|---|
| Có cần agent không | Luồng cố định, model chỉ ở bước phán "con số này có phải mức giá đó không" | Khớp. Nói thật khi trình bày: đây là quy trình cố định có một bước model + người duyệt; agent của hệ thống là trợ lý chat |
| Bất biến do code | Số, dòng mới, file vá đều do code; model không trả chữ để ghi | Khớp |
| Quyết định giá lỗi cao không dựa riêng vào lời model | Model quyết chỗ nào VÀO file vá; người đọc rồi mới áp | Lệch có chủ ý, đã biết: người duyệt là lớp cuối. Giảm bằng: nhóm "không rõ" không vào file vá; mỗi chỗ hiện câu cũ ⇒ câu mới + lý do |
| Công cụ / tham số | Model không có công cụ. Đường dẫn bài do bộ dò của hệ thống sinh, không từ model | Khớp |
| Lỗi hạ tầng ≠ rỗng | Lỗi model ⇒ lệnh dừng với lỗi, không ra đề xuất rỗng; "kho không có con số này" là thông báo riêng | Khớp |
| Trần lượt, thời hạn, vết | 1 lời gọi / lần chạy, hạn 180 giây, `vet.json` giữ mọi phán đoán + tiền | Khớp |
| Chống chạy lặp | Lệnh duyệt so băm từng bài với lúc đề xuất; mỗi đề xuất một thư mục mới | Khớp |
| Bộ ba chết người | Dữ liệu riêng: không (chỉ bài kho công khai). Chữ không tin cậy: KHÔNG CÓ ở đường này (không có chữ web; lời mô tả do chủ dự án gõ). Đường ra: nhà cung cấp model đang dùng | Không thành. Khi làm đường phụ tra web phải rà lại — lúc đó có chữ web |
| Quyền ghi | Chỉ `ops.duyet_sua_kho` ghi kho, chỉ người chạy; lệnh đề xuất chỉ ghi vào thư mục đề xuất trong `data/` | Khớp. Coding agent không chạy lệnh duyệt trên kho thật (bảng quyền: sửa kho = hỏi chủ dự án) |
| Lộ khoá | Lệnh không in, không ghi biến môi trường; `vet.json` chỉ có token, tiền, phán đoán | Khớp [đọc code; chưa có test riêng — theo góp ý E 21/11 là thừa] |

## 6. Chưa làm · tự hoãn

| Việc | Vì sao |
|---|---|
| Nối thật với lệnh cập nhật chỉ mục của C | Nhánh C chưa có code. Phần gọi (`dong_bo(chi_xem=True)` rồi so `bai_doi` với các bài vừa vá, trùng mới chạy thật) đã viết theo giao diện C nhắn; CHƯA chạy ⇒ khi hai nhánh gộp cần một lượt đầu–cuối trên bản chép với collection thử |
| Đường phụ tự tra web | Giao sau khi đường chính đạt |
| Chạy bộ test các bảng chép từ kho bên trong lệnh duyệt (A yêu cầu chọn) | Chọn: lệnh đề xuất tự kiểm TRƯỚC khi duyệt (câu nào của bảng chép nguyên văn từ bài mà vừa đổi — báo ở mục 4 của bản đề xuất, là lúc người duyệt còn đọc), lệnh duyệt chỉ IN hai dòng lệnh test. Lý do: một bản sửa chỉ thay con số không thể làm một quán thành "đã đóng cửa"; còn câu chép nguyên văn thì phép kiểm trực tiếp ở trên bắt sớm hơn và không kéo bộ chạy test vào một lệnh vận hành |
| Quét trùng / 10 câu an toàn / T1 của runbook mục 5 trong lệnh duyệt | Không đưa vào: lệnh chỉ thay con số trong câu đang có, không thêm câu; hook kiểm trước khi ghi vẫn chạy lúc lưu bản ghi git. Nêu để phiên điều phối cân |
| Sổ tay + bài học cho cả tính năng (hai nửa) | Nhánh này có mục cho nửa lệnh; phần cập nhật chỉ mục bổ sung khi nhánh C gộp |

## 7. Giới hạn đã biết

- Phải biết giá cũ; mỗi lần chạy một mức giá.
- Con số viết bằng chữ, hoặc khoảng viết gọn kiểu "200–250 nghìn" (số đầu không có đơn vị), không được tìm thấy.
- Con số dùng chung cho nhiều nơi và con số tính từ giá cũ: chỉ nhắc, người sửa tay.
- Độ đúng của bước phán mới đo trên hai mức giá, một model; chưa đo trên model cũ (đang gác).
- Câu "tham khảo tháng 09/2026" ở tiêu đề mục chứa giá không được đổi theo — dòng nguồn mới ghi ngày đối chiếu ở cuối bài.

## 8. Lệnh kiểm + đầu ra

| Lệnh (từ `backend/`) | Đầu ra |
|---|---|
| `uv run pytest tests/test_sua_kho.py tests/test_assistant_boundary.py -q` | `16 passed` |
| `uv run python -m ops.de_xuat_sua_kho --noi "Đại Nội"` | bảng các số tiền đứng cùng dòng với tên nơi; 200.000: 10 lần |
| `HUE_BEDROCK_CREDS_FILE=<file khoá> uv run python -m ops.de_xuat_sua_kho --gia "Vé vào cổng Đại Nội, người lớn" --cu 200.000 --moi 250.000 --nguon "<…>" --goc <bản chép>` | `Sẽ sửa 9 chỗ ở 6 bài · không rõ 1 · không phải giá này 27 · model 0.0529 USD` · `Kho CHƯA đổi` |
| `uv run python -m ops.duyet_sua_kho <thư mục đề xuất> --goc <bản chép> --thu` | `6 files changed, 21 insertions(+), 9 deletions(-)` · `Chế độ thử: không commit…` |
| `uv run python -m ops.duyet_sua_kho <thư mục đề xuất> --goc <bản chép>` | `Đã lưu bản ghi git c13ed3e8` · `CHƯA cập nhật chỉ mục…` (mã thoát 3) |

Hồ sơ riêng tư: `data/de_xuat_kho/2026-11-22_083503/`, `…_083711/`, `…_084123/` (ca Lăng Tự Đức), `…_084208/` (bản code cuối).

Phép này KHÔNG cho biết: model phán đúng tới đâu ở mức giá không gắn với một tên nơi rõ (giá thuyền theo tuyến, giá theo khoảng) và ở lần chạy thứ n của cùng ca ngoài ba lần đã thấy · hướng rộng hơn tôi thấy: kho ghi cùng một mức giá ở nhiều bài là gốc của việc phải "tìm mọi chỗ" — một bảng giá duy nhất mà các bài trỏ tới sẽ bỏ được cả bước tìm; đó là sửa kho, việc của chủ dự án · đếm rẻ nhất: đếm bao nhiêu mức giá trong 15 bài có giá xuất hiện ở từ hai bài trở lên (0 đồng, dùng chính bộ tìm theo giá trị này).

Ý cho `session_prompt/Y_CHUA_THU.md`: bảng giá một nơi gốc (ý trên); cho lệnh nhận nhiều mức giá một lần khi một nghị quyết giá mới đổi cả biểu.
