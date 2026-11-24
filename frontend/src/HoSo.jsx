import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { anhCuaBai } from "./anhBai.js";
import { IC, KhungXuong, Net, NoiDungMuc, SongMucLuc, TienDo, inSoTay, useBenDangDoc } from "./SoTay.jsx";
import { baiHref } from "./route.js";
import { createSseParser } from "./stream.js";
import { linhVuc } from "./song/nhin.js";
import "./ho_so.css";

// BẢN THỬ (nhánh `thu-c-ho-so-chu-de`, công tắc server `ho_so_chu_de` mặc định TẮT). Chủ dự án 22:18 24/11/2026 chọn "Chọn từ danh sách": 20 chủ đề do
// CODE dựng từ kho, người dùng bấm một chủ đề (không gõ tự do) ⇒ trợ lý đọc các bài của chủ đề, gom thành mục, viết một hồ sơ có nguồn.
// Ba chỗ người dùng thấy (phiên điều phối gật 22:2x): dải "Đọc theo chủ đề" ở đầu trang Khám phá ⇒ lưới `#/kham-pha/chu-de` ⇒ trang đọc
// `#/kham-pha/chu-de/<mã>`. Trang đọc dùng lại khối và lớp nhìn của trang sổ tay (`SoTay.jsx`, `so_tay.css`); file này chỉ thêm lưới thẻ, dải, và phần
// riêng của hồ sơ. Hợp đồng lõi B: `GET /api/ho_so/chu_de` ⇒ {chu_de: [{ma, ten, so_bai, bai: [{ten, bai_id}]}]}; `POST /api/ho_so` {ma} ⇒ SSE
// `chu_de` {ma, ten, so_bai, bai} ⇒ `dan_y` {tieu_de, muc: [{id, ten, bai}]} ⇒ nhiều `muc` {id, trang_thai, muc_do, doan, nguon} (lộn thứ tự) ⇒ `xong`.
// Chữ lõi gửi không có số tham chiếu; nguồn hiện thành khối riêng dưới mỗi mục như ô trợ lý.

const ANH_GOC = import.meta.env.BASE_URL + "anh/";
const RONG = [];
const BAN_DAU = { pha: "chua", ma: null, chuDe: null, danY: null, muc: {}, xong: null, loi: null };
const KHONG_CO_CHU_DE = "khong_co_chu_de";

// Trạng thái sống ở App: danh sách chủ đề tải MỘT lần; hồ sơ đang đọc giữ qua các lần đổi trang (bấm lại cùng chủ đề đang có thì không dựng lại).
export function useHoSo() {
  const [ds, setDs] = useState(null);       // null = chưa tải · [] = tải lỗi / rỗng
  const [st, setSt] = useState(BAN_DAU);
  const huy = useRef(null), daTai = useRef(false);
  const taiDs = useCallback(() => {
    if (daTai.current) return;
    daTai.current = true;
    fetch("/api/ho_so/chu_de").then(r => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then(d => setDs(Array.isArray(d.chu_de) ? d.chu_de : [])).catch(() => setDs([]));
  }, []);
  const tao = useCallback(async ma => {
    huy.current?.abort();
    const dk = new AbortController();
    huy.current = dk;
    setSt({ ...BAN_DAU, pha: "dang", ma });
    const loi = (code, cau) => setSt(s => ({ ...s, pha: "loi", loi: { ma: code, cau } }));
    try {
      const r = await fetch("/api/ho_so", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ma }), signal: dk.signal });
      if (!r.ok) {
        const than = await r.json().catch(() => null);
        return loi(than?.error?.code || String(r.status), than?.error?.message || null);
      }
      let ket = false;
      const doc = createSseParser((ten, du) => {
        if (ten === "chu_de") setSt(s => ({ ...s, chuDe: du }));
        else if (ten === "dan_y") setSt(s => ({ ...s, danY: du }));
        else if (ten === "muc") setSt(s => ({ ...s, muc: { ...s.muc, [du.id]: du } }));
        else if (ten === "xong") { ket = true; setSt(s => ({ ...s, pha: "xong", xong: du })); }
        else if (ten === "error") { ket = true; loi(du?.code || "loi", du?.message || null); }
      });
      const luong = r.body.getReader(), giai = new TextDecoder();
      for (;;) {
        const { done, value } = await luong.read();
        if (done) break;
        doc(giai.decode(value, { stream: true }));
      }
      if (!ket) loi("dut", null);
    } catch (e) {
      if (e.name !== "AbortError") loi("mang", null);
    }
  }, []);
  return { ds, taiDs, ...st, tao };
}

