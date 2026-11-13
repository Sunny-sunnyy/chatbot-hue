import { useEffect, useMemo, useState } from "react";
import { renderArticleHtml } from "./markdown.js";
import { baiHref } from "./route.js";
import { ANH_DAU_TRANG, ANH_LINH_VUC, MAN_NHO, MOI_ANH } from "./anh.js";

// Các trang của cổng đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` D9–D12), bản mẫu 2 "Sông Hương".
// Thẻ bài chỉ hiện trường kho có (tên, loại, tóm tắt) — không sao, không "Liên hệ", không giờ / giá chung chung (D10). Ảnh (User chốt 07/11):
// chỉ 2 ảnh đầu trang + 5 ô lĩnh vực (`anh.js`); thẻ bài / trang bài giữ khối hoa văn.

// 5 lĩnh vực kho (mã = tên thư mục); thứ tự như bản mẫu.
export const LINH_VUC = [
  { id: "foods", ten: "Ẩm thực", mo: "Món Huế, quán ăn, cà phê, đặc sản" },
  { id: "heritages", ten: "Di tích", mo: "Kinh thành, lăng tẩm, chùa, di sản" },
  { id: "festivals", ten: "Lễ hội", mo: "Lễ cung đình, lễ dân gian, Festival" },
  { id: "performing_arts", ten: "Nghệ thuật biểu diễn", mo: "Nhã nhạc, ca Huế, tuồng" },
  { id: "travel", ten: "Đi lại và tham quan", mo: "Điểm đến, vé tham quan, dịch vụ" },
];
const LOAI_CON = { restaurants: "Quán ăn", cafes: "Quán cà phê", local_specialties: "Đặc sản", heritage: "Di tích", festival: "Lễ hội",
                   arts: "Loại hình nghệ thuật", places: "Điểm đến", tickets: "Vé tham quan", services: "Dịch vụ" };
const TRANG = 12;  // số thẻ mỗi lần "Xem thêm"
const TONG_QUAN = "_tong_quan";  // bài nằm ngay gốc lĩnh vực (`loai_con` null) — khác "chưa lọc" (null)
const loaiCua = b => b.loai_con ?? TONG_QUAN;

// Câu gợi ý ở trang chủ: câu tự viết đã có ở giao diện trước (kiểm có trong kho bằng `scripts/grep_kb.sh`) — không câu Golden / kín (D9).
export const GOI_Y = ["Ăn sáng ở Huế nên thử món gì?", "Chỉ có nửa ngày thì nên đi lăng nào?", "Lễ hội Điện Huệ Nam diễn ra khi nào?",
                      "Nghe ca Huế trên sông ở đâu?", "Từ sân bay vào trung tâm bằng gì?"];

// Biểu mẫu "Lên kế hoạch" (D3): giá trị = đúng tập `TruongInput` của server (`backend/llm/hoi_lai.py`); "kiểu đi" ẩn ở đợt 1 (Q-U3).
const BIEU_MAU = [
  { ten: "so_ngay", nhan: "Mấy ngày", bat_buoc: true,
    chon: [["1", "1 ngày"], ["2", "2 ngày"], ["3", "3 ngày"], ["4+", "Từ 4 ngày"]] },
  { ten: "di_cung", nhan: "Đi cùng ai",
    chon: [["mot_minh", "Một mình"], ["cap_doi", "Cặp đôi"], ["gia_dinh_tre_em", "Gia đình có trẻ em"], ["nguoi_lon_tuoi", "Có người lớn tuổi"],
           ["nhom_ban", "Nhóm bạn"]] },
  { ten: "so_thich", nhan: "Thích gì",
    chon: [["di_tich", "Di tích"], ["am_thuc", "Ẩm thực"], ["thien_nhien", "Thiên nhiên"], ["le_hoi_nghe_thuat", "Lễ hội, nghệ thuật"],
           ["chup_anh", "Chụp ảnh"]] },
];
export const CAU_BIEU_MAU = "Lên kế hoạch tham quan Huế";  // chỉ để in lại trong khung trò chuyện — server dựng câu từ giá trị nút

