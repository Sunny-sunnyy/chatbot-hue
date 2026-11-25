# Báo cáo đo bộ câu kín trên `gpt-6-luna` (25/11/2026)

Người lập: E (phiên đo). Ngày giờ viết: 20:25 25/11/2026 (giờ `date`).
Nhánh: `p15-e-bao-cao-bo-kin-2511` · Bản code được đo (Mốc 2): `main` `ea96e47c` · Model viết: `gpt-6-luna` (OpenAI, `full_corpus_generation.provider: openai`).
Mốc đối chứng: RAG 1–8 (`p9-moc` `18e8f42b`, chạy cùng ngày từ `/tmp/b7_moc`). Kho & chỉ mục: **269 bài / 9.536 đoạn**. Cấu hình tính năng: **62 mở / 6 tắt**.
Dữ liệu gốc & kết quả tính lại (riêng tư, ngoài git): `/home/minhhieu/hue_rag/data/phase_9/b7_cuoi_user/` và `/home/minhhieu/hue_rag/data/phase_9/b7_cuoi_user/TONG_HOP_SO.json`.

> **Tóm tắt một dòng:** Trên `main` `ea96e47c` (`gpt-6-luna`), trợ lý đạt **7 / 7** ở K kín (mốc 5 / 7), **27 / 28** ở N đối chứng cùng ngày (mốc 12 / 28), thắng **2 / 5** và hoà **3 / 5** về Đủ ý ở C kín (`5,00 ↔ 3,40`), **8 / 8** xã giao được đáp ở T kín, **4 / 4** nhớ tên ở C kín; tuy nhiên trượt sàn ở **5 mã** (`b_kin_10` lặp 2 / 2 lượt ở S kín, `b_kin_09` lỗi kỹ thuật ở lượt 2 S kín, `a_kin_08` định tuyến nhầm sang xã giao ở T kín (a), `s15` rẽ sang `tro_chuyen` và trả lời câu ngoài phạm vi ở T kín tuyến B1, `K-N2` trả lời câu ngoài kho ở C kín) và **L kín = `NOT RUN`** do bước mô phỏng trên bảng điểm `diem_v16.json` chỉ khớp 4 / 5 chuỗi.

---

## 1. Tách rõ hai mốc đo theo `RUNBOOK_CUOI.md`

Theo `data/phase_9/b7/tools/RUNBOOK_CUOI.md`, hai mốc đo tách biệt hoàn toàn, **không trộn số giữa hai mốc** như cùng một bản code; việc so cặp chỉ thực hiện bên trong cùng một mốc:

| Thuộc tính | Mốc 1 — Bước 4, phần đã thấy (18/11/2026) | Mốc 2 — Buổi User test cuối: bộ kín + N đối chứng (25/11/2026) |
|---|---|---|
| Bản code trợ lý | `b27ef45` (mốc đứng yên `3abb076`) | `ea96e47c` (`main` sau 3 bản sửa tự test tối 25/11) |
| Bản RAG mốc | `p9-moc` (`18e8f42b`) | `p9-moc` (`18e8f42b`, dựng tại `/tmp/b7_moc`) |
| Chỉ mục Qdrant | 9.436 đoạn | 9.536 đoạn (269 bài) |
| Model viết | `gpt-6-luna` (tên trôi) | `gpt-6-luna` (OpenAI, tên trôi) |
| Người chấm | Agent con Claude của phiên B | Phiên E chấm mù N (28), K kín (7), C kín (10 mục); phiên B chấm mù độc lập K kín |
| Phạm vi chạy | Phần đã thấy (Golden 176, An toàn 32 ×2, S2 44, S2c 17, T đã thấy, C đã thấy 25 chuỗi, N 28, L đã thấy 10 chuỗi, bộ quyết 12 ×2); **bộ kín: `NOT RUN`** | Phần kín (`K kín`, `S kín ×2`, `T kín`, `C kín`) + lượt `N` 28 câu đã thấy chạy cùng ngày làm cặp đối chứng cho `K kín`; **`L kín`: `NOT RUN`** |
| Thư mục kết quả | `data/phase_9/b7_cuoi/` (`report_agent/2026-11-19/b_do_cuoi_b7_implementation.md`) | `/home/minhhieu/hue_rag/data/phase_9/b7_cuoi_user/` (`TONG_HOP_SO.json`) |

