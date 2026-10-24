# Probe Report: context 5 → 10 chunk (H4) — EXPLORATORY

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Việc: B5 trong `session_prompt/CURRENT_HANDOFF.md`

> **Thăm dò, không phải quyết định Phase 8.** Tôi không chấm điểm câu trả lời và không kết
> luận "tốt hơn". Phần paid chạy trên **22 case được chọn vì đã lỗi** (từ chối nhầm ở Run 1),
> nên kết quả không suy ra được tỉ lệ chung trên 176 case.

## 1. Tiêu chí ghi trước (theo handoff)

1. Free, 158 case trong phạm vi: tỉ lệ keyword mang đáp án có trong context top-5 so với
   top-10, cùng retrieval runtime; tổng và theo category.
2. Paid ≤0,01 USD: sinh lại 22 case từ chối nhầm của Run 1 với `max_context_documents=10`;
   đếm số case còn từ chối, số lỗi citation, mức tăng token input.

## 2. Thay đổi code (`backend/evaluation/full_corpus_eval.py`)

- `build_context_builder(settings, max_documents=None)` và
  `generate --max-context-documents N`: override chỉ trong lệnh, mặc định vẫn theo
  `settings.yaml` (không sửa file này, runtime API không đổi).
- Lệnh `context-coverage --sizes 5 10 --out …` (`context_keyword_coverage`,
  `summarize_context_coverage`): với mỗi cỡ context, đóng gói context từ cùng một kết quả
  retrieval, đếm keyword mang đáp án (`answer_keywords`, B4) nằm trong text đóng gói, kèm
  số token prompt. Không gọi sinh.
- Thêm 1 test logic thuần (tổng 15 passed).

## 3. Cách đã chạy

Chạy từ `backend/`:

```bash
HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval context-coverage --sizes 5 10 \
  --out ../data/evaluation/phase_8_probe/context_coverage_5_10.jsonl
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m evaluation.full_corpus_eval generate --golden full \
  --cases <22 case_index từ chối nhầm Run 1> --max-context-documents 10 \
  --out ../data/evaluation/phase_8_probe/run1_false_refusals_ctx10.jsonl
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_eval.py -q -p no:cacheprovider   # 15 passed
```

Trước phần paid, B dự báo từ số token prompt đo được ở bước 1 (36.981 token cho 22 case):
~0,005 USD.

## 4. Kết quả quan sát

### 4.1 Keyword đáp án trong context, 158 case (free)

Mọi case đóng gói được đủ 5 hoặc đủ 10 source (không chạm giới hạn token).

| Category | n | Tỉ lệ keyword top-5 → top-10 | Case có đủ keyword top-5 → top-10 | Token prompt TB top-5 → top-10 |
|---|---:|---|---|---|
| direct_fact | 75 | 0,940 → 0,973 | 0,933 → 0,973 | 903 → 1.595 |
| conditional | 29 | 0,897 → 0,948 | 0,862 → 0,931 | 868 → 1.499 |
| multi_source | 29 | 0,767 → 0,830 | 0,621 → 0,690 | 965 → 1.708 |
| comparative | 25 | 0,640 → 0,820 | 0,440 → 0,720 | 898 → 1.621 |
| **Tổng** | **158** | **0,853 → 0,918** | **0,785 → 0,873** | **907 → 1.602 (×1,77)** |

Mức tăng lớn nhất ở comparative: số case có đủ keyword tăng từ 44% lên 72%.

### 4.2 Sinh lại 22 case từ chối nhầm với context 10 (paid)

| Mục | Context 5 (Run 1) | Context 10 (probe) |
|---|---:|---:|
| Còn từ chối | 22/22 | **12/22** |
| Lỗi citation | — (từ chối thì không có citation) | 0/22 |
| Lỗi kỹ thuật | 0 | 0 |
| Token input (22 case) | 21.809 | 37.641 (×1,73) |
| Token output (22 case) | 1.927 | 2.376 |

Hết từ chối, theo category: comparative 5/8, multi_source 3/11, direct_fact 1/2,
conditional 1/1.

Hết từ chối, theo nhóm chẩn đoán B4:

| Nhóm B4 (context 5) | Hết từ chối / tổng |
|---|---:|
| Một phần keyword | 7/10 |
| Retrieval miss | 2/8 |
| Đủ keyword (vẫn từ chối ở context 5) | 1/4 |

Hết từ chối, theo việc keyword có tăng khi mở lên top-10 hay không: tăng 7/11, không tăng
3/11.

**Đọc số cẩn thận:**

- "Không còn từ chối" **không có nghĩa là trả lời đúng**. Các câu trả lời này chưa được
  chấm; model có thể trả lời thiếu ý hoặc sai.
- Ở context 5, Run 1 và Run 2 có cùng 22 case từ chối (A kiểm, 0 case đổi). Vì vậy 10 case
  đổi ở đây nhiều khả năng do context, không phải nhiễu sinh. Dù vậy, mỗi case mới chạy một
  lần ở context 10.
- 3/4 case "đủ keyword" vẫn từ chối dù có thêm context. Điều này giữ nguyên câu hỏi về prompt
  "tất cả hoặc không" (H8): mở rộng context không giải quyết được nhóm này.

### 4.3 Tiền

| Bước | Calls | Input | Output | USD |
|---|---:|---:|---:|---:|
| Sinh lại 22 case, context 10 | 22 | 37.641 | 2.376 | **0,00495** (giới hạn 0,01) |

Tổng paid của B trong session: 0,0820 (7B) + 0,0050 = **~0,087 USD**.

## 5. Giới hạn

- Mẫu paid n=22 được chọn theo lỗi. Không suy ra được tỉ lệ từ chối chung hay chất lượng
  chung khi đổi sang context 10. Muốn đo hiệu quả thật phải chạy 176 case và chấm điểm (đo
  trước–sau, Phase 8).
- Keyword là proxy substring (xem B4 §4.3).
- Context 10 làm tăng token input khoảng 1,7–1,8 lần. Ở mức giá hiện tại, phần tăng đó vẫn
  nhỏ: ~0,016 USD cho một run 176 case.
- Không đổi runtime/settings; API vẫn dùng 5 chunk.

## 6. Bàn giao

- Kiểm code: override `max_documents` chỉ đi qua tham số; `settings.yaml` không đổi
  (`git diff backend/config` rỗng).
- Kết quả private: `data/evaluation/phase_8_probe/`.
- Gợi ý cho brainstorm Phase 8 (đề xuất): thử context 10 trên 176 case có chấm điểm, và thử
  tách riêng thay đổi prompt (H8). Mỗi lần chỉ đổi một thứ.
- Không commit (B không có quyền).
