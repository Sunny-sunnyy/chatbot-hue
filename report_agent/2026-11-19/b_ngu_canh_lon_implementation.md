# Thử đưa ngữ cảnh LỚN HƠN vào model viết câu trả lời — kết quả (phiên B chạy + chấm; phiên C viết plan; phiên E đọc tay)

Viết 19:04 19/11/2026 (giờ `date`). Hồ sơ riêng tư đủ số, mã câu và từng ô: `data/ngu_canh_lon_2026-11-19/KET_QUA.md` (không vào git). Plan bản duyệt `689f192dc249`. File này chỉ ghi ở mức loại câu.

Từ dùng: **đoạn** = một mảnh nhỏ của bài trong kho mà bước tìm trả về · **mốc** = bản đang chạy, đưa 10 đoạn cho model · **nhánh 15 đoạn** = đưa 15 đoạn · **nhánh cả mục** = mỗi đoạn trong 10 đoạn được thay bằng cả mục chứa nó · **bộ câu mẫu** = 176 câu hỏi kèm đáp án · **bộ an toàn** = 32 câu hỏi về cảnh báo / điều kiện · **sàn** = lỗi không được phép có thêm · **"Đủ ý"** = điểm 1–5 do người chấm cho, đo câu trả lời có đủ ý của đáp án không.

## 1. Người dùng thấy gì khác
Không có gì đổi: **không nhánh nào được đề nghị đưa vào bản chạy**. Trợ lý vẫn đưa 10 đoạn cho model như trước.

## 2. Kết quả so với mốc chạy cùng buổi
| | 15 đoạn | Cả mục | Mốc (10 đoạn) | Nhãn |
|---|---|---|---|---|
| "Đủ ý" trên 129 câu số chính: chênh trung bình so với mốc (khoảng tin cậy 95 % đã chỉnh cho hai phép so) | −0,008 (−0,140 đến +0,116) | −0,008 (−0,047 đến +0,031) | — | [máy kiểm; chưa người thứ hai tính lại] |
| Xếp loại theo luật ghi trước | **không khác** | **không khác** | | |
| Số câu thắng / hoà / thua ở "Đủ ý" | 7 / 117 / 5 | 3 / 122 / 4 | | [máy kiểm] |
| "Đúng": chênh trung bình (sàn: không thấp hơn −0,1) | −0,031 đạt | +0,008 đạt | | [máy kiểm] |
| Câu ngoài kho bị trả lời MỚI (sàn 0; 18 câu) | 0 | **1 — phạm** | 0 | [máy kiểm; người thứ hai đọc: không con số, không ý bịa] |
| Lỗi trích dẫn mới (sàn 0) | **1 — phạm** | 0 | 0 | [máy kiểm; người thứ hai đọc: nội dung đúng, thiếu ký hiệu nguồn] |
| Nói chắc mà sai mới (sàn 0) | 0 | 0 | | [máy kiểm] |
| Câu trong kho bị từ chối nhầm | 2 (một câu là mới) | 2 | 4 | [máy kiểm] |
| Tiền mỗi câu so với mốc | ×1,20 | ×1,48 | 0,000419 USD | [máy kiểm] |
| Chữ đưa vào model mỗi câu (token, trung bình trên cả 176 câu, kể cả 11 câu không gọi trợ lý) | 3.290 | 4.540 | 2.551 | [máy kiểm] |
| Thời gian cả câu, giữa / chậm nhất 5 % (giây; máy dùng chung, không phải lượt đo tốc độ) | 5,4 / 9,9 | 5,6 / 10,8 | 5,5 / 11,1 | [máy kiểm] |

**Bộ an toàn (32 câu × 2 lượt mỗi nhánh; hai người chấm độc lập, không biết bản nào thuộc nhánh nào; cả hai người chấm bắt 10 / 10 câu sai cài sẵn và báo nhầm 0 / 5 câu đúng cài sẵn):**
- Nhánh 15 đoạn: **sạch về cảnh báo an toàn** [người thứ hai kiểm]. Còn một ô về điều kiện vé bị gắn "thiếu", nằm trong mức dao động của chính mốc.
- Nhánh cả mục, dòng 1 — **phạm thật:** ở một lượt, một câu mất cảnh báo "tạm ngừng mùa lũ" mà mốc có ở cả hai lượt. Lý do: ngữ cảnh to hơn nên lượt đó model không trích đúng mục chứa câu cảnh báo, và code chỉ nối dòng cảnh báo từ nguồn ĐÃ được trích [người thứ hai kiểm].
- Nhánh cả mục, dòng 2 — **phạm theo luật "cột riêng":** một câu bỏ hai cảnh báo chỉ có ở phần ngữ cảnh thêm, cả hai lượt. Bản mốc cũng không cho người dùng hai ý này; luật này luôn bất lợi cho nhánh ngữ cảnh to [người thứ hai kiểm].
- Đảo cảnh báo: 0 ở cả hai nhánh [người thứ hai đọc; người chấm có gắn "trái nguồn" cho một câu ở lượt 2 của cả hai nhánh — chính mốc lượt 1 cũng bị gắn đúng câu đó nên người đọc xếp vào dao động của mốc]. Câu ngoài kho bị trả lời: 0 / 3 ở mọi lượt. Câu an toàn bắt buộc sinh lại 3 + 3 lần: thiếu cảnh báo 3 / 3 ở cả nhánh lẫn mốc ⇒ không phải lỗi mới.
- **Đừng tin số ô thô:** người chấm gắn 1–6 CÂU "mới" mỗi cặp nhánh ↔ mốc (một câu có thể bị gắn ở hơn một loại lỗi), nhưng hai lượt MỐC không đổi gì so với nhau cũng lệch 1 câu mới + 4 câu hết. Chỉ các ô người đọc tay xác nhận ở trên là khác biệt thật.

