# STATUS C — PHIÊN 30/10 (mở 10:31 30/10/2026 `date`; cập nhật 12:00 30/10/2026)

Terminal `hue-rag-0e` · A = `hue-rag-0f` (suy ra: B tự báo là `hue-rag-24`), B = `hue-rag-24` (trực tiếp). Quyền phiên 29/10 **hết hạn**; chờ A giao việc.
Kiểm nhanh 10:31 30/10/2026: `main` `d8401d1`, không thay đổi tracked, hook `.githooks`, Qdrant 1 collection 8.426 point — khớp handoff.
Lệch: `dot2.jsonl` vẫn bản 4 `cdec67127c4d` (bản 4b của B chưa dựng); 3 report untracked (C84, plan B, review C85); 4 worktree AGY (`~/.gemini/…`, commit `c725987`) handoff không nhắc — không đụng; `tham khảo 26_10/` không còn.
User (10:41 30/10/2026 ghi nhận, terminal C): C làm việc trực tiếp với A, báo cáo cho A; **việc A giao = User nói "làm đi"**. Chờ A giao.
**C87 (A giao 10:57 30/10, = "làm đi")** — nhận 11:02 30/10/2026. Khai báo sửa: `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan_review.md`, `…/do_loi_nang_aa_implementation.md` (dòng Date),
`data/sua_kho_2026-10-27/dot2/c87_doc_lai_nguon_2026-10-30.md` (mới, private); file tạm `/tmp/c87_src/`, `/tmp/c87_tools/` (HTML nguồn web, không chữ kho) — xóa khi xong. Dòng C trong `CURRENT_HANDOFF.md`.
**C87 xong 11:09 30/10/2026:** C85 vòng 2 `changes_requested` 0/1/1 (M-4 thứ tự `dump-headings` bước 1; m-4 lý do K017); 4b `c0b5876ea510` đạt; nguồn K017 / D2 / D6 khớp; `<T>` điền; C84 m-2 sửa. `/tmp/c87_*` đã xóa. 0 USD. Chờ B sửa M-4 ⇒ C kiểm phần sửa; rồi kiểm từng bước áp; C86 sau.
Bẫy 30/10: trang nguồn D2 trả gzip dù không xin (curl không `--compressed`) ⇒ tách chữ ra rỗng; luôn `file` / `gunzip` trước khi kết luận "trang không có".
A (11:09 30/10/2026 ghi nhận): duyệt 4b `c0b5876ea510`; B sửa M-4 + m-4 ⇒ C kiểm vòng 3 (chỉ phần sửa). Harness Qwen3-8B nay là **B92** (B viết, nhánh `b92-qwen3-harness`) — C review khi B báo bản cuối (thay C86). C rảnh tới lúc đó.
**C85 vòng 3 11:12 30/10/2026: ready 0/0/0** (plan `5f30ac7eac16`, bảng `92e5b3caf6f1`). Tiếp: kiểm từng bước khi B áp đợt 2; review code B92 khi B báo.
A (11:16 30/10/2026 ghi nhận): duyệt plan `5f30ac7eac16` + bảng `92e5b3caf6f1`; **B93** áp đợt 2 bước 1–6 + bộ "sau" + 32 câu an toàn. C kiểm khi B báo: diff backup (sau bước 2), chia đoạn thử, build record / T1, quét Golden. **W31: đang ghi kho / Qdrant + đo ⇒ C không việc nặng / trả phí.** B92 review sau đo "sau".
Kiểm B93 bước 1 (11:24 30/10/2026): khai báo file mới `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_b1_review.md`.
**C88 (A giao, 11:26 30/10/2026 nhận):** review code B92 (nhánh `b92-qwen3-harness` `8545650`). Khai báo: file mới `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_harness_review.md`; worktree đọc riêng `/tmp/c88_wt` (gỡ khi xong). Không gọi OpenRouter / tạo collection; không việc nặng khi B ở bước 2–6.
**C88 xong 11:31 30/10/2026:** code `changes_requested` 0/1/1, plan sửa đổi ready. Worktree `/tmp/c88_wt` đã gỡ. Chờ B sửa M-1 ⇒ C kiểm lại; chờ B93 bước 2.
A (11:32 30/10/2026 ghi nhận): duyệt plan `70ee5d44c260`; M-1 theo cách 1 + p50/p95 báo **cả hai** (mọi câu / chỉ câu gọi một lần) + số câu thử lại; luật dừng mới "câu phải thử lại > 5 % ⇒ dừng"; m-1 B sửa. ⇒ C kiểm phần sửa khi B báo commit + sha plan; T1 sau rebase kho đợt 2.
**C88 vòng 2 11:35 30/10/2026: ready 0/0/0** (code `fb0b82c`, plan `9f3d616e2a59`). Worktree `/tmp/c88b_wt` đã gỡ. Chờ B93 bước 2; T1 B92 sau rebase.
**C89 (A giao, 11:45 30/10/2026 nhận):** (a) đếm lỗi citation mọi lượt đo; (b) nháp streaming v2. Khai báo: file mới `data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming_v2.md`, `data/tinh_nang_moi_2026-10-27/c89_dem_loi_citation.md` (+ script `data/tinh_nang_moi_2026-10-27/tools/c89_count.py`). 0 USD, không sửa code.
**C89 xong 11:50 30/10/2026:** (a) `c89_dem_loi_citation.md` — cấu hình đang chạy 0 / 489 lần sinh (0 / 841 kể cả chấm lại v2), cận trên ≈ 0,6 %; lỗi còn lại chỉ dạng "không có [n]"; (b) `c77_phuong_an_streaming_v2.md` (v1 giữ `274bf12a650a`). 0 USD.
**C90 (A giao, 11:51 30/10/2026 nhận):** nháp bảng giới hạn đã biết Phase 0–8. Khai báo: file mới `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md`. Chỉ đọc, 0 USD.
**C90 xong 11:54 30/10/2026:** `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` — 33 giới hạn (chất lượng 11, PCN 5, chia đoạn / index 6, đo 6, vận hành 5). 0 USD.
**C91 (A giao, 11:55 30/10/2026 nhận):** nháp phương án hội thoại nhiều lượt. Khai báo: file mới `data/tinh_nang_moi_2026-10-27/c91_phuong_an_nhieu_luot.md`. 0 USD.
**C91 xong 11:58 30/10/2026:** `c91_phuong_an_nhieu_luot.md` (`1c0313aafd25`) — PA0–PA3, C nghiêng PA1 (trình duyệt giữ, server không lưu, luật chữ, ≤ 3 đoạn `[11]`–`[13]`), đo cặp PA1 ↔ PA2; D0–D7. Tiếp: sửa 3 minor C89 (B review `c89_review.md`).
**C89 minor sửa 11:59 30/10/2026:** m-1 / m-2 / m-3 (B `c89_review.md`); sha c89 `575f128f1c86`, nháp v2 `b19f8454e22b`. Bẫy: "chỉ một dạng lỗi" là nói quá — phải tách *quan sát* với *code cho phép*. Chờ A / B93 bước 2.

