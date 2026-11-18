# HIỆN TRẠNG hue_rag — trang agent đọc khi mở phiên

Viết lại lần cuối: 10:36 18/11/2026 (giờ `date`), trên `main` `d3330eb`. Người giữ: phiên điều phối. Mục 4: phiên B đã soát 13 ý với nguồn.

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
- **Số hôm nay** (lệnh kiểm ở mục 6): kho **265 bài ⇒ 9.436 đoạn**, một collection Qdrant `hue_full_corpus_7a2_e5_small_384` (cổng 6335);
  tìm = vector `e5-small` + từ khoá BM25 trộn RRF, **10 đoạn** vào ngữ cảnh, không xếp lại; model viết `gpt-6-luna` (OpenAI); tra web qua Serper.
- **Cờ đang BẬT** (23 = 22 cờ ở mục `assistant:` của `backend/config/settings.yaml` + `anh.bat`): `router`, `song_song_tra_loi`, `tim_them`, `het_luot_bo_cong_cu`,
  `nho_hoi_thoai`, `cau_nhieu_y`, `may_have_changed_notice`, `tra_web`, `web_cau_noi_tiep`, `thoi_tiet`, `bao_lu_cong_cu`, `ngay_lich`, `khoang_cach`,
  `khoang_cach_tinh_san`, `lich_trinh_bieu_mau`, `len_ke_hoach_v2`, `anh_lich`, `ban_do_lich`, `luu_tru_lich`, `quan_lich`, `sua_lich_v2`,
  `sua_lich_chua_ho_tro`, `anh.bat`. **TẮT (đủ 4 cờ còn lại):** `lich_trinh` (lịch từ câu gõ tự do — bản đầu, không đạt; lịch nay đi qua biểu mẫu `len_ke_hoach_v2`),
  `today_line` (không giúp gì), `nho_cau_tra_loi` (từng mượn nhầm đoạn của nơi khác), `so_vet` (mặc định tắt; muốn xem sổ vết thì mở server kèm biến
  `HUE_SO_VET=true` — chỉ ở máy local, bản công khai không đặt).
- **Mỗi cờ làm gì, bằng lời thường, kèm số đo:** bảng "Cái gì ĐANG chạy" của `bai_hoc/BAN_DO_DU_AN.md`; chú thích kỹ thuật nằm cạnh
  từng dòng cờ trong `settings.yaml`.
- **Lần chạy cả bộ test gần nhất:** 17/11, 1.345 đạt (theo sổ việc; CHƯA chạy lại trên bản hiện tại — lượt kế trước tối thứ Bảy 21/11).
- **Giới hạn đã biết + đường cũ đừng chép:** `guides/RUNBOOK_BAN_GIAO.md` mục 10. Gặp hành vi trông như lỗi ⇒ tra ở đó TRƯỚC khi sửa hay báo.

## 2. Mốc và việc đang mở

Mốc (User chốt theo THỨ trong tuần, 18/11/2026 — chỗ nào tài liệu cũ ghi ngày lệch thứ thì theo bảng này):

| Khi nào | Việc |
|---|---|
| Sáng thứ Bảy 21/11 | User tự bật hệ thống theo runbook mục 1–3, hỏi mươi câu, xem sổ vết; phiên điều phối ngồi cạnh |
| Tối thứ Bảy 21/11 | **Code đứng yên**; trước đó chạy cả `backend/tests` một lượt trên `main` rồi ghi mã commit đứng yên vào sổ đo |
| Chủ nhật 22/11 | **Lượt đo cuối** (bộ công cụ + lệnh: file riêng tư `data/phase_9/b7/tools/RUNBOOK_CUOI.md`; trần 0,45 USD; phiên B chạy) |
| Khoảng thứ Hai 23/11 | Đọc kết quả ⇒ User đóng giai đoạn trợ lý (Phase 9) |
| Tối thứ Ba 24/11 | User lái Codex rồi Antigravity làm thử thay Claude (đọc tài liệu từ đầu ⇒ runbook mục 1–3 ⇒ một việc nhỏ) |

