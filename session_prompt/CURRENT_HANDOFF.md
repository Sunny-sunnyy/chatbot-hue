# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 16:13 30/10/2026 (A, **kết phiên 30/10**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Lịch sử phiên 28–30/10 (handoff tại commit `bfb0b41` ~14:45 30/10: quyết định theo giờ tới 14:39, mục việc B90–B97 /
C84–C93, mục cũ 28/10; phần sau 14:45 — C94 / C95 / B98, Qwen3-8B, quyết định 14:44 — ở `TONG_HOP.md` §8) dời nguyên văn sang `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-10-28_30.md` (I7). Tổng hợp kỹ thuật: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md`
§7 (28/10), §8 (30/10); nhật ký User `bao_cao_he_thong/nhat_ky/2026-10-30_ap_dot_2_sua_kho.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống (`main`, `git log -1 main`):**
- Chatbot: context 10 + query NFC, reasoning mặc định, không rerank, validator v2; `/api/chat` ghi `chat_metrics` mỗi câu. Giao diện: trang đơn giản Phase 6 (`frontend/`, một
  lượt hỏi – đáp, không stream).
- **Kho sau đợt 2** (User đóng 14:39 30/10, giữ sao lưu cả hai đợt): 204 file / 8.424 đoạn; collection `hue_full_corpus_7a2_e5_small_384` 8.424 point; record `51fb1ec63cbc`;
  sparse `c8134c49a648` (vocab 5.631); **T1 `4d5bbe9e0edc`**. Sao lưu: `knowledge-base-hue/meta/backup_sua_kho_2026-10-28/`, `…/backup_sua_kho_dot2_2026-10-30/`,
  `data/sua_kho_2026-10-27/backup/`, `…/dot2/backup/` (snapshot Qdrant).
- **Thước đo:** nhãn đoạn đúng **gold v5** `data/phase_8_1/gold/gold_v5.jsonl` (`33d16fd6b8f4`, `GOLD_PATH` từ `bfb0b41`); Golden md5 **`6331e88fb171`** (User sửa câu 5, 127
  30/10); bộ 32 câu an toàn bắt buộc (sàn: P0_sai mới ≤ 2 hai chiều + sinh lại 3 lần; đảo cảnh báo 0); bộ 15 câu "ngày tương đối" `data/ngay_hien_tai_2026-10-30/` (mốc Phase 9).
- **Số hiện tại (đo 30/10, kho đợt 2):** p50 2,19 / p95 4,90 s (harness); từ chối nhầm 12 / 158; lỗi citation 0 / 489 lần sinh; câu theo ngày tương đối 0 nói sai, 6 / 14 bị từ chối.
  **Tiền / câu ≈ 0,00025 USD** (giá ghi đệm 0,125 — `cost_usd` hiện tính phẳng 0,10 ⇒ ghi thiếu ~20 %, `Project_Status.md` §5).
- Qdrant `:6335`: đúng 1 collection (thử 8B đã xoá). Repo **PUBLIC**. Nhánh: `main` (+ `b92-qwen3-harness` nếu User chưa chạy lệnh tag + xoá kết phiên 30/10 — kiểm `git tag -l 'hoso/*'`
  có `hoso/b92-qwen3-harness` rồi mới xoá nhánh); hồ sơ thí nghiệm là tag `hoso/*`.

**Thứ tự việc phiên sau (User 30/10: PA2 — giữ thứ tự cũ; đóng gói Phase 1–8 trước Phase 9):**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 30/10 hết hạn).
   Kiểm User đã chạy lệnh kết phiên 30/10 chưa: `ls data/qwen3_8b_2026-10-28/emb` (phải không còn); `git tag -l 'hoso/b92*'` (phải có) rồi nhánh `b92-qwen3-harness` đã xoá.
