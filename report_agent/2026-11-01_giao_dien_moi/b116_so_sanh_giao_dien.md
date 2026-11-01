# B116 — So sánh cách làm giao diện mới (tư liệu để User chọn, chưa code)

B, 14:39 01/11/2026 (`date`); sửa 14:46 01/11/2026 theo quyết định User + A 14:45 (laptop, công nghệ, yêu cầu 18, dò CSP); thêm hướng nhìn 14:59 01/11/2026 (User chốt 14:53 + 14:57). Việc: `session_prompt/CURRENT_HANDOFF.md` mục B116 (A giao 14:36; User chọn (a)). 0 USD, không sửa code, không cài gói.
Nhãn: **[Chạy]** = đã kiểm thật bằng lệnh / file (0 USD) · **[Suy ra]** = từ đọc code / hiểu biết thư viện, chưa chạy · **[Ước]** = ước công, chưa làm.

## Căn cứ để review
1. `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md` — đọc cả 17 yêu cầu.
2. `frontend/app.js`, `frontend/index.html`; `backend/api/app.py:28-46, :155-165` (cách phục vụ trang + CSP); `backend/api/routes/chat.py:304-316` (`finish`: chữ cuối được chuẩn hoá nhưng **không gửi lại** cho giao diện).
3. `data/phase_8_2/b0/ket_qua_b0_2026-11-01.md` (ý citation) · `report_agent/2026-10-31_streaming_spec/s4_do_d2_implementation.md:39-56` (số D5).
4. Ghi chú dự án khác (private): `data/giao_dien_moi_2026-11-01/tham_khao_du_an_khac.md`.

## Đã chọn (User + A, 14:45 01/11/2026 — `CURRENT_HANDOFF.md` mục B116)
- **Thiết bị:** làm cho **laptop** (hiện chỉ User dùng); điện thoại chỉ cần không vỡ, không tốn công riêng.
- **Công nghệ (User để A chọn):** **React + Vite build tĩnh, FastAPI phục vụ** — tức PA-B dưới đây, cộng hai điểm:
  - **Tailwind được dùng** (CSS sinh lúc build ⇒ không đụng CSP);
  - **shadcn / Radix chỉ dùng linh kiện nào qua dò CSP 0 vi phạm** — xem mục "Bước đầu khi code".
- **Không dùng Next:** cần server Node hoặc export tĩnh, thêm phần dựng trang phía server không cần.
- **Thêm yêu cầu 18** (mục dưới). Nguồn: B khuyên hiện số nhỏ bấm được; D5: B khuyên giữ PA1 — hai mục này vẫn chờ A / User chốt.
- Giao diện mới **không cần đổi API, không nới CSP**. Bản cũ (JS thuần) đạt 16 / 17 yêu cầu, chỉ thiếu yêu cầu 17 (huỷ `fetch`).

## Ba phương án đã cân (hồ sơ — đã chọn PA-B + Tailwind + shadcn đã dò)

