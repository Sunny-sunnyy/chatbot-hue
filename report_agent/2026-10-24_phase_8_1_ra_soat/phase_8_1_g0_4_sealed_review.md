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

## 8. Thêm dấu cho mọi câu kín (C24, 25/10/2026 11:41–11:48)

User 25/10 11:40: "thêm dấu cho mọi câu". Yêu cầu này thay chỉ dẫn "không dấu" của spec 8.1 §5 G0.4 bước 4. Theo
`CURRENT_HANDOFF.md` mục C24, việc qua **hai sub-agent `general-purpose` mới**: một sửa, một kiểm. Hai sub-agent khác
nhau, người kiểm không xem báo cáo của người sửa. **C vẫn chưa đọc nội dung câu.** 3 dòng `capability_only` (2, 21, 33)
vẫn chờ User; lượt này chỉ thêm dấu.

**Bước 1 — sao lưu (C, `cp`, không đọc):**
- `sealed_authoring.jsonl` → `sealed_authoring_v3_backup.jsonl`, md5 `0377e966ada5` (= bản v3 ở §7);
- `sealed_user_sample.md` (bản 3) → `sealed_user_sample_v3_backup.md`, md5 `ab9a6cbe62da`;
- `check --authoring` trước khi sửa: exit 0; 36 dòng, phân bố 15 / 6 / 7 / 5 / 3.

**Bước 2 — sửa (sub-agent 1):**
- Thêm dấu cho `question` ở **16 dòng**: 1, 5, 6, 7, 8, 11, 15, 18, 22, 23, 24, 26, 28, 30, 31, 34. Trong đó 13 dòng không
  dấu cả câu; 2 dòng thiếu dấu một từ.
- 20 dòng vốn đủ dấu; `reference_answer` cả 36 dòng vốn đủ dấu nên không đổi.
- Giữ nguyên những chỗ không phải chuyện dấu: gõ tắt văn nói, lỗi gõ cố ý, chữ hoa/thường.
- Nghi ngờ nhẹ ở 2 dòng: 22 (địa danh có hai cách viết trong nguồn) và 18 (từ một âm tiết đọc được hai nghĩa).

**C tự kiểm bằng máy (chỉ in số dòng và kết quả đúng/sai):**
- So từng byte với bản sao lưu: đúng 16 dòng trên đổi; 20 dòng giống hệt.
- Chỉ field `question` đổi. Thứ tự key và cách serialize giữ nguyên.
- Bỏ dấu (NFD bỏ combining, đ→d) thì bản mới = bản cũ ở mọi field đổi. Chuỗi mới ở dạng NFC.
- `check --authoring` sau khi sửa: **exit 0**, phân bố không đổi (direct_fact 15 / multi_source 6 / conditional 7 /
  comparative 5 / out_of_scope 3). md5 file mới: **`a095e08bd7ac`**.

**Bước 3 — kiểm độc lập (sub-agent 2), theo báo cáo của nó: ĐẠT.**
- Tự tìm ra cùng 16 dòng đổi; cả 16 dòng OK: không đổi ngoài dấu, không dấu sai nghĩa, tên riêng khớp nguồn, ý không đổi.
- Cả 36 dòng: **0 dòng** còn chữ thiếu dấu. Chữ không dấu còn lại đều vốn không dấu, viết tắt, đơn vị, số hoặc từ nước
  ngoài. Riêng dòng 22: âm tiết không dấu là đúng theo nguồn.
- Đồng ý cách đặt dấu ở mọi từ đa nghĩa (dòng 5, 7, 11, 18, 26, 30, 31, 34), dựa theo đáp án, keyword và nguồn.
- **Để User biết** (không phải lỗi dấu, không đổi so với bản cũ): dòng 3 và 19 có một dạng gõ tắt bớt chữ cái; dòng 13 có
  lỗi gõ cố ý ở phụ âm cuối. User muốn chính tả chuẩn hoàn toàn thì quyết 3 dòng này.
- `check --authoring`: exit 0.

