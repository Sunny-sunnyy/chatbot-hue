# Review sớm: Phase 9 T4 — lịch trình từ câu gõ tự do, phần code (nhánh `p9-t4-lich` `9780d93`, E)

Decision: **changes_requested (nhẹ)** — 0 blocker · 1 major (chỉ cần thêm một dòng tiêu chí đếm bằng code, 0 USD); một vòng, chỉ blocker / major (A 09/11)
Người kiểm: C (Claude Code, `hue-rag-6a`)
Date: 21:11 09/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-09-phase-9-t4-lich-trinh-plan.md` bản 2 (A duyệt `29708ef92e30`)
Implementation report: chưa có (review sớm phần code, trước rebase + lượt có phí)

## 1. Phạm vi đã review

Exact diff `main...origin/p9-t4-lich` (3 file: `lich_trinh.py` `chot_so_ngay` + câu cố định, `assistant.py` log (c) + nối câu (b), `test_b5_lich_trinh.py`); plan bản 2 §1, §4, §5.
**Lệch tài liệu:** file plan trên ổ hiện có sha `5a22b51fe49c`, khác sha A duyệt (`29708ef92e30`, ghi là tính **trước** khi thêm dòng "A duyệt") — file chưa từng commit nên không so được
bản đã duyệt; C review theo bản hiện tại. A xác nhận khác biệt chỉ là dòng 3.

## 2. Findings

Đối chiếu plan: (a) `chot_so_ngay` thứ tự mới nút ⇒ số dò (đúng một giá trị) ⇒ tham số model ⇒ hỏi — **khớp**, nhánh "model gửi số khác ⇒ hỏi" đã gỡ; (c) log `so_ngay_model` +
`so_ngay_do` — **khớp**, an toàn dữ liệu: `so_ngay` của model là kiểu liệt kê `lt.SoNgay` ("1" / "2" / "3" / "4+"), số dò là chữ số ⇒ log không có chữ tự do; (b) câu cố định nối
một lần sau lời lịch tối thiểu khi có `sau_lich`, đi qua kiểm cuối + kiểm citation — **khớp** (test: `lich_kiem == []`, `citation_error is None`, stream `delta` = `answer`).

### M-1 (major) — Câu cố định (b) có thể nói sai khi người dùng **không** hỏi kèm, mà plan không có số đo cho trường hợp đó

- **Vị trí:** `assistant.py` `_finish_generated` nhánh có lịch — điều kiện chỉ là `any(t.get("sau_lich") for t in trace.tools)`; plan §4 dòng **E20**.
- **Bằng chứng:** `sau_lich` đánh dấu **mọi** lần model gọi `tim_kho` sau khi có lịch (`assistant.py` `tool_for_turn`), không riêng lần tìm cho phần hỏi kèm. Model có thể tìm thêm
  vì chính lịch (vd muốn thêm thông tin một điểm) rồi từ chối ⇒ code nối "Phần bạn hỏi thêm ngoài lịch hiện chưa có…" cho người dùng **không hỏi thêm gì** — một câu sai sự thật
  (lỗi "nói chắc sai" xếp thứ 2, `Project_Status.md` §1). Tiêu chí E20 hiện chỉ đếm chiều "câu hỏi kèm ⇒ có câu cố định", không đếm chiều ngược.
- **Tiêu chí đóng (0 USD, không đổi code):** thêm vào plan §4 dòng E20: "câu xin lịch **không** hỏi kèm (5 câu E20 không hỏi kèm + câu lịch của B5 / E19) có câu cố định (b): **0**"
  (đếm bằng code trên chữ cuối, nhãn có / không hỏi kèm ghi trước lượt có phí). > 0 ⇒ âm cho (b) — khi đó mới bàn điều kiện hẹp hơn (không đoán trước).

Không thấy blocker. Không thấy over-engineering (3 file, +42 / −11).

## 3. Cách người kiểm chạy lại thật

Worktree tách `/tmp/c_t4rv` ở `9780d93` (symlink `data/`, `knowledge-base-hue/`): `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_b5_lich_trinh.py
tests/test_b5b_thoi_tiet.py -q`; Q1 cờ `lich_trinh` tắt: `capture_all.py` ⇒ `data/phase_9/t4/q1_c_review_tat.jsonl`, `cmp` với `data/phase_9/t3_bang_ve_gio/q1_a/main_5c982a0.jsonl`
(dùng lại được: `git diff 5c982a0 3d2d420 -- backend` rỗng, `3d2d420` = điểm tách nhánh).

## 4. Kết quả quan sát

331 passed (30 giây). **Q1 cờ tắt 228 / 228 giống byte**. 0 USD.

## 5. Giới hạn hoặc phần chưa chạy

Không kiểm đường #6 cho (b) (plan §5 bước 2 ghi "cả 3 đường"; test có `/api/chat` + stream — phần song song của #6 chạy chính `answer_turn_stream` nên rủi ro thấp, ghi để E thêm nếu
rẻ). Chuỗi `tim_kho` + `lich_trinh` + `yeu_cau_tra_web` (T2) chưa có test `max_turns` — kiểm khi T4 rebase lên `main` có T2. Lượt có phí: NOT RUN (chờ G + T2).

## 6. Decision và bước tiếp theo

E (hoặc A) thêm một dòng tiêu chí M-1 vào plan trước lượt có phí; code không phải sửa. Sau rebase: C xem delta + kết quả đo như T2.
