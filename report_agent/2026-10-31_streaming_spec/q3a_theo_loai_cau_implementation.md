# Implementation Report: Q3a — đo lại L2 / L3 theo loại câu (plan đo cuối Phase 1–8 §4)

Người làm: B (Claude Opus 5.5)
Date: 11:56 01/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` — A duyệt **`ae8d42d520d4`** (commit `0a6340f`), §4 bước Q3a. Mục việc: tin A 01/11.
0 USD — chỉ đọc file kết quả đã có; không gọi API, không Qdrant, không server. Nhãn độ tin: **[một lần chạy]** (bộ "sau" đợt 2 sinh 1 lần, judge Claude).

## 1. Phạm vi

Đo lại hai lỗi đã biết của plan §4 trên **kho hiện tại** (bộ "sau" đợt 2 sửa kho, 30/10, commit `751b352`, build record `51fb1ec63cbc`): **L2** câu so sánh / nhiều nguồn, **L3** dòng bảng giá —
để biết lỗi nào còn lớn trước khi tốn công nghiên cứu. L1 (từ chối nhầm) không thuộc Q3a, chỉ ghi chỗ nó trùng L2. Không chọn biến thể, không đổi gì trong chatbot.

## 2. Thay đổi chính

Không đổi code / dữ liệu dùng chung. File mới (private): `data/q3a_2026-11-01/tieu_chi_ghi_truoc.md` (`86130244c355`, ghi **trước** khi tính), `tools/q3a.py` (`446b9fca93a3`),
`q3a_ket_qua.json` (`ca55ae1e047e`, số từng câu — private vì theo `case_index`).

## 3. Cách đã chạy thật

`cd backend && uv run python ../data/q3a_2026-11-01/tools/q3a.py`. Đầu vào: `data/sua_kho_2026-10-27/dot2/eval_sau/t1_sau.jsonl` (tầng tìm, 158 câu), `eval_sau/sau_all.jsonl` (câu trả lời
`sau_all` `45487ea1d88a`), `judge/` (điểm Claude bên "sau", cùng lượt mù với bên "trước"; ghép qua `judge/map.json` — đủ 176 câu), `eval_sau/chunks_sau.json` (vị trí phần bằng chứng
của 8.424 đoạn — chữ đoạn dựng lại từ file kho), nhãn đoạn đúng **v5** `33d16fd6b8f4` (cùng luật giao vị trí như W6 của harness đợt 2), Golden md5 `6331e88fb171`, nhãn độ tự nhiên
(số chính = bỏ 29 câu người thật ít hỏi). "Câu bảng" (L3) = câu có ≥ 1 keyword đáp án **chỉ** nằm trong đoạn dạng bảng (đoạn có ≥ 2 dòng bắt đầu bằng `|`).

**Kiểm chéo (bất biến):** từ chối nhầm cộng 4 loại = 1 + 8 + 0 + 3 = **12 / 158** (= mốc 30/10 `10_BAO_CAO_DANH_GIA.md` §1); câu có nhãn đoạn đúng cộng lại = **55** (= 40 + 15 nhãn v5) ✓.

## 4. Kết quả quan sát

**Theo loại câu — số chính (147 câu tự nhiên / năng lực; 129 trong kho):**

| Loại câu | n | MRR | Keyword @10 | Đủ keyword trong top-10 | Đủ đoạn đúng (câu có nhãn) | Đủ ý (Completeness) TB | Đúng (Accuracy) TB | Câu Đủ ≤ 3 | — trong đó thiếu bằng chứng ở tầng tìm | Từ chối nhầm |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Một dữ kiện | 66 | 0,804 | 97,7 % | 64 / 66 | 1 / 2 | **4,92** | 4,94 | 1 | 1 | 1 |
| **Nhiều nguồn** | 18 | **0,510** | 82,4 % | 12 / 18 | **8 / 16** | **3,50** | 3,78 | **8** | **8** | **5** |
| Có điều kiện | 25 | 0,801 | 94,0 % | 23 / 25 | 5 / 8 | 4,60 | 4,96 | 1 | 1 | 0 |
| So sánh | 20 | 0,510 | 82,5 % | 14 / 20 | 11 / 16 | 4,35 | 4,50 | 2 | 2 | 2 |

Cả 158 câu trong kho (không bỏ câu nào): nhiều nguồn MRR 0,543, Đủ 3,52, 13 câu Đủ ≤ 3 (cả 13 thiếu bằng chứng), từ chối nhầm 8; so sánh MRR 0,527, Đủ 4,32, 3 câu ≤ 3 (cả 3 thiếu bằng chứng).
MRR so với số cũ (24/10, kho cũ, 158 câu: so sánh 0,53 / nhiều nguồn 0,54 — `06_BAO_CAO_TIM_KIEM.md`) ⇒ **gần như không đổi** sau hai đợt sửa kho + context 10 (context 10 nâng khâu trả lời, không đổi xếp hạng).

**L3 — dòng bảng giá:** 144 / 8.424 đoạn có dạng bảng. **8** câu bảng (6 một dữ kiện, 1 có điều kiện, 1 so sánh; cả 8 thuộc số chính).

| | n câu | Keyword lọt top-10 | MRR | Đủ TB | Câu Đủ ≤ 3 |
|---|---:|---:|---:|---:|---:|
| Câu bảng | 8 | **8 / 10** keyword (80 %) | 0,569 | **4,50** | 1 |
| Câu khác (trong kho) | 150 | 270 / 299 (90,3 %) | 0,730 | 4,53 | 17 |

**Áp luật ghi trước** (`tieu_chi_ghi_truoc.md`, không đổi sau khi thấy số):

| Lỗi | (a) Đủ thấp hơn "một dữ kiện" ≥ 0,3 | (b) ≥ 5 câu Đủ ≤ 3 kèm thiếu bằng chứng | Kết luận theo luật |
|---|---|---|---|
| L2 — **nhiều nguồn** | ✓ −1,42 | ✓ 8 câu (cả 8 thiếu bằng chứng; 5 / 8 là từ chối nhầm) | **còn lớn — đáng thử hướng tìm** |
| L2 — **so sánh** | ✓ −0,57 | ✗ 2 câu | "(a) không (b)" ⇒ theo luật: **không phải hướng tìm** (xem ghi chú dưới) |
| L3 — **bảng giá** | ≥ 5 câu bảng ✓ (8); keyword lọt top-10 thấp hơn 10,3 điểm % (< 15) ✗; Đủ thấp hơn 0,03 (< 0,3) ✗ | — | **không còn lớn** |

**Ghi chú — quan sát, không phải kết luận theo luật:**
- Ở câu so sánh, luật ghi "(a) không (b) ⇒ lỗi ở khâu trả lời". Số thật cho thấy khác: cả **2** câu yếu đều **thiếu** bằng chứng (0 câu yếu có đủ bằng chứng); chênh −0,57 chủ yếu do nhiều câu
  4 điểm thay vì 5, không do lỗi khâu trả lời rõ ràng. Luật B ghi trước gộp hai trường hợp này — B ghi rõ để A / User không đọc nhầm thành "khâu trả lời hỏng".
- **L1 ↔ L2 cùng gốc:** 8 / 12 câu từ chối nhầm (cả 158 câu) là câu **nhiều nguồn**; mọi câu nhiều nguồn yếu đều thiếu bằng chứng trong 10 đoạn đưa model ⇒ thử một hướng tìm cho câu nhiều nguồn
  là thử luôn L1 (khớp kết luận 8.1: "22 / 22 câu từ chối nhầm thiếu dữ kiện trong ngữ cảnh").

**Gợi ý cho A trình User (theo plan §4: mỗi lỗi được chọn một plan riêng):**
1. **Đáng thử tiếp: L2 câu nhiều nguồn (gộp L1).** Hướng plan §4 đã ghi: xếp hạng / chọn đoạn rẻ, không thêm lần gọi model trên đường chính (tách câu nhiều vế thường thêm lần gọi ⇒ vướng sàn
   tốc độ). Đã thử và bỏ, không thử lại nếu không có lý do mới: pool 100, luna chọn 10 / 30, rerank GPU, small-to-big / gộp đoạn, Qwen3-8B, trả lời phần có căn cứ. Bước đầu: nghiên cứu ngoài
   (Codex + ChatGPT) với bối cảnh `file:dòng`.
2. **Không thử L3:** ghi "đo lại 01/11 trên kho hiện tại: không còn lớn (8 câu, 80 % ↔ 90 % keyword lọt top-10, Đủ 4,50 ↔ 4,53)" vào báo cáo so sánh; giữ giới hạn "mẫu câu bảng nhỏ".
3. **Câu so sánh:** không mở plan riêng theo luật; nếu thử L2 nhiều nguồn thì đo kèm câu so sánh (cùng bộ thước, theo dõi).

## 5. Lỗi và giới hạn

- Cỡ mẫu nhỏ: 18 câu nhiều nguồn, 20 câu so sánh, 8 câu bảng (10 keyword) ở số chính ⇒ chỉ là **gợi ý thứ tự**, không phải chứng minh; nhãn [một lần chạy], judge Claude, chưa có mốc người.
- "Thiếu bằng chứng" dùng thước tự động (keyword @10 hoặc đoạn đúng v5); câu không có nhãn đoạn đúng chỉ dựa keyword — keyword có thể có mặt mà ý vẫn thiếu (và ngược lại).
- "Câu bảng" nhận theo hình dạng đoạn (dòng `|`) + keyword; không phân biệt bảng giá với bảng khác (giờ mở cửa…), và câu hỏi giá mà keyword nằm ngoài bảng không được tính.
- Keyword lọt top-10 xét **10 đoạn của tầng tìm**; ngữ cảnh đưa model cũng là 10 đoạn (`context_sources` 10) nên trùng với "trong ngữ cảnh" ở cấu hình đang chạy.
- Luật (a)/(b) của B gộp "tụt dàn trải" với "lỗi khâu trả lời" (ghi chú §4) — nếu dùng lại luật này, tách hai trường hợp.

## 6. Bàn giao cho người kiểm

- Chạy lại (0 USD, tất định, ~1 phút): lệnh §3 ⇒ so `q3a_ket_qua.json` sha `ca55ae1e047e`. Bất biến kiểm: từ chối nhầm cộng = 12, câu có nhãn = 55.
- Ca dò khác cách gợi ý: đếm "câu bảng" bằng cách khác (vd. đoạn có ký tự `|` ở ≥ 50 % dòng) xem kết luận L3 có đổi không.

**Giải thích ngắn:** trước khi tốn công thử cải tiến, mình đo lại trên kho hiện tại xem hai lỗi cũ còn lớn không. Câu cần gom thông tin từ nhiều nguồn vẫn yếu rõ (điểm đủ ý 3,5 / 5 so với
4,9 ở câu hỏi một dữ kiện), và lý do là tầng tìm chưa đưa đủ đoạn cần thiết cho model — đây cũng là chỗ gây phần lớn các lần từ chối nhầm. Lỗi dòng bảng giá thì nay gần như hết. Nên nếu thử
thêm, chỉ nên thử một hướng: tìm đoạn tốt hơn cho câu nhiều nguồn.
