# Review — nhánh `p9-cho-o` (trang "Chỗ ở" + bảng lưu trú v3)

Người kiểm: E (`hue-rag-3e`) · ghi lúc 10:45 15/11/2026 (`date`) · người làm: C · plan khách sạn bản 2 §1 (sha `b5d8bc184090`).
Phạm vi: `86acfb1`, dựng trên `3c27cc9`. 10 file, +168 / −3. Bảng `data/khach_san_2026-11-15/bang_luu_tru_lich_v3.json` (md5 `97eedb0cc2ab` — khớp C báo, 137 cơ sở).

**Kết luận: `ready_for_user_confirmation`.** m-1 nên sửa (1 dòng); m-2, m-3 tuỳ C. Sửa ≤ 2 dòng thì A merge thẳng.

## Đã kiểm

| Cổng | Kết quả |
|---|---|
| Đúng plan | `/api/cho_o` theo cờ `luu_tru_lich` (tắt ⇒ 404, dựng một lần). Trang chỉ mở từ ô "Nơi ở" (không lên thanh trên cùng). Nhóm khu ⇒ mức. Trong mức: có ảnh trước. Không giá / điện thoại / toạ độ. Link chỉ 2 gốc, kiểm cả phía trình duyệt. Ảnh chỉ `/anh/khach_san/` |
| Bảng v3 | Gộp La Perle; bỏ A Lưới / Phong Điền; La Vela vào trung tâm. 10 / 10 cơ sở ven biển có `phia_bien`, loader từ chối giá trị sai (test 3 ca hỏng có ca đối chứng) |
| Lịch đổi vì bảng v3 | 364 / 3.840 khung, một kiểu: La Vela (5 sao, có ảnh) thay Indochine Palace (5 sao, có ảnh) khi cụm chính là An Cựu. Hợp lý: La Vela gần An Cựu hơn |
| Test | `test_luu_tru_lich.py` **11 passed**, cả có / không `--env-file` (12,0 s / 10,8 s) — nhánh đổi `settings.yaml`. Cả suite: C chạy 1.050 passed; E không chạy lại (máy đang nhường dự án khác) |
| `git diff --check` | sạch |

## Câu C nhờ xét

1. **Gloria vào "phía bắc":** chấp nhận. Toạ độ Places (16,441 · 107,810) cách tâm cụm Thuận An / Tam Giang **23,2 km**, cách tâm cụm nam **25,7 km**, tức gần như giữa hai phía. Theo địa giới, Phú Vinh thuộc Phú Vang, khớp nhãn nhóm "Thuận An, Phú Vang". Đây là E suy luận về địa giới, chưa tra lại.
2. **Lịch vẫn lọc phía bằng chữ trong địa chỉ** (`PHIA_BIEN`, `luu_tru_lich.py:27/79`) nên Gloria không vào lịch.
   - Chấp nhận cho nhánh này, không sửa trong đây (chồng `chon_co_so` với nhánh của B).
   - Đề xuất việc nhỏ sau khi cả hai merge: lọc bằng trường `phia_bien` (cụm `dong_bien` ⇒ bac, `nam_xa` ⇒ nam) thay cho dò chữ.
   - E đã đối chiếu: 9 / 10 cơ sở cho cùng kết quả cả hai cách; chỉ Gloria đổi (thêm một 4 sao cho lịch ven biển phía bắc). Vừa đơn giản hơn, vừa khớp với trang.

## Finding

**m-1 (nên sửa, 1 dòng):** key React trùng.
- `ChoO.jsx` dùng `key={c.ten}`, nhưng bảng v3 có **"Khách sạn Như Phú" hai dòng cùng nhóm trung tâm, cùng mức** (16 Chu Văn An — 1 sao; 14b Chu Văn An — Đạt chuẩn). Test chỉ khoá duy nhất theo (tên, địa chỉ).
- Hệ quả: trong một danh sách có hai key trùng thì React có thể vẽ sai khi đổi bộ lọc. Bản dev báo cảnh báo trong console; bản build không báo, nên Playwright "0 lỗi console" không bắt được.
- Đóng khi: `key={c.ten + "|" + (c.dia_chi || "")}`.

**m-2 (tuỳ C):** link "Xem thêm chỗ ở khu này" từ lịch ven biển mở **cả hai phía**.
- `o.khu` = khu ven biển (không có phía) ⇒ `n.khu.startsWith(chon)` khớp cả `:bac` lẫn `:nam`.
- Khách đi Thuận An thấy cả Lăng Cô, cách khoảng 40 km. Cũng không nút lọc nào sáng.
- Đóng khi (tuỳ chọn): `o_dau` trả thêm phía ⇒ link `#/cho-o/<khu>:<phía>`. Hoặc ghi vào giới hạn: chỉ 36 / 3.840 lịch là ven biển.

**m-3 (tuỳ C):** hash khu lạ (vd `#/cho-o/abc`) ⇒ trang chỉ còn tiêu đề và dòng nguồn, không có cơ sở nào, không nút nào sáng. Gợi ý: không khớp nhóm nào ⇒ coi như "Mọi khu". Không phải lỗi an toàn, vì React thoát ký tự.

## Ghi cho checklist deploy (A)
Allow-list `dung_dockerignore.py` đang ghi bảng lưu trú **v2**. Từ nhánh này `settings.yaml` trỏ **v3** (`data/khach_san_2026-11-15/bang_luu_tru_lich_v3.json`) ⇒ đổi lúc deploy.

## Tiền / thời gian
0 USD. Pytest 2 × ~11 s. Không Playwright (C đã chạy 1440 + 390; máy đang bận).
