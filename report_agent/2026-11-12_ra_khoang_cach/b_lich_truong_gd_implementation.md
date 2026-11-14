# Hai trường backend cho giao diện lịch mới — B · 10:59 14/11/2026

Nhánh `p9-lich-truong-gd` từ `ee6dde9`, commit **`0025878`** (push). A giao 14/11 (mức nhẹ, 0 USD). Người review: E hoặc C.

## Plan (mức nhẹ, ghi trước khi code)
- **Mục tiêu:** giao diện mới (khung của E, `data/ui_mau_2026-11-14/KHUNG_LEN_KE_HOACH.md`) đặt dòng "Nếu mưa" dưới đúng ngày và hiện "khoảng N phút đi" giữa hai điểm, **không bóc chữ**, không đoán.
- **Tiêu chí:**
  - (1) mọi dòng dự báo / "Nếu mưa" có `ngay` đúng với ngày trong câu; dòng nguồn không có;
  - (2) `phut_di` chỉ có giữa hai điểm liền nhau **cùng buổi**, bằng đúng số bộ xếp đã dùng để giãn giờ; mục đầu buổi / buổi tối / tối nghỉ không có;
  - (3) chữ người dùng thấy và chuỗi gửi model **không đổi**;
  - (4) ca dò toàn tổ hợp 0 lỗi.
- **Bộ đo:** test file chạm + ca dò `do_sua_1411.py` (đã thêm kiểm `ngay`). **Tiền:** 0.

## Làm gì
- `len_ke_hoach.dong_du_bao` trả `[{"cau", "ngay"}]` thay vì chuỗi; `dung_lich` nối nguyên dict vào `ghi_chu` mã `du_bao`.
- `dung_lich`: mục thứ 2 trở đi trong cùng buổi (không phải tối) có `phut_di = _phut_di(trước, sau)`.
- **Vì sao không tính từ toạ độ:** bộ xếp đã giãn giờ bằng chính số này. Hiện số khác thì giờ và "phút đi" sẽ lệch nhau. Đây là số **ước theo cụm** (15 phút cùng cụm / 30 phút cụm kề), nên giao diện nên ghi "khoảng".

## Kết quả
| Kiểm | Kết quả |
|---|---|
| Test `test_len_ke_hoach_v2.py` + `test_ban_do_lich.py` | **96 đạt** (1 test mới). Test mới khẳng định: `phut_di` đúng chỗ, đúng giá trị, giờ mục sau ≥ giờ xong mục trước + `phut_di`; `tin_nhan_model` và `ghep_chu` không chứa trường mới; ghi chú `du_bao` trong `lich` mang đúng `ngay` |
| Ca dò 9.600 khung (có / không dự báo) | 0 mã lỗi kiểm khung; 13.824 ngày mưa: mỗi ngày đúng một dòng "Nếu mưa" **có `ngay` đúng** |
| Q1 (chuỗi gửi model giống byte) | **không chạy**: `tin_nhan_model` không đổi và chỉ đọc `id_muc` / `ten` / `nguon` (test khẳng định); đường cờ tắt không chạm |

**Giới hạn:** giao diện hiện tại chưa dùng hai trường (chờ giao diện mới của E). `phut_di` là số ước theo cụm, không phải đường đi thật.

## Thêm: nhãn "kiểm lịch diễn" gắn nhầm cho chợ (A báo từ lượt thật trên `main` `86c093d`) — 11:03 14/11/2026

- **Lỗi:** không có ngày đi ⇒ mọi hoạt động tối đều nhận nhãn "kiểm lịch diễn trước khi đi", kể cả chợ / phố đêm (không có suất diễn).
- **Sửa** (commit `3ba7e9b`; nhánh rebase lên `main` `86c093d`): nhãn chỉ cho điểm tối loại lễ hội – nghệ thuật (`co_suat_dien`). Điểm chỉ mở vài tối trong tuần vốn không được xếp khi chưa có ngày (`dung_thu`, có test) ⇒ không cần nhãn khác.
- **Bộ chấm ý 5** (`tools/nghiem_thu.py`) đổi theo: nhãn phải có đúng ở điểm diễn và không có ở chợ / phố. Ý 5 trong định nghĩa chấm vẫn giữ nguyên ("không khẳng định hoạt động tối diễn ra hôm đó") — chợ / phố mở mọi tối nên không có khẳng định sai.
- **Đếm** (`tools/do_nhan_toi.py`, 0 USD):

  | | Lịch có nhãn sai | Mẫu số |
  |---|---|---|
  | Trước sửa (không ngày đi) | **228** | 960 |
  | Sau sửa, không ngày đi (**cùng nhóm với dòng trên**) | **0** | 960 |
  | Sau sửa, mọi tổ hợp (cả có ngày đi) | **0** | 3.840 (2.700 mục tối, 144 có nhãn — đều là điểm diễn chưa có ngày) |

- **Test:** sửa test nhãn để phủ cả điểm diễn lẫn chợ / phố; 96 đạt.
- **Review C** (`c_review_lich_truong_gd.md`): ready, 0 blocker / 0 major. m-1: `co_suat_dien` suy từ loại sở thích ⇒ nếu sau này thêm điểm tối loại lễ hội mà không phải buổi diễn thì cần sửa luật. Đã ghi điều kiện này vào `ghi_chu` của bảng `diem_v8.json`. m-2: giao diện ghi "khoảng N phút" — đã báo E (bản mẫu H1 đã ghi "khoảng").
