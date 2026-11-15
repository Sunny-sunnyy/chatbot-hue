# Ba sửa giao diện theo lượt thử của User (E · 15:46 15/11/2026, `date`)

Người làm: E. A giao (User tự thử trên bản đang chạy, A ghi nhận 15:38 15/11/2026). Nhánh `p9-gd-3-sua`. Chỉ đổi `frontend/src/` (6 file, +20 / −46 dòng); không đổi server, lời dặn, dữ liệu.

## 1. Đã đổi gì
| # | User báo | Sửa | File |
|---|---|---|---|
| 1 | Bỏ dòng báo "ảnh được gửi tới … để đoán tên" cạnh nút Hỏi bằng ảnh | Bỏ dòng đó. **Lưu ý:** dòng này là yêu cầu của spec Phase 10 (báo đường dữ liệu ra ngoài ngay tại nút); bỏ theo yêu cầu của User — người dùng duy nhất hiện nay. Trang Giới thiệu vẫn còn câu nói ảnh gửi tới đâu, không lưu. Bản công khai cần dòng báo lại (A ghi checklist deploy). | `HoiBangAnh.jsx` |
| 2 | Bỏ dòng "Các bước: …" dưới câu hỏi sau khi đã có câu trả lời | Bỏ dòng tóm tắt bước. Lúc chờ chỉ còn **một** dòng — bước đang chạy (từ sự kiện thật của server) + ba chấm; chữ trả lời đầu tiên hiện ⇒ dòng biến mất, không để lại gì. Dòng tiến độ xếp lịch (đường lịch cũ) cùng kiểu: lúc chờ chỉ bước mới nhất, xong thì mất. Đổi được ở **một chỗ**: hằng `HIEN_BUOC_LUC_CHO` trong `chat.jsx` (false ⇒ lúc chờ chỉ còn ba chấm). Gỡ luôn code + CSS chỉ phục vụ danh sách bước cũ. | `chat.jsx`, `LenKeHoach.jsx`, `tl.css` |
| 3 | Nút "Sửa — điền lại biểu mẫu" ở trang Lên kế hoạch không hoạt động | Xem mục 2. | `App.jsx`, `index.css` |

## 2. Lỗi nút Sửa — tái tạo trước khi sửa, nguyên nhân gốc
Playwright trên bản build do FastAPI phục vụ (`data/gd_3_sua_2026-11-15/tools/pw_sua.py`): xếp một lịch 3 ngày bằng biểu mẫu ⇒ đổi biểu mẫu sang giá trị khác ⇒ bấm nút.
- **Trước sửa:** biểu mẫu CÓ được điền lại đúng giá trị đã gửi, nhưng trang đứng yên (vị trí cuộn 4.590 ⇒ 4.590 px) và biểu mẫu nằm ngoài màn hình ⇒ người dùng không thấy gì xảy ra. Gốc: nút nằm cuối lịch, cùng trang với biểu mẫu; hàm xử lý chỉ đổi địa chỉ trang sang chính trang đang đứng ⇒ trình duyệt không cuộn.
- **Sửa:** đang ở trang Lên kế hoạch ⇒ cuộn tới biểu mẫu + đưa tiêu điểm vào ô đầu của biểu mẫu; biểu mẫu chừa 96 px cho thanh đầu trang dính.
- **Sau sửa:** khổ 1440: cuộn 4.614 ⇒ 3.995, biểu mẫu trong màn hình (cách đỉnh 88 px), giá trị đúng như đã gửi, tiêu điểm ở biểu mẫu. Khổ 390: cuộn 6.943 ⇒ 228, biểu mẫu trong màn hình (đo trước khi thêm bước đưa tiêu điểm — bước đó không cuộn).
- Nút cùng tên ở trang Trợ lý: trước và sau sửa đều chạy đúng (sang trang Lên kế hoạch, đầu trang, biểu mẫu đúng giá trị).

## 3. Kiểm
| Bước | Kết quả |
|---|---|
| `npm ci && npm run build` | đạt; JS chính 406.310 ⇒ 405.095 byte (bớt code danh sách bước) |
| `test_static_ui.py` + `test_cong_dot_1.py` | 26 đạt (45 s); sau rebase `test_static_ui.py` 4 đạt |
| Playwright trước / sau (1440) + sau (390) | dòng báo ảnh 1 ⇒ 0; dòng "Các bước" sau câu trả lời 1 ⇒ 0; nút Sửa như mục 2; 0 lỗi console. Ảnh + số: `data/gd_3_sua_2026-11-15/{truoc,sau,sau_390}/` |
| Test rộng, Q1 | NOT RUN — chỉ đổi giao diện |

Tiền: 4 lượt Playwright × (1 lịch + 1 câu) ≈ 0,005 USD (3 lượt đầu 0,0034 theo log; lượt cuối ước cùng cỡ).

## 4. Giới hạn
- Dòng bước lúc chờ: mình chỉ chụp được nhãn đầu ("đang hiểu câu hỏi") vì câu thử trả lời nhanh; các nhãn sau dùng cùng một dòng nên không kiểm riêng.
- Cột trái trang Trợ lý vẫn có dòng mô tả tính năng đoán tên từ ảnh (không phải dòng User yêu cầu bỏ) — giữ.

**Giải thích ngắn:** nút Sửa vốn vẫn điền lại biểu mẫu nhưng người dùng đang đứng ở cuối lịch nên không nhìn thấy — giờ trang tự cuộn về biểu mẫu. Hai dòng chữ User thấy thừa đã bỏ; lúc chờ vẫn còn một dòng báo trợ lý đang làm gì để màn hình không "đứng".

## 5. Sau review C (ready, 0 blocker / 0 major / 2 minor; C đọc diff + grep, không chạy lại Playwright)
- m-1 đóng: lớp `.progress` nay là một dòng chữ ⇒ bỏ `padding-left` + `list-style` của danh sách cũ (dòng bước không còn thụt vào so với ba chấm).
- m-2 (tài liệu, A sửa khi merge): `Project_Status.md` §6 ghi ảnh gửi đi "kèm dòng báo trên giao diện" — nay dòng báo chỉ còn ở trang Giới thiệu.
