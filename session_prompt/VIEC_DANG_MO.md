# VIỆC ĐANG MỞ — mục lục theo việc (sống xuyên ngày; GHI ĐÈ tại chỗ)

Cập nhật: 11:26 19/11/2026 (giờ `date`). Người giữ: phiên điều phối. **[đang thử từ 19/11, xét lại sau 3 ngày làm việc]**

Trang này là gì: mỗi việc kéo quá một ngày có MỘT khối ở đây, để phiên mở sáng hôm sau tìm lại đủ hồ sơ mà không lục từng thư mục ngày. Việc xong ⇒ dời MỘT dòng sang `session_prompt/VIEC_DA_XONG.md` (tên · ngày xong · sha gộp · các thư mục ngày có hồ sơ) rồi xoá khối. Trần: 8 việc / 60 dòng. **"Bước kế" của một việc CHỈ ghi ở trang này** — trang hiện trạng, `TONG_HOP.md` của ngày và `STATUS_<X>.md` chỉ trỏ tới đây, không chép lại. Dòng "plan" luôn là bản HIỆN HÀNH + sha đã duyệt; bản plan cũ có dòng đầu "đã thay bởi …". Report đã nằm ở thư mục ngày nào thì KHÔNG dời; bản cập nhật ngày sau là file MỚI ở thư mục ngày mới, dòng "report" liệt kê đủ theo ngày. Dữ liệu riêng tư ở `data/<tên việc>/` (không vào git) — ở đây chỉ ghi đường dẫn.

## 1. Thí nghiệm mức suy luận low · medium · high (User giao 19/11)
- Trạng thái: plan đã duyệt, công cụ sẵn + chạy khô, CHƯA chạy lượt có phí nào. Ai: E đặt tiêu chí · B chạy · C đọc tay.
- Plan + sha duyệt: `data/phase_9/muc_suy_luan/PLAN.md` bản `eb0a43776125` (A duyệt 19/11; danh sách 45 câu bậc 1 ở plan dòng 35–36). "medium" = KHÔNG gửi tham số (nhánh gửi tường minh chỉ để kiểm 10 câu).
- Không có nhánh code — chỉ công cụ riêng tư `data/phase_9/muc_suy_luan/tools/`, chạy theo thứ tự: `chup_muc.py` ⇒ `chay_xen_ke.py` ⇒ `an_toan_muc.py` ⇒ `in_gia.py`; `ba_muc.py` cho bậc 2. Kết quả ra `data/phase_9/muc_suy_luan/bac_1/` (sẽ tạo).
- Bước kế: B chạy bậc 1 trên `main` ≥ `55d01a8` (trần bậc 1 = 0,25 USD; trần cứng cả việc 1,2 USD); lệnh từng bước + điều kiện dừng: `report_agent/2026-11-19/b_nhat_ky.md` mục "Việc ĐANG DỞ". Xong DỪNG, báo A số thật ⇒ A báo User ⇒ bậc 2.
- Không được: chạy khi máy đang trong khung đo giây của dự án khác; so với điểm sáng 19/11 (chỉ so với medium chạy lại cùng buổi); nới hạn giờ 45 s.
- Report: chưa có. Review / đọc tay: chưa có.

