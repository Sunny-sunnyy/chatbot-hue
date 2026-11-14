import { Suspense, lazy, useEffect, useRef, useState } from "react";
import { boMaTrichDan } from "./markdown.js";
import { toaDoHopLe } from "./toaDo.js";
import { SourceLine } from "./SourceLine.jsx";
import { dungIcs } from "./lich_ics.js";
import { baiHref } from "./route.js";

const BanDoLich = lazy(() => import("./BanDoLich.jsx"));

// Thẻ lịch "Lên kế hoạch" bản 2 + lưu lịch (tách từ chat.jsx, đợt 0 giao diện H1; hành vi giữ nguyên).
export const MAP_PREFIX = "https://www.google.com/maps/search/";  // D11: chỉ nhận link bản đồ đúng gốc này (kiểm cả phía trình duyệt)

// "Lên kế hoạch" bản 2 (spec 5c.5): thẻ lịch vẽ TỪ KHUNG do code dựng (tên, buổi, giờ, ghi chú); câu model đổ vào theo `id_muc`, chưa tới ⇒
// "đang viết…". Loại mục chưa biết (đợt sau: ăn uống…) ⇒ bỏ qua, không lỗi. Nút "Sửa" điền lại biểu mẫu bằng đúng giá trị đã gửi.
const NHAN_BUOI_V2 = { sang: "Sáng", trua: "Trưa", chieu: "Chiều", toi: "Tối" };
const LOAI_MUC_V2 = new Set(["tham_quan", "hoat_dong_toi", "nghi"]);
const NHAN_MUC_V2 = { co_the_di_lai: "có thể đi lại", kiem_lich_dien: "kiểm lịch diễn trước khi đi" };  // cùng chữ với server (`NHAN_MUC`)
// Điểm nhấn 14/11 (User: Lên kế hoạch "đơn điệu"): nhãn + màu theo loại điểm (`loai_diem` của server, lấy từ bảng điểm) — màu luôn đi kèm chữ.
const NHAN_LOAI_DIEM = { di_tich: "Di tích", am_thuc: "Ẩm thực", thien_nhien: "Thiên nhiên", le_hoi_nghe_thuat: "Lễ hội, nghệ thuật", chup_anh: "Chụp ảnh" };

// Khoảnh khắc chính (mẫu 16, `c_nghien_cuu_wow.md`): mỗi ngày một dòng sông Hương đi QUA từng điểm theo thứ tự trong ngày, vẽ dần khi cuộn
// (lkh.css, chỉ dưới html.hieu-ung; giảm chuyển động ⇒ hiện sẵn cả đường). Toạ độ = tâm chấm buổi (màn rộng) hoặc tâm ảnh (màn hẹp), đo lại khi
// khung đổi cỡ (ảnh tải xong, đổi khổ). Trang trí: aria-hidden, không chặn bấm.
function SongNgay({ dongRef, khoa }) {
  const [d, setD] = useState("");
  useEffect(() => {  // useEffect (không layout): ref của <ul> anh em đứng SAU thành phần này mới chắc đã gắn
    const ul = dongRef.current;
    if (!ul || typeof ResizeObserver === "undefined") return undefined;
    const ve = () => {
      const goc = ul.getBoundingClientRect();
      const diem = [...ul.querySelectorAll(":scope > .lkh-muc")].map(li => [".lkh-cham-buoi", ".lich-anh img", ".lkh-khong-anh"]
        .map(c => li.querySelector(c)).find(e => e && e.offsetParent !== null)).filter(Boolean).map(e => {
          const b = e.getBoundingClientRect();
          return [Math.round(b.left + b.width / 2 - goc.left), Math.round(b.top + b.height / 2 - goc.top)];
        });
      if (diem.length < 2) { setD(""); return; }
      let p = `M${diem[0][0]} ${diem[0][1]}`;
      diem.slice(1).forEach(([x, y], i) => {
        const [px, py] = diem[i], w = (i % 2 ? -1 : 1) * 22, dy = y - py;  // uốn trái / phải xen kẽ như khúc sông
        p += ` C${px + w} ${py + dy / 3}, ${x + w} ${y - dy / 3}, ${x} ${y}`;
      });
      setD(p);
    };
    ve();
    const ro = new ResizeObserver(ve);
    ro.observe(ul);
    return () => ro.disconnect();
  }, [dongRef, khoa]);
  if (!d) return null;
  return <svg className="lkh-song-ngay" aria-hidden="true"><path d={d} pathLength="1" /></svg>;
}

