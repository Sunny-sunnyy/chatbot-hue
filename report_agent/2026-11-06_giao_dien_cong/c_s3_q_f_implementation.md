# S3 — đo Q-F biểu mẫu "Lên kế hoạch" (C)

Spec cổng đợt 1 bản 2 `ff3c317ec88b` §6 Q-F. Trạng thái: **ghi trước xong, CHƯA CHẠY lượt có phí** (chờ B xong S1 trên `p11-cong-dot-1`, gồm sửa lỗi model từ chối ở lượt biểu mẫu).

## 1. Ghi trước (12:23 07/11/2026, trước mọi lượt có phí)

**Q-U3 (User):** ẩn "đi dày" ở đợt 1 ⇒ biểu mẫu không gửi `kieu_di` (mọi tổ hợp `kieu_di` = không chọn).

**Bộ 12 tổ hợp chính thức** — file private `data/phase_9/cong_dot_1/to_hop_chinh_thuc.jsonl` md5 `792a3cbe3fe5` (= bản nháp `to_hop_nhap_an_di_day.jsonl`, không đổi):

| id | so_ngay | di_cung | so_thich |
|---|---|---|---|
| F01 | 1 | mot_minh | di_tich |
| F02 | 1 | gia_dinh_tre_em | — |
| F03 | 1 | nguoi_lon_tuoi | am_thuc |
| F04 | 1 | cap_doi | chup_anh |
| F05 | 2 | nhom_ban | am_thuc |
| F06 | 2 | cap_doi | thien_nhien |
| F07 | 2 | nguoi_lon_tuoi | — |
| F08 | 2 | mot_minh | le_hoi_nghe_thuat |
| F09 | 3 | gia_dinh_tre_em | di_tich |
| F10 | 3 | nhom_ban | — |
| F11 | 3 | mot_minh | thien_nhien |
| F12 | 4+ | cap_doi | le_hoi_nghe_thuat |

Luật phủ §6 (máy kiểm, `do_bieu_mau.py kiem`): đủ 5 `di_cung` (mot_minh 3, cap_doi 3, gia_dinh_tre_em 2, nguoi_lon_tuoi 2, nhom_ban 2) · `so_ngay` 1 / 2 / 3 = 4 / 4 / 3 lần (+ 1 lần 4+) · 9 có `so_thich` (đủ 5 giá trị) · 3 không chọn sở thích ⇒ **đạt**.

**Chạy ×2 = 24 lượt.** Tiêu chí (chép §6, không đổi):
- **Sàn code 24 / 24:** 0 lượt chữ model là câu từ chối thay lịch (code dựng lời thay ⇒ vẫn trượt, đếm riêng); `kiem_cuoi` 0 lỗi; 0 rút lại; khung 0 lỗi `kiem_khung`; tham số khung = giá trị nút; 0 thẻ hỏi lại; 0 công cụ ngoài `lich_trinh`. Lượt có ≠ 1 dòng `chat_metrics` sau mốc ⇒ "không đo được" (sàn không đạt).
- **F-a "lời khớp khung":** 2 sub-agent Claude ngữ cảnh mới, độc lập, mỗi lượt nhận khung + chữ model + giá trị nút; đạt khi **≥ 11 / 12 mỗi lần** theo cả hai, bất đồng ⇒ tính trượt.
- Trượt bất kỳ ⇒ cờ `lich_trinh_bieu_mau` tắt, biểu mẫu ẩn (phương án B §1).
- **Tiền:** script dừng khi tiền cả thư mục kết quả chạm 0,025 USD (trần 0,03 là của cả spec, gồm cổng ổn định). Dự phóng 24 × ~0,0006 ≈ 0,015.
- Theo dõi (không quyết): USD / lượt, latency tổng + tới chữ đầu p50 / p95, số lần gọi model / lượt.

## 2. Công cụ (private, `data/phase_9/cong_dot_1/tools/`)

- `do_bieu_mau.py` (md5 `b07002c6e173`): `kiem` 0 USD — luật phủ + `lich_trinh.xep` thật với nút (12 / 12 khung 0 lỗi, tham số = nút) + 9 / 9 ca phá bắt [Chạy]; `chay` CÓ PHÍ — `TestClient(create_app(<bản sao settings bật lich_trinh_bieu_mau>))`, đường `/api/chat/stream`, mỗi tổ hợp một cuộc mới, bọc `_remember` (hàm thật vẫn chạy) giữ khung + chữ model + mã kiểm cuối; `cham` sàn code; `phieu` / `gop` cho F-a [Chạy trên dòng giả].
- **Còn khớp với S1** trước lượt có phí: khuôn body biểu mẫu (`body_bieu_mau` — đang GIẢ ĐỊNH `bieu_mau: true` + `truong`), tên cờ, đường biểu mẫu vẫn qua `_remember`. Khớp xong ⇒ chạy lại `kiem` + 1 lượt thử (pilot 1 tổ hợp) rồi mới chạy ×2.

## 3. Dữ kiện đi kèm (đã báo A, dùng cho Q-U3)

[Chạy] `kieu_di` thong_tha / day_lich / không chọn ⇒ khung giống hệt nhau ở **0 / 120** tổ hợp (`so_ngay` 4 × `di_cung` 5 × `so_thich` 6, bảng `diem_v3.json`) — chọn "đi dày" hiện không đổi gì.

## 4. Kết quả

NOT RUN.
