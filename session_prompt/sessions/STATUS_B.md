# STATUS B — KẾT PHIÊN tối 2026-10-25 22:28 +0700 (mở 18:21; terminal `hue-rag-c3`; A = `hue-rag-77`, C = `hue-rag-7f`)

Agent: Claude Opus 5.5 · Vai: thực thi · User: B làm việc trực tiếp với A, xong báo A, chờ A giao.

## Trạng thái kết phiên
- **File đang khai báo sửa: không.** Không giữ GPU; không server nào chạy (uvicorn port 8011 của cổng 1b đã tắt bằng SIGTERM).
- Working tree lúc kết phiên đang ở nhánh **`dot3`** của C (C đưa về `main`); B **không** đổi nhánh, không commit. File B chưa commit:
  `report_agent/2026-10-25_ra_soat_code/ung_vien_cai_tien_B.md` (untracked — A commit khi tiện) + file này.
- **Phiên sau B làm đầu tiên:** review **toàn nhánh `dot3`** (đợt 3 của C, plan `sua_dot3_plan.md` bản 3 sha `7c8c660558e5`, B review ready §7) khi C báo
  xong — theo `risk-gated-agent-review`, không đọc `STATUS_C`; trọng tâm D1 (sha đoạn toàn kho), D2 (T1 `cefb2d1ad609`), D3 (chuỗi gửi model), D8
  (`git ls-files knowledge-base-hue` rỗng), T-C (User chạy `!`).

## Việc đã xong phiên tối (đều 0 USD trừ ghi chú)
| Việc | Kết quả | File |
|---|---|---|
| B25 rà code dựng index + nền | 21 finding (B-08 rút sau); top 10; 3 sub-agent | `ra_soat_code_B.md` |
| Kiểm chéo top 5 của C | ready; 6 minor R-01…R-06; khai xung đột lợi ích (C-09 bác report G2 của B) | `kiem_cheo_B.md` |
| Sửa B25 theo kiểm chéo của C | R1–R4 đồng ý (B-11 vừa, B-17 thấp…) | `ra_soat_code_B.md` |
| Review C35 gói 1a (citation `[Nguồn n]`) | ready; 1.600 câu 69 → 14, 0 câu đạt thành lỗi | `sua_1a_review.md` |
| B26 gói 4 (tài liệu) + sửa m1–m4 (m3 phản biện đúng) | 16 file; đường dẫn chết ngoài vùng lịch sử 34 → 1; đường dẫn home repo khác 48 → 0; notebook 3 / 3 | `sua_4_implementation.md` (A commit `1b9c126`) |
| Plan gói 1b (3 bản) | quy ước (b) import trần; C review ready; A duyệt `8b36bab7901c` | `sua_1b_plan.md` |
| Review gói 3 (C, 3a / 3b) | ready; so cặp giống byte 5 cặp; chuỗi gửi model giống 25 / 25 | `sua_3_review.md` (A commit `47a4e32`) |
| **Gói 1b (sửa code)** | K1–K7 đạt: nạp đôi 0 ở 11 điểm vào + pytest; T-A / T-B / T-C đỏ → xanh; 198 passed (C-17 không tăng); T1 giống byte; cổng ổn định đạt | `sua_1b_implementation.md` (A commit `1e4acd0`, báo cáo `b60f362`) |
| Review plan đợt 3 (C) | bản 1 changes_requested (M-1 `git mv`); bản 3 ready | `sua_dot3_plan_review.md` |
| Ứng viên cải tiến khâu dựng kho | 10 dòng; QB1–QB4 A ghép vào yêu cầu ChatGPT (câu 7–10); QB5 / #6 chờ User | `ung_vien_cai_tien_B.md` |

## Dở / chờ
- Review nhánh `dot3` (khi C xong đợt 3) — việc đầu phiên sau.
- Việc cũ còn chờ B (từ phiên chiều): review plan E1 của C khi 8.2 chạy lại (plan đổi sha theo C-02 / C-09 / `paired_stats`).
- Rebase `p82-b1` sau 1b: theo `sua_1b_plan.md` §6 (xung đột khối import `retrieval/full_corpus.py`, import `test_full_corpus_retrieval.py`, comment
  `b1.py:23`, chạy lại T1–T2 của B1) — khi 8.2 chạy lại; B là người làm B1.

