# Implementation Report: Phase 8.2 §10 K3 — `gpt-6-luna` xếp lại pool 30 → top-10 — dừng ở L1, phạm sàn (lỗi đầu ra luna)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-31`) · 2026-10-27 09:06 +0700 (`date`) · Việc: B54 (A giao 27/10; User duyệt quyền 08:47 27/10).
Plan A duyệt: `phase_8_2_k3_plan.md` sha **`0a6370204c7d`** (tính từ file trên `main` trước khi chạy). Spec §10 bản `cd910c4c4169`.
Code: nhánh `p82-k3` = `811d25d` + `ff93703` (harness `k3.py`, sha `e58a0a33848f`). **Tiền thật: 0,0251129 USD** (40 lần gọi luna).
Trạng thái: **chờ review** (C).

## Cho bạn — lời thường

1. Mình thử cho chatbot **nhờ model AI xếp lại 30 đoạn tìm được**, rồi lấy 10 đoạn tốt nhất đưa vào câu trả lời. Hiện nay chatbot xếp bằng
   công thức trộn điểm, và nhiều lúc đoạn đúng nằm trong 30 đoạn nhưng không lọt vào 10 đoạn đầu.
2. Có **1 lần trong 40 lần gọi**, model trả danh sách thiếu một đoạn (29 thay vì 30). Theo luật ghi trước, đây là lỗi kỹ thuật, nên mình
   **dừng ngay** và kết luận **kém hơn**. Mình không thử lại và không vá lỗi.
3. Ở 39 lần gọi còn lại, kết quả rất tốt: cả **9 / 9 câu** có thể cứu đều được cứu, và **không câu nào mất** đoạn đúng. Đây chỉ là **một
   lượt**, chưa đo lần hai và chưa chạy nhóm kiểm, nên chưa đủ để kết luận. Nhưng nó cho thấy hướng này đáng làm tiếp, nếu xử lý được lỗi
   thiếu đoạn.
4. Cái giá: mỗi câu **chờ thêm khoảng 5,6 giây** (có lúc 8,6 giây), và tốn thêm khoảng **0,00063 USD** (≈ 16 đồng). Tiền một câu tăng khoảng
   **gấp 4 lần** (mốc ≈ 0,0002 USD / câu). Tiền đã dùng: 0,025 USD (≈ 630 đồng).

## 1. Phạm vi

Làm đúng plan §5 bước 0–2:
- bước 0: M1, M2, lượt `--rerank none` cho dev và test;
- bước 1: pilot L1 10 câu;
- bước 2: L1 phần dev còn lại (30 câu).

Bước 2 vấp lỗi đầu ra luna ở câu cuối (câu dev 173), nên dừng theo plan §6.3. **NOT RUN:** bước 3 (L2 — A/A của luna), bước 4 (test 15),
bước 5 (lượt sinh 176 câu + judge). Không đổi production, không ghi Qdrant, không mở câu kín, không đọc câu test theo từng câu.

## 2. Thay đổi

`backend/experiments/phase_8_2/k3.py` (mới, `ff93703`). Gồm ba lệnh:

- **`retrieval --cases dev|pilot|rest|test --rerank none|luna`**:
  - gọi `service.search` production (pool 30, RRF k 60);
  - lấy 30 đoạn từ `trace.stages["rrf"]` theo thứ tự RRF, payload qua `g1_retrieval.load_payloads`, dựng bằng `build_retrieved_document`;
  - `--rerank luna` gọi nguyên `g4_rerank.luna_rank` (8.1, `LUNA_INSTRUCTIONS`, `store=False`, `max_output_tokens` 2048 từ `settings.yaml`
    ở `811d25d`, không gửi reasoning), rồi lấy 10 đầu;
  - context dựng bằng `build_context_builder` production;
  - chấm `top10_gold_*` / `context_gold_*` / `pool_gold_*` bằng `g1_retrieval.gold_coverage`, `mrr` / `ndcg` bằng `score_retrieval`;
  - **lỗi đầu ra luna đầu tiên ⇒ ghi dòng lỗi rồi dừng lượt**: không gọi lại, không thay bằng thứ tự RRF.