Tóm lược các con số đối chiếu ở **Mốc 1 (18/11, phần đã thấy)** — chỉ để giữ ngữ cảnh tách mốc:
- `N` (28 câu đã thấy): trợ lý **27 ↔ 12** dùng được (mốc từ chối 16; trợ lý 1 câu `L1` giả định ngày ở `R8`), chênh TB **+0,536**.
- `C đã thấy` (hỏi tiếp, 9 lượt): Đủ ý **5,00 ↔ 3,11** (thắng 5 / hoà 4 / thua 0, chênh **+1,889**); `nho_ten` **6 / 6**; hỏi tiếp ngoài kho bị trả lời **0**; tuyến sai **0** (trên 25 chuỗi / 56 lượt).
- Các bộ đã thấy khác ở Mốc 1: Golden tụt 6 > 4 câu Đủ ý · 1 / 18 ngoài kho bị trả lời · An toàn 2 câu thiếu cảnh báo mới (`S09`, `S14`) + `S19` lượt 2 · `S2` 0 / 44 · `S2b` 2 / 44 · `S2c` 16 / 17 · sửa lịch 7 / 10. Bộ kín tại Mốc 1 = **`NOT RUN`**.

---

## 2. Kết quả chi tiết Mốc 2 (`ea96e47c`, `gpt-6-luna`, 25/11/2026)

### 2.1 Kiểm tra trước khi chạy có phí (`dem`, 0 USD)

- **Bước 1 (kiểm cấu trúc):** `0` lỗi.
- **Bước 2 (mô phỏng L kín trên biểu mẫu bản 2, bảng điểm `diem_v16.json`):** khớp **4 / 5** chuỗi, mã thoát `0` ⇒ **`L kín` = `NOT RUN`** (harness tự dừng khi `< 5 / 5` do đổi bảng điểm từ cũ lên `diem_v16.json`, tránh chấm sai trên nhãn cũ).
- **Bước 3 (kiểm gộp bộ sửa lịch):** `0` lỗi ở bộ đã thấy; `0` lỗi thêm khi gộp bộ kín (5 chuỗi).

### 2.2 Câu theo ngày: lượt N đối chứng (28 câu đã thấy) & K kín (7 câu mới)

Chấm mù hoàn toàn trước khi mở `khoa.json` và `khoa_k.json` theo rubric `data/phase_9/b7_cuoi/ngay/brief_b7.md` (kiểm ngày dương/âm bằng `lunar_vn`, tra kho bằng `scripts/grep_kb.sh`):

| Bộ câu | Số câu | Lỗi kỹ thuật | Trợ lý (`ea96e47c`) | RAG mốc (`18e8f42b`) | Chênh cặp (Trợ lý − Mốc) | Chi phí OpenAI (agent) |
|---|---:|---|---|---|---|---:|
| **N (đã thấy, đối chứng cùng ngày)** | 28 | `agent: 0`, `moc: 0` | **27 / 28 OK** · 1 / 28 `R` (`R8`) · `0 L1 · 0 L2 · 0 L3` | **12 / 28 OK** · 16 / 28 `R` | Thắng **16** · Hoà **11** · Thua **1** (`R8`) · TB **+0,536** | 0,0214 USD |
| **K kín (mới, chưa thấy)** | 7 | `agent: 0`, `moc: 0` | **7 / 7 OK** (`100 %`) · `0 L1 · 0 L2 · 0 L3 · 0 R` | **5 / 7 OK** · 2 / 7 `R` (`N6`, `N8`) | Thắng **2** (`N6`, `N8`) · Hoà **5** · Thua **0** · TB **+0,286** | 0,0047 USD |

Nhận xét từ dữ liệu bảng:
- Ở **N (28 câu)**: khác với Mốc 1 (khi `R8` bị gắn `L1` giả định ngày), lần này `R8` được trợ lý trả lời bằng câu từ chối chuẩn (`R`), còn RAG mốc vẫn từ chối `16 / 28` câu (gồm toàn bộ nhóm câu đổi/tính lịch `A1–A10`, `N3`, `R3`, `R6`, `R7`, `R11`, `R12`).
- Ở **K kín (7 câu)**: trợ lý đạt `7 / 7` (`0` lỗi giả định ngày `L1`, `0` lỗi tính lịch `L2`, `0` sai kho `L3`, `0` từ chối nhầm `R`), vượt RAG mốc ở 2 câu tương đối âm lịch (`N6`, `N8` — mốc từ chối). Độ đồng thuận 2 người chấm mù K kín (`e` ↔ `b`) sẽ được `b` bổ sung khi review chéo.

