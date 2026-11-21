# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 16:42 20/11/2026 (giờ `date`; KẾT PHIÊN CHIỀU 20/11). Người giữ: phiên điều phối.

**Trang này là gì.** Ảnh chụp "bây giờ" của dự án cho BẤT KỲ coding agent nào vừa mở phiên; **viết lại tại chỗ** mỗi lần kết phiên, không nối thêm. Thứ tự mở
phiên ở `session_prompt/START_SESSION.md`; sổ việc dài chỉ mở khi cần. `AGENTS.md`, code và file cấu hình thắng trang này — thấy lệch thì báo để sửa trang.

Từ dùng: **phiên** = một cửa sổ agent · **phiên điều phối (A)** = phiên nói chuyện với User và giao việc; **B, C, E** = phiên làm việc; **D** = phiên giảng (tuỳ chọn).
Làm MỘT MÌNH ⇒ "báo phiên điều phối" = hỏi User (`guides/KHI_CHI_CO_MOT_AGENT.md`) · **User** = chủ dự án (đọc `bai_hoc/`, không đọc code) · **kho** = bộ bài
Markdown riêng tư trợ lý được phép trả lời từ đó · **cờ** = một dòng bật / tắt trong `backend/config/settings.yaml` · **bộ câu mẫu** ("Golden") = 176 câu hỏi kèm
đáp án, riêng tư · **câu kín** (`*sealed*`) = bộ câu agent không được mở · **sổ vết** = bản ghi debug từng lượt · **lượt đo cuối** = lần chấm toàn bộ trên bản code đứng yên.

## 1. Hệ thống đang chạy

- **Là gì:** trợ lý hỏi đáp du lịch – văn hoá Huế cho du khách và người dân (đồ án tốt nghiệp của User), trả lời CHỈ từ kho, có ghi nguồn; kho không có thì từ chối, rồi tra web một lần ở mục riêng "chưa kiểm".
  Web: FastAPI (`backend/`) + giao diện React dựng sẵn (`frontend/`). Chạy trên máy User; **chưa deploy**.
- **Số hôm nay** (lệnh kiểm: runbook mục 0): kho **265 bài ⇒ 9.436 đoạn**, collection Qdrant `hue_full_corpus_7a2_e5_small_384` (cổng 6335);
  tìm = vector `e5-small` + từ khoá BM25 trộn RRF, **10 đoạn** vào ngữ cảnh, không xếp lại; model viết `gpt-6-luna` (OpenAI), từ 19/11 không còn trần token đầu ra và ngân sách ngữ cảnh mỗi lượt; tra web qua Serper.
- **Cờ:** **31 BẬT** (30 cờ ở mục `assistant:` của `backend/config/settings.yaml` + `anh.bat` = hỏi bằng ảnh); đã gộp nhưng còn TẮT, chờ bước cuối (xem `VIEC_DANG_MO.md` khối 0): `su_kien_theo_ngay`, `len_lich_dan_trang`; hai cờ mới bật chiều 20/11: `cache_cau_tra_loi` (câu lặp ở cuộc trò chuyện khác trả từ bộ nhớ, 24 giờ, trong RAM) và `danh_sach_noi_that` (câu xin danh sách có dòng "có thể chưa đủ"). Giới hạn từng cờ: runbook 10.1, 10.2.
  **TẮT (đủ 4 cờ còn lại):** `lich_trinh` (lịch từ câu gõ tự do — không đạt), `today_line` (vô ích), `nho_cau_tra_loi` (từng mượn nhầm đoạn của nơi khác), `so_vet` (bật bằng biến `HUE_SO_VET=true` lúc mở server, chỉ ở máy local).
- **Mỗi cờ làm gì, bằng lời thường, kèm số đo:** bảng "Cái gì ĐANG chạy" của `bai_hoc/BAN_DO_DU_AN.md`.
- **Lần chạy cả bộ test gần nhất:** 20/11 chiều trên main `e13709a9` (29 cờ, từng file, 55 file, Python 3.13): 1.555 đạt, 0 hỏng — các bản gộp SAU đó (dời điểm, cache, dòng danh sách, trang Bản đồ; 31 cờ) mới chạy file test chạm đường đổi + lượt thật qua giao diện, CHƯA chạy cả bộ (để dành một lượt cuối đợt). `frontend/dist` cây chính dựng lại 16:17 20/11 trên `58bad83e` (có trang Bản đồ; nút in chỉ còn ở trang Lên kế hoạch).
- **Bẫy RAM (19/11):** không gom nhiều file test dựng cả app vào một tiến trình pytest; chạy từng file ở cây chính, không cùng lúc với server.
- **Máy:** mở lại máy ⇒ `/tmp` MẤT, Qdrant TẮT: `docker compose up -d qdrant`, kiểm 9.436 điểm (runbook mục 1).
- **Giới hạn đã biết:** `guides/RUNBOOK_BAN_GIAO.md` mục 10 — gặp hành vi trông như lỗi thì tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và hướng (việc đang mở KHÔNG ghi ở đây)

