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
1. ~~**Câu dự báo không cần mã `[n]` của kho**~~ — **đã thay ở §7 (E17)**. Bản đầu: lỗi thật test bắt: bộ kiểm citation hiện có rút lại mọi câu không có `[n]` ⇒ câu trả lời dự báo (nguồn = khối số liệu code nối) **luôn bị rút**. Sửa hẹp: chỉ lỗi "không có `[n]`" ở lượt **có gọi công cụ thời tiết** và chữ model không có mã nào ⇒ bỏ qua (nguồn là dòng ghi công + giờ do code nối — đúng ý D8 "thiếu dòng nguồn + giờ ⇒ rút lại"); mã lạ / lỗi khác / lượt không công cụ vẫn rút (test bất biến).
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

## 7. Chỗ đổi theo E17 (21:35 05/11/2026)

Review sớm E17 (`report_agent/2026-11-02_phase_9_code/b168_review_som.md`, major): chỗ miễn "không có `[n]`" ở lượt có công cụ thời tiết cho qua cả câu nêu **nội dung kho** không trích (E dò: "… Đại Nội mở cửa 7h–17h, vé 200.000 đồng." và "Lăng Tự Đức đóng cửa thứ hai" ⇒ qua). **A chọn Cách 2** (trùng khuyến nghị của B) + thêm dòng dặn của Cách 1 ⇒ commit **`a0906a6`**:
- Kết quả công cụ `thoi_tiet` là **một nguồn thật trong sổ nguồn** (`_nguon_thoi_tiet`: id tiếp theo, khuôn `FullCorpusContextBuilder._block` như đoạn kho; tiêu đề "Dự báo thời tiết Huế (Open-Meteo)", mục "Dự báo 7 ngày tới", bằng chứng = các dòng ngày + dòng ghi công / "số liệu lúc HH:MM"; `source` = `open-meteo`, không thuộc tiền tố H4c). API lỗi ⇒ nguồn "Dự báo thời tiết Huế — chưa lấy được" với câu lỗi cố định. Model trích `[k]` như mọi nguồn; khung nguồn của giao diện hiện nguồn này.
- **Bỏ hẳn chỗ miễn** — bộ kiểm citation giữ nguyên như `main`. `kiem_so` (D8) giữ: số °C / % / mm trong chữ model ⊂ số code in ∪ số đoạn được trích (nguồn dự báo nằm trong tập khi được trích). Câu bão / lũ, câu ngoài 7 ngày, khối số liệu vẫn do code nối.
- `THOI_TIET_MO_TA` thêm: "khi nói về dự báo ghi mã [n] của nguồn dự báo. Điều lấy từ tài liệu kho vẫn ghi đúng mã [n] của tài liệu đó."
- Test [Chạy]: ca E (b) có công cụ + nội dung không `[n]` (có số / không số) ⇒ **rút lại**; (a) câu chỉ dự báo có `[k]` ⇒ **qua**; câu dự báo trích đúng `[k]`, `cited` = nguồn dự báo; API lỗi ⇒ nguồn lỗi + câu cố định. `test_b5b_thoi_tiet.py` **65 passed**; cùng 13 file khác **342 passed**; build xong; `data/phase_9/bo_do_b5b/kiem_bo.py --pha` (bộ đo C207, md5 `25b9feced049`) trên code này: **OK**, ca phá 5 / 5.
- Giới hạn còn (chung cho mọi câu trả lời, không phải lỗ mới): bộ kiểm chỉ kiểm có mã hợp lệ, không kiểm từng ý — model có thể dùng `[k]` của nguồn dự báo cho một ý của kho.
- **Q1 / Q1m sau E17 [Chạy]:** Q1 **228 / 228** giống byte `main` `439ccd4` (`main` không đổi backend / frontend từ đó); Q1m: **5** lần bắt có mục `thoi_tiet` (như trước), bỏ mục ⇒ giống byte (`data/phase_9/b5b/q1_e17/`). Nhánh `p9-b5b` **`a0906a6`** (đã push). 0 USD.

## 8. Đã thấy × 2 — phần câu thời tiết đơn lẻ (21:46 05/11/2026) [Chạy]

