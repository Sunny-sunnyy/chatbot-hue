# Review plan T1 — ngày + âm lịch (`2026-11-08-phase-9-t1-ngay-plan.md`, bản 1)

Người review: sub-agent độc lập (A giao), 08/11/2026 khoảng 11:10 (`date` lúc kiểm: 11:09:22 08/11/2026). Chỉ đọc; không gọi API trả phí, không cài gì.
Thước: spec Phase 9 bản 13 §12 (sha `5557f0fd7650`, kèm review B v13 m-2), `Session_Prompt.md` §4, §6–§8, §10, `WORKFLOW.md` §4 (4c),
`skills/run-experiment/SKILL.md`, code thật ở `main` (`442f758`).

**Kết luận: `changes_requested`** — 0 blocker · 5 major · 6 minor.

Phần đúng hướng: chọn lịch Việt Nam UTC+7, không dùng thư viện lịch Trung Quốc; model chỉ gửi số + loại lịch (`Literal`, kiểm khoảng), code dựng chữ;
≤ 2 lần / câu; chỉ đưa công cụ khi code dò thấy từ chỉ ngày (giống `thoi_tiet`); không bộ kín (khớp §12.4); phương án B khớp §12.2; sàn
"0 ngày / thứ sai trong chữ trả lời, cả khi model không gọi công cụ" khớp m-2; có 2 năm Việt Nam khác Trung Quốc (1985, 2007); cách cài thư viện
không xoá gói lạ trong `.venv` chung (đã kiểm, xem cuối).

---

## Major

### M-1 — Tiền: plan chạy "mỗi bên ×2" nhưng giữ ước 0,11 của spec (tính cho 2 lượt tổng) ⇒ chạm điểm dừng 0,13 giữa chừng

- **Chỗ:** plan §1 "Mốc … Mỗi bên ×2"; §4 "Tiền ≈ 0,11 … dừng ở 0,13".
- **Yêu cầu:** spec §12.7 dòng T1 ≈ 0,11 = (28 + 32 + 30) × **2** × 0,0006 ("một biến thể + mốc"); `run-experiment` §1.5 ước USD trước, §3.8 ước theo đúng câu bị ảnh hưởng, kèm cận trên.
- **Bằng chứng:** 90 câu × 0,0006 = 0,054 / lượt. Plan chạy mốc ×2 + nhánh ×2 = 4 lượt ⇒ ≈ **0,22**, chưa tính lượt có công cụ tốn thêm một vòng gọi model,
  pilot 5 câu, và thủ tục S-AT (sinh lại câu an toàn 3 + 3 lần khi chênh). Số 0,11 chỉ đúng khi mỗi bên 1 lượt.
- **Hệ quả:** harness dừng ở 0,13 khi mới chạy được ~60 % ⇒ thiếu số cho tiêu chí; hoặc phải xin thêm tiền giữa chừng.
- **Hướng sửa gợi ý (rẻ nhất, đúng tinh thần đo):** câu Golden 30 / an toàn 32 mà **code không dò thấy từ chỉ ngày** thì chuỗi gửi model giống byte giữa
  mốc và nhánh (do cổng công cụ) — test chuỗi chứng minh được, 0 USD — nên chạy chúng chỉ đo nhiễu, không đổi kết quả. Chỉ chạy cặp mốc / nhánh ×2 cho
  câu có từ chỉ ngày (28 câu ngày + phần Golden / an toàn mà bộ dò bật). Nếu chọn cách này phải ghi trước + A đồng ý (đổi cách đo S1 / S4 của spec).
- **Đóng khi:** plan ghi phép tính tiền khớp số lượt thật (mỗi bộ × số lượt × bên), có cận trên gồm vòng công cụ + S-AT + pilot, và điểm dừng đặt theo số đó
  (hoặc thu bộ như gợi ý trên, có A duyệt); nếu > 0,11 thì nêu rõ phần vượt so với dòng §12.7.

### M-2 — Câu trả lời chỉ có ngày (không đoạn kho) sẽ hỏng kiểm citation ⇒ lỗi thay vì câu trả lời

