# TONG_HOP — rà code Phase 0–7 (đợt `2026-10-25_ra_soat_code`)

Người gộp: A (Claude Opus 5.5, `hue-rag-77`) · 18:57 25/10/2026 (`date`) · trạng thái: **rà + kiểm chéo xong; chờ User chọn gói sửa**.
Báo cáo cho User (lời thường, có câu hỏi): `bao_cao_he_thong/DE_XUAT_SUA_CODE.md`. Chưa sửa code (User 18:3x: "tôi đồng ý mới sửa").

## Mục tiêu

User 16:5x 25/10: dừng 8.2, rà **code** (file, folder, guide) các Phase trước rồi mới đi tiếp. Tiêu chí 1–7 và phạm vi: mục "Rà code" trong
`session_prompt/CURRENT_HANDOFF.md` (bản `c272644`). Chỉ đọc, 0 USD, rà trên `main` `bc568f1` / `1e8cf8f` (code không đổi giữa hai commit).

## Diễn biến (giờ theo `date` / tin nhắn)

| Giờ | Việc |
|---|---|
| 16:58 | A giao B25 (dựng index + nền), C34 (trả lời + đánh giá); dừng 17:05 vì kết phiên |
| 18:25 | Phiên mới, User cho tiếp; B / C làm tiếp từ phần dở |
| 18:3x | User: báo cáo "nên sửa gì" trước, đồng ý mới sửa; commit + push trước khi sửa code; được thử nghiệm / so sánh |
| 18:3x | C báo sớm C-09 (cao); A tự kiểm 3 điểm (code `citations.py:9`, `full_corpus_context.py:82`, `chat.py:136-145`; đếm độc lập g20 dev 4 / 4, g24_none 6 / 8; report G2 `:100`) ✔ |
| 18:39 | B25 xong: 21 finding. A tự kiểm B-11 (checker token chỉ quyết tách, không ghi `errors`), B-12 (9 selector, 5.324 ký tự), B-19 (48 đường dẫn ngoài repo trong 6 guide) ✔ |
| 18:43 | C34 xong: 18 finding (C-15, C-16 gộp) |
| 18:51 | B kiểm C-09, C-02, C-01, C-12, C-19: 5 / 5 đúng, 6 minor (R-01…R-06) — `kiem_cheo_B.md`; B tự rút B-08 (sai) |
| 18:55 | C kiểm B-11, B-12, B-16, B-17, B-20: 4 đúng, B-17 một phần, 4 minor (R1–R4) — `kiem_cheo_C.md`; B-01 = C-01 tìm độc lập ⇒ coi như đã kiểm chéo |

## Kết quả — gói đề xuất (chi tiết, mức, phương án: file finding)

| Gói | Finding | Ghi chú gộp |
|---|---|---|
| 1 Lỗi chatbot đang gặp | **C-09** (cao; 4–8 / 176 câu ⇒ 500, toàn do định dạng `[Nguồn n]`) · **B-01 = C-01** (+ tách lỗi "model không nạp" khỏi 409; một quy ước import cho build / API / test / harness) + C-11 | R-01, R-02 (tính lại mốc ra file mới, không ghi đè G0.6; chốt định nghĩa trước khi mở câu kín), R-03 (UI chỉ tách `[n]`) |
| 2 Chốt an toàn trước build lại | B-11 (vừa sau kiểm chéo; phải sửa trước build lại; huydang 255 / 256) · B-20 · B-18 | R1, R2 |
| 3 Công cụ đo trước 8.2 | C-02 (sửa cả `verdict`, R-04) + C-20 · C-03 · 3c: xem lại quyết định 8.1 reasoning `none` sau C-09 (giả thuyết, thí nghiệm) | plan E1 phụ thuộc C-02 + C-09 |
| 4 Tài liệu | B-16 + C-12 + C-13 + C-14 (một lần sửa) · B-17 (thấp sau kiểm chéo) · B-21 · B-19 | đường dẫn chết trước sửa: phase_1 4, phase_2 4, phase_3 10, phase_4 5 |
| 5 Dọn code (không đổi hành vi) | B-02, B-04, B-05, B-06, B-07, B-09, B-14, B-15, C-04, C-06, C-07, C-10, C-17 (= marker `live` B-20), C-18 | gộp vào lần sửa đụng cùng file; kiểm: sha đoạn toàn kho, T1 retrieval giống byte |
| Câu hỏi User | C-05, C-19 (giữ / gỡ Representation B, 2 runner smoke; R-06) · B-12 + B-19 (repo public) · B-16 cách sửa guide | |
| Để sau (thiết kế) | B-03 (yaml ↔ loader ghim cứng), B-13 (converter dùng một lần), B-10 (dependency thừa — User giữ) | |
| Đã đo, ổn | C-08 (tìm kiếm p50 28 ms; độ trễ ở bước sinh) | |

## Thứ tự A đề xuất

Review + merge B1 (`p82-b1`) trước (gói 1b chạm `retrieval/full_corpus.py` B1 sửa) → gói 1 (1a rồi 1b) → gói 3 → gói 2 + 5 cùng đợt build
lại index → gói 4 bất cứ lúc nào. Mỗi gói: commit + push trước khi sửa; plan ngắn; review chéo; test liệt kê file + đường thật; 4 chỗ
`bao_cao_he_thong/` nếu đổi hành vi.

## Giới hạn

- Hiệu năng chỉ đo tầng tìm kiếm (C-08) và khởi động (B-08 rút); không đo độ trễ sinh mới.
- Tác động "Qdrant lỗi khi hỏi ⇒ 500" (C-01) vẫn suy ra từ code; trường hợp index cũ đã tái tạo bằng cấu hình trong bộ nhớ (A chấp nhận làm
  bằng chứng phụ — không đổi dữ liệu / môi trường).
- 8 test cần `OPENAI_API_KEY` không chạy (không `--env-file`); "không paid khi có key" dựa trên đọc code (C kiểm B-17).
- Kết quả chi tiết của sub-agent (private): `data/ra_soat_code/sa{1,2,3}_*.md` (B), `/tmp/c34/` (C, tạm); script: `data/ra_soat_code_2026-10-25/tools/`.
- A sửa `Project_Status.md` §8 (lệnh pytest, danh sách test paid lỗi thời) theo báo của C — governance nhỏ, ghi ở đây để người khác kiểm.

## Bước tiếp

User trả lời 4 câu ở `DE_XUAT_SUA_CODE.md` §4 ⇒ A ghi mục việc từng gói trong `CURRENT_HANDOFF.md`, giao B / C (file không chồng nhau).
