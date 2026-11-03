# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 08:46 03/11/2026 (A, **mở phiên 03/11**: giao B131 hoàn tất B1, C133 bộ đo B2, C134 review delta — mục "Việc đang mở — phiên 03/11"). Trước: 20:47 02/11/2026 (A, **kết phiên tối 02/11**: B0 merge `1c10111`; B1 đo xong trên `p9-b1`, chưa merge). Trước: 14:52 02/11/2026 (A, **kết phiên 02/11**: giao diện mới vào `main` `ed8e6e8`; Phase 9 đổi hướng agent; **spec Phase 9 bản 9 User duyệt sha `169c2dd5f86a`**; vòng cải tiến 14).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Lịch sử phiên 02/11 (mọi mục việc B121–B124 / C118–C121, quyết định theo giờ, trạng thái review) dời **nguyên văn** sang
`session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`; 01/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-01.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-02_giao_dien_moi_va_spec_phase_9.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main`):** chatbot RAG mức 1 như 01/11 (streaming, 10 đoạn, `gpt-6-luna`) + **giao diện mới React + Vite + Tailwind** (merge `ed8e6e8` 02/11): bản build `frontend/dist/` **không commit** —
clone / worktree mới hoặc sửa `frontend/src/` ⇒ `cd frontend && npm ci && npm run build` (thiếu ⇒ `/` 404). Kho 204 file / 8.424 đoạn; Golden md5 `6331e88fb171`; T1 `4d5bbe9e0edc`. Qdrant chạy bằng Docker Desktop —
`curl :6335` không trả lời ⇒ báo User, không tự bật.

**Phase 9 = trợ lý agent có công cụ — SPEC DUYỆT** `docs/superpowers/specs/2026-11-02-phase-9-design.md` **bản 9 sha `169c2dd5f86a`** (User duyệt, A ghi nhận 14:48 02/11/2026; review 3 vòng
`…_review_v6.md`; bản 5 hướng cũ ở `077e3cb`). Sửa spec sau duyệt = bản mới, duyệt lại phần đổi. Tóm tắt:
- **Agent dưới chính sách**, OpenAI Agents SDK **0.19.4** (giữ — B123 + C121): agent **định tuyến** đầu ra có cấu trúc ⇒ trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp; trợ lý gọi công cụ tìm thêm kho · hỏi lại ·
  lịch trình; **code giữ** ngày hôm nay (vào lời dặn), tra web Serper (khi kho từ chối, mục "Từ web" [w n], nhãn chưa kiểm), lần tìm đầu (thí nghiệm). Nhớ hỏi + đáp trong cuộc trò chuyện (server RAM, 30 phút).
- **8 bậc** B0 nền ⇒ B1 định tuyến + trò chuyện + ngày ⇒ B2 tìm kho + thí nghiệm câu tìm ⇒ B3 nhớ ⇒ B4 hỏi lại ⇒ B5 lịch trình ⇒ B6 web ⇒ B7 so RAG cũ (cùng tuần). Mỗi bậc: plan nhỏ ⇒ session khác review ⇒ A duyệt sha ⇒
  nhánh riêng ⇒ review cả nhánh + cổng ổn định ⇒ A merge.
- **Chất lượng trước** — sàn tiền / tốc độ chỉ theo dõi; **bắt buộc log USD + ms** mỗi lần gọi LLM / Serper / câu / tuyến. Trần Phase **2,0 USD**, mỗi phiên ≤ 1 USD. Đóng code ~20/12/2026.

**KẾT PHIÊN TỐI 02/11 (20:47 02/11/2026) — phiên sau làm theo thứ tự:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền tối 02/11 hết hạn; User tối 02/11: "làm đi, đừng hỏi tôi" ⇒ đề xuất một câu duy nhất: quyền như 02/11 + A tự quyết trong kế hoạch); kiểm Qdrant.
2. **B1 hoàn tất (B):** nhánh `p9-b1` `7e190d7`, worktree `/tmp/b_p9b1` (có `dist/`; mất sau khởi động lại máy ⇒ tạo lại). Việc: (a) kiểm 0 USD lần gọi trả lời giống byte B0 trên **32 câu bộ an toàn** ⇒ giống thì dùng lại S-AT 01/11;
   (b) sửa m-1 C132 (`aclose` lõi trước khi ghi log) ; (c) đổi mặc định cờ `router` + `may_have_changed_notice` = true (`emergency_rule`, `today_line` giữ false); (d) cổng ổn định có 1 ca ngắt thật `curl -m`;
   cập nhật `b129_b1_implementation.md`. ⇒ **C review delta `7e190d7..<cuối>`** (`b129_review.md`) ⇒ A merge ⇒ 5 chỗ báo cáo (LUONG, BAO_CAO_SINH — mục 4 đã có dòng B1 tối 02/11, Project_Status, guide 6, nhật ký).
3. Sau merge B1 ⇒ **B2** (spec §5: B2a thí nghiệm câu tìm kho, B2b vòng công cụ `tim_kho`): người viết plan B2 ≠ người viết bộ đo. Mốc tuần: B1 đóng trước 16/11 (luật cắt spec §6).
4. Theo dõi khi B7: tốc độ (định tuyến thêm ~1,7 s / câu); tắt ghi đệm prompt (−13,3 % tiền, C126); khoá cache theo phiên ở B3.
5. ~~Xoá nhánh `p9-b0`~~ **XONG 21:28 02/11/2026** (User `!`, local + origin). User `!` (không gấp): cắt 22 dòng log cũ (lệnh trong chat tối 02/11: sao lưu `/tmp` ⇒ `sed -i '/Received question/d'`) — nếu chưa chạy.

(cũ — kế hoạch tuần soạn 15:09 02/11, phần B0 / bước 0 / bộ đo B1 **đã xong** tối 02/11:)
**Thứ tự việc phiên sau:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 02/11 hết hạn); kiểm Qdrant; `cd frontend && npm ci && npm run build` nếu chưa có `dist/`.
2. **Giao B0** (spec §5): người viết plan B0 + người review khác người viết; A duyệt sha (tính từ file). Việc song song không chồng file (vd C soạn bộ câu tuyến / chuỗi hỏi tiếp cho B1–B3 theo spec §4; phần kín do người không code giữ).
3. Đặt mốc kiểm mọi việc > 30 phút (W47); brief việc Phase 9 kèm mọi tài liệu cũ cùng Phase (W46); trước khi đề xuất cơ chế an toàn / bộ đo thêm: "đã quan sát chưa · ai dùng · bao giờ deploy" (W48).

**Kế hoạch chi tiết tuần 02–08/11 (A soạn 15:09 02/11/2026; theo spec §5, §6 — phiên sau giao, chưa ai làm):**
- **B0 — nền (≈ 0,003 USD), người làm đề xuất: B** (đã dò SDK ở B123, code giao diện B121):
  bọc RAG 1–8 thành công cụ `tim_kho` (gọi `retrieval_service.search`, `backend/retrieval/full_corpus.py:419`; top-k + collection do code điền); lõi chung `backend/llm/assistant.py` cho route stream + `/api/chat` + `answer_case`;
  sổ nguồn (kho `[n]` / web `[w n]`); log USD + ms mỗi lần gọi model (`RunHooks.on_llm_start/end` — `b123_sdk_probe.md`), mỗi câu, mỗi tuyến.
  **Tiêu chí B0 (spec §5):** S-T1 mới giống byte; `answer_case` qua lõi chung ra đúng câu trả lời đường RAG 1–8; test ranh giới (chỉ một module gọi mạng ngoài; không công cụ nào nhận URL); log đủ trường;
  grep chữ câu hỏi / mã phiên trong log = 0. Quy trình: B viết plan B0 ⇒ **C review plan** (chỉ dựa "Căn cứ để review") ⇒ A duyệt sha ⇒ nhánh `p9-b0` (worktree) ⇒ review cả nhánh ⇒ cổng ổn định ⇒ A merge.
- **Bước 0 khẩn cấp (User chọn Q1 (a) của spec bản 5, A ghi nhận 11:03 02/11/2026):** ~10 câu khẩn cấp **tự viết** (cháy, trẻ lạc, đuối nước, cấp cứu…) qua chatbot hôm nay (≈ 0,003 USD) ⇒ **User đọc** 10 câu trả lời ⇒ có lỗi ⇒ luật code + câu soạn sẵn ở B1;
  không ⇒ ghi "không cần". Người soạn câu + chạy: C (song song B0, không chồng file — chỉ gọi `/api/chat` qua server tạm cổng riêng; nếu B đang đo latency thì chờ, W31).
- **Viết bộ đo cho B1 (song song, người viết: C — không phải người code B1):** bộ tuyến (~40 đã thấy + phần kín; có 5 ca lái tuyến), bộ ngày (dùng lại 15 câu `data/do_cuoi_2026-11-01/ngay/`; 12 câu quyết), bộ khẩn cấp;
  mẫu Golden cố định ~30 câu cho B3–B6 (seed ghi trước, khoá ở B0 — spec §4). Phần kín: B (người code) **không mở**.
- **Mốc tuần:** B0 đạt trước 09/11 ⇒ tuần 09–15/11 làm B1. Luật cắt đầu tiên **16/11** (B1 chưa đóng ⇒ B2 chỉ làm B2a). A kiểm luật cắt mỗi thứ Hai (spec §6).
- **Chú ý khi viết plan các bậc** (minor còn lại từ review spec, sửa trong plan): m17 nếu B2a giữ V2 thuần thì A/A đường có công cụ chạy ngay ở B2a; lượt `hoi_lai` + `StopAtTools` có `final_output` khác `AnswerOutput`
  (`backend/llm/generator_openai_full_corpus.py:269`) ⇒ cần nhánh riêng; cổng web chỉ mở khi `outcome` thường; danh sách "trước khi deploy" ở spec §7 (soát chữ web, điều khoản Serper, lưu phiên, R1 C106).

**Đọc khi viết plan B5 (lịch trình) — ghi 09:57 03/11/2026:** `data/nghien_cuu_phase_9_2026-11-01/báo cáo nghiên cứu github.txt` (757 dòng, 3 báo cáo khảo sát ~01/10: repo gợi ý khách sạn / địa điểm + lịch trình, khuyến nghị "lịch trình cơ bản theo luật + tổng hợp thông tin"). Tới nay chỉ dùng **8 tên repo** (C116 ⇒ `c_mach4.md`), **chưa đọc nội dung** ⇒ người viết plan B5 đọc §4 "Khuyến nghị" của cả 3 báo cáo + đối chiếu spec §5 B5. User 03/11: làm xong việc hiện tại ổn định rồi mới mở rộng nghiên cứu (A đồng ý).

**Công cụ dự báo thời tiết Huế (User đề xuất, User chọn 10:52 03/11/2026):** tra cứu trước (0 USD, C139) ⇒ **quyết lúc viết plan B5** (gộp vào lịch trình hoặc bậc nhỏ sau B5). Nguyên tắc A nêu, User đã thấy: code gọi API, model chỉ diễn đạt kèm nguồn + giờ cập nhật, không tự dự báo; lũ / bão vẫn trỏ cơ quan chính thức / 112; kiểm điều khoản dùng thương mại. Không chen vào B2 / B3.

**Giao diện "đẹp, sinh động" (User 11:09 03/11/2026, đổi hướng so với 01/11 "gọn, nét Huế nhẹ"):** C140 dựng 3 trang mẫu tĩnh (`data/giao_dien_v2/mau/`) theo skill frontend-design + tham khảo baoyu-design / ui-ux-pro-max / ui-styling (dữ liệu) ⇒ User chọn ⇒ **code cùng phần giao diện nhiều lượt của B3** (không làm hai lần). Giữ CSP, ảnh có giấy phép, tắt chuyển động khi giảm chuyển động.

**Mã hay gặp:** B0–B7 = bậc Phase 9 (spec §5); P1–P5 = câu User đã chọn 14:42 02/11 (spec §10); V0–V3 = phương án câu tìm kho (B2a); [w n] = trích dẫn web; T1 = kết quả tìm 158 câu (so "giống byte");
S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`; M-n / m-n = finding major / minor; Bxx / Cxx = mã việc A giao B / C.

