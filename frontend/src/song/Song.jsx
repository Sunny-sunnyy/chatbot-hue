// Giao diện "Dòng sông dẫn đường" (việc X13, 22/11/2026 — nhóm chọn trên ảnh dựng thử, hồ sơ riêng tư `data/giao_dien_2026-11-22/`).
// MỘT hình dùng ba nơi: con sông Hương là bố cục màn đầu Trang chủ (sáu lối vào = sáu bến ở mép bờ), là hình lúc chờ ở Hỏi đáp (khúc sông + con đò),
// và là trục thời gian của trang Lên kế hoạch. Chỉ lớp nhìn: chữ, ô hỏi, lối vào, luồng giữ như cũ. Hình sông tự vẽ giản lược, không lấy hình học bản đồ.
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { giamChuyenDong } from "../hieuUng.js";
import { ANH_DAU_TRANG } from "../anh.js";
import { GOI_Y } from "../chung.jsx";
import { linhVuc } from "./nhin.js";
import { Do, SONG_DOC, SONG_NGANG } from "./hinh.jsx";
import { baiHref } from "../route.js";

function Icon({ d, co = 24 }) {
  return (
    <svg width={co} height={co} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true"><path d={d} /></svg>
  );
}

function OHoi({ cau, setCau, submit, onAsk, soChip = 5 }) {
  return (
    <>
      <form className="hoi vao" style={{ "--n": 2 }} onSubmit={submit}>
        <label className="sr-only" htmlFor="hoi-lon">Câu hỏi cho Trợ lý Huế</label>
        <input id="hoi-lon" className="hoi-o" value={cau} onChange={e => setCau(e.target.value)} placeholder="Ví dụ: chiều nay nên đi lăng nào?"
               autoComplete="off" maxLength={500} />
        <button className="nut nut-chinh nhan-nut" type="submit">Hỏi</button>
      </form>
      <div className="goi-y" aria-label="Câu hỏi gợi ý">
        {GOI_Y.slice(0, soChip).map((q, i) => (
          <button key={q} className="chip vao nhan-nut" style={{ "--n": 3 + i }} type="button" onClick={() => onAsk(q)}>{q}</button>
        ))}
      </div>
    </>
  );
}

// ───────── Màn đầu Trang chủ: con sông LÀM bố cục — chữ và ô hỏi ở một bờ, sáu lối vào là sáu bến nằm trên chính đường cong.
// Hình sông tự vẽ giản lược (khúc uốn + hai cồn), không lấy hình học từ dữ liệu bản đồ.
const TAM_RONG = "M1440 28 C1250 54 1010 134 960 267 C915 391 1120 462 1200 568 C1270 666 1100 755 930 800";  // chữ S ở nửa phải: đúng chỗ ảnh có cầu + mặt nước
const RONG = 250, RONG_HEP = 84;
const TAM_HEP = SONG_DOC;
// Sáu bến ở màn rộng, đặt tay theo hình sông: vị trí dọc dòng (0–1), bờ nào ("a" = bờ trái theo chiều chảy, "b" = bờ phải) và nhãn nằm phía nào của bến —
// chọn sao cho chữ luôn nằm trên nền sương, không đè ảnh và không đè cột chữ bên trái.
const T_RONG = [.06, .37, .435, .60, .80, .99], BO = ["b", "a", "a", "b", "a", "a"], NHAN = ["duoi", "trai", "trai", "phai", "trai", "tren"];  // "tren" = bên trái nhưng nhích LÊN: ở bến cuối bờ sông chạy chéo xuống trái, nhãn ngang tầm bến sẽ chạm vào ảnh (đo tương phản: 1,0 : 1 ở cuối dòng)
const T_HEP = [.1, .26, .42, .58, .74, .9];
// Dưới 1140 px cột chữ và con sông chữ S không còn đủ chỗ đứng cạnh nhau (đếm: 1024 px nhãn đè câu dẫn, 768 px ô hỏi đè sông) ⇒ bố cục DỌC như điện thoại.
// Mốc này phải trùng mốc của khối màn đầu trong song.css.
const MAN_DOC = "(max-width: 1140px)";

