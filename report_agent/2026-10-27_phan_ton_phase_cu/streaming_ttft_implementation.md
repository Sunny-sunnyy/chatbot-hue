# Implementation Report: C73 — đo "thời gian tới chữ đầu tiên" khi stream (kết quả)

Người làm: C (Claude Opus 5.5, `hue-rag-32`) · Date: 10:34 28/10/2026 (`date`) · Trạng thái: B review ready 0 / 0 / 1 (`streaming_ttft_review.md`) ⇒ m-1 sửa 11:00 28/10/2026.
Plan: `streaming_ttft_plan.md` bản 2, **A duyệt sha `9683641b6c38`** (giữ D10). Code: nhánh `c70-ttft` `1f70095` (B review ready, vòng 2 0 / 0 / 0).
Chạy: worktree `/tmp/c_ttft` (symlink `data/`, `knowledge-base-hue/`), `main` khi chạy = `249d270` + 2 commit harness; backend production không đổi; context 10.
Chạy sau bộ "trước" B78, không chồng lượt trả phí nào (A cho chạy).

## Cho bạn — lời thường

1. **Thử gì:** cho chatbot gửi câu trả lời **dần từng chữ** (streaming) thay vì đợi viết xong mới gửi, và đo người dùng thấy chữ sớm hơn bao nhiêu. Chỉ đo, chưa đổi
   chatbot.
2. **Kết quả:** với câu trong kho, chữ đầu tiên hiện ra sớm hơn lúc câu trả lời xong khoảng **1,9 giây** (trung vị trên 7 câu, khoảng tin cậy 1,6–4,3 giây) ⇒ đạt dải
   **"rõ"** đã ghi trước (≥ 1,5 s). Tính từ lúc bấm gửi, người dùng thấy chữ đầu sau khoảng **2,4 s** (trung vị; câu chậm ≈ 4,8 s). Nếu đợi toàn bộ như hôm nay thì
   trung vị **≈ 4,6 s** (câu chậm ≈ 7,6 s) — số này là của 8 câu C viết, phần lớn cần trả lời dài. Trên 176 câu Golden (bộ "trước" B78, cùng context 10), đợi toàn bộ chỉ
   **≈ 2,2 s / 4,9 s** ⇒ chờ lâu hay không tùy loại câu; streaming lợi nhiều nhất ở câu trả lời dài (sửa theo review B m-1).
3. **Nếu chỉ cho hiện câu nào đã có nguồn `[n]`** (an toàn hơn, không lộ chữ chưa kiểm), phần lợi còn khoảng **1,0 giây**. Đây là dải "vừa", nhưng khoảng tin cậy
   rất rộng (0,1–3,0 giây) nên chưa chắc.
4. Đường streaming **không làm câu trả lời xong chậm hơn**, và thư viện Agents đang dùng gần như không thêm trễ (≈ 0,08 s lúc bắt đầu, ≈ 0 ở cuối). Cả 30 lần gọi đều
   cho câu trả lời hợp lệ; 2 câu ngoài kho từ chối đúng.
5. **Tiền:** 0,0103 USD (≈ 260 đồng), cao hơn ước 70% vì câu trả lời dài hơn ước. **Giới hạn:** chỉ 10 câu tự viết (7 câu dùng được cho số chính), đo trong script,
   không qua trình duyệt.

## 1. Đã chạy

```bash
cd /tmp/c_ttft/backend   # c70-ttft 1f70095; data/, knowledge-base-hue/ là symlink tới repo chính
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python -m experiments.streaming.ttft run --pilot --name pilot   # 10:2x
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python -m experiments.streaming.ttft run --name main            # 10:31:12–10:33:18
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.streaming.ttft summarize --names main
```

Qdrant `:6335` thật (chỉ đọc), e5-small CPU, `gpt-6-luna` thật, tuần tự. Thứ tự câu (seed `20261028`): q03, q04, q07, q08, q02, q06, q05, q01, q09, q10; mỗi câu chạy
S10 → D10 → N10. Có 1 lần gọi khởi động (N10, câu tự viết khác bộ, không tính).

Dữ liệu private `data/streaming_ttft_2026-10-28/`, sha 12 ký tự:

| File | sha |
|---|---|
| `main.jsonl` | `3003d6517f20` |
| `main.events.jsonl` | `62852c19c182` |
| `main.meta.json` | `be8b3609d42f` |
| `main.summary.json` | `2c9ff82d1d9a` |
| `pilot.jsonl` | `3c465c782922` |
| `questions.jsonl` | `107620cb30f1` |

## 2. Pilot (không gộp số)

