# Review: Phase 9 B3 plan bản 1 (B135)

Người kiểm: C (Claude Opus 5.5) — viết bộ đo B3 (C136), không code B3. Date: 11:43 03/11/2026 (`date`). Việc C142 (A giao 03/11).
Plan `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` **bản 1 sha `aa75f956c320`** (C tính lại từ file — khớp). 0 USD.

## 1. Phạm vi đã review

- Chỉ dựa "Căn cứ để review": plan (toàn bộ); spec bản 9 `169c2dd5f86a` §3 "Nhớ" + "Log + vết", §4, §5 B3, §7; README bộ đo B3 + `c136_bo_do_b3.md`; `b134_b2_implementation.md` §4b, §4c, §6. Không đọc `STATUS_B` / tin B.
  Lệnh chỉ đọc: `compare_main.json` S-AT B2 (P0_thieu); `settings.yaml` (`safety_margin`, `context_limit`). Không chạy code B3 (chưa có).
- **A đã quyết D11 = (a)** (tin A 03/11): bên so của quyết 2 = câu gõ thật gửi không lịch sử; `dung_mot_minh` = trần. ⇒ C đã sửa câu chữ README bộ đo B3 (`57c31a7110c5`, bảng §2 + trường `dung_mot_minh` §3) và report C136 (`3301f3c7b7e3`). `kiem_bo.py` vẫn OK. Plan bản 2 dẫn sha README mới.
- Điểm A dặn soi: D5 đếm token, D6 lời dặn mới ⇒ hồi quy 208 + S20 ×3, cờ `nho_hoi_thoai` tắt tới khi có giao diện (D8), cookie / TTL / dữ liệu cá nhân, phần kín.

## 2. Đối chiếu spec (không finding)

| Spec | Plan | Khớp |
|---|---|---|
| §3 Nhớ: RAM theo phiên, cookie HttpOnly, mã ngẫu nhiên, TTL 30 phút, trần token; lưu câu hỏi + câu trả lời cuối đã cắt "Từ web", không kết quả công cụ; không log mã phiên / chữ | D1 (RAM, `token_urlsafe(16)` = 128 bit, HttpOnly + SameSite=Strict + Path=/api, TTL 30 phút từ lượt cuối, trần 500 cuộc), D2 (3 lượt / 1.500 token, bỏ mã trích dẫn, `stored_answer` để B6 cắt "Từ web", không kết quả công cụ), D4 (log chỉ `n_history_turns`, `history_tokens`) | đúng |
| §5 B3 sàn: hỏi tiếp ngoài kho 0 câu bị trả lời; hỏi tiếp điều kiện 0 đảo cảnh báo | Q5 (đã thấy + kín) | đúng |
| quyết 1 ≥ 9 / 10 chuỗi nhớ tên | Q3 (6 + 4 kín, luật tên README) | đúng |
| quyết 2 Completeness lượt sau so "gửi như câu độc lập" CI 95 % > 0, kín không ngược | Q4 + D11 (a) | đúng (cách hiểu "độc lập" A quyết) |
| mức tụt: đổi chủ đề ≤ 1 câu | Q6 | đúng (+ đếm câu tìm không mang đối tượng cũ) |
| S-G / S-AT nhớ tắt: dùng lại nếu hash lời dặn + công cụ không đổi | D6 đổi lời dặn chung ⇒ Q2 hồi quy **đủ 208** | đúng (không dùng lại vì có đổi) |
| kết quả âm ⇒ chỉ nhớ câu hỏi | "Kết quả âm" + cờ `nho_cau_tra_loi` | đúng |
| §7 trước khi deploy: `Host` + giới hạn lượt (R1 C106), lưu phiên | D1 + §8: `Secure`, `Host`, giới hạn lượt ⇒ danh sách trước deploy | đúng |

