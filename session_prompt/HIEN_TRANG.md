# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 13:12 18/11/2026 (kết phiên sáng); sửa mục 1, 2, 4, 6 lúc 13:55 18/11/2026 (giờ `date`). Người giữ: phiên điều phối.

**Trang này là gì.** Ảnh chụp "bây giờ" của dự án, cho BẤT KỲ coding agent nào (Claude Code, Codex, Antigravity) vừa mở phiên. Nó được **viết lại tại chỗ**
mỗi lần kết phiên — không nối thêm. Thứ tự mở phiên (bạn là phiên nào, báo gì, chờ gì) ở `session_prompt/START_SESSION.md`; trang này là phần "dự án đang
thế nào" của bước đọc; sổ việc dài chỉ mở khi cần. `AGENTS.md` thắng trang này; code / file cấu hình thắng trang này — thấy lệch thì báo để sửa trang.

Từ dùng trong trang: **phiên** = một cửa sổ agent đang chạy · **phiên điều phối (A)** = phiên nói chuyện với User và giao việc; **B, C, E** = phiên làm việc; **D** = phiên giảng cho User (tuỳ chọn, chỉ đọc). Làm MỘT MÌNH ⇒
"báo / hỏi phiên điều phối" = hỏi User (`guides/KHI_CHI_CO_MOT_AGENT.md`) ·
**User** = chủ dự án (không đọc code; đọc báo cáo và `bai_hoc/`) · **kho** = bộ bài viết Markdown riêng tư mà trợ lý được phép trả lời từ đó ·
**cờ** = một dòng bật / tắt tính năng trong `backend/config/settings.yaml` · **bộ câu mẫu** (tên cũ "Golden") = 176 câu hỏi kèm đáp án để chấm, riêng tư ·
**câu kín** (`*sealed*`) = bộ câu giữ riêng, agent không được mở · **sổ vết** = bản ghi debug từng lượt hỏi, có nội dung · **lượt đo cuối** = lần chấm toàn bộ
trợ lý trên bản code đã đứng yên.

## 1. Hệ thống đang chạy

- **Là gì:** trợ lý hỏi đáp du lịch – văn hoá Huế cho du khách và người dân (đồ án tốt nghiệp của User; hiện chỉ User và nhóm dùng thử), trả lời CHỈ từ kho, có ghi nguồn; kho không có thì từ chối, rồi tra web một lần ở mục riêng "chưa kiểm".
  Web: FastAPI (`backend/`) + giao diện React dựng sẵn (`frontend/`). Chạy trên máy User; **chưa deploy**.
- **Số hôm nay** (lệnh kiểm: runbook mục 0): kho **265 bài ⇒ 9.436 đoạn**, một collection Qdrant `hue_full_corpus_7a2_e5_small_384` (cổng 6335);
  tìm = vector `e5-small` + từ khoá BM25 trộn RRF, **10 đoạn** vào ngữ cảnh, không xếp lại; model viết `gpt-6-luna` (OpenAI); tra web qua Serper.
- **Cờ:** **23 BẬT** (22 cờ ở mục `assistant:` của `backend/config/settings.yaml` + `anh.bat`). **TẮT (đủ 4 cờ còn lại):** `lich_trinh`
  (lịch từ câu gõ tự do — không đạt; nay qua biểu mẫu), `today_line` (vô ích), `nho_cau_tra_loi` (từng mượn nhầm đoạn của nơi khác), `so_vet` (mặc định
  tắt; bật bằng biến `HUE_SO_VET=true` lúc mở server, chỉ ở máy local).
- **Mỗi cờ làm gì, bằng lời thường, kèm số đo:** bảng "Cái gì ĐANG chạy" của `bai_hoc/BAN_DO_DU_AN.md`.
- **Lần chạy cả bộ test gần nhất:** 17/11, 1.345 đạt (theo sổ việc; CHƯA chạy lại — lượt kế trước tối thứ Bảy 21/11).
- **Máy lúc 13:37 18/11/2026:** Qdrant TẮT, server không chạy. Bật (báo điều phối trước): `docker compose up -d qdrant`.
- **Giới hạn đã biết + đường cũ đừng chép:** `guides/RUNBOOK_BAN_GIAO.md` mục 10. Gặp hành vi trông như lỗi ⇒ tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và việc đang mở

