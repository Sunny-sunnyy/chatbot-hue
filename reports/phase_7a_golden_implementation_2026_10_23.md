# Implementation Report: Phase 7A Golden full-corpus — Task 3 (viết song song)

Implementer: Claude Opus 5.5 (session `hue-rag-08`)
Date: 2026-10-23 (+07)
Base commit: `b688926`
Head commit: worktree (Implementer Git authorization: none)
Risk level: medium
Canonical inputs:

```text
docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md (§3–§6)
docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md (Task 3)
session_prompt/CURRENT_HANDOFF.md (Task 3, Reviewer hue-rag-66)
```

Paid call: không. Git: không. Không sửa curated Markdown, module/test Task 1,
hay 20 case pilot `heritages`. Chưa merge (theo handoff).

## 1. Phạm vi

- Viết 6 file authoring còn lại. Mỗi partition giao cho 1 sub-agent.
- Phần thêm của `heritages` do tôi tự viết: 16 case nối sau 20 case pilot.
- Đọc lại và đối chiếu từng case với `sources`, sửa hoặc xóa case kém.
- Ghi mâu thuẫn mới K11–K50 (file:dòng) vào file mâu thuẫn private.

Report này không chép câu hỏi hay đáp án.

## 2. Thay đổi

| Path | Tracked | Nội dung |
|---|---|---|
| `knowledge-base-hue/<partition>/evaluation/golden_full_corpus_authoring.jsonl` × 7 | private | 180 case |
| `knowledge-base-hue/meta/corpus-contradictions-2026-10-23.md` | private | Append mục "Bổ sung Task 3", K11–K50. K1–K10 giữ nguyên |
| `reports/phase_7a_golden_implementation_2026_10_23.md` | có (mới) | Report này |
| `session_prompt/CURRENT_HANDOFF.md` | có | Chuyển sang `final_review` |

Thư mục `evaluation/` của 6 partition mới được tạo, đúng path ở spec §10.

## 3. Cách đã chạy thật

Chạy từ `backend/`, không gọi mạng:

```text
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/<dir>/evaluation/golden_full_corpus_authoring.jsonl --authoring
```

| Partition | exit | Tổng | direct | multi | cond | comp | oos |
|---|---:|---:|---:|---:|---:|---:|---:|
| foods | 0 | 38 | 17 | 7 | 6 | 5 | 3 |
| heritages | 0 | 36 | 15 | 6 | 6 | 5 | 4 |
| festivals | 0 | 28 | 12 | 5 | 5 | 4 | 2 |
| performing_arts | 0 | 17 | 8 | 2 | 3 | 2 | 2 |
| travel_places | 0 | 34 | 14 | 6 | 6 | 5 | 3 |
| travel_services | 0 | 13 | 5 | 1 | 3 | 2 | 2 |
| travel_tickets | 0 | 14 | 5 | 2 | 3 | 2 | 2 |
| **Tổng** | | **180** | **76** | **29** | **32** | **25** | **18** |

Kiểm thêm:
- `git diff --check`: exit 0.
- Script đếm trùng câu hỏi giữa cả 7 file (sau NFC và casefold): 0 trùng, tổng
  180.
- Không chạy lại pytest: module Task 1 không đổi từ GATE P (`8 passed`).

## 4. So với target

| | Target | Biên ±20% | Thực tế | Đạt |
|---|---:|---:|---:|---|
| direct_fact | ~70 | 56–84 | 76 | có |
| multi_source | ~35 | 28–42 | 29 | có, sát biên dưới |
| conditional | ~30 | 24–36 | 32 | có |
| comparative | ~25 | 20–30 | 25 | có |
| out_of_scope | ~15 | 12–18 | 18 | có, chạm biên trên |
| Tổng | ~175 | | 180 | |

| Partition | Target | Thực tế |
|---|---:|---:|
| foods | ~37 | 38 |
| heritages | ~37 | 36 (20 pilot + 16) |
| festivals | ~27 | 28 |
| performing_arts | ~17 | 17 |
| travel_places | ~32 | 34 |
| travel_services | ~12 | 13 |
| travel_tickets | ~13 | 14 |

`multi_source` thấp ở `travel_services` (1) và `performing_arts` (2). Hai
partition này ít file, và các câu ghép từ ≥2 file thường đụng mâu thuẫn K21–K33
hoặc trùng dữ kiện với partition khác. Tôi không ép thêm case cho đủ số.

