# Báo cáo cho bạn: Sinh câu trả lời, API và giao diện (Phase 6, cải tiến ở Phase 8)

**Cập nhật lần cuối: 17:10 31/10/2026 — bản 14: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này. Người viết: sub-agent của A (bản 14) · Review: agent con ngữ cảnh mới (31/10). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (đúng hiện trạng 31/10/2026)

- **Khâu này làm gì:** chatbot Huế trả lời câu hỏi trên toàn bộ kho (món ăn, di tích, lễ hội, nghệ thuật, du lịch) qua một API và một trang
  web đơn giản. Mỗi ý có trích dẫn `[1]`, `[2]`… trỏ tới đoạn nguồn thật; thiếu thông tin thì trả đúng một câu từ chối cố định, không bịa.
- **Đang chạy cách nào:** chuẩn hóa chữ câu hỏi (NFC — gộp dấu tiếng Việt về một dạng) → tìm đoạn → lấy tối đa **10 đoạn** nguyên vẹn vừa
  ngân sách 16.384 token → `gpt-6-luna` (OpenAI, để mức suy luận mặc định) viết câu trả lời chỉ từ các đoạn đó → backend kiểm từng `[n]` →
  trả câu trả lời + nguồn. Mỗi lần hỏi, API ghi **một dòng số đo** (token, thời gian từng khâu; không ghi nội dung câu hỏi / trả lời, không ghi USD).
  Trang web: JS thuần, một lượt hỏi – đáp, **chữ chưa hiện dần** (streaming đang thiết kế, mục 6).
- **Đo được trên bản đang chạy** (10 đoạn, kho đã sửa hai đợt; 176 câu Golden; 30/10):
  - từ chối nhầm câu có trong kho **12 / 158**; **0** câu ngoài kho bị trả lời; câu sai điều kiện (giờ, vé, cảnh báo) trên bộ 32 câu an toàn: **0**;
  - lỗi trích dẫn (người dùng nhận lỗi 500): **0 / 489** lần sinh, đếm trên mọi lượt đo đã lưu;
  - so với chatbot đầu Phase 8.2 (5 đoạn) trên 33 câu kín: điểm Đủ **+0,82**, Đúng **+0,70** (thang 1–5), 0 câu tụt (28/10);
  - thời gian chờ cả câu: trung vị **2,19 s**, câu chậm (p95) **4,90 s** — đo trong bộ chạy thử, chưa tính đường mạng tới trình duyệt;
  - tiền: **≈ 0,00025 USD / câu** theo bảng giá đủ (bạn dán 30/10); công cụ đo `cost_usd` ghi ~0,00021 vì còn tính giá phẳng ⇒ **thiếu ≈ 20 %**.
  - Điểm Đúng / Đủ / Trúng ý trung bình tuyệt đối chỉ có ở mốc cũ 7B (5 đoạn, 24/10): **4,43 / 4,28 / 4,45**; các lượt đo sau báo chênh theo cặp, không báo lại điểm tuyệt đối.
- **So với yêu cầu bạn chốt 28/10** (trung vị ≤ 3 s, p95 ≤ 5 s cả câu, ≤ 0,0005 USD / câu): Golden **đạt sát** (p95 4,90 s); câu cần trả lời dài **chưa đạt**
  (8 câu tự viết, 28/10: trung vị 4,6 s / p95 7,6 s); tiền **đạt**. Gần hết thời gian chờ là lúc model viết (~98 %).
- **Giới hạn chính:** từ chối nhầm vẫn là chỗ mất điểm lớn nhất (gốc ở khâu tìm: đoạn có đáp án không vào 10 đoạn); câu hỏi theo ngày tương đối
  ("tối nay", "tuần này") bị từ chối dù kho có lịch (6 / 14 câu) — an toàn nhưng chưa trả lời được ⇒ Phase 9; bảng giá và câu tổng hợp nhiều nguồn còn yếu;
  10 đoạn được chọn bằng người chấm Claude, **chưa có mốc người**.
