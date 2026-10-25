# Nhật ký 25/10/2026 — cải tiến cách làm việc của các agent

**Cập nhật lần cuối: 10:31 25/10/2026.** Tiền paid trong ngày: 0 USD. Chatbot không đổi gì.

## Tóm tắt
Phiên sáng chỉ bàn và sửa **cách các agent làm việc**, không đụng chatbot. Nguồn ý: bản mô tả cách làm của một dự
án khác của bạn (bản 2) và khóa AI FDE — 5 sub-agent đọc lại 15 file tóm tắt, tìm cái áp được cho hue_rag. Đã thêm:
vòng tự rút kinh nghiệm có bạn duyệt, skill thí nghiệm chặt hơn (đo nhiễu, tính cỡ mẫu trước), Session D để bạn tự
học dự án, file `AGENTS.md` cho mọi agent (cả Codex, AGY), và một "rào bằng máy" chặn commit dữ liệu riêng lên GitHub.
Một người kiểm độc lập (sub-agent) đã tìm ra 1 lỗi lớn ở rào chặn; đã sửa và thử lại.

## Bạn cần làm gì
- Không có việc bắt buộc. Khi muốn học lại một việc: mở Session D bằng `START_SESSION.md` với `<X>` = D.
- Phiên sau (tiếp dự án): A đọc `report_agent/2026-10-25_cai_tien_cach_lam/de_xuat_cho_du_an.md` trước khi duyệt kế
  hoạch G4/G2.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Vòng tự cải tiến + sổ | Đã thêm, vòng đầu ghi 8 sự cố thật | Lỗi quy trình được ghi lại và sửa đúng chỗ, không lặp |
| Skill thí nghiệm | Nâng cấp | Không kết luận "tốt hơn" khi chỉ là dao động ngẫu nhiên |
| Session D | Đã thêm vai + sổ khái niệm 28 mục (private) | Bạn tự giải thích lại được việc agent làm |
| `AGENTS.md` | Đã thêm | Codex / AGY / sub-agent đọc cùng luật như Claude |
| Rào chặn commit | Chạy thật; thử 13 ca phải chặn, 8 ca phải qua — đúng hết | Dữ liệu riêng, secret, tên dự án khác không lọt lên repo public |
| Đề xuất cho dự án | 19 mục cho 8.1 / 8.2 / Phase 9 / deploy | Chưa làm; quyết ở từng gate |

## Giải thích ngắn (để bạn tự nói lại được)
Agent không nhớ gì giữa các phiên, nên "kinh nghiệm" phải nằm trong file mà agent nào cũng đọc. Mỗi khi có sự cố
(lỡ tốn tiền, suýt lộ dữ liệu, bạn phải nhắc lại), A ghi vào sổ, đề xuất sửa luật ở đúng chỗ, bạn duyệt cho thử,
phiên sau xem có hết lặp không. Việc nào hậu quả không đảo ngược được (như lộ dữ liệu lên GitHub) thì chặn bằng
máy ngay. Giới hạn: bằng chứng "luật có ích" chỉ là quan sát qua nhiều phiên, chưa phải số đo.

## Đọc thêm
- `report_agent/2026-10-25_cai_tien_cach_lam/KE_HOACH.md` (danh sách thay đổi, phép thử), `review.md` (kiểm độc lập),
  `de_xuat_cho_du_an.md` (đề xuất cho dự án)
- `session_prompt/SO_CAI_TIEN_CACH_LAM.md` (sổ cải tiến)