**Tóm tắt lúc 12:00 30/10/2026:** xong C87 (C85 vòng 2–3 ready), kiểm B93 bước 1 ready, C88 (B92 vòng 2 ready, plan sửa đổi ready), C89 (+ 3 minor), C90, C91. Tiền paid C phiên 30/10: **0 USD**.
**Đang chờ:** A nhắn B "chạy bước 2" (User về ~13:00) ⇒ C kiểm từng bước đợt 2: diff với backup sau bước 2 (`knowledge-base-hue/meta/backup_sua_kho_dot2_2026-10-30/`), `dump-headings --arm truoc` có chạy trước bước 5, chia đoạn thử (cột huydang ≤ 256), build record / T1 mới, quét Golden. Sau đợt 2: T1 nhánh B92 sau rebase. Không việc nặng trước đó.
**File C tạo phiên này (private, không commit):** `data/sua_kho_2026-10-27/dot2/c87_doc_lai_nguon_2026-10-30.md`; `data/tinh_nang_moi_2026-10-27/{c89_dem_loi_citation.md, c77_phuong_an_streaming_v2.md, c91_phuong_an_nhieu_luot.md, tools/c89_count.py}`; `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md`. **Tracked (untracked, A commit):** `report_agent/2026-10-27_phan_ton_phase_cu/{sua_kho_dot2_do_plan_review.md, do_loi_nang_aa_implementation.md, sua_kho_dot2_b1_review.md, qwen3_8b_harness_review.md}`.
**Bẫy 30/10:** curl trang nguồn có thể trả gzip / cần cookie JS ⇒ kiểm `file`, đọc HTML gốc trước khi kết luận "không có"; đừng nói "chỉ một dạng lỗi" khi mới chỉ *quan sát* một dạng.

