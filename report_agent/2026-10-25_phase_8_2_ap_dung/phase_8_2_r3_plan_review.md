# Review: plan Phase 8.2 §10 — R3, câu prompt "nêu đủ chi tiết có trong bằng chứng"

Decision: **changes_requested** (0 blocker / 1 major / 2 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 22:19 +0700 (`date`)
Bản được kiểm: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r3_plan.md` sha `c613f524ea10` (B, untracked)
Căn cứ: đúng mục "Căn cứ để review" của plan:
1. spec §10.2–§10.4 bản `cd910c4c4169`;
2. C37 §3–§5;
3. C36 §5;
4. plan R2 `b70ea775efb2` §2–§3.

Tính lại từ `data/phase_8_2/b1/` (plan cho phép), `uv run`, chỉ đọc, 0 USD. Câu A trả lời §6 (qua tin của A cho C): đồng ý chữ R3, trần 0,05 USD,
quyền ghi khi duyệt.

**Tự kiểm phần của mình:** R3 là đề xuất của C (C37), còn 9 câu U là nhãn C gắn (C36). C chỉ kiểm plan có dùng đúng các nguồn đó cho **mốc B1**
hay không. C không đánh giá lại đề xuất của mình.

## 1. Phạm vi đã review

Toàn bộ plan: lớp bài toán, chữ R3, giả định G1–G4, YAML, luật giữ, cỡ mẫu, cách chạy, tiền, quan hệ với R2, §6. Đối chiếu với spec §10.2 (luật (i),
"đo tốc độ theo khâu", sàn, Holm {R2, R3} cố định) và dòng R3 ở §10.3.

## 2. Findings

### M-1 (major) — Giả định G2 kiểm được ngay và sai một phần: trần thật trên mốc B1 là 6 câu U, không phải 9

- **Vị trí:** plan §1 bảng giả định dòng G2 ("*giả định*: phần lớn 9 câu còn điểm 4 ở B1; harness in điểm B1 … ở bước judge"); §2 cỡ mẫu ("trần
  là 9 câu U … thực tế cần ≥ 8 thắng / 1 thua").
- **Yêu cầu:** `run-experiment` §1.2 ("kiểm giả định bằng máy **trước** khi code") và §1.6 ("đếm số câu thật sự có thể đổi kết quả … đừng chạy
  rồi mới thấy").
- **Bằng chứng** (C tính từ `data/phase_8_2/b1/judge/`: map `runs` b1 / g21a, `scores_*`, dev chính 88; 0 USD):
  - Điểm Completeness của B1 ở 9 câu U: 28 → **5**, 38 → 4, 41 → **5**, 51 → 4, 65 → 4, 66 → 4, 93 → **5**, 141 → 4, 173 → 4. Như vậy chỉ
    **6 / 9** câu còn chỗ +1 ở mốc B1.
  - Cả dev chính B1 chỉ có **7** câu điểm 4: 38, 51, 65, 66, **92**, 141, 173. Câu 92 thuộc nhóm thiếu bằng chứng (C36 §5), R3 không thêm fact được.
  - Các câu điểm ≤ 3 không phải từ chối (3 + 1 câu) đều là thiếu bằng chứng (C36 §3).
- **Tác động:** với Holm họ 2, cần ≥ 5 thắng / 0 thua (p 0,013). 8 / 1 (p 0,015) **không thể đạt** khi trần chỉ 6–7. Nhiễu A/A dev chính
  thường cho khoảng 1 câu tụt (B1 §4). Nghĩa là R3 gần như phải cứu **5 / 6 câu U mà không tụt câu nào**. Xác suất "chưa rõ" cao hơn plan
  đang ghi. Với User nhạy chi phí, A cần con số đúng để quyết có chi 0,04 USD hay không.
- **Tiêu chí đóng:**
  - G2 ghi kết quả đã kiểm: 6 / 9 câu U còn điểm 4 ở B1; dev chính có 7 câu điểm 4.
  - Mục cỡ mẫu ghi trần **6** (tối đa 7) và "cần ≥ 5 / 0; 8 / 1 không đạt được".
  - Bảng p của B giữ nguyên. C tính lại và **khớp** cả 7 dòng: 4 / 0 0,031; 5 / 0 0,013; 5 / 1 0,131; 6 / 1 0,063; 7 / 1 0,036; 8 / 1 0,015; 9 / 2 0,036.
  - A quyết chạy hay không theo số mới.

### m-1 (minor) — R4 của B1 đã có file ra; `r4_numbers` từ chối ghi đè

- Plan §3 bước 7: "R4 trên B1 + R3". `data/phase_8_2/r4/b1_{dev,test}.jsonl` đã có từ C39, mà `main()` của `r4_numbers` (`2c7ecfd`) từ chối khi
  file ra đã tồn tại.
- **Tiêu chí đóng:** plan ghi "B1: dùng lại `data/phase_8_2/r4/b1_*.jsonl` (C39, cùng đầu vào); chỉ chạy R4 trên file R3". Không đổi tiêu chí.

### m-2 (minor) — Vế "mỗi chi tiết kèm citation" có thể đổi cách trích; nên theo dõi số citation

- Chữ R3 thêm một ràng buộc mới về citation, ngoài ý "nêu đủ". Validator v2 bắt lỗi định dạng (mức tụt +2 câu), nhưng **không** bắt việc trích
  nhiều hơn hoặc trích sai đoạn. R4 bắt một phần (số).
- **Tiêu chí đóng:** thêm dòng theo dõi "số `[n]` khác nhau mỗi câu, TB R3 / B1 (dev 120)". Tính bằng `CITATION_PATTERN`, 0 USD. Chữ R3 **không
  sửa** (A đã đồng ý).

## 3. Đã kiểm, đạt

- **Đổi đúng một thứ:** chèn một câu trước `_REFUSAL_RULE`, luật từ chối giữ nguyên. `_REFUSAL_RULE` có trong prompt ở `811d25d`: harness R2 của
  C import ở `811d25d` qua đúng `assert` này (`g2_generate.py:58`).
- **Sàn** (OOS 0 / 18; 120 / 168 vẫn từ chối; 0 lỗi 500 / kỹ thuật) khớp spec §10.2 và plan R2.
- **Chỉ số quyết:** `paired_stats(a_values=B1, b_values=R3, 'completeness')` cùng thứ tự `case_index`, dev chính 88; CI > 0 và Holm họ {R2, R3} cố
  định (p × 2 < 0,05). Đúng spec §10.2 và đúng chữ ký hàm.
- **Mức tụt:** Accuracy 4 / 5; Completeness test 6; từ chối nhầm +1 / +1; citation v2 +2 (tính lại cả hai lượt); USD +20 %, 0 lần gọi API thêm;
  `output_tokens` +20 %. Khớp spec §10.2 và bảng A/A (C41).
- **Ghi trước** "R3 có thể vượt +20 % token ra ⇒ trình User": đúng luật (i) và nguyên tắc chất lượng trước.
- **Tiền:** ≈ 0,040, trần 0,05; pilot ước lại; dừng sớm ở bước 3 ≈ 0,005. Hợp spec §10.4.
- **Quan hệ R2 / ghép:** so cùng mốc; ghép là lượt riêng. Đúng spec.

## 4. Cách người kiểm tính lại

`uv run python -` (inline, chỉ đọc), từ `backend/`:
- `bootstrap_mean_diff` cho 7 tỷ lệ thắng / thua (n 88);
- điểm Completeness B1 từ `data/phase_8_2/b1/judge/` (`map.json` `runs` b1, `scores_*`) trên dev chính (split + realism, bỏ OOS);
- đếm phân bố điểm.

Kiểm thêm `data/phase_8_2/r4/` có sẵn file B1.

## 5. Giới hạn

- Điểm B1 dùng ở M-1 là lượt chấm `b1/judge`. Khi chạy R3, B1 sẽ được chấm lại cùng lượt mù với R3, nên điểm B1 có thể đổi 1–2 câu (A/A judge).
  Trần 6 vì thế là ước, có thể là 5–7.
- `r3.py` chưa có, nên C mới chỉ kiểm thiết kế.

## 6. Decision

**changes_requested:** sửa M-1 (G2 + cỡ mẫu theo số B1); m-1, m-2 cùng lượt. Ra sha mới ⇒ C kiểm phần sửa ⇒ A ghi "duyệt bản sha". A quyết chạy
R3 tối nay hay không, theo trần thật 6 câu và giờ kết phiên của User.