const hrefChuDe = ma => `#/kham-pha/chu-de/${encodeURIComponent(ma)}`;
const anhCua = baiId => { const a = typeof baiId === "string" ? anhCuaBai(baiId) : null; return a ? `${ANH_GOC}${a.anh}.jpg` : null; };
// ảnh của một chủ đề = ảnh các bài của nó có trong bảng ảnh Khám phá (không có ⇒ ô màu theo lĩnh vực, không mượn ảnh khác)
const anhChuDe = (c, n) => [...new Set((c.bai || []).map(b => anhCua(b.bai_id)).filter(Boolean))].slice(0, n);
const lvChuDe = c => linhVuc((c.bai || [])[0]?.bai_id) || "travel";

function TheChuDe({ c, n }) {
  const anh = anhChuDe(c, 3);
  const tieuBieu = (Array.isArray(c.tieu_bieu) ? c.tieu_bieu : (c.bai || []).map(b => b.ten)).slice(0, 3);
  return (
    <a className="hs-the nang hien" style={{ "--n": n }} href={hrefChuDe(c.ma)} data-lv={lvChuDe(c)}>
      <div className={`hs-the-anh hs-the-anh-${anh.length}`}>
        {anh.map(src => <img key={src} src={src} alt="" loading="lazy" decoding="async" />)}
        <span className="hs-the-so">{c.so_bai} bài kho</span>
      </div>
      <div className="hs-the-than">
        <h3 className="hs-the-ten">{c.ten}</h3>
        {tieuBieu.length > 0 && <p className="hs-the-bai">{tieuBieu.join(" · ")}{c.so_bai > tieuBieu.length ? " …" : ""}</p>}
        <span className="hs-the-doc">Đọc hồ sơ</span>
      </div>
    </a>
  );
}

function OChuDe({ c }) {
  const anh = anhChuDe(c, 1)[0];
  return (
    <a className="hs-o" href={hrefChuDe(c.ma)} data-lv={lvChuDe(c)}>
      {anh ? <img src={anh} alt="" loading="lazy" decoding="async" /> : <i aria-hidden="true" />}
      <span><b>{c.ten}</b><small>{c.so_bai} bài kho</small></span>
    </a>
  );
}

// Dải ở đầu trang Khám phá: vài chủ đề + lối sang lưới đủ. Chưa tải xong / không có chủ đề ⇒ không vẽ gì (trang Khám phá như cũ).
export function DaiChuDe({ hoSo }) {
  useEffect(() => { hoSo.taiDs(); }, [hoSo]);
  const ds = hoSo.ds || [];
  // rải qua các nhóm: lấy chủ đề đầu tiên của mỗi lĩnh vực trước, đủ bốn thẻ
  const chon = useMemo(() => {
    const dau = [], thay = new Set();
    for (const c of ds) if (!thay.has(lvChuDe(c)) && anhChuDe(c, 1).length) { thay.add(lvChuDe(c)); dau.push(c); }
    return [...dau, ...ds.filter(c => !dau.includes(c))].slice(0, 4);
  }, [ds]);
  if (!chon.length) return null;
  return (
    <section className="hs-dai" aria-labelledby="hs-dai-h">
      <div className="hs-dai-dau">
        <h2 id="hs-dai-h" className="hs-dai-h">Đọc theo chủ đề</h2>
        <p className="hs-dai-p">Trợ lý đọc các bài kho về một chủ đề và gom lại thành hồ sơ ngắn, có dẫn nguồn.</p>
        <a className="hs-dai-het" href="#/kham-pha/chu-de">Xem cả {ds.length} chủ đề</a>
      </div>
      <div className="hs-dai-o">{chon.map(c => <OChuDe key={c.ma} c={c} />)}</div>
    </section>
  );
}

