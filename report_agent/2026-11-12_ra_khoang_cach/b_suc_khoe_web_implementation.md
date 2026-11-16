# Report — câu sức khoẻ trong mục "Từ web" (lời dặn cũ) + đếm "chỗ ở không nêu hạng" (B)

B viết 14:42 16/11/2026 · A giao (User chọn giữ mục web bản dài + câu sức khoẻ) · nhánh `p9-suc-khoe-web` (code `43110de`) · plan gốc `docs/superpowers/plans/2026-11-16-muc-web-gon-ban-2-plan.md` (trên `p9-web-gon-2`; dùng lại §4 bộ dò + sàn) · tiền nhánh **0,0342 USD** / trần 0,05.

## Tóm tắt
- Câu hỏi sức khoẻ ⇒ lần gọi viết mục web gắn dòng `SUC_KHOE` ⇒ **code** bỏ dấu trước mọi kiểm và nối câu cố định "Thông tin sức khoẻ, thuốc men trên web chỉ để tham khảo — bạn nên hỏi dược sĩ hoặc bác sĩ trước khi dùng." dưới mọi kết quả sau lần gọi model. Phần rút gọn mục web KHÔNG vào nhánh này.
- Bộ dò 27 câu (agent con của A soạn) qua `cong_web` thật + Serper: **sức khoẻ gắn 12 / 12** · cấp cứu 3 / 3 · ranh giới 2 / 3 · **sàn gắn nhầm 3 / 9 — TRƯỢT** (S11 giờ khám bệnh viện, S12 giờ nhà thuốc, S13 món "tốt cho sức khoẻ"). Trên lời dặn bản 2 cùng bộ: 1 / 9 (chỉ S13) ⇒ lời dặn cũ (dài, cho phép kể) gắn rộng hơn.
- Hệ quả của gắn nhầm: thêm câu nhắc thận trọng thừa dưới mục web của câu sát chủ đề sức khoẻ (bệnh viện, nhà thuốc, món "tốt cho sức khoẻ"); chữ mục web không đổi. **Chờ A quyết:** ghi giới hạn hay một vòng chỉnh.

## Đổi gì
| File | Đổi |
|---|---|
| `backend/llm/full_corpus_prompt.py` `TU_WEB_LUAT` | thêm một câu: câu sức khoẻ / thuốc / bệnh / triệu chứng / chấn thương ⇒ dòng cuối đúng một từ `SUC_KHOE` |
| `backend/llm/tra_web.py` | `SUC_KHOE_TEXT`; `tach_suc_khoe` (chữ HOA không dấu — không khớp "sức khoẻ" viết thường) |
| `backend/llm/assistant.py` `cong_web` | bỏ dấu trước `kiem_muc_web`; if / elif thay 2 `return`; nối câu cố định khi có dấu; `web.suc_khoe = true` (cờ, không chữ) |
| `backend/tests/test_b6_tra_web.py` | 2 test: dấu bỏ trước kiểm + câu cố định ở có mục / rào chặn; không dấu hoặc "sức khoẻ" thường ⇒ không câu cố định |

## Kiểm
| Bước | Kết quả | Thời gian |
|---|---|---|
| `pytest tests/test_b6_tra_web.py` | 116 đạt | 22 s |
| `git diff --check` | sạch | — |
| Chạy khô `do_suc_khoe.py kho` (ca đối chứng có / không của hàm tách dấu) | đạt | < 10 s |
| Bộ dò 27 câu, lời dặn cũ + dòng dấu (`data/web_gon_2026-11-16/do_suc_khoe_loi_dan_cu/ket_qua.jsonl`) | 0,03417 USD (gồm 27 lượt Serper) · ms trung vị 6.598 | 3 phút 04 |

Không Q1 / Playwright (chỉ đổi lời dặn mục web — chính là thứ đo; giao diện dựng Markdown sẵn). Không đo lại 28 đầu vào web với dòng mới. Test rộng `backend/tests`: NOT RUN — chạy trước merge.
**Giới hạn:** dấu chỉ có khi lần gọi viết mục web chạy (kho từ chối + cổng web mở + Serper có kết quả + không phải câu thiên tai); câu khẩn cấp đi tuyến `khan_cap`.

## Đếm "xin chỗ ở không nêu hạng ⇒ hiện mọi hạng" — KHÔNG xây (A đồng ý)
Server tạm 8042 bản main `a9d1674`; mỗi câu một cuộc: biểu mẫu 3 ngày KHÔNG chọn hạng (lịch không ô Nơi ở) ⇒ 8 chuỗi / 9 câu xin chỗ ở không nêu hạng (B viết; công cụ `data/cho_o_khong_hang_2026-11-16/tools/dem.py`, kết quả `dem.jsonl`).
- 0 / 9 thành lượt sửa lịch, 0 / 9 hỏi lại hạng (giả định "bị hỏi lại hạng" không xảy ra); 8 / 9 được trả lời thường từ kho, đúng việc (khu nên ở theo lịch, nhiều câu nêu tên cơ sở kèm hạng).
- **Giới hạn ghi nhận:** câu ra lệnh "thêm chỗ ở vào lịch" bị từ chối bằng câu chuẩn (1 / 9) — ô Nơi ở không được thêm vào lịch bằng lời khi không nêu hạng.
- Tiền **0,019 USD** (17 lượt `chat_metrics`, gồm 8 lượt biểu mẫu — B ước 0,002 vì quên lượt biểu mẫu).
