# E20 — vì sao model từ chối khi câu xin lịch có hỏi kèm

Người làm: E (Claude Code `hue-rag-28`), A giao lúc 22:13 06/11/2026. Viết lúc 22:21 06/11/2026 (`date`). Không sửa code.
Tiền: **0,008092 USD** (trần 0,01). File tracked, repo public: không chép câu hay chữ trả lời; tả ở mức loại câu.

## 1. Vấn đề

Kín v2 (`e19_kin_v2.md`): ở 2 / 5 câu xin lịch có hỏi kèm, chữ model là câu từ chối chuẩn. Một câu hỏi kèm chỗ ở, một câu hỏi kèm cách đi.
Lịch người dùng thấy là lời do code dựng (đường dự phòng T3 của B171); phần hỏi kèm bị bỏ qua im lặng.

## 2. Cách làm (ghi trước: `data/phase_9/b5_v2/e20/ghi_truoc.md`)

- **Bộ câu:** `data/phase_9/b5_v2/e20/cau_e20.jsonl` md5 `d79ffecd2c0b` — 10 câu **E tự viết**, không chép câu kín:

| Câu | Loại |
|---|---|
| A1–A2 | xin lịch + hỏi kèm chỗ ở |
| A3–A4 | xin lịch + hỏi kèm đi lại |
| A5 | xin lịch + giờ tới |
| A6 | xin lịch + giờ về |
| B1–B4 | A1–A4 bỏ đúng phần hỏi kèm — cặp đối chứng, đổi một thứ |

- **Chạy:** `data/phase_9/b5_v2/e20/tools/chay_e20.py` (md5 `b608966cb699`), 1 lần / câu, trên `main` (`7210d8c`, code như `dbb4004`), cờ `lich_trinh` bật trong tiến trình.
  - Giống harness B5, ghi thêm: câu tìm model gửi `tim_kho`, cờ "`tim_kho` sau khi có lịch", tham số số ngày model gửi.
  - 0 USD trước: chạy thử bằng khoá giả + cổng đóng ⇒ cả 10 câu tới bước gọi model, không vỡ. Lượt có phí: User `!`.
- **Giả thuyết H1 (ghi trước):** bị chặn tìm thêm sau khi có lịch + lời dặn "bằng chứng không đủ ⇒ trả **đúng duy nhất** câu từ chối" ⇒ model bỏ cả lịch.
- **Luật đọc (ghi trước):** H1 được ủng hộ nếu A1–A4 từ chối ≥ 2 / 4 **và** B1–B4 từ chối ≤ 1 / 4.

## 3. Kết quả [Chạy] — `data/phase_9/b5_v2/e20/ket_qua.jsonl` (private, md5 `cdd8f3ccf7e4`)

| Câu | Model từ chối | `tim_kho` sau khi có lịch | Ghi chú |
|---|---|---|---|
| A1 chỗ ở | **có** | có (tìm phần chỗ ở) | lời do code dựng thay |
| A2 chỗ ở | **có** | có (tìm phần chỗ ở) | lời do code dựng thay |
| A3 đi lại | không | không | ngữ cảnh tìm đầu (bằng câu gốc) đã có đoạn về phần hỏi kèm ⇒ model trả lời cả lịch lẫn phần hỏi kèm, có trích dẫn |
| A4 đi lại | **có** | có (tìm phần đi lại) | lời do code dựng thay |
| A5 giờ tới | không | không | lịch vẫn có buổi sáng ngày đầu, không nhắc giờ tới |
| A6 giờ về | không | không | chiều ngày cuối vẫn xếp điểm, không nhắc giờ về |
| B1–B4 | không (0 / 4) | không | lịch bình thường |

- **A1–A4 từ chối 3 / 4, B1–B4 0 / 4 ⇒ H1 được ủng hộ** theo luật ghi trước.
- **Quan sát khớp hoàn toàn:** 3 / 3 lượt từ chối đều có `tim_kho` sau lịch; 7 / 7 lượt không từ chối đều không có.
- Số ngày model gửi = số code dò = số chốt ở **cả 10** câu (không câu nào dùng cách viết tắt như K2 của kín v2).

## 4. Nguyên nhân — đã chứng minh ↔ suy luận

