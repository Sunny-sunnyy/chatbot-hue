# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 19:52 29/10/2026 (A, **phiên 29/10 đang chạy** — quyết định User + giao B90 / C84–C86). Trước: 13:21 28/10/2026 (kết phiên 28/10). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Chi tiết phiên 28/10: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §7; 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`; nhật ký User
`bao_cao_he_thong/nhat_ky/2026-10-28_dua_context_10.md`. Bản handoff trước khi viết lại (có từng mục B78–B89 / C70–C83): `git show 25f23ae:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN 29/10 — ĐANG CHẠY (mở 19:13, User kết phiên ~22:00–22:10 29/10/2026)

**User quyết (6 câu mở phiên, A ghi nhận trước 19:52 29/10/2026 theo `date`; "làm đi" 19:52):**
1. Quyền phiên **như 28/10** (A tự điều phối + tự thử / chọn trong luật; ≤ 1 USD cả phiên; B / C commit + push nhánh riêng theo việc).
2. Trần đợt 2 sửa kho **0,10 USD**.
3. **Luật nội dung kho (User): "những câu nào bạn không chắc chắn có thể bỏ hoặc sửa lại câu khác mà bạn chắc chắn"** ⇒ một chỗ sửa chỉ vào đợt 2 khi có nguồn đọc được
   nguyên văn **và** một session khác đọc lại khớp; không thì sửa thành câu nguồn nói đúng, hoặc bỏ. Áp cho K017 và cho D1–D7 + 15 câu (`dot2/quyet_dinh_user.md`) — User
   không trả lời từng mục nữa. **K017:** A tự đọc nguồn BRIDGE2 (curl có cookie, 29/10): 2 ý của edit đúng nguyên văn; edit 2 còn 1 con số gắn sai chủ thể + 1 chi tiết
   không nguồn nào nói ⇒ edit 1 giữ; edit 2 viết lại theo nguồn ⇒ D3 xong theo luật này. Chi tiết + nguyên văn: `data/sua_kho_2026-10-27/dot2/a_k017_2026-10-29.md` (private).
4. **Qwen3-8B duyệt**: gửi kho + câu hỏi đánh giá ra OpenRouter (pin Nebius, `data_collection: deny`), tạo `hue_c78_qwen3_8b_4096`, xóa khi xong, trần 0,10 USD; chạy **sau đợt 2**.
5. User gửi ChatGPT yêu cầu streaming (`c573949ac59a`) tối 29/10; kết quả vào `gửi chatgpt/2026-10-28/kết quả nghiên cứu/`.
6. Thước lỗi nặng: **nhận 32 câu an toàn làm bộ kiểm bắt buộc** cho thay đổi sau; **đo nhiễu A/A trước** khi đặt sàn P0_sai. A dời lượt A/A lên **trước** khi sửa kho
   (để có mốc + sàn cho chính đợt 2; không có lượt đo latency nào chạy) — đã báo User.

**Giờ:** B / C xong phần chuẩn bị + review ~21:30; **áp đợt 2 vào kho chỉ khi B ước (theo thời gian đợt 1) làm trọn bước 1–8 trước 21:40** — không để kho / index sửa dở qua
kết phiên; không kịp ⇒ áp ở phiên sau. 21:45: B / C cập nhật `STATUS_<X>.md` + dòng mình ở đây; A kết phiên.

**B90 (B) — chuẩn bị đợt 2, không đụng kho / Qdrant, 0 USD.** Đọc: handoff mục "PHIÊN SAU" 2 (b)–(e) dưới; `data/sua_kho_2026-10-27/dot2/README.md`, `quyet_dinh_user.md`,
`review_b88.md` (full); plan B78 `sua_kho_do_truoc_sau_plan.md` (`41485782b39e`, targeted). Làm: (a) tham số đầu vào / đầu ra cho `data/sua_kho_2026-10-27/tools/apply_edits.py`
và `truoc_sau.py` (mặc định giữ hành vi cũ) — C kiểm diff; (b) `dot2.jsonl` bản mới theo luật User mục 3 (K017 edit 2 theo `a_k017_2026-10-29.md`; D1–D7 + 15 câu: mỗi mục
sửa theo nguồn đọc được hoặc bỏ, ghi bảng mục ⇒ quyết định ⇒ trích nguồn / lý do; bản cũ giữ như `edits_v3_9b5105b35e8b`), báo sha mới; (c) phụ lục plan đo đợt 2 (mục "Căn
cứ để review" đầu file): bộ "trước" = "sau" đợt 1 + 4 kiểm, **bộ 32 câu an toàn trước ↔ sau** (sàn theo nhiễu C84), câu đổi đoạn vì 2 edit đổi tiêu đề mục, trần 0,10 USD.
Không làm: áp kho, xóa / ghi Qdrant, gọi API trả phí. Xong ⇒ báo A + C (sha file b + c).

**C84 (C) — đo nhiễu A/A thước lỗi nặng, ≈ 0,008 USD (trần 0,02), chạy ngay.** Đọc: `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_review.md` m-1 (cách (a)),
`do_loi_nang_implementation.md` §6 (targeted). Làm: chạy lại mốc 32 câu an toàn (`data/loi_nang_2026-10-28/an_toan/questions.jsonl` `9fa81b0fcec4`) một lượt trên chatbot hiện tại,
cùng cấu hình B89 + 2 judge như B89; so với lượt B89 ⇒ số câu đổi P0_sai / H giữa hai lượt; đề xuất sàn (vd "P0_sai mới ≤ nhiễu"). Đầu ra `data/loi_nang_2026-10-28/an_toan/aa_2026-10-29/`
+ report ngắn `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_aa_implementation.md`; B kiểm khi rảnh. Không làm: đổi câu / rubric; lượt khác song song.
**C85** (sau B90): review (a) diff tham số, (b) `dot2.jsonl` bản mới — **đọc lại độc lập** nguồn của mọi mục đổi / thêm (người thứ hai của luật mục 3), (c) phụ lục plan ⇒
`<plan>_review.md`; A duyệt sha sau review. **C86** (khi rảnh): harness Qwen3-8B theo plan `52555da95828` (nhánh riêng, chưa chạy; B review code).

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống (`main`, `git log -1 main`):**
- Chatbot: **context 10 + query NFC** (Phase 8.2 B1, `510e1a8`), reasoning `medium`, không rerank, validator v2 (`[n]` + `[Nguồn n]`); `/api/chat` ghi `chat_metrics` mỗi câu.
- **Kho đã sửa đợt 1** (28/10): 204 file / 8.426 đoạn; collection `hue_full_corpus_7a2_e5_small_384` 8.426 point; build record `574b5d02088b`; sparse state `1bae9e0f3c49`
  (vocab 5.631); **T1 = `23c58c47635d`** (158 câu; trước `cefb2d1ad609`). Sao lưu đợt 1 **giữ** (User): `knowledge-base-hue/meta/backup_sua_kho_2026-10-28/`, `data/sua_kho_2026-10-27/backup/`.
- **Thước đo:** nhãn đoạn đúng **gold v4** `data/phase_8_1/gold/gold_v4.jsonl` (`927bae1bf201`, `GOLD_PATH` `g1_retrieval.py:48`, `e08a126`); v1–v3 giữ. Golden md5 `0f7dbf41b422`
  (không đổi). **Câu kín đã dùng** (B3) — không còn là bộ "chưa ai thấy". Thước "lỗi nặng" (B89, C83 ready) nhận: `data/loi_nang_2026-10-28/`.
- **Yêu cầu User chốt 28/10:** cả câu p50 ≤ 3 s, p95 ≤ 5 s; ≤ 0,0005 USD / câu; thứ tự lỗi: **sai cảnh báo an toàn / điều kiện vào khu vực > nói chắc sai / bịa > trả lời câu
  ngoài kho > thiếu ý > từ chối nhầm**. Số hiện tại (bộ "trước" B78, 176 câu, harness): p50 2,2 s / p95 4,9 s; ~0,00021 USD / câu; từ chối nhầm 13 / 158.
- Qdrant `:6335` đúng 1 collection. Repo **PUBLIC**. Untracked ở gốc **của User, không đụng**: `báo cáo nghiên cứu github.txt`, `tham khảo 26_10/`. Kiểm `ss -ltnp | grep ':80'`
  trước khi chạy server (8013, 8016 dùng được 28/10). `--env-file` chạy nền: **đường dẫn tuyệt đối** (`Project_Status.md` §8).

**Thứ tự việc phiên sau (User 28/10: "nhiệm vụ, câu hỏi … ở session tiếp theo"):**
1. Mở A / B / C; A `ListAgents`, cập nhật bảng Session; **hỏi lại quyền phiên** (quyền 28/10 hết hạn).
2. **Đợt 2 sửa kho — áp phần sẵn sàng, việc đầu tiên** (User 28/10: "Áp phần sẵn sàng", "phiên sau"): `data/sua_kho_2026-10-27/dot2/edits/dot2.jsonl` **`9b5105b35e8b`**
   (104 edit / 33 file; B88 vòng 3 ready 0 / 0 / 0; nguồn K004 = 2 bài cổng Chính phủ 21/04 + 21/06/2025 + NQ 1675). Chạy **như đợt 1** theo spec `937cf8969810` §5
   bước 1–10 (sao lưu ⇒ áp ⇒ chia đoạn thử ⇒ User `!` xóa 3 đích ở terminal B ⇒ build ⇒ T1 mới ⇒ gold v5 nếu offset lệch ⇒ quét Golden ⇒ đo "sau" ⇒ báo cáo).
   Bộ "trước": **dùng lại bộ "sau" đợt 1** (`data/sua_kho_2026-10-27/eval_sau/`) **được** nếu qua 4 kiểm "còn hiệu lực" (B đề xuất, `STATUS_B.md`): diff `backend/` từ lượt đó,
   build record `574b5d02088b` + sparse không đổi, T1 giống byte `23c58c47635d`, model / context như meta — và vẫn chấm hai bên **cùng lượt mù**; C review, A duyệt. Trần đợt 2:
   A đề xuất **0,10 USD** (hỏi User). D1–D7 + 15 câu (`dot2/quyet_dinh_user.md`) chưa trả lời ⇒ để nguyên.
   **Bổ sung sau thử mở phiên (13:32 28/10/2026):** (a) bước áp dụng spec §5 bước **1, 2, 4–10** (bước 3 `exclude_files` chỉ của đợt 1); (b) `data/sua_kho_2026-10-27/tools/apply_edits.py`
   đọc / ghi cứng `edits/` + `diffs_them/` ⇒ `applied_edits.jsonl` (đã có, script dừng), `truoc_sau.py:269` cũng đọc cứng ⇒ **B thêm tham số** đầu vào / đầu ra (đợt 2 ghi
   `dot2/applied_edits_dot2.jsonl`), giữ hành vi cũ mặc định — C kiểm diff; (c) **B viết phụ lục plan đo** cho đợt 2 (dựa plan B78 `41485782b39e`: bộ "trước" = "sau" đợt 1 + 4 kiểm;
   **2 edit đổi tiêu đề mục** (`dot2/README.md`) ⇒ `heading_path` / `chunk_id` có thể đổi ⇒ ghi trước tiêu chí cho câu đổi đoạn vì đổi tiêu đề; trần) ⇒ C review ⇒ A duyệt sha
   **trước** khi đụng kho; (d) **K017**: B / C không đọc được nguồn bằng trình duyệt ⇒ **User** mở nguồn (đường dẫn trong `dot2/README.md`) xác nhận, hoặc **rút K017** khỏi đợt
   2 (mặc định nếu User chưa xem); (e) trần: spec §7 0,15 USD cho cả đợt sửa kho đã dùng 0,073 ⇒ A hỏi User trần riêng cho đợt 2 (khuyên 0,10).
3. **Thí nghiệm Qwen3-Embedding-8B** (User: "để session sau chạy"): plan duyệt **`52555da95828`** (`report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_plan.md`; B84 review
   ready vòng 2). **Cần User duyệt đầu phiên:** gửi toàn bộ kho + câu hỏi đánh giá ra OpenRouter (pin Nebius, `data_collection: deny`), tạo collection `hue_c78_qwen3_8b_4096`, xóa khi
   xong; trần 0,10 USD. Chạy **sau đợt 2** (kho cuối). C viết harness (`dense_runner` cho `build_candidate`, thử lại 429 / 5xx ≤ 3 + Retry-After, cache batch), B review code.
4. **Streaming:** đợi kết quả ChatGPT (`gửi chatgpt/2026-10-28/tìm thông tin/streaming_rag_citation_2026_10_28.md` **`c573949ac59a`** — User gửi, lưu vào `…/2026-10-28/kết quả
   nghiên cứu/`) ⇒ A đọc + WebFetch URL ⇒ cập nhật bản nháp `data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming.md` (`274bf12a650a`; PA0–PA3, C nghiêng PA1) ⇒ A brainstorm
   spec với User (`propose-options`, quyết định D0–D5 trong bản nháp). Số đo: chữ hiện sớm hơn trung vị **1,92 s** [1,61; 4,31] (C73). Hội thoại nhiều lượt sau streaming.
5. **Thước lỗi nặng (B89, C83 ready 2 vòng)** — chờ User: nhận bộ 32 câu an toàn tự viết làm bộ kiểm cho thí nghiệm sau? Sàn "P0_sai mới = 0" cần **đo nhiễu A/A trước**
   (≈ 0,008 USD, B + C cùng khuyên). Kết quả trên Golden: bịa thêm 1 / 145, P0_sai 0 / 65; bộ an toàn: P0_sai 2 / 27 (cả hai nói sai *về nguồn*, không đảo cảnh báo), ngoài kho
   0 / 4 bị trả lời. Mẫu người 20 câu `data/loi_nang_2026-10-28/human_sample.md` (User đọc khi rảnh; tới lúc đó số là tạm).
6. **B0** (mốc người, trước bảo vệ ~tháng 1/2027): User đọc `data/phase_8_2/b0/doc_cap_mu.md`, ghi `nhan_xet_user.md` ⇒ A mở `khoa.json` (chỉ A; **B đã thấy khóa — không tóm nhãn**),
   sub-agent mới tóm nhãn, luật dừng spec 8.2 §3 mục 4 ⇒ dừng / chưa rõ: A trình User giữ 10 / quay về 5 (spec 8.2 §11).

**Mục tiêu sản phẩm:** đồ án tốt nghiệp (bảo vệ ~tháng 1/2027; User: xong càng sớm càng tốt), xem như sản phẩm kinh doanh thật; người dùng = User, du khách, người dân.

**Mã hay gặp:** T1 = kết quả tìm 158 câu; A/A = hai lượt cùng cấu hình; F1–F4 / T1–T3 / W1–W8 = sàn / mức tụt / watch của plan đo trước ↔ sau (`sua_kho_do_truoc_sau_plan.md`);
H / P0_sai / P0_thiếu = chỉ số thước lỗi nặng (`do_loi_nang_plan.md`); Kxxx = mục kho; D1–D7 = quyết định đợt 2; S / W / I = sổ cải tiến; Bxx / Cxx = việc A giao (28/10: B78–B89, C70–C83).
M-n / m-n = finding major / minor của review; G0.6 = khóa bộ đo 8.1 (manifest); S36 = 36 câu kín (B3); K3b-m = biến thể "luna chọn 10 / 30" (gác); PA0–PA3 = phương án
streaming (bản nháp C77); Q1–Q5 = câu hỏi spec sửa kho §4; luật (a) / (i) = luật nhận biến thể spec 8.2 §10.2; NQ / QH / BRIDGE2 = ký hiệu nguồn trong `dot2/README.md`.

## Câu hỏi cho User (báo cáo mở phiên sau — mỗi câu có khuyến nghị)

1. **Quyền phiên.** A khuyên: như 28/10 (A tự điều phối + tự thử trong luật; ≤ 1 USD; B / C commit + push nhánh riêng theo việc).
2. **Trần đợt 2 sửa kho** — A khuyên 0,10 USD (đợt 1 dùng 0,073).
3. **Duyệt chạy Qwen3-8B** (gửi kho ra OpenRouter + collection thử, trần 0,10 USD) — A khuyên chạy sau đợt 2; "chưa rõ" là kết quả dễ xảy ra (B84: cần ~4 thắng / 0 thua).
4. **Gửi ChatGPT** yêu cầu streaming (`c573949ac59a`).
5. **Thước lỗi nặng:** nhận 32 câu an toàn; đo nhiễu một lượt mốc (≈ 0,008 USD) rồi mới đặt sàn P0_sai — A khuyên đồng ý.
6. **Đợt 2:** D1–D7 + 15 câu `data/sua_kho_2026-10-27/dot2/quyet_dinh_user.md` (mỗi mục có gợi ý; D2 ngày miễn vé: tra ngoài trước).
7. ✓ **Đã xóa** `c59-log`, `gold-v2`, `p82-b1` (User chạy `!` kết phiên 28/10, local + origin). Nhánh hồ sơ giữ: `p82-k1`, `p82-k3`,
   `p82-k3b`, `p82-r1`, `p82-r2`, `c70-ttft`.
8. (Khi bàn spec hội thoại nhiều lượt) **lưu câu hỏi người dùng?** — hướng 25/08 trái chính sách "log không ghi câu hỏi" (`chat.py:24-25`).
9. (Khi rảnh) B0; 20 câu mẫu lỗi nặng; xóa sao lưu đợt 1 sau khi đợt 2 xong.

## Câu hỏi A còn nợ (không cần User)

- Log `FileHandler` không xoay vòng (~400 byte / câu) — xem lại khi deploy.
- C65: G2.1a (8 câu) chưa đếm lại bằng validator hiện tại (không đổi kết luận đã đóng).
- Đoạn dài nhất sát trần tokenizer huydang (255 / 256) — đợt 2 đổi chữ ⇒ bước chia đoạn thử phải xem cột huydang; vượt ⇒ dừng, báo A.
- Sổ cải tiến: theo dõi **W30** (hook cảnh báo giờ ước), **W31** (lượt đo latency ⇒ cấm việc nặng song song), **I6**, W24–W26, W28 `đang thử` (vòng 9). Governance `25f23ae`: C kiểm
  — C kiểm `governance_vong9_review.md` ready 0 / 0 / 2: **nợ phiên sau** m-1 nới mẫu W30 (bắt cả `X` hoa, giờ 1 chữ số, `xx`), m-2 in `file:dòng` thay vì
  "dòng diff #N" (sửa xong ⇒ C kiểm lại).

## Session

| Vai | Terminal | Agent | Liên lạc | Việc phiên 28/10 | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | **`hue-rag-f7` (29/10)**; 28/10 `hue-rag-bf` | Claude Opus 5.5 | trực tiếp | 29/10: điều phối; 28/10: merge B1; 5 chỗ báo cáo; TONG_HOP 8.2; vòng cải tiến 9 | `STATUS_A.md`; 28/10 ≈ 0,0004 USD |
| B — thực thi | **`hue-rag-a7` (29/10)**; 28/10 `hue-rag-ac` | Claude Opus 5.5 | trực tiếp | 29/10: B90; 28/10: B78–B89 xong | `STATUS_B.md`; 28/10 ≈ 0,0948 USD |
| C — thực thi | **`hue-rag-ef` (29/10)**; 28/10 `hue-rag-32` | Claude Opus 5.5 | trực tiếp | 29/10: C84 → C85 → C86; 28/10: C70–C83 | `STATUS_C.md`; 28/10 ≈ 0,0103 USD |

Tên terminal đổi mỗi lần mở: `ListAgents`. Cả ba Claude Code ⇒ `trực tiếp`. **B / C lúc mở phiên sau:** không có việc đang chạy; mở phiên ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.
Việc A dự định giao: **B** áp đợt 2 (bước 1–10, như B81–B83), **C** review từng bước (như C75 / C76 / C80) + harness Qwen3-8B; A tổng hợp + báo cáo.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt: A tự
  duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run` trong `.venv`; luôn thử + so baseline trước khi chọn
  (User 24/10 20:49); commit trước sửa code + cổng ổn định sau mỗi gói (User 26/10).
