# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 17:09 25/10/2026 (A, **KẾT PHIÊN tối 25/10** — User dừng: "session sau chúng ta sẽ kiểm tra lại"). Cách dùng:
`WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở; lịch sử phiên ở `PROJECT_HISTORY.md` (mục 25/10 tối).
Bản handoff đầy đủ trước khi rút gọn lần này: `git show bc568f1:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống lúc kết phiên:** `main` (commit cuối: `git log -1`, ghi ở `sessions/STATUS_A.md`). **Chatbot không đổi** (context 5,
không NFC) — mọi thay đổi 8.2 chưa vào `main`. Qdrant `:6335` còn **1** collection `hue_full_corpus_7a2_e5_small_384` (8.459).
Nhánh **`p82-b1`** (`f23d396`, đã push): code Bước 1 của 8.2 (context 10 + NFC), **chưa A review, chưa merge**. Repo `chatbot-hue`
**PUBLIC** (hook `.githooks/pre-commit`). File untracked `báo cáo nghiên cứu github.txt` ở gốc: của User cho Phase 9 — **không đụng**.

**Đang ở đâu (3 mạch việc):**

1. **Rà code Phase 0–7 — ĐANG LÀM, DỞ** (User 16:5x: "dừng 8.2, rà code trước khi bắt đầu phase mới"). User hỏi về **code**
   (file, folder, guide), **không phải dữ liệu kho**. Đợt `report_agent/2026-10-25_ra_soat_code/`. B25 (luồng dựng index + nền) và
   C34 (luồng trả lời + đánh giá) chỉ đọc, 0 USD; mỗi bên lưu phần dở trong `ra_soat_code_<B|C>.md` (đầu file ghi đã rà / chưa rà).
   Tiêu chí, khuôn finding, phạm vi: mục "Việc đang mở" dưới.
   **Phát hiện sớm (tạm, chưa kiểm chéo):** B-01 = C-01 (B và C **tìm độc lập**): API nạp `core.schema` hai lần (`core.*` và
   `backend.*`) ⇒ bắt hụt lớp lỗi retrieval — Qdrant lỗi khi hỏi ra 500 thay 503; index cũ lúc khởi động ra 503 thay 409 (C chứng minh
   danh tính lớp bằng script `data/ra_soat_code_2026-10-25/tools/`; tác động HTTP suy ra từ code, chưa tái tạo bằng lỗi thật). Gốc:
   `ingestion/full_corpus_pipeline.py` import `backend.*` + `app.py` chèn gốc repo vào `sys.path`. **C-02:** `g2_generate.paired` không đổi
   dấu cho `refusal` ⇒ thắng / thua ngược (input nhỏ chứng minh) — **plan E1 §4 / §5 phải sửa** khi 8.2 chạy lại (sha mới). Ai sửa
   B-01 / C-01: quyết khi User chọn mục sửa (chạm cả hai phạm vi). Sub-agent của B (guide, test / notebook) và của C (3 cái) bị dừng,
   **chưa ra kết quả** ⇒ giao lại.
2. **Phase 8.2 — TẠM DỪNG** (spec User duyệt 16:21, sha `dabae90b2b60`, `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`):
   - B0 (mốc người đọc cặp mù): file ready (B24 review 2 vòng) — **User đọc khi tiện**: `data/phase_8_2/b0/nhan_xet_user.md`.
   - B1 (context 10 + NFC): **B xong, T1–T5 đạt**, 0,0369 USD; report `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_implementation.md`
     (sha `bb5fea83aeb6`, ở nhánh `p82-b1`) — **chờ A review**. A/A context 10: Completeness đổi 5 / 176 câu (dev chính 2 / 88);
     lỗi citation B1 12 vs G2.1a 8 (chỉ 2 câu chung) ⇒ nhiễu citation lớn (cần cho E2).
   - E1 plan (C): `phase_8_2_e1_plan.md` sha `f86240418ca1` — **chờ B review** + **A trả lời Q1–Q3** (plan §10).
   - E2, E3a, E3b, B3 (câu kín): chưa bắt đầu.
3. **Rà nội dung kho (C32) — XONG**, A review ready. Là A **hiểu nhầm** câu hỏi của User (User quan tâm code); giữ làm hồ sơ cho đợt build
   lại index: 139 mục (mâu thuẫn chắc 22 / có thể 53; có thể cũ 4 / 33; khác 5 / 22), danh sách private
   `data/ra_soat_kho_2026-10-25/danh_sach.md`. Không làm gì thêm trừ khi User yêu cầu.

