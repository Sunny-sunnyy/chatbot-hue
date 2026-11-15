# Mục "Từ web (chưa kiểm)" trả lời thẳng, gọn — implementation

B · viết 20:42 15/11/2026 · A giao theo góp ý User khi thử trang Trợ lý · plan `docs/superpowers/plans/2026-11-15-muc-web-gon-plan.md` (A duyệt bản `0c71bb06c4ba`; mức nhẹ) · nhánh `p9-web-gon` · **chờ User xem cặp trước / sau + một review cả nhánh**.

## Tóm tắt
- **Lỗi có thật (đếm 0 USD trước khi làm):** 35 / 38 mục web đã lưu viết kiểu kể về nguồn ("đoạn trích…", "chưa xác minh…"); một nửa là mục "không có câu trả lời" mà vẫn dài ~170 ký tự kèm 2 link. Gốc: lời dặn cũ **yêu cầu** viết như vậy.
- **Đổi một thứ** — hợp đồng đầu ra của lần gọi viết mục web: trả lời thẳng 1–2 câu, ≤ 2 mã nguồn; không đoạn trích nào trả lời được ⇒ model viết từ khoá, **code** thay bằng dòng cố định đã có, không link. Không cờ. Rào code, nhãn "chưa kiểm", câu cố định thiên tai, phần kho: không đổi.
- **Kết quả (28 đầu vào đã lưu, cùng đoạn trích, sau đúng một vòng chỉnh):** ba tiêu chí quyết ĐẠT; sàn rào code + sàn an toàn ĐẠT; **sàn đọc tay có 1 mục ở mức ranh giới** (một chữ suy ra, số đúng) — B báo A quyết, không tự coi là đạt.

## Số đo [đã chạy] — n = 28 (19 tin nhắn gửi model lưu 14/11: 9 hỏi kèm, 7 ngoài kho, 3 an toàn có mở web; + 9 mẫu giờ mở cửa 15/11)
| Vai | Chỉ số | Ngưỡng ghi trước | Mốc (bản cũ) | Lượt 1 | **Lượt 2 (sau vòng chỉnh — bản nộp)** |
|---|---|---|---|---|---|
| Quyết | Mục kể lể trong các mục model viết | ≤ 2 | 25 / 28 | 1 / 16 | **1 / 17** ✓ |
| Quyết | Độ dài trung vị mục model viết | ≤ 120 ký tự | 189 | 90 | **103** ✓ |
| Quyết | Mục dùng > 2 mã nguồn | 0 | 7 | 0 | **0** ✓ |
| Sàn | Mục trượt rào code (bị thay câu cố định) | ≤ mốc | 3 | 2 | **1** ✓ |
| Sàn | Đọc tay mọi mục hiện ra: câu khẳng định ngoài đoạn trích | 0 | — | (xem dưới) | **0 rõ ràng; 1 ranh giới** |
| Sàn | 3 câu an toàn mở web: lời khuyên nguy hiểm / mất cảnh báo có trong đoạn trích | 0 | — | 0 | **0** ✓ |
| Mức tụt | Từ khoá "không có" ở đầu vào mà bản cũ trả lời được có căn cứ | ≤ 2 | — | 0 | **0** ✓ |
| Theo dõi | Mục thành dòng cố định "chưa tìm thấy" | báo | 0 | 12 | 11 |
| Theo dõi | USD / lượt viết mục web · ms model trung vị | báo | ~0,00016 | 0,00012 · 1,6 s | 0,00016 · 2,3 s |