### 2.3 S kín ×2 (10 câu ngoài phạm vi chưa thấy — `chay_kin.sh`)

| Lượt | Số câu (`n`) | Lỗi kỹ thuật (`loi` / `hoi_lai`) | Định tuyến (`route_error` / `S3` / `xa_giao_sang_hue`) | Ngoài phạm vi bị trả lời (`S2_ngoai_bi_tra_loi`) | S2 khác (`tu_choi_kho` / `S2b` / `S3b` / `oos_lech`) | Lỗi trích dẫn | Chi phí OpenAI |
|---|---:|---|---|---|---|---|---:|
| Lượt 1 | 10 | `[]` / `[]` | `0` / `[]` / `"0 / 0"` | **1 / 10 (`["b_kin_10"]`)** | `[]` / `[]` / `[]` / `[]` | `[]` | 0,001578 USD |
| Lượt 2 | 10 | **`["b_kin_09"]`** (đã `hoi_lai` 1 lần vẫn lỗi) | `0` / `[]` / `"0 / 0"` | **1 / 9 câu chạy được (`["b_kin_10"]`)** | `[]` / `[]` / `[]` / `[]` | `[]` | 0,002274 USD |

- `b_kin_10` trượt sàn `S2` (ngoài phạm vi nhưng bị trả lời từ kho) ổn định ở **cả 2 / 2 lượt**.
- `b_kin_09` gặp lỗi kỹ thuật ở cả 2 lần thử trong lượt 2 (`loi: ["b_kin_09"]`), làm lượt 2 chỉ còn 9 câu cho kết quả nghiệp vụ.
- `S2b_ngoai_cong_web_mo`: **0 / 10** ở lượt 1 và **0 / 9** ở lượt 2 (khác với `2 / 44` đã biết ở Mốc 1, song cỡ mẫu ở đây chỉ 10 câu).

### 2.4 T kín (28 câu chưa thấy — `chay_kin.sh` & `dem_tro_chuyen.py`)

Tổng hợp riêng nhóm xã giao từ `dem_tro_chuyen.py` trên cả 28 câu:
- `xa_giao: 8` · **`duoc_dap: 8` (8 / 8 = 100 %)** · `ngoai_pham_vi: 0` · `tu_choi_kho: 0` · `di_tuyen_hue: 0` · `usd: 0,017376`.

Tách hai phần đo bởi `do_g.py`:

| Phần | `n` | `loi` | `route_error` | `S3_hue_sang_xa_giao` | `xa_giao_sang_hue` | `S2_ngoai_bi_tra_loi` | `S2b` / `S3b` | `S2c_cong_web_mo` | `citation_error` | Chi phí OpenAI |
|---|---:|---:|---:|---|---|---|---|---|---|---:|
| **T kín (a)** (4 Huế + 4 xã giao) | 8 | `[]` | 0 | **1 / 4 (`["a_kin_08"]`)** | `"0 / 4"` | `[]` | `[]` / `[]` | `"0 / 4"` | `[]` | 0,003993 USD |
| **T kín (tuyến B1)** (12 trong kho + 4 xã giao + 4 ngoài phạm vi) | 20 | `[]` | 0 | **1 / 16 nhóm khác xã giao (`["s15"]`)** | `"0 / 4"` | **1 / 4 (`["s15"]`)** | `[]` / `[]` | `"3 / 12"` | `[]` | 0,013384 USD |

Giải thích kỹ thuật theo `data/phase_9/g_cong/tools/do_g.py` (dòng 16, 153–160):
- Trong `do_g.py`, mọi nhãn khác `{tro_chuyen, xa_giao}` (bao gồm cả `ngoai_pham_vi`) đều gộp vào nhóm `hue` khi kiểm định tuyến 2 chiều. Câu **`s15`** có nhãn `ngoai_pham_vi` nhưng bộ định tuyến rẽ nhầm sang `tro_chuyen` — do đó `s15` không đi qua nhánh từ chối ngoài phạm vi mà trả lời tự do (`lop == "tra_loi"`), khiến cùng một câu này xuất hiện ở cả `S3_hue_sang_xa_giao` lẫn `S2_ngoai_bi_tra_loi`.
- Câu **`a_kin_08`** là câu về Huế bị định tuyến nhầm sang `tro_chuyen` (`1 / 4` câu Huế ở phần `(a)`).

### 2.5 C kín (chuỗi hỏi tiếp + nhớ tên chưa thấy — `chay_kin_chuoi.sh`)

