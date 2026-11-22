# STATUS A — ghi đè 21:35 22/11/2026 (giờ `date`; MỞ PHIÊN ĐÊM 22/11 — năm phiên mở lại 21:26 sau khi máy khởi động lại 21:25; ngày 23/11 chủ dự án TỰ TEST trong lúc nhóm làm). Vai: phiên điều phối. Terminal: điều phối `hue-rag-ea` · B `hue-rag-f3` · C `hue-rag-72` · D `hue-rag-62` · phiên đo E `hue-rag-74` — phiên mở lại có tên khác, dò bằng danh sách phiên

Việc đang mở, ai làm, bước kế: sổ việc `session_prompt/VIEC_DANG_MO.md` khối A — gạch ĐẦU "PHIÊN ĐÊM 22/11" (bảng sáu việc). Quyết định của chủ dự án: `session_prompt/HIEN_TRANG.md` mục 4. Trang này chỉ ghi phần riêng của phiên điều phối.

## Hệ thống lúc ghi
Main `9b45acda` + các commit sổ của đêm 22/11 (code không đổi từ `950bb55`): 48 tính năng mở, kho 267 bài / 9.479 điểm, giao diện CŨ (`frontend/dist` cây chính dựng 17:34 22/11) — bản chủ dự án tự test 23/11; bật bằng `HUE_SO_VET=true scripts/bat_he_thong.sh`. Cả bộ test mới nhất: 20:48–21:07 22/11, 78 file chạy đều thoát 0, 4 bỏ, 2.197 ca. Qdrant BẬT (bật lại 21:29 sau khi máy khởi động lại); cổng 8010 trống. Giao diện MỚI chưa gộp: ứng viên `origin/p13-c-chua-bai` `551d02f`, đang chữa trên nhánh con (C `p13-c-man-dau-cao`, B một nhánh con cho `lkh.css`).

## Đã làm từ lúc mở phiên
1. Tin mở phiên + giao việc cho bốn phiên trong MỘT tin (không ai phải chờ); cả bốn đã báo vai và đang làm.
2. Tự mở ảnh xác nhận điểm nặng nhất của ba file so cặp: cảnh A01 ở 390 px (ô nhập bị thanh dưới che nửa) ⇒ đã chuyển C.
3. Đọc phần kết luận, chín ca giao nhau và 15 đề xuất của bản nghiên cứu harness (GPT-6.2 Sol, về 21:20); tự đọc code điểm đứng đầu (A1): có thật, cỡ một nháy ⇒ đã chuyển B kèm thứ tự A1 / A2 · A5 · A6 · A8 · đề xuất 4, 2, 7.
4. Đồng ý cỡ thứ tư 1536 × 695 theo phép đọc màn hình máy demo của phiên đo; đã báo C, B và ghi điều kiện gộp.
5. Sổ: khối A viết gọn (phần đã xong dời nguyên văn sang `report_agent/2026-11-22/TONG_HOP.md`), ba dòng ở `VIEC_DA_XONG.md`, `HIEN_TRANG.md` sửa bốn chỗ cũ + mục 3 thêm ba câu gác, `CURRENT_HANDOFF.md` một dòng mở phiên.

