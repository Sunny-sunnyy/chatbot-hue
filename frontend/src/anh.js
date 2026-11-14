// Ảnh của cổng (User chốt 07/11): đóng vào bản build (`public/anh/`), không link ảnh ngoài — CSP `img-src 'self'` giữ nguyên.
// Chỉ đường ảnh: giao diện không hiện ghi công (User 14/11). Nguồn + giấy phép từng ảnh giữ ở bảng dữ liệu
// `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/bay_anh_dot1.json` (ảnh Commons) — không vào bản build.
/* global __CO_ANH_LE_HOI_RIENG__ */

const GOC = `${import.meta.env.BASE_URL}anh/`;

// `srcNho`: bản cho màn ≤ 760 px (`data/phase_11/anh_cong/tools/anh_nho.py`; việc nhỏ 10 — điện thoại tải ít byte hơn).
function anh(file) {
  return { src: GOC + file, srcNho: GOC + file.replace(/\.jpg$/, "_nho.jpg") };
}

export const MAN_NHO = "(max-width: 760px)";  // cùng mốc khổ điện thoại của `index.css`

// Ảnh lễ hội: ảnh thật chỉ có khi máy build có file `public/anh/rieng/` (xem `vite.config.js`); không thì ảnh Commons.
const LE_HOI = __CO_ANH_LE_HOI_RIENG__ ? anh("rieng/lv_festivals.jpg") : anh("lv_festivals.jpg");

export const ANH_DAU_TRANG = { song: anh("dau_trang_song.jpg"), ngoMon: anh("dau_trang_ngo_mon.jpg") };

// Khoá = mã lĩnh vực (`LINH_VUC` ở `chung.jsx`).
export const ANH_LINH_VUC = {
  foods: anh("lv_foods.jpg"),
  heritages: anh("lv_heritages.jpg"),
  festivals: LE_HOI,
  performing_arts: anh("lv_performing_arts.jpg"),
  travel: anh("lv_travel.jpg"),
};
