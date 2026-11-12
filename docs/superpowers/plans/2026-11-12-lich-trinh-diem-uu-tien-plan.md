# Plan (mức nhẹ) — lịch trình: cột "ưu tiên" trong bảng điểm + chọn điểm ưu tiên trước · **NHÁP — chờ User duyệt phiếu điểm ưu tiên**

Người viết: C, 20:50 12/11/2026 (`date`), A giao. Chưa code, chưa đổi bảng, 0 USD. Repo public: tên điểm cụ thể + danh sách đề xuất nằm ở phiếu private.

## Căn cứ để review

- Lượt đếm: `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` mục 3 (mô phỏng 360 tổ hợp + 14 lịch thật).
- Code: `backend/llm/lich_trinh.py` — `nap_bang` (nạp + kiểm bảng), `xep` (chọn theo thứ tự `bang.diem`), `_cum_hop` (≤ 2 cụm / ngày, cụm kề), `kiem_khung`, `kiem_cuoi`.
- Bảng đang chạy: `data/phase_9/lich_trinh/diem_v3.json` (sha256 `e94b7f4263f2`, User duyệt); phiếu cho User: `data/phase_9/lich_trinh/phieu_diem_uu_tien.md` (private).
- Bộ quyết biểu mẫu 12 tổ hợp + công cụ: `data/phase_9/cong_dot_1/` (`to_hop_chinh_thuc.jsonl`, `tools/do_bieu_mau.py`).

## 1. Lỗi đã đếm

Hàm `xep` chọn điểm tham lam theo **thứ tự dòng của bảng**; bảng xếp theo cụm địa lý; mỗi buổi một điểm ⇒ trên 360 tổ hợp biểu mẫu: **7 / 28 điểm không bao giờ được xếp**, gồm
ngôi chùa nổi tiếng nhất và hai lăng lớn; trong 120 tổ hợp "thích di tích / không chọn": các điểm đó 0 / 120. 14 lịch thật: 0 lịch di tích có chùa hay lăng lớn.

## 2. Việc đề xuất

- **Dữ liệu:** bảng v8 = v3 + cột `uu_tien` (1 · 2 · trống) cho các điểm User tick ở phiếu (đề xuất 5 điểm mức 1 + 4 điểm mức 2). Không đổi trường nào khác.
- **Code (một chỗ):** `nap_bang` sắp `bang.diem` theo (`uu_tien` 1 ⇒ 2 ⇒ trống, rồi thứ tự dòng cũ) và kiểm giá trị cột. **`xep` không sửa** — nó vẫn đi theo thứ tự `bang.diem`,
  nên mọi luật cũ (cụm kề, nhóm hạn chế, cụm xa từ 3 ngày, buổi tối, lấp di tích có ghi chú) giữ nguyên.
- **Cấu hình:** `settings.yaml` `lich_trinh_bang` trỏ bảng v8 (bảng v3 giữ để lùi). Không cờ mới: lùi = trỏ lại v3.
- **Lời dặn / chuỗi gửi model:** không đổi lời dặn; chuỗi gửi model của lượt biểu mẫu đổi **chỉ vì khung khác** (điểm khác). Lượt không có lịch: giống byte.
- Nếu User chọn phương án (b) ở câu 1 của phiếu ("mọi sở thích đều có một điểm mức 1") ⇒ đó là **thêm một luật vào `xep`**, không còn là đổi thứ tự ⇒ ghi thêm tiêu chí + test, vẫn mức nhẹ.

**Đã thử trước [Chạy 12/11, 0 USD — đổi thứ tự bảng trong bộ nhớ, code không đổi]:** với danh sách đề xuất, trên 360 tổ hợp: lỗi `kiem_khung` 0 · ngày có hai điểm không cùng /
kề cụm 0 · nhóm hạn chế có buổi tối 0. Trong 30 tổ hợp "di tích / không chọn" mỗi mức số ngày — chùa nổi tiếng: 15 / 30 (1 ngày), 30 / 30 (từ 2 ngày); lăng thứ nhất: 15 / 30 (2 ngày),
30 / 30 (từ 3 ngày); lăng thứ hai: 15 / 30 (2–3 ngày), 30 / 30 (4 ngày); lăng xa: 15 / 30 (từ 3 ngày). Số tổ hợp phải lấp ngoài sở thích không đổi (150). Mặt trái: số điểm không bao giờ
được xếp **không giảm** (7 ⇒ 9, đổi sang các điểm ít tên tuổi hơn) vì mỗi buổi vẫn một điểm.

## 3. Tiêu chí ghi trước

