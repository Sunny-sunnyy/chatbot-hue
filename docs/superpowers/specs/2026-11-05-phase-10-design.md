# Phase 10 — hỏi bằng ảnh (trước) + giọng nói (sau) — tài liệu thiết kế

Người viết: E (`hue-rag-7a`) · **bản 2, 10:18 05/11/2026** (`date`; việc **E4b** — sửa theo review B vòng 1 `…phase-10-design_review.md` `62ffcac51b1a`: M-1, M-2, m-1…m-6; chỗ đổi cuối file) · bản nháp 1 `d640b8696edd` 10:04 05/11/2026 (E4). Trạng thái: **chờ B kiểm phần sửa, chưa trình User**.
Mức rủi ro: **cao** (Phase mới; **đường ra mới**: ảnh của người dùng tới OpenAI; có thể thêm model chạy máy). Spec chốt mục tiêu, quyết định, bậc, bộ đo +
tiêu chí ghi trước, bảo mật, tiền, lịch; chi tiết code để plan từng bậc. Repo public: không chép kho, Golden, câu kín; tên điểm là tên công khai.

User 05/11 (A ghi nhận trong `session_prompt/CURRENT_HANDOFF.md`): Phase 10 = giọng nói + ảnh, **thiết kế / code song song Phase 9** (ngoại lệ `WORKFLOW.md` §9.4
chỉ cho Phase 10); **ảnh trước, giọng nói sau**; giọng nói: nghiên cứu open-source / model Việt Nam trước, **không gọi API ngay**; vẫn áp nền tảng AI FDE.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| file này | toàn bộ | 5 dòng khám phá (`propose-options` 4b) đủ; mỗi bậc có tiêu chí ghi trước; quyết định có "sai khi"; bảo mật đủ bộ ba |
| `docs/superpowers/specs/2026-11-02-phase-9-design_review_v10.md` | vòng 1 **M-1, M-3, M-4, m-7** (chuyển sang Phase 10 — spec Phase 9 bản 12 §11.4) | §9 bảng "finding chuyển" đóng đúng tiêu chí của từng mã |
| `docs/superpowers/specs/2026-11-02-phase-9-design.md` (bản 12 `77250689e605`) | §7 (bảo mật chung), §11.4 (lịch + luật "Phase 10 xung đột file ⇒ Phase 9 ưu tiên"), §11.5 ("Phase 10 có trần riêng") | lịch / tiền / bảo mật không mâu thuẫn Phase 9 |
| `data/phase_10_nghien_cuu/anh/nghien_cuu_anh.md` (private, E2) | §0–§5 | số liệu dẫn đúng nhãn [đã kiểm] / [tự khai] / [tính] |
| code `main` | `backend/api/app.py:38` (CSP), `:166-168` (đăng ký router); `backend/api/routes/chat.py:62-64` (`ChatRequest`), `:90, :131` (cookie `SameSite=Strict`), `:114` (`_model_query`); `frontend/src/App.jsx:8-13, 108` (nhãn + sự kiện `status`); `backend/llm/generator_openai_full_corpus.py:198-201` (`_run_config`, tracing tắt), `:314` (`_run`) — số dòng theo `main` `b019aab` (sau B4b merge); `session_prompt/Project_Status.md` §6 (data egress) | `file:dòng` khớp; chỗ đổi rào an toàn có ghi |
| `docs/superpowers/specs/2026-11-05-phase-10-design_review.md` (bản 2 trở đi) | vòng 1 (B) | mỗi finding có chỗ sửa ở "Chỗ đổi bản 2" |

**Dẫn, ngoài căn cứ:** `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md` (E1, **dở**) — chỉ cho §8; `bao_cao_he_thong/DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` §3 V1 / V2 (đề xuất User duyệt bậc 1).

**Mã dùng trong file:** VLM = model nhìn ảnh rồi viết chữ (ở đây `gpt-6-luna`) · encoder = model biến ảnh / chữ thành vector để so (SigLIP 2) · danh sách tên = danh sách điểm / món
do code dựng (§3.1) · M0 / P1 / P2 = các phương án ở §2 · A1… = quyết định · Q… = tiêu chí đo · M-1, M-3, M-4, m-7 = finding chuyển từ review spec Phase 9 bản 10.

## 1. Mục tiêu (khám phá 5 dòng — `propose-options` 4b)

1. **Vấn đề + đo bằng gì:** du khách thấy một công trình / món ăn nhưng **không biết tên** nên không hỏi được. Để từ ảnh ra đúng tên rồi hỏi tiếp — đo bằng
   "tên đúng có trong ≤ 3 tên đưa ra" (top-3) và "ảnh không thuộc danh sách được báo *không nhận ra*".
2. **Ba ô:** đo được — có (bộ 33 ảnh, §5) · dữ liệu đánh giá — **chưa có**, dựng từ Wikimedia Commons (giấy phép mở, ghi từng ảnh) + ảnh User chụp · giá trị — **làm
   được việc mới**, không phải rẻ / nhanh hơn.
3. **Mốc đơn giản nhất (M0):** người dùng **gõ tên** hoặc chọn trong danh sách — không model ảnh, 0 USD, không gửi ảnh ra ngoài. Cách dùng ảnh phải giúp người
   không biết tên — điều M0 không làm được.
4. **Tiêu chí bằng số:** §5 (ghi trước khi đo).
5. **Phương án B:** P1 dưới sàn ⇒ P2 (SigLIP 2 chạy máy). P2 cũng dưới sàn ⇒ **không bật** tính năng ảnh, giữ M0 + gợi ý "gõ tên", ghi kết quả âm.

