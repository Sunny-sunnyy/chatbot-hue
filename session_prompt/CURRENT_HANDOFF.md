# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 18:45 12/11/2026 (A, mở phiên 12/11 — giao việc). Trước: 16:24 11/11/2026 (A, kết phiên chiều 11/11). Trước: 10:43 11/11/2026 (A, kết phiên sáng 11/11).
Nguyên văn handoff trong phiên 10/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-10.md`; 09/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-09.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-10_toc_do_xa_giao_cau_ngay.md`.

## VIỆC PHIÊN 12/11 (A giao 18:45 12/11/2026; quyền "như 10/11")

Terminal: A `hue-rag-7d` · B `hue-rag-1b` · C `hue-rag-e1` · E `hue-rag-33` (cả bốn Claude Code, trực tiếp; mọi session phiên này chạy Fable 5.2). Qdrant **đang chạy** (2 collection, 8.435 điểm) — dòng "Qdrant tắt" bên dưới đã cũ.
Luật chung: mục "Việc đang mở — luật chung" cuối file. Máy ~15 GB RAM ⇒ **mỗi lúc chỉ một session chạy server / model** (B trước; C cần server thì nhắn B). Không ai đo tốc độ phiên này.

| Session | Việc | Đọc | Làm / không làm | Tiền | Đầu ra | Trạng thái |
|---|---|---|---|---|---|---|
| **B** | **B7 bước 0** (kiểm trước lượt có phí) + probe log truy cập | plan nháp `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` §2, §4 (full-read); "Câu hỏi cho User" Q-DP ý log uvicorn | (1) worktree `/tmp/b7_moc` ở tag `p9-moc`: khởi động được với build record hiện tại, `/health` 5 / 5, T1 158 câu = mốc `64656a87c109`; khác ⇒ dừng, báo A, không sửa code cũ. (2) bản sao harness vào `data/phase_9/b7/tools/` (chỉ đổi hằng số build record / số điểm). (3) một lần chạy server `main` thật: log truy cập uvicorn có in IP không (chỉ `/health`). **Không** chạy lượt có phí, không mở `*sealed*`, không sửa code `backend/` | 0 USD | `report_agent/2026-11-08_phase_9_ban_13/b7_buoc_0_implementation.md` | **chờ review** (18:50 12/11/2026): 3 / 3 đạt — code mốc `/health` 5 / 5, T1 giống byte `64656a87c109`; log truy cập không in IP; harness cần sửa hơn hằng số (report §5). **18:55 12/11/2026: harness hai bên + runner chuỗi phía RAG xong, chạy thử 0 USD đạt (report §7); chờ plan bản 2 duyệt sha rồi pilot** **19:54 12/11/2026: B7 GIỮA KỲ phần đã thấy XONG — chờ review E** (`b7_implementation.md`): (i) tốt hơn ở cả 3 nhóm; S-G đạt (tụt 4 = ngưỡng); **phạm S2b (2 câu) + S1 thiếu cảnh báo mới (1 câu)**; 0,288 / 0,35 USD; phần kín C / S / T chờ User `! bash data/phase_9/b7/tools/chay_kin.sh`; biểu mẫu 12 tổ hợp chưa chạy lại |
| **E** | **Review plan B7** (người viết là C) | plan nháp (full-read) + căn cứ ghi ở đầu plan (spec Phase 9 §4, §5 B7, §8, §11.5, §12.3, §12.4 — targeted) | review theo `risk-gated-agent-review`, chỉ dựa plan + spec + lệnh chỉ đọc; xét cả "lượt nào không giữ sàn nào ⇒ cắt"; cờ ở `main` hôm nay so với danh sách cờ trong plan §2. Không đọc STATUS_C | 0 USD | `docs/superpowers/plans/2026-11-10-phase-9-b7-plan_review.md` | **vòng 1 xong 18:49 12/11/2026 — changes_requested** (3 major: bản sao harness không chạy được như ghi · cách tính (i) chưa ghi trước · S2 / S2b + vế "0 truy vấn chứa tên" thiếu lượt đo; 6 minor; cờ khớp 14 / 14). **Vòng 2 xong 19:02 12/11/2026 — ready** (bản 2 sha `da7bff5d0c4e`: 0 major, 5 minor không chặn; 7 câu ngày kín không mở — đạt) ⇒ A duyệt sha |
| **C** | **Đợt 2 cổng — lượt đếm rẻ trước khi xây** (lưu trú · ăn gần · sự kiện theo ngày) | spec cổng đợt 1 D2 + §4 "Ngoài"; nghiên cứu đợt 2 cũ của C (C209); `Session_Prompt.md` §7 "Đếm lỗi trước khi xây" | với **mỗi** ý trong 3 ý: trên hệ thống đang chạy (log `chat_metrics` / `chat_feedback`, bộ đã thấy, kho qua `scripts/grep_kb.sh`) đếm người hỏi loại câu đó thì hôm nay ra sao (trả lời được từ kho · từ chối ⇒ web · sai) ⇒ kết luận "đủ lỗi để xây / không xây" kèm số đếm. Ưu tiên dữ liệu có sẵn; cần gửi câu mới thì ≤ 30 câu tự viết. **Không** viết spec / code, không mở `*sealed*` | ≤ 0,02 USD | `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` (mức loại câu, không chép câu / kho) | **chờ review** (19:06 12/11/2026): 18 câu tự viết, 0,0247 USD — ăn gần đủ lỗi (5 / 6 không đủ dùng từ kho; lỗi ở dữ liệu định vị quán) · lưu trú đủ lỗi cho phần nhỏ (câu hỏi cơ sở cụ thể 3 / 4 từ chối) · sự kiện không đủ lỗi (4 / 6 kho trả lời) · 0 / 18 sai |