- **Chỗ:** plan §3 `ngay_lich.py` "chữ trả về do code dựng"; không nói kết quả công cụ có vào sổ nguồn không.
- **Yêu cầu:** spec §12 "Không đổi: sổ nguồn + kiểm citation"; tiêu chí 1 (giảm từ chối nhầm ở câu "có thể trả lời bằng ngày").
- **Bằng chứng:** `backend/llm/citations.py:28-29` — câu trả lời không phải câu từ chối mà không có `[n]` ⇒ `CitationIntegrityError("Grounded answer has no citation")`;
  `[n]` phải nằm trong sổ nguồn (`:31-33`). Công cụ `thoi_tiet` giải bài này bằng cách đăng kết quả thành một nguồn có mã `[n]`
  (`assistant.py:400-407` `_nguon_thoi_tiet`, mô tả công cụ dặn ghi `[n]` — `full_corpus_prompt.py:132-136`). Plan T1 không có bước tương tự.
- **Hệ quả:** câu kiểu "Tết năm nay ngày mấy", "hôm nay âm lịch ngày mấy" — kho không có đoạn nào để trích — model trả lời đúng ngày vẫn bị code coi là lỗi
  citation ⇒ người dùng thấy lỗi; tiêu chí 1 có thể trượt vì cơ chế chứ không vì model.
- **Đóng khi:** plan chọn rõ một cách (vd kết quả `ngay_lich` thành một nguồn trong sổ nguồn như `thoi_tiet`, mô tả công cụ dặn ghi `[n]`; nguồn hiện
  tiêu đề kiểu "Lịch hệ thống — tính theo giờ Việt Nam") và có test 0 USD: câu trả lời chỉ trích nguồn ngày qua được `check_citations`.

### M-3 — `max_turns` = 4 với tối đa 2 `tim_kho` + 2 `ngay_lich` (+ `thoi_tiet`): spec giao plan kiểm, plan không nhắc

- **Chỗ:** plan §3 "≤ 2 lần / câu"; không có dòng `max_turns`.
- **Yêu cầu:** spec §12.6 dòng §4 "plan kiểm `max_turns` đủ khi đủ 4 công cụ … plan đo `max_turns` = 0".
- **Bằng chứng:** `generator_openai_full_corpus.py:420-422` chạy với `ASSISTANT_MAX_TURNS`; chạm trần ⇒ `INSUFFICIENT_ANSWER` + outcome `max_turns`
  (`assistant.py:615-616`). Câu "rằm tháng tới" cần: biết hôm nay → đổi âm → dương → `tim_kho` lễ hội → viết = 4 vòng nếu gọi tuần tự. Plan không nói
  kết quả `doi(...)` có kèm luôn dòng "hôm nay" (để một lần gọi đủ) hay không, cũng không nêu chữ ký công cụ (một công cụ tham số tuỳ chọn, hay hai việc).
- **Hệ quả:** câu ngày phức tạp chạm trần ⇒ thành câu từ chối — đúng loại lỗi T1 muốn sửa, và bị đếm như "từ chối nhầm".
- **Đóng khi:** plan (a) nêu chữ ký công cụ và nội dung trả về (khuyến nghị: mọi kết quả kèm dòng hôm nay dương + âm + thứ, để câu "tháng tới / năm nay"
  chỉ cần 1 lần gọi); (b) thêm chỉ số "lượt chạm `max_turns` ở nhánh = 0" (sàn hoặc theo dõi, ghi trước) đếm bằng code từ `outcome`.

### M-4 — Bộ dò "từ chỉ ngày" là cổng chính nhưng chưa có danh sách từ, chưa đo độ phủ

- **Chỗ:** plan §3 "chỉ đưa khi code dò thấy từ chỉ ngày … như `thoi_tiet.co_tu_khoa_luot`".
- **Yêu cầu:** spec §12.2 dòng T1 (công cụ / phương án B đều "chỉ khi câu có từ chỉ ngày (code dò)"); bài học B5c (công cụ có mặt đổi cách tìm — spec §12.6 §5);
  `run-experiment` §1.2 "kiểm giả định bằng máy trước khi code", §1.6 cỡ mẫu.
- **Bằng chứng:** `thoi_tiet.py:48-70` có danh sách từ cụ thể; plan T1 không ghi từ nào. Hai chiều hỏng: bộ dò hẹp ⇒ bỏ sót câu "rằm / mùng / Tết / Vu Lan /
  cuối tuần" ⇒ không có công cụ ⇒ tiêu chí 1 trượt; bộ dò rộng ("ngày", "tháng" rất hay gặp trong câu về lễ hội, giờ mở cửa) ⇒ công cụ có mặt ở nhiều câu Golden /
  an toàn ⇒ lặp lại rủi ro B5c và mất cách giảm tiền ở M-1.
