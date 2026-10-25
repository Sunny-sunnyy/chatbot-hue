# Review: Phase 8.1 G5 — tổng hợp (A)

Decision: **changes_requested** (0 blocker, 2 major, 4 minor) — sửa chữ + một bảng tính từ JSONL đã lưu (0 USD)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 14:10 (`date`)
Report được kiểm: `phase_8_1_g5_synthesis.md` sha `c55e70d4e727` · đối chiếu: spec 8.1 §5 G5, §6; bảng G5
`phase_8_1_g5_decision_table_draft.md` (B19, sha `32d3be7f97f7`); report G0–G4K + review; `CURRENT_HANDOFF.md`.
Lưu ý độc lập: bảng G5 là của chính B; phần kiểm đó dựa trên report gốc, không dựa trên bảng.

## 1. Cổng tối thiểu

- File mới, untracked; không đổi code. Không có phần chạy lại cần (G5 là tổng hợp); B kiểm số bằng report gốc + lệnh grep.
- Số chính đối chiếu với report gốc **khớp**: context 10 dev +0,26 [+0,08; +0,48], test +0,27 [+0,02; +0,59] (G2 §4.1,
  §4.4); không dấu 13/32 → 1/32 (G4K §4.1); sparse@100 0,25 → 0,81 (G4K §4.3); luna MRR +0,17 (G4 §4.2); P1 13 → 1, 2 OOS
  (G2 §4.2); pool +4/−1 (G4 §4.4); nhiễu judge 2/88, cả đường 10/83 (G2 §4, §4.5); tiền B17 0,1653 (G2 §5).

## 2. Findings

- **M1 (major) — tiêu chí 2 ghi PASS nhưng thiếu phần "theo loại câu".**
  - Vị trí: §2 dòng 2. Spec §6 tiêu chí 2: "kết quả theo cặp (chênh, CI, thắng/hòa/thua, **theo loại câu**)".
  - Bằng chứng: `grep` tên loại câu (`direct_fact`, `multi_source`, `comparative`, "loại câu") trong report G1, G2, G3, G4,
    G4K: **0** dòng ở cả năm. Các report chỉ báo tổng + "chỉ natural" + nhóm (a)/(b).
  - Tác động: tiêu chí nghiệm thu 8.1 chưa đủ; User đóng 8.1 dựa trên dòng PASS này. Loại câu cũng quan trọng cho 8.2 (C11:
    comparative MRR 0,53, multi_source 0,54 là chỗ yếu).
  - **Đóng khi** (một trong hai): (a) thêm một bảng "theo loại câu" cho **chỉ số quyết** của mỗi gate có kết luận
    (tối thiểu: G2.1a context 10 dev + test; G4-A luna; G4-B; G3 H2 512; G4K E native) — tính từ JSONL đã lưu, 0 USD (B làm
    được nếu A giao); hoặc (b) ghi tiêu chí 2 là **PARTIAL** và nêu "theo loại câu chưa báo" vào mục lệch spec để User quyết
    chấp nhận.
- **M2 (major) — thứ tự đề xuất 8.2: mốc người đứng thứ 9 nhưng là điều kiện của mục 1 và 6.**
  - Vị trí: §4 mục 9 "Mốc người 20 câu trước khi quyết bằng điểm câu trả lời".
  - Bằng chứng: `CURRENT_HANDOFF.md` (câu hỏi cho User, mục 6) ghi "Trước quyết định 8.2 dựa vào điểm câu trả lời: nhắc chấm
    tay 20 câu (D6)". Mục 1 (context 10) và mục 6 (H8) **chỉ** có bằng chứng từ điểm judge Claude.
  - Tác động: đọc theo thứ tự hiện tại, 8.2 có thể đổi context trước khi có mốc người — ngược quyết định D6.
  - **Đóng khi:** mốc người đưa lên trước (bước 0) hoặc ghi rõ "mục 1 và 6 chỉ vào runtime sau khi có mốc người 20 câu";
    tương tự mục 10 "tách khâu dính **trước khi** thêm cải tiến" đang đứng cuối — đưa lên bước 0 hoặc bỏ chữ "trước".
- **m1 (minor) — danh sách lệch spec / plan chưa đủ.** Thêm:
  (i) G3 §10 B10 là thí nghiệm **thêm sau khi thấy kết quả H2** (tiêu chí vẫn ghi trước khi đo B10; kết quả kém hơn nên
  không thiên vị kết luận, nhưng nên ghi là bổ sung có lý do);
  (ii) luật tiền đổi giữa chừng (A 25/10: so với ước lại từ pilot thay vì ước plan, thêm trần lượt 0,05 / tổng B17 0,25)
  sau khi một lượt luna vượt 54% ước plan;
  (iii) judge mỗi sub-agent 40 câu (7B: 10) — cùng cho mọi biến thể nên không lệch, nhưng là đổi quy trình chấm;
  (iv) G3 build `hue_81_g3_h1` trước khi A duyệt §9 (chưa đo; A chấp nhận).
