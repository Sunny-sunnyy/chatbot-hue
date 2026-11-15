# Plan — tìm thêm song song (tốc độ) · B · bản 2 · 11:18 15/11/2026 (bản 1 11:15; sửa theo phản biện E)

User duyệt việc 15/11 (A giao): plan tốc độ 1 trang theo `run-experiment`. Mức nhẹ (≤ 0,2 USD, không đổi kiến trúc) ⇒ 1 người phản biện, A đọc.
Căn cứ đếm: `report_agent/2026-11-12_ra_khoang_cach/b_dem_toc_do.md` (E tính lại khớp).

## 0. Đếm trước khi xây (0 USD, đã chạy)

| Đo gì | Số | Nguồn |
|---|---|---|
| Lượt có tìm thêm (mọi lượt web cũng nằm trong đây) | 83 / 402 lượt gọi model thật từ 10/11 (20,6 %) | `chat_metrics` |
| Chữ đầu lượt tìm thêm / mục web | p50 8,57 s / 6,78 s (sàn 3 s) | như trên |
| Số lần model tự tìm / lượt | 2 lần: **52** · 1 lần: 31 (22 lượt chạm trần ⇒ "hết lượt") | `tools` |
| Câu tìm mỗi lần gọi | **1 câu ở 135 / 135 lần** | `n_queries` |
| Golden 176 (lượt đủ sau ghi kho 2) | 14 câu model tìm 2 lần · 29 câu 1 lần · 122 câu không tìm thêm | `ghi_kho_2/sau/golden.jsonl` |

⇒ Chậm vì lần tìm thứ hai **chờ** lần gọi model trước. `parallel_tool_calls=False` đang ép mỗi lượt gọi model chỉ một công cụ (`backend/llm/generator_openai_full_corpus.py:325`, B2 D5).

## 1. Biến thể — đổi MỘT thứ

- **H1:** `parallel_tool_calls=True` cho agent trợ lý (cờ mới `tim_song_song`, mặc định tắt) ⇒ model **được phép** gọi 2 `tim_kho` trong cùng một lượt; hai lần tìm chạy cùng lúc.
  Trần `MODEL_SEARCH_LIMIT = 2`, sổ nguồn, `het_luot_bo_cong_cu`, lời dặn: **không đổi**.
