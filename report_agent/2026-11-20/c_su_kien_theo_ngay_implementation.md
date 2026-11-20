# C — "sự kiện theo ngày": code + bảng + test (nhánh `p9-c-su-kien-theo-ngay`; plan đã duyệt `c_su_kien_theo_ngay_plan.md` `0681f44`)

Ghi 16:05 20/11/2026 (giờ `date`). Cờ `su_kien_theo_ngay` mặc định **TẮT**. Tiền: 0 USD. CHƯA có: người thứ hai đọc bảng, bộ dò độc lập của cổng, lượt thật.

**1. Người dùng thấy gì khác (khi cờ bật).** Hỏi "cuối tuần này ở Huế có sự kiện gì", "tối nay có lễ hội gì không", "tháng Giêng âm lịch ở Huế có lễ hội gì", "ngày 27/2 có gì đặc biệt"
⇒ trợ lý trả lời từ một danh sách do CODE tra: lễ hội có ngày cố định rơi vào khoảng đó (kèm ngày dương code đổi từ ngày âm của bài kho), lễ hội kho chỉ ghi khoảng, và hoạt động
lặp theo tuần (ca Huế hằng đêm, phố đi bộ tối cuối tuần, suất diễn ở Đại Nội). Khoảng không có lễ hội nào ⇒ nói thật là kho không ghi, kèm lễ hội gần nhất sắp tới. Cờ tắt (hiện nay) ⇒ không khác gì.

**2. Đã sửa.** file private `data/su_kien_theo_ngay_2026-11-20/su_kien_theo_ngay_v1.json` (mới, 27 dòng: 17 ngày cố định · 6 chỉ ghi khoảng · 4 theo tuần; mỗi dòng mang NGUYÊN VĂN câu ghi thời gian của bài kho) ·
`backend/llm/su_kien.py` (mới, hàm thuần: `hoi_su_kien`, `khoang_hoi`, `tra`, `dong_nguon`) · `backend/llm/assistant.py` (+19 dòng: cờ, bảng nạp ở rìa, `_nguon_su_kien`, một nhánh
trong `_before_model`) · `backend/config/settings.yaml` (+2 dòng) · `guides/RUNBOOK_BAN_GIAO.md` 10.1 (một dòng giới hạn) · test.
Lệch so với plan, nói thẳng: plan ước "~28 dòng = 17 + 8 + 3–4"; bảng thật có **6** dòng "chỉ ghi khoảng" (không phải 8) — hai bài C bỏ vì phải TỰ DIỄN GIẢI mới ra ngày
("đầu tháng 3 âm lịch", "nửa cuối tháng Chạp") và một bài chỉ ghi lệ xưa.

**3. Bằng chứng [máy kiểm, test bằng đồ giả — chưa có người thứ hai].** `tests/test_su_kien_theo_ngay.py` 21 đạt: mỗi dòng bảng có nguyên văn trong đúng bài nguồn (27 / 27) ·
đổi ngày âm đúng (mồng 6 tháng Giêng Đinh Mùi = 11/02/2027, 22 tháng Giêng = 27/02/2027; mốc đối chiếu: Tết Đinh Mùi 06/02/2027) · khoảng vắt qua Tết âm là MỘT lần
(23 tháng Chạp – mồng 7 tháng Giêng = 30/01 – 12/02/2027) · khoảng trống ⇒ lễ hội gần nhất · hoạt động theo tuần đúng thứ · cổng: 5 câu phải mở, 8 câu phải đóng ·
nối vào trợ lý: nguồn có trong lần gọi model đầu; câu không qua cổng ⇒ chuỗi gửi model giống từng ký tự với cờ tắt. Ca nối vào trợ lý ĐỎ khi gỡ dòng nối (1 hỏng / 20 đạt).
Tự khai: ba ngày mong đợi C viết lần đầu SAI (C nhẩm 23 tháng Chạp = 31/01, đúng là 30/01 vì tháng Chạp năm đó 29 ngày) — sửa kỳ vọng của test sau khi tính lại từ mốc Tết, không sửa code.
File chạm cờ / đường ngữ cảnh: `test_khoang_cach` 101 · `test_settings_env` 6 · `test_api_chat` 14 đạt (1 test cần khoá API không chạy ở lượt này).

