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

Tên terminal đổi mỗi lần mở: `ListAgents`. Cả ba Claude Code ⇒ `trực tiếp`. **B / C lúc mở phiên sau:** không có việc đang chạy; mở phiên ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Thường trực:** A commit / push (**tạm:** A stage từng file + đưa lệnh `!` vì auto mode chặn — S50, chờ User câu hỏi 3); B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ
  cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền; code luôn `uv run`; luôn thử + so baseline trước khi chọn.
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

## Hồ sơ đã đóng (chỉ tra cứu)

- Phase 8.2 (User đóng 28/10): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
- Đợt sửa kho 1 (28/10) + 2 (30/10), thước lỗi nặng, đo ngày hôm nay, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/` — `TONG_HOP.md` §7–§8.
