import { useEffect, useMemo, useState } from "react";
import { renderArticleHtml } from "./markdown.js";
import { baiHref } from "./route.js";
import { ANH_DAU_TRANG } from "./anh.js";
import { Anh, LINH_VUC, LOAI_CON, O5LinhVuc, TRANG, loaiCua } from "./chung.jsx";

export function KhamPha({ bai }) {
  return (
    <>
      <section className="kp-dau" aria-labelledby="kp-dau-h">
        <Anh a={ANH_DAU_TRANG.ngoMon} className="hero-anh" />
        <div className="khung kp-dau-in">
          <p className="vet"><a href="#/">Trang chủ</a> / Khám phá</p>
          <h1 id="kp-dau-h" className="trang-h">Khám phá Huế</h1>
          <p className="ds-p">Năm chủ đề của kho tư liệu — đọc bài gốc mà trợ lý dùng để trả lời.</p>
        </div>
      </section>
      <div className="khung khoi-trang">
        <O5LinhVuc bai={bai} />
      </div>
    </>
  );
}

export function LinhVuc({ linhVuc, bai, loi }) {
  const lv = LINH_VUC.find(x => x.id === linhVuc);
  const [loai, setLoai] = useState(null);
  const [soHien, setSoHien] = useState(TRANG);
  useEffect(() => { setLoai(null); setSoHien(TRANG); }, [linhVuc]);
  const cuaLv = useMemo(() => (bai || []).filter(b => b.linh_vuc === linhVuc), [bai, linhVuc]);
  const cacLoai = useMemo(() => [...new Set(cuaLv.map(loaiCua))], [cuaLv]);
  const loc = loai === null ? cuaLv : cuaLv.filter(b => loaiCua(b) === loai);
  if (!lv) {
    return (
      <div className="khung khoi-trang">
        <h1 className="trang-h">Không có chủ đề này</h1>
        <p className="khoi-p"><a href="#/kham-pha">Xem 5 chủ đề của kho</a></p>
      </div>
    );
  }
  return (
    <>
      <div className="ds-dau">
        <div className="khung">
          <p className="vet"><a href="#/">Trang chủ</a> / <a href="#/kham-pha">Khám phá</a> / {lv.ten}</p>
          <h1 className="ds-h">{lv.ten}</h1>
          <p className="ds-p">{bai ? `${cuaLv.length} bài trong kho` : "Đang tải…"} — {lv.mo.toLowerCase()}.</p>
        </div>
      </div>
      <div className="khung">
        {loi && <p className="loi" role="alert">{loi}</p>}
        {cacLoai.length > 1 && (
          <div className="ds-loc" aria-label="Lọc theo loại">
            <button type="button" className="chip chip-sm" aria-pressed={loai === null} onClick={() => { setLoai(null); setSoHien(TRANG); }}>Tất cả</button>
            {cacLoai.map(l => (
              <button key={l} type="button" className="chip chip-sm" aria-pressed={loai === l}
                      onClick={() => { setLoai(l); setSoHien(TRANG); }}>{LOAI_CON[l] ?? "Tổng quan"}</button>
            ))}
          </div>
        )}
        <div className="the-ds">
          {loc.slice(0, soHien).map(b => <TheBai key={b.id} b={b} />)}
        </div>
        {loc.length > soHien && (
          <p className="ds-them">
            <button className="nut nut-phu" type="button" onClick={() => setSoHien(n => n + TRANG)}>Xem thêm {Math.min(TRANG, loc.length - soHien)} bài</button>
          </p>
        )}
        <p className="ds-ghi">Thẻ chỉ hiện điều kho có. Không có sao đánh giá hay giá chung chung vì không có dữ liệu thật.</p>
      </div>
    </>
  );
}

function TheBai({ b }) {
  return (
    <a className="the" href={baiHref(b.id)}>
      <div className="anh anh-the" aria-hidden="true" />
      <div className="the-than">
        <p className="the-nhom">{LOAI_CON[b.loai_con] ?? "Tổng quan"}</p>
        <h3 className="the-ten">{b.tieu_de}</h3>
        <p className="the-trong">{b.tom_tat}</p>
      </div>
    </a>
  );
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
  const html = useMemo(() => (data ? renderArticleHtml(data.markdown) : ""), [data]);
  const lv = data && LINH_VUC.find(x => x.id === data.linh_vuc);
  const khac = data && bai ? bai.filter(b => b.linh_vuc === data.linh_vuc && b.loai_con === data.loai_con && b.id !== data.id).slice(0, 6) : [];
  if (!data) {
    return (
      <div className="khung ct">
        <h1 className="ct-h">{trang.loi ? "Không mở được bài" : "Đang tải bài…"}</h1>
        {trang.loi && <p className="loi" role="alert">{trang.loi} <a href="#/kham-pha">Về Khám phá</a></p>}
      </div>
    );
  }
  return (
    <div className="khung ct">
      <p className="vet">
        <a href="#/">Trang chủ</a> / <a href="#/kham-pha">Khám phá</a> / {lv ? <a href={`#/kham-pha/${lv.id}`}>{lv.ten}</a> : data.linh_vuc} / {data.tieu_de}
      </p>
      <h1 className="ct-h">{data.tieu_de}</h1>
      <div className="anh anh-lon" aria-hidden="true" />
      <div className="ct-luoi">
        <article className="ct-bai answer" dangerouslySetInnerHTML={{ __html: html }} />
        <aside className="ct-hop">
          <p className="ct-hop-h">Muốn biết thêm?</p>
          <p className="text-[15px] text-muted">Trợ lý Huế trả lời từ bài này và các bài khác trong kho, có ghi nguồn.</p>
          <button type="button" className="nut nut-chinh ct-hoi" onClick={() => onAskAbout(data.tieu_de)}>Hỏi trợ lý về điểm này</button>
          {khac.length > 0 && (
            <>
              <p className="ct-hop-h mt-6">Bài khác cùng loại</p>
              <ul className="ct-khac">{khac.map(b => <li key={b.id}><a href={baiHref(b.id)}>{b.tieu_de}</a></li>)}</ul>
            </>
          )}
          <BaoSai key={data.id} baiId={data.id} />
        </aside>
      </div>
    </div>
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