// Trang lưới `#/kham-pha/chu-de`
export function LuoiChuDe({ hoSo }) {
  useEffect(() => { hoSo.taiDs(); }, [hoSo]);
  const ds = hoSo.ds;
  return (
    <>
      <section className="kp2-dau hs-dau" aria-labelledby="hs-h">
        <div className="khung">
          <p className="vet vao" style={{ "--n": 0 }}><a href="#/">Trang chủ</a> / <a href="#/kham-pha">Khám phá</a> / Hồ sơ theo chủ đề</p>
          <h1 id="hs-h" className="kp2-h vao" style={{ "--n": 1 }}>Hồ sơ theo chủ đề</h1>
          <p className="kp2-p vao" style={{ "--n": 2 }}>
            {ds?.length ? `${ds.length} chủ đề` : "Các chủ đề"} dựng sẵn từ kho tư liệu. Bấm một chủ đề: trợ lý đọc các bài của chủ đề đó, gom thành từng mục và viết một hồ sơ ngắn — có dẫn nguồn để bạn kiểm lại.
          </p>
        </div>
      </section>
      <div className="khung hs-than">
        <div className="hs-luoi" aria-busy={ds === null}>
          {ds === null
            ? Array.from({ length: 8 }, (_, i) => <div key={i} className="hs-the hs-the-cho" aria-hidden="true" />)
            : ds.map((c, i) => <TheChuDe key={c.ma} c={c} n={i % 4} />)}
        </div>
        {ds && ds.length === 0 && <p className="kp2-rong" role="status">Chưa tải được danh sách chủ đề — thử tải lại trang.</p>}
        <p className="ds-ghi">Danh sách chủ đề và các bài của mỗi chủ đề do chương trình chọn từ kho; trợ lý chỉ gom và viết lại từ các bài đó.</p>
      </div>
    </>
  );
}

// Ý không nêu tên nơi nó nói tới (phiên đo đọc tay 24/11: khoảng 3 / 10 ý) ⇒ gắn tên BÀI mà ý dựa vào (lõi gửi `gach_so[i]` = số nguồn của ý thứ i trong
// `nguon` của chính mục) — chữ nhỏ dưới ý, bấm mở bài. Ý đã nhắc đúng tên bài thì không gắn (khỏi lặp chữ). Đây là TÊN bài, không phải số tham chiếu.
function duoiY(d, j, nguon) {
  if (d.nhan) return null;  // khối có nhãn ("Giờ mở cửa và giá vé": mỗi dòng đã mở đầu bằng tên nơi; nguồn giá là bài VÉ) ⇒ không gắn
  if (new Set(nguon.map(s => s.bai_id || s.title)).size < 2) return null;  // mục chỉ có MỘT bài: tên bài đã ở ngay đầu mục ⇒ gắn vào từng ý là thừa
  const so = Array.isArray(d.gach_so?.[j]) ? d.gach_so[j] : [];
  const y = String(d.gach?.[j] ?? "").toLowerCase();
  const bai = [...new Map(so.map(n => nguon.find(s => s.id === n)).filter(s => s && typeof s.title === "string" && !y.includes(s.title.toLowerCase()))
    .map(s => [s.bai_id || s.title, s])).values()];
  if (!bai.length) return null;
  return (
    <small className="hs-y-bai">Theo bài{" "}
      {bai.map((s, k) => <span key={s.bai_id || s.title}>{k > 0 && " · "}{typeof s.bai_id === "string" ? <a href={baiHref(s.bai_id)}>{s.title}</a> : s.title}</span>)}</small>
  );
}

