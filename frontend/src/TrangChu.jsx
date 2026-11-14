import { useState } from "react";
import { ANH_DAU_TRANG, ANH_LINH_VUC, GP, MAN_NHO } from "./anh.js";
import { GOI_Y, LINH_VUC, soBai } from "./chung.jsx";
import { baiHref } from "./route.js";
import "./tc.css";

// Trang chủ H1 "Sông Hương" (bản mẫu `data/ui_mau_2026-11-14/h1/trang_chu.html`, User duyệt 14/11). Không thêm số liệu / lời hứa mới:
// mọi chữ là chữ trang cũ hoặc tên điểm + mô tả ngắn đã có trong bài kho; ảnh chỉ là ảnh đã có ghi công.

// Ảnh đầu trang đổi lần lượt (B, `b_hieu_ung_tham_khao.md` §3): chuyển mờ bằng CSS; có nút Dừng (WCAG 2.2.2 — nội dung tự đổi > 5 s);
// máy giảm chuyển động ⇒ chỉ ảnh đầu, đứng yên.
const ANH_HERO = [ANH_DAU_TRANG.song, ANH_DAU_TRANG.ngoMon, ANH_LINH_VUC.heritages];

// Lối vào nhanh: chỉ dẫn tới chỗ đã có trên trang (không câu hỏi soạn sẵn mới). `co` = cờ phải bật mới hiện.
const NHANH = [
  { href: "#/kham-pha/foods", ten: "Ăn gì ở Huế", mo: "Món sáng, món chiều, quán trong kho", mau: "cam",
    d: "M3 11h18M5 11a7 7 0 0 0 14 0M12 4v3M9 5l1 2M15 5l-1 2" },
  { href: "#/kham-pha/heritages", ten: "Đi đâu hôm nay", mo: "Kinh thành, lăng tẩm, chùa", mau: "ngoc", d: "M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6" },
  { href: "#/kham-pha/festivals", ten: "Lễ hội và ngày âm", mo: "Hỏi lễ nào, ngày nào", mau: "sen",
    d: "M8 2v4M16 2v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" },
  { href: "#/len-ke-hoach", ten: "Lên kế hoạch", mo: "Lịch theo buổi, có giờ gợi ý", mau: "lam", co: "lich_trinh_bieu_mau",
    d: "M9 20l-6-3V4l6 3 6-3 6 3v13l-6-3-6 3zM9 7v13M15 4v13" },
  { href: "#/tro-ly", ten: "Hỏi bằng ảnh", mo: "Gửi ảnh món ăn, công trình", mau: "tim", co: "anh",
    d: "M3 7h3l2-3h8l2 3h3v13H3zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" },
  { href: "#/kham-pha/travel", ten: "Đi lại", mo: "Sân bay, ga, bến xe, trong phố", mau: "la", d: "M5 17h14M7 17l1.5-6h7l1.5 6M9 11l1-4h4l1 4" },
];

// Điểm nên đến: ảnh tự host `public/anh/lich/` (bảng ảnh của C, Wikimedia Commons) + bài kho có thật — `bai` = đuôi tên file, tìm mã bài
// trong danh sách `/api/kham_pha` lúc chạy (không có ⇒ ẩn nút "Đọc bài").
const COMMONS = "https://commons.wikimedia.org/wiki/File:";
const DIEM = [
  { anh: "dai_noi", bai: "Đại Nội Huế.md", ten: "Đại Nội Huế", nhan: ["Di tích", "Kinh thành"],
    mo: "Quần thể cung điện, miếu thờ trong lòng Kinh thành.", tg: "Lưu Ly", gp: "Phạm vi công cộng", f: "Dien_Thai_Hoa.jpg" },
  { anh: "chua_thien_mu", bai: "Chùa Thiên Mụ.md", ten: "Chùa Thiên Mụ", nhan: ["Di tích", "Kim Long"],
    mo: "Tháp Phước Duyên bên bờ bắc sông Hương.", tg: "CEphoto, Uwe Aranas", gp: "CC BY-SA 3.0", f: "Hue_Vietnam_Thien-Mu-Temple-and-Pagoda-01.jpg" },
  { anh: "lang_tu_duc", bai: "Lăng Tự Đức.md", ten: "Lăng Tự Đức", nhan: ["Di tích", "Thủy Xuân"],
    mo: "Hồ nước, đồi thông và nhà tạ giữa thung lũng.", tg: "CEphoto, Uwe Aranas", gp: "CC BY-SA 3.0", f: "Hue_Vietnam_Tomb-of-Emperor-Tu-Duc-03.jpg" },
  { anh: "pha_tam_giang", bai: "Phá Tam Giang.md", ten: "Phá Tam Giang", nhan: ["Thiên nhiên", "Phía đông"],
    mo: "Mặt nước rộng, bãi bồi và hoàng hôn trên phá.", tg: "Christophe95", gp: "CC BY-SA 4.0", f: "Aerial_view_of_the_Tam_Giang_Lagoon.jpg" },
  { anh: "duyet_thi_duong", bai: "tại Duyệt Thị Đường.md", ten: "Duyệt Thị Đường",
    nhan: ["Nghệ thuật", "Kinh thành"], mo: "Nhà hát cung đình, nơi diễn nhã nhạc.", tg: "Francisco Anzola", gp: "CC BY 2.0",
    f: "Duy%E1%BB%87t_Th%E1%BB%8B_%C4%90%C6%B0%E1%BB%9Dng_(ho%C3%A0ng_th%C3%A0nh_Hu%E1%BA%BF).jpg" },
  { anh: "cho_dong_ba", bai: "Chợ Đông Ba.md", ten: "Chợ Đông Ba", nhan: ["Ẩm thực", "Kinh thành"],
    mo: "Chợ truyền thống, gian ẩm thực ở tầng trệt.", tg: "Chainwit", gp: "CC BY 4.0",
    f: "Dong_Ba_Market_(Hue)_-_Ch%E1%BB%A3_%C4%90%C3%B4ng_Ba_Hu%E1%BA%BF_(July_2024)_-_img_02.jpg" },
];
const ANH_LICH = `${import.meta.env.BASE_URL}anh/lich/`;