**Plan B7 bản 2 — A DUYỆT 19:03 12/11/2026:** bản review `da7bff5d0c4e` (E vòng 2 ready); file sau khi thêm dòng duyệt `456c13142879`; `$C_DONG` = `dfd0c96`; `KIN_NGAY` tắt; `MAX_DROP` 4; ước ≈ 0,31 USD (quỹ 0,35); người chạy B, review kết quả E. Lượt cuối (cuối tháng 12) cần quỹ riêng cùng cỡ — hỏi User khi tới.

**Ghi thêm (19:06 12/11/2026):** plan B7 sau sửa chữ n-3 (C) sha file `2ca3f63ce45b` — không đổi tiêu chí / tiền, không duyệt lại. **Đếm đợt 2 cổng (C, 18 câu, 0,0247 USD):** ăn gần **đủ lỗi** (5 / 6 không đủ dùng từ kho; gốc ở dữ liệu định vị bài quán, không phải thiếu bản đồ) · lưu trú đủ lỗi cho **phần nhỏ** (khu nên ở + link tìm phòng do code dựng) · sự kiện theo ngày **không đủ lỗi** (4 / 6 đủ dùng). B7 là đo giữa kỳ ⇒ điều kiện "đáng xây ⇒ hỏi User trước B7" không còn chặn; hai ý đủ lỗi vào danh sách tổng hợp trình User.

