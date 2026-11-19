# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 10:49 19/11/2026 (giờ `date`; sau khi bật hai cờ, User đổi hướng ưu tiên). Người giữ: phiên C (phiên điều phối sửa mục 2–3 lúc kết phiên).

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
- **Lần chạy cả bộ test gần nhất:** 19/11 trên `main` `55d01a8` (hai cờ mới bật, đã gỡ ngân sách ngữ cảnh): 1.437 đạt, 0 hỏng (B).
- **Máy:** mở lại máy ⇒ `/tmp` MẤT (worktree) và Qdrant TẮT: `docker compose up -d qdrant`, kiểm 9.436 điểm (runbook mục 1). Server không chạy sẵn.
- **Giới hạn đã biết:** `guides/RUNBOOK_BAN_GIAO.md` mục 10 — gặp hành vi trông như lỗi thì tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và việc đang mở

Thứ tự việc — KHÔNG gắn ngày: bước trước đạt và máy rảnh là làm bước sau ngay:

| Bước | Việc | Trạng thái |
|---|---|---|
| 1–4 | Cả bộ test · soát tích hợp · code đứng yên · lượt đo cuối phần đã thấy (18/11, có mục không đạt) | XONG; bộ kín NOT RUN |
| 4b | Sửa lỗi an toàn trước khi ghi mốc (User 19/11): câu thiếu cảnh báo "tạm ngừng mùa lũ" | bản lời dặn KHÔNG đạt (không vào main); bản CODE đã bật, giới hạn ở runbook 10.1 |
| 5 | **Đợt hoàn thiện local — theo hướng mới: việc PHỔ THÔNG của người dùng thật** (dưới) | đang bàn với User |
| 6 | Deploy AWS (cần User một lần: tài khoản, khoá, ngân sách) | chưa |
| 7 | **User test TOÀN BỘ một lần** (`data/test_cuoi/DANH_SACH.md`) ⇒ User đóng Phase 9 | chưa |

**Hướng của User từ 19/11:** KHÔNG mở thêm việc nào về bão / lũ / khẩn cấp (hành vi an toàn đang có giữ nguyên). Ưu tiên việc 100 người dùng thật sẽ thử: hỏi đáp +
xác nhận thông tin · gợi ý quán / chỗ ở / địa chỉ · lịch trình + ngân sách · làm thay (đặt phòng, gửi thư) · việc phổ thông khác. Ba phiên đã nộp danh sách việc;
phiên điều phối gom, hỏi User từng câu. Mốc "Phase 9 xong phần nhóm" = code `55d01a8`, kèm danh sách mục chưa đạt (sổ việc).

Việc đang mở (ai · việc) — chi tiết ở sổ việc (mục 7):
- **A:** gom ba danh sách "việc phổ thông", tra cứu + xin tư vấn model khác hãng, hỏi User; gộp nhánh; ghi mốc.
- **B:** thí nghiệm mức suy luận low / medium / high (User duyệt chi phí; plan của E); lượt cả bộ test trên `main`.
- **C:** giữ trang này + runbook mục 10; đọc tay thí nghiệm mức suy luận; góc lịch trình + ngân sách.
- **E:** plan mức suy luận; góc "làm thay"; giữ `guides/CACH_LAM_VIEC.md`.
- **Chưa ai nhận:** mục không đạt còn lại của lượt đo cuối (câu ngoài kho trả lời sai khuôn · câu tụt "Đủ ý") · lỗi tìm "quán gần một chùa lớn" (10.1) · runbook mục 8.

Số nhiễu (19/11): hai lượt bộ câu mẫu không đổi gì lệch 1 câu "Đúng" · 2 "Đủ ý" · 7 "Trọng tâm" ⇒ phép thử đổi lời dặn phải có bên tắt CÙNG BUỔI, chấm cùng lô.
Hai con số đo cách làm (bị lật lại · User nhắc lại): `SO_CAI_TIEN_CACH_LAM.md`. Hỏi User > 8 hộp / ngày ⇒ gom câu.

