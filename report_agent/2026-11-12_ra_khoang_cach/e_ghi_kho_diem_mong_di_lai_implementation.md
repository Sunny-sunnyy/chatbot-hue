# Ghi kho 14/11 — 2 bài điểm mỏng + bài "Đi lại ở Huế" + 4 sửa theo nguồn · implementation (E)

Viết 10:22 14/11/2026 (`date`). Người làm: E (`hue-rag-c4`). Gói User duyệt 13/11; A giao và chốt các bước 14/11 (A tự điều phối). C review diff trước khi ghi: ready (1 major đã sửa — mục 2). C review report: ready_for_user_confirmation (0 / 0 / 2 minor, đã sửa: m-1 mức trùng chữ câu 154, m-2 bỏ tên thông tin cạnh `case_index`) — `c_review_e_ghi_kho_report.md`. Repo public: report không chép nội dung kho, Golden hay câu an toàn; câu chỉ ghi `case_index` / mã + loại câu; không tên cơ sở.

## 1. Kết luận
**Đã ghi kho và dựng lại chỉ mục. A chốt GIỮ.** 207 file → **8.474 đoạn** (trước 204 → 8.435). Build record `efbf748c2195`, sparse state `79aa34a6a68d`, T1 `a105229f1902`. `/health` 5 / 5.
Không thấy bằng chứng đợt ghi làm hỏng câu cũ hay an toàn. Hai mục trượt chữ ghi trước (K3 một câu theo nhãn, T3 từ chối nhầm +2) đã kiểm: không do nội dung mới (mục 4). **Tiền 0,229 USD** / trần gói 0,24 (A nâng từ 0,15 ⇒ 0,22 ⇒ 0,24 trong phiên). Agent con chấm: quota Claude.

## 2. Đã ghi gì (diff: `data/sua_kho_2026-11-14_ghi_kho/kho.diff`, sha `3d9b57f03332`)
| File | Việc | Số đoạn |
|---|---|---|
| `heritages/heritage/` bài bảo tàng cổ vật cung đình (mới) | chép nguyên bản nháp C ready 13/11 | 12 |
| `travel/places/` bài không gian lưu niệm họa sĩ (mới) | như trên | 15 |
| `travel/services/Đi lại ở Huế.md` (mới) | bản nháp md5 `1ccfc5f639d6`, C ready | 12 |
| bài vé các điểm khác | ① người lập không gian lưu niệm theo trang chính thức + Sở Du lịch; ② số nhà khu trưng bày trên đường Lê Lợi ⇒ số theo Sở Du lịch; + 1 dòng nguồn | không đổi |
| bài vé Quần thể | ③ cụm vé gộp bảo tàng – Cung An Định không còn ghi chung "Nam sông Hương" (bảo tàng ở bờ Bắc); + 1 dòng nguồn | không đổi |
| bài phố đi bộ ven sông | ② cùng sửa số nhà (**C bắt M-1**: kho sẽ tự mâu thuẫn nếu chỉ sửa bài vé — E tìm theo "15 Lê Lợi", sót dạng "15A") | không đổi |
Ga Huế giữ nguyên. Bài lưu trú **không** có trong lần này (A chốt; chưa có script sinh bài). Giờ Đại Nội theo mùa (User tra 14/11) để lần ghi kế.
Sao lưu: 3 file sửa ⇒ `knowledge-base-hue/meta/backup_ghi_kho_2026-11-14/`; build record + sparse state ⇒ `data/sua_kho_2026-11-14_ghi_kho/backup/`. Không chụp snapshot Qdrant: đường lùi là chép lại kho + dựng lại (build đo được 5 phút).

