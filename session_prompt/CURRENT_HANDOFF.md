# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 15:43 27/10/2026 (A, **kết phiên 27/10 chiều**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Chi tiết phiên chiều: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md`; nhật ký User `bao_cao_he_thong/nhat_ky/2026-10-27_chieu_phan_ton.md`. Bản handoff
trước khi viết lại (có từng mục B71–B76 / C62–C68): `git show 3d53370:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống (`main`, `git log -1 main`):**
- Chatbot: context **5**, chưa NFC, reasoning `medium` mặc định, không rerank. `/api/chat` ghi một dòng `chat_metrics` mỗi câu (`5100b90`; `dense_ms` làm tròn 1
  chữ số từ `dfbcca5`). Latency thật (B65): p50 3,3 s / p95 5,7 s tuần tự — vượt mức theo dõi 5 s.
- **Thước đo:** nhãn đoạn đúng **`data/phase_8_1/gold/gold_v3.jsonl`** (`3b1117cf59e9`, mặc định từ `fa192f8`; = v2 + 2 câu test). v2 `2f5a347a71ff`, v1
  `gold_draft` `bab707b9ab22` giữ nguyên (G0.6 khóa). Mọi số `*_gold_*` ghi kèm bản nhãn. `validate_gold.py` nay tự dừng nếu `gold_draft` đã có.
- Qdrant `:6335` 1 collection `hue_full_corpus_7a2_e5_small_384` (8.459). Repo **PUBLIC**. Untracked ở gốc **của User, không đụng**: `báo cáo nghiên cứu
  github.txt`, `tham khảo 26_10/`. Cổng: kiểm `ss -ltnp | grep ':80'` trước khi chạy server (27/10 chiều 8010, 8015, 8020, 8023, 8030 bị chiếm; 8013, 8016 dùng được).

**Thứ tự việc (chặn chính: B0 — chỉ User làm):**
1. Mở A / B / C; A `ListAgents`, cập nhật bảng Session; **hỏi lại quyền phiên** (quyền 27/10 chiều hết hạn).
2. **B0** (User đọc `data/phase_8_2/b0/doc_cap_mu.md`, ghi `nhan_xet_user.md`) ⇒ A mở `khoa.json` (chỉ A; **B đã thấy khóa — không tóm nhãn**), sub-agent mới
   tóm nhãn, áp luật dừng spec 8.2 §3 mục 4 ⇒ không dừng: **merge `p82-b1` `c3d5607`** (đã rebase lên `576f84e`, C review ready
   `phase_8_2_b1_rebase2_review.md`; `main` sau đó chỉ thêm tài liệu + `dense_ms` + gold v3 — kiểm lại không xung đột, T1, cổng context 10) ⇒ sửa context 5 ⇒ 10 ở
   guide 6 "Hiện hành", guide 8, `Project_Status` + đủ 5 chỗ (`WORKFLOW.md` §6).
3. **B3 mốc cuối** (User quyết mở câu kín): plan duyệt sha `27e75be5ed44` (`phase_8_2_b3_plan.md`); người chạy **B**; report tách riêng số câu 500 kiểu "validator v1
   không nhận `[Nguồn n]`" mỗi bên (C65). ⇒ `TONG_HOP` 8.2 ⇒ User đóng 8.2.
4. **Đợt sửa kho + build lại index** (phần tồn cuối): spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` — **User DUYỆT sha
   `937cf8969810` (15:39 27/10/2026)** sau C68 3 vòng (`..._design_review.md`); trần 0,15 USD. Chạy theo §5 **sau khi đóng 8.2**: bước 0 (bộ "trước" 176 câu + plan đo
   có review) **trước** khi đụng kho; bước 2–6 làm liền; gold v4 + Golden sửa từng mục User duyệt; kết quả ChatGPT 78 mục: WebFetch đối chiếu URL trước khi áp (đợt 2). Dữ liệu private `data/sua_kho_2026-10-27/` (README mục lục).
5. **Thí nghiệm Qwen3-8B** (User 15:1x: đo, không bỏ) sau đợt sửa kho — collection riêng, tầng tìm theo gold v4 trước; plan `run-experiment` + review.
6. **Tính năng mới** (chỉ mới bàn): streaming trước (A chọn — User "làm gì cũng được"), rồi hội thoại nhiều lượt. Căn cứ C63 `data/tinh_nang_moi_2026-10-27/c63_can_cu.md`:
   quyết định cũ "không streaming khi chưa có nhu cầu thật" (25/08, 11/09); streaming không rút phần suy luận + ~1,2 s ⇒ **đo "thời gian tới chữ đầu tiên" trước**
   (~10 câu, ~0,002 USD); hội thoại nhiều lượt: hướng User duyệt 25/08 (server giữ hội thoại + viết lại câu hỏi trước khi tìm) **va chính sách không ghi câu hỏi**
   ⇒ User quyết; cần bộ đánh giá hội thoại riêng. Cả hai đổi API + UI = rủi ro cao ⇒ một spec. Gợi ý / lịch trình ⇒ Phase 9; deploy khi ổn định.

