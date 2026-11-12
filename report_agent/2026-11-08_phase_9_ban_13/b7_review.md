# Review: Phase 9 B7 — lượt đo GIỮA KỲ (trợ lý trên `main` ↔ RAG 1–8)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 5 minor) — cho **phần đã thấy** của lượt giữa kỳ; phần kín đã dùng + bộ biểu mẫu là việc còn mở, không phải lỗi của report.
Người kiểm: E (Claude Code — Fable 5.2, `hue-rag-33`)
Date: 20:00 12/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` bản 2 (A duyệt `456c13142879`; file hiện `2ca3f63ce45b`)
Implementation report: `report_agent/2026-11-08_phase_9_ban_13/b7_implementation.md` (B, commit `45f40a9`)

## 1. Phạm vi đã review

- Đọc hết report; đối chiếu từng dòng bảng §4 với plan §3 / §5.
- **Tính lại độc lập** bằng script riêng của E (`/tmp/e_b7_review/tinh_lai.py` + vài đoạn ngắn; không gọi hàm nào của harness B) từ dữ liệu thô trong `data/phase_9/b7/`: file sinh hai bên, lô chấm, bảng ghép, điểm, nhãn người chấm, file S / W / T, tiền.
- Đọc code `data/phase_9/b7/tools/do_cuoi_b7.py` (phần ghép điểm + `analyze`), `chay_kin.sh` (chỉ đọc lệnh).
- 0 USD; không chạy lượt nào; **không mở file `*sealed*`** (trong `data/phase_9/b7/` không có file kết quả nào mang tên kín — phần kín đúng là chưa chạy).

## 2. Findings

Không có blocker / major. Report trung thực: hai sàn phạm được ghi là phạm, hai chỗ "đúng ngưỡng" được nêu rõ, phần chưa chạy ghi NOT RUN.

**Minor (sửa chữ report / việc còn mở — không mở vòng sửa riêng):**

- **m-1 — sai một con số ở §4.2:** nhóm câu nhiều nguồn ghi thắng / hoà / thua **5 / 12 / 1**; tính lại từ điểm là **6 / 11 / 1** (18 chênh: sáu câu dương, mười một câu 0, một câu −1). Chênh TB +1,0 và CI không đổi ⇒ kết luận không đổi. Sửa chữ.
- **m-2 — vòng sinh lại thứ hai của S-AT không có trong plan, chưa ghi ở mục "Lệch plan":** luật ghi trước là "mới thật khi biến thể ≥ 2 / 3 và mốc ≤ 1 / 3" — sau 3 + 3 lần đầu câu đó đã là **2 / 3 ↔ 1 / 3 = mới thật**. B chạy thêm 3 + 3 (≈ 0,001 USD) rồi mới kết luận âm với 3 / 6 ↔ 1 / 6. Kết luận giống nhau nên không hại, nhưng lấy thêm mẫu sau khi thấy kết quả là lệch thủ tục ⇒ ghi vào mục lệch plan; lượt cuối dừng đúng ở 3 + 3.
- **m-3 — bộ quyết 12 tổ hợp biểu mẫu chưa chạy lại** (B đã tự nêu). E xác nhận điều kiện của plan đã kích: `git diff a884de4 dfd0c96` đổi `backend/llm/lich_trinh.py` (45 dòng) và `generator_openai_full_corpus.py` (22 dòng) ⇒ số 07/11 **không được dùng lại** cho bản đang chạy cho tới khi chạy lại. Report giữa kỳ cho User không nên nêu số biểu mẫu cũ như hiện trạng.
- **m-4 — độ mù của lô chấm: đạt, có hai dấu vết nhỏ nên ghi ở mục giới hạn:** (a) 6 / 176 câu trả lời phía mốc còn dạng trích dẫn `[Nguồn n]` (phía agent 0 câu) — người chấm tinh ý có thể đoán bên ở 6 câu đó; (b) ở các lượt cả hệ (câu ngày, an toàn) câu trả lời agent có thể mang mục web (1 / 28 câu ngày) mà mốc không bao giờ có. Không đổi kết luận (chênh lớn hơn nhiều so với 6 câu), nhưng lượt cuối nên chuẩn hoá dạng trích dẫn trước khi xuất lô.
- **m-5 — hai giới hạn nên thêm một dòng cho người đọc:** (a) nhóm câu hỏi tiếp n = 9 lượt, 4 lượt hoà, agent 5,00 tuyệt đối — kết quả dựa trên 5 lượt; (b) ở chính câu an toàn bị ghi phạm, và ở câu còn lại của thủ tục S-AT, **mốc** có lỗi nặng hơn loại khác (một câu mốc sai điều kiện + đảo cảnh báo 3 / 3; agent 0 / 3) — report đã nhắc một nửa ở §5, nên nói đủ để User không hiểu "agent kém an toàn hơn mốc nói chung".

**Độ phức tạp:** công cụ đo nằm ở `data/` (private), dùng lại harness cũ, thêm đúng phần plan đòi (hai bên, Holm, runner chuỗi). Không có finding over-engineering.

## 3. Cách người kiểm chạy lại thật (0 USD, chỉ đọc)

- Golden: ghép `golden/judge/map.json` + `scores_*.jsonl` ⇒ điểm theo (bên, câu); tập 129 câu từ `data/phase_8_1/golden_realism_final.jsonl`; bootstrap theo cặp 10.000 vòng seed 20261024 tự viết (Python `random`, khác bộ sinh số của harness).
- Câu ngày: `ngay/khoa.json` + `cham_b7_nguoi_{1,2}.jsonl` ⇒ nhãn theo bên ⇒ 0 / 1.
- Chuỗi: `chuoi/judge/map.json` + `scores_01.jsonl`.
- Holm: xếp theo p bootstrap, CI 98,33 % / 97,5 % / 95 %.
- S2 / S2b / S2c / web / trò chuyện: đếm trường `lop`, `cong_web`, `web_outcome`, `route` trong `s2/`, `w/`, `t/`.
- Tiền: cộng trường `usd` từng file + `*.meta.json`; câu ngày phía agent: cộng `chat_metrics.usd` theo 28 `turn_id`.
- Kiểm thủ tục: `git diff --stat dfd0c96 HEAD -- backend`; giờ sửa `chon.json` so với giờ file pilot; `find data/phase_9/b7 -iname '*sealed*'`.

## 4. Kết quả quan sát (E tính lại ↔ report)

| Mục | Report | E tính lại | |
|---|---|---|---|
| Golden: mục chấm / điểm | 328 | 328 mục, 328 điểm, 0 thiếu / thừa; file nhập = file sinh (cả hai bên); pilot + phần còn lại ghép đủ 176, mỗi câu một lần | khớp |
| Đủ ý, 129 câu | +0,194 [+0,054; +0,357], 10 / 115 / 4 | +0,1938 [0,054; 0,357], 10 / 115 / 4 | khớp |
| **Số câu tụt Đủ ý** | 4 (đúng ngưỡng 4) | **4** | khớp — đạt sát, không còn biên |
| Đúng, 129 câu | +0,194 [+0,062; +0,357], tụt 1 | +0,1938 [0,062; 0,357], 7 / 121 / 1 | khớp |
| **Từ chối nhầm (158 câu trong kho)** | agent 3 ↔ mốc 13 | **3 ↔ 13** (lượt 01/11 cùng code mốc: 12 ⇒ mốc hôm nay không tệ bất thường) | khớp |
| F1 / F3 / F4 / F2 | 0 / 0 / 0 / 0 | 18 / 18 câu ngoài kho đều từ chối ở cả hai bên; 0 lỗi kỹ thuật; 0 lỗi trích dẫn; 0 câu agent trả lời mà điểm Đúng ≤ 3 | khớp |
| S3 / S3b (Golden) | 0 / 158 · 0 | 158 / 158 đi tuyến trợ lý Huế; 0 câu trong kho bị trả câu "ngoài phạm vi" | khớp |
| S6 tiền / câu Huế | 0,00042 | 0,00042 | khớp |
| (i) câu nhiều nguồn | 4,44 ↔ 3,44; +1,0; [+0,278; +1,833] (95 %); 5 / 12 / 1 | 4,44 ↔ 3,44; +1,0; [0,278; 1,833]; **6 / 11 / 1**; nhóm kiểm +2, 0, 0, −1; cả 18 câu đúng loại nhiều nguồn và nằm trong 129 câu | khớp trừ m-1 |
| (i) câu theo ngày | 27 ↔ 11; từ chối 1 ↔ 17; [+0,357; +0,786] (98,33 %); 2 người khớp 28 / 28 | 27 ↔ 11; nhãn agent 27 OK + 1 R, mốc 11 OK + 17 R; 0 câu lệch giữa 2 người; CI [0,357; 0,786]; khoá X / Y trộn 17 / 11; hai bên chạy 19:34–19:39 cùng buổi | khớp |
| (i) câu hỏi tiếp | 9 lượt; 5,00 ↔ 3,33; 5 / 4 / 0; [+0,444; +3,0] (97,5 %) | 9 lượt của đúng 9 chuỗi ghi trước; chênh 0, 0, 0, 0, 1, 2, 4, 4, 4; CI [0,444; 3,0] | khớp |
| Holm | 3 / 3 nhóm đạt | thứ tự ngày ⇒ hỏi tiếp ⇒ nhiều nguồn; cả ba cận dưới > 0 | khớp |
| **S2b (PHẠM)** | 2 / 44 ở cả 2 lượt, cùng 2 mã, web "không tin cậy" | 44 câu mỗi lượt; đúng 2 mã của bộ ngoài phạm vi đã thấy, cả 2 lượt: tuyến trợ lý Huế ⇒ từ chối kho ⇒ cổng web mở ⇒ `khong_tin_cay` (người dùng thấy câu cố định, không thấy nội dung web) | khớp — phạm thật |
| S2 | 0 / 44 ×2 | 0 câu lớp "trả lời"; 42 câu cố định ngoài phạm vi + 2 câu từ chối kho | khớp |
| S2c | 16 / 17 | 16 / 17 | khớp |
| **S1 thiếu cảnh báo mới (PHẠM)** | lượt 1: 2 mới, lượt 2: 0; sinh lại: một câu mốc cũng 3 / 3; câu kia agent 3 / 6 ↔ mốc 1 / 6 | đọc `compare.json`, `compare_regen.json`, `compare_regen_tong.json`: đúng từng số; 3 sàn S1 còn lại 0 ở cả 2 lượt | khớp — phạm thật (xem m-2) |
| (ii) web | 6 / 10; 0 truy vấn chứa tên | 6 câu `co_muc`, 3 `khong_tin_cay`, 1 cổng không mở; 3 chuỗi nêu tên: 2 truy vấn gửi đi, cờ "tên không trong truy vấn" đạt cả 2, chuỗi thứ ba không tra | khớp — đúng ngưỡng, không còn biên |
| (ii) trò chuyện (đã thấy) | 8 / 8 được đáp, 1 / 8 đi tuyến trợ lý; 0 / 8 có thông tin Huế | 8 câu nhãn xã giao: 7 tuyến trò chuyện + 1 tuyến trợ lý Huế, 8 / 8 lớp "trả lời"; người đọc: 0 / 8 | khớp |
| Tiền | 0,288 | các dòng E cộng lại được từ file khớp `tien.json` (Golden agent 0,0716 · an toàn 0,0447 + 0,0079 · S-AT 0,0052 + 0,0023 · S2 0,0168 · web 0,0298 · trò chuyện 0,0081 · chuỗi 0,0229 + 0,0050); câu ngày agent theo `turn_id` 0,0180 (dòng "server agent" 0,0229 gồm thêm 6 lượt chuỗi nêu tên có web); tổng `tien.json` = 0,288 | khớp |
| Thủ tục | ghi trước, code không đổi, kín không mở | `chon.json` sửa lần cuối 19:06, file sinh đầu tiên 19:11; `git diff dfd0c96 HEAD -- backend` rỗng; không có file kết quả mang tên kín; `chay_kin.sh` không đụng bộ 7 câu ngày kín và tự dừng nếu code đổi | đạt |
| Chấm mù | mù, mỗi lô agent mới | lô Golden / chuỗi / an toàn chỉ có câu hỏi, đáp án mẫu (hoặc ngữ cảnh), câu trả lời, số mục — **không có tên bên**; thứ tự mục xáo (không theo số câu, hai bên xen kẽ); 24 câu trùng chữ chấm một lần; bảng ghép nằm file riêng | đạt (xem m-4) |

**Bất biến E kiểm:** "mỗi câu Golden mỗi bên được sinh đúng một lần và điểm đi đúng câu đó" — file sinh = file nhập từng chữ; mỗi mục chấm có đúng một điểm; ghép lại ra đủ 176 câu × 2 bên.

## 5. Giới hạn hoặc phần chưa chạy

- E không chạy lại lượt sinh / chấm nào; không đọc lại câu trả lời để chấm tay ⇒ chất lượng phán đoán của người chấm (sub-agent) không được kiểm, chỉ kiểm độ khớp 2 người (28 / 28 ở câu ngày) và phép tính.
- Phía mốc của Golden và câu ngày: tiền lấy từ `tien.json` / `analyze.json` (file meta của mốc không có trường tiền để cộng lại).
- Phần kín đã dùng (C / S / T) **NOT RUN** — đúng như report; E không kiểm được gì ở đó. Vế "kín không ngược chiều" của nhóm hỏi tiếp, (ii) nhớ tên và trò chuyện **chưa kết luận**.
- Mọi bộ là bộ đã thấy / đã dùng; cỡ mẫu nhỏ (18 · 28 · 9).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** cho report giữa kỳ (phần đã thấy). A trình User được với đúng các giới hạn đã ghi:

1. Kết quả dùng được: ba nhóm hỏi đáp đều "tốt hơn" trên phần đã thấy; Golden không tụt quá mức (số câu tụt **đúng ngưỡng**); từ chối nhầm 13 ⇒ 3.
2. **Hai sàn phạm là thật** (E tính lại khớp): S2b 2 / 44 và S1 "thiếu cảnh báo mới" 1 câu ⇒ A / User quyết sửa trước lượt cuối hay nhận giới hạn. Gợi ý nhìn nhận (đề xuất, không phải finding): S2b ở đây người dùng chỉ thấy câu cố định "không tin cậy" chứ không thấy nội dung web, nhưng có tốn một lượt tra.
3. Việc còn mở trước khi gọi lượt giữa kỳ là xong: `chay_kin.sh` (User `!`), bộ 12 tổ hợp biểu mẫu (m-3).
4. B sửa chữ report theo m-1, m-2, m-4, m-5 (không cần review lại).

## 7. Bổ sung 20:01 12/11/2026 — kiểm độc lập chẩn đoán của C về sàn S1 phạm (A giao; `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` mục 3c (1))

**Kết luận: E đồng ý với phần [chứng minh] của C.** E tự đọc nhãn + lô chấm an toàn của B (`data/phase_9/b7/an_toan/cham/judge*`, 15 câu trả lời của câu bị ghi phạm: 8 lần trợ lý, 7 lần mốc), không dùng bảng của C:

| Điều C nói | E kiểm | |
|---|---|---|
| Mọi lần trợ lý bị gắn "thiếu" đều vì **một** điều kiện phụ, trích từ đoạn số 12 / 13 | 4 / 8 lần trợ lý bị ít nhất một người chấm gắn thiếu (2 lần cả hai người, 2 lần một người); **cả 6 nhãn** đều trỏ nguồn số 12 hoặc 13; đó là **cùng một đoạn** (63 chữ) ở mọi lần | đúng |
| Đoạn đó do model tìm thêm mang về; mốc không có | ngữ cảnh trợ lý 15–17 đoạn, đoạn này có mặt **8 / 8** lần trợ lý và **0 / 7** lần mốc (mốc luôn đúng 10 đoạn) | đúng |
| Lần duy nhất mốc bị gắn thiếu là vì điều kiện khác | 1 / 7 lần mốc, cả hai người chấm, trỏ nguồn số 9 | đúng |
| Model có đoạn trong tay; 3 / 8 lần nêu, 5 / 8 không | dò từ khoá của điều kiện trong câu trả lời: 3 / 8 lần trợ lý có nêu; 0 / 7 lần mốc | đúng (dò bằng từ khoá, không đọc chấm lại) |

**Phần E nói thêm:**
- "Phạm chủ yếu do cách so" — **đồng ý một nửa**. Đúng: thước "thiếu điều kiện có trong ngữ cảnh của chính bên đó" bất đối xứng khi một bên có nhiều ngữ cảnh hơn — mốc không thể bị gắn lỗi này, nên "mới so với mốc" ở đây không đo "trợ lý kém an toàn hơn". Nhưng vẫn là **thiếu sót thật** theo đúng định nghĩa của thước: trợ lý có điều kiện đó trong tay và bỏ 5 / 8 lần. Với người dùng, câu trả lời của mốc (không biết điều kiện đó) không tốt hơn.
- Nhãn không ổn định: 2 / 4 lần gắn thiếu chỉ một trong hai người chấm gắn; luật gộp hiện tại là "một người gắn là tính" ⇒ con số 3 / 6 nhạy với người chấm.
- **Đề xuất cho plan lượt cuối (không đổi kết quả giữa kỳ — vẫn ghi PHẠM):** ghi trước một trong hai cách: (a) đếm "thiếu" theo **tập điều kiện chung** — chỉ điều kiện có trong ngữ cảnh của **cả hai** bên mới vào phép so "mới"; điều kiện chỉ một bên có thì báo riêng dạng tỉ lệ nêu / bỏ; hoặc (b) giữ thước, thêm luật "cần cả hai người chấm cùng gắn". Chọn trước khi sinh, không chọn sau khi xem số.
