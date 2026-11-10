# Báo cáo hệ thống hue_rag — bắt đầu ở đây

Cập nhật 10/11/2026 (bản mẫu sắp xếp lại; các bản cũ xem trong lịch sử phiên bản — git). Thư mục này viết cho người **không đọc code**. Báo cáo kỹ thuật
của các agent nằm ở `report_agent/` — mỗi file ở đây có mục "Đọc chi tiết" trỏ sang đó. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## Chatbot này là gì

Trợ lý du lịch – văn hoá Huế trên một trang web (gọi là "chatbot" hay "trợ lý" đều là một hệ thống). Người dùng hỏi bằng tiếng Việt có dấu; chatbot
**trả lời từ kho bài viết đã biên soạn** (204 bài về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch) và ghi nguồn dưới mỗi câu trả lời. Ngoài kho
chỉ có ba thứ: ngày tháng và dự báo thời tiết (code tính / lấy), và mục "Từ web (chưa kiểm)" tách riêng khi kho không có. Kho không có ⇒ nói "không đủ thông
tin" chứ không bịa; câu ngoài chủ đề Huế ⇒ từ chối bằng một câu cố định.

**Làm được (đang chạy):**
- Hỏi đáp về Huế; nhớ 3 câu hỏi gần nhất trong một cuộc trò chuyện (chỉ câu hỏi, không nhớ câu trả lời); chữ hiện dần; dòng "Nguồn" bấm được để đọc đoạn gốc / cả bài.
- Trò chuyện xã giao (chào, cảm ơn, hỏi chatbot là ai).
- Câu hỏi có ngày (hôm nay, cuối tuần, rằm, Tết, ngày âm của lễ hội): **ngày do code tính**, model chỉ diễn đạt. Câu chỉ hỏi về ngày tháng (âm ↔ dương, thứ mấy,
  lễ / Tết ngày nào) được trả lời cả khi không nhắc Huế; câu hỏi việc khác vào ngày đó mà không về Huế (giá vàng, thời tiết nơi khác…) vẫn từ chối.
- Dự báo thời tiết Huế 7 ngày (số lấy từ Open-Meteo, code dựng câu).
- Kho không có ⇒ tra web một lần, hiện riêng mục "Từ web (chưa kiểm)".
- Biểu mẫu "Lên kế hoạch": chọn số ngày / người đi cùng / sở thích ⇒ code xếp lịch theo buổi từ địa điểm trong kho, model viết lời.
- Hỏi bằng ảnh: chụp ảnh ⇒ chatbot gợi ≤ 3 tên điểm / món ⇒ người dùng bấm xác nhận mới trả lời.
- Cổng du lịch: trang chủ, "Khám phá" đọc thẳng 204 bài, nút 👍 / 👎 dưới câu trả lời.

**Chưa làm được / chưa bật:** lịch trình từ câu gõ tự do (chỉ qua biểu mẫu) · bản đồ vẽ cả lịch trình (có code, chờ bạn duyệt toạ độ) · giọng nói (chờ 40 câu
thu âm) · câu gõ không dấu (ngoài phạm vi — bạn quyết 25/10) · lưu trú, quán gần đây, sự kiện theo ngày · hiểu câu nhắc tới câu trả lời trước ("quán đó") ·
chưa đưa lên mạng (đã chạy thử bản đóng gói Docker trên máy; đưa lên máy chủ AWS chờ bạn quyết + tài khoản).

**Bước cuối Phase 9:** đo lại cả hệ thống hiện tại so với bản cuối Phase 8 trên cùng các bộ câu (kế hoạch đang nháp).

## Số chính (mỗi số chỉ ghi ở đây — file khác trỏ về)

**Yêu cầu bạn chốt (28/10):** chữ đầu tiên hiện trên trình duyệt sau ≤ 3 s ở câu giữa (trung vị), ≤ 5 s ở 95 % câu; tiền ≤ 0,0005 USD / câu. **Thứ tự lỗi
nặng → nhẹ:** sai cảnh báo an toàn > nói chắc sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.