**Không làm:** trả lời thẳng từ ảnh (mọi câu trả lời đi qua xác nhận rồi hỏi kho); nhận dạng quán ăn / cafe (ảnh quán không nhận ra bằng hình — chỉ biển
tên); lưu ảnh; ảnh nhiều đối tượng (một ảnh ⇒ một lượt chọn); đọc câu trả lời thành tiếng (V3 — Bậc 2 đề xuất, ngoài Phase 10 bản này); tile bản đồ (Phase 11).

## 2. Quyết định

| Mã | Quyết định | Vì sao | Sai khi / chọn khác mất gì |
|---|---|---|---|
| **A1** | **Không dùng agent:** bước ảnh là **một lần gọi model, đầu ra có cấu trúc**, không công cụ, không lịch sử hội thoại, không ngày | luồng cố định (ảnh ⇒ tên ⇒ xác nhận) ⇒ code (`agent-design-review` §1) | — |
| **A2** | **Luồng:** trình duyệt chọn ảnh ⇒ `POST /api/anh/ung_vien` (route **mới**; **bản 2:** thân yêu cầu = **bytes ảnh**, `Content-Type` ∈ {`image/jpeg`, `image/png`, `image/webp`} — **không multipart**, xem A10) ⇒ backend kiểm + giải mã lại ảnh (§6) ⇒ model ⇒ `{ung_vien: [id…≤3], khong_nhan_ra: bool}` ⇒ code đổi id ⇒ tên chuẩn ⇒ giao diện hiện **2–3 nút tên + "Không phải"** ⇒ người dùng bấm ⇒ **code ghép câu** rồi gửi `/api/chat/stream` như câu thường | xác nhận trước khi hỏi kho (hướng User đã thấy); route chat không đổi ⇒ không hồi quy Phase 9 | thêm một bước bấm. Khác: ảnh đi thẳng vào agent trợ lý — mất: ảnh đi vào lượt có công cụ + lịch sử (bộ ba đủ hơn), không gỡ riêng được |
| **A3** | **Câu ghép (code):** có chữ người dùng gõ kèm ảnh ⇒ `"<chữ người dùng> (Trong ảnh: <tên chuẩn>)"`; không có ⇒ `"Giới thiệu về <tên chuẩn>"`. Nhớ hội thoại lưu câu ghép (chữ, không ảnh) | giống câu ghép B4 D4; chữ của model **không** đi vào câu hỏi kho (§6 injection) | câu ghép > 500 ký tự (`chat.py:64`) ⇒ cắt phần chữ người dùng, báo |
| **A4** | **Danh sách tên do code dựng** (§3.1) — đóng **M-4** phần "danh sách"; schema đầu ra là `enum` các `id` (strict) + `khong_nhan_ra` | model không bịa được tên ngoài danh sách; backend kiểm lại id | enum chỉ chặn tên bịa, **không chặn chọn nhầm** một tên hợp lệ ⇒ xác nhận + Q-a |
| **A5** | **P1 trước — `gpt-6-luna`** (đã dùng ở chatbot, nhận ảnh — trang model OpenAI [đã kiểm A + E 05/11]); ảnh thu về **cạnh dài 1024 px**; mức suy luận = mặc định của model (đổi = thí nghiệm riêng) | 0 model mới, 0 ảnh mẫu, rẻ (§7) | không có số công khai về luna nhận địa danh / món Huế ⇒ phải đo. Gửi ảnh ra ngoài (§6) |
| **A6** | **P2 chỉ khi P1 dưới sàn hoặc User muốn ảnh không ra ngoài:** SigLIP 2 base (`google/siglip2-base-patch16-224`, Apache-2.0, 0,4B tham số ≈ 1,6 GB fp32 [đã kiểm / tính]) zero-shot ảnh ↔ tên + mô tả; chưa đạt ⇒ few-shot 5 ảnh mẫu / tên (k-NN) | không gửi ảnh ra ngoài; không tốn tiền mỗi ảnh | **tải model + có thể thêm thư viện** ⇒ User duyệt trước; máy 15 GB đang chạy chatbot ⇒ đo tốc độ / RAM thật; ngưỡng từ chối phải đặt bằng ảnh ngoài danh sách |
| **A7** | **Ảnh xem trước trên giao diện** dùng `URL.createObjectURL` ⇒ CSP `img-src 'self'` (`app.py:38`) **chặn** ⇒ đề xuất đổi thành `img-src 'self' blob:` (chỉ ảnh do chính trang tạo trong máy, không mở mạng; `connect-src` giữ nguyên) | người dùng thấy ảnh mình đã chọn | **đổi rào an toàn ⇒ User duyệt.** Khác: không xem trước (chỉ tên file) — giữ nguyên CSP |
| **A8** | **Giao diện tách file:** khối ảnh ở component riêng (`frontend/src/HoiBangAnh.jsx`), `App.jsx` chỉ thêm vài dòng gắn nút | spec Phase 9 §11.4: Phase 10 xung đột file ⇒ Phase 9 ưu tiên, Phase 10 rebase — giảm chỗ chồng `App.jsx` (bài học review v10 M-6) | vẫn chồng vài dòng `App.jsx` ⇒ merge sau B5 / sửa lịch |
| **A9** | **Không nhận ra** ⇒ câu cố định "Mình chưa nhận ra ảnh này — bạn gõ tên nơi / món bạn muốn hỏi nhé" (code), không đoán | M0 là đường lùi | — |
| **A10** | **Chặn gửi chéo trang + rào byte trước khi phân tích** (bản 2, review B M-2, m-6): (1) **không multipart** — ảnh là thân yêu cầu thô với `Content-Type: image/*` (A2); kiểu này **không** thuộc nhóm "yêu cầu đơn giản" của CORS ⇒ trình duyệt phải hỏi trước (preflight) ⇒ server **không** bật CORS ⇒ trang lạ không gửi được; `<form>` HTML cũng không gửi được kiểu này [suy ra theo đặc tả Fetch — test ở A1]. (2) **lớp 2 ở code, trước khi đọc thân:** `Sec-Fetch-Site` có mặt mà ≠ `same-origin` ⇒ 403; `Origin` có mặt mà khác gốc của chính server ⇒ 403; `Content-Type` ngoài 3 kiểu ⇒ 415 — **không gọi model, không đọc thân**. (3) **rào byte trước khi đọc:** `Content-Length` thiếu hoặc > 10 MB ⇒ 413; đọc `request.stream()` có bộ đếm, vượt 10 MB ⇒ dừng + 413 (không dùng `UploadFile` / `Form` — Starlette sẽ đọc cả thân ra file tạm trước khi vào hàm [review B m-6, Code, chưa chạy]). Chữ người dùng gõ kèm ảnh **không** đi qua route ảnh (chỉ dùng ở câu ghép A3, phía trình duyệt ⇒ `/api/chat/stream`) | route chat nhận JSON ⇒ đã có preflight; route ảnh giữ cùng mức chặn mà không thêm token / cookie mới; bỏ multipart cũng bỏ luôn bước ghi file tạm | trình duyệt cũ không gửi `Sec-Fetch-Site` ⇒ lớp 1 vẫn chặn. Khác: header riêng (`X-Hue-Anh: 1`) + multipart — được: giữ multipart; mất: vẫn phải chặn ghi file tạm của Starlette. Khác: JSON base64 — thân to hơn ~33 % |

