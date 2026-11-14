import { useEffect, useMemo, useState } from "react";
import { renderArticleHtml } from "./markdown.js";
import { baiHref } from "./route.js";
import { ANH_DAU_TRANG, GP } from "./anh.js";
import { anhCuaBai, khoaBai } from "./anhBai.js";
import { Anh, LINH_VUC, LOAI_CON, TRANG, loaiCua } from "./chung.jsx";
import "./kp.css";

// Khám phá theo H1 "Sông Hương" (đợt 1 giao diện, C, 14/11/2026; mẫu `data/ui_mau_2026-11-14/h1/kham_pha*.html`).
// Một trang danh sách cho cả "Khám phá" lẫn "Khám phá / <lĩnh vực>": ô tìm theo tên + lọc lĩnh vực / loại, thẻ có ảnh khi bài có trong bảng `anhBai.js`
// (không có ⇒ ô màu + biểu tượng lĩnh vực, không mượn ảnh khác). Thẻ chỉ hiện điều kho có: không sao, không giá chung chung.
// Hiệu ứng (A chốt từ nghiên cứu "wow"): ảnh thẻ ⇒ ảnh đầu bài bằng View Transitions (`view-transition-name` theo mã bài), ảnh lộ dần qua
// mặt nạ (`clip-path`) — CSS trong kp.css, chỉ chạy dưới `html.hieu-ung` (máy không giảm chuyển động).

const ANH_GOC = import.meta.env.BASE_URL + "anh/";
const IC_LV = {  // biểu tượng nét mảnh theo lĩnh vực (tự vẽ)
  foods: "M5 11h14a7 7 0 0 1-14 0zM9 4c0 2 2 2 2 4M13 4c0 2 2 2 2 4",
  heritages: "M3 20h18M5 20V10l7-5 7 5v10M9 20v-6h6v6",
  festivals: "M12 3v4M5 8l2 2M19 8l-2 2M6 20l6-9 6 9z",
  performing_arts: "M9 18V6l10-2v12M7 20.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM17 18.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
  travel: "M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11zM12 12.2a2.2 2.2 0 1 0 0-4.4 2.2 2.2 0 0 0 0 4.4z",
};

function IconLv({ lv, lon }) {
  return (
    <svg className={lon ? "kp-ic-lon" : "kp-ic"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"
         strokeLinejoin="round" aria-hidden="true"><path d={IC_LV[lv] || IC_LV.travel} /></svg>
  );
}

// tên chuyển cảnh: cùng một tên ở thẻ và ở ảnh đầu bài ⇒ trình duyệt "bay" ảnh sang trang mới (phải là tên CSS hợp lệ, duy nhất trên trang)
const tenChuyenCanh = id => `kp-anh-${khoaBai(id)}`;

function GhiCongAnh({ a }) {
  const ngoai = { target: "_blank", rel: "noopener noreferrer" };
  return (
    <>Ảnh: {a.tacGia} · {GP[a.giayPhep] ? <a href={GP[a.giayPhep]} {...ngoai}>{a.giayPhep}</a> : a.giayPhep} ·{" "}
      <a href={a.trang} {...ngoai}>trang ảnh trên Wikimedia Commons</a> · đã {a.doi}</>
  );
}

function bo(s) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();
}

