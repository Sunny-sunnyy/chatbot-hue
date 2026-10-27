# STATUS C — mở phiên 08:40 27/10/2026 (chờ A giao việc; trạng thái kết phiên tối 26/10 ở dưới, giữ nguyên)

Terminal: **`hue-rag-5b`** (mở 08:40 27/10/2026; tối 26/10 là `hue-rag-b5`; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-5f`, B = `hue-rag-31` (27/10, trực tiếp; A xác nhận).
User tối 26/10 (20:3x): C làm việc trực tiếp với A; A giao việc = "làm đi". Quyền phiên tối 26/10 (C commit + push `p82-r2`, paid ≤ 0,06 USD cho R2)
**hết hạn cuối phiên**.

## Mở phiên 08:40 27/10/2026

Kiểm nhanh khớp: `main` `c81e45e`, sạch (2 mục untracked của User), hooksPath `.githooks`, Qdrant 1 × 8.459; `origin/p82-r2` = `aec9ab8`; K3 plan sha `0a6370204c7d` khớp; chưa có `p82-k3`; không còn `/tmp/b_*`, `/tmp/c_*`. Quyền phiên tối 26/10 đã hết ⇒ chờ A hỏi User + giao việc. Không khai báo file nào.

**User 08:41 27/10/2026:** C làm việc trực tiếp với A, báo cáo cho A; việc A giao = User nói "làm đi".

A trả lời: plan R1 viết song song K3 (không chờ kết quả K3), **chỉ bắt đầu khi A nhắn "làm đi"**; R1 so mốc B1 `811d25d`; file `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md` ở working tree chung, đầu file có mục "Căn cứ để review" (WORKFLOW §9.1).

**C46 (A giao 'làm đi', 08:52 27/10/2026) — khai báo file:** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md` (mới, working tree chung, không commit); private `data/phase_8_2/r1_plan/` (script tính số mốc). 0 USD.
**C46 xong 08:54 27/10/2026: plan R1 sha `0a702b4ac1e4` (tính từ file) — chờ B review ⇒ A duyệt sha.** 0 USD; quét trùng 0. Plan hỏi A 3 câu (§6: mức tụt C thêm; quyền `p82-r1` + ≤ 0,05 USD; thời điểm chạy so với K3). **Đã báo sha ⇒ không sửa plan nữa** (luật A 22:1x 26/10). R2: B53 ready, A đóng kém hơn (`8010fda`).
**A trả lời 08:55 27/10/2026:** sha khớp; B55 = B review plan R1. Q1 giữ mức tụt chặt hơn; Q2 quyền có **sau khi B review + A ghi duyệt sha**: C commit + push `p82-r1` (không merge), worktree `/tmp/c_r1`, ≤ 0,05 USD, judge sub-agent; Q3 chạy sau pilot K3, report ghi giờ chạy (chồng thời gian với K3); §5 R1 qua cũng trình User. Trong lúc chờ: sẵn sàng review K3.
**C47 xong 08:57 27/10/2026** (đối chiếu yêu cầu ChatGPT mục tiêu sản phẩm; chỉ đọc; kết quả trong tin gửi A, không ghi file tracked).
**Khai báo 08:57 27/10/2026 (A cho phép sau C47):** worktree `/tmp/c_r1`, nhánh cục bộ `p82-r1` từ `811d25d`; file mới `backend/experiments/phase_8_2/r1.py` (trên nhánh). 0 USD, chưa commit / push, không chạy lệnh có phí.
**Harness R1 viết xong 09:00 27/10/2026** (`/tmp/c_r1/backend/experiments/phase_8_2/r1.py`, untracked trên `p82-r1`): kiểm 0 USD — import, tập câu 12 + 11 + 97 = dev 120, 10 + 46 = test 56, `ratio(B1, B1)` = 1, quét trùng 0. Chưa chạy lệnh có phí. Chờ B55 + A duyệt sha. Worktree giữ tới khi xong R1 (symlink `data`, `knowledge-base-hue` gỡ trước commit).
**C48 (A giao 09:01 27/10/2026) — khai báo file:** private `data/cai_tien_tung_khau_2026-10-26/c48/` (script + kết quả theo câu); report `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md` (mới, working tree chung, không commit). 0 USD, chỉ B1 dev, không test từng câu / câu kín.
**C48 xong 09:10 27/10/2026:** 4 / 68 câu có số bị cờ (= R4), đọc tay 6 / 6 cờ là phép tính đúng; mẫu 10 câu không cờ 10 / 10 đúng ⇒ 0 lỗi số thấy được. Report untracked, quét trùng 0.
**B55 = changes_requested (0/1/3)** — sửa plan R1 sau C49. **C49 (A giao 09:10 27/10/2026, ưu tiên):** review report K3 (`origin/p82-k3` `80e7329`) ⇒ `phase_8_2_k3_review.md` working tree chung.
**C49 xong 09:13 27/10/2026:** ready_for_user_confirmation (0/0/3 minor) — K3 kém hơn đúng luật; tiền 0,0251129 khớp; 9 / 0 trên 39 tính lại khớp. Script `data/phase_8_2/k3/tools/c49_check.py`. Tiếp: sửa plan R1 theo B55.
**Plan R1 bản 2 xong 09:16 27/10/2026: sha `8e76e77e0448`** (bản 1 `0a702b4ac1e4`; sửa M-1, m-1..m-3 B55: 172 / 173 vào pilot, sàn API 500 ghi trước, citation v2 tụt chỉ đếm lỗi khác "no citation", U 6 / 9 ở B1, từ chối mới đếm câu). Harness `r1.py` sửa khớp (early 12 câu). Chờ B kiểm phần sửa ⇒ A duyệt. **Đã báo sha ⇒ không sửa plan nữa.**
**C50 xong 09:20 27/10/2026:** review plan K3b (sha `4f92e478cb65`) ready (0/0/4 minor) — `phase_8_2_k3b_plan_review.md`. **A duyệt plan R1 bản 2 `8e76e77e0448` (`78a5f05`)**; quyền C: commit + push `p82-r1`, ≤ 0,05 USD, judge sub-agent. Tiếp: chạy R1.
**R1 chạy 09:25 27/10/2026: KÉM HƠN — phạm sàn ở pilot** (câu 168, từ chối đúng ở B1, bị trả lời vòng: thông tin cùng chủ đề có `[n]` + câu không citation "nguồn không nêu…" — cùng dạng R2 câu 160). OOS 12 / 12 từ chối; 0 API 500 (172, 173 có `[n]`). Dừng theo plan §3 bước 2. **0,0049030 USD thật.** `origin/p82-r1` `63a472f` (harness `d2646e6` + report). Worktree `/tmp/c_r1` đã gỡ (symlink + worktree). Dữ liệu `data/phase_8_2/r1/`. Chờ B review report + harness.
**C51 (A giao 09:26 27/10/2026) — khai báo file:** private `data/cai_tien_tung_khau_2026-10-26/c51/`; report `report_agent/2026-10-26_cai_tien_tung_khau/c51_kiem_sau_sinh_kha_thi.md` (mới, working tree chung). 0 USD, chỉ đọc lượt đã ghi; dev đọc tay, test chỉ đếm tổng.
**K3b bản 2 vòng 2 ready** (`57dad7150322`, mục Vòng 2 trong review). **C51 xong 09:31 27/10/2026:** L2 bắt 160 + 168 (trên mẫu đã chỉnh), 0 cờ ở B1 dev / test; mẫu 10 cờ khác: 7 / 10 là nội dung có ích ⇒ dùng được làm rào cho R1 (về đúng hợp đồng từ chối), không cho R2. Report untracked, quét trùng 0.
**A 09:33 27/10/2026:** C51 commit `8dad0cd`; A gác hướng R1 + L2 (lợi nhỏ, luật khớp từ 2 câu lỗi, đổi hợp đồng Phase 6). **R1 đóng: kém hơn** (B58 ready, `d665a5b`). K3b-n kém hơn (lỗi kỹ thuật: luna viết thêm chữ sau JSON); B sửa harness rồi chạy K3b-m. **Việc kế của C: review report K3b (n + m) + commit sửa harness.** Đang rảnh có lý do; không tự mở việc mới.
**C52 xong 10:05 27/10/2026:** review report K3b (`origin/p82-k3b` `806e8ad`) ready (0/0/3 minor) — n kém hơn, m tầng tìm tốt hơn (tạm): 9/0 dev ổn định, 3/0 test, 0/95 sai hợp đồng — C tính lại `context_gold_all` từ payload: khớp; tiền log 0,0592176 khớp; m-1 cận trên ước n không chặt (≈0,044). Script `data/phase_8_2/k3b/tools/c52_check.py`. File `phase_8_2_k3b_review.md` (untracked).
**C53 xong 10:10 27/10/2026:** review phụ lục K3b-m (`84d4aaf0ad04`) changes_requested (0/1/3) — M-1: `chat.py:125-135` trả 500 cho MỌI lỗi citation ⇒ T6 "+2" mâu thuẫn T2 sàn 0 / spec §10.2 (lỗi định nghĩa này cũng có trong plan R1 bản 2 của C — R1 đã dừng, không ảnh hưởng). File `phase_8_2_k3b_m_answer_plan_review.md`.
**Bẫy / học:** định nghĩa sàn "500" phải đối chiếu đúng nhánh trả lỗi trong `chat.py`, không suy từ tên lỗi validator (plan R1 C46 và B55 đều bỏ sót).
**Phụ lục K3b-m bản 2 vòng 2 ready 10:15 27/10/2026** (`92a8a7eb4177`); m-4 mới: regex W2 tách rời ". [1]" (43/99 câu B1) — sửa trong harness.
**Phụ lục bản 3 vòng 3 ready 10:33 27/10/2026** (`2a3b22b38ab6`): 120 về theo dõi; C xác nhận độc lập (a) context K3b-m của 120 có 2 / 2 fact, (b) B1 0. Pilot bản 2 dừng vì sàn 120 — sàn đó từ gợi ý m-2 của C.
**Bẫy / học (C, 27/10):** (1) nhãn đoạn đúng chỉ đánh dấu MỘT chỗ cho mỗi fact ⇒ `*_gold_frac` 0 không có nghĩa context không có fact; trước khi đề xuất sàn "context 0 fact" phải đọc nội dung (m-2 C53 ⇒ pilot bản 2 dừng oan). (2) Script dựng lại context chạy từ working tree `main` (context 5) phải truyền `max_documents=10` cho mốc B1 / K3b — suýt kết luận sai trên 5 đoạn.
**C54 xong 10:51 27/10/2026:** review K3b-m answer (`a6f609c`) ready (0/0/2 minor) — kém hơn đúng luật (T3 5 > 4: 26, 66, 93, 112, 134); sàn + T4/T5/T7 đạt; chỉ báo TB tăng CI > 0; tiền 0,0749297 khớp; e2e p50 6,5 s / p95 9,1 s. m-1: 66 nhiều khả năng nhiễu judge. C khuyên không chạy A/A biến thể (giá trị thấp), trình User câu hỏi luật nhận. Script `data/phase_8_2/k3b/answer/tools/c54_{check,read}.py`.
**C55 (A giao 11:16 27/10/2026) — khai báo file:** `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md` (bản 10; working tree chung, chưa commit, A review). User chọn chốt đợt cải tiến ⇒ B0 ⇒ merge context 10.
**C55 xong 11:19 27/10/2026:** bản 10 viết xong (Tóm tắt, checklist 4 dòng sửa + 3 dòng mới, §4 mục 27/10, §5 3 dòng, §6 viết lại, phụ lục); quét trùng 0; chờ A review.
**A 11:21 27/10/2026:** BAO_CAO_SINH bản 10 review tốt; A sửa câu 168 tả quá cụ thể. **Đợt đóng; C chờ B0 của User** (không có việc).
**Bẫy / học (A nhắc, 27/10):** report tracked (repo public) tả câu dev ở **mức loại câu**, không nêu chủ đề cụ thể (tên nơi, món, loại giá…) cạnh `case_index`. C rà lại file mình viết hôm nay 11:21 27/10/2026: sửa 2 chỗ (C48 §3 dạng phép tính theo câu; review phụ lục K3b-m vòng 3 tên fact của câu 120) — untracked diff, A commit.
**C56 (A giao 11:32 27/10/2026) — khai báo file:** private `data/phase_8_2/gold_fix_proposal_2710/{proposal.jsonl, ghi_chu.md, tools}`; report `report_agent/2026-10-26_cai_tien_tung_khau/c56_de_xuat_sua_nhan.md` (mới). Không sửa `gold_draft.jsonl`. 0 USD.
**C56 xong 11:37 27/10/2026 +0700:** 120 thêm 2 khoảng, 156 thêm 1 (khác B61), 143 không thêm — đếm thiếu do tiêu đề mục (đổi hàm đếm, A/User quyết); test 95/130/138 chưa quyết. Áp đề xuất: B1 22→23, K3b-m 31→32, thắng vẫn 9 / thua 0. gold_draft không đổi (`bab707b9ab22`).
**A 11:38 27/10/2026:** C56 commit `7a4e86c`. **Việc kế của C: review report B65 (latency đầu–cuối)** — 4 điểm: câu hỏi không lấy từ Golden (quét overlap), điều kiện đo hai bản giống nhau, p50 / p95 tính lại được, tiền đúng. Đang chờ B65. B sẽ kiểm đề xuất nhãn C56 sau B65.
**C57 xong 11:49 27/10/2026** (trả lời bằng tin nhắn): B65 đạt mọi điểm đo (câu hỏi 0 trùng, điều kiện giống, p50/p95 khớp, tiền ghi ước); cần sửa câu "K3b-m thêm ≈ 3 s" ⇒ cùng câu + cùng harness là ≈ +4,6–4,7 s p50 (chọn đoạn 4,6 s), qua API ước ≈ 8 s p50. Minor: chatbot hiện tại qua API p95 5,7–6,2 s > mức theo dõi 5 s.
**C58 (A giao 11:53 27/10/2026) — khai báo:** worktree `/tmp/c_lat` (detached `main`, chỉ thêm đo thời gian tạm, không commit, gỡ khi xong); private `data/phase_8_2/latency_2710/c58/`; report `report_agent/2026-10-26_cai_tien_tung_khau/c58_latency_theo_khau.md`. Paid ≤ 0,01 USD; cổng 8014.
**C58 xong 12:00 27/10/2026:** gọi model chiếm ≈ 98 % thời gian (tìm ~40 ms, ngữ cảnh ~2 ms, HTTP ~2 ms); khoảng dư 1,5 s = bộ câu khác (câu tự viết ra ~1,8× token ⇒ +1,1 s; cùng câu dev API ≈ harness). Không có chỗ thừa để cắt; đề xuất nhỏ: log token + thời gian theo khâu ở /api/chat. **0,0074884 USD thật.** Worktree `/tmp/c_lat` đã gỡ, server 8014 đã tắt.
**12:06 27/10/2026:** C58 sửa nhãn theo B67 (token ra = "giải thích được, chưa can thiệp"; 0,2 s = giả thuyết; "token do generator trả về") — sha `d76fb10e0c5a`. **C59 plan log token xong** — `report_agent/2026-10-26_cai_tien_tung_khau/c59_log_token_plan.md` sha `3cafe700ccec`, chờ B review; chưa sửa code.
**12:14 27/10/2026:** C59 plan bản 2 (sửa B68 M-1, M-2 theo A: một điểm ghi try/except/finally, `_answer` giữ thân cũ; m-1..m-3) — sha `7f1456a1ae55`; chờ B kiểm phần sửa. **Đã báo sha ⇒ không sửa nữa.**

## Còn treo (phiên sau xử lý trước)

1. ~~Report R2 chưa commit / chưa push~~ — **xong 22:25 26/10/2026**: User chạy `!` ⇒ commit `aec9ab8`, `origin/p82-r2` = `aec9ab8`; worktree `/tmp/c_r2` đã gỡ (nhánh `p82-r2` giữ, không merge).
2. B review report R2 (A giao) — chưa có.

## Đã làm tối 26/10 (theo thứ tự; 0 USD trừ C43)

| Việc | Kết quả | File |
|---|---|---|
| Mở phiên 20:29 | kiểm nhanh khớp (main `3cf8781`, hooks, Qdrant 1 × 8.459) | — |
| **C36** phân loại lỗi tầng trả lời (ctx 10, 88 câu dev chính) | 10 câu bị cờ, **cả 10 thiếu bằng chứng**; 5 từ chối khi có một phần fact (20 / 46 điểm); 9 trả lời gọn (điểm 4). A ready (`2d56193`) | `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md` |
| Review **W16** hook quét trùng + luật sổ cải tiến | vòng 1: 1 major (worktree không symlink ⇒ hook im lặng bỏ qua) — vòng 2 ready (`018c8dc`) | `…/governance_w16_review.md` |
| **C37** bản nháp khâu trả lời | R1 `none`, R2 = E1b, R3 "nêu đủ chi tiết", R4 thước số; E2 NOT RUN | `…/de_xuat_khau_tra_loi_C.md` |
| **C38** review spec 8.2 §10 | vòng 1: 4 major (Holm vs cỡ mẫu; K2 dùng lại dev đã thấy; luật (i) thiếu mức tụt; "không chờ B0") — vòng 2 ready | `…/spec_8_2_s10_review.md` |
| **C41** review plan K1 | vòng 1: 1 major (test thiếu mức tụt) — vòng 2 ready (C tự tính A/A test khớp B) | `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_plan_review.md` |
| **C39** R4 thước "số trong câu trả lời có trong đoạn được trích" | bắt 2 / 2 lỗi thật đã biết, nhầm 1 / 3 (trên mẫu đã thấy); ngoài mẫu 0 / 5 thật ⇒ chỉ là danh sách đọc lại. B47 ready; A commit `2c7ecfd` | `backend/experiments/phase_8_2/r4_numbers.py`, `backend/tests/test_r4_numbers.py`, `…/phase_8_2_r4_implementation.md` |
| **C40** plan R2 (thay plan E1) | B49: 1 major (latency khâu sinh không đo được ±50 ms ⇒ đổi sang `output_tokens`); A duyệt `b70ea775efb2` (`08419c0`) | `…/phase_8_2_r2_plan.md` |
| **C42** review report K1 | **K1 kém hơn xác nhận** (chạy lại độc lập 108 / 108 giống; mất câu 154) | `…/phase_8_2_k1_review.md` |
| **C43** chạy R2 | **KÉM HƠN — phạm sàn bước 1**: OOS dev câu 160 bị trả lời (11 / 12), cùng dạng lỗi P1 8.1. Dừng đúng plan. **0,0026861 USD thật**. A gác hướng R2 (hướng mở) | `p82-r2` `0cbad2d` + report chưa commit (mục trên); `data/phase_8_2/r2/` |
| **C44** review plan K3 | ready (0 / 0 / 2 minor: ghi trước `max_output_tokens` luna; số p95) | `…/phase_8_2_k3_plan_review.md` |
| **C45** review plan R3 | changes_requested: **trần thật ở mốc B1 = 6 câu U**, không phải 9 ⇒ A: **R3 NOT RUN** (hướng mở: mở rộng bộ câu tự nhiên) | `…/phase_8_2_r3_plan_review.md` |

## Phiên sau C làm gì đầu tiên

Mở theo `START_SESSION.md`, báo A, **chờ A giao việc**. Mục "Còn treo" chỉ còn B review report R2. Việc có thể tới lượt C:
1. Review report K3 (B chạy, nếu A duyệt sha) hoặc report R2 vòng B review (C sửa nếu có finding).
2. **R1** (`none`, luật (a)) — plan chưa viết; đứng cuối thứ tự "chất lượng trước" (spec §10.3).
3. Hướng mở đã ghi: R2 (cách mới phải được kiểm trước trên câu 160); R3 (cần bộ câu lớn hơn). C32 rà kho: chờ User.

## Đã xong phiên 26/10

- Đợt 3 sửa code (gói 2 + gói 5 + B-12): rebase `dot3` lên `main` `71d2450`, làm commit 4–12 + docs B-18; 12 commit code `3a37af4 … 8f0e5c4` (37 file, +289 / −2.711),
  report `report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md`; B review `sua_dot3_review.md` ready (0 / 0 / 3 minor — m-1, m-2 C sửa, m-3 A);
  A merge `421c302` + cổng ổn định trên `main` đạt, push `7b662c9`.
- Kết quả: danh sách đoạn toàn kho, T1 tìm kiếm, chuỗi gửi model 25 câu, 8.459 `PointStruct` đều giống byte; code `backend/` 8.345 → 6.218 dòng; test không key
  197 passed / 1 failed + 4 error (đúng phần cần key); `git ls-files knowledge-base-hue` rỗng, 0 chuỗi kho trong file tracked; T-C (User `!`) 1 passed hai lần.
- Script + ghi chép (private): `data/ra_soat_code_2026-10-25/tools/dot3/` (`notes_26_10.md`, `b12_move_samples.py`, `b02_points.py`, `gate.py`, d1/d4/d7/d8/d9).
  File private mới: `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json (sha 3013c24fd8f4), backup_b12_2026-10-26/}`,
  `data/tools/huegov_converters/`. Tạm `/tmp/c42/` đã xóa 16:19.
- **C chưa đọc nội dung câu kín** (md5 `ddc59587b502`, manifest `9ea480d0d083`).

## Câu hỏi / thắc mắc còn treo (cho A / User)

- **R1 (`none`, luật (a))**: plan chưa viết; ai viết / khi nào (spec §10.3 xếp cuối nhánh trả lời). Thay ý "3c xác nhận `none` trên test" cũ.
- **K3**: A duyệt plan `0a6370204c7d`; chạy khi User chọn giờ (B làm). Nếu cần review report K3 ⇒ C.
- **Hướng mở** (A ghi): R2 — chỉ quay lại với cách mới đã kiểm trước trên câu 160; R3 — cần bộ câu tự nhiên lớn hơn (trần 6 câu ở mốc B1).
- C32: `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index — loại ở lần build lại?
- Ghi chú cũ (đợt 3, A nhận ở m-3): guide 5 `:65` còn nhắc MiniLM của service; `guides/full_corpus_rag.md` bước 4b "cutover cần sửa code (B-06)"
  dùng mã B-06 của B26 (khác B-06 của plan đợt 3).
- Đã hết (không còn hỏi): plan E1 Q1–Q3 (thay bằng plan R2, đã chạy); xóa nhánh `dot3` (User 20:4x đồng ý xóa).

## File private C tạo phiên 25/10 (không commit; phiên 26/10 ở mục "Đã xong")

- `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `brief_common.md`, `nguon_count.py`, `cite_shapes.py`, `recheck_both.py`,
  `c01_probe_*.py`; thư mục `kiem_cheo_C/`, `review_4/`, `review_1b_plan/`, `review_1b/`, `sua_1a/`, `sua_3/`, `citation_v2/`, `dot3_plan/`); `data/ra_soat_code_2026-10-25/citation_v2/`.
