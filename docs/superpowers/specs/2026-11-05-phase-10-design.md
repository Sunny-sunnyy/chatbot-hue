# Phase 10 — hỏi bằng ảnh (trước) + giọng nói (sau) — tài liệu thiết kế

Người viết: E (`hue-rag-7a`; bản 3 `hue-rag-bc`) · **bản 3, 20:47 05/11/2026** (`date`; việc **E12** — viết đủ §8 giọng nói phần NGHE theo nghiên cứu E1 + User chọn "nghe trước, đọc sau"; **phần ảnh §1–§7, §10 không đổi**; chỗ đổi cuối file; trạng thái: **chờ review, chưa trình User**) · bản 2 `bf67b90fb6fc` **User duyệt 10:28 05/11/2026** (phần ảnh) · bản 2, 10:18 05/11/2026 (`date`; việc **E4b** — sửa theo review B vòng 1 `…phase-10-design_review.md` `62ffcac51b1a`: M-1, M-2, m-1…m-6; chỗ đổi cuối file) · bản nháp 1 `d640b8696edd` 10:04 05/11/2026 (E4). Trạng thái: **chờ B kiểm phần sửa, chưa trình User**.
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

**Căn cứ thêm cho bản 3 (§8):** `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md` (private, E1 **xong** 05/11) §0–§8 — số liệu dẫn đúng nhãn [đã kiểm] / [Codex] / [tự báo]; code `main` `b75fefc`: `backend/api/routes/anh.py:23-54` (rào dùng lại), `backend/api/app.py:42-43` (CSP), `:146-152` (nạp lúc khởi động), `frontend/src/App.jsx:62, :72` (ô gõ). **Dẫn, ngoài căn cứ:** `bao_cao_he_thong/DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` §3 V1 / V2 (đề xuất User duyệt bậc 1).

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

## 8. Giọng nói — NGHE (nói ⇒ chữ) — bản 3

**Bản 3 thay toàn bộ mục chờ của bản 2.** User chọn (A chuyển, phiên tối 05/11): **thử nghe trước, đọc sau**. **Đọc thành tiếng (TTS): để sau** — mục riêng khi mở lại
(ứng viên đã xếp ở `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md` §6; mốc `speechSynthesis` của trình duyệt). Căn cứ số liệu: cùng file đó §1, §8 (nguồn).

### 8.1 Mục tiêu (khám phá 5 dòng)

1. **Vấn đề + đo bằng gì:** du khách đang đi / tay bận muốn **nói** câu hỏi thay vì gõ. Đo bằng **tên riêng Huế chép đúng** (quyết định tìm kho có ra đúng không),
   WER, số đúng, độ trễ, RAM.
2. **Ba ô:** đo được — có (bộ 40 câu, §8.4) · dữ liệu đánh giá — **chưa có**, User thu · giá trị — làm được việc mới (nhập bằng giọng), không phải rẻ / nhanh hơn.
3. **Mốc đơn giản nhất (G-M0):** người dùng **gõ** — 0 model, đang chạy. Mốc trình duyệt (Web Speech API) **mặc định gửi âm thanh tới dịch vụ ngoài** [đã kiểm MDN] ⇒
   chỉ để so, không làm đường chính. API này nhận **micro trực tiếp**, không nhận file [suy ra, chưa kiểm bản mới của đặc tả] ⇒ không chạy được trên cùng 40 file
   ⇒ **không nằm trong bộ đo chính**; muốn so: User đọc lại 10 câu trực tiếp trên Chrome, chỉ tham khảo, cần User duyệt egress lượt thử (§12 (9)).
4. **Tiêu chí bằng số:** §8.5 (ghi trước khi đo).
5. **Phương án B:** cả hai model dưới sàn sau ≤ 2 vòng chỉnh (§8.5) ⇒ **không bật**, giữ gõ tay, ghi kết quả âm; Moonshine vi (xếp thứ 3 ở E1) chỉ thử khi User muốn thêm một lượt.

**Không làm:** tự gửi câu sau khi chép; lưu âm thanh; đọc trả lời thành tiếng; nhận lệnh bằng giọng ("xoá cuộc trò chuyện"…); nhận giọng liên tục (luôn nghe).

