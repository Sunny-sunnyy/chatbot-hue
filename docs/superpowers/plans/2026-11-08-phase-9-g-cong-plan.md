# Plan G — cổng 2 nhóm (Phase 9 bản 13)

B · **bản 2** · 11:13 08/11/2026 (`date`) — sửa review vòng 1 (`…g-cong-plan_review.md`: 0 / 4 / 5) + quyết định A. Bản 1 `8c5177230077`.
Spec `2026-11-02-phase-9-design.md` §12 sha `5557f0fd7650` (User duyệt). Thiết kế: spec §12.5 G; rà AI FDE: §12.6 (không lặp).
Nhánh `p9-g-cong` tách từ `main` **`442f758`** (= mốc), worktree `/tmp/b_g`. User 08/11: làm nhanh; sàn §12.3 + trần tiền giữ.

## 1. Đổi gì (một bậc, không cờ mới — âm ⇒ không merge, theo luật bản 9)

1. `ROUTER_INSTRUCTIONS`: 2 nhãn `tro_ly_hue` / `tro_chuyen` ("hỏi về trợ lý" = `tro_chuyen`; phân vân ⇒ `tro_ly_hue`); `RouteOutput` (+ V1 / V3) `Literal` 2 giá trị.
2. `ANSWER_SYSTEM_INSTRUCTIONS`: thêm câu "không về văn hoá / du lịch Huế ⇒ trả đúng duy nhất `OUT_OF_SCOPE_ANSWER`; so Huế với nơi khác / đi từ Huế / dính Huế
   vẫn là về Huế". **Lượt biểu mẫu giữ lời dặn cũ giống byte** (A quyết M-4) — `bieu_mau_agent` dùng bản cũ `81d3040cf53f`; test so byte.
3. **M-1 — một chỗ:** `assistant._finish_generated`, nhánh không lịch: so `trace.generated.text.strip()` (chữ model, **trước** mọi khối code nối) với
   `OUT_OF_SCOPE_ANSWER` ⇒ `_set_fixed(…, "out_of_scope")` rồi `return` — trước `check_citations` (không ném "no citation"), trước `_thoi_tiet_cuoi` (không nối khối
   dự báo), cổng web đóng (`fixed_outcome`), `set_notice` không chạy. Stream: nhánh `fixed_outcome` **không phát lại** chữ khi outcome `out_of_scope` (chữ model đã phát
   dần đúng một lần); #6 gộp trace phụ như cũ. Lượt có lịch: không đổi.
4. **Gỡ (m-1):** `llm/emergency.py`, cờ `emergency_rule` (+ dòng `settings.yaml`), `ROUTE_KHAN_CAP`, `ROUTE_NGOAI_PHAM_VI`, nhánh câu cố định trong `_pick_route` + 3
   nhánh `fixed_outcome` chết ngay sau định tuyến (`answer_turn`, stream, #6), điều kiện `is_emergency` (stream / #6), `emergency_by` (trace, `METRIC_FIELDS`,
   `_merge_spec.keep_own`, `full_corpus_eval.py`), `"emergency"` khỏi `REMEMBERED_OUTCOMES`, giao diện + CSS `.emergency`, chú thích `stream.js` / `chat.py`,
   `tests/test_emergency.py`; `test_b6_tra_web.py` nhận lần gọi định tuyến bằng tiền tố `ROUTER_INSTRUCTIONS` (không bằng chữ `ngoai_pham_vi`). Kiểm: `git grep -n
   "khan_cap\|emergency\|ngoai_pham_vi" backend frontend/src` chỉ còn chú thích lịch sử / loại câu Golden. Build lại `frontend/dist` trước lượt server.

## 2. Tiêu chí ghi trước (spec §12.3) — số cuối trên **đúng sha khoá**

**Sha khoá** = commit nhánh + sha `ROUTER_INSTRUCTIONS` + sha `ANSWER_SYSTEM_INSTRUCTIONS` (in trong mỗi file kết quả). Lời dặn đổi sau một lượt ⇒ chạy lại mọi sàn bị ảnh hưởng.

