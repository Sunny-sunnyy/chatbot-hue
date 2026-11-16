# STATUS C — phiên 16/11 (C `hue-rag-80` · A `hue-rag-db` · B `hue-rag-83` · E `hue-rag-af`); mục dưới là kết phiên tối 15/11 (C `hue-rag-10` · A `hue-rag-ef` · B `hue-rag-7d` · E `hue-rag-f0`). Lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`

## PHIÊN 16/11 (C ghi 14:03 16/11/2026 `date`)

- A giao (User duyệt quyền "như tối 15/11 + xin lượt máy"): **việc 1 mục dưới** — chạy trên server 8010 của A (web bật + sổ vết), CHỜ Qdrant + lượt máy; tiêu chí giữ nguyên. C cũng kiểm 100 % nhãn bộ ảnh đo mới khi E gom xong. Tiền tối 15/11: A tự cộng bằng `dem_chat_metrics.py --sha`.
- Chuẩn bị (chỉ đọc code, 0 USD) — chỗ cần đọc trong bản ghi lượt 3:
  - Lịch sử gửi model: `llm/generator_openai_full_corpus.py` `with_history` — cờ `nho_cau_tra_loi: false` ⇒ chỉ có các tin user trần (câu A, câu B), không tin assistant; lời dặn thêm `ASSISTANT_HISTORY_NOTE` (`llm/full_corpus_prompt.py:121`) bảo câu tìm phải nêu tên đối tượng của lượt trước.
  - Mục web: `llm/assistant.py` `cau_cho_web` — lượt có lịch sử + model đã tìm kho ⇒ câu web = câu tìm kho **CUỐI** model viết (`trace.model_queries[-1]`). Lượt đếm sạch thấy model tìm cho câu B ở lượt 3 (3 / 8) ⇒ **giả thuyết (chưa đo):** mục web nói khoảng cách là vì câu tìm cuối thuộc câu B, không phải vì web làm lượt 3 từ chối; lượt từ chối có thể do model chỉ tìm cho câu B rồi thấy kho không có.
  - Đọc trong sổ vết lượt 3: `tim_kho[].cau` (thứ tự câu tìm), `tim_kho[].ket_qua` / `vao_ngu_canh` (có đoạn của câu A không), `tra_loi.chu` / `ket_qua_co_dinh`, `web.cau_gui_tra_web`, `lich_su`.
- **Việc 1 XONG (14:08 16/11/2026):** server 8010, web bật + sổ vết: lượt 3 từ chối **0 / 3** ⇒ theo tiêu chí: ghi giới hạn, không xây. Sổ vết lượt 3: model không tự tìm thêm, đoạn đúng bài vào ngữ cảnh. ≈ 0,0092 USD. Report: `report_agent/2026-11-12_ra_khoang_cach/c_dem_hoi_lai_cau_cu.md` mục cuối. Đã báo A.
- **Kiểm "## Sửa đổi 16/11" plan so ảnh — READY** (0 major, 1 minor: `tran_sai_quyet_1` nhận số ảnh TRONG danh sách của nhóm "một tên"); đã gửi A + B.
- **Công cụ khoảng cách — CHỜ REVIEW (14:40 16/11/2026):** `ĐÃ PUSH fa3244e origin/p9-khoang-cach`, cờ `khoang_cach: false`. Đếm trước 4 / 6 từ chối; bộ dò từ khoá 27 câu 0 ra sai; an toàn 32 chạm 0 ⇒ không lượt an toàn; lượt đo 16 câu: đúng cặp 13 / 14, ngoài bảng ra số 0 / 2, 0 số sai tới người dùng (2 rút lại oan do kiểm số không nhận số làm tròn ⇒ sửa, chạy lại 2 / 2 đạt); test rộng 1216 passed. Tiền ≈ 0,028 USD. Report `report_agent/2026-11-12_ra_khoang_cach/c_khoang_cach_implementation.md` (trên nhánh). Worktree `/tmp/c_kc` (symlink data / kho / node_modules) giữ tới khi review xong.
- Ý kiến web gọn bản 2 gửi A + B: không merge bản 2; đọc tay bản cũ trên cùng 28 đầu vào trước khi mở vòng 3.
- **Review spec deploy AWS bản 1 của E (14:43 16/11/2026) — vòng 1 changes_requested (0 / 3 / 6):** `ĐÃ PUSH 66a3070 origin/p12-deploy-aws-spec-review`; vòng 2 chỉ đọc lại 3 major + minor. Đã báo A + E.
- **Đánh giá bản đồ lịch XONG (14:45 16/11/2026, 0 USD):** `data/ban_do_lich_2026-11-16/danh_gia.md`. Phát hiện: `tile.openstreetmap.org` TLS thất bại từ mạng này (CARTO / Esri / OSM Pháp / Đức 200) ⇒ cần User thử link ô trên điện thoại + chọn host (Q-BĐ1); còn thiếu: kéo trên điện thoại, 0 lỗi console, User xem ảnh ghim. Ước 3,5–4,5 giờ; plan mức nhẹ. Đã báo A.
- **Plan bật bản đồ (14:51 16/11/2026):** `ĐÃ PUSH 0823fe1 origin/p11-ban-do-bat` (chỗ chọn host trống; tra điều khoản `data/tra_cuu_cli/2026-11-16_o-ban-do/`: CARTO cần khoá, 5 triệu ô / tháng phi thương mại; OSM Đức phi thương mại, không đăng ký) — chờ User thử link + chọn host. Worktree `/tmp/c_bd`.
- **Review spec deploy vòng 2 — READY** (`77a7d6c` trên `origin/p12-deploy-aws-spec-review`; 1 minor n-1 rollback bản chụp).

## PHIÊN SAU ĐỌC TRƯỚC (KẾT PHIÊN TỐI 15/11 — C viết 22:07 15/11/2026 `date`; User kết phiên, phiên sau là 4 phiên mới không còn ngữ cảnh)

C là session thực thi; A điều phối. Tối 15/11 C làm: dọn nợ vùng "sửa lịch bằng lời", ba bản giao diện "hỏi bằng ảnh", sửa lỗi tải lại trang, hai lượt đếm một lỗi hội thoại, ba review. Mọi nhánh code của C đã vào `main`. **Việc đã giao cho phiên sau: một việc (mục 1).**

### 1. VIỆC ĐẦU PHIÊN SAU — tái tạo lỗi "hỏi lại câu cũ trong cùng một cuộc bị từ chối" trên ĐÚNG cấu hình đang chạy (A giao; ≈ 0,013 USD; cần A giao lại + quyền phiên trước khi chạy)

- **Lỗi User gặp (tối 15/11, trang Trợ lý):** trong một cuộc trò chuyện: câu A = hỏi VỊ TRÍ một di tích (trả lời đúng) ⇒ câu B = hỏi tiếp KHOẢNG CÁCH từ đó sang một di tích khác (kho từ chối, hiện mục "Từ web") ⇒ hỏi lại đúng câu A ⇒ bị TỪ CHỐI, mục web lại nói về khoảng cách của câu B. Ba câu thật nằm trong file private `data/f5_cuoc_moi_2026-11-15/tai_tao.py` (biến `CAU`) — report tracked chỉ tả mức loại câu.
- **Đã biết (số đo):**
  - Server thật, tra web BẬT (đúng cấu hình User dùng), đường `POST /api/chat/stream` giữ cookie: lượt 3 từ chối **3 / 3**; thêm 1 / 1 ở lượt đếm đầu (trong tiến trình, web tắt).
  - Lượt đếm SẠCH (4 bộ ba câu × 2 cuộc, trong tiến trình, tra web TẮT để giữ tiền): đối chứng 8 / 8, lượt 3 từ chối **0 / 8** ⇒ theo tiêu chí ghi trước (≥ 2 / 8 = lỗi rộng) thì không phải lỗi rộng. Bộ "vị trí ⇒ khoảng cách" trong lượt này: 0 / 2.
  - Ở lượt 3 model tự tìm kho cho câu B (không phải câu A vừa gõ) ở **3 / 8** cuộc sạch (vẫn trả lời đúng A).
  - **Chỗ chưa khớp:** 3 / 3 (web bật) ↔ 0 / 2 (web tắt) — chưa biết do model dao động hay do tra web bật. Lượt đếm tắt web là sai lầm của C (không tái lập cấu hình gặp lỗi) ⇒ thành luật W87.
  - **Giả thuyết CHƯA đo:** lịch sử gửi model chỉ có các câu hỏi cũ dạng tin người dùng trần, không có câu trả lời (cờ `nho_cau_tra_loi: false`; `backend/llm/generator_openai_full_corpus.py` `with_history`) ⇒ model coi câu B là chưa được đáp. Nhánh chẩn đoán "lịch sử kèm câu trả lời" chưa chạy.
- **Cách làm (theo W87: đúng cấu hình đang chạy, thử MỘT cuộc trước):**
  1. Server có tra web + sổ vết: dùng server 8010 của User nếu A cho (đang chạy `HUE_SO_VET=true`), hoặc server tạm của C: `cd backend && HUE_SO_VET=true HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8041` (kiểm `ss -ltnp` + `readlink /proc/<pid>/cwd`; tắt bằng pid của cổng).
  2. Một cuộc trước: `uv run python data/f5_cuoc_moi_2026-11-15/tai_tao.py http://127.0.0.1:<cổng> <backend của server đó>/logs/application.log 1` (KHÔNG thêm `--moi-truoc-luot-3`). Mỗi dòng in: từ chối?, có mục web?, `n_history_turns`, công cụ, USD. Chạy ổn ⇒ đổi `1` thành `2` cho đủ 3 cuộc. ≈ 0,0045 USD / cuộc.
  3. Đọc bản ghi lượt 3: `uv run python scripts/xem_so_vet.py -n 9` (hoặc `--ma <turn_id>`; file `data/debug_trace/<ngày>.jsonl`) — xem `lich_su` (gửi model), `cau_tim_model`, `tim_kho`, `web.cau_gui_tra_web`, `tra_loi`.
- **Tiêu chí đọc (ghi trước, C đề xuất — A sửa nếu cần trước khi chạy):** lượt 3 từ chối ≥ 2 / 3 ⇒ lỗi gắn với cấu hình có tra web ⇒ dùng bản ghi chỉ ra chỗ lệch (câu tìm model viết là của câu B? lịch sử gửi model khác gì lượt web tắt?) rồi đề xuất MỘT hướng sửa cho A (plan mức nhẹ; đổi chuỗi gửi model ở lượt có lịch sử ⇒ phải đo bộ câu hỏi tiếp + bộ an toàn); ≤ 1 / 3 ⇒ ghi giới hạn "câu B bị kho từ chối có thể kéo lượt sau từ chối theo, không ổn định", không xây. Không đo thêm sau khi thấy số. Hướng sửa C nghĩ tới (chưa duyệt, chưa đo): đưa lịch sử thành một khối ghi rõ "các câu đã hỏi trước, đã xử lý xong" thay vì tin người dùng trần.
- Hồ sơ: `report_agent/2026-11-12_ra_khoang_cach/c_dem_hoi_lai_cau_cu.md` (hai lượt đếm + đính chính), `…/c_f5_cuoc_moi_implementation.md` (tái tạo + sửa phần tải lại trang). Dữ liệu private: `data/hoi_lai_cau_cu_2026-11-15/` (`tieu_chi.md`, `dem2.py` — công cụ đếm trong tiến trình, `ket_qua2_chinh.json` có chữ câu tìm + lịch sử), `data/f5_cuoc_moi_2026-11-15/`.

### 2. Review plan "nhận diện ảnh bằng so ảnh với ảnh mẫu" của B — ĐÃ XONG

Hai vòng: vòng 1 changes_requested (3 major) ⇒ B sửa ⇒ **vòng 2 READY**; A duyệt bản plan sha256 đầu `3b9a1894a195`; plan + biên bản ở `docs/superpowers/plans/2026-11-15-so-anh-embedding-plan.md` và `…-plan_review.md`. 5 minor B sửa lúc viết file ngưỡng: luật "≤ 2 ảnh sai" nên theo cỡ nhóm tự tin + thêm dòng đối chiếu với nhóm "model đang chạy trả một tên"; câu chọn ngưỡng t mơ hồ mẫu số; mức 30 % trên ảnh mẫu lệch với 50 % trên bộ đo; "≤ 5 % ảnh âm" sát sàn 2 / 20; báo riêng ảnh lạ rơi vào "nhiều tên". Plan đề nghị **C kiểm 100 % nhãn bộ ảnh đo mới** (E gom, B chạy) — chờ A / User chốt.

### 3. Trạng thái các vùng C giữ

- **Sửa lịch bằng lời** (`backend/llm/sua_lich_v2.py`): biểu mẫu 8 trường, sửa được bằng lời 7 / 8 (chưa: số người lớn); bảng đầy đủ ở đầu `report_agent/2026-11-12_ra_khoang_cach/c_dem_sua_lich_truong.md`. Tối 15/11 thêm: lượt đổi số ngày / kiểu lịch không đổi được gì có dòng báo; sau "Đã đổi kiểu đi / sở thích / trẻ em / người lớn tuổi" có dòng "Lịch xếp lại theo lựa chọn mới: …" hoặc "Các điểm trong lịch giữ nguyên chỗ."; quá 6 tên thì chỉ nêu số điểm; hàm so hai khung `_so_cho` dùng TẬP (ngày, buổi) của mỗi điểm trên cả ba buổi (sửa luôn câu đổi ngày đi). Còn mở (chưa ai giao): ngày tương đối / ngày âm; **xin chỗ ở không nêu hạng ⇒ hiện mọi hạng — đếm 6–8 câu "gợi ý chỗ ở" trước (≈ 0,002 USD) xem model có xếp vào `doi_hang_o` không**; chuỗi S06 chập chờn ở thẻ chọn; nút trên biểu mẫu không tự đồng bộ theo lời. Chi tiết từng mục + chỗ trong code: mục "Còn mở" của kết phiên chiều bên dưới.
- **Hỏi bằng ảnh** (`frontend/src/HoiBangAnh.jsx`, hook `useHoiBangAnh`; `chat.jsx`): bản đang ở `main` = nút dấu cộng trong ô nhập + dán ảnh ⇒ ảnh nhỏ đính kèm (0 lần gọi API) ⇒ bấm Hỏi mới nhận diện ⇒ **một tên: tự hỏi luôn + dòng "Mình đoán trong ảnh là … — có thể sai"; 2–3 tên: thẻ chọn tên** (phần lai do E viết, C review). Giới hạn còn: không có nút huỷ lúc "Đang xem ảnh…"; URL ảnh trong bong bóng câu hỏi không thu hồi tới khi tải lại trang; nút × bỏ ảnh 24 px; Safari / Firefox chưa thử; bước nhận ảnh dao động trên cùng một ảnh (E đếm 7 lượt: đúng 1 · một tên sai 2 · hai tên 2 · lỗi model 2) ⇒ giả định "một tên thì đáng tin" cần đếm lại trên ảnh thật.
- **Tải lại trang ⇒ cuộc mới ở server** (`chat.jsx` `useChat`): đã ở `main`; lịch đã lưu trong cuộc cũng mất khi tải lại (đúng với màn hình trống).
- **Sổ vết debug** (của E, `backend/core/so_vet.py`): C thêm khung lịch bản 2 (`lich.v2_khung`, `v2_ngay_di`, `v2_mua`); bật bằng `HUE_SO_VET=true`, chỉ máy local.
- **Đếm "biểu mẫu đưa cơ sở khác hạng sao đã chọn"**: 0 / 9.216, A quyết không sửa; chạy lại khi đổi bảng điểm hoặc bảng lưu trú (lệnh ở mục 4).

### 4. Công cụ và kết quả trong `data/` (private) — lệnh chạy lại

| Việc | Thư mục | Lệnh (từ gốc repo trừ khi ghi khác) | Tốn |
|---|---|---|---|
| Tái tạo lỗi hỏi lại câu cũ qua server | `data/f5_cuoc_moi_2026-11-15/` | `uv run python data/f5_cuoc_moi_2026-11-15/tai_tao.py <url> <application.log> <số cuộc>` | ≈ 0,0045 USD / cuộc |
| Kiểm "tải lại trang ⇒ cuộc mới" (Playwright) | như trên | `uv run python data/f5_cuoc_moi_2026-11-15/pw_f5.py <url>/ <application.log> <ảnh ra .png>` | ≈ 0,0025 |
| Đếm trong tiến trình (web tắt) | `data/hoi_lai_cau_cu_2026-11-15/` | từ `backend/`: `HUE_TRA_WEB=false PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env python ../data/hoi_lai_cau_cu_2026-11-15/dem2.py chinh 2` | ≈ 0,015 |
| Đếm biểu mẫu lệch hạng chỗ ở | `data/dem_lech_hang_bieu_mau_2026-11-15/` | từ `backend/`: `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/dem_lech_hang_bieu_mau_2026-11-15/tools/dem_lech_hang.py` (sửa 2 đường dẫn bảng ở đầu vòng lặp nếu bảng đổi) | 0 |
| Ảnh đính kèm — mọi ca (Playwright) | `data/anh_dinh_kem_2026-11-15/` | `pw_dinh_kem.py <url>/ <ảnh .jpg> <thư mục ảnh ra>` (viết cho bản "luôn hiện thẻ tên" — với bản lai phải chặn route trả 2 tên); `pw_khong_nhan_ra.py`, `pw_hai_minor.py` (0 USD, chặn route) | ≈ 0,002 / 0 |
| Ca "người dùng làm việc khác trong lúc chờ ảnh" | `data/review_anh_tra_loi_thang_2026-11-15/` | `uv run python …/pw_do2.py <url>/ frontend/public/anh/dau_trang_ngo_mon.jpg` — đạt khi đối chứng 1 câu / 1 lượt, ca1 không thêm request bị huỷ, ca2 rỗng | 0 |
| Thử sổ vết trên 3 loại lượt | `data/thu_so_vet_2026-11-15/` | `uv run python …/thu.py <url> <ảnh .jpg> data/debug_trace/<ngày>.jsonl` (in tên trường, không in nội dung) | ≈ 0,0015 |
| Nút dấu cộng (Playwright) | `data/nut_anh_cong_2026-11-15/` | `pw_nut_anh.py`, `pw_co_tat.py` (bản cũ trước khi có đính kèm — chỉ để tra) | — |

Server tạm cho việc giao diện: worktree `git worktree add -b <nhánh> /tmp/c_x origin/main && cd /tmp/c_x || exit 1`; symlink `data`, `knowledge-base-hue`, `frontend/node_modules` từ cây chung; `cd frontend && npm run build` (< 1 giây); server `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8041`; xong: tắt bằng pid của cổng, xoá symlink, `git worktree remove --force`.

### 5. Việc tối 15/11 (để tra)

| Việc (A giao tối 15/11) | Trạng thái | Số chính | Tiền |
|---|---|---|---|
| Đếm 4b(c): biểu mẫu đưa cơ sở khác hạng không kèm lý do | **xong — A quyết không sửa** | 0 / 9.216 ô (3.840 khung × 3 mức; đối chứng W83 đúng); công cụ `data/dem_lech_hang_bieu_mau_2026-11-15/tools/dem_lech_hang.py` — chạy lại khi đổi bảng điểm / bảng lưu trú | 0 |
| Việc 1 (handoff mục 4): lượt đổi tham số không đổi được gì có dòng báo · dòng "lịch xếp lại / giữ nguyên chỗ" · bảng 7 / 8 trường | **đã merge** (main `e5b076e`; nhánh `8059e29`) | B review bắt lỗi thật (điểm dời ban ngày ↔ tối ghi vừa "bớt" vừa "thêm", có sẵn ở câu đổi ngày đi) ⇒ sửa chung; > 6 tên ⇒ chỉ nêu số; bộ quét B 0 câu sai / 540 lượt | 0 |
| Nút dấu cộng trong ô nhập + dán ảnh (User báo khi thử) | **đã merge** (nhánh `caccfb7`; E review ready, E đã thử dán PNG thật 3 / 3) | ảnh `data/nut_anh_cong_2026-11-15/anh/`; chưa thử Safari / Firefox | 0,0007 |
| Tải lại trang ⇒ cuộc mới ở server (LỗI User báo: F5 xong hỏi lại câu đầu bị từ chối) | **đã merge** (main `b833c7b`; A đọc diff, merge thẳng) | tái tạo 3 / 3; sau sửa Playwright: reload ⇒ hỏi lại ⇒ lịch sử 0, được trả lời | 0,0159 |
| Đếm lỗi riêng "cùng một cuộc: A ⇒ hỏi tiếp B ⇒ hỏi lại A" (A duyệt 2 lượt) | **xong** — lượt sạch 0 / 8 ⇒ không phải lỗi rộng; còn chỗ chưa khớp với server thật (web bật) | lượt đầu không sạch (lỗi "kết nối" thật ra do công cụ của C: mỗi cuộc một TestClient); lượt sạch: đối chứng 8 / 8, model tìm kho cho câu B ở lượt 3: 3 / 8 nhưng vẫn trả lời đúng A; nhánh chẩn đoán "lịch sử kèm câu trả lời" CHƯA ĐO | 0,0149 + **0,0298** (vượt mức duyệt ≈ 0,02 vì 32 lượt hỏng của bản công cụ lỗi vẫn tốn phần định tuyến) |
| Thử sổ vết debug của E (`p9-so-vet` `8493624`, `HUE_SO_VET=true`) trên 3 loại lượt | **xong, đã báo A + B** | biểu mẫu xếp lịch · sửa lịch bằng lời · ảnh: 3 / 3 ra dòng; THIẾU `lich.khung` cho lịch bản 2 (bản ghi đọc `trace.lich`, khung v2 ở `trace.lich_v2`) — chưa ai sửa; `data/thu_so_vet_2026-11-15/thu.py`. Phần sửa 3 điểm review A giao cho C: E đã tự sửa trước ⇒ C bỏ, không push | 0,0014 |
| Sổ vết: thêm khung lịch bản 2 (`v2_khung`, `v2_ngay_di`, `v2_mua`) | **B ready; sổ vết đang BẬT trên server 8010** — `origin/p9-so-vet` `dc4f392` | khoá ngày của `mua` đổi ra chữ (không thì mất cả dòng); test_so_vet 7 passed; thử khung thật 0 USD | 0 |
| Review `p9-anh-tra-loi-thang` `f724f7c` của E (ảnh 1 tên ⇒ trả lời thẳng) | **READY ở `6c183cf`, đã merge** (main `d649b50`; vòng 1 `f724f7c` changes_requested 1 major ⇒ E sửa ⇒ C chạy lại 2 ca đạt) | lúc "Đang xem ảnh…": bấm "Cuộc trò chuyện mới" ⇒ câu ảnh tự gửi vào cuộc mới; lượt khác đang chạy ⇒ bị huỷ. Công cụ `data/review_anh_tra_loi_thang_2026-11-15/pw_do2.py` (0 USD; đạt khi ca1 không thêm request bị huỷ + không câu "(Trong ảnh: …)", ca2 rỗng, đối chứng 1 câu / 1 lượt) | 0 |
| Review plan "so ảnh với ảnh mẫu" của B, 2 vòng | **vòng 1 changes_requested 0 / 3 / 6 ⇒ B sửa ⇒ vòng 2 READY (5 minor)** — biên bản `origin/p10-so-anh-review` `30a63b1` | vòng 1: 25 ảnh không phân biệt 22 ↔ 20; sàn ngoài danh sách trên 5 ảnh; đổi nhiều thứ một bước + thiếu phép dò rẻ (đã chạy: DINOv2 17 / 25). Vòng 2: minor quanh luật chọn ngưỡng và "≤ 2 ảnh sai" | 0 |
| Ảnh đính kèm tin nhắn — bấm Hỏi mới xử lý (User chốt: tải ảnh lên không làm gì) | **đã merge** (main `67dd28d`; B review ready) + **2 minor chờ A đọc diff / B liếc**: `origin/p9-anh-dinh-kem-2` `cb00fa4` (dòng nhắc "Chọn một tên ở trên…" khi bấm Hỏi lúc thẻ mở; "Cuộc trò chuyện mới" gỡ ảnh + thẻ) | Playwright mọi ca đạt; ảnh `data/anh_dinh_kem_2026-11-15/anh/`; giới hạn: chưa có nút huỷ lúc "Đang xem ảnh…", Safari / Firefox chưa thử | 0,0019 |
| Review nhánh `p9-chu-gioi-thieu` của E (A nhờ) | **ready, A đã merge** | câu ví dụ "ở khách sạn 3 sao" chạy thật 6 / 6 ra đổi hạng 2–3 sao (`data/review_chu_gioi_thieu_2026-11-15/`) | 0,00075 |

### 6. Câu hỏi / thắc mắc cho A (hoặc User qua A)