Thứ tự việc, KHÔNG gắn ngày — bước trước đạt và máy rảnh thì làm bước sau:

| Bước | Việc | Trạng thái |
|---|---|---|
| 1–4 | Cả bộ test · soát tích hợp · code đứng yên · lượt đo cuối phần đã thấy (18/11) · sửa câu thiếu cảnh báo bằng code (19/11) | XONG; bộ kín NOT RUN |
| 5 | **Đợt hoàn thiện local** — phần "bốn việc" + soát khác hãng xong sáng 20/11; chiều 20/11 User nói rõ phạm vi rộng hơn (mục 4) ⇒ **ĐỢT HOÀN THIỆN PHASE 9–12 đang chạy**: đã xong + đang chạy 5 mục (dời điểm có lý do + gợi ý · cache câu trả lời · dòng "danh sách có thể chưa đủ" · trang Bản đồ · ứng xử coi là đã có); đã gộp cờ TẮT chờ bước cuối 2 mục (sự kiện theo ngày · dòng dẫn sang trang Lên kế hoạch); code xong chưa gộp 3 mục (đổi chỗ hai ngày · nhớ câu trả lời liền trước · trang theo dõi); chưa bắt đầu 3 mục (hỏi lại khi thiếu thông tin · "gần X có gì ăn" · agent đề xuất sửa kho) | ĐANG LÀM — bảng từng mục + bước kế: `VIEC_DANG_MO.md` khối 0. Bản code gần nhất đã chạy CẢ bộ test: `e13709a9`; mọi thứ gộp sau đó mới qua file test chạm đường đổi + lượt thật |
| 6 | **User test TOÀN BỘ một lần, trên máy LOCAL** (`data/test_cuoi/DANH_SACH.md` — CHƯA có dòng cho các việc chiều 20/11; thêm khi đợt xong) — HOÃN tới khi bước 5 xong hết | chưa |
| 7 | Deploy AWS, SAU buổi test local (cần User một lần: tài khoản, khoá, ngân sách); xong thì User thử khói ~10 phút trên máy chủ | chưa |

**Việc đang mở, ai làm, bước kế:** CHỈ ở `session_prompt/VIEC_DANG_MO.md` (xong: `session_prompt/VIEC_DA_XONG.md`). Mốc "Phase 9 xong phần nhóm" = code `55d01a8`.

Số nhiễu (19/11): hai lượt bộ câu mẫu không đổi gì lệch 1 "Đúng" · 2 "Đủ ý" · 7 "Trọng tâm" ⇒ thử đổi lời dặn phải có bên tắt CÙNG BUỔI.
Hai con số đo cách làm: `SO_CAI_TIEN_CACH_LAM.md`. Hỏi User > 8 hộp / ngày ⇒ gom.

## 3. Đang chờ User (chỉ các việc ghi ở đây; việc đã chốt thì đừng hỏi lại)

1. User tự làm: trần chi tiêu từng khoá API · vô hiệu hoá khoá AWS cũ ở thư mục khoá học.
2. Buổi User tự tay test toàn bộ (bước 6) — User chưa có giờ; KHÔNG nhắc.
3. Đã trả lời trong ngày 20/11 (đừng hỏi lại): bản sửa "báo đã dời" — đã gộp · bộ bài đánh giá coding agent — User TỰ đưa `data/danh_gia_model_2026-11-20/KHUNG.md` + `KHUON_MO_DAU.md` cho AI khác hãng soạn đề (đó là file ĐỂ SOẠN ĐỀ, không phải đề; nhóm không soạn / không kiểm đề; A đã đưa đường dẫn + câu dán) · cảnh báo câu bộ đo — KHÔNG thêm · sao lưu — KHÔNG sao lưu định kỳ, kho + bộ câu mẫu ở git, KHÔNG ghi ổ C · phạm vi + tám điều cách làm (mục 4). Chờ User xác nhận, không gấp: dòng "© OpenStreetMap" trên hai bản đồ (xem `VIEC_DANG_MO.md` khối 0); giọng nói "dẹp" hay "không làm trước 30/11" (đang coi là bỏ). Không gấp: ~20 câu User tự gõ (`data/kich_ban_pho_thong_2026-11-19/CAU_CUA_USER.md`).
4. Chưa hỏi, không tự mở: giá phòng, bổ sung kho (số điện thoại, chỗ đậu xe…), vị trí người dùng.

