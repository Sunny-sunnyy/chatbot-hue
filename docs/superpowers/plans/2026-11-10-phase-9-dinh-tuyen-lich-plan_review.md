# Review plan (vòng 1): câu lịch / ngày âm chung đi trợ lý bằng lời dặn định tuyến

Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-4f`) · 10/11/2026 · việc A giao (`CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11", dòng B thứ ba: quy trình đủ, review plan ≤ 2 vòng).
Đối tượng: `docs/superpowers/plans/2026-11-10-phase-9-dinh-tuyen-lich-plan.md` bản 1, sha256 **`71b65873ef26`** (B, chưa commit). Đối chiếu: mục việc trong handoff,
spec Phase 9 §12.3 (sàn), `backend/llm/assistant.py` (cổng web), `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md`. Không chạy gì (0 USD).

## Kết luận

**`changes_requested`** — 0 blocker · **2 major** · 3 minor. Hướng đúng (đổi một chuỗi, đo tầng 1 chỉ lần gọi định tuyến, chỉ sinh câu đổi tuyến, có bộ giữ mù do người khác viết,
≤ 2 vòng chỉnh). Lập luận §2 đứng: đường sau tuyến không đổi ⇒ câu giữ tuyến cùng phân phối `main` (đúng với mọi đường, kể cả song song #6 — chỉ đọc `trace.route`).

## Findings

**M-1 (major) · cách so 2 lượt mới với 2 lượt cũ chưa ghi rõ ⇒ tiêu chí K / N0 / S1 đọc được nhiều cách** (§4).
- "số câu sang `tro_ly_hue` (bản mới) ≤ bản cũ + `N_AA`": không nói đếm ở **lượt nào** (lượt 1? cả hai? hợp hai lượt?), và `N_AA` tính trên **toàn bộ** R + AT + L + N rồi dùng
  làm phần cho phép ở **từng nhóm nhãn** — một nhóm nhỏ (vd ngoài phạm vi 10 + 11 câu) được cộng nhiễu của cả 166 câu.
- Tác động: tiêu chí ghi trước mà đọc được nhiều cách thì sau khi có số dễ chọn cách thuận (luật `run-experiment`: chỉ số quyết ghi trước, một nghĩa).
- **Đóng:** ghi một câu: "một câu tính là *sang X* nếu ở **ít nhất một** lượt mới ra X; bản cũ đếm cùng cách trên 2 lượt cũ; `N_AA` = số câu **của đúng nhóm đó** đổi tuyến giữa
  2 lượt cũ". Golden (1 lượt mỗi bên): đếm theo câu, ngưỡng như S1 (xem m-2).

**M-2 (major) · N2 cho câu ngoài phạm vi có mục web là "đạt" — yếu hơn sàn S2b của spec** (§4 tầng 2, §6).
- Spec §12.3 **S2b**: "ngoài phạm vi có mục web = **0**". Hiện câu "giá vàng hôm nay / thời tiết nơi khác ngày mai" bị định tuyến chặn ⇒ 0 mục web. Sau đổi, câu nào lọt sang
  `tro_ly_hue` mà trợ lý trả `INSUFFICIENT_ANSWER` ⇒ cổng web mở (`assistant.py:839`) ⇒ câu hỏi ra Serper + mục "Từ web (chưa kiểm)" trả lời đúng câu ngoài phạm vi.
  Giới hạn User nhận 09/11 là "thỉnh thoảng" (1 / 20 kín G) — không phải giấy phép cho một **loại** câu mới (có từ chỉ ngày) đi web.
- **Đóng:** N2 = "0 câu bị trả lời **và** số câu có mục web ≤ bản cũ (0)" trên N + R + G; H giữ "ngoài phạm vi sang `tro_ly_hue` ≤ 1 / 10" nhưng câu đó **không** được có mục web.
  Có mục web ⇒ báo A (A trình User như một giới hạn mới), không tự tính đạt. Report ghi riêng: số câu sang trợ lý · từ chối `OUT_OF_SCOPE_ANSWER` (đóng cổng) · `INSUFFICIENT_ANSWER` (mở cổng) · mục web.

**Minor:**
- **m-1 · K phần "giữ đúng `khan_cap` ≥ cũ − `N_AA`" ⇒ âm** — theo phương án B (09/11), `khan_cap` và `tro_ly_hue` cùng một đường trả lời (`_pick_route` đổi tuyến, chỉ log
  `emergency_by` khác). Câu khẩn cấp chuyển `khan_cap` → `tro_ly_hue` người dùng thấy **y như cũ** ⇒ không giữ sàn nào. Giữ phần "sang `ngoai_pham_vi` / `tro_chuyen` = 0"
  (đúng sàn), phần còn lại chuyển thành **theo dõi** (vòng tự soi: bỏ đo không giữ sàn).
- **m-2 · Golden 1 lượt mỗi bên** — nhiễu định tuyến trên Golden không đo (G 09/11 chạy Golden ×2 cho S3). Chấp nhận để rẻ, nhưng ghi trong report **danh sách câu**
  Golden nhãn trong kho mới sang `ngoai_pham_vi` (ở lượt mới, không ở lượt cũ) để A xem từng câu, thay vì chỉ một số đếm so ngưỡng.
- **m-3 · AT "dùng lại 4 số `main`"** — `main` đã có T1 nhanh (`1633c18`, đổi ngữ cảnh câu có từ chỉ ngày) ⇒ ghi rõ 4 số dùng lại là của bản nào (lượt S1 G 09/11 cho 28 câu giống byte
  + 4 câu bộ dò ngày đo lại ở T1 nhanh 10/11), để người đọc biết mốc.

## Khớp (không finding)

- Đổi một thứ (`ROUTER_INSTRUCTIONS`), không luật từ khoá (User 21:00), không ví dụ bằng địa danh / câu thật; test T khoá chuỗi khác giống byte.
- L1 ≥ 8 / 9 ở **cả 2 lượt** + L2 đúng ngày ≥ 8 / 9 — khớp sàn handoff "≥ 8 / 9 câu lịch chung được trả lời đúng ngày"; X14 vẫn từ chối.
- H do E viết (B không đọc), chạy một lần trên bản khoá, không chỉnh sau H — đúng luật giữ mù; người chạy ≠ B (auto mode chặn đọc `*sealed*` ⇒ lệnh `!` chỉ in số đếm).
- Tiền ≈ 0,06–0,11 ≤ 0,15, có điểm dừng 0,14. Không đo tốc độ riêng (theo dõi `routing_ms`) — hợp lý với lời dặn dài thêm ~2 dòng.

## Bước tiếp

B sửa M-1, M-2 (+ minor nếu muốn) ⇒ bản 2 ⇒ C xem vòng 2 (chỉ phần sửa) ⇒ A duyệt sha.

## Vòng 2 (21:07 10/11/2026) — bản 2 sha256 `aa493aec252f`, chỉ phần sửa

| Finding | Bản 2 | Đóng? |
|---|---|---|
| M-1 | §4 "Cách đếm": "sang X" = ≥ 1 lượt, bản cũ đếm cùng cách; `N_AA(nhóm)` riêng từng nhóm nhãn; K / N0 / S1 dùng đúng nhóm. L1 vẫn chặt hơn ("cả 2 lượt") — hợp lý vì là mục tiêu việc | đóng |
| M-2 | N2: 0 câu bị trả lời **và** mục web ≤ bản cũ (= 0); "không đủ thông tin" mở cổng web ⇒ tính phạm, báo A; report tách 3 loại; H ghi "không mục web" | đóng |
| m-1 | K: phần giữ đúng `khan_cap` thành theo dõi, sàn chỉ còn "sang `ngoai_pham_vi` / `tro_chuyen` = 0" | đóng |
| m-2 | Golden: liệt kê từng câu đổi tuyến | đóng |
| m-3 | AT: ghi nguồn từng phần của 4 số (`442f758` + `3b52017` + `1633c18`), nói rõ không đo lại | đóng |

Không thấy chỗ sửa nào làm lệch phần đã khớp ở vòng 1. **Decision vòng 2: `ready_for_user_confirmation`** (0 blocker · 0 major · 0 minor mở) ⇒ A duyệt sha `aa493aec252f`.