**Bước 4 — mẫu cho User bản 4** (`sealed_user_sample.md`, md5 `ad205c839bd0`, ghi đè bản 3):
- cùng 15 dòng: 2, 5, 11, 12, 13, 17, 18, 20, 21, 24, 25, 28, 31, 33, 36;
- dòng đầu ghi các dòng có câu hỏi được thêm dấu: 5, 11, 18, 24, 28, 31;
- C so với bản sao lưu: diff 14 dòng, đúng bằng 6 câu hỏi đổi cộng dòng đầu ghi chú. Phần còn lại (ô Đồng ý / Sửa / Bỏ,
  ghi chú dòng 2, 21, 33) giữ nguyên.

`sealed_realism.jsonl` không đổi (md5 `b7a679d7e6f0`). Mọi file mới / sửa đều private: `git check-ignore` xác nhận.

**Ghi minh bạch:** báo cáo của sub-agent kiểm liệt kê **tên các file nguồn** đã grep. Vì vậy C biết được chủ đề (tên địa
danh / món / lễ hội) của các câu kín, nhưng không biết câu hỏi, đáp án hay keyword. C không chép các tên đó vào file
tracked nào. Ảnh hưởng tới độ mù: thấp, vì các chủ đề này cũng có trong Golden dev C đã dùng; nhưng C ghi lại để A/User
biết. Lần sau, brief sub-agent cấm cả tên file nguồn trong báo cáo cuối.

**Kết luận C24:** bộ kín v4 (`a095e08bd7ac`) đủ dấu, chỉ đổi dấu, máy kiểm exit 0. Còn chờ User: (1) 3 dòng
`capability_only` 2, 21, 33; (2) duyệt mẫu bản 4; (3) tùy chọn: dòng 3, 19, 13 (gõ tắt / lỗi gõ cố ý). Sau đó A tạo
file chính thức 4 field và khóa (G0.6).

Tiền: **0 USD** (quota Claude Code: sub-agent sửa ~46k, sub-agent kiểm ~62k token).

## 9. Sửa / rà đáp án tham chiếu (C25, 25/10/2026 12:06–12:13)

User đã duyệt mẫu bản 4: câu hỏi ổn, nhưng một đáp án lặp chủ ngữ, thiếu tự nhiên. Nhận xét nguyên văn ở
`sealed_user_feedback_private.md`; **C không đọc** file này. Như C24, việc qua **hai sub-agent `general-purpose` mới**,
một sửa, một kiểm. Brief cả hai cấm ghi nội dung câu, tên thực thể **và tên file nguồn** trong báo cáo cuối (bài học §8).
Chỉ sửa `reference_answer`; câu hỏi giữ bản 4. 3 dòng 2, 21, 33 vẫn chờ User.

**Sao lưu (C, `cp`):** `sealed_authoring.jsonl` → `sealed_authoring_v4_backup.jsonl`, md5 `a095e08bd7ac` (= v4 ở §8).

**Sửa (sub-agent 1)** — 4 dòng, chỉ `reference_answer`:

| Dòng | Loại lỗi | Ảnh hưởng tới chấm |
|---|---|---|
| 11 | lặp chủ ngữ + thiếu tự nhiên (User nêu; sửa đúng theo đề xuất của User) | thấp |
| 18 | lặp nguyên văn một cụm ở hai câu → gộp một câu | thấp |
| 26 | lặp ý (câu cuối nhắc lại điều kiện) → bỏ câu thừa, giữ đủ điều kiện + dữ kiện | thấp |
| 36 | lặp từ + thiếu tự nhiên → viết gọn, số liệu giữ nguyên | thấp |

- Không dòng nào sai so với nguồn hoặc thiếu ý so với nguồn.
- **Thấy nhưng không sửa (cần User quyết), vì sửa sẽ đổi phạm vi đáp án:**
  - Dòng 6: đáp án có thêm một quy định ngoài điều câu hỏi hỏi. Ảnh hưởng **trung bình**: judge có thể trừ Completeness
    khi câu trả lời đúng mà không nêu ý đó.
  - Dòng 3, 19, 24, 29, 33: mỗi dòng có 1–2 dữ kiện phụ, đều đúng nguồn. Ảnh hưởng thấp–trung bình.
  - User quyết chung một lần: giữ, hay dặn judge rằng dữ kiện phụ không bắt buộc.

