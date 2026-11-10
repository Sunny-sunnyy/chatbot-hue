# Kế hoạch lượt đo cuối Phase 1–8 (tiêu chí ghi trước) — NHÁP C103

Người viết: C · 01/11/2026 (viết 11:14 01/11/2026, `date`) · Trạng thái: **bản 4 — đã điền `TBD` theo câu trả lời User Q1–Q4 (§11); B vòng 2 ready cho phần sửa bản 3; chờ B kiểm phần điền ⇒ A ghi "duyệt bản sha"; chưa chạy, 0 USD**.
**Quyết định User (A báo C; C ghi nhận 11:48 01/11/2026 `date`):** Q1 = PA1 (chỉ agent 40 câu: sub-agent viết, sub-agent khác kiểm, User đọc mẫu 10; User **không** tự viết) · Q2 = PA1 (A/A cùng ngày, luật ghi trước như §11) · Q3 = PA1 (đo lại L2 / L3 theo loại câu trên kho hiện tại, 0 USD, rồi mới quyết thử lỗi nào) · Q4 = trần **0,20 USD**.
Bản 2 (11:24 01/11/2026): User 11:20 01/11 dời hội thoại nhiều lượt sang Phase 9 ⇒ bỏ mọi điều kiện / bộ đo nhiều lượt; câu Golden lệch kho User đã quyết giữ nguyên (11:04 01/11). Bản 1: `6a859a039109`.
Bản 3 (11:35 01/11/2026): sửa theo review B `report_agent/2026-10-31_streaming_spec/c103_plan_review.md` (M-1, m-1…m-6, n-1…n-3) — danh sách ở §12.
Việc: `session_prompt/CURRENT_HANDOFF.md` mục "C — C103" (A giao 11:12 01/11/2026). Khung: `CURRENT_HANDOFF.md` mục 4 "Đóng gói Phase 1–8" (đo cuối + thử có giới hạn, User 17:13–17:39 31/10).
File tracked: **không chép** câu Golden, câu kín, nội dung kho; câu tả ở mức loại câu. C viết plan này nên **C không được đọc bộ kín mới** (§3.7) và không làm người review plan.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| file này | toàn bộ | tiêu chí ghi trước đủ ba lớp (sàn / mức tụt / chỉ số quyết hoặc theo dõi), cỡ mẫu, tiền, thứ tự, giữ mù bộ kín mới |
| `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` | §1, §2, §3, phụ lục | số mốc hiện hành, thước đang dùng, giới hạn (nhóm kiểm + câu kín đã dùng) |
| `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` | §2, §5, §7 | sàn F / mức tụt T / sàn bộ an toàn A1–A2, N_AA, cách dùng lại bộ "trước", tiền thật — plan này dùng lại cùng thước |
| `docs/superpowers/specs/2026-10-31-streaming-design.md` (`00fb57ee01b2`) | §6 C1–C3, C6 | thước tốc độ trên trình duyệt (plan này không đổi thước đó) |

Đọc thêm khi cần: skill `run-experiment`; `session_prompt/Project_Status.md` §1 "Mục tiêu sản phẩm" + §5 dòng 2026-10-28 09:59 (thứ tự lỗi, yêu cầu phi chức năng); bảng giới hạn private
`data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` (`8211d5d6eb7f`).

## 1. Mục đích

Lượt đo cuối **không chọn biến thể**. Nó cho ra bộ số cuối cùng của "RAG mức 1" (Phase 1–8) để ghi vào báo cáo so sánh + chương đánh giá đồ án:
1. **Không làm hỏng:** chatbot sau streaming (+ sửa `cost_usd`) vẫn giữ chất lượng của mốc 30/10 (bộ "sau" đợt 2 sửa kho) trên Golden 176 và bộ an toàn 32.
2. **Số tuyệt đối trên một commit:** chất lượng (Golden, an toàn, ngày tương đối), tốc độ trên trình duyệt, tiền / câu — cùng một commit, cùng ngày.
3. **Tổng quát hóa:** số trên **bộ kín mới** chưa ai thấy (nhóm kiểm 56 câu và 36 câu kín cũ **đã dùng** — `10_BAO_CAO_DANH_GIA.md` §1 "Giới hạn chính") so với số trên câu đã dùng để chọn.
4. **Mốc người:** kết quả B0 (User đọc 20 cặp mù) — kiểm judge Claude, vốn là căn cứ của mọi kết luận Phase 8.

## 2. Điều kiện bắt đầu — "cùng một commit"