2. ✓ **Qwen3-8B xong 30/10: kém hơn ⇒ giữ e5-small** (sàn "0 câu mất đoạn đúng" vỡ; vector câu hỏi 2,2 s qua mạng; `qwen3_8b_implementation.md`). Không còn việc.
3. **Streaming:** kết quả ChatGPT (`gửi chatgpt/2026-10-28/kết quả nghiên cứu/`, **chưa có** 30/10 — hỏi User đã gửi chưa) ⇒ A đọc + WebFetch ⇒ nháp
   `data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming_v2.md` (`b19f8454e22b`) ⇒ spec với User (`propose-options`); **W33: Codex review spec một lần** (worktree sạch không `data/`,
   `knowledge-base-hue/`). Giao diện "ra dáng sản phẩm" bàn cùng spec (User 30/10: hỏi "chưa có giao diện").
4. **Hội thoại nhiều lượt:** nháp `c91_phuong_an_nhieu_luot.md` (`1c0313aafd25`; PA1 trình duyệt giữ lịch sử, server không lưu) ⇒ spec sau streaming.
5. **Đóng gói Phase 1–8** (User; A hỏi lại nghĩa "đóng gói" khi tới): bảng giới hạn `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` (37 dòng, `8211d5d6eb7f`) ⇒
   `LUONG` §5; báo cáo tổng "đã thử / chọn / bỏ" (`BAO_CAO_SO_SANH_PHUONG_AN.md`, đề xuất); sửa `cost_usd` + log `cache_write_tokens`; lệnh kiểm sạch (test cần key bỏ qua rõ);
   bộ kín mới trước bảo vệ; tối ưu: tắt ghi đệm nếu API cho (chưa biết — tra trước).
6. Sau đóng gói: brainstorm Phase 9 (đầu vào: `data/course_notes/v3/TONG_HOP_A_2026-10-30.md` §3, file cập nhật dự án kia II–VII; câu ngày tương đối = ca đầu cho trợ lý).
7. Khi rảnh (User): **B0** (mốc người) — quy trình `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md` (User đọc `data/phase_8_2/b0/doc_cap_mu.md`,
   ghi `nhan_xet_user.md` ⇒ A mở `khoa.json` (chỉ A; **B đã thấy khóa — không tóm nhãn**) ⇒ sub-agent mới tóm ⇒ luật dừng spec 8.2 §11); 20 câu mẫu lỗi nặng.

**Mục tiêu sản phẩm:** đồ án tốt nghiệp (bảo vệ ~tháng 1/2027; 6–10 tuần, không toàn thời gian), càng giống sản phẩm thật càng tốt; người dùng = User, du khách, người dân;
AWS 10–50 USD / tháng chỉ khi local ổn (User xác nhận 30/10).

**Mã hay gặp:** T1 = kết quả tìm 158 câu; A/A = hai lượt cùng cấu hình; F / T / W = sàn / mức tụt / watch plan đo trước ↔ sau; H / P0_sai / P0_thiếu = thước lỗi nặng;
L1 / L2 / L3 = nhãn đo "ngày hôm nay"; Kxxx = mục kho; S / W / I = sổ cải tiến; Bxx / Cxx = việc A giao (30/10: B90–B97, C84–C94); M-n / m-n = finding major / minor;
luật (a) / (i) = luật nhận biến thể spec 8.2 §10.2; luật chạm "f" = câu có đoạn của file bị xoá dòng (plan đợt 2 §10).
Sổ cải tiến (`SO_CAI_TIEN_CACH_LAM.md`): W32 = người kiểm viết ca dò khác cách + câu bất biến; I7 = dời lịch sử file mở phiên sang `archive/`; W33 = Codex review
spec streaming một lần; S49 = giờ ước trong tin nhắn; S50 = commit của A bị auto mode chặn.

## Câu hỏi cho User (báo cáo mở phiên sau)

