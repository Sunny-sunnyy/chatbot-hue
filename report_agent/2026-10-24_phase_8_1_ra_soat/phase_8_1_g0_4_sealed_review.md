# Review: Phase 8.1 G0.4 — 36 câu kín (C17)

Decision: **changes_requested** (0 blocker; 1 major: 9/36 câu trùng ý Golden; 1 câu mơ hồ) — chờ User duyệt
mẫu rồi tác giả sửa
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a3`) qua **một sub-agent `general-purpose` mới**
Date: 24/10/2026, 21:04–21:16 (giờ lấy bằng `date`)
File được review (private): `knowledge-base-hue/evaluation/phase_8_1/sealed_authoring.jsonl` (36 dòng,
md5 `af809684…`, sửa lần cuối 20:58; sub-agent không sửa file này)

**C chưa đọc nội dung câu hỏi, đáp án hay keyword.** C giữ "mù" vì sẽ chạy thí nghiệm 8.1. C chỉ đọc báo
cáo tóm tắt của sub-agent (số dòng, số đếm, nhãn lỗi) và tự chạy lại máy kiểm (chỉ xem exit code và số
đếm). Report này không chép câu hỏi, đáp án, keyword hay tên thực thể.

## 1. Cách làm

- **Brief cho sub-agent** (viết trong prompt giao việc, không lưu file): đọc file kín, các file `sources`
  của từng dòng, Golden 176 (chỉ để tìm câu trùng ý), spec 7A §3/§4/§6. Kiểm từng dòng:
  - đáp án đúng theo nguồn;
  - khách quan, không lộ đáp án;
  - đúng nhãn loại câu;
  - luật keyword;
  - câu `out_of_scope` thật sự vắng khỏi toàn kho (grep có/không dấu, loại `evaluation/`,
    `_source-dumps/`, `meta/`);
  - không trùng ý Golden.

  Xem kỹ dòng 6, 22, 36. Chỉ đề xuất sửa, không sửa. Không gọi API trả phí.
- **Đầu ra private của sub-agent** (git-ignored):
  - `knowledge-base-hue/evaluation/phase_8_1/sealed_review_notes_private.md`: bảng từng dòng, bằng chứng
    (file + heading), đề xuất sửa, log grep, bản đồ trùng Golden;
  - `knowledge-base-hue/evaluation/phase_8_1/sealed_user_sample.md`: mẫu cho User duyệt.
- **C tự kiểm lại:**
  - `golden_full_corpus check --authoring` → exit 0, 36 dòng (direct_fact 14 / multi_source 7 /
    conditional 7 / comparative 5 / out_of_scope 3);
  - md5 file kín không đổi;
  - hai file đầu ra tồn tại và `git check-ignore` xác nhận private.

## 2. Kết quả (theo báo cáo sub-agent)

- **Máy kiểm:** exit 0, 0 lỗi. Sub-agent kiểm thêm: mọi keyword có nguyên văn trong chính nguồn của dòng
  và trong đáp án tham chiếu.
- **Kết luận từng dòng:** 26 OK (16 OK, 10 OK kèm ghi chú), **10 ISSUE**.

| Loại câu | Số dòng | Dòng ISSUE |
|---|---:|---|
| direct_fact | 14 | 2, 23 |
| multi_source | 7 | 5, 12, 33, 36 |
| conditional | 7 | 10, 26 |
| comparative | 5 | 21 |
| out_of_scope | 3 | 20 |

**Theo loại lỗi:**

- `duplicate_of_golden`: **9 dòng**. Hỏi cùng dữ kiện với câu Golden đã có:
  - 2→61, 5→71+168, 10→27, 12→4+24, 20→175, 21→95, 23→74, 26→171, 33→165+51 (số dòng Golden);
  - dòng 20 vẫn là một câu `out_of_scope` đúng, chỉ trùng ý Golden.
- `ambiguous`: **dòng 36**, kèm trùng một phần với Golden 156. Cùng file nguồn còn một con số khác mà một
  câu trả lời đúng cũng có thể trích.
- **Không** có `wrong_label`, `answer_wrong`, `answer_incomplete`, `keyword_rule`,
  `oos_present_in_corpus`, `leak`.

**Trùng một phần, giữ OK kèm ghi chú** (một vế trùng Golden): 11, 16, 19, 25, 27, 35 (và 36 ở trên).

**Cùng dạng câu nhưng khác địa điểm/dữ kiện, giữ:** 3, 4, 6, 7, 28, 30, 34.

**Ba dòng A hỏi:**

- **Dòng 6:** nhãn `conditional` đúng. Đáp án phụ thuộc điều kiện, cùng mẫu với một câu Golden cùng nhãn.
  Có một gợi ý nhỏ: câu mở đầu đáp án mềm hơn quy định gốc.
- **Dòng 22:** suy luận chu kỳ năm **có căn cứ**. Nguồn ghi chu kỳ và một năm mẫu, nên đáp án suy ra
  bằng phép tính từ chính kho. OK.
- **Dòng 36:** nhãn `multi_source` chấp nhận được. Hai dữ kiện nằm ở hai mục `###` khác nhau của cùng một
  file, nên chunker cắt thành hai đoạn khác nhau, đạt "≥2 đoạn" của spec §4. Dòng vẫn ISSUE vì mơ hồ (ở
  trên).