**C tự kiểm bằng máy (chỉ in số dòng, độ dài, đúng/sai):**
- So từng byte với bản sao lưu: đúng 4 dòng 11, 18, 26, 36 đổi; 32 dòng giống hệt.
- Chỉ field `reference_answer` đổi; thứ tự key, cách serialize và dạng NFC giữ nguyên.
- Mọi keyword có trong đáp án cũ vẫn có trong đáp án mới. Cả 4 đáp án ngắn đi 15–59 ký tự.
- `check --authoring`: **exit 0**, phân bố không đổi (15 / 6 / 7 / 5 / 3). md5 file mới: **`6d413c8d98fa`**.

**Kiểm độc lập (sub-agent 2, không xem báo cáo người sửa): ĐẠT.**
- Tự tìm ra cùng 4 dòng đổi, cả 4 OK. Dòng 11 khớp từng chữ đề xuất của User. Không mất dữ kiện cần, không thêm dữ kiện
  ngoài nguồn, lỗi lặp đã hết.
- 32 dòng không đổi: không thấy lỗi rõ bị bỏ sót. Mọi con số trong đáp án có nguồn đều xuất hiện nguyên văn trong nguồn;
  ngoại lệ là một năm lấy từ câu hỏi để suy luận, suy luận đúng.
- Dòng 17: một keyword chỉ khác chữ hoa đầu câu. Code chấm so sau `casefold` nên không ảnh hưởng.
- Dòng 6: câu mở đầu hơi cứng, không phải lỗi rõ.
- `check --authoring`: exit 0.

**Dọn:** xóa thư mục script tạm của 4 sub-agent C24/C25 (`/tmp/c24_fix`, `/tmp/c24_check`, `/tmp/c25_fix`,
`/tmp/c25_check`), vì có thể chứa nội dung câu kín. Còn lại trong `/tmp` chỉ là output số đếm của `check`.

**Kết luận C25:** bộ kín v5 (`6d413c8d98fa`) đạt. Chờ User:
1. 3 dòng `capability_only` 2, 21, 33;
2. dòng 6 và nhóm dữ kiện phụ (3, 19, 24, 29, 33): giữ hay dặn judge;
3. (tùy chọn) dòng 3, 19, 13 gõ tắt / lỗi gõ cố ý (§8).

Mẫu cho User bản 4 **chưa** cập nhật đáp án mới của dòng 11, 18, 36 (trong mẫu). A quyết có cần bản 5 không. Sau đó A tạo
file chính thức 4 field và khóa (G0.6).

Tiền: **0 USD** (quota Claude Code: sub-agent sửa ~103k, sub-agent kiểm ~56k token).

## 10. Áp sửa User duyệt 12:20 (C26, 25/10/2026 12:21–12:31)

User 12:20 duyệt "sửa theo đề xuất". Nguyên tắc: đáp án chỉ trả lời điều câu hỏi hỏi; chỉ thêm điều kiện khi thiếu nó thì
sai hoặc gây hiểu lầm; chi tiết phụ đúng nguồn giữ nguyên. Cụ thể:
- dòng 2, 21, 33 (`capability_only`) sửa theo đề xuất ghi chú v3;
- dòng 6 bỏ quy định ngoài điều câu hỏi hỏi;
- dòng 3, 19, 24, 29, 33 giữ chi tiết phụ.

Việc qua **hai sub-agent `general-purpose` mới**, một sửa, một kiểm. Brief cấm nội dung câu, tên thực thể và tên file
nguồn trong báo cáo cuối. **C vẫn chưa đọc nội dung câu.**

**Sao lưu (C, `cp`):**
- `sealed_authoring_v5_backup.jsonl`: md5 `6d413c8d98fa` (= v5 ở §9);
- `sealed_realism_v5_backup.jsonl`: `b7a679d7e6f0`;
- `sealed_user_sample_v4_backup.md`: `ad205c839bd0`.

**Sửa (sub-agent 1):**

| Dòng | Field đổi | Ghi chú |
|---|---|---|
| 2 (direct_fact) | question, keywords (2 → 1), reference_answer | **Lệch đề xuất có lý do:** nguồn của dòng không có loại thông tin đề xuất nêu làm ví dụ; đổi sang nguồn khác sẽ lệch `partition` ⇒ chọn một thông tin thiết thực khác trong cùng nguồn |
| 6 (conditional) | reference_answer | bỏ câu nêu quy định ngoài điều câu hỏi hỏi; 2 keyword giữ |
| 21 (comparative) | question, reference_answer | theo đề xuất; thêm một điều kiện có trong nguồn (thiếu thì gây hiểu lầm) |
| 33 (multi_source) | question, keywords (3 → 2), reference_answer, sources (2 → 3) | theo đề xuất; bỏ keyword của phần đã bỏ. **Lệch có lý do:** không đặt keyword cho phần mới vì hai nguồn ghi khác nhau, đáp án ghi cả hai |