Pilot gồm q03 (câu dài) và q09 (ngoài kho), mỗi câu chạy S10 + D10 ⇒ 4 lần gọi, 0 lỗi. Các kiểm của plan §6 đều đạt:
- đủ loại sự kiện (`response.created`, `output_item.done` với `reasoning` và `message`, 549 / 492 / 23 / 23 `output_text.delta`, `response.completed`);
- mọi mốc tính được; delta không có `\u`;
- provider **có** gửi `cached_tokens` (4 / 4, bằng 0);
- 4 / 4 lần gọi `valid`; q09 từ chối đúng.

**Tiền vượt ước.** Pilot 0,001385 USD ⇒ 0,000346 USD / lần, so với ước 0,000204 (**+70 %**). Nguyên nhân: q03 ra 626–732 token, trong đó 124–173 token suy luận. Vượt luật
"> 50 % thì dừng" ⇒ C dừng, báo A. A ước lại ≈ 0,012 USD (thử + thật), vẫn dưới trần 0,03 ⇒ **A duyệt chạy tiếp**.

## 3. Kết quả (bảng do `summarize` in, `main.summary.json`)

**Chỉ số quyết** — S10, câu trong kho có trả lời hợp lệ, n = 7. q02 bị model **từ chối** ở cả ba ô nên không tính.

| Chỉ số | Trung vị ms | CI 95 % (bootstrap trên câu) | p95 | Dải ghi trước |
|---|---:|---|---:|---|
| `gain_visible` = `S_done − S_first_visible` | **1.921,3** | [1.608,2; 4.309,9] | 4.867,0 | **clear** (≥ 1.500 và CI > 0) |
| `gain_cited` = `S_done − S_first_cited_sentence` | **1.014,3** | [144,2; 3.040,8] | 3.978,4 | **moderate** (500–1.500; CI chứa cả 500 lẫn 1.500) |

- `extension_rule_triggered` = **false**: CI của chỉ số quyết `gain_visible` không chứa 500 hay 1.500, và có 7 ≥ 6 câu. Ghi chú: CI của `gain_cited` (chỉ số phụ) chứa cả hai
  ngưỡng; plan §5 chỉ áp luật mở rộng cho chỉ số quyết ⇒ không chạy thêm. Muốn chắc dải của kiểu B thì cần lượt thêm — A quyết (§5).
- `prediction_check` = **within**. Dự đoán ghi trước là ≈ 1,0–1,5 s; đo được 1,9 s, cao hơn vì câu trả lời dài hơn ước (S10: token ra trung vị 232,5, phần chữ hiện ra trung vị
  153 token).

**Theo dõi**

| Chỉ số | Kết quả | Ý nghĩa |
|---|---|---|
| `stream_overhead` = `S_done − N_total` (n 7) | trung vị **−180,5 ms**, CI [−956,9; +1.606,1] | đường stream không làm xong chậm hơn; `overhead_over_300ms` false |
| Chờ tới chữ đầu, đầu–cuối = tìm + context + `S_first_visible` (trong kho, n 8; mọi dòng S10 đều không cache) | p50 **2.441,8 ms**, p95 **4.802,8** | — |
| (tính thêm, script inline) chờ đủ câu hôm nay = tìm + context + `N_total` (trong kho, n 8) | p50 **4.621,9 ms**, p95 **7.649,2** | — |
| Trước chữ đầu, S10 (n 10, cached 0) | sự kiện đầu 652,0 · suy luận xong 2.339,1 · delta đầu 2.339,7 · chữ đầu 2.359,8 ms (trung vị) | ~0,65 s mở luồng + ~1,7 s suy luận rồi mới có chữ |
| Token suy luận S10 | trung vị 79,5 (p95 229,2) | — |
| Lớp Agents SDK so với gọi thẳng (S10 − D10, n 10) | sự kiện đầu **+76,7 ms**, CI [−132,0; +114,5]; đuôi luồng **+1,0 ms** | không đáng kể |
| Ngoài kho (S10) | q09: chữ đầu 1.965, biết là câu từ chối 2.080, xong 2.213 ms; q10: 1.429 / 1.596 / 1.729 | kiểu B với câu từ chối: chỉ hiện được ~0,1 s trước khi xong |
| Mỗi ô (10 dòng) | lỗi 0 / 0 / 0; `valid` 10 / 10 / 10; từ chối trong kho 1 (q02) ở cả ba ô; `first_visible` thiếu 0 | — |
| Cache | S10: 10 / 10 `cached_tokens` = 0; D10: 2 dòng > 0 (q03 2.057, q09 1.174 — cùng prompt với pilot ~10 phút trước); N10: không đo được (n-1) | S10 sạch; D10 / N10 có thể được cache như plan §4 đã ghi |
| USD / lần gọi | S10 0,0002942 · D10 0,0002793 · N10 0,000286 | — |