**C90 bản 2 12:02 30/10/2026:** sửa theo B `gioi_han_da_biet_review.md` (M-1 + m-1…m-4 + gợi ý) ⇒ 36 dòng, sha `6113fce7b3fe`; B kiểm phần sửa. Bẫy: đừng dẫn số dòng `CURRENT_HANDOFF.md` (đổi hằng ngày) — dẫn tên mục.
**C90 vòng 2 (12:04 30/10/2026): B ready 0/0/0** (bản 2 `6113fce7b3fe`, `gioi_han_da_biet_review.md` §5). Chờ đợt 2 bước 2.
**C92 (A giao, 12:09 30/10/2026 nhận):** review plan B96 "không biết ngày hôm nay". Khai báo: file mới `data/ngay_hien_tai_2026-10-30/plan_nhap_review.md`. Chỉ đọc, 0 USD.
**C92 xong 12:13 30/10/2026:** review plan B96 `ccaf9b426197` ⇒ `changes_requested` 0/1/4 (`data/ngay_hien_tai_2026-10-30/plan_nhap_review.md`). Chờ B sửa ⇒ C kiểm phần sửa.
**C92 vòng 2 12:17 30/10/2026: ready 0/0/0** (plan B96 bản 2 `fd63d9192ef6`).
Việc dở chờ giao (từ phiên 29/10, dưới): C85 vòng 2 + phần NOT RUN; điền `<T>` 2 report; C86 harness Qwen3-8B. Handoff: A mới hỏi User xác nhận mục tiêu mới ⇒ thứ tự có thể đổi.

---

# STATUS C — KẾT PHIÊN 29/10 (cập nhật sau 21:16 29/10/2026 `date`; Bash bị chặn lúc ghi nên chưa lấy được giờ mới)

Terminal `hue-rag-ef` · A = `hue-rag-f7`, B = `hue-rag-a7` (trực tiếp). Quyền phiên như 28/10 (User, qua A) — **hết hạn cuối phiên**. Việc: C84 → C85 → C86 (`CURRENT_HANDOFF.md` mục "PHIÊN 29/10").

## Phiên 29/10

| Mã | Việc | Kết quả | File |
|---|---|---|---|
| C84 | đo nhiễu A/A thước lỗi nặng (32 câu an toàn) | **xong, chờ B kiểm.** Lượt 2 32 / 32, 0 lỗi, ngữ cảnh giống từng chữ lượt 1; chấm mù trộn 2 lượt + 15 đối chứng, 2 judge (8 sub-agent). Cổng đối chứng đạt; nhiễu chấm 0; P0_sai 2 → 0 (S11, S12), 0 câu mới; H y hệt. Sàn A nhận: P0_sai mới ≤ 2 (hai chiều) + sinh lại 3 lần; đảo cảnh báo = 0 | `report_agent/…/do_loi_nang_aa_implementation.md`; `data/loi_nang_2026-10-28/tools/an_toan_aa.py`; `data/loi_nang_2026-10-28/an_toan/aa_2026-10-29/` |
| C85 | review B90 (tham số, `dot2.jsonl` bản 4, phụ lục plan) | **vòng 1 changes_requested 0/3/3**; A quyết M-1 / M-2 / M-3 (bỏ dòng D1-K004 (3)(4)) + bỏ D7 (bản 4b) | `report_agent/…/sua_kho_dot2_do_plan_review.md` |
| C86 | harness Qwen3-8B | **dời phiên sau** (A) | — |

**Tiền paid phiên 29/10 (C): 0,0081144 USD** (C84 lượt sinh). Judge: quota Claude (~0,8 M token), 0 USD.

**Dở — phiên sau làm TRƯỚC bước 1 áp kho đợt 2:**
1. C85 vòng 2 trên `dot2.jsonl` bản 4b (B báo sha) + phụ lục sửa M-1 / M-2.
2. NOT RUN vòng 1: đọc lại độc lập nguồn K017 / D2 / D6 bằng WebFetch (URL trong `dot2/b90_quyet_dinh.md` §1); `sha256sum` 5 file đầu vào; `diff` 2 script với `tools/truoc_b90/`;
   104 edit cũ = bản 3 (trừ K017 edit 2); bảng = jsonl; `apply_edits.py --edits` chạy thử; `scripts/grep_kb.sh` cho Q6.
