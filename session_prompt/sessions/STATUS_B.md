# STATUS B — cập nhật 13:20 03/11/2026 (KẾT PHIÊN 03/11: B3 nhánh `p9-b3` `46008ed` — khoá phần đã thấy, chờ C chạy kín; chưa merge)

Terminal phiên 03/11: `hue-rag-52` (A = `hue-rag-5e`, C = `hue-rag-d8`) · Agent: Claude Opus 5.5 · Vai: thực thi. Mã việc = mã A giao.
**Phiên mới:** mở theo `session_prompt/START_SESSION.md`; việc lấy ở `CURRENT_HANDOFF.md` (A viết) — file này chỉ là sổ tay của B. Tên terminal đổi mỗi lần mở ⇒ `ListAgents`.
Quyền phiên (User qua A: việc A giao = "làm đi", B push nhánh riêng) **hết hạn cuối phiên** — hỏi lại phiên sau.
**Phiên chiều 03/11 (mở 18:02 03/11/2026):** terminal B `hue-rag-32`; peer `hue-rag-40`, `hue-rag-9e` (chưa rõ ai là A). User: B làm trực tiếp với A, việc A giao = "làm đi". Worktree `/tmp/b_p9b3` mất (prunable) ⇒ tạo lại khi được giao.

## PHIÊN SAU — B3 (B136 dở; report `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md`)
Worktree **`/tmp/b_p9b3` giữ** (nhánh `p9-b3`, symlink `data/` + `knowledge-base-hue/`). Lệnh nền: `cd /tmp/b_p9b3/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag [--env-file /home/minhhieu/hue_rag/.env] …`.
Trần B3 **0,40 USD, dừng > 0,37** (A, 03/11); đã dùng **≈ 0,255**. Ước tiền từng bước trước khi chạy; bước làm tổng > 0,37 ⇒ báo A trước.
1. **Phần kín — C chạy** (đã khoá 13:17, report §5): `python -m evaluation.full_corpus_eval chuoi ../data/phase_9/bo_do_b3/chuoi_sealed.jsonl --ben nho|doc_lap|tran --out <thư mục C> --khong-in-chu` trên commit `46008ed`, rồi `python ../data/phase_9/b3/tools/cham_chuoi.py may|export|analyze <thư mục> <bo>` (judge do C gửi; brief judge **phải dặn ghi "item"**). B **không mở** `chuoi_sealed.jsonl`, chỉ nhận số đếm Q3–Q6. Kín ngược chiều ⇒ luật "kết quả âm" của plan.
2. Sau số kín: luật giữ / gỡ (plan §4) ⇒ cập nhật report.
3. **Q10 cổng:** uvicorn cổng riêng, bản sao `settings.yaml` bật `nho_hoi_thoai`; 2 chuỗi 3 lượt qua cookie thật (`curl -c/-b`, `/api/chat` + stream); "cuộc mới" xoá lịch sử; header `HttpOnly` / `SameSite=Strict`; log `chat_metrics` = số lượt; grep tên / câu hỏi / `conversation_id` trong log = 0; 1 ca `curl -m`; TaskStop. Báo A trước khi đo latency (W31).
4. **Bước 8 giao diện — User chọn Bản 1 "Huế hiện đại"** (13:11 03/11; `data/giao_dien_v2/mau/1.html` sha `2952d57f3a92` + README cùng thư mục): khung nhiều lượt, nút "Cuộc trò chuyện mới" (gọi `POST /api/conversation/new`), thẻ "đang tìm", câu khẩn cấp, gợi ý 5 chủ đề, D9 (c) số trích dẫn hiển thị 1..k. Giữ CSP (CSS / JS ra file, không inline, 0 tài nguyên ngoài), tắt chuyển động khi giảm chuyển động, tương phản AA; **không thêm gói npm** (cần ⇒ hỏi A). Playwright ảnh laptop + điện thoại vào cổng. Rồi mới bật `nho_hoi_thoai: true`.
5. Commit report + C review nhánh `10ec9a2..<cuối>` ⇒ A merge.

