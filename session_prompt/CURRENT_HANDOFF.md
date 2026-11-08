# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 12:24 08/11/2026 (A, kết phiên 08/11). Trước: 15:43 07/11/2026 (A, **trước khi User mở lại cả 4 session để reset context — giữa phiên 07/11, chưa kết phiên**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Nguyên văn phần đầu phiên 07/11 (11:53 → 15:43 07/11/2026): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-07.md`; 06/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-07_cong_dot_1_tu_soi.md`.

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 12:24 08/11/2026, kết phiên 08/11)

**Phiên 08/11 đã kết** (User nghỉ, dặn ~13:00 dừng). Quyền phiên 08/11 **hết hạn** ⇒ A mới hỏi lại User một câu. Nguyên văn phần đầu phiên: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-08.md`. Tổng hợp đợt: `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md`; nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-08_pham_vi_dong_goi.md`.

**Hệ thống (`main` = `origin/main`):** như 07/11 + từ 08/11: 7 ảnh cổng · **hỏi bằng ảnh BẬT** (`anh.bat: true`) · bản đồ lịch trình (cờ `ban_do_lich` TẮT) · 14 việc nhỏ (nút Dừng, ô 500 ký tự, gợi ý dưới câu từ chối, Nguồn gộp theo bài, sao chép / tải lịch, thẻ Khám phá, nút báo sai `/api/bao_sai`, ảnh điện thoại, kiểm số mục web ⊂ đoạn trích, `turn_id` trong `chat_metrics`) · README đúng hiện trạng. Định tuyến vẫn 4 tuyến (G chưa merge).
**Quyết định User 08/11 (giờ ở archive / TONG_HOP):** chưa deploy tới khi đủ tính năng + đóng gói + Docker; phạm vi trước đóng gói = bản đồ + ảnh + giọng nói + Nhóm 1 + 2; **spec Phase 9 bản 13 duyệt `5557f0fd7650`** (cổng 2 nhóm, bỏ khẩn cấp, ngoài phạm vi ⇒ agent từ chối; 4 công cụ T1–T4; T2 = agent chỉ quyết lúc tra); trần Phase 9 **3,5**; bỏ mốc ngày; **mức nhẹ cho việc nhỏ** + **5 cách giảm thời gian test** (Session_Prompt §7–§8, WORKFLOW §6); mức dừng G 0,75 + chỉnh lời dặn nhiều vòng; T3 vòng 3.
**Tiền 08/11:** ≈ 0,99 USD (B G ≈ 0,75 + bản đồ / việc nhỏ / review ≈ 0,011 · E ≈ 0,128 · C ≈ 0,096 · A ≈ 0,003). Phase 9 ≈ 3,0 / 3,5 (≈ 2,02 trước 08/11 + ≈ 0,98 hôm nay; số cộng từ report, chưa đối chiếu log tổng) — quỹ B7 0,35 giữ riêng ⇒ còn ≈ 0,15 cho việc mới ⇒ **lượt kín G + S5 + đợt 2 cần User nâng trần**. Phase 10 ≈ 0,107 / 0,15.