function NgayLich({ ng, turnKey, cau, xong, theoNgay, i, an }) {
  const dongRef = useRef(null);
  const muc = ng.muc.filter(m => LOAI_MUC_V2.has(m.loai));
  return (
    <section id={`ngay-${turnKey}-${ng.ngay}`} className="lich-ngay hien" style={{ "--n": i }} aria-label={`Ngày ${ng.ngay}`}>
      <h3>Ngày {ng.ngay}{ng.ngay_thang ? ` · ${THU_V2[ng.thu]} ${ng.ngay_thang.split("-").reverse().join("/")}` : ""}
        {ng.chang?.length > 0 && <span className="lkh-chang">{ng.chang.join(" → ")}</span>}</h3>
      <div className="lkh-dong-khung">
        <SongNgay dongRef={dongRef} khoa={muc.map(m => m.id_muc).join(",")} />
        <ul className="lkh-dong" ref={dongRef}>
          {muc.map((m, k) => {
            const loai = (m.loai_diem || []).filter(x => NHAN_LOAI_DIEM[x]);
            return [
              m.phut_di != null && <li key={`${m.id_muc}-di`} className="lkh-di">khoảng {m.phut_di} phút đi</li>,
              <li key={m.id_muc} className={`lkh-muc lkh-${MAU_BUOI[m.buoi] || "sang"} ${m.loai === "nghi" ? "lkh-nghi" : ""} ${loai[0] ? `lkh-l-${loai[0]}` : ""}`}
                  style={{ "--k": k }}>
                <span className="lkh-cham-buoi" aria-hidden="true">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d={IC_BUOI[m.buoi] || IC_BUOI.sang} /></svg>
                </span>
                {anhHopLe(m.anh) ? <AnhLich anh={m.anh} ten={m.ten} /> : <span className="lkh-khong-anh" aria-hidden="true" />}
                <div className="lkh-than">
                  <span className="lich-buoi">{NHAN_BUOI_V2[m.buoi] || m.buoi}{m.gio ? ` · ${m.gio}` : ""}</span>
                  <span className="lich-ten">{m.ten}{(m.nhan || []).filter(x => NHAN_MUC_V2[x]).map(x => <small key={x}>{NHAN_MUC_V2[x]}</small>)}</span>
                  {loai.length > 0 && <span className="lkh-loai">{loai.map(x => <small key={x} className={`lkh-loai-${x}`}>{NHAN_LOAI_DIEM[x]}</small>)}</span>}
                  {m.loai !== "nghi" && (
                    <span className="lich-cau">{cau[m.id_muc] != null ? <span className="lkh-cau-moi">{boMaTrichDan(cau[m.id_muc])}</span>
                      : !xong && <><span className="sr-only">đang viết…</span><span className="lkh-xuong" aria-hidden="true" /><span className="lkh-xuong lkh-ngan" aria-hidden="true" /></>}
                    </span>
                  )}
                </div>
              </li>,
            ];
          })}
        </ul>
      </div>
      {an?.length > 0 && <AnUong an={an} />}
      {theoNgay(ng.ngay).length > 0 && <ul className="lkh-du-bao">{theoNgay(ng.ngay).map((g, j) => <li key={j}>{g.cau}</li>)}</ul>}
    </section>
  );
}
const THU_V2 = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật"];  // `thu` của server: thứ Hai = 0

// Đợt 2 (B): ảnh tự host của điểm (cờ `anh_lich`) — chỉ vẽ khi `src` dưới /anh/lich/ và trang ảnh là Wikimedia Commons (kiểm cả phía trình
// duyệt như link bản đồ); điểm không có ảnh ⇒ không vẽ gì (không ảnh thay). Không hiện dòng ghi công (User 14/11: nguồn chỉ còn trong bảng
// dữ liệu). `src` của server tính từ gốc `public/` ⇒ ghép `BASE_URL` (/static/) như ảnh cổng (`anh.js`).
const ANH_LICH = "/anh/lich/";
const TRANG_COMMONS = "https://commons.wikimedia.org/";
function anhHopLe(a) {
  return !!a && typeof a.src === "string" && a.src.startsWith(ANH_LICH) && !a.src.slice(ANH_LICH.length).includes("/")
    && typeof a.trang === "string" && a.trang.startsWith(TRANG_COMMONS) && !!a.tac_gia && !!a.giay_phep;
}