- **m2 (minor) — tiền: chỉ ghi phần của B.** §2 dòng 5 ghi 0,1653 USD (B17). Nên ghi tổng 8.1 theo từng session (B 0,1653;
  A …; C …; trước 25/10: 0) kèm nguồn, để tiêu chí 5 đọc được "cả 8.1".
- **m3 (minor) — thiếu sót của chính B, cần ghi.** Plan G2 §2 G2.2 có chỉ số phụ "claim không nguồn trên 32 câu" — **chưa
  đo** và report G2 bản trước không ghi NOT RUN. B đã bổ sung dòng NOT RUN vào `phase_8_1_g2_implementation.md` §6 (lúc
  14:10). G5 nên nhắc: bám nguồn (7B.2) vẫn chưa có số ở 8.1.
- **m4 (minor) — tên / trạng thái file bảng.** §0 gọi `phase_8_1_g5_decision_table_draft.md` là "bảng chính thức của G5";
  file vẫn ghi "nháp" trong tên + dòng trạng thái. Đổi một trong hai cho khớp (ví dụ đổi dòng trạng thái thành "chính
  thức, A review 13:5x").

## 3. Thứ tự đề xuất 8.2 — có lập luận được bằng số đo không

| # | Mục | Số đo đứng sau | Nhận xét |
|---:|---|---|---|
| 1 | Context 10 | dev + test, CI > 0 | mạnh nhất — **nhưng** chờ mốc người (M2) |
| 2 | NFC | G1.4 trên câu biến đổi máy; tất định | rẻ; lợi thật phụ thuộc tỉ lệ NFD thật (chưa biết) — ghi rõ |
| 3 | Câu không dấu | G4K: chỉ số phụ mạnh, chỉ số chính chưa rõ; câu biến đổi máy | đúng là lỗ hổng lớn nhất; thứ tự hợp lý vì cần thiết kế + câu thật |
| 4 | Build lại có dọn (H1, S1–S3) | **không khác** (không có lợi đo được) | lập luận bằng rủi ro thấp / vệ sinh, không bằng số; đề xuất gộp vào lần build của mục 3 hoặc 8 thay vì đứng riêng ở vị trí 4 |
| 5 | Pool + luna | +4/−1 câu; MRR +0,17 có CI | tín hiệu; hợp lý |
| 6 | H8 có chặn OOS | 13 → 1 từ chối nhầm, phạm sàn 2 câu | hợp lý; cần mốc người (M2) |
| 7 | Lỗi citation | P2 4 → 1 (phụ); G2.3 không chạm | hợp lý |
| 8 | Index 8B | **không có số đo ở 8.1** | theo spec, không theo số — ghi rõ |
| 9 | Mốc người | — | nên là bước 0 (M2) |
| 10 | Tách khâu dính | danh sách G5 §4 | nên là bước 0 nếu giữ chữ "trước khi" (M2) |

## 4. Phần đúng

- Kết luận một đoạn khớp số đo; tiêu chí 1 (PARTIAL: G0.4, G0.6), 3, 4 (kèm "kiểm lại lần cuối khi đóng") ghi đúng trạng thái.
- 4 lệch spec đã liệt kê đúng và có User / A duyệt.
- Giới hạn §6 đủ ý chính (cỡ mẫu, judge, câu biến đổi máy, test đã nhìn, câu kín chưa dùng, A đã thấy 3 câu kín).

## 5. Vòng 2 (synthesis sha `8833bffa4d00`)

| Finding | Kiểm | Kết quả |
|---|---|---|
| M1 theo loại câu | §2 tiêu chí 2 trỏ `phase_8_1_g5_by_category.md` (`1f630d9db100`), A chạy lại script 51/51 dòng khớp; §3 thêm hàng "Theo loại câu" — số khớp file của B (dev +0,71 / +0,64; test +0,83 n 6 mô tả; trực tiếp 1/42/1; H2 / B10 mất ở nhiều nguồn) | **đóng** (phạm vi: chỉ số quyết các gate chính — đúng phạm vi A giao) |
| M2 thứ tự 8.2 | thêm bước 0 (mốc người + tách khâu dính); mục 1 và 6 chỉ vào runtime sau mốc người | **đóng** |
| m1 lệch / đổi quy trình | thêm (5)–(9), đúng 4 mục B nêu + "theo loại câu bổ sung sau" | **đóng** |
| m2 tiền theo session | B 0,1653 / C 0 / A 0 / trước 25/10: 0 | **đóng** |
| m3 bám nguồn | §6 thêm "claim không nguồn NOT RUN" trỏ G2 §6 | **đóng** |
| m4 trạng thái bảng | dòng trạng thái bảng G5: "bảng chính thức của G5 (tên file giữ chữ draft để không gãy link)" | **đóng** |
| §3 nhận xét mục 4 | "dọn chunker" ghi rõ không có lợi đo được, gộp vào build của mục 3 / 8 | **đóng** |

Còn một chi tiết cũ, không chặn: §5 bước 4 ghi "đang làm: B20, C30" — cả hai đã review ready (B20: C, đóng; C30: B, 4 minor
chữ). Sửa khi A cập nhật lần sau.

**Kết luận vòng 2: ready_for_user_confirmation** (0 finding mở).
