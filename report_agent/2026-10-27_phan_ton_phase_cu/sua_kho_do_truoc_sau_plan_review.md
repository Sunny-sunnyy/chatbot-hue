# Review: plan đo "trước ↔ sau" đợt sửa kho (B78)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 6 minor) — bản sha `7b79c3971bc7`
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C72
Date: 09:45 28/10/2026 (`date`)
Canonical guide: spec sửa kho `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (sha file `937cf8969810`, User duyệt) §2, §5, §6, §7;
spec 8.2 §10.2, §11
Implementation report: (plan) `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_do_truoc_sau_plan.md`

## 1. Phạm vi đã review

Chỉ theo gói "Căn cứ để review" của plan (`WORKFLOW.md` §9.1). Không đọc STATUS_B hay tin của B ngoài tin báo sha.
- Plan (đọc hết), spec sửa kho §2, §5 (bước 0–12, "Dừng + khôi phục"), §6, §7; spec 8.2 §10.2, §11; skill `run-experiment` §1–§4.
- Code `main` `510e1a8` / `62c284f` (backend giống nhau): `full_corpus_eval.py:162-164, :322-364, :367-386`; `chat.py:128-144, :177-189`; `app.py:161-165`;
  `full_corpus_judge_prompt.md:10-31`; `retrieval/full_corpus_context.py:50-68, :80-100`.
- Chạy lại 3 script đếm của B (đọc code trước, sha khớp plan) và 3 kiểm riêng của C (§3).
- A dặn xét kỹ: (1) F2 có đo đúng lỗi nặng nhất không; (2) cách tách câu chạm / không chạm; (3) 3 câu hỏi §8. Trả lời ở §2 (mục "Ba điểm A hỏi").

## 2. Findings

Không có blocker hay major. Mọi số đếm trong plan tái lập được (§4).

### Ba điểm A hỏi

**(1) F2 "nói chắc sai".** Định nghĩa đếm được bằng máy, không chồng với F1 / F3 / F4 ở phía **sàn**, và khớp nhiễu: A/A B1 ↔ G2.1a = 0 / 0. Phân bố Accuracy
của số chính là 1 (8 câu, đúng 8 câu từ chối) / 4 / 5 ⇒ câu có trả lời chưa từng ≤ 3 ⇒ sàn 0 có cơ sở. F2 bắt đúng **"nói ngược đáp án"**. Có hai chỗ sót:
(a) "bịa thêm" — plan đã ghi giới hạn (`judge_prompt.md:13-15`), C đồng ý không thêm thước giữa chừng (§8 câu 2); (b) **sai một chi tiết nhỏ** (số, giờ, giá, tên)
mà judge cho 4 — xem m-1. Với du khách, sai giá hay giờ là "nói chắc sai" dù judge coi là nhỏ.

**(2) Câu chạm / không chạm.** Làm được bằng máy, không cần đọc nội dung:
- `evidence_parts` trong payload có `start` / `end` theo ký tự của file nguồn lúc build ⇒ luật (b) dùng offset file backup, luật (c) dùng offset file đã sửa.
- "Context = `top_chunk_ids[:context_sources]`" chỉ đúng khi builder không bỏ đoạn nào (`full_corpus_context.py:60-61` bỏ đoạn không có evidence). C đếm:
  **0 / 8.459** đoạn thiếu evidence ⇒ đúng trên index hiện tại. Với index "sau" cần kiểm lại (m-3).
- 123 edit hiện có: 0 `new` rỗng, 0 `new` ngắn hơn 12 ký tự, 0 `new` đã xuất hiện > 1 lần trong file gốc ⇒ luật (c) hôm nay không phình. Edit từ 16 câu User
  chưa có ⇒ luật cho `new` rỗng chưa định nghĩa (m-3).
- Ước 29 / 129 (mức đoạn) so với 79 / 129 (mức file) tái lập đúng.

**(3) Ba câu hỏi §8.** Câu 1 và câu 3: đồng ý mặc định của B, nhưng cả hai **lệch spec đã duyệt** ⇒ A ghi quyết định (m-4, m-5). Câu 2: đồng ý.

### Minor

**m-1 — Câu Accuracy 4 mới không được đọc.** Vị trí: §4 F2, W2. Yêu cầu bị ảnh hưởng: thứ tự lỗi User 28/10 ("nói chắc sai" nặng nhất), skill `run-experiment` §2
(câu có số chấm bằng code khi được). Bằng chứng: rubric 4 = "sai lệch nhỏ không đổi kết luận" (`judge_prompt.md:28`); W2 chỉ đếm, A/A 6 / 7 câu (trong phạm vi).
Tác động: một câu "sau" sai giá / giờ / tên nhưng judge cho 4 sẽ lọt qua mọi dòng quyết. Thêm vào đó:
- "Mới" sau `rejudge` chưa nói dùng điểm chấm lại của **cả hai** bên hay chỉ bên `sau`.
- Ứng viên F2 thuộc tập chạm có thể là **Golden chưa sửa kịp** (bước 8 sót), không phải chatbot hỏng. Luật xử lý trường hợp này phải ghi **trước**.

Tiêu chí đóng:
- Thêm một dòng watch "Accuracy 5 ⇒ 4 mới" (cùng câu, trong phạm vi, có trả lời). C đọc hết các câu này cùng các câu F2, ghi từng câu "sai fact (số / giờ / tên…)" hoặc
  "khác cách diễn đạt"; câu sai fact báo A trong report (không phải sàn).
- Ghi rõ "mới" = điểm `rejudge` của cả hai item.
- Ghi luật cho trường hợp Golden sót: ứng viên F2 chạm mà C xác nhận câu trả lời khớp kho đã sửa còn Golden thì chưa ⇒ ghi riêng, chuyển mục Golden đợt 2, A trình User.

**m-2 — Câu "không chồng" chưa đúng hẳn.** Vị trí: §4 dòng "Không chồng" và đoạn "Luật chấm câu 500 citation". Bằng chứng: một câu 500 citation mới bị đếm ở F4 **và** là
một câu tụt ở T1 / T2 (gán 1). Một câu F2 mới cũng là câu tụt Accuracy ở T2. F1 lấy `refusal == false` nên câu ngoài kho có `citation_error` vào cả F1 lẫn F4. Tác động
hiện tại nhỏ: các sàn đều là 0, nên khi sàn vỡ thì kết luận đã là "làm hỏng". Nhưng nếu A / User chọn giữ sau khi F4 vỡ (§8 câu 1), T1 / T2 sẽ tính câu đó lần
nữa. Tiêu chí đóng: sửa câu "không chồng" cho đúng; ghi trước rằng câu đã vỡ sàn **không** tính lại vào T1 / T2 khi A / User quyết giữ, hoặc tính — một trong hai.
Ghi F1 cho câu có `citation_error`: hoặc loại khỏi F1 (người dùng thấy 500, không thấy câu trả lời), hoặc nói rõ đếm cả hai.

**m-3 — Luật câu chạm ở hai trường hợp biên.** Vị trí: §3 (c), §2 `preflight --arm sau`. Hai trường hợp:
- edit xóa (`new` rỗng): `str.find("")` khớp ở vị trí 0 ⇒ (c) không có nghĩa;
- index "sau" có đoạn không evidence ⇒ `top_chunk_ids[:context_sources]` không còn là context.

Tiêu chí đóng:
- Ghi luật "`new` rỗng ⇒ chỉ dùng (b) cho edit đó".
- `preflight --arm sau` đếm số đoạn không có evidence của collection mới; phải bằng 0, khác 0 ⇒ dừng. Hoặc lấy context từ `PackedSource` thay vì cắt `top_chunk_ids`.

**m-4 — Chạy bộ "trước" sớm lệch thứ tự spec §2.** Vị trí: §1 "Giả định về chatbot 'trước'", §8 câu 3. Bằng chứng: spec §2: cả đợt chạy **sau** B3 và sau khi User đóng 8.2;
chỉ phần chuẩn bị 0 USD được làm trước. Bước 0 tốn ≈ 0,037 USD và thuộc đợt. C đồng ý chạy sớm: bước 0 chỉ đọc kho, không lẫn vào B3, và có kiểm "còn hiệu lực"
(code runtime, T1, build record). Tiêu chí đóng:
- A ghi duyệt lệch thứ tự này (handoff hoặc ghi chú duyệt), không ngầm hiểu.
- Plan thêm: không chạy bộ "trước" cùng lúc với B3 hay lượt trả phí khác, vì W5 (`wall_ms` tuần tự) sẽ lệch.

**m-5 — "A trình User trước khi khôi phục" là đổi spec §5.** Vị trí: §4 "Kết luận", §8 câu 1. Bằng chứng: spec §5 "Dừng + khôi phục": sàn §6 vỡ ⇒ dừng; khôi phục.
C đồng ý mặc định của B. Về số: 14 / 1.600 câu còn lỗi citation sau sửa 1a là gộp **cả các biến thể** (prompt P1 / P2, reasoning none / low / high —
`report_agent/2026-10-25_ra_soat_code/sua_1a_implementation.md:40, :63`). Cấu hình production context 10: 0 / 352 lần gọi (A/A, `b78_cit.py`). Tức F4 vỡ vì nhiễu
là có thể, nhưng không chắc. Tiêu chí đóng:
- A ghi quyết định đổi bước khôi phục (User duyệt nếu A coi là đổi spec).
- Tùy chọn (C gợi ý, ≈ 0,0002 USD / câu): khi F4 vỡ, sinh lại đúng câu đó **một lần** ở bên `sau` (file mới, giữ cả hai, không thay dòng), kèm nhãn context
  giống / khác. Đây là bằng chứng cho User chọn giữ hay khôi phục, không phải retry để PASS. Bên `trước` không sinh lại được vì index cũ đã xóa.

**m-6 — Lệnh T1 nạp key thừa.** Vị trí: §5 mục 1. `full_corpus_eval retrieval` không gọi API trả phí. Tiêu chí đóng: bỏ `--env-file ../.env` khỏi lệnh này
(luật: chỉ nạp env khi việc cần).

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, Qdrant `:6335` thật (chỉ đọc), không key, 0 USD:

```bash
sha256sum ../data/sua_kho_2026-10-27/tools/b78_{counts,cit,touched}.py      # 010037f7d9dd / feb413b57979 / 7c3ade66174d — khớp plan
for x in counts cit touched; do HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/sua_kho_2026-10-27/tools/b78_$x.py; done
```

Kiểm riêng của C (script inline, chỉ in số):
- scroll toàn collection lấy `evidence_parts` ⇒ đếm đoạn không có evidence;
- đọc `edits/*.jsonl` + `diffs_them/edits_them.jsonl` ⇒ đếm `new` rỗng / ngắn / lặp trong file gốc;
- grep `1.600` trong report rà code 1a.

## 4. Kết quả quan sát

| Khẳng định của plan | C thấy | Khớp |
|---|---|---|
| 176 / 18 OOS / 158 / số chính 129; độ tự nhiên 82 / 65 / 29 | `b78_counts`: đúng các số đó | ✓ |
| A/A số chính: Completeness 4 / 124 / 1, Accuracy 3 / 124 / 2 ⇒ A/A = 2 ⇒ mức tụt 5 | đúng; trong phạm vi 4 / 153 / 1 và 3 / 153 / 2; 176: 4 / 171 / 1, 3 / 171 / 2 | ✓ |
| Từ chối đổi 0; OOS bị trả lời 0 / 0 | `refusal flips` 0 (cả 3 tập); `oos answered` 0 / 0 | ✓ |
| "Nói chắc sai" A/A 0 / 0 | `ncs acc<=3` 0 / 0 ở số chính lẫn trong phạm vi; Accuracy số chính B1 {1: 8, 4: 4, 5: 117}, G2.1a {1: 8, 4: 5, 5: 116}; câu từ chối số chính 8 / 8 | ✓ |
| W2 Accuracy 4 có trả lời A/A 6 / 7 (158) | `acc4 non-refusal` 6 / 7 | ✓ |
| Lỗi citation validator hiện tại 0 / 0 | `b78_cit`: B1 0, G2.1a 0 (176 mỗi bên) | ✓ |
| 123 edit / 65 file / 0 `old` không thấy; 114 đoạn chạm + 33 đoạn danh mục ⇒ 29 / 129; mức file 79 / 129 | `b78_touched`: đúng; chunk 8.459, 0 lỗi | ✓ |
| Tiền 0,0369 USD / bên | 291.269 × 0,1 / 1M + 15.585 × 0,5 / 1M = 0,02913 + 0,00779 = 0,0369 | ✓ |
| Dòng code dẫn trong plan | `is_refusal` `:162-164`; `answer_case` `:322-364` (lỗi ⇒ `error` `:362`); `chat.py:128-135, :140-144, :177-189`; `app.py:161-165`; rubric `:29-31`, chi tiết thêm `:13-15`, bỏ dấu trích dẫn `:16` | ✓ |
| (thêm) context = `top_chunk_ids[:context_sources]` | 0 / 8.459 đoạn không evidence ⇒ builder không bỏ đoạn; vỡ ngân sách chỉ `break` ⇒ vẫn là tiền tố | ✓ (index hiện tại) |
| (thêm) luật (c) không phình | 0 `new` rỗng, 0 `new` < 12 ký tự, 0 `new` đã có > 1 lần trong file gốc | ✓ (123 edit hiện có) |

Ý nghĩa: số nền của plan (A/A, cỡ tập, tiền, ước câu chạm) đúng. Tiêu chí bám spec §6, có hai chỗ chặt hơn spec: TB kiểm thêm trên tập không chạm, và T3 từ chối nhầm.
Phần còn mở là cách xử lý khi sàn vỡ và chỗ sót của F2 — đều là quyết định / ghi chú, không phải lỗi đo.

## 5. Giới hạn hoặc phần chưa chạy

- Chưa có harness `truoc_sau.py` để đọc (plan chưa chạy): hợp đồng §7 giao C đọc diff harness khi có.
- Không kiểm "cùng đầu vào từng token" giữa B1 ↔ G2.1a. Nguồn A/A này spec §6 đã ghi và User đã duyệt.
- Không đọc nội dung Golden, kho hay câu trả lời: chỉ chạy script in số.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Plan đo được đúng câu spec §6 hỏi, số nền tái lập được. Còn 6 minor; B có thể gộp vào bản sau, C kiểm phần sửa. A cần quyết hai lệch spec:
- m-4: chạy bước 0 trước B3 / trước khi đóng 8.2;
- m-5: "A trình User trước khi khôi phục" thay cho khôi phục ngay khi sàn vỡ.

A cũng chọn có lấy dòng watch m-1 không. C khuyên lấy: 0 USD, chỉ thêm việc đọc vài câu, và đúng loại lỗi User xếp nặng nhất.
