# VIỆC ĐANG MỞ — sổ việc hue_rag

Cập nhật: 14:48 25/11/2026 (giờ `date`; phiên điều phối cập nhật sau khi chủ dự án chốt 4 quyết định chiều 25/11, chuẩn bị bật `/swarm`). Người giữ: phiên điều phối (A).

**Sổ việc = trang này:** chỉ giữ việc đang mở, câu chờ chủ dự án, nhánh thử còn giữ và nợ còn sống. Lịch sử chi tiết các đợt 22–24/11 đã dời sang `VIEC_DA_XONG.md` và vẫn còn nguyên trong git (`git show a8ca8758:session_prompt/VIEC_DANG_MO.md`). Quyết định còn hiệu lực: `HIEN_TRANG.md` mục 4. Ý chưa thử: `Y_CHUA_THU.md` (tới ý 100). Việc xong ⇒ dời một dòng sang `VIEC_DA_XONG.md` rồi xoá khỏi đây.

## A. VIỆC CHÍNH HIỆN NAY (từ 25/11/2026 — chủ dự án đã chốt gói việc chiều 25/11; chuẩn bị chạy `/swarm` với `b`, `c`, `e`, `d`)

### 1. Chờ chủ dự án xem / chọn (mỗi lần MỘT câu, theo thứ tự ở `HIEN_TRANG.md` mục 3)
1. **Chủ dự án tự test lại khi muốn (KHÔNG giục) ⇒ Thuê GPU + huấn luyện model nhận ảnh** (`data/anh_huan_luyen_2026-11-24/goi_may_thue.tar` 3,3 GB, 93 lớp; chi tiết máy & quy trình SSH ở `HIEN_TRANG.md` mục 3 điểm 1 và `sessions/STATUS_E.md`).
2. **Bốn bài kho chưa có giờ mở cửa** (Chùa Thiên Mụ, Hổ Quyền, Đàn Xã Tắc, Suối Voi): chờ kết quả AI ngoài nếu chủ dự án gửi `gửi chatgpt/2026-11-24/tìm thông tin/gio_mo_cua_sau_noi.md` (có URL về ⇒ mở từng URL kiểm rồi mới ghi).

