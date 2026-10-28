# Review: plan B87 — đo "bịa thêm" và "sai cảnh báo an toàn / điều kiện vào khu vực"

Decision: bản 1 `41065f985c85` **changes_requested** (0 / 1 / 4) ⇒ **bản 2 `d69481b2addb` (12:35 28/10/2026): ready_for_user_confirmation** — M-1 + 4 minor đóng, 1 ghi chú mới không chặn (§8)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C81
Date: 12:28 28/10/2026 (`date`)
Chỉ dựa gói "Căn cứ để review" (`WORKFLOW.md` §9.1). Không đọc STATUS_B / tin của B ngoài tin báo sha.

## 1. Phạm vi đã review

- Plan (đọc hết, 141 dòng).
- `backend/evaluation/full_corpus_judge_prompt.md:10-16, :25-31` — judge hiện tại không trừ chi tiết thêm, bỏ qua citation, không chấm bám nguồn.
- `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` §1 "Thước đạt", §6 "Thước còn thiếu".
- `data/muc_tieu_san_pham_2026-10-28/doi_chieu_nghien_cuu.md` §1 mục 8–10, §3 "Mới".
- `skills/run-experiment/SKILL.md` §1–§2.
- Hai script khả thi (`b87_ctx_check.py` `7f4c8ded626b`, `b87_safety_count.py` `28303fea2f24`): đọc code, chạy lại (0 USD; trước khi chạy đã kiểm không có lượt đo latency nào
  đang chạy theo handoff).

## 2. Bốn điểm A hỏi

**(1) Judge đọc ngữ cảnh thay vì đáp án mẫu — đúng hướng cho "bịa thêm".**
- Bịa thêm = chi tiết không có căn cứ trong đúng phần model đã đọc, nên phải so với **ngữ cảnh**, không so với Golden. Judge hiện tại không làm được việc này: nó ghi rõ không
  trừ chi tiết thêm (`judge_prompt.md:13-15`).
- Ngữ cảnh dựng lại khả thi và đã kiểm: C chạy lại `b87_ctx_check.py` ⇒ top-10 trùng 176 / 176, số nguồn trùng 176 / 176, chênh token vào giữa API và ước trên máy **= 41 ở
  mọi câu**.
- Chỗ yếu là **báo nhầm** (judge gắn "không có" cho ý thật ra có căn cứ): xem M-1.

**(2) Phép kiểm người chấm.**
- **Đo recall được.** Chèn 20 ý bịa (đổi số 10 + câu lạc đề 10) + 5 điều kiện sai, biết chắc đáp án, trộn mù.
- **Không đo được báo nhầm trên câu thật.** 10 câu âm là câu chép nguyên văn ngữ cảnh — quá dễ (M-1).
- **Có thể lộ đáp án**, nếu bản gốc và bản chèn của cùng một câu vào cùng một judge: judge thấy hai câu trả lời chỉ khác một con số (m-1).
- **Cần sửa:** kappa giữa hai judge cùng model đo **độ nhất quán**, không đo **độ đúng** (M-1). P0 chỉ 5 câu chèn thì yếu (m-2).

**(3) Thước an toàn trên ~30 câu Golden.**
- C chạy lại `b87_safety_count.py`: 30 câu trong phạm vi có từ khóa ở câu hỏi hoặc đáp án (26 câu số chính); chỉ **17** câu (không tính 1 câu ngoài kho) có từ khóa **ở câu hỏi**.
- Từ khóa rộng: "mở cửa" 6, "cấm" 6, "trẻ em" 3, "mưa" 3… Nhiều câu hỏi giờ / giá chứ không phải điều kiện có hậu quả.
- ⇒ Trên Golden, P0 chỉ đủ làm **mốc + theo dõi**. "0 P0_sai" trên ~25–30 câu cho cận trên ~10–12 % — đúng như plan tự ghi. Không đủ làm sàn.
- Thước khả thi duy nhất cho sàn P0 là **bộ câu an toàn riêng** (plan §8) — xem trả lời câu 2 dưới.

**(4) Hai câu B hỏi A — ý kiến C:**
1. **Judge thứ 3 (đa số).** Đồng ý, nhưng báo **cả hai số**: đa số (số chính) và "một trong hai judge gắn" (cận trên, thiên về bắt lỗi). Riêng **P0_sai**, dùng "một trong hai" làm
   số chính: lỗi nặng nhất, thà báo dư rồi người đọc loại bớt.
