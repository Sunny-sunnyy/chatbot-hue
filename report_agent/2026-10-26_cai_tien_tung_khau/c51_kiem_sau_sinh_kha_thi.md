# C51 — Kiểm sau sinh cho lỗi "trả lời vòng + câu báo thiếu": có khả thi không? (đo trên dữ liệu đã ghi)

Người làm: C (Claude Opus 5.5, `hue-rag-5b`) · 2026-10-27 09:30 +0700 (`date`) · Việc: C51 (A giao). **0 USD**, không gọi API, không sửa code production.
Đọc mọi lượt sinh đã ghi thật (8.1 G2, B1, R2, R1). Dev đọc tay; test chỉ đếm tổng; không mở câu kín. File không chép câu hỏi, câu trả lời hay
nội dung kho — chỉ tên lượt, `case_index`, số đếm.

## Cho bạn (3 dòng)

- Một luật đơn giản bằng code bắt được **cả hai lỗi thật** đã làm dừng R2 (câu 160) và R1 (câu 168), và **không động tới câu trả lời nào** của chatbot hiện
  tại (0 / 99 câu dev, 0 / 47 câu test).
- Nhưng luật chỉ nhìn được **hình thức** ("một câu có nguồn + một câu nói nguồn không có…"). Nó **không phân biệt** câu lạc đề (lỗi) với câu trả lời
  **một phần nhưng có ích** (ví dụ trả lời đúng một nửa câu hỏi rồi nói nửa kia không có) — trong mẫu đọc tay, phần lớn cờ là loại có ích.
- Nghĩa là: luật này dùng được làm **rào cho R1** (giữ đúng hợp đồng "không đủ thì từ chối" như hiện nay), **không dùng được cho R2** (vì R2 muốn giữ chính
  các câu một phần có ích đó).

## 1. Luật đã thử

Script private `data/cai_tien_tung_khau_2026-10-26/c51/c51_scan.py` (chạy từ `backend/`: `PYTHONPATH=. uv run python ../data/cai_tien_tung_khau_2026-10-26/c51/c51_scan.py`;
cờ theo câu `c51_flags.jsonl` (dev), tổng `c51_summary.json`; từ chối ghi đè). Chỉ xét câu trả lời **không phải từ chối**, không lỗi.

- **Tách câu:** theo dòng, rồi tại dấu kết câu kèm các citation đứng ngay sau (model hay viết `.[2] Câu sau`); citation đi cùng câu trước; mẩu chỉ có
  citation (`. [1]` cuối dòng) gắn vào câu trước. Citation nhận cả `[n]` và `[Nguồn n]` (`llm/citations.py` `CITATION_PATTERN`).
- **Câu báo thiếu:** câu **không có citation** khớp một cụm phủ định về nguồn — "không nêu / không có thông tin / không đề cập / không cung cấp…", "chưa
  xác định / chưa rõ…", hoặc "nguồn / dữ liệu / tài liệu / bằng chứng / thông tin được cung cấp … không|chưa …".
- **L1:** câu trả lời có ≥ 1 câu có citation **và** ≥ 1 câu báo thiếu.
- **L2:** L1 **và** chỉ có **≤ 1 câu có citation** (phần có căn cứ chỉ một ý).

**Chỉnh trên chính mẫu mục tiêu (ghi trung thực):** bản đầu bỏ sót cả 160 và 168 — (1) tách câu sai khi `[n]` đứng sau dấu chấm; (2) cụm "nguồn dữ liệu
không có mức giá…" ngoài danh sách. Bản cuối sửa hai chỗ đó, và sửa thêm một báo nhầm do tách câu (B1 câu 25). Vậy **độ nhạy 2 / 2 là trên mẫu đã dùng để
chỉnh**, chưa phải ngoài mẫu.

## 2. Kết quả theo lượt (script in, `c51_summary.json`)

| Lượt | Nhóm | Câu trả lời (không từ chối) | Cờ L1 | Cờ L2 |
|---|---|---:|---:|---:|
| `g20_baseline` (ctx 5, prompt hiện hành) | dev | 92 | 1 | 1 |
| `g2_context10` (G2.1a) | dev | 99 | 0 | 0 |
| `g2_doc_order` | dev | 92 | 0 | 0 |
| `g2_p1_partial` (P1 "trả lời một phần") | dev | 109 | **18** | **13** |
| `g2_p2_spec_rules` | dev | 93 | 0 | 0 |
| `g24_none` | dev | 103 | 5 | 5 |
| `g24_low` | dev | 97 | 3 | 3 |
| `g24_high` | dev | 93 | 2 | 2 |
| **`b1_dev` (chatbot hiện tại, ctx 10)** | dev | 99 | 1 (câu 70) | **0** |
| `r2_oos_dev` (R2) | dev OOS | 1 | **1 (160)** | **1 (160)** |
| `r1_oos_dev` (R1) | dev OOS | 0 | 0 | 0 |
| `r1_early` (R1) | dev | 11 | **1 (168)** | **1 (168)** |
| `t_baseline`, `t_context10`, `b1_test` | test | 44 / 47 / 47 | 0 / 0 / 0 | 0 / 0 / 0 |

