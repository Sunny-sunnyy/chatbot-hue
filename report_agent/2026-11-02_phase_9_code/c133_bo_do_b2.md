# Implementation Report: Phase 9 B2 — bộ đo tầng tìm (C133)

Người làm: C (Claude Opus 5.5) — không code B2
Date: 08:54 03/11/2026 (`date`); sửa 08:57 03/11/2026 theo 2 quyết định A
Mục việc: `CURRENT_HANDOFF.md` "Việc đang mở — phiên 03/11" C133 + 3 quyết định A (tin nhắn sáng 03/11). Spec Phase 9 bản 9 `169c2dd5f86a` §4, §5 B2.
0 USD. Không đụng nhánh `p9-b1`. Mục lục bộ đo (private): `data/phase_9/b2/README.md` `529bad98dae0`.

## 1. Phạm vi

Chốt bộ câu + script chấm tầng tìm cho B2a (V0 / V1 / V3 / V2). Không code biến thể, không chạy khâu trả lời. Mức báo cáo: số đếm, md5, cách chọn — không câu hỏi, không `case_index`.

## 2. Thay đổi chính (mọi file private, `data/phase_9/b2/`)

| File | sha256 (12) | Việc |
|---|---|---|
| `tools/chon_bo_cau.py` | `78649cf48ec4` | chọn 38 câu, 12 câu có thể đổi, dev / test; khoá 4 đầu vào bằng hash |
| `bo_cau_b2.json` | `e5d40678c1aa` | kết quả chọn (chỉ chỉ số + nhãn) |
| `tools/do_tang_tim.py` | `45e35e800500` (trước `019704b06db4`, `04bdba9ea11a`) | `v0` (tìm bằng câu gốc) + `cham` (chấm các lượt biến thể so V0, cổng sàng, xếp hạng; `--nhom dev` cho vòng chỉnh — không tính / in số test) |
| `ket_qua/v0.jsonl` | `a849b1ccad75` | V0 61 câu |
| `ket_qua/tu_kiem.json` (`adc6f5288514`), `doi_chung_khong_goi.jsonl`, `tu_kiem/` | — | 2 ca đối chứng âm + 2 ca dương tổng hợp (dữ liệu giả) |

Script dùng lại hàm sẵn có, không chép: `score_retrieval`, `paired_stats`, `holm_adjust` (`backend/evaluation/full_corpus_eval.py`), `load_gold`, `chunk_hits_quote`
(`backend/experiments/phase_8_1/g1_retrieval.py`), `service.search` của runtime.

## 3. Cách đã chạy thật

```bash
cd backend
uv run python ../data/phase_9/b2/tools/chon_bo_cau.py
HF_HUB_OFFLINE=1 uv run python ../data/phase_9/b2/tools/do_tang_tim.py v0 --out ../data/phase_9/b2/ket_qua/v0.jsonl
HF_HUB_OFFLINE=1 uv run python ../data/phase_9/b2/tools/do_tang_tim.py cham --v0 …/v0.jsonl --bien AA=v0,v0 --bien KHONG_GOI=…,… --out …
```

Qdrant thật (`hue_full_corpus_7a2_e5_small_384`, 8.424 point, chỉ đọc), e5-small CPU, `main` `22068df`. Không có lượt đo latency lúc chạy (B chưa đo).

## 4. Kết quả quan sát

- **Bộ câu (ghi trước):** 38 câu (18 nhiều nguồn + 20 so sánh); 12 câu có thể đổi (6 + 6) — khớp Q3a §4; 32 câu có nhãn v5 (16 + 16); dev 28 / test 10; có thể đổi: dev 9 / test 3.
  md5 danh sách: có thể đổi `b93b90f65ed2`, dev `37407f1a8139`, test `44c9f2bc0793`, câu có nhãn ngoài 38 `758ad4f95b0d` (23 câu).
