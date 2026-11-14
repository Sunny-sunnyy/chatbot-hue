# Ảnh Khám phá v4b — lượt bổ sung (12 quán + 2 minor của C; biển Thuận An thử rồi bỏ) · E · 18:23 14/11/2026

Nhánh `p9-anh-v4b`, chồng trên main `7784385` (đã có v4). Tiền: **0 USD OpenAI / Serper**; Codex tính vào gói ChatGPT; Commons miễn phí.
Việc do A giao sau khi merge v4 (User: "đầy đủ").

## Kết quả (sau sửa theo review C `c_review_anh_v4b.md`)
| | Main (v4) | Nhánh này |
|---|---|---|
| Bài Khám phá có ảnh | 212 / 224 | **218 / 224** |
| Ảnh hiện được cạnh câu trả lời trợ lý (không `kc`) | 162 | 161 |
| Ảnh `kc` | 50 | 57 |
| Ảnh lịch | 33 / 34 | 33 / 34 (không đổi) |

Số "hiện được" giảm 1: thêm Bảo Thạnh (+1), bớt 2 ảnh mà C bắt ở review v4 nay gắn `kc` (−2).

- **12 quán còn trống ⇒ nhận 6, còn 6 trống.**
  - Cách làm:
    - Codex tra trang review hoặc trang địa điểm của từng quán (346 s, 27 trang mở, 0 URL tự khai). Codex không đọc được URL file ảnh nào.
    - Script `lay_anh_trang.py` mở các trang đó và tải ảnh có `alt` hoặc tên file khớp tên quán (20 ảnh).
    - E chọn và nhìn cả 20 ảnh. Chỉ một người chọn ⇒ ảnh gắn `kc`, trừ khi biển tên đọc rõ trong ảnh.
  - Nhận:
    - Tiệm bánh Bảo Thạnh: không `kc`, biển tên đọc rõ.
    - 5 quán gắn `kc`: Phúc Long (từ trang chính thức chi nhánh Huế), Rú, Cơm hến 17 Hàn Mặc Tử, Cơm hến Thu Hiền, Đầm Chuồn An Phú.
  - Vẫn trống:
    - 1 quán: mọi ảnh có dấu nước to vắt ngang;
    - 1 quán: chỉ có ảnh ghép 4 ô;
    - 1 quán: trang lỗi chứng chỉ SSL;
    - 2 quán: Codex không tìm ra trang nào có ảnh;
    - Đầm Chuồn Hội Quán: theo review C m-1 — ảnh là chỗ thuê ván chèo có chữ "Quán", không chắc là quán.
- **Biển Thuận An — thử rồi bỏ** (review C M-1):
  - Ảnh Commons duy nhất mà tác giả ghi đúng tên nơi lại có nhiều trẻ em mặc đồ bơi ở giữa khung. Điều này trái luật chung trong `TIEU_CHI.md`, chính E đã ghi.
  - Người ở khắp ảnh nên không cắt được. Tìm thêm 6 cụm từ trên Commons: không có ảnh nào khác (chỉ một tranh khắc cổ).
  - ⇒ Khám phá giữ ảnh v4 (`kc`), ảnh lịch vẫn trống 33 / 34, bảng lịch v3 không dùng.
  - Bài học: người chọn (E) nhìn ảnh theo câu hỏi "có đúng nơi không" mà quên luật chung về người trong ảnh. Lần sau, bước nhìn lại đọc cả danh sách luật bỏ ảnh.
- **Minor C (`c_review_anh_v4.md`):**
  - m-1: bài cẩm nang đi lại ⇒ `kc`.
  - m-2: ảnh có bảng giá lệch với kho ⇒ `kc`.
  - m-3 (số điện thoại nhỏ trên biển một quán): giữ, không chặn.

## Kiểm [Chạy]
- Script sinh `anhBai.js`: 218 ảnh, 57 `kc`; assert không chép chuỗi trùng kho vẫn đạt.
- 0 file ảnh mồ côi trong `kp/`: đã gỡ ảnh Hội Quán.
- Ảnh Thuận An giống hệt main.
- `npm run build` đạt.
- pytest `test_cong_dot_1` + `test_static_ui` + `test_anh_tra_loi` 27 đạt (36 s).
- Bản đầu nhánh (`1eb8d09`, trước khi sửa): 117 test đạt; server tạm 219 / 219 ảnh trả 200.
- Không Playwright: không đổi giao diện.

## Hồ sơ (private)
`data/anh_day_du_2026-11-14/`:
- `tools/gop_anh_v4.py` (`COMMONS`, `BO_SUNG`, `THEM_KC`);
- `tools/lay_anh_trang.py`; `tools/lich_thuan_an.py` + `data/phase_9/lich_trinh/bang_anh_v3.json` (không dùng — Thuận An bỏ);
- `quan12/`, `thuan_an/`;
- kết quả Codex: `data/tra_cuu_cli/2026-11-14_anh-12-quan/`.
