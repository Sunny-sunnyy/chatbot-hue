# Implementation Report: Phase 9 B5 v2 — E19 câu lịch trình tự nhiên (phần 1–3)

Người làm: E (Claude Code, Claude Opus 5.5)
Date: 06/11/2026 (viết 11:01 06/11/2026 theo `date`)
Việc: `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN 06/11", dòng E — E19.

## 1. Phạm vi

- **Đã giao:**
  - (1) thử Huế TRIPO vòng 4 bằng Playwright, phần chưa thử;
  - (2) nghiên cứu cách người thật hỏi lịch trình Huế từ nguồn công khai;
  - (3) viết câu mẫu tự nhiên + bảng loại ràng buộc ⇒ A đưa User duyệt;
  - (4) sau khi User duyệt: viết bộ kín 5 câu.
- **Đã làm:** (1)–(3). **(4) chưa làm** — chờ User duyệt câu mẫu.
- Không sửa code. 0 USD.

## 2. Thay đổi chính (toàn bộ ở `data/` — private, không commit)

| File | Nội dung |
|---|---|
| `data/nghien_cuu_tinh_nang_2026-11-06/tripo_v4/tripo_v4.md` | Báo cáo TRIPO vòng 4: đủ lựa chọn của biểu mẫu "Lên kế hoạch" (kể cả "Tùy chọn thêm"), 3 tab Lưu trú / Ăn uống / Dịch vụ, bộ lọc Điểm tham quan, bản đồ (lớp, xe, bán kính), 1 lần gửi biểu mẫu đủ trường |
| `…/tripo_v4/tools/` | `recon_form.py`, `thu_bam.py`, `tom_tat_form.py` + JSON thô; ảnh `…/tripo_v4/anh/` (21 ảnh, 17 MB) |
| `data/nghien_cuu_tinh_nang_2026-11-06/yeu_cau/` | 2 yêu cầu tra web (chỉ thông tin công khai) |
| `data/tra_cuu_cli/2026-11-06_e19-cach-hoi-lich-trinh/`, `…_e19-cach-hoi-tieng-viet/` | Kết quả Codex |
| `data/phase_9/b5_v2/mau_cau_tu_nhien.md` | **File cần User duyệt:** người thật ↔ câu máy, bảng 15 loại ràng buộc (người thật nói kiểu gì · tần suất · TRIPO có trường không · B5 hiện có · cần đo gì), 8 câu mẫu, đề xuất cách viết bộ kín, 3 câu hỏi |

## 3. Cách đã chạy thật

- TRIPO (từ gốc repo, 10:50–10:57 06/11/2026):
  - `timeout 400 uv run python data/nghien_cuu_tinh_nang_2026-11-06/tripo_v4/tools/recon_form.py`
  - `timeout 300 uv run python …/thu_bam.py a b`
  - `timeout 600 uv run python …/thu_bam.py c`
  - Playwright 1.58, chromium headless, một trình duyệt, `permissions=[]`, không đăng nhập.
  - Gửi tới máy chủ lập lịch: 1 lần Enter trên biểu mẫu + 1 lần "Xác nhận phương án". Không gõ chữ tự do.
- Tra web:
  - `scripts/tra_web_codex.sh <yêu cầu> e19-cach-hoi-lich-trinh` (6 trang mở thật, 1 bài tiếng Việt);
  - `… e19-cach-hoi-tieng-viet` (7 trang mở thật, 20 lượt hỏi tiếng Việt, 0 lệnh shell).
  - E tự WebFetch kiểm 3 chủ đề diễn đàn chính ⇒ khớp báo cáo Codex (ngày, ràng buộc, cụm viết tắt).
- Dò số ngày (0 USD, hàm thuần): `cd backend && HF_HUB_OFFLINE=1 uv run python -c "from llm.do_so import do_so_ngay; …"` với 11 cách nói số ngày.

## 4. Kết quả quan sát

**Người thật hỏi khác câu máy** (20 lượt tiếng Việt, mẫu tiện dụng, gần như chỉ một diễn đàn):
- kể hoàn cảnh trước rồi mới xin;
- ràng buộc rải trong câu, có chỗ mơ hồ;
- hay kèm thứ không phải trường lịch (xe gì, mấy giờ tới, ở đâu);
- nhiều câu hỏi trong một lượt; có ý ghét / né;
- viết tắt số ngày và khẩu ngữ;
- câu hỏi phụ ở lượt sau rất ngắn; có người đưa lịch nháp xin góp ý.

Ràng buộc hay gặp nhất: số ngày (12 / 20), phương tiện (9 / 20). Hiếm: thời tiết (1 / 20).

**TRIPO vòng 4:**
- Biểu mẫu đủ trường ⇒ máy chủ không gọi mô hình hiểu câu, không hỏi thêm; dùng đúng ngày / giờ / số người.
- Ô nhập tự sinh câu liệt kê nhãn — đúng kiểu "câu máy" User chê.
- Lỗi thấy trên chính trang, so với dữ liệu TRIPO tự ghi:
  - 2 điểm xếp quá giờ đóng cửa (vòng 1 cũng gặp);
  - vé trẻ em tính bằng giá người lớn;
  - lựa chọn "không muốn đi bộ nhiều" không thấy đổi lịch.

**Dò số ngày của B5** (`backend/llm/do_so.py`):
- Không dò được: "4n3d" (chữ d không dấu), "2 hôm", "cuối tuần", "đi trong ngày", "ở 2 đêm", "3n2đ hay 4n3đ" (nước đôi — đúng thiết kế).
- Khi code không dò được thì dùng số do model trích (`lich_trinh.py:123-132`), nên đây **chưa phải lỗi** — chỉ là chỗ dựa vào model. Ghi để B171 / đo sau biết.

## 5. Lỗi và giới hạn

- **Nguồn người thật hẹp:**
  - gần như chỉ một diễn đàn (giọng trẻ, "các bác / em");
  - không tìm được câu dùng được ở diễn đàn phụ huynh, bình luận báo, mạng xã hội đóng;
  - 6 bài tiếng Anh chỉ để tham khảo.
  - ⇒ Giọng phụ huynh / người lớn tuổi trong câu mẫu là **E đoán**, chưa có nguồn.
- Câu không dấu ngoài phạm vi (User 25/10) ⇒ câu mẫu đều có dấu, dù người thật đôi khi gõ thiếu dấu.
- TRIPO: một lần chạy mỗi phần, không kiểm dữ kiện với nguồn chính thức.
  - Bộ lọc "Giáo dục – bảo tàng" trả cả điểm thiên nhiên — chưa rõ do nhãn gắn rộng hay do mã lọc; chưa kiểm thêm.
- Phần (4) bộ kín: NOT RUN (chờ User).

## 6. Bàn giao cho người kiểm

- A đọc `data/phase_9/b5_v2/mau_cau_tu_nhien.md` §1–§3 rồi đưa User duyệt:
  - giọng 8 câu mẫu;
  - có câu hai lượt không;
  - có giữ phần ngoài lịch trong câu không.
- B / C **không** đọc `data/phase_9/b5_v2/` (theo việc giao).
- Bảng ràng buộc §2 nêu chỗ B5 chưa có trường: ngân sách, giờ tới / về, phương tiện, chỗ ở, "né", mưa, ghép nơi khác. Đây là **đầu vào để đo, không phải đề xuất sửa code** — chatbot cần nói thật phần không làm được.
- Không commit / push.
