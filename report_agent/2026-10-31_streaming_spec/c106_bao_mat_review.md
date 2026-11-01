# Review: C106 — Rà bảo mật một lần lúc đóng gói Phase 1–8

Decision: changes_requested
Người kiểm: agent con ngữ cảnh mới do A giao (Claude Opus 5.5)
Date: 11:52 01/11/2026 (`date`)
Canonical guide: `skills/agent-security-review/SKILL.md` (mục 1, 2, 3, 4, 5, 7, 8); mức theo `skills/risk-gated-agent-review/SKILL.md`
Implementation report: `report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` — sha256 `2ef499b91a594204ea0a62ae32de49d5cfd56aab14898d509082e43bb06ef1d9` (12 ký tự đầu `2ef499b91a59`, khớp sha A ghi trong `CURRENT_HANDOFF.md`)

## 1. Phạm vi đã review

- Đọc toàn bộ báo cáo C106 và hai skill.
- Code đọc bằng `git show`: `887cbc5` (đầu nhánh `s1-loi-chung`) `backend/api/routes/chat.py`, `backend/llm/answer_stream.py`, `backend/core/logging_setup.py`,
  `backend/config/logging.yaml`, `backend/llm/grounded_answer.py`, `backend/llm/evidence_recorder.py`; `830df0e` `backend/api/app.py`,
  `backend/llm/generator_openai_full_corpus.py`, `backend/llm/full_corpus_prompt.py`, `backend/llm/citations.py`, `backend/config/settings.yaml`;
  `bbbdbf9` `generator_openai_full_corpus.py` + `git diff 830df0e bbbdbf9 -- chat.py generator…`; `git diff --stat 830df0e 887cbc5`; `pyproject.toml`, `uv.lock` (phiên bản).
- Working tree: `frontend/app.js`, `frontend/index.html`, `frontend/vendor/` (phiên bản + danh sách thẻ mặc định của DOMPurify), `docker-compose.yml`, `.gitignore`,
  `.githooks/pre-commit`, `.claude/settings.json`, `.claude/settings.local.json` (chỉ lọc các luật liên quan, không chép đường dẫn), `.claude/hooks/*.sh` (đầu file),
  `scripts/tra_web_codex.sh`, `~/.claude/settings.json` (chỉ tên khoá cấp 1 + `permissions`).
- Log: chỉ `grep -c` trên `backend/logs/application.log` (không in dòng nào).

## 2. Findings

Không có `blocker`. Có **1 `major`**, 6 `minor`.

### M-1 (major) — Mục 7 "chính coding agent" thiếu: chưa kê bộ ba của coding agent, bỏ sót `settings.local.json` và đường web của Codex

- **Vị trí:** báo cáo R10 (`c106_bao_mat_dong_goi.md:37`), §1 (chỉ kê bộ ba của chatbot).
- **Yêu cầu:** skill mục 7 + mục 1: coding agent cũng phải kê (a) riêng tư · (b) không tin cậy · (c) đường ra; skill gọi tên `git push` là đường ra phải hỏi User trước.
- **Bằng chứng (đã kiểm):**
  1. `.claude/settings.local.json` (file máy, không theo dõi git — `~/.config/git/ignore:1`) có 93 luật `allow`, trong đó `Bash(git push *)`, `Bash(git add *)`,
     `Bash(uv run *)`, `Bash(python3 *)`, `Bash(echo *)`, `Bash(docker compose *)`, `WebFetch(domain:github.com)` và vài luật `Read` tới thư mục ngoài dự án.
     ⇒ đẩy lên repo **public** được tự duyệt, không qua hỏi; mọi script Python chạy được không hỏi (đọc được `.env` mà không cần `cat`).
     Báo cáo chỉ đọc `.claude/settings.json` và kết luận "minor", đề xuất thêm deny `cat .env` — đề xuất này không đóng được đường `uv run` / `python3`.
  2. `scripts/tra_web_codex.sh:50-51`: Codex chạy `--search` + `-s read-only`; đầu file (`:8`) đã ghi read-only **không chặn đọc file ngoài thư mục**; lệnh shell chỉ được
     **đếm sau khi chạy** và cảnh báo (`:60-64`, `:68`), không chặn. Đủ bộ ba ngay trong một lượt Codex: đọc được file máy (kể cả `.env`) · trang web là nội dung không tin cậy
     (có thể cài lệnh) · câu tìm kiếm / URL mở trang là đường ra. Báo cáo chỉ nêu rủi ro theo hướng "yêu cầu gửi đi phải công khai", chưa nêu hướng trang web cài lệnh
     khiến Codex đọc file máy rồi nhét vào câu tìm (suy luận theo cơ chế, chưa thử — không được thử).
  3. Quan sát thêm trái với câu R10 "không cấm `Bash(cat .env)`": trong lượt review này 3 lệnh Bash có nhắc `.env` (`ls -l .env`; một lệnh ghép có `ls -l .env`;
     `stat … /home/…/.env`) đều bị hệ thống quyền từ chối, còn `ls -l backend/logs/` thì chạy. Có một lớp rào máy với lệnh shell nhắc tên file — người kiểm **không** xác định được
     cơ chế (luật `Read` deny áp cả cho Bash, hay "phải hỏi" ⇒ agent con bị từ chối tự động).