function DanhSach({ bai, loi, linhVuc }) {
  const [lv, setLv] = useState(linhVuc ?? null);
  const [loai, setLoai] = useState(null);
  const [tim, setTim] = useState("");
  const [soHien, setSoHien] = useState(TRANG);
  useEffect(() => { setLv(linhVuc ?? null); setLoai(null); setSoHien(TRANG); }, [linhVuc]);
  const theoLv = useMemo(() => (bai || []).filter(b => !lv || b.linh_vuc === lv), [bai, lv]);
  const cacLoai = useMemo(() => (lv ? [...new Set(theoLv.map(loaiCua))] : []), [theoLv, lv]);
  const q = bo(tim.trim());
  const loc = theoLv.filter(b => (loai === null || loaiCua(b) === loai) && (!q || bo(b.tieu_de).includes(q)));
  const chonLv = id => { setLv(id); setLoai(null); setSoHien(TRANG); };
  const thongTin = LINH_VUC.find(x => x.id === lv);
  return (
    <>
      <section className="kp2-dau" aria-labelledby="kp2-h">
        <div className="kp2-nen troi-cuon"><Anh a={ANH_DAU_TRANG.ngoMon} className="anh-troi" /></div>
        <div className="khung kp2-dau-in">
          <p className="vet vao" style={{ "--n": 0 }}>
            <a href="#/">Trang chủ</a> / {thongTin ? <><a href="#/kham-pha">Khám phá</a> / {thongTin.ten}</> : "Khám phá"}
          </p>
          <h1 id="kp2-h" className="kp2-h vao" style={{ "--n": 1 }}>{thongTin ? thongTin.ten : "Khám phá Huế"}</h1>
          <p className="kp2-p vao" style={{ "--n": 2 }}>
            {bai ? `${theoLv.length} bài` : "Các bài"} trong kho tư liệu mà trợ lý dùng để trả lời{thongTin ? ` — ${thongTin.mo.toLowerCase()}` : ""}. Bấm để đọc cả bài.
          </p>
          <label className="kp2-tim vao" style={{ "--n": 3 }}>
            <span className="sr-only">Tìm bài theo tên</span>
            <input type="search" value={tim} onChange={e => { setTim(e.target.value); setSoHien(TRANG); }}
                   placeholder="Tìm theo tên bài, ví dụ: lăng, chè, ca Huế" />
          </label>
        </div>
      </section>
      <div className="khung kp2-than">
        {loi && <p className="loi" role="alert">{loi}</p>}
        <div className="kp2-loc" role="group" aria-label="Lọc theo lĩnh vực">
          <button type="button" className="chip chip-sm nhan-nut" aria-pressed={!lv} onClick={() => chonLv(null)}>
            Tất cả {bai && <b>{bai.length}</b>}
          </button>
          {LINH_VUC.map(x => (
            <button key={x.id} type="button" className="chip chip-sm nhan-nut" aria-pressed={lv === x.id} onClick={() => chonLv(x.id)}>
              <IconLv lv={x.id} />{x.ten} {bai && <b>{bai.filter(b => b.linh_vuc === x.id).length}</b>}
            </button>
          ))}
        </div>
        {cacLoai.length > 1 && (
          <div className="kp2-loc kp2-loc-con" role="group" aria-label="Lọc theo loại">
            <button type="button" className="chip chip-sm nhan-nut" aria-pressed={loai === null} onClick={() => { setLoai(null); setSoHien(TRANG); }}>Mọi loại</button>
            {cacLoai.map(l => (
              <button key={l} type="button" className="chip chip-sm nhan-nut" aria-pressed={loai === l}
                      onClick={() => { setLoai(l); setSoHien(TRANG); }}>{LOAI_CON[l] ?? "Tổng quan"}</button>
            ))}
          </div>
        )}
        {/* lúc chưa tải: giữ chỗ đúng cỡ lưới ⇒ chân trang không bị đẩy (CLS — review đợt 0 m-1) */}
        <div className="kp2-luoi" aria-busy={bai === null}>
          {bai === null
            ? Array.from({ length: 8 }, (_, i) => <div key={i} className="kp2-the kp2-cho" aria-hidden="true" />)
            : loc.slice(0, soHien).map((b, i) => <TheBai key={b.id} b={b} n={i % 4} />)}
        </div>
        {bai && loc.length === 0 && <p className="kp2-rong" role="status">Không có bài nào khớp “{tim.trim()}”.</p>}
        {loc.length > soHien && (
          <p className="ds-them">
            <button className="nut nut-phu nhan-nut" type="button" onClick={() => setSoHien(n => n + TRANG)}>Xem thêm {Math.min(TRANG, loc.length - soHien)} bài</button>
          </p>
        )}
        <p className="ds-ghi">Thẻ chỉ hiện điều kho có. Không có sao đánh giá hay giá chung chung vì không có dữ liệu thật. Ảnh chỉ có ở bài đã có ảnh giấy phép mở.</p>
      </div>
    </>
  );
}

export function KhamPha({ bai, loi }) {
  return <DanhSach bai={bai} loi={loi} linhVuc={null} />;
}

export function LinhVuc({ linhVuc, bai, loi }) {
  if (!LINH_VUC.some(x => x.id === linhVuc)) {
    return (
      <div className="khung khoi-trang">
        <h1 className="trang-h">Không có chủ đề này</h1>
        <p className="khoi-p"><a href="#/kham-pha">Xem 5 chủ đề của kho</a></p>
      </div>
    );
  }
  return <DanhSach bai={bai} loi={loi} linhVuc={linhVuc} />;
}