function Icon({ d }) {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true"><path d={d} /></svg>
  );
}

export function TrangChu({ bai, tinhNang, thoiTiet, onAsk, onAskAbout }) {
  const [cau, setCau] = useState("");
  const [dung, setDung] = useState(false);
  function submit(event) {
    event.preventDefault();
    if (cau.trim() && onAsk(cau)) setCau("");
  }
  const maBai = duoi => (bai || []).find(b => b.id.endsWith(duoi))?.id;
  return (
    <>
      <section className={`tc-hero ${dung ? "tc-dung" : ""}`} aria-labelledby="hero-h">
        <div className="tc-anh troi-cuon" aria-hidden="true">
          {ANH_HERO.map((a, i) => (
            <picture key={a.src}>
              <source media={MAN_NHO} srcSet={a.srcNho} />
              <img src={a.src} alt="" className="tc-anh-i" fetchpriority={i === 0 ? "high" : "low"}
                   loading={i === 0 ? "eager" : "lazy"} />
            </picture>
          ))}
        </div>
        {tinhNang.thoi_tiet && thoiTiet?.trang_thai === "ok" && <ThoiTiet tt={thoiTiet} />}
        <div className="tc-hero-in">
          <h1 id="hero-h" className="hero-h vao" style={{ "--n": 0 }}>Hỏi về Huế, như hỏi người bản xứ</h1>
          <p className="hero-p vao" style={{ "--n": 1 }}>Trả lời từ kho tư liệu về món ăn, di tích, lễ hội Huế — kèm tên tài liệu để bạn tự kiểm.</p>
          <form className="hoi vao" style={{ "--n": 2 }} onSubmit={submit}>
            <label className="sr-only" htmlFor="hoi-lon">Câu hỏi cho Trợ lý Huế</label>
            <input id="hoi-lon" className="hoi-o" value={cau} onChange={e => setCau(e.target.value)} placeholder="Ví dụ: chiều nay nên đi lăng nào?"
                   autoComplete="off" maxLength={500} />
            <button className="nut nut-chinh nhan-nut" type="submit">Hỏi</button>
          </form>
          <div className="goi-y" aria-label="Câu hỏi gợi ý">
            {GOI_Y.map((q, i) => (
              <button key={q} className="chip vao nhan-nut" style={{ "--n": 3 + i }} type="button" onClick={() => onAsk(q)}>{q}</button>
            ))}
          </div>
        </div>
        <button type="button" className="tc-dung-nut" aria-pressed={dung} onClick={() => setDung(!dung)}>
          {dung ? "Chạy ảnh" : "Dừng ảnh"}
        </button>
        <svg className="tc-song" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
          <path className="song-lop sau" fill="currentColor" opacity=".45" d="M0 40c180-30 360-30 540 4s360 30 540-2 270-26 360-10V90H0z" />
          <path className="song-lop" fill="currentColor" d="M0 52c160-34 320-34 480 0s320 34 480 0 320-34 480 0V90H0z" />
        </svg>
      </section>

      <div className="khung">
        <nav className="tc-nhanh vao" style={{ "--n": 6 }} aria-label="Lối vào nhanh">
          {NHANH.filter(n => !n.co || tinhNang[n.co]).map(n => (
            <a key={n.href + n.ten} className="nang" href={n.href}>
              <span className={`tc-bt tc-bt-${n.mau}`}><Icon d={n.d} /></span><b>{n.ten}</b><span>{n.mo}</span>
            </a>
          ))}
        </nav>

        <section className="khoi" aria-labelledby="kp-h">
          <h2 id="kp-h" className="khoi-h">Khám phá theo chủ đề</h2>
          <p className="khoi-p">Mỗi chủ đề là các bài trong kho mà trợ lý dùng để trả lời. Bấm để đọc cả bài.</p>
          <div className="tc-kham">
            {LINH_VUC.map((lv, i) => {
              const n = soBai(bai, lv.id);
              return (
                <a key={lv.id} className="tc-o nang hien lop-mau" style={{ "--n": i }} href={`#/kham-pha/${lv.id}`}>
                  <picture><source media={MAN_NHO} srcSet={ANH_LINH_VUC[lv.id].srcNho} />
                    <img src={ANH_LINH_VUC[lv.id].src} alt="" loading="lazy" /></picture>
                  <div className="nhan"><h3>{lv.ten}</h3><p>{lv.mo}</p>{n != null && <span className="tc-dem">{n} bài</span>}</div>
                </a>
              );
            })}
          </div>
        </section>
      </div>

      <div className="tc-dai-nen">
        <div className="khung">
          <section className="khoi" aria-labelledby="dn-h">
            <h2 id="dn-h" className="khoi-h">Điểm nên đến</h2>
            <p className="khoi-p">Một vài điểm trong kho — mỗi điểm có bài để đọc và có thể hỏi trợ lý thêm.</p>
            <div className="tc-dai-the">
              {DIEM.map((d, i) => (
                <article key={d.anh} className="tc-the nang hien" style={{ "--n": i }}>
                  <figure>
                    <img src={`${ANH_LICH}${d.anh}.jpg`} alt="" loading="lazy" decoding="async" />
                    <figcaption>Ảnh: {d.tg} · {GP[d.gp] ? <a href={GP[d.gp]} target="_blank" rel="noopener noreferrer">{d.gp}</a> : d.gp} ·{" "}
                      <a href={COMMONS + d.f} target="_blank" rel="noopener noreferrer">Commons</a> · đã thu nhỏ</figcaption>
                  </figure>
                  <div className="tc-the-than">
                    <div className="tc-nhan">{d.nhan.map(x => <span key={x}>{x}</span>)}</div>
                    <h3>{d.ten}</h3>
                    <p>{d.mo}</p>
                    <div className="tc-hanh">
                      {maBai(d.bai) && <a className="tc-doc" href={baiHref(maBai(d.bai))}>Đọc bài</a>}
                      <button type="button" className="tc-hoi-diem nhan-nut" onClick={() => onAskAbout(d.ten)}>Hỏi trợ lý</button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </div>
      </div>

      <div className="khung">
        {tinhNang.lich_trinh_bieu_mau && (
          <section className="tc-ke hien" aria-labelledby="lc-h">
            <div>
              <h2 id="lc-h" className="khoi-h">Lên kế hoạch đi Huế</h2>
              <p className="khoi-p">Chọn số ngày, người đi cùng và điều bạn thích — trợ lý xếp lịch theo buổi từ các điểm trong kho, điểm nào không xếp được sẽ
                ghi lý do.</p>
              <a className="tc-ke-nut nhan-nut" href="#/len-ke-hoach">Bắt đầu lên kế hoạch</a>
            </div>
          </section>
        )}

        <section className="khoi" aria-labelledby="tl-h">
          <h2 id="tl-h" className="khoi-h">Trợ lý trả lời thế nào</h2>
          <p className="khoi-p">Mỗi câu trả lời đi qua ba bước, để bạn biết thông tin đến từ đâu.</p>
          <ol className="tc-buoc hien">
            <li><b>Bạn hỏi</b><p>Gõ câu hỏi bằng tiếng Việt{tinhNang.anh ? ", hoặc gửi ảnh một món ăn, một công trình" : ""}.</p></li>
            <li><b>Tìm trong kho</b><p>Trợ lý tìm các đoạn liên quan trong kho tư liệu về Huế.</p></li>
            <li><b>Trả lời có nguồn</b><p>Câu trả lời ghi số nguồn [1] [2] — bấm để xem đoạn gốc.</p></li>
          </ol>
        </section>

        <p className="dai-bao">Trợ lý Huế trả lời từ kho tư liệu và ghi nguồn, nhưng vẫn có thể sai. <a href="#/gioi-thieu">Trợ lý làm được gì?</a></p>
      </div>
    </>
  );
}

function ThoiTiet({ tt }) {
  const { tmin, tmax, xs_mua } = tt.hom_nay;
  return (
    <aside className="tt-hop vao" style={{ "--n": 3 }} aria-label="Thời tiết Huế hôm nay">
      <p className="tt-h">Huế hôm nay</p>
      <p className="tt-so">{tmin}–{tmax} °C{xs_mua != null && <span className="tt-mo"> · khả năng mưa {xs_mua} %</span>}</p>
      <p className="tt-chu">{tt.ghi_cong} — số liệu lúc {tt.cap_nhat}.</p>
    </aside>
  );
}