- **Tác động:** kết luận mục 7 ("minor", rào chỉ thiếu deny `cat`) dựa trên bức tranh thiếu; đường ra quan trọng nhất của coding agent (push lên repo public) đang tự duyệt bằng máy,
  ngược với luật chữ "commit / push luôn hỏi trước".
- **Tiêu chí đóng (quan sát được):** báo cáo có một mục / hàng "bộ ba của coding agent" kê đủ ba vế với `file:dòng` (gồm `settings.local.json` các luật trên — không chép
  đường dẫn ngoài dự án — và `tra_web_codex.sh`), mức cho từng hàng, và đề xuất tương xứng để A trình User chọn (ví dụ: bỏ `Bash(git push *)` khỏi `allow` để push lại hỏi,
  kèm hệ quả là User phải bấm duyệt mỗi lần push — đối chiếu memory "chạy lệnh tự làm sau khi User đồng ý"; ghi giới hạn của Codex web vào "giả định an toàn" của coding
  agent). R10 sửa câu "không cấm `cat .env`" cho khớp quan sát ở ý 3 (hoặc ghi rõ chưa xác định cơ chế). Không yêu cầu sửa cấu hình trong vòng này.

### m-1 (minor) — Phạm vi ghi commit cũ

- **Vị trí:** `c106_bao_mat_dong_goi.md:4`.
- **Bằng chứng:** đầu nhánh `s1-loi-chung` là `887cbc5` (commit 11:41 01/11, sau giờ báo cáo 11:39); `git diff --stat 830df0e 887cbc5` chỉ đổi `backend/llm/answer_stream.py`
  (+5/−1, giữ nửa đầu cặp surrogate) và một test — người kiểm đọc, **không** ảnh hưởng bảo mật. `bbbdbf9` dựng trên `830df0e`, không trên `887cbc5`.
- **Tiêu chí đóng:** dòng phạm vi ghi `887cbc5` + một câu "delta `830df0e→887cbc5` không đổi đường dữ liệu / log / sự kiện".

### m-2 (minor) — Vài `file:dòng` lệch

- `chat.py:24-29` "trên `830df0e`" (R4) là khối import; chính sách log ở `830df0e:chat.py:35-36` (`:24` là số dòng trên `main`).
- `generator_openai_full_corpus.py:147` (§1) ⇒ `:145` trên `830df0e` (`:157` trên `bbbdbf9`).
- `chat.py:46-48` (R5) ⇒ hai chuỗi lỗi cố định ở `:47-48` (`:46` là `STREAM_DRAIN_SECONDS`).
- `tra_web_codex.sh:57-61` (R10) ⇒ đếm ở `:60-64`, cảnh báo ở `:68`.
- Mọi tham chiếu còn lại người kiểm mở và **khớp**: `chat.py:43, :53, :56-60, :222-266, :269-328, :321, :400`; `app.py:129-174`; `generator…:89-90, :128, :156, :176, :246`;
  `full_corpus_prompt.py:8-10`; `citations.py:19-34`; `settings.yaml:56`; `docker-compose.yml:7-8`; `.gitignore:11, :23`; `.githooks/pre-commit:16, :29`; `pyproject.toml:27`;
  `frontend/app.js:72`; `index.html` không có CSP.
