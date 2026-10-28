# Review: Phase 8.2 B1 — 5 chỗ báo cáo cho context 10 + NFC (commit `92b9a43`)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 5 minor — A tự sửa, không cần vòng review riêng)
Người kiểm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 09:47 28/10/2026 (`date`) · Việc: B79 (A giao 28/10). Chỉ đọc, 0 USD.
Canonical: `WORKFLOW.md` §6 (5 chỗ + văn phong cho User); code trên `main` `510e1a8`. Implementation: `phase_8_2_b1_merge_implementation.md` (merge B1).

## 1. Phạm vi đã review

`git show 92b9a43`: 9 file, +150 / −59 — `bao_cao_he_thong/{LUONG_HOAT_DONG_HE_THONG, BAO_CAO_SINH_CAU_TRA_LOI_API (bản 12), BAO_CAO_TIM_KIEM (bản 9),
README}.md`, `bao_cao_he_thong/nhat_ky/2026-10-28_dua_context_10.md` (mới), `session_prompt/Project_Status.md`, `guides/{phase_6_generation_api, phase_8_benchmark_model_selection,
full_corpus_rag}.md`. Đọc exact diff cả 9 file + bản đầy đủ của nhật ký mới; quét mọi chỗ còn ghi "5 đoạn / top-5 / tối đa 5" trong 7 file sống.

## 2. Kết quả theo 5 tiêu chí A giao

| # | Tiêu chí | Kết quả |
|---|---|---|
| 1 | Mô tả hành vi khớp code | **Đạt.** `settings.yaml:55` `max_context_documents: 10`, `:52` `context_limit: 16384` (khớp "`settings.yaml:52,55`"); `core/settings_loader.py:75` chỉ nhận 10 (khớp guide 6); `retrieval/full_corpus.py:97-102` `normalize_query` = kiểm rỗng + NFC, gọi ở `:420` đầu `search` (khớp LUONG §3 bước 0, TIM_KIEM §5). Số cổng chạy thật (1.282 token vào, 6 nguồn trích, 10 nguồn ngữ cảnh, 5,1 s; ngoài kho 2,5 s; ≈ 0,000423 USD; 51 test) khớp `phase_8_2_b1_merge_implementation.md:18-34` |
| 2 | Còn sót "5 đoạn" là hiện trạng | Gần đạt — 1 chỗ (m-1). Các chỗ khác ghi "5 đoạn" đều là số đo cũ có nhãn, thử nghiệm 8.1, hoặc mục lịch sử (guide 6 `:430`, `:640`; guide 8 `:99`… nằm dưới "Quyết định đã phê duyệt" / "Baseline"; `full_corpus_rag.md:463` lịch sử có chú "Hiện hành 28/10") |
| 3 | Số đo ghi đúng nguồn; số ở 5 đoạn ghi rõ | Gần đạt — 3 chỗ (m-2, m-3, m-4) |
| 4 | Không lộ nội dung kho / Golden | **Đạt.** `.githooks/overlap_scan.py` trên 9 file: **0 trùng** mỗi file; nhật ký và phần thêm chỉ có số đếm, mã commit, loại câu |
| 5 | Văn phong cho User | **Đạt.** Nhật ký có "Bạn cần làm gì", "Giải thích ngắn (để bạn tự nói lại được)", số kèm ý nghĩa, tiền thật từ log, nói rõ giới hạn "chưa có mốc người" và cách quay về 5. Mã nội bộ (PA3, B0) đều có giải nghĩa ngay cạnh. 1 chữ (m-5) |

`git show 92b9a43 --check`: sạch.

## 3. Findings (đều minor — A sửa)

### m-1 — guide 6 mục "Hiện hành" vẫn mở đầu bằng "tối đa Top 5"

- `guides/phase_6_generation_api.md:45-46` (trong "Contract full-corpus hiện hành", mục Hiện hành): "context pack tối đa Top 5 nguyên chunk … ; **Hiện hành 28/10: tối đa 10**".
  Câu chính vẫn nói 5, rồi phần thêm vào nói 10. Người đọc lướt dễ hiểu sai.
- **Đóng:** viết lại thành "tối đa 10 nguyên chunk (từ 28/10, Phase 8.2 B1 `510e1a8`; trước đó 5)".

### m-2 — "chưa đo lại trên bộ lớn" sai: tiền / token ở 10 đoạn đã đo trên 176 câu