## Việc đang mở — phiên 03/11 (User "làm đi", A ghi nhận 08:46 03/11/2026)

Quyền phiên: như 02/11 (mục "Quyền"). Tốc độ B1 (định tuyến +1,7 s p50 / câu): User không chọn khác ⇒ **PA1 mặc định A khuyên** — merge B1 như đo, chưa tối ưu (đợi B2a quyết có dùng câu định tuyến viết hay không);
cổng cuối B1 đo chữ đầu 10 câu thật trên đường stream (≈ 0,003 USD) để có số thay 1 câu. Không có lượt đo latency khác chạy cùng lúc trong lúc B đo 10 câu (W31) ⇒ C chỉ làm việc 0 USD, nhẹ CPU khi đó.

### B131 — hoàn tất B1 (B, `hue-rag-52`) — giao 08:46 03/11/2026 — **XONG 09:00 03/11/2026, chờ C134 review delta `7e190d7..dcd1519`** (push; (a) 32 / 32 giống byte ⇒ dùng lại S-AT; (b) m-1 + test; (c) 2 cờ true; (d) cổng + 2 ca ngắt thật + chữ đầu 10 câu p50 3,05 / p95 5,64 s; 0,0029 USD; report `b129_b1_implementation.md` §4b `0febf8eb574d`, chưa commit — trên `main` working tree)
- **Việc:** CURRENT_HANDOFF "KẾT PHIÊN TỐI 02/11" mục 2 (a)–(d) + `STATUS_B.md` "PHIÊN SAU — B1": `git worktree prune` + tạo lại `/tmp/b_p9b1` (symlink `data/`, `knowledge-base-hue/`; `npm ci && npm run build`);
  (a) 32 câu an toàn giống byte B0 (0 USD) ⇒ giống thì dùng lại S-AT 01/11; (b) sửa m-1 C132; (c) mặc định `router` + `may_have_changed_notice` = true; (d) cổng ổn định có 1 ca ngắt thật `curl -m` **+ chữ đầu 10 câu tự viết trên `/api/chat/stream`** (p50 / p95, ghi theo tuyến).