| | **PA-A — JS thuần làm lại** (bỏ) | **PA-B — React + Vite, CSS tự viết** (**đã chọn**, làm nền) | **PA-C — React + Vite + Tailwind + shadcn/ui** (lấy một phần: Tailwind + linh kiện đã dò) |
|---|---|---|---|
| Đổi gì | Giữ `frontend/`, viết lại HTML / CSS, tách `app.js` thành vài module ES (`type="module"`), giữ `vendor/marked` + `purify` | Thư mục mới (ví dụ `frontend/`, nguồn `src/`, bản build `dist/`); FastAPI phục vụ `dist/` (Vite `base: "/static/"` ⇒ giữ đường `/static`); `marked` + `dompurify` thành gói npm | Như PA-B + Tailwind v4 (CSS sinh lúc build) + linh kiện shadcn (chép vào repo, dựa trên Radix) |
| Công [Ước] | thấp: ~0,5–1 ngày agent | vừa: ~1–1,5 ngày (chuyển parser SSE + vẽ chữ sang hook / component; sửa `app.py` vài dòng phục vụ `dist/`; viết lại `test_static_ui.py`; Playwright kiểm lại) | vừa–cao: PA-B + ~0,5–1 ngày (cài, cấu hình, **dò CSP** từng linh kiện) |
| Thêm vào quy trình | không | Node + `npm run build` trước khi chạy / deploy (máy có Node v24.19, npm 11.17 [Chạy]); khoá phiên bản + lockfile | như PA-B + nhiều gói hơn (Radix, tiện ích Tailwind) |
| CSP (yêu cầu 14) | như hiện nay — đạt | bản build Vite chỉ có `<script type="module" src=…>` ngoài, bundle React 0 `eval` / `new Function` [Chạy — grep trên một bản build React + Vite thật của một dự án khác của User]; dev mode chạy trên server Vite, không qua CSP ⇒ kiểm CSP trên bản build | **rủi ro:** một số linh kiện Radix (hộp thoại, khoá cuộn) tự chèn thẻ `<style>` lúc chạy ⇒ bị `style-src 'self'` chặn trừ khi có nonce [Suy ra, chưa chạy — phải dò trước khi chọn] |
| Không CDN (15) | đạt | đạt nếu font tự host trong bản build (dự án khác dùng Google Fonts CDN — **không chép**) | như PA-B |
| Lọc HTML (13) | giữ y nguyên | giữ `marked` → `DOMPurify` với **đúng** danh sách 25 thẻ / 4 thuộc tính, đưa vào bằng `dangerouslySetInnerHTML` sau lọc | như PA-B |
| Phase 9 (nhiều lượt) | khó: tự quản trạng thái nhiều tin bằng tay | dễ: mỗi tin một component, trạng thái luồng theo từng tin | dễ, có sẵn linh kiện (khung chat, hộp thoại) |
| Khi nào sai | Phase 9 thêm nhiều màn hình ⇒ phải làm lại lần nữa (trái "làm một lần") | giao diện chỉ dừng ở một ô hỏi ⇒ thêm Node / build là thừa | CSP chặn style chạy lúc dùng ⇒ hoặc nới CSP (cấm) hoặc bỏ linh kiện; nhiều gói hơn ⇒ rủi ro chuỗi cung ứng lớn hơn, khó tự giải thích |
| Chọn khác mất gì | so PA-B: mất cấu trúc component cho Phase 9 | so PA-A: thêm bước build + gói npm (cần User duyệt dependency, `Session_Prompt.md` §4); so PA-C: tự viết CSS, ít linh kiện sẵn | so PA-B: thêm công + rủi ro CSP, đổi lại đẹp nhanh hơn |

Phương án đã xét và bỏ: **htmx + SSE**. Phần mở rộng SSE của htmx nhận HTML do server dựng, còn API của mình gửi JSON ⇒ phải đổi API (chạm điều kiện dừng của B116).

**Tự kiểm (để User biết mình đã hiểu):** "Vì sao PA-B không phải nới CSP, còn PA-C thì có thể?"
Đáp: bản build Vite chỉ nạp script từ file của chính server. Còn vài linh kiện Radix tự chèn thẻ `<style>` lúc chạy, mà `style-src 'self'` chặn thẻ đó.

## Yêu cầu 18 (thêm vào 17 yêu cầu của `yeu_cau_cho_giao_dien_moi.md`)
18. Link nguồn bắt **cả** `[n]` lẫn `[Nguồn n]`. Lý do: giao diện vẽ chữ thô từ các mảnh `delta`; server chỉ chuẩn hoá chữ cuối để so (`delta_matches_final`), không gửi lại (`chat.py:304-316`); bản cũ chỉ bắt `[\d+]` (`app.js:44`).
    - Đổi chỗ nào: chỉ trên nút chữ, sau bộ lọc HTML.
    - Cách hiện: hai dạng cùng hiện thành số nguồn gọn (mục "Ý B0" dưới).
    - Kiểm: một ca Playwright có `[Nguồn n]` trong chữ ⇒ thành link sau `sources`.
    - Nguồn: B116 phát hiện, A kiểm code xác nhận.

