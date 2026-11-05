# Plan: sửa kho nhỏ — giờ mở cửa 11 điểm Quần thể (C190, bản 2)

C viết 11:48 05/11/2026 (`date`), A giao (User duyệt phạm vi 05/11). Bản trình duyệt. **Chỉ chạy SAU khi B5 merge.** Plan nhỏ ⇒ A đọc rồi duyệt, không có vòng review.
Căn cứ: `data/kiem_kho_thieu_2026-11-05/c189_ket_qua.md` §3–§4 · `guides/full_corpus_rag.md` mục "Build lại index khi corpus đổi" · `Session_Prompt.md` §5 (sửa kho) · lần sửa kho trước `data/sua_kho_2026-10-27/` (công cụ `tools/apply_edits.py`, đo trước ↔ sau `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b9_*`).

## 1. Nguồn giờ — A quyết 05/11 (sau phát hiện lúc soạn)

- **Phát hiện:**
  - Dữ liệu mở (`…/raw/Danh-sach-dia-diem-di-tich-van-hoa-…_1726311601.json`, trường `mocua` / `dongcua`; bản chụp 14/09/2024 theo dấu thời gian tên file) ghi 07:00 – 17:00.
  - Kho đã có giờ chung **07h00 – 17h30** (file vé Quần thể trong `travel/tickets/`, phần quy định khung giờ; nguồn của file đối chiếu ngày 23/10/2026).
  - Chèn giờ dữ liệu mở ⇒ kho tự mâu thuẫn.
- **A quyết:**
  - Không tra web, không dùng giờ dữ liệu mở (bản 2024, đã cũ).
  - Chèn giờ chung **07h00 – 17h30** đã có trong kho, kèm câu "giờ có thể thay đổi theo mùa / sự kiện".
  - Nguồn là chính kho ⇒ không phải đổi phạm vi lớn. A báo User.
- **Bỏ:**
  - Chợ Đông Ba: kho đã có giờ chi tiết hơn.
  - **Kinh thành Huế:** không thuộc Quần thể (`quan_the: false` trong bảng B5; quảng trường Ngọ Môn – Kỳ Đài mở tự do, kho đã ghi) và không có nguồn giờ riêng.

## 2. Danh sách — 11 file di tích (mỗi điểm có mục vé riêng trong file vé), thư mục `heritages/heritage/` của kho

Đại Nội Huế · Cung An Định · Đàn Nam Giao · Điện Hòn Chén · Lăng Tự Đức · Lăng Dục Đức · Lăng Đồng Khánh · Lăng Thiệu Trị · Lăng Khải Định · Lăng Minh Mạng · Lăng Gia Long.
- **Ghi chú:** A nghĩ Cung An Định nằm ngoài Quần thể. C kiểm qua `grep_kb.sh`: file vé có mục riêng cho Cung An Định (bảng giá vé lẻ + vé gộp với Bảo tàng Cổ vật), bảng B5 ghi `quan_the: true` ⇒ **giữ**. Điểm nằm ngoài Quần thể là Kinh thành, nên bỏ Kinh thành theo đúng logic của A.
- **Chữ chèn (giống nhau ở 11 file):** `- **Giờ mở cửa:** 07h00 – 17h30 hằng ngày, theo khung giờ tham quan chung của Quần thể Di tích Cố đô Huế; giờ có thể thay đổi theo mùa hoặc sự kiện.`
- **Nguồn:** `- Giờ mở cửa theo khung chung của Quần thể Di tích Cố đô Huế (đối chiếu ngày 23/10/2026): <URL>`. URL lấy từ mục nguồn của file vé đã đỡ dòng giờ; không xác định được URL ⇒ ghi tên file vé.

## 3. Cách sửa (theo khuôn kho: không frontmatter, nguồn ở "## Nguồn dữ liệu")

