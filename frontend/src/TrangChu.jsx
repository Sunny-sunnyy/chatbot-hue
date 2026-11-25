import { useMemo, useState } from "react";
import { ANH_LINH_VUC, MAN_NHO } from "./anh.js";
import { GOI_Y, LINH_VUC, LOAI_CON, soBai } from "./chung.jsx";
import { baiHomNay } from "./homNay.js";
import { baiHref } from "./route.js";
import "./tc.css";
import { HeroSong } from "./song/Song.jsx";

// Trang chủ. Màn đầu từ 22/11/2026 là `song/Song.jsx` (con sông làm bố cục, sáu lối vào là sáu bến); phần dưới giữ bản H1 "Sông Hương" 14/11. Không thêm số liệu / lời hứa mới:
// mọi chữ là chữ trang cũ hoặc tên điểm + mô tả ngắn đã có trong bài kho; ảnh chỉ là ảnh đã có ghi công.

// Lối vào nhanh: chỉ dẫn tới chỗ đã có trên trang (không câu hỏi soạn sẵn mới). `co` = cờ phải bật mới hiện.
const NHANH = [
  { href: "#/kham-pha/foods", ten: "Ăn gì ở Huế", mo: "Món sáng, món chiều, quán trong kho", mau: "cam",
    d: "M3 11h18M5 11a7 7 0 0 0 14 0M12 4v3M9 5l1 2M15 5l-1 2" },
  { href: "#/kham-pha/heritages", ten: "Đi đâu hôm nay", mo: "Kinh thành, lăng tẩm, chùa", mau: "ngoc", d: "M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6" },
  { href: "#/kham-pha/festivals", ten: "Lễ hội", mo: "Hỏi lễ nào, ngày nào", mau: "sen",
    d: "M8 2v4M16 2v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" },
  { href: "#/len-ke-hoach", ten: "Lên kế hoạch", mo: "Lịch theo buổi, có giờ gợi ý", mau: "lam", co: "lich_trinh_bieu_mau",
    d: "M9 20l-6-3V4l6 3 6-3 6 3v13l-6-3-6 3zM9 7v13M15 4v13" },
  { href: "#/tro-ly", ten: "Hỏi bằng ảnh", mo: "Gửi ảnh món ăn, công trình", mau: "tim", co: "anh",
    d: "M3 7h3l2-3h8l2 3h3v13H3zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" },
  { href: "#/kham-pha/travel", ten: "Đi lại", mo: "Sân bay, ga, bến xe, trong phố", mau: "la", d: "M5 17h14M7 17l1.5-6h7l1.5 6M9 11l1-4h4l1 4" },
];

// Điểm nên đến: ảnh tự host `public/anh/lich/` (bảng ảnh của C; nguồn chỉ ghi trong bảng dữ liệu, không hiện — User 14/11) + bài kho có thật —
// `bai` = đuôi tên file, tìm mã bài trong danh sách `/api/kham_pha` lúc chạy (không có ⇒ ẩn nút "Đọc bài").
const DIEM = [
  { anh: "dai_noi", bai: "Đại Nội Huế.md", ten: "Đại Nội Huế", nhan: ["Di tích", "Kinh thành"],
    mo: "Quần thể cung điện, miếu thờ trong lòng Kinh thành." },
  { anh: "chua_thien_mu", bai: "Chùa Thiên Mụ.md", ten: "Chùa Thiên Mụ", nhan: ["Di tích", "Kim Long"],
    mo: "Tháp Phước Duyên bên bờ bắc sông Hương." },
  { anh: "lang_tu_duc", bai: "Lăng Tự Đức.md", ten: "Lăng Tự Đức", nhan: ["Di tích", "Thủy Xuân"],
    mo: "Hồ nước, đồi thông và nhà tạ giữa thung lũng." },
  { anh: "pha_tam_giang", bai: "Phá Tam Giang.md", ten: "Phá Tam Giang", nhan: ["Thiên nhiên", "Phía đông"],
    mo: "Mặt nước rộng, bãi bồi và hoàng hôn trên phá." },
  { anh: "duyet_thi_duong", bai: "tại Duyệt Thị Đường.md", ten: "Duyệt Thị Đường",
    nhan: ["Nghệ thuật", "Kinh thành"], mo: "Nhà hát cung đình, nơi diễn nhã nhạc." },
  { anh: "cho_dong_ba", bai: "Chợ Đông Ba.md", ten: "Chợ Đông Ba", nhan: ["Ẩm thực", "Kinh thành"],
    mo: "Chợ truyền thống, gian ẩm thực ở tầng trệt." },
];
const ANH_LICH = `${import.meta.env.BASE_URL}anh/lich/`;
const ANH_GOC = `${import.meta.env.BASE_URL}anh/`;  // ảnh theo mã bài (`anhBai.js`), như trang Khám phá

