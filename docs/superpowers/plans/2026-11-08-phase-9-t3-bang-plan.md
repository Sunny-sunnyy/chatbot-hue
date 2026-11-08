# Plan T3 — bảng vé + giờ mở cửa có cấu trúc (`tra_ve_gio`)

Người viết: C · **bản 2** 11:10 08/11/2026 (`date`) — sửa theo review vòng 1 `…t3-bang-plan_review.md` (0 / 6 / 4) · bản 1 `81767d819e13`. Nền: spec Phase 9 **bản 13** §12
(User duyệt `5557f0fd7650`, commit `af017f6`) — T3 ở §12.2, §12.4, §12.5 + sàn §12.3. User 08/11: plan ngắn, không mốc ngày. Mức rủi ro: trung bình (đổi đường trả lời
sau cờ). Nhánh `p9-t3-bang` **sau khi** User duyệt bảng + plan duyệt. Repo public: không chép kho / Golden; tả dữ liệu ở mức loại.

## 1. Làm gì

- **Dữ liệu (private, User duyệt):** `data/phase_9/t3_bang_ve_gio/bang_v1.json` (bản duyệt của `bang_nhap.json`: User câu 1 (a) 08/11, A theo khuyến nghị câu 2–5 — `phieu_cho_user.md`); mỗi ô có file + dòng kho;
  mọi chuỗi kiểm có thật ở đúng dòng (`tools/kiem_nhap.py`, 1.011 / 1.011 ở nháp). **Chỉ nạp khi cờ bật** (khuôn `nap_bang_lich`, `assistant.py:109-110`); schema sai ⇒ lỗi khởi động.
- **Công cụ** `tra_ve_gio(diem: list[str] ≤ 5)`, ≤ 1 lần / câu (đếm trong code). Khớp tên bằng `chuan_ten` (`lich_trinh.py:90`) + bí danh trong bảng. **Không** cộng / nhân.
  Điểm ngoài bảng ⇒ câu cố định "bảng chưa có điểm này" (không thấy ≠ không tồn tại).
- **Trường nào đi đâu (M-2):**

| Trường bảng | Gửi model | Chỉ khối code | Ghi |
|---|---|---|---|
| tên điểm · loại vé · `doi_tuong` (nhãn hàng, kể cả khoảng tuổi ghi trong nhãn) · giá · đơn vị — **dòng giá là số** | ✓ | | nhãn hàng cần để nói giá đúng đối tượng |
| dòng giá "miễn phí" / 0 · `mien_giam[]` · `ghi_chu_nguyen_van` · quy định chung (theo phiếu câu 4a) | | ✓ | model chỉ thấy một câu "có điều kiện miễn giảm — hiện bên dưới" (bài học B5c: model bỏ điều kiện miễn cho trẻ nhỏ) |
| giờ: `mua_hoac_ngay` · `muc` · mở · đóng | ✓ | | |
| ngày nguồn | ✓ | ✓ | |
| file + dòng | | ✓ | hiện ở dòng "Nguồn" |

- **Nguồn — lệch spec §12.5, có lý do (M-5):** spec ghi "dòng + `[n]` đoạn nguồn (như B5 D6)". Plan dùng khuôn **nguồn do code dựng** của công cụ thời tiết (`_nguon_thoi_tiet`,
  `assistant.py:400-408`): **một nguồn cho mỗi file kho** có dòng được trả, `source` = **đường dẫn file kho thật** ⇒ dòng "Nguồn" mở được bài gốc ở Khám phá (`bai_id`);
  chữ nguồn = các dòng bảng đã gửi model. Lý do: B5c D10 tìm đoạn kho thật cho từng dòng vé chỉ được 10 / 12 (`b162` dòng 24 (d)); số trong bảng đã kiểm nguyên văn có file:dòng.
  **A chấp nhận lệch này hoặc yêu cầu theo spec** trước khi code.
