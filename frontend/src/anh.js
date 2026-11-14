// Ảnh của cổng (User chốt 07/11): đóng vào bản build (`public/anh/`), không link ảnh ngoài — CSP `img-src 'self'` giữ nguyên.
// Nguồn + giấy phép: `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/bay_anh_dot1.json`; mọi ảnh trong git từ Wikimedia Commons.
/* global __CO_ANH_LE_HOI_RIENG__ */

const GOC = `${import.meta.env.BASE_URL}anh/`;
export const GP = {  // cũng dùng cho ghi công ảnh lịch (`chat.jsx` `AnhLich`)
  "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
  "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
  "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/",
  "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
  "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
  "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
};
const commons = file => `https://commons.wikimedia.org/wiki/File:${file}`;

// `srcNho`: bản cho màn ≤ 760 px (`data/phase_11/anh_cong/tools/anh_nho.py`; việc nhỏ 10 — điện thoại tải ít byte hơn).
function anh(file, cho, tacGia, giayPhep, nguon, doi = "thu nhỏ") {
  return { src: GOC + file, srcNho: GOC + file.replace(/\.jpg$/, "_nho.jpg"), cho, tacGia, giayPhep, linkGiayPhep: GP[giayPhep] ?? null, nguon, doi };
}

export const MAN_NHO = "(max-width: 760px)";  // cùng mốc khổ điện thoại của `index.css`

// Ảnh lễ hội: ảnh thật chỉ có khi máy build có file `public/anh/rieng/` (xem `vite.config.js`); không thì ảnh Commons phạm vi công cộng.
const LE_HOI = __CO_ANH_LE_HOI_RIENG__
  ? anh("rieng/lv_festivals.jpg", "Lễ hội — khai mạc Festival Huế 2024", "Cục Du lịch Quốc gia Việt Nam", null,
        "https://images.vietnamtourism.gov.vn/vn//images/2024/thang_10/0210.festival-hue-3.jpg")
  : anh("lv_festivals.jpg", "Lễ hội — đoàn rước qua Phu Văn Lâu, Festival Huế 2008", "Lưu Ly", "Phạm vi công cộng",
        commons("Festival_Hu%E1%BA%BF_2008-4.JPG"));

export const ANH_DAU_TRANG = {
  song: anh("dau_trang_song.jpg", "Đầu trang chủ — cầu Trường Tiền trên sông Hương", "Supanut Arunoprayote", "CC BY 4.0",
            commons("Truong_Tien_bridge_(I).jpg"), "phủ màu"),
  ngoMon: anh("dau_trang_ngo_mon.jpg", "Đầu trang Khám phá — Ngọ Môn", "Chainwit", "CC BY 4.0",
              commons("Hu%E1%BA%BF_(2024)_-_Meridian_Gate_-_Ng%E1%BB%8D_M%C3%B4n_(Ho%C3%A0ng_th%C3%A0nh_Hu%E1%BA%BF)_-_img_02.jpg"),
              "cắt ngang 16:7, phủ màu"),
};

// Khoá = mã lĩnh vực (`LINH_VUC` ở `pages.jsx`).
export const ANH_LINH_VUC = {
  foods: anh("lv_foods.jpg", "Ẩm thực — bún bò Huế", "Kham Tran - www.khamtran.com", "CC BY 3.0", commons("Bun-Bo-Hue-from-Huong-Giang-2011.jpg")),
  heritages: anh("lv_heritages.jpg", "Di tích — điện Thái Hòa", "Lưu Ly", "Phạm vi công cộng", commons("Dien_Thai_Hoa.jpg")),
  festivals: LE_HOI,
  performing_arts: anh("lv_performing_arts.jpg", "Nghệ thuật biểu diễn — ca Huế thính phòng", "NguCung12", "CC0",
                       commons("Hue_chamber_music.jpg")),
  travel: anh("lv_travel.jpg", "Đi lại và tham quan — đầm Chuồn, phá Tam Giang", "Tran Trong Nhan", "CC BY-SA 3.0",
              commons("%C4%90%E1%BA%A7m_Chu%E1%BB%93n,_Ph%C3%A1_Tam_Giang_(a_lagoon_in_central_Vietnam),_2019.jpg")),
};

export const MOI_ANH = [ANH_DAU_TRANG.song, ANH_DAU_TRANG.ngoMon, ...Object.values(ANH_LINH_VUC)];