function Icon({ d }) {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true"><path d={d} /></svg>
  );
}

export function TrangChu({ bai, tinhNang, thoiTiet, onAsk, onAskAbout, dai = null }) {
  const [cau, setCau] = useState("");
  function submit(event) {
    event.preventDefault();
    if (cau.trim() && onAsk(cau)) setCau("");
  }
  const maBai = duoi => (bai || []).find(b => b.id.endsWith(duoi))?.id;
  // Ô "Hôm nay ở Huế": code chọn một bài có ảnh chắc theo ngày (`homNay.js`); chữ chỉ là tên bài + tên nhóm + dòng tóm tắt của chính bài (như thẻ bài ở Khám phá) — không câu mô tả mới, không ngày tháng.
  const homNay = useMemo(() => baiHomNay(bai), [bai]);
  return (
    <>
      <HeroSong nhanh={NHANH.filter(n => !n.co || tinhNang[n.co])} cau={cau} setCau={setCau} submit={submit} onAsk={onAsk}
                thoiTiet={tinhNang.thoi_tiet && thoiTiet?.trang_thai === "ok" ? <ThoiTiet tt={thoiTiet} /> : null} />

      <div className="khung">
        {homNay && (
          <section className="tc-hn" aria-labelledby="hn-h">
            <a className="tc-hn-the nang hien" href={baiHref(homNay.bai.id)}>
              <figure className="tc-hn-anh"><img src={`${ANH_GOC}${homNay.anh}.jpg`} alt={homNay.bai.tieu_de} decoding="async" /></figure>
              <div className="tc-hn-than">
                <h2 id="hn-h" className="tc-hn-nhan">Hôm nay ở Huế</h2>
                <p className="tc-hn-ten">{homNay.bai.tieu_de}</p>
                {homNay.bai.tom_tat && <p className="tc-hn-tt">{homNay.bai.tom_tat}</p>}
                <span className="tc-hn-loai">{LOAI_CON[homNay.bai.loai_con] ?? LINH_VUC.find(lv => lv.id === homNay.bai.linh_vuc)?.ten ?? "Tổng quan"}</span>
                <span className="tc-hn-doc">Đọc bài</span>
              </div>
            </a>
          </section>
        )}
        <section className="khoi" aria-labelledby="kp-h">
          <h2 id="kp-h" className="khoi-h chu-hien">Khám phá theo lĩnh vực</h2>
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
          {/* BẢN THỬ (nhánh `thu-c-trang-chu-chu-de`): dải "Hồ sơ theo chủ đề" dẫn sang lưới 20 chủ đề — đặt DƯỚI năm ô lĩnh vực nên màn đầu, các bến và ô
              "Hôm nay ở Huế" đứng nguyên chỗ. App chỉ đưa `dai` khi server gửi khoá `chu_de_trang_chu` (chưa có ở server ⇒ mặc định không vẽ). */}
          {dai}
        </section>
      </div>

      <div className="tc-dai-nen">
        <div className="khung">
          <section className="khoi" aria-labelledby="dn-h">
            <h2 id="dn-h" className="khoi-h chu-hien">Điểm nên đến</h2>
            <p className="khoi-p">Một vài điểm trong kho — mỗi điểm có bài để đọc và có thể hỏi trợ lý thêm.</p>
            <div className="tc-dai-the">
              {DIEM.map((d, i) => (
                <article key={d.anh} className="tc-the nang hien" style={{ "--n": i }}>
                  <figure>
                    <img src={`${ANH_LICH}${d.anh}.jpg`} alt="" loading="lazy" decoding="async" />
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
          <h2 id="tl-h" className="khoi-h chu-hien">Trợ lý trả lời thế nào</h2>
          <p className="khoi-p">Mỗi câu trả lời đi qua ba bước, để bạn biết thông tin đến từ đâu.</p>
          <ol className="tc-buoc hien">
            <li><b>Bạn hỏi</b><p>Gõ câu hỏi bằng tiếng Việt{tinhNang.anh ? ", hoặc gửi ảnh một món ăn, một công trình" : ""}.</p></li>
            <li><b>Tìm trong kho</b><p>Trợ lý tìm các đoạn liên quan trong kho tư liệu về Huế.</p></li>
            <li><b>Trả lời có nguồn</b><p>Dưới câu trả lời có dòng Nguồn — bấm tên bài để xem đoạn gốc.</p></li>
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
      <p className="tt-so">{tmin}–{tmax} °C{xs_mua != null && <span className="tt-mo"> · khả năng mưa cao nhất {xs_mua} %</span>}</p>
      <p className="tt-chu">Số liệu lúc {tt.cap_nhat}.</p>{/* không hiện dòng ghi công Open-Meteo (User 14/11); nguồn ghi ở `llm/thoi_tiet.py` */}
    </aside>
  );
}
