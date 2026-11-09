# Plan T2 — tra web thành công cụ agent tự yêu cầu (Phase 9 bản 13, đợt 2)

> **Bản 2 — chờ A đọc duyệt (mức nhẹ).** C · 20:51 09/11/2026 (`date`), viết lại bản nháp của B (`921f75d64a7c`, B 12:29 08/11/2026) theo review
> `2026-11-08-phase-9-t2-web-plan_review.md` (3 major, B đồng ý) + chốt vòng tự soi 09/11 (A: sàn chỉ S1 + ngoài kho / ngoài phạm vi + đúng câu; S5 / S6 đo chung lúc đóng
> đợt; không bộ kín). Tiền ≈ 0,18 ≤ 0,2 ⇒ mức nhẹ (`Session_Prompt.md` §7): A đọc duyệt, không review plan; đo 1 lượt (bộ an toàn 32 ×2); 1 review cả nhánh. Chưa code.

Spec `2026-11-02-phase-9-design.md` §12 (User duyệt `5557f0fd7650`): hàng T2 §12.2, thiết kế §12.5, rà §12.6, User xác nhận §12.8 — **agent chỉ quyết lúc tra**; code
dựng câu tra, tra **sau** câu kho, viết mục web riêng "Từ web (chưa kiểm)"; agent **không** đọc chữ web. **Nền:** `main` sau G (cổng 2 nhóm; nếu G đi phương án B thì nền
là bản đó) — nhánh `p9-t2-web` tách từ đúng sha G đã đo. Code chờ G vào `main`.

## 1. Đổi gì (một bậc, cờ mới `tra_web_cong_cu: false`)

1. Công cụ `yeu_cau_tra_web()` **không tham số**, đưa cho agent Huế ở **mọi** lượt `tro_ly_hue` có công cụ khi `tra_web` ∧ `tra_web_cong_cu` (lượt biểu mẫu, lượt có lịch,
   lượt ghép `truong` không đưa). Code: đặt `trace.web_yeu_cau = True` (trường của `AnswerTrace` ⇒ `_merge_spec` của #6 chép sang), trả **câu cố định trung tính**
   "Đã ghi nhận — viết câu trả lời từ kho như bình thường." (không hứa mục web — tra có thể lỗi / rỗng, B6 D3). Trần 1 lần / câu (lần 2 trả cùng câu, không đổi gì).
   Mô tả công cụ (chốt nguyên văn trước khi có bộ hỏi kèm, ≤ 2 câu): "Gọi khi câu hỏi về Huế có một phần mà Bằng chứng không có thông tin (vd giá hiện tại, sự kiện mới).
   Không gọi khi Bằng chứng đã đủ trả lời, hoặc câu hỏi không về văn hoá / du lịch Huế."
2. **Số vòng tối đa (review M-1):** công cụ gọi lần lượt (`parallel_tool_calls=False`) ⇒ ăn một vòng riêng; chuỗi xấu nhất tìm ×2 + "hết lượt" + yêu cầu web + viết = 5 > 4
   ⇒ chạm trần ⇒ outcome `max_turns` (mất cả câu kho lẫn web). Sửa: `max_turns_for(ngay_lich_fn, web_fn=None)` (`generator_openai_full_corpus.py`) +1 khi lượt có
   `yeu_cau_tra_web`, cộng dồn với +1 của T1; giá trị không vào thân yêu cầu ⇒ chuỗi gửi model khi cờ tắt không đổi.
3. `web_gate_open` (**một chỗ**, `assistant.py`): thêm nhánh `flags.tra_web_cong_cu ∧ trace.web_yeu_cau ∧ fixed_outcome is None ∧ citation_error is None ∧ answer ∉
   REFUSAL_ANSWERS` (+ mọi điều kiện cũ: tuyến `tro_ly_hue`, chưa tra, không lịch, không lượt ghép). G đặt outcome `out_of_scope` khi chữ = `OUT_OF_SCOPE_ANSWER` ⇒ đã đóng
   bằng `fixed_outcome`; điều kiện chữ giữ cho đường chưa qua G. Cổng cũ (sau câu "không đủ thông tin") giữ nguyên.
4. Không đổi: `cong_web` của B6 (câu tra = câu hỏi lượt này `tw.cau_tim_web`, một lần Serper, lần gọi riêng không công cụ / không lịch sử viết mục, mọi kiểm cuối B6),
   `TU_WEB_LUAT` (giữ tiền đề "kho không có" — xem §2 quan sát Q-K), #6 (phần chạy song song không tra web; cổng chạy sau gộp), log không chữ (`tools` thêm mục
   `yeu_cau_tra_web`).