Mốc (User chốt theo THỨ, 18/11/2026):

| Khi nào | Việc |
|---|---|
| Cuối MỖI ngày | Vòng tự cải thiện cách làm: đọc hai con số · lỗi lặp lần hai ⇒ máy trước chữ sau · thêm bao nhiêu gỡ bấy nhiêu (CHƯA chạy lần nào) |
| Sáng thứ Bảy 21/11 | User tự bật hệ thống theo runbook mục 1–3, gõ ~10 câu tự chấm, xem sổ vết, đọc trang bản đồ + bài 26 (45–60 phút, User chốt 18/11); phiên điều phối ngồi cạnh, không làm hộ |
| Thứ Bảy 21/11, trước tối | Chạy cả `backend/tests` một lượt trên `main` · gói soát mù cho model hãng khác (file riêng tư `data/review_khac_hang/2026-11-21_truoc_dung_code/DE_BAI.md` — A xem phạm vi trước) |
| Tối thứ Bảy 21/11 | **Code đứng yên**; ghi mã commit đứng yên vào sổ đo |
| Chủ nhật 22/11 | **Lượt đo cuối** (lệnh: file riêng tư `data/phase_9/b7/tools/RUNBOOK_CUOI.md`; trần 0,45 USD; phiên B chạy) |
| Khoảng thứ Hai 23/11 | Đọc kết quả ⇒ User đóng Phase 9; sau đó vòng tự tối ưu bản hẹp ở bước tìm (đã duyệt, CHƯA có kế hoạch) |
| Tối thứ Ba 24/11 | User lái Codex rồi Antigravity làm thử thay Claude; chạy lại 7 đề chấm skill (file riêng tư `data/cham_skill_2026-11-18/de/`) |

Đã vào `main` 18/11: xem `git log --merges --oneline -25`.

Việc đang mở (ai · việc · trạng thái) — chi tiết ở sổ việc (mục 7):
- **A:** trò chuyện với User về cách làm việc; runbook mục 9; gói soát mù thứ Bảy; gộp nhánh.
- **B:** lượt đo cuối Chủ nhật 22/11; giữ trang bản đồ.
- **C:** giữ trang này; runbook mục 10; 2 skill mới đã chấm MỘT lượt (chưa có người chấm thứ hai); 4 skill cũ chưa chấm để tối thứ Ba 24/11.
- **E:** 8 skill sửa + 2 skill mới (`soat-tich-hop`, `giao-viec-agent-con`) ĐÃ vào `main`; hai skill mới đã chấm một lượt; A áp file luật + liên kết `.claude/skills/`.
  E giữ `guides/CACH_LAM_VIEC.md`.
- **Chưa ai nhận, để sau lượt đo cuối:** các hàng "sửa sau lượt đo cuối" của runbook 10.3b · lỗi tìm "quán gần một chùa lớn" (10.1) · lịch đi vòng trong cùng
  quần thể (10.2) · runbook mục 8 (deploy) — chỉ viết khi User mở lại chuyện deploy.

Từ nay tới tối thứ Bảy 21/11: chỉ sửa lỗi đã tái hiện được; không thêm tính năng; đổi chuỗi gửi model ⇒ hỏi phiên điều phối trước.

Hai con số đo cách làm (tuần 16–22/11, đếm từ 18/11 — A đếm, chưa ai soát): việc đã báo "xong" bị lật lại **4** · User phải nhắc lại một điều đã nói **5**.

## 3. Đang chờ User (gom một chỗ — đừng hỏi lại thứ không có ở đây)

1. User tự làm: trần chi tiêu trên từng khoá API · vô hiệu hoá khoá AWS cũ trong thư mục khoá học.
2. Ba lệnh đếm bộ câu kín trước lượt đo cuối (ở `RUNBOOK_CUOI.md`) — *chưa kiểm đã chạy chưa*. Deploy / AWS: chỉ hỏi lại SAU khi Phase 9 đóng.