## 4. Quyết định còn hiệu lực — không hỏi lại, không trình lại như lỗi

Sản phẩm:
- Trả lời chỉ từ kho, có nguồn; câu ngoài kho phải bị từ chối (sàn: 0 câu ngoài kho được trả lời bằng kho). Người dùng gõ tiếng Việt CÓ DẤU; không làm tiếng Anh.
- Câu khẩn cấp (bị cướp, mất ví, mất giấy tờ, số khẩn cấp) là NGOÀI PHẠM VI — User chốt ba lần; không sửa, không báo lại.
- **19/11 — hướng:** chất lượng trước, tiền / tốc độ sau · việc PHỔ THÔNG mà 100 người dùng thật sẽ thử; KHÔNG mở thêm việc bão / lũ / khẩn cấp · trước khi thêm file, cờ, test, bước kiểm: "lỗi đã thấy thật chưa · ai dùng · không làm thì mất gì".
- **15:13 20/11/2026 — PHẠM VI "XONG Ở LOCAL" (User nói rõ, nhóm đã hiểu hẹp):** "không thêm tính năng mới" = không thêm gì NGOÀI những tính năng đã chốt ở Phase 9–12 và trước đó; những tính năng đã chốt đó PHẢI XONG HẾT trước buổi test — không phải chỉ Phase 9 / "bốn việc". Local CHƯA xong. User chọn: làm 13 mục chưa xong + bốn mục phổ thông; bốn mục đã đo âm giữ giới hạn — danh sách + thứ tự: `VIEC_DANG_MO.md` khối 0; bảng kiểm kê: `data/kiem_ke_phase_2026-11-20/`; chia Phase gốc: `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md`.
- **09:41 21/11/2026 — ĐỔI TẠM MODEL VIẾT (User nói rõ):** cả sản phẩm (chín loại lời gọi) đổi TẠM từ `gpt-6-luna` (OpenAI) sang Claude Sonnet 5.5 chạy trên Amazon Bedrock; người chấm điểm lúc đo VẪN là luna; giữ nguyên framework OpenAI Agents SDK; không cần stream thật; tiền Bedrock không phải mối lo (vẫn ghi số thật); không xây cơ chế lo khoá Bedrock hết hạn. ĐƯỜNG VỀ LUNA PHẢI LUÔN CÒN: đường gọi OpenAI + lời dặn bản luna không bị sửa đè, công tắc là MỘT dòng `full_corpus_generation.provider` trong `backend/config/settings.yaml`; User nói "chuyển về luna" ⇒ phiên điều phối đổi dòng đó về `openai`, chạy file test chạm + một lượt thật, không hỏi lại. Dòng "giữ model `gpt-6-luna`" ở dưới tạm đứng sau quyết định này. Vì sao phải có lớp dịch (cổng kiểu OpenAI của Bedrock không phục vụ Sonnet 5.5), số đo lượt thử và trạng thái: `VIEC_DANG_MO.md` khối 0a; trang hướng dẫn đổi qua / đổi về viết khi việc xong.
- **15:56 20/11/2026 — CÁCH LÀM (User chọn hai lượt, tám điều; chữ đủ của bốn điều đầu ở `Session_Prompt.md` §7 gạch đầu dòng đầu):** (1) test vừa đủ, cả bộ test chỉ ở mốc · (2) lỗi hiếm ghi giới hạn, không sửa, không hỏi (trừ an toàn); đề xuất sửa phải kèm số lượt thật gặp · (3) báo "xong" bằng bảng người dùng làm được / chưa làm được; phiên nào thấy việc được giao không đáng thì nói một dòng TRƯỚC khi làm, kể cả với điều phối · (4) tài liệu một bản một người đọc, độ dài linh hoạt, ưu tiên ghi ĐỦ trạng thái · (5) **bớt sổ**: sổ việc, trang này, trang việc đang mở — điều phối ghi THẲNG lên main, không nhánh, không người đọc (`bai_hoc/` và luật vẫn cần người đọc); trang này KHÔNG còn trần byte; mỗi việc xong chỉ viết một mục `bai_hoc/` + một dòng giới hạn (nếu có) + một dòng sổ việc, báo cáo kỹ thuật riêng chỉ khi có số đo; `bao_cao_he_thong/` ngừng cập nhật (giữ làm hồ sơ cũ). User dặn kèm: việc bớt sổ KHÔNG được làm giảm chất lượng, trạng thái, ngữ cảnh của các phiên ⇒ thứ phiên mở lại cần để làm việc vẫn phải có ở trang này + `VIEC_DANG_MO.md` + `STATUS_<X>.md` · (6) **bớt nhiễu cho User**: không chuyển tiếp thông báo tự động "không có gì mới"; chỉ báo khi một việc gộp xong, một việc đo không đạt, hoặc cần User; quyết định nhỏ điều phối tự chọn mặc định và ghi lại; hộp hỏi chỉ cho tiền, xoá dữ liệu, sửa kho, đổi hướng sản phẩm · (7) **bỏ nghi thức không ai dùng**: bỏ số đếm lúc mở phiên ("lần đọc ngắn thứ mấy, mấy tin rải"); vòng tự soi MỘT lần / ngày (thêm khi User nhắc); bộ quét trùng của hook chỉ cần chặn câu kín (CHƯA sửa hook — làm cùng điều 8) · (8) **gọt bộ luật SAU khi đợt Phase 9–12 xong** (không làm bây giờ): hai file luật còn khoảng một nửa, giữ bảy luật cứng, một phiên khác đọc.
- **19/11 — THỨ TỰ ĐÓNG (User nói rõ):** xong HẾT ở local ⇒ User test MỘT lần ở local ⇒ KHÔNG phát triển gì nữa (chỉ sửa lỗi buổi test tìm ra) ⇒ rồi mới deploy. Thứ gì muốn có trong sản phẩm phải vào danh sách TRƯỚC buổi test. KHÔNG thêm tính năng mới.
- **19/11 — danh sách đóng = BỐN việc, đều đã bật:** lịch đã lưu vào lượt hỏi thường · nói thật giới hạn (không gửi email, không giả lập đặt phòng) · xuất lịch (kiểu "Di sản" của nhóm) · nhớ tên nơi vừa trích (20/11: câu đúng khuôn "kể lại các nơi vừa nêu" và câu gõ lại nguyên văn không còn nhận dòng tên nơi — giới hạn còn lại ở runbook 10.1; User chọn "đọc sàn bộ bẫy theo mục đích").
- **19/11 — GHI GIỚI HẠN, không làm trước khi đóng, không mở lại khi User chưa nêu:** "gần X" · ngày của nguồn giá vé · ngân sách / tổng tiền vé do code tính · câu "những quán nào có đặc điểm X" trả thiếu mục · "kho có một phần thì từ chối cả câu" · gõ "lên lịch giúp mình" trong ô chat · 15 đoạn / cả mục / cả bài · đổi mức suy luận.
- **20/11 — soát khác hãng:** mọi điểm chưa sửa GHI GIỚI HẠN; KHÔNG soát vòng nữa, không vá thêm khâu đoán ý từ câu gõ. Nút in chỉ còn ở trang Lên kế hoạch. Đề xuất trình User = ý đa số / cả nhóm, ghi rõ ai không có ý kiến.
- **19/11 — khác:** sàn "thiếu cảnh báo mới": ngữ cảnh chung tính sàn, phần riêng người đọc tay xét · agent được gọi PowerPoint của Windows dựng slide thử (một file một lần, PowerPoint đang mở thì không gọi) · trước deploy phải giới hạn số lượt tải file xuất.
- Không nói giá phòng ở phần gợi ý chỗ ở (câu hỏi chi phí chung vẫn nêu khoảng giá có nguồn từ kho). Khối "Nơi ở" chỉ hiện khi người dùng
  đã chọn hạng chỗ ở — ở biểu mẫu hoặc nói bằng lời.