3. Điền giờ `date` thay chữ `<T>` ở dòng "Date" của `do_loi_nang_aa_implementation.md` và `sua_kho_dot2_do_plan_review.md`.
4. ✓ **Đã xóa** `/tmp/judge_a0/`, `/tmp/judge_a2/`, `/tmp/judge_a1_1/`, `/tmp/judge1_a1_1_mine/`, `/tmp/judge_a2_1/` (script nháp của sub-agent judge, có chữ kho) — User chạy `!` ở terminal C tối 29/10.
5. C86 harness Qwen3-8B.

**Bẫy gặp phiên 29/10 (đầu vào vòng cải tiến):**
- **Máy kiểm an toàn của auto mode lỗi server ~20:30–21:30** ⇒ Bash / WebFetch / SendMessage / Agent bị chặn chập chờn (Read / Write / Edit vẫn chạy). Cách đi tiếp được: làm phần
  chỉ cần đọc file (review diff bằng Read hai bản), ghi report với chỗ trống `<T>` và mục NOT RUN rõ ràng, thử lại công cụ giữa các bước; không gõ giờ ước.
- Sub-agent judge cũng bị chặn Bash ⇒ 2 / 8 lô viết file nhãn bằng Write, chưa tự kiểm JSON ⇒ `check` của người giao bắt buộc trước khi dùng số (lượt này 71 / 71, 0 lỗi).
- Sub-agent để script nháp có chữ kho ở `/tmp` dù brief không yêu cầu ⇒ brief judge lần sau: "không tạo file ngoài file nhãn; cần script thì viết vào `/tmp/<tên lô>/` và xóa khi xong".
- **Đếm nhiễu A/A một chiều là sai** khi hai lượt cùng cấu hình (hoán đổi được): C viết finding M-2 theo một chiều trước khi có số, có số rồi phải sửa lại thành hai chiều.

- Sửa dòng cũ: hai review ở §1 phiên 28/10 dưới đây **đã commit** (`979537d`).

---

# STATUS C — KẾT PHIÊN 28/10 (cập nhật 13:26 28/10/2026)

