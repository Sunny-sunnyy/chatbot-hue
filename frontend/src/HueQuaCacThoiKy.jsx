import { useEffect, useRef, useState } from "react";
import "./hue_thoi_ky.css";

// Màn cuộn kể chuyện "Huế qua các thời kỳ" (B, 14/11/2026; User chọn làm). Sáu mốc, chữ viết lại từ bài trong kho — bảng căn cứ (bài + dòng)
// ở data/hue_thoi_ky_2026-11-14/can_cu.json (private: file tracked không ghi đường dẫn kho). Ảnh lấy từ bộ ảnh lịch có sẵn (public/anh/lich/);
// không hiện ghi công (User 14/11), nguồn ảnh nằm trong bảng ảnh. Màn rộng: ảnh ghim bên trái (CSS sticky) đổi theo mốc đang đọc; màn hẹp: mỗi
// mốc ảnh trên chữ dưới, không ghim. Không tự có lề trang: đặt trong một khối .khung (vd .gt-than của Giới thiệu). Chuyển động chỉ dưới <html class="hieu-ung"> (máy giảm chuyển động ⇒ hiện đủ, không mờ chéo).
const ANH = `${import.meta.env.BASE_URL}anh/lich/`;

export const MOC = [
  { id: "thuan_hoa", nam: "1306", ten: "Vùng đất Thuận Hóa", anh: "pha_tam_giang", alt: "Phá Tam Giang nhìn từ trên cao",
    chu: "Vùng đất Huế xưa thuộc châu Ô và châu Lý. Năm 1306, dưới thời vua Trần Anh Tông, hai châu nhập vào Đại Việt "
       + "và được đổi tên là Thuận Hóa." },
  { id: "chua_nguyen", nam: "1601 – 1774", ten: "Đất của các chúa Nguyễn", anh: "chua_thien_mu", alt: "Chùa Thiên Mụ bên sông Hương",
    chu: "Năm 1601, chúa Tiên Nguyễn Hoàng cho dựng chùa Thiên Mụ. Các chúa Nguyễn đặt thủ phủ ở Kim Long năm 1636, tới năm 1687 thì dời "
       + "về Phú Xuân, nơi làm thủ phủ xứ Đàng Trong hơn một thế kỷ." },
  { id: "tay_son", nam: "1788", ten: "Quang Trung lên ngôi", anh: "dan_nam_giao", alt: "Đàn Nam Giao",
    chu: "Cuối năm 1788, Nguyễn Huệ cho dựng đàn tế trên núi Bân, gần núi Ngự Bình, và lên ngôi hoàng đế, lấy niên hiệu Quang Trung, rồi "
       + "tiến quân ra Bắc đánh quân Thanh. Phú Xuân trở thành kinh đô của nhà Tây Sơn." },
  { id: "kinh_do_nguyen", nam: "1802 – 1945", ten: "Kinh đô của nhà Nguyễn", anh: "kinh_thanh", alt: "Kinh thành Huế",
    chu: "Năm 1802, vua Gia Long chọn Phú Xuân làm kinh đô, và Huế giữ vai trò này trong 143 năm. Kinh thành được khởi công năm 1805. "
       + "Tới năm 1832, dưới thời vua Minh Mạng, công trình cơ bản hoàn thành, tường đất được ốp gạch vồ và đá." },
  { id: "dong_tay", nam: "1884 – 1945", ten: "Gặp gỡ Đông – Tây", anh: "lang_khai_dinh", alt: "Lăng Khải Định",
    chu: "Thời Pháp thuộc, công trình cung đình bắt đầu dùng vật liệu và kiểu dáng phương Tây, tiêu biểu là lăng Khải Định, xây từ 1920 "
       + "tới 1931. Ngày 30/08/1945, vua Bảo Đại, vị vua cuối cùng của nhà Nguyễn, làm lễ thoái vị tại Ngọ Môn." },
  { id: "di_san", nam: "1993 – nay", ten: "Di sản của thế giới", anh: "dai_noi", alt: "Đại Nội Huế",
    chu: "Chiến tranh để lại nhiều cung điện đổ nát. Ngày 11/12/1993, UNESCO ghi danh các di tích của Cố đô vào danh mục di sản thế giới, "
       + "lần đầu Việt Nam có một di sản như vậy. Năm 2003 tới lượt Nhã nhạc cung đình. Điện Thái Hòa trùng tu xong năm 2024, và từ "
       + "01/01/2025 Huế là thành phố trực thuộc Trung ương." },
];

export function HueQuaCacThoiKy() {
  const [dang, setDang] = useState(0);
  const buoc = useRef([]);
  // Mốc đang đọc = mốc cắt dải giữa màn hình (IntersectionObserver, không nghe sự kiện cuộn).
  useEffect(() => {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) setDang(Number(e.target.dataset.i)); }),
      { rootMargin: "-45% 0px -45% 0px" });
    buoc.current.forEach(el => el && io.observe(el));
    return () => io.disconnect();
  }, []);
  return (
    <section className="tk" aria-labelledby="tk-h">
      <div>
        <h2 id="tk-h" className="khoi-h">Huế qua các thời kỳ</h2>
        <p className="tk-phu">Sáu mốc, từ vùng đất Thuận Hóa tới thành phố di sản hôm nay.</p>
        <div className="tk-cot">
          <div className="tk-ghim" aria-hidden="true">
            <div className="tk-khung-anh">
              {MOC.map((m, i) => <img key={m.id} src={`${ANH}${m.anh}.jpg`} alt="" loading="lazy" decoding="async" className={i === dang ? "tk-anh-dang" : ""} />)}
              <span className="tk-nam-lon">{MOC[dang].nam}</span>
            </div>
            <div className="tk-tien"><i style={{ transform: `scaleX(${(dang + 1) / MOC.length})` }} /></div>
          </div>
          <ol className="tk-moc">
            {MOC.map((m, i) => (
              <li key={m.id} ref={el => { buoc.current[i] = el; }} data-i={i} className={`tk-buoc hien${i === dang ? " tk-dang" : ""}`}>
                <img className="tk-anh-nho" src={`${ANH}${m.anh}.jpg`} alt={m.alt} loading="lazy" decoding="async" />
                <p className="tk-nam">{m.nam}</p>
                <h3>{m.ten}</h3>
                <p>{m.chu}</p>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  );
}