- **Đóng khi:** plan ghi danh sách mẫu (regex) và trước lượt có phí chạy 0 USD báo: số câu bật trên 28 câu ngày (mục tiêu: bật ở mọi câu cần ngày; liệt kê câu
  bỏ sót có chủ ý), trên Golden 30, an toàn 32 (và nên cả Golden 176) — số này cũng là cỡ mẫu thật cho S1 / S4.

### M-5 — Chỉ số quyết "giảm từ chối" có thể đạt bằng câu trả lời sai (không phải sai ngày)

- **Chỗ:** plan §1 tiêu chí 1 + 2.
- **Yêu cầu:** `Session_Prompt.md` §7 "chất lượng cần thiết trước"; `run-experiment` §1.3 (mỗi chỉ số định nghĩa đếm gì, không đếm gì), §4 "câu chỉ đổi ở một lượt
  không tính".
- **Bằng chứng:** tiêu chí 1 chỉ đếm chữ = `INSUFFICIENT_ANSWER`; tiêu chí 2 chỉ bắt ngày / thứ sai. Câu chuyển từ "từ chối" sang "trả lời" mà nói chắc điều
  kho không có (vd khẳng định "tuần này có lễ X", giờ / lịch biểu diễn khác kho) vẫn được tính là thắng. Bộ 30/10 đã có nhãn cho đúng loại lỗi này
  (`data/ngay_hien_tai_2026-10-30/plan_nhap.md` §2: L1 giả định ngày / kết luận không điều kiện, L3 sai kho); ở lượt 30/10, 6 / 12 câu quyết bị từ chối
  (đếm từ `ket_qua.json`) ⇒ "giảm ≥ 3" khả thi nhưng chỉ có nghĩa khi câu mới trả lời là câu dùng được. Plan cũng chưa nói câu nào trong ~10 câu âm lịch mới
  "có thể trả lời bằng ngày" (nhãn ghi trước) và chưa nói cách xử lý câu chỉ đổi ở một trong hai lượt.
- **Đóng khi:** plan định nghĩa chỉ số quyết = số câu từ chối nhầm giảm **mà câu trả lời mới được sub-agent ngữ cảnh mới chấm mù là OK** (không L1 / L3 theo
  nhãn 30/10), hoặc thêm sàn "câu L1 / L3 mới ở bộ ngày = 0"; ghi nhãn từng câu (in_kho, expected_type) cho ~10 câu mới trước khi chạy; ghi luật "câu chỉ
  đổi ở một lượt không tính".

## Minor

### m-1 — 4c: thiếu loại lượt và đường chạy

- **Chỗ:** plan §3 "mỗi loại lượt (đầu, hỏi tiếp, có lịch sử)". **Yêu cầu:** `WORKFLOW.md` §4 (4c) — lượt đầu, lượt hỏi lại, **lượt ghép sau khi bấm nút**, lượt có
  lịch sử. **Bằng chứng:** có 3 đường gọi công cụ — không stream `answer_query` (`assistant.py:663-668`), stream (`:914-916`), song song #6 (`song_song_tra_loi: true`,
  `settings.yaml:65`); lượt biểu mẫu (`answer_bieu_mau`) sinh không công cụ và không được có `ngay_lich`. **Đóng khi:** bảng test ghi đủ: lượt đầu, lượt hỏi lại / ghép
  sau nút, lượt có lịch sử (từ chỉ ngày ở câu trước), cả không stream + stream, và lượt biểu mẫu không có công cụ.

### m-2 — Danh sách file thiếu chỗ đăng ký công cụ và trạng thái stream; nên dùng lại hàm ngày có sẵn

