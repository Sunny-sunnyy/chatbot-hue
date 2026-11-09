# Implementation Report: Phase 9 T4 — lịch trình từ câu gõ tự do — **ÂM ở Q3 (ii) "hợp người đi cùng"**

Người làm: E (Claude Code, `hue-rag-ea`) · 22:17 09/11/2026 (`date`) · A giao 09/11 · review sớm: C (`c_t4_lich_review.md`)
Plan `docs/superpowers/plans/2026-11-09-phase-9-t4-lich-trinh-plan.md` bản 2a (A duyệt; sha cuối A ghi handoff). Ghi trước lượt có phí: `data/phase_9/t4/tieu_chi.md`.
Nhánh `p9-t4-lich` **`9481904`** (push; rebase trên `main` `8e3abc2` — G phương án B + **cờ ngày bật**). Cờ `lich_trinh` **tắt**.

## 1. Thay đổi (plan §1, code — không đổi lời dặn)
- (a) `lich_trinh.chot_so_ngay`: số ngày code dò được trong câu thắng tham số model (trước: lệch ⇒ hỏi lại).
- (b) `assistant._finish_generated`: lượt có lịch, model trả câu từ chối sau khi `tim_kho` bị chặn ⇒ lời lịch tối thiểu (B171) + câu cố định `CAU_HOI_THEM_CHUA_CO`.
- (c) log công cụ `lich_trinh` ghi `so_ngay_model` / `so_ngay_do`.
- Test: `test_b5_lich_trinh.py` 247 passed; Q1 cờ tắt 228 / 228 giống byte; test rộng sau rebase 826 passed (hỏng = 4 test cần khoá + 3 test giao diện thiếu `frontend/dist` ở worktree).

## 2. Lượt có phí (1 lượt; 31 câu chỉ nhánh; sàn chung nhánh ↔ mốc `8e3abc2`)
Công cụ: `data/phase_9/t4/tools/do_t4.py` (31 câu, `answer_turn` thật, web thật) + `data/phase_9/t2_web/tools/do_t2.py` (an toàn / mẫu 30 / `s2`). Kết quả `data/phase_9/t4/ket_qua/`, chấm `data/phase_9/t4/cham/`.

| Tiêu chí (ghi trước) | Kết quả | |
|---|---|---|
| **Q3** cả 3 tiêu chí ≥ 26 / 27 (2 người chấm) | (i) đúng luật xếp 26 · 24 · (ii) **hợp người đi cùng 21 · 15** · (iii) có nguồn 26 · 26; đạt cả 3: **21 · 14 / 27** | **trượt** |
| K2 hỏi lại thừa khi dò được số ngày | 0 | đạt |
| E20 "từ chối thay cả lịch" | 0 (27 / 27 có lịch) | đạt |
| (b) không nói sai (19 câu không hỏi kèm) | 0; câu cố định chỉ ở câu hỏi kèm (5 / 8) | đạt |
| Q2 khung 0 lỗi · kiểm cuối 0 lọt | khung 0; kiểm cuối **bắt** 1 (E20_A3: model ghi số tiền ⇒ rút lại — không lọt, nhưng người dùng không thấy lịch ⇒ Q3 không đạt) | đạt (Q2) |
| S1 an toàn 32 (nhánh ×2 ↔ mốc ×1, 2 người, S-AT) | đảo 0 · sai điều kiện mới 0 · thiếu cảnh báo **mới** 0 (S27 người 1 chấm thiếu ở **cả** nhánh lẫn mốc) · ngoài kho 0 | đạt |
| S2 / S2b (`s2` 44) | S2 0; S2b 2 — `b_dt_12` (đã biết, y tế ⇒ định tuyến khẩn cấp) + `b_dt_20` (định tuyến **lỗi** đúng lượt ⇒ đường dự phòng `tro_ly_hue`; lượt mốc G: chặn đúng) | không do T4 |
| S3b · `max_turns` · citation | 0 · 0 · 0 (trừ rút lại E20_A3) | đạt |
| S4 mẫu 30 (1 người, mù cặp) | đúng: nhánh +1 / 29 ngang · đủ: nhánh +2 / −3 ⇒ tụt ròng 1 < 3 | đạt |

- **Hai người chấm cùng "không" ở (ii):** L4, L5, M2, M4, M5, E20_A3. Gốc lỗi **ở luật xếp / bảng điểm B5, không ở sửa (a)–(c)**:
  - "đi dày" vẫn 2 điểm / ngày (L5, M5) — đã biết: bảng thiếu cột thời lượng (phiếu v7);
  - sở thích nói bằng lời ("đi dạo, ăn uống, 1 lăng") không vào `so_thich` ⇒ lịch không theo (M2);
  - luật "tối không xếp cho người lớn tuổi" bỏ cả điểm kho ghi hợp người lớn tuổi (L4);
  - người dùng lo mưa ⇒ lịch vẫn nhiều điểm ngoài trời ven nước, không nhắc cảnh báo mùa mưa kho có (M4).
- **Ghi nhận (không trừ điểm, đúng giới hạn plan):** giờ tới / về bị bỏ (M2, M8, E20_A5, E20_A6 — đã biết); câu hỏi kèm chỉ nhận câu cố định (đúng thiết kế (b)).
- **Tiền thật:** 31 câu 0,026855 · sàn nhánh 0,047927 + 0,023929 · mốc 0,037363 = **0,136074 USD** (≤ dừng 0,2). Chấm: sub-agent (0 USD API).

## 3. Kết luận + đề xuất (A quyết)
- **Âm** theo luật ghi trước (Q3 (ii)). Sửa (a)–(c) **làm đúng việc của nó** (K2 0, từ chối thay lịch 0, câu cố định không nói sai) — nhưng câu gõ tự do còn yếu ở phần **xếp hợp nhu cầu**, do luật xếp / bảng điểm.
- Spec §12.2 phương án B: **giữ biểu mẫu "Lên kế hoạch" là đường lịch trình duy nhất**, `lich_trinh` tắt. Bậc "câu gõ tự do ⇒ code gợi ý mở biểu mẫu" **chưa** đề xuất làm: chưa có số người dùng thật gõ câu xin lịch (log không ghi chữ) — nếu muốn, đo rẻ trước bằng đếm `route` + công cụ trong `chat_metrics` khi có người dùng.
- Code (a)–(c): (1) **merge cờ tắt** — nhỏ, Q1 giống byte, test đạt; dùng lại khi bảng điểm có thời lượng / sở thích tự do; hoặc (2) **đóng hồ sơ** tag `hoso/p9-t4-lich`. E nghiêng (2) cho gọn (mã không chạy khi cờ tắt; luật 09/11 "không làm thì mất gì": mất 0 với người dùng hiện tại).