function MucHoSo({ d, muc, dang, i }) {
  const bai = Array.isArray(d.bai) ? d.bai : [];
  const theoTen = new Map(bai.map(b => [b.ten, b.bai_id]));
  // ô thiếu của hồ sơ: bài của mục mà không ý nào nói tới — tên bài bấm mở được
  const oThieu = (thieu, doan) => {
    const maBai = t => doan.find(x => x.nhan === t)?.bai_id ?? theoTen.get(t);  // lõi gửi kèm `bai_id`; không có thì tra theo tên trong dàn ý
    return (
      <p className="st-thieu"><Net d={IC.sach} /><span><b>Hồ sơ chưa ghi được:</b>{" "}
        {thieu.map((t, k) => <span key={t}>{k > 0 && " · "}{typeof maBai(t) === "string" ? <a href={baiHref(maBai(t))}>{t}</a> : t}</span>)} — mở bài để xem.</span></p>
    );
  };
  return (
    <article id={`st-${d.id}`} className="st-muc st-muc-chu_de hien" style={{ "--n": i % 4 }} data-muc={d.id} aria-busy={!muc && dang ? "true" : undefined}>
      <div className="st-muc-than">
        <p className="st-buoi hs-so-muc">Mục {i + 1}</p>
        <h3 className="st-ten">{d.ten}</h3>
        {bai.length > 0 && (
          <ul className="hs-bai" aria-label="Các bài kho của mục này">
            {bai.map(b => (
              <li key={b.bai_id || b.ten}>
                {typeof b.bai_id === "string"
                  ? <a href={baiHref(b.bai_id)} data-lv={linhVuc(b.bai_id)}>{anhCua(b.bai_id) ? <img src={anhCua(b.bai_id)} alt="" loading="lazy" decoding="async" /> : <i aria-hidden="true" />}{b.ten}</a>
                  : <span><i aria-hidden="true" />{b.ten}</span>}
              </li>
            ))}
          </ul>
        )}
        {muc ? <NoiDungMuc muc={muc} khoa={`hs-${d.id}`} oThieu={oThieu} duoiY={duoiY} />
          : dang ? <><KhungXuong /><span className="sr-only">đang viết…</span></>
          : <p className="st-muc-loi">Mục này chưa có nội dung — bấm “Dựng lại” để thử lần nữa.</p>}
        {muc?.muc_do === "mong" && <p className="hs-mong">Mục này kho nói ít.</p>}
      </div>
    </article>
  );
}

const DONG_CUOI = "Từ Trợ lý Huế — có thể sai; giờ mở cửa, giá vé có thể đã thay đổi, hãy kiểm lại trước khi đi.";
const IT_BAI = 6;  // chủ đề có từ chừng này bài trở xuống ⇒ nói thật số bài ngay đầu trang

