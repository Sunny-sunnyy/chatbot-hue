# STATUS B — phiên tối 2026-10-25 (mở 18:21 +0700, terminal `hue-rag-c3`; A = `hue-rag-77`, C = `hue-rag-7f`)

## Trạng thái (20:17)
- **B25 rà code luồng dựng index + nền — XONG 18:39, chờ kiểm chéo** (A "làm đi" 18:2x; 0 USD; 3 sub-agent). Nền rà `main` `1e8cf8f` (code không
  đổi so `bc568f1`). 21 finding, top 10 chốt; B-01 cao, B-11 cao. File `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md`.
- Sub-agent: SA1 guide 0–2 + README, SA2 guide 3–4 + index `full_corpus_rag.md`, SA3 test + notebook 03/04 (97 passed) ⇒ `data/ra_soat_code/sa{1,2,3}_*.md`
  (private). B kiểm lại 2–4 khẳng định chính mỗi cái. SA2 có gọi một scroll Qdrant (POST chỉ đọc) ngoài brief "chỉ GET".
- Chỉ đề xuất, chưa sửa code (User 18:3x).
- **Kiểm chéo top 5 của C (C-09, C-02, C-01, C-12, C-19) — XONG 18:51** ⇒ `report_agent/2026-10-25_ra_soat_code/kiem_cheo_B.md`:
  `ready_for_user_confirmation`, 5 / 5 đúng, mức hợp lý, 6 minor bổ sung (R-01…R-06) cho TONG_HOP. Script riêng `/tmp/b25x/`, 0 USD, không `.env`.
  B khai xung đột lợi ích: C-09 bác nhận định trong report 8.1 G2 do B viết.
- **B-08 rút** (sai: runtime đã làm nóng e5 lúc khởi động — thấy khi kiểm C-01) ⇒ sửa trong `ra_soat_code_B.md` (sau commit `c272644`).
- **Review C35 (gói 1a) — XONG 19:56** ⇒ `report_agent/2026-10-25_ra_soat_code/sua_1a_review.md`: ready, 0 blocker / major, 2 minor;
  A đã commit `9e6d371` + `63fec4f`. Script `/tmp/b27/`.
- **B26 gói 4 (tài liệu) — XONG 20:0x, chờ review C** ⇒ `report_agent/2026-10-25_ra_soat_code/sua_4_implementation.md`. 16 file (13 guide +
  3 notebook), chưa commit. Đếm ngoài vùng lịch sử 34 ⇒ 1 (roadmap dự kiến); đường dẫn home repo khác 48 ⇒ 0; notebook Run All bản tạm 3 / 3.
  Private: `data/ra_soat_code/b19_duong_dan_ngoai.md`, `tools/{deadrefs,edit_notebooks}.py`, `b26_deadrefs_{before,after}.txt`. 0 USD.
- **File đang khai báo sửa:** 16 file B26 (giữ khai báo tới khi review xong / A commit). Chờ A.
- **Plan gói 1b — XONG 20:1x, chờ C review + A duyệt sha** ⇒ `report_agent/2026-10-25_ra_soat_code/sua_1b_plan.md` (sha `8b36bab7901c`, bản 3).
  Quy ước (b) đã chọn (A + C). Bản 3 sửa P1, P2, m1–m4; T-C do User chạy `!` (auto mode chặn HF_HOME rỗng). Script đo `data/ra_soat_code/tools/{inventory,dup_modules}.py`. Chưa sửa code.
- File tạm: `/tmp/b25/`, `/tmp/b25x/`, `/tmp/b26/`, `/tmp/b27/` (script B), `/tmp/b25_sa{1,2,3}/` của sub-agent — xóa khi kết phiên.

- **Review gói 3 (C) — XONG 20:46** ⇒ `sua_3_review.md` ready (A commit `47a4e32`).
- **Gói 1b — XONG 21:3x, chờ review C** ⇒ `report_agent/2026-10-25_ra_soat_code/sua_1b_implementation.md`. 26 file (25 sửa + 1 test mới), chưa commit.
  K1–K7 đạt: nạp đôi 0 ở 11 điểm vào + pytest; T-A / T-B / T-C đỏ ⇒ xanh (T-C User chạy `!`); 15 file test 198 passed (C-17 không tăng); T1 sha
  giống byte; notebook 3 / 3; cổng ổn định đạt (~0,0004 USD ước). A cần sửa `chạy_môi_trường.md:10-12`, `BAO_CAO_KHO_DU_LIEU.md:89`, Project_Status §8.
  **File đang khai báo sửa:** 26 file gói 1b (giữ tới khi A commit). Script `/tmp/b30/`.

- **Review plan đợt 3 (C) — XONG 21:36** sha `8bbe98640c80` ⇒ `sua_dot3_plan_review.md`: changes_requested (M-1 `git mv` sang `meta/` đưa file vào index; m-1…m-6).

## Ý cải tiến (cho đợt tìm hướng tốt hơn sau 5 gói — giả thuyết, chưa đo)
- Chia đoạn: bỏ ràng buộc tokenizer huydang 256 (model không chạy ở runtime) ⇒ đoạn dài hơn / ít đoạn vụn; 8.1 G3 H1 đã đo đoạn đúng không đổi —
  cần đo Completeness câu nhiều nguồn (giống lợi ích context 10).
- Khởi động API: nạp e5 2,45 s + chia lại / hash kho — đo thời gian khởi động thật để biết có cần tối ưu không (hiện chưa có số qua `create_app`).
- Build lại index: cách *đích mới rồi cutover* cần tên collection / đường sparse state lấy từ settings thay hằng (B-06) — làm cùng đợt build lại.
- Đánh giá: điểm judge đang chấm cả câu mà API trả 500 — tách chỉ số "trải nghiệm người dùng" (câu lỗi = 0 điểm) bên cạnh điểm judge.

## Đã học / bẫy gặp (phiên tối 25/10)
- 25/10 20:3x: auto mode chặn lệnh chạy Python với `HF_HOME` trỏ thư mục rỗng (thử model không nạp) — chặn cả B lẫn C ⇒ không thử lại / đổi
  cách; ghi lệnh vào plan để User chạy `!`, tách test đó ra file riêng để pytest của B không chạy nó.
- 25/10 tối: B ghi "`scripts/` không tồn tại" vì chỉ tìm ở gốc repo — mục việc ghi đường dẫn tương đối ⇒ `find . -name <tên> -not -path './.venv/*'` trước khi kết luận "không có".
- 25/10 tối: B-04 phiên chiều khẳng định "chunker đã fail-closed" khi chưa đọc chunker ⇒ không ghi khẳng định về code chưa đọc; ghi "chưa kiểm".
- 25/10 tối: B-08 đo "câu đầu chậm" bằng script tự nạp model, không qua đường khởi động thật (đã có warm-up) ⇒ đo hiệu năng phải đi đúng
  đường production (`create_app` / `build_full_corpus_retrieval_service`), không dựng lại từng bước.
- 25/10 tối: sub-agent SA2 gọi scroll Qdrant bằng POST (chỉ đọc) trong khi brief ghi "GET thì được" ⇒ brief nêu rõ "chỉ GET; POST scroll /
  query cũng không" hoặc cho phép rõ POST chỉ đọc nếu cần.
- 25/10 tối: B dùng `python3` hệ thống để sửa text STATUS_B (vi phạm §10 / bài học cũ) ⇒ sửa file bằng Edit, mọi Python bằng `uv run`.

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