## Đang khai báo sửa
- **B138 (B3b, A giao): một câu vào `ASSISTANT_HISTORY_NOTE`** — worktree `/tmp/b_p9b3b` (nhánh `p9-b3b` từ `main` `a3dabba`): `backend/llm/full_corpus_prompt.py`, (test) `backend/tests/test_b3_memory.py`. Không mở `data/phase_9/bo_do_b3b/`. Dữ liệu: `data/phase_9/b3b/` (private). Worktree cũ `/tmp/b_p9b3` đã gỡ.
- **B137 (A giao 18:04 03/11/2026 ghi nhận): bước 8 giao diện Bản 1** — worktree `/tmp/b_p9b3` (`p9-b3`, tạo lại): `frontend/src/App.jsx`, `frontend/src/index.css`, `frontend/src/stream.js`, `frontend/src/markdown.js`, `frontend/index.html`, (nếu cần) `backend/tests/test_static_ui.py`. Không sửa backend / lời dặn / `settings.yaml`. Ảnh + script Playwright: `data/phase_9/b3/giao_dien/` (private).
- nhánh `p9-b3` (`/tmp/b_p9b3`): `backend/api/conversations.py` (mới), `backend/api/app.py`, `backend/api/routes/chat.py`, `backend/llm/assistant.py`, `backend/llm/generator_openai_full_corpus.py`, `backend/llm/full_corpus_prompt.py`, `backend/retrieval/full_corpus_context.py`, `backend/evaluation/full_corpus_eval.py`, `backend/config/settings.yaml`, `backend/tests/test_b3_memory.py` (mới), `backend/tests/test_b2_tool_loop.py`; (bước 8) `frontend/`.
- `data/phase_9/b3/` (private); `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md` (working tree `main`, chưa commit).

## Phiên tối 03/11 (18:14 03/11/2026)
- **B137 bước 8 giao diện Bản 1: xong** — `p9-b3` `291b459` (chỉ `frontend/src/`, đã push); Playwright server thật lần 2 đạt (CSP 0, ngoài 0, D9 (b) (c), bấm nguồn lượt cũ, khẩn cấp, lỗi + Thử lại, cuộc mới, điện thoại, giảm chuyển động) — report §2b, §4b; ảnh `data/phase_9/b3/giao_dien/anh/`. Tiền 0,0035.
- Số kín C146 đã nhận + ghi report §5b: mọi luật đạt **trừ Q5 ngoài kho chờ A quyết** (C: lỗi nhãn). Tiếp: A quyết Q5 ⇒ Q10 cổng (nhớ bật trên bản sao settings, cả giao diện) ⇒ bật `nho_hoi_thoai` ⇒ C review `10ec9a2..` ⇒ A merge.
- Report `b136_b3_implementation.md` sửa ở working tree `main` (A commit `e00e752`).
- **Q10 cổng: xong 18:21 03/11/2026, đạt** (report §4c; `data/phase_9/b3/q10/`, nhớ bật qua `app_nho.py` — không sửa `settings.yaml`); câu gợi ý lễ hội đổi `b156f92` (A quyết). Tiền Q10 0,0047. K-N2 chạy lại có ngữ cảnh ⇒ trích dẫn trỏ sai ⇒ **sàn Q5 phạm ⇒ cờ nhớ KHÔNG bật** (A báo 18:23 03/11/2026; report §5b). A trình User hướng (A khuyên B3b trên bộ chuỗi mới C viết). B chờ: không sửa settings / lời dặn; chỉ đọc chỗ lời dặn nhớ để chuẩn bị phương án. Report + STATUS chưa commit (A commit).
- C147 review dải `10ec9a2..b156f92`: **ready_for_user_confirmation** (merge với cờ nhớ tắt; m-3 đóng 18:27 03/11/2026, report `1c4459e8d80d`). B chờ A merge / User chọn hướng B3b.

- **B138 (B3b PA1): `p9-b3b` `1ed7b34` (đã push)** — câu dặn lịch sử sha `64e347d5df58`; đã thấy: Q3 6/6, Q5 0/0, Q6 0, Q8 14 đạt; **Q4 20 lượt +0,50 [−0,15; +1,20] KHÔNG đạt** (B3: +0,65 [+0,15; +1,25]); ca dò tự viết 9 chuỗi không tái hiện lỗi. Report `report_agent/2026-11-02_phase_9_code/b138_b3b_implementation.md` (18:45 03/11/2026, chưa commit). Tiền B138 ≈ 0,089 ⇒ B3 ≈ 0,385 / 0,50. **Chờ A quyết** (a) thử `nho_cau_tra_loi: false` / (b) chuyển C bộ mới / (c) gỡ.

## Phiên 03/11 đã xong
| Việc | Kết quả |
|---|---|
| B131 hoàn tất B1 | `dcd1519`, cổng đạt; A merge `f01c032` |
| B132 / B135 plan B2 / B3 | B2 bản 3 `efa27cb8207c`; B3 bản 2 `cd099ec0a00e` (A duyệt) |
| B133 review README | `b133_readme_review.md` changes_requested 0 / 3 / 7 |
| B134 code B2 | B2b `tim_them` giữ; cổng Q9 đạt; A merge `00d670e` |
| B136 code B3 (dở) | Q1 PASS · Q2 2 vòng ⇒ D6 hẹp giữ (từ chối 4, P0_sai 0) · Q3 6 / 6 · Q4 +0,65 [+0,15; +1,25] · Q5 0 / 0 · Q6 tụt 0 · Q8 max 167 < 512 · khoá `46008ed` |