- **Tiêu chí đóng:** 4 tham chiếu trên sửa đúng commit + dòng.

### m-3 (minor) — R2 thiếu đường tải ngoài khác ngoài `<img>`; đề xuất `FORBID_TAGS: ['img']` không đủ

- **Vị trí:** R2 (`c106_bao_mat_dong_goi.md:29`).
- **Bằng chứng (đã kiểm trên `frontend/vendor/purify.min.js`, DOMPurify 3.4.15):** danh sách thẻ mặc định có `form`, `input`, `button`, `img`, `video`, `source`, `style`;
  danh sách thuộc tính mặc định có `style`, `srcset`, `action`. `marked` 18.0.12 để nguyên HTML thô ⇒ câu trả lời chứa `<form action="http://…">`, `<style>` hay
  `style="background:url(…)"` vẫn qua `app.js:72`. Suy luận: chặn `img` không chặn tải qua CSS `url()` / `<video>` / gửi form ra ngoài; CSP `default-src 'self'; img-src 'self'`
  chặn được tải ảnh / CSS / media nhưng **không** chặn gửi form nếu thiếu `form-action`. Thêm: ở route stream, chữ `delta` hiện **trước** bộ kiểm trích dẫn
  (`887cbc5:chat.py:367-376`) ⇒ ảnh trong chữ bị rút lại (`retracted`) vẫn đã được tải.
- **Tiêu chí đóng:** đề xuất R2 nêu (a) CSP là lớp chính, có thêm `form-action 'none'` (hoặc `'self'`); (b) DOMPurify dùng danh sách thẻ cho phép kiểu Markdown
  (`ALLOWED_TAGS`) thay vì chỉ cấm `img` — hoặc ghi lý do chọn cách khác; (c) S3 phải sanitize mỗi lần vẽ lại chữ đang stream. Không bắt buộc chặn mọi link ngoài
  (link bấm tay ít rủi ro hơn tải tự động; chặn hết thì mất link hữu ích trong câu trả lời — ghi lựa chọn cho A).

### m-4 (minor) — §3 "giả định an toàn" nói hơi quá ở hai chỗ

- **Vị trí:** `c106_bao_mat_dong_goi.md:43, :45`.
- **Bằng chứng:** (1) "OpenAI không lưu câu trả lời để truy xuất lại (`store=False`)": đúng với `store=False` (`830df0e:generator…:128`), nhưng người đọc thường dễ hiểu là
  "OpenAI không lưu gì"; chính báo cáo R7 ghi chính sách lưu giữ phía OpenAI **chưa kiểm**. (2) "API nghe `127.0.0.1`" chỉ đúng khi chạy lệnh trong tài liệu
  (`LUONG_HOAT_DONG_HE_THONG.md:123` trên `887cbc5`, không có `--host` ⇒ mặc định của uvicorn) — code không ép.
- Các ý khác của §3 người kiểm thấy **khớp** code: model không công cụ (Agent không khai báo `tools`, `max_turns=1`), không bí mật trong ngữ cảnh, log runtime không ghi chữ
  (`logging.yaml` mức INFO, không logger nào ghi body; `app.py:150, :163` chỉ ghi `url.path`), Qdrant chỉ `127.0.0.1`.
- **Tiêu chí đóng:** (1) thêm "OpenAI vẫn có thể giữ dữ liệu một thời gian theo chính sách API của họ — chưa kiểm"; (2) "khi chạy đúng lệnh trong tài liệu (không đặt `--host`)".

### m-5 (minor) — R1 bỏ sót DNS rebinding; câu về CORS nói thiếu

