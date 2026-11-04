# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 21:22 04/11/2026 (A, **kết phiên 04/11**: câu khẩn cấp PA1 vào `main` `4e3cb4e`; tốc độ #1 âm, **#6 đạt** (chưa merge); B4 khoá 3 đạt mọi phần đã thấy; nghiên cứu 8 repo + paper + TRIPO v3 ⇒ 18 ý vào kế hoạch; bậc mới "sửa lịch nhiều lượt"). Trước: 20:56 03/11/2026 (A, kết phiên tối 03/11).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Phiên 04/11 nguyên văn (việc giao, quyết định theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; tối 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03_toi.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-04_phase_9_b4_toc_do.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main` = `origin/main`):** chatbot = RAG 1–8 + trợ lý Phase 9: định tuyến 4 tuyến (trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp — câu soạn sẵn 113 / 114 / 115 / 112, **từ 04/11 dòng mở PA1** "…đang gặp nguy hiểm hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng)…") + dòng nhắc "có thể đã thay đổi" + trợ lý tự gọi `tim_kho` thêm ≤ 2 lần (B2b) + nhớ hội thoại (chỉ câu hỏi, 3 lượt) + câu dặn hẹp (B3) + giao diện nhiều lượt + 👍 / 👎 + nút gợi ý ngoài phạm vi. `frontend/dist/` không commit ⇒ `cd frontend && npm ci && npm run build`. Kho 204 file / 8.424 đoạn; Golden md5 `6331e88fb171`; T1 `4d5bbe9e0edc`. Qdrant chạy bằng Docker Desktop.

**Phase 9** — spec bản 9 `169c2dd5f86a` + **bậc mới User chọn 04/11: "sửa lịch nhiều lượt" ngay sau B5** (ghi sửa đổi spec khi viết plan bậc đó). Bậc: B0–B3b ✓ · **B4 đo gần xong** · B5 (plan bản 3 duyệt, bản 4 đang viết) · bậc sửa lịch · B5b thời tiết · B6 web · B7 đóng gói. Tiền Phase ≈ **1,20 / 2,0 USD** (phiên 04/11 ≈ 0,23); **dự phóng tới B7 ≈ 1,9** ⇒ xem kỹ trần mỗi plan; mỗi phiên ≤ 1 USD.