**B7 GIỮA KỲ — phần đã thấy xong (19:55 12/11/2026; B chạy, E đang review; số của B, chưa qua review):** tiền 0,288 / 0,35. (i) cả 3 nhóm đạt sau Holm: câu theo ngày dùng được 27 ↔ 11 / 28 · hỏi tiếp Đủ 5,00 ↔ 3,33 (9 lượt) · nhiều nguồn 4,44 ↔ 3,44 (18 câu). Golden 129 câu: Đủ +0,194 [+0,054; +0,357], câu tụt 4 = đúng ngưỡng; từ chối nhầm 3 ↔ 13; F1–F4 = 0. **Hai sàn PHẠM:** S2b 2 / 44 câu ngoài phạm vi mở cổng web · S1 thiếu cảnh báo mới 1 câu (S-AT agent 3 / 6 ↔ mốc 1 / 6) — C chẩn đoán 0 USD; sửa / nhận giới hạn ⇒ **User quyết**. Report `report_agent/2026-11-08_phase_9_ban_13/b7_implementation.md`. ~~Chờ User `!` phần kín~~ ⇒ bỏ ở giữa kỳ (chốt vòng tự soi 1).
**E review B7 giữa kỳ (20:02 12/11/2026): READY** (0 blocker / 0 major / 5 minor; E tính lại độc lập khớp mọi số chính; hai sàn phạm là phạm thật; `b7_review.md`). E đồng ý chẩn đoán C về S1 (điều kiện nằm ở đoạn model tìm thêm, mốc không có) nhưng vẫn là bỏ sót thật 5 / 8 lần ⇒ thước lượt cuối: đếm "thiếu mới" trên điều kiện có ở ngữ cảnh cả hai bên hoặc đòi hai người chấm cùng gắn — **User duyệt trước lượt cuối**. **Danh sách 7 việc sau khi đếm:** `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` mục 3d — chờ User chọn.
**Đếm 0 USD trên B7 (C, `c_phan_chua_on.md` mục 3b):** từ chối nhầm 3 / 3 là tìm trượt · tìm thêm cứu 10 / 10 câu (giữ) · 0 số tiền / giờ lạ / 155 câu · ổn định 0 / 76 câu đổi · 4 câu tụt = viết ngắn hơn, không đủ lỗi · đường web: 6 / 8 câu kho thiếu tốn một lượt xin tìm lần ba vô ích. **3 plan nháp chờ User chọn:** `docs/superpowers/plans/2026-11-12-{an-gan-dinh-vi-quan,het-luot-tim,nhan-loai-cau}-plan.md`.

**Vòng tự soi 1 — A chốt (20:04 12/11/2026; C + E đã gửi cả nhóm, B đang chạy lượt đo nên góp sau):**
- **Bỏ phần kín của lượt giữa kỳ** (bộ kín đã dùng: chuỗi / ngoài phạm vi / trò chuyện — không đổi quyết định nào hôm nay) ⇒ **không cần User chạy `chay_kin.sh`**; report B7 ghi ba mục đó "chưa kết luận ở giữa kỳ — để lượt cuối". 12 tổ hợp biểu mẫu **vẫn chạy** (nợ theo plan).
- **Lượt cuối làm nhẹ:** bộ ngoài phạm vi ×2 ⇒ ×1 (44 / 44 giống nhau hai lượt); không sinh lại S-AT cho điều kiện đến từ đoạn tìm thêm (báo riêng); plan lượt cuối chỉ sửa thước an toàn + công tắc kín + commit — không viết bản 3, chỉ review phần đổi thước; review kết quả chỉ tính lại số quyết (câu tụt, Holm, sàn phạm) + thủ tục.
- **Thước "thiếu cảnh báo mới" cho lượt cuối** (ghi trước khi sinh; User duyệt): đếm trên điều kiện có ở ngữ cảnh cả hai bên; "đổi nhãn" chỉ tính khi cả hai người chấm cùng gắn; điều kiện từ đoạn tìm thêm báo riêng, không dùng để hạ sàn. Kết quả giữa kỳ giữ chữ PHẠM.
- **Sửa harness trước lượt cuối (nhỏ, 0 USD):** file sinh ghi thêm số lần tìm / hết lượt, ms từng lượt gọi model, id đoạn tìm thêm.
- **Giữ (đã bắt lỗi thật hôm nay):** review plan trước lượt có phí · bước 0 chạy thử 0 USD · đếm lỗi trước khi xây (hạ 3 ứng viên, đổi đợt 2 thành việc dữ liệu) · tính lại độc lập số quyết · hai người chấm · mở trang gốc kiểm lời Codex · đọc từng ca thay vì tin số đếm.
- **Sửa chốt (20:05 12/11/2026, sau ý B + phản biện E):** phần kín giữa kỳ: **chỉ chạy phần chuỗi** (hỏi tiếp + nhớ tên, ≈ 0,02 USD — vế "kín không ngược chiều" của kết luận (i) và ngưỡng nhớ tên) khi User về chạy một lệnh `!`; bộ kín ngoài phạm vi + trò chuyện bỏ ở giữa kỳ. Vòng sinh lại S-AT **giữ 2 người chấm**, tính "thiếu" khi cả hai cùng gắn; cổng đối chứng 15 câu còn 1 lần / phiên chấm.
- **Rút kinh nghiệm:** xếp hạng sau khi đếm, không trước; tra repo / paper theo câu hỏi cụ thể, không theo hạn mức số mục; báo User chỗ "đúng ngưỡng, hết biên" (4 câu tụt; web 6 / 10) tách khỏi chữ "đạt". Đề xuất cho vòng cải tiến kết phiên: skill review thêm câu "sàn kiểu 'mới so với mốc' phải cùng mẫu số ở hai bên".

