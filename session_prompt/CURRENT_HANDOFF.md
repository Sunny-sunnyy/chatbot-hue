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

**Thứ tự việc (cập nhật 10:24 28/10/2026):**
1. ✓ Mở phiên 28/10 (quyền: ≤ 1 USD, A tự điều phối, B / C push nhánh riêng).
2. ✓ **Phase 8.2 ĐÓNG** (User 10:24 28/10; `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`): PA3 (spec §11) ⇒ merge B1 `510e1a8` (context 10 + NFC) ⇒ B3 câu kín tốt hơn,
   0 câu tụt. **B0 còn nợ** (mốc người, trước bảo vệ): User đọc `data/phase_8_2/b0/doc_cap_mu.md`, ghi `nhan_xet_user.md` ⇒ A mở `khoa.json` (chỉ A; **B đã thấy khóa — không
   tóm nhãn**), sub-agent mới tóm nhãn, luật dừng spec 8.2 §3 mục 4 ⇒ dừng / chưa rõ: A trình User giữ 10 / quay về 5.
3. (gộp vào 2)
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

**Mã hay gặp:** B0 / B1 / B3 = bước spec 8.2; T1 = kết quả tìm 158 câu (mốc **`23c58c47635d`** từ 28/10 sau sửa kho; trước `cefb2d1ad609`); A/A = hai lượt cùng cấu hình; K / R = biến thể
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
- **Trạng thái (B, 09:37 28/10/2026):** plan bản 1 xong, sha `7b79c3971bc7` (chưa commit) — **chờ C review**. 3 câu hỏi cho A ở plan §8 (có mặc định).
- A 09:4x: **C72** = C review plan này **sau C71** (§9.1: chỉ dựa "Căn cứ để review", không đọc STATUS_B / tin của B) ⇒ `sua_kho_do_truoc_sau_plan_review.md`; A trả lời
  §8 lúc duyệt sha. Chưa chạy bộ "trước" tới khi A ghi "duyệt bản sha".
- **C72 ready 0 / 0 / 6** (`sua_kho_do_truoc_sau_plan_review.md`, bản `7b79c3971bc7`). **A quyết (09:4x 28/10 — trước ghi nhầm giờ ước "10:0x", B bắt):** B viết bản 2 đóng m-1 … m-6, C kiểm phần sửa, rồi A duyệt sha.
  - **m-4 / §8 câu 3:** cho chạy bước 0 (bộ "trước") **trước B3 / trước khi đóng 8.2** (lệch thứ tự spec sửa kho §2, A duyệt): bước 0 chỉ đọc kho + gọi model,
    tính vào trần đợt 0,15 USD; điều kiện: không chạy cùng lúc B3 / lượt trả phí khác; kiểm "còn hiệu lực" trước bước 1 như plan.
  - **m-5 / §8 câu 1:** **giữ spec §5** "sàn vỡ ⇒ dừng + khôi phục" (không đổi spec). Thêm: F4 vỡ ⇒ sinh lại đúng câu đó một lần ở bên `sau` (file riêng, giữ
    cả hai) làm bằng chứng; sau khôi phục A trình User kèm bằng chứng để quyết áp lại hay không.
  - §8 câu 2: đồng ý (ghi giới hạn "bịa thêm") + dòng watch m-1.
- **Trạng thái (B, 09:50 28/10/2026):** bản 2 xong, sha `41485782b39e` (chưa commit; đóng m-1 … m-6, ghi 3 quyết định A ở §8, bảng sửa §9) — **chờ C kiểm phần sửa**.
- **A DUYỆT bản sha `41485782b39e` (09:59 28/10/2026)** — sha tính từ file; C kiểm phần sửa ready 6 / 6 (review §7). Người chạy B, **sau B80 (B3)** (không chạy cùng lúc lượt trả phí khác).
- **Bước 0 (B, 10:28 28/10/2026):** bộ "trước" xong — `data/sua_kho_2026-10-27/eval_truoc/` (README); 0 lỗi, F1 / F4 = 0, 0,0361 USD. C73 được chạy.

### C70 — plan đo "thời gian tới chữ đầu tiên" (C viết, B review; 28/10)