- **Trần:** 0,02 USD. Cập nhật `b129_b1_implementation.md` ⇒ commit + push `p9-b1` ⇒ báo A. Không mở `*sealed*`.

### C133 — bộ đo B2 (C, `hue-rag-d8`) — giao 08:46 03/11/2026 — **XONG 08:55 03/11/2026** (report `c133_bo_do_b2.md`; mục lục `data/phase_9/b2/README.md` `3bdffc77d46e` (2 quyết định A đã ghi; script `04bdba9ea11a`; tự kiểm 2 ca âm + 2 ca dương tổng hợp đạt, `tu_kiem.json` `adc6f5288514`); bộ câu `e5d40678c1aa`: 38 / 12 có thể đổi / 32 nhãn v5 / dev 28 – test 10; V0 trùng T1 61 / 61; 0 USD). **Cần A quyết cho plan B2:** (1) luật "≥ 3 / 12" ↔ Holm (dev 28: 3 câu thêm ⇒ p 0,082; cần ≥ 5–6) — Holm là cổng hay chỉ báo số; (2) sàn mất đoạn đúng chấm trên cả 55 câu có nhãn (C đề xuất) hay chỉ 32 trong 38. **A quyết 08:56 03/11/2026 (ghi trước khi đo):** (1) tầng tìm = cổng sàng theo luật đếm spec (≥ 3 / 12 thêm cả hai lượt trên 38 + 0 mất + test không ngược chiều); Holm chỉ báo số + xếp hạng khi nhiều biến qua — cổng chất lượng thật là khâu trả lời (Completeness 18 câu CI > 0 + sàn §4); (2) sàn mất đoạn đúng trên cả 55 câu có nhãn ("mọi câu bị đổi"), báo tách trong / ngoài 38
- **Việc:** theo spec §5 B2 + 3 quyết định A (tin nhắn sáng 03/11): 38 câu Golden (18 nhiều nguồn + 20 so sánh), không thêm câu mới; chốt 12 câu chưa đủ keyword @10 (6 + 6, khớp Q3a §4); ghi rõ sàn "mất đoạn đúng" chỉ kiểm được trên 32 / 38 câu có nhãn v5;
  chia dev / test theo `split.json` + md5 — B chỉnh V1 / V3 chỉ trên dev, test không ngược chiều; script đo tầng tìm (đủ keyword @10, mất đoạn đúng v5, Holm 3 biến so V0) chạy được trên V0 (0 USD, nhẹ).
- **Đầu ra:** `data/phase_9/b2/` (private) + README; report `report_agent/2026-11-02_phase_9_code/c133_bo_do_b2.md` (số đếm, md5, cách chọn — không nội dung câu). 0 USD. Không đụng file nhánh `p9-b1`.

**B1 MERGE 09:19 03/11/2026: `main` `f01c032`** (A; C134 ready `b129_review.md` `4730a847d853`; code `main` = nhánh ⇒ dùng lại cổng B131 / C134; A chạy lại trên `main`: build giao diện + pytest 8 file có key **60 / 60 pass**). User đồng ý (giữa 09:07 và 09:11 03/11/2026, theo `date` của A) merge + A tự commit / push cả phiên 03/11 (hộp chọn). 5 chỗ báo cáo xong (LUONG bản 20, BAO_CAO_SINH bản 20, Project_Status §2 / §3 / §4, guide 6 "Hiện hành 03/11", nhật ký `2026-11-03_phase_9_b1_va_b2.md`) + mục lục. Nhánh `p9-b1` + worktree `/tmp/b_p9b1` ⇒ đề xuất xoá lúc kết phiên (User `!`).

### B132 — viết plan B2 (B) — giao 09:00 03/11/2026; 0 USD — **bản 1 XONG 09:07 03/11/2026 sha `0cf5c194a182`** (A tính từ file) ⇒ **C135 review plan** (sau C134). A chốt: trần B2 **0,45 USD**, dừng > 0,40; bước 0 câu hai ý: C đếm. B rảnh có lý do (nhánh `p9-b1` đang review) — chỉ probe SDK 0 USD cho D5 / D6 trong `/tmp` ⇒ `data/phase_9/b2/probe_sdk.md` — **bản 1 09:06 03/11/2026 sha `0cf5c194a182`, chờ C review** (B) · **bản 2 09:36 03/11/2026 sha `52fd872b941f`, chờ C kiểm phần sửa** (B) · **bản 3 09:39 03/11/2026 sha `efa27cb8207c`, chờ C kiểm M-4** (B)
- `docs/superpowers/plans/2026-11-03-phase-9-b2-plan.md` có "Căn cứ để review"; đọc spec §4, §5 B2, §7–§8; plan B1 + review; bộ đo C133 (`data/phase_9/b2/README.md`, `c133_bo_do_b2.md`); tài liệu cũ Phase 9 (W46, `find` 09:00: roadmap, 2 review spec, plan / review B0 + B1).
- Luật đã chốt A 08:56 (mục C133). Ghi: thứ tự biến, vòng công cụ, ước tiền + pilot 10 câu, trần, điều kiện dừng, luật cắt 16/11, trường `routing_ms` (quan sát B131). Xong ⇒ sha ⇒ C review plan.

### C135 — review plan B2 bản 1 (C) — **changes_requested** (`…-b2-plan_review.md` `1cfa46d1b03d`; 0 blocker / 3 major / 5 minor; 0 USD)
- **A quyết (09:31 03/11/2026, ghi trước khi đo):** M-1 (a) N_AA V0 / V1 / V3 / B2b = 6 (câu tụt Đủ của P5 B1 — cặp A/A vì lần gọi trả lời giống byte), ngưỡng S-G 6 + 3; V2 sinh A/A riêng. M-2: tầng tìm luôn tìm bằng `cau_tim` bất kể tuyến; lỗi tuyến ở Q5; đếm đổi tuyến ở Q3. M-3: C thêm `cham --nhom dev` (43 câu, không in số test). D5 = (b) max_turns 4 (probe B `probe_sdk.md` `2f43c894e2d5`). ⇒ B plan bản 2 ⇒ C kiểm phần sửa ⇒ A duyệt sha.
- **B133 (B) review README.md** (User nhờ A viết): `b133_readme_review.md` `01f99d3c732a` changes_requested 3M / 7m ⇒ A sửa hết; User yêu cầu viết lại gọn kiểu repo chuyên nghiệp, bỏ phần quy trình agent ⇒ A viết lại, chờ User xem rồi commit.

- **Vòng 2 (C, review `cb977b24ad8e`):** bản 2 `52fd872b941f` đóng 8 / 8, còn **M-4** (A quyết: B2b dùng N_AA từ A/A Golden 2 lượt của B2b, spec "thay N_AA … từ đây"). A đồng ý 5 điểm dò code của B (tool bọc trong generator, cờ `hit_max_turns`, token `chat_metrics` = tổng mọi lượt, ngân sách token gồm kết quả công cụ, dùng lại nhãn `searching`) ⇒ **B viết bản 3** ⇒ C kiểm M-4 + "Chỗ đổi bản 3" ⇒ A duyệt sha.