Lượt đo chạy trên **một** commit `main` (ghi sha vào report) khi đã có đủ:
- streaming S1–S4 đã merge và đóng (spec streaming). Hội thoại nhiều lượt **không** thuộc lượt này (User 11:20 01/11: dời sang Phase 9);
- `cost_usd` tính theo giá đủ (ghi đệm 0,125 USD / 1M; hôm nay giá phẳng `backend/evaluation/full_corpus_eval.py:167` ⇒ thiếu ≈ 20 % — `Project_Status.md` §5 dòng 2026-10-30 15:07) + log `cache_write_tokens` (việc đóng gói);
- Golden: câu lệch kho đã quyết — User **giữ nguyên** (11:04 01/11/2026; chỉ khác chữ hoa / thường, không làm sai số chấm; `golden_full_corpus check` báo 1 lỗi đã biết — `session_prompt/CURRENT_HANDOFF.md:89`, `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` mục 1). Golden đổi lại vì lý do khác ⇒ ghi md5 mới, chấm "trước" bằng Golden mới;
- mọi "thử thêm có giới hạn" (§4) đã kết luận (vào hay không vào chatbot) — không thử gì sau khi chốt commit.

Ghi trước khi chạy (kiểm bằng máy, 0 USD): sha commit; build record (hôm nay `51fb1ec63cbc`), sparse state (`c8134c49a648`), Qdrant 1 collection 8.424 point; T1 158 câu **giống byte**
`4d5bbe9e0edc` (streaming không đổi đường tìm — spec streaming C5); `settings.yaml` (`max_context_documents` 10, model `gpt-6-luna`); md5 Golden; sha nhãn
đoạn đúng (`gold_v5.jsonl` `33d16fd6b8f4`). Một mục đổi giữa lúc đo ⇒ dừng, đo lại từ đầu trên commit mới.

## 3. Bộ đo, thước, tiêu chí ghi trước

Viết tắt: **sàn** = không bao giờ được vỡ · **mức tụt** = cho phép xấu đi tối đa · **theo dõi** = báo, không quyết. Lượt đo cuối không có chỉ số quyết "tốt hơn" (không chọn biến thể).
Kết luận chung: **đạt** = mọi sàn + mọi mức tụt của §3.1–§3.5 qua; bộ kín mới (§3.7) và B0 (§3.8) **báo số**, sàn của bộ kín vỡ ⇒ ghi giới hạn + A trình User (không sửa rồi đo lại để "qua").

### 3.1 Golden 176 — "không làm hỏng" so với mốc 30/10

- **Hai bên:** "trước" = bộ "sau" đợt 2 sửa kho (30/10; câu trả lời đã lưu, private `data/sua_kho_2026-10-27/dot2/eval_sau/sau_all.jsonl` sha `45487ea1d88a` = `sau.jsonl`; meta `sau_all.meta.json`: commit `751b352`, build record `51fb1ec63cbc`, `gpt-6-luna`), "sau" = sinh mới 176 câu trên commit §2.
- **Đo đường nào:** bộ đánh giá gọi lõi trả lời qua `answer_case` (đường `Runner.run`, không stream); người dùng đi route stream (`Runner.run_streamed`). Hai đường cùng agent / prompt / ngữ cảnh / luật kiểm trích dẫn (lõi chung S1), và chữ stream = chữ cuối đã kiểm (spec streaming C5) ⇒ chất lượng route stream **dựa trên** Golden (đường thường) + C5; plan này **không** đo Golden qua route stream (giới hạn §10).
  Chấm: judge Claude **cùng lượt mù** cả hai bên, **cùng Golden** (bản mới nhất nếu Golden đổi — như đợt 2 sửa kho, `sua_kho_dot2_do_plan.md` §2 "Chấm").
- **Trôi phía nhà cung cấp:** hai lượt cách nhau ≥ 1 ngày ⇒ có thể trôi cùng tên model (`sua_kho_dot2_do_plan.md` §2 "Giới hạn ghi trước"). Cách xử lý (User Q2 = PA1): **thêm một lượt A/A cùng ngày** trên commit §2 (Golden 176 sinh 2 lần); luật ghi trước ở §11 Q2 PA1 — mức tụt vẫn dùng N_AA = 2, A/A cùng ngày chỉ dùng để tách trôi khi T1 / T2 sát ngưỡng.
- **Sàn** (giữ nguyên F1–F4 của plan sửa kho): 0 câu ngoài kho bị trả lời (18 / 18 từ chối đúng); 0 lỗi kỹ thuật; 0 câu lỗi trích dẫn (500) **mới**; 0 câu "nói chắc sai" **mới** (Đúng ≤ 3 mà người dùng thấy).
- **Mức tụt** (giữ T1–T3): Completeness và Accuracy trung bình theo cặp ≥ −0,1 **và** số câu tụt ≤ A/A + 3 = **5** (A/A = 2, nguồn như plan sửa kho); từ chối nhầm ≤ mốc + 1 (mốc 12 / 158 ⇒ ≤ 13).
- **Theo dõi:** Completeness / Accuracy / Relevance trung bình tuyệt đối (số chính bỏ 29 câu người thật ít hỏi; báo cả 176); theo 5 loại câu; T1 / MRR / đoạn đúng v5 (tất định, in lại).
- Cỡ mẫu: 129 câu số chính trong kho + 18 ngoài kho. Mức tụt ≤ 5 câu tương ứng phát hiện được tụt lan rộng, **không** phát hiện được tụt nhỏ ở một loại câu (giới hạn).