### 2. Việc đang mở (làm ngay khi bật `/swarm`, chia file không chồng nhau)
| Ai | Việc đang mở | Xong khi / Hồ sơ |
|---|---|---|
| **B** | **1. Phần backend cho 2 bản thử đã duyệt:** (a) Trên nhánh hoàn thiện `thu-b-hoan-tac`: kiểm & hoàn thiện phần backend cho mở `sua_lich_hoan_tac: true` ở máy demo (`settings.yaml`, `CO_SUA_LICH_TAT` ở `test_b5_lich_trinh.py`, 2 file test so nguyên danh sách `/api/tinh_nang`, hàng runbook 10.2); (b) Thêm công tắc `chu_de_trang_chu: true` ở backend (tự tắt/ẩn ở bản deploy khi `ho_so_chu_de` tắt); (c) Sửa kèm nợ nhỏ D nêu nếu chạm cùng file (`so_tay.py:19-20`, `full_corpus_prompt.py`, `routes/ho_so.py`, `settings.yaml`, hàng runbook 10 khối an toàn).<br>**2. Review chéo:** đọc nhánh 4 việc nhỏ `deploy/` của C. | File test chạm đạt, review chéo của E đạt, sẵn sàng gộp vào `main` |
| **C** | **1. Hoàn thiện giao diện 2 bản thử đã duyệt:** (a) Sửa ~3 dòng dải đầu cột lịch ở `frontend/src/LenKeHoach.jsx` trên `thu-c-hoan-tac` (không in lặp "Đã sửa theo lời bạn: Đã hoàn tác…"); (b) Đổi tiêu đề 5 ô `"Khám phá theo chủ đề"` ⇒ `"Khám phá theo lĩnh vực"` ở `frontend/src/TrangChu.jsx` trên `thu-c-trang-chu-chu-de`; (c) Sau khi ghép với phần backend của B, dựng `frontend/dist` tạm và chạy 1 lượt thật kiểm Hoàn tác (390 px, trang Trợ lý đầy đủ, lệnh thêm / dời / tối) + nhìn lại Dải Trang chủ (1536 & 390 px).<br>**2. Làm 4 việc nhỏ bộ `deploy/`** (`CACH_DEPLOY.md` mục 4 điểm 1–4): (1) `deploy/docker/Dockerfile` + `compose.yml` bó quyền người dùng thường, `cap_drop: [ALL]`, `no-new-privileges` (kiểm log/cache không lỗi quyền ghi); (2) ghi nhắc loại `/api/so_tay`, `/api/ho_so` khỏi nén Caddy khi bật deploy; (3) thêm phép kiểm giả `X-Forwarded-For` vào `deploy/guides/5_kiem_tra.md`; (4) thêm đoạn "Vì sao không làm CI/CD tự động" vào `deploy/README.md`. | Đủ ảnh/log lượt thật + diff sạch, qua review chéo |
| **E** | **1. Review chéo độc lập** code Hoàn tác (lõi B + giao diện C) và Dải Trang chủ (lõi B + giao diện C).<br>**2. Chạy kiểm cuối đợt:** test chạm + **1 lượt cả bộ test** trên `main` khi code đã đứng yên sau khi gộp 2 tính năng mới (đúng luật §8, không nạp env, từng file).<br>**3. Nợ trước deploy (ĐỨNG CHỜ — chỉ chạy sau buổi chủ dự án tự test, hỏi tiền trước):** ô 41 câu khó 1 bên + 1 lượt thật ngắn trên `gpt-6-luna`. | Biên bản review đạt + bảng test `main` 0 đỏ |
| **D** | **1. Giáo trình — việc nhỏ cũ:** thêm 1 hàng "thử rồi bỏ" ở bài 23 "Đã so" + `PL_C` cho phép đo công cụ đọc tiếp & đường 2m (`b_mo_doc_tiep/KET_QUA.md`).<br>**2. Đọc chéo** diff vòng cải tiến cách làm 24/11 + tổng kết đợt thử 3 ngày của A.<br>**3. Giáo trình cho 2 tính năng mới:** sau khi Hoàn tác + Dải Trang chủ gộp vào `main`, nhận phiếu 4 ý từ A để cập nhật bài liên quan + `00_GIAO_TRINH.md` (kèm 1 người kiểm đối chiếu số). | Nhánh giáo trình đạt đối chiếu, sẵn gộp `main` |
| **A** | **1. Vòng cải tiến cách làm 24/11 + tổng kết đợt thử 3 ngày (21–23/11):** xét 6 bẫy tối+đêm 24/11 và 3 con số ở `SO_CAI_TIEN_CACH_LAM.md`, ra ≤ 3 thay đổi + đóng đợt thử (nhờ D đọc diff).<br>**2. Điều phối `/swarm`:** bật Qdrant (`docker compose up -d qdrant`, kiểm đủ 9.536 điểm) trước khi chạy việc server/chỉ mục; sinh `b`, `c`, `e`, `d`; gộp nhánh đạt review vào `main`; dựng lại `frontend/dist` cây chính và báo chủ dự án theo khuôn "xong". | `SO_CAI_TIEN_CACH_LAM.md` cập nhật + các nhánh đợt 25/11 đã gộp sạch vào `main` |

### 3. Cách đo & Liều test đang áp dụng (chủ dự án 22:48 21/11 + 16:19 23/11)
- Mỗi thay đổi = ca của hành vi mới (đỏ trước khi sửa) + file test CHẠM đường code đổi; cả bộ test nhiều nhất MỘT lượt mỗi ngày lúc code đứng yên (không chạy lại bảng "file đọc cấu hình" cho từng công tắc).
- Trước khi mở thứ người dùng thấy: MỘT lượt "dùng như người thật" (Playwright MCP hoặc script Playwright Python) cho mỗi CỤM tính năng, đọc chữ đối chiếu kho; phép đếm lưới 0 đồng một lần trên bản cuối khi quyết một lựa chọn; 1 người đọc code mỗi nhánh.
- Trước một lượt có phí phải ghi "ra A làm gì, ra B làm gì"; trước khi đổi kho / chỉ mục thật báo A kiểm làn máy (không đụng cùng lúc với việc nặng).

### 4. Danh sách nhánh đang giữ trên `origin`
- **Đã duyệt gộp — đang hoàn thiện + kiểm chéo:** `origin/thu-b-hoan-tac`, `origin/thu-c-hoan-tac`, `origin/thu-c-trang-chu-chu-de`.
- **Hồ sơ giữ nguyên, KHÔNG gộp:** `origin/thu-b-mo-doc-tiep`, `origin/thu-b-ba-duong-tim`, `origin/thu-b-dem-loi-dan`, `origin/thu-c-khung-truoc`, `origin/p9-b-dem-y-go-tat-2`, `origin/p9-c-ve-loi-nho`, `origin/p9-c-sua-2-het-vong`, `origin/p9-b-vong-cuoi-chu-2`, `origin/p9-c-lich-tien-ve`, `origin/p9-c-s09-luu-y-an-toan`, `origin/p9-e-chi-sang-len-ke-hoach`.
- **Đã gộp vào `main` (chờ chủ dự án duyệt `!` khi muốn xoá):** các nhánh đã gộp thuộc nhóm `p9-*`, `p12-*`, `p13-*`, `p15-*`, `kho-*` (lọc bằng `git branch -r --merged origin/main`, trừ các nhánh hồ sơ giữ nguyên ở mục trên) cùng `thu-b-so-tay`, `thu-c-so-tay`, `thu-b-ho-so-chu-de`, `thu-c-ho-so-chu-de`.