## Tiền paid phiên tối
- Gói 1b cổng ổn định: 2 lượt `gpt-6-luna` ≈ **0,0004 USD (ước — route không log usage)**. Còn lại 0 USD (review / rà / tài liệu; sub-agent quota).

## Câu hỏi cho A / User
- #6 ứng viên (dense local `bge-m3` / `Qwen3-Embedding-0.6B`): model mới — A hỏi User trong tài liệu thiết kế (A 22:0x).
- QB5 (tra nguồn cho 22 mâu thuẫn kho qua ChatGPT): đưa dữ liệu kho ra ngoài — User duyệt riêng, để đợt build lại (A 22:0x).
- Route API không ghi usage token ⇒ mọi cổng ổn định chỉ ước được tiền (trùng ý C #5) — có làm ở gói sau không?

## File tạm / private
- Thư mục tạm `/tmp/b25*`…`/tmp/b31` (script B, sub-agent) **đã xóa 22:3x** — script cần dùng lại đã chép vào `data/ra_soat_code/tools/`.
- Private dùng lại (không commit): `data/ra_soat_code/` — `sa{1,2,3}_*.md`, `b19_duong_dan_ngoai.md`, `b26_deadrefs_{before,after}.txt`,
  `b1b_pytest_before.txt`, `b1b_tc_{before,after}.txt`, `tools/{deadrefs,edit_notebooks,inventory,dup_modules}.py`.

## Ý cải tiến (giả thuyết, chưa đo — đã đưa vào `ung_vien_cai_tien_B.md` #4, #9, #7, #10)
- Bỏ ràng buộc tokenizer huydang 256 khi build lại (đo thêm Completeness câu nhiều nguồn).
- Đo thời gian khởi động API thật qua `create_app`.
- Build lại không ngừng phục vụ: tên collection / sparse state từ settings (B-06) + cutover + snapshot.
- Chỉ số "trải nghiệm người dùng": câu API trả lỗi = 0 điểm, báo cạnh điểm judge.

## Đã học / bẫy gặp (phiên tối 25/10 — đầu vào vòng cải tiến)
- **Auto mode chặn lệnh dùng `HF_HOME` rỗng** (thử "model không nạp") ở cả B lẫn C ⇒ không thử lại / đổi cách; tách test ra file riêng, ghi lệnh vào plan,
  User chạy `!` trong terminal B (trước / sau sửa). Pytest của B liệt kê file, không gồm file đó.
- **`git mv` sang thư mục bị gitignore vẫn đưa file vào index** (thử repo tạm) ⇒ chuyển dữ liệu private ra khỏi repo: `cp` + `git rm`, kiểm
  `git ls-files <thư mục private>` rỗng; hook pre-commit chỉ là lưới cuối.
- **Regex lồng `(...)+?` với backreference treo Python** (script đổi import, timeout 120 s) ⇒ dừng task, kiểm phần đã ghi (5 file đúng), viết lại bản duyệt
  theo dòng; script sửa code hàng loạt luôn có assert "không đổi nghĩa" (thân `try` bỏ `backend.` = thân `except`) và giữ chuỗi định danh dữ liệu
  (`"backend.scoring.bm25.tokenize:v1"`).
- B ghi "`scripts/` không tồn tại" vì chỉ tìm ở gốc repo ⇒ `find . -name <tên> -not -path './.venv/*'` trước khi kết luận "không có".
- Khẳng định về code chưa đọc (B-04 "chunker đã fail-closed") sai ⇒ chỉ khẳng định sau khi đọc; ghi "chưa kiểm".
- Đo hiệu năng bằng script tự nạp model (B-08) sai vì bỏ qua warm-up thật ⇒ đo qua đường production (`create_app` / service builder).
- Sub-agent gọi scroll Qdrant bằng POST khi brief ghi "GET thì được" ⇒ brief nêu rõ "chỉ GET" hoặc cho phép POST chỉ đọc.
- B dùng `python3` hệ thống để sửa text (vi phạm §10) ⇒ mọi Python bằng `uv run`.
- Test viết trước cho mã HTTP phải kiểm **nguyên nhân** (lớp + thông điệp), không chỉ mã — 503 cũng ra khi Qdrant tắt (P2 plan 1b, m-4 plan đợt 3).
- Đếm "tham chiếu chết" phụ thuộc quy tắc vùng lịch sử ⇒ nhãn phải đọc được bằng máy (banner cố định + `## Hiện hành`), ghi quy tắc trước khi đếm "sau".
- Báo cáo của mình bị bác (C-09 vs report G2 do B viết) ⇒ khai xung đột lợi ích trong review, quyết bằng số đo.

---

## (Lịch sử) Phiên chiều 25/10 — giữ làm hồ sơ; câu hỏi dưới đã xử lý trong phiên tối (B-01 ⇒ gói 1b quy ước (b))

# STATUS B — kết phiên 2026-10-25 17:07 +0700 (User kết phiên 17:0x; B25 dừng giữa chừng)

Terminal phiên này: `hue-rag-de` (A = `hue-rag-00`; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi
User (25/10, terminal B): B báo cáo trực tiếp cho A; việc A giao = User nói "làm đi".

## Trạng thái kết phiên
- **File đang khai báo sửa: không.** Đang giữ GPU: không. Server uvicorn kiểm (port 8000) đã dừng.
- **B25 rà code luồng dựng index + nền — DỞ** (dừng 17:05). File `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` (đầu file ghi
  đã rà / chưa rà). 10 finding tạm; nổi bật **B-01 (cao)**: `core.schema` và `backend.core.schema` cùng nạp trong API ⇒ `chat.py` / `app.py`
  bắt sai lớp lỗi (Qdrant lỗi khi hỏi ⇒ 500 thay 503; corpus đổi lúc khởi động ⇒ 503 thay 409) — *suy ra* từ code + kiểm `is`, chưa tái tạo
  bằng lỗi thật. **Phiên sau:** rà nốt chunker / markdown_blocks / upsert, test, notebook 03 / 04, guide phase_0–4 + phần index
  `full_corpus_rag.md` + `guides/README.md` (2 sub-agent bị dừng, chưa ra file — giao lại); chốt top 10; rồi kiểm chéo top 5 của C.
- **8.2 tạm dừng (User 16:5x).** B1 (B23) xong, T1–T5 đạt, report `phase_8_2_b1_implementation.md` (sha `bb5fea83aeb6`) — **chờ A
  review**; code ở nhánh `p82-b1` (A cất, chưa merge). Dữ liệu `data/phase_8_2/b1/`.
- Review xong trong phiên: B22 spec 8.2 (3 vòng ⇒ ready; User duyệt `dabae90b2b60`); B24 B0 prep (2 vòng ⇒ ready, `doc_cap_mu.md`
  `37b66efb3499`). B đã thấy khóa X / Y ⇒ **B không làm người tóm nhãn** B0.
- Việc còn chờ B (theo handoff): review plan E1 của C (sha `f86240418ca1`) khi 8.2 chạy lại.

## Việc phiên chiều 25/10 (sau 15:51)
| Việc | Kết quả | File |
|---|---|---|
| B22 review spec 8.2 | 3 vòng: 4 major + 5 minor ⇒ 1 major + 2 minor ⇒ ready | `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_spec_review.md` |
| B23 B1 context 10 + NFC | plan duyệt `1a5ac660bd5d`; T1–T5 đạt; A/A context 10; nhiễu citation 12 vs 8 | `phase_8_2_b1_plan.md`, `phase_8_2_b1_implementation.md` |
| B24 review B0 prep | F1 major (lộ mù câu 17 `[Nguồn 8]`) ⇒ sửa ⇒ ready | `phase_8_2_b0_prep_review.md` |
| B25 rà code (dở) | 10 finding tạm | `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` |

## Tiền paid phiên chiều 25/10
- **B1: 0,0369194 USD** (log; 291.269 token vào / 15.585 ra, 176 câu) + live `/chat` 2 câu ≈ **0,0004 USD (ước — API không ghi usage)**.
  Judge: 8 sub-agent Claude (quota, 0 USD). Review / rà code: 0 USD. (Phiên sáng 25/10, 8.1: 0,1653212 USD — đã ghi ở các report 8.1.)

## File tạm / private
- `/tmp/b24/`, `/tmp/b24_out*`, `/tmp/b25/`, log uvicorn: **đã xóa** (17:06).
- Private B tạo phiên này: `data/phase_8_2/b1/` (lượt B1, judge, check / analyze, câu NFD tự viết); `data/ra_soat_code/` (rỗng).

## Đã học / bẫy gặp
- 25/10 B22: đọc JSON private bằng `python3 -I` thay vì `uv run python -I` (A nhắc) ⇒ mọi lệnh Python, kể cả chỉ đọc, dùng `uv run`.
- Qdrant có thể tắt giữa phiên; pytest vẫn chạy và lỗi môi trường trông như lỗi code: đọc dòng `E` trước.
- pytest: rootdir là gốc repo; chỉ liệt kê file test, không dựa vào `--deselect`.
- Lệnh paid mới: chạy thử không `--env-file` trước để thấy nó định gọi gì.
- Auto-mode chặn `curl -X DELETE` Qdrant / `rm` lớn: dừng, nhờ User chạy `!` trong terminal B.
- Hai session cùng sửa working tree: khi gate cần so byte mà file session khác đang dở, chạy bản HEAD (`git show HEAD:…`
  hoặc `git archive HEAD backend` vào `/tmp` + symlink `data/`, `knowledge-base-hue/` chỉ đọc).
- Script ngoài `backend/` cần `PYTHONPATH=.:..`.
- Qdrant không cam kết thứ tự hòa điểm; runtime và native đã phá hòa theo point_id.
- Validator citation: câu từ chối chuẩn + `[n]` = lỗi.
- `g1_retrieval run` với `--name` đã có sẽ ghi đè JSONL.
- `g1/c_runtime.jsonl` cùng tập câu với `runtime.jsonl` (dev, 108 câu) — không phải tập test; số test lấy theo `split.json`.
- Mở phiên: chưa biết terminal nào là A ⇒ gửi cùng tin cho cả hai peer, hỏi ai là A (25/10, ổn).
- Danh sách "chưa commit" trong STATUS / tin nhắn bị cũ khi A commit giữa chừng (25/10: báo g2_generate.py chưa commit
  trong khi đã ở `266c105`) ⇒ trước khi liệt kê, chạy `git status --short` + `git log --oneline -3`.
- Model "đã có trong HF cache" có thể chỉ là thư mục `refs` rỗng ⇒ kiểm `du -sh` / file `.safetensors` trước khi lập kế
  hoạch offline (25/10: M1 / M2 phải tải 2,2 GB mỗi cái; M2 cần `sentencepiece`).
- Lượt có phí với model tự suy luận: token ra có thể gấp ~3 lần ước (luna listwise ~270 token / câu) ⇒ luôn pilot 10 câu và
  ước lại từ pilot.
- Khi so điểm judge giữa biến thể, chấm baseline **cùng lượt mù** với biến thể (nhiễu judge-only đo được 2/88 câu).
- HNSW: kết quả dense phụ thuộc `limit` (30 đầu của `limit=100` ≠ `limit=30` ở 1/108 câu) ⇒ tái lập runtime phải hỏi
  đúng `limit` như production. Qdrant sparse tính float32 ⇒ phá hòa có thể khác float64 trong bộ nhớ.
- 25/10 B24: kiểm mù bằng regex chỉ dạng `[n]` bỏ sót `[Nguồn n]` do model tự viết ⇒ quét mọi cụm ngoặc vuông có số + "nguồn <số>".
- 25/10 B23: giờ ghi trong file phải lấy bằng `date` ngay trước khi ghi (B ghi nhầm 16:37 khi `date` là 16:32 — đã sửa).
- 25/10 B25: `python -m` từ `backend/` + `sys.path` có cả gốc repo ⇒ module nạp hai lần (`core.*` / `backend.core.*`), lớp lỗi khác nhau;
  khi so `isinstance` / `except` giữa module, kiểm `sys.modules`.

## Câu hỏi cho A / User
- B-01 (import kép): sửa cách import cho cả `backend/` là thay đổi nhiều file — chọn một kiểu import (`core.*` hay `backend.*`) và có tái
  tạo lỗi 503 / 409 bằng app thử (collection không tồn tại, port khác) không — A / User quyết.
- B-03: tham số sinh câu trả lời — hằng trong code hay yaml là nguồn (loader chỉ kiểm kiểu)?
- Mâu thuẫn corpus Hải Vân Quan vẫn chờ User (sửa khi build lại index).
