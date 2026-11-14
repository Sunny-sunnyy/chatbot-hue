// Ảnh dưới câu trả lời của trợ lý (E 14/11, plan A duyệt): CODE quyết, không model. Một ảnh của bài nguồn khi câu trả lời là về MỘT nơi / món:
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

export function anhTraLoi(turn) {
  if (!turn || turn.phase !== "done" || turn.outcome !== "success" || turn.tuChoiKho || turn.web || turn.lich || turn.lichV2
      || turn.clarify || turn.suaThe || !Array.isArray(turn.sources) || turn.sources.length === 0) return null;
  const bai = [...new Set(turn.sources.map(s => s.bai_id))];
  if (bai.length !== 1 || bai[0] == null || !LOAI_MOT_NOI.has(loaiCuaMa(bai[0]))) return null;
  const a = anhCuaBai(bai[0]);
  if (!a || a.kc) return null;
  return { anh: a.anh, baiId: bai[0], ten: turn.sources[0].title };
}