Terminal phiên 28/10: `hue-rag-32` (tên đổi mỗi lần mở — dùng `ListAgents`) · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-bf`, B = `hue-rag-ac` (trực tiếp).
Đầu phiên: `dccdb74`; cuối phiên HEAD `25f23ae`. Quyền phiên 28/10 (User, qua A): A tự điều phối; API ≤ 1 USD cả phiên; B/C commit + push nhánh riêng theo việc. **Quyền hết hạn cuối phiên.**
STATUS cũ: phiên 27/10 chiều = `git show dccdb74:session_prompt/sessions/STATUS_C.md`; phiên sáng 27/10 = `git show fb1eade:session_prompt/sessions/STATUS_C.md`.

## 1. Đang làm / dở

- **Không việc dở.** Không worktree, server, nhánh mới của C còn chạy. Worktree thử hook `/tmp/c_gov9_wt` đã gỡ. File tạm `/tmp/c84_terms.tsv`, `/tmp/c85_read.txt` đã xóa
  (file sau có chữ kho). Các file `/tmp/c_*` khác **không** phải của C phiên này — không đụng.
- Hai review cuối **chưa commit** (A commit): `do_loi_nang_review.md` (thêm vòng 2, §7–§11, sha `8333d9c62753`), `governance_vong9_review.md` (mới, `bdd3c8f71785`).
  File governance có **cố ý** các dòng thử dạng giờ ước (bảng §4) ⇒ hook W30 sẽ in cảnh báo khi commit — đúng, không phải lỗi.

## 2. Việc C làm phiên 28/10 (mã A giao; chi tiết ở report / review)

| Mã | Việc | Kết quả | File |
|---|---|---|---|
| C70 | plan đo thời gian tới chữ đầu tiên (streaming) | v2 `9683641b6c38` A duyệt | `streaming_ttft_plan.md` |
| C71 | kiểm merge B1 `510e1a8` | ready 0/0/0 | `phase_8_2_b1_merge_review.md` |
| C72 | review plan B78 (đo trước ↔ sau sửa kho) | ready 0/0/6 ⇒ v2 6/6 đóng | `sua_kho_do_truoc_sau_plan_review.md` |
| C73 | harness + chạy TTFT (nhánh `c70-ttft`, `9ff45d1`, `1f70095`; `ttft.py` `7e992e229fc5`, 7 test) | 31 lần, 0 lỗi, **0,010291 USD**; lợi hiện chữ sớm 1,92 s CI [1,61; 4,31] (clear); lợi tới câu có [n] 1,01 s (moderate). Nhánh giữ làm hồ sơ | `streaming_ttft_implementation.md` |
| C74 | review B3 câu kín (giữ mù) | ready 0/0/1 | `phase_8_2_b3_review.md` |
| C75 | kiểm sửa kho bước 1–6 | ready 0/0/1 | `sua_kho_b1_6_review.md` |
| C76 | kiểm sửa kho bước 7–8 | ready 0/0/1 | `sua_kho_b7_8_review.md` |
| C77 | yêu cầu ChatGPT streaming + nháp phương án | yêu cầu `c573949ac59a` (B đối chiếu đạt; **User chưa gửi**); nháp PA0–PA3 `274bf12a650a` | `gửi chatgpt/2026-10-28/tìm thông tin/streaming_rag_citation_2026_10_28.md`; `data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming.md` |
| C78 | plan Qwen3-8B | v2 `52555da95828` A duyệt; **chạy chờ User** (gửi kho ra OpenRouter + collection mới) | `qwen3_8b_plan.md` |
| C79 | kiểm code B83 + soạn đợt 2 sửa kho | code review ready 0/0/3; đợt 2 bản 3 `dot2.jsonl` `9b5105b35e8b` (104 edit / 33 file), B kiểm ready 0/0/0; **áp chờ User** (D1–D7 + 15 câu mở) | `sua_kho_b83_code_review.md`; `data/sua_kho_2026-10-27/dot2/` (README `db5ce14a344a`, `quyet_dinh_user.md`, `tools/build_dot2.py` `2afb0d843f58`) |
| C80 | kiểm bước 9 B83 | ready 0/0/1 | `sua_kho_b9_review.md` |
| C81 | review plan B87 (thước lỗi nặng) + xác nhận câu âm | v1 changes_requested 0/1/4 ⇒ v2 `d69481b2addb` ready; câu âm 15 / 16 (`negatives_c_confirm.json` `32e4b41e4d6f`) | `do_loi_nang_plan_review.md` |
| C83 | review B89 phần Golden | ready 0/0/1 (câu lạc đề quá dễ) | `do_loi_nang_review.md` §1–§6 |
| C84 | kiểm bộ câu an toàn trước khi sinh (3 vòng) | bản 3 `9fa81b0fcec4` đạt 32 / 32 | `data/loi_nang_2026-10-28/an_toan/c_check.md` `c233175801d9` |
| C85 | review B89 §6 (kết quả bộ an toàn) | ready 0/0/1 — m-1: sàn "P0_sai mới = 0" cần đo nhiễu A/A trước (≈ 0,008 USD) | `do_loi_nang_review.md` §7–§11 |
| C86 | review governance vòng 9 (`25f23ae`: W30, W31, I6) | ready 0/0/2 — m-1 mẫu hook lọt `X` hoa / giờ 1 chữ số / `xx`; m-2 cảnh báo in nội dung, không in tên file | `governance_vong9_review.md` |

## 3. Việc C làm phiên sau

1. **Harness Qwen3-8B** theo plan `52555da95828` — **chạy cần User duyệt đầu phiên** (gửi kho ra OpenRouter, collection Qdrant mới, trần plan). Trước khi chạy: hỏi A có lượt đo
   latency nào đang chạy không (W31).
2. **Review đợt 2 sửa kho khi B áp** (sau khi User trả lời D1–D7): đối chiếu backup + `dot2.jsonl` (áp lần lượt trong bộ nhớ), chia đoạn thử — 2 edit đổi tiêu đề mục `###` làm đổi
   `heading_path`; kiểm `full_corpus_conditions.json` (chọn theo nguyên văn), build lại, T1. K017 chỉ dựa một nguồn khó đọc ⇒ người áp đọc lại nguồn trước.
