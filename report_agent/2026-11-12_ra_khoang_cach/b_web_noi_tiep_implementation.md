# Câu hỏi nối tiếp: mục web mang đúng chủ thể — implementation · B · 16:02 15/11/2026

Plan `docs/superpowers/plans/2026-11-15-cau-noi-tiep-web-plan.md` (`236cc3b89b28`, A duyệt; User chọn hướng 15/11). Lỗi + nguyên nhân gốc: `b_cau_noi_tiep_dem.md`.
Nhánh `p9-web-noi-tiep` (code `16a6715`), cờ `web_cau_noi_tiep` — **mặc định TẮT**, chờ review rồi A trình User bật.

## Đã đổi (3 file)

- `backend/llm/assistant.py`: cờ mới; hàm `cau_cho_web` — cờ bật **và** lượt có lịch sử **và** model đã tự tìm kho ⇒ trả câu tìm kho cuối model viết, còn lại trả câu người dùng gõ.
  `cong_web` dùng câu đó cho (1) câu gửi tra web — vẫn qua `tra_web.cau_tim_web` (bỏ email / số điện thoại, cắt 120 ký tự, thêm "Huế") và (2) câu đưa model viết mục web.
  Luật chặn theo câu hỏi (thiên tai, thời gian thực, lưu trú) xét **cả hai câu** ⇒ chỉ chặt hơn; luật "số người dùng tự gõ được phép" vẫn chỉ tính câu gõ. Log: mục `tools` "tra_web" thêm cờ `cau_tu_model: true` (không chữ).
- `backend/config/settings.yaml`: `web_cau_noi_tiep: false`.
- `backend/tests/test_b6_tra_web.py`: +9 ca (4 loại lượt không đổi: cờ tắt / nơi gọi không truyền cờ / lượt đầu / có lịch sử nhưng model không tìm; lượt có lịch sử dùng câu model; bộ lọc email / số điện thoại / độ dài; 3 ca luật an toàn xét cả hai câu).
- Không đổi: cổng web, lời dặn, số lần gọi model, mọi kiểm cuối mục web, chuỗi gửi trợ lý.

## Kết quả theo tiêu chí ghi trước

Đo: `data/cau_noi_tiep_2026-11-15/tools/do_quyet.py` — đường stream thật, cùng cuộc 2 lượt, tra web thật, cờ bật trong bản sao settings trong RAM; 1 lượt; file `quyet_r1.jsonl`.
Bộ: 2 cặp đã thấy (B) + 12 cặp A viết (`bo_quyet_A.jsonl`, B không sửa; B đọc nhãn trước khi chạy, không thấy nhãn sai) + 3 chuỗi cũ "nêu tên rồi hỏi câu cần web".

| Tiêu chí | Mốc (cờ tắt) | Cờ bật | |
|---|---|---|---|
| Mẫu chỉ số quyết: cặp hỏi tiếp mà cổng web mở | — | n = **8** (2 đã thấy + 6 / 8 cặp N của A; **loại 2** cặp vì kho trả lời được — theo luật A ghi trước; cần n ≥ 6) | đủ mẫu |
| **Quyết 1:** câu gửi tra web nêu đúng chủ thể (so chữ bằng code; cần ≥ n − 1) | 0 / 10 (tất định, tính 0 USD trên cả 10 cặp) | **8 / 8** | ĐẠT |
| **Quyết 2:** mục web nói về nơi khác (B đọc tay cả 8; cần 0) | 2 / 2 (ca của User) | **0 / 8** — 5 mục nói đúng chủ thể, 3 mục là câu cố định an toàn | ĐẠT |
| S1: câu gửi tra web chứa tên người dùng | 0 | **0 / 4** lượt chạm (3 chuỗi cũ + 1 cặp mới; cặp mới còn lại kho trả lời được ⇒ "không chạm") | ĐẠT (n nhỏ) |
| S2: cờ tắt / lượt đầu / model không tìm ⇒ như cũ | — | test (4 ca) | ĐẠT |
| S3: cặp đổi chủ đề — câu web chứa chủ thể lượt 1 | — | **0 / 1** lượt chạm (cặp kia kho trả lời được) | ĐẠT (n = 1) |
| S4: kiểm cuối mục web giữ nguyên | — | không sửa code kiểm; 109 test file cổng web đạt | ĐẠT |

Ghi thêm: cặp "nêu tên mình" có cổng web mở thực ra cũng là câu hỏi tiếp ("trong đó…") — cờ tắt mục web nói chung chung về cả thành phố, cờ bật nói đúng nơi của lượt 1.