**Plan B2 DUYỆT — bản 3 sha `efa27cb8207c`** (A 09:43 03/11/2026, sha tính từ file; C135 vòng 3 ready, review `…-b2-plan_review.md` `90ed2605c9a9`; 2 minor m-6 / m-7 B sửa lúc code). ⇒ **B134 code B2** trong worktree nhánh `p9-b2` từ `main` mới nhất; trần B2 **0,45 USD**, dừng khi > 0,40; pilot 10 câu trước mỗi lượt có phí; phần kín (nếu có) C chạy sau khi B ghi dòng "Khoá". Lượt đo latency / pilot của B ⇒ C chỉ làm việc 0 USD nhẹ (W31).

### C136 — bộ đo B3 nhớ hội thoại (C) — giao 09:39 03/11/2026; 0 USD; dừng khi B báo bản 3 — **XONG 09:49 03/11/2026** (report `c136_bo_do_b3.md`; mục lục `data/phase_9/bo_do_b3/README.md` `2c094e287c65`; 25 đã thấy / 15 kín `*sealed*` / 3 web; nhớ tên 10; đáp án mẫu = câu Golden cùng nghĩa; `kiem_bo.py` OK; mẫu 10 chuỗi cho User `mau_cho_user.md` `dadb44ffcc6c`; 0 USD)
- Spec §4 + §5 B3: 40 chuỗi (25 / 15 kín) + 3 chuỗi cho B6; B code B3 ⇒ B không mở phần kín. `data/phase_9/bo_do_b3/`, report `c136_bo_do_b3.md`.

### B134 — code B2 (B) + C137 review sớm (C) — **XONG 11:29 03/11/2026, chờ C review `74c5d68..1f2a57c`** (B; B2a giữ V0, B2b `tim_them` bật — User giữ; ≈ 0,255 USD; report `b134_b2_implementation.md`)
- **B134 mốc 1** `456df18` (push `p9-b2`, 0 USD): D1–D10 + m-6; Q1 T1 giống byte; Q7 228 / 228 yêu cầu giống byte HEAD (v0 + tim_them tắt); test 70 / 70 + 10 mới. Lệch D2: bỏ "cắt 3 câu" V3 (schema strict chặn trước ⇒ router_failed ⇒ câu gốc). Pilot tầng tìm 10 câu dev × V1 / V3 / V2 ≈ 0,004 USD đang chạy.
- **C137 vòng sớm** (`b134_review.md` `3e05245866e1`): 0 blocker / 0 major / 2 minor — m-1 gather không bắt lỗi từng câu; m-2 V3 > 3 câu mất tuyến (kể cả khẩn cấp) ⇒ A: rủi ro an toàn, báo số route_error ở pilot / Q3 / Q5, > 0 ⇒ quay về cắt 3 câu. Review cuối: `456df18..<cuối>` + bằng chứng có phí.

- **B2a âm ⇒ giữ V0** (Q2: V1 +0, V3 +1, V2 +0 / 12; khoá `e0ca48c`). **C138:** câu hai ý 0 / 38 ⇒ không cần.
- **B2b ĐẠT (Q8):** Đủ 18 câu nhiều nguồn **+1,17** [+0,44; +2,00] (6 / 12 / 0), test không ngược; N_AA đường công cụ 5 / 5 ⇒ ngưỡng 8; Golden Đủ / Đúng TB +0,22; F1–F4 0; từ chối nhầm 12 ⇒ 4 / 6; S-AT: **1 P0_sai mới thật** (S20, thêm lời khuyên chung không có trong nguồn — không đảo cảnh báo; 2 / 3 ↔ 0 / 3) ⇒ dùng 1 / 2 suất cả Phase. Tiền B2 0,2478 / 0,45.
- **User quyết 11:16 03/11/2026 (hộp chọn): GIỮ `tim_them`; sửa ở B3** — plan B3 thêm dòng lời dặn "chỉ nêu điều có trong nguồn, không thêm lời khuyên chung" + kiểm lại S20 trong lượt an toàn B3. Theo dõi: router đưa S20 sang `khan_cap` 1 / 3 lần sinh lại. ⇒ B: mặc định `tim_them` true ⇒ Q7 ⇒ cổng Q9 ⇒ C review nhánh ⇒ A merge.

### C134 — review delta `p9-b1` (C) — **giao 09:00 03/11/2026** (delta `7e190d7..dcd1519`; trước ca dương tổng hợp C133) — **XONG 09:09 03/11/2026: ready_for_user_confirmation** (`b129_review.md` `4730a847d853` "Vòng cuối": 0 blocker / 0 major / 1 minor m-3 `generate` không `--flags` nay có định tuyến ⇒ ghi guide 6 / LUONG lúc merge; m-1 / m-2 vòng sớm đóng; 32 / 32 an toàn giống byte (HTTP, định tuyến thành công); P6 `190a6999c43b` = `main`; ngắt thật trước + giữa chữ đạt; ≈ 0,0006 USD)
- `7e190d7..<cuối>` vào `b129_review.md` theo `risk-gated-agent-review`; chạy lại ca dò byte HTTP P6 + 1 ca ngắt thật; ≈ 0,0005 USD. Đạt ⇒ A merge ⇒ 5 chỗ báo cáo. P2 kín bỏ (`today_line` tắt).

## (cũ) Việc đang mở — phiên tối 02/11 (User "làm đi" theo kế hoạch tuần, A ghi nhận 18:32 02/11/2026)

Đợt: `report_agent/2026-11-02_phase_9_code/` (report từng việc). Dữ liệu chạy: `data/phase_9/<việc>/` (private). Spec: bản 9 sha `169c2dd5f86a` — đọc §3–§5, §7–§8 (full-read §5 phần bậc mình làm).
Tài liệu cũ cùng Phase (W46, `find` 18:27 02/11): `guides/phase_9_agentic_rag_roadmap.md` (đã thay — chỉ reference), `…_design_review.md`, `…_design_review_v6.md`. Không có lượt đo latency trong phiên này (W31 không chặn).

### B125 — viết plan B0 (B, `hue-rag-e7`) — **bản 2 19:08 02/11/2026 (sửa theo review C124 M-1, m-1…m-4), sha `c126e7432c82` — chờ C kiểm phần sửa**; bản 1 `592a519bdd91`; 0 USD
- **Mục tiêu:** plan B0 theo spec §5 B0 + "Kế hoạch chi tiết tuần" ở trên (gồm 3 câu B hỏi / A trả lời và 2 rủi ro B / C ghi). Chỉ viết plan, **chưa code**.
- **Đọc:** spec §3, §4, §5 B0, §7, §8 (full); `data/nghien_cuu_phase_9_2026-11-01/agent/b123_sdk_probe.md`; `backend/llm/grounded_answer.py`, `backend/retrieval/full_corpus.py` (targeted).
- **Đầu ra:** `docs/superpowers/plans/2026-11-02-phase-9-b0-plan.md`, đầu file có mục **"Căn cứ để review"** (2–4 file, mục cần đọc); tiêu chí ghi trước: S-T1 giống byte, `answer_case` qua lõi chung = chuỗi gửi model giống byte + T1 giống byte, test danh sách module được import client mạng, không công cụ nhận URL, log đủ trường (USD + ms mỗi lần gọi / câu / tuyến), grep câu hỏi / mã phiên trong log = 0; không để hai lõi.
- **Không làm:** sửa code / test, gọi API trả phí (plan 0 USD; ước tiền lượt kiểm B0 ≈ 0,003 USD ghi trong plan), mở bộ đo kín của C.
- **Xong ⇒** báo A sha plan (tính từ file); A giao C review (C124). Người viết không sửa plan sau khi báo sha.

