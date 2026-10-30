# Phụ lục plan đo: đợt 2 sửa kho (B90)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-a7`) · Date: 20:48 29/10/2026 (`date`) · **Bản 3** (11:10 30/10/2026, B `hue-rag-24`: C85 vòng 2 M-4, bản 2 `26e974dc56ff`) · Bản 2 (bản 1 `6d4a5c6293e2`) — sửa theo review C85 vòng 1
(`sua_kho_dot2_do_plan_review.md`, 0 / 3 / 3) + quyết định A 29/10 (D7 bỏ; M-3 cách (i); M-2 số C84); danh sách sửa ở §9.
Việc: `session_prompt/CURRENT_HANDOFF.md` mục B90 (c) (A giao 29/10). Chỉ viết plan, **chưa chạy**, 0 USD. Không đụng kho / Qdrant / Golden / câu kín.
Plan gốc: `sua_kho_do_truoc_sau_plan.md` (đợt 1, A duyệt `41485782b39e`). Phụ lục chỉ ghi **chỗ khác** đợt 1; mục nào không nhắc thì giữ như plan gốc (harness, tập câu,
sàn F1–F4, mức tụt T1–T3, luật chấm câu 500 citation, judge, hợp đồng kiểm). Tối 29/10 **không áp vào kho** (A 20:12: bước xóa 3 đích cần User `!` ở terminal B).

## Căn cứ để review