**Mục tiêu sản phẩm:** đồ án tốt nghiệp (bảo vệ ~**tháng 1/2027**, User: xong càng sớm càng tốt — để học dự án, tìm lỗ hổng, tối ưu, hướng mới, deploy), xem như
sản phẩm kinh doanh thật; người dùng = User, du khách, người dân. Thứ tự lỗi A đề xuất (chưa chốt): nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.

**Mã hay gặp:** B0 / B1 / B3 = bước spec 8.2; T1 = kết quả tìm 158 câu (mốc `cefb2d1ad609` — đổi sau sửa kho); A/A = hai lượt cùng cấu hình; K / R = biến thể
đợt cải tiến (đóng); Kxxx = mục rà kho C32; S / W = sự cố / đề xuất sổ cải tiến; Bxx / Cxx = việc A giao (27/10 chiều: B71–B76, C62–C68).

## Câu hỏi cho User (phiên sau — gói trong báo cáo mở phiên, mỗi câu có khuyến nghị)

1. **Quyền phiên.** A khuyên: như 27/10 (điều phối + tự thử trong luật; ≤ 1 USD; B / C commit + push nhánh riêng theo việc).
2. **B0** — khi tiện (spec sửa kho đã duyệt 27/10; chạy sau đóng 8.2).
3. **16 câu về kho** `data/sua_kho_2026-10-27/cau_hoi_user.md` (mỗi câu có gợi ý) — câu chưa trả lời lúc áp thì chuyển đợt 2.
4. **Gửi ChatGPT** 2 yêu cầu `gửi chatgpt/2026-10-27/tìm thông tin/`: `tra_ngoai_kho_2026_10_27.md` (78 mục kho, B76, A kiểm: chỉ câu ngắn) và
   `muc_tieu_san_pham_2026_10_27.md` (thời gian chờ tối đa, tiền / câu, thứ tự lỗi). Kết quả ⇒ `gửi chatgpt/2026-10-27/kết quả nghiên cứu/`.
5. **Thứ tự lỗi nặng → nhẹ** (trên) — đồng ý? ⇒ "nói chắc sai" thành sàn cho các lần đo sau.
6. **Xóa nhánh đã merge** (auto mode chặn A): `! git push origin --delete c59-log gold-v2 && git branch -d c59-log gold-v2`.
7. **Hội thoại nhiều lượt — lưu câu hỏi người dùng?** Hướng 25/08 (server giữ hội thoại) trái chính sách hiện tại "log không ghi câu hỏi" (`chat.py:24-25`).
   Hỏi khi bàn spec tính năng; A sẽ đưa phương án (lưu trong bộ nhớ phiên, không ghi đĩa / lưu có hạn / chỉ phía trình duyệt).
8. (Không gấp) Hướng K3b-m (hồ sơ — mở lại khi muốn luật nhận riêng cho biến thể đổi context); usage OpenAI 27/10 09:30–09:31, 11:38–11:44 (thay số ước);
   tên dự án khác trong lịch sử git — để nguyên.

## Câu hỏi A còn nợ (phiên sau A xử lý, không cần User)