Dòng 3, 19, 24, 29 không đổi; dòng 33 giữ chi tiết phụ.

**C tự kiểm bằng máy (không in nội dung):**
- Đúng 4 dòng 2, 6, 21, 33 khác bản v5; 32 dòng giống từng byte.
- Category không đổi. Serialize và NFC giữ nguyên.
- `check --authoring`: **exit 0**, phân bố 15 / 6 / 7 / 5 / 3.
- md5 bản mới: **`631334704fdd`**.

**Kiểm độc lập (sub-agent 2, không xem báo cáo người sửa): ĐẠT.**
- Dòng đổi và field đổi khớp. So với bản User xem ở mẫu bản 4, có 8 dòng đổi: 2, 6, 11, 18, 21, 26, 33, 36.
- Dòng 2, 6, 21 OK. Dòng 33 OK, kèm 2 ghi chú mức thấp:
  - đáp án diễn đạt một mốc thời gian mềm hơn chữ trong nguồn; phần đó không có keyword nên không ảnh hưởng chấm;
  - nhãn `multi_source` yếu, vì một nguồn đã trả lời được cả hai ý.
- Hai chỗ lệch đề xuất (dòng 2, 33): **chấp nhận**. Người kiểm tự grep xác nhận lý do của người sửa.
- **Không trùng ý Golden**: dò cả 176 câu; có vài câu cùng thực thể nhưng hỏi dữ kiện khác.
- Độ tự nhiên cuối: dòng 2, 21, 33 đều **natural**.
- `check --authoring`: exit 0.

**Nhãn độ tự nhiên** (`sealed_realism.jsonl`, sửa bởi người kiểm; md5 `d1f7c235b83c`). C so với backup: chỉ dòng 2, 21, 33
đổi, và chỉ ở `changed` (false → true) + `reason`. Nhãn vẫn natural, vì file vốn ghi natural; chỉ người duyệt v3 chấm
capability_only. Phân bố: **natural 36** / capability_only 0 / unnatural 0.

**Mẫu cho User bản 5** (`sealed_user_sample.md`, md5 `4f7fe6df5cca`, ghi đè bản 4):
- 17 dòng: 15 dòng của bản 4, thêm dòng 6 và 26 (đáp án đổi sau khi User xem bản 4);
- 8 dòng đổi đánh dấu "[ĐỔI: …]", ghi rõ field đổi; dòng đầu file liệt kê đủ;
- ghi chú cũ của dòng 2, 21, 33 thay bằng "Đã sửa theo đề xuất, User duyệt 12:20";
- người kiểm tự thêm (ngoài brief, C chấp nhận vì giúp User xem lần cuối): mục "Lưu ý" về chỗ lệch đề xuất ở dòng 2 và
  33, mục "Keyword (mới)" ở dòng 2 và 33.

Mọi file mới / sửa đều private (`git check-ignore`).

**Ghi minh bạch (theo báo cáo người sửa):** một lệnh grep trong corpus của người sửa vô tình in 1 dòng từ mỗi file trong
3 file mẫu cho User (`sealed_user_sample*.md`, loại file bị cấm đọc). Cả 3 dòng là đề xuất sửa dòng 2, trùng nội dung ghi
chú v3 mà người sửa được đọc. Người sửa không mở các file đó. Ảnh hưởng: không đáng kể. Bài học: grep trong corpus nên
loại trừ `evaluation/`.

**Dọn:** đã xóa `/tmp/c26_fix`, `/tmp/c26_check` (script của sub-agent, có thể chứa nội dung câu kín).

**Kết luận C26:** bộ kín v6 (`631334704fdd`) đạt, 36/36 natural, `check` exit 0. Chờ: User xem mẫu bản 5 lần cuối.
Sau đó A tạo file chính thức 4 field và khóa (G0.6).

Tiền: **0 USD** (quota Claude Code: sub-agent sửa ~76k, sub-agent kiểm ~75k token).