Các điểm A dặn:
- **D6 + S20:** lời dặn trả lời đổi một câu ⇒ Q2 đủ 208, so với câu trả lời B2 Q8 lượt 1 chấm cùng lượt mù; S20 sinh lại 3 lần mỗi bên, luật "không còn mới thật" (≤ 1 / 3, hoặc mốc ≥ 2 / 3) khớp spec §4; S-G dùng N_AA đường có công cụ (5 + 3 = 8) và từ chối nhầm mốc B2 (4) + 1 — đúng số B2 (C141 đã tính lại). Đổi **một** thứ ở Q2 — đúng run-experiment. (Thêm: m-2.)
- **D8 cờ `nho_hoi_thoai`:** mặc định false trên nhánh và lúc merge; Q10 bật trên **bản sao** `settings.yaml`; bật thật chỉ ở bước 8 sau khi User chọn mẫu — hợp lý (bật nhớ mà giao diện không hiện lịch sử thì người dùng không biết).
- **Cookie / TTL / dữ liệu cá nhân:** đúng §3; tắt cờ ⇒ không cookie, không kho (D7); grep tên / câu hỏi / `conversation_id` trong log = 0 ở Q10. Hai yêu cầu song song cùng cuộc: không khoá, ghi giới hạn — chấp nhận được với giả định một người dùng (spec §7).
- **Phần kín:** B không mở `chuoi_sealed.jsonl`; khoá trước kín; C chạy. (Thêm: m-3.)
- **D5 đếm token:** hướng đúng (đếm trên đúng danh sách mục gửi đi, test chặn hai tầng). (Thêm: m-1.)

## 3. Findings

**0 blocker · 0 major · 5 minor.**

- **m-1 — D5: thước token cần đo trên mọi lượt có phí, và phần đệm tính theo số mục.** B2 cho thấy test logic (thân yêu cầu + tokenizer) chênh chỉ 16 token, trong khi token thật của API chênh **194–352** (B134 §4b). Vậy test (a) "< 128" **không bắt được** phần đệm của API. Phần đệm này tăng theo **số mục** gửi đi (lịch sử 3 lượt = 6 mục thêm, mỗi lần `tim_kho` = 2 mục).
  **Đóng:** (1) `ITEM_OVERHEAD` là hằng số **mỗi mục** (không phải một số chung cho cả lượt), ước từ pilot có số mục khác nhau, ghi nguồn; (2) ghi "`usage.input_tokens` − builder" ở **mọi** lượt có phí (pilot, chuỗi đã thấy, Q2 — số đã có trong log, 0 USD), báo max; chênh ≥ 512 ở lượt bất kỳ ⇒ dừng (không chỉ ở pilot). Lý do cần: `context_limit` 16.384, B2b tới 30 đoạn + lịch sử 1.500 ⇒ ngân sách **có thể** chạm.
- **m-2 — D6 có thể làm *thiếu* cảnh báo, mà spec không đặt sàn cho việc thiếu.** S-AT spec chỉ có "0 đảo cảnh báo" + "P0_sai mới ≤ 2". Lời dặn "không thêm lưu ý không có trong nguồn" có thể khiến model bỏ cả lưu ý **có** trong nguồn. B2b đã có thêm 2 câu `P0_thieu` mới so mốc 01/11 (`compare_main.json`: 9 câu, mới S10 + S28). Plan §9 ghi "S-AT + Đủ bắt", nhưng `P0_thieu` không phải sàn.
  **Đóng:** Q2 báo `P0_thieu` (mới so B2 và so 01/11) như chỉ số theo dõi **ghi trước**, kèm luật: có thêm câu thiếu mới ⇒ báo A trước khi giữ D6.
- **m-3 — phần kín cần chấm điểm, nên ghi rõ ai chấm.** Q4 / Q5 / Q6 kín cần judge (Completeness; đảo cảnh báo bằng thước an toàn hai judge). Plan chỉ ghi "C chạy 15 chuỗi kín … gửi số đếm".
  **Đóng:** ghi rõ C chạy **và** chấm phần kín (sub-agent judge do C gửi, cùng prompt / thủ tục với phần đã thấy). B nhận số đếm + sha, không nhận câu trả lời kín. Lệnh harness `chuoi` có cờ để không in chữ.