### C122 — bước 0 khẩn cấp (C, `hue-rag-cc`) — **XONG 18:38 02/11/2026, chờ User đọc** (report `c122_khan_cap_buoc0.md` `60b0c14b9e72`; bản cho User `data/phase_9/khan_cap_buoc0/doc_cho_user.md` `b4aca2f4770c`; 10 / 10 câu từ chối chuẩn, 0 nguồn; 0,0025 USD)
- **Mục tiêu:** spec §5 B0 "Bước 0 khẩn cấp": ~10 câu khẩn cấp **tự viết** (cháy, trẻ lạc, đuối nước, cấp cứu, ngộ độc…; người dùng thật gõ, có dấu) qua chatbot hôm nay ⇒ **User đọc** 10 câu trả lời.
- **Cách chạy:** server tạm cổng trống (`cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng>`), gọi `/api/chat`; tắt bằng TaskStop (không `pkill -f`). Trần **0,01 USD** (ước 0,003); ghi token + USD từ log.
- **Đầu ra:** câu + trả lời ở `data/phase_9/khan_cap_buoc0/` (private); bản để User đọc dạng dễ đọc trong cùng thư mục; report ngắn `report_agent/2026-11-02_phase_9_code/c122_khan_cap_buoc0.md` (mức loại câu, không chép câu trả lời). Không tự kết luận "cần / không cần" — User đọc rồi quyết.
- Câu này dùng lại làm bộ khẩn cấp "đã thấy" của B1.

### C123 — viết bộ đo B1 + mẫu Golden ~30 câu (C) — **XONG 18:44 02/11/2026; phần kín khẩn cấp (C125) xong 19:07** (report `c123_bo_do_b1.md` `8293d7acf873`; mục lục `data/phase_9/bo_do_b1/README.md` `e34248dd5749`; `khan_cap_sealed.jsonl` `15a41db0c741` 8 + 8 câu; 0 USD)
- **Mục tiêu:** spec §4 + §5 B1: bộ tuyến (~40 đã thấy + phần kín; có 5 ca lái tuyến), bộ ngày (dùng lại 15 câu `data/do_cuoi_2026-11-01/ngay/`; 12 câu quyết), bộ khẩn cấp (10 câu C122 + phần kín); mẫu Golden ~30 câu từ cả 176 (6 / loại × 5 loại, seed ghi trước, chỉ hồi quy).
- **Đầu ra:** `data/phase_9/bo_do_b1/` (phần kín tên `*sealed*`; **B không mở**); report `report_agent/2026-11-02_phase_9_code/c123_bo_do_b1.md` (số đếm, md5, cách chọn — không nội dung câu). 0 USD.
- Ưu tiên: khi B báo plan B0 xong ⇒ C dừng C123, làm C124 trước.

### Quyết định khẩn cấp (User, A ghi nhận 19:00 02/11/2026)
- User đọc kết quả C122 qua tóm tắt của A ⇒ **"chỉ từ chối" câu khẩn cấp = LỖI, sửa gọn ở B1**: luật code nhận câu khẩn cấp ⇒ câu soạn sẵn cố định (113 công an · 114 cứu hoả / cứu nạn · 115 cấp cứu), không sơ cứu, không vào model.
  Số phải kiểm nguồn công khai (B126). Sàn spec §5 B1 giữ: 0 câu khẩn cấp vào model; 0 câu thường bị chặn.
- Bộ khẩn cấp có **phần kín** (A quyết, lệch spec §4 "10 / —"): luật do B viết sau khi thấy 10 câu ⇒ cần câu chưa thấy để bắt luật khớp riêng; C viết ~8 câu khẩn cấp kín + ~8 câu thường dễ nhận nhầm, B không mở.

### B126 — kiểm số khẩn cấp Việt Nam (B) — **XONG** (0 USD; `data/phase_9/so_khan_cap.md`; Codex mở 0 trang ⇒ B WebFetch / pdftotext từng nguồn; A WebFetch kiểm lại 2 nguồn 19:06 02/11/2026: Học viện PCCC 30/09/2026 — 113 / 114 / 115 khớp; Báo Chính phủ 15/09/2025 — 112 khớp, miễn cước)
- **A quyết câu soạn sẵn B1 (19:06 02/11/2026, chi tiết trong phạm vi):** nêu **113** công an · **114** cháy, cứu nạn · **115** cấp cứu · **112** thiên tai / lũ lụt (Huế hay lũ; nguồn chính thức, miễn cước). Không nêu số địa phương, không "đã gộp về 113", không hứa gọi khi không SIM.
- **C127 xong — A chọn Bản 1** (19:22 02/11/2026): `data/phase_9/cau_khan_cap_soan_san.md` `e25f6c6b0126`, một câu chung 5 dòng (4 số + nói rõ ở đâu + trợ lý không gọi hộ + 1 dòng tiếng Anh) — code B1 chỉ cần "có khẩn cấp không", không phân loại (tránh nhấn nhầm số ở ca lẫn loại); Bản 2 (dòng đầu theo loại) để sau nếu cần.
- (cũ, nay C128) **C rảnh có lý do:** chờ B127 xong để review cả nhánh `p9-b0` (C là người review; việc khác dễ chồng file B đang sửa).
- **Trước bảo vệ / deploy:** kiểm lại — Bộ Công an Kế hoạch 642 (07/08/2026) gộp 113 / 114 / 115 về 113, giai đoạn 1 tới 2027 (B126).

**Plan B0 DUYỆT — bản 2 sha `c126e7432c82`** (A duyệt 19:20 02/11/2026, sha tính từ file; review C124 vòng 2 ready `…_plan_review.md` `afa3ed23cc68`). ⇒ **B127 code B0** trong worktree nhánh `p9-b0` theo plan; trần B0 0,01 USD; xong ⇒ report `report_agent/2026-11-02_phase_9_code/b127_b0_implementation.md` ⇒ C review cả nhánh ⇒ cổng ổn định ⇒ A merge.
  **B127 xong 19:36 02/11/2026 — chờ review (C):** nhánh `p9-b0` commit `215a77f` (đã push), worktree `/tmp/b_p9b0`; T-1…T-9 PASS (T1 `4d5bbe9e0edc`; chuỗi gửi model = HEAD 176 / 176 + 20 / 20); ≈ 0,0020 USD; report `b127_b0_implementation.md`.
  **B128 plan B1 bản 1 19:41 02/11/2026:** `docs/superpowers/plans/2026-11-02-phase-9-b1-plan.md` sha `0bc74ed957e7` — chờ review (người khác B); 0 USD. **Bản 2 19:51 02/11/2026** sha `0c9e137b56af` (sửa theo C129) — chờ C kiểm phần sửa.
