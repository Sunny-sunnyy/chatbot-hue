# Implementation Report: Phase 9 T3 — bảng vé + giờ mở cửa (`tra_ve_gio`) — **ÂM theo luật ghi trước** sau vòng 3 (User duyệt): Q2 19 / 20 ✓ nhưng **Q3 sàn trượt 6 / 10** — cờ tắt

Người làm: C (Claude Code, `hue-rag-e9`) · 08/11/2026 (code 11:12 → đo xong 11:36 — `date`)
Nhánh `p9-t3-bang` = `7ae4faf` (từ `main` `de10c6b`, đã push; cờ `tra_ve_gio: false`). Plan bản 2 `dbcd1a2f6d81` (A duyệt). Luật đo nhẹ (User 08/11, `Session_Prompt.md` §7–§8):
Q2 mốc 1 + nhánh 1 lượt. Tiền lượt này **0,025679 USD** (Q2 mốc 0,012847 + nhánh 0,012832, từ `chat_metrics.usd`). Repo public: không chép kho / câu bộ đo.

## 1. Dữ liệu (User duyệt 08/11 câu 1; A theo khuyến nghị câu 2–5)

- `data/phase_9/t3_bang_ve_gio/bang_v1.json` sha256 `874af96dd995` (private): 60 điểm, 161 dòng vé, 119 dòng giờ (gồm 9 điểm dùng **giờ chung Quần thể**, ghi rõ), 28 điểm
  đánh dấu "nguồn ghi khác nhau", 59 mục quy định chung áp cho nhóm Quần thể; bỏ 6 sự kiện đã diễn ra. Nháp `bang_nhap.json` kiểm **1.011 / 1.011** chuỗi có thật ở đúng
  file:dòng (`tools/kiem_nhap.py`, đọc kho qua `scripts/grep_kb.sh`); `tools/chot_v1.py` chứng minh v1 không thêm dòng nào ngoài nháp.

## 2. Code (`7ae4faf`, 0 USD)

`backend/llm/ve_gio.py` (mới: nạp + khớp tên / bí danh, cổng từ khoá, trường gửi model ↔ khối code, khối điều kiện nguyên văn, kiểm số tiền + giờ trong ngày) · `assistant.py`
(cờ + bảng chỉ nạp khi cờ bật, `ve_gio_for_turn`, nguồn mỗi file kho một nguồn — `source` = file kho, `_ve_gio_cuoi`: kiểm số ⇒ rút lại như thời tiết, câu từ chối có dòng ⇒
câu dẫn + dòng, `OUT_OF_SCOPE_ANSWER` ⇒ không khối, `chu_cua_model` bóc khối, stream giữ chữ từ chối) · `generator_openai_full_corpus.py` (công cụ thứ tư + `max_turns_cho`: +1 có
`tra_ve_gio`, +1 nữa khi cùng có `thoi_tiet` — n-1) · `settings.yaml` (cờ tắt + đường dẫn) · `tests/test_t3_ve_gio.py` (36 ca).

## 3. Kiểm 0 USD

| Kiểm | Kết quả | Thời gian |
|---|---|---|
| `test_t3_ve_gio.py` | **36 passed** — gồm rút lại khi bịa giá trên **cả 3 đường** (`/api/chat`, stream, song song), câu từ chối có dòng ⇒ câu dẫn (stream không lộ câu từ chối), dòng miễn phí không vào chuỗi gửi model, nguồn có `bai_id`, cổng từ khoá (10 câu dương + 6 câu thường âm + 6 / 6 câu miễn giảm của bộ an toàn trúng), `max_turns` | ~15 s |
| 12 file test bị chạm | **542 passed / 1 failed** — failed `test_cong_dot_1.py::test_weather_and_feature_routes` (`anh: True ≠ False`) **cũng hỏng trên `main` `099c756` khi chạy cả file** (C chạy); chạy riêng thì đạt ⇒ phụ thuộc thứ tự, không do nhánh | 2 phút 42 giây |
| Q1 (`capture_all.py`) | cờ tắt **228 / 228** giống byte `main` `806b5df`; cờ bật: **181 / 181** câu không từ khoá giống byte; đúng 45 câu có từ khoá được đưa công cụ (Golden 30 / 176 · an toàn 13 / 32 · smoke 2 / 10) | 3 lần chụp × ~1–2 phút |

