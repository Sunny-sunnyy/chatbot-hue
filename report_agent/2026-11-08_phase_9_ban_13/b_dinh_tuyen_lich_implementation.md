# Implementation Report: câu lịch / ngày âm chung (không nhắc Huế) đi trợ lý — lời dặn định tuyến

Người làm: B (Claude Code, `hue-rag-05`) · 21:30 10/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-10-phase-9-dinh-tuyen-lich-plan.md` bản 2 `aa493aec252f` (C review 2 vòng ⇒ ready; A duyệt, commit `8c57c47`). Trần A nâng 0,18
(dừng 0,17) trước vòng 2. Nhánh `p9-dinh-tuyen-lich` **`e8e07c9`** (đã push; rebase lên `main` `f380d76` — `main` từ `e5505e7` chỉ đổi 1 dòng `backend/api/feedback.py` + tài liệu; sau rebase `test_feedback` + `test_toc_do_song_song` + `test_ngay_lich` 96 đạt, 27 s; worktree `/tmp/b_dtl`). **Merge chờ User đồng ý.**

## 0. Kết luận

- **ĐẠT mọi tiêu chí ghi trước** trên bản khoá (vòng 2). Câu lịch thuần từng bị xếp "ngoài phạm vi" nay được trả lời: **9 / 9** đi trợ lý ở cả 2 lượt (bản cũ 0 / 9),
  **8 / 9** trả lời đúng ngày (sàn ≥ 8); câu thứ 9 có nội dung đúng lịch nhưng bị rút lại ở bước kiểm citation (giới hạn, §3).
- Không câu khẩn cấp, an toàn, Golden hay ngoài phạm vi nào bị kéo sai; bộ giữ mù do E viết (B không đọc) đạt cả 3 sàn.
- **Đổi:** chỉ `ROUTER_INSTRUCTIONS` (`backend/llm/full_corpus_prompt.py`): sha **`164bd4a254e9` → `8cd30cbb359a`** (bản 1 `0b87d2974330` bỏ). Lời dặn trả lời
  `81d3040cf53f` giống byte `main`. Không cờ — gỡ = revert một commit.
- Tiền thật **≈ 0,169 USD** (trần 0,18).

## 1. Thay đổi (2 câu thêm vào lời dặn định tuyến)

- Ở tuyến `tro_ly_hue`: câu **chỉ hỏi về chính ngày tháng** — hôm nay / một ngày là thứ mấy, ngày âm ↔ dương lịch, ngày lễ / Tết rơi vào ngày nào, còn bao nhiêu ngày
  tới một ngày — cũng là `tro_ly_hue`, kể cả khi không nhắc Huế.
- Ở tuyến `ngoai_pham_vi`: câu có từ chỉ ngày nhưng hỏi **việc khác diễn ra vào ngày đó** mà không gắn với Huế (giá, tỷ giá, kết quả xổ số / thi đấu, lịch nghỉ, thời tiết
  hay sự kiện ở nơi khác) vẫn là `ngoai_pham_vi`. Không ví dụ bằng địa danh / câu thật.
- **Vòng 1 → 2:** bản 1 viết rộng ("câu hỏi về ngày tháng, … ngày lễ / Tết theo lịch") ⇒ kéo 1 câu ngoài phạm vi hỏi *việc diễn ra vào một ngày lễ* sang trợ lý (phạm N0,
  gần chắc sẽ mở cổng web). Bản 2 thu hẹp thành "chỉ hỏi về chính ngày tháng" + nêu "việc khác diễn ra vào ngày đó". Đây là vòng chỉnh cuối plan cho phép.

## 2. Kết quả theo tiêu chí ghi trước (bản khoá `8cd30cbb359a`)

Tầng 1 — **chỉ lần gọi định tuyến** (`data/phase_9/dinh_tuyen_lich/tools/tuyen.py`, chấm `cham_tuyen.py`; cũ `cu_r1/r2`, `g_cu` · mới `moi2_r1/r2`, `g_moi2`):

| Mã | Kết quả | Nhãn |
|---|---|---|
| **T** | chỉ `ROUTER_INSTRUCTIONS` đổi (sha trên); `ANSWER_SYSTEM_INSTRUCTIONS` giống byte; 2 test dùng `ROUTER_INSTRUCTIONS[:80]` để nhận lần gọi định tuyến — phần đầu không đổi | PASS |
| **L1** | 9 câu từng bị từ chối: **9 / 9** `tro_ly_hue` cả 2 lượt (cũ 0 / 9); 10 câu ngày khác (gồm câu ngoài kho phải từ chối) vẫn `tro_ly_hue` cả 2 lượt | PASS |
| **K** | câu nhãn khẩn cấp (R + AT): 0 sang ngoài phạm vi / trò chuyện (cũ 0). Theo dõi: giữ đúng `khan_cap` 20 ↔ 20 | PASS |
| **N0** | câu nhãn ngoài phạm vi (N 10 tự viết + R): sang `tro_ly_hue` cũ 0 ↔ mới **0** (ngưỡng 0) ⇒ không câu nào cần tầng 2. Bản 1: 1 câu (đã sửa ở bản 2) | PASS |
| **S1** | câu nhãn Huế (R + AT): sang từ chối cũ 0 ↔ mới 0 (ngưỡng 4; `N_AA(tro_ly_hue)` = 3) | PASS |
| **AT** | an toàn 32: tuyến mới (2 lượt) ⊂ tập tuyến cũ ở **32 / 32** ⇒ không sinh lại; 4 số hiện hành của `main` không đo lại (nguồn: plan §4 AT) | PASS (dùng lại, có lý do) |
| **G** | Golden 176 (1 lượt mỗi bên): đổi tuyến **1 câu** — `golden#145` (nhãn Huế, loại câu có điều kiện, **không có từ chỉ ngày / lễ**) `tro_ly_hue → ngoai_pham_vi`. Chạy lại riêng câu đó 5 lần mỗi bản: **5 / 5 `tro_ly_hue` cả cũ lẫn mới** ⇒ nhiễu. Bản 1: 0 câu đổi. Ngoài phạm vi sang Huế: 0 ↔ 0 | PASS (S1 tính chung: 1 ≤ 4) |
| **H** giữ mù (E chạy, B không đọc; `h_sealed_r1.jsonl`, sha bộ `5ef0d41b62f2`) | lịch chung **12 / 12** `tro_ly_hue` (sàn ≥ 10) · ngoài phạm vi có từ chỉ ngày **0 / 10** sang Huế (sàn ≤ 1) · khẩn cấp 3 / 3 `khan_cap` (sàn 0 sang từ chối) · 0 lỗi | PASS |