- Trước đó: `data/ra_soat_kho_2026-10-25/` (C32), `data/phase_8_2/e1_plan/` (C33).
- Tạm: `/tmp/c34`, `/tmp/c34x`, `/tmp/c35`–`/tmp/c42` (mất khi tắt máy; không nội dung private ngoài số đếm).

## Ý cải tiến (A xin danh sách sau 5 gói — chỉ là ý, chưa thử; bản đầy đủ `ung_vien_cai_tien_C.md`)

- **Route API ghi usage (token, latency, số nguồn) mỗi câu vào log** — cổng ổn định gói 3 / 1b / đợt 3 đều phải **ước** tiền; không ghi nội dung câu hỏi.
- **Nhãn context `[Nguồn n]` ↔ prompt `[n]`** (C-09): thử khớp nhãn — thí nghiệm, đo lỗi "không ngoặc số" (14 / 1.600) + Completeness.
- **14 câu "không có ngoặc số"** còn lại sau 1a đều ở context 5 nguồn — xem có phải câu liệt kê / một ý.
- **Bộ đếm token context nhận instructions** khi harness đổi prompt (C-03 phần 2) — khi 8.2 E1 cần.
- **Kiểm token mỗi đoạn tốn gấp đôi thời gian chia nếu không nhớ kết quả** (đợt 3 commit 2) — đã cache; nếu sau này đổi chunker, đo lại thời gian.

