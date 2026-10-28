# STATUS B — KẾT PHIÊN 28/10/2026 (mở 08:45 — `date` lúc kiểm nhanh; ghi 13:20 28/10/2026 `date`)

Terminal: `hue-rag-ac` (A = `hue-rag-bf`, C = `hue-rag-32`) · Agent: Claude Opus 5.5 · Vai: thực thi. Mã việc = mã A giao (B78…B89).
Bản giữa phiên 28/10 (từng dòng việc + khai báo sửa B78–B89): `git show ed70c4a:session_prompt/sessions/STATUS_B.md`. Kết phiên 27/10 chiều: `git show 94eb683:session_prompt/sessions/STATUS_B.md`.

## Đang làm / dở

- **B89 — xong, C kiểm đạt cả hai phần:** report `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_implementation.md` (untracked, A commit; sha **`5553e480abfc`**).
  Golden: C83 ready 0/0/1 (m-1 sửa §2). Bộ an toàn §6: C review vòng 2 (`do_loi_nang_review.md` §7–§11, `8333d9c62753`) ready 0/0/1 — m-1 (chạy lại mốc 1 lần là kiểm nhiễu yếu)
  sửa ở đề xuất §6: (a) đo A/A 32 câu trước ≈ 0,008 USD (B + C khuyến nghị) / (b) chạy lại mốc + biến thể 3 lần câu bị bắt — **chờ A / User chọn**. Không còn việc dở.
- Không lượt paid, server, worktree nào của B đang chạy. File tạm `/tmp/b89_*` của B: **User đã xóa** (28/10, sau khi C kiểm xong). Worktree `.gemini/...` trong `git worktree list` **không phải của B**.

## Việc B phiên sau (A giao; User quyết 28/10: đóng đợt 1 GIỮ sao lưu; đợt 2 áp phần sẵn sàng **đầu tiên**; Qwen3-8B chạy phiên sau)

1. **Áp đợt 2 sửa kho** — `data/sua_kho_2026-10-27/dot2/edits/dot2.jsonl` sha **`9b5105b35e8b`** (bản 3: 104 edit / 33 file; README `dot2/README.md`; review B88 3 vòng `dot2/review_b88.md`;
   phần User quyết D1–D7 ở `dot2/quyet_dinh_user.md`, 4 dòng K004 chờ D1 ở `edits/k004_user_lines.jsonl` — **không áp** dòng chưa quyết). Chạy lại chuỗi bước 1–9 như đợt 1:
   - kiểm sha `dot2.jsonl` trước khi áp; áp bằng `data/sua_kho_2026-10-27/tools/apply_edits.py` (chuỗi cũ khớp đúng 1 lần, **theo thứ tự áp** — C76) — xem script có nhận file
     edit khác / ghi `applied_edits` riêng (đừng ghi đè `applied_edits.jsonl` của đợt 1);
   - sao lưu file sắp sửa (thư mục mới, không đè `knowledge-base-hue/meta/backup_sua_kho_2026-10-28/` — User GIỮ bản đợt 1) + phiếu build + từ điển + snapshot Qdrant;
   - chia đoạn thử ⇒ **xóa 3 đích** (collection + phiếu build + `full_corpus_sparse_state.json`) — **auto mode chặn B** ⇒ đưa User lệnh `!` (đợt 1: User chạy) ⇒ build lại ⇒ kiểm
     điểm / payload / `/health`; T1 mới (đợt 1: `23c58c47635d`);
   - bước 7–8: nhãn đoạn đúng (gold v4 `927bae1bf201` ⇒ v5 nếu trích dẫn đổi chữ, User duyệt) + quét Golden chạm phần sửa (`data/sua_kho_2026-10-27/tools/golden_scan.py`);
   - bước 9: đo "trước ↔ sau" (`truoc_sau.py`; đợt 1 report `sua_kho_b9_implementation.md`), chấm mù cùng lượt; trần tiền A ghi khi giao.
   - Plan đợt 1: `sua_kho_do_truoc_sau_plan.md` (A duyệt `41485782b39e`) — hỏi A có cần plan mới hay dùng lại có ghi lệch.
2. **Ý kiến B: bộ "trước" của đợt 2 dùng lại bộ "sau" đợt 1 (`data/sua_kho_2026-10-27/eval_sau/sau.jsonl`, 0,036 USD) được KHÔNG?**
   **Được, nếu qua kiểm "còn hiệu lực"** — làm đúng như B78 bước 0 đã làm trước đợt 1: (a) `git diff` `backend/` từ commit chạy bộ "sau" (`e08a126` là commit cuối đụng `backend/`)
   tới HEAD không đụng đường retrieval / context / prompt / sinh / settings; (b) phiếu build vẫn `574b5d02088b`, `full_corpus_sparse_state.json` không đổi, kho không đổi so với lúc
   chạy (phiếu build kiểm vân tay); (c) chạy lại T1 158 câu (free) giống byte `23c58c47635d`; (d) model / `max_context_documents` như meta của `sau`. Một mục lệch ⇒ chạy bộ
   "trước" mới (~0,036 USD). **Lợi:** tiết kiệm 0,036 USD + ~10 phút. **Giá:** hai lượt sinh cách nhau nhiều giờ / ngày ⇒ phía provider có thể đổi (cùng tên model) — nhiễu này
   lẫn vào "trước ↔ sau"; đợt 1 có A/A = 2 lượt nên luật "mức tụt cho phép" đã tính nhiễu sinh, nhưng **không** tính trôi theo ngày. **Chấm:** dù dùng lại câu trả lời, vẫn chấm
   **lại** "trước" và "sau đợt 2" cùng một lượt mù (judge cùng lượt — đợt 1 làm vậy), không dùng điểm cũ. Khi nào sai: nếu bộ "sau" đợt 1 có câu lỗi / 500 phải chạy lại thì
   câu đó chạy lại ở cả hai bên.