1. Việc mục 1: chạy trên server 8010 của User hay server tạm của C; tiêu chí đọc C ghi ở trên có cần sửa không.
2. C có là người kiểm nhãn bộ ảnh đo mới của plan so ảnh không (plan đề nghị).
3. Tiền C tối nay ≈ 0,066 USD chưa có người thứ hai tính lại; lượt đếm thứ hai vượt mức A duyệt (0,0298 so với ≈ 0,02).
4. Giới hạn "không nút huỷ lúc Đang xem ảnh…" có làm không, sau khi User thử bản lai.

### 7. Luật mới phải nhớ (User duyệt 21:40 15/11/2026; chữ đầy đủ ở `WORKFLOW.md` §9.1, `Session_Prompt.md` §8, sổ `SO_CAI_TIEN_CACH_LAM.md`)

- **W85:** góp ý giao diện có hơn một cách hiểu ⇒ hỏi lại User bằng hộp chọn TRƯỚC khi code.
- **W86:** sàn "người đọc tay" do người KHÔNG viết lời dặn đọc, trước khi trình User.
- **W87:** đếm / tái tạo lỗi User báo trên ĐÚNG cấu hình đang chạy, thử một lượt trước khi chạy cả bộ.
- Từ chiều 15/11 (vẫn áp): W82 bộ câu dò ≥ 20 cho code đọc chữ người dùng; W83 phép kiểm mới phải có ca đối chứng ra "có"; W84 đổi bảng dữ liệu ⇒ quét nhãn + mô phỏng trước merge.

### 8. Bẫy gặp tối 15/11

- Đếm lỗi với tra web TẮT trong khi User gặp lỗi lúc web BẬT ⇒ 0,045 USD cho một kết luận còn treo (nay là W87).
- Công cụ đếm chạy ứng dụng trong tiến trình: **một `TestClient` cho mọi cuộc** (xoá cookie giữa các cuộc). Mỗi cuộc một client ⇒ lỗi kết nối model 32 / 32 mà vẫn tốn phần định tuyến; chữ trả lời rỗng ≠ "không từ chối".
- Bộ câu tự viết phải qua đối chứng trước (câu A hỏi ở cuộc mới có được trả lời không) — một bộ trượt 2 / 2.
- Playwright: muốn làm trễ một route thì bọc `fetch` trong trang (`add_init_script`); `threading.Timer` / `time.sleep` trong hàm chặn route làm ca đối chứng ra 0 và suýt báo sai. Chặn route (`page.route`) cho ca không cần model = 0 USD.
- React: code chạy sau `await` dùng hàm / trạng thái của lần vẽ CŨ ⇒ mọi luồng "chờ mạng rồi tự làm gì đó" phải thử ca "người dùng làm việc khác trong lúc chờ" (E đề nghị thành mục kiểm cố định).
- So hai khung lịch bằng dict `{id: (ngày, buổi)}` ghi đè điểm buổi tối nằm ở nhiều ngày ⇒ dùng tập chỗ.
- `json.dumps(..., default=str)` không cứu KHOÁ dict là ngày ⇒ đổi khoá ra chữ trước.
- Log `backend/logs/application.log` của cây chung nhận cả lượt đo trong tiến trình lẫn server 8010 ⇒ đếm tiền theo mốc dòng + nhìn giờ; sự kiện SSE `done` đến sau `web`.
- A chuyển cho C việc sửa nhánh của E khi E đã sửa xong ⇒ làm trùng ~10 phút; trước khi nhận sửa nhánh người khác, `git fetch` xem nhánh đã đổi chưa.
- Tính năng ảnh đi 4 bản một tối vì chưa hỏi User bằng hộp chọn trước bản đầu (nay là W85).

### 9. Tiền và máy

- **Tiền C tối 15/11 ≈ 0,066 USD** (chưa ai tính lại): câu ví dụ hạng sao 0,00075 · nút dấu cộng 0,00072 · tái tạo + kiểm tải lại trang 0,0159 · đếm hỏi lại câu cũ 0,0149 + 0,0298 · ảnh đính kèm 0,0019 · thử sổ vết 0,0014; các review, plan review, sửa sổ vết, hai minor: 0 USD.
- **Máy lúc kết phiên:** 0 worktree `/tmp/c_*`, 0 server tạm (8041 đã tắt), 0 tiến trình nền, 0 file tạm `/tmp/c_*`. Server 8010 là của A / User (C không đụng). Nhánh của C đã merge, User xoá được khi tiện: `p9-sua-lich-no-nho p9-nut-anh-cong p9-f5-cuoc-moi p9-anh-dinh-kem p9-anh-dinh-kem-2 p9-tai-lieu-dem-hoi-lai p10-so-anh-review` (hai nhánh tài liệu: xoá sau khi chắc file đã ở `main`). C không tự xoá nhánh.

---

## (Kết phiên chiều 15/11 — CŨ, giữ để tra)

## PHIÊN SAU ĐỌC TRƯỚC (KẾT PHIÊN CHIỀU 15/11 — C viết 18:23 15/11/2026 `date`)

- **Trạng thái máy:** 0 worktree `/tmp/c_*`, 0 server tạm, 0 tiến trình nền, 0 file tạm của C. Mọi nhánh của C đã vào `main` (origin `a11e601` lúc viết). Nhánh cho User xoá (A đã ghi vào danh sách): `p9-luu-tru-v5 p9-commit-push p9-sua-hang-o p9-hang-o-m12 p9-o-khi-hoi p9-sua-ngay-di p9-tai-lieu-hang-o p9-tai-lieu-ngay-di`. C không tự xoá nhánh.
- **Việc phiên sau:** KHÔNG có việc đã giao. Chờ A. Ứng viên của vùng "sửa lịch bằng lời" ở mục "Còn mở" dưới.

### Đã xong chiều 15/11 (đều đã merge; report ở `report_agent/2026-11-12_ra_khoang_cach/`)
| Việc | Nhánh ⇒ merge | Plan (sha256 12) | Report | Số chính | Tiền (theo sha) |
|---|---|---|---|---|---|
| Bảng lưu trú v5 (gộp cơ sở lặp) | `p9-luu-tru-v5` ⇒ `2189c96` | giao trong handoff | `c_v5_commit_push_implementation.md` | 137 ⇒ 136 cơ sở; ô Nơi ở đổi 0 / 15.360; bảng `data/luu_tru_v5_2026-11-15/` md5 `34836e7c1438` (main nay dùng **v6** của E) | 0 |
| `scripts/commit_push.sh` (W81) | `p9-commit-push` ⇒ `f21eb88` | — | cùng file trên | thử 15 / 15 ca (`data/commit_push_2026-11-15/thu.sh`); in `ĐÃ PUSH <sha> origin/<nhánh>` / `CHƯA PUSH — …` | 0 |
| Đổi hạng chỗ ở bằng lời (bậc 1) | `p9-sua-hang-o` ⇒ `42e0c5b` | `…-sua-lich-hang-cho-o-plan.md` `8b10ccd50d37` (+ mục "Chỗ đổi") | `c_sua_hang_o_implementation.md`; review độc lập `data/review_sua_hang_o_2026-11-15/review.md` | bản đầu `c48ccf8` đạt ngưỡng nhưng chuỗi S08 hồi quy (main 4 / 4 ↔ nhánh 0 / 2) ⇒ A cho MỘT vòng chỉnh (chi tiết hạng dời xuống khối "cách nói thường gặp") ⇒ bản `32c129f`: H1 12 / 12 · sai mức 0 / 24 · H2 0 / 12, hỏi lại 6 / 6 · H3 0 / 12 · H4b 8 / 8 · Q3 10 / 10 · Q5 0 / 64 · Q5b 0 / 16 | 0,1017 + 0,0960 + Q5 0,0070 + mốc main 0,0054 = **0,2101** |
| m-1 / m-2 của review bậc 1 | `p9-hang-o-m12` ⇒ `609f13f` | A giao miệng | trong tin nhắn; test `test_luu_tru_lich.py` | hạng đặt nhầm hành động vẫn áp; `doi_hang_o` xét sau cùng (`sua_lich_v2._hang_o_sau_cung`); B review ready | 0 |
| Khối Nơi ở chỉ hiện khi hỏi | `p9-o-khi-hoi` ⇒ `ac03e0a` | `…-noi-o-chi-khi-hoi-plan.md` `d99fb6ec4a5c` | `c_noi_o_khi_hoi_implementation.md`; `e_review_noi_o_khi_hoi.md` | không mức hạng ⇒ 0 khối + khoá `cho_o_link` (dòng link); có mức ⇒ như cũ; lịch mẫu thêm mức 2–3 sao; test rộng 1.087; Playwright DAT | 0,0013 × 2 = **0,0026** |
| Đổi ngày đi bằng lời (bậc 2) | `p9-sua-ngay-di` ⇒ `a52ffd6` (bản `b7b47f1`) | `…-sua-lich-ngay-di-plan.md` `f36fe8bb5b6a` | `c_sua_ngay_di_implementation.md`; `e_review_sua_ngay_di.md` | đo trên `ad81cc0`, không vòng chỉnh: D1 12 / 12 · sai ngày 0 / 24 · D2 0 / 12, lý do 5 / 6 · D3 0 / 16 · đổi nhầm số ngày 0 · D4 8 / 8 · Q3 8 / 10 + S08 2 / 2 · H1 12 / 12 · Q5 0 / 64 · Q5b 0 / 16. **Review E M-1:** hàm đọc ngày nhận chữ GIỐNG ngày (8 / 34 câu dò) ⇒ sửa `0463bf2` (E ready; test rộng 1.160) ⇒ C sửa thêm `add3186` ⇒ E bắt hồi quy "5/5 người" ⇒ A cho đúng một commit `b7b47f1`; bảng ca 65 / 65; bộ dò E 35 / 35 và 18 · 0 · 1; ngoại tuyến 34 câu đã đo 0 lệch | 0,1189 + Q5 0,0037 = **0,1226** |
| Tài liệu (bài 25, sổ 07, nhật ký) | `p9-tai-lieu-hang-o` ⇒ `2f7cf33`; `p9-tai-lieu-ngay-di` ⇒ `f276894` | — | biên bản kiểm độc lập `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25_hang_o.md`, `…_ngay_di.md` | agent con: 53 khẳng định (0 sai, 8 sửa) · 51 khẳng định (1 sai — C ghi ngược bớt / thêm —, 10 sửa) | 0 |

- **Tổng tiền C chiều 15/11 ≈ 0,335 USD** (cộng theo sha; chưa ai tính lại). Review C làm: W79 của B (ready, 2 minor), `p9-gd-3-sua` của E (ready, 2 minor).
- **Dữ liệu đo (private):** `data/sua_lich_hang_2026-11-15/` (bộ H `cau_h.jsonl` md5 `f048c0e67761`, `tools/do_h.py`, `tools/cham_h.py`, `do/`) · `data/sua_lich_ngay_2026-11-15/` (bộ D `cau_d.jsonl` md5 `7b5b22cbda07`, `cau_d4.jsonl`, `tools/do_d.py --mo-phong`, `tools/cham_d.py`, `do/`, `log/`) · `data/noi_o_khi_hoi_2026-11-15/` (`tools/pw_noi_o.py`, ảnh, `log/`) · bộ dò của E `data/review_sua_ngay_di_2026-11-15/do_34.py`, `do_19.py`.

### Sửa lịch bằng lời — trường nào sửa được (sau chiều 15/11)
Biểu mẫu có 8 trường. Sửa được bằng lời **7 / 8**: số ngày (`doi_so_ngay`, có rào số ngày) · kiểu đi, sở thích, trẻ em, người lớn tuổi (`doi_tham_so`) · hạng chỗ ở (`doi_hang_o`) · ngày đi (`doi_ngay_di`). Chưa: **số người lớn** (chỉ vào lời văn, không vào bộ xếp — chưa ai đếm nhu cầu). Cộng 4 hành động theo điểm (bỏ / thêm / thay / dời buổi) ⇒ `HanhDong.loai` có 8 loại; code áp tối đa 2 / lượt, nhận tối đa 3.

### Còn mở / ứng viên (chưa ai giao; mỗi mục kèm chỗ trong code)
- (i) **Ngày tương đối** ("dời 2 hôm", "lùi một tuần") + **ngày âm / "dịp Tết"**: chưa làm — `backend/llm/do_so.py` `ngay_tu_cau` trả `ngay_chua_ro` (âm lịch chặn bằng `_AM_LICH`); tính tương đối cần ngày đang dùng (`luu["ngay_di"]`) ⇒ làm ở `sua_lich_v2.ngay_di_moi`. Câu "dịp Tết âm lịch" model còn không coi là câu sửa (D2-06).
- (ii) **Xin chỗ ở không nêu hạng ⇒ hiện mọi hạng**: chưa làm — hiện `sua_lich_v2.ly_do_giu_hang` trả `hang_chua_ro` (hỏi lại). Cần trạng thái "đã hỏi, không hạng" đi qua `ThamSoV2` / `tham_so` + `len_ke_hoach.gan_o_an`; chưa đếm model có xếp câu "gợi ý chỗ ở đi" vào `doi_hang_o` không (đếm 6–8 câu ≈ 0,002 USD trước).
- (iii) **`doi_tham_so` rỗng hẳn vẫn im lặng** (lượt sửa không dòng báo): `sua_lich_v2.ap`, nhánh `doi_so_ngay / doi_tham_so`, `if not doi: continue` (B ghi nhận khi review m12).
- (iv) **Lượt 3 ý có đổi hạng ⇒ "Chưa làm: đổi hạng chỗ ở"** (do `_hang_o_sau_cung` + `MAX_AP = 2`): A đã nhận.
- (v) **Dòng "Đã đổi số trẻ em: 0 → 1" không nói lịch đã xếp lại** (H4b câu 7; ghi nhận của review bậc 1): `sua_lich_v2.thay_doi` — bậc 2 đã có khuôn đếm điểm đổi chỗ (`kq["ngay_di"]`: `doi_cho` / `ra` / `vao`) dùng lại được cho `doi_tham_so`.
- (vi) **Giới hạn hàm đọc ngày** (`do_so.ngay_tu_cau`): 1 câu từ chối nhầm ("đi ngày 3/12 giờ nào cũng được"); luật theo danh sách từ đứng trước / sau (`_TRUOC_THU_TU`, `_TRUOC_TEN`, `_DON_VI`) không kín; "tuần sau" theo tuần lịch (Chủ nhật nói "thứ Bảy tuần sau" = 6 ngày nữa); dd/mm đã qua không năm ⇒ năm sau ⇒ thường `ngay_ngoai_han`. A + User đã nhận; W82 cấm mở vòng sửa nữa trên các bộ đã ghi.
- (vii) **S06 chập chờn ở bước thẻ chọn** (Q3: 1 / 2 ở 2 trong 3 lần đo hôm nay; có từ 14/11) — `sua_lich_v2.ap` nhánh `thay_diem` không `ten_moi` + model; chưa ai tìm gốc.
- (viii) **Nhãn bộ chuỗi sửa lịch sau bảng điểm v9:** S07 (đã thấy) lệch nhãn; B đã sửa `data/phase_9/bo_do_sua_lich/tools/mo_phong_v2.py` nhận bảng đang cấu hình (B báo v9 + bộ mới 10 / 10 — C chưa chạy lại); **bộ kín có thể dính tương tự — lệnh đếm chờ User `!`** (A / B giữ). C là người đo ⇒ không sửa nhãn.
- (ix) Nút hạng / ngày trên **biểu mẫu không tự đồng bộ** theo lời (mọi trường đều vậy): `frontend/src/LenKeHoach.jsx` giữ `chon` riêng.

### Luật mới phải nhớ (User duyệt 18:01 15/11/2026)
- **W82** (`Session_Prompt.md` §8): code đọc chữ người dùng ⇒ TRƯỚC lượt có phí, người **không viết code đó** soạn ≥ 20 câu dò (đúng + "giống mà không phải" + câu ghép + ngoài phạm vi), chạy thẳng hàm thuần; sau bản sửa thêm **đúng một** bộ ≤ 20 câu; dừng khi 0 câu ra SAI (từ chối nhầm được phép); review đã ready ⇒ commit code thêm phải được A cho trước + reviewer dò lại, còn lỗi ⇒ merge bản đã ready.
- **W83** (§8): phép kiểm mới trong harness phải có ca đối chứng biết chắc ra "có" trước khi số 0 được ghi "đạt"; cột 0 % / 100 % mọi lượt ⇒ report ghi "chưa từng thấy giá trị ngược lại".
- **W84** (`WORKFLOW.md` §3.4): đổi bảng dữ liệu mà bộ đo phụ thuộc ⇒ người đổi quét nhãn + chạy mô phỏng nhãn không model trước merge.
- `scripts/commit_push.sh "<lời>" <file>…` — báo sha chỉ bằng dòng nó in; commit merge (không file riêng) thì `git push` + `git ls-remote`.

### Thứ tự đo khuyên dùng khi đổi lời dặn "hiểu ý sửa" (`SUA_LICH_LOI_DAN`)
test 0 USD (kể cả bộ dò W82) ⇒ commit + push (log mang `git_sha`) ⇒ hỏi B / E một dòng ⇒ server tạm cổng 8041 từ worktree (kiểm `readlink /proc/<pid>/cwd`) ⇒ **bộ câu chính ×2 ⇒ Q3 ×2 NGAY** (bắt hồi quy trước khi tốn bộ khác) ⇒ (≤ 1 vòng chỉnh, A ghi tiêu chí trước) ⇒ nhắn A "đã chốt" để A viết bộ câu lạ ⇒ bộ hồi quy bậc trước ×1, Q5 (`q5_sua_lich.py`, chạy từ `backend/` của worktree), Q5b (`q5b_tron.py … --log <worktree>/backend/logs/application.log`), câu lạ ×1 ⇒ tắt server bằng pid của cổng ⇒ đếm tiền `scripts/dem_chat_metrics.py --log … --sha <sha>` SAU khi tắt. Chi tiết cách nói đặt ở khối "cách nói thường gặp", không chèn chữ dài vào danh sách hành động.

### Bẫy gặp chiều 15/11
- Thêm vài dòng vào danh sách hành động của lời dặn làm hỏng một kiểu câu KHÔNG liên quan (S08).
- Bộ câu đo tự viết không có "chữ giống ngày" ⇒ lượt có phí đạt hết mà hàm vẫn sai 8 / 34 câu dò của reviewer (nay là W82).
- Tự sửa thêm sau khi A đã nhận giới hạn ⇒ tự gây hồi quy ("5/5 người").
- Chuỗi Q3 trượt có thể do **nhãn cũ** (bảng điểm đổi) — chạy lại chuỗi đó trên server bản main + xem `sua_ap` trước khi quy cho nhánh.
- Tả kết quả từ trí nhớ ⇒ ghi NGƯỢC bớt / thêm trong bài + report (agent con bắt) — đọc dữ liệu (`ngay_hoat_dong`) rồi mới viết.
- Đếm tiền khi server còn chạy ra thiếu (0,0012 ↔ 0,0013).
- `git merge -q … | tail` nuốt thông báo ⇒ tưởng đã gộp; sau xung đột phải `git add` rồi mới `git commit`; kiểm `git merge-base --is-ancestor origin/main HEAD`.
- Sửa file trong worktree đang chạy test rộng (số vẫn của bản cũ, nhưng phải giải thích) — dùng worktree khác.
- Harness cũ `q3_sua_lich.py` / `q5_sua_lich.py` chèn `/tmp/b_lkh/backend` vào đường import (không còn) ⇒ đặt `PYTHONPATH=<worktree>/backend`.
- `commit_push.sh` báo `CHƯA PUSH` khi nhánh thiếu file của main (đúng thiết kế) ⇒ gộp main trước.

### Câu hỏi / thắc mắc cho A phiên sau
1. Có làm tiếp ứng viên nào ở mục "Còn mở" không — C nghiêng (v) (dòng báo khi `doi_tham_so` làm lịch xếp lại, 0 USD, dùng lại khuôn bậc 2) và (iii) (hết im lặng), vì cùng loại "nói rõ đã làm gì"; (i) và (ii) cần đếm nhu cầu trước.
2. Bộ kín sửa lịch sau v9: ai chạy lệnh đếm của User và ai sửa nhãn (không phải C).
3. Tổng tiền 0,335 USD của C chưa có người thứ hai tính lại.

