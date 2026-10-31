# B106 — Codex review spec streaming một lần (W33) + lọc finding

Người chạy / lọc: B (Claude Opus 5.5) · Date: 12:06 31/10/2026 (`date`) · 0 USD (gói tài khoản ChatGPT của User).
Spec được review: `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 3 **`cd44744ea3d7`** (chưa commit; B kiểm phần đổi so với `e243371b57eb`: chỉ thêm câu "gọi lại
`result.stream_events()` — iterator mới" ở §4.5 bước 3; 217 dòng; quét trùng 0). Review Claude trước đó: `b105_review.md` (B, 2 vòng, ready `96bcc907886b`).
Gói chạy: `data/tinh_nang_moi_2026-10-27/b104_codex_review_spec.md` (private). Kết quả thô của Codex là **dữ liệu**: private ở
`data/tinh_nang_moi_2026-10-27/2026-10-31-streaming-design_review_codex/` (`review_codex.md` `1e0fa4b558d7`, `codex.jsonl`, `lenh_codex.txt`, `usage.json`).

## 1. Lượt chạy

| Mục | Giá trị |
|---|---|
| Lệnh | `codex exec -m gpt-6-luna -c model_reasoning_effort="high" -s read-only --ephemeral -C <worktree sạch> --json -o …` (không `--search`) |
| Worktree | `git worktree add --detach /tmp/codex_review_spec_wt main` (`16f482a`) + chép spec ⇒ sha bản chép `cd44744ea3d7`; không `data/`, kho, `.env`; gỡ sạch sau khi chạy (`git status` trống trước khi gỡ) |
| Thời gian | 58 s, mã thoát 0 |
| Token | vào 271.598 (đệm 225.664), ra 6.331 (suy luận 4.675) |
| Lệnh shell | **14**, B đọc hết: đều là `cat` / `nl -ba` / `sed -n` / `wc -l` / `pwd` trên file **trong** worktree (spec, `chat.py`, `citations.py`, generator, `app.js`, `index.html`, `full_corpus_eval.py`, `settings.yaml`, `api/app.py`, `pyproject.toml`, `Session_Prompt.md`). Bộ lọc "lệnh trỏ ra ngoài": **0** |
| Kết luận Codex | `changes_requested`, 2 finding major |

## 2. Lọc từng finding (B tự kiểm bằng code thật)

| Codex | Nội dung (tóm) | B kiểm | Phân loại | Mức B đề xuất |
|---|---|---|---|---|
| M-1 | Spec không nói nhánh nào bắt việc hủy và gán `outcome = client_disconnected` trước khi `finally` ghi log; `metrics` khởi tạo toàn `None` | `chat.py:65` `metrics = dict.fromkeys(METRIC_FIELDS)` ✓; spec §4.5 / §4.6 chỉ liệt kê `outcome` mới, không nói chỗ gán. **B thêm:** §4.3 bước 5 ghi "`gen()` **tự bắt mọi lỗi** rồi phát `error` + `done`". Nếu người làm hiểu "mọi lỗi" là `BaseException` thì sẽ nuốt luôn `CancelledError` (probe B105: việc hủy đến dưới dạng `asyncio.CancelledError`), rồi cố `yield` lên kết nối đã đóng, và model có thể chạy tiếp ⇒ tốn tiền. | **đúng — mới** (B105 không bắt) | **minor**: thiếu chỉ dẫn; C7 ca ngắt sẽ bắt khi chạy thật. Nên sửa: "nhánh `except asyncio.CancelledError`: gán `client_disconnected`, token `None`, **raise lại**; nhánh bắt lỗi chung chỉ bắt `Exception`" |
| M-2 | 422 do FastAPI kiểm thân request xảy ra **trước** handler ⇒ không có dòng `chat_metrics`; cam kết "một dòng mỗi lần gọi" không phủ ca này | `ChatRequest` (`chat.py:36-38`): `str_strip_whitespace=True`, `min_length=1`, `max_length=500` ⇒ thân rỗng / toàn khoảng trắng / > 500 ký tự bị trả 422 ở `api/app.py:148-159` (test `test_api_chat.py:36-48`), không vào `chat()` ✓. **B thêm (quan trọng hơn):** spec §7 dùng đúng ca "thân rỗng / quá dài ⇒ 422" để kiểm **lỗi trước luồng** của cách (b). Hai ca đó không chạy tới nhánh trước luồng của route (nhánh `if not query` ở `chat.py:88-89` gần như không thể chạy tới), nên cách (b) **không** được kiểm bằng ca đó. Các nhánh còn lại (503 / 409 tìm, 500 context, 502 generator chưa sẵn sàng) chỉ có khi gặp thật — tạo ra là đổi môi trường (§8). | **đúng — mới** (B105 không bắt) | **minor**: (i) §4.6 / C4 / C7 ghi "một dòng mỗi lần gọi **vào handler**" — hành vi hôm nay, không đổi; (ii) §7 ghi rõ ca 422 chỉ kiểm lớp FastAPI; nhánh trước luồng của route = test logic thuần (gọi hàm kiểm trước với `state` thật ở trạng thái chưa sẵn sàng **chỉ khi** có được bằng đường thật) hoặc ghi **giới hạn chưa kiểm bằng đường thật** |

"Đã kiểm, không thấy vấn đề" của Codex (§4.8 khác biệt, `.strip()`, DOMPurify, chính sách log): B đối chiếu — khớp với kết luận B105 ✓. "Không kiểm được" của Codex: mọi hành vi
thư viện (Starlette hủy, Agents SDK, `format_sse_event`) — đúng, vì worktree cố ý không có `.venv`.

## 3. So với review Claude (kết quả W33)

- **Codex bắt được 2 điều Claude không bắt:** đều về độ phủ của log / `outcome` (ca ngắt; 422 trước handler). Đi theo M-2, B tìm thêm: ca test "lỗi trước luồng" ở §7 không chạy tới
  nhánh cần kiểm. Đây đúng là loại lỗi W33 muốn bắt — đọc kỹ code tracked, khác cách người viết / người kiểm cùng họ Claude.
- **Codex không bắt (và không thể bắt):** finding chính của B105 (M-1: anyio hủy ở mọi `await` trong `finally`) cần chạy thư viện thật — worktree không có thư viện, Codex tự ghi
  "không kiểm được". Codex review **bản đã sửa**, nên không so được với m-1…m-4 của B105.
- **Chi phí:** 58 s, 0 USD, 14 lệnh đọc trong worktree, không lệnh ra ngoài.
- **Đề xuất cho sổ cải tiến (A quyết):** W33 cho kết quả **dương nhỏ** (2 minor mới, có thật). Ý cho lần sau, nếu giữ: (1) chạy Codex **song song** với review Claude trên cùng bản,
  để so được cả finding đã sửa; (2) cho phép một bản `.venv` chỉ đọc (hoặc mã nguồn thư viện) nếu muốn Codex kiểm được hành vi thư viện — đổi rủi ro / phạm vi, cần User duyệt.

## 4. Việc tiếp

- Hai minor ở mục 2 ⇒ C sửa spec (một lượt), báo sha; B kiểm phần đổi (không chạy Codex lần 2 — A quyết).
- Phần `TBD` (mức chuẩn ngành "chữ đầu tiên"): A điền ⇒ B kiểm phần đổi.
- Sau đó User duyệt sha.

---

## 5. Kiểm phần sửa — spec bản 4 `cf1ae9ef6c2c` (12:10 31/10/2026, `date`)

Decision: **ready_for_user_confirmation** (2 minor Codex đóng; phần `TBD` chưa review — A điền sau). Không chạy Codex lần 2 (A quyết).

| Codex | Chỗ sửa ở bản 4 | Đóng? |
|---|---|---|
| #1 ngắt | §4.3 bước 5: "bắt mọi lỗi **thuộc `Exception`**"; nhánh `except asyncio.CancelledError` riêng ⇒ `outcome = client_disconnected`, token `None`, **raise lại**; không `yield` lên kết nối đã đóng; dọn ở `finally` theo §4.5 | ✓ |
| #2 422 | §4.1 thêm dòng 422 của FastAPI trước handler (`api/app.py:148-159`); §4.6 / C4 / C7 "một dòng mỗi lần gọi **vào handler**", 422 FastAPI không có dòng log (giữ hành vi hôm nay); §7: ca 422 chỉ kiểm lớp FastAPI, **không** kiểm nhánh lỗi trước luồng của cách (b); 503 / 409 / 500 / 502 ⇒ giới hạn §10 + "đọc diff phải thấy route stream dùng chung đoạn kiểm trước model với route JSON" | ✓ |

- Ngoài chỗ khai báo ở dòng "Bản 4", B không thấy chỗ đổi khác (224 dòng; đọc lại §4.1, §4.3, §4.6, §6 C4 / C7, §7, §10). Quét trùng 0; 0 dòng có khoảng trắng cuối.
- C **không** thêm test logic dựng `app.state` "chưa sẵn sàng" cho 503 / 502 (lý do: gần "dựng lỗi giả" + A đã quyết không thêm chỗ nối chỉ dùng khi test) — B đồng ý, khớp quyết định A.
  **Ghi cho A (không phải finding):** repo đã có một tiền lệ đường "gần thật" cho 503: `backend/tests/test_startup_model_missing.py` (tiến trình con với `HF_HUB_OFFLINE=1` + `HF_HOME` rỗng ⇒
  503 `retrieval_unavailable`, không mock; User chạy bằng `!` vì auto mode chặn). Nếu A muốn route stream có một ca 503 thật thì có thể chạy cùng kiểu đó trên route mới. Đây là
  quyết định về luật §8 ("đổi môi trường"), không tự áp.
- Câu bất biến: spec vẫn chỉ là tài liệu; `POST /api/chat` giữ nguyên (§1, §3) ✓.