## 4. Quyết định còn hiệu lực — không hỏi lại, không trình lại như lỗi

Sản phẩm:
- Trả lời chỉ từ kho, có nguồn; câu ngoài kho phải bị từ chối (sàn: 0 câu ngoài kho được trả lời bằng kho). Người dùng gõ tiếng Việt CÓ DẤU; không làm tiếng Anh.
- Câu khẩn cấp (bị cướp, mất ví, mất giấy tờ, số khẩn cấp) là NGOÀI PHẠM VI — User chốt ba lần; không sửa, không báo lại.
- Không nói giá phòng ở phần gợi ý chỗ ở (câu hỏi chi phí chung vẫn nêu khoảng giá có nguồn từ kho). Khối "Nơi ở" chỉ hiện khi người dùng
  đã chọn hạng chỗ ở — ở biểu mẫu hoặc nói bằng lời.
- Việc phải luôn đúng (phép tính, ngày, tiền, thứ tự bắt buộc) do CODE làm; model chỉ diễn đạt. Giữ model `gpt-6-luna`, giữ `e5-small`, giữ 10 đoạn.
- Sàn tốc độ: chữ đầu tiên trên trình duyệt p50 ≤ 3 s, p95 ≤ 5 s; tiền TRUNG BÌNH ≤ 0,0005 USD / câu (câu có tìm thêm / web được vượt). Thứ tự lỗi tệ nhất: sai cảnh báo an toàn > nói chắc mà sai >
  trả lời câu ngoài kho > thiếu ý > từ chối nhầm.
- Không mở lại khi User chưa nêu: giọng nói (dẹp) · so ảnh bằng embedding (hoãn, chưa có ngày; ảnh mẫu còn giữ) · nhớ sở thích người dùng (không làm) ·
  "tra web sớm" (bỏ) · "gộp câu tìm" (gác) · mục web giữ bản dài (bản gọn đã thử, không dùng).
- Deploy / AWS chỉ bàn khi dự án xong ở máy local.
- Đây là ĐỒ ÁN TỐT NGHIỆP, chấm một lần, User trình bày với giảng viên — tài liệu không dùng chữ "sếp" / "công ty"; gói "giảng viên hỏi vặn" làm sau khi
  hệ thống hoàn tất và User đã đọc bài học.

Cách làm:
- Quyền theo bảng "Quyền thường trực" trong `AGENTS.md` — KHÔNG hỏi "quyền phiên" mỗi lần mở. Cách làm việc áp cho mọi coding agent, không gắn mốc ngày nào.
- Chất lượng cần thiết trước, tốc độ / tiền sau. Đổi gì có đo: ghi tiêu chí TRƯỚC, đổi một thứ, so với mốc. Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật.
- Test thật, dữ liệu thật, kết quả thật; được dùng tiền API để đo / thử (ghi số thật). Báo cáo tách "test bằng đồ giả" ↔ "lượt thật".
- Người viết không tự kiểm. Hai thói quen kiểm thử (User chọn 18/11): sau mỗi đợt gộp lớn soát chỗ các tính năng gặp nhau · định kỳ soát
  độ thật của test (test nào thay hẳn phần cần kiểm). Giám khảo khác hãng: dùng ở MỐC CHỐT, qua một file `.md`;
  User chỉ gửi khi nhóm YÊU CẦU rõ; mặc định GPT sol + Gemini 4 Hydrogen (bỏ Carbon — quá lâu).
- Mọi báo cáo "xong" kết bằng bảng: đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra. Báo cáo cho User có 4 ý: người dùng thấy gì khác · bằng chứng ·
  chưa làm / giới hạn · cách thử trong 2 phút; mỗi khẳng định gắn nhãn [máy kiểm] / [người thứ hai kiểm] / [chưa kiểm].