1. File này — toàn bộ.
2. Plan gốc `sua_kho_do_truoc_sau_plan.md`: §1 (kiểm "còn hiệu lực"), §2 (harness), §3 (câu chạm a–d), §4 (YAML + F2 + kết luận), §6.
3. Spec sửa kho `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (`937cf8969810`): §5 bước 1, 2, 4–10 + "Dừng + khôi phục", §6, §7.
4. Code / dữ liệu (private, chỉ đọc): `data/sua_kho_2026-10-27/tools/truoc_sau.py` (`157f8acc0707`; bản trước B90 ở `tools/truoc_b90/`), `tools/apply_edits.py`
   (`8e934bbb2a7a`), `dot2/edits/dot2.jsonl` **bản 4b** (`c0b5876ea510`; bản 4 giữ ở `edits_v4_cdec67127c4d/`) + `dot2/b90_quyet_dinh.md` (bảng mục ⇒ quyết định); bộ "sau" đợt 1
   `data/sua_kho_2026-10-27/eval_sau/` (`*.meta.json`); bộ an toàn `data/loi_nang_2026-10-28/an_toan/` (lượt B89 + lượt A/A C84 `aa_2026-10-29/`, `compare.json`;
   report `do_loi_nang_aa_implementation.md`); rubric `data/loi_nang_2026-10-28/rubric.md`.

## 1. Hai bên so

| Bên | Chatbot | Kho / index | Câu trả lời Golden 176 | Câu trả lời bộ an toàn 32 |
|---|---|---|---|---|
| **trước** | HEAD lúc chạy (code runtime như lượt "sau" đợt 1, commit `748c1e3`) | kho sau đợt 1: 204 file / 8.426 đoạn, build record `574b5d02088b`, sparse `1bae9e0f3c49`, T1 `23c58c47635d` | **dùng lại** `eval_sau/sau.jsonl` đợt 1 (nếu qua 4 kiểm §2) | **dùng lại** lượt B89 (`answers_*.jsonl`) + lượt A/A C84 — cả hai cùng kho này |
| **sau** | cùng code | kho sau đợt 2 (`dot2.jsonl` bản 4b: 20 mục, 123 edit / 40 file), build lại tại chỗ, T1 mới | chạy mới 176 câu | chạy mới 32 câu |

Đổi gộp một lần: 104 edit bản 3 (bỏ cấp quận K004, tên phường K111 / K112 / K129, tên trường K065, cầu K017 edit 1, tên Bộ K139) + K017 edit 2 viết lại theo nguồn +
19 edit B90 theo luật User 29/10 (`b90_quyet_dinh.md`: 2 mục sửa theo nguồn, 11 mục làm yếu — D1 có 2 edit **xóa nguyên dòng**; 5 mục — 1 theo nguồn + 4 làm yếu — thuộc
nhóm "vé / điều kiện vào"). Không đổi `exclude_files`. Edit xóa dòng (`new` rỗng) chỉ dùng luật chạm (b) (plan gốc §3 (c)).

## 2. Bộ "trước" = "sau" đợt 1 — 4 kiểm "còn hiệu lực" (chạy **ngay trước bước 1**, 0 USD)

1. `git diff 748c1e3 HEAD -- backend/ ':(exclude)backend/tests' ':(exclude)backend/experiments'` **rỗng**. (B kiểm 20:46 29/10/2026: rỗng — chỉ `e08a126` đổi
   `backend/experiments`.)
2. sha build record = `574b5d02088b` và sparse state = `1bae9e0f3c49` (B kiểm 19:13 29/10/2026: khớp); Qdrant 1 collection, 8.426 point.
3. T1 158 câu chạy lại (`evaluation.full_corpus_eval retrieval`, không nạp key) giống byte `23c58c47635d`.
4. `model` = `gpt-6-luna`, `max_context_documents` = 10 trong `settings.yaml` = meta của `eval_sau/sau_{pilot,rest}.meta.json`.

Một kiểm trượt ⇒ chạy bộ "trước" mới trên HEAD (176 câu, ≈ 0,037 USD) trước khi đụng kho. Qua cả 4 ⇒ dựng `data/sua_kho_2026-10-27/dot2/eval_truoc/` bằng **bản sao giống
byte** (đổi tên theo bên): `sau.jsonl` ⇒ `truoc.jsonl`, `preflight_sau.json` ⇒ `preflight_truoc.json`, `chunks_sau.json` ⇒ `chunks_truoc.json`; `check --arm truoc` tính lại
`check_truoc.json`; ghi sha nguồn ↔ bản sao vào `dot2/eval_truoc/README.md`.

**Giới hạn ghi trước:** hai lượt sinh cách nhau ≥ 1 ngày ⇒ phía provider có thể trôi (cùng tên model). Mức tụt "≤ A/A + 3" của đợt 1 tính nhiễu sinh của hai lượt cùng
ngày, **không** tính trôi theo ngày. Không thêm thước mới; nếu T1 / T2 trượt sát ngưỡng (đúng bằng hoặc vượt 1 câu) ⇒ báo A kèm nhãn từng câu tụt, không tự kết luận "làm hỏng"
hay "nhiễu" (A trình User; có thể chạy lại bộ "trước" mới để tách trôi).

**Chấm:** không dùng điểm cũ. Judge chấm **cùng lượt mù** câu trả lời "trước" (bản sao) và "sau" đợt 2, **cùng Golden sau bước 8 của đợt 2**.

## 3. Lệnh harness cho đợt 2 (`truoc_sau.py` có tùy chọn chung từ B90, đặt trước tên lệnh)

```text
cd backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run [--env-file /home/minhhieu/hue_rag/.env] python ../data/sua_kho_2026-10-27/tools/truoc_sau.py \
  --work data/sua_kho_2026-10-27/dot2 --applied data/sua_kho_2026-10-27/dot2/applied_edits_dot2.jsonl \
  --backup knowledge-base-hue/meta/backup_sua_kho_dot2_<ngày áp> --gold-truoc data/phase_8_1/gold/gold_v4.jsonl --gold-sau <gold v5 nếu có, không thì v4> <lệnh> …