// Trang đọc `#/kham-pha/chu-de/<mã>`
export function HoSoChuDe({ ma, hoSo }) {
  const { pha, chuDe, danY, muc, xong, loi, tao } = hoSo;
  useEffect(() => { if (hoSo.ma !== ma) tao(ma); }, [ma, hoSo.ma, tao]);  // mở thẳng / đổi chủ đề ⇒ dựng; quay lại đúng chủ đề đang có ⇒ giữ nguyên
  const dung = hoSo.ma === ma;
  const ds = (dung && danY?.muc) || RONG;
  const dangDoc = useBenDangDoc(ds);
  const nhom = useMemo(() => (ds.length ? [{ khoa: "muc", ngay: null, ten: "Mục", muc: ds.map(d => ({ ...d, loai: "muc" })) }] : []), [ds]);
  const dang = dung && pha === "dang";
  const cd = dung ? chuDe : null;
  const soXong = ds.filter(d => muc[d.id]).length;
  const benAnh = useMemo(() => (cd ? anhChuDe(cd, 4) : []), [cd]);
  const baiDung = useMemo(() => {
    const thay = new Map();
    for (const d of ds) for (const s of muc[d.id]?.nguon || []) if (typeof s.bai_id === "string" && !thay.has(s.bai_id)) thay.set(s.bai_id, s.title);
    return [...thay].map(([bai_id, title]) => ({ bai_id, title }));
  }, [ds, muc]);

  return (
    <div className="st hs">
      <header className="st-dau">
        <div className="st-song-dau" aria-hidden="true">
          <svg viewBox="0 0 720 260" fill="none" strokeLinecap="round">
            <path d="M-20 210C120 120 220 250 360 170S560 40 740 110" stroke="#CFE7E2" strokeOpacity=".22" strokeWidth="46" />
            <path d="M-20 210C120 120 220 250 360 170S560 40 740 110" stroke="#F0A63A" strokeOpacity=".55" strokeWidth="3" strokeDasharray="2 14" />
          </svg>
          {benAnh.map((src, i) => <img key={src} className={`st-ben-anh st-ben-anh-${i}`} src={src} alt="" decoding="async" />)}
        </div>
        <div className="khung">
          <p className="vet"><a href="#/kham-pha">Khám phá</a> › <a href="#/kham-pha/chu-de">Hồ sơ theo chủ đề</a></p>
          <h1 className="st-h">{danY?.tieu_de && dung ? danY.tieu_de : cd?.ten || "Hồ sơ theo chủ đề"}</h1>
          <p className="st-p">Trợ lý đọc {cd ? `${cd.so_bai} bài kho` : "các bài kho"} về chủ đề này và gom lại thành từng mục — có dẫn nguồn để bạn kiểm lại.</p>
          {/* chủ đề ít bài: nói thật số bài, KHÔNG đoán "hồ sơ sẽ ngắn" (lượt thật: chủ đề 5 bài vẫn ra 5 mục đủ ý); "bản ngắn" chỉ nói khi LÕI đếm ra
              (`xong.ban_ngan`: dưới nửa số mục có đủ ý) */}
          {dung && pha === "xong" && xong?.ban_ngan
            ? <p className="hs-it">Đây là bản ngắn vì kho nói ít về chủ đề này.</p>
            : cd && cd.so_bai <= IT_BAI && <p className="hs-it">Kho hiện có {cd.so_bai} bài về chủ đề này — hồ sơ viết từ đúng {cd.so_bai} bài đó.</p>}
          {dang && <TienDo xong={soXong} tong={ds.length} choDau={cd ? `Đang đọc ${cd.so_bai} bài và chia mục…` : "Đang mở chủ đề…"} />}
          {dung && pha === "xong" && (
            <ul className="st-tom" aria-label="Tóm tắt hồ sơ">
              {cd && <li><b>{cd.so_bai}</b> bài kho của chủ đề</li>}
              <li><b>{ds.length}</b> mục</li>
              <li><b>{baiDung.length}</b> bài được dẫn</li>
              {xong?.giay != null && <li>viết trong <b>{Math.round(xong.giay)}</b> giây</li>}
            </ul>
          )}
          <div className="st-nut">
            {dung && pha === "xong" && <button type="button" className="nut st-nut-sang" onClick={inSoTay}>In / Lưu PDF</button>}
            <a className="nut st-nut-vien" href="#/kham-pha/chu-de">Chủ đề khác</a>
            {dung && (pha === "xong" || pha === "loi") && loi?.ma !== KHONG_CO_CHU_DE && <button type="button" className="nut st-nut-vien" onClick={() => tao(ma)}>Dựng lại</button>}
          </div>
        </div>
      </header>

      {dung && pha === "loi" && (
        <div className="khung">
          <div className="st-bao" role="alert">
            {loi.ma === KHONG_CO_CHU_DE || loi.ma === "404"
              ? <><p><b>Không có chủ đề này.</b> Hồ sơ chỉ dựng cho các chủ đề trong danh sách.</p><a className="nut nut-chinh" href="#/kham-pha/chu-de">Xem danh sách chủ đề</a></>
              : <p><b>Hồ sơ chưa viết xong.</b> {loi.cau || "Kết nối bị gián đoạn hoặc hệ thống đang bận."} {ds.length > 0 ? "Các mục đã viết vẫn ở bên dưới." : ""} Bấm “Dựng lại” để thử lần nữa.</p>}
          </div>
        </div>
      )}

      {ds.length > 0 && (
        <div className="khung st-hai-cot">
          <SongMucLuc nhom={nhom} muc={muc} dangDoc={dangDoc} />
          <div className="st-than">
            {ds.map((d, i) => <MucHoSo key={d.id} d={d} muc={muc[d.id]} dang={dang} i={i} />)}
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
      {/* chưa có dàn ý (3–5 giây đầu): tên các bài sẽ đọc + khung xương */}
      {dang && ds.length === 0 && (
        <div className="khung st-cho-dau" aria-busy="true">
          {cd?.bai?.length > 0 && <p className="hs-dang-doc">Đang đọc: {cd.bai.map(b => b.ten).join(" · ")}</p>}
          <KhungXuong />
        </div>
      )}
    </div>
  );
}