- **m-4 — tiền §6:** cận dưới "0,13" không khớp bảng. Không chỉnh + không M2 thì cộng ra 0,08 + 0,003 + 0,045 + 0,03 + 0,01 ≈ **0,17**; cận trên 0,263 khớp. **Đóng:** sửa cận dưới.
- **m-5 — ghi D11 = (a) vào plan + dẫn README mới.** Plan bản 1 để D11 mở và dẫn README `3a369aaaf215`. **Đóng:** bản 2 ghi "D11 = (a), A quyết", bỏ (b), dẫn README `57c31a7110c5`. Ghi thêm: với (a), bên "câu gõ thật không lịch sử" thường bị từ chối ở câu hỏi tiếp ⇒ CI > 0 là ngưỡng **dễ**; số so với trần `dung_mot_minh` là số cho biết nhớ tốt tới đâu.

## 4. Giới hạn

- Không chạy code / lượt nào; mọi khẳng định về B2 (chênh token, P0_thieu, N_AA) lấy từ report / file kết quả B2 đã có (C141 đã tính lại phần Q8).
- Chưa đánh giá chữ của lời dặn D3 / D6 (B viết khi code; chữ D6 cuối A chọn).
- Bước giao diện 8 phụ thuộc lựa chọn của User — chưa review được.

## 5. Kết luận

**`ready_for_user_confirmation` sau khi bản 2 sửa m-5 (ghi D11 = (a))** — thiết kế khớp spec §3 / §5 B3, không finding chặn. m-1…m-4 sửa cùng bản 2; C chỉ kiểm phần sửa.

---

## Vòng 2 — bản 2 sha `cd099ec0a00e` (C142 · 11:48 03/11/2026 `date`)

Cách kiểm: `git diff --word-diff` bản 1 (`HEAD`, sha `aa75f956c320` — khớp) ↔ bản 2; bảng "Chỗ đổi bản 2". Không có chỗ đổi ngoài bảng. 0 USD.

| Finding | Sửa ở bản 2 | Kết luận |
|---|---|---|
| m-1 token | D5: `ITEM_OVERHEAD` **mỗi mục**, ước bằng hồi quy "token thật − số đếm" theo số mục (0 / 1 / 2 lần `tim_kho` × 0 / 1 / 3 lượt lịch sử); test logic ghi rõ chỉ bắt lỗi đếm thiếu mục; Q8 + §7: "token thật − builder" ở **mọi** lượt có phí, ≥ 512 ở lượt bất kỳ ⇒ dừng | đóng |
| m-2 `P0_thieu` | Q2: chỉ số ghi trước, mới so B2 (9 câu) và so 01/11 (10 câu) — khớp `compare_main.json`; câu thiếu mới ⇒ sinh lại 3 lần; vẫn mới ⇒ báo A trước khi giữ D6 | đóng |
| m-3 phần kín | C chạy **và chấm** (sub-agent C, cùng prompt / thủ tục); B chỉ nhận số đếm + sha; cờ `--khong-in-chu` | đóng |
| m-4 tiền | cận dưới ≈ 0,17 (cộng lại khớp), trần 0,30 / dừng > 0,27 (A chốt) | đóng |
| m-5 D11 | D11 = (a) ghi rõ, bỏ (b); Q4 bên so = câu gõ thật không lịch sử, báo kèm trần cùng lượt mù; README `57c31a7110c5` | đóng |

Ghi nhận nhỏ (không mở vòng): mục "Căn cứ" còn dẫn report C136 sha `101fdade80eb`, bản hiện tại là `3301f3c7b7e3` (chỉ đổi câu chữ quyết 2 theo D11) — sửa khi tiện.

### Kết luận vòng 2

**`ready_for_user_confirmation`** cho plan B3 bản 2 `cd099ec0a00e`. A duyệt sha (tính từ file).
