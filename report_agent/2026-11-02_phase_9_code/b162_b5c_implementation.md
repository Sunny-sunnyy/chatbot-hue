# Implementation Report: Phase 9 B5c — tính tiền bằng code (`tinh_tien`) — **ÂM hai lần theo luật ghi trước ở Q4 — lượt B5c (F2 + S-AT) và lượt B5c-2 (S-AT 1 câu miễn giảm vé); cờ tắt; nhánh `p9-b5c` `7821d34`**

Người làm: B (Claude Opus 5.5, `hue-rag-48`) · việc **B162** (A giao 05/11) · bản này 13:52 05/11/2026 (`date`; trước 12:48).
Plan: `docs/superpowers/plans/2026-11-05-phase-9-b5c-plan.md` bản 3 `bab730a57798` (A duyệt; trần 0,14 / dừng 0,13). Bộ đo: `data/phase_9/bo_do_b5c/` (C) — **chỉ đã thấy 14 + chuỗi 7** (kín bỏ theo luật 11:18 05/11).
Nhánh `p9-b5c` từ `p9-b5` `5bc45cf` (B5 chưa merge), worktree `/tmp/b_b5c`: `f0fc864` (dò số người + chuẩn hoá tiền) → `e6cda0b` (công cụ) → `42bdd93` (câu tìm đoạn vé). Đã push, chưa review. **Khi B5 merge ⇒ rebase lên `main` + chạy lại Q1 / Q1m rồi mới chạy lượt có phí.**
Report tracked, repo public: không chép kho / câu bộ đo; số kỳ vọng trong test tính lại từ ô bảng lúc chạy.

## 1. Đã làm

**Ý chính (khung FDE):** model chỉ chọn **loại câu** (dự toán / vé / cả hai / khoản ngoài bảng), mức chi, tên điểm. **Code** đọc bảng kho, lấy số người / ngày, nhân / cộng, dựng bảng có `[n]` + khối ghi chú, kiểm số tiền trong chữ model; thiếu số người / ngày thì code tự trả thẻ hỏi lại (như B5).

| File | Thay đổi |
|---|---|
| `backend/llm/tinh_tien.py` (mới) | nạp 3 bảng dự toán (5 / 6 / 6 hạng mục + dòng tổng, **tổng kho = tổng cộng** cả 9 ô, ngày đối chiếu) và bảng vé lẻ Quần thể (12 dòng, điều kiện tuổi đọc từ tiêu đề cột, ngày hiệu lực, **11 điểm Quần thể của bảng điểm B5 khớp đúng một dòng**) — sai ⇒ không khởi động; `chot_tham_so` (D6 / D7), `tinh` (D3, D2b, D4, D5), `bang_markdown` / `khoi_ghi_chu` / `dong_minh_hieu` (D8), `khung_chu` (chữ đưa model), `kiem_tien` (D9) |
| `backend/llm/do_so.py`, `so_tien.py` | `do_so_nguoi` (người lớn / trẻ em, "vợ chồng" = 2, "một mình" = 1, mơ hồ ⇒ không đoán, > 20 ⇒ ngoài phạm vi), `do_ngay_du_toan` ("nửa ngày", "X ngày Y đêm" lệch ⇒ ngoài phạm vi); `tim_gia_tri` (số đồng, gồm cận thấp của khoảng). Hàm B5 dùng không đổi |
| `backend/llm/hoi_lai.py` | loại thẻ `chi_phi` (số người · số ngày · mức chi); `TruongInput.so_nguoi` số nguyên 1–20, `muc_chi` |
| `backend/llm/assistant.py` | cờ `tinh_tien` + `bang_tien` (nạp ở rìa); `tinh_tien_for_turn` (≤ 1 lần / câu; thiếu ⇒ thẻ chỉ trường thiếu; lượt mang `truong` ⇒ không hỏi lần hai, đặt tạm 1); `_lay_nguon_tien` (D10); `_finish_generated`: dòng "Mình hiểu" + chữ model + bảng + ghi chú, **D9 chạy mọi câu trợ lý khi cờ bật**, hỏng ⇒ rút lại như citation hỏng; stream: bước `tinh_tien`, bảng + ghi chú nối sau chữ model; `tool_overhead` cộng hằng hai công cụ |
| `backend/llm/generator_openai_full_corpus.py`, `full_corpus_prompt.py` | công cụ `tinh_tien` (mô tả ngắn `TINH_TIEN_MO_TA`, **không** thêm lời dặn hệ thống), luật trình bày trong kết quả công cụ; dừng lượt khi code trả thẻ (chung cơ chế B5 D15) |
| `backend/retrieval/full_corpus_context.py` | `TINH_TIEN_TOOL_OVERHEAD = 275` (ước: 359 × token lược đồ 433 / 566 của `lich_trinh`; pilot đo lại) |
| `backend/api/routes/chat.py`, `config/settings.yaml`, `evaluation/full_corpus_eval.py` | log nhãn `tinh_tien_*` (không chữ); `ChatResponse.tinh_tien` + SSE `tinh_tien` (thẻ Sửa); cờ `tinh_tien: false` + 2 đường dẫn file kho |
| `frontend/src/App.jsx`, `index.css` | "Đang tính tiền…", nhãn bước (đã chọn bảng / đã tính bằng code ✓ / cần thêm … / ngoài phạm vi), thẻ Sửa, nút số người 1–5 + "6+" mở ô số 6–20 |
| `backend/tests/test_b5c_do_so.py` (37), `test_b5c_tinh_tien.py` (mới) | bảng §3b của plan; nạp bảng kho thật + bảng hỏng bị từ chối; phép tính 3 ngày × 3 cỡ nhóm × có / không mức; lưu ý D3 / D4 / D5; vé (bí danh, tên lạ, trẻ không rõ số, miễn phí); thẻ chỉ trường thiếu; số từ câu trước; "Trả lời luôn" tạm; lượt đầy đủ stream (thứ tự bước, `[n]` là đoạn bảng thật); số tự nghĩ ⇒ rút lại cả khi không gọi công cụ; route 422 + cờ tắt ghép câu. `test_b5_lich_trinh.py`: 2 chỗ đổi vì `so_nguoi` nay hợp lệ |

