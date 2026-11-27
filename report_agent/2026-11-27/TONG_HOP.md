# Tổng hợp đợt 27/11/2026 — Chuẩn hoá bộ deploy/Docker (Phương án A) & Lệnh smoke eval rẻ

**Thời gian:** 08:38 – 09:07 27/11/2026 (giờ `date`)  
**Điều phối:** Session A (`agy` CLI + `/swarm` gồm `b`, `c`, `e`, `monitor`)  
**Phạm vi đã duyệt:** Gói A trong `data/x14_deploy_2026-11-23/BAN_DO_PRODUCTION_2026-11-26.md` + 1 câu OpenAI thật qua Docker cổng `8880` + xây và chạy thử 1 lượt lệnh `smoke_eval` (`0 USD` AWS, ~`0,02–0,03 USD` OpenAI).

---

## 1. Kết quả gộp lên `main`
- **`a3d1aed0` (`b` — `origin/p16-b-deploy-tf-docs` @ `ab6b7419`):**
  - `deploy/terraform/1_nen_tang/main.tf`: thêm `aws_sns_topic_policy.alerts` (cho `cloudwatch.amazonaws.com` gọi `sns:Publish` kèm điều kiện `aws:SourceAccount`) và `aws_s3_bucket_lifecycle_configuration.artifacts` (`abort_incomplete_multipart_upload` 3 ngày).
  - `deploy/terraform/2_may_chu/` (`main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars.example`, `README.md`): thêm EventBridge Scheduler (`aws_scheduler_schedule.auto_stop`, `cron(30 23 * * ? *)`, `Asia/Ho_Chi_Minh`) + IAM role riêng (`ec2:StopInstances` trên đúng `aws_instance.app.arn`) + biến `auto_stop_enabled` (`true`), `auto_stop_schedule`.
  - `deploy/guides/hue-rag-deploy-policy.json`: thêm quyền `GiaoVaiChoScheduler`, `LichTuDungMayEC2` và `cloudwatch:GetMetricStatistics` trong `XemTrangThai` (bắt qua review chéo của `e`, finding #7).
  - Đồng bộ tài liệu `deploy/README.md`, `deploy/docker/README.md`, `deploy/guides/0..7` (thêm hướng dẫn kiểm `CPUCreditBalance` ở guide `5`), `docs/superpowers/specs/2026-11-23-deploy-aws-design-ban-3.md` sang mốc 26/11 (`gpt-6-luna` mặc định cả local lẫn deploy, `269` bài / `9.540` điểm / `269/269` ảnh, thống nhất `9 + 2 = 11` file riêng tư, gỡ nhắc `vi_sao`).
- **`21843ed2` (`c` — `origin/p16-c-docker-smoke-eval` @ `a64c0efc`):**
  - `pyproject.toml` + `uv.lock`: chuyển 13 gói không dùng trực tiếp ở runtime sang `[dependency-groups] dev` (`uv export --frozen --no-dev` giảm từ **706** xuống **345** dòng).
  - `deploy/docker/Caddyfile`: thêm `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `X-Frame-Options: DENY` (không đặt đè `Content-Security-Policy` của FastAPI), `Strict-Transport-Security` chỉ trên `@https protocol https`, `Cache-Control` cho `/static/assets/*` (`immutable`) và `/static/anh/*`, kèm mẫu `basic_auth` tắt mặc định.
  - `deploy/docker/compose.yml` & `deploy/docker/thu_o_may.sh`: thêm `no-new-privileges:true` cho `qdrant`, `mem_limit: 128m` cho `caddy`, và kiểm `id -u` (`10001`), security headers, `Cache-Control` trong `thu_o_may.sh kiem`.
  - `backend/evaluation/smoke_eval.py` + `backend/tests/test_smoke_eval.py`: lệnh smoke eval 14 ca công khai (0 câu kín `*sealed*`), chấm tất định không dùng LLM judge, hỗ trợ `--dry-run` (có ca đối chứng FAIL).

---

## 2. Kiểm chứng thực tế (`e` trên bản ghép `21843ed2`)
- **Kiểm 0 USD:**
  - `dung_ngu_canh.py --ref HEAD --du-lieu data --chi-kiem`: đủ **9 + 2 = 11** file riêng tư, thiếu `0`.
  - `terraform fmt -check -recursive deploy/terraform/` + `terraform init -backend=false` + `terraform validate` cho `1_nen_tang` và `2_may_chu`: đều hợp lệ.
  - `pytest tests/test_smoke_eval.py tests/test_assistant_boundary.py`: **8 passed** (trước đó `c` chạy thêm `test_static_ui.py` đạt **12 passed**).
  - `smoke_eval --dry-run`: **14/14 PASS**, `control_fail=CAUGHT`.
- **Docker mới & `thu_o_may.sh` cổng `8880`:**
  - Ảnh `hue-rag-app:21843ed`: **3,49 GB** (giảm **0,13 GB** so với `3,62 GB` trước đó), `269` bài kho, `0` file cấm.
  - Ba hộp `healthy` sau `27,7 s`; `app` chạy `UID=10001` (`hue`, `CapDrop=[ALL]`, `no-new-privileges:true`); `qdrant` có `no-new-privileges:true`; `caddy` `mem_limit=128m`; `/` `200` (đủ CSP của FastAPI + header Caddy), `/health` `ok`, `/docs` `404`, `/api/kham_pha` `269 bài`, thân JSON 13 MB `413`, `/static/assets/*.js` có `Cache-Control: public, max-age=31536000, immutable`, nguồn Qdrant 6335 giữ nguyên `9.540` điểm và `0` snapshot thừa.
  - 1 câu OpenAI thật qua Caddy `:8880` (`"Vé tham quan Đại Nội bao nhiêu?"`): `status_code: 200`, `outcome: success`, `model: gpt-6-luna`, `n_cited_sources: 2`, `total_ms: 6885,9 ms`, chi phí **`0,00058635 USD`**. Đã chạy `thu_o_may.sh don` sạch sẽ.
- **Lượt thật `smoke_eval` trên `gpt-6-luna` (cổng `8038`):**
  - Kết quả: **14/14 PASS**, `p50=3614,6 ms`, `p95=5258,0 ms`, chi phí **`0,00647328 USD`**.
  - Dữ liệu chi tiết: `data/smoke_eval/smoke_eval_20261127_020614.json`.
- **Tổng chi phí OpenAI đợt 27/11:** **`0,00705963 USD`** (~`0,0071 USD`); lũy kế phần test của nhóm ~**0,75 USD** / trần **2–2,5 USD**.

---

## 3. Giới hạn / phần chưa chạy
- Toàn bộ thao tác tạo tài nguyên thật trên AWS (`terraform plan/apply`, EventBridge Scheduler, SNS email, HTTPS qua tên miền thật) vẫn ở trạng thái `[chưa kiểm trên AWS]` theo phạm vi `0 USD AWS`.
- Ghi chú `thu_o_may.sh kiem` dùng `curl -sI` (`HEAD /`) ở đợt 1 đã được sửa sang `curl -sD - -o /dev/null` (`GET /`) trong đợt 2 (`9c385952`).

---

## 4. Đợt 2 (09:43 – 09:57 27/11/2026, `0 USD` AWS, `0 USD` OpenAI) — Production Local 1 & Kiểm toán / Nghiên cứu Agentic–Harness
- **Gộp lên `main` (`9c385952`, nhánh `origin/p17-b-async-retrieval-limit`, `e` duyệt `READY`):**
  - `backend/embedding/full_corpus.py`: thêm `threading.RLock` quanh `FullCorpusDenseRunner` (`load`, `embed_documents_matrix`, `embed_queries`, `close`) và `OpenRouterDenseRunner` (`load`, `_embed`) ngăn PyTorch CPU thread oversubscription.
  - `backend/llm/assistant.py`: chuyển 3 lời gọi `context_builder.build(...)` sang `asyncio.to_thread(...)`.
  - `backend/api/gioi_han.py`: thêm `TRONG_SO_DUONG` (`/api/chat`, `/api/chat/stream`, `/api/anh/ung_vien` = `1`; `/api/so_tay` = `10`; `/api/ho_so` = `8`) áp dụng cho cả trần IP và trần tổng, giữ tương thích ngược `cho_qua()` và `tai_file=True`.
  - `deploy/docker/Caddyfile`: bỏ nén gzip cho `/api/so_tay` và `/api/ho_so` (`caddy validate` = `Valid configuration`).
  - `deploy/docker/dong_goi.sh`: thêm tuỳ chọn `HUE_MO_SO_TAY_HO_SO=1` (mặc định `0` cho tới khi kiểm thật trên `gpt-6-luna`); `deploy/docker/thu_o_may.sh`: sửa kiểm `GET /` CSP (`bash -n` đạt).
  - **Số đo kiểm chứng độc lập bởi `e` (`data/nghien_cuu_2026-11-27/bench_event_loop.py`, Qdrant `6335` 9.540 điểm):**
    - `3_concurrent_api_chat_x8`: `wall` `811,13 → 503,24 ms` (`-38%`), `/health` max `47,97 → 12,54 ms` (`p50 2,45 → 1,17 ms`).
    - `4_concurrent_to_thread_search_x8`: `wall` `874,00 → 476,02 ms` (`-45,5%`), `/health` max `21,03 → 5,57 ms`.
    - Pytest 8 file chạm (`HF_HUB_OFFLINE=1`): **96 passed in 29.09s**.
- **2 báo cáo riêng tư của `c` (`data/nghien_cuu_2026-11-27/`, `e` đối chiếu khớp 100% log & `file:dòng`):**
  - `KIEM_TOAN_PRODUCTION_LOCAL.md`: thống kê Prompt Caching thật trên `63` lượt `gpt-6-luna` (`16/63 = 25,40%` lượt trúng, `89.643 / 310.320 = 28,89%` tokens; `sua_lich` `60,83%`, `tro_ly_hue` `28,64%` ở vòng 2+); chỉ ra 2 điểm đáng sửa gọn (`CancelScope(shield=True)` thu hồi task khi client ngắt SSE ở `so_tay.py:148-155` & `ho_so.py:160-169`, và `--timeout-graceful-shutdown` cho `uvicorn`) cùng 4 điểm không nên sửa để tránh over-engineer.
  - `NGHIEN_CUU_AGENTIC_HARNESS_TOOLS_2026.md`: đề xuất 4 nâng cấp Harness (`TurnBudget` + *Actionable Feedback*, tách Fast-path vs Agentic Loop, chuẩn hoá `CancelScope` + graceful shutdown, *Trajectory Eval Gate* `0 USD` + Blue-Green Alias) và 4 tool mới dùng dữ liệu sẵn có (`tinh_ve_va_gio_tham_quan`, `so_sanh_diem_den`, `goi_y_phuong_an_mua_nang`, `tim_tuyen_di_lai`).

---

## 5. Đợt 3 (10:08 – 10:13 27/11/2026, `0 USD` AWS, `0 USD` OpenAI) — Sửa `CancelScope`, Graceful Shutdown & Dọn nhánh
- **Gộp lên `main` (`19cbb878`, nhánh `origin/p17-b-cancel-graceful`, `e` duyệt `READY`):**
  - `backend/api/routes/so_tay.py` & `backend/api/routes/ho_so.py`: khối `finally` của `_su_kien` chỉ `v.cancel()` các task chưa `done()` và bọc `await asyncio.gather(*viec, return_exceptions=True)` trong `anyio.CancelScope(shield=True)` để thu hồi sạch task con khi client ngắt kết nối SSE giữa chừng.
  - `deploy/docker/Dockerfile` & `deploy/docker/compose.yml`: thêm `--timeout-graceful-shutdown 15` cho `uvicorn` và `stop_grace_period: 20s` cho service `app`.
  - `backend/tests/test_so_tay.py` & `backend/tests/test_ho_so_chu_de.py`: thêm `test_ngat_ket_noi_sse_giua_chung_huy_va_don_het_viec_con` (`56 passed in 3.93s` trên worktree sạch có `data`, `docker compose -f deploy/docker/compose.yml config` hợp lệ).
  - **Dọn gọn:** xoá 4 nhánh tạm đã gộp sáng 27/11 (`p16-b-deploy-tf-docs`, `p16-c-docker-smoke-eval`, `p17-b-async-retrieval-limit`, `p17-b-cancel-graceful`) ở cả local và `origin` (giữ nguyên 9 nhánh hồ sơ/bản thử cũ), đồng thời đóng `/swarm`.

---

## 6. Đợt 4 — Đợt 1 Chiến dịch Tối ưu Harness · Agentic RAG · Tools (`11:10 – 11:55 27/11/2026`, `0 USD` AWS, `~0,052–0,059 USD` OpenAI)
- **Gộp lên `main` (`e432e32c`, nhánh `origin/p18-b-harness-chong-lap` của `b2`, `e2` duyệt `READY` với `428 passed`):**
  - `backend/llm/assistant.py`, `backend/config/settings.yaml`, `backend/api/routes/chat.py`, `backend/evaluation/trajectory_eval.py`: thêm `chong_lap_cong_cu` (chuẩn hoá tham số, chặn lặp kèm gợi ý trỏ `[N]`, ghi `lap: true`), `cuu_max_turns` (chạm trần có bằng chứng thì viết lại MỘT lần tắt hết tool), `siet_tro_chuyen`, và `trajectory_eval.py` đọc `application.log` (`219` lượt tổng / `66` `gpt-6-luna`).
- **Kết quả đo đối chứng cùng buổi trên `gpt-6-luna` (`e2` đo cổng `8039`, `0,039305 USD`, `data/thu_harness_2026-11-27/KET_LUAN_DOT1.md`):**
  - **1A — GIỮ & BẬT (`chong_lap_cong_cu: true`, `cuu_max_turns: true` → `64 MỞ / 7 TẮT`):** trên `n = 14` (`10` smoke + `4` đa ngày/lễ hội), chạm `max_turns` giảm `1/14 → 0/14` (`1a_multi_03` được cứu từ `0` nguồn → `8` nguồn hợp lệ, `0` lỗi citation), `p95` lượt thường giảm `14.488 → 11.987 ms`, vòng tool TB/p95 giảm `1,643/6,0 → 1,286/3,0`, `0` vi phạm sàn (`0,029046 USD`).
  - **1B — GỠ / GIỮ TẮT (`siet_tro_chuyen: false`):** trên `n = 18` câu đã thấy, bên TẮT đã đạt `0/6` bẫy lọt `tro_chuyen` (`CHƯA RÕ`), bật lên tốn thêm `+8,5%` tiền prompt (`0,010259 USD`).
- **Kiểm chứng Đợt 1C trên `gpt-6-luna` (`c2` chạy cổng `8039`, `e2` đối chiếu `100%`, `KET_QUA_1C_3_CUM_LUNA.md`):**
  - `so_tay` đạt (`9,92s` mặc định 2 ngày / `16,47s` 3 ngày thiên nhiên, `0` lỗi JSON), `ho_so_chu_de` đạt (`bien_dam_pha` `9,85s` / `ca_phe` `13,31s`, `0` lỗi), `sua_lich_hoi_truoc` đạt `5/5` lệnh gõ tay (`0` câu dự phòng). Chi phí đo `0,004828 USD` từ log + ước `~0,0083–0,0149 USD` cho `so_tay`/`ho_so` (phát hiện `so_tay.py` & `ho_so.py` chưa ghi `usd`/tokens vào log).
- **Thiết kế Đợt 2 & Đợt 3:** `c2` lập [THIET_KE_DOT2_DOT3.md](../../data/thu_harness_2026-11-27/THIET_KE_DOT2_DOT3.md), `e2` góp ý 3 điểm chốt trước khi mở Đợt 2.

---

## 7. Đợt 5 — Đợt 2 Chiến dịch Tối ưu Harness · Tools (`12:15 – 13:43 27/11/2026`, `0 USD` AWS, `0,169822 USD` OpenAI)
- **Chuẩn bị bộ câu & baseline (`c2`, `0,042205 USD`):** `data/thu_harness_2026-11-27/bo_cau_dot2.json` (`n=50` công khai, `0` `*sealed*`) + `BASELINE_DOT2.md` xác nhận cả hai nhóm đích chỉ đạt `1/8` khi công cụ tắt.
- **Gộp lên `main` (`aaafe678`, nhánh `origin/p19-b-tools-dot2` của `b2`, `e2` duyệt `READY` với `0` blocker / `0` major, `442 passed`) + mở cờ trên `main` (`66 MỞ / 7 TẮT`, `109 passed`):**
  - `backend/llm/mua_nang.py` (`goi_y_mua_nang: true`): gợi ý phương án trong nhà/có mái che theo buổi & cụm khi mưa/nắng, chặn 3 lớp khi bão/lũ hoặc mưa `>= 100mm`, tái sử dụng `flags.du_bao` và `trace.muc_luc_bai`.
  - `backend/llm/so_sanh.py` (`so_sanh_diem_den: true`): so sánh thực dụng 2–3 điểm từ `diem_v16`, `the_noi_bang` (không đọc `gio_mo_cua` nội bộ), `khoang_cach_bang`, `trace.muc_luc_bai`.
  - `backend/llm/generator_openai_full_corpus.py`: khoá `MAX_VONG_CONG_CU_TOI_DA = 6` trong `max_turns_for`.
  - `backend/api/routes/so_tay.py` & `ho_so.py`: log JSON `_cong_usage` ghi đủ `input_tokens`, `output_tokens`, `cached_tokens`, `usd`.
- **Kết quả đo đối chứng cùng buổi trên `gpt-6-luna` (`e2` đo cổng `8039`, `0,127617 USD`, `data/thu_harness_2026-11-27/KET_LUAN_DOT2.md`):**
  - **`H2_mua_nang` (`n=16`) — GIỮ & BẬT:** `1/8 → 5/8` (`+4/8 >= +3/8`), `0/4` lọt bão/lũ, `0/4` ngoài phạm vi, `0` lỗi citation, `cuu_max_turns` `2 → 0`, `p95 24,4s → 12,4s`, USD **`-40,5%`** (`0,031553 → 0,018774`).
  - **`H2_so_sanh` (`n=14`) — GIỮ & BẬT:** `1/8 → 6/8` (`+5/8 >= +3/8`), `0/3` hụt chiều sâu văn hoá, `0/3` ngoài phạm vi, `0` lỗi citation, `cuu_max_turns` `2 → 0`, `p95 22,2s → 13,2s`, USD **`-37,3%`** (`0,024455 → 0,015321`).
  - **`H2_cong_cong_cu_luon` (`n=20`) — GỠ / giữ `tu_khoa` (chuyển sang Nấc 2B):** lách từ khoá `0/10 → 10/10` (`0/10` gọi thừa), nhưng USD tăng **`+44,50%`** (vượt ngưỡng `<= +40%`; riêng câu thuần kho tăng `+89,0%` do lặp danh sách 40 địa điểm ở `KHOANG_CACH_MO_TA` + `GAN_DIEM_MO_TA` và `cached=0`).
- **Tổng chi phí OpenAI tích luỹ sau Đợt 2:** ~**0,98 USD** / trần **2–2,5 USD**.

---

## 8. Đợt 6 — Nấc 2B + Đợt 3A + 2 Báo cáo Nghiên cứu Chuyên sâu Paper & Repo (`13:47 – 14:13 27/11/2026`, `0 USD` AWS, `0,099352 USD` OpenAI)
- **Gộp lên `main` (`75f545c6`, nhánh `origin/p20-b-nang-cap-2b-3a` của `b2`, `e2` duyệt `READY` với `0` blocker / `0` major, `447 passed`) + mở `cong_cong_cu: linh_hoat`, giữ `anh.che_do_tu_choi: mac_dinh`:**
  - **Nấc 2B (`cong_cong_cu: linh_hoat`) — GIỮ & BẬT:** khử lặp bảng 40 địa điểm giữa `khoang_cach` / `gan_diem` / `so_sanh_diem_den` (chỉ in 1 lần) và cố định `extra_args={"prompt_cache_key": ...}` theo 4 biến thể trợ lý (`assistant_agent`, `assistant_history_agent`, `nhieu_y`). Đo cặp `gpt-6-luna` `n=20` (`0,028704 USD`): lách từ khoá **`0/10 → 9/10`** (chỉ trượt `cc_lach_04` thiếu ngày âm lễ hội trong kho), gọi thừa tool **`0/5`**, sàn ngoài phạm vi `5/5`, tổng USD **`-15,23%`** (`0,015535 → 0,013169`), `cached_tokens` tăng **`46,5% → 76,9%`** (riêng câu kho thuần `21,4% → 83,5%`, giảm **`-35,3%`** USD), `p95` `16.097 → 11.529 ms` (`-28,4%`), `0` lỗi (`KET_LUAN_DOT2B_3A.md`).
  - **Đợt 3A (`anh.che_do_tu_choi: confidence_gate`) — GIỮ TẮT (`mac_dinh`):** `c2` lập [bo_anh_dot3.json](../../data/thu_harness_2026-11-27/bo_anh_dot3.json) (`n=76`: `55` dương 55 tên + `18` âm/dễ nhầm + `3` bẫy chữ dán) + `chay_do_dot3_anh.py`; `e2` đo cặp `gpt-5-nano` (`0,070648 USD`): FP giảm `-50,0%` (`10/18 → 5/18`), bẫy chữ dán `fooled 1/3 → 0/3`, NHƯNG recall dương tụt nặng **`-17` top-1 (`49/55 → 32/55`) / `-20` top-3 (`52/55 → 32/55`)**, `0` cached, tăng `+18,9%` USD ⇒ không đạt ngưỡng cho phép (`<= 2` ảnh), giữ nguyên `mac_dinh`.
- **2 Báo cáo Nghiên cứu Chuyên sâu (`0 USD`, không cài/chạy repo ngoài, đã xoá `/tmp/hr_*_repos/`):**
  - `c2`: `data/nghien_cuu_2026-11-27/KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md` — khảo sát 7 trục paper 2024–2026 (*Adaptive-RAG*, *CRAG*, *Self-RAG*, *Sufficient Context*, *Search-R1*, *τ-bench*, *BFCL*, *RAG-MCP*, *VAD-R*, *ReCoVERR*, *RAGChecker*, *FRAMES*, *FACTS Grounding*) + tài liệu Anthropic/OpenAI/Manus + đọc code `5` repo Agent Harness (`openai-agents-python`, `pydantic-ai`, `smolagents`, `langgraph`, `haystack`).
  - `b2`: `data/nghien_cuu_2026-11-27/DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md` — đọc code `5` repo Agentic RAG / Eval / Verifier (`haystack`, `llama_index`, `ragas`, `dspy`, `ragflow`) và đề xuất phân loại theo 4 nhóm (*Phát triển mới · Bổ sung · Cải thiện · Tối ưu*).
- **Tổng chi phí OpenAI tích luỹ sau Nấc 2B + Đợt 3A:** ~**1,08 USD** / trần **2–2,5 USD**.

---

## 9. Đợt 7 — Đồng bộ Giáo trình (`bai_hoc/giao_trinh/`) & Thu gọn cuối đợt (`14:22 – 14:44 27/11/2026`, `0 USD` AWS, `0 USD` OpenAI)
- **Gộp lên `main` (`d341fd96`, nhánh `origin/p20-d-giao-trinh-2711` của `d2`, `21` file `+220 / -86`):**
  - `d2` cập nhật đồng bộ toàn bộ `00_GIAO_TRINH.md`, `21_HARNESS.md`, `24`, `26`, `32`, `35`, `36`, `37`, `38`, `40`, `41`, `43`, `44`, và 8 phụ lục (`PL_A 190 · B 140 · C 258 · E 240 · F 197 · G 352 · H 210 · I 223`; **66 mở / 7 tắt**, `cong_cong_cu: linh_hoat`, `anh.che_do_tu_choi: mac_dinh`).
  - `e2` review chéo bắt & sửa sạch 3 điểm (`bedrock.cong_cong_cu` chỉ có `tu_khoa | luon`, đường dẫn `backend/evaluation/{smoke,trajectory}_eval.py`, phân biệt `22/55` `khong_nhan_ra` vs `23/55` trượt top-1) ⇒ duyệt `READY` (`0` blocker, `0` leak đường dẫn riêng tư).
- **Trạng thái chốt đợt:** `main` đồng bộ sạch, Qdrant `:6335` đủ **9.540 điểm**, cổng `8010/8039/8880` rỗng, `/tmp/hr_*_repos/` đã xoá sạch, đã thu gọn `/swarm`.

---

## 10. Đợt 8 — Đợt 4A (Đánh giá 3 tầng + Tối ưu Harness/Tools) · Thiết kế Đợt 5 · Đồng bộ Giáo trình (`15:28 – 16:49 27/11/2026`, `0 USD` AWS, `0,265824 USD` OpenAI)
- **Gộp lên `main` (`cd217536`, `f245963c`, `442055ba` — `68 MỞ / 8 TẮT`):**
  - **`eval` (`origin/p21-c-eval-dot4a` @ `41e45fed`, `38 passed`):** `backend/evaluation/faithfulness_eval.py` (chấm bám nguồn ngữ nghĩa 2 bước offline trên JSONL `full_corpus_eval.py` & Đợt 4A), `ToolCallAccuracy` (`0 USD`) trong `backend/evaluation/trajectory_eval.py`, bộ test + bộ đo `data/thu_dot4_2026-11-27/`.
  - **`builder` (`origin/p21-b-harness-dot4a` @ `ce051c9d`, `114 passed`):** 3 công tắc mặc định tắt (`kiem_du_bang_chung`, `canh_bao_vong_con_lai`, `toi_uu_dot2_va_viet_lai`), vá `cached_tokens` ở `backend/api/routes/anh.py`, `backend/tests/test_dot4a_harness.py`; sau khi mở 2 công tắc trên `main`, vá tương thích `canh_bao_vong_con_lai` ở `_assistant_for` (`generator_openai_full_corpus.py`) và cập nhật `test_dot4a_harness.py` + `guides/RUNBOOK_BAN_GIAO.md` (**`108 passed` + `88 passed`**, `verifier` duyệt `READY` ở `#27`).
- **Kiểm định & Đo cặp thật trên `gpt-6-luna` (`verifier` đo cổng `8039`, `0,265824 USD`, `data/thu_dot4_2026-11-27/KET_LUAN_DOT4A.md`):**
  - **Kiểm định bộ chấm & Mốc nền:** `faithfulness_eval.py` đạt **`15/15 = 100%`** khớp nhãn tay (`3/3` bắt gán sai `[n]`, `0,005063 USD`); mốc Golden `20` câu đạt `mean_faithfulness_cited = 0,8833` (**`17/20 = 85%` strict**, `0` misattributed, `0,014730 USD`); `ToolCallAccuracy` (`0 USD`) xác nhận khớp Đợt 2 (`2b_linh_hoat` `19/20 = 95%`).
  - **V1 `kiem_du_bang_chung` (`n=36`) — GIỮ TẮT (`false`):** nền đã tránh bịa `18/18`, bật thêm `+0/18`, tăng `+10,7%` USD (`0,031803 → 0,035197`), làm 1 ca bỏ sót `khoang_cach` (`suf_mix_17`).
  - **V2 `canh_bao_vong_con_lai` (`n=18`) — GIỮ & BẬT (`true`):** giảm `cuu_max_turns` **`2 → 0`**, cắt `50%` gọi thừa (`6 → 3`), `ToolCallAccuracy` F1 `0,831 → 0,849`, cache bước `>=2` `91,00% → 94,58%`, giảm **`-6,84%`** USD (`0,028547 → 0,026594`).
  - **V3 `toi_uu_dot2_va_viet_lai` (`n=38`) — GIỮ & BẬT (`true`):** `H2_mua_nang` **`4/8 → 8/8`** (USD `-4,3%`), `H2_so_sanh` **`5/8 → 7/8`** (`ToolCallAccuracy` `0,500 → 0,875`, USD `-16,4%`), `4A_viet_lai` USD `-10,4%`, tổng USD **`-10,02%`** (`0,057429 → 0,051674`). Giới hạn: `_chan_doan_viet_lai` mới kiểm unit test (`0/8` ca kích hoạt live); `vl_01` bên bật có `1` lần gọi nhầm `thoi_tiet(bao_lu)` ở vòng 7.
- **Đồng bộ Giáo trình (`b1b69754`, `0 USD`):** `docs` cập nhật `22` file `bai_hoc/giao_trinh/` (`e92e1455`, phụ lục `A 192 · B 144 · C 262 · E 240 · F 200 · G 353 · H 212 · I 225`), `verifier` duyệt `READY` (`0` blocker/major).
- **Thiết kế Đợt 5 Multi-Agent & Tính tự chủ (`0 USD`, gác sang phiên sau theo xác nhận chủ dự án `15:57`):** `data/dot5_multi_agent_2026-11-27/B_PHAN_TICH_KY_THUAT.md` (`455` dòng) và `THIET_KE_DOT5.md` (`242` dòng) cho cả 3 cụm (Google Calendar, Slide Designer Agent, Action Executor tách biệt quyền).
- **Tổng chi phí OpenAI tích luỹ sau Đợt 4A:** ~**1,35 USD** (trần cũ 2–2,5 USD, chủ dự án đã xác nhận duyệt nếu vượt).
