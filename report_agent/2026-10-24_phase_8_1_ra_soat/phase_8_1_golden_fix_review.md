# Review: Phase 8.1 — sửa `reference_answer` 10 câu Golden (A qua sub-agent; C27)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major; 2 minor đã đóng — §7)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 12:28 (`date`)
Căn cứ: User duyệt 12:20 "sửa theo đề xuất". Nguyên tắc: đáp án chỉ trả lời điều câu hỏi hỏi; chỉ thêm điều kiện khi
thiếu nó thì sai hoặc gây hiểu lầm; chi tiết phụ đúng nguồn giữ nguyên.
Implementation report (private): `data/phase_8_1/golden_reference_fix_2026-10-25.md`

Report này không chép câu hỏi, đáp án hay keyword Golden.

## 1. Phạm vi đã review

- File chính thức `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` và smoke
  `golden_full_corpus_smoke.jsonl`.
- 7 file authoring `knowledge-base-hue/<domain>/evaluation/golden_full_corpus_authoring.jsonl`.
- Backup `knowledge-base-hue/meta/golden_backup_2026-10-25/` (9 file).
- Report từng câu của A.
- Code `merge_authoring` / `select_smoke` / `check_case` (`backend/evaluation/golden_full_corpus.py:41-130`).
- Các dòng nguồn mà report trích.

C đọc nội dung Golden: được phép, A giao. C **không** đụng câu kín trong việc này.

md5 (12 ký tự):

| File | Bản sao lưu | Hiện tại |
|---|---|---|
| official | `c30b56f22bd3` | `b40ca15ef5f8` |
| smoke | `fae56cd0515f` | `d80b58c50f38` |

Cả hai giá trị "hiện tại" khớp tin của A. sha256 12 ký tự của official hiện tại: `99637ae3c8d4`.

## 2. Findings

Không có blocker hay major.

- **m1 (minor) — dòng 92 thêm một lời dặn mà câu hỏi không hỏi.**
  - Đáp án mới thêm một vế khuyên khách tự kiểm tra thông tin trước mỗi kỳ. Vế này đúng nguồn (`Lễ hội Điện Huệ
    Nam.md:112`), nhưng không phải điều kiện mà thiếu nó thì sai hay gây hiểu lầm: vế đầu của đáp án đã trả lời đủ câu
    hỏi.
  - Yêu cầu bị ảnh hưởng: nguyên tắc User 12:20.
  - Tác động **trung bình**: judge có thể trừ Completeness với câu trả lời đúng và gọn mà không nêu lời dặn. Đây chính là
    loại lỗi đợt sửa này muốn gỡ.
  - **Đóng khi:** A bỏ vế đó, chỉ giữ vế đầu (keyword vẫn đủ), hoặc A ghi lý do giữ.
- **m2 (minor) — dòng 41: `sources` chưa có file chứa dữ kiện mới.** A đã tự nêu. Đáp án mới lấy danh sách giấy tờ đầy
  đủ từ file vé, nhưng `sources` chỉ có file hướng dẫn di tích, mà file đó ghi hẹp hơn.
  - Tác động **thấp**: `merge` bỏ `sources` khỏi file chính thức, nên không đổi cách chấm; chỉ ảnh hưởng truy vết.
  - **Đóng khi:** thêm file vé vào `sources` của dòng authoring đó và chạy lại `check --authoring` + `merge`, hoặc ghi
    "để nguyên" kèm lý do.

Ghi nhận, không phải finding:
- **Dòng 46, 157** vẫn lặp một cụm chỉ mốc khoảng cách: keyword chứa nguyên cụm đó, nên không gỡ hết được. Chấp nhận.
- **Dòng 165** thêm một khoản bắt buộc chưa tính trong giá vé. Thiếu vế này người dùng hiểu sai tổng tiền phải trả. Hợp
  nguyên tắc "thiếu thì gây hiểu lầm".
- **Dòng 141** thêm cách đi hợp lệ. Nếu chỉ trả lời "không", người đọc dễ hiểu là không có cách nào đi được. Hợp nguyên
  tắc.
- **Dòng 23:** nguồn của quán thứ hai (`banh canh o hoa.md:19`) cũng khớp với câu hỏi. Đáp án mới tách chú thích riêng
  cho từng quán, nên hết mơ hồ và đúng nguồn.
- **Không còn so trực tiếp với 7B Run 1 ở 10 câu này:** điểm 7B chấm theo đáp án cũ. G0.6 cần ghi hash Golden mới và
  ghi rõ giới hạn này. Split không bị ảnh hưởng, vì `split.json` khóa theo SHA câu hỏi, và câu hỏi không đổi.

## 3. Cách người kiểm chạy lại thật

Mọi lệnh chỉ đọc; không chạy `merge` / `smoke` (hai lệnh này ghi file Golden).

```bash
# so với backup + dựng lại file chính thức bằng hàm merge_authoring (không ghi) + kiểm smoke + giữ keyword
cd backend && HF_HUB_OFFLINE=1 uv run python -I -c "…merge_authoring(kb) == official; select dòng smoke; diff từng authoring với backup…"
# pytest (không paid, không Qdrant)
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py tests/test_full_corpus_eval.py -q
# check thật trên file Golden (chỉ đọc)
uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl
uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/<domain>/evaluation/golden_full_corpus_authoring.jsonl --authoring   # 7 domain
# đối chiếu nguồn: sed -n '<dòng>p' trên đúng các dòng report trích
```