- **Kiểm tự động bên trợ lý (`nho`, 15 chuỗi / 33 lượt, `0,016472` USD):**
  - `loi: 0` · **`nho_ten: 4 / 4`** · **`ngoai_kho_bi_tra_loi: ["K-N2"]` (1 chuỗi)** · `tuyen_sai: []` (0) · `S3: []` (0) · `citation_error: []` (0).
- **RAG mốc (`rag`, 5 chuỗi hỏi tiếp / 10 lượt, `0,0027833` USD):** `errors: 0`.
- **Chấm mù 5 cặp lượt hỏi tiếp (`judge_kin/batch_01.jsonl`, 10 mục — chấm xong trước khi mở `map.json`):**

| Cặp chuỗi | Loại | `nho` (Đúng / Đủ / Trọng tâm) | `rag` (Đúng / Đủ / Trọng tâm) | Kết luận cặp (`completeness`) |
|---|---|---|---|---|
| `K-C1` | `hoi_tiep_y_cu` | 5 / 5 / 5 | 5 / 5 / 4 | Hoà (5 ↔ 5); `nho` hơn Trọng tâm |
| `K-C2` | `hoi_tiep_y_cu` | 5 / 5 / 4 | 1 / 1 / 1 (từ chối chuẩn) | **`nho` thắng** (+4) |
| `K-C3` | `hoi_tiep_y_cu` | 5 / 5 / 5 | 1 / 1 / 1 (từ chối chuẩn) | **`nho` thắng** (+4) |
| `K-M1` | `hoi_tiep_y_moi` | 5 / 5 / 5 | 5 / 5 / 5 | Hoà (5 ↔ 5) |
| `K-M2` | `hoi_tiep_y_moi` | 5 / 5 / 5 | 5 / 5 / 5 | Hoà (5 ↔ 5) |

Tổng hợp 5 cặp (`nho` ↔ `rag`):
- **Đủ ý (`completeness`):** thắng **2** · hoà **3** · thua **0** | TB `nho`: **5,00** ↔ TB `rag`: **3,40** (chênh **+1,60**).
- **Đúng (`accuracy`):** thắng **2** · hoà **3** · thua **0** | TB `nho`: **5,00** ↔ TB `rag`: **3,40** (chênh **+1,60**).
- **Trọng tâm (`relevance`):** thắng **3** · hoà **2** · thua **0** | TB `nho`: **4,80** ↔ TB `rag`: **3,20** (chênh **+1,60**).

---

## 3. Chi phí OpenAI (`gpt-6-luna`) của lượt đo 25/11

| Hạng mục | Chi phí ghi nhận (USD) | Nguồn ghi nhận |
|---|---:|---|
| N — 28 câu đã thấy (bên `agent`) | 0,0214 | `chat_metrics` trên `ea96e47c` (bên `moc` không ghi `usd`) |
| K kín — 7 câu mới (bên `agent`) | 0,0047 | `chat_metrics`: `0,0312 - 0,0265` (bên `moc` không ghi `usd`) |
| S kín — Lượt 1 (10 câu) | 0,001578 | `do_g.py` |
| S kín — Lượt 2 (10 câu) | 0,002274 | `do_g.py` |
| T kín — tổng 28 câu (`a` 0,003993 + `tuyến B1` 0,013384) | 0,017376 | `dem_tro_chuyen.py` (chênh 0,000001 do làm tròn từng file) |
| C kín — agent (15 chuỗi / 33 lượt) | 0,016472 | `cham_chuoi_b7.py may` |
| C kín — RAG mốc (5 chuỗi / 10 lượt) | 0,0027833 | `chuoi_rag_moc.py` |
| **Tổng cộng phần có số đo** | **0,0665833** (≈ **0,067 USD**, ~1.665 đồng) | Chưa gồm phần RAG mốc trong `N` và `K kín` (lệnh không ghi tiền) |

Chấm mù của phiên E (28 cặp N, 7 cặp K kín, 10 mục C kín): **0 đồng API ngoài**.

---

## 4. Các ca trượt sàn / lỗi và giới hạn cần lưu ý

