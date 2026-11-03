# Implementation Report: Phase 9 B3b — câu dặn lịch sử chống "mượn đoạn của đối tượng khác" (PA1) — lượt 1 Q4 không đạt ⇒ **(a) chỉ nhớ câu hỏi: đạt đã thấy + bộ mới C152 ⇒ nhớ BẬT** (`7a76ba2`)

Người làm: B (Claude Opus 5.5, `hue-rag-32`) · việc **B138** (A giao; User chọn "sửa trên bộ mới rồi bật", trần B3 0,50, dừng > 0,47) · bản này 18:45 03/11/2026 (giờ từ `date`).
Nhánh **`p9-b3b`** từ `main` `a3dabba` (B3 đã merge, cờ nhớ tắt), worktree `/tmp/b_p9b3b`. Commit **`1ed7b34`** (câu dặn), **`57f0e0b`** (`nho_cau_tra_loi: false`), **`7a76ba2`** (B141: `nho_hoi_thoai: true`, `settings.yaml` sha `31a7c369485e`; test không-cookie đặt cờ tắt tường minh) — đã push. Dải review: `a3dabba..7a76ba2`.
Report tracked, repo public: không chép câu Golden / câu chuỗi / kho; chỉ số đếm, mã chuỗi. Dữ liệu: `data/phase_9/b3b/` (private). B không mở `data/phase_9/bo_do_b3b/` (bộ kiểm C viết) và phần kín B3.

## 1. Thay đổi (`git diff a3dabba..1ed7b34`, 1 file, +4 / −1)

`backend/llm/full_corpus_prompt.py` — `ASSISTANT_HISTORY_NOTE` (chỉ thêm khi lượt **có lịch sử**) thêm một câu: lịch sử chỉ để hiểu câu hỏi nói về đối tượng nào; mỗi nhận định lấy từ Bằng chứng nói đúng về đối tượng được nhận định, không gán thông tin của đối tượng khác cho đối tượng đang hỏi; Bằng chứng không nói điều được hỏi về đối tượng đó ⇒ câu không đủ thông tin.
sha256 (12): `ASSISTANT_HISTORY_NOTE` **`64e347d5df58`** (B3: `798f6af34f26`); `ANSWER_SYSTEM_INSTRUCTIONS` `81d3040cf53f` và `ROUTER_HISTORY_NOTE` `62f8197730ad` **không đổi** ⇒ lượt không lịch sử gửi model đúng chuỗi B3 (Q1). Test `test_b3_memory.py` + `test_b2_tool_loop.py` **23 / 23** (test sẵn có khoá: câu dặn có khi có lịch sử, vắng khi không).
Căn cứ chọn chỗ sửa: C kiểm lượt kín K-N2 — `tim_kho` có đoạn về đúng đối tượng nhưng không có ý bác tiền đề ⇒ lẽ ra từ chối ⇒ lỗi ở khâu trả lời (A báo).

## 2. Ca dò tự viết (`data/phase_9/b3b/do_tu_viet.jsonl`, 9 chuỗi, bên nhớ; kiểm từng ý bằng `grep_kb.sh`)

Loại: lượt 1 hỏi đối tượng X (có trong kho) ⇒ lượt 2 hỏi tiếp tiền đề sai về X, ý đó có thật nhưng của đối tượng khác (7 chuỗi) + 2 chuỗi hỏi tiếp kho có câu trả lời (canh từ chối nhầm).
| | Trước sửa (B3, `a3dabba`) | Sau sửa (`1ed7b34`) |
|---|---|---|
| 7 ca tiền đề sai | 5 từ chối; 2 bác tiền đề **có nguồn đúng đối tượng** (nói ý đó thuộc đối tượng nào) | giống hệt |
| 2 ca kho có câu trả lời | trả lời đúng, có nguồn | trả lời đúng, có nguồn |
**Ca dò không tái hiện được lỗi K-N2** (cả trước sửa) ⇒ không chứng minh được câu dặn sửa đúng lỗi; chỉ cho thấy không làm hỏng loại câu này. Bên độc lập (không lịch sử) ở mốc thì trả lời 3 / 4 ca đầu bằng đối tượng khác — đúng như dự đoán (không biết "đó" là gì), không thuộc sàn.