## 4. Lượt có phí — Q2 (20 câu, ghi nhãn trước `do/bo_t3.jsonl` md5 `c89955f1bed9`; server thật `/api/chat/stream`)

| | Mốc `main` | Nhánh (cờ bật) |
|---|---|---|
| Q2 đạt (luật plan: mọi số tiền / giờ ∈ dòng bảng của điểm nhãn ∧ có số nhãn ∧ không rút lại) | 16 / 20 | **17 / 20** (≥ mốc ✓, **< 19 / 20** ✗) |
| Model gọi `tra_ve_gio` | — | **2 / 20** |
| Q3 khối điều kiện ở 4 câu miễn giảm / đối tượng | 0 / 4 | **0 / 4** ✗ (khối chỉ có khi công cụ được gọi) |
| rút lại · `max_turns` | 0 · 0 | 0 · 0 |
| USD | 0,012847 | 0,012832 |

Chữ đầu (chỉ ghi, **không** là S5 — A: máy đang đo việc khác): mốc p50 2,1 s / p95 8,5 s · nhánh p50 2,8 s / p95 10,3 s.

**Sửa bộ chấm (không chạy lại lượt có phí):** bản chấm đầu báo gần mọi câu "tiền ngoài bảng" ở **cả hai** nhánh vì (1) nhãn giá ghi thiếu đơn vị ("200.000") ⇒ bộ nhận tiền
không đọc được nhãn; (2) tập cho phép chỉ gồm số nhãn, hẹp hơn luật plan ("∈ dòng nhãn của câu"). Sửa theo đúng chữ plan (mọi dòng bảng của điểm nhãn, giá kèm đơn vị) rồi
chấm lại cùng dữ liệu. Code runtime không bị ảnh hưởng (dòng gửi model có đơn vị).

## 5. Đọc kết quả

- **Quan sát:** model trả lời giá / giờ từ đoạn kho của lần tìm đầu (`lan_tim_dau: v0` — đoạn bảng vé thường đã có trong 10 đoạn) ⇒ hiếm khi gọi công cụ thứ tư; Q2 nhánh
  ≈ mốc (17 ↔ 16). Phần T3 thật sự thêm giá trị — **khối điều kiện nguyên văn** và **kiểm số theo bảng** — chỉ chạy khi model gọi ⇒ 0 / 4 câu miễn giảm có khối.
- **Theo luật ghi trước:** Q2 < n − 1 và Q3 trượt ⇒ **âm** ở lượt 1; cờ giữ tắt. Không chạy S1 / S4 cho biến thể này (tiết kiệm ≈ 0,1 USD — biến thể đã trượt sàn).
- **Giả thuyết (chưa chứng minh):** để model quyết gọi là sai chỗ theo khung AI FDE ("thứ tự bắt buộc ⇒ code") — khi code đã thấy từ khoá vé / giờ **và** dò được tên điểm
  trong câu, việc tra bảng là bắt buộc, không cần phán đoán.

## 6. Hướng tiếp (A / User quyết)

- **(a) Phương án B của spec:** bảng chỉ cho kiểm cuối (không công cụ) — code kiểm số trong câu trả lời so với bảng, sai ⇒ câu cố định "giá / giờ có thể khác — xem nguồn".
- **(b) Vòng chỉnh 2 (plan cho phép tới 2 vòng):** **code tự tra** khi câu có từ khoá **và** code dò được ≥ 1 tên điểm của bảng trong câu (khớp nguyên tên / bí danh trong
  chữ) ⇒ dòng bảng thành nguồn **trước** lần sinh (như lần tìm đầu) + khối điều kiện + kiểm số như hiện có; công cụ giữ cho câu code không dò ra tên. Đo lại Q2 (2 × 0,013) rồi
  S1 ×2 + S4 (≈ 0,1). C khuyến nghị (b): giữ đúng hai giá trị T3 (khối nguyên văn + kiểm số) mà không phụ thuộc model.

