# Implementation Report: Phase 9 — B5b thời tiết Huế (`thoi_tiet`, B168, phần 0 USD)

Người làm: B (Claude Code, Opus 5.5)
Date: 21:26 05/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-05-phase-9-b5b-plan.md` bản 2 sha `cc09fda9f634` (A duyệt 13:36 05/11; review E vòng 2 ready)
Nhánh: `p9-b5b` — code `2005566` rồi rebase 2 lần (lên `7ff8e5a` merge B6, rồi `439ccd4` B6 bật) ⇒ **`b669981`**. Worktree `/tmp/b_b5b`.

## 1. Phạm vi

- **Đã làm (plan §6 bước 2, 0 USD):** code D1–D11 + test, cờ `thoi_tiet: false`; Q1 / Q1m (mục 4).
- **Chưa làm:** probe Open-Meteo thật (bước 3, 0 USD); đã thấy × 2, Q4, Q8 (có phí — sau khi A báo; thứ tự plan: sau sửa lịch). Bảng v4 (`diem_v4.json`) **User chưa duyệt** — code chỉ **đọc** cột `trong_nha` / `bac_thang` (thiếu cột ⇒ không gợi ý); `settings.yaml` vẫn trỏ bảng v3.

## 2. Thay đổi chính

| File | Việc |
|---|---|
| `backend/llm/thoi_tiet.py` (mới) | Module **duy nhất** gọi Open-Meteo (D2): toạ độ Huế cố định, `timezone=Asia/Ho_Chi_Minh`, 7 ngày, `daily` nhiệt độ max / min, xác suất mưa max, lượng mưa + `current` (lấy giờ số liệu). `lay_du_bao` (D7): hết giờ 3 s, không thử lại; HTTP ≠ 200 / JSON hỏng / sai schema / độ dài ≠ 7 / số ngoài miền (nhiệt −10…50, xác suất 0…100, mưa 0…1000) ⇒ "loi", 0 số; cache RAM 30 phút (chỉ kết quả đạt). `khoi_du_bao` (D5): dòng cố định / ngày (làm tròn: nhiệt độ, xác suất nguyên; mưa 1 chữ số thập phân) + "Dữ liệu thời tiết: Open-Meteo.com (CC BY 4.0) — số liệu lúc HH:MM dd/mm. Dự báo có thể thay đổi." + câu "theo cả ngày" khi câu có buổi. Bộ dò: từ khoá D4 (cả từ, câu cuối hoặc câu hỏi liền trước), bão / lũ D6 ("cảnh báo" chỉ khi cùng từ thời tiết), ngoài 7 ngày D3, buổi D5. D8 `so_thoi_tiet` / `kiem_so`. Câu cố định: lỗi API (link NCHMF), bão / lũ (NCHMF + cổng lũ quét `luquetsatlo.nchmf.gov.vn` + 112), ngoài 7 ngày. |
| `backend/llm/do_so.py` | `do_ngay_di` (D9): "mai" 1 · "ngày kia / mốt" 2 · "thứ X" / "chủ nhật" lần tới · "cuối tuần (này)" thứ Bảy · "dd/mm"; nhiều giá trị / ngoài 0–6 ⇒ None; "ngày thứ ba" (ngày 3 của chuyến) không bị hiểu là thứ Ba. |
| `backend/llm/assistant.py` | Cờ `thoi_tiet` + `du_bao` (hàm lấy dự báo, nạp ở rìa như `bang_lich`); công cụ `thoi_tiet(tu_ngay, den_ngay)` enum 0–6, ≤ 1 lần / câu, **chỉ dựng khi có từ khoá** (D4, trong `_lich_extra`); `_thoi_tiet_cuoi` chạy ở **mọi** câu `tro_ly_hue` khi cờ bật (D8 m-1): số thời tiết của chữ model ⊂ số code in ∪ số trong đoạn kho được trích, hỏng ⇒ rút lại như citation hỏng; rồi nối khối số liệu (hoặc câu lỗi) + câu bão / lũ + câu ngoài 7 ngày (khi có từ khoá). Lịch (D9 / D10): `_dong_thoi_tiet_lich` — ngày đi trong 7 ngày ⇒ một dòng dự báo / ngày lịch + "Nếu mưa ngày N: có thể thay X bằng Y (trong nhà)" (khả năng mưa ≥ 60 %, cùng cụm, chưa có trong lịch) + "X có nhiều bậc thang (theo kho)" khi người lớn tuổi; API lỗi ⇒ câu cố định; nối cuối khối ghi chú; **khung lịch không đổi**. Stream: trạng thái `thoi_tiet`; phần code nối phát thành `delta` sau chữ model (chữ hiện = câu cuối). |
| `generator_openai_full_corpus.py`, `full_corpus_prompt.py` | Công cụ thứ ba `thoi_tiet` (mô tả `THOI_TIET_MO_TA`, không thêm lời dặn hệ thống). |
| `backend/llm/lich_trinh.py` | `khoi_ghi_chu(…, them_dong=())` — rỗng ⇒ đúng như B5 (`kiem_ghi_chu` không đổi). |
| `backend/api/routes/chat.py` | Log `thoi_tiet` (D11): có đưa công cụ, câu bão / lũ, có gọi API, trạng thái, mã lỗi, ms, từ cache, số ngày, số "số ngoài tập" — không chữ. |
| `settings.yaml`, `test_assistant_boundary.py`, `App.jsx` | `thoi_tiet: false`; `httpx` cho `llm.thoi_tiet`; nhãn trạng thái "Đang xem dự báo thời tiết…". |
| `backend/tests/test_b5b_thoi_tiet.py` (mới) | Xem mục 4. |

**Lệch nhỏ so với plan (B tự quyết trong phạm vi):**
1. **Câu dự báo không cần mã `[n]` của kho** — lỗi thật test bắt: bộ kiểm citation hiện có rút lại mọi câu không có `[n]` ⇒ câu trả lời dự báo (nguồn = khối số liệu code nối) **luôn bị rút**. Sửa hẹp: chỉ lỗi "không có `[n]`" ở lượt **có gọi công cụ thời tiết** và chữ model không có mã nào ⇒ bỏ qua (nguồn là dòng ghi công + giờ do code nối — đúng ý D8 "thiếu dòng nguồn + giờ ⇒ rút lại"); mã lạ / lỗi khác / lượt không công cụ vẫn rút (test bất biến).
2. Toạ độ + hết giờ là hằng số trong code (D2 ghi "cố định trong code"; §3 ghi `settings.yaml`) — chỉ cờ ở `settings.yaml`.
3. "Hôm nay" của công cụ = ngày đầu API trả (giờ Việt Nam) ⇒ tất định theo bản ghi API của lần chạy (plan §5).
4. Câu "ngoài 7 ngày" chỉ nối khi câu có từ khoá thời tiết (tránh nối vào câu kho thường kiểu "tháng sau có lễ hội gì").
5. Câu bão / lũ không nối ở nhánh từ chối trước model (ngữ cảnh rỗng) / chạm trần — ghi giới hạn.

## 3. Cách đã chạy thật (0 USD)

Từ `/tmp/b_b5b/backend`: `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest -q -p no:cacheprovider tests/test_b5b_thoi_tiet.py tests/test_b6_tra_web.py tests/test_b5_lich_trinh.py …` (14 file + test Phase 10 ảnh); `cd frontend && npm ci && npm run build`; Q1 / Q1m: `data/phase_9/b2_chay/tools/capture_all.py` qua `/tmp/b164/capture_flags.py` (cờ trong bản sao settings) và `/tmp/b164/capture_bo_cong_cu.py` (bỏ đúng mục công cụ `thoi_tiet` trước khi băm, đếm số lần bắt có mục đó).

## 4. Kết quả quan sát

- **Test [Chạy]:** `test_b5b_thoi_tiet.py` **63 passed** (từ khoá khớp / không khớp, "trời ơi" = giới hạn, câu liền trước; bão / lũ + "cảnh báo bậc thang"; ngoài 7 ngày, buổi; ngày đi 9 ca; schema / làm tròn / giờ cập nhật; 9 ca lỗi API ⇒ 0 số; yêu cầu chỉ có toạ độ cố định + múi giờ; cache; khối số liệu đúng từng dòng; **mỗi dạng số D8 một ca** (°C, °, độ, độ C, %, phần trăm, mm, mi-li-mét, li, khoảng, "từ … đến", thập phân) + 3 ca không bắt nhầm ("giảm 50 %", "2 li cà phê", "3 ngày"); model tự thêm số ⇒ rút; lượt không công cụ viết số ⇒ rút; câu khí hậu trích kho có số ⇒ **không** rút; API lỗi ⇒ câu cố định + bão / lũ + ngoài 7 ngày, 0 số; "cảnh báo bậc thang" ⇒ không NCHMF; lịch có ngày ⇒ dòng dự báo + "Nếu mưa" (bảng v4) + bậc thang người lớn tuổi; lịch không ngày ⇒ 0 lần gọi API; lịch API lỗi ⇒ câu cố định, `kiem_ghi_chu` vẫn đạt; nối lõi: công cụ chỉ khi có từ khoá + cờ tắt ⇒ danh sách công cụ như cũ; khối nối đúng cuối câu; stream: chữ hiện = câu cuối, có trạng thái `thoi_tiet`; lịch: khung giống B5; bất biến citation). Cùng 13 file khác (gồm B6 đã merge, Phase 10): **340 passed**.
- **Q1 ĐẠT [Chạy, 21:27 05/11/2026]: 228 / 228 giống byte `main` `439ccd4`** (B6 bật) — `data/phase_9/b5b/q1/main_439ccd4.jsonl` ↔ `nhanh_tat.jsonl`, sha `dba1f578eef1` cả hai.
- **Q1m ĐẠT:** cờ `thoi_tiet` bật, bỏ đúng mục công cụ `thoi_tiet` ⇒ giống byte cờ tắt (`nhanh_bat_bo_thoi_tiet.jsonl`, `dba1f578eef1`); **5 lần bắt có mục `thoi_tiet`** / 456 — khớp đếm của plan D4 (Golden 1 + an toàn 4) ⇒ mọi lượt khác không đổi gì.
- **Probe Open-Meteo thật (bước 3, 0 USD) [Chạy, 21:27 05/11/2026]:** HTTP 200 (~1,0 s); khoá cấp trên có `daily`, `current`, `timezone` = `Asia/Ho_Chi_Minh`, `utc_offset_seconds` 25200; `daily` đúng 5 cột code dùng, 7 ngày; `current.time` cho giờ số liệu (bước 15 phút); qua `lay_du_bao` thật ⇒ "ok", khối số liệu dựng đúng khuôn, "số liệu lúc 21:15 05/11". Không chạm điều kiện dừng §8 (schema khớp). Phản hồi thô private `data/phase_9/b5b/probe/open_meteo_raw.json`.
- Tiền: **0 USD**.

## 5. Lỗi và giới hạn

- Từ khoá D4 không bao giờ đủ ("mai đi Huế có cần mang ô không?" ⇒ không công cụ; D8 vẫn chặn số bịa); "trời ơi" khớp từ khoá (đưa công cụ thừa, không sai số).
- Bộ dò D8 bắt số đứng **trước** đơn vị; "nhiệt độ 30" (không đơn vị) không bị bắt.
- Câu bão / lũ không có câu NCHMF ở nhánh từ chối trước model / chạm trần (`max_turns`).
- Bảng v4 chưa duyệt; "Nếu mưa" chỉ có khi bảng có cột `trong_nha` và cụm có điểm trong nhà (C196: chỉ cụm Kinh thành có).
- Phản hồi Open-Meteo trong test là bản ghi tay theo tài liệu — schema thật kiểm ở probe bước 3.

## 6. Bàn giao cho người kiểm

- Đọc trước: plan D3–D9, rồi `thoi_tiet.py`, `assistant.py` `_lich_extra` / `thoi_tiet_for_turn` / `_thoi_tiet_cuoi` / `_dong_thoi_tiet_lich`.
- Bước tiếp: probe Open-Meteo (0 USD) ⇒ đã thấy × 2 (có phí, sau khi A báo).