// Ảnh có bản nhỏ cho điện thoại: `<source media>` chọn theo khổ màn (không theo mật độ điểm ảnh như `srcset`) ⇒ máy ≤ 760 px luôn tải bản nhỏ.
function Anh({ a, ...props }) {
  return (
    <picture>
      <source media={MAN_NHO} srcSet={a.srcNho} />
      <img src={a.src} alt="" {...props} />
    </picture>
  );
}

function Song({ className }) {
  return (
    <svg className={className} viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 150 C 240 110, 480 190, 720 150 S 1200 110, 1440 150 L1440 220 L0 220 Z" fill="#0E6B66" opacity=".35" />
      <path d="M0 175 C 260 140, 500 210, 760 175 S 1220 140, 1440 178 L1440 220 L0 220 Z" fill="#0E6B66" opacity=".55" />
      <path d="M0 200 C 280 175, 520 225, 800 200 S 1240 178, 1440 202 L1440 220 L0 220 Z" fill="#EDF4F2" />
    </svg>
  );
}

function soBai(bai, linhVuc) {
  return bai ? bai.filter(b => b.linh_vuc === linhVuc).length : null;
}

export function TrangChu({ bai, tinhNang, thoiTiet, onAsk }) {
  const [cau, setCau] = useState("");
  function submit(event) {
    event.preventDefault();
    if (cau.trim() && onAsk(cau)) setCau("");
  }
  return (
    <>
      <section className="hero" aria-labelledby="hero-h">
        <Anh a={ANH_DAU_TRANG.song} className="hero-anh" fetchpriority="high" />
        <Song className="song" />
        <div className="hero-in">
          <h1 id="hero-h" className="hero-h">Hỏi về Huế, như hỏi người bản xứ</h1>
          <p className="hero-p">Trả lời từ kho tư liệu về món ăn, di tích, lễ hội Huế — kèm tên tài liệu để bạn tự kiểm.</p>
          <form className="hoi" onSubmit={submit}>
            <label className="sr-only" htmlFor="hoi-lon">Câu hỏi cho Trợ lý Huế</label>
            <input id="hoi-lon" className="hoi-o" value={cau} onChange={e => setCau(e.target.value)} placeholder="Ví dụ: chiều nay nên đi lăng nào?"
                   autoComplete="off" maxLength={500} />
            <button className="nut nut-chinh" type="submit">Hỏi</button>
          </form>
          <div className="goi-y" aria-label="Câu hỏi gợi ý">
            {GOI_Y.map(q => <button key={q} className="chip" type="button" onClick={() => onAsk(q)}>{q}</button>)}
          </div>
          {tinhNang.thoi_tiet && thoiTiet?.trang_thai === "ok" && <ThoiTiet tt={thoiTiet} />}
        </div>
      </section>

      <div className="khung">
        <section className="khoi" aria-labelledby="kp-h">
          <h2 id="kp-h" className="khoi-h">Khám phá theo chủ đề</h2>
          <p className="khoi-p">Mỗi chủ đề là các bài trong kho mà trợ lý dùng để trả lời.</p>
          <O5LinhVuc bai={bai} />
        </section>

        {tinhNang.lich_trinh_bieu_mau && (
          <section className="khoi lc-the" aria-labelledby="lc-h">
            <div>
              <h2 id="lc-h" className="khoi-h">Lên kế hoạch đi Huế</h2>
              <p className="khoi-p">Chọn số ngày, người đi cùng và điều bạn thích — trợ lý xếp lịch theo buổi từ các điểm trong kho, điểm nào không xếp được sẽ
                ghi lý do.</p>
            </div>
            <a className="nut nut-chinh" href="#/len-ke-hoach">Bắt đầu lên kế hoạch</a>
          </section>
        )}

        <p className="dai-bao">Trợ lý Huế trả lời từ kho tư liệu và ghi nguồn, nhưng vẫn có thể sai. <a href="#/gioi-thieu">Trợ lý làm được gì?</a></p>
      </div>
    </>
  );
}

