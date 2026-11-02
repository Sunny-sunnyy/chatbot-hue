# Review: Phase 9 B1 — plan (`2026-11-02-phase-9-b1-plan.md`)

Người kiểm: C (Claude Opus 5.5, `hue-rag-cc`) · việc **C129** · 19:46 02/11/2026 (`date`). Skill `risk-gated-agent-review`.
Bản được review: **bản 1 sha `0bc74ed957e7`** (C tính lại từ file — khớp).
Chỉ dựa "Căn cứ để review" (plan; spec bản 9 §3, §4, §5 B1, §8; `data/phase_9/bo_do_b1/README.md` + `luat_gan_nhan_tuyen.md`; `cau_khan_cap_soan_san.md` Bản 1) và phần "đọc thêm khi cần" (code `215a77f`). Không đọc `STATUS_B` / tin nhắn B.
**Lưu ý vai:** C là người viết bộ đo B1 (C123 / C125). File này không nêu nội dung câu nào trong bộ đo, kín hay đã thấy; chỉ ghi số đếm và loại câu.

A đã quyết trước hai mục: **D7** (dòng ngày ở đầu tin nhắn người dùng) và **trần 0,25 USD**. Hai mục này không thành finding; C chỉ xét D7 có làm hỏng thước đo không (xem m-4).

## 1. Phạm vi đã review

- **6 phần so với spec §5 B1.** Định tuyến, trò chuyện, ngoài phạm vi, khẩn cấp, ngày, H4c: mỗi phần có cờ, có chỉ số / sàn ghi trước và có hành động khi "không đạt". Các con số chép **đúng** spec:
  - định tuyến ≥ 90 % trên 40 câu đã thấy;
  - sàn 1 / sàn 2;
  - ngày: giảm ≥ 3 trên 12 câu quyết, 2 lượt, mốc cùng ngày;
  - khẩn cấp: 0 câu vào model, 0 câu thường bị chặn;
  - H4c: 3 ca test.
- **Bộ đo dùng đúng cách:** "đúng" = `nhan` ∪ `chap_nhan`; khẩn cấp 10 câu đã thấy + 16 câu kín (8 + 8); ngày có 12 câu quyết. Riêng nhóm `out_of_scope` của Golden thì không đúng, xem M-1.
- **Thứ tự lượt, ranh giới mạng, đường lỗi, tiền:**
  - D1: luật khẩn cấp đứng trước định tuyến.
  - D3: định tuyến không có công cụ; lỗi ⇒ `tro_ly_hue`; agent nằm trong module OpenAI nên T-3 giữ nguyên.
  - Tiền ≈ 0,14 USD (spec 0,16).
  - Điều kiện dừng có "kín ngược chiều ⇒ không chỉnh rồi đo lại".
  - **Khớp.**
- **Bốn điểm A dặn xem kỹ** (luật khẩn cấp ↔ sàn "0 câu thường bị chặn", khoá trước khi mở kín, D6 lỗi Qdrant thành SSE `error`, P6) và m-1 của C128: xem §2.

## 2. Findings

**0 blocker · 3 major · 5 minor.**

### M-1 (major) — nhóm `out_of_scope` của Golden bị loại khỏi sàn 1 và bị coi là đi `ngoai_pham_vi`, nhưng 7 / 18 câu vẫn là câu về Huế

- **Vị trí:** §4 P1 sàn 1 ("208 — mọi câu Golden / an toàn **trừ nhóm `out_of_scope`** coi là `tro_ly_hue`"); §9 dòng "Golden `out_of_scope` đi tuyến `ngoai_pham_vi`".
- **Bằng chứng** (C đếm 0 USD, chỉ in số, không in câu): trong 18 câu Golden `out_of_scope`, có **7 câu nhắc "Huế"**. Theo luật gán nhãn của bộ đo, những câu này là `tro_ly_hue`. `luat_gan_nhan_tuyen.md` dòng `tro_ly_hue`: "Kho có hay không có thông tin đó không quan trọng" (kho không có thì trợ lý từ chối, hoặc B6 tra web). `out_of_scope` của Golden nghĩa là "**kho** không có", không phải "**ngoài chủ đề Huế**". Hai nghĩa này khác nhau.
- **Tác động:**
  - (1) Định tuyến đưa những câu Huế này sang `ngoai_pham_vi` thì người dùng nhận "chỉ hỗ trợ thông tin Huế" cho chính một câu về Huế. Sàn 1 không bắt được vì nhóm này bị loại khỏi phép đếm.
  - (2) Ở B6, cổng web đòi tuyến `tro_ly_hue`, nên các câu này **không bao giờ** được tra web. Đây đúng là loại câu B6 muốn giúp.
  - (3) S-OOS vẫn "đạt" (vì `is_refusal` nhận cả hai câu từ chối), nên lỗi bị che.