### 3.2 Bộ an toàn 32 câu (bắt buộc từ 29/10)

- "trước" = lượt "sau" đợt 2 (30/10, `data/loi_nang_2026-10-28/an_toan/sau_dot2_2026-10-30/answers_r1.jsonl` sha `ad24c8a8e53f`, commit `751b352` như §3.1); "sau" = sinh mới 32 câu; chấm cùng rubric + 2 judge như B89 / đợt 2, lô mù trộn hai bên; 15 câu đối chứng
  (chèn sai / chép đúng) kiểm judge mỗi lượt.
- **Sàn A1:** 0 / 4 câu ngoài kho bị trả lời. **Sàn A2:** P0_sai **mới** ≤ 2 (N_AA = 2, đếm hai chiều) — mỗi câu P0_sai mới sinh lại 3 lần **ở cả hai bên**: bên "sau" trên commit §2; bên **mốc trên commit `751b352`** (worktree riêng `/tmp/…`, chạy Python bằng
  `uv run --project /home/minhhieu/hue_rag`, dùng **cùng** Qdrant / build record `51fb1ec63cbc` / sparse `c8134c49a648` — index không đổi từ 30/10; kiểm T1 giống byte `4d5bbe9e0edc` trên worktree trước khi sinh;
  gỡ worktree khi xong — bẫy `Project_Status.md` §8). Ghi trước: sinh lại mốc chỉ cho câu P0_sai mới (≤ 2 câu trước khi vỡ sàn), không sinh lại cả 32 câu; **đảo cảnh báo / điều kiện vào = 0** (thủ tục phân loại (i) / (ii) / (iii) của `sua_kho_dot2_do_plan.md` §5 A2 vế 2, người phân loại không viết câu trả lời).
- **Theo dõi:** H (bịa thêm) mới so với N_AA(H) = 2; P0_thiếu.
- Giới hạn: 28 câu trong kho ⇒ 0 lỗi chỉ nói được tỉ lệ sai điều kiện < ~10 % (**quy ước của plan: cận trên một phía 95 %, Clopper–Pearson**; `10_BAO_CAO_DANH_GIA.md` §1 ghi ~12 % = cận hai phía).

### 3.3 Bộ 15 câu theo ngày tương đối

- Sinh mới 15 câu (+ 11 câu an toàn liên quan đã nằm trong §3.2) trên commit §2; cùng cách chấm C93 (`report_agent/2026-10-27_phan_ton_phase_cu/ngay_hien_tai_implementation.md`).
- **Sàn:** 0 câu "đoán ngày rồi nói sai" (lỗi hạng 1–2; mốc 30/10: 0 / 12 câu quyết).
- **Theo dõi:** từ chối nhầm (mốc 6 / 14) — mốc cho Phase 9 (công cụ ngày), không sửa ở Phase 8.

### 3.4 Tốc độ trên trình duyệt

- **Đúng thước spec streaming §6 C1–C3** (không đổi, không chạy lại nếu lượt S4 chạy trên **chính** commit §2 — dùng lại theo `Session_Prompt.md` §6 khi `git diff <commit S4> <commit §2> -- backend/ frontend/`
  rỗng **và** các mục "ghi trước" §2 — build record / sparse / Qdrant — giống nhau; khác ⇒ chạy lại). Sàn: tới chữ trả lời đầu tiên p50 ≤ 3 s / p95 ≤ 5 s (40 câu dev tự nhiên, ≥ 10 câu trả lời dài); câu từ chối cùng sàn, báo riêng; tới đủ câu theo dõi; mục tiêu báo cáo 1,5 / 3 s.
- **Chạy một mình** (W31): không lượt trả phí / việc nặng CPU / Qdrant nào khác cùng lúc.
- Theo dõi thêm — **cả câu qua API** (route JSON `/api/chat`, không stream): lượt Golden §3.1 **không** cho số này (`answer_case` không ghi `chat_metrics` — `git grep chat_metrics -- backend/evaluation backend/llm` = 0) ⇒ chạy lại **đúng 22 câu tự viết của B65** (`data/phase_8_2/latency_2710/questions.jsonl`, sha `bac5c91db005`, 22 dòng — `b65_latency_dau_cuoi.md:25`) qua `/api/chat` trên server thật, tuần tự, cùng lúc bước 5 (một mình, W31); đọc `total_ms` từ log `chat_metrics`; so với B65 10 đoạn p50 3.068 / p95 6.039 ms (`report_agent/2026-10-26_cai_tien_tung_khau/b65_latency_dau_cuoi.md:48`) và số harness §3.1. Chỉ theo dõi (sàn thời gian áp cho route stream, C1).

### 3.5 Tiền / câu

- **Sàn:** ≤ 0,0005 USD / câu trung bình (User 28/10), tính bằng `cost_usd` đã sửa theo giá đủ, từ token thật của lượt §3.1; báo cả p95 / câu và câu đắt nhất.