## 7. Bằng chứng (private)

`data/phase_9/t3_bang_ve_gio/`: `bang_v1.json`, `phieu_cho_user.md`, `q1/` (3 bản chụp + `khac_bat.json`), `do/bo_t3.jsonl`, `do/q2_moc_main.jsonl` / `.cham.json`,
`do/q2_nhanh.jsonl` / `.cham.json`, `tools/` (`kiem_nhap.py`, `gop.py`, `chot_v1.py`, `do_t3.py`).

**Giải thích ngắn:** bảng vé / giờ đã dựng và kiểm từng chữ với kho; code đọc bảng đúng (test, 3 đường). Nhưng khi để model tự quyết có tra bảng hay không, nó gần như không
tra (2 / 20) vì kho đã có giá — nên phần quan trọng (điều kiện miễn giảm chép nguyên văn, kiểm số) không chạy. Đề xuất: code tự tra khi thấy tên điểm + câu hỏi về vé / giờ.


## 8. Vòng chỉnh 2 (cuối) — A chọn (b) 08/11

**Ghi rõ (A yêu cầu):** (1) đây là vòng 2, **vòng cuối** của plan — trượt ⇒ phương án B; (2) **bộ chấm sửa sau khi thấy dữ liệu lượt 1**, hai chỗ, mỗi chỗ khớp chữ plan:
(a) tập số hợp lệ = **mọi** số trong các dòng bảng (vé + giờ) của điểm nhãn — đúng chữ plan Q2 "mọi số tiền / giờ trong chữ ∈ **dòng nhãn** của câu" (bản đầu chỉ lấy số nhãn ⇒
hẹp hơn plan); (b) chuỗi giá của nhãn kèm đơn vị như bảng — để bộ nhận tiền (`so_tien.py`, cần đơn vị) đọc được; không đổi luật, chỉ đổi cách đọc nhãn. **Không sửa gì
thêm sau lượt 2.**

- **Đổi một thứ:** câu có từ khoá vé / giờ **và** code dò được ≥ 1 tên / bí danh điểm của bảng trong câu (hoặc câu hỏi liền trước) ⇒ **code tự tra**: dòng bảng thành nguồn nối
  cuối ngữ cảnh **trước** lần sinh (`tra_truoc`, `by="code"`); công cụ chỉ còn cho câu có từ khoá mà code không dò ra tên. Khối điều kiện, kiểm số, câu từ chối giữ nguyên.
- Commit `c706c2f` (rebase lên `main` `f124527`, đẩy lại nhánh). Test T3 **43 passed**; 12 file test **549 passed / 1 failed** (cùng `test_cong_dot_1::test_weather_and_feature_routes`
  — C kiểm: **chỉ hỏng khi nạp khoá** `--env-file` (có khoá ⇒ ảnh bật ⇒ `anh: True`); không khoá ⇒ cả file 22 / 22; hỏng sẵn, không do nhánh). 2 phút 10 giây.
- **Q1 (đổi chuỗi gửi model ⇒ chạy lại):** cờ tắt **228 / 228** giống byte (mốc `main` `806b5df` **dùng lại** — `backend/` không đổi `806b5df..f124527`, `git diff --stat` rỗng);
  cờ bật **181 / 181** câu không từ khoá giống byte; 45 câu có từ khoá: **21 code tự tra** (Golden 12 · an toàn 7 · smoke 2) · 24 đưa công cụ. 51 giây.
- **Q2 vòng 2** (cùng bộ 20 câu, cùng bộ chấm, server thật, 71 giây, **0,011858 USD**):

