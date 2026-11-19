# Nhật ký phiên E — 19/11/2026 (nối; mỗi việc ≤ 3 dòng: việc · kết quả + mã commit · tiền · bẫy)

Viết 11:19 19/11/2026 (`date`) lúc kết phiên nhẹ. Vai hôm nay: người kiểm / người đọc tay / người đặt tiêu chí. Tiền API của E cả ngày: 0 USD. Chi tiết từng mục (giờ, số, lời qua lại): `session_prompt/archive/STATUS_E_LICH_SU_2026-11-18_19.md`.

1. **Review báo cáo lượt đo cuối của B** (`p9-b-do-cuoi-1811`) ⇒ yêu cầu sửa rồi ĐẠT ở `53e559e`. Bẫy: ba góp ý chỉ về hình thức — không đáng một vòng.
2. **Câu lời dặn cho ca thiếu lưu ý an toàn** (C viết, `p9-c-s09-luu-y-an-toan`): review plan hai vòng + nhánh `338337c` ⇒ sẵn sàng với cờ tắt; E đọc tay lượt thật ⇒ KHÔNG ĐẠT tiêu chí ghi trước (điểm "đủ ý" tụt quá mức cho phép), cờ giữ tắt, không gộp. Bẫy: bộ dò chữ của công cụ đo sai 6 / 9 ca E thử ⇒ phải đọc tay.
3. **Bản bằng code cho cùng ca đó** (C, `p9-c-s09-noi-dong-tam-ngung`): `0ceaafc` yêu cầu sửa (lưu ý chép nửa câu do dòng kho bị xuống hàng) ⇒ ĐẠT ở `c2813b1`; cờ đã bật trên main `55d01a8`.
4. **Sửa lịch "đổi chỗ" bằng code** (B, `p9-b-sua-lich-doi-cho`): `dedb552` yêu cầu sửa (hai ca áp nhầm) ⇒ ĐẠT ở `693bde4`; E đọc lượt thật: 9 / 10 chuỗi đạt cả hai lần, 0 lần sửa sai / 42 ⇒ cờ bật.
5. **Ba nhánh nhỏ của B**: tự tối ưu bước tìm `c8dcdd4` ĐẠT · bỏ trần token đầu ra `33bb05a` ⇒ sửa nhỏ ⇒ `8840d2d` ĐẠT · bỏ ngân sách ngữ cảnh `bd2a2ac` ĐẠT. Bẫy: một ca "thử phá" của E không áp được vào code mà suýt bị đọc là "test vẫn xanh" ⇒ xác nhận ca phá đã áp trước khi đọc kết quả.
6. **Đọc diff ba nhánh tài liệu** (runbook của B `2e3936b`; tài liệu + trang hiện trạng của C `fe187d7`; thư mục báo cáo theo ngày của A `3f1b221`) ⇒ ĐẠT sau các chỗ sửa chữ (số cờ bật ghi sai, nhãn độ tin ghi quá).
7. **Kế hoạch thí nghiệm mức suy luận low / medium / high** — E viết tiêu chí, bản 3 sha256 đầu `eb0a43776125`, A duyệt; B chạy, C đọc tay. Chưa chạy lượt có phí. Bẫy: ghi giờ ước trước khi chạy `date`.
8. **Góc "làm thay" cho hướng việc phổ thông** — gửi nhóm: không đặt thật, không gửi thư từ server; link điền sẵn do code dựng + bản nháp tin nhắn. Bẫy: gộp cờ `-il` cho `scripts/grep_kb.sh` rồi che stderr ⇒ 14 số 0 giả.
9. **Trang cách làm việc + bộ khung theo "thư mục từng ngày"** — `b3f721b` + `0a44538`, C đọc diff (4 chỗ sửa), gộp ở `02c1156`. Bẫy: ba vòng cắt mới dưới trần byte.
10. **Bộ kịch bản "việc phổ thông" bản đầu + kế hoạch một trang** — 80 kịch bản / 106 lượt, B đã đọc và E đã sửa theo; CHƯA được A duyệt theo sha, chưa chạy. Bẫy: dựng sẵn phần giữ kín rồi phải bỏ; ước tiền cao gấp 3–6 lần số thật.

