# Phase 8.1 G5 — chỉ số quyết theo loại câu (review G5 M1)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 14:14 +0700 (`date`) · Việc: A giao sau review G5 M1 (spec 8.1 §6
tiêu chí 2: "kết quả theo cặp … theo loại câu") · 0 USD, chỉ đọc JSONL đã lưu. Không chép câu Golden.

**Cách tính:** theo cặp trên câu số chính (bỏ `unnatural`, nhãn sha `0b65d1c138d2`); chênh = B − A; thắng/hòa/thua theo câu;
CI 95% bootstrap (10.000, seed 20261024) **chỉ khi n ≥ 10** (A 25/10), còn lại "mô tả". Hàng "tất cả" của G2 **gồm cả 12 / 6
câu out_of_scope** (Completeness của chúng = 5 ở cả hai bên), nên khác số report G2 (+0,261 trên 88 câu trong kho dev; +0,268
trên 41 câu test) — cùng dữ liệu, khác mẫu số. Không có Holm ở đây (bảng mô tả theo nhóm, không phải phép quyết mới).

**Lệnh:** từ `backend/`: `HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g5_by_category` (script
`backend/experiments/phase_8_1/g5_by_category.py`; đọc `data/phase_8_1/g2/` qua `g2_generate.attach_labels` với lượt chấm
`judge/` và `judge_test/`, và `data/phase_8_1/{g3,g4,g4k}/*.jsonl`). Bảng dưới do script in ra, không gõ tay.

**G2.1a context 10 — dev** — chỉ số `completeness`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 44 | 4.886 | 4.886 | +0.000 | 1/42/1 | [-0.068; +0.068] |
| multi_source | 14 | 2.429 | 3.143 | +0.714 | 3/11/0 | [+0.000; +1.571] |
| conditional | 16 | 4.250 | 4.500 | +0.250 | 2/13/1 | [-0.125; +0.812] |
| comparative | 14 | 3.857 | 4.500 | +0.643 | 3/11/0 | [+0.000; +1.500] |
| out_of_scope | 12 | 5.000 | 5.000 | +0.000 | 0/12/0 | [+0.000; +0.000] |
| tất cả | 100 | 4.310 | 4.540 | +0.230 | 9/89/2 | [+0.070; +0.420] |

**G2.1a context 10 — test** — chỉ số `completeness`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 22 | 4.773 | 5.000 | +0.227 | 2/20/0 | [+0.000; +0.636] |
| multi_source | 4 | 4.250 | 4.250 | +0.000 | 0/4/0 | mô tả |
| conditional | 9 | 4.778 | 4.889 | +0.111 | 1/8/0 | mô tả |
| comparative | 6 | 3.167 | 4.000 | +0.833 | 3/2/1 | mô tả |
| out_of_scope | 6 | 5.000 | 5.000 | +0.000 | 0/6/0 | mô tả |
| tất cả | 47 | 4.553 | 4.787 | +0.234 | 6/40/1 | [+0.021; +0.489] |

**G4-A luna listwise vs runtime (dev 30)** — chỉ số `context5_gold_all`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 1 | 0.000 | 0.000 | +0.000 | 0/1/0 | mô tả |
| multi_source | 14 | 0.357 | 0.500 | +0.143 | 2/12/0 | [+0.000; +0.357] |
| conditional | 5 | 0.400 | 0.400 | +0.000 | 0/5/0 | mô tả |
| comparative | 10 | 0.500 | 0.600 | +0.100 | 1/9/0 | [+0.000; +0.300] |
| tất cả | 30 | 0.400 | 0.500 | +0.100 | 3/27/0 | [+0.000; +0.233] |

**G4-A M1 đoạn trơn vs runtime (dev 30)** — chỉ số `context5_gold_all`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 1 | 0.000 | 0.000 | +0.000 | 0/1/0 | mô tả |
| multi_source | 14 | 0.357 | 0.429 | +0.071 | 2/11/1 | [-0.143; +0.286] |
| conditional | 5 | 0.400 | 0.400 | +0.000 | 0/5/0 | mô tả |
| comparative | 10 | 0.500 | 0.600 | +0.100 | 1/9/0 | [+0.000; +0.300] |
| tất cả | 30 | 0.400 | 0.467 | +0.067 | 3/26/1 | [-0.067; +0.200] |

