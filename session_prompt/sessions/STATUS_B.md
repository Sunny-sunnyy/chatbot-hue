# STATUS B — cập nhật 14:49 02/11/2026 (KẾT PHIÊN 02/11: B121–B123 xong; spec Phase 9 bản 9 User duyệt — việc tiếp của B: bậc B0 phiên sau)

Terminal phiên 02/11: `hue-rag-d6` · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-7e`, C = `hue-rag-29` (cả ba Claude Code, trực tiếp). Mã việc = mã A giao.
**Phiên mới:** mở theo `session_prompt/START_SESSION.md`; việc lấy ở `CURRENT_HANDOFF.md` (A viết) — file này chỉ là sổ tay của B. Tên terminal đổi mỗi lần mở ⇒ `ListAgents`.
Phiên 02/11: User nói ở terminal B (09:49 02/11/2026, giờ B ghi bằng `date`): B làm việc trực tiếp với A; việc A giao = "làm đi". Quyền phiên (≤ 1 USD, B / C push nhánh riêng) **hết hạn cuối phiên**.

## Đang làm / dở
- **Không** (kết phiên 14:49 02/11/2026). Không job nền, không server, không worktree; file tạm `/tmp` của B121–B123 đã xoá.
- Nhánh `giao-dien-moi` (đã merge `ed8e6e8`) còn trên máy + `origin` — A đề xuất User xoá (User `!`).
- **Việc tiếp (phiên sau):** bậc **B0** của spec Phase 9 bản 9 (User duyệt, sha `169c2dd5f86a`) — chờ A giao mục việc trong `CURRENT_HANDOFF.md`.

## Đang khai báo sửa
- không

## Phiên 02/11 đã xong
| Việc | Kết quả | File / commit |
|---|---|---|
| **B121** giao diện mới (React + Vite + Tailwind, FastAPI phục vụ `frontend/dist/`) | dò CSP: Radix Collapsible / Tooltip / Popover đạt, Dialog / ScrollArea vi phạm ⇒ 0 gói Radix; 19 yêu cầu [Chạy] / [Tự dựng]; review C119 ready (0 / 0 / 2 minor); m-1 (lời lỗi tiếng Việt) sửa `deaa605`; **A merge `ed8e6e8`** | `report_agent/2026-11-02_giao_dien_moi_code/b121_giao_dien_implementation.md`; `data/giao_dien_moi_2026-11-01/do_csp/`, `b121/` |
| **B122** tra web agent Phase 9 (3 lượt Codex + WebFetch 3 × 3 ý) | Serper: điều khoản 29/05/2024 không nói rõ dùng cho người dùng cuối / hiển thị / lưu ⇒ chưa qua W35; 0,001 USD / lượt; SDK mới nhất 0.24.0, ≥ 0.21 đòi `openai>=3`; đo agent: pass^k, chọn công cụ; injection: quyền hẹp, spotlighting | `data/nghien_cuu_phase_9_2026-11-01/agent/b122_tra_web.md`; `data/tra_cuu_cli/2026-11-02_b122-*` |
| **B123** dò Agents SDK 0.19.4 (probe công cụ giả) | cả 3 việc làm được trên 0.19.4: hook `on_llm_start/end` + `response.usage` (USD + ms mỗi lần gọi); lượt gọi công cụ không có `output_text.delta` ⇒ lọc theo mục `message`; `output_type` strict `route` trước `answer` (phải sửa `ANSWER_PREFIX`); `tool_choice="required"` tự reset. A kiểm 2 ý: đạt | `data/nghien_cuu_phase_9_2026-11-01/agent/b123_sdk_probe.md`, `b123/` |

## Tiền paid (B, 02/11, giá đủ)
B121 ≤ 0,0015 (4 câu có token ≈ 0,00094 + 2 câu rời trang không có số token — cận trên) · B122 0 (Codex qua tài khoản ChatGPT) · B123 0,00023 ⇒ **≈ 0,002 USD**. Không gọi `agy`, không gọi Serper.

## Câu hỏi / thắc mắc cho A
1. 4 worktree AGY cũ `~/.gemini/antigravity-cli/…` (commit `c725987`) vẫn còn — User quyết.
2. Sự cố pgrep (bẫy đầu tiên dưới) — đầu vào vòng cải tiến: đề xuất luật "việc dài luôn `run_in_background`; không im lặng quá ~15 phút khi chờ".

## Bẫy đã gặp — đọc trước khi làm
- **(02/11, sự cố — mất ~2 giờ)** Chờ một tiến trình bằng `until ! pgrep -f "<mẫu>"` ⇒ `pgrep -f` khớp **chính dòng lệnh của vòng chờ** (chứa mẫu) ⇒ không bao giờ dừng, B ngồi chờ thông báo không tới, A phải hỏi. Gốc: chạy lượt Codex bằng `&` trong lệnh Bash (không có thông báo xong) thay vì `run_in_background`. Cách đúng: mỗi việc dài chạy bằng `run_in_background` (có thông báo); nếu phải chờ PID thì `while kill -0 <PID>`; và đặt mốc tự kiểm (không im lặng quá ~15 phút khi chờ).
- (02/11) Playwright `page.route` gọi handler với 1 hoặc 2 tham số tuỳ chữ ký ⇒ lambda `(r, s=spec)` nhận `request` vào `s`; dùng hàm một tham số. Script tự bật server con ⇒ bọc `try/finally` tắt server (lần lỗi đầu để sót uvicorn 8813, đã `kill` đúng PID).
- (02/11) Dò CSP nhiều linh kiện **chung một trang** ⇒ vi phạm của một cái (ScrollArea chèn `<style>` lúc hiện) làm mọi ca trông như vi phạm ⇒ mỗi linh kiện một trang. `curl -I` (HEAD) vào `/` trả 405 nên không thấy header CSP ⇒ kiểm bằng GET (`curl -s -D - -o /dev/null`).
- (02/11) DOMPurify phân tích chữ có `<style>` bằng `DOMParser` ⇒ trình duyệt báo 1 vi phạm CSP dù thẻ bị lọc (CSP chặn lúc phân tích) — không phải lỗi giao diện; bản cũ cũng vậy.
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
- Phiên 01/11 (S1–S4, B107–B120): `git show 9c86a98:session_prompt/sessions/STATUS_B.md`.
- Phiên 31/10 (B99–B106): `git show f34cb7f:session_prompt/sessions/STATUS_B.md`. Phiên 30/10: `session_prompt/archive/STATUS_B_LICH_SU_2026-10-30.md`; 29/10: `…_2026-10-29.md`.