| | Mức | Đo bằng |
|---|---|---|
| **Quyết (0 USD)** — trên tổ hợp "thích di tích / không chọn" | không kém bản thử trước ở mục 2: lịch từ 2 ngày **100 %** có ngôi chùa đó; từ 3 ngày **100 %** có lăng thứ nhất; lịch 4 ngày **100 %** có lăng thứ hai; **mọi** điểm mức 1 có mặt ở **≥ 50 %** tổ hợp từ 3 ngày (danh sách User đổi ⇒ chạy lại bản thử, ghi số mới vào đây **trước** khi sửa code) | mô phỏng 360 tổ hợp (script chỉ đọc, < 5 giây) |
| Không điểm ưu tiên nào bị bỏ rơi | **0** điểm mức 1 / mức 2 "không bao giờ được xếp" trên cả 360 tổ hợp | như trên |
| Luật cũ giữ nguyên | `kiem_khung` 0 lỗi / 360 · 0 ngày có hai điểm không cùng / kề cụm · nhóm hạn chế 0 buổi tối · cụm xa chỉ ở lịch từ 3 ngày | như trên |
| Sở thích khác không bị đổi (nếu User chọn phương án (a)) | khung của 240 tổ hợp "thiên nhiên / ẩm thực / chụp ảnh / lễ hội" **giống hệt** bảng v3, trừ phần lấp di tích | so khung v3 ↔ v8 |
| Đi lại không xa hơn | số ngày dùng 2 cụm không tăng quá **+ 15 điểm phần trăm** so với v3 (v3: 546 / 900 ngày; thử trước: 657 / 900 = + 12) và 0 ngày ghép hai cụm không kề | mô phỏng |
| Lịch thật | 14 yêu cầu của lượt 12/11 chạy lại 1 lượt: 14 / 14 qua kiểm cuối, 0 rút, 0 từ chối; lịch di tích từ 2 ngày có điểm mức 1 đúng như khung | server thật, `gui_cau.py` |
| Bộ quyết biểu mẫu | 12 tổ hợp ×2: sàn code 24 / 24; hai người chấm độc lập ≥ 11 / 12 mỗi lượt (như 07/11) | `do_bieu_mau.py` |
| Test | `nap_bang`: sắp đúng theo `uu_tien`, giá trị lạ ⇒ lỗi rõ; bảng không có cột ⇒ thứ tự cũ (bảng v3 vẫn nạp được); 2–3 ca khung cố định | pytest file lịch trình (file chạm) |

Phạm một sàn ⇒ trỏ lại bảng v3, ghi kết quả âm.

## 4. Rủi ro

- **Dồn điểm ưu tiên làm ngày đi xa hơn** (chùa ở tây bắc, lăng ở tây nam): chặn bằng luật cụm kề đang có + tiêu chí "số ngày 2 cụm". Thử trước: + 12 điểm phần trăm, 0 ngày nhảy cụm.
- **Điểm ít tên tuổi biến mất khỏi lịch** (9 điểm không bao giờ được xếp sau khi đổi) — chấp nhận ở việc này; chữa bằng việc 2 dưới.
- **Lịch 1 ngày "không chọn sở thích"**: buổi chiều đang dành cho một điểm thiên nhiên (luật mặc định cũ) ⇒ điểm mức 1 thứ hai chỉ vào được 15 / 30 tổ hợp 1 ngày — đúng luật cũ, ghi rõ; câu 2 của phiếu hỏi User.
- Bảng là dữ liệu User duyệt ⇒ v8 chỉ có hiệu lực sau khi User tick phiếu; C không tự chọn danh sách.

## 5. Việc 2 (thời lượng + "đi dày") — ghép chung đợt được không?

**Ghép được, nếu User duyệt phiếu thời lượng v7 cùng lúc** — cả hai việc cùng chạm bảng và cùng đo bằng mô phỏng 360 tổ hợp, nhưng **đo tách hai bước** (đổi một thứ một lần):
1. Bước A = việc này (bảng v8: cột ưu tiên) ⇒ đo ⇒ giữ / gỡ.
2. Bước B = thêm thời lượng từ phiếu v7 vào bảng (v9) + nới luật "đi dày" trong `xep` (hai điểm ngắn cùng cụm / cụm kề trong một buổi) ⇒ đo: "đi dày" đổi khung ở ≥ một nửa số nhóm
   (hôm nay 0 / 120); số điểm không bao giờ được xếp giảm (mục tiêu ≤ 3, mỗi điểm còn lại có lý do ghi rõ); nhóm hạn chế không đổi. Bước B sửa `xep` ⇒ thêm test + một review riêng phần luật.
Không có phiếu v7 ⇒ chỉ làm bước A; "đi dày" tiếp tục ẩn trên biểu mẫu.

## 6. Tiền · giờ · file chạm

- **Tiền ≤ 0,03 USD:** 14 lịch thật ≈ 0,006 · bộ quyết 12 ×2 ≈ 0,012 · cổng ổn định ≈ 0,002. Mô phỏng: 0 USD. (Bước B nếu ghép: + ≤ 0,03.)
- **Giờ:** ~2–3 giờ agent cho bước A (bảng v8 + 1 chỗ code + test 40 phút · mô phỏng + đo 40 phút · report + một review cả nhánh). Bước B: + ~3 giờ.
- **Chạm:** `data/phase_9/lich_trinh/diem_v8.json` (mới, private) · `backend/llm/lich_trinh.py` (`nap_bang`) · `backend/config/settings.yaml` (đường dẫn bảng) · test lịch trình · allow-list đóng gói Docker (tên file bảng) · bài học 14 + bảng tổng bài 19 khi xong.

## 7. Cần User

Tick phiếu `data/phase_9/lich_trinh/phieu_diem_uu_tien.md` (danh sách + 3 câu). Muốn ghép việc 2: duyệt thêm phiếu thời lượng v7.