- **Mục tiêu:** biết streaming rút được bao nhiêu giây người dùng chờ, trước khi bàn spec streaming.
- **Đọc:** `data/tinh_nang_moi_2026-10-27/c63_can_cu.md`; code sinh câu trả lời (`backend/generation/`, `backend/api/`) theo nhu cầu; skill `run-experiment`.
- **Làm:** plan `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_plan.md`: ~10 câu **tự viết** (không lấy Golden / câu kín); đo thời gian tới chữ đầu tiên,
  tới hết câu, token suy luận; đường chính `Runner.run_streamed` (đường production sẽ dùng), stream SDK OpenAI trực tiếp chỉ làm mốc nếu rẻ; context 5 hiện tại
  **và** context 10 (B1) nếu không tốn thêm nhiều — ghi lý do; p50 / p95; tiền ước (≈ 0,002 USD); "Căn cứ để review".
- **Không làm:** chạy đo, sửa code `backend/`. 0 USD.
- **Xong:** báo sha cho A + B; B review ⇒ `<plan>_review.md`.
- **Trạng thái (09:30 28/10/2026, C):** plan viết xong, **chờ B review** — sha `1e792df347fd`; bộ câu private `data/streaming_ttft_2026-10-28/questions.jsonl` `107620cb30f1`. Ước khi chạy ≈ 0,016 USD (lệch ≈ 0,002 của handoff — plan §8, §10 có bản gọn ≈ 0,007).
- A 09:3x: B review khi xong B78 (bản đủ / gọn, D5); A chọn lúc duyệt sha.
- **A DUYỆT bản sha `9683641b6c38` (09:59 28/10/2026)** — sha tính từ file; B kiểm vòng 2 ready 0 / 0 / 1 (n-1 xử lý trong harness). §10: **giữ D10** (+0,002 USD; B, C cùng khuyên).
  ⇒ **C73:** C viết harness trên nhánh `c70-ttft` (commit + push nhánh), B review code; **chạy sau khi B xong B80 + bộ "trước" B78** (đo latency — không chạy chồng
  lượt trả phí khác). Trần 0,03 USD.

### C71 — kiểm merge B1 vào `main` (C; 28/10)

