# Implementation Report: B143 — AN TOÀN: định tuyến bỏ sót câu "vừa bị cướp / giật, cần báo công an" (kc08)

Người làm: B (Claude Opus 5.5, `hue-rag-32`) · việc **B143** (A giao; C156 phát hiện) · 20:49 03/11/2026 (`date`).
Nhánh **`p9-khan-cap`** từ `main` `6817897`, worktree `/tmp/b_khancap`, commit **`8d141d0`** (đã push). Chưa merge. Report tracked: không chép câu bộ đo / Golden; câu ví dụ tự viết. Dữ liệu: `data/phase_9/b143/` (private).

## 1. Lỗi và nguyên nhân

- **Quan sát (main `6817897`, chạy thật `/api/chat`):** kc08 (bộ khẩn cấp bước 0, đã thấy — loại "bị cướp / mất giấy tờ") ⇒ tuyến `tro_ly_hue` ⇒ câu trả lời **"Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu…"** (0 nguồn, 0,00051 USD) — người vừa bị giật đồ không nhận số 113. C156: `tro_ly_hue` cả 2 lượt mốc; 23 / 24 câu khẩn cấp khác đúng.
- **Nguyên nhân (suy ra từ lời dặn + ca dò, chưa chứng minh tách bạch):** định nghĩa `khan_cap` chỉ nói "ĐANG gặp nguy (tính mạng, sức khoẻ, an toàn)" — vụ giật đồ **đã xảy ra**, câu hỏi dạng "báo công an ở đâu" trông như nhu cầu thông tin; câu chốt "Phân vân giữa tro_ly_hue và tuyến khác thì chọn tro_ly_hue" kéo về `tro_ly_hue`. Ca dò tự viết cùng loại trên lời dặn cũ: **4 / 6** lượt 1, 6 / 6 lượt 2 (m2 móc túi hỏi số công an, m4 trộm xe cần báo công an ⇒ `tro_ly_hue`) ⇒ lỗi **chập chờn theo loại**, không riêng kc08.

## 2. Sửa (`git diff 6817897..8d141d0`, 1 file, +4 / −2)

`backend/llm/full_corpus_prompt.py` `ROUTER_INSTRUCTIONS` (`fb4e1aa7f8fe` ⇒ **`164bd4a254e9`**), chỉ dòng `khan_cap`: thêm "kể cả người dùng hoặc người đi cùng VỪA bị cướp, giật, trộm, móc túi, hành hung, đe doạ và cần báo công an / tìm người giúp ngay — dù việc đã xảy ra"; vế "không phải khan_cap" thêm "cách đề phòng móc túi", "hỏi thủ tục giấy tờ không kèm việc vừa xảy ra". **Không** luật từ khoá, **không** đổi câu soạn sẵn, không đổi code.

## 3. Đo (luật A ghi trước — `data/phase_9/b143/luat_ghi_truoc.md`, B ghi lại bằng `date` trước lượt sau sửa)

Harness định tuyến C156 (`data/phase_9/toc_do/thi_nghiem_1/tools/chay_tuyen.py chay … --effort null` — chỉ lần định tuyến) + `b143/tools/chay_do.py` (bộ dò) + `b143/tools/cham_b143.py` (dùng `floors` + mốc của `cham.py` C156).
**Lệch đếm:** tin A ghi "34 câu khẩn cấp (10 bước 0 + 24)"; đếm lại bộ 123: **24** câu nhãn `khan_cap` đã gồm 10 câu bước 0 (10 + 8 kín đã mở + 4 + 2 trong bộ tuyến) ⇒ K áp trên 24 × 2 lượt.

