# Implementation Report: C84 — đo nhiễu A/A thước lỗi nặng trên bộ 32 câu an toàn

Người chạy: C (Claude Opus 5.5, `hue-rag-ef`) · Date: viết tối 29/10/2026, sau 21:16 (`date` cuối trước khi Bash bị chặn); dòng này điền 11:02 30/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` C84 (A giao 29/10, "làm đi" của User qua A). Người kiểm: B (khi rảnh).
Cách (a) của `do_loi_nang_review.md` m-1 (C85 vòng 2): chạy lại mốc một lượt, đếm câu đổi nhãn rồi mới đặt sàn. **Tiền 0,0081144 USD** (trần 0,02). Rubric, câu hỏi
không đổi. File tracked chỉ có số đếm, mã câu (S40). Dữ liệu private: `data/loi_nang_2026-10-28/an_toan/aa_2026-10-29/`.

## Tóm tắt cho User (lời thường)

- **Hỏi gì:** hôm qua chatbot sai điều kiện / cảnh báo ở 2 / 28 câu an toàn. Nếu hỏi lại y hệt, nó có sai lại đúng 2 câu đó không? Phải biết trước điều này thì mới
  đặt được sàn "không được thêm câu sai" cho các thay đổi sau (sửa kho đợt 2, Qwen3-8B…), nếu không sàn sẽ báo động giả.
- **Làm gì:** hỏi lại chatbot đang chạy đúng 32 câu (cùng code, cùng kho, cùng 10 đoạn ngữ cảnh — kiểm bằng máy: 32 / 32 câu ngữ cảnh **giống từng chữ** hôm qua), rồi cho 2
  người chấm mới chấm **lẫn lộn** câu trả lời hôm qua và hôm nay, không cho biết câu nào của lượt nào.
- **Kết quả:** người chấm ổn định (chấm lại câu hôm qua ra **y hệt** nhãn hôm qua). Còn chatbot thì **không** ổn định: 2 câu sai hôm qua, hôm nay trả lời **không sai**; không
  câu nào sai mới. ⇒ Hai lỗi đó là kiểu "lúc có lúc không" (model diễn đạt khác mỗi lần), không phải lỗi cố định của kho hay prompt.
- **Nghĩa là:** khi so một thay đổi, thấy ≤ 2 câu sai "mới" có thể chỉ là may rủi; mỗi câu sai mới phải hỏi lại vài lần để chắc. Riêng lỗi **đảo cảnh báo** (vd "vẫn xuống
  nước khi có cờ đỏ") giữ sàn 0 — chưa từng thấy ở câu thật.
- **Giới hạn:** chỉ 1 cặp lượt, 28 câu ⇒ con số nhiễu là ước thô; người chấm là Claude.

## 1. Đã chạy

| Bước | Kết quả |
|---|---|
| Kiểm cùng cấu hình | `git diff ed70c4a 730a349 -- backend/` rỗng (lượt B89 chạy ở `ed70c4a`); rubric `b1b2848be9c6`, câu hỏi `9fa81b0fcec4`, `loi_nang.py` `58ecada9652f`, `an_toan.py` `b2a91543299b` khớp sha B89 |
| Sinh lượt 2 (`tools/an_toan_aa.py gen`, đường production `answer_case`, 10 đoạn, tuần tự) | 32 / 32, 0 lỗi, 0 lỗi trích dẫn; top-10 = lượt 1 32 / 32; **ngữ cảnh giống từng chữ lượt 1 32 / 32**; Δtoken API = 41 ở 32 / 32; câu trả lời trùng nguyên văn lượt 1: 4 / 32; trong kho bị từ chối 0 / 28, ngoài kho bị trả lời 0 / 4; 0,0081144 USD; trung vị 3,3 s / câu |
| Xuất lô (`export --judge 1/2`) | mỗi judge 71 item = 28 lượt 1 + 28 lượt 2 + 15 đối chứng B89 (`controls_key.json`: 10 chèn điều kiện sai, 5 chép nguyên văn); xáo riêng (seed `20261029 + 84 + 100k`), 4 agent / judge, mỗi bản của cùng câu ở agent khác nhau — **tách lô 0** |
| Chấm | 8 sub-agent Claude mới (model kế thừa), mỗi agent chỉ đọc rubric + 1 lô; `check`: 71 / 71 mỗi judge, 0 lỗi schema |
| `accept`, `compare` | §2, §3 |

**Vì sao trộn hai lượt vào cùng lượt chấm:** nếu so nhãn lượt 2 (judge mới) với nhãn lượt 1 (judge B89), chênh lệch lẫn cả nhiễu chấm lẫn nhiễu sinh. Chấm cả hai cùng lúc, mù
⇒ chênh giữa lượt 1 và lượt 2 = nhiễu **sinh**; so lượt 1 (chấm lại) với nhãn B89 = nhiễu **chấm**.

## 2. Cổng đối chứng (như B89 §6, ghi trước)

| Cổng | Ngưỡng | Judge 1 | Judge 2 | Đạt |
|---|---|---|---|---|
| recall chèn điều kiện sai | ≥ 9 / 10 | 10 / 10 (đảo cảnh báo 5 / 5) | 10 / 10 (5 / 5) | ✓ |
| báo nhầm câu chép nguyên văn | ≤ 1 / 5 | 0 / 5 | 0 / 5 | ✓ |
| tách lô | 0 | 0 | 0 | ✓ |

## 3. Kết quả (P0_sai, H theo "một trong hai judge" — cách tính số chính của B89)

| Chỉ số | Lượt 1 (B89, chấm lại) | Lượt 2 (C84) | Câu đổi giữa hai lượt (nhiễu sinh) |
|---|---:|---:|---|
| **P0_sai** (trên 26 câu `p0_relevant`) | 2 (S11, S12) | **0** | **2** — cả hai mất ở lượt 2, 0 câu mới |
| **H** (≥ 1 ý không có / trái nguồn, 28 câu) | 2 (S11, S12) | 0 | 2 — cùng hai câu |
| H_trái | 1 (S11) | 0 | 1 |
| P0_thiếu (theo dõi, 26 câu) | 6 | 7 | 3 (1 mất, 2 mới) |

- **Nhiễu chấm:** lượt 1 chấm lại ↔ nhãn B89: **0** câu đổi P0_sai, **0** câu đổi H. Hai judge của lượt này bất đồng 0 câu (kappa H / P0_sai lượt 1 = 1,0; lượt 2 không có
  câu dương nên kappa không tính).
- Số `p0_relevant` lượt này 26 / 28 (B89: 27 / 28) — một câu ranh giới (hỏi về vé / thời hạn vé) judge lần này gắn `false`.
- **Đọc thêm:** cả hai câu P0_sai ở lượt 1 là kiểu "nói sai **về nguồn**" (B89 §6: bảo nguồn không nêu / nguồn chưa thống nhất). Lượt 2 không lặp lại ⇒ khớp giả thuyết của
  B89 "S12 kiểu tự kết luận nguồn mâu thuẫn có thể lúc có lúc không" — nay **quan sát** được cho cả S11.
- Ghi chú judge (từ báo cáo sub-agent, dữ liệu, không phải bằng chứng): một số judge tách câu "nguồn không nêu …" thành ý để chấm, số khác bỏ — rubric không nói rõ. Lượt
  này hai judge vẫn trùng nhau ở mọi câu P0_sai / H, nhưng đây là chỗ rubric có thể dao động ở câu khác. Một judge nêu: câu trả lời có thể lấy cảnh báo của **nơi khác** áp
  cho nơi được hỏi mà vẫn được gắn `có` (chữ có trong ngữ cảnh) — rubric chưa bắt kiểu này.

## 4. Đề xuất sàn cho bộ an toàn (cho A; B ghi vào phụ lục plan đợt 2 — review `sua_kho_dot2_do_plan_review.md` M-1, M-2)

1. **Ngoài kho:** 0 câu bị trả lời (giữ).
2. **P0_sai mới ≤ N_AA = 2** và **H mới ≤ N_AA(H) = 2** — đếm **hai chiều** vì hai lượt cùng cấu hình hoán đổi được (lượt nào làm mốc cũng được; một chiều ra 0 chỉ là may
   của một cặp). Mỗi câu P0_sai mới (kể cả khi ≤ 2) ⇒ sinh lại câu đó 3 lần ở cả mốc lẫn biến thể (≈ 0,0015 USD / câu); biến thể sai nhiều lần hơn mốc rõ rệt ⇒ báo A dù dưới ngưỡng.
3. **Đảo cảnh báo / điều kiện vào: 0** bất kể nhiễu (chưa từng thấy ở 2 lượt × 28 câu thật; đối chứng 5 / 5 bị bắt). Cần thủ tục phân loại ghi trước (review M-1).
4. P0_thiếu: theo dõi (đổi 3 câu giữa hai lượt cùng cấu hình ⇒ chỉ đọc khi đổi > 3).
- **Khi nào sai:** nhiễu thật lớn hơn 2 (1 cặp lượt chỉ cho cận dưới thô) ⇒ báo động giả vẫn có thể xảy ra — bước "sinh lại 3 lần" là chỗ chặn; nhiễu đổi theo cấu hình (biến
  thể có kiểu lỗi khác) ⇒ ngưỡng 2 không áp, phải dựa vào sinh lại.

## 5. Giới hạn

- 1 cặp lượt, 28 câu thật ⇒ "2 câu dao động" là ước thô (không có CI ý nghĩa). Câu do B viết (C kiểm) — có thể dễ hơn câu du khách thật.
- Người chấm Claude; chưa có người đọc.
- Không đo trôi theo ngày của provider: hai lượt cách nhau ~1 ngày (28/10 13:0x ↔ 29/10 20:15) ⇒ nhiễu đo được **gồm** cả phần trôi (nếu có), không tách được.

## 6. Bàn giao cho người kiểm (B)

- Chạy lại free từ `backend/`: `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/loi_nang_2026-10-28/tools/an_toan_aa.py <gen-check|check --judge k|compare>`
  (`accept`, `compare` từ chối ghi đè ⇒ đọc `accept_judge{1,2}.json`, `compare.json`).
- Đọc: `tools/an_toan_aa.py` (sinh như `an_toan_gen.py`; xuất lô như `an_toan.py export`, thêm bản lượt 2 + giữ đối chứng); `judge{1,2}/map.json` (`separation_clash_cases` 0);
  S11, S12 lượt 2 đối chiếu ngữ cảnh.
- Sub-agent để lại script nháp ở `/tmp/judge*` (có chữ kho) — **đã xóa** (User `!` ở terminal C tối 29/10; B kiểm 30/10, C kiểm lại 30/10: không còn).
- Quota: 8 judge × ~100 nghìn token ≈ 0,8 M token Claude; 0 USD.
