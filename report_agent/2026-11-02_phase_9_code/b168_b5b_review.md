# Review: Phase 9 B5b — thời tiết Huế (`thoi_tiet`), review cả nhánh `p9-b5b`

Decision: **changes_requested** (1 major, 3 minor)
Người kiểm: C (Claude Code, Opus 5.5) — C viết plan B5b và bộ đo, **không** viết code nhánh này; review sớm E17 / E18 do E làm.
Date: 10:58 06/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-05-phase-9-b5b-plan.md` (bản 2 `cc09fda9f634` + 2 mục "Chỗ đổi" A duyệt — file hiện `50fbdd0b4c27`)
Implementation report: `report_agent/2026-11-02_phase_9_code/b168_b5b_implementation.md` (§1–§12)

## 1. Phạm vi đã review

- Nhánh `origin/p9-b5b` **`18d1cec`**, gốc `439ccd4` (`main` hiện `23ea0f9` — `git diff 439ccd4 main -- backend frontend` rỗng ⇒ chưa cần rebase để review). 5 commit: `b669981` · `a0906a6` (E17) · `8bdeb65` (vòng chỉnh 1) · `18d1cec` (Q8 hiển thị).
- Exact diff 11 file (+798 / −18): `thoi_tiet.py` (mới, đọc hết), `assistant.py` (đọc hết phần đổi), `do_so.py`, `lich_trinh.py`, `generator_openai_full_corpus.py`, `full_corpus_prompt.py`, `chat.py`, `settings.yaml`, `test_assistant_boundary.py`, `App.jsx`; test `test_b5b_thoi_tiet.py` (lướt tên ca). `git diff --check` sạch. Không file ngoài phạm vi plan §3.
- Dữ liệu đo của B (private, chỉ đếm / đọc phần chữ model, không chép vào đây): `data/phase_9/b5b/da_thay/raw_lan{1,2}.jsonl`, `raw_v1_lan{1,2}.jsonl`; harness `data/phase_9/b5b/tools/app_thoi_tiet.py`.

## 2. Findings

### M-1 (major) — câu dự báo: chữ model là câu từ chối, code vẫn nối khối dự báo ⇒ người dùng thấy "không tìm thấy đủ thông tin" rồi ngay sau là số dự báo

- **Vị trí:** `backend/llm/assistant.py` `_thoi_tiet_cuoi` (nối `tool["khoi"]` vào `trace.answer` bất kể chữ model); đường stream `answer_turn_stream` (phát `thoi_tiet_noi` sau chữ model).
- **Yêu cầu:** mục tiêu sản phẩm (câu trả lời "dùng được", `Project_Status.md` §1); plan D5 "model chỉ viết lời quanh khối đó". Q3 chỉ đo "có gọi công cụ" nên không bắt được.
- **Bằng chứng [Chạy, đọc dữ liệu đo của B]:** lượt đã thấy × 2 trên `a0906a6`: câu `du_bao` **F03, F07 ở cả 2 lần (4 / 20 lượt dự báo)** — công cụ `thoi_tiet` được gọi (`trang_thai: ok`), chữ model bắt đầu bằng đúng câu từ chối `INSUFFICIENT_ANSWER`, theo sau là khối "Dự báo thời tiết Huế" do code nối; log `outcome: success`. F03 cả 2 lần và F07 lần 1 gọi công cụ **2 lần** (lần 2 nhận "Đã lấy dự báo ở lần gọi trước…"); F07 lần 2 gọi 1 lần vẫn từ chối. Report §8 ghi "Q3 ĐẠT 9 / 10", "bị rút lại 0 / 21" nhưng không nhắc 4 lượt này.
- **Tác động:** 1 / 5 câu hỏi dự báo ra câu tự mâu thuẫn — đúng loại lỗi "từ chối nhầm" người dùng thấy; cờ `refusal` của log cũng không bắt (câu ≠ câu từ chối nguyên văn).
- **Tiêu chí đóng (A chọn cách, đề xuất của C — luật bắt buộc ⇒ code):** lượt có kết quả công cụ `ok` mà chữ model (sau `strip()`) đúng bằng câu từ chối ⇒ **code** thay chữ model bằng một câu dẫn cố định (vd "Dự báo thời tiết Huế cho ngày bạn hỏi:") rồi nối khối như cũ; không còn câu từ chối đứng trước số. Một test cho đường thường + một cho stream. Xem thêm: lời trả về ở lần gọi thứ 2 có thể làm model hiểu là "không có gì" — chỉ đổi khi đo thấy cần (không gộp vào sửa này). Đo lại: chạy lại F03 / F07 × 2 (≈ 0,003 USD) ⇒ 0 lượt "câu từ chối + số".

### m-1 (minor) — chữ code nối sau câu từ chối của kho làm cổng tra web (B6, đang BẬT) đóng và cờ `refusal` thành sai — chưa khai báo, chưa đo

- **Vị trí:** `_thoi_tiet_cuoi` nối `CAU_BAO_LU` / `CAU_NGOAI_7_NGAY` / khối vào `trace.answer` ⇒ `web_gate_open` đòi `trace.answer.strip() == INSUFFICIENT_ANSWER` ⇒ đóng; `chat.py` `metrics["refusal"] = answer.strip() in REFUSAL_ANSWERS` ⇒ false.
- **Bằng chứng [Chạy, đọc dữ liệu đo]:** B01 (bão / lũ) lần 2: câu từ chối + câu bão / lũ, **không tra web** (cờ thoi_tiet tắt thì câu này đi cổng web ⇒ câu thiên tai cố định của B6); X01 vòng chỉnh 1 × 2: câu từ chối + câu "chỉ có dự báo 7 ngày", không tra web. Q4 chạy `tra_web` tắt ở cả hai bên (report §10) ⇒ tương tác chưa được đo.
- **Tác động:** nhỏ về an toàn (câu bão / lũ vẫn có NCHMF + 112), nhưng là đổi hành vi của B6 đang bật khi bật `thoi_tiet`, và số đếm từ chối trong log lệch.
- **Tiêu chí đóng:** A chốt hành vi mong muốn (đề xuất: giữ như hiện tại — câu cố định của B5b thay cổng web cho câu thời tiết — nhưng cờ `refusal` tính trên **chữ model** chứ không trên câu đã nối), ghi vào report + 1 test khẳng định hành vi đã chọn.

### m-2 (minor) — kiểm số D8 bỏ sót vài cách viết đơn vị

- **Bằng chứng [Chạy, ca dò C `/tmp/c207_tools/probe_b5b.py` trên `18d1cec`, tập cho phép {24, 30, 80}]:** bắt đúng "25–31 °C", "31 độ C", "95%", "95 phần trăm", "12mm"; **lọt** "31℃" (ký tự U+2103), "31ºC" (U+00BA, hay gõ nhầm), "31oC", "31 °F", "12 milimet". ("nhiệt độ cao nhất 31", "ba mươi mốt độ" là giới hạn đã khai báo.)
- **Tiêu chí đóng:** thêm `℃`, `º`, `oC`, `°F`, `milimet` vào mẫu đơn vị + 1 ca test mỗi dạng; không cần đo có phí.

### m-3 (minor) — cache 30 phút dùng qua nửa đêm ⇒ "mai" lệch một ngày

- **Vị trí:** `thoi_tiet.lay_du_bao` (cache chỉ theo thời gian); công cụ hiểu `tu_ngay` = chỉ số trong `kq.ngay` (0 = ngày đầu của bản ghi).
- **Bằng chứng [Chạy, ca dò]:** bản ghi "ok" có ngày đầu 06/11 đặt vào cache 20 phút trước ⇒ gọi lúc ngày 07/11 vẫn trả từ cache; `tu_ngay=1` ("mai") in dòng **07/11** (đúng ra 08/11). Dòng in có ngày nên không nói sai ngày, nhưng trả nhầm ngày người dùng hỏi trong ≤ 30 phút sau 0 giờ. (`ngoai_7_ngay` / `do_ngay_di` của lịch đã dùng ngày của bản ghi hoặc giờ Việt Nam đúng chỗ.)
- **Tiêu chí đóng:** cache chỉ dùng khi `kq.ngay[0]["ngay"] == hôm nay (giờ Việt Nam)` + 1 test.

Ghi chú (không phải finding): report ghi plan sha `cc09fda9f634`; file plan nay `50fbdd0b4c27` vì thêm 2 mục "Chỗ đổi" A duyệt — nên ghi sha mới khi cập nhật report. Không thấy over-engineering: một module gọi mạng, không retry / fallback chồng, cờ + Q1 như các bậc trước.

## 3. Cách người kiểm chạy lại thật

- Worktree tách `/tmp/c_b5b_probe/src` detach `origin/p9-b5b` `18d1cec` (symlink `data/`, `knowledge-base-hue/`).
- **Q1 fresh:** từ `backend/`: `env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python ../data/phase_9/b2_chay/tools/capture_all.py data/phase_9/b5b/q1_c_review/nhanh_18d1cec.jsonl` ⇒ `cmp` với bản bắt của `main` `0a9e0f3` C chạy cùng sáng (`data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl`; `main` `23ea0f9` chỉ khác tài liệu). Không gọi mạng, 0 USD.
- **Ca dò:** `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python /tmp/c207_tools/probe_b5b.py` — `kiem_so` với 12 cách viết, `ngoai_7_ngay` 5 câu tự viết, cache qua nửa đêm (đặt `_CACHE` bằng tay, không mạng).
- **Đọc dữ liệu đo của B:** script nhỏ đếm, theo từng lượt, có câu từ chối trong chữ không / có chữ nối sau không / công cụ đã gọi (chỉ in mã câu + số đếm).

## 4. Kết quả quan sát

- **Q1 fresh: 228 / 228 giống byte `main`** (sha `dba1f578eef1`) trên `18d1cec` [Chạy].
- **Bất biến kiểm:** "cờ `thoi_tiet` tắt ⇒ chuỗi gửi model và chữ trả về như `main`" — chuỗi gửi: Q1 trên [Chạy]; chữ trả về: đọc code — `_thoi_tiet_cuoi` chỉ gọi khi `flags.thoi_tiet`, `_lich_extra` không thêm gì khi cờ tắt, `lich_trinh_for_turn` nhận `du_bao=None`, stream chỉ phát `thoi_tiet_noi` khi khác None [Code, đọc].
- Ca dò: như M-1 / m-2 / m-3. `ngoai_7_ngay`: "20/11", "13/11", "tháng 12" ⇒ ngoài 7 ngày; "12/11" (6 ngày) ⇒ trong; "Tết" ⇒ không bắt (giới hạn, không phải lỗi).
- Dùng lại (không chạy lại): test 73 passed + `test_static_ui` 3 passed + Q8 Playwright của B trên `18d1cec` (report §12) — cùng commit, không đổi đầu vào.
- Tiền review: **0 USD**.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại lượt có phí (đã thấy, Q4, Q8) — dùng dữ liệu đo B để lại.
- Không chạy lại Q1m (B: 5 lần bắt có mục `thoi_tiet`, bỏ mục ⇒ giống byte); `18d1cec` chỉ đổi chữ khối nối sau lượt có công cụ ⇒ lý do dùng lại của B hợp lệ.
- Phần lịch D9 / D10 chưa đo được (chờ `lich_trinh` + bảng v5) — review chỉ đọc code `_dong_thoi_tiet_lich`.

## 6. Decision và bước tiếp theo

**changes_requested.** B sửa M-1 (cần A chốt cách — đề xuất ở trên), m-2, m-3 trong một lượt; m-1 chờ A chốt hành vi rồi B ghi report + test. Kiểm lại: C chạy test các ca mới + Q1 (0 USD) + đọc lượt đo lại F03 / F07 × 2. Sau đó: rebase lên `main` mới + Q1 ⇒ A merge cờ tắt ⇒ hỏi User bật.

## 7. Vòng kiểm lại (sửa `0380345`) — C, 11:15 06/11/2026 (`date`)

**Decision: ready_for_user_confirmation** — cả 4 finding đóng; không finding mới chặn.

- **Cổng:** `18d1cec..0380345` một commit, 4 file (`chat.py`, `assistant.py`, `thoi_tiet.py`, test), `git diff --check` sạch, không file ngoài phạm vi. Đọc exact diff.
- **M-1 — đóng.** `_thoi_tiet_cuoi`: có khối dự báo + chữ model (sau `strip()`) = câu từ chối ⇒ câu dẫn cố định `CAU_DAN_DU_BAO` + khối; stream giữ chữ chừng nào còn là khúc đầu của câu từ chối. Ca dò C (điều kiện giữ): "Tôi ", "Tôi không tìm", "\nTôi không", câu từ chối đủ ⇒ giữ; "Tôi có dự báo", câu từ chối + chữ khác ⇒ phát [Chạy]. Dữ liệu đo lại của B (`raw_sua_m1_lan{1,2}.jsonl`, `chat_metrics_sua_m1.log`) đếm độc lập: F03 / F07 × 2 ⇒ **0 / 4** câu từ chối trong chữ, 4 / 4 có câu dẫn + khối, `delta_matches_final` true 4 / 4, `refusal` false 4 / 4, `outcome` success 4 / 4 [Chạy]. Cả 4 lượt model vẫn gọi công cụ 2 lần rồi từ chối — sửa này không dựa vào lý do model từ chối (theo dõi, không sửa — A quyết).
- **m-1 — đóng.** `chu_cua_model` bỏ phần code nối ⇒ cờ `refusal` tính trên chữ model ở `/api/chat` và stream; cổng web giữ đóng sau câu cố định (hành vi A chốt) — có test.
- **m-2 — đóng.** Ca dò C trên `0380345`: "31ºC", "31℃", "31oC", "31 o C", "88 °F", "12 milimet", "12 mi-li-met" ⇒ đều bắt; không bắt nhầm "2 ốc đảo", "giảm 50 %", "2 li cà phê", "Thứ 7 ok", "5 ô cửa"; một ca dựng "phòng 31 OC Hotel" bị bắt (chỉ ra chữ bị rút ở câu hiếm — chấp nhận, ghi giới hạn) [Chạy].
- **m-3 — đóng.** `tu_cache()`: ca dò C gọi trực tiếp (không mạng): ngày đầu = hôm nay ⇒ dùng; ngày đầu = hôm qua ⇒ không; quá 30 phút ⇒ không [Chạy].
- **Chạy lại:** `test_b5b_thoi_tiet.py` + `test_b6_tra_web.py` + `test_chat_stream.py` **178 passed**; **Q1 fresh `0380345`: 228 / 228 giống byte `main` `0a9e0f3`** (`data/phase_9/b5b/q1_c_review/nhanh_0380345.jsonl`) [Chạy]. Dùng lại: bộ rộng 539 passed của B (cùng commit).
- **Quan sát (minor, không chặn):** lượt có **lịch + công cụ thời tiết** mà model chỉ viết câu từ chối — stream phát chữ giữ lại ở cuối **không** kèm dòng "Mình hiểu" (đường thường không thay vì `trace.answer` có dòng đó) ⇒ có thể lệch `delta_matches_final`. Hiếm, và phần lịch D9 / D10 chưa bật; xem lại khi đo phần lịch.
- Tiền vòng kiểm lại: **0 USD**.
- **Bước tiếp:** rebase lên `main` mới + Q1 ⇒ A merge cờ `thoi_tiet` tắt ⇒ A hỏi User bật (việc rủi ro cao — User đóng).
