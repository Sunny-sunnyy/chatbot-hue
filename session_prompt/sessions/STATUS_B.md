# STATUS B — KẾT PHIÊN 27/10/2026 chiều (mở 13:4x; ghi 15:31 27/10/2026 `date`)

Terminal: `hue-rag-2d` (A = `hue-rag-51`, C = `hue-rag-86`) · Agent: Claude Opus 5.5 · Vai: thực thi; User 27/10 chiều: việc A giao = "làm đi".
Mã việc = mã A giao (B71…B76). Phiên sáng 27/10 (B53–B70): `git show 473f61e:session_prompt/sessions/STATUS_B.md`.

## Đang làm
- **Không.** Không việc dở.

## Đang khai báo sửa
- **Không.** Không worktree, server, lượt paid hay file tạm nào của B (`/tmp/b71_*`, `/tmp/b73_*`, `/tmp/b74_*` đã xóa; worktree `/tmp/b71_b1` đã gỡ).
  Các `/tmp/b_*` còn trên máy (`b_cd`, `b_fix`, `b_kho`, `b_ui`…) **không phải của B** (session dự án khác) — không đụng.

## Nhánh của B

| Nhánh | Commit | Trạng thái |
|---|---|---|
| `p82-b1` | `c3d5607` (= origin) | context 10 + NFC, **trên `main` `576f84e`** (B71, C review ready 0/0/2). **Chờ B0** rồi A merge |
| `p82-k1`, `p82-k3`, `p82-k3b` | như phiên sáng | hồ sơ, không merge |

## Vừa xong (phiên 27/10 chiều)

| Mã | Việc ⇒ kết quả | File / commit |
|---|---|---|
| B71 | rebase `p82-b1` lên `576f84e`: không xung đột, file B1 giống byte; test 50 passed (= main + 1 NFC; 1 failed + 1 error cần key); T1 giống byte `cefb2d1ad609`; cổng 8013 context 10 (2 câu, `chat_metrics` +2, `n_context_sources` 10); force-push lease `811d25d` | `phase_8_2_b1_rebase2_implementation.md` (nhánh); C review ready 0/0/2 |
| B72 | plan B3 (mốc cuối, câu kín) — **không mở câu kín**; bản 1 `9d60b16b63da` ⇒ C 0/2/4 ⇒ bản 2 theo quyết định A (500 citation chấm 1; B khớp số dòng 3 câu A thấy) ⇒ **A duyệt `27e75be5ed44`** | `phase_8_2_b3_plan.md` (`962c386`) |
| (C64) | review `dense_ms` làm tròn ⇒ ready 0/0/0 | `c64_dense_ms_review.md` |
| B73 | soạn đợt sửa kho (7 sub-agent, chỉ đọc kho): 53 mục ⇒ 41 diff + 12 chuyển nhóm; 16 câu hỏi User; 78 mục tra ngoài; đề xuất loại file inventory (33 đoạn). C66 ⇒ B sửa K011 / K048 / K049 ⇒ ready (giữ 40, K091 có điều kiện) | `data/sua_kho_2026-10-27/` (README) |
| B74 | (1) review đề xuất nhãn 3 câu test C64 ⇒ ready 0/0/1 (m-1: câu 138 chỉ gắn trích dẫn nói thẳng ý so sánh); (2) 11 diff tên phường sót (14 edit, dựng sau 41 edit) — C67 ready | `c64_de_xuat_nhan_test_review.md`; `data/sua_kho_2026-10-27/diffs_them/` |
| B75 | gold v3 = v2 + 130, 138 (`3b1117cf59e9`); v2 / v1 sha không đổi; `GOLD_PATH` → v3; +1 test luật đếm (thử ngược bắt đúng); test B1 7→9, K3b-m 10→11, dev không đổi; C ready 0/0/2 (sửa chữ) | `fa192f8`, `gold_v3_implementation.md` |
| B76 | yêu cầu ChatGPT tra 78 mục (chỉ câu ngắn, có file:dòng, phần đã biết 23/10) — **User tự gửi** | `gửi chatgpt/2026-10-27/tìm thông tin/tra_ngoai_kho_2026_10_27.md` (`c5a9198d81d8`) |