- **Tiêu chí đóng:** plan ghi **trước** nhãn tuyến cho 18 câu `out_of_scope` theo đúng luật gán nhãn. Câu về Huế ⇒ `tro_ly_hue`, và được tính vào sàn 1. Câu ngoài chủ đề Huế ⇒ `ngoai_pham_vi` (`chap_nhan` `tro_ly_hue`).
  - Nhãn do người không code gán. C làm được ngay (0 USD, ≈ 10 phút) và giao danh sách `case_index` + nhãn.
  - Sửa dòng §9 cho đúng.

### M-2 (major — cần A quyết, vì chạm chữ spec) — hành động "không đạt ⇒ tắt luật" của P3 đi ngược mục tiêu khi luật **sót** câu khẩn cấp kín

- **Vị trí:** §4 P3 ("sàn: 0 câu khẩn cấp vào model — 14 / 14 đã thấy và **8 / 8 kín**… ; 0 câu thường bị chặn…; không đạt ⇒ **tắt `emergency_rule`**"); §2 D2 "Sai khi".
- **Lập luận:** P3 gộp hai sàn có hậu quả ngược nhau.
  - **Chặn nhầm câu thường** là hại thật: người dùng hỏi bình thường lại nhận câu số khẩn cấp. Ở trường hợp này, tắt luật là đúng.
  - **Sót một câu khẩn cấp kín** thì câu đó vẫn đi định tuyến. D1 nói tuyến `khan_cap` do định tuyến chọn cũng trả Bản 1. Nếu vì vậy mà tắt luật, thì **cả 14 câu đã bắt được cũng vào model**, tức kết quả **tệ hơn** so với giữ luật, trên đúng sàn đang đo.
  - Luật mẫu chữ viết từ 14 câu đã thấy khó bắt đủ 8 / 8 câu kín, vì phần kín cố ý khác loại và khác cách gõ (README bộ đo). Nên nhánh "tắt luật" có khả năng cao bị kích hoạt.
  - Spec §5 B1 ghi "Không đạt ⇒ tắt luật" cho cả dòng. Plan chép đúng chữ, nhưng hệ quả này spec chưa xét.
- **Tiêu chí đóng (A chọn, ghi trước):** tách P3 thành:
  - (a) **sàn chặn nhầm:** 0 câu thường bị chặn (208 + 36 + 5 + 8 kín). Không đạt ⇒ tắt luật;
  - (b) **độ phủ:** 14 / 14 đã thấy (sàn). Trên 8 câu kín thì **báo số** bắt bởi luật / bắt bởi định tuyến / sót cả hai. Sót cả hai ⇒ kết quả âm, ghi lại, **không** tắt luật. Không chỉnh rồi đo lại kín, đúng luật §7.
  - Đồng thời P1 phải chạy định tuyến trên những câu khẩn cấp kín mà luật sót, để biết lưới thứ hai có bắt không. Hiện P1 chỉ chạy 40 + 5 + 208 + 20 câu tuyến kín.

### M-3 (major) — P6 "4 cờ tắt ⇒ giống byte B0" chỉ so chuỗi gửi model; hợp đồng HTTP / SSE vẫn đổi khi tắt hết cờ