3. **Review harness Qwen3-8B** (C viết; plan `qwen3_8b_plan.md` bản 2 `52555da95828`, B review `qwen3_8b_plan_review.md` ready 0/0/0 vòng 2). Chạy cần User duyệt gửi kho ra
   OpenRouter + collection thử `hue_c78_qwen3_8b_4096` (xóa khi xong), trần 0,10 USD. Kiểm khi review: latency_gate theo luật spec 8.2 (B84 M-1), collection riêng không đụng
   collection đang chạy, ghi từng dòng / từ chối ghi đè, pin provider Nebius, `data_collection: deny`.
4. **B89 còn lại:** sửa theo review C của §6; nếu A / User nhận đề xuất §6 (bộ 32 câu làm bộ kiểm an toàn; sàn "P0_sai mới = 0" kèm chạy lại mốc câu bị gắn; hoặc đo nhiễu 1 lượt mốc
   ≈ 0,008 USD) thì dùng harness `tools/an_toan_gen.py` + `tools/an_toan.py` (cho biến thể: thêm tham số đích / tên lượt — hiện code đọc `answers_*.jsonl` trong `an_toan/`).

## File / sha / dữ liệu quan trọng (B làm phiên này)

| Việc | File chính (private ở `data/` trừ khi ghi) | sha |
|---|---|---|
| B89 thước lỗi nặng | `data/loi_nang_2026-10-28/` — rubric `rubric.md`; harness `tools/loi_nang.py`; `contexts.jsonl`; `controls_key.json`; `negatives_c_confirm.json`; `judge{1,2}/`; `analyze.json`; `per_case.json`; `human_sample.md` (+key, cho User đọc) | `b1b2848be9c6`, `58ecada9652f`, `adb893b4ad5d`, `739e01cdfb92`, `32e4b41e4d6f`, —, `135b387cb037`, `aa1b35bfc6b2`, `453ff9172982` |
| B89 bộ an toàn | `data/loi_nang_2026-10-28/an_toan/` — `questions.jsonl` (C đạt bản 3), `c_check.md` (C), `answers_{pilot,rest,rest2}.jsonl`, `controls_key.json`, `judge{1,2}/map.json`, `analyze.json`, `per_case.json`; harness `tools/an_toan_gen.py`, `tools/an_toan.py` | `9fa81b0fcec4`, `c233175801d9`, —, `a41f609c2348`, `802edb4b258c` / `87504c37bd70`, `358ca95ef7f1`, `e6c67aea7eca`; `b4f5577540d0`, `b2a91543299b` |
| B89 plan + report | `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_plan.md` (A duyệt), `do_loi_nang_implementation.md` (untracked) | `d69481b2addb`, `c733012dfcc6` |
| Đợt sửa kho 1 (B78, B81–B83) | `data/sua_kho_2026-10-27/` — `applied_edits.jsonl`, `tools/{apply_edits,truoc_sau,golden_scan,gate_b81}.py`, `eval_truoc/`, `eval_sau/`, `judge/`, `analyze.json`, `backup/`; kho backup `knowledge-base-hue/meta/backup_sua_kho_2026-10-28/` | phiếu build `574b5d02088b`, T1 `23c58c47635d`, gold v4 `927bae1bf201` |
| Báo cáo hệ thống (B85, B86) | `bao_cao_he_thong/BAO_CAO_KHO_DU_LIEU.md` bản 5, `BAO_CAO_DANH_GIA.md` bản 4 | A đã commit |
| B80 (B3 câu kín) | `data/phase_8_2/b3/`; report `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_implementation.md` | — |

## Vừa xong (phiên 28/10)

