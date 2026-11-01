# STATUS B — cập nhật 16:16 01/11/2026 (kết phiên chiều 01/11: B116–B120 xong; B rảnh)

Terminal phiên chiều 01/11: `hue-rag-7a` · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-c0`, C = `hue-rag-b0` (phiên sáng: B `hue-rag-da`, A `hue-rag-27`, C `hue-rag-6a`) (cả ba Claude Code, trực tiếp). Mã việc = mã A giao.
**Phiên mới:** mở theo `session_prompt/START_SESSION.md`; việc lấy ở `CURRENT_HANDOFF.md` (A viết) — file này chỉ là sổ tay của B.
Phiên chiều 01/11: User nói ở terminal B (13:59, giờ B ghi nhận bằng `date`): B làm việc trực tiếp với A; việc A giao = "làm đi". Quyền khác (trần tiền…) theo mục việc A ghi trong `CURRENT_HANDOFF.md` (A đang hỏi lại User).

## Đang làm / dở
- **B119** xong 15:55 01/11/2026, chờ A xem (`tripo/b119_kham_pha.md`). Server 8797 đã tắt, script `/tmp/b119_tools` đã xoá, không job nền. Tiền ≈ 0,0040 USD.
- **Không** (kết phiên chiều 15:24 01/11/2026). Không job nền, không server, không worktree, không nhánh mới của B. Codex: 2 lượt `tra_web_codex.sh` đã xong.
- Phiên sáng: nhánh **giữ** chờ User xoá: `s1-loi-chung`, `s3-giao-dien`, `dg-cost-usd`, `streaming-final` (đã vào `main` ở `a80e12d`).

## Đang khai báo sửa
- (xong) B119 (từ 15:39 01/11/2026): `data/nghien_cuu_phase_9_2026-11-01/tripo/` (ảnh, kết quả thô, `b119_kham_pha.md`); script tạm `/tmp/b119_tools/`; dòng trạng thái B119 trong `CURRENT_HANDOFF.md`
- không (file của B116 / B117 đã xong; chưa commit — A commit `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md`; file `data/` là private)

## Phiên 01/11 đã xong
| Việc | Kết quả | File / commit |
|---|---|---|
| Review spec streaming vòng 3 + R3.4 | ready (sau Q1 User) | `report_agent/2026-10-31_streaming_spec/b105_review.md` |
| **S1** gom lõi chung (route JSON + `answer_case`) | T1 giống byte; review A ready | nhánh `s1-loi-chung` `9c83003`; `s1_loi_chung_implementation.md` |
| B107 đề xuất sửa câu Golden lệch kho | User giữ nguyên (chỉ `check` phân biệt hoa / thường) | `data/golden_sua_2026-11-01/b107_de_xuat.md` |
| **S2** route `/api/chat/stream` (SSE) + sửa m-1 nửa surrogate emoji | review ready; S2 đóng | `830df0e`, `887cbc5`; `s2_stream_route_implementation.md` |
| **B108** `cost_usd` giá đủ + token đệm trong log | SDK trả `cache_write_tokens` = vào − 3 cả hai đường | `dg-cost-usd` `bbbdbf9`; `b108_cost_usd_implementation.md` |
| Review plan đo cuối C103 (3 vòng) | ready ⇒ A duyệt `ae8d42d520d4` | `c103_plan_review.md` |
| **S3** giao diện đọc luồng + R2 (DOMPurify danh sách cho phép, CSP `/` + `/static`) | review C ready | `9374212`, `fc10873`, `716ba4d`; `s3_giao_dien_implementation.md` |
| Q3a L2 / L3 theo loại câu | chỉ câu nhiều nguồn còn lớn ⇒ User dời Phase 9 | `q3a_theo_loai_cau_implementation.md`; `data/q3a_2026-11-01/` |
| Nhánh gộp `streaming-final` | gộp sạch, 88 test, T1 giống byte | `6a0c842` (A merge `a80e12d`) |
| **S4** đo D2 trên trình duyệt | chữ đầu p50 1,23 / p95 2,61 s (đạt sàn + mục tiêu); lợi 441 ms < 500 ⇒ A xem PA3 | `s4_do_d2_implementation.md`; `data/s4_2026-11-01/` |
| Review runbook đo cuối C108 (2 vòng) | ready sau sửa `$G` / NameError / bỏ retry | `c108_runbook_review.md` |
| Review governance A CA1 + CA3 (2 vòng) | M-1 pre-push lọt tên có dấu ⇒ A thêm `-z` ⇒ ready | `a_governance_ca1_ca3_review.md` |
| **Đo cuối §6 + §7** (bộ an toàn, câu theo ngày) | qua mọi sàn; A2 vế 1 = 2 ≤ 2 (đúng ngưỡng), sinh lại ngang mốc 751b352 | `do_cuoi_b_an_toan_ngay.md` |
| **Đo cuối §8** bộ kín mới (40 câu, chỉ số đếm) | qua mọi sàn; Đủ ý −0,40 so với Golden, do **cả** 4 từ chối nhầm **lẫn** câu trả lời kém đủ ý (cùng cách: −0,22; một dữ kiện 4,42 ↔ 4,97) | `do_cuoi_b_bo_kin.md` (A commit `85f8e46`) |
| Sửa theo `do_cuoi_review.md` (M-1, m-2, m-3 bộ kín + m-1 an toàn) | A nhận đạt; trỏ bằng chứng sang `archive/CURRENT_HANDOFF_LICH_SU_2026-11-01.md` | `do_cuoi_b_bo_kin.md` `d8d9258a9ce7` (A commit), `do_cuoi_b_an_toan_ngay.md` `cac60f04137e` |
| Kiểm lại sổ cải tiến sau A khôi phục | 0 mục mất; S63–S67 thiếu 2 / 7 cột | báo A |
| **Phiên chiều 01/11** | | |
| **B116** so sánh cách làm giao diện mới (tư liệu) | đã chọn React + Vite build tĩnh, FastAPI phục vụ, Tailwind, shadcn chỉ sau dò CSP; yêu cầu 18 (`[Nguồn n]` thành link); bước dò CSP; hướng nhìn (ASCII, 12 token AA tính thật, Be Vietnam Pro OFL tự host, 6 trạng thái). Còn chờ User: cách hiện nguồn, D5 | `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md`; `data/giao_dien_moi_2026-11-01/` |
| **B117** tra cứu Phase 9 mạch 1 + 2 | Codex 2 lượt + B WebFetch: Huế TRIPO (31/10/2026), cổng an toàn Royal Armouries, Air Canada; Expedia trust gap, Agoda VN, Musa Guide; A kiểm lại 2 ý khớp; sửa phạm vi 8 % (Mỹ + Anh) | `data/nghien_cuu_phase_9_2026-11-01/b_mach1.md`, `b_mach2.md` |
| **B118** review bản sơ bộ `BAO_CAO_NGHIEN_CUU_PHASE_9.md` (A viết) | `changes_requested`: 0 blocker · 3 major (2 ý tự khai dưới nhãn C kiểm; "đúng cách hue_rag" nói quá) · 5 minor; overlap_scan 0 trùng. **Vòng 2 (15:29 01/11/2026): ready** — 3 major đóng; còn m-2 / m-3 một phần + m-6 (FEVER gọi sai "kiểm dữ kiện") + m-7, không chặn | `report_agent/2026-11-01_nghien_cuu_phase_9/b118_review_bao_cao_so_bo.md` |
| **B119** khám phá Huế TRIPO (Playwright) + 10 câu so hue_rag | TRIPO: biểu mẫu → hỏi thêm bằng nút → 3 phương án → lịch trình có giờ / chi phí / bản đồ / thuyết minh / PDF; nhớ hội thoại; trả giờ / giá. Yếu: câu trang phục Đại Nội trái hue_rag (chưa kiểm ai đúng), an toàn / chi phí tự sinh không nguồn, lịch quá giờ đóng cửa, 14–36 s. hue_rag: từ chối câu 2 + 7 (câu 2 có thể từ chối nhầm) | `data/nghien_cuu_phase_9_2026-11-01/tripo/b119_kham_pha.md` |
| **B120** review bản 2 `BAO_CAO_NGHIEN_CUU_PHASE_9.md` | lần 1 blocked (bản 2 chưa lưu); lần 2 **ready**: 0 blocker / 0 major, 2 minor (câu 4 "đúng" ⇒ "khớp"; thiếu lưu ý bản dịch Luật AI); overlap_scan 0 trùng | `report_agent/2026-11-01_nghien_cuu_phase_9/b120_review_ban_2.md` |

## Tiền paid (B, 01/11, giá đủ; ca ngắt / hết token không có usage ⇒ cận trên)
S1 0,0018 · S2 0,0041 · B108 0,0007 · S3 ~0,0033 · S4 0,0158 · đo cuối §6–§8 0,0293 ⇒ **≈ 0,055 USD**. Không gọi `agy`; Codex không chạy (dùng lượt của A). **Phiên chiều 01/11: ≈ 0,0040 USD** (B119 hue_rag 11 lượt; còn lại 0 USD API) (2 lượt Codex qua tài khoản ChatGPT, WebFetch).

## Câu hỏi / thắc mắc cho A
1. S4: lợi "đủ câu − chữ đầu" 441 ms < 500 ⇒ D5 xem lại PA3 hay giữ PA1; nâng sàn (đạt mục tiêu 1,5 / 3 s)?
2. 4 nhánh của B còn trên `origin` (đã merge) ⇒ xoá khi User duyệt (tag `hoso/…` nếu cần).
3. 4 worktree AGY cũ `~/.gemini/antigravity-cli/…` (commit `c725987`) vẫn còn — User quyết.

## Bẫy đã gặp — đọc trước khi làm
- (01/11 chiều) WebFetch trang có JS (Huế TRIPO) **sót phần động** (ngân sách, chia sẻ) ⇒ B ghi "không thấy" sai; nhận xét về giao diện trang ngoài ⇒ dùng Playwright thật trước khi khẳng định "không có".
- (01/11 chiều) `tra_web_codex.sh` lượt nghiên cứu: Codex chạy chỉ 100–170 s, `url_da_mo.txt` rỗng dù báo cáo tự nói "đã mở trang gốc" ⇒ coi mọi URL là tự khai, tự WebFetch; vài trang (VietnamPlus, Wiley) WebFetch hết giờ / 403 / 502 ⇒ ghi tự khai, chọn ý dự phòng.
- (01/11 chiều) Đọc `.npmrc` của dự án khác bị auto mode chặn (có thể chứa token) ⇒ không đọc file cấu hình gói của dự án khác.
- (01/11) Chuỗi `G="VAR=… cmd"` rồi `$G` **không chạy** trong bash (gán biến chỉ nhận khi viết thẳng) ⇒ dùng hàm bash có `env`, gọi thẳng; hàm đưa vào `bash -c` không thấy biến ngoài.
- (01/11) `git diff-tree --name-only` không `-z` in tên có dấu trong ngoặc kép + bát phân ⇒ regex đường dẫn lọt; luôn `-z` (pre-push đã sửa).
- (01/11) SDK Agents tự `cancel()` (đặt `is_complete`) khi lần chờ `stream_events()` bị hủy ⇒ đọc nốt phải dựa cờ "mình dừng sớm", không dựa `is_complete`.
- (01/11) `curl … | tee | grep -m N` không làm đứt kết nối (tee không chết) ⇒ ngắt thật dùng `curl --max-time`.
- (01/11) Playwright `wait_for_function` dùng `eval` trong trang ⇒ bị CSP `script-src 'self'` chặn ⇒ chờ bằng vòng `page.evaluate`.
- (01/11) Bộ đệm prompt OpenAI chỉ áp từ ~1.024 token vào ⇒ câu ngắn ra `cache_write_tokens` 0 (không phải SDK làm rơi trường).
- (01/11) Lệnh "không ghi đè" (`write_new`) của harness lượt thật ⇒ không chạy thử trong thư mục lượt thật (chặn lượt thật); thử trên bản sao.
- (01/11) Script phân tích chạy từ `backend/` mà nằm ở `data/…/tools/` ⇒ `sys.path` lấy thư mục script; thêm `Path.cwd()`.
- (31/10) `rm` / `cp` với đường dẫn ghép từ biến bị tầng an toàn chặn ⇒ `"${X:?}"/…` hoặc đường dẫn tuyệt đối. Heredoc luôn `<<'EOF'` (trừ khi cố ý mở rộng biến).
- (31/10) Không bao giờ gọi `agy`. TestClient ≠ uvicorn với luồng ⇒ kiểm trên uvicorn thật. Finding suy từ đọc code ghi [Code, chưa chạy] tới khi chạy.
- Gõ giờ ước ⇒ luôn `date` trước (hook W37 bắt một giờ ước trong report S4 01/11 — đã sửa). Lệnh ghép có thao tác rủi ro ⇒ tách lệnh.
- Worktree có symlink `data/` ⇒ `unlink` từng link rồi `git worktree remove` (không `--force`, không `rm -r`).

## Lịch sử
- Phiên 31/10 (B99–B106): `git show f34cb7f:session_prompt/sessions/STATUS_B.md`. Phiên 30/10: `session_prompt/archive/STATUS_B_LICH_SU_2026-10-30.md`; 29/10: `…_2026-10-29.md`.
