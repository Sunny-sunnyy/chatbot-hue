# Plan — hai thử nghiệm tốc độ: (S-A) tra web sớm · (S-B) gộp câu tìm · B · bản 1 · 15:23 15/11/2026

User chọn thử cả hai (A ghi nhận 15:19 15/11/2026; User đã chấp nhận: S-A gửi thêm câu hỏi về Huế ra Serper + 0,001 USD / lần). Theo `run-experiment`:
mỗi thử nghiệm **một bậc riêng, một nhánh, một cờ mặc định tắt, đổi một thứ**. Thứ tự: **S-A trước** (chỉ code, chuỗi gửi model không đổi ⇒ đo rẻ), **S-B sau**
(đổi lời dặn + tham số công cụ ⇒ chạm mọi câu). Trần **≤ 0,25 USD / bậc**. Chưa code tới khi A duyệt sha.

**Căn cứ để review:** `backend/llm/assistant.py` (`web_gate_open`, `cong_web`, `_answer_core`, `tool_for_turn`, `search_into_trace`) · `backend/llm/tra_web.py`
(`cau_tim_web`, `tim_web`) · `backend/llm/full_corpus_prompt.py` (đoạn lời dặn công cụ `tim_kho`) · hai bậc âm sáng 15/11:
`report_agent/2026-11-12_ra_khoang_cach/b_tim_song_song_implementation.md`, `b_tran_tim_1_implementation.md`.

## 0. Đếm trước khi xây (0 USD, đã chạy 15:20 — log `chat_metrics` sau mốc bật "hết lượt tìm" 20:07 13/11; log chưa có `git_sha` nên cắt theo giờ)

| Đo gì | Số |
|---|---|
| Lượt gọi model thật / lượt tuyến trợ lý Huế không phải lịch | 262 / **101** |
| Model tự tìm thêm: 0 lần · 1 lần · 2 lần (trong 101; 9 lượt không có lần tìm nào) | 58 · 20 · **14** |
| Lượt có mục web | **10** — cả 10 đều có ≥ 1 lần model tìm thêm trước đó (3 lượt 1 lần, 7 lượt 2 lần) |
| Một lần Serper | 1,75–5,17 s, **trung vị 2,2 s** (n = 10) |
| Cả câu của lượt web | 12,7–22,2 s; lần gọi model viết mục web 1,9–9,4 s (chạy SAU Serper) |

**Hai điều phải nói thẳng trước khi làm:**
- **S-A không làm "chữ đầu" nhanh hơn.** Ở lượt web, chữ đầu là câu "kho không đủ thông tin" (ra sau 2–3 lần gọi trợ lý); Serper chỉ nằm trên đường tới **mục web**.
  S-A rút thời gian **tới mục web / cả câu** khoảng 2 s trên ~15 s (≈ 15 %). Sàn chữ đầu 3 / 5 s của đường này vẫn trượt sau S-A.
- **S-B** chỉ giúp lượt model tìm 2 lần: 14 / 101 lượt Huế (≈ 5 % mọi lượt). Bớt được một lần gọi ≈ −2,4 s (số đo sáng nay ở bậc "trần 1"); chữ đầu nhóm này ~5,8 s ⇒ có thể vẫn trên 3 s.

## 1. S-A — tra web sớm (nhánh `p9-web-som`, cờ `tra_web_som`, mặc định tắt)

**Đổi một thứ:** lúc **model gọi `tim_kho` lần đầu** trong lượt (dấu hiệu kho có thể không đủ), code khởi một tác vụ nền gọi Serper bằng đúng câu `cau_tim_web(câu hỏi)` như hôm nay.
Cổng web (`web_gate_open`) **không đổi**: cổng mở ⇒ `cong_web` dùng kết quả đã có (hoặc chờ nốt) thay vì gọi mới; cổng không mở ⇒ huỷ tác vụ, bỏ kết quả, không hiện gì.
- Vì sao khởi ở lần `tim_kho` đầu, không phải "mọi câu về Huế" (hẹp hơn mức User đã chấp nhận): phủ 10 / 10 lượt web đã thấy, mà chỉ gửi ra ngoài ở 34 / 101 lượt (thay vì 101 / 101) — ít dữ liệu ra hơn,
  ít tiền hơn, lợi như nhau. Lượt kho từ chối ngay không tìm thêm (0 / 10 đã thấy) đi đường cũ.