- **Bằng chứng:** công cụ được gắn vào agent ở `generator_openai_full_corpus.py:395-437` (`_assistant_for`, `generate_with_tools`, `start_tools_stream` — tham số
  `lich_trinh_fn` / `thoi_tiet_fn`) và mô tả công cụ ở `full_corpus_prompt.py` (như `THOI_TIET_MO_TA`) — không có trong plan §4. Stream: công cụ lạ rơi vào nhánh
  "đang tìm" / "đã tìm" (`assistant.py:957-971`) ⇒ giao diện báo "đang tìm kho" khi đang tính ngày. Đã có `thoi_tiet.hom_nay_vn()` (`thoi_tiet.py:148`) và
  `today_line` + tên thứ (`full_corpus_prompt.py:38-45`) — plan viết `hom_nay()` mới. **Đóng khi:** plan thêm 2 file trên + nhánh trạng thái stream (hoặc ghi lý do
  để nguyên), và dùng lại `hom_nay_vn` / bảng tên thứ thay vì viết bản thứ hai.

### m-3 — Bộ ≥ 10 ngày đối chiếu: mới có 3, nguồn phần còn lại để sau; roundtrip không phải bằng chứng đúng

- **Yêu cầu:** spec §12.5 (≥ 10 ngày Tết / rằm công khai, ≥ 1 ngày Việt Nam ≠ Trung Quốc, năm khác plan tự kiểm nguồn); `run-experiment` (ghi trước).
- **Bằng chứng:** plan §2 nêu 1985, 2007, 2026; "7+ ngày khác E kiểm sau". Nguồn 1985: en.wikipedia (độc lập được) + agereckoner (plan tự nói cùng gốc Hồ Ngọc Đức);
  "tháng nhuận 1984 / 1985 khác lịch Trung Quốc" chưa có nguồn. Roundtrip dương → âm → dương chỉ kiểm tự nhất quán (thư viện tự kiểm điều này rồi), không chứng
  minh đổi đúng.
- **Đóng khi:** trước khi viết test, plan / file test có bảng ≥ 10 dòng: ngày dương · ngày âm · nguồn ngoài dòng Hồ Ngọc Đức (URL + ngày mở); roundtrip ghi là
  kiểm phụ, không tính vào 10. (0 USD — sửa lúc code được.)

### m-4 — Cách đếm "ngày sai trong chữ trả lời" chưa đủ rõ để code

- **Chỗ:** plan §1 tiêu chí 2. **Bằng chứng / chỗ hở:** (a) "đối chiếu với đáp án" — mỗi câu cần đáp án ghi trước (ngày đích dương + âm + thứ), còn ngày lấy từ kho
  (ngày âm của lễ hội, năm lịch sử) không so với ngày chạy; nên tách 3 luật tất định: thứ khớp ngày nêu cùng câu · cặp dương ↔ âm cùng câu khớp hàm đã qua bộ đối
  chiếu · "hôm nay / ngày mai là …" khớp ngày chạy; (b) mẫu thiếu "Chủ nhật", "tháng Chạp / Giêng", "ngày … âm lịch"; (c) ngày chạy lấy theo giờ Việt Nam **từng câu**
  (lượt có thể qua nửa đêm); (d) sàn áp cho tập nào — nên mọi câu trả lời của nhánh (bộ ngày + Golden + an toàn). Đáp án dùng cùng thư viện là vòng tròn — chấp nhận
  được nhờ bộ đối chiếu, nhưng ghi rõ giới hạn này. **Đóng khi:** plan ghi 4 điểm trên trước lượt có phí.

### m-5 — S5 / S6 bị hạ thành "báo thêm" mà không ghi lý do

- **Bằng chứng:** spec §12.3 "Sàn chung … áp cho mọi việc có lượt trả lời" (S5 p50 ≤ 3 s / p95 ≤ 5 s; S6 ≤ 0,0005 USD / câu Huế), nhưng dòng T1 §12.2 chỉ liệt kê S1 + Golden.
  Plan chọn đọc hẹp mà không nói. Lưu ý thật: lượt gọi `ngay_lich` thêm một vòng model ⇒ câu ngày chậm hơn và tốn hơn; ước 0,0006 / lượt đã > 0,0005 của S6.
- **Đóng khi:** plan ghi một câu "S5 / S6 theo dõi, không sàn cho T1 vì §12.2 dòng T1" và A xác nhận; báo p50 / p95 + USD / câu **riêng cho câu có công cụ**.

### m-6 — Thư viện: "nhỏ" đúng, "phổ biến" thì không; đã cài vào `.venv` chung trước khi plan được duyệt

