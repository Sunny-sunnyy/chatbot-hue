# Review: B93 bước 2–6 — áp đợt 2 sửa kho (kiểm từng bước)

Người kiểm: C (Claude Opus 5.5, `hue-rag-0e`) · Việc: A giao 30/10 (kiểm từng bước B93). Người làm: B (`hue-rag-24`). Plan `sua_kho_dot2_do_plan.md` bản 3 `5f30ac7eac16` §6.
Chỉ đọc; 0 USD. File tracked chỉ ghi sha / số đếm (không chữ kho). Mỗi bước một mục, ghi ngay khi kiểm xong.

## Bước 2 — áp edit (13:12 30/10/2026 `date`): `ready` 0 / 0 / 0

Script C: `data/sua_kho_2026-10-27/dot2/tools/c_check_b2.py` (`8aa50cd69d08`, chỉ đọc; áp lại `dot2.jsonl` lên **backup** trong bộ nhớ, so kho).

| Kiểm | Kết quả |
|---|---|
| sha `dot2.jsonl` = bản A duyệt `c0b5876ea510` | ✓ |
| 40 file sửa: backup `knowledge-base-hue/meta/backup_sua_kho_dot2_2026-10-30/` + 123 edit theo thứ tự = kho hiện tại, **từng byte** | 40 / 40 ✓ (40 / 40 khác backup) |
| 164 file còn lại: sha256 kho = sha trong build record trước đợt 2 (`dot2/backup/`, `574b5d02088b`) | 164 / 164 ✓ — không file nào ngoài danh sách bị đổi; 40 + 164 = 204 = số file record |
| `dot2/applied_edits_dot2.jsonl` (`60c8721812c9`): 123 dòng, (file, old, new) đúng thứ tự `dot2.jsonl` | ✓ |
| `dump-headings --arm truoc` chạy **trước bước 5** (plan bản 3 §6 bước 2): `dot2/eval_truoc/headings_truoc.json` (`c19bdaeab3b3`) — 1 file, 81 đoạn; đoạn dưới 2 tiêu đề cũ: **4 và 6** | ✓ — trùng số C thử trên Qdrant ở C85 vòng 2 (4 / 6) |
| Qdrant: vẫn đúng 1 collection runtime (chưa tới bước 5); `git status` không có file tracked của B đổi | ✓ |

Số B tự báo (khớp): 123 edit / 20 mục / 40 file, 2 edit xóa dòng; 119 / 121 chuỗi `new` khác rỗng còn nguyên trong kho, 2 chuỗi bị edit sau sửa tiếp trên cùng dòng (đúng thứ tự áp — script C áp tuần tự nên đã gồm).

## Bước 4–6 — chia đoạn, build, T1, cổng ổn định (13:38 30/10/2026 `date`): `ready` 0 / 0 / 0

C chạy độc lập **sau** build (không chồng CPU), script tạm `/tmp/c93/` (xóa khi xong; chỉ in số đếm).