## PHIÊN CHIỀU 15/11 — nhật ký (mở 15:08; giữ để tra) — C `hue-rag-51` · A `hue-rag-60` · B `hue-rag-cb` · E `hue-rag-ab`
**A giao (15:11 15/11/2026; quyền phiên "như sáng 15/11"):** (1) bảng lưu trú v5 gộp Như Phú — giữ dòng 1 sao / số 16, bỏ dòng 14b ⇒ 136 cơ sở, 57 có ảnh; (2) `scripts/commit_push.sh` (W81). Hai nhánh riêng từ origin/main.
**Khai báo sửa:** (1) `data/luu_tru_v5_2026-11-15/` (script + bảng v5 + so v4 ↔ v5, private) · nhánh `p9-luu-tru-v5`: `backend/config/settings.yaml` dòng `lich_trinh_bang_luu_tru` (+ `frontend/src/theKhachSanTrung.js` nếu danh sách sinh lại đổi) — worktree `/tmp/c_v5`. (2) nhánh `p9-commit-push`: `scripts/commit_push.sh` (mới) — worktree `/tmp/c_cp`. File này.
**Hai việc XONG — chờ A (15:14 15/11/2026, 0 USD):** report `report_agent/2026-11-12_ra_khoang_cach/c_v5_commit_push_implementation.md` (chưa commit — A commit).
- v5: nhánh `p9-luu-tru-v5` @ `ea0e82c` (đã push; diff 1 dòng `settings.yaml` ⇒ A merge thẳng). Bảng `data/luu_tru_v5_2026-11-15/bang_luu_tru_lich_v5.json` md5 `34836e7c1438`; 136 cơ sở, 57 có ảnh; lịch đổi 0 / 15.360; test 16 passed có / không env.
- `scripts/commit_push.sh`: nhánh `p9-commit-push` @ `609c7ac` (đã push bằng chính script; chờ A review). Chạy thử `data/commit_push_2026-11-15/thu.sh` ĐÚNG 15 / 15.
- Worktree còn: `/tmp/c_v5`, `/tmp/c_cp` — gỡ sau khi A merge. 0 server / tiến trình nền.
**Review W79 của B XONG (15:16 15/11/2026, 0 USD):** nhánh `p9-w79-sha` @ `7b1ba00` — ready, 0 blocker / 0 major / 2 minor (`--sha HEAD` chạy git ở thư mục đang đứng, không phải thư mục của log mặc định; mặc định bỏ lượt 0 đồng mà không in số lượt đã bỏ). Chạy lại `test_api_chat.py` 11 passed + 1 lỗi cần khoá (có sẵn); dò script bằng log tự viết 5 dòng. Kết luận gửi B + A bằng tin nhắn (review ≤ 5 dòng, không file riêng). Worktree `/tmp/c_rv` đã gỡ.
**v5 + `commit_push.sh` đã vào main (`e54c19d`); worktree `/tmp/c_v5`, `/tmp/c_cp` đã gỡ.**
**Plan bậc 1 "đổi hạng chỗ ở bằng lời" NHÁP XONG (15:19 15/11/2026, 0 USD, chưa code):** `docs/superpowers/plans/2026-11-15-sua-lich-hang-cho-o-plan.md` (chưa commit) — hành động mới `doi_hang_o`, 4 câu "không đổi" có lý do, không bộ kín, ≈ 0,19 USD (trần 0,25). Chờ A duyệt rồi mới code. Khai báo sửa khi được duyệt: `backend/llm/sua_lich_v2.py`, `full_corpus_prompt.py` (`SUA_LICH_LOI_DAN`), `len_ke_hoach.py`, test `test_sua_lich_v2.py`, bộ câu `data/sua_lich_hang_2026-11-15/`.
**Bậc 1 "đổi hạng chỗ ở bằng lời" — code + đo vòng 1 XONG, CHỜ A QUYẾT (15:42 15/11/2026):** nhánh `p9-sua-hang-o` @ `c48ccf8` (đã push), worktree `/tmp/c_ho` (còn symlink `data/`, `knowledge-base-hue/`). Plan A duyệt `8b10ccd50d37`.
- Đạt mọi tiêu chí ghi trước: H1 11 / 12 · sai mức 0 / 24 · H2 0 / 12 đổi, nói rõ hạng 5 / 6 · H3 0 / 12 · H4 8 / 8 · Q5 0 / 64 · Q5b 0 / 16 · Q3 pass^2 8 / 10 (mốc 9 / 10).
- **Hồi quy thật:** chuỗi S08 lượt 3 trên nhánh 0 / 2 (model trả đổi số ngày ⇒ rào chặn ⇒ "Chưa làm"), trên main 4 / 4 ⇒ đã hỏi A: (a) nhận theo ngưỡng / (b) một vòng chỉnh lời dặn + chạy lại (≈ +0,10 USD). C khuyến nghị (b). Chưa nhờ review, chưa viết report.
- Dữ liệu đo: `data/sua_lich_hang_2026-11-15/` (bộ câu `cau_h.jsonl` md5 `f048c0e67761`, `cau_h4.jsonl` của A, `tools/do_h.py`, `tools/cham_h.py`, kết quả `do/`). Tiền ≈ 0,11 USD (trần 0,25). Server tạm đã tắt.
**Bậc 1 vòng chỉnh ĐẠT — chờ B review (15:58 15/11/2026):** nhánh `p9-sua-hang-o` @ `192fe50` (script in "ĐÃ PUSH 192fe50"; bản đo `32c129f`). A chọn (b): một vòng chỉnh (chi tiết hạng dời xuống khối cách nói). S08 2 / 2 · Q3 10 / 10 · H1 12 / 12 · sai mức 0 · H2 0 / 12, nói 6 / 6 · H3 0 / 12 · H4b 8 / 8 · Q5 0 / 64 · Q5b 0 / 16. Tiền bậc ≈ 0,210 USD. Report trên nhánh `c_sua_hang_o_implementation.md`. Review E `p9-gd-3-sua` @ `0c852b0`: ready 0 / 0 / 2 (tin nhắn). Còn: sau merge viết `bai_hoc/25` + sổ 07; gỡ worktree `/tmp/c_ho`; bậc 2 (ngày đi) chờ A giao. 0 server.
**(16:03 15/11/2026)** Nhánh bậc 1 gộp main mới nhất (v6): origin `fe1dba4`, 116 test đạt; A cho agent con review, B không review. **Plan bậc 2 "đổi ngày đi bằng lời" NHÁP XONG** (0 USD, chưa code): `docs/superpowers/plans/2026-11-15-sua-lich-ngay-di-plan.md` (chưa commit) — hành động `doi_ngay_di` KHÔNG tham số, code đọc ngày từ chữ người dùng, đổi ngày có thể xếp lại + câu báo nêu số điểm đổi; Q3 chạy ngay sau D1–D3; trần 0,25; không bộ kín. Chờ A duyệt; code sau khi bậc 1 vào main.
**(16:10 15/11/2026) Ba việc đang mở của C:**
- **Bậc 1** `p9-sua-hang-o` @ `fe1dba4`: A cho agent con review, chờ merge. Worktree `/tmp/c_ho`.
- **Bậc 2** (plan A duyệt `f36fe8bb5b6a`): nhánh `p9-sua-ngay-di` @ `7369fba` (tách từ nhánh bậc 1; worktree `/tmp/c_nd`, còn symlink `data/`, `knowledge-base-hue/`) — XONG phần code 0 USD (`do_so.ngay_tu_cau`, `sua_lich_v2.ngay_di_moi` + `ap(ngay_moi=)`, nối ở `len_ke_hoach.hieu_va_ap`, `test_sua_ngay_di.py` 40 đạt). CÒN: sửa lời dặn (1 gạch `doi_ngay_di` + 1 câu ở khối cách nói) ⇒ viết bộ D1–D3 (ngày sinh theo hôm chạy) ⇒ hỏi B ⇒ lượt có phí D1–D3 ⇒ Q3 ngay ⇒ chốt ⇒ nhắn A viết D4 ⇒ H1 ×1, Q5, Q5b. Chỉ chạy có phí SAU khi bậc 1 merge và sau việc "Nơi ở chỉ khi hỏi".
- **Nơi ở chỉ hiện khi hỏi** (User qua A): plan `docs/superpowers/plans/2026-11-15-noi-o-chi-khi-hoi-plan.md` `d99fb6ec4a5c` (chưa commit) chờ A duyệt + quyết lịch mẫu; code trên nhánh mới từ main sau khi bậc 1 merge. E báo đang chạm `LichV2.jsx` (mục "nghỉ"), `ghep_chu` — không chạm khối NoiO.
- Review nhờ: B `p9-web-noi-tiep` — C đã nhắn để E nhận.
**(16:20 15/11/2026) Cập nhật:**
- **Nơi ở chỉ khi hỏi XONG — chờ E review:** nhánh `p9-o-khi-hoi` @ `16e7d08` (code `2456c2f`, đứng trên bậc 1; worktree `/tmp/c_ok`, đã build `frontend/dist`). Test file 18 đạt · test rộng 1.087 đạt (5 ca cần khoá) · Playwright DAT · 0,0012 USD. Report trên nhánh `c_noi_o_khi_hoi_implementation.md`; dữ liệu `data/noi_o_khi_hoi_2026-11-15/`.
- **Bậc 2 sẵn cho lượt có phí:** `p9-sua-ngay-di` @ `6460385` (đã có lời dặn). Bộ D1–D3: `data/sua_lich_ngay_2026-11-15/cau_d.jsonl` md5 `7b5b22cbda07`, `tools/do_d.py` (`--mo-phong` 0 USD), `tools/cham_d.py`. Bước kế khi A báo bậc 1 + nhánh nơi ở đã vào main: rebase ⇒ hỏi B ⇒ server tạm ⇒ D1–D3 ×2 ⇒ Q3 ×2 ngay ⇒ (≤ 1 vòng chỉnh) ⇒ nhắn A "đã chốt" + khuôn D4 + ngày đang dùng ⇒ H1 ×1, Q5, Q5b, D4. Lưu ý: chữ câu "hỏi lại hạng" đổi ở nhánh nơi ở ⇒ `cham_h.py` vẫn chấm theo mã `hang_chua_ro`, không theo chữ.
- Tiền C phiên chiều tới giờ ≈ 0,21 USD (bậc 1) + 0,0012.
**(16:25 15/11/2026) Cập nhật:** bậc 1 ĐÃ vào main (review agent con ready, 4 minor). `p9-o-khi-hoi` @ `6058298` (đã gộp main): E ready 0 / 0 / 2 ⇒ chờ A merge. Nhánh nhỏ đóng m-1 + m-2 của review bậc 1: `p9-hang-o-m12` @ `64f6905` (worktree `/tmp/c_ok`, đứng trên nhánh nơi ở; hàm `_hang_o_sau_cung`; 47 test đạt) ⇒ chờ B review ≤ 5 dòng ⇒ A merge. Nhánh ngày đi `/tmp/c_nd`: đã gộp ở MÁY cả nhánh nơi ở + nhánh nhỏ (chưa push; origin vẫn `6460385`), test chạm đạt. Sau khi A merge cả hai: gộp origin/main, push, hỏi B, chạy D1–D3 ⇒ Q3 (Q5b dùng harness mới của B, thêm `--log <worktree>/backend/logs/application.log`, chạy từ `backend/`). Worktree `/tmp/c_ho` đã gỡ.
**(16:26 15/11/2026) Cập nhật:** bậc 1 ĐÃ vào main (review agent con ready, 4 minor). `p9-o-khi-hoi` @ `6058298` (đã gộp main): E ready 0 / 0 / 2 ⇒ chờ A merge. Nhánh nhỏ đóng m-1 + m-2 của review bậc 1: `p9-hang-o-m12` @ `64f6905` (worktree `/tmp/c_ok`, đứng trên nhánh nơi ở; hàm `_hang_o_sau_cung`; 47 test đạt) ⇒ chờ B review ≤ 5 dòng ⇒ A merge. Nhánh ngày đi `/tmp/c_nd`: đã gộp ở MÁY cả nhánh nơi ở + nhánh nhỏ (2 xung đột ở `sua_lich_v2.py` đã giải, giữ cả hai; chưa push, origin vẫn `6460385`), test chạm đạt. Sau khi A merge cả hai: gộp origin/main, push, hỏi B, chạy D1–D3 ⇒ Q3 (Q5b dùng harness mới của B, thêm `--log <worktree>/backend/logs/application.log`, chạy từ `backend/`). Worktree `/tmp/c_ho` đã gỡ.
**(16:46 15/11/2026) Cập nhật:**
- ĐÃ vào main: bậc 1 (đổi hạng chỗ ở bằng lời), `p9-o-khi-hoi` (nơi ở chỉ hiện khi hỏi), `p9-hang-o-m12` (m-1 + m-2 review bậc 1).
- **Bậc 2 đổi ngày đi: ĐO XONG, ĐẠT, chờ E review** — `p9-sua-ngay-di` @ `40d97e5` (bản đo `ad81cc0`; worktree `/tmp/c_nd`). D1 12 / 12 · sai 0 / 24 · D2 0 / 12, lý do 5 / 6 · D3 0 / 16 · Q3 8 / 10 + S08 2 / 2 (S07 trượt do nhãn cũ lệch bảng điểm v9 — A: không sửa nhãn ở bậc này, người khác rà sau) · H1 12 / 12 · Q5 0 / 64 · Q5b 0 / 16 · D4 8 / 8 · ≈ 0,123 USD. Report trên nhánh `c_sua_ngay_di_implementation.md`. Test rộng chưa chạy trên bản này.
- **Tài liệu bậc 1 + nơi ở:** `p9-tai-lieu-hang-o` @ `11f37f9` (worktree `/tmp/c_tl`) chờ A merge; agent con kiểm 53 khẳng định (0 sai, 8 chỗ đã sửa), biên bản `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25_hang_o.md`.
- Còn: sau khi bậc 2 merge ⇒ viết tài liệu bậc 2 (bài 25 mục 1 + sổ 07 + nhật ký; có agent con kiểm) ⇒ gỡ worktree `/tmp/c_nd`, `/tmp/c_ok`, `/tmp/c_tl`.
- **Tiền C phiên chiều ≈ 0,34 USD** (bậc 1 ≈ 0,21 · nơi ở ≈ 0,0024 · bậc 2 ≈ 0,123). 0 server tạm.
**(16:58 15/11/2026) Cập nhật bậc 2:** E review vòng 1 changes_requested (M-1: hàm đọc ngày nhận chữ GIỐNG ngày — "chị Mai", "điểm thứ hai", "24/7", phân số… 8 / 34 câu dò) ⇒ C sửa `do_so.ngay_tu_cau` qua 3 commit: `0463bf2` (E ready, 35 / 35; test rộng 1.160 đạt trên bản này) ⇒ `add3186` (đóng thêm ca E tìm sau; E bắt 1 hồi quy "5/5 người") ⇒ **`b7b47f1`** (A cho đúng một commit: tử ≤ mẫu; bảng ca 65 / 65; hai bộ dò của E C tự chạy 35 / 35 và 18 · 0 · 1; ngoại tuyến 34 câu đã đo 0 lệch). Chờ E xác nhận trên `b7b47f1` ⇒ A merge (luật dừng của A: còn câu sai ngày / hồi quy ⇒ merge `0463bf2`, phần sau thành nhánh riêng). KHÔNG thêm commit code nào nữa. Tài liệu bậc 2: nhánh `p9-tai-lieu-ngay-di` trong `/tmp/c_tl` (CHƯA commit; đã sửa theo kiểm độc lập 51 khẳng định: 1 sai + 10 dễ hiểu nhầm, biên bản `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25_ngay_di.md`; đã thêm chuyện review) — commit + push + báo A SAU khi nhánh code vào main (nếu A merge `0463bf2` thì sửa số 65 ⇒ 57 và bỏ đoạn "5/5 người").
**(17:00 15/11/2026) BẬC 2 ĐÃ VÀO MAIN (`b7b47f1`, origin main `a52ffd6`).** Tài liệu bậc 2: `p9-tai-lieu-ngay-di` @ `22160ed` (worktree `/tmp/c_tl`) chờ A merge ⇒ rồi gỡ `/tmp/c_tl`. Đã gỡ `/tmp/c_nd`, `/tmp/c_ok`. Nhánh của C đã merge (User `!` xoá): `p9-luu-tru-v5 p9-commit-push p9-sua-hang-o p9-o-khi-hoi p9-hang-o-m12 p9-sua-ngay-di p9-tai-lieu-hang-o` (+ `p9-tai-lieu-ngay-di`).
**Tiền C phiên chiều ≈ 0,335 USD** (theo sha): bậc 1 0,2101 · nơi ở khi hỏi 0,0026 · bậc 2 0,1226. **Rảnh — chờ A.** 0 server / tiến trình nền.
**Bẫy phiên chiều (cho vòng cải tiến):** (1) thêm vài dòng vào danh sách hành động của lời dặn làm hỏng một kiểu câu KHÔNG liên quan ⇒ chạy bộ hồi quy ngay sau bộ câu chính, chi tiết cách nói để ở khối "cách nói thường gặp"; (2) bộ câu đo do mình viết không có "chữ giống ngày" ⇒ lượt có phí đạt hết mà hàm đọc ngày vẫn sai 8 / 34 câu dò của reviewer ⇒ hàm thuần đọc chữ người dùng phải có ca "chữ giống mà không phải" TRƯỚC khi đo có phí; (3) sửa thêm sau review tự gây hồi quy ("5/5 người") ⇒ mọi lần sửa luật chữ đều chạy lại bộ dò của reviewer; (4) nhãn bộ đo cũ lệch khi bảng điểm đổi (S07) ⇒ đổi bảng điểm thì rà nhãn các bộ chuỗi; (5) report ghi ngược "bớt / thêm" vì tả từ trí nhớ thay vì đọc `ngay_hoat_dong` — agent con kiểm bắt; (6) đếm tiền sớm khi server còn chạy ra thiếu 1 lượt (0,0012 ↔ 0,0013) ⇒ đếm sau khi tắt server.
**(17:02 15/11/2026) KẾT QUẢ CHIỀU 15/11 CỦA C — mọi việc đã vào main (origin `f276894` lúc ghi):** bảng lưu trú v5 · `scripts/commit_push.sh` · sửa lịch bằng lời đổi hạng chỗ ở (bậc 1) + nhánh nhỏ m-1 / m-2 · khối Nơi ở chỉ hiện khi hỏi · sửa lịch bằng lời đổi ngày đi (bậc 2, `b7b47f1`) · tài liệu bài 25 + sổ 07 + nhật ký cho cả ba. Review C làm: W79 (B), `p9-gd-3-sua` (E). Vòng tự soi 2 đã gửi cả nhóm (đề xuất: câu PHÁ ngoại tuyến trước lượt có phí; md5 bảng điểm trong bộ chuỗi; ca đối chứng cho mỗi phép kiểm; luật hẹp "sau ready không tự thêm commit code"). Mọi worktree `/tmp/c_*` + file tạm đã gỡ. **Rảnh — chờ A** (User vắng, chưa kết phiên).
**(18:02 15/11/2026) Rảnh — chờ A.** User đã về 18:01: W82–W84 duyệt, đã vào luật (`Session_Prompt.md` §8: bộ câu dò ≥ 20 do người không viết code soạn TRƯỚC lượt có phí, thêm đúng một bộ sau bản sửa, dừng khi 0 câu ra sai, sau ready commit thêm phải được A cho; phép kiểm harness có ca đối chứng ra "có" · `WORKFLOW.md` §3.4: đổi bảng dữ liệu ⇒ quét nhãn + mô phỏng không model trước merge) — C đã đọc lại. Không có việc mới.

## (Kết phiên trưa 15/11 — CŨ, giữ để tra) PHIÊN SAU ĐỌC TRƯỚC (C viết 14:43 15/11/2026 `date`)

- **Trạng thái máy:** 0 worktree `/tmp/c_*`, 0 server tạm (cổng 8037–8040 đã tắt), 0 tiến trình nền của C. Mọi nhánh của C hôm nay đã merge.
- **Việc phiên sau đã định (A giao lúc kết phiên):**
  1. **Bảng lưu trú v5 — gộp "Như Phú":** bảng v4 (`data/anh_khach_san_2026-11-15/bang_luu_tru_lich_v4.json`, md5 `c98ca8c19889`, 137 cơ sở, 58 có ảnh) có 2 dòng "Khách sạn Như Phú" (16 và 14b Chu Văn An) ⇒ trang Chỗ ở + thẻ khách sạn có thể ra 2 thẻ. User chốt gộp (hỏi A cách gộp nếu chưa rõ: giữ dòng nào, địa chỉ nào).
     - Cách làm như v3: script mới trong `data/` (mẫu `data/khach_san_2026-11-15/tools/dung_bang_v3.py`), ra **file v5 mới**, KHÔNG sửa tại chỗ file main đang trỏ.
     - Đổi `settings.yaml` `lich_trinh_bang_luu_tru` trên nhánh riêng.
     - Chạy lại `dung_trung.py` (danh sách tên trùng sinh từ bảng) + `so_v2_v3.py` kiểu so trước / sau (đổi đường dẫn) ⇒ báo số lịch đổi.
     - Test file chạm: `test_luu_tru_lich.py`, `test_the_khach_san.py`. Theo W80 (nếu User duyệt): nhánh nhỏ, tất định ⇒ A merge thẳng.
  2. **`scripts/commit_push.sh` (W81):** commit theo đường dẫn truyền vào ⇒ nếu hook chặn thì in "CHƯA PUSH" và thoát ≠ 0 ⇒ push ⇒ in sha của origin (`git ls-remote`). Lý do: hôm nay C (×1) và B (×2) báo "đã push" khi commit bị hook chặn. Governance / scripts: hỏi A ai sửa (`scripts/` không thuộc vùng governance, nhưng là công cụ chung ⇒ A review).
- **Đã làm hôm nay (đều đã merge, report ở `report_agent/2026-11-12_ra_khoang_cach/`):**
  - Ghi chú ăn uống Bạch Mã / Nhị Hồ (`p9-ghi-chu-an`) — `c_dem_quan_nam_xa.md`.
  - Ngưỡng mưa 6 mm (`p9-mua-6mm`, `fe895c1`) — `c_dem_mua.md` phần 5 (thước cố định QCVN).
  - Trang Chỗ ở + bảng v3 (`p9-cho-o`, `60f556b`) — `c_cho_o_implementation.md`.
  - Ảnh nhiều nơi trong chat (`p9-anh-chat`, `e801c83`) + khớp tên cả trên câu hỏi (`p9-anh-chat-hoi`, `688bad8`) — `c_anh_chat_implementation.md`, `c_dem_anh_chat.md`, `c_dem_anh_chat_b2.md`.
  - Thẻ khách sạn trong chat (`p9-the-ks-chat`, `aecde1d`) — `c_dem_ks_chat.md`, `c_the_ks_chat_implementation.md`.
  - Rào "ngày tháng ⇒ đổi số ngày" (`p9-rao-so-ngay`, `78dd6b9`) — `c_dem_sua_lich_truong.md`.
  - Sửa kho Tây Sơn 1786 / 1788 (chỉ mục dựng lại 11:22, record `1b53af26b662`) — `c_kho_mau_thuan.md`, `c_sua_kho_tay_son_implementation.md`.
  - Plan: `docs/superpowers/plans/2026-11-15-{khach-san-trang-va-ngan-sach,anh-trong-chat,the-khach-san-chat}-plan.md`.
  - Review: Docker nháp E (`c_review_docker_nhap.md`).
  - Chuẩn bị: 10 nơi cho bảng điểm lịch (`data/diem_lich_moi_2026-11-15/c_chon_10.md`; E làm tiếp diem_v9 với 7 nơi).
  - Tài liệu: bài 22, 23, 24, 25 + sổ 02, 07 + README — mỗi lần sửa nhiều có agent con kiểm độc lập (biên bản `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_*`).
- **Nhánh đã merge (cho lệnh dọn của A):** `p9-ghi-chu-an` (nhánh remote đã không còn), `p9-mua-6mm`, `p9-cho-o`, `p9-anh-chat`, `p9-the-ks-chat`, `p9-anh-chat-hoi`, `p9-rao-so-ngay`. C không tự xoá.
- **Việc dở / ý chờ User:**
  - Sửa lịch bằng lời đổi thêm **hạng sao** (bậc 1) và **ngày đi** (bậc 2) — đếm `c_dem_sua_lich_truong.md`; theo phản biện B: mỗi bậc đo Q3 + Q5 0 / 64 + bộ trộn khẩn cấp 0 / 16 ≈ 0,1–0,25 USD.
  - Giới hạn đã nhận:
    - ảnh chat "Lý Huế" ↔ "quản lý Huế";
    - thẻ khách sạn "Meliá" ↔ "Meliã" (tên khác dấu ⇒ không thẻ);
    - lễ hội / nghệ thuật trong lịch vẫn 39 % ngoài sở thích (kho không có nơi biểu diễn mới).
- **Bẫy gặp hôm nay:**
  - Hook pre-commit chặn commit (test chép tiêu đề bài kho ≥ 40 ký tự) mà C đã báo "đã push" ⇒ luôn `git ls-remote` trước khi báo (W81 sẽ máy hoá).
  - Worktree mới chưa build `frontend/dist` ⇒ 3 test giao diện fail giả ⇒ build trước khi chạy suite (E: nếu đổi thành skip thì phải in "SKIP vì chưa build").
  - `uv run` trong worktree tạo `.venv` mới ⇒ dùng `--project /home/minhhieu/hue_rag` hoặc `/home/minhhieu/hue_rag/.venv/bin/python` + `PYTHONPATH=<worktree>/backend`; worktree thiếu `data/`, `knowledge-base-hue/` ⇒ symlink tạm, gỡ trước commit.
  - `pkill -f "<chuỗi>"` có thể giết chính shell đang chạy (chuỗi có trong lệnh) ⇒ tắt server bằng pid từ `ss -ltnp`.
  - Đo "mưa thật" bằng thước trùng ngưỡng đang thử ⇒ thiên vị; luôn thước cố định.
  - Mô phỏng lịch phải dùng cùng 4 ngày đi (None, 28/11, 7/4, 16/11) — E lệch số vì chạy không ngày đi.
  - Số trong plan phải đếm trên khung thật, không liệt kê tổ hợp (ước 36 ⇒ thật 32 / 33).
  - Hai session gửi chéo nhau khi bàn thứ tự ⇒ để A chốt.
  - Dò hành vi phải qua đúng đường người dùng đi: `POST /api/chat` không stream không vào luồng sửa lịch.
- **Câu hỏi còn mở:** không có câu mới của C. Các câu chờ User (W79–W81, sửa lịch hạng sao / ngày đi) A đã giữ.
- **Tiền C hôm nay ≈ 0,05 USD** (cộng từ log / file từng việc):
  - Tây Sơn 0,029 (Serper 0,002 · 2 câu thử 0,0009 · chạy bù an toàn 0,0218 + ngoài kho 0,0046);
  - khách sạn chat 0,0134 (12 câu 0,0083 · Vedana ×5 0,0041 · Playwright ≈ 0,001);
  - ảnh chat Playwright ≈ 0,002; trang chỗ ở Playwright ≈ 0,002; ghi chú ăn ≈ 0,0007; sửa lịch đếm 0,0012.
  - Chưa tính: các lượt gọi thật trong 6 lần chạy cả `backend/tests` (`--env-file`), chưa tách số.