- **Hiện trạng (C đếm qua `scripts/grep_kb.sh`, 11:50 05/11):** cả 11 file **0 dòng giờ**. 10 / 11 file có `## Thông tin dành cho du khách` (Cung An Định không có). Chỉ Lăng Tự Đức có `## Nguồn dữ liệu`.
- **Chỗ chèn:** cuối mục `## Thông tin dành cho du khách` ⇒ thêm 1 gạch đầu dòng `- **Giờ mở cửa:** … (theo …)`. Cung An Định: thêm mục này ở cuối file, trước mục nguồn.
- **Nguồn:** thêm 1 dòng `- Giờ mở cửa … (đối chiếu ngày dd/mm/2026): <URL>` (cách ghi sẵn có của kho) vào `## Nguồn dữ liệu`. 10 file chưa có mục này ⇒ thêm mục ở **cuối file**.
- **Áp bằng máy:** viết `edits.jsonl` (`old` / `new`, mỗi `old` xuất hiện đúng 1 lần) và áp bằng cách của `data/sua_kho_2026-10-27/tools/apply_edits.py`.
  - Chạy thử trong bộ nhớ trước.
  - `--write` chỉ chạy khi đã có bản sao.
  - Diff để ở `data/sua_kho_2026-11-05_gio/` (private).
- **Sao lưu:** copy 11 file gốc (giống byte) vào `knowledge-base-hue/meta/backup_gio_mo_cua_2026-11-05/` trước khi ghi.
- Kiểm `knowledge-base-hue/meta/full_corpus_conditions.json`: không điều kiện nào trỏ vào đoạn bị sửa (có ⇒ sửa cùng lúc).

## 4. Dựng lại chỉ mục (guide "Build lại index", cách (a) tại chỗ như sửa kho 27/10 — A trình User vì chatbot ngừng trong lúc build)

1. Chia đoạn thử, chỉ đọc: `chunk_full_corpus()` 0 lỗi; đoạn bị sửa ≤ 256 token huydang.
2. Sao lưu đích cũ: Qdrant snapshot `hue_full_corpus_7a2_e5_small_384`, kèm build record và `full_corpus_sparse_state.json`, cất ở `data/sua_kho_2026-11-05_gio/backup/`.
3. Xoá đủ cả ba (collection, build record, **sparse state cũ**), rồi từ `backend/`: `uv run python -m ingestion.full_corpus_pipeline build --candidate e5-small-384`.
   - e5 chạy CPU, không tốn tiền.
   - Một việc nặng một lúc, có `timeout`, không chạy cùng lượt đo tốc độ (W31).
4. Kiểm sau build: summary JSON, `/health` 200, số point ghi vào báo cáo.

## 5. Đo lại (tiêu chí ghi trước)

| Đo | Cách | Sàn |
|---|---|---|
| T1 retrieval 158 câu, trước ↔ sau (0 USD) | như B81 / B9: top-10 + đoạn đúng trong ngữ cảnh | 0 câu **không chạm** 11 file bị mất đoạn đúng |
| Golden rút gọn (có phí) | câu Golden có trích dẫn đúng nằm trong 11 file + smoke 10, sinh lại, chấm mù trước ↔ sau | không câu nào tụt Completeness / Accuracy > 1 điểm mà không giải thích được bằng dòng giờ |
| An toàn rút gọn (có phí) | bộ an toàn 32 câu, chấm như Phase 9 | 0 lỗi mới so với lượt đã có |
| 1 câu thật | "Lăng Tự Đức mở cửa mấy giờ?" qua API server | trả đúng giờ đã ghi, có trích dẫn file lăng hoặc file vé; không từ chối |

## 6. Tiền, dừng, đường lùi

- **Trần ≈ 0,03 USD.** Dừng khi chạm 0,025 USD. Ước tính: Golden rút gọn ≈ 30 câu × 0,0002 + an toàn 32 câu × ≈ 0,0003 + 1 câu thật ≈ **0,016 USD**. Judge dùng sub-agent (quota Claude).
- **Dừng khi gặp một trong các điều kiện sau:**
  - B5 chưa merge;
  - A chưa chọn hướng ở §1;
  - một `old` không xuất hiện đúng 1 lần;
  - chunker báo lỗi hoặc vượt token;
  - build dừng ở bước kiểm đích;
  - `/health` ≠ 200;
  - phạm sàn ở §5;
  - đang có lượt đo tốc độ của Phase 9.
- **Đường lùi:** chép 11 file từ bản sao, xoá collection mới, khôi phục snapshot cùng build record và sparse state đã cất. Xoá bản sao / snapshot chỉ khi User duyệt.
- **Báo cáo:** báo cáo khâu kho + nhật ký ngày (luật 3 chỗ, `1d1fa77`), tiền ghi ngay sau mỗi lượt.
- **Việc kế (ngoài đợt này):** cột `gio_mo_cua` của bảng `diem_v3.json` (B5) có thể lấy giờ riêng từng điểm. Đó là việc của B, sau đợt này.