**4. Chưa làm / giới hạn.** [chưa đo trên đường thật] · bảng CHƯA có người thứ hai đọc 100 % (phiên điều phối giao phiên B) · cổng đọc chữ người dùng CHƯA qua bộ dò độc lập (phiên E) ·
lượt thật cặp tắt ↔ bật 10 câu (≈ 0,02 USD) xếp sau · cả bộ test không chạy (một lượt cuối đợt) · model có trích đúng nguồn mới và có giữ câu "ban tổ chức có thể đổi ngày" không: chưa biết ·
giới hạn sản phẩm: runbook 10.1 dòng mới.

**5. Cách thử trong 2 phút (sau khi bật cờ + mở server).** Hỏi "cuối tuần này ở Huế có sự kiện gì" ⇒ câu trả lời nói không có lễ hội cố định, nêu lễ hội gần nhất + phố đi bộ / ca Huế;
hỏi "Huế có những lễ hội nào" ⇒ như trước (không qua cổng).

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm + đầu ra |
|---|---|---|---|
| bảng 27 dòng + hàm thuần + nối trợ lý + cờ tắt + test + dòng runbook | người thứ hai đọc bảng; bộ dò cổng; lượt thật; bật cờ | lượt thật chờ lượt bật server chung | `cd backend && uv run pytest tests/test_su_kien_theo_ngay.py -q` ⇒ `21 passed` |
- Thêm 16:06 20/11/2026: bảng để ở `data/` (private) chứ không vào git — hook của dự án chặn commit vì bảng chép nguyên văn câu của kho (12 dòng trùng ≥ 40 ký tự với kho, 1 dòng trùng với bộ câu kín theo nhãn của hook; C không mở bộ kín, không vượt hook). Hệ quả: bản chép không có `data/` thì file test tự bỏ qua và cờ không bật được — giống các bảng lịch.
- Thêm 16:12 20/11/2026 — phiên B đọc 100 % bảng (bản `v1`): SỐ đúng 27 / 27 dòng; bốn dòng "chỉ ghi khoảng" dễ bị hiểu là lễ kéo suốt cả khoảng ⇒ C sửa LỜI của nguồn ("lễ chỉ diễn ra một hoặc vài ngày TRONG khoảng đó… không khẳng định là có diễn ra đúng những ngày được hỏi") và thêm ba ghi chú nguyên văn (lễ Kỳ yên "Vào một ngày tốt"; Sóng nước Tam Giang chu kỳ hai năm; Điện Huệ Nam "mỗi năm 2 lần" — bảng chỉ có kỳ Thu tế). Bảng mới là `su_kien_theo_ngay_v2.json` (bản v1 giữ nguyên). B nêu một ứng viên chưa đưa vào: chợ đêm lặp HẰNG THÁNG vào một ngày âm lịch — cần kiểu lịch mới, C không thêm ở bản này (ghi giới hạn).
- Thêm 16:17 20/11/2026 — bộ dò MÙ của phiên E cho cổng (`data/kiem_ke_phase_2026-11-20/E_bo_do_su_kien.md`, chạy trên `c85e413`): phải mở 15 / 15; mở nhầm **1 / 20** — sàn ghi trước 0 / 20 KHÔNG đạt ở lần chạy mù: câu hỏi về QUÁ KHỨ ("tháng 3 năm ngoái … có lễ hội gì") được coi như tháng 3 sắp tới. Sửa MỘT lần: câu có từ chỉ quá khứ (năm ngoái, năm trước, tuần trước, vừa rồi, đã qua…) ⇒ cổng đóng; ba ca test mới đỏ trước (2 hỏng / 22 đạt), xanh sau (24 đạt). C chạy lại cùng 35 câu (không còn mù): mở 15 / 15, mở nhầm 0 / 20.
- Thêm 16:23 20/11/2026 — phiên B review cả nhánh (`22b17b6`): READY, 0 lỗi chặn; B tự đặt 12 + 20 câu và 14 ca khoảng ngày khó (cuối tháng, 30–31/12, sát Tết âm, ngày không có thật) — ngày đều đúng; cổng mở nhầm 4 / 20, trong đó hai câu cùng gốc ("có gì không ổn …", "có gì không nên …") ⇒ C sửa một dòng: "có gì không" chỉ nhận khi đứng cuối câu (ca test đỏ ⇒ xanh, 26 đạt); hai câu còn lại hiếm / vô hại ⇒ ghi giới hạn cùng năm giới hạn B nêu (runbook 10.1).
