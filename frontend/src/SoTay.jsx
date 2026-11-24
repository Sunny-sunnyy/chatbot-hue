import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { anhHopLe } from "./LichV2.jsx";
import { SourceLine } from "./SourceLine.jsx";
import { baiHref } from "./route.js";
import { createSseParser } from "./stream.js";
import { linhVuc } from "./song/nhin.js";
import "./so_tay.css";

// BẢN THỬ (nhánh `thu-c-so-tay`, công tắc server `so_tay` mặc định TẮT; chủ dự án 21:21 24/11/2026: "làm cả hai kiểu", sổ tay trước; "giao diện đẹp
// mắt, thu hút, hiện đại, sinh động"). Trang `#/so-tay`: một SỔ TAY cho chuyến đi, dựng từ lịch đang lưu của cuộc trò chuyện — mỗi điểm của lịch một
// mục (dữ kiện chép từ kho + "nên xem" + "lưu ý"), ăn uống từng ngày, "trước khi đi". Chữ và nguồn do server gửi (lõi của B, `POST /api/so_tay`);
// trang chỉ vẽ. Hợp đồng sự kiện SSE (B chốt 24/11): `dan_y` {tieu_de, so_ngay, muc: [{id, loai, ngay, buoi, ten, gio, bai_id, anh}]} có ngay ⇒ nhiều
// `muc` {id, trang_thai, doan: [{nhan, kieu: van | gach | thieu | an_toan, chu, gach}], nguon} về KHÔNG theo thứ tự ⇒ `xong` {giay, so_muc, so_muc_loi}.
// Nguồn đánh số TRONG từng mục (như một câu trả lời của trợ lý) ⇒ số không nhảy khi mục khác về sau.

const KHONG_CO_LICH = "khong_co_lich";
const BAN_DAU = { pha: "chua", danY: null, muc: {}, xong: null, loi: null };

// Trạng thái sổ tay sống ở App ⇒ rời trang rồi quay lại vẫn còn; bấm nút ở thẻ lịch thì dựng lại (lịch có thể vừa được sửa).
export function useSoTay() {
  const [st, setSt] = useState(BAN_DAU);
  const huy = useRef(null);
  const tao = useCallback(async () => {
    huy.current?.abort();
    const dk = new AbortController();
    huy.current = dk;
    setSt({ ...BAN_DAU, pha: "dang" });
    const loi = (ma, cau) => setSt(s => ({ ...s, pha: "loi", loi: { ma, cau } }));
    try {
      const r = await fetch("/api/so_tay", { method: "POST", credentials: "same-origin", signal: dk.signal });
      if (!r.ok) {
        const than = await r.json().catch(() => null);
        return loi(than?.error?.code || String(r.status), than?.error?.message || null);
      }
      let ket = false;
      const doc = createSseParser((ten, du) => {
        if (ten === "dan_y") setSt(s => ({ ...s, danY: du }));
        else if (ten === "muc") setSt(s => ({ ...s, muc: { ...s.muc, [du.id]: du } }));
        else if (ten === "xong") { ket = true; setSt(s => ({ ...s, pha: "xong", xong: du })); }
        else if (ten === "error") { ket = true; loi(du?.code || "loi", du?.message || null); }
      });
      const luong = r.body.getReader();
      const giai = new TextDecoder();
      for (;;) {
        const { done, value } = await luong.read();
        if (done) break;
        doc(giai.decode(value, { stream: true }));
      }
      if (!ket) loi("dut", null);  // luồng đóng mà chưa có `xong`: các mục đã về vẫn hiện, kèm lời báo
    } catch (e) {
      if (e.name !== "AbortError") loi("mang", null);
    }
  }, []);
  return { ...st, tao };
}