2. **Bộ câu an toàn tự viết.** C nghiêng **làm ngay sau khi thước nhận** (§4 đạt), không chờ thêm số trên Golden:
   - Golden chỉ cho cận trên ~10–12 % — câu trả lời đã biết trước;
   - bộ 20–30 câu tự viết tốn ≈ 0,006 USD;
   - P0 là mức lỗi User xếp nặng nhất.
   A / User quyết; plan ghi lựa chọn.

## 3. Findings

### M-1 (major) — phép kiểm người chấm không đo **báo nhầm trên câu trả lời thật**, nên thước có thể được "nhận" trong khi H bị thổi phồng

- **Vị trí:** §4 `controls.negative` (10 câu chép nguyên văn), `accept.báo_nhầm_âm`, `accept.đồng_thuận` (kappa ≥ 0,6); §3 bước 1–2 (tách ý, nhãn).
- **Yêu cầu:** `run-experiment` §2 (kiểm người chấm trước khi chấm hàng loạt bằng rubric mới — phiếu "đã biết mức" phải giống loại câu sẽ chấm); BAO_CAO_DANH_GIA §6 ("bịa
  thêm" là lỗi nặng nhì ⇒ số sai theo hướng nào cũng đổi quyết định); nghiên cứu §3 "Mới" (kiểm judge bằng người, báo false-pass).
- **Bằng chứng:**
  - (a) Câu âm chép nguyên văn ngữ cảnh: mọi ý trùng chữ, nên judge gần như chắc gắn "có". Câu trả lời thật thì **diễn đạt lại, gộp hai nguồn, so sánh, tính chênh lệch** (ví dụ
    "rẻ hơn X đồng" từ hai giá trong ngữ cảnh), và chính các ý loại này dễ bị gắn "không có" nhầm. Rubric §3 chưa có luật cho **ý suy ra** (tính từ ngữ cảnh, không nói thẳng).
  - (b) Hai judge cùng model, cùng rubric ⇒ kappa ≥ 0,6 chỉ cho thấy hai lần chấm **giống nhau**; nếu cùng hiểu sai một loại ý (ví dụ cùng coi phép so sánh là "không có") thì kappa
    vẫn cao.
  - (c) Mẫu người 20 item "không chặn".
  - ⇒ Không có lớp nào trong cổng nhận đo báo nhầm trên câu giống câu thật.
- **Tác động:** H (đề xuất làm sàn ở §5) có thể cao giả. Một biến thể sau làm câu trả lời diễn đạt khác đi có thể "vỡ sàn" vì nhầm của judge, không vì bịa.
- **Tiêu chí đóng** (gộp được, đều 0 USD):
  1. **Rubric thêm luật ý suy ra:** ý tính được trực tiếp từ ngữ cảnh (cộng / trừ / so sánh hai giá trị có trong ngữ cảnh, gộp hai nguồn) ⇒ `có`, ghi các `n`. Ý chỉ đúng khi biết
     thêm ngoài ngữ cảnh ⇒ `không có`.
  2. **Kiểm chéo bằng code trên toàn bộ 145 câu thật** cho phần đo được bằng máy. Với mỗi ý có **con số** (giá, giờ, năm, khoảng cách), so judge với code: số đó có xuất hiện trong
     ngữ cảnh không (chuẩn hóa dấu chấm / phẩy, đơn vị). Báo hai bảng chéo:
     - judge `không có` mà code thấy số trong ngữ cảnh — ứng viên báo nhầm;
     - judge `có` mà code không thấy — ứng viên bỏ sót hoặc ý suy ra.
     Plan §8 ghi "khớp số bằng code 27/10 đã thử, chưa cần"; ở đây cần nó làm **thước kiểm judge**, không phải thước chính.
  3. **Câu âm giống thật:** thay 10 câu chép nguyên văn bằng (hoặc thêm) ≥ 10 câu **diễn đạt lại / gộp / so sánh**. Có thể là câu trả lời thật mà kiểm chéo bằng code (mục 2) thấy mọi
     ý có số đều có trong ngữ cảnh, và người kiểm (C) đọc xác nhận không có ý ngoài ngữ cảnh. Thêm cổng nhận `báo_nhầm_thật ≤ 1 / 10`.
  4. Ghi trước: kappa là **điều kiện cần**, không phải bằng chứng đúng. Số H / P0 vẫn **tạm** tới khi có mẫu người (như plan đã ghi).

### m-1 — đối chứng có thể lộ: bản gốc và bản chèn của cùng câu cùng vào một judge

- **Vị trí:** §4 `controls.positive` (chèn vào **câu trả lời thật**), §6 bước 3 (trộn 145 + 35, lô ~12 item, mỗi agent ≤ 2 lô).
- **Bằng chứng:** câu chèn = câu thật đổi đúng một số hoặc thêm một câu. Nếu cùng agent đọc cả hai, chỉ cần so hai câu là thấy chỗ chèn ⇒ recall cao giả. Ngược lại, judge có thể
  gắn "có" cho ý chèn vì thấy nó giống câu kia.
- **Đóng:** harness xếp lô sao cho **bản gốc và mọi bản chèn của cùng `case_index` không nằm trong lô của cùng một agent**. Sub-agent không có trí nhớ chung, nên tách theo agent là
  đủ. Kiểm bằng máy, ghi vào `accept.json`.

### m-2 — P0: 5 câu chèn quá ít để đo recall; ghi rõ P0 trên Golden chỉ là mốc

- **Vị trí:** §4 `controls.p0_positive` (5), `accept.recall_P0` (≥ 4 / 5); §5 (P0_sai mới = 0 làm sàn).
- **Bằng chứng:** 4 / 5 ⇒ Wilson 95 % cho recall ≈ [0,38; 0,96] — không phân biệt được judge tốt với judge bắt được một nửa. 30 câu có từ khóa chủ yếu là giờ / giá (§2 (3)).
- **Đóng:**
  - tăng câu chèn P0 lên **≥ 10** (đổi giờ đóng cửa, đổi đối tượng miễn vé, bỏ chữ "không" trong một câu cấm…), ngưỡng ≥ 9 / 10;
  - §5 ghi rõ: sàn P0 chỉ đặt **sau** khi có bộ câu an toàn riêng; trên Golden, P0_sai là mốc + theo dõi.

### m-3 — kappa ở tỉ lệ thấp không ổn định; báo thêm số đi kèm

- **Vị trí:** `accept.đồng_thuận` (kappa H ≥ 0,6 trên 145 câu).
- **Bằng chứng:** nếu H thật ~5–10 % (plan ước 10–20 %), kappa dao động mạnh khi chỉ đổi vài câu, và có thể < 0,6 dù hai judge đồng ý > 95 % câu.
- **Đóng:** ghi trước — báo kappa **kèm** tỉ lệ đồng ý thô và tỉ lệ H của mỗi judge. Nếu kappa < 0,6 mà đồng ý thô ≥ 95 % và H < 10 %, xem bất đồng từng câu trước khi coi là trượt
  (trọng tài đã có trong plan).

### m-4 — ghi thêm "trích nhầm nguồn" (rẻ, cùng nhãn)

- **Vị trí:** §3 bước 2 (judge ghi `n` cho ý `có`).
- **Đóng:** script so `n` judge tìm thấy với `[n]` câu trả lời gắn cho ý đó (nếu câu có gắn) ⇒ chỉ số theo dõi "ý có căn cứ nhưng trích nhầm nguồn". Bộ kiểm citation hôm nay chỉ kiểm định
  dạng / id hợp lệ (`backend/llm/citations.py:19-35`), không kiểm id có đúng ý không. Không thêm lượt chấm.

## 4. Cách người kiểm chạy lại thật

Từ `backend/`, 0 USD:

```bash
HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/loi_nang_2026-10-28/tools/b87_safety_count.py
HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/loi_nang_2026-10-28/tools/b87_ctx_check.py
```

## 5. Kết quả quan sát

| Khẳng định của plan | C thấy | Khớp |
|---|---|---|
| ngữ cảnh dựng lại đúng | top-10 176 / 176, số nguồn 176 / 176, chênh token 41 ở mọi câu (`distinct [41]`) | ✓ |
| 30 câu trong phạm vi có từ khóa an toàn (26 số chính) | 30 / 26; câu hỏi có từ khóa 18 (1 câu ngoài kho); từ khóa nhiều nhất: mở cửa 6, cấm 6, trang phục 3, miễn phí 3, bắt buộc 3, trẻ em 3, mưa 3 | ✓ |
| judge cũ không chấm bám nguồn | `judge_prompt.md:13-16` | ✓ |
| 145 câu có câu trả lời người dùng thấy | 158 − 13 từ chối (bước 9: 0 câu 500, 0 lỗi) = 145 | ✓ (harness đếm lại khi chạy) |
| Wilson / "0 trong mẫu" | đúng nghiên cứu §1 mục 10 | ✓ |

## 6. Giới hạn hoặc phần chưa chạy

- Chưa có harness `loi_nang.py` và rubric để đọc (plan chưa chạy); hợp đồng §9 giao C đọc rubric + 10 item khi chạy.
- C không ước H thật trên 145 câu (cần chấm).

## 7. Decision và bước tiếp theo

**changes_requested.** B sửa M-1 (bắt buộc); minor nên gộp vào cùng bản. B báo sha mới ⇒ C kiểm phần sửa ⇒ A duyệt sha. Hai câu §10 của B: ý kiến C ở §2 (4).

## 8. Kiểm phần sửa — bản 2 (sha `d69481b2addb`, 12:35 28/10/2026)

Phạm vi: các chỗ bản 2 ghi ở §12 của plan, cộng §10, §11 (quyết định A). sha tính từ file khớp tin của B.

| Finding | Tiêu chí đóng | Bản 2 | Đóng |
|---|---|---|---|
| M-1 | luật ý suy ra; kiểm chéo số bằng code trên 145 câu; câu âm giống thật ≥ 10, ngưỡng ≤ 1 / 10; kappa là điều kiện cần | §3 bước 2 (cộng / trừ / so sánh / gộp nguồn / đổi đơn vị ⇒ `có`); §3 dòng "kiểm chéo số" + §4 `kiểm_chéo_số ≤ 5 %` + bảng ngược; §4 `negative_real` ≥ 10 (code thấy mọi số + **C đọc xác nhận trước khi chấm**), `báo_nhầm_thật ≤ 1 / 10`; `đồng_thuận.note` ghi điều kiện cần; số tạm tới mẫu người | ✓ |
| m-1 | bản gốc / bản chèn không chung agent, kiểm bằng máy | §4 `separation`, `tách_lô = 0` trong accept; §6 bước 4 | ✓ |
| m-2 | P0 chèn ≥ 10, ngưỡng ≥ 9 / 10; sàn P0 chỉ sau bộ câu an toàn | §4, §5, §7 | ✓ |
| m-3 | kappa kèm đồng ý thô + tỉ lệ H mỗi judge | §4 `đồng_thuận.note` (kèm luật xem bất đồng trước khi coi trượt) | ✓ |
| m-4 | theo dõi trích nhầm nguồn | §3 bảng chỉ số | ✓ |
| §10, §11 | — | A quyết: judge thứ 3, báo đa số + "một trong hai", P0 dùng "một trong hai"; bộ câu an toàn 20–30 câu + 3–5 câu ngoài kho, chạy sau khi thước qua §4, ≈ 0,006 USD, trần 0,01; B viết câu, C kiểm câu trước khi sinh | ✓ (khớp ý kiến C §2 (4)) |

**Ghi chú mới (n-1, không chặn):** cổng `kiểm_chéo_số` đếm "judge gắn `không có` mà code **thấy** số trong ngữ cảnh" là báo nhầm. Nhưng số có trong ngữ cảnh chưa chắc cùng nghĩa: cùng
mức giá có thể là của mục khác, cùng năm có thể của sự kiện khác. Khi đó judge đúng, code trùng ngẫu nhiên ⇒ cổng có thể trượt oan.
- Gợi ý: nếu cổng trượt, người kiểm (C) đọc các ứng viên, chia "judge sai" / "trùng số ngẫu nhiên", rồi tính lại tỉ lệ chỉ trên "judge sai" **trước khi** sửa rubric. Ghi luật này
  vào `accept` khi viết harness — không cần bản plan mới.

Kết luận bản 2: **ready_for_user_confirmation** — A duyệt sha `d69481b2addb`. Trước khi B chấm, C đọc xác nhận ≥ 10 câu âm giống thật (§6 bước 3 của plan).
