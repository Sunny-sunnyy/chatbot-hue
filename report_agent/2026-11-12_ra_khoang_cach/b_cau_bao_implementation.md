# Câu hỏi bão / lũ — model chọn `loai`, code dựng phần thời tiết (B, 10:04 17/11/2026)

Plan: `docs/superpowers/plans/2026-11-17-cau-bao-plan.md` (A duyệt sha `6bea9ccb4050`, trần 0,30 ⇒ 0,35 USD). Nhánh `p9-cau-bao` (code cuối `383f055`), cờ `bao_lu_cong_cu` TẮT.
Dữ liệu đo (private): `data/cau_bao_2026-11-17/` (bộ dò do E soạn; công cụ đo ở `tools_b/`; kết quả ở `do/`).

## Lỗi
Câu hỏi bão / lũ: công cụ thời tiết trả bảng mưa cho model ⇒ model tự viết câu kết luận "không xác nhận có bão". Mốc cờ tắt, câu gốc ×5: **3 / 5 lượt** (khớp tự thử 16/11).

## Đã làm (cờ bật)
1. Công cụ `thoi_tiet` có tham số `loai` (`du_bao` | `bao_lu`) do model chọn. Mô tả công cụ riêng cho cờ bật; cờ tắt ⇒ schema + mô tả cũ.
2. Lượt `bao_lu` (model chọn, hoặc lưới từ khoá rộng khớp ở câu cuối / câu liền trước): model nhận một nguồn KHÔNG số. Code nối: câu nhãn "Dự báo dưới đây chỉ có nhiệt độ và mưa, không có thông tin bão hay áp thấp." + bảng số + câu NCHMF / 112. Model trả câu từ chối ⇒ câu dẫn cố định "Mình không theo dõi được tin bão / lũ — bạn xem bản tin chính thức dưới đây." (thay sau bước kiểm citation; stream giữ chữ như `CAU_DAN_DU_BAO`).
3. Lưới khớp mà model không gọi công cụ (trả lời từ kho) ⇒ code đặt câu "Mình không theo dõi được tin bão / lũ hiện tại — dưới đây là thông tin chung từ tài liệu." LÊN TRƯỚC chữ model (trừ khi model từ chối hoặc lượt có lịch).
4. Cổng đưa công cụ: từ thời tiết cũ + danh sách ĐÓNG các từ nguy hiểm thời tiết (khớp `tra_web._THIEN_TAI` + giông, lốc, mưa đá, nước dâng), câu cuối hoặc câu liền trước.

## Diễn biến đo (mọi số do B đếm bằng code; S-a do agent con của A đọc 100 %)
| Bước | Kết quả | Tiền |
|---|---|---|
| Bước 0 (hàm thuần) | cổng nới bắt 21 / 22 câu cần đi đường bão ⇒ luật chuyển hướng 2.5 bật: thử "luôn đưa công cụ ở tuyến trợ lý Huế" | 0 |
| Mốc cờ tắt, câu gốc ×5 | 3 / 5 lượt tự nhận định | 0,0041 |
| "Luôn đưa công cụ" — bộ 31 + 3 câu dự báo thường | S-b 19 / 19 (22 / 22); S-c 3 / 3; khối thừa nhãn khong 3 / 5; 0 rút lại. Đọc tay: S-a2 = 0, nhưng câu dẫn bản đầu đọc được thành "không có bão" và một câu trả lời từ kho mở bằng "Có." ⇒ sửa (2) và (3) | 0,0306 |
| — an toàn 32 tắt ×1 ↔ bật ×2 | 0 đổi lớp; từ chối 3 = 3 = 3; 0 rút lại | 0,0697 |
| — Golden 176 tắt ↔ bật | **sàn (ii) trượt 1 câu**: một câu ngoài kho, không có từ thời tiết, model gọi công cụ rồi từ chối ⇒ bảng mưa thay câu từ chối. Gọi thừa 2 / 176 (≤ 3) | 0,1855 |
| Lùi theo luật 2.5 (User chọn) — bộ 31 + 3 câu thường + câu chạm (an toàn 4 ×2, Golden 3) | S-b 18 / 19 (21 / 22 ≥ 20), chỉ sót câu nói vòng không từ khoá; S-c 3 / 3; khối thừa nhãn khong 3 / 5; an toàn 0 đổi lớp; Golden 3 câu chạm trả lời như cờ tắt; 0 rút lại | 0,0369 |

Tổng ≈ **0,33 USD** (log `chat_metrics` của server tạm + trường `usd` của file kết quả). Chữ đầu trên bộ bão (sau lùi) p50 4,38 s / p95 7,42 s — trên sàn 3 / 5 s, nhưng mốc cờ tắt của câu gốc p50 6,9 s (câu thời tiết vốn có 2 lần gọi model + gọi Open-Meteo); câu dự báo thường p50 ≈ 2,5–3,0 s.

## Kiểm tất định
- `tests/test_b5b_thoi_tiet.py` 115 đạt (trước nhánh 92; 23 ca mới tính cả tham số: từng loại lượt §4c — lượt đầu, hỏi tiếp có lịch sử, stream, song song định tuyến, câu từ chối, câu đầu, cổng nới, cờ tắt giữ schema).
- Q1: cờ tắt ⇒ chuỗi gửi model giống byte main 228 / 228.
- Test rộng (trên `2a2e940`): 1310 đạt; 8 hỏng môi trường (khoá API 4, bản build giao diện 4). Commit sau chỉ chạm 3 file đã chạy test file.

## Giới hạn
- Câu bão nói vòng không chứa từ thời tiết / nguy hiểm nào (1 / 22 câu của bộ) ⇒ không công cụ, không khối.
- Câu "giống mà không phải" có từ bão / lũ (tên phim, "bão giá", "lũ trẻ") ⇒ khối NCHMF thừa (3 / 5); có lượt model chọn `bao_lu` ở câu loại này ⇒ thêm bảng số thừa.
- Câu hỏi tiếp không liên quan ngay sau câu bão ⇒ khối thừa (lưới xét câu liền trước).
- Câu ghép bão + ý khác: phần ý khác có thể ngắn / mất (đọc tay).
- Lỗi mới thấy ở Golden là lý do lùi; nếu sau này muốn "luôn đưa công cụ" thì phải sửa riêng đường "gọi công cụ rồi từ chối ⇒ câu dẫn + bảng số".