**Thứ tự việc phiên sau:**

1. Mở A/B/C bằng `START_SESSION.md`; A `ListAgents`; A **hỏi lại quyền phiên** (§9.8: điều phối rộng, trần tiền).
2. **Rà code làm tiếp:** B25 / C34 tiếp từ phần dở (đọc đầu file `ra_soat_code_<B|C>.md`) → xong thì **kiểm chéo** (B kiểm top 5 của C,
   C kiểm top 5 của B, chạy lại bằng chứng) → A tự kiểm 2–3 khẳng định chính, gộp `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`
   → **trình User chọn sửa gì** (skill `propose-options`). Sửa code là việc rủi ro trung bình: plan + review chéo + test / đường thật.
3. **Thứ tự giữa sửa code và B1** (hỏi User, câu 3 dưới): B1 sửa `backend/config/settings.yaml`, `backend/core/settings_loader.py`,
   `backend/retrieval/full_corpus.py`, `backend/tests/test_full_corpus_retrieval.py`, `backend/tests/test_phase6_settings.py`. Sửa code
   chạm các file đó hoặc đường tìm kiếm / sinh ⇒ sau khi rebase `p82-b1` phải **chạy lại T1–T2** của B1 (free) — không dùng lại bằng
   chứng cũ khi đầu vào đổi (`Session_Prompt.md` §6).
4. Chạy lại 8.2 khi User nói: A review B1 → B0 (User đọc ⇒ sub-agent mới tóm nhãn — **không phải B**, B đã thấy khóa ⇒ A ghép khóa
   ⇒ luật dừng spec §3.4) → merge `p82-b1` + 4 chỗ `bao_cao_he_thong/` → E1 (B review plan, A trả lời Q1–Q3, duyệt sha).

## Câu hỏi cho User (phiên sau)

1. **Quyền phiên** (điều phối rộng? trần tiền ≤ 1 USD?).
2. **Rà code:** khi có bảng tổng hợp — sửa mục nào, theo thứ tự nào.
3. **Thứ tự sửa code ↔ B1:** (a) A review + merge B1 trước (nhỏ, đã đạt; mọi sửa sau đo trên runtime mới) rồi sửa code; hay (b) sửa code
   trước, rebase B1 và chạy lại T1–T2. A nghiêng (a) — B1 chỉ 5 file nhỏ, đã có bằng chứng; nhưng User đã nói dừng 8.2 nên hỏi.