## 5. Sub-agent đã dùng

6 sub-agent `general-purpose`, mỗi agent một partition: foods, festivals,
performing_arts, travel_places, travel_services, travel_tickets. Agent chỉ ghi
file authoring của partition mình, không gọi API, không dùng Git.
`heritages` không dùng sub-agent.

Mỗi prompt gồm:
- hướng dẫn viết nguyên văn (bản GATE P);
- spec §3–§6 nguyên văn;
- danh sách file `.md` của partition, lấy từ `discover_full_corpus_files()`;
- target, output path, K1–K10, ranh giới chống trùng.

Mỗi agent báo đã đọc hết file của partition trước khi viết.

**Deviation:** prompt đầu của agent foods tóm tắt spec §3–§6 và K1–K10 thay vì
chép nguyên văn. Khoảng 1 phút sau khi khởi chạy agent, tôi gửi bổ sung qua
SendMessage phần nguyên văn còn thiếu. Tôi không có bằng chứng riêng về thời điểm agent nhận tin so với lúc bắt đầu viết. Case
foods đã được tôi đối chiếu theo đúng hướng dẫn nguyên văn (§6). Năm prompt
sau đều có đủ nguyên văn ngay từ đầu.

**Chống trùng theo quyền sở hữu dữ kiện:**
- `travel_tickets` giữ giá, giờ và chính sách vé. Ngoại lệ là pilot #4 và #19
  ở `heritages`.
- 16 case mới của `heritages` không hỏi vé.
- `festivals` không hỏi lại dữ kiện Nam Giao, Xã Tắc, Huệ Nam đã có trong pilot.
- `foods` không hỏi file Bún bò thuộc heritage hay tổ nghề Vân Cù.
- `performing_arts` không hỏi giá vé hay năm xây Duyệt Thị Đường.
- `travel_places` không hỏi vé, lịch sử Hải Vân Quan, lăng, Đại Nội hay Thiên
  Mụ.

Sau khi đọc lại, tôi xác nhận không có dữ kiện nào bị hỏi ở hai partition.
Một số thực thể xuất hiện ở hai partition nhưng hỏi dữ kiện khác nhau: Bạch Mã,
Duyệt Thị Đường, sân bay Phú Bài, Đàn Nam Giao, Điện Huệ Nam.

## 6. Review của Implementer: case đã sửa hoặc xóa

Tôi đọc 180/180 case và in đoạn nguồn quanh từng keyword để đối chiếu. Với
case liệt kê ("những quán/địa điểm nào"), tôi tìm text trên toàn corpus để
chắc đáp án đủ. Trước khi sửa file nào, tôi đều sao lưu file đó vào `/tmp`.

| Partition | Thao tác | Lý do (mô tả dạng) |
|---|---|---|
| travel_services | Sửa câu hỏi 1 case | Câu hỏi để lộ con số đáp án |
| performing_arts | Xóa 1 case | Câu đánh đố về danh tính một người, không phải câu du khách tự nhiên (spec §6.3) |
| performing_arts | Viết lại 1 case `comparative` | Câu cũ dựa vào tên một công trình mà corpus ghi hai cách (K33). Câu mới so hai con số đã thống nhất trong một file |
| travel_places | Cắt gọn đáp án 1 case `multi_source` | Đáp án thừa ý (P1) |
| travel_places | Viết lại đáp án và keyword 1 case `conditional` | Bỏ vế phương án thay thế vì corpus mâu thuẫn (K48). Bỏ keyword là chuỗi con của tên một thực thể khác |
| foods, festivals, heritages, travel_tickets | Không sửa | Đối chiếu đúng nguồn |

Các sub-agent tự loại hoặc sửa thêm nhiều bản nháp trước khi bàn giao. Lý do:
dữ kiện mâu thuẫn, sai nhãn `multi_source`, câu lời khuyên, đáp án liệt kê có
thể chưa đủ, keyword là chuỗi con, đáp án thừa ý.

## 7. Out-of-scope search ledger

Tìm casefold trên đủ 205 file qua `load_corpus()`. Tên thật nằm trong file
authoring private.