**`out_of_scope` (dòng 7, 14, 20):** cả 3 thật sự vắng khỏi kho. Grep có/không dấu, theo ranh giới từ,
chỉ ra các khớp chuỗi con không liên quan.

**Mẫu cho User** (`sealed_user_sample.md`):

- Seed 20261024. `random.Random(20261024).sample(range(1, 37), 10)` cho các dòng 2, 5, 12, 13, 17, 20,
  24, 25, 28, 33.
- Thêm mọi dòng ISSUE chưa có trong mẫu: 10, 21, 23, 26, 36.
- Thêm dòng 6, 22 (tùy chọn).
- Tổng **17 dòng** (15 bắt buộc + 2 tùy chọn). Mỗi dòng có ô "Đồng ý / Sửa / Bỏ"; ước ~20–30 phút.

Mỗi dòng ISSUE có đề xuất thay thế trong ghi chú private, đã đối chiếu nguồn. Mọi đề xuất giữ nguyên loại
câu và partition, nên phân bố không đổi.

## 3. Findings

- **major M1. 9/36 câu (25%) hỏi lại dữ kiện Golden 176 đã kiểm.**
  - Mục đích của bộ kín là phép kiểm cuối "chưa ai thấy" (spec 8.1 D5). Câu trùng dữ kiện Golden chỉ đo
    lại thứ đã tối ưu trên nhóm thử/kiểm, nên làm yếu phép kiểm. Dù văn phong khác, đáp án và đoạn nguồn
    giống.
  - Tiêu chí đóng: tác giả thay 9 dòng bằng câu hỏi dữ kiện khác. Đề xuất có sẵn trong ghi chú private,
    cùng loại câu và cùng partition. Hoặc User quyết giữ một số dòng như phép thử "cùng dữ kiện, cách hỏi
    đời thường". Nếu giữ, ghi rõ trong report để không tính là câu chưa thấy.
- **minor m1. Dòng 36 mơ hồ** (hai con số có thể đúng). Tiêu chí đóng: sửa câu hỏi để chỉ một đáp án
  đúng, theo đề xuất trong ghi chú.
- **minor m2. Dòng 6:** cân nhắc chỉnh câu mở đầu đáp án tham chiếu cho sát quy định gốc.

## 4. Giới hạn

- C không tự xác minh nội dung (chủ ý giữ mù). Độ đúng của từng kết luận dựa vào **một** sub-agent; User
  duyệt mẫu 17 dòng là lớp kiểm của người.
- 10 dòng OK ngoài mẫu (không bị chọn ngẫu nhiên, không ISSUE) chỉ có một lượt kiểm của sub-agent.
- Câu thay thế (sau khi sửa) cần máy kiểm lại. Dòng 20 thay thế cần grep toàn kho lại để chắc vẫn vắng.

## 5. Bước tiếp theo

1. A đưa `knowledge-base-hue/evaluation/phase_8_1/sealed_user_sample.md` cho User duyệt (~20–30 phút).
   Câu hỏi chính: thay 9 câu trùng Golden, hay giữ một số.
2. Người soạn G0.4 (A giao; theo skill `run-experiment` §2 nên là sub-agent, người điều phối không đọc câu kín)
   sửa theo quyết định User và ghi chú private, rồi chạy lại
   `golden_full_corpus check --authoring` và grep `out_of_scope`.
3. Khóa kín (chỉ mở cuối 8.2). C không đọc nội dung ở bước nào; muốn kiểm lại thì dùng sub-agent mới.

Tiền: **0 USD** (sub-agent dùng quota Claude Code, ~185k token).

## 6. Review lần 2 sau khi sửa (C20, 24/10/2026 21:25–21:34)