const NHAN_BUOI = { sang: "Sáng", chieu: "Chiều", toi: "Tối" };
const IC = {  // nét 24 × 24, cùng kiểu nét với biểu tượng buổi của thẻ lịch
  sang: "M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",
  chieu: "M17 18a5 5 0 0 0-10 0M12 9V3M4.2 10.2l1.4 1.4M1 18h2M21 18h2M18.4 11.6l1.4-1.4M23 22H1",
  toi: "M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z",
  dia_chi: "M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11zM12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
  gio: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2",
  ve: "M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4zM14 6v12",
  xem: "M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
  luu_y: "M12 9v4M12 17h.01M10.3 3.9 2.6 17.2A2 2 0 0 0 4.3 20h15.4a2 2 0 0 0 1.7-2.8L13.7 3.9a2 2 0 0 0-3.4 0z",
  an: "M4 11h16a8 8 0 0 1-16 0zM7 21h10M9 7c0-1 1-1.5 1-2.5S9 3 9 3M13 7c0-1 1-1.5 1-2.5S13 3 13 3",
  di_lai: "M5 17h14M6 17V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v9M6 12h12M8.5 20v-3M15.5 20v-3",
  khac: "M9 6l6 6-6 6",
  sach: "M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM19 19v2H6",
};
// nhãn do server gửi ⇒ biểu tượng; nhãn lạ ⇒ mũi tên trung tính (không đoán)
function icNhan(nhan) {
  const n = (nhan || "").toLowerCase();
  if (n.startsWith("địa chỉ") || n.startsWith("vị trí")) return IC.dia_chi;
  if (n.startsWith("giờ") || n.startsWith("thời")) return IC.gio;
  if (n.startsWith("giá vé") || n.startsWith("vé")) return IC.ve;
  if (n.startsWith("nên xem") || n.startsWith("hoạt động")) return IC.xem;
  if (n.startsWith("lưu ý") || n.startsWith("mùa")) return IC.luu_y;
  if (n.startsWith("bữa") || n.startsWith("trưa") || n.startsWith("tối")) return IC.an;
  if (n.startsWith("đi lại") || n.startsWith("di chuyển")) return IC.di_lai;
  return IC.khac;
}
function Net({ d, co = 18 }) {
  return (
    <svg width={co} height={co} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true"><path d={d} /></svg>
  );
}

// Chữ có mã nguồn [n] ⇒ số bấm được: nguồn là một bài kho thì mở bài; nguồn do chương trình dựng (bảng quán của lịch…) thì chỉ là số có chú thích.
function ChuCoNguon({ chu, nguon }) {
  const theoSo = new Map(nguon.map(s => [String(s.id), s]));
  return String(chu ?? "").split(/(\[\d+\])/).map((manh, i) => {
    const m = /^\[(\d+)\]$/.exec(manh);
    if (!m) return manh;
    const s = theoSo.get(m[1]);
    if (!s) {  // số không có trong danh sách nguồn của mục ⇒ không vẽ số mồ côi; để lại một dòng cho người soát (lõi phải ra 0)
      console.warn(`so_tay: số nguồn [${m[1]}] không có trong danh sách nguồn của mục`);
      return null;
    }
    const chuThich = [s.title, ...(s.heading_path || [])].join(" › ");
    return typeof s.bai_id === "string"
      ? <a key={i} className="st-so" href={baiHref(s.bai_id)} title={chuThich} data-lv={linhVuc(s.bai_id)}>{m[1]}</a>
      : <span key={i} className="st-so st-so-tinh" title={chuThich}>{m[1]}</span>;
  });
}

function NoiDungMuc({ muc, khoa }) {
  // Dữ liệu lệch hợp đồng không được làm trắng cả trang (không có lớp bắt lỗi quanh trang): thiếu mảng ⇒ mảng rỗng; nguồn luôn có `heading_path`,
  // `excerpts` (dòng nguồn dùng chung `SourceLine` đọc thẳng hai trường đó khi bấm mở)
  const nguon = (Array.isArray(muc.nguon) ? muc.nguon : []).map(s => ({ ...s, heading_path: s.heading_path || [], excerpts: s.excerpts || [] }));
  const doan = Array.isArray(muc.doan) ? muc.doan : [];
  const thieu = doan.filter(d => d.kieu === "thieu").map(d => d.nhan).filter(Boolean);
  const turnNguon = { key: khoa, sources: nguon, numbers: new Map(nguon.map(s => [String(s.id), s.id])) };
  // vẽ THEO THỨ TỰ server gửi: các đoạn nhãn–nội dung liền nhau gom thành một bảng; câu an toàn đứng đúng chỗ của nó
  const khoi = [];
  for (const d of doan) {
    if (d.kieu === "an_toan") khoi.push(d);
    else if (d.kieu !== "thieu") {  // `van`, `gach` và mọi kiểu lạ: vẽ như một dòng nhãn–nội dung (mất chữ lặng lẽ tệ hơn vẽ thô)
      const cuoi = khoi[khoi.length - 1];
      if (Array.isArray(cuoi)) cuoi.push(d); else khoi.push([d]);
    }
  }
  return (
    <>
      {khoi.map((k, n) => (Array.isArray(k)
        ? <dl key={n} className="st-dl">
            {k.map((d, i) => (
              <div key={i} className="st-d">
                <dt><Net d={icNhan(d.nhan)} /> {d.nhan}</dt>
                <dd>{Array.isArray(d.gach)
                  ? <ul>{d.gach.map((g, j) => <li key={j}><ChuCoNguon chu={g} nguon={nguon} /></li>)}</ul>
                  : <ChuCoNguon chu={d.chu || ""} nguon={nguon} />}</dd>
              </div>
            ))}
          </dl>
        // câu an toàn (bão / lũ, 112): chữ cố định của hệ thống — giữ nguyên chữ và lớp hiển thị an toàn của sản phẩm
        : <p key={n} className="notice notice-an-toan" role="note">{k.chu}</p>))}
      {thieu.length > 0 && (
        <p className="st-thieu"><Net d={IC.sach} /><span><b>Kho tư liệu chưa có:</b> {thieu.map(t => t[0].toLowerCase() + t.slice(1)).join(" · ")}</span></p>
      )}
      {muc.trang_thai === "loi" && <p className="st-muc-loi">Phần mô tả của mục này chưa viết được — bấm “Dựng lại” để thử lần nữa.</p>}
      {nguon.length > 0 && <SourceLine turn={turnNguon} />}
    </>
  );
}