- **Phiên 29/10 (User, trước 19:52 29/10/2026; hết hạn cuối phiên):** như 28/10 — A tự điều phối + tự thử / chọn trong luật; ≤ 1 USD; B / C commit + push nhánh riêng theo việc;
  đợt 2 ≤ 0,10 USD; Qwen3-8B ≤ 0,10 USD (gửi ra OpenRouter + collection thử duyệt); C84 ≤ 0,02 USD.
- **Phiên 28/10 — HẾT HẠN** (A tự điều phối + tự thử / chọn trong luật; ≤ 1 USD; B / C push nhánh riêng). Tiền phiên 28/10 ≈ **0,106 USD** (cổng merge 0,0004; B3 0,0138; bộ "trước"
  0,0361; C73 0,0103; cổng sau build 0,0004; bộ "sau" 0,0365; B89 bộ an toàn 0,0079).
- Trần đợt sửa kho đợt 1 0,15 USD (dùng ≈ 0,073; **đóng** User 28/10, giữ sao lưu). Giá `gpt-6-luna`: 0,1 USD / 1M vào, 0,5 USD / 1M ra (~0,00021 USD / câu context 10).

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v4.jsonl` (+ `gold_v4_CHANGES.md`) | **nhãn đoạn đúng mặc định** (kho sau đợt 1); v3 `3b1117cf59e9`, v2 `2f5a347a71ff`, v1 `bab707b9ab22` giữ | `927bae1bf201` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — **đã dùng ở B3** (người chạy B); vẫn không chép nội dung | md5 `ddc59587b502` |
| `data/phase_8_2/b0/` | đọc cặp mù (`nhan_xet_user.md` chưa ghi; **`khoa.json` chỉ A** `5b9240842b7b`) | — |
| `data/sua_kho_2026-10-27/` | README mục lục; đợt 1: `applied_edits.jsonl`, `eval_truoc/`, `eval_sau/`, `backup/`, `chunks_truoc.json`; **`dot2/`** (edits `9b5105b35e8b`, `quyet_dinh_user.md`, `review_b88.md`); `ket_qua_chatgpt_78_doi_chieu.md`; `cau_hoi_user.md` | — |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng: `analyze.json`, `human_sample.md` (+ `_key.json`), `an_toan/questions.jsonl` (32 câu, bản 3 `9fa81b0fcec4`) | — |
| `data/muc_tieu_san_pham_2026-10-28/doi_chieu_nghien_cuu.md` | đối chiếu nghiên cứu thước đo sản phẩm (7 nguồn khớp) | — |
| `data/tinh_nang_moi_2026-10-27/` | `c63_can_cu.md`; `c77_phuong_an_streaming.md` (nháp) | `274bf12a650a` |
| `data/streaming_ttft_2026-10-28/` | 10 câu tự viết + kết quả C73 | `107620cb30f1` (câu) |
| `gửi chatgpt/2026-10-28/tìm thông tin/streaming_rag_citation_2026_10_28.md` (+ `_doi_chieu.md`) | yêu cầu streaming, **chưa gửi** | `c573949ac59a` |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report
  `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file). Đổi người review ⇒ báo cả người cũ.
