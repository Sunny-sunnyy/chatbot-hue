# Mục web: bỏ số 0 đầu nhóm 2 chữ số khi so số — **BỎ, không merge** (A quyết: cứu 0 / 76, nới một rào số) — B · 12:18 15/11/2026

Rà nợ 15/11 (`b_ra_no_cu.md`), A duyệt. Nhánh `p9-web-so-0` từ main `0f739ed`. 0 USD.

- **Lỗi:** `tra_web._chuoi_so` so dãy chữ số ⇒ "8/11" (`811`) ≠ "08/11" (`0811`) ⇒ mục web đúng bị thay câu cố định. Ca thử tái hiện [Chạy].
- **Sửa** (`backend/llm/tra_web.py` `_chuoi_so`, 1 dòng + chú thích): nhóm đúng 2 chữ số có số 0 đầu bỏ số 0 ("08" ⇒ "8"); nhóm dài hơn (mã vùng, số điện thoại) giữ nguyên.
- **Test** (`tests/test_b6_tra_web.py`): "06:30" ↔ "6:30" đạt; "6:03" ≠ "6:30" vẫn chặn; "8/11" ↔ "08/11" và "09/11" ↔ "9/11" đạt; "18/11" ≠ "8/11" vẫn chặn (C). 103 đạt (22 s).
- **Đếm lại trên 76 mục web đã lưu** (`data/dem_web_thay_cau_2026-11-14/dem.py`, main ↔ nhánh): bị thay **21 ⇒ 21** — sửa này **cứu 0 mục**: các mục bị chặn vì năm "2026"
  (script đếm không truyền câu hỏi nên luật miễn năm không áp), "39", số tiền — không mục nào do số 0 đầu.
- **Đánh giá thẳng:** lỗi có thật nhưng **0 lần gặp** trên dữ liệu đã lưu (luật "đếm lỗi trước khi xây": số đếm không ủng hộ). Code đã viết, 1 dòng, có test ⇒ A chọn merge (phòng ngày / giờ viết "08/11") hay bỏ.

**Quyết (A, 15/11):** bỏ — 0 / 76 mục được cứu, phần sửa nới lỏng rào số của mục web; luật "đếm trước khi xây": không đủ lỗi ⇒ không làm. Bài học (A): việc sửa rào ⇒ đếm trước rồi mới duyệt. Nhánh `p9-web-so-0` xoá lúc dọn cuối phiên.