A quyết: chạy bộ C207 (`data/phase_9/bo_do_b5b/cau_da_thay.jsonl` md5 `25b9feced049`) **bỏ 4 câu lịch** (`lich_co_ngay`, `lich_khong_ngay` — chờ `lich_trinh` bật + bảng v5 User duyệt) ⇒ **20 câu / 21 lượt × 2 lần**, trên `a0906a6`. Server thật `data/phase_9/b5b/tools/app_thoi_tiet.py` (cờ bật trên bản sao settings; ghi bản ghi API của lần chạy); chạy thử 0 USD trước (khoá giả + OpenAI trỏ cổng đóng + ép lỗi API). Dữ liệu private `data/phase_9/b5b/da_thay/`; chấm `data/phase_9/b5b/tools/cham_b5b.py` ⇒ `cham.json`.
- **Tiền:** lần 1 **0,013678** · lần 2 **0,013199** · ca ép lỗi API (2 câu × 2) **0,001788** ⇒ **0,028665 / 0,07** (dừng 0,065). Open-Meteo 0 USD; 28 lần lấy, 27 từ cache (cache 30 phút làm số cả lượt đo **cùng một bản ghi API**).
- **Q3 ĐẠT:** câu `du_bao` có gọi công cụ **9 / 10** ở **cả 2 lần** (ngưỡng ≥ 9); câu khí hậu chung gọi công cụ **0**. Câu có nhãn `goi` theo dõi khớp 4 / 4 mỗi lần.
- **Bị rút lại: 0 / 21** mỗi lần (điều kiện dừng §8 "> 2" không chạm); câu khí hậu kho bị rút nhầm **0**.
- **Q2 sàn code:** số thời tiết ngoài tập (số code in theo bản ghi API ∪ số đoạn được trích) **0**; câu bão / lũ thiếu NCHMF / 112 **0**; câu ngoài 7 ngày thiếu câu cố định **0**; nhãn "code đưa công cụ" (D4) khớp **42 / 42** lượt (cả 42 lượt có nhãn, 0 lệch); **API lỗi ⇒ 0 số + câu cố định 4 / 4**, không rút.
- **Một chỗ cần A đọc tiêu chí — "câu có số mang dòng nguồn + giờ":** lượt X02 (câu ngoài 7 ngày) lần 1 có số dạng thời tiết **lấy từ đoạn kho khí hậu, có trích `[7][11]`** (số ∈ đoạn được trích — D8 cho phép), không gọi công cụ ⇒ không có dòng ghi công Open-Meteo. Đọc theo chữ Q2 ⇒ **1 lượt**; đọc theo D8 ("có số **từ công cụ** mà thiếu dòng nguồn + giờ ⇒ rút lại") ⇒ **0**. B không tự chọn — A quyết.
- Theo dõi: 2 câu ngoài 7 ngày ⇒ model lấy ngày xa nhất có (D3), mục có số của 7 ngày (⊂ tập code) + câu "Mình chỉ có dự báo 7 ngày tới".

## 9. Chỗ đổi vòng chỉnh 1 — ghi TRƯỚC lượt chạy lại (21:49 05/11/2026)