### Buổi trưa 19/11 (phiên E mở lại ~11:25, terminal `hue-rag-b5`)
11. **Soát công cụ chạy bộ kịch bản của B** — bản đầu chưa đạt (lỗi Qdrant / model giữa luồng không tính là lỗi hạ tầng; trần tiền chết khi thiếu `--log`); B sửa, bản `40bf732efeb1` đạt. Bẫy: E viết "khoản bị bỏ đã nằm trong tổng" quá rộng ⇒ B bỏ khỏi trần ⇒ E đọc lại code, B xác nhận bằng log, hoàn lại. 0 USD.
12. **Bài `bai_hoc/VIEC_MOI_XONG.md` mục 7–11** (việc xong sáng 19/11) — đã ở main (`7a42599`, sửa 70 lượt `fa74846`). Agent con đối chiếu 110 khẳng định: 4 sai · 14 dễ hiểu nhầm · 1 không nguồn, sửa hết trước commit. 0 USD.
13. **Thử ba "cách thử 2 phút" trên giao diện** — cả ba không ra như bài viết; sửa bài + dòng Đã thử (`9a1f91a`, đã ở main); runbook 10.2 thêm hai giới hạn (`cf4bf4b`, CHƯA gộp). Thấy: dời hai điểm trên lịch mặc định bị luật xếp chặn (B: 1 / 13 cặp được); câu dời kèm dấu hỏi được đáp "Được, có thể đổi…" mà lịch không đổi; câu kể dài bị rút vì trích dẫn. ≤ 0,004 USD.
14. **Phân xử hai phiếu chấm bộ 80 kịch bản** — xong nới 51 · sát chữ 40 · mục web 4 · chưa xong 25 · sai 5; ba lỗi đầu: trả lời theo lịch khác (3), trả lời rỗng báo thành công (2 lượt), từ chối khuôn thay vì nói thật. E chỉ mở 21 / 80 kịch bản. 0 USD.
15. **Khối "sửa sau duyệt" plan mức suy luận** (bậc 2 chỉ medium + low, một phép so, S19 sinh lại 3 + 3, trần bậc 2 hạ còn 0,35 USD) — sha `de90b6bde2da`, chờ A ghi duyệt.
16. **Bước 0b plan "ngữ cảnh lớn hơn": đọc 26 câu yếu** — chạm: 15 đoạn 7 câu · cả mục 6 câu; tổng cổng 12 / 10 (theo chữ plan) hoặc 8 / 7 (chỉ trong 26 câu) — A chọn. Dò theo từ khoá rồi mới mở dòng. 0 USD.
17. **Plan "nói thật giới hạn thay câu từ chối khuôn"** — sha `78de38324834`, B đang review. Đếm trước: 18 lượt từ chối khuôn đều do model viết; chỉ 4 lượt là "làm thay". Thiết kế: một trường thêm ở lần gọi định tuyến + code thay câu, không sửa lời dặn trả lời.

**File riêng tư E viết hôm nay (ngoài git — chỉ ghi đường dẫn):**
- `data/phase_9/b7_cuoi/review_bao_cao_E.md`
- `data/phase_9/s09_luu_y/PLAN_review.md` · `data/phase_9/s09_luu_y/NHANH_review_E.md` · `data/phase_9/s09_luu_y/doc_tay_E.md`
- `data/phase_9/s09_code/PLAN_review.md` · `data/phase_9/s09_code/NHANH_review_E.md`
- `data/phase_9/muc_suy_luan/PLAN.md`
- `data/kich_ban_pho_thong_2026-11-19/` (`PLAN.md`, `README.md`, `bo_kich_ban.jsonl`, `kho_dem.tsv`, `tools/dem_kho.py`)
- (trưa) `data/kich_ban_pho_thong_2026-11-19/luot_1/KET_QUA.md`, `phan_xu_E.json` · `data/da_thu_2026-11-19/` · `data/bai_hoc_doi_chieu_2026-11-19/doi_chieu_muc_7_11.md` · `data/ngu_canh_lon_2026-11-19/buoc_0b/doc_cham_E.md` · `data/tu_choi_khuon_2026-11-19/PLAN.md`