- **`check-base`** (M2) và **`compare`** (luật quyết hai lượt, Holm {K1 p 0,798, K3}).
- **`merge`**.

Mọi lệnh ghi đều từ chối ghi đè (`run-experiment` §3.8).

Khác plan §3:
- **Không import `k1.py`**: nhánh tạo từ `811d25d` không có file này. Hai hàm nhỏ dùng lại (`new_file`, dựng service pool 30) được viết lại
  trong `k3.py`.
- **Chưa viết phần lượt sinh** (bước 5: lớp bọc retrieval, phát lại thứ tự, judge), vì K3 dừng trước bước đó. Không viết code cho bước chưa chạy.

## 3. Cách đã chạy thật

Worktree `/tmp/b_k3` (nhánh `p82-k3`), symlink `data/` + `knowledge-base-hue/` tạm. Từ `/tmp/b_k3/backend`, Qdrant `:6335` chỉ đọc, e5-small CPU:

```bash
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m evaluation.full_corpus_eval retrieval --out …/data/phase_8_2/k3/m1_t1.jsonl   # M1
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.phase_8_2.k3 retrieval --name base_dev --cases dev --rerank none
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.phase_8_2.k3 check-base --name base_dev                            # M2
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.phase_8_2.k3 retrieval --name base_test --cases test --rerank none
# paid, --env-file /home/minhhieu/hue_rag/.env:
… -m experiments.phase_8_2.k3 retrieval --name l1_pilot --cases pilot --rerank luna    # 08:59:29–09:00:28
… -m experiments.phase_8_2.k3 retrieval --name l1_rest  --cases rest  --rerank luna    # 09:00:57–09:03:42, dừng ở câu 173
# số theo dõi 39 câu (private, không thuộc harness):
PYTHONPATH=. uv run --project /home/minhhieu/hue_rag python ../data/phase_8_2/k3/tools/k3_watch.py
```

## 4. Kết quả quan sát

Dữ liệu private `data/phase_8_2/k3/`, sha 12:

| File | sha |
|---|---|
| `m1_t1.jsonl` | `cefb2d1ad609` |
| `base_dev.jsonl` | `e5b1d436aa6b` |
| `base_test.jsonl` | `4621e53ccb08` |
| `l1_pilot.jsonl` | `a0fd67ff7ef2` |
| `l1_rest.jsonl` | `3fefe87bc43b` |
| `tools/k3_watch.py` | `49cdd227b129` |

Mỗi lượt có kèm `.meta.json`.

### 4.1 Mốc (bước 0, 0 USD)

- **M1:** T1 sha `cefb2d1ad609` ✓.
- **M2:** `check-base` 40 / 40 câu, cùng tập câu, **0 trường lệch** (`top_chunk_ids`, `top10_gold_all`, `top10_gold_frac`) so với
  `data/phase_8_2/k1/base_dev.jsonl` ✓.
- **Trần tính lại trên mốc** (W23): dev 22 / 40 đủ đoạn đúng ở top-10, pool đủ ở 31 / 40. Câu có thể thắng là **9**: 17, 38, 48, 67, 70, 85,
  156, 159, 167, đúng danh sách plan §1. Test: 7 / 15 đủ ở top-10, có thể thắng 3 (20, 95, 130). Mốc có context = top-10 ở 40 / 40 câu
  (builder không bỏ đoạn nào).

### 4.2 Pilot (bước 1, 10 câu dev, seed 20261024)

| | Plan ước | Thật | Luật dừng | |
|---|---|---|---|---|
| USD / lần gọi | ≈ 0,0006 | **0,000564** (−6 %) | vượt > 50 % ⇒ dừng | ✓ |
| Ước lại tầng tìm (bước 1–4, 95 lần) | — | ≈ 0,054 | trần con 0,08 (A chốt khi giao) | ✓ |
| `rerank_ms` p50 / p95 | 4–8 s | 5,7 s / 8,2 s | p95 > 15 s ⇒ dừng | ✓ |
| Lỗi đầu ra luna | 0 | 0 / 10 | ≥ 1 ⇒ dừng | ✓ |
| Token ra max | < 2048 | 818 | — | ✓ |

A nhận số pilot lúc 09:0x, cho chạy tiếp.

