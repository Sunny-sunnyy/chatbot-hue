import { useEffect, useState } from "react";
import { HoiPhongNut, linkPhongHopLe, MAP_PREFIX } from "./LichV2.jsx";
import "./co.css";

// Trang "Chỗ ở" (plan 2026-11-15 §1, C): mọi cơ sở của bảng lưu trú theo khu ⇒ mức hạng sao, do server dựng (`/api/cho_o`). Chỉ mở từ ô "Nơi ở" của
// lịch (không có trên thanh trên cùng — User 15/11). Không giá, không "còn phòng"; link chỉ nhận đúng 2 gốc như ô Nơi ở; ảnh chỉ gốc tự host.
const ANH_KS = "/anh/khach_san/";
const anhHopLe = a => typeof a === "string" && a.startsWith(ANH_KS) && a.endsWith(".jpg") && !a.includes("..");

export function ChoO({ khu }) {
  const [du, setDu] = useState(null);
  const [loi, setLoi] = useState(false);
  const [chon, setChon] = useState(khu || null);
  const [muc, setMuc] = useState(null);
  useEffect(() => {
    fetch("/api/cho_o").then(r => (r.ok ? r.json() : Promise.reject(r.status))).then(setDu).catch(() => setLoi(true));
  }, []);
  useEffect(() => setChon(khu || null), [khu]);
  if (loi) return <div className="khung co-than"><p>Chưa tải được danh sách chỗ ở. Thử tải lại trang.</p></div>;
  if (!du) return <div className="khung co-than co-cho" aria-busy="true" />;
  // khu từ link lịch có thể là cả khu ven biển (hai phía) ⇒ khớp đầu mã; mã lạ ⇒ như "Mọi khu" (review E m-2, m-3)
  const khop = n => !!chon && (n.khu === chon || n.khu.startsWith(chon + ":"));
  const coKhop = du.nhom.some(khop);
  const nhom = coKhop ? du.nhom.filter(khop) : du.nhom;
  const tenMuc = [...new Set(du.nhom.flatMap(n => n.muc.map(m => m.ten)))];
  return (
    <div className="khung co-than">
      <p className="vet"><a href="#/len-ke-hoach">Lên kế hoạch</a> / Chỗ ở</p>
      <h1 className="co-h">Chỗ ở theo khu</h1>
      <p className="co-p">Cơ sở lưu trú đã xếp hạng trong danh mục công khai, nhóm theo khu và hạng sao. {du.nhan}</p>
      <div className="co-loc" role="group" aria-label="Khu">
        <button type="button" aria-pressed={!coKhop} onClick={() => setChon(null)}>Mọi khu</button>
        {du.nhom.map(n => <button key={n.khu} type="button" aria-pressed={khop(n)} onClick={() => setChon(n.khu)}>{n.ten}</button>)}
      </div>
      <div className="co-loc" role="group" aria-label="Hạng sao">
        <button type="button" aria-pressed={!muc} onClick={() => setMuc(null)}>Mọi hạng</button>
        {tenMuc.map(t => <button key={t} type="button" aria-pressed={muc === t} onClick={() => setMuc(t)}>{t}</button>)}
      </div>
      {nhom.map(n => (
        <section key={n.khu} className="co-nhom" aria-label={n.ten}>
          <h2>{n.ten}</h2>
          {n.muc.filter(m => !muc || m.ten === muc).map(m => (
            <div key={m.ten} className="co-muc">
              <h3>{m.ten} <small>· {m.co_so.length} cơ sở</small></h3>
              <ul>{m.co_so.map(c => (
                <li key={`${c.ten}|${c.dia_chi}`}>
                  {anhHopLe(c.anh) ? <img src={`${import.meta.env.BASE_URL}${c.anh.slice(1)}`} alt={c.ten} loading="lazy" decoding="async" />
                    : <span className="co-khong-anh" aria-hidden="true" />}
                  <span className="co-ten">{c.ten}</span>
                  <small>{c.xep_hang}</small>
                  {c.dia_chi && <span className="co-dc">{c.dia_chi}</span>}
                  <span className="co-link">
                    {typeof c.map_url === "string" && c.map_url.startsWith(MAP_PREFIX) &&
                      <a href={c.map_url} target="_blank" rel="noopener noreferrer">Bản đồ</a>}
                    {c.deep_links
                      ? [["booking", "Booking"], ["agoda", "Agoda"], ["traveloka", "Traveloka"]].map(([k, nhan]) => (
                          linkPhongHopLe(c.deep_links[k]) &&
                          <a key={k} href={c.deep_links[k]} target="_blank" rel="noopener noreferrer">{nhan}</a>
                        ))
                      : linkPhongHopLe(c.link) && <a href={c.link} target="_blank" rel="noopener noreferrer">Tìm phòng</a>}
                    {c.mau_hoi_phong && <HoiPhongNut mau={c.mau_hoi_phong} />}
                  </span>
                </li>
              ))}</ul>
            </div>
          ))}
        </section>
      ))}
      <p className="co-nguon">Nguồn: {du.nguon}.</p>
    </div>
  );
}