function AnhLich({ anh, ten }) {
  return (
    <figure className="lich-anh">
      <img src={`${import.meta.env.BASE_URL}${anh.src.slice(1)}`} alt={anh.chu_thich ? `${ten} — ${anh.chu_thich}` : ten} loading="lazy" decoding="async" />
    </figure>
  );
}

const KIEU_V2 = { nhe_nhang: "nhẹ nhàng", can_bang: "cân bằng", kham_pha: "khám phá nhiều" };
const MAU_BUOI = { sang: "sang", trua: "sang", chieu: "chieu", toi: "toi" };
const IC_BUOI = { sang: "M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",
                  chieu: "M17 18a5 5 0 0 0-10 0M12 9V3M4.2 10.2l1.4 1.4M1 18h2M21 18h2M18.4 11.6l1.4-1.4M23 22H1",
                  toi: "M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z" };
IC_BUOI.trua = IC_BUOI.sang;

// H1 (14/11): thẻ lịch kiểu dòng thời gian (bản mẫu `data/ui_mau_2026-11-14/h1/len_ke_hoach.html`). Giữ lớp bộ đo bám: .lich-v2 .lich-hieu
// .lich-ngay (aria-label "Ngày N") .lich-ten .lich-cau .lich-anh .lich-ghi-chu .lich. Ghi chú dự báo có `ngay` ⇒ đặt dưới đúng ngày (B, trường mới).
// Phút đi `phut_di` (B) chỉ có giữa hai mục cùng buổi ⇒ chỉ vẽ khi có trường, không đoán.
export function LichV2({ turn, onEditPlan }) {
  const lich = turn.lichV2;
  const cau = turn.cauV2 || {};
  const xong = turn.phase === "done";
  const ts = lich.tham_so || {};
  const banDo = lich.ngay.some(ng => ng.muc.some(m => toaDoHopLe(m.toa_do)))
    ? lich.ngay.flatMap(ng => ng.muc.filter(m => m.loai === "tham_quan" || m.loai === "hoat_dong_toi")
        .filter(m => typeof m.map_url === "string" && m.map_url.startsWith(MAP_PREFIX))
        .map((m, i) => ({ ten: m.ten, map_url: m.map_url, ngay: ng.ngay, buoi: m.buoi, thu_tu: i + 1, toa_do: m.toa_do })))
    : [];
  const theoNgay = n => lich.ghi_chu.filter(g => g.ngay === n);
  const chung = lich.ghi_chu.filter(g => g.ngay == null);
  const ngayDau = lich.ngay[0];
  const diCung = [ts.nguoi_lon ? `${ts.nguoi_lon} người lớn` : null, ts.tre_em ? `${ts.tre_em} trẻ em` : null, ts.lon_tuoi ? "có người lớn tuổi" : null]
    .filter(Boolean).join(" · ");
  return (
    <div className="bubble lich-v2">
      <div className="lkh-thanh">
        {ngayDau?.ngay_thang && <div><small>Bắt đầu</small><b>{THU_V2[ngayDau.thu]} {ngayDau.ngay_thang.split("-").reverse().join("/")}</b></div>}
        {diCung && <div><small>Đi cùng</small><b>{diCung}</b></div>}
        <div><small>Thời gian</small><b>{lich.ngay.length} ngày{KIEU_V2[ts.kieu_di] ? ` · ${KIEU_V2[ts.kieu_di]}` : ""}</b></div>
      </div>
      <p className="lich-hieu">{lich.minh_hieu.replaceAll("**", "")}</p>
      {/* Sửa lịch bằng lời (B, cờ `sua_lich_v2`): `lich.thay_doi` = [{cau, duoc}] — câu do CODE viết đã có sẵn động từ ("Đã bỏ…", "Chưa làm…")
          ⇒ vẽ nguyên câu, màu theo `duoc`; lượt không sửa ⇒ không có khối này */}
      {Array.isArray(lich.thay_doi) && lich.thay_doi.length > 0 && (
        <ul className="lkh-doi" aria-label="Thay đổi của lịch">
          {lich.thay_doi.map((d, i) => <li key={i} className={d.duoc ? "lkh-doi-duoc" : "lkh-doi-khong"}>{d.duoc ? "" : "Không đổi được: "}{d.cau.replace(/^Không đổi được: /, "")}</li>)}
        </ul>
      )}
      <section className="lkh-tong" aria-label="Tổng quan">
        <p className="lkh-tong-h">Tổng quan</p>
        <ol>{lich.ngay.map(ng => (
          <li key={ng.ngay}><a href={`#ngay-${turn.key}-${ng.ngay}`} onClick={e => { e.preventDefault();
            document.getElementById(`ngay-${turn.key}-${ng.ngay}`)?.scrollIntoView({ behavior: "smooth", block: "start" }); }}>Ngày {ng.ngay}</a>{" "}
            {ng.muc.filter(m => m.loai !== "nghi").map(m => m.ten).join(" → ")}</li>
        ))}</ol>
      </section>
      <div className="lkh-ngay-ds">
        {lich.ngay.map((ng, i) => <NgayLich key={ng.ngay} ng={ng} turnKey={turn.key} cau={cau} xong={xong} theoNgay={theoNgay} i={i}
                                              an={(lich.an || []).filter(a => a.ngay === ng.ngay)} />)}
      </div>
      {banDo.length > 0 && <Suspense fallback={null}><BanDoLich items={banDo} /></Suspense>}
      {chung.length > 0 && (
        <div className="lich-ghi-chu">
          <p className="font-semibold">Ghi chú của lịch</p>
          <ul>{chung.map((g, i) => <li key={i} className={`lkh-gc-${g.ma || "khac"}`}>{g.cau}</li>)}</ul>
        </div>
      )}
      {lich.o_dau && <NoiO o={lich.o_dau} />}
      {turn.sources?.length > 0 && <SourceLine turn={turn} />}
      {turn.notice && <p className="notice">{turn.notice}</p>}
      {xong && (
        <div className="lich">
          <LuuLich getText={() => vanBanLich(turn, boMaTrichDan(turn.text || ""), [])} />
          <NutIcs lich={lich} cau={cau} />
          {onEditPlan && <button type="button" className="retry" onClick={() => onEditPlan(null, turn.truong)}>Sửa — điền lại biểu mẫu</button>}
        </div>
      )}
    </div>
  );
}

