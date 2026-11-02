# Implementation Report: Phase 9 — bộ đo B1 + mẫu Golden cố định (C123)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-cc`)
Date: 18:44 02/11/2026 (`date`)
Căn cứ: spec Phase 9 bản 9 `169c2dd5f86a` §4 (bảng "Bộ đo", hồi quy B3–B6), §5 B1; mục C123 trong `session_prompt/CURRENT_HANDOFF.md`.

## 1. Phạm vi

Việc giao gồm: bộ tuyến (~40 câu đã thấy, phần kín, 5 ca lái tuyến), bộ ngày (dùng lại 15 câu cũ, thêm 10 câu mới), bộ khẩn cấp, và mẫu Golden ~30 câu (6 câu / loại × 5 loại, seed ghi trước).
Việc này 0 USD. C không chạy chatbot và không code B1.

Đã làm: tất cả. Phần kín của bộ khẩn cấp lúc đầu hoãn, vì spec §4 ghi "10 / —" còn handoff ghi "+ phần kín". C đã hỏi A; A trả lời: cần, vì B1 có luật code. Phần này đã viết, xem §5b.

## 2. Thay đổi chính

Chỉ thêm file private ở `data/phase_9/bo_do_b1/`; mục lục, số câu và sha ở `README.md` trong thư mục đó. Không đổi code, kho hay Golden.

| Bộ | Đã thấy | Kín | Ghi chú |
|---|---:|---:|---|
| tuyến | 40 | 20 | Huế / trò chuyện / ngoài phạm vi / khẩn cấp = 20 / 8 / 8 / 4 (đã thấy) và 10 / 4 / 4 / 2 (kín); luật gán nhãn ghi **trước** khi viết câu |
| ca lái tuyến | 5 | — | 5 kiểu: đòi coi là trò chuyện · chèn nhãn tuyến giả · phủ nhận chủ đề · đòi đóng vai cho việc ngoài phạm vi · giả khẩn cấp |
| ngày | 15 cũ + 3 mới | 7 mới | câu mới: ngày trong tuần, cuối tuần, ngày làm việc, âm lịch, dương lịch; 2 câu đối chứng có ngày rõ |
| khẩn cấp | 10 (= C122) | 16 (8 khẩn cấp + 8 câu thường dễ nhầm) | §5b |
| mẫu Golden cố định | — | — | 30 `case_index`, 6 / loại |

**Luật gán nhãn tuyến** (`luat_gan_nhan_tuyen.md`): có 7 luật phân xử, luật trước thắng. Chính:
- đang gặp nguy ⇒ khẩn cấp;
- câu lẫn lộn chào + hỏi thông tin Huế ⇒ trợ lý Huế;
- câu có Huế + nơi khác ⇒ trợ lý Huế; câu chỉ nói nơi khác ⇒ ngoài phạm vi;
- chữ người dùng đòi đổi tuyến **không** đổi nhãn;
- câu mơ hồ có thêm danh sách `chap_nhan` (các nhãn khác cũng tính đúng).

Hai sàn của B1 viết thành cách chấm cụ thể trong file.

**Mẫu Golden:** luật ghi trước ở `session_prompt/sessions/STATUS_C.md` (mục C123):
- Golden md5 `6331e88fb171`; `random.Random(20261102)`;
- lấy lần lượt từng loại theo thứ tự `direct_fact, multi_source, conditional, comparative, out_of_scope`, mỗi loại `sample(…, 6)`;
- không lọc theo độ tự nhiên, không chọn lại;
- kết quả: danh sách 30 `case_index` có md5 `66c389f25270`.

## 3. Cách đã chạy thật

```bash
uv run python data/phase_9/bo_do_b1/tools/chon_mau_golden.py   # in 30 case_index + md5, không in câu
```

Dòng kho cho câu ngày mới tìm bằng `scripts/grep_kb.sh` (mẫu thứ trong tuần / cuối tuần / âm lịch), rồi mở đúng file / dòng để ghi đáp án và `kho_ref`. Số dòng đã kiểm lại; một chỗ lệch 1 dòng đã sửa trước khi ghi sha.

## 4. Kết quả quan sát

- Có đủ các file ở §2. Số câu theo nhãn đếm bằng script từ chính file (khớp bảng).
- Bộ tuyến viết không nhìn kho, vì nhãn tuyến không phụ thuộc kho. Bộ ngày mới có đáp án mong đợi và nhãn lỗi L1 / L2 theo cách chấm cũ (C93).

## 5. Lỗi và giới hạn

- Một người (C) viết và gán nhãn mọi câu. Chưa có người thứ hai gán nhãn độc lập. User đọc mẫu 10 câu tuyến (`mau_cho_user.md`), đúng như spec ghi.
- Câu ngày mới phụ thuộc ngày chạy. Câu N6 ghi đáp án theo ngày chạy 11–12/2026; chạy sau thời gian đó thì phải xem lại.
- Câu âm lịch: C **không** tự quy đổi âm ↔ dương. Nếu model quy đổi thì judge cần đối chiếu lịch Việt Nam công khai (chưa chuẩn bị).
- Mẫu Golden có thể gồm câu không tự nhiên (spec không ghi lọc). Mẫu này chỉ dùng cho sàn F1–F4 rút gọn, không dùng cho chỉ số quyết.

## 5b. Thêm — phần kín bộ khẩn cấp (C125, 19:07 02/11/2026)

Sau C122, User chốt "chỉ từ chối = lỗi, sửa gọn", nên B1 sẽ có luật code khẩn cấp. A giao thêm phần kín để luật không chỉ khớp riêng 10 câu đã thấy.

- `data/phase_9/bo_do_b1/khan_cap_sealed.jsonl` sha `15a41db0c741`, 16 câu:
  - 8 câu khẩn cấp, khác loại hoặc khác cách gõ so với 10 câu cũ (viết hoa, câu cụt, kể sự việc không hỏi, trộn tiếng Anh);
  - 8 câu thường dễ bị nhận nhầm: từ ngữ khẩn cấp dùng theo nghĩa bóng, hỏi lịch sử, hỏi phòng trước, nói quá.
- B (người code luật) **không mở**. 0 USD.
- Giới hạn: vẫn một người viết (C); 8 câu là cỡ nhỏ, chỉ bắt được luật khớp quá hẹp hoặc chặn quá rộng ở mức thô.

## 6. Bàn giao cho người kiểm

- Đọc `data/phase_9/bo_do_b1/README.md`, rồi `luat_gan_nhan_tuyen.md`. Phần đã thấy được đọc tự do. Phần `*sealed*` chỉ người được giao mới mở.
- Chạy lại mẫu Golden: lệnh ở §3. Kết quả phải ra đúng md5 `66c389f25270`.
- C không commit.
