# Plan thí nghiệm tốc độ #6 — bắt đầu lần trả lời song song với định tuyến

Người viết: C · **bản 2** 20:46 04/11/2026 (`date`; sửa theo review B `…-toc-do-song-song-plan_review.md` `5834e2d07df0`: m-1, m-2, m-3) · bản 1 `c3c787b78650` · việc **C169** (A giao). Chưa A duyệt sha, chưa code, 0 USD. Mức vừa: đổi luồng sau cờ (`run-experiment`). File tracked, repo public: không chép câu bộ đo / Golden / kho.
Nền: thí nghiệm #1 (mức suy luận `none` cho định tuyến) **kết quả âm** — phạm sàn S1 (`report_agent/2026-11-02_phase_9_code/c156_toc_do_dinh_tuyen.md`); plan #1 §4 ghi #6 là bước sau. Chữ đầu câu về Huế hiện **3,50 / 5,33 s** (B2, 10 câu) > sàn User **3 / 5 s**.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục | Để kiểm gì |
|---|---|---|
| `data/phase_9/toc_do/c150_phan_tich.md` (`db2cab1d821c`) | §1–§3 | định tuyến ≈ 46 % chữ đầu `tro_ly_hue` (p50 1,5 s), TTFT trợ lý ≈ 1,7 s ⇒ lợi tối đa |
| `backend/llm/assistant.py` `_pick_route` (:336), `answer_turn_stream` (:389–), `_before_model` (:275) + `backend/api/routes/chat.py` `_answer_events` | luồng hôm nay | D1–D4 làm được; đầu vào hai lần gọi model không phụ thuộc tuyến |
| `docs/superpowers/plans/2026-11-03-phase-9-toc-do-dinh-tuyen-plan.md` bản 5 (`da2ff2c8e56c`) §2–§3 + `c156_toc_do_dinh_tuyen.md` | bộ đo, sàn K / S1 / N / R / AT, mốc C165 | chép đúng sàn; dùng lại mốc có hợp lệ |
| spec Phase 9 (`169c2dd5f86a`) | §4 (S-AT, tốc độ chỉ theo dõi), §7 | sàn an toàn; tiền |

## 1. Đổi một thứ

- Cờ `settings.yaml` `assistant.song_song_tra_loi` (mặc định `false` = như `main`). Bật: ở **đường stream** (`/api/chat/stream` — giao diện dùng), khi `router` bật và câu đi qua định tuyến model, code chạy **cùng lúc** (i) lần định tuyến như hôm nay và (ii) phần của tuyến `tro_ly_hue`: lần tìm đầu bằng câu gốc (`lan_tim_dau: v0` — không phụ thuộc tuyến) + lần gọi trợ lý stream. Sự kiện của (ii) **giữ trong hàng đợi**, không gửi trình duyệt, tới khi định tuyến xong:
  - tuyến `tro_ly_hue` (kể cả định tuyến lỗi / > 10 s ⇒ `tro_ly_hue` như hôm nay) ⇒ xả hàng đợi rồi stream tiếp;
  - tuyến khác ⇒ **huỷ** (ii), bỏ mọi thứ (ii) đã làm, đi đúng đường hôm nay của tuyến đó (câu soạn sẵn khẩn cấp / câu ngoài phạm vi / lần gọi trò chuyện).
- `/api/chat` (không stream) **không đổi** (bước sau nếu cần).
- Không đổi: lời dặn + đầu vào lần định tuyến, lời dặn + đầu vào lần trả lời, nhớ hội thoại, kiểm citation, dòng nhắc.

## 2. Quyết định

