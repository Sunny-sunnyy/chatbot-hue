import { giamChuyenDong } from "../hieuUng.js";

// Hình sông dùng chung của giao diện "Dòng sông dẫn đường" — MỘT nét cho mọi nơi (lúc chờ ở Hỏi đáp, trục ngày – buổi ở Lên kế hoạch…).
// Cách vẽ một khúc sông: nền `.net-song` (dải nhạt) + `.net-song-chay` (nét đứt chạy giữa dòng, chỉ chạy dưới `.hieu-ung`) + `<Do />` (con đò màu nắng).
// Kiểu ở `song.css` mục "Nét sông dùng chung". Hình tự vẽ giản lược, không lấy hình học bản đồ.
export const SONG_NGANG = "M0 24 C60 6 110 6 170 24 S280 42 340 24 S450 6 510 24 S570 38 600 28";  // viewBox 0 0 600 44 — khúc sông nằm ngang
export const SONG_DOC = "M318 0 C318 96 78 116 78 214 C78 312 312 322 312 420 C312 518 96 528 66 640";  // viewBox 0 0 390 640 — khúc sông chảy dọc (chữ S)

// Con đò (đò mái vòm trên sông Hương, nhìn TỪ TRÊN XUỐNG như trên bản đồ: thân thoi nhọn hai đầu + mái vòm ở giữa) — xoay theo hướng dòng nào cũng đúng dáng. Đặt trong một <svg>, đi dọc đường có id `duong` (thẻ <path id=…> của chính
// svg đó). `to` = hệ số phóng; `giay` = thời gian đi hết đường; `xoay` = cách xoay theo đường (mặc định "auto").
export function Do({ duong, to = 1.5, giay = 7, lop = "do-song", batDau, xoay = "auto" }) {
  if (giamChuyenDong()) return null;  // máy bật giảm chuyển động: không vẽ con đò (đứng yên thì nó nằm ở gốc toạ độ, lạc chỗ) — nét sông vẫn còn
  return (
    <g className={lop}>
      <g transform={`scale(${to})`}>
        <path className="do-than" d="M-17 0 C-9 -7.5 9 -7.5 17 0 C9 7.5 -9 7.5 -17 0 Z" />
        <path className="do-mai" d="M-6 -4.2 H5 C7.5 -4.2 7.5 4.2 5 4.2 H-6 C-8.5 4.2 -8.5 -4.2 -6 -4.2 Z" />
      </g>
      <animateMotion dur={`${giay}s`} begin={batDau} repeatCount="indefinite" rotate={xoay}><mpath href={`#${duong}`} /></animateMotion>
    </g>
  );
}