// Gợi ý nơi ở (B, cờ `luu_tru_lich`): khối do CODE chọn (khu cả chuyến, ≤ 5 cơ sở, lý do, nhãn "chưa kiểm giá"). Link tìm phòng chỉ nhận đúng gốc
// LINK_TIM_PHONG (kiểm cả phía trình duyệt như link bản đồ), mở tab mới khi bấm; không giá, không "còn phòng".
const LINK_TIM_PHONG = "https://www.booking.com/searchresults.html?ss=";
// Quán ăn gợi ý (cờ `quan_lich`, code chọn ≤ 2 quán cùng cụm ≤ 2 km): quán kho ⇒ "Đọc bài"; nguồn mở ⇒ nhãn "chưa kiểm" + link bản đồ.
// Link chỉ nhận đúng gốc bản đồ của lịch (như link điểm); không giờ / giá / điện thoại.
function AnUong({ an }) {
  return (
    <ul className="lkh-an" aria-label="Ăn uống gợi ý">
      {an.map(a => (
        <li key={a.bua}>
          <span className="lkh-an-h">{a.bua === "trua" ? "Ăn trưa" : "Ăn tối"} gần {a.gan}</span>
          {a.quan.map(q => (
            <span key={q.ten} className="lkh-an-q">
              {typeof q.bai_id === "string" ? <a href={baiHref(q.bai_id)}>{q.ten}</a>
                : typeof q.map_url === "string" && q.map_url.startsWith(MAP_PREFIX)
                  ? <a href={q.map_url} target="_blank" rel="noopener noreferrer">{q.ten}</a> : q.ten}
              <small>{q.loai}{q.nhan ? ` · ${q.nhan}` : ""}</small>
            </span>
          ))}
        </li>
      ))}
    </ul>
  );
}

