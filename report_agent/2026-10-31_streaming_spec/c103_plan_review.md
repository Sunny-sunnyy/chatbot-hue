# Review: plan lượt đo cuối Phase 1–8 (C103 bản 2)

Decision: **changes_requested** (0 blocker / 1 major / 6 minor) · Người kiểm: B (Claude Opus 5.5) · Date: 11:32 01/11/2026 (`date`)
Bản kiểm: `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` **`ba70843a4652`** (B tự tính `sha256sum`; file untracked, 212 dòng).
Cách review (`WORKFLOW.md` §9.1): **chỉ** gói "Căn cứ để review" của plan — plan toàn bộ; `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` §1–§3 + phụ lục;
`report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` §1, §2, §5, §7; spec streaming `00fb57ee01b2` §6 C1–C3, C6 (B đã đọc khi làm S1 / S2) — cộng lệnh chỉ đọc
trên dữ liệu private. **Không** đọc `STATUS_C.md`, tin nhắn của C. Không mở câu kín. 0 USD.

## 1. Phạm vi đã review

Tiêu chí ghi trước (sàn / mức tụt / theo dõi) của §3.1–§3.8, cỡ mẫu, điều kiện "cùng một commit" §2, giữ mù bộ kín mới §3.7, thứ tự §5, tiền §6, câu hỏi User §11.
Không review: nội dung các plan "thử thêm" §4 (chưa có), phương án streaming (spec riêng).

**Đạt (đối chiếu được):**
- Ba lớp tiêu chí đủ cho Golden (F1–F4, T1–T3 giữ đúng như plan đợt 2 §5; A/A = 2 ⇒ ≤ 5 câu khớp `BAO_CAO_DANH_GIA.md` §1 "Đủ tụt 1, Đúng tụt 2") và bộ an toàn (A1, A2 hai vế,
  N_AA = 2, thủ tục (i)/(ii)/(iii) dẫn đúng plan đợt 2 §5).
- Cỡ mẫu số chính **129 trong kho + 18 ngoài kho**: B tính lại từ `data/phase_8_1/golden_realism_final.jsonl` (82 / 65 / 29) + Golden ⇒ 147 câu, đúng 129 + 18.
- Cận trên Clopper–Pearson một phía 95 %: 0 / 6 ⇒ 0,393 ✓; 0 / 28 ⇒ 0,1015 ✓ (B tính lại).
- Tiền §6: tổng 0,0763 / 0,1128 cộng đúng.
- Giữ mù bộ kín mới: người viết / kiểm / judge là sub-agent mới, người chạy chỉ in số đếm, tên `*sealed*` (hook quét), so SHA256 với mọi `question` cũ, khóa manifest trước — đủ ý, khớp
  luật `Session_Prompt.md` §5. Không dùng bộ kín để chọn biến thể (§4) ✓.
- Bộ "trước" của §3.1 có thật: `data/sua_kho_2026-10-27/dot2/eval_sau/sau_all.jsonl` (176 dòng; meta: commit `751b352`, build record `51fb1ec63cbc`, `gpt-6-luna`).

## 2. Findings

**M-1 (major) — §3.2 Sàn A2 vế 1: "sinh lại được cả hai bên" không nói bên mốc sinh lại trên commit nào.**
- Vị trí: plan dòng 59–60. Yêu cầu bị ảnh hưởng: tiêu chí ghi trước phải quyết được mà không chọn sau khi thấy số (`run-experiment`; plan đợt 2 §5 A2 vế 1 — mốc sinh lại trên **kho /
  code của mốc**).
- Bằng chứng: mốc 30/10 sinh bằng commit `751b352` (meta `sau_all.meta.json`); bên "sau" là commit §2 (sau S1–S4 + `cost_usd`). Plan chỉ nói "index không đổi nên sinh lại được cả hai
  bên". Nếu sinh lại "mốc" trên chính commit §2 thì hai bên cùng là "sau" ⇒ phép so "mới so với mốc" mất nghĩa; nếu trên `751b352` thì cần worktree + kiểm build record — plan không ghi.
