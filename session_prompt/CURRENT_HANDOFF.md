# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 15:43 07/11/2026 (A, **trước khi User mở lại cả 4 session để reset context — giữa phiên 07/11, chưa kết phiên**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Nguyên văn phần đầu phiên 07/11 (11:53 → 15:43 07/11/2026): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-07.md`; 06/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-07_cong_dot_1_tu_soi.md`.

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 15:43 07/11/2026)

**Mở lại giữa phiên 07/11:** User tắt + mở lại A / B / C / E để reset context, **không kết phiên**. Quyền phiên 07/11 dưới đây vẫn là ý User hôm nay ⇒ A mới **xác nhận lại bằng một câu** (không hỏi lại từ đầu), rồi giao việc theo mục "Làm tiếp".

**Hệ thống (`main` = `origin/main`, `fbcb903` trở lên):** RAG 1–8 + trợ lý Phase 9 (định tuyến 4 tuyến, tìm thêm ≤ 2, nhớ câu hỏi 3 lượt, khẩn cấp PA1, #6 song song, tra web B6) **+ từ 07/11:** **giao diện cổng du lịch đợt 1** (merge `dbfc925`: bản mẫu Sông Hương; trang chủ, Khám phá 204 bài, Trợ lý Huế nổi mọi trang + trang riêng, Giới thiệu, dòng "Nguồn" thay số [n]; 4 API chỉ đọc) · **thời tiết BẬT** (`0dab4e5`) · **biểu mẫu "Lên kế hoạch" BẬT** (V5 merge `312ad9f` + cờ `a884de4`: code xếp lịch bằng giá trị nút; lượt biểu mẫu = luật lịch trong lời dặn hệ thống + suy luận "low"). Cờ tắt: `lich_trinh` (câu tự do), `hoi_lai`, `anh.bat`. Kho 204 / 8.435; build record `9921888f2030`; Golden md5 `6331e88fb171`; bảng điểm runtime `diem_v3.json`. `frontend/dist/` không commit ⇒ build khi cần. Bẫy: đừng `uv sync` ở `main` (sherpa-onnx — `STATUS_E.md`); test đọc `settings.yaml` thật ⇒ mốc "cờ tắt" đặt rõ trong test (B `a884de4`).
**Số đo 07/11:** biểu mẫu S3 bộ quyết 24 / 24 sàn, F-a 12 / 12 × 2, chữ đầu p95 4,25 s; trên `main` sau bật: biểu mẫu chữ đầu p50 2,30 / p95 4,22 s, câu kho 1,78 / 3,61 s (n = 10). Q-G / Q-N đạt.
**Tiền:** 07/11 ≈ 0,10 USD (C ≈ 0,078 · B ≈ 0,009 · E ≈ 0,002 · A ≈ 0,002). Phase 9 ≈ 2,02 / 2,5. Phase 10 ≈ 0,098 / 0,15.

**Quyền phiên 07/11 (User):** như 06/11 (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng) + **vượt 1 USD / phiên được, thoải mái thực nghiệm** + khoá `SERPER_API_KEY` dùng được cho tra cứu (qua `--env-file`, không đọc khoá) + "việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; tự do nghiên cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đề xuất lẫn nhau".

**User quyết 07/11 (giờ ở archive):** duyệt spec cổng `ff3c317ec88b`; Q-U1 bản 2 Sông Hương · Q-U2 ảnh giấy phép mở (agent tìm, User kiểm) · Q-U3 ẩn "đi dày" + bổ sung thời gian tham quan song song · Q-U4 bật thời tiết · Q-U5 "Huế · Trải nghiệm văn hóa & du lịch" / "Trợ lý Huế"; "biểu mẫu + bổ sung dữ liệu"; **bật biểu mẫu với V5**; F-a (4) = "không trái nhóm là đủ" (User hỏi "sao code chọn điểm mà không phải agent" ⇒ A giải thích luật AI FDE: luật cứng / thứ tự ⇒ code, agent hiểu ý + viết lời); **ảnh: chỉ 7 (2 đầu trang + 5 lĩnh vực)**; **mọi ảnh lấy từ ảnh đại diện bài vi.wikipedia, chỉ file `/wikipedia/commons/`** (User bắt bộ cũ sai: "bún bò" là bún riêu; "Điện Thái Hòa" là Đại Cung môn).

### Làm tiếp (theo thứ tự)
1. **Ảnh (E xong 16:2x — 30 ảnh, mọi file trên Commons; User chọn #1 = cầu Trường Tiền `File:Truong_Tien_bridge_(I).jpg`):** User xem tiếp #2–#7 ⇒ chốt. Trước: E làm lại ảnh từ vi.wikipedia (thư mục `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/`, có `xem_anh.html` mở qua `\\wsl.localhost\Ubuntu-24.04\…`) ⇒ **User kiểm 7 ảnh** ⇒ **B** đóng 7 ảnh vào `frontend/` + dòng ghi công (tác giả · giấy phép · link) ⇒ review (C hoặc E) ⇒ A merge + cổng (`npm ci && npm run build`).
2. **Hỏi User (mỗi lần một câu):** (a) lộ trình tới đóng code (`report_agent/2026-11-07_tu_soi_lo_trinh/TONG_HOP.md` §4 — bốn session đồng thuận: **deploy thử sớm** Lightsail 4 GB ≈ 24 USD / tháng, User tạo tài khoản + khoá OpenAI riêng có hạn mức; ⚠ gói miễn phí AWS tự đóng tài khoản sau 6 tháng / hết tín dụng) ⇒ (b) giọng nói giữ / nhẹ 10 câu / cắt ⇒ (c) đóng lịch trình câu tự do + sửa lịch tới sau bảo vệ ⇒ (d) mốc quyển báo cáo + slide (nguồn: `e_tb_bang_bang_chung.md`) ⇒ (e) phiếu thời lượng v7 (C) + 3 ô phiếu v6 ⇒ (f) kịch bản demo nháp (`e_demo_5_phut.md`) ⇒ (g) luật cải tiến: "đường mới có model ⇒ 1 lượt thật trước bộ test" (B) + "đồ đo dựng sau khi code chạy được" (C) + "đóng gói dữ liệu private bằng danh sách chừa + đếm trong sản phẩm cuối" (A) + **hook `pre-commit` / `pre-push` đọc thêm danh sách tên dự án khác từ file private trong `data/`** (07/11: tên một dự án khác lọt vào 2 file tracked từ 05/11 — mẫu cứng trong hook chỉ có một tên; đã sửa tiến `2c83b7d`, lịch sử giữ; báo User).
3. **Deploy (khi User duyệt):** nhánh `p12-deploy-nhap` `4cfe681` (biến môi trường `HUE_QDRANT_URL` / `HUE_TRA_WEB`, review E ready) + nháp `data/phase_12/deploy_nhap/` (allow-list `dung_dockerignore.py`, review E vòng 2 ready; build lại vì `--no-cache`, đo cỡ ảnh). Trước link công khai: giới hạn lượt, cookie `Secure`, tắt `/docs`, `tra_web` tắt trên AWS (E-dep checklist 9 mục).
4. **User `!` khi tiện:** xoá nhánh đã merge (mục Nhánh). (Ảnh Docker cũ chứa file đánh giá `hue-rag-app:nhap` — User đã xoá 07/11; còn `nhap2` sạch.)
5. **Máy dùng chung với một dự án khác của User:** trước khi đo độ trễ / build nặng, A nhắn phiên điều phối bên đó (tên thấy trong `ListAgents`) — bên đó cũng hỏi trước khi chạy việc nặng (chi tiết chỉ ghi ở `data/`). **07/11 16:05 → khoảng 17:05:** bên đó chạy việc nặng (A hue_rag đồng ý) ⇒ hue_rag **không đo độ trễ** trong khoảng này; build giao diện + 1 server thử thì được.
6. A: kết phiên khi User nói (Project_Status, PROJECT_HISTORY, TONG_HOP đợt `2026-11-06_giao_dien_cong/`, vòng cải tiến — bẫy ghi ở `STATUS_A.md`).

### Nhánh

`main`; **đang mở:** `p12-deploy-nhap` `4cfe681` (B; chờ User duyệt deploy), `p9-sua-lich` `79b3d9c` (C; hoãn), `p10-giong-noi` `93bbc63` (E), `p9-b5c` (hồ sơ, đã tag). **Đã merge ⇒ chờ User xoá (User `!`):** `p11-cong-dot-1`, `p11-bat-bieu-mau`, `p9-b4`, `p9-b5`, `p9-toc-do-6`, `p9-toc-do-6b`, `p10-anh`, `p10-anh-mobile`, `p9-b6`, `p9-b5b`, `p9-b5-sua` (local + origin). 4 worktree AGY cũ `c725987` (User quyết).

### Mã hay gặp

B0–B7 = bậc Phase 9; B5b = thời tiết, B6 = tra web; G0–G4 = bậc giọng nói (spec Phase 10 §8); Q… / D… / V-… = câu đo / quyết định / tiêu chí giọng nói; S-AT = thủ tục sinh lại câu an toàn (luật mới 05/11 tối: chênh đúng 1 ⇒ thêm 3 + 3, âm khi tổng chênh ≥ 2 / 6 — `skills/run-experiment/SKILL.md` §4); Bxx / Cxx / Exx = việc A giao; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`; #1–#18 = ý nghiên cứu 04/11.

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

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên 07/11 (User chọn "như 06/11", A ghi nhận 11:55 07/11/2026):** A tự điều phối — giao ngay việc có sẵn trong handoff, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5. Hết hạn cuối phiên.
  **Thêm (12:30 07/11/2026, User đi nghỉ):** "tiếp tục nghiên cứu, triển khai, phát triển, đánh giá, viết báo cáo đầy đủ; việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; làm việc khác; tự do nghiên cứu, gọi Codex tra cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau". Trần tiền như trên (≤ 1 USD / phiên). **(12:31 07/11/2026) User: "trần tiền tôi vẫn duyệt nếu quá 1$, có thể thoải mái thực nghiệm"** ⇒ vượt 1 USD / phiên được; A vẫn ghi tiền thật từ log mỗi việc + báo tổng ở nhật ký.
- Phiên tối 06/11 — hết hạn 22:41 06/11/2026. Tiền phiên ≈ 0,027 USD.
- **Tiền Phase 9: trần 2,5 USD** (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
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