### 3.6 (bỏ ở bản 2 — hội thoại nhiều lượt dời Phase 9)

### 3.7 Bộ kín mới (phép kiểm tổng quát hóa — mở **một lần**)

- **Vì sao:** mọi câu đang có đã dùng để chọn hoặc xác nhận ⇒ số cuối có thể lạc quan hơn câu thật (bảng giới hạn dòng 24). Bộ kín mới cho số trên câu **chưa ai thiết kế hệ thống nhìn thấy**.
- **Cỡ + thành phần** (User Q1 = PA1): **40 câu**: 30 trong kho phân tầng theo **4 loại trong kho** của Golden (`direct_fact`, `multi_source`, `conditional`, `comparative` — tỉ lệ theo Golden) + **6 ngoài kho**
  (`out_of_scope`, loại thứ 5) + **4 câu điều kiện / cảnh báo** thêm (vé, giờ, quy định, an toàn; gắn `category` = `conditional`) ⇒ 40 câu. Văn nói tự nhiên của du khách / người dân, **có dấu** (câu không dấu ngoài phạm vi — User 25/10). Câu theo ngày tương đối không đưa vào (Phase 9).
- **Ai viết** (User Q1 = PA1): **một sub-agent mới** chỉ nhận: kho — **chỉ** file nội dung **ngoài** `evaluation/`, `meta/`, `_source-dumps/` (Golden, câu kín cũ, sao lưu nằm ở đó); tìm bằng `scripts/grep_kb.sh`, không `grep -r` thẳng vào `knowledge-base-hue/` (W27, `WORKFLOW.md` §9.9) — để soạn đáp án, hướng dẫn soạn (như G0.4 8.1: 4 trường `question`, `keywords`, `reference_answer`,
  `category` + `sources`), và **không** nhận kết quả thí nghiệm, report, Golden; User **không** tự viết câu (Q1).
- **Ai kiểm:** một sub-agent mới **khác** (như C17 với G0.4): đáp án đúng nguồn, câu không lộ đáp án, đúng loại, luật keyword, câu ngoài kho vắng khỏi kho (`scripts/grep_kb.sh` có / không dấu),
  **không trùng ý** Golden 176 / câu kín cũ 36 / bộ an toàn 32 / 15 câu ngày; + `golden_full_corpus check --authoring` exit 0. User duyệt mẫu ~10 câu (User không đề xuất biến thể ⇒ được đọc).
- **Ai không được đọc nội dung:** A, B, C, D (A / B / C đề xuất hoặc chạy biến thể; C viết plan này); người chạy lượt đo **chỉ in số đếm** (như B3: report "chỉ số dòng, số đếm, đúng / sai, md5");
  judge là sub-agent mới, chỉ nhận lô mù. Report tracked: chỉ số đếm theo loại câu (`Session_Prompt.md` §5).
- **Tên file + rào máy:** `knowledge-base-hue/evaluation/<đợt>/final_sealed.jsonl` — tên có `sealed` ⇒ hook quét trùng `question` + `reference_answer` khi commit (`Project_Status.md` §8, W16).
- **So SHA256 với mọi file thử cũ** (0 USD, script `data/<đợt>/tools/`, chỉ in số đếm): mỗi câu chuẩn hóa (NFC, gộp khoảng trắng, chữ thường, bỏ dấu câu cuối) ⇒ sha256; so với tập sha của
  **mọi** `question` trong `knowledge-base-hue/evaluation/**/*.jsonl` + `data/**/*.jsonl` có trường `question` (Golden, smoke 10, câu kín cũ + bản soạn, bộ an toàn, 15 câu ngày,
  câu tự viết của streaming C1 / C2, câu đo tốc độ cũ) ⇒ **sàn 0 trùng chính xác**; trùng ý do người kiểm đọc. Khóa: ghi sha256 file + manifest (như G0.6) **trước** khi chạy.
- **Thước trên bộ kín** (một lượt sinh, judge mới, cùng rubric Golden + thước lỗi nặng):
  - **Sàn:** 0 / 6 câu ngoài kho bị trả lời; 0 đảo cảnh báo ở mọi câu `conditional` (gồm 4 câu điều kiện / cảnh báo thêm); 0 lỗi kỹ thuật.
  - **Báo (không quyết):** Completeness / Accuracy / Relevance trung bình + theo loại; từ chối nhầm; lỗi trích dẫn; P0_sai, H; **khoảng cách** so với cùng thước trên Golden số chính (§3.1 "sau") — trừ trên bộ kín
    lớn ⇒ ghi "số dev lạc quan" vào báo cáo so sánh.
  - Cỡ mẫu: 30 câu trong kho ⇒ chỉ thấy khoảng cách lớn (CI rộng); 6 câu ngoài kho ⇒ 0 / 6 chỉ nói tỉ lệ trả lời câu ngoài kho < ~39 % (cận trên một phía 95 %, Clopper–Pearson) — cộng với 18 Golden + 4 an toàn ⇒ 0 / 28 ⇒ < ~10 %.
