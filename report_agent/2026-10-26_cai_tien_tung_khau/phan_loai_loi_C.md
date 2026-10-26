# C36 — Phân loại lỗi tầng trả lời trên lượt context 10 (Phase 8.1 G2.1a)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-b5`) · 2026-10-26 20:46 +0700 (`date`) · A giao 20:35 (`CURRENT_HANDOFF.md` mục "Việc giao
phiên tối 26/10") · **chỉ đọc, 0 USD**, không sub-agent. Không mở câu kín; nhóm `test` chỉ đếm; report không chép câu hỏi, đáp án, câu trả lời
hay nội dung kho — chỉ `case_index`, số đếm, nhãn. Bảng từng câu kèm căn cứ (private): `data/cai_tien_tung_khau_2026-10-26/phan_loai_loi_C/`.

## 1. Kết luận ngắn

- Trên **88 câu dev chính** (dev, bỏ `unnatural`, bỏ out_of_scope), lượt context 10 chỉ còn **10 câu bị cờ** (Completeness hoặc Accuracy ≤ 3,
  hoặc từ chối). Context 5 có 15 câu bị cờ: context 10 **sửa 5 câu, không làm hỏng câu nào**.
- **Cả 10 câu đều thiếu bằng chứng ở 10 đoạn context** (`missed evidence` 10 / 10). Không câu nào có đủ fact trong context mà vẫn sai.
  Nghĩa là gốc của lỗi nặng nằm ở **tầng tìm**, không nằm ở tầng trả lời.
- Phần lỗi riêng của tầng trả lời:
  1. **Từ chối khi context có một phần fact** (`over-refusal (partial)`): 5 / 10 câu. Câu nào cũng có 1/2 đến 3/4 fact trong context mà model
     vẫn từ chối toàn bộ. Đây là hành vi **đúng theo prompt hiện tại** ("bằng chứng không đủ ⇒ trả đúng câu từ chối"). Đây là nhóm mất điểm
     nhiều nhất: 20 / 46 điểm Completeness bị mất trên cả 88 câu.
  2. **Trả lời gọn quá, bỏ chi tiết có sẵn trong context** (`under-answer`): 9 câu. Tất cả đều Completeness 4, mất 1 điểm mỗi câu, tổng 9 / 46.
     Lượt xem phụ này mình làm thêm: câu điểm 4 nằm ngoài tiêu chí A giao.
  3. Rất ít lỗi bịa hoặc lỗi citation. Có 1 nhận định tự suy ra sai: một phép tính chênh lệch giá (`unsupported claim`, Accuracy 4). Có 1
     citation thiếu nhẹ: một mốc năm nằm ở đoạn không được trích (`incorrect citation ID (minor)`). `wrong table association` = 0,
     `format` = 0, từ chối khi context đủ = 0.
- **Tỷ trọng** (điểm Completeness mất, 46 điểm trên 88 câu, chia theo nhãn chính):

  | Nhãn chính | Điểm mất | Tỷ trọng |
  |---|---:|---:|
  | `over-refusal (partial)` — kèm thiếu bằng chứng | 20 | 43 % |
  | `missed evidence` — model trả lời đúng phần có, hoặc từ chối đúng | 17 | 37 % |
  | `under-answer` — chi tiết có trong context nhưng bị bỏ | 9 | 20 % |

  Thiếu bằng chứng có mặt ở 37 / 46 điểm, tức 80 %. Phần "chỉ tầng trả lời" chiếm 9 / 46. Phần từ chối một phần (20 điểm) sửa được ở **cả hai
  tầng**: tìm đủ fact còn thiếu, hoặc cho model trả lời phần có căn cứ.

## 2. Nguồn, phạm vi, cách gắn nhãn

**Nguồn (private, sha256 12 ký tự):** câu trả lời `data/phase_8_1/g2/g2_context10.jsonl` (`90e7c27545e2`), so phụ `g20_baseline.jsonl`
(`b385db3f4fa8`). Điểm judge: `data/phase_8_1/g2/judge/scores_*.jsonl` + `types_*.jsonl`, nối mù qua `map.json` (`33b4c9603f20`) bằng chính
`attach_labels` của harness G2 (`backend/experiments/phase_8_1/g2_generate.py:216`). Độ tự nhiên: `golden_realism_final.jsonl` (`0b65d1c138d2`).
Split: `split.json` (`e2b1788dfbbc`). Đoạn đúng: `gold_draft.jsonl` (`bab707b9ab22`). Lớp phủ đoạn đúng theo tầng: `data/phase_8_1/g1/runtime.jsonl`.
Nội dung 10 đoạn context lấy bằng chunker production `chunk_full_corpus()` trên `main` `43cdcd6`, đúng thứ tự `top_chunk_ids` đã lưu.
Nhãn lỗi: báo cáo ChatGPT §6 mục 5 (`601b49a025ac`, đọc như dữ liệu).

