# Review: lượt đo cuối Phase 1–8 (C111 + phần B §6–§8) và 2 nháp cho báo cáo

Decision: **changes_requested** (0 blocker · 2 major · 5 minor; chỉ sửa chữ, không chạy lại, 0 USD)
Người kiểm: agent con ngữ cảnh mới do A giao — review một lần (Claude Opus 5.5)
Date: 13:28 01/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` **`ae8d42d520d4`** (sha kiểm lại bằng `sha256sum`) §2, §3, §6, §8
Implementation report: `do_cuoi_implementation.md` (`ac361fba4eea`), `do_cuoi_b_an_toan_ngay.md` (`a15196ffc4d7`), `do_cuoi_b_bo_kin.md` (`6890b98f1b3e`);
nháp private `data/so_sanh_phuong_an/them_01_11.md` (`f27bcad1d79c`), `danh_gia_them_01_11.md` (`339c7e22ea23`)

## 1. Phạm vi đã review

- Đọc toàn bộ plan, 3 report, 2 nháp; số thô: `golden/analyze.json` (`13fccf9bab68` — khớp report), `golden/theo_loai_cau.json` (`485304553865`), `golden/sau/check_sau.json`, các `golden/*/*.meta.json`,
  `b65/seq.meta.json` (`267e2cd3fd43`), `b_an_toan_ngay_tom_tat.md` (`cbfce3edd471`), `an_toan/compare_main.json` (`a7ca5ad06ec1`), `an_toan/compare_regen.json` (`2fe348e3e4e7`),
  `ngay/ket_qua.json` (`0e1bc5514795`), `data/s4_2026-11-01/summary_main.json`, `s4_do_d2_implementation.md` §3–§5, `q3a_theo_loai_cau_implementation.md` §4.
- Đọc code harness private `data/do_cuoi_2026-11-01/tools/do_cuoi.py`: `run` (chốt theo code — sửa 12:53), `scored`, `f2_candidates`, `paired`, `analyze` (luật A/A sát ngưỡng 4–6 câu, mức tụt ≤ N_AA + 3).
- **Không** mở `data/do_cuoi_2026-11-01/kin/`, file `*sealed*`, `knowledge-base-hue/evaluation/final_2026-11-01/`, `.env`; không gọi API, không chạy server. Số bộ kín chỉ kiểm được bằng tính nhất quán nội bộ.

## 2. Findings

### M-1 (major) — "chỉ câu được trả lời thì Đủ ý 4,60 ≈ Golden" so hai thứ khác nhau ⇒ kết luận "khoảng cách gần như toàn bộ do từ chối nhầm" sai

- **Vị trí:** `do_cuoi_b_bo_kin.md` §4 bảng "Báo số" (dòng "chỉ câu được trả lời", cột Golden "—") + "Đọc số" gạch 2 + "Giải thích ngắn" ("những câu được trả lời thì chất lượng ngang bộ cũ");
  `do_cuoi_implementation.md` §4 đoạn bộ kín; `them_01_11.md` E13 "Giới hạn" + "Nhãn", bảng 2.1 dòng 67 ("từ chối nhầm ở câu nhiều nguồn / so sánh"); `danh_gia_them_01_11.md` gạch "Bộ câu kín mới".
- **Requirement:** plan §3.7 "Báo … **khoảng cách** so với **cùng thước** trên Golden số chính".
- **Evidence (người kiểm chạy, 0 USD, chỉ in số):** 4,60 là bộ kín **chỉ câu được trả lời** (30 câu), còn 4,58 là Golden **gồm cả câu bị từ chối** (từ chối chấm Đủ = 1). Cùng thước "chỉ câu được trả lời" trên
  Golden bên "sau", số chính: **121 câu, Đủ 4,818** (8 câu từ chối, Đủ TB 1) ⇒ khoảng cách còn **≈ −0,22**, không phải ≈ 0. Theo loại: câu một dữ kiện bộ kín Đủ **4,42** (12 câu, **0** từ chối nhầm) ↔ Golden
  4,91 (đã trả lời: 4,97) ⇒ **−0,5 ở loại không có từ chối nào**. Kiểm chéo: trộn lại theo trọng số loại câu của Golden (66 / 18 / 25 / 20) từ số theo loại của bộ kín ⇒ Đủ ≈ 4,20 — khoảng cách **không** do
  thành phần bộ kín.
- **Tác động:** nháp cho User nói khoảng cách "gần như chỉ vì 4 câu từ chối nhầm … đúng chỗ yếu đã biết (Phase 9)" — lạc quan hơn số thật; bỏ sót tín hiệu mới: câu được trả lời trên câu chưa ai thấy
  **kém đủ ý hơn** (nhất là câu một dữ kiện), không chỉ do tầng tìm ở câu nhiều nguồn.
- **Tiêu chí đóng:** điền cột Golden "chỉ câu được trả lời" = 4,82 (121 câu) và khoảng cách ≈ −0,22; sửa "Đọc số" + "Giải thích ngắn" + 3 chỗ ở 2 nháp thành: khoảng cách đến từ **cả** từ chối nhầm (4 câu nhiều
  nguồn / so sánh) **lẫn** câu trả lời kém đủ ý hơn (một dữ kiện 4,42 ↔ 4,91, n = 12); n nhỏ, chưa có CI cho phần "chỉ câu được trả lời" (hoặc tính bootstrap như phần khác). Giữ "số dev hơi lạc quan",
  bỏ "≈ Golden". Không chạy lại, không mở bộ kín (tính từ file điểm đã có, chỉ in số).

### M-2 (major) — số tốc độ đưa vào §1 "chatbot đang chạy" + so với 27/10 thiếu lưu ý "ngày đo model gần như không suy luận"

- **Vị trí:** `danh_gia_them_01_11.md` bảng "Tốc độ — 3 thước" (cột nguồn "(27/10: 3,07 / 6,04 s)") và "Sửa kèm §1"; `them_01_11.md` E13 "Kết quả số" ("Qua API … (mốc 27/10: 3.068 / 6.039)").
- **Requirement:** brief kiểm nháp: không để số theo dõi một lần đo đọc thành "nhanh hơn"; `Session_Prompt.md` §6 tách đã kiểm ↔ suy luận.
- **Evidence:** S4 tự ghi (s4 §4 "Đọc số", §5): hôm đo token suy luận trung vị **0** (28/10: 81) ⇒ "chữ đầu sớm hơn thường". Cùng đường `answer_case`, cùng đoạn tìm (T1 giống byte), thời gian sinh trong harness bên
  mốc 30/10 **2,19 / 4,90 s** ↔ 01/11 **1,76 / 3,42 s** (`analyze.json` `watch_usd_wall`) ⇒ phần lớn chênh lệch giữa các ngày là phía nhà cung cấp, không do code. Nháp đặt API 2,34 / 3,80 s cạnh 27/10 3,07 / 6,04 s
  không có câu này; khối §1 thay số "đang chạy" bằng số tốc độ một lần đo không kèm lưu ý. S18 của `them_01_11.md` có lưu ý suy luận ≈ 0 — E13 và nháp đánh giá thì không.
- **Tác động:** User / CEO dễ đọc "API nhanh hơn ~25–35 % so với 27/10" và "đạt cả mục tiêu 1,5 / 3 s" như tính chất ổn định của hệ thống; phần dư so với mục tiêu chỉ 0,27 / 0,39 s (s4 §4).
- **Tiêu chí đóng:** thêm một câu ở bảng tốc độ + khối §1 + E13: "một lần đo (01/11); hôm đo model gần như không suy luận trước khi viết ⇒ có thể nhanh hơn ngày thường; chênh với 27/10 / 30/10 chủ yếu do phía
  nhà cung cấp, không phải do code (cùng đường tìm, T1 giống byte). Sàn 3 / 5 s đạt rộng; mục tiêu 1,5 / 3 s đạt sát."

### Minor (ghi ngắn, không mở vòng)

- **m-1** Sinh lại 3 lần / bên ⇒ "dao động của model, **không phải** kém đi" (`danh_gia` gạch an toàn; "Giải thích ngắn" của `do_cuoi_b_an_toan_ngay.md`) nói chắc hơn số: chính B §5 ghi 3 lần / bên chỉ thấy khác
  biệt lớn. Nên viết "không thấy kém đi so với mốc (3 lần mỗi bên — chỉ phát hiện khác biệt lớn)". Số khớp: `compare_regen.json` S11 / S12 đều 1 / 3 ↔ 1 / 3, `bao_A` false.
- **m-2** Lệch plan §3.7 của bộ kín chưa ghi ở report tracked: thành phần **12 / 6 / 6 / 6** (+ 4 điều kiện) so với tỉ lệ Golden ≈ 14 / 6 / 5 / 5 (A giao; `CURRENT_HANDOFF.md:152` ghi "ghi giới hạn"), và dùng
  `check` thường thay `check --authoring` (cùng dòng). Không đổi kết luận (trộn lại theo tỉ lệ Golden vẫn ≈ 4,20 — M-1), nhưng nên thêm 1 dòng ở `do_cuoi_b_bo_kin.md` §5 + trỏ bằng chứng khâu viết / kiểm
  (0 trùng sha, vòng chặn trùng ý rồi sửa, User đọc mẫu, sha cuối `7f97d4c10b2b`).
- **m-3** `do_cuoi_implementation.md` §4 + E13 gộp "0 bịa thêm" vào danh sách "sàn đạt" của bộ kín; plan §3.7 xếp H là **báo**, không phải sàn. Tách ra.
- **m-4** Harness `run` sau sửa 12:53 so `git diff <commit đo> HEAD` (hai commit), **không** so cây làm việc; cũng không kiểm lại build record / sparse / Qdrant mỗi lượt (meta chỉ ghi sha build record). Lỗ này có cả ở
  bản cũ (so HEAD); lúc kiểm `git status --porcelain backend frontend pyproject.toml uv.lock` rỗng, meta 3 lượt Golden ghi HEAD `19801e0` / `commit_do` `89c988e`. Câu "trước mọi lần gọi có phí" chỉ đúng cho
  `do_cuoi.py`: lượt 22 câu B65 (`latency_cuoi.py`) bắt đầu 12:51:46, trước sửa — khi đó HEAD vẫn `89c988e` nên không ảnh hưởng. Ghi một câu.
- **m-5** Plan §3.1 "Theo dõi" đòi báo điểm TB **cả 176** + T1 / MRR / đoạn đúng v5 in lại; report chỉ có số chính 129 và "T1 giống byte" (ngầm: số tìm không đổi). Ghi một dòng "không in lại vì T1 giống byte"
  hoặc thêm số.

Không có blocker. Mọi kết luận "đạt / không làm hỏng" theo **tiêu chí ghi trước** đứng vững (mục 4); hai major là cách diễn giải số báo / theo dõi, không đổi kết luận nào của sàn / mức tụt.

## 3. Cách người kiểm chạy lại thật

- `sha256sum` plan + 3 report + 2 nháp + file số thô (sha ở đầu file); `git diff --stat 6a0c842 89c988e -- backend frontend pyproject.toml uv.lock` và `git diff --stat 89c988e HEAD -- …` ⇒ **rỗng cả hai**
  (điều kiện dùng lại S4 + "cùng một commit" — plan §2, §3.4); `git log` giờ commit (`89c988e` 12:48:57, `d50e679` 12:53:11, `19801e0` 12:53:58).
- Đọc khóa JSON (chỉ số, mã câu) của `analyze.json`, `theo_loai_cau.json`, `check_sau.json`, `*.meta.json`, `seq.meta.json`, `compare_main.json`, `compare_regen.json`, `ket_qua.json`, `summary_main.json`.
- Tính "chỉ câu được trả lời" trên Golden (M-1), 0 USD, không gọi Qdrant / API, chỉ in số:
  `cd backend && PYTHONPATH=$PWD:../data/do_cuoi_2026-11-01/tools HF_HUB_OFFLINE=1 uv run python -c "…do_cuoi.scored() + load_realism(); đếm từ chối, TB Đủ / Đúng câu được trả lời theo bên / loại…"`.
- Riêng tư: `uv run python .githooks/overlap_scan.py <file>` cho 5 file ⇒ **0 trùng** cả 5 (exit 0); `grep -i` tên dự án khác ⇒ 0; đọc tay: mã câu (`S11`, `R6`, `K01…K40`) chỉ đi kèm loại lỗi / loại câu.

## 4. Kết quả quan sát

**Theo tiêu chí ghi trước (plan §3):** F1 0 / 18, F3 0 (sau, A/A), F4 0 mới, F2 0 ứng viên; T1 tụt 2 ≤ 5 và +0,016 ≥ −0,1; T2 tụt 2 và +0,008; T3 12 ≤ 13; A/A không sát ngưỡng (luật 4–6 câu, code
`near = MAX_DROP−1 ≤ drops ≤ MAX_DROP+1` khớp §11 Q2); A1 0 / 4; A2 vế 1 = 2 ≤ 2 (đúng ngưỡng — report ghi rõ "đúng ngưỡng", không viết thành "dư"); A2 vế 2 (i) = 0; câu ngày 0 / 12; tiền 0,000247 ≤ 0,0005;
bộ kín 3 sàn đạt; tổng tiền 0,139 ≤ trần 0,20, không lượt nào vượt ước > 50 % (§6). Không thấy nới thước / đổi ngưỡng sau khi thấy số. Lệch plan đã ghi: chốt commit theo code (12:53, có lý do, A đồng ý); lệch
chưa ghi: m-2, m-5. Điều kiện dừng §8: không cái nào xảy ra (cổng ổn định + `/health` dùng lại từ lượt trên `6a0c842`, code giống).

**Đối chiếu số (report / nháp ↔ file thô):**

| # | Số | Report / nháp | File thô | |
|---|---|---|---|---|
| 1 | F1 / F3 / F4 / F2 | 0 / 0 / 0 / 0 | `analyze.json` danh sách rỗng | khớp |
| 2 | T1 tụt · TB · CI · thắng/hoà/thua | 2 · +0,016 · [−0,023; +0,054] · 4/123/2 | 2 · 0,0155 · [−0,0233; 0,0543] · 4/123/2 | khớp |
| 3 | T2 | 2 · +0,008 · [−0,023; +0,039] · 3/124/2 | 2 · 0,0078 · [−0,0233; 0,0388] · 3/124/2 | khớp |
| 4 | T3 từ chối nhầm | 12 (mốc 12) | truoc / sau / aa = 12 / 12 / 12 | khớp |
| 5 | sau ↔ A/A | Đủ 0/128/1, Đúng 1/128/0 | như vậy | khớp |
| 6 | TB số chính sau · mốc · A/A | 4,713/4,581/4,721 · 4,705/4,566/4,721 · 4,721/4,574/4,698 | như vậy | khớp |
| 7 | Theo loại (sau, Đúng/Đủ/Trúng ý) — nháp đánh giá | 4,92/4,91/4,91 · 4,96/4,68/4,96 · 4,55/4,35/4,55 · 3,78/3,50/3,89 | `theo_loai_cau.json` 4,924/4,909/4,909 … 3,778/3,5/3,889 | khớp |
| 8 | Tiền / câu sau: TB · p95 · lớn nhất; A/A | 0,000247 · 0,000339 · 0,000436; 0,000248 | 0,0002468 · 0,0003391 · `check_sau` 0,0004364; 0,0002478 | khớp |
| 9 | Thời gian sinh harness sau · A/A · mốc | 1,76/3,42 · 1,89/4,06 · 2,19/4,90 s | 1763,7/3418,6 · 1894,2/4060,7 · 2193,2/4900 | khớp |
| 10 | Pilot · Golden sau · A/A (USD) | 0,00016/câu · 0,0434 · 0,0436 | 0,0016004/10 · 0,0016004+0,0418342 · 0,0436084 | khớp |
| 11 | B65 p50 [CI] · p95 [CI] · max | 2.340 [1.703; 3.086] · 3.800 [3.466; 4.141] · 4.141 | `seq.meta.json` như vậy | khớp |
| 12 | B65 server · dòng metrics · từ chối · USD | 2.390/4.106 · 23 · 2/20 + 2/2 ngoài kho · 0,0070 | 2390/4106 · 23 = 23 · [6, 9] + 2 true · 0,0069953 | khớp |
| 13 | S4 C1 · C2 · C3 · lợi · C6 | 1.228/2.612 (n 38) · 1.476/2.930 · 1.725/3.807 · 441 [371; 535] · 0,000247 | `summary_main.json` 1227,5/2612,3 · 1476,4/2930,4 · 1724,9/3806,7 · 441,3 [370,6; 535] · 0,0002466 | khớp |
| 14 | S4 tiền | 0,0158 | s4 report :59 0,015802 (64 lần gọi; `summary_main` lượt chính 0,014548) | khớp |
| 15 | An toàn A1 · A2 vế 1 · H mới · P0_thiếu | 0/4 · S11, S12 · 2 · 7/28, mới 1, mất 1 | `compare_main.json` như vậy | khớp |
| 16 | Sinh lại 3 lần | 1/3 ↔ 1/3 cả hai câu; `bao_A` false | `compare_regen.json` như vậy | khớp |
| 17 | Câu ngày | 0 / 12; từ chối nhầm 5; R11 không bị trả lời | `ket_qua.json` như vậy | khớp |
| 18 | Tiền B §6–§7 | 0,018118 | 0,009497+0,002127+0,002164+0,004330 = 0,018118 | khớp |
| 19 | Tổng | 0,1122 → 0,1280 → 0,1392 | cộng lại 0,1121–0,1122 (làm tròn) → 0,128 → 0,139 | khớp |
| 20 | Bộ kín Đủ / Đúng TB (không mở file) | 4,18 / 4,38 | từ số theo loại: (12·4,42+6·3,67+10·4,70+6·3,33)/34 = 4,18; Đúng = 149/34 = 4,38; 30 trả lời ×4,60 + 4 từ chối ×≈1 ≈ 4,18 | nhất quán |
| 21 | Golden "chỉ câu được trả lời" | "≈ Golden" (so 4,58) | **4,818** (121 câu) | **lệch — M-1** |

**Nói quá / giới hạn trong 2 nháp:** "đạt" chỉ dùng khi qua tiêu chí ghi trước; A2 vế 1 ghi "đúng ngưỡng" ở mọi chỗ ✓. Giới hạn có: một lần đo (nhãn `[một lần chạy]`, S18), cỡ mẫu nhỏ (bộ kín CI, "không phát hiện tụt
nhỏ ở một loại câu"), judge Claude chưa mốc người ✓, bộ kín do agent viết ✓, đường không stream ✓. Thiếu: M-1, M-2, m-1.

**Riêng tư:** 5 file 0 trùng chữ ≥ 40 ký tự với Golden / kho / câu kín; không câu hỏi / câu trả lời / chủ đề cụ thể cạnh mã câu; không tên dự án khác; đường dẫn `data/` chỉ là tên file. Đạt.

## 5. Giới hạn hoặc phần chưa chạy

- Không mở bộ kín ⇒ số bộ kín (4,18, CI, theo loại, 4 / 34) chỉ kiểm bằng tính nhất quán nội bộ, không so với file điểm.
- Không chạy lại `do_cuoi.py check|check-judge|analyze` trên bản sao (chỉ đọc kết quả + code `analyze`); không chạy lại T1; không đọc file nhãn judge an toàn / ngày (chỉ file tổng hợp).
- Không kiểm khâu viết / kiểm bộ kín (0 trùng sha, trùng ý) — ngoài phạm vi; chỉ ghi m-2.

## 6. Decision và bước tiếp theo

**changes_requested** — sửa chữ M-1 + M-2 (một lượt, 0 USD, không chạy lại, không mở bộ kín — số Golden 4,82 đã có ở mục 4; nếu muốn CI cho phần "chỉ câu được trả lời" thì tính từ file điểm, chỉ in số);
minor sửa kèm nếu tiện, không cần vòng kiểm riêng. Sau khi sửa, A tự đối chiếu 3 chỗ M-1 + 3 chỗ M-2 rồi trình User; kết luận "không làm hỏng" và mọi sàn **không đổi**. Rủi ro: trung bình (báo cáo cho User / CEO).
User cần biết khi đọc: bản cuối an toàn trên mọi bộ, nhưng trên câu mới chưa ai thấy, câu được trả lời cũng kém đủ ý hơn ~0,2 (không chỉ do từ chối nhầm); tốc độ đo một ngày model trả lời nhanh.
