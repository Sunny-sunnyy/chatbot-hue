# Cả bộ test một lượt trên main cuối (B, 12:09 20/11/2026, giờ `date`)

- **Bản được chạy:** `main` `d8651d41` (mọi bản sửa của ngày đã gộp; cây sạch), Python 3.13.15, môi trường của cây chính.
- **Kết quả [máy kiểm]:** **55 / 55 file đạt · 1.554 ca đạt · 0 hỏng · 0 lỗi.** Mốc so: tối 19/11 là 1.542 ca / 0 hỏng trên 55 file ⇒ thêm 12 ca từ test mới của ngày 20/11. Không file nào phải chạy lại. Phiên điều phối đã tự đọc bảng (109 dòng, 0 dòng mã thoát khác 0, 55 tên file).
- **Cách chạy:** từng file `backend/tests/test_*.py` một tiến trình pytest, nối tiếp, `HF_HUB_OFFLINE=1`; hai file cần khoá API chạy với `--env-file`; dừng nếu RAM khả dụng < 4 GB. Script + bảng + log (riêng tư): `data/test_rong_2026-11-20/` (`chay.sh`, `KET_QUA_d8651d41.tsv`, `log/`).
- **Sai sót của người chạy — đọc trước khi dùng số:** lượt này vô tình chạy HAI bản song song. Lần khởi động đầu (11:41:42) dùng tiến trình tách rời; bước chờ theo dõi nhầm PID của lớp bọc nên báo "xong" sai; người chạy tưởng bản đầu đã tắt, xoá bảng dở và khởi động lần hai (11:42:23) trong khi bản đầu vẫn chạy.
  - Vì sao kết luận vẫn đứng: mã thoát lấy theo TỪNG tiến trình pytest — cả 109 tiến trình (54 file × 2 + file đầu × 1) thoát mã 0; ở mọi file có đủ hai dòng tổng, hai lần ra cùng số ca. Số 1.554 tính mỗi file MỘT lần.
  - Thứ KHÔNG dùng được: số giây từng file (hai bản tranh CPU; cả lượt ≈ 25 phút đồng hồ, 11:41:42 → 12:06:39) · dòng "TỔNG" script in (cộng đôi) · dòng tổng của ba file ở một trong hai lần chạy bị trống vì hai bản ghi chung log (mỗi file vẫn còn một dòng đủ).
  - Trái luật "một tiến trình dựng app một lúc": RAM khả dụng thấp nhất lúc bắt đầu một file 4.966 MB (chưa chạm ngưỡng 4 GB); không dự án nào báo dừng.
- **Tiền gọi model thật:** cận trên 0,0048 USD (28 dòng `chat_metrics` có model + tiền trong khung giờ chạy) — `test_api_chat` chạy hai lần do sai sót trên, và không tách được ca dùng model giả có ghi tiền.
- **Chưa làm:** không chạy lại lượt sạch (phiên điều phối chốt không cần) · không có lượt trình duyệt / model thật nào trong việc này.