User chọn thay cả 9 câu trùng. Một sub-agent của A sửa file. C review lần 2 bằng **một sub-agent
`general-purpose` mới khác** (không đọc ghi chú và mẫu của lần 1 trước khi tự kết luận). **C vẫn chưa đọc
nội dung câu.**

**C tự kiểm (không xem nội dung):**

- Bản trước khi sửa `/tmp/sealed_before.jsonl` có md5 `af809684…`, đúng bản đã review ở lần 1.
- So từng dòng với bản mới (md5 `8488e61c…`): đúng **11 dòng đổi** (2, 5, 6, 10, 12, 20, 21, 23, 26, 33,
  36); **25 dòng còn lại giống từng byte**.
- `check --authoring`: exit 0.
- md5 file kín không đổi sau review lần 2.
- Hai file đầu ra private (`git check-ignore`).

**Kết quả lần 2** (theo báo cáo sub-agent):

- **Máy kiểm:** exit 0, 0 lỗi. Phân bố giữ nguyên: direct_fact 14 / multi_source 7 / conditional 7 /
  comparative 5 / out_of_scope 3.
- **11 dòng đổi: 10 OK, 1 ISSUE.**
  - OK: 2, 5, 6, 10, 12, 20, 21, 23, 26, 33.
  - ISSUE: **dòng 36 — `ambiguous`**. Cách hỏi vẫn khớp hai giá trị khác nhau trong cùng file nguồn. Đề
    xuất sửa: hỏi cả hai vế từ một bảng, nêu rõ mức ngân sách. Sub-agent gợi ý thêm đổi nhãn sang
    `direct_fact`; nếu làm thì phân bố loại câu đổi (multi_source 6 / direct_fact 15), User/A quyết.
- **Trùng lặp:** 0 cặp trùng Golden 176; 0 cặp trùng giữa các câu kín.
- **Dòng 20 (`out_of_scope`):** vắng thật khỏi kho (grep có/không dấu; log trong ghi chú private).
- **Ba dòng người sửa đã lưu ý:**
  - 36: `ambiguous` (ISSUE, như trên).
  - 23: OK. Giá trị chỉ xuất hiện một lần trong toàn kho. Nằm ở mục chỉ đường làm khó tìm hơn, không làm
    câu bất công.
  - 33: OK. Hai file khớp giờ bắt đầu và số suất; chỉ một file có thêm giờ kết thúc khác 5 phút. Bot trích
    file kia vẫn đúng, nên `source_conflict` không đáng kể. Có gợi ý chỉnh chữ đáp án (tùy chọn).
- **Ghi chú tùy chọn:**
  - dòng 12, 33 gắn `multi_source` nhưng trả lời được từ một file; vẫn đạt "≥2 đoạn" của spec;
  - dòng 12, 26 có gợi ý chỉnh chữ;
  - dòng 2, 3, 6 cùng một thực thể nhưng hỏi dữ kiện khác nhau (cụm, không trùng).

**Mẫu cho User (bản 2, ghi đè bản cũ)** — `knowledge-base-hue/evaluation/phase_8_1/sealed_user_sample.md`:

- cùng lượt rút seed 20261024 như lần 1: 2, 5, 12, 13, 17, 20, 24, 25, 28, 33;
- thêm các dòng đổi chưa có trong lượt rút: 6, 10, 21, 23, 26, 36;
- tổng **16 dòng**, ô "Đồng ý / Sửa / Bỏ";
- 5 dòng không đổi trong mẫu (13, 17, 24, 25, 28): sub-agent chỉ đối chiếu nhanh với nguồn, vẫn khớp.

Ghi chú private lần 2: `knowledge-base-hue/evaluation/phase_8_1/sealed_review_notes_private_v2.md`.

**Kết luận lần 2: `changes_requested` (minor).** Chỉ còn dòng 36 mơ hồ. Sau khi sửa dòng 36 (và User
duyệt mẫu 16 dòng), bộ kín đạt. Đề xuất: người sửa (sub-agent) sửa dòng 36 theo ghi chú v2, chạy lại
`check --authoring`. Nếu đổi nhãn thì ghi phân bố mới. Sửa một dòng không cần review lần 3 đầy đủ; một
sub-agent mới kiểm riêng dòng 36 là đủ.

Tiền: **0 USD** (sub-agent dùng quota Claude Code, ~124k token).

## 7. Review lần 3 sau sửa độ tự nhiên (C22, 24/10/2026 22:40–22:46)