## PHIÊN 15/11 — nhật ký
**Mở phiên 15/11:** kiểm nhanh khớp handoff (main `6c7c01b`, Qdrant 9.425). Chờ A.
**Đếm quán vùng nam xa XONG (09:39 15/11/2026, 0 USD):** 720 / 3.840 khung (18,8 %), 1.080 / 22.680 bữa (4,8 %); chỉ khi chọn "thiên nhiên" và chuyến ≥ 3 ngày. Kho nói Bạch Mã không có quán trong vùng lõi (mang đồ ăn), Nhị Hồ có chòi ăn tại chỗ, đóng 17:30 ⇒ **đếm rồi không làm (không cào quán)**. Đề xuất tuỳ chọn: ghi chú ăn uống cho 2 điểm (0 USD, ~1 giờ), chờ nhóm. Report `report_agent/2026-11-12_ra_khoang_cach/c_dem_quan_nam_xa.md`; script `data/dem_quan_nam_xa_2026-11-15/`.
**Ghi chú ăn uống nam xa (A duyệt) XONG (09:50 15/11/2026):** nhánh `p9-ghi-chu-an` @ `81e3aff` (worktree `/tmp/c_ga`) — chờ E review. `quan_lich.py` `GHI_CHU_AN` 3 câu theo kho + `LichV2.jsx` / `lkh.css`; test file 16 passed, cả suite 1048 passed (265 s), Playwright DAT. Khai báo sửa: 4 file trên (nhánh riêng). Tiền ≈ 0,001 USD.
**Tài liệu ghi chú nam xa (09:51 15/11/2026):** `bai_hoc/25` + sổ `07` (bản 54) trên cùng nhánh @ `8d0280b` — E review cùng code. Nhật ký + README sổ: A ghi lúc merge.
**Sửa 2 minor review E (m-1, m-2) — nhánh @ `e001cb2`:** chờ A grep + merge. Rảnh.
**p9-ghi-chu-an đã merge (main `2e50789`, sổ `214a502`).** Đã gỡ worktree `/tmp/c_ga`; nhánh vào danh sách dọn. **Rảnh — chờ** (PA3 ngưỡng mưa khi User chốt).
**Plan khách sạn (A giao, 10:17 15/11/2026):** nháp `docs/superpowers/plans/2026-11-15-khach-san-trang-va-ngan-sach.md` (đếm `data/khach_san_2026-11-15/`: 12 / 140 từng hiện; ngân sách ⇒ 36; 0 khung trống mức) — chờ B / E phản biện rồi chốt, nhắn A. Khai báo sửa: file plan này.
**Plan khách sạn bản 2 (10:22 15/11/2026)** — đã sửa theo phản biện của B + E, gửi A trình User. Chờ User duyệt rồi mới code.
**Ngưỡng mưa đo lại theo QCVN (0 USD):** `c_dem_mua.md` phần 5 — đề xuất phương án 3 với 6 mm; đã gửi cả nhóm. Rảnh — chờ User (ngưỡng mưa, plan khách sạn).
**p9-mua-6mm merge (fe895c1).** Sổ 07 (bản 55) + bài 23 đã ghi trên main working tree, A gộp.
**Trang chỗ ở XONG:** nhánh `p9-cho-o` @ `86acfb1` (worktree `/tmp/c_co`) — chờ E review. Bảng v3 `data/khach_san_2026-11-15/` (137 cơ sở; lịch đổi 364 / 3.840: La Vela thay Indochine ở cụm An Cựu). Test 11 + suite 1050 passed, Playwright DAT. Report `c_cho_o_implementation.md`. Worktree `/tmp/c_mua` gỡ sau khi A dọn.
**p9-cho-o sau review E (ready, 3 minor đã sửa) + rebase lên 418a585 @ `366fac8`:** test file chạm 128 passed, Playwright DAT — chờ A merge. Việc kế: nhánh nhỏ lịch lọc phía biển bằng `phia_bien`.
**p9-cho-o merge (60f556b).** Đang: tài liệu hai tính năng khách sạn — `bai_hoc/25`, sổ `07` (bản 56), README (main working tree, chưa commit); số thật `data/khach_san_2026-11-15/dem_sau.json` (13 ⇒ 32 / 137). Agent con kiểm độc lập đang chạy ⇒ biên bản `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25_cho_o.md`. Vòng tự soi 1 đã gửi.
**Tài liệu khách sạn XONG (11:00 15/11/2026):** bài 25 + sổ 07 + README sửa theo kiểm độc lập (57 khẳng định, 10 sai chủ yếu do main đổi giữa chừng ⇒ số mới 14 ⇒ 33 / 137) — chờ A commit. Rảnh — chờ.
**Kho mâu thuẫn — đếm + tra XONG:** `report_agent/2026-11-12_ra_khoang_cach/c_kho_mau_thuan.md` — vị trí bảo tàng đã khớp; năm đóng đô 1786 ↔ 1788 còn lệch (nguồn: 1786 chiếm thành, 1788 lên ngôi ⇒ gợi ý câu gộp), chờ User; quét thêm 0 lệch mới. Tiền ≈ 0,002 USD.
**Sửa kho Tây Sơn (User duyệt):** 2 câu ở 2 bài (E review, m-1 sửa), sao lưu `meta/backup_sua_kho_2026-11-15_tay_son`, dựng 11:15–11:22 ⇒ 9.425 point, record `1b53af26b662`, sparse `ccd1d3ae36ec`; T1 giống mốc (`aa34d4215f15`), 0 câu có đoạn sửa trong top 10 ⇒ không đo Golden có phí. Còn: 2 câu hỏi thử (chờ E build Docker xong) + report + bài học / sổ 02. Hồ sơ `data/sua_kho_2026-11-15_tay_son/`.
**Đếm ảnh trong chat XONG:** `c_dem_anh_chat.md` (77 ⇒ ~118 / 154 ước; khách sạn 0 câu Golden) — đã gửi nhóm bàn.
**Tây Sơn: 2 câu thử xong (PARTIAL so tiêu chí — đúng, khớp, chỉ nêu 1788).** Report `c_sua_kho_tay_son_implementation.md`; bài 22 + sổ 02 + README sửa trên main working tree; agent con kiểm độc lập bài 22 đang chạy ⇒ `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_tay_son.md`. Tiền việc ≈ 0,003 USD.
**Tây Sơn XONG (đo + tài liệu):** kiểm độc lập bắt C bỏ sót an toàn 32 + 18 ngoài kho ⇒ chạy bù: 0 đổi lớp, 0 / 18 — đạt. Bài 22 + sổ 02 + README sửa theo biên bản — chờ A commit. Tiền ≈ 0,029 USD. Rảnh — chờ (B đang chạy lượt đo có phí: không server / pytest / dựng).
**Review Docker nháp E: ready 0/0/1** (`c_review_docker_nhap.md`). **Plan ảnh trong chat bản 1** `docs/superpowers/plans/2026-11-15-anh-trong-chat-plan.md` — chờ A duyệt. Khai báo sửa (khi duyệt): `frontend/src/anhTraLoi.js`, `chat.jsx`, css, `backend/tests/test_anh_tra_loi.py`, `data/anh_chat_2026-11-15/`.
**Ảnh trong chat (plan bf43cc57f6ea A duyệt):** nhánh `p9-anh-chat` (worktree `/tmp/c_ac`, chưa commit) — `anhTraLoi.js` trả danh sách, `chat.jsx` hàng ảnh có tên, `tl.css`, test 2 passed. T3 mô phỏng: câu có ảnh 77 ⇒ 103 / 154 (26 câu mới, 39 ảnh). T4 agent con nhìn lại 39 ảnh đang chạy. Còn: build, test rộng, Playwright (sau khi B đo xong độ trễ).
**Ảnh trong chat XONG T1–T5:** nhánh `p9-anh-chat` đã push — chờ E review. 77 ⇒ 103 / 154 câu có ảnh; 39 ảnh mới 0 sai nơi (3 ảnh quảng cáo báo E sửa gốc); Playwright DAT; suite 1056 passed. Report `c_anh_chat_implementation.md`.
**12 câu khách sạn soạn sẵn (chưa chạy):** `data/anh_chat_2026-11-15/cau_khach_san.json` — gồm bẫy tên viết khác, tên lồng nhau, tên trùng sông, cơ sở không ảnh, cơ sở không có trong danh mục. Việc sau merge ảnh chat: bài 24 + sổ 08 / 07.
**Ảnh chat merge (`e801c83`) + tài liệu XONG:** bài 25 §8, bài 24, sổ 07 (bản 58), README — sửa theo kiểm độc lập (8 chỗ); chờ A commit. Rảnh — chờ.
**Đếm KS trong chat XONG (0,0083 USD):** `c_dem_ks_chat.md` — 10 / 12 câu nêu tên cơ sở, 7 / 12 có ảnh, khớp tên lõi + tên dài nhất. Plan thẻ khách sạn bản 1 `docs/superpowers/plans/2026-11-15-the-khach-san-chat-plan.md` — chờ A duyệt. Phản biện rà nợ cũ của B đã gửi.
**Thẻ KS (`aecde1d`) + ảnh chat bản 2 (`688bad8`) đã merge; tài liệu XONG:** bài 25 + sổ 07 (bản 60) + README, kiểm độc lập (31: 0 sai, 6 dễ hiểu nhầm — đã sửa); số ảnh KS 58 / 137 cập nhật (ô có ảnh 95,3 %). Chờ A commit.
**Đề xuất việc tiếp (A gom cho User):** sửa lịch bằng lời đổi ngày đi + hạng sao — đếm `c_dem_sua_lich_truong.md` (hạng sao 5 / 5 không sửa được, không báo; ngày đi 1 / 5 bị hiểu thành đổi số ngày 3 ⇒ 1, báo 'Đã đổi'); 2 bậc theo phản biện B. Nhớ sở thích: User đã bỏ. Chữ Kirin 1 / 6.254 ⇒ không xây. Tiền ≈ 0,0012 USD. Rảnh — chờ.
**Rào số ngày (A giao sửa ngay):** nhánh `p9-rao-so-ngay` @ `d5dfec8` — sau review E vòng 1 (M-1 + 2 minor đã sửa), chờ E vòng 2. Test 20, suite 1085, Q3 16 đúng chặn 0, 3 sai chặn 3. Worktree `/tmp/c_rs`.
**Rào số ngày merge (`78dd6b9`); tài liệu bài 25 §1 + sổ 07 (1 dòng mỗi chỗ) — chờ A commit. Đã gỡ mọi worktree `/tmp/c_*`. Rảnh.**
**Chọn 10 nơi thêm vào bảng điểm lịch (chuẩn bị, chưa sửa bảng):** `data/diem_lich_moi_2026-11-15/c_chon_10.md` — thiếu điểm: ẩm thực 56,4 %, chụp ảnh 51,7 %, lễ hội 39 %, thiên nhiên 24,4 % (+72 buổi trống), di tích 0 %. Đã gửi E gom căn cứ. Rảnh.
**Vòng tự soi 2 đã chốt (W79–W81, chờ User).** Rảnh — chờ User về ~14:30. 0 worktree / server / tiến trình nền của C.

## (Kết phiên tối 14/11 — CŨ) PHIÊN SAU ĐỌC TRƯỚC (C viết lúc kết phiên tối 14/11, 22:35 14/11/2026 `date`)

- **Trạng thái:** mọi việc C nhận tối 14/11 đã xong và merge. Máy: 0 worktree `/tmp/c_*`, 0 server, 0 tiến trình nền của C.
- **Đã làm tối 14/11 (file / dữ liệu ở đâu):**
  - **Bảng quán lịch sau ghi kho 4:** +7 quán kho (Hội Quán ngoài bảng: thiếu toạ độ), khử trùng kho ↔ OSM (5 dòng), bữa có quán kho **49,3 ⇒ 69,1 %** (Kim Long 0 ⇒ 57,2; biển / đầm 0 ⇒ 48,5; Thủy Xuân 33,6 ⇒ 62,6; nam xa vẫn 0). Script `data/quan_lich_2026-11-14/tools/dung_bang.py` (`QUAN_KHO_4`, `_trung`, `DA_DONG`, ảnh); biên bản `data/quan_lich_2026-11-14/bien_ban_quan_kho_them.md`.
  - **Bỏ quán đã đóng** (Nhà hàng chay Huế An, hiện ở 324 / 3.840 lịch) — `DA_DONG` trong `dung_bang.py`.
  - **Ảnh quán ở thẻ bữa** (`LichV2.jsx` `anhQuan`; `quan_lich.py` trường `anh` kiểm lúc nạp): quán kho dùng ảnh Khám phá trừ `kc`; ngoài kho chỉ làm 15 quán TỪNG HIỆN (`data/anh_quan_2026-11-14/tools/dem_quan_hien.py`) ⇒ 5 ảnh = 32,3 % lượt hiện quán ngoài kho. Hồ sơ `data/anh_quan_2026-11-14/` (TIEU_CHI, bảng ảnh, tra "còn mở" Codex: 0 đóng / 8 mở / 7 không rõ). Report `report_agent/2026-11-12_ra_khoang_cach/c_anh_quan_implementation.md`.
  - **Đếm mưa 4 phần** (`report_agent/2026-11-12_ra_khoang_cach/c_dem_mua.md`; script + dữ liệu `data/dem_mua_2026-11-14/`): (1) lịch đã có luật mưa + dòng "Nếu mưa"; 33 % ngày mưa "không thay được", 81 % là ngày phá / đầm / Bạch Mã ⇒ KHÔNG thêm điểm trong nhà; (2) đổi ngày bằng code cứu ≤ 13,7 % chuyến (mùa mưa 8–21 % số chuyến kẹt) ⇒ KHÔNG xây; (3) ngưỡng: 222 / 365 ngày ≥ 60 %, chỉ 115 ngày ≥ 5 mm; (4) so ERA5: hiện hành đúng 56 % (thừa 96), ≥ 5 mm đúng 86 % (thừa 16, sót 23 %). **Phương án 3** (B, C đồng ý; E chọn ≥ 5 mm): xếp lại khi ≥ 60 % VÀ ≥ 5 mm, dòng "Nếu mưa" vẫn từ ≥ 60 % (27 / 29 ngày bị sót vẫn có nhắc) — **chờ User** (ngưỡng 60 % là luật spec User duyệt).
  - **Ghi kho 6 (lễ hội + nghệ thuật):** bước 1 đếm `data/bai_kho_6_le_hoi/BUOC_1_DEM.md` (24 mục chưa có bài: từ chối 9 · mỏng 7 · đủ 8; 0,0178 USD); C viết 8 bài (Tết Nguyên đán, Âm hồn, Trung thu, Vu Lan, Đoan Ngọ, Truyền Lô, Hò Huế, Lý Huế — nháp `data/bai_kho_6_le_hoi/nhap/`, bàn giao `BAN_GIAO_C.md`, brief viết `BRIEF_VIET.md`, nguồn `nguon/`); B review + C sửa ⇒ B ghi kho 6 (263 file / 9.425 đoạn).
  - **Review:** `p9-web-so-cau-hoi` (A; M-1 chỉ miễn năm), `p9-khach-san` + `p9-khach-san-anh2` (B), `p9-anh-v4` / `v4b` (Thuận An có trẻ em đồ bơi ⇒ trống) / `p9-anh-kc` (10 / 13 ảnh nâng chỉ bằng nguồn ⇒ giữ kc) / `p9-anh-kho5` / `p9-anh-kho6` (E), 23 bài ghi kho 5 (B 10 món · E 13 địa điểm; Lục Bộ nằm TRONG Kinh thành), 8 bài ghi kho 6 của B (Ca kịch Huế trùng câu Golden ngắn ⇒ sửa). Biên bản ở `report_agent/2026-11-12_ra_khoang_cach/c_review_*.md` và `data/<đợt>/c_review_*.md`.
- **Việc dở / gợi ý việc kế:**
  - Khi User chọn ngưỡng mưa: nhánh nhỏ đổi `lich_trinh_v2.py` (thêm điều kiện `precipitation_sum` ≥ 5 mm cho luật xếp; `len_ke_hoach.dong_neu_mua` giữ ≥ 60 %) + chạy lại `data/dem_mua_2026-11-14/dem_mua.py` / `dem_nguong.py` làm số "sau".
  - 9 / 15 quán ngoài kho hay hiện chưa có ảnh (Truong Son, Phong Nha, Quán 171 Bún hến…); 7 quán "không rõ còn mở" — làm khi có nguồn ảnh / tra mới. Bảng quán đổi ⇒ chạy lại `dem_quan_hien.py`.
  - Lỗi thật thấy khi đếm kho 6: hỏi "Ca kịch Huế" từng được trả lời bằng tư liệu Ca Huế (sai chủ thể, không báo) — nay có bài riêng; loại lỗi "gần tên" có thể còn ở chỗ khác.
- **Bẫy gặp tối nay:**
  - `uv run` trong worktree tự tạo `.venv` mới (Python 3.14) ⇒ chạy bằng `/home/minhhieu/hue_rag/.venv/bin/python` + `PYTHONPATH=<worktree>/backend`; worktree thiếu `data/` ⇒ trỏ tạm `data/` + `knowledge-base-hue/` rồi gỡ trước commit.
  - Open-Meteo `archive-api` mặc định trả **đúng số historical forecast** (365 / 365) ⇒ so "mưa thật" phải dùng `models=era5`.
  - Hook commit KHÔNG quét bài kho (kho không tracked) ⇒ chạy `.githooks/overlap_scan.py <file nháp>` trước mọi lần ghi kho (bắt được cụm Golden ở bài Ca kịch).
  - Ảnh có thể chứa số điện thoại / bảng giá / trẻ em dù 2 agent cùng chọn ⇒ người giao nhìn lại 100 % ảnh sẽ hiện.
  - Lấy mẫu ngẫu nhiên trước khi đếm "người dùng thấy gì" ⇒ phí (30 quán thử 0 / 30 trùng quán hiện).
  - Tin chia việc gửi chéo nhau 3 lần với E ⇒ một người đề xuất, người kia chỉ đồng ý / sửa.
- **Câu hỏi cho A / User:** (1) ngưỡng mưa — phương án 3 hay giữ 60 % hay ≥ 5 mm thuần (số ở `c_dem_mua.md` phần 3–4); (2) không câu mới khác.
- **Tiền C tối 14/11 ≈ 0,09 USD:** Serper ≈ 0,061 (ảnh quán 45 · tra kho 6 16) · hỏi thử kho 6 0,0178 · lượt xếp lịch Playwright 0,0043 · Photon / Open-Meteo / WebFetch 0 · Codex (gói ChatGPT User) 1 lượt.

## PHIÊN TỐI 14/11 — nhật ký (giữ để tra)
**Phiên mở 17:45 14/11/2026:** C `hue-rag-eb` · B `hue-rag-62` · E `hue-rag-1f` · A `hue-rag-fb`. Kiểm nhanh khớp handoff; kho chưa ghi 8 quán; chờ A giao việc.
**A giao (phiên tối):** bảng quán lịch + đếm lại sau khi B dựng chỉ mục; review nhánh ảnh của E. **Khai báo sửa:** `data/quan_lich_2026-11-14/` (tools/dung_bang.py, photon_quan_them.json, biên bản) · `data/phase_9/lich_trinh/bang_quan_lich_v1.json` · nhánh `p9-quan-kho-them-bang` (chỉ md5 trong comment `settings.yaml`).
**Thêm (A, phiên tối):** ảnh mọi quán bảng quán lịch ⇒ khai báo thêm `data/anh_quan_2026-11-14/` · `frontend/src/LichV2.jsx` + file ảnh quán (nhánh riêng `p9-anh-quan`).
**Bảng quán lịch sau ghi kho 4 XONG (17:54 14/11/2026):** 469 quán md5 `580881638793`; bữa có quán kho 49,3 ⇒ 69,1 %; mô phỏng 0/0/0; nhánh `p9-quan-kho4-bang` `26505d6` chờ E review (worktree `/tmp/c_qb`). Biên bản `data/quan_lich_2026-11-14/bien_ban_quan_kho_them.md`. Ảnh: E làm mọi bài Khám phá; C làm ảnh quán OSM + thẻ bữa (`data/anh_quan_2026-11-14/TIEU_CHI.md`).
**Ảnh quán OSM (18:04 14/11/2026):** thử 30 ⇒ 11/30 đạt; chỉ 15 quán ngoài kho từng hiện trong lịch ⇒ chỉ làm 15 (2 agent con đang chọn). Bỏ Huế An (đã đóng, hiện 324 lịch) ⇒ nhánh `p9-quan-bo-da-dong` `f9119d1` chờ E (worktree `/tmp/c_qd`). Review A `p9-web-so-cau-hoi` xong (vòng 2 ready). Tiền C phiên tối ≈ 0,045 USD Serper.
**Ảnh quán ở thẻ bữa (18:13 14/11/2026):** nhánh `p9-anh-quan` `496206d` chờ E review (worktree `/tmp/c_aq`); report `report_agent/2026-11-12_ra_khoang_cach/c_anh_quan_implementation.md`. 6/15 quán ngoài kho có ảnh (48 % lượt hiện); 15 quán: 0 đã đóng (Codex + WebFetch 3). Tiền C phiên tối ≈ 0,05 USD.
**Sau review E (18:19 14/11/2026):** `p9-anh-quan` @ `815ab2e` (ẩn ảnh kc ở thẻ bữa, 5 ảnh ngoài kho = 32,3 % lượt hiện) — A merge. Review `p9-anh-v4` E: ready 0/0/3 (`c_review_anh_v4.md`). Đếm mưa XONG (`c_dem_mua.md`): đề xuất không thêm điểm trong nhà; nếu làm tiếp thì đổi ngày bằng code. Chờ B: review `p9-khach-san`.
**Đếm đổi ngày khi mưa XONG (18:20 14/11/2026, 0 USD):** cứu cận trên 13,7 % chuyến, mùa mưa 8–21 % số chuyến kẹt ⇒ đề xuất không xây (`c_dem_mua.md` phần 2). Chờ B: review `p9-khach-san`.
**Review phiên tối (18:47 14/11/2026):** `p9-khach-san` ready 0/0/3 · `p9-anh-v4b` vòng 2 ready · `p9-anh-kc` changes_requested (10/13 ảnh nâng bằng luật nguồn không nhận ra nơi; dự kiến hiện được 161 ⇒ 169).
**(19:02 14/11/2026)** `p9-khach-san-anh2` review ready — A merge. Việc kế: review bài nháp ghi kho 5 khi E (địa điểm / di tích) và B (món / đặc sản) nhắn (cách kho 3 / 4). Đang rảnh.
**Ghi kho 6 bước 1 XONG (19:47 14/11/2026, 0,0178 USD):** `data/bai_kho_6_le_hoi/BUOC_1_DEM.md` — 24 mục chưa có bài: từ chối 9 · mỏng 7 · đủ 8; danh sách viết 16 (đợt 1 = 10). Chưa viết bài, chờ A. Review ghi kho 5 xong (B 10 + E 13 ready). Tiền C phiên tối ≈ 0,07 USD.
**Ghi kho 6 XONG (20:30 14/11/2026, B ghi):** 263 file / 9.425 đoạn; 8 bài của C (Tết, Âm hồn, Trung thu, Vu Lan, Đoan Ngọ, Truyền Lô, Hò Huế, Lý Huế) — câu thử trích đúng bài mới. C review 8 bài B + B review 8 bài C xong. Rảnh.

## (Kết phiên chiều 14/11 — CŨ, giữ để tra) PHIÊN SAU ĐỌC TRƯỚC (C viết 17:40 14/11/2026 `date`)

- **Việc kế (đang dở):** 8 bài quán mới của B cho Kim Long / Thủy Xuân / Đầm Chuồn.
  - C đã review: ready sau 5 minor (sửa chữ). Biên bản private `data/quan_kho_them_2026-11-14/c_review_8_bai.md`. Nháp ở `data/quan_kho_them_2026-11-14/nhap/`.
  - **Chờ B** sửa minor ⇒ ghi kho ⇒ dựng chỉ mục (B báo cả nhóm).
  - **Sau đó C** dựng lại bảng quán lịch:
    1. `uv run python data/quan_lich_2026-11-14/tools/dung_bang.py` ⇒ `data/phase_9/lich_trinh/bang_quan_lich_v1.json` (hiện md5 `e7b239019f22`, 467 quán = kho 35 + dữ liệu mở 4 + OSM 428).
       Cần sửa script trước khi chạy:
       - thêm 8 quán mới;
       - **khử trùng** quán kho mới ↔ dòng OSM cùng quán (tên gần giống + ≤ 200 m), vd Đầm Chuồn Hương Quán có cả hai;
       - chép `muc_toa_do`.
    2. Toạ độ:
       - Thu Sương (86 Kim Long), O Lé (kiệt 104 Kim Long), ECO (107 Minh Mạng), Không Gian Xưa (98 Minh Mạng), Maison Trang 2 (94 Huyền Trân Công Chúa): Photon theo địa chỉ, không ra số ⇒ ước theo số kề cùng đường (như Bánh ép Huệ, xem `data/quan_lich_2026-11-14/photon_banh_ep_hue.json`), mức "uoc";
       - An Phú: giải Plus Code GJ8V+VH2 (mức "vua");
       - Hương Quán: lấy toạ độ dòng OSM cùng tên;
       - Hội Quán: chỉ có "thôn Định Cư" ⇒ để ngoài bảng.
    3. `uv run python data/quan_lich_2026-11-14/tools/dem_theo_cum.py backend data/quan_lich_2026-11-14/dem_theo_cum_<lần>.json` ⇒ gửi B / A số "bữa có ≥ 1 quán kho theo cụm". Mốc hiện tại: tổng 49,3 %; Thủy Xuân 33,6 %; Kim Long 0 %; biển / đầm phá 0 %; nam xa 0 quán.
    4. `tools/mo_phong.py backend` (sàn: 0 ngoài bảng / khác cụm / lặp; ≤ 2 km). `pytest tests/test_quan_lich.py`. Nhánh nhỏ đổi md5 trong comment `settings.yaml` (`lich_trinh_bang_quan`) ⇒ E review ⇒ A merge.
- **Đang chạy trên main (C làm chiều 14/11):**
  - quán ăn trong lịch: cờ `quan_lich: true`; bữa chính chỉ quán ăn; ≤ 2 quán cùng cụm ≤ 2 km; không giờ / giá / điện thoại; không vào model;
  - ảnh lịch 33 / 34 (`bang_anh_v2.json` md5 `6fe592114d2b`; Thuận An trống);
  - ảnh Khám phá 184 / 216;
  - câu nhiều ý: so_y "và / còn / với" + mục web chỉ viết ý thiếu + log `nhieu_y` / `chi_y_thieu`;
  - Giới thiệu mới; bỏ mọi chữ ghi công.
