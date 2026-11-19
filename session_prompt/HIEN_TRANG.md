# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 16:32 19/11/2026 (giờ `date`; phiên điều phối viết lại mục 1, 3, 4 lúc kết phiên nhẹ chiều 19/11). Người giữ: phiên C.

**Trang này là gì.** Ảnh chụp "bây giờ" của dự án cho BẤT KỲ coding agent nào vừa mở phiên; **viết lại tại chỗ** mỗi lần kết phiên, không nối thêm. Thứ tự mở
phiên ở `session_prompt/START_SESSION.md`; sổ việc dài chỉ mở khi cần. `AGENTS.md`, code và file cấu hình thắng trang này — thấy lệch thì báo để sửa trang.

Từ dùng: **phiên** = một cửa sổ agent · **phiên điều phối (A)** = phiên nói chuyện với User và giao việc; **B, C, E** = phiên làm việc; **D** = phiên giảng (tuỳ chọn).
Làm MỘT MÌNH ⇒ "báo phiên điều phối" = hỏi User (`guides/KHI_CHI_CO_MOT_AGENT.md`) · **User** = chủ dự án (đọc `bai_hoc/`, không đọc code) · **kho** = bộ bài
Markdown riêng tư trợ lý được phép trả lời từ đó · **cờ** = một dòng bật / tắt trong `backend/config/settings.yaml` · **bộ câu mẫu** ("Golden") = 176 câu hỏi kèm
đáp án, riêng tư · **câu kín** (`*sealed*`) = bộ câu agent không được mở · **sổ vết** = bản ghi debug từng lượt · **lượt đo cuối** = lần chấm toàn bộ trên bản code đứng yên.

## 1. Hệ thống đang chạy

- **Là gì:** trợ lý hỏi đáp du lịch – văn hoá Huế cho du khách và người dân (đồ án tốt nghiệp của User; hiện chỉ User và nhóm dùng thử), trả lời CHỈ từ kho, có ghi nguồn; kho không có thì từ chối, rồi tra web một lần ở mục riêng "chưa kiểm".
  Web: FastAPI (`backend/`) + giao diện React dựng sẵn (`frontend/`). Chạy trên máy User; **chưa deploy**.
- **Số hôm nay** (lệnh kiểm: runbook mục 0): kho **265 bài ⇒ 9.436 đoạn**, một collection Qdrant `hue_full_corpus_7a2_e5_small_384` (cổng 6335);
  tìm = vector `e5-small` + từ khoá BM25 trộn RRF, **10 đoạn** vào ngữ cảnh, không xếp lại; model viết `gpt-6-luna` (OpenAI), từ 19/11 không còn trần token đầu ra và ngân sách ngữ cảnh mỗi lượt; tra web qua Serper.
- **Cờ:** **25 BẬT** (24 cờ ở mục `assistant:` của `backend/config/settings.yaml` + `anh.bat` = hỏi bằng ảnh); bật 19/11: `sua_lich_doi_cho_code`
  (code đọc câu "dời hai điểm"), `noi_dong_tam_ngung` (code nối dòng "tạm ngừng khi lũ / lệnh cấm" của nguồn đã trích vào ghi chú an toàn).
  **TẮT (đủ 4 cờ còn lại):** `lich_trinh` (lịch từ câu gõ tự do — không đạt; nay qua biểu mẫu), `today_line` (vô ích), `nho_cau_tra_loi` (từng mượn
  nhầm đoạn của nơi khác), `so_vet` (bật bằng biến `HUE_SO_VET=true` lúc mở server, chỉ ở máy local).
- **Mỗi cờ làm gì, bằng lời thường, kèm số đo:** bảng "Cái gì ĐANG chạy" của `bai_hoc/BAN_DO_DU_AN.md`.
- **Lần chạy cả bộ test gần nhất:** 19/11 trên `55d01a8`: 1.437 đạt, 0 hỏng. SAU ĐÓ main gộp ba thay đổi code CHƯA có lượt cả bộ (`76ef380` · `26ccef9` · `1a9a0f8`; hai cờ mới đều TẮT) ⇒ chạy cả bộ TRƯỚC khi bật cờ nào.
- **Bẫy RAM (19/11):** không gom nhiều file test dựng cả app vào một tiến trình pytest; chạy từng file ở cây chính, không cùng lúc với server.
- **Máy:** mở lại máy ⇒ `/tmp` MẤT (worktree) và Qdrant TẮT: `docker compose up -d qdrant`, kiểm 9.436 điểm (runbook mục 1). Server không chạy sẵn.
- **Giới hạn đã biết:** `guides/RUNBOOK_BAN_GIAO.md` mục 10 — gặp hành vi trông như lỗi thì tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và hướng (việc đang mở KHÔNG ghi ở đây)

Thứ tự việc, KHÔNG gắn ngày — bước trước đạt và máy rảnh thì làm bước sau:

| Bước | Việc | Trạng thái |
|---|---|---|
| 1–4 | Cả bộ test · soát tích hợp · code đứng yên · lượt đo cuối phần đã thấy (18/11) · sửa câu thiếu cảnh báo bằng code (19/11) | XONG; bộ kín NOT RUN |
| 5 | **Đợt hoàn thiện local — theo hướng mới: việc PHỔ THÔNG của người dùng thật** (dưới) | đang làm; **điểm dừng = danh sách đóng 5 việc** (mục 4) + một lượt đo lại bộ 80 kịch bản |
| 6 | Deploy AWS (cần User một lần: tài khoản, khoá, ngân sách) | chưa |
| 7 | **User test TOÀN BỘ một lần** (`data/test_cuoi/DANH_SACH.md`) ⇒ User đóng Phase 9 | chưa |

**Việc đang mở, ai làm, bước kế:** CHỈ ở `session_prompt/VIEC_DANG_MO.md` (xong: `session_prompt/VIEC_DA_XONG.md`). Mốc "Phase 9 xong phần nhóm" = code `55d01a8`.

**Hướng của User từ 19/11:** việc 100 người dùng thật sẽ thử; thứ tự sửa + bước kế từng việc CHỈ ở `session_prompt/VIEC_DANG_MO.md`. KHÔNG mở thêm việc về bão / lũ / khẩn cấp. Trước khi thêm file, cờ, test, bước kiểm: "lỗi đã thấy thật chưa · ai dùng · không làm thì mất gì".

Số nhiễu (19/11): hai lượt bộ câu mẫu không đổi gì lệch 1 câu "Đúng" · 2 "Đủ ý" · 7 "Trọng tâm" ⇒ thử đổi lời dặn phải có bên tắt CÙNG BUỔI, chấm cùng lô.
Hai con số đo cách làm: `SO_CAI_TIEN_CACH_LAM.md`. Hỏi User > 8 hộp / ngày ⇒ gom câu.

## 3. Đang chờ User (chỉ những việc ghi ở đây đang chờ User; việc đã chốt hoặc đã hỏi rồi thì đừng hỏi lại)

1. User tự làm: trần chi tiêu trên từng khoá API · vô hiệu hoá khoá AWS cũ trong thư mục khoá học.
2. Buổi User tự tay test toàn bộ (bước 7) — User chưa có giờ; KHÔNG nhắc.
3. Hỏi khi tới lượt (sau khi đủ điều kiện ở `VIEC_DANG_MO.md`): bật cờ `noi_that_lam_thay` · bật hai nút xuất lịch (`xuat_pptx`) · giá phòng, bổ sung kho, vị trí người dùng.

## 4. Quyết định còn hiệu lực — không hỏi lại, không trình lại như lỗi

Sản phẩm:
- Trả lời chỉ từ kho, có nguồn; câu ngoài kho phải bị từ chối (sàn: 0 câu ngoài kho được trả lời bằng kho). Người dùng gõ tiếng Việt CÓ DẤU; không làm tiếng Anh.
- Câu khẩn cấp (bị cướp, mất ví, mất giấy tờ, số khẩn cấp) là NGOÀI PHẠM VI — User chốt ba lần; không sửa, không báo lại.
- Bão / lũ / khẩn cấp: hành vi đang có giữ nguyên, không đầu tư thêm (giới hạn đã nhận: runbook mục 10).
- **19/11 — User TỰ NÊU:** chất lượng trước, tiền / tốc độ sau · làm việc phổ thông, không dồn công vào bão / lũ / khẩn cấp · báo cáo theo thư mục ngày · tự nhắc nhau không over-engineer.
- **19/11 — User CHỌN Ô (sáng – trưa):** "Sửa lỗi an toàn trước" · "Chung tính sàn, riêng đọc tay" · "Làm bản code rồi ghi mốc" · "Bật ngay, ghi giới hạn" · cả bốn nhóm việc phổ thông · "Chèn hai lỗi nặng lên trước" (thứ tự ở mục 2).
- **19/11 — User CHỌN (chiều):** giữ mức suy luận mặc định (đo xong) · giá vé = chép giá kho ĐÃ CÓ vào bảng điểm · lượt nhờ "làm thay": ba câu nói thật do code chọn, không mục web; KHÔNG làm gửi email; đặt / hỏi phòng không giả lập · xuất lịch: PDF in từ trình duyệt + PowerPoint do code vẽ, GIỮ kiểu "Di sản" của nhóm (đã cho bốn agent khác hãng thi, User vẫn chọn bản nhóm) · agent được gọi PowerPoint của Windows để dựng slide thử ra ảnh (chỉ file thử, một file một lần, thấy PowerPoint đang mở thì không gọi) · **"lịch vào lượt hỏi thường": BẬT RIÊNG phần lịch + số giờ** (tổng tiền vé model tự cộng — giới hạn đã nhận; phần tiền vé bằng code chưa bật).
- **19:13 19/11/2026 — User CHỌN điểm dừng bước 5 = "danh sách vừa":** lịch đã lưu vào lượt hỏi thường · nói thật giới hạn · xuất lịch · hỏi tiếp về thứ vừa gợi ý · câu xin danh sách trả thiếu mục; rồi MỘT lượt đo lại bộ 80 kịch bản (chỉ báo trước → sau; không ngưỡng số vì hai người chấm lệch 8 / 80). "Gần X", ngày của nguồn giá vé, ngân sách do code tính = giới hạn đã biết, KHÔNG làm trước khi đóng Phase 9.
- Không nói giá phòng ở phần gợi ý chỗ ở (câu hỏi chi phí chung vẫn nêu khoảng giá có nguồn từ kho). Khối "Nơi ở" chỉ hiện khi người dùng
  đã chọn hạng chỗ ở — ở biểu mẫu hoặc nói bằng lời.
