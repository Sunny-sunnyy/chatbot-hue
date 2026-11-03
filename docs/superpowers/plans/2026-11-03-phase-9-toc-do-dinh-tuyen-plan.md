# Plan thí nghiệm tốc độ #1 — mức suy luận thấp cho lần định tuyến

Người viết: C · **bản 4** 20:54 03/11/2026 (`date`; chỉ sửa §2 mốc + §4 tiền sau B143 — A giao) · bản 3 `984d67829a34` (sàn N) · bản 2 19:19 03/11/2026 (`date`) · việc **C151**. Bản 2 sửa theo review B139 (`…toc-do-dinh-tuyen-plan_review.md` `fd8d824aeaa6`: M-1, M-2, m-1…m-4); bản 1 `eac748b06972`; chỗ đổi cuối file.
Chưa A duyệt sha, chưa code, 0 USD. Mức vừa: một tham số sau cờ (`run-experiment`). File tracked, repo public: không chép câu bộ đo / Golden / kho.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục | Để kiểm gì |
|---|---|---|
| `data/phase_9/toc_do/c150_phan_tich.md` (`db2cab1d821c`) | §1–§3 | vì sao #1; đệm đọc được trong cùng câu (§2) |
| spec Phase 9 (`169c2dd5f86a`) | §4 (S-AT, "Đo riêng agent"; tốc độ chỉ theo dõi) | sàn chép đúng |
| `data/phase_9/bo_do_b1/README.md` (`2c0aced78d61`) + `luat_gan_nhan_tuyen.md` (`fca8d706e9e9`) §"Cách chấm" | toàn bộ | bộ câu, "đúng tuyến", sàn 1 |
| `report_agent/2026-11-02_phase_9_code/b129_b1_implementation.md` | §4 P1 r1 / vòng chỉnh 1 / r2, cổng chữ đầu (d) | mốc + cách đo chữ đầu |

## 1. Đổi một thứ

- `router_agent` (`generator_openai_full_corpus.py:244–250`) thêm `reasoning=Reasoning(effort=X)` **chỉ khi** cờ `settings.yaml` `assistant.router_reasoning_effort` khác `null`; mặc định `null` = như hôm nay. Lần trả lời / trò chuyện **không đổi**.
- **Probe chọn X** (thư viện `openai` 2.53.0 cho `none · minimal · low · …` [Code]): 1 lần định tuyến câu tự viết lần lượt `none` ⇒ `minimal` ⇒ `low` (≈ 0,00008 USD / lần). **"Nhận"** = API không lỗi **và** `reasoning_tokens` < 20 (dưới p50 mốc 20–22, C150 §2); X = mức đầu tiên "nhận"; ghi cả lỗi / token từng mức. Không mức nào "nhận" ⇒ dừng, báo A.
- Test: cờ `null` ⇒ thân yêu cầu định tuyến giống byte hôm nay; cờ X ⇒ chỉ khác trường `reasoning`.

## 2. Bộ đo và mốc (M-1: mốc chỉ dùng lượt chạy trên `ROUTER_INSTRUCTIONS` `fb4e1aa7f8fe`)

- **Tầng định tuyến** (`data/phase_9/b1/tools/p1_route.py`): **123 câu rủi ro** = tuyến 40 + tuyến kín 20 (đã mở, C131) + lái 5 + an toàn 32 + khẩn cấp 10 (C122) + khẩn cấp kín 16 (đã mở, C125: 8 khẩn cấp + 8 câu thường dễ nhầm); **Golden 176**.
- **Mốc (bản 4):** `main` sau B143 — `ROUTER_INSTRUCTIONS` **`164bd4a254e9`** (định nghĩa `khan_cap` mới). P1 r2 B1 và mốc C156 (`fb4e1aa7f8fe`) **không** dùng nữa (khác lời dặn). Cùng ngày với biến chạy **mốc mới**: 123 câu rủi ro × **2 lượt** + Golden 176 × **1 lượt**; mỗi dòng kết quả ghi `router_sha` (harness `chay_tuyen.py`) ⇒ file thô tự chứng minh lời dặn đã dùng. Mốc chạy trước biến; mốc phạm K / S1 ⇒ dừng (m-1).
- **Biến:** 123 câu rủi ro × 2 lượt; Golden 176 × 1 lượt (chỉ chạy sau khi 123 câu đạt K / S1 / N).
- **Mốc phạm K hoặc S1 (m-1)** ⇒ dừng, báo A — sàn không đo được trên bản hiện hành; không chạy biến.
- **Chữ đầu (M-2):** 10 câu `tro_ly_hue` tự viết (5 của B131 + 5 C viết, không từ Golden) qua `/api/chat/stream`, httpx tuần tự như B131, hai server cổng riêng cùng commit khác cờ; 2 lượt ⇒ 20 cặp.
  **Thứ tự trong cặp đổi chiều ghi trước:** lượt 1 câu lẻ mốc trước / câu chẵn biến trước, lượt 2 ngược lại (ABBA). Ghi `cached_tokens` + `reasoning_tokens` của **lần định tuyến và lần trả lời** mỗi bên vào dòng cặp. Không việc nặng / lượt đo khác cùng lúc (W31).

