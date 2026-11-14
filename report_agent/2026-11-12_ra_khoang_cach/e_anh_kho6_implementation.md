# Ảnh Khám phá cho 16 bài ghi kho 6 (lễ hội / nghệ thuật) · E · 20:42 14/11/2026

- Nhánh `p9-anh-kho6`. Việc A giao.
- Tiền: Serper 16 lượt ≈ 0,016 USD; Commons miễn phí; agent con tính vào quota Claude.

## Kết quả
| | Main (sau ghi kho 6) | Nhánh này |
|---|---|---|
| Bài Khám phá có ảnh | 238 / 263 | **248 / 263** |
| Ảnh hiện được cạnh câu trả lời | 188 | **196** |
| Ảnh `kc` | 50 | 52 |

- **Cách chọn:**
  - 1 agent con chọn theo `BRIEF_CHON.md`, có luật riêng cho 3 loại bài:
    - lễ cụ thể: đúng lễ + đúng nơi;
    - phong tục chung: phải là ở Huế;
    - nghệ thuật: đúng loại hình.
  - E nhìn cả 12 ảnh agent chọn.
- **Kết quả nhận:**
  - 8 ảnh không `kc`: mỗi ảnh có công trình nhận ra được hoặc tiêu đề trang khớp đúng lễ và nơi.
  - 2 ảnh `kc`:
    - 2 ảnh nhóm diễn ca Huế, cho hai bài về hai loại hình hát; chỉ dựa vào tiêu đề trang để biết đúng loại;
    - (1 ảnh lễ của đồng bào miền núi đã gỡ theo review C m-1: có thể có trẻ em ở tiền cảnh ⇒ bài để trống.)
  - E bác 1 ảnh: 3 diễn viên chụp gần, mặt rõ là trọng tâm ⇒ bài đó để trống.
- **6 bài vẫn trống** (gồm bài gỡ theo review C): ứng viên là lễ cùng tên ở vùng khác (Nam Bộ, Hà Nội), là một lễ khác, là poster, hoặc không có ảnh nào chắc đúng lễ.

## Sửa script dựng
`dung_anh_bai_js.py` (private, `data/`):
- Thêm đọc bảng v7.
- Thêm bước đổi trang nguồn của ảnh CŨ về trang chủ tên miền khi trang đó nay trùng nguồn của bài kho mới. Lý do: kho lớn dần nên 5 trang cũ bị assert chặn. Đây là cùng luật đã áp cho ảnh mới.
- Trang nguồn chỉ nằm trong file ghi công private. `anhBai.js` chỉ chứa đường ảnh và cờ `kc`.

## Kiểm [Chạy]
- Script sinh `anhBai.js`: 248 ảnh, 52 `kc`; `anhBai.js` chỉ thêm 10 dòng, 0 dòng cũ đổi.
- 0 file ảnh mồ côi.
- `npm run build` đạt.
- pytest `test_cong_dot_1` + `test_static_ui` + `test_anh_tra_loi` đạt.

## Hồ sơ (private)
`data/anh_kho6_2026-11-14/`: `tools/tim.py`, `ung_vien.json`, `bang_ghep/`, `BRIEF_CHON.md`, `chon.json`, `bang_anh_kham_pha_v7.json`.