- **Khi nào đưa công cụ (m-2):** cờ `assistant.tra_ve_gio: false`; bật ⇒ chỉ khi câu cuối / câu hỏi liền trước khớp regex có ranh giới từ (khuôn `thoi_tiet._TU_KHOA` +
  `co_tu_khoa_luot`): `\bvé\b`, `giá vé`, `bao nhiêu tiền`, `mất tiền`, `\bphí\b` (gồm "miễn phí", "lệ phí"), `mở cửa`, `đóng cửa`, `mấy giờ`, `giờ (mở|đóng|tham quan|hoạt động)`,
  `\bmiễn\s+(giảm|phí|vé)`, `\bgiảm\s+(giá|vé|\d+\s*%)`, `ưu đãi`. Không khớp "bây giờ", "bao giờ", "đánh giá", "miễn là". Regex chốt trong test **trước** lượt có phí: mọi câu
  bộ T3 + 6 câu miễn giảm của bộ an toàn trúng; ≥ 5 câu thường gần giống không trúng.
- **`max_turns` (M-3):** lượt có `tra_ve_gio` ⇒ `max_turns` = 4 + 1 (chuỗi xấu nhất: `tim_kho` ×2 + `tra_ve_gio` + `thoi_tiet` + viết = 5; `parallel_tool_calls=False`);
  lượt không có công cụ ⇒ giữ 4 (giống byte). Test kịch bản: `tim_kho` ×2 + `tra_ve_gio` + `thoi_tiet` ⇒ vẫn ra lời.
- **Kiểm cuối (M-1)** — chỉ ở **lượt đã gọi `tra_ve_gio`**:
  - tập kiểm: số tiền (`so_tien.tim_so_tien`) + chuỗi **dạng giờ** (`\d{1,2}\s*(h|giờ|:)\s*\d{0,2}`) trong chữ model; **không** kiểm số đơn lẻ / năm;
  - tập cho phép: số trong các dòng đã gửi model ∪ số trong đoạn kho được trích ∪ số trong câu hỏi người dùng ("2 người lớn", "200 nghìn có đủ không");
  - vi phạm ⇒ **rút lại như thời tiết / lịch** (`citation_error` ⇒ sự kiện lỗi + "Thử lại", `assistant.py:469-470`, `chat.py:495-499`) — cùng một đường cho `/api/chat`, stream,
    #6; không thêm sự kiện "thay chữ" (giữ S5: chữ vẫn phát ngay). Khối điều kiện không hiện khi đã rút lại.
- **Có dòng bảng mà model từ chối (M-4):** chữ = `INSUFFICIENT_ANSWER` ⇒ code thay bằng câu dẫn cố định "Theo bảng vé / giờ trong nguồn dữ liệu:" + các dòng đã gửi model (dựng
  tất định) + khối điều kiện — khuôn thời tiết `CAU_DAN_DU_BAO` (`assistant.py:457-459`); stream: chữ từ chối đang được giữ lại ⇒ phát chữ thay qua `_chu_giu_lai` (`:1012-1018`).
  Chữ = `OUT_OF_SCOPE_ANSWER` ⇒ **không** nối khối, giữ nguyên câu. `chu_cua_model` bóc cả khối T3 (sau khối thời tiết) ⇒ cờ `refusal` + S3b đếm trên chữ model.
- **Log** (`chat_metrics.tools`): `tra_ve_gio` {n_diem, n_khop, n_khong_bang, co_dieu_kien, kiem, thay_tu_choi} — số / nhãn, không chữ.

## 2. Tiêu chí ghi trước (trước lượt có phí)

