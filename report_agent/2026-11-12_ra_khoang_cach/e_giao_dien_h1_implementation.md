# Giao diện H1 "Sông Hương" lên code — dung lượng JS / CSS theo từng trang · E, 12:32 14/11/2026

Plan: `docs/superpowers/plans/2026-11-14-giao-dien-h1-plan.md` (A duyệt). Nhánh `p9-gd-h1`, A đã merge vào main trên máy ở `55f48fe`.

**Vì sao có mục này:** plan đặt ngưỡng JS tăng ≤ 8 KB (gzip). Thực tế tăng **+10,53 KB**: JS chính 112,08 KB ⇒ 122,61 KB gzip. A nhờ E ghi rõ trang nào thêm bao nhiêu.

## Cách đo
- Build lại bằng `vite build` ở từng commit của nhánh, tính từ commit gốc trên main `a192843`.
- Dùng một worktree tạm, chung `node_modules` với worktree của E. Đọc cỡ gzip vite in ra cho `index-*.js` và `index-*.css`.
- 0 USD.

| Commit | Việc | JS gzip | Tăng JS | CSS gzip |
|---|---|---|---|---|
| `a192843` | mốc (main trước giao diện mới) | 112,08 KB | — | 7,04 KB |
| `848eafa` | đợt 0: lớp chung, font, lớp hiệu ứng, View Transitions (E) | 112,46 | +0,38 | 7,92 |
| `4118069` | Trang chủ (E) | 114,45 | +1,99 | 9,36 |
| `db8c875` | Lên kế hoạch + thẻ lịch dòng thời gian, ảnh + ghi công (E) | 116,10 | +1,65 | 11,15 |
| `d6bc51e` + `0afcebd` | Trợ lý Huế: bước công cụ thật, cột gợi ý (B) | 117,49 | +1,39 | 11,76 |
| `9f086d2` | Xuất lịch `.ics` (E) | 118,79 | +1,30 | 11,79 |
| `d72e7f0` | Khám phá, trang bài, Giới thiệu (C) | 122,54 | **+3,75** | 13,38 |
| `6f37756` + `ff2ebe9` | sửa theo review (CLS, cờ, mất dòng) | 122,61 | +0,07 | 13,39 |

## Đọc số
- **Phần tăng lớn nhất là Khám phá (+3,75 KB).** Trong đó có `anhBai.js`: bảng 24 ảnh, mỗi ảnh có tên tác giả, giấy phép và link trang Commons dài (URL đã mã hoá %). Phần còn lại là trang danh sách / trang bài mới và biểu tượng SVG theo lĩnh vực.
- **Font không tính vào JS.** Font serif nạp qua `@fontsource` thành file `.woff2` riêng.
- **Ảnh không tính vào JS.** Ảnh nằm ở `public/`, tải khi cần.
- **Không thêm thư viện nào.** Hiệu ứng là CSS cộng khoảng 30 dòng JS (`hieuUng.js`).
- **Giảm dưới ngưỡng thì có cách, nhưng chưa làm.**
  - Tách mỗi trang thành chunk riêng bằng `React.lazy` (mỗi trang chỉ tải phần của mình).
  - Chuyển bảng ghi công ảnh sang file JSON tải khi cần.
  - Mỗi cách đều thêm một lần tải khi chuyển trang và có thể làm chuyển trang (View Transitions) kém mượt. Khoảng 10 KB gzip trên mạng 4G mất dưới 0,1 giây.
  - E đề xuất **giữ như hiện tại**, nâng ngưỡng của plan cho đợt này lên 11 KB. A / User chốt.