- **Bạn cần quyết (phiên sau, A hỏi):** một câu về mục tiêu "tới chữ đầu tiên" của streaming, rồi duyệt spec streaming (mục 6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
trang web / POST /api/chat {"query": "..."}           (câu hỏi 1–500 ký tự sau khi bỏ khoảng trắng đầu/cuối)
 → chuẩn hóa NFC → tìm đoạn (dense + từ khóa, trộn RRF) → lấy tối đa 10 đoạn nguyên vẹn, vừa ngân sách 16.384 token
 → gpt-6-luna viết câu trả lời, chỉ dùng các đoạn đó, đặt [n] sau mỗi ý (hoặc trả đúng câu từ chối)
 → backend đổi [Nguồn n] về [n], kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources}; lỗi có mã rõ ràng: 422 câu hỏi không hợp lệ · 409 chỉ mục lệch kho · 503 tìm kiếm tạm lỗi · 500 trích dẫn hỏng
 → ghi một dòng chat_metrics (backend/logs/application.log)
```

- Khi khởi động, hệ thống so "dấu vân tay" kho với hồ sơ chỉ mục; kho đổi mà chưa dựng lại chỉ mục thì từ chối chạy.
- Bấm `[n]` trên trang web cuộn tới thẻ nguồn ghi tiêu đề, mục và đoạn trích nguyên văn.
- Code: `backend/api/routes/chat.py` (API; kiểm câu hỏi `:36–38`, route `:60`, kiểm trích dẫn `:177–188`), `backend/retrieval/full_corpus_context.py`
  (chọn đoạn theo ngân sách), `backend/config/settings.yaml:48` (model), `:53` (ngân sách), `:56` (`max_context_documents: 10`),
  `backend/llm/full_corpus_prompt.py:7–16` (prompt), `backend/llm/generator_openai_full_corpus.py` (gọi model), `backend/llm/citations.py:11` (mẫu bắt
  `[n]` và `[Nguồn n]`), `frontend/` (trang web, phục vụ ở `backend/api/app.py:141–146`).

Tự hỏi chatbot (không bắt buộc): bật Docker Desktop, `docker compose up -d qdrant`; từ `backend/` chạy
`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`; mở `http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (phí rất nhỏ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu có đủ bằng chứng → trả lời kèm `[n]` | **Đã xử lý, đóng gói** | mốc 7B (5 đoạn) 4,43 / 4,28 / 4,45; câu kín 28/10 (10 đoạn) Đủ +0,82, Đúng +0,70 so với 5 đoạn |
| Câu ngoài kho → từ chối, không bịa | **Đã xử lý, đóng gói** | 30/10: 0 câu ngoài kho bị trả lời (Golden; bộ an toàn 0 / 4); câu từ chối cố định `full_corpus_prompt.py:3–5,14–15` |
| Kiểm `[n]` trỏ đúng nguồn, lỗi thì trả mã rõ ràng | **Đã xử lý, đóng gói** | nhận cả `[Nguồn n]`, đổi về `[n]` (từ 25/10); bản đang chạy 0 / 489 lần sinh lỗi; dạng lỗi còn thấy ở bản cũ chỉ là "không gắn `[n]` nào"; `citations.py:11`, `chat.py:177–188` |
| Trang web bấm `[n]` tới thẻ nguồn | **Đã xử lý, đóng gói** | `frontend/`; `api/app.py:141–146` |
| Kho lệch chỉ mục → từ chối khởi động | **Đã xử lý, đóng gói** | API báo 409 "cần lập chỉ mục lại"; `retrieval/full_corpus.py:383–385`; test `test_api_chat.py` |
| Qdrant / model tìm kiếm lỗi → báo lỗi tạm | **Đã xử lý, đóng gói** | 503 `retrieval_unavailable` (`chat.py:96–119`); test `test_startup_model_missing.py` (bạn chạy `!`) |
| Đưa 10 đoạn thay vì 5 + chuẩn hóa NFC | **Đã xử lý, đóng gói** (từ 28/10) — chưa có mốc người | 8.1: Đủ +0,26 (thử) / +0,27 (kiểm); câu kín +0,82; trung vị / p95 2,19 / 4,90 s. Đổi ngược về 5: sửa `settings.yaml:56` **và** chốt kiểm ở `core/settings_loader.py:75` (đang ép đúng 10) |
| Câu có một vế có bằng chứng, vế kia thiếu | **Đã thử, chưa áp dụng** | prompt bắt từ chối cả câu (`full_corpus_prompt.py:14`). Hai lần thử "trả lời phần có căn cứ" đều trả lời câu ngoài kho ⇒ gác; luật kiểm sau sinh không cứu được (mục 4) |
| Đoạn chứa đáp án nằm ngoài các đoạn đưa model | **Xử lý một phần** | mọi câu từ chối nhầm đo ở 8.1 đều thiếu ít nhất một đoạn đúng — gốc ở khâu tìm; 10 đoạn giảm gần một nửa; phần còn lại: `BAO_CAO_TIM_KIEM.md` |
| Mức suy luận của model | **Đã thử, chưa áp dụng** | giữ mặc định (không gửi tham số: `generator_openai_full_corpus.py:98–99,120`); `none` kém hơn (trả lời vòng câu lẽ ra từ chối), lợi tiền chỉ 3–6 % (mục 4) |
| Câu trả lời quá gọn, bỏ chi tiết có trong nguồn | **Chưa thực hiện** | 26/10: 9 / 88 câu mất điểm vì bỏ chi tiết; thử "nêu đủ chi tiết" không chạy được (chỉ 6 câu đổi được, quá ít để kết luận) |
| Câu trả lời ghi sai con số (giá, giờ, năm) | **Xử lý một phần** (đo được, chưa có rào chặn) | 27/10, 10 đoạn: 0 / 68 câu có số bị thấy sai; chưa đo sai về chữ (tên, sự kiện) |
| Kiểm bằng code sau khi sinh để chặn "trả lời vòng" | **Đã thử, chưa áp dụng** | 7 / 10 câu bị cờ là câu có ích ⇒ gác |
| Để model chọn 10 / 30 đoạn trước khi trả lời | **Đã thử, chưa áp dụng** | trung bình tốt lên nhưng 5 câu tụt > 4 cho phép; chờ ~6,5 s, tiền ×3,8 (mục 4) |
| Xếp đoạn gom theo tài liệu; 2 luật cũ của prompt Phase 6; "một nguồn thì gán nguồn đó" | **Đã thử, chưa áp dụng** | 8.1: không khác (mục 4) |
| Câu tổng hợp nhiều nguồn | **Xử lý một phần** | lúc đóng Phase 6 chỉ dùng 1 nguồn; 8.1: lợi của 10 đoạn nằm nhiều ở câu nhiều nguồn / so sánh; chưa có phép đo riêng "tổng hợp đúng" |
| Câu hỏi giá vé + miễn giảm (bảng giá) | **Đã thử, chưa áp dụng** | không tìm ra dòng bảng giá; 8.1 thử gộp dòng bảng khi chia đoạn: không khác (`BAO_CAO_TIM_KIEM.md`); chưa đo lại riêng ở 10 đoạn |
| Tách câu hỏi hai ý | **Chưa thực hiện** | Phase 8 không làm; giả thuyết xếp "cân nhắc cho Phase 9" (`reports/phase_8_candidate_hypotheses_2026_10_24.md:68`) |
| Câu hỏi theo ngày tương đối ("tối nay", "tháng sau") | **Xử lý một phần** (an toàn; chưa trả lời được) — Phase 9 | 30/10: 0 câu đoán ngày rồi nói sai; 6 / 14 câu có trong kho bị từ chối (4 câu có lịch ngay trong đoạn model đọc). Prompt không có ngày hôm nay (`full_corpus_prompt.py:7–16`) |
| Hiện chữ dần (streaming) | **Chưa thực hiện** — đang thiết kế | spec bản 4 review đạt; bạn chốt 3 câu (31/10); còn 1 câu + duyệt spec ⇒ mới code (mục 6) |
| Hội thoại nhiều lượt | **Chưa thực hiện** | có nháp phương án (private); làm spec **sau** streaming (cùng sửa API + trang web) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (mới ở trên)

Mỗi dòng: thử gì · kết quả · giữ / bỏ vì sao · hồ sơ. Mọi thí nghiệm có luật ghi trước khi chạy và người khác kiểm lại.

### 30/10/2026
- **Câu hỏi theo ngày tương đối** (15 câu tự viết + 11 câu bộ an toàn, 2 người chấm Claude không biết ngày chạy; 0,0037 USD): 0 câu tự đoán ngày rồi nói chắc,
  0 câu tính sai thứ / âm lịch; nhưng 6 / 14 câu có trong kho bị từ chối, cùng thông tin hỏi không kèm ngày thì trả lời đúng. **Bạn quyết (14:44):** không sửa prompt ở
  Phase 8; Phase 9 thêm công cụ "hôm nay là ngày nào", bộ câu này làm mốc. `report_agent/2026-10-27_phan_ton_phase_cu/ngay_hien_tai_implementation.md`.
- **Đếm lại lỗi trích dẫn** trên mọi lượt đo đã lưu (0 USD): bản đang chạy 0 / 489 lần sinh; bản 5 đoạn cũ 2 / 528. Lỗi còn lại chỉ là câu không gắn `[n]` nào, chỉ
  biết khi câu đã viết xong ⇒ căn cứ cho streaming "hiện chữ trước, kiểm cuối". `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §8.2.
- **Giá đủ của `gpt-6-luna`:** mỗi câu bị tính giá **ghi đệm** cho gần hết phần đọc vào, không được giảm giá đọc đệm ⇒ tiền thật ≈ 0,00025 USD / câu, công cụ đo ghi
  thiếu ≈ 20 %; mọi số USD cũ trong báo cáo này đếm theo giá phẳng. Sửa công thức: việc đóng gói Phase 1–8. `Project_Status.md` §5 (30/10 15:07).

### 28/10/2026
- **Đưa 10 đoạn + chuẩn hóa NFC vào chatbot** (merge `510e1a8`): bạn chọn đưa vào theo người chấm Claude, đọc cặp mù làm sau. Kiểm trên `main`: 51 test đạt, kết quả
  tìm 158 câu giống từng byte, câu gõ dấu tách rời cho đúng ngữ cảnh như câu thường, chạy thật 2 câu đạt (≈ 0,0004 USD). **Giữ.**
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_merge_implementation.md`.
- **Đo thử "chữ đầu tiên" nếu có streaming** (đo trong script, chưa trên trình duyệt; 7–8 câu tự viết, phần lớn trả lời dài): chữ đầu hiện sớm hơn lúc xong câu
  ~**1,9 s** (trung vị); tới chữ đầu p50 2,4 / p95 4,8 s, so với chờ đủ câu 4,6 / 7,6 s ⇒ lý do làm streaming.
  `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_implementation.md`.

### 27/10/2026
- **Thời gian chờ thật qua API** (22 câu tự viết, bản 5 đoạn lúc đó): trung vị 3,3 s / p95 5,7 s tuần tự; ~98 % là lúc model viết (tăng theo số chữ model viết ra: ≈ 11,5 ms mỗi token, tương quan 0,97 — `report_agent/2026-10-26_cai_tien_tung_khau/c58_latency_theo_khau.md`), tìm ~40 ms, dựng ngữ cảnh ~2 ms;
  thời gian viết đi theo số token viết ra. Số này của cấu hình cũ — số hiện hành ở mục 1. `report_agent/2026-10-26_cai_tien_tung_khau/b65_latency_dau_cuoi.md`, `c58_latency_theo_khau.md`.
- **API ghi số đo mỗi câu** (bạn duyệt; merge `5100b90`): một dòng log mỗi lần hỏi, không chứa câu hỏi. **Giữ.** `report_agent/2026-10-26_cai_tien_tung_khau/c59_log_token_implementation.md`.
- **Trả lời ngay, không suy luận** (mốc 10 đoạn): một câu lẽ ra phải từ chối bị trả lời vòng ⇒ phạm sàn, dừng ở 24 câu (0,0049 USD); lợi nhỏ (token viết ra ~0,72×,
  tiền ~0,94–0,97×). **Bỏ.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md`.
- **Model chọn 10 / 30 đoạn rồi mới trả lời** (120 câu thử): đủ ý +0,22, đúng +0,25 trung bình, từ chối nhầm 7 → 2 / 88, nhưng **5 câu đủ ý tụt** > 4 cho phép ⇒ kém
  hơn theo luật; chờ p50 6,5 / p95 9,1 s, tiền ×3,8 (0,0749 USD). **Bỏ.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_m_answer_review.md`.
- **Sai số liệu trong câu trả lời** (đo hiện trạng, 0 USD): 0 / 68 câu có số bị thấy sai (máy nghi 4 câu, đều là phép tính đúng). Không cần rào chặn lúc này.
  `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md`.
- **Luật kiểm sau sinh chặn "trả lời vòng"** (0 USD): không tách được câu lạc đề với câu trả lời một phần có ích (7 / 10 cờ là câu có ích). **Bỏ.**
  `report_agent/2026-10-26_cai_tien_tung_khau/c51_kiem_sau_sinh_kha_thi.md`.
- Bạn chốt đợt cải tiến từng khâu: không cách nào vào chatbot. Tổng hợp: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.

### 26/10/2026
- **Phân loại lỗi** (88 câu, mốc 10 đoạn): 10 câu kém đều thiếu thông tin trong 10 đoạn; model không bịa. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md`.
- **Trả lời phần có căn cứ, chữ prompt siết hơn:** vẫn trả lời 1 / 12 câu ngoài kho ⇒ dừng ngay bước đầu (0,0027 USD). **Bỏ.**
- **Nêu đủ chi tiết:** không chạy (chỉ 6 câu đổi được). **Thước kiểm số liệu có trong nguồn:** chỉ dùng chọn câu đọc lại. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r3_plan.md`, `phase_8_2_r4_implementation.md`.

### 25/10/2026
- **API báo đúng loại lỗi** (rà code): một module bị nạp hai lần làm Qdrant lỗi ra 500 thay 503, kho đổi ra 503 thay 409 ⇒ sửa về một cách import, chạy mọi lệnh từ
  `backend/`. **PASS.** `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`.
- **Lỗi trích dẫn `[Nguồn n]`:** model đôi khi trích đúng nhãn ngữ cảnh "[Nguồn n]", bộ kiểm chỉ hiểu "[n]" ⇒ người dùng nhận 500. Sửa: nhận cả hai dạng, đổi về `[n]`.
  Trên 1.600 câu đã sinh: lỗi 69 → 14, 0 câu đạt bị đổi. **PASS, giữ.** Số "lỗi trích dẫn" trước ngày này đếm theo bộ kiểm cũ.
- **Phase 8.1 — thử 5 cách trả lời** (120 câu thử, chấm mù bằng Claude, so theo cặp; "tốt hơn" phải xác nhận trên 56 câu kiểm; 0,157 USD):

  | Cách | Điểm Đủ (thử) | Rào chắn | Kết luận |
  |---|---|---|---|
  | **10 đoạn ngữ cảnh** | **+0,26** | đạt; tiền ×1,5 | **tốt hơn**, bộ kiểm +0,27 ⇒ **đã đưa vào 28/10** |
  | Xếp 5 đoạn gom theo tài liệu | −0,02 | đạt | không khác ⇒ bỏ |
  | Prompt "trả lời phần có căn cứ" | +0,11 | trả lời 2 câu ngoài kho | kém hơn ⇒ bỏ |
  | Prompt thêm 2 luật cũ | 0,00 | đạt | không khác ⇒ bỏ |
  | Mức suy luận `none` / `low` / `high` | +0,14 / +0,02 / +0,02 | `none`, `low`: lỗi trích dẫn tăng (đếm theo bộ kiểm cũ) | không dùng; `none` thử lại 27/10 vẫn kém |
  | "Một nguồn thì gán nguồn đó" | — | — | 0 câu đổi ⇒ bỏ |

  Đính chính: chẩn đoán 7B "4 / 22 câu có đủ bằng chứng mà vẫn từ chối" (theo từ khóa) — đo bằng đoạn đúng thì **0 câu**. `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`.

### 24/10/2026 và trước
- **Phase 7B — mốc 176 câu** (5 đoạn): Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45; từ chối đúng 18 / 18 câu ngoài kho; từ chối nhầm 22 / 158; lỗi trích dẫn 4 / 176
  (bộ kiểm cũ); ~0,024 USD. `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`.
- **Dọn code sau Phase 7:** gỡ đường sinh câu trả lời bản món ăn (đã hỏng: gửi `temperature` ⇒ lỗi 400) cùng code / test món ăn; đường toàn kho không đổi.
  `reports/phase_7_cleanup_inventory_2026_10_24.md`.
- **23/10 — đóng Phase 6 trên `gpt-6-luna`:** 5 câu thật, 4 đạt / 1 không (câu giá vé + miễn giảm: không tìm ra bảng giá); câu nhiều nguồn đạt nhưng chỉ dùng 1 nguồn.
- **Đổi model sinh:** Qwen 3.5-9B (OpenRouter) → `gpt-5.4-nano` → `gpt-6-luna` (23/10). Hai model đầu **đã bỏ**.
  `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`.

## 5. Hôm nay còn đúng không

Kiểm với code `main` (`1985a81`) lúc 17:10 31/10/2026 và `session_prompt/Project_Status.md` §4.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| API `POST /api/chat`, trả `{answer, sources}`, câu hỏi 1–500 ký tự | **còn dùng** | `backend/api/routes/chat.py:36–38,48–50,60` |
| Model sinh `gpt-6-luna`, không gửi mức suy luận | **còn dùng** | `settings.yaml:48`; `generator_openai_full_corpus.py:98–99,120` |
| Tối đa 10 đoạn, ngân sách 16.384 token (thay 5 đoạn từ 28/10) | **còn dùng** — chưa có mốc người | `settings.yaml:53,56`; `core/settings_loader.py:69–76` |
| Chuẩn hóa NFC câu hỏi trước khi tìm | **còn dùng** (từ 28/10) | `backend/retrieval/full_corpus.py:97–102` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng** | `full_corpus_prompt.py:14` |
| Kiểm trích dẫn nhận cả `[n]` và `[Nguồn n]` | **còn dùng** (từ 25/10) | `citations.py:11–16`; `chat.py:177–188` |
| Ghi `chat_metrics` mỗi câu, không ghi nội dung, không ghi USD | **còn dùng** (từ 27/10) | `chat.py:24–29,60–84` |
| Từ chối khởi động khi kho lệch chỉ mục | **còn dùng** | `retrieval/full_corpus.py:383–385` |
| Chỉ mục đang dùng | **còn dùng**: `hue_full_corpus_7a2_e5_small_384`, 8.424 đoạn (dựng lại 30/10), Qdrant cổng 6335 | `Project_Status.md` §4; `settings.yaml:38` |
| `cost_usd` của công cụ đo | **ghi thiếu ≈ 20 %** (giá phẳng, chưa tính ghi đệm) — sửa ở đóng gói | `backend/evaluation/full_corpus_eval.py:167` |
| Chẩn đoán 7B "4 / 22 câu đủ bằng chứng vẫn từ chối" | **đã thay** bởi số đo theo đoạn đúng của 8.1: 0 / 22 | `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` |
| "Representation B" (LLM viết thêm ngữ cảnh cho đoạn) | **đã gỡ** 26/10 | commit `c6e130c` |

## 6. Việc còn lại / cần quyết

- **Streaming — đang thiết kế, chưa code.** Bạn đã chốt (31/10): chữ hiện ngay khi model viết + báo tiến độ, kiểm trích dẫn ở cuối như hôm nay; sàn trung vị ≤ 3 s /
  p95 ≤ 5 s đổi sang "tới chữ trả lời đầu tiên hiện trên trình duyệt" (tới lúc streaming chạy, sàn vẫn áp cho cả câu); kiểm cuối hỏng ⇒ rút lại chữ đã hiện, lỗi / đứt
  giữa chừng ⇒ xoá hết, kèm lời báo + nút "Thử lại". **Còn:** một câu về mục tiêu báo cáo cho "chữ đầu tiên" (A khuyên giữ sàn 3 / 5 s, báo thêm mục tiêu 1,5 / 3 s) +
  bạn duyệt spec ⇒ code. Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md`; đợt: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
- **Hội thoại nhiều lượt:** spec sau streaming (nháp: trình duyệt giữ lịch sử, server không lưu).
- **Đóng gói Phase 1–8:** sửa `cost_usd` theo giá đủ + ghi số token ghi đệm; bảng giới hạn đã biết; bộ câu kín mới trước buổi bảo vệ.
- **Khi bạn rảnh:** đọc cặp mù (20 cặp, ~30–45 phút) làm mốc người cho 10 đoạn; nếu bạn ngược người chấm Claude nhiều ⇒ A trình giữ 10 hay về 5.
- **Phase 9:** công cụ "hôm nay là ngày nào" cho câu theo ngày tương đối; tách câu hỏi hai ý là ứng viên.
- **Còn mở, không gấp:** câu trả lời quá gọn (cần thêm câu tự nhiên để đo); bảng giá và câu nhiều nguồn (gốc ở khâu tìm); sai về chữ (tên, sự kiện) chưa có cách đo rẻ.
- Hướng đã gác (chỉ mở lại khi có ý mới đã kiểm trước): trả lời phần có căn cứ; trả lời không suy luận; luật kiểm sau sinh; model chọn 10 / 30 đoạn.

## Phụ lục — hồ sơ kỹ thuật

- **Mã việc ở mục 4:** ngày tương đối = C93 (plan B96); đếm lại trích dẫn = C89; giá đủ = B95; 10 đoạn + NFC = Phase 8.2 B1 (nhánh `p82-b1` `c3d5607`, spec 8.2 §11 "PA3"
  — đưa vào không chờ B0, commit `d922bf7`); đo chữ đầu = probe TTFT; latency 27/10 = B65 / C58; log số đo = C59 / C60 (review B70); không suy luận = **R1**
  (plan sha `8e76e77e0448`, nhánh `p82-r1` `63a472f`); model chọn đoạn = **K3b-m** khâu trả lời (plan bản 3 sha `2a3b22b38ab6`, nhánh `p82-k3b` `a6f609c`, review C54;
  5 câu tụt theo chỉ số T3); sai số liệu = C48; luật kiểm sau sinh = C51; phân loại lỗi = C36; trả lời một phần = **R2** (nhánh `p82-r2`) / H8; nêu đủ chi tiết = **R3**
  (NOT RUN); thước số = **R4**; API báo đúng lỗi = rà code gói 1b (`1e4acd0`); `[Nguồn n]` = gói 1a (`9e6d371`); 8.1 = G2 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md`
  §4, luật ghi trước `phase_8_1_g2_g4_plan.md` §2.1 sha `a4adfc8eedd9`).
- **B0** = lượt bạn đọc cặp câu trả lời mù (mốc người); luật dừng ở spec 8.2 §11 (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`).
- Mã giới hạn: tổng hợp nhiều nguồn = **F1**; bảng giá = **F2**; tách câu hai ý = giả thuyết **H13**.
- Thử 10 đoạn đầu tiên (24/10, 22 câu từ chối nhầm, 10 / 22 hết từ chối, chưa chấm): `reports/phase_8_probe_context_top10_2026_10_24.md`.
- **Lệch tài liệu đã biết (24/10, còn đúng 31/10):**
  - Spec umbrella `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` §1 cho phép "trả phần có căn cứ"; spec Phase 6 và prompt bắt từ chối cả câu.
    Code theo spec Phase 6.
  - `guides/full_corpus_rag.md:500` (đoạn lịch sử) còn ghi "direct `AsyncOpenAI`, không Agent/Runner"; code dùng OpenAI Agents SDK một lượt, không tool — đúng theo
    `docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md`. Không phải lỗi code.
