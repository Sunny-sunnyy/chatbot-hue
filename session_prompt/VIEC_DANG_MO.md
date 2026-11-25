# VIỆC ĐANG MỞ — sổ việc hue_rag

Cập nhật: 14:03 25/11/2026 (giờ `date`; phiên điều phối viết gọn toàn sổ sau khi chuyển sang `agy` CLI + `/swarm` `a8ca8758`). Người giữ: phiên điều phối (A).

**Sổ việc = trang này:** chỉ giữ việc đang mở, câu chờ chủ dự án, nhánh thử còn giữ và nợ còn sống. Lịch sử chi tiết các đợt 22–24/11 đã dời sang `VIEC_DA_XONG.md` và vẫn còn nguyên trong git (`git show a8ca8758:session_prompt/VIEC_DANG_MO.md`). Quyết định còn hiệu lực: `HIEN_TRANG.md` mục 4. Ý chưa thử: `Y_CHUA_THU.md` (tới ý 100). Việc xong ⇒ dời một dòng sang `VIEC_DA_XONG.md` rồi xoá khỏi đây.

## A. VIỆC CHÍNH HIỆN NAY (từ 25/11/2026 — máy demo đã mở 61 tính năng gồm `so_tay` và `ho_so_chu_de`; nhóm chạy bằng `agy` CLI + `/swarm`)

### 1. Chờ chủ dự án xem / chọn (mỗi lần MỘT câu, theo thứ tự ở `HIEN_TRANG.md` mục 3)
1. **Báo gọn kết quả đêm 24 ⇒ 25/11** (`so_tay` + `ho_so_chu_de` đã mở ở máy demo, cách thử `data/test_cuoi/TEST_2411_TRUA.md` mục 4–5, bản sửa cảnh báo an toàn, cả bộ test 2.391 ca / 0 đỏ, vị trí hồ sơ ở Khám phá).
2. **Hai bản thử ở nhánh riêng (xem ảnh ⇒ hỏi gộp + mở từng cái):**
   - Nút **"Hoàn tác lần sửa này"**: lõi `origin/thu-b-hoan-tac` `34af509` + giao diện `origin/thu-c-hoan-tac` `ae54841`; lượt thật chung đạt (6.209 / 6.209 lưới, 0,1 s hoàn tác, 409 khi cũ); ảnh `data/x15_phan_ai_2026-11-23/c_ho_so/luot_that_hoan_tac/`. Nếu chọn gộp: sửa nhẹ ~3 dòng dải đầu cột lịch ở `LenKeHoach.jsx`, thử thêm 390 px, lệnh thêm/dời/tối và model cũ.
   - **Dải chủ đề ở Trang chủ**: `origin/thu-c-trang-chu-chu-de` `b7794fe` (cần B thêm công tắc `chu_de_trang_chu` nếu mở); ảnh `data/x15_phan_ai_2026-11-23/c_ho_so/anh_trang_chu/`. Kèm câu hỏi: đổi tiêu đề 5 ô lĩnh vực ở Trang chủ "Khám phá theo chủ đề" ⇒ "Khám phá theo lĩnh vực"?
3. **Kết quả đọc sâu 25 repo ngoài** (`data/x22_doc_repo_2026-11-24/TOM_TAT.md`, `TINH_NANG_DANG_THEM.md`, `CACH_DEPLOY.md`, đề bài AI khác hãng `DE_BAI_3.md`): chọn ứng viên dựng tiếp trong 6 ý chưa dựng (dòng "đã đổi gì" · ô "Để dành" · phương án khi mưa · khối "Sổ tay đã ghi được gì" · bản đồ ghim · bản in có công tắc) và 5 việc nhỏ của bộ deploy.
4. **Chủ dự án tự test lại khi muốn (KHÔNG giục) ⇒ Thuê GPU + huấn luyện model nhận ảnh** (`data/anh_huan_luyen_2026-11-24/goi_may_thue.tar` 3,3 GB, 93 lớp; chi tiết máy & quy trình SSH ở `HIEN_TRANG.md` mục 3 điểm 4 và `sessions/STATUS_E.md`).
5. **Bốn bài kho chưa có giờ mở cửa** (Chùa Thiên Mụ, Hổ Quyền, Đàn Xã Tắc, Suối Voi): chờ kết quả AI ngoài nếu chủ dự án gửi `gửi chatgpt/2026-11-24/tìm thông tin/gio_mo_cua_sau_noi.md` (có URL về ⇒ mở từng URL kiểm rồi mới ghi).