- Giả định cần kiểm **trước khi đo có phí** (0 USD):
  (a) hai `tim_kho` song song: trần đếm trước `await` ⇒ lần thứ 3 vẫn bị chặn; dựng gói nguồn + `extend` đồng bộ ⇒ không trùng đoạn, không vượt ngân sách (E đọc code).
  Số thứ tự nguồn theo **lần tìm xong trước** ⇒ chạy lại có thể khác thứ tự — tiêu chí là **mỗi [n] trỏ đúng nguồn của gói đó** (test), không đòi giống byte;
  (a') hai `retrieval_service.search` đồng thời ở 2 luồng (SDK `asyncio.gather`, search trong `to_thread`) dùng chung model e5 + tokenizer HF — tokenizer "fast" từng ném
  "Already borrowed" khi chia luồng ⇒ phép thử 0 USD: **50 cặp search đồng thời trên Qdrant thật ⇒ 0 lỗi, kết quả = chạy lần lượt**; lỗi ⇒ thêm khoá quanh encode
  (lợi chính là bớt một lượt gọi model, vẫn còn);
  (b) cờ tắt ⇒ chuỗi gửi model giống byte (228 / 228).
- Không làm: hạ trần 2 ⇒ 1 (bớt tìm ⇒ rủi ro thiếu ý câu nhiều nguồn, tìm thêm từng cho +1,17); model viết lại câu tìm đầu (B2a đã thử, không qua luật); hiện dòng "đang tìm" (không phải chữ trả lời).

## 2. Tiêu chí (ghi trước khi thấy số)

- **Câu chạm:** cờ bật đổi **mọi** yêu cầu gửi trợ lý (tham số `parallel_tool_calls`) ⇒ chạm = 176 Golden + an toàn 32 (luật "đo đúng chỗ đổi": băm yêu cầu khác ⇒ chạm hết).
- **Sàn:** an toàn 32 đủ 4 số, 0 đảo cảnh báo / 0 đổi lớp mới so với lượt kho 6; 18 câu ngoài kho 0 bị trả lời; 0 lỗi kỹ thuật; từ chối nhầm ≤ mốc + 1; 0 lỗi trích dẫn mới.
- **Mức tụt cho phép:** câu có chữ khác mốc ⇒ agent con chấm mù cùng ý / khác ý; **khác ý mà bản sau kém ≤ 1 câu** (mốc A/A: 56 / 57 cùng ý ở đo bù 15/11).
- **Chỉ số quyết:** trên 14 câu Golden model tìm 2 lần (danh sách lấy từ mốc): **số lần gọi trợ lý nối tiếp** giảm ở ≥ 7 / 14 câu.
- **Theo dõi (không quyết — nhiễu provider lớn trên 14 câu):** cả câu theo cặp từng câu (trung vị hiệu số sau − trước), Golden harness không stream.
- **Theo dõi:** USD / câu; số câu model gọi 2 công cụ cùng lượt; chữ đầu qua server stream ở 5 câu tìm thêm × 5 lượt (mốc sạch ≥ 5 lượt cùng ngày, không chồng việc nặng).
- **Giữ khi:** đủ sàn + mức tụt + chỉ số quyết. Model hầu như không gọi song song (< 3 / 14) ⇒ "không đổi", gỡ cờ, ghi kết quả âm — **không** thêm lời dặn ép gọi song song ở bậc này.

## 3. Đo

1. Mốc: Golden 176 + an toàn 32 + 18 ngoài kho đã có trên kho hiện tại sau khi C dựng xong (nếu C đổi kho ⇒ chạy lại mốc 176 ×1 trên kho mới, ≈ 0,06 USD).
2. Chữ đầu: mốc 5 câu × 5 lượt qua server trước khi bật cờ; sau bật 5 × 5. Không chạy khi C dựng / E build Docker.
3. Biến thể: cùng lệnh, cờ bật (bản sao settings trong RAM, không sửa `settings.yaml` tới khi đạt).

## 4. Tiền và trần

Mốc 176 (nếu cần) ≈ 0,06 · biến thể 176 + an toàn 32 + 18 ≈ 0,09 · chữ đầu 50 lượt ≈ 0,03 · chấm mù: quota Claude ⇒ **≈ 0,12–0,18 USD**, trần 0,2. Dừng nếu một lượt quá 30 phút.

## 5. Khi nào sai

- Model không dùng song song (không lời dặn) ⇒ lợi 0 — vẫn là kết quả, gỡ.
- Hai câu tìm song song cùng lấy đoạn trùng ⇒ ít nguồn mới hơn tìm nối tiếp (lần 2 không biết lần 1 đã có gì) ⇒ có thể thiếu ý: mức tụt + chấm mù bắt.
- Lợi chỉ ở ~8 % câu Golden (14 / 176) và ~13 % lượt thật (52 / 402) ⇒ p50 chung gần như không đổi; sàn mục web không đạt bằng bậc này; lượt thường p95 5,92 s (E đếm)
  cũng trượt ⇒ **sau bậc này sàn chung vẫn chưa đạt** (nói rõ với User).

## 6. Rà khung AI FDE (ngắn)

| Mục | Hiện trạng | Khớp / lệch | Đề xuất |
|---|---|---|---|
| Phép tính / trần do code | trần 2 lần tìm đếm ở `assistant.py:56`, `:861` (tăng trước `await`) | khớp | giữ; test (a) + phép thử (a') |
| Công cụ / tham số | `tim_kho(cau_tim: str)` không đổi | khớp | — |
| Vòng lặp + phục hồi | `max_turns` 4 + `het_luot_bo_cong_cu` không đổi | khớp | — |
| Bảo mật | không nguồn / đường ra mới | khớp | — |