- **Đọc:** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_merge_implementation.md` (full-read); spec 8.2 §11; `git show 510e1a8`.
- **Làm:** cổng tối thiểu `risk-gated-agent-review` (merge không sửa tay: `git diff c3d5607 510e1a8 -- backend/` chỉ là phần `main` thêm; T1 free chạy lại nếu
  thấy cần); kiểm các khẳng định bảng §2 bằng file / log thật (`data/phase_8_2/b1/merge_2810/`, dòng `chat_metrics` cuối của `backend/logs/application.log`).
  Không chạy server lại trừ khi thấy bằng chứng thiếu (≤ 0,001 USD nếu chạy).
- **Đầu ra:** `phase_8_2_b1_merge_review.md`; nhắn A. A sửa 5 chỗ báo cáo song song; xong A nhờ C kiểm phần mô tả hành vi.

### B80 — mốc cuối B3 (B chạy; C kiểm giữ mù; 28/10)

- **User 09:59 28/10/2026: "Chạy B3 ngay"** (mở 36 câu kín cho người chạy B). Plan duyệt `27e75be5ed44` (`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md`, full-read).
- Chatbot "cuối 8.2" = `main` `510e1a8` trở đi (context 10 + NFC; `backend/` không đổi từ đó); "đầu 8.2" = context 5 như plan. Report tách riêng số câu 500 kiểu "validator v1
  không nhận `[Nguồn n]`" mỗi bên (C65). Trần theo plan; ≈ 0,02 USD.
- **Không làm:** chạy cùng lúc bộ "trước" B78 / C73. Report tracked giữ mù (số đếm, số dòng, đúng / sai; không nội dung câu, không tên file nguồn).
- **Xong:** report `phase_8_2_b3_implementation.md` ⇒ nhắn A + C; **C74** = C review giữ mù ⇒ A viết `TONG_HOP` 8.2 ⇒ User đóng 8.2.
- **Trạng thái (B, 10:15 28/10/2026):** chạy xong, report `phase_8_2_b3_implementation.md` (chưa commit) — **chờ C74**. S36 (match-seen 1 / 3): không làm hỏng + tốt hơn; ≈ 0,0138 USD.

### B81 — đợt sửa kho bước 1–6 (B làm, C kiểm; A giao 10:29 28/10/2026)

- **Căn cứ:** spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (User duyệt `937cf8969810`) §5 bước 1–6 + "Dừng + khôi phục" (full-read); plan đo
  `sua_kho_do_truoc_sau_plan.md` (`41485782b39e`) phần kiểm "còn hiệu lực"; `guides/full_corpus_rag.md` "Build lại index"; `data/sua_kho_2026-10-27/README.md`.
- **Bước 0 xong** (B, 10:29): `data/sua_kho_2026-10-27/eval_truoc/` — 176 câu, lỗi 0, ngoài kho bị trả lời 0 / 18, 500 = 0, từ chối nhầm 12 / 158; 0,0361 USD; harness p50 2,2 s / p95 4,9 s.
- **Khi bắt đầu:** **chỉ sau khi C báo xong C73** (C73 dùng index hiện tại). Bước 1 trước: kiểm "còn hiệu lực" + sao lưu (kho ⇒ `meta/` kèm ngày; snapshot Qdrant; build record +
  sparse state ⇒ `data/sua_kho_2026-10-27/backup/`). Bước 2–6 **làm liền**. 16 câu User chưa trả lời ⇒ để nguyên, đợt 2 (spec). K091 không áp.
- **Quyền:** sửa kho theo `edits/` + `diffs_them/` đã review; xóa + build lại collection `hue_full_corpus_7a2_e5_small_384`, build record, sparse state (đích đúng như spec,
  liệt kê trước khi xóa — khác thì dừng); sửa `backend/config/settings.yaml` (`exclude_files`) + test discovery + docstring + file mẫu chunker trên working tree chung
  (**không commit** — A commit sau khi C kiểm). 0 USD trừ cổng ổn định (≤ 0,001 USD). Bước 7–9 chưa làm.
- **Dừng + khôi phục** đúng spec §5. Mọi bước báo A ở cuối bước 6 (hoặc khi dừng).
- **Đầu ra:** `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b1_6_implementation.md` ⇒ **C75** = C kiểm (diff với backup từng mục, chunk / token, build, T1 mới, cổng).
- **Trạng thái (B, 11:10 28/10/2026):** bước 1–6 xong — report trên (chưa commit); T1 mới `23c58c47635d`; build record `574b5d02088b`; chatbot khởi động lại được. **Chờ C75.**

- **B81 xong bước 1–6** (B, report `sua_kho_b1_6_implementation.md`): 204 file / 8.426 đoạn; build record `574b5d02088b`; vocab 5.631; **T1 mới `23c58c47635d`** (40 / 158 câu đổi
  top-10); cổng 8016 đạt; code 3 file trên working tree chờ C75. A giao **C75** 11:11.

### B82 — đợt sửa kho bước 7–8: gold v4 + quét Golden lệch kho (B; A giao 11:11 28/10/2026)

- **Căn cứ:** spec sửa kho §5 bước 7, 8 + §6 (full-read); `data/phase_8_1/gold/gold_v3.jsonl` + `gold_v3_CHANGES.md`; `data/sua_kho_2026-10-27/applied_edits.jsonl`.
- **Làm:** (7) `data/phase_8_1/tools/build_gold_v4.py` (chỉ đọc, từ chối ghi đè) ⇒ `gold_v4.jsonl` mới: tìm lại từng trích dẫn nguyên văn trong file đã sửa, đúng 1 lần; trích dẫn
  bị edit chồng ⇒ **đề xuất** trích dẫn mới (không tự chọn). (8) Quét Golden 176 câu chạm fact / file đã sửa ⇒ **đề xuất** sửa `reference_answer` / `keywords` (file đề xuất
  private `data/sua_kho_2026-10-27/golden_de_xuat.md`). Ghi kèm: câu q02 kiểu "giờ mở cửa" của bộ C73 bị từ chối cả 3 ô (C) — xem có chạm mục sửa không (chỉ ghi).
- **Không làm:** sửa Golden, đổi `GOLD_PATH`, mở câu kín, gọi API. 0 USD. Tìm trong kho chỉ qua `scripts/grep_kb.sh` hoặc đọc file theo đường dẫn edit.
- **Xong:** report `sua_kho_b7_8_implementation.md` ⇒ C kiểm ⇒ A trình User duyệt từng mục. Nếu C75 tìm lỗi phải khôi phục ⇒ dừng B82.
- **Trạng thái (B, 11:19 28/10/2026):** xong — gold v4 nháp (2 trích dẫn câu 27 chờ User), Golden 0 câu cần sửa; chờ C kiểm.

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