### Đợt rà khoảng cách (User giao 18:58 12/11/2026) — `report_agent/2026-11-12_ra_khoang_cach/`

**User (18:58 12/11/2026):** chưa deploy, chưa đóng Phase 9 (mốc đóng code vẫn 25–30/12). **B7 hôm nay = đo giữa kỳ** (trả lời "trợ lý đã hơn RAG 1–8 chưa, ở đâu"); lượt cuối chạy lại lúc đóng code ⇒ **bộ kín chưa mở `ngay_moi_sealed` 7 câu giữ cho lượt cuối, hôm nay không mở**. Đồng thời: rà khoảng cách tới agentic RAG; nghiên cứu repo (file `báo cáo nghiên cứu github.txt` + Codex tra thêm); thử đầy đủ Huế TRIPO bằng Playwright; rồi A tổng hợp "tính năng nào cần bổ sung · phần nào chưa ổn cần phát triển / tối ưu lại" trình User.

| Session | Việc | Đọc trước (để không đề xuất lại cái đã có / đã bỏ) | Làm / không làm | Đầu ra |
|---|---|---|---|---|
| **E** | **Rà khoảng cách agentic RAG + repo** | `guides/phase_9_agentic_rag_roadmap.md`; spec Phase 9 §2–§5; `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` (mục 000 + bảng 18 ý trong handoff + dòng "Không làm"); `data/nghien_cuu_phase_9_2026-11-01/báo cáo nghiên cứu github.txt`; `data/nghien_cuu_tinh_nang_2026-11-04/` (8 repo đã đọc); `Project_Status.md` §4; code `backend/llm/assistant.py` | (1) bảng "agentic RAG thường gồm gì · hue_rag có gì (`file:hàm`) · thiếu gì · lỗi tương ứng đã quan sát chưa"; (2) repo trong file github.txt **chưa đọc** ở 04/11 + ≤ 6 repo / tài liệu mới qua `scripts/tra_web_codex.sh` (chỉ thông tin công khai; WebFetch kiểm 2–3 ý chính); (3) ≤ 8 ứng viên xếp hạng, mỗi cái: lợi cho người dùng, lỗi đã thấy chưa, cách đếm rẻ trước khi xây. **Không** viết spec / code; 0 USD API. Ngắt giữa chừng để review plan B7 bản 2 khi C xong | `data/nghien_cuu_agentic_2026-11-12/` (hồ sơ) + `report_agent/2026-11-12_ra_khoang_cach/e_khoang_cach_agentic.md` |
| **B** | **Huế TRIPO vòng 5 bằng Playwright** (làm trong lúc chờ plan B7; **A báo sha plan ⇒ dừng TRIPO, chạy B7 trước**, xong quay lại) | các vòng cũ: `data/nghien_cuu_tinh_nang_2026-11-04/tripo_v3` + `sa2_tripo_v3_agentic.md`, vòng 4 ở `report_agent/2026-11-06_b5_cau_tu_nhien/`, giao diện ở `report_agent/2026-11-06_giao_dien_cong/` | kiểm kê **mọi** tính năng trang đang có hôm nay (đổi gì so với vòng 4) ⇒ bảng "TRIPO có · hue_rag có / không · chất lượng khi thử cùng câu"; cùng ≤ 20 câu tự viết gửi cả hai bên (hue_rag ≤ 0,02 USD). Chỉ trang công khai, không đăng nhập / đặt chỗ / gửi biểu mẫu, gửi thưa. Không chạy cùng lúc với lượt sinh B7 | `data/tripo_v5_2026-11-12/` + `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v5.md` |
| **C** | sau plan B7 bản 2 + đếm đợt 2: **rà trong dự án "phần nào chưa ổn"** | handoff "Giới hạn biết" + "Câu hỏi A còn nợ"; `bai_hoc/16` (chỗ còn yếu); log `chat_metrics` / `chat_feedback` | gom thành một bảng: phần chưa ổn · bằng chứng (số đo / log) · mức ảnh hưởng người dùng · sửa rẻ hay đắt. Chỉ đọc, 0 USD | `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` |

