# Implementation Report: Phase 9 B7 — đo GIỮA KỲ: trợ lý (agent trên `main`) ↔ RAG 1–8

Người làm: B (Claude Code — Fable 5.2, terminal `hue-rag-1b`). Người chấm: sub-agent Claude ngữ cảnh mới, mù. Review kết quả: E (A giao).
Date: 19:54 12/11/2026 (`date`). Lượt đo chạy 19:11–19:52 12/11/2026.
Plan: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` bản 2 (A duyệt `456c13142879`; file lúc chạy `2ca3f63ce45b` sau commit sửa chữ `582c9d0`).
Tham số: `$C_DONG` = `dfd0c96` · `KIN_NGAY` TẮT (7 câu ngày kín **không mở**) · `MAX_DROP` = 4 · quỹ 0,35 USD.

> **Nhãn "giữa kỳ":** lượt này trả lời "hôm nay trợ lý đã hơn RAG 1–8 chưa, ở đâu"; lượt cuối chạy lại lúc đóng code. Sàn phạm ở đây ⇒ ghi âm + nêu để sửa trước lượt cuối.

## 1. Phạm vi

Đã chạy đủ các lượt G, A, N, C, S, W, T của plan §4 trên **phần đã thấy**. **Phần kín đã dùng** của C / S / T (cần User chạy lệnh `!`): **NOT RUN** lúc viết report — lệnh soạn sẵn `data/phase_9/b7/tools/chay_kin.sh` (ghi ở `STATUS_B.md`). Bước K (câu ngày kín): không chạy theo công tắc.
**Lệch plan (B tự quyết, nêu để A xét):** (1) **bộ quyết 12 tổ hợp biểu mẫu chưa chạy lại** dù `lich_trinh.py` có đổi sau `a884de4` (plan §5 yêu cầu chạy lại) — cần 24 lượt + 4 lượt chấm, B để sau phần kín, quỹ còn đủ; (2) bộ ngoài phạm vi đã thấy có **44** câu (plan ghi ≈ 48); (3) câu thứ 28 của bộ ngày (`U1`) công cụ cũ loại sẵn ⇒ chạy bù bằng `file:` ngay sau lượt chính, cùng buổi; (4) sàn S2c lấy ≥ 15 / 17 (mốc `main` 16 trong report G) — ghi vào `chon.json` trước khi chạy.

## 2. Thay đổi chính (chỉ công cụ đo, private `data/phase_9/b7/tools/`; không sửa `backend/`, không sửa code ở `p9-moc`)

`do_cuoi_b7.py` (Golden hai bên) · `chuoi_rag_moc.py` (phía RAG của chuỗi; thêm `--loai`) · `cham_chuoi_b7.py` (bản sao hai bên — review E n-1) · `holm.py` (bootstrap + Holm — n-2) · `an_toan_b7.py` (bản sao, đổi đường dẫn) · `cap_mu_ngay.py` · `dem_tro_chuyen.py` · `chay_khong_server.sh`, `chay_ngay.sh`, `chay_sat.sh`, `chay_kin.sh`.
Ghi trước khi sinh: `data/phase_9/b7/chon.json` (18 câu nhiều nguồn, 9 chuỗi hỏi tiếp, danh sách "mong từ chối" = **0 mã** — n-5, sàn S2c, tham số Holm).

## 3. Cách đã chạy thật

- **Bước 0 (0 USD):** cờ in dưới đúng lệnh có `--env-file` khớp plan 14 / 14; `ROUTER_INSTRUCTIONS` `8cd30cbb359a` · `ANSWER_SYSTEM_INSTRUCTIONS` `81d3040cf53f`; `git diff dfd0c96 HEAD -- backend` rỗng trước mỗi lượt; preflight đạt; chạy thử `cham_chuoi_b7.py` / `holm.py` trên file cũ + số giả; kiểm đầu vào các bộ của `do_g.py` (không gọi model). Bước 0 trước đó: `b7_buoc_0_implementation.md`.
- **Pilot** 10 câu Golden mỗi bên: agent 0,00031 · RAG 0,00016 USD / câu (dưới ước) ⇒ chạy tiếp; 10 câu pilot ghép với 166 câu còn lại (mỗi câu sinh đúng một lần).
- **Sinh:** G 19:12–19:18 · A / S / W / T / C (không server) 19:19–19:31 · N qua server thật: agent 19:34–19:37, RAG 19:37–19:38, bù `U1` 19:39 · S-AT sinh lại 19:41–19:47 · 3 chuỗi nêu tên qua server ghi truy vấn 19:50.
- **Chấm (sub-agent mù, mỗi lô một agent mới):** Golden 5 agent / 14 lô / 328 mục; chuỗi 1 agent / 18 mục; an toàn 2 judge × 6 agent (99 mục mỗi judge, có 15 câu đối chứng) + vòng sinh lại 2 × 7 + vòng thêm 2 × 7; câu ngày 2 người; trò chuyện 1 người đọc. `analyze --max-drop 4` chạy **một lần**.

## 4. Kết quả quan sát

### 4.1 Sàn và ngưỡng

| Sàn / ngưỡng | Mức | Kết quả | |
|---|---|---|---|
| S-G F1 ngoài kho bị trả lời · F3 lỗi kỹ thuật · F4 lỗi trích dẫn mới · F2 "nói chắc sai" mới | 0 | 0 · 0 · 0 · 0 (không có ứng viên F2) | **đạt** |
| S-G mức tụt (129 câu số chính) | Đủ / Đúng TB ≥ −0,1; câu tụt ≤ 4; từ chối nhầm ≤ mốc + 1 | Đủ **+0,194** [CI95 +0,054; +0,357], thắng / hoà / thua 10 / 115 / 4 ⇒ **tụt 4 (đúng ngưỡng)**; Đúng +0,194 [+0,062; +0,357], tụt 1; từ chối nhầm agent 3 ↔ mốc 13 | **đạt (sát ở số câu tụt)** |
| S1 an toàn — đảo cảnh báo · sai điều kiện mới · ngoài kho bị trả lời | 0 | 0 · 0 · 0 ở cả 2 lượt agent (cổng đối chứng 2 judge: 10 / 10, 0 / 5) | **đạt** |
| S1 an toàn — **thiếu cảnh báo mới** | 0; chênh 1 ⇒ thủ tục S-AT | lượt 1: 2 câu mới, lượt 2: 0 ⇒ sinh lại 3 + 3: một câu mốc cũng thiếu 3 / 3 (không mới); **câu còn lại (loại miễn / giảm): agent 2 / 3 ↔ mốc 1 / 3 ⇒ thêm 3 + 3 ⇒ tổng agent 3 / 6 ↔ mốc 1 / 6, chênh 2 ⇒ ÂM** | **PHẠM (1 câu)** |
| S2 ngoài phạm vi bị trả lời | 0 | 0 / 44 ×2 (+ 11 câu Golden) | **đạt** (phần đã thấy) |
| **S2b** ngoài phạm vi có mục web | 0 | **2 / 44 ở cả 2 lượt** (cùng 2 mã của bộ (b) đã thấy: đi tuyến trợ lý Huế ⇒ kho từ chối ⇒ cổng web mở, kết quả web "không tin cậy") | **PHẠM** |
| S2c Huế-kho-thiếu vẫn có web | ≥ 15 / 17 | 16 / 17 | **đạt** |
| S3 câu Huế bị coi là xã giao | 0 | 0 / 158 (Golden) · 0 lượt chuỗi | **đạt** |
| S3b câu Huế bị trả "ngoài phạm vi" | 0 | 0 (G, A ×2, W) | **đạt** |
| Trích dẫn | 0 lỗi | 0 ở mọi lượt agent | **đạt** |
| S6 tiền | ≤ 0,0005 USD / câu Huế | 0,00042 (158 câu Golden trong kho); kèm: ngoài phạm vi 0,00019 · đường web 0,0018 | **đạt** |

### 4.2 Kết luận (i) — "tốt hơn ở hỏi đáp" (phần đã thấy; Holm 3 nhóm, bootstrap 10.000 vòng, seed 20261024)

| Nhóm | n | Agent ↔ RAG | Chênh TB | CI đã chỉnh (mức) | Kết luận giữa kỳ |
|---|---:|---|---:|---|---|
| Câu theo ngày ("dùng được" 0 / 1; 2 người chấm khớp 28 / 28) | 28 | 27 ↔ 11 câu dùng được; từ chối 1 ↔ 17 | +0,571 | [+0,357; +0,786] (98,33 %) | **tốt hơn** |
| Câu hỏi tiếp (Đủ 1–5) | 9 lượt | 5,00 ↔ 3,33; thắng / hoà / thua 5 / 4 / 0 | +1,667 | [+0,444; +3,0] (97,5 %) | **tốt hơn** — phần kín 5 chuỗi chưa chạy ⇒ chưa kiểm "kín không ngược chiều" |
| Câu nhiều nguồn (Đủ 1–5) | 18 | 4,44 ↔ 3,44; thắng / hoà / thua 5 / 12 / 1 | +1,0 | [+0,278; +1,833] (95 %) | **tốt hơn** (4 câu nhóm kiểm báo kèm: +2, 0, 0, −1) |

### 4.3 Kết luận (ii) — việc mới (trên bộ đã dùng để quyết bật — giới hạn A đã chốt)

| Việc | Ngưỡng | Kết quả phần đã thấy | Phần kín |
|---|---|---|---|
| Nhớ tên | ≥ 9 / 10 chuỗi | 6 / 6; 0 câu hỏi tiếp ngoài kho bị trả lời; 0 tuyến sai | 4 chuỗi — NOT RUN |
| Web | ≥ 6 / 10 câu có mục web hợp lệ **và** 0 truy vấn chứa tên | **6 / 10** (3 "không tin cậy", 1 cổng không mở) — đúng ngưỡng; 3 chuỗi nêu tên: 2 truy vấn gửi đi, **0 chứa tên** (chuỗi thứ ba cổng không mở) | — |
| Trò chuyện | ≥ 90 % câu xã giao được đáp (trên kín) **và** 0 câu có thông tin Huế cụ thể (trên đã thấy) | đã thấy: 8 / 8 được đáp, 1 / 8 đi tuyến trợ lý Huế; **0 / 8** có thông tin Huế cụ thể | 28 câu — NOT RUN |

Quan sát ngoài tiêu chí (người đọc nêu, B chưa kiểm thêm): một câu xã giao đi tuyến trợ lý Huế nên câu đáp có số trích dẫn; một câu hỏi danh tính được đáp bằng tên model / hãng của nhà cung cấp thay vì tên trợ lý.

### 4.4 Tiền (thật, từ trường `usd` / log) — **0,288 / 0,35 USD**

Golden 0,072 + 0,044 · an toàn 0,045 + 0,008 · S2 ×2 0,017 · web / S2c 0,030 · trò chuyện 0,008 · chuỗi 0,023 + 0,005 · câu ngày + chuỗi nêu tên (server) 0,023 · câu ngày mốc 0,007 · S-AT 0,005 + 0,002. Chi tiết `data/phase_9/b7/tien.json`. An toàn đắt hơn ước (≈ 0,0007 USD / câu vì có đường web). Judge: 0 USD API.
Thời gian thật: sinh ≈ 30 phút, chấm ≈ 25 phút (sub-agent chạy song song).

## 5. Lỗi và giới hạn

- **Hai sàn phạm (giữa kỳ ⇒ việc phải sửa / quyết trước lượt cuối):** S2b (2 câu ngoài phạm vi mở cổng web — cùng loại giới hạn User đã nhận 1 câu ở phương án B, nay 2 câu) và S1 "thiếu cảnh báo mới" ở 1 câu loại miễn / giảm (agent 3 / 6 ↔ mốc 1 / 6). Ở chính câu đó mốc lại có 1 / 6 "sai điều kiện", agent 0 / 6.
- Số câu tụt Golden = 4, **đúng ngưỡng**; web 6 / 10 **đúng ngưỡng** ⇒ hai chỗ không còn biên.
- Phần kín C / S / T chưa chạy ⇒ (ii) nhớ tên, trò chuyện và vế "kín không ngược chiều" của nhóm hỏi tiếp **chưa kết luận**. Biểu mẫu 12 tổ hợp chưa chạy lại.
- Cỡ mẫu nhỏ (18 · 28 · 9); judge là Claude, chưa có mốc người; mọi bộ ở đây đã thấy / đã dùng ⇒ không chứng minh tổng quát hoá. Tới lượt cuối, mọi bộ (trừ 7 câu ngày kín) đã đi qua harness này một lần (n-4).
- Người chấm Golden coi câu từ chối "chỉ hỗ trợ thông tin về Huế" là tương đương câu từ chối chuẩn ở câu ngoài kho (không vào phép so 129 câu).
- Phía agent của Golden / chuỗi là đường chỉ-kho (không web) theo plan §2; lượt An toàn / S / W / T / N là cả hệ.

## 6. Bàn giao cho người kiểm

- Đọc: `data/phase_9/b7/` — `chon.json`, `golden/analyze.json`, `an_toan/cham/compare.out` + `compare_regen.out` + `compare_regen_tong.json`, `ngay/cham_b7_nguoi_*.jsonl` + `khoa.json`, `chuoi/analyze_da_thay.json`, `holm_da_thay.json`, `gen/luot_khong_server.log`, `w/neu_ten.jsonl`, `tien.json`.
- Chạy lại rẻ nhất (0 USD): `do_cuoi_b7.py check-judge`; `holm.py holm_dau_vao_da_thay.json`; `do_g.py dem <file>` cho S / W / T; `an_toan_b7.py accept --judge k`.
- Việc của A: quyết hai sàn phạm (sửa trước lượt cuối hay nhận giới hạn — hỏi User nếu đổi phạm vi); cho chạy `chay_kin.sh` (User `!`); quyết bộ 12 tổ hợp biểu mẫu.
- Giải thích ngắn cho User: trên các bộ câu đã có, trợ lý trả lời đủ ý hơn bản RAG cũ ở cả ba nhóm (câu nhiều nguồn, câu theo ngày, câu hỏi tiếp), ít từ chối nhầm hơn và không làm hỏng câu thường; còn hai chỗ chưa đạt: hai câu ngoài phạm vi vẫn kích tra web, và một câu về miễn / giảm vé trợ lý hay bỏ sót một điều kiện hơn bản cũ.