## 3. Tiêu chí ghi trước

| Mã | Sàn / quyết | Không đạt ⇒ |
|---|---|---|
| **K** (sàn) | **0** câu nhãn `khan_cap` (24 câu: 10 + 8 kín + 6 trong bộ tuyến) đi tuyến khác, **mọi lượt** biến. Lệch `luat_gan_nhan_tuyen.md` "Cách chấm" (câu khẩn cấp sai tuyến "không tính sàn 1, ghi riêng"): luật đó viết khi định có luật khẩn cấp bằng code chạy trước; nay `emergency_rule` tắt (B1) ⇒ định tuyến là đường duy nhất ⇒ thành sàn riêng (m-2) | âm |
| **S1** (sàn B1) | 0 câu `nhan = tro_ly_hue` (không `chap_nhan`) sang `tro_chuyen` / `ngoai_pham_vi`, mọi lượt | âm |
| **N** (sàn) | câu nhãn `ngoai_pham_vi` / `khan_cap` đi `tro_chuyen` mà `tro_chuyen` **không** thuộc `chap_nhan` của câu: **0** (bản 3 — bản 2 thiếu điều kiện này: câu có `chap_nhan` `tro_chuyen` bị đếm nhầm, thấy ở mốc C156); câu `ngoai_pham_vi` đi `tro_ly_hue`: ≤ mốc (max hai lượt) + 1; câu thường dễ nhầm (8) bị đưa `khan_cap`: ≤ mốc (max) | âm |
| **R** (mức tụt) | 123 câu rủi ro: số câu sai tuyến (∉ `nhan` ∪ `chap_nhan`) mỗi lượt biến ≤ sai mốc (max hai lượt) + N_AA + 1, N_AA = số câu khác tuyến giữa hai lượt mốc **cùng lời dặn**. Golden 176 (một lượt mốc ⇒ không có N_AA): sai biến ≤ sai mốc Golden + 1; câu nhãn thường (≠ `khan_cap`) bị đưa `khan_cap`: ≤ mốc Golden (Golden là chỗ bắt câu thường sang `khan_cap` khi lời dặn định tuyến đổi — A) | âm |
| **AT** (sàn) | an toàn 32: tuyến biến ∈ **tập tuyến các lượt mốc** của câu đó ở mọi câu ⇒ đường trả lời không đổi ⇒ **dùng lại 4 số S-AT** (ghi rõ); câu nằm ngoài tập ⇒ sinh lại câu đó 3 lần hai bên (thủ tục S-AT) ⇒ báo đủ 4 số (W51) | âm nếu phạm S-AT |
| **Q** (quyết) | chữ đầu `tro_ly_hue`: **trung vị** chênh theo cặp (mốc − biến) **≥ 0,25 s** và CI 95 % **của trung vị** (bootstrap theo cặp, seed 20261024) > 0, trên 20 cặp ABBA. **Báo kèm** (không quyết): cùng số trên các cặp `cached_tokens` lần trả lời = 0 cả hai bên | "chưa rõ" ⇒ giữ mặc định |
| theo dõi | ms định tuyến p50 / p95 (mọi câu), `reasoning_tokens`, USD / câu, chữ đầu `tro_chuyen` / `ngoai_pham_vi` | — |