function ThoiTiet({ tt }) {
  const { tmin, tmax, xs_mua } = tt.hom_nay;
  return (
    <aside className="tt-hop" aria-label="Thời tiết Huế hôm nay">
      <p className="tt-h">Huế hôm nay</p>
      <p className="tt-so">{tmin}–{tmax} °C{xs_mua != null && <span className="tt-mo"> · khả năng mưa {xs_mua} %</span>}</p>
      <p className="tt-chu">{tt.ghi_cong} — số liệu lúc {tt.cap_nhat}.</p>
    </aside>
  );
}

function O5LinhVuc({ bai }) {
  return (
    <div className="kp-ds">
      {LINH_VUC.map(lv => (
        <a key={lv.id} className="kp" href={`#/kham-pha/${lv.id}`}>
          <Anh a={ANH_LINH_VUC[lv.id]} className="kp-anh" loading="lazy" />
          <span className="kp-ten">{lv.ten}</span>
          <span className="kp-mo">{lv.mo}</span>
          {soBai(bai, lv.id) != null && <span className="kp-so">{soBai(bai, lv.id)} bài</span>}
        </a>
      ))}
    </div>
  );
}

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

export function LenKeHoach({ bat, prefill, pending, onSubmit }) {
  const [chon, setChon] = useState(prefill || {});
  useEffect(() => { if (prefill) setChon(prefill); }, [prefill]);
  const du = BIEU_MAU.filter(t => t.bat_buoc).every(t => chon[t.ten]);
  const tomTat = BIEU_MAU.filter(t => chon[t.ten]).map(t => t.chon.find(([v]) => v === chon[t.ten])[1]).join(" · ");
  if (!bat) {
    return (
      <div className="khung khoi-trang">
        <h1 className="trang-h">Lên kế hoạch</h1>
        <p className="khoi-p">Tính năng này chưa bật. Bạn vẫn có thể hỏi <a href="#/tro-ly">Trợ lý Huế</a> về các điểm muốn đi.</p>
      </div>
    );
  }
  return (
    <div className="khung khoi-trang">
      <p className="vet"><a href="#/">Trang chủ</a> / Lên kế hoạch</p>
      <h1 className="trang-h">Lên kế hoạch đi Huế</h1>
      <p className="khoi-p">Trợ lý xếp lịch theo buổi từ các điểm trong kho. Muốn đổi lịch thì quay lại đây điền lại.</p>
      <form className="lc" onSubmit={e => { e.preventDefault(); if (du && !pending) onSubmit(Object.fromEntries(Object.entries(chon).filter(([, v]) => v)), tomTat); }}>
        {BIEU_MAU.map(t => (
          <fieldset key={t.ten} className="lc-nhom">
            <legend className="lc-ten">{t.nhan}{t.bat_buoc ? "" : " (không bắt buộc)"}</legend>
            <div className="lc-chip">
              {t.chon.map(([gia_tri, nhan]) => (
                <button key={gia_tri} type="button" className="chip chip-sm" aria-pressed={chon[t.ten] === gia_tri}
                        onClick={() => setChon(old => ({ ...old, [t.ten]: old[t.ten] === gia_tri ? undefined : gia_tri }))}>{nhan}</button>
              ))}
            </div>
          </fieldset>
        ))}
        <button className="nut nut-chinh lc-nut" type="submit" disabled={!du || pending}>
          {pending ? "Trợ lý đang trả lời…" : du ? `Xếp lịch ${tomTat.split(" · ")[0]}` : "Chọn số ngày để xếp lịch"}
        </button>
      </form>
    </div>
  );
}

// "Lên kế hoạch" bản 2 (plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md`, spec bản 3.3 §5) — chỉ khi server bật `len_ke_hoach_v2`.
// Bốn nhóm theo câu người đi tự hỏi; chỉ vẽ ô có trong `cauHinh.o_hien` (ô ẩn không có trong DOM); giá trị = đúng hợp đồng `truong` mới của server.
const KIEU_DI = [["nhe_nhang", "Nhẹ nhàng", "khoảng 2 điểm một ngày"], ["can_bang", "Cân bằng", "khoảng 3 điểm một ngày"],
                 ["kham_pha", "Khám phá nhiều", "tới 4 điểm một ngày"]];