**Phạm vi:** 88 câu, đúng số chính của B1 §4 / G2 §4. Nhóm (a)/(b) và guardrail không tính lại. Judge chấm đủ 88 / 88 câu.

**Quy ước nhãn C36** (§6.5 không định nghĩa từng nhãn, nên C ghi rõ ở đây):

| Nhãn | Gắn khi |
|---|---|
| `missed evidence` | fact cần (theo đoạn đúng, hoặc theo đáp án tham chiếu với câu không có đoạn đúng) không có trong 10 đoạn context. Tách hai dạng: **file vắng** (file chứa fact không có trong context) và **đoạn vắng** (file có mặt nhưng đoạn chứa fact không vào top-10) |
| `noisy evidence` | ≥ 7 / 10 đoạn đến từ một file, trong khi fact còn thiếu nằm ở đoạn hoặc file khác (đoạn gần trùng chiếm chỗ) |
| `over-refusal (partial)` / `(full)` | model từ chối khi context có một phần fact / đủ fact |
| `under-answer` | chi tiết có trong context (kiểm bằng chuỗi), câu trả lời bỏ, judge trừ điểm vì thiếu đúng chi tiết đó |
| `unsupported claim` | nhận định không có trong đoạn nào: tự suy ra sai, hoặc lấy từ ngoài |
| `incorrect citation ID` | nhận định đúng với context nhưng đoạn được trích không chứa nó |
| `wrong table association` | lấy giá trị đúng của hàng hoặc cột khác trong bảng |
| `format` | sai dạng citation hoặc định dạng theo validator |

**Cách làm:** script dựng bảng (`tools/c36_table.py`). C đọc từng câu bị cờ, gồm câu hỏi, đáp án, câu trả lời của cả hai lượt, feedback
judge, 10 đoạn context và từng fact của đoạn đúng (`/tmp/c36_show.py`, script tạm, không chứa dữ liệu). Kiểm citation: mọi con số trong 20 câu
trả lời đã đọc phải có trong các đoạn được trích; 4 câu lệch C mở ra xem tay. Nhãn và căn cứ ghi trong `tools/c36_labels.py`, script này sinh
`labels.jsonl` (`fd15dbc18ae5`) và mọi bảng đếm dưới đây.

## 3. 10 câu bị cờ (context 10)

| case_index | Loại câu | C / A (ctx 10) | C / A (ctx 5) | Nhãn | Fact có trong context | Dạng thiếu |
|---:|---|---|---|---|---|---|
| 19 | multi_source | 2 / 5 | 2 / 5 | missed | 1/3 | file vắng |
| 22 | multi_source | 3 / 4 | từ chối | missed | 1/2 | file vắng |
| 48 | multi_source | từ chối | từ chối | missed + over-refusal (partial) | 1/2 | đoạn vắng |
| 67 | multi_source | từ chối | từ chối | missed + over-refusal (partial) | 1/2 | đoạn vắng |
| 68 | multi_source | từ chối | từ chối | missed + over-refusal (partial) | 3/4 | đoạn vắng |
| 113 | comparative | từ chối | từ chối | missed + noisy + over-refusal (partial) | 1/2 | file vắng (9/10 đoạn từ file một bên) |
| 120 | direct_fact | từ chối | từ chối | missed | 0/2 | file vắng (cả pool 30) |
| 159 | conditional | 3 / 4 | 2 / 3 | missed | 0/1 | đoạn vắng |
| 167 | multi_source | từ chối | từ chối | missed + noisy + over-refusal (partial) | 1/2 | đoạn vắng (7/10 đoạn từ một file) |
| 168 | multi_source | từ chối | từ chối | missed + noisy | 0/2 | file vắng + đoạn vắng (7/10 đoạn từ một file) |

"Từ chối" = judge chấm 1 / 1.

