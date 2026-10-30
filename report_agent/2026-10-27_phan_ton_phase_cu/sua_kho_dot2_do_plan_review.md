# Review C85: B90 — tham số harness, `dot2.jsonl` bản 4, phụ lục plan đo đợt 2

Người kiểm: C (Claude Opus 5.5, `hue-rag-ef`) · Date: vòng 1 viết tối 29/10/2026, sau 21:16 (`date` cuối trước khi Bash bị chặn); dòng này điền 11:02 30/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` C85. Người làm: B (`hue-rag-a7`).
Đầu vào (sha B báo): `tools/apply_edits.py` `8e934bbb2a7a`, `tools/truoc_sau.py` `d02bc33650f5`, `dot2/edits/dot2.jsonl` bản 4 `cdec67127c4d`, `dot2/b90_quyet_dinh.md` `2e9b25867a06`,
`sua_kho_dot2_do_plan.md` `6d4a5c6293e2`. **Bản này là vòng 1, chưa đủ cổng:** trong lúc review, Bash / WebFetch / SendMessage của C bị chặn (lỗi server máy kiểm an toàn
của auto mode) ⇒ chỉ đọc file được. Phần NOT RUN ghi ở §4; kết luận cuối chờ phần đó.
File tracked: chỉ mã mục, không chép câu kho (S40).

## 0. Kết luận — vòng 3 (11:11 30/10/2026): `ready_for_user_confirmation`, xem §6. Vòng 2 (C87, C `hue-rag-0e`, 11:07 30/10/2026 `date`) — xem §5

`changes_requested` — 0 blocker / 1 major / 1 minor. Bản 4b `dot2.jsonl` **đạt** (mọi kiểm máy + đọc lại 3 nguồn khớp); M-1, M-2, M-3, m-1, m-2 **đóng**; mới: **M-4** plan §6 bước 1
chạy `dump-headings --arm truoc` khi file edit đã áp chưa có ⇒ lệnh dừng (tái tạo được); m-4 câu lý do K017 trong bảng. Sửa M-4 là một dòng plan ⇒ vòng 3 C chỉ kiểm phần đó.

## 1. Kết luận vòng 1

`changes_requested` — 0 blocker / 3 major / 3 minor. (a) code: đạt (2 minor). (b) `dot2.jsonl`: 1 major (D1). (c) plan: 2 major (sàn A2).

**A quyết (tin nhắn A 29/10, sau vòng 1):** M-3 ⇒ **bỏ cả dòng** "Đơn vị quản lý" ở D1-K004 (3) và (4); (1), (2) giữ như B90. M-2 ⇒ nhận sàn C84 (P0_sai mới ≤ 2 đếm hai
chiều + sinh lại 3 lần mỗi câu P0_sai mới; đảo cảnh báo = 0). M-1 ⇒ B ghi trước thủ tục phân loại trong phụ lục. Vòng 2 (C kiểm phần sửa + §4) làm phiên sau, **trước
bước 1** áp kho.

## 2. Findings

### M-1 (plan §5, sàn A2 vế 2) — "đảo cảnh báo" không có cách đo

- **Vị trí:** `sua_kho_dot2_do_plan.md` §5 "Sàn A2": "0 câu mới mà lỗi là đảo cảnh báo an toàn / điều kiện vào (rubric B89 tách loại lỗi P0)".
- **Bằng chứng:** rubric `data/loi_nang_2026-10-28/rubric.md` (`b1b2848be9c6`) bước 2–3 chỉ có nhãn ý `có / không có / trái` + cờ `condition`; **không** có trường loại lỗi.
  Loại "đảo cảnh báo" chỉ có ở khóa đối chứng (`an_toan/controls_key.json`, trường `how`) — câu thật không có.
- **Tác động:** sàn hạng 1 của User không đo được như ghi ⇒ ai đó sẽ phân loại sau khi thấy dữ liệu (tiêu chí không còn "ghi trước").
- **Đóng khi:** plan ghi trước thủ tục: mọi câu P0_sai **mới** ⇒ một người không viết câu trả lời (C, hoặc sub-agent mới) đọc ý bị gắn + ngữ cảnh, phân vào đúng một loại
  ghi sẵn: (i) **đảo cảnh báo / điều kiện vào** — ý `condition` cho phép / bỏ qua điều ngữ cảnh cấm hay cảnh báo, hoặc đổi ngưỡng / đối tượng / giờ thành giá trị ngữ cảnh
  không có; (ii) nói sai **về nguồn** ("nguồn không nêu", "chưa thống nhất" khi nguồn có / không mâu thuẫn — kiểu S11 / S12 của B89); (iii) khác. Sàn 0 áp cho (i).

### M-2 (plan §5, sàn A2 vế 1) — N_AA chưa định nghĩa đủ để ghi trước (sửa sau khi có số C84)

- **Vị trí:** §5 bộ an toàn: N_AA = "số câu đổi nhãn giữa lượt B89 ↔ lượt A/A C84"; sàn: "P0_sai **mới** (ở 'sau', không ở B89) ≤ N_AA".
- **Bằng chứng (C84, `do_loi_nang_aa_implementation.md`):** lượt 1 (B89) P0_sai 2 câu, lượt 2 0 câu ⇒ 2 câu đổi, **cả hai cùng chiều** (mất ở lượt 2), 0 câu thêm. Chấm lại lượt 1
  khớp nhãn B89 0 câu đổi ⇒ nhiễu ở bước **sinh**, không ở judge. Đếm một chiều ("mới ở lượt 2") cho 0 — nhưng hai lượt cùng cấu hình là **hoán đổi được** (lượt nào làm mốc
  cũng được), nên 0 một chiều chỉ là may của một cặp: chính 2 câu đó cho thấy một lượt bất kỳ có thể sinh ra ~2 câu P0_sai dao động.
- **Tác động:** định nghĩa mơ hồ ⇒ ngưỡng 0 (một chiều) hay 2 (hai chiều) chọn được sau khi thấy dữ liệu; ngưỡng 0 sẽ báo động giả khi kho sửa không liên quan.
- **Đóng khi:** ghi số: **N_AA(P0_sai) = 2, N_AA(H) = 2** (tổng câu đổi hai chiều, C84) ⇒ A2 vế 1: P0_sai mới ≤ 2; **và** mỗi câu P0_sai mới (kể cả khi ≤ 2) được sinh lại 3 lần
  cả mốc lẫn "sau" (cách (b), ≈ 0,0015 USD / câu) và ghi số lần — vượt mốc rõ (vd 3 / 3 ở "sau", 0 / 3 ở mốc) ⇒ báo A dù dưới ngưỡng. Vế 2 (đảo cảnh báo, M-1) vẫn sàn 0.

### M-3 (`dot2.jsonl`, D1-K004 dòng (3) và (4)) — đổi vai trò "phối hợp" thành "đơn vị quản lý" là khẳng định mới không nguồn

- **Vị trí:** `b90_quyet_dinh.md` §1 dòng D1-K004 (3) (file phố đi bộ thứ nhất) và (4) (file phố đi bộ thứ hai). B đã tự ghi "vai trò đổi nhẹ".
- **Bằng chứng:** câu cũ: cơ quan cấp quận là đơn vị quản lý, các cơ quan còn lại **phối hợp**. Câu mới: bỏ cấp quận và đưa cơ quan phối hợp lên làm đơn vị quản lý. Bảng ghi
  nguồn "—": không nguồn nào nói các cơ quan đó quản lý từ 01/07/2025. Dòng (1) khác: Sở vốn là chủ thể, chỉ bỏ vế "phối hợp cùng quận" ⇒ thuần bớt, đạt. Dòng (2) đạt.
- **Tác động:** trái luật User 29/10 mục 3 ("chỉ vào đợt 2 khi có nguồn … không thì sửa thành câu nguồn nói đúng, hoặc bỏ"). Câu hỏi "ai quản lý phố đi bộ" sẽ được trả lời
  chắc bằng một khẳng định kho chưa từng có.
- **Đóng khi:** (i) **khuyên:** bỏ cả dòng "Đơn vị quản lý" ở 2 file (không còn biết chắc ai quản lý; luật kho: không ghi field rỗng) — mất: câu hỏi về đơn vị quản lý 2 phố
  thành "kho không có" (thiếu ý, hạng 4); hoặc (ii) giữ vai trò cũ, chỉ bỏ cơ quan không còn: đổi nhãn dòng thành vai trò phối hợp — vẫn là suy ra rằng việc phối hợp
  còn sau sáp nhập, kém chắc hơn (i). Chọn (i) hay (ii): A.

### m-1 (`truoc_sau.py` `analyze`) — tên khóa W6 gắn cứng bản nhãn

- `analyze()` trả `"truoc_v3"` / `"sau_v4"` (dòng 458 bản mới) dù nhãn nay lấy từ `--gold-truoc` / `--gold-sau` ⇒ đợt 2 (v4 ↔ v5 / v4) ghi nhãn sai tên. Đổi thành
  `"truoc"` / `"sau"` + ghi tên file nhãn vào kết quả. Không đổi số.

### m-2 (`truoc_sau.py` `touched`) — lý do (d) vẫn tính ở đợt 2

- Lý do (d) "context trước có file danh mục" vẫn chạy với `--work dot2`. Vô hại (file đó đã loại khỏi discovery từ đợt 1 nên không thể có trong context) nhưng plan §5 nói
  "(d) không áp ở đợt 2" ⇒ in `by_reason.d` phải = 0; ghi một câu vào report thay vì sửa code.

### m-3 (`dot2.jsonl` D7-K069) — câu rào nói về mức hiểu biết của kho — **hết hiệu lực: A đã quyết bỏ edit D7 (bản 4b, `CURRENT_HANDOFF.md` B90)**; vòng 2 kiểm bản 4b

- Thêm cụm "chưa xác minh tình trạng gia hạn sau ngày này": không thêm fact về thế giới, chỉ chặn việc chatbot suy "đã hết hạn" ⇒ **C nhận** là làm yếu hợp luật. Gợi ý câu
  tự nhiên hơn cho người đọc ("chưa rõ đã gia hạn hay chưa") — B / A tự chọn, không chặn.

## 3. Đã kiểm, đạt

- **(a) `apply_edits.py`** (đọc cả hai bản, so tay vì Bash bị chặn): chỉ thêm `--edits` (danh sách file, thay bộ mặc định; khi có thì **không** nối `diffs_them`) và
  `--record` (mặc định = `applied_edits.jsonl` cũ). Kiểm "đúng 1 lần", "backup giống byte", "record đã có ⇒ dừng" giữ nguyên và chạy **trước** khi ghi file kho. `SKIP K091`
  vẫn áp — vô hại cho đợt 2.
- **(a) `truoc_sau.py`:** `configure()` gán lại `SK`, `ARM_DIR`, `APPLIED`, `BACKUP`, `JUDGE`, `GOLD` một lần trong `main()` trước mọi lệnh; mặc định argparse = đúng đường
  dẫn đợt 1 (`work` = `data/sua_kho_2026-10-27`, `applied_edits.jsonl`, `backup_sua_kho_2026-10-28`, gold v3 ↔ v4 — khớp bản cũ dòng 425). `touched()` đọc `APPLIED` thay đường
  dẫn cứng; `analyze()` đọc `GOLD`. `choices=list(ARM_DIR)` tính trước `configure` nhưng khóa không đổi. Không đổi logic đo.
- **(b) 12 mục làm yếu** (đọc cặp câu cũ / mới trong `b90_quyet_dinh.md`): D1 (1)(2), D4 (1)(2), D5, Q2, Q3 (1)(2), Q5, Q10, Q12, Q14 (1)(2), Q15 — câu mới chỉ bỏ con số / cụm
  khẳng định / chữ "duy nhất"–"chỉ", không thêm ý mới, câu còn nguyên nghĩa. Q6 thêm "cổng vào" + "khoảng": B dẫn chính file đó gọi số nhà đó là cổng vào — **chưa** kiểm bằng
  `grep_kb.sh` (§4). Nhóm vé / điều kiện vào: Q2 bỏ giờ xuất phát, Q5 bỏ khung giờ trong ngoặc (hai khung chi tiết còn), Q14 bỏ tính độc quyền của một chính sách hoàn
  tiền, Q15 bỏ độ dài giai đoạn (mốc ngày còn) — đều theo hướng bớt điều kiện, không đổi điều kiện ⇒ rủi ro là "thiếu ý", plan đã có W9.
- **(c) plan:** §2 bốn kiểm "còn hiệu lực" + giới hạn trôi theo ngày (ghi trước, không tự kết luận) — đạt; §4 lý do (e) cho 2 tiêu đề đổi — đạt (code chưa viết, plan nói C đọc
  diff trước bước 9); §3 backup đợt 2 thư mục **mới** — đạt; trần 0,10 USD, ước 0,082 — đạt.

## 4. NOT RUN (vòng 2 làm khi công cụ chạy lại)

1. **Đọc lại độc lập 3 nguồn** (luật người thứ hai): K017 (cổng HĐND), D2 (bài Luật Di sản sửa đổi), D6 (bài Tuần lễ Âm nhạc) — WebFetch bị chặn. Chưa xác nhận edit
   K017 (2), D2, D6 khớp nguyên văn nguồn.
2. Máy: `sha256sum` 5 file đầu vào; `diff` hai bản script; 104 edit cũ bản 4 giống bản 3 (trừ K017 edit 2); bảng `b90_quyet_dinh.md` khớp `dot2.jsonl`; `apply_edits.py --edits`
   chạy thử trong bộ nhớ (124 / 41, 0 lỗi); `grep_kb.sh` cho Q6.

## 5. Vòng 2 (C87, 11:07 30/10/2026 `date`) — bản 4b + plan bản 2 + phần NOT RUN vòng 1

**Đầu vào — sha tính từ file (12 ký tự), khớp sha B báo 11:01:** `dot2/edits/dot2.jsonl` bản 4b `c0b5876ea510`; plan `26e974dc56ff`; bảng `b90_quyet_dinh.md` `42b89bd818f4`;
`tools/apply_edits.py` `8e934bbb2a7a`; `tools/truoc_sau.py` `157f8acc0707`; builder `dot2/tools/build_dot2_b90.py` `f2049a793093`; bản 4 giữ `edits_v4_cdec67127c4d/dot2.jsonl`
`cdec67127c4d`; bản 3 giữ `9b5105b35e8b`. Bản trước B90: `tools/truoc_b90/apply_edits.py` `9e8c6a96360d`, `truoc_sau.py` `61e9dcc863e1`.

### 5.1 Phần NOT RUN vòng 1 — đã chạy

1. **Đọc lại độc lập 3 nguồn** (người thứ hai, luật User 29/10 mục 3): `curl` + tách chữ (K017 cần cookie do JS đặt, như A 29/10; D2 trang trả gzip); WebFetch thử thêm (K017 trả trang rỗng;
   D2, D6 khớp bản curl). Trích nguyên văn + so từng ý: `data/sua_kho_2026-10-27/dot2/c87_doc_lai_nguon_2026-10-30.md` (private).
   - **K017 edit 2: khớp** — chiều dài cầu, chiều dài tuyến, vốn giai đoạn 1 gắn với tuyến (không với cầu), ngày thông xe kỹ thuật, việc cho lưu thông: đều đúng nguyên văn; tên kết cấu nhịp
     không có trong trang ⇒ bỏ đúng. (Lệch nhỏ ở câu lý do — m-4.)
   - **D2: khớp** — nguồn chỉ nêu một ngày cho Ngày Di sản văn hóa; ngày thứ hai trong câu kho cũ không phải Ngày Di sản (là một ngày kỷ niệm khác, theo một bài khác cùng trang); nguồn không
     nói miễn vé ngày nào ⇒ bỏ ngày thứ hai đúng luật (bớt con số tranh cãi). Rủi ro còn lại là "thiếu ý" nếu điểm đó thật có miễn vé ngày thứ hai ⇒ để tra ngoài; nhóm "vé / điều kiện
     vào" của plan §5 đã có bước C đọc câu trả lời.
   - **D6: khớp** — hai nghệ sĩ bị bỏ khỏi dòng đêm thứ hai thuộc đêm bế mạc theo nguồn. Ghi chú: nguồn không nêu nghệ sĩ nào cho đêm đó và không có hai tên chương trình mà dòng kho
     ghi ⇒ phần còn lại của dòng dựa nguồn cũ của kho; edit không thêm chúng ⇒ không phải finding đợt 2.
2. **Máy:**
   - Bản 4b ↔ bản 3: 104 edit đầu cùng thứ tự / file; khác **đúng 1** (K017 edit 2, cùng `old`); metadata mục cũ chỉ đổi `checked_at` + thêm `b90` ở K017. ✓
   - Bản 4b ↔ bản 4: bỏ đúng D7-K069; thứ tự mục giữ; khác đúng D1-K004 edit 3, 4 (`new` rỗng, `old` = trọn một dòng, bắt đầu đầu dòng, kết thúc `\n`). ✓
   - Bảng ↔ jsonl: 20 edit B90 (19 + K017 edit 2) — `old` và `new` có mặt nguyên văn trong bảng §1: **20 / 20**; không còn chỗ giữ chỗ `SHA_4B` / `SHA_TS` / `COUNT_4B` / `FILES_4B`. ✓
   - `apply_edits.py --edits dot2/edits/dot2.jsonl --record dot2/applied_edits_dot2.jsonl` (không `--write`): `{"edits": 123, "sources": 20, "files": 40, "empty_new": 2}`, file record
     **không** được tạo. ✓ Kiểm cấu trúc trên văn bản sau áp trong bộ nhớ (40 file): mọi file bắt đầu `#`; 0 dòng trống ba / khoảng trắng đôi / ngoặc rỗng / khoảng trước dấu câu mới;
     số dòng tiêu đề không đổi; 0 mục rỗng mới (2 dòng xóa không để lại tiêu đề trống); tiêu đề đổi chữ chỉ ở 2 dòng của file hướng dẫn nghệ thuật biểu diễn (2 edit K004 đã biết). ✓
   - `diff` `apply_edits.py` với `truoc_b90/`: chỉ `--edits` / `--record` như vòng 1. `truoc_sau.py`: phần vòng 1 + `dump-headings`, lý do `e`, khóa W6 (m-1); `py_compile` đạt.
   - Q6 (`scripts/grep_kb.sh --dir travel`): chính file đó có dòng chỉ đường gọi số nhà đó là **cổng vào** ⇒ câu mới khớp câu cùng file. ✓ Edit Q6 áp sau K004 edit trên cùng dòng — chạy thử
     tuần tự 0 lỗi. ✓
   - **Lý do `e` thử trên Qdrant thật (chỉ đọc, scroll lọc `source`, không ghi file):** 2 edit có `old` bắt đầu `#`, mỗi `old` = trọn dòng tiêu đề; file có 81 đoạn; tiêu đề cũ khớp
     `heading_path` của 4 và 6 đoạn ⇒ `touched` sẽ không dừng ở "no chunk". Tiêu đề mới là chuỗi con của tiêu đề cũ; trên dữ liệu hiện tại tập đoạn chứa chữ mới **trùng đúng** tập chứa
     chữ cũ ⇒ so chuỗi con không bắt nhầm đoạn khác. ✓

