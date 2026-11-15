# Câu hỏi nối tiếp mất ngữ cảnh — tái tạo, đếm, nguyên nhân gốc · B · 15:49 15/11/2026

A giao (User tự thử 15/11 gặp lỗi): lượt 1 hỏi về một nơi, lượt 2 hỏi tiếp không nêu tên nơi ("… lúc mấy giờ") ⇒ kho từ chối ⇒ mục web trả lời về nơi khác và ghi "bạn chưa nêu địa điểm".
**Chưa sửa code.** Dữ liệu + công cụ (private): `data/cau_noi_tiep_2026-11-15/` (`tools/dem.py`, `cap_cau_r1.json`, `cap_cau.json`, `ket_qua_r1.jsonl`, `ket_qua_r2_web.jsonl`). Câu thử do B tự viết.

## Cách đo

Đi đúng đường người dùng: `POST /api/chat/stream`, cùng cuộc trò chuyện, 2 lượt (chạy trong tiến trình với app thật: kho, model, định tuyến như server). Công cụ **ghi lại rồi gọi tiếp hàm thật**:
mọi câu tìm kho (lần đầu do code, các lần model tự viết) kèm 3 tiêu đề đầu, và câu code gửi tra web. "Nêu chủ thể" = chuỗi có tên nơi / món của lượt 1 (so chữ bằng code).

## Kết quả

**Bước 0 USD — lần tìm đầu của code (dùng nguyên câu lượt 2), 10 cặp:**

| Loại cặp | Lần tìm đầu trúng chủ thể (3 đoạn đầu) | Nếu ghép câu 1 + câu 2 bằng code |
|---|---|---|
| Hỏi tiếp, không chủ ngữ (4) | **0 / 4** | 3 / 4 |
| Hỏi tiếp, có đại từ "nó / ở đó / … này" (3) | **1 / 3** (1 cặp may nhờ danh từ chung trùng tên) | 3 / 3 |
| Đổi chủ đề thật (3) | 3 / 3 | **1 / 3** — ghép làm hỏng 2 cặp |

⇒ ghép câu bằng code không dùng được (cứu câu hỏi tiếp nhưng phá câu đổi chủ đề).

**Lượt thật 1 — 10 cặp, kho CÓ thông tin được hỏi (0,0122 USD theo log lọc sha):**
- 7 / 7 cặp hỏi tiếp **trả lời đúng chủ thể**, 0 từ chối, 0 mục web. Ở 5 / 7 cặp model tự gọi tìm thêm một lần với câu tìm **có nêu tên chủ thể** (5 / 5); 2 cặp còn lại trả lời được từ lần tìm đầu.
- 3 / 3 cặp đổi chủ đề trả lời đúng, không tìm thêm.
- Hệ quả phụ: câu hỏi tiếp gần như luôn tốn thêm một lần gọi model (lần tìm đầu của code trượt 6 / 7) — chậm hơn chứ không sai.

**Lượt thật 2 — tái tạo ca của User: 2 cặp mà kho KHÔNG có thông tin được hỏi (một nơi kho không ghi giờ mở cửa; gọi tra web thật; 0,0079 USD theo log lọc sha):**

| Cặp | Model tìm kho | Kho | Câu code gửi tra web | Mục web |
|---|---|---|---|---|
| không chủ ngữ | 2 lần, cả 2 nêu đúng tên | từ chối (đúng — kho không có) | **nguyên câu lượt 2, không tên nơi** | nói về hai nơi KHÁC + "bạn chưa nêu rõ địa điểm" |
| có đại từ "nó" (đối chứng) | 2 lần, cả 2 nêu đúng tên | từ chối (đúng) | **nguyên câu lượt 2** | nói về nơi khác + "chưa nói rõ 'nó' là địa điểm nào" |

⇒ **tái tạo 2 / 2**, kể cả khi có đại từ.

## Nguyên nhân gốc (đã chứng minh bằng câu ghi lại + mã)

1. **Phần kho không mất ngữ cảnh:** lịch sử (các câu hỏi trước) có tới model; model viết câu tìm nêu đúng tên (9 / 9 lần tìm thêm của các cặp hỏi tiếp).
2. **Phần web mất ngữ cảnh — do thiết kế cũ:** `assistant.cong_web` dựng câu tra web bằng `tra_web.cau_tim_web(câu hỏi lượt này)` — hàm ghi rõ "không câu ghép, không lịch sử"; lần gọi model viết mục web
   (`generate_web_section`) cũng chỉ nhận câu lượt này + đoạn trích, không lịch sử. Lý do cũ: sàn "0 truy vấn web chứa tên người dùng" (người dùng nói tên mình ở lượt trước) — bộ 3 chuỗi `data/phase_9/bo_do_b3/web_neu_ten.jsonl`.
   Hệ quả: mọi câu hỏi tiếp mà kho thiếu ⇒ tra web bằng câu cụt ⇒ mục web lạc đề. Ca chưa có trong bộ đo nào (bộ nhớ hội thoại chỉ có "đó / này" với câu kho trả lời được).
3. Giả thuyết ban đầu của A "câu tìm đầu dùng câu trần": **đúng nhưng không phải nguyên nhân của lỗi User thấy** — model tự bù bằng lần tìm thêm; "câu gửi web dùng câu trần": **đúng, là nguyên nhân**.

## Không kết luận được

- n nhỏ (7 cặp hỏi tiếp + 2 cặp kho thiếu, mỗi cặp 1 lượt): tỉ lệ ở người dùng thật chưa biết; cặp 3 lượt trở lên chưa thử.
- "Nhớ cả câu trả lời" (`nho_cau_tra_loi`, tắt từ 03/11 vì phạm sàn trích dẫn trên bộ kín) không liên quan lỗi này — không đề xuất bật lại.

Tiền (log lọc `git_sha`): lượt 1 0,0122 + lượt 2 0,0079 ⇒ **0,0201 USD** (trần A cho 0,02 — chạm trần, không chạy thêm). Plan sửa: `docs/superpowers/plans/2026-11-15-cau-noi-tiep-web-plan.md`.
