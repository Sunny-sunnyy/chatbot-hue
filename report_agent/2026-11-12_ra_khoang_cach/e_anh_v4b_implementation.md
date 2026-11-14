# Ảnh Khám phá v4b — lượt bổ sung (biển Thuận An + 12 quán + 2 minor của C) · E · 18:23 14/11/2026

Nhánh `p9-anh-v4b`, chồng trên main `7784385` (đã có v4). Tiền: **0 USD OpenAI / Serper**; Codex tính vào gói ChatGPT; Commons miễn phí.
Việc do A giao sau khi merge v4 (User: "đầy đủ").

## Kết quả
| | Main (v4) | Nhánh này |
|---|---|---|
| Bài Khám phá có ảnh | 212 / 224 | **219 / 224** |
| Ảnh hiện được cạnh câu trả lời trợ lý (không `kc`) | 162 | **162** |
| Ảnh `kc` | 50 | 57 |
| Ảnh lịch | 33 / 34 | **34 / 34** |

Số "hiện được" không đổi: +1 Thuận An, +1 Bảo Thạnh, −2 bài C bắt phải gắn `kc`.

- **Biển Thuận An:**
  - Ảnh Commons "Thuận An Beach, Huế, Vietnam" (CC BY-SA 3.0). Chính tác giả ghi tên nơi trong chú thích.
  - Luật A đặt cho lượt này: ảnh có tên nơi trong chú thích của tác giả là ảnh chắc.
  - E xem: bãi cát và biển; người trong ảnh nhỏ, không ai là trọng tâm.
  - Dùng cho cả Khám phá (bỏ `kc`) và ảnh lịch. Bảng lịch là file mới `bang_anh_v3.json`; bảng v2 mà main đang trỏ tới giữ nguyên, \`settings.yaml\` trỏ sang v3.
- **12 quán còn trống ⇒ nhận 7, còn 5 trống:**
  - Cách làm:
    - Codex tra trang review hoặc trang địa điểm của từng quán (346 s, 27 trang mở, 0 URL tự khai). Codex không đọc được URL file ảnh nào.
    - Script `lay_anh_trang.py` mở các trang đó và tải ảnh có `alt` hoặc tên file khớp tên quán (20 ảnh).
    - E chọn và nhìn cả 20 ảnh. Chỉ có một người chọn, nên ảnh gắn `kc`, trừ khi biển tên đọc rõ trong ảnh.
  - Nhận:
    - Tiệm bánh Bảo Thạnh: không `kc`, biển tên đọc rõ.
    - 6 quán gắn `kc`: Phúc Long (từ trang chính thức chi nhánh Huế), Rú, Cơm hến 17 Hàn Mặc Tử, Cơm hến Thu Hiền, Đầm Chuồn An Phú, Đầm Chuồn Hội Quán.
  - Vẫn trống:
    - 1 quán: mọi ảnh có dấu nước to vắt ngang;
    - 1 quán: chỉ có ảnh ghép 4 ô;
    - 1 quán: trang lỗi chứng chỉ SSL;
    - 2 quán: Codex không tìm ra trang nào có ảnh.
- **Minor C (`c_review_anh_v4.md`):**
  - m-1: bài cẩm nang đi lại ⇒ `kc`.
  - m-2: ảnh có bảng giá lệch với kho ⇒ `kc`.
  - m-3 (số điện thoại nhỏ trên biển một quán): giữ, không chặn.

## Kiểm [Chạy]
- Script sinh `anhBai.js`: 219 ảnh, 57 `kc`; assert không chép chuỗi trùng kho vẫn đạt.
- `npm ci && npm run build` đạt.
- pytest `test_cong_dot_1` + `test_static_ui` + `test_anh_tra_loi` + `test_len_ke_hoach_v2`: 117 đạt (49 s).
- Server tạm của worktree (cổng 8037, kiểm cwd, không lượt có phí):
  - khởi động được ⇒ bảng ảnh lịch v3 qua bước kiểm lúc nạp (\`nap_bang_anh\`);
  - \`/static/anh/lich/bien_thuan_an.jpg\` trả 200;
  - 219 / 219 file ảnh Khám phá trả 200.
- Không Playwright: không đổi giao diện, chỉ đổi file ảnh và bảng.

## Hồ sơ (private)
`data/anh_day_du_2026-11-14/`:
- `tools/gop_anh_v4.py` (`COMMONS`, `BO_SUNG`, `THEM_KC`);
- `tools/lay_anh_trang.py`, `tools/lich_thuan_an.py`;
- `quan12/`, `thuan_an/`;
- kết quả Codex: `data/tra_cuu_cli/2026-11-14_anh-12-quan/`.
