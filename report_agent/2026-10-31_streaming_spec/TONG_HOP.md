# TỔNG HỢP đợt 2026-10-31 — spec streaming câu trả lời

Viết 12:42 31/10/2026; **cập nhật 13:35 01/11/2026 (A, phiên 01/11)**. Trạng thái: **streaming XONG, vào `main` (merge `a80e12d`)**; đợt còn mở cho tới khi User đóng Phase 8 (chờ B0). Cùng đợt 01/11: lượt đo cuối Phase 1–8, rà bảo mật đóng gói, `cost_usd` giá đủ.
Dữ liệu (private): `data/tinh_nang_moi_2026-10-27/` (nháp v2 / v3, C97, B99, B104, kết quả thô Codex review), kết quả ChatGPT `gửi chatgpt/2026-10-28/kết quả nghiên cứu/`.

## Mục tiêu
Chữ trả lời hiện dần thay vì chờ trắng (câu dài hôm nay p95 7,6 s > yêu cầu 5 s), giữ bảo đảm citation và lỗi tệ nhất User chốt 28/10 (sai cảnh báo an toàn).

## Quyết định theo giờ (giờ A ghi nhận bằng `date`)
- 10:23 — giao diện mới (React / Next…) bàn **sau Phase 8**, gộp nội dung AI FDE; spec này chỉ API + sửa tối thiểu `frontend/` JS thuần.
- 10:32–10:46 — A: lỗi trước luồng chọn cách (b) (endpoint thường, `StreamingResponse` tự dựng); ép `response.incomplete` bằng tham số thật không phải lỗi giả (≤ 0,001 USD).
- Trước 11:02 (giờ A không ghi lúc đó; trước B102 vòng 2) — A: không thêm chỗ nối chỉ dùng khi test (giao diện D3 (a), luồng đứt ⇒ giới hạn).
- 11:26 — **User chốt D1 = PA1** (chữ hiện ngay + tiến độ thật, kiểm citation cuối như hôm nay).
- 11:44 — **User chốt D2 = (a)**: sàn p50 ≤ 3 s / p95 ≤ 5 s cho "tới chữ trả lời đầu tiên trên trình duyệt"; tới đủ câu chỉ theo dõi.
- 11:48 — **User chốt D3 = phương án 1**: kiểm cuối hỏng ⇒ rút lại; lỗi / đứt giữa chừng ⇒ xóa hết; lời báo + "Thử lại". A đặt D5 = 1 % / tuần; không nút "Dừng".
- 11:52 — A: câu từ chối cùng sàn 3 / 5 s, đo tới lúc biết chắc là từ chối, báo riêng.

## Chuỗi việc + review
| Việc | Ai | Kết quả |
|---|---|---|
| B99 kiểm nguồn kết quả ChatGPT | B | 21 / 22 URL mở, 0 ý bị nguồn nói ngược, 3 ý "suy ra", #3314 đã sửa (A tự kiểm 2 ý) |
| C97 đối chiếu với code + nháp v2 | C | JSON `output_type` vẫn stream trên SDK đã cài; từ chối gần như luôn do model viết; FastAPI có sẵn SSE; 14 mục nháp cần sửa — B100: 1 major (generator SSE + lỗi trước `yield` ⇒ 200 thân rỗng, probe thật) ⇒ ready |
| C98 nháp v3 (D1 theo propose-options) | C | B102: 1 major (hứa test không tạo được bằng đường thật) ⇒ ready |
| C100 spec | C | B105: 1 major (anyio hủy mọi `await` trong `finally` khi ngắt ⇒ log trước mọi await + `CancelScope(shield=True)`) ⇒ ready; **Codex review một lần (W33)**: 2 minor mới (bắt riêng `CancelledError`; 422 trước handler không có dòng log) ⇒ bản 4 ready |
| Tra Codex "chữ đầu tiên" | A | không có chuẩn ngành; Nielsen 1 s; API công khai p50 vài trăm ms – ~1,1 s; Codex suy ra mục tiêu 1,5 / 3 s (A WebFetch kiểm 2 ý) |

Tiền: 0 USD paid (Codex theo gói tài khoản).

## Kết quả W33 (Codex review)
Dương nhỏ: 2 minor thật mà review Claude bỏ sót; không bắt được lỗi cần chạy thư viện (worktree không có `.venv`); 58 s, 14 lệnh đọc trong worktree, 0 lệnh ra ngoài.