| Kiểm | Kết quả |
|---|---|
| Build record mới `51fb1ec63cbc`: `chunk_count` 8.424, 204 nguồn; sha256 cả 204 file = kho hiện tại | 204 / 204 ✓ |
| Sparse state mới `c8134c49a648` (kho đổi ⇒ đổi là đúng) | ✓ |
| Qdrant: đúng 1 collection runtime, **8.424** point | ✓ |
| Chia đoạn chạy lại bằng chunker production (`prepare_full_corpus_input`): 8.424 đoạn, 0 lỗi | ✓ |
| Token lớn nhất trên đoạn thật: e5-small **366 / 512**, e5-base **366 / 512**, huydang **255 / 256** | ✓ (sát trần huydang như đợt 1, không vượt) |
| `chunk_id` so `chunks_truoc.json`: mất đúng 2 id cuối của 2 file Phố đi bộ (`#52`, `#63`), 0 id mới; chỉ 2 file đó có id lệch ⇒ đúng hiện tượng "dồn số" B báo | ✓ |
| File hướng dẫn nghệ thuật biểu diễn (Qdrant scroll chỉ đọc ↔ `headings_truoc.json`): 81 đoạn, **cùng tập `chunk_id`**, **10 / 81** đổi `heading_path` (= 4 + 6) | ✓ |
| **T1 chạy lại** (`evaluation.full_corpus_eval retrieval`) ⇒ sha **`4d5bbe9e0edc`**, **giống từng byte** `dot2/eval_sau/t1_sau.jsonl` | ✓ |
| T1 mới ↔ T1 cũ `23c58c47635d`: **25 / 158** đổi top-10; **24** có đoạn của file đã sửa (bên trước hoặc sau); 1 không chạm: câu 88 — chỉ đổi đoạn **hạng 10**, keyword 100 → 100, MRR 0,583 → 0,583 | ✓ — cùng kiểu đợt 1: kho đổi ⇒ sparse state (IDF toàn kho) đổi ⇒ thứ hạng đuôi xê dịch [suy ra từ sparse sha đổi + 2 đoạn bớt; không đo IDF từng từ] |
| TB T1 cũ → mới: keyword 92,35 → 92,35; MRR 0,7216 → 0,7216; nDCG 0,7552 → 0,7554 | ✓ không tụt |
| Câu có đoạn 2 file Phố đi bộ trong top-10 (bên nào cũng được): 3 / 158 | để biết cỡ tập luật "f" |
| Cổng ổn định `dot2/eval_sau/gate_dot2.json` (`9bc840d2b143`): `/` 200; `/health` 5 / 5 ready; 1 câu trong kho 200, 2 nguồn, có `[n]`; 1 câu ngoài kho 200 + từ chối, 0 nguồn; 2 dòng `chat_metrics` mới, 0 câu hỏi trong log | ✓ (đọc file B ghi; C không chạy lại server) |

## Luật chạm "f" + plan "Sửa đổi" §10 (13:38 30/10/2026): `ready` 0 / 0 / 1

- `truoc_sau.py` `58351a493a04` (`touched()`): `deleted_line_files` = file có edit `new` rỗng trong `--applied` ⇒ đợt 2 đúng **2 file Phố đi bộ**; "f" khi context **trước hoặc sau**
  có đoạn thuộc 2 file (tra `source` qua `chunks_<arm>.json` từng bên ⇒ id dồn số vẫn ra đúng file) ✓ bắt đủ hai bên. Chỉ **thêm** nhãn "f"; nhánh (a)–(e) không đổi ✓.
- **Đợt 1 không đổi:** `applied_edits.jsonl` đợt 1 có 0 edit `new` rỗng. C chạy `touched` trên **bản sao tạm** dữ liệu đợt 1 bằng code mới **và** bằng bản `truoc_b90/` (trước B90): ra **cùng
  sha `8483819aed72`** ⇒ code mới trung tính với đợt 1. (Cả hai ra 44 câu so với `touched.json` đợt 1 là 43 — khác ở câu 132 lý do (c), vì (c) đọc kho **hiện tại** (nay là kho sau
  đợt 2) để tìm chỗ `new`; đúng thiết kế, không phải lỗi; `touched.json` đợt 1 không bị ghi đè.)
- Plan `fb2afe68e12d` vs bản A duyệt `5f30ac7eac16` (`git show 751b352`): **chỉ thêm** 11 dòng §10; sàn F1–F4, A1–A2, mức tụt T1–T3 không đổi ✓.
- **m-1 (§10 câu "luật chặt hơn"):** không hẳn — câu thuộc tập chạm **ra khỏi** phép kiểm "TB ≥ −0,1 trên tập không chạm" và khỏi danh sách C đọc ("tìm đổi đoạn không chạm"). Cỡ nhỏ
  (≈ 3 câu theo T1). **Đóng khi:** sửa câu thành "cần để tránh nhãn sai do dồn số; cái giá: ≤ vài câu rời tập không chạm" **và** C đọc câu trả lời hai bên của mọi câu chỉ có lý do "f"
  (như câu "tìm đổi đoạn"). Không chặn bước 9.

## Bước 7 — gold v5 (13:38 30/10/2026): `ready` 0 / 0 / 0 (còn chờ User duyệt 1 đề xuất)

- `build_gold_v5.py` `f32266a27fa4` ↔ `build_gold_v4.py`: chỉ đổi hằng (nguồn v4, backup đợt 2, `applied_edits_dot2.jsonl`, đầu ra v5, kiểm thêm v3 không đổi) + docstring ✓.
- `gold_v4.jsonl` vẫn `927bae1bf201` ✓. Đề xuất duy nhất (`gold_v5_proposals.json` `d26d0a97c7ad`): câu 172, edit order 98 (K129), không nới; C tính lại = áp đúng edit đó lên trích dẫn cũ
  ⇒ **trùng** `proposed_quote`; xuất hiện **1 lần** trong kho hiện tại ✓. `gold_v5_draft.jsonl` `33d16fd6b8f4`.

