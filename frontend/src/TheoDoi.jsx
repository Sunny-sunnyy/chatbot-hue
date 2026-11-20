import { useState } from "react";
import "./co.css";

// Trang theo dõi cho CHỦ dự án (plan `report_agent/2026-11-20/e_trang_theo_doi_plan.md`): KHÔNG có trong menu, vào bằng địa chỉ `#/theo-doi`. Số do server
// gom theo ngày từ log số đo (`/api/theo_doi`) — không có chữ câu hỏi nào. Khoá quản trị gửi ở header, chỉ giữ trong bộ nhớ trang (tải lại trang là
// phải nhập lại; không lưu xuống máy, không nằm trong địa chỉ). File tải riêng (`lazy` ở `App.jsx`).
const COT = [["tra_loi", "Trả lời từ kho"], ["tu_choi", "Từ chối"], ["ngoai_pham_vi", "Ngoài phạm vi"], ["web", "Có mục web"], ["lich", "Lịch / sửa lịch"],
             ["cache", "Trúng bản lưu"], ["loi", "Lỗi"]];
const giay = ms => (ms == null ? "–" : (ms / 1000).toFixed(1));
const ngayVn = iso => iso.split("-").reverse().slice(0, 2).join("/");

export default function TheoDoi() {
  const [khoa, setKhoa] = useState("");
  const [du, setDu] = useState(null);
  const [bao, setBao] = useState("");
  const [dangTai, setDangTai] = useState(false);

  async function xem(e) {
    e.preventDefault();
    setDangTai(true);
    setBao("");
    try {
      const r = await fetch("/api/theo_doi", { headers: { "X-Khoa-Theo-Doi": khoa } });
      if (r.ok) setDu(await r.json());
      else { setDu(null); setBao(r.status === 403 ? "Sai khoá." : "Trang theo dõi chưa bật trên máy chủ này."); }
    } catch {
      setBao("Chưa tải được số liệu. Thử lại.");
    } finally {
      setDangTai(false);
    }
  }

  const max = du ? Math.max(1, ...du.ngay.map(n => n.luot)) : 1;
  const tong = k => du.ngay.reduce((s, n) => s + n[k], 0);
  return (
    <div className="khung co-than td-trang">
      <h1 className="co-h">Theo dõi</h1>
      <p className="co-p">Trang riêng của chủ dự án: số lượt hỏi, kết cục, tiền và độ trễ theo ngày. Không có nội dung câu hỏi của ai ở đây.</p>
      <form className="td-khoa" onSubmit={xem}>
        <label htmlFor="td-khoa-o">Khoá quản trị</label>
        <input id="td-khoa-o" type="password" autoComplete="off" value={khoa} onChange={e => setKhoa(e.target.value)} />
        <button type="submit" className="nut nut-chinh" disabled={!khoa || dangTai}>{du ? "Tải lại" : "Xem"}</button>
        {bao && <span role="alert" className="td-bao">{bao}</span>}
      </form>
      {du && du.ngay.length === 0 && <p className="co-p">Log chưa có lượt nào.</p>}
      {du && du.ngay.length > 0 && (
        <>
          <div className="td-cuon">
            <table className="td-bang">
              <thead>
                <tr><th>Ngày</th><th>Số lượt</th>{COT.map(([k, ten]) => <th key={k}>{ten}</th>)}<th>USD</th><th>p50 (s)</th><th>p95 (s)</th><th>Bản code</th></tr>
              </thead>
              <tbody>
                {du.ngay.map(n => (
                  <tr key={n.ngay}>
                    <td>{ngayVn(n.ngay)}</td>
                    <td className="td-luot"><span className="td-thanh" style={{ width: `${Math.round((n.luot / max) * 100)}%` }} aria-hidden="true" /><b>{n.luot}</b></td>
                    {COT.map(([k]) => <td key={k} className={k === "loi" && n.loi > 0 ? "td-loi" : undefined}>{n[k]}</td>)}
                    <td>{n.usd.toFixed(4)}</td><td>{giay(n.p50_ms)}</td><td>{giay(n.p95_ms)}</td><td className="td-sha">{n.git_sha || "–"}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr><td>Tổng</td><td><b>{tong("luot")}</b></td>{COT.map(([k]) => <td key={k}>{tong(k)}</td>)}<td>{tong("usd").toFixed(4)}</td><td /><td /><td /></tr>
              </tfoot>
            </table>
          </div>
          <p className="co-p td-chu">
            {du.ngay.length} ngày gần nhất có lượt hỏi (tối đa {du.so_ngay}), đọc từ log lúc {du.doc_luc}. Mỗi lượt nằm ở đúng một cột; độ trễ không tính lượt lỗi;
            "Bản code" là bản của lượt gần nhất trong ngày. Đã bỏ {du.bo_model_gia} dòng của bộ thử tự động{du.bo_dong_hong > 0 ? ` và ${du.bo_dong_hong} dòng hỏng` : ""}.
            Ở máy phát triển, số còn lẫn lượt thử của nhóm (nhất là cột Lỗi).
          </p>
        </>
      )}
    </div>
  );
}