## Tiền paid phiên chiều (B)
- **≈ 0,000325 USD** (token trong log `chat_metrics` của 2 câu cổng B71: vào 2.232 × 0,1 / 1M + ra 204 × 0,5 / 1M). Không lượt paid nào khác.
- Quota Claude (không USD): 7 sub-agent B73 ≈ 0,68 triệu token.

## Đã học / bẫy gặp (phiên chiều)
- **Sự cố B73 — sub-agent đọc ngoài phạm vi (ghi 14:30 27/10/2026, báo A ngay):** sub-agent s7 chạy `grep -rn` trên cả `knowledge-base-hue/foods/` ⇒ đọc nhầm
  `foods/evaluation/` (Golden Foods cũ, không phải câu kín). **Nguyên nhân:** brief cấm đọc `evaluation/` và đưa `grep_kb.sh` nhưng **không cấm `grep -r` thẳng
  vào kho** (luật bằng lời, không rào). **Cách tránh:** brief sub-agent động vào kho ghi "chỉ grep bằng `grep_kb.sh`; cấm `grep -r` / `rg` / Glob trên
  `knowledge-base-hue/`"; cân nhắc rào bằng máy (A — vòng cải tiến). A quyết: edit s7 đánh dấu `[s7-golden]`, review chỉ theo căn cứ trong kho (C66 giữ cả 9).
- Kết quả sub-agent là dữ liệu: B kiểm máy (chuỗi cũ khớp 1 lần, không chồng) + đọc mẫu; C66 vẫn bắt 3 lỗi B không bắt (K011 hướng ngược, K048 / K049 làm mất thông tin)
  ⇒ đọc mẫu nên gồm cả mục "đổi lời" (dễ mất ý), không chỉ mục số.
- **Giờ ước lọt vào file** (2 lần ở B73: "14:4x", "14:3x" ghi trước khi chạy `date`) — B tự bắt, sửa bằng `date`. Lại đúng bẫy WORKFLOW §6: ghi giờ chỉ sau `date`.
- Một lần sửa STATUS_B bằng `python3` hệ thống (13:52) thay vì `uv run python` — không phải code / bằng chứng, nhưng lệch §10; từ đó dùng `uv run python -I`.
- Log của worktree ghi ở `/tmp/<wt>/backend/logs/`, và pytest `test_api_chat.py` cũng ghi `chat_metrics` ⇒ đếm "dòng mới" lấy mốc ngay trước khi gửi câu (B71: mốc 5).
  Gỡ worktree xóa luôn log ⇒ **chép dòng `chat_metrics` vào `data/` trước khi gỡ** (C B71 m-1).
- Test `gold_coverage`: trích dẫn "không trúng" cùng file rơi vào nhánh đọc file tiêu đề (`source_text`) ⇒ test tự viết dùng file khác để không đọc đĩa.
- Bản chạy cũ `b1_*.jsonl` không có `context_chunk_ids` ⇒ dựng lại từ `top_chunk_ids[:context_sources]`; ghi rõ trong report (C B75 m-1).
- **Thử phá rào `scripts/grep_kb.sh` (W27, 4 vòng, ghi 15:59 27/10/2026):** B tìm 4 lối thoát lần lượt (mẫu trùng tên thư mục con; đường dẫn thừa; `-e` / `--regexp=` biến mẫu
  thành file; `--dir <file>` trong `evaluation/` / `meta/`) + 1 minor (`--include` thắng `--exclude='*sealed*'` theo luật GNU "cái sau thắng") ⇒ A sửa tới `77ac6ec`.
  **Bẫy:** shell tương tác có hàm `grep` gọi **ugrep** (không truyền vào script / shell con) ⇒ thử hành vi của script phải gọi `/usr/bin/grep` (GNU 3.11),
  không gọi `grep` trực tiếp (B lỡ một lần, chạy lại). Thử phá chỉ in đường dẫn / số đếm (`-l`, `-c`), không in nội dung.
