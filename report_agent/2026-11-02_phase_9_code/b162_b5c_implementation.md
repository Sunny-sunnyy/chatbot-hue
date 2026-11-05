# Implementation Report: Phase 9 B5c — tính tiền bằng code (`tinh_tien`) — **phần 0 USD xong (test, Q1, Q1m, dò bảng); lượt có phí chờ B5 merge; cờ tắt; nhánh `p9-b5c` `42bdd93`**

Người làm: B (Claude Opus 5.5, `hue-rag-48`) · việc **B162** (A giao 05/11) · bản này 12:48 05/11/2026 (`date`).
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

## 3. Còn lại (theo plan §5) — sau khi B5 merge

Rebase lên `main` ⇒ Q1 / Q1m lại (lúc đó `main` có thể bật `lich_trinh`) ⇒ pilot 3 câu (đo lại `TINH_TIEN_TOOL_OVERHEAD`) ⇒ đã thấy 14 × 2 lượt + chuỗi Q3 ⇒ ≤ 2 vòng chỉnh ⇒ khoá ⇒ Q4 hồi quy 62 (+ S-AT nếu có) ⇒ cổng + Playwright ⇒ report ⇒ review. Tiền: chưa dùng (0 USD).

**Giới hạn đã biết:** "mình và 2 bạn" ⇒ dò 2 người (theo mẫu plan); số lấy từ câu hỏi trước có thể cũ nếu người dùng đổi chủ đề; bảng chỉ có vé lẻ Quần thể (vé gộp / điểm khác: không tổng, câu cố định); D5 chỉ nói khi có lưu trú (≥ 2 ngày).

**Giải thích ngắn:** Khi người dùng hỏi "đi Huế mấy ngày, mấy người hết bao nhiêu" hay "vé vào mấy điểm bao nhiêu", code lấy đúng bảng giá trong kho, tự nhân / cộng và in bảng có trích nguồn; model chỉ viết vài câu dẫn và bị code chặn nếu tự ghi số tiền không có trong kho. Thiếu số người / ngày thì code hỏi bằng nút. Bật / tắt bằng một cờ; cờ tắt thì chatbot chạy y như trước (đã kiểm từng byte).