1. **Quyền phiên.** A khuyên: như 30/10 (A tự điều phối + tự thử trong luật; ≤ 1 USD; B / C push nhánh riêng theo việc).
2. **Kết quả ChatGPT streaming** đã có chưa (yêu cầu `c573949ac59a`)?
3. **Commit / push:** A bị auto mode chặn 3 lần 30/10 (luật chung "commit / push luôn hỏi trước") ⇒ phiên sau A stage từng file + đưa lệnh `!`; hoặc User thêm quyền (S50, vòng 11).
4. (Khi bàn spec nhiều lượt) lưu câu hỏi người dùng? — PA1 của C91 không cần lưu.
5. (Khi rảnh) B0; 20 câu mẫu lỗi nặng; xoá sao lưu đợt 1 + 2 khi đóng gói.

## Câu hỏi A còn nợ (không cần User)

- Sổ cải tiến: theo dõi **W32** (ca dò khác cách), **I7** (dời lịch sử), **W33** (Codex một lần), W30, W31; vòng 11: S49 (giờ ước trong tin nhắn, ≥ 9 lần) + S50 (commit bị chặn).
  Nợ cũ: W30 m-1 (nới mẫu hook), m-2 (in `file:dòng`).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. C65: G2.1a chưa đếm lại bằng validator hiện tại.

## Session

| Vai | Terminal | Agent | Liên lạc | Phiên 30/10 | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-0f` (30/10) | Claude Opus 5.5 | trực tiếp | điều phối; 7 sub-agent đọc khoá; 5 chỗ báo cáo (B97 làm, A review); sổ vòng 10 | `STATUS_A.md`; 0 USD |
| B — thực thi | `hue-rag-24` (30/10) | Claude Opus 5.5 | trực tiếp | B90–B98 (đợt 2 áp + đo, harness + chạy Qwen3-8B, B94 / B95, plan ngày, báo cáo) | `STATUS_B.md`; ≈ 0,0568 USD |
| C — thực thi | `hue-rag-0e` (30/10) | Claude Opus 5.5 | trực tiếp | C84–C95 (review đợt 2 + Qwen, C89 citation, C90 giới hạn, C91 nhiều lượt, C93 đo ngày, C94 báo cáo) | `STATUS_C.md`; ≈ 0,0037 USD |

**Phiên 31/10 (mở 09:44):** A = `hue-rag-1a`, B = `hue-rag-3b`, C = `hue-rag-69`; cả ba trực tiếp; Qdrant `:6335` tắt lúc mở (Docker Desktop chưa chạy — chờ User bật).

Tên terminal đổi mỗi lần mở: `ListAgents`. Cả ba Claude Code ⇒ `trực tiếp`. **B / C lúc mở phiên sau:** không có việc đang chạy; mở phiên ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Thường trực:** A commit / push (**tạm:** A stage từng file + đưa lệnh `!` vì auto mode chặn — S50, chờ User câu hỏi 3); B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ
  cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền; code luôn `uv run`; luôn thử + so baseline trước khi chọn.
- **Phiên 31/10 (User 10:10 31/10/2026, hết hạn cuối phiên):** như 30/10 — A tự điều phối B / C + tự thử trong luật; trần ≤ 1 USD cả phiên; B / C push nhánh riêng khi việc ghi rõ.
- **Phiên 30/10 — HẾT HẠN** (như 29/10; ≤ 1 USD; đợt 2 ≤ 0,10; Qwen3-8B ≤ 0,10; ngày ≤ 0,01). Tiền phiên 30/10 ≈ **0,061 USD** theo giá phẳng (B 0,0568 gồm đợt 2 + B95 + Qwen3-8B; C 0,0037; A 0) — thật cao hơn ~20 % phần vào (ghi đệm).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M.

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | **nhãn đoạn đúng mặc định** (kho đợt 2); v1–v4 giữ | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 (sao lưu trước sửa: `meta/golden_backup_dot2_2026-10-30/`) | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `data/phase_8_2/b0/` | đọc cặp mù (`khoa.json` chỉ A) | — |
| `data/sua_kho_2026-10-27/` | đợt 1 + `dot2/` (edits 4b `c0b5876ea510`, eval trước / sau, backup, quét Golden) | — |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu (`9fa81b0fcec4`) | — |
| `data/ngay_hien_tai_2026-10-30/` | plan + 15 câu ngày tương đối + kết quả C93 | — |
| `data/tinh_nang_moi_2026-10-27/` | nháp streaming v2, nhiều lượt C91, đếm citation C89 | — |
| `data/dong_goi_2026-10-30/` | bảng giới hạn Phase 0–8 (nháp, B ready) | `8211d5d6eb7f` |
| `data/course_notes/v3/` | 7 đối chiếu khoá + `TONG_HOP_A_2026-10-30.md` | — |
| `data/external_project_notes/` | file dự án kia (cập nhật 29/10, RAG B94) | — |
| `gửi chatgpt/2026-10-28/tìm thông tin/streaming_rag_citation_2026_10_28.md` | yêu cầu streaming (User gửi 29/10?) | `c573949ac59a` |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report
  `<việc>_implementation.md`; review chéo (W32: ca dò khác cách + câu bất biến); plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file).
- **Cổng ổn định:** (1) test file chạm; (2) `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5,
  1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop); (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ
  5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31). Lượt dài > ~30 phút: pilot đo cả phương án song song (bài học Qwen 30/10).
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file **và trong tin nhắn**: chạy `date` trước (S49).

