# Review cả nhánh — T1 ngày + âm lịch (`p9-t1-ngay`)

Người review: sub-agent độc lập (Claude Code, ngữ cảnh mới) · 12:17 08/11/2026
- Nhánh `origin/p9-t1-ngay` head `9f08d91` (5 commit trên `main` `442f758`); `git diff main...origin/p9-t1-ngay`: 8 file, +381 / −8.
- Tiêu chí: plan `docs/superpowers/plans/2026-11-08-phase-9-t1-ngay-plan.md` (sha256 đầu `cdf2c061381a` — đã kiểm khớp), spec Phase 9 §12 dòng T1.
- Report của E (`e_t1_ngay_implementation.md`) chỉ dùng làm mục lục; các ý chính kiểm lại bên dưới.
- Không mở file `*sealed*`, `.env`, `knowledge-base-hue/`, `STATUS_*.md`. 0 USD (không gọi API trả phí).

**Kết luận: `changes_requested` — 0 blocker / 1 major / 6 minor.**
- Code gọn, đúng hướng spec, cờ tắt không đổi gì.
- Một lỗi tất định cần sửa trước khi merge (M-1): từ 1/1 tới Tết, "năm nay" của lịch âm bị hiểu thành năm âm đang chạy ⇒ code tự ghi "đã qua N ngày" cho Tết sắp tới.

## 1. Đã tự kiểm (bằng chứng)