4. **Đọc cặp mù (B0):** `data/phase_8_2/b0/nhan_xet_user.md`, 20 câu, ~30–45 phút, khi tiện (cần trước khi giữ context 10 vào chatbot).
5. Rà kho C32 (139 mục): để đợt build lại index; muốn tra ngoài 69 mục qua ChatGPT thì A viết yêu cầu.
6. Tên dự án khác còn trong 15 file đã commit + lịch sử git (repo public) — A đề xuất để nguyên; gỡ khỏi lịch sử là phá hủy, chỉ khi User yêu cầu.
7. 3 câu kín A đã thấy: giữ (spec 8.2 §3.7 báo cả 36 và 33 câu) — đã ghi trong spec, chỉ hỏi nếu User muốn đổi.
8. **Sổ cải tiến vòng 3** (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`): duyệt / bác **W14** (A nhắc lại ý User một câu khi câu hỏi có
   nhiều cách hiểu — sau S19 rà kho thay vì rà code) và **W15** (quét file session khác trước khi commit — sau S20).

## Câu hỏi A còn nợ (phiên sau A trả lời, không cần User)

- Plan E1 §10: **Q1** test không đủ câu cho CI 95% — chấp nhận "xác nhận hướng" trên test (lệch `run-experiment` §4)? **Q2** chỉ E1b hay
  thêm E1a (P1 nguyên văn; Holm cần 5 / 0)? **Q3** số A/A lấy từ report B1 (sau khi A review B1).
- Ghi chú B (vòng 3 spec): plan E3b thêm mức tụt Completeness / lỗi citation như E3a.
- C-02 (rà code C34): sửa `paired` cho `refusal` trước khi dùng cho E1; C sửa plan E1 ⇒ sha mới ⇒ B review.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-00` (tối 25/10) | Claude Opus 5.5 | trực tiếp | brainstorm + spec 8.2; B0 prep; review B1 plan, C32; dừng 8.2; giao rà code | kết phiên 17:0x — `STATUS_A.md` |
| B — thực thi | `hue-rag-de` (tối 25/10) | Claude Opus 5.5 | trực tiếp | B22 review spec; B23 B1; B24 review B0; B25 rà code (dở) | xem `STATUS_B.md`; 0,0369 USD |
| C — thực thi | `hue-rag-d6` (tối 25/10) | Claude Opus 5.5 | trực tiếp | C32 rà kho; C33 plan E1; C34 rà code (dở) | xem `STATUS_C.md`; 0 USD |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã
  duyệt: A tự duyệt, báo sau (User 25/10); Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report;
  code luôn `uv run` trong `.venv`; thư viện thừa giữ nguyên; luôn thử + so baseline trước khi chọn (User 24/10 20:49).
- **Phiên tối 25/10 (User 15:5x) — HẾT HẠN, hỏi lại phiên sau:** A tự điều phối B/C rộng; API ≤ 1 USD cả phiên (dùng 0,0369). Trần 8.2: 0,5 USD (trong spec).
  Luật kỹ thuật giữ từ phiên trước: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- File untracked `báo cáo nghiên cứu github.txt` (gốc repo): của User, dùng cho Phase 9 — **không đụng, không commit**.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra.

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024 | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_draft.jsonl` | đoạn đúng 55 câu (40 dev / 15 test) | `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (82 / 65 / 29) | `0b65d1c138d2` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín chính thức — **không đọc** tới mốc cuối 8.2 | md5 `ddc59587b502` |
| `data/phase_8_1/baseline/g0_6_manifest.json` | manifest khóa G0.6 (hash mọi file mốc) | `9ea480d0d083` |
| `data/phase_8_1/{g1,g2,g3,g4,g4k}/` | kết quả từng câu của các gate | — |
| `data/phase_8_1/tools/` | script dùng lại (`make_sealed_official.py`, `select_gold.py`, …) | — |
| `data/phase_8_1/external_lessons_private.md` | bài học dự án khác của User | — |
| `data/phase_8_2/b0/` | đọc cặp mù: `doc_cap_mu.md` (`37b66efb3499`), `nhan_xet_user.md` (User ghi), **`khoa.json` chỉ A** (`5b9240842b7b`), `tools/make_pairs.py` | — |
| `data/phase_8_2/b1/` | kết quả chạy B1 (sinh 176 câu, judge, retrieval, nfd-check) | — |
| `data/ra_soat_kho_2026-10-25/` | rà kho C32: `danh_sach.md` 139 mục, `sub_g*.md`, `tools/` | — |

## Việc đang mở

### Rà code các Phase trước (User 16:5x 25/10: dừng 8.2, rà code trước khi đi tiếp)

User hỏi về **code** (file, folder, guide của các Phase), không phải dữ liệu kho (C32 là A hiểu nhầm — giữ làm hồ sơ).
Đợt `report_agent/2026-10-25_ra_soat_code/`. Chỉ đọc, 0 USD. Rà trên `main` sạch (`f4353e2`; code B1 cất ở nhánh `p82-b1`).

**Chung cho B25 và C34:**
- **Tiêu chí** (skill `practical-project-coding` + `Session_Prompt.md` §7): (1) code thừa / không còn được gọi / sót Foods-Phase cũ —
  **chứng minh bằng grep** import + lời gọi (cả gọi động, CLI, notebook, test); (2) dễ đọc, theo được data flow, phức tạp quá nhu cầu
  (abstraction, wrapper, cấu hình, fallback, validator phòng xa); (3) hằng ẩn, đọc settings sâu, khâu dính; (4) test: bảo vệ hành vi
  thật hay không, còn mock / stub, test thừa, test paid / ghi Qdrant nằm lẫn; (5) guide / notebook / docstring lệch code đang chạy;
  (6) hiệu năng (khởi động, độ trễ mỗi câu) — chỉ đo khi cần cho một finding, chạy thật không paid; (7) cơ hội phát triển / so sánh —
  ghi **giả thuyết**, cách thử (theo `run-experiment`), không kết luận.
- **Không lặp cái đã biết:** đối chiếu `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md` §4 (khâu dính)
  và `phase_8_1_decision_inventory.md` §6 (lệch tài liệu–code); trùng thì ghi "đã biết (nguồn)" kèm điều mới nếu có.
- **Được:** đọc mọi code / test / guide / notebook / `settings.yaml`; chạy test **không paid, không ghi Qdrant** (liệt kê file, không
  `--deselect` — `Project_Status.md` §8); script đo trong `/tmp`; ≤ 3 sub-agent mỗi session (brief đọc lại trước khi gửi; tự kiểm 2–3
  khẳng định chính của sub-agent bằng file thật). **Không:** sửa code / test / guide; gọi API trả phí; ghi Qdrant; mở câu kín; chép nội
  dung kho / Golden vào report.
- **Mỗi finding:** id (`B-xx` / `C-xx`), khâu, `file:dòng`, loại (1–7), mức (cao / vừa / thấp: tác động × rủi ro khi để nguyên), quan sát
  (bằng chứng: lệnh grep / test / số đo), *suy ra* tách riêng, đề xuất sửa (nhỏ nhất đủ), cách kiểm khi sửa (đường thật), rủi ro khi sửa.
  Đầu file: **top 10** theo mức; cuối: phần **không rà được** / chưa chắc.
- **Đầu ra:** `report_agent/2026-10-25_ra_soat_code/ra_soat_code_<B|C>.md` (tracked — repo public, không nội dung private). Xong nhắn A.
- **Kiểm chéo:** khi cả hai xong, B kiểm top 5 của C, C kiểm top 5 của B (chạy lại bằng chứng) ⇒ A gộp `TONG_HOP.md`, trình User chọn sửa gì.

- **B — B25: rà luồng dựng index + nền** · `backend/ingestion/`, `embedding/`, `vectorstore/`, `scoring/`, `core/` (gồm
  `settings_loader.py`), `scripts/`, `backend/config/settings.yaml`, `pyproject.toml` (dependency không dùng: chỉ ghi — User giữ thư viện
  thừa), `docker-compose.yml`; test của các phần đó; notebook `03`, `04`; guide `phase_0`–`phase_4`, phần index của
  `guides/full_corpus_rag.md`, `guides/README.md`.
  **Trạng thái 17:07 (B): DỞ** — đã rà ingestion pipeline / source_state / preview, embedding, scoring, vectorstore (qdrant, points), core,
  settings, pyproject, docker-compose; chưa rà chunker / markdown_blocks / upsert, test, notebook, guide. 10 finding tạm, B-01 cao (module nạp hai
  lần ⇒ API bắt sai lớp lỗi). `scripts/` không tồn tại. File `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md`.
- **C — C34: rà luồng trả lời + đánh giá** · `backend/retrieval/`, `reranking/`, `llm/`, `api/`, `evaluation/`, `frontend/`; test của các
  phần đó; notebook `06`; guide `phase_5`–`phase_9`, `llm_rag_reference_for_hue_rag.md`, phần trả lời của `full_corpus_rag.md`;
  `backend/experiments/phase_8_1/` chỉ hỏi "còn cần giữ / chạy lại được không".
  - **Trạng thái (C, 17:08 25/10): DỞ** — `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md` (đầu file: đã rà / chưa rà). 8
    finding, 2 mức vừa: C-01 runtime nạp `core.schema` hai lần ⇒ API trả sai mã lỗi khi retrieval lỗi (gốc chung với phạm vi B25);
    C-02 `g2_generate.paired` ngược dấu với `refusal` (ảnh hưởng plan E1). 0 USD.

### Phase 8.2 — TẠM DỪNG 16:5x (User)

- Đã xong: spec duyệt (`dabae90b2b60`); B0 file đọc cặp mù ready (User đọc khi tiện: `data/phase_8_2/b0/nhan_xet_user.md`); **B1 xong**
  (B, T1–T5 đạt, 0,0369 USD — report `phase_8_2_b1_implementation.md` sha `bb5fea83aeb6`, **chưa A review**); code B1 ở nhánh
  **`p82-b1`** (`f23d396`, đã push, chưa merge main). Plan E1 (C, sha `f86240418ca1`) chờ B review + A trả lời Q1–Q3 (§10 plan).
- Chạy lại: A review B1 → (B0 xong) → merge `p82-b1` → E1. Tiền 8.2 đã dùng: **0,0369 USD** / 0,5.


- Chi tiết từng việc 8.2 đã giao phiên tối 25/10 (B22 review spec, B23 B1, B24 review B0, C32 rà kho, C33 plan E1 — mục tiêu, đọc gì,
  quyền, tiêu chí): `git show bc568f1:session_prompt/CURRENT_HANDOFF.md` mục "Việc đang mở".
- Sổ cải tiến `session_prompt/SO_CAI_TIEN_CACH_LAM.md`: W11–W13, I4 `đang thử` (vòng 2); **vòng 3 (17:07): S19–S22, đề xuất W14, W15 chờ
  User duyệt** (câu hỏi cho User mục 8).