- Việc phải luôn đúng (phép tính, ngày, tiền, thứ tự bắt buộc) do CODE làm; model chỉ diễn đạt. Giữ model `gpt-6-luna`, giữ `e5-small`, giữ 10 đoạn.
- **Rào tối ưu sớm đã GỠ (User 19/11):** không sàn tiền / câu, sàn tốc độ, trần token đầu ra, ngân sách ngữ cảnh, trần lịch sử — tiền / giây chỉ ĐO và BÁO; một việc > 1 USD báo trước. Lỗi tệ nhất trước: sai cảnh báo an toàn > nói chắc mà sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.
- KHÔNG in chữ ghi công / tác giả / giấy phép ảnh ở đâu người dùng thấy (màn hình, bản in, file tải về), không lọc ảnh theo giấy phép — User 14/11, nhắc lại 19/11.
- Không mở lại khi User chưa nêu: giọng nói (dẹp) · so ảnh bằng embedding (hoãn, chưa có ngày; ảnh mẫu còn giữ) · nhớ sở thích người dùng (không làm) ·
  "tra web sớm" (bỏ) · "gộp câu tìm" (gác) · mục web giữ bản dài (bản gọn đã thử, không dùng).
- Đây là ĐỒ ÁN TỐT NGHIỆP, chấm một lần — tài liệu không dùng chữ "sếp" / "công ty"; gói "giảng viên hỏi vặn" làm sau khi hệ thống hoàn tất.

