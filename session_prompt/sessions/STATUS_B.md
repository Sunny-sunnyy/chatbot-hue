# STATUS B — PHIÊN 27/10/2026 (mở 08:4x; terminal `hue-rag-31`; A = `hue-rag-5f`, C = `hue-rag-5b`)

Agent: Claude Opus 5.5 · Vai: thực thi · User 27/10: B làm việc trực tiếp với A; việc A giao = User nói "làm đi".
Mã việc dưới đây là **mã A giao** (B53…B69). Bản STATUS trước 13:1x từng dùng số riêng (B70–B75) — đã bỏ (A nhắc 13:0x).
Bản phiên tối 26/10: `git show c81e45e:session_prompt/sessions/STATUS_B.md`.

## Trạng thái hiện tại (cập nhật 13:1x 27/10/2026)

- **Việc dở: không.** B70 xong 13:20 27/10/2026 (review C60 = ready, file `c59_log_token_review.md` sha `86d2bce6423c`, A commit); B69 chờ C review. **File đang khai báo sửa: không.**
- Không worktree `/tmp/b_*` nào của B, không server, không lượt paid đang chạy. Các `/tmp/b_*` khác trên máy (`b_vong1..4`, `b_moc*`, …) không phải
  của B phiên này, B không đụng.
- **Nhánh của B** (đều = origin, **không merge**):
  - `p82-b1` `811d25d`: B1 context 10 + NFC, merge sau B0; B63 thử rebase lên `main` sạch.
  - `p82-k1` `870a5d5`: K1, hồ sơ.
  - `p82-k3` `80e7329`: K3, hồ sơ.
  - `p82-k3b` `4c85195`: K3b + phụ lục khâu trả lời, hồ sơ.
  - `gold-v2` `b972b55`: B69, **chờ C review**.
- **Tiền paid phiên 27/10 của B:**
  - log 0,1592602 USD (K3 0,0251129 + K3b 0,0592176 + phụ lục khâu trả lời 0,0749297);
  - ước: lượt K3b-n mất usage ≈ 0,0087 (cận trên ≈ 0,0142) + B65 ≈ 0,0155 (API không trả usage);
  - ⇒ **≈ 0,184 (≤ 0,190) USD**.

## Việc phiên 27/10 (mã A giao)

| Mã | Việc | Kết quả | File / sha |
|---|---|---|---|
| B53 | review report R2 (C) | ready 0/0/2 minor; R2 kém hơn (sàn OOS) | `phase_8_2_r2_review.md` |
| B54 | chạy K3 (luna xếp 30 đoạn) | **kém hơn**: lỗi đầu ra 1/40; theo dõi 9/0; 0,0251 USD | `p82-k3`, `phase_8_2_k3_implementation.md` |
| B55 / B57 | review plan R1 (C) + vòng 2 | changes_requested (M-1 "no citation" = sàn 500) ⇒ bản 2 ready | `phase_8_2_r1_plan_review.md` |
| B56 + chạy | plan K3b (2 bản) + harness + chạy | K3b-n **kém hơn** (chữ thừa sau JSON); K3b-m tầng tìm **tốt hơn (tạm)** 22→31/40, 9/0 ổn định, test 3/0 | `p82-k3b`, `phase_8_2_k3b_{plan,implementation}.md` |
| B58 | review report R1 (C) | ready 0/0/1 (regex tách câu) | `phase_8_2_r1_review.md` |
| B59 | phụ lục khâu trả lời K3b-m (3 bản) + chạy | bản 2 dừng ở sàn câu 120 (nhãn thiếu) ⇒ User chọn 120 theo dõi ⇒ bản 3: **kém hơn theo luật T3** (5 câu tụt > 4); chỉ báo tốt lên | `phase_8_2_k3b_m_answer_{plan,implementation}.md` |
| B61 | quét nhãn đoạn đúng | lặp nguyên văn 1/55; kết luận tầng tìm không đổi | `data/phase_8_2/k3b/gold_scan/` |
| B62 | BAO_CAO_TIM_KIEM bản 8 | A review + commit `2936165` | `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md` |
| B63 | thử rebase B1 lên `main` | không xung đột; 68 passed / 1 failed (thiếu key, giống main); T1 giống byte | (STATUS này) |
| B64 | review tài liệu đóng đợt (A) | 1 lỗi số (cận trên tiền) + 3 minor ⇒ A sửa ⇒ ready; lỗi gốc ước tiền của B ⇒ sửa report `4c85195` | tin nhắn |
| B65 | latency API thật (main ↔ B1) | không khác; p50 ~3,1–3,6 s, p95 ~5,7–6,4 s; sửa theo C57 | `b65_latency_dau_cuoi.md` (`a94ebc5`) |
| B66 | kiểm đề xuất sửa nhãn C56 | đồng ý cả 3; nhận định B61 "156 báo nhầm" của B là sai | tin nhắn |
| B67 | review C58 (latency theo khâu) | số khớp; sửa nhãn "đã chứng minh" ⇒ C sửa | tin nhắn |
| B68 | review plan C59 (log token) + vòng 2 | changes_requested (M-1 409, M-2 một điểm ghi) ⇒ bản 2 ready | `c59_log_token_plan_review.md` (`2ddd65d`) |
| B69 | gold v2 + đếm tiêu đề mục | `gold_v2.jsonl` `2f5a347a71ff` (gold_draft `bab707b9ab22` giữ); B1 22→24, K3b-m 31→33, 9/0 giữ | `gold-v2` `b972b55`, `gold_v2_implementation.md` ⇒ **C review** |
| B70 | review C60 (log token `/api/chat`, `c59-log` `cc70124`) | ready 0/0/2 minor; test 32/4 = mốc 31/4 + 1; log thật 15 trường, không nội dung; thử ngược whitelist đỏ khi đặt đúng chỗ | `c59_log_token_review.md` |

