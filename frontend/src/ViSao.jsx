import { useState } from "react";
import { baiHref } from "./route.js";
import "./vi_sao.css";

// Nút "Vì sao trả lời vậy?" dưới một lượt + khung mở tại chỗ (24/11/2026; cảnh thử `data/x15_phan_ai_2026-11-23/canh_vi_sao/canh.png`).
// Dữ liệu: `GET /api/vi_sao/{turn_id}` — bản tóm tắt của lượt do server giữ trong RAM (công tắc `vi_sao`, chỉ máy demo). Nút chỉ vẽ khi sự kiện
// `done` của lượt mang `vi_sao: true` + `turn_id`; không có ⇒ thành phần này không vẽ gì (giao diện y như trước).
// Mọi nhãn tiếng Việt của từng bước (`nhan`, `tom_tat`, `ghi_chu`) do server viết — ở đây chỉ có chữ khung. Nhóm nào rỗng thì không vẽ nhóm đó.

const so = (x, le = 1) => Number(x).toLocaleString("vi-VN", { maximumFractionDigits: le });
const giay = x => `${so(x, x < 1 ? 2 : 1)} giây`;
const SO_BAI_DAU = 4;   // một lần tìm có thể ra tới 10 bài: vẽ 4 bài đầu, còn lại sau nút "xem thêm"
const SO_BUOC_DAU = 4;  // tin nhiều ý có thể tìm 6–7 lần: vẽ 4 bước đầu, còn lại gập

export function ViSao({ turn }) {
  const [mo, setMo] = useState(false);
  const [tai, setTai] = useState(null);  // null = chưa tải · {dang} · {d} = dữ liệu · {het} = server không còn giữ · {loi}
  if (!turn.viSao || !turn.turnId) return null;
  const khungId = `vi-sao-${turn.key}`;
  const bam = async () => {
    const moi = !mo;
    setMo(moi);
    if (!moi || (tai && !tai.loi)) return;  // đã tải (hoặc đã biết là hết) thì không gọi lại; lần trước lỗi mạng ⇒ bấm mở lại là thử lại
    setTai({ dang: true });
    try {
      const response = await fetch(`/api/vi_sao/${encodeURIComponent(turn.turnId)}`);
      if (response.status === 404) setTai({ het: true });
      else if (!response.ok) setTai({ loi: true });
      else setTai({ d: await response.json() });
    } catch {
      setTai({ loi: true });
    }
  };
  return (
    <div className="vi-sao">
      <button type="button" className="vi-sao-nut" aria-expanded={mo} aria-controls={khungId} onClick={bam}>
        <span aria-hidden="true">{mo ? "▾" : "▸"}</span> Vì sao trả lời vậy?
      </button>
      {mo && (
        <section className="vi-sao-khung" id={khungId} aria-label="Trợ lý đã làm gì để ra câu trả lời này">
          {tai?.dang && <p className="vi-sao-mo" role="status">Đang lấy chi tiết của lượt này…</p>}
          {tai?.het && <p className="vi-sao-mo">Chi tiết của lượt này không còn được giữ (máy chủ đã khởi động lại, hoặc lượt đã quá cũ).</p>}
          {tai?.loi && <p className="vi-sao-mo">Chưa lấy được chi tiết của lượt này. Bấm nút lần nữa để thử lại.</p>}
          {tai?.d && <NoiDung d={tai.d} turn={turn} />}
        </section>
      )}
    </div>
  );
}