| Partition | Case | Dạng term | Số file khớp |
|---|---:|---|---|
| foods | 3 | 2 chuỗi đồ uống/ăn nhanh quốc tế; 1 quán ăn địa phương | 0 / 0 / 0 (biến thể chính tả cũng 0) |
| heritages (mới) | 2 | 1 di tích Hà Nội; 1 di sản tỉnh khác | tên đầy đủ: 0 / 0; tên rút gọn khớp 3 file mỗi term ở ngữ cảnh khác |
| festivals | 2 | 1 lễ hội thành phố lân cận; 1 lễ hội miền Bắc | 0 / 0; tên tỉnh/thành có trong 2–24 file, chỉ nói địa lý |
| performing_arts | 2 | 1 show diễn ở đô thị khác; 1 nhà hát thủ đô | 0 / 0 |
| travel_places | 3 | 1 bãi biển Huế vắng trong corpus; 1 hang động tỉnh khác; 1 bãi biển tỉnh lân cận | 0 / 0 / 0 |
| travel_services | 2 | giá vé tàu liên tỉnh; giá taxi từ sân bay | thực thể có trong corpus; tìm theo cặp thực thể + giá: 0 dòng |
| travel_tickets | 2 | vé 2 điểm du lịch ở thành phố lân cận | 0 / 0 |

2 case `out_of_scope` của pilot giữ nguyên ledger ở report GATE P.

## 8. Mâu thuẫn corpus mới (K11–K50)

Đã append vào `knowledge-base-hue/meta/corpus-contradictions-2026-10-23.md`,
mỗi mục có file:dòng của cả hai bên. Tôi kiểm lại từng dòng bằng tìm text.

| Partition phát hiện | Mục | Nhóm chủ đề |
|---|---|---|
| foods | K11–K15 | phường của một trung tâm thương mại; tên gọi khác của một món bánh; kiểu bánh theo vùng; giá trị kép giờ/giá/số nhà trong cùng file; giờ một quán |
| travel_tickets | K16–K22 | ngày miễn vé Tết; ngoại lệ hoàn vé; đối tượng học sinh/sinh viên; thời hạn vé combo; mức tiết kiệm vé toàn tuyến; giá vé Ca Huế; giá xe trung chuyển |
| travel_services | K23–K24 | thời điểm sạt lở một tuyến đường; địa danh một khu suối khoáng |
| performing_arts | K25–K33 | thuyền neo hay chạy khi diễn; suất diễn thứ ba; số quyết định và số nhạc cụ; thời gian đến sớm; ngày các đêm dạ yến; mùa tổ chức một tuần lễ âm nhạc; đội hình một đêm diễn; ngày một tuần lễ festival; tên một công trình |
| festivals | K34–K38 | mùa tái hiện một lễ; vua có trực tiếp chủ tế không; giờ quy đổi canh tư; phường của một điện thờ; 4 lệch nhỏ |
| travel_places | K39–K50 | ngày một nghị quyết; năm học (gần K4); quyết định bảo vật quốc gia; địa giới cũ; hướng/cự ly hai bãi biển; diện tích một đầm; quan hệ hai đầm; thời gian ủ mắm; cự ly; xe máy qua hầm; mùa leo núi trong cùng file; chiều dài một con đèo |

Golden không dùng dữ kiện nào thuộc K1–K50. Ngoại lệ có chủ đích: một case so
sánh dùng khoảng diện tích ở K44, vì kết luận đúng với cả hai con số.

Theo quyết định A của User, Phase 7A không sửa corpus.

## 9. Lỗi và giới hạn

- Script §9 chỉ kiểm cấu trúc và luật keyword. Độ đúng nội dung do tôi tự đối
  chiếu; Reviewer cần đối chiếu độc lập.
- `multi_source` = 29, sát biên dưới (28). `out_of_scope` = 18, chạm biên trên.
- Một số case `multi_source` lấy đáp án từ ≥2 đoạn của cùng một file. Spec §4
  cho phép điều này, nhưng tính "đa nguồn" yếu hơn. Một case `multi_source` ở
  `travel_services` ghép hai dữ kiện cùng một file và khá dễ đoán.
- Một case `conditional` về chu kỳ lễ hội cần suy luận năm âm lịch từ chu kỳ và
  các năm ví dụ trong file. File không ghi thẳng năm được hỏi.
