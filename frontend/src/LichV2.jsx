import { Suspense, lazy, useState } from "react";
import { boMaTrichDan } from "./markdown.js";
import { toaDoHopLe } from "./toaDo.js";
import { GP } from "./anh.js";
import { SourceLine } from "./SourceLine.jsx";

const BanDoLich = lazy(() => import("./BanDoLich.jsx"));

// Thẻ lịch "Lên kế hoạch" bản 2 + lưu lịch (tách từ chat.jsx, đợt 0 giao diện H1; hành vi giữ nguyên).
export const MAP_PREFIX = "https://www.google.com/maps/search/";  // D11: chỉ nhận link bản đồ đúng gốc này (kiểm cả phía trình duyệt)

// "Lên kế hoạch" bản 2 (spec 5c.5): thẻ lịch vẽ TỪ KHUNG do code dựng (tên, buổi, giờ, ghi chú); câu model đổ vào theo `id_muc`, chưa tới ⇒
// "đang viết…". Loại mục chưa biết (đợt sau: ăn uống…) ⇒ bỏ qua, không lỗi. Nút "Sửa" điền lại biểu mẫu bằng đúng giá trị đã gửi.
const NHAN_BUOI_V2 = { sang: "Sáng", trua: "Trưa", chieu: "Chiều", toi: "Tối" };
const LOAI_MUC_V2 = new Set(["tham_quan", "hoat_dong_toi", "nghi"]);
const NHAN_MUC_V2 = { co_the_di_lai: "có thể đi lại", kiem_lich_dien: "kiểm lịch diễn trước khi đi" };  // cùng chữ với server (`NHAN_MUC`)
const THU_V2 = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật"];  // `thu` của server: thứ Hai = 0

// Đợt 2 (B): ảnh tự host của điểm (cờ `anh_lich`) — chỉ vẽ khi `src` dưới /anh/lich/ và trang ảnh là Wikimedia Commons (kiểm cả phía trình
// duyệt như link bản đồ); điểm không có ảnh ⇒ không vẽ gì (không ảnh thay). Dòng ghi công: tác giả · giấy phép · trang ảnh (điều kiện CC BY).
// `src` của server tính từ gốc `public/` ⇒ ghép `BASE_URL` (/static/) như ảnh cổng (`anh.js`). Ghi công như ảnh cổng: link giấy phép + "đã thu
// nhỏ" (CC BY / BY-SA đòi ghi thay đổi; `doi` của bảng khi có chỉnh khác, vd cắt).
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
      <figcaption>
        {anh.chu_thich && <>{anh.chu_thich}. </>}Ảnh: {anh.tac_gia} ·{" "}
        {GP[anh.giay_phep] ? <a href={GP[anh.giay_phep]} target="_blank" rel="noopener noreferrer">{anh.giay_phep}</a> : anh.giay_phep} ·{" "}
        <a href={anh.trang} target="_blank" rel="noopener noreferrer">trang ảnh trên Wikimedia Commons</a> · đã {anh.doi || "thu nhỏ"}
      </figcaption>
    </figure>
  );
}

export function LichV2({ turn, onEditPlan }) {
  const lich = turn.lichV2;
  const cau = turn.cauV2 || {};
  const xong = turn.phase === "done";
  // đợt 2: bản đồ chỉ khi server gắn toạ độ (cờ `ban_do_lich`); thứ tự ghim = thứ tự mục trong ngày, mục "nghỉ" không ghim; thiếu toạ độ ⇒ danh sách
  // ghi "chưa có trên bản đồ" (BanDoLich), không ghim đoán
  const banDo = lich.ngay.some(ng => ng.muc.some(m => toaDoHopLe(m.toa_do)))
    ? lich.ngay.flatMap(ng => ng.muc.filter(m => m.loai === "tham_quan" || m.loai === "hoat_dong_toi")
        .filter(m => typeof m.map_url === "string" && m.map_url.startsWith(MAP_PREFIX))
        .map((m, i) => ({ ten: m.ten, map_url: m.map_url, ngay: ng.ngay, buoi: m.buoi, thu_tu: i + 1, toa_do: m.toa_do })))
    : [];
  return (
    <div className="bubble lich-v2">
      <p className="lich-hieu">{lich.minh_hieu.replaceAll("**", "")}</p>
      {lich.ngay.map(ng => (
        <section key={ng.ngay} className="lich-ngay" aria-label={`Ngày ${ng.ngay}`}>
          <h3>Ngày {ng.ngay}{ng.ngay_thang ? ` · ${THU_V2[ng.thu]} ${ng.ngay_thang.split("-").reverse().join("/")}` : ""}</h3>
          <ul>
            {ng.muc.filter(m => LOAI_MUC_V2.has(m.loai)).map(m => (
              <li key={m.id_muc}>
                <span className="lich-buoi">{NHAN_BUOI_V2[m.buoi] || m.buoi}{m.gio ? ` · ${m.gio}` : ""}</span>
                <span className="lich-ten">{m.ten}{(m.nhan || []).filter(x => NHAN_MUC_V2[x]).map(x => <small key={x}> · {NHAN_MUC_V2[x]}</small>)}</span>
                {m.loai !== "nghi" && (
                  <span className="lich-cau">{cau[m.id_muc] != null ? boMaTrichDan(cau[m.id_muc]) : (xong ? "" : "đang viết…")}</span>
                )}
                {anhHopLe(m.anh) && <AnhLich anh={m.anh} ten={m.ten} />}
              </li>
            ))}
          </ul>
        </section>
      ))}
      {lich.ghi_chu.length > 0 && (
        <div className="lich-ghi-chu">
          <p className="font-semibold">Ghi chú của lịch</p>
          <ul>{lich.ghi_chu.map((g, i) => <li key={i}>{g.cau}</li>)}</ul>
        </div>
      )}
      {turn.sources?.length > 0 && <SourceLine turn={turn} />}
      {turn.notice && <p className="notice">{turn.notice}</p>}
      {banDo.length > 0 && <Suspense fallback={null}><BanDoLich items={banDo} /></Suspense>}
      {xong && (
        <div className="lich">
          <LuuLich getText={() => vanBanLich(turn, boMaTrichDan(turn.text || ""), [])} />
          {onEditPlan && <button type="button" className="retry" onClick={() => onEditPlan(null, turn.truong)}>Sửa — điền lại biểu mẫu</button>}
        </div>
      )}
    </div>
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