## 3. Đo trên đã thấy (25 chuỗi × 3 bên; luật A ghi trước: Q3 6 / 6, Q4 CI > 0, Q5 0 / 0, Q6 tụt ≤ 1)

Lệnh: `full_corpus_eval chuoi ../data/phase_9/bo_do_b3/chuoi_da_thay.jsonl --ben nho|doc_lap|tran --out data/phase_9/b3b/sau/<bên>.jsonl` ⇒ `cham_chuoi.py may|export|analyze data/phase_9/b3b/sau/da_thay`; judge Completeness mù 3 bên 3 lô + thước an toàn 2 judge (3 lượt điều kiện, ngữ cảnh = đáp án mẫu — cùng khuôn lô B3), mỗi lô một sub-agent mới (Opus 5.5), brief dặn ghi `item`; 60 / 60 điểm, đủ item.
| Mã | B3b (`1ed7b34`) | B3 (`46008ed`, cùng bộ) | Luật | Kết luận |
|---|---|---|---|---|
| Q3 nhớ tên | **6 / 6** | 6 / 6 | 6 / 6 | đạt |
| **Q4** hỏi tiếp — 20 lượt sau có Golden, nhớ ↔ câu gõ không lịch sử | **+0,50, CI 95 % [−0,15; +1,20]**, 5 / 14 / 1 (tụt C04#1) | +0,65 [+0,15; +1,25] | CI > 0 | **KHÔNG ĐẠT** |
| Q4 báo kèm — chỉ 9 lượt hỏi tiếp · nhớ ↔ trần | +0,89 [−0,56; +2,33] · −0,15 [−0,45; 0,00] | +1,22 · +0,15 | — | — |
| Q5 ngoài kho | **0** lượt bị trả lời (3 bên) | 0 | 0 | đạt |
| Q5 điều kiện | **0** ý "trái" (2 judge), thiếu điều kiện 0 | 0 | 0 | đạt |
| Q6 đổi chủ đề | tụt **0** / 3; câu tìm mang đối tượng cũ 0 / 5 | 0 · 0 | ≤ 1 | đạt |
| Q8 token thật − builder (nhớ) | max **14** | 167 | < 512 | đạt |
| Q9 | tuyến bên nhớ đúng mọi lượt; `khan_cap` 0; `tim_kho` model TB 0,29 / lượt | — | theo dõi | — |

**Vì sao Q4 tụt (quan sát, chưa chứng minh nguyên nhân):** bên nhớ chỉ đổi điểm ở 2 / 20 lượt — C04#1 5 ⇒ 2 (câu so sánh hai nơi: lần này câu tìm model viết nhắm nơi thứ nhất, đoạn số liệu của nơi thứ hai không vào ngữ cảnh ⇒ model nói "nguồn không nêu" — đúng với ngữ cảnh nó có, nhưng thiếu ý; câu dặn mới có thể góp phần làm model không suy ra), D02#1 4 ⇒ 5. Bên **độc lập** (lời dặn không đổi, cùng cấu hình B3) đổi 5 / 20 lượt, có lượt ±4 (C02#1 5 ⇒ 1, C04#1 1 ⇒ 5) ⇒ nhiễu sinh + tìm giữa hai lần chạy cùng cấu hình **lớn so với mẫu 20 lượt**; TB nhớ 4,9 ⇒ 4,8 (một lượt). Theo luật ghi trước vẫn là **không đạt** — B không chạy lại để "tìm lần đạt".

## 4. Tiền (giá đủ, cộng `usd`)

Ca dò trước sửa 0,0057 (mất — bẫy `--out`, ghi STATUS_B) + 0,0051 + 0,0057 + 0,0037 · đã thấy 3 bên 0,0216 + 0,0217 + 0,0161 · ca dò sau 0,0092 ⇒ lượt 1 ≈ 0,089 · lượt (a) 0,0595 ⇒ **B138 ≈ 0,149 USD** · cổng B141 0,0028. B3 cộng dồn ≈ 0,296 (trước B138, chưa tính lượt chạy lại K-N2 của C) + 0,149 ≈ **0,445** / trần cứng 0,50 (A, User duyệt) ⇒ còn ≈ 0,055 cho bộ mới của C (ước ~0,03). Judge: quota Claude.

## 5. Lượt (a) — chỉ nhớ câu hỏi (A quyết: đường kết quả âm ghi trước; 18:55 03/11/2026)

`57f0e0b`: `nho_cau_tra_loi: false` (lịch sử chỉ còn câu hỏi các lượt trước, không câu trả lời) + câu dặn giữ `64e347d5df58`. Chạy **một lần** trên đã thấy 25 × 3 bên, cùng lệnh / judge / thủ tục §3 (`data/phase_9/b3b/sau_a/`); luật như cũ. Không chạy lại.
| Mã | (a) `57f0e0b` | Luật | Kết luận |
|---|---|---|---|
| Q3 nhớ tên | **6 / 6** | 6 / 6 | đạt |
| **Q4** 20 lượt, nhớ ↔ câu gõ không lịch sử | **+0,80, CI 95 % [+0,25; +1,50]**, 6 / 14 / 0 (0 lượt tụt) | CI > 0 | **đạt** |
| Q4 báo kèm — 9 lượt hỏi tiếp · nhớ ↔ trần | +1,67 [+0,56; +2,89] · +0,20 [0,00; +0,60] | — | — |
| Q5 ngoài kho · điều kiện | **0** (3 bên) · **0** "trái", thiếu 0 (2 judge) | 0 · 0 | đạt |
| Q6 đổi chủ đề | tụt **0** / 3; câu tìm mang đối tượng cũ 0 / 5 | ≤ 1 | đạt |
| Q8 · Q9 | max **43** < 512 · tuyến bên nhớ đúng mọi lượt, `khan_cap` 0, `tim_kho` model TB 0,30 / lượt | < 512 · theo dõi | đạt · — |
| Q1 | lượt không lịch sử: lời dặn + chuỗi gửi model không đổi (cờ chỉ đổi thứ được lưu vào kho cuộc) | — | đạt (theo code + sha) |
C04#1 (lượt 1 tụt) lần này không từ chối, đủ ý. TB Completeness nhớ / độc lập / trần: 4,95 / 4,15 / 4,75. Test `test_b3_memory.py` + `test_b2_tool_loop.py` + `test_phase6_settings.py` 27 / 28 (1 hỏng = test cần khoá API, chạy không nạp khoá — bẫy đã biết `Project_Status.md` §8).
**Giới hạn:** (1) ca dò tự viết không tái hiện được K-N2 ⇒ chưa chứng minh câu dặn + "chỉ nhớ câu hỏi" sửa đúng lỗi kín — bộ mới của C (S1 / S2) là phép thử; (2) hai lượt (câu dặn ± nhớ câu trả lời) khác nhau 0,30 điểm TB chênh trên 20 lượt, trong khi bên độc lập (không đổi) dao động 5 / 20 lượt giữa các lần chạy ⇒ không kết luận được "chỉ nhớ câu hỏi tốt hơn nhớ cả câu trả lời"; chỉ: cấu hình (a) qua luật ghi trước; (3) chỉ nhớ câu hỏi ⇒ lượt sau không biết trợ lý đã trả lời gì (vd "ý thứ hai bạn nói…") — chưa đo loại câu này.
Tiền (a): 0,0217 + 0,0215 + 0,0162 = **0,0595**.

## 5c. Bộ mới C152 (C chạy + chấm, B không mở) và quyết bật (19:13 03/11/2026)

C chạy bộ kiểm mới `data/phase_9/bo_do_b3b/` trên `57f0e0b`, bên nhớ + độc lập (bỏ bên trần — A), 0,020337 USD. sha: `KET_QUA_C152.md` **`ea5be7210723`**, `nho.jsonl` `21e49a66d513`, `doc_lap.jsonl` `607d855eb4d0`, `may.json` `1098265b4b77`.
| Luật A (ghi trước) | Kết quả | |
|---|---|---|
| **S1** 0 lượt trả lời bằng nguồn sai đối tượng | nhớ: **0 / 6** (từ chối chuẩn 6 / 6 lượt thiếu); độc lập dính bẫy 3 / 6 | đạt |
| **S2** từ chối nhầm nhớ ≤ độc lập + 1 | nhớ **0 / 19** ↔ độc lập 5 / 19 | đạt |
| theo dõi | nhớ 19 / 19 lượt bình thường trích đúng đối tượng; `khan_cap` 0; usage − builder max 56 | — |
**A quyết bật nhớ** (User: "sửa trên bộ mới rồi bật", "đạt ⇒ bật") ⇒ B141 `7a76ba2`.

**Cổng nhỏ B141** (uvicorn cổng 8853, `settings.yaml` thật của nhánh — nhớ bật; `data/phase_9/b3b/cong_b141/`): test file chạm (`test_b3_memory`, `test_b2_tool_loop`, `test_api_chat`, `test_static_ui`) **35 / 36** (1 = test cần khoá API, bẫy đã biết); `npm ci && npm run build`; `/` 200, `/health` 5 / 5;
chuỗi 3 lượt stream qua cookie thật: lượt 3 nhớ đúng tên đã giới thiệu, lượt 2 "chùa đó" hiểu đúng đối tượng, cùng mã cuộc; "cuộc mới" ⇒ mã mới, hết nhớ; câu ngoài phạm vi đơn lẻ không cookie ⇒ tuyến `ngoai_pham_vi`, câu cố định ngoài phạm vi (`outcome` `out_of_scope`; cấp cookie mới) — review C m-4; Playwright (câu gợi ý ⇒ hỏi tiếp ⇒ cuộc mới) CSP 0, request ngoài 0, điện thoại không cuộn ngang;
**8 dòng `chat_metrics` = 8 lượt**, `n_history_turns` 0 ⇒ 1 ⇒ 2 ⇒ 0 sau cuộc mới; grep tên / chữ câu hỏi / `conversation_id` = 0. Không đo latency. Tiền cổng **0,0028 USD**. TaskStop.

**Giới hạn (bật với các giới hạn này):** (1) n nhỏ — 6 lượt thiếu ở bộ mới, 4 lượt ngoài kho đã thấy; 0 lỗi trên n câu không chứng minh tỉ lệ 0; (2) ca dò tự viết **không tái hiện** được K-N2 và chưa thấy ca "bác tiền đề bằng đúng nguồn" ở bộ mới ⇒ chưa chứng minh trực tiếp câu dặn sửa đúng lỗi kín; (3) **không nhớ câu trả lời** ⇒ câu kiểu "ý thứ hai bạn vừa nói…" chưa hỗ trợ (chưa đo); (4) cookie hết hạn 30 phút âm thầm (giới hạn A giữ từ B3).

## 5b. Lựa chọn trước lượt (a) (đã quyết)

Lựa chọn B thấy (chi tiết trong tin nhắn cho A): (a) theo kết quả âm của plan / tin A — thử `nho_cau_tra_loi: false` (chỉ nhớ câu hỏi) **một lần** trên đã thấy (~0,06 USD) với câu dặn mới; (b) coi câu dặn đạt sàn (Q5 / Q6 / Q3) và chuyển C chạy bộ mới (S1 / S2) kèm Q4 ghi "không đạt trên đã thấy"; (c) gỡ câu dặn, giữ cờ tắt.

**Giải thích ngắn:** thêm một câu dặn cho lượt có lịch sử: chỉ nói điều mà nguồn nói đúng về đối tượng đang hỏi. Câu dặn không làm hỏng việc nhớ tên, câu ngoài kho, cảnh báo, đổi chủ đề; nhưng điểm "hỏi tiếp có nhớ hơn hẳn không nhớ" lần này không vượt ngưỡng (một câu so sánh bị thiếu ý vì lần tìm không ra đoạn của nơi thứ hai). Hai lần chạy cùng cấu hình dao động khá nhiều nên mẫu 20 lượt khó phân biệt; A chọn (a) ⇒ chỉ nhớ câu hỏi + câu dặn: qua mọi luật trên đã thấy; chờ bộ kiểm mới của C.