function NoiDung({ d, turn }) {
  const goi = d.goi_model || [], buoc = d.buoc || [], nguon = d.nguon || [], ghiChu = d.ghi_chu || [];
  const modelDoc = d.sua_lich?.model_doc || [], ketQua = d.sua_lich?.ket_qua || [];
  const soTim = buoc.filter(b => b.loai === "tim").length;
  let thuTu = 0;  // số của từng nhóm đánh theo nhóm THẬT có mặt (lượt sửa lịch không có nhóm tìm kho…)
  const Dau = ({ children }) => <h4><i aria-hidden="true">{++thuTu}</i>{children}</h4>;
  return (
    <>
      <h3>Trợ lý đã làm gì để ra câu trả lời này</h3>
      {d.tom_tat && <p className="vi-sao-tom">{d.tom_tat}</p>}
      {/* `gui` chỉ có khi chuỗi thật đem đi KHÁC câu gõ: lượt nối tiếp, lượt trả lời ảnh (kèm tên đã đoán), nút gửi câu lệnh đủ tên */}
      {d.cau?.gui && (
        <p className="vi-sao-cau">Bạn gõ: <q>{d.cau.go}</q><br />Hệ thống đem đi xử lý: <q>{d.cau.gui}</q></p>
      )}
      {goi.length > 0 && (
        <>
          <Dau>{goi.length} lần gọi model, theo thứ tự</Dau>
          <ol className="vi-sao-goi">
            {goi.map((g, i) => <li key={i}><b>{g.nhan}</b>{g.giay != null && <small>{giay(g.giay)}</small>}</li>)}
          </ol>
        </>
      )}
      {(modelDoc.length > 0 || ketQua.length > 0) && (
        <>
          <Dau>Model đọc câu lệnh, code áp lên lịch</Dau>
          {/* hai danh sách rời: server không ghi phép nối từng hành động ↔ từng dòng kết quả */}
          {modelDoc.length > 0 && (
            <ul className="vi-sao-hd"><li className="vi-sao-hd-dau">Model đọc ra:</li>{modelDoc.map((h, i) => <li key={i}>{h.nhan}</li>)}</ul>
          )}
          {ketQua.length > 0 && (
            <ul className="vi-sao-hd"><li className="vi-sao-hd-dau">Code làm:</li>
              {ketQua.map((k, i) => <li key={i} data-duoc={k.duoc ? "co" : "khong"}><span>{k.duoc ? "đã làm" : "chưa làm"}</span>{k.cau}</li>)}</ul>
          )}
        </>
      )}
      {buoc.length > 0 && (
        <>
          <Dau>{soTim === buoc.length ? `Đã tìm gì trong kho tư liệu (${soTim} lần tìm)` : `Tìm trong kho và gọi công cụ, theo thứ tự (${buoc.length} bước)`}</Dau>
          <CacBuoc buoc={buoc} />
        </>
      )}
      {d.web && (
        <>
          <Dau>Tra web sau khi kho không đủ</Dau>
          <p className="vi-sao-web">Câu đem đi tra: <q>{d.web.cau}</q>{d.web.so_nguon != null && <> · {d.web.so_nguon} nguồn web</>}</p>
        </>
      )}
      {nguon.length > 0 && (
        <>
          <Dau>Câu trả lời dựa vào {nguon.length} nguồn</Dau>
          <ul className="vi-sao-nguon">
            {nguon.map(n => (
              <li key={n.ma}>
                {/* `ma` là mã gốc của đoạn; câu trả lời trên màn hình đánh số lại ⇒ in đúng số người xem đang thấy */}
                <span className="vi-sao-ma">[{turn.numbers?.get(String(n.ma)) ?? n.ma}]</span>
                <span>{n.bai_id ? <a href={baiHref(n.bai_id)}>{n.title}</a> : <b>{n.title}</b>}{n.muc && <small>{n.muc}</small>}</span>
              </li>
            ))}
          </ul>
        </>
      )}
      {d.thoi_gian?.tong > 0 && (
        <>
          <Dau>Mất bao lâu — tổng {giay(d.thoi_gian.tong)}</Dau>
          <ThoiGian t={d.thoi_gian} />
        </>
      )}
      {ghiChu.length > 0 && <ul className="vi-sao-ghi">{ghiChu.map((c, i) => <li key={i}>{c}</li>)}</ul>}
    </>
  );
}

// `buoc[]`: lần tìm trong kho và công cụ khác, ĐÚNG thứ tự server ghi nhận; `ai` = code làm trước khi model viết, hay model tự gọi giữa chừng.
function CacBuoc({ buoc }) {
  const [het, setHet] = useState(false);
  const hien = het ? buoc : buoc.slice(0, SO_BUOC_DAU);
  return (
    <>
      <div className="vi-sao-tim">{hien.map((b, i) => <Buoc key={i} b={b} stt={i + 1} />)}</div>
      {buoc.length > SO_BUOC_DAU && !het && (
        <button type="button" className="vi-sao-them" onClick={() => setHet(true)}>Xem thêm {buoc.length - SO_BUOC_DAU} bước</button>
      )}
    </>
  );
}

function Buoc({ b, stt }) {
  const [het, setHet] = useState(false);
  const bai = b.bai || [];
  const hien = het ? bai : bai.slice(0, SO_BAI_DAU);
  return (
    <div className="vi-sao-lan" data-ai={b.ai}>
      <p className="vi-sao-lan-dau"><b>{stt}. {b.nhan}</b>{b.giay != null && <small> · {giay(b.giay)}</small>}</p>
      {(b.cau || []).map((cau, i) => <p key={i} className="vi-sao-lan-cau"><q>{cau}</q></p>)}
      {bai.length > 0 && (
        <ul className="vi-sao-bai">
          {hien.map((x, i) => (
            <li key={i}>
              <span className="vi-sao-bai-ten">{x.bai_id ? <a href={baiHref(x.bai_id)}>{x.title}</a> : x.title}
                {x.duoc_trich && <em>được trích</em>}</span>
              <small>{x.so_doan} đoạn{x.hang != null && <> · đoạn tốt nhất đứng thứ {x.hang}</>}</small>
            </li>
          ))}
        </ul>
      )}
      {bai.length > SO_BAI_DAU && !het && (
        <button type="button" className="vi-sao-them" onClick={() => setHet(true)}>Xem thêm {bai.length - SO_BAI_DAU} bài</button>
      )}
      {b.so_doan_tim != null && (
        <p className="vi-sao-lan-cuoi">{b.so_doan_tim} đoạn tìm ra{b.so_doan_moi != null && <> · {b.so_doan_moi} đoạn mới được đưa cho model đọc</>}</p>
      )}
    </div>
  );
}

// Thanh ba đoạn: tìm trong kho · dựng phần cho model đọc · model đọc và viết. Phần quá nhỏ vẫn có vạch 2 px để người xem thấy nó tồn tại.
function ThoiGian({ t }) {
  const phan = [["tim", "Tìm trong kho", t.tim], ["dung", "Dựng phần cho model đọc", t.dung_ngu_canh], ["model", "Model đọc và viết", t.model]]
    .filter(([, , x]) => x != null);
  return (
    <>
      <div className="vi-sao-thanh" aria-hidden="true">
        {phan.map(([ma, , x]) => <i key={ma} data-phan={ma} style={{ flexGrow: Math.max(x, 0), flexBasis: 2 }} />)}
      </div>
      <ul className="vi-sao-chu-giai">
        {phan.map(([ma, nhan, x]) => <li key={ma} data-phan={ma}>{nhan}: <b>{giay(x)}</b></li>)}
      </ul>
    </>
  );
}