**A:** tổng hợp 3 báo cáo + kết quả B7 giữa kỳ ⇒ danh sách ngắn cho User chọn (propose-options, mỗi lần một câu).

**User chốt (18:46 12/11/2026):** **chạy B7 trong phiên này** — đóng phần hỏi đáp ở `main` hôm nay (bản đồ = hiển thị, giọng nói = cách nhập, không đổi câu trả lời ⇒ không chờ); **trần Phase 9 nâng 4,2 ⇒ 4,3 USD**; điều kiện: bước 0 của B đạt + plan qua review của E + A duyệt sha; C đếm ra "đợt 2 đáng xây" ⇒ A hỏi lại User trước khi chạy.
**Chờ User (A hỏi mỗi lần một câu):** góp ý `bai_hoc/` · các câu ở mục "Câu hỏi cho User".
**Lệch ghi nhận lúc mở:** `Project_Status.md` §1 còn ghi "mọi session Claude Opus 5.5" (sửa ở kết phiên).

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 16:24 11/11/2026, kết phiên chiều 11/11)

**Phiên chiều 11/11 đã kết** (mở 13:39, chỉ A mở). Quyền phiên **hết hạn** ⇒ A mới hỏi lại User một câu. **Dự án chưa xong** — Phase 9 tiếp tục.
Khối kết phiên sáng 11/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-11_sang.md`; 10/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-11.md`.

**Hệ thống:** không đổi so với 10/11 (`main` chỉ thêm tài liệu: `f892528`, `02405c9` + commit kết phiên). **Qdrant tắt** (dữ liệu `qdrant_storage/` còn) ⇒ việc cần chatbot: `docker compose up -d qdrant` trước.
**Tiền 11/11:** 0 USD API (agent con chỉ đọc = quota Claude). Phase 9 ≈ 3,88 / 4,2.

### Xong 11/11 — bộ bài học cho User
- **`bai_hoc/` 22 bài (0–21)** + `README.md`. Chiều 11/11 thêm: 17 giao diện + tốc độ · 18 đóng gói Docker · 19 bảng tổng 34 lần so sánh · 20 làm đồ án thế nào (dòng thời gian, nhiều agent, rào bằng máy, tiền ≈ 4,7 USD từ 24/10) · 21 dữ liệu người dùng + bảo mật; bổ sung bài 0 (tên đề tài, người dùng), 12 (vì sao chọn tính năng + đã cân mà không làm). Sửa 5 câu sai ở bài đã commit (4, 11, 14 ×2, 20) + 1 câu chưa rõ (8).
- **Luật User chốt chiều 11/11** (`WORKFLOW.md` §6, memory `user-reading-style`): bài học chứa **mọi việc đã làm xong** (xây, triển khai, so sánh, tối ưu, đóng gói, cách làm); **phần chưa xong / đang dở không đưa vào**, xong mới viết bổ sung; độ dài như bộ 0–19 (User: "ổn"). **W65 (đang thử):** bài mới / sửa nhiều ⇒ agent con kiểm độc lập với nguồn trước commit.
- Bản ghi số liệu + biên bản kiểm (private): `data/hoc_cung_user_2026-11-10/` (`fact_*.md`, `review_*.md`, `do_phu_bai_hoc.md`); cách đọc của User: `data/hoc_cung_user_2026-11-10/ghi_chu_cach_doc_cua_user.md`.