**G4K E khử dấu · native · câu không dấu** — chỉ số `context5_gold_all`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 1 | 0.000 | 0.000 | +0.000 | 0/1/0 | mô tả |
| multi_source | 14 | 0.071 | 0.143 | +0.071 | 1/13/0 | [+0.000; +0.214] |
| conditional | 6 | 0.167 | 0.333 | +0.167 | 1/5/0 | mô tả |
| comparative | 11 | 0.000 | 0.091 | +0.091 | 1/10/0 | [+0.000; +0.273] |
| tất cả | 32 | 0.062 | 0.156 | +0.094 | 3/29/0 | [+0.000; +0.188] |

**G3 H2 512 vs H1 (ngân sách 750)** — chỉ số `ctxB_gold_all`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 1 | 0.000 | 0.000 | +0.000 | 0/1/0 | mô tả |
| multi_source | 14 | 0.286 | 0.071 | -0.214 | 0/11/3 | [-0.429; +0.000] |
| conditional | 6 | 0.500 | 0.333 | -0.167 | 0/5/1 | mô tả |
| comparative | 11 | 0.545 | 0.364 | -0.182 | 0/9/2 | [-0.455; +0.000] |
| tất cả | 32 | 0.406 | 0.219 | -0.188 | 0/26/6 | [-0.312; -0.062] |

**G3 B10: H2 512 vs H1 (ngân sách 1.500)** — chỉ số `ctxB10_gold_all`

| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |
|---|---:|---:|---:|---:|---|---|
| direct_fact | 1 | 0.000 | 0.000 | +0.000 | 0/1/0 | mô tả |
| multi_source | 14 | 0.500 | 0.214 | -0.286 | 0/10/4 | [-0.500; -0.071] |
| conditional | 6 | 0.500 | 0.333 | -0.167 | 0/5/1 | mô tả |
| comparative | 11 | 0.545 | 0.455 | -0.091 | 0/10/1 | [-0.273; +0.000] |
| tất cả | 32 | 0.500 | 0.312 | -0.188 | 0/26/6 | [-0.344; -0.062] |

## Đọc kết quả (quan sát → suy ra)

- **Context 10 (G2.1a):** lợi tập trung ở câu **nhiều nguồn** (dev +0,71, 3/11/0) và **so sánh** (dev +0,64, 3/11/0; test
  +0,83, 3/2/1); câu **trực tiếp** dev không đổi (1/42/1), test +0,23 (2/20/0); câu ngoài phạm vi giữ nguyên 5. *Suy ra*: đúng
  cơ chế "câu cần nhiều đoạn được thêm đoạn"; với từng loại n nhỏ (14 / 4–6), CI chạm 0 — kết luận chung vẫn dựa trên tổng.
- **Đoạn đúng (G3, G4, G4K):** 32 câu có đoạn đúng hầu hết là câu nhiều nguồn (14), so sánh (10–11), có điều kiện (5–6); chỉ
  **1 câu trực tiếp** — vì đoạn đúng được gắn cho câu khó (G0.3). Mọi bảng đoạn đúng vì vậy **không nói được gì về câu trực
  tiếp**.
- **G3 H2 512 / B10:** câu mất đoạn đúng rơi chủ yếu ở **nhiều nguồn** (0/11/3 ở 750; 0/10/4 ở 1.500 — CI dưới 0) ⇒ *suy ra*:
  đoạn to làm hại đúng loại câu cần nhiều đoạn khác nhau.
- **G4 luna / M1, G4K E:** thắng rải đều nhiều nguồn / so sánh / có điều kiện, mỗi loại 1–2 câu — quá ít để tách theo loại.

## Giới hạn

- n mỗi loại nhỏ (4–16 với câu trả lời; 1–14 với đoạn đúng); không dùng bảng này để quyết riêng từng loại.
- Thang loại câu là nhãn `category` của Golden (5 loại), không phải nhãn độ tự nhiên.