Việc đang mở (ai · việc · trạng thái) — chi tiết từng việc ở sổ việc (mục 7):
- **A:** trò chuyện với User về cách làm việc với coding agent; viết runbook mục 9; gộp nhánh.
- **B:** chạy lượt đo cuối Chủ nhật 22/11; giữ trang bản đồ `bai_hoc/BAN_DO_DU_AN.md` (đã gộp).
- **C:** giữ nháp trang này + mẫu `guides/khung/HIEN_TRANG.mau.md`; runbook mục 10 (giới hạn đã biết).
- **E:** `guides/CACH_LAM_VIEC.md` + bộ khung `guides/khung/` (đã gộp bản 2; còn rút gọn theo lượt đọc lại).
- **Chưa ai nhận, để sau lượt đo cuối:** hai chỗ câu thời tiết / bão bị nối nhầm vào câu hỏi tiếp không liên quan (hai hàng đầu bảng runbook 10.3b) · lỗi tìm
  "quán gần một chùa lớn" (10.1) · lịch đi vòng trong cùng quần thể (10.2) · runbook mục 8 (deploy) — chỉ viết khi User mở lại chuyện deploy.
- Nhánh đang chờ gộp lúc viết: `p9-runbook-g2-g6`, `p9-hien-trang-2` (đều chỉ tài liệu) — gộp sau khi một phiên KHÁC người viết đã đọc; đừng sửa nhánh của người khác.

Trước khi sửa code từ nay tới tối thứ Bảy 21/11: chỉ sửa lỗi đã tái hiện được; không thêm tính năng; đổi chuỗi gửi model ⇒ hỏi phiên điều phối trước.

Hai con số đo cách làm (ghi mỗi tuần; tuần 16–22/11, đếm từ 18/11 — A đếm, chưa ai soát): việc đã báo "xong" bị lật lại **2** · User phải nhắc lại một điều
đã nói **3**.

## 3. Đang chờ User (gom một chỗ — đừng hỏi lại thứ không có ở đây)

1. Gửi gói "giám khảo khác hãng" đầu tiên (một file đề bài để model hãng khác soát độc lập) cho Codex / Antigravity: file riêng tư `data/review_khac_hang/2026-11-18_tich_hop_phase_9/DE_BAI.md`.
2. Ba lệnh đếm bộ câu kín phải chạy trước lượt đo cuối (agent không được mở file kín; lệnh ở `RUNBOOK_CUOI.md`) — *theo sổ việc 15–17/11, chưa kiểm User đã chạy chưa*.
3. Chuyện deploy / AWS: phiên điều phối hỏi lại SAU khi Phase 9 đóng — trước đó không hỏi.
4. Trang này mới dùng từ 18/11: hai phiên tới đọc cả khối đầu sổ việc để bắt chỗ chép sót (lệch ⇒ sổ việc thắng, báo để sửa trang).

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

Cách làm:
- Quyền theo bảng "Quyền thường trực" trong `AGENTS.md` — KHÔNG hỏi "quyền phiên" mỗi lần mở. Cách làm việc áp cho mọi coding agent, không gắn mốc ngày nào.
- Chất lượng cần thiết trước, tốc độ / tiền sau. Đổi gì có đo: ghi tiêu chí TRƯỚC, đổi một thứ, so với mốc. Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật.
- Test thật, dữ liệu thật, kết quả thật; được dùng tiền API để đo / thử (ghi số thật). Báo cáo tách "test bằng đồ giả" ↔ "lượt thật".
- Người viết không tự kiểm. Hai thói quen kiểm thử (User chọn 18/11): sau mỗi đợt gộp lớn soát chỗ các tính năng gặp nhau · định kỳ soát
  độ thật của test (test nào thay hẳn phần cần kiểm). Việc mức cao: giám khảo khác hãng qua một file `.md` do User tự gửi.
- Mọi báo cáo "xong" kết bằng bảng: đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra. Báo cáo cho User có 4 ý: người dùng thấy gì khác · bằng chứng ·
  chưa làm / giới hạn · cách thử trong 2 phút; mỗi khẳng định gắn nhãn [máy kiểm] / [người thứ hai kiểm] / [chưa kiểm].