| Mã | Loại | Đo | Mức |
|---|---|---|---|
| Q1 | sàn (m-1) | `capture_all.py` | cờ tắt: 228 / 228 giống byte `main`; cờ bật: k / k câu **không** khớp regex giống byte — báo k và số câu Golden 176 / an toàn 32 / mẫu 30 được đưa công cụ |
| Q2 | quyết | bộ T3 ~20 câu đã thấy (vé từng điểm, nhiều điểm, giờ theo mùa / suất, điểm ngoài bảng, câu miễn giảm, câu chỉ hỏi giờ) | **một câu đạt (m-3)** = mọi số tiền / giờ trong chữ ∈ dòng nhãn của câu ∧ có ≥ 1 số của dòng nhãn ∧ không bị rút lại; câu điểm ngoài bảng đạt = có câu cố định; mỗi lượt tính riêng. Mức: **≥ n − 1 / n mỗi lượt ×2 và ≥ mốc `main`** (spec) |
| Q3 | sàn | mọi lượt (Q2 + S1) có dòng có điều kiện | có khối n / n (code đếm); **0** câu model tự nêu điều kiện: code gắn cờ chữ model có mẫu tuổi / chiều cao / nhóm miễn giảm **không** nằm trong nhãn hàng đã gửi ⇒ sub-agent trả có / không cho "chữ model có tự nêu điều kiện miễn / giảm ngoài khối code không" |
| — | sàn (M-3) | mọi lượt đo | `outcome = max_turns` = 0 |
| S1 | sàn | an toàn 32 (6 câu miễn giảm, 5 câu giờ) | 4 số so với lượt mốc `main` cùng ngày: đảo cảnh báo 0 · sai điều kiện **mới** 0 · thiếu cảnh báo **mới** 0 · ngoài kho bị trả lời 0 (S-AT khi chênh 1) |
| S3b | sàn | mọi lượt cả câu | 0 câu về Huế ra `OUT_OF_SCOPE_ANSWER` (code đếm trên `chu_cua_model`) |
| S4 | sàn | mẫu Golden 30, biến thể + mốc cùng lượt chấm mù | không tụt quá nhiễu |
| S5 | sàn | `chat_metrics` lượt Q2 (stream) | chữ đầu p95 ≤ 5 s (spec §12.3) |
| S6 | sàn + báo (m-4) | `chat_metrics.usd` | mẫu Golden 30 trung bình ≤ 0,0005 USD / câu (spec); lượt có `tra_ve_gio` thêm một vòng model ⇒ báo USD / câu riêng (không là sàn: spec §12.3 S6 áp câu Huế thường) |

Âm (Q1 / Q3 / max_turns / S1 / S3b / S4 / S5 trượt, hoặc Q2 dưới mức) ⇒ cờ tắt, ghi kết quả; **phương án B** (spec): bảng chỉ dùng cho kiểm cuối (không công cụ) — sai ⇒
câu cố định "giá / giờ có thể khác — xem nguồn". Không vòng chỉnh thứ ba.

## 3. Bộ đo, lượt chạy, tiền (M-6)

Bộ T3 ~20 câu (không kín — số do code kiểm, spec §12.4) viết **sau** khi User duyệt bảng; nhãn = id dòng bảng ghi trước khi chạy. Trước có phí: test 0 USD (parser bảng thật,
khớp tên + bí danh, điểm ngoài bảng, trường đi đâu — điểm có dòng miễn cho trẻ nhỏ ⇒ chuỗi gửi model không chứa chuỗi điều kiện, khối đủ nguyên văn —, kiểm cuối có ca cố
tình vi phạm trên **cả 3 đường**, câu từ chối ×2 loại, chuỗi `max_turns`, regex, Q1).

| Lượt | Bộ | Nhánh | Số lượt | USD (ước: biến thể có công cụ 0,0008 · `main` 0,0005) |
|---|---|---|---|---|
| pilot | 3 câu T3 | biến thể | ×1 | 0,003 ⇒ ước lại cả bảng |
| Q2 | T3 20 | `main` ×1 + biến thể ×2 | 60 | 0,010 + 0,032 = 0,042 |
| S1 | an toàn 32 | `main` ×1 + biến thể ×2 | 96 | 0,016 + 0,045 = 0,061 |
| S4 | mẫu Golden 30 | `main` + biến thể cùng lượt | 60 | 0,015 + 0,021 = 0,036 |
| **Tổng** | | | | **≈ 0,14 USD** · dừng ở **0,20** (trong ≈ 1,1 còn lại của bản 13); ước sau pilot vượt 0,20 ⇒ nhắn A trước |

Tính vào Phase 9 (trần 3,5, quỹ B7 0,35 giữ riêng).