**B127 xong (19:37 02/11/2026 A ghi nhận):** nhánh `p9-b0` `215a77f` (push, chưa merge); T-1…T-9 PASS theo report `b127_b0_implementation.md`; ≈ 0,0020 USD; A kiểm `git grep grounded_answer` = 0. ⇒ **C128 review cả nhánh — XONG 19:43 02/11/2026: ready_for_user_confirmation** (0 blocker / 0 major / 1 minor m-1 `/api/chat` bỏ `llm_calls` khi lượt lỗi sau khi model đã trả lời; `b127_review.md` `18829b0e9c12`; T-1 chạy lại `4d5bbe9e0edc`, T-2 ca dò byte HTTP giống hệt HEAD ×2 / nhánh, ngắt giữa stream chạy thật đúng plan; ≈ 0,0007 USD).
**B129 khoá (20:24 02/11/2026 A ghi nhận):** nhánh `p9-b1` `7e190d7` (push); đã thấy: P6 PASS (4 cờ tắt = B0, 176 + 20), P3 luật bắt 14 / 14, chặn nhầm 0 / 249, P1 r2 253 / 253 (r1 phạm sàn 1 ở 1 câu ⇒ chỉnh lời dặn định tuyến 1 vòng trên phần đã thấy), sàn 2 0 / 8; ≈ 0,041 USD. Chưa chạy: P2 (B đang làm), P5 hồi quy 208 + judge (phiên sau). ⇒ **C131 chạy phần kín P1 + P3 — XONG 20:28 02/11/2026** (`c131_kin_b1.md` `53a3ce1fe6a6`; khoá 6 / 6 khớp): **P1 kín 20 / 20, sàn 1 = 0, sàn 2 0 / 5**; **P3 kín: luật bắt 0 / 8 (+ 0 / 2), chặn nhầm 2 / 8 câu thường ⇒ (a) không đạt ⇒ theo luật ghi trước tắt `emergency_rule`**; định tuyến bắt 10 / 10 câu khẩn cấp kín; 0,002384 USD.
  **B129 kết phiên (20:34 02/11/2026, B ghi): PARTIAL — chờ judge P5.** P2 đã thấy không đạt (từ chối nhầm 5,0 ⇒ 4,5; vòng chỉnh 1 cũng 4,5) ⇒ `today_line` tắt; cổng ổn định 4 tuyến × 2 đường + Playwright đạt; P5 sinh xong (S-OOS 18 / 18, từ chối nhầm 12 / 158 = mốc, 0 lỗi) — **judge Đủ / Đúng + S-AT NOT RUN**. Tiền B1 ≈ 0,140 USD (B) + 0,0024 (C). Report `b129_b1_implementation.md`; lệnh chạy tiếp ở `STATUS_B.md`.