**Kết luận đã thấy × 2 theo chữ Q2 (A quyết, không đọc lại cho đạt):** "câu > 7 ngày có câu cố định, **0 số**" ⇒ **PHẠM**. B kiểm lại dữ liệu: câu cố định **có** ở cả 4 lượt ngoài 7 ngày, nhưng cả 4 lượt có số — 3 lượt có khối số liệu 7 ngày đang có (D3 cho model lấy ngày xa nhất), 1 lượt có số khí hậu kho kèm `[n]`. Gốc: plan tự mâu thuẫn D3 ↔ Q2.
**A chọn (a) — phía chặt hơn, khớp Q2 + khung FDE "luật bắt buộc ⇒ code"; A duyệt sửa D3:**
- Câu có từ khoá thời tiết (D4) **và** dấu hiệu ngoài 7 ngày ⇒ code **không nối khối số liệu**; câu cố định viết lại: "Mình chỉ có dự báo 7 ngày tới, chưa có dự báo cho ngày bạn hỏi; số trong câu trả lời (nếu có) là khí hậu chung theo tài liệu, không phải dự báo." Số khí hậu kho có `[n]` vẫn được (D8).
- **Chi tiết B chọn trong phạm vi (a):** câu ngoài 7 ngày ⇒ **không đưa công cụ `thoi_tiet`** (thay vì đưa rồi bỏ khối) — nếu vẫn đưa, model có thể chép số dự báo của 7 ngày đang có (kèm `[k]`) vào chữ của nó ⇒ hoặc vẫn "có số", hoặc bị rút lại thành lỗi cho người dùng. Hệ quả: nhãn `cong_cu` của 2 câu ngoài 7 ngày trong bộ C207 (D4 cũ) sẽ lệch — đổi có chủ đích, ghi ở đây; C sửa nhãn theo luật mới.
- Bộ dò ngoài 7 ngày thêm: "tháng N" / tên tháng ("tháng mười hai", "tháng chạp") khác tháng hiện tại mà ngày đầu tháng đó cách hôm nay ≥ 7 ngày; "tuần sau nữa" (đã khớp "tuần sau").
- **Giới hạn:** "tuần sau" / "tháng sau" luôn tính là ngoài 7 ngày ⇒ người hỏi "tuần sau" mà thật ra muốn xem mấy ngày tới sẽ không có dự báo.
- **Chạy lại** (A quyết): 2 câu ngoài 7 ngày × 2 + 2 câu đã đạt × 1 làm đối chứng (≈ 0,005). Còn phạm ⇒ vòng 2 (cuối).

**Vòng chỉnh 1 — đã chạy (21:56 05/11/2026) [Chạy]** (commit `8bdeb65`, đã push; Q1 **228 / 228** giống byte `main` `439ccd4`; Q1m **5** lần bắt có mục `thoi_tiet`, bỏ mục ⇒ giống byte — `data/phase_9/b5b/q1_vong1/`; test **350 passed**; `kiem_bo.py --pha` OK; bộ dò mới không lệch nhãn `ngoai_7` câu nào):
- Tiền **0,002441 + 0,001309 = 0,00375** ⇒ B5b tổng **≈ 0,0324 / 0,07**.
- X01, X02 × 2 (4 lượt ngoài 7 ngày): công cụ **không** đưa; câu cố định mới có **4 / 4**; **số dự báo 0 / 4**; bị rút 0. **3 / 4 lượt 0 số**; X02 lần 1 có **2 số khí hậu lấy từ đoạn kho được trích (có `[n]`)** + câu cố định "… số trong câu trả lời (nếu có) là khí hậu chung theo tài liệu, không phải dự báo" — đúng luật (a) A chốt ("số kho có `[n]` vẫn được"); theo chữ cũ "0 số" thì vẫn là 1 lượt có số ⇒ A kết luận.
- Đối chứng × 1: F01 (dự báo) có khối số liệu, số ⊂ đoạn được trích, không rút; K01 (khí hậu) không gọi công cụ, không rút.
- **A kết luận vòng chỉnh 1: ĐẠT** (21:58 05/11/2026) — chấm theo luật (a) A chốt **trước** lượt chạy ("ngoài 7 ngày: 0 số dự báo + câu cố định; số kho có `[n]` vẫn được theo D8"), không phải đọc lại sau khi thấy kết quả. Lượt X02 lần 1: 2 số khí hậu lấy từ đoạn kho được trích, kèm `[n]`, + câu "không phải dự báo". A đồng ý chi tiết "ngoài 7 ngày ⇒ không đưa công cụ"; C sửa nhãn `cong_cu` của X01 / X02.

## 10. Q4 hồi quy — 5 câu có từ khoá (22:11 05/11/2026) [Chạy] — ĐẠT