### 8.2 Quyết định

| Mã | Quyết định | Vì sao | Sai khi / chọn khác mất gì |
|---|---|---|---|
| **G1** | **Không dùng agent, không LLM:** chép lời là **một lần gọi model nhận dạng chạy trên máy** (sherpa-onnx), không lời dặn, không công cụ | luồng cố định (âm thanh ⇒ chữ) ⇒ code (`agent-design-review` §1) | — |
| **G2** | **Model chạy máy, hai ứng viên:** **Gipformer 68M RNNT int8** (bảng tác giả: ViMD 7,17 · giọng Trung 32,27 — tốt nhất bảng; MIT) và **Zipformer-30M-RNNT-6000h** (`hynt`, gói sherpa int8 ~32 MB, RTF 0,011 một luồng [đã kiểm log sherpa]; giọng Trung 45,19); chạy bằng **sherpa-onnx** (ONNX Runtime, **không torch**) | âm thanh không rời máy; nhỏ; số giọng Trung tốt nhất trong nguồn có | mọi số là **tự báo** của một nhóm ⇒ phải đo. Gipformer chạy được bằng sherpa-onnx **chưa kiểm** ⇒ bước G0; không chạy ⇒ chỉ còn Zipformer (không thêm thư viện khác khi chưa duyệt). Khác: PhoWhisper — mất: cần torch, giọng Trung 59–65 trong bảng |
| **G3** | **Chữ chép luôn vào ô gõ** (`frontend/src/App.jsx:62` `draft` / `setDraft`, `:72` `queryRef`): ô trống ⇒ thay; ô có chữ ⇒ nối sau một dấu cách; con trỏ về ô gõ; **người dùng sửa / bấm Hỏi** — code **không bao giờ tự gửi** | lỗi chép không thành câu hỏi sai (như "hỏi bằng ảnh": model chỉ đề xuất, người xác nhận); chữ đi đúng đường `/api/chat` như câu gõ | thêm một lần bấm. Khác: tự gửi khi đủ tin cậy — mất: điểm tin cậy của model không phải bảo đảm, câu sai tên đi thẳng vào kho |
| **G4** | **Luồng:** nút "Nói" (component riêng `frontend/src/HoiBangGiong.jsx`, cùng cách tách file của A8) ⇒ trình duyệt xin quyền micro **chỉ khi bấm** ⇒ ghi tối đa **15 s** (bấm lần nữa để dừng; tự dừng ở 15 s) ⇒ **trình duyệt tự đổi sang WAV PCM 16 kHz mono 16-bit** (giải mã + lấy mẫu lại bằng Web Audio ngay trong trang) ⇒ `POST /api/giong_noi/chep` (thân = bytes WAV, `Content-Type: audio/wav`) ⇒ `{chu: "…"}` | backend **không cần ffmpeg / thư viện giải mã** (đọc WAV bằng `wave` của Python); 15 s × 32 KB/s ≈ 480 KB | trình duyệt cũ không có Web Audio ⇒ nút không hiện. Khác: gửi WebM / Opus của `MediaRecorder` — mất: cần ffmpeg ở server (công cụ hệ thống mới vào runtime) |
| **G5** | **Rào route = rào route ảnh** (`backend/api/routes/anh.py:28` `kiem_dau_vao`, `:44` `doc_than` — dùng lại, chỉ đổi tập kiểu): `Sec-Fetch-Site` ≠ `same-origin` / `Origin` khác gốc ⇒ 403; `Content-Type` ≠ `audio/wav` ⇒ 415; `Content-Length` thiếu hoặc > **512 KB** ⇒ 413; đọc luồng có bộ đếm; sau khi đọc: WAV phải **1 kênh, 16 bit, 16 kHz, ≤ 15 s** (`wave`) ⇒ sai ⇒ 415 / 413 — **trước khi gọi model** | cùng mức chặn gửi chéo trang (A10: thân `audio/*` bắt preflight, không CORS); không thêm token / cookie | — |
| **G6** | **Không lưu âm thanh, không log chữ:** âm thanh chỉ ở RAM trong lượt; log `giong_noi_metrics` một dòng / yêu cầu: outcome, mã HTTP, giây âm thanh, **số ký tự** chép, ms xử lý — **không** chữ, không âm thanh, không header | giọng nói = dữ liệu cá nhân (§8.6) | — |
| **G7** | **Model nạp một lần lúc khởi động** khi cờ `giong_noi.bat` bật (như `app.state.anh`, `backend/api/app.py:146-152`); cờ tắt / nạp lỗi ⇒ route 404, nút không hiện (`GET` trước, như ảnh); chép trong `asyncio.to_thread`; **một lượt chép tại một thời điểm** (đang bận ⇒ 429 "đang nghe câu khác, thử lại") | CPU máy User; tránh hai lượt cùng ăn CPU / RAM (bài học review C198 m-3) | người dùng thứ hai phải chờ — chấp nhận trên máy User; Phase 12 xem lại |
| **G8** | **Từ khoá tên riêng (hotwords) do code dựng** từ danh sách tên Phase 10 (`data/phase_10/anh/danh_sach_ten.json`, 42 mục + bí danh) — chỉ bật ở **vòng chỉnh** nếu vòng 0 thiếu tên riêng; cần `modified_beam_search` [Codex — trang hotwords sherpa; kiểm ở G0] | tên Huế là điểm yếu dễ đoán trước; danh sách đã có, User đã duyệt | hotwords có thể **chèn tên sai** vào câu không có tên ⇒ đo hai chiều (V-e) |
| **G9** | Lỗi / quá hạn (**10 s** cho một lượt chép) / chữ rỗng ⇒ câu cố định "Mình chưa nghe rõ — bạn nói lại hoặc gõ giúp nhé" (code); chữ > 500 ký tự (`backend/api/routes/chat.py:68`) ⇒ cắt, báo | đường lùi = gõ tay | — |

