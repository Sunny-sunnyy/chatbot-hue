# Dữ liệu lịch còn hở — bữa chưa có gợi ý, ảnh đèo Hải Vân, nguồn thứ hai chợ Bến Ngự

E, 19:41 15/11/2026 (`date`). Việc A giao tối 15/11 (handoff mục 3 + 4b). Nhánh `p9-lich-ho` từ origin/main `aa0a9ae`. Mức nhẹ: một review cả nhánh.

## Tóm tắt

| Việc | Kết quả | Căn cứ |
|---|---|---|
| Đo lại "bữa có quán kho" trên bảng 41 điểm | **63,9 %** (14.545 / 22.752 bữa); bảng 34 điểm cùng công cụ ra 69,1 % (khớp số cũ) | [đã chạy] A chạy lại khớp |
| Bữa tối sau đèo Hải Vân (72 bữa mô phỏng trống) | thêm ghi chú ăn — cùng câu, cùng căn cứ kho với bữa trưa | kho (bài về đèo + bài về đầm cạnh đó); 0 lượt tra |
| Bữa trưa / tối ở làng nón Tây Hồ (144 bữa trống) | thêm ghi chú ăn **không nêu tên quán**: chưa có gợi ý quán gần làng, cách trung tâm khoảng 12 km, nên ăn ở trung tâm | khoảng cách: kho; "chưa có gợi ý": quán gần nhất trong bảng cách ~6 km; tra 3 lượt **chưa có nguồn** nào nêu quán tại làng |
| Ảnh đèo Hải Vân (lịch + Khám phá) | đổi ảnh đoàn tàu trên sườn đèo ⇒ **cửa ải Hải Vân Quan** sau trùng tu, Commons CC BY 4.0, cắt khung quanh cổng; không người, không chữ số | E nhìn 26 ứng viên Commons; A nhìn lại trước merge |
| Nguồn thứ hai cho thời lượng chợ Bến Ngự | **có**: một bài hướng dẫn (đăng 11/09/2026) xếp khung dạo chợ 90 phút — E đọc được trang. Nhãn thời lượng giữ nguyên (90 và ~120 phút cùng một nhãn) | 3 lượt tra; ghi ở file căn cứ private, ghép vào bảng điểm bản kế |

Tiền: Serper 6 lượt = **0,006 USD**; Commons, WebFetch 0; không lượt model nào.

## Số đếm trước ⇒ sau (3.840 khung mô phỏng, 0 USD) [đã chạy]

| Đo gì | main `aa0a9ae` | nhánh | Ghi chú |
|---|---|---|---|
| Bữa | 22.752 | 22.752 | |
| Bữa có ≥ 1 quán | 17.115 (75,2 %) | 17.115 | không đổi — nhánh không thêm quán |
| Bữa có ≥ 1 quán kho | 14.545 (63,9 %) | 14.545 | |
| Bữa chỉ có ghi chú ăn | 2.336 | 2.552 | +216 = 144 (Tây Hồ) + 72 (Hải Vân tối) |
| Bữa trống | 3.301 (14,5 %) | **3.085 (13,6 %)** | |
| Bữa có quán hoặc ghi chú | 85,5 % | **86,4 %** | |

Bữa còn trống sau nhánh, theo điểm: vùng phá (1.824), một điện thờ ven sông thượng nguồn (688), một không gian nghệ thuật ở đồi phía tây nam (481), biển (88), thác phía nam (4). Chưa làm — ngoài việc được giao.

**Một dòng cho A hỏi User (cụm nam xa, 2.412 bữa, 0 quán kho):** cả 4 điểm của cụm đều đã có ghi chú ăn (sau nhánh: 100 % bữa của cụm có dòng). Muốn có **quán kho** thì chỉ đầm ở chân đèo là làm được: 2–4 bài quán ven đầm (bộ chọn lấy ≤ 2 quán / bữa, không lặp trong chuyến) phủ 660 bữa ⇒ số quán kho toàn bảng 63,9 ⇒ khoảng 66,8 %. Đỉnh đèo (704 bữa): bảng quán không có quán nào trong 2 km, khu nhà hàng kho nhắc tới nằm ở chân đèo — giữ ghi chú; vườn quốc gia + thác (1.048 bữa) kho đã nói không có quán. Không làm thì không sai: người dùng vẫn thấy câu chỉ chỗ ăn, chỉ thiếu tên quán cụ thể.

