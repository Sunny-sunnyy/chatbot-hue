import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { toaDoHopLe } from "./toaDo.js";
import { nguonBanDo } from "./nguonBanDo.js";

// Bản đồ lịch trình (plan `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` §2, §4): ghim có số theo thứ tự trong ngày, dữ liệu do server
// dựng từ bảng (model không tạo toạ độ). File này tải riêng (`lazy` ở `chat.jsx`) ⇒ câu thường không tải Leaflet, không gọi máy chủ tile.
// Không vẽ đường nối (không có đường đi thật); không tải trước vùng / lưu offline (luật dùng tile OSMF).

// URL ô + tên nhà cung cấp do server gửi (`nguonBanDo.js`) — cùng một hằng số với CSP `img-src`, nên đổi host không phải sửa file này.
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const ghiCong = n => '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'
  + ` · Ô bản đồ: <a href="${esc(n.trang_nha_cung_cap)}" target="_blank" rel="noopener noreferrer">${esc(n.ten_ngan)}</a>`
  + " · Toạ độ: dữ liệu mở thành phố Huế";
const NHAN_BUOI = { sang: "Sáng", chieu: "Chiều", toi: "Tối" };

function oGhim(item) {
  // dựng bằng DOM + textContent (tên điểm không đi qua HTML)
  const div = document.createElement("div");
  const ten = document.createElement("strong");
  ten.textContent = `${item.thu_tu}. ${item.ten}`;
  const buoi = document.createElement("div");
  buoi.textContent = NHAN_BUOI[item.buoi] ?? "";
  const link = document.createElement("a");
  link.href = item.map_url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = "Mở Google Maps";
  div.append(ten, buoi, link);
  return div;
}

export default function BanDoLich({ items }) {
  const ngays = [...new Set(items.map(i => i.ngay))];
  const [ngay, setNgay] = useState(ngays[0]);
  const cuaNgay = items.filter(i => i.ngay === ngay);
  // review E m-1: số trên ghim đi qua `innerHTML` của Leaflet ⇒ chỉ nhận số nguyên dương (server luôn dựng vậy — kiểm lại như toạ độ)
  const coToaDo = cuaNgay.filter(i => toaDoHopLe(i.toa_do) && Number.isInteger(i.thu_tu) && i.thu_tu > 0);
  const khoa = coToaDo.map(i => `${i.thu_tu}:${i.toa_do}`).join("|");
  const khung = useRef(null);
  const nguon = nguonBanDo();  // chưa có (tải cờ lỗi) ⇒ chỉ danh sách, không khung xám
  const coKhung = coToaDo.length > 0 && !!nguon;

  useEffect(() => {
    if (!coKhung || !khung.current) return undefined;
    // Điện thoại: một ngón vuốt qua khung là CUỘN TRANG (không kéo bản đồ — đo 16/11 khổ 390: vuốt dọc kéo bản đồ 144 px, trang đứng yên);
    // vẫn phóng to / thu nhỏ bằng nút hoặc hai ngón, bấm ghim mở ô tên.
    const map = L.map(khung.current, { scrollWheelZoom: false, dragging: !L.Browser.mobile });
    L.tileLayer(nguon.tile, { maxZoom: 18, attribution: ghiCong(nguon) }).addTo(map);
    // `lech` = số điểm ảnh vẽ ghim lệch sang phải (đổi điểm neo của biểu tượng; toạ độ thật của ghim không đổi)
    const bieuTuong = (item, lech = 0) => L.divIcon({ className: `ghim ghim-ngay-${(item.ngay - 1) % 5}`, html: String(item.thu_tu),  // màu theo ngày (đợt 2)
                                                     iconSize: [30, 30], iconAnchor: [15 - lech, 15] });
    const ghim = coToaDo.map(item => L.marker(item.toa_do, { icon: bieuTuong(item), title: item.ten, alt: item.ten, keyboard: true }).bindPopup(oGhim(item)).addTo(map));
    // Hai điểm cách nhau vài trăm mét (cụm lăng) ở mức phóng xa rơi vào cùng chỗ ⇒ ghim này che số ghim kia. Ghim cách một ghim đã vẽ < 24 px
    // ⇒ vẽ lệch sang phải từng nấc 16 px cho tới khi hết đè; tính lại mỗi lần đổi mức phóng (phóng gần thì tự hết lệch).
    function tachGhim() {
      const daVe = [];
      coToaDo.forEach((item, i) => {
        const p = map.latLngToContainerPoint(item.toa_do);
        let lech = 0;
        while (lech < 96 && daVe.some(q => Math.abs(q.x - (p.x + lech)) < 24 && Math.abs(q.y - p.y) < 24)) lech += 16;
        daVe.push({ x: p.x + lech, y: p.y });
        ghim[i].setIcon(bieuTuong(item, lech));
      });
    }
    map.on("zoomend", tachGhim);
    // Lề dưới rộng hơn: dòng ghi công nằm đè lên mép dưới khung (màn hẹp xuống 2 dòng ≈ 36 px) ⇒ ghim ở mép dưới bị che một phần
    map.fitBounds(L.latLngBounds(coToaDo.map(i => i.toa_do)), { paddingTopLeft: [28, 28], paddingBottomRight: [28, 60], maxZoom: 15 });
    tachGhim();
    return () => map.remove();
  }, [ngay, khoa]);  // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="bd">
      <p className="text-sm font-semibold text-accent-deep">Bản đồ lịch trình</p>
      {ngays.length > 1 && (
        <div className="bd-ngay" role="group" aria-label="Chọn ngày">
          {ngays.map(n => (
            <button key={n} type="button" className="chip chip-sm" aria-pressed={n === ngay} onClick={() => setNgay(n)}>Ngày {n}</button>
          ))}
        </div>
      )}
      {coKhung
        ? <div ref={khung} className="bd-khung" role="region" aria-label={`Bản đồ các điểm ngày ${ngay}`} />
        : <p className="text-sm text-muted">Các điểm ngày này chưa có vị trí trên bản đồ.</p>}
      <ol className="bd-ds">
        {cuaNgay.map(i => (
          <li key={`${i.ngay}-${i.thu_tu}`}>
            <span className="bd-so" aria-hidden="true">{i.thu_tu}</span>
            <a href={i.map_url} target="_blank" rel="noopener noreferrer">{i.ten}</a>
            {!toaDoHopLe(i.toa_do) && <span className="text-muted"> · chưa có trên bản đồ</span>}
          </li>
        ))}
      </ol>
    </div>
  );
}