function KhungXuong() {
  return (
    <div className="st-xuong" aria-hidden="true">
      <span /><span /><span className="st-xuong-ngan" /><span /><span className="st-xuong-ngan" />
    </div>
  );
}

function Muc({ d, muc, dang, i }) {
  const anh = anhHopLe(d.anh) ? `${import.meta.env.BASE_URL}${d.anh.src.slice(1)}` : null;
  return (
    <article id={`st-${d.id}`} className={`st-muc st-muc-${d.loai}${anh ? " st-co-anh" : ""} hien`} style={{ "--n": i % 4 }} data-muc={d.id}
             aria-busy={!muc && dang ? "true" : undefined}>
      {anh && (
        <figure className="st-anh">
          <img src={anh} alt={d.ten} loading="lazy" decoding="async" />
          {typeof d.bai_id === "string" && <figcaption><a href={baiHref(d.bai_id)}>Đọc cả bài về nơi này</a></figcaption>}
        </figure>
      )}
      <div className="st-muc-than">
        {d.loai === "diem" && d.buoi && (
          <p className={`st-buoi st-buoi-${d.buoi}`}><Net d={IC[d.buoi]} co={16} /> {NHAN_BUOI[d.buoi]}{d.gio ? ` · ${d.gio}` : ""}</p>
        )}
        {d.loai === "an_uong" && <p className="st-buoi st-buoi-an"><Net d={IC.an} co={16} /> Ngày {d.ngay}</p>}
        <h3 className="st-ten">{typeof d.bai_id === "string" ? <a href={baiHref(d.bai_id)}>{d.ten}</a> : d.ten}</h3>
        {muc ? <NoiDungMuc muc={muc} khoa={`st-${d.id}`} />
          : dang ? <><KhungXuong /><span className="sr-only">đang viết…</span></>
          : <p className="st-muc-loi">Mục này chưa có nội dung — bấm “Dựng lại” để thử lần nữa.</p>}
      </div>
    </article>
  );
}

// "Dòng sông mục lục": một nét dọc, mỗi mục một bến; bến của mục đã viết xong thì đầy, mục đang đọc thì sáng.
function SongMucLuc({ nhom, muc, dangDoc }) {
  return (
    <nav className="st-song" aria-label="Mục lục sổ tay">
      {nhom.map(g => (
        <div key={g.khoa} className="st-song-nhom">
          <p className="st-song-ngay">{g.ten}</p>
          <ol>{g.muc.map(d => (
            <li key={d.id}>
              <a href={`#st-${d.id}`} className="st-ben" data-tt={muc[d.id] ? "xong" : "cho"} aria-current={dangDoc === d.id ? "true" : undefined}
                 onClick={e => { e.preventDefault(); document.getElementById(`st-${d.id}`)?.scrollIntoView({ behavior: "smooth", block: "start" }); }}>
                <i aria-hidden="true" />
                <span>{d.loai === "an_uong" ? "Ăn uống" : d.ten}{d.buoi && <small>{NHAN_BUOI[d.buoi]}{d.gio ? ` · ${d.gio.split("–")[0].trim()}` : ""}</small>}</span>
              </a>
            </li>
          ))}</ol>
        </div>
      ))}
    </nav>
  );
}