function NoiO({ o }) {
  const ds = (o.co_so || []).filter(c => c.ten);
  if (!ds.length) return null;
  return (
    <section className="lkh-o" aria-label="Nơi ở gợi ý">
      <p className="lkh-o-h">Nơi ở gợi ý: khu {o.ten_khu}</p>
      <p className="lkh-o-ly">{o.ly_do}</p>
      <ul>{ds.map(c => (
        <li key={c.ten}>
          <span className="lkh-o-ten">{c.ten}</span> <small>{c.xep_hang}</small>
          {c.dia_chi && <span className="lkh-o-dc">{c.dia_chi}</span>}
          {typeof c.link === "string" && c.link.startsWith(LINK_TIM_PHONG) &&
            <a href={c.link} target="_blank" rel="noopener noreferrer">Tìm phòng</a>}
        </li>
      ))}</ul>
      <p className="lkh-o-nhan">{o.nhan} Nguồn: {o.nguon}.</p>
    </section>
  );
}

// Việc agent (4) 14/11: thêm lịch vào lịch điện thoại / máy tính — tệp .ics do code dựng từ khung (lich_ics.js), tải về bằng Blob (không gửi đi).
// Lịch không có ngày đi ⇒ không đoán ngày: thay nút bằng dòng nhắc.
function NutIcs({ lich, cau }) {
  const [bao, setBao] = useState("");
  const coNgay = lich.ngay.every(ng => ng.ngay_thang);
  if (!coNgay) return <p className="lkh-ics-nhac">Chọn ngày đi ở biểu mẫu để thêm lịch vào lịch điện thoại.</p>;
  function taiIcs() {
    const sach = Object.fromEntries(Object.entries(cau || {}).map(([k, v]) => [k, boMaTrichDan(v)]));
    const kq = dungIcs(lich, sach);
    if (!kq) return;
    const url = URL.createObjectURL(new Blob([kq.ics], { type: "text/calendar;charset=utf-8" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "lich-trinh-hue.ics";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setBao(`Đã tạo ${kq.soSuKien} sự kiện${kq.soBo ? ` (${kq.soBo} điểm không có giờ cụ thể nên không thêm)` : ""}.`);
  }
  return (
    <span className="lkh-ics">
      <button type="button" className="retry" onClick={taiIcs}>Thêm vào lịch (.ics)</button>
      <span className="text-sm text-muted" role="status">{bao}</span>
    </span>
  );
}

// Việc nhỏ (1) 08/11: lưu lịch ra chữ thường — chữ lấy từ phần đang hiện (không gọi server, không gửi đi đâu).
const TEN_FILE_LICH = "lich-trinh-hue.txt";
const DONG_CUOI_LICH = "Từ Trợ lý Huế — có thể sai; giờ mở cửa, giá vé có thể đã thay đổi, hãy kiểm lại trước khi đi.";

export function vanBanLich(turn, answerText, items) {
  const links = items.filter(item => typeof item.map_url === "string" && item.map_url.startsWith(MAP_PREFIX));
  const diem = links.map(i => (i.ngay ? `Ngày ${i.ngay} · ${i.thu_tu}. ${i.ten}: ${i.map_url}` : `- ${i.ten}: ${i.map_url}`));
  return [turn.question + (turn.summary ? ` · ${turn.summary}` : ""), "", answerText.trim(),
          ...(diem.length ? ["", "Bản đồ từng điểm:", ...diem] : []), "", DONG_CUOI_LICH, ""].join("\n");
}

export function LuuLich({ getText }) {
  const [bao, setBao] = useState("");
  async function saoChep() {
    try {
      await navigator.clipboard.writeText(getText());  // chỉ có ở trang https / localhost
      setBao("Đã sao chép lịch.");
    } catch {
      setBao("Trình duyệt không cho sao chép — dùng nút Tải về.");
    }
  }
  function taiVe() {
    const url = URL.createObjectURL(new Blob([getText()], { type: "text/plain;charset=utf-8" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = TEN_FILE_LICH;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setBao("Đã tải về " + TEN_FILE_LICH + ".");
  }
  return (
    <div className="luu-lich">
      <button type="button" className="retry" onClick={saoChep}>Sao chép lịch</button>
      <button type="button" className="retry" onClick={taiVe}>Tải về (.txt)</button>
      <span className="text-sm text-muted" role="status">{bao}</span>
    </div>
  );
}