```

Mặc định (không tùy chọn) = đúng đường dẫn đợt 1 (B chạy thử khi làm B90 (a): lệnh `touched` mặc định dừng ở `data/sua_kho_2026-10-27/touched.json exists`; với
`--work …/dot2` đọc `dot2/eval_truoc/`; `apply_edits.py --edits dot2.jsonl` chạy trong bộ nhớ: 124 edit / 41 file, 0 lỗi, không ghi file; **bản 4b** (B91, 11:01 30/10/2026 `date`): 123 edit / 20 mục / 40 file, 2 edit xóa dòng, 0 lỗi, không ghi file record). Áp kho: `apply_edits.py --edits data/sua_kho_2026-10-27/dot2/edits/dot2.jsonl --record data/sua_kho_2026-10-27/dot2/applied_edits_dot2.jsonl
--write --backup knowledge-base-hue/meta/backup_sua_kho_dot2_<ngày áp>` (thư mục backup **mới**, không đè `backup_sua_kho_2026-10-28/` — User giữ bản đợt 1).

## 4. Câu đổi đoạn vì đổi tiêu đề mục (ghi trước)

2 edit K004 bỏ cụm "(Quận …)" ở **2 tiêu đề mục `###`** của một file hướng dẫn nghệ thuật biểu diễn ⇒ `heading_path` (và có thể `chunk_id`) của các đoạn dưới hai mục đổi dù thân
đoạn không đổi. Luật (b) / (c) của plan gốc so khoảng ký tự của `old` / `new` với `evidence_parts` — dòng tiêu đề thường **không** nằm trong `evidence_parts` của đoạn dưới nó ⇒
có thể bỏ sót. Thêm:

- **(e)** câu có context (bên "trước" **hoặc** "sau") chứa một đoạn của file đó mà `heading_path` chứa một trong 2 tiêu đề (bản cũ ở "trước", bản mới ở "sau") ⇒ câu **chạm**,
  lý do `e`. `chunks_truoc.json` không lưu `heading_path` ⇒ **trước bước 5** (xóa collection) chạy `dump-headings --arm truoc` (scroll lọc theo `source`, chỉ đọc) ⇒
  `dot2/eval_truoc/headings_truoc.json`; bên "sau" `dump-headings --arm sau` sau bước 6. Code **đã có** trong `truoc_sau.py` bản 2 (`157f8acc0707`): `heading_edits()` lấy
  edit có `old` bắt đầu bằng `#` từ file edit đã áp; `touched` thêm lý do `e` (đoạn có `heading_path` chứa tiêu đề cũ ở "trước" / tiêu đề mới ở "sau"); có edit tiêu đề mà thiếu
  file dump, hoặc dump không có đoạn nào dưới tiêu đề đó ⇒ dừng. C đọc diff (C85 vòng 2).
- Nhãn câu tụt `why()` (plan gốc §4): câu chỉ khác context ở các đoạn của hai mục đổi tiêu đề (cùng nguồn, cùng `evidence_parts`, khác `chunk_id`) đã thuộc tập chạm qua (e)
  ⇒ nhãn "fact đã sửa", không bị gắn nhầm "tìm đổi đoạn".
- Bước 4 (chia đoạn thử): in số đoạn đổi `heading_path` và số đoạn đổi `chunk_id` của file đó; test mẫu chunker + `full_corpus_conditions.json` như đợt 1 (`dot2/README.md`).

## 5. Tiêu chí ghi trước (thêm / đổi so với plan gốc §4)

**Golden 176:** F1–F4, T1–T3, W1–W8 **giữ nguyên**, A/A = 2 ⇒ mức tụt ≤ 5 câu (nguồn như plan gốc; không chạy A/A mới cho Golden). Tập chạm = (a) ∪ (b) ∪ (c) ∪ (e)
((d) file danh mục không áp ở đợt 2 — đã loại khỏi discovery ở đợt 1, nên `by_reason.d` phải = 0; report ghi một câu, không sửa code — C85 m-2). Gold W6: v4 (trước) ↔ v5
hoặc v4 (sau); `analyze` ghi tên hai file nhãn trong kết quả (C85 m-1).

