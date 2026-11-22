# Plan (một trang) — mục [8] nhớ CÂU TRẢ LỜI trong một cuộc trò chuyện (B, 16:28 20/11/2026, giờ `date`; nền main `f20c4765`; chờ phiên điều phối quyết — có cả phương án "giữ tắt")

**Từ dùng:** *hỏi tiếp* = lượt thứ hai trở đi của một cuộc trò chuyện · *sổ vết* = bản ghi debug có nội dung từng lượt chạy qua hệ thống thật ở máy này (`data/debug_trace/`, riêng tư) · *mượn nhầm đoạn* = lỗi 03/11: trợ lý
lấy đoạn kho của NƠI KHÁC để trả lời một câu hỏi tiếp mà kho không có đáp án (câu ngoài kho bị trả lời — phạm sàn) · *dòng ghi chú tên nơi* = cờ `nho_ten_goi_y` (19/11): lịch sử mang TÊN các nơi lượt trước đã trích.

**1. Hồ sơ lần đo cũ (vì sao đang tắt)** — `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` dòng 433–440, `report_agent/2026-11-02_phase_9_code/b138_b3b_implementation.md`:
- 03/11 bản nhớ cả hỏi + đáp của 3 lượt: phần kín 1 / 2 lượt ngoài kho bị trả lời bằng đoạn của đối tượng khác ⇒ phạm sàn, cờ không bật. Vòng sửa (thêm câu dặn "mỗi ý phải từ đoạn nói đúng đối tượng"), vẫn nhớ cả đáp:
  đạt mọi sàn nhưng lợi ở câu hỏi tiếp +0,50 [−0,15; +1,20] — khoảng tin chạm 0 ⇒ không đạt luật ghi trước ⇒ đi đường dự phòng "chỉ nhớ câu hỏi": +0,80 [+0,25; +1,50], bẫy từ chối đúng 6 / 6, từ chối nhầm 0 / 19 ↔ 5 / 19 ⇒ bật bản đó.
- Tức là: bản nhớ đáp KHÔNG bị chứng minh là hại sau vòng sửa; nó bị loại vì chưa chứng minh được là LỢI hơn, và hồ sơ tự ghi "không kết luận được bản chỉ nhớ câu hỏi tốt hơn". Giới hạn ghi lúc đó: câu "ý thứ hai bạn vừa nói…" chưa hỗ trợ.

**2. Đếm trên sổ vết 15–20/11/2026 (0 USD; 732 lượt qua hệ thống thật — phần lớn là kịch bản do nhóm gõ, KHÔNG phải người dùng thật)** [máy đếm + B đọc tay từng lượt hỏng]:
- Lượt hỏi tiếp dạng hỏi đáp thường (không lịch, không sửa lịch, không nút): **122**. Trả lời được 98; không ra câu trả lời 24 (17 câu khác nhau).
- 17 câu hỏng chia theo nguyên nhân: kho không có điều được hỏi (số điện thoại, chỗ đậu xe, giờ của một nơi kho thiếu, giá…) 10 · lỗi "gõ lại câu cũ thì trả lời câu khác" đã sửa 20/11: 2 · câu nhờ làm thay (đúng thiết kế): 2 ·
  "gần X": 1 · **cần câu trả lời trước của chính trợ lý: 3** — hai câu trỏ theo THỨ TỰ ("quán thứ hai bạn vừa nói ở đường nào", "quán đầu tiên mở tới mấy giờ") và một câu tính tiếp trên CON SỐ vừa nêu ("chia ra mỗi người bao nhiêu").
- Nhìn từ phía câu hỏi: trong 122 lượt có **6** lượt trỏ vào nội dung câu trả lời trước (5 theo thứ tự, 1 theo con số). 3 bị từ chối (ở trên); 3 trả lời ĐÚNG — một nhờ dòng ghi chú tên nơi, hai vì lần tìm lại tình cờ ra cùng thứ tự
  (B đối chiếu với câu trả lời trước trong sổ vết: đúng nơi đứng đầu). **0 lượt nói chắc mà sai** vì thiếu câu trả lời trước.
- Tóm lại: thiếu "nhớ đáp" làm hỏng **3 / 122 lượt hỏi tiếp (2,5 %)**, đều là TỪ CHỐI, không có câu sai. Dòng ghi chú tên nơi đã có mặt ở 58 / 122 lượt.

**3. Hai phương án — phiên điều phối chọn**
- **(a) Giữ tắt, ghi lý do bằng số trên** (rẻ nhất, 0 rủi ro): mất 2,5 % lượt hỏi tiếp kiểu "quán thứ hai…", người dùng nhận câu từ chối chứ không nhận câu sai; hỏi lại bằng TÊN quán thì được.
  Sai khi: người dùng thật trỏ theo thứ tự nhiều hơn kịch bản của nhóm (sau một câu trả lời dạng danh sách đây là cách hỏi tự nhiên) — chưa có số người thật.