Nhiễu A/A bản cũ (2 lượt): `N_AA` khẩn cấp 0 · ngoài phạm vi 0 · Huế 3 · trò chuyện 0. 0 lỗi định tuyến ở mọi lượt.

Tầng 2 — **sinh + chấm** (server nhánh, `data/phase_9/t1/tools/chay_t1.py` của E, 19 câu L, 1 lượt; `l2_r1.jsonl`; dòng log `chat_metrics_tang2.log`):

| Mã | Kết quả | Nhãn |
|---|---|---|
| **L2** | `kiem_l2.py` (code): 0 / 19 cờ. Người chấm sub-agent (brief theo `t1_nhanh/cham/brief.md`, tự đổi lịch bằng `lunar_vn`; `cham/cham_l2_ket_qua.jsonl`) trên 12 câu (9 từng bị từ chối + 2 dao động + câu ngoài kho): **OK 10 · R 2 · L1 / L2 / L3 0**. 9 câu từng bị từ chối: **8 / 9 OK** (sàn ≥ 8); 1 câu R = lần trả lời bị rút do `citation_integrity_error` (nội dung đúng lịch — §3). Câu ngoài kho: từ chối chuẩn (R) như bản cũ. 9 câu đã đi trợ lý: outcome như E 10/11 (`ngay_nhanh.jsonl`) | PASS |
| **N2** | không câu ngoài phạm vi nào đổi sang trợ lý (N0 = 0, H = 0) ⇒ 0 mục web mới | PASS (không có ca) |