export function HeroSong({ nhanh, thoiTiet, ...hoi }) {
  const ref = useRef(null);
  const [vt, setVt] = useState([]);
  const [rong, setRong] = useState(RONG);  // bề dày nét sông ở màn rộng: co theo chiều cao màn đầu (màn thấp mà giữ 250 px thì hai khúc uốn dồn vào nhau)
  // Con đò + nét chạy là chuyển động tự chạy quá 5 giây ⇒ có nút dừng (như nút "Dừng ảnh" của bản cũ); máy bật giảm chuyển động ⇒ dừng sẵn.
  const [dung, setDung] = useState(() => giamChuyenDong());
  useEffect(() => {
    ref.current?.querySelectorAll("svg.h1-ve").forEach(s => (dung ? s.pauseAnimations() : s.unpauseAnimations()));
  }, [dung]);
  useLayoutEffect(() => {
    const tinh = () => {
      const goc = ref.current;
      if (!goc) return;
      const hep = window.matchMedia(MAN_DOC).matches;
      goc.style.setProperty("--h1-tren", `${Math.round(goc.getBoundingClientRect().top + window.scrollY)}px`);  // song.css: chiều cao màn đầu = khung nhìn trừ phần này
      const duong = goc.querySelector(hep ? ".h1-tam-hep" : ".h1-tam-rong");
      const vb = duong.ownerSVGElement.viewBox.baseVal, dai = duong.getTotalLength();
      const hop = goc.querySelector(".h1-song").getBoundingClientRect();
      const px = q => ({ x: (q.x / vb.width) * hop.width, y: (q.y / vb.height) * hop.height });
      const rongThat = RONG * Math.min(1, hop.height / 800);  // hình vẽ trong ô cao 800 px
      setRong(rongThat);
      setVt(nhanh.map((_, i) => {
        const d = (hep ? T_HEP : T_RONG)[i] * dai, p = px(duong.getPointAtLength(d)), q = px(duong.getPointAtLength(Math.min(d + 2, dai)));
        if (hep) return { x: p.x, y: p.y };  // điện thoại: bến nằm giữa dòng, nhãn so le hai bên
        // màn rộng: bến nằm ở MÉP BỜ (đúng nghĩa bến) — lùi nửa bề rộng sông theo pháp tuyến, chọn bờ trái (hoặc bờ dưới khi sông chảy ngang) ⇒ chữ nằm trên nền, không đè ảnh
        const dai2 = Math.hypot(q.x - p.x, q.y - p.y) || 1, tx = (q.x - p.x) / dai2, ty = (q.y - p.y) / dai2, h = rongThat / 2;
        const v = BO[i] === "a" ? { x: p.x - ty * h, y: p.y + tx * h } : { x: p.x + ty * h, y: p.y - tx * h };
        v.x = Math.min(v.x, hop.width - 44);            // bến tròn (bán kính 32) luôn nằm trọn trong màn
        v.cho = Math.max(120, hop.width - v.x - 58);    // chỗ còn lại bên PHẢI bến cho nhãn nằm bên phải (màn 1101–1340 px: dòng mô tả tự xuống dòng thay vì bị cắt)
        return v;
      }));
    };
    tinh();
    window.addEventListener("resize", tinh);
    return () => window.removeEventListener("resize", tinh);
  }, [nhanh.length]);
  const song = (lop, d, vb, rong) => (
    <svg className={`h1-ve ${lop}`} viewBox={vb} preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id={`g-${lop}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#0A4E4A" stopOpacity=".28" /><stop offset=".5" stopColor="#0A4E4A" stopOpacity=".1" /><stop offset=".8" stopColor="#0A4E4A" stopOpacity=".22" /><stop offset="1" stopColor="#083538" stopOpacity=".92" />
        </linearGradient>
        <mask id={`m-${lop}`} maskUnits="userSpaceOnUse">
          <path className="h1-mat" d={d} pathLength="1" fill="none" stroke="#fff" strokeWidth={rong} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        </mask>
      </defs>
      <path className="h1-bo" d={d} pathLength="1" fill="none" strokeWidth={rong + 18} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      <g mask={`url(#m-${lop})`}>
        <image href={ANH_DAU_TRANG.song.src} x={lop === "rong" ? "9%" : "-60%"} y="0" width={lop === "rong" ? "100%" : "220%"} height="100%" preserveAspectRatio="xMidYMid slice" />
        <rect className="h1-nuoc" x="0" y="0" width="100%" height="100%" fill={`url(#g-${lop})`} />
      </g>
      <path className={`h1-tam ${lop === "rong" ? "h1-tam-rong" : "h1-tam-hep"}`} id={`tam-${lop}`} d={d} fill="none" vectorEffect="non-scaling-stroke" />
      <Do duong={`tam-${lop}`} to={lop === "rong" ? 2 : 1.5} giay={44} batDau="-13s" />
    </svg>
  );
  return (
    <section className={`h1-hero ${dung ? "h1-dung-lai" : ""}`} aria-labelledby="hero-h" ref={ref}>
      <div className="h1-song">
        {song("rong", TAM_RONG, "0 0 1440 800", rong)}
        {song("hep", TAM_HEP, "0 0 390 640", RONG_HEP)}
        <nav className="h1-ben-ds" aria-label="Lối vào nhanh">
          {nhanh.map((n, i) => (
            <a key={n.href + n.ten} href={n.href} className={`h1-ben h1-ben-${i} h1-nhan-${NHAN[i]} nhan-nut`}
               style={{ "--x": `${vt[i]?.x ?? 0}px`, "--y": `${vt[i]?.y ?? 0}px`, "--cho": `${vt[i]?.cho ?? 240}px`, "--n": i }}>
              <span className={`h1-cham tc-bt-${n.mau}`}><Icon d={n.d} /></span>
              <span className="h1-nhan"><b>{n.ten}</b><small>{n.mo}</small></span>
            </a>
          ))}
        </nav>
      </div>
      <div className="h1-chu">
        <h1 id="hero-h" className="hero-h vao" style={{ "--n": 0 }}>Hỏi về Huế, như hỏi người bản xứ</h1>
        <p className="hero-p vao" style={{ "--n": 1 }}>Trả lời từ kho tư liệu về món ăn, di tích, lễ hội Huế — kèm tên tài liệu để bạn tự kiểm.</p>
        <OHoi {...hoi} soChip={5} />
        {thoiTiet}
      </div>
      {!giamChuyenDong() && <button type="button" className="h1-dung" aria-pressed={dung} onClick={() => setDung(!dung)}>{dung ? "Chạy tiếp" : "Dừng chuyển động"}</button>}
    </section>
  );
}

// ───────── Lúc chờ ở Hỏi đáp (cả ba hướng dùng chung khung, khác hình): bước THẬT + tên bài đã tìm thấy.
// Tên bài hiện nay server chưa gửi (chỉ gửi số đoạn) ⇒ bản thử đọc `window.__mau_cho` (dữ liệu mẫu đúng khuôn sự kiện sẽ thêm); không có ⇒ không vẽ bến nào.
export function ChoSong({ dongBuoc, daTim }) {
  // `daTim` = trường `bai` của sự kiện `searched` ([{title, bai_id}], cộng dồn, server đã lọc); giao diện tự đặt trần 6 bến, phần còn lại gộp thành "+k bài".
  const tat = (daTim?.length ? daTim : (typeof window !== "undefined" && Array.isArray(window.__mau_cho) ? window.__mau_cho : []))
    .map(b => (typeof b === "string" ? { title: b, bai_id: null } : b));
  const ten = tat.slice(0, 6);
  return (
    <div className="cho-thu">
      <div className="cho-hinh" aria-hidden="true">
        <svg viewBox="0 0 600 44" preserveAspectRatio="none">
          <path id="cho-song" className="net-song" d={SONG_NGANG} vectorEffect="non-scaling-stroke" />
          <path className="net-song net-song-chay" d={SONG_NGANG} vectorEffect="non-scaling-stroke" />
          <Do duong="cho-song" />
        </svg>
      </div>
      <p className="buoc-dang">{dongBuoc}</p>
      {ten.length > 0 && (
        <>
          <p className="cho-nhan">Đã tìm thấy {tat.length} bài<span className="cho-nhan-them"> — bấm tên để đọc trong lúc chờ</span></p>
          <ul className="cho-ben">
            {ten.map((b, i) => (
              <li key={b.title} style={{ "--n": i }} data-lv={linhVuc(b.bai_id)}><span className="cho-so" aria-hidden="true" />
                {b.bai_id ? <a href={baiHref(b.bai_id)} target="_blank" rel="noopener">{b.title}</a> : b.title}</li>
            ))}
            {tat.length > ten.length && <li className="cho-them" style={{ "--n": ten.length }}>+{tat.length - ten.length} bài</li>}
          </ul>
        </>
      )}
    </div>
  );
}
