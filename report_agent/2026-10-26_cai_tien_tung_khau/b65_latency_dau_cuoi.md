# B65 — Latency đầu–cuối qua API thật: chatbot đang chạy (context 5) và bản B1 (context 10 + NFC)

Người làm: B (Claude Opus 5.5, `hue-rag-31`) · 2026-10-27 11:44 +0700 (`date`; sửa theo review C57 lúc 11:51 27/10/2026) · Việc: B65 (A giao 27/10; B ghi B70). Đo hiện trạng, không phải biến
thể ⇒ không có plan duyệt (A). **Tiền: ≈ 0,016 USD (ước — API không trả usage token).** Không đổi code, không merge, không ghi Qdrant.

Report không chép câu hỏi: chỉ số đếm, mã câu.

## Cho bạn — lời thường

1. Mình gửi 22 câu tự viết vào chatbot thật qua API, đo thời gian người dùng phải chờ. 20 câu là kiểu du khách / người dân hay hỏi, phủ 5 mảng;
   2 câu ngoài kho.
2. Đo hai bản:
   - bản đang chạy (đưa model 5 đoạn);
   - bản chờ đưa vào sau khi bạn đọc cặp mù (10 đoạn + chuẩn hóa chữ).

   Mỗi bản đo hai cách: hỏi lần lượt từng câu, và 4 câu cùng lúc.
3. **Kết quả:** hai bản chờ gần như bằng nhau: khoảng **3–3,5 giây** (trung vị), **6–6,5 giây** cho câu chậm (p95). Bản 10 đoạn chậm hơn trung bình
   0,1–0,2 giây, nằm trong dao động đo. Không câu nào lỗi; 2 câu ngoài kho đều được từ chối đúng.
4. "Luna chọn 10 đoạn" (thử sáng nay) **thêm một bước chọn đoạn ≈ 4,6–5 giây** (trung vị). Số này đo trực tiếp trong chính lượt đó, cùng 80 câu. Cộng
   vào thời gian chờ qua API hôm nay ⇒ ước người dùng chờ **≈ 8 giây** (trung vị). Đây là *suy ra*, chưa đo qua API.
5. Ngay bản đang chạy, câu chậm (p95) đã mất **5,7–6,2 giây**, vượt mức theo dõi 5 giây mà nhóm đang dùng tạm.

## 1. Cách đo

- **Câu hỏi:** `data/phase_8_2/latency_2710/questions.jsonl` (private, sha `bac5c91db005`).
  - B tự viết 22 câu: mỗi domain 4 câu (foods, heritages, festivals, performing_arts, travel) + 2 câu ngoài kho;
  - có dấu, kiểu người dùng thật;
  - không lấy từ Golden hay câu kín;
  - quét `.githooks/overlap_scan.py`: 0 trùng.
- **Server thật** như cổng ổn định: `HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app`. `/health` 5 / 5 ready trước khi đo.
  - **Bản đang chạy:** `main` `7a4e86c`, context 5, cổng **8013**. A giao 8011, nhưng cổng 8011 đang bị một tiến trình khác trên máy chiếm (không thuộc
    dự án này), B không đụng tới.
  - **Bản B1:** `p82-b1` `811d25d` (context 10 + NFC), worktree `/tmp/b_lat`, cổng 8012, `uv run --project /home/minhhieu/hue_rag`.
- **Client:** `run_latency.py` (sha `88fc07cd7f5f`), `httpx`, `POST /api/chat {"query": …}`.
  - Thời gian đo phía client, từ lúc gửi tới lúc nhận đủ phản hồi.
  - Mỗi lượt có 1 câu khởi động riêng, không tính.
  - Lượt **tuần tự**: 22 câu lần lượt. Lượt **đồng thời 4**: 4 luồng.
  - Thứ tự đo: main tuần tự → main đồng thời → B1 tuần tự → B1 đồng thời (11:39–11:43).
- **Tóm tắt:** `summarize.py` (sha `ba412cc91655`) ⇒ `summary.json` (`ed93fe39f968`). CI 95 % là bootstrap 10.000 lần, seed 20261024. Mỗi CI dùng
  rng riêng (C57 m). Bản đầu dùng chung một rng nên CI phụ thuộc thứ tự tính (`summary_v1_shared_rng.json`); p50 / p95 / TB không đổi, CI lệch ≤ 0,4 s.

## 2. Kết quả

