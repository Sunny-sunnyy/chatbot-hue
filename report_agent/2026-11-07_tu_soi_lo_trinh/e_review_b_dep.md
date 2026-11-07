# Review: B-dep — nhánh `p12-deploy-nhap` `50e4ebf` + nháp `data/phase_12/deploy_nhap/` sau sửa của B

Decision: **ready_for_user_confirmation** (vòng 2, 13:26 07/11/2026 — §5) · vòng 1: changes_requested (1 major M-1 + 5 minor) ⇒ B sửa ⇒ M-1 + m-1…m-4 **đóng**, m-5 ghi nhận; 1 minor mới m-6 (không chặn).
Người kiểm: E (Claude Opus 5.5) · vòng 1 13:06, vòng 2 13:26 07/11/2026 (`date`) · 0 USD
Căn cứ: `e_dep_chuan_bi_deploy.md` (E), `tu_soi_B.md` §5 (B review nháp của E: M1–M3), report B `b_dep_build_cuc_bo.md`; luật `Session_Prompt.md` §5 (Golden / câu kín / `evaluation/` private).

## 1. Phạm vi đã review

- Nhánh: `git diff main...50e4ebf` — 2 file, +48. `backend/core/settings_loader.py` (`apply_env_overrides`), `backend/tests/test_settings_env.py`.
- Nháp: `Dockerfile`, `Dockerfile.dockerignore`, `compose.yml`, `Caddyfile` ở `data/phase_12/deploy_nhap/` (bản B sửa 12:52–13:00).
- Ảnh `hue-rag-app:nhap` B đã build: E chỉ **liệt kê file** bên trong. Lệnh `docker run --rm --network none --entrypoint sh`, không chạy app, không build.

## 2. Code nhánh — đạt

| Tiêu chí | Bằng chứng | Kết quả |
|---|---|---|
| Phạm vi tối thiểu | Đúng 2 khoá (`vector_database.url`, `assistant.tra_web`); đọc ở rìa `load_settings` trước bước kiểm | khớp |
| Không đặt biến ⇒ như file | `test_no_env_keeps_file_values` so cả dict với YAML | khớp [Chạy] |
| Giá trị lạ ⇒ dừng | `"0"`, `"False"`, `"no"`, `""` ⇒ `ValueError`; E thử thêm `TRUE` ⇒ `ValueError` | khớp [Chạy] |
| Cờ tới đúng nơi dùng | E thử `HUE_TRA_WEB=true` ⇒ `AssistantFlags.from_settings(...).tra_web` = True | khớp [Chạy] |
| Không đọc / log secret | Chỉ đọc 2 biến tên `HUE_*`; không log | khớp |
| Chỗ khác dùng URL Qdrant | `vectorstore/qdrant.py:23` đọc `settings["vector_database"]`. `ingestion/full_corpus_pipeline.py:99` đòi `localhost:6335` khi build index ⇒ nếu `HUE_QDRANT_URL` còn trong shell thì build dừng — đúng chiều an toàn | khớp |

`tests/test_settings_env.py`: **6 passed** (0,05 s), chạy trong worktree riêng `/tmp/e_rv2` (đã gỡ).

## 3. Findings