- **Vị trí:** §2 D6 (tìm kho chạy **trong** luồng ⇒ lỗi Qdrant thành sự kiện `error` thay JSON 503; thêm trạng thái `routing`); D9 / §4 P6 ("bằng chứng gỡ được").
- **Bằng chứng (code `215a77f`):** hôm nay lỗi tìm kho ở route stream ⇒ JSON 503 `retrieval_unavailable`, **trước** khi mở luồng (`chat.py:156-175`). Theo D6, thứ tự đổi bất kể cờ: luồng mở trước, rồi mới định tuyến / tìm. Plan không nói khi `router` tắt thì có còn trạng thái `routing` và có còn lỗi trong luồng không.
- **Tác động:**
  - Spec §5 B1 đòi "mỗi phần có cờ riêng, gỡ độc lập". Tắt `router` mà hợp đồng lỗi stream vẫn khác B0 thì phần "định tuyến" chưa gỡ được hết.
  - P6 sẽ báo PASS (chuỗi gửi model giống byte) dù hành vi người dùng thấy khi có lỗi đã khác.
- **Tiêu chí đóng (một trong hai, ghi trước):**
  - (a) `router` tắt ⇒ tìm kho chạy **trước** khi mở luồng như B0, không có trạng thái `routing`. P6 thêm 1 test "4 cờ tắt + Qdrant lỗi ⇒ JSON 503 giống B0" và so thứ tự sự kiện SSE của 1 câu với B0;
  - (b) ghi rõ trong P6 / §1 rằng đổi hợp đồng lỗi là **không gỡ bằng cờ** (đổi cố ý của lõi mới), kèm lý do. A quyết.

### m-1 (minor) — đưa m-1 của C128 vào plan

`/api/chat` và `answer_case` bỏ `llm_calls` khi model đã trả lời mà lượt vẫn lỗi (JSON hỏng / hết giờ sau phản hồi); route stream thì vẫn ghi ở `finally` (`b127_review.md` m-1). B1 dựng lại lõi (`answer_turn`) và thêm 2 lần gọi model nữa (định tuyến, trò chuyện), nên các đường lỗi nhân lên.
**Tiêu chí đóng:** §3 dòng `assistant.py` / generator ghi "mọi lần gọi đã xong vào `trace.llm_calls` ở `finally` cho cả đường không stream" (vd `GenerationError` mang `calls`), và P7 có 1 test logic cho ca "định tuyến xong rồi trả lời lỗi" ⇒ `llm_calls` có mục định tuyến.

### m-2 (minor) — khoá trước khi mở kín: ghi bằng file, không chỉ "nhắn A"

§5 bước 6: "Khoá cả bộ (sha lời dặn, mẫu khẩn cấp, commit nhánh) ⇒ nhắn A ⇒ C chạy phần kín". Tin nhắn không phải nguồn sự thật (`WORKFLOW.md` §7).
**Tiêu chí đóng:** trước khi C chạy phần kín, B ghi một dòng "Khoá" (commit + sha `ROUTER_INSTRUCTIONS`, `CHAT_INSTRUCTIONS`, `emergency.py`, `settings.yaml`) vào report B1. C kiểm các sha đó trên commit trước khi chạy, và ghi lại trong số đếm gửi về.

### m-3 (minor) — D6: sự kiện `error` cho lỗi Qdrant giữa luồng phải mang đúng lời tiếng Việt cũ; nhãn `routing` cần sửa trong `App.jsx`

- Giao diện `215a77f` **không bị phá**:
  - `frontend/src/stream.js:56`: sự kiện `error` ⇒ `StreamError(data.message || INTERRUPTED_MESSAGE)`.
  - `App.jsx:84-89`: xoá chữ, hiện lời báo + "Thử lại", y như lỗi JSON trước luồng (`stream.js:48-50`).
- Hai chỗ cần ghi rõ:
  - (1) `message` của sự kiện `retrieval_unavailable` dùng **cùng** câu như JSON 503 hôm nay. Nếu thiếu `message` thì người dùng thấy "bị gián đoạn" thay vì "chưa sẵn sàng".
  - (2) Hôm nay `App.jsx:61` đổi mọi `status` khác `generating` thành nhãn "Đã tìm thông tin…". Nếu chưa thêm nhãn `routing` thì lúc đang định tuyến giao diện báo "đã tìm" (sai). Plan đã có dòng sửa `App.jsx`, chỉ cần 1 kiểm trong cổng ổn định.
