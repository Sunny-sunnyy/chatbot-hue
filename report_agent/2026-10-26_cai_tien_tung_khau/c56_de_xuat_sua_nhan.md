# C56 — Đề xuất sửa nhãn "đoạn đúng" ở các câu bị đếm thiếu

Người làm: C (Claude Opus 5.5, `hue-rag-5b`) · 11:37 27/10/2026 +0700 (`date`) · Việc: C56 (A giao). **0 USD**, chỉ đọc + ghi nháp private. **Không sửa** file nhãn
`data/phase_8_1/gold/gold_draft.jsonl` (sha `bab707b9ab22`, kiểm lại sau khi làm). Chỉ nhóm dev được đọc; test chỉ đếm. File này không chép câu hỏi, đáp án hay nội
dung kho — chỉ `case_index`, số đếm.

## Cho bạn (3 dòng)

- Nhãn "đoạn đúng" đánh dấu **một chỗ** cho mỗi thông tin, trong khi kho thường nói lại thông tin đó ở chỗ khác. Vì vậy đôi khi máy đếm "thiếu" dù model đã thấy đủ.
- Trong 3 câu thử được giao đọc: **2 câu nên thêm khoảng nhãn** (3 khoảng), **1 câu không phải lỗi nhãn** mà do cách đếm bỏ qua tiêu đề mục. 3 câu kiểm chưa quyết vì
  không được đọc từng câu.
- Nếu áp đề xuất, kết quả "luna chọn 10 đoạn" ở bước tìm **không đổi**: vẫn thắng 9 câu, thua 0 (một câu ra, một câu vào).

## 1. Cách làm

Nguồn danh sách: quét B63 (`data/phase_8_2/k3b/gold_scan/per_case.jsonl`): câu 120 và 5 câu mà mức "loose" (chunk chứa mọi con số và ≥ 60 % từ của quote) khác nhãn ở mốc
B1 — 95, 130, 138 (test), 143, 156 (dev). Với mỗi câu dev: in fact đã nhãn, quote đã nhãn và **mọi** chunk khớp loose trong context B1 / K3b-m (script private
`data/phase_8_2/gold_fix_proposal_2710/tools/c56_inspect.py`), đọc tay, quyết. Khoảng mới cắt **nguyên văn** từ chunk đã đọc, offset tính bằng tìm chuỗi trong file kho (chuỗi
xuất hiện đúng 1 lần). Đề xuất ở `proposal.jsonl` cùng định dạng file nhãn (thêm trường `proposal`), hiệu ứng ở `effect.json` (`tools/c56_build.py`).

## 2. Kết quả

| Câu | Nhóm | Quyết | Khoảng thêm | Ghi chú |
|---|---|---|---:|---|
| 120 | dev | thêm | 2 (2 fact) | hai đoạn khác cùng file nói lại hai fact; 1 chunk khớp loose khác bị loại (trùng từ chung, không phải fact) |
| 156 | dev | thêm | 1 (gắn cho 2 fact dùng chung quote) | đoạn khác cùng file nói lại fact; câu trả lời mốc B1 trích đúng đoạn này, được chấm 5 / 5. **Khác nhận định ban đầu của B61 ("có vẻ báo nhầm")**; 1 chunk khớp loose khác bị loại (giữ chặt) |
| 143 | dev | **không thêm** | 0 | fact nằm ở **tiêu đề mục** của chunk đang có trong context; model thấy tiêu đề (câu trả lời B1 dùng đúng fact, 5 / 5) nhưng hàm đếm chỉ so phần thân đoạn ⇒ lỗi **cách đếm**, không phải nhãn |
| 95, 130, 138 | test | chưa quyết | — | không đọc từng câu (A giao) |

Không câu nào trong phạm vi là "báo nhầm" thuần: 2 chunk khớp loose bị loại, nhưng câu tương ứng vẫn có chunk khác nói đúng fact.

## 3. Hiệu ứng nếu áp đề xuất (chỉ báo cáo, không đổi kết luận nào đã đóng)

| | Trước | Sau |
|---|---:|---:|
| `context_gold_all` B1 (dev 40) | 22 | **23** (câu 156) |
| `context_gold_all` K3b-m L1 / L2 | 31 / 31 | **32 / 32** (câu 120) |
| Thắng ổn định K3b-m | 9 | **9** (156 ra, 120 vào) |
| Thua | 0 | **0** |

Nếu thêm cả luật đếm tiêu đề mục (143), B1 lên 24 — bằng mức loose của B63.

## 4. Cần A / User quyết

- Áp 3 khoảng đề xuất vào file nhãn hay không (file nhãn là dữ liệu đánh giá — người khác kiểm trước khi áp, User duyệt như lần gắn nhãn đầu).
- Hàm đếm có tính **tiêu đề mục** (`heading_path`, model có thấy) không — đổi thước đo tầng tìm, nên ghi trước cho lần đo sau, không áp ngược.
- 3 câu test: cần một session được giao đọc test (hoặc để nguyên, vì test chỉ dùng "không làm hỏng").

## 5. Giới hạn

- Một người đọc (C); 3 câu dev. Mức loose là gợi ý đọc lại, không phải nhãn.
- Không quét những câu mà cả nhãn lẫn loose đều không bắt (đếm thiếu kiểu khác vẫn có thể còn).
