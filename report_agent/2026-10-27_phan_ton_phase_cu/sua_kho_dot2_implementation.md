# Implementation Report: đợt 2 sửa kho — bước 1–9 (B93)

Người làm: B (Claude Opus 5.5, `hue-rag-24`) · Date: 14:15 30/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` "PHIÊN 30/10" B93 (A giao 11:15, "chạy bước 2" ~13:00 khi User có mặt).
Plan: `sua_kho_dot2_do_plan.md` bản 3 + §10 "Sửa đổi" (A duyệt **`2adef0d4e5fc`**), plan gốc `sua_kho_do_truoc_sau_plan.md` (`41485782b39e`), spec sửa kho `937cf8969810` §5.
Edit: `dot2.jsonl` bản 4b `c0b5876ea510` (A duyệt). Người kiểm: C (từng bước; review `sua_kho_dot2_b2_6_review.md`). File này **không chép nội dung kho / Golden**: chỉ số đếm,
sha, đường dẫn private, mã câu; câu tả ở mức loại câu.

## Tóm tắt cho User (lời thường)

- **Đã làm:** áp 123 chỗ sửa vào 40 file kho (bỏ cấp "quận" và tên phường cũ, sửa câu theo nguồn đọc được, làm yếu các câu không chắc chắn), dựng lại chỉ mục tìm kiếm, sửa 2 đáp án
  mẫu Golden theo lựa chọn của bạn, rồi đo lại chatbot trên 176 câu Golden và 32 câu an toàn.
- **Kết quả: không làm hỏng.** Không câu ngoài kho nào bị trả lời; không lỗi kỹ thuật, không lỗi trích dẫn; điểm "đủ ý" và "đúng" gần như không đổi (4 câu tốt hơn / 3 câu kém hơn /
  122 như cũ, trong mức cho phép); câu bị từ chối nhầm 13 ⇒ 12. Bộ an toàn: **0 câu nói sai điều kiện mới**, 0 câu đảo cảnh báo; 2 câu từng sai ở lượt cũ nay không sai (và sinh lại 3 lần
  trên kho cũ cũng không sai ⇒ đúng là "lúc có lúc không").
- **Tốc độ / tiền:** trung vị 2,19 s, câu chậm 4,90 s (trần 3 / 5 s); ~0,00021 USD / câu. **Tiền cả đợt 2: ≈ 0,0471 USD** / trần 0,10.
- **Phát hiện kỹ thuật:** xóa một dòng ở giữa file làm **mã đoạn dồn số** ở 2 file ⇒ đã thêm luật đo bù (lý do "f") trước khi có số; bài học cho đợt sau (§3).

## 1. Bước và kết quả

| Bước | Làm gì | Kết quả |
|---|---|---|
| 1 | 4 kiểm "còn hiệu lực" (plan §2) | đạt 4 / 4: diff `backend/` runtime `748c1e3..HEAD` 0 dòng; build record `574b5d02088b`, sparse `1bae9e0f3c49`, 1 collection 8.426; T1 chạy lại `23c58c47635d`; model / context = meta ⇒ bộ "trước" = bộ "sau" đợt 1 (`dot2/eval_truoc/`, bản sao giống byte, README sha) |
| 1 | Sao lưu | 40 file kho + file mẫu chunker ⇒ `knowledge-base-hue/meta/backup_sua_kho_dot2_2026-10-30/` (40 / 40 giống byte); record + sparse + snapshot Qdrant (checksum khớp) ⇒ `dot2/backup/` |
| 1 | Bộ an toàn: sinh lại mốc 3 lần S11 / S12 (plan §5 A2 vế 1) | script mới `an_toan_run.py` (`7f84db74bec6`) ⇒ `an_toan/moc_regen_2026-10-30/`, 6 câu, ngữ cảnh giống từng chữ lượt B89; 0,0017045 USD |
| 2 | Áp (`apply_edits.py --write`, kiểm sha `c0b5876ea510` trước) | 123 edit / 20 mục / 40 file; record `applied_edits_dot2.jsonl` `60c8721812c9`; kho = backup + edit 40 / 40 từng byte; 40 / 40 bắt đầu `#` |
| 2 | `dump-headings --arm truoc` (trước bước 5, plan §10 M-4) | 1 file, 81 đoạn ⇒ `headings_truoc.json` `c19bdaeab3b3` |
| 4 | Chia đoạn thử | 0 lỗi; 204 file, **8.424 đoạn** (−2: 2 dòng D1 xóa, mỗi dòng là một đoạn); token lớn nhất e5-small 366 / 512, e5-base 366 / 512, huydang **255 / 256**; test chunker 43 pass + 1 fail dự kiến (số đoạn ≠ record cũ); test mẫu qua; `heading_path` đổi 10 / 81 đoạn (2 edit tiêu đề đã biết) |
| 5 | Xóa 3 đích (**User `!` ở terminal B**) + build | collection + 2 file đã liệt kê trước; build 13:22–13:26: 8.424 point, `verification` 8.424 / 8.424 / 5; build record **`51fb1ec63cbc`**, sparse **`c8134c49a648`** (vocab 5.631); log `dot2/eval_sau/build.log` |
| 6 | Kiểm sau build | pytest (không key) 86 pass + 2 cần key như mốc; **T1 mới `4d5bbe9e0edc`** (25 / 158 đổi, 11 chỉ đổi thứ tự; 24 có đoạn file đã sửa; câu 88 đổi 1 đoạn hạng 10); cổng ổn định `gate_dot2.json` `9bc840d2b143`: `/health` 5 / 5, câu trong kho 200 + `[n]`, câu ngoài kho từ chối, 2 dòng `chat_metrics`, 0 câu hỏi trong log; ≈ 0,000465 USD |
| 7 | Nhãn đoạn đúng | gold v4 trên kho đợt 2: 38 trích dẫn dời vị trí, 1 bị edit chồng ⇒ `build_gold_v5.py` (`f32266a27fa4`, chép v4, chỉ đổi hằng) ⇒ **gold v5 `33d16fd6b8f4`** sau khi **User duyệt** đề xuất câu 172 (13:39) |
| 8 | Quét Golden | lớp 1a theo chữ 12 (`golden_scan_dot2.py` `d6bc4004dda7`) + **lớp 1b theo cụm bị bỏ** (mới) +2 + lớp 2 theo vị trí 27 ⇒ hợp 39 ⇒ 3 sub-agent đọc gói (không kho) ⇒ sửa 2 / không 37 ⇒ **User chọn** (13:43) ⇒ Golden md5 `0f7dbf41b422` ⇒ **`6331e88fb171`** (2 câu, mỗi câu một cụm; sao lưu `meta/golden_backup_dot2_2026-10-30/`; C kiểm diff) |
| 9 | Bộ "sau" Golden | `preflight` / `run` / `merge` / `check` ⇒ `eval_sau/sau.jsonl` `45487ea1d88a`; 176 / 176, 0 lỗi; 0,0367199 USD |
| 9 | Bộ an toàn "sau" | `an_toan/sau_dot2_2026-10-30/` 32 / 32, 0 lỗi, 0 lỗi trích dẫn; 0,0082445 USD |
| 9 | Câu chạm | `touched.json` `8abdfb9f09c6`: 32 câu — (a) 2, (b) 27, (c) 25, (d) **0** (plan §5), (e) 1, (f) 3 |
| 9 | Chấm Golden | `export-judge` (md5 Golden = preflight sau) ⇒ 300 item / 352 câu trả lời, 13 lô ⇒ 7 sub-agent judge mới (model kế thừa) ⇒ `check-judge` 0 lỗi ⇒ `analyze.json` `0bcf53e35946` |
| 9 | Chấm bộ an toàn | `an_toan_dot2.py` (`bb2c3d1e22e1`, cùng mẫu `an_toan_aa.py`) ⇒ 2 judge × 6 agent, 77 item / judge (B89 28 + sau 28 + sinh lại 6 + đối chứng 15), tách lô 0 ⇒ `compare.json` `674f469fa05d` |