| Bản × cách gọi | Lỗi | p50 ms [CI 95 %] | p95 ms [CI 95 %] | TB ms | Câu trong phạm vi bị từ chối | Ngoài kho từ chối đúng |
|---|---:|---|---|---:|---:|---:|
| Đang chạy (context 5), tuần tự | 0 / 22 | **3.304** [2.419; 4.158] | **5.700** [4.408; 5.797] | 3.375 | 3 / 20 | 2 / 2 |
| Đang chạy, đồng thời 4 | 0 / 22 | **3.568** [2.268; 4.542] | **6.249** [4.646; 6.501] | 3.533 | 5 / 20 | 2 / 2 |
| B1 (context 10 + NFC), tuần tự | 0 / 22 | **3.068** [2.007; 4.564] | **6.039** [5.379; 6.185] | 3.505 | 2 / 20 | 2 / 2 |
| B1, đồng thời 4 | 0 / 22 | **3.410** [2.614; 4.883] | **6.432** [4.923; 7.530] | 3.739 | 1 / 20 | 2 / 2 |

**Chênh theo cặp (cùng câu, B1 − đang chạy):**
- tuần tự: TB **+130 ms**, CI [−318; +565];
- đồng thời 4: TB **+205 ms**, CI [−458; +912].

Cả hai khoảng đều chứa 0 ⇒ **không thấy khác** về thời gian chờ.

- Log server (hai bản): 0 dòng lỗi.
- **Từ chối trong phạm vi** (theo dõi, không phải đánh giá chất lượng; câu tự viết, không có đáp án):
  - đang chạy: 3 câu ở lượt tuần tự, 5 câu ở lượt đồng thời. Cùng câu hỏi mà khác lượt, tức model không tất định;
  - B1: 2 câu và 1 câu.
  - Không kết luận gì về chất lượng từ số này.
- **Bản đang chạy đã vượt mức theo dõi 5 s ở p95:** 5,7 s tuần tự, 6,2 s đồng thời 4. B1 cũng vậy: 6,0 / 6,4 s. Spec §10.2 coi 5 s là mức theo dõi, không
  phải sàn.
- **So với K3b-m — sửa theo C57 (bản đầu trừ chéo hai mốc khác nhau, nên sai).** Bản đầu ghi "K3b-m thêm ≈ 3 s", lấy e2e K3b-m (harness, câu dev) trừ
  số API ở đây (câu tự viết). Phép trừ đó trộn hai cách đo và hai bộ câu.
  - Tách đúng **trong chính lượt K3b-m** (cùng 80 câu gọi rerank mới, cùng harness, gọi đồng thời 4; B tính lại từ `k3b/answer/answer_dev.jsonl`):
    - bước chọn đoạn (`rerank_ms`) p50 **4.620** / p95 6.892 ms;
    - bước sinh p50 1.686 ms (B1 trên cùng câu: 1.646 ms, đo 26/10).
  - ⇒ K3b-m **thêm bước chọn đoạn ≈ 4,6–5 s p50**, đo trực tiếp.
  - Cộng vào thời gian chờ API của bản đang chạy hôm nay (p50 3,3–3,6 s) ⇒ ước **≈ 8 s p50** qua API. Đây là *suy ra*, **chưa đo qua API**.

## 3. Tiền (ước)

API không trả usage token (đã biết: route `/api/chat` không ghi token). Ước theo giá / câu trung bình đã đo thật bằng evaluator:
- context 5 ≈ 0,000133 (8.1 G2.0);
- context 10 ≈ 0,000204 (B1 dev).

Mỗi bản 46 lần gọi (2 × 22 + 2 câu khởi động):
- đang chạy ≈ 0,0061;
- B1 ≈ 0,0094;
- **tổng ≈ 0,0155 USD** (≈ 390 đồng), dưới trần 0,02.

Số thật xem được ở Usage OpenAI, `gpt-6-luna` 11:38–11:44 27/10.

## 4. Giới hạn

- 22 câu / lượt, một lượt mỗi ô ⇒ p95 gần như là câu chậm thứ hai; CI rộng (bảng).
- Đo trên máy User. Latency phụ thuộc lúc gọi OpenAI. Bốn lượt chạy liền nhau trong ~5 phút, không xen kẽ từng câu.
- Từ chối trong phạm vi là đếm máy (`answer == INSUFFICIENT_ANSWER`), không có đáp án tham chiếu.
- Tiền là ước, không phải log.

## 5. File

Private `data/phase_8_2/latency_2710/`, sha 12:

| File | sha |
|---|---|
| `questions.jsonl` | `bac5c91db005` |
| `run_latency.py` | `88fc07cd7f5f` |
| `summarize.py` | `ba412cc91655` |
| `summary.json` | `ed93fe39f968` |
| `main_seq.jsonl` | `3a9fa7c4050f` |
| `main_conc4.jsonl` | `a4f6db1bc0b3` |
| `b1_seq.jsonl` | `8d2dcfd797a3` |
| `b1_conc4.jsonl` | `0ddecf0a9ba6` |

Mỗi lượt có kèm `.meta.json`.