- Không đổi: câu gửi Serper, hạn 5 s, một lần gọi / lượt không thử lại, lời dặn + lần gọi model viết mục web, mọi kiểm cuối bằng code, chuỗi gửi trợ lý.
- Không làm ở bậc này: viết sẵn mục web song song (thêm một lần gọi model cho mọi lượt tìm thêm — bậc riêng nếu S-A đạt và User muốn).

**Tiêu chí (ghi trước):**
- *Sàn bằng test, 0 USD:* (1) cờ tắt ⇒ hành vi + chuỗi gửi model giống byte; cờ bật ⇒ chuỗi gửi trợ lý **vẫn giống byte** (⇒ 0 câu Golden / an toàn chạm ⇒ không lượt Golden, không lượt an toàn có phí);
  (2) kho trả lời được ⇒ **không** sự kiện `web`, không mục web, tác vụ bị huỷ; (3) ≤ 1 lần Serper / lượt, lỗi / hết giờ ⇒ câu cố định như cũ, không gọi lại; (4) người dùng ngắt / lỗi giữa lượt ⇒ tác vụ bị huỷ, không rò;
  (5) lượt lịch, lượt nút, tuyến khác, câu khẩn cấp ⇒ không khởi; (6) log chỉ thêm số đếm: mục `tools` "tra_web" có `som`, `cho_ms`; lần bị bỏ ghi `bo: true` + USD — không chữ.
- *Chỉ số quyết (cấu trúc, ít nhiễu):* `cho_ms` = thời gian đường chính phải chờ Serper sau khi cổng mở. Mốc ≈ cả lần gọi (trung vị 2,2 s). Đạt khi **trung vị ≤ 0,3 s và ≥ 8 / 10 câu web ≤ 0,5 s**.
- *Chỉ số quyết thứ hai:* cả câu (`total_ms`, = lúc mục web tới) theo cặp từng câu, trung vị hiệu số biến thể − mốc **≤ −1,0 s và vượt nhiễu A/A** (nhiễu = trị tuyệt đối trung vị hiệu số giữa hai nửa lượt mốc).
- *Mức tụt cho phép:* câu thường (không tìm thêm) chữ đầu p50 không chậm quá **+0,3 s**; câu có tìm thêm mà kho trả lời được: cả câu không chậm quá +0,3 s; kết quả mục web theo loại (`co_muc` / `khong_tin_cay` / lỗi) trên 10 câu không tệ hơn mốc quá **1 câu** (kết quả Serper tự trôi giữa các lần gọi).
- *Theo dõi:* số lần Serper bị bỏ / lượt có tìm thêm (ước 24 / 34 ≈ 70 %) ⇒ USD thừa ≈ 0,0007 / lượt có tìm thêm ≈ **+0,00024 USD / lượt Huế**; báo cả USD / câu.
- *Giữ khi:* đủ sàn + hai chỉ số quyết + mức tụt. Không ⇒ gỡ cờ, tag hồ sơ.

**Đo** (qua server stream thật, cổng + cwd kiểm trước; nhắn nhóm "đang đo tốc độ"): bộ đã thấy B6 — 10 câu loại "web trả lời được" + 4 câu "kho có"; thêm 6 câu Golden model có tìm thêm mà kho trả lời được
(chọn bằng máy từ lượt mốc sáng nay, seed ghi trong report) + 6 câu thường. Mốc (cờ tắt) **3 lượt** rồi biến thể 3 lượt, xen kẽ theo lượt, cùng buổi, máy sạch ⇒ 26 câu × 6 = 156 lượt.
Trước đó một lượt mô phỏng 0 USD (Serper giả lập trễ 2 s trong test) để chắc harness + `cho_ms` đúng. **Tiền:** 60 lượt web × ~0,0025 + 96 lượt khác × ~0,0006 + Serper bị bỏ ≈ **0,22 USD**; dừng ở 0,25.