**Lệch plan (B tự quyết, ghi lại):** (a) D1 `loai` thêm `ca_hai` (≤ 1 lần / câu mà câu D4 cần cả hai bảng) và `ngoai_bang` (câu giá phòng / bữa ăn / xe cụ thể ⇒ code nối câu cố định S2 thay vì hỏi số người vô nghĩa); (b) khung đưa model **không có số** (chỉ nói bảng nào sẽ hiện) — model không có số để chép / nhân, D9 vẫn cho phép số code tính; (c) mục vé lẻ nhận bằng từ khoá tiêu đề — hook pre-commit chặn chép nguyên tiêu đề kho ≥ 40 ký tự; (d) D10 vé: kho chia bảng vé **một dòng / một đoạn** ⇒ mỗi dòng một lần tìm, câu tìm chọn bằng dò 0 USD (12 / 12 dòng có đoạn đúng trong top-10; "Giá vé <tên>" chỉ 10 / 12); (e) D9 bắt cả số nhóm nghìn **không đơn vị** ("777.000") và cận thấp của khoảng; (f) câu vé nói "N người" chung ⇒ N người lớn, 0 trẻ (khớp nhãn của C); (g) vé chỉ bắt buộc số người.

## 2. Đã chạy (0 USD)

| Kiểm | Kết quả |
|---|---|
| pytest B5 + B5c + giao diện tĩnh | **160 passed**; cả bộ 384 passed (lỗi còn lại = test cần khoá API / bản dựng, bẫy đã biết) |
| **Q1** cờ tắt ↔ `p9-b5` `5bc45cf` (`capture_all.py`, 228 ca) | **228 / 228** giống byte (mốc chạy lại trên HEAD trước: = file mốc B5 `908e93b`) |
| **Q1m** cờ bật, bỏ mục `tinh_tien` | **228 / 228** giống byte; 228 / 228 lần gọi trợ lý có đúng một mục `tinh_tien`, 228 lần định tuyến không có |
| Nạp bảng kho thật | 3 bảng 5 / 6 / 6 hạng mục, tổng 9 / 9 khớp, 12 dòng vé, 11 / 11 điểm Quần thể khớp đúng một dòng |
| Phép tính ↔ **đáp án C tính tay độc lập** (`so_dap_an.py`) | **8 / 8** câu trong phạm vi khớp từng dòng + tổng (dò số từ chính câu) |
| Dò số trên đã thấy + chuỗi (`do_so_bo.py`) | khớp nhãn 100 % |
| Đoạn nguồn D10 (Qdrant chỉ đọc) | 3 / 3 bảng dự toán, 12 / 12 dòng vé |
| App cờ bật khởi động (khoá giả, không gọi API) | bảng nạp được; `so_nguoi: 25` ⇒ 422 |