## Thay đổi

- `backend/llm/quan_lich.py`: `GHI_CHU_AN` thêm 3 khoá (đèo / tối; làng nón / trưa, tối). Ghi chú chỉ hiện khi bữa đó không chọn được quán — như các khoá cũ.
- `backend/tests/test_quan_lich.py`: thêm một ca (sáng ở làng nón, chiều ở đèo ⇒ hai bữa ra đúng hai ghi chú, không quán). Test cũ đã kiểm mọi khoá ghi chú: điểm có trong bảng và không có quán nào trong 2 km.
- `frontend/public/anh/kp/k15551t8.jpg` + `frontend/public/anh/lich/deo_hai_van.jpg`: ảnh mới (480 × 360, cùng tên file ⇒ `anhBai.js` không đổi).
- `backend/config/settings.yaml`: `lich_trinh_bang_anh` ⇒ `bang_anh_v6.json` (md5 `eb99b39803f9`; = v5 đổi tác giả / giấy phép / trang của một dòng; vẫn 40 / 41 điểm).
- Private: `data/lich_ho_2026-11-15/` (kết quả tra, 26 ứng viên ảnh + tấm ghép, `bang_anh_kham_pha_v10.json`, `can_cu_bo_sung.json`, công cụ đếm `tools/dem_bua.py`); script dựng ảnh Khám phá đọc thêm v10 (chạy lại: đúng 1 file ảnh đổi); Docker nháp trỏ bảng ảnh v6 (sao lưu `sao_luu_2026-11-15_toi/`).

## Kiểm

| Bước | Kết quả | Thời gian |
|---|---|---|
| `test_quan_lich.py` | 16 passed | 12 s |
| 5 file test chạm bảng ảnh / ăn uống + `test_static_ui.py`, **không** khoá | 397 passed | 75 s |
| cùng bộ, **có** khoá | 397 passed | 83 s |
| `npm run build` | đạt | < 1 s |
| Đếm 3.840 khung trước / sau | bảng trên | ~10 s mỗi lượt |
| Playwright | không chạy — chỉ đổi ảnh + dữ liệu ghi chú (luật bớt test 15/11) | — |
| Lượt có phí (model) | không — ghi chú do code nối, không vào chuỗi gửi model | 0 USD |

**Quét nhãn bộ đo khi đổi bảng (W84):** bảng đổi là bảng ảnh lịch (một dòng, cùng id điểm, cùng tên file) — không bộ đo nào có nhãn theo ảnh; bảng điểm, toạ độ, quán, lưu trú **không đổi** ⇒ mô phỏng nhãn không cần chạy lại. Ghi chú ăn không nằm trong nhãn bộ chuỗi sửa lịch (nhãn theo điểm / buổi).

## Giới hạn / chưa làm

- Câu ghi chú ở làng nón là lời khuyên suy từ "bảng không có quán gần + cách trung tâm ~12 km", không phải nguồn nào nói "ở làng không có quán" — reviewer cân câu chữ.
- Nguồn thứ hai của chợ là **khung giờ trong một lịch trình gợi ý**, không phải câu "mất khoảng … tiếng"; nguồn một vẫn bị chặn khi tải trực tiếp. Chưa ghép vào bảng điểm (không đổi nhãn nên không dựng bảng mới chỉ vì một dòng căn cứ).
- Ảnh mới chụp cổng từ phía trong khu di tích, có cột điện cao thế trong khung (không cắt bỏ được mà vẫn giữ cổng ở giữa).
- Biển (ảnh lịch còn trống 1 / 41) không thuộc việc này.