Cờ gom lại ở dev: L1 32 cờ trên 18 câu khác nhau; L2 26 cờ trên 14 câu. Dạng này gần như chỉ xuất hiện khi prompt / mức suy luận **nới** chuyện từ chối
(P1, `none`, `low`); prompt hiện hành gần như không sinh ra nó.

**So với mốc cùng context** (script `c51_vs_base.py`: mốc ctx 5 = `g20_baseline`, ctx 10 = `b1_dev`): trong 26 cờ L2, **21 cờ ở câu mà mốc đang từ chối** — nếu
luật đổi các câu này thành câu từ chối, hành vi chỉ **trở về như mốc**. 5 cờ L2 ở câu mà mốc đang trả lời: câu 70 (3 lượt), 159, 19 — đây là chỗ luật có thể
làm hại so với hiện tại.

## 3. Đọc tay

Ghi chép private `data/cai_tien_tung_khau_2026-10-26/c51/doc_tay.md`. Nhãn do **một người** (C).

- **Hai cờ ở chatbot hiện tại:** câu 25 — báo nhầm do tách câu, đã sửa luật (hết cờ). Câu 70 (chỉ L1) — câu trả lời **đúng đủ** kèm một câu lưu ý có ích về
  nguồn ⇒ **báo nhầm của L1**; L2 không cờ.
- **Mẫu seed 20261024, 10 / 29 cờ khác** (bỏ 160, 168, B1 25 / 70):

  | Loại | Số | `case_index` (lượt) |
  |---|---:|---|
  | đúng dạng mục tiêu (thông tin cùng chủ đề, không trả lời điều hỏi) | 1 | 97 (P1) |
  | lưng chừng (không trả lời thẳng, có gợi ý liên quan) | 2 | 159 (`g24_high`), 143 (P1) |
  | **một phần có ích** (trả lời đúng một phần, nói rõ phần thiếu) | 5 | 167 (`g24_low`), 48 / 154 (`g24_none`), 68 / 85 (P1) |
  | **đúng đủ kèm lưu ý có ích** | 2 | 70 (`g20_baseline`, `g24_high`) |

  ⇒ Nếu luật dùng để **chặn** (đổi thành câu từ chối), trong mẫu chỉ 1–3 / 10 cờ là chặn đúng; 7 / 10 là chặn mất nội dung có ích (5 một phần + 2 đúng đủ).

## 4. Kết luận khả thi

- **Quan sát:** L2 bắt 2 / 2 lỗi đã biết (trên mẫu đã chỉnh), **0 cờ** ở chatbot hiện tại (dev 99, test 47). L1 thêm 1 báo nhầm ở chatbot hiện tại (70).
- **Vì sao không phân biệt được:** "lạc đề + báo thiếu" và "một phần có ích + báo thiếu" có **cùng hình thức**. Khác nhau ở chỗ phần có citation có trả lời
  điều được hỏi không — đó là câu hỏi về **nghĩa**, luật từ vựng không thấy.
- **Dùng cho R1 (*đề xuất*, A quyết có viết plan không):** ghép R1 `none` + L2 làm bước kiểm sau sinh: câu bị cờ ⇒ trả câu từ chối chuẩn. Ở chatbot hiện tại
  luật không đổi gì (0 cờ); với R1 nó đưa câu kiểu 168 về đúng hợp đồng "không đủ thì từ chối". Cái giá: các câu R1 trả lời một phần có ích cũng thành từ chối —
  nhưng đó **đúng là hành vi hiện tại** (mốc đang từ chối 21 / 26 câu bị cờ). Rủi ro còn lại: dạng câu 70 (đúng đủ + lưu ý, gộp trong 1 câu có citation) bị chặn
  nhầm — 3 lần trong 8.1, 0 lần ở B1. Đây là **biến thể mới** (đổi hai thứ so mốc: mức suy luận + bước kiểm), cần plan riêng, đo lại độ nhạy ngoài mẫu.
- **Không dùng được cho R2:** R2 muốn giữ câu một phần có ích; luật này chặn chính chúng. Muốn tách "lạc đề" khỏi "một phần có ích" cần kiểm theo nghĩa (ví dụ một
  lần gọi model chấm "phần có nguồn có trả lời điều hỏi không") — thêm lần gọi API, thuộc luật "tốn hơn ⇒ trình User"; chưa đo.
- **Giới hạn:** độ nhạy chỉ đo trên 2 câu đã dùng để chỉnh luật; mẫu đọc tay 10 câu, một người gắn nhãn; dev only; câu kín không chạm.