### 4.3 L1 phần còn lại — lỗi đầu ra luna ⇒ dừng

- 30 / 30 lần gọi xong, **lần cuối (câu dev 173) lỗi**: `order is not a permutation of 1..n`.
  - Luna trả `status: completed`, 401 token ra (không bị cắt ở 2048), nhưng danh sách có **29 số**: thiếu đoạn **5**, không lặp, không số lạ.
  - Ở mốc, câu 173 có đủ đoạn đúng ở top-10.
- **Sàn "lỗi đầu ra luna = 0"** (plan §4, sàn "0 lỗi kỹ thuật" của spec §10.2) bị phạm ⇒ plan §6.3: **dừng, ghi nguyên văn, không gọi lại, không
  thay bằng thứ tự RRF.**
- **Tỉ lệ lỗi quan sát: 1 / 40 = 2,5 %**, CI 95 % Clopper–Pearson **[0,06 %; 13,2 %]**. Nếu đưa nguyên cách này vào chatbot, cứ khoảng 8 đến
  1.600 câu sẽ có 1 câu gặp lỗi. Ước điểm là 1 / 40. Mẫu nhỏ nên khoảng rất rộng. 8.1 G4 (luna xếp 10 đoạn, 30 lần) có 0 / 30 lỗi; danh sách
  30 đoạn dài gấp 3, nên có thể dễ thiếu hơn (*giả thuyết*, chưa đo riêng).

### 4.4 Số theo dõi trên 39 câu L1 hợp lệ — **không dùng để kết luận**

Các số dưới đây chỉ ghi hồ sơ. Đây là một lượt, không có L2 (A/A của luna). Theo plan, "thắng" phải giữ ở cả hai lượt, nên **chỉ số quyết
chưa tính được**. Script `k3_watch.py` in ra:

| Chỉ số | Mốc (RRF) | K3 L1 | Ghi chú |
|---|---:|---:|---|
| Câu đủ đoạn đúng ở top-10 (`top10_gold_all`) | 21 / 39 | **30 / 39** | thắng **9** (17, 38, 48, 67, 70, 85, 156, 159, 167) = **cả 9 câu trần**; thua **0** |
| Câu mất đoạn đúng khỏi top-10 / khỏi context | — | **0 / 0** | không câu nào mất (câu 154 của K1: giữ) |
| `top10_gold_frac` TB | 0,736 | 0,878 | 11 câu tăng / 0 câu giảm |
| MRR@10 (keyword) TB | 0,442 | 0,706 | |
| nDCG TB | 0,514 | 0,744 | |
| Câu đổi tập top-10 | — | 39 / 39 | |
| 120 / 168 (`top10_gold_frac`) | 0 / 0 | 0 / 0,5 | 168 có thêm 1 / 2 fact (theo dõi) |

*Suy ra* (chưa chứng minh): **9 / 0 trên một lượt** cho thấy, ở mốc context 10, chỗ nghẽn "xếp hạng" mà K1 chỉ ra phần lớn gỡ được bằng
listwise rerank. Nếu L2 giữ được 9 / 0, chỉ số quyết qua ngưỡng ≥ 5 / 0 (Holm {K1, K3}) với dư địa lớn. Nhưng luật ghi trước đã quyết "kém
hơn" vì lỗi kỹ thuật, nên kết luận này chưa được dùng.

### 4.5 Tốc độ, tiền (đo thật; khâu tìm)

| | Mốc | K3 (L1) |
|---|---:|---:|
| `rerank_ms` p50 (CI 95 % bootstrap) | 0 | **5.613 ms** [5.369; 6.278] |
| `rerank_ms` p95 (CI) | 0 | **8.565 ms** [7.439; 9.210]; max 9.210 |
| Tìm đầu–cuối p50 / p95 (retrieval + rerank) | 27 / 33 ms | 5.681 / 8.618 ms |
| Token luna / lần: vào TB / ra TB / ra max | — | 4.013 / 453 / 818 |
| USD luna / lần | 0 | **0,000628** |
| USD / câu đầu–cuối (ước, sinh = mốc B1 0,000204) | 0,000204 | ≈ 0,000832 (**≈ 4,1×**) |

