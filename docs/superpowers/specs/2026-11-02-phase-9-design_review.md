# Review: Phase 9 — spec thiết kế (bản 1)

Decision: **changes_requested**
Người kiểm: session review độc lập (sub-agent Claude Opus 5.5, không phải người viết C)
Date: 10:09 02/11/2026 (`date`)
Canonical guide: `docs/superpowers/specs/2026-11-02-phase-9-design.md` — sha256 12 ký tự đã review **`e5be02400646`** (tính lại khớp)
Implementation report: không có (việc tài liệu); căn cứ là mục "Căn cứ để review" của spec

## 1. Phạm vi đã review

Chỉ dựa trên spec + 4 nguồn trong "Căn cứ để review":
- [Đọc] `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` §1, §3, §6.
- [Đọc] `session_prompt/CURRENT_HANDOFF.md` mục "Brainstorm Phase 9", mục "C118" (bản trong worktree, có sửa chưa commit).
- [Đọc] `report_agent/2026-10-31_streaming_spec/q3a_theo_loai_cau_implementation.md` §4 (và §5 giới hạn cỡ mẫu).
- [Đọc] code `main` `411bbc5` qua `git show HEAD:`: `backend/llm/grounded_answer.py`, `backend/llm/full_corpus_prompt.py`, `backend/api/routes/chat.py` (1–80),
  `backend/config/settings.yaml` (40–62); thêm `generator_openai_full_corpus.py` và `retrieval/full_corpus_context.py` chỉ bằng `git grep` để kiểm câu "nơi dựng duy nhất".
- [Chạy] đếm lại chỉ in số trên Golden, bộ an toàn, bộ ngày, kho (qua `scripts/grep_kb.sh`), sha T1, thứ trong tuần của các mốc ngày, quét trùng.

Không đọc: `STATUS_*.md`, tin nhắn / report khác của C, file `*sealed*`, `.env`. Không gọi API trả phí. Không sửa file nào ngoài file này.

## 2. Findings

Không có blocker. Có 4 major, 8 minor.

### M1 (major) — H4 bị diễn giải lại ở hai chỗ, không ghi thành chỗ lệch / câu hỏi