**Đọc tay các cặp lệch điểm của bộ câu mẫu (phiên E, 37 cặp):** khoảng hai phần ba là cùng nội dung, điểm lệch do cách diễn đạt. Nhánh 15 đoạn được 4 câu thêm ý thật và mất 5; nhánh cả mục được 2, mất 2. Không cặp nào có khẳng định trái đáp án.

## 3. Giới hạn
- Bộ an toàn chạy trên ba bản code vì nhánh chính nhận hai nhánh code (cờ tắt) giữa lượt đo; đã chụp lại 228 yêu cầu gửi model sau khi gộp: giống từng byte bản đầu buổi. Bộ câu mẫu ba nhánh cùng một bản.
- File kết quả bộ an toàn không lưu dòng cảnh báo do code nối ⇒ đã DỰNG LẠI bằng chính hàm đang chạy thật (thử trước trên dữ liệu cũ biết chắc có dòng nối: ra đúng danh sách đã ghi); không phải bản ghi của lượt thật. Con số "0 dòng" B ghi buổi chiều là sai và đã được sửa.
- Mỗi nhánh một lượt trên bộ câu mẫu; hai ô phạm sàn ở bảng đứng trên một lượt, chưa biết lặp lại hay ngẫu nhiên (lượt sinh lại riêng hai câu đó KHÔNG chạy: kết luận không còn phụ thuộc nó). Bộ câu mẫu đã dùng nhiều lượt, không có bộ kín cho việc này.
- Người chấm là 57 agent con cùng hãng; B tự kiểm mẫu 3 mục điểm thấp với nguồn (khớp). Công cụ chấm do B viết, phiên E đọc hai vòng, sáu điểm đã sửa trước khi chấm, có ca thử bằng điểm cài sẵn.
- Hai dòng đếm máy của plan về "phép kiểm số tự nới theo cỡ ngữ cảnh": chưa đo (NOT RUN) vì không nhánh nào đi tiếp.
- Nhánh "cả bài" đã dừng từ bước 1 (nối nhầm cảnh báo của hoạt động khác, giá ×5,5).

## 4. Tiền thật
Bước 0: 0 USD · bước 1: 0,144 · bước 2 (sinh): 0,442 · chấm: 0 USD (agent con). **Cả việc 0,586 USD**, trần cứng đã duyệt 1,40.

## 5. Bảng "xong"
| Việc | Trạng thái | Lệnh kiểm (từ `backend/`; `V=../data/ngu_canh_lon_2026-11-19`) ⇒ đầu ra |
|---|---|---|
| Chấm mù bộ câu mẫu ba bên, một lô | XONG | `DO_CUOI_DIR=$V/chay/b2_cham B7_EXPECT=3622a573e28e,ea442226257d,9436 PYTHONPATH=$PWD uv run python $V/tools_B/ba_nhanh_nc.py check-judge` ⇒ `"items": 448, "scores": 448, "missing": []` |
| Bảng "Đủ ý" + sàn từng nhánh | XONG | `… ba_nhanh_nc.py ba-muc --khong-ghi` ⇒ hai dòng `xếp loại: không khác`; `… san --khong-ghi` ⇒ nhánh 15 đoạn: `loi_trich_dan_moi` có 1 câu; nhánh cả mục: `ngoai_kho_bi_tra_loi_moi` có 1 câu |
| Chấm an toàn 3 nhánh × 2 lượt, hai người chấm | XONG | `B7_OUT=$V/chay/b2_at PYTHONPATH=$PWD uv run python $V/tools_B/an_toan_3x2.py check --judge 1` ⇒ `"items": 187, "labels": 187, "n_errors": 0` |
| Câu an toàn sinh lại 3 + 3, hai nhánh | XONG | `python3 -m json.tool $V/chay/b2_at_s19_MUC/an_toan/cham/compare_regen.json` ⇒ `"moi_that_P0_thieu": false` |
| Dựng lại dòng cảnh báo do code nối | XONG | `PYTHONPATH=$PWD uv run python $V/tools_B/noi_lai_an_toan.py dem` ⇒ 11 dòng nối trên 6 lượt chính |
| Đọc tay (phiên E) | XONG | `grep -c '' $V/chay/doc_tay_E.md`; mục 6 và 7 |
| Nhận định của người viết plan (phiên C) | CHƯA — sau lượt test của C | |
| Sinh lại hai câu phạm sàn × 3 | KHÔNG làm — phiên điều phối bỏ, lý do ở mục 3 | |
| Hai dòng đếm "phép kiểm số tự nới" | Tự hoãn — không nhánh nào đi tiếp | |
| Viết vào `bai_hoc/` | CHƯA — sau nhận định của C | |