- **C131 phần kín (20:29 02/11/2026):** P1 kín 20 / 20 đúng tuyến, sàn 1 = 0, sàn 2 0 / 5; **P3 kín: luật bắt 0 / 8 khẩn cấp, chặn nhầm 2 / 8 câu thường** (luật khớp quá sát phần đã thấy) ⇒ theo luật ghi trước **tắt `emergency_rule`** (A quyết 20:29 02/11/2026); định tuyến bắt 10 / 10 câu khẩn cấp kín ⇒ vẫn trả Bản 1 (chuỗi soạn sẵn), thêm 1 lần gọi định tuyến. Sàn spec "0 câu khẩn cấp vào model" **không đạt nguyên văn**; ý an toàn (model không viết lời khuyên khẩn cấp) giữ qua định tuyến — báo User. Không sửa luật theo câu kín. 0,0024 USD.
- **Cờ B1 (B đề xuất, A đồng ý 20:30 02/11/2026, theo luật ghi trước):** `router` BẬT (253 / 253 + kín 20 / 20); `may_have_changed_notice` (H4c) BẬT; `emergency_rule` TẮT (kín: bắt 0 / 8, chặn nhầm 2 / 8); `today_line` TẮT (P2 đã thấy: từ chối nhầm TB 5,0 ⇒ 4,5, cần giảm ≥ 3 — kết quả âm, gốc ở tầng tìm / model như C93). Nhánh hiện để cả 4 cờ mặc định `false` ⇒ **trước merge phiên sau: đổi mặc định `router` + `may_have_changed_notice` = true** (sau khi judge P5 đạt). P5 sinh 208 câu đang chạy (≈ 0,07 USD); **judge P5 NOT RUN** ⇒ phiên sau; **B1 chưa merge**. Tiền B1 ≈ 0,073 + P5.
- **C132 (C) XONG 20:34 02/11/2026, 0 USD:** review sớm phần đã khoá `a406bea..7e190d7` ⇒ `b129_review.md` `865445ba1461` "Vòng sớm": **0 blocker / 0 major / 2 minor** (m-1 route ghi log trước `aclose()` lõi ⇒ ca ngắt lúc gửi có thể mất `llm_calls`; m-2 đường ngắt qua lõi mới chưa chạy thật ⇒ cổng cuối). P6 ca dò byte HTTP: `main` ×2 = nhánh (`190a6999c43b`); pytest 48 / 3 error (cần key). Review cuối chỉ xem `7e190d7..` (P2, P5).
- **Phiên sau B sửa (A):** m-1 C132 (`aclose` lõi trước khi ghi log) + m-2 (cổng cuối có 1 ca ngắt thật `curl -m`). **B130 (B, đang làm, 0 USD):** judge P5 nếu chạy tiếp được từ chỗ dừng; dừng 21:35. **C rảnh có lý do:** việc còn lại B1 là của B; review cuối cần nhánh xong.
- **B130 XONG (20:45 02/11/2026):** judge P5 Golden 311 / 311 điểm; sàn F1–F4 đạt; Đúng đạt; từ chối nhầm 12 = 12; Đủ TB −0,023 [−0,070; +0,023] nhưng **6 câu tụt > ngưỡng 5**. Lần gọi trả lời giống byte B0 176 / 176 ⇒ **A chọn dùng lại theo spec §4 dòng 158** (nhiễu sinh lại cùng đầu vào; ghi trung thực). S-AT: phiên sau B kiểm giống byte trên 32 câu an toàn (0 USD) ⇒ giống thì dùng lại S-AT 01/11; không sinh A/A. Tiền B1 tổng ≈ 0,142 USD.
- **Theo dõi tốc độ (A, cần báo User):** định tuyến thêm p50 1,7 s / p95 2,7 s mỗi câu; chữ đầu tuyến trợ lý 4,9 s ở cổng (1 câu) — trước B1 p50 1,23 / p95 2,61 s ⇒ có thể vượt sàn cũ p95 ≤ 5 s tới chữ đầu. Spec Phase 9: tốc độ chỉ theo dõi (chất lượng trước). Ứng viên tối ưu sau: chạy định tuyến song song với tìm kho / model định tuyến nhỏ hơn — đo ở B7 hoặc thí nghiệm riêng.
**Plan B1 DUYỆT — bản 2 sha `0c9e137b56af`** (A 19:54 02/11/2026, sha tính từ file; C129 vòng 2 ready, review `…b1-plan_review.md` `d00e0d9508c1`). ⇒ **B129 code B1** trong worktree nhánh `p9-b1` từ `main` mới; trần B1 0,25 USD (dừng > 0,21); 21:40 chưa xong ⇒ commit WIP lên nhánh + STATUS_B. Phần kín: C chạy sau khi B ghi dòng "Khoá" (sha) vào report.
**C rảnh có lý do (19:54 02/11/2026):** chờ B129 (review cả nhánh + chạy phần kín) — việc khác dễ chồng file B1.
**B0 MERGE 19:49 02/11/2026: `main` `1c10111`** (A; C128 ready `b127_review.md` `18829b0e9c12`; code `main` = nhánh — dùng lại bằng chứng cổng của B127 / C128; A chạy lại trên `main`: pytest có key **222 / 222 pass**). 5 chỗ báo cáo xong (LUONG mục 9, BAO_CAO_SINH bản 19, Project_Status §2 / §4, guide 6 "Hiện hành", nhật ký `2026-11-02_toi_phase_9_b0.md`) + mục lục. Nhánh `p9-b0` còn (origin + local) ⇒ đề xuất xoá lúc kết phiên.
**C129 review plan B1 bản 1: changes_requested** (3M / 5m, `…b1-plan_review.md` `aa344a4cf5cb`). **A quyết 19:49 02/11/2026:** M-1 đồng ý (C130 gán nhãn 18 câu Golden out_of_scope, ghi trước, tính vào sàn 1); M-2 tách sàn — (a) "0 câu thường bị chặn" trượt ⇒ tắt luật, (b) độ phủ phần kín chỉ báo số, sót ⇒ kết quả âm, không tắt / không sửa luật theo câu kín (cách hiểu dòng spec §5 B1 "không đạt ⇒ tắt luật" — báo User); M-3 (b) lỗi Qdrant giữa luồng ⇒ SSE error là đổi cố ý, giữ đúng câu 503 cũ; m-5 bỏ kiểm `[n]` ở trò chuyện. ⇒ B sửa plan bản 2; C130 đang làm.
**B128 XONG 19:42 02/11/2026 — plan B1 bản 1 sha `0bc74ed957e7`** (A tính từ file) ⇒ C129 review plan sau C128. **C129 XONG 19:47 02/11/2026: changes_requested** — 3 major (M-1 Golden `out_of_scope` 7 / 18 câu nhắc Huế bị loại khỏi sàn 1; M-2 P3 "sót kín ⇒ tắt luật" đi ngược — A quyết; M-3 P6 không phủ hợp đồng lỗi SSE khi tắt cờ — A quyết) + 5 minor; review `…_b1-plan_review.md` `aa344a4cf5cb`. **Vòng 2 19:53 02/11/2026: ready_for_user_confirmation trên bản 2 `0c9e137b56af`** (8 / 8 đóng; review `d00e0d9508c1`). A quyết trước: D7 dòng ngày đầu tin nhắn người dùng thay vì lời dặn (lệch chữ spec §2, cùng ý "code giữ ngày"; lời dặn giữ hằng — A chấp nhận, báo User lúc kết phiên); trần B1 0,25 USD (dừng > 0,21); 3 chuỗi chữ cho người dùng (ngoài phạm vi, H4c, nhãn tuyến) A chọn sau review, báo User. (cũ) **B128 — plan B1 (B, đang làm, 0 USD):** `docs/superpowers/plans/2026-11-02-phase-9-b1-plan.md` theo spec §5 B1 + quyết định khẩn cấp Bản 1; B không mở `*sealed*`. Người review plan: C (sau C128).
**User 19:20 02/11/2026: "làm đi, đừng hỏi tôi"** ⇒ A tự quyết trong quyền phiên (≤ 1 USD, A commit / push), chỉ báo kết quả; việc luật bắt User `!` (xoá dữ liệu / nhánh) vẫn đưa lệnh.
**C126 xong** (`c126_uoc_loi_cache.md` `9bd3b71716aa`): khoá cố định lợi ≈ 0 (tiền tố chung ≈ 148 token < ngưỡng 1.024); tắt ghi đệm −13,3 % / câu. **A quyết:** không làm bây giờ (đã dưới sàn tiền, chất lượng trước) ⇒ danh sách "tối ưu tiền sau khi ổn"; plan B3 (nhớ hội thoại) xét khoá theo phiên.
(cũ) **B rảnh có lý do:** chờ C124 (~20–30 phút); việc kế của B = sửa plan theo review ⇒ code B0 — giao việc khác dễ chồng file / lộ bộ đo B1.

### C124 — review plan B0 (C) — **Vòng 2 19:10 02/11/2026: ready_for_user_confirmation trên bản 2 `c126e7432c82`** (5 / 5 finding đóng; review `afa3ed23cc68`). Vòng 1 19:05: changes_requested (1 major M-1 T-2 chuỗi gửi model không ổn định trên HEAD + 4 minor; review `…_b0-plan_review.md` `b4f8be175140`; C chỉ kiểm lại phần sửa) (giao 19:00 02/11/2026; bản sha `592a519bdd91`; chú ý D3 ranh giới mạng, D6 vòng stream ở `chat.py` ↔ spec §3, giờ ước "18:3x" trong plan = minor). Sau đó: phần kín bộ khẩn cấp (C125).
- Chỉ dựa "Căn cứ để review" trong plan (không đọc STATUS / tin nhắn của B); `risk-gated-agent-review`; ghi `docs/superpowers/plans/2026-11-02-phase-9-b0-plan_review.md`. Đạt ⇒ A duyệt sha (tính từ file).

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. **Quyền phiên.** A khuyên: như 02/11 (A tự điều phối + tự thử trong luật; ≤ 1 USD / phiên; A tự commit / push; B / C push nhánh riêng).
2. ~~**Xoá nhánh `giao-dien-moi`**~~ **XONG 15:15 02/11/2026** (User `!` xoá local + origin). Cũ: (local + origin): đã merge `ed8e6e8`; `git log main..giao-dien-moi` rỗng (A kiểm 14:52 02/11/2026) — User `!`
   (`git branch -d giao-dien-moi` + `git push origin --delete giao-dien-moi`).
