# STATUS C — cập nhật 2026-10-25 11:26

Terminal: `hue-rag-a1` (25/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi
User 25/10: việc A giao = "làm đi"; xong báo cáo, nhắn A, chờ việc.

## Đang làm (25/10)
- **C24 (A giao 11:40) — thêm dấu mọi câu kín, C không đọc nội dung.** Bước 1 xong 11:41: backup `cp` →
  `sealed_authoring_v3_backup.jsonl` (md5 `0377e966ada5` = v3) + `sealed_user_sample_v3_backup.md` (`ab9a6cbe62da`);
  check trước sửa exit 0 (15/6/7/5/3). **XONG 11:48:** sub-agent sửa thêm dấu 16 dòng (chỉ `question`; máy C kiểm:
  bỏ dấu = bản cũ, NFC, 20 dòng giống byte); sub-agent kiểm mới ĐẠT, 0 dòng thiếu dấu; check exit 0; kín v4
  `a095e08bd7ac`; mẫu bản 4 `ad205c839bd0`. §8 trong `phase_8_1_g0_4_sealed_review.md`. Chờ User: 2/21/33, mẫu 4,
  (tùy) dòng 3/19/13 gõ tắt. **Bẫy:** báo cáo sub-agent kiểm lộ tên file nguồn (chủ đề) cho C — lần sau cấm cả tên
  file nguồn trong báo cáo cuối.
- **C26 XONG 12:31** — kín v6 `631334704fdd` (đổi 2/6/21/33), kiểm độc lập ĐẠT, 36/36 natural (`d1f7c235b83c`), mẫu bản 5
  `4f7fe6df5cca` (17 dòng); §10. Đã xóa /tmp/c26_*. Chờ User xem mẫu 5 → A khóa G0.6.
- **C27 XONG** — review sửa 10 đáp án Golden: ready; m1 (92) / m2 (41) A sửa, C kiểm lại → đóng 12:30 (§7). Official
  `0f7dbf41b422`, smoke `d80b58c50f38`; check thật exit 0; pytest 27.
- A dặn (12:27, User ngủ trưa): report G4/G2 của B phải đủ thông số từng lượt (model + revision, device thật,
  max_length, pool, top-k, sha tập câu, seed, latency, token/USD, lệnh, đường dẫn kết quả) — thiếu là finding.
  Ưu tiên: G4 → C26 → C27. Thấy `pyproject.toml` + `uv.lock` đổi trong working tree (B?) — soi khi review G4.
- **C26 (A giao, User duyệt 12:20) — áp sửa câu kín:** 2/21/33 theo đề xuất v3, dòng 6 bỏ quy định ngoài câu hỏi,
  3/19/24/29/33 giữ. 12:21 backup `sealed_authoring_v5_backup.jsonl` (`6d413c8d98fa`), `sealed_realism_v5_backup.jsonl`
  (`b7a679d7e6f0`), `sealed_user_sample_v4_backup.md` (`ad205c839bd0`). Sub-agent sửa mới đang chạy → kiểm (mới) cập nhật
  realism + mẫu bản 5 → §10. Sau đó: review 10 đáp án Golden của A (C được đọc Golden).
- **C25 (A giao 12:05) — sửa / rà `reference_answer` câu kín**, C không đọc nội dung lẫn `sealed_user_feedback_private.md`.
  12:06 backup `cp` → `sealed_authoring_v4_backup.jsonl` (`a095e08bd7ac`). **XONG 12:13:** 4 đáp án sửa (11, 18, 26, 36;
  chỉ `reference_answer`, keyword giữ — máy C kiểm), kiểm độc lập ĐẠT, check exit 0, kín v5 `6d413c8d98fa`; §9. Chờ User:
  dòng 6 + dữ kiện phụ 3/19/24/29/33 (giữ hay dặn judge); mẫu bản 4 chưa có đáp án mới 11/18/36. Đã xóa /tmp script
  sub-agent C24/C25.
- **Review G4 thêm (A 11:50):** `backend/reranking/cross_encoder.py` là production ⇒ chứng minh mặc định giữ hành vi
  (`max_length=None` = mặc định CrossEncoder; `loaded_device` không đổi đường runtime); chạy pytest reranker (không paid).
- **Tiếp (A giao):** review từng gate G4/G2 khi B nhắn — đối chiếu plan `a4adfc8eedd9` (commit `b9789f4`, sha bản commit
  khớp); kiểm log đủ 4 điều kiện GPU §0 (cuda thật / device tham số, nvidia-smi không session khác, câu thử) và mỗi lượt
  = 1 cấu hình ≤ 30 câu, trần 60 s / 20 phút.
- **C23 ĐÓNG (A duyệt + commit `b9789f4`) — vòng 2 ready**: plan `a4adfc8eedd9` sẵn sàng để A duyệt, mọi finding đóng (review §7; bản sao
  `/tmp/c23/plan_a4adfc8e.md`). Tiếp: chờ A giao (review G4/G2 khi B chạy). 0 USD, không GPU.
- (vòng 1) 11:31 **changes_requested**. G1 §7: mọi số khớp, m1/m2 B đã sửa (đóng).
  Plan `43086f053db8`: M1 G2.1/G2.4 thiếu tiêu chí ghi trước; M2 luật G4 bỏ MRR@10 của spec không khai; M3 G4-B cần mốc
  "native p100 không rerank" (G1: 15/30 vs runtime 12/30); m3–m6. Chờ B sửa → C kiểm diff với `/tmp/c23/plan_43086f05.md`.
- Khai báo sửa: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_b16_review.md` (mới), file này, dòng C trong
  `CURRENT_HANDOFF.md`. Output tạm: `/tmp/c23_*.json`.
- Sửa ghi chép cũ: §7 sealed review và STATUS_B đã được A commit ở `6c168e6` (mục "Chưa commit" dưới là cũ).

## Kết phiên 24/10 (cũ)
- **C chưa đọc nội dung câu kín** (`knowledge-base-hue/evaluation/phase_8_1/sealed_authoring.jsonl`):
  - mọi review câu kín (C17, C20, C22) đều do sub-agent mới làm;
  - C chỉ đọc báo cáo tóm tắt (số dòng / số đếm / nhãn), so dòng bằng md5/diff, và chạy `check --authoring`
    (chỉ xem exit code, số đếm);
  - phiên sau giữ nguyên: muốn kiểm câu kín thì giao sub-agent mới, C không mở file.

## Đang khai báo sửa
- không

## Chưa commit (của C) lúc kết phiên
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_4_sealed_review.md` (+54 dòng: §7 review lần 3, C22).
- `session_prompt/sessions/STATUS_C.md` (file này) và dòng C trong `session_prompt/CURRENT_HANDOFF.md`.
- Khác trong working tree **không phải của C**:
  - B: `backend/experiments/phase_8_1/g1_retrieval.py`, `phase_8_1_g1_implementation.md`,
    `phase_8_1_g2_g4_plan.md` (untracked), `STATUS_B.md`;
  - User: `báo cáo nghiên cứu github.txt`.

## Phiên sau (việc của C, chờ A giao)
1. **Câu kín, còn 3 dòng `capability_only` (2, 21, 33)** theo tiêu chí độ tự nhiên của User.
   - Sub-agent lần 3 đã đề xuất cách hỏi lại, nằm trong `sealed_review_notes_private_v3.md`.
   - Nếu A/User cho sửa: người sửa là sub-agent; C kiểm mù bằng **một sub-agent mới** chỉ cho các dòng đổi.
   - So dòng với bản v3: md5 `0377e966…`, sao ở `/tmp/c22_sealed_v3.jsonl`; `/tmp` có thể mất, khi đó
     cần A giữ bản trước khi sửa.
   - `sealed_realism.jsonl` của người sửa đang ghi cả 36 dòng là natural, lệch ở 2, 21, 33 → cập nhật theo
     nhãn cuối.
   - User cần duyệt mẫu `sealed_user_sample.md` (bản 3, 15 dòng).
2. **Review các gate 8.1 tiếp theo khi B nhắn** (G2/G4: `phase_8_1_g2_g4_plan.md` của B). Nhớ:
   - G2.2 đo tách hai nhóm: câu đủ đoạn đúng trong context vs câu thiếu một phần (phát hiện C21: 22/22 từ
     chối nhầm thiếu fact trong context; ngược B4);
   - G3 harness phải lấy id context từ `packed.sources` (m1 C21) và truyền `record_path` +
     `sparse_state_path` (m1 C18);
   - G3 cần thêm tham số `chunks` cho `build_candidate` (A đồng ý, giao khi mở G3);
   - report G1/G3 báo số câu hòa điểm ở biên pool (m1 C19).

## Vừa xong hôm nay (2026-10-24, phiên tối)
| Việc | Kết quả | Commit A |
|---|---|---|
| C9 review B9 (dọn Foods) + kiểm sức khỏe | ready; pytest 191; retrieval giống byte; /health 200; payload 8.459×7; `phase_7_cleanup_review.md` | `1832201` |
| C10 4 báo cáo khâu về mẫu mới | bản 2, số đo giữ nguyên | `c57ec43` |
| C11 bảng rà 56 quyết định Phase 0–7B | `phase_8_1_decision_inventory.md` (3 sub-agent gom dữ kiện) | `3077b9b` |
| C12 sửa 4 lỗi báo cáo cũ của C | bản 3; H-report §9 đính chính | `3077b9b` |
| C13 / C13b báo cáo khâu sau B9 | TIM_KIEM b4, KHO_DU_LIEU b3, SINH b4, GOLDEN b4 | (A commit cùng B10) |
| C14 kiểm URL nghiên cứu ChatGPT 8.1 | 22/29 nguồn; Qdrant 1.18.3; `phase_8_1_research_url_check.md` | đợt 8.1 |
| C15–C15d review spec 8.1 (v1→v4) + gỡ chi tiết dự án khác | `phase_8_1_spec_review.md` | spec duyệt 20:49 |
| C16 G0.1 split 120/56 + G0.2 compare theo cặp | đối chứng âm/dương PASS; B review đạt, 3 minor đã sửa | `b8dbe95` |
| C17 / C20 / C22 review mù câu kín lần 1–3 | lần 3: 5/5 dòng đổi OK, còn 3 capability_only; `phase_8_1_g0_4_sealed_review.md` §1–§7 | §7 chưa commit |
| C18 review B11 (tham số mặc định-như-cũ) | ready; `phase_8_1_g0_5_review.md` | `b8dbe95` |
| C19 review B13 (phá hòa sparse native) | ready; mốc native `1fbb5c17…`; `phase_8_1_b13_review.md` | đã commit |
| C21 review G1 (B15) | ready; chạy lại 4 cấu hình trùng từng câu; `phase_8_1_g1_review.md` | `8156395` |

Paid đã dùng phiên này: **0 USD**. Quota Claude Code cho sub-agent: C11 ~620k, C17 ~185k, C20 ~124k,
C22 ~111k token.

## File private đang dùng (không commit)
- `knowledge-base-hue/evaluation/phase_8_1/split.json`: chia 120/56, seed 20261024, SHA `e2b1788d…`.
- `knowledge-base-hue/evaluation/phase_8_1/sealed_authoring.jsonl` (C **không đọc**), `sealed_realism.jsonl`,
  `sealed_review_notes_private{,_v2,_v3}.md`, `sealed_user_sample.md` (bản 3).
- `data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl`: mốc native, SHA `1fbb5c17…`.
  Mốc dense: `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`, SHA `cefb2d1a…`.
- `data/phase_8_1/g1/c_*.jsonl`: các lượt chạy lại của C khi review G1. Tên tiền tố `c_` để không ghi đè
  file của B.
- `data/phase_8_1/external_lessons_private.md`: ghi chú về dự án khác của User (A viết). Không chép vào
  file tracked.

## Script tạm ở /tmp (mất khi khởi động lại; không commit)
- `/tmp/c11/`:
  - `brief_common.md` (brief sub-agent rà quyết định);
  - `nfc_probe*.py`;
  - ghi chú vùng `area2_verified.md`, `area3_verified.md`, `nfc_facts.md`.
- `/tmp/c9/health_c.py` (kiểm sức khỏe kiểu B1), `/tmp/c9/run_nb.py` (Run All notebook tạm).
- `/tmp/c16/`: output đối chứng âm/dương.
- `/tmp/c18_ties.py`: hòa điểm sparse ở biên top-30.
- `/tmp/c21_ev.py`: đếm point thiếu `evidence_parts`.
- Bản sao câu kín để so dòng: `/tmp/sealed_before.jsonl` (v1 `af809684`), `/tmp/c20_sealed_v2.jsonl` (v2
  `8488e61c`), `/tmp/c22_sealed_v3.jsonl` (v3 `0377e966`).
- Phiên trước: `/tmp/c_probe/`, `/tmp/c_judge/`, `/tmp/c_review/` (có thể đã mất).

## Đã học / bẫy gặp
- **Repo `chatbot-hue` là PUBLIC.**
  - File tracked không chép tên, số đo, đường dẫn của dự án khác của User; chi tiết để ở ghi chú private
    `data/…`.
  - Tên dự án khác vẫn còn trong 15 file đã commit từ trước. Đã báo A; gỡ khỏi lịch sử git là thao tác phá
    hủy, cần User quyết.
- **Giữ mù câu kín:**
  - giao sub-agent mới mỗi lượt, cấm nó in nội dung trong báo cáo cuối;
  - so dòng bằng diff/md5 với bản sao;
  - đọc exit code `check` riêng, không qua pipe (lần đầu C lỡ đọc exit của `grep`).
- Mỗi lần trước khi người khác sửa file kín: **sao một bản** (`cp`, không đọc) để còn so dòng.
- Harness G1: `run --name X` ghi đè `data/phase_8_1/g1/X.jsonl` → khi review dùng tên khác. So hai lượt thì
  bỏ trường thời gian (`dense_ms`) và `config`.
- **Retrieval:**
  - Qdrant trả các điểm hòa theo thứ tự nội bộ (phụ thuộc `limit` và trạng thái), nên native trước B13
    không tất định. Runtime `dense_bm25_rrf` tất định (tự phá hòa).
  - Qdrant tắt/bật hoặc xóa collection có thể đổi thứ tự hòa.
- **Evaluator** (C16):
  - `compare --a A --b B1 B2 …` (Holm khi >1), `--split …/split.json --group dev|test`;
  - `retrieval --shuffle-seed` chỉ cho đối chứng dương;
  - `summarize` có `macro` và `refusal.matrix`.
- Gold `gold_all` khắt khe (thiếu 1 fact = 0) và lệch với keyword proxy. Ví dụ: B4 "4/22 đủ keyword" so với
  gold "0/22 đủ fact".
- Chạy script import `backend.*` từ repo root, hoặc thêm cả `.` và `..` vào `sys.path` khi chạy từ
  `backend/` với `python -I`.
- Grep có brace-expansion `--exclude-dir={…}` kèm tên tiếng Việt bị safety check chặn → dùng nhiều
  `--exclude-dir=` riêng.
- File tracked (`bao_cao_he_thong/`, report): nhắc tên địa danh/chủ đề được, **không** chép số liệu, địa
  chỉ, giá từ corpus, cũng không chép câu Golden / câu kín.
- Giờ ghi trong file lấy bằng `date`. STATUS cập nhật ngay sau mỗi việc. B/C không commit (A commit).

## Câu hỏi cho A/User
- **User:**
  - 3 câu kín `capability_only` (2, 21, 33): sửa theo đề xuất hay giữ?
  - Duyệt mẫu `sealed_user_sample.md` bản 3 (15 dòng, ~20–30 phút).
  - Tên dự án khác còn trong lịch sử git của repo public: có cần viết lại lịch sử không (phá hủy)?
- **A:**
  - commit §7 sealed review;
  - ghi phát hiện "22/22 từ chối nhầm thiếu fact" vào bảng rà C11 / G5;
  - cập nhật `sealed_realism.jsonl` theo nhãn cuối.