- **Vị trí:** R1 (`c106_bao_mat_dong_goi.md:28`).
- **Bằng chứng / suy luận (chưa chạy):** `830df0e:app.py:129-174` không có kiểm `Host` (không `TrustedHostMiddleware`). Một trang web lạ dùng tên miền trỏ lại `127.0.0.1`
  (DNS rebinding) thành "cùng nguồn" với API ⇒ gọi được `/api/chat` (tốn tiền thật, đọc được trích đoạn kho private) dù API chỉ nghe máy cục bộ. Ngược lại, câu "trang khác
  không đọc được phản hồi" nói **thiếu**: không có CORS thì trang khác cũng không gửi được JSON (cần preflight), và FastAPI 0.141.1 từ chối body không phải JSON ⇒ gửi
  `text/plain` chỉ nhận 422, chưa tới model (suy luận theo hành vi FastAPI, chưa thử).
- **Mức:** minor (máy một người, thiệt hại tối đa nhỏ, cần User mở trang độc đúng lúc server chạy).
- **Tiêu chí đóng:** R1 thêm một câu về DNS rebinding + cách rào rẻ (kiểm `Host` chỉ `localhost` / `127.0.0.1`) vào danh sách điều kiện trước deploy hoặc "chưa rào" ở §3;
  sửa câu CORS cho đúng. Không yêu cầu sửa code ngay.

### m-6 (minor) — §1 (c) / R7 chưa kê đường ra phụ không mang chữ người dùng

- **Bằng chứng / suy luận:** `docker-compose.yml` không tắt telemetry của Qdrant (theo tài liệu Qdrant, telemetry ẩn danh bật mặc định — **chưa kiểm** trên container);
  model nhúng tải từ Hugging Face nếu lệnh chạy thiếu `HF_HUB_OFFLINE=1` (log hiện có 3 dòng nhắc `huggingface.co`, chỉ đếm). Không đường nào mang câu hỏi / kho ⇒ không
  phải rủi ro dữ liệu, chỉ cho đủ danh sách mục 5.
- **Tiêu chí đóng:** §1 (c) hoặc R7 có một dòng "đường ra phụ: telemetry Qdrant (chưa kiểm), HF hub khi thiếu biến offline — không mang chữ người dùng".

## 3. Cách người kiểm chạy lại thật

- `sha256sum report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md`; `git log --oneline` hai nhánh; `git diff --stat 830df0e 887cbc5`; `git diff 830df0e bbbdbf9 -- …`.
- `git show <commit>:<file> | cat -n` cho các file ở §1; `git grep 'Received question' 830df0e|bbbdbf9 -- backend` (0 / 0); `git grep -i gradio 887cbc5 -- backend` (0);
  `git grep 'logger\.' 887cbc5 -- backend/api backend/llm backend/retrieval backend/core`.
- `grep -c` trên `backend/logs/application.log`: tổng 1351 dòng; `Received question` 22; `chat_metrics` 58; logger `chat` 144; `sk-` 0; `bearer` 0; `api_key` 0;
  `api.gradio.app` 5 dòng; `chat_stream_drain` 0.
- `head`/`grep -o` trên `frontend/vendor/purify.min.js` (bản 3.4.15, danh sách thẻ / thuộc tính mặc định), `marked.umd.js` (18.0.12); `grep -c Content-Security frontend/index.html` (0).
- Lọc `.claude/settings.local.json` bằng `python3 -c` (chỉ in luật khớp mẫu push / python / uv run / curl / WebFetch); `git check-ignore -v .claude/settings.local.json`; `git config core.hooksPath` (`.githooks`).
- `uv run python .githooks/overlap_scan.py report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` ⇒ `0 trùng`, mã 0; `grep -ciE` tên dự án khác / tên user khác ⇒ 0;
  mẫu secret ⇒ 0; `git diff --no-index --check` ⇒ không cảnh báo khoảng trắng.
- 0 USD, không chạy server, không gọi API, không mở `.env`, không mở file `*sealed*` / Golden.

## 4. Kết quả quan sát