| Mã | Quyết định | Vì sao | Sai khi |
|---|---|---|---|
| **D1** | (ii) ghi vào **trace phụ** (sổ nguồn, đoạn, `tools`, `llm_calls` riêng); chỉ khi tuyến = `tro_ly_hue` mới gộp vào trace chính | tuyến khác không mang nguồn / số đo / công cụ của lượt bị bỏ | quên gộp một trường ⇒ log thiếu — test khoá tập trường `chat_metrics` |
| **D2** | Huỷ (ii) bằng huỷ task asyncio (cùng cách ngắt khi trình duyệt đóng — B131 (d) đã thấy lần trả lời bị huỷ dừng sạch). `chat_metrics` thêm `n_tra_loi_bo` + `usd_bo`: lượt bỏ **đã chạy xong trước khi có tuyến** ⇒ usage thật (như mọi lần gọi); lượt **bị huỷ giữa chừng** ⇒ không có usage (B131) ⇒ ghi `usd_bo_uoc` = **cận dưới** (token vào bộ dựng đếm × giá vào) + cờ `bo_huy_giua` (bản 2, m-2) | đo được giá lượt bỏ mà không chờ lần gọi xong | giá thật của lượt huỷ cao hơn ước (token ra trước khi huỷ) — chỉ phần này là "cận dưới" |
| **D3** | Lỗi của (ii) (tìm / ngân sách ngữ cảnh / model) khi tuyến ≠ `tro_ly_hue` ⇒ bỏ qua, không log lỗi; khi tuyến = `tro_ly_hue` ⇒ xử như hôm nay | lượt bỏ không được làm hỏng câu khẩn cấp / ngoài phạm vi | — |
| **D4** | Nhớ hội thoại ghi như hôm nay (sau `done`, câu hỏi của lượt) — lượt bỏ không ghi gì thêm | — | — |
| **D5** | Câu khẩn cấp do luật code (`emergency_rule`, đang tắt) giữ đường cũ: luật chạy trước, không bắt đầu (ii) | không tốn lượt bỏ khi luật đã bắt | — |

## 3. Bộ đo và mốc