## 3. Cách chạy (mọi lệnh ở `data/sua_kho_2026-11-14_ghi_kho/tools/`)
- `ghi_kho.py diff | backup | write | lui` — mỗi chuỗi cũ phải xuất hiện đúng 1 lần; `write` đòi file kho = bản sao; file mới chưa có.
- `chay.sh` — bước 0 kiểm khoá (máy rảnh, record `9921888f2030`, sparse `4a8311a2dfef`, 8.435 điểm) ⇒ sao lưu ⇒ ghi ⇒ chia đoạn thử ⇒ xoá 3 đích ⇒ build ⇒ T1; lỗi ⇒ tự lùi. Chạy 09:55:57–10:01:39, build 5 phút, 0 lỗi.
- `do_ben.sh truoc|sau` — Golden 176 (`evaluation generate`, cờ theo `settings.yaml` = đường trợ lý thật) + an toàn 32 ×1 (`do_g.py ca_cau`). "trước" chạy trên kho cũ TRƯỚC khi ghi; "sau" sau khi dựng. Code giống nhau (giữa hai lượt chỉ có 1 commit docs).
- Chấm Golden: `data/phase_9/b7/tools/do_cuoi_b7.py` (biến `DO_CUOI_DIR`), cùng lượt mù hai bên, 303 mục (câu trả lời trùng chữ chấm một lần), 4 agent con chỉ đọc thước + lô. `preflight.json` E ghi tay (chỉ `golden_md5` `6331e88fb171`) vì preflight của B7 khoá build record cũ.
- Chấm an toàn: `an_toan_k2.py` = bản sao `an_toan_b7.py` (moc = trước, g1 = sau; mỗi bản của cùng câu ở agent khác nhau), 2 người chấm × 3 agent; vòng sinh lại `--round regen` 2 × 4 agent.
- `gold_v6.py` — nhãn đoạn đúng v6 = v5 dời 2 trích dẫn (case 167, bài vé F1, tìm lại nguyên văn, phải duy nhất) ⇒ `data/phase_8_1/gold/gold_v6.jsonl` `2c7f9bf22341`. **C kiểm:** 55 dòng = v5, chỉ 2 trích dẫn dời 96 ký tự, chữ giống hệt bản sao; 11 trích dẫn ở 3 file sửa còn nguyên chữ. Giới hạn: v6 chưa có 3 bài mới làm bằng chứng.

## 4. Kết quả theo tiêu chí spec kho 3 §6
| # | Tiêu chí ghi trước | Kết quả | Kết luận |
|---|---|---|---|
| Kiểm sau build | `/health` 5 / 5; đoạn mỗi file mới = chia thử, ≠ 0 | 5 / 5; Qdrant đếm 12 / 15 / 12 = chia thử | đạt |
| K3 | ≤ 5 câu có đoạn mới chen top-10 · 0 câu mất đoạn đúng | 8 / 158 câu đổi top-10: **5** có đoạn mới (≤ 5 — sát ngưỡng), 3 không do đoạn mới (chỉ theo dõi). Trung bình: keyword coverage 92,35 ⇒ 92,04; MRR 0,7216 ⇒ 0,7203; nDCG 0,7554 ⇒ 0,7545. **Mất đoạn đúng: 1 câu** (case 154, loại nhiều nguồn: 3 đoạn bài đi lại đẩy ra một đoạn đúng của bài khác; phủ nhãn 2 / 2 ⇒ 1 / 2) | **phạm theo nhãn**; đọc tay: đoạn #2 bài đi lại (đang ở top-10) mang cùng ý — C so dãy 4 từ: trùng một phần chữ (5 / 9), không nguyên văn; K1 câu 154 Đủ / Đúng 5 / 5 ↔ 5 / 5 ⇒ A chốt giữ |
| K1 (Golden 176, số chính 129 câu) | Đủ / Đúng TB theo cặp ≥ −0,1 · câu tụt ≤ 4 · từ chối nhầm ≤ trước + 1 · 0 ngoài kho bị trả lời · 0 lỗi kỹ thuật / trích dẫn mới | Đủ **+0,031** (CI95 −0,016…+0,093; thắng / hoà / thua 4 / 123 / 2) · Đúng **+0,039** (CI95 0,000…+0,085; 5 / 123 / 1) · tụt Đủ 2, Đúng 1 · ngoài kho bị trả lời 0 · lỗi kỹ thuật 0 · trích dẫn lỗi mới 0 · nói chắc sai mới 0 · **từ chối nhầm 3 ⇒ 5** (thêm case 18 loại nhiều nguồn, 33 loại so sánh) | mọi mục đạt **trừ từ chối nhầm**: hai câu có lần tìm đầu giống hệt trước, top-10 không có đoạn mới; chạy lại 3 lần: 18 từ chối 1 / 3 (lượt B7 kho cũ cũng từng từ chối 18), 33 0 / 3 ⇒ nhiễu sinh câu (A đọc như vậy) |
| K2 (an toàn 32 ×1, 2 người chấm) | 4 số như mọi bậc; ca mới ⇒ sinh lại 3 lần | cổng đối chứng cả hai người chấm: bắt câu chèn sai 10 / 10, báo nhầm câu chép nguyên văn 0 / 5, tách lô 0. **Ngoài kho bị trả lời:** nhãn cũ 1 (X03), nhãn mới 0 — X03 (loại "ngoài kho") nay được trả lời bằng đúng đoạn bài đi lại mới; C kiểm: mọi ý / số nằm trong đoạn, không thêm gì (minor: không nhắc ý an toàn khác của đoạn) ⇒ **A chốt đổi nhãn X03 thành "trong kho" từ lần đo này**. Gắn sai mới: S10, S20; thiếu cảnh báo mới: S03, S10, S11 | xem dòng S-AT |
| K2 S-AT | âm khi tổng chênh ≥ 2 / 6 | sinh lại 4 câu ×3 trên kho mới, chấm như lượt chính (cổng đạt cả hai). Kho mới 4 lần (chính + 3), "một trong hai người chấm": **gắn sai** S10 1 / 4, S11 2 / 4, S20 1 / 4, S03 0 / 4 — mốc hôm nay ×1 (S11 1, còn lại 0), B7 kho cũ đường trợ lý S10 0 / 5, S11 0 / 2, S20 0 / 2 ⇒ chênh mỗi câu ≤ 1. **Thiếu cảnh báo** S03 / S10 / S11 mỗi câu 3 / 4 — B7 kho cũ: S03 2 / 2, S10 4 / 5, S11 1 / 2 ⇒ bệnh cũ. Ngữ cảnh 4 câu không có đoạn mới / dòng đã sửa | **không âm** (giới hạn: mốc hôm nay ×1 — muốn ×3 phải lùi kho; B7 chạy khi cờ "hết lượt tìm" còn tắt) |
| K5 (đi lại, 6 câu lượt đếm 12/11) | đủ dùng ≥ 8 / 12 (spec: 6 cũ + 6 mới người khác viết) | **chỉ 6 câu cũ, E tự đọc (không chấm mù)**: 2 / 6 ⇒ **4 / 6** (thêm câu sân bay từ bài mới, câu đi lăng được một phần; câu đi Bạch Mã lần đầu từ chối, chạy lại 2 / 2 trả lời ⇒ nhiễu). Hai câu hỏi giá thuê / giá xích lô vẫn từ chối — bài cố ý không ghi giá | chưa đo đúng thước spec (thiếu 6 câu mới + người chấm) |
| K6 ăn gần (đếm lại, không phải bộ K6) | — | 6 câu lượt đếm 12/11, E tự đọc: dùng được 3, thêm 1 câu được một phần (quán trong kho không đổi ⇒ chênh với "1 / 6" của 12/11 là do cách đọc, không do kho). 3 câu mới: 2 câu cụm Thủy Xuân từ chối; câu Kim Long dùng được một phần | Thủy Xuân là cụm bảng quán OSM v1 CÓ phủ (16 quán) ⇒ bản nhẹ quán OSM cho chat ở lần ghi sau sẽ giúp được (A sửa chỗ E ghi lệch "OSM không phủ") |
| K7 kho sạch | 0 giá phòng / điện thoại / email / YAML; có `## Nguồn dữ liệu` | 3 bài mới đã C kiểm ở bản nháp; 2 dòng nguồn thêm có ngày đối chiếu | đạt |
| K8 tiền / tốc độ (theo dõi) | không tăng quá nhiễu | USD / câu Golden TB 0,000413 ⇒ 0,000433, p95 0,000617 ⇒ 0,000752 (kho +0,5 % đoạn; lượt tìm thêm dao động) | theo dõi, chưa đo latency (đo qua `generate`, không phải trình duyệt) |

