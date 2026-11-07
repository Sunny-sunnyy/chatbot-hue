import { useEffect, useMemo, useState } from "react";
import { renderArticleHtml } from "./markdown.js";
import { baiHref } from "./route.js";

// Các trang của cổng đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` D9–D12), bản mẫu 2 "Sông Hương".
// Thẻ bài chỉ hiện trường kho có (tên, loại, tóm tắt) — không sao, không "Liên hệ", không giờ / giá chung chung (D10). Chưa có ảnh được phép ⇒ khối
// hoa văn giữ chỗ (Q-U2 (b): ảnh Commons vào sau khi User kiểm).

// 5 lĩnh vực kho (mã = tên thư mục); thứ tự như bản mẫu.
export const LINH_VUC = [
  { id: "foods", ten: "Ẩm thực", mo: "Món Huế, quán ăn, cà phê, đặc sản",
    icon: "M3 12h18a9 8 0 0 1-18 0zM8 8c0-2 2-2 2-4M13 8c0-2 2-2 2-4" },
  { id: "heritages", ten: "Di tích", mo: "Kinh thành, lăng tẩm, chùa, di sản",
    icon: "M2 21h20M4 21V11h16v10M1 11l11-8 11 8M9 21v-6h6v6" },
  { id: "festivals", ten: "Lễ hội", mo: "Lễ cung đình, lễ dân gian, Festival",
    icon: "M12 2v3M7 6h10l2 4-2 9H7l-2-9zM9 19v3M15 19v3" },
  { id: "performing_arts", ten: "Nghệ thuật biểu diễn", mo: "Nhã nhạc, ca Huế, tuồng",
    icon: "M12 20V5l8-2v13M12 20a3 3 0 1 1-3-3h3M20 16a3 3 0 1 1-3-3h3" },
  { id: "travel", ten: "Đi lại và tham quan", mo: "Điểm đến, vé tham quan, dịch vụ",
    icon: "M2 17c4-3 6 3 10 0s6 3 10 0M6 14l3-8h6l3 8" },
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

function Icon({ d, size = 26 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true">
      <path d={d} />
    </svg>
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
          <span className="kp-ic"><Icon d={lv.icon} /></span>
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
    <div className="khung khoi-trang">
      <p className="vet"><a href="#/">Trang chủ</a> / Khám phá</p>
      <h1 className="trang-h">Khám phá Huế</h1>
      <p className="khoi-p">Năm chủ đề của kho tư liệu — đọc bài gốc mà trợ lý dùng để trả lời.</p>
      <O5LinhVuc bai={bai} />
    </div>
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
        </aside>
      </div>
    </div>
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

export function GioiThieu() {
  return (
    <div className="khung khoi-trang gioi-thieu">
      <p className="vet"><a href="#/">Trang chủ</a> / Giới thiệu</p>
      <h1 className="trang-h">Về Trợ lý Huế</h1>
      <h2>Trợ lý làm được gì</h2>
      <ul>
        <li>Trả lời câu hỏi về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, đi lại và vé tham quan ở Huế.</li>
        <li>Xếp lịch tham quan theo buổi từ các điểm trong kho (khi tính năng Lên kế hoạch bật).</li>
        <li>Khi kho không có, có thể tra thêm trên web — phần đó ghi rõ “Từ web (chưa kiểm)”.</li>
      </ul>
      <h2>Trả lời từ kho, có nguồn</h2>
      <p>Mỗi câu trả lời lấy từ kho tư liệu về Huế và ghi tên tài liệu đã dùng ở dòng “Nguồn”. Bấm tên để xem đoạn gốc hoặc đọc cả bài ở mục Khám phá.</p>
      <h2>Giới hạn</h2>
      <ul>
        <li>Trợ lý có thể sai. Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại trước khi đi.</li>
        <li>Chưa có bản đồ, nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau).</li>
        <li>Câu hỏi ngoài chủ đề Huế sẽ được báo là ngoài phạm vi.</li>
      </ul>
      <h2>Dữ liệu của bạn</h2>
      <p>Trợ lý nhớ các câu hỏi trong một cuộc trò chuyện để hiểu câu hỏi tiếp theo: nhớ trong bộ nhớ máy chủ, tối đa 30 phút, qua một cookie chỉ dùng cho
        trò chuyện. Máy chủ không lưu chữ câu hỏi hay câu trả lời vào nhật ký. Nút “Cuộc trò chuyện mới” xoá phần đã nhớ.</p>
      <p>Để trả lời, câu hỏi được gửi tới dịch vụ mô hình AI (OpenAI); khi tra web, câu hỏi cũng được gửi tới dịch vụ tìm kiếm. Đừng gõ thông tin cá nhân
        vào câu hỏi.</p>
    </div>
  );
}
