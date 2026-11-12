# Implementation Report: Phase 9 B7 — bước 0 (kiểm trước lượt có phí) + probe log truy cập uvicorn

Người làm: B (Claude Code, terminal `hue-rag-1b`)
Date: 18:49 12/11/2026 (`date`)
Việc giao: `CURRENT_HANDOFF.md` "VIỆC PHIÊN 12/11" dòng B. Plan nháp: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` §2, §4.
Tiền: **0 USD** (không gọi model sinh; chỉ tìm kiếm cục bộ + `/health`).

## 1. Phạm vi

Ba việc, đúng mục giao; không sửa `backend/`, không mở `*sealed*`, không chạy lượt có phí:

1. Code RAG 1–8 (tag `p9-moc` = `18e8f42`) có chạy được với chỉ mục / build record hiện tại không, và tầng tìm của nó có cho đúng kết quả mốc không.
2. Bản sao harness đo Golden vào `data/phase_9/b7/tools/`.
3. Server `main` thật có in IP người gọi ra log truy cập không (câu Q-DP).

## 2. Thay đổi chính

- Worktree `/tmp/b7_moc` (tách rời, tại `p9-moc`; symlink `data/`, `knowledge-base-hue/`; **không sửa file nào** — `git status` chỉ thấy 2 symlink). Giữ lại cho B7.
- `data/phase_9/b7/tools/do_cuoi_b7.py` (private): bản sao `data/do_cuoi_2026-11-01/tools/do_cuoi.py` (sha `286df0ba5b3d`), đổi 4 chỗ:
  build record `51fb1ec63cbc` ⇒ `9921888f2030` · sparse state `c8134c49a648` ⇒ `4a8311a2dfef` · số điểm 8.424 ⇒ 8.435 · thư mục mặc định ⇒ `data/phase_9/b7`;
  **và một chỗ không phải hằng số** (B tự quyết, xem §5): phép kiểm "Qdrant chỉ có đúng một collection" ⇒ "collection chatbot có mặt", vì Qdrant nay có thêm collection thử ảnh.
- Kết quả chạy (private): `data/phase_9/b7/buoc_0/`.

## 3. Cách đã chạy thật

`R=/home/minhhieu/hue_rag`, `W=$R/data/phase_9/b7/buoc_0`. Mọi lệnh Python dùng `.venv` của dự án (`uv run --project $R`).

```bash
git worktree add --detach /tmp/b7_moc p9-moc          # + 2 symlink data/, knowledge-base-hue/
# (1a) T1 158 câu trên code mốc — 21 s
cd /tmp/b7_moc/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 timeout 900 uv run --project $R python -m evaluation.full_corpus_eval retrieval --out $W/t1_p9_moc.jsonl
# (1b) server code mốc, cổng 8881 ⇒ GET /health
cd /tmp/b7_moc/backend && HF_HUB_OFFLINE=1 timeout 300 uv run --project $R --env-file $R/.env uvicorn api.app:app --port 8881
# (3) server main (a83defd), cờ như Dockerfile nháp, cổng 8882 ⇒ GET /health ×2 (1 lần kèm X-Forwarded-For: 203.0.113.7) + GET /
cd $R/backend && HF_HUB_OFFLINE=1 timeout 240 uv run --env-file $R/.env uvicorn api.app:app --host 127.0.0.1 --port 8882 --proxy-headers --forwarded-allow-ips '*'
# (2) lệnh 0 USD của bản sao harness, ghi vào thư mục thử (không đụng thư mục đo thật), ở cả hai bên
cd <bên>/backend && DO_CUOI_DIR=$W/thu_preflight_<bên> PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project $R python $R/data/phase_9/b7/tools/do_cuoi_b7.py preflight
```

Hai server đã tắt bằng TaskStop; cổng 8881 / 8882 trống.

## 4. Kết quả quan sát

| Kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Code mốc khởi động với build record hiện tại (kiểm "chỉ mục khớp kho") | **PASS** — khởi động ~8 s, không báo lệch | `server_p9_moc.out` |
| `/health` code mốc | **PASS 5 / 5** (app, qdrant, retrieval, tokenizer, generator) | `health_p9_moc.json` |
| T1 158 câu trên code mốc = mốc hiện tại | **PASS** — 158 dòng, sha `64656a87c109`, **giống byte** file T1 sau sửa kho 05/11 (`cmp`) | `t1_p9_moc.jsonl` |
| Bản sao harness: `preflight` trên `main` và trên code mốc | **PASS** cả hai — 8.435 điểm, build record `9921888f2030`, sparse `4a8311a2dfef`, nhãn đoạn đúng `33d16fd6b8f4`, Golden `6331e88fb171` / 176 câu, ngữ cảnh 10, `gpt-6-luna` | `thu_preflight_main/`, `thu_preflight_moc/` |
| Log truy cập uvicorn trên `main` có in IP không | **Không in** — 3 lần gọi (2 `/health`, 1 `/`) đều 200; đầu ra server có **0** dòng `GET …`, **0** lần xuất hiện `203.0.113.7` hay `127.0.0.1`; `application.log` thêm 5 dòng khởi động, 0 dòng có IP | `server_main.out`, `log_moc_dong.txt` |

Ý nghĩa: hai bên của B7 (code cũ ↔ `main`) đọc cùng một chỉ mục và tầng tìm của code cũ cho đúng từng byte kết quả mốc ⇒ khác biệt đo được ở B7 chỉ đến từ code trả lời, đúng giả định plan §2.
Quan sát thêm: server code mốc cũng không in dòng truy cập nào (cùng hiện tượng).

Nguyên nhân log truy cập bị tắt: B **không** kiểm lại — A đã dò 11/11 (cấu hình log trong lúc khởi động tắt logger truy cập của uvicorn); lần chạy này chỉ xác nhận **hành vi** trên server thật.

## 5. Lỗi và giới hạn

- **Harness cần hơn "đổi hằng số" để dùng cho B7** (báo A / người viết plan; B chưa sửa vì ngoài phạm vi "chỉ đổi hằng số"):
  1. Phép kiểm một-collection — B đã nới (ở trên), không nới thì `preflight` dừng ngay.
  2. Script gắn cứng **ba bên** `truoc` / `sau` / `aa`: `export-judge` và `analyze` đòi đủ cả ba, mà plan §5 bỏ A/A ⇒ phải sửa logic (hai bên) hoặc chấm bằng đường khác.
  3. `run` chỉ sinh bên `sau` / `aa` bằng đường RAG thuần, và dừng nếu code khác commit lúc `preflight` ⇒ mỗi bên cần thư mục riêng; plan §4 vốn định sinh bằng `evaluation generate`, khi đó file kết quả phải khớp khuôn mà `check` / `export-judge` đọc — **chưa kiểm**.
  4. Sàn "câu tụt ≤ A/A + 3" đang lấy `N_AA = 2` của 01/11 — khớp quyết định Q2 của plan (dùng lại A/A cũ).
- Code mốc chạy bằng `.venv` hiện tại của dự án (thư viện mới hơn thời 01/11); T1 giống byte cho thấy tầng tìm không bị ảnh hưởng; **phần sinh câu trả lời của code mốc chưa chạy thử** (có phí) — lần đầu sẽ là pilot 10 câu của B7.
- Worktree mốc không có bản build giao diện ⇒ `/` trả 404 (không cần cho B7, chỉ dùng harness).
- Probe log chỉ phủ uvicorn + log ứng dụng. **Chưa kiểm:** log truy cập của Caddy (lớp đứng trước khi deploy) và đường báo quá lượt (429) có ghi IP không.

## 6. Bàn giao cho người kiểm

- Chạy lại rẻ nhất (0 USD, ~30 s): lệnh (1a) với tên file ra khác rồi `sha256sum … | cut -c1-12` ⇒ `64656a87c109`; `diff data/do_cuoi_2026-11-01/tools/do_cuoi.py data/phase_9/b7/tools/do_cuoi_b7.py` ⇒ đúng 5 chỗ ở §2.
- Việc của A: quyết hướng cho mục 5.2 / 5.3 (sửa harness hai bên là việc của bước chuẩn bị B7, cần nằm trong plan trước khi duyệt sha); bỏ / sửa ý "log truy cập uvicorn" trong Q-DP.
- Giải thích ngắn cho User: bản chatbot cũ (trước khi có trợ lý) vẫn chạy được trên kho hiện tại và tìm ra đúng y các đoạn như bản mới, nên khi so hai bản, chênh lệch chỉ do cách trả lời; server không ghi địa chỉ IP người hỏi vào log.

## 7. Bổ sung 18:55 12/11/2026 — harness hai bên (A giao sau review E M-1; 0 USD)

Phần (2) ở trên ("chỉ đổi hằng số") **được thay** bằng mục này. Phạm vi: chỉ `data/phase_9/b7/tools/` (private); không sửa `backend/`, không sửa code ở `p9-moc`.

**Đã sửa `do_cuoi_b7.py`** (294 dòng, từ bản gốc 383 dòng):

- Hai bên thay ba: `truoc` = RAG 1–8 (sinh mới ở worktree `p9-moc`), `sau` = agent (`main`). Gỡ bên `aa` và mọi phép so với nó.
- Script không còn sinh câu trả lời (gỡ `run`, `merge`, `import-truoc`): mỗi bên sinh bằng `evaluation.full_corpus_eval generate` ở đúng bản code của nó; lệnh mới `nhap` chép file vào thư mục đo, dừng nếu không đủ 176 câu hoặc thiếu trường.
- Ngưỡng số câu tụt thành tham số bắt buộc `analyze --max-drop N` — số này phải do plan ghi trước (A/A 01/11 đo được 1 câu tụt Completeness / 129 ⇒ "A/A + 3" = 4; bản gốc dùng 5). B không chọn hộ.
- Sàn lỗi kỹ thuật xét cả hai bên; tiền mỗi câu của agent lấy trường `usd` của dòng (tổng mọi lần gọi).
- Các sàn / phép tính khác giữ nguyên bản gốc (ngoài kho bị trả lời, lỗi trích dẫn mới, nói chắc sai mới + chấm lại, từ chối nhầm, bootstrap theo cặp, seed xáo).

**Mới `chuoi_rag_moc.py`** (80 dòng): phía RAG của bộ chuỗi — mỗi lượt hỏi như một câu đơn qua đường sinh của `p9-moc`; chỉ in số đếm; `--thu` chạy không gọi model; `--bo-luot` bỏ các lượt đã có câu trả lời ở lượt Golden (nếu plan chọn).

**Chạy thử 0 USD** (thư mục thử `data/phase_9/b7/buoc_0/thu_hai_ben/` — **không phải kết quả đo**):

| Lệnh | Đầu vào thử | Kết quả |
|---|---|---|
| `preflight` | `main` `a83defd` | đạt |
| `nhap` + `check` bên `truoc` | file 176 câu của lượt đo cuối 01/11 (khuôn dòng RAG) | đọc được, 176 dòng |
| `nhap` + `check` bên `sau` | file 176 câu `generate` của agent (đợt B3) | đọc được, 176 dòng; thời gian từng câu = trống (file `generate` không có trường này — chỉ là số theo dõi) |
| `export-judge` | hai file trên | 330 mục / 14 lô (câu trả lời trùng chữ chấm một lần) |
| `check-judge`, `f2-candidates`, `analyze --max-drop 4` | **điểm giả sinh ngẫu nhiên, có file dán nhãn** | chạy hết, đủ khoá kết quả; thiếu `--max-drop` ⇒ dừng |
| `chuoi_rag_moc.py --thu` (trong `/tmp/b7_moc`) | 25 chuỗi đã thấy | 56 / 56 lượt tìm + dựng ngữ cảnh, 0 lỗi |
| `generate --help` ở `p9-moc` | — | nhận `--cases`, `--out` |

**Chưa kiểm / giới hạn:** `generate` phía `p9-moc` chưa sinh thật câu nào (có phí ⇒ pilot của B7); khuôn dòng của nó suy từ code (cùng hàm đã sinh file 01/11). Harness này chỉ phủ Golden + phía RAG của bộ chuỗi; an toàn 32, câu ngày, câu ngoài phạm vi, trò chuyện / web dùng công cụ cũ theo plan — B chưa chạy thử các công cụ đó phiên này. Danh sách sửa đã gửi C để ghi vào plan bản 2.
