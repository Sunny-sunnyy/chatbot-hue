# STATUS B — phiên 27/10 chiều (mở 13:4x; cập nhật 13:52 27/10/2026)

Terminal: `hue-rag-2d` (A = `hue-rag-51`, C = `hue-rag-86`) · Agent: Claude Opus 5.5 · Vai: thực thi; User 27/10 chiều: việc A giao = "làm đi".

## Đang làm (phiên 27/10 chiều)
- **B71 — chờ review C** (A giao 13:50; xong 13:59): `p82-b1` rebase lên `main` `576f84e`, không xung đột ⇒ `2fa6f16`, `4653013` + report `c3d5607`;
  `git push --force-with-lease=p82-b1:811d25d` ⇒ `origin/p82-b1` = `c3d5607`. Không merge.
  Kết quả: file B1 giống byte nhánh cũ; 6 file test 50 passed (main 49, +1 NFC; cùng 1 failed + 1 error cần key); T1 giống byte `cefb2d1ad609` (158); T5 10 / 10;
  cổng 8013: `/` 200, `/health` 5 / 5, câu trong kho 200 + `[n]` + `n_context_sources` 10, câu ngoài kho từ chối, `chat_metrics` +2, grep câu hỏi = 0.
  Report `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_rebase2_implementation.md` (trên nhánh). Dữ liệu `data/phase_8_2/b1/rebase_2710/`.
- Tiền phiên chiều: **≈ 0,000325 USD** (token log 2 câu cổng).

## Đang khai báo sửa (phiên 27/10 chiều)
- **Không** (worktree `/tmp/b71_b1` đã gỡ, `/tmp/b71_*` đã xóa, server tắt).

## Đã học / bẫy gặp (phiên 27/10 chiều)
- Log của worktree ghi ở `/tmp/<wt>/backend/logs/application.log` và pytest `test_api_chat.py` cũng ghi `chat_metrics` vào đó ⇒ đếm "dòng mới" phải lấy mốc
  ngay trước khi gửi câu (B71: mốc 5 do pytest, không phải 0).

---

# (Phiên trước) KẾT PHIÊN 2026-10-27 13:25 (mở 08:4x)

Terminal: `hue-rag-31` (A = `hue-rag-5f`, C = `hue-rag-5b`) · Agent: Claude Opus 5.5 · Vai: thực thi; việc A giao = User nói "làm đi".
Mã việc là **mã A giao** (B53…B70). Phiên tối 26/10: `git show c81e45e:session_prompt/sessions/STATUS_B.md`.

## Đang làm
- **Không.** Không việc dở.

## Đang khai báo sửa
- **Không.**
- Không worktree, server, lượt paid hay file tạm nào của B. Các `/tmp/b_*` còn trên máy (`b_cd`, `b_fix`, `b_fix2`, `b_grade`, `b_khach`, `b_kn`, `b_pay`,
  `b_ui`) thuộc session của **dự án khác**, B không đụng.

## Nhánh của B (đều = origin)

| Nhánh | Commit | Trạng thái |
|---|---|---|
| `p82-b1` | `811d25d` | context 10 + NFC; **chờ B0** rồi merge. B63 thử rebase lên `main` sạch |
| `p82-k1` | `870a5d5` | hồ sơ, không merge |
| `p82-k3` | `80e7329` | hồ sơ |
| `p82-k3b` | `4c85195` | hồ sơ (K3b + khâu trả lời K3b-m) |
| `gold-v2` | `b972b55` | **đã merge `main` `a819789`** (C61 ready) |

`c59-log` của C: B review (B70), đã merge `main` `5100b90`.

## Vừa xong (phiên 27/10)

