// Ảnh dưới câu trả lời của trợ lý (E 14/11, plan A duyệt; C 15/11 thêm nhiều ảnh theo tên): CODE quyết, không model. Một ảnh của bài nguồn khi câu trả lời là về MỘT nơi / món:
// lượt xong, trả lời bằng kho (không từ chối / ngoài phạm vi / hỏi lại / lịch / có mục web), mọi nguồn được trích thuộc đúng MỘT bài, bài đó là
// loại "một nơi / món" (không bài gốc lĩnh vực, vé tham quan, dịch vụ / lưu trú), có ảnh và ảnh không bị đánh "không chắc" (`kc`).
// Hàm thuần (test bằng node: `backend/tests/test_anh_tra_loi.py`).
import { anhCuaBai } from "./anhBai.js";

// mã bài = đường dẫn bài trong kho `<lĩnh vực>/<loại>/<tên>.md`; bài ngay gốc lĩnh vực (2 đoạn) = bài tổng quan
export const LOAI_MOT_NOI = new Set(["restaurants", "cafes", "local_specialties", "heritage", "festival", "arts", "places"]);

export function loaiCuaMa(id) {
  const p = String(id).split("/");
  return p.length >= 3 ? p[1] : null;  // như `loai_con` của `/api/kham_pha` (api/routes/cong.py)
}

// Tên bài dùng để khớp trong chữ trả lời: bỏ phần trong ngoặc, NFC; tên < 2 chữ ("Ga Huế" đủ, "Chè" không) ⇒ không khớp (dễ trùng lời thường).
// Khớp theo RANH GIỚI TỪ và giữ hoa / thường trừ chữ đầu (review E): "Quán Nhỏ" không còn khớp "một quán nhỏ"; "chợ Xép" vẫn khớp "Chợ Xép".
// Giới hạn đã biết: tên mà chữ sau cũng là chữ thường trong câu (vd "Lý Huế" ↔ "quản lý Huế") vẫn khớp nếu bài đó được trích. Giữ hoa cả chữ đầu
// chặn được nhưng mất 14 / 39 ảnh mới đúng (mô phỏng 15/11: model hay viết "chợ …", "lăng …").
export function tenKhop(title) {
  const t = String(title || "").replace(/\s*\([^)]*\)\s*/g, " ").trim().normalize("NFC");
  if (t.split(/\s+/).length < 2) return null;
  const dau = t[0], esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(?<![\\p{L}\\p{N}])[${esc(dau.toLowerCase())}${esc(dau.toUpperCase())}]${esc(t.slice(1))}(?![\\p{L}\\p{N}])`, "u");
}

const SO_ANH_TOI_DA = 3;

// Danh sách ảnh dưới câu trả lời (plan 2026-11-15-anh-trong-chat, sha bf43cc57f6ea): `[{anh, baiId, ten}]`, rỗng ⇒ không ảnh.
// - Mọi nguồn trích thuộc MỘT bài ⇒ như luật cũ: 1 ảnh (không cần tên trong chữ).
// - Nguồn thuộc ≥ 2 bài ⇒ theo thứ tự ở dòng Nguồn, bài "một nơi / món", ảnh chắc, tên ≥ 2 chữ CÓ trong chữ trả lời hoặc câu hỏi (ranh giới từ); tối đa 3.
//   `turn.sources` = nguồn ĐƯỢC TRÍCH do server gửi (api/routes/chat.py `_source_responses(trace.cited)`) ⇒ ảnh chỉ của bài câu trả lời dựa vào.
export function anhTraLoi(turn) {
  if (!turn || turn.phase !== "done" || turn.outcome !== "success" || turn.tuChoiKho || turn.web || turn.lich || turn.lichV2
      || turn.clarify || turn.suaThe || !Array.isArray(turn.sources) || turn.sources.length === 0) return [];
  // thứ tự như dòng "Nguồn" (SourceLine.jsx: theo `turn.numbers` = số trích hiện trong chữ) ⇒ ảnh đứng cùng thứ tự người đọc thấy tên nguồn
  const nguon = turn.numbers instanceof Map
    ? [...turn.sources].sort((a, b) => (turn.numbers.get(String(a.id)) ?? Infinity) - (turn.numbers.get(String(b.id)) ?? Infinity)) : turn.sources;
  const ten = new Map();
  for (const s of nguon) if (s.bai_id != null && !ten.has(s.bai_id)) ten.set(s.bai_id, s.title);
  const bai = [...new Set(nguon.map(s => s.bai_id))];
  const dung = id => id != null && LOAI_MOT_NOI.has(loaiCuaMa(id)) && anhCuaBai(id) && !anhCuaBai(id).kc;
  const ra = id => ({ anh: anhCuaBai(id).anh, baiId: id, ten: ten.get(id) });
  if (bai.length === 1) return dung(bai[0]) ? [ra(bai[0])] : [];
  // tên có trong chữ trả lời HOẶC trong câu người dùng hỏi (plan bản 2, sha 6c8973b89ebd: hỏi đích danh một nơi mà câu trả lời không nhắc lại tên);
  // bài vẫn phải là nguồn được trích
  const chu = String(turn.text || "").normalize("NFC"), hoi = String(turn.question || "").normalize("NFC");
  return bai.filter(id => { const re = dung(id) && tenKhop(ten.get(id)); return re && (re.test(chu) || re.test(hoi)); }).slice(0, SO_ANH_TOI_DA).map(ra);
}