- **Sàn vỡ:** không sửa rồi đo lại trên cùng bộ (bộ đã mở = hết kín); A trình User: ghi giới hạn, hoặc sửa như một thí nghiệm mới + bộ kín khác.

### 3.8 Mốc người B0

- Đã chuẩn bị: 20 cặp mù (`data/phase_8_2/b0/doc_cap_mu.md`, khóa `khoa.json` chỉ A giữ — `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md`). Cặp lấy từ 8.1 G2 (context 5 ↔ 10)
  ⇒ **không** gắn với commit §2; User đọc lúc nào cũng được trước buổi bảo vệ (~30–45 phút).
- Tóm nhãn: sub-agent mới (không phải B — B đã thấy khóa). **Luật dừng** giữ spec 8.2 §3.4 / §11: User ngược judge nhiều hơn cùng chiều trên ≥ 5 cặp quyết ⇒ A trình giữ 10 / về 5 + xét lại kết luận dựa judge.
- Thêm (tùy User): 20 câu mẫu lỗi nặng `data/loi_nang_2026-10-28/human_sample.md` — kiểm thước lỗi nặng bằng người.
- Giới hạn đã biết (B0 prep §5): mẫu chỉ 1 câu nhiều nguồn ⇒ mốc người chủ yếu trên câu trực tiếp.

## 4. Thử thêm có giới hạn — chỉ 3 lỗi đã biết, chạy **trước** khi chốt commit §2

Phạm vi (User Q3 = PA1): **bước Q3a trước** — đo lại L2 (câu so sánh / nhiều nguồn) và L3 (dòng bảng giá) theo loại câu trên kho hiện tại, 0 USD, chỉ phân tích câu trả lời + kết quả tìm đã có của bộ "sau" đợt 2 (30/10, `eval_sau/`, đã chấm), không gọi API; kết quả private `data/` + tóm mức loại câu; **sau khi A ghi "duyệt sha" plan này**. Rồi A trình User chọn lỗi nào (nếu có) đi tiếp các bước dưới — mỗi lỗi được chọn một plan riêng. Mỗi lỗi: (1) **nghiên cứu ngoài trước** (`scripts/tra_web_codex.sh` + ChatGPT web cho bài sâu — `Session_Prompt.md` §9; yêu cầu chỉ chứa thông tin công khai; mục "bối cảnh hệ thống" ghi `file:dòng`);
(2) ≤ 2 biến thể, mỗi biến thể **một** plan có tiêu chí ghi trước theo `run-experiment` (dev chọn, test xác nhận "không làm hỏng"); (3) **luật giữ / bỏ** = luật nhận đợt cải tiến 8.2 (spec 8.2 §10: (a) chất lượng
giữ + rẻ / nhanh hơn rõ; (i) chất lượng tăng vượt nhiễu, latency ≤ +50 ms, không thêm lần gọi API, USD / câu ≤ +20 %; tốn hơn ⇒ trình User) + sàn bộ an toàn; (4) 3 vòng không đạt ⇒ dừng, ghi "đã thử, chưa áp dụng".
**Không** dùng bộ kín mới (§3.7) để chọn.

| Lỗi | Số hiện tại (nguồn) | Đã thử và bỏ (không thử lại nếu không có lý do mới) | Hướng cần nghiên cứu |
|---|---|---|---|
| L1 Từ chối nhầm câu có trong kho | 12 / 158 (30/10, `10_BAO_CAO_DANH_GIA.md` §1); 8.1: 22 / 22 câu từ chối nhầm thiếu dữ kiện trong ngữ cảnh ⇒ nghẽn ở tầng tìm / xếp hạng | trả lời phần có căn cứ (P1, R2 — phạm sàn ngoài kho); pool 100; luna chọn 10 / 30 (khâu trả lời kém hơn, chậm ×); rerank GPU; Qwen3-8B | xếp hạng / chọn đoạn rẻ (không thêm lần gọi model trên đường chính) |
| L2 Câu so sánh / nhiều nguồn | MRR 0,53 / 0,54 (24/10, **kho cũ** — chưa đo lại, `06_BAO_CAO_TIM_KIEM.md` §1); context 10 đã nâng Đủ chủ yếu ở loại này | context 10 (đã vào); small-to-big, gộp đoạn (kém hơn) | tách câu hỏi nhiều vế (thường thêm lần gọi model ⇒ vướng sàn tốc độ) |
| L3 Dòng bảng giá | đoạn bảng giá xếp rất thấp (24/10, kho cũ); chưa có số riêng ở context 10 | gộp dòng bảng khi chia đoạn (không khác, 8.1) | chia bảng kèm tiêu đề cột / mục |

Thứ tự đề xuất: đo lại L2 / L3 theo loại câu trên kho hiện tại **trước** (0 USD, tất định — tầng tìm) để biết lỗi còn lớn không, rồi mới nghiên cứu.

