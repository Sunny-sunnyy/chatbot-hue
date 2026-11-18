# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 13:12 18/11/2026 (kết phiên sáng); sửa gần nhất 20:07 18/11/2026 (giờ `date`). Người giữ: phiên C (phiên điều phối sửa mục 2–3 lúc kết phiên).

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
- **Cờ:** **23 BẬT** (22 cờ ở mục `assistant:` của `backend/config/settings.yaml` + `anh.bat` = hỏi bằng ảnh). **TẮT (đủ 4 cờ còn lại):** `lich_trinh`
  (lịch từ câu gõ tự do — không đạt; nay qua biểu mẫu), `today_line` (vô ích), `nho_cau_tra_loi` (từng mượn nhầm đoạn của nơi khác), `so_vet` (mặc định
  tắt; bật bằng biến `HUE_SO_VET=true` lúc mở server, chỉ ở máy local).
- **Mỗi cờ làm gì, bằng lời thường, kèm số đo:** bảng "Cái gì ĐANG chạy" của `bai_hoc/BAN_DO_DU_AN.md`.
- **Lần chạy cả bộ test gần nhất:** 18/11, 1.375 đạt + 1 hỏng do mã commit đổi giữa lượt (chạy lại file đó: 13 đạt) — số của B.
- **Máy:** mở lại máy ⇒ `/tmp` MẤT (worktree, bản mốc đo) và Qdrant TẮT: `docker compose up -d qdrant`, kiểm 9.436 điểm (runbook mục 1). Server không chạy sẵn.
- **Giới hạn đã biết + đường cũ đừng chép:** `guides/RUNBOOK_BAN_GIAO.md` mục 10. Gặp hành vi trông như lỗi ⇒ tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và việc đang mở

Thứ tự việc — KHÔNG gắn ngày (User 18/11: không cố định thời gian; bước trước đạt và máy rảnh là làm bước sau ngay; chất lượng giữ nguyên):

| Bước | Việc | Đạt khi |
|---|---|---|
| 1 | Cả `backend/tests` một lượt trên `main`; sửa lỗi tái hiện được | 0 test hỏng do code |
| 2 | Agent con soát tích hợp (thay gói khác hãng) · tự chạy 5 mục "cách thử" của `bai_hoc/VIEC_MOI_XONG.md` | mỗi điểm đã tái hiện rồi sửa hoặc ghi runbook mục 10 |
| 3 | **Code đứng yên**: ghi mã commit vào sổ đo, chép sao lưu | có mã commit |
| 4 | **Lượt đo cuối** phần đã thấy (`data/phase_9/b7/tools/RUNBOOK_CUOI.md`; trần 0,45 USD; B chạy); bộ kín NOT RUN chờ User | mọi sàn đạt ⇒ "Phase 9 xong phần nhóm" |
| 5 | **Đợt hoàn thiện local**: tự tối ưu bước tìm · sửa lỗi hoãn (runbook mục 10) · công cụ kiểm · kế hoạch deploy | từng sửa đổi đo đạt, có người khác kiểm |
| 6 | Deploy AWS (cần User một lần: tài khoản, khoá, ngân sách) | kiểm trên bản đã lên mạng |
| 7 | **User test TOÀN BỘ một lần** (`data/test_cuoi/DANH_SACH.md`; bộ kín đo trên bản LÚC ĐÓ, báo cáo tách khỏi số bước 4) ⇒ User đóng Phase 9 | — |

Mỗi ngày: vòng tự cải thiện cách làm.

**Tới 20:07 18/11:** bước 0, 1 ĐẠT. Bước 2: 5 điểm (`data/review_tich_hop_2026-11-18/dot_2/`) — P1 / P2 đã sửa (`b1f4dc8`, C review đạt), P3–P5 ở runbook 10.3b. Kế: B chạy cả bộ test ⇒ bước 3.

Việc đang mở (ai · việc · trạng thái) — chi tiết ở sổ việc (mục 7):
- **A:** danh sách User test cuối (phiếu chấm: `data/tu_tay_2026-11-21/`); gộp nhánh.
- **B:** cả bộ test sau gộp P1 / P2; lượt đo cuối; sau đó plan vòng tự tối ưu + thử `ruff` (chỉ `backend/`, `scripts/`); giữ trang bản đồ.
- **C:** giữ trang này; runbook mục 10; sau bước 4: script kiểm đường dẫn, chấm 4 skill cũ.
- **E:** giữ `guides/CACH_LAM_VIEC.md`; 10 skill đã vào `main` — KHÔNG sửa chữ skill khi chưa có số chấm mới.
- **Chưa ai nhận, để sau lượt đo cuối:** các hàng "sửa sau lượt đo cuối" của runbook 10.3b · lỗi tìm "quán gần một chùa lớn" (10.1) · lịch đi vòng trong cùng
  quần thể (10.2) · runbook mục 8 (deploy) — viết ở bước 5.

Tới khi xong bước 4: chỉ sửa lỗi đã tái hiện được; không thêm tính năng; đổi chuỗi gửi model ⇒ hỏi phiên điều phối trước.

Hai con số đo cách làm (tuần 16–22/11; B soát): việc đã báo "xong" bị lật lại **5** · User phải nhắc lại điều đã nói **6**. Hỏi User chiều 18/11: 8 hộp (> 8 ⇒ gom câu; A đếm ngay lúc hỏi).

## 3. Đang chờ User (chỉ những việc ghi ở đây đang chờ User; việc đã chốt hoặc đã hỏi rồi thì đừng hỏi lại)

1. User tự làm: trần chi tiêu trên từng khoá API · vô hiệu hoá khoá AWS cũ trong thư mục khoá học.
2. Dời về buổi test toàn bộ cuối (User chốt 18/11, KHÔNG nhắc trước đó): buổi tự tay, gói khác hãng, lệnh bộ kín, đóng Phase 9.

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
- User 18/11: bỏ qua phần cần User, làm hết phần không cần; cuối cùng User test toàn bộ một lần. Deploy AWS: sau đợt hoàn thiện local, xong sớm thì làm luôn.
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