- Một case `conditional` về vé trẻ em ở một lăng: bảng giá và
  `heritage-guides.md` thống nhất, nhưng `Hướng dẫn mua và sử dụng vé…:120` có
  một câu về tỷ lệ cho "lăng lớn" có thể đọc theo hai cách. Tôi giữ case và
  ghi limitation.
- Một case `foods` hỏi nguồn gốc một món bánh. File `travel/places` của một bãi
  biển khác gọi món này là "thương hiệu" của vùng đó, nhưng không nói đó là
  nguồn gốc. Tôi không coi là mâu thuẫn.
- Hai case khác partition có dữ kiện gần nhau:
  - Chi phí ăn uống/ngày (`foods`) và tổng chi phí chuyến đi (`travel_services`)
    là hai dữ kiện khác nhau.
  - Nhưng bảng ăn uống ở `Chi phí du lịch Huế.md` cho khoảng khác với
    `food-guides.md`, nên retrieval có thể trả về nguồn lệch.
- Keyword proxy có nhiễu: vài keyword đáp án dạng ngày/năm hoặc tên phường khớp
  nhiều file. Các case này đã kèm tên thực thể trong `keywords`.
- Dữ liệu giá/giờ ghi mốc tham khảo tháng 09/2026 nên có thể lỗi thời.
- Golden do LLM viết rồi Implementer review, không phải câu hỏi người dùng thật
  (spec §8).

## 10. Handoff cho Reviewer (GATE R)

- **Đọc trước:** report này, sau đó 7 file authoring private và mục K11–K50.
- **Chạy lại:**
  - `git status` và `git diff --check`;
  - `check --authoring` cho 7 file;
  - đối chiếu độc lập các case với `sources` (toàn bộ hoặc mẫu);
  - tìm text cho 18 case `out_of_scope`;
  - kiểm chéo partition xem có trùng dữ kiện không.
- **Cần quyết định:**
  - chấp nhận `multi_source` = 29 hay yêu cầu bổ sung;
  - giữ hay bỏ các case nêu ở §9.
- **Chưa làm (đúng handoff):** `merge`, smoke, commit.

## 11. Correction GATE R

Theo correction handoff ngày 2026-10-23 và bảng "GATE R" trong
`knowledge-base-hue/evaluation/phase_7a_review_notes.md` (private). User đã
đồng ý xử lý cả 14 case và chấp nhận `multi_source` = 29.

Trước khi sửa, tôi sao lưu 7 file authoring và file mâu thuẫn vào
`/tmp/gate_r_backup/`. Mỗi case, trước khi sửa, được assert đúng chủ đề.

| Partition | # (đánh số trước sửa) | Xử lý | Đã làm |
|---|---:|---|---|
| foods | 16 | DROP | Xóa (hai nguồn lệch nhau về cùng dữ kiện) |
| foods | 19 | FIX | Câu hỏi đổi sang số nhiều cho khớp đáp án 2 quán |
| heritages | 30 | FIX | Nhãn `conditional` → `direct_fact`; nội dung giữ nguyên |
| festivals | 5 | FIX | Câu hỏi nói rõ danh hiệu nào; bỏ keyword là tên đã có trong câu hỏi |
| festivals | 16 | FIX | Keyword đáp án đổi sang chuỗi nguyên văn dài, có kèm tên thực thể; đáp án viết lại chứa đúng chuỗi đó |
| festivals | 18 | DROP | Xóa (K51) |
| festivals | 20 | FIX | Bỏ câu rào đón trong đáp án |
| festivals | 22 | FIX | Câu hỏi và đáp án dứt khoát (mở đầu "Không."); giữ nhãn `conditional` |
| performing_arts | 15 | FIX | Viết gọn thành câu so sánh có/không; không dùng ngày hay tên công trình thuộc K29, K33 |
| travel_places | 3 | DROP | Xóa (câu tin tức hành chính) |
| travel_places | 9 | DROP | Xóa (K52) |
| travel_places | 14 | FIX | Hỏi ngày thành lập thay vì số quyết định |
| travel_services | 8 | FIX | Đáp án dùng hai khoảng cách cụ thể. `sources` đổi sang 2 file `travel/places` chứa khoảng cách |
| travel_services | 10 | FIX | Nhãn `conditional` → `direct_fact` |
| travel_services | 11 | FIX | Đáp án nêu điều kiện cụ thể; `sources` thêm file vé biểu diễn |

