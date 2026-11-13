# Review: Phase 9 — "Lên kế hoạch" đợt 1 — kết quả nghiệm thu (report của B)

Decision: **ready_for_user_confirmation** cho kết luận của report: **"nghiệm thu TRƯỢT — không bật cờ"** là đúng, và số liệu trung thực (0 blocker · 0 major · 4 minor + 1 lỗi của chính bộ đo E).
Người kiểm: E (Claude Code, `hue-rag-e8`), A giao 13/11 · Date: 21:30 13/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md` bản 3 §5 · spec `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` bản 3.3 · bộ đo `data/phase_9/lich_trinh/bo_do_v2/` (E viết)
Implementation report: `report_agent/2026-11-12_ra_khoang_cach/b_len_ke_hoach_dot_1_implementation.md`

## 1. Phạm vi đã review
- **Có:** kết quả nghiệm thu (mốc `main`, hai lượt 20 yêu cầu), mô phỏng (bằng ca dò riêng), 13 ca phụ, bảng đề xuất "đoạn mô tả", việc tuân theo plan §5 (tiêu chí ghi trước, vòng chỉnh, bộ quyết chưa mở), cờ, test file mới.
- **Không:** review cả nhánh code (plan §5 ghi riêng; report §0 ghi NOT RUN — A chưa giao). Không đọc từng dòng diff 2.079 dòng; chỉ đọc `kiem_cau` / `cau_du_phong` / `chon_cau` (`backend/llm/lich_trinh_v2.py`) và `tools/nghiem_thu.py` (`cham_code`) — hai chỗ quyết định con số trượt.

## 2. Findings

**m-1 (minor) — điều kiện loại ngay "tên điểm / quán / cơ sở không có trong bảng" không được chấm.** `data/len_ke_hoach_v2_2026-11-13/tools/nghiem_thu.py` `cham_code`: `loai_ngay = tien or du_phong > 0.3 * n_cau` — thiếu vế tên ngoài bảng mà `dinh_nghia_cham.md` đòi; `kiem_cau` (code sản phẩm) chỉ bắt tên **điểm khác có trong bảng**. Report §3.4 ghi "hai điều kiện loại ngay chấm bằng code". Bằng chứng thực tế: E quét 330 câu model (2 lượt) bằng từ khoá quán / nhà hàng / khách sạn / cửa hàng / tiệm / cà phê / resort / homestay / công ty ⇒ **0 câu** — không có lỗi quan sát được, chỉ thiếu phép kiểm. **Đóng khi:** lượt nghiệm thu sau có phép kiểm này trong `cham_code` (hoặc report ghi rõ "chỉ dò từ khoá, E dò 0 / 330").

**m-2 (minor) — 3 / 80 tổ hợp không hạn chế: ba kiểu đi ra cùng một khung, không có ghi chú.** Ca dò E (gọi thẳng `xep_v2` ở `49daaa7`, mọi số ngày × sở thích 0–2 loại, không trẻ em / lớn tuổi): nhẹ ≤ cân bằng ≤ khám phá **và** khám phá > nhẹ ở **77 / 80**; trượt: lịch **1 ngày** + thiên nhiên · chụp ảnh · cả hai — hai điểm nửa ngày ở cụm phía đông lấp đủ ngày (2 ↔ 2 ↔ 2). Không dòng nào trong bộ 20 trúng ⇒ nghiệm thu không thấy; người dùng chọn "khám phá" sẽ nhận lịch y hệt "nhẹ nhàng" mà không được giải thích. Ý 3 của định nghĩa chấm sẽ trượt ở lịch đó. **Đóng khi:** khung có một ghi chú do code ("lịch 1 ngày ở khu này đã kín — chọn thêm ngày để đi nhiều điểm hơn") hoặc report ghi đây là giới hạn đã biết.

**m-3 (minor) — ghi chú bậc thang lặp theo từng điểm.** Lượt 2, Y20: **5 dòng** `bac_thang` gần giống nhau (một dòng / điểm) cạnh dòng mùa mưa + nhóm hạn chế. Không trái định nghĩa chấm (ý 2 chỉ đòi "có dòng ghi chú"), nhưng làm khối ghi chú dài. **Đóng khi:** gộp thành một dòng liệt kê tên điểm (vòng sau), hoặc A ghi không sửa.

**m-4 (minor) — chữ ở report §0 "A quyết theo plan §5".** Plan §5 chỉ ghi luật giữ / gỡ cho sàn của ô, "Luôn" và bộ quyết; không có câu nào cho "trượt bộ 20 yêu cầu". Quyết định không bật là đúng hướng, nhưng là **A quyết** (không phải luật đã ghi). **Đóng khi:** sửa chữ thành "A quyết (plan §5 không ghi luật cho trường hợp này)".

**Lỗi của bộ đo E (không phải của B):** cặp D4 trong `ca_phu_13_11.jsonl` có trẻ em ⇒ spec cho nhóm hạn chế trần luôn là "nhẹ nhàng" ⇒ cặp này không thể khác. E thiết kế sai một cặp; B chấm đúng. Ca dò m-2 thay cho cặp này.

**Đồng ý, không phải finding:**
- `tam_dung_mua` chỉ nối khi điểm bị loại là điểm ưu tiên — cách B đọc spec 5c.2 (i) hợp lý (câu spec chỉ nói ghi chú "khi đó" = điểm ưu tiên).
- Vòng chỉnh đoạn kho làm **trên chính 20 yêu cầu đã thấy** — report ghi rõ, không trình bày lượt 2 như bằng chứng không bị nắn.

**Ngoài phạm vi (ghi ngắn):** bảng điểm ghi giờ phố đi bộ cuối tuần 19:30–22:30, bài kho ghi 18:00–24:00 cùng ba tối — đưa vào phiếu D4 của User.

## 3. Cách người kiểm chạy lại thật
Script của E (không dùng `tom_tat.json` hay hàm chấm của B): `/tmp/e_rv_lkh/tinh.py` (đếm câu dự phòng theo **mẫu câu** của `cau_du_phong` trên từng `lich_cau` gửi tới trình duyệt, khung / đủ câu từ `moc_ms`), `y126.py` (ý 1, 2, 6 đọc thẳng từ `lich_khung`, cách khác `cham_code`), `do_nhiho.py`, `do_kieudi.py` (gọi `xep_v2` trong worktree `/tmp/b_lkh` @ `49daaa7`, bảng `diem_v8.json`); chunker offline cho 9 `chunk_id` đề xuất; `pytest tests/test_len_ke_hoach_v2.py` trong worktree. 0 USD, không server.

## 4. Kết quả quan sát

| Số | B báo | E tính lại | |
|---|---|---|---|
| Lịch ≤ 1 câu dự phòng — lượt 1 / lượt 2 | 16 / 17 (của 20) | **16 / 17** | khớp; 0 lịch lệch với `so_cau_du_phong` code báo |
| Lịch > 30 % câu dự phòng | lượt 1: 2 · lượt 2: 1 (33 %) | lượt 1: 2 (một lịch 10 / 10 — đầu ra model sai khuôn — + một lịch 2 / 6) · lượt 2: 1 (2 / 6) | khớp |
| Tổng câu dự phòng | — | lượt 1: 23 / 165 mục · lượt 2: 12 / 165 | |
| `lich_khung` trung vị · chậm nhất · số > 1 s | 237 / 236 ms · 1.262 / 1.266 ms · 1 | 237 / 236 · 1.262 / 1.266 · **1 / 20** mỗi lượt | khớp ⇒ tiêu chí "≤ 1 giây" **trượt** đúng như report |
| Đủ câu trung vị ↔ mốc `main` | 5,17 / 5,43 s ↔ 5,07 s | 5,174 / 5,4265 ↔ 5,070 s | khớp (+0,36 s ≤ 2 s — đạt) |
| Ý 1, 2, 6 | 20 / 20 | **0 lỗi** ở cả hai lượt (cách đếm riêng) | khớp |
| Ngày đi theo `kieu_ngay` | — | 15/11 · thứ Tư 07/04/2027 · thứ Bảy 21/11 | đúng bảng `dinh_nghia_cham.md` |
| Trường `dat` trong `tom_tat` (18 / 19) | — | = 20 − số lịch > 30 % câu dự phòng | không mâu thuẫn với "ý 1–6: 20 / 20" |
| Test file mới | 78 đạt | **78 passed** (15,1 s) | |
| Cờ trên nhánh | tắt | `len_ke_hoach_v2: false` | |
| `git diff --check main...p9-len-ke-hoach-v2` | — | sạch | 18 file, +2.079 / −44 |

**Ca dò — câu bất biến "điểm tạm dừng theo mùa không bao giờ được xếp vào ngày trong tháng dừng":** 13.176 khung (số ngày 3–5 × 3 nhóm người × 3 kiểu đi × 4 sở thích × ngày bắt đầu mỗi 3 ngày suốt 12 tháng) ⇒ điểm tạm dừng tháng 9–2 xếp **0 lần** ở ngày tháng 9–2, **1.648 lần** ở tháng 3–8 (luật không chặn nhầm); `kiem_khung_v2` 0 lỗi.

**13 ca phụ (B chạy, E đối chiếu với `ca_phu_ket_qua.txt`):** điểm tạm dừng 0 / 0 / 0 / 0 ở 4 lịch mùa mưa; đối chứng tháng 4 xếp 1 lần; dày > thong thả ở D1 4 → 8 · D2 6 → 11 · D3 2 → 3; D4 6 ↔ 6 (lỗi bộ đo E, trên).

**Bảng "đoạn mô tả" (9 chunk_id):** cả 9 có trong kho (chunker offline, đúng số thứ tự đoạn); 8 / 9 ở mục "Tổng quan" hoặc mục kiến trúc và mở đầu bằng câu tả chính điểm đó; 1 / 9 (không gian lưu niệm trong file vé) là đoạn "thông tin chung" — B đã ghi "tạm, nên bổ sung bài kho". 1 điểm không có bài riêng — B ghi "cần bổ sung kho". **Không thấy đoạn nào chọn nhầm điểm.**

## 5. Giới hạn hoặc phần chưa chạy
Không review code cả nhánh (luật xếp, giao diện, API) — việc riêng của plan §5. Phép dò m-1 chỉ bằng từ khoá — tên riêng không kèm từ chỉ loại cơ sở không bắt được. Không chạy lại lượt có phí, không Playwright. Bộ quyết 12 không mở (đúng quyết định A).

## 6. Decision và bước tiếp theo
`ready_for_user_confirmation` cho **report + kết luận "trượt, không bật cờ"**. Minor m-1 … m-4 sửa ở vòng sau cùng với cột "đoạn mô tả" (không mở vòng sửa riêng). Lượt nghiệm thu sau: bộ quyết 12 (chưa mở) + Playwright + phép kiểm m-1; E sửa bảng tra cho người chấm (đang thiếu điểm có buổi tối mà không ghi giờ).