- Tác động: ca có câu P0_sai mới (chính là ca sàn cần quyết) mở đường chọn cách sau khi thấy kết quả.
- Tiêu chí đóng: ghi rõ "bên mốc sinh lại 3 lần trên commit `751b352` (worktree riêng, cùng build record `51fb1ec63cbc` / sparse `c8134c49a648`, kiểm T1 trước), bên 'sau' trên commit §2",
  hoặc lý do chọn khác — trước khi chạy.

**m-1 — §3.4 "Theo dõi thêm: `total_ms` … qua API (log `chat_metrics`) trên lượt Golden §3.1" không chạy được như viết.**
- Lượt Golden đi qua `answer_case` (bộ đánh giá, không qua API); `git grep chat_metrics -- backend/evaluation backend/llm` ⇒ **0** chỗ ghi ⇒ lượt §3.1 không sinh dòng `chat_metrics` nào.
  Tiêu chí đóng: đổi nguồn số (vd chạy N câu qua API trên server thật, nêu N), hoặc bỏ dòng này. Số "qua API p95 6,0 s" dẫn từ báo cáo so sánh 01/11 không nằm trong gói căn cứ — ghi
  nguồn `file:dòng`.

**m-2 — §3.1 / §1 mục 1: lượt Golden đo đường không stream.** "Chatbot sau streaming vẫn giữ chất lượng" đo bằng `answer_case` (đường `Runner.run`), còn người dùng đi route stream
(`Runner.run_streamed`). Hai đường cùng agent / prompt / kiểm citation, và chữ stream = chữ cuối đã kiểm theo spec C5 — nhưng plan nên ghi một câu: chất lượng route stream dựa trên
Golden (đường thường) + C5 (tương đương chữ), không đo Golden qua route stream. Tiêu chí đóng: thêm câu đó vào §3.1 hoặc §10.

**m-3 — §3.2 ↔ §10 / §3.7: cùng n = 28 mà hai con số khác nhau.** §3.2 (dẫn `BAO_CAO_DANH_GIA.md` §1) ghi "28 câu ⇒ < ~12 %" — đó là cận trên **hai phía** 95 % (1 − 0,025^(1/28) = 0,123);
§10 / §3.7 ghi "0 / 28 ⇒ < ~10 %" — cận **một phía** (0,1015). Tiêu chí đóng: dùng một quy ước cho mọi cận trên trong plan / report (B khuyên một phía 95 %, ghi rõ), sửa con số kia.

**m-4 — §6 tiền: ước theo giá phẳng, nhưng lúc chạy `cost_usd` đã là giá đủ (điều kiện §2).** Ước có A/A 0,113 (phẳng) ⇒ ≈ 0,136 theo giá đủ (+20 %, `BAO_CAO_DANH_GIA.md` §1); trần đề xuất
0,15 chỉ dư ≈ 10 % (không phải "+30 %"), trong khi luật dừng là "vượt ước > 50 %". Tiêu chí đóng: ghi ước theo giá đủ và mức dư thật của trần (hoặc nâng trần đề xuất), để Q4 trình User đúng.
(Tham khảo: B108 01/11 — `cost_usd` giá đủ đã code trên nhánh `dg-cost-usd` `bbbdbf9`, chưa merge; mục §2 dòng 32 cập nhật lúc đó.)

**m-5 — §3.1 bộ "trước" và §3.2 lượt mốc an toàn chưa ghi tên file + sha.** Plan gốc đợt 2 ghi sha từng bộ dùng lại. Tiêu chí đóng: ghi `eval_sau/sau_all.jsonl` (`45487ea1d88a`; `sau.jsonl`
cùng sha) + meta commit `751b352`, và file lượt "sau" đợt 2 của bộ an toàn (`an_toan/sau_dot2_2026-10-30/answers_r1.jsonl` + sha) vào §3.1 / §3.2 hoặc §2 "ghi trước".

**m-6 — §3.7 rào đọc kho cho sub-agent viết bộ kín.** "Chỉ nhận kho (đọc file kho)" — kho chứa `evaluation/` (Golden, câu kín cũ) và `meta/` (sao lưu Golden). Brief cần nói rõ: chỉ đọc file
nội dung ngoài `evaluation/`, `meta/`, `_source-dumps/`; tìm bằng `scripts/grep_kb.sh` (W27 — `WORKFLOW.md` §9.9). Kèm: §3.7 ghi "phân tầng theo 5 loại như Golden" nhưng liệt kê 4 loại
trong kho (loại thứ 5 là ngoài kho, tính riêng 6 câu) — sửa chữ; và nói 4 "câu điều kiện / cảnh báo" có gắn `category` `conditional` hay không (sàn "4 câu điều kiện + mọi câu `conditional`").

