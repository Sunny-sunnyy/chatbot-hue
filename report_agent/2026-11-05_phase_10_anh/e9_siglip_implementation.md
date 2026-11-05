# Implementation Report: Phase 10 E9 — thí nghiệm P2 SigLIP 2 (chạy trên máy) cho "hỏi bằng ảnh"

Người làm: E (Claude Opus 5.5, `hue-rag-bc`) · việc **E9** (A giao, phiên tối 05/11)
Date: 20:17 05/11/2026 (`date`)
Tiêu chí ghi trước: `data/phase_10/anh/e9/tieu_chi_ghi_truoc.md` **`a8524989f221`** (11:43 05/11/2026, trước mọi lượt đo). Spec Phase 10 bản 2 `bf67b90fb6fc` §5; User duyệt tải SigLIP 2 + collection ảnh mới (11:42 05/11/2026).
Code chạy: `p10-anh` `973823f` (= phần ảnh đã merge `main` `2ca9937`), worktree `/tmp/e_anh`; script thí nghiệm ở `data/` (private) — **không có code mới vào repo**.

## 1. Kết luận

**ÂM theo tiêu chí ghi trước — cả ba phương án** (đạt ⇔ Q-a ≥ 22 / 25 **và** Q-c ≤ 1 / 5, luật A/A: cả hai lượt). Không phương án nào thay P1 luna v1 (đang ở `main`, cờ tắt).
Không chạy vòng chỉnh (tiêu chí cho ≤ 2 vòng) — lý do có số đo ở §4.

| Phương án | Q-a (≥ 22/25) | Q-c bị ép (≤ 1/5) | Q-d theo lệnh (≤ 1/3) | Q-b top-1 | Q-e đổi giữa 2 lượt | ms / ảnh p50 · p95 | USD 2 lượt |
|---|---|---|---|---|---|---|---|
| **P2a** zero-shot chữ ("Ảnh <tên>, Huế, Việt Nam") | 5 · 5 ✗ | 5 · 5 ✗ | 0 · 0 ✓ | 4 | 0 / 33 | 278 · 337 (CPU) | 0 |
| **P2b** k-NN ảnh mẫu (Qdrant) | 20 · 20 ✗ (công trình 9/13, cảnh 3/4, món 6/6, biển tên 2/2 — từng loại đạt) | 5 · 5 ✗ | 0 · 0 ✓ | 15 | 0 / 33 | 253–278 · 308–337 (CPU) | 0 |
| **P2c** P2b top-5 ⇒ luna v1 chọn | 21 · 19 ✗ | 1 · 3 ✗ | 0 · 1 ✓ | 21 · 19 | **12 / 33** | 3.299–3.647 · 7.302–7.325 | **0,015681** |
| *(mốc)* P1 luna v1 — A2, cùng bộ, không chạy lại | 22 · 22 ✓ | 0 · 2 ✗ | 1 · 1 ✓ | 21 · 21 | 6 / 33 | 2.959–3.173 · 6.780–7.688 | 0,026456 |

## 2. Đã làm

- **Ảnh mẫu (k-NN):** tải nốt vòng Commons (`tools/tai_anh.py`) ⇒ **172 ảnh / 40 tên** (≤ 5 / tên; 2 tên trong danh sách 42 không có ứng viên). 5 tên tải dở thiếu `phieu_nguon.jsonl` (nguồn tra theo thứ tự dòng `e9/mau/<id>.txt`); 1 tên chỉ 2 ảnh (Commons giữ > 15 phút ⇒ bỏ). Ảnh mẫu **chưa ai xem tận mắt**.
- **Kiểm lớp 2 (không trùng ảnh đo):** `e9/kiem_trung.py` `30d124ce3a89` — sha256 byte + tên file Commons chuẩn hoá, so 36 ảnh của bộ đã thấy (33 + 3 ảnh chữ ra lệnh) ⇒ **0 trùng** (`e9/kiem_trung_ket_qua.json`). Lớp 1 (tên file) đã làm lúc tìm (`tim_mau.py`). Giới hạn: không bắt ảnh gần giống (cắt / đổi cỡ từ nguồn khác).
- **Nạp:** `e9/e9.py nap` (`e9.py` `d107b7909011`; thêm 1 chỗ: đọc kết quả lớp 2 để bỏ ảnh trùng) ⇒ collection Qdrant **`hue_anh_siglip2`** 172 điểm, 768 chiều, cosine. Collection chatbot `hue_full_corpus_7a2_e5_small_384` không đụng.
  **τ chọn trước, không nhìn bộ đo** (luật ghi trước): leave-one-out trên ảnh mẫu, phân vị 10 % ⇒ `tau_b` 0,582 · `tau_a` 0,067 (`e9/tau.json` `f38deed91f79`).