Ghi chú `travel_services` #8:
- Hai file nguồn cũ không chứa con số khoảng cách. Tôi đã tìm text trong cả
  hai file. Vì vậy tôi thay hẳn `sources`, không chỉ thêm.
- Case vẫn ở partition `travel_services`.

**Phạm vi:** so với bản sao lưu, chỉ 15 dòng cũ không còn (4 xóa, 11 sửa).
Đúng danh sách GATE R; các case khác và `travel_tickets` không đổi.

**File mâu thuẫn:** đã append mục "Bổ sung GATE R":
- K51: chu kỳ Cầu ngư;
- K52: độ cao đỉnh đèo Hải Vân;
- K53: cự ly Huế – Lăng Cô/Hải Vân;
- ghi chú thêm cho K45.

Mỗi mục kèm file:dòng; tôi đã định vị lại từng dòng bằng tìm text.

**Chạy lại:**

| Partition | exit | Tổng | direct | multi | cond | comp | oos |
|---|---:|---:|---:|---:|---:|---:|---:|
| foods | 0 | 37 | 16 | 7 | 6 | 5 | 3 |
| heritages | 0 | 36 | 16 | 6 | 5 | 5 | 4 |
| festivals | 0 | 27 | 12 | 5 | 4 | 4 | 2 |
| performing_arts | 0 | 17 | 8 | 2 | 3 | 2 | 2 |
| travel_places | 0 | 32 | 12 | 6 | 6 | 5 | 3 |
| travel_services | 0 | 13 | 6 | 1 | 2 | 2 | 2 |
| travel_tickets | 0 | 14 | 5 | 2 | 3 | 2 | 2 |
| **Tổng** | | **176** | **75** | **29** | **29** | **25** | **18** |

- Không trùng câu hỏi giữa các file: 0 trùng, tổng 176.
- `git diff --check`: exit 0.
- So với dự kiến của Reviewer (direct ~74, cond ~29): `conditional` khớp.
  `direct_fact` = 75 đúng theo phép tính 76 − 3 (xóa) + 2 (đổi nhãn).

Limitation ở §9 về một case `conditional` chu kỳ lễ hội không còn: case đó đã
bị xóa (K51). Case so sánh dùng khoảng ở K44 vẫn giữ.

## 12. Task 5 — merge và smoke

Theo handoff Task 5 ngày 2026-10-23. User đã duyệt bộ smoke 10 câu.
- Không sửa file authoring, module, curated Markdown.
- Không gọi API, không dùng Git.

Trước khi merge, `knowledge-base-hue/evaluation/` chưa có file Golden chính
thức nào, nên merge chỉ tạo file mới, không ghi đè.

| Bước | Lệnh (từ `backend/`) | Kết quả quan sát |
|---|---|---|
| 1 | `HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus merge` | `category: {'direct_fact': 75, 'multi_source': 29, 'conditional': 29, 'comparative': 25, 'out_of_scope': 18}`, `total: 176`, exit 0 |
| 2 | `... smoke 3 24 42 44 55 82 114 141 155 163` | `smoke: 10`, exit 0 |
| 3 | Script so chuỗi từng dòng smoke với dòng tương ứng của file chính thức, và so đầu câu hỏi với bảng trong handoff | 10/10 khớp nguyên văn; 10/10 câu hỏi đúng bảng. File chính thức có đúng 4 field ở mọi dòng |
| 4 | `... check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (chế độ chính thức) | `total: 176`, distribution như bước 1, exit 0 |
| 4 | `... check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl` | `category: {'direct_fact': 3, 'conditional': 2, 'multi_source': 2, 'out_of_scope': 1, 'comparative': 2}`, `total: 10`, exit 0 |
| 5 | `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q` | `8 passed`, exit 0 |
| 5 | `git diff --check` | exit 0 |

**File tạo ra (private):** `git check-ignore` xác nhận hai file sau thuộc
`.gitignore:25` (`knowledge-base-hue/`):
- `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (176 dòng);
- `knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl` (10 dòng).

**Ghi chú:**
- Lệnh `check` kiểm keyword theo corpus tại thời điểm chạy. Nếu sau này có đợt
  sửa curated Markdown, cần chạy lại `check` cho file chính thức và file smoke.
- `git status` có thêm một thư mục untracked ở root mà tôi không tạo
  (`gửi chatgpt/`). Tôi không đọc và không đụng tới thư mục này.