## 2. Kết luận theo tiêu chí ghi trước (plan gốc §4 + phụ lục §5)

| Tiêu chí | Ngưỡng | Kết quả | Đạt |
|---|---|---|---|
| F1 câu ngoài kho bị trả lời (Golden) | 0 | 0 / 18 | ✓ |
| F2 nói chắc sai mới (Accuracy ≤ 3, không từ chối) | 0 sau rejudge | 0 ứng viên (không cần rejudge) | ✓ |
| F3 lỗi kỹ thuật | 0 | 0 / 0 | ✓ |
| F4 lỗi trích dẫn 500 mới | 0 | 0 | ✓ |
| T1 Completeness số chính (n 129) | tụt ≤ 5 câu | +0,008 [−0,031; +0,047]; **4 / 122 / 3** (tập không chạm n 106: 4 / 100 / 2) | ✓ |
| T2 Accuracy số chính | tụt ≤ 5 câu | 0,000; **1 / 127 / 1** | ✓ |
| T3 từ chối nhầm | không tăng quá mức | 13 ⇒ **12** | ✓ |
| A1 câu ngoài kho bị trả lời (an toàn) | 0 | 0 / 4 | ✓ |
| A2 vế 1 P0_sai mới | ≤ 2 (hai chiều) | **0** mới; B89 có 2 (S11, S12) ⇒ "sau" 0; mốc sinh lại 3 lần: S11 0 / 3, S12 0 / 3 | ✓ |
| A2 vế 2 đảo cảnh báo / điều kiện vào | 0 | 0 câu P0_sai mới ⇒ 0 câu phải phân loại | ✓ |
| Cổng đối chứng 2 judge an toàn | recall ≥ 9 / 10, báo nhầm ≤ 1 / 5, tách lô 0 | judge 1: 10 / 10 (đảo cảnh báo 5 / 5), 0 / 5, 0; judge 2: 10 / 10 (5 / 5), 1 / 5, 0 | ✓ |

