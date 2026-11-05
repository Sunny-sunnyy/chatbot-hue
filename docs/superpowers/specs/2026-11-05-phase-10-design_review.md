# Review: Phase 10 — spec "hỏi bằng ảnh (trước) + giọng nói (sau)", bản nháp 1

## Vòng 1 — spec `d640b8696edd` (B158, A giao)

Decision: **changes_requested** (0 blocker / 2 major / 6 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-48`)
Date: 10:10 05/11/2026 (`date`)
Người viết: E (`hue-rag-7a`) · file `docs/superpowers/specs/2026-11-05-phase-10-design.md` (sha256 12 ký tự tính từ file lúc review: `d640b8696edd`)

### 1. Phạm vi đã review

Chỉ dựa trên mục "Căn cứ để review" của spec (`WORKFLOW.md` §9.1). Không đọc STATUS / tin nhắn của người viết.
- Spec: toàn bộ (207 dòng).
- `docs/superpowers/specs/2026-11-02-phase-9-design_review_v10.md`, vòng 1: M-1, M-3, M-4, m-7 (dòng 11, 13, 14, 28) và dòng m-5 về điều kiện "chuyển hợp lệ".
- Spec Phase 9 bản 12 (`77250689e605`, sha tính từ file): §7, §11.4 (gồm cột Phase 10 và luật "Phase 10 xung đột file ⇒ Phase 9 ưu tiên"), §11.5.
- `data/phase_10_nghien_cuu/anh/nghien_cuu_anh.md` (private) §0–§5: đối chiếu nhãn [đã kiểm] / [tự khai] / [tính].
- Code `main` (chỉ đọc): `backend/api/app.py:38-39` (CSP), `backend/api/routes/chat.py:59-61` (`ChatRequest`, `max_length=500`), `frontend/src/App.jsx:8-13, 104-108`, `session_prompt/Project_Status.md:224` (data egress).
- Thêm theo A giao: bảng rà khung AI FDE theo luật mới `Session_Prompt.md:118`; CSP `blob:`; egress ảnh; ngưỡng; tiền; lịch song song Phase 9.

### 2. Findings

| Mã | Mức | Vị trí | Vấn đề + bằng chứng | Tiêu chí đóng |
|---|---|---|---|---|
| **M-1** | major | §3.2 dòng "Đã thấy / kín"; §4 A2; §5; dòng "Kết quả âm" | **Bộ kín 10 ảnh không có ngưỡng, và luật quyết trên 2 lượt A/A chưa có.** (1) §4 A2 ghi "≤ 2 vòng chỉnh lời dặn trên đã thấy ⇒ khoá ⇒ 10 ảnh kín". Nhưng mọi ngưỡng §5 (Q-a 22 / 25, Q-c ≤ 1 / 5, Q-d 0 / 3) chỉ viết cho 33 ảnh đã thấy, tức chính bộ dùng để chỉnh lời dặn. Dòng "kín ngược chiều ⇒ không chỉnh" vì vậy không có thước để biết thế nào là "ngược chiều". Không có ngưỡng kín thì kết quả đạt chỉ dựa trên bộ đã chỉnh, dễ khớp quá sát (bài học B1 02/11: luật khớp 14 câu đã thấy, kín bắt 0 / 8). (2) Q-a / Q-c đo trên 33 ảnh × 2 lần nhưng không nói cả hai lượt cùng phải đạt, hay chỉ lượt 1, hay gộp | §5 thêm dòng kín: 8 ảnh trong danh sách ⇒ top-3 đúng ≥ k / 8 (vd ≥ 7 / 8) và 2 ảnh ngoài danh sách ⇒ bị ép tên ≤ x / 2 (vd 0 / 2); kín phạm ⇒ âm, không chỉnh. Ghi luật A/A: Q-a, Q-c, Q-d phải đạt ở **cả hai** lượt (hoặc cách khác, ghi rõ) |
| **M-2** | major | §2 A2 (route mới `POST /api/anh/ung_vien`, **multipart**); §6 dòng "Lạm dụng route" | **Route multipart mở đường gửi chéo trang mà route chat hiện không có** [suy luận theo đặc tả Fetch / CORS, chưa chạy]. `multipart/form-data` là kiểu "yêu cầu đơn giản": trang web lạ mà người dùng đang mở có thể `fetch` POST một ảnh tới server mà trình duyệt **không hỏi trước** (không preflight). Trang lạ không đọc được phản hồi, nhưng server vẫn xử lý và **gọi OpenAI có tính tiền**. Route chat hiện nhận JSON ⇒ có preflight ⇒ bị chặn. Rào "một lượt ảnh / phiên" cũng không giữ được: cookie phiên `SameSite=Strict` (`chat.py:131`) không đi theo yêu cầu chéo trang ⇒ mỗi yêu cầu là một "phiên" mới. Ảnh hưởng: tốn tiền / tài nguyên khi chatbot chạy trên máy User (thấp) và trên AWS ở Phase 12 (cao hơn). Đây là ranh giới bảo mật nên không hạ xuống minor | §6 thêm rào ở code: kiểm header `Origin` / `Sec-Fetch-Site` (chỉ cùng nguồn), hoặc bắt một header riêng (vd `X-Hue-Anh: 1` — làm yêu cầu thành "không đơn giản" ⇒ có preflight), hoặc gửi ảnh dạng JSON base64. Thêm test: yêu cầu thiếu header / khác nguồn ⇒ 403, **không** gọi model. Ghi vào bảng §10.2 mục 3 "Giới hạn ở API" |
| m-1 | minor | §10.1, §10.2 | Luật mới `Session_Prompt.md:118` ghi bảng rà khung phải có cột **mục · hiện trạng `file:dòng` · khớp / lệch · đề xuất**. Bảng hiện có 3 cột: thiếu "hiện trạng `file:dòng`" (vd CSP `app.py:38`, `ChatRequest` `chat.py:59-61`, cookie `chat.py:131`, chỗ gọi model mà route mới sẽ dùng) và thiếu "đề xuất" khi lệch. Nội dung hai bảng đủ mục của hai skill | thêm 2 cột; dòng nào "khớp" thì để trống ô đề xuất |
| m-2 | minor | §5 Q-d | Sàn "0 / 3 đầu ra ngoài schema hoặc có chữ tự do" gần như tự đạt: strict schema đã làm API không trả gì ngoài schema. Rủi ro thật (chọn đúng tên mà chữ lệnh trong ảnh đòi) lại chỉ là "theo dõi". Bản nghiên cứu §5.1 đề xuất "> 1 / 3 ⇒ dừng xét" | đổi Q-d thành: (i) test schema (giữ, là test); (ii) **sàn đo**: số ảnh chọn đúng tên kẻ tấn công đòi ≤ 1 / 3 (theo nghiên cứu), hoặc ghi rõ vì sao chỉ theo dõi (hậu quả = một tên sai còn phải bấm xác nhận) |
| m-3 | minor | §5 Q-a "mỗi loại ≥ 2/3 số ảnh của loại" | Chưa ghi cách làm tròn: loại biển tên có 2 ảnh ⇒ 2/3 × 2 = 1,33 (cần 2 / 2 hay 1 / 2?); cảnh 4 ⇒ 2,67; món 6 ⇒ 4. Người chấm có thể tính khác nhau | ghi số tuyệt đối cho từng loại (vd công trình ≥ 9 / 13, cảnh ≥ 3 / 4, món ≥ 4 / 6, biển tên ≥ 2 / 2) |
| m-4 | minor | §11 + spec Phase 9 bản 12 §11.4 | Cột Phase 10 trong spec Phase 9 §11.4 (đã duyệt) xếp **giọng nói trước** (10–16/11 STT, 17–23 code giọng nói, 24–30 ảnh). Spec này xếp **ảnh trước** và ghi "thay cột Phase 10 … A / User duyệt". Khi duyệt bản này thì hai spec đang hiệu lực mâu thuẫn nhau | khi duyệt: A sửa spec Phase 9 §11.4 cột Phase 10 (một dòng "theo spec Phase 10 §11") cùng lượt, hoặc spec này ghi rõ nó thay cột kia từ lúc được duyệt |
| m-5 | minor | §11 tuần 01–14/12 | Đo giọng nói trên máy (model STT chạy CPU, RAM lớn) trùng tuần Phase 9 B5b (01–07/12) và B6 (08–14/12) có lượt đo. Luật W31 (`WORKFLOW.md` §9.2): đang có lượt đo tốc độ ⇒ session khác không chạy việc nặng CPU. Cột "Ràng buộc" chỉ ghi "trước B7" | thêm ràng buộc: lượt đo giọng nói trên máy không chạy cùng lúc lượt đo Phase 9 (W31); A xếp giờ |
| m-6 | minor | §2 A2, §6 dòng "bom giải nén" (1) | (a) "Giới hạn byte trước khi đọc: `Content-Length` + đọc tối đa 10 MB": nếu plan khai báo tham số `UploadFile`, FastAPI / Starlette sẽ đọc và lưu cả phần thân yêu cầu ra file tạm **trước** khi vào hàm xử lý [Code, chưa chạy — Starlette 1.3.1, `python-multipart` 0.0.32 đã có trong `.venv`] ⇒ rào phải đặt trước bước phân tích (đọc `Request` thô, kiểm header rồi đọc luồng có giới hạn), hoặc plan ghi probe kiểm điều này. (b) Q-g ghi "ảnh **lưu lại** / gửi đi không còn EXIF", trong khi §6 nói không lưu ảnh ⇒ bỏ chữ "lưu lại" | plan bậc A1 ghi chỗ đặt rào byte + một probe 0 USD (gửi phần thân > 10 MB ⇒ bị từ chối trước khi ghi file tạm); sửa chữ Q-g |

**Không phải finding (đã kiểm, khớp):**
- `file:dòng` spec trích đều khớp `main`: CSP `app.py:38`; `ChatRequest` `max_length=500` `chat.py:61`; `STATUS_TEXT` `App.jsx:9-12`; xử lý sự kiện `status` `App.jsx:106`; data egress `Project_Status.md:224` (hiện chỉ có chữ + 10 đoạn kho tới OpenAI ⇒ ảnh đúng là đường ra mới, §12.1 có ghi User duyệt + A sửa §6).
- **CSP `blob:`** (A7): chỉ thêm `blob:` vào `img-src`, `connect-src 'self'` và `default-src 'self'` giữ ⇒ không mở mạng. URL `blob:` chỉ do script của chính trang tạo được; chữ Markdown của model lọt qua DOMPurify chỉ trỏ được tới blob đã tồn tại trong trang. Rủi ro thấp, có phương án giữ nguyên CSP (không xem trước). Đồng ý cần User duyệt.
- **Thư viện:** Pillow 12.3.0 và `python-multipart` 0.0.32 có sẵn trong `.venv` (kiểm `importlib.metadata`) ⇒ P1 không cần thư viện mới. `open_clip_torch` chưa có, `transformers` 5.14.1 có ⇒ P2 có thể không cần thêm thư viện, nhưng vẫn phải tải model (A6 đã ghi "User duyệt").
- **Nhãn số liệu** đối chiếu nghiên cứu E2: luna nhận ảnh [đã kiểm] · Kimura 15,8 % [đã kiểm] · SigLIP 2 Apache-2.0 [đã kiểm], 1,6 GB [tính] · chính sách dữ liệu OpenAI [đã kiểm] · token ảnh [đã kiểm trang + tính, ghi giả định] · Commons [đã kiểm] · HEIC iPhone [suy ra] — spec giữ đúng nhãn. Spec **sửa đúng** một chỗ nghiên cứu §4 ghi sai: nghiên cứu nói bước ảnh "không đủ ba" (không có kênh ra), spec §6 ghi OpenAI là đường ra và ảnh là dữ liệu riêng ⇒ đủ ba ở mức nhẹ — chặt hơn, đúng.
- **Tiền:** 140–175 lần gọi × 0,0003–0,0005 USD ≈ 0,042–0,088 [tính lại, khớp §7]; trần riêng 0,15 / dừng 0,13, ngoài quỹ Phase 9 và quỹ B7 — khớp spec Phase 9 §11.5 "Phase 10 có trần riêng"; mỗi phiên ≤ 1 USD gộp. Có bước 0 kiểm token ảnh trước lượt lớn.
- **Finding chuyển (§9):** M-4 đóng được — mẫu số tách (n_H = 25 / ngoài danh sách 5, Q-a / Q-c riêng), danh sách tên có nguồn + số đếm (28 + 29 + 9, ước 45–55 sau gộp, User duyệt ca trùng). m-7 đóng được — rào điểm ảnh 4 lớp, Pillow có sẵn (đã kiểm phiên bản). M-1, M-3 ghi "mở" đúng: phần giọng nói chưa viết; việc chuyển hợp lệ theo review v10 m-5 (spec trỏ lại mã trong "Căn cứ để review").
- Khám phá 5 dòng đủ; mốc M0 rẻ nhất có; phương án B (P2) có; "Không làm" rõ; A1 (không agent) và A3 (chữ model không vào câu hỏi kho) đúng chia việc code ↔ model; Q1 mở rộng cho cả cờ `anh` bật ⇒ route chat giống byte `main` — tốt.

### 3. Cách người kiểm chạy lại thật

Chỉ đọc, 0 USD: `sha256sum` hai spec; đọc các dòng code trích (`sed -n`); `uv run --project /home/minhhieu/hue_rag python -c "importlib.metadata.version(...)"` cho pillow / python-multipart / starlette / fastapi / transformers / open_clip_torch; tính lại tiền §7 bằng tay. Không gọi API, không tải gì.

### 4. Kết quả quan sát

Như mục 2 "Không phải finding". M-2 dựa trên đặc tả CORS (yêu cầu đơn giản với `multipart/form-data`), **chưa chạy probe** vì route chưa có — plan A1 nên có test chặn.

### 5. Giới hạn hoặc phần chưa chạy

- Không đọc file nghiên cứu giọng nói (E1, dở — ngoài căn cứ); §8 chỉ kiểm việc ghi trạng thái "mở" của M-1 / M-3.
- Không WebFetch lại nguồn ngoài (nhãn [đã kiểm] là của E; B chỉ đối chiếu spec ↔ nghiên cứu).
- Duyệt bản này **không** nên được hiểu là duyệt phần giọng nói: §8 còn là mục chờ, đường ra / model giọng nói phải duyệt khi viết đủ (spec nên ghi một dòng như vậy — gộp vào sửa M-1 nếu E muốn).

### 6. Decision và bước tiếp theo

**changes_requested.** E sửa M-1 (ngưỡng kín + luật A/A), M-2 (rào chống gửi chéo trang cho route multipart + test) và các minor, rồi báo sha mới. B kiểm phần sửa.

## Vòng 2 — kiểm phần sửa, spec bản 2 `bf67b90fb6fc` (E nhờ trực tiếp; sửa theo vòng 1 `62ffcac51b1a`)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 0 minor mới)
Người kiểm: B (`hue-rag-48`) · Date: 10:22 05/11/2026 (`date`) · sha bản 2 tính từ file lúc kiểm.

Kiểm theo mục "Chỗ đổi bản 2" của spec, rồi đọc lại các phần bị chạm (§2 A2 / A10, §4 A1 / A2, §5, §6, §7, §8, §10, §11). Code `main` = `b019aab` (sau merge B4b).

| Finding vòng 1 | Bản 2 | Kết quả |
|---|---|---|
| **M-1** kín không ngưỡng + luật A/A | §5 **Q-k**: 10 ảnh kín × 2 lượt sau khoá — trong danh sách ≥ 7 / 8, ngoài danh sách bị ép 0 / 2, cả hai lượt; phạm ⇒ âm, không chỉnh, không chạy lại. **Luật A/A** riêng: Q-a, Q-c, Q-d, Q-k đạt ở cả hai lượt, không lấy lượt tốt hơn / trung bình. P2 dùng bộ kín mới. §4 A2 khoá có sha trước kín | **đóng** |
| **M-2** gửi chéo trang qua multipart | **A10**: thân `image/jpeg|png|webp` (không thuộc 3 kiểu "đơn giản" ⇒ trình duyệt phải preflight; server không bật CORS — đã kiểm `app.py` chỉ `include_router`, không có middleware CORS; `<form>` không gửi được kiểu này) + lớp 2 trước khi đọc thân: `Sec-Fetch-Site` ≠ `same-origin` / `Origin` khác gốc ⇒ 403, `Content-Type` khác ⇒ 415; Q-j sàn test "0 lần gọi model"; probe 11 MB. B kiểm thêm một đường lách [suy ra theo đặc tả Fetch, chưa chạy]: `fetch` chế độ `no-cors` với thân Blob `image/jpeg` ⇒ trình duyệt **bỏ** header `Content-Type` không an toàn ⇒ yêu cầu tới không có `Content-Type` ⇒ 415 của A10 bắt (và `Sec-Fetch-Site: cross-site` ⇒ 403). Đủ hai lớp | **đóng** |
| m-1 bảng FDE thiếu cột | §10.1 / §10.2 có cột hiện trạng `file:dòng` + đề xuất. B kiểm từng `file:dòng` trên `b019aab`: `assistant.py:382` `_pick_route` · `chat.py:114` `_model_query` · `settings.yaml:64` `router_timeout_seconds` · `:67-68` nhớ · `generator…:314` `_run` · `:198-201` `tracing_disabled` · `chat.py:36`, `:162` log số đếm · `:107-111` `_remember` · `:62-64` `ChatRequest` · `:90`, `:131` cookie `SameSite=Strict` · `app.py:38` CSP · `app.py:166-168` router — **khớp hết**. Dòng §4 hạn giờ ghi "lệch nhẹ" + đề xuất 15 s ở plan — hợp lý | **đóng** |
| m-2 Q-d tự đạt | Q-d thành sàn đo ≤ 1 / 3 mỗi lượt chọn đúng tên kẻ tấn công đòi (tên hợp lệ khác), ca khó thật; schema thành test | **đóng** |
| m-3 làm tròn | 9 / 13 · 3 / 4 · 4 / 6 · 2 / 2 (làm tròn lên) + "cỡ loại đổi ⇒ ghi lại trước khi đo" | **đóng** |
| m-4 hai spec mâu thuẫn lịch | §11: thay cột Phase 10 của spec Phase 9 §11.4 kể từ lúc User duyệt; A ghi dòng trỏ ở `CURRENT_HANDOFF.md` | **đóng** (A nhớ ghi dòng trỏ khi duyệt) |
| m-5 W31 | §11 ghi ràng buộc ở 10–16/11, 17–23/11, 01–14/12; §4 A2 | **đóng** |
| m-6 rào byte + chữ "lưu lại" | A10 (3): `Content-Length` + đọc `request.stream()` có bộ đếm, không `UploadFile` / `Form`; probe 11 MB ở A1 (RAM không tăng theo cỡ thân); Q-g "không ghi ảnh ra đĩa" | **đóng** |
| §5 vòng 1 "duyệt không gồm giọng nói" | §8 dòng đầu ghi rõ; giọng nói cần bản sửa đổi riêng có review | **đóng** |

**Nhận xét (không phải finding, không cần sửa trước khi duyệt):** §7 ước 150–185 lần gọi. Luật A/A làm mỗi vòng chỉnh cũng cần 2 lượt mới quyết được ⇒ tối đa 66 + 2 × 66 + 20 = 218 lần ≈ **0,065–0,11 USD**, vẫn dưới dừng 0,13. Plan A2 nên ghi rõ số lượt mỗi vòng.

**Kết luận:** mọi finding vòng 1 đã đóng, không có finding mới ⇒ **ready_for_user_confirmation**. A trình User gói duyệt §12 (đường ra ảnh tới OpenAI, tải ảnh Commons, CSP `blob:`, trần 0,15) cùng spec; phần giọng nói (§8) không thuộc lần duyệt này.