### 8.3 Bậc làm (giọng nói)

| Bậc | Việc | 0 USD? | Đầu ra |
|---|---|---|---|
| **G0** | sau khi User duyệt §12 (7)–(8): `uv add sherpa-onnx`; tải 2 model (≤ 300 MB tổng); chạy file mẫu kèm gói ⇒ kiểm Gipformer chạy được bằng sherpa-onnx, đầu ra (viết hoa / dấu câu), hotwords chạy với `modified_beam_search`; ghi RAM / ms một câu | có | report ngắn; Gipformer không chạy ⇒ báo A, đo chỉ Zipformer |
| **G1** | User thu bộ 40 câu (§8.4) ⇒ đổi sang WAV 16 kHz mono bằng `ffmpeg` **có sẵn trên máy** (công cụ đo, không vào runtime) | có | `data/phase_10/giong_noi/bo_do/` (private) |
| **G2** | script đo: 2 model × 40 câu (vòng 0, không hotwords) ⇒ V-a…V-f; lặp lần 2 kiểm **giống hệt** (tất định); ≤ 2 vòng chỉnh (hotwords G8, số luồng / cách giải mã) trên cùng bộ | có | report + bảng so |
| **G3** | (model đạt) route + rào + test (G5, G6, G9: ca 403 / 413 / 415 / WAV sai dạng ⇒ 0 lần gọi model; log không có chữ) sau cờ `giong_noi: false` | có | nhánh `p10-giong` |
| **G4** | giao diện `HoiBangGiong.jsx` + Playwright (máy tính + khung điện thoại; micro giả của Chromium phát file WAV có sẵn — không cần người nói) + Q1 kiểu Phase 9 (cờ tắt / bật ⇒ chuỗi gửi model `/api/chat*` giống byte `main`) | có | merge `main`, cờ bật nếu User đồng ý |

### 8.4 Bộ đo — 40 câu User thu (người dựng bộ ≠ người code)

- **Câu chữ:** C soạn (E không soạn) 40 câu **kiểu người dùng thật hỏi chatbot**: **20 câu có tên riêng Huế** (địa danh, món — lấy từ danh sách tên Phase 10, mỗi tên ≤ 2 lần),
  **10 câu có số** (giá, giờ, số ngày, số người), **10 câu thường** không tên riêng, không số (ca thường gần giống — để đo chèn tên sai). C ghi nhãn: từng tên riêng, từng
  con số, bản chép chuẩn **theo cách đọc** (số viết bằng chữ). User duyệt câu trước khi thu.
