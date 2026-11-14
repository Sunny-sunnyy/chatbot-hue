// Ảnh theo mã bài cho Khám phá (sinh bằng data/anh_kham_pha_2026-11-14/tools/dung_anh_bai_js.py — không sửa tay).
// v1: 24 ảnh điểm lịch (Wikimedia Commons, người đã nhìn kiểm) ⇒ public/anh/<anh>.jpg; bài không có dòng ⇒ ô màu theo lĩnh vực, không ảnh thay.
// Khoá = mã băm của mã bài (không ghi đường dẫn file kho vào repo public).
export function khoaBai(id) {
  let h = 0;
  for (const c of id) h = (h * 31 + c.codePointAt(0)) >>> 0;
  return `k${h.toString(36)}`;
}

const ANH = {
  km7im9e: {"ten": "Đại Nội Huế", "anh": "lich/dai_noi", "tacGia": "Lưu Ly", "giayPhep": "Phạm vi công cộng", "trang": "https://commons.wikimedia.org/wiki/File:Dien_Thai_Hoa.jpg", "doi": "thu nhỏ"},
  krxq1kw: {"ten": "Kinh thành Huế (Ngọ Môn – Kỳ Đài)", "anh": "lich/kinh_thanh", "tacGia": "Chainwit", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Hu%E1%BA%BF_(2024)_-_Meridian_Gate_-_Ng%E1%BB%8D_M%C3%B4n_(Ho%C3%A0ng_th%C3%A0nh_Hu%E1%BA%BF)_-_img_02.jpg", "doi": "thu nhỏ"},
  k1l90tqr: {"ten": "Chợ Đông Ba", "anh": "lich/cho_dong_ba", "tacGia": "Chainwit", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Dong_Ba_Market_(Hue)_-_Ch%E1%BB%A3_%C4%90%C3%B4ng_Ba_Hu%E1%BA%BF_(July_2024)_-_img_02.jpg", "doi": "thu nhỏ"},
  kfpe8h5: {"ten": "Phố cổ và chợ Bao Vinh", "anh": "lich/bao_vinh", "tacGia": "Sgnpkd", "giayPhep": "CC BY-SA 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Bao_Vinh_street.jpg", "doi": "thu nhỏ"},
  k8o6w0o: {"ten": "Trường Quốc Học Huế", "anh": "lich/quoc_hoc", "tacGia": "Chainwit", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Qu%E1%BB%91c_H%E1%BB%8Dc_%E2%80%93_Hu%E1%BA%BF_High_School_for_the_Gifted_(entrance)_(2024)_-_img_01.jpg", "doi": "thu nhỏ"},
  k18xozml: {"ten": "Cung An Định", "anh": "lich/cung_an_dinh", "tacGia": "Chainwit", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:An_Dinh_Palace_-_Cung_An_%C4%90%E1%BB%8Bnh_(2024)_-_front_facade_-_img_04.jpg", "doi": "thu nhỏ, cắt dải đáy"},
  kdbj9dk: {"ten": "Đàn Nam Giao", "anh": "lich/dan_nam_giao", "tacGia": "Lưu Ly", "giayPhep": "Phạm vi công cộng", "trang": "https://commons.wikimedia.org/wiki/File:Dan_Nam_Giao_Hue.jpg", "doi": "thu nhỏ"},
  kts4jys: {"ten": "Lăng Dục Đức", "anh": "lich/lang_duc_duc", "tacGia": "Lưu Ly", "giayPhep": "CC BY-SA 3.0", "trang": "https://commons.wikimedia.org/wiki/File:Cong_An_lang.jpg", "doi": "thu nhỏ"},
  kzmjfc8: {"ten": "Núi Ngự Bình", "anh": "lich/nui_ngu_binh", "tacGia": "Lưu Ly", "giayPhep": "CC BY 3.0", "trang": "https://commons.wikimedia.org/wiki/File:Nui_Ngu_Binh.jpg", "doi": "thu nhỏ"},
  kpvqmn7: {"ten": "Lăng Tự Đức", "anh": "lich/lang_tu_duc", "tacGia": "CEphoto, Uwe Aranas", "giayPhep": "CC BY-SA 3.0", "trang": "https://commons.wikimedia.org/wiki/File:Hue_Vietnam_Tomb-of-Emperor-Tu-Duc-03.jpg", "doi": "thu nhỏ"},
  k1uohksw: {"ten": "Lăng Đồng Khánh", "anh": "lich/lang_dong_khanh", "tacGia": "Chainwit", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Mausoleum_of_Emperor_Dong_Khanh_(Hue)_-_L%C4%83ng_%C4%90%E1%BB%93ng_Kh%C3%A1nh_(2024_July)_-_img_05.jpg", "doi": "thu nhỏ"},
  k1tlvemo: {"ten": "Lăng Thiệu Trị", "anh": "lich/lang_thieu_tri", "tacGia": "Lưu Ly", "giayPhep": "Phạm vi công cộng", "trang": "https://commons.wikimedia.org/wiki/File:Tomb_of_ThieuTri.jpg", "doi": "thu nhỏ"},
  kcm3u3y: {"ten": "Lăng Khải Định", "anh": "lich/lang_khai_dinh", "tacGia": "Chainwit", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Hu%E1%BA%BF_(2024)_-_Mausoleum_of_Emperor_Kh%E1%BA%A3i_%C4%90%E1%BB%8Bnh_-_exterior_-_img_01.jpg", "doi": "thu nhỏ"},
  k1xfvkch: {"ten": "Hổ Quyền", "anh": "lich/ho_quyen", "tacGia": "Lưu Ly", "giayPhep": "Phạm vi công cộng", "trang": "https://commons.wikimedia.org/wiki/File:H%E1%BB%95_Quy%E1%BB%81n_1.jpg", "doi": "thu nhỏ"},
  k17isa4o: {"ten": "Chùa Thiên Mụ", "anh": "lich/chua_thien_mu", "tacGia": "CEphoto, Uwe Aranas", "giayPhep": "CC BY-SA 3.0", "trang": "https://commons.wikimedia.org/wiki/File:Hue_Vietnam_Thien-Mu-Temple-and-Pagoda-01.jpg", "doi": "thu nhỏ"},
  k1kb4n84: {"ten": "Điện Hòn Chén", "anh": "lich/dien_hon_chen", "tacGia": "Lưu Ly", "giayPhep": "Phạm vi công cộng", "trang": "https://commons.wikimedia.org/wiki/File:%C4%90i%E1%BB%87n_H%C3%B2n_Ch%C3%A9n1.jpg", "doi": "thu nhỏ"},
  kyebart: {"ten": "Lăng Minh Mạng", "anh": "lich/lang_minh_mang", "tacGia": "CEphoto, Uwe Aranas", "giayPhep": "CC BY-SA 3.0", "trang": "https://commons.wikimedia.org/wiki/File:Hue_Vietnam_Tomb-of-Emperor-Minh-Mang-04.jpg", "doi": "thu nhỏ"},
  kaet2a5: {"ten": "Lăng Gia Long", "anh": "lich/lang_gia_long", "tacGia": "CEphoto, Uwe Aranas", "giayPhep": "CC BY-SA 3.0", "trang": "https://commons.wikimedia.org/wiki/File:Hue_Vietnam_Tomb-of-Emperor-Gia-Long-01.jpg", "doi": "thu nhỏ"},
  k10lyu0i: {"ten": "Đầm Chuồn", "anh": "lich/dam_chuon", "tacGia": "Tran Trong Nhan", "giayPhep": "CC BY-SA 3.0", "trang": "https://commons.wikimedia.org/wiki/File:%C4%90%E1%BA%A7m_Chu%E1%BB%93n,_Ph%C3%A1_Tam_Giang_(a_lagoon_in_central_Vietnam),_2019.jpg", "doi": "thu nhỏ"},
  k1ujnt82: {"ten": "Phá Tam Giang", "anh": "lich/pha_tam_giang", "tacGia": "Christophe95", "giayPhep": "CC BY-SA 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Aerial_view_of_the_Tam_Giang_Lagoon.jpg", "doi": "thu nhỏ"},
  k1cnaniv: {"ten": "Vườn quốc gia Bạch Mã", "anh": "lich/bach_ma", "tacGia": "Andre Hospers", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Bach_Ma_Natinal_Park_Franse_villa.jpg", "doi": "thu nhỏ"},
  khmz27a: {"ten": "Bảo tàng Cổ vật Cung đình Huế", "anh": "lich/bao_tang_co_vat", "tacGia": "Gin The Wanderer", "giayPhep": "CC BY 2.0", "trang": "https://commons.wikimedia.org/wiki/File:B%E1%BA%A3o_t%C3%A0ng_C%E1%BB%95_v%E1%BA%ADt_Cung_%C4%91%C3%ACnh_Hu%E1%BA%BF_(15245479432).jpg", "doi": "thu nhỏ"},
  k12nk5w2: {"ten": "Duyệt Thị Đường", "anh": "lich/duyet_thi_duong", "tacGia": "Francisco Anzola", "giayPhep": "CC BY 2.0", "trang": "https://commons.wikimedia.org/wiki/File:Duy%E1%BB%87t_Th%E1%BB%8B_%C4%90%C6%B0%E1%BB%9Dng_(ho%C3%A0ng_th%C3%A0nh_Hu%E1%BA%BF).jpg", "doi": "thu nhỏ"},
  k1966825: {"ten": "Ca Huế trên sông Hương", "anh": "lich/ca_hue_song_huong", "tacGia": "P. Hughes", "giayPhep": "CC BY 4.0", "trang": "https://commons.wikimedia.org/wiki/File:Hu%E1%BA%BF_-_Vietnamese_dragon_boat_operating_as_a_tourist_vessel_on_the_Perfume_River.jpg", "doi": "thu nhỏ"},
};

export const anhCuaBai = id => ANH[khoaBai(id)] ?? null;
export const MOI_ANH_BAI = Object.values(ANH);
