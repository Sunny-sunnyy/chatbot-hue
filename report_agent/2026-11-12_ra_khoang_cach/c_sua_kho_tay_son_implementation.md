# Sửa kho — năm Tây Sơn đóng đô (C, 15/11/2026)

User duyệt "ghi cả hai mốc" (qua A, 15/11). Đếm + nguồn: `c_kho_mau_thuan.md`. Review diff: `e_review_tay_son.md` (ready sau 1 minor ngữ pháp). Hồ sơ: `data/sua_kho_2026-11-15_tay_son/` (`TIEU_CHI.md` ghi trước, `kho.diff`, `chay.log`, `cau_cham.json`, `tools/`).

## Đổi gì
- 2 câu ở 2 bài di tích lớn: trước một bài ghi giai đoạn kinh đô Tây Sơn bắt đầu 1786, bài kia 1788.
- Nay cả hai cùng ghi hai mốc: 1786 (chiếm Phú Xuân) và kinh đô 1788 (lên ngôi) – 1801. Không chép nguyên câu kho vào file tracked.
- Không thêm / bớt file.
- Sao lưu: `knowledge-base-hue/meta/backup_sua_kho_2026-11-15_tay_son/` + record / sparse cũ ở `backup/`.
- Quét trùng bản nháp (`.githooks/overlap_scan.py`): 0 dòng trùng Golden / câu kín.

## Chạy [đã chạy]
- `tools/chay.sh` (theo mẫu ghi kho lần 6 của B; bước 0 kiểm khoá; tự lùi nếu lỗi), 11:15–11:22 15/11/2026, cả nhóm được báo trước / sau:
  - chia đoạn 9.425 đoạn · 263 file;
  - Qdrant **9.425 point**;
  - record `af5e225c497e` ⇒ **`1b53af26b662`**, sparse `4888dc70d01f` ⇒ **`ccd1d3ae36ec`**.
- T1 sau = **`aa34d4215f15`**, giống hệt mốc: top 10 của 158 / 158 câu không đổi.
- Câu chạm (`tools/cau_cham.py`): 0 câu đổi top 10, **0 câu có đoạn đã sửa trong top 10**.
  - Hai đoạn sửa: Kinh thành #11, Quần thể #9.
  - ⇒ Ngữ cảnh gửi model của mọi câu Golden giống trước (lần tìm đầu; lần tìm thêm không kiểm) ⇒ không chạy lại Golden.
- **Lệch tiêu chí đã sửa:** `TIEU_CHI.md` ghi "0 câu chạm ⇒ an toàn 32 + 18 ngoài kho + 2 câu thử"; C lúc đầu bỏ an toàn + ngoài kho. Kiểm độc lập bắt ⇒ chạy bù 11:33–11:35 (`sau/`, HEAD `644899e`): **ngoài kho 0 / 18 bị trả lời, 0 lỗi (0,0046 USD) · an toàn 32: 0 lỗi, 0 đổi lớp so với lượt kho 6 (0,0218 USD)** — ĐẠT.
- Hỏi thử 2 câu (lõi trợ lý thật, tắt tra web): xem mục dưới.
- **Hỏi thử 2 câu** (`tools/hoi_thu.py`, `TAT_WEB=1`, `hoi_thu_sau.jsonl`, 11:30 15/11/2026, 0,00089 USD):
  - câu hỏi năm Phú Xuân thành kinh đô Tây Sơn ⇒ "từ năm 1788, khi Quang Trung lên ngôi", trích bài Kinh thành;
  - câu hỏi trước nhà Nguyễn Phú Xuân là kinh đô của ai, bao giờ ⇒ "triều Tây Sơn từ năm 1788 đến năm 1801", trích cả hai bài.
  - **Đối chiếu tiêu chí ghi trước: PARTIAL.** Hai câu trả lời đúng và khớp giữa hai bài (không còn mốc trái nhau). Nhưng tiêu chí đòi "có cả hai mốc", mà câu trả lời chỉ nêu 1788: câu hỏi hỏi năm *kinh đô*, model trả đúng mốc đó, không nhắc 1786 (năm chiếm thành). Không có lượt "trước" để so (không chạy trước khi sửa).
  - Không sửa thêm: câu trả lời đúng sự thật. Ghi lại để A / User quyết có cần không.

## Tiền
≈ 0,029 USD: Serper 2 lượt lúc tra nguồn 0,002 + 2 câu hỏi thử 0,00089 + chạy bù an toàn 0,0218 + ngoài kho 0,0046. Dựng chỉ mục, T1, đếm câu chạm 0 USD.

## Lùi (nếu cần)
`python3 -I tools/ghi_kho.py lui` rồi dựng lại (`chay.sh` có hàm `lui`); record / sparse cũ ở `backup/`.