function TheBai({ b, n }) {
  const a = anhCuaBai(b.id);
  const lv = LINH_VUC.find(x => x.id === b.linh_vuc);
  return (
    <a className="kp2-the nang hien" style={{ "--n": n }} href={baiHref(b.id)}>
      <div className={`kp2-the-anh lop-mau kp2-o-${b.linh_vuc}`}>
        {a ? <img src={`${ANH_GOC}${a.anh}.jpg`} alt="" loading="lazy" decoding="async" style={{ viewTransitionName: tenChuyenCanh(b.id) }} />
          : <IconLv lv={b.linh_vuc} lon />}
        <span className="nhan kp2-nhan"><IconLv lv={b.linh_vuc} />{LOAI_CON[b.loai_con] ?? lv?.ten ?? "Tổng quan"}</span>
      </div>
      <div className="kp2-the-than">
        <h3 className="kp2-the-ten">{b.tieu_de}</h3>
        <p className="kp2-the-trong">{b.tom_tat}</p>
        <span className="kp2-doc">Đọc bài</span>
      </div>
    </a>
  );
}

// "Thông tin chung" của bài (dòng `- **Tên:** giá trị`) ⇒ thẻ "Thông tin nhanh" bên phải; mục đó bỏ khỏi thân bài để không lặp.
// Không đọc được ≥ 2 dòng ⇒ giữ nguyên bài, không có thẻ.
function tachThongTin(md) {
  const dong = md.split("\n");
  const dau = dong.findIndex(l => /^#{2,3}\s+Thông tin chung/i.test(l));
  if (dau < 0) return { nhanh: [], md };
  let cuoi = dau + 1;
  while (cuoi < dong.length && !/^#{1,3}\s/.test(dong[cuoi])) cuoi++;
  const nhanh = dong.slice(dau + 1, cuoi).map(l => l.match(/^-\s+\*\*(.+?):\*\*\s*(.+)$/)).filter(Boolean).map(m => [m[1], m[2]]);
  if (nhanh.length < 2) return { nhanh: [], md };
  return { nhanh: nhanh.slice(0, 7), md: [...dong.slice(0, dau), ...dong.slice(cuoi)].join("\n") };
}

export function Bai({ baiId, bai, onAskAbout }) {
  const [trang, setTrang] = useState({ id: null, data: null, loi: "" });
  const coTrongDs = bai === null ? null : bai.some(b => b.id === baiId);  // null = danh sách chưa tải
  useEffect(() => {
    let huy = false;
    setTrang({ id: baiId, data: null, loi: "" });
    if (coTrongDs === null) return undefined;
    if (!coTrongDs) {  // mã không có trong danh sách ⇒ báo ngay, không gọi server (server cũng trả 404 — `api/routes/cong.py`)
      setTrang({ id: baiId, data: null, loi: "Không tìm thấy bài này." });
      return undefined;
    }
    fetch(`/api/kham_pha/bai?id=${encodeURIComponent(baiId)}`)
      .then(r => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(data => !huy && setTrang({ id: baiId, data, loi: "" }))
      .catch(status => !huy && setTrang({ id: baiId, data: null, loi: status === 404 ? "Không tìm thấy bài này." : "Chưa tải được bài — thử lại sau." }));
    return () => { huy = true; };
  }, [baiId, coTrongDs]);
  const data = trang.id === baiId ? trang.data : null;
  const tach = useMemo(() => (data ? tachThongTin(data.markdown) : { nhanh: [], md: "" }), [data]);
  const html = useMemo(() => (data ? renderArticleHtml(tach.md) : ""), [data, tach]);
  const lv = data && LINH_VUC.find(x => x.id === data.linh_vuc);
  const khac = data && bai ? bai.filter(b => b.linh_vuc === data.linh_vuc && b.loai_con === data.loai_con && b.id !== data.id) : [];
  // bài liên quan: bài cùng loại có ảnh trước (thẻ đẹp hơn), tối đa 3
  const lienQuan = [...khac.filter(b => anhCuaBai(b.id)), ...khac.filter(b => !anhCuaBai(b.id))].slice(0, 3);
  const a = data ? anhCuaBai(data.id) : null;
  const diaDiem = tach.nhanh.find(([k]) => /^(Địa điểm|Địa chỉ)/i.test(k))?.[1];
  if (trang.loi) {
    return (
      <div className="khung ct kp2-tai">
        <h1 className="ct-h">Không mở được bài</h1>
        <p className="loi" role="alert">{trang.loi} <a href="#/kham-pha">Về Khám phá</a></p>
      </div>
    );
  }
  if (!data) {
    // đang tải: vẽ sẵn đúng khung của trang bài (dải tiêu đề + hai cột) ⇒ khi bài tới, phần trên không bị đẩy (CLS)
    const meta = bai?.find(b => b.id === baiId);
    return (
      <div aria-busy="true">
        <section className="kp2-bai-dau"><div className="khung">
          <p className="vet">&nbsp;</p>
          <h1 className="kp2-bai-h">{meta ? meta.tieu_de : "Đang tải bài…"}</h1>
          <p className="kp2-dia">&nbsp;</p>
        </div></section>
        <div className="khung kp2-hai-cot">
          <div className="kp2-bai-than kp2-cho-bai" role="status">Đang tải bài…</div>
          <div className="kp2-ben"><div className={`kp2-ben-anh kp2-cho-anh ${anhCuaBai(baiId) ? "" : "kp2-an"}`} /></div>
        </div>
      </div>
    );
  }
  return (
    <>
      <section className="kp2-bai-dau">
        <div className="khung">
          <p className="vet vao" style={{ "--n": 0 }}>
            <a href="#/">Trang chủ</a> / <a href="#/kham-pha">Khám phá</a> / {lv ? <a href={`#/kham-pha/${lv.id}`}>{lv.ten}</a> : data.linh_vuc}
          </p>
          <h1 className="kp2-bai-h vao" style={{ "--n": 1 }}>{data.tieu_de}</h1>
          <p className="kp2-dia vao" style={{ "--n": 2 }}>{diaDiem ? <><IconLv lv="travel" />{diaDiem}</> : "\u00a0"}</p>
        </div>
      </section>
      <div className="khung kp2-hai-cot">
        <article className="ct-bai answer kp2-bai-than" dangerouslySetInnerHTML={{ __html: html }} />
        <aside className="kp2-ben" aria-label="Ảnh và thông tin nhanh">
          {a && (
            <figure className="kp2-ben-anh">
              <img src={`${ANH_GOC}${a.anh}.jpg`} alt={data.tieu_de} decoding="async" style={{ viewTransitionName: tenChuyenCanh(data.id) }} />
              <figcaption><GhiCongAnh a={a} /></figcaption>
            </figure>
          )}
          <div className="kp2-nhanh">
            {tach.nhanh.length > 0 && (
              <>
                <h2 className="kp2-nhanh-h">Thông tin nhanh</h2>
                <dl>{tach.nhanh.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v.replace(/\*\*/g, "")}</dd></div>)}</dl>
                <p className="kp2-luu">Giờ mở cửa, giá vé có thể đã đổi — kiểm lại trước khi đi.</p>
              </>
            )}
            <button type="button" className="nut nut-chinh ct-hoi nhan-nut" onClick={() => onAskAbout(data.tieu_de)}>Hỏi trợ lý về điểm này</button>
            <BaoSai key={data.id} baiId={data.id} />
          </div>
        </aside>
      </div>
      {lienQuan.length > 0 && (
        <section className="khung kp2-lien" aria-labelledby="kp2-lien-h">
          <h2 id="kp2-lien-h" className="khoi-h">Bài cùng loại</h2>
          <div className="kp2-luoi kp2-luoi-3">{lienQuan.map((b, i) => <TheBai key={b.id} b={b} n={i} />)}</div>
        </section>
      )}
    </>
  );
}

// Việc nhỏ 8: "Báo thông tin chưa đúng" — server chỉ ghi mã bài (`POST /api/bao_sai`), không nhận chữ tự do. Một lần mỗi lần mở bài.
function BaoSai({ baiId }) {
  const [trangThai, setTrangThai] = useState("chua");  // chua · dang · xong · loi
  async function gui() {
    setTrangThai("dang");
    try {
      const r = await fetch("/api/bao_sai", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ bai_id: baiId }) });
      setTrangThai(r.ok ? "xong" : "loi");
    } catch {
      setTrangThai("loi");
    }
  }
  return (
    <p className="ct-bao" role="status">
      {trangThai === "xong" ? "Cảm ơn bạn — bài này sẽ được kiểm lại."
        : <>Thấy thông tin chưa đúng? <button type="button" onClick={gui} disabled={trangThai === "dang"}>Báo thông tin chưa đúng</button>
            {trangThai === "loi" && " Chưa gửi được — thử lại sau."}</>}
    </p>
  );
}