3. **Cập nhật nháp phương án streaming** (`c77_phuong_an_streaming.md`) khi có kết quả ChatGPT (User gửi yêu cầu `c573949ac59a`); đối chiếu URL bằng WebFetch; số đo C73 là căn cứ.
4. Nếu A / User chọn cách đặt sàn an toàn (C85 m-1): kiểm lượt chạy lại mốc 32 câu (A/A) khi B làm.

## 4. Câu hỏi cho A / User

- **User:** đợt 2 — D1 (4 dòng chỉ còn cấp quận đứng tên; C gợi ý b), D2 (ngày miễn vé thứ hai; gợi ý tra ngoài trước), D3–D7, 15 câu mở (`dot2/quyet_dinh_user.md`).
- **User:** duyệt chạy Qwen3-8B (`qwen3_8b_plan.md` v2); gửi yêu cầu ChatGPT streaming.
- **A / User:** sàn bộ câu an toàn — (a) đo A/A 32 câu trước rồi viết sàn theo nhiễu (C nghiêng), hay (b) chạy lại câu bị bắt 3 lần cả mốc lẫn biến thể.
- **A:** hook W30 — nới mẫu hay ghi giới hạn vào sổ (m-1); in `file:dòng` thay nội dung (m-2). `STATUS_A.md:18` còn bẫy đã dời sang Project_Status và có giờ ước (dòng cũ).

## 5. Tiền paid phiên 28/10 (C)

- **Log: 0,010291 USD** (C73, lượt TTFT pilot + thật). Mọi việc khác của C: 0 USD (judge / review: quota Claude Code; WebFetch miễn phí).

## 6. Bẫy gặp phiên 28/10 (đầu vào vòng cải tiến)

- **Ghi giờ ước vào file (4 lần trong phiên: dạng `HH:Mx` và dạng giờ trông như thật).** Luật: `T=$(date '+%H:%M %d/%m/%Y')` ngay trước khi ghi. Viết file bằng Write thì để chỗ trống `<T>`
  rồi thay bằng `$T`. Không nhớ giờ thì ghi mốc tương đối ("trước khi ghi bản 2"). Hook W30 chỉ bắt dạng `HH:Mx`.
- **Chạy việc nặng CPU / Qdrant chồng lượt đo latency của B** (đầu giờ chiều 28/10, C tự khai ở review C80) ⇒ nay thành luật WORKFLOW §9.2 (W31). Trước việc nặng: xem handoff / hỏi A.
- **Tìm tên riêng trong kho phải dùng `-i`** — mẫu K004 phân biệt hoa thường sót 9 dòng "(Quận …)" ở tiêu đề / bảng (C79 bản 3).
- **`grep_kb.sh` không nhận cờ gộp** (`-ril`) ⇒ viết cờ rời (`-r -i -l`).
- **Gõ sha từ trí nhớ** (gửi B một sha sai cho file câu âm) ⇒ luôn `sha256sum | cut -c1-12` ngay trước khi viết tin.
- **Nối lệnh bằng `;` sau một assert Python** ⇒ assert lỗi mà script sau vẫn chạy ⇒ dòng STATUS bị ghi đôi. Dùng `&&`, hoặc gộp vào một script.
- **Pilot vượt ước tiền 70 %** (C73) ⇒ dừng theo luật, A duyệt chạy tiếp. Luật dừng-khi-vượt-ước có tác dụng.
- **Kiểm trùng dữ kiện Golden phải đọc cả đáp án mẫu**, không chỉ câu hỏi (C84: câu thay S25 lần đầu khác chữ câu hỏi Golden, nhưng trùng đúng một ý trong đáp án mẫu của câu đó).
- **Kiểm đối chứng "chép nguyên văn"** phải bỏ `*` / `_` của Markdown trước khi so với ngữ cảnh, và so với **đúng khối `[Nguồn n]`** được dẫn (C85).

## 7. File private C tạo phiên 28/10 (không commit)

`data/sua_kho_2026-10-27/{review_c75_tools/, review_c76_tools/, dot2/}`; `data/loi_nang_2026-10-28/negatives_c_confirm.json`; `data/loi_nang_2026-10-28/an_toan/{c_check.md, c_review/before.sha}`;
`data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming.md`; `data/streaming_ttft_2026-10-28/`; `data/phase_8_2/b1/merge_2810/c_review/`; `data/phase_8_2/b3_c_review/`;
`gửi chatgpt/2026-10-28/tìm thông tin/streaming_rag_citation_2026_10_28.md`.