## Bước đầu khi code: dò CSP cho shadcn / Radix (chưa làm bây giờ)
Mục đích: biết linh kiện nào dùng được mà **không nới CSP** (yêu cầu 14).
- **Ở đâu:** worktree riêng `/tmp/…`. Cài gói npm cần User duyệt dependency (`Session_Prompt.md` §4) — A ghi khi giao việc code.
- **Làm:**
  1. Dựng khung Vite + React + Tailwind.
  2. Thêm từng linh kiện định dùng (ví dụ nút, ô nhập, vùng cuộn, tooltip, hộp thoại).
  3. `npm run build`.
  4. Cho FastAPI phục vụ `dist/` với **đúng** `FRONTEND_CSP` hiện tại (`app.py:33-34`).
  5. Playwright mở trang, bấm mở từng linh kiện, nghe sự kiện `securitypolicyviolation` + đọc console + đếm request ra ngoài máy.
- **Tiêu chí ghi trước:** mỗi linh kiện **0 vi phạm CSP** và **0 request ra ngoài** khi mở / đóng.
  - Linh kiện nào vi phạm ⇒ không dùng; tự viết bằng React + Tailwind thay. Không nới CSP, không thêm nonce chỉ để cứu một linh kiện.
- **Nghi trước [Suy ra]:** hộp thoại / khoá cuộn của Radix có thể chèn thẻ `<style>` lúc chạy.
- **Đầu ra:** bảng linh kiện → đạt / không đạt, ghi trong report của việc code.

## Khớp 17 yêu cầu — chỗ cần chú ý khi làm lại (áp cho mọi phương án)
- **1–7 (gọi API, sự kiện SSE, parser):** chuyển nguyên logic `app.js:104-187`, không đổi hợp đồng. Parser vẫn phải chịu được ba ca: một sự kiện bị cắt qua nhiều lần đọc, nhiều sự kiện trong một lần đọc, và UTF-8 cắt giữa byte (`TextDecoder` `stream: true`). Không dùng `EventSource`, vì nó không gửi được `POST` có thân câu hỏi [Suy ra].
- **8 (vẽ lại cả buffer theo khung hình):** React ⇒ giữ `text` trong state, vẽ theo `requestAnimationFrame` như hiện nay, không vẽ lại cho từng mảnh.
- **9 + ý B0 về nguồn:** xem mục dưới.
- **10–12 (xoá khi lỗi, "Thử lại", khoá ô hỏi):** giữ nguyên.
- **17 (huỷ `fetch`):** thêm `AbortController` — huỷ khi rời trang, đóng tab, bấm hỏi lại (PA-B: thêm khi component bị gỡ). Đây là chỗ **duy nhất** bản cũ chưa có.
- **Kiểm khi làm lại:** dùng lại `probe_v2.py` (25 ca dò lọc HTML ⇒ 0 request ra ngoài) và Playwright trên server thật, như mục "Kiểm khi làm lại" của file yêu cầu.

## Ý B0 (1): hiển thị nguồn gọn thay cho `[n]` chen trong câu
`[n]` vẫn giữ ở tầng máy (validator, sàn có citation). Giao diện chỉ **đổi cách hiện**, không đổi API.

| Cách | Hiện thế nào | Mất gì |
|---|---|---|
| **(i) số nhỏ nâng lên, bấm được** (B khuyên) | `[2]` ⇒ số ² nhỏ cạnh chữ; bấm thì mở / nhảy tới thẻ nguồn; dưới câu là danh sách nguồn gọn (chỉ tiêu đề, bấm mở đoạn trích) | gần như không mất — vẫn biết ý nào từ nguồn nào |
| (ii) bỏ số, chỉ danh sách nguồn cuối | câu sạch nhất | không biết ý nào dựa nguồn nào ⇒ người dùng khó kiểm, yếu đi mục tiêu "có nguồn" |
| (iii) gom số về cuối mỗi đoạn | ít chen hơn (i) | một đoạn nhiều nguồn ⇒ mờ nguồn từng ý |