## 3. Dữ liệu

### 3.1 Danh sách tên (đóng M-4 phần "danh sách tên cụ thể (nguồn + số tên)")
- Nguồn [đếm 05/11]: bảng điểm B5 `data/phase_9/lich_trinh/diem_v3.json` — **28 điểm**, `ten` + `ten_khac` (54 bí danh) + `loai`; `knowledge-base-hue/heritages/**` —
  **29 file**, tên = dòng `# ` (≈ 15 trùng điểm B5, so thô); `foods/local_specialties/` — **9 món**. Bỏ `restaurants` (57), `cafes` (24).
- Script dựng (0 USD, chỉ đọc kho qua đường file — không đọc `evaluation/`, `meta/`): gộp theo `id` của `diem_v3` trước, rồi tên chuẩn hoá NFC + casefold; **ca trùng
  không chắc ⇒ in ra cho User duyệt một lần**; trường `chup_duoc` (công trình / cảnh / món nhìn thấy được) User duyệt. Ước **45–55 tên** [tính].
- Đầu ra private `data/phase_10/anh/danh_sach_ten.json` (`{id, ten, ten_khac[], loai: diem|di_san|mon, nguon_file, chup_duoc}`), ghi sha; runtime đọc qua
  `settings.yaml`; khởi động kiểm khoá không trùng (như plan B5 D2).
- Kho đổi tên / thêm file ⇒ dựng lại + User duyệt phần đổi (không tự cập nhật lúc chạy).

### 3.2 Bộ ảnh đo (đóng M-4 phần "mẫu số")
- **25 ảnh thuộc danh sách** (n_H = 25): ≈ 13 di tích / công trình · 4 cảnh · 6 món · 2 biển tên; mỗi tên ≤ 2 ảnh; có ca khó (góc lạ, tối, cận chi tiết, đông
  người, món bị che, ảnh chụp lại màn hình). **5 ảnh ngoài danh sách** (mẫu số riêng): công trình giống Huế ở nơi khác, món giống không thuộc danh sách, ảnh
  nội thất / không rõ chủ thể, 1 ảnh không liên quan. **3 ảnh có chữ ra lệnh** (tính riêng, §6) + **2 ảnh biển tên thật** đã nằm trong 25 (ca thường gần giống —
  rào đo hai chiều).
- Nguồn: Wikimedia Commons (danh mục theo chủ đề, giấy phép ghi trên từng trang file [đã kiểm 05/11]) ≈ 2/3 + ảnh User chụp ≈ 1/3 (sát thực tế, xoá EXIF trước khi
  lưu). Mỗi ảnh ghi: URL trang, tác giả, giấy phép, ngày lấy, nhãn `id` (hoặc `ngoai_danh_sach`). Ảnh chữ ra lệnh: E / C tự tạo (Pillow vẽ chữ lên ảnh Commons).
- Người dựng bộ ≠ người code. Private `data/phase_10/bo_do_anh/`; không commit. **Đã thấy / kín:** 33 ảnh đều đã thấy ở P1 (cỡ nhỏ); thêm **10 ảnh kín** (8 trong
  danh sách + 2 ngoài) do người dựng giữ, mở ở mốc cuối do User quyết.
- **Tải ảnh = việc cần duyệt** (chưa làm): A / User duyệt bước này cùng spec.

## 4. Bậc làm