- **Tiêu chí đóng:** P7 thêm "Qdrant lỗi giữa luồng ⇒ thân `error.message` = câu 503 cũ" (test logic) và "nhãn `routing` hiện đúng" (cổng ổn định, giao diện).

### m-4 (minor) — D7 không làm hỏng thước đo, nhưng có thể đổi số đoạn trong ngữ cảnh ở mép ngân sách token

- **D7 với thước đo:**
  - P2 so bật ↔ tắt **cùng ngày**, và dòng log có `today`: đúng.
  - P6 tắt cờ ⇒ `today=None` ⇒ như B0: đúng.
  - S-T1 so danh sách tài liệu tìm được, không so ngữ cảnh đã đóng gói: không bị chạm.
- **Một chỗ có thể đổi:** dòng ngày được tính vào đếm token ngữ cảnh (`full_corpus_context.py:41`). Câu nằm ở mép ngân sách có thể mất 1 đoạn. Khi đó P5 đo cả hiệu ứng "bớt đoạn", không chỉ "có ngày".
- **Tiêu chí đóng:** P5 báo số câu có `n_context_sources` khác B0 khi `today_line` bật (đếm từ log, 0 USD).

### m-5 (minor) — D4: chữ trò chuyện có `[n]` ⇒ "citation hỏng" ⇒ `/api/chat` trả 500

D4 coi `[n]` trong lời trò chuyện là citation hỏng, nên `/api/chat` trả 500 và stream rút lại chữ. Đây là kiểm phòng xa (W48: chưa quan sát), và cách xử lý nặng (lỗi 500 cho một câu chào). Sàn 2 đã đo lọt thông tin bằng judge.
**Tiêu chí đóng (B chọn):**
- bỏ kiểm này tới khi đo thấy lọt; hoặc
- giữ nhưng đổi hành động thành thay bằng câu trò chuyện cố định, không trả 500;
- và ghi lý do.

## 3. Cách người kiểm chạy lại thật

```bash
# đếm câu Golden out_of_scope có nhắc "Huế" (chỉ in số)
uv run python -c "import json; r=[json.loads(l) for l in open('knowledge-base-hue/evaluation/golden_full_corpus.jsonl',encoding='utf-8')]; o=[x for x in r if x['category']=='out_of_scope']; print(len(o), sum('huế' in x['question'].lower() for x in o))"
git show 215a77f:frontend/src/stream.js | sed -n 44,71p      # xử lý error trước / trong luồng
git show 215a77f:frontend/src/App.jsx | sed -n 55,90p        # nhãn status + xoá chữ khi lỗi
git show 215a77f:backend/api/routes/chat.py | sed -n 150,180p # 503 retrieval_unavailable trước luồng
```

## 4. Kết quả quan sát

- Golden `out_of_scope`: 18 câu, 7 câu nhắc "Huế". Đây là đếm thô theo chữ, chưa gán nhãn từng câu theo luật. Gán nhãn đúng là việc của tiêu chí đóng M-1.
- Giao diện: sự kiện `error` giữa luồng và JSON lỗi trước luồng cùng dẫn tới một màn hình lỗi (lời server + "Thử lại"). `status` khác `generating` hiện nhãn "đã tìm".
- 0 USD; không chạy code nhánh B1 (chưa có).

## 5. Giới hạn hoặc phần chưa chạy

- Không thử luật khẩn cấp: chưa có `emergency.py`. M-2 là lập luận trên thiết kế + đặc điểm bộ đo, không phải số đo.
- Không kiểm `ROUTER_INSTRUCTIONS` / `CHAT_INSTRUCTIONS`, vì plan chưa có chữ.
- Không đọc spec bản 5 (đọc thêm, không cần cho các finding trên).

## 6. Decision và bước tiếp theo

**`changes_requested`**: 3 major (M-1, M-2, M-3) + 5 minor.