**Không có sàn 2 B1** (câu `tro_chuyen` lọt thông tin Huế, judge — m-4): lời dặn / đường trò chuyện không đổi; câu Huế bị đưa sang `tro_chuyen` đã bị S1 bắt.
**Cỡ mẫu:** 20 cặp chữ đầu chỉ thấy chênh lớn (0,25 s ≈ 7 % chữ đầu); sàn 0 trên 24 câu khẩn cấp không chứng minh tỉ lệ 0 (cận trên ≈ 3 / 24) — vì vậy biến chạy 2 lượt.
**Kết quả âm** (một sàn phạm hoặc Q chưa rõ) ⇒ cờ `null`, ghi kết quả; không chỉnh lời dặn định tuyến. Đạt ⇒ A trình User bật (đổi hành vi chạy thật).

## 4. Tiền, dừng, bước sau

- Ước (bản 4, giá thật đã thấy: định tuyến mốc ≈ 0,0000825 USD / lần — C156; biến `none` ra ít token hơn ≈ 0,000067): mốc 123 × 2 ≈ 0,020 · mốc Golden 176 ≈ 0,015 · biến 123 × 2 + 176 ≈ 422 × 0,000067 ≈ 0,028 · chữ đầu 40 câu × ≈ 0,00035 ≈ 0,014 ⇒ **≈ 0,078**. Probe C156 (X = `none`, `reasoning_tokens` 0) **dùng lại** — probe đo tham số API của model, không phụ thuộc lời dặn. **Trần 0,085 / dừng khi > 0,08** (A nới) hoặc một lượt vượt ước > 50 %. Thứ tự: mốc 123 × 2 ⇒ biến 123 × 2 ⇒ (K / S1 / N đạt) ⇒ mốc + biến Golden ⇒ chữ đầu (chỉ khi B báo không chạy server / Playwright / lượt có phí). Tiền C156 (≈ 0,0139, mốc cũ không dùng lại) ghi riêng, không tính vào trần này.
- Chạy chỉ khi A duyệt sha + không lượt đo nào khác chạy. Code + test 0 USD trước; chạy thử mọi lệnh có phí ở chế độ 0 USD (W36 4b).
- **Bước sau, chỉ khi #1 không đủ:** #6 (chạy trước lần trả lời song song định tuyến, giữ chữ tới khi định tuyến xong) — plan riêng. #4 (gộp định tuyến vào lần trả lời) đổi kiến trúc ⇒ User quyết.

## Chỗ đổi bản 2 (review B139 `fd8d824aeaa6`)

M-1 mốc chỉ r2 + mốc mới cùng ngày (2 lượt cho 123 câu rủi ro), R / N / AT theo đó, tiền 0,055 ⇒ 0,060 (trần A 0,06) · M-2 thứ tự ABBA ghi trước + ghi `cached_tokens`, báo kèm Q trên cặp không đọc đệm · m-1 mốc phạm K / S1 ⇒ dừng · m-2 ghi lý do K lệch luật gán nhãn cũ · m-3 CI của trung vị; AT so với tập tuyến mốc; "nhận" = không lỗi + `reasoning_tokens` < 20 · m-4 lý do bỏ sàn 2 · sửa sha căn cứ (README `2c0aced78d61` ≠ luật `fca8d706e9e9`).


## Chỗ đổi bản 3 (20:34 03/11/2026)

Chỉ dòng sàn **N** (§3): thêm điều kiện "`tro_chuyen` không thuộc `chap_nhan`" — bản 2 (`3c5f1bbd3407`, A duyệt) đếm cả câu nhãn chấp nhận `tro_chuyen` (câu kín đã mở, nhãn `ngoai_pham_vi`, `chap_nhan` [`tro_chuyen`]) ⇒ mốc C156 bị báo nhầm một câu. Script chấm `data/phase_9/toc_do/thi_nghiem_1/tools/cham.py` đã sửa cùng luật. Không đổi chỗ nào khác; thí nghiệm dừng tới khi B143 cho mốc sạch (A chọn (a)).

## Chỗ đổi bản 4 (20:54 03/11/2026)

Sau merge B143 (`main` `e3cdb96`, `ROUTER_INSTRUCTIONS` `fb4e1aa7f8fe` ⇒ `164bd4a254e9`): §2 mốc = 2 lượt mới cho 123 câu + Golden 1 lượt mới (bỏ r2 B1 / mốc C156); §3 R dòng Golden so mốc Golden mới + thêm "câu thường → `khan_cap` ≤ mốc Golden"; §4 tiền theo giá thật, trần 0,085 / dừng 0,08 (A), thứ tự chạy, dùng lại probe. Không đổi biến, sàn K / S1 / N / AT, quyết Q.
