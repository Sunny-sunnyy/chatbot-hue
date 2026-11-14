# Plan — câu nhiều ý: trả lời ý kho có, ý thiếu mới mở cổng web (việc agent (3), mức nhẹ)

Viết: C, 14/11/2026. A giao (User duyệt "4 việc theo thứ tự nhóm"; bàn nhóm vòng 1 B / C / E). Chờ A duyệt.

## Đếm lỗi trước khi xây (0 USD, dữ liệu đã có)
Bộ 10 câu hỏi kèm (`data/phase_9/t2_web/hoi_kem_10.jsonl`): mỗi câu có một ý kho có + một ý cần web. Lượt chạy thật 12/11 trên đường đang chạy
(`data/exa_2026-11-12/server/serper.jsonl`, Serper):
- **8 / 10 câu bị từ chối cả câu** — phần kho trả đúng câu "không đủ thông tin", dù ý kho có nằm sẵn trong kho;
- chỉ 4 / 8 câu có mục web dùng được.

Gốc lỗi: lời dặn có câu "Bằng chứng không đủ ⇒ trả **đúng duy nhất** câu từ chối" (`backend/llm/full_corpus_prompt.py:19`). Câu này kéo ngược với "gọi tim_kho tới khi đủ **mọi ý**" (`:97`). Rà lời dặn bản 1 của C (12/11) đã ghi chỗ lệch này. **Lỗi có thật, đủ nhiều ⇒ làm.**

## Làm gì (cờ `cau_nhieu_y`, mặc định tắt)
1. **Lời dặn trả lời** (chỉ khi cờ bật): thay câu `:19` bằng luật theo ý:
   - ý nào có Bằng chứng thì trả lời ý đó, kèm [n];
   - ý nào Bằng chứng không nêu thì viết **một dòng riêng** bắt đầu đúng chuỗi cố định `CAU_Y_THIEU = "Tư liệu chưa có thông tin về:"` + tên ý ngắn, không citation, không đoán;
   - không ý nào có Bằng chứng ⇒ trả đúng câu từ chối như cũ.

   Cờ tắt ⇒ chuỗi gửi model giống byte bản trước.
2. **Code, một chỗ** (`web_gate_open`, `backend/llm/assistant.py:898`): thêm điều kiện "cờ bật ∧ câu trả lời có dòng bắt đầu bằng `CAU_Y_THIEU`" ⇒ mở cổng web như với câu từ chối. Mọi điều kiện còn lại giữ nguyên (tuyến trợ lý Huế, chưa tra, không lịch, không lỗi, không hỏi lại).
   - Truy vấn web vẫn **do code dựng từ câu hỏi người dùng** (D2), không dùng chữ model ⇒ không thêm đường ra mới.
3. **Kiểm cuối bằng code:** dòng `CAU_Y_THIEU` không được có [n]. Có [n] ⇒ lỗi trích dẫn như hiện nay, không mở web.

## Tiêu chí ghi trước + bộ đo (bản build thật, `uv run --env-file`)
| Bộ | Sàn / chỉ số quyết |
|---|---|
| Hỏi kèm 10 ×1 | **quyết:** phần kho được trả lời ≥ 7 / 10 (mốc 2 / 10); mỗi câu trả lời: ý kho đúng + có [n], ý thiếu nằm ở dòng `CAU_Y_THIEU`, 0 câu bịa phần thiếu (C đọc tay cả 10) |
| An toàn 32 ×2 (2 người chấm, cổng đối chứng) | 0 đảo cảnh báo; sai điều kiện mới ≤ 2 (luật S-AT); 0 câu ngoài kho bị trả lời |
| Golden 176 ×1, so mốc K1 "sau" hôm nay (cùng kho, cùng code, chỉ khác cờ) | 0 / 18 câu ngoài kho bị trả lời; từ chối nhầm ≤ mốc + 1; Đủ / Đúng trung bình theo cặp ≥ −0,1; 0 lỗi kỹ thuật / trích dẫn mới |
| Test | test file chạm + Q1 (chuỗi gửi model giống byte khi cờ tắt); test cờ bật: lời dặn có câu mới, cổng mở đúng một lần với dòng `CAU_Y_THIEU`, không mở khi dòng đó có [n] |

Không chạy bộ kín: chỉ một vòng chỉnh lời dặn. Không đạt một sàn ⇒ cờ giữ tắt, ghi số, không chỉnh tiếp trong đợt này.
**Tiền ước:** hỏi kèm ≈ 0,02 · an toàn 32 ×2 ≈ 0,05 · Golden 176 ≈ 0,08 ⇒ **≈ 0,15 USD**. Chấm bằng agent con (quota Claude). Review: E.

## Bảng rà theo khung AI FDE (skill `agent-design-review` + `agent-security-review`)
| Mục | Hiện trạng | Sau thay đổi | Khớp / lệch |
|---|---|---|---|
| Luật kiểm được ⇒ code | "mở web khi nào" đã là code (`web_gate_open`) | thêm một điều kiện code dò chuỗi cố định; model chỉ đánh dấu ý thiếu | khớp |
| Một luật một nơi | câu từ chối là hằng `INSUFFICIENT_ANSWER` | `CAU_Y_THIEU` cũng là hằng, dùng chung cho lời dặn + code | khớp |
| Bộ ba chết người (dữ liệu riêng · nội dung không tin cậy · đường ra) | web: truy vấn = câu người dùng; mục web tách, có kiểm số / tiền / link | không đổi truy vấn, không đường ra mới; số lần tra tối đa vẫn 1 / câu | khớp |
| Câu ngoài phạm vi | định tuyến chặn trước; Phase 8.1 P1 (nới tương tự, chưa có định tuyến) từng làm 2 câu ngoài phạm vi bị trả lời | đo bằng 18 câu Golden ngoài kho + an toàn 32 | rủi ro chính, có sàn |
| Bịa phần thiếu | lời dặn cấm đoán; kiểm [n] ∈ nguồn | dòng thiếu không [n]; đọc tay 10 câu | có sàn |
| Tiền / tốc độ | mỗi câu hỏi kèm vốn đã mở web (sau từ chối) | như cũ — chỉ khác: phần kho có chữ | không tăng |

## File chạm
`backend/llm/full_corpus_prompt.py` (hằng + câu dặn theo cờ) · `backend/llm/assistant.py` (`web_gate_open`, cờ) · `backend/llm/generator_openai_full_corpus.py` (chọn lời dặn theo cờ, nếu cần) · `backend/config/settings.yaml` (`cau_nhieu_y: false`) · test mới trong `backend/tests/`.