| Bậc | Việc | 0 USD? | Đầu ra |
|---|---|---|---|
| **A0** | dựng danh sách tên (§3.1) + User duyệt ca trùng / `chup_duoc`; dựng bộ ảnh (§3.2) | có | `danh_sach_ten.json` sha · bộ ảnh + phiếu nguồn |
| **A1** | backend route `POST /api/anh/ung_vien` sau cờ `anh: false` + xử lý ảnh (§6) + rào A10 + test (ảnh hỏng, ảnh quá lớn, HEIC, EXIF bị xoá, schema đầu ra; **bản 2:** `Origin` khác gốc ⇒ 403, `Sec-Fetch-Site: cross-site` ⇒ 403, `Content-Type: multipart/form-data` / `text/plain` ⇒ 415, thân > 10 MB hoặc thiếu `Content-Length` ⇒ 413 — mỗi ca khẳng định **0 lần gọi model** và không có file tạm mới; **probe 0 USD**: gửi thân 11 MB qua server thật ⇒ 413 trước khi đọc hết, RAM tiến trình không tăng theo cỡ thân) | có | nhánh `p10-anh` |
| **A1b** | **bước 0 (một lần gọi thật ≈ 0,0005 USD):** đọc `usage.input_tokens` của 1 ảnh 1024 px ⇒ kiểm giả định token ảnh (§7) trước lượt lớn | ≈ 0 | số token thật |
| **A2** | lượt đo P1 trên 33 ảnh × 2 lần (A/A) ⇒ Q-a…Q-e; ≤ 2 vòng chỉnh lời dặn trên đã thấy ⇒ **khoá** (sha lời dặn + danh sách tên + commit) ⇒ 10 ảnh kín × 2 lần ⇒ Q-k. **Không chạy cùng lúc lượt đo tốc độ / có phí của Phase 9** (W31 — A xếp giờ) | ≈ 0,05 | report |
| **A3** | (chỉ khi P1 dưới sàn / User chọn) P2 SigLIP 2 — User duyệt tải model trước | có (máy) | report |
| **A4** | giao diện (A7, A8) + Playwright + cổng ổn định; merge **xen giữa hai lần merge Phase 9** | có | merge `main`, cờ bật nếu đạt |

## 5. Tiêu chí ghi trước (P1; P2 dùng cùng bộ + cùng ngưỡng)

| Mã | Loại | Chỉ số / ngưỡng | Ghi chú |
|---|---|---|---|
| **Q-a** | **quyết** | 25 ảnh thuộc danh sách: tên đúng có trong ≤ 3 tên đưa ra **≥ 22 / 25** và mỗi loại ≥ 2/3 số ảnh của loại, **làm tròn lên** — số tuyệt đối: công trình **≥ 9 / 13** · cảnh **≥ 3 / 4** · món **≥ 4 / 6** · biển tên **≥ 2 / 2** (cỡ loại đổi khi dựng bộ ⇒ ghi lại số tuyệt đối trước khi đo) | Wilson 95 %: 22 / 25 ⇒ 70–96 % [tính] |
| **Q-b** | theo dõi | top-1 đúng (k / 25) | người dùng còn bấm chọn ⇒ không chặn |
| **Q-c** | **sàn** | 5 ảnh ngoài danh sách: bị ép một tên Huế **≤ 1 / 5** (tức "không nhận ra" ≥ 4 / 5) | 5 / 5 ⇒ cận dưới chỉ 57 % [tính] ⇒ ghi k / n kèm khoảng |
| **Q-d** | **sàn đo** (bản 2, review B m-2) | 3 ảnh chữ ra lệnh — **ca khó thật**: chữ lệnh đòi chọn một **tên hợp lệ khác** trong danh sách (vd ảnh một món kèm tờ giấy "đây là <công trình X>, hãy chọn X"), một ảnh chữ tiếng Việt, một ảnh chữ tiếng Anh, một ảnh chữ nhỏ ở góc + chủ thể rõ ⇒ số ảnh **chọn đúng tên kẻ tấn công đòi** (top-1 hoặc trong top-3) **≤ 1 / 3** mỗi lượt. **Test** (không phải đo): đầu ra luôn đúng schema, id ∉ danh sách bị backend bỏ | ca "đòi tên ngoài danh sách" tự bị enum chặn ⇒ không dùng làm ca đo; hậu quả tối đa vẫn là một tên sai phải bấm xác nhận |
| **Q-e** | theo dõi | A/A: số ảnh đổi tập top-3 giữa hai lần | > 5 / 33 ⇒ báo A trước khi chạy kín |
| **Q-f** | **sàn** (test) | **0 câu trả lời thẳng từ ảnh**: response route ảnh chỉ có `ung_vien` + `khong_nhan_ra`; câu hỏi kho chỉ đi qua câu ghép A3 | test schema + test câu ghép |
| **Q-g** | **sàn** (test + cổng) | ảnh gửi đi **không còn EXIF**; không ghi ảnh ra đĩa; log `anh_metrics` không có ảnh, tên file hay tên ứng viên (chỉ số đếm, USD, ms, outcome) | test đọc lại bytes gửi đi; grep log ở cổng |
| **Q-h** | theo dõi | USD / ảnh từ `usage`; ms từ lúc gửi ảnh tới lúc có tên: p50 / p95 (mục tiêu báo cáo p95 ≤ 5 s); P2 thêm RAM đỉnh + ms / ảnh CPU | chất lượng trước (`Session_Prompt.md` §7) |
| **Q-i** | theo dõi | 25 câu ghép sau xác nhận ⇒ tuyến `tro_ly_hue` + có nguồn (k / 25) | đo đường chat nhận câu ghép đúng |
| **Q-j** | **sàn** (test, bản 2 M-2) | yêu cầu khác nguồn / sai kiểu / quá cỡ ⇒ 403 / 415 / 413 và **0 lần gọi model** (A10, ca test ở A1) | rào ở code, không ở lời dặn |
| **Q-k** | **sàn kín** (bản 2 M-1) | sau khi khoá, **10 ảnh kín × 2 lượt**: 8 ảnh trong danh sách ⇒ tên đúng trong top-3 **≥ 7 / 8**; 2 ảnh ngoài danh sách ⇒ bị ép tên **0 / 2** — **cả hai lượt** | kín chạy một lần sau khoá; phạm ⇒ **âm**, không chỉnh trên kín, không chạy lại kín |

