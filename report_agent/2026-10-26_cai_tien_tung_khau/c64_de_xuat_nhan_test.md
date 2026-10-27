# C64 mục 3 — đề xuất nhãn "đoạn đúng" cho 3 câu nhóm kiểm (95, 130, 138)

Người làm: C (Claude Opus 5.5, `hue-rag-86`) · 14:30 27/10/2026 (`date`) · Việc: `session_prompt/CURRENT_HANDOFF.md` → C64 mục 3 (A giao 14:15, được đọc 3 câu kiểm này).
**0 USD**, chỉ đọc + ghi nháp private. **Không sửa** `data/phase_8_1/gold/gold_v2.jsonl` (sha `2f5a347a71ff`, kiểm lại sau khi làm). File này không chép câu hỏi,
đáp án hay nội dung kho — chỉ `case_index`, loại câu, số đếm. Chi tiết (private): `data/phase_8_2/gold_fix_proposal_2710/ghi_chu_c64.md`.

## Cho bạn (3 dòng)

- Ba câu kiểm mà C56 để lại: **1 câu thêm một khoảng nhãn**, **1 câu chỉ cần gắn lại trích dẫn đã có** cho ý so sánh, **1 câu giữ nguyên** (đếm "thiếu" là đúng).
- Nếu áp: số câu kiểm có đủ đoạn đúng trong context ở chatbot context 10 tăng 7 → 9 / 15; ở biến thể "luna chọn 10 đoạn" 10 → 11 / 15.
- Không đổi kết luận nào đã đóng. Áp vào file nhãn hay không: A / User quyết (như C56 → gold v2).

## 1. Cách làm (như C56)

Nguồn danh sách: quét B63 (`data/phase_8_2/k3b/gold_scan/per_case.jsonl`) — ba câu này ở mốc B1 có mức "loose" (chunk chứa mọi con số và ≥ 60 % từ của trích dẫn)
khác nhãn. Với mỗi câu: in fact, trích dẫn đã nhãn, chunk trúng nhãn và **mọi** chunk khớp loose trong context B1 test cho fact bị đếm thiếu, theo **nhãn v2 + luật dòng
tiêu đề** đang dùng (`backend/experiments/phase_8_1/g1_retrieval.py` `GOLD_PATH`, `chunk_hits_quote`); đọc tay, quyết; đối chiếu câu trả lời B1 đã lưu. Khoảng mới cắt
nguyên văn, kiểm xuất hiện đúng 1 lần trong file kho và offset đúng (script `tools/c64_build.py`, từ chối ghi đè).

## 2. Kết quả

| Câu | Loại câu | Quyết | Ghi chú |
|---|---|---|---|
| 95 | so sánh | **không đổi** | một ý không có chunk nào trong context nói thẳng; chunk khớp loose bỏ qua đúng chữ phân biệt ⇒ báo nhầm. Câu trả lời mốc tự suy ra ý đó (đúng, nhưng là suy luận) — giữ nhãn chặt |
| 130 | nhiều nguồn | **thêm 1 khoảng** (1 fact) | một chunk khác cùng file nói lại đúng ý đã nhãn; chunk đó có trong context mốc, khoảng đã nhãn chỉ ở biến thể |
| 138 | so sánh | **gắn thêm 2 trích dẫn đã có** cho ý so sánh | ý "bên nào lớn hơn" chỉ gắn 2 trích dẫn không có trong context, trong khi hai ý số liệu đã có trích dẫn khác (có trong context); một trích dẫn nói thẳng ý so sánh. Không thêm khoảng mới |

## 3. Hiệu ứng nếu áp (chỉ báo cáo)

| `context_gold_all` (test, 15 câu có đoạn đúng) | Trước (v2) | Sau |
|---|---:|---:|
| Mốc B1 (context 10) | 7 | **9** (130, 138) |
| K3b-m (luna chọn 10 / 30) | 10 | **11** (138) |

## 4. Giới hạn

- Một người đọc (C), 3 câu. Mức loose chỉ là gợi ý đọc lại.
- Câu 138: đổi cách gắn trích dẫn của một ý suy ra (so sánh) — nếu A / User muốn quy ước chung "ý so sánh = cần đủ hai ý số liệu", đó là đổi thước (ghi trước cho lần
  đo sau), rộng hơn đề xuất này.