const SO_THICH = BIEU_MAU.find(t => t.ten === "so_thich").chon;
const MAC_DINH_V2 = { so_ngay: 2, nguoi_lon: 2, tre_em: 0, lon_tuoi: false, kieu_di: null, so_thich: [], ngay_di: "" };

function ngayIso(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

// prefill = `truong` đã gửi (nút "Sửa") ⇒ về trạng thái biểu mẫu
function tuTruong(truong) {
  if (!truong) return MAC_DINH_V2;
  const st = truong.so_thich;
  return { ...MAC_DINH_V2, ...truong, so_ngay: Number(truong.so_ngay === "4+" ? 4 : truong.so_ngay || 2),
           so_thich: Array.isArray(st) ? st : st ? [st] : [], ngay_di: truong.ngay_di || "" };
}

function SoDem({ id, nhan, giaTri, min, max, onDoi }) {
  return (
    <div className="lc-dem">
      <span id={id}>{nhan}</span>
      <button type="button" className="chip chip-sm" aria-label={`Bớt ${nhan.toLowerCase()}`} disabled={giaTri <= min}
              onClick={() => onDoi(giaTri - 1)}>−</button>
      <output aria-labelledby={id} aria-live="polite">{giaTri}</output>
      <button type="button" className="chip chip-sm" aria-label={`Thêm ${nhan.toLowerCase()}`} disabled={giaTri >= max}
              onClick={() => onDoi(giaTri + 1)}>+</button>
    </div>
  );
}

export function LenKeHoachV2({ cauHinh, prefill, pending, onSubmit }) {
  const [chon, setChon] = useState(() => tuTruong(prefill));
  useEffect(() => { if (prefill) setChon(tuTruong(prefill)); }, [prefill]);
  const hien = new Set(cauHinh.o_hien);
  const doi = (ten, giaTri) => setChon(old => ({ ...old, [ten]: giaTri }));
  const homNay = new Date();
  const toiDa = new Date(homNay.getFullYear(), homNay.getMonth(), homNay.getDate() + 180);
  const soNgay = Math.min(chon.so_ngay, cauHinh.so_ngay_toi_da);

  const truong = { so_ngay: String(soNgay) };
  if (hien.has("nguoi_lon")) truong.nguoi_lon = chon.nguoi_lon;
  if (hien.has("tre_em")) truong.tre_em = chon.tre_em;
  if (hien.has("lon_tuoi")) truong.lon_tuoi = chon.lon_tuoi;
  if (hien.has("kieu_di") && chon.kieu_di) truong.kieu_di = chon.kieu_di;
  if (hien.has("so_thich") && chon.so_thich.length) truong.so_thich = chon.so_thich.slice(0, cauHinh.so_thich_toi_da);
  if (hien.has("ngay_di") && chon.ngay_di) truong.ngay_di = chon.ngay_di;

  const tomTat = [`${soNgay} ngày`,
    hien.has("nguoi_lon") && `${chon.nguoi_lon} người lớn`,
    hien.has("tre_em") && chon.tre_em > 0 && `${chon.tre_em} trẻ em`,
    hien.has("lon_tuoi") && chon.lon_tuoi && "có người lớn tuổi",
    truong.kieu_di && KIEU_DI.find(([v]) => v === truong.kieu_di)[1].toLowerCase(),
    truong.so_thich && `thích ${truong.so_thich.map(v => SO_THICH.find(([k]) => k === v)[1].toLowerCase()).join(", ")}`,
    truong.ngay_di && `đi ngày ${truong.ngay_di.split("-").reverse().join("/")}`].filter(Boolean).join(" · ");

  function bamSoThich(v) {
    setChon(old => {
      if (old.so_thich.includes(v)) return { ...old, so_thich: old.so_thich.filter(x => x !== v) };
      const moi = [...old.so_thich, v];
      return { ...old, so_thich: moi.slice(Math.max(0, moi.length - cauHinh.so_thich_toi_da)) };  // quá số cho phép ⇒ bỏ lựa chọn cũ nhất
    });
  }

  return (
    <div className="khung khoi-trang">
      <p className="vet"><a href="#/">Trang chủ</a> / Lên kế hoạch</p>
      <h1 className="trang-h">Lên kế hoạch đi Huế</h1>
      <p className="khoi-p">Trợ lý xếp lịch theo buổi từ các điểm trong kho. Muốn đổi lịch thì quay lại đây điền lại.</p>
      <form className="lc" onSubmit={e => { e.preventDefault(); if (!pending) onSubmit(truong, tomTat); }}>
        {(hien.has("nguoi_lon") || hien.has("tre_em") || hien.has("lon_tuoi")) && (
          <fieldset className="lc-nhom">
            <legend className="lc-ten">Ai đi?</legend>
            <div className="lc-chip">
              {hien.has("nguoi_lon") && <SoDem id="lc-nguoi-lon" nhan="Người lớn" giaTri={chon.nguoi_lon} min={1} max={10} onDoi={v => doi("nguoi_lon", v)} />}
              {hien.has("tre_em") && <SoDem id="lc-tre-em" nhan="Trẻ em" giaTri={chon.tre_em} min={0} max={6} onDoi={v => doi("tre_em", v)} />}
              {hien.has("lon_tuoi") && (
                <label className="lc-hop"><input type="checkbox" checked={chon.lon_tuoi} onChange={e => doi("lon_tuoi", e.target.checked)} /> Có người lớn tuổi</label>
              )}
            </div>
          </fieldset>
        )}
        <fieldset className="lc-nhom">
          <legend className="lc-ten">Đi bao lâu, khi nào?</legend>
          <div className="lc-chip">
            <SoDem id="lc-so-ngay" nhan="Số ngày" giaTri={soNgay} min={1} max={cauHinh.so_ngay_toi_da} onDoi={v => doi("so_ngay", v)} />
            {hien.has("ngay_di") && (
              <label className="lc-hop">Ngày đi (không bắt buộc){" "}
                <input type="date" value={chon.ngay_di} min={ngayIso(homNay)} max={ngayIso(toiDa)} onChange={e => doi("ngay_di", e.target.value)} />
              </label>
            )}
          </div>
        </fieldset>
        {hien.has("kieu_di") && (
          <fieldset className="lc-nhom">
            <legend className="lc-ten">Đi kiểu nào? (không bắt buộc)</legend>
            <div className="lc-chip">
              {KIEU_DI.map(([v, nhan, giai]) => (
                <button key={v} type="button" className="chip chip-sm" aria-pressed={chon.kieu_di === v}
                        onClick={() => doi("kieu_di", chon.kieu_di === v ? null : v)}>{nhan} — {giai}</button>
              ))}
            </div>
            {chon.kieu_di && chon.kieu_di !== "nhe_nhang" && (chon.tre_em > 0 || chon.lon_tuoi) && (
              <p className="lc-tom">Có trẻ em hoặc người lớn tuổi: lịch giữ mức nhẹ nhàng, mỗi buổi một điểm.</p>
            )}
          </fieldset>
        )}
        {hien.has("so_thich") && (
          <fieldset className="lc-nhom">
            <legend className="lc-ten">Thích gì? {cauHinh.so_thich_toi_da > 1 ? `(tối đa ${cauHinh.so_thich_toi_da})` : "(chọn một)"}</legend>
            <div className="lc-chip">
              {SO_THICH.filter(([v]) => cauHinh.so_thich_hien.includes(v)).map(([v, nhan]) => (
                <button key={v} type="button" className="chip chip-sm" aria-pressed={chon.so_thich.includes(v)} onClick={() => bamSoThich(v)}>{nhan}</button>
              ))}
            </div>
          </fieldset>
        )}
        <p className="lc-tom" aria-live="polite">{tomTat}</p>
        <button className="nut nut-chinh lc-nut" type="submit" disabled={pending}>{pending ? "Trợ lý đang trả lời…" : `Xếp lịch ${soNgay} ngày`}</button>
      </form>
    </div>
  );
}

export function GioiThieu({ banDo, anh, muc }) {
  // `#/gioi-thieu/<mục>` ⇒ cuộn tới mục (sau lần `scrollTo(0, 0)` của `useRoute` lúc đổi hash — effect chạy sau khi trang đã vẽ)
  useEffect(() => {
    if (muc) document.getElementById(muc)?.scrollIntoView();
  }, [muc]);
  return (
    <div className="khung khoi-trang gioi-thieu">
      <p className="vet"><a href="#/">Trang chủ</a> / Giới thiệu</p>
      <h1 className="trang-h">Về Trợ lý Huế</h1>
      <h2>Trợ lý làm được gì</h2>
      <ul>
        <li>Trả lời câu hỏi về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, đi lại và vé tham quan ở Huế.</li>
        <li>Xếp lịch tham quan theo buổi từ các điểm trong kho (khi tính năng Lên kế hoạch bật).</li>
        <li>Khi kho không có, có thể tra thêm trên web — phần đó ghi rõ “Từ web (chưa kiểm)”.</li>
        {anh && <li>Hỏi bằng ảnh: trợ lý gợi ý tên nơi / món trong ảnh (có thể sai), bạn bấm chọn đúng tên rồi mới hỏi.</li>}
      </ul>
      <h2>Trả lời từ kho, có nguồn</h2>
      <p>Mỗi câu trả lời lấy từ kho tư liệu về Huế và ghi tên tài liệu đã dùng ở dòng “Nguồn”. Bấm tên để xem đoạn gốc hoặc đọc cả bài ở mục Khám phá.</p>
      <h2>Giới hạn</h2>
      <ul>
        <li>Trợ lý có thể sai. Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại trước khi đi.</li>
        <li>{banDo ? "Chưa có nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau). Bản đồ lịch trình chỉ ghim các điểm đã có toạ độ."
          : "Chưa có bản đồ, nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau)."}</li>
        <li>Câu hỏi ngoài chủ đề Huế sẽ được báo là ngoài phạm vi.</li>
      </ul>
      <h2>Dữ liệu của bạn</h2>
      <p>Trợ lý nhớ các câu hỏi trong một cuộc trò chuyện để hiểu câu hỏi tiếp theo: nhớ trong bộ nhớ máy chủ, tối đa 30 phút, qua một cookie chỉ dùng cho
        trò chuyện. Máy chủ không lưu chữ câu hỏi hay câu trả lời vào nhật ký. Nút “Cuộc trò chuyện mới” xoá phần đã nhớ.</p>
      <p>Để trả lời, câu hỏi được gửi tới dịch vụ mô hình AI (OpenAI); khi tra web, câu hỏi cũng được gửi tới dịch vụ tìm kiếm. Đừng gõ thông tin cá nhân
        vào câu hỏi.</p>
      {banDo && <p>Khi lịch có bản đồ, trình duyệt của bạn tải ảnh bản đồ từ máy chủ OpenStreetMap — máy chủ đó nhận địa chỉ IP và vùng bản đồ bạn
        đang xem (không nhận câu hỏi của bạn).</p>}
      {anh && <p>Ảnh bạn gửi được thu nhỏ, bỏ thông tin vị trí, gửi tới OpenAI để đoán tên, không lưu.</p>}
      <h2 id="nguon-anh">Nguồn ảnh</h2>
      <ul className="nguon-anh">
        {MOI_ANH.map(a => <li key={a.src}><GhiCong a={a} /></li>)}
      </ul>
    </div>
  );
}

function GhiCong({ a }) {
  const ngoai = { target: "_blank", rel: "noopener noreferrer" };
  return (
    <>
      {a.cho}. Ảnh: {a.tacGia}
      {a.giayPhep && <> · {a.linkGiayPhep ? <a href={a.linkGiayPhep} {...ngoai}>{a.giayPhep}</a> : a.giayPhep}</>}
      {" · "}<a href={a.nguon} {...ngoai}>{a.giayPhep ? "trang ảnh trên Wikimedia Commons" : "nguồn ảnh"}</a>
      {a.doi && <> · đã {a.doi}</>}
    </>
  );
}