## 3. Đang chờ User (chỉ những việc ghi ở đây đang chờ User; việc đã chốt hoặc đã hỏi rồi thì đừng hỏi lại)

1. User tự làm: trần chi tiêu trên từng khoá API · vô hiệu hoá khoá AWS cũ trong thư mục khoá học.
2. Buổi User tự tay test toàn bộ (bước 7) — User chưa có giờ; KHÔNG nhắc. Việc thuộc hàng "hỏi User trước" thì vẫn hỏi ngay, một câu có đáp án.
3. Chọn việc phổ thông làm trước + gửi file xin tư vấn model khác hãng — phiên điều phối đưa.

## 4. Quyết định còn hiệu lực — không hỏi lại, không trình lại như lỗi

Sản phẩm:
- Trả lời chỉ từ kho, có nguồn; câu ngoài kho phải bị từ chối (sàn: 0 câu ngoài kho được trả lời bằng kho). Người dùng gõ tiếng Việt CÓ DẤU; không làm tiếng Anh.
- Câu khẩn cấp (bị cướp, mất ví, mất giấy tờ, số khẩn cấp) là NGOÀI PHẠM VI — User chốt ba lần; không sửa, không báo lại.
- Bão / lũ / khẩn cấp: KHÔNG đầu tư thêm (User 19/11); hỏi tiếp sau câu bão chỉ xét câu liền trước; dòng "tạm ngừng" chỉ hiện khi câu trả lời trích bài có cảnh báo — giới hạn đã nhận.
- Không nói giá phòng ở phần gợi ý chỗ ở (câu hỏi chi phí chung vẫn nêu khoảng giá có nguồn từ kho). Khối "Nơi ở" chỉ hiện khi người dùng
  đã chọn hạng chỗ ở — ở biểu mẫu hoặc nói bằng lời.
- Việc phải luôn đúng (phép tính, ngày, tiền, thứ tự bắt buộc) do CODE làm; model chỉ diễn đạt. Giữ model `gpt-6-luna`, giữ `e5-small`; số đoạn / cách đưa ngữ cảnh: đang mở lại để thử (A hiểu từ lời User 10:04 19/11 về cách đưa ngữ cảnh; đã báo, User chưa phản đối; bật gì do User quyết).
- **User 10:04 19/11/2026: chất lượng TRƯỚC, tiền / tốc độ sau — GỠ các rào tối ưu sớm:** bỏ sàn tiền "TB ≤ 0,0005 USD / câu" và sàn tốc độ "chữ đầu p50 ≤ 3 s, p95 ≤ 5 s" (từ nay tiền / giây chỉ ĐO và BÁO cạnh chất lượng, không dùng để loại phương án; đặt lại sau khi chất lượng đã đạt, User quyết); bỏ trần token đầu ra (đã gỡ); bỏ ngân sách ngữ cảnh 16.384 token / lượt; bỏ trần lịch sử 1.500 token; thử mức suy luận low / medium / high; User cho dùng tiền API để thử (một việc > 1 USD vẫn báo trước). Thứ tự lỗi tệ nhất giữ nguyên: sai cảnh báo an toàn > nói chắc mà sai >
  trả lời câu ngoài kho > thiếu ý > từ chối nhầm.
- Không mở lại khi User chưa nêu: giọng nói (dẹp) · so ảnh bằng embedding (hoãn, chưa có ngày; ảnh mẫu còn giữ) · nhớ sở thích người dùng (không làm) ·
  "tra web sớm" (bỏ) · "gộp câu tìm" (gác) · mục web giữ bản dài (bản gọn đã thử, không dùng).
- User chỉ chưa có giờ TỰ TAY TEST (test toàn bộ một lần ở cuối); vẫn duyệt, trao đổi bình thường ⇒ việc "hỏi User trước" hỏi ngay, không dồn; nhóm không chờ User đóng Phase 9 mới làm tiếp. Deploy AWS: sau đợt hoàn thiện local.
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