- Từ trước (giữ): harness ghi từng dòng, bắt mọi lỗi lần gọi; từ chối ghi đè; tiền ước dùng token thật; không trừ hai số đo khác cách; in đúng phần tử làm cờ bật;
  API 500 cho mọi `CitationIntegrityError`; thử ngược test đặt lỗi ở nhánh thật chạy qua; `validate_gold.py` ghi đè `gold_draft`; `ss -ltn` trước khi chạy
  server; report public tả câu ở mức loại câu; worktree `uv run --project …` + gỡ symlink, push từ working tree chung; pytest liệt kê file; pilot 10 câu;
  **B đã thấy khóa X / Y của B0 ⇒ B không làm người tóm nhãn B0.**

## Việc dở / câu hỏi còn treo (khớp `CURRENT_HANDOFF.md` "Mục việc phiên sau", rà 16:46 27/10/2026)
- Việc dở của B: **không**.
- **Việc chờ của B phiên sau** (A giao sau khi User cấp quyền):
  1. **Khi chờ B0:** viết plan đo "trước ↔ sau" đợt sửa kho (spec `937cf8969810` §5 bước 0 + §6; khuôn `run-experiment` §1 + "Căn cứ để review"; harness
     ghi từng dòng; A/A = 2 nguồn B1 ↔ G2.1a) ⇒ C review ⇒ A duyệt sha. **Chưa chạy** (bộ "trước" chạy trên chatbot sau merge B1).
  2. **Review plan C** đo "thời gian tới chữ đầu tiên" (streaming, ~10 câu, ≈ 0,002 USD khi chạy) ⇒ A duyệt sha.
  3. **Sau B0:** nếu `main` xung đột với `p82-b1` `c3d5607` thì B rebase lại (A merge; cổng ổn định context 10).
  4. **B3 — người chạy B** theo plan `27e75be5ed44` khi User quyết mở câu kín: khớp 3 câu A đã thấy từ `sealed_user_feedback_private.md` ⇒ `a_seen_lines.json`
     (không đủ 3 ⇒ chỉ S36); report tách riêng số câu 500 kiểu "validator v1 không nhận `[Nguồn n]`" mỗi bên (C65); C kiểm (giữ mù).
  5. **Đợt sửa kho (sau đóng 8.2):** B chạy bước 0 (bộ "trước" 176 câu) + bước 1–6 (sao lưu, **áp sửa §5 bước 2** bằng thay chuỗi từ `edits/*.jsonl` rồi
     `diffs_them/` — K091 không áp; loại file danh mục; chia đoạn thử; build lại tại chỗ; kiểm sau build) — làm liền bước 2–6; C review diff + kiểm chunk / build.
     Trần 0,15 USD. Trích dẫn kho: tìm **chỉ** bằng `scripts/grep_kb.sh`.
- Chờ User (qua A): B0; quyết mở câu kín (B3); 16 câu `data/sua_kho_2026-10-27/cau_hoi_user.md` (chưa trả lời ⇒ đợt 2); gửi ChatGPT 78 mục (B76) — kết quả
  ⇒ `gửi chatgpt/2026-10-27/kết quả nghiên cứu/` ⇒ WebFetch đối chiếu URL trước khi áp (đợt 2).
- Ghi chú cho A: dòng đầu spec sửa kho vẫn ghi "NHÁP, chờ User duyệt" dù User đã duyệt sha `937cf8969810` (sửa chữ = sha mới ⇒ ghi trạng thái duyệt ở
  handoff là đủ, hoặc A quyết). K3b-m vẫn gác (gold v3 không đổi kết luận đã đóng).