// Lúc chờ: con đò đi dọc nét sông theo số mục đã viết xong (máy bật giảm chuyển động: đò đứng đúng chỗ, không trượt).
function TienDo({ xong, tong }) {
  const phan = tong ? Math.round((xong / tong) * 100) : 0;
  return (
    <div className="st-tien" role="progressbar" aria-valuemin={0} aria-valuemax={tong} aria-valuenow={xong} aria-label="Tiến độ viết sổ tay">
      <div className="st-tien-song"><i style={{ width: `${phan}%` }} /><b style={{ left: `${phan}%` }} aria-hidden="true">
        <svg width="34" height="20" viewBox="0 0 34 20" aria-hidden="true"><path d="M2 9h30l-5 8H7z" fill="currentColor" /><path d="M17 9V2l8 7" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" /></svg>
      </b></div>
      <p className="st-tien-chu" aria-live="polite">{tong ? `Đang viết — xong ${xong} / ${tong} mục` : "Đang đọc lịch của bạn…"}</p>
    </div>
  );
}

function inSoTay() {
  // ảnh `loading="lazy"` ngoài màn hình chưa tải ⇒ bản in thiếu ảnh: tải hết rồi mới mở khung in (chờ tối đa 4 giây) — như nút in của thẻ lịch
  const anh = [...document.querySelectorAll(".st img")];
  anh.forEach(i => { i.loading = "eager"; });
  const cho = Promise.all(anh.map(i => (i.complete ? Promise.resolve() : i.decode().catch(() => {}))));
  Promise.race([cho, new Promise(r => setTimeout(r, 4000))]).then(() => window.print());
}

const DONG_CUOI = "Từ Trợ lý Huế — có thể sai; giờ mở cửa, giá vé có thể đã thay đổi, hãy kiểm lại trước khi đi.";