**Khi nào sai:** Serper nhanh hơn lần gọi trợ lý kế hầu hết thời gian ⇒ lợi đúng bằng một lần Serper, không hơn; provider chậm bất thường ⇒ `total_ms` nhiễu che lợi (vì thế `cho_ms` là chỉ số quyết chính);
câu hỏi ra ngoài nhiều hơn 3,4 lần hôm nay (34 so với 10 trên 101 lượt) — User đã chấp nhận, nhưng **bản công khai sau này phải quyết lại** (ghi vào checklist deploy).

**Rà khung AI FDE (S-A):**

| Mục | Hiện trạng | Khớp / lệch | Đề xuất |
|---|---|---|---|
| Đường ra: gửi gì | `tra_web.cau_tim_web`: câu hỏi lượt này, bỏ email / số điện thoại, ≤ 120 ký tự, không lịch sử | khớp — giữ nguyên hàm | test: câu gửi sớm = câu gửi hôm nay |
| Đường ra: gửi khi nào | `assistant.web_gate_open`: chỉ sau khi kho từ chối | **lệch có chủ đích** (User duyệt): gửi cả khi kho rồi trả lời được | chỉ khởi ở lần `tim_kho` đầu của model; đếm lần bị bỏ trong log |
| Hạn giờ, thử lại | `settings.yaml` `tra_web_timeout_seconds: 5`, một lần | khớp | giữ; tác vụ nền cùng hạn |
| Huỷ | chưa có tác vụ nền | mới | huỷ khi kho trả lời được / ngắt / lỗi; test rò tác vụ |
| Chữ web là dữ liệu | kiểm cuối bằng code trong `cong_web` + `tra_web.kiem_muc_web` | khớp — không chạm | kết quả sớm đi qua đúng các kiểm đó |
| Log | `chat_metrics` không nội dung | khớp | chỉ thêm `som`, `cho_ms`, `bo`, USD |
| Quyết bằng code hay model | cổng web do code quyết | khớp | model không được "xin" tra web |

## 2. S-B — gộp câu tìm (nhánh `p9-gop-cau-tim`, cờ `gop_cau_tim`, mặc định tắt) — chỉ bắt đầu sau khi S-A có kết luận

**Đổi một thứ:** công cụ `tim_kho` nhận **danh sách 1–3 câu tìm** trong một lần gọi (code đã có sẵn đường nhiều câu: `search_into_trace` ⇒ `search_many`, trộn RRF) + câu lời dặn đi kèm:
"còn thiếu nhiều phần ⇒ đưa hết các câu tìm trong **một** lần gọi". Trần 2 lần gọi, `max_turns`, "hết lượt tìm thì dừng", sổ nguồn: không đổi. Cờ tắt ⇒ giống byte.
- Khác hai bậc âm sáng nay: không hạ trần (bậc "trần 1" mất câu trả lời), không trông vào model tự gọi song song (1 / 176) — ở đây model được **nói rõ** cách lấy đủ trong một lần.
- Kiểm giả định trước lượt có phí (0 USD): 3 câu tìm trong một lần ⇒ số đoạn mới + token ngữ cảnh không vượt ngân sách (`ContextBudgetError` = 0 trên 37 câu Golden có tìm thêm, chạy riêng bước tìm);
  test mỗi loại lượt (đầu, hỏi tiếp có lịch sử, nhiều ý, lượt lịch) khẳng định chuỗi gửi model có / không phần mới đúng như trên.

