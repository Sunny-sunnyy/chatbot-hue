# Thí nghiệm tốc độ #6 — chạy lần trả lời song song với lần định tuyến: **đạt** (C172 chạy, C175 viết report)

Người làm: C · report 09:13 05/11/2026 (`date`; chạy đo 04/11 tối) · plan `docs/superpowers/plans/2026-11-04-phase-9-toc-do-song-song-plan.md` **bản 2 `093d548445a3`** (A duyệt; trần 0,10 / dừng 0,095). Code: nhánh `p9-toc-do-6` `ea081b0` (đã push; tách từ `main` `ebd8965` — đã có câu khẩn cấp PA1 `4e3cb4e`; `main` sau đó không đổi `backend/` tới `cafb1b6`). Cờ `assistant.song_song_tra_loi` mặc định **`false`** = như `main`. Dữ liệu private: `data/phase_9/toc_do/thi_nghiem_6/`.

## Kết luận

**Mọi sàn đạt, chỉ số quyết đạt.** Ở giao diện (đường stream), khi bật cờ, chữ trả lời đầu tiên của câu về Huế hiện **sớm hơn trung vị 1,37 s** (CI 95 % [0,34; 2,14] s; 15 / 20 cặp nhanh hơn) — ngưỡng ghi trước ≥ 0,5 s và CI > 0. An toàn không đổi: 90 lượt (30 câu khẩn cấp, ngoài phạm vi, trò chuyện, câu dễ nhầm, 20 lượt về Huế) **0 lượt lọt chữ / nguồn của lần trả lời bị bỏ**, 0 câu khẩn cấp sai tuyến; câu khẩn cấp ra chữ nhanh như cũ.
**Chưa bật** — bật là đổi hành vi chạy thật ⇒ A trình User (plan §4 "Đạt ⇒ A trình User bật"). Hai đổi User cần biết: (1) mỗi câu **không** về Huế tốn thêm một lần trả lời bị bỏ (đo: ≈ 0,00023 USD / câu bỏ, cận dưới); (2) câu khẩn cấp / ngoài phạm vi / trò chuyện nay cũng gửi kèm đoạn kho tới OpenAI (hôm nay chỉ gửi câu cho lần định tuyến) — cùng nhà cung cấp, không thêm loại dữ liệu.
Vẫn **chưa đạt sàn User** 3 / 5 s chữ đầu (biến p50 3,53 / p95 7,72 s hôm đo; mốc cùng lúc 5,36 / 8,69 s — nhà cung cấp chậm hôm đó so với B2 3,50 / 5,33 s) ⇒ bước sau theo `data/phase_9/toc_do/c150_phan_tich.md` (#4 gộp định tuyến vào lần trả lời — đổi kiến trúc, User quyết).

## Đổi một thứ (plan §1–§2)

Cờ bật, đường `/api/chat/stream`, câu đi qua định tuyến model: code chạy **cùng lúc** lần định tuyến và phần của tuyến `tro_ly_hue` (lần tìm đầu bằng câu gốc + lần gọi trợ lý stream). Sự kiện của phần sau **giữ trong hàng đợi** tới khi có tuyến: `tro_ly_hue` (kể cả định tuyến lỗi / quá 10 s) ⇒ xả hàng đợi rồi stream tiếp; tuyến khác ⇒ huỷ task, bỏ hết, đi đúng đường hôm nay của tuyến đó. Phần chạy sớm ghi vào trace phụ, chỉ gộp khi giữ (D1); `chat_metrics` thêm `n_tra_loi_bo`, `usd_bo`, `bo_huy_giua` (D2). `/api/chat` không đổi.

| File (nhánh, `main...p9-toc-do-6`) | Đổi |
|---|---|
| `backend/llm/assistant.py` (+83) | `AssistantFlags.song_song_tra_loi`; `answer_turn_stream_parallel` (task song song + hàng đợi + huỷ); 3 trường trace |
| `backend/api/routes/chat.py` (+9 / −3) | route stream gọi hàm mới khi cờ bật; log 3 trường |
| `backend/config/settings.yaml` (+1) | `song_song_tra_loi: false` |
| `backend/tests/test_toc_do_song_song.py` (mới, 7 test) | client model giả (logic thuần — không phải bằng chứng cho model / mạng): cờ tắt = đường cũ; tuyến giữ ⇒ 0 sự kiện trước tuyến + cùng yêu cầu; tuyến khác ⇒ bỏ hết (khẩn cấp, ngoài phạm vi); huỷ giữa chừng ⇒ cận dưới + câu soạn sẵn không chậm; trò chuyện ⇒ đường cũ; định tuyến lỗi ⇒ giữ; phần sớm lỗi + tuyến khác ⇒ câu đúng tuyến |

## Cách đã chạy thật (04/11, `ROUTER_INSTRUCTIONS` `164bd4a254e9`)

1. **Q1 (0 USD):** `capture_all.py` — 228 yêu cầu (208 câu Golden + an toàn `answer_case`, 10 `/api/chat`, 10 `/api/chat/stream`) trên `main` `ebd8965`, nhánh cờ tắt, nhánh cờ bật ⇒ `q1/{main,nhanh_tat,nhanh_bat}.jsonl`.
2. **Tầng an toàn (paid):** `tools/chay_an_toan.py chay an_toan_r1.jsonl` — 90 lượt qua đúng `_answer_events` của route stream (cờ bật ở rìa), ghi chuỗi sự kiện SSE + trace; chấm `tools/cham_an_toan.py an_toan_r1.jsonl` (mốc tuyến C165 dùng lại — A chốt, cùng ngày, Q1 giống byte).
3. **Chữ đầu ABBA (paid):** hai server uvicorn cùng commit, hai worktree, khác cờ (mốc `false` / biến `true`); `tools/chu_dau_abba.py chay chu_dau_r1.jsonl` — 16 câu (10 về Huế + 4 khẩn cấp + 1 ngoài phạm vi + 1 trò chuyện) × 2 lượt × 2 bên, thứ tự đổi chiều ghi trước, mỗi yêu cầu một client mới; `tinh` ⇒ Q / KC. Log server `log_moc.log`, `log_bien.log`. Không lượt có phí / việc nặng khác cùng lúc (W31).
4. **Kiểm lại lúc viết report (05/11, 0 USD):** chạy lại `cham_an_toan.py` + `chu_dau_abba.py tinh` trên dữ liệu đã lưu ⇒ đúng các số dưới; so `q1/*.jsonl` ⇒ cờ tắt = `main` 228 / 228, cờ bật = `main` 228 / 228; `pytest tests/test_toc_do_song_song.py tests/test_assistant.py tests/test_emergency.py` trên `ea081b0` ⇒ **20 passed**.

## Kết quả (plan §4)

| Mã | Sàn / quyết | Kết quả | |
|---|---|---|---|
| Q1 | cờ tắt giống byte `main`; cờ bật: yêu cầu định tuyến + trả lời giống byte cờ tắt | 228 / 228 · 228 / 228 | đạt |
| T | test logic | 7 / 7 (cùng 13 test file chạm: 20 / 20) | đạt |
| AN | tuyến ≠ `tro_ly_hue`: 0 `delta` / `sources` / `clarify` / `notice` của phần bỏ; chữ = câu soạn sẵn / lời trò chuyện; tuyến giữ: chữ ghép = câu cuối | 0 vi phạm / 90 | đạt |
| K | 0 / 30 câu khẩn cấp sai tuyến | 0 / 30 | đạt |
| S1 | 0 / 20 lượt về Huế sang trò chuyện / ngoài phạm vi | 0 / 20 | đạt |
| N | ngoài phạm vi / khẩn cấp sang trò chuyện 0; ngoài phạm vi sang `tro_ly_hue`; câu thường sang khẩn cấp | 0 · 0 · 0 | đạt |
| R | sai tuyến ≤ sai mốc + N_AA + 1 | 123: 0 (ngưỡng 2) · lịch sử: 0 (ngưỡng 1) | đạt |
| AT | 10 câu an toàn trong bộ: tuyến ∈ tập mốc ⇒ dùng lại 4 số S-AT của `main` | 0 câu ngoài tập ⇒ dùng lại (Q1 giống byte) | đạt |
| **Q** | trung vị (mốc − biến) ≥ 0,5 s, CI 95 % > 0 (20 cặp, bootstrap theo cặp seed 20261024) | **1,368 s [0,337; 2,137]**, 15 / 20 cặp biến nhanh hơn | **đạt** |
| KC | chữ đầu khẩn cấp: trung vị biến ≤ mốc + 0,3 s (8 lần / bên) | 1,80 ↔ mốc 1,83 s | đạt |

**Theo dõi:** chữ đầu câu về Huế p50 / p95 mốc 5,36 / 8,69 s ↔ biến 3,53 / 7,72 s (cả hai > sàn User 3 / 5 s; định tuyến p50 mốc 1,90 ↔ biến 1,74 s). **Câu trò chuyện biến chậm hơn** (2 câu × 2 lượt: mốc 2,95 / 3,10 s ↔ biến 3,95 / 3,42 s) — mẫu quá nhỏ để kết luận; [giả thuyết] lần tìm + mô hình nhúng chạy cùng lúc tranh CPU với lần gọi trò chuyện. Câu ngoài phạm vi: mốc 1 / 2 lượt đi `tro_ly_hue` (nhiễu định tuyến của mốc, biến 2 / 2 đúng). Lượt bỏ: 62 / 90 lượt (61 huỷ giữa chừng) ⇒ `usd_bo` 0,0143 (cận dưới cho phần huỷ) ≈ **0,00023 USD / câu bỏ** — câu không về Huế từ ≈ 0,00009 (chỉ định tuyến) lên ≈ 0,0003 USD, vẫn ≤ NFR 0,0005 USD / câu.

## Tiền

**0,0593 USD** = tầng an toàn 0,0214 (gồm lượt bỏ 0,0143) + chữ đầu 0,0235 (mốc 0,0116 + biến 0,0119) — trong trần 0,10. Judge: không.

## Giới hạn

- Chỉ đường stream; `/api/chat` không đổi (plan §1). Câu trò chuyện có thể chậm hơn (mẫu 2 câu) — đo thêm nếu bật.
- Nhà cung cấp chậm hôm đo ⇒ số tuyệt đối p50 / p95 không so được với lượt cũ; Q so theo cặp cùng lúc nên vẫn dùng được.
- 20 cặp chỉ thấy chênh lớn; sàn 0 / 30 câu khẩn cấp không chứng minh tỉ lệ 0 (cận trên ≈ 3 / 30).
- `usd_bo` của lượt huỷ giữa chừng là cận dưới (không có usage thật khi huỷ — D2).
- Nhánh chưa có B4 (`hoi_lai`): B4 merge trước ⇒ rebase + chạy lại Q1 + test (sự kiện `clarify` thuộc phần sớm — giữ / bỏ như `delta`, plan §5); cổng ổn định chạy lúc merge.

## Bàn giao cho người kiểm (B)

- Đọc: plan bản 2 `093d548445a3` §1–§4 ⇒ `git diff main...p9-toc-do-6` (4 file) ⇒ report này.
- Chạy lại 0 USD: `cd data/phase_9/toc_do/thi_nghiem_6 && uv run --project /home/minhhieu/hue_rag python tools/cham_an_toan.py an_toan_r1.jsonl` và `… tools/chu_dau_abba.py tinh chu_dau_r1.jsonl`; so `q1/*.jsonl`; pytest trên worktree nhánh (`/tmp/c_toc_do6` C vừa tạo lại).
- Lệch: không (mốc tuyến dùng lại C165 là A chốt trong plan).