- **Vị trí:** spec §3 (Trong), §5.1, §5.2, §10.
- **Yêu cầu:** hướng User chọn (báo cáo nghiên cứu §1: "thông tin theo ngày **ghi rõ nguồn / ngày** + chặn câu an toàn trước mô hình"; §6 dòng 2: "Chặn câu an toàn + ghi
  'theo nguồn ngày…' cho giờ / giá / lễ hội"); C118: "không tự mở rộng / thu hẹp; chỗ lệch đề xuất A đều ghi lý do".
- **Bằng chứng:** spec chỉ có H4a = thêm "hôm nay là ngày nào" vào prompt cho câu có từ chỉ thời gian. Phần "ghi theo nguồn ngày… cho giờ / giá / lễ hội" (cho người dùng biết thông tin
  dễ đổi lấy từ nguồn ngày nào) không xuất hiện ở đâu trong spec, kể cả mục Ngoài. "Chặn câu an toàn trước model" được hiểu thành "câu **khẩn cấp**" (H4b); spec tự nói bộ an toàn 32 câu
  là câu điều kiện, nhưng không nói vì sao "câu an toàn" của User = câu khẩn cấp, và Q2 chỉ hỏi "thử trước hay làm luôn", không hỏi cách hiểu.
- **Tác động:** User duyệt một lần có thể tưởng đã có phần "ghi nguồn ngày", hoặc tưởng câu an toàn điều kiện (loại lỗi nặng nhất) sẽ được chặn trước model. Thu hẹp phạm vi không khai.
- **Tiêu chí đóng:** spec hoặc (a) thêm phần "ghi theo nguồn ngày" (có bộ đo + tiêu chí như các phần khác), hoặc (b) đưa nó vào mục Ngoài kèm lý do; và thêm một câu hỏi cho User
  (phương án + hệ quả + khi nào sai) về cả hai điểm: có làm "ghi nguồn ngày" không; "chặn câu an toàn" nghĩa là câu khẩn cấp hay cả câu điều kiện.

### M2 (major) — Câu hai ý mà kho chỉ có một ý bị bỏ khỏi phạm vi mà không khai

- **Vị trí:** spec §5.6 (dòng "thử TRIPO câu 2 … cùng gốc" và danh sách "Đã thử và bỏ").
- **Yêu cầu:** báo cáo nghiên cứu §6 dòng cuối: "Thêm vào danh sách thử: câu hỏi 2 ý bị từ chối cả câu khi kho chỉ có một ý … cách xử lý phải khác lần thử 'trả lời một phần'";
  Brainstorm: "kho có giá vé …, thiếu giờ? ⇒ xét 'trả lời phần có' cách khác R2".
- **Bằng chứng:** spec gộp câu 2 vào "một vế thiếu bằng chứng ở tầng tìm" và để R2 trong "đã thử và bỏ". Nếu một vế **không có trong kho** (Brainstorm còn để ngỏ "thiếu giờ?") thì
  tách câu để tìm không giúp: lời dặn `full_corpus_prompt.py:14-15` vẫn bắt trả câu từ chối cho cả câu khi bằng chứng không đủ. Spec không nói đã kiểm vế giờ có trong kho hay không.
- **Tác động:** một mục User / A đã ghi "thêm vào danh sách thử" biến mất lặng lẽ; H1 bậc 1 có thể "dương" mà câu loại này vẫn bị từ chối.
- **Tiêu chí đóng:** spec ghi rõ một trong hai: (a) câu hai ý mà kho thiếu một ý là phần riêng (hoặc biến thể của H1) có tiêu chí giữ S-OOS; hoặc (b) để Ngoài kèm lý do + thành câu hỏi
  cho User. Ghi rõ vế nào của câu thử TRIPO 2 có / không có trong kho (đếm bằng `grep_kb.sh`, chỉ in số).

### M3 (major) — Sàn an toàn S-AT và S-G không rõ mốc, cộng dồn và cách xử nhiễu

- **Vị trí:** spec §4 (S-AT, S-G), §9 dòng 2.
- **Yêu cầu:** brief việc review mục 3 (sàn đo được bằng số, không mơ hồ); thứ tự lỗi: sai cảnh báo / điều kiện là lỗi nặng nhất (spec §2).
- **Bằng chứng:** "câu sai điều kiện **mới** ≤ 2. Mốc 01/11 là 2 … làm số này lên 3 thì dừng". [Chạy] đếm số trong `data/do_cuoi_2026-11-01/an_toan/compare_main.json`: số "2" là số
  câu sai mới của lượt cuối **so với một mốc trước đó** (2 ca cần phân loại). Spec không nói Phase 9 đếm "mới" so với commit nào: so với `main` hôm nay thì số bắt đầu từ 0 (và mỗi phần được
  thêm 2 ⇒ 5 phần có thể cộng dồn tới 10); đếm tuyệt đối thì đã ở ngưỡng, một lần sinh nhiễu là dừng phần. Không nói sinh lại mấy lần khi có ca sai mới (lượt cuối 01/11 có sinh lại 3 lần).
  S-G "số câu tụt ≤ 5" cũng không nói tụt theo thước nào, so với mốc nào, có cộng dồn qua các phần không; định nghĩa nằm ở file ngoài Căn cứ.
- **Tác động:** sàn của loại lỗi tệ nhất có thể vừa quá lỏng (cộng dồn) vừa quá chặt (nhiễu) — người đo sẽ phải tự chọn cách đếm sau khi thấy số, trái luật "ghi trước".
- **Tiêu chí đóng:** với S-AT và S-G ghi: mốc = commit / lượt nào; đếm theo phần hay cộng dồn so với mốc đầu Phase (khuyên: cộng dồn so với `main` đầu Phase 9); thước "tụt" của S-G;
  ca sai mới thì sinh lại K lần và luật quyết theo K đó.

### M4 (major) — Chỉ số quyết các phần chưa nói đo trên phần nào; H1 bậc 1 thiếu mức tụt cho câu bị tách nhầm

- **Vị trí:** §4 "Bộ đo mỗi phần", §5.1, §5.3, §5.5, §5.6 bậc 1.
- **Yêu cầu:** tiêu chí ghi trước đo được bằng số, không mơ hồ (`run-experiment`; brief mục 3).
- **Bằng chứng:**
  - Mọi phần chia "đã thấy / kín", nhưng không phần nào nói chỉ số quyết tính trên tập nào và phần kín phải qua ngưỡng nào (vd H2 "≥ 12 / 15" trong khi 15 câu thiếu trường trải trên cả
    ~20 đã thấy và ~10 kín; L "5 cặp" lấy từ đâu). Luật chữ được chỉnh trên phần đã thấy ⇒ số trên phần đó lạc quan.
  - H4a "giảm ≥ 3 câu, sinh 2 lượt mỗi bên": không nói một câu tính "từ chối" thế nào qua 2 lượt (cả 2 / một trong 2 / cộng). Bộ ngày có câu cũ + ~15 câu mới; mốc 5 chỉ đo trên 12 câu cũ
    ([Chạy] `ngay/ket_qua.json`: 15 dòng, 12 câu quyết, 5 từ chối nhầm, 0 lỗi đoán ngày — khớp spec) — ngưỡng "≥ 3" tính trên bộ nào chưa rõ.
  - H1 bậc 1: "thêm ≥ 3 câu đủ bằng chứng" không nói thước nào ("đủ keyword top-10" hay "đủ đoạn đúng" — Q3a §4 có cả hai, 12 / 18 và 8 / 16) và tính trên dev, test hay cả 18.
    Không có mức tụt cho câu **không phải nhiều nguồn** mà luật tách vẫn bắt (S-T1 chỉ bảo vệ câu luật không bắt). [Chạy] chỉ để thấy cỡ rủi ro: 42 / 176 câu Golden có chữ "và"
    (luật tách theo liên từ có thể chạm nhiều câu một dữ kiện / có điều kiện); "0 câu mất đoạn đúng" chỉ xét câu nhiều nguồn.
- **Tác động:** H1 bậc 1 chạy ngay tuần này (nếu User chọn Q1a) mà luật giữ / gỡ còn chỗ để chọn sau khi thấy số; các phần sau tương tự.
- **Tiêu chí đóng:** §4 thêm một câu chung: chỉ số quyết tính trên tập nào, phần kín phải đạt gì (vd không ngược chiều / đạt ngưỡng tỉ lệ). H4a ghi cách gộp 2 lượt và bộ tính ngưỡng.
  H1 bậc 1 ghi thước quyết, tập quyết, và thêm: số câu Golden bị luật tách bắt ngoài nhóm nhiều nguồn / so sánh + mức tụt "0 câu mất đủ bằng chứng" trên mọi câu bị bắt.

### m1 (minor) — Nhiều số quyết định nằm ở file ngoài "Căn cứ để review"

- Mốc H4a (`do_cuoi_b_an_toan_ngay.md` §4), sàn tốc độ / tiền (`Project_Status.md` §1), mốc S-AT / S-G, B119 §2–§3, báo cáo §4 / §5 (CLAMBER, Luật 91/2025, Royal Armouries), C102.
- Người kiểm đếm lại được từ dữ liệu: Golden 176, bộ an toàn 32 (chia nhóm 5 / 6 / 5 / 4 / 4 / 4 / khác 4 khớp), 4 câu ngoài kho, bộ ngày 15 / 12 / 5 / 0, sha T1 `4d5bbe9e0edc` (khớp).
  Không kiểm được: p50 / p95, 0,00025 USD / câu, định nghĩa "tụt" của S-G.
- **Tiêu chí đóng:** thêm 1 dòng Căn cứ (vd `do_cuoi_b_an_toan_ngay.md` §4 + `Project_Status.md` §1) hoặc ghi các số này là "dẫn, chưa nằm trong căn cứ".

### m2 (minor) — Đếm "chỉ in số" không ghi mẫu nên không lặp lại được đúng

- Luật thời gian: với đúng 5 từ ví dụ trong spec §5.1, [Chạy] ra **0 / 176** Golden và **1 / 32** bộ an toàn; phải thêm từ (vd "ngày mai", "hiện nay"…) mới ra 1 / 176 và 2 / 32 như spec.
- Kho: khớp với mẫu hợp lý — places 36, heritages 29, tọa độ 24, giờ mở cửa 25, km 32, "âm lịch" 37, khẩn cấp 15 (mẫu có ghi). Lệch theo mẫu: "giá vé" spec 30 ↔ 20–24;
  "thời lượng" spec 16 ↔ 10–20 tuỳ mẫu (chỗ quyết khả thi của L).
- **Tiêu chí đóng:** ghi mẫu (regex) cạnh mỗi số đếm; luật thời gian ghi danh sách từ đầy đủ dùng để đếm.

### m3 (minor) — Câu "grep date|today … = 0 dòng" sai nghĩa đen; đường ngày phải đi qua hai chỗ gọi

- [Chạy] `git grep -i -E 'date|today'` trên `backend/llm` + `backend/api/routes` ra 15 dòng (update / validate, và `datetime` ở `phase6_live_smoke.py:4,196`). Đường trả lời đúng là không có
  ngày (`full_corpus_prompt.py:7-20` khớp).
- `build_answer_input` là nơi dựng duy nhất (khớp `full_corpus_prompt.py:18-20`), nhưng nó được gọi từ hai đường: đếm token (`retrieval/full_corpus_context.py:41` qua
  `build_answer_messages`) và gửi đi (`generator_openai_full_corpus.py:252, 261`). Ngày phải truyền cùng một giá trị cho cả hai.
- **Tiêu chí đóng:** sửa câu thành "0 dòng trong đường trả lời"; ghi ý truyền ngày cho cả hai chỗ gọi vào phần H4a (hoặc để plan, ghi "chốt lúc tới lượt").

### m4 (minor) — S-T1 "chuỗi gửi model giống byte" chưa có mốc / công cụ

- T1 chỉ phủ 158 câu Golden trong kho (kết quả tìm). Chưa có dấu vân tay cho chuỗi gửi model, và bộ an toàn / bộ ngày không nằm trong T1.
- **Tiêu chí đóng:** ghi: trước phần đầu tiên, ghi mốc 0 USD trên `main` (sha của `build_answer_input` cho Golden + bộ an toàn + bộ ngày, không gọi model), mỗi phần so với mốc đó.

### m5 (minor) — Lịch và luật cắt có chỗ vênh

- Luật cắt 3 (14/12 còn phần chưa đóng ⇒ dừng) đè lên ô H1 bậc 2 12–19/12 ⇒ bậc 2 thực chất chỉ có 12–14/12.
- [Chạy] 29/11 là Chủ nhật, 04/12 là thứ Sáu, trong khi "A kiểm mỗi thứ Hai".
- §9 nói "giao diện trễ ⇒ luật cắt §6" nhưng §6 không có luật cho giao diện trễ. H2 đếm hỏi lại bằng code nên phần server đo được không cần giao diện; chỉ phần hiện nút cần.
- Bảng điểm L (dữ liệu, không chạm `chat.py`) có thể soạn song song sớm hơn 30/11, giảm rủi ro luật cắt 2.
- **Tiêu chí đóng:** sửa luật 3 cho khớp ô H1 bậc 2; ghi ngày kiểm cho các luật; thêm luật giao diện trễ (hoặc ghi H2 làm server trước); cân nhắc dời việc soạn bảng điểm lên sớm.

### m6 (minor) — L còn ba chỗ để trống

- Bảng điểm đặt ở "`knowledge-base-hue/` hoặc `data/`": nếu đặt trong kho dạng file được nạp, lần nạp lại sẽ đổi Qdrant / T1 (trái §8 "không ghi Qdrant").
- Ô thời lượng để trống (thiếu ở ≥ nửa số điểm) thì code xếp số điểm / ngày theo luật nào chưa nói.
- Sàn "S-OOS cho yêu cầu ngoài Huế" nhưng thành phần bộ đo L không có yêu cầu ngoài Huế.
- **Tiêu chí đóng:** chốt chỗ đặt bảng (khuyên `data/` hoặc đường không bị nạp); ghi "ô trống ⇒ …"; thêm vài yêu cầu ngoài Huế vào bộ đo L.

### m7 (minor) — H2 và H3 có tiêu chí khó đo đúng

- H3 "bắt nhầm câu đủ ý ≤ 2 / 208": 208 câu Golden + an toàn là câu một lượt, không có lịch sử ⇒ nhánh hỏi tiếp không thể bật; phép đếm này luôn ra 0 trừ khi ghép một lượt trước.
- H2: câu ghép sau khi chọn nút đi đường thường nhưng chỉ có "theo dõi", không có mức tụt (vd Accuracy không thấp hơn mốc) — chỗ có thể nói sai giá.
- **Tiêu chí đóng:** H3 ghi cách dựng lượt trước cho phép đếm bắt nhầm; H2 thêm một mức tụt bằng số cho lượt sau khi chọn.

### m8 (minor) — Mức công và câu hỏi cho User

- 6 phần × (review plan + review nhánh) + bộ kín riêng + User đọc mẫu mỗi phần trong ~7 tuần. Với phần rất nhỏ (H4a thêm một dòng, H4b nếu làm), một lượt review nhánh và dùng lại bộ ngày sẵn
  có + vài câu kín có thể đủ. Ghi như đề xuất cho A / User, không bắt buộc.
- Q5 gộp hai quyết định (duyệt spec + trần tiền) và không có phương án / khi nào sai. Q1 "khi nào sai" yếu: rủi ro thật là bậc 1 dương nhưng bậc 2 bị luật cắt 1 ⇒ công tuần 1 không vào chatbot.
  Thiếu câu hỏi cho M1, M2, chỗ đặt bảng điểm L.
- **Tiêu chí đóng:** tách Q5; sửa "khi nào sai" của Q1; thêm câu hỏi theo M1 / M2 (mỗi lần một câu, có phương án tick được).

**Phần ổn (không finding):** phạm vi Ngoài khớp Brainstorm (không agent, không đặt chỗ / giọng nói / ảnh / nhiều ngôn ngữ); lịch trình không giờ / giá chính xác; ba chỗ lệch A (H1 lên tuần 1, H4b
có bước 0, H3 mang đoạn 1 lượt + 3 câu hỏi) đều có lý do và thành Q1 / Q2 / Q4; số H1 khớp Q3a §4 (18 câu, Đủ 3,50 ↔ 4,92, MRR 0,510, 8 câu yếu đều thiếu bằng chứng, 5 / 8 từ chối nhầm,
8 / 12 trên 158 câu); danh sách "đã thử và bỏ" đủ 6 mục như Q3a §4; biến thể H1 không thêm lần gọi model (khớp cảnh báo của Q3a §4 về sàn tốc độ). Mọi `file:dòng` code đã kiểm khớp:
`grounded_answer.py:44-99`, `:51`; `full_corpus_prompt.py:7-20`, `:9-10`, `:18-20`; `chat.py:35-40`, `:35-36`, `:51-53`; `settings.yaml:53` (16384), `:56` (10). "Mặc định = hành vi
hôm nay" làm được: `prepare_answer` / `answer_query` nhận thêm tham số từ khoá có mặc định. Tiền: các ước cộng đúng 0,24 USD, khớp 0,00025 USD / lần sinh (H4a 200 × 0,00025 = 0,05).
Bảo mật từng phần hợp lý: ngày từ server; trường H2 theo danh sách cho phép + `extra="forbid"`; H3 không nhận chữ câu trả lời cũ, mã đoạn là UUID, server tự đọc; L không thêm đường ra; log không chữ.

## 3. Cách người kiểm chạy lại thật

- `sha256sum docs/superpowers/specs/2026-11-02-phase-9-design.md | cut -c1-12` ⇒ `e5be02400646` (đầu và cuối review).
- `git show HEAD:<file>` cho 4 file code; `git grep -i -E 'date|today'`, `git grep build_answer_input` trên `HEAD`.
- `uv run python` (đọc JSONL, chỉ in số): số dòng Golden / bộ an toàn, đếm nhóm, đếm luật thời gian (2 danh sách từ), đếm chữ "và"; tóm tắt số trong `ngay/ket_qua.json` và
  `an_toan/compare_main.json`.
- `sha256sum` các file T1 trong `data/`.
- `scripts/grep_kb.sh -l …` đếm file (kho chung, `--dir travel/places`), chỉ đếm dòng ra.
- `date -d …` cho thứ của 02/11, 29/11, 04/12, 14/12, 20/12.
- `uv run python .githooks/overlap_scan.py docs/superpowers/specs/2026-11-02-phase-9-design.md`.

## 4. Kết quả quan sát

- Quét trùng spec: **0 trùng** với Golden / kho / câu kín. Không thấy chi tiết dự án khác. Không có khoảng trắng cuối dòng.
- Số khớp: xem "Phần ổn" và m1, m2. Số lệch / không lặp lại được: m2, m3.
- 02/11/2026 là thứ Hai, 20/12/2026 là Chủ nhật (khớp spec).
- Docs-only: không chạy chatbot, không gọi model; 0 USD.

## 5. Giới hạn hoặc phần chưa chạy

- NOT RUN: kiểm sàn tốc độ / tiền / câu (nguồn `Project_Status.md` ngoài Căn cứ); định nghĩa "tụt" của S-G; nội dung B119, C102, báo cáo §4 / §5 — theo luật review chỉ dựa trên Căn cứ.
- Không đọc nội dung câu nào khi đếm (chỉ in số), nên "câu khớp luật thời gian có thật là câu chỉ thời gian không" và "câu có 'và' có bị luật tách bắt không" chưa xác định — số ở M4 / m2 chỉ là cỡ rủi ro.
- `CURRENT_HANDOFF.md` đọc bản worktree (có sửa chưa commit), không phải bản `HEAD`.

## 6. Decision và bước tiếp theo

**changes_requested.** C sửa trong một lượt M1–M4 (bắt buộc) và các minor (nên làm, không mở vòng riêng), rồi gửi sha mới. Người kiểm kiểm lại chỉ phần đổi + câu hỏi mới ở §10.
Ranh giới giữ nguyên: phạm vi Ngoài, ba chỗ lệch A đã có câu hỏi, số H1, trần tiền. Đây là vòng 1.

---

# Vòng 2 — kiểm phần sửa (bản 2)

Decision vòng 2: **changes_requested** (còn 1 major về mức công; phần sửa nhỏ, vòng 3 chỉ cần kiểm hẹp)
Date: 10:22 02/11/2026 (`date`)
Sha đã review: **`d819918c2f2e`** (557 dòng; tính lại khớp)
Căn cứ: 5 dòng của bản 2 — thêm [Đọc] `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` §3.1, §3.2. Đọc cả spec bản 2 và bảng "Trả lời review vòng 1".

## V2.1 Finding vòng 1 — đóng / chưa

| Finding | Kết quả | Bằng chứng |
|---|---|---|
| M1 | **đóng** | §2 ghi 3 dòng "cách hiểu (C), chờ User"; H4c (§5.3) có bộ đo + tiêu chí; Q2 thêm (c) câu điều kiện, Q3 có (a) / (b) / (c). Chuyển "ngày" thành "năm" có lý do bằng số: [Chạy] ngày đủ cạnh "truy cập / cập nhật" = 2 file `travel/tickets` (thư mục có 6 file `.md`), 0 ở places / festivals / heritages — khớp spec. |
| M2 | **đóng** (nhưng xem V2.3 N1) | H1b §5.8 + Q4; ghi rõ khác R2; danh sách "đã thử và bỏ" tách riêng. |
| M3 | **đóng** | Mốc chung = `main` đầu Phase 9; [Chạy] `git log a80e12d..HEAD -- backend` = 0 commit ⇒ "chưa đổi code từ đó" đúng. Cộng dồn ≤ 2 cả Phase; sinh lại 3 lần, luật ≥ 2 / 3 ↔ ≤ 1 / 3. [Chạy] `compare_regen.json`: hai câu dao động, mỗi bên sai 1 / 3 — khớp. S-G dùng mức tụt plan §3.1 (≥ −0,1; ≤ A/A + 3 = 5; ≤ 13 / 158) — khớp plan. Còn một chỗ nhỏ: N3. |
| M4 | **đóng** | §4 luật "chỉnh trên đã thấy, sàn cả hai, kín không ngược chiều", gộp nhiều lượt 0 / 0,5 / 1; H4a quyết trên 12 câu cũ; H2 tách ngưỡng 8 / 10 + 4 / 5; L 5 cặp lấy từ kín; H1 bậc 1 có thước, tập dev / test, sàn trên mọi câu bị bắt. [Chạy] `split.json`: dev nhiều nguồn 20 + so sánh 17, test 9 + 8 — khớp. |
| m1 | đóng | dòng Căn cứ thứ 5 + mục "Số dẫn, ngoài căn cứ". |
| m2 | đóng (một số lệch, N2) | [Chạy] đúng 16 từ của §4 ⇒ **1 / 176** và **2 / 32** — khớp. Places: tọa độ 24, giờ mở cửa 25, km 32, thời lượng 16; "giá vé \| vé tham quan" 30 — khớp đúng mẫu ghi. |
| m3 | đóng | §5.1 ghi đường trả lời + hai chỗ gọi. |
| m4 | đóng | "bước 0 chung" ghi dấu vân tay `build_answer_input`, 0 USD. |
| m5 | đóng | [Chạy] 16/11, 23/11, 30/11, 07/12, 14/12 đều là thứ Hai; 18/12 thứ Sáu; H1 bậc 2 14–18/12 khớp luật 5; có luật giao diện trễ. Còn N4 (song song). |
| m6 | đóng | bảng ở `data/phase_9/lich_trinh/`; `null` ⇒ "nửa buổi"; thêm 3 yêu cầu ngoài Huế. |
| m7 | đóng | H3 ghép lượt trước theo seed; H2 có mức tụt Accuracy + 0 "nói chắc sai" mới. |
| m8 | đóng phần đã nêu | Q1 "khi nào sai" đã sửa; Q5 cũ đã tách. Mức công mở lại ở N1 / N5 với bằng chứng mới (file 351 ⇒ 557 dòng, 6 ⇒ 8 phần, 5 ⇒ 8 câu hỏi). |

Kiểm thêm: `chat.py:56-60` (`SourceResponse`) khớp; tiền cộng đúng 0,24 USD. Quét trùng bản 2: **0 trùng**; không có khoảng trắng cuối dòng.

## V2.2 Cách chạy (vòng 2)

`sha256sum`; `git log a80e12d..HEAD -- backend`; `uv run python` chỉ in số (luật 16 từ trên Golden / bộ an toàn; nhóm dev / test trong `split.json`; tóm tắt `compare_regen.json`);
`scripts/grep_kb.sh` đếm file (`^## Nguồn` kèm `-A15`, mẫu năm, ngày cạnh "truy cập / cập nhật", các mẫu places, "giá vé"); `date -d` cho các mốc; `overlap_scan.py` trên spec.

## V2.3 Finding vòng 2

### N1 (major) — H1b là việc phòng xa, mà spec lại khuyên làm

- **Vị trí:** §5.8, §6 (tuần 30/11–11/12), §10 Q4 (a) "C khuyên".
- **Yêu cầu:** mức công tương xứng; chính spec dùng luật "phòng xa ⇒ bước 0 trước" (`Session_Prompt.md` §7) cho H4b.
- **Bằng chứng:** chính đếm của H1b cho thấy câu thử TRIPO 2 **có cả hai vế trong kho** ("có lẽ là lỗi tầng tìm (H1), không phải kho thiếu"). Ngoài câu đó, spec không đưa ra câu nào quan sát
  được mà kho thật sự thiếu một vế. Vậy H1b chưa có lỗi quan sát được, nhưng vẫn được khuyên làm: 20 câu mới + phần kín + đổi lời dặn (chạm S-AT / S-OOS, hai sàn nặng nhất) + ~3 ngày,
  đặt vào đúng cửa sổ chật nhất (cùng tuần với L). Số phần tăng từ 6 lên 8.
- **Tác động:** phình việc ở giai đoạn trễ; User khó tự giải thích vì sao làm một phần không có lỗi đã thấy; đổi lời dặn tạo rủi ro cho loại lỗi tệ nhất.
- **Tiêu chí đóng:** áp cùng luật như H4b. Q4 khuyên **"bước 0 trước"**: từ kết quả H1 bậc 1 (0 USD, đã có), đếm câu nhiều nguồn / so sánh mà một vế **không có keyword nào trong kho**
  (`grep_kb.sh`, chỉ in số). < 3 câu ⇒ ghi giới hạn, không làm. ≥ 3 câu ⇒ mở plan H1b. §5.8 rút về vài dòng, chi tiết bộ đo để plan lúc tới lượt.

### N2 (minor) — Số "130 / 143 file có năm" không khớp mẫu ghi; chưa nói chọn năm nào

- [Chạy] `^## Nguồn` = 143 file (khớp). Năm theo đúng mẫu ghi `20(2[3-6])` trong 15 dòng sau tiêu đề ⇒ **119 / 143**. Ra 130 khi dùng mẫu `20[0-9]{2}` (mọi năm 20xx) ⇒ 11 file chỉ có năm cũ hơn 2023.
- Mục Nguồn có nhiều năm thì thẻ hiện năm nào (mới nhất? đầu tiên?) chưa ghi.
- **Tiêu chí đóng:** sửa số hoặc mẫu cho khớp nhau; ghi một câu luật chọn năm (khuyên: năm lớn nhất; file chỉ có năm < 2023 vẫn hiện, vì đó chính là thông tin "nguồn cũ").

### N3 (minor) — S-G chỉ liệt kê mức tụt, chưa nói các sàn F1–F4 của plan §3.1

- Plan §3.1 có sàn: 0 lỗi kỹ thuật, 0 lỗi trích dẫn (500) mới, 0 câu "nói chắc sai" mới (loại lỗi thứ 2 trong thứ tự lỗi). Spec ghi "thước của plan đo cuối §3.1 (dùng lại)" nhưng chỉ chép mức tụt
  ⇒ chưa rõ các sàn này có giữ không.
- **Tiêu chí đóng:** thêm một dòng "sàn F1–F4 của plan §3.1 giữ nguyên" (hoặc liệt kê ba sàn).

### N4 (minor) — Lịch còn hai tuần chạy song song hai phần cùng sửa đường trả lời

- Tuần 30/11–11/12: L (nhánh mới tới một lần gọi model) và H1b (đổi lời dặn + đường tìm) cùng chạm `grounded_answer.py` / prompt / `chat.py`. Câu "không chạm file của L" không chứng minh được;
  trái luật "không song song" ở cuối §6. Tuần 09–15/11: H4a (prompt) và H4c (`SourceResponse` trong `chat.py`) cũng vậy.
- **Tiêu chí đóng:** ghi hai phần trong cùng tuần chạy **lần lượt** (merge phần trước rồi mới mở nhánh phần sau); nếu N1 làm H1b ra khỏi Phase thì tuần 30/11 tự hết vênh.

### N5 (minor) — Mức công: vài cơ chế không cần cho quyết định; 8 câu hỏi gộp được còn 5

Phần đã thêm theo M3 / M4 (sinh lại 3 lần, gộp theo câu, kín không ngược chiều) là cần cho luật giữ / gỡ — **giữ**. Đề xuất cắt cụ thể:
- **H1 bậc 1 "> 20 câu ngoài nhóm ⇒ siết rồi đếm lại":** thừa. Chất lượng đã do sàn "0 câu mất bằng chứng trên mọi câu bị bắt" giữ, tốc độ đã do `search_ms` p95 ≤ 150 ms giữ; luật này còn
  không có điểm dừng (đếm lại vẫn > 20 thì sao). Hạ thành **theo dõi**: báo số câu bị bắt ngoài nhóm.
- **H4c "session khác đối chiếu 20 file chọn ngẫu nhiên (seed ghi trước)":** nặng so với một nhãn hiển thị 0 USD. Gộp vào review nhánh: người review mở 5 file, "0 năm sai trong 5".
- **Câu hỏi User 8 ⇒ 5.** Q7, Q8 là do vòng 1 (m8) của người kiểm yêu cầu tách Q5 cũ; nay thấy nên gộp lại cho gọn:
  - **Q7 bỏ.** C118 đã chốt "User duyệt một lần"; phương án (b) mở lại quy trình. Giữ một dòng cuối: "Duyệt sha này ⇒ A giao phần đầu".
  - **Q8 gộp** vào dòng duyệt đó: "trần 0,30 USD cho Phase (mặc định, trong luật ≤ 1 USD / phiên)" — A tự đặt mặc định được, User chỉ cần phản đối nếu muốn khác.
  - **Q1** là thứ tự nội bộ, 0 USD, không đổi chatbot ⇒ A tự quyết được, chỉ báo User một dòng (vẫn giữ lý do ở §6).
  - Còn lại cho User: Q2, Q3, Q4, Q5, Q6 — đều là hành vi sản phẩm.
- **Tiêu chí đóng:** áp ba chỗ cắt trên (hoặc phản biện bằng lý do cần cho một quyết định cụ thể).

## V2.4 Giới hạn vòng 2

- NOT RUN: đếm 36 dòng / 11 file và 11 dòng / 6 file của H1b — cần tên di tích trong câu thử TRIPO 2, câu này nằm ở `data/…/cau_thu.md` ngoài Căn cứ; không mở.
- NOT RUN: "Runtime đã đọc mọi file kho để kiểm hash" (H4c) — nguồn `Project_Status.md` §4, spec đã ghi là ngoài căn cứ.

## V2.5 Decision vòng 2

**changes_requested** — vòng 2 / 4. Bắt buộc: N1. Nên làm cùng lượt: N2–N5. Vòng 3 người kiểm chỉ kiểm §5.8, Q4, §10 (số câu hỏi), §6 tuần 09–15/11 và 30/11, S-G, H4c, H1 bậc 1.
Ranh giới giữ nguyên: mọi phần đã đóng ở V2.1, phạm vi Ngoài, số H1, tiền.

---

# Vòng 3 — kiểm phần sửa (bản 3)

Decision vòng 3: **changes_requested** (vòng 3 / 4 — một sửa nhỏ về số của H4c; các phần khác đạt)
Date: 10:33 02/11/2026 (`date`)
Sha đã review: **`7c67656f0ff8`** (507 dòng; tính lại khớp). Quét trùng bản 3: **0 trùng**.
Chỉ kiểm phần sửa N1–N5 + 5 câu hỏi; không mở finding ngoài phần sửa.

## V3.1 N1–N5

| Finding | Kết quả | Bằng chứng |
|---|---|---|
| N1 | **đóng** | §5.8 rút còn bước 0 (0 USD, < 3 câu ⇒ không làm); bỏ bộ 20 câu khỏi lịch mặc định; §3 ghi "chỉ nếu bước 0 thấy ≥ 3 câu"; Q3 khuyên bước 0. |
| N2 | **chưa đóng — nâng thành major (N2′), bằng chứng mới ở V3.2** | luật chọn năm đã ghi (năm lớn nhất) — phần này đạt; số đếm thì sai mục. |
| N3 | **đóng** | §4 S-G liệt kê đủ sàn F1–F4, khớp plan §3.1. |
| N4 | **đóng** | §6: H4a rồi H4c lần lượt; H1b chỉ ở 14–18/12, sau H1 bậc 2; luật "cùng tuần ⇒ lần lượt" ghi rõ, kể cả `frontend/`. |
| N5 | **đóng** | "> 20 ⇒ siết" thành theo dõi (§5.7, §9); H4c đối chiếu 5 file lúc review nhánh; câu hỏi 8 ⇒ 5; trần thành dòng "Duyệt" mặc định. [Đọc] không còn chỗ trỏ Q6–Q8 hay số câu hỏi cũ. Lưu ý cho A: dòng "A quyết" ở §2 do C ghi — A cần tự xác nhận khi trình. |

**5 câu hỏi:** Q1–Q5 mỗi câu có 2–3 phương án tick được, có được / mất, phương án khuyên có "khi nào sai", có câu tự kiểm. Đạt (Q2 phụ thuộc N2′).

## V3.2 Đếm lại số năm bằng cách khác

Cách khác người viết: lấy số dòng (`grep_kb.sh -H -n`) của tiêu đề và của dòng có năm, rồi so khoảng dòng (tiêu đề + 15 dòng) — không đọc file trực tiếp.
- Mẫu `^## Nguồn`: **143 file / 151 tiêu đề**; năm 2023–26 ⇒ 119; 20xx ⇒ 130 (khớp vòng 2, chưa khớp 111 / 123 của người viết — chênh nhỏ, chấp nhận ghi "cỡ").
- **Nhưng mẫu `^## Nguồn` gộp cả mục "## Nguồn gốc"** (lịch sử ra đời, không phải nguồn dữ liệu): 151 tiêu đề = **112 "Nguồn dữ liệu" + 38 "Nguồn gốc" + 1 khác**. Chỉ tính
  "Nguồn dữ liệu": **112 file**, cả 112 có năm 2023–26 ⇒ "12 file chỉ có năm < 2023" đến từ mục **Nguồn gốc**, không phải nguồn cũ.
- **Trong đúng ba thư mục H4c định hiện năm**, số file có mục "## Nguồn dữ liệu": `travel/tickets` **4 / 6**, `travel/places` **8 / 36**, `festivals` **1 / 27** ⇒ **13 / 69 file**.
  (`festivals` có 27 / 27 tiêu đề `^## Nguồn` nhưng gần hết là "Nguồn gốc".)

### N2′ (major) — Số làm căn cứ cho Q2 sai mục; H4c phủ khoảng 1 / 5 file đích

- **Vị trí:** §5.3 "Kho có gì", luật chọn năm; §10 Q2 (a).
- **Yêu cầu:** số dẫn khớp thật; User chọn Q2 dựa trên hệ quả đúng.
- **Bằng chứng:** V3.2. Thiết kế đọc mục "Nguồn dữ liệu" (đúng), nhưng số "143 / cỡ 110–130 file" đếm theo `^## Nguồn` (gồm "Nguồn gốc"), và đếm trên cả kho chứ không trên ba thư mục đích.
- **Tác động:** Q2 (a) hứa "thẻ hiện nguồn năm …" nhưng với số thật đa số thẻ `travel/places` và gần hết thẻ `festivals` sẽ trống. Nếu plan làm theo con số (khớp `^## Nguồn`), thẻ lễ hội
  sẽ hiện năm lấy từ mục lịch sử — sai sự thật trên giao diện. Câu "file chỉ có năm < 2023 vẫn hiện, vì đó là nguồn cũ" dựa trên cách đếm này.
- **Tiêu chí đóng:**
  1. §5.3 thay số bằng số theo `^## Nguồn dữ liệu` trên ba thư mục đích (mẫu ghi cạnh số), ghi rõ "không đọc mục Nguồn gốc".
  2. Bỏ hoặc sửa câu "12 file chỉ có năm < 2023 … nguồn cũ".
  3. Q2 (a) "khi nào sai" thêm: chỉ ~13 / 69 file đích có mục nguồn ⇒ đa số thẻ không hiện năm. Thêm một ngưỡng ghi trước cho kết quả âm (vd < 50 % file đích đọc được năm ⇒ làm như (c)),
     hoặc nói rõ phần đọc thêm dòng "Nguồn:" khác (nếu có) để plan chốt.

## V3.3 Giới hạn vòng 3

- NOT RUN: các số 36 / 11 và 11 / 6 của H1b (như vòng 2, cần câu thử ngoài Căn cứ).
- Chưa kiểm các dạng ghi nguồn khác "## Nguồn dữ liệu" trong `travel/places` (có 16 file có dòng bắt đầu bằng "Nguồn / Tham khảo") — để người viết chốt ở tiêu chí đóng 3.

## V3.4 Decision vòng 3

**changes_requested** — vòng 3 / 4. Chỉ cần sửa N2′ (§5.3 + Q2). Vòng 4 người kiểm chỉ kiểm hai chỗ đó. Còn vòng `changes_requested` thứ tư nữa thì theo skill phải dừng và xem lại thiết kế với User;
để tránh, sửa đúng tiêu chí đóng, không mở thêm. Mọi phần khác đạt, ranh giới giữ nguyên.

---

# Vòng 4 — kiểm N2′ (bản 4, cuối)

Decision vòng 4: **ready_for_user_confirmation**
Date: 10:37 02/11/2026 (`date`)
Sha đã review: **`589bec308f41`** (531 dòng; tính lại khớp). Quét trùng bản 4: **0 trùng**.
Phạm vi: chỉ §5.3, Q2 và các sửa kéo theo người viết khai (§1 dòng vấn đề, §2 dòng cách hiểu H4c, §3 bảng phạm vi, §9 giới hạn).

## V4.1 N2′ — **đóng**

- [Chạy] Đếm lại bằng cách khác người viết (`grep_kb.sh --dir <thư mục> -c '^## Nguồn dữ liệu'`, lấy file có số > 0): tickets **4**, places **8**, festivals **1** ⇒ **13 / 69**. Khớp §5.3.
- [Chạy] `travel/places`, mẫu `^[#*> -]*(nguồn|tham khảo)`: 19 file; số dòng đó có năm `20[0-9]{2}` = **0**. Đếm thêm bằng mẫu khác `(nguồn|tham khảo) *:.*20[0-9]{2}`: 0 dòng / 0 file. Khớp câu "0 dòng có năm".
- Câu "năm < 2023 = nguồn cũ" đã bỏ; [Đọc] không còn "năm lớn nhất / nguồn năm / 111 / 123" ngoài bảng lịch sử "Trả lời review".
- Ngưỡng ghi trước "< 50 % file đích đọc được năm ⇒ không hiện năm" có sẵn, áp lên số hôm nay (19 %) ra "không làm" — áp đúng luật ghi trước, không chọn sau khi thấy số.

## V4.2 Q2 mới

Tick được: (a) dòng cố định khi nguồn trích thuộc ba thư mục đích, (b) hiện năm, (c) không làm. Mỗi phương án có hệ quả. (a) có "khi nào sai" (chỉ biết "có thể đã đổi", không biết cũ bao nhiêu);
(b) nêu độ phủ 13 / 69 + ngưỡng; có câu tự kiểm. Đạt.

## V4.3 Sửa kéo theo

§1, §2, §3, §9 cùng nghĩa với §5.3 mới ("báo có thể đã đổi", không qua model). §6 (H4a rồi H4c), §8 (H4c 0 USD) vẫn khớp. Không thấy mâu thuẫn. Thiết kế mới nhỏ hơn bản 3 (nửa ngày, không
đổi chữ câu trả lời, không chạm S-G / S-AT) — hợp mức công.

Không có finding mới.

## V4.4 Decision vòng 4

**ready_for_user_confirmation** cho sha `589bec308f41`.
- User cần: duyệt sha này một lần (trần mặc định 0,30 USD) và chọn Q1–Q5; A tự xác nhận dòng "A quyết" ở §2 (H1 bậc 1 tuần 1) khi trình.
- Giới hạn review còn lại: các số 36 / 11 và 11 / 6 của H1b (NOT RUN, ngoài Căn cứ); số dẫn ngoài Căn cứ (`Project_Status.md` §1 / §4, B119, C102) spec đã ghi là "dẫn".
- Phase 9 chưa mở code cho tới khi User duyệt; mỗi phần vẫn qua plan nhỏ + review riêng.