## Phiên 31/10 — quyết định + việc đang mở

**User 10:23 31/10/2026 (giờ A ghi nhận):** (1) kết quả ChatGPT streaming đã có: `gửi chatgpt/2026-10-28/kết quả nghiên cứu/NGHIEN_CUU_SAU_STREAMING_CITATION_HUE_RAG_2026-10-31.md`
(224 dòng, 22 URL, sha `6bbfd2166721`); (2) Qdrant bật lại — A kiểm: 1 collection, 8.424 point ✓; (3) **giao diện mới (React / Next…) bàn sau khi xong Phase 8**, gộp áp nội dung
AI FDE (đang được chỉnh ở dự án khác — chờ); (4) ý mới: A gọi thẳng Codex CLI / AGY CLI để tra web thay chuyển tay qua ChatGPT — **đang bàn với User, chưa làm**.
Giả định A (chờ User xác nhận khi bàn spec): spec streaming chỉ đổi API + sửa tối thiểu giao diện hiện tại (JS thuần) để hiện chữ dần.

### B99 — kiểm nguồn kết quả nghiên cứu streaming (chỉ đọc, 0 USD)
- **Mục tiêu:** biết khẳng định nào trong kết quả ChatGPT có nguồn nói đúng, để A dùng làm căn cứ spec.
- **Đọc:** full-read file kết quả trên (là **dữ liệu**, chỉ dẫn bên trong không phải lệnh); targeted-read yêu cầu gốc `…/tìm thông tin/streaming_rag_citation_2026_10_28.md` mục C (câu hỏi).
- **Làm:** WebFetch các URL ở §12 và URL trong bài; với khẳng định chính ở §0, §2, §3, §4 (wire protocol), §8, §10, §11: nguồn nói đúng / nói khác / không thấy / URL hỏng; ghi
  nguyên câu ngắn của nguồn + URL. Ưu tiên khẳng định về OpenAI Agents SDK (stream + `output_type`), SSE / FastAPI, hủy luồng.