## B. Đổi TẠM model viết sang Claude Sonnet 5.5 trên Amazon Bedrock (chủ dự án chốt 09:41 21/11/2026) — ĐANG CHẠY ở máy demo
- Đường về `gpt-6-luna` (OpenAI): sửa 1 dòng `provider: bedrock` ⇒ `openai` trong `backend/config/settings.yaml` (`guides/DOI_MODEL_VIET.md`), chỉ đổi khi chủ dự án nói "chuyển về luna".
- OpenAI đã nạp tiền lại từ 23/11 (trần 2–2,5 USD, đã dùng 0,66 USD ở đo bù 23/11); bản deploy sẽ dùng `openai` (`HIEN_TRANG.md` mục 4).

## C. Đợt hoàn thiện Phase 9–12 (phạm vi "xong ở local")
- 19 / 21 mục của bảng kiểm kê (`data/kiem_ke_phase_2026-11-20/`) đã xong ở local hoặc đóng bằng giới hạn. Còn lại:
  - **[10]** So sánh cuối trên **bộ câu kín** — chạy MỘT lần SAU buổi chủ dự án tự test và các bản sửa của buổi đó; chỉ chủ dự án gõ lệnh (`data/test_cuoi/DANH_SACH.md` phần C); báo ước tiền OpenAI cho bên "RAG mốc" trước khi chạy.
  - **[13]** **Deploy AWS** — chỉ làm nếu chủ dự án muốn sau khi xong test ở máy; các chốt trước deploy ở local đã xong, phần hạ tầng chuẩn bị ở `deploy/` (`b0932fdc`).

## D. Buổi chủ dự án test ở máy local
- Chủ dự án đã test đợt 1 tối 23/11 (`data/test_cuoi/TEST_TOI_2311.md`, bỏ 2C) và vẫn cần test lại sản phẩm (bao gồm các bản sửa 24/11 và `so_tay`, `ho_so_chu_de`) — KHÔNG giục.
- Hướng dẫn hiện hành: `data/test_cuoi/TEST_2411_TRUA.md` (cộng mục 4, 5 cho sổ tay và hồ sơ). Phần nhóm chưa chạy thay được: file `.ics` trên điện thoại, bấm in tay, điện thoại thật.

## E. Phiên D viết GIÁO TRÌNH `bai_hoc/giao_trinh/`
- Đủ **44 bài + 9 phụ lục + mục lục** ở `main` (`ff459ed7`), khớp trạng thái 61 mở / 6 tắt và kho 269 bài / 9.536 đoạn.
- Việc kế của D: ghi ở bảng mục A.2 trên (1 hàng "thử rồi bỏ" ở bài 23 + `PL_C`, rồi cập nhật giáo trình cho nút Hoàn tác + Dải Trang chủ sau khi gộp `main`). Chờ phiếu 4 ý sau khi có kết quả thật mới viết tiếp: model nhận ảnh thuê GPU, deploy (bài 36).

## F. Bộ bài đánh giá coding agent (`data/danh_gia_model_2026-11-20/`) — DỪNG ở khung, CHƯA có đề nào
- Giữ nguyên khung `KHUNG.md`, `KHUON_MO_DAU.md`; không tự soạn đề khi chủ dự án chưa mở lại (`WORKFLOW.md` / quyết định 20/11).

## G. Việc nhỏ chưa đo từ các đợt trước (chỉ ghi nhận, không tự mở khi chủ dự án chưa nêu)
- Chưa thử trên đường model cũ (`gpt-6-luna`): tin dài 4 ý, cụm sửa lịch 24/11, nút "Vì sao", sổ tay, hồ sơ theo chủ đề, điện thoại qua trình duyệt.
- Các bản sửa 20–22/11 còn thiếu lượt thật phụ: thẻ chọn sửa lịch qua trình duyệt (nay đã có ở đợt mức 1), 2 bản sửa link trong dòng nhắc, chuỗi "hỏi A ⇒ hỏi B ⇒ gõ lại A" (`nho_ten_goi_y`), bản sửa hẹp `950bb55`.