| | Mốc `main` | Vòng 1 | **Vòng 2** |
|---|---|---|---|
| Q2 đạt | 16 / 20 | 17 / 20 | **18 / 20** (≥ mốc ✓, **< 19** ✗) |
| Bảng được tra (code / model) | — | 2 / 20 | **19 / 20** |
| Q3 khối điều kiện (4 câu miễn giảm / đối tượng) | 0 / 4 | 0 / 4 | **4 / 4** ✓ |
| rút lại · `max_turns` | 0 · 0 | 0 · 0 | 1 · 0 |
| chữ đầu (chỉ ghi, không là S5) | p50 2,1 / p95 8,5 s | 2,8 / 10,3 s | 2,8 / 4,1 s |

- **2 câu không đạt — đọc chữ:**
  - **T05 (rút lại):** chữ model đúng (giá vé tuyến 3 điểm + giá trẻ em, trích đoạn kho). Bị rút lại vì **lỗi của kiểm cuối runtime**: code dò ra 3 điểm lẻ (không phải vé
    tuyến) nên dòng gửi model không có giá tuyến; giá có trong đoạn kho được trích, nhưng bảng giá trong kho ghi số **không kèm "đồng"** ⇒ `tim_so_tien` không nhận số ở đoạn
    trích ⇒ tập cho phép thiếu. Sửa 1 dòng: tập cho phép thêm số nhóm nghìn trần (`\d{1,3}(\.\d{3})+`) như thời tiết dùng `tap_so`. **Chưa sửa** (vòng cuối; A / User quyết).
  - **T14 (số ngoài dòng nhãn):** chữ model đúng — thêm giá vé Đại Nội có trích dẫn kho ("chưa gồm vé vào Đại Nội …"). Luật Q2 ghi trước chỉ cho số trong dòng bảng của điểm
    nhãn ⇒ trượt (mốc `main` trượt đúng câu này). Kiểm cuối runtime cho qua (số có trong đoạn kho được trích) — đúng thiết kế.
- **Theo luật ghi trước:** vòng 2 **âm** (18 < 19) ⇒ theo plan: phương án B, cờ tắt. **Quan sát cho A / User:** cả 2 câu trượt có chữ đúng; 1 câu do lỗi code đã rõ nguyên nhân
  (sửa 1 dòng), 1 câu do luật chấm chặt hơn kiểm runtime. Phần giá trị chính của T3 (khối điều kiện nguyên văn) đạt 4 / 4. Quyết giữ âm (phương án B) hay sửa lỗi T05 + đo lại
  (vòng thứ ba — ngoài plan) là của A / User.
- **Chưa chạy:** S1 (an toàn 32 ×2 + mốc), S4 (mẫu 30), S5 (A xếp riêng) — lệnh ở `STATUS_C.md`.
- Tiền T3: vòng 1 0,025679 + vòng 2 0,011858 = **0,037537 USD**.


## 9. Vòng 3 — User duyệt 08/11 (ngoài plan), lý do = sửa lỗi code thật, **không nới sàn / luật chấm**

- **Sửa:** `kiem_so` — phía cho phép nhận thêm số nhóm nghìn **trần** ("420.000") từ đoạn kho được trích, như thời tiết dùng `tap_so` (lỗi T05 vòng 2: ô bảng giá kho không kèm
  "đồng" ⇒ `tim_so_tien` bỏ qua ⇒ rút lại oan một câu đúng). Commit `21ec06d` (pushed). Test: 3 ca mới (số trần được phép · số khác vẫn bị bắt · năm / giờ không thành số tiền);
  `test_t3_ve_gio.py` + `test_b5b_thoi_tiet.py` **130 passed**. Chỉ chạm kiểm **sau** lần sinh ⇒ chuỗi gửi model không đổi ⇒ **không chạy lại Q1** (luật §8 User 08/11).
- **Q2 vòng 3** (cùng bộ, cùng bộ chấm, server thật, 83 giây, **0,012194 USD**): **19 / 20** ✓ (≥ n − 1 và ≥ mốc 16) · rút lại 0 · `max_turns` 0 · bảng tra 19 / 20 · khối điều kiện 4 / 4.
  Câu trượt duy nhất: T14 (luật chấm như ghi trước; mốc `main` trượt cùng câu).