### 5.2 Finding cũ

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| M-1 | đóng | plan §5 A2 vế 2: 3 loại ghi trước, người phân loại không viết câu trả lời, phân vân ⇒ (i) |
| M-2 | đóng | plan §5: N_AA(P0_sai) = 2, N_AA(H) = 2 hai chiều; sinh lại 3 lần; giới hạn "mốc chỉ sinh lại 2 câu S11 / S12 trước bước 5" ghi rõ — chấp nhận được, đã ghi trước |
| M-3 | đóng | bản 4b xóa trọn dòng ở 2 file (kiểm máy §5.1) |
| m-1 | đóng | `analyze` trả `truoc` / `sau` + `gold_files` |
| m-2 | đóng | plan §5: `by_reason.d` phải = 0, ghi trong report |
| m-3 | hết hiệu lực | D7 bỏ ở bản 4b |

### 5.3 Finding mới

#### M-4 (plan §6 bước 1 ↔ `truoc_sau.py` `heading_edits`) — `dump-headings --arm truoc` ở bước 1 chạy khi file edit đã áp chưa có ⇒ dừng

- **Vị trí:** plan §6 bước 1 ghi `dump-headings --arm truoc (§4)`; `heading_edits()` đọc `--applied` (`dot2/applied_edits_dot2.jsonl`), file này chỉ được ghi ở **bước 2**
  (`apply_edits.py … --write`).
