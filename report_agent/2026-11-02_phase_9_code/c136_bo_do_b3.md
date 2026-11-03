# Implementation Report: Phase 9 B3 — bộ đo nhớ hội thoại (C136)

Người làm: C (Claude Opus 5.5) — không code B3
Date: 09:48 03/11/2026 (`date`)
Mục việc: tin A sáng 03/11 (C136). Spec Phase 9 bản 9 `169c2dd5f86a` §3 "Nhớ", §4 bảng bộ đo ("nhớ (B3): 40 chuỗi + 3 chuỗi nêu tên rồi hỏi câu cần web (B6) · 25 / 15"), §5 B3, §5 B6.
0 USD. Mục lục bộ đo (private): `data/phase_9/bo_do_b3/README.md` `2c094e287c65`. Report này chỉ có số đếm, md5, cách viết — không câu hỏi, không tên đối tượng, không `case_index`.

## 1. Phạm vi

Viết bộ chuỗi hội thoại nhiều lượt cho B3 + 3 chuỗi cho B6, kèm nhãn kỳ vọng từng lượt và script kiểm. Không code, không chạy chatbot, không viết harness. Mức tối thiểu đủ cho tiêu chí spec §5 B3.

## 2. Thay đổi chính (private, `data/phase_9/bo_do_b3/`)

| File | md5 (12) | Số |
|---|---|---|
| `chuoi_da_thay.jsonl` | `2f4f985b5540` | 25 chuỗi / 56 lượt |
| `chuoi_sealed.jsonl` | `e7cd934bd6cf` | 15 chuỗi / 33 lượt — **B không mở** |
| `web_neu_ten.jsonl` | `2219b5c65237` | 3 chuỗi / 6 lượt (B6) |
| `tools/kiem_bo.py` | sha256 `9377764f0033` | kiểm luật + in số đếm |

| Loại | Đã thấy | Kín | Tiêu chí spec §5 B3 |
|---|---:|---:|---|
| nhớ tên (gồm chuỗi sửa tên, nói tên ở giữa) | 6 | 4 | quyết 1: ≥ 9 / 10 |
| hỏi tiếp ý cũ | 5 | 3 | quyết 2: Completeness lượt sau, nhớ bật ↔ câu gõ thật gửi không lịch sử (A quyết D11 (a) plan B3; câu viết lại đứng một mình = trần, chỉ báo số) |
| hỏi tiếp ý mới ("còn … thì sao") | 4 | 2 | quyết 2 |
| hỏi tiếp ngoài kho | 4 | 2 | sàn: 0 câu bị trả lời |
| hỏi tiếp điều kiện / an toàn | 3 | 2 | sàn: 0 đảo cảnh báo |
| đổi chủ đề | 3 | 2 | mức tụt ≤ 1 câu |

## 3. Cách viết

- Câu có dấu, NFC, kiểu người thật hỏi tiếp ("lăng đó", "quán đó", "còn … thì sao", sửa tên).
- Mỗi lượt có nhãn: tuyến kỳ vọng, kỳ vọng (trả lời / nhắc tên / từ chối / giữ cảnh báo / web), câu viết lại đứng một mình, từ câu tìm kho phải / không được chứa.
- **Đáp án mẫu không viết mới:** lượt hỏi tiếp viết lại đứng một mình trùng nghĩa với một câu Golden 176 (không `out_of_scope`) ⇒ chấm Completeness / đảo cảnh báo bằng đáp án mẫu Golden sẵn có. Lượt sau có đáp án mẫu: đã thấy 20, kín 10.
- **Kín** không dùng chung câu Golden nào với phần đã thấy / web (máy kiểm).
- Câu "ngoài kho" + câu cần web: kiểm bằng `scripts/grep_kb.sh` (0 dòng trong file của đối tượng; một đề tài kho có ⇒ bỏ).
- Tên trong chuỗi nhớ tên chọn để không trùng chữ thường gặp; luật chấm: khớp nguyên từ, phân biệt hoa thường (đã đổi 4 tên dễ trùng).

## 4. Kết quả quan sát

- `kiem_bo.py`: **OK** — 40 chuỗi B3 (nhớ tên 10); 2–4 lượt mỗi chuỗi; mọi câu NFC có dấu; mọi câu đứng một mình chứa đủ từ phải chứa, không chứa từ cấm; lượt điều kiện đều có đáp án mẫu; kín ∩ đã thấy (Golden) = 0; không trùng id.
- Ca thử phá (bản sao `/tmp`, đã xoá): thêm đối tượng cũ vào một câu đứng một mình ⇒ script dừng đúng lỗi "chứa từ cấm".
- Mọi tên được hỏi lại đều đã nêu ở lượt trước (kiểm bằng script).

## 5. Giới hạn

- Câu đứng một mình do C soạn; "trùng nghĩa" với câu Golden là phán đoán của người viết.
- Thước "câu tìm phải chứa" là chuỗi con thô.
- Ý "ngoài kho" kiểm bằng chữ; kho có thể nói bằng chữ khác — câu nào bị trả lời thì người chạy kiểm lại.
- Mẫu 10 câu cho User đọc (spec §4 "User đọc mẫu 10 câu"): **chưa làm** — chờ A nói có cần ở bậc này không.
- Harness gửi nhiều lượt qua cùng phiên: việc của người code B3.

## 6. Tiền

0 USD.