export function SoTay({ soTay }) {
  const { pha, danY, muc, xong, loi, tao } = soTay;
  const [dangDoc, setDangDoc] = useState(null);
  useEffect(() => { if (pha === "chua") tao(); }, [pha, tao]);  // mở thẳng / tải lại `#/so-tay` ⇒ tự dựng từ lịch đang lưu của cuộc

  const ds = danY?.muc || [];
  const nhom = useMemo(() => {
    const ra = [];
    for (const d of ds) {
      const khoa = d.ngay != null ? `n${d.ngay}` : "truoc";
      let g = ra.find(x => x.khoa === khoa);
      if (!g) ra.push(g = { khoa, ngay: d.ngay, ten: d.ngay != null ? `Ngày ${d.ngay}` : "Trước khi đi", muc: [] });
      g.muc.push(d);
    }
    return ra;
  }, [ds]);

  // bến đang đọc: mục trên cùng đang nằm trong dải giữa màn hình
  useEffect(() => {
    if (!ds.length || typeof IntersectionObserver === "undefined") return undefined;
    const qs = new IntersectionObserver(vao => {
      const thay = vao.filter(v => v.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (thay) setDangDoc(thay.target.dataset.muc);
    }, { rootMargin: "-20% 0px -60% 0px" });
    document.querySelectorAll(".st-muc").forEach(e => qs.observe(e));
    return () => qs.disconnect();
  }, [ds]);

  const soXong = ds.filter(d => muc[d.id]).length;
  const soDiem = ds.filter(d => d.loai === "diem").length;
  const baiDung = useMemo(() => {
    const thay = new Map();
    for (const d of ds) for (const s of muc[d.id]?.nguon || []) if (typeof s.bai_id === "string" && !thay.has(s.bai_id)) thay.set(s.bai_id, s.title);
    return [...thay].map(([bai_id, title]) => ({ bai_id, title }));
  }, [ds, muc]);
  const dang = pha === "dang";
  // bốn bến ảnh ở đầu trang: rải đều qua các điểm có ảnh của lịch
  const benAnh = useMemo(() => {
    const co = ds.filter(d => d.loai === "diem" && anhHopLe(d.anh)).map(d => `${import.meta.env.BASE_URL}${d.anh.src.slice(1)}`);
    const so = Math.min(4, co.length);
    return [...new Set(Array.from({ length: so }, (_, i) => co[Math.round((i * (co.length - 1)) / Math.max(1, so - 1))]))];
  }, [ds]);

  return (
    <div className="st">
      <header className="st-dau">
        {/* trang trí: dòng sông của chuyến đi, mỗi "bến ảnh" là một điểm trong lịch (chỉ ở màn rộng; trình đọc màn hình bỏ qua) */}
        <div className="st-song-dau" aria-hidden="true">
          <svg viewBox="0 0 720 260" fill="none" strokeLinecap="round">
            <path d="M-20 210C120 120 220 250 360 170S560 40 740 110" stroke="#CFE7E2" strokeOpacity=".22" strokeWidth="46" />
            <path d="M-20 210C120 120 220 250 360 170S560 40 740 110" stroke="#F0A63A" strokeOpacity=".55" strokeWidth="3" strokeDasharray="2 14" />
          </svg>
          {benAnh.map((src, i) => <img key={src} className={`st-ben-anh st-ben-anh-${i}`} src={src} alt="" decoding="async" />)}
        </div>
        <div className="khung">
          <p className="vet"><a href="#/len-ke-hoach">Lên kế hoạch</a> › Sổ tay</p>
          <h1 className="st-h">{danY?.tieu_de || "Sổ tay cho chuyến đi"}</h1>
          <p className="st-p">Mỗi điểm trong lịch: nên xem gì, giờ mở cửa, giá vé, điều cần lưu ý — viết từ kho tư liệu, có dẫn nguồn để bạn kiểm lại.</p>
          {dang && <TienDo xong={soXong} tong={ds.length} />}
          {pha === "xong" && (
            <ul className="st-tom" aria-label="Tóm tắt sổ tay">
              {danY?.so_ngay != null && <li><b>{danY.so_ngay}</b> ngày</li>}
              <li><b>{soDiem}</b> điểm trong lịch</li>
              <li><b>{baiDung.length}</b> bài kho đã dùng</li>
              {xong?.giay != null && <li>viết trong <b>{Math.round(xong.giay)}</b> giây</li>}
            </ul>
          )}
          <div className="st-nut">
            {pha === "xong" && <button type="button" className="nut st-nut-sang" onClick={inSoTay}>In / Lưu PDF</button>}
            <a className="nut st-nut-vien" href="#/len-ke-hoach">Về lịch</a>
            {(pha === "xong" || pha === "loi") && loi?.ma !== KHONG_CO_LICH && <button type="button" className="nut st-nut-vien" onClick={tao}>Dựng lại</button>}
          </div>
        </div>
      </header>

      {pha === "loi" && (
        <div className="khung">
          <div className="st-bao" role="alert">
            {loi.ma === KHONG_CO_LICH
              ? <><p><b>Lịch của bạn không còn được giữ.</b> Sổ tay viết từ lịch đang có trong cuộc trò chuyện; lịch chỉ được giữ một lúc và mất khi trang được mở lại.</p>
                  <a className="nut nut-chinh" href="#/len-ke-hoach">Xếp lại lịch</a></>
              : <p><b>Sổ tay chưa viết xong.</b> {loi.cau || "Kết nối bị gián đoạn hoặc hệ thống đang bận."} {ds.length > 0 ? "Các mục đã viết vẫn ở bên dưới." : ""} Bấm “Dựng lại” để thử lần nữa.</p>}
          </div>
        </div>
      )}

      {ds.length > 0 && (
        <div className="khung st-hai-cot">
          <SongMucLuc nhom={nhom} muc={muc} dangDoc={dangDoc} />
          <div className="st-than">
            <nav className="st-chip-ngay" aria-label="Tới ngày">
              {nhom.map(g => <a key={g.khoa} className="chip chip-sm" href={`#st-nhom-${g.khoa}`}
                                onClick={e => { e.preventDefault(); document.getElementById(`st-nhom-${g.khoa}`)?.scrollIntoView({ behavior: "smooth", block: "start" }); }}>{g.ten}</a>)}
            </nav>
            {nhom.map(g => (
              <section key={g.khoa} id={`st-nhom-${g.khoa}`} className="st-nhom" aria-label={g.ten}>
                {g.ngay != null && (
                  <h2 className="st-ngay-h"><span>Ngày {g.ngay}</span>
                    <small>{g.muc.filter(d => d.loai === "diem").map(d => d.ten).join(" → ")}</small></h2>
                )}
                {g.muc.map((d, i) => <Muc key={d.id} d={d} muc={muc[d.id]} dang={dang} i={i} />)}
              </section>
            ))}
            {baiDung.length > 0 && !dang && (
              <section className="st-bai" aria-label="Các bài kho đã dùng">
                <h2 className="st-bai-h">Các bài kho đã dùng <small>{baiDung.length} bài</small></h2>
                <ul>{baiDung.map(b => <li key={b.bai_id}><a href={baiHref(b.bai_id)} data-lv={linhVuc(b.bai_id)}><i aria-hidden="true" />{b.title}</a></li>)}</ul>
              </section>
            )}
            {!dang && <p className="st-cuoi">{DONG_CUOI}</p>}
          </div>
        </div>
      )}
      {dang && ds.length === 0 && <div className="khung st-cho-dau" aria-busy="true"><KhungXuong /></div>}
    </div>
  );
}