### Làm tiếp (theo thứ tự)
1. **G cổng 2 nhóm (B)** — khoá `87d6798` (ROUTER `6b4796f7a35c`, ANSWER `426109d21b13`); G3 đạt mọi sàn trên bộ đã thấy + lượt khoá (S2 / S2b / S3b 0; S1 ngoài kho 0 ×2). **Còn:** lượt kín (a 8 + b 10, ≈ 0,011 USD — vượt mức dừng 0,75 ⇒ **A xin User trước**, User chạy `!` 2 lệnh ghi ở `STATUS_B.md`), chấm mù S1 + S4 (0 USD), S5 độ trễ (≈ 0,06) ⇒ review cả nhánh ⇒ merge.
2. **T1 ngày + âm lịch (E)** — nhánh `p9-t1-ngay` `f388b19`, cờ `ngay_lich` tắt; đạt 4 tiêu chí; review nhánh vòng 1 bắt M-1 (Tết tháng 1) ⇒ đã sửa; vòng 2 xem `report_agent/2026-11-02_phase_9_code/t1_ngay_branch_review.md`. Trước bật: S5 + lượt xác nhận câu ngày mới (gồm ca 1/1 – Tết) + đo lại 5 câu ngày khi G vào `main`. Thư viện `lunar-vn==1.4.0` (A duyệt 11:06). **Bẫy:** tới khi T1 vào `main`, KHÔNG `uv sync` thường (gỡ `lunar-vn` + `sherpa-onnx`) — dùng `uv sync --inexact --frozen`.
3. **T3 bảng vé + giờ (C)** — nhánh `p9-t3-bang` `21ec06d`, cờ tắt; vòng 3 Q2 19/20 nhưng Q3 trượt 6/10 ⇒ **chờ User chọn** (mục "Câu hỏi cho User").
4. **Đợt 2** (sau khi G vào `main`): T2 tra web thành công cụ ⇒ T4 lịch trình từ câu gõ (spec §12).
5. **User khi rảnh:** tick phiếu toạ độ bản đồ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` (⇒ bật `ban_do_lich`); thu 40 câu giọng nói (`data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`); phiếu v6 / v7.
6. **Đo độ trễ (S5):** mỗi lượt đo riêng, lần lượt B ⇒ E ⇒ C (lệnh ở `STATUS_<X>.md`); báo phiên điều phối dự án khác (nếu có trong `ListAgents`) trước.
7. Kết phiên sau: báo cáo khâu (`BAO_CAO_SINH_CAU_TRA_LOI_API`, `LUONG`) gộp mọi thay đổi đợt (luật mới: sửa lúc đóng đợt), `Project_Status.md`, vòng cải tiến (W59, W60 chờ User).

### Nhánh
`main`; **đang mở:** `p9-g-cong` (B), `p9-t1-ngay` (E), `p9-t3-bang` (C), `p12-deploy-nhap` (chờ deploy), `p9-sua-lich` (hoãn), `p10-giong-noi` (E), `p9-b5c` + `p9-toc-do-6` (hồ sơ). **Đã merge ⇒ chờ User xoá (User `!`):** `p10-anh-bat`, `p11-anh-cong`, `p11-ban-do`, `p11-lich-nho`, `p11-viec-nho-c`, `p11-viec-nho-e`, `p9-sua-test-cong` + các nhánh cũ ở archive 07/11. Worktree giữ: `/tmp/b_g` (G), `/tmp/e_t1` (T1), `/tmp/c_t3` (T3).

### Mã hay gặp
G = cổng 2 nhóm; T1 ngày + âm lịch; T2 web thành công cụ; T3 bảng vé + giờ; T4 lịch trình câu gõ (spec §12); S1–S6 / S2b / S2c / S3b = sàn §12.3; B0–B7 = bậc Phase 9; Bxx / Cxx / Exx = việc A giao; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`.

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