## 2. Hướng "việc phổ thông của người dùng thật" (User giao 19/11)
- Trạng thái: **User CHỐT thứ tự 11:07 19/11/2026** — (1) bộ kịch bản phổ thông từ câu người thật + đo hiện trạng ⇒ (2) câu xin danh sách trả thiếu mục + hỏi tiếp đúng thứ vừa gợi ý ⇒ (3) gợi ý quán / chỗ ở theo tiêu chí + "gần X" bằng bảng 468 quán có toạ độ ⇒ (4) hiện ngày của nguồn cho giá vé / giờ mở ⇒ (5) ngân sách do code tính (bắt đầu từ tổng tiền vé của lịch) ⇒ (6) "mang lịch đi" + "làm thay" ở mức soạn sẵn tin + link người dùng tự bấm. Song song: việc 1 và việc 3 của trang này.
- Hồ sơ: ba bản liệt kê của B / C / E (tin nhắn 19/11, ý chính ở sổ việc) · tra cứu công khai `data/tra_cuu_cli/2026-11-19_viec-pho-thong-tro-ly-du-lich/` · đề bài + bốn bản tư vấn model khác hãng `gửi chatgpt/2026-11-19/` · bảng đối chiếu `data/tu_van_khac_hang_2026-11-19/DOI_CHIEU.md` · file User điền câu thật `data/kich_ban_pho_thong_2026-11-19/CAU_CUA_USER.md`.
- Bước kế (bước 1): E đã soạn xong bản đầu — plan `data/kich_ban_pho_thong_2026-11-19/PLAN.md` bản `b16eb85e65e6` + bộ `bo_kich_ban.jsonl` bản `6a8db610054e` (80 kịch bản / 106 lượt; B đã đọc phần tiền + công cụ; trạng thái đủ ở `README.md` cùng thư mục) — **A DUYỆT 11:26 19/11/2026 đúng hai sha này** (plan nhỏ, đo hiện trạng, không sàn đạt / trượt; A tự kiểm: 80 kịch bản / 106 lượt, nhóm 28 · 24 · 20 · 8, 2 ca hiếm, 0 câu bão / lũ / khẩn cấp) ⇒ A báo User ước tiền (0,10–0,25 USD, trần dừng 0,40), xếp lượt máy SAU bậc 1 của việc 1; B soạn sẵn bản sao công cụ chạy (~10 dòng, 0 USD); B + C chấm, E phân xử. User điền ~20 câu thật vào `CAU_CUA_USER.md` (không gấp; có thì thay vào kịch bản E tự viết).
- Việc lẻ đã rời trang hiện trạng, CHƯA ai nhận (xét khi tới bước tương ứng, không mở riêng): câu ngoài kho trả lời sai khuôn từ chối · lỗi tìm "quán gần một nơi" (thuộc bước 3) · câu tụt "Đủ ý" (thuộc bước 2) · runbook mục 8 (deploy).
- Không được: mở thêm việc bão / lũ / khẩn cấp; sửa nội dung kho, đổi quyết định "không nói giá phòng", nhận vị trí người dùng, gửi thư từ server khi User chưa chọn; đặt sàn "0 câu" cho bộ phổ thông.

## 3. Đưa ngữ cảnh lớn hơn vào model (User hỏi 19/11)
- Trạng thái: chưa bắt đầu; xếp SAU việc 1 (mỗi lần đổi một thứ). Ai: chưa giao.
- Hồ sơ: cách một dự án khác của User làm `data/ngu_canh_nho_lon_2026-11-19/` · lần thử cũ 25/10 ở `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` mục N2-02 (kém hơn vì ngân sách chặt + mở rộng theo thứ hạng) · bảng giới hạn `data/kiem_ke_gioi_han_2026-11-19/BANG_GIOI_HAN.md`.
- Bước kế: plan 1 trang — tìm đoạn nhỏ ⇒ gom theo mục / bài ⇒ khử trùng ⇒ đưa N đơn vị khác nhau, so với 10 đoạn; và biến thể 15 đoạn (đếm 0 USD trước).

## 4. Cách làm việc theo thư mục từng ngày (User giao 19/11) [đang thử]
- Trạng thái: đã có `report_agent/2026-11-19/` + trang này. Ai: A; C viết script kiểm; E sửa `guides/CACH_LAM_VIEC.md` + `guides/khung/`.
- Hồ sơ: câu trả lời của hai dự án khác `data/cach_lam_theo_ngay_2026-11-19/`; chốt của A ở `session_prompt/CURRENT_HANDOFF.md` khối 19/11.
- Bước kế (lúc KẾT PHIÊN 19/11, không làm giữa chừng): mỗi phiên GHI ĐÈ mục đầu `STATUS_<X>.md` theo khuôn mới; A cắt `CURRENT_HANDOFF.md` còn khối trỏ (bản cũ nguyên văn sang `archive/`, `cmp`); trang hiện trạng mục 2 chỉ còn bảng bước + dòng trỏ trang này; `scripts/mo_ngay.sh`. Ghi hai con số của ngày + số dòng mỗi phiên đọc lúc mở để so sau 3 ngày.