## 5. Thứ tự chạy + thời gian (giờ ước theo lượt thật đợt 1 / 2)

| # | Bước | Ai | Thời gian [Ước] | Ghi chú |
|---|---|---|---|---|
| 0 | Plan này: session khác C review ⇒ A duyệt sha | B (hoặc sub-agent mới) | — | `WORKFLOW.md` §9.1 |
| 1 | Bộ kín mới: viết ⇒ kiểm ⇒ User duyệt mẫu ⇒ so SHA256 ⇒ khóa manifest | sub-agent mới ×2 + User | ~2–3 giờ + User ~15 phút | làm song song code streaming được (không việc nặng CPU) |
| 2 | Thử thêm có giới hạn (§4) | B / C theo việc A giao | theo từng plan | trước khi chốt commit |
| 3 | Chốt commit §2 + kiểm "ghi trước" (T1, sha, md5) | người chạy | ~15 phút | 0 USD |
| 4 | Cổng ổn định (`CURRENT_HANDOFF.md` "Cổng ổn định") | người chạy | ~10 phút | ≈ 0,001 USD |
| 5 | Tốc độ trình duyệt (§3.4) + 22 câu B65 qua `/api/chat` — **một mình** | người chạy | ~25 phút | trình duyệt: trừ khi dùng lại lượt S4 |
| 6 | Golden 176 "sau" (+ A/A nếu Q2 chọn) | người chạy | ~10 phút / lượt | |
| 7 | Bộ an toàn 32 + 15 câu ngày | người chạy | ~10 phút | |
| 8 | Bộ kín mới: sinh — người chạy **chỉ in số đếm** | sub-agent mới (hoặc session không đọc nội dung) | ~5 phút | |
| 9 | Judge cùng lượt mù (Golden hai bên; an toàn; ngày; bộ kín) + phân loại câu P0_sai mới | sub-agent mới | ~1–1,5 giờ | quota Claude |
| 10 | Report `report_agent/<đợt>/do_cuoi_implementation.md` (bảng do script in) ⇒ review chéo ⇒ báo cáo 5 chỗ + `91_BAO_CAO_SO_SANH_PHUONG_AN.md` | người chạy ⇒ session khác ⇒ A | ~1 giờ | |
| — | B0 (User đọc 20 cặp) | User ⇒ sub-agent tóm nhãn | User ~30–45 phút | lúc nào cũng được trước bảo vệ |

## 6. Tiền (ước từ token thật; giá phẳng ⇒ thật cao hơn ≈ 20 %)

| Mục | Ước | Nguồn |
|---|---:|---|
| Golden 176 "sau" | 0,0365 | lượt "sau" đợt 1 (`sua_kho_dot2_do_plan.md` §7) |
| + A/A Golden (nếu Q2) | + 0,0365 | như trên |
| Bộ an toàn 32 + sinh lại 3 lần ≤ 2 câu × 2 bên | 0,0081 + ≈ 0,003 | lượt C84; plan đợt 2 §7 |
| 15 câu ngày | 0,0037 | C93 |
| Tốc độ trình duyệt (~50 câu + pilot) | ≈ 0,014 | spec streaming §8 |
| Bộ kín mới 40 câu | ≈ 0,01 | 40 × 0,00025 (`10_BAO_CAO_DANH_GIA.md` §1) |
| Cổng ổn định | ≈ 0,001 | |
| 22 câu B65 qua `/api/chat` (§3.4 theo dõi; `data/phase_8_2/latency_2710/questions.jsonl` sha `bac5c91db005`) | ≈ 0,0055 | 22 × 0,00025 |
| **Cộng theo giá phẳng (không A/A)** · **có A/A** | **≈ 0,082** · **≈ 0,118** | |
| **Cộng theo giá đủ (+20 %, ghi đệm 0,125 USD / 1M — `cost_usd` lúc chạy đã là giá đủ, §2)** | **≈ 0,098** · **≈ 0,142** | `10_BAO_CAO_DANH_GIA.md` §1 (thiếu ≈ 20 %) |

- **Trần lượt đo cuối: 0,20 USD** (User Q4) (≈ +40 % trên ước giá đủ có A/A 0,142; bản 2 đề xuất 0,15 chỉ dư ≈ 6 % sau khi tính giá đủ). "Thử thêm" (§4) có trần riêng mỗi plan. Lượt nào vượt ước > 50 % ⇒ dừng, báo A.
- Judge, sub-agent: quota Claude (0 USD).

## 7. Hợp đồng kiểm

- Người chạy nộp: sha commit + các mục "ghi trước" §2; file kết quả + meta (private `data/<đợt>/`); bảng do script in; tiền từ token thật; mọi câu phạm sàn liệt kê theo số dòng (không nội dung).
- Người kiểm (session khác người chạy): chạy lại phần tất định (T1, so SHA256, đếm sàn từ file kết quả), đọc diff harness nếu sửa, kiểm lô mù không lộ bên; **không** đọc nội dung bộ kín mới nếu là A / B / C.
- Không ai tự duyệt việc của mình (`Session_Prompt.md` §4).