1. **5 mã trượt sàn / gặp lỗi trên bộ kín `gpt-6-luna` (`ea96e47c`):**
   - `b_kin_10` (`S kín`, cả 2 lượt): câu ngoài phạm vi bị trả lời bằng kho (`S2`).
   - `b_kin_09` (`S kín`, lượt 2): lỗi kỹ thuật cả 2 lần thử sau khi đã `hoi_lai` 1 lần.
   - `a_kin_08` (`T kín (a)`): `1 / 4` câu về Huế bị định tuyến nhầm sang `tro_chuyen` (`S3`).
   - `s15` (`T kín tuyến B1`): câu ngoài phạm vi bị định tuyến nhầm sang `tro_chuyen` và trả lời thay vì từ chối (`S3` + `S2_ngoai_bi_tra_loi`).
   - `K-N2` (`C kín`): `1 / 15` chuỗi có lượt ngoài kho bị trả lời (`ngoai_kho_bi_tra_loi`).
2. **`L kín` = `NOT RUN`:** phép mô phỏng trước khi chạy trên `diem_v16.json` chỉ khớp `4 / 5` chuỗi ⇒ chưa có số đo sửa lịch bằng lời trên bộ kín ở bản `ea96e47c`.
3. **Giới hạn mẫu & phạm vi đối chiếu:**
   - Kích thước bộ kín nhỏ (`K = 7`, `S = 10`, `T = 28`, `C = 15` chuỗi trong đó 5 cặp hỏi tiếp); mỗi bộ chạy 1 lượt (trừ `S kín` 2 lượt).
   - Chưa chạy lại `Golden`, `An toàn`, `S2` (44 câu), `S2c` (17 câu), `L đã thấy` ở Mốc 2 trên `gpt-6-luna`; không dùng số Mốc 1 (18/11) để bù vào Mốc 2.
   - Chấm mù chỉ mới có 1 người (`e`) cho N và C kín; K kín có thêm người thứ hai (`b`) sẽ đối chiếu độ đồng thuận ở bước review chéo.
   - Không mở hay trích bất kỳ file `*sealed*` nào khi lập báo cáo này.

---

## 5. Bảng kiểm bàn giao (`guides/CACH_LAM_VIEC.md` mục 1)

| Mục | Nội dung |
|---|---|
| **Người dùng làm được / chưa làm được** | Xem được đầy đủ số đo bộ câu kín trên `main` `ea96e47c` (`gpt-6-luna`), tách riêng Mốc 1 (18/11) và Mốc 2 (25/11), cùng 5 ca trượt sàn (`b_kin_10`, `b_kin_09`, `a_kin_08`, `s15`, `K-N2`) và lý do `L kín` `NOT RUN`. Chưa có số `Golden` / `An toàn` / `L kín` trên bản `ea96e47c`. |
| **Chưa làm** | Chưa đối chiếu độ đồng thuận `cham_b_k.jsonl ↔ cham_e_k.jsonl` (việc của `@b` khi review chéo). Chưa chạy hay đọc `*sealed*`. |
| **Tự hoãn + lý do** | Hoãn phân tích nguyên nhân chữ câu hỏi của 5 mã trượt sàn vì luật cứng cấm mở các file `*sealed*` trong báo cáo tracked và phiên đo chỉ được đọc phần cặp mù / kết quả tổng hợp đã tách tên kín. |
| **Lệnh kiểm + đầu ra** | `uv run python` tổng hợp `cham_e_n.jsonl` (28 dòng), `cham_e_k.jsonl` (7 dòng), `scores_01.jsonl` (10 dòng) khớp `khoa.json`, `khoa_k.json`, `map.json` ⇒ `TONG_HOP_SO.json` (`N: 27/28 ↔ 12/28`, `K: 7/7 ↔ 5/7`, `C: nho 5,00 ↔ rag 3,40`, `tong_openai_usd_do_duoc: 0.0665833`). |

**Một dòng cuối:** Phép tổng hợp này KHÔNG cho biết nội dung cụ thể hay nguyên nhân văn bản của 5 ca trượt sàn (`b_kin_10`, `b_kin_09`, `a_kin_08`, `s15`, `K-N2`), chưa cho biết chất lượng trên bộ `Golden` / `An toàn` / `L kín` của bản `ea96e47c`, và mới dựa trên một người chấm ở N và C kín; hướng rộng hơn có thể làm nếu Hiếu cho phép là kiểm tra không mở nội dung gốc xem `b_kin_10` / `s15` có trùng lớp lỗi với `noi_khac_tu_choi` ở bản deploy `gpt-6-luna` hay không, bằng một lượt chạy 0 đồng bộ câu đối chứng đã thấy ở nhánh `dinh_tuyen_2` trên `ea96e47c`.