Cách làm:
- Chất lượng cần thiết trước, tốc độ / tiền sau. Đổi gì có đo: ghi tiêu chí TRƯỚC, đổi một thứ, so với mốc. Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật.
- Người viết không tự kiểm. Sau mỗi đợt gộp lớn soát chỗ các tính năng gặp nhau · định kỳ soát độ thật của test. Giám khảo khác hãng: ở MỐC CHỐT, qua
  một file `.md`, User chỉ gửi khi nhóm YÊU CẦU rõ; mặc định GPT sol + Gemini 4 Hydrogen (bỏ Carbon).
- Báo cáo "xong" kết bằng bảng: đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra. Báo cáo cho User: người dùng thấy gì khác · bằng chứng · giới hạn ·
  cách thử 2 phút; mỗi khẳng định gắn nhãn [máy kiểm] / [người thứ hai kiểm] / [chưa kiểm].
- Hỏi User: mỗi lần MỘT câu, có sẵn đáp án, mỗi đáp án kèm hệ quả. Tiếng Việt, lời thường, đủ quan trọng hơn ngắn. Giờ ghi vào tài liệu lấy bằng `date`.
- Lỗi cách làm lặp lần hai mới thành luật; máy kiểm được thì làm phép kiểm thay chữ. Không thêm công cụ / rào riêng tư mới (User 14/11) — giữ rào đang có.
- User không vắng trừ khi tự nói "đi vắng" (User 15/11). Không bao giờ gọi `agy` từ agent. Repo PUBLIC: `data/`, câu kín không vào git (kho + bộ câu mẫu thì được, User 20/11).
- Kho + bộ câu mẫu ở git (20/11); `data/`, chỉ mục: chỉ ở máy, không sao lưu. KHÔNG ghi ổ C. Câu kín chỉ còn luật chữ giữ.
- User chỉ đọc `bai_hoc/`: việc xong mới viết vào đó, mỗi con số kèm đo gì / so với mốc nào.

Danh sách đủ, có ngày và nguồn: `session_prompt/Project_Status.md` mục 5 (nhật ký — chỉ mở khi cần tra một quyết định cụ thể).

## 5. Bật hệ thống và kiểm

Lệnh từng bước + kết quả mong đợi: `guides/RUNBOOK_BAN_GIAO.md` mục 1 (Qdrant), 2 (giao diện + server), 3 (test). Hay vấp: lệnh Python chạy từ `backend/` bằng
`uv run …`; máy dùng chung ⇒ việc nặng (server, cả bộ test, đo) báo phiên điều phối trước, RAM khả dụng < 4 GB thì dừng; hook git: `git config core.hooksPath .githooks`.

## 6. Lệnh kiểm các con số của trang này

Ba lệnh (số bài / đoạn của kho · Qdrant khớp · số cờ bật) kèm kết quả phải ra: `guides/RUNBOOK_BAN_GIAO.md` mục 0.

## 7. Nhật ký ở đâu (KHÔNG bắt đọc lúc mở phiên — mở khi cần trả lời một câu cụ thể)

- `session_prompt/CURRENT_HANDOFF.md` — sổ việc theo giờ (khối đầu mới nhất) · `session_prompt/sessions/STATUS_<X>.md` — sổ riêng từng phiên.
- `session_prompt/Project_Status.md` — mục 4 từng tính năng + mã commit · mục 5 quyết định theo ngày · mục 8 bẫy kỹ thuật · việc đã đóng: `PROJECT_HISTORY.md`, `archive/`.
- Luật đủ: `session_prompt/Session_Prompt.md`, `WORKFLOW.md` · cách làm việc: `guides/CACH_LAM_VIEC.md`.

## 8. Cách giữ trang này

Kết phiên: người giữ VIẾT LẠI mục 1–4 cho đúng lúc đó (xoá thứ đã xong); chi tiết theo giờ để ở nhật ký. Quyết định mới của User ⇒ thêm vào mục 4 NGAY.
Không còn trần byte (User 20/11); giữ trang đủ để phiên mở lại làm việc được. Phép thử: agent ngữ cảnh mới chỉ đọc `AGENTS.md` + trang này trả lời tám câu ở `guides/khung/HIEN_TRANG.mau.md`.
