import { useEffect } from "react";
import { ANH_DAU_TRANG } from "./anh.js";
import { Anh } from "./chung.jsx";
import { HueQuaCacThoiKy } from "./HueQuaCacThoiKy.jsx";
import "./gt.css";

// Giới thiệu theo H1 "Sông Hương" (rút gọn theo góc nhìn người dùng, 25/11/2026).
// Các thẻ "Trợ lý làm được gì" và câu dữ liệu ảnh hiện theo cờ server (`/api/tinh_nang`).

const IC = {
  hoi: "M4 5h16v11H9l-5 4zM8 9h8M8 12h5",
  lich: "M4 5h16v15H4zM4 10h16M9 3v4M15 3v4M8 14h3M8 17h6",
  web: "M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16zM4 12h16M12 4c3 3 3 13 0 16M12 4c-3 3-3 13 0 16",
  anh: "M4 8h3l2-3h6l2 3h3v11H4zM12 16.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z",
  troi: "M7 17h10a4 4 0 0 0 .6-7.96A6 6 0 0 0 6.1 10 3.5 3.5 0 0 0 7 17zM9 20l-1 2M13 20l-1 2M17 20l-1 2",
  soTay: "M6 4h12v16H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM9 8h6M9 12h6M9 16h4",
  hoSo: "M4 6h5l2 2h9v11H4V6zM8 12h8M8 15h5",
};

function Ic({ d }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={d} />
    </svg>
  );
}

export function GioiThieu({ tinhNang, daCo, muc }) {
  const anh = !!tinhNang?.anh;
  const moHinh = tinhNang?.mo_hinh;  // tên nơi nhận câu hỏi do server gửi theo model ĐANG CHẠY; chưa có ⇒ câu không nêu tên (không ghi cứng tên hãng ở đây)
  // `#/gioi-thieu/<mục>` ⇒ cuộn tới mục có id đó (sau lần `scrollTo(0, 0)` của `useRoute` lúc đổi hash).
  // chưa biết cờ ⇒ chưa vẽ thân trang (thẻ "làm được gì" theo cờ nở ra lúc cờ về ⇒ đẩy cả trang: CLS 0,17–0,66 đo ở 390, 14/11) và chưa cuộn
  useEffect(() => {
    if (!muc || !daCo) return;
    const el = document.getElementById(muc);
    // cuộn sau khi font đã tải: cuộn sớm thì chữ phía trên đổi cỡ lúc font về ⇒ vùng đang xem bị đẩy (CLS 0,6 đo được trên bản build)
    let huy = false;
    document.fonts.ready.then(() => requestAnimationFrame(() => { if (!huy) el?.scrollIntoView(); }));
    return () => { huy = true; };
  }, [muc, daCo]);
  const lam = [
    [IC.hoi, "Hỏi về Huế", "Món ăn, di tích, lễ hội, nghệ thuật biểu diễn, đi lại và vé tham quan — trả lời bằng tiếng Việt, kèm nguồn."],
    // mỗi dòng theo cờ server như bản cũ (review E M-2): tính năng tắt thì không hứa
    ...(tinhNang?.lich_trinh_bieu_mau ? [[IC.lich, "Lên kế hoạch", "Chọn số ngày, người đi cùng, sở thích; trợ lý xếp lịch theo buổi từ các điểm có trong kho."
      // .ics nằm trong lịch bản 2 (`LichV2.jsx`) ⇒ chỉ hứa khi server bật lịch bản 2
      + (tinhNang?.len_ke_hoach_v2 ? " Đã chọn ngày đi thì tải lịch về lịch điện thoại (.ics)." : "")]] : []),
    ...(tinhNang?.tra_web ? [[IC.web, "Tra thêm trên web", "Khi kho không có, trợ lý tra web một lần và để riêng phần đó dưới nhãn “Từ web (chưa kiểm)”."]] : []),
    ...(tinhNang?.thoi_tiet ? [[IC.troi, "Thời tiết Huế", "Thời tiết hôm nay ở trang chủ; hỏi trợ lý “mai trời thế nào” để có dự báo tới 7 ngày, kèm nguồn."]] : []),
    ...(anh ? [[IC.anh, "Hỏi bằng ảnh", "Gửi ảnh kèm câu hỏi; trợ lý đoán nơi hoặc món trong ảnh (có thể sai) rồi trả lời ngay từ kho; đoán chưa đúng thì bấm “Hỏi lại với” tên khác dưới câu trả lời, hoặc tự gõ tên."]] : []),
    ...(tinhNang?.so_tay ? [[IC.soTay, "Sổ tay cho chuyến đi", "Tổng hợp lịch trình bạn đã lập thành cuốn sổ tay gọn gàng: điểm nên xem, giờ mở cửa, giá vé và lưu ý cần nhớ, in hoặc lưu PDF được."]] : []),
    ...(tinhNang?.ho_so_chu_de ? [[IC.hoSo, "Hồ sơ theo chủ đề", "Đọc tóm tắt theo từng chủ đề văn hoá – du lịch Huế tổng hợp từ nhiều bài viết, kèm lưu ý an toàn và đường dẫn về bài gốc."]] : []),
  ];
  return (
    <>
      <section className="gt-dau" aria-labelledby="gt-h">
        <div className="gt-nen troi-cuon"><Anh a={ANH_DAU_TRANG.song} className="anh-troi" /></div>
        <div className="khung gt-dau-in">
          <p className="vet vao" style={{ "--n": 0 }}><a href="#/">Trang chủ</a> / Giới thiệu</p>
          <h1 id="gt-h" className="gt-h vao" style={{ "--n": 1 }}>Về Trợ lý Huế</h1>
          <p className="gt-dan vao" style={{ "--n": 2 }}>
            Người bạn đồng hành tra sổ tay về Huế: hỏi gì cũng trả lời từ kho tư liệu đã biên soạn, và chỉ cho bạn chỗ lấy thông tin.
          </p>
        </div>
      </section>

      {!daCo ? <div className="gt-cho" /> : <div className="khung gt-than">
        <section className="gt-khoi" aria-labelledby="gt-lam">
          <h2 id="gt-lam" className="khoi-h">Trợ lý làm được gì</h2>
          <ul className="gt-lam">
            {lam.map(([d, t, m], i) => (
              <li key={t} className="gt-the nang hien" style={{ "--n": i }}>
                <span className="gt-ic"><Ic d={d} /></span><h3>{t}</h3><p>{m}</p>
              </li>
            ))}
          </ul>
        </section>

        <HueQuaCacThoiKy />

        <section className="gt-khoi" aria-labelledby="gt-luu-y">
          <div className="gt-gioi-han hien">
            <h2 id="gt-luu-y" className="gt-h2">Lưu ý khi dùng</h2>
            <ul>
              <li>Trợ lý có thể sai — giờ mở cửa, giá vé và lịch lễ hội có thể đã thay đổi, bạn nên kiểm tra lại trước khi đi.</li>
              <li>Trợ lý chỉ tư vấn thông tin về văn hoá, du lịch Huế và chưa hỗ trợ đặt phòng hay mua vé trực tiếp.</li>
              <li>Không nhập thông tin cá nhân nhạy cảm; {anh ? "câu hỏi và ảnh" : "câu hỏi"} bạn gửi được chuyển tới dịch vụ AI bên ngoài{moHinh ? ` (${moHinh})` : ""} để xử lý, không lưu tài khoản hay lịch sử lâu dài.</li>
            </ul>
          </div>
        </section>
      </div>}
    </>
  );
}
