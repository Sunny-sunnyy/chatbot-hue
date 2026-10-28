# Implementation Report: đợt sửa kho — bước 9: đo "trước ↔ sau" (B83)

Người làm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 12:01 28/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` mục B83 (A giao 28/10; User duyệt 2 trích dẫn gold mới + "0 câu Golden cần sửa").
Plan: `sua_kho_do_truoc_sau_plan.md` (A duyệt sha `41485782b39e`). Spec: `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (`937cf8969810`) §5 bước 9, §6.
Người kiểm: C (C80 ready 0/0/1, `sua_kho_b9_review.md`; m-1 đã sửa). File tracked này chỉ có số đếm, mã câu, loại câu (S40). Dữ liệu private `data/sua_kho_2026-10-27/`.

## Tóm tắt cho User (lời thường)

- **Thử gì:** so chatbot trên kho **trước** và **sau** đợt sửa kho (40 mục lỗi + 11 chỗ tên phường + bỏ file danh mục), cùng 176 câu Golden, chấm mù cùng một lượt.
- **Kết quả: không làm hỏng.** Không câu ngoài kho nào bị trả lời; không lỗi kỹ thuật; không lỗi trích dẫn mới; không câu nào "nói chắc sai" mới. Điểm đủ ý / đúng gần như y hệt
  (đủ ý −0,008, đúng 0,000 trên 129 câu chính; 4 câu tụt / 4 câu tăng). Câu bị từ chối nhầm 12 → 13 (đúng mức cho phép).
- **Không thấy "tốt hơn" rõ** ở câu chạm phần sửa (31 câu): đáp án Golden không đổi, và phần lớn edit chỉ thêm tên phường mới — judge không có chỗ để cộng điểm. Lợi chính của
  đợt này là **kho đúng hơn** (đã review từng mục), không phải điểm số.
- **Tiền:** bộ "sau" 0,0365 USD (~910 đồng); cả đợt sửa kho ≈ 0,073 / 0,15 USD. **Thời gian chờ** ở lượt "sau" có nhiều câu chậm (câu chậm 9,8 s so với 4,9 s) — chậm ở
  **phía mạng / nhà cung cấp** trong vài phút cuối lượt (không tách được hai bên), không do kho: phần tìm kiếm trên máy không đổi, câu trả lời không dài hơn. **Số câu chậm
  của lượt "sau" vì vậy không đại diện** cho chatbot.

## 1. Đã chạy

| Bước | Lệnh (từ `backend/`, harness `data/sua_kho_2026-10-27/tools/truoc_sau.py` sha `61e9dcc863e1`) | Kết quả |
|---|---|---|
| gold v4 | `data/phase_8_1/tools/build_gold_v4.py --approved` | `gold_v4.jsonl` `927bae1bf201` (= nháp đã duyệt); v1 / v2 / v3 sha không đổi |
| GOLD_PATH | `backend/experiments/phase_8_1/g1_retrieval.py:48` ⇒ `gold_v4.jsonl` | A commit `e08a126` (C review code ready 0/0/3); `test_gold_coverage.py` 3 pass |
| preflight sau | `preflight --arm sau` | 8.426 point, **0 đoạn thiếu evidence**, 204 file, build record `574b5d02088b`, Golden md5 `0f7dbf41b422` (= trước), md5 câu hỏi 176 / 176 = bộ "trước" |
| sinh (có phí) | `run --arm sau --cases pilot` rồi `rest` (tuần tự) | pilot 10 câu 0,0020443 USD (bộ "trước" 0,001981 ⇒ +3 %); 176 câu, **0 lỗi**, không chạy lại câu nào |
| check | `merge`, `check --arm sau` | bảng §2 |
| câu chạm | `touched` | **43** / 176 (a 0, b 37, c 38, d 3); số chính 31 / 129; `touched.json` `bff33023cc83` |
| judge | `export-judge --batch-size 24` (dừng nếu Golden ≠ preflight sau) ⇒ 7 sub-agent judge mới (model kế thừa `global.anthropic.claude-opus-5-5`, cùng judge B1 / G2 / B3), mỗi agent ≤ 2 lô | 303 item khác nhau / 352 câu trả lời, 13 lô; `check-judge`: 303 / 303, 0 lỗi schema |
| rejudge (F2) | — | **không cần**: 0 ứng viên F2 |
| analyze | `analyze` | `analyze.json` `caa608ed4f8d` |