| Ý cần kiểm | Cách kiểm | Kết quả |
|---|---|---|
| Cờ tắt ⇒ prompt giống byte (Q1) | Đọc diff: mọi đường mới đều nằm sau `flags.ngay_lich` hoặc `ngay_lich_fn is not None`. `max_turns_for(None) = 4`. `full_corpus_prompt.py` chỉ thêm một hằng dùng làm mô tả công cụ. `cmp data/phase_9/t1/q1_main.jsonl q1_nhanh_tat.jsonl` ⇒ giống hệt (228 dòng) | **Khớp.** File Q1 ghi lúc 11:20, ở commit `0357d80`. Ba commit sau đó chỉ đụng đường cờ bật ⇒ theo cấu trúc code vẫn giống (xem m-3) |
| Cờ bật, câu không có từ chỉ ngày ⇒ giống byte | `grep`: `flags.ngay_lich` chỉ được đọc ở `_lich_extra` và `__post_init__`. Không có `ngay_lich_fn` ⇒ generator được gọi y như cờ tắt. Test `test_date_tool_offered_only_with_date_words` và `test_max_turns_…` (4 vòng) | **Khớp theo cấu trúc code.** Chưa có phép đo byte riêng cho ca này (m-3) |
| Tham số chỉ là số / `Literal` | Chữ ký `ngay_lich(loai: Literal[...], ngay: int, thang: int, nam: int, thang_nhuan: bool)`. Chữ người dùng (`cau`) chỉ đi vào `re.findall` của `khoang_ngay` (không chạy, không ghi log, không làm đường dẫn / URL). Log `tools` chỉ có `loai` | **Khớp.** Có kẽ hở: `ngay` / `thang` không bị kiểm khoảng (m-1) |
| Lịch âm UTC+7, chỉ nhận năm hỗ trợ | Chạy lại `data/phase_9/t1/tools/so_tet.py` với file tải về (`-I`): 199 năm, khớp 195. Lệch 1903 / 1925 / 1935 / 1965 — đúng như report. Thăm dò `ket_qua` ở biên 1976 / 2100 / 1968 / 2101 / 30 tháng thiếu / nhuận sai | **Khớp.** Ngoài khoảng ⇒ câu cố định; ngày không có ⇒ câu cố định |
| Câu chỉ trích nguồn ngày qua kiểm citation | Test của nhánh (không stream). Thêm một thăm dò stream của tôi (`/tmp/t1_review/test_probe_t1.py`, không nằm trong repo) | **Khớp**: `citation_error = None`, nguồn trích là `Lịch hệ thống…`. Stream chỉ có trạng thái `['searched', 'generating']`; `searched` đến từ lần tìm đầu V0, không có `searching` / `searched` do `ngay_lich` |
| Không làm hỏng công cụ / đường khác | Chạy 14 file test liên quan ở `/tmp/e_t1` (gồm b2, b5, b5b, song song #6, cổng đợt 1 / biểu mẫu, stream, api_chat, b3, b6, generator, assistant, boundary, citations, settings) | **531 passed**, 1 failed + 3 errors. Cả 4 ca hỏng đều cần `OPENAI_API_KEY` (`require_openai_key` / `bool('')`) — tôi chạy không nạp `.env`, lần chạy kèm `--env-file` bị chặn quyền ⇒ **NOT RUN**, không quy cho nhánh |
| Test có ý nghĩa | Đọc `test_ngay_lich.py`: phần lịch là logic thuần, có đáp án ngoài (Tết vi.wikipedia, 1985 / 2007 VN ≠ TQ). Phần nối vào trợ lý dùng model soạn kịch bản, chỉ để kiểm hành vi **của code** (danh sách công cụ, trần lần gọi, `max_turns`, citation), không giả làm PASS cho hành vi model | **Khớp.** `48 passed` (chạy lại) |
| `uv.lock` chỉ thêm `lunar-vn`, có hash | Diff `uv.lock`: 3 khúc, chỉ `lunar-vn` (sdist + wheel đều có sha256; wheel `c42506ee…`). `uv lock --check --offline` ⇒ khớp. `grep` mã thư viện trong `.venv`: không có `os` / `subprocess` / `socket` / `urllib` / `open(` | **Khớp** |
| Merge được | `git merge-tree --write-tree main origin/p9-t1-ngay` | sạch, không xung đột |
| Làm quá tay (over-engineering) | Module 139 dòng; `khoang_ngay` và `so_voi_hom_nay` là phép tính tất định, đúng luật "phép tính ⇒ code". Chỉ hơi trùng: `hom_nay` gần giống `thoi_tiet.hom_nay_vn`; khối dựng `PackedSource` gần giống `_nguon_thoi_tiet` | Không thành finding (nhỏ, có lý do: cần `now` để test) |

## 2. Finding

### M-1 (major) — "năm nay" của lịch âm sai từ 1/1 tới Tết: code tự ghi "đã qua" cho Tết sắp tới

- **Chỗ:** `backend/llm/ngay_lich.py:129` (`nam = nam or (solar_to_lunar(hom).year if loai == "am" else hom.year)`); mô tả công cụ `backend/llm/full_corpus_prompt.py:141` ("nam = 0 nghĩa là năm nay").
- **Yêu cầu:** spec §12 T1 / plan §1 tiêu chí 3 — 0 ngày sai trong chữ trả lời. Thứ tự lỗi của User: nói chắc mà sai còn tệ hơn từ chối nhầm. Nhánh đặt phép so "đã qua / còn N ngày" vào code chính để tránh lỗi A2 (kết luận ngược).
- **Bằng chứng (chạy thật, 0 USD):** `ket_qua("am", 1, 1, 0, False, now=20/01/2027 10:00 giờ VN)` trả về:
  `Ngày được hỏi (âm lịch 1/1/2026): Thứ Ba, 17/02/2026 … — đã qua 337 ngày (so với hôm nay)`.
  Người hỏi "Tết năm nay là ngày nào?" vào tháng 1/2027 là muốn hỏi Tết Đinh Mùi 06/02/2027.
  - Trước lần gọi, model không biết năm (công cụ chính là để cho biết), và mô tả công cụ dặn `nam = 0` là năm nay ⇒ rất dễ gửi 0.
  - Ca ngược lại cũng có: hỏi "rằm tháng Chạp năm nay" trong tháng 1 thì năm âm đang chạy lại đúng. Nếu chỉ đổi sang năm dương, ca này hỏng.
  - Lượt đo ngày 08/11 không thể bắt lỗi này: tháng 11 thì năm âm trùng năm dương.
- **Ảnh hưởng:** khoảng 3–7 tuần mỗi năm, đúng lúc người ta hỏi về Tết nhiều nhất. Câu trả lời sẽ nói chắc là "Tết năm nay đã qua", và lời nói đó có code đứng sau. Cờ đang tắt nên chưa ai gặp, nhưng code này được merge để bật sau.
- **Đóng khi:**
  - (a) Khi năm âm của hôm nay khác năm dương, `loai = "am"` và `nam = 0`, code trả **cả hai** ngày (năm âm N−1 và N, mỗi ngày có "đã qua / còn N ngày"), hoặc chọn theo một luật ghi rõ.
  - Kèm test có `now` rơi giữa 1/1 và Tết, gồm cả hai ca: "Tết / rằm tháng Giêng năm nay" và "tháng Chạp năm nay".
  - (b) Hoặc A / User chấp nhận đây là giới hạn đã biết, ghi vào report, và đặt làm cổng phải xử lý trước khi bật cờ.

### m-1 (minor) — `ngay` / `thang` không được kiểm khoảng; số quá lớn làm hỏng cả lượt

- **Chỗ:** `backend/llm/ngay_lich.py:49-52` (`dt.date(nam, thang, ngay)`, chỉ bắt `ValueError`); `backend/llm/assistant.py:452-470`; `failure_error_function=None` ở `generator_openai_full_corpus.py:420`.
- **Yêu cầu:** spec §12.5 — tham số là "kiểu `Literal`, kiểm khoảng".
- **Bằng chứng:** `ket_qua("duong", 10**20, 1, 2026, …)` ⇒ `OverflowError`. Thăm dò qua `answer_turn` với model soạn kịch bản ⇒ `GenerationError` ("OpenAI generation failed"): cả lượt ra câu lỗi thay vì câu cố định `CAU_NGAY_SAI`. Với `loai = "am"` thì đã bắt được (ra câu cố định).
- **Ảnh hưởng:** thấp. Model phải gửi số vô lý (người dùng gõ số rất dài là có thể). Không phải lỗ hổng bảo mật.
- **Đóng khi:** kiểm `1 ≤ ngay ≤ 31`, `1 ≤ thang ≤ 12` trước khi tính (hoặc bắt cả `OverflowError`) ⇒ trả `CAU_NGAY_SAI`; thêm một ca vào `test_impossible_dates_get_fixed_sentence`.

### m-2 (minor) — Bộ dò bắt nhầm số thứ tự và phân số

- **Chỗ:** `backend/llm/ngay_lich.py:75-79` (`thứ (?:hai|ba|…|[2-7])`, `\b\d{1,2}/\d{1,2}\b`).
- **Yêu cầu:** plan §2 bộ dò viết hẹp: công cụ có mặt ở mọi lượt thì đổi cách model tìm (bài học B5c), và lượt bật được thêm vòng (`max_turns` 5).
- **Bằng chứng:** `co_tu_ngay` trả True cho "mùa thứ hai", "Thứ ba bậc thềm". Câu Huế kiểu "vua thứ ba triều Nguyễn", "lần thứ hai" cũng dính theo cùng mẫu. Phân số như "1/2", "24/7" cũng bị bắt.
- **Ảnh hưởng:** chỉ khi cờ bật. Câu lịch sử nhận công cụ không cần ⇒ tốn thêm tiền, có rủi ro S4. Report ghi Golden 176 bật 9 / 176 nhưng chưa tách bao nhiêu câu trong đó là bắt nhầm.
- **Đóng khi:** chọn một trong hai:
  - loại "thứ X" khi đứng sau danh từ chỉ thứ tự ("vua / đời / lần / mùa / người / con …");
  - hoặc ghi vào report số câu bắt nhầm trong 9 / 176 và A chấp nhận.

### m-3 (minor) — Bằng chứng Q1 cũ hơn head và không phủ ca "cờ bật, không từ chỉ ngày"

- **Chỗ:** report §4 "Q1 cờ tắt: 228 / 228"; plan §1 "câu không bật có chuỗi gửi model giống byte … test + Q1 đã chứng minh".
- **Bằng chứng:**
  - `q1_*.jsonl` ghi lúc 11:20, ở commit `0357d80`, trước `2c6cd46` / `f536dfe` / `9f08d91`.
  - Q1 chỉ so nhánh **cờ tắt** với `main`.
  - Ca cờ bật mà câu không có từ chỉ ngày chỉ được test kiểm tên công cụ, không so chuỗi.
- **Ảnh hưởng:** thấp. Đọc code thấy giống theo cấu trúc (mục 1), nhưng report đang viết mạnh hơn bằng chứng có.
- **Đóng khi:** chạy lại Q1 ở `9f08d91` (0 USD) và thêm một chiều "cờ bật, câu không từ chỉ ngày". Hoặc sửa câu trong report thành "giống byte theo cấu trúc code; Q1 đo ở `0357d80`".

### m-4 (minor) — Report của E còn chỗ cũ, tự mâu thuẫn

- **Chỗ:** `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md`:
  - dòng 26 "44 test", dòng 59 "Test 44 passed … 142" (head có 48 / 146);
  - dòng 145 "A2 … **Chưa làm**" (đã làm ở `f536dfe`, mục 4b);
  - dòng 158 "E đề xuất **(b) trước khi bật**", và §6 còn để (a) / (b) / (c) như đang chờ quyết. §5 ghi R8 hai lần.
- **Yêu cầu:** luật "report luôn đúng hiện tại; xoá cái không còn đúng".
- **Ảnh hưởng:** A / User đọc §5–§6 sẽ hiểu nhầm trạng thái. Đoạn dán vào `bao_cao_he_thong` thì đúng.
- **Đóng khi:** sửa §2, §4, §5, §6 cho khớp lượt 3 và head `9f08d91`.

### m-5 (minor) — Kết quả "Đạt" là trên chính bộ đã dùng để chỉnh qua 3 lượt; chưa đo S5

- **Chỗ:** report §4, §4b, §4c.
- **Yêu cầu:** run-experiment — sửa sau khi đã thấy kết quả thì cần một lượt xác nhận. Spec §12 có sàn S5 (p50 ≤ 3 s / p95 ≤ 5 s).
- **Bằng chứng:**
  - Có 3 lần đổi code sau khi xem kết quả (`max_turns`, "đã qua / còn", khoảng tuần / tháng), đo lại trên cùng 27 câu.
  - Tiêu chí 3 chỉ đạt ở lượt 3. Tiêu chí 1 dao động 8 / 9 / 8; E2 / E3 / A6 đổi qua lại.
  - S5 NOT RUN.
- **Ảnh hưởng:** không chặn merge khi cờ tắt. Các sửa là phép tính tất định, không phải lời dặn khớp riêng từng câu, nên rủi ro "học thuộc bộ đo" thấp. Nhưng "Đạt" chưa đủ để bật cờ.
- **Đóng khi:** report ghi rõ "đạt trên bộ đã dùng để chỉnh". Trước khi bật cờ cần: S5 (đã xếp lượt) + một lượt xác nhận trên vài câu ngày mới, gồm ca của M-1.

### m-6 (minor) — Test chưa phủ vài đường plan đã nêu

- **Chỗ:** `backend/tests/test_ngay_lich.py`.
- **Bằng chứng:**
  - Plan §3 nêu test "lượt biểu mẫu không dùng đường công cụ" — không có trong file. Theo code thì đúng: `answer_bieu_mau` không gọi `_lich_extra`.
  - Không có test stream cho lần gọi `ngay_lich` thật (trạng thái không báo "đang tìm kho", review plan m-2). Thăm dò của tôi cho kết quả đúng: `['searched', 'generating']`.
  - Không có test cho đường song song #6. Theo code thì đúng: `spec` trace mang `history`, `_merge_spec` chép `so_nguon` / `tools`.
  - Bỏ ngỏ thêm: "tháng tới / tháng sau / cuối tuần" vẫn để model tự cộng tháng âm (năm nhuận, Chạp sang Giêng). Đây là phép tính lịch mà §2 muốn để code làm; chưa thấy ghi là giới hạn.
- **Ảnh hưởng:** thấp. Nếu sau này sửa luồng stream / song song thì có thể hỏng mà test không báo.
- **Đóng khi:** chọn một trong hai:
  - thêm 1 test stream có gọi `ngay_lich` (kiểm thứ tự trạng thái + citation) và ghi "tháng tới / cuối tuần do model tính" vào giới hạn trong report;
  - hoặc A chấp nhận và bỏ câu "lượt biểu mẫu" khỏi phần test đã làm.

## 3. Kết luận

`changes_requested`: 0 blocker / 1 major / 6 minor.
- **M-1** là lỗi tất định nằm trong chính phép tính mà code đảm nhận, sửa nhỏ (vài dòng + test).
- Các minor đóng được bằng sửa nhỏ hoặc ghi rõ trong report.
- Phần còn lại đạt tiêu chí:
  - cờ tắt không đổi gì;
  - tham số chỉ là số / `Literal`;
  - lịch âm UTC+7 đã đối chiếu;
  - citation qua cả stream lẫn không stream;
  - 531 test liên quan qua;
  - `uv.lock` sạch;
  - không làm quá tay.

## Vòng 2 — kiểm phần sửa `f388b19` (12:25 08/11/2026)

- Phạm vi: `git diff 9f08d91..origin/p9-t1-ngay`, 3 file, +40 / −7: `ngay_lich.py`, `NGAY_LICH_MO_TA`, `test_ngay_lich.py`.
- Worktree `/tmp/e_t1` đang ở `f388b19`, sạch.
- A chọn luật cho M-1: `nam = 0` ⇒ code trả **cả** lần gần nhất đã qua và lần sắp tới, mỗi lần kèm "đã qua / còn N ngày".
- A dời m-2…m-6 sang phiên sau; khi cờ tắt chúng không chặn merge.

| Finding | Kiểm | Kết quả |
|---|---|---|
| **M-1** | Đọc diff: `ket_qua` khi `nam = 0` tính 3 năm (gốc −1, gốc, gốc +1; gốc = năm âm của hôm nay khi `loai = "am"`), sắp xếp, rồi tách `≤ hôm nay` ↔ `> hôm nay`. Không còn đoán "năm nay". Mô tả công cụ đổi thành "nam = 0 khi người dùng không nêu năm — công cụ trả cả lần gần nhất đã qua và lần sắp tới". Test mới `test_no_year_gives_last_and_next_occurrence`: giờ giả 20/01/2027 (giữa 1/1 và Tết) cho Tết và rằm tháng Chạp; giờ giả 07/02/2027 (sau Tết). Tôi thăm dò thêm (`/tmp/t1_review/probe2.py`): đúng ngày Tết ⇒ "lần gần nhất … là hôm nay" + lần sắp tới 2028; tháng 6 nhuận ⇒ chỉ có lần đã qua (2025); 30/12 hay ngày 40 ⇒ câu cố định; năm 2100 ⇒ chỉ có lần đã qua, không lỗi | **Đóng.** Ví dụ 20/01/2027: "lần gần nhất 17/02/2026 — đã qua 337 ngày" + "lần sắp tới 06/02/2027 — còn 17 ngày nữa". Model có đủ hai ngày, không còn chỉ có Tết đã qua |
| **m-1** | `ngay_duong` kiểm `1 ≤ ngay ≤ 31`, `1 ≤ thang ≤ 12` trước khi tính. Test thêm `10**20`. Thăm dò `ket_qua("duong", 10**20, 1, 0)` và `("am", -3, 1, 0)` ⇒ câu cố định. Thăm dò cả lượt qua `answer_turn` (model soạn kịch bản gửi `10**20`) ⇒ hết `GenerationError` | **Đóng** |
| Q1 cờ tắt | Phần sửa chỉ đụng hàm của công cụ và mô tả công cụ; cả hai chỉ dùng khi công cụ được đưa ra ⇒ đường cờ tắt không đổi theo cấu trúc code. `cmp q1_main_head.jsonl q1_nhanh_tat_head.jsonl` ⇒ giống hệt, 228 dòng; file ghi lúc 12:21–12:22, cùng phút với commit `f388b19` (12:21) | **Khớp** |
| Test của nhánh | `pytest tests/test_ngay_lich.py` ở `/tmp/e_t1` ⇒ **53 passed**. Thăm dò stream cũ chạy lại: trạng thái `['searched', 'generating']`, citation qua | Đạt. Không chạy lại 14 file liên quan vì phần sửa chỉ nằm trong `ngay_lich.py` và mô tả công cụ |

**Kết luận vòng 2: `ready_for_user_confirmation`** khi merge với cờ `ngay_lich: false`. M-1 và m-1 đã đóng. Còn mở, đã dời phiên sau theo quyết định của A:
- m-2: bộ dò bắt nhầm số thứ tự / phân số;
- m-3: Q1 chưa đo ca "cờ bật, câu không có từ chỉ ngày";
- m-4: report của E còn chỗ cũ;
- m-5: chữ "Đạt" là trên bộ đã dùng để chỉnh; chưa đo S5; cần một lượt xác nhận trước khi bật cờ;
- m-6: thiếu test stream / biểu mẫu / song song; "tháng tới / cuối tuần" vẫn để model tự tính.

Ghi chú nhỏ, không phải finding: khi `nam = 0`, câu cố định "Ngày này không có trong lịch" (ví dụ 30 tháng Chạp) chỉ xét trong khoảng ±1 năm.