- Log `FileHandler` không xoay vòng (~400 byte / câu) — xem lại khi deploy.
- C65: số "lỗi citation" ở thí nghiệm Bước 2 so với mốc B1 (validator v1) lệch có lợi cho biến thể ⇒ kết luận "kém hơn" không đảo (A suy ra); G2.1a (8 câu) chưa đếm lại.
- Sổ cải tiến: theo dõi W24–W29 `đang thử` (vòng 8, 27/10 chiều: W27 script grep kho, W28 không khuyên bỏ hướng chưa đo, W29 guide "Hiện hành").

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-bf` (28/10) | Claude Opus 5.5 | trực tiếp | điều phối; đọc kết quả ChatGPT 27/10 (2 file) | `STATUS_A.md` |
| B — thực thi | `hue-rag-ac` (28/10) | Claude Opus 5.5 | trực tiếp | B78 (plan đo trước ↔ sau sửa kho) | `STATUS_B.md` |
| C — thực thi | `hue-rag-32` (28/10) | Claude Opus 5.5 | trực tiếp | C70 (plan đo thời gian tới chữ đầu tiên) | `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.
**B / C lúc mở phiên sau:** chưa có mục việc đang chạy. Mở phiên ⇒ kiểm nhanh ⇒ báo A ⇒ chờ. Việc A dự định giao (sau khi User cấp quyền) ở mục
"Mục việc phiên sau" cuối file.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt:
  A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run` trong `.venv`; luôn thử + so baseline
  trước khi chọn (User 24/10 20:49); commit trước sửa code + cổng ổn định sau mỗi gói (User 26/10); "báo trước, chờ User đồng ý" chỉ áp ngoài phạm vi đã duyệt.
- **Phiên 28/10 (User 09:2x) — HẾT HẠN cuối phiên:** A tự điều phối + tự thử / chọn trong luật; API ≤ 1 USD cả phiên; B / C commit + push nhánh riêng theo việc.
  User 28/10: B0 chưa rảnh làm; **đồng ý thứ tự lỗi** nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm; User tự xóa `c59-log`, `gold-v2`.
- Trần 8.2: 0,5 USD (dùng ≈ 0,213). Trần đợt sửa kho (khi spec duyệt): 0,15 USD. GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra (~0,000133 USD / câu context 5; ~0,000204 context 10).

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024 | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v3.jsonl` (+ `gold_v3_CHANGES.md`) | **nhãn đoạn đúng dùng từ 27/10 chiều** (55 câu; v2 + câu 130, 138) | `3b1117cf59e9` |
| `data/phase_8_1/gold/gold_v2.jsonl`, `gold_draft.jsonl` | v2; v1 (G0.6 khóa) — không sửa | `2f5a347a71ff`, `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (82 / 65 / 29) | `0b65d1c138d2` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — **không đọc** tới B3 (người chạy B) | md5 `ddc59587b502` |
| `data/phase_8_1/baseline/g0_6_manifest.json` | manifest khóa G0.6 | `9ea480d0d083` |
| `data/phase_8_2/b0/` | đọc cặp mù (`nhan_xet_user.md` **chưa ghi**; **`khoa.json` chỉ A** `5b9240842b7b`) | — |
| `data/phase_8_2/b1/rebase_2710/` | B71 + C review (log cổng `c_review/`); `b1/c65/` kiểm validator v1 | — |
| `data/sua_kho_2026-10-27/` | đợt sửa kho: `de_xuat_sua.md`, `edits/` + `diffs/` (41), `diffs_them/` (11), `review_c66.md`, `cau_hoi_user.md`, `tra_ngoai.md`, `de_xuat_inventory.md` | — |
| `data/tinh_nang_moi_2026-10-27/c63_can_cu.md` | căn cứ streaming + hội thoại nhiều lượt | — |
| `gửi chatgpt/2026-10-27/tìm thông tin/{tra_ngoai_kho,muc_tieu_san_pham}_2026_10_27.md` | 2 yêu cầu chưa gửi | `c5a9198d81d8`, — |
| `data/phase_8_2/{b1,k1,k3,k3b,r1,r2,r4,latency_2710}/`, `data/cai_tien_tung_khau_2026-10-26/` | hồ sơ thí nghiệm 8.2 + đo hiện trạng 27/10 | — |
| `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json}` | điều kiện chunker + mẫu test chunker (đợt sửa kho cập nhật mẫu) | conditions `b84a0a637bfc` |

## Việc đang mở

### Luật chung khi sửa code (mẫu cổng ổn định — dùng cho merge B1, đợt sửa kho)

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file,
  không `--env-file` trừ khi mục ghi; report `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha
  (§9.1, sha tính từ file). Dừng khi: đường thật đổi ngoài dự kiến; phải đụng file người kia đang khai báo; vượt tiền. Đổi người review ⇒ báo **cả** người cũ.
- **Cổng ổn định sau mỗi gói:** (1) test các file chạm (lỗi thiếu key ghi rõ); (2) chạy thật `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn
  api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho (200, `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết, body `{"query": …}`;
  **đếm dòng `chat_metrics` mới = số câu**, grep câu hỏi trong log = 0; đo client bằng Python `perf_counter`; tắt server (TaskStop); (3) chạm tìm kiếm / chia
  đoạn: T1 giống byte; (4) đủ 5 chỗ (`WORKFLOW.md` §6) nếu hành vi đổi; (5) hook quét trùng tự chạy; A commit + push.
