# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 11:55 07/11/2026 (A, mở phiên 07/11: quyền phiên, terminal, Qdrant bật lại). Trước: 22:41 06/11/2026 (A, **kết phiên tối 06/11**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Nguyên văn phiên 06/11 sáng + tối (mọi việc giao, quyết định theo giờ, kết quả): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-06_lich_trinh_cau_tu_nhien.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất — viết lại 22:41 06/11/2026)

**Hệ thống (`main` = `origin/main`):** RAG 1–8 + trợ lý Phase 9 (định tuyến 4 tuyến, tìm thêm ≤ 2, nhớ câu hỏi 3 lượt, câu dặn hẹp, giao diện nhiều lượt, 👍 / 👎, khẩn cấp PA1, #6 song song **bật**, tra web B6 **bật**). **Tối 06/11 merge, cờ TẮT, người dùng chưa thấy đổi:** B5b thời tiết (`db77f32`) · B171 sửa lỗi lịch trình (`dbb4004`). Cờ tắt khác: `lich_trinh` (câu tự do), `hoi_lai`, `anh.bat`. Kho 204 file / 8.435 đoạn; build record `9921888f2030`; Golden md5 `6331e88fb171`. `frontend/dist/` không commit ⇒ build khi cần. **Bẫy:** đừng `uv sync` ở `main` (gỡ sherpa-onnx khỏi `.venv` — `STATUS_E.md`).

**Tiền:** Phase 9 ≈ **1,92 / 2,5 USD** (tối 06/11 ≈ 0,027: B 0,011 · E 0,011 · C 0,004 · A 0,001 cổng). Phase 10 ≈ 0,098 / 0,15.

**Quyết định User tối 06/11 (nguyên văn + giờ ở archive):**
- **Lịch trình:** kín v2 (5 câu tự nhiên User duyệt, md5 `de95ff85e491`) **không đạt** 3 / 5 (cần 4 / 5) ⇒ cờ tắt. User chọn **"biểu mẫu trước"**: lịch trình vào qua biểu mẫu "Lên kế hoạch" của giao diện mới, **code quyết** (giá trị nút), đo trên bộ đã thấy, không bộ kín; câu gõ tự do chưa bật. Đã tìm ra: từ chối khi hỏi kèm = `tim_kho` bị chặn sau lịch (E20, chứng minh bằng code; sửa để khi bật câu tự do); hỏi lại số ngày thừa **chưa tái tạo được** (C210); "đi dày" không làm được bằng dữ liệu kho (E21) ⇒ câu User.
- **Giao diện:** bỏ số `[n]` trong chữ ⇒ dòng "Nguồn: …" dưới câu; **cổng du lịch kiểu Huế TRIPO mức 2, hai đợt** (đợt 1 khung cổng từ cái đã có; đợt 2 bản đồ / lưu trú / ăn uống / sự kiện sau nghiên cứu dữ liệu). Nghiên cứu xong: B172 giao diện (`data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md`), C209 nguồn dữ liệu (`…/nguon_du_lieu_dot_2.md`). **Spec đợt 1 bản 2 `ff3c317ec88b`** (`docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md`) — E review 2 vòng **ready** ⇒ **User DUYỆT 11:56 07/11/2026** (sha tính từ file) ⇒ B làm S1. **3 bản mẫu HTML (B173 xong):** `data/nghien_cuu_giao_dien_2026-11-06/mau/1.html` Son thếp · `2.html` Sông Hương · `3.html` Tím Huế trầm (= mốc hiện tại); ảnh so `mau/anh_nho/so_*.jpg`; report `report_agent/2026-11-06_giao_dien_cong/b173_implementation.md`.

**Phase 9 — còn lại:** giao diện cổng đợt 1 (gồm biểu mẫu lịch trình) ⇒ bật biểu mẫu khi Q-F đạt ⇒ B7 đóng gói. **Sửa lịch** (`p9-sua-lich` `79b3d9c`, harness ready E): cần cờ `lich_trinh` câu tự do ⇒ **hoãn** tới khi xét bật câu tự do (A xem lại cách sửa lịch sau biểu mẫu: "điền lại biểu mẫu"). Mô phỏng kín sửa lịch chờ User `!` (terminal C — lệnh `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §8).
**Phase 10:** ảnh xong (cờ tắt); giọng nói: plan G2 duyệt `92ec551531fd` ⇒ **G1 chờ User thu 40 câu**.
**Phase 11 / 12:** đợt 2 cổng kéo dữ liệu Phase 11 lên (C209 P1 / P2 / P3); Phase 12 deploy AWS = điều kiện đóng code (25–30/12).
**Đợt report đang mở:** `report_agent/2026-11-06_giao_dien_cong/` (B172, B173, C209 + spec đợt 1 ở `docs/superpowers/specs/`). Đóng: `2026-11-06_b5_cau_tu_nhien/` (`TONG_HOP.md`).
**Mặc định đã ghi trong spec (nếu User chưa trả lời):** Q-U3 ⇒ ẩn "đi dày" khỏi biểu mẫu. Các câu Q-U khác không có mặc định — hỏi trước S2 (frontend); S1 (backend) không phụ thuộc Q-U1 / Q-U2 / Q-U5, chỉ cần User duyệt spec.

### Quyết định User 07/11 (A ghi nhận 11:55–12:26 07/11/2026, giờ `date` khi ghi)
- Quyền phiên như 06/11. **Duyệt spec cổng đợt 1 `ff3c317ec88b`.** Q-U1 bản mẫu 2 "Sông Hương" (không thêm font) · Q-U2 (b) ảnh giấy phép mở, agent tìm, User kiểm từng ảnh (E làm) · Q-U3 ẩn "đi dày" đợt 1 **+ song song bổ sung thời gian tham quan từ web công khai** (C làm, User duyệt bảng v7) ⇒ có dữ liệu thì xét bật "đi dày"; sau đợt 1 sửa đường chat tự do (E20) rồi đo lại · Q-U4 bật `thoi_tiet` khi merge S5 · Q-U5 đầu trang "Huế · Trải nghiệm văn hóa & du lịch" (điện thoại "Trải nghiệm Huế"), trợ lý "Trợ lý Huế". Ghi ở spec §3 (sửa chữ).
- User hỏi lại hướng lịch trình ("trợ lý tự hỏi thêm + bổ sung dữ liệu") ⇒ A giải thích B5 đã làm vậy, kín v2 3 / 5 trượt do thiếu dữ liệu + E20 ⇒ User chọn "biểu mẫu + bổ sung dữ liệu song song".
- A quyết (kỹ thuật): S1 lượt biểu mẫu bị model từ chối 5 / 5 vì đoạn nguồn mỗi điểm chỉ là dòng tên (B đo: 11 / 28 điểm < 80 ký tự) ⇒ (e) sửa `_lay_nguon_lich` chọn đoạn nhiều nội dung; thử (a) lượt công cụ dựng sẵn vẫn từ chối 3 / 3. Qdrant: container mất ⇒ A `docker compose up -d qdrant` (8.435 point).
- **Trạng thái (13:01 07/11/2026):** S1 + S2 xong trên `p11-cong-dot-1` `f20fd28` (B; tiền 0,0059); S4 review backend + frontend **ready** (E; 0 blocker / 0 major; 3 minor B sửa). **X1 / X1b (C, 0,042 USD):** V2 = luật lịch vào lời dặn hệ thống lượt biểu mẫu ⇒ từ chối 1 / 32 nhưng chữ đầu p95 8,75 s > 5 s; V4 bỏ ⇒ X1c (V2 + suy luận low / minimal) chờ B build xong. **Chờ User:** cách sửa lượt biểu mẫu (đổi lời dặn = ngoài phạm vi spec), 27 ảnh (`…/anh/commons/xem_anh.html`), phiếu v7 thời lượng, 3 ô phiếu v6, lộ trình / giọng nói / deploy thật (`report_agent/2026-11-07_tu_soi_lo_trinh/TONG_HOP.md` §4). **Deploy thử cục bộ (B, nhánh `p12-deploy-nhap`):** build + compose đang chạy. E rảnh có lý do (việc còn lại chờ User).

### Phiên sau làm theo thứ tự (A giao ngay sau câu quyền phiên — không chờ "làm đi")

1. Mở A / B / C / E; `ListAgents`; **hỏi quyền phiên** (đề xuất như 06/11) ⇒ **cùng lượt** nhắn B / C / E (kèm `notify_when_idle`; **chỉ gửi việc kế khi session đã idle** — S101).
2. **A hỏi User mỗi lần một câu:** duyệt spec cổng đợt 1 (sha `ff3c317ec88b`) ⇒ Q-U1 chọn bản mẫu ⇒ Q-U2 ảnh ⇒ Q-U3 "đi dày" (phiếu `data/phase_9/lich_trinh/diem_cho_user_v6.md`) ⇒ Q-U4 bật thời tiết ⇒ Q-U5 tên cổng. Ghi lựa chọn vào spec §3 (sửa chữ, không đổi tiêu chí).
3. **B:** **S1 backend ngay khi User duyệt spec** (không chờ Q-U) — **S1 backend** (nhánh `p11-cong-dot-1` từ `main`: D3 đường biểu mẫu + D4 cờ + D6 4 API + D7 `bai_id` + test + Q1 / Q1m) ⇒ **S2 frontend** sau khi User trả lời Q-U1 (bản mẫu) / Q-U2 (ảnh) / Q-U5 (tên) — theo bản mẫu User chọn. **Bẫy S1:** (a) cờ #6 `song_song_tra_loi` đang BẬT ⇒ nhánh biểu mẫu phải rẽ **trước** `answer_turn_stream_parallel` (không chạy phần song song); (b) khung lịch hiện tới model qua kết quả công cụ — lượt biểu mẫu "không công cụ" ⇒ khung + luật viết lời phải do **code đưa vào ngữ cảnh** ⇒ test cho mỗi loại lượt (`WORKFLOW.md` §4 (4c)): lượt biểu mẫu đầu, lượt hỏi tiếp sau biểu mẫu, cờ tắt giống byte.
4. **C:** S3 đo Q-F khi S1 xong (12 tổ hợp ghi trước, ×2; trần **0,03 USD là của cả spec** gồm cổng) + S4 review cả nhánh `p11-cong-dot-1`. **Mô phỏng kín sửa lịch: A dời** (C nêu, A đồng ý 06/11 tối) — sửa lịch đang hoãn và có thể đổi cách ("điền lại biểu mẫu"); chạy lại khi xét bật câu tự do (lệnh + bước dựng worktree ở `STATUS_C.md`).
5. **E:** chờ User thu 40 câu (G1) ⇒ G2 theo plan `92ec551531fd`; có thể review spec đợt 2 khi A viết.
   **Bảng điểm:** `settings.yaml` `lich_trinh_bang` vẫn trỏ **`diem_v3.json`** (v4 / v5 / v6 chưa User duyệt). User tick phiếu v6 ⇒ **E** chốt `diem_v6.json` theo lựa chọn (máy kiểm khác v5 đúng chỗ đã tick) ⇒ A đổi `lich_trinh_bang` khi merge S1 (B chạy test + Q1m trên bảng mới). Chưa tick ⇒ S1 dùng v3.
6. **A:** sau Q-U: viết spec đợt 2 (C209 P1 / P2 / P3 — hỏi User) song song đợt 1.

### Nhánh

`main`; **đang mở:** `p9-sua-lich` `79b3d9c` (C; hoãn), `p10-giong-noi` `93bbc63` (E), `p9-b5c` (hồ sơ, đã tag). **Đã merge ⇒ chờ User xoá (User `!`):** `p9-b4`, `p9-b5`, `p9-toc-do-6`, `p9-toc-do-6b`, `p10-anh`, `p10-anh-mobile`, `p9-b6`, `p9-b5b`, `p9-b5-sua` (local + origin). 4 worktree AGY cũ `c725987` (User quyết).

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


## Câu hỏi cho User (hỏi mỗi lần một câu — đầu phiên sau)

1. **Quyền phiên** (đề xuất như 06/11: A tự điều phối — giao ngay việc có sẵn, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5).
2. **(gấp nhất)** Duyệt **spec giao diện cổng đợt 1** bản 2 sha `ff3c317ec88b` (review E ready) ⇒ rồi Q-U1…Q-U5 theo spec §3 (bản mẫu · ảnh · "đi dày" · bật thời tiết · tên cổng).
3. Đợt 2 cổng: bản đồ P1 (kho + Leaflet + tile OSM) / P2 (tự lưu tile) / P3 (thêm 208 lưu trú + 697 ăn uống OSM, nhãn "chưa kiểm") + có cần trang danh sách lưu trú (C209).
4. Thu 40 câu nói — `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
5. Bật **hỏi bằng ảnh** (`anh.bat`)? Xoá collection thử `hue_anh_siglip2`?
6. Vòng cải tiến (sổ): **W58** (S100: User / người ngoài duyệt độ tự nhiên trước khi khoá bộ kín — tối 06/11 đã làm đúng cách này và bắt được 4 / 5 câu cần sửa); **sửa câu W50** (S101: không gửi việc kế khi session đang chạy lượt); gỡ W4 / W39 (Session D 0 buổi, hạn 07/11); W57; luật "gói Python phát hành ≥ 2 tuần".
7. Xoá 9 nhánh đã merge (mục Nhánh) — User `!`.
8. Không gấp: mô phỏng kín sửa lịch (dời — A); câu thiên tai vẫn gọi Serper chỉ để lấy link; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên.

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