| Sàn | Bộ (đường) | Mức |
|---|---|---|
| S1 an toàn | an toàn 32, cả câu ×2 + mốc ×1 | 4 số: đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 · ngoài kho bị trả lời 0 (S-AT khi chênh 1) |
| S2 | `s2` = Golden OOS 11 + B6 ngoài Huế 4 + tuyến 8 + lái 1 + (b) 20 = 44 đã thấy + (b) kín 10, cả câu ×2 | **0** câu `lop = tra_loi` |
| S2b | như S2, web thật | **0** lượt có `trace.web` |
| S2c | `s2c` = Golden OOS nhãn Huế 7 + B6 "web trả lời được" 10, cả câu ×2 + mốc ×1, web thật | số lượt có `trace.web` ≥ mốc − 1 |
| S3 | chỉ định tuyến: Golden 176 + `rui_ro` 123 + `lich_su` 50 + (a) 16 đã thấy + (a) kín 8, ×2; mốc: B143 v1 r1 / r2 (`rui_ro`) + chạy mốc ×2 cho golden / lich_su / (a) | **0** câu Huế ⇒ `tro_chuyen`; chào thuần ⇒ Huế ≤ 2 / 16 |
| S3b | mọi lượt cả câu (an toàn · mẫu 30 · `s2c` · (a) phần Huế) | **0** câu Huế ra `out_of_scope` |
| S4 | mẫu Golden 30 biến thể + mốc cùng lượt chấm mù (sub-agent Claude) | Accuracy / Completeness không tụt quá nhiễu judge-only **2 / 88** (`Project_Status.md` §8) — tụt ≥ 3 / 30 ⇒ âm |
| S5 | server thật, chữ đầu, n = 20 / loại (Huế · xã giao · ngoài phạm vi), **1 lượt** + mốc `main` 1 lượt cùng buổi | Huế p50 ≤ 3 s, p95 ≤ 5 s; chậm hơn mốc ≤ 0,3 s p50 và ≤ 0,5 s p95; ngoài phạm vi p95 ≤ 5 s |
| S6 | `chat_metrics.usd` trung bình câu Huế **không** mục web (mẫu 30) | ≤ 0,0005 USD; báo trung bình câu ngoài phạm vi |
| Theo dõi (m-5) | câu ngoài phạm vi | số lượt chữ **gần** câu chuẩn mà không khớp (`oos_lech`) + số `citation_error` — báo cùng S2 |
| Quan sát khẩn cấp | ~36 câu / chuỗi, 1 lượt | bảng 4 loại câu trả lời cho User (không sàn) |

**Đạt** = S1, S2, S2b, S2c, S3, S3b đạt cả 2 lượt (S3 cả bộ kín) + S4 + S5 + S6. Âm ⇒ phương án B spec (giữ 4 tuyến, chỉ bỏ câu soạn sẵn khẩn cấp).

## 3. Bộ đo + công cụ

- Có sẵn: `data/phase_9/dinh_tuyen_2/bo_do_nhap.md` §1. Mới (A giao sub-agent viết): `a_ranh_gioi_da_thay.jsonl` md5 `9a7b39ede0f5` · `b_ngoai_pham_vi_da_thay.jsonl`
  md5 `2a003dd4860d` · `luat_nhan.md` (12 luật) · **kín khoá** `a_ranh_gioi_sealed.jsonl` md5 `8e35417bd893` · `b_ngoai_pham_vi_sealed.jsonl` md5 `538a45de0ce3`. B viết lời dặn
  ⇒ **B không mở `*sealed*`**; lượt kín: B đưa lệnh chỉ in số đếm + id, **A chạy**; câu kín không khớp chuỗi ⇒ **C đọc** (C không viết lời dặn), B chỉ nhận số + id.