### Làm tiếp (theo thứ tự)
1. **Hỏi User quyền phiên** (một câu).
2. **Góp ý bài học:** User đọc dần ⇒ sửa ngay; câu sai ⇒ sửa + ghi ở Nguồn + báo User. **Việc nào vào hệ thống mà xong** (kể cả thử rồi bỏ) ⇒ viết vào bài bị chạm / bảng tổng bài 19 **cùng đợt**, qua W65.
3. **Phase 9 tiếp:** B7 lượt đo cuối (nháp `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md`; quỹ thiếu ≈ 0,03 — hỏi User lúc chạy) · bản đồ (chờ phiếu toạ độ) · giọng nói (chờ 40 câu, nhánh `p10-giong-noi`) · deploy AWS (Q-DP dưới). Đợt 2 cổng: lượt đếm rẻ trước (W61).
4. **Ứng viên từ bài 16 "chỗ còn yếu"** (đề xuất, chưa duyệt; mỗi cái cần lượt đếm rẻ trước): thử lại model xếp lại ở 10 đoạn; kiểm số tiền / giờ trong câu trả lời kho phải có trong đoạn được trích; thu câu người dùng thật khi deploy.
5. **User khi rảnh (không chặn):** đọc `bai_hoc/` · bảng điểm v7 `data/phase_9/lich_trinh/diem_cho_user_v7.md` · phiếu toạ độ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` · thu 40 câu giọng nói `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
6. **Giới hạn biết** (như 10/11): biểu mẫu "dày lịch" gần như không tác dụng; người lớn tuổi / trẻ em không có buổi tối; câu lịch bị rút khi thiếu `[n]` (1 / 9); log truy cập uvicorn: probe 11/11 cho thấy bị tắt (xác nhận khi chạy server thật). **Lệch còn mở (sửa khi chạm):** chú thích `settings.yaml` cạnh `ngay_lich: true` và `anh.bat: true` còn ghi "TẮT tới khi đạt"; `07_BAO_CAO…` checklist còn dòng "câu lịch thuần ⇒ ngoài phạm vi"; vài số dòng `file:dòng` cũ trong 05 / 06 / 07 / 10; `bao_cao_he_thong/01_LUONG…` bảng dữ liệu thiếu nút "Báo thông tin chưa đúng" và ý "câu không về Huế cũng gửi đoạn kho tới OpenAI"; docstring `backend/api/gioi_han.py` + checklist dưới ghi "IP Caddy" trong khi Dockerfile dùng `'*'` (lý do B / C đã chấp nhận).

**Vòng tự soi chiều 11/11:** chỉ A ⇒ tự soi một mình: không test / đo nào chạy (1 probe 0 USD); 7 agent con chỉ đọc (3 fact sheet, rà độ phủ, 2 review, 2 fact sheet) — review bắt thật 6 sai + 15 hiểu nhầm ⇒ đáng; W65 thay một luật thừa (số luật không tăng). Sổ vòng 26 (S121–S123).

### Nhánh
`main`. Đang mở cũ: `p9-sua-lich` (hoãn), `p10-giong-noi` (E), `p9-b5c` + `p9-toc-do-6` (hồ sơ). Worktree `/tmp`: không. Ảnh docker cục bộ: `hue-rag-app:dep10b` (đạt), `dep10`, `nhap2` (cũ, xoá được), `nhap` (có file private — User `! docker image rm hue-rag-app:nhap`).