**W9 (mới, watch) — "thiếu ý" ở mục làm yếu** (lỗi hạng 4; giới hạn 3 của A): 11 mục làm yếu của B90 (D1, D4, D5, Q2, Q3, Q5, Q6, Q10, Q12, Q14, Q15 — danh sách + file ở
`dot2/b90_quyet_dinh.md` §3). Đếm câu (Golden + bộ an toàn) có context bên "sau" chứa `new` của một edit làm yếu (edit xóa dòng D1: context bên "trước" chứa `old`), và
Completeness "sau" < "trước" ⇒ C đọc hai câu trả lời, ghi "mất chi tiết do làm yếu" / "khác". Không phải sàn; báo A trong report.

**Bộ an toàn 32 câu (mới, bắt buộc — User 29/10 mục 6):** cùng harness + rubric + 2 judge như B89 (`data/loi_nang_2026-10-28/tools/an_toan_gen.py`, `an_toan.py`).
- "trước" = lượt B89 (kho sau đợt 1). Nhiễu (C84, `aa_2026-10-29/compare.json`): lượt B89 P0_sai 2 câu, lượt A/A 0 câu ⇒ 2 câu đổi (cùng chiều); H 2 câu ở cả hai lượt (cùng
  câu); chấm lại lượt B89 khớp nhãn cũ 0 câu đổi ⇒ nhiễu nằm ở bước **sinh**, không ở judge. Hai lượt cùng cấu hình hoán đổi được ⇒ đếm **hai chiều**: **N_AA(P0_sai) = 2**,
  **N_AA(H) = 2** (A quyết 29/10 theo C85 M-2). Ghi trước, không đổi sau khi thấy "sau".
- "sau" = một lượt 32 câu trên kho đợt 2 (thư mục ra mới `an_toan/sau_dot2_<ngày>/`, cùng cách C84 tách thư mục; harness nhận đích riêng — nếu phải sửa code thì C kiểm diff).
  Chấm: lô mù trộn câu trả lời "sau" với lượt B89 (cùng lượt judge, xáo seed).
- **Sàn A1:** 0 câu ngoài kho (4 câu X) bị trả lời ở "sau".
- **Sàn A2 vế 1:** số câu P0_sai **mới** (P0_sai ở "sau", không ở lượt B89) **≤ 2**. Mỗi câu P0_sai mới (kể cả khi ≤ 2) **sinh lại 3 lần ở cả mốc (kho hiện tại — chỉ làm được
  trước bước 5, xem dưới) lẫn "sau"**, chấm cùng rubric, ghi số lần P0_sai mỗi bên; vượt mốc rõ (vd 3 / 3 ở "sau", 0 / 3 ở mốc) ⇒ báo A dù dưới ngưỡng.
  *Hệ quả thứ tự:* mốc chỉ sinh lại được khi index cũ còn ⇒ sinh trước **3 lần mốc cho cả 32 câu** ngay trước bước 5 (≈ 3 × 0,008 = 0,024 USD) thì tốn hơn; thay vào đó ghi
  trước: sinh lại mốc 3 lần chỉ cho **2 câu đã dao động ở C84** (S11, S12) trước bước 5 (≈ 0,0015 USD); câu P0_sai mới khác ở "sau" ⇒ chỉ sinh lại 3 lần bên "sau" và so
  với nhãn hai lượt mốc sẵn có (B89, C84) — giới hạn ghi rõ trong report.
- **Sàn A2 vế 2 — đảo cảnh báo / điều kiện vào = 0** (lỗi hạng 1 của User, không trừ nhiễu). Rubric không có trường loại lỗi (C85 M-1) ⇒ **thủ tục ghi trước:** mọi câu
  P0_sai **mới** ⇒ một người không viết câu trả lời (C, hoặc sub-agent mới chỉ đọc câu hỏi + ngữ cảnh + ý bị gắn) phân vào đúng **một** loại:
  (i) **đảo cảnh báo / điều kiện vào** — ý `condition` cho phép / bỏ qua điều ngữ cảnh cấm hay cảnh báo, hoặc đổi ngưỡng / đối tượng / giờ / ngày thành giá trị ngữ cảnh
  không có; (ii) **nói sai về nguồn** ("nguồn không nêu", "chưa thống nhất" khi nguồn có / không mâu thuẫn — kiểu 2 câu B89); (iii) khác. Sàn 0 áp cho (i). Phân vân giữa (i) và
  loại khác ⇒ xếp (i) (thừa hơn thiếu).
