import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { toaDoHopLe } from "./toaDo.js";
import { nguonBanDo } from "./nguonBanDo.js";
import { TUY_CHON_BAN_DO } from "./BanDoLich.jsx";
import { BIEU_MAU } from "./chung.jsx";
import "./co.css";

// Trang "Bản đồ" (menu cổng mức 2 — chủ dự án 06/11; plan `report_agent/2026-11-20/e_trang_ban_do_plan.md`): ghim của mọi điểm tham quan trong bảng điểm
// lịch có toạ độ (`/api/ban_do`, server dựng từ bảng — model không tạo toạ độ), lọc theo loại. File tải riêng (`lazy` ở `App.jsx`) ⇒ trang khác không
// tải Leaflet. Không quán / chỗ ở, không vị trí người dùng, không đường đi (plan mục 2). Nguồn ô + dòng ghi công bản đồ: như bản đồ lịch (`BanDoLich.jsx`).
const LOAI = BIEU_MAU.find(t => t.ten === "so_thich").chon;  // [mã, nhãn] — cùng nhãn với ô "Thích gì" của trang Lên kế hoạch

function oGhim(d) {
  // dựng bằng DOM + textContent (tên điểm không đi qua HTML)
  const div = document.createElement("div");
  const ten = document.createElement("strong");
  ten.textContent = d.ten;
  const loai = document.createElement("div");
  loai.textContent = LOAI.filter(([ma]) => d.loai.includes(ma)).map(([, nhan]) => nhan).join(" · ");
  const link = document.createElement("a");
  link.href = d.map_url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = "Mở Google Maps";
  div.append(ten, loai, link);
  return div;
}

export default function TrangBanDo() {
  const [diem, setDiem] = useState(null);
  const [loi, setLoi] = useState(false);
  const [loai, setLoai] = useState(null);
  const khung = useRef(null);
  const nguon = nguonBanDo();  // chưa có (tải cờ lỗi) ⇒ chỉ danh sách, không khung xám
  useEffect(() => {
    fetch("/api/ban_do").then(r => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(d => setDiem(d.diem.filter(x => toaDoHopLe(x.toa_do)))).catch(() => setLoi(true));
  }, []);
  const hien = (diem || []).filter(d => !loai || d.loai.includes(loai));
  const khoa = hien.map(d => d.ten).join("|");

  useEffect(() => {
    if (!nguon || !khung.current || hien.length === 0) return undefined;
    // Điện thoại: một ngón vuốt qua khung là cuộn trang, như bản đồ lịch (đo 16/11 khổ 390); phóng to / thu nhỏ bằng nút hoặc hai ngón
    const map = L.map(khung.current, TUY_CHON_BAN_DO);
    L.tileLayer(nguon.tile, { maxZoom: 18 }).addTo(map);
    const bieuTuong = L.divIcon({ className: "ghim ghim-diem", html: "", iconSize: [18, 18], iconAnchor: [9, 9] });
    hien.forEach(d => L.marker(d.toa_do, { icon: bieuTuong, title: d.ten, alt: d.ten, keyboard: true }).bindPopup(oGhim(d)).addTo(map));
    map.fitBounds(L.latLngBounds(hien.map(d => d.toa_do)), { paddingTopLeft: [28, 28], paddingBottomRight: [28, 60], maxZoom: 15 });
    return () => map.remove();
  }, [khoa, !!nguon]);  // eslint-disable-line react-hooks/exhaustive-deps

  if (loi) return <div className="khung co-than"><p>Chưa tải được bản đồ. Thử tải lại trang.</p></div>;
  if (!diem) return <div className="khung co-than co-cho" aria-busy="true" />;
  return (
    <div className="khung co-than bd-trang">
      <h1 className="co-h">Bản đồ điểm tham quan</h1>
      <p className="co-p">{diem.length} điểm tham quan ở Huế mà trang Lên kế hoạch dùng để xếp lịch. Bấm một dấu tròn để xem tên và mở Google Maps.</p>
      <div className="co-loc" role="group" aria-label="Loại điểm">
        <button type="button" aria-pressed={!loai} onClick={() => setLoai(null)}>Tất cả ({diem.length})</button>
        {LOAI.map(([ma, nhan]) => {
          const n = diem.filter(d => d.loai.includes(ma)).length;
          return n > 0 && <button key={ma} type="button" aria-pressed={loai === ma} onClick={() => setLoai(ma)}>{nhan} ({n})</button>;
        })}
      </div>
      {nguon
        ? <div ref={khung} className="bd-khung" role="region" aria-label={`Bản đồ ${hien.length} điểm tham quan`} />
        : <p className="co-p">Chưa tải được ô bản đồ — danh sách các điểm ở dưới vẫn dùng được.</p>}
      <ol className="bd-ds bd-trang-ds">
        {hien.map(d => <li key={d.ten}><a href={d.map_url} target="_blank" rel="noopener noreferrer">{d.ten}</a></li>)}
      </ol>
    </div>
  );
}