- **Yêu cầu:** `Session_Prompt.md` §4 "Thư viện nhỏ, **phổ biến**, cần để chạy việc đã duyệt: A tự duyệt, ghi lý do, báo User sau"; spec §12.5 chỉ ghi "thư viện nhỏ".
- **Bằng chứng (PyPI JSON, WebFetch 08/11):** MIT ✓ · `requires_dist: null` (0 phụ thuộc) ✓ · `requires_python >=3.9`, phân loại 3.9–3.13 ✓ (`.venv` là 3.13) · 1.4.0 tải lên
  2026-07-11 ✓ · wheel 13 220 byte ✓ · README: mặc định UTC+7, 1900–2100, test roundtrip ✓. Gói **mới** (bản đầu 2026-02-07, 7 bản trong 9 tháng), một tác giả `thongbui`,
  `maintainer: null`; số người giữ trên PyPI không xem được (trang dự án bị chặn "Client Challenge") ⇒ "1 người giữ" của plan **chưa kiểm được**, chỉ biết 1 tác giả.
  Quan sát: `lunar_vn` đã có trong `.venv` chung lúc **11:07:28 08/11** (`ls --time-style=full-iso`), worktree `/tmp/e_t1` đã sửa `pyproject.toml` + `uv.lock` và có
  `backend/llm/ngay_lich.py` mới — trong khi plan ghi "chờ A duyệt".
- **Đóng khi:** A ghi duyệt thư viện kèm lý do (nhỏ, 0 phụ thuộc, MIT, **không phổ biến** ⇒ bù bằng đọc hết mã + ghim hash) và báo User sau theo §4; E xác nhận việc
  cài / code trước duyệt nằm trong quyền đã có (hoặc A chấp nhận). Ghi chú cho mọi session: tới khi T1 vào `main`, `uv sync` thường ở `main` sẽ gỡ `lunar-vn`
  (cùng `sherpa-onnx`) — chỉ dùng `--inexact`.

---

## Đã kiểm (cách kiểm)

| Mục | Kết quả |
|---|---|
| Spec §12.2 / §12.3 / §12.4 / §12.5 / §12.6 / §12.7 + review B v13 m-2 | đọc đủ; khớp trừ M-1, M-3, m-5 |
| Phép tính 0,11 | (28 + 32 + 30) × 2 × 0,0006 = 0,108 ✓ — nhưng là 2 lượt tổng (M-1) |
| Bộ ngày 15 | `md5sum` = `722d7c92ae9ec1cb…` ✓ khớp plan; 15 dòng; bộ mới 3 dòng ✓; lượt 30/10: 6 câu từ chối, cả 6 trong 12 câu quyết (đếm khoá, không chép câu) |
| Cách `thoi_tiet` được gắn cờ / đăng ký | `assistant.py:687-702` (chỉ khi `co_tu_khoa_luot`), `generator_openai_full_corpus.py:395-437`, nguồn `[n]` `assistant.py:400-407`, cờ cần `tim_them` (`:103-104`); `settings.yaml:62` `today_line: false`, `:67` `tim_them: true`, `:77` `thoi_tiet: true` |
| Kiểm citation | `citations.py:19-33` — câu không từ chối phải có `[n]` trong sổ nguồn (M-2) |
| PyPI `lunar-vn` | WebFetch `https://pypi.org/pypi/lunar-vn/json` 08/11 — số ở m-6; sha256 wheel `c42506ee…4749`, sdist `d8101646…1bf9` |
| Cách cài | diff worktree: `pyproject.toml` +1 dòng, `uv.lock` +11 dòng chỉ gói `lunar-vn`, hash khớp PyPI ✓. `uv sync --dry-run --inexact --frozen` ở `main`: "Would make no changes"; `uv sync --dry-run --frozen` (không inexact): sẽ gỡ `lunar-vn`, `sherpa-onnx`, `sherpa-onnx-core` ⇒ cách cài của plan đúng là không gỡ gói lạ |
| Không mở | file `*sealed*`, `.env`, `knowledge-base-hue/`, `STATUS_*.md`; không đọc nội dung `backend/llm/ngay_lich.py` trong worktree (ngoài phạm vi review plan) |

**Over-engineering:** không thấy lớp thừa lớn. Nhẹ: roundtrip mỗi ngày 1950–2100 trùng test của thư viện (giữ được vì rẻ, nhưng không tính là bằng chứng — m-3);
chạy Golden / an toàn ×2 cho cả câu có chuỗi giống byte là đo nhiễu tốn tiền (M-1).