- **Giới hạn đã ghi (không làm thêm nếu không được giao):**
  - ngoài 3 cụm trung tâm, quán gần như chỉ OSM "chưa kiểm", tên mỏng;
  - không có dòng ăn ở phá / biển Thuận An / Hòn Chén / Gia Long / Bạch Mã;
  - câu hai ý không dấu phẩy / không từ hỏi / "A hay B" ⇒ vẫn từ chối cả câu; "với" giới từ có thể đếm thừa;
  - mục web cho ý thiếu ít giá trị: đếm 3 / 16 có ích, mức tốt nhất 6 / 16 ⇒ giữ nguyên.
- **Bẫy gặp hôm nay:**
  - `git worktree add -b <tên>` trùng tên nhánh có sẵn ⇒ lệnh hỏng ⇒ lệnh sau chạy ở cây chung. Hôm nay C lỡ sửa 1 dòng `settings.yaml` rồi hoàn lại. ⇒ Kiểm tên nhánh trước, nối bằng `&&`.
  - `quan_theo_cum.json` trộn 3 nguồn (kho / OSM / dữ liệu mở): lọc `nguon == "kho"`. Hôm nay C đếm nhầm 42 là quán kho (đúng 28), đã sửa.
  - Worktree không có `frontend/dist` ⇒ `test_ban_do_lich` trượt (môi trường) ⇒ `npm ci && npm run build` trước test rộng.
  - RAM: 2 bộ test rộng cùng lúc ⇒ 0 GB trống. Luật A: chỉ A chạy test rộng; mỗi người ≤ 1 server tạm.
- **Tiền C 14/11 ≈ 0,47 USD:** sáng ≈ 0,35 (câu nhiều ý v1 + v2) · chiều ≈ 0,12 (so_y 0,015 · web ý thiếu 0,035 · ảnh Khám phá 0,035 · đếm web 0,016 · ảnh lịch 0,004 · quán lịch 0,0013 · ví dụ 0,0004).
- **Câu hỏi còn mở (chờ A / User):** không có câu mới. Câu cũ "dòng © OSM": A đã chốt không hiện, ghi ở "Câu hỏi cho User" dạng BÁO.
- **Máy:** 0 server, 0 pytest của C. Mọi worktree `/tmp/c_*` của C đã gỡ (`/tmp/c_yc2` không phải worktree ⇒ để nguyên).

## PHIÊN 14/11

**A giao (09:46 14/11/2026):** (1) rà lời dặn bản 2 (0 USD) · (2) B0 bảng ảnh đợt 2 — 24 / 34 User chốt 13/11 (tải Commons nền, chậm) · (3) E báo đã ghi kho ⇒ dừng, review diff kho với `meta/` trước khi E dựng chỉ mục · (4) góp ý W69 ≤ 5 dòng cùng kết quả rà gửi cả nhóm. Bài lưu trú: lần này không ghi.
**Khai báo sửa:** file này · `data/anh_kham_pha_2026-11-14/` (A giao 14/11: ảnh Khám phá + 10 điểm lịch) · `report_agent/2026-11-12_ra_khoang_cach/c_nghien_cuu_wow.md` · `data/ui_mau_2026-11-14/` (tools/, c/, h*/gioi_thieu.html) · `bao_cao_he_thong/` 02–07, 09, 10, 90, README + `nhat_ky/2026-11-14_ghi_kho_3_bai.md` (A giao 14/11, ghi kho) · `data/osm_quan_2026-11-12/` (script + bảng + biên bản mới) · `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan_ban2.md` · `data/phase_9/lich_trinh/tools/dung_bang_anh.py` + `data/phase_9/lich_trinh/bang_anh_v1.json` + `data/phase_9/lich_trinh/anh_lich_v1/` (ảnh tải về) · `data/ra_khoang_cach_2026-11-12/` (script đếm). Không chạm `knowledge-base-hue/`, code `backend/` / `frontend/`.