### 2. Việc nội bộ còn mở (không chờ chủ dự án, làm theo bảng quyền)
| Ai | Việc đang mở | Xong khi / Hồ sơ |
|---|---|---|
| **A** (cần 1 phiên khác đọc) | **Vòng cải tiến cách làm ngày 24/11 + tổng kết đợt thử 3 ngày (21–23/11):** xét 6 bẫy tối+đêm 24/11 (`STATUS_A.md` mục 5) và 3 con số cách làm ở `SO_CAI_TIEN_CACH_LAM.md`, ra ≤ 3 thay đổi (nếu đủ điều kiện lặp lần 2) và đóng đợt thử | Đã cập nhật `SO_CAI_TIEN_CACH_LAM.md`, một phiên khác đọc diff |
| **D** | **Giáo trình — 1 việc nhỏ:** thêm 1 hàng "thử rồi bỏ" ở bài 23 "Đã so" + `PL_C` cho phép đo công cụ đọc tiếp & đường 2m (`data/x15_phan_ai_2026-11-23/b_mo_doc_tiep/KET_QUA.md`); một người kiểm đối chiếu số trước khi gộp | Đẩy nhánh `p9-d-giao-trinh` + phiên khác đối chiếu số |
| **B** *(làm kèm khi chạm file)* | Sửa nợ nhỏ D nêu ở bài 44 / 43: 3 chú thích cũ (`full_corpus_prompt.py` gọi hai tính năng là "bản thử", `routes/ho_so.py` "5–9 lời gọi" ↔ 3–9, `so_tay.py:19-20` câu cũ về Thác Nhị Hồ); chú thích cũ ở `backend/config/settings.yaml`; hàng runbook 10 về khối "Lưu ý an toàn" hồ sơ (đã nhìn 23:28); nếu chạm bộ đệm hồ sơ: lưu ý ca `kiem_dan_y` tự chia dàn ý hỏng | Khi có việc chạm các file đó |
| **E** *(sau buổi tự test, hỏi tiền trước)* | **Nợ trước deploy** (chỉ chạy MỘT lần trên bản deploy đứng yên, đường OpenAI `gpt-6-luna`, trong phần còn lại của trần 2–2,5 USD — đã dùng 0,66 USD ở đo bù 23/11): ô 41 câu khó 1 bên (ngưỡng ≤ 3 lệch so với 37/41) + 1 lượt thật ngắn cụm sửa lịch mức 1 và "Vì sao" | Đủ báo cáo trước khi đóng gói deploy |

### 3. Cách đo & Liều test đang áp dụng (chủ dự án 22:48 21/11 + 16:19 23/11)
- Mỗi thay đổi = ca của hành vi mới (đỏ trước khi sửa) + file test CHẠM đường code đổi; cả bộ test nhiều nhất MỘT lượt mỗi ngày lúc code đứng yên (không chạy lại bảng "file đọc cấu hình" cho từng công tắc).
- Trước khi mở thứ người dùng thấy: MỘT lượt "dùng như người thật" (Playwright MCP hoặc script Playwright Python) cho mỗi CỤM tính năng, đọc chữ đối chiếu kho; phép đếm lưới 0 đồng một lần trên bản cuối khi quyết một lựa chọn; 1 người đọc code mỗi nhánh.
- Trước một lượt có phí phải ghi "ra A làm gì, ra B làm gì"; trước khi đổi kho / chỉ mục thật báo A kiểm làn máy (không đụng cùng lúc với việc nặng).

### 4. Danh sách nhánh đang giữ trên `origin`
- **Chờ chủ dự án chọn:** `origin/thu-b-hoan-tac`, `origin/thu-c-hoan-tac`, `origin/thu-c-trang-chu-chu-de`.
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
- Việc nhỏ kế của D: ghi ở bảng mục A.2 trên (1 hàng "thử rồi bỏ" ở bài 23 + `PL_C`). Chờ phiếu 4 ý sau khi có kết quả thật mới viết tiếp: model nhận ảnh thuê GPU, deploy (bài 36), tính năng mới nếu chủ dự án chọn.

## F. Bộ bài đánh giá coding agent (`data/danh_gia_model_2026-11-20/`) — DỪNG ở khung, CHƯA có đề nào
- Giữ nguyên khung `KHUNG.md`, `KHUON_MO_DAU.md`; không tự soạn đề khi chủ dự án chưa mở lại (`WORKFLOW.md` / quyết định 20/11).

## G. Việc nhỏ chưa đo từ các đợt trước (chỉ ghi nhận, không tự mở khi chủ dự án chưa nêu)
- Chưa thử trên đường model cũ (`gpt-6-luna`): tin dài 4 ý, cụm sửa lịch 24/11, nút "Vì sao", sổ tay, hồ sơ theo chủ đề, điện thoại qua trình duyệt.
- Các bản sửa 20–22/11 còn thiếu lượt thật phụ: thẻ chọn sửa lịch qua trình duyệt (nay đã có ở đợt mức 1), 2 bản sửa link trong dòng nhắc, chuỗi "hỏi A ⇒ hỏi B ⇒ gõ lại A" (`nho_ten_goi_y`), bản sửa hẹp `950bb55`.