- **Người đọc:** User + **ít nhất 1 người giọng Huế / miền Trung** (người đó đồng ý bằng lời cho việc thu, dùng trong đồ án, xoá sau khi đóng Phase 10). Không có người giọng
  Huế ⇒ vẫn đo, ghi giới hạn "không nói được gì về giọng Huế". Mỗi người đọc cả 40 câu hoặc chia đều (ghi trước trong plan).
- **Cách thu:** điện thoại hoặc laptop, app ghi âm bất kỳ (định dạng bất kỳ); đọc **tự nhiên**, không đọc chậm; **30 câu nơi yên tĩnh + 10 câu có ồn nền** (quán, đường, quạt
  — ca khó); mỗi câu một file, tên file = số câu. File gốc ⇒ WAV 16 kHz mono (G1) ⇒ xoá file gốc; WAV private `data/phase_10/giong_noi/bo_do/`, **không commit**, xoá khi đóng
  Phase 10.
- **Bộ kín: không** (luật User 05/11 — model nhận dạng tất định, không có lời dặn để chỉnh nhiều vòng; đo bằng bộ đã thấy). Chỉnh ≤ 2 vòng ghi rõ đổi gì.

### 8.5 Tiêu chí ghi trước (áp cho từng model, trên 40 câu)

Chuẩn hoá trước khi so (một hàm, mọi model như nhau, ghi trong plan): NFC, chữ thường, bỏ dấu câu, gộp khoảng trắng.

| Mã | Loại | Chỉ số / ngưỡng | Ghi chú |
|---|---|---|---|
| **V-a** | **quyết** | **tên riêng đúng ≥ 90 %** số lần tên riêng xuất hiện (tên đúng = cả cụm tên sau chuẩn hoá có trong bản chép) | mẫu số ≈ 20–30 lần xuất hiện ⇒ ghi k / n + khoảng Wilson |
| **V-b** | **quyết** | **WER ≤ 15 %** (cả 40 câu) | báo riêng nhóm yên tĩnh / có ồn, theo người đọc |
| **V-c** | **quyết** (M-3) | **số đúng ≥ 90 %** số con số trong 10 câu có số | |
| **V-d** | **quyết** | **p95 ≤ 1,5 s** / câu (đọc WAV + chép, sau khi nạp model, số luồng ghi trước = như lúc chạy thật) · **RAM đỉnh tiến trình đo ≤ 1,5 GB** | báo thêm p50, thời gian nạp model, dung lượng model |
| **V-e** | **sàn** (khi bật hotwords) | **chèn tên sai** (tên riêng có trong bản chép mà không có trong câu nói) **≤ 1 / 40 câu** | rào đo hai chiều: 10 câu thường là ca gần giống |
| **V-f** | **sàn** (test) | route: yêu cầu khác nguồn / sai kiểu / quá cỡ / WAV sai dạng ⇒ 403 / 415 / 413 và **0 lần chép**; log không có chữ; không file âm thanh nào ghi ra đĩa | G3 |

**Chọn:** model đạt **cả** V-a…V-d (và V-e nếu dùng hotwords); cả hai đạt ⇒ chọn V-a cao hơn, bằng nhau ⇒ nhỏ / nhanh hơn. **Kết quả âm:** không model nào đạt sau
2 vòng chỉnh ⇒ không bật, ghi âm vào báo cáo; xét Moonshine (§8.1 ý 5) chỉ khi User muốn. Lặp lần 2 phải giống hệt — khác ⇒ báo A trước khi kết luận.

### 8.6 Bảo mật (`agent-security-review`) + dữ liệu cá nhân

**Bộ ba ở bước nghe:** (a) dữ liệu riêng tư — **giọng nói** (nhận ra được người nói) · (b) nội dung không tin cậy — âm thanh (kể cả lời "ra lệnh") · (c) đường ra — **không có**
(model chạy máy; chữ chép chỉ về trình duyệt). Thiếu (c) ⇒ không đủ bộ ba; chữ chép đi tiếp **chỉ khi người dùng bấm Hỏi**, như câu gõ.

