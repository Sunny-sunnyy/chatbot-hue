# Review plan B7 lượt đo cuối — B, 15:12 16/11/2026 (vòng 1)

Plan: `docs/superpowers/plans/2026-11-23-phase-9-b7-cuoi-plan.md` trên `origin/p9-b7-cuoi-plan` `d6a7a53`, sha256 đầu `3c44a3782118` (đã kiểm). Căn cứ: plan B7 bản 2 (`2026-11-10-phase-9-b7-plan.md`), code / cấu hình tại `dfd0c96` (giữa kỳ) và `origin/main`, các thư mục đo sửa lịch 15/11. 0 USD, chỉ đọc.

**Kết luận: changes_requested — 0 blocker · 1 major · 5 minor.** Khung đúng: mọi lượt có tìm kho chạy lại vì kho đổi, T đã thấy được dùng lại có căn cứ, lượt A / S bắt buộc vì giữa kỳ phạm sàn, có pilot và thứ tự cắt ghi trước. Major duy nhất là một lượt có thể đo thừa.

## Đã kiểm độc lập (cách khác người viết)
- **Điều kiện dùng lại T đã thấy — ĐÚNG.** Tự tính sha256 các chuỗi lời dặn ở `dfd0c96` ↔ `origin/main` bằng cách nạp `full_corpus_prompt.py` của từng commit: `ROUTER_INSTRUCTIONS` `8cd30cbb359a` = `8cd30cbb359a`, `CHAT_INSTRUCTIONS` `df921574c362` = `df921574c362` (khớp plan). Thêm phần plan chưa kiểm: chuỗi gửi định tuyến còn ghép đoạn theo biến thể `lan_tim_dau` (`generator_openai_full_corpus.py` `ROUTER_OUTPUTS`) — cả hai commit `lan_tim_dau: v0`, `model: gpt-6-luna`, `router_timeout_seconds: 10` ⇒ định tuyến câu trò chuyện giống byte. Cờ `cau_nhieu_y` (bật 14/11) chỉ đổi lời dặn **trả lời** của câu ≥ 2 ý (`assistant.py:789`, `generator…:475`), không chạm câu trò chuyện.
- **Lời dặn mục web ĐÃ ĐỔI** (`TU_WEB_LUAT` `e5f516aa383e` ⇒ `7180f74a00e6`, câu sức khoẻ merge `3a4d5db` 16/11) ⇒ lượt W phải chạy lại — plan đã chạy "đủ", chỉ thiếu ghi lý do này (m-2).
- **Luật ba:** 3 / 44 = 6,8 % — đúng.

## Major

**M-1 — Lượt L phần đã thấy (Q3 10 chuỗi × pass^2 + biểu mẫu bản 2 bộ quyết) có thể đo thừa so với luật "đo đúng chỗ đổi".**
- Bằng chứng: code sửa lịch / xếp lịch đổi lần cuối `79aecf3` (15/11 20:54; `git log -1 origin/main -- backend/llm/sua_lich_v2.py backend/llm/lich_trinh_v2.py backend/llm/len_ke_hoach.py`); Q3 đã chạy nhiều lượt ngày 15/11 (`data/sua_lich_hang_2026-11-15/do/q3*`, `data/sua_lich_ngay_2026-11-15/do/q3_vong1`). Plan B7 bản 2 (dòng 123, "Biểu mẫu lịch trình: dùng lại số 07/11") cũng đã **dùng lại** số biểu mẫu thay vì đo lại. L không đo tìm kho (lịch do code xếp), nên lý do "kho đổi ⇒ chạy lại" của §1 không áp.
- Tác động: ≈ 0,05 USD + thời gian cho số có thể tái dùng; phần đã thấy không giữ sàn nào mà lượt Q3 gần nhất chưa giữ.
- Tiêu chí đóng: L đã thấy + biểu mẫu **có điều kiện** — bước 0 ngày 23/11: tìm sha của lượt Q3 / biểu mẫu gần nhất đạt; `git diff <sha đó> $C_DONG -- backend/llm/sua_lich_v2.py backend/llm/lich_trinh_v2.py backend/llm/len_ke_hoach.py backend/llm/do_so.py` + chuỗi lời dặn hiểu ý sửa lịch giống byte ⇒ **dùng lại** số đó (ghi "dùng lại, lý do"); khác ⇒ chạy như plan. **Giữ L kín** (5 chuỗi chưa từng mở — số duy nhất không lạc quan cho kết luận (ii) lịch trình; rẻ). Ghi lại ước tiền khi L đã thấy được dùng lại.

## Minor
- **m-1 §1 record build cũ.** "build record `af5e225c497e`" là bản 14/11; hiện hành `1b53af26b662` (sửa kho Tây Sơn 15/11) và tối nay đổi tiếp (ghi kho Lập An 2 bài). Kết luận "chạy lại mọi lượt có tìm kho" không đổi. Đóng: bước 0 ghi record sha + số point lúc chạy vào report (một dòng), bỏ con số cứng.
- **m-2 §1 thiếu lý do W.** Thêm một dòng: `TU_WEB_LUAT` đổi 16/11 (câu sức khoẻ) ⇒ W chạy lại dù không có kho; và cờ `cau_nhieu_y` / `web_cau_noi_tiep` đổi luật mở cổng web.
- **m-3 Ước tiền lượt A có vẻ thấp.** 32 câu × (agent ×2 + RAG ×1) = 96 lượt × 0,0007 ≈ 0,067, plan ghi 0,045 (có thể RAG rẻ hơn — ghi đơn giá RAG riêng). Pilot đã có luật "vượt > 50 % ⇒ dừng" nên không chặn; đóng: ghi phép nhân từng lượt cạnh cột USD.
- **m-4 Thứ tự cắt (1) nên thành mặc định.** S đã thấy 44 câu chạy ×2 trong khi sàn S2b đọc trên câu mở cổng web (2 câu giữa kỳ); lượt thứ hai của phần đã thấy không giữ thêm sàn nào ngoài độ ổn định mà S kín ×2 đã đo. Đề nghị: S đã thấy ×1, S kín ×2 ngay từ đầu (~ −0,01).
- **m-5 Bước 0 kiểm thêm cấu hình, không chỉ sha lời dặn.** Ghi rõ bước 0 so cả `lan_tim_dau`, `model`, `router_timeout_seconds` giữa `dfd0c96` và `$C_DONG` (phép kiểm của review này) — để điều kiện dùng lại T đủ, không chỉ 3 sha.

## Không phải finding (đã cân)
- §3 nhãn lỗi tự động + luật ba: 0 USD, có ca đối chứng biết chắc ra "có" (file giữa kỳ) — đúng luật phép kiểm harness. Giữ.
- §3 bỏ thử mất mạng — đúng §8. §4 ba lệnh đếm kín giữ đuôi chỉ in số đếm. §6 câu 2 (đưa L vào (ii)): đồng ý **có**, với điều kiện M-1.
- Không thấy bộ nào không giữ sàn ngoài M-1 / m-4.