- **Đã chứng minh bằng code (tất định):**
  - `assistant.py` hàm `tim_kho`: khi lượt đã có lịch, `tim_kho` **không tìm** mà trả `TOOL_DA_DU_LICH` ("Lịch đã xếp và tài liệu của từng điểm đã có; không tìm thêm — hãy viết câu trả lời ngay theo khung"). Chặn này có từ B5 vòng chỉnh 1, vì pilot B160 từng chạm `max_turns`.
  - Lời dặn hệ thống (`ANSWER_SYSTEM_INSTRUCTIONS`): "Nếu bằng chứng không đủ, trả đúng duy nhất câu sau…". Đoạn công cụ: "Gọi `tim_kho` khi Bằng chứng hiện có chưa đủ để trả lời **mọi ý** của câu hỏi".
- **Quan sát [Chạy]:** phần hỏi kèm không có trong ngữ cảnh tìm đầu ⇒ model gọi `tim_kho` cho phần đó ⇒ bị chặn ⇒ trả câu từ chối thay cho cả lời lịch (3 / 3). Phần hỏi kèm có sẵn trong ngữ cảnh tìm đầu (A3) ⇒ không tìm thêm, không từ chối.
- **Suy luận (chưa chứng minh):** model đọc lời dặn "không đủ ⇒ trả duy nhất câu từ chối" theo nghĩa cả câu hỏi, vì không có luật "trả lời phần có, nói rõ phần không có". Đây là hành vi model, chưa thử đổi lời dặn để chứng minh.
- **Không phải nguyên nhân (đã loại):** ngân sách ngữ cảnh (0 lỗi ngân sách, 0 `max_turns`); thứ tự công cụ (cùng chuỗi `tim_kho` → `lich_trinh` ở cả A lẫn B); định tuyến (10 / 10 `tro_ly_hue`).
- **Ghi nhận ngoài việc:** ràng buộc giờ tới / giờ về (A5, A6) bị bỏ qua im lặng — B5 không có trường giờ (bảng R7: "không"). Đúng như đã biết, nhưng người dùng không được báo.

## 5. Đề xuất sửa (A / User quyết) + cách đo trên bộ đã thấy

Nguyên tắc AI FDE: điều bắt buộc ⇒ code; model chỉ diễn đạt.

- **Sửa 1 (khuyến nghị — code, tất định):** khi lời lịch do code dựng thay câu từ chối (`chu_thay`) **và** model đã gọi `tim_kho` sau lịch, code nối thêm một câu cố định đúng sự thật, vd "Phần bạn hỏi thêm ngoài lịch, mình chưa tìm thấy thông tin trong nguồn dữ liệu."
  - Không nhắc lại chữ người dùng. Không đổi lời dặn, không đổi chuỗi gửi model ⇒ Q1 giống byte khi cờ tắt.
  - **Đo:** test thuần (có / không `tim_kho` sau lịch ⇒ có / không câu nối); chạy lại bộ E20 ×1 (≈ 0,008 USD) ⇒ mọi lượt "từ chối + `tim_kho` sau lịch" có câu nối; B1–B4 không có.
  - **Khi nào sai:** model từ chối vì lý do khác (vd kho thật sự thiếu đoạn của điểm) mà vẫn có `tim_kho` sau lịch ⇒ câu nối vẫn đúng sự thật ("chưa tìm thấy").
- **Sửa 2 (tuỳ chọn, cần đo kỹ hơn):** cho `tim_kho` sau lịch tìm thật **một lần** cho phần hỏi kèm thay vì chặn hẳn; lần thứ hai mới trả `TOOL_DA_DU_LICH`.
  - Lợi: phần hỏi kèm có trong kho (như A3) thì vẫn được trả lời.
  - Rủi ro: chạm lại lỗi `max_turns` của pilot B160; đổi hành vi model ⇒ cần đo ×2 trên bộ đã thấy B5 13 câu + E20 10 câu: `max_turns` 0, từ chối ở A ≤ 1 / 8 lượt, B5 đã thấy không tụt.
  - Ước ≈ 0,04 USD. Nên làm sau Sửa 1 và khi bật lại đường câu gõ tự do.
- Không đề xuất đổi lời dặn hệ thống: lời dặn closed-world đang giữ sàn "0 câu ngoài kho bị trả lời"; đổi nó chạm cả RAG 1–8.

## 6. Giới hạn

- 1 lần / câu, 10 câu: chỉ là dò hướng. Tỉ lệ thật cần lượt đo ×2 khi sửa.
- Không xem chuỗi gửi model ở lượt có phí. Lời dặn và chữ công cụ lấy từ code (tất định); không bắt thân yêu cầu.
