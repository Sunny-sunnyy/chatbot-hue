# Implementation Report: Phase 9 bậc G — cổng 2 nhóm (ĐANG LÀM — còn kín, S1 / S4 chấm mù, S5)

Người làm: B (Claude Code, `hue-rag-a1`) · cập nhật 12:22 08/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-08-phase-9-g-cong-plan.md` bản 2 `2513df2c6930` (A duyệt sau review sub-agent 2 vòng). Spec bản 13 §12 `5557f0fd7650`.
User 08/11 (qua A): mức dừng G **0,75 USD**; cho chỉnh lời dặn **nhiều vòng** trên bộ đã thấy, lượt quyết cuối trên bộ **kín** + an toàn ×2 + mẫu 30 trên sha khoá.

**Sha khoá:** nhánh `p9-g-cong` **`87d6798`** · `ROUTER_INSTRUCTIONS` **`6b4796f7a35c`** · `ANSWER_SYSTEM_INSTRUCTIONS` **`426109d21b13`** · lời dặn biểu mẫu `81d3040cf53f`
(= `main`, giống byte). Mốc: worktree `main` `442f758` (ROUTER `164bd4a254e9`, ANSWER `81d3040cf53f`).

## 1. Thay đổi code (`d0849ce` + 3 commit chỉnh lời dặn)

- Định tuyến 2 nhãn `tro_ly_hue` / `tro_chuyen` (`RouteOutput` + V1 / V3 `Literal` 2 giá trị).
- `ANSWER_SYSTEM_INSTRUCTIONS` = phần đầu cũ + **khối ngoài phạm vi** + câu "không đủ thông tin" cũ; lượt biểu mẫu dùng `ANSWER_BIEU_MAU_INSTRUCTIONS` = bản cũ (M-4).
- `_finish_generated`: chữ model `strip()` = `OUT_OF_SCOPE_ANSWER` ⇒ `_set_fixed(…, "out_of_scope")` trước `check_citations` / khối thời tiết; stream không phát lại chữ.
- Gỡ: `llm/emergency.py`, cờ `emergency_rule`, `ROUTE_KHAN_CAP` / `ROUTE_NGOAI_PHAM_VI`, `emergency_by`, 3 nhánh chết sau định tuyến, giao diện `.emergency`,
  `test_emergency.py`; `REMEMBERED_OUTCOMES` bỏ `emergency`.
- Test: `tests/test_g_cong.py` (mỗi loại lượt; biểu mẫu giống byte; 3 đường `out_of_scope` chữ đúng 1 lần; `done` không `tu_choi_kho`; không nối khối thời tiết);
  sửa `test_assistant.py`, `test_toc_do_song_song.py`, `test_b6_tra_web.py`, `test_cong_dot_1.py`. Test rộng (không khoá) **749 đạt** — còn lại đúng 2 test cần khoá.

## 2. Các vòng (mỗi vòng: sha · đổi gì · số · tiền) — đếm bằng code `data/phase_9/g_cong/tools/do_g.py`

| Vòng · lúc | Sha | Đổi gì | S2 | S2b | S3 | S3b | S2c (17) | Khẩn cấp (30, quan sát) | A4 / A5 âm lịch | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| mốc `main` · 11:25–11:55 | R `164bd4a2` · A `81d3040c` | — | — (tuyến riêng) | — | 0 ×2; xã giao ⇒ Huế 1 / 15 | — | 16 | — | (tuyến ngoai_pham_vi — E thấy) | 0,108 |
| G0 định tuyến · ~11:30 | R `8f3c3e04` | 2 nhãn | | | **0 ×2**; nhưng nhắc tên chuỗi B3 ⇒ Huế **6 / 7** | | | | | 0,041 |
| G1 định tuyến · ~11:38 | R `6b4796f7` | + "hỏi lại điều người dùng đã kể (tên, tuổi…) = xã giao" | | | **0 ×2**; xã giao ⇒ Huế 2 / 27 (lịch sử 1 / 7, (a) 1 / 8) | | | | `tro_ly_hue` ×2 | 0,043 |
| G1 cả câu ×2 · 11:41–11:50 | R `6b4796f7` · A `33690e61` | khối ngoài phạm vi bản 1 | **0 ×2** | **7 · 5** ✗ (nơi khác ⇒ "không đủ thông tin" ⇒ web) | | 0 (sàn) | 16 · 15 | 9 ⇒ ngoài phạm vi ✗ | ⇒ ngoài phạm vi ✗ | 0,236 |
| G2 · 12:04 (1 lượt) | A `5d70126f` | nơi khác / nhờ viết thư ⇒ ngoài phạm vi; câu không nêu nơi ⇒ về Huế | 0 | **2** ✗ | | **0** | 16 | 0 ngoài phạm vi (27 "không đủ" + web, 3 trả lời) | "không đủ" | 0,155 |
| G3 · 12:13 (bộ bị ảnh hưởng) | A `426109d2` | nêu tên công trình / lễ hội / địa danh nơi khác ⇒ ngoài phạm vi; "không đủ thông tin" chỉ cho câu về Huế | **0** | **0** | | **0** | 15 (= sàn) | 0 ngoài phạm vi (28 "không đủ", 2 trả lời) | "không đủ" | 0,108 |
| **Khoá** · 12:18–12:22 | `87d6798` | — | an toàn ×2 + mẫu 30: 0 | 0 | | 0 | | | | 0,057 |

(Một lượt thử 11:42 0,0007; R = `ROUTER_INSTRUCTIONS`, A = `ANSWER_SYSTEM_INSTRUCTIONS`, 8 chữ đầu sha.) **Tiền G tới giờ ≈ 0,747 USD** / mức dừng 0,75.

S1 phần đếm được bằng code: "ngoài kho bị trả lời" **0** (4 câu ngoài kho của bộ an toàn ra "không đủ thông tin") ở cả 2 lượt khoá — mốc cũng 0. 3 số còn lại
(đảo cảnh báo · sai điều kiện mới · thiếu cảnh báo mới) **chưa chấm** (judge mù). S4 (mẫu 30) **chưa chấm**.

Đọc số:
- Khẩn cấp (chỉ quan sát, không sàn): sau G3 không câu nào bị trả "ngoài phạm vi"; 28 / 30 ra "không đủ thông tin" (đa số có mục web) — đúng rủi ro User đã chấp
  nhận khi bỏ câu soạn sẵn (spec §12.8). Bảng 4 loại câu trả lời (chỉ dẫn nơi giúp · từ chối thuần · mục web · nói sai nguy hiểm) **chưa** làm — cần đọc chữ.
- A4 / A5 (E nhờ): định tuyến đưa vào agent Huế (đúng); agent trả "không đủ thông tin" vì chưa có công cụ ngày — việc của T1.

## 3. Còn làm

1. **Kín (A chạy, lệnh trong `STATUS_B.md` mục 0g):** (a) 8 câu chỉ định tuyến ×2 (S3 = 0, chào thuần ⇒ Huế cộng phần đã thấy ≤ 2 / 16) · (b) 10 câu cả câu ×2
   (S2 = 0, S2b = 0). ≈ 0,011 USD ⇒ vượt nhẹ 0,75 — A quyết.
2. **Chấm mù 0 USD:** S1 (3 số còn lại, 2 judge, mẫu `data/phase_9/b2_chay/tools/an_toan_b2.py`, so mốc `ket_qua/cacau_moc_r1.jsonl`) · S4 (mẫu 30 khoá ↔ mốc).
3. **S5** (báo A trước; ≈ 0,06 USD ⇒ cần thêm tiền) · S6 từ `ket_qua/khoa_r1.jsonl` (trung bình câu Huế không web).
4. Cổng ổn định ⇒ report đủ ⇒ review cả nhánh.

Giới hạn: chuỗi nhiều lượt chỉ đo định tuyến (`lich_su`), chưa đo cả câu; đường đo cả câu là `answer_turn` (không stream) — stream / #6 tương đương bằng test 0 USD.
Dữ liệu: `data/phase_9/g_cong/` (`tools/do_g.py`, `ket_qua/` — `tuyen_*`, `cacau_*`, `khoa_*`).