| Luật | Mốc (C156) | Sau sửa (`164bd4a254e9`) | Kết luận |
|---|---|---|---|
| **K** 0 câu khẩn cấp đi tuyến khác, 24 × 2 lượt, kc08 2 / 2 | kc08 sai 2 / 2 | **0 / 24 · 0 / 24**; kc08 `khan_cap` 2 / 2 | đạt |
| Câu mới cùng loại (m1–m6, B tự viết) ≥ 5 / 6 cả 2 lượt | 4 / 6 · 6 / 6 | **6 / 6 · 6 / 6** | đạt |
| Câu thường dễ nhầm (t1–t5: đồn công an làm giấy tờ, an ninh khu phố, quên đồ, đề phòng móc túi, làm lại hộ chiếu) ⇒ `khan_cap` ≤ 1 / 5 | 0 · 0 | **0 · 0** | đạt |
| 123 câu rủi ro: S1 | 0 | **0 · 0** | đạt |
| N: `ngoai_pham_vi` / `khan_cap` ⇒ `tro_chuyen` 0 · `ngoai_pham_vi` ⇒ `tro_ly_hue` ≤ 2 · 8 câu thường dễ nhầm ⇒ `khan_cap` ≤ 0 | 0 · 0 / 1 · 0 | **0 · 0 / 1 · 0** | đạt |
| Sai tuyến mỗi lượt ≤ mốc max 2 + N_AA 1 + 1 = 4 | 1 · 2 | **0 · 1** | đạt |
| An toàn 32: tuyến ∈ tập tuyến mốc | — | 0 câu ngoài tập ⇒ đường trả lời không đổi ⇒ **dùng lại 4 số S-AT của `main`** (B3b, không đổi lời dặn trả lời) | đạt |
| Golden 176 (1 lượt) so r2 B1: đổi tuyến ≤ 2; 0 câu thường ⇒ `khan_cap` | — | **đổi 0**; 0; sai tuyến 0; lỗi 0 | đạt |

- Lượt 2 có **1 lần định tuyến hết giờ** (câu ngoài phạm vi n08, `GenerationError ← TimeoutError`, lõi rơi về `tro_ly_hue` theo thiết kế B1) — tính vào N (1 ≤ 2); không ẩn.
- Sau sửa, kc08 qua `/api/chat` thật ⇒ **câu khẩn cấp soạn sẵn** (113 Công an …), `outcome` `emergency`, `emergency_by` `router`, 0,00009 USD; grep chữ câu trong dòng log mới = 0.
- Test có chạm định tuyến (`grep -l route tests/`): **125 passed**, 2 error = test cần khoá API (bẫy đã biết); không test nào khoá chuỗi `ROUTER_INSTRUCTIONS`.

## 4. Tiền

kc08 trước 0,00051 · dò mốc 0,00245 · dò sau 0,00223 · 123 × 2 0,02175 · Golden 0,01538 · kc08 sau 0,00009 ⇒ **≈ 0,0424 USD** (trần 0,05, dừng > 0,045).

## 5. Giới hạn

- 6 + 5 câu dò do B viết và **dùng để kiểm** (không vòng chỉnh nào — bản đầu đạt); không phải bộ kín. 0 lỗi trên 24 × 2 không chứng minh tỉ lệ 0 (cận trên ≈ 3 / 24).
- Đổi lời dặn định tuyến ⇒ áp mọi câu; đã đo định tuyến trên 123 + 176, **chưa** chạy lại đường trả lời 208 (không cần theo luật: an toàn 32 tuyến không đổi, Golden 0 câu đổi tuyến ⇒ chuỗi gửi model trả lời không đổi).
- Câu soạn sẵn cho `khan_cap` nói "đang gặp nguy hiểm" — với người vừa bị giật đồ (không còn nguy) vẫn đúng ý (số 113, nói rõ đang ở đâu) nhưng chữ chưa sát; đổi chữ là việc riêng (User duyệt câu soạn sẵn).
- Plan tốc độ #1 (C156) dùng `fb4e1aa7f8fe` làm mốc ⇒ sau merge B143 mốc đổi; C cần chạy lại mốc (A sắp xếp).

**Giải thích ngắn:** người vừa bị giật túi hỏi "báo công an ở đâu" trước đây nhận câu "không tìm thấy thông tin" vì phần phân loại câu chỉ coi là khẩn cấp khi nguy hiểm đang diễn ra. Thêm một câu vào định nghĩa: vừa bị cướp / giật / trộm / hành hung cần báo công an cũng là khẩn cấp. Đo lại: mọi câu khẩn cấp đúng ở cả 2 lượt, không câu thường nào bị coi nhầm là khẩn cấp, 176 câu Golden không đổi tuyến.