- Test cần key OpenAI (không chạy mặc định): `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan` (+ các test `require_openai_key`),
  `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. Test thiếu model: User `!`.
- Sub-agent đọc kho: grep **chỉ** qua script đã loại `evaluation/`, `meta/`, `*sealed*` (`scripts/grep_kb.sh`, W27) — bẫy s7 27/10.

### B78 — plan đo "trước ↔ sau" đợt sửa kho (B viết, C review; 28/10)

- **Mục tiêu:** plan cho spec sửa kho `937cf8969810` §5 bước 0 + bước 9 + §6, có tiêu chí ghi trước, để A duyệt sha **trước** khi chạy bộ "trước".
- **Đọc:** spec sửa kho (full-read) + `..._design_review.md` (targeted: finding còn mở); skill `run-experiment` §1; spec 8.2 §10 (luật nhận, targeted).
- **Làm:** `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_do_truoc_sau_plan.md` (hoặc đợt mới nếu A mở — A báo): mục "Căn cứ để review" (2–4 file, mục cần đọc); sàn
  (0 câu ngoài kho bị trả lời; thêm **"nói chắc sai"** theo thứ tự lỗi User đồng ý 28/10 — B đề xuất cách đếm); mức tụt; chỉ số quyết; A/A = 2 (B1 ↔ G2.1a);
  harness ghi từng dòng (append), lỗi bất kỳ vẫn giữ usage; tiền ước; ghi rõ bộ "trước" chạy trên chatbot nào (spec: sau merge B1 — B0 chưa có ngày, ghi điều này
  như giả định, không tự đổi). Mỗi tiêu chí sàn trỏ `file:dòng` hành vi production nó đo.
- **Không làm:** chạy đo, gọi API, đụng kho / Qdrant / Golden, mở câu kín. 0 USD.
- **Xong:** báo sha (12) cho A + C; C review theo §9.1 (chỉ dựa gói căn cứ) ⇒ `<plan>_review.md`.

### C70 — plan đo "thời gian tới chữ đầu tiên" (C viết, B review; 28/10)

- **Mục tiêu:** biết streaming rút được bao nhiêu giây người dùng chờ, trước khi bàn spec streaming.
- **Đọc:** `data/tinh_nang_moi_2026-10-27/c63_can_cu.md`; code sinh câu trả lời (`backend/generation/`, `backend/api/`) theo nhu cầu; skill `run-experiment`.
- **Làm:** plan `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_plan.md`: ~10 câu **tự viết** (không lấy Golden / câu kín); đo thời gian tới chữ đầu tiên,
  tới hết câu, token suy luận; đường chính `Runner.run_streamed` (đường production sẽ dùng), stream SDK OpenAI trực tiếp chỉ làm mốc nếu rẻ; context 5 hiện tại
  **và** context 10 (B1) nếu không tốn thêm nhiều — ghi lý do; p50 / p95; tiền ước (≈ 0,002 USD); "Căn cứ để review".
- **Không làm:** chạy đo, sửa code `backend/`. 0 USD.
- **Xong:** báo sha cho A + B; B review ⇒ `<plan>_review.md`.

### Hồ sơ đã đóng (chỉ tra cứu)

Thí nghiệm 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/` + `2026-10-26_cai_tien_tung_khau/`; nhánh hồ sơ không merge `p82-k1`, `p82-k3`, `p82-k3b`, `p82-r1`,
`p82-r2`. Phiên 27/10 chiều: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §3.

### Mục việc phiên sau (A giao sau khi User cấp quyền; mọi việc dưới là 0 USD trừ khi ghi)

- **Khi chờ B0 (song song, không chồng file):**
  - **B:** viết plan đo "trước ↔ sau" đợt sửa kho (spec `937cf8969810` §5 bước 0 + §6; khuôn `run-experiment` §1, mục "Căn cứ để review"; harness ghi từng dòng; A/A = 2
    nguồn B1 ↔ G2.1a) ⇒ C review ⇒ A duyệt sha. Chưa chạy (bộ "trước" chạy trên chatbot sau merge B1).
  - **C:** viết plan đo "thời gian tới chữ đầu tiên" cho streaming (~10 câu tự viết, `Runner.run_streamed` hoặc stream SDK OpenAI, đo cả thời gian suy luận; ≈ 0,002 USD
    khi chạy; căn cứ `data/tinh_nang_moi_2026-10-27/c63_can_cu.md`) ⇒ B review ⇒ A duyệt sha; chạy sau merge B1 (context 10).
- **Sau B0:** A tóm nhãn (sub-agent mới) + luật dừng ⇒ A merge `p82-b1` (hoặc B rebase lại nếu `main` xung đột) ⇒ cổng ổn định ⇒ 5 chỗ báo cáo; C kiểm.
- **B3:** B chạy theo plan `27e75be5ed44` khi User quyết mở câu kín; C kiểm report (giữ mù); A viết `TONG_HOP` 8.2 ⇒ User đóng 8.2.
- **Đợt sửa kho:** B chạy bước 0 + áp sửa (bước 1–6), C review diff + kiểm chunk / build; bước 7–9 theo spec. Trần 0,15 USD.
- **A:** brainstorm spec tính năng (streaming trước) với User sau khi có số "chữ đầu tiên"; đọc kết quả ChatGPT khi User gửi (WebFetch đối chiếu URL).