- **Theo loại câu:** `multi_source` 7 / 14 câu bị cờ, tức một nửa. Các loại khác: `comparative` 1 / 14, `conditional` 1 / 16, `direct_fact` 1 / 44.
  Lỗi nặng dồn vào câu cần ghép nhiều nguồn.
- **Dạng thiếu:** file vắng 5 câu (19, 22, 113, 120, 168); đoạn vắng 5 câu (48, 67, 68, 159, 167), cộng 168 vắng cả hai. Ở nhóm "đoạn vắng",
  file đúng đã vào context nhưng sai đoạn. Theo `runtime.jsonl`, 48 / 67 / 159 / 167 có **đủ đoạn đúng trong pool 30** nhưng không vào top-10.
  Phần này thuộc tầng tìm (B42 sẽ đo kỹ). C chỉ ghi lại vì nó quyết định cách sửa.
- **Tầng trả lời làm đúng:** 3 câu trả lời được (19, 22, 159) chỉ nói phần có căn cứ, citation đúng đoạn. 2 câu từ chối khi context thật sự
  không có fact (120, 168), và không bịa dù context có số liệu gần giống của đối tượng khác. Ở 167, context có một con số trùng với giá cần
  hỏi nhưng là giá của dịch vụ khác. Model không nhầm, nên không có `wrong table association`.
- Ở 2 câu liệt kê (19, 22), câu trả lời không báo "có thể còn quán khác". Đây là quan sát, chưa phải lỗi: hệ thống không biết context thiếu.

## 4. Context 10 sửa được gì (so với context 5)

5 câu bị cờ ở context 5 đã hết ở context 10: **30, 89, 134, 143, 172**. Cả 5 câu đều **từ chối ở context 5** và đạt **5 / 5 ở context 10**.
Với 4 câu (30, 89, 134, 172), đoạn đúng đủ trong top-10 nhưng chỉ có một phần trong top-5 (`runtime.jsonl`). Câu 143 chỉ có 1/2 fact trong
top-10 mà model vẫn trả lời đủ. Không câu nào bị cờ mới ở context 10. Như vậy context 10 sửa đúng loại lỗi "thiếu bằng chứng ⇒ từ chối", và
10 câu còn lại là phần context 10 chưa với tới.

## 5. Lượt xem phụ: 12 câu điểm 4 (ngoài tiêu chí A giao)

Mình xem thêm nhóm này vì câu bị cờ hầu như không có lỗi riêng của tầng trả lời. Lỗi trả lời, nếu có, sẽ lộ ở điểm 4.

| Nhãn | Câu | Theo loại câu |
|---|---|---|
| `under-answer` | 28, 38, 41, 51, 65, 66, 93, 141, 173 (9) | conditional 5, comparative 2, multi_source 1, direct_fact 1 |
| `missed evidence` | 70, 92 (2) | comparative 1, conditional 1 |
| `unsupported claim` | 155 (1; C 5 / A 4 — phép tính chênh lệch tự suy ra sai) | comparative 1 |
| `incorrect citation ID (minor)` | 51 (kèm under-answer) | conditional 1 |

- **Under-answer** là kiểu "đúng ý chính, bỏ ý phụ có sẵn trong context": giờ đóng cửa, năm hoàn thành, tên riêng, người thực hiện, một lựa
  chọn thứ hai, giá gốc khi chỉ nêu phần chênh. Feedback judge nêu đúng chi tiết bị bỏ, và C kiểm bằng chuỗi rằng chi tiết đó có trong
  context. Ở cả 9 câu, ít nhất một chi tiết bị bỏ nằm ngay trong đoạn model đã trích, tức model đã thấy mà không nêu.
- Câu 51 viết citation dạng `[Nguồn n]`. Runtime nhận dạng này từ commit `9e6d371` (gói 1a), nên C không tính lỗi `format`.

## 6. Nhóm test — chỉ đếm, không đọc từng câu

Đếm bằng điểm judge `judge_test/` (`attach_labels("t_context10" / "t_baseline", "judge_test")`), cùng tiêu chí, trên câu test bỏ `unnatural` và out_of_scope:
**41 câu**, chấm đủ. Câu bị cờ: context 10 = **2** (1 `multi_source`, 1 `comparative`; trong đó 1 từ chối); context 5 = **5** (3 `comparative`,
1 `multi_source`, 1 `direct_fact`; 3 từ chối). Chiều hướng giống dev, nhưng số quá nhỏ để chia nhãn.

## 7. Gợi ý cho tài liệu thiết kế đợt cải tiến