## Đã học / bẫy gặp (đầu vào vòng cải tiến)

- **26/10 tối C43: auto mode chặn lệnh ghép `rm` symlink + `git add` + `git commit` + `git push` trong worktree `/tmp`** ("không đánh giá được", sẽ chặn suốt hội thoại) ⇒ report R2 kẹt untracked trong `/tmp`. Bài học: commit file report **ngay khi viết xong, tách riêng** khỏi `push` (bẫy §8 đã có: push từ worktree bị chặn ⇒ push từ working tree chung hoặc User `!`); report của nhánh thí nghiệm có thể viết ở working tree chung `main` (như review) để không phụ thuộc `/tmp`.
- **26/10 tối C45: giả định "câu U còn điểm 4 ở mốc mới" kiểm được 0 USD từ judge mốc nhưng plan để "kiểm sau khi chạy"** — khi đổi mốc (G2.1a → B1), đếm lại trần trên **đúng mốc** trước khi ước cỡ mẫu (9 → 6 câu).
- **26/10 tối C40: sửa plan R2 (ghi chú chữ của B) sau khi đã báo sha cho A** ⇒ A ghi duyệt `aa808a85184c` trong commit nhưng file trên đĩa đã là `b70ea775efb2`; phải dựng lại diff để chứng minh chỉ đổi chữ. Luật A 22:1x: **đã báo sha thì không sửa plan nữa**; ghi chú chữ đến sau ⇒ gom vào lần sửa kế, hoặc báo A trước khi sửa.
- **26/10 tối C41: báo nhầm "khối lặp" trong plan K1 vì in file bằng nhiều `sed -n '/mẫu/,$p'` nối nhau** — mẫu khớp cả dòng đầu file nên đoạn in chồng lên nhau, C tưởng file bị lặp (B chỉ ra, C rút lại). Kết luận về cấu trúc file: kiểm bằng `grep -n '^## '`, không bằng output `sed` ghép.
- **26/10 tối C36: chạy script phân tích bằng `python3` hệ thống** (`c36_labels.py`, quét / xem dữ liệu) thay vì `uv run python` — lệch §10 dù script chỉ dùng thư viện chuẩn;
  A bắt ở review (minor). Mọi lệnh Python của dự án, kể cả script tạm chỉ đọc: `uv run python …` từ gốc repo hoặc `backend/`.