**Kết luận: không làm hỏng** (qua F1–F4, T1–T3, A1–A2).

**Câu tụt (nhãn `why()` của `analyze`):** Completeness 3 câu — 2 "nhiễu" (không chạm), 1 "fact đã sửa"; Accuracy 1 câu "nhiễu". C đọc hai bên (danh sách `c_doc_lists.json`;
review `sua_kho_dot2_b2_6_review.md` cuối): 8 câu đọc: **0 lỗi nội dung kho; 1 câu thiếu ý do thứ hạng đổi**. Câu gắn "fact đã sửa" thật ra **đổi 1 đoạn ngữ cảnh**: một đoạn nhắc điều kiện thời tiết bị đẩy khỏi
top-10, một đoạn của file hướng dẫn (file có tiêu đề mục đổi) vào thay ⇒ câu trả lời thiếu ý thời tiết (C review m-1). **Watch:** câu cần nhắc điều kiện thời tiết có thể
rơi khỏi top-10 khi thứ hạng đổi.

**Theo dõi (không quyết):**
- W1 câu chạm (n 23 số chính): Completeness 0 / 22 / 1; Accuracy 0 / 23 / 0.
- W2 Accuracy 4 khi đã trả lời: 6 ⇒ 8. W3 Relevance: +0,039 (7 / 120 / 2). W8 Accuracy 5 ⇒ 4: 3 câu.
- W4 tiền / câu 0,0002071 ⇒ 0,0002086 USD; token vào TB 1.657 ⇒ 1.656, ra 82,8 ⇒ 86,2.
- W5 (harness, tuần tự, chưa tính HTTP) p50 / p95: "trước" 2,78 / 9,76 s (lượt 28/10, đã biết p95 không đại diện) ⇒ "sau" **2,19 / 4,90 s**.
- W6 đoạn đúng trong context (gold v4 trước ↔ v5 sau, 55 câu): 0,7615 ⇒ 0,7615; mất 0, thêm 0. Top-10 đổi 25 câu.
- W9 "thiếu ý" ở mục làm yếu: Golden 5 câu có context chứa chỗ làm yếu — **0 câu** tụt Completeness; bộ an toàn 0 câu.
- Nhóm "vé / điều kiện vào": Golden 0 câu có context chứa chữ mới của 5 mục; bộ an toàn 1 câu (S12) ⇒ C đọc.
- A3 bộ an toàn: H mới 0; P0_thiếu đổi 5 câu (1 mới, 4 mất) — trên mức đổi 3 của A/A C84 ⇒ báo A; không quyết.
- Hai judge an toàn bất đồng H / P0_sai: 0 câu.

