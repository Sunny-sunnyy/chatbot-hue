# Review: Phase 8.2 B3 — mốc cuối trên câu kín (giữ mù)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C74
Date: 10:19 28/10/2026 (`date`)
Canonical guide: plan `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md` (sha file `27e75be5ed44` = bản A duyệt); spec 8.2 §11
Implementation report: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_implementation.md` (B, 10:14 28/10)

**Giữ mù:** C **không** mở câu kín, file câu trả lời, lô chấm hay điểm kèm feedback. C chỉ chạy script in số. Review này chỉ ghi số dòng, số đếm, md5 / sha, token, USD và ms.

## 1. Phạm vi đã review

- Report B3 (đọc hết) và plan §1–§8.
- Script `data/phase_8_2/b3/tools/b3.py` (sha `6615b7310e15`, khớp report), đọc hết 371 dòng để tìm chỗ in nội dung. Kết quả:
  - các lệnh chỉ in số dòng, số đếm, md5, token, USD, ms;
  - `export-judge` ghi nội dung vào lô, nhưng chỉ in số item / số lô;
  - `match-seen` chỉ in và ghi số dòng.
- Validator v1 phát lại (`v1_error`, `b3.py:196-205`) so với `git show f26485b:backend/llm/citations.py`: cùng mẫu `\[(\d+)\]` và cùng thứ tự luật (câu từ chối có marker,
  câu từ chối chuẩn, không marker, id lạ) ⇒ phát lại đúng.
- Dữ liệu `data/phase_8_2/b3/`: các file `meta`, `preflight`, `t1_*`, `a_seen_lines.json` (chỉ đọc trường số); `check.json`, `analyze.json` (so sha).

## 2. Findings

Không có blocker hay major.

**m-1 — Số phụ trong report không do script đã nộp in ra.** Vị trí: report §4 "Số phụ để đọc kết luận". Yêu cầu bị ảnh hưởng: plan §5 mục 7 ("bảng do script in ra, không
gõ tay") và §7 (người review chạy lại được). Bằng chứng: `b3.py` không có lệnh nào in các số sau:
- điểm judge thô;
- tập 29 câu bỏ câu 500;
- điểm thô của 4 câu 500 bên đầu;
- câu thắng theo loại.

C dựng script tạm (`/tmp/c74/watch.py`, chỉ in số, đã xóa) để tính lại. **Mọi số khớp report:**
- thô Completeness +0,364 [+0,091; +0,727] 8 / 24 / 1;
- thô Accuracy +0,242 [+0,030; +0,545] 4 / 29 / 0;
- bỏ câu 500 (n = 29): Completeness +0,448 [+0,138; +0,828] 8 / 21 / 0; Accuracy +0,276 [+0,034; +0,621] 4 / 25 / 0;
- 4 câu 500 bên đầu, điểm thô: (4, 4), (5, 5), (5, 5), (5, 5);
- 12 câu thắng: conditional 5, multi_source 3, direct_fact 2, comparative 2.

Tác động: không đổi kết luận (đây là số theo dõi, đã tái lập). Chỉ là hồ sơ thiếu đường tái lập. Tiêu chí đóng: B lưu script đã dùng vào `data/phase_8_2/b3/tools/`
và ghi sha trong report, hoặc report ghi "số phụ: script tạm, C74 tính lại khớp".

Ghi nhận (không phải finding):
- **Độ tự nhiên khớp theo `line`, không theo `question`.** Plan §4 ghi khớp theo `question` NFC. File `sealed_realism.jsonl` chỉ có khóa `changed`, `line`, `realism`,
  `reason` (C đọc tên khóa của dòng đầu) ⇒ khớp theo `line` là cách duy nhất làm được. Report đã ghi đúng điều này. Kết quả: 0 câu ≠ natural, 0 câu không khớp.
- **Độ mù của judge (giới hạn, C không kiểm vì sẽ phải đọc câu trả lời).** Bên cuối có 10 nguồn nên có thể trích `[6]`…`[10]`, bên đầu thì không. Về nguyên tắc judge
  đoán được nhánh. Judge prompt bỏ qua dấu trích dẫn (`full_corpus_judge_prompt.md:16`) và judge không biết cấu hình nào là mới. Cách chấm này giống các lần so context
  5 ↔ 10 ở 8.1. Đề xuất cho lần sau (ngoài phạm vi): đánh số lại citation trước khi xuất lô.

## 3. Cách người kiểm chạy lại thật

Từ `backend/` của repo chính, 0 USD, không key, Qdrant chỉ đọc. Trước khi chạy, ghi sha `check.json` / `analyze.json` của B
(`data/phase_8_2/b3_c_review/before.txt`):

```bash
for c in check check-judge analyze; do PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/phase_8_2/b3/tools/b3.py $c; done   # stdout ⇒ data/phase_8_2/b3_c_review/<c>.out
md5sum knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl | cut -c1-12
sha256sum data/phase_8_2/b3/t1_{start,end}.jsonl | cut -c1-12
git diff --stat 510e1a8 249d270 -- backend/          # rỗng
uv run python .githooks/overlap_scan.py report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_implementation.md
```

Thêm: đọc trường số của `*.meta.json` và `preflight_*.json`; chạy script tạm `/tmp/c74/watch.py` (đã xóa) cho m-1.

## 4. Kết quả quan sát

| Khẳng định của report | C thấy (lần chạy mới, trừ khi ghi "đọc file") | Khớp |
|---|---|---|
| md5 câu kín / số dòng | `ddc59587b502`; preflight hai nhánh: 36 dòng (đọc file) | ✓ |
| T1 hai worktree giống byte mốc | `t1_start`, `t1_end` sha `cefb2d1ad609` | ✓ |
| Code nạp đúng worktree; HEAD; context | (đọc file) preflight: `module_files_outside_worktree` rỗng cả hai; đầu `f26485b` / 5, cuối `249d270` / 10; 8.459 point; NFC khác 0; > 500 ký tự 0 | ✓ |
| `249d270` backend = `510e1a8` | `git diff --stat` rỗng | ✓ |
| Meta 4 phần | (đọc file) commit / context / số câu / lỗi / USD: start_pilot `f26485b` 5 10 0 0,0014036 · start_rest `f26485b` 5 26 0 0,0041307 · end_pilot `249d270` 10 10 0 0,0021488 · end_rest `249d270` 10 26 0 0,0061294 ⇒ pilot 0,0035524, tổng 0,0138125 | ✓ |
| `match-seen` khớp 1 ⇒ chỉ S36 | (đọc file) `a_seen_lines.json`: n = 1; `analyze`: `a_seen_n` 1, chỉ có tập S36 | ✓ |
| `check` | lỗi 0 / 0; OOS 3, bị trả lời 0 / 0; từ chối trong phạm vi 4 ⇒ 2; câu 500 citation 4 ⇒ 0; C65 bên đầu 4 / 4 (đúng 4 câu 500), bên cuối 5; nguồn TB 5 / 10; token 34.463 / 4.176 và 60.657 / 4.425; USD / câu 0,0001537 / 0,0002299; `wall_ms` p50 / p95 4.885,6 / 9.170,3 và 3.659,2 / 9.066,8 | ✓ |
| `check.json` / `analyze.json` không đổi khi chạy lại | sha trước = sau: `8711c517acb1`, `0ec5a8cd753b` | ✓ |
| `check-judge` | 63 item, 63 điểm, 0 lỗi schema, 0 thiếu, 0 thừa | ✓ |
| `analyze` S36, n trong phạm vi 33 | Completeness 3,606 ⇒ 4,424, **+0,8182** [+0,3939; +1,3333] 12 / 21 / **0**; Accuracy 3,879 ⇒ 4,576, **+0,697** [+0,2727; +1,2121] 8 / 25 / **0**; Relevance +0,1515 [−0,1212; +0,5152] 3 / 27 / 3; OOS bị trả lời (cuối) 0 | ✓ |
| Số phụ (m-1) | khớp hết (§2) | ✓ |
| Report giữ mù | `overlap_scan` 0 trùng (quét cả câu kín); report chỉ có số dòng (pilot), số đếm, loại câu, md5 / sha, token, USD, ms; không tên file nguồn | ✓ |
| Dọn | `git worktree list` không còn `b3_`; không còn `/tmp/b3_*` | ✓ |

**Đối chiếu tiêu chí ghi trước (plan §4) bằng số C chạy lại:**

| Dòng | Ngưỡng | Kết quả | Đạt |
|---|---|---|---|
| sàn OOS bị trả lời (cuối) | 0 | 0 / 3 | ✓ |
| sàn lỗi kỹ thuật | 0 mỗi nhánh | 0 / 0 | ✓ |
| Completeness | TB ≥ −0,1, tụt ≤ 5 | +0,818, tụt 0 | ✓ |
| Accuracy | như trên | +0,697, tụt 0 | ✓ |
| từ chối nhầm | ≤ +1 | −2 | ✓ |
| watch "tốt hơn" | CI > 0 | [+0,394; +1,333] | tốt hơn |

Ý nghĩa: kết luận của B đứng vững theo đúng luật ghi trước. Chatbot cuối 8.2 **không làm hỏng** trên 36 câu kín và **tốt hơn** theo judge. Bỏ 4 câu 500 thì vẫn tốt hơn
với CI > 0, tức lợi không chỉ đến từ bộ kiểm trích dẫn mới.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại lượt sinh có phí (đúng hợp đồng plan §7). Bằng chứng sinh là file của B: meta có commit, context, token.
- Không đọc câu trả lời / feedback ⇒ không kiểm được nội dung judge chấm, cũng không đếm được câu trích `[6]`–`[10]` (giới hạn độ mù ở §2).
- Giới hạn của chính B3 (report đã ghi): chỉ S36; NFC không được thử; judge Claude, chưa có mốc người (B0 làm sau); A/A mượn từ bộ khác; `wall_ms` đo khi gọi đồng thời 4.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** B3 chạy đúng plan đã duyệt; mọi số trong report tái lập được bằng số liệu đã lưu. A viết `TONG_HOP` 8.2 rồi trình User đóng 8.2.

Khi trình User, A nên nói rõ ba giới hạn:
- người chấm là Claude;
- kết luận trên 36 câu, gồm cả 3 câu A đã thấy (máy chỉ khớp được 1 nên không tách ra được);
- trong 36 câu kín, không câu nào gõ ở dạng ký tự tách dấu (NFD) nên chưa thử được phần chuẩn hóa chữ.

m-1 không chặn; B đóng khi tiện.