- `rerank_ms` đo theo câu, tuần tự (không gọi song song); CI là bootstrap trên 40 lần gọi, seed 20261024.
- p95 ≈ 8,6 s **vượt mức theo dõi 5 s** (spec §10.2: theo dõi, không phải sàn). Plan ước 4–8 s.
- Token ra trung bình 453, lớn hơn ước 350–600 nhưng vẫn trong khoảng; max 818, cách trần 2048 xa.
- Retrieval ms ở lượt luna (p50 32, p95 86) cao hơn lượt mốc (27 / 33). Hai lượt chạy khác lúc, không xen kẽ, nên đây không phải phép đo
  latency khâu tìm theo luật (i). Số này chỉ để biết.
- USD sinh đầu–cuối là **ước** (lượt sinh NOT RUN).

## 5. Kết luận theo tiêu chí ghi trước

- **K3 (luna xếp lại pool 30) — kém hơn (phạm sàn: 1 lỗi đầu ra luna / 40 lần gọi).** Dừng ở L1, đúng plan §6.3.
- **NOT RUN:** L2 (A/A), test 15, lượt sinh, judge. Không có số Completeness, từ chối nhầm hay `output_tokens` của khâu sinh.
- **Không đưa vào chatbot.**
- Hướng mở (B ghi, A / User quyết; *chưa đo*):
  - Số theo dõi 9 / 0 cho thấy hướng rerank listwise trên pool 30 có lợi lớn ở tầng tìm. Đây là tín hiệu mạnh nhất của đợt cải tiến tới giờ.
  - Muốn thử lại thì cần **biến thể mới (K3b), plan mới, review lại**. K3b phải ghi trước cách xử lý khi luna trả danh sách sai, vì đổi luật xử lý
    lỗi sau khi thấy số là biến thể mới (`run-experiment` §4: tối đa 3 vòng; đây là vòng 1). Ví dụ:
    - (1) đoạn bị thiếu xếp cuối theo thứ tự RRF. Đây là một fallback, phải cân nhắc `Session_Prompt.md` §7 và đo tỉ lệ lỗi như một chỉ số;
    - (2) gọi lại một lần. Thêm tiền và độ trễ;
    - (3) chỉ yêu cầu luna trả 10 số đầu thay vì đủ 30. Đổi `LUNA_INSTRUCTIONS`, đầu ra ngắn hơn, có thể nhanh hơn.
  - Kể cả khi K3b thắng, độ trễ +5,6 s (p95 +8,6 s) và tiền ≈ 4× vẫn phải **trình User** (spec §10.2: "tốn hơn" ⇒ User). Theo "chất lượng trước",
    bước sau là tìm cách nhanh / rẻ hơn, ví dụ N nhỏ hơn hoặc reranker local.

## 6. Lỗi và giới hạn

- Chỉ một lượt luna; 9 / 0 là quan sát một lần. Luna không tất định, nên không biết L2 có giữ được không.
- Tỉ lệ lỗi 1 / 40 có CI rất rộng (0,06–13,2 %).
- Đoạn đúng (gold) của 40 câu do agent gắn, agent khác kiểm, User duyệt ~10 câu. Đây là thước tầng tìm duy nhất (spec §10.5).
- Latency đo trên máy User, gọi tuần tự. Production có thể gọi đồng thời, nên số có thể khác.
- Tiền thật lấy từ usage provider trong file kết quả: tổng của 40 lần gọi = 0,0251129 USD (= tổng hai `.meta.json`: 0,0056416 + 0,0194713).

## 7. Bàn giao cho người kiểm (C)

- Đọc `k3.py` (`ff93703`): 30 đoạn lấy từ `stages["rrf"]` theo thứ tự RRF; `luna_rank` gọi nguyên 8.1; dừng ở lỗi đầu tiên; không ghi Qdrant.
- Kiểm lại không tốn tiền:
  - `check-base --name base_dev` (M2);
  - lỗi câu 173 trong `l1_rest.jsonl` (`luna.raw` 29 số, thiếu 5);
  - tiền = tổng `luna.usd`;
  - `k3_watch.py` cho bảng §4.4 / §4.5.
- Không cần chạy lại lượt có phí: kết luận đã chốt bằng một lỗi quan sát được.