## 2. Kết quả theo tiêu chí ghi trước (plan §4)

| Dòng | Ngưỡng | Kết quả | Đạt |
|---|---|---|---|
| F1 OOS người dùng thấy câu trả lời (sau) | 0 / 18 | 0 | ✓ |
| F2 nói chắc sai mới (158 trong phạm vi) | 0 | 0 ứng viên (không cần rejudge) | ✓ |
| F3 lỗi kỹ thuật | 0 mỗi bên | 0 / 0 | ✓ |
| F4 500 citation mới | 0 | 0 (cả hai bên 0 câu 500) | ✓ |
| T1 Completeness, số chính 129 | câu tụt ≤ 5; TB ≥ −0,1 trên 129 **và** tập không chạm | 4 tụt (4 / 121 / 4); TB −0,0078 [−0,062; +0,039]; không chạm (98): 0,000 [−0,051; +0,051] | ✓ |
| T2 Accuracy, số chính 129 | như T1 | 1 tụt (1 / 127 / 1); TB 0,000 [−0,023; +0,023]; không chạm: +0,010 [0,000; +0,031] | ✓ |
| T3 từ chối nhầm trong phạm vi | sau ≤ trước + 1 | 12 ⇒ 13 (câu mới 33: so sánh, nhãn `unnatural`, không chạm, context đổi) | ✓ (đúng mức) |

⇒ **Kết luận theo plan: "không làm hỏng"** (spec §6 tiêu chí "không làm hỏng" đạt).

**Câu tụt và nhãn giải thích** (plan §4; T1 4 câu, T2 1 câu):

| Câu | Chỉ số | Nhãn máy | Loại câu |
|---|---|---|---|
| 50 | Completeness | nhiễu (context hai bên giống hệt, cả thứ tự) | so sánh |
| 93 | Completeness | nhiễu (giống hệt) | điều kiện |
| 143 | Completeness | nhiễu (giống hệt) | điều kiện |
| 169 | Completeness | fact đã sửa (luật c) | điều kiện |
| 21 | Accuracy | fact đã sửa (luật b + c) | nhiều nguồn |

**Theo dõi (không quyết):**

| Dòng | Kết quả |
|---|---|
| W1 câu chạm (31 câu số chính) | Completeness −0,032 [−0,194; +0,097] (1 / 29 / 1); Accuracy −0,032 [−0,097; 0,000] (0 / 30 / 1) — **không "tốt hơn"** |
| W2 Accuracy = 4 có trả lời (158) | 5 ⇒ 7 |
| W3 Relevance | −0,008 [−0,054; +0,039] (4 / 120 / 5) |
| W4 USD / câu · token vào / ra TB | 0,0002053 ⇒ 0,0002071 · 1.654,9 / 79,6 ⇒ 1.657,3 / 82,8 |
| W5 `wall_ms` tuần tự p50 / p95 | 2.207,7 / 4.883,6 ⇒ 2.782,1 / **9.763,0** — phần sinh p95 4,6 ⇒ 9,4 s; phần trên máy (tìm + context) trung vị 38 ⇒ 45 ms; token ra theo cặp +3,2 TB; 10 câu chậm nhất đều ở cuối lượt (case 143–171, 11:53–11:56; C80: ms / token khúc cuối ×2,9 so với cùng câu lượt trước) ⇒ chậm ở **phía mạng / provider** (không tách được hai bên), không do kho; **p95 lượt "sau" không đại diện** *[quan sát; không chạy lại]*. Ghi thêm: 11:50–11:56 có việc không trả phí nhưng nặng CPU / Qdrant của C chạy song song (C tự khai — lỗi điều phối, không phải của người chạy); phần trên máy của lượt này không tăng ⇒ ít khả năng là nguyên nhân |
| W6 top-10 đổi · đoạn đúng trong context (v3 trước ↔ v4 sau) | 40 / 158 câu đổi top-10 (như T1 B81); tỉ lệ fact có trích dẫn trong context 0,7615 ⇒ 0,7615, 0 câu mất / 0 câu thêm (chỉ tính giao `evidence_parts`, không luật dòng tiêu đề) |
| W7 Completeness "tốt hơn" | không (CI chứa 0) |
| W8 Accuracy 5 ⇒ 4 mới | 3 câu: 17, 20, 21 (nhiều nguồn) ⇒ **C đọc** |