- **(b) Bản nhỏ nhất, B nghiêng về phương án này vì mục này chủ dự án ghi "bắt buộc (hỏi + đáp)" 02/11 và lỗi rơi đúng vào kiểu hỏi tự nhiên sau danh sách — nhưng CHỈ bật khi qua sàn dưới:**
  - Chỉ gửi kèm câu trả lời của lượt LIỀN TRƯỚC (không phải 3 lượt), đã bỏ mã trích dẫn `[n]` (hàm `stored_answer` có sẵn), cắt ở 1.200 ký tự, đứng sau một dòng nhãn cố định do code viết:
    "[Lời trợ lý ở lượt trước — chỉ để hiểu câu hỏi tiếp; KHÔNG phải nguồn, không được trích hay coi là bằng chứng]". Các lượt cũ hơn vẫn chỉ có câu hỏi + dòng ghi chú tên nơi như hiện nay.
  - KHÔNG đổi lời dặn hệ thống (lời dặn lịch sử hiện có đã ghi "lịch sử chỉ để hiểu câu hỏi nói về đối tượng nào; mỗi nhận định phải lấy từ Bằng chứng…") ⇒ lượt không có lịch sử và mọi lượt khi cờ tắt giống từng byte.
  - Chỗ sửa: `backend/api/conversations.py` (`ConversationStore.append` / `history`: giữ đáp của lượt cuối, hạ về dòng ghi chú khi có lượt mới) — ước ~25 dòng + test; dùng lại cờ `nho_cau_tra_loi` với nghĩa MỚI này,
    bỏ nghĩa cũ "nhớ đáp cả 3 lượt" (đã đo, không dùng). Phải đọc `backend/llm/ten_goi_y.py` `lich_su_cho_luot` trước khi viết (lượt "kể lại các nơi vừa nêu" đang gỡ dòng ghi chú — hai cơ chế gặp nhau ở cùng một ô lịch sử).
  - Không chạm: bộ nhớ câu trả lời giữa các cuộc trò chuyện (chỉ lượt đầu), lịch đã lưu, mục web (chữ web vốn không vào lịch sử).

**4. Tiêu chí ghi TRƯỚC (cho phương án b)** — cặp bật ↔ tắt chạy CÙNG BUỔI; người viết không tự chấm; trần tiền 0,15 USD
- Sàn 1 — cờ tắt: 228 chuỗi gửi model giống byte main; chuỗi lịch sử của bộ chuỗi đã thấy giống byte.
- Sàn 2 — lỗi đã làm tắt: bộ bẫy của 03/11 (`data/phase_9/bo_do_b3b/`, 12 chuỗi, 6 lượt bẫy; phiên KHÁC chạy và chấm, B không mở): bên bật từ chối đúng **6 / 6**; 0 lượt ngoài kho bị trả lời bằng đoạn của nơi khác.
- Sàn 3 — an toàn: 0 lượt đảo / bỏ cảnh báo so với bên tắt trên các chuỗi có cảnh báo của bộ đã thấy (`data/phase_9/bo_do_b3/chuoi_da_thay.jsonl`).
- Sàn 4 — không lấy câu trả lời cũ làm nguồn: 0 lượt bị rút lại vì trích mã nguồn không thuộc lượt này; người thứ hai đọc tay mọi lượt đích: 0 nhận định chỉ có trong câu trả lời trước mà nguồn của lượt này không nói.
- Quyết — bộ đích MỚI do phiên khác soạn, ≥ 12 chuỗi đúng ba kiểu đã thấy trong sổ vết (trỏ theo thứ tự · tính tiếp trên con số vừa nêu · "ý thứ hai bạn vừa nói"): bên bật trả lời đúng nơi / đúng ý ≥ 9 / 12 VÀ hơn bên tắt ≥ 4 chuỗi.
- Một lượt thật qua trình duyệt (hỏi xin vài quán ⇒ "quán thứ hai ở đường nào"). Một sàn không đạt ⇒ cờ giữ tắt, báo phiên điều phối kèm số — không sửa vòng hai để đẹp số.

**5. Giới hạn biết trước:** chỉ lượt liền trước — "quán thứ hai" của ba lượt trước không hiểu được · câu trả lời dài hơn 1.200 ký tự bị cắt đuôi (mục cuối danh sách có thể mất) · mỗi lượt hỏi tiếp thêm khoảng 300–400 token đầu vào ·
số 3 / 122 đếm trên kịch bản của nhóm, không phải người dùng thật.