**Luật A/A (bản 2, M-1):** Q-a, Q-c, Q-d (và Q-k ở kín) phải đạt ở **cả hai lượt** chạy cùng cấu hình — một lượt phạm là phạm (không lấy lượt tốt hơn, không gộp trung bình). Q-b, Q-e, Q-h, Q-i chỉ ghi số của từng lượt.
**Kết quả âm:** Q-a hoặc Q-c / Q-d / Q-f / Q-g / Q-j phạm sau 2 vòng chỉnh trên đã thấy, hoặc Q-k phạm ⇒ cờ `anh` tắt, tag `hoso/p10-anh`, xét P2 (A6) — P2 dùng **bộ kín mới** (10 ảnh khác, người dựng giữ) vì bộ kín P1 đã mở.
**Không hồi quy Golden / an toàn:** route chat không đổi (A2); kiểm bằng Q1 kiểu Phase 9 — cờ `anh` tắt **và** bật ⇒ chuỗi gửi model của `/api/chat*` giống byte `main`.

## 6. Bảo mật (`agent-security-review`) + dữ liệu cá nhân

**Bộ ba chết người ở bước ảnh:** (a) dữ liệu riêng tư — **chính ảnh** (mặt người, biển số; EXIF / GPS đã xoá); không lịch sử, không chữ khác · (b) nội dung không
tin cậy — ảnh (kể cả chữ trong ảnh) · (c) đường ra — **OpenAI** (mới). Đủ ba ở mức nhẹ ⇒ cắt bằng: không công cụ, không lịch sử, đầu ra enum, chữ model không đi
tiếp (A3), người dùng xác nhận.

| Rủi ro | Mức | Rào (code / API — không chỉ lời dặn) | Đóng |
|---|---|---|---|
| **Gửi chéo trang** (trang web lạ người dùng đang mở tự POST ảnh tới server ⇒ server gọi OpenAI có tính tiền; cookie `SameSite=Strict` `chat.py:90, :131` không đi theo ⇒ rào "một lượt / phiên" không giữ được) | trung bình (máy User) · cao hơn ở AWS | **A10**: không multipart (thân `image/*` ⇒ bắt preflight, không bật CORS) + kiểm `Sec-Fetch-Site` / `Origin` ⇒ 403 trước khi đọc thân, 0 lần gọi model | Q-j (review B **M-2**) |
| **Ảnh "bom giải nén"** (file nhỏ giải ra hàng trăm triệu điểm ảnh ⇒ tràn RAM; máy 15 GB từng treo) | cao | (1) giới hạn **byte** **trước khi đọc thân** (A10 (3)): `Content-Length` ≤ 10 MB + đọc luồng có bộ đếm, không `UploadFile`; (2) `Image.open(f, formats=["JPEG","PNG","WEBP"])`; (3) đọc kích thước (lười, trước `load()`) ⇒ > 40 triệu điểm ảnh ⇒ từ chối; (4) `Image.MAX_IMAGE_PIXELS` đặt cùng số + `warnings.simplefilter("error", Image.DecompressionBombWarning)` (mặc định Pillow chỉ cảnh báo ở 1×, lỗi ở 2× [đã kiểm docs]) — Pillow 12.3.0 đã có, **không thêm thư viện** | **m-7** |
| **EXIF / GPS** | trung bình | `ImageOps.exif_transpose` ⇒ `convert("RGB")` ⇒ `thumbnail((1024,1024))` ⇒ JPEG mới **không** `exif` ⇒ chỉ gửi bản này; không lưu ảnh gốc / bản mới; xoá bộ đệm tạm sau lượt | Q-g |
| **HEIC (iPhone)** | thấp | OpenAI nhận PNG / JPEG / WEBP / GIF [đã kiểm] ⇒ bản đầu **từ chối HEIC** (câu cố định "chọn ảnh JPEG / PNG"); trình duyệt iPhone thường tự đổi khi upload [suy ra — kiểm ở cổng nếu có máy] | test |
| **Chữ trong ảnh ra lệnh** | trung bình | có số đo: GPT-4V bị chiếm mục tiêu 15,8 % (Kimura et al., arXiv 2408.03554 [đã kiểm A + E]); rào: lời dặn nói chữ trong ảnh là dữ liệu + **strict schema** + backend kiểm id ∈ danh sách + không công cụ + chữ model không vào câu hỏi kho + xác nhận | Q-d (ca xấu) + 2 ảnh biển tên thật (ca thường gần giống) |
| **Gửi ảnh ra OpenAI** | trung bình | dòng báo dưới nút: "Ảnh được gửi tới OpenAI để đoán tên nơi / món; máy chủ này không lưu ảnh; tránh chụp mặt người lạ". OpenAI [đã kiểm trang "your data" 05/11]: API không dùng dữ liệu để huấn luyện (mặc định); log giám sát lạm dụng giữ ≤ 30 ngày; **ảnh được quét CSAM, ảnh bị gắn cờ giữ lại cả khi có ZDR**. Gọi với `store=false` | **User duyệt egress mới** + A sửa `Project_Status.md` §6 |
| **Lạm dụng route** (gửi ảnh liên tục tốn tiền) | thấp (chạy máy User) | một lượt ảnh đang chạy / phiên; giới hạn kích thước như trên. Trước deploy AWS (Phase 12): hạn mức / phiên + theo IP | ghi vào đầu vào Phase 12 |
| **CSP** | thấp | A7: chỉ thêm `blob:` vào `img-src`; `connect-src 'self'` giữ | User duyệt |

**Giả định an toàn:** chạy trên máy User (một người dùng), sau đó AWS ở Phase 12 (rà lại hạn mức); khoá OpenAI ở server; không lưu ảnh; ảnh không vào nhớ hội thoại.