## Còn mở / bước tiếp
1. User trả lời Q1 (A khuyên: sàn 3 / 5 s giữ + mục tiêu báo cáo 1,5 / 3 s) ⇒ A điền `TBD` ⇒ B kiểm phần đổi.
2. User duyệt sha bản cuối ⇒ commit ⇒ code S1 (gom lõi chung, T1 giống byte) ⇒ S2–S4; đo C1–C7 trên trình duyệt thật.
3. Giới hạn chính (spec §10): lỗi nghĩa không bắt ở phương án nào; giao diện D3 (a) + luồng đứt chưa kiểm bằng đường thật; nhánh 503 / 409 / 500 / 502 chỉ test logic.

## Phiên 01/11 (A ghi 13:35 01/11/2026)

**Quyết định (User):** quyền như 31/10 + A tự commit / push; Q1 sàn 3 / 5 s + mục tiêu báo cáo 1,5 / 3 s; duyệt spec bản 5 `00fb57ee01b2`; Golden 127 giữ nguyên; hội thoại nhiều lượt ⇒ Phase 9; câu nhiều nguồn ⇒ Phase 9 (sau Q3a);
plan đo cuối `ae8d42d520d4` (bộ kín agent 40 câu, A/A cùng ngày, Q3a trước, trần 0,20 USD); trần S4 riêng 0,03 USD; giữ PA1 + giữ sàn sau S4; CA1 hook pre-push; CA3 tra tài liệu Codex rồi rào; duyệt mẫu 10 câu kín;
vòng cải tiến 13: W36, W45, I8 cho thử, W44 không chọn. **User hỏi "có over-engineer không"** ⇒ A: có (S64) — streaming dừng sau review cả nhánh, minor không mở vòng.

| Việc | Ai | Kết quả | Hồ sơ |
|---|---|---|---|
| S1 lõi chung | B | T1 giống byte; review A ready (ca dò 200.000 chuỗi citation) | `s1_loi_chung_*` |
| S2 route stream SSE | B | review agent con ready, 2 minor; m-1 surrogate sửa `887cbc5` (0 / 16.000) | `s2_stream_route_*` |
| S3 giao diện + CSP / allowlist | B | review C: M-1 lọt `background` + `/static` thiếu CSP ⇒ sửa `716ba4d` ⇒ ready | `s3_giao_dien_*` |
| B108 `cost_usd` giá đủ | B | review A ready | `b108_cost_usd_*` |
| S4 đo trên trình duyệt | B | chữ đầu p50 1,23 / p95 2,61 s; đủ câu 1,73 / 3,81 s; lợi ~0,44 s (chạm D5 ⇒ User giữ PA1) | `s4_do_d2_implementation.md` |
| Review cả nhánh (a1) | agent con | ready, 6 minor ghi giới hạn | `streaming_final_branch_review.md` |
| Rà bảo mật C106 | C + agent con | 11 rủi ro, 0 chặn; CA1 / CA3 rào (A, review B 2 vòng) | `c106_*`, `a_governance_ca1_ca3_review.md` |
| Plan + runbook đo cuối | C; review B | plan 3 vòng ⇒ duyệt; runbook 2 vòng | `c103_plan_review.md`, `c108_runbook_review.md` |
| Lượt đo cuối | C (§1–§5), B (§6–§8) | **mọi sàn đạt**; Golden không làm hỏng (2 câu tụt / ≤ 5); bộ kín 0 / 6 ngoài kho, Đủ 4,18 ↔ Golden 4,58 (câu được trả lời 4,60 ↔ 4,82 ⇒ số dev lạc quan thật); ≈ 0,139 USD | `do_cuoi_*`, `do_cuoi_review.md` |
| Báo cáo so sánh phương án | C (6 agent con) + 2 review | đăng `bao_cao_he_thong/BAO_CAO_SO_SANH_PHUONG_AN.md` | `data/so_sanh_phuong_an/` |

**Giới hạn khi đóng streaming (a6):** trường log `delta_matches_final` thêm ngoài spec §4.6 (A quyết giữ); lỗi hiếm ngoài SDK chưa huỷ lần gọi model; giao diện hiện lời lỗi trình duyệt khi đứt mạng; route stream ghi bản ghi bằng
chứng nửa chừng; rút lại / luồng đứt chỉ kiểm bằng phát lại; một lần đo 38 câu; giao diện JS thuần sẽ làm lại (`yeu_cau_cho_giao_dien_moi.md`).
**Tiền phiên 01/11:** ≈ 0,055 (B) + ≈ 0,095 (C, gồm §4–§5) + agent con của A ≈ 0,001 ⇒ **≈ 0,15 USD** / trần phiên 1 USD.