- Hỏi User: mỗi lần MỘT câu, có sẵn đáp án, mỗi đáp án kèm hệ quả. Tiếng Việt, lời thường, đủ quan trọng hơn ngắn. Giờ ghi vào tài liệu lấy bằng `date`.
- Lỗi cách làm lặp lần hai mới thành luật; máy kiểm được thì làm phép kiểm thay chữ. Không thêm công cụ / rào riêng tư mới (User 14/11) — giữ rào đang có.
- User không vắng trừ khi tự nói "đi vắng" (User 15/11). Không bao giờ gọi `agy` từ agent. Repo PUBLIC: `data/`, kho, câu của bộ đo không vào file được git theo dõi.
- Thứ ngoài git (`data/`, kho, chỉ mục) đã sao lưu sang ổ khác cùng máy 11:45 18/11 — chép lại ở mỗi mốc chốt. Câu kín chỉ còn luật chữ giữ (User chọn).
- "Gói mở lại nhẹ" khi tắt / mở lại phiên (User duyệt 18/11; đang thử ba lần mở kế): kết phiên nhẹ · mở phiên đọc ngắn · chỉ mở lại phiên đã đầy ·
  phiên mới đợi tin của phiên điều phối. Chi tiết: sổ việc, khối PHIÊN CHIỀU 18/11.
- User chỉ đọc `bai_hoc/`: việc xong mới viết vào đó, mỗi con số kèm đo gì / so với mốc nào.

Danh sách đủ, có ngày và nguồn: `session_prompt/Project_Status.md` mục 5 (nhật ký — chỉ mở khi cần tra một quyết định cụ thể).

## 5. Bật hệ thống và kiểm

Lệnh từng bước, kết quả mong đợi, điều kiện dừng: `guides/RUNBOOK_BAN_GIAO.md` mục 1 (Qdrant), 2 (giao diện + server), 3 (test). Ba điều hay vấp:
mọi lệnh Python chạy từ thư mục `backend/` bằng `uv run …`; máy dùng chung với dự án khác ⇒ việc nặng (server, cả bộ test, dựng chỉ mục, đo) báo phiên điều
phối trước và dừng khi RAM khả dụng < 4 GB; bật hook git một lần sau khi clone: `git config core.hooksPath .githooks`.

## 6. Lệnh kiểm các con số của trang này

Ba lệnh (số bài / số đoạn của kho · Qdrant khớp · số cờ bật) kèm kết quả phải ra: `guides/RUNBOOK_BAN_GIAO.md` mục 0, bảng "Kiểm số của trang hiện trạng".

## 7. Nhật ký ở đâu (KHÔNG bắt đọc lúc mở phiên — mở khi cần trả lời một câu cụ thể)

- `session_prompt/CURRENT_HANDOFF.md` — sổ việc theo giờ (khối đầu mới nhất) · `session_prompt/sessions/STATUS_<X>.md` — sổ riêng từng phiên (đọc mục đầu của mình).
- `session_prompt/Project_Status.md` — mục 4 chi tiết từng tính năng + mã commit · mục 5 mọi quyết định theo ngày · mục 8 bẫy kỹ thuật · việc đã đóng: `PROJECT_HISTORY.md`, `archive/` (cùng chỗ).
- Luật đầy đủ: `session_prompt/Session_Prompt.md`, `session_prompt/WORKFLOW.md` · cách làm việc: `guides/CACH_LAM_VIEC.md`.

## 8. Cách giữ trang này

Kết phiên: người giữ VIẾT LẠI mục 1–4 cho đúng lúc đó (xoá thứ đã xong, không ghi "trước đó…"); chi tiết theo giờ để ở nhật ký. Quyết định mới của User ⇒ thêm
vào mục 4 NGAY trong phiên. Giới hạn ≤ 150 dòng và ≤ 14.000 byte (`wc -lc`; có công cụ cắt file hướng dẫn ở
24.000 byte). Phép thử: agent ngữ cảnh mới chỉ đọc `AGENTS.md` + trang này trả lời tám câu ở `guides/khung/HIEN_TRANG.mau.md`.