| Đo gì | Kết quả | Đo lúc nào, trên gì |
|---|---|---|
| Kho | 204 bài → 8.435 đoạn | chỉ mục dựng lại 05/11 |
| Điểm chất lượng (thang 1–5) | Đúng **4,71** · Đủ ý **4,58** · Trúng ý **4,72** | **bản cuối Phase 8** (01/11), 129 câu Golden có đáp án trong kho (đã bỏ 29 câu ít giống cách người thật hỏi) |
| … loại câu yếu nhất | câu cần ghép nhiều nguồn: Đủ ý **3,50** (Phase 9 thêm "tìm thêm" để sửa — chưa đo lại trên cả bộ) | như trên |
| Từ chối nhầm (kho có đáp án mà nói "không đủ thông tin") | **4–6 / 158** câu (mỗi lần chạy lại ra 4–6 vì model viết hơi khác mỗi lần); trước khi có "tìm thêm": 12 / 158 | 158 câu Golden có đáp án trong kho, 03/11 |
| Câu ngoài kho mà phần trả lời từ kho vẫn trả lời | **0** trên mọi bộ đã đo | 18 câu Golden ngoài kho + bộ an toàn (mục web ghi riêng, không tính ở đây) |
| An toàn (vé, giờ, quy định, cảnh báo) | 0 câu đảo cảnh báo; 2 câu nói sai điều kiện kiểu mới (vd ghi sai giờ) — đúng ngưỡng cho phép ≤ 2, bản trước sinh lại cũng sai y vậy | bộ 32 câu an toàn, lượt đo cuối Phase 8 (01/11); mỗi phần mới của Phase 9 đều đo lại bộ này trước khi bật |
| Tốc độ tới **chữ đầu tiên** (trung vị / 95 % câu) | câu về Huế **2,16 / 4,32 s** ✓ · câu có ngày **2,35 / 4,56 s** ✓ · ngoài phạm vi 1,62 / 2,97 s ✓ · **xã giao 3,46 / 7,73 s ✗** | trình duyệt thật, chạy một lần trên 65 câu (09/11); câu có ngày: 19 câu (10/11). Thời gian tới lúc xong cả câu chưa đo chung |
| Tiền một câu (theo bảng giá OpenAI, gồm cả phí lưu tạm) | câu về Huế **0,00047 USD** (~12 đồng, sát trần) · câu có ngày 0,00036 USD | cùng lượt trên |
| Hỏi bằng ảnh | tên đúng nằm trong 3 gợi ý ở **22 / 25** ảnh; đoán mất ~3 s (chậm nhất 6–9 s ✗) | 05/11 |

**Bản cuối Phase 8 khác bản đang chạy ở đâu:** Phase 8 chỉ có "tìm 10 đoạn → model trả lời". Bản đang chạy thêm bước phân loại câu, tìm thêm, nhớ câu hỏi, tra web,
thời tiết, ngày, biểu mẫu, ảnh. Mỗi phần mới được đo riêng trên bộ câu của nó trước khi bật; cả hệ mới sẽ đo lại trên bộ 176 câu ở bước cuối Phase 9.

## Từ hay gặp

| Từ | Nghĩa |
|---|---|
| kho | 204 bài Markdown đã biên soạn — nguồn sự thật của câu trả lời |
| đoạn | một mẩu của bài (một đoạn văn, một mục danh sách, một dòng bảng) — đơn vị để tìm và trích nguồn |
| vector nghĩa | dãy 384 con số đại diện cho *ý nghĩa* một đoạn; hai đoạn cùng ý thì gần nhau (tính bằng model nhỏ e5-small, chạy ngay trên máy) |
| BM25 | cách chấm theo **từ trùng** giữa câu hỏi và đoạn |
| RRF | cách gộp hai bảng xếp hạng (theo nghĩa, theo từ): đoạn đứng cao ở cả hai thì lên đầu |
| chỉ mục | các đoạn + vector nghĩa + bảng từ khoá, dựng ra từ kho và cất trong Qdrant — thứ chatbot thật sự tìm trong đó; kho đổi thì phải dựng lại |
| Qdrant | cơ sở dữ liệu cất chỉ mục để tìm nhanh (một "collection" = một chỉ mục trong Qdrant) |
| ngữ cảnh | 10 đoạn tìm được, gửi cho model cùng câu hỏi |
| model | `gpt-6-luna` của OpenAI — đọc ngữ cảnh rồi viết câu trả lời |
| token | đơn vị chữ mà model đếm (một từ tiếng Việt ≈ 1–2 token); tiền tính theo token |
| lời dặn | hướng dẫn cố định gửi kèm mọi câu cho model (cách trả lời, khi nào từ chối) |
| phân loại câu hỏi | một lần gọi model ngắn xếp câu vào 4 loại: xã giao / về Huế / ngoài phạm vi / khẩn cấp. Khẩn cấp được trả lời như câu về Huế, chỉ đánh dấu riêng trong log để theo dõi |
| công cụ | việc code làm khi model yêu cầu: tìm thêm trong kho, đổi ngày, lấy dự báo |
| Golden | bộ 176 câu hỏi chuẩn có đáp án mẫu, dùng để chấm |
| chấm mù | một model khác (Claude) chấm từng câu trả lời so với đáp án mẫu, **không biết** câu đó của bản nào. Đúng = không sai so với đáp án; Đủ ý = có đủ các ý của đáp án; Trúng ý = trả lời thẳng điều được hỏi, không lan man |
| bộ kín | bộ câu người sửa code không được xem, chỉ mở một lần để kiểm cuối |
| sàn | mức tối thiểu ghi **trước** khi đo; không đạt ⇒ không đưa vào chatbot |
| cờ | công tắc bật / tắt một tính năng trong cấu hình |
| trung vị / p95 | trung vị = câu ở giữa; p95 = 95 % câu nhanh hơn số này |
| Docker, AWS | Docker = đóng gói chatbot thành một khối chạy được trên máy khác; AWS = dịch vụ thuê máy chủ của Amazon |
| Phase | giai đoạn của đồ án: 0–8 dựng chatbot hỏi đáp từ kho và chọn cách làm tốt nhất; 9 trợ lý có công cụ; 10–12 ảnh, giọng nói, bản đồ, đưa lên mạng |