| Rủi ro | Mức | Rào (code / API) | Đóng |
|---|---|---|---|
| Giọng nói rời máy | trung bình | chỉ model chạy máy (G2); Web Speech **không** dùng ở đường chính (§8.1 ý 3) | **M-1** |
| Lưu / lộ giọng nói, chữ chép | trung bình | không ghi đĩa, không log chữ (G6); bộ đo private, xoá khi đóng Phase 10 | V-f + cổng grep log |
| Gửi chéo trang (trang lạ bắt máy User chép âm thanh — tốn CPU) | thấp | G5 (cùng A10 của ảnh) | V-f |
| Âm thanh "bom" / quá dài | thấp | byte ≤ 512 KB trước khi đọc + kiểm dạng WAV + ≤ 15 s trước model (G5) | V-f |
| Lời nói "ra lệnh" ("bỏ qua luật…") | thấp | chữ chép = dữ liệu người dùng, vào ô gõ, đi qua định tuyến + rào Phase 9 như câu gõ; route nghe không có quyền gì khác | — |
| Chiếm CPU (nhiều lượt cùng lúc) | thấp (máy User) | một lượt / lúc ⇒ 429 (G7); Phase 12 thêm hạn mức theo IP | ghi đầu vào Phase 12 |
| Quyền micro | thấp | xin chỉ khi bấm nút; ngoài `localhost` trình duyệt chỉ cho micro trên HTTPS ⇒ Phase 12 | — |

Dòng báo dưới nút: "Giọng nói được chép thành chữ ngay trên máy chủ này, không lưu âm thanh. Kiểm tra chữ trước khi bấm Hỏi."

**Giả định an toàn:** chạy trên máy User (một người dùng), `localhost`; AWS ở Phase 12 (HTTPS, hạn mức); không gửi âm thanh ra ngoài; không lưu âm thanh.

### 8.7 Rà theo khung AI FDE (giọng nói)

`agent-design-review`:

| Mục khung | Hiện trạng (`file:dòng`, `main` `b75fefc`) | Phase 10 (nghe) | Khớp / lệch | Đề xuất |
|---|---|---|---|---|
| §1 Có cần agent | trợ lý có công cụ chỉ ở tuyến `tro_ly_hue` | **không agent, không LLM**: một lần chạy model nhận dạng (G1); mốc G-M0 = gõ tay | khớp | |
| §2 Chia việc code ↔ model | câu ghép nút do code (`chat.py` `_model_query`) | model chỉ chép chữ; code: rào, kiểm WAV, cắt 500 ký tự, đưa vào ô gõ, **không tự gửi** (G3), danh sách hotwords (G8), câu G9 | khớp | |
| §2 Câu cố định hứa hành động | — | G9 "nói lại hoặc gõ giúp" — không hứa gì code không làm | khớp | |
| §3 Công cụ / tham số | — | không công cụ; tham số model (số luồng, cách giải mã) cố định trong `settings.yaml` | khớp | |
| §4 Trần + phục hồi | ảnh: `timeout: 20` (`settings.yaml` khối `anh:`), lỗi ⇒ câu cố định | một lượt, hạn 10 s, lỗi ⇒ G9, không chép lại; một lượt / lúc ⇒ 429 | khớp | test quá hạn ở G3 |
| §5 Trí nhớ | nhớ hội thoại lưu câu hỏi (`chat.py:112` `_remember`) | âm thanh **không** vào nhớ; chỉ câu người dùng gửi (chữ) như hôm nay | khớp | |
| Log | `anh_metrics` chỉ số đếm (`anh.py:23`) | `giong_noi_metrics` chỉ số đếm (G6) | khớp | |

`agent-security-review`:

| Mục | Hiện trạng (`file:dòng`) | Phase 10 (nghe) | Mức | Đề xuất |
|---|---|---|---|---|
| 1 Bộ ba | đường ra hôm nay: chữ + đoạn kho + ảnh (khi bật) tới OpenAI (`Project_Status.md` §6) | không thêm đường ra (§8.6) | — | |
| 2 Nội dung không tin cậy | chữ người dùng = dữ liệu | chữ chép = chữ người dùng | — | |
| 3 Giới hạn ở API | rào ảnh `anh.py:28-54` | G5 dùng lại + kiểm WAV | — | test V-f |
| 4 Quyền hẹp | khoá OpenAI ở server | route nghe không dùng khoá, không đọc / ghi gì khác | — | |
| 5 Dữ liệu cá nhân | log không chữ (`chat.py:33` logger `chat`, `:167`) | không lưu âm thanh, không log chữ, bộ đo xoá khi đóng Phase | V-f | |
| 6 Rào đo hai chiều | — | hotwords: tên đúng (V-a) **và** chèn tên sai (V-e) | — | |
| 7 Coding agent | `Session_Prompt.md` §2 | model tải từ HF = việc cần duyệt; file ghi âm = dữ liệu cá nhân, không commit | — | |
| CSP / quyền trình duyệt | CSP `connect-src 'self'` (`app.py:42-43`); chưa có `Permissions-Policy` | micro không bị CSP chặn; đề xuất thêm `Permissions-Policy: microphone=(self)` (chỉ trang mình) | thấp | plan G3 |

### 8.8 Tiền, máy, lịch

- **0 USD** (chạy máy; không lượt gọi model trả phí). Tải ≤ 300 MB model + gói `sherpa-onnx` (cỡ wheel chưa kiểm — ghi ở G0).
- Việc nặng (G2 đo, G4 Playwright) **không chạy cùng lúc** lượt đo có phí / tốc độ của Phase 9 (W31) — A xếp giờ; kiểm RAM trống ≥ 5 GB trước khi chạy.
- Lịch: G0 ngay sau khi User duyệt bản 3 + §12 (7)–(8); G1 khi User thu xong 40 câu; G2–G4 sau đó. **Luật cắt giữ nguyên: 14/12 chưa đạt ⇒ không bật, ghi dở.**

## 9. Finding chuyển từ review spec Phase 9 bản 10 (`…design_review_v10.md`, vòng 1)

| Mã | Tiêu chí đóng (review) | Spec này | Trạng thái |
|---|---|---|---|
| **M-1** | liệt kê đường ra nhận dạng giọng trình duyệt (kể cả lượt thử); User duyệt cả các phương án (provider trình duyệt, PhoWhisper — giấy phép + RAM + không chạy cùng việc nặng) hoặc bỏ phương án chưa duyệt | §8.1 ý 3 + G2 + §8.6: **chỉ model chạy máy**, Web Speech không ở đường chính (lượt so tuỳ chọn = egress cần duyệt §12 (9)); model mới + thư viện User duyệt §12 (7)–(8); không chạy cùng việc nặng §8.8 | đề xuất đóng (bản 3) — reviewer kiểm |
| **M-3** | ngưỡng V1 tên đúng ≥ x / 15 và số đúng ≥ y, dưới ⇒ không bật | §8.5: V-a tên riêng đúng ≥ 90 %, V-c số đúng ≥ 90 %, V-b WER ≤ 15 %, V-d p95 ≤ 1,5 s + RAM ≤ 1,5 GB trên **40 câu** (thay 15 câu bản 2); dưới ⇒ không bật | đề xuất đóng (bản 3) — reviewer kiểm |
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
| 24–30/11 | ~~merge A4~~ (**ảnh đã merge cờ tắt 05/11** `2ca9937` + `76319e2`); giọng nói G0–G2 (§8.3) khi User duyệt bản 3 + thu xong 40 câu | G2 không chạy cùng lượt đo Phase 9 |
| 01–14/12 | giọng nói G3–G4 (route, giao diện) ⇒ đóng Phase 10 (bản 3: có thể sớm hơn — ảnh xong sớm) | **trùng tuần đo B5b (01–07/12) và B6 (08–14/12)** ⇒ lượt đo giọng nói trên máy (CPU / RAM nặng) **không chạy cùng lúc** lượt đo Phase 9 (W31; review B m-5) — A xếp giờ; xong trước B7 (15–21/12, không việc nặng song song) |

**Luật cắt:** 30/11 ảnh chưa merge ⇒ dừng ảnh, ghi dở; 14/12 giọng nói chưa đạt ⇒ không bật, ghi dở. Phase 9 B7 không bị chậm vì Phase 10.

## 12. Quyền cần User duyệt (gom một lần)