- **R1–R11 hiện trạng:** đúng với code thật, trừ 4 tham chiếu dòng lệch (m-2) và câu "không cấm `cat .env`" (M-1 ý 3). Số đếm log của báo cáo (22 / 58 / 144 / 0-0-0) khớp lần đếm lại.
  R11 "2 request tới `api.gradio.app`": người kiểm đếm được 5 dòng có chuỗi đó; không in dòng nên không phân được thành số request — không coi là mâu thuẫn.
- **Mức:** R1 (minor nay / major khi deploy), R3, R4, R7, R9, R11 minor — hợp lý; R5, R6, R8 "đạt" — hợp lý (route stream: sự kiện chỉ mang chữ trả lời, nguồn được trích, mã /
  thông điệp cố định; log stream chỉ số / cờ / tên lớp lỗi). R10 minor — chưa đủ căn cứ (M-1). R2 minor hợp lý nhưng đề xuất thiếu (m-3).
- **Đề xuất:** không thấy phòng xa — phần lớn là ghi vào "giả định an toàn" hoặc điều kiện trước deploy, sửa gộp vào S3; R9 `chmod 600` chỉ có ích với user khác trên máy
  (không chặn tiến trình cùng user, kể cả agent) — có thể ghi thêm cho rõ.
- **Riêng tư của file báo cáo (public):** không có câu hỏi người dùng / Golden / nội dung kho (quét trùng 0), không tên / số dự án khác, không mẫu secret; ngày giờ log
  cũ chỉ là số đếm. Đạt.

## 5. Giới hạn hoặc phần chưa chạy

- Không kiểm được quyền file `.env` (R9 `-rw-r--r--`): mọi lệnh nhắc `.env` của agent con bị từ chối (M-1 ý 3) ⇒ R9 dựa trên quan sát của C.
- DNS rebinding (m-5), hành vi FastAPI với `text/plain`, telemetry Qdrant (m-6), đường Codex đọc file theo lệnh trang web (M-1 ý 2): suy luận theo cơ chế, chưa thử.
- Không đọc nhánh `s3-giao-dien` (ngoài phạm vi; giao diện stream chưa bàn giao).
- Các giới hạn trên không đổi kết luận: M-1 dựa trên cấu hình đã đọc thật.

## 6. Decision và bước tiếp theo

`changes_requested` — một lượt sửa tài liệu (không sửa code / cấu hình):

1. M-1: thêm mục bộ ba của coding agent (settings.local.json · Codex web) + sửa câu R10 (tiêu chí ở M-1).
2. m-1 … m-6: sửa theo tiêu chí đóng từng mục.
3. Kiểm lại: người kiểm đọc delta báo cáo, mở lại `file:dòng` mới, chạy lại `overlap_scan.py` trên file mới. Bằng chứng code / log ở vòng này dùng lại được nếu các commit
   `887cbc5` / `bbbdbf9` và `.claude/settings.local.json` không đổi.
4. Sau khi đạt: A trình User các đề xuất cần User quyết (R4, R9, R10 / M-1, R11, cách chặn ở R2).

Người kiểm không sửa thay phần việc đang kiểm. A commit/push sau khi đóng.

# Vòng 2 — kiểm bản 2 của báo cáo (agent con ngữ cảnh mới do A giao, 12:14 01/11/2026 `date`)

Decision: **ready_for_user_confirmation** — M-1, m-1…m-6 đóng; không có finding mới.
Báo cáo kiểm: `c106_bao_mat_dong_goi.md` bản 2, sha256 12 ký tự đầu `94ae4e98b673` (tự tính, khớp A gửi). Phạm vi code thêm: `s3-giao-dien` `716ba4d`.