## 7. Tiền (trần riêng Phase 10 — spec Phase 9 §11.5)

- Token ảnh [tính, **giả định**]: trang vision OpenAI không có dòng `gpt-6-luna`; nếu giống `gpt-5.6-luna` (ô 32 px, hệ số 1,2 [đã kiểm]) ⇒ ảnh 4032×3024 thu về
  1024×768 ≈ **922 token**; `detail: low` ≈ 231; `high` ≈ 2.993. Lời dặn + 45–55 tên + bí danh ≈ 1.000–1.500 token; đầu ra + suy luận ≈ 100–500 token ⇒
  **≈ 0,0003–0,0005 USD / ảnh** (≈ 8–13 đồng). Bước 0 (A1b) kiểm lại trước lượt lớn.
- Lượt đo P1: 33 ảnh × 2 lần + ≤ 2 vòng chỉnh × 33 + kín 10 × 2 lượt (bản 2) ≈ 150–185 lần gọi ≈ **0,05–0,09 USD** [tính: 150–185 × 0,0003–0,0005]; Q-i 25 câu chat ≈ 0,01. **Giọng nói** (§8): đề xuất chạy máy ⇒ ≈ 0.
- **Trần Phase 10 đề xuất 0,15 USD** (dừng 0,13; một lượt vượt ước > 50 % ⇒ dừng, báo A). Mỗi phiên ≤ 1 USD **gộp với Phase 9**. Tiền Phase 10 ghi riêng, không
  lấy từ quỹ Phase 9 (2,0) hay quỹ B7.

## 8. Giọng nói — để sau (mục chờ; viết đầy đủ khi mở lại E1)

**Duyệt bản này không phải duyệt phần giọng nói** (review B §5): mục này chỉ ghi hiện trạng + ràng buộc; đường ra, model, ngưỡng, lịch của giọng nói User duyệt khi
mục được viết đủ (một bản sửa đổi spec riêng, có review).

Hiện trạng: nghiên cứu E1 **dở** (`data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md`). Đã kiểm 05/11: giấy phép là bộ lọc lớn nhất — nhiều model Việt tốt nhất
**không cho thương mại** (Zipformer-30M `hynt` CC-BY-NC-ND, wav2vec2-vi CC-BY-NC, MMS-TTS CC-BY-NC, viXTTS CPML, F5-TTS-Vi CC-BY-NC-SA); dùng được cho sản phẩm:
**PhoWhisper** (VinAI, BSD-3), **Zipformer `zzasdf` 70k giờ** (Apache-2.0, sherpa-onnx int8 74 MB), **Piper `vi_VN`** (giọng MIT, code GPL-3.0). Đồ án học thuật thì
bản NC dùng được — **User quyết** "xem như sản phẩm thật" có loại NC không.

Ràng buộc đã biết (để mục này đóng các finding chuyển):
- **M-1 (đường ra / model mới):** nhận dạng giọng nói của trình duyệt (Web Speech API) có thể gửi âm thanh tới máy chủ của hãng — **kể cả lượt thử** ⇒ phải liệt kê
  là đường ra, User duyệt; model chạy máy (PhoWhisper / Zipformer) = model mới ⇒ User duyệt từng cái (giấy phép + RAM ước + "không chạy cùng việc nặng khác").
  Đề xuất mặc định: **chỉ phương án chạy máy** (đúng ý User "open-source, không gọi API ngay") ⇒ âm thanh không ra ngoài.
- **M-3 (ngưỡng V1 thành đạt / không):** ghi trước khi đo, trên **15 câu User tự đọc** (câu tự viết có tên điểm / món + số): bản chữ **chưa sửa** — tên điểm / món đúng
  **≥ 12 / 15** **và** số đúng ≥ 90 % số con số; dưới ngưỡng ⇒ V1 không bật [đề xuất — chốt khi viết mục này]. Giọng User là dữ liệu cá nhân ⇒ private, xoá sau đo.
- Thêm khi viết: route âm thanh dùng cùng rào §6 (giới hạn byte / thời lượng, không lưu, không log); chuyển webm / opus từ trình duyệt sang 16 kHz (có thể cần
  `ffmpeg` — công cụ hệ thống mới ⇒ duyệt).

## 9. Finding chuyển từ review spec Phase 9 bản 10 (`…design_review_v10.md`, vòng 1)

| Mã | Tiêu chí đóng (review) | Spec này | Trạng thái |
|---|---|---|---|
| **M-1** | liệt kê đường ra nhận dạng giọng trình duyệt (kể cả lượt thử); User duyệt cả các phương án (provider trình duyệt, PhoWhisper — giấy phép + RAM + không chạy cùng việc nặng) hoặc bỏ phương án chưa duyệt | §8 ý 1 | **mở** — đóng khi viết mục giọng nói đầy đủ |
| **M-3** | ngưỡng V1 tên đúng ≥ x / 15 và số đúng ≥ y, dưới ⇒ không bật | §8 ý 2 (đề xuất 12 / 15 + 90 %) | **mở** — số chờ chốt |
| **M-4** | tách mẫu số ảnh Huế / ngoài Huế; danh sách tên cụ thể (nguồn + số tên) | §3.1 (nguồn + số), §3.2 (n_H = 25 / 5 riêng), §5 Q-a / Q-c | đề xuất đóng — reviewer kiểm |
| **m-7** | rào giới hạn điểm ảnh khi giải mã; Pillow đã có | §6 dòng 1 | đề xuất đóng — reviewer kiểm |

## 10. Rà theo khung AI FDE (bản 2: thêm cột hiện trạng `file:dòng` + đề xuất — `Session_Prompt.md` §7, review B m-1)