Hai điểm kỹ thuật cho (i):
- Trước khi có sự kiện `sources`, số chỉ là chữ mờ, không bấm được (yêu cầu 9).
- Đổi số **sau** bộ lọc HTML, trên nút chữ, như `wireCitations` hiện nay. Không chèn HTML vào chuỗi trước khi lọc.

**Lỗ hổng phát hiện thêm [Suy ra từ code]:** giao diện vẽ chữ **thô** từ các mảnh `delta`. Server có chuẩn hoá `[Nguồn n]` → `[n]` (`chat.py:306`) nhưng không gửi lại bản đã chuẩn hoá. Trong khi đó model viết `[Nguồn n]` ở 24 / 465 lần (bẫy `Project_Status.md` §8), mà `wireCitations` chỉ bắt `[\d+]`.
- Hệ quả: những lần model viết `[Nguồn n]` thì số đó không thành link — ở bản cũ và cả bản mới nếu chép nguyên.
- Cách sửa (không đổi API): giao diện mới bắt cả hai dạng.
- ⇒ **yêu cầu 18** (mục trên; A kiểm code xác nhận). Chưa chạy để thấy tận mắt; cờ log `delta_matches_final` đếm được tần suất. Bản cũ không sửa, vì sắp thay.

## D5: giữ PA1 (chữ hiện dần) hay PA3 (chỉ tiến độ, câu hiện một lần)
- **Số S4** (38 câu, trình duyệt thật, một lần đo): chữ đầu p50 1,23 / p95 2,61 s; đủ câu p50 1,73 / p95 3,81 s.
- **Lợi theo cặp** (chữ đầu sớm hơn đủ câu): trung vị 0,44 s, CI 95 % [0,37; 0,54]. Khoảng tin cậy **chứa** mốc 0,5 s. Câu dài lợi 0,51 s.
- Hôm đo, model gần như không suy luận (trung vị 0 token) ⇒ lợi thấp hơn ngày model suy luận nhiều.
- **B khuyên giữ PA1**, vì:
  1. Code + kiểm của PA1 đã xong; PA3 không bớt được phần khó nào (vẫn cần parser SSE, xoá khi lỗi).
  2. Câu dài và ngày model suy luận nhiều thì lợi lớn hơn.
  3. Rủi ro "đọc chữ rồi bị rút" đo được rất thấp (lỗi kiểm cuối 0 / 489, spec streaming dòng 210).
- **Khi nào sai:** log dùng thật cho thấy số lần rút / xoá vượt luật D5 (> 1 % câu / tuần, hoặc ≥ 3 lần trên ≥ 100 câu) ⇒ đổi sang PA3.
- **Chọn PA3 thì mất:** chữ hiện chậm hơn ~0,4–0,5 s. Đổi lại không bao giờ có cảnh chữ đã hiện bị xoá.
- Cả hai đều chỉ là hành vi giao diện; API giữ nguyên.

## Hướng nhìn (User chốt 14:53 + 14:57 01/11/2026 — `CURRENT_HANDOFF.md` mục B116)
**Đề bài:**
- Bây giờ chỉ có **trang hỏi đáp**, khung nguồn nằm bên cạnh. Phase 9 sẽ nâng cấp thêm.
- Phong cách: hiện đại, gọn, nét Huế nhẹ. Nền sáng trung tính, màu nhấn **tím Huế** (nút, link nguồn, tiêu đề), một font tự host; không hoa văn, không ảnh nền.
- Khung: skill `frontend-design`.

**Điểm nhớ duy nhất (chỗ dành cho cái riêng):** số nguồn màu tím trong câu. Bấm số ⇒ đúng nguồn đó ở khung bên sáng lên. Mọi thứ khác giữ yên, gọn.

