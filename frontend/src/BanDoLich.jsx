import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { toaDoHopLe } from "./toaDo.js";

// Bản đồ lịch trình (plan `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` §2, §4): ghim có số theo thứ tự trong ngày, dữ liệu do server
// dựng từ bảng (model không tạo toạ độ). File này tải riêng (`lazy` ở `chat.jsx`) ⇒ câu thường không tải Leaflet, không gọi máy chủ tile.
// Không vẽ đường nối (không có đường đi thật); không tải trước vùng / lưu offline (luật dùng tile OSMF).

const TILE = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";  // khớp `TILE_HOST` trong CSP (`backend/api/app.py`)
const GHI_CONG = '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'
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

  useEffect(() => {
    if (!coToaDo.length || !khung.current) return undefined;
    const map = L.map(khung.current, { scrollWheelZoom: false });
    L.tileLayer(TILE, { maxZoom: 18, attribution: GHI_CONG }).addTo(map);
    for (const item of coToaDo) {
      const icon = L.divIcon({ className: `ghim ghim-ngay-${(item.ngay - 1) % 5}`, html: String(item.thu_tu), iconSize: [30, 30] });  // màu theo ngày (đợt 2)
      L.marker(item.toa_do, { icon, title: item.ten, alt: item.ten, keyboard: true }).bindPopup(oGhim(item)).addTo(map);
    }
    map.fitBounds(L.latLngBounds(coToaDo.map(i => i.toa_do)), { padding: [28, 28], maxZoom: 15 });
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
      {coToaDo.length > 0
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