- Hỏi User: mỗi lần MỘT câu, có sẵn đáp án, mỗi đáp án kèm hệ quả. Tiếng Việt, lời thường, đủ quan trọng hơn ngắn. Giờ ghi vào tài liệu lấy bằng `date`.
- Lỗi cách làm lặp lần hai mới thành luật; máy kiểm được thì làm phép kiểm thay chữ. Không thêm công cụ / rào riêng tư mới (User 14/11) — giữ rào đang có.
- User không vắng trừ khi tự nói "đi vắng" (User 15/11). Không bao giờ gọi `agy` từ agent. Repo PUBLIC: `data/`, kho, câu của bộ đo không vào file được git theo dõi.
- User chỉ đọc `bai_hoc/`: việc xong mới viết vào đó, mỗi con số kèm đo gì / so với mốc nào.

Danh sách đủ, có ngày và nguồn: `session_prompt/Project_Status.md` mục 5 (nhật ký — chỉ mở khi cần tra một quyết định cụ thể).

## 5. Bật hệ thống và kiểm

Lệnh từng bước, kết quả mong đợi, điều kiện dừng: `guides/RUNBOOK_BAN_GIAO.md` mục 1 (Qdrant), 2 (giao diện + server), 3 (test). Ba điều hay vấp:
mọi lệnh Python chạy từ thư mục `backend/` bằng `uv run …`; máy dùng chung với dự án khác ⇒ việc nặng (server, cả bộ test, dựng chỉ mục, đo) báo phiên điều
phối trước và dừng khi RAM khả dụng < 4 GB; bật hook git một lần sau khi clone: `git config core.hooksPath .githooks`.

## 6. Lệnh kiểm các con số của trang này

| Kiểm gì | Lệnh (từ gốc repo) | Phải ra |
|---|---|---|
| Số bài / số đoạn của kho | `uv run python -c "import json;d=json.load(open('data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json'))['corpus'];print(d['file_count'],d['chunk_count'])"` | `265 9436` [đã chạy 18/11] |
| Qdrant khớp | `curl -s http://127.0.0.1:6335/collections/hue_full_corpus_7a2_e5_small_384 \| grep -o '"points_count":[0-9]*'` | `"points_count":9436` [đã chạy 18/11; cần Qdrant bật] |
| Cờ bật / tắt | `sed -n '/^assistant:/,$p' backend/config/settings.yaml \| grep -cE '^  [a-z_0-9]+: true'` | `23` [đã chạy 18/11] |
| Cách tìm, không xếp lại | `grep -nE 'retrieval_treatment\|reranker:' backend/config/settings.yaml` | `dense_bm25_rrf`, `none` [đã chạy 18/11] |

## 7. Nhật ký ở đâu (KHÔNG bắt đọc lúc mở phiên — mở khi cần trả lời một câu cụ thể)

- `session_prompt/CURRENT_HANDOFF.md` — sổ việc theo giờ (dài; khối trên cùng mới nhất) · `session_prompt/sessions/STATUS_<X>.md` — sổ riêng từng phiên (đọc mục đầu của mình).
- `session_prompt/Project_Status.md` — mục 4 chi tiết từng tính năng + mã commit · mục 5 mọi quyết định theo ngày · mục 8 bẫy kỹ thuật.
- Luật đầy đủ: `session_prompt/Session_Prompt.md`, `session_prompt/WORKFLOW.md` · cách làm việc: `guides/CACH_LAM_VIEC.md`.

## 8. Cách giữ trang này

Kết phiên: người giữ VIẾT LẠI mục 1–4 cho đúng lúc đó (xoá thứ đã xong, không ghi "trước đó…"); chi tiết theo giờ để ở nhật ký. Quyết định mới của User ⇒ thêm
vào mục 4 NGAY trong phiên. Số nào đổi ⇒ chạy lại lệnh mục 6 rồi mới sửa. Giới hạn ≤ 150 dòng và ≤ 14.000 byte (`wc -lc`; có công cụ cắt file hướng dẫn ở
24.000 byte). Phép thử: agent ngữ cảnh mới chỉ đọc `AGENTS.md` + trang này trả lời tám câu ở `guides/khung/HIEN_TRANG.mau.md` (18/11: 6 / 8 đủ ⇒ đã sửa).