1. Đường ra mới: **ảnh người dùng tới OpenAI** (`gpt-6-luna`, model đang dùng) + dòng báo người dùng (§6).
2. Tải ~30–40 ảnh Commons / dùng ảnh User chụp vào `data/` (§3.2).
3. Đổi CSP `img-src 'self' blob:` (A7) — hoặc chọn không xem trước.
4. Trần Phase 10 0,15 USD (§7).
5. (khi cần) tải SigLIP 2 base ~1,6 GB + thư viện nếu thiếu (A6).
6. ~~có loại model giấy phép NC không~~ — **bỏ** (luật User 05/11: không kiểm giấy phép).
7. **(bản 3)** thêm thư viện **`sherpa-onnx`** (`uv add`, ONNX Runtime, không torch) cho bước nghe (G2).
8. **(bản 3)** tải 2 model nghe **≤ 300 MB tổng**: Gipformer 68M RNNT int8 + Zipformer-30M-RNNT-6000h int8 (gói sherpa) vào HF cache / `data/`.
9. **(bản 3, tuỳ chọn)** lượt so Web Speech API trên Chrome (10 câu User đọc trực tiếp) = **âm thanh gửi tới dịch vụ của trình duyệt** — chỉ khi User muốn; không chọn ⇒ không chạy.
10. **(bản 3)** User + ≥ 1 người giọng Huế / miền Trung thu 40 câu (§8.4); file private, xoá khi đóng Phase 10.

## 13. Giới hạn

- Không có số công khai về độ chính xác nhận địa danh / món Huế của bất kỳ model nào [E2] ⇒ mọi kỳ vọng là giả thuyết tới lượt đo.
- 30 ảnh chỉ bắt lỗi lớn (§5 Wilson); ảnh Commons đẹp hơn ảnh du khách ⇒ đo có thể lạc quan — bù bằng 1/3 ảnh User chụp.
- Token ảnh của `gpt-6-luna` là giả định tới bước 0.
- Giọng nói (bản 3): mọi số WER / tốc độ của model nghe là **tự báo** (bảng giọng Trung là bộ riêng của một nhóm); Gipformer chạy bằng sherpa-onnx chưa kiểm (G0); 40 câu chỉ bắt lỗi lớn; đọc thành tiếng (TTS) chưa thiết kế.

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

## Chỗ đổi bản 3 (E12, 20:47 05/11/2026 — không phải sửa theo review; phần ảnh giữ nguyên)

| Chỗ | Đổi |
|---|---|
| §8 | viết lại toàn bộ: **NGHE trước** (User chọn), TTS để sau một dòng; 8.1 khám phá 5 dòng (mốc gõ tay; Web Speech chỉ để so, không cùng file) · 8.2 G1–G9 (không agent / LLM; sherpa-onnx + Gipformer 68M + Zipformer-30M; chữ vào ô gõ, không tự gửi; WAV 16 kHz do trình duyệt đổi — không ffmpeg ở server; rào = route ảnh + kiểm WAV; không lưu / không log chữ; nạp lúc khởi động, một lượt / lúc; hotwords do code; câu lỗi cố định) · 8.3 bậc G0–G4 · 8.4 bộ 40 câu (C soạn, User + ≥ 1 giọng Huế thu, 30 yên + 10 ồn; **không bộ kín**) · 8.5 V-a…V-f (tên riêng ≥ 90 %, WER ≤ 15 %, số ≥ 90 %, p95 ≤ 1,5 s + RAM ≤ 1,5 GB, chèn tên sai ≤ 1 / 40, rào test) · 8.6 bảo mật (không đường ra mới) · 8.7 bảng rà khung FDE · 8.8 tiền 0 USD, máy, lịch |
| §9 | M-1, M-3: "mở" ⇒ đề xuất đóng (chỗ đóng ở §8) |
| §11 | hai dòng cuối: ảnh đã merge; lịch giọng nói theo G0–G4 |
| §12 | (6) bỏ (không kiểm giấy phép); thêm (7) `sherpa-onnx` · (8) tải 2 model ≤ 300 MB · (9) tuỳ chọn lượt so Web Speech (egress) · (10) thu 40 câu |
| §13 | dòng giọng nói viết lại |
| đầu file | dòng người viết / bản; căn cứ bản 3 |