Harness lượt có phí đã viết, **chưa chạy**: `data/phase_9/b5c/tools/chay_b5c.py` (`chay` / `dem` / `kiem` — `kiem` 0 USD đã chạy), `chuoi_b5c.py` + `app_tien.py` (Q3 qua server thật).

## 3. Lượt có phí (sau B5 merge, rebase lên `main` có #6)

Rebase: `main` `ae5a6d6` (B5) rồi `ba0c187` (#6 bật) ⇒ nhánh `fb981b8`. Q1 / Q1m lại sau mỗi lần rebase: **228 / 228** cả hai; sau #6 kiểm cả hai trạng thái cờ `song_song_tra_loi` (4 lần bắt, đều giống byte `main`). Thêm test đường song song giữ giá trị nút số người / "Trả lời luôn".

| Mốc | Tiêu chí ghi trước | Kết quả | |
|---|---|---|---|
| Pilot 3 + 3 câu | ước tiền + đo hằng D11 | hằng đo **325** (ước 275). Câu vé T5: model **không gọi** công cụ, tự nhân giá trong tài liệu ⇒ D9 bắt, rút lại (rào an toàn chạy đúng) | ⇒ vòng chỉnh 1 |
| **Vòng chỉnh 1** (1 / 2 vòng) | — | mô tả công cụ nói rõ "gọi cả khi tài liệu đã có giá, không tự nhân / cộng"; code coi "dự toán + tên điểm" là cả hai (T7); hằng 325. Lượt 1 đã thấy lộ lỗi ghép của code: câu từ chối chuẩn của model ở câu ngoài phạm vi bị kiểm citation nhầm (N1, N2) ⇒ sửa code: kiểm citation trên chữ model + bảng (dòng "Mình hiểu" / ghi chú là câu cố định) | ⇒ **khoá `ecc099c`** |
| **Đã thấy 14 × 2 lượt** (khoá) | Q2a ≥ 7 / 8 mỗi lượt; S1, S2 = 0; Q5 ≥ 7 / 8; thẻ đúng trường 2 / 2 | **cả hai lượt:** Q2a 8 / 8 · S1 0 · S2 0 · câu ngoài phạm vi có câu cố định 4 / 4 · **Q5 8 / 8** (khớp đáp án C tính tay từng dòng) · thẻ 2 / 2 · rút lại 0 · `max_turns` 0 | **đạt** |
| **Chuỗi Q3 × 2 lượt** (server thật, cookie, #6 bật) | 0 lượt 2 bị hỏi lại lần hai; "Trả lời luôn" 0 thẻ + giá trị tạm | **6 / 6** chuỗi sàn đạt cả hai lượt (lượt 2 không hỏi lại, giá trị = nhãn; c4 / c5 tạm đúng trường); log 0 dòng có chữ câu hỏi. Lệch nhãn C ở **lượt 1** chuỗi c3 (câu chỉ hỏi giá vé một điểm): model trả giá đơn vị từ kho kèm [n], không gọi công cụ ⇒ không thẻ — không thuộc sàn Q3 (sàn đếm lượt 2) | đạt |
| **Q4 Golden 30** | F1–F4 | F1 0 · F3 0 · F4 0 · **F2 câu mới bị chấm sai: 1** (câu hỏi giá vé một suất biểu diễn — kho có giá ở file khác, ngoài bảng vé lẻ Quần thể; công cụ trả "ngoài bảng", luật trình bày "không tự viết số tiền" làm model **bỏ luôn giá có trong kho**, ghi chú "chưa có giá vé" ⇒ chấm 2 / 5 ↔ mốc 5 / 5). Từ chối trong phạm vi 0 | **phạm** |
| **Q4 an toàn 32** (2 judge, cổng đối chứng 10 / 10 · 0 / 5 cả hai) | 4 số + S-AT | ngoài kho bị trả lời 0 · sai điều kiện mới 1 · thiếu cảnh báo mới 3 ⇒ S-AT | ⇒ S-AT |
| **S-AT** (3 B5c + 3 mốc mỗi câu, 2 judge mới mù bên; đạt ⇔ B5c ≤ mốc mọi câu) | | thiếu cảnh báo câu 1 **2 / 3 ↔ 3 / 3** · câu 2 **3 / 3 ↔ 3 / 3** · câu 3 **1 / 3 ↔ 0 / 3**; sai điều kiện 0 / 18 cả hai bên | **phạm** (câu 3) |
| S-NHAM | công cụ gọi ở câu không phải tiền ≤ 1 / 62 | 0 / 62 (1 lần gọi ở câu Golden hỏi giá vé — đúng là câu tiền) | đạt |
| Rút lại do D9 | ≤ 1 / 62 | 0 / 62 | đạt |

**Đọc kết quả [suy luận, n nhỏ]:** câu S-AT phạm (miễn giảm vé) **không gọi** `tinh_tien`; bên B5c tìm kho thêm nhiều hơn (2 lần ở 2 / 3 lượt ↔ 1 lần ở mốc) — cùng dạng B4b (§2g báo cáo B4): công cụ + mô tả thứ hai trong **mọi** lượt trợ lý đổi cách model tìm ở vài câu. Chênh 1 / 3 ↔ 0 / 3 không chứng minh được bằng n = 3, nhưng luật ghi trước tính là âm, không vòng thêm. Câu Golden phạm là lỗi thiết kế của B5c (luật trình bày quá chặt ở câu ngoài bảng) — sửa được bằng code / lời (cho model nêu giá có trong tài liệu khi công cụ không có bảng), nhưng plan đã ghi "Q4 không đạt ⇒ âm".

**Theo plan:** kết quả âm ⇒ cờ `tinh_tien` tắt, câu chi phí giữ hành vi `main`; tag `hoso/p9-b5c`. A / User quyết: giữ âm (merge cờ tắt như B4b, hay không merge) hay mở vòng sửa mới (đổi tiêu chí ⇒ User duyệt).

## 3b. Lượt B5c-2 (thí nghiệm mới, plan "Chỗ đổi B5c-2" `815e44e9882a` A duyệt; khoá `7821d34`; 14:18 05/11/2026)

Đổi so với lượt B5c (lượt đó giữ âm, không chỉnh): **D8′** câu không có bảng ⇒ model được nêu giá có trong tài liệu kèm [n] (luật riêng `TINH_TIEN_LUAT_KHONG_BANG`), ghi chú "«…» không thuộc bảng vé lẻ nên hệ thống không tự tính tổng", không dòng "Mình hiểu", không hỏi số người khi không điểm nào thuộc bảng vé lẻ; **D11′** chỉ đưa công cụ khi code thấy dấu hiệu chi phí (câu gốc / câu trước / trường chi phí từ nút; mẫu gồm cả "tốn / hết / chuẩn bị … bao nhiêu" — phủ 14 / 14 câu đã thấy + 7 / 7 lượt đầu chuỗi).

| Mốc | Tiêu chí | Kết quả | |
|---|---|---|---|
| Q1 / **Q1m′** (2 trạng thái `song_song`) | cờ tắt giống byte `main`; cờ bật: câu không dấu hiệu giống byte `main`, câu có dấu hiệu chỉ thêm một mục | **228 / 228** cả bốn lần bắt; chỉ **45 / 228** lần gọi trợ lý có `tinh_tien`, còn lại giống byte `main` không cần bỏ mục | đạt |
| Đã thấy 14 × 1 | không gãy sàn | Q2a 8 / 8 · S1 0 · S2 0 · câu cố định 4 / 4 · Q5 8 / 8 · thẻ 2 / 2 · rút lại 0 | đạt |
| **Golden 30** | F1–F4 | **sạch** (F2 0 — câu giá vé biểu diễn nay nêu giá kho kèm [n]); từ chối trong phạm vi 0; TB đủ ý 4,80 ↔ 4,87, chính xác 4,93 ↔ 4,97 | **đạt** |
| An toàn 32 (2 judge, cổng 10 / 10 · 0 / 5) | 4 số | **11 / 32 câu có dấu hiệu chi phí** (được đưa công cụ), 21 / 32 giống byte `main`. Sai điều kiện mới 0 (2 câu mốc hết) · trái nguồn 0 · ngoài kho bị trả lời 0 · thiếu cảnh báo mới 3 (2 câu **không** dấu hiệu — yêu cầu giống byte `main`, chênh là nhiễu model; 1 câu có dấu hiệu) | ⇒ S-AT |
| **S-AT** (3 + 3, 2 judge mới mù) | B5c-2 ≤ mốc mọi câu | 2 câu không dấu hiệu: **0 / 3 ↔ 1 / 3** cả hai · câu có dấu hiệu (miễn vé trẻ nhỏ khi nghe ca Huế trên thuyền): **3 / 3 ↔ 1 / 3** — `tinh_tien` được gọi 2 / 3 lượt, câu trả lời bỏ điều kiện (chiều cao / ngồi cùng người lớn) thường hơn; sai điều kiện 0 / 18 | **phạm** |
| S-NHAM / rút lại D9 | ≤ 1 / 62 | 0 / 62 (1 lần gọi ở câu Golden hỏi giá vé — câu tiền) · 0 / 62 | đạt |

**Đọc [suy luận, n = 3]:** D11′ làm đúng việc của nó — 21 câu an toàn không dấu hiệu nay giống byte `main`, và hai câu "thiếu cảnh báo mới" trong nhóm đó hết khi sinh lại (0 / 3). Lỗi còn lại nằm ở **câu miễn giảm vé**: có chữ "vé / miễn phí" nên được đưa công cụ (A dặn không nới dấu hiệu để né); khi model gọi `tinh_tien` (loại vé, ngoài bảng), câu trả lời ngắn lại và bỏ điều kiện an toàn. Đây là cùng nhóm câu đã làm B5c lượt 1 phạm S-AT (miễn giảm vé người khuyết tật).

**Theo luật:** B5c-2 âm, không vòng thêm ⇒ cờ `tinh_tien` tắt; tag `hoso/p9-b5c`. Hướng nếu làm tiếp (việc mới, cần plan): tách câu "miễn / giảm vé" khỏi công cụ bằng code (câu hỏi điều kiện miễn giảm ⇒ không đưa công cụ, vì công cụ không tính được miễn giảm — D2b đã ghi "chính sách miễn / giảm chỉ nhắc bằng câu cố định").

## 4. Tiền

Lượt B5c: pilot 0,0036 · đã thấy l1 0,0083 · khoá l2 0,0082 + l3 0,0080 · chuỗi × 2 0,0123 · Q4 sinh 0,0306 · S-AT 0,0079 ⇒ 0,079. Lượt B5c-2: đã thấy 0,0089 · Q4 sinh 0,0295 · S-AT 0,0106 ⇒ 0,049. **Tổng ≈ 0,128 / 0,14**. Judge: quota Claude (sub-agent). Không gọi `agy`.

**Giới hạn đã biết:** "mình và 2 bạn" ⇒ dò 2 người (theo mẫu plan); số lấy từ câu hỏi trước có thể cũ nếu người dùng đổi chủ đề; bảng chỉ có vé lẻ Quần thể (vé gộp / điểm khác: không tổng, câu cố định); D5 chỉ nói khi có lưu trú (≥ 2 ngày).

**Giải thích ngắn:** Khi người dùng hỏi "đi Huế mấy ngày, mấy người hết bao nhiêu" hay "vé vào mấy điểm bao nhiêu", code lấy đúng bảng giá trong kho, tự nhân / cộng và in bảng có trích nguồn; model chỉ viết vài câu dẫn và bị code chặn nếu tự ghi số tiền không có trong kho. Thiếu số người / ngày thì code hỏi bằng nút. Bật / tắt bằng một cờ; cờ tắt thì chatbot chạy y như trước (đã kiểm từng byte).