### Mã hay gặp
G = cổng 2 nhóm (đóng); T1 ngày + âm lịch (bật, bản nhanh 10/11); T2 / T3 / T4 đóng hồ sơ 09/11; S1–S6 / S2b = sàn §12.3; B0–B7 = bậc Phase 9; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`.

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

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

(1) Quyền phiên. (2) Góp ý `bai_hoc/` (khi User đã đọc). (Q-DP, **khi tới deploy AWS** — không hỏi sớm): tra web trên bản công khai · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền (HUE_SITE phải là tên miền https, không thì cookie Secure làm mất nhớ hội thoại) · log truy cập uvicorn ghi IP ⇒ `--no-access-log`? (**15:04 11/11/2026 A probe 0 USD:** `setup_logging()` trong lifespan tắt logger `uvicorn.access` — `disable_existing_loggers` mặc định — ⇒ nhiều khả năng không in IP; xác nhận bằng một lần chạy server thật trước khi bỏ câu này) · xoá ảnh docker cũ — report `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md` §3. (B7) quỹ thiếu ≈ 0,03 USD. **Vòng cải tiến cũ còn chờ** (gom một lần, không hỏi lẻ): W60 / W58 / W57 / W4 + W39 + vòng 24 (sổ). **Mới (15:18 11/11/2026, review agent con bắt):** tên công ty nơi anh thực tập còn trong 11 file tracked đã public từ 23–24/10 (`WORKFLOW.md` §6 dòng "Học từ…", 2 file `report_agent/2026-10-24_to_chuc_bao_cao/*` có tên công ty trong tên file, `report_agent/README.md`, 2 spec, 4 file `reports/`, 1 nhật ký) — sửa tiến (đổi chữ / dời file sang `data/`) hay để nguyên? lịch sử git vẫn giữ. **Không gấp:** xoá collection thử `hue_anh_siglip2`; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; ảnh `hue-rag-app:nhap` có file private (User `! docker image rm hue-rag-app:nhap`); báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo; nhãn cũ câu "hôm nay âm lịch" trong bộ 30/10 (`data/ngay_hien_tai_2026-10-30/questions.jsonl`) còn ghi từ chối.

## Câu hỏi A còn nợ (không cần User)

- **09/11:** T1 đã bật (xong lượt xác nhận + lượt sau G); giới hạn T1: "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên 12/11 (mở 18:40 12/11/2026):** A `hue-rag-7d` · B `hue-rag-1b` · C `hue-rag-e1` · E `hue-rag-33` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên chiều 11/11 (mở 13:39 11/11/2026):** A `hue-rag-2f` — chỉ A (B / C / E không mở; 8 terminal khác là dự án khác). Qdrant tắt. Việc: bàn `bai_hoc/` với User.

**Phiên 11/11 (mở 08:18 11/11/2026):** A `hue-rag-96` — chỉ A (B / C / E không mở). Qdrant tắt lúc mở.

**Phiên 10/11 (mở 19:02 10/11/2026):** A `hue-rag-55` · B `hue-rag-05` · C `hue-rag-4f` · E `hue-rag-e4` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên 12/11 (User chọn "như 10/11", A ghi nhận 18:45 12/11/2026):** A tự điều phối, giao ngay việc có sẵn trong handoff, A tự commit / push, B / C / E push nhánh riêng, trần Phase 9 4,2 (≈ 3,88 đã dùng), việc cần User duyệt thì gác. Hết hạn cuối phiên.
  **Thêm (19:01 12/11/2026) User đi nghỉ, trở lại ~20:30:** "cứ tiếp tục làm việc; vẫn duyệt chi phí API; **không hỏi khi User vắng**; làm tiếp không cần hỏi" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User"; tiền ghi thật từ log, vượt trần 4,3 chỉ khi cần cho việc đã giao và báo lại.
- **Quyền phiên chiều 11/11 HẾT HẠN (16:24 11/11/2026, kết phiên).**
- **Phiên chiều 11/11 (User chọn "như sáng 11/11", A ghi nhận 13:41 11/11/2026):** A sửa `bai_hoc/` theo góp ý, tự commit / push; trần Phase 9 4,2; việc cần User duyệt thì gác. Hết hạn cuối phiên.
- **Quyền phiên 11/11 (sáng) HẾT HẠN (10:43 11/11/2026, kết phiên).**
- **Phiên 11/11 (User chọn "như 10/11", A ghi nhận 08:20 11/11/2026):** như 10/11 dưới đây (A tự điều phối, tự commit / push, B / C / E push nhánh riêng, trần Phase 9 4,2, việc cần User duyệt thì gác, không hỏi khi User vắng). Hết hạn cuối phiên.
- **Phiên 10/11 (User chọn "như 09/11 + trần 4,2", A ghi nhận 19:05 10/11/2026):** như 09/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác; tiền API thoải mái nhưng ưu tiên tốc độ, không test vô nghĩa). **Trần Phase 9 nâng 4,0 ⇒ 4,2 USD** (cho 2 việc tốc độ, quỹ B7 0,35 giữ riêng). Hết hạn cuối phiên.
  **Thêm (19:12 10/11/2026) User:** "hạn chế test các phần không cần thiết, không over-engineer, muốn đẩy nhanh quá trình; chi phí API vẫn duyệt; các session cùng trao đổi, thảo luận để đề xuất, chốt phương án" ⇒ A mở vòng tự soi 1 ngay (plan B / E là kết quả đầu); tiền không còn là lý do giữ bộ đo — thời gian là thước.
  **Thêm (19:15 10/11/2026) User đi nghỉ:** "tiếp tục điều phối, phát triển, triển khai, ghi báo cáo đầy đủ; câu cần User chốt thì gác lại, triển khai phần khác; **không đưa câu hỏi lúc User vắng** (treo việc)" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User".
- **Phiên 09/11 (User chọn "như 08/11", A ghi nhận 20:13 09/11/2026):** A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác. Trần Phase 9 nâng 4,0. Hết hạn cuối phiên.
  **Thêm (20:21 09/11/2026) User:** "thoải mái tiền API cho triển khai, phát triển nhưng phải đảm bảo tốc độ; không làm những thứ vô nghĩa hay test những thứ mất thời gian; 4 bạn trao đổi, thảo luận cùng nhau để đưa ra phương pháp, hướng xử lý phù hợp" ⇒ ưu tiên tốc độ làm; cắt test / đo không phục vụ sàn chất lượng; B / C / E bàn thẳng với nhau, A chốt khi lệch phạm vi.
- Spec Phase 9 file hiện tại sha `01b7476a3eb1` ≠ bản duyệt `5557f0fd7650` do commit `442f758` (bỏ mốc ngày theo User 08/11; sàn + tiền không đổi) ⇒ sửa chữ, không cần duyệt lại (A ghi 20:13 09/11/2026).
- **Quyền phiên 08/11 HẾT HẠN (12:50 08/11/2026, kết phiên).** (User 11:06: ~13:00 dừng; User 12:50 08/11/2026: để nhiệm vụ / câu hỏi cho phiên sau.)
- **Phiên 08/11 (User chọn "như 07/11", A ghi nhận 09:22 08/11/2026):** như 07/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, khoá Serper cho tra cứu, việc cần User duyệt thì gác). Hết hạn cuối phiên. Giao lúc mở: B ảnh cổng (`p11-anh-cong`), C review ảnh, E rà "Câu hỏi A còn nợ" (chỉ đọc).
- **Phiên 07/11 (User chọn "như 06/11", A ghi nhận 11:55 07/11/2026):** A tự điều phối — giao ngay việc có sẵn trong handoff, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5. Hết hạn cuối phiên.
  **Thêm (12:30 07/11/2026, User đi nghỉ):** "tiếp tục nghiên cứu, triển khai, phát triển, đánh giá, viết báo cáo đầy đủ; việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; làm việc khác; tự do nghiên cứu, gọi Codex tra cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau". Trần tiền như trên (≤ 1 USD / phiên). **(12:31 07/11/2026) User: "trần tiền tôi vẫn duyệt nếu quá 1$, có thể thoải mái thực nghiệm"** ⇒ vượt 1 USD / phiên được; A vẫn ghi tiền thật từ log mỗi việc + báo tổng ở nhật ký.
- Phiên tối 06/11 — hết hạn 22:41 06/11/2026. Tiền phiên ≈ 0,027 USD.
- **Tiền Phase 9: trần 4,0 USD** (User nâng, A ghi nhận 20:15 09/11/2026; dự phóng việc chờ ≈ 0,55: G 0,12 · T1 0,04 · T3 0,05–0,1 · T2 0,21 · T4 0,12; quỹ B7 0,35 giữ riêng). Trước: 3,5 (User nâng 10:38 08/11/2026; trước 2,5) (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
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
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