## Phiên sau B làm gì đầu tiên

Nguồn sự thật: `CURRENT_HANDOFF.md`. Từ phía B:
- Nếu C review `gold-v2` có finding, B sửa trên nhánh đó.
- Script tính lại bảng §4 của report gold v2 nay ở `data/phase_8_1/tools/recount_gold_v2.py` (sha `aad629632518`). Report trên nhánh ghi
  `/tmp/b75_recount.py`, file đó đã xóa ⇒ nếu C cần, B sửa đường dẫn ở commit tiếp.

## Câu hỏi còn treo (cho A / User)

- `data/phase_8_1/tools/validate_gold.py` **không nhận đầu vào và ghi đè `gold_draft.jsonl`** (file G0.6 khóa) ⇒ đề xuất thêm tham số vào / ra, hoặc cảnh báo
  ở đầu file (B69 không chạy nó).
- B0 (User đọc cặp mù) chặn merge B1. Merge thật vẫn cần cổng ổn định có key.
- Từ trước: dense local mới ngoài danh sách duyệt; mâu thuẫn kho Hải Vân Quan — sửa khi build lại index.

## Đã học / bẫy gặp

- **27/10:**
  - Harness gọi API trả phí phải **ghi từng dòng ngay** và bắt mọi lỗi của một lần gọi. `responses.parse` có thể ném `pydantic.ValidationError` (chữ
    thừa sau JSON strict, ở `reasoning none`). Bản đầu harness K3b chỉ bắt `OpenAIError` + ghi ở cuối lượt ⇒ mất usage.
  - **Tiền ước dùng token thật của đúng các câu bị ảnh hưởng**, không dùng giá TB của lượt khác (0,0074 → 0,0087).
  - **Số trong lời thường đếm lại từ bảng**, không gõ tay ("Ba trong 5" → 4).
  - **Không trừ hai số đo bằng hai cách / hai bộ câu khác nhau** (B65 "thêm ≈ 3 s" → tách trong cùng lượt: ≈ 4,6 s).
  - Khi in "bằng chứng" cho một cờ, in **đúng phần tử làm cờ bật** (B61 in chunk khớp nhiều từ nhất ⇒ kết luận sai ở câu 156).
  - Kiểm dạng lỗi cụ thể của biến thể cũ, không chỉ số đếm (B55: 2 lỗi citation `none` đều là "no citation" = 500). API trả 500 cho **mọi**
    `CitationIntegrityError` (`chat.py:124–135`).
  - Regex tách câu phải giữ `[n]` sau dấu chấm, kể cả `. [1]` và `[nguồn n]` (bài học B58 + C53 m-4).
  - Script dữ liệu có thể ghi đè file khóa: đọc script trước khi chạy (`validate_gold.py`).
  - Cổng `8011` có thể bị tiến trình khác chiếm ⇒ kiểm `ss -ltn` trước; file tracked không ghi tên tiến trình đó.
  - Report public tả câu ở mức loại câu (W26), kể cả chuỗi mẫu trong test.
- **Từ 26/10 (giữ):** harness mới luôn từ chối ghi đè; giả định "trần" kiểm trên đúng mốc; người kiểm ghi sha ngay lúc đọc; worktree dùng
  `uv run --project /home/minhhieu/hue_rag`, gỡ symlink khi xong, push từ working tree chung; script ngoài `backend/` cần `PYTHONPATH=.`.
- **Từ 25/10 (giữ):** mọi Python bằng `uv run`; pytest liệt kê file; lệnh paid mới chạy thử không `--env-file` trước; giờ bằng `date`; đọc code
  trước khi khẳng định; pilot 10 câu cho lượt paid; chấm baseline cùng lượt mù; **B đã thấy khóa X / Y của B0 ⇒ B không làm người tóm nhãn B0.**