## Thứ tự đọc (theo dòng chảy dữ liệu)

| Số | File | Đọc để biết |
|---:|---|---|
| 01 | [01_LUONG_HOAT_DONG_HE_THONG.md](01_LUONG_HOAT_DONG_HE_THONG.md) | Một câu hỏi đi qua những bước nào; một ví dụ trọn vẹn; dữ liệu người dùng gửi đi đâu |
| 02 | [02_BAO_CAO_KHO_DU_LIEU.md](02_BAO_CAO_KHO_DU_LIEU.md) | Kho lấy từ đâu, đã sửa gì, còn thiếu gì |
| 03 | [03_BAO_CAO_CHIA_DOAN.md](03_BAO_CAO_CHIA_DOAN.md) | Bài được cắt thành đoạn thế nào, vì sao cắt vậy |
| 04 | [04_BAO_CAO_EMBEDDING_TU_KHOA.md](04_BAO_CAO_EMBEDDING_TU_KHOA.md) | Đoạn biến thành vector nghĩa + từ khoá ra sao, vì sao chọn model nhỏ |
| 05 | [05_BAO_CAO_LUU_TRU_QDRANT.md](05_BAO_CAO_LUU_TRU_QDRANT.md) | Cất ở đâu, khi nào phải dựng lại |
| 06 | [06_BAO_CAO_TIM_KIEM.md](06_BAO_CAO_TIM_KIEM.md) | Chọn 10 đoạn nào cho một câu hỏi, vì sao hay từ chối nhầm |
| 07 | [07_BAO_CAO_SINH_CAU_TRA_LOI_API.md](07_BAO_CAO_SINH_CAU_TRA_LOI_API.md) | Trợ lý viết câu trả lời: phân loại, công cụ, kiểm nguồn, giao diện |
| 08 | [08_BAO_CAO_HOI_BANG_ANH.md](08_BAO_CAO_HOI_BANG_ANH.md) | Hỏi bằng ảnh làm gì, đúng tới đâu |
| 09 | [09_BAO_CAO_BO_CAU_HOI_GOLDEN.md](09_BAO_CAO_BO_CAU_HOI_GOLDEN.md) | Bộ câu chuẩn dùng để đo gồm gì, soạn thế nào |
| 10 | [10_BAO_CAO_DANH_GIA.md](10_BAO_CAO_DANH_GIA.md) | Chấm thế nào, tốt tới đâu, yếu ở đâu |

**Hồ sơ tra (ngoài đường đọc):** [91_BAO_CAO_SO_SANH_PHUONG_AN.md](91_BAO_CAO_SO_SANH_PHUONG_AN.md) (mọi cách đã thử / chọn / bỏ) ·
[90_BAO_CAO_NEN_TANG.md](90_BAO_CAO_NEN_TANG.md) (dự án dựng trên gì) · [92_BAO_CAO_NGHIEN_CUU_PHASE_9.md](92_BAO_CAO_NGHIEN_CUU_PHASE_9.md) +
[93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md](93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md) (vì sao làm Phase 9 – 12) · [94_DE_XUAT_SUA_CODE.md](94_DE_XUAT_SUA_CODE.md)
(đợt dọn code 25–26/10) · [nhat_ky/](nhat_ky/) (chuyện từng ngày).

## Luật cập nhật (cho agent — bạn bỏ qua mục này)

- Thay đổi vào hệ thống đang chạy ⇒ sửa đúng file khâu bị chạm + 1 dòng nhật ký ngày đó; LUONG chỉ khi đường đi của câu hỏi đổi; số chung ⇒ **chỉ** bảng
  "Số chính" ở trên (file khác trỏ về, không chép số). Quy tắc đủ: `session_prompt/WORKFLOW.md` §6.
- Thân bài lời thường: không mã việc, mã commit, tên hàm, file:dòng — gom vào mục "Đọc chi tiết" cuối file. Phương án đã bỏ: 1 dòng + trỏ `91_BAO_CAO_SO_SANH_PHUONG_AN.md`.
- Phần "đang chạy" của file khâu ≤ ~40 dòng; LUONG ≤ ~120 dòng. Không dòng "Trước: …", không khối "Mới ngày …" (git + nhật ký giữ lịch sử). Giờ lấy bằng `date`.