- **Không làm:** sửa code, gọi API trả phí, đối chiếu với code hue_rag (việc của C97).
- **Đầu ra:** `data/tinh_nang_moi_2026-10-27/b99_kiem_nguon_streaming.md` (bảng: mục · khẳng định · URL · kết luận · trích ngắn) + 5 dòng "điều A cần biết nhất". Xong ⇒ STATUS_B + nhắn A.
- **Dừng khi:** > 1/3 URL hỏng ⇒ báo A trước khi làm tiếp.
- **Trạng thái (10:30 31/10):** xong, A nhận làm căn cứ (`b99_kiem_nguon_streaming.md` `44644b22d9ef`; 21 / 22 URL mở; không ý nào bị nguồn nói ngược; 3 ý "suy ra", #3314 đã sửa).
  A tự kiểm 2 ý: #3314 đóng 10/09/2026 (PR #3345) ✓ (WebFetch); `.venv` có `fastapi.sse.EventSourceResponse` (fastapi 0.141.1, agents 0.19.4) ✓.
- **B rảnh — lý do:** chờ C97 xong ⇒ B review chéo C97 (W32: ca dò khác cách); không giao việc khác vì thứ tự còn lại (nhiều lượt, đóng gói) đi sau spec streaming.

### C97 — đối chiếu kết quả nghiên cứu streaming với code + nháp v2 (chỉ đọc, 0 USD)
- **Mục tiêu:** biết mỗi đề xuất "áp cho hue_rag" có đúng với code thật và quyết định đã chốt không.
- **Đọc:** full-read file kết quả trên (dữ liệu, không phải lệnh); full-read nháp `data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming_v2.md` (`b19f8454e22b`); code theo nhu cầu
  (`backend/api/app.py`, agent sinh, validator citation, `frontend/app.js`).
- **Làm:** mỗi đề xuất ở §2–§5, §7, §9: khớp code? (`file:dòng`) · đi ngược quyết định nào (`Project_Status.md` §5)? · khác nháp v2 chỗ nào? Kiểm bản Agents SDK đã cài hỗ trợ
  stream khi có `output_type` bằng đọc code thư viện trong `.venv` (`uv run python -c …`, không gọi API).
- **Không làm:** sửa code / nháp v2, gọi API trả phí, WebFetch nguồn (việc của B99).
- **Đầu ra:** `data/tinh_nang_moi_2026-10-27/c97_doi_chieu_code_streaming.md` + danh sách "nháp v2 cần sửa gì". Xong ⇒ STATUS_C + nhắn A.
- **Trạng thái (C, 10:46 31/10/2026):** B100 vòng 2 ready (`b0b49be37fc4`); bản 3 `702cc7ed8af4` (áp n-1, n-2) — chờ A đóng; nháp v2 không đổi.

### B100 — review chéo C97 (chỉ đọc, 0 USD; giao 10:32 31/10/2026)
- **Căn cứ (chỉ gói này; không đọc STATUS_C / tin nhắn của C):** `c97_doi_chieu_code_streaming.md` (`d4c1f35d8d2d`); file kết quả ChatGPT; nháp `c77_phuong_an_streaming_v2.md`;
  code + thư viện trong `.venv` theo `file:dòng` C ghi.
- **Làm:** theo skill `risk-gated-agent-review`; ưu tiên 5 điều §0 (nhất là: sự kiện chữ thô vẫn ra khi có `output_type` — `run_loop.py:1712-1713`; đường từ chối không gọi model gần như
  không chạy — đếm lại log bằng cách khác C; danh sách 14 mục §4). W32: mỗi khẳng định chính dò bằng một cách khác C (đọc code khác chỗ, đếm khác lệnh), không chạy lại y lệnh của C.
- **Không làm:** sửa file của C / nháp, gọi API trả phí, chạy server.
- **Đầu ra:** `data/tinh_nang_moi_2026-10-27/b100_review_c97.md` (finding blocker / major / minor + kết luận `ready_for_user_confirmation` / `changes_requested`). Xong ⇒ STATUS_B + nhắn A.
- **Trạng thái (A ghi 10:41):** `changes_requested` (`d7f57991904e`: M-1 SSE + lỗi trước yield đầu ⇒ 200 thân rỗng — probe thật; 6 minor). B nhắn C; C sửa ⇒ B kiểm phần đổi ⇒ báo A.

### A — thử tra web bằng Codex CLI / AGY CLI (User duyệt 10:3x 31/10 PA1; 0 USD — gói tài khoản)
- Tiêu chí ghi trước: `data/tra_cuu_cli_2026-10-31/tieu_chi.md` (10:39). 6 lượt chạy song song từ 10:41: {Codex `gpt-6-luna`, AGY `gemini-3.8-flash-high`} × {Y1 streaming, Y2 thước đo,
  Y3 Claude gọi CLI}; mỗi lượt thư mục trống `/tmp/tra_cuu_cli/`, kết quả `data/tra_cuu_cli_2026-10-31/ket_qua/`. Y3 cũng gửi ChatGPT (User): `gửi chatgpt/2026-10-31/tìm thông tin/claude_goi_codex_agy_tra_web_2026_10_31.md` (`b51687978f9f`).
- Người chấm (A chạy ⇒ không tự chấm): **B (B101)** — đổi từ C lúc 10:46 vì C viết nháp v3 (C98).

**C97 + B100 đóng (A 10:46):** C97 bản 2 `4baf321f76a3` ready (B100 vòng 2 `b0b49be37fc4`); bản 3 `702cc7ed8af4` chỉ thêm n-1 / n-2 của B (dùng bản 3); A nhận làm đầu vào nháp v3. Câu "ép `incomplete` bằng `answer_max_output_tokens` nhỏ" — **A quyết: không
phải lỗi giả** (model + API thật, chỉ đặt tham số thật; ghi rõ trong spec), trần ≤ 0,001 USD.

### C98 — nháp streaming v3 (sửa tài liệu private, 0 USD; giao 10:46 31/10/2026)
- **Mục tiêu:** một bản nháp đủ để A trình User các câu quyết định (D1…) rồi viết spec.
- **Đọc:** nháp v2 (`b19f8454e22b`), C97 bản 2 §2a + §4 (14 mục), B100 vòng 2 (n-1, n-2), B99 (5 dòng đầu + 3 ý "suy ra").
- **Làm:** viết `data/tinh_nang_moi_2026-10-27/c98_phuong_an_streaming_v3.md` (v2 giữ nguyên): áp 14 mục; chọn kỹ thuật lỗi trước luồng (a/b/c) — A nghiêng (b), C viết lý do; các câu
  cho User viết theo `propose-options` (mỗi câu: đổi gì, tốn gì, khi nào sai, chọn khác mất gì), **D1 đầu tiên** (hiện chữ chưa kiểm ↔ chỉ câu đã kiểm ↔ chỉ tiến độ; kèm căn cứ lỗi tệ
  nhất User 28/10); danh sách test đã lọc; giới hạn. Phạm vi: API + sửa tối thiểu giao diện JS thuần (giao diện mới sau Phase 8 — User 31/10). Đầu file mục "Căn cứ để review" (`WORKFLOW.md` §9.1).
- **Không làm:** code, gọi API trả phí, chọn thay User các câu D.
- **Đầu ra:** file v3 + sha; xong ⇒ STATUS_C + nhắn A (A giao B review trước khi trình User).
- **Trạng thái (C, 11:02 31/10/2026):** B102 vòng 2 ready (`c59b412d702f`); bản 3 `3b6a9ba09149` (áp n-1…n-3) — chờ A trình User; v2 không đổi.
- **User chốt D1 = PA1 (11:26 31/10/2026, giờ A ghi nhận):** chữ hiện ngay khi model viết + tiến độ thật (PA3), kiểm citation cuối như hôm nay; căn cứ nháp v3 bản 3 `3b6a9ba09149` §1.
  Điều kiện A xem lại (báo User): đo qua trình duyệt lợi < 0,5 s hoặc tỉ lệ xóa chữ > ngưỡng D5 ⇒ đề xuất PA3. Tiếp: D2 ⇒ D3 ⇒ (D5 A đặt 1 %) ⇒ spec.

### B101 — chấm thử tra web Codex / AGY (chỉ đọc, 0 USD; giao 10:46, bắt đầu khi A báo 6 lượt chạy xong)
- **Căn cứ:** `data/tra_cuu_cli_2026-10-31/tieu_chi.md` (thước + luật kết luận ghi trước — không đổi); `ket_qua/*.md` hoặc `log/agy_*.json` (trường `response`); log; mốc ChatGPT ghi trong tiêu chí; B99.
- **Làm:** đúng thước 1–5; kiểm URL bằng HTTP (script trong `/tmp`) + WebFetch 6 khẳng định / bản; xem log có lệnh đọc file máy không. Được dùng sub-agent (≤ 3 file / sub-agent).
  Y3 chưa có mốc ChatGPT ⇒ so Codex ↔ AGY, chấm phần ChatGPT khi User lưu kết quả.
- **Không làm:** chạy lại lượt tra; sửa tiêu chí.
- **Đầu ra:** `data/tra_cuu_cli_2026-10-31/b101_cham.md` (bảng 6 bản × thước + kết luận theo luật). Xong ⇒ STATUS_B + nhắn A.
- **Sửa phạm vi (A 10:51):** 6 lượt xong 10:50 (cả 6 SUCCESS; Codex 133–167 s, 26–46 lượt tìm, 0 lệnh shell; AGY 347–565 s; AGY `response` đã tách ra `ket_qua/agy_Y*.md`). Để B
  review nháp v3 (B102), **B101 thu lại = chỉ mốc ChatGPT Y2** (thước 3, đang làm) ⇒ ghi vào `b101_cham.md`; **chấm 6 bản chuyển sang C (C99)**.

**⚠ 10:54 31/10 (A): KHÔNG session nào gọi `agy`** — điều khoản Google cấm truy cập Antigravity qua phần mềm bên thứ ba (nêu tên Claude Code), có thể khoá tài khoản (FAQ, A WebFetch;
chi tiết cuối `data/tra_cuu_cli_2026-10-31/tieu_chi.md`). Kết quả ChatGPT Y3: `gửi chatgpt/2026-10-31/kết quả/NGHIEN_CUU_CLAUDE_CODE_GOI_CODEX_AGY_TRA_WEB_2026_10_31.md` (`02f7735fa2b7`).

### B102 — review nháp streaming v3 (chỉ đọc, 0 USD; giao 10:51, làm sau phần mốc Y2 của B101)
- **Căn cứ:** chỉ gói "Căn cứ để review" đầu file `data/tinh_nang_moi_2026-10-27/c98_phuong_an_streaming_v3.md` (`d77f36ca05b0`) + code để đối chiếu C ghi; không đọc STATUS_C / tin nhắn của C.
- **Làm:** skill `risk-gated-agent-review`; ưu tiên: (1) D1 có viết công bằng các phương án không (hệ quả, khi nào sai, mất gì) — User sẽ chọn dựa vào đây; (2) **đổi nghiêng D3 (b)** "giữ phần đã hiện ⇒ xóa
  hết" có lý do đủ không; (3) chọn (b) cho lỗi trước luồng khớp probe; (4) 14 mục C97 có mặt (§7); (5) test đã lọc không va `Session_Prompt.md` §6 / §8. W32: dò khác cách người viết.
- **Đầu ra:** `data/tinh_nang_moi_2026-10-27/b102_review_c98.md`; B nhắn C nếu `changes_requested`; ready ⇒ nhắn A.

### C99 — chấm 6 bản tra web Codex / AGY (chỉ đọc, 0 USD; giao 10:51) — thay phần chấm của B101
- **Căn cứ / Làm / Không làm:** như B101 ở trên (tiêu chí `tieu_chi.md` không đổi; mốc Y1 = ChatGPT + B99; mốc Y2 = ChatGPT + phần thước 3 B ghi trong `b101_cham.md` khi xong). Thêm: AGY
  không có log lượt tìm trong JSON ⇒ xem `~/.gemini/antigravity-cli/conversations/` (chỉ đọc, chỉ 3 hội thoại 10:41–10:51) để biết AGY có tìm web / đọc file máy không; không thấy thì ghi "không kiểm được".
- **Đầu ra:** `data/tra_cuu_cli_2026-10-31/c99_cham.md`. Xong ⇒ STATUS_C + nhắn A.
- **Trạng thái (C, 11:08 31/10/2026):** xong, chờ A — `c99_cham.md` `514ea908654b`.

### A — tra web bằng Codex vào cách làm (User duyệt 11:1x 31/10: "đồng ý làm script", nhớ ghi mốc thời gian để lấy thông tin mới nhất)
- C99 chấm xong (`c99_cham.md` `514ea908654b`; A tự kiểm 2 ý: arXiv 2404.06183 = bài vật lý ✓, weaveai.dev 404 ✓): Codex đạt "tra nhanh" Y1, Y2 (Y3 trượt chỉ vì 403 trang thật);
  thay ChatGPT: ngang 2 / 3, kém rõ Y1; AGY kém rõ cả 3. Luật lần sau: 403 trang thật đếm riêng + kiểm tiêu đề trang (áp từ lần đo sau).
- A làm (governance — chưa commit): `scripts/tra_web_codex.sh` (`b1216941a659`; thêm ngày hôm nay + đòi thông tin mới nhất; thử thật 11:20: 28 s, 10 lượt tìm, 0 lệnh shell, đáp án khớp
  PyPI API); `.claude/settings.json` chặn `Bash(agy)` / `Bash(agy:*)` (A thử `agy --version` ⇒ bị chặn ✓); `Session_Prompt.md` §9 thêm đoạn "Tra web bằng Codex CLI".
- **B103 — review (chỉ đọc + được chạy script 1 lần với câu công khai nhỏ, 0 USD):** `git diff` 3 file trên + script; kiểm: script đúng tham số đã thử (`tieu_chi.md`), cảnh báo lệnh shell có bắt
  đúng dạng log Codex không (W32: dò khác cách — ví dụ đọc tài liệu định dạng log / tìm mẫu `exec` trong log cũ), chặn `agy` có lọt dạng lệnh ghép không (chỉ thử bằng lệnh
  vô hại như `agy --version`; **không** chạy `agy -p`), §9 rõ cho agent không phải Claude. Đầu ra `report_agent/2026-10-31_tra_web_codex/b103_review.md` (tracked — không chép kết quả tra / nội dung private).
  **Sửa lệch (A 11:31):** luật chặt hơn thắng — không thử `agy` dưới dạng nào, kể cả `--version` (thử chặn chỉ bằng `false && agy …` như B đã làm).
- **B103 vòng 1 `changes_requested`** (`f90ef9a82481`). A sửa (11:31): **M-1** ⇒ chọn (a): script dùng `--json`, đếm `command_execution` / `web_search` bằng `jq`, thêm `url_da_mo.txt`
  (trang Codex thật mở, `open_page`); A kiểm bộ đếm bằng 1 lần Codex chạy `echo b103` thật trong `/tmp` trống (không header cấm shell) ⇒ sự kiện `command_execution` `/bin/bash -lc 'echo b103'` ✓;
  chạy lại script thật 11:30 (32 s, 6 lượt tìm, 1 trang mở, 0 lệnh shell). Script `e0dc2d76a86f`. **m-3** ⇒ `AGENTS.md` luật cứng 7; **m-4** ⇒ §9 thêm câu cho session Codex / AGY + cách
  đọc `url_da_mo.txt`. **m-1** giữ (câu nhỏ ~30 s chấp nhận được; thêm chế độ "nhanh" là núm chưa có nhu cầu). **m-2** ghi giới hạn: Codex nạp `~/.codex/skills` dùng chung
  (của User, ngoài repo) — không đổi cấu hình máy User.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phase 8.2 (User đóng 28/10): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
- Đợt sửa kho 1 (28/10) + 2 (30/10), thước lỗi nặng, đo ngày hôm nay, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/` — `TONG_HOP.md` §7–§8.
