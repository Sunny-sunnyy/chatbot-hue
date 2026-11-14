import { useState } from "react";
import { ANH_DAU_TRANG, ANH_LINH_VUC } from "./anh.js";
import { Anh, GOI_Y, LINH_VUC, O5LinhVuc, Song, soBai } from "./chung.jsx";

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
