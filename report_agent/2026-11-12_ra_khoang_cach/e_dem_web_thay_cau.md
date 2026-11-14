# Đếm lại: mục web bị thay câu cố định sau khi so tiền theo giá trị · E · 17:51 14/11/2026

0 USD. Không gọi model, Serper hay Qdrant; không chạy server.

## Kết luận
- Trên cùng 76 mục web đã lưu (19 câu, mỗi câu 4 lần viết), phép kiểm hiện tại của main thay **21 / 76 = 27,6 %** mục bằng câu cố định. Trước khi so tiền theo giá trị là **33 / 76 = 43,4 %** (đây là con số "~45 %" ghi trong handoff).
  4 mục khác (5,3 %) ra "chưa xác minh" vì câu hỏi thời gian thực có số, đúng luật.
- **16 / 21 mục còn bị thay là chặn nhầm.** Cả 16 mục bị chặn vì một **con số năm có sẵn trong câu hỏi của người dùng**.
  - Loại câu: hỏi kèm một mốc thời gian sắp tới (một tháng hoặc dịp lễ có ghi năm).
  - Model chỉ nhắc lại năm đó trong câu thận trọng "chưa xác minh được … <năm>".
  - Luật `so_ngoai_trich` (`backend/llm/tra_web.py:236`) đòi mọi chuỗi số trong mục web phải có trong đoạn trích. Luật này không xét câu hỏi.
  - 4 câu loại này bị chặn đủ 4 / 4 lần viết.
- 5 mục còn lại bị thay đúng hoặc cần xem riêng:
  - 4 mục `tien_ngoai_trich`, cùng một câu: số tiền không có trong đoạn trích ⇒ chặn đúng.
  - 1 mục: số "39" không có trong đoạn trích, model tự thêm ⇒ chặn đúng.
- Hai mức suy luận ra như nhau (mặc định 11 ↔ low 10 mục bị thay), nên lỗi ở luật kiểm chứ không ở model.

## Có đáng làm tiếp không — đề xuất, chưa làm
- **Đáng làm, nhỏ:** cho phép những chuỗi số **có trong câu hỏi** qua luật `so_ngoai_trich`. **Không** nới luật tiền: `tien_ngoai_trich` vẫn so với đoạn trích, để người dùng gõ sai giá thì model không "xác nhận" được giá đó.
  - Trên 76 mục: dự kiến 16 mục chặn nhầm sẽ ra mục web (21 ⇒ 5).
  - Ước tốn 0 USD, ~30 phút: 1 dòng code + 2 test (năm trong câu hỏi qua; số tự thêm vẫn chặn).
  - Đường đổi chỉ là phép kiểm sau khi model viết, không đổi chuỗi gửi model ⇒ theo luật hiện hành chỉ cần test giống byte, không cần lượt có phí.
- **Rủi ro cần cân:** câu hỏi chứa một số sai mà model lặp lại như sự thật.
  - Với năm hay tháng, model chỉ dùng số đó để nói "chưa xác minh", nên rủi ro thấp.
  - Muốn chặt hơn thì chỉ cho qua chuỗi số dạng năm hoặc ngày tháng lấy từ câu hỏi.
- **Giới hạn mẫu:** 76 mục chỉ đến từ 19 câu, trong đó nhiều câu "hỏi kèm" do B đặt ra để đo. Log thật của server sau lúc merge (16:31) chỉ có 7 dòng có mục web, cả 7 đều ra mục ⇒ quá ít để tính tỉ lệ trên người dùng thật. Các lượt đo trong worktree `/tmp` ghi log riêng, không có trong `backend/logs/application.log`.

## Tính lại
```
cd backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/dem_web_thay_cau_2026-11-14/dem.py        # số đếm
cd backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/dem_web_thay_cau_2026-11-14/dem.py --so   # chuỗi số bị coi là ngoài trích, từng mục
```
Đầu vào: `data/web_suy_luan_2026-11-14/buoc1.jsonl` (đoạn trích + cờ) và `buoc2.jsonl` (76 mục model đã viết), đều private. Mốc 43 ⇒ 51 lấy từ `b_tien_web_chuan_hoa_implementation.md`.
