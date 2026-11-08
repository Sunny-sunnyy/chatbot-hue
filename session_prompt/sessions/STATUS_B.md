# STATUS B — phiên 08/11 (mở 09:16 08/11/2026 `date`)

Vai: thực thi. Terminal 08/11: A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22`. Quyền phiên: User cấp lại "như 07/11" (A báo).

## 0. Đang làm — B-ảnh: đưa 7 ảnh cổng vào `frontend/` (A giao 08/11, 0 USD)
- Nhánh `p11-anh-cong` từ `main` `db6e15d`, worktree `/tmp/b_anh` (symlink `data/`, `knowledge-base-hue/`).
- Nguồn: `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/` (`bay_anh_dot1.json`, `danh_sach.md` "7 ảnh dùng cho đợt 1"; #5 thật ở `ngoai_git/`).
- **File khai báo sửa (trong worktree):**
  - `frontend/public/anh/*.jpg` (mới — 6 ảnh Commons + dự phòng lễ hội)
  - `frontend/public/anh/rieng/` (gitignore — ảnh #5 thật, không commit) + `.gitignore`
  - `frontend/vite.config.js` (cờ build: có ảnh #5 thật hay không)
  - `frontend/src/pages.jsx` (ảnh đầu trang, 5 ô lĩnh vực, mục "Nguồn ảnh" ở Giới thiệu), `frontend/src/anh.js` (mới — danh sách ảnh + ghi công), `frontend/src/index.css`, `frontend/src/App.jsx` (link "Nguồn ảnh" ở chân trang)
  - test: `backend/tests/test_static_ui.py` (nếu cần)
  - report: `report_agent/2026-11-06_giao_dien_cong/b_anh_cong_implementation.md`
- Ảnh: User đã chốt 17:11 07/11 (bộ vi.wikipedia, không còn bộ `commons/` cũ).
- **Xong 09:31 08/11/2026 (`date`), chờ review C:** `p11-anh-cong` = `fb00719` (đã push). 24 test đạt; Playwright 1440 + 390: 7 ảnh tải, 0 lỗi console / CSP, cả khi có lẫn không có ảnh riêng; `git ls-files` 0 file `rieng`. Report `report_agent/2026-11-06_giao_dien_cong/b_anh_cong_implementation.md`. Tiền 0 USD. Server thử 8871 đã tắt. Worktree `/tmp/b_anh` giữ tới khi review xong.
- Script: `data/phase_11/anh_cong/tools/dong_anh.py` (chép + thu nhỏ, chạy lại ra cùng byte), `kiem_anh.py` (Playwright tự kiểm).
- Cần A quyết lúc deploy: ảnh #5 riêng vào `dist/` nếu máy build có file ⇒ link công khai có phục vụ ảnh này không.

## 0b. Đang làm — plan "bản đồ lịch trình" (A giao 08/11, P1 đợt 2 cổng; 0 USD, chưa code)
- File khai báo sửa: `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` (mới).
- **Bản 1 xong 09:35 08/11/2026 (`date`), chờ review** (A chọn người). Khuyến nghị Leaflet 1.9.4 + tile OSM, cờ `ban_do_lich` tắt mặc định, CSP thêm 1 host `img-src` theo cờ; 17 / 28 điểm có toạ độ; 3 câu cần A quyết ở §10. 0 USD.
- Ảnh cổng: A nhận `fb00719`, C review sau; deploy công khai mặc định KHÔNG kèm ảnh #5 riêng (A ghi checklist).

## 0c. Đang làm — code bản đồ lịch trình (A duyệt plan `e738f6f9f3ae` 08/11; trần 0,005 USD)
- Nhánh `p11-ban-do` từ `main` `2a2a40e`, worktree `/tmp/b_bando` (symlink `data/`, `knowledge-base-hue/`).
- **File khai báo sửa (trong worktree):** `backend/llm/lich_trinh.py`, `backend/llm/assistant.py`, `backend/config/settings.yaml`, `backend/api/app.py`,
  `backend/api/routes/cong.py`, `frontend/package.json` + `package-lock.json`, `frontend/src/BanDoLich.jsx` (mới), `frontend/src/chat.jsx`, `frontend/src/pages.jsx`,
  `frontend/src/index.css`, `frontend/src/App.jsx` (nếu cần cờ), test `backend/tests/test_ban_do_lich.py` (mới) + test cũ chạm cờ / CSP;
  report `report_agent/2026-11-06_giao_dien_cong/b_ban_do_implementation.md`; dữ liệu đo `data/phase_11/ban_do/`.
- **Xong 09:59 08/11/2026 (`date`), chờ review:** `p11-ban-do` = `d0adf31` (đã push; rebase lên `main` `1611d34`, 355 test + kiểm 0 USD đạt). Q1 228/228 giống byte (cờ tắt + bật); test rộng 731 đạt (hỏng còn lại = test cần khoá); Playwright lượt 2: 6/6 ngày ghim đúng, 0 lỗi CSP, tile 66/66, 0 host lạ, 0 lộ chữ; cổng ổn định đạt. CSP cờ bật = `img-src 'self' blob: data: https://tile.openstreetmap.org` (A chọn (a)). Sửa test B6 hỏng sẵn (A giao). Tiền 0,00306 USD / 0,005. Server 8873 đã tắt; worktree `/tmp/b_bando` giữ tới review.

## 0d. Đang làm — việc nhỏ (1) sao chép / tải lịch · (4) câu buổi tối chỉ khi có sở thích · (6) link Maps theo toạ độ (User duyệt Nhóm 1 + 2, A giao 08/11)
- Nhánh `p11-lich-nho` xếp chồng trên `p11-ban-do` `d0adf31` (dùng bảng toạ độ của nhánh bản đồ), worktree `/tmp/b_nho`; rebase lên `main` sau khi bản đồ merge.
- **File khai báo sửa:** `backend/llm/lich_trinh.py`, `backend/llm/assistant.py`, `backend/tests/test_ban_do_lich.py`, `backend/tests/test_b5_lich_trinh.py` (nếu chạm), `frontend/src/chat.jsx`,
  `frontend/src/index.css`; report `report_agent/2026-11-06_giao_dien_cong/b_lich_nho_implementation.md`; dữ liệu `data/phase_11/lich_nho/`.
- **10:47 08/11/2026 (`date`):** `p11-lich-nho` = `de08454` (rebase lên `main` `06dafb4`; 2 minor bản đồ + **bỏ (6)** theo A; 735 test; trình duyệt đạt) ⇒ A merge (E kiểm diff). Bản cũ: `098a710` (đã push). Q1 228/228; test rộng 735 đạt; trình duyệt: clipboard = file tải, 4/4 link đúng code; cổng ổn định đạt. Tiền 0,000435 USD. Cần User mở 17 link theo toạ độ (`data/phase_11/lich_nho/kiem_17_link.md`) — nghi lệch 1 điểm (Kinh thành / Ngọ Môn – Kỳ Đài). Server 8874 đã tắt; worktree `/tmp/b_nho` giữ.

## 0g. Đang làm — việc G cổng 2 nhóm (spec bản 13 §12, User duyệt sha `5557f0fd7650`, A giao 08/11). Bước 1 plan: `docs/superpowers/plans/2026-11-08-phase-9-g-cong-plan.md` (mới). Code sau khi plan duyệt: nhánh `p9-g-cong`, worktree `/tmp/b_g`. B viết lời dặn ⇒ **không đọc câu kín** của bộ (a) / (b).

## 0f. Đang làm — review spec Phase 9 bản 13 (§12, sha `0845b1caefbc`, C viết; A giao 08/11). File khai báo: `docs/superpowers/specs/2026-11-02-phase-9-design_review_v13.md` (mới). Chỉ đọc spec + gói căn cứ + code / dữ liệu; không đọc STATUS_C / tin của C.
- **Vòng 1 xong 10:53 08/11/2026 (`date`): `changes_requested`** — 2 major (M-1 outcome `out_of_scope` mất khi gỡ nhánh định tuyến; M-2 thiếu sàn S3b agent từ chối nhầm câu Huế) + 5 minor; 0 USD. Chờ C sửa ⇒ vòng 2 (diff §12). Sau khi User duyệt: B code G.
- **Vòng 2 xong (sha `89a48ca72cbd`): `ready_for_user_confirmation`** — 7 / 7 finding vòng 1 đóng; còn 1 minor n-1 (dòng G §12.2 chưa liệt kê S3b ⇒ plan G ghi). 0 USD. Chờ A duyệt sha / User duyệt ⇒ B viết plan + code G.

## 0e. Xong 08/11 — phiếu toạ độ (`data/phase_11/ban_do/phieu_toa_do_11_diem.md` + nháp `diem_toa_do_v6_nhap.json`, chờ User tick) · review `p11-viec-nho-e` (`report_agent/2026-11-06_giao_dien_cong/b_viec_nho_e_review.md`: ready, 2 minor; tiền ≈ 0,0053 USD — vượt trần 0,005 của A ~0,0003).

# (cũ) STATUS B viết lại 15:43 07/11/2026

## 1. Đã xong 07/11 (sha trên origin)

- **S1 backend cổng đợt 1** `1c31ce4`:
  - D3 lượt biểu mẫu (code xếp bằng giá trị nút; không định tuyến / #6 / công cụ);
  - D4 cờ `lich_trinh_bieu_mau`;
  - D6 `/api/kham_pha`, `/api/kham_pha/bai`, `/api/thoi_tiet`, `/api/tinh_nang` (`backend/api/routes/cong.py`);
  - D7 `bai_id`.
- **(e)** `_lay_nguon_lich` chọn đoạn cùng file có bằng chứng dài nhất `0cb0b0a`.
- **S2 giao diện** (bản mẫu 2 Sông Hương, hash route, trợ lý nổi, dòng Nguồn, biểu mẫu) `f20fd28`.
- **3 minor review S4** `27ed091` ⇒ A merge `main` `0dab4e5` (+ bật thời tiết).
- **V5** (luật lịch trong lời dặn hệ thống + reasoning "low", chỉ lượt biểu mẫu) `632a4f7` ⇒ S3 của C đạt, User duyệt, A merge.
- **Sửa 4 test mốc cờ tắt** sau khi bật cờ `a884de4` ⇒ A merge `main`, cổng đạt.
- **B-dep** — nhánh `p12-deploy-nhap` = `4cfe681`, chưa merge (deploy chờ User):
  - biến môi trường `HUE_QDRANT_URL` / `HUE_TRA_WEB`;
  - nháp `data/phase_12/deploy_nhap/` (private): `Dockerfile` (có `--no-cache`, chưa build lại), `Dockerfile.dockerignore` **sinh bằng `dung_dockerignore.py`** (danh sách chừa 204 bài + 8 mục), `compose.yml`, `Caddyfile`;
  - ảnh sạch `hue-rag-app:nhap2` (204 .md, 0 Golden / sealed / backup — E review vòng 2 ready).
  - Ảnh cũ `hue-rag-app:nhap` (có file private): **User đã xoá 07/11**.
- **Report:** `report_agent/2026-11-06_giao_dien_cong/{s1,s2,b_v5}_implementation.md`, `report_agent/2026-11-07_tu_soi_lo_trinh/{tu_soi_B,b_dep_build_cuc_bo}.md`.

## 2. Đang chờ — việc kế của B

1. **7 ảnh cổng** — đang làm (mục 0).
2. **Deploy thật chờ User.** Khi lên máy:
   - merge `main` vào `p12-deploy-nhap` ⇒ build lại ⇒ đo lại cỡ ảnh (bản trước có cache uv 1,9 GB);
   - chạy lại `dung_dockerignore.py` nếu build record đổi;
   - đếm trong ảnh `docker run --rm --network none … find`.
   - Trước link công khai còn phải làm: giới hạn lượt / ngày, cookie `Secure`, tắt `/docs`.

## 3. Bẫy đã gặp 07/11

- Test lấy `settings.yaml` thật làm mốc "cờ tắt" ⇒ hỏng khi bật cờ ⇒ đặt rõ `OFF = flags_from(lich_trinh_bieu_mau=False)` trong test, so đúng một cờ.
- Đếm file private trong ảnh phải đếm đủ: `find … | head` từng cho số sai "0 evaluation" ⇒ dùng danh sách chừa + `wc -l` toàn ảnh (bỏ `.venv`).
- Đường mới có model ⇒ gọi thật 1 lượt (≤ 0,001 USD) ngay khi chạy được, trước khi viết bộ test.
- `huggingface_hub` 1.26 + model tải một phần ⇒ `IncompleteSnapshotError` ⇒ xoá `trees/` sau khi tải (Dockerfile đã có).
- Push từ worktree / lệnh ghép commit + push bị chặn ⇒ commit ở worktree, `git push` riêng từ repo chính. Build nhánh chưa merge: `--build-context code=<worktree>/backend`.
- Mốc Q1 đổi khi bật cờ ⇒ luôn chụp lại trên `main` hiện tại, so cùng cờ.

## 4. Tiền B 07/11 ≈ 0,0074 USD (S1 0,0041 · S2 0,0018 · B-dep 0,0011 · V5 0,0004)

## 5. Lệnh cho User

- Nhánh đã merge, xoá khi muốn: `p11-cong-dot-1`, `p11-bat-bieu-mau` (local + origin).

---

# (cũ) Chi tiết phiên 07/11 — nhật ký từng bước (tham khảo)

Vai: thực thi. Terminal 07/11: A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81`. Quyền phiên: User cấp "như 06/11" (A báo).

## Tóm tắt mới nhất (13:25 07/11/2026 `date`)
- `p11-cong-dot-1` = `632a4f7` (S1 + S2 + 3 minor S4 + V5; `27ed091` đã merge `main` `0dab4e5` bởi A). V5 chờ S3 của C + User duyệt bật cờ.
- `p12-deploy-nhap` = `4cfe681` (biến môi trường `HUE_QDRANT_URL` / `HUE_TRA_WEB` + merge `main` `fb8d3d2`; 26 test đạt), giữ riêng, chưa merge. Nháp Dockerfile thêm `uv pip install --no-cache` (E m-6) — chưa build lại, đo lại cỡ ảnh lúc lên máy. E review B-dep vòng 2: ready.
- Deploy cục bộ: ảnh `hue-rag-app:nhap2` sạch (204 .md, 0 Golden / sealed / backup), `/health` 5/5. Ảnh cũ `hue-rag-app:nhap` có file private ⇒ chờ User `! docker image rm hue-rag-app:nhap`. Report `report_agent/2026-11-07_tu_soi_lo_trinh/b_dep_build_cuc_bo.md`.
- `a884de4` (sửa 4 test mốc cờ tắt) đã merge `main` (A, cổng đạt) ⇒ biểu mẫu V5 BẬT trên `main`. Worktree `/tmp/b_cong` đã gỡ; còn `/tmp/b_dep` (p12).
- Việc chờ: User kiểm 7 ảnh Commons (2 đầu trang + 5 lĩnh vực, không ảnh thẻ bài) ⇒ B đóng ảnh vào build + dòng ghi công (`tai_ve.json`).
- **B rảnh có lý do:** deploy thật / bật biểu mẫu V5 / ảnh Commons đều chờ User. **Lệnh cho User:** `! docker image rm hue-rag-app:nhap` (ảnh cũ có file private; giữ `nhap2`).
- Tiền B phiên 07/11 ≈ 0,0074 USD (S1 0,0041 · S2 0,0018 · B-dep 0,0011 · V5 0,0004).

## Đang làm — S1 backend cổng đợt 1 (spec duyệt `ff3c317ec88b`, User 11:56 07/11; A giao)
- Nhánh `p11-cong-dot-1` từ `main` `eb68458`; worktree `/tmp/b_cong` (symlink `data/`, `knowledge-base-hue/`).
- A trả lời 3 câu (07/11): (1) `bieu_mau` trường mới; giá trị nút dùng `truong`; câu `query` cố định code dựng — B quyết; (2) Q-U3 chưa chốt ⇒ ẩn "đi dày", `kieu_di` = mặc định code; (3) S1 chỉ cần duyệt spec.
- Q-U1 = bản mẫu 2 "Sông Hương" (cho S2), không thêm font.
- **File khai báo sửa (trong worktree `/tmp/b_cong`):**
  - `backend/api/routes/chat.py` (`ChatRequest.bieu_mau`, `SourceResponse.bai_id`, nhánh biểu mẫu ở 2 route)
  - `backend/llm/assistant.py` (cờ `lich_trinh_bieu_mau`, `AnswerTrace.bieu_mau`, đường biểu mẫu trong `answer_turn` / `answer_turn_stream`, bỏ qua phần song song #6)
  - `backend/api/routes/cong.py` (mới: `/api/kham_pha`, `/api/kham_pha/bai`, `/api/thoi_tiet`, `/api/tinh_nang`)
  - `backend/api/app.py` (đăng ký route + nạp danh sách bài lúc khởi động)
  - `backend/config/settings.yaml` (cờ `lich_trinh_bieu_mau: false`)
  - test: `backend/tests/test_cong_dot_1.py` (mới), `test_api_chat.py` / `test_chat_stream.py` (khuôn `sources` nếu cần)
  - report: `report_agent/2026-11-06_giao_dien_cong/s1_implementation.md`
- Tiền S1 dự kiến 0 USD (Q1 / Q1m chụp chuỗi, không gửi).

### Tiến độ S1 (12:24 07/11/2026 `date`)
- Commit dở `1c31ce4` trên `p11-cong-dot-1` (chưa push). D4 / D6 / D7 xong; D3 code xong nhưng **dừng chờ A** (lỗi model từ chối).
- Đạt: Q1 228/228 giống byte (cờ tắt + cờ bật, mốc `main_eb68458.jsonl` sha `dba1f578eef1`); Q1m lượt biểu mẫu (1 lần gọi, 0 công cụ, chat = stream, tất định, chữ gõ không lọt) — `data/phase_11/cong_dot_1/q1/`; 20 test mới; test rộng 723 đạt (2 hỏng = test cần khoá); cổng ổn định đạt (cổng 8861).
- Vướng D3: lượt thật từ chối 5/5 (server 8862) + cách (a) "lượt công cụ dựng sẵn" 3/3 (`data/phase_11/cong_dot_1/thu_cach_a/lan1.jsonl`). Nguyên nhân: đoạn chọn cho mỗi điểm (`_lay_nguon_lich`) chỉ là dòng tên ở 11/28 điểm ⇒ luật lịch đòi "ý ngắn từ tài liệu" không có ⇒ từ chối. Đề xuất A: (e) chọn đoạn nhiều bằng chứng nhất.
- Tiền S1: 0,0028 USD.
- Script: `data/phase_11/cong_dot_1/tools/` (`q1m_bieu_mau.py`, `app_bieu_mau.py` cho S3, `thu_cach_a.py`).
- (e) xong (`0cb0b0a`, đã push): 0 điểm < 80 ký tự, Q1 228/228; pilot 1/3 model viết, 2/3 vẫn từ chối ⇒ dừng D3 theo A.

## Đang làm — S2 frontend (A giao, bản mẫu 2 Sông Hương; tên "Huế · Trải nghiệm văn hóa & du lịch" / "Trải nghiệm Huế" / "Trợ lý Huế")
- **File khai báo sửa (worktree `/tmp/b_cong/frontend/src/`):** `App.jsx` (khung cổng + điều hướng hash), `chat.jsx` (mới — trợ lý: hook + lượt + dòng Nguồn), `pages.jsx` (mới — trang chủ, Khám phá, bài, Lên kế hoạch, Giới thiệu), `route.js` (mới), `markdown.js` (bỏ số [n], link ngoài), `stream.js` (`bieu_mau`), `index.css` (token bản 2); `HoiBangAnh.jsx` chỉ nếu cần.
- **S2 xong (12:45 07/11/2026 `date`), chờ review:** commit `f20fd28` (đã push). 0 lỗi console trên 11 hash × 1440 / 390; bundle 105,99 KB gzip; lượt thật: 0 `[n]` trong chữ, dòng Nguồn = sources 6/6, biểu mẫu ⇒ lịch + "Sửa" về biểu mẫu chọn sẵn. Tiền S2 0,0018 USD. Report `report_agent/2026-11-06_giao_dien_cong/s2_implementation.md`; S1: `s1_implementation.md`. Ảnh `data/phase_11/cong_dot_1/anh_s2/`.
- Còn mở: ảnh thật (chờ User / E), D3 chờ X1 của C, server thử đã tắt. Worktree `/tmp/b_cong` giữ (nhánh `p11-cong-dot-1`).

---

# (cũ) STATUS B — KẾT PHIÊN TỐI 06/11 (22:41 06/11/2026 `date`; mở 20:54) — sổ tay cho phiên sau

Vai: thực thi. Terminal phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28` (đổi mỗi lần mở ⇒ `ListAgents`). Quyền phiên **hết hạn**. Không còn worktree `/tmp` của B. Không có code dở.

## Xong phiên tối 06/11
- **B171** sửa lỗi lịch trình: merge `main` `dbb4004` (cờ `lich_trinh` tắt; C ready `b0e52f8`). Tiền B171 0,028844 / 0,04. Nhánh `p9-b5-sua` chờ User xoá.
- **B172** nghiên cứu giao diện cổng: `data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md` (15 mẫu, 10 không nên chép) + `report_agent/2026-11-06_giao_dien_cong/b172_implementation.md`.
- **B173** 3 bản mẫu HTML tĩnh: `data/nghien_cuu_giao_dien_2026-11-06/mau/{1,2,3}.html` (1 Son thếp · 2 Sông Hương · 3 Tím Huế trầm = mốc hiện tại), 24 ảnh `mau/anh/`, bản so `mau/anh_nho/so_*.jpg`; tương phản đạt (6 chỗ dưới ngưỡng = nhãn ẩn); report `…/b173_implementation.md`. **Chưa ai soát ngoài B.**

## Việc dở / bước kế
- B173: chờ A đưa User chọn hướng. Thiếu, nếu User cần:
  - danh sách / chi tiết khác bố cục giữa 3 bản (hiện chung bố cục);
  - font tiêu đề có chân — cần thêm 1 gói `@fontsource`, chưa cài, cần duyệt;
  - ảnh thật (chưa có ảnh được phép).
  - Sinh lại: `uv run python data/nghien_cuu_giao_dien_2026-11-06/tools/dung_mau.py` rồi `chup_mau.py`, `do_tuong_phan.py`.
- Khi spec đợt 1 duyệt ⇒ B code (A giao).

## Phiên sau — S1 / S2 cổng đợt 1 (bổ sung 22:46 06/11/2026 `date`, A nhờ)
**Điều kiện bắt đầu:**
- S1 backend: User duyệt spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` sha **`ff3c317ec88b`** (`sha256sum … | cut -c1-12` — đổi sha ⇒ đọc lại).
- S2 frontend: thêm Q-U1 (bản mẫu) + Q-U2 (ảnh) + Q-U5 (tên cổng).
- Q-U3 "đi dày": mặc định ẩn. Q-U4 bật thời tiết: ô thời tiết ẩn khi cờ tắt.

**Đọc trước:**
- spec §2 D1–D14, §6 tiêu chí;
- `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` (C211: mỗi ý có `file:hàm`);
- bản mẫu User chọn (`mau/<n>.html`, sinh từ `tools/dung_mau.py`).

**Nhánh:** `p11-cong-dot-1` từ `main` mới nhất, worktree `/tmp/b_cong` (symlink `data/`, `knowledge-base-hue/`; `npm ci && npm run build` trong `frontend/` của worktree).

**S1 — file / hàm sẽ sửa (dự kiến, đối chiếu C211 trước khi code):**
- `backend/api/routes/chat.py`:
  - `ChatRequest` thêm `bieu_mau` (D3) — kiểm ghép với `truong: TruongInput` (B4) đã có;
  - `SourceResponse` + `_source_responses` thêm `bai_id` (D7);
  - đường `/api/chat` + `/api/chat/stream` rẽ nhánh khi `bieu_mau`.
- `backend/llm/assistant.py`:
  - nhánh biểu mẫu: bỏ `_pick_route`, code gọi phần xếp của `lich_trinh_for_turn` (`lt.xep` + `_lay_nguon_lich` + `khung_chu`) với giá trị nút ở **cả 4 trường**, rồi sinh **không công cụ**;
  - `_finish_generated` giữ kiểm cuối D8 + T3 (b) `chu_thay`;
  - `AssistantFlags` + `BOOL_FIELDS` thêm `lich_trinh_bieu_mau` (D4).
- `backend/config/settings.yaml` (cờ, tắt).
- Route mới D6 trong `backend/api/routes/` + đăng ký ở `backend/api/app.py` `create_app`: `/api/kham_pha`, `/api/kham_pha/bai`, `/api/thoi_tiet` (`llm/thoi_tiet.py` `lay_du_bao`), `/api/tinh_nang`.
- Test:
  - mọi tổ hợp nút (Q-F phần tất định), 404 cho id lạ / `..` / `evaluation/` / `sealed`, khuôn JSON có `bai_id`;
  - khoá tập trường `chat_metrics` (`test_api_chat.py`) nếu thêm trường log.
- Kiểm: Q1 228 / 228 giống byte (`capture_all.py`, cờ mới tắt) + Q1m (cờ `lich_trinh_bieu_mau` bật).

**S2:** `frontend/src/App.jsx` (tách trang theo hash D5), `markdown.js` (bỏ số `[n]` ⇒ dòng Nguồn D1; link ngoài `rel="noopener noreferrer"` D11), `index.css` (token theo bản mẫu), `stream.js`.
- Đo Q-G tương phản: dùng lại `data/nghien_cuu_giao_dien_2026-11-06/tools/do_tuong_phan.py` (đo chữ thật trên trang; trỏ vào bản build thay file mẫu).
- Bundle gzip ≤ 200 KB.

**Bẫy đã thấy khi đọc spec / code (chưa code):**
- Cờ **#6 `song_song_tra_loi` đang BẬT**: route stream đi qua `answer_turn_stream_parallel` (chạy trước phần trả lời cùng lúc định tuyến). Nhánh biểu mẫu phải rẽ **trước** đường song song (không định tuyến, không chạy trước).
- Hiện khung lịch tới model qua **kết quả công cụ** `lich_trinh` (gồm `LICH_TRINH_LUAT`). Lượt biểu mẫu "không công cụ" ⇒ khung + luật phải vào ngữ cảnh / tin nhắn do code dựng. Đổi chuỗi gửi model khi cờ bật ⇒ cần test mỗi loại lượt (`WORKFLOW.md` §4 (4c)).
- 4 bài nằm ngay gốc lĩnh vực (file hướng dẫn chung của 4 lĩnh vực festivals / foods / heritages / performing_arts — tên ở `corpus.sources`) ⇒ không có "loại con" theo thư mục cấp 2 (D10). `travel` không có bài gốc. `corpus.sources` là dict 204 khoá dạng `<lĩnh vực>/<loại>/<tên>.md`.
- Câu `query` cố định do code dựng từ nút: không được khớp `hoi_buoi_toi` nhầm. Biểu mẫu không có trường buổi tối ⇒ `hoi_toi` false.
- `frontend/dist/` không commit; `test_static_ui` cần bản build trong worktree.

**Câu hỏi / thắc mắc cho A (hỏi khi bắt đầu S1):**
1. D3 dùng lại `truong` (TruongInput, 4 trường B4) + `bieu_mau: true`, hay trường riêng? Câu `query` cố định dựng bằng `ghep_cau` B4 hay câu mới?
2. Lượt biểu mẫu khi `kieu_di` bị ẩn (Q-U3) ⇒ `kieu_di = None` (giả định "thong thả" do code nối như hiện nay) — đúng ý spec?
3. Thứ tự spec §5 / handoff mục 3 ghi "S1 sau khi User duyệt spec **+ chọn bản mẫu**", nhưng đoạn "Mặc định đã ghi trong spec" nói S1 chỉ cần duyệt spec ⇒ B hiểu: S1 chạy ngay khi spec duyệt, S2 chờ Q-U1 / Q-U2 / Q-U5.

## Tiền B phiên tối 06/11: 0,010975 USD (chỉ B171: M-1 0,002843 + T3 0,002337 + dòng tối 0,003915 + T5 / T5b 0,00188); B172 / B173 0 USD.

## Bẫy mới phiên tối
- Ảnh cả trang (Playwright `full_page`) vẽ phần tử `position: fixed` (nút nổi, thanh dưới) chồng giữa trang — xem vị trí thật bằng ảnh màn đầu.
- Đo tương phản: nhãn `.sr` (1 px) báo dưới ngưỡng — bỏ qua.
- Câu thử tự viết cho lịch trình phải có ý "lên lịch" rõ, nếu không model trả lời thẳng, không gọi `lich_trinh` (T5 phiên tối).
- Không `uv sync` ở `main` (gỡ sherpa-onnx của E).

## Sổ tay (từ phiên sáng 06/11, còn đúng)

## Dựng lại worktree (máy khởi động lại ⇒ `/tmp` mất)
- `git worktree prune`; `git worktree add /tmp/b_b5sua p9-b5-sua` (hoặc `/tmp/b_b5b p9-b5b`); trong worktree: `ln -s /home/minhhieu/hue_rag/data data && ln -s /home/minhhieu/hue_rag/knowledge-base-hue knowledge-base-hue`. Không đụng 4 worktree AGY (`~/.gemini/…`).
- Giao diện (`test_static_ui`, Playwright): `cd frontend && npm ci && npm run build` trong worktree.
- So bản cũ ↔ mới (`so_khung_cu_moi.py`): `mkdir -p /tmp/b171_cu/llm && git show main:backend/llm/lich_trinh.py > /tmp/b171_cu/llm/lich_trinh_cu.py`.

## Lệnh hay dùng (từ `backend/` của worktree, `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag …`)
- Q1: `env -u OPENAI_API_KEY -u SERPER_API_KEY OPENAI_API_KEY=capture-only … python ../data/phase_9/b2_chay/tools/capture_all.py <out>` ⇒ `cmp` với `../data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl` (sha `dba1f578eef1`; `main` sau đó chỉ đổi tài liệu).
- B5 có phí: `--env-file /home/minhhieu/hue_rag/.env python ../data/phase_9/b5/tools/chay_b5.py chay <bo> <out> [--chi id …]`; đếm `… dem <bo> <out>` (0 USD). Không ghi đè file cũ.
- B5b server: `B5B_API=<file> uvicorn --factory --app-dir /home/minhhieu/hue_rag/data/phase_9/b5b/tools app_thoi_tiet:make_app --port 8851`; `chay_b5b.py <BASE> <out> <log> --lan N --chi F03,F07`; `q8_b5b.py ui …`.
- B171 0 USD: `data/phase_9/b171/tools/tai_tao_la.py` (quét 120 tổ hợp), `so_khung_cu_moi.py` (1.728 tổ hợp cũ ↔ mới), `chay_khong_dong_toi.py` (biến thể bỏ dòng khung — có phí).
- Test rộng không key: mọi file `tests/*.py` trừ `test_phase6_live_smoke`, `test_openai_full_corpus_generator`, `test_startup_model_missing` ⇒ 2 hỏng đúng là test cần key.

## Tiền B phiên sáng 06/11 (USD) — tổng ≈ 0,0214
- B5b ≈ 0,0035 (Q8 0,00086 · đo lại F03 / F07 × 2 0,00266) ⇒ **B5b tổng ≈ 0,0544 / 0,07**.
- B171 0,017869 (17 câu 0,011375 · T3 thêm 6 lượt 0,006494) / trần **0,04**.

## Bẫy — đọc trước khi làm
- Chọn trước buổi sáng đã từng làm rơi điểm người dùng nêu (Bạch Mã) ⇒ điểm người dùng nêu luôn đứng trước; test `test_branches_of_the_plan` bắt được.
- Kiểm "nói ngược" theo từ dễ bắt nhầm lời khuyên nghỉ (C dò: 5 / 10) ⇒ luật rút lại cả câu chỉ nên bắt khi có **tên điểm** — lượt có phí 4 câu không đủ thấy bắt nhầm.
- Câu hỏi có / không về phần lịch không xếp ⇒ model trả nguyên câu từ chối kho (7 / 7) — đổi chữ dòng khung không giúp.
- Stream: chữ model phát dần ⇒ muốn thay chữ model phải giữ chữ chừng nào còn là khúc đầu câu từ chối (`giu_chu` B5b).
- Dặn cũ vẫn đúng: lệnh `git push` tách riêng (auto mode chặn khối ghép); push nhánh đã rebase ⇒ `--force-with-lease=<nhánh>:<sha cũ>`; báo cáo có backtick ⇒ `python3 - <<'PYEOF'`; chờ nền bằng `run_in_background` (không `pgrep -f`); tắt server bằng TaskStop; giờ lấy từ `date`; không gọi `agy`; không mở câu kín (`data/phase_9/b5/kin/`, `data/phase_9/b5_v2/`, `bo_do_b5/cau_sealed.jsonl`).
