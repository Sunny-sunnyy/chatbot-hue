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

- `do_bieu_mau.py` (md5 `4de78cb35999`; bản trước `b07002c6e173` — 07/11 thêm số theo dõi `cat_ngay_cuoi`): `kiem` 0 USD — luật phủ + `lich_trinh.xep` thật với nút (12 / 12 khung 0 lỗi, tham số = nút) + 9 / 9 ca phá bắt [Chạy]; `chay` CÓ PHÍ — `TestClient(create_app(<bản sao settings bật lich_trinh_bieu_mau>))`, đường `/api/chat/stream`, mỗi tổ hợp một cuộc mới, bọc `_remember` (hàm thật vẫn chạy) giữ khung + chữ model + mã kiểm cuối; `cham` sàn code; `phieu` / `gop` cho F-a [Chạy trên dòng giả].
- **Còn khớp với S1** trước lượt có phí: khuôn body biểu mẫu (`body_bieu_mau` — đang GIẢ ĐỊNH `bieu_mau: true` + `truong`), tên cờ, đường biểu mẫu vẫn qua `_remember`. Khớp xong ⇒ chạy lại `kiem` + 1 lượt thử (pilot 1 tổ hợp) rồi mới chạy ×2.

**Ghi nhận từ E (review S4, 07/11):** 3 / 120 tổ hợp biểu mẫu (4+ ngày · ẩm thực · một mình / cặp đôi / nhóm bạn) bị bớt ngày cuối vì vượt ngân sách ngữ cảnh (`vuot_ngan_sach`, có cả trước `0cb0b0a`). Bộ quyết 12 không có tổ hợp này (F12 = 4+ · cặp đôi · lễ hội nghệ thuật). Lưu ý: `kiem_khung` **coi ngày cắt là hợp lệ** (`lich_trinh.py:310-311` cộng ngày `vuot_ngan_sach` vào số ngày) ⇒ sàn code không bắt; harness S3 sẽ đếm riêng số lượt có `vuot_ngan_sach` (theo dõi, không quyết).

## 3. Dữ kiện đi kèm (đã báo A, dùng cho Q-U3)

[Chạy] `kieu_di` thong_tha / day_lich / không chọn ⇒ khung giống hệt nhau ở **0 / 120** tổ hợp (`so_ngay` 4 × `di_cung` 5 × `so_thich` 6, bảng `diem_v3.json`) — chọn "đi dày" hiện không đổi gì.

## 4. Q-G + Q-N cho bản S2 `f20fd28` — ghi trước (12:53 07/11/2026; chạy SAU X1c)

Tiêu chí chép spec §6 (không đổi); dưới đây chỉ ghi **cách đo** cố định trước:
- **Nền:** worktree tách `f20fd28`, `cd frontend && npm ci && npm run build`, FastAPI phục vụ bản build (`uvicorn api.app:app` cổng trống) — không `vite dev`. Cờ như `settings.yaml` của nhánh (biểu mẫu tắt ⇒ "Lên kế hoạch" là đích theo cờ, không tính vào 7 / 7).
- **Q-G đích + CSP** — `data/phase_9/cong_dot_1/tools/playwright_cong.py` md5 `fa580e39f5ed`, ở 1440 và 390: 7 / 7 đích (trợ lý · 5 trang lĩnh vực `#/kham-pha/<tên thư mục kho>` · giới thiệu) tới được trong ≤ 2 lần bấm từ `#/` (link `#…` đang hiện, hoặc mở menu `aria-expanded` rồi theo link); mỗi trang mở thẳng + tải lại giữ hash và có `h1`; 0 lỗi CSP; 0 lỗi console / `pageerror`; bundle JS gzip ≤ 200 KB. Hash khớp `frontend/src/route.js` của `f20fd28` (C đã đọc).
- **Q-G tương phản** — `tools/tuong_phan.py` md5 `f53a31153ce3`: mọi cặp chữ / nền trên trang đã dựng (mặc định + `:hover` + `::placeholder`) ở 7 trang × 1440 / 390 ≥ 4,5 : 1; chữ trên ảnh / SVG / gradient liệt kê để đọc mắt.
- **Q-N** — `tools/qn_nguon.py` md5 `1aab1db65b88` trên 10 câu C tự viết (`data/phase_9/cong_dot_1/qn/cau_qn.txt` md5 `a6a4b6df98e7`; loại câu: nguồn gốc món, năm xây dựng, thời gian lễ hội, công nhận di sản, giá vé, vị trí, món ăn kèm, nơi biểu diễn, đặc điểm điểm đến, tháng lễ hội; quét trùng Golden / kho / kín bằng `.githooks/overlap_scan.py`: 0 trùng): mỗi câu một cuộc mới ở `#/tro-ly`; đạt khi **10 / 10** câu có nguồn **và** chữ hiện ra 0 `[n]` / `[Nguồn n]` **và** tập tên dòng "Nguồn" = tập `title` của sự kiện SSE `sources` cùng lượt. Câu không có nguồn (từ chối) ⇒ không tính, báo A để thay câu (không tự đổi). Có phí ≈ 10 lượt chat (~0,005 USD) — trong trần cả spec.

## 5. Kết quả

NOT RUN.