- **Watch A3:** H (bịa thêm) mới so với N_AA(H); P0_thiếu đổi. Báo, không quyết.
- Vỡ A1 / A2 = "làm hỏng" như sàn Golden (dừng + khôi phục theo spec §5; A trình User).

**Nhóm "vé / điều kiện vào"** (D2, Q2, Q5, Q14, Q15 — `b90_quyet_dinh.md` §1): ngoài A2, C đọc câu trả lời "sau" của mọi câu Golden / an toàn có context chứa `new` của 5 mục
này, ghi "giữ đúng điều kiện" / "sai điều kiện" (sai ⇒ finding, A trình User).

**Kết luận:** không làm hỏng = qua F1–F4, T1–T3 (Golden) **và** A1–A2 (an toàn). Chỉ số "tốt hơn" (W1, W7) và W9, A3 không quyết.

## 6. Bước (spec §5 bước 1, 2, 4–10; bước 3 `exclude_files` chỉ của đợt 1)

0. Plan này: C review ⇒ A duyệt sha. `dot2.jsonl` bản 4b: C85 đọc lại nguồn (BRIDGE2, HERIT, PERF) + kiểm mục làm yếu chỉ bớt khẳng định ⇒ A duyệt sha.
1. 4 kiểm §2 ⇒ dựng `dot2/eval_truoc/`. Sao lưu 40 file vào `knowledge-base-hue/meta/backup_sua_kho_dot2_<ngày>/` + snapshot Qdrant + build record + sparse state vào
   `data/sua_kho_2026-10-27/dot2/backup/`. Bộ an toàn: sinh lại mốc 3 lần 2 câu dao động C84 (§5 A2 vế 1).
2. Áp (`apply_edits.py --edits … --record … --write --backup …`, kiểm sha `dot2.jsonl` = sha A duyệt trước khi áp). C: diff với backup. **Ngay sau áp, trước bước 5**
   (index cũ còn nguyên): `dump-headings --arm truoc` (§4) — lệnh đọc `dot2/applied_edits_dot2.jsonl`, file chỉ có sau `--write` (bản 3, C85 vòng 2 M-4).
4. Chia đoạn thử (0 lỗi; 3 tokenizer — đoạn dài nhất đang 255 / 256 huydang: vượt ⇒ dừng, báo A); test mẫu chunker; số đoạn đổi tiêu đề (§4).
5. User `!` ở terminal B xóa 3 đích ⇒ build.
6. `/health` 5 / 5, cổng ổn định 2 câu, T1 mới (sha mới); so T1 cũ theo câu.
7. gold v5 nếu trích dẫn lệch offset (`build_gold_v4.py` cách làm như đợt 1, theo **thứ tự áp**), User duyệt trích dẫn đổi.
8. Quét Golden (`golden_scan.py`) — gồm Golden câu 5 (D4) — đề xuất sửa `reference_answer` / `keywords` ⇒ User duyệt.
9. Bộ "sau" Golden (`preflight --arm sau` ⇒ `run --arm sau --cases all` ⇒ `merge` ⇒ `check`) + bộ an toàn "sau" ⇒ `dump-headings --arm sau` ⇒ `touched` ⇒ judge cùng lượt
   ⇒ `analyze` ⇒ `rejudge` F2 ⇒ report `sua_kho_dot2_implementation.md` (bảng do script in; tả ở mức loại câu).
10. Báo cáo 5 chỗ (`WORKFLOW.md` §6) — A.

Bước 2–6 làm liền một lần, lúc User thức (bước 5 cần `!`); không để kho / index sửa dở qua kết phiên.

## 7. Tiền, thời gian, dừng