- **M-1 (major) — ảnh Docker chứa dữ liệu đánh giá private, trái với report B.**
  - *Báo cáo:* `b_dep_build_cuc_bo.md` §2 ghi "0 file `evaluation/` / `*sealed*` của kho".
  - *Bằng chứng [Chạy]:* trong ảnh có **16 file** dưới `*/evaluation/`:
    - `golden_full_corpus_authoring.jsonl` ở 6 thư mục lĩnh vực;
    - Golden bản món ăn: `foods/evaluation/golden_v2.jsonl`, `golden_v3_smoke.jsonl`, `tests.jsonl`, `judge_calibration_v1.jsonl`…
  - Thêm `meta/`, **148 file**, gồm `golden_backup_2026-10-25`, `golden_backup_dot2_2026-10-30`, 4 thư mục sao lưu kho, ghi chú soạn kho.
  - *Nguyên nhân:* `Dockerfile.dockerignore` dòng `knowledge-base-hue/evaluation` chỉ khớp thư mục `evaluation/` **ở gốc kho**. Kho có thêm 7 thư mục `evaluation/` lồng trong từng lĩnh vực (`find knowledge-base-hue -type d -name evaluation`).
  - *Tác động:*
    - App không phục vụ các file này: `/api/kham_pha` chỉ trả `corpus.sources`.
    - Nhưng ảnh sẽ nằm trên máy AWS công khai, và có thể bị chuyển / lưu ở nơi khác.
    - Luật §5: Golden và bộ đánh giá là private, chỉ để đúng chỗ cần.
    - Runtime chỉ cần đúng 1 file trong `meta/`: `full_corpus_conditions.json` (`settings.yaml:22`, `full_corpus_chunker.py:128`).
  - *Đóng:*
    - (a) `Dockerfile.dockerignore`: `knowledge-base-hue/**/evaluation` (thay dòng hiện có) và `knowledge-base-hue/meta` + `!knowledge-base-hue/meta/full_corpus_conditions.json`;
    - (b) build lại, chạy cùng lệnh liệt kê: `find /app/knowledge-base-hue -path "*evaluation*" -type f | wc -l` = **0**, `find /app/knowledge-base-hue/meta -type f` = **1 file**;
    - (c) app vẫn `/health` 5 / 5 (hash kho khớp record);
    - (d) sửa câu trong report B §2.