- **Tầng an toàn end-to-end (cờ bật, 1 lượt; bản 2 m-3):** qua `answer_turn_stream` thật (harness gọi hàm, ghi chuỗi sự kiện + trace). Yêu cầu định tuyến giống byte (Q1) ⇒ đo lại tuyến trên cả bộ chủ yếu là nhiễu model; thứ #6 thật sự đổi là **AN** (lượt bỏ có lọt ra không, lượt giữ có xả đúng không) ⇒ bộ = **mọi lượt nhãn ≠ `tro_ly_hue`** trong 123 câu rủi ro + tầng lịch sử 50 lượt (plan #1 bản 5): 30 khẩn cấp · 13 ngoài phạm vi · 8 câu thường dễ nhầm · 19 trò chuyện = **70** + **20 lượt `tro_ly_hue` chọn trước** (10 câu đầu bộ an toàn 32 theo thứ tự `qid` + 10 lượt `tro_ly_hue` có lịch sử đầu tiên của `ls_b3` theo thứ tự file) = **90 lượt**. Lượt `tro_ly_hue` chạy hết (cần sự kiện thật để kiểm xả hàng đợi).
- **Mốc tuyến:** mốc C165 (04/11, `ROUTER_INSTRUCTIONS` `164bd4a254e9`, 123 × 2 + 50 × 2 — `data/phase_9/toc_do/thi_nghiem_1/ban4/moc_*.jsonl`). **A chốt: dùng lại** (cùng ngày 04/11, lần định tuyến giống byte — Q1 phải chứng minh trước khi chạy). Chạy sang ngày khác ⇒ **Lệch** luật "mốc cùng ngày" (plan #1 M-1) ⇒ báo A trước; thay thế: mốc mới 123 × 2 + 50 × 2 (≈ 0,031).
- **Chữ đầu ABBA (M-2 plan #1):** 10 câu `tro_ly_hue` của C165 (`data/phase_9/b131/questions.jsonl` i 1–5 + `data/phase_9/toc_do/thi_nghiem_1/chu_dau_cau_c.jsonl`) + **6 câu tuyến khác** tự viết (**4 khẩn cấp** — bản 2 m-1, 1 ngoài phạm vi, 1 trò chuyện) = 16 câu; hai server cùng commit khác cờ; 2 lượt, thứ tự đổi chiều ghi trước; script `tools/chu_dau_abba.py` (C165, sửa: thêm 4 câu + nhóm). Không việc nặng / lượt có phí / Playwright khác cùng lúc (W31 — C nhắn A + B, chờ xác nhận).

## 4. Tiêu chí ghi trước

| Mã | Sàn / quyết | Không đạt ⇒ |
|---|---|---|
| **Q1** (gỡ được + giống byte) | cờ tắt ⇒ mọi yêu cầu gửi model giống byte `main` (`capture_all.py`, 176 + 32 + smoke); cờ bật ⇒ yêu cầu định tuyến **và** yêu cầu trả lời của mỗi câu giống byte yêu cầu tương ứng khi cờ tắt (chỉ khác thời điểm) | sửa tới khi đạt |
| **T** (test, 0 USD) | client giả: định tuyến chậm / nhanh hơn trợ lý; trợ lý phát chữ trước khi có tuyến ⇒ **0 sự kiện** ra trước tuyến; tuyến ≠ `tro_ly_hue` ⇒ 0 sự kiện của (ii), trace chính không có nguồn / công cụ của (ii); định tuyến lỗi ⇒ xả; (ii) lỗi + tuyến khác ⇒ câu đúng tuyến | sửa |
| **AN** (sàn, code đếm, 90 lượt) | tuyến ≠ `tro_ly_hue`: **0** lượt có `delta` / `sources` / `clarify` / `notice` của (ii); chữ ra **đúng bằng** câu soạn sẵn (khẩn cấp, ngoài phạm vi) hoặc lời trò chuyện; tuyến = `tro_ly_hue`: chữ ghép từ `delta` = câu trả lời cuối (`delta_matches_final`) | âm |
| **K / S1 / N** (sàn) | như plan #1 §3, trên 90 lượt: 0 câu khẩn cấp (30 — đủ cả bộ) sai tuyến; 0 lượt `tro_ly_hue` (20, không `chap_nhan`) sang `tro_chuyen` / `ngoai_pham_vi`; N như plan #1 bản 3 (đủ cả bộ ngoài phạm vi / câu thường) | âm |
| **R** (mức tụt) | trên đúng các lượt đã chạy: sai tuyến ≤ sai mốc C165 cùng lượt (max hai lượt) + N_AA (cùng lượt) + 1, tính riêng phần 123 / tầng lịch sử | âm |
| **AT** (sàn) | an toàn 32: Q1 giống byte cả lần định tuyến lẫn lần trả lời ⇒ đường của câu không đổi ⇒ dùng lại 4 số S-AT của `main` (nguồn như plan #1 bản 5 §3); 10 câu an toàn có trong bộ 90: tuyến ∈ tập tuyến mốc C165, ngoài tập ⇒ sinh lại 3 lần hai bên, báo đủ 4 số (W51) | âm nếu phạm S-AT |
| **Q** (quyết) | 20 cặp chữ đầu `tro_ly_hue`: trung vị chênh (mốc − biến) **≥ 0,5 s** và CI 95 % của trung vị (bootstrap theo cặp, seed 20261024) > 0. Báo kèm: p50 / p95 chữ đầu biến so sàn User 3 / 5 s | "chưa rõ" ⇒ giữ cờ tắt |
| **KC** (sàn) | chữ đầu 4 câu khẩn cấp × 2 lượt = **8 lần đo mỗi bên** (bản 2 m-1): trung vị biến ≤ mốc + 0,3 s (huỷ (ii) không làm chậm câu soạn sẵn) | âm |
| theo dõi | USD / câu theo tuyến; `n_tra_loi_bo`, `usd_bo` (tách: xong trước tuyến = thật; huỷ giữa chừng = `usd_bo_uoc` cận dưới) — so NFR User ≤ 0,0005 USD / câu; chữ đầu ngoài phạm vi / trò chuyện; CPU / RAM máy (lần tìm + mô hình nhúng chạy cùng lúc định tuyến) | — |

**Ngưỡng Q 0,5 s** (A chốt; plan #1: 0,25 s): lợi kỳ vọng ≈ thời gian định tuyến (p50 1,5 s, C150) — đặt nửa mức tối thiểu để chỉ giữ thay đổi đưa chữ đầu gần sàn. **Cỡ mẫu:** 20 cặp chỉ thấy chênh lớn; sàn 0 trên 30 câu khẩn cấp không chứng minh tỉ lệ 0 (cận trên ≈ 3 / 30); KC 8 lần / bên chỉ bắt chậm rõ.
**Kết quả âm** (một sàn phạm hoặc Q chưa rõ) ⇒ cờ `false`, tag `hoso/p9-toc-do-6`, ghi kết quả. **Đạt** ⇒ A trình User bật (đổi hành vi chạy thật: mỗi câu không về Huế tốn thêm một lần trả lời bị bỏ).

## 5. Tiền, dừng, thứ tự

- Ước (giá thật 04/11: định tuyến ≈ 0,000088 / lần; lần trả lời có công cụ ≈ 0,0003–0,0004 USD): tầng an toàn 90 lượt × (0,000088 + ≈ 0,0003 — gồm lượt bỏ, phần vào chiếm chủ yếu) ≈ **0,035** · chữ đầu 16 câu × 2 lượt × 2 bên × ≈ 0,0004 ≈ **0,026** ⇒ **≈ 0,061**. Mốc mới (nếu A chọn thay dùng lại): + 0,031.
- **Trần 0,10 / dừng > 0,095** (A chốt) hoặc một lượt vượt ước > 50 %. **Trước chữ đầu:** tiền đã dùng + 0,026 > mốc dừng ⇒ báo A, không bắt đầu.
- **Thứ tự:** code + T + Q1 (0 USD) ⇒ chạy thử mọi lệnh có phí ở chế độ 0 USD (W36 4b) ⇒ tầng an toàn 90 (AN / K / S1 / N / R / AT) ⇒ đạt ⇒ chữ đầu ABBA (Q, KC). Nhánh `p9-toc-do-6` từ `main` mới nhất; mốc C165 / dùng lại ghi commit `main` lúc chạy.
- Nếu B4 (`hoi_lai`) đã merge lúc code: sự kiện `clarify` thuộc (ii) — giữ / bỏ như `delta` (đã có trong AN).

## 6. Rà agent (phần chạm)

| Mục | #6 | Nhãn |
|---|---|---|
| Đường ra | thêm **một lần gọi OpenAI** cho câu không về Huế (bị huỷ) — cùng nhà cung cấp, cùng dữ liệu (câu hỏi + đoạn kho) như lượt `tro_ly_hue`; không đường ra mới | thiết kế |
| Dữ liệu cá nhân | câu khẩn cấp / ngoài phạm vi nay cũng gửi kèm đoạn kho tới OpenAI (hôm nay chỉ gửi câu cho định tuyến) — không thêm loại dữ liệu; log không chữ như cũ | ghi giới hạn khi trình User |
| Lỗi | (ii) lỗi không được chạm câu soạn sẵn (D3, AN) | test + sàn |

## 7. Bước sau

- #6 âm hoặc Q chưa rõ: #4 (gộp định tuyến vào lần trả lời — đổi kiến trúc) ⇒ User quyết; hoặc giữ chữ đầu "chỉ theo dõi" (PA1 User mặc định 03/11).

## Chỗ đổi bản 2 (20:46 04/11/2026, review B `5834e2d07df0`)

| Finding | Sửa ở |
|---|---|
| m-1 KC "8 lần / bên" sai với 2 câu × 2 lượt | §3 bộ chữ đầu thêm 2 câu khẩn cấp (4 câu) ⇒ 8 lần / bên; §5 tiền |
| m-2 lượt bỏ đã xong có usage thật | D2: tách usage thật / cận dưới (`bo_huy_giua`); dòng theo dõi |
| m-3 (A chốt theo B) | §3 tầng an toàn 173 ⇒ 90 lượt (mọi lượt nhãn ≠ `tro_ly_hue` + 20 lượt `tro_ly_hue` chọn trước); K / S1 / N / R / AT theo đó; §5 tiền ≈ 0,061 |
| A chốt: mốc dùng lại C165, trần 0,10 / dừng 0,095, ngưỡng Q 0,5 s | §3 mốc; §5 trần; §4 dòng ngưỡng Q |

Không đổi: D1, D3–D5, Q1, T, AN (luật), Q, KC (luật), kết quả âm.
