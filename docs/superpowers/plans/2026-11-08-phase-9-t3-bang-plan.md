# Plan T3 — bảng vé + giờ mở cửa có cấu trúc (`tra_ve_gio`)

Người viết: C · bản 1 11:03 08/11/2026 (`date`). Nền: spec Phase 9 **bản 13** §12 (User duyệt sha `5557f0fd7650`, commit `af017f6`) — dòng T3 ở §12.2, §12.4,
§12.5 + sàn §12.3. User 08/11: plan ngắn, không phần phòng xa, không mốc ngày. Mức rủi ro: trung bình (đổi đường trả lời sau cờ). Nhánh `p9-t3-bang` **sau khi** User duyệt
bảng + plan duyệt. File tracked, repo public: không chép kho / Golden; tả dữ liệu ở mức loại.

## 1. Làm gì

- **Dữ liệu (private, User duyệt):** `data/phase_9/t3_bang_ve_gio/bang_ve_gio.json` dựng từ 5 file vé + file di tích / điểm có giờ (đọc qua `scripts/grep_kb.sh`); mỗi dòng
  có file + dòng nguồn trong kho; mọi chuỗi đã kiểm có thật ở đúng dòng (`tools/kiem_nhap.py`). Nạp lúc khởi động theo đường dẫn `settings.yaml`; schema sai ⇒ lỗi khởi động.
- **Công cụ** `tra_ve_gio(diem: list[str] ≤ 5)` cho agent Huế, ≤ 1 lần / câu (đếm trong code). Code khớp tên (luật `chuan_ten` của B5 + bí danh trong bảng); trả cho model
  **một nguồn** trong sổ nguồn (như công cụ thời tiết — `assistant.py` `_nguon_thoi_tiet`): dòng vé (đối tượng · giá · đơn vị) + giờ (mùa / ngày · mở · đóng) + ngày nguồn.
  **Không** cộng / nhân (B5c âm 2 lần). Điểm không có trong bảng ⇒ câu cố định "bảng chưa có điểm này" (không thấy ≠ không tồn tại).
- **Chữ điều kiện miễn giảm không vào model:** kết quả công cụ chỉ ghi "có điều kiện miễn giảm — hiện bên dưới"; **code nối khối điều kiện nguyên văn** (bỏ trùng) dưới câu trả lời
  **mỗi khi** một dòng trả về có điều kiện, kèm tên file nguồn. Giao diện: khối Markdown sẵn có.
- **Khi nào đưa công cụ:** cờ `assistant.tra_ve_gio: false`; bật ⇒ chỉ đưa công cụ khi câu cuối / câu hỏi liền trước có từ khoá vé · giá · giờ · mở / đóng cửa · miễn / giảm
  (code dò, như `thoi_tiet` — `assistant.py` `_lich_extra`); câu khác ⇒ chuỗi gửi model **giống byte** cờ tắt.
- **Kiểm cuối (code):** mọi số tiền (`so_tien.py`) và chuỗi số giờ (bộ đếm chuỗi số của `tra_web.py`) trong chữ model ⊂ {số trong dòng bảng đã trả} ∪ {số trong đoạn kho
  được trích}; vi phạm ⇒ code thay chữ model bằng lời tối thiểu dựng từ dòng bảng (như đường dự phòng B171) + log mã.
- **Log** (`chat_metrics.tools`): `tra_ve_gio` {n_diem, n_khop, n_khong_bang, co_dieu_kien, kiem} — số / nhãn, không chữ.

## 2. Tiêu chí ghi trước (trước lượt có phí)

| Mã | Loại | Đo | Mức |
|---|---|---|---|
| Q1 | sàn | chuỗi gửi model, cờ tắt **và** cờ bật với câu không có từ khoá (`capture_all.py`) | 228 / 228 giống byte `main` |
| Q2 | quyết | bộ T3 đã thấy ~20 câu (C viết: vé từng điểm, nhiều điểm, giờ theo mùa, điểm ngoài bảng, câu miễn giảm, câu chỉ hỏi giờ), ×2 | số trong câu trả lời đúng dòng bảng (code so) ≥ n − 1 / n mỗi lượt; **0** số ngoài (kiểm cuối phải bắt trước khi tới người dùng); câu điểm ngoài bảng ⇒ câu cố định n / n |
| Q3 | sàn | khối điều kiện | mọi lượt có dòng có điều kiện ⇒ có khối (code đếm) n / n; **0** câu model tự nêu tuổi / đối tượng miễn giảm ngoài khối (code: mẫu tuổi / chiều cao / nhóm đối tượng trong chữ model ⇒ sub-agent đọc câu khớp) |
| S1 | sàn | an toàn 32 ×2 (có 6 câu miễn giảm, 5 câu giờ) | 4 số: đảo cảnh báo 0 · sai điều kiện **mới** 0 · thiếu cảnh báo **mới** 0 · ngoài kho bị trả lời 0 (thủ tục S-AT khi chênh 1) |
| S3b | sàn | các lượt cả câu ở trên | 0 câu về Huế ra `OUT_OF_SCOPE_ANSWER` (code đếm) |
| S4 | sàn | mẫu Golden 30, biến thể + mốc cùng lượt chấm mù | không tụt quá nhiễu |
| S5 / S6 | theo dõi | `chat_metrics` của lượt Q2 | chữ đầu p95 ≤ 5 s; USD / câu báo số |

Âm (Q1 / Q3 / S1 / S3b / S4 trượt, hoặc Q2 dưới mức) ⇒ cờ tắt, ghi kết quả; **phương án B** (spec): bảng chỉ dùng cho kiểm cuối (không công cụ) — code kiểm số trong câu trả
lời so với bảng, sai ⇒ câu cố định "giá / giờ có thể khác — xem nguồn". Không vòng chỉnh thứ ba.

## 3. Bộ đo + tiền

- Bộ T3 ~20 câu đã thấy (không kín — số do code kiểm, spec §12.4) viết **sau** khi User duyệt bảng; nhãn = dòng bảng đúng (id) ghi trước khi chạy.
- Thứ tự: test 0 USD (parser bảng thật, khớp tên + bí danh, điểm ngoài bảng, khối điều kiện, kiểm cuối có ca cố tình vi phạm, Q1) ⇒ pilot 3 câu ×1 ⇒ Q2 ×2 ⇒ S1 ×2 ⇒ S4 ×2.
- **Tiền ≈ 0,10 USD** ((20 + 32 + 30) × 2 × 0,0006); dừng ở 0,15. Tính vào Phase 9 (trần 3,5, quỹ B7 0,35 giữ riêng).
