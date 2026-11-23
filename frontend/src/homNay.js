import { anhCuaBai, khoaBai } from "./anhBai.js";

// Ô "Hôm nay ở Huế" của Trang chủ (23/11/2026): mỗi ngày MỘT bài của kho, do code chọn — không model, không API mới, không ảnh mới.
// Tập chọn = bài của `/api/kham_pha` có ảnh mà ảnh KHÔNG mang dấu "không chắc" (`kc`), xếp theo khoá băm của mã bài (thứ tự ổn định, trông như đã xáo);
// bài của ngày = phần tử thứ (số ngày theo giờ Việt Nam) chia dư cho cỡ tập ⇒ ai mở cùng ngày cũng thấy cùng bài, hết tập thì quay vòng.
// File riêng (không nằm trong TrangChu.jsx) để phép chọn chạy được bằng Node khi kiểm, không cần dựng giao diện.
const LECH_VN_MS = 7 * 3600 * 1000;  // giờ Việt Nam = UTC+7 quanh năm (không đổi giờ theo mùa) ⇒ mốc đổi bài là 0 giờ Việt Nam
const MOT_NGAY_MS = 24 * 3600 * 1000;

export function soNgayVN(luc = Date.now()) {
  return Math.floor((luc + LECH_VN_MS) / MOT_NGAY_MS);
}

export function baiHomNay(bai, luc = Date.now()) {
  const tap = (bai || []).filter(b => { const a = anhCuaBai(b.id); return a && !a.kc && b.tieu_de; })
    .map(b => [khoaBai(b.id), b]).sort((x, y) => (x[0] < y[0] ? -1 : x[0] > y[0] ? 1 : 0));
  if (!tap.length) return null;  // danh sách chưa tải / lỗi / không bài nào có ảnh chắc ⇒ Trang chủ không vẽ ô
  const b = tap[soNgayVN(luc) % tap.length][1];
  return { bai: b, anh: anhCuaBai(b.id).anh };
}
