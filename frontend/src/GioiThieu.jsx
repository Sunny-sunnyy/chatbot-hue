import { useEffect, useState } from "react";
import { ANH_DAU_TRANG, GP, MOI_ANH } from "./anh.js";
import { khoaBai, taiGhiCong } from "./anhBai.js";
import { Anh } from "./chung.jsx";
import "./gt.css";

// Giới thiệu theo H1 "Sông Hương" (đợt 1 giao diện, C, 14/11/2026; mẫu `data/ui_mau_2026-11-14/h1/gioi_thieu.html`, bàn nhóm C / E vòng 1).
// Nội dung giữ đúng trang cũ, không thêm lời hứa / số mới; câu "chưa có…" và dòng về ảnh / bản đồ theo cờ server (`/api/tinh_nang` ⇒ banDo, anh).
// Hiệu ứng riêng (A chốt từ nghiên cứu "wow"): đường sông Hương vẽ dần khi cuộn qua dải "ba bước" (SVG stroke) — chỉ dưới html.hieu-ung;
// máy giảm chuyển động ⇒ đường hiện sẵn đầy đủ.

const IC = {
  hoi: "M4 5h16v11H9l-5 4zM8 9h8M8 12h5",
  lich: "M4 5h16v15H4zM4 10h16M9 3v4M15 3v4M8 14h3M8 17h6",
  web: "M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16zM4 12h16M12 4c3 3 3 13 0 16M12 4c-3 3-3 13 0 16",
  anh: "M4 8h3l2-3h6l2 3h3v11H4zM12 16.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z",
};

function Ic({ d }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={d} />
    </svg>
  );
}

