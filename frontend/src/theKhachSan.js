// Thẻ khách sạn dưới câu trả lời (plan 2026-11-15-the-khach-san-chat, sha 1952c39cfc46, C): CODE quyết, không model. Hàm thuần (test bằng node:
// `backend/tests/test_the_khach_san.py`). Dữ liệu cơ sở = `/api/cho_o` (bảng lưu trú của server: tên, hạng, địa chỉ, ảnh, 2 link) — không giá / điện thoại.
// Chỉ khi lượt trả lời bằng kho trích ít nhất một bài lưu trú; khớp TÊN LÕI (bỏ tiền tố loại hình — model hay viết "Laguna Lăng Cô" thay cho
// "Khách sạn nghỉ dưỡng Laguna Lăng Cô", đếm 15/11: tên đầy đủ chỉ 4 / 12 câu), ranh giới từ như ảnh chat; tên chồng nhau ⇒ lấy tên dài nhất
// ("Villa Louise" lọt trong "Villa Louise Beach"); tối đa 3, theo thứ tự xuất hiện trong chữ.
import { tenKhop } from "./anhTraLoi.js";
import { CAN_TIEN_TO } from "./theKhachSanTrung.js";

const BAI_LUU_TRU = "travel/services/Lưu trú ở Huế";
const TIEN_TO = /^(khu nghỉ dưỡng và spa|khu nghỉ dưỡng sinh thái|khách sạn nghỉ dưỡng|khách sạn nghĩ dưỡng|khu nghỉ dưỡng|khách sạn|biệt thự du lịch)\s+/iu;
const SO_THE_TOI_DA = 3;

// tên lõi (bỏ tiền tố loại hình), thêm bản bỏ chữ "Huế" / "Hue" cuối ("Silk Path Grand Huế" ↔ "Silk Path Grand"). Mỗi tên kèm `tienTo`: tên 1 chữ
// ("Cherish", "Eldora") hoặc trùng địa danh / sự kiện / tên đường (`CAN_TIEN_TO`, sinh bằng script — "trong Thành Nội", "dịp Festival Huế") ⇒ chỉ khớp
// khi ngay trước có chữ loại hình (review E m-1).
export function tenLoi(ten) {
  const loi = String(ten || "").normalize("NFC").trim().replace(TIEN_TO, "");
  const bo = loi.replace(/\s+(Huế|Hue)$/u, "");
  return [...new Set([loi, bo])].filter(Boolean).map(t => ({ t, tienTo: t.split(/\s+/).length < 2 || CAN_TIEN_TO.has(t) }));
}

const LOAI_HINH = "(?:[Kk]hách [Ss]ạn(?: [Nn]ghỉ [Dd]ưỡng)?|[Kk]hu [Nn]ghỉ [Dd]ưỡng|[Rr]esort|[Hh]otel)\\s+";
function mauKhop({ t, tienTo }) {
  if (!tienTo) return tenKhop(t);
  const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(?<![\\p{L}\\p{N}])${LOAI_HINH}${esc(t)}(?![\\p{L}\\p{N}])`, "u");  // tên giữ đúng hoa / thường khi đi sau chữ loại hình
}

export function phangCoSo(choO) {  // `/api/cho_o` ⇒ danh sách cơ sở phẳng
  return (choO?.nhom || []).flatMap(n => (n.muc || []).flatMap(m => m.co_so || []));
}

export function theKhachSan(turn, coSo) {
  if (!turn || turn.phase !== "done" || turn.outcome !== "success" || turn.tuChoiKho || turn.web || turn.lich || turn.lichV2
      || turn.clarify || turn.suaThe) return [];
  if (Array.isArray(turn.luuTru?.co_so) && turn.luuTru.co_so.length > 0) {
    return turn.luuTru.co_so.slice(0, 5);
  }
  if (!Array.isArray(turn.sources) || !Array.isArray(coSo) || coSo.length === 0) return [];
  if (!turn.sources.some(s => typeof s.bai_id === "string" && s.bai_id.startsWith(BAI_LUU_TRU))) return [];
  const chu = String(turn.text || "").normalize("NFC");
  const khop = [];
  for (const c of coSo) {
    for (const t of tenLoi(c.ten)) {
      const re = mauKhop(t);
      if (!re) continue;
      const m = new RegExp(re.source, "gu");
      for (let x; (x = m.exec(chu));) khop.push({ c, dau: x.index, cuoi: x.index + x[0].length });
    }
  }
  // tên nằm trọn trong một tên khớp dài hơn ⇒ bỏ (Villa Louise ⊂ Villa Louise Beach)
  const giu = khop.filter(k => !khop.some(o => o !== k && o.dau <= k.dau && o.cuoi >= k.cuoi && o.cuoi - o.dau > k.cuoi - k.dau));
  const ra = [];
  for (const k of giu.sort((a, b) => a.dau - b.dau)) if (!ra.includes(k.c)) ra.push(k.c);
  return ra.slice(0, SO_THE_TOI_DA);
}