**Lượt đối chứng ngoài tiêu chí** (B thêm sau khi thấy rủi ro: cờ bật đổi câu web của MỌI lượt ≥ 2 có tìm kho, kể cả câu vốn đứng một mình; ghi rõ là không ghi trước; cờ tắt, 5 cặp, 1 lượt, `quyet_doi_chung_co_tat.jsonl`):
3 cặp câu đứng một mình so được — 1 cặp mục web giống nhau, 1 cặp đều ra câu cố định, 1 cặp "trích không cho biết" (tắt) ↔ câu cố định "chưa xác minh" (bật): không cặp nào kém đi rõ. n = 3, một lượt, kết quả web tự trôi ⇒ chỉ là "chưa thấy tụt".

## Điều người quyết cần biết (không che)

1. **Ca gốc của User hết lạc đề nhưng chưa có câu trả lời:** 2 / 2 lần cờ bật ra câu cố định "chưa tra được thông tin đáng tin" — mục model viết bị bộ kiểm số chặn (mã `so_ngoai_trich`: có con số không nằm nguyên dạng trong đoạn trích). Đây là luật kiểm cũ, không do bản sửa; cả lượt: 5 / 13 mục web cờ bật là câu cố định (3 do bộ kiểm số, 1 do bộ kiểm số + tiền, 1 do luật thời gian thực) (cờ tắt, mẫu khác: 1 / 4). Muốn ra được giờ mở cửa thật ⇒ việc riêng về bộ kiểm số (đếm trước).
2. **Câu model viết dài hơn câu gõ:** 1 / 13 câu bị cắt ở 120 ký tự (cắt giữa từ); model có khi thêm ngày cụ thể suy từ "cuối tuần này" ⇒ luật thời gian thực chặn (đúng hướng an toàn).
3. **Thứ ra ngoài đã đổi** (User đã nhận): chữ model viết, có tên nơi của lượt trước. Tên người dùng: 0 / 4 — mẫu nhỏ, rủi ro chưa loại hẳn.
4. Lượt hỏi tiếp mà model không tìm kho lần nào rồi kho từ chối ⇒ vẫn như cũ (0 lần gặp trong 17 cặp).

## Test, thời gian, tiền

| Bước | Kết quả | Thời gian |
|---|---|---|
| `test_b6_tra_web.py` (không khoá) | 109 đạt | 17 s |
| Test rộng `backend/tests` | **1.090 đạt**; 4 trượt + 4 lỗi đều do môi trường: 3 ca cần bản build giao diện (worktree của B không build), 1 trượt + 4 lỗi là nhóm test cần khoá OpenAI ghi trong handoff | 4 phút 51 s |
| Q1 "chuỗi gửi model giống byte" | NOT RUN — chuỗi gửi trợ lý không chạm; chuỗi lần viết mục web: test khẳng định 4 loại lượt không đổi | — |
| Playwright | NOT RUN — không sửa giao diện | — |
| Lượt có phí | 34 lượt (đo) + 10 lượt (đối chứng) | ~6 phút |

Tiền (log lọc `git_sha 16a6715`): **0,0556 USD** (trần 0,15); cộng phần đếm trước 0,0201 ⇒ cả việc 0,076 USD.

**Giải thích ngắn:** khi hỏi tiếp kiểu "mở cửa mấy giờ" mà kho không có, trợ lý trước đây đem nguyên câu cụt đó đi tra web nên trả lời lạc sang nơi khác. Bản sửa dùng luôn câu tìm kho mà model vừa tự viết (đã có tên nơi) để tra web. Đo 8 cặp: 8 / 8 câu tra web đúng nơi, không còn mục web lạc đề, tên người dùng không lọt ra. Còn hạn chế: nhiều mục web vẫn bị bộ kiểm số thay bằng câu "chưa tra được".

## Sửa theo review E (16:18 15/11/2026) — `e_review_web_noi_tiep.md`: 0 blocker / 1 major (chỉ chặn bật cờ) / 2 minor

- **M-1 (đóng theo cách A chọn):** lượt **nhiều ý** giữ câu người dùng gõ như cũ — câu tìm cuối của model có thể thuộc vế kho đã trả lời, còn mục web phải viết cho vế thiếu; đường này chưa đo nên không đổi. 1 điều kiện trong `cau_cho_web` + 1 ca test.
- **m-1:** câu tìm cuối của model rỗng / toàn dấu cách ⇒ rơi về câu gõ (không tra web bằng mỗi chữ "Huế"). + 1 ca test.
- **m-2 (theo dõi khi bật, A ghi checklist):** tên người dùng mới đo 0 / 4 lượt chạm; không thêm bộ lọc đoán.
- `test_b6_tra_web.py` 111 đạt (18 s). Không chạy lại lượt có phí: 17 lượt thứ hai đã đo không có lượt nhiều ý nào và không có câu tìm rỗng ⇒ hai sửa này không chạm lượt nào đã đo.
- Giới hạn mới: **câu hỏi tiếp nhiều ý mà kho thiếu vẫn tra web bằng câu gõ (có thể cụt)** — chưa sửa, chưa đo.