### Bố cục (laptop ≥ 900 px; hẹp hơn ⇒ khung nguồn xuống dưới câu trả lời)
```text
┌────────────────────────────────────────────────────────────────────────┐
│ Hỏi về Huế  (tím, đậm 600)                Trả lời từ kho tư liệu về Huế │  thanh đầu mảnh, viền dưới
├─────────────────────────────────────────────┬──────────────────────────┤
│ Câu bạn hỏi (in lại, đậm 600)                │ Nguồn                    │
│                                             │ 1  Tiêu đề nguồn          │
│ Câu trả lời, chữ hiện dần … ý thứ nhất¹ …    │    mục › mục con          │
│ … ý thứ hai² …                              │    ▸ xem đoạn trích       │
│                                             │ ───────────────────────── │
│ Đang viết câu trả lời…  (chữ mờ, dòng trạng  │ 2  Tiêu đề nguồn  ◀ sáng  │
│ thái)                                       │    (nền tím nhạt khi bấm²)│
│                                             │  (khung dính khi cuộn)    │
├─────────────────────────────────────────────┤                          │
│ ┌─────────────────────────────────┐ ┌──────┐ │                          │
│ │ Hỏi gì về Huế…  (nhiều dòng)     │ │ Hỏi  │ │                          │
│ └─────────────────────────────────┘ └──────┘ │                          │
└─────────────────────────────────────────────┴──────────────────────────┘
  cột chính rộng tối đa ~720 px (≈ 70 ký tự / dòng), canh trái    cột nguồn ~340 px
```
- **Ô hỏi ở dưới**, như khung chat: Phase 9 thêm nhiều lượt thì không phải dời. Enter = gửi, Shift + Enter = xuống dòng.
- Nguồn là **danh sách thường**: đánh số (vì là số thật của nguồn), giữa các mục là một vạch mảnh. Không làm thẻ bo góc có bóng giống nhau. Đoạn trích gập lại, bấm mới mở.

### Bảng màu (token CSS / Tailwind `@theme`; tương phản tính bằng công thức WCAG 2 trong Python [Chạy])

| Token | Hex | Dùng cho | Tương phản |
|---|---|---|---|
| `bg` | `#F6F6F8` | nền trang (xám lạnh, không kem) | — |
| `surface` | `#FFFFFF` | cột chính, khung nguồn, ô hỏi | — |
| `text` | `#211D27` | chữ thường | 16,54 trên `surface` · 15,32 trên `bg` |
| `muted` | `#5E5866` | dòng trạng thái, mục › mục con, số nguồn **trước** khi bật | 6,85 / 6,35 |
| `accent` (tím Huế) | `#5B2C83` | tiêu đề, nút, số nguồn đã bật, viền focus | 9,85 trên `surface` · 9,12 trên `bg` |
| `accent-strong` | `#47206A` | nút khi rê / bấm | chữ trắng trên nó 12,48 |
| `on-accent` | `#FFFFFF` | chữ trên nút | 9,85 trên `accent` |
| `accent-soft` | `#F1EBF7` | nền nguồn đang được trỏ | `text` 14,15 · `accent` 8,42 |
| `line` | `#DCD8E1` | vạch chia, viền trang trí | 1,40 — **chỉ trang trí**, không dùng làm viền ô nhập |
| `field-line` | `#7D7785` | viền ô hỏi / nút viền | 4,33 trên `surface` (≥ 3 : 1 cho viền linh kiện) |
| `error` | `#A4262C` | chữ lỗi | 7,26 trên `surface` · 6,38 trên `error-soft` |
| `error-soft` | `#FBEDEE` | nền hộp lỗi | `text` 14,53 |

Mọi cặp chữ / nền đạt **AA (≥ 4,5 : 1)**, phần lớn đạt cả AAA (≥ 7). Màu tím chỉ dùng đúng 3 chỗ User nêu, cộng viền focus.