- **Q3 (sàn "0 câu model tự nêu điều kiện ngoài khối") — TRƯỢT:** sub-agent mới đọc 10 câu code gắn cờ (luật ghi trước: nhãn hàng giá "trẻ em 7–12 tuổi: …" không tính) ⇒
  **6 / 10 có** (T01, T06, T07, T08, T19, T20 — model tự viết "trẻ dưới 7 tuổi miễn phí", "người dân Huế giảm 50 %", "người cao tuổi giảm 50 %", "học sinh ngoại khoá miễn"…)
  — `do/q3_cham.json`. **Nguyên nhân (suy luận, chưa chứng minh):** thiết kế chỉ giữ chữ điều kiện **của bảng** ngoài model; **đoạn kho** của lần tìm đầu vẫn chứa điều kiện
  miễn giảm ⇒ model chép từ đó. Sub-agent ghi T06 "trẻ em 7–12 tuổi được miễn phí" có thể **sai** với nguồn (bảng: 30.000 / 40.000 cho 7–12 tuổi tuỳ điểm) — chưa kiểm.
- **Lỗi công cụ đo của C (ảnh hưởng mọi lượt Q2 — mốc + 3 vòng):** `do_t3.py` dùng **một** `httpx.Client` ⇒ cookie giữ ⇒ 20 câu chạy trong **một cuộc trò chuyện** (nhớ 3
  câu hỏi trước), trái chú thích "mỗi câu cuộc mới". Mốc và nhánh cùng điều kiện ⇒ so sánh vẫn cùng thước, nhưng số không phải "câu độc lập". Sửa lần sau: client mới mỗi câu.
- **Lỗi thiết kế lộ ra nhờ lỗi trên (T17):** đường code tự tra lấy điểm của **câu hỏi liền trước** khi câu này không nêu tên ⇒ người dùng đổi chủ đề (hỏi chợ rồi hỏi chùa) vẫn bị
  nối dòng "nguồn ghi khác nhau ở … Chợ Đông Ba" — sai ngữ cảnh. Sửa khả dĩ: chỉ lấy câu trước khi câu này **không** có danh từ địa điểm nào khác / bỏ hẳn fallback.
- **S1 (an toàn 32):** đã **sinh** nhánh ×2 (`tools/an_toan_t3.py` — công cụ mới vì `an_toan_run.py` cũ gọi cờ mặc định = RAG 1–8; `do/s1_nhanh/`, **0,035522 USD**); **chưa chấm
  4 số, chưa chạy mốc** (dừng vì Q3 đã trượt sàn + hết phiên). S4, S5: chưa chạy.
- **Theo luật ghi trước + lời User ("vẫn trượt ⇒ giữ cờ tắt, phương án B"):** Q2 đạt nhưng **Q3 là sàn và trượt** ⇒ **âm** ⇒ cờ `tra_ve_gio` tắt; A / User chọn: phương án B
  (bảng chỉ cho kiểm cuối) hay việc mới (thiết kế lại cách giữ điều kiện ngoài model — vd lọc câu điều kiện khỏi chữ model bằng code, hoặc chấp nhận model nêu điều kiện khi có
  trích dẫn kho và đổi sàn ⇒ User duyệt).
- **Tiền T3:** vòng 1 0,025679 · vòng 2 0,011858 · vòng 3 0,012194 · S1 sinh 0,035522 = **0,085253 USD** (trần 0,20).
- **Thời gian:** pytest rộng 2 phút 10–42 giây; Q1 51 giây / lần; Q2 70–90 giây / lượt; S1 sinh 6 phút 16 giây (2 × 32 câu); Playwright: không (không sửa giao diện).


## 10. Kiểm thêm sau vòng 3 (A giao, 0 USD)

