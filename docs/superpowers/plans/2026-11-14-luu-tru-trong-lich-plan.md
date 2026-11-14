# Plan (mức nhẹ) — Gợi ý nơi ở trong lịch bản 2 · B · 13:56 14/11/2026

A chốt 14/11 (User chọn theo đa số): khách sạn = (a) bài kho (E) + **(b) gợi ý trong lịch (B, việc này)**. Phiếu nhóm vòng 1 + ý Codex A gửi: mặc định **một khu cho cả chuyến**; lý do địa lý do code viết; không tạo "điểm chất lượng"; không giá. Dữ liệu: bảng của E `data/luu_tru_2026-11-14_lich/bang_luu_tru_lich.json` (md5 `a4c97df36c7c`, 140 cơ sở có hạng, khu 100 %, nguồn danh mục Sở + ngày) + `khu_cum_v1` của C (đã gói trong bảng).

**Người dùng thấy:** lịch từ 2 ngày có thẻ "Nơi ở gợi ý: khu <tên> — gần các điểm ngày 1–3", kèm 3–5 cơ sở. Mỗi cơ sở: tên · hạng · địa chỉ · link "tìm phòng" do code dựng. Nhãn cố định: "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống · danh mục <nguồn>, <ngày>".

## Luật (code; model không chọn, không viết tên)
1. **Khu cả chuyến:**
   - đếm điểm ban ngày của lịch theo khu (`cum_ve_khu`); mặc định **lõi đô thị**;
   - **phía tây** chỉ khi > 50 % điểm ở phía tây VÀ không có trẻ em / người lớn tuổi;
   - **ven biển** chỉ khi ≥ 60 % điểm ở ven biển (ngày ra biển / Bạch Mã thường là đi trong ngày — C, E nhắc).
   - Lịch 1 ngày ⇒ không có thẻ.
2. **Cơ sở trong khu:**
   - tối đa 5, trải theo hạng để khách tự chọn: tối đa 2 cơ sở 4–5 sao · 2 cơ sở 2–3 sao · 1 cơ sở 1 sao / đạt chuẩn;
   - trong cùng mức hạng: `cum_gan` trùng cụm có nhiều điểm nhất đứng trước, rồi theo tên (tất định).
   - Không xếp theo khoảng cách trong khu trung tâm (toạ độ chỉ ~1 km — E).
3. **Lý do** do code viết: "cùng khu với n / N điểm của lịch" hoặc "khu trung tâm — đi cùng trẻ em / người lớn tuổi".
4. **Link tìm phòng:** `https://www.booking.com/searchresults.html?ss=<tên + Huế>`, mã hoá bằng code (A chốt "Booking do code dựng"). Không link đặt chỗ, không giá.
5. **Dữ liệu:** `lich["o_dau"]` (chỗ đã có sẵn). **Không vào tin nhắn gửi model**; chữ chép / tải (`ghep_chu`) thêm một khối ngắn.
6. **Cờ** `luu_tru_lich` (TẮT, cần `len_ke_hoach_v2`) + `lich_trinh_bang_luu_tru`. Kiểm lúc khởi động: khu hợp lệ, mọi cụm của bảng điểm có trong `cum_ve_khu`, cơ sở có tên + hạng + nguồn.
7. **Giao diện:** thẻ "Nơi ở gợi ý" trong `LichV2`, cuối lịch. Hợp đồng dữ liệu `{khu, ten_khu, ly_do, co_so: [{ten, xep_hang, dia_chi, link}], nhan, nguon}`; báo E cách vẽ trong H1.

## Tiêu chí ghi trước
| Mã | Tiêu chí | Đo bằng | Tiền |
|---|---|---|---|
| Luôn | 3.840 khung: lịch ≥ 2 ngày có `o_dau` 100 %, 1 ngày 0 %; mọi cơ sở có trong bảng và đúng khu đã chọn; khu đúng luật (1) 100 %; 0 link ngoài mẫu Booking; ≤ 5 cơ sở; có nhãn "chưa kiểm giá" | mô phỏng 0 USD + test | 0 |
| Q1 | cờ tắt ⇒ chuỗi gửi model giống byte; cờ bật ⇒ tin nhắn viết câu của lịch giống byte (`o_dau` không vào) | test / capture | 0 |
| Người xem | agent con ngữ cảnh mới xem 10 lịch (bảng ghép: điểm theo ngày + khu + cơ sở): "khu ở hợp lý cho lịch này?" | ≥ 9 / 10 | 0 |
| UI | Playwright 1440 + 390: thẻ hiện, link mở tab mới, 0 lỗi console, 0 yêu cầu ra ngoài lúc tải (link chỉ mở khi bấm) | Playwright | ≈ 0,002 |

**Giờ:** ~0,5 ngày. **Không làm:** đổi khu giữa chuyến (ngưỡng ghi sau nếu User muốn); giá / phòng trống; điểm đánh giá Google (phương án (c) chưa chọn).

## Bảng AI FDE (agent-design-review + agent-security-review)
| Mục | Thiết kế | Khớp / lệch |
|---|---|---|
| Có cần model? | Không — chọn khu, chọn cơ sở, viết lý do, dựng link đều do code | khớp |
| Dữ liệu ngoài vào sản phẩm | Danh mục công khai của Sở (đã có nguồn + ngày), toạ độ ước OSM / dữ liệu mở; ghi nhãn ngày dữ liệu | khớp |
| Đường ra mới | Link Booking chỉ mở khi người dùng bấm (trình duyệt), không gọi từ server; không gửi chữ người dùng | khớp (đường ra đã chốt 13/11) |
| Nói chắc sai | Không giá, không "còn phòng"; nhãn "chưa kiểm"; hạng theo danh mục | khớp |
| Dữ liệu cá nhân | Không có (chỉ tên / địa chỉ cơ sở kinh doanh công khai) | khớp |