5. **Test 0 USD** (`backend/tests/test_t2_web_cong_cu.py`, SDK thật + client kịch bản như `test_b6_tra_web.py`):
   - (4c) mô tả công cụ có ở lượt đầu / lượt có lịch sử khi cờ bật; không có ở lượt biểu mẫu / lượt ghép; cờ tắt ⇒ chuỗi gửi model giống byte `main` (Q1 `capture_all.py` 1 lượt).
   - Cổng 4 ca × **3 đường** (`answer_turn`, `answer_turn_stream`, #6 `answer_turn_stream_parallel`): yêu cầu ∧ câu trả lời thường ⇒ mở · yêu cầu ∧ `OUT_OF_SCOPE_ANSWER` ⇒ đóng ·
     không yêu cầu ∧ câu trả lời thường ⇒ đóng · "không đủ thông tin" ⇒ mở như cũ; + 1 ca lượt ghép `truong` ⇒ đóng; trần 1 lần.
   - Chuỗi xấu nhất (tìm, tìm, tìm "hết lượt", yêu cầu web, viết) ⇒ không chạm trần.

## 2. Tiêu chí ghi trước (1 lượt, cùng lượt với mốc khi cần mốc)

| Sàn (chặn merge) | Bộ | Mức |
|---|---|---|
| **S1** an toàn | an toàn 32, ×2 | 4 số như G (đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 · ngoài kho bị trả lời 0; S-AT khi chênh 1) |
| **S2 / S2b** ngoài phạm vi bị trả lời / có mục web | `s2` 44 (G) + 4 câu "ngoài Huế" của B6 | **0 / 0** |
| **S3b** câu về Huế bị trả `OUT_OF_SCOPE_ANSWER` | mọi lượt cả câu ở trên + mẫu 30 + B6 24 câu Huế | **0** (code so chuỗi) |
| **Tra web khi kho trả lời được** | mẫu Golden 30 + 4 câu `kho_co` của B6 (nằm trong bộ 28) | **0 / 34** |
| **Câu kho nhắc mục web** (chữ model có "web" / "bên dưới" / "tra thêm") | mọi lượt | **0** (code đếm) |
| **`max_turns`** (review M-1) | mọi lượt | **0** (code đếm outcome) |
| **Câu hỏi kèm có phần web** (review M-3) | bộ hỏi kèm 10 (§3) | biến thể ≥ mốc + 2 / 10 |
| **S2c** câu Huế kho thiếu vẫn có web | 10 câu `web_tra_loi_duoc` của B6 | cổng mở ≥ mốc − 1 |
| **Mục web đúng luật B6** | B6 28 + bộ hỏi kèm 10 | 0 link ngoài sổ · 0 số / tiền ngoài đoạn trích · câu thiên tai cố định (`data/phase_9/b6/tools/cham_b6.py`) |
| **S4** chất lượng câu Huế (mô tả công cụ vào mọi lượt — bài học B5c) | mẫu 30 biến thể ↔ mốc, chấm mù **1 người** (tự soi 09/11: 2 người khớp 100 % hai lượt trước) | tụt < 3 / 30 |

- **"Có phần web" (M-3), đếm bằng code:** lượt có `trace.web` ∧ `web.outcome == "co_muc"`. Mốc đếm cùng cách (ở mốc web chỉ mở khi kho từ chối cả câu).
- **Quan sát, không sàn:** **Q-K** "mục web nói khác câu kho" ở bộ hỏi kèm 10 (1 sub-agent đọc; review ghi chú 1 — `TU_WEB_LUAT` giữ tiền đề "kho không có", câu tra = cả câu
  hỏi); số lần model gọi công cụ / bộ; USD / câu (S6) và chữ đầu (S5) ghi số — **S5 / S6 đo chung một lượt lúc đóng đợt** (chốt tự soi 09/11).
- **Đạt** = mọi sàn trên. Âm ⇒ ≤ 1 vòng chỉnh mô tả công cụ trên bộ đã thấy (spec §12.4), rồi **phương án B** (spec): giữ cổng B6 (chỉ sau câu từ chối), thêm cổng cho câu
  "từ chối + đã hỏi kèm" do **code** nhận.

## 3. Bộ đo

- Có sẵn: `s2` 44 (G), B6 đã thấy 28 (`data/phase_9/bo_do_b6/cau_da_thay.jsonl` — `loai`: 10 `web_tra_loi_duoc` · 6 `khong_xac_minh` · 4 `ngoai_hue` · 4 `kho_co` · 2
  `theo_ngay` · 2 `ten_trong_cau`), mẫu Golden 30 (`data/phase_9/bo_do_b1/mau_golden_30.json`), an toàn 32 — công cụ `data/phase_9/g_cong/tools/do_g.py` `ca_cau` (web thật,
  có `context` cho S1).
- **Bộ hỏi kèm 10 (mới, đã thấy — không kín):** `data/phase_9/t2_web/hoi_kem_10.jsonl`. Người viết: **E** (không viết / không chỉnh mô tả công cụ). Mỗi câu: hỏi về Huế
  có **một phần kho trả lời được** + **một phần kho không có** mà web có thể có (giá hiện tại, sự kiện năm nay, dịch vụ mới…); không câu khẩn cấp / thiên tai / lưu trú cụ thể
  (đã có luật riêng). Trường: `id`, `cau`, `phan_kho`, `phan_web` (mô tả loại phần, không đáp án). Người viết kiểm phần kho bằng `scripts/grep_kb.sh`. **md5 ghi vào đây trước
  lượt có phí**; không sửa bộ sau khi thấy số.
- Mốc (`main` sau G, cùng lượt): bộ hỏi kèm 10 + 10 câu S2c. S1 / S4 mốc **dùng lại lượt G** khi nhánh tách từ đúng sha G đã đo (cờ T1 / T3 tắt, Q1 giống byte) — ghi nhãn
  "dùng lại" + lý do; sha khác ⇒ chạy mốc mẫu 30 (+ 0,018).

## 4. Tiền (giá `gpt-6-luna`, đơn giá B6 / G)

Biến thể: B6 28 × 0,0018 = 0,050 · hỏi kèm 10 × 0,0018 = 0,018 · mẫu 30 × 0,0006 = 0,018 · an toàn 32 × 2 × 0,0006 = 0,038 · `s2` 44 × 0,0005 = 0,022 ⇒ **0,146**.
Mốc: hỏi kèm 10 + S2c 10 × 0,0012 = **0,024** (+ 0,018 nếu không dùng lại được S4 của G). **Tổng ≈ 0,17 (≤ 0,19).** Dừng 0,25 ⇒ báo A. Ghi `usd` thật từ log.
S5 / S6 không tính ở đây (lượt chung lúc đóng đợt).

## 5. Rà ngắn (spec §12.6 đã rà — chỉ phần chạm)

Đường ra Serper nay theo **phán đoán model** (lúc tra), nhưng truy vấn vẫn do code dựng từ câu lượt này, chữ web không vào agent chính ⇒ bộ ba chết người không mở;
câu ngoài phạm vi bị chặn ở code (outcome `out_of_scope` của G / chữ ∈ `REFUSAL_ANSWERS`) + S2b; lệnh lái trong câu người dùng ("tra web đi…") vẫn ≤ 1 lần / câu (bộ `s2`
có câu lệnh lái). Số lần ra Serper tăng (mọi câu model yêu cầu, không chỉ câu từ chối) — ghi số lần / bộ. Deploy: `tra_web` / `tra_web_cong_cu` tắt trên AWS.