## Tiền paid (B, 03/11, giá đủ)
B131 0,0029 · B134 (B2) ≈ 0,255 (gồm cổng Q9) · B136 (B3) ≈ 0,255 ⇒ **≈ 0,513 USD** (phiên trưa). Phiên tối: B137 0,0035 + Q10 0,0047 = 0,0082. Judge: quota Claude. Không gọi `agy`.

## Bẫy đã gặp — đọc trước khi làm
- (03/11 tối) `full_corpus_eval chuoi --out` là **đường dẫn file** `.jsonl` (không phải thư mục) ⇒ chạy hai bên cùng `--out <dir>` thì bên sau ghi đè bên trước (mất lượt nho dò, 0,0057 USD). Luôn `--out <thư mục>/<bên>.jsonl`.
- (03/11) **Brief judge thiếu "ghi item / case_index"** ⇒ file điểm không ghép được (`KeyError`); phải ghép lại theo thứ tự dòng. Mỗi brief judge ghi rõ khoá đầu ra gồm id mục, dù rubric không có.
- (03/11) Chấm thước an toàn với **ngữ cảnh = đáp án mẫu** (không phải ngữ cảnh thật) ⇒ ý đúng theo kho bị gắn "không có" ⇒ đọc kèm `grep_kb.sh` trước khi kết luận.
- (03/11) Lời dặn "chỉ nêu điều có trong Bằng chứng; không thêm lời khuyên chung" làm model **dè dặt**: từ chối nhầm tăng, bỏ cả lời khuyên có trong nguồn, mở đầu cụt "Có." — judge an toàn không bắt các lỗi này ⇒ **đọc chữ câu bị đổi**, đếm trên mọi lần sinh. Chặn đúng loại lỗi (lưu ý an toàn không nguồn), không chặn chung.
- (03/11) Sinh lại phía mốc của một đợt trước: lời dặn chung đã đổi trong worktree ⇒ chạy mốc từ code `main` (đợt trước), không từ worktree mới.
- (03/11) Chạy script `data/…/tools/*.py` từ `backend/` cần `PYTHONPATH=$PWD` (thiếu ⇒ `No module named 'core'`, 0 USD nhưng mất một lượt).
- (02/11 tối) **Luật mẫu chữ viết trên 14 câu đã thấy khớp quá sát:** kín bắt 0 / 8, chặn nhầm 2 / 8 ⇒ cờ tắt. Bài học: luật tất định cần bộ câu đã thấy lớn + đa dạng cách gõ trước khi khoá; 0 / 249 chặn nhầm trên phần đã thấy không nói được gì về câu khó kín.
- (02/11 tối) Thước C93 (ngày) viết cho chatbot **không** được báo ngày ("nêu hôm nay thứ…" ⇒ L1) ⇒ không dùng nguyên văn cho bên có dòng ngày; sửa thước trước khi đo lại.
- (02/11 tối) Judge P5: `do_cuoi.py` + `DO_CUOI_DIR=<thư mục mới>` dùng lại được; 13 lô × ~35 s, 3 sub-agent một lúc ⇒ ~5 phút; mỗi lô một file `scores_NN` ⇒ chạy tiếp được. Câu tụt sát ngưỡng ⇒ kiểm "lần gọi trả lời giống byte mốc" (0 USD) trước khi tính tốn tiền A/A.
- (02/11 tối) Kiểm giống byte khi có nhiều lần gọi model / lượt: lấy **lần bắt cuối** (trả lời) — lần định tuyến bị bắt trước sẽ ném lỗi ⇒ lõi đi `tro_ly_hue` ⇒ vẫn ra đúng lần gọi trả lời.
- (02/11) Mẹo dò tiến trình không tự khớp: `pgrep -f "[u]vicorn …"` (ký tự đầu trong ngoặc) — B124 [Chạy]: mẫu thường khớp thêm chính shell đang dò, mẫu ngoặc thì không. Tắt server tạm: TaskStop / PID đã ghi, không `pkill -f`.
- (02/11) Tool chặn `sleep` dài trong lệnh thường ⇒ tiến trình mẫu / chờ dùng `run_in_background`; script phân tích dùng mã `backend/` từ `/tmp`: chạy từ `backend/` với `PYTHONPATH=.`.
- (02/11) SDK 0.19.4: lượt gọi công cụ không phát `output_text.delta`; `on_llm_end` có cả khi stream; prompt < ~1.024 token ⇒ token đệm 0 (B123).
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
- Phiên 02/11 tối + 03/11 sáng (B129–B135): `git show 737f7a7:session_prompt/sessions/STATUS_B.md`.
- Phiên 01/11 (S1–S4, B107–B120): `git show 9c86a98:session_prompt/sessions/STATUS_B.md`.
- Phiên 31/10 (B99–B106): `git show f34cb7f:session_prompt/sessions/STATUS_B.md`. Phiên 30/10: `session_prompt/archive/STATUS_B_LICH_SU_2026-10-30.md`; 29/10: `…_2026-10-29.md`.