export function GioiThieu({ tinhNang, daCo: daCoCo, bai, muc }) {
  const banDo = !!tinhNang?.ban_do_lich, anh = !!tinhNang?.anh;
  // tên bài cho dòng ghi công ảnh: lấy từ /api/kham_pha (anhBai.js không chứa tên bài — repo public); daCo chờ cả danh sách bài
  const [ghiCong, setGhiCong] = useState(null);  // ghi công ảnh Khám phá: JSON tĩnh tải khi mở trang (không nằm trong JS mọi trang)
  useEffect(() => { let huy = false; taiGhiCong().then(gc => !huy && setGhiCong(gc)); return () => { huy = true; }; }, []);
  const daCo = daCoCo && ghiCong !== null;
  const tenBai = Object.fromEntries((bai ?? []).map(b => [khoaBai(b.id), b.tieu_de]));
  // `#/gioi-thieu/<mục>` ⇒ cuộn tới mục (sau lần `scrollTo(0, 0)` của `useRoute` lúc đổi hash). Mục "Nguồn ảnh" thu gọn ⇒ mở sẵn ngay lần vẽ đầu
  // (thuộc tính open ở dưới): mở bằng code sau khi vẽ thì danh sách ~167 dòng bung ra cùng khung hình với lần cuộn ⇒ chân trang bị tính là xô lệch (CLS 0,24)
  // chưa biết cờ / chưa có danh sách bài / ghi công ⇒ chưa vẽ thân trang (thẻ "làm được gì" theo cờ nở ra lúc cờ về ⇒ đẩy cả trang: CLS 0,17–0,66 đo ở 390, 14/11) và chưa cuộn
  useEffect(() => {
    if (!muc || !daCo) return;
    const el = document.getElementById(muc);
    // cuộn sau khi font đã tải: cuộn sớm thì chữ phía trên đổi cỡ lúc font về ⇒ vùng đang xem bị đẩy (CLS 0,6 đo được trên bản build)
    let huy = false;
    document.fonts.ready.then(() => requestAnimationFrame(() => { if (!huy) el?.scrollIntoView(); }));
    return () => { huy = true; };
  }, [muc, daCo]);
  const lam = [
    [IC.hoi, "Hỏi về Huế", "Món ăn, di tích, lễ hội, nghệ thuật biểu diễn, đi lại và vé tham quan — trả lời bằng tiếng Việt, kèm nguồn."],
    // mỗi dòng theo cờ server như bản cũ (review E M-2): tính năng tắt thì không hứa
    ...(tinhNang?.lich_trinh_bieu_mau ? [[IC.lich, "Lên kế hoạch", "Chọn số ngày, người đi cùng, sở thích; trợ lý xếp lịch theo buổi từ các điểm có trong kho."]] : []),
    ...(tinhNang?.tra_web ? [[IC.web, "Tra thêm trên web", "Khi kho không có, trợ lý tra web một lần và để riêng phần đó dưới nhãn “Từ web (chưa kiểm)”."]] : []),
    ...(anh ? [[IC.anh, "Hỏi bằng ảnh", "Gửi ảnh, trợ lý gợi ý tên nơi hoặc món (có thể sai); bạn bấm chọn đúng tên rồi mới hỏi."]] : []),
  ];
  const buoc = [
    ["Bạn hỏi", "Gõ câu hỏi như nói chuyện, hoặc bấm một câu gợi ý."],
    ["Trợ lý tìm trong kho", "Tìm các đoạn liên quan trong kho tư liệu về Huế đã biên soạn; chưa đủ thì tìm thêm."],
    ["Trả lời kèm nguồn", "Mỗi ý có số [n]; bấm tên ở dòng “Nguồn” để xem đoạn gốc hoặc đọc cả bài ở Khám phá."],
  ];
  return (
    <>
      <section className="gt-dau" aria-labelledby="gt-h">
        <div className="gt-nen troi-cuon"><Anh a={ANH_DAU_TRANG.song} className="anh-troi" /></div>
        <div className="khung gt-dau-in">
          <p className="vet vao" style={{ "--n": 0 }}><a href="#/">Trang chủ</a> / Giới thiệu</p>
          <h1 id="gt-h" className="gt-h vao" style={{ "--n": 1 }}>Về Trợ lý Huế</h1>
          <p className="gt-dan vao" style={{ "--n": 2 }}>
            Người bạn đồng hành tra sổ tay về Huế: hỏi gì cũng trả lời từ kho tư liệu đã biên soạn, và chỉ cho bạn chỗ lấy thông tin.
          </p>
        </div>
      </section>

      {!daCo ? <div className="gt-cho" /> : <div className="khung gt-than">
        <section className="gt-khoi" aria-labelledby="gt-lam">
          <h2 id="gt-lam" className="khoi-h">Trợ lý làm được gì</h2>
          <ul className="gt-lam">
            {lam.map(([d, t, m], i) => (
              <li key={t} className="gt-the nang hien" style={{ "--n": i }}>
                <span className="gt-ic"><Ic d={d} /></span><h3>{t}</h3><p>{m}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="gt-khoi gt-buoc-khoi" aria-labelledby="gt-buoc">
          <h2 id="gt-buoc" className="khoi-h">Một câu hỏi đi qua ba bước</h2>
          {/* đường sông Hương nối ba bước: vẽ dần theo cuộn (gt.css); trang trí, trình đọc màn hình bỏ qua */}
          <svg className="gt-song" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true">
            <path pathLength="1" d="M0 34 C 120 6, 240 6, 360 30 S 600 58, 720 30 S 960 2, 1080 26 S 1170 44, 1200 34" />
          </svg>
          <ol className="gt-buoc">
            {buoc.map(([t, m], i) => (
              <li key={t} className="hien" style={{ "--n": i }}><span className="gt-so">{i + 1}</span><h3>{t}</h3><p>{m}</p></li>
            ))}
          </ol>
        </section>

        <section className="gt-khoi gt-doi">
          <div className="gt-gioi-han hien">
            <h2 className="gt-h2">Giới hạn</h2>
            <ul>
              <li>Trợ lý có thể sai. Giờ mở cửa, giá vé, lịch lễ hội có thể đã đổi — kiểm lại trước khi đi.</li>
              <li>{banDo ? "Chưa có nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau). Bản đồ lịch trình chỉ ghim các điểm đã có toạ độ."
                : "Chưa có bản đồ, nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau)."}</li>
              <li>Câu hỏi ngoài chủ đề Huế được báo là ngoài phạm vi.</li>
            </ul>
          </div>
          <div className="gt-du-lieu hien" style={{ "--n": 1 }}>
            <h2 className="gt-h2">Dữ liệu của bạn</h2>
            <p>Trợ lý nhớ các câu hỏi trong một cuộc trò chuyện để hiểu câu hỏi tiếp theo: nhớ trong bộ nhớ máy chủ, tối đa 30 phút, qua một cookie chỉ dùng
              cho trò chuyện. Máy chủ không lưu chữ câu hỏi hay câu trả lời vào nhật ký. Nút “Cuộc trò chuyện mới” xoá phần đã nhớ.</p>
            <p>Để trả lời, câu hỏi được gửi tới dịch vụ mô hình AI (OpenAI); khi tra web, câu hỏi cũng được gửi tới dịch vụ tìm kiếm. Đừng gõ thông tin cá nhân
              vào câu hỏi.</p>
            {banDo && <p>Khi lịch có bản đồ, trình duyệt của bạn tải ảnh bản đồ từ máy chủ OpenStreetMap — máy chủ đó nhận địa chỉ IP và vùng bản đồ bạn
              đang xem (không nhận câu hỏi của bạn).</p>}
            {anh && <p>Ảnh bạn gửi được thu nhỏ, bỏ thông tin vị trí, gửi tới OpenAI để đoán tên, không lưu.</p>}
          </div>
        </section>

        <details className="gt-nguon" id="nguon-anh" open={muc === "nguon-anh" || undefined}>
          <summary>Nguồn ảnh trên trang</summary>
          <ul>{MOI_ANH.map(a => <li key={a.src}><GhiCong a={a} /></li>)}</ul>
          {/* ảnh thẻ Khám phá: thẻ không có chỗ ghi công ⇒ ghi đủ ở đây (trang bài cũng ghi dưới ảnh) */}
          <h3 className="gt-nguon-h">Ảnh các bài ở Khám phá</h3>
          <ul>{Object.entries(ghiCong ?? {}).map(([khoa, a]) => ({ khoa, ...a })).map(a => (
            <li key={a.khoa}>{tenBai[a.khoa] ? `${tenBai[a.khoa]}. ` : ""}{a.nguon
              ? <>{a.minhHoa && "Ảnh minh hoạ · "}Nguồn ảnh: <a href={a.trang} target="_blank" rel="noopener noreferrer">{a.nguon}</a></>
              : <>Ảnh: {a.tacGia} ·{" "}
                {GP[a.giayPhep] ? <a href={GP[a.giayPhep]} target="_blank" rel="noopener noreferrer">{a.giayPhep}</a> : a.giayPhep} ·{" "}
                <a href={a.trang} target="_blank" rel="noopener noreferrer">trang ảnh trên Wikimedia Commons</a> · đã {a.doi}</>}</li>
          ))}</ul>
        </details>
      </div>}
    </>
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