- **26/10 C4: nối lệnh quét trùng với `git commit` bằng `;` ⇒ commit chạy dù quét exit 1** (dòng bị cờ là chuỗi có sẵn, không lộ thêm — nhưng là may).
  Quét là một bước riêng: chạy, đọc kết quả, rồi mới `git add` / commit; nếu nối thì dùng `&&`.
- **Đổi literal hàng loạt trong test: viết script AST + kiểm ngược round-trip** (thay lại ⇒ đúng file gốc từng byte) thay vì sửa tay 58 chỗ; đánh số theo
  vị trí trong file (lần đầu theo thứ tự `ast.walk` ra `S[7]` trước `S[4]`).
- **So "trước / sau" cho thay đổi đường build: tách khâu đắt ra dùng chung** (B-02: mã hóa e5 một lần 201 s, dựng điểm hai lần từ cùng ma trận) — đổi một thứ, đo một thứ.
- **`git diff --stat main..dot3` (hai chấm) đếm cả commit `main` đi sau nhánh** ⇒ số kích thước nhánh ghi theo `git diff --shortstat <gốc>..<đỉnh>` (m-1 review B).
- **Plan ghi thông điệp lỗi phải đối chiếu đúng dòng ném đầu tiên** (đợt 3 commit 1: plan m-4 ghi `"Target collection already exists"`, thực tế
  `require_fresh_full_corpus_target` ném trước với `"target is non-empty"`) ⇒ khi viết test "đúng lý do", chạy thử một lần để thấy thông điệp thật trước khi ghi vào plan.