3. **Rà bảo mật C106** (`report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` bản 2): **R4 XONG 21:29 02/11/2026** (User `!`: sao lưu `/tmp/application_log_truoc_cat.log`, cắt; còn 0 dòng "Received question", dòng `chat_metrics` giữ nguyên). Cũ: User chọn cắt 22 dòng log cũ "Received question" (A ghi nhận 18:35 02/11/2026; A đếm lại 22) — khi **không server nào chạy** (sau C122), sao lưu rồi User `!`; các mục deploy để lúc deploy.
4. **Sổ cải tiến:** W35 **User không chọn** (18:38 02/11/2026: over-engineer — đồ án, chỉ tra cứu web). W42, W43: A **không hỏi lẻ** nữa (User muốn tiến Phase 9, ít nghi thức) — xét gộp ở vòng cải tiến kết phiên, mặc định đề xuất bỏ trừ khi có sự cố mới.
5. Không gấp: 4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`, nhánh `subagent-Monuments-Reviewer-*`) giữ hay gỡ (User `!`)? Xoá sao lưu kho đợt 1 + 2?

## Câu hỏi A còn nợ (không cần User)

- **Câu C hỏi A (C, kết phiên 02/11; A trả lời sẵn 15:12 02/11/2026 — kỹ thuật trong phạm vi):**
  1. Phân công người code B1–B3 ⇒ **A quyết lúc giao**, giữ luật "người viết bộ đo ≠ người code bậc đó" (vd B code B0–B2, C viết bộ tuyến / ngày / nhớ; nếu C code B3 thì B viết bộ nhớ).
  2. Mẫu Golden ~30 câu ⇒ **đồng ý: lấy từ cả 176**, 6 câu / loại × 5 loại, seed ghi trước (chỉ hồi quy, không dùng chọn biến thể).
  3. 10 câu bước 0 khẩn cấp ⇒ **đồng ý dùng lại làm bộ khẩn cấp "đã thấy" của B1** (phần kín viết thêm riêng).
- **Câu B hỏi A (B, kết phiên 02/11; A trả lời sẵn — kỹ thuật trong phạm vi):**
  1. B0 giữ đường RAG 1–8 y nguyên qua lõi mới (code gọi `tim_kho`, sinh 1 lần, `max_turns=1`); vòng công cụ do model gọi để B2b (hoặc B2a nếu đo V2) ⇒ **đúng ý spec** (§5 B1: `tro_ly_hue` = đường RAG 1–8, chưa công cụ).
  2. "Chỉ một module gọi mạng ngoài" ⇒ **mỗi nhà cung cấp một module** (OpenAI: generator hiện có; Serper: module mới ở B6) + test kiểm **danh sách module cho phép** import client mạng (`openai`, `httpx`, `requests`…); ghi rõ câu này trong plan B0.
  3. Chọn + khoá mẫu Golden ~30 câu ở B0 ⇒ **C** (người không code), seed ghi trước.
  - **Rủi ro B ghi cho plan B0:** đã có lõi chung `backend/llm/grounded_answer.py` ⇒ `assistant.py` bọc / thay, **không để hai lõi**; S-T1 qua `tim_kho` so danh sách chunk bên trong, không so chữ đã định dạng.
  - **Ghi cho plan B0 (rủi ro C thấy trước):** tiêu chí "`answer_case` ra đúng câu trả lời đường RAG 1–8" phải đo bằng **chuỗi gửi model giống byte + T1 giống byte**, không so chữ trả lời (model không tất định).

- **C126 (C, đang làm, 0 USD):** ước lợi thí nghiệm cache key bằng số từ log + tra tài liệu OpenAI ⇒ `report_agent/2026-11-02_phase_9_code/c126_uoc_loi_cache.md`; ưu tiên kiểm plan B0 bản mới nếu B báo.
- **Ứng viên tối ưu tiền (giả thuyết, C124 phát hiện, A kiểm 19:07 02/11/2026):** SDK 0.19.4 gán `prompt_cache_key` = `agents-sdk:run:<ngẫu nhiên>` mỗi `Runner.run` (`agents/run_internal/prompt_cache_key.py:124-129`); 40 dòng `chat_metrics` gần nhất `cached_tokens` = 0, `cache_write_tokens` ≈ 1.872 / câu ⇒ mỗi câu trả giá ghi đệm (0,125 / 1M, đắt hơn vào thường 0,10) mà không đọc lại. Phần chung giữa các câu chỉ là lời dặn (10 đoạn kho khác nhau mỗi câu) ⇒ lợi có thể nhỏ. Làm **thí nghiệm riêng sau B0** (`run-experiment`: key cố định ↔ hiện tại, đo USD / câu + chữ đầu), không trong B0.
- Bảng sổ cải tiến: S41–S44 thiếu 1 cột từ trước. W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức tín dụng phía OpenAI cho key — chưa kiểm. Hạn mức trả trước phía Serper — đặt khi tới B6.

## Session

**Phiên 03/11 (mở 08:36):** A `hue-rag-5e` · B `hue-rag-52` · C `hue-rag-d8` — cả ba Claude Code, trực tiếp. Bảng dưới là phiên tối 02/11.

| Vai | Terminal (phiên tối 02/11, mở 18:27) | Agent | Liên lạc | Phiên tối 02/11 | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-24` | Claude Opus 5.5 | trực tiếp | điều phối; merge B0; 5 chỗ báo cáo; vòng cải tiến 15 | `STATUS_A.md`; 0 USD |
| B — thực thi | `hue-rag-e7` | Claude Opus 5.5 | trực tiếp | B125 plan B0, B126 số khẩn cấp, B127 code B0, B128 plan B1, B129 code B1 (PARTIAL), B130 judge P5 | `STATUS_B.md`; ≈ 0,142 USD |
| C — thực thi | `hue-rag-cc` | Claude Opus 5.5 | trực tiếp | C122 khẩn cấp, C123 / C125 bộ đo B1, C124 / C129 review plan, C126 cache, C127 câu soạn sẵn, C128 review B0, C130 nhãn, C131 phần kín, C132 review sớm B1 | `STATUS_C.md`; ≈ 0,0055 USD |

Phiên sáng / chiều 02/11 (terminal cũ `hue-rag-7e` / `-d6` / `-29`): B121–B124, C118–C121 — `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên 03/11** (User: "quyền của A như 02/11", A ghi nhận 08:46 03/11/2026): A tự điều phối + tự quyết trong kế hoạch; ≤ 1 USD / phiên; A tự commit / push; B / C push nhánh riêng. Hết hạn cuối phiên. User: C làm trực tiếp với A, việc A giao = "làm đi".
- **Phiên tối 02/11 — HẾT HẠN (kết phiên 20:47 02/11/2026)** (User chọn "như 02/11", A ghi nhận 18:32 02/11/2026): A tự điều phối + tự thử trong luật; ≤ 1 USD / phiên; A tự commit / push (hỏi User trước theo luật chung); B / C push nhánh riêng. **Kết phiên 22:00 02/11/2026** (User, nói lúc 18:32) — A bắt đầu kết phiên ~21:30; B / C ghi STATUS + report dở trước ~21:40.
- (cũ) **Phiên 02/11 — HẾT HẠN cuối phiên** (User, A ghi nhận 09:48 02/11/2026): như 01/11 — A tự điều phối + tự thử; ≤ 1 USD; A tự commit / push; B / C push nhánh riêng. Tiền phiên 02/11 ≈ **0,003 USD** paid
  (B ≈ 0,002 · C ≈ 0,0006 · A 0; sub-agent + judge dùng quota Claude).
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
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`:
  `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop — **không `pkill -f`**, bẫy §8);
  (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ 5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31). Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ (W45). `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 02/11 nguyên văn (B121 giao diện, B122 / B123, C118–C121, các quyết định agent theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/` (`b121_giao_dien_implementation.md`, `b121_review.md`); hướng chọn B116 `report_agent/2026-11-01_giao_dien_moi/`.
- Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + lượt đo cuối Phase 1–8 (01/11): `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