| Mã | Việc ⇒ kết quả | File / commit |
|---|---|---|
| B53 | review report R2 ⇒ ready 0/0/2; R2 kém hơn (sàn OOS) | `phase_8_2_r2_review.md` |
| B54 | chạy K3 (luna xếp 30 đoạn) ⇒ kém hơn: lỗi đầu ra 1/40; theo dõi 9/0 | `p82-k3`, `phase_8_2_k3_implementation.md` |
| B55, B57 | review plan R1 ⇒ M-1 ("no citation" = sàn 500) ⇒ bản 2 ready | `phase_8_2_r1_plan_review.md` |
| B56 | plan K3b (2 bản) + harness + chạy ⇒ n kém hơn (chữ thừa sau JSON); m tầng tìm tốt hơn (tạm) 22→31/40, 9/0 ổn định, test 3/0 | `p82-k3b`, `phase_8_2_k3b_{plan,implementation}.md` |
| B58 | review report R1 ⇒ ready 0/0/1 (regex tách câu) | `phase_8_2_r1_review.md` |
| B59 | phụ lục khâu trả lời K3b-m (3 bản) + chạy. Bản 2 dừng ở sàn câu 120 (nhãn thiếu) ⇒ User: 120 về theo dõi. Bản 3: **kém hơn theo luật T3** (5 câu Completeness tụt > 4); chỉ báo: Completeness +0,22, Accuracy +0,25, từ chối nhầm 7→2 | `phase_8_2_k3b_m_answer_{plan,implementation}.md` |
| B61 | quét nhãn đoạn đúng ⇒ lặp nguyên văn 1/55; kết luận tầng tìm không đổi | `data/phase_8_2/k3b/gold_scan/` |
| B62 | `BAO_CAO_TIM_KIEM.md` bản 8 | `2936165` |
| B63 | thử rebase B1 lên `main` ⇒ không xung đột; 68 passed / 1 failed (thiếu key, giống main); T1 giống byte | tin nhắn |
| B64 | review tài liệu đóng đợt của A ⇒ cận trên tiền sai (gốc là ước của B) ⇒ sửa | report K3b `4c85195` |
| B65 | latency API thật main ↔ B1 ⇒ không khác (p50 3,1–3,6 s, p95 5,7–6,4 s); sửa theo C57 | `b65_latency_dau_cuoi.md` (`a94ebc5`) |
| B66 | kiểm đề xuất sửa nhãn C56 ⇒ đồng ý cả 3 | tin nhắn |
| B67 | review C58 (latency theo khâu) ⇒ số khớp; nhãn "chứng minh" ⇒ "giải thích" | tin nhắn |
| B68 | review plan C59 + vòng 2 ⇒ M-1 409, M-2 một điểm ghi ⇒ bản 2 ready | `c59_log_token_plan_review.md` |
| B69 | gold v2 + đếm tiêu đề mục ⇒ `gold_v2.jsonl` `2f5a347a71ff` (`gold_draft` `bab707b9ab22` giữ); B1 22→24, K3b-m 31→33, 9/0 giữ | `gold-v2` → `a819789`, `gold_v2_implementation.md` |
| B70 | review C60 (log token) ⇒ ready 0/0/2 | `c59_log_token_review.md` (`8c763dc`) |

## Tiền paid phiên 27/10 (B)

- **Log:** K3 0,0251129 + K3b 0,0592176 + khâu trả lời K3b-m 0,0749297 = **0,1592602 USD**.
- **Ước:** lượt K3b-n mất usage ≈ 0,0087 (cận trên 0,0142); B65 ≈ 0,0155 (API chưa ghi usage lúc đó).
- ⇒ **tổng ≈ 0,184 USD (≤ 0,190)**.

## Đã học / bẫy gặp

- Harness gọi API trả phí: ghi từng dòng ngay, bắt mọi lỗi của một lần gọi. `responses.parse` có thể ném `pydantic.ValidationError` (chữ thừa sau
  JSON strict, `reasoning none`).
- Tiền ước dùng token thật của đúng câu bị ảnh hưởng (0,0074 → 0,0087). Số trong lời thường đếm lại từ bảng ("Ba" → "Bốn").
- Không trừ hai số đo bằng hai cách / hai bộ câu khác nhau (B65: "+3 s" sai ⇒ tách trong cùng lượt: chọn đoạn ≈ 4,6 s).
- In bằng chứng cho một cờ: in đúng phần tử làm cờ bật (B61 sai ở câu 156).
- Xét dạng lỗi cụ thể, không chỉ số đếm. API trả 500 cho **mọi** `CitationIntegrityError` (`chat.py`). Sàn đặt trên nhãn: đọc nội dung kho trước (câu 120).
- Regex tách câu giữ `[n]` sau dấu chấm, kể cả `. [1]` / `[nguồn n]`.
- Thử ngược một test: đặt lỗi ở chỗ nhánh test **thật sự chạy qua** (B70: chèn sau `build` thì nhánh ngân sách không tới).
- `validate_gold.py` ghi đè `gold_draft.jsonl` (A đã ghi bẫy `a872c59`). Đọc script dữ liệu trước khi chạy.
- Cổng 8011 có thể bị tiến trình khác chiếm ⇒ `ss -ltn` trước; file tracked không ghi tên tiến trình đó. Report public tả câu ở mức loại câu (W26).
- Từ trước (giữ): harness từ chối ghi đè; trần kiểm trên đúng mốc; người kiểm ghi sha lúc đọc; worktree `uv run --project /home/minhhieu/hue_rag` +
  gỡ symlink, push từ working tree chung, lệnh push để riêng; mọi Python `uv run`; pytest liệt kê file; pilot 10 câu; giờ bằng `date`; **B đã thấy khóa
  X / Y của B0 ⇒ B không làm người tóm nhãn B0.**

## Việc dở / câu hỏi cho A / User

- Việc dở của B: **không**.
- Cho User qua A:
  - (1) B0 vẫn chặn merge B1. Merge thật cần cổng ổn định có key.
  - (2) Hướng K3b-m: tầng tìm tốt rõ nhưng khâu trả lời kém hơn theo luật T3, giá ≈ +4,6 s / 3,8× tiền. Muốn đi tiếp cần luật nhận riêng cho biến thể
    đổi context, hoặc bản nhanh (K3c) — User quyết.
- Cho A:
  - (3) Test khóa danh sách trắng C59 chỉ phủ trường gán trước điểm lỗi ngân sách (B70 m-1) ⇒ ghi hồ sơ / Project_Status §8.
  - (4) Từ trước: mâu thuẫn kho Hải Vân Quan (sửa khi build lại index); dense local mới ngoài danh sách duyệt.
