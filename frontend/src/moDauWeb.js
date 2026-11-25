// Câu kho thiếu mà mục "Từ web (chưa kiểm)" ngay dưới có nội dung (chủ dự án chọn 25/11: bỏ bong bóng lặp phía trên): server GIỮ
// câu từ chối chuẩn (sàn closed-world, bộ chấm dựa vào nó); chỉ GIAO DIỆN bỏ câu từ chối chuẩn ở trên khi `web.outcome === "co_muc"`, để hiện thẳng
// khung "Từ web (chưa kiểm)". Mục web trắng / câu cố định / trả lời một phần vẫn giữ phần chữ còn lại bình thường.
// Hàm thuần, test bằng node: `backend/tests/test_mo_dau_web.py` (test đối chiếu chuỗi với `INSUFFICIENT_ANSWER` của server).
export const CAU_TU_CHOI = "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.";

export function moDauWeb(text, web) {
  if (web?.outcome !== "co_muc" || typeof text !== "string") return text;
  const dau = text.trimStart();
  return dau.startsWith(CAU_TU_CHOI) ? dau.slice(CAU_TU_CHOI.length).trimStart() : text;
}
