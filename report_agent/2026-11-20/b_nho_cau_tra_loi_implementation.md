# B — mục [8] nhớ câu trả lời LIỀN TRƯỚC trong một cuộc trò chuyện: code + test xong, CHƯA đo có phí, cờ TẮT (ghi 16:37 20/11/2026, giờ `date`, lúc kết phiên)

Plan đã duyệt: `report_agent/2026-11-20/b_nho_cau_tra_loi_plan.md` (phương án bản nhỏ nhất; phiên điều phối quyết chiều 20/11). Nhánh `p9-b-nho-cau-tra-loi` — KHÔNG gộp.

**1. Người dùng thấy gì khác (khi cờ `nho_cau_tra_loi` bật — hiện TẮT, nên hôm nay không khác gì).** Hỏi tiếp kiểu "quán thứ hai bạn vừa nói ở đường nào", "chia ra mỗi người bao nhiêu" thì trợ lý nhìn thấy
câu trả lời vừa rồi của chính mình để biết đang nói nơi nào / con số nào. Hiện các câu này bị từ chối (đếm trên sổ vết: 3 / 122 lượt hỏi tiếp).

**2. Đã sửa** (mọi thứ ở lớp ngoài, lõi `llm/assistant.py` không đổi hành vi, lời dặn hệ thống không đổi):
- `backend/api/conversations.py`: hằng `NHAN_LOI_TRUOC`, `CAT_LOI_TRUOC` (1.200 ký tự); `loi_luot_truoc` (nhãn + chữ đã bỏ mã trích dẫn, cắt); `dap_duoc_nho` (chỉ lượt hỏi đáp thường trả lời được — KHÔNG giữ câu cố định,
  lượt lịch / biểu mẫu / sửa lịch vì chữ lịch có tên quán từ bản đồ mở); `ConversationStore(chi_dap_lien_truoc=…)`: lượt vừa xong giữ câu trả lời, có lượt mới thì ô của nó về dòng ghi chú tên nơi (hoặc rỗng).
- `backend/api/routes/chat.py` `_remember`: đưa chữ rỗng cho lượt không được giữ đáp. `backend/api/app.py`: cờ `nho_cau_tra_loi` nay bật chế độ mới (`keep_answers` cũ — nhớ đáp cả ba lượt — nơi dựng app không bật nữa;
  tham số còn trong lớp vì ba file test cũ gọi, B không dọn ngoài phạm vi). `backend/evaluation/full_corpus_eval.py` (lệnh chạy chuỗi `chuoi`): dùng đúng kho + luật giữ đáp như route.
- `backend/config/settings.yaml`, `backend/llm/assistant.py`: chỉ chữ chú thích (cờ vẫn `false`).

**3. Bằng chứng [máy kiểm, test bằng đồ giả — CHƯA có người thứ hai, CHƯA có lượt thật]:**
- `tests/test_nho_dap_lien_truoc.py` 12 đạt: lượt hai nhận đúng một tin trợ lý = nhãn + câu trả lời lượt một đã bỏ `[1]`; lượt ba chỉ thấy đáp lượt hai (đáp lượt một không còn); cờ tắt ⇒ không lượt nào thấy nhãn;
  cắt ở 1.200 ký tự; bảy loại lượt được / không được giữ đáp; câu xin kể lại và câu gõ lại không làm mất câu trả lời liền trước. (Đọc chuỗi gửi model thật qua SDK thật + client dựng sẵn; tìm kho thật.)
- File cũ chạm trí nhớ hội thoại: `test_b3_memory` 13 · `test_nho_ten_goi_y` 19 · `test_cache_tra_loi` 25 · `test_b6_tra_web` 162 — đều đạt (Python 3.13 của cây chính, từng file).
- CHƯA chạy: 228 chuỗi "cờ tắt giống byte" (sàn 1 — theo đọc code cờ tắt đi đúng nhánh cũ, nhưng chưa chạy lệnh) · `test_api_chat`, `test_chat_stream` · cả bộ test.

**4. Chỗ gặp nhau với tính năng khác (phiên điều phối hỏi) — đều là ĐỌC CODE + test đồ giả, chưa đo thật:**
- Bộ nhớ câu trả lời GIỮA các cuộc trò chuyện (cờ `cache_cau_tra_loi`, đang bật): chỉ tra / lưu ở lượt ĐẦU (lịch sử rỗng) ⇒ lượt hai trở đi không chạm, vẫn đúng. Lượt đầu trúng bản lưu thì câu trả lời đó được nhớ làm "lời lượt trước" như lượt thường.
- "Nhớ tên nơi vừa trích" (cờ `nho_ten_goi_y`): lượt LIỀN TRƯỚC chỉ mang câu trả lời, KHÔNG kèm dòng ghi chú (không nói hai lần); lượt cũ hơn mang dòng ghi chú như hiện nay.
- Câu xin "kể lại các nơi vừa nêu": dòng ghi chú của lượt cũ vẫn bị gỡ, câu trả lời liền trước được GIỮ (danh sách thật nằm ở đó) — khác hôm nay (hôm nay lượt đó không thấy gì).
- "Gõ lại nguyên văn câu cũ" (lỗi hỏi A ⇒ hỏi B ⇒ gõ lại A thì trả lời B, sửa 20/11): luật gỡ ghi chú giữ nguyên; nhưng nay lượt B (liền trước) có câu trả lời trong lịch sử — CHƯA BIẾT model có lại trả lời B không ⇒ PHẢI có chuỗi này trong lượt đo.
- Câu hỏi nối tiếp ra web (cờ `web_cau_noi_tiep`): câu tìm web do model viết nay có thể mang chi tiết của câu trả lời trước (đều là chữ từ kho) — chủ dự án đã nghe và chọn bật việc "chữ model mang chi tiết lượt trước ra web" (15/11); nêu lại để người đọc biết phạm vi rộng hơn một chút.

**5. Còn lại trước khi được bật (theo plan mục 4):**
1. Chạy sàn 1 (228 chuỗi): `cd backend && env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --no-sync --project /home/minhhieu/hue_rag python ../data/phase_9/b2_chay/tools/capture_all.py <out.jsonl>` trên nhánh và trên main, `cmp`.
2. Bộ đích của phiên E ĐÃ CÓ: `data/nho_cau_tra_loi_2026-11-20/E_bo_dich.md` (12 chuỗi đích + 5 đối chứng; B CHƯA mở). Phải đổi sang khuôn `.jsonl` của lệnh `full_corpus_eval chuoi` (mẫu khuôn: `data/phase_9/bo_do_b3/chuoi_da_thay.jsonl`) rồi chạy hai bên bật ↔ tắt cùng buổi — ước 68 lượt ≈ 0,07 USD.
3. Bộ bẫy 03/11 `data/phase_9/bo_do_b3b/`: phiên C chạy và chấm (B không mở). Thêm chuỗi "hỏi A ⇒ hỏi B ⇒ gõ lại A".
4. Người thứ hai (C) đọc tay "0 lượt lấy câu trả lời cũ làm nguồn"; C review cả nhánh; một lượt thật qua trình duyệt. Lượt có phí cần phiên điều phối xếp lượt máy. Trần 0,15 USD; đã tiêu 0.

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm + đầu ra |
|---|---|---|---|
| code chế độ "chỉ đáp liền trước" + test + chú thích cờ | sàn 1 · lượt đo có phí · review · lượt thật · bật cờ | kết phiên theo lời chủ dự án; lượt có phí chờ lượt máy | `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_nho_dap_lien_truoc.py -q -p no:cacheprovider` ⇒ `12 passed` |