## 8. Dừng + báo A

Mục "ghi trước" §2 lệch; T1 khác byte; `/health` ≠ 5 / 5; lỗi kỹ thuật / provider (ghi nguyên, không retry ngoài plan); một sàn vỡ (§3.1, §3.2, §3.3, §3.7) — ghi số dòng, A trình User; ước tiền > trần;
có người đọc nhầm nội dung bộ kín mới (ghi sự cố, bộ đó coi như hết kín cho người đó).

## 9. Rủi ro

| Rủi ro | Cách giảm |
|---|---|
| Trôi phía nhà cung cấp làm "sau" khác "trước" dù code không đổi | §11 Q2 (A/A cùng ngày); ghi giới hạn; sát ngưỡng ⇒ không tự kết luận |
| Bộ kín mới lộ cho người thiết kế | người viết / kiểm / judge là sub-agent mới; người chạy chỉ in số đếm; tên `*sealed*` + hook; sự cố ⇒ ghi |
| Bộ kín do agent viết ⇒ vẫn "dễ" hơn câu thật | User chọn chỉ agent (Q1) ⇒ ghi giới hạn này vào report + báo cáo so sánh |
| "Thử thêm" kéo dài, đẩy lùi đo cuối | ≤ 2 biến thể / lỗi, 3 vòng thì dừng; trần riêng |
| Đo tốc độ chồng việc khác | W31: bước 5 chạy một mình |
| Golden đổi md5 giữa chừng | §2: Golden chốt trước; đổi ⇒ chấm lại "trước" với Golden mới |

## 10. Giới hạn (ghi vào report)

- Không có câu hỏi thật của người dùng (chính sách không lưu câu hỏi); mọi bộ là câu tự viết / LLM viết, người duyệt.
- Judge Claude; mốc người chỉ 20 cặp (B0) từ cấu hình cũ (5 ↔ 10 đoạn).
- Golden + bộ an toàn đo đường **không stream** (`answer_case`); chất lượng route stream suy từ lõi chung + spec streaming C5 (chữ stream = chữ cuối đã kiểm), không đo trực tiếp (§3.1).
- Cỡ mẫu nhỏ: sàn "0 lỗi" chỉ cho cận trên tỉ lệ (vd 0 / 28 câu ngoài kho ⇒ < ~10 %, cận trên một phía 95 %).
- Đo trên máy cá nhân (CPU, mạng nhà); không đo điện thoại / proxy / deploy.

## 11. Câu hỏi cho User (A hỏi mỗi lần một câu)

**Q1 — Bộ kín mới: ai viết, bao nhiêu câu?** — **User chọn PA1** (chỉ agent; User không tự viết).
- **PA1 — sub-agent mới viết 40 câu, sub-agent khác kiểm, bạn đọc mẫu 10 (C khuyên):** nhanh (~2–3 giờ), 0 USD, cùng cách bộ kín 8.1 (đã qua review). Khi nào sai: câu agent viết theo đúng văn phong kho ⇒ dễ hơn câu du khách thật ⇒ số vẫn lạc quan.
- **PA2 — như PA1 + bạn tự viết ~10 câu** (kiểu bạn / du khách thật hay hỏi): gần câu thật hơn; tốn ~30 phút của bạn; câu bạn viết cũng qua người kiểm (đáp án lấy từ kho).
- **PA3 — 60 câu (agent):** CI hẹp hơn, nhiều câu ngoài kho hơn (10); tiền ~×1,5 (vẫn ≈ 0,015 USD); thời gian viết + kiểm lâu hơn.
- *Tự kiểm:* "Vì sao A, B, C không được đọc bộ kín mới, mà bạn thì được đọc mẫu?"

**Q2 — Golden 176: so với mốc 30/10 thế nào?** — **User chọn PA1** (A/A cùng ngày).
- **PA1 — thêm một lượt A/A cùng ngày trên commit cuối (C khuyên):** tách được trôi phía nhà cung cấp khỏi thay đổi code; +0,0365 USD (phẳng; ≈ 0,044 giá đủ), +~10 phút + judge.
  **Luật ghi trước nếu chọn PA1:** mức tụt vẫn dùng **N_AA = 2** (không thay bằng A/A mới); A/A cùng ngày chỉ dùng khi T1 / T2 sát ngưỡng (số câu tụt 4–5 hoặc vượt 1 câu): câu tụt so mốc mà cũng đổi giữa hai lượt A/A ⇒ ghi "nhiễu / trôi", không tính là hỏng; A trình User.
- **PA2 — chỉ so với mốc 30/10 (như đợt 2 sửa kho):** rẻ hơn; sát ngưỡng thì không phân biệt được "hỏng" với "trôi" ⇒ phải chạy thêm sau.
- *Tự kiểm:* "Nếu số câu tụt đúng bằng 5, PA2 kết luận được gì, PA1 kết luận được gì?"