Ghi chú người chấm: nhãn ghi trước của một câu "hôm nay âm lịch" là `expected_type: refuse` (nhãn cũ từ trước khi User đưa câu ngày vào phạm vi) — người chấm gắn OK theo
thang chấm; nhãn cũ nên sửa thành "trả lời" (file nhãn của E, không phải việc này).

## 3. Giới hạn

- **1 / 9 câu lịch bị rút lại** (`citation_integrity_error`, giao diện báo lỗi) dù nội dung đúng — lỗi kiểm citation ở đường trả lời (có từ trước, không do lời dặn định tuyến).
  Chưa tìm nguyên nhân (ngoài phạm vi việc này) — đề xuất: xem câu có nguồn "Lịch hệ thống" khi model trích dẫn.
- Cỡ mẫu: 9 + 12 câu lịch chung; 0 / 20 câu ngoài phạm vi có từ chỉ ngày lọt — cận trên thật có thể vài phần trăm. Câu lịch thuần cần "Lịch hệ thống" + công cụ `ngay_lich`
  (đã bật). Không đo tốc độ (lời dặn dài thêm ~4 dòng ≈ +60 token vào mỗi lần định tuyến).
- Câu "lịch nghỉ" chung (nghỉ lễ / Tết mấy ngày) theo lời dặn mới là ngoài phạm vi.

## 4. Tiền, thời gian, kiểm tra

| Bước | USD (log / file kết quả) |
|---|---|
| Tầng 1 bản cũ (2 × 166 + Golden 176) | 0,0467 |
| Tầng 1 bản 1 (2 × 166 + Golden) | 0,0516 |
| Tầng 1 bản 2 (2 × 166 + Golden) | 0,0528 |
| Chạy lại câu Golden #145 (5 + 5) | 0,0014 |
| H giữ mù (E chạy, 25 câu) | 0,0026 |
| Tầng 2 (19 câu + cổng ổn định 3 câu) | 0,0136 |
| **Tổng** | **≈ 0,169** (trần 0,18, dừng 0,17) |

Cổng ổn định (server nhánh cổng 8876): `/health` 5 / 5 · câu trong kho có nguồn · câu ngoài kho tự viết có từ chỉ ngày ⇒ `out_of_scope` · mỗi câu đúng 1 dòng `chat_metrics` ·
0 chữ câu hỏi trong log. Giao diện không đổi ⇒ không build / Playwright. Test rộng (có key, bỏ `test_static_ui.py`): **861 đạt / 1 trượt** (`test_ban_do_lich.py::test_csp_adds_tile_host…` đòi bản build giao diện — worktree không build; cùng test ở working tree chính đạt), 3 phút 59 giây.

## Giải thích ngắn

Trước đây câu kiểu "hôm nay là ngày mấy âm lịch?" bị bước phân loại câu coi là "không liên quan Huế" và từ chối, dù trợ lý đã tính được ngày. Sửa: dặn bước phân loại rằng
câu chỉ hỏi về chính ngày tháng thì cho qua trợ lý, còn câu hỏi việc khác vào ngày đó (giá vàng, thời tiết nơi khác…) vẫn từ chối. Đo trên hơn 500 câu (kể cả bộ câu người
khác viết mà B không đọc): câu lịch nay được trả lời đúng ngày, câu khẩn cấp / an toàn / ngoài phạm vi không bị xếp sai thêm. Đổi phạm vi sản phẩm ⇒ User đồng ý mới merge.
