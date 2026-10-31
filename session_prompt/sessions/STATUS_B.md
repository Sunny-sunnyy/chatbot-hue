# STATUS B — cập nhật 12:36 31/10/2026 (KẾT PHIÊN 31/10)

Terminal 31/10: `hue-rag-3b` · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-1a`, C = `hue-rag-69`. Mã việc = mã A giao.
**Phiên mới:** mở theo `session_prompt/START_SESSION.md`; việc lấy ở `CURRENT_HANDOFF.md` (A viết) — file này chỉ là sổ tay của B, không phải danh sách việc.

## Đang làm / dở
- **Không.** Không job nền, không worktree của B, không server, `/tmp` không còn file của B (đã kiểm `ls` + `git worktree list` 12:36).
- Chờ (không phải việc đang chạy): phần `TBD` "mức chuẩn ngành chữ đầu tiên" của spec streaming — A điền ⇒ B kiểm **phần đổi** (không chạy Codex lần 2, A quyết).

## Đang khai báo sửa
- không

## Phiên 31/10 đã xong (sha 12 ký tự, tính lúc kết phiên)
| Việc | Kết quả | File (sha) |
|---|---|---|
| B99 kiểm nguồn kết quả ChatGPT streaming | 21 / 22 URL mở, 0 ý bị nguồn nói ngược, 3 ý "theo tài liệu" là suy ra | `data/tinh_nang_moi_2026-10-27/b99_kiem_nguon_streaming.md` (`44644b22d9ef`) |
| B100 review C97 (2 vòng) | M-1 `EventSourceResponse` + lỗi trước luồng ⇒ 200 thân rỗng; ready (C97 bản 2/3) | `…/b100_review_c97.md` (`b0b49be37fc4`); probe `…/tools/b100_probe_sse_status.py` (`b96f4233083f`), `b100r_app_probe.py` (`f1008b3329a9`), `b100r_drive_disconnect.py` (`b661a9fdad31`) |
| B101 (thu hẹp) mốc ChatGPT Y2 | 6 / 6 khẳng định đúng; URL 15 / 18 2xx (3 × 403 chặn máy, 0 bịa); chấm 6 bản ⇒ C99 | `data/tra_cuu_cli_2026-10-31/b101_cham.md` (`911b4bb778ce`) |
| B102 review nháp v3 (2 vòng) | M-1 test giao diện không tạo được bằng đường thật; ready | `…/b102_review_c98.md` (`c59b412d702f`) |
| B103 review governance tra web Codex (3 vòng) | `--json` + `jq`, đếm theo `item.id`, dòng hỏng cảnh báo; ready ⇒ A commit `1a9dca4` | `report_agent/2026-10-31_tra_web_codex/b103_review.md` (`748e81ca362d`, đã commit); lượt chạy `data/tra_cuu_cli/2026-10-31_b103-probe/`, `…_b103-r2/` |
| B104 gói Codex review spec | lệnh worktree sạch + `codex exec` read-only + lọc lệnh; thử dựng / gỡ 2 lần | `…/b104_codex_review_spec.md` (`a8ba02fc2a59`), `…/b104_prompt_codex.md` (`c9fd057a6e28`) |
| B105 review spec streaming (2 vòng) | M-1 anyio hủy mọi `await` trong `finally` (probe 0/5 ↔ shield 5/5); ready bản 3 | `report_agent/2026-10-31_streaming_spec/b105_review.md` (`96bcc907886b`, **chưa commit**); probe `…/tools/b105_app.py` (`fdd0ad410464`), `b105_drive.py` (`7c3057c60fba`) |
| B106 Codex review spec 1 lần (W33) + lọc | 58 s, 14 lệnh đọc trong worktree, 0 ra ngoài; 2 finding đúng — mới (minor); C sửa ⇒ **spec bản 4 `cf1ae9ef6c2c` ready** | `report_agent/2026-10-31_streaming_spec/b106_codex_review.md` (`cab2ca485750`, **chưa commit**); thô `data/tinh_nang_moi_2026-10-27/2026-10-31-streaming-design_review_codex/` |

## Tiền paid (B, 31/10)
- **0 USD.** Codex (2 lượt script + 1 lượt review) dùng gói tài khoản ChatGPT của User. Không gọi `gpt-6-luna`. Không gọi `agy` lần nào.

## Câu hỏi / thắc mắc cho A
1. Commit: `report_agent/2026-10-31_streaming_spec/{b105_review.md, b106_codex_review.md}` (quét trùng 0) + spec `cf1ae9ef6c2c` khi User duyệt.
2. W33 — 2 ý ở `b106_codex_review.md` mục 3 (chạy Codex song song với review Claude; cho Codex đọc mã thư viện) ⇒ vòng cải tiến.
3. Ca 503 gần thật cho route stream: tiền lệ `backend/tests/test_startup_model_missing.py` (User `!`) — dùng hay không là quyết định luật §8 (`b106_codex_review.md` mục 5).
4. 4 worktree AGY cũ ở `~/.gemini/antigravity-cli/…` (commit `c725987` 05/09) vẫn còn — không phải của B; User quyết giữ / gỡ.

## Bẫy đã gặp — đọc trước khi làm
- (31/10) `rm` / `cp` với đường dẫn ghép từ biến (`"$WT/$SPEC"`) bị tầng an toàn Claude Code chặn ⇒ viết `"${WT:?}/${SPEC:?}"` (biến rỗng thì shell dừng) hoặc đường dẫn tuyệt đối.
- (31/10) Probe rào `agy` bằng `bash -c '…'` bị tầng an toàn auto mode chặn (cảnh báo áp cả phần còn lại của phiên) ⇒ chỉ thử dạng `false && agy …` (không bao giờ chạy agy), bị chặn thì dừng, không lách.
- (31/10) Không bao giờ gọi `agy` (kể cả `--version`) — luật cứng 7 `AGENTS.md`; mục việc ghi khác thì theo luật chặt hơn và báo lệch.
- (31/10) Heredoc không ngoặc (`<<EOF`) chạy cả backtick trong chữ ⇒ mất chữ trong file ⇒ luôn `<<'EOF'` hoặc Write.
- (31/10) Probe httpx: `next(resp.iter_raw())` tạo iterator tạm bị dọn ngay ⇒ client tự đóng sau 0,01 s ⇒ giữ biến iterator.
- (31/10) Finding suy từ đọc code (B100 m-3 "thời điểm khác") bị chạy thật bác ⇒ finding của người kiểm cũng ghi [Code, chưa chạy] tới khi chạy.
- (31/10) Kết review ⇒ nhắn **cả** người làm lẫn A (skill review: người kiểm nhắn người làm).
- (31/10) Codex nạp `~/.codex/skills` dùng chung của User (> 1.000 skill) và tự đọc `AGENTS.md` ở gốc worktree ⇒ prompt phải nói phần nào của `AGENTS.md` không áp.
- (31/10) TestClient ≠ uvicorn: lỗi giữa luồng TestClient ra "thân rỗng", uvicorn thật ra đứt kết nối ⇒ kiểm hành vi luồng trên uvicorn thật.
- Gõ giờ ước ("11:5x") ⇒ luôn chạy `date` trước khi viết dòng có giờ (W30; 31/10 lỡ 1 lần trong file B104, đã sửa).
- Lệnh Bash ghép nhiều bước có thao tác rủi ro bị auto mode chặn ⇒ tách lệnh; bị tầng an toàn chặn thì không lách.
- Worktree có symlink `data/` ⇒ `unlink` từng link rồi `git worktree remove` (không `--force`, không `rm -r`).

## Lịch sử
- Phiên 31/10: bảng trên + từng review (đường dẫn trong bảng).
- Phiên 30/10 (B91–B98): `session_prompt/archive/STATUS_B_LICH_SU_2026-10-30.md`. Phiên 29/10 (B90): `…/STATUS_B_LICH_SU_2026-10-29.md`. 28/10: `git show 5af038d:session_prompt/sessions/STATUS_B.md`.