## Plan bản `2adef0d4e5fc` + gold v5 + bước 8 (13:42 30/10/2026 `date`): `ready` 0 / 0 / 0

- **Plan:** diff với bản A duyệt `5f30ac7eac16` (`git show 751b352`) = chỉ §10 (11 dòng thêm); so với nội dung §10 C đọc ở bản `fb2afe68e12d`, khác **đúng một gạch** "Vì sao không phải đổi
  tiêu chí…": bỏ "luật chặt hơn", ghi câu chạm ra khỏi phép kiểm tập không chạm + **bù: C đọc câu trả lời hai bên của mọi câu chỉ có lý do (f)** ⇒ m-1 **đóng**. Các gạch khác giữ nguyên chữ.
- **Gold v5:** `gold_v5.jsonl` `33d16fd6b8f4` = `gold_v5_draft.jsonl` (`cmp` giống byte); v4 `927bae1bf201` không đổi ✓ (User duyệt đề xuất câu 172 13:39 theo B).
- **Bước 8 quét Golden** (`dot2/golden_de_xuat_dot2.md` `856fcf061fd5`): Golden md5 vẫn `0f7dbf41b422` (chưa sửa — chờ User) ✓; 39 câu ứng viên ⇒ 3 gói sub-agent ⇒ **sửa 2 / không 37**
  (đếm lại từ `result_*.jsonl`: 39 dòng, 37 "không", 2 "sửa") ✓. **C quét độc lập** (khác cách B): với mỗi edit lấy cụm bị bỏ / thay (so từ, ≥ 2 từ hoặc có chữ số) ⇒ tìm trong
  đáp án mẫu + keyword (NFC, `casefold`) ⇒ 4 câu (5, 25, 51, 81) — **cả 4 nằm trong 39 ứng viên của B**; câu 25, 51, 81 sub-agent ghi "không" với lý do khớp chữ ngẫu nhiên / chủ đề
  khác — hợp lý (cụm khớp là chữ chung như "3 năm", "Chỉ"). 0 câu Golden còn chữ "quận" (câu hỏi + đáp án + keyword) ✓. Hai đề xuất (câu 5 bỏ tên phường; câu 127 thêm "khoảng")
  đúng hướng edit; chọn phương án là việc của User.

## Sửa Golden theo User (2 câu) (13:52 30/10/2026 `date`): `ready` 0 / 0 / 0

- md5 bản sao lưu (`knowledge-base-hue/meta/golden_backup_dot2_2026-10-30/`) = `0f7dbf41b422` (= md5 cũ) ✓; Golden mới **`6331e88fb171`**.
- So từng dòng thô: 177 dòng hai bên; **chỉ dòng câu 5 và câu 127** khác; ở cả hai chỉ trường `reference_answer` đổi (`question`, `keywords`, `category` giống); phần còn lại của dòng giống byte
  (thứ tự khóa, escape giữ) ✓.
- Câu 5: **xóa đúng** một cụm 17 ký tự (tên phường cũ, theo lựa chọn User) — không thêm gì ✓. Câu 127: **chèn đúng** chữ "khoảng" (7 ký tự gồm khoảng trắng) trước số nhà ✓.
- Smoke 10 câu không chứa 2 câu này (B); `test_golden_full_corpus.py` 8 pass (B — C không chạy lại, W31 đang đo).

## Bước 9 — phần C đọc (bắt đầu 14:06 30/10/2026 `date`)

**Lượt sinh "sau" (đọc file, không chạy lại):** `dot2/eval_sau/sau.jsonl` 176 / 176 câu (đủ 0–175), 0 lỗi, 0 lỗi citation, 30 từ chối (tính cả câu ngoài kho); meta `gpt-6-luna`, context 10, commit
`751b352` — `git diff 748c1e3 751b352 -- backend/` (trừ tests / experiments) rỗng ⇒ cùng code runtime với bộ "trước" ✓; 0,0367199 USD.