- Việc phải luôn đúng (phép tính, ngày, tiền, thứ tự bắt buộc) do CODE làm; model chỉ diễn đạt. Giữ model `gpt-6-luna`, giữ `e5-small`; số đoạn / cách đưa ngữ cảnh: đang thử (plan đã duyệt; bật gì do User quyết).
- **User 10:04 19/11/2026 — GỠ rào tối ưu sớm:** bỏ sàn tiền / câu, sàn tốc độ chữ đầu, trần token đầu ra, ngân sách ngữ cảnh, trần lịch sử (tiền / giây chỉ ĐO và BÁO); được dùng tiền API để thử — một việc > 1 USD báo trước (riêng việc "ngữ cảnh lớn hơn" đã duyệt, trần 1,40). Lỗi tệ nhất trước: sai cảnh báo an toàn > nói chắc mà sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.
- KHÔNG in chữ ghi công / tác giả / giấy phép ảnh ở đâu người dùng thấy (màn hình, bản in, file tải về), không lọc ảnh theo giấy phép — User 14/11, nhắc lại 19/11.
- Không mở lại khi User chưa nêu: giọng nói (dẹp) · so ảnh bằng embedding (hoãn, chưa có ngày; ảnh mẫu còn giữ) · nhớ sở thích người dùng (không làm) ·
  "tra web sớm" (bỏ) · "gộp câu tìm" (gác) · mục web giữ bản dài (bản gọn đã thử, không dùng).
- User chỉ chưa có giờ TỰ TAY TEST (một lần ở cuối); vẫn duyệt, trao đổi bình thường ⇒ việc "hỏi User trước" hỏi ngay; nhóm không chờ User đóng Phase 9. Deploy AWS: sau đợt hoàn thiện local.
- Đây là ĐỒ ÁN TỐT NGHIỆP, chấm một lần — tài liệu không dùng chữ "sếp" / "công ty"; gói "giảng viên hỏi vặn" làm sau khi hệ thống hoàn tất.

Cách làm:
- Quyền theo bảng "Quyền thường trực" trong `AGENTS.md` — KHÔNG hỏi "quyền phiên" mỗi lần mở. Cách làm việc áp cho mọi coding agent, không gắn mốc ngày nào.
- Chất lượng cần thiết trước, tốc độ / tiền sau. Đổi gì có đo: ghi tiêu chí TRƯỚC, đổi một thứ, so với mốc. Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật.
- Test thật, dữ liệu thật, kết quả thật; được dùng tiền API để đo / thử (ghi số thật). Báo cáo tách "test bằng đồ giả" ↔ "lượt thật".
- Người viết không tự kiểm. Sau mỗi đợt gộp lớn soát chỗ các tính năng gặp nhau · định kỳ soát độ thật của test. Giám khảo khác hãng: ở MỐC CHỐT, qua
  một file `.md`, User chỉ gửi khi nhóm YÊU CẦU rõ; mặc định GPT sol + Gemini 4 Hydrogen (bỏ Carbon).
- Báo cáo "xong" kết bằng bảng: đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra. Báo cáo cho User: người dùng thấy gì khác · bằng chứng · giới hạn ·
  cách thử 2 phút; mỗi khẳng định gắn nhãn [máy kiểm] / [người thứ hai kiểm] / [chưa kiểm].
- Hỏi User: mỗi lần MỘT câu, có sẵn đáp án, mỗi đáp án kèm hệ quả. Tiếng Việt, lời thường, đủ quan trọng hơn ngắn. Giờ ghi vào tài liệu lấy bằng `date`.
- Lỗi cách làm lặp lần hai mới thành luật; máy kiểm được thì làm phép kiểm thay chữ. Không thêm công cụ / rào riêng tư mới (User 14/11) — giữ rào đang có.
- User không vắng trừ khi tự nói "đi vắng" (User 15/11). Không bao giờ gọi `agy` từ agent. Repo PUBLIC: `data/`, kho, câu của bộ đo không vào file được git theo dõi.
- Thứ ngoài git (`data/`, kho, chỉ mục) sao lưu sang ổ khác cùng máy (18/11) — chép lại ở mỗi mốc chốt. Câu kín chỉ còn luật chữ giữ.
- "Gói mở lại nhẹ" (User duyệt 18/11): kết phiên nhẹ · mở phiên đọc ngắn · chỉ mở lại phiên đã đầy · phiên mới đợi tin của phiên điều phối.
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