## 3. Sửa trong code trước / trong khi analyze

- **C review code B83 (0/0/3), sửa trước analyze:** m-1 nhãn "tìm đổi đoạn" theo **tập** đoạn (không theo danh sách có thứ tự) + nhãn phụ "nhiễu (chỉ đổi thứ tự)"; m-2 `rerun-f4`
  in nhãn context giống / khác (không dùng — F4 không vỡ); m-3 `export-judge` dừng khi md5 Golden ≠ `preflight_sau`.
- **B sửa thêm sau lần analyze đầu:** lần đầu so tập theo (nguồn, `evidence_parts` vị trí ký tự) ⇒ câu 50 (context giống hệt, cả thứ tự) bị gán "tìm đổi đoạn" vì đoạn của file có
  edit ở chỗ khác bị dời offset dù chữ không đổi. Đổi sang so **tập `chunk_id`** (câu đến nhánh này đều không chạm vùng sửa ⇒ cùng id = cùng chữ). Chỉ đổi nhãn câu 50; mọi số
  quyết không đổi. (analyze ghi đè `analyze.json` — file dẫn xuất.)

## 4. Giới hạn

- Judge Claude, **chưa có mốc người** (B0 làm sau). Cùng model / prompt / rubric với B1 / G2 / B3 ⇒ không chạy kiểm 4 phiếu.
- A/A dùng lại B1 ↔ G2.1a (không chạy mới, đúng spec §6).
- F2 chỉ bắt "nói ngược đáp án", không bắt "bịa thêm" (judge không trừ chi tiết thêm — giới hạn đã ghi ở plan).
- W1 không thấy "tốt hơn": Golden không đổi (User duyệt 0 sửa) và phần lớn edit chỉ thêm tên mới ⇒ thước Golden không nhạy với loại sửa này.
- W5 hai lượt khác giờ ⇒ chênh latency gồm cả biến động mạng / provider (không phải phép so latency); khúc cuối lượt "sau" trùng một việc nặng CPU / Qdrant chạy song song.

## 5. Bàn giao cho người kiểm (C)

- Chạy lại free (từ `backend/`): `check --arm sau`, `check-judge`, `analyze` ⇒ số trùng §2 (`analyze` ghi đè `analyze.json` cùng nội dung); `touched` từ chối ghi đè (đã có).
- **Đọc** (plan §7): câu tụt nhãn "nhiễu" 50, 93, 143 (context giống hệt ⇒ xác nhận không có lỗi kho mới); W8 17, 20, 21 (ghi "sai fact" / "khác cách diễn đạt"); không có câu F2.
- Đọc diff `truoc_sau.py` cả file (phần "sau" + 3 sửa C + sửa nhãn §3).
- Tiền: bộ "sau" **0,036454 USD**; cả đợt sửa kho: bước 0 0,0361284 + cổng B81 0,000449 + bước 9 0,036454 ≈ **0,0730 USD** / trần 0,15.
