# Report — mục "Từ web" gọn bản 2 + câu sức khoẻ do code nối (B)

B viết 14:30 16/11/2026 · plan `docs/superpowers/plans/2026-11-16-muc-web-gon-ban-2-plan.md` (A duyệt sha `cfa314ac6db0`) · nhánh `p9-web-gon-2` (code `722a717`) · tiền **0,0374 / 0,05 USD**.

## Tóm tắt
- **Số quyết ĐẠT** trên 28 đầu vào (so cặp với bản 1 lượt 2): kể lể 0 (≤ 2) · dài trung vị 99 ký tự (≤ 120) · 0 mục > 2 mã · trượt rào code 0 (mốc 1).
- **Sàn đọc tay "0 khẳng định ngoài đoạn trích":** chưa có kết quả — agent con ngữ cảnh mới do A giao đọc 100 % `data/web_gon_2026-11-16/do/doc_tay.md` (B không đọc sàn).
- **Câu sức khoẻ:** sàn bộ dò TRƯỢT 1 / 9 (S13: hỏi món "tốt cho sức khoẻ" ⇒ thêm câu nhắc hỏi dược sĩ thừa) ⇒ A chọn **ghi giới hạn, không vòng chỉnh**. Câu sức khoẻ gắn 12 / 12.
- Trạng thái: chờ sàn đọc tay ⇒ một review cả nhánh (C) ⇒ merge.

## Đổi gì
| File | Đổi |
|---|---|
| `backend/llm/full_corpus_prompt.py` `TU_WEB_LUAT` | giữ điều kiện / phạm vi đoạn trích kèm theo; điều nói về dịp / đối tượng khác không phải câu trả lời; câu sức khoẻ ⇒ dòng `SUC_KHOE` |
| `backend/llm/tra_web.py` | `SUC_KHOE_TEXT` (câu người dùng thấy, A giữ nguyên chữ) · `tach_suc_khoe` (chữ HOA không dấu) |
| `backend/llm/assistant.py` `cong_web` | bỏ dấu trước mọi kiểm; một chuỗi if / elif thay 3 lần `return`; nối câu cố định dưới MỌI kết quả sau lần gọi model; `web.suc_khoe` (cờ); `vet["web"]["chu_model"]` ghi cả khi `KHONG_CO` |
| `backend/tests/test_b6_tra_web.py` | 2 test mới (dấu bỏ trước kiểm ở 4 kết quả; chữ "sức khoẻ" thường không phải dấu) |

Bản 1 (`p9-web-gon`, 3 commit) cherry-pick lên `origin/main` `6012208`: **không xung đột** (STATUS cũ dự đoán xung đột 2–3 dòng ở `cong_web` — không xảy ra).

## Kiểm
| Bước | Kết quả | Thời gian |
|---|---|---|
| `pytest tests/test_b6_tra_web.py` (worktree, liên kết `data/`, `knowledge-base-hue/`) | 124 đạt | 18 s |
| `git diff --check` | sạch | — |
| Chạy khô 0 USD: `do.py kho` (mốc tính lại), `do_suc_khoe.py kho` (27 câu, nhóm chấm, ca đối chứng hàm tách dấu có / không) | đạt | < 10 s |
| Lượt có phí 1: 28 đầu vào (`data/web_gon_2026-11-16/do/sau.jsonl`) | 0,00463 USD · ms model trung vị 2.414 | 1 phút 24 |
| Lượt có phí 2: bộ dò 27 câu qua `cong_web` thật + Serper (`data/web_gon_2026-11-16/do_suc_khoe/ket_qua.jsonl`) | 0,0328 USD (gồm 27 lượt Serper × 0,001) · ms trung vị 5.188 | 2 phút 32 |

Không Q1 / Playwright: không đổi chuỗi gửi model ngoài lời dặn mục web (chính là thứ được đo), không đổi giao diện (mục web dựng Markdown ⇒ đoạn mới hiện sẵn). Test rộng `backend/tests`: NOT RUN — chạy một lần trước merge.

## Số đo (28 đầu vào, một lượt; mốc = bản 1 lượt 2)
| Chỉ số | Mốc | Bản 2 | Ngưỡng |
|---|---|---|---|
| Kết quả | có mục 15 · không có 11 · chưa xác minh 1 · rào chặn 1 | có mục 14 · không có 13 · chưa xác minh 1 · rào chặn 0 | — |
| Kể lể | (bản gốc 25 / 28) | 0 / 15 mục model viết | ≤ 2 |
| Dài trung vị | 103 | 99 ký tự | ≤ 120 |
| > 2 mã | 0 | 0 | 0 |
| Mức tụt: mốc có mục ⇒ bản 2 "không có" | — | 2 (hai câu an toàn sức khoẻ; cả hai được gắn dấu ⇒ vẫn hiện câu hỏi dược sĩ) | ≤ 2 |
| Chiều ngược (mốc "không có" ⇒ bản 2 có mục) | — | 0 | báo |

**B thấy khi dựng cặp cho User (KHÔNG phải sàn đọc tay; để người đọc tự đánh giá):** ở một câu giờ mở cửa, bản 1 nêu cả hai giờ khác nhau của các nguồn, bản 2 chỉ còn một giờ — trái câu lời dặn "nói khác nhau ⇒ nêu cả hai" (đoạn trích còn lại có giờ khác không: chưa kiểm).

## Bộ dò sức khoẻ (27 câu, agent con của A soạn)
| Nhóm | Câu | Gắn dấu |
|---|---|---|
| Không phải sức khoẻ (sàn) | 9 | **1** (S13) — sàn 0 ⇒ TRƯỢT |
| Sức khoẻ (rõ + ghép) | 12 | 12 |
| Ranh giới (báo riêng) | 3 | 2 (hai câu ghép; câu phòng khám nhận thẻ không gắn) |
| Cấp cứu (ngoài đời đi tuyến khẩn cấp, báo riêng) | 3 | 3 |

**Giới hạn ghi nhận (A chọn, không vòng chỉnh):** câu hỏi món ăn / dịch vụ dùng chữ "tốt cho sức khoẻ" có thể nhận thêm câu "nên hỏi dược sĩ / bác sĩ" thừa; mục web vẫn trả lời đúng điều được hỏi. Dấu chỉ có khi lần gọi viết mục web chạy (cổng web mở, Serper có kết quả, không phải câu thiên tai).

## Tiền
0,00463 (28 đầu vào) + 0,0328 (bộ dò) = **0,0374 USD** / trần 0,05. Không agent con của B.