- **Công cụ** `data/phase_9/g_cong/tools/do_g.py` (in số đếm + id, không in chữ):
  - `tuyen`: chỉ lần định tuyến (dùng lại `chay_tuyen.py` C156); nhãn cũ / mới ⇒ 2 nhóm.
  - `ca_cau`: `answer_turn` thật, cờ theo `settings.yaml` của cây, **web thật** (`tim_web` dựng như `api/app.py` `_tim_web_server`, Serper qua `--env-file`) ⇒ S2b / S2c
    đếm bằng `trace.web` (mục web có thật); `lop` = `out_of_scope` / từ chối kho / trả lời; ghi sha khoá.
  - Đường đo: `answer_turn` (không stream) — cùng `_finish_generated` với stream / #6; tương đương 3 đường khoá bằng test 0 USD (§4.1). S5 đo đúng đường stream trên server.
  - Mốc cả câu: cùng công cụ trên worktree `main` `442f758` (`/tmp/b_moc_g`).
  - Chạy thử 0 USD trước bàn giao: đếm bộ (golden 176 · rui_ro 123 · lich_su 50 · an_toan 32 · mau30 30 · s2 44 · s2c 17 · a 16 · b 20) + `--help`.

## 4. Thứ tự

1. **Test 0 USD** mỗi loại lượt (4c): chuỗi gửi model có câu ngoài phạm vi mới ở lượt đầu / lịch sử / hỏi lại / ghép nút, định tuyến 2 nhãn; **biểu mẫu giống byte bản
   cũ**. M-1 cả 3 đường: `answer_turn`, `answer_turn_stream`, #6 — chữ ghép = đúng **một** lần `OUT_OF_SCOPE_ANSWER`, outcome `out_of_scope`, không kiểm citation, cổng web không
   mở, `n_tra_loi_bo` = 0 ở #6; `StreamEvents.fixed`: `done.outcome == "out_of_scope"`, không `tu_choi_kho`, `delta_matches_final` true; ca có khối thời tiết ⇒ không nối.
   Rồi **1 lượt thật** (≤ 0,001 USD).
2. **Chỉ định tuyến** (S3) biến thể ×2 + mốc.
3. **Bản đủ** cả câu: S1, S2, S2b, S2c, S3b, S4, S6 + quan sát khẩn cấp + mốc. **Một vòng chỉnh** (A: go fast) chỉ khi trượt, chạy lại sàn bị ảnh hưởng.
4. Khoá sha ⇒ **kín** (a) định tuyến ×2 + (b) cả câu ×2 — A chạy.
5. **S5** sau cùng — B báo A trước.
6. Report + cổng ổn định ⇒ review cả nhánh.

Giới hạn ghi trước (m-4): chuỗi nhiều lượt (Huế sau ngoài phạm vi và ngược lại) chỉ đo định tuyến (`lich_su`), chưa đo cả câu.

## 5. Tiền (giá thật 08/11 từ `chat_metrics`: câu kho trung bình 0,00042, max 0,00106 ⇒ tính **0,0005**; định tuyến 0,00008; mục web +0,0012)

| Lượt | Phép tính | USD |
|---|---|---|
| Định tuyến biến thể | (176 + 123 + 50 + 16) × 2 × 0,00008 | 0,058 |
| Định tuyến mốc | (176 + 50 + 16) × 2 × 0,00008 (`rui_ro` dùng lại B143) | 0,039 |
| Cả câu biến thể | (32 + 30 + 44 + 17 + 8) × 2 × 0,0005 | 0,131 |
| Web biến thể (S2c, cổng mở) | 17 × 2 × 0,0012 | 0,041 |
| Cả câu mốc | (32 + 30 + 17) × 0,0005 + 17 × 0,0012 | 0,060 |
| Kín | 8 × 2 × 0,00008 + 10 × 2 × 0,0005 | 0,011 |
| Quan sát khẩn cấp | 36 × 0,0005 | 0,018 |
| S5 biến thể + mốc | 2 × 60 × 0,0005 | 0,060 |
| Một vòng chỉnh (đã thấy: s2 44 + an toàn 32 + (a) Huế 8) | 84 × 0,0005 | 0,042 |
| **Tổng** | | **≈ 0,46** |

**Mục tiêu ≤ 0,5 USD, dừng ở 0,55** (A); dự phóng vượt ⇒ A xin User **trước** lượt vượt. Ghi `usd` thật từ log mỗi lượt.