- **Bằng chứng (chạy thật, 30/10, `--work /tmp/c87_wk`, không ghi gì):** `dump-headings --arm truoc` ⇒ `FileNotFoundError: …/dot2/applied_edits_dot2.jsonl`.
- **Tác động:** bước 1 như viết không chạy được. Lỗi to tiếng (không hỏng dữ liệu), nhưng `headings_truoc.json` **chỉ lấy được khi index cũ còn** — dời tay sai chỗ (sau bước 5) là mất
  bên "trước" của luật (e), chỉ cứu bằng snapshot.
- **Đóng khi:** plan §6 dời `dump-headings --arm truoc` sang **sau bước 2, trước bước 5** (Qdrant chưa đổi tới bước 5 — khớp §4 "trước bước 5"); hoặc `heading_edits()` đọc file
  `--edits` thay vì file đã áp. C khuyên cách đầu (một dòng plan, không đổi code). Ghi lại sha plan.

#### m-4 (`b90_quyet_dinh.md` §1 dòng K017, cột lý do) — câu lý do nói một cụm "không nguồn" trong khi nguồn có ý gần như vậy

- Nguồn có cụm "đã cơ bản hoàn thành các hạng mục chính"; bảng ghi cụm "đã cơ bản hoàn thiện" là không nguồn. Bỏ cụm này vẫn hợp luật (chỉ bớt) ⇒ không đổi edit; sửa câu lý do cho
  đúng (vd "gần nguồn nhưng không cần, bỏ cho gọn") để người đọc sau không hiểu nhầm nguồn. Không chặn.