- **Cổng ổn định:** (1) test file chạm (lỗi thiếu key ghi rõ); (2) `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`:
  `/` 200, `/health` 5 / 5, 1 câu trong kho (200, `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết, body `{"query": …}`; đếm dòng `chat_metrics` mới = số câu (mốc ngay trước
  khi gửi), grep câu hỏi trong log = 0; client `perf_counter`; tắt server (TaskStop); (3) chạm tìm / chia đoạn: T1 giống byte (hoặc ghi mốc mới khi kho đổi); (4) đủ 5 chỗ
  (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency đang chạy ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (`WORKFLOW.md` §9.2, W31).
- Test cần key (không chạy mặc định): `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`.
- Đọc kho: **chỉ** `scripts/grep_kb.sh` (tên riêng: thêm `-i`); report tracked tả câu ở mức loại câu (S40 / S47).

## Hồ sơ đã đóng (chỉ tra cứu)

- Phase 8.2 (User đóng 28/10): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`; thí nghiệm `2026-10-26_cai_tien_tung_khau/`.
- Phiên 28/10 (đợt sửa kho đợt 1 — **User đóng**, streaming đo, plan 8B, thước lỗi nặng): `report_agent/2026-10-27_phan_ton_phase_cu/` — `TONG_HOP.md` §7, `sua_kho_*`,
  `streaming_ttft_*`, `qwen3_8b_plan*`, `do_loi_nang_*`.