- **Đo:** `e9.py do lap1|lap2` (P2a + P2b), `e9.py ket_hop lap1|lap2` (P2c, có phí, A duyệt ≈ 0,027) ⇒ chấm `tools/do_a2.py cham` (cùng luật nhãn A2, nhãn md5 `1f37c7f11821`). Kết quả thô `data/phase_10/anh/e9/p2{a,b,c}_lap{1,2}.jsonl`.

## 3. Số máy (SigLIP 2 base `google/siglip2-base-patch16-224`)

Model trên đĩa 1,5 GB · nạp 2,8–4,8 s · RSS đỉnh tiến trình **1.642 MB** · ms / ảnh (thu nhỏ + embed + truy vấn Qdrant, CPU 6 luồng) p50 253–278, p95 308–337. P2a / P2b **tất định**: hai lượt giống hệt (0 / 33). Ảnh **không rời máy** ở P2a / P2b.

## 4. Quan sát (đã chứng minh từ dữ liệu) và vì sao không chỉnh

- **P2b không biết "không nhận ra":** điểm top-1 của 5 ảnh ngoài danh sách 0,688–0,889 nằm **trong** khoảng của 25 ảnh trong danh sách 0,713–0,956 ⇒ τ 0,582 không loại ảnh nào. [Chẩn đoán trên bộ đo, **không** dùng để chọn τ:] muốn Q-c ≤ 1 / 5 cần τ > 0,841 ⇒ 11 / 25 ảnh trong danh sách rơi dưới ngưỡng ⇒ Q-a ≤ 14. ⇒ chỉnh τ không cứu được.
- **P2c bị chặn trần bởi P2b:** top-5 của P2b chứa tên đúng ở **22 / 25** ảnh = đúng ngưỡng ⇒ luna phải đúng hết ở cả hai lượt; luna đổi tập ứng viên ở **12 / 33** ảnh giữa hai lượt (A2 v1: 6) ⇒ chỉnh lời dặn chỉ dời lỗi Q-a ↔ Q-c như A2.
- **P2a** (vector chữ tiếng Việt): gần như ngẫu nhiên (5 / 25; một tên bị kéo lên top-1 cho hầu hết ảnh công trình) ⇒ SigLIP 2 base không hiểu mô tả tên riêng Huế bằng chữ; đổi câu mẫu khó đưa 5 ⇒ 22.
- Sai lặp lại cả P2b lẫn P2c: chùa / lăng / điện Huế lẫn nhau (cùng kiểu mái, sân); Ngọ Môn Bắc Kinh, cổng Văn Miếu Hà Nội bị gán tên Huế — giống A2 ⇒ củng cố giả thuyết A2 "lỗi gốc là nhận dạng".

## 5. Lỗi và giới hạn

- P2c: mỗi lượt **1 lần quá hạn 20 s** (`GenerationError`) — luật chấm tính là "không nhận ra" ⇒ 1 trong 2 ca đó được chấm đúng (lạc quan); `CallLog` ghi 0 USD cho lần quá hạn ⇒ tiền thật có thể cao hơn số log ≤ ~0,0008.
- Ảnh mẫu Commons ít, góc chụp đẹp (khác ảnh người dùng chụp); 5 tên thiếu phiếu nguồn; chưa xem tận mắt.
- Không có ảnh ngoài danh sách để hiệu chỉnh τ (đã ghi trước là giới hạn).
- Bộ đo nhỏ (25 + 5 + 3), một bộ đã thấy — cùng giới hạn A2.

## 6. Tiền

P2c 0,007871 + 0,007810 = **0,015681 USD** (log `CallLog`; ước trước 0,027). **Tiền Phase 10: 0,080179 + 0,015681 = 0,095860 USD** / trần 0,15 (dừng 0,13). P2a / P2b / nạp / kiểm trùng: 0 USD.

## 7. Bàn giao / cần quyết (A ⇒ User)

- Tiêu chí gốc: không phương án nào đạt ⇒ đề xuất **giữ P1 luna v1 dạng gợi ý có xác nhận** (User đã chọn) và không đưa SigLIP vào chatbot.
- Điểm đáng cân nhắc nếu User muốn dùng thước "gợi ý có xác nhận" (không tự áp): P2b **0 USD, ~0,3 s / ảnh, ảnh không gửi ra ngoài**, Q-a 20 / 25 (luna v1 22 / 25), nhưng **luôn gợi tên** cả cho ảnh con mèo ⇒ cần User quyết có chấp nhận không.
- Dọn: collection `hue_anh_siglip2` (172 điểm, thí nghiệm) — giữ tới khi User quyết, xoá cần duyệt; worktree `/tmp/e_anh` + symlink.
- **Giải thích ngắn:** thử một model nhận ảnh chạy ngay trên máy (không tốn tiền, nhanh gấp ~10 lần) theo ba cách; cách tốt nhất gần bằng cách hiện tại về đoán đúng tên nhưng không biết nói "không nhận ra"; ghép với luna cũng không qua ngưỡng ⇒ giữ cách hiện tại.