**Nhóm "vé / điều kiện vào"** (plan §5; D2, Q2, Q5, Q14, Q15): script tạm `/tmp/c94/ve.py` — lấy đoạn context "sau" từng câu từ Qdrant (chỉ đọc, 1.396 đoạn), tìm 50 ký tự đầu của `new`
(bỏ dấu Markdown) — kiểm phép tìm: mỗi `new` tìm thấy đúng trong đoạn của chính file đó (6 / 6).
- Golden "sau": **0 câu** có đoạn chứa `new` của 5 mục này trong context.
- Bộ an toàn "sau": **1 câu (S12)**, chạm D2. C đọc hai bên (B89 ↔ "sau"): "sau" **giữ đúng điều kiện** (miễn phí ngày đó cho công dân Việt Nam + giấy tờ xuất trình) và bỏ câu
  "các nguồn chưa thống nhất" của B89 (chính kiểu P0_sai "nói sai về nguồn" của S12 ở B89), chỉ còn lưu ý mềm về mức phí chung; ngày bị D2 bỏ không xuất hiện trong câu trả lời ⇒ không
  phải lỗi do D2. Watch A thêm "đem cảnh báo của nơi khác áp cho nơi được hỏi": không thấy ở S12.

### Bước 9 — kiểm số + đọc hai bên (14:21 30/10/2026 `date`): `ready_for_user_confirmation` 0 / 0 / 1

Đầu vào (sha C tính): report `sua_kho_dot2_implementation.md` `f6dbbc59375e`; `dot2/analyze.json` `0bcf53e35946`; `dot2/touched.json` `8abdfb9f09c6`; `an_toan/dot2_2026-10-30/compare.json`
`674f469fa05d`; `an_toan_dot2.py` `bb2c3d1e22e1`; `golden_scan_dot2.py` `d6bc4004dda7`; danh sách đọc `dot2/c_doc_lists.json` `8e86097d22ad`.

**Tính lại bằng máy:**
- `touched` + `analyze` chạy lại trên **bản sao tạm** (`/tmp/c95/`, cùng code `58351a493a04`, cùng nhãn chấm) ⇒ `touched.json` `8abdfb9f09c6` và `analyze.json` `0bcf53e35946` **giống từng byte**
  bản của B ⇒ số F1–F4, T1–T3, W1–W8 trong report khớp file. touched 32: (a) 2, (b) 27, (c) 25, (d) 0, (e) 1, (f) 3; T1 Completeness +0,0078 [−0,031; +0,047], 4 / 122 / 3.
- Bộ an toàn: `an_toan_dot2.py check` judge 1 + 2: 77 / 77 nhãn, 0 thiếu / thừa / lỗi; cổng đối chứng (`accept_judge{1,2}.json`): recall P0 10 / 10 (đảo cảnh báo 5 / 5) cả hai, báo nhầm 0 / 5 và
  1 / 5, tách lô 0 ⇒ đạt. `compare.json`: ngoài kho bị trả lời 0; P0_sai B89 {S11, S12} ⇒ "sau" ∅, **mới 0**; sinh lại mốc S11 / S12 0 / 3 mỗi câu; H mới 0; 2 judge bất đồng 0.
- Diff script: `an_toan_dot2.py` ↔ `an_toan_aa.py`: bỏ phần sinh (không gọi API), nguồn = r1 (B89) + "sau" + 3 lượt sinh lại + đối chứng, `N_AGENTS` 6 + chặn "nhiều bản hơn agent", `compare`
  đếm "mới ở sau" theo plan §5 (`write_new` từ chối ghi đè) ✓. `golden_scan_dot2.py` ↔ `golden_scan.py`: chỉ đổi đường dẫn record / đầu ra + `encoding` + mở `"x"` ✓.

**Đọc hai bên** (câu trả lời "trước" ↔ "sau" + điểm hai bên; tả ở mức loại câu):