User đưa tiêu chí độ tự nhiên: loại câu chỉ đo năng lực tìm chi tiết lạ, kiểu Golden case_index 18 và 142.
Sub-agent của A sửa lần 3. C review bằng **một sub-agent `general-purpose` mới thứ ba**: không đọc ghi chú
lần 1–2 trước khi kết luận, hiệu chỉnh nhãn theo `data/phase_8_1/golden_realism.jsonl`. **C vẫn chưa đọc
nội dung câu.**

**C tự kiểm (không xem nội dung):**

- So từng dòng với bản v2 (`/tmp/c20_sealed_v2.jsonl`, md5 `8488e61c…`): đúng **5 dòng đổi** (11, 18, 24,
  31, 36); **31 dòng giống từng byte**.
- Bản v3 md5 `0377e966…`; sub-agent không sửa file kín lẫn file nhãn `sealed_realism.jsonl`.
- `check --authoring`: exit 0.
- Phân bố: direct_fact 15 / multi_source 6 / conditional 7 / comparative 5 / out_of_scope 3. Dòng 36 đổi
  nhãn multi_source → direct_fact.

**Kết quả lần 3** (theo báo cáo sub-agent):

- **5 dòng đổi: 5/5 OK**, không nhãn lỗi nào.
  - Dòng 11: OK; độ tự nhiên sát biên, vẫn tính là `natural`.
  - Dòng 18: OK; cùng mục nguồn với Golden case_index 126 nhưng hỏi dữ kiện khác, nên không trùng.
  - Dòng 24: OK.
  - Dòng 31: OK. Một file khác ghi mạnh hơn nguồn chính một chút; đáp án viết an toàn nên không gắn
    `source_conflict` (ghi chú private).
  - Dòng 36: OK. Hết mơ hồ; `direct_fact` đúng vì hai giá trị là ô của cùng một bảng trong một mục. Khác
    dữ kiện với câu Golden và câu kín dùng cùng bảng.
- **Độ tự nhiên cả 36 dòng** (nhãn của sub-agent): natural 33 / capability_only **3** / unnatural 0.
  - capability_only: dòng **2, 21, 33** (không đổi ở lần 3). Mỗi dòng có đề xuất sửa trong ghi chú
    private.
  - Lệch với `sealed_realism.jsonl` của người sửa (ghi cả 36 là natural): đúng 3 dòng 2, 21, 33. 5 dòng
    đổi khớp nhãn.
  - Dòng 21 (người sửa lưu ý): `capability_only`. Dữ kiện và keyword đúng, cùng mẫu với Golden case_index
    94/96. Đề xuất đổi cách hỏi, giữ loại `comparative`.
- **Khác:**
  - dòng 19 (không đổi) có nửa câu trùng một phần với Golden case_index 163. Trùng một phần, không chặn.
  - 3 câu `out_of_scope` (7, 14, 20) grep lại vẫn vắng khỏi kho.
- **Ghi minh bạch:** một lần grep thuật ngữ ngoài kho tình cờ in 3 dòng của ghi chú v2 (hàng dòng 20).
  Lúc đó sub-agent đã kết luận xong và không đọc phần khác của ghi chú cũ.

**Mẫu cho User (bản 3, ghi đè)** — `knowledge-base-hue/evaluation/phase_8_1/sealed_user_sample.md`:

- cùng lượt rút seed 20261024 (2, 5, 12, 13, 17, 20, 24, 25, 28, 33);
- thêm các dòng đổi 11, 18, 24, 31, 36 và các dòng capability_only 2, 21, 33;
- bỏ trùng còn **15 dòng**: 2, 5, 11, 12, 13, 17, 18, 20, 21, 24, 25, 28, 31, 33, 36.

Ghi chú private lần 3: `knowledge-base-hue/evaluation/phase_8_1/sealed_review_notes_private_v3.md`.

**Kết luận lần 3:** 5 dòng đổi **đạt**. Còn **3 dòng `capability_only`** (2, 21, 33), lệch với file nhãn
của người sửa. Theo tiêu chí User, các dòng này nên được đổi cách hỏi (đề xuất có sẵn) hoặc User giữ khi
duyệt mẫu. Nếu sửa, chỉ cần một sub-agent mới kiểm riêng 3 dòng đó. File `sealed_realism.jsonl` cần cập
nhật nhãn của 2, 21, 33 theo kết quả cuối.

Tiền: **0 USD** (sub-agent dùng quota Claude Code, ~111k token).