**Phiên sau làm theo thứ tự:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 04/11 hết hạn) — đề xuất: như 04/11 (A tự điều phối + tự quyết trong kế hoạch, A tự commit / push cả phiên, ≤ 1 USD, "tiếp tục điều phối, phát triển, triển khai, tự nghiên cứu, so sánh, đánh giá, viết báo cáo"). Hỏi **giờ kết phiên**. Kiểm Qdrant; worktree `/tmp/…` mất khi máy khởi động lại ⇒ B / C tạo lại.
2. **B4 (nhánh `p9-b4`, khoá 3 `7d72703`, plan bản 5 `acfaf8ca0df5`, trần 0,24 / dừng 0,23, đã dùng ≈ 0,134):** đã thấy đạt hết — Q1 228 / 228 · Q2 8 / 10 (ngưỡng ≥ 8) · Q3 0 / 7 · Q6(b) 0 / 5 × 2 · Q6(a) 2 judge mù 0 ý trái / 0 ý không nguồn giá-giờ-điều kiện · Q4 đã thấy 0 / 40 hỏi thừa, 40 / 40 đúng tuyến. **Còn:** (a) **kín** 10 lượt hỏi + 5 lượt ghép Q6k (C chạy trên `7d72703`; cần User `!` ở terminal C — auto mode chặn đọc file kín; nếu chưa chạy phiên 04/11 thì chạy đầu phiên); (b) Q4 phần 20 câu `tuyen_sealed` (auto mode terminal B chặn ⇒ User xác nhận ở terminal B hoặc giao C chạy bằng `chay_b4.py`, đổi query ⇒ cau như `data/phase_9/b4/q4/bo_tuyen_da_thay.jsonl`); (c) Q5 (hồi quy an toàn 32 + Golden), Q7, Q8 + Playwright; ⇒ C review cả nhánh ⇒ A merge + 5 chỗ báo cáo. Lệnh: `STATUS_B.md` "PHIÊN SAU ĐỌC TRƯỚC". Report `report_agent/2026-11-02_phase_9_code/b144_b4_implementation.md` (lệch luật "sau khoá không chỉnh" + Q4 trước kín đã ghi, User / A duyệt). Giới hạn đã cho ghi: chênh token đếm ↔ thật tăng theo số lần tìm thêm (max 854–909) — nợ A.
3. **Tốc độ #6 ĐẠT** (plan `093d548445a3`; nhánh `p9-toc-do-6` `ea081b0`, đã push): viết câu trả lời song song định tuyến — chữ đầu câu về Huế nhanh hơn trung vị **1,37 s** [0,34; 2,14]; an toàn 90 lượt 0 vi phạm; Q1 228 / 228; khẩn cấp không đổi. **Còn:** C viết report ⇒ B review ⇒ A merge (sau hoặc trước B4 — **merge bên nào trước thì bên kia rebase + chạy lại Q1**) + 5 chỗ báo cáo. Vẫn > sàn 3 / 5 s (provider chậm hôm đo) ⇒ bước sau theo `data/phase_9/toc_do/c150_phan_tich.md` (#4 gộp định tuyến ⇒ User quyết).
4. **B5 (lịch trình):** plan bản 3 **duyệt `bba7d2559b77`** (trần 0,15 / dừng 0,14); bảng điểm v2 **User duyệt** (`diem_cho_user_v2.md` `4e71222d7526`). **C173** (mã C đặt; C172 = chạy #6) viết plan bản 4 — chưa bắt đầu (ý #1–#7, #12, #18 bảng dưới) + bảng v3 có `ten_khac` ⇒ B review plan ⇒ A duyệt sha; **User duyệt bảng v3**. Code B5 chỉ sau khi B4 merge.
5. **Bậc "sửa lịch nhiều lượt"** (ý #8, #9): plan sau khi B5 merge; A xem lại lịch tới 20/12 + tiền Phase lúc đó.
6. **B6 (web):** User chọn web chỉ cho câu **về Huế** kho không có; bộ đo B6 nháp C160 (`data/phase_9/bo_do_b6/`), phải có ca "ở Huế có quán phở Hà Nội nào ngon".
7. Theo dõi: router đưa S20 sang `khan_cap` (2 lần trước); định tuyến quá 10 s ⇒ `tro_ly_hue`; `chat_feedback` chưa nối `chat_metrics`; câu từ chối sau 3 lần tìm ~8 s; #6: câu trò chuyện có thể chậm hơn (mẫu 2 câu).

**Nhánh:** `main`; `p9-b4` (B4); `p9-toc-do-6` (#6); `p9-chu-khan-cap` đã merge `4e3cb4e`, worktree đã gỡ ⇒ **chờ User `!` xoá**; `p9-toc-do-1` có tag `hoso/p9-toc-do-1` ⇒ User đã được đưa lệnh xoá (kiểm `git branch -a`).

**Mã hay gặp:** B0–B7 = bậc Phase 9 (spec §5); D… / Q… / m-… = quyết định / câu đo / finding minor; S20, S10, S04 = mã câu bộ an toàn 32 (private); P0_sai / P0_thieu = sai điều kiện / thiếu cảnh báo; N_AA = số câu tụt giữa hai lượt cùng cấu hình; Bxx / Cxx = mã việc A giao B / C; S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`; #1–#18 = ý tưởng từ nghiên cứu 04/11 (bảng dưới).


## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 ⇒ ÁP DỤNG (User: "cái gì đáng học thì ứng dụng, phát triển, cải thiện, add vào" — A ghi 21:16 04/11/2026)

Nguồn: `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ từng repo `data/nghien_cuu_tinh_nang_2026-11-04/` (`sa1`–`sa3`, `repo_*.md`, `paper_2203.07742.md` — đủ để không clone lại). Mỗi ý khi làm vẫn đi plan / đo / review như thường.

| # | Ý | Học từ | Bậc | Ai | Trạng thái |
|---|---|---|---|---|---|
| 1 | Kiểm giá sau sinh bắt cả "…000đ" và "triệu" | repo khách sạn (lọc giá sai không báo) | B5 (D8) | C173 plan, B code | đang đưa vào plan B5 bản 4 |
| 2 | Không đủ điểm hợp sở thích ⇒ câu cố định nói rõ, không lặng lẽ lấp | Travel-AI, TRIPO | B5 (D2 / D4) | C173 | như trên |
| 3 | Trường `khong_xep` + lý do từ mã luật code (model chỉ diễn đạt) + D8 kiểm lời nhắc đủ | TRIPO bớt điểm im lặng | B5 | C173 | như trên |
| 4 | Dòng giả định / lưu ý do **code** nối, không để model chép | Travel-AI (câu trả lời cuối là khuôn code) | B5 | C173 | như trên |
| 5 | Mỗi luật xếp lịch có một test **cố tình vi phạm** | Travel-AI (bộ đo để ca sai vẫn đạt) | B5 | B code | như trên |
| 6 | Dòng "Mình hiểu: 2 ngày · … — sai thì bấm sửa" + code dò số trong câu để phát hiện lệch ⇒ hỏi lại | TRIPO mất "2 ngày" | B5 (dùng đường hỏi lại B4) | C173 | như trên |
| 7 | Cột `ten_khac` (bí danh điểm) trong bảng | đối chiếu kho | B5 bảng v3 | C173 ⇒ User duyệt | User đồng ý thêm cột |
| 8 | **Sửa lịch nhiều lượt**: khung lịch giữ ở server, công cụ `sua_lich` hành động có tên, xếp lại cùng luật, dòng "Đã đổi / Giữ nguyên", thay điểm ⇒ 2–3 điểm cùng cụm để bấm; tránh 2 lỗi gộp của Travel-AI (không bỏ được sở thích; giá trị mặc định ghi đè giá trị đã nói); ≤ 2 hành động / lượt, nêu ý không làm | TRIPO, Travel-AI, Flex-TravelPlanner | **bậc mới sau B5** (User chọn) | plan sau B5 merge | chờ B5 |
| 9 | Bộ đo chuỗi sửa, mỗi chuỗi 3 lần (đạt cả 3 = pass^3) + câu sửa kiểu người thật (dời buổi, ý gộp hai yêu cầu) | nguồn agent đã kiểm, TRIPO v3 | bậc sửa lịch | người viết bộ đo | chờ |
| 10 | Cột trong nhà / nhiều bậc ⇒ "phương án ngày mưa", "ít bậc thang"; kho không ghi ⇒ để trống, không khẳng định | trip-advisor, TRIPO | B5b (cùng thời tiết) | C soạn, User duyệt | chờ |
| 11 | Bộ đo B4: thêm vài câu `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — chỉ theo dõi, không đổi sàn | SA4b | B4 lượt sau / bậc sửa lịch | B | ý cho lượt đo sau |
| 12 | Lời dặn không dùng tên địa danh thật làm ví dụ (model dễ chép ví dụ) | SA4b | B5 + lời dặn mới | B / C | áp khi viết lời dặn |
| 13 | **Lọc / ưu tiên theo lĩnh vực** (ý của User trong github.txt): đếm 0 USD trên kết quả đo đã có — thí nghiệm chỉ khi ≥ 3 câu thiếu ý vì đoạn lĩnh vực khác chiếm chỗ; ưu tiên mềm, không lọc cứng | User, SA1 | sau Phase 9 (hoặc lúc rảnh, phần đếm) | session rảnh | chờ |
| 14 | Đếm đoạn gần trùng trong 10 đoạn vào model (0 USD) ⇒ có nhiều mới thử lọc | `vietnamese-rag-system` | như #13 | session rảnh | chờ |
| 15 | Gắn nhãn lỗi tự động trên kết quả đo (thứ tự đúng: xét trả lời đúng trước "không tìm thấy") | `vietnamese-rag-system` (thứ tự sai) | B7 / sau | — | chờ |
| 16 | Báo cáo đồ án: "0 lỗi trên n ca" kèm **luật ba** (tỉ lệ lỗi thật vẫn có thể tới ~3 / n); ghi rõ nhãn nào do LLM gán, phần nào người kiểm mù; datasheet cho bộ đo | ViHoRec | B7 (đóng gói / báo cáo bảo vệ) | A | chờ |
| 17 | Dự phòng demo khi mất mạng (video / câu trả lời ghi sẵn — không dùng làm bằng chứng đo); đề cương gọi "trợ lý RAG có công cụ", không nói quá | github.txt | B7 | A | đã ghi ở "A còn nợ" |
| 18 | Nếu B5 đo thấy model hay bỏ sót `lich_trinh` (Q2a < 9 / 10): định tuyến gắn cờ ⇒ code gọi `lich_trinh` thẳng (đổi lời dặn định tuyến ⇒ hồi quy 176 + 32) | KhaiBoiPho (`app/core/chat/router.py` 1–15) | B5 phương án dự phòng | B | chỉ khi Q2a trượt |

**Không làm** (đã cân): lọc cộng tác / rating, tối ưu quãng đường (TSP), GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới (Phase 8 đã bỏ), nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. Quyền phiên + giờ kết phiên.
2. Vòng cải tiến 18 (A chuẩn bị lúc kết phiên 04/11 — `SO_CAI_TIEN_CACH_LAM.md` "Vòng 18").
3. Duyệt bảng điểm B5 v3 (cột `ten_khac`) khi C172 xong.
4. Khi rảnh: đọc 10 câu mẫu B4 `data/phase_9/bo_do_b4/mau_cho_user.md` và 10 câu mẫu B6 `data/phase_9/bo_do_b6/mau_cho_user.md`.
5. Không gấp: 4 worktree AGY cũ giữ hay gỡ; xoá sao lưu kho đợt 1 + 2?; báo cáo tiến độ cho giáo viên (cập nhật tới B2) — cập nhật thêm nếu muốn gửi lại.

## Câu hỏi A còn nợ (không cần User)

- Cách đếm token (`_token_count`) không tính kết quả tìm thêm + mô tả công cụ ⇒ chênh tới ~900 token khi tìm nhiều lần (B4 m-3); ngữ cảnh đo 1,7–4k ≪ trần 16k ⇒ chưa ảnh hưởng; xem lại khi lời dặn / công cụ dài thêm (B5).
- Ứng viên tối ưu tiền `prompt_cache_key`: lợi ≈ 0 hiện tại; xét lại khi lời dặn dài hơn.
- Bảng sổ cải tiến: S41–S44 thiếu 1 cột. W4 / W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức OpenAI / Serper — đặt khi tới B6.
- B7: dự phòng demo khi mất mạng; đề cương nói "trợ lý RAG có công cụ"; ý #15–#17 bảng dưới.

## Session

**Phiên 04/11 (mở 19:34):** A `hue-rag-b7` · B `hue-rag-2d` · C `hue-rag-81` — cả ba Claude Code, trực tiếp.

**Phiên tối 03/11 (mở 17:56):** A `hue-rag-9e` · B `hue-rag-32` · C `hue-rag-40` — cả ba Claude Code, trực tiếp.

**Phiên 03/11 (mở 08:36, kết 13:26 03/11/2026):** A `hue-rag-5e` · B `hue-rag-52` · C `hue-rag-d8` — cả ba Claude Code, trực tiếp. B: B131 hoàn tất B1, B132 plan B2, B134 code B2, B135 plan B3, B136 code B3 (≈ 0,513 USD). C: C133 bộ đo B2, C134 review B1, C135 review plan B2, C136 bộ đo B3, C137 / C141 review B2, C138 câu hai ý, C139 thời tiết, C140 mẫu giao diện, C142 review plan B3, C143 bộ đo B4 + chi phí, C144 bảng điểm B5, C145 review sớm B3 (≈ 0,0006 USD). A: điều phối, merge B1 + B2, 5 chỗ báo cáo × 2, README repo, báo cáo cho giáo viên, vòng cải tiến 16.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên 04/11 — HẾT HẠN lúc kết phiên (21:34 04/11/2026)**: quyền như 03/11 + mandate "tiếp tục điều phối, phát triển, triển khai, tự nghiên cứu, so sánh, đánh giá, viết báo cáo". Tiền phiên 04/11 ≈ **0,226 USD** (B ≈ 0,108 · C ≈ 0,117 chưa gồm kín B4 · A ≈ 0,001). Vòng cải tiến 18: W55, W56 `đang thử`.
- **Phiên 04/11** (User chọn "như 03/11", A ghi nhận 19:38 04/11/2026): A tự điều phối + tự quyết trong kế hoạch; A tự commit / push cả phiên; ≤ 1 USD / phiên; B / C push nhánh riêng. Hết hạn cuối phiên.
- **User (A ghi nhận 19:40 04/11/2026):** "tiếp tục điều phối, phát triển, triển khai, tự nghiên cứu, so sánh, đánh giá, viết báo cáo". Vòng cải tiến 17 duyệt cả 3 (W52, W54 đang thử; I10 xong).
- **User 18:05 (A ghi nhận 18:05 03/11/2026):** "tiếp tục điều phối, phát triển, tự nghiên cứu, so sánh, tối ưu, đánh giá, viết báo cáo"; **kết phiên ~22:10** ⇒ A bắt đầu kết phiên ~21:40.
- **Phiên tối 03/11 — HẾT HẠN lúc kết phiên** (User chọn "như trưa 03/11", A ghi nhận 18:01 03/11/2026): A tự điều phối + tự quyết trong kế hoạch; A tự commit / push cả phiên; ≤ 1 USD / phiên; B / C push nhánh riêng. Hết hạn cuối phiên.
- **Phiên 03/11 — HẾT HẠN (kết phiên 13:26 03/11/2026)** (User: "quyền của A như 02/11" 08:46; "đồng ý cả phiên" A tự commit / push ~09:10): A tự điều phối + tự quyết trong kế hoạch; ≤ 1 USD / phiên; B / C push nhánh riêng. Tiền phiên 03/11 ≈ **0,514 USD** (B ≈ 0,513 · C ≈ 0,0006 · A 0). User: C làm trực tiếp với A, việc A giao = "làm đi".
- **Phase 9 (spec duyệt, không hết hạn theo phiên):** trần **2,0 USD** cả Phase; Serper dùng luôn (User chấp nhận rủi ro điều khoản — spec §2, §7); gói npm giao diện như đã duyệt 02/11.
- **Thường trực:** A commit / push — **hỏi User trước** (luật chung của User), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (I8, `WORKFLOW.md` §9.6); B / C không commit trừ khi việc ghi rõ; duyệt cho A =
  duyệt cho B / C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper (B122, trang giá): 0,001 USD / lượt (gói 50 USD / 50.000; 2.500 lượt thử).

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | bộ kín 40 câu — **đã dùng** 01/11 | `7f97d4c10b2b` |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối Phase 1–8 (mốc của Phase 9): runbook, tools, golden/, an_toan/, ngay/, kin/ | — |
| `data/nghien_cuu_phase_9_2026-11-01/` | nghiên cứu Phase 9: mạch 1–4, TRIPO; **`agent/`**: `a_sa1–3.md` (khoá FDE), `b122_tra_web.md`, `b123_sdk_probe.md` (+ `b123/`), `c121_sdk_024.md` | — |
| `gửi chatgpt/2026-11-02/` | yêu cầu agent có công cụ (`015467cce3f1`) + kết quả `NGHIEN_CUU_PHASE9_AGENT_CONG_CU_HUE_RAG_2026-11-02.md` | — |
| `data/giao_dien_moi_2026-11-01/` | ghi chú tham khảo, `do_csp/`, `b121/` (script Playwright, ảnh, log) | — |
| `data/tra_cuu_cli/<ngày>_<tên>/` | đầu ra `scripts/tra_web_codex.sh` (02/11: `b122-a-agents-sdk`, `b122-b-serper`, `b122-c-do-agent`) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report
  `<việc>_implementation.md`; review chéo (W32: ca dò khác cách + câu bất biến); plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file).
- **Báo kết quả bộ an toàn 32 câu luôn đủ 4 số** (đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời) — `run-experiment` §4, W51.
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`:
  `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop — **không `pkill -f`**, bẫy §8);
  (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ 5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31). Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ (W45). `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 03/11 nguyên văn (B131–B136, C133–C145, quyết định theo giờ, B1 / B2 merge): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`.
- Phiên 02/11 nguyên văn (B121 giao diện, B122 / B123, C118–C121, các quyết định agent theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/` (`b121_giao_dien_implementation.md`, `b121_review.md`); hướng chọn B116 `report_agent/2026-11-01_giao_dien_moi/`.
- Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + lượt đo cuối Phase 1–8 (01/11): `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