| Finding | Kiểm lại (đã mở thật) | Kết quả |
|---|---|---|
| M-1 | §1b mới đủ ba vế + CA1–CA5 có mức, phương án cho User kèm hệ quả. Dòng luật `.claude/settings.local.json` khớp: `:12` `git add *`, `:14` `git push *`, `:25` `docker compose *`, `:74` `uv run *`, `:77` `echo *`, `:81` `WebFetch(domain:github.com)`, `:93` `python3 *` (chỉ lọc tên luật, không chép đường dẫn ngoài dự án). CA3 dẫn `tra_web_codex.sh:8, :19, :50-51, :60-64, :68` — khớp. CA5 mô tả đúng quan sát vòng 1 và ghi "cơ chế chưa xác định". CA1 / CA3 `major`, CA2 / CA4 / CA5 `minor` — hợp lý; CA3 ghi rõ là suy luận, chưa thử | đóng |
| m-1 | đầu file: `887cbc5` + câu delta; `bbbdbf9` dựng trên `830df0e`; thêm `716ba4d` | đóng |
| m-2 | `830df0e:chat.py:35-36`, `generator…:145`, `chat.py:47-48`, `tra_web_codex.sh:60-64 / :68` — đúng | đóng |
| m-3 | R2 viết lại theo S3. Đã kiểm `716ba4d`: `frontend/app.js:77` `SANITIZE_OPTIONS` (25 thẻ Markdown, thuộc tính chỉ `href` / `title` / `align` / `start`); `:85` mọi lần vẽ lại đều qua `DOMPurify.sanitize(…, SANITIZE_OPTIONS)`, `innerHTML` chỉ dùng ở đó; `backend/api/app.py:33` CSP có `img-src 'self'`, `form-action 'self'`, `object-src 'none'`; `:37` `FrontendStaticFiles` gắn CSP cho trang HTML dưới `/static`, `:163` cho `/`. `form-action 'self'` đủ vì `form` không còn trong danh sách cho phép. Số "0 request ra ngoài, 25 ca" là bằng chứng của `s3_giao_dien_review.md` Vòng 2 (ready) — người kiểm không chạy lại trình duyệt | đóng |
| m-4 | §3 + R7: "khi chạy đúng lệnh trong tài liệu"; "OpenAI vẫn có thể giữ dữ liệu… chưa kiểm". `LUONG_HOAT_DONG_HE_THONG.md:168` (working tree / `main`) đúng là lệnh không có `--host` | đóng |
| m-5 | R1 + §3 + §4: DNS rebinding (ghi suy luận), kiểm `Host` vào điều kiện, câu CORS / 422 sửa đúng | đóng |
| m-6 | §1 (c) + R7: telemetry Qdrant (chưa kiểm), HF hub — không mang chữ người dùng | đóng |
| ghi chú R9, R11 | R9 nêu `chmod` không chặn tiến trình cùng user; R11 ghi cả hai cách đếm | đóng |

**Chỗ sửa có tạo lỗi mới không:**
- `file:dòng` mới đều khớp (bảng trên).
- Không nói quá: §3 ý "trang không tự tải gì" có điều kiện "khi giao diện streaming vào chatbot". Trên `main` hôm nay giao diện cũ (`frontend/app.js:72`) vẫn chưa rào cho tới khi merge S3; R2 và §5 ghi "chờ merge" — đủ.
- §1b (a) có nhắc loại khoá trong `.env`: tên nhà cung cấp lấy từ code (`.githooks/pre-commit`, `backend/…` có `OPENROUTER`), không lộ giá trị.

**Riêng tư (public):** `uv run python .githooks/overlap_scan.py …c106_bao_mat_dong_goi.md` ⇒ `0 trùng`; tên dự án khác / user khác 0; mẫu secret 0; giờ ước 0; `git diff --no-index --check` không cảnh báo.

**Giới hạn:** không chạy lại trình duyệt / server (R2 dùng lại bằng chứng review S3: cùng commit `716ba4d`, đầu vào không đổi); quyền `.env` vẫn không tự kiểm được (R9, như vòng 1). Hai giới hạn này không đổi kết luận.

**Bước tiếp:** A trình User các quyết định: CA1 (push tự duyệt — C khuyên bỏ khỏi `allow`), CA3 (Codex web), CA2, CA4, CA5, R1 kiểm `Host`, R4, R7, R9, R11; R2 đóng theo khi merge S3.