- **Câu sub-agent nghi sai (T06 "trẻ em 7–12 tuổi được miễn phí" — Bảo tàng Cổ vật Cung đình Huế): ĐÚNG với kho.** `scripts/grep_kb.sh --dir travel/tickets`: file vé Quần thể
  dòng 24 tiêu đề cột "Giá vé trẻ em từ 7–12 tuổi", dòng 33 hàng Bảo tàng Cổ vật = 50.000 · **Miễn phí**. Mốc `main` và nhánh trả lời cùng nội dung ⇒ **không** phải lỗi đang chạy.
  (Q3 vẫn đếm câu này là "model tự nêu điều kiện" theo luật ghi trước — luật đo chỗ chữ điều kiện, không đo đúng / sai.)
- **Sửa lỗi đo `do_t3.py`:** mỗi câu một `httpx.Client` mới ⇒ không cookie ⇒ mỗi câu một cuộc trò chuyện riêng (probe 0 USD: client mới không mang cookie). **Các lượt đã chạy**
  (mốc + vòng 1–3) đều chạy **trong một cuộc** với cùng công cụ ⇒ cùng thước, so sánh giữa chúng vẫn hợp lệ; nhưng số không phải "câu độc lập" — lượt đo sau dùng bản đã sửa.

## 11. Giới hạn (cập nhật)

- **Lỗi thiết kế T17 — lưu ý gắn điểm cũ khi đổi chủ đề:** đường code tự tra lấy điểm của **câu hỏi liền trước** khi câu này không nêu tên điểm của bảng ⇒ người dùng hỏi chợ rồi
  hỏi chùa (không có trong bảng) vẫn bị nối dòng "nguồn dữ liệu ghi khác nhau ở … Chợ Đông Ba". Lộ ra vì lượt đo chạy trong một cuộc. Hướng sửa (chưa làm): chỉ dùng câu trước khi
  câu này là câu hỏi tiếp không nêu địa điểm nào (vd "còn giờ mở cửa?"), hoặc bỏ fallback.
- Q3 trượt vì đoạn kho của lần tìm đầu vẫn chứa điều kiện miễn giảm (thiết kế chỉ giữ chữ điều kiện **của bảng** ngoài model) — chọn hướng ở "Câu hỏi cho User" (A ghi handoff).
- S1 mới sinh nhánh ×2 (`do/s1_nhanh/`), chưa chấm / chưa mốc; S4, S5 chưa chạy.

## 12. Hướng (a) — "phương án B" của spec (User chọn 09/11, A giao; viết 20:32 09/11/2026 — `date`)

**Đổi gì (commit `4bc2e5f`, nhánh rebase lên `main` `5c982a0`, cờ `tra_ve_gio` tắt):** bỏ công cụ `tra_ve_gio`, bỏ "code tự tra" trước lần sinh, bỏ khối điều kiện miễn
giảm, bỏ thay câu từ chối. Bảng chỉ dùng **sau** khi model viết: câu (hoặc câu hỏi liền trước) có từ khoá vé / giá / giờ ∧ chữ model không phải câu từ chối / ngoài phạm
vi ∧ lượt không có lịch ⇒ kiểm số tiền + giờ trong chữ model ⊂ dòng bảng của điểm **nêu trong câu này** ∪ mọi đoạn kho đã đưa model ∪ câu hỏi; lệch ⇒ nối câu cố định
"Lưu ý: giá vé / giờ mở cửa nêu trên có chỗ chưa khớp bảng vé và nguồn dữ liệu, có thể khác thực tế — hãy xem phần Nguồn hoặc hỏi nơi đến trước khi đi." (không rút lại câu
trả lời). Không lấy điểm từ câu hỏi liền trước (sửa lỗi gắn điểm cũ §11). Log: một mục `tools` `kiem_ve_gio` (số điểm + mã lỗi, không chữ).
`generator_openai_full_corpus.py` trở về đúng bản `main`.

**0 USD (đã chạy):** test T3 41 đạt (19 giây); 7 file lõi (b2 / b5 / b5b / b6 / ngày / feedback / b3) 511 đạt (76 giây). **Q1 cờ BẬT giống byte `main` 228 / 228**
(`capture_all.py`, `data/phase_9/t3_bang_ve_gio/q1_a/`, 27–31 giây / lần) ⇒ cờ bật không đổi gì gửi model.