| # | Ý | Trạng thái |
|---|---|---|
| 1–7, 12 | Kiểm giá "…000đ" / "triệu"; không đủ điểm ⇒ câu cố định; `khong_xep` + lý do từ mã luật; dòng giả định do code nối; test cố tình vi phạm; dòng "Mình hiểu…"; cột `ten_khac`; lời dặn không dùng địa danh thật làm ví dụ | vào B5 (`d66f6a3`) |
| 8 | Sửa lịch nhiều lượt (`sua_lich` hành động có tên, khung giữ ở server, Đã đổi / Giữ nguyên, ≤ 2 hành động / lượt) | code trên `p9-sua-lich` `79b3d9c` (rebase lên B5b + B171, giữ `hoi_toi` / lý do buổi tối — C208); harness đo E review ready; **hoãn** (cần cờ `lich_trinh` câu tự do) |
| 9 | Bộ chuỗi sửa lịch pass^k | bộ `data/phase_9/bo_do_sua_lich/` (10 + 5 kín; nhãn đã thấy S03 / S08 sửa theo B171 — C208); plan chọn pass^2; pilot = S01 + S06 (A đồng ý) |
| 10 | Cột trong nhà / bậc thang ⇒ phương án ngày mưa | phiếu gộp **v6** `data/phase_9/lich_trinh/diem_cho_user_v6.md` chờ User (gồm 2 câu v5 + cột thời lượng E21) |
| 11 | `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — theo dõi | C210 06/11: code không dò "3N2D" / "4n3d" / "2 hôm" / "cuối tuần" nhưng model tự gửi đúng số 5 / 5; biểu mẫu bỏ vấn đề này |
| 13, 14 | Ưu tiên theo lĩnh vực; đoạn gần trùng | đếm 0 USD xong — không mở thí nghiệm (C179) |
| 15–17 | Nhãn lỗi tự động; "0 lỗi trên n ca" + luật ba; dự phòng demo mất mạng | B7 |
| 18 | Router gắn cờ ⇒ code gọi `lich_trinh` | không cần (Q2a đạt) |

**Không làm** (đã cân): lọc cộng tác / rating, TSP, GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới, nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.


## Câu hỏi cho User (hỏi mỗi lần một câu)

**Mới 08/11 (User nghỉ lúc hỏi):** (0) **Tiền:** Phase 9 ≈ 3,0 / 3,5, quỹ B7 0,35 ⇒ còn ≈ 0,15 — nâng trần để chạy lượt kín G (≈ 0,011, vượt mức dừng G 0,75), S5 các việc (≈ 0,06 mỗi việc), đợt 2 T2 / T4 (≈ 0,33)? (1) **T3 bảng vé + giờ** — vòng 3: đúng 19/20 (đạt), khối điều kiện 4/4, nhưng sàn Q3 "0 câu model tự nêu điều kiện ngoài khối" trượt 6/10 (model chép điều kiện từ đoạn kho của lần tìm đầu) ⇒ chọn: phương án B (bảng chỉ cho kiểm cuối số, cờ tắt) · hay thiết kế lại (code lọc câu điều kiện khỏi chữ model) · hay đổi sàn Q3 (User duyệt). Report `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` §9. (2) Bật bản đồ `ban_do_lich` sau khi User tick phiếu toạ độ. (3) Bật `ngay_lich` sau review nhánh + đo S5.

Xem "Làm tiếp" mục 1 (kiểm 7 ảnh vi.wikipedia) + mục 2 (a)–(g). Không gấp: bật hỏi bằng ảnh `anh.bat` + xoá collection thử `hue_anh_siglip2`; đợt 2 cổng (C209: P1 bản đồ từ toạ độ kho — tự soi đề xuất chỉ P1); thu câu giọng nói (nếu giữ); câu thiên tai vẫn gọi Serper chỉ để lấy link; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên; vòng cải tiến cũ (W58, sửa câu W50, gỡ W4 / W39 — hạn 07/11, Session D 0 buổi, W57).

## Câu hỏi A còn nợ (không cần User)

- **Tối 06/11:** E20 Sửa 1 (code nối câu "phần hỏi thêm chưa có thông tin") + Sửa 2 (cho `tim_kho` sau lịch tìm thật 1 lần) — làm khi xét bật câu tự do; C210 giả thuyết còn lại (harness kín sau ghi `so_ngay` model + số code dò + có thẻ hỏi); giờ tới / về bị bỏ qua im lặng (B5 không có trường giờ); "chưa có điểm buổi tối hợp sở thích" hiện cả khi không nêu sở thích + lượt sửa không có cách xin buổi tối (E, ngoài phạm vi C208); link trong chữ Markdown câu trả lời chưa có `rel` (C211 — vào S2). **06/11 sáng:** quan sát B5b "model gọi `thoi_tiet` 2 lần rồi từ chối" (theo dõi); "đi dày" ít tác dụng vì bảng điểm thiếu thời lượng (ghi nhận, chưa sửa); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần" / "đi trong ngày" (dựa vào model — đo ở kín v2); B171 thêm `hoi_toi` + `chon_sang` vào tham_so ⇒ `p9-sua-lich` phải tôn trọng khi merge.
- Link Google Maps của B5 đổi sang toạ độ cho 17 điểm có toạ độ (C197; v5 thêm 1 toạ độ) — A quyết khi bật B5.
- B6 giới hạn: địa chỉ / số điện thoại trong mục web chưa kiểm ⊂ đoạn trích (đề xuất "mọi chuỗi số ⊂ đoạn trích" — việc sau); chữ đầu mục web p50 ~13 s (theo dõi; ý tối ưu: tra web song song khi kho có dấu hiệu thiếu); thêm "đang" vào luật thời gian thực sẽ chặn nhầm 1 câu đúng.
- B5b giới hạn: câu "tuần sau" không có số dự báo (luật ngoài 7 ngày); câu không dấu không có công cụ (ngoài phạm vi, User 25/10).
- Cách đếm token (`_token_count`) không tính kết quả tìm thêm + mô tả công cụ ⇒ chênh tới ~900 token; ngữ cảnh 1,7–4k ≪ 16k.
- Ghi đệm OpenAI: C202 05/11 tối âm — giữ như cũ; xét lại nếu tắt tìm thêm. Bảng sổ cải tiến: S41–S44 thiếu 1 cột. Log `FileHandler` không xoay vòng (deploy). Hạn mức OpenAI / Serper — đặt trước deploy (B6 đã bật).
- B7: dự phòng demo khi mất mạng; đề cương "trợ lý RAG có công cụ"; ý #15–#17.
- Theo dõi: router đưa S20 sang `khan_cap`; định tuyến > 10 s ⇒ `tro_ly_hue`; `chat_feedback` chưa nối `chat_metrics`; case Golden 67 từ chối ngẫu nhiên sau tìm thêm (C192).

## Session

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Kết phiên 08/11 (User 11:06 08/11/2026): khoảng 13:00 dừng việc, A yêu cầu mọi session kết phiên — không kết sớm hơn.**
- **Phiên 08/11 (User chọn "như 07/11", A ghi nhận 09:22 08/11/2026):** như 07/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, khoá Serper cho tra cứu, việc cần User duyệt thì gác). Hết hạn cuối phiên. Giao lúc mở: B ảnh cổng (`p11-anh-cong`), C review ảnh, E rà "Câu hỏi A còn nợ" (chỉ đọc).
- **Phiên 07/11 (User chọn "như 06/11", A ghi nhận 11:55 07/11/2026):** A tự điều phối — giao ngay việc có sẵn trong handoff, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5. Hết hạn cuối phiên.
  **Thêm (12:30 07/11/2026, User đi nghỉ):** "tiếp tục nghiên cứu, triển khai, phát triển, đánh giá, viết báo cáo đầy đủ; việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; làm việc khác; tự do nghiên cứu, gọi Codex tra cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau". Trần tiền như trên (≤ 1 USD / phiên). **(12:31 07/11/2026) User: "trần tiền tôi vẫn duyệt nếu quá 1$, có thể thoải mái thực nghiệm"** ⇒ vượt 1 USD / phiên được; A vẫn ghi tiền thật từ log mỗi việc + báo tổng ở nhật ký.
- Phiên tối 06/11 — hết hạn 22:41 06/11/2026. Tiền phiên ≈ 0,027 USD.
- **Tiền Phase 9: trần 3,5 USD** (User nâng 10:38 08/11/2026; trước 2,5) (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
- **Đã duyệt, không hết hạn theo phiên:** spec giao diện cổng đợt 1 bản 2 `ff3c317ec88b` (User 11:56 07/11/2026); plan G2 giọng nói `92ec551531fd` (A duyệt sau review 2 vòng, 06/11 tối); spec Phase 10 bản 4 `784d6f7abd9f` (sherpa-onnx, tải model ≤ 300 MB, thu 40 câu; Web Speech bỏ); tải SigLIP 2 + collection ảnh (11:42 05/11); luật S-AT mới (20:14 05/11); cache câu trả lời ⇒ Phase 12 (20:27 05/11); bật `tra_web` (21:15 05/11).
- **User (09:00 05/11/2026):** cần công cụ / nghiên cứu / tải / khoá mới ⇒ tự nghiên cứu (0 USD, thông tin công khai) + đề xuất; thêm công cụ / thư viện lớn / tải model / khoá / tài khoản mới vẫn trình User trước (`Session_Prompt.md` §4).
- **Phase 9 (spec):** Serper dùng luôn (User chấp nhận rủi ro điều khoản); gói npm giao diện như đã duyệt 02/11; dữ liệu công khai dùng cho học tập, không kiểm giấy phép (05/11).
- **Thường trực:** A commit / push — hỏi User trước (luật chung), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (`WORKFLOW.md` §9.6); B / C / E không commit trừ khi việc ghi rõ; duyệt cho A = duyệt cho B / C / E; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. **(12:32 07/11/2026) User: khoá `SERPER_API_KEY` dùng được cho tra cứu nghiên cứu** (gọi qua `uv run --env-file /home/minhhieu/hue_rag/.env …`, không đọc / in khoá; chỉ câu tra thông tin công khai; 0,001 USD / lượt, ghi số lượt). Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper: 0,001 USD / lượt. Open-Meteo: 0.

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | bộ kín 40 câu — **đã dùng** 01/11 | `7f97d4c10b2b` |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối Phase 1–8 (mốc của Phase 9) | — |
| `data/phase_9/` | bộ đo B4 / B5 / B5c / B6 / sửa lịch, bảng điểm v3 / v4, toạ độ, kết quả đo | — |
| `data/phase_10/anh/` | bộ ảnh đo, danh sách tên, patch `p10-anh`, E9 | — |
| `data/sua_kho_2026-11-05_gio/` | sửa kho giờ mở cửa: lệnh `tools/chay.sh`, sao lưu record / sparse | — |
| `data/nguon_mo_huegov_2026-08-05/` | dữ liệu mở Huế (có file dữ liệu cá nhân ⚠ — không vào kho / báo cáo) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C / E sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file); review ≤ 2 vòng.
- **Bộ an toàn 32 câu luôn báo đủ 4 số** (đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời).
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (tự viết); `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server bằng TaskStop (không `pkill -f`); (3) chạm tìm / chia đoạn: T1 giống byte; (4) 3 chỗ báo cáo (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Đang dựng chỉ mục / đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant.** Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ. `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 06/11 sáng + tối nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`.

- Phiên tối 05/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`.
- Phiên 05/11 sáng–chiều nguyên văn (C173–C197, B156–B163, E1–E8, quyết định theo giờ, merge B4b / B5 / #6, B5c âm): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`.
- Phiên 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`, `…_2026-11-03_toi.md`; 02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