## 3. Lệch / ghi chú

- **`chunk_id` dồn số (phát hiện ở bước 4):** 2 edit D1 xóa nguyên dòng, mỗi dòng là một đoạn ⇒ mọi đoạn sau chỗ xóa trong 2 file đó đổi nội dung dưới cùng id (`file#số`). Plan chưa
  lường ⇒ A đồng ý **lý do chạm (f)** trước khi có số "sau" (plan §10; `truoc_sau.py` `58351a493a04`, C kiểm). (f) đưa 3 câu vào tập chạm; 2 câu chỉ có (f) ⇒ C đọc hai bên (bù phần ra
  khỏi phép kiểm "tập không chạm"). **Bài học:** id `file#số` không bền khi xóa / thêm đoạn giữa file — đợt sau ghi trước hoặc dùng id theo nội dung.
- **Lớp quét Golden 1b (mới):** script đợt 1 (cửa sổ 2 từ hai bên chỗ sửa) bỏ sót 2 câu có chữ bị bỏ (câu 5 mà plan đã dặn, câu 84) ⇒ thêm quét theo đúng cụm bị bỏ.
- **Script mới / chép (tất cả private, C kiểm diff):** `an_toan_run.py` (sinh vào thư mục riêng), `an_toan_dot2.py` (chấm bộ an toàn đợt 2), `golden_scan_dot2.py` và `build_gold_v5.py`
  (chép bản đợt 1, chỉ đổi đường dẫn + chặn ghi đè — bản đợt 1 ghi đè đầu ra cũ). Cổng ổn định chạy bản sao `/tmp` của `gate_b81.py` với đầu ra mới (bản gốc ghi đè file đợt 1), đã xóa.
- **Sub-agent:** 3 (đọc gói Golden) + 7 (judge Golden) + 12 (judge an toàn) — mỗi agent chỉ đọc file được giao, không kho / câu kín / `map.json`. Một số agent để script nháp ở `/tmp/judge_*`
  (có thể có chữ kho) ⇒ B đã xóa. Kết quả agent là dữ liệu: B kiểm lại đề xuất Golden (chữ hiện tại có trong Golden; 0 câu còn "quận"; keyword so `casefold`), cổng đối chứng chạy bằng máy.
- Sai sót quy trình của B: sửa plan sau khi đã báo sha mà chưa báo sha mới (A phát hiện, `WORKFLOW.md` §9.1); ghi giờ ước trong tin nhắn (A nhắc).

## 4. Giới hạn

- Bộ "trước" sinh 28/10, "sau" 30/10 ⇒ trôi phía provider theo ngày không tách được (plan §2); T1 / T2 không sát ngưỡng nên không cần chạy lại "trước".
- Judge Claude, chưa có người đọc; bộ an toàn do agent viết, n 28 ⇒ cận P0_sai "sau" 0–12 %.
- W5 đo trong harness, chưa tính HTTP; một lượt.
- P0_thiếu đổi 5 câu > A/A 3 — chưa rõ do kho hay do sinh; theo dõi.

## 5. Bàn giao

- **C đọc** (`dot2/c_doc_lists.json` + `compare.json`): chỉ (f) 2 câu; tụt "nhiễu" không chạm 3 câu; nhóm vé bộ an toàn S12; câu P0_thiếu mới S10; diff 4 script mới.
- **Chạy lại free** (từ `backend/`): `truoc_sau.py --work data/sua_kho_2026-10-27/dot2 … check --arm sau | check-judge | analyze`; `an_toan_dot2.py check|accept --judge k` (`compare` từ chối ghi đè).
- **A:** cập nhật chỗ tracked trỏ T1 `23c58c47635d` / 8.426 đoạn / record `574b5d02088b` / Golden md5 `0f7dbf41b422` (Project_Status, guide, LUONG, handoff, báo cáo kho); `GOLD_PATH` ⇒ v5
  (đổi code, B / C review); 5 chỗ báo cáo (bước 10); xóa sao lưu đợt 1 / 2 khi User duyệt.