| Mã | Việc ⇒ kết quả |
|---|---|
| B78 | plan đo "trước ↔ sau" đợt sửa kho (A duyệt `41485782b39e`) + bước 0 bộ "trước" 176 câu (0,0361 USD) |
| B79, C70, C73 | review tài liệu 8.2 (ready 0/0/5); review plan TTFT (changes_requested 0/1/4); review harness TTFT (ready 0/0/2) |
| B80 | B3 mốc cuối trên câu kín S36: không làm hỏng + tốt hơn (Completeness +0,818); 0,0138 USD |
| B81–B83 | đợt sửa kho 1 bước 1–9: 123 edit / 65 file, build lại 204 file / 8.426 đoạn, gold v4, Golden 0 câu sửa, "sau": không làm hỏng (0,0365 USD) |
| B84, C78 | review plan Qwen3-8B (changes_requested 0/1/4 ⇒ bản 2 ready) |
| B85, B86 | BAO_CAO_KHO_DU_LIEU bản 5, BAO_CAO_DANH_GIA bản 4 |
| B87, B88 | plan thước lỗi nặng (A duyệt `d69481b2addb`); review đợt 2 sửa kho 3 vòng |
| B89 | thước lỗi nặng: Golden H 1/145, P0_sai 0/65 (0 USD); bộ an toàn 32 câu: ngoài kho 0/4 bị trả lời, P0_sai 2/27 (cả hai nói sai về nguồn, 0 đảo cảnh báo), P0_thiếu 8/27 (0,0079 USD) |

## Tiền paid phiên 28/10 (B)
- B80 0,0138125 + B78 bước 0 0,0361284 + B81 2 câu thử ≈ 0,0004 + B83 bộ "sau" 0,036454 + B89 an toàn 0,007943 ⇒ **≈ 0,0948 USD** (≈ 2.370 đồng). Mọi lượt dưới trần A ghi.
- Quota Claude (không USD): B89 Golden 16 judge ≈ 1,6 M token; B89 an toàn 8 judge ≈ 0,55 M; B81–B83 judge + sub-agent (xem report).

## Câu hỏi cho A / User
- A: đợt 2 dùng lại plan đợt 1 (ghi lệch) hay plan mới? Trần tiền đợt 2? Dùng lại bộ "sau" đợt 1 làm "trước" (ý kiến B ở trên) — A quyết.
- A / User: nhận đề xuất B89 §6 (bộ kiểm an toàn + sàn P0_sai mới = 0)? Cách tính nhiễu (a) đo A/A trước ≈ 0,008 USD (khuyến nghị) hay (b) chạy lại 3 lần câu bị bắt?
- User (khi rảnh, không chặn): đọc `data/loi_nang_2026-10-28/human_sample.md` (20 câu) — tới khi có, số H / P0 là tạm.
- A (W30 đã đề xuất): hook cảnh báo giờ ước — B lọt 5 lần phiên này (bẫy dưới).

## Đã học / bẫy gặp (phiên 28/10)
- **Giờ ước vào file — 5 lần** (08:4x, 09:50, 12:1x, 13:14, 13:19): luôn tự bắt, sửa bằng `date`. Cách tránh: chạy `date` **trước**, rồi mới viết dòng có giờ; grep `[0-9]:[0-9]x`
  trước khi báo sha; không gõ giờ trong cùng lệnh làm việc khác.
- (B89) Khóa `by_src` = `src` ⇒ 145 câu thật gộp thành 1; lộ ở cổng `bao_nham_that` [0,1]. Cách tránh: `assert len(dict) == số item` mỗi lần dựng map (đã thêm vào `an_toan.py`).
- (B89) Cổng trần tiền đọc lại file đang ghi + cộng biến đếm ⇒ đếm hai lần, dừng sớm (không tốn thêm). Cách tránh: đọc tiền các lượt trước **một lần** trước vòng lặp.
- (B89) Ngữ cảnh production có gạch đầu dòng kép "- - **…**" ⇒ hàm bỏ Markdown một lần không đủ; kiểm mắt câu đối chứng **trước** khi giao judge (B bắt kịp).
- (B89) Viết câu thử tự do vẫn dễ trùng **dữ kiện** Golden dù khác chữ (6 câu Jaccard 0,4–0,5; 1 câu C bắt qua đáp án mẫu). Cách tránh: so cả đáp án mẫu, không chỉ câu hỏi.
- (B89) Kho có chỗ 2 nguồn lệch (vé trẻ em) — câu thử rơi vào đó làm nhiễu P0 ⇒ tránh khi viết câu; ghi sang đợt sửa kho.
- (B82, B89) S40 lọt: loại thông tin cạnh mã câu trong report tracked — C bắt. Cách tránh: trước khi gửi report tracked, grep mã câu và xem cạnh đó có danh từ chủ đề không.
- (B81) Auto mode chặn Qdrant DELETE + `rm` file build ⇒ dừng, đưa User lệnh `!`; không nhờ session khác chạy.
- (B82) `why()` so offset đoạn ⇒ báo "tìm đổi đoạn" giả ⇒ so tập `chunk_id`. `build_gold_v4.py` tìm edit chồng trên file gốc ⇒ đợt 2 đi theo **thứ tự áp** (C76).
- (B81) `tail -0` trong pipe làm lệnh kiểm T1 không ra file — chạy lại; kiểm file ra tồn tại trước khi so sha.
- Từ trước (giữ): harness ghi từng dòng, từ chối ghi đè; tiền tính bằng token thật; sub-agent động vào kho chỉ grep bằng `scripts/grep_kb.sh`; worktree log mất khi gỡ ⇒ chép
  `chat_metrics` trước; thử hành vi script gọi `/usr/bin/grep` (shell có hàm `grep` = ugrep); report public tả ở mức loại câu; `uv run` cho code.