**Tiêu chí ghi trước lượt có phí** (A 09/11: đo 20 câu + bộ an toàn 32; ×2 chỉ khi S-AT đòi; bỏ S4 vì chuỗi gửi model giống byte):
- **Cách đo ghép cặp trong cùng một lượt:** Q1 chứng minh lần sinh của nhánh = lần sinh của `main` ⇒ "mốc" của mỗi câu là **chính phần chữ model** của câu đó (bỏ câu lưu ý),
  "nhánh" là chữ hiện cho người dùng. Không chạy mốc riêng; không dùng lại mốc 08/11 (không cần).
- **K2 báo nhầm:** câu Q2 đúng theo bộ chấm (`do_t3.py cham`, nhãn 08/11) mà vẫn bị gắn lưu ý **≤ 2 / 20**.
- **K3 bắt lệch (quan sát, không sàn):** câu bộ chấm thấy số ngoài nhãn mà không có lưu ý — ghi số + lý do (số có trong đoạn kho đã đưa model ⇒ đúng thiết kế).
- **K4:** 0 câu bị rút lại / đổi chữ model do T3 (chữ hiện = chữ model [+ lưu ý]).
- **S1 (bộ an toàn 32, ×1, cờ bật):** ngoài kho bị trả lời **0** (so với câu chuẩn); mọi câu có lưu ý ⇒ sub-agent đọc mù: lưu ý không đảo / không làm thiếu cảnh báo, không thêm
  điều kiện sai. Phần chữ model giống `main` theo Q1 ⇒ 4 số trên phần đó là tính chất của `main`, không do T3. Chênh 1 ở bất kỳ số nào ⇒ thủ tục S-AT (chạy ×2).
- **Đạt** = K2 + K4 + S1. Q2 đạt / 20 chỉ báo số (model không đổi ⇒ dự kiến ≈ mốc 16 / 20).

**Kết quả lượt có phí (viết 20:43 09/11/2026 — `date`; trên `4bc2e5f`, cờ bật tạm trong worktree, đã trả `false`):**

| Tiêu chí | Kết quả | |
|---|---|---|
| K1 Q1 cờ bật giống byte `main` | 228 / 228 | ✓ |
| K2 câu đúng mà bị gắn lưu ý (≤ 2 / 20) | **0 / 20** (lưu ý bật 0 / 20) | ✓ |
| K3 bộ chấm thấy số ngoài nhãn, không lưu ý (quan sát) | 3 / 20 (T04, T06, T14) — runtime cho qua vì số có trong đoạn kho đã đưa model (đúng thiết kế; T06 đã kiểm 08/11 là đúng kho) | — |
| K4 câu bị rút lại / đổi chữ model do T3 | 0 / 20 · 0 / 32 | ✓ |
| S1 ngoài kho bị trả lời | **0 / 4** (code, so câu chuẩn); 0 lỗi citation / lỗi chạy trên 32 | ✓ |
| S1 câu có lưu ý | 1 / 32 (một câu loại "giờ") — **báo nhầm** do lỗi code thật (dưới) | ✗ ⇒ sửa |
| Q2 đạt (báo số) | 15 / 20 (mốc 08/11 16 / 20; 2 câu miễn giảm không số nhãn trượt theo luật chấm cũ đòi khối điều kiện — hướng (a) không còn khối) | — |
| Tiền · thời gian | Q2 0,010562 USD / 69 giây · an toàn 32 0,017105 USD / 3 phút 49 giây | |

