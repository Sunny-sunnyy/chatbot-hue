import { ANH_LINH_VUC, MAN_NHO } from "./anh.js";

// Phần dùng chung của các trang cổng (tách từ pages.jsx — đợt 0 giao diện H1, 14/11/2026; hành vi giữ nguyên).
// Các trang của cổng đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` D9–D12), bản mẫu 2 "Sông Hương".
// Thẻ bài chỉ hiện trường kho có (tên, loại, tóm tắt) — không sao, không "Liên hệ", không giờ / giá chung chung (D10). Ảnh (User chốt 07/11):
// chỉ 2 ảnh đầu trang + 5 ô lĩnh vực (`anh.js`); thẻ bài / trang bài giữ khối hoa văn.

// 5 lĩnh vực kho (mã = tên thư mục); thứ tự như bản mẫu.
export const LINH_VUC = [
  { id: "foods", ten: "Ẩm thực", mo: "Món Huế, quán ăn, cà phê, đặc sản" },
  { id: "heritages", ten: "Di tích", mo: "Kinh thành, lăng tẩm, chùa, di sản" },
  { id: "festivals", ten: "Lễ hội", mo: "Lễ cung đình, lễ dân gian, Festival" },
  { id: "performing_arts", ten: "Nghệ thuật biểu diễn", mo: "Nhã nhạc, ca Huế, tuồng" },
  { id: "travel", ten: "Đi lại và tham quan", mo: "Điểm đến, vé tham quan, dịch vụ" },
];
export const LOAI_CON = { restaurants: "Quán ăn", cafes: "Quán cà phê", local_specialties: "Đặc sản", heritage: "Di tích", festival: "Lễ hội",
                   arts: "Loại hình nghệ thuật", places: "Điểm đến", tickets: "Vé tham quan", services: "Dịch vụ" };
export const TRANG = 12;  // số thẻ mỗi lần "Xem thêm"
export const TONG_QUAN = "_tong_quan";  // bài nằm ngay gốc lĩnh vực (`loai_con` null) — khác "chưa lọc" (null)
export const loaiCua = b => b.loai_con ?? TONG_QUAN;

// Câu gợi ý ở trang chủ: câu tự viết đã có ở giao diện trước (kiểm có trong kho bằng `scripts/grep_kb.sh`) — không câu Golden / kín (D9).
export const GOI_Y = ["Ăn sáng ở Huế nên thử món gì?", "Chỉ có nửa ngày thì nên đi lăng nào?", "Lễ hội Điện Huệ Nam diễn ra khi nào?",
                      "Nghe ca Huế trên sông ở đâu?", "Từ sân bay vào trung tâm bằng gì?"];

// Biểu mẫu "Lên kế hoạch" (D3): giá trị = đúng tập `TruongInput` của server (`backend/llm/hoi_lai.py`); "kiểu đi" ẩn ở đợt 1 (Q-U3).
export const BIEU_MAU = [
  { ten: "so_ngay", nhan: "Mấy ngày", bat_buoc: true,
    chon: [["1", "1 ngày"], ["2", "2 ngày"], ["3", "3 ngày"], ["4+", "Từ 4 ngày"]] },
  { ten: "di_cung", nhan: "Đi cùng ai",
    chon: [["mot_minh", "Một mình"], ["cap_doi", "Cặp đôi"], ["gia_dinh_tre_em", "Gia đình có trẻ em"], ["nguoi_lon_tuoi", "Có người lớn tuổi"],
           ["nhom_ban", "Nhóm bạn"]] },
  { ten: "so_thich", nhan: "Thích gì",
    chon: [["di_tich", "Di tích"], ["am_thuc", "Ẩm thực"], ["thien_nhien", "Thiên nhiên"], ["le_hoi_nghe_thuat", "Lễ hội, nghệ thuật"],
           ["chup_anh", "Chụp ảnh"]] },
];
export const CAU_BIEU_MAU = "Lên kế hoạch tham quan Huế";  // chỉ để in lại trong khung trò chuyện — server dựng câu từ giá trị nút

// Ảnh có bản nhỏ cho điện thoại: `<source media>` chọn theo khổ màn (không theo mật độ điểm ảnh như `srcset`) ⇒ máy ≤ 760 px luôn tải bản nhỏ.
export function Anh({ a, ...props }) {
  return (
    <picture>
      <source media={MAN_NHO} srcSet={a.srcNho} />
      <img src={a.src} alt="" {...props} />
    </picture>
  );
}

export function Song({ className }) {
  return (
    <svg className={className} viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 150 C 240 110, 480 190, 720 150 S 1200 110, 1440 150 L1440 220 L0 220 Z" fill="#0E6B66" opacity=".35" />
      <path d="M0 175 C 260 140, 500 210, 760 175 S 1220 140, 1440 178 L1440 220 L0 220 Z" fill="#0E6B66" opacity=".55" />
      <path d="M0 200 C 280 175, 520 225, 800 200 S 1240 178, 1440 202 L1440 220 L0 220 Z" fill="#EDF4F2" />
    </svg>
  );
}

export function soBai(bai, linhVuc) {
  return bai ? bai.filter(b => b.linh_vuc === linhVuc).length : null;
}

export function O5LinhVuc({ bai }) {
  return (
    <div className="kp-ds">
      {LINH_VUC.map(lv => (
        <a key={lv.id} className="kp" href={`#/kham-pha/${lv.id}`}>
          <Anh a={ANH_LINH_VUC[lv.id]} className="kp-anh" loading="lazy" />
          <span className="kp-ten">{lv.ten}</span>
          <span className="kp-mo">{lv.mo}</span>
          {soBai(bai, lv.id) != null && <span className="kp-so">{soBai(bai, lv.id)} bài</span>}
        </a>
      ))}
    </div>
  );
}