## Việc kế của phiên điều phối, theo thứ tự
1. Nhận kết quả ca đối chứng của phiên đo (phép kiểm màn đầu phải ra "KHÔNG TRỌN" trên `551d02f` ở 1280 × 620); nhận "máy trả" của B (cổng 8033) và phiên đo (cổng 8012).
2. Khi C + B báo MỘT sha: tự mở ảnh màn đầu ở 1536 × 695 và 1280 × 620 + cảnh A01 ở 390 ⇒ phiên đo chạy cổng gộp ⇒ gộp vào main ⇒ phiên đo: cả bộ test + dựng `dist` + nhìn ba màn ⇒ báo chủ dự án "chạy lại lệnh bật" + phiếu bốn ý cho D. Lộ lỗi chặn mới thì KHÔNG gộp đêm nay — không ước giờ với chủ dự án.
3. Bảng harness của B ⇒ chọn việc kế của X12; bản sửa A1 (nếu B chữa) cần phiên đo đọc + một lượt thật trước khi gộp.
4. D báo nhánh `p9-d-giao-trinh` sẵn ⇒ đọc diff, gộp.
5. Trong buổi chủ dự án test 23/11: chép nguyên văn lỗi vào `data/loi_user/2026-11-23.md`, tra runbook mục 10, đếm / tái hiện rồi mới giao; KHÔNG bật server ở 8010, không đổi chỉ mục; bản sửa gom thành đợt, nói rõ "chạy lại lệnh bật để có X, Y".
6. Gói soát khác hãng cho CODE chiều + tối 22/11 (`c19ab298..main`) sau khi giao diện gộp; nói chủ dự án một lần.
7. Câu gác cho chủ dự án, mỗi lần MỘT câu có ô tick: thứ tự ở `HIEN_TRANG.md` mục 3 (bảy câu). KHÔNG nêu: AWS, tiền OpenAI, tiền Bedrock (kể cả số ước), chuyện trình bày.
8. Kết phiên đêm: vòng cải tiến cách làm (đầu vào: `SO_CAI_TIEN_CACH_LAM.md` khối "PHIÊN TỐI 22/11" + mục bẫy dưới + bẫy trong sổ B, C, E) · đoạn tóm tắt chiều + tối ở `TONG_HOP.md` (hiện mới có phần dời nguyên văn).

## Đang chạy / file tạm
Agent con của phiên điều phối: 0 (ba agent so cặp ảnh của phiên trước đã dừng; kết quả ở `data/giao_dien_2026-11-22/so_cap/`: NHOM_1 đủ 17 cảnh, NHOM_2 tới H13, NHOM_3 tới L10 — chưa so C01–C03, L11, L11a). Tiến trình nền: 0. File tạm của phiên này trong `/tmp`: `hr_a_sua_so.py`, `hr_a_sua_ht.py`, bốn file `hr_a_*.txt` (bản dời sổ; bỏ được). File riêng tư còn dùng: `data/review_khac_hang/2026-11-22_giao_dien/` (đề bài + ba kết quả), `data/review_khac_hang/2026-11-22_harness/` (đề bài + kết quả GPT-6.2 Sol). Bốn bản chụp Qdrant của 22/11 còn trong container (xoá là việc hỏi chủ dự án).

## Bẫy (đầu vào cho vòng cải tiến; bốn dòng đầu của phiên tối 22/11, giữ tới khi vòng cải tiến chạy)
- "ĐÃ CHỤP" ≠ "ĐÃ SO": cổng gộp giao diện phải có bước so từng cặp cùng mã cảnh.
- Bộ kiểm chỉ đổi MỘT chiều (bề rộng) bỏ sót chiều cao khung nhìn máy xách tay — AI khác hãng mới thấy. Đêm 22/11 phiên đo đi thêm một bước đúng: đọc cỡ màn hình THẬT của máy demo thay vì đoán ba cỡ.
- Ba lần nói "sắp gộp" trong hai giờ, mỗi lần lộ một lỗi chặn; ước giờ cho chủ dự án lùi ba lần ⇒ không ước giờ gộp.
- Đích di động (đẩy thêm commit vào nhánh đang được kiểm) và giao trùng `lkh.css` ⇒ đêm 22/11: C / B chia file ngay trong tin mở phiên, nhánh con riêng, ghép thành một sha.
- Báo số tiền Bedrock cho chủ dự án ba lần (trí nhớ đã cấm) · nối `commit_push.sh … | tail && git merge` làm bước gộp chạy dù commit bị hook chặn.
- Mới đêm 22/11: sổ ghi "Qdrant bật" nhưng máy khởi động lại sau lúc ghi ⇒ lệnh kiểm nhanh lúc mở phiên bắt được (cổng 6335 không trả lời); một phiên C và một phiên đo mở giữa 20:44 và 21:25 đã làm dở việc không có trong sổ (nhánh local `p13-c-man-dau-cao`, bộ chụp sửa 21:22) — phiên mở lại tự thấy nhờ giờ sửa file.