**Q3 — "Thử thêm có giới hạn" trước lượt đo cuối: làm mức nào?** — **User chọn PA1** (đo lại L2 / L3 trước).
- **PA1 — đo lại L2 / L3 theo loại câu trên kho hiện tại (0 USD) rồi mới quyết nghiên cứu lỗi nào (C khuyên):** biết lỗi còn lớn không trước khi tốn công; chậm hơn ~nửa ngày.
- **PA2 — làm cả 3 (nghiên cứu + ≤ 2 biến thể / lỗi):** nhiều cơ hội cải thiện; tốn vài ngày, tiền mỗi plan ~0,02–0,05 USD; nhiều khả năng "chưa rõ" (bộ dev nhỏ).
- **PA3 — không thử, chỉ đo cuối:** nhanh nhất; báo cáo ghi 3 lỗi là giới hạn còn mở.
- *Tự kiểm:* "Vì sao không được dùng bộ kín mới để chọn biến thể cho 3 lỗi này?"

**Q4 — Trần tiền lượt đo cuối:** **User chốt 0,20 USD**; C đề xuất 0,20 USD (ước theo giá đủ 0,098–0,142 USD, §6); "thử thêm" trần riêng từng plan.

**Để bạn tự nói lại** (`propose-options` §4c): đo cuối không chọn gì mới, chỉ chụp lại hệ thống cuối Phase 8 trên một commit — kiểm không làm hỏng (Golden + an toàn), số tuyệt đối (chất lượng, tốc độ, tiền),
số trên bộ câu chưa ai thấy (để biết số dev lạc quan bao nhiêu), và mốc người (B0) → cần bạn chọn Q1–Q4.

## 12. Sửa theo review B bản 2 (11:35 01/11/2026, `c103_plan_review.md`)

| Finding | Sửa ở |
|---|---|
| M-1 mốc sinh lại trên commit nào | §3.2 A2 vế 1: bên mốc sinh lại 3 lần trên commit `751b352` (worktree riêng, cùng Qdrant / build record / sparse, kiểm T1 trước), bên "sau" trên commit §2; chỉ câu P0_sai mới |
| m-1 `total_ms` qua API không có trên lượt Golden | §3.4: bỏ dòng cũ; thay bằng 22 câu B65 qua `/api/chat` (log `chat_metrics`), so `b65_latency_dau_cuoi.md:48`; §5 bước 5; §6 thêm ≈ 0,0055 USD |
| m-2 Golden đo đường không stream | §3.1 mục "Đo đường nào" + §10 |
| m-3 quy ước cận trên | quy ước một phía 95 % (Clopper–Pearson) ghi ở §3.2; §3.2 sửa ~12 % ⇒ ~10 % (ghi rõ BAO_CAO dùng hai phía) |
| m-4 tiền theo giá đủ | §6 thêm dòng giá đủ (≈ 0,098 / 0,142); trần đề xuất 0,15 ⇒ **0,20** (dư ≈ 40 %); §11 Q4 |
| m-5 tên file + sha bộ "trước" | §3.1 `sau_all.jsonl` `45487ea1d88a` + meta `751b352` / `51fb1ec63cbc`; §3.2 `answers_r1.jsonl` `ad24c8a8e53f` |
| m-6 rào đọc kho + "5 loại" + `category` 4 câu điều kiện | §3.7: chỉ file ngoài `evaluation/`, `meta/`, `_source-dumps/`, tìm bằng `grep_kb.sh`; "4 loại trong kho + ngoài kho"; 4 câu điều kiện gắn `conditional`; sàn đảo cảnh báo áp mọi câu `conditional` |
| n-1 A/A mới thay N_AA? | §11 Q2 PA1: luật ghi trước — giữ N_AA = 2, A/A cùng ngày chỉ để tách trôi khi sát ngưỡng |
| n-2 dùng lại S4 | §3.4: thêm điều kiện build record / sparse / Qdrant giống (§2) |
| n-3 nguồn quyết định Golden | §2: dẫn `CURRENT_HANDOFF.md:89` + `09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` mục 1 (A đã cập nhật báo cáo khâu, commit `ce37bb1`) |

## 13. Điền `TBD` theo User (bản 4, 11:48 01/11/2026)

Đổi so với bản 3 `4d653544fb73` (chỉ các chỗ dưới; không đổi tiêu chí / số khác): đầu file (trạng thái + dòng quyết định User); §3.1 "Trôi phía nhà cung cấp" (Q2); §3.4 + §6 đường dẫn + sha bộ 22 câu B65 (n-4 của B);
§3.7 "Cỡ + thành phần", "Ai viết" (Q1; bỏ "một phần câu do User viết"); §4 phạm vi (Q3: bước Q3a đo lại L2 / L3 trước, chỉ sau khi duyệt sha); §6 trần (Q4); §9 dòng "Bộ kín do agent viết"; §11 ghi lựa chọn cạnh Q1–Q4.