- `LUONG_HOAT_DONG_HE_THONG.md:83` ("Ở 10 đoạn … tiền mỗi câu tăng (8.1 ước ~+50 %); chưa đo lại trên bộ lớn") và nhật ký "Giải thích ngắn" ("8.1 ước ~+50 %").
- Bằng chứng: lượt B1 (cùng cấu hình context 10, đường `answer_case`) trên **176 câu**: **0,0369 USD** = ≈ **0,00021 USD / câu**, token vào TB **1.655** (`phase_8_2_b1_implementation.md` §4;
  B tính lại từ `data/phase_8_2/b1/b1_{dev,test}.jsonl`). So với ~0,00014 ở 5 đoạn ⇒ +50 % là **số đo**, không chỉ là ước. (Số này đo qua harness, không qua API — nhưng cùng
  đường tìm → đóng gói → sinh.)
- **Đóng:** thay bằng "đo ở lượt B1 176 câu: ~0,00021 USD / câu (~5 đồng), ~1.650 token vào" (LUONG; nhật ký có thể ghi gọn tương tự).

### m-3 — `BAO_CAO_SINH` Tóm tắt: "Giới hạn chính: từ chối nhầm 22/158" là số 5 đoạn, không có nhãn

- `BAO_CAO_SINH_CAU_TRA_LOI_API.md:19`. Tóm tắt phải "luôn đúng hiện trạng"; 22 / 158 là 7B (5 đoạn). Ở 10 đoạn, lượt B1 176 câu có **12 / 158** câu trong kho bị từ chối
  (đếm `refusal` trên `b1_{dev,test}.jsonl`; 8.1 dev: 13 → 7).
- **Đóng:** "từ chối nhầm 22/158 ở 5 đoạn (7B); ở 10 đoạn còn 12/158 (lượt B1)" — hoặc chỉ thêm nhãn "(7B, 5 đoạn)". Bảng §4 của LUONG đã có câu "Bảng trên đo ở bản 5 đoạn" ⇒ đạt; có thể
  thêm số 12 / 158 vào đoạn ngay dưới bảng cho rõ.

### m-4 — `BAO_CAO_SINH` Tóm tắt: "Chi phí: sinh 176 câu ~0,024 USD" không có nhãn 5 đoạn

- `BAO_CAO_SINH_CAU_TRA_LOI_API.md:21`. Đó là 7B (5 đoạn); ở 10 đoạn lượt B1 176 câu = **0,0369 USD** (~920 đồng).
- **Đóng:** thêm nhãn và số 10 đoạn (cùng nguồn m-2).

### m-5 — `Project_Status.md` §3: dòng 8.2 ghi "chờ C71 review" trong khi §2 ghi "C71 ready"

- `Project_Status.md` bảng §3 dòng `| 8.2 |`: "… ≈ 0,000423 USD; **chờ C71 review**)". §2 (cùng commit) và nhật ký: C71 **ready 0 / 0 / 0**.
- **Đóng:** đổi thành "C71 review ready 0 / 0 / 0".

### Ngoài phạm vi (không yêu cầu sửa)

- Dòng "Cập nhật lần cuối" đầu `BAO_CAO_TIM_KIEM.md` và `BAO_CAO_SINH_CAU_TRA_LOI_API.md` còn dấu `**` lẻ từ các bản trước (ví dụ "… giống từng byte.** Bản 5"; "… (25 câu).** Bản 7")
  ⇒ Markdown có thể hiện dấu sao thừa. Có từ trước commit này; sửa khi tiện.

## 4. Cách người kiểm chạy lại thật

Chỉ đọc, 0 USD: `git show 92b9a43` (từng file); `sed -n` / `grep -n` `backend/config/settings.yaml`, `backend/core/settings_loader.py:68-80`, `backend/retrieval/full_corpus.py:95-103,415-422`;
`/usr/bin/grep -n` các số trong `phase_8_2_b1_merge_implementation.md`; `uv run --quiet python .githooks/overlap_scan.py <9 file>` ⇒ 0 trùng mỗi file; `git show 92b9a43 --check`;
`uv run python -I` đếm `refusal` / `usd` / `input_tokens` trên `data/phase_8_2/b1/b1_{dev,test}.jsonl` (12 / 158; 0,03692 USD; 1.655 token vào TB). Quét "5 đoạn / top-5 / tối
đa 5 / 22/158 / 0,024 / 0,00014" trong 7 file sống, xem mục chứa từng dòng.

## 5. Giới hạn

- Không kiểm các phần **không đổi** của 9 file (ngoài các dòng có từ khóa đã quét).
- Số 12 / 158 và 0,0369 USD là lượt harness B1 (25/10, trước merge; cùng đầu vào model với `main` sau merge theo T2 của B1), không phải số qua API.

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`: mô tả hành vi đúng code, không lộ nội dung, văn phong đạt. 5 minor (m-1 … m-5) A sửa thẳng; B không cần kiểm lại trừ khi A muốn.
