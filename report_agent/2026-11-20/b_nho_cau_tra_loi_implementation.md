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

## Thêm 15:14 21/11/2026 (giờ `date`) — làm tiếp sau khi model viết đổi sang Sonnet: sàn 1, lượt tự kiểm, hai thay đổi nhỏ. Cờ vẫn TẮT.

**Sàn 1 [máy kiểm]:** cờ tắt, 228 chuỗi gửi model (đường luna) trên nhánh giống từng byte main (cùng mã băm `fd8382fa…`).

**Lượt tự kiểm của người viết** (7 chuỗi hai lượt TỰ ĐẶT, mong đợi ghi trước; qua đúng lệnh chạy chuỗi của phiên đo; hai model; tắt ↔ bật; không phải bộ đích của phiên đo, không phải bộ bẫy 03/11 — hai bộ đó tôi không mở).
Đọc lượt 2 và đối chiếu với danh sách ở lượt 1 của chính lần chạy đó:

| Kiểu câu hỏi tiếp | luna: tắt ⇒ bật | Sonnet high: tắt ⇒ bật |
|---|---|---|
| "Quán thứ hai bạn vừa nói ở đường nào" | nêu SAI quán (nói chắc) ⇒ đúng quán | từ chối ⇒ đúng quán |
| "Ý thứ hai bạn vừa nói, giải thích rõ hơn" | từ chối ⇒ đúng ý | từ chối ⇒ đúng ý |
| "Cái đầu tiên trong danh sách cách trung tâm bao xa" | từ chối ⇒ đúng | đúng ⇒ đúng |
| "Con số bạn vừa nói là cho một người hay cả nhóm" (giá vé) | đúng ⇒ đúng | đúng ⇒ đúng |
| Đối chứng: câu không liên quan lượt trước | giống hệt | giống hệt |
| Bẫy tự đặt: số điện thoại của "quán đầu tiên" (kho không có) | từ chối ⇒ từ chối | từ chối ⇒ từ chối (không mượn số quán khác) |

⇒ 5 lượt hỏng (4 từ chối, 1 sai) thành đúng; 0 lượt đúng thành sai ở các kiểu này. 0 lỗi kỹ thuật, 0 lỗi trích dẫn.

**Một kiểu câu XẤU ĐI ở bản đầu, đã đổi thiết kế (phiên điều phối chọn):** hỏi tiếp về con số DỰ BÁO vừa đưa ("con số khả năng mưa bạn vừa đưa là cao hay thấp?") trên Sonnet — có câu trả lời cũ trong lịch sử thì
model tự từ chối 8 / 10 lần (con số đã nằm trong lời "không phải nguồn" nên model không gọi lại công cụ thời tiết), không có thì 0 / 6. luna không bị.
**Đổi:** lượt đã dùng công cụ / nguồn đổi theo giờ (dự báo, ngày - lịch âm, sự kiện theo ngày, khoảng cách, lịch đã lưu) KHÔNG được giữ đáp — cùng luật với bộ nhớ câu trả lời giữa các cuộc. Sau đổi, chạy lại:
Sonnet 4 / 4 lượt trả lời (0 từ chối); luna 3 / 3 ở cả hai bên. Lượt tìm kho, tra web, liệt kê bài vẫn giữ đáp.
**Giới hạn mới:** sau một lượt thời tiết / ngày / khoảng cách, câu trỏ ngược bằng thứ tự ("ý thứ hai bạn vừa nói") không hiểu được — chưa thấy ca nào như vậy trong sổ vết hay các bộ đã chạy.

**Trần cắt câu trả lời được nhớ: 1.200 ⇒ 4.000 ký tự.** Câu trả lời lượt 1 của Sonnet dài hơn 1.200 ở 2 / 7 chuỗi (1.283 và 1.422; dài nhất cả ngày 2.229); luna 0 / 7. Giữ một trần để bộ bẫy đọc được trên lượng chữ có giới hạn.

**Lớp dịch Sonnet:** không sửa. Thêm một test khẳng định thân gửi có CHỮ THẬT của câu trả lời ở cặp lượt cuối và dòng giữ chỗ ở các cặp cũ hơn.
Test: `tests/test_nho_dap_lien_truoc.py` 20 ca; 7 file chạm trí nhớ hội thoại / lớp dịch đạt. Tiền lượt tự kiểm: 1,4 USD (gần hết Sonnet) + các lượt phát lại ≈ 0,5 USD.

**Còn lại trước khi được bật (không đổi so với plan):** bộ bẫy 03/11 (phiên khác chạy + chấm) · bộ đích của phiên đo + các mục "quên câu trả lời trước / câu cụt đại từ" của bộ câu khó · người thứ hai đọc tay lượt đích
(0 nhận định chỉ có trong câu trả lời trước) · một lượt trình duyệt. Điểm nối chưa đo: phép kiểm số không nhận số chỉ có ở câu TRẢ LỜI trước — sau thay đổi trên, lượt thời tiết / khoảng cách không còn được nhớ nên
tình huống đó hẹp lại còn "số trong câu trả lời từ kho" (giá vé…), vốn không qua phép kiểm số.
