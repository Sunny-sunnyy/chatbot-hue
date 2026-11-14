# Quán ăn gợi ý trong lịch bản 2: implementation (C, nhánh `p9-quan-lich` `b03ed28`)

Cập nhật: 16:39 14/11/2026 (C). Plan `docs/superpowers/plans/2026-11-14-quan-trong-lich-plan.md` (A duyệt; số sửa sha `3ebeebee4361`). Cờ `quan_lich` **TẮT** trong commit; chỉ bật tạm trong worktree lúc đo, đã trả về.
A chốt câu ODbL: **không** hiện dòng "© OpenStreetMap contributors". Nguồn ghi trong bảng dữ liệu + report. Nhãn "từ bản đồ mở, chưa kiểm" giữ.

## Người dùng thấy gì
Mỗi ngày có tối đa hai dòng:
- "Ăn trưa gần <điểm cuối buổi sáng>";
- "Ăn tối gần <điểm buổi tối>" (không có điểm buổi tối ⇒ gần điểm cuối buổi chiều).

Mỗi dòng ≤ 2 quán:
- quán có bài kho ⇒ bấm mở bài ở Khám phá;
- quán OSM / dữ liệu mở ⇒ nhãn "chưa kiểm" + link bản đồ.

Không giờ, không giá, không điện thoại. Chữ chép / tải có thêm khối "Ăn uống gợi ý".
**Ngoài 3 cụm trung tâm (bờ nam, Kinh thành, An Cựu) gần như chỉ có quán OSM chưa kiểm.**

## Đổi gì
| File | Việc |
|---|---|
| `backend/llm/quan_lich.py` (mới) | Nạp + kiểm bảng: tên ≤ 80 ký tự, không ký tự điều khiển / link / thẻ; loại / cụm / nguồn đã biết; link OSM đúng gốc. Chọn quán: cùng cụm, ≤ 2 km, quán kho trước, quán ăn trước cà phê, gần trước, không lặp. Dòng chữ cho nút chép. Toàn bộ do code. |
| `backend/llm/assistant.py` | Cờ `quan_lich` + bảng + toạ độ điểm. Kiểm "cần cờ bản 2 + bảng" lúc khởi động. |
| `backend/llm/len_ke_hoach.py`, `lich_trinh_v2.py` | Cờ bật ⇒ `lich["an"]` sau `dung_lich` (cả lượt sửa lịch). `ghep_chu` thêm khối. Không vào `tin_nhan_model`. |
| `backend/config/settings.yaml` | `quan_lich: false` + `lich_trinh_bang_quan`. |
| `frontend/src/LichV2.jsx`, `lkh.css` | Dòng "Ăn trưa / Ăn tối" cuối mỗi ngày. Link quán kho ⇒ `#/kham-pha/bai/…`; link khác chỉ nhận gốc bản đồ của lịch, tab mới khi bấm. |
| `backend/tests/test_quan_lich.py` (mới), `test_cong_dot_1.py` | 10 test. `flags_from` ghim thêm `quan_lich: False`. |
| `data/quan_lich_2026-11-14/tools/dung_bang.py` ⇒ `data/phase_9/lich_trinh/bang_quan_lich_v1.json` (private, md5 `dedc8051bee6`) | 460 quán = 28 quán kho + 4 dữ liệu mở thành phố + 428 OSM trong cụm. Tên OSM có chữ cà phê ⇒ loại cà phê. |

**Ba quyết định trong phạm vi plan** (đều do lượt đo bắt):
1. **Trần 2 km.** Mô phỏng đầu có p95 9,3 km: cụm rộng (phá, biển, lăng xa) ⇒ dòng "ăn gần X" sai nghĩa. Điểm không có toạ độ ⇒ không có dòng.
2. **Bữa tối gần điểm buổi tối.** Playwright lần 1 cho thấy "ăn tối gần Đầm Chuồn" trong khi buổi tối của lịch ở Chợ Đông Ba.
3. **Tên OSM có chữ cà phê ⇒ cà phê.** Người xem bắt 2 tiệm cà phê bị gắn loại "quán ăn".

## Đo [Chạy]
| Bộ | Kết quả |
|---|---|
| 3.840 khung, mô phỏng 0 USD (`tools/mo_phong.py` ⇒ `mo_phong.json`) | 0 quán ngoài bảng · 0 khác cụm · 0 lặp trong chuyến. Bữa có dòng **80,7 %** (18.306 / 22.680). Khoảng cách trung vị **0,78 km**, p95 1,94 km, max 1,99 km. |
| Chuỗi gửi model | giống byte dù có hay không `lich["an"]` (test). Cờ tắt ⇒ `ghep_chu` giống bản trước. Không chạy bộ 228 vì code không chạm phần dựng chuỗi. |
| Người xem 10 lịch (agent con ngữ cảnh mới; 8 / 10 có buổi ở Thủy Xuân / Kim Long) | **10 / 10** đạt cả 3 câu: hợp chỗ · nhãn đúng nguồn · không số / giờ lạ. File `data/quan_lich_2026-11-14/xem_10.md`, chấm `xem_10_cham.md`. |
| Playwright 1440, bản build thật, lịch thật 3 ngày (`tools/pw_quan.py`) | **ĐẠT**: dòng hiện; 1–2 quán / dòng; link kho đúng `#/kham-pha/bai/`; link khác đúng gốc bản đồ + `_blank` + `noopener` + nhãn "chưa kiểm"; 0 lỗi console; 0 yêu cầu ra ngoài. Ảnh `data/quan_lich_2026-11-14/anh/`. |
| Test file chạm (`test_quan_lich`, `test_cong_dot_1`, `test_luu_tru_lich`, `test_len_ke_hoach_v2`, `test_static_ui`) | 131 đạt không khoá (56 s) · 131 đạt có khoá (52 s) |

**Tiền:** 2 lượt xếp lịch thật cho Playwright ≈ **0,0013 USD**. Mô phỏng, người xem: 0 USD.

## Giới hạn (ghi để User biết)
- **Ngoài trung tâm gần như chỉ có quán OSM chưa kiểm.** Người xem nhận xét tên quán ở Thủy Xuân thường mỏng: viết không dấu, tên chung chung, không biết bán món gì, có tên nghe giống nhà vườn. Nhãn đúng, nhưng khách có ít lý do để chọn.
- **Không có dòng ăn** ở phá Tam Giang, biển Thuận An, điện Hòn Chén, lăng Gia Long (> 2 km tới quán gần nhất cùng cụm), Bạch Mã / Nhị Hồ (0 quán), và điểm không có toạ độ.
- **Quán kho được ưu tiên dù xa hơn quán OSM** (vẫn ≤ 2 km), và quán ăn đứng trước cà phê — cố ý: quán kho có bài để đọc.
- Lịch mẫu "Ví dụ" chưa có dòng ăn (`/api/lich_mau` không gọi phần này) — làm thêm được nếu muốn.

## Sau review B (ready, 2 minor — đã sửa `3133c23`)
- m-1: tên quán bị chặn thêm ký tự định dạng vô hình (Unicode Cf, vd ký tự đảo chiều, ký tự không độ rộng), "//" và cú pháp link Markdown "](". Thêm 4 ca test (14 đạt). Bảng thật vẫn nạp được (0 dòng bị chặn).
- m-2: an toàn "tên quán OSM không vào model" còn dựa vào cờ `nho_cau_tra_loi: false`. Nếu sau này bật nhớ câu trả lời thì chữ lịch (cả tên quán) sẽ vào lịch sử gửi model ⇒ phải xem lại trước khi bật. Đã ghi ở đầu `quan_lich.py`.