**Tiêu chí (ghi trước; có mức nhiễu — bài học hai bậc âm: sàn không ghi nhiễu ⇒ không tách được nhiễu với lỗi thật):**
- *Câu chạm:* cờ bật đổi mô tả công cụ + lời dặn ở **mọi** yêu cầu trợ lý ⇒ Golden 176 + an toàn 32 (đếm băm yêu cầu bằng code trước khi chạy để xác nhận).
- *Luật "mới thật" cho mọi sàn đếm theo câu:* câu đổi trạng thái xấu đi so mốc (từ chối mới; ngoài kho bị trả lời mới; lỗi trích dẫn mới) ⇒ sinh lại **3 lần mỗi bên**; tính là mới thật khi biến thể xấu hơn mốc **≥ 2 lần trên 3 + 3**.
  Số câu phải sinh lại ghi trước: tối đa 10 câu (quá ⇒ kết luận âm luôn).
- *Sàn:* 0 lỗi kỹ thuật; 18 câu ngoài kho: 0 câu bị trả lời mới thật; an toàn 32 đủ 4 số, 0 đảo cảnh báo, 0 đổi lớp mới thật, "thiếu cảnh báo" theo thủ tục S-AT.
- *Mức tụt cho phép:* từ chối nhầm mới thật ≤ 1 câu; trên 37 câu có tìm thêm + các câu loại nhiều nguồn / so sánh: câu chữ khác mốc ⇒ một agent con chấm mù "đủ ý như mốc / thiếu ý", **thiếu ý ≤ 1 câu**.
- *Chỉ số quyết:* trên các câu mốc model tìm 2 lần (sáng nay 7 câu; đếm lại trên mốc mới — **< 6 câu ⇒ ghi trước là "có thể chỉ ra chưa rõ"**): số lần gọi trợ lý giảm ở **≥ 2 / 3 số câu** mà câu vẫn được trả lời;
  và cả câu theo cặp trên nhóm đó, trung vị hiệu số **≤ −1,0 s**.
- *Theo dõi:* số câu tìm / lần gọi; USD / câu; chữ đầu qua server stream 5 câu tìm 2 lần × 5 lượt mỗi bên (mốc sạch cùng buổi).
- *Giữ khi:* đủ sàn + mức tụt + chỉ số quyết. Tối đa **1 vòng chỉnh chữ** lời dặn nếu trượt vì model không gộp; trượt sàn chất lượng ⇒ dừng, không chỉnh.

**Đo:** mốc Golden 176 ×1 trên kho hiện tại (kho đổi 2 câu sau lượt mốc sáng ⇒ không dùng lại) ≈ 0,075 · biến thể 176 ≈ 0,075 · an toàn 32 ≈ 0,022 · sinh lại ≤ 10 câu × 6 ≈ 0,02 · chữ đầu 50 lượt ≈ 0,03
⇒ **≈ 0,22 USD**, dừng ở 0,25. `DRY=1` trước mọi lệnh có phí; cờ bật tạm trong `settings.yaml` của worktree rồi trả lại (lệnh `--flags` không dựng được hàm dự báo).

**Khi nào sai:** ba câu tìm trộn RRF đẩy đoạn đúng của ý chính ra khỏi phần được đưa vào ⇒ thiếu ý (chấm mù bắt); model gộp nhưng vẫn gọi lần hai ⇒ lợi 0; model coi "gộp" là "tìm ít đi" như sáng nay ⇒ từ chối tăng (sàn bắt).

## 3. Hồ sơ và báo cáo

Mỗi bậc: report `report_agent/2026-11-12_ra_khoang_cach/b_web_som_implementation.md` / `b_gop_cau_tim_implementation.md` (thời gian từng bước, tiền thật từ log lọc theo `git_sha`), review cả nhánh một lần,
kết quả âm ⇒ tag `hoso/…` + 1–3 dòng ở sổ khâu 07 và bài 19; đạt ⇒ A trình User bật cờ. Dữ liệu đo: `data/toc_do_web_som_2026-11-15/`, `data/toc_do_gop_tim_2026-11-15/`.