- **V0:** top-10 trùng T1 (`4d5bbe9e0edc`) **61 / 61**; đủ keyword 26 / 38, 0 / 12.
- **Tự kiểm script** (logic, không phải bằng chứng hệ thống; chạy lại trên bản `04bdba9ea11a` sau lượt đo tốc độ của B): V0 ↔ V0 ⇒ thêm 0 / mất 0 / p Holm 1,0; "không gọi `tim_kho`" ⇒ đủ keyword 0 / 38, mất đoạn đúng 50 / 55 câu có nhãn, test thêm − mất = −7; cả hai không qua cổng — đúng chiều mong đợi.
- **Ca dương tổng hợp (DỮ LIỆU GIẢ để kiểm logic, không phải số đo)**: biến giả chèn đoạn đủ keyword ở 3 câu có thể đổi ⇒ thêm 3 / 12, mất 0, **qua cổng**, đứng đầu xếp hạng; biến giả thứ hai bỏ thêm một đoạn đúng ở 1 câu ngoài 38 ⇒ mất 1 (trong 38: 0) ⇒ **trượt cổng**. Bốn ca chấm chung một lần (`tu_kiem.json` `adc6f5288514`; script tạo `tu_kiem/tao_bien_gia.py` `7958e025af92`).

## 5. Quyết định A (08:57 03/11/2026, ghi trước khi đo) và giới hạn

1. **Luật "thêm ≥ 3 / 12 câu" (spec §5 B2a) và Holm không cùng ngưỡng.** Đo bằng `paired_stats` trên 28 câu dev, k câu thêm, 0 câu mất: k = 3 ⇒ p 0,082 ("không khác"); k = 4 ⇒ 0,025; k = 5 ⇒ 0,009; k = 6 ⇒ 0,002.
   Holm 3 biến ⇒ cần k ≥ 5–6; dev chỉ có 9 câu có thể đổi. **A quyết:** cổng sàng tầng tìm = luật đếm spec (≥ 3 / 12 ở cả hai lượt) + 0 câu mất đoạn đúng + nhóm test thêm − mất ≥ 0;
   Holm chỉ báo số, phá hoà khi xếp hạng (thêm nhiều nhất trước). Lý do: tầng tìm là sàng; cổng chất lượng thật ở khâu trả lời (Completeness 18 câu nhiều nguồn CI 95 % > 0 + sàn §4).
2. **Sàn "0 câu mất đoạn đúng":** chỉ kiểm được trên 32 / 38 câu có nhãn v5; 6 câu không nhãn (đều trong 26 câu đã đủ keyword) chỉ kiểm "mất keyword".
   **A quyết:** vì V1 / V3 / V2 đổi câu tìm của mọi câu, chấm sàn trên **cả 55 câu có nhãn** (32 + 23), báo tách trong / ngoài 38.
3. Nhóm test 10 câu, 3 câu có thể đổi ⇒ "không ngược chiều" là kiểm yếu.
4. Keyword là thước chuỗi con; khâu trả lời (Completeness 18 câu nhiều nguồn) không thuộc bộ này.
5. Hợp đồng đầu vào cho harness B2 (README §4): mỗi lượt một JSONL `{case_index, top_chunk_ids}` đủ 61 câu; V2 ghi `goi_tim_kho: false` khi không gọi, lấy lần gọi đầu.

## 5b. Sửa sau review plan B2 (C135 M-3, A quyết 09:33 03/11/2026)

Thêm `cham --nhom dev`: vòng chỉnh của plan B2 D8 chấm 43 câu dev mà không tính / in / ghi số nhóm test. Tự kiểm (dữ liệu giả + V0): biến giả có 3 câu đổi đều thuộc test ⇒ chế độ dev ra 0 câu thêm, đầu ra 0 chuỗi `test`; chế độ đủ 61 câu ra đúng số cũ. 0 USD.

## 6. Tiền

0 USD (không gọi API).