Đọc tay (B đọc 28 / 28 cặp kèm đoạn trích, file private `data/web_gon_2026-11-15/do2/doc_tay.md`):
- **Ranh giới (1):** một câu hỏi giá vé — mục mới ghi "vé một chiều … khoảng <số>" trong khi đoạn trích chỉ ghi "vé … khoảng <số>" (số đúng; chữ "một chiều" model suy ra do đoạn trích khác nói giá khứ hồi). Lượt 1 không có chữ này ⇒ dao động theo lượt.
- **Vì sao có vòng chỉnh:** lượt 1 có 2 mục giờ mở cửa mà các trang web ghi KHÁC nhau nhưng mục mới chọn một phía (nghe chắc hơn mức nguồn cho phép), 1 mục suy rộng chủ thể, và 1 mục model viết một câu rồi mới viết từ khoá (bị rào "đoạn không mã" thay câu cố định). Sau vòng chỉnh: 2 mục mâu thuẫn nêu ngắn cả hai phía; mục suy rộng thành câu thận trọng; từ khoá kèm câu không mã được nhận là "không có".
- **Điều mất đi:** ở 3 / 11 mục "không có", bản cũ có kể thông tin bên lề dùng được (khoảng cách tới trung tâm, tên hai quán, nơi khác cùng loại) — bản mới bỏ, đúng yêu cầu "không kể thứ không trả lời câu hỏi".
- 3 câu an toàn: một câu thành dòng cố định (bản cũ cũng không trả lời được); một câu nêu lời khuyên chung có nguyên văn trong tiêu đề đoạn trích; một câu nêu mẹo không dùng thuốc có trong đoạn trích — bản cũ có thêm câu "hỏi dược sĩ / bác sĩ" do model tự thêm, không có trong nguồn.

Hai câu kiểu User gặp, **đường thật** (kho + tra web thật, cùng đoạn trích cho hai bản; không vào luật quyết): câu nhiều ý "ở đâu + ăn gì gần đó" 301 ký tự / 2 link ⇒ 75 ký tự / 1 link; câu "từ nơi này sang nơi kia bao xa" 206 ký tự / 3 link ⇒ dòng cố định, 0 link. Cặp cho User: `data/web_gon_2026-11-15/cap_truoc_sau.md` (8 cặp, private).

## Thay đổi
- `backend/llm/full_corpus_prompt.py` `TU_WEB_LUAT` — lời dặn mới (không đổi lời dặn nào khác ⇒ không chạy "giống byte" cho phần kho / định tuyến).
- `backend/llm/tra_web.py` `la_khong_co` + `backend/llm/assistant.py` `cong_web` (3 dòng): từ khoá và không mã nguồn ⇒ kết quả `web_rong`, dòng cố định, `kiem = ["model_khong_co"]` (đếm được trong `chat_metrics` `web_kiem`).
- `backend/tests/test_b6_tra_web.py`: 5 ca cho nhánh mới (từ khoá lẫn trong mục có mã thì không nuốt mục).

## Kiểm + thời gian
| Bước | Kết quả | Thời gian |
|---|---|---|
| `test_b6_tra_web.py` không khoá / có khoá | 117 / 117 đạt | 17 s / 33 s |
| Chạy khô 0 USD (tính mốc bằng hàm kiểm hiện tại) | chạy được, bảng mốc ở trên | < 5 s |
| Lượt có phí 1 + 2 (28 lần gọi mỗi lượt) | bảng trên | ~1 phút mỗi lượt |
| 2 câu đường thật | chạy được | ~30 s |
| Test rộng · Playwright · an toàn 32 đủ bộ | không chạy: chạm một lời dặn + 3 dòng; không sửa giao diện; câu an toàn chạm đường đổi (3) đã nằm trong 28 | — |

Tiền thật (file kết quả): lượt 1 0,00342 + lượt 2 0,00446 + đường thật ≈ 0,0042 (2 lượt chat 0,0018 + 2 lần gọi bản cũ ≈ 0,0004 + Serper 0,002) ⇒ **≈ 0,012 USD** / trần 0,03.

## Giới hạn
- n = 28 trên 27 câu khác nhau; bản cũ so bằng chữ đã lưu (lượt 1 của 14–15/11), không chạy lại. Mục web dao động theo lượt (chữ "một chiều" ở trên là ví dụ) ⇒ sàn đọc tay cần đọc lại khi đổi lời dặn lần nữa.
- "≤ 2 link" do lời dặn giữ (0 / 28 vượt), **không** có rào code.
- Bỏ câu "chưa xác minh" làm mục web nghe chắc hơn; chỗ chống đỡ còn lại là nhãn "chưa kiểm" + rào số / tiền bằng code + luật "nguồn nói khác nhau ⇒ nêu cả hai".
- Lượt hỏi tiếp nhiều ý và câu lưu trú không có trong 28 đầu vào (lưu trú: 0 đầu vào) ⇒ chưa đo với lời dặn mới; rào "lưu trú 0 tiền" bằng code không đổi.
- Công cụ: `data/web_gon_2026-11-15/tools/` (`dem.py`, `do.py kho|chay|doc`, `cap_that.py`).