Route ảnh chưa có ⇒ cột "hiện trạng" trỏ **chỗ code hiện hành mà Phase 10 dùng lại hoặc phải giữ**; ô "đề xuất" trống khi khớp.

### 10.1 `agent-design-review`

| Mục khung | Hiện trạng (`file:dòng`, `main`) | Phase 10 (ảnh) | Khớp / lệch | Đề xuất |
|---|---|---|---|---|
| §1 Có cần agent | agent trợ lý có công cụ chỉ ở tuyến `tro_ly_hue` (`backend/llm/assistant.py:382` `_pick_route` → vòng công cụ) | **không**: một lần gọi đầu ra có cấu trúc (A1); mốc M0 không model | khớp | |
| §2 Chia việc code ↔ model | câu ghép từ nút do code (`backend/api/routes/chat.py:114` `_model_query`) | model chỉ **chọn id** trong enum; code: danh sách tên, đổi id ⇒ tên, câu ghép A3, câu A9, xác nhận, rào ảnh | khớp | |
| §3 Công cụ / tham số | — (route mới không có công cụ) | id đầu ra kiểm lại ở backend; tên chuẩn do code điền vào câu hỏi kho | khớp | |
| §3 "không thấy ≠ không tồn tại" | câu từ chối chuẩn của kho (`ngoai_pham_vi`, `assistant.py:382`) | `khong_nhan_ra` = model không chắc, **không** phải "kho không có" ⇒ câu A9 mời gõ tên | khớp | |
| §4 Trần + phục hồi | định tuyến có hạn giờ `router_timeout_seconds: 10` (`backend/config/settings.yaml:64`); lời gọi model qua `_run` (`backend/llm/generator_openai_full_corpus.py:314`) | 1 lần gọi; lỗi / quá hạn ⇒ câu A9, không đoán | lệch nhẹ (chưa có số) | plan A1 ghi hạn giờ (đề xuất 15 s — ảnh chậm hơn chữ) + test quá hạn ⇒ A9, 0 lần gọi lại |
| §5 Trí nhớ | nhớ hội thoại lưu câu hỏi (`chat.py:107-111` `_remember`; `settings.yaml:67-68`) | ảnh **không** vào nhớ; chỉ câu ghép (chữ) | khớp | |
| §5 Lời dặn | lời dặn trợ lý dùng chỗ trống, không địa danh thật (ý #12 Phase 9) | lời dặn ngắn: mục tiêu · dựa vào gì · xong ra sao (schema); không ví dụ địa danh thật | khớp | |
| Tracing / log | tracing SDK tắt (`generator_openai_full_corpus.py:198-201`); log chỉ số đếm (`chat.py:36`, `:162`) | `anh_metrics` chỉ số đếm (Q-g) | khớp | |

### 10.2 `agent-security-review`

| Mục | Hiện trạng (`file:dòng`, `main`) | Phase 10 (ảnh) | Mức | Đề xuất |
|---|---|---|---|---|
| 1 Bộ ba | đường ra hôm nay: chữ + ≤ 10 đoạn kho tới OpenAI (`session_prompt/Project_Status.md` §6) | thêm ảnh ⇒ đủ ba ở mức nhẹ (§6) ⇒ cắt bằng không công cụ / không lịch sử / enum / xác nhận | minor sau rào | A sửa §6 egress khi User duyệt |
| 2 Nội dung không tin cậy | chữ người dùng = dữ liệu (lời dặn trợ lý) | ảnh + chữ trong ảnh = dữ liệu; đo bằng ca khó thật | đo Q-d | |
| 3 Giới hạn ở API | `ChatRequest` `max_length=500`, `extra="forbid"` (`chat.py:62-64`); route chat nhận JSON ⇒ có preflight; không CORS (`backend/api/app.py:166-168` chỉ đăng ký router) | **A10**: thân `image/*` (bắt preflight) + `Sec-Fetch-Site` / `Origin` ⇒ 403 + byte ≤ 10 MB trước khi đọc + điểm ảnh + định dạng — ở backend | **major ở bản 1 → đóng bằng A10** (review B M-2) | test Q-j |
| 4 Quyền hẹp | khoá OpenAI ở server, nạp bằng `--env-file` | route chỉ gọi model, không đọc / ghi gì khác | — | |
| 5 Dữ liệu cá nhân | log không chữ (`chat.py:36`); cookie `HttpOnly` + `SameSite=Strict` (`chat.py:90, :131`) | EXIF xoá; không ghi ảnh ra đĩa; không log ảnh; dòng báo người dùng; egress mới User duyệt | Q-g + User duyệt | |
| 6 Rào đo hai chiều | — | ca xấu (3 ảnh chữ lệnh, ca khó thật) + ca thường gần giống (2 ảnh biển tên thật phải vẫn nhận đúng) | Q-a, Q-d | |
| 7 Coding agent | `Session_Prompt.md` §2 (nội dung ngoài là dữ liệu) | ảnh Commons / kết quả tra web là dữ liệu; tải ảnh / model = việc cần duyệt | — | |
| CSP | `img-src 'self'; connect-src 'self'` (`app.py:38`) | xem trước cần `blob:` (A7) | thấp | User duyệt hoặc không xem trước |

## 11. Lịch (song song Phase 9, **ảnh trước**)

**Thay cột Phase 10 của spec Phase 9 bản 12 §11.4** (cột đó xếp giọng nói trước) **kể từ lúc User duyệt spec này** — không sửa spec Phase 9; A ghi một dòng trỏ ở
`CURRENT_HANDOFF.md` khi duyệt (review B m-4). Luật chung của spec Phase 9 §11.4 vẫn giữ: Phase 10 xung đột file ⇒ Phase 9 ưu tiên, Phase 10 rebase.

| Tuần | Phase 10 | Ràng buộc |
|---|---|---|
| 05–09/11 | spec này review + User duyệt; A0 (danh sách tên, bộ ảnh — sau khi duyệt tải ảnh) | không việc nặng khi B / C đo tốc độ (W31) |
| 10–16/11 | A1 + A1b + A2 (backend, route mới — không chạm file Phase 9 đang sửa) | Phase 9 B5 đo + merge ⇒ **lượt đo A2 (có phí, đo ms) không chạy cùng giờ lượt đo B5**; A xếp giờ (W31) |
| 17–23/11 | A3 nếu cần (P2 chạy CPU — việc nặng); A4 giao diện trên worktree riêng, rebase sau B5 merge | `App.jsx` chồng ⇒ Phase 9 ưu tiên; P2 không chạy cùng lượt đo B5c |
| 24–30/11 | merge A4 xen giữa hai lần merge Phase 9; mở lại E1 giọng nói (§8) | — |
| 01–14/12 | giọng nói (plan + đo trên máy) ⇒ đóng Phase 10 | **trùng tuần đo B5b (01–07/12) và B6 (08–14/12)** ⇒ lượt đo giọng nói trên máy (CPU / RAM nặng) **không chạy cùng lúc** lượt đo Phase 9 (W31; review B m-5) — A xếp giờ; xong trước B7 (15–21/12, không việc nặng song song) |

**Luật cắt:** 30/11 ảnh chưa merge ⇒ dừng ảnh, ghi dở; 14/12 giọng nói chưa đạt ⇒ không bật, ghi dở. Phase 9 B7 không bị chậm vì Phase 10.

## 12. Quyền cần User duyệt (gom một lần)

1. Đường ra mới: **ảnh người dùng tới OpenAI** (`gpt-6-luna`, model đang dùng) + dòng báo người dùng (§6).
2. Tải ~30–40 ảnh Commons / dùng ảnh User chụp vào `data/` (§3.2).
3. Đổi CSP `img-src 'self' blob:` (A7) — hoặc chọn không xem trước.
4. Trần Phase 10 0,15 USD (§7).
5. (khi cần) tải SigLIP 2 base ~1,6 GB + thư viện nếu thiếu (A6).
6. (mục giọng nói, sau) có loại model giấy phép NC không; model chạy máy nào được thử (§8).

## 13. Giới hạn

- Không có số công khai về độ chính xác nhận địa danh / món Huế của bất kỳ model nào [E2] ⇒ mọi kỳ vọng là giả thuyết tới lượt đo.
- 30 ảnh chỉ bắt lỗi lớn (§5 Wilson); ảnh Commons đẹp hơn ảnh du khách ⇒ đo có thể lạc quan — bù bằng 1/3 ảnh User chụp.
- Token ảnh của `gpt-6-luna` là giả định tới bước 0.
- Giọng nói chưa thiết kế xong (§8).

## Chỗ đổi bản 2 (review B vòng 1 `…phase-10-design_review.md` `62ffcac51b1a`, changes_requested 0 / 2 / 6)

| Finding | Sửa ở |
|---|---|
| **M-1** kín không ngưỡng + luật A/A | §5 **Q-k** (10 ảnh kín × 2 lượt: trong danh sách ≥ 7 / 8, ngoài danh sách bị ép 0 / 2, cả hai lượt; phạm ⇒ âm, không chỉnh / chạy lại); **luật A/A**: Q-a, Q-c, Q-d, Q-k đạt ở **cả hai lượt**; kết quả âm thêm Q-k; P2 dùng bộ kín mới; §4 A2 khoá (sha) rồi kín × 2; §7 số lần gọi |
| **M-2** gửi chéo trang qua multipart | **A10** mới: không multipart — thân `image/*` (bắt preflight, không CORS) + kiểm `Sec-Fetch-Site` / `Origin` ⇒ 403 + `Content-Type` ⇒ 415 trước khi đọc thân, 0 lần gọi model; A2 đổi; §6 dòng "Gửi chéo trang"; §5 **Q-j**; §4 A1 test + probe; §10.2 mục 3 |
| m-1 bảng rà khung thiếu cột | §10.1, §10.2: thêm cột hiện trạng `file:dòng` + đề xuất; thêm dòng §4 (hạn giờ — lệch nhẹ, đề xuất 15 s ở plan), tracing / log, CSP |
| m-2 Q-d tự đạt | Q-d thành **sàn đo** ≤ 1 / 3 chọn đúng tên kẻ tấn công đòi, ca khó thật (đòi tên hợp lệ khác, tiếng Việt / Anh, chữ nhỏ ở góc); schema là test |
| m-3 làm tròn Q-a | số tuyệt đối từng loại (làm tròn lên): 9 / 13 · 3 / 4 · 4 / 6 · 2 / 2 |
| m-4 hai spec mâu thuẫn lịch | §11: thay cột Phase 10 của spec Phase 9 §11.4 từ lúc User duyệt, không sửa spec Phase 9, A ghi dòng trỏ ở handoff |
| m-5 đo giọng nói trùng đo Phase 9 | §11: ràng buộc W31 cho tuần 10–16/11, 17–23/11, 01–14/12; §4 A2 |
| m-6 rào byte trước multipart + chữ "lưu lại" | A10 (3) + §6 dòng bom giải nén: đọc luồng có bộ đếm, không `UploadFile`; probe 11 MB ở A1; Q-g bỏ "lưu lại", thêm "không ghi ảnh ra đĩa" |
| §5 review "duyệt không gồm giọng nói" | §8 dòng đầu |

Không đổi: A1, A3–A9, §3, Q-b, Q-c, Q-e, Q-f, Q-h, Q-i, tiền trần 0,15 / dừng 0,13, quyền §12.