**Ghi chú (không phải finding):**
- n-1: §11 Q2 PA1 (A/A cùng ngày) chưa nói A/A mới **thay** N_AA = 2 hay chỉ dùng để tách trôi khi sát ngưỡng. Plan để `TBD` — khi User chọn PA1, phải ghi luật quyết trước khi chạy.
- n-2: §3.4 điều kiện dùng lại lượt S4: thêm "cùng build record / sparse / Qdrant" (dữ liệu không nằm trong `git diff`) — §2 "ghi trước" đã có các mục này nên chỉ cần dẫn chéo.
- n-3: §2 câu Golden lệch kho "User giữ nguyên 11:04 01/11" — B không kiểm được quyết định này trong gói căn cứ (chỉ thấy `BAO_CAO_DANH_GIA.md` §1 ghi "chờ bạn duyệt", bản 31/10) ⇒ A xác nhận
  và cập nhật báo cáo khâu.

## 3. Cách người kiểm chạy lại thật

- `sha256sum` plan; đếm số chính từ `golden_realism_final.jsonl` + Golden (Python chỉ đọc, in số đếm); tính cận Clopper–Pearson n = 6 / 28 (một / hai phía); `git grep chat_metrics -- backend/evaluation
  backend/llm`; `ls` + `sha256sum` + đọc meta bộ "trước" (`eval_sau/`), thư mục `an_toan/sau_dot2_2026-10-30/`. Không gọi API, không mở câu kín, không đọc câu trả lời.

## 4. Kết quả quan sát

Như §1 "Đạt" và bằng chứng trong từng finding. Không có số nào trong plan bị dữ liệu nói ngược, trừ m-3 (quy ước cận trên) và m-4 (ước tiền theo giá phẳng).

## 5. Giới hạn hoặc phần chưa chạy

- Không đọc plan gốc đợt 1 `sua_kho_do_truoc_sau_plan.md` (ngoài gói) ⇒ định nghĩa chi tiết F1–F4 / T3 / W1–W8 kiểm qua plan đợt 2 + `BAO_CAO_DANH_GIA.md`, không qua bản gốc.
- Không kiểm các số mốc ngày tương đối ("0 / 12 câu quyết", "6 / 14") ngoài dòng tóm tắt của `BAO_CAO_DANH_GIA.md` §3 (khớp "6 / 14").
- B là người viết B107 (đề xuất sửa Golden) và người code S1 / S2 / B108 mà plan dựa vào — không phải người viết plan, nên review vẫn độc lập theo §9.1; ghi để A biết.

## 6. Decision và bước tiếp theo

`changes_requested` — C sửa M-1 + m-1…m-6 trong một lượt (n-1…n-3 tùy), báo sha mới; B kiểm **phần sửa** (dùng lại các kiểm §1 "Đạt" nếu các dòng đó không đổi). Sau đó A điền các `TBD`
theo câu trả lời Q1–Q4 của User ⇒ B (hoặc người review) kiểm phần điền ⇒ A ghi "duyệt bản sha" (tính từ file).

---

# Vòng 2 — kiểm phần sửa bản 3 (`4d653544fb73`)

Decision: **ready_for_user_confirmation** cho phần đã có (M-1, m-1…m-6, n-1…n-3 đóng; 2 ghi chú nhỏ, không mở vòng) — còn `TBD` chờ User Q1–Q4 §11 · Người kiểm: B · Date: 11:38 01/11/2026 (`date`)

B tự tính `sha256sum` ⇒ `4d653544fb73` (235 dòng). Plan untracked ⇒ không có diff máy với bản 2; B đọc lại bảng §12 + mọi mục §12 trỏ tới (§2, §3.1, §3.2, §3.4, §3.7, §5, §6, §10, §11)
và chỗ bị ảnh hưởng. Cùng ranh giới vòng 1 (chỉ gói căn cứ + lệnh chỉ đọc; không đọc `STATUS_C.md` / tin của C; 0 USD).