| Câu (loại) | Vì sao đọc | Context | Đọc thấy | Kết luận |
|---|---|---|---|---|
| 133 (nhiều nguồn, năm khai trương) | chỉ lý do (f) | khác (đoạn Phố đi bộ dồn id) | hai bên cùng hai năm, cùng nguồn; 5 / 5 / 5 cả hai | giữ đúng |
| 137 (so sánh, giờ cấm xe) | chỉ lý do (f) | khác | hai bên cùng giờ cấm xe của hai nơi, đúng kho; 5 / 5 / 5 | giữ đúng điều kiện |
| 23 (có điều kiện, giờ mở cửa quán) | tụt Completeness 5 → 4, "nhiễu" | giống | cùng kết luận "không mở" + giờ nghỉ trưa; "sau" bớt một chi tiết giờ buổi sáng | nhiễu sinh / chấm, không lỗi kho |
| 112 (có điều kiện, vật dụng được phép) | tụt Completeness 5 → 4, "nhiễu" | giống | "sau" bỏ vế liệt kê chất liệu **không** được dùng — thiếu ý về một quy định (M4) | nhiễu sinh (context giống từng đoạn) — ghi watch |
| 138 (so sánh, diện tích) | tụt Accuracy 5 → 4, "nhiễu" | giống | "sau" ghi một **khoảng** số thay vì một số; khoảng đó **có trong kho** (file đầm, `grep_kb.sh`) — không bịa | nhiễu sinh |
| 159 (có điều kiện, có diễn mỗi tối) | tụt Completeness 3 → 2, "fact đã sửa" | khác **1 đoạn**: đoạn có lời nhắc kiểm tra thời tiết rơi khỏi context, thay bằng đoạn file hướng dẫn nghệ thuật biểu diễn (file có 2 edit tiêu đề) | "sau" vẫn giữ điều kiện "chỉ diễn khi đủ điều kiện xuất bến", mất câu nhắc thời tiết; cả hai bên đều chưa nói mùa mưa lũ như đáp án mẫu | **tìm đổi đoạn do sửa kho** (thứ hạng đổi), thiếu ý M4, không đảo điều kiện — m-1 |
| S12 (an toàn, miễn vé) | nhóm vé | khác | xem mục "Nhóm vé" trên: giữ đúng điều kiện, bỏ lỗi "nói sai về nguồn" | giữ đúng |
| S10 (an toàn, miễn vé theo chiều cao) | P0_thiếu mới (A3) | **giống** | hai bên cùng nội dung (được miễn theo chiều cao, có nguồn); cờ chỉ ở bên "sau", một judge | nhiễu chấm, không do kho |

- A3 P0_thiếu đổi 5 câu: 3 câu context **giống** hai bên (S10 mới; S03, S15 mất) ⇒ nhiễu sinh / chấm; 2 câu context khác (S12, S19) đều **mất** cờ ⇒ không câu nào tệ đi vì kho.
- W9 (5 câu có context chứa chỗ làm yếu): 0 câu tụt Completeness ⇒ theo plan không phải đọc; C không đọc thêm.
- Watch A thêm ("đem cảnh báo của nơi khác áp cho nơi được hỏi"): **không thấy** ở 8 câu đã đọc.

**m-1 (report §2 "Câu tụt"):** câu 159 ghi "fact đã sửa" theo nhãn máy, nhưng đọc hai bên thì nguyên nhân là **context đổi 1 đoạn** (đoạn có lời nhắc thời tiết bị đẩy ra) — kiểu "tìm đổi
đoạn do sửa kho", không phải "câu chữ đã sửa làm câu trả lời kém". **Đóng khi:** report thêm một dòng tả đúng như vậy (loại câu, không chép chữ), và ghi watch "câu nhắc điều kiện thời
tiết có thể rơi khỏi top-10 khi thứ hạng đổi" cho đợt sau. Không đổi kết luận "không làm hỏng" (T1 4 / 3 trong mức; không sàn nào chạm).

**Kết luận bước 9:** `ready_for_user_confirmation` 0 / 0 / 1 — "không làm hỏng" đứng: số tính lại khớp byte; 8 câu đọc hai bên không có lỗi do kho mới ngoài một câu thiếu ý (159, M4).

**m-1 — đóng** (14:23 30/10/2026 `date`): report `8fae5afe6d16` §2 (dòng 56–58) tả đúng câu 159 (đổi 1 đoạn ngữ cảnh, đoạn nhắc thời tiết bị đẩy khỏi top-10, câu trả lời thiếu ý thời tiết) + watch cho đợt sau;
quét trùng 0. Gợi ý chữ (không chặn): "0 lỗi do kho" nên đọc là "0 lỗi **nội dung** kho; 1 câu thiếu ý do **thứ hạng đổi** sau sửa kho" — để User không hiểu là sửa kho không có tác động phụ nào.
**Bước 9 khép: `ready_for_user_confirmation` 0 / 0 / 0.**