- M-2 và M-3 (b) chạm chữ spec / quyết định của A ⇒ **A quyết** trước khi B sửa.
- M-1: C có thể giao danh sách nhãn 18 câu (0 USD) khi A đồng ý.
- B sửa trong một lượt, báo sha mới. C chỉ kiểm phần sửa của M-1…M-3; minor sửa cùng đợt, nếu không sửa thì phản biện; không mở vòng mới cho minor.

## Vòng 2 — kiểm phần sửa (bản 2 sha `0c9e137b56af`, C tính lại từ file — khớp; 19:53 02/11/2026 `date`)

Phạm vi: chỉ bảng "Chỗ đổi bản 2" cuối plan, đối với M-1…M-3 và m-1…m-5 cùng các quyết định của A (M-2 tách hai sàn; M-3 (b); m-5 bỏ kiểm). Không mở finding mới.

| Finding | Sửa ở (plan bản 2) | C kiểm | Kết luận |
|---|---|---|---|
| **M-1** | Căn cứ (thêm `golden_oos_nhan.jsonl` md5 `7cf3b6fa67b9`); §4 P1 sàn 1: 32 câu an toàn + 158 câu Golden không `out_of_scope` là `tro_ly_hue`; 18 câu `out_of_scope` theo nhãn ghi trước (7 tính vào sàn 1, 11 `ngoai_pham_vi` `chap_nhan` `tro_ly_hue`); §9 dòng sửa nghĩa | md5 khớp file C130; 32 + 158 + 18 = 208 | **đóng** |
| **M-2** | §4 P3: (a) sàn chặn nhầm ⇒ tắt luật; (b) 14 / 14 đã thấy là sàn, 8 câu kín chỉ báo số (luật bắt / định tuyến bắt / sót cả hai) ⇒ kết quả âm, **không** tắt, **không** sửa theo kín; P1 thêm câu kín luật sót; D2 "Sai khi"; §5 bước 6 | đúng quyết định của A | **đóng** |
| **M-3** | §2 D6: đổi cố ý, **không** gỡ bằng cờ; lỗi Qdrant giữa luồng ⇒ `error` `retrieval_unavailable` + câu "Hệ thống tra cứu tạm thời không khả dụng." + `done`; `router` tắt ⇒ không có `routing`; §4 P6 ghi rõ không gồm hợp đồng lỗi | câu này khớp từng chữ với `main` (`api/routes/chat.py:163, :177`, `api/app.py:63`); lý do (một đường stream) có ghi | **đóng** |
| m-1 | §3 `assistant.py` (mọi lần gọi xong vào `trace.llm_calls` ở `finally`, cả đường không stream) + generator (`CallLog` do lõi tạo, truyền vào); §4 P7 test "định tuyến xong rồi trả lời lỗi" | đủ tiêu chí đóng | **đóng** |
| m-2 | §5 bước 6: dòng "Khoá" trong report (commit + sha 4 thứ) ⇒ push ⇒ C kiểm sha trên đúng commit rồi mới chạy kín, ghi sha đã kiểm vào kết quả | đủ | **đóng** |
| m-3 | D6 (`message` = câu 503 cũ); D6 / §3 `App.jsx:61` + nhãn `routing`; P7 test logic + cổng giao diện | đủ | **đóng** |
| m-4 | §4 P5 theo dõi số câu `n_context_sources` khác B0 | đủ | **đóng** |
| m-5 | §2 D4 + §8: bỏ kiểm `[n]` (A quyết) | đúng | **đóng** |

Phần sửa không sinh lỗi mới. Có một ghi chú cho lúc C chạy phần kín, không phải finding: 2 câu `khan_cap` nằm trong bộ tuyến kín (20 câu) sẽ bị luật khẩn cấp bắt trước khi tới định tuyến nếu chạy cả đường với cờ bật. C sẽ báo riêng "luật bắt" và "định tuyến bắt" cho 2 câu này khi đếm P1 kín, để không lẫn với tỉ lệ định tuyến.

**Kết luận vòng 2: `ready_for_user_confirmation`** (bản `0c9e137b56af`). A duyệt sha (tính từ file).
