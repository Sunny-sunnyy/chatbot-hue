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