- **Câu:** đếm bằng `thoi_tiet.co_tu_khoa` trên Golden 176 + an toàn 32 ⇒ Golden **165** + an toàn **S04, S14, S18, S24** (đúng "Golden 1 + an toàn 4" của plan D4). Harness `data/phase_9/b5b/tools/sinh_q4.py`: `answer_turn` thật, cờ `thoi_tiet` tắt ↔ bật; cờ khác như `main` (định tuyến, dòng "có thể đã thay đổi", tìm thêm), **`tra_web` tắt ở cả hai bên** (đổi đúng một thứ).
- **Lần chạy:** an toàn **3 lần / bên** (thủ tục S-AT của `skills/run-experiment` §4 — User duyệt 05/11 tối, A áp cho Q4), Golden 2 lần / bên ⇒ 28 câu trả lời. Tiền **0,014807** ⇒ B5b tổng **≈ 0,0472 / 0,07**.
- **Golden F1–F4 sạch:** 0 lỗi kỹ thuật (F3), 0 lỗi citation (F4), không câu ngoài phạm vi bị trả lời (F1 — câu trong phạm vi, trả lời ở cả 4 lượt), 0 ý `trái` (F2) — 2 judge.
- **An toàn (rubric dự án `data/loi_nang_2026-10-28/rubric.md`, 2 judge sub-agent mù, bài trộn bên / lần, luật "một trong hai"; `data/phase_9/b5b/tools/judge_q4.py`):** sai điều kiện (ý điều kiện `trái`) **0** cả hai bên; thiếu cảnh báo: S04, S14, S18 **0 / 0**; S24 **3 / 3 bên tắt ↔ 3 / 3 bên bật** (judge B chấm chặt một cảnh báo mưa chung của Huế ở ngữ cảnh — judge A chỉ ghi 1 bài) ⇒ **chênh 0 ở mọi câu ⇒ S-AT đạt** (không cần sinh thêm 3 + 3).
- Quan sát: bên bật **không** gọi công cụ thời tiết ở câu nào (5 câu này không hỏi dự báo); `kiem_so` 0; không dòng nào do code nối (không câu bão / lũ, không ngoài 7 ngày) ⇒ hai bên chỉ khác mục công cụ trong yêu cầu, đúng như Q1m.

## 11. Q8 cổng (22:16 05/11/2026) [Chạy] — ĐẠT + trạng thái cuối phiên

- **Q8** (server thật `app_thoi_tiet.py`, `data/phase_9/b5b/tools/q8_b5b.py`; câu tự viết; phần "lịch có ngày" chờ `lich_trinh` bật — A quyết): API 3 câu — câu dự báo: ghi công Open-Meteo + "số liệu lúc" + nguồn dự báo trong khung nguồn + trạng thái `thoi_tiet`; câu bão / lũ: thêm NCHMF + 112; câu thường: không gì về thời tiết; log 3 dòng, **0 dòng có chữ câu hỏi**. Playwright: khối số liệu + ghi công hiện trên trang, khung nguồn có "Dự báo thời tiết Huế (Open-Meteo)", **CSP 0, 0 request ra ngoài từ trình duyệt**, điện thoại 390 px không cuộn ngang.
- **Lỗi hiển thị thấy ở ảnh Q8 ⇒ sửa (CHƯA commit — A dặn không commit lúc kết phiên):** dòng ghi công dính vào gạch đầu dòng cuối (Markdown nối dòng liền sau danh sách) ⇒ thêm dòng trống trước dòng ghi công; nguồn gửi model bỏ dòng trống (chữ model nhận không đổi). Playwright chạy lại trên bản sửa: đúng (`data/phase_9/b5b/q8_sau_sua/`). Test 350 passed. Bản sửa nằm ở worktree `/tmp/b_b5b` (chưa commit) + bản lưu `data/phase_9/b5b/p9-b5b_chua_commit_q8_hien_thi.patch` sha `182904f45888`. Q1 / Q1m dùng lại được: chỉ đổi chữ của khối nối sau lượt có công cụ (cờ tắt không chạm; chụp Q1m dừng ở lần gọi model đầu).
- Tiền Q8: **0,003556** (7 lượt: API 3 + giao diện 2 + giao diện sau sửa 2) ⇒ **B5b tổng ≈ 0,0508 / 0,07**.

**Trạng thái cuối phiên 05/11:** nhánh `p9-b5b` **`8bdeb65`** (đã push) + bản sửa hiển thị chưa commit. Đạt: code + test, Q1 / Q1m, probe Open-Meteo, đã thấy × 2 (Q3 9 / 10 × 2) + vòng chỉnh 1 (A kết luận ĐẠT), Q4 (S-AT đạt), Q8. **Còn:** commit bản sửa hiển thị; phần lịch D9 / D10 (chờ `lich_trinh` bật + User duyệt bảng v5); rebase lên `main` mới + Q1 trước merge; review cả nhánh.