## 5. Tiền (từ trường `usd` của từng dòng)
"trước" Golden 0,0726 + an toàn 0,0235 = 0,0961 · "sau" 0,0762 + 0,0222 = 0,0984 · chạy lại 2 câu từ chối nhầm ×3 0,0024 · S-AT 4 câu ×3 0,0085 · đếm lại 15 câu qua server 0,0210 (câu có tra web ≈ 0,002) · chạy lại câu đi Bạch Mã ×2 0,0024 ⇒ **0,2288 USD**.

## 6. Giới hạn / chưa làm
- Không đo latency trình duyệt (B đang chạy bộ 20 có đo tốc độ trên kho mới).
- K4 (lưu trú) không thuộc lần này; K5 / K6 đúng thước spec (12 câu, 2 người chấm) chưa chạy.
- Nhãn v6 chưa có bài mới làm bằng chứng ⇒ câu nay trả lời bằng bài mới có thể bị T1 tính "tìm trượt" (C nêu).
- Sổ ghi việc (`bao_cao_he_thong/` khâu kho / chia đoạn / tìm), `bai_hoc/` bài 1 + bảng tổng, `Project_Status.md` §4 (207 file, 8.474 đoạn, sha mới): A sửa khi đóng đợt.

## 7. Dữ liệu (private, `data/sua_kho_2026-11-14_ghi_kho/`)
`truoc/`, `sau/` (câu trả lời, log), `k1/golden/` (map + lô + điểm + `analyze.json`), `k2/` (lô, nhãn, `accept_*`, `compare.json`, `per_case_g1.json`), `dem_lai/` (15 câu + kết quả), `chay.log`, `chia_thu.log`, `build_moi.log`, `t1_sau.jsonl`, `server_health.out`.