## 4. Kết quả quan sát

**(2) Không đổi gì ngoài phạm vi:**

| Phép kiểm | Kết quả |
|---|---|
| File chính thức: 176 = 176 dòng; khác backup đúng 10 dòng 23, 41, 46, 92, 93, 141, 151, 157, 165, 174; field đổi chỉ `reference_answer` | đạt |
| `merge_authoring(kb)` (không ghi) = file chính thức, từng row; serialize `json.dumps(ensure_ascii=False)` khớp từng dòng | đạt |
| Smoke = dòng 3, 24, 42, 44, 55, 82, 114, 141, 155, 163 của file chính thức mới. Smoke cũ cũng đúng bằng các dòng đó của file cũ. Chỉ vị trí 8 (dòng 141) đổi | đạt |
| Authoring so với backup, số dòng giữ nguyên, chỉ `reference_answer` đổi: foods [23]; heritages [4, 9]; festivals [19, 20]; performing_arts không đổi; travel/places [24]; travel/services [2, 8]; travel/tickets [3, 12] | đạt |
| Mọi keyword có trong đáp án cũ vẫn có trong đáp án mới (10/10) | đạt |

**(1) Đúng nguồn và đúng nguyên tắc 12:20:** C đọc câu hỏi và keyword của 10 câu, rồi in đúng các dòng nguồn report
trích:
- dòng 23: `banh canh o buom.md:5`, `banh canh o hoa.md:19`;
- dòng 41: `Vé tham quan Quần thể Di tích Cố đô Huế.md:130`, `heritage-guides.md:105`;
- dòng 46: `Lăng Khải Định.md:19`, `Lăng Tự Đức.md:100`;
- dòng 92: `Lễ hội Điện Huệ Nam.md:86`, `:112`;
- dòng 93: `Hội xuân Gia Lạc.md:10`, `:36`;
- dòng 141: `Đèo Hải Vân.md:130`;
- dòng 151: `Chi phí du lịch Huế.md:99`, `:101`;
- dòng 157: `Vịnh Lăng Cô.md:9`, `Bãi biển Thuận An.md:9`;
- dòng 165: `Vé biểu diễn … sông Hương.md:33`, `:41`;
- dòng 174: `Vé tham quan Quần thể … .md:58`.

Mọi dữ kiện trong 10 đáp án mới đều có ở dòng nguồn đã trích. 8/10 câu đạt nguyên tắc; dòng 92 vượt nguyên tắc (m1).
Dòng 41 đúng nguồn, nhưng `sources` chưa cập nhật (m2).

**(3) Test và máy kiểm:**
- pytest `test_golden_full_corpus.py` + `test_full_corpus_eval.py`: **27 passed**. Các test này dùng dữ liệu tự dựng, không
  đọc Golden thật, nên C chạy thêm `check` trên file thật:
  - official: **exit 0**, 176 dòng (75 / 29 / 29 / 25 / 18);
  - smoke: **exit 0**, 10 dòng;
  - 7 file authoring `--authoring`: **exit 0** cả 7 (37 / 36 / 27 / 17 / 32 / 13 / 14 dòng).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy `merge` / `smoke` thật (ghi file). Thay vào đó gọi hàm `merge_authoring` / so dòng smoke trong bộ nhớ, cho
  cùng kết luận.
- Không chấm lại câu trả lời 7B theo đáp án mới. Đó là việc của G0.6 / G2, ngoài phạm vi C27.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Đúng phạm vi, không đổi gì ngoài 10 đáp án, dữ kiện đúng nguồn, máy kiểm và test đạt.
Bước tiếp:
- A quyết m1 (bỏ lời dặn ở dòng 92 hay giữ) và m2 (thêm nguồn vào dòng 41 hay để nguyên). Nếu A sửa, C chỉ cần kiểm lại
  diff của dòng đó, cùng `check` và `merge`.
- Sau đó A ghi hash Golden mới vào G0.6.

Tiền: **0 USD**.

## 7. Kiểm lại m1, m2 sau khi A sửa (12:31)

| Finding | A sửa | C kiểm | Trạng thái |
|---|---|---|---|
| m1 dòng 92 | bỏ vế lời dặn | đáp án mới chỉ còn vế trả lời câu hỏi; giữ 2 keyword; khác bản gốc chỉ ở cách chữ | đóng |
| m2 dòng 41 | thêm file vé vào `sources` (authoring heritages dòng 4) | dòng authoring đó chỉ đổi `reference_answer` + `sources`; file thêm có trong corpus (`check --authoring` exit 0) | đóng |

Kiểm lại toàn bộ:
- File chính thức vẫn khác backup đúng 10 dòng như trước.
- `merge_authoring` (gọi trong bộ nhớ) vẫn ra đúng file chính thức.
- Các file authoring khác không đổi so với lần kiểm 12:28.
- `check`: official, smoke và heritages `--authoring` đều **exit 0**.

md5 sau sửa:
- official: **`0f7dbf41b422`** (khớp tin của A);
- smoke: `d80b58c50f38`, không đổi vì dòng 92 không thuộc smoke, đúng như mong đợi.
