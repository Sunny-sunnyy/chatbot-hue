# Thí nghiệm tốc độ #1 — mức suy luận `none` cho lần định tuyến: **kết quả âm** (C156 + C165)

Người làm: C · 20:27 04/11/2026 (`date`) · plan `docs/superpowers/plans/2026-11-03-phase-9-toc-do-dinh-tuyen-plan.md` **bản 5 `da2ff2c8e56c`** (A duyệt, commit `7460b42`; trần 0,11 / dừng 0,105). Code cờ: nhánh `p9-toc-do-1` `d190545` (đã push; cờ `assistant.router_reasoning_effort`, mặc định `null` = như `main`). Dữ liệu private: `data/phase_9/toc_do/thi_nghiem_1/ban4/` (mốc / biến), chấm `tools/cham_ban4.py` `cc437bf4ed32`.

## Kết luận

**Kết quả âm — cờ giữ `null`, không đổi chatbot.** Biến `none` (lần định tuyến không suy luận) **phạm sàn S1**: 2 câu của bộ an toàn 32 (nhãn `tro_ly_hue`, không `chap_nhan`) bị đưa sang `ngoai_pham_vi` — một câu ở **cả 2 lượt**, một câu ở 1 / 2 lượt; ở mốc (cùng ngày, cùng lời dặn `164bd4a254e9`) cả hai câu đi `tro_ly_hue` ở 2 / 2 lượt. Người dùng hỏi câu an toàn về Huế sẽ nhận câu "ngoài phạm vi" thay vì câu trả lời có nguồn — đúng loại lỗi sàn S1 chặn. Theo luật ghi trước (plan §3 "Kết quả âm"): dừng, **không chạy** Golden 176 và chữ đầu (Q) — **NOT RUN**; không chỉnh lời dặn định tuyến.

## Số đo (plan §2–§3; mốc và biến cùng ngày 04/11, cùng commit)

| Phần | Mốc `null` r1 / r2 | Biến `none` r1 / r2 | Sàn | Kết quả |
|---|---|---|---|---|
| K — 24 câu khẩn cấp + 6 lượt khẩn cấp có lịch sử sai tuyến | 0 / 0 · 0 / 0 | 0 / 0 · 0 / 0 | 0 | đạt |
| **S1** — câu `tro_ly_hue` sang `tro_chuyen` / `ngoai_pham_vi` (123 câu) | 0 / 0 | **2 / 1** | 0 | **phạm** |
| S1 — tầng lịch sử (37 lượt `tro_ly_hue`) | 0 / 0 | 0 / 0 | 0 | đạt |
| N — ngoài phạm vi / khẩn cấp sang `tro_chuyen`; ngoài phạm vi sang `tro_ly_hue`; câu thường sang `khan_cap` | 0; 0; 0 | 0; 0; 0 | 0; ≤ 1; ≤ 0 | đạt |
| R — sai tuyến 123 câu (ngưỡng = sai mốc max 0 + N_AA 1 + 1 = 2) | 0 / 0 | 2 / 1 | ≤ 2 | đạt (sát ngưỡng) |
| R — tầng lịch sử 50 lượt (ngưỡng 0 + 0 + 1) | 0 / 0 | 0 / 0 | ≤ 1 | đạt |
| AT — câu an toàn ra tuyến ngoài tập mốc | — | 2 câu | 0 ⇒ dùng lại 4 số S-AT | không dùng lại được (đã âm ở S1, không sinh lại) |
| Lỗi gọi định tuyến | 0 | 0 | — | — |

**Theo dõi (không quyết; không phải đo ABBA cùng lúc):** ms định tuyến p50 / p95 — 123 câu mốc 1,74 / 3,04 s và 1,66 / 2,50 s ↔ biến 1,50 / 2,54 s và 1,31 / 2,04 s; tầng lịch sử mốc 1,50 / 2,54 s ↔ biến 1,16 / 1,75 – 1,90 s ⇒ nhanh hơn ≈ 0,2–0,35 s ở p50. Token suy luận định tuyến: mốc trung bình 25–32 / lần (max 104) ↔ biến **0**. USD / lần: mốc ≈ 0,0000884 ↔ biến ≈ 0,0000742 (−16 %).
**Quan sát:** hai câu đổi tuyến là câu mốc **suy luận nhiều nhất** trong bộ an toàn (62–90 token, gấp 2–3 lần trung bình) ⇒ [giả thuyết, chưa chứng minh] phần suy luận chính là chỗ model phân biệt câu an toàn về Huế với câu ngoài phạm vi; bỏ hẳn suy luận thì mất đúng ở câu khó.

## Tiền

C165: mốc 123 × 2 0,021710 + mốc lịch sử × 2 0,009609 + biến 123 × 2 0,018252 + biến lịch sử × 2 0,007860 = **0,057431 USD** (/ trần 0,11). C156 (03/11, mốc lời dặn cũ, không dùng lại): ≈ 0,0139. Tổng thí nghiệm #1 ≈ **0,0713 USD**. Probe `none` (C156) dùng lại.

## Đã làm / bằng chứng

- Rebase `p9-toc-do-1` lên `main` `244e82b` (main sau đó chỉ đổi docs, kiểm `git diff 244e82b main -- backend frontend` rỗng); comment code bỏ sha plan bản 2 (m-7); test 19 / 19 (`test_toc_do_router`, `test_assistant*`, `test_emergency`); push `--force-with-lease` (A cho phép).
- Harness `chay_tuyen.py`: thêm tầng `lich_su` (50 lượt = 31 lượt 2+ bộ B3 + 13 bộ B3b + 6 chuỗi khẩn cấp tự viết; lịch sử = câu hỏi trước ≤ 3, trả lời rỗng — như chạy thật khi chỉ nhớ câu hỏi; `route(..., history)` dùng `router_history_agent`); mỗi dòng ghi `router_sha` — mọi dòng 8 file = `164bd4a254e9` (script chấm từ chối file lệch).
- Chạy thử 0 USD trước lượt có phí: `kiem` 123 / 50 lượt + nhãn; `cham_ban4.py` trên dữ liệu phá (bắt K / S1 / AT / R / sha lệch).
- Script đo chữ đầu ABBA `tools/chu_dau_abba.py` đã viết + thử phần tính trên dữ liệu giả — **không chạy** (kết quả âm trước bước Q).

## Bước sau (đề xuất, A / User quyết)

1. Nhánh `p9-toc-do-1` là hồ sơ phương án bỏ ⇒ tag `hoso/p9-toc-do-1` rồi xoá khi User duyệt (WORKFLOW §9.6).
2. Theo plan §4: #6 (chạy lần trả lời song song với định tuyến, giữ chữ tới khi định tuyến xong) — plan riêng; #4 (gộp định tuyến vào lần trả lời) đổi kiến trúc ⇒ User quyết.
3. [Đề xuất, chưa có trong plan] Thử mức `low` / `minimal` là **thí nghiệm mới** (plan mới, tiêu chí ghi trước) — lợi tối đa nhỏ hơn `none` (p50 chỉ ≈ 0,2–0,35 s ở `none`), cần cân với chi phí đo (≈ 0,06 USD).
