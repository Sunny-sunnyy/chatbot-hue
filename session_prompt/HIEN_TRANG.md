# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 14:05 20/11/2026 (giờ `date`; chiều 20/11, sau bản sửa "báo đã dời" + cả bộ test trên bản mới). Người giữ: phiên điều phối.

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
- **Cờ:** **29 BẬT** (28 cờ ở mục `assistant:` của `backend/config/settings.yaml` + `anh.bat` = hỏi bằng ảnh). Giới hạn từng cờ: runbook 10.1, 10.2.
  **TẮT (đủ 4 cờ còn lại):** `lich_trinh` (lịch từ câu gõ tự do — không đạt), `today_line` (vô ích), `nho_cau_tra_loi` (từng mượn nhầm đoạn của nơi khác), `so_vet` (bật bằng biến `HUE_SO_VET=true` lúc mở server, chỉ ở máy local).
- **Mỗi cờ làm gì, bằng lời thường, kèm số đo:** bảng "Cái gì ĐANG chạy" của `bai_hoc/BAN_DO_DU_AN.md`.
- **Lần chạy cả bộ test gần nhất:** 20/11 chiều trên main `e13709a9` (29 cờ, từng file, 55 file, Python 3.13): 1.555 đạt, 0 hỏng. `frontend/dist` cây chính dựng lại 20/11 (nút in chỉ còn ở trang Lên kế hoạch).
- **Bẫy RAM (19/11):** không gom nhiều file test dựng cả app vào một tiến trình pytest; chạy từng file ở cây chính, không cùng lúc với server.
- **Máy:** mở lại máy ⇒ `/tmp` MẤT, Qdrant TẮT: `docker compose up -d qdrant`, kiểm 9.436 điểm (runbook mục 1).
- **Giới hạn đã biết:** `guides/RUNBOOK_BAN_GIAO.md` mục 10 — gặp hành vi trông như lỗi thì tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và hướng (việc đang mở KHÔNG ghi ở đây)

Thứ tự việc, KHÔNG gắn ngày — bước trước đạt và máy rảnh thì làm bước sau:

| Bước | Việc | Trạng thái |
|---|---|---|
| 1–4 | Cả bộ test · soát tích hợp · code đứng yên · lượt đo cuối phần đã thấy (18/11) · sửa câu thiếu cảnh báo bằng code (19/11) | XONG; bộ kín NOT RUN |
| 5 | **Đợt hoàn thiện local — việc PHỔ THÔNG**: bốn việc của danh sách đóng đã bật; bộ 80 kịch bản 51 ⇒ 58; 20/11: soát khác hãng ba lượt ⇒ 12 bản sửa nhỏ đã gộp, còn lại ghi giới hạn (runbook mục 10); test trình duyệt + cả bộ test đạt | XONG phần nhóm (20/11); chiều 20/11 thêm bản sửa "báo đã dời khi lịch không đổi" (User chọn); code ĐỨNG YÊN ở `e13709a9` — chỉ sửa lỗi buổi test tìm ra |
| 6 | **User test TOÀN BỘ một lần, trên máy LOCAL, khi nhóm đã làm xong hết** (`data/test_cuoi/DANH_SACH.md`) — nhóm KHÔNG chờ buổi này để làm bước kế | chưa |
| 7 | Deploy AWS, SAU buổi test local (cần User một lần: tài khoản, khoá, ngân sách); xong thì User thử khói ~10 phút trên máy chủ | chưa |

**Việc đang mở, ai làm, bước kế:** CHỈ ở `session_prompt/VIEC_DANG_MO.md` (xong: `session_prompt/VIEC_DA_XONG.md`). Mốc "Phase 9 xong phần nhóm" = code `55d01a8`.

Số nhiễu (19/11): hai lượt bộ câu mẫu không đổi gì lệch 1 "Đúng" · 2 "Đủ ý" · 7 "Trọng tâm" ⇒ thử đổi lời dặn phải có bên tắt CÙNG BUỔI.
Hai con số đo cách làm: `SO_CAI_TIEN_CACH_LAM.md`. Hỏi User > 8 hộp / ngày ⇒ gom.

## 3. Đang chờ User (chỉ các việc ghi ở đây; việc đã chốt thì đừng hỏi lại)

1. User tự làm: trần chi tiêu từng khoá API · vô hiệu hoá khoá AWS cũ ở thư mục khoá học.
2. Buổi User tự tay test toàn bộ (bước 6) — User chưa có giờ; KHÔNG nhắc.
3. Ba câu gác 20/11 ĐÃ trả lời (đừng hỏi lại): bản sửa "báo đã dời" — đã gộp · bộ bài đánh giá coding agent — User TỰ đưa khung cho AI khác hãng soạn, nhóm không soạn / kiểm đề · cảnh báo câu bộ đo — KHÔNG thêm. Không gấp: ~20 câu User tự gõ (`data/kich_ban_pho_thong_2026-11-19/CAU_CUA_USER.md`).
4. Chưa hỏi, không tự mở: giá phòng, bổ sung kho (số điện thoại, chỗ đậu xe…), vị trí người dùng.

## 4. Quyết định còn hiệu lực — không hỏi lại, không trình lại như lỗi

Sản phẩm:
- Trả lời chỉ từ kho, có nguồn; câu ngoài kho phải bị từ chối (sàn: 0 câu ngoài kho được trả lời bằng kho). Người dùng gõ tiếng Việt CÓ DẤU; không làm tiếng Anh.
- Câu khẩn cấp (bị cướp, mất ví, mất giấy tờ, số khẩn cấp) là NGOÀI PHẠM VI — User chốt ba lần; không sửa, không báo lại.
- **19/11 — hướng:** chất lượng trước, tiền / tốc độ sau · việc PHỔ THÔNG mà 100 người dùng thật sẽ thử; KHÔNG mở thêm việc bão / lũ / khẩn cấp · trước khi thêm file, cờ, test, bước kiểm: "lỗi đã thấy thật chưa · ai dùng · không làm thì mất gì".
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
- User không vắng trừ khi tự nói "đi vắng" (User 15/11). Không bao giờ gọi `agy` từ agent. Repo PUBLIC: `data/`, kho, câu của bộ đo không vào file được git theo dõi.
- Thứ ngoài git (`data/`, kho, chỉ mục) chống mất: `Session_Prompt.md` §5 (20/11: không xoá, không ghi đè kết quả, hai bản chép ổ D, gói cho User chép ra USB). KHÔNG ghi lên ổ C. Câu kín chỉ còn luật chữ giữ.
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
Giới hạn ≤ 150 dòng và ≤ 14.000 byte (`wc -lc`). Phép thử: agent ngữ cảnh mới chỉ đọc `AGENTS.md` + trang này trả lời tám câu ở `guides/khung/HIEN_TRANG.mau.md`.
