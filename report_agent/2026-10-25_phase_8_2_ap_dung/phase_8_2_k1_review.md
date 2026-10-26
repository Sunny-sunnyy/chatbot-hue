# Review: Phase 8.2 §10 K1 — pool dense 30 → 100 (report B48)

Decision: **ready_for_user_confirmation** — kết luận **"kém hơn"** của B được xác nhận (0 blocker / 0 major / 1 minor chữ)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 22:02 +0700 (`date`)
Bản được kiểm:
- report `origin/p82-k1:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_implementation.md` (`a7710ed`);
- code `git diff 811d25d..origin/p82-k1` (`k1.py`, +292);
- dữ liệu `data/phase_8_2/k1/`.

Tiêu chí ghi trước: plan `phase_8_2_k1_plan.md` sha `b8f1597f6a0f` (A duyệt, `2c0520c`) §4, §6.

## 1. Phạm vi đã review

- Git: `origin/p82-k1` = `811d25d` + `d50c41f` (harness) + `a7710ed` (report). Diff chỉ thêm 2 file (`k1.py`, report). Không sửa production,
  `g1_retrieval.py`, `b1.py`. Đúng plan §3.
- Đã đọc: report §1–§7, `k1.py` phần tầng tìm (`retrieval`, `compare`, `check_base`, `latency`). Phần tầng trả lời (`generate`, `analyze`,
  `citation_v2`) **chưa chạy** (plan §6.2), nên C chỉ xem chữ ký hàm, không kiểm hành vi.
- Đối chiếu với plan §4: chỉ số quyết, sàn, latency, các dòng theo dõi. Đối chiếu với §6: điều kiện dừng.

## 2. Findings

Không có blocker, không có major.

- **n-1 (minor, chữ):** report §4 "Tầng pool" viết "**Hai** câu tăng một phần: 19 (0,33 → 0,67)", nhưng chỉ nêu một câu. C tính lại thì đúng
  là chỉ có một câu tăng một phần (19). Còn 92 và 113 đều 0,67 → 0,67, khớp nhóm "bốn câu không đổi" mà report đã ghi.
  **Tiêu chí đóng:** sửa "Hai câu" thành "Một câu". Cũng nên ghi ở dòng 2 phần lời thường rằng có thêm câu 67 (ngoài trần) lên đủ.

## 3. Cách người kiểm chạy lại thật (fresh, 0 USD)

Worktree riêng của C, `/tmp/c_r2`, ở `811d25d`, cùng code production với `p82-k1`, vì `k1.py` chỉ là harness. Symlink `data/` +
`knowledge-base-hue/` tạm, đã gỡ. Lệnh: `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -`, gọi đúng
`g1_retrieval.run_config(Namespace(... treatment="dense_bm25_rrf", pool=30|100, rrf_k=60, nfc=False ...))` với tham số như
`k1.retrieval`. Ghi ra `/tmp/c42_{base,k1}.jsonl` (không đụng file của B), so xong thì xóa. Qdrant `:6335` chỉ đọc, e5-small CPU, ~26 s cho cả hai
lượt. Chỉ số tính bằng `full_corpus_eval.paired_stats` + `holm_adjust`.

## 4. Kết quả quan sát

| Kiểm | Kết quả C | Report B | Khớp |
|---|---|---|---|
| Lượt chạy lại so với file của B | `top_chunk_ids`, `dense_chunk_ids`, `top10_gold_all / frac`, `pool_dense_gold_all`: **108 / 108** giống ở cả pool 30 lẫn pool 100; độ dài pool dense 30 / 100 | — | ✓ (tất định, tái lập được) |
| M1 | sha `m1_t1.jsonl` = `cefb2d1ad6094913` | `cefb2d1ad6094913…` | ✓ |
| Chỉ số quyết `top10_gold_all` (dev 40) | +0,025 [−0,050; +0,100], **2 / 37 / 1**, p 0,80; Holm họ 2 = 1,0 | 2 / 37 / 1, CI chứa 0 | ✓ |
| Sàn "0 câu mất" | mất **154** (mốc 1,0 → K1 0,5) | 154 | ✓ ⇒ **phạm sàn** |
| Câu thắng | 22 (trong trần), 67 (ngoài trần) | 22, 67 | ✓ |
| Pool dense đủ đoạn đúng | 31 → **37** / 40; cả 6 câu trần (19, 22, 92, 97, 113, 168) có đủ đoạn đúng trong pool 100 | 31 → 37 | ✓ |
| Top-10 đủ đoạn đúng | 22 → **23** / 40 | 23 / 40 | ✓ |
| Số câu đổi tập top-10 (theo dõi) | **54** / 108 | 54 | ✓ |
| 120 / 168 (theo dõi) | `top10_gold_frac` 0 → 0 cả hai | 0 → 0 | ✓ |
| Latency (`lat_dev.json`, C đọc file, không đo lại) | trung bình chênh +8,88 ms; p95 chênh +48,4 ms; nhiễu base: trung bình −1,8 ms, p95 \|chênh\| 62,8 ms | +8,9 ms | ✓ (≤ +50) |

- **Kết luận theo luật ghi trước:** plan §6.2 "K1 mất ≥ 1 câu ở dev ⇒ kém hơn; không chạy test, không lượt sinh". B làm đúng: dừng sau tầng tìm
  dev, 0 USD. Đo latency sau khi đã phạm sàn là để ghi đủ hồ sơ phương án bị bỏ (`run-experiment` §5), không tốn tiền. Hợp lệ.
- **Nhận định của B "chỗ nghẽn là xếp hạng, không phải vùng ứng viên":** dữ liệu ủng hộ. Pool 100 chứa đủ đoạn đúng ở 37 / 40 câu, nhưng top-10
  chỉ đủ ở 23 / 40. Đây vẫn là *suy ra* từ một biến thể, B đã ghi đúng là suy ra.
- **Ghi chú cho bước sau, không phải finding:** 54 / 108 câu đổi tập top-10. Pool 100 làm xáo context rộng, nên nếu sau này thử "xếp lại trên
  pool 100" thì sàn "0 câu mất" vẫn là rủi ro chính, đúng như ca biên 154.

## 5. Giới hạn

- Code tầng trả lời của `k1.py` chưa chạy, nên C chưa kiểm hành vi. Nếu sau này dùng lại `k1.py` cho lượt sinh thì cần review phần đó.
- Latency: C dùng lại `lat_dev.json` của B, không đo lại. Lý do: phép đo phụ thuộc tải máy (B đã ghi), và K1 đã kém hơn vì phạm sàn, nên latency
  không đổi kết luận.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation:** K1 = **kém hơn**, không đưa vào chatbot, không chạy test hay lượt sinh. Việc mức trung bình ⇒ A đóng, báo User,
ghi `BAO_CAO_TIM_KIEM.md` mục "Đã thử, chưa áp dụng". K3 chạy hay không: A trình User theo §10.2, vì K3 tốn 3–5 s và có phí. n-1 sửa khi tiện.
