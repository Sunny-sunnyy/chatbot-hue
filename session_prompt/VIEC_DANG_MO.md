# VIỆC ĐANG MỞ — mục lục theo việc (sống xuyên ngày; GHI ĐÈ tại chỗ)

Cập nhật: 11:01 19/11/2026 (giờ `date`). Người giữ: phiên điều phối. **[đang thử từ 19/11, xét lại sau 3 ngày làm việc]**

Trang này là gì: mỗi việc kéo quá một ngày có MỘT khối ở đây, để phiên mở sáng hôm sau tìm lại đủ hồ sơ mà không lục từng thư mục ngày. Việc xong ⇒ XOÁ khối (kết quả đã nằm ở `report_agent/<ngày>/`). Trần: 8 việc / 60 dòng. Report đã nằm ở thư mục ngày nào thì KHÔNG dời; bản cập nhật ngày sau là file MỚI ở thư mục ngày mới, dòng "report" liệt kê đủ theo ngày. Dữ liệu riêng tư ở `data/<tên việc>/` (không vào git) — ở đây chỉ ghi đường dẫn.

## 1. Thí nghiệm mức suy luận low · medium · high (User giao 19/11)
- Trạng thái: plan đã duyệt, công cụ sẵn, CHƯA chạy lượt có phí nào. Ai: E đặt tiêu chí · B chạy · C đọc tay.
- Plan + sha duyệt: `data/phase_9/muc_suy_luan/PLAN.md` bản `eb0a43776125` (A duyệt 19/11). Công cụ: `data/phase_9/muc_suy_luan/tools/`.
- Bước kế: B chạy bậc 1 (45 câu × 3 mức + câu theo dõi) trên `main` ≥ `55d01a8`; xong DỪNG, báo A số thật ⇒ A báo User ⇒ bậc 2. Trần cứng 1,2 USD.
- Không được: chạy khi máy đang trong khung đo giây của dự án khác; so với điểm sáng 19/11 (chỉ so với medium chạy lại cùng buổi); nới hạn giờ 45 s.
- Report: chưa có. Review / đọc tay: chưa có.

## 2. Hướng "việc phổ thông của người dùng thật" (User giao 19/11)
- Trạng thái: đang gom ý, CHƯA chốt thứ tự làm. Ai: A bàn với User từng câu; B (hỏi đáp + gợi ý), C (lịch + ngân sách), E (làm thay) đã gửi bản liệt kê.
- Hồ sơ: tra cứu công khai `data/tra_cuu_cli/2026-11-19_viec-pho-thong-tro-ly-du-lich/` · đề bài + kết quả tư vấn model khác hãng `gửi chatgpt/2026-11-19/` · bảng đối chiếu `data/tu_van_khac_hang_2026-11-19/DOI_CHIEU.md` (agent con của A đang lập).
- Bước kế: A gom ⇒ hỏi User (mức "làm thay" · giá phòng · bổ sung kho · vị trí người dùng · 20 câu User tự gõ) ⇒ dựng bộ kịch bản phổ thông ⇒ đo hiện trạng.
- Không được: mở thêm việc bão / lũ / khẩn cấp; sửa nội dung kho hay đổi quyết định "không nói giá phòng" khi User chưa chọn.

## 3. Đưa ngữ cảnh lớn hơn vào model (User hỏi 19/11)
- Trạng thái: chưa bắt đầu; xếp SAU việc 1 (mỗi lần đổi một thứ). Ai: chưa giao.
- Hồ sơ: cách một dự án khác của User làm `data/ngu_canh_nho_lon_2026-11-19/` · lần thử cũ 25/10 ở `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` mục N2-02 (kém hơn vì ngân sách chặt + mở rộng theo thứ hạng) · bảng giới hạn `data/kiem_ke_gioi_han_2026-11-19/BANG_GIOI_HAN.md`.
- Bước kế: plan 1 trang — tìm đoạn nhỏ ⇒ gom theo mục / bài ⇒ khử trùng ⇒ đưa N đơn vị khác nhau, so với 10 đoạn; và biến thể 15 đoạn (đếm 0 USD trước).

## 4. Cách làm việc theo thư mục từng ngày (User giao 19/11) [đang thử]
- Trạng thái: đã có `report_agent/2026-11-19/` + trang này. Ai: A; C viết script kiểm; E sửa `guides/CACH_LAM_VIEC.md` + `guides/khung/`.
- Hồ sơ: câu trả lời của hai dự án khác `data/cach_lam_theo_ngay_2026-11-19/`; chốt của A ở `session_prompt/CURRENT_HANDOFF.md` khối 19/11.
- Bước kế (lúc KẾT PHIÊN 19/11, không làm giữa chừng): mỗi phiên GHI ĐÈ mục đầu `STATUS_<X>.md` theo khuôn mới; A cắt `CURRENT_HANDOFF.md` còn khối trỏ (bản cũ nguyên văn sang `archive/`, `cmp`); trang hiện trạng mục 2 chỉ còn bảng bước + dòng trỏ trang này; `scripts/mo_ngay.sh`. Ghi hai con số của ngày + số dòng mỗi phiên đọc lúc mở để so sau 3 ngày.
