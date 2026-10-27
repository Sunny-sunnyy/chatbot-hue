# Đợt sửa kho + build lại index — tài liệu thiết kế (NHÁP, chờ User duyệt)

Người viết: A · Ngày: 27/10/2026 · Trạng thái: **chờ review (session khác) rồi User duyệt sha** — số mục từ B73 (xong 14:31 27/10; `data/sua_kho_2026-10-27/README.md`, private).
Lý do mở: User 27/10 chiều — "xong phần tồn càng sớm càng tốt, xong phần tồn mới yên tâm đi tiếp các phase tiếp theo".
File tracked này **không chép nội dung kho**: chỉ quy trình, số đếm, đường dẫn private.

## 1. Mục tiêu

Sửa các lỗi kho đã biết (rà kho C32, 25/10: 139 mục) và một lỗi cấu hình index (file danh mục `performing_arts` tự ghi "phải loại khỏi
ingestion" nhưng đang nằm trong index), rồi build lại index — để chatbot không trả lời theo thông tin mâu thuẫn / sai trong kho. Đây là
**phần tồn cuối** của các Phase cũ (Phase 2 kho / chunker, 7A2 index).

Không đổi: chunker, model tìm, cách trộn, context, prompt, model sinh. Chỉ đổi **nội dung kho** + **danh sách file loại khỏi index**.

## 2. Thứ tự với Phase 8.2

Chạy **sau** mốc cuối 8.2 (B3, câu kín) và User đóng 8.2. Lý do: B3 so chatbot đầu ↔ cuối 8.2 trên **cùng kho**; sửa kho trước B3 thì kết
quả lẫn hai thay đổi. Chuẩn bị (B73) làm trước, 0 USD, không đụng kho.

## 3. Đầu vào (B73, private `data/sua_kho_2026-10-27/`)

| Nhóm | Số mục | Xử lý trong đợt |
|---|---:|---|
| Sửa được bằng căn cứ trong kho (đã đọc lại từng mục; diff dựng bằng máy, chuỗi cũ khớp đúng 1 lần) | 41 | đợt này |
| Chuyển nhóm khi đọc lại: 9 sang tra ngoài (8 vì hai nguồn trong kho ngang nhau), 3 sang "không cần sửa" | 12 | theo nhóm mới |
| User biết thì trả lời (`cau_hoi_user.md`, lời thường, mỗi câu có gợi ý) | 16 | đợt này, theo câu trả lời User |
| Cần tra ngoài (`tra_ngoai.md`, 7 loại: hành chính, quán ăn, khoảng cách, lịch sử, dự án, lịch lễ hội, giao thông / vé; + nháp yêu cầu ChatGPT) | 69 + 9 = 78 | **đợt 2** (Q2) |
| File danh mục `performing_arts` ⇒ `exclude_files` (205 ⇒ 204 file, 8.459 ⇒ 8.426 đoạn; vào context B1 ở 3 / 176 câu; nhãn gold_v2 trỏ tới: 0) | 1 file, 33 đoạn | đợt này |

Phát hiện thêm khi soạn (ngoài 139 mục): tên đơn vị hành chính cũ còn sót ⇒ B74 soạn **11 diff / 14 edit** (`diffs_them/`, căn cứ duy nhất: ghi chú
sắp xếp đơn vị trong kho; 5 chỗ không soạn có lý do) — C67 review; cấp hành chính ghi chưa thống nhất để chung với mục cùng loại.

**Review đề xuất (C66, 27/10):** vòng 1 `changes_requested` (3 mục: một edit đổi câu đúng thành sai, hai edit bỏ mất thông tin ngoài phạm vi) ⇒ B sửa ⇒ vòng 2
`ready_for_user_confirmation`: 40 giữ + 1 giữ có điều kiện (chỉ áp nếu **không** loại file danh mục — mục đó sửa chính file danh mục); 9 / 9 edit nhóm đánh dấu
giữ (đủ căn cứ trong kho); áp thử toàn bộ edit trong bộ nhớ 0 lỗi, 0 chồng chéo. Áp thật bằng thay chuỗi từ `edits/*.jsonl` (file `.diff` chỉ để xem).

Sự cố khi soạn (B73, 27/10): một sub-agent nhóm món ăn grep cả thư mục và đọc nhầm Golden Foods cũ (không phải câu kín). Các bản sửa của
nhóm đó **đánh dấu riêng**; người review đối chiếu từng bản chỉ với căn cứ trong kho, bản nào không đứng được thì bỏ.

## 4. Quyết định của User (15:21 27/10/2026)

| Câu | User chọn |
|---|---|
| Q1 phạm vi đợt 1 | 41 mục (40 + K091 có điều kiện ⇒ **không áp** vì file danh mục bị loại) + 11 diff tên đơn vị sót + loại file danh mục + 16 câu User trả lời; tra ngoài ⇒ đợt 2 |
| Q2 tra ngoài | đồng ý, chỉ câu ngắn (không gửi cả file) |
| Q3 cách thay index | **tại chỗ** (snapshot trước) |
| Q4 Qwen3-8B | **thí nghiệm sau đợt sửa kho** — chưa từng đo (7A2 hoãn vì 504 / 429; 8.2 để ngoài vì không build lại index). Collection riêng, đo tầng tìm trước, plan riêng có review; chatbot không đổi tới khi có số. A đã rút khuyến nghị "đóng" (lý do vận hành, không có số chất lượng — trái nguyên tắc "thử + so baseline") |
| Q5 Golden lệch kho | đồng ý: quét + User duyệt sửa Golden trước khi đo lại |

Phân tích từng câu lúc trình (giữ làm hồ sơ):

- **Q1 — phạm vi đợt 1.** A khuyên: mục có căn cứ trong kho + file danh mục + mục User trả lời; phần tra ngoài để đợt 2. Sai khi: phần lớn lỗi
  User gặp nằm ở nhóm tra ngoài.
- **Q2 — tra ngoài qua ChatGPT** = đưa trích đoạn kho ra ngoài. A khuyên: đồng ý, chỉ gửi câu ngắn cần tra (không gửi file), kết quả qua
  `gửi chatgpt/`, A / B WebFetch đối chiếu URL; web mâu thuẫn kho ⇒ ghi nguồn, User chọn (`Session_Prompt.md` §5).
- **Q3 — cách thay index.** (a) tại chỗ: xóa collection + build record + sparse state rồi build lại đúng tên — chatbot ngừng trong lúc build
  (e5 CPU, thời gian đo khi chạy); (b) đích mới rồi cutover — cần sửa code runtime đọc tên đích từ cấu hình. A khuyên **(a)**: chatbot chạy
  trên máy User, ngừng ngắn chấp nhận được; (b) là code mới chưa có nhu cầu (deploy). Có snapshot trước khi xóa.
- **Q4 — index Qwen3-8B** (tồn từ 7A2, spec 8.2 để ngoài). A khuyên lúc đầu (đã rút) **đóng: không làm trong đồ án** — mỗi câu hỏi phải gửi ra OpenRouter để
  nhúng (thêm độ trễ mạng, đã gặp 504 / 429, câu hỏi người dùng ra bên thứ ba), trong khi p95 đã vượt mức theo dõi. Đảo khi: sau đợt sửa kho,
  tầng tìm vẫn là chỗ mất điểm chính và cách chạy trên máy đã thử hết.
- **Q5 — Golden lệch kho sau sửa.** Sửa một fact có thể làm `reference_answer` / `keywords` Golden lệch kho. A khuyên: quét Golden tìm câu chạm
  fact đã sửa (theo `file:dòng`), đưa danh sách đề xuất sửa Golden cho User duyệt **trước** khi đo lại.

## 5. Các bước (mỗi bước người làm ↔ người kiểm khác nhau)

1. **Sao lưu** file sẽ sửa vào `knowledge-base-hue/meta/` (kèm ngày). Snapshot Qdrant collection đang chạy; copy build record + sparse state ra
   `data/sua_kho_2026-10-27/backup/`.
2. **Áp sửa** (B) theo diff đã duyệt; luật curated `Session_Prompt.md` §5. **Review** (C): diff với backup, từng mục khớp đề xuất; nhóm đánh
   dấu riêng đối chiếu căn cứ trong kho.
3. **Thêm file danh mục vào `exclude_files`** (`backend/config/settings.yaml`); test discovery liên quan.
4. **Chia đoạn thử, chỉ đọc:** `chunk_full_corpus()` 0 lỗi; token từng đoạn với 3 tokenizer (`guides/full_corpus_rag.md` "Build lại index"
   bước 2 — giới hạn sát nhất huydang 256). Vượt ⇒ dừng, báo A.
5. **Build lại tại chỗ** (Q3 (a)) theo guide bước 4a–6; xóa sparse state cũ trước (bẫy `Project_Status.md` §8).
6. **Kiểm sau build:** summary build; `/health` 5 / 5; cổng ổn định 2 câu; **T1 mới** (158 câu) làm mốc tìm mới — so T1 cũ theo câu: câu nào
   đổi đoạn, có giải thích bằng file đã sửa không; Golden sửa (Q5) rồi **chạy 176 câu** + judge mù cùng lượt so trước ↔ sau theo loại câu.
7. **Báo cáo:** 4 chỗ `bao_cao_he_thong/`, `Project_Status.md` §4 (số đoạn, vocabulary), guide `full_corpus_rag.md`.
8. **Dọn:** snapshot / bản sao cũ chỉ xóa khi User duyệt.
9. **Sau đợt (Q4):** plan thí nghiệm Qwen3-8B (collection riêng, tầng tìm trước) theo `run-experiment`; session khác review trước khi A duyệt sha.

16 câu hỏi User (`cau_hoi_user.md`): mục nào User chưa trả lời lúc áp thì để nguyên, chuyển đợt 2 — không chặn đợt 1.

## 6. Tiêu chí nghiệm thu

- Mọi mục đợt 1 có trạng thái: đã sửa / bỏ (lý do) / chuyển đợt 2; diff review đạt.
- Chunk 0 lỗi; index khớp build record; runtime khởi động; cổng ổn định đạt.
- Sàn closed-world: 0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật / 500 mới.
- Chất lượng "không làm hỏng" so trước ↔ sau trên 176 câu (số chính = câu tự nhiên + năng lực): Completeness / Accuracy TB ≥ −0,1; số câu tụt
  ≤ A/A + 3 — mỗi câu tụt có giải thích (fact đã sửa / tìm đổi đoạn).
- Tiền thật từ log.

## 7. Quyền và giới hạn

- Sửa curated corpus (User duyệt spec này); Qdrant xóa + tạo lại **đúng một** collection runtime; snapshot trước.
- Paid: `gpt-6-luna` cho đo 176 câu (ước ≈ 0,04 USD, trần đợt 0,10 USD); judge Claude sub-agent. Không OpenRouter (Q4).
- Không đổi chunker / model / prompt; không sửa câu kín.

## 8. Rủi ro

| Rủi ro | Giảm bằng |
|---|---|
| Bản sửa sai (97 / 139 mục C32 chỉ có tự kiểm sub-agent) | B73 đọc lại từng mục; C review diff; mục không chắc chuyển nhóm |
| Bản sửa "chiều theo" Golden (sự cố s7) | đánh dấu riêng, đối chiếu căn cứ trong kho |
| Đoạn vượt token sau sửa | bước 4 chạy trước, dừng nếu vượt |
| Golden lệch kho ⇒ điểm giả | Q5: sửa Golden trước khi đo, User duyệt |
| Chatbot ngừng khi build | snapshot; làm lúc User không dùng; đo thời gian |