**Lỗi tìm được bằng lượt thật (sửa `e547b9e`):** bộ đọc giờ (và bộ đọc số tiền trần "420.000") chặn mọi số đứng trước dấu phẩy — luật nhằm bỏ số thập phân "7,5" nhưng bắt
cả liệt kê "17:20, 18:00" ⇒ giờ trong kho không được đọc ⇒ câu trả lời đúng kho bị gắn lưu ý. Tái tạo: chữ model 9 giờ khởi hành, dòng kho chứa cả 9 (đọc qua `grep_kb.sh`)
⇒ bản cũ đọc model 2 giờ / kho 1 giờ ⇒ `gio_ngoai_bang`; bản sửa đọc 9 / 9 ⇒ `[]`. Ranh giới mới: trước không là chữ số / "chữ số + . ,", sau không là chữ số / ". ," + chữ số
("7,5" vẫn không thành giờ). +3 ca test; test T3 44 đạt. Lỗi này có từ vòng 1 (cả kiểm cuối vòng 1–3).

**Đọc kết quả (quan sát):** trên 52 câu thật, lưới kiểm **chưa bắt được một số sai nào** — lần bật duy nhất là báo nhầm do lỗi trên. Hướng (a) an toàn theo thiết kế (không đổi
chuỗi gửi model, không rút lại), nhưng lợi đo được ≈ 0 ⇒ đề xuất A hỏi User: merge cờ tắt (giữ làm lưới) hay đóng hồ sơ. Chạy lại an toàn 32 ×1 trên `e547b9e` để có số sau sửa:
**chưa chạy** (A dặn không mở lượt mới tới khi chốt vòng tự soi). Chấm mù 2 người bộ 32: không làm — chữ hiện = chữ model (giống `main` theo Q1) trừ câu lưu ý ⇒ số "mới" = 0
theo định nghĩa (C đề xuất trong vòng tự soi, chờ A chốt).
Data private: `data/phase_9/t3_bang_ve_gio/q1_a/`, `do/q2_nhanh_a.jsonl` (+ `.cham.json`), `do/s1_a/`.

## 13. Kết luận — ĐÓNG HỒ SƠ, không merge (User chọn, A báo C; ghi 20:50 09/11/2026 — `date`)

- **Đo gì:** T3 thử 4 cách dùng bảng vé + giờ User duyệt (60 điểm): (1) công cụ model tự gọi — model gọi 2 / 20, Q2 17 / 20 < 19; (2) code tự tra trước lần sinh — Q2 18 / 20;
  (3) vòng 3 sửa kiểm cuối — Q2 19 / 20 nhưng sàn Q3 trượt 6 / 10 (model tự nêu điều kiện miễn giảm chép từ kho); (4) hướng (a) = phương án B của spec — bảng chỉ kiểm số
  sau khi model viết, chuỗi gửi model giống byte `main`.
- **Ra gì (hướng (a), 52 câu thật):** an toàn theo thiết kế (0 rút lại, ngoài kho bị trả lời 0 / 4), nhưng lưới kiểm **chưa bắt được số sai nào**; lần bật duy nhất là báo nhầm do
  lỗi bộ đọc giờ (đã sửa `e547b9e`, không đo lại theo chỉ thị).
- **Vì sao đóng:** lợi đo được ≈ 0 so với `main` mà thêm ~120 dòng code + một bảng private phải giữ đúng theo kho. Model ở `main` đã chép giá / giờ từ đoạn kho khá đúng
  (mốc Q2 16 / 20; câu trượt chủ yếu do thiếu / chọn sai dòng, không do bịa số).
- **Giữ lại để dùng sau:** nhánh `p9-t3-bang` = `e547b9e` (A gắn tag `hoso/p9-t3-bang` + xoá nhánh khi User duyệt); bảng `data/phase_9/t3_bang_ve_gio/bang_v1.json`
  (`874af96dd995`, User duyệt) — dùng lại được nếu sau này cần kiểm cuối số cho tính năng khác; bài học: **kiểm bằng code trên lượt thật nhỏ trước khi kết luận** (lỗi dấu
  phẩy chỉ lộ ở dữ liệu thật); bộ đọc số liệt kê nên dùng lại cách ranh giới mới nếu `thoi_tiet` / `tra_web` có lỗi tương tự (chưa kiểm).
- **Tiền T3 cả đợt:** 08/11 0,085253 + 09/11 0,027667 ≈ **0,113 USD**.
