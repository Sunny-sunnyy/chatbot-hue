# Dòng nhắc dưới câu trả lời: link "trang Lên kế hoạch" nằm liền trong câu — report của phiên C (viết 11:06 22/11/2026)

Lỗi hình thức phiên đo thấy trong ảnh (khổ 1440): khi dòng nhắc có câu dẫn sang trang Lên kế hoạch, cụm link bị tách thành một cột hẹp bên phải, xuống ba
dòng, dấu chấm đứng lẻ. Nhánh `p9-c-notice-link`: một dòng ở `frontend/src/chat.jsx`.

**Vì sao:** dòng nhắc (`.notice`) là khối xếp ngang (flex) để biểu tượng đứng cạnh chữ. Khi câu có link, chữ trước link, link và phần sau link là ba phần tử
con ⇒ thành ba cột. Sửa: gói cả câu vào một khối `<span>` ⇒ biểu tượng + MỘT cột chữ, link chảy theo dòng như chữ thường. Dòng nhắc không có link không đổi.

**Số đo [máy kiểm; 0 đồng]** — server tạm cổng 8011 từ cây nhánh; câu trả lời của lượt là dữ liệu giả do trình duyệt tự trả cho `/api/chat/stream` đúng khuôn
sự kiện của server, chữ dòng nhắc là đúng hai câu code đang ghép ("…có thể đã thay đổi…" + câu dẫn trang); trang, CSS và các API khác là của server thật.
Script + ảnh (riêng tư): `data/test_cuoi/chay_2026-11-22_c_notice_link/` (`do_link.py`, `truoc/`, `sau/`).

| Bố cục | Link, TRƯỚC (rộng × cao, số dòng) | Link, SAU | Bấm link |
|---|---|---|---|
| 1440, trang Trợ lý | 55 × 67 px, 3 dòng | 130 × 18 px, 1 dòng | sang `#/len-ke-hoach` (trước và sau) |
| 1440, khung trợ lý nổi | 43 × 90 px, 4 dòng | 130 × 18 px, 1 dòng | như trên |
| 390, trang Trợ lý | 43 × 90 px, 4 dòng | nằm trong dòng chữ, ngắt dòng tự nhiên giữa cụm ("trang Lên kế / hoạch.") | như trên |

Tràn ngang 0, lỗi trang 0 ở cả ba, trước và sau. Chiều cao cả dòng nhắc ở khung nổi: 112 ⇒ 90 px.

**Chưa làm · giới hạn:** chưa có lượt nhìn trên lượt trả lời thật (phiên đo nhìn lại); sau khi gộp phải dựng lại `frontend/dist`. Quan sát thêm, KHÔNG sửa ở đây: link
trong dòng nhắc cùng màu, không gạch chân nên trông như chữ thường — người dùng khó biết là bấm được.

Phép này KHÔNG cho biết dòng nhắc trong khối lịch (`.lich-v2 .notice`) có cùng lỗi không (ở đó dòng nhắc không có link) · đếm rẻ nhất: không.

## Thêm 11:09 22/11/2026 — link trong dòng nhắc có kiểu link (phiên điều phối đồng ý sửa quan sát ở trên)
Một dòng CSS ở `frontend/src/index.css`: `.notice a` cùng kiểu với link trong câu trả lời (màu nhấn, gạch chân). Đo [máy kiểm, 0 đồng, cùng script, thư mục
`kieu_truoc/`, `kieu_sau/`] ở 1440 trang Trợ lý · 1440 khung nổi · 390 trang Trợ lý: gạch chân `none` ⇒ `underline`; màu link `rgb(70, 96, 95)` (trùng màu chữ
dòng nhắc) ⇒ `rgb(14, 107, 102)`; kích thước và số dòng của link không đổi so với bản đã gộp (130 × 18 px một dòng ở 1440; ngắt dòng tự nhiên ở 390); bấm vẫn sang
`#/len-ke-hoach`; tràn ngang 0, lỗi trang 0. Chưa có lượt nhìn trên lượt trả lời thật.