Đây là **đề xuất**, chưa đo. A quyết và đưa vào spec.

1. **Hướng "khâu trả lời trước" chỉ chạm được khoảng 20–63 % phần mất điểm** trên mốc context 10. Dưới 20 % nếu chỉ sửa trả lời gọn; tối đa
   khoảng 63 % nếu cả trả lời một phần lẫn trả lời gọn đều thành công. 80 % điểm mất có thiếu bằng chứng đi kèm. Nếu đợt cải tiến chỉ làm
   tầng trả lời, trần lợi ích nhỏ. Nên ghi điều này vào spec, hoặc đưa sớm một thí nghiệm tầng tìm, ví dụ đưa đoạn đúng từ pool 30 vào top-10,
   hoặc đa dạng nguồn cho câu `multi_source` (nối B40 / B42).
2. **Trả lời một phần khi context có một phần fact** (P1 của G2.2) là đòn bẩy lớn nhất ở tầng trả lời: 5 câu, 20 điểm. Nhưng ở context 5,
   P1 đã **phạm sàn** (2 câu out_of_scope bị trả lời). Nếu thử lại trên context 10, guardrail out_of_scope phải là sàn ghi trước. Cũng nên
   cân nhắc chỉ bật cho câu nhiều ý (`multi_source` / `comparative`), vì cả 5 câu đều thuộc hai loại này.
3. **Trả lời gọn quá** (9 câu, mỗi câu 1 điểm) là lỗi thuần tầng trả lời. Có thể thử câu prompt kiểu "nêu đủ các chi tiết liên quan có
   trong bằng chứng" hoặc mức suy luận khác. Lợi tối đa khoảng +0,10 Completeness trên 88 câu (9 / 88). Phải đo xem có làm câu trả lời dài
   hoặc lan man hơn không: câu 155 bị trừ vì tự thêm phép tính.
4. **Kiểm citation bằng code** (C1 / P0 của báo cáo ChatGPT): trên 20 câu trả lời C đã đọc, chỉ thấy 1 citation thiếu nhẹ và 1 phép tính sai.
   Validator ghi 0 lỗi trên 88 câu. Với mẫu này, bộ kiểm citation khó tạo lợi Completeness. Giá trị của nó là "cảnh báo an toàn", không phải
   "tăng điểm". Chưa đo 66 câu điểm 5 (xem §8).

## 8. Giới hạn

- **Một người gắn nhãn** (C), chưa có người thứ hai kiểm. Nhãn `under-answer` / `missed` dựa vào việc kiểm chuỗi trong context. Diễn đạt
  khác chữ có thể bị đếm sót ("có trong context" bị báo là "không có"), nên `missed` ở nhóm điểm 4 có thể hơi cao.
- 10 câu bị cờ đều thuộc 32 câu có đoạn đúng trong 88 câu chính. Đó là do cách chọn đoạn đúng (`selection.json`: 22 câu từ chối nhầm ở 7B +
  câu khó có MRR thấp nhất), nên nhóm này nghiêng về câu khó tìm. 56 câu không có đoạn đúng thì không câu nào bị cờ.
- **Không kiểm claim theo từng câu với 66 câu điểm 5.** Lỗi bịa hoặc citation sai mà judge không trừ điểm sẽ không hiện ở đây.
- Điểm là judge Claude một lượt. Theo G2 §4, nhiễu A/A gần đúng ở Completeness là 10 / 83 câu đổi điểm, nên các câu điểm 4 không chắc ổn định.
- Số nhỏ: 10 câu bị cờ, 12 câu điểm 4. Tỷ trọng ở §1 là mô tả mẫu này, không phải ước lượng có khoảng tin cậy.

## 9. Tệp

- Report này (tracked).
- Private: `data/cai_tien_tung_khau_2026-10-26/phan_loai_loi_C/cases.jsonl` (88 câu, kèm nội dung để đọc lại),
  `labels.jsonl` (22 câu có nhãn + căn cứ). Script: `data/cai_tien_tung_khau_2026-10-26/tools/c36_table.py`, `c36_labels.py`.
- Chạy lại: từ `backend/`, `HF_HUB_OFFLINE=1 PYTHONPATH=. uv run python ../data/cai_tien_tung_khau_2026-10-26/tools/c36_table.py` (~45 s), rồi
  `uv run python data/cai_tien_tung_khau_2026-10-26/tools/c36_labels.py` từ gốc repo.