- **Thêm một phép kiểm vào vòng lặp nóng: đo thời gian trước / sau** (B-11 gấp đôi thời gian chia đoạn cho tới khi cache) — plan có ghi "đo giây" nên thấy ngay.
- **`git mv` sang thư mục bị gitignore vẫn đưa file vào index** (B tìm, M-1 plan đợt 3) ⇒ chuyển dữ liệu sang chỗ private bằng `cp` + `git rm`, kiểm `git ls-files`.
- **Script đo đọc `HEAD` chỉ đúng sau khi commit** (`usage.py` dùng `git grep <rev>`): D6 chạy sau commit, hoặc grep working tree.
- **Lệnh với `HF_HOME` rỗng bị auto mode chặn** trong session C (và B) ⇒ test kiểu đó để User chạy `!` (WORKFLOW §3.6), ghi rõ "dùng lại kết quả User" khi review.
- **Chỉ số lỗi do validator đếm: phân loại theo hình dạng output trước khi kết luận nguyên nhân** (C-09: 8.1 ghi "model quên `[n]`", thực tế viết `[Nguồn n]`).
- **Đọc đúng tài liệu trước khi phản biện** (sua_4 m3: C đọc nhầm plan G3, B đúng — H1 mới là bước bỏ huydang).
- **Import hai kiểu (`backend.X` / `X`) tạo hai bản module** ⇒ `except` / `isinstance` hụt — đã sửa ở gói 1b (quy ước import trần, chạy từ `backend/`).
- **Hàm so cặp của harness 8.1 không đổi dấu cho chỉ số "càng thấp càng tốt"** — từ gói 3a dùng `paired_stats` với tên `false_refusal`.
- `grep` ở máy là ugrep: regex dài báo "exceeds complexity limits" ⇒ tách ngắn hoặc dùng Python.
- Giữ từ trước: repo public (không chép nội dung kho / Golden / câu kín / dự án khác vào file tracked); giờ lấy bằng `date`; không báo "đã xong" trước khi lệnh ghi
  file trả kết quả; đọc tin mới trước bước đo / thay đổi; chạy GPU phải được A ghi rõ.

## Tiền

Paid API C phiên 27/10: **0,0123914 USD thật** (R1 pilot 0,0049030 + C58 0,0074884, usage log). Paid API C phiên tối 26/10: **0,0026861 USD thật** (C43 R2 bước 1, usage log). Paid API C phiên 26/10 chiều: **≈ 0,0020 USD ước** — 5 lượt cổng ổn định D5 × 2 câu `gpt-6-luna` (~0,0002 / câu; route không ghi usage). Cả đợt 3 ≈ 0,0024 (trần 0,003).
2 test generator có key: 0 USD (không gọi mạng). Quota Claude Code: không dùng sub-agent.

Paid API C phiên tối 25/10: **≈ 0,0016 USD** — đo: 0,000427 (C35, 2 lượt `gpt-6-luna`); ước (route không log usage): 3 lượt cổng ổn định × 2 câu × ~0,0002
(gói 3, review 1b, đợt 3 commit 2) ≈ 0,0012. Trần chung gói 1–5: 0,05 USD; đợt 3: ≤ 0,003 (đã dùng ~0,0004). Phiên chiều 25/10: 0 USD.
Quota Claude Code cho sub-agent: C34 3 sub-agent (S1–S3) phiên tối; C32 ~2,1M token phiên chiều.