Tìm + context trung vị 53,8 + 4,4 ms (so với giây thì không đáng kể).

**So với yêu cầu phi chức năng User 28/10** (p50 ≤ 3 s / p95 ≤ 5 s / ≤ 0,0005 USD mỗi câu — theo `CURRENT_HANDOFF.md` commit `249d270`; [S] ước trên 8 câu, p95 của 8 giá trị
≈ giá trị lớn nhất):
- Hôm nay, đợi đủ câu — **tùy loại câu**:
  - 8 câu C (phần lớn trả lời dài; S10 token ra trung vị 232,5): p50 4,6 s / p95 7,6 s ⇒ **không đạt** cả hai;
  - 176 câu Golden (bộ "trước" B78, harness tuần tự, không HTTP, cùng context 10): p50 2,2 s / p95 4,9 s ⇒ **đạt** (theo `CURRENT_HANDOFF.md` mục B81, không phải số của C).
  ⇒ Không nói "hôm nay không đạt" chung chung; câu hỏi cần trả lời dài (kể, so sánh, liệt kê) mới vượt mức (review B m-1).
- Stream, tính tới chữ đầu tiên: p50 2,4 s / p95 4,8 s ⇒ **đạt** cả hai.
- Tiền mỗi câu ≈ 0,00029 USD ⇒ đạt.

## 4. Tiền thật

Token lấy từ usage:
- pilot: 6.474 vào / 1.476 ra = **0,001385 USD**;
- lượt thật (31 lần gọi): 50.301 vào / 7.752 ra = **0,008906 USD**;
- **tổng 0,010291 USD**, trần 0,03.

Ước plan 0,0071 cho 35 lần gọi; thật 35 lần = 0,0103 (+45 % trên cả lượt, +70 % ở pilot) — nguyên nhân như §2. Giá tính đủ cả token cache (cận trên).

## 5. Giới hạn, NOT RUN, câu cho A

- **Cỡ mẫu nhỏ:** 7 câu cho chỉ số quyết; p95 trên 7–10 giá trị ≈ giá trị lớn nhất. Chỉ đủ để nói **cỡ** lợi (giây), không đủ cho số chính xác.
- **q02 (câu hỏi giờ mở cửa) bị từ chối ở cả 3 ô:** model không tìm thấy đủ trong context 10. Đây là quan sát cho đợt sửa kho / tầng tìm, ngoài phạm vi C70.
- **Kiểu B chỉ là ước:** `t_first_cited_sentence` không xử lý `TP.` và chưa thật sự kiểm từng câu. CI 0,1–3,0 s rộng.
- **NOT RUN** (plan §4):
  - context 5;
  - đầu ra văn bản thường thay JSON;
  - kiểu B thật (tách câu + kiểm từng câu);
  - gọi đồng thời;
  - đo qua API / trình duyệt (chưa có route stream);
  - lượt mở rộng 22 câu B65 (luật không kích hoạt).
- **Câu cho A:**
  1. Muốn chắc dải của kiểu B (CI chứa cả 500 lẫn 1.500)? Có thể chạy thêm S10 + N10 trên 22 câu B65, ≈ 0,013 USD theo giá thật. Cần sửa harness để đọc bộ câu đó (B kiểm).
     C khuyên: **không cần trước khi brainstorm spec**. Số "rõ" ở kiểu C / D đã đủ để thấy streaming đáng bàn; dải kiểu B nên đo bằng bản cài thật (tách câu thật) trong spec.
  2. Dọn: worktree `/tmp/c_ttft` (symlink `data/`, `knowledge-base-hue/`) giữ tới khi B review xong (B chạy lại `summarize` ở đó), rồi C gỡ. Nhánh `c70-ttft`: merge vào
     `main` (code thí nghiệm, không chạm runtime) hay giữ làm hồ sơ — A quyết.

## 6. Người kiểm nên chạy lại

Free, từ `/tmp/c_ttft/backend`:
- `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.streaming.ttft summarize --names main` ⇒ trùng §3;
- tính lại `t_first_cited_sentence` của 1–2 dòng bằng `timeline` trên `main.events.jsonl`;
- kiểm `main.meta.json`: commit `1f70095…`, `questions_sha` `107620cb30f1`, 0 lỗi, USD;
- dòng "chờ đủ câu hôm nay" ở §3 là script inline của C (không lưu): tính lại từ `main.jsonl` = `search_ms + context_ms + t_done`, ô N10, `scope == in_kb`.
