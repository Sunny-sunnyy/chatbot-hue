# Review nhánh `p9-web-so-cau-hoi` @ `664d4ff` — C · 17:58 14/11/2026

**Kết luận: `changes_requested`** — 0 blocker · 1 major · 1 minor. 0 USD (không gọi model / Serper / Qdrant).

## Cổng tối thiểu
- Diff: `tra_web.py` (tham số `cau_hoi`, trừ chuỗi số câu hỏi khỏi luật `so_ngoai_trich`), `assistant.py:1045` (`cau_hoi=query`), 1 test, report. Không ngoài phạm vi. `git diff --check` sạch.
- Đường truyền: `cong_web(query, …)` nhận `query` từ hai chỗ gọi (`assistant.py:1063`, `:1089`) — là câu người dùng gửi, không phải câu đã nối "chỉ viết cho phần…" ⇒ đúng như report.
- Luật tiền `tien_ngoai_trich` không đổi; nhánh thời gian thực không đổi ⇒ đúng.
- [Chạy] `tests/test_b6_tra_web.py`: 100 passed (worktree cần `data/` + `knowledge-base-hue/` trỏ tạm — 7 test đường thật đọc build record; không có thì 7 error môi trường).
- Chuỗi gửi model không đổi ⇒ không cần lượt có phí: đồng ý.

## M-1 (major) — nới rộng hơn nhu cầu đã đo; mở đường "nói chắc sai"
- **Bằng chứng [Chạy]** (`/tmp/c_photon/dem_web.py`, `dem_web2.py` trên 76 mục `data/web_suy_luan_2026-11-14/`): 11 mục nhánh cứu được thì **cả 11** chỉ nhờ chuỗi số dạng năm (2026 ×7, 2027 ×4). Phương án hẹp "chỉ năm 19xx / 20xx đứng riêng trong câu hỏi" cho **cùng kết quả**: bị thay 21 ⇒ 10 (nhánh: 21 ⇒ 10).
- **Tác động:** nhánh miễn MỌI chuỗi số trong câu hỏi — ngày, giờ, số nhà, số điện thoại. Người dùng hỏi kèm tiền đề sai (giờ / ngày) ⇒ model nhắc lại số đó như sự thật trong mục web ⇒ phép kiểm không còn chặn. Đây là lỗi thứ hạng 2 ("nói chắc sai") trong thứ tự lỗi User chốt; lợi ích đo được không cần nới phần đó.
- **Tiêu chí đóng:** chỉ trừ năm: vd `nam = {x for x in re.findall(r"(?<!\d)(?:19|20)\d\d(?!\d)", cau_hoi)}` thay cho `_chuoi_so(cau_hoi)`; sửa test: (a) năm trong câu hỏi qua; (b) giờ / ngày người dùng gõ mà đoạn trích không có ⇒ vẫn `so_ngoai_trich`; đếm lại 76 mục = 10.
- Lưu ý: `_chuoi_so("6/2026")` = `"62026"` (một chuỗi) ⇒ test hiện có "tháng 6/2026" sẽ đổi kết quả với phương án hẹp; dữ liệu thật không có dạng này trong 11 ca cứu.

## m-1 (minor)
- Report mục Rủi ro ghi rủi ro nhưng không ghi vì sao chấp nhận ⇒ sau khi sửa M-1, viết lại: "chỉ năm; giờ / ngày / số nhà vẫn phải có trong đoạn trích".

## Vòng 2 — kiểm phần sửa @ `f919b95` (C · 18:00 14/11/2026)
**Kết luận: `ready_for_user_confirmation`** — M-1 + m-1 đóng, 0 finding mới.
- `_NAM = (?<!\d)(?:19|20)\d\d(?!\d)` chỉ lấy năm đứng riêng từ câu hỏi; phần còn lại so như main. Đọc ca biên: "19:30" (có dấu hai chấm) không khớp; số điện thoại / dãy dài không khớp nhờ hai phía `\d`; câu hỏi "6/2026" cho "2026" nhưng model viết "6/2026" thành chuỗi `62026` ⇒ vẫn chặn (phía an toàn).
- Test thêm "mở 19:30" người dùng gõ ⇒ vẫn `so_ngoai_trich`; tiền vẫn `tien_ngoai_trich`.
- [Chạy] `tests/test_b6_tra_web.py` 100 passed; đếm lại 76 mục bằng code nhánh: bị thay 21 ⇒ 10 (khớp report). `git diff --check` sạch. Report mục Rủi ro đã viết lại.