| Finding | Chỗ sửa | Kiểm | Đóng? |
|---|---|---|---|
| M-1 | §3.2 A2 vế 1: mốc sinh lại 3 lần trên **`751b352`** (worktree riêng, `uv run --project`, cùng Qdrant / build record `51fb1ec63cbc` / sparse `c8134c49a648`, kiểm T1 giống byte `4d5bbe9e0edc` trước, gỡ worktree); "sau" trên commit §2; chỉ câu P0_sai mới | đúng commit trong `sau_all.meta.json` (vòng 1); luật ghi trước, không còn chỗ chọn sau | ✓ |
| m-1 | §3.4: bỏ dòng "`total_ms` trên lượt Golden"; thay 22 câu B65 qua `/api/chat`, so `b65_latency_dau_cuoi.md:48`; §5 bước 5; §6 +0,0055 | dòng 48 = "B1 (context 10 + NFC), tuần tự" p50 **3.068** / p95 **6.039** ms ✓ — đúng cấu hình 10 đoạn | ✓ |
| m-2 | §3.1 "Đo đường nào" + §10 | ghi rõ Golden qua `answer_case` (`Runner.run`), route stream suy từ lõi chung + C5 | ✓ |
| m-3 | §3.2 quy ước một phía 95 % ⇒ "~10 %", ghi BAO_CAO dùng hai phía | khớp §3.7 (0 / 6 < ~39 %) và §10 (0 / 28 < ~10 %) — cùng một quy ước | ✓ |
| m-4 | §6 dòng giá đủ ≈ 0,098 / 0,142; trần đề xuất 0,20; §11 Q4 | B cộng lại: phẳng 0,0763 + 0,0055 = 0,0818 / có A/A 0,1183; × 1,2 = 0,098 / 0,142 ✓; 0,20 / 0,142 = +41 % ✓; "0,15 chỉ dư ≈ 6 %" = 0,15 / 0,142 ✓ | ✓ |
| m-5 | §3.1 `sau_all.jsonl` `45487ea1d88a` + meta; §3.2 `answers_r1.jsonl` `ad24c8a8e53f` | B tính lại: `ad24c8a8e53f` ✓ | ✓ |
| m-6 | §3.7 rào đọc kho (ngoài `evaluation/`, `meta/`, `_source-dumps/`; `grep_kb.sh`); "4 loại trong kho + `out_of_scope`"; 4 câu điều kiện gắn `conditional` | 30 + 6 + 4 = 40 ✓; sàn "mọi câu `conditional`" nay gồm 4 câu thêm | ✓ |
| n-1 | §11 Q2 PA1: giữ N_AA = 2; A/A cùng ngày chỉ khi sát ngưỡng (4–5 câu tụt hoặc vượt 1) | luật ghi trước, không đổi thước sau khi thấy số | ✓ |
| n-2 | §3.4 thêm điều kiện build record / sparse / Qdrant | ✓ | ✓ |
| n-3 | §2 dẫn `CURRENT_HANDOFF.md:89` + `BAO_CAO_BO_CAU_HOI_GOLDEN.md` (bản 8, 11:04 01/11) | cả hai ghi "User 11:04 01/11: giữ nguyên" ✓ | ✓ |

**Ghi chú (không mở vòng):**
- n-4: §3.4 / §6 "22 câu tự viết của B65" chưa ghi đường dẫn + sha bộ câu — có ở `b65_latency_dau_cuoi.md:25`: `data/phase_8_2/latency_2710/questions.jsonl` (`bac5c91db005`). Thêm khi điền `TBD` (cùng kiểu m-5). Bộ này có trường `question` trong `data/` ⇒ tự nằm trong phép so SHA256 §3.7.
- n-5: dòng "giá đủ (+20 %)" §6 nhân 1,2 cả hai dòng đã tính bằng 0,00025 USD / câu (tốc độ trình duyệt, bộ kín, 22 câu B65) — số 0,00025 vốn là **giá đủ** (`BAO_CAO_DANH_GIA.md` §1) ⇒ ước hơi dư (≈ +0,006 USD), theo chiều an toàn; không cần sửa.

Bước tiếp: A điền `TBD` theo câu trả lời Q1–Q4 của User ⇒ người review kiểm đúng phần điền ⇒ A ghi "duyệt bản sha" (tính từ file).
