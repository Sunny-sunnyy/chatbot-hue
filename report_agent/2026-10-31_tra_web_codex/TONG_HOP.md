# TỔNG HỢP đợt 2026-10-31 — tra web bằng Codex CLI thay chép tay qua ChatGPT web

Viết 12:42 31/10/2026 (A, kết phiên). Trạng thái: **ĐÓNG** (User duyệt cách làm 11:21 31/10; governance commit `1a9dca4`, B103 review 3 vòng ready).
Dữ liệu chạy (private): `data/tra_cuu_cli_2026-10-31/` (tiêu chí, yêu cầu, kết quả, log, chấm), `data/tra_cuu_cli/` (đầu ra script).

## Mục tiêu
Claude Code của dự án chạy qua Bedrock nên không có WebSearch; trước đây mọi câu tra web phải nhờ User chép yêu cầu sang ChatGPT web rồi lưu kết quả về (chậm một vòng,
tốn công User). User 31/10 đề nghị: A gọi thẳng Codex CLI / Antigravity CLI (AGY) trong terminal để tra web, so kết quả với ChatGPT web trước khi dùng.

## Quyết định theo giờ (giờ A ghi nhận bằng `date`)
- 10:41 (ghi nhận) — User chọn PA1: chạy song song (A viết yêu cầu ChatGPT + thử CLI); Codex / AGY theo gói tài khoản, không tốn tiền; yêu cầu gửi CLI phải đòi "tìm chuyên sâu".
- 10:39 — tiêu chí ghi trước khi chạy (`tieu_chi.md`): URL mở ≥ 90 %, 0 URL bịa, 0 / 6 khẳng định bị nguồn nói khác, phủ ≥ 80 % ⇒ "tra nhanh"; thêm phủ đủ ý ≥ ChatGPT − 1 và giá trị
  không kém rõ ⇒ "thay ChatGPT".
- 10:54 — **dừng gọi AGY**: FAQ Google nói dùng phần mềm bên thứ ba (nêu tên Claude Code) truy cập Antigravity vi phạm điều khoản, có thể khoá tài khoản; bọc `agy -p` trong
  coding agent bên thứ ba không được hỗ trợ ở gói cá nhân (A WebFetch xác nhận). Đã gọi 4 lần trước đó. User tự dùng `agy` thì được.
- 11:21 — User duyệt: script + chặn `agy` + sửa luật; nhắc thêm ngày hôm nay vào yêu cầu để lấy thông tin mới nhất.
- 11:44 — User: "khi bạn chạy lỗi và không thể chạy thì tôi mới chạy giúp" ⇒ A tự chạy commit / push sau khi hỏi.

## Kết quả thử (6 lượt, chấm C99 — người chấm không phải người chạy)
| | Y1 streaming | Y2 thước đo sản phẩm | Y3 Claude gọi CLI |
|---|---|---|---|
| Codex (`gpt-6-luna`, 133–167 s, 26–46 lượt tìm, 0 lệnh shell) | tra nhanh đạt; giá trị **kém rõ** | tra nhanh đạt; **tương đương** | trượt đúng chữ (URL 87 %, 4 trang 403 có thật); **tương đương** |
| AGY (Gemini 3.8 Flash, 347–565 s) | trượt (83 %) | trượt (74 %: 3 URL 404, 3 URL trỏ sai bài) | đạt chữ, nhưng không nói điều khoản Google, còn khuyên cho Claude gọi `agy` |
| Mốc ChatGPT web | URL 91 % | 83 % | 86 % |

Codex: 0 / 18 khẳng định bị nguồn nói khác; 1 chỗ nói ngược nguồn ngoài 6 khẳng định (Y1). Hạn chế của thước (ghi để lần sau): ngưỡng 90 % làm cả ChatGPT trượt vì trang thật chặn máy;
6 khẳng định không bắt link trỏ sai bài ⇒ lần sau đếm riêng 403 trang thật + kiểm tiêu đề trang.

## Đã đổi (governance)
- `scripts/tra_web_codex.sh`: thêm ngày hôm nay + đòi thông tin mới nhất; Codex chạy thư mục trống `/tmp`, sandbox read-only, `--json`; đếm lệnh shell (`command_execution`, đã thử với
  `echo` thật — `data/tra_cuu_cli_2026-10-31/log/codex_json_echo_test.jsonl`) + cảnh báo; `url_da_mo.txt` = trang Codex thật sự mở (URL khác trong báo cáo là tự khai).
- `.claude/settings.json` chặn `Bash(agy)` / `Bash(agy:*)`; `AGENTS.md` luật cứng 7; `Session_Prompt.md` §9 đoạn "Tra web bằng Codex CLI" (câu tra nhanh: tự chạy; nghiên cứu lớn: Codex
  **và** ChatGPT web).
- Review B103: vòng 1 changes_requested (M-1 bộ đếm lệnh shell viết theo đoán định dạng log) ⇒ vòng 2, 3 ready (`b103_review.md` `748e81ca362d`).

## Giới hạn
- Mỗi yêu cầu chạy một lần / công cụ ⇒ chưa biết dao động giữa các lần. Codex nhận thêm phần đầu "tìm chuyên sâu" mà ChatGPT không có.
- `-s read-only` không chặn Codex đọc file ngoài thư mục làm việc — chỉ có lời cấm + bộ đếm cảnh báo; chưa cô lập bằng user Linux / container.
- Codex nạp `~/.codex/skills` dùng chung của User (ngoài repo) — không đổi cấu hình máy User.
- AGY có đọc file máy không: không kiểm được (auto mode chặn đọc `~/.gemini/`).

## Bước tiếp
Dùng script cho câu tra nhanh (31/10 đã dùng cho mức chuẩn "chữ đầu tiên" — `data/tra_cuu_cli/2026-10-31_ttft-chuan-nganh/`). Theo dõi: có lần nào cảnh báo lệnh shell không; tỉ lệ URL
tự khai so với trang thật mở.