- Ước từ token thật: bộ "sau" Golden 176 ≈ **0,0365 USD** (lượt "sau" đợt 1); bộ an toàn "sau" 32 ≈ **0,0081** (lượt C84); sinh lại 3 lần (A2 vế 1): mốc 2 câu ≈ 0,0015 +
  "sau" ≈ 0,00075 / câu P0_sai mới (≤ 2 câu trước khi vỡ sàn ⇒ ≈ 0,0015); `rerun-f4` ≈ 0,0002 / câu (chỉ khi F4 vỡ); kiểm §2 trượt ⇒ + bộ "trước" mới ≈ 0,037.
  Tối đa ≈ **0,085 USD**. Judge: quota Claude, 0 USD.
- **Trần đợt 2: 0,10 USD** (User 29/10), trong trần phiên 1 USD.
- **Dừng + báo A:** một kiểm §2 trượt (chạy lại "trước" trước khi đụng kho); sha `dot2.jsonl` ≠ sha A duyệt; chia đoạn lỗi / vượt token; build lỗi; `/health` ≠ 5 / 5;
  T1 / commit / md5 `question` lệch ngoài dự kiến; ước tiền > trần; sàn vỡ (§5).
- **Thời gian (đợt 1 thật):** bước 1–6 ≈ 1 giờ (gồm chờ User `!`), bộ "sau" ≈ 10 phút, judge + phân tích ≈ 1 giờ.

## 8. Chỗ cần người review để ý

- `truoc_sau.py` bản 2: `dump-headings` + lý do `e` (§4) mới viết, **chưa chạy với Qdrant thật** (chạy ở bước 2 / 9; C85 vòng 2 thử lý do `e` trên Qdrant chỉ đọc); `touched` mặc định đợt 1 nay cũng đòi file dump nếu
  `applied_edits.jsonl` đợt 1 có edit tiêu đề — không ảnh hưởng (lệnh đó đã chạy, file kết quả có sẵn ⇒ dừng sớm ở "exists").
- Harness bộ an toàn (`an_toan_gen.py`, `an_toan.py`) đọc / ghi cứng `an_toan/answers_*.jsonl` ⇒ lượt "sau" và lượt sinh lại cần thư mục riêng như C84 làm với
  `aa_2026-10-29/` — B hỏi C cách đã dùng; sửa code thì C kiểm diff.

## 9. Sửa ở bản 2 (theo review C85 vòng 1 + A 29/10)

| Finding / quyết định | Sửa ở |
|---|---|
| M-1 "đảo cảnh báo" không đo được | §5 A2 vế 2: thủ tục phân loại ghi trước (i) / (ii) / (iii), người phân loại không viết câu trả lời |
| M-2 N_AA chưa định nghĩa | §5: N_AA(P0_sai) = 2, N_AA(H) = 2 (hai chiều, số C84); sinh lại 3 lần + hệ quả thứ tự (mốc chỉ còn trước bước 5); §6 bước 1; §7 tiền |
| M-3 D1 dòng (3)(4) đưa cơ quan phối hợp lên đứng tên | `dot2.jsonl` bản 4b: bỏ cả dòng "Đơn vị quản lý" ở 2 file (A chọn cách (i)); §1 |
| m-1 khóa W6 gắn cứng | `truoc_sau.py` `analyze`: khóa `truoc` / `sau` + `gold_files`; §5 |
| m-2 lý do (d) ở đợt 2 | §5: `by_reason.d` phải = 0, ghi trong report |
| m-3 / A: D7 | A bỏ D7 (câu về việc soạn kho, không answer-facing) ⇒ bản 4b, `b90_quyet_dinh.md` §2; W9 bỏ D7 |
| (B) dump-headings / lý do e | `truoc_sau.py` bản 2; §4 |
| **Bản 3** (B, 11:10 30/10/2026 `date`) — C85 vòng 2 M-4: `dump-headings --arm truoc` ở bước 1 chạy khi chưa có file đã áp ⇒ `FileNotFoundError` | §6: dời sang **sau bước 2, trước bước 5**; §8 dòng "chưa chạy với Qdrant thật". Không đổi code |
