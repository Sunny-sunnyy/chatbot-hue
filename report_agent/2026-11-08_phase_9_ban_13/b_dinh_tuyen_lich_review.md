# Review: câu lịch / ngày âm chung (không nhắc Huế) đi trợ lý — lời dặn định tuyến

Decision: **ready_for_user_confirmation**
Người kiểm: E (Claude Code, `hue-rag-e4`) — A giao thay C (tối 10/11/2026, sau 21:30), một vòng, chỉ chỗ rủi ro.
Date: 21:39 10/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-10-phase-9-dinh-tuyen-lich-plan.md` bản 2 `aa493aec252f` (A duyệt)
Implementation report: `report_agent/2026-11-08_phase_9_ban_13/b_dinh_tuyen_lich_implementation.md` (`f060a0d`)
Nhánh: `p9-dinh-tuyen-lich` `e8e07c9` (dựng trên `main` `f380d76`), worktree `/tmp/b_dtl`.

**Tính độc lập (khai rõ):** E **không viết code** nhánh này. E **có viết bộ giữ mù H** (25 câu, `giu_mu_sealed.jsonl` sha `5ef0d41b62f2`) và **tự chạy** H trên bản
khoá — nên phần H trong report là số E đo, review này không coi là bằng chứng độc lập cho H. E cũng viết `lich_san` (nguồn "Lịch hệ thống", T1 nhanh) mà tầng 2 đi qua.

## 1. Phạm vi đã review

- Cổng tối thiểu: commit gốc / worktree khớp report; đường dẫn đổi = **1 file** `backend/llm/full_corpus_prompt.py` (+4 dòng, đều trong `ROUTER_INSTRUCTIONS`); exact diff; `git diff --check` sạch.
- Chỗ rủi ro A / B nêu: (1) chỉ lời dặn định tuyến đổi; (2) số tầng 1 / tầng 2 khớp file kết quả; (3) câu bị rút do `citation_integrity_error`; (4) nhãn cũ "hôm nay âm lịch"; (5) lời dặn mới có kéo câu ngoài phạm vi / khẩn cấp sai không; lập luận "chỉ câu đổi tuyến mới cần sinh"; Golden #145.
- Không chạy lại: test rộng (861 / 1 — B), tầng 2 sinh câu (19 câu), cổng ổn định.

## 2. Findings

**0 blocker · 0 major · 2 minor** (không mở vòng sửa).

- **m-1 — câu lịch thuần trả lời đúng nhưng bị rút vì thiếu mã trích dẫn (giới hạn, đã khai báo).** Vị trí: `l2_r1.jsonl` câu Y3 (loại "còn mấy ngày tới một ngày âm"),
  `outcome: retracted`, `after_text: true`. Bằng chứng: chữ trả lời đúng ngày (E tự đổi: ngày chạy + 102 ngày = rằm tháng Giêng năm âm sau) nhưng **không có mã [n] nào** ⇒
  luật sẵn có `backend/llm/citations.py:28-29` ("Grounded answer has no citation") ⇒ rút. **Không phải lỗi mới trong code**; lời dặn định tuyến không chạm phần này. Mới ở
  chỗ: loại câu lịch thuần trước đây bị định tuyến chặn, nay tới đường trả lời ⇒ lộ tỉ lệ model quên trích nguồn "Lịch hệ thống" (1 / 9 ở lượt này; ở lượt T1 nhanh của E
  10/11, 8 câu ngày đi trợ lý đều có [n]). Tác động người dùng: thấy chữ hiện ra rồi bị thay bằng thông báo lỗi. Tiêu chí ghi trước L2 ≥ 8 / 9 vẫn đạt. **Đề xuất (việc
  sau, không chặn):** đếm tỉ lệ trên ≥ 20 câu lịch thuần trước khi quyết sửa; không tự gắn [n] bằng code (làm yếu rào trích dẫn).
- **m-2 — nhãn cũ "từ chối" của câu "hôm nay âm lịch" (R11).** Đúng như người chấm của B ghi. **E đã sửa trong bộ của E** `data/phase_9/t1/bo_sau_g.jsonl` (R11:
  `expected_type` refuse ⇒ unconditional, `tra_loi_duoc_bang_ngay: true`; nhãn cũ giữ ở trường `nhan_cu_truoc_10_11`; md5 `f581d252bc10` ⇒ `d48fc411af3a`; bản trước
  `/tmp/e_bo_sau_g_truoc_sua.jsonl`). Bộ gốc `data/ngay_hien_tai_2026-10-30/questions.jsonl` (không phải của E, bộ 30/10) còn nhãn cũ — **A quyết** có sửa không (bộ đó
  dùng như lịch sử). Câu ngoài kho X14 nhãn "từ chối" là đúng, không sửa.

Độ đơn giản: thay đổi là 2 câu chữ trong một lời dặn, không cờ, gỡ = revert một commit — tương xứng. Không thấy over-engineering trong code; bộ đo (tầng 1 chỉ gọi định
tuyến, chỉ câu đổi tuyến mới sinh) là cách rẻ nhất đủ.

## 3. Cách người kiểm chạy lại thật

```bash
# sha các lời dặn trên main ↔ nhánh (git show ra /tmp, sha256[:12] như chay_tuyen.py:14)
# chấm lại tầng 1 từ file kết quả của B (0 USD)
cd data/phase_9/dinh_tuyen_lich/tools && python3 cham_tuyen.py ../cu_r1.jsonl ../cu_r2.jsonl ../moi2_r1.jsonl ../moi2_r2.jsonl ../g_cu.jsonl ../g_moi2.jsonl
# ca dò riêng của E: 10 câu ranh giới E tự viết (/tmp/e_do_dtl/do_ranh_gioi.jsonl), CHỈ gọi định tuyến của nhánh, 2 lượt
cd /tmp/b_dtl/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env \
  python /home/minhhieu/hue_rag/data/phase_9/dinh_tuyen_lich/tools/tuyen.py chay file:/tmp/e_do_dtl/do_ranh_gioi.jsonl /tmp/e_do_dtl/ra_moi_<k>.jsonl