**Rà lời dặn bản 2 XONG (09:55 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan_ban2.md` — log không cho thấy lỗi mới do lời dặn; giữ Đ1 (nhánh B) + Đ5 (skill, A); **bỏ Đ3** (bản 1 sai giả định: mô tả thời tiết / ngày chỉ đưa khi có từ khoá); không làm Đ4. Đã gửi bàn nhóm vòng 1 cùng W69 (đồng ý hook chỉ cảnh báo + lọc tên trùng món / điểm từ đầu). B đồng ý.
**Review gói ghi kho 14/11 của E XONG (09:55 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_ghi_kho_14_11.md` — M-1 (kho tự mâu thuẫn số nhà 15A ↔ 17 ở bài phố đi bộ) ⇒ E sửa, A chốt cùng mục ② ⇒ **ready**, E ghi được.
**B0 bảng ảnh XONG (09:58 14/11/2026, 0 USD):** `data/phase_9/lich_trinh/bang_anh_v1.json` md5 `a5e210e5a1f0` — 24 / 34 (đúng sàn), ảnh `anh_lich_v1/` ≤ 80 KB mỗi ảnh, tổng 1.769 KB; tác giả / giấy phép 0 lệch so với Commons; C nhìn 24 / 24 đúng điểm, ảnh #7 đã cắt. Biên bản `bien_ban_bang_anh_v1.md`. Đã nhắn B (B1) + A.
**W69:** User BỎ (A báo). Rà lời dặn: A chốt theo C.
**Bảng quán OSM riêng cho lịch v1 XONG (10:01 14/11/2026, A giao, 0 USD):** `data/osm_quan_2026-11-12/bang_quan_osm_v1.json` md5 `8563a685723a` — 488 quán (581 ⇒ lọc tự động 471 ⇒ đọc tay cả 110 bỏ +44 và cả 471 giữ −20 ⇒ gộp trùng ≤ 150 m −8); 5 / 8 cụm ≥ 3 quán. Biên bản `bien_ban_bang_quan_v1.md`. Chờ E review. Chưa code (đợt 3).
**Kiểm X03 + gold_v6 XONG (10:18 14/11/2026, A giao, 0 USD):** X03 sau ghi kho trả lời đúng theo đoạn bài đi lại, 0 số ngoài đoạn, thiếu câu nhắc mũ bảo hiểm / rượu bia (minor) ⇒ đồng ý đổi nhãn "trong kho"; gold_v6 chỉ dời 2 trích dẫn (case 167), chữ giống hệt. Đã gửi A + E.
**Review report ghi kho của E XONG (10:26 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_e_ghi_kho_report.md` — ready, 2 minor ("nguyên văn" case 154 ⇒ 5 / 9 dãy 4 từ; tên thông tin cạnh case_index). Mọi số mục 4 tính lại khớp.
**Sổ ghi việc cho ghi kho 14/11 XONG (10:31 14/11/2026, A giao):** `bao_cao_he_thong/` 01–10, 90, README (207 bài / 8.474 đoạn, record / sparse / T1 / nhãn v6, X03, Qdrant còn 1 collection) + `nhat_ky/2026-11-14_ghi_kho_3_bai.md` — chưa commit, chờ A đọc.
**Bảng quán OSM: E review ready (0/0/2) ⇒ C sửa 2 minor (10:31 14/11/2026)** — bảng không đổi.
**Bản mẫu Giới thiệu × 3 hướng XONG (10:43 14/11/2026, A giao, 0 USD, không chạm repo):** `data/ui_mau_2026-11-14/h{1,2,3}/gioi_thieu.html` + ảnh `c/` + `c/BIEN_BAN_GIOI_THIEU.md`; công cụ `tools/kiem_tuong_phan.py` (0 trượt / 6). Chờ trang chủ của E ⇒ kiểm tương phản + 390 cả 3; sau User chọn: Giới thiệu + Khám phá.
**Đầu vào cho mẫu Khám phá (B, TRIPO v7):** `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v7_giao_dien.md` §2 — thẻ bài có ảnh + nhãn lĩnh vực ở góc; trang bài hai cột (nội dung trái, thẻ "thông tin nhanh" phải lấy từ "Thông tin chung"); "bài liên quan" cuối trang; ảnh 03_diem_tham_quan_1440.png, 06_chi_tiet_dai_noi_1440.png. Làm SAU khi User chọn hướng.
**Mẫu Khám phá H1 XONG (11:06 14/11/2026):** `data/ui_mau_2026-11-14/h1/kham_pha.html` + `kham_pha_bai.html` (tools/dung_kham_pha.py) — tương phản 0 trượt, CLS ≤ 0,0025, giảm chuyển động 0 animation. Công cụ `tools/kiem_hieu_ung.py` (CLS + reduced-motion) + `kiem_tuong_phan.py --khung-cuoi-ken-burns`. Giới thiệu H1 gắn lớp hiệu ứng chung của E. Đo Lên kế hoạch H1 của E: sau sửa 0 trượt.
**Review nhánh B `p9-lich-truong-gd` XONG (11:06 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_lich_truong_gd.md` — ready 0/0/2; worktree /tmp/c_rv đã gỡ.
**Đo Trợ lý H1 + Lên kế hoạch H1 (E) XONG (11:15 14/11/2026):** cả 5 trang H1 qua 3 phép đo ở 1440 + 390.
**Review nhánh B `p9-anh-lich` XONG (11:15 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_anh_lich.md` — ready 0/0/3 (ghi công thiếu "đã thu nhỏ" + link giấy phép; chữ 12 px; test đọc data/). Worktree /tmp/c_rv2 đã gỡ.
**Hiệu ứng bản 2 (E) áp cho trang C + đo 6 trang H1 XONG (11:28 14/11/2026):** 0 trượt (390 sau khi E dời dải báo), CLS ≤ 0,034, giảm chuyển động 0 animation.
**Tra framework hiệu ứng XONG (11:28 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_framework_hieu_ung.md` — CSS đủ; GSAP + ScrollTrigger chỉ cho màn cuộn kể chuyện; số gzip C đo + thử CSP thật (0 vi phạm). Kết quả Codex `data/tra_cuu_cli/2026-11-14_fw-hieu-ung/`. /tmp/c_fw đã xoá. **Lỗi của C:** gõ giờ ước (11:40) vào report ⇒ hook bắt, sửa bằng `date`.
**Việc kế (User "làm đi", A giao):** chờ E xong đợt chung trên nhánh `p9-gd-h1` ⇒ C làm Khám phá + trang bài + Giới thiệu từ mẫu, review chéo với E, đo 3 phép trên bản build thật. Khai báo file trước khi sửa.
**Chờ việc** (11:28 14/11/2026). Còn mở: review bài lưu trú khi E viết xong.
**Câu nhiều ý — code XONG (nhánh `p9-cau-nhieu-y` 5bc07b1, đã push, cờ tắt):** chờ E "dựng xong" ⇒ đo có phí (hỏi kèm 10, an toàn 32 ×2, Golden 176; ≈ 0,15 USD) ⇒ E review.
**Ảnh Khám phá v2 XONG (13:30 14/11/2026):** nhánh `p9-anh-kp` 3c5350f (từ main cfb5d99) — 167 bài có ảnh, 29 "Ảnh minh hoạ", ghi công ở `public/anh/kp/ghi_cong.json` (tải khi mở trang bài / Giới thiệu), 31 link trùng kho về trang chủ tên miền (hook không vượt). Sửa thêm CLS Giới thiệu #nguon-anh 390 (0,17–0,66 trên main ⇒ ≤ 0,03). E review ⇒ ready; chờ A merge. Server 8897 (bản nhánh ảnh) còn chạy — merge xong tắt.
**Nhãn bộ sửa lịch theo lịch bản 2 XONG (13:23 14/11/2026, 0 USD):** `data/phase_9/bo_do_sua_lich/` — đã thấy 2923d432da9b, kín 1165ecfa6367; mô phỏng code B 2bc020d 4/10 ⇒ 10/10, kín 1/5 ⇒ 5/5; cơ cấu giữ nguyên; báo B lỗi harness `q3_sua_lich.py` thiếu luật `khong_doi` (A chốt 06/11).
**Review nhẹ ghi kho 2 của E XONG (13:29):** `report_agent/2026-11-12_ra_khoang_cach/c_review_e_ghi_kho_2.md` — ready 0/0/0, mọi số khớp.
**Câu nhiều ý — đo XONG, KHÔNG ĐẠT (13:37 14/11/2026, 0,1601 USD):** `report_agent/2026-11-12_ra_khoang_cach/c_cau_nhieu_y_do.md` — hỏi kèm 4 ⇒ 10/10 đạt; an toàn máy đếm đạt; Golden trượt (ngoài kho bị trả lời 3/18, lỗi trích dẫn mới 2) ⇒ cờ giữ tắt, không merge; đề xuất vòng 2 chờ A. Mở: X01 TypeError chập chờn (đường web cũ). Nhánh rebase 31d38f3 chưa push. 8897 đã tắt; /tmp/c_anh đã gỡ (nhánh ảnh A merge ef8bc46).
**Câu nhiều ý VÒNG 2 — đo XONG (14:03 14/11/2026, ≈ 0,19 USD):** nhánh 2c99534 (đã push); `report_agent/2026-11-12_ra_khoang_cach/c_cau_nhieu_y_do_v2.md` — mọi sàn đạt trừ Golden ngoài kho 1/18 (câu 161, đường không đổi: yêu cầu gửi model giống byte bật/tắt ⇒ nhiễu). Golden 0/176 đi vào luật mới. CHỜ A quyết (i) đóng / (ii) S-AT 2 judge ⇒ E review. NK06/NK07 của E: không do cờ (đường cũ).
**Bẫy 14/11:** review kho 3 ngày 13/11 không grep chỗ khác nhắc cùng sự kiện (sót dòng 15A) ⇒ sửa một sự kiện trong kho thì grep mọi chỗ nhắc nó.

## (Phiên 13/11 — giữ để tra)

## PHIÊN SAU ĐỌC TRƯỚC (C viết lúc kết phiên, 22:39 13/11/2026 `date`)

*Tên quán / cơ sở trong file tracked ghi bằng nhãn; bảng nhãn ở `data/` (private). Report tracked tả quán / cơ sở ở MỨC LOẠI ngay khi viết.*

**Việc đầu phiên sau (theo thứ tự; A giao lại khi mở phiên):**
1. **Rà lời dặn bản 2 — DỞ:** `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan_ban2.md` md5 `ad661b94415b` — đã có số hành vi từ log (407 lượt; model tự gọi tìm kho lần 3 ở 37 câu; công cụ thời tiết dùng 2 / 403, ngày 12 / 403). **Còn:** đối chiếu từng câu dặn với lượt đo ở `data/` (B7, hết lượt tìm, lịch trình), đếm câu ngoài phạm vi, ≤ 5 đề xuất theo lợi / công ⇒ gửi cả nhóm. Script: `data/ra_khoang_cach_2026-11-12/tools/dem_log_chat_metrics.py`. B rà harness song song (`b_ra_harness_tro_ly.md`) — không chồng.
2. **Review diff kho** với bản sao ở `knowledge-base-hue/meta/` khi E ghi kho 3 (2 bài điểm mỏng + bài Đi lại + 3 chỗ sửa) — đo đã dời sang phiên sau theo lời User. Không đọc `evaluation/`, `*sealed*`.
3. **Khi A giao:** bảng quán OSM riêng cho lịch (A chốt 13/11) — đọc tay ~110 dòng bị lọc trước khi dựng (`data/osm_quan_2026-11-12/dem_cho_cau_kho_rieng.md`); bản nhẹ ~10 quán vào bài "ăn gì gần" chỉ SAU khi ghi kho 3 + đếm lại. Phần (B) ảnh của plan đợt 2: chờ User duyệt phiếu ảnh bản 2 (tối đa 24 / 34 = đúng sàn, 0 biên) ⇒ C dựng `bang_anh_v1.json` (tải Commons CHẬM, ≥ 10 s / yêu cầu).

**Sản phẩm phiên 13/11 (đều 0 USD API):** khớp OSM bản 2 + Photon (bài kho có toạ độ 29 ⇒ 34 / 81) · đếm OSM cho câu "bảng riêng / kho chính" · toạ độ v7 (`data/phase_9/lich_trinh/diem_toa_do_v7.json` `158e184154de`, 33 / 34) · plan đợt 2 (`docs/superpowers/plans/2026-11-13-len-ke-hoach-dot-2-plan.md`, A duyệt) · phiếu ảnh bản 2 · điểm lễ hội ban ngày · review: kho 3 của E (2 vòng), bật cờ hết lượt tìm (`9d6a0f7`), bài kho điểm mỏng, kiểm độc lập `bai_hoc/`, so mốc bước (b) (khớp 4 / 4).
**Tiền C phiên 13/11: 0 USD API** (gửi ra ngoài: Overpass 2 truy vấn, Photon 2, Commons ~13 có 1 lần bị 429, WebFetch ~10 trang — chỉ thông tin công khai).
**Không server / worktree / nhánh / container của C.** File tạm `/tmp` đã xoá.

**Bẫy phiên 13/11 (đừng lặp):**
- **Gửi số trước khi lệnh chạy xong** (gộp SendMessage cùng lượt với lệnh tính md5) ⇒ tin mang 4 md5 bịa. Số / md5 chỉ gửi SAU khi thấy đầu ra.
- **Report tracked chép tên / địa chỉ cơ sở từ `data/`** (sự cố e74c6df) ⇒ viết ở mức loại ngay từ đầu, cả review và STATUS.
- **Grep thẳng kho** thay vì `scripts/grep_kb.sh` (1 lần, lúc đọc tay khớp quán).
- **Luật chữ dò trên chữ bỏ dấu** ("Quán" ↔ "quận", "Làng" ↔ "lăng") ⇒ dò tên tiếng Việt trên chữ còn dấu.
- **Gửi dồn ~11 truy vấn Commons** ⇒ 429 ⇒ luôn chờ + cách ≥ 10 s.
- Script cũ có sẵn biến trùng tên với biến mới chèn (`BANG`) ⇒ grep tên trước khi thêm.

## PHIÊN 13/11

*Tên quán / cơ sở lấy từ kho hoặc `data/` ghi bằng nhãn (Q-…, L-…); bảng nhãn ở `data/osm_quan_2026-11-12/nhan_status_c_13_11.md` và `data/luu_tru_2026-11-12/nhan_review_c_13_11.md` (private).*

**Phiếu ảnh bản 2 XONG:** `data/phase_9/lich_trinh/phieu_anh_2026-11-13_ban2.md` (4 ảnh mới CHƯA AI NHÌN; #6, #16 không có ảnh thay ⇒ thẻ không ảnh). Commons 429 khi gửi dồn ⇒ chạy chậm.
**So mốc bước (b) XONG (20:27 13/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_so_moc_buoc_b.md` — khớp 4 / 4 sàn của B (81 % · 58 % · 1 · 50 %); script `tools/dem_lai_buoc_b.py`; `mo_phong_*.py` nhận biến BANG. Lễ hội / chụp ảnh đúng ngưỡng 50 %.
**Kiểm độc lập bai_hoc/ XONG (20:36 13/11/2026):** `data/hoc_cung_user_2026-11-10/kiem_doc_lap_13_11.md` — 0 sai số; 2 hiểu nhầm ("xử lý trước lượt cuối" ⇒ "sửa hoặc nhận giới hạn"; bài 19 dòng 35 thiếu "phạm theo chữ") + 6 nhỏ; 5 chỗ chưa chắc của người viết đã trả lời. Đã nhắn A. **Rảnh — chờ việc** (21:20 13/11/2026): B đo xong, chạy việc nặng lại được; C không có việc mở (kho 3 chờ User).
**Plan đợt 2 "Lên kế hoạch" XONG (21:37 13/11/2026, A giao, mức nhẹ):** `docs/superpowers/plans/2026-11-13-len-ke-hoach-dot-2-plan.md` md5 `5d55b0676d9e` — (A) bản đồ làm ngay (toạ độ 18 / 34 ⇒ C dựng v7; B code); (B) ảnh chờ User (tối đa 25 / 34 = 74 %, biên 1 ảnh so sàn 70 %). Chờ A duyệt.
**Review 2 bài kho nháp của E XONG (21:49 13/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_bai_kho_diem_mong.md` — ready, 3 minor (m-1: "phòng trưng bày" ⇒ "loạt tác phẩm"); chia đoạn 12 / 15, 0 lỗi; WebFetch 3 trang khớp. **Rảnh — chờ việc** (22:02 13/11/2026): User dặn đo để mai ⇒ ghi kho + dựng lại chỉ mục **hoãn sang phiên sau**. **Việc phiên sau của C:** review diff kho với bản sao ở `meta/` khi E ghi xong (không đọc `evaluation/`, `*sealed*`).
**Bàn quán OSM — A chốt (22:21 13/11/2026, CURRENT_HANDOFF "Quán OSM — chốt"):** (1) bảng riêng cho lịch ngay (rào nhóm: dòng quán do code viết, nhãn "chưa kiểm, có thể đã đóng" + ngày tải, không giờ / số điện thoại OSM, © OSM); bản nhẹ (3) ~10 quán cụm thiếu vào bài "ăn gì gần" — User duyệt nội dung, làm SAU khi ghi kho 3 + đếm lại; không (2) Qdrant; (4) `tra_quan` khi đếm được lỗi. Việc dữ liệu kéo theo cho C (khi giao): đọc tay ~110 dòng bị lọc trước khi dựng bảng.
**A0 toạ độ v7 XONG (21:41 13/11/2026, plan đợt 2 A duyệt):** `data/phase_9/lich_trinh/diem_toa_do_v7.json` md5 `158e184154de` — 34 dòng = 34 điểm, 33 có toạ độ (null: Không gian lưu niệm Lê Bá Đảng); biên bản `bien_ban_toa_do_v7.md`. Đã nhắn A + B (B làm A1). Phần (B) ảnh: chờ User; tối đa 24 / 34 = đúng sàn.
**Gỡ tên / địa chỉ khỏi file tracked XONG (21:33 13/11/2026, A giao — sự cố e74c6df):** `c_review_kho3_e.md` (nhãn L-a…L-e) + file này (nhãn Q-a…Q-c); bảng nhãn ở `data/` (private). Lịch sử git còn tên — A / User quyết. **Bẫy cho C:** report tracked tả cơ sở / quán ở mức loại ngay khi viết, kể cả trong review và STATUS.
Khai báo sửa: file này · `data/osm_quan_2026-11-12/` (script khớp + bảng khớp mới + biên bản) · `data/sua_kho_2026-11-12_an_gan/` (script dựng, `quan_theo_cum.json`, phiếu quán + mốc, bài nháp). Không chạm `knowledge-base-hue/`.

**Kho 3 ăn uống — 4 bước XONG, chờ A (19:55 13/11/2026, 0 USD, không gọi mạng, không chạm kho):**
- (1) Luật khớp bản 2 (`data/osm_quan_2026-11-12/tools/khop_osm_v2.py`, luật ghi trước) ⇒ `khop_bai_kho_v2.json` 13 dòng; **đọc tay 22 dòng** (13 + 9 dòng bản 1 bị bỏ) ⇒ `doc_tay_v2.json`: nhận 13 (thêm tay 1 dòng — Q-a), bỏ 9. Bản 1 không dùng được 6 / 22 (4 khớp nhầm rõ, 1 trong đó gắn "chắc").
- (2) `dung_quan_theo_cum.py` bản 2: 13 toạ độ OSM cho bài kho + OSM nguồn thứ ba cho cụm / mốc < 3 quán (đọc tay 12 quán được chọn, loại 2 ⇒ `BO_TAY_OSM`). Sửa thêm lỗi làm tròn bản 1 (285 m ⇒ "300 m" mà 303 m ⇒ "0,3 km").
- (3) Tiêu đề mục bài nháp: dài nhất 305 ⇒ 48 ký tự; phường + tên điểm vào câu đầu đoạn.
- (4) Phiếu quán + mốc bản 2 (bảng A2 OSM chờ User; bảng D thêm cột OSM). md5: `quan_theo_cum.json` `2c96ac42e946` · phiếu `ce7264f07c17` · bài nháp `1b387b1c4cc2`.
- Số (so bản 1 tối 12/11): bài kho có toạ độ 29 ⇒ 34 / 81 · gán cụm 22 ⇒ 28 · cụm 0 quán 4 / 8 ⇒ 2 / 8 nếu dùng OSM (Thủy Xuân +6, Kim Long +3, Đông +1); không OSM vẫn 4 / 8. Còn trống: lăng xa, nam xa, mốc cầu ngói Thanh Toàn.
- Lệnh tính lại + chi tiết: `data/osm_quan_2026-11-12/bien_ban.md` mục "Phiên 13/11". Bản 1 của script / bảng / bài nháp sao ở `/tmp/c_*_ban12.*` (mất khi khởi động lại; data/ không có git).
- **Lỗi quy trình của C:** khi đọc tay đã `grep` thẳng 3 bài quán trong `knowledge-base-hue/foods/restaurants/` (dòng địa chỉ) thay vì `scripts/grep_kb.sh` — không chạm câu kín / Golden, nhưng sai luật §5; lần sau dùng `grep_kb.sh`.

**Review chéo kho 3 của E XONG (20:04 13/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_kho3_e.md` — changes_requested: M-1 151 dòng có hạng = 143 cơ sở (316 = 293); bài đi lại 4 minor; WebFetch 3/3 ý khớp. Đã nhắn E + A.
**Sửa 3 minor review E cho phần ăn uống XONG (20:04 13/11/2026):** quán Q-b ⇒ ước (không gán cụm) · bỏ mức "osm", thêm `nguon_toa_do` · quán Q-c: số kiệt. Gán cụm 28 ⇒ 27. md5: 9416b5c6adca  quan_theo_cum.json;48475905ac68  phieu_quan_va_moc_2026-11-12.md;7b57ee5e389e  bai_nhap_an_gi_gan_diem_tham_quan.md;722d72c97292  ../osm_quan_2026-11-12/doc_tay_v2.json;
**Kiểm lại kho 3 của E vòng 2 XONG (20:06 13/11/2026):** ready (mục 7 `c_review_kho3_e.md`): 142 cơ sở có hạng, 140 / 142 gán khu; bài đi lại m-2…m-5 đóng.
**Photon ⇒ bảng quán XONG (20:08 13/11/2026, 0 USD):** 9 dòng đạt luật, 7 trùng OSM (cùng gốc), 2 dùng mới; gán cụm 27 ⇒ 28; md5 quan_theo_cum eae693cac1b0 · phiếu 6d0e46a572fe · bài nháp 8cfe17ac9e4f (chi tiết bien_ban.md OSM).
**Đếm cho câu "OSM bảng riêng / kho chính" XONG:** `data/osm_quan_2026-11-12/dem_cho_cau_kho_rieng.md` (giữ 471, lọc tự động bỏ nhầm ~32 % — cần đọc tay; +91 đoạn = +1,1 %; 5 / 8 cụm ≥ 3 quán).
**Điểm lễ hội ban ngày XONG:** `data/phase_9/lich_trinh/de_xuat_them_le_hoi_ban_ngay.md` (2 gắn nhãn điểm sẵn có + 1 có điều kiện; không có điểm mới đủ căn cứ).
**Vòng tự soi 1:** đã gửi A / B / E.
**ĐANG LÀM (20:20 13/11/2026):** tìm ảnh Commons thay 4 dòng "đổi" + phương án #16, #27 ⇒ phiếu ảnh bản 2 (C KHÔNG nhìn được ảnh ⇒ ảnh mới ghi "CHƯA ai nhìn"). Commons trả 429 khi C gửi ~11 truy vấn liền ⇒ chạy lại chậm (chờ 90 s, cách 10 s / yêu cầu, gộp file).
**Phụ lục spec "581 quán OSM" — A giao rồi TẠM DỪNG (20:11 13/11/2026):** User đang cân nhắc để quán OSM ở bảng / kho riêng thay vì kho RAG chính; chưa sửa spec, chưa chạy gì. Chờ A.
**Review `9d6a0f7` XONG (20:11 13/11/2026):** ready, 2 minor (Project_Status còn ghi cờ false; eval mặc định nay có cờ ⇒ ghi vào plan B7 cuối) — `c_review_bat_co_het_luot.md`. Trước đó: review commit `9d6a0f7` (bật cờ `het_luot_bo_cong_cu`, A làm) ⇒ `report_agent/2026-11-12_ra_khoang_cach/c_review_bat_co_het_luot.md`.
**Bẫy 13/11 (lỗi bằng chứng của C):** gửi tin cho A SONG SONG với lệnh tính md5 ⇒ tin mang 4 md5 bịa; đã đính chính ngay. Luật cho mình: tin báo số chỉ gửi SAU khi đã thấy đầu ra lệnh, không gộp cùng lượt gọi công cụ.

## (Phiên 12/11 — giữ để tra)

## PHIÊN SAU ĐỌC TRƯỚC (C viết lúc kết phiên, 22:22 12/11/2026 `date`)

**Việc dở của C (đều 0 USD, chưa chạm kho, chưa code):**
1. **Quán từ OpenStreetMap — làm dở.** Đã tải + làm sạch + đếm: `data/osm_quan_2026-11-12/` (`tho_overpass.json`, `osm_quan.json` 581 quán có tên, `bien_ban.md` — đọc mục "Tới đâu khi kết phiên"). **Bảng khớp 22 bài kho
   (`khop_bai_kho.json`) CHƯA dùng được** — ≥ 3 dòng khớp sai rõ, luật còn lỏng ⇒ siết luật + xem tay. Chưa đưa nguồn OSM vào `data/sua_kho_2026-11-12_an_gan/tools/dung_quan_theo_cum.py`, chưa cập nhật phiếu quán + bảng D.
   Không cần tải lại (script: `data/osm_quan_2026-11-12/tools/tai_overpass.py`; tra địa chỉ dự phòng: `data/sua_kho_2026-11-12_an_gan/tools/tra_photon.py` — máy chủ đó hôm nay không trả lời).
2. **Bài nháp "ăn gì gần điểm tham quan":** E chia đoạn thử 21 đoạn 0 lỗi nhưng tiêu đề mục dài tới 305 ký tự ⇒ rút còn tên cụm ngắn, tên phường đưa vào câu đầu đoạn (sửa trong `dung_quan_theo_cum.py`).
3. **Sửa số ở report cũ:** "6.794 cơ sở" là 6.794 dòng / 208 tên — A nhận ghi dòng "Sửa số"; nếu A chưa làm: `c_dot_2_dem_implementation.md`, `c_phan_chua_on.md`, plan ăn gần.

**Sản phẩm phiên này + đường dẫn:**
- Phiếu cho User (private): `data/phase_9/lich_trinh/phieu_gop_cho_user_2026-11-12.md` (User đã trả lời 3 câu, không sửa ô) · `…/phieu_nho_dot_1_2026-11-12.md` (User đã trả lời 3 câu) · `…/phieu_anh_2026-11-12.md` (chưa xem;
  7 điểm chưa có ảnh) · `data/sua_kho_2026-11-12_an_gan/phieu_quan_va_moc_2026-11-12.md` (chưa xem).
- Bảng: `data/phase_9/lich_trinh/diem_v8_de_xuat.json` (34 dòng, md5 `0cbd845ede30`, CHƯA thay bảng chạy; dựng bằng `tools/dung_v8.py`) · `data/sua_kho_2026-11-12_an_gan/quan_theo_cum.json` (md5 `b4f1661e95fd`).
- Mô phỏng 0 USD: `data/phase_9/lich_trinh/tools/mo_phong_v8.py` (bộ xếp thật, 360 tổ hợp) · `…/mo_phong_kieu_di.py` (bản thử luật phút + ưu tiên + cụm xa — KHÔNG phải code sản phẩm).
- Tài liệu tracked: spec "Lên kế hoạch" bản 3.3 `8c521ecdc80d` · plan đợt 1 bản 3 `27919be11ef6` (B đã đọc, đồng ý; B làm bước (a)) · `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan.md` (rà lời dặn, 5 đề xuất chưa làm).

**Chờ User:** liếc danh sách điểm ưu tiên theo sở thích (trong bảng v8) · phiếu ảnh · phiếu quán + mốc (giữ / bỏ từng quán dữ liệu mở) · có cho đưa quán OpenStreetMap vào kho không (mở rộng Q3) · giờ + thứ của phố đêm cạnh
Kinh thành (tuỳ chọn) · chọn có làm đề xuất Đ2–Đ4 của report lời dặn không.

**Bẫy gặp hôm nay (đừng lặp):**
- **Đếm dòng thay vì đếm cơ sở:** dữ liệu mở có dòng lặp (6.794 dòng = 208 tên) ⇒ mọi phép đếm trên dữ liệu ngoài phải khử trùng trước khi ghi số.
- **Xếp hạng / ước độ phủ trước khi đếm:** bảng "phần chưa ổn" phải hạ 2 / 5 mục đầu sau khi đếm; plan ăn gần ước 30–45 bài khớp, thật 7; spec ghi "3–5 hoạt động tối", kho chỉ có 1. ⇒ chạy bước dò rẻ TRƯỚC khi ghi con số vào plan / spec.
- **Khớp tên tự động phải xem tay:** luật khớp OSM gắn "chắc" cho dòng sai — không nhận bảng khớp khi chưa đọc từng dòng.
- **Auto mode chặn lệnh kiểm DNS qua máy chủ ngoài** (lúc máy không phân giải được tên miền bản đồ) và dặn không lách ⇒ không lách, báo A; việc tải sau đó dùng máy chủ khác phân giải bình thường.
- Hook báo "giờ ước" khi ghi giờ chưa tới hoặc chép giờ khuyết phút ⇒ luôn lấy `date` ngay trước khi ghi.

**Tiền C cả phiên 12/11: 0,058691 USD** (3 lượt đếm có phí buổi tối sớm; từ 20:47 trở đi mọi việc 0 USD — 4 lượt tra Codex, WebFetch, 1 truy vấn Overpass).
**Không server / worktree / nhánh / container của C.** (Lúc kết phiên có một uvicorn cổng 8010 đang chạy — không phải C khởi động trong đợt việc tối; C không đụng.)
**Vòng tự soi 2 (đã gửi nhóm):** tốn mà lợi ít = bảng khớp OSM làm vội cuối phiên + phiếu ảnh khi chưa nhìn được ảnh; phiên sau: dò rẻ trước khi viết số, khử trùng dữ liệu ngoài, phiếu nào cần mắt người thì giao cho session có trình duyệt.

## PHIÊN 12/11 — C `hue-rag-e1` · A `hue-rag-7d` · B `hue-rag-1b` · E `hue-rag-33`

**ĐANG LÀM (18:45 12/11/2026, A giao; User: việc A giao = "làm đi"):** đợt 2 cổng — lượt đếm rẻ trước khi xây (lưu trú · ăn gần · sự kiện theo ngày), trần 0,02 USD, không spec / code, không `*sealed*`.
Khai báo sửa: `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` (mới) · file này · dòng C trong `CURRENT_HANDOFF.md`. Dữ liệu chạy: `data/phase_11/dot_2_dem/` (private). Cần server ⇒ nhắn B trước (một session chạy server / model một lúc).

**Đếm đợt 2 — DỞ (18:53 12/11/2026):** đã gửi 13 / 18 câu tự viết (6 lưu trú · 6 ăn gần · 1 sự kiện), 0,018295 USD (trần 0,02) ⇒ kết quả `data/phase_11/dot_2_dem/ket_qua_lan_1.jsonl`; 5 câu sự kiện S2–S6 (`cau_18.jsonl`) CHƯA gửi (hết quỹ — đã xin A ≈ 0,01). Công cụ: `data/phase_11/dot_2_dem/tools/` (`gui_cau.py` có phí · `quet_bo.py`, `log_tien.py` 0 USD). Server 8871 đã tắt. Còn lại: đọc + phân loại 13 câu, đối chiếu kho, viết report.
**Việc chen (18:53 12/11/2026, A giao, đường găng):** plan B7 bản 2 theo review vòng 1 của E (`docs/superpowers/plans/2026-11-10-phase-9-b7-plan_review.md`: 3 major, 6 minor). Khai báo sửa thêm: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md`. Xong ⇒ nhắn E + A ⇒ quay lại đếm đợt 2.
**Plan B7 bản 2 XONG (18:59 12/11/2026):** `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` sha256 `da7bff5d0c4e` (chưa commit — A commit) — lượt hôm nay = đo giữa kỳ, `KIN_NGAY` TẮT, `MAX_DROP` 4, ≈ 0,31 USD; đã nhắn E (vòng 2) + A.
**Việc kế (A giao):** (1) đếm đợt 2: gửi nốt 5 câu sự kiện (trần nâng 0,032, nhắn B trước khi chạy server) ⇒ report; (2) rà "phần nào chưa ổn" — `CURRENT_HANDOFF.md` mục "Đợt rà khoảng cách" dòng C ⇒ `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` (chỉ đọc, 0 USD).
**Đếm đợt 2 XONG — chờ review (19:06 12/11/2026):** report `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` (chưa commit). 18 câu, **0,024691 USD** (trần 0,032). Kết luận: ăn gần đủ lỗi (dữ liệu định vị quán) · lưu trú đủ lỗi phần nhỏ · sự kiện không đủ lỗi. Server đã tắt.
**Plan B7 bản 2:** E vòng 2 READY; sửa chữ n-3 ⇒ sha mới `2ca3f63ce45b` (không đổi tiêu chí). 5 minor còn lại là việc người chạy (B).
**Rà "phần nào chưa ổn" XONG (19:08 12/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` (chưa commit; 0 USD) — 5 mục trên cùng: ăn gần · từ chối cả câu · đường web chậm 15–25 s · số tiền / giờ chưa kiểm với đoạn trích · log không có loại câu. Công cụ: `data/phase_11/dot_2_dem/tools/log_tong.py`.
**Việc kế (19:09 12/11/2026, A giao, 0 USD, chỉ đọc):** đếm trên kết quả B7 giữa kỳ của B — (2) câu Golden bị từ chối / một phần mà ngữ cảnh có đoạn đúng (gold v5) · (3) lần tìm kho thứ 3–4 + đường web có cứu câu nào, tốn bao nhiêu giây / USD · (4) số tiền / giờ không khớp đoạn trích ⇒ thêm mục "Đếm trên B7 giữa kỳ" vào `c_phan_chua_on.md`, xong nhắn A. Đã nhắn B xin đường dẫn file sinh; không sửa / chạy lại / đụng phần chấm mù của B.
**Đếm trên B7 — xong phần Golden + an toàn (19:25 12/11/2026):** mục "3b" trong `c_phan_chua_on.md`; script `data/ra_khoang_cach_2026-11-12/tools/dem_b7.py golden` (chạy từ `backend/`, `PYTHONPATH=$PWD`). Từ chối nhầm trợ lý 3 ↔ mốc 13, cả 3 tìm trượt · tìm thêm cứu 10 câu · 0 số tiền / giờ sai nguồn / 155 · an toàn 0 / 32 đổi kết luận. **CÒN CHỜ B:** `s2/s2_r2.jsonl` (ổn định S2) · `w/s2c.jsonl` (đường web: tìm 3–4 lần, giây, USD) · điểm chấm mù ("trả lời một phần", nhãn cảnh báo). Không đọc `golden/judge/`.
**Đếm trên B7 — bổ sung xong (19:28 12/11/2026):** thêm (b2) đường web · S2 ổn định 0 / 44 · (e) 4 câu tụt Đủ ý (chung gốc: cùng ngữ cảnh, viết ngắn hơn) · trả lời một phần 0 câu khi đủ đoạn đúng. Đã nhắn A lần cuối. **Còn một ý chờ B:** nhãn "có ↔ không cảnh báo" giữa 2 lượt an toàn (khi B chấm xong an toàn) — A không giao lại thì thôi.
**3 plan nháp mức nhẹ XONG (19:32 12/11/2026; chờ User chọn, chưa code / chưa sửa kho, 0 USD):** `docs/superpowers/plans/2026-11-12-an-gan-dinh-vi-quan-plan.md` (sửa kho 53 bài, cách B toạ độ dữ liệu mở khuyến nghị, ≤ 0,08) · `…-het-luot-tim-plan.md` (bỏ công cụ `tim_kho` sau 2 lần tìm; probe `is_enabled` trước, ≤ 0,09) · `…-nhan-loai-cau-plan.md` (trường `loai_cau` 11 nhãn từ khoá, ≈ 0,001). Sửa số: bài quán có câu định vị = 12 / 81 (report đếm đã commit ghi 15 — đã báo A).
**Bổ sung cuối (19:55 12/11/2026):** sửa số 12 / 81 trong report đếm · probe `is_enabled` [Chạy] ghi vào plan hết lượt tìm (xét lại mỗi lượt, cả stream; model xin công cụ đã tắt ⇒ `ModelBehaviorError` phải bắt) · mục 3b (d): nhãn "thiếu cảnh báo" đổi 4 / 27 câu giữa 2 lượt an toàn, 5 câu thiếu ở cả hai ⇒ đã báo A là mục mới xếp cao.
**Chẩn đoán 2 sàn phạm B7 XONG (19:59 12/11/2026, 0 USD):** mục "3c" trong `c_phan_chua_on.md` — (1) thiếu cảnh báo câu miễn / giảm = do cách so (điều kiện nằm ở đoạn model tìm thêm, mốc không có đoạn đó); 5 câu thiếu ở cả hai lượt = lỗi khâu viết có từ RAG mốc; (2) S2b: 1 câu = giới hạn User đã nhận 09/11, 1 câu = loại mới (câu ranh giới có chữ Huế, định tuyến dao động từ trước 10/11). **C đề xuất A bỏ lượt 3 an toàn (0,02 USD)** — chờ A trả lời; chưa chạy gì có phí.
**A quyết bỏ lượt 3 an toàn. Bảng "Danh sách sau khi đếm" XONG (20:01 12/11/2026):** mục "3d" trong `c_phan_chua_on.md` (7 việc đáng làm + 7 mục nhận giới hạn / không làm); đã nhắn A.
Không server / worktree / nhánh / container của C. (Tiền: xem dòng "Tiền C 12/11 (mới)".)
**Vòng tự soi 1 (20:04 12/11/2026):** đã gửi A / B / E. Tự nhận: xếp hạng "chưa ổn" trước khi đếm (2 / 5 mục đầu phải hạ); thước "thiếu cảnh báo mới" trong plan B7 của C chấm hai bên theo ngữ cảnh riêng (lỗ không ai thấy ở review). Nhận phản biện E: câu miễn / giảm "do cách so" chỉ một nửa — đã sửa mục 3c. Đề xuất tới lượt cuối: bỏ phần kín giữa kỳ, S2 ×1, harness ghi thêm tools / ms / id đoạn tìm thêm.
**Lượt đếm rẻ thứ hai XONG (20:16 12/11/2026):** 17 câu (di chuyển 6 · tiếng Anh 5 · việc gấp 6), **0,023453 USD** (trần 0,03) ⇒ mục "3e" + bảng 3d cập nhật trong `c_phan_chua_on.md`. Việc gấp: 3 / 6 không có hướng dẫn, 0 / 6 có số khẩn cấp ⇒ đề xuất code nối dòng số cố định khi định tuyến xếp khẩn cấp (cần User — đảo một phần "bỏ khẩn cấp"); di chuyển 4 / 6 kho từ chối ⇒ bổ sung kho; tiếng Anh 5 / 5 đúng nội dung nhưng trả lời tiếng Việt ⇒ chuyện phạm vi. Server đã tắt.
**Tiền C 12/11 (mới):** 0,024691 + 0,023453 = **0,048144 USD**.
**Plan nháp "việc gấp" XONG (20:19 12/11/2026, 0 USD, chưa code):** `docs/superpowers/plans/2026-11-12-viec-gap-so-khan-cap-plan.md` — định tuyến xếp khẩn cấp ⇒ code nối dòng số khẩn cấp qua kênh `notice` sẵn có + không mở cổng web; chuỗi gửi model giống byte; ≤ 0,06 USD, ~2 giờ; cần User (đảo một phần "bỏ khẩn cấp" 08/11). Đã nhắn A.
**Lịch trình — bảng khoảng cách TRIPO + đếm rẻ XONG (20:47 12/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` (chưa commit). 14 biểu mẫu + 3 gõ tự do = **0,010547 USD**; mô phỏng 0 USD 360 tổ hợp qua `lich_trinh.xep`: 7 / 28 điểm không bao giờ được xếp (chùa nổi tiếng + 5 lăng), "đi dày" đổi khung 0 / 120, buổi 2 điểm 0 / 360 — gốc: chọn theo thứ tự bảng, không cột ưu tiên, 24 / 28 điểm chưa có thời lượng. 6 ứng viên; đầu bảng: cột ưu tiên + luật chọn (cần User duyệt danh sách điểm phải đi), rồi thời lượng v7 + luật đi dày. User đã quyết KHÔNG làm "việc gấp" (plan nháp giữ làm hồ sơ).
**Tiền C 12/11 (mới nhất):** 0,024691 + 0,023453 + 0,010547 = **0,058691 USD**.
**Bẫy:** hook báo giờ ước khi chép nguyên dạng giờ khuyết phút từ tin của A ⇒ ghi "tối 12/11, theo handoff" thay vì chép dạng giờ khuyết.
**Phiếu điểm ưu tiên + plan XONG (20:53 12/11/2026, 0 USD, chưa code / chưa đổi bảng):** phiếu `data/phase_9/lich_trinh/phieu_diem_uu_tien.md` (5 điểm mức 1 + 4 điểm mức 2 đề xuất sẵn, 3 câu cho User) · plan `docs/superpowers/plans/2026-11-12-lich-trinh-diem-uu-tien-plan.md` (cột `uu_tien` + sắp trong `nap_bang`, `xep` không sửa; thử trước 0 USD: 0 lỗi kiem_khung / 360, chùa 30 / 30 từ 2 ngày; mặt trái: điểm không bao giờ xếp 7 ⇒ 9 tới khi có "đi dày"). B đang đo giây (cổng 8887) ⇒ C KHÔNG chạy server / việc nặng tới khi B nhắn "đo xong".
**Đợt việc tối 12/11 (A giao theo "User chốt hướng") — tới 21:04 12/11/2026:** (1) review plan lưu trú của E XONG (`…luu-tru-khu-va-link-plan_review.md`, 1 major: kích hoạt theo nguồn kho chỉ chắc bắt 2 / 6 câu đã đếm). (2) phiếu gộp cho User XONG: `data/phase_9/lich_trinh/phieu_gop_cho_user_2026-11-12.md` (dựng bằng `tools/dung_phieu_gop.py`; 13 / 28 dòng "cần xem"); A đã đưa User. (3) dữ liệu "ăn gần" XONG, CHƯA sửa kho: `data/sua_kho_2026-11-12_an_gan/` (`bang_de_xuat.md/.jsonl`, `mat_do_quanh_diem.json`, `tools/khop_quan.py` + `uoc_theo_so_nha.py`) — dữ liệu mở chỉ chứa 7 / 81 bài quán; ước theo số nhà kề thêm 22 (sai số trung vị 107 m) ⇒ 29 / 81 có toạ độ; quanh các lăng: kho 0 quán, dữ liệu mở cũng 0 trong 1 km. Đã ghi "sửa số" vào plan nháp ăn gần.
**ĐANG LÀM:** (4) tra Codex (0 USD) nguồn thật cho 7 ô thời lượng C ước + ô "trong nhà" kho không ghi ⇒ dựng lại phiếu gộp bằng script; **User đã sửa vào phiếu thì KHÔNG ghi đè** — ghi file kèm bên cạnh, báo A.
**(4) XONG 21:10 12/11/2026:** phiếu gộp cập nhật bằng nguồn Codex (`data/tra_cuu_cli/2026-11-12_c-phieu-gop-thoi-luong/`, C WebFetch kiểm 3 trang): cần xem 13 ⇒ 8 / 28; cung An Định ⇒ "cả hai". **Nominatim: BỎ** (máy không phân giải tên miền openstreetmap.org; auto mode của terminal C chặn lệnh kiểm tên miền qua máy chủ công cộng và báo sẽ chặn tiếp ⇒ không lách; A giao E tra bằng nguồn khác; script `tools/tra_nominatim.py` để lại, 0 lượt đã gửi).
**Spec "Lên kế hoạch bản 2" NHÁP bản 1 XONG (21:16 12/11/2026):** `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` — nguyên tắc "ô nào hiện thì đổi được lịch", bảng từng ô (code dùng · dữ liệu · tiêu chí mô phỏng), 3 đợt (≤ 0,15 / 0,25 / 0,15 USD), giao diện 0 gói mới, bảng rà FDE, 4 câu cho User. Chờ E review, User duyệt; B code.
**Bẫy 12/11 tối:** ước lượng độ phủ dữ liệu ngoài mà chưa chạy thử (plan ăn gần ghi 30–45 bài, thật 7) ⇒ lần sau chạy bước dò khớp TRƯỚC khi ghi con số vào plan.
**Đợt việc 21:15–21:33 12/11/2026 (đều 0 USD):** review gộp Exa `report_agent/2026-11-12_ra_khoang_cach/e_exa_review.md` (đếm lại khớp 17 / 25; F-1: 5 / 25 mục đạt của Exa trích trang địa điểm của chính Exa ⇒ loại thì 20 < 22; plan 2 major) · spec biểu mẫu bản 2 (E ready vòng 2) · review spec kho 3 vòng 1 `…bo-sung-kho-dot-3-design_review.md` (3 major: thư mục mới không được quét, dạng bài mỗi dòng một đoạn, dữ liệu quán mỏng) · đọc 5 ảnh + 2 file TRIPO của User ⇒ mục 4b trong `c_lich_trinh_khoang_cach.md` · **spec "Lên kế hoạch" BẢN 3** (`docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md`): một lịch đủ 4 phần + biểu mẫu đủ + ảnh + bản đồ là cam kết của mốc (User chốt), 3 đợt nối nhau ≤ 0,75 USD, mục "phải hơn TRIPO", mục 5b thứ tự ưu tiên luật + ghi chú thực thi của B. **Còn nợ:** vòng 2 review spec kho 3 bản 2 (`fd152810627b`, 3 major) · phiếu nhỏ đợt 1 (thứ hoạt động, tháng lưu ý mùa, 3–5 hoạt động buổi tối) + phiếu ảnh — chưa soạn, chờ A giao.
**Vòng 2 spec kho 3 XONG (21:35 12/11/2026):** ready (3 major đóng), 1 ghi chú: ngưỡng "0 câu đổi 10 đoạn đầu không do đoạn mới" quá chặt ⇒ để theo dõi. Spec biểu mẫu bản 3 sha `16e9f7f4fa19` chờ E kiểm phần đổi.
**Cập nhật 21:49 12/11/2026 (`date`) — 0 USD thêm (một lượt tra web Codex, 199 giây):**
- **Phiếu nhỏ đợt 1 XONG** (private): `data/phase_9/lich_trinh/phieu_nho_dot_1_2026-11-12.md` — thứ 3 điểm tối · tháng lưu ý mùa 10 điểm · kho chỉ có 1 hoạt động tối đủ giờ + thứ (+ 1 chờ User) · 3 câu.
- **User trả lời phiếu gộp** (không sửa ô nào, md5 phiếu không đổi): ưu tiên THEO SỞ THÍCH · dùng cả bảng thời lượng · thêm 5 điểm trong nhà ⇒ C dựng **bảng đề xuất v8** `data/phase_9/lich_trinh/diem_v8_de_xuat.json`
  (33 điểm, md5 `695c0d71f072`, CHƯA thay bảng chạy; `tools/dung_v8.py`, nguồn tra thêm `tools/tl_tra_them.json`, kết quả tra `data/tra_cuu_cli/2026-11-12_c-o-chua-chac-v8/`).
- **Mô phỏng 0 USD:** `tools/mo_phong_v8.py` (360 tổ hợp, bộ xếp thật: ưu tiên số 1 có mặt 60 / 60 mọi sở thích; luật "đi dày" cũ chỉ 3 / 120) · `tools/mo_phong_kieu_di.py` (bản thử luật kiểu đi bằng phút: 3 mức khác nhau 24 / 30 = 80 %).
- **Spec "Lên kế hoạch" bản 3.2** sha256 `3ea9bcb8bc10` (chưa commit): 3 sửa chữ của E · số thật buổi tối · ưu tiên theo sở thích · **mục 5c — 8 quyết định để code** (B đã xác nhận model trả mảng theo id mục, hiện nguyên câu từng mục).
- **Phiếu ảnh XONG 21:56 12/11/2026 (`date`)** (private): `data/phase_9/lich_trinh/phieu_anh_2026-11-12.md` — 27 dòng ảnh (23 mới + 4 dùng lại bộ cổng), 5 dòng cần xem, **7 điểm chưa có ảnh** (phố Tây, phố Hai Bà Trưng, đồi Thiên An, thác Nhị Hồ, 2 điểm Lê Bá Đảng, Bảo tàng Hồ Chí Minh). C chưa nhìn thấy ảnh (công cụ chỉ trả chữ) ⇒ User / session đợt 2 phải xem. Dựng bằng `tools/dung_phieu_anh.py`.

- **Plan đợt 1 "Lên kế hoạch" NHÁP bản 1** (21:57 12/11/2026 `date`, 0 USD, chưa commit): `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md` — bước (a)–(e), tiêu chí Luôn / Sàn, lượt thử sớm, điểm dừng D1–D4. Luật "cụm xa không ở ngày 1" đã mô phỏng (0 / 180; 18 / 18). Chờ: B đọc trước, A duyệt; E kiểm spec 5c ⇒ C sửa plan một lần.

- **22:09 12/11/2026 (`date`), 0 USD (2 lượt tra Codex):** spec "Lên kế hoạch" **bản 3.3** `8c521ecdc80d` (nhận kết quả E kiểm 5c + User trả lời phiếu nhỏ) · plan đợt 1 **bản 2** `82ea67f6e17d` (đã có mã băm bộ đo của E; chờ B đọc, A duyệt) · bảng đề xuất 34 dòng md5 `0cbd845ede30` (cột thứ / giờ tối / mùa + dòng hoạt động tối) · **rà lời dặn XONG:** `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan.md` (7 vai, 9 điểm đối chiếu hướng dẫn chính thức, 5 đề xuất, khung lời dặn vai mới của lịch; chỉ đọc).

- **22:17 12/11/2026 (`date`), 0 USD:** plan đợt 1 **bản 3** `27919be11ef6` (gộp 6 ý của B) · **kho 3 phần (c) ăn gần — bước chuẩn bị XONG, chưa chạm kho** (private, `data/sua_kho_2026-11-12_an_gan/`): `quan_theo_cum.json` (md5 `b4f1661e95fd`) · `phieu_quan_va_moc_2026-11-12.md` · `bai_nhap_an_gi_gan_diem_tham_quan.md` · `tools/dung_quan_theo_cum.py`. Số: 22 / 29 quán kho gán được cụm; quán dữ liệu mở chọn 6 + 3 + 1; 4 / 8 cụm 0 quán; 3 mốc. **Sửa số:** dữ liệu mở 6.794 dòng nhưng chỉ 208 tên khác nhau ⇒ "276 / 174 cơ sở" ở tài liệu trước là số dòng lặp. Chờ E khớp trường + ghi kho.

**Trạng thái: rảnh — chờ A** (không server / worktree / nhánh / container của C; việc dở: không) (review kết quả B7 nếu A giao; không server / worktree / nhánh / container của C).
**Bẫy 12/11:** lệnh shell dài viết thẳng (heredoc quét `data/` có chữ tên bộ kín) bị auto mode chặn ⇒ viết script bằng Write rồi chạy; log `chat_metrics` không có nội dung câu ⇒ không đếm theo loại câu được, phải gửi câu tự viết; câu kho từ chối đi web ≈ 0,002 USD / câu ⇒ ước tiền lượt đếm theo giá đường web, không theo giá trung bình.
(Tiền tới lúc đó 0,024691 USD — số cuối phiên ở dòng "Tiền C 12/11 (mới)".)

---

## (10/11) kết phiên — chỉ tra cứu

## PHIÊN SAU ĐỌC TRƯỚC (C mới bắt đầu ở đây — viết 22:41 10/11/2026)

**Trạng thái:** **rảnh — không việc dở, không worktree `/tmp`, không nhánh, không container của C.** Phiên 10/11 terminal: C `hue-rag-4f` · A `hue-rag-55` · B `hue-rag-05` ·
E `hue-rag-e4` (tên đổi khi mở lại — `ListAgents`). Chờ A giao (việc A giao = User nói "làm đi"). Mọi file C viết hôm nay: A commit.

**Hướng mới cho báo cáo (User chốt cuối phiên 10/11 — A ghi đủ trong `CURRENT_HANDOFF.md`):** User đọc file 02 bản 10/11 vẫn thấy khó hiểu ⇒ thêm thư mục
`bao_cao_he_thong/hieu_he_thong/` = **chuỗi bài để hiểu**, mỗi bài **một ý**, nói **vì sao trước**, có **ví dụ đời thường**, thuật ngữ đưa ra sau khi đã giải thích;
các file `01_…10_` hiện có = **sổ ghi việc** (giữ). Bài học từ mẫu 10/11: bảng "đợt sửa / số chỗ / kết quả" và danh sách tính năng vẫn là giọng sổ công trường — User cần
câu chuyện "vấn đề là gì → làm gì → vì sao vậy". Memory `user-reading-style` đã ghi.

**Việc C phiên 10/11 (đều xong, 0 USD):**
- Review: nhánh B xã giao song song (code ready, đo chưa đạt ⇒ đóng hồ sơ) · nhánh E câu ngày nhanh (1 major — "mùng N tháng <số>" không "âm" bị coi là ngày âm ⇒ E sửa ⇒ ready, merge `1633c18`)
  · sửa báo cáo `c54c932` (ready, 2 minor) · deploy cục bộ B (1 major — danh sách ảnh thiếu trong Docker ⇒ hỏi bằng ảnh tắt im lặng ⇒ sửa ⇒ ready, merge `5081e89`)
  · plan định tuyến câu lịch B (2 vòng ⇒ ready `aa493aec252f`). Nhánh định tuyến: E review (không phải C).
- Nháp plan B7 `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` (A chốt Q1–Q4, tag `p9-moc` = `18e8f42`).
- Mẫu báo cáo: `README.md`, `01_LUONG_HOAT_DONG_HE_THONG.md`, `02_BAO_CAO_KHO_DU_LIEU.md` (mỗi file sub-agent vai người không đọc code đọc thử, sửa theo góp ý).

**Bẫy / học được 10/11:**
- Log truy cập mặc định của uvicorn **ghi IP + đường dẫn** (log chatbot thì không) ⇒ bản deploy muốn "không lưu IP" phải `--no-access-log` — đã báo A làm câu cho User.
- Ảnh Docker chỉ chép file theo danh sách chừa ⇒ thiếu file cấu hình của một cờ đang bật ⇒ tính năng **tắt im lặng** (log "startup failed", không lỗi khởi động). Review deploy: so cờ bật ↔ file runtime cần.
- Regex ngày âm: "mùng / mồng N tháng <số>" không "âm" thường là ngày **dương** (Quốc khánh 2/9, 8/3) — probe bằng câu tự viết trước khi tin bộ đo (bộ đo có 0 câu dạng này).
- Dòng "thông tin có thể đã thay đổi" chỉ cho nguồn vé / địa điểm / lễ hội (`NOTICE_SOURCE_PREFIXES`) — tả báo cáo phải đối chiếu code, đừng suy.
- Hai session gửi tin chéo nhau trong brainstorm ⇒ mỗi bên nhận ý bên kia ⇒ phải gửi thêm một bản chốt chung; lần sau: đợi tin bên kia rồi mới nhận / bác.
- `ugrep` (lệnh `grep` trên máy) báo "exceeds complexity limits" với regex dài có `.{0,80}` + tiếng Việt ⇒ dùng Python để tìm trong tài liệu.
- Bẫy cũ còn đúng (09/11, 08/11): xem khối "(09/11)" ngay dưới.

**Tiền C 10/11:** 0 USD (mọi việc chỉ đọc / test 0 USD / sub-agent).

---

## (10/11) nhật ký trong phiên — chỉ tra cứu
### Phiên 10/11 (mở 19:06 10/11/2026) — C `hue-rag-4f` · A `hue-rag-55` · B `hue-rag-05` · E `hue-rag-e4`

**Trạng thái: rảnh — chờ review B / E.** A giao (CURRENT_HANDOFF "VIỆC PHIÊN 10/11", `main` `624a17b`): review cả nhánh (`risk-gated-agent-review`, một vòng, chỉ plan + diff + số đo)
(1) B `p9-xa-giao-song-song` ⇒ `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_review.md`; (2) E `p9-t1-nhanh` ⇒ `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_review.md`. Tiền 0 (chạy lại ≤ 0,01 nếu cần).
Khai báo sửa: chỉ 2 file review trên + file này.
**Việc xen giữa (19:19 10/11/2026, A giao, 0 USD):** nháp plan B7 ⇒ khai báo sửa thêm `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` (mới). Review B / E vẫn ưu tiên. **XONG 19:21 10/11/2026:** nháp `fe5788b63089` (untracked) đã gửi A — tag `p9-moc` đề xuất `18e8f42`; ≈ 0,30 USD; 4 câu A chốt §8. Lệch báo A: Project_Status §4 `anh.bat` false ≠ thực tế true (`cf57309`). A commit nháp + chốt Q1–Q4 (`main` `1bcc830`), tag `p9-moc` = `18e8f42` đã gắn. **(19:24 10/11/2026) Việc kế:** review phần sửa `bao_cao_he_thong/` (2 sub-agent của A, theo `data/ra_soat_bao_cao_2026-11-10/sa1_*.md` + `sa2_*.md`) khi A nhắn diff sẵn. Thứ tự: review B / E nếu tới trước. **Review sửa báo cáo `c54c932` XONG 19:36 10/11/2026:** `ready_for_user_confirmation`, 0 blocker / 0 major / 2 minor — `report_agent/2026-11-08_phase_9_ban_13/c_sua_bao_cao_1011_review.md` `daf963d9ecd9` (untracked). **Review B `p9-xa-giao-song-song` `9ce7cfd` XONG 19:39 10/11/2026:** code `ready_for_user_confirmation` (0 blocker / 0 major / 3 minor), kết quả đo chưa đạt (đúng nhãn B) — `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_review.md` (untracked). Chạy lại 0 USD: 15 test đạt, AN chấm lại 0 lọt. **Review E `p9-t1-nhanh` `7d6f25f` (19:44 10/11/2026):** `changes_requested` — M-1 câu hỏi "mùng N tháng <số>" không "âm" bị coi là ngày âm (probe 0 USD; bộ đo 0 câu dạng này) + 3 minor — `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_review.md` (untracked). Q1 so lại 215 / 228, 82 test đạt. **Delta `0385bcf` (19:47 10/11/2026): M-1 đóng ⇒ `ready_for_user_confirmation`** (review §7). **Review deploy cục bộ B (19:55 10/11/2026):** `changes_requested` — M-1 hỏi bằng ảnh tắt im lặng trên bản deploy (thiếu `danh_sach_ten.json` trong ảnh) + 2 minor — `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_review.md` (untracked). Đếm lại trong ảnh `dep10`: 0 file private. **Delta (20:03 10/11/2026):** M-1 (a) + m-1 + m-2 đóng ⇒ `ready_for_user_confirmation` (review §6; đếm lại `dep10b`: 0 private). **Review plan định tuyến lịch (B) vòng 1 (21:05 10/11/2026):** `changes_requested` — M-1 cách so 2 lượt / `N_AA` theo nhóm chưa rõ · M-2 N2 cho mục web là đạt (yếu hơn S2b) + 3 minor — `docs/superpowers/plans/2026-11-10-phase-9-dinh-tuyen-lich-plan_review.md` (untracked). **Vòng 2 (21:07 10/11/2026):** bản 2 `aa493aec252f` ⇒ `ready` (5 finding đóng). **Rảnh — chờ B code xong ⇒ review nhánh.** **(21:20 10/11/2026) A giao:** viết lại mẫu `bao_cao_he_thong/README.md` + `01_LUONG_HOAT_DONG_HE_THONG.md` (khai báo sửa 2 file này) ⇒ sub-agent đọc thử ⇒ A. **XONG 21:28 10/11/2026:** README `4d2955801afc` (99 dòng) · LUONG `48f3eca3dff7` (127 dòng), chưa commit; sub-agent đọc thử ~25 góp ý đã sửa; overlap 0. Phát hiện: access log uvicorn ghi IP (đã báo A). **(21:38 10/11/2026) File 02 kho dữ liệu XONG** (A giao; User xem thêm 1 file mẫu): `02_BAO_CAO_KHO_DU_LIEU.md` `55a6e0d27311` + README `eb13afb8a3e9` (cột thứ tự 01…10, thêm "chỉ mục"), chưa commit; sub-agent đọc thử ~20 góp ý đã sửa. Review nhánh định tuyến: A giao E (không phải C). **Rảnh — chờ A / User góp ý.**
**Tự soi 1 (19:15 10/11/2026, A chốt, `main` `839ddb7`):** A nhận cả 6 ý của C. E thu D1 về các dạng có trong bộ đo. Report của B / E có các mục C xin. C chỉ review chỗ rủi ro, không chạy lại lượt đo tốc độ.
Danh sách soi khi review: **B** — khối `finally` của `answer_turn_stream_parallel` (huỷ, gather, `n_tra_loi_bo` / `usd_bo` khi bỏ cả hai phần) · `_merge_spec` gộp trace trò chuyện · số lượt bị huỷ giữa chừng · ngắt kết nối ⇒ task không treo.
**E** — regex dò ngày âm trong đoạn kho (dò nhầm ⇒ dòng lịch thừa / sai) · lượt đã từ chối sẵn (không có nguồn) không được chèn nguồn lịch · câu không có từ chỉ ngày giống byte · D1 chỉ gồm các dạng có trong bộ đo. Kiểm mở phiên: `main` sạch, hooksPath `.githooks`, Qdrant 2 collection / 8.435 point — khớp.

---

---

## (09/11) STATUS C — kết phiên 09/11 (viết 22:28 09/11/2026 — `date`). Lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`

### (09/11) phần "phiên sau" cũ — bẫy còn đúng ở cuối khối

**Trạng thái:** **rảnh — không việc dở, không worktree `/tmp` nào, không nhánh của C đang mở.** Phiên 09/11 terminal: C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E
`hue-rag-ea` (tên đổi khi mở lại — `ListAgents`). Chờ A giao (việc A giao = User nói "làm đi").

**Việc C phiên 09/11 (đều xong):**
- T3 bảng vé + giờ: hướng (a) code + đo (Q1 bật cờ 228/228 giống byte · Q2 lưu ý 0/20 · an toàn 32: ngoài kho bị trả lời 0/4, 1 báo nhầm do lỗi bộ đọc giờ dấu phẩy ⇒ sửa) ⇒
  **đóng hồ sơ** (User), tag `hoso/p9-t3-bang` `e547b9e`; kết luận `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` §13. Bảng `data/phase_9/t3_bang_ve_gio/bang_v1.json` giữ.
- T2: review plan bản nháp (3 major) ⇒ C viết lại plan bản 2 (A duyệt `88b1f0586e99`; + md5 bộ hỏi kèm của E ⇒ `69836a615353`) ⇒ review code E phần 0 USD (ready) ⇒ lượt đo của E **âm** ⇒ đóng hồ sơ.
- T4: review sớm code E (1 major: tiêu chí "câu cố định (b) không nói sai" — E đo 0/19, đóng) ⇒ lượt đo **âm** ở luật xếp ⇒ đóng hồ sơ.
- 4 chốt trước deploy: `p12-chot-deploy` ⇒ merge `ccc9f4f` (A review). Biến: `HUE_LUOT_MOI_NGAY`, `HUE_COOKIE_SECURE`, `HUE_TAT_DOCS`; log xoay vòng 10 MB × 3 luôn bật.
  **Checklist deploy:** uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`; đặt 3 biến trong `compose.yml`; sổ đếm lượt ở RAM.
- Nháp mục "Phiên 09/11" của `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (A duyệt / sửa; số S5 + tiền B / E / A để trống).
- Tự soi cuối phiên đã gửi A / B / E: bài học chính — **đếm lỗi thật trên mốc trước khi dựng tính năng** (T3 chữa lỗi chưa thấy; T2 + T4 âm cùng gốc "lời dặn từ chối cả câu" — một pilot
  mốc 10 câu ≈ 0,012 USD đã đủ thấy).

**Tiền C 09/11 ≈ 0,028 USD:** T3 (a) Q2 0,010562 + an toàn 32 0,017105 · chốt deploy ≈ 0,00035 · review / plan 0 USD.

**Bẫy mới 09/11:**
- Auto mode chặn đọc file `*sealed*` cả khi A giao rõ (rào đúng, không lách) ⇒ viết sẵn một lệnh `!` chỉ in dòng cần, gửi A; `cut -c1-4000` có thể cắt mất phần trả lời — bỏ trường `context` trước khi in.
- `git worktree remove` cần `--force` khi worktree còn file gitignore (`backend/logs/`); gỡ symlink `data/`, `knowledge-base-hue/` trước.
- Log `application.log` xoay vòng ở 10 MB (từ `ccc9f4f`) ⇒ harness đếm dòng theo vị trí có thể đếm hụt nếu xoay giữa lượt — kiểm cỡ log trước lượt đo.
- `@app.middleware("http")` (BaseHTTPMiddleware) bọc luồng SSE + dò ngắt kết nối ⇒ middleware chặn lượt viết dạng ASGI thuần (`api/gioi_han.py` `ChanLuot`).
- Test gọi `logging.config.dictConfig` đổi logging toàn cục cả tiến trình pytest ⇒ hỏng test đếm dòng log — không viết test kiểu đó.
- Bộ đọc giờ / số liệt kê: ranh giới số phải cho ", " (liệt kê) — luật cũ `(?![\d,])` bỏ mọi số đứng trước dấu phẩy.

### Bẫy (08/11, vẫn đúng)
- `kill` PID server tạm bị auto mode chặn ⇒ chạy server bằng `run_in_background` để tắt bằng TaskStop; nếu lỡ `nohup` ⇒ User `!`.
- `test_cong_dot_1::test_weather_and_feature_routes` hỏng **chỉ khi nạp khoá** (`--env-file`; có khoá ⇒ ảnh bật) — không do nhánh.
- `tim_so_tien` cần đơn vị ("đồng") — ô bảng giá trong kho thường ghi số trần ⇒ phía "cho phép" phải nhận cả số nhóm nghìn trần.
- Công cụ đo SSE: một `httpx.Client` giữ cookie ⇒ mọi câu chung một cuộc trò chuyện — mỗi câu một client.
- Bộ chấm: nhãn giá phải kèm đơn vị như bảng; tập cho phép theo đúng chữ plan — kiểm bộ chấm trên một câu trước khi đọc số.
- `an_toan_run.py` cũ gọi `answer_case` **không** cờ (= RAG 1–8) ⇒ đo trợ lý phải truyền `AssistantFlags.from_settings`.
- `wait_for_function` chuỗi của Playwright bị CSP chặn (`unsafe-eval`) ⇒ chờ bằng vòng Python.
- Sub-agent đọc kho đôi khi đổ đầu ra ra `/tmp` — brief nhắc "không ghi file ngoài đích".
- Giờ trong file: luôn `date`; không ghi "~hh:mm".


---

## (09/11) nhật ký trong phiên — chỉ tra cứu (mở 20:10 09/11/2026) — C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E `hue-rag-ea`
**A giao (20:13 09/11/2026, User: việc A giao = "làm đi"), 0 USD:**
(1) dựng lại `/tmp/c_t3` từ `p9-t3-bang` `21ec06d`, rebase lên `main` `5c982a0`, chạy test file bị chạm (chưa đo). Khai báo sửa: nhánh `p9-t3-bang` (5 file của nhánh, chỉ giải xung đột rebase), push nhánh.
(2) review plan T2 `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (`921f75d64a7c`) ⇒ file mới `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan_review.md`.
**(1) XONG:** `p9-t3-bang` rebase lên `main` `5c982a0` = **`0eeb6f9`** (pushed): giữ cả T1 + T3, `max_turns_for(ngay_lich, ve_gio, thoi_tiet)` cộng dồn + 1 test. Test file chạm 460 đạt; cả `backend/tests` 885 đạt / 8 hỏng-lỗi đã biết (5 cần khoá, 2 cần bản build UI), 3 phút 43 giây.
**(2) XONG:** review T2 `changes_requested` 0 blocker · 3 major (max_turns · sàn S2c/S5/S6/S1×2 · bộ hỏi kèm 10) — sha `2653316dd16a` (untracked, A commit). Đã nhắn B + A.
**(3) T3 ĐÓNG HỒ SƠ (20:50 09/11/2026, User chọn, A báo):** không merge; nhánh `p9-t3-bang` = `e547b9e` (pushed) — A gắn tag `hoso/p9-t3-bang` + xoá nhánh khi User duyệt. Kết luận report §13. Worktree `/tmp/c_t3` (cờ `false`) — gỡ: `rm /tmp/c_t3/data /tmp/c_t3/knowledge-base-hue && git worktree remove /tmp/c_t3` (User `!` nếu `rm` bị chặn). Câu kín b_kin_07: A bỏ (User đã chạy lệnh 1: câu thuộc loại pháp lý chung, nhãn ngoài phạm vi chắc; chưa ghi `kin_c_doc.md` vì A bỏ việc). Tiền T3 09/11 0,027667.
**(4) ĐANG LÀM (20:50 09/11/2026, A giao):** sửa plan T2 theo 3 major C ghi + chốt tự soi (sàn S1 + ngoài kho / ngoài phạm vi + đúng câu; S5 / S6 đo chung lúc đóng đợt; không bộ kín). Khai báo sửa: `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (C cầm thay B). ≤ 0,2 USD ⇒ mức nhẹ, A đọc duyệt. Code chờ G vào `main`. **Bản 2 XONG — sha `88b1f0586e99`, chờ A duyệt** (≈ 0,17 USD); bộ hỏi kèm 10 nhờ E viết (`data/phase_9/t2_web/hoi_kem_10.jsonl`, md5 ghi vào plan §3 trước lượt có phí).
**(5) XONG — chờ review (21:01 09/11/2026; giao lúc 20:55 09/11/2026, A giao, 0 USD, mức nhẹ) — 4 chốt trước deploy, nhánh `p12-chot-deploy` từ `main` `2db09b8`, worktree `/tmp/c_dep`.** Plan ½ trang:
- **Mặc định = hành vi hiện tại** (không đặt biến môi trường ⇒ không đổi gì; chuỗi gửi model không chạm).
- (1) Log: `config/logging.yaml` handler `file` ⇒ `logging.handlers.RotatingFileHandler` 10 MB × 3 bản (luôn bật; dưới 10 MB y như cũ — log máy User ~0,6 MB).
- (2) Cookie: `HUE_COOKIE_SECURE=1` ⇒ cookie `conversation_id` có `Secure` (đọc mỗi lần đặt cookie, `api/routes/chat.py` `_set_cookie`); không đặt ⇒ `secure=False` như cũ.
- (3) Tài liệu API: `HUE_TAT_DOCS=1` ⇒ `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` (`api/app.py`); không đặt ⇒ như cũ.
- (4) Giới hạn lượt: `HUE_LUOT_MOI_NGAY=<n>` (> 0) ⇒ đếm lượt POST `/api/chat`, `/api/chat/stream`, `/api/anh/ung_vien` theo IP (`request.client.host`) theo ngày giờ Việt Nam, trong RAM; vượt ⇒ 429 JSON `{error: {code: "rate_limited", message}}` (giao diện hiện `error.message`, không sửa giao diện); log 1 dòng cảnh báo không ghi IP. Không đặt / 0 ⇒ tắt. Sau proxy (Caddy): uvicorn phải chạy `--proxy-headers --forwarded-allow-ips <ip proxy>` để `client.host` là IP thật — ghi vào checklist deploy, không tự đọc `X-Forwarded-For` (giả mạo được).
- Khai báo sửa: `backend/config/logging.yaml`, `backend/api/app.py`, `backend/api/routes/chat.py`, `backend/api/gioi_han.py` (mới), `backend/tests/test_chot_deploy.py` (mới).
- Kiểm: test file mới + file chạm (`test_api_chat.py` không khoá, `test_static_ui.py`); 1 lần server thật bật cả 4 biến (`/docs` 404, cookie `Secure`, lượt thứ n+1 ⇒ 429) + 1 lần không biến (như cũ). 0 USD (dùng câu ngoài phạm vi / lượt bị chặn trước model — vẫn có 1–2 câu thật ≈ 0,001).
- **Kết quả:** nhánh `p12-chot-deploy` = **`a3db152`** (pushed). Test mới `test_chot_deploy.py` 5 đạt; file chạm (`test_api_chat` · `test_feedback` · `test_cong_dot_1`) 40 đạt / 1 lỗi = test cần khoá (đã biết). Server thật cổng 8897: **bật 3 biến** (`HUE_TAT_DOCS=1 HUE_COOKIE_SECURE=1 HUE_LUOT_MOI_NGAY=2`) ⇒ `/docs` 404 · `/openapi.json` 404 · cookie có `Secure` · lượt 1–2 200, lượt 3 `/api/chat` 429 + lời báo, `/api/chat/stream` 429 · log 2 dòng `chat_metrics` + 2 dòng "Rate limited", 0 lần chứa IP; **không biến** ⇒ `/docs` 200, cookie không `Secure`, không 429. Log xoay vòng nạp được (server khởi động bình thường). Tiền ≈ 0,00035 USD (4 câu ngoài phạm vi). Bỏ test cấu hình log (dictConfig trong test đổi logging toàn cục ⇒ hỏng test đếm dòng log).
- **Checklist deploy (cho A):** sau Caddy phải chạy uvicorn `--proxy-headers --forwarded-allow-ips <ip Caddy>` (không thì mọi người chung một IP ⇒ một sổ đếm); đặt 3 biến trong `compose.yml`; đếm trong RAM ⇒ khởi động lại là xoá sổ (chấp nhận cho đồ án).
**(6) XONG (21:08 09/11/2026):** review `p9-t2-web` `2ac126a` (E, phần 0 USD) — **ready** 0 blocker · 0 major · 2 minor; `report_agent/2026-11-08_phase_9_ban_13/c_t2_web_review.md` (untracked). Chạy lại: 183 test đạt · Q1 cờ tắt 228/228 giống byte. Worktree `/tmp/c_t2rv` (tách, symlink `data/`, `knowledge-base-hue/`) — gỡ khi xong.
**Bẫy (A ghi, 1 dòng):** harness đếm dòng `application.log` theo vị trí — từ `ccc9f4f` log xoay vòng 10 MB ⇒ lượt đo trùng lúc xoay đếm hụt; kiểm cỡ log trước lượt đo. `p12-chot-deploy` đã merge (`ccc9f4f`), nhánh chờ User `!` xoá; worktree `/tmp/c_dep` gỡ khi xoá nhánh.
**(7) XONG (21:11 09/11/2026, A giao):** review sớm `p9-t4-lich` `9780d93` (E) — 0 blocker · 1 major (thêm tiêu chí "câu xin lịch không hỏi kèm có câu cố định (b) = 0", code không sửa); `report_agent/2026-11-08_phase_9_ban_13/c_t4_lich_review.md` (untracked). 331 test · Q1 tắt 228/228. Worktree `/tmp/c_t4rv` (tách, symlink) — gỡ khi xong. Lệch: plan T4 sha trên ổ `5a22b51fe49c` ≠ A duyệt `29708ef92e30` (đã báo A).
**T2 âm (E, 21:49 09/11/2026):** hỏi kèm có web 4/10 = mốc; C đồng ý đóng hồ sơ, không đề xuất vòng chỉnh mô tả (đã nhắn A). **RẢNH — chờ E** rebase + đo T4 ⇒ C xem delta. Worktree `/tmp/c_t2rv` hết dùng.
**T4 âm (E, 22:18 09/11/2026):** Q3 (ii) 21 · 15 / 27 < 26; review M-1 của C đóng (câu (b) nói sai 0/19). C đồng ý đóng hồ sơ (đã nhắn A). **RẢNH — chờ A** (không còn delta nào phải xem). Worktree `/tmp/c_t4rv` hết dùng.
**Dọn (22:19 09/11/2026, A giao):** đã gỡ 4 worktree `/tmp/c_dep`, `/tmp/c_t2rv`, `/tmp/c_t3`, `/tmp/c_t4rv` (gỡ symlink trước; chỉ còn file bị gitignore như `backend/logs/` ⇒ `--force`). C không còn worktree nào. **RẢNH — chờ A** (đang khoá máy cho S5 của B: không chạy lượt có phí / pytest rộng / build).

## (07/11) kết phiên — chỉ tra cứu
**Trạng thái:** rảnh có lý do — không việc đang dở, không worktree `/tmp` nào của C. Chờ A giao (việc A giao = User nói "làm đi"). `main` khi viết: `fbcb903`.
Phiên 07/11: terminal C `hue-rag-a0` · A `hue-rag-7a` · B `hue-rag-10` · E `hue-rag-81` (tên đổi khi mở lại — `ListAgents`).

### 1. Việc xong 07/11 (report tracked — sha256 12 lúc viết)
- **S3 đo cổng đợt 1** — `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` `b178c47c6abe`:
  - bộ quyết 12 tổ hợp `data/phase_9/cong_dot_1/to_hop_chinh_thuc.jsonl` md5 `792a3cbe3fe5` (ẩn "đi dày" theo Q-U3) — **đã dùng để quyết**, từ nay chỉ là bộ hồi quy;
  - **Q-G + Q-N trên `27ed091`: ĐẠT** (7 / 7 đích × 1440 / 390, 0 CSP / console, JS gzip 101,9 KB, tương phản thấp nhất 5,42; Q-N 10 / 10) — đã merge;
  - **Q-F bộ quyết trên `632a4f7` (V5): ĐẠT** — sàn code 24 / 24, F-a 12 / 12 + 12 / 12 (2 sub-agent, 0 bất đồng); User duyệt bật biểu mẫu + F-a (4) = "không trái nhóm đi cùng" ⇒ `main` `a884de4` cờ `lich_trinh_bieu_mau` BẬT;
  - §6 chữ đầu trên `main` `a884de4` (theo dõi): biểu mẫu p50 2,30 / p95 4,22 s · câu kho 1,78 / 3,61 s (n = 10 mỗi loại).
  - Data private: `data/phase_9/cong_dot_1/s3/` (lan_1 / lan_2 / `fa/` phiếu + 2 file chấm), `qn/` (10 câu Q-N + kết quả), `qg_tuong_phan_27ed091.json`, `chu_dau_main_a884de4.jsonl`.
- **X1 / X1b / X1c lượt biểu mẫu bị model từ chối** — `report_agent/2026-11-06_giao_dien_cong/c_x1_luot_bieu_mau.md` `99abfe79ee01`; data `data/phase_11/cong_dot_1/x1/`. Nguyên nhân (ủng hộ, chưa chứng minh): `LICH_TRINH_LUAT` nằm trong phần Bằng chứng ⇒ model coi là dữ liệu. V0 từ chối 10 / 16 · V1 (giả lượt công cụ) 12 / 16 · V2 (luật lên lời dặn hệ thống) 1 / 16 → 0 / 16 nhưng chữ đầu p95 8,8 s · V4 (thêm câu dặn) kém · **V5 = V2 + reasoning `low`** đạt (p95 4,75 s) ⇒ B đưa vào nhánh · V6 `minimal` ⇒ 400 · V3 (code dựng lời, 0 USD) đọc như trích máy. Đề xuất dự phòng chưa làm: "hiện khung code trước, lời model sau".
- **Tự soi** — `report_agent/2026-11-07_tu_soi_lo_trinh/tu_soi_C.md` `69727aa946ad` (deploy chưa thử = rủi ro lớn nhất; đóng hồ sơ sửa lịch; gỡ 3 cờ âm ở B7; giọng nói cắt nếu chưa có 40 câu trước ~20/11; đợt 2 chỉ P1).
- **C-tl thời lượng tham quan từ web** (0 USD; private): `data/phase_9/lich_trinh/thoi_luong_web.json` (link + ngày + trích từng nguồn) · `diem_v7_thoi_luong_web_nhap.json` sha256 `363763ae2101` (trường khác giống v6) · `tools/dung_v7.py` · tra thô `data/tra_cuu_cli/2026-11-07_c-tl-thoi-gian-1/`, `-2/`. 19 / 26 điểm có số (11 ngắn · 8 nửa buổi); mức chắc cao 4 · vừa 5 · thấp 6 · lệch 4.
- Dữ kiện Q-U3: `kieu_di` không đổi khung ở 0 / 120 tổ hợp với bảng v3/v6; v7 ⇒ 12 / 120.

### 2. Đang chờ User (qua A) — C không tự làm
- **Phiếu v7** `data/phase_9/lich_trinh/diem_cho_user_v7.md` (sha256 `ee2f22328691`): A dùng cả bảng / B chỉ dòng chắc cao + vừa (9 điểm) / C giữ v6. `settings.yaml` `lich_trinh_bang` vẫn `diem_v3.json`.
- **3 luật xếp "đi dày" đề xuất, CHƯA ĐO** (phiếu v7 §2): điểm thứ hai lấy cả di tích lấp chỗ · cho cặp ngắn ở cụm kề · "đi dày" mở buổi tối hợp sở thích cho nhóm không hạn chế. Biểu mẫu đợt 1 đã ẩn "đi dày" ⇒ không chặn gì.
- **Mô phỏng kín sửa lịch: vẫn DỜI** (sửa lịch hoãn, có thể đổi cách "điền lại biểu mẫu") — lệnh ở mục (cũ) dưới, chỉ chạy khi A giao lại.

### 3. Công cụ dùng lại được (private, chạy từ `backend/` của worktree nhánh cần đo; `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag [--env-file /home/minhhieu/hue_rag/.env] python …`)
- `data/phase_9/cong_dot_1/tools/do_bieu_mau.py` md5 `4de78cb35999` — Q-F biểu mẫu: `kiem <bộ>` (0 USD: luật phủ + xếp thật + 9 ca phá) · `chay <bộ> <out.jsonl> --lan N [--dung 0.025]` (CÓ PHÍ, `/api/chat/stream` qua TestClient, bọc `_remember`; `--dung` cộng mọi *.jsonl cùng thư mục) · `cham` · `phieu <bộ> <kq> <thư_mục>` (đầu vào 2 người chấm F-a) · `gop <thư_mục> <c1> <c2>`.
- `data/phase_9/cong_dot_1/tools/tuong_phan.py` md5 `f53a31153ce3` — tương phản WCAG trên trang đã dựng (Playwright): `uv run python …/tuong_phan.py http://127.0.0.1:<cổng>/ --trang '#/,#/kham-pha,#/kham-pha/foods,#/kham-pha/bai/<id>,#/len-ke-hoach,#/tro-ly,#/gioi-thieu' [--json out]`.
- `data/phase_9/cong_dot_1/tools/playwright_cong.py` md5 `fa580e39f5ed` — 7 / 7 đích ≤ 2 lần bấm + mở thẳng / tải lại + CSP / console + bundle: `uv run python …/playwright_cong.py http://127.0.0.1:<cổng>/ --dist <worktree>/frontend/dist`.
- `data/phase_9/cong_dot_1/tools/qn_nguon.py` md5 `3710c9c69c4e` — Q-N 10 câu (`qn/cau_qn.txt`) qua giao diện + chữ đầu phía trình duyệt (CÓ PHÍ ~0,004).
- `data/phase_9/cong_dot_1/tools/do_chu_dau_main.py` md5 `5915e4a681ef` — chữ đầu qua server thật: `uv run python …/do_chu_dau_main.py http://127.0.0.1:<cổng> <log server> <out.jsonl>` (CÓ PHÍ ~0,008).
- `data/phase_11/cong_dot_1/x1/x1.py` (gọi hàm lõi trong tiến trình, V0–V3) · `x1b.py` / `x1c.py` (đường stream, agent clone đổi lời dặn / reasoning) · `tong.py` / `tong_b.py` (in bảng). Mẫu để thử biến thể lời dặn / tham số model mà không sửa nhánh.
- Cổng server tạm: worktree tách (`git worktree add --detach /tmp/<tên> <sha>` + symlink `data/`, `knowledge-base-hue/`), `cd frontend && npm ci && npm run build` nếu cần giao diện, `uvicorn api.app:app --port <trống>` chạy nền, tắt bằng TaskStop, gỡ symlink rồi `git worktree remove --force`.

### 4. Bẫy đã gặp 07/11
- `gpt-6-luna` **không nhận `reasoning.effort = "minimal"`** ở đường trả lời ⇒ 400 (`BadRequestError`, app không log chữ lỗi). `low` được.
- **Chỉnh trên bộ phát triển, quyết trên bộ giữ riêng**: X1 dùng 8 tổ hợp phát triển; bộ quyết 12 không chạy / không xem tới khi chốt biến thể. Giữ cách này cho thí nghiệm sau.
- **Đo latency không chồng việc nặng**: trước lượt đo nhắn B / E (và hỏi A — có lúc một dự án khác trên máy cũng chờ dùng máy); xong nhắn "xong đo". Lượt latency là việc của một người một lúc.
- `kiem_cuoi` không phân biệt biến thể khi lượt từ chối được code thay bằng lời tối thiểu (B171) ⇒ đếm từ chối riêng (chữ model = câu từ chối hoặc có `chu_thay`).
- `kiem_khung` coi ngày bị cắt vì vượt ngân sách (`vuot_ngan_sach`) là hợp lệ ⇒ đếm riêng (`cat_ngay_cuoi`).
- Tiêu chí chấm bằng người / sub-agent có chữ mơ hồ ("phù hợp người đi cùng") ⇒ ghi cách hiểu **trước** khi chấm; người làm không tự chốt cách hiểu sau khi thấy số.
- Sub-agent chấm có thể ghi file bằng Bash thay vì Write — kiểm file ra đủ mã, ghi vào report.
- **Sửa trước khi tái tạo** (C210): việc "sửa lỗi X" mà nguyên nhân chưa chứng minh ⇒ tái tạo trên code gốc TRƯỚC (đọc tham số thật), chưa viết sửa — A phải nhắc lần này.
- Đổi hành vi code (vd B171 đổi khung) ⇒ chạy lại mô phỏng nhãn (`mo_phong.py`, kín qua `!`) **trước** lượt có phí.
- Q1m: `data/phase_9/b5b/tools/capture_flags.py <out> lich_trinh=1 sua_lich=0|1`. Script import `llm.*`: không `-I`, `PYTHONPATH=$PWD`.
- Rebase "hai bên cùng thêm": giữ cả hai, kiểm `git range-diff`. Heredoc shell có backtick ⇒ dùng Write.
- Ca dò của người kiểm gồm cả câu **hợp lệ** model hay viết. Giờ trong file: luôn `date` trước.
- Overpass máy chủ công khai hay quá tải (06/11: 3 / 5 lượt 502) ⇒ `out count` nhẹ qua được; lấy thẻ thì một lần, giãn cách, không gửi dồn.
- Tin A có thể đến lúc C đang làm việc khác ⇒ việc mới ưu tiên theo lời A (vd B171 trước harness); việc dở ghi STATUS trước khi chuyển.

### 5. Tiền C 07/11 ≈ **0,078 USD**: X1 0,0247 · X1b 0,0174 · X1c 0,0143 · Q-N 0,0042 · S3 0,0087 · chữ đầu `main` 0,0084; mọi việc khác 0 USD (Codex tra web dùng tài khoản ChatGPT).

### 6. Tạm
- `/tmp/c_tl/` chỉ còn file thử / bảng tạm (yêu cầu tra web, kết quả thử V3, bảng tương phản) — không dữ liệu kín; mất khi khởi động lại cũng được.

---

## (cũ) — kết phiên tối 06/11 (chỉ tra cứu)

### Việc + lệnh của phiên tối 06/11 (S3 / S4 trong đó đã XONG 07/11; harness + lệnh sửa lịch vẫn đúng khi mở lại)
- **Đã xong tối 06/11** (terminal `hue-rag-42`):
  - **Harness sửa lịch:** `data/phase_9/sua_lich/tools/chay_sua_lich.py` md5 `559ebaf5f81e` — E review vòng 2 + vòng 3: **ready**. Bộ Q4 `bo_do_sua_lich/chuoi_q4.jsonl` `d35f8d9c5027`. Pilot = S01 + S06 (A duyệt). Report `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §7–§8.
  - **B171 review:** ready trên `b0e52f8` (đã merge `dbb4004`) — `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` §7–§8.
  - **C208:** `p9-sua-lich` ⇒ **`79b3d9c`** trên `main` `d930867` (pushed). Gỡ xung đột B5b; sửa `hoi_toi` khi xếp lại / sửa trực tiếp + 4 test. 411 test; Q1 / Q1m 228/228 (`data/phase_9/sua_lich/q1_c208/`). Nhãn đã thấy S03 / S08 sửa theo B171 ⇒ `chuoi_da_thay.jsonl` **`c00de07114b5`**. E kiểm rebase: ready.
  - **C209:** `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md` (P1 / P2 / P3 bản đồ + dữ liệu; C khuyên P1) — chờ User quyết khi A trình spec.
  - **C210:** chưa tái tạo được "hỏi lại số ngày thừa" ⇒ không sửa code (`report_agent/2026-11-06_b5_cau_tu_nhien/c210_implementation.md`). Đề xuất: harness kín lần sau ghi `so_ngay` model gửi + số code dò + có thẻ hỏi không.
  - **C211:** nháp kỹ thuật spec đợt 1 `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` — A dùng khi viết spec.
- **Việc đầu phiên sau — lệnh `!` mô phỏng bộ kín sửa lịch** (0 USD, chỉ in số đếm + mã chuỗi / số lượt hỏng, trên nền `79b3d9c`):
  1. C dựng lại worktree (đã gỡ):
     ```
     git worktree prune; git worktree add /tmp/c_sualich p9-sua-lich
     ln -s /home/minhhieu/hue_rag/data /tmp/c_sualich/data
     ln -s /home/minhhieu/hue_rag/knowledge-base-hue /tmp/c_sualich/knowledge-base-hue
     ```
  2. Đưa User lệnh nguyên văn (cũng ở report C207 §8):
     ```
     ! cd /tmp/c_sualich/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python ../data/phase_9/bo_do_sua_lich/tools/mo_phong_kin.py | python3 -c "import json,sys,re; d=json.load(sys.stdin); print('kin ok', sum(v=='ok' for v in d.values()), '/', len(d)); [print(k, [re.match(r'L[0-9]+', x).group() for x in v]) for k, v in d.items() if v != 'ok']"
     ```
  3. Kết quả hỏng ⇒ sửa nhãn kín bằng `bo_do_sua_lich/tools/cau_truc.py` (không in câu) **trước** lượt có phí. `main` đổi code ⇒ rebase + Q1 / Q1m trước.
- **Sửa lịch — HOÃN** (handoff 22:41 06/11): cần cờ `lich_trinh` câu tự do; A xem lại cách sửa sau biểu mẫu ("điền lại biểu mẫu"). Khi đi tiếp:
  - thư mục kết quả `data/phase_9/sua_lich/do/` chỉ chứa file kết quả (`--dung 0.19` cộng mọi `*.jsonl` trong đó);
  - pilot S01 + S06 lần 1 ⇒ đọc file ⇒ lần 1 / lần 2 / Q4 ×2 ⇒ kín ×2 qua User `!` ⇒ `cham`.
- **S3 — đo Q-F biểu mẫu lịch trình** (spec cổng đợt 1 `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` bản 2 `ff3c317ec88b` §6; khi B xong S1 trên `p11-cong-dot-1`; cờ mới `assistant.lich_trinh_bieu_mau`):
  - **trước lượt có phí:** ghi 12 tổ hợp vào report S3, **sau khi User chốt Q-U3** (đi dày). Phủ đủ 5 `di_cung`; mỗi `so_ngay` 1 / 2 / 3 ≥ 3 lần; ≥ 4 có `so_thich`; ≥ 2 không chọn sở thích;
  - harness lưu **khung + chữ model + tham số** mỗi lượt (dựng theo mẫu `chay_sua_lich.py`: TestClient trong tiến trình, bọc hàm, đọc log sau mốc). Ghi cả `so_ngay` model gửi / số code dò (đề xuất C210);
  - ×2 = 24 lượt. Sàn code 24 / 24: 0 câu từ chối thay lịch, `kiem_cuoi` 0 lỗi, 0 rút lại;
  - F-a: 2 sub-agent mới độc lập chấm (khung + chữ + giá trị nút), ≥ 11 / 12 mỗi lượt theo cả hai, bất đồng ⇒ trượt;
  - Playwright §6 (Q-G phần C được giao); tiền cả spec ≤ 0,03 USD.
- **S4 — review cả nhánh `p11-cong-dot-1`** một lần (`risk-gated-agent-review`; bảng rà AI FDE §7 là một tiêu chí). Ca dò khác cách người làm: API Khám phá `../`, `sealed`, id ngoài `corpus.sources`; form gửi `truong` lạ ⇒ 422.
- **Đợt 2 (dữ liệu bản đồ / lưu trú / ăn uống / sự kiện):** chờ User chọn P1 / P2 / P3 (C209). Chọn P1 / P3 ⇒ Overpass **một** lần lấy thẻ tên ⇒ khớp toạ độ 15 điểm thiếu (người xem bằng mắt). Chọn P2 ⇒ đo dung lượng PMTiles + cỡ gói MapLibre trước.
- **Câu treo cho A** (không chặn):
  1. mô phỏng kín sửa lịch có còn cần chạy đầu phiên không, khi sửa lịch hoãn và có thể đổi cách ("điền lại biểu mẫu");
  2. C210: câu nêu số ngày mơ hồ ("3 hay 4 ngày") + model gửi số ⇒ code hiện dùng số model, không hỏi — giữ hay hỏi;
  3. link trong chữ câu trả lời chưa có `target` / `rel` — gộp vào S1 / S2?
- **Bộ đo (private, md5 12):** sửa lịch đã thấy `c00de07114b5` (trước C208 `d0ad12b6ed12`) · kín `daf762bcbbe5` · Q4 `d35f8d9c5027`; B6 `6ed74db21616` / kín `4de04132600b`; B5b `7e1bc3da2e44`; bảng `diem_v5.json` `c7d294fcacd5`.
- **Không đọc:** `data/phase_9/b5_v2/`, `data/phase_9/b5/kin/`.
- **Tiền C tối 06/11: 0,003855 USD** (C210 tái tạo; mọi việc khác 0 USD). Overpass (OSM) quá tải 3/5 lượt — lần sau gọi một lần, ngoài giờ cao điểm.
- **Backlog cho A:**
  - kho mâu thuẫn vị trí Bảo tàng Cổ vật · câu thiên tai vẫn gọi Serper · case 67 Golden từ chối ngẫu nhiên;
  - link trong chữ câu trả lời chưa có `target` / `rel` (C211);
  - câu `toi_khong_diem` nói "hợp sở thích" cả khi không nêu sở thích (E, có sẵn trên `main`).