- **m-1 (minor) — mở cổng 443 trên máy AWS.**
  - Caddy + sslip.io cần cả 80 (để Let's Encrypt kiểm) lẫn 443 từ Internet.
  - Lightsail mặc định chỉ mở 22 / 80 ⇒ phải thêm 443 trong firewall của instance, không thì HTTPS treo.
  - *Đóng:* ghi vào bước lên máy (report hoặc đầu `compose.yml`).
- **m-2 (minor) — log không giới hạn.**
  - `./logs` dùng `FileHandler` (không xoay vòng), và log stdout của Docker mặc định `json-file` không trần.
  - Hai tháng demo thì nhỏ (0,53 MB / tuần trên máy User), nhưng một lượt bị gọi dồn sẽ làm phình.
  - *Đóng:* compose thêm `logging: {driver: json-file, options: {max-size: "10m", max-file: "3"}}` cho 3 dịch vụ. `RotatingFileHandler` để sau.
- **m-3 (minor) — Docker phải tự bật khi máy khởi động lại.**
  - `restart: unless-stopped` chỉ có tác dụng khi daemon Docker chạy.
  - *Đóng:* ghi `sudo systemctl enable --now docker` vào bước lên máy.
- **m-4 (minor) — chú thích lệch số cổng.**
  - `settings_loader.py` ghi "trong compose: `http://qdrant:6335`", nhưng `compose.yml` dùng `http://qdrant:6333` (đúng, sau khi bỏ `network_mode`).
  - *Đóng:* sửa chú thích thành `6333`.
- **m-5 (minor, ghi nhận) — `rm -rf …/trees` phụ thuộc chi tiết bên trong `huggingface_hub` 1.26.**
  - B đã đọc code thư viện và chạy thật; `uv.lock` ghim bản ⇒ ổn tới khi nâng bản.
  - *Đóng:* không cần. Khi nâng `huggingface_hub` thì kiểm lại `/health`.

**Không thấy quá tay:**
- Stage `code` + `--build-context` cần thật trước khi merge; nhỏ.
- Healthcheck Qdrant đủ: app chỉ kiểm Qdrant một lần lúc khởi động.
- Không có thêm thư viện, retry hay script phụ.

**Còn đúng từ trước (không phải finding của nhánh này):** cookie `Secure`, tắt `/docs`, giới hạn lượt / ngày (`e_dep_chuan_bi_deploy.md` §4) — bắt buộc trước khi gửi link công khai. Report B §3 đã ghi.

## 4. Cách E chạy lại

- `git worktree add /tmp/e_rv2 50e4ebf --detach` ⇒ `uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_settings_env.py` ⇒ 6 passed.
- Ca dò: `HUE_QDRANT_URL="" HUE_TRA_WEB=true` ⇒ URL giữ `localhost:6335`, `tra_web` True tới `AssistantFlags`; `HUE_TRA_WEB=TRUE` ⇒ `ValueError`.
- Gỡ worktree.
- Ảnh: `timeout 60 docker run --rm --name e_rv_ls --network none --entrypoint sh hue-rag-app:nhap -c 'find …'`. Vài giây, không tải mạng; C đang đo latency, lệnh này không chạy app hay model.
- **Bất biến kiểm:** không đặt biến ⇒ `load_settings()` y hệt `settings.yaml` (test của B + E đọc code: chỉ ghi khi biến có giá trị).

## 5. Vòng 2 — kiểm phần sửa (13:26 07/11/2026)

Căn cứ: B sửa ở `b_dep_build_cuc_bo.md` §4; ảnh mới `hue-rag-app:nhap2`; nhánh `p12-deploy-nhap` `23454f3`. E đếm **bằng cách riêng**, không dùng lệnh của B:
- `find /` toàn ảnh, bỏ `.venv` / `/usr` / `/proc`, lọc tên chứa `evaluation|golden|sealed|backup|_source-dumps|.env|split.json|gold_v`;
- so danh sách `.md` trong ảnh với `corpus.sources` của build record, trên máy chủ.

Lệnh `docker run --rm --network none --entrypoint sh` — chỉ liệt kê, không chạy app.

| Finding | Kết quả [Chạy] | Trạng thái |
|---|---|---|
| **M-1** dữ liệu đánh giá trong ảnh | Tên khớp mẫu chỉ còn **mã**: `backend/evaluation/*.py` + `.md` lời dặn chấm, `backend/tests/test_golden_full_corpus.py`, thư viện `sentence_transformers/*/evaluation/` trong cache uv, 2 file `dpkg-db-backup` của hệ điều hành. **0** file `evaluation/` của kho, 0 câu kín, 0 sao lưu Golden / kho, 0 `.env`. Kho trong ảnh: 204 `.md` = **đúng tập `corpus.sources`** (so bằng Python) + `meta/` **đúng 1 file** `full_corpus_conditions.json`. `data/` đúng 3 file (record, sparse state, `diem_v3.json`). Danh sách chừa sinh bằng script từ build record (`dung_dockerignore.py`) ⇒ kho đổi thì sinh lại, không sót thư mục lồng | **đóng** |
| m-1 cổng 443 · m-3 `systemctl enable docker` | Ghi ở đầu `compose.yml` | **đóng** |
| m-2 log Docker không trần | `x-log` json-file 10 MB × 3 áp cho các dịch vụ; B thấy áp vào container | **đóng** |
| m-4 chú thích cổng | `23454f3` sửa thành 6333 | **đóng** |
| m-5 `trees/` | Không cần sửa (như vòng 1) | ghi nhận |

- **m-6 (minor, mới) — cache uv 1,9 GB còn trong ảnh.**
  - `/root/.cache` = 1,9 GB [Chạy]: bản sao gói của `uv pip install`, trùng với `.venv`.
  - Ảnh nặng gần gấp đôi khi chuyển máy hoặc ghi đĩa. Lightsail 80 GB vẫn đủ, nhưng `docker save | ssh` chậm hơn.
  - *Đóng:* thêm `--no-cache` vào `uv pip install` (hoặc `&& rm -rf /root/.cache/uv` trong cùng `RUN`), build lại, `du -sh /root/.cache` ≈ 0. Không chặn.

**Kết luận vòng 2:** ready_for_user_confirmation. Deploy thật vẫn chờ User (tài khoản, máy, tiền). Trước khi đưa link công khai còn: giới hạn lượt, cookie `Secure`, tắt `/docs` (`e_dep_chuan_bi_deploy.md` §4).