```

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Chỉ `ROUTER_INSTRUCTIONS` đổi | **Đúng.** `main` ↔ nhánh: định tuyến `164bd4a254e9` ⇒ `8cd30cbb359a`; lời dặn trả lời `81d3040cf53f`, trò chuyện `df921574c362`, mô tả công cụ ngày `1c64dfcca1d3` **giống hệt**. 4 dòng thêm nằm giữa lời dặn ⇒ 80 ký tự đầu (2 test dùng để nhận lần gọi định tuyến) không đổi |
| Mỗi dòng kết quả mang đúng sha | `cu_r1/r2` (166) + `g_cu` (176) toàn `164bd4a254e9`; `moi2_r1/r2` + `g_moi2` toàn `8cd30cbb359a`; `moi1_r1` toàn `0b87d2974330` (bản 1); 0 lỗi định tuyến |
| Số tầng 1 khớp report | **Khớp** từng mục: N_AA (khẩn cấp 0 · ngoài 0 · Huế 3 · trò chuyện 0); L1 9 / 9 cả 2 lượt (cũ 0 / 9), 0 câu ngày khác lệch; K 0 sang từ chối, giữ khẩn cấp 20 ↔ 20; N0 0 ↔ 0; S1 0 ↔ 0; AT ngoài tập cũ 0; G đổi 1 (#145 Huế ⇒ ngoài phạm vi), ngoài phạm vi sang Huế 0 ↔ 0 |
| Golden #145 | Câu không có từ chỉ ngày / lễ ⇒ hai câu thêm không nhắm loại này; B chạy lại 5 + 5 lần đều `tro_ly_hue` ⇒ E đồng ý **nhiễu** (dùng lại số của B, không chạy lại) |
| Lập luận "chỉ câu đổi tuyến mới cần sinh" | **Đúng**: lời dặn trả lời giống byte và lần gọi trả lời không chứa lời dặn định tuyến (cả đường song song #6) ⇒ câu cùng tuyến nhận đúng chuỗi gửi model như cũ. Đổi tuyến đo trên 2 lượt + so N_AA bản cũ ⇒ đủ bắt câu đổi thật |
| Tầng 2 câu bị rút | m-1 ở trên |
| Ca dò riêng E (10 câu × 2 lượt, chỉ định tuyến) | **20 / 20 đúng tuyến** — ngày lễ dương "là thứ mấy" ⇒ trợ lý; cùng ngày đó + sự kiện ở nơi khác ⇒ ngoài phạm vi; "Tết nghỉ mấy ngày" ⇒ ngoài phạm vi (đúng như report §3 tự ghi); "còn bao nhiêu ngày tới Giáng sinh", "năm X có tháng nhuận không", "hôm nay là ngày bao nhiêu" ⇒ trợ lý; mùng 1 + chùa ở Huế ⇒ trợ lý; khẩn cấp có "tối nay" ⇒ khẩn cấp; **bất biến** thời tiết Huế ngày mai ⇒ trợ lý, thời tiết nơi khác ⇒ ngoài phạm vi. 0,002213 USD |

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại tầng 2 (sinh + chấm 19 câu), test rộng, cổng ổn định — dùng số của B (đầu vào, môi trường không đổi; tầng 2 B đo trên đúng `8cd30cbb359a`).
- Bộ H không độc lập với E (E viết + chạy) — đã khai ở đầu.
- Ca dò 10 câu là mẫu nhỏ; cận trên tỉ lệ câu ngoài phạm vi lọt vẫn vài phần trăm như report §3 ghi.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Đổi phạm vi sản phẩm (câu lịch chung trong phạm vi) ⇒ User đồng ý rồi A merge. Giới hạn trình User: 1 / 9 câu lịch thuần bị rút vì model
quên trích nguồn (m-1); "nghỉ lễ / Tết mấy ngày" vẫn ngoài phạm vi. A quyết m-2 phần bộ 30/10. Tiền review: 0,0022 USD.
