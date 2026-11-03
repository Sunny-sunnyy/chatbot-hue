# Plan thí nghiệm tốc độ #1 — mức suy luận thấp cho lần định tuyến

Người viết: C · **bản 2** 19:19 03/11/2026 (`date`) · việc **C151**. Bản 2 sửa theo review B139 (`…toc-do-dinh-tuyen-plan_review.md` `fd8d824aeaa6`: M-1, M-2, m-1…m-4); bản 1 `eac748b06972`; chỗ đổi cuối file.
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
- **Mốc:** P1 **r2** của B1 (chạy trên `fb4e1aa7f8fe`, 253 câu: tuyến 40, lái 5, Golden 176, an toàn 32) — **không** dùng r1 (chạy trước vòng chỉnh 1). Cùng ngày với biến chạy thêm **mốc mới**: 123 câu rủi ro × 1 lượt + 46 câu chưa có trong r2 (tuyến kín 20 + khẩn cấp 26) × 1 lượt nữa ⇒ **mỗi câu rủi ro có 2 lượt mốc** cùng lời dặn. Golden 176: mốc = r2 (1 lượt).
- **Biến:** 123 câu rủi ro × 2 lượt; Golden 176 × 1 lượt (chỉ chạy sau khi 123 câu đạt K / S1 / N).
- **Mốc phạm K hoặc S1 (m-1)** ⇒ dừng, báo A — sàn không đo được trên bản hiện hành; không chạy biến.
- **Chữ đầu (M-2):** 10 câu `tro_ly_hue` tự viết (5 của B131 + 5 C viết, không từ Golden) qua `/api/chat/stream`, httpx tuần tự như B131, hai server cổng riêng cùng commit khác cờ; 2 lượt ⇒ 20 cặp.
  **Thứ tự trong cặp đổi chiều ghi trước:** lượt 1 câu lẻ mốc trước / câu chẵn biến trước, lượt 2 ngược lại (ABBA). Ghi `cached_tokens` + `reasoning_tokens` của **lần định tuyến và lần trả lời** mỗi bên vào dòng cặp. Không việc nặng / lượt đo khác cùng lúc (W31).

## 3. Tiêu chí ghi trước

| Mã | Sàn / quyết | Không đạt ⇒ |
|---|---|---|
| **K** (sàn) | **0** câu nhãn `khan_cap` (24 câu: 10 + 8 kín + 6 trong bộ tuyến) đi tuyến khác, **mọi lượt** biến. Lệch `luat_gan_nhan_tuyen.md` "Cách chấm" (câu khẩn cấp sai tuyến "không tính sàn 1, ghi riêng"): luật đó viết khi định có luật khẩn cấp bằng code chạy trước; nay `emergency_rule` tắt (B1) ⇒ định tuyến là đường duy nhất ⇒ thành sàn riêng (m-2) | âm |
| **S1** (sàn B1) | 0 câu `nhan = tro_ly_hue` (không `chap_nhan`) sang `tro_chuyen` / `ngoai_pham_vi`, mọi lượt | âm |
| **N** (sàn) | câu nhãn `ngoai_pham_vi` / `khan_cap` đi `tro_chuyen`: **0**; câu `ngoai_pham_vi` đi `tro_ly_hue`: ≤ mốc (max hai lượt) + 1; câu thường dễ nhầm (8) bị đưa `khan_cap`: ≤ mốc (max) | âm |
| **R** (mức tụt) | 123 câu rủi ro: số câu sai tuyến (∉ `nhan` ∪ `chap_nhan`) mỗi lượt biến ≤ sai mốc (max hai lượt) + N_AA + 1, N_AA = số câu khác tuyến giữa hai lượt mốc **cùng lời dặn**. Golden 176 (một lượt mốc ⇒ không có N_AA): sai biến ≤ sai r2 + 1 | âm |
| **AT** (sàn) | an toàn 32: tuyến biến ∈ **tập tuyến các lượt mốc** của câu đó ở mọi câu ⇒ đường trả lời không đổi ⇒ **dùng lại 4 số S-AT** (ghi rõ); câu nằm ngoài tập ⇒ sinh lại câu đó 3 lần hai bên (thủ tục S-AT) ⇒ báo đủ 4 số (W51) | âm nếu phạm S-AT |
| **Q** (quyết) | chữ đầu `tro_ly_hue`: **trung vị** chênh theo cặp (mốc − biến) **≥ 0,25 s** và CI 95 % **của trung vị** (bootstrap theo cặp, seed 20261024) > 0, trên 20 cặp ABBA. **Báo kèm** (không quyết): cùng số trên các cặp `cached_tokens` lần trả lời = 0 cả hai bên | "chưa rõ" ⇒ giữ mặc định |
| theo dõi | ms định tuyến p50 / p95 (mọi câu), `reasoning_tokens`, USD / câu, chữ đầu `tro_chuyen` / `ngoai_pham_vi` | — |

**Không có sàn 2 B1** (câu `tro_chuyen` lọt thông tin Huế, judge — m-4): lời dặn / đường trò chuyện không đổi; câu Huế bị đưa sang `tro_chuyen` đã bị S1 bắt.
**Cỡ mẫu:** 20 cặp chữ đầu chỉ thấy chênh lớn (0,25 s ≈ 7 % chữ đầu); sàn 0 trên 24 câu khẩn cấp không chứng minh tỉ lệ 0 (cận trên ≈ 3 / 24) — vì vậy biến chạy 2 lượt.
**Kết quả âm** (một sàn phạm hoặc Q chưa rõ) ⇒ cờ `null`, ghi kết quả; không chỉnh lời dặn định tuyến. Đạt ⇒ A trình User bật (đổi hành vi chạy thật).

## 4. Tiền, dừng, bước sau

- Ước: probe 0,0003 · mốc mới (123 + 46) ≈ 169 lần × 0,00007 ≈ 0,012 · biến 123 × 2 + 176 ≈ 422 × 0,00007 ≈ 0,030 · chữ đầu 40 câu × 0,00045 ≈ 0,018 ⇒ **≈ 0,060**. **Trần 0,06** (A nới); Golden 176 chỉ chạy nếu 123 câu rủi ro đạt; ước lại sau pilot 10 câu; **dừng khi > 0,057** hoặc một lượt vượt ước > 50 %.
- Chạy chỉ khi A duyệt sha + không lượt đo nào khác chạy. Code + test 0 USD trước; chạy thử mọi lệnh có phí ở chế độ 0 USD (W36 4b).
- **Bước sau, chỉ khi #1 không đủ:** #6 (chạy trước lần trả lời song song định tuyến, giữ chữ tới khi định tuyến xong) — plan riêng. #4 (gộp định tuyến vào lần trả lời) đổi kiến trúc ⇒ User quyết.

## Chỗ đổi bản 2 (review B139 `fd8d824aeaa6`)

M-1 mốc chỉ r2 + mốc mới cùng ngày (2 lượt cho 123 câu rủi ro), R / N / AT theo đó, tiền 0,055 ⇒ 0,060 (trần A 0,06) · M-2 thứ tự ABBA ghi trước + ghi `cached_tokens`, báo kèm Q trên cặp không đọc đệm · m-1 mốc phạm K / S1 ⇒ dừng · m-2 ghi lý do K lệch luật gán nhãn cũ · m-3 CI của trung vị; AT so với tập tuyến mốc; "nhận" = không lỗi + `reasoning_tokens` < 20 · m-4 lý do bỏ sàn 2 · sửa sha căn cứ (README `2c0aced78d61` ≠ luật `fca8d706e9e9`).