### 5.4 Trả lời câu hỏi plan §8 (harness bộ an toàn)

C84 không sửa `an_toan_gen.py` / `an_toan.py`: viết script riêng `data/loi_nang_2026-10-28/tools/an_toan_aa.py` gọi đường production `answer_case` (10 đoạn), ghi vào thư mục mới
`aa_2026-10-29/`. Bên "sau" đợt 2 dùng lại được cách này (thêm tham số thư mục ra, hoặc chép script với đích `sau_dot2_<ngày>/`) — sửa code thì C kiểm diff, như plan §5 ghi.

### 5.5 Kết luận vòng 2

`changes_requested` 0 / 1 / 1. `dot2.jsonl` bản 4b `c0b5876ea510` **đạt** — A duyệt sha được ngay; plan cần sửa M-4 (một dòng) rồi A duyệt sha plan mới sau khi C kiểm phần sửa.
File tạm của vòng này: `/tmp/c87_src/` (HTML nguồn web), `/tmp/c87_tools/` (script kiểm, có đọc kho trong bộ nhớ, không ghi chữ kho ra file) — xóa khi xong.

## 6. Vòng 3 (C, 11:11 30/10/2026 `date`) — chỉ phần sửa M-4, m-4

Đầu vào (sha từ file): plan bản 3 `5f30ac7eac16` (bản 2 `26e974dc56ff`); bảng `92e5b3caf6f1`; `dot2.jsonl` `c0b5876ea510` (không đổi — A duyệt 11:09); `truoc_sau.py` `157f8acc0707`,
`apply_edits.py` `8e934bbb2a7a` (không đổi). Bản 2 không giữ bản sao ⇒ so phần sửa với nội dung bản 2 C đọc ở vòng 2.

- **M-4 — đóng.** §6 bước 1 không còn `dump-headings`; bước 2 thêm `dump-headings --arm truoc` **ngay sau áp, trước bước 5**, ghi lý do (file đã áp chỉ có sau `--write`) — đúng thứ tự
  code đòi (vòng 2 tái tạo lỗi) và khớp §4 "trước bước 5"; bước 9 (`--arm sau`) không đổi. §8 sửa "bước 2 / 9"; §9 thêm dòng "Bản 3"; header ghi bản 3. Phần còn lại của bước 1
  (4 kiểm, sao lưu, sinh lại 2 câu S11 / S12) giữ như bản 2.
- **m-4 — đóng.** Câu lý do K017 nay ghi cụm đó "gần ý nguồn … bỏ cho gọn, chỉ bớt" kèm cụm nguồn; không còn câu "không nguồn" cho cụm này. Bảng ↔ jsonl vẫn 20 / 20.

**Kết luận vòng 3: `ready_for_user_confirmation`** — 0 / 0 / 0 còn mở. A duyệt sha plan `5f30ac7eac16` (+ bảng `92e5b3caf6f1`) được.
