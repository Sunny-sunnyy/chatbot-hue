// Câu kho thiếu mà mục "Từ web (chưa kiểm)" ngay dưới có nội dung (User chọn 17/11): server GIỮ câu từ chối chuẩn (sàn closed-world, bộ chấm
// dựa vào nó); chỉ GIAO DIỆN thay câu mở đầu đó bằng câu dẫn sang mục web. Mục web trắng / câu cố định (outcome khác "co_muc") ⇒ giữ câu cũ.
// Hàm thuần, test bằng node: `backend/tests/test_mo_dau_web.py` (test đối chiếu chuỗi với `INSUFFICIENT_ANSWER` của server).
export const CAU_TU_CHOI = "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.";
export const CAU_DAN_WEB = "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm).";

export function moDauWeb(text, web) {
  if (web?.outcome !== "co_muc" || typeof text !== "string") return text;
  const dau = text.trimStart();
  return dau.startsWith(CAU_TU_CHOI) ? CAU_DAN_WEB + dau.slice(CAU_TU_CHOI.length) : text;
}