### Chữ
- **Be Vietnam Pro** — giấy phép **OFL**, do người Việt thiết kế, có bộ chữ `vietnamese`. Đã đọc `METADATA.pb` của Google Fonts [Chạy — WebFetch].
- Hai độ đậm 400 + 600, chỉ dạng đứng; thêm 400 nghiêng chỉ khi câu trả lời hay có chữ nghiêng.
- File `woff2` (bộ latin + vietnamese) **nằm trong bản build**: dùng gói font npm hoặc chép file vào `src/` — chọn khi code. Không dùng Google Fonts CDN (yêu cầu 15).
- Font dự phòng khi tải lỗi: `system-ui, "Segoe UI", sans-serif`.
- Cỡ chữ: thân 17 px, dòng cách 1,65 (laptop đọc dài); câu hỏi in lại 20 px / 600; tên trang 20 px / 600 tím; khung nguồn 15 px.
- Không chữ in hoa toàn bộ, không nhãn nhỏ đặt trên mỗi tiêu đề.

### Trạng thái (lời lấy từ server / bản cũ; không đổi API)

| Lúc | Cột chính | Khung nguồn | Ô hỏi |
|---|---|---|---|
| Chưa hỏi | một câu: "Hỏi về di tích, món ăn, lễ hội, nghệ thuật và du lịch Huế. Câu trả lời dựa trên kho tư liệu, có ghi nguồn." | trống (ẩn khung) | mở |
| Đang tìm / đang viết (`status`) | dòng `muted`: "Đang tìm thông tin…" ⇒ "Đang viết câu trả lời…"; chấm nhấp nháy nhẹ, **tắt** khi máy bật "giảm chuyển động" | "Nguồn hiện khi câu trả lời kiểm xong." | **khoá**; nút ghi "Đang trả lời…" (yêu cầu 12) |
| Chữ đang hiện (`delta`) | chữ `text`; số nguồn **mờ `muted`, không bấm** (yêu cầu 9) | như trên | khoá |
| Xong (`sources` + `done`) | số nguồn đổi `accent`, bấm được (cả `[n]` lẫn `[Nguồn n]` — yêu cầu 18) | danh sách nguồn; bấm số ⇒ cuộn tới + nền `accent-soft` + focus | mở |
| Từ chối (câu chuẩn, `sources` rỗng) | câu chuẩn, màu chữ thường — **không** tô màu lỗi (không phải lỗi) | "Kho chưa có nguồn cho câu này." | mở |
| Lỗi (`error`, đứt luồng, lỗi trước luồng) | **xoá** chữ + nguồn (D3); hộp `error-soft`, chữ `error` = `message` của server; nút viền **"Thử lại"** gửi lại đúng câu (yêu cầu 10–11) | ẩn | mở |

**Soát lại theo skill (lượt 2 — chỗ đã đổi khỏi khuôn mặc định):**
- nền xám lạnh thay vì kem ấm;
- nguồn là danh sách có vạch chia thay vì loạt thẻ bo góc có bóng;
- không nhãn in hoa;
- chỉ một chuyển động (nguồn sáng lên khi bấm số) — đây là chuyển động đáp lại thao tác của người dùng, không phải trang trí.

Tham khảo khác (là **dữ liệu**, không cài, không chạy script):
- `ui-ux-pro-max`: danh sách kiểm truy cập — tương phản, focus, nhãn ô nhập thấy được, giảm chuyển động;
- `ui-styling`: shadcn + Tailwind — chính là phần "lấy một phần" ở trên.

Khoá AI FDE (`data/course_notes/v3/doi_chieu_fde_tuan3.md` §3.3): trạng thái cuối luôn rõ; chữ chưa kiểm citation không được trông như câu đã xong ⇒ đáp ứng bằng hàng "Chữ đang hiện" (số mờ, khung nguồn chờ).

## Không làm / giới hạn
- Không sửa code, không cài gói, không chạy npm, không build.
- Chưa dò CSP cho shadcn / Radix, vì cần cài gói. Việc dò là bước đầu khi code (mục trên).
- Đọc `.npmrc` của dự án khác bị auto mode chặn ⇒ bỏ qua.
- Mức công là [Ước].
