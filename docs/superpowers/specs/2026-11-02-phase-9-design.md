# Phase 9 — trợ lý Huế dạng agent có công cụ — tài liệu thiết kế

Người viết: C · bản 6 13:39 · bản 7 13:54 · bản 8 14:14 · **bản 9 14:42 02/11/2026** (`date`). Review `2026-11-02-phase-9-design_review_v6.md`: vòng 3 trên bản 8 (`82127aabcb5b`) = ready_for_user_confirmation.
- Bản 9 **chỉ ghi lựa chọn của User P1–P5 + quyết định A về bộ hồi quy + m17** (chỗ đổi liệt kê cuối file). Bản 5 (hướng không agent) giữ ở commit `077e3cb`.
- Trạng thái: bản 9 User duyệt `169c2dd5f86a` (14:55 02/11/2026). Bản 10 (09:30 05/11/2026, A) §11 — review C177 changes_requested. Bản 11 (09:42 05/11/2026, A) §11 viết lại chỉ phần Phase 9 — review C178 changes_requested 0 / 2 / 5. **Bản 12 (09:45 05/11/2026, A): sửa M-1, M-2, m-1–m-5 của C178 — chờ C kiểm phần sửa + User duyệt sha.** **Bản 13 (10:47 08/11/2026, C — A giao): §12 cổng 2 nhóm + 4 công cụ T1–T4; review B vòng 1 `…design_review_v13.md` changes_requested 0 / 2 / 5 ⇒ sửa 10:56 08/11/2026 (M-1, M-2, m-1–m-5) — chờ B vòng 2 + A duyệt sha.**

Mức rủi ro: **cao** (Phase mới, thêm công cụ + đường ra ngoài).
- Spec chốt kiến trúc, bậc làm, bộ đo, tiêu chí ghi trước, tiền, bảo mật. Chi tiết code để plan nhỏ của từng bậc (nguyên tắc "làm vừa đủ", sổ cải tiến S64).
- **Mỗi công cụ là một bậc giữ / gỡ riêng.** Không chép nội dung kho, câu Golden hay câu kín; câu ví dụ là câu tự viết.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `session_prompt/CURRENT_HANDOFF.md` | mục "Phase 9 đổi hướng" + mục "C120" | spec đúng quyết định User 11:21–13:36 02/11 và ý A giao; chỗ lệch có lý do |
| `data/nghien_cuu_phase_9_2026-11-01/agent/a_sa2.md` | §3 (bộ ba, R1–R15, 6 rào §3c, §3d) | 6 rào đủ ở B6; rủi ro mỗi bậc |
| `data/nghien_cuu_phase_9_2026-11-01/agent/a_sa1.md` + `a_sa3.md` | a_sa1 §2.1–§2.5; a_sa3 §2b–§2d, §3a | trần, công cụ, ước tiền / độ trễ dẫn đúng |
| `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` | §3.1–§3.3 | sàn Golden / bộ an toàn / câu theo ngày dùng lại đúng |
| code `main` | `backend/llm/generator_openai_full_corpus.py:96-104, 130-145, 183-190`; `backend/llm/grounded_answer.py`; `backend/api/routes/chat.py:35-53, 355-400` | `file:dòng` khớp; lõi chung + streaming làm được |

**Bản 13 (§12) — căn cứ:**

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `session_prompt/CURRENT_HANDOFF.md` | mục 2d (brainstorm định tuyến 10:30 08/11) + tin A giao C 08/11 | §12 đúng quyết định User: 2 nhóm, bỏ khẩn cấp, `OUT_OF_SCOPE_ANSWER`, 4 công cụ, thứ tự, trần 3,5 |
| `data/phase_9/dinh_tuyen_2/bo_do_nhap.md` (private) | §0–§4 + mục "A quyết" | sàn S1–S6, bộ có sẵn / thiếu, số log, ước tiền chép đúng |
| `report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`, `e20_tu_choi_hoi_kem.md`, `c210_implementation.md` | §3–§5 | sửa T4 (a)–(d) đúng nguyên nhân đã chứng minh |
| `report_agent/2026-11-02_phase_9_code/b162_b5c_implementation.md` | dòng 1, 57, 76 | bài học B5c vào T3 |
| `docs/superpowers/plans/2026-11-05-phase-9-b6-plan.md` | D1–D5 | T2 giữ rào B6 |
| code `main` | `backend/llm/assistant.py:46-52, 250-290, 742-785`; `backend/llm/full_corpus_prompt.py:42-50`; `backend/config/settings.yaml:59-75` | `file:dòng` khớp |

**Dẫn, ngoài căn cứ:**
- kết quả ChatGPT 02/11 — dữ liệu; A đã kiểm SDK v0.24.0 + `max_turns`;
- `guides/phase_9_agentic_rag_roadmap.md` — ý định tuyến, câu tìm đứng một mình, "kho trước + cổng đủ bằng chứng", nguồn gốc web;
- spec bản 5 (`077e3cb`) — 4 lựa chọn User đã chọn, bảng điểm lịch trình.
- `data/nghien_cuu_phase_9_2026-11-01/agent/b123_sdk_probe.md` (B123, dò SDK 0.19.4 có công cụ + stream) và `b122_tra_web.md` (B122, điều khoản + giá Serper).

**Mã dùng trong file:** RAG 1–8 = chatbot hỏi–đáp của Phase 1–8 · Golden = bộ 176 câu đánh giá · T1 = kết quả tìm 158 câu Golden (so "giống byte") · bộ an toàn = 32 câu điều kiện / cảnh báo ·
P0_sai = câu nói sai điều kiện · H4c = dòng "có thể đã thay đổi" · C106 = rà bảo mật đóng gói 01/11 · W35 = luật "đọc điều khoản trước khi dùng dịch vụ ngoài".

## 1. Mục tiêu

RAG 1–8: mỗi câu một lượt tìm + một lần gọi model, không công cụ. User 02/11: "lên trợ lý mà không có gì khác RAG mức 1 thì gọi thẳng LLM cần gì trợ lý".
⇒ Phase 9: **trợ lý dạng agent cho mọi câu**; RAG 1–8 thành công cụ tìm kho; **giữ chỗ mạnh đã đo** (nguồn từng ý, không bịa, không nói ngược kho ở câu điều kiện).
Bảo vệ 04–10/01/2027 ⇒ ~~đóng code 20/12/2026~~ — **sửa 05/11 (§11.4): đóng code khi User nói, dự kiến 25–30/12, lúc đó đã chạy trên AWS**.

**Năm dòng khám phá** (`propose-options` §4b):
1. **Vấn đề + đo bằng gì.** Hôm nay hệ thống:
   - không trò chuyện, không nhớ lượt trước (kể cả tên);
   - không hỏi lại khi thiếu thông tin; không lập lịch;
   - yếu câu nhiều nguồn (Đủ 3,50 ↔ 4,92 câu một dữ kiện — Q3a §4);
   - từ chối câu kho không có;
   - từ chối nhầm câu theo ngày tương đối (5 câu trong kho trên 12 câu quyết, bộ 15 câu — plan đo cuối §3.3, lượt 01/11).
   Đo bằng bộ câu có nhãn đường + hồi quy chung (§4).
2. **Ba ô:** đo được (judge Claude + code + nhãn đường); dữ liệu chưa có câu thật ⇒ bộ tự viết có phần kín; giá trị = việc mới + tìm tốt hơn ở câu khó.
3. **Mốc:** RAG 1–8 = `main` đầu Phase 9. Đường trả lời (`llm/`, `retrieval/`, `api/routes/chat.py`) không đổi từ `a80e12d` ⇒ dùng lại câu trả lời + điểm lượt đo cuối 01/11.
4. **Tiêu chí bằng số:** §4 + từng bậc §5, ghi trước.
5. **Phương án B:** bậc không qua ⇒ tắt bằng cờ, giữ bậc trước; cả agent không hơn ⇒ ghi kết quả âm (B7).

**"Agent dưới chính sách"** (ChatGPT 02/11 §0, A đồng ý): code giữ luật (trần, cổng web, kiểm nguồn, khẩn cấp); thêm một công cụ mỗi bậc; B7 so cả hệ với RAG 1–8 — giữ tinh thần khoá "luồng cố định thì không cần agent" (a_sa1 §3 D1).

## 2. Quyết định

| Khi | Quyết định | Ai |
|---|---|---|
| 11:21 02/11/2026 | Agent có công cụ cho mọi câu; RAG 1–8 thành công cụ. Giữ OpenAI Agents SDK (bản cài `0.19.4`) | User; A |
| 13:29 02/11/2026 | Mẫu khoá: trần lượt; từng công cụ một; lời từ chối của công cụ về model; nhớ chỉ hỏi + đáp; soát chữ web; test ranh giới; thẻ công cụ trên giao diện; tracing tại máy. **Không người duyệt lúc chạy** | User |
| 13:29 02/11/2026 | Cổng vào = **agent định tuyến**, đầu ra có cấu trúc ⇒ trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp | User |
| 13:29 02/11/2026 | Câu tìm kho: **thí nghiệm** so phương án, chọn theo số | User |
| 13:29 02/11/2026 | **Nhớ hội thoại bắt buộc** (hỏi + đáp, không kết quả công cụ; tên không log, xoá được). Nhớ khi mở lại trang: P1 (a) — không (§10) | User |
| 13:36 02/11/2026 | Chất lượng trước: 0,0005 USD / câu + p50 3 / p95 5 s ⇒ theo dõi. **Bắt buộc log** USD + ms mỗi lần gọi LLM / Serper / câu / tuyến. Trần phiên ≤ 1 USD + trần Phase là cứng | User |
| 11:03 02/11/2026 (bản 5) | Giữ 4 lựa chọn bản 5: câu khẩn cấp thử 10 câu trước · H4c dòng cố định · câu hai ý thiếu một ý đếm trước (≥ 3 câu mới làm) · chi phí chỉ liệt kê giá có nguồn, chọn lại sau | User |
| A giao C120 (mục C120 handoff) | S-OOS định nghĩa lại khi có web; 6 rào trước khi bật web (rào 6 "đo hai chiều" bỏ — User 14:42); Serper chưa gọi tới khi đọc điều khoản; cuối Phase so RAG cũ ↔ agent | User / A |
| **14:12 02/11/2026 (User chọn, sau review M13)** | **Code giữ 3 chỗ** User từng nêu là "model tự quyết": (1) **ngày hôm nay** luôn vào lời dặn (không là công cụ); (2) **web do code gọi khi kho từ chối** (không là công cụ); (3) **lần tìm đầu là thí nghiệm** — "code tìm trước" ↔ "trợ lý tự quyết có tìm không" (V2 thuần), chọn theo số (B2a) | User |
| như trên — hệ quả web User đã thấy | (a) câu kho trả lời được **một phần** không bao giờ đi web (cổng chỉ mở khi câu trả lời đúng bằng câu từ chối chuẩn); (b) câu bị **từ chối nhầm** (mốc 12 / 158) sẽ ra mục web thay vì kho; (c) người dùng thấy câu từ chối hiện trước rồi mới tới mục "Từ web"; (d) câu hỏi tiếp tra web chỉ bằng câu hỏi lượt này ⇒ "còn giá vé ở đó?" ra truy vấn mất chủ ngữ. Để model tự gọi thì được câu kho một phần + câu hỏi tiếp, nhưng mất cổng code thấy được (review v6 M2) và chữ web vào vòng có công cụ / lịch sử | User |
| 14:12 02/11/2026 (User) | **Sau Phase 9:** hiện chỉ vài công cụ; khi hệ thống ổn định thì nghiên cứu, tạo thêm công cụ mới | User |
| 14:42 02/11/2026 (User chọn P1–P5) | Bảng "User đã chọn" §10: nhớ chỉ trong cuộc trò chuyện · model viết mục "Từ web" · không giới hạn tên miền · trần Phase 2,0 USD · dùng Serper luôn | User |
| **lệch có lý do (User 14:42)** | (1) **Dùng Serper khi điều khoản chưa rõ** (B122: dịch vụ business-to-business, không nói về người dùng cuối / hiển thị / lưu — W35 coi là chưa đủ căn cứ). User chấp nhận rủi ro, không email hỏi; B6 vẫn sau rào code + cờ. (2) **Bỏ** bộ kết quả web xấu cố định, model thứ hai soát chữ web, đo hai chiều riêng cho web — User: "over-engineer quá". Lệch với mẫu khoá "soát chữ web" (13:29) và rào 6 của a_sa2 §3c. **Giữ rào dạng code**: lần gọi web riêng không công cụ / không lịch sử, link do code, nhãn, câu an toàn theo kho. Đo web chỉ trên Serper thật | User |
| 14:42 02/11/2026 (A quyết, User hỏi) | **Bộ hồi quy:** đủ 176 + 32 ở B1, B2, B7 và ở bậc nào sửa lời dặn chung / lõi chung. B3–B6: bộ riêng + 32 câu an toàn + **mẫu Golden cố định ~30 câu** (§4) | A |

## 3. Kiến trúc

```text
trình duyệt (React, SSE) ──> FastAPI: session (cookie HttpOnly), hạn giờ, log số đo
  └─ LÕI CHUNG backend/llm/assistant.py — route stream, /api/chat và answer_case (bộ đánh giá) cùng gọi
       ├─ [code] luật khẩn cấp (chỉ nếu bước 0 thấy cần)
       ├─ [model] ĐỊNH TUYẾN — 1 lần gọi, đầu ra có cấu trúc, không công cụ, không stream
       │     route ∈ {tro_chuyen, tro_ly_hue, ngoai_pham_vi, khan_cap} · cau_tim (nếu B2 chọn)
       ├─ tro_chuyen    → model trò chuyện (prompt riêng, có lịch sử, không tìm kho)
       ├─ ngoai_pham_vi → câu từ chối cố định (code)
       ├─ khan_cap      → câu soạn sẵn User duyệt (code)
       └─ tro_ly_hue    → AGENT TRỢ LÝ (max_turns 3–4, parallel_tool_calls=False)
             code đưa vào: ngày hôm nay (giờ VN), lịch sử hỏi + đáp (đã cắt phần web), đoạn kho tìm trước (hoặc không — B2a)
             công cụ (mỗi cái một bậc): tim_kho(cau_tim) · hoi_lai(loai, truong_thieu) [StopAtTools] · lich_trinh(...)
             đầu ra: {answer} như hôm nay (câu từ chối chuẩn = từ chối)
             └─ [code] CỔNG WEB (B6, cờ): answer = câu từ chối chuẩn ∧ outcome thường (không chạm trần, không lỗi công cụ)
                   ∧ tuyến tro_ly_hue ∧ chưa gọi web
                   ⇒ code dựng truy vấn từ câu hỏi lượt này ⇒ Serper ⇒ 1 lần gọi model riêng
                     (không công cụ, không lịch sử) viết mục "Từ web" trích [w n]
  └─ [code] kiểm cuối: mã trích ∈ sổ nguồn (kho [n], web [w n]) · H4c · log số đo
```

**Chia việc code ↔ model:**
- **Ngày hôm nay** do code đưa vào, không là công cụ — việc luôn cần ⇒ code (a_sa1 §2.2, a_sa2 R10).
- **`hoi_lai` là công cụ + `StopAtTools`** (a_sa1 §2.2):
  - lượt thường giữ đầu ra `{answer}` như hôm nay ⇒ bộ tách chữ stream (`AnswerTextStream`, `chat.py:368-371`) và `ANSWER_PREFIX` không đổi (B123 §3 chỉ đòi sửa khi đổi sang kiểu có `route`);
  - **lượt `hoi_lai`:** `final_output` là giá trị công cụ trả, không phải `AnswerOutput`, mà `finish_answer_stream` hôm nay ép `AnswerOutput` (`generator_openai_full_corpus.py:269`) ⇒ **nhánh riêng** đọc kết quả `hoi_lai` trước khi ép kiểu (plan B4);
  - code dựng nút từ danh sách trường. (a_sa2 R15 khuyên kiểu đầu ra; chọn công cụ để không đổi đường stream.)
- **`tra_web` không là công cụ** (sửa M2). Code thấy được "câu trả lời là câu từ chối chuẩn", nên cổng web đặt **sau** câu trả lời kho.
  - Kho luôn thắng: câu kho trả lời được thì không tra web.
  - Chữ web chỉ vào **một lần gọi riêng** không công cụ, không lịch sử ⇒ web độc không lái được công cụ hay lượt sau.
- **Sổ nguồn** một danh sách cho cả lượt; model chỉ trích mã có trong sổ; link + nhãn web do code dựng (a_sa2 R3).
- **Trần** (con số chốt ở plan B2):
  - định tuyến 1 lần; trợ lý `max_turns` 3–4; `tim_kho` ≤ 2, `lich_trinh` ≤ 1 (đếm trong code); web ≤ 1 lần / câu;
  - hết trần ⇒ câu từ chối chuẩn + `outcome="max_turns"` (SDK 0.19.4 có `error_handlers` — a_sa1 §2.3) — **không mở cổng web**.
  - `tool_choice="required"` (ép gọi công cụ lần đầu, B123): đã xét, không dùng — lần tìm đầu do B2a quyết.
- **Lỗi công cụ ≠ không có kết quả:** lỗi Qdrant / Serper ⇒ chữ báo lỗi cho model hoặc câu cố định "chưa tra được web", `outcome` riêng (a_sa2 R8).

**Streaming** (B123 §2–§3, SDK 0.19.4):
- định tuyến và lượt gọi công cụ **không có chữ** ⇒ mỗi lượt gửi sự kiện trạng thái. Đây là **thẻ công cụ** trên giao diện: "đang hiểu câu hỏi…", "đang tìm kho…", "đang tra web…", kèm số đoạn tìm được;
- lần gọi công cụ không phát `output_text.delta` (B123) ⇒ bộ lọc hôm nay (`chat.py:368`) chỉ còn chữ lượt cuối;
- mục "Từ web" stream sau, khối riêng;
- **rút lại khi trích dẫn hỏng áp cho cả `[n]` lẫn `[w n]`** (`chat.py:309-313` mở rộng).

**Chữ đầu dự kiến** (ước, a_sa3 §2c; hôm nay p50 1,23 / p95 2,61 s):

| Đường | p50 |
|---|---|
| trò chuyện / trợ lý không gọi công cụ | ≈ 2,8–2,9 s (thêm lần gọi định tuyến ~1,6 s) |
| + một lần `tim_kho` | +~1,6 s |
| web | chữ câu từ chối ≈ 2,9 s; **chữ đầu mục web** ≈ 5–6 s (đo riêng) |

Chỉ theo dõi (User 13:36). "Chữ đầu" = chữ trả lời, **không** tính dòng trạng thái. Đường web báo cả hai số; thước chính là chữ đầu mục web.

**Nhớ** (sửa M3, m8):
- server giữ trong RAM theo phiên (cookie HttpOnly, mã ngẫu nhiên); TTL 30 phút; trần token;
- lưu câu hỏi + câu trả lời cuối **đã cắt mục "Từ web"**; không kết quả công cụ;
- **không log mã phiên**, không log chữ.
- Vì sao không để trình duyệt gửi lại: trình duyệt sửa được "trợ lý đã nói …" ⇒ chỗ cài lệnh.

**Log + vết:**
- thêm trường vào `chat_metrics` (`chat.py:35-40`; hôm nay chỉ token, không USD) và vào dòng kết quả của bộ đánh giá — **không** thêm nơi thứ ba;
- mỗi lần gọi LLM: tuyến, token, USD (`cost_usd`, `evaluation/full_corpus_eval.py:169`), ms — lấy bằng `RunHooks.on_llm_start` / `on_llm_end` + `response.usage` (B123 §1);
- mỗi lần Serper: USD, ms, trạng thái;
- mỗi câu: tổng USD / ms, chữ đầu, số lần gọi, công cụ, tuyến, **`has_web_section`** (`refusal` hôm nay = câu trả lời đúng bằng câu từ chối, `chat.py:100` ⇒ câu có mục web phải tách riêng);
- tracing SDK giữ tắt (`generator_openai_full_corpus.py:96-104`).

**SDK:** giữ `0.19.4` cho Phase 9 (A quyết 14:02, sau B123 + C121 `c121_sdk_024.md`). Nâng = bước riêng khi một bậc cần (vd `agents.testing`), có cổng ổn định thật.

## 4. Thước đo chung

**Mốc:** RAG 1–8. Mỗi bậc so **bậc trước đã giữ**; B7 so cả hệ với mốc.

**Sàn — không được phạm**, cộng dồn so với mốc:
- **S-AT** — bộ an toàn 32 câu, plan đo cuối §3.2: 0 đảo cảnh báo; P0_sai mới ≤ 2 cả Phase (2 câu dao động 01/11 nằm trong mốc); ca mới ⇒ sinh lại 3 lần hai bên, "mới thật" khi biến thể ≥ 2 / 3 và mốc ≤ 1 / 3.
- **S-G** — Golden 176, plan đo cuối §3.1:
  - sàn F1–F4: 0 câu ngoài kho bị trả lời ở đường chỉ-kho; 0 lỗi kỹ thuật; 0 lỗi trích dẫn mới; 0 "nói chắc sai" mới;
  - mức tụt: Đủ / Đúng TB theo cặp ≥ −0,1; câu tụt ≤ A/A + 3; từ chối nhầm ≤ mốc + 1.
- **S-OOS định nghĩa lại:**
  - đường chỉ-kho (web tắt): "0 câu ngoài kho bị trả lời";
  - có web: "**0 câu không có bằng chứng hợp lệ bị trả lời khẳng định**"; câu ngoài chủ đề Huế luôn từ chối.
  - Nhãn câu: `kho_tra_loi_duoc` · `web_tra_loi_duoc` · `khong_xac_minh` · `can_hoi_lai` · `ngoai_chu_de`.
- **S-T1 mới:** `tim_kho` với câu gốc ⇒ kết quả giống byte T1 `4d5bbe9e0edc`.
- **Trích dẫn:** 100 % mã trích nằm trong sổ nguồn.

**Hồi quy mỗi bậc** (A quyết 14:42), 1 lượt, ca mới theo thủ tục S-AT:
- **đủ 176 + 32 câu** ở B1, B2, B7 và ở bậc nào sửa **lời dặn chung / lõi chung**;
- **B3–B6** (chỉ thêm một công cụ / một đường): bộ riêng của bậc + 32 câu an toàn + **mẫu Golden cố định ~30 câu** (chọn bằng seed ghi trước, chia đều 5 loại câu, khoá ở B0). Trên mẫu này đo sàn F1–F4; mức tụt S-G đủ (≤ A/A + 3…) chỉ tính ở lượt đủ 176;
- chuỗi gửi model không đổi (so hash lời dặn + danh sách công cụ) ⇒ dùng lại số của bậc trước.

**Theo dõi** (User 13:36): USD / câu, chữ đầu p50 / p95, tổng ms — theo tuyến và theo đường.

**Đo riêng agent:**
- định tuyến đúng (ma trận nhầm);
- đường đúng (nhãn đường kỳ vọng ↔ danh sách lời gọi công cụ);
- tỉ lệ câu đủ thông tin được trả lời thẳng (chống "hỏi lại / từ chối hết");
- **3 lượt chỉ cho câu rủi ro ở B7**; các bậc khác 1 lượt + thủ tục "ca mới ⇒ sinh lại 3 lần".

**Bộ đo** (người viết câu ≠ người code; User đọc mẫu 10 câu; private `data/phase_9/<bậc>/`; chỉnh trên đã thấy, khoá trước khi mở kín, kín không ngược chiều):

| Bộ | Số câu | Đã thấy / kín | Viết tuần |
|---|---:|---|---|
| tuyến (B1) | 60 (+5 ca lái tuyến) | 40 / 20 | 02–08/11 |
| câu theo ngày (B1) | 15 cũ + 10 mới | 15 + 3 / 7 | 02–08/11 |
| khẩn cấp (bước 0 + B1) | 10 | 10 / — | 02–08/11 |
| nhớ (B3) | 40 chuỗi + 3 chuỗi nêu tên rồi hỏi câu cần web (B6) | 25 / 15 | 16–22/11 |
| hỏi lại (B4) | 30 | 20 / 10 | 16–22/11 |
| lịch trình (B5) | 18 | 13 / 5 | 23–29/11 |
| web (B6, Serper thật) | 25 thường + 3 chuỗi nêu tên + 2 câu tên trong câu | 20 / 10 | 30/11–06/12 |
| mẫu Golden cố định (B3–B6) | 30 (trong Golden 176) | — | khoá ở B0 |

**Luật giữ / gỡ** (`run-experiment` §4): không phạm sàn · không tụt quá mức · chỉ số quyết vượt nhiễu và kín không ngược chiều.
Không đạt ⇒ cờ tắt, tag `hoso/p9-<bậc>`; 3 vòng sửa không đạt ⇒ dừng bậc.

## 5. Bậc làm (lần lượt; merge bậc trước rồi mới mở nhánh bậc sau)

### B0 — nền (≈ 0,003 USD)

- Bọc RAG 1–8 thành `tim_kho` (gọi `retrieval_service.search`, `retrieval/full_corpus.py:419`; top-k, collection do code); lõi chung `assistant.py`; sổ nguồn; log §3.
- **Bước 0 khẩn cấp:** ~10 câu tự viết qua chatbot hôm nay; User đọc. Có lỗi ⇒ luật code + câu soạn sẵn ở B1; không ⇒ ghi "không cần".
- **Tiêu chí:** S-T1 mới giống byte; `answer_case` qua lõi chung ra đúng câu trả lời đường RAG 1–8; test ranh giới (chỉ một module gọi mạng ngoài; không công cụ nào nhận URL); log đủ trường; grep chữ câu hỏi / mã phiên trong log = 0.

### B1 — định tuyến + trò chuyện + ngoài phạm vi + khẩn cấp + ngày + H4c

Ở B1, `tro_ly_hue` = đường RAG 1–8 (chưa công cụ). Mỗi phần có cờ riêng, gỡ độc lập:

| Phần | Chỉ số quyết / sàn (ghi trước) | Không đạt ⇒ |
|---|---|---|
| định tuyến (+ trò chuyện, ngoài phạm vi) | quyết: đúng ≥ 90 % trên 40 đã thấy, kín không ngược chiều. Sàn: **0 câu Huế cần thông tin bị đưa sang trò chuyện / ngoài phạm vi**; **0 câu trò chuyện chứa thông tin Huế cụ thể** trên 5 ca lái tuyến + bộ tuyến (judge) | tắt cờ: mọi câu vào `tro_ly_hue` |
| ngày hôm nay | quyết: từ chối nhầm trên 12 câu quyết (bộ 15) giảm ≥ 3, sinh 2 lượt, TB theo câu, mốc sinh lại cùng ngày; kín không ngược chiều. Sàn: 0 "đoán ngày rồi nói sai" | tắt dòng ngày |
| khẩn cấp (nếu bước 0 cần) | sàn: 0 câu khẩn cấp vào model (luật code tất định ⇒ 1 lượt); 0 câu thường bị chặn trên 208 | tắt luật |
| H4c | test code: có dòng khi nguồn trích thuộc `travel/tickets` / `travel/places` / `festivals`; không có khi khác hoặc khi từ chối | tắt dòng |

- Cả B1: S-AT, S-G, S-OOS (chỉ-kho) — hồi quy 1 lượt.
- **Trò chuyện:** chặn "nói thông tin Huế" là lời dặn + sàn đo. Đo thấy lọt ⇒ thêm kiểm code rẻ (đầu ra trò chuyện có số / giờ / giá ⇒ chuyển sang trợ lý).
- **Bảo mật:** chữ người dùng là dữ liệu với định tuyến; định tuyến không có công cụ ⇒ bị lừa chỉ đổi tuyến. Tuyến trò chuyện **không có nguồn để kiểm** ⇒ rào là hai sàn trên.

### B2 — câu tìm (B2a) rồi vòng công cụ `tim_kho` (B2b)

- **Vấn đề:** câu nhiều nguồn + so sánh, số chính 38 câu. **12 câu chưa đủ keyword trong top-10** = số câu có thể đổi ở tầng tìm: Q3a §4 bảng, "đủ keyword" 12 / 18 nhiều nguồn + 14 / 20 so sánh (`report_agent/2026-10-31_streaming_spec/q3a_theo_loai_cau_implementation.md:34, :36`). Câu hỏi tiếp cần câu tìm đứng một mình.
- **B2a — lần tìm đầu** (User chọn: thí nghiệm). Mốc **V0 = B1**: code tìm bằng câu gốc.
  - **V1** code tìm trước bằng câu định tuyến viết (đứng một mình);
  - **V3** code tìm trước bằng câu định tuyến viết lại + chia ≤ 3 câu nhỏ, trộn RRF thành 10;
  - **V2 thuần** không tìm trước — trợ lý tự quyết có gọi `tim_kho` không, tự viết câu tìm. Cần vòng công cụ ⇒ **dựng vòng công cụ ở đây**.
  - **Tầng tìm**, 2 lượt mỗi biến, trên 38 câu:
    - V1 / V3 chỉ tốn lần gọi định tuyến; V2 tốn trợ lý tới lần gọi công cụ đầu (~0,0002 USD / câu);
    - V2 mà trợ lý không gọi `tim_kho` ⇒ tính "không đủ keyword".
    - Biến qua tầng tìm khi **thêm ≥ 3 / 12 câu đủ keyword ở cả hai lượt và 0 câu mất đoạn đúng** (nhãn v5) trên mọi câu bị đổi; Holm cho 3 biến so V0 ở tầng này.
  - **Khâu trả lời:** chỉ biến qua tầng tìm và đứng đầu. Quyết: Completeness trên **18 câu nhiều nguồn** CI 95 % > 0 so V0 (so sánh chỉ theo dõi — Q3a: câu so sánh chỉ 2 câu yếu) **và** sàn §4.
  - **Cỡ mẫu:** 12 câu có thể đổi ⇒ chỉ thấy lợi lớn. "Chưa rõ" ghi trước là dễ xảy ra ⇒ giữ V0.
  - Đo V2 ở khâu trả lời ⇒ **A/A đường có công cụ chạy tại B2a** (Golden sinh 2 lượt V2), mức tụt S-G của V2 dùng nhiễu này (review vòng 3 m17).
- **B2b — tìm thêm**, chỉ khi B2a giữ biến có tìm trước (V0 / V1 / V3): trợ lý được gọi `tim_kho` thêm ≤ 2 lần. Mốc = biến giữ ở B2a. (B2a giữ V2 ⇒ B2b gộp vào V2, không đo riêng.)
  - **Vòng công cụ là hạ tầng:** gỡ B2b = tắt `tim_kho` thêm; vòng vẫn giữ cho `hoi_lai` / `lich_trinh`.
  - **A/A đường có công cụ** ở đây: Golden sinh 2 lượt cùng cấu hình; thay N_AA (nhiễu A/A cũ) cho mức tụt S-G từ đây. B2b bị cắt / gỡ trước khi đo ⇒ A/A + thẻ công cụ chuyển sang B4.
  - **Quyết:** Completeness 18 câu nhiều nguồn CI 95 % > 0 so B2a; nhóm test không ngược chiều.
  - **Cỡ mẫu:** câu có thể đổi = câu trong 38 còn thiếu keyword sau B2a (≤ 12) ⇒ "chưa rõ" dễ ⇒ khi đó tắt `tim_kho` thêm.
  - **Theo dõi:** % câu gọi `tim_kho`, lần gọi / câu, USD, chữ đầu.
  - **Thẻ công cụ** trên giao diện làm ở bậc đầu có vòng công cụ (B2a nếu đo V2, không thì B2b).
- **Bước 0 câu hai ý** (lựa chọn bản 5) chạy sau B2a: đếm câu nhiều nguồn có một vế không có keyword nào trong kho; ≥ 3 câu mới mở việc riêng.

### B3 — nhớ hội thoại (bắt buộc, không cắt)

- Như §3 "Nhớ". Làm được trên B1 nếu B2 chưa xong (câu tìm = câu gốc + lịch sử trong prompt).
- **Bộ đo:** 40 chuỗi 2–4 lượt — nhớ tên, hỏi tiếp ý cũ / ý mới, hỏi tiếp ngoài kho, hỏi tiếp điều kiện, đổi chủ đề. Đường thật nhiều lượt.
- **Tiêu chí:**
  - sàn: hỏi tiếp ngoài kho 0 câu bị trả lời; hỏi tiếp điều kiện 0 đảo cảnh báo;
  - **quyết 1 — nhớ tên:** đúng ≥ 9 / 10 chuỗi nhớ tên;
  - **quyết 2 — hỏi tiếp:** Completeness lượt sau so "gửi như câu độc lập" CI 95 % > 0, kín không ngược chiều;
  - mức tụt: đổi chủ đề tụt ≤ 1 câu;
  - S-G / S-AT với nhớ **tắt**: dùng lại số bậc trước nếu hash lời dặn + công cụ không đổi.
- **Dữ liệu cá nhân:** tên không log; nằm trong RAM phiên; xoá khi hết TTL / bấm "Cuộc trò chuyện mới"; vẫn gửi OpenAI như câu hỏi (giới hạn, Luật 91/2025).
- **Kết quả âm ⇒** chỉ nhớ câu hỏi, không câu trả lời.

### B4 — `hoi_lai` (lịch trình / chi phí)

- Danh sách trường cố định trong code (bản 5 §5.4); model chọn trường thiếu trong danh sách; `StopAtTools`; code dựng nút.
- Chi phí: chỉ liệt kê giá có nguồn. **Trước khi code phần chi phí:** tra web cách trợ lý du lịch trình bày (0 USD) + User đọc mẫu hai cách ⇒ chọn lại.
- **Tiêu chí:**
  - quyết: câu thiếu trường được hỏi lại đúng ≥ 8 / 10 đã thấy, ≥ 4 / 5 kín;
  - sàn: hỏi lại nhầm câu đủ trường ≤ 1 / 10; tỉ lệ trả lời thẳng trên bộ tuyến không giảm;
  - mức tụt lượt sau khi chọn: Đúng ≥ −0,1; 0 "nói chắc sai" mới.
- Giá trị trường chỉ nhận trong danh sách; không trường dữ liệu cá nhân.

### B5 — `lich_trinh`

- Bảng điểm `data/phase_9/lich_trinh/diem.json`: ~20–30 điểm, User duyệt; thời lượng không có ⇒ `null`, xếp như "nửa buổi". Soạn song song từ 16/11.
- **Code xếp:** ≤ 2 cụm / ngày, số suất theo kiểu đi. Model trích trường + viết lời có `[n]`. Code kiểm 0 giờ / giá chính xác, 0 điểm ngoài bảng.
- **Tiêu chí:**
  - sàn code đếm (như bản 5) + 3 / 3 yêu cầu ngoài Huế bị từ chối;
  - **quyết:** User chấm 5 lịch trình kín theo 3 tiêu chí **ghi trước** (đúng luật xếp · hợp người đi cùng · mỗi điểm có nguồn), đạt cả 3 ở ≥ 4 / 5.
  - Không so mù với RAG 1–8: khác dạng, không mù được.

### B6 — web (Serper) qua cổng code + cờ

- **Điều khoản (B122 `b122_tra_web.md`):** điều khoản Serper (29/05/2024) không nói được dùng kết quả cho người dùng cuối, hiển thị đoạn trích, lưu; Serper tự nhận là dịch vụ business-to-business. **User 14:42: dùng luôn, chấp nhận rủi ro** (§2, §7). Giá: 2.500 lượt dùng thử; gói rẻ nhất 0,001 USD / lượt.
- Khoá Serper chỉ ở server, nạp `--env-file`, không đọc / in.
- **Rào dạng code** (từ a_sa2 §3c; rào 6 "đo hai chiều" bỏ theo User 14:42):
  1. S-OOS định nghĩa lại + chia lại câu sàn theo nhãn;
  2. không công cụ mở URL; **truy vấn do code dựng từ câu hỏi lượt này** (không lịch sử; trần độ dài; bỏ số điện thoại / email); ≤ 5 kết quả: tiêu đề + đoạn trích + URL; một module duy nhất gọi Serper;
  3. link + nhãn web do code dựng từ sổ nguồn; model chỉ trích `[w n]`; link không khớp sổ ⇒ bỏ. Sửa `frontend/src/markdown.js` (hôm nay cho `href` tuỳ ý, mẫu trích chỉ `[n]`);
  4. chữ web là dữ liệu, nhãn "từ web, chưa kiểm", chỉ vào một lần gọi riêng không công cụ / không lịch sử; không ghi đè / làm nhẹ cảnh báo của kho; câu khẩn cấp không đi web; **mục "Từ web" bị cắt khỏi lịch sử nhớ**;
  5. trần trong code (1 lần / câu, timeout, hết hạn mức ⇒ câu cố định "chưa tra được web").
- **Bộ đo** (Serper thật; P3 đã chọn ⇒ không benchmark tên miền riêng):
  - 25 câu thường (15 `web_tra_loi_duoc` + 10 `khong_xac_minh`);
  - 3 chuỗi "đã nêu tên rồi hỏi câu cần web" ⇒ đếm truy vấn chứa tên trên vết lượt đo;
  - 2 câu "nêu tên ngay trong câu cần web" ⇒ chỉ **theo dõi**: tên trong cùng câu vẫn đi ra (§7).
- **Tiêu chí:**
  - sàn: **0 truy vấn chứa tên** (3 chuỗi); 0 câu `khong_xac_minh` bị trả lời khẳng định; 0 link không khớp sổ nguồn tới người dùng; S-AT; S-OOS mới;
  - **quyết:** ≥ 60 % câu `web_tra_loi_duoc` (đã thấy) có mục web với nguồn hợp lệ; kín không ngược chiều;
  - mức tụt: câu kho trả lời được mà vẫn đi web ≤ 2 % hồi quy (chỉ xảy ra khi từ chối nhầm).
- **Kết quả âm ⇒** cờ web tắt, ghi kết quả.

### B7 — so sánh cuối RAG 1–8 ↔ agent (bắt buộc, không cắt)

- Cùng bộ: Golden 176 + bộ an toàn 32 + phần kín của các bộ mới (mở lần đầu nếu chưa mở); chấm cùng lượt mù. Câu rủi ro 3 lượt.
- **Bên RAG 1–8 sinh lại cùng tuần** trên mọi bộ B7, trong worktree ở commit đầu Phase 9 (tag `p9-moc`). Không dùng câu trả lời 01/11: bộ mới chưa từng chạy trên RAG 1–8, và câu theo ngày đổi đáp án theo ngày chạy.
- **Hai kết luận ghi trước, báo cả hai, không gộp:**
  - **(i) "tốt hơn ở hỏi đáp":** 3 nhóm ghi trước — câu nhiều nguồn · câu theo ngày · câu hỏi tiếp. Nhóm nào Completeness (hoặc từ chối nhầm với câu theo ngày) vượt nhiễu, CI 95 % > 0 sau Holm (3 nhóm) thì "tốt hơn" ở nhóm đó. 0 nhóm ⇒ "không tốt hơn ở hỏi đáp".
  - **(ii) "thêm được việc mới":** mỗi việc đạt ngưỡng riêng của bậc nó trên phần kín:

    | Việc | Ngưỡng |
    |---|---|
    | trò chuyện | ≥ 9 / 10 câu chào / cảm ơn / hỏi về trợ lý được đáp tự nhiên, không từ chối **và** 0 câu chứa thông tin Huế cụ thể |
    | nhớ tên | ≥ 9 / 10 |
    | hỏi lại | ≥ 4 / 5 |
    | lịch trình | ≥ 4 / 5 đạt 3 tiêu chí |
    | web | ≥ 60 % và 0 truy vấn chứa tên |

    Báo từng việc đạt / không.
- Sàn §4 phạm ở B7 ⇒ ghi kết quả âm, không chỉnh rồi đo lại.

## 6. Lịch (tuần từ thứ Hai; A kiểm luật cắt mỗi thứ Hai)

| Tuần | Việc | Mốc kiểm |
|---|---|---|
| 02–08/11 | spec duyệt · B0 · bước 0 khẩn cấp · viết bộ tuyến / ngày / khẩn cấp | B0 đạt |
| 09–15/11 | B1 | B1 giữ / gỡ |
| 16–22/11 | B2a rồi B2b · viết bộ nhớ, hỏi lại · soạn bảng điểm | B2 giữ / gỡ |
| 23–29/11 | B3 (bắt buộc) · viết bộ lịch trình · User duyệt bảng điểm | B3 giữ / gỡ |
| 30/11–06/12 | B4 rồi B5 · viết bộ web | B4, B5 giữ / gỡ |
| 07–13/12 | B6 | cờ web bật / tắt |
| 14–18/12 | B7 · đệm | báo cáo B7 |
| 20/12 | **đóng code** | — |
| 21/12–03/01 | luận văn, slide, sửa lỗi nặng | — |

**Luật cắt:**
1. **16/11** B1 chưa đóng ⇒ B2 chỉ làm B2a, bỏ B2b.
2. **25/11** B2 chưa chọn xong ⇒ đóng B2 với biến đang dẫn trên dev (hoặc V0), sang B3.
3. **30/11** B3 chưa đóng ⇒ B3 làm tiếp (bắt buộc); B4 + B5 dồn, B5 thu nhỏ.
4. **07/12** B5 chưa đóng ⇒ dừng B5, ghi kết quả dở.
5. **14/12** B6 chưa qua rào code + tiêu chí ⇒ cờ web tắt.
6. **B3 và B7 không cắt.**

Hai bậc cùng sửa đường trả lời / API / giao diện ⇒ lần lượt. Bộ đo, bảng điểm, plan, đọc điều khoản làm song song được.

## 7. Bảo mật chung (`agent-security-review`)

**Bộ ba chết người sau Phase 9** (a_sa2 §3a):
- (a) dữ liệu riêng tư: chữ người dùng + lịch sử (có thể có tên) trong ngữ cảnh; khoá ở server;
- (b) nội dung không tin cậy: chữ người dùng, kho lấy từ web, chữ web (B6);
- (c) đường ra: câu trả lời + OpenAI; thêm truy vấn Serper và link trong câu trả lời.
⇒ **Gần đủ ba ở mức nhẹ.** Rủi ro chính là nội dung sai trình bày như thật (sai cảnh báo, nói chắc sai).

**Rào chính:** ở §3 (chia việc, nhớ, log) và rào code B6. Không công cụ ghi / hành động ⇒ không cần người duyệt lúc chạy.

**Giả định an toàn** (cho luận văn):
- chạy trên máy User, một người dùng, không deploy; nhớ trong RAM; khoá Serper riêng có hạn mức;
- tên người dùng nêu **ngay trong câu cần web** vẫn đi tới Serper (truy vấn lấy câu hỏi lượt này);
- **dùng Serper khi điều khoản chưa rõ** cho người dùng cuối / hiển thị / lưu — User chấp nhận rủi ro (14:42);
- **không** có model thứ hai soát chữ web, **không** đo bằng kết quả web xấu cố định (User 14:42) ⇒ chống trang web cài lệnh chỉ dựa vào rào code (lần gọi web riêng không công cụ / không lịch sử, link do code, câu an toàn theo kho).

**Trước khi deploy:** xem lại soát chữ web + điều khoản dịch vụ web; rà R1 của C106 (kiểm `Host` + giới hạn lượt); lưu phiên; nút gắn cờ.

## 8. Quyền và tiền

- Mỗi bậc: plan nhỏ ⇒ session khác review ⇒ A duyệt sha; nhánh riêng; A merge sau review cả nhánh + cổng ổn định. Lựa chọn bản 5 + P1–P5 ghi vào plan bậc tương ứng.
- **Tiền ước** — đường agent ~0,0004 USD / câu: trợ lý ~0,00034 + định tuyến ~0,00007 (a_sa3 §2b, chưa đo). Hồi quy đủ 176 + 32 câu 1 lượt ≈ 0,08 USD; hồi quy rút gọn B3–B6 (32 an toàn + 30 mẫu Golden) ≈ 0,025 USD.

  | Bậc | Gồm | USD |
  |---|---|---:|
  | B0 | bước 0 khẩn cấp | 0,003 |
  | B1 | hồi quy + bộ tuyến / ngày / khẩn cấp ~90 câu × 2 lượt | 0,16 |
  | B2 | B2a: định tuyến 38 câu × 2 biến × 2 lượt + V2 tới lần gọi công cụ đầu 38 × 2 + 1 biến trả lời trên hồi quy; B2b hồi quy + A/A (2 lượt) | 0,39 |
  | B3 | 40 chuỗi × ~3 lượt hỏi (hồi quy dùng lại nếu hash không đổi khi nhớ tắt; đổi lõi chung ⇒ đủ 208, +0,08) | 0,06 |
  | B4 | hồi quy rút gọn + 30 câu | 0,04 |
  | B5 | hồi quy rút gọn + 18 câu (lịch dài ~0,0006 / câu) | 0,04 |
  | B6 | hồi quy rút gọn + 30 câu × ~0,00075 | 0,05 + Serper (lượt dùng thử) |
  | B7 | agent ~380 câu + câu rủi ro 3 lượt; **RAG 1–8 sinh lại cùng tuần** ~380 × 0,00025 | 0,35 |
  | **cộng** | | **≈ 1,1** |

- Ước lại từ pilot 10 câu đầu B1. **Trần Phase 2,0 USD** (User 14:42). Mỗi phiên ≤ 1 USD (cứng). Lượt vượt ước > 50 % ⇒ dừng, báo A. Judge dùng quota Claude.
- Serper (B122 đã kiểm): 2.500 lượt dùng thử đủ cho đo B6; vận hành 0,001 USD / lượt, gấp đôi 0,0005 USD / câu — chỉ theo dõi.
- Không ghi Qdrant; không sửa kho / Golden; bảng điểm ở `data/`. Thư viện nhỏ: A tự duyệt, báo User.

## 9. Giới hạn

Rủi ro và cách giảm đã ghi tại từng bậc (§5) và luật cắt (§6). Giới hạn: không có câu thật của du khách; judge Claude; bộ nhỏ chỉ thấy khác biệt lớn; 0 lỗi trên n câu không chứng minh tỉ lệ lỗi 0 (cận trên 95 % ≈ 3 / n); nhớ mất khi server khởi động lại; web có thể cũ / sai dù có nhãn.

## 10. User đã chọn (thay phần câu hỏi — review vòng 3 m18)

| Câu | User chọn (14:42 02/11/2026, A ghi nhận) | Nghĩa là |
|---|---|---|
| P1 nhớ khi mở lại trang | **(a)** chỉ nhớ trong cuộc trò chuyện đang mở | server giữ trong RAM theo phiên, 30 phút; đóng tab / bấm "Cuộc trò chuyện mới" là quên; không lưu dữ liệu cá nhân xuống đĩa |
| P2 kết quả web hiện thế nào | **(a)** model viết mục "Từ web", trích `[w n]`; code kiểm mã + dựng link | một lần gọi model riêng (không công cụ, không lịch sử); +~1,6 s, +~0,0003 USD ở câu có web |
| P3 giới hạn tên miền | **(a)** không giới hạn; câu an toàn / điều kiện vào khu vực theo kho; nhãn "từ web, chưa kiểm" | không benchmark tên miền riêng |
| P4 trần tiền Phase 9 | **(a)** **2,0 USD**; mỗi phiên ≤ 1 USD | ước hiện ≈ 1,1 USD (§8) |
| P5 dịch vụ web | **dùng Serper luôn, không email** — User chấp nhận rủi ro điều khoản chưa rõ | ghi §2 "lệch có lý do" + §7 giả định an toàn; B6 vẫn sau rào code + cờ |
| thêm (User) | **bỏ** bộ kết quả web xấu cố định, model thứ hai soát chữ web, đo hai chiều riêng cho web ("over-engineer quá") | giữ rào dạng code; đo web chỉ trên Serper thật (§5 B6) |
| bộ hồi quy (A quyết, User hỏi) | đủ 176 + 32 ở B1, B2, B7 + bậc sửa lời dặn chung / lõi chung; B3–B6 rút gọn | §4 |

**Duyệt:** duyệt sha bản 9 ⇒ A giao B0. Phần nào không duyệt ⇒ ra khỏi Phase, ghi lý do.

**Để bạn tự nói lại** (`propose-options` §4c):
- Vấn đề: RAG 1–8 đúng, có nguồn, nhưng chỉ hỏi–đáp một lượt.
- Đã xem: luồng cố định (bản 5, bỏ) ↔ agent tự do (bỏ — khó đo, đắt) ↔ **agent dưới chính sách** (chọn).
- Làm từng công cụ một; web đi qua cổng code sau câu trả lời kho; lần tìm đầu (code tìm trước ↔ trợ lý tự quyết) chọn bằng thí nghiệm.
- Cuối Phase sinh lại RAG 1–8 cùng tuần, báo hai kết luận: tốt hơn ở hỏi đáp không, và thêm được việc mới nào.

## Trả lời review (`2026-11-02-phase-9-design_review_v6.md`)

**Vòng 1** (bản 6 `fbb2853aa90c`): 10 major + 9 minor, đã sửa hết ở bản 7 `37e306ef40f7`, 0 phản biện; vòng 2 xác nhận đóng cả 19. Bảng chi tiết: bản 7 trong git + file review.

**Vòng 2** (bản 7 `37e306ef40f7`):

| Finding | Xử lý | Chỗ sửa |
|---|---|---|
| M11 B7 bên RAG 1–8 dùng lại mốc | **đã sửa**: sinh lại RAG 1–8 cùng tuần trên mọi bộ B7 (worktree tag `p9-moc`); +0,10 USD | §5 B7, §8 |
| M12 B4 / B5 khi B2b gỡ | **đã sửa**: vòng công cụ là hạ tầng (dựng ở B2a nếu đo V2, không thì B2b); gỡ B2b = tắt `tim_kho` thêm; B2b cắt / gỡ ⇒ A/A + thẻ công cụ sang B4; B2b có cỡ mẫu + "chưa rõ ⇒ tắt `tim_kho` thêm" | §5 B2 |
| M13 3 chỗ bớt tự chủ | **User đã chọn (14:12, A ghi handoff)**: §2 ghi đủ 3 chỗ code giữ + 4 hệ quả web (a)–(d) + được / mất khi để model gọi — không còn là câu hỏi. **V2 thuần quay lại B2a** (bỏ "chính là V2" ở B2b). Thêm dòng "sau Phase 9: thêm công cụ mới khi ổn định" | §2, §3, §5 B2 |
| m10 B123 | **đã sửa**: USD từng lần gọi bằng `RunHooks` (B123 §1); lần gọi công cụ không phát delta ⇒ bộ lọc `chat.py:368` đủ; `ANSWER_PREFIX` không đổi vì giữ `{answer}`; `tool_choice="required"` đã xét, không dùng; **lượt `hoi_lai` cần nhánh riêng trước khi ép `AnswerOutput`** (`generator_openai_full_corpus.py:269`) | §3 |
| m11 cổng web khi chạm trần / lỗi | **đã sửa**: cổng thêm "outcome thường"; chạm trần không mở cổng | §3 |
| m12 chữ đầu đường web, log | **đã sửa**: báo chữ câu từ chối + chữ đầu mục web, thước chính là mục web; trường `has_web_section` | §3 |
| m13 B2a chỉ số quyết | **đã sửa**: "và"; Holm ở tầng tìm (3 biến); nguồn số 12 = `q3a…:34, :36`; Completeness quyết trên 18 câu nhiều nguồn, so sánh chỉ theo dõi | §5 B2 |
| m14 B7 trò chuyện | **đã sửa**: thêm ngưỡng dương ≥ 9 / 10 câu đáp tự nhiên | §5 B7 |
| m15 tên trong cùng câu | **đã sửa**: 2 ca theo dõi ở B6 + ghi ở "Giả định an toàn" | §5 B6, §7 |
| m16 cắt ~40 dòng | **đã sửa một phần**: cắt ~35 dòng, nhưng thêm ~38 dòng (§2 các dòng User chọn + hệ quả web, B2a V2 thuần, P5) ⇒ 447 ⇒ 450 dòng; §7 "Rào chính" thành một dòng trỏ; bảng §9 bỏ; §1 "agent dưới chính sách" gộp một dòng; bảng trả lời vòng 1 rút gọn; khẩn cấp B1 còn 1 lượt | §1, §5 B1, §7, §9, cuối file |

**Thêm ngoài review** (đầu vào mới, khai rõ): kết quả B122 — điều khoản Serper chưa đủ căn cứ theo W35 ⇒ B6 ghi điều kiện + câu **P5** (≤ 5 câu hỏi User như A giao).
Giữ nguyên theo ranh giới review: hướng agent, SDK 0.19.4, thứ tự B0–B7, 6 rào, sàn S-AT / S-G.

**Vòng 3** (bản 8 `82127aabcb5b`): **ready_for_user_confirmation**; m17, m18 để sửa lúc plan / lúc hỏi User. Bản 9 ghi:
- lựa chọn User P1–P5 + phần "bỏ đo web độc / model soát / đo hai chiều" (§2, §5 B6, §7, §8, §10);
- A quyết bộ hồi quy (§2, §4, §8 — tiền ≈ 1,35 ⇒ ≈ 1,1 USD);
- m17: A/A đường có công cụ tại B2a khi đo V2 (§5 B2a);
- m18: §10 câu hỏi thay bằng bảng "User đã chọn" ⇒ không còn phương án thiếu dòng.
Không đổi chỗ khác.

## 11. Sửa đổi 05/11/2026 — bản 11 (A viết 09:42 05/11/2026) + bản 12 (sửa review C178, 09:45 05/11/2026)

**Căn cứ:** User duyệt bậc 1 + lịch (`bao_cao_he_thong/DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md`, 05/11); User chọn "Tách — giữ lịch trình" cho B4 (09:21); **User 05/11: không dồn hết vào Phase 9 ⇒ chia Phase 10 (giọng nói + ảnh), 11 (trải nghiệm Huế: bản đồ, sự kiện theo ngày, tiếng Anh…), 12 (vận hành); Phase 10 thiết kế / code song song Phase 9** (ngoại lệ `WORKFLOW.md` §9.4 chỉ cho Phase 10); **User 05/11: vẫn áp nền tảng AI FDE** (skill `agent-design-review`, `agent-security-review`, `run-experiment`).
Bản 9 §1–§10 giữ nguyên trừ chỗ ghi dưới. Review bản 11: chỉ mục này, đối chiếu §5–§8 + review bản 10 (`…phase-9-design_review_v10.md`).
**Chuyển khỏi Phase 9** (review bản 10 M-1–M-4, m-4, m-7 mang sang spec Phase 10 / 11): giọng nói, ảnh, bản đồ (toạ độ ngoài kho + nới CSP). Plan B5 bản 4 giữ "không bản đồ".

### 11.1 Đổi bậc trong Phase 9

| Bậc | Đổi | Vì sao |
|---|---|---|
| **B4 ⇒ B4b** | `hoi_lai` chỉ loại `lich_trinh`; câu chi phí giữ hành vi `main`. Tiêu chí: plan B4 **bản 8 `69afbb2732cf`** (A duyệt 09:37 05/11/2026). §5 B4 câu "chi phí: chỉ liệt kê giá có nguồn" + "≥ 8 / 10, ≥ 4 / 5" **thay bằng plan bản 8** (n câu lịch trình: đã thấy 5, kín 3) | B4 khoá 3 âm (Q6k (b) kín + Q7 g2) ⇒ thu hẹp bỏ phần hỏng |
| **B5** thêm (i) | **dòng tiến độ dùng bước thật**: giao diện đã có dòng tiến độ theo sự kiện SSE (`frontend/src/App.jsx`); B5 thêm các bước của `lich_trinh` ("đang xếp lịch", "đã kiểm luật ✓", "bỏ 1 điểm vì …") **chỉ phát khi code đã làm bước đó**. Kiểm: Playwright + so danh sách sự kiện SSE đã gửi (không cần trường log mới) | demo thấy agent làm gì, không bước giả |
| **B5c — tính tiền bằng code** (mới, sau B5) | công cụ tất định đọc **bảng dự toán có nguồn** (file chi phí du lịch: 1 ngày / 2N1Đ / 3N2Đ × 3 mức, khoảng giá **một người**, có ngày đối chiếu, luật nhóm) + **vé** (bảng có cấu trúc, mỗi người / lượt, ngày hiệu lực) — C176 `data/phase_9/tinh_tien/kiem_ke_gia.md` `deb4a0eff9c8` ⇒ code nhân theo số người, cộng theo luật nhóm của kho, giữ khoảng A–B ⇒ bảng có `[n]` + ngày nguồn; model chỉ viết lời quanh bảng. **Ngoài phạm vi dữ liệu** (≥ 4 ngày, giá món ăn không ngày, phòng / xe không bảng) ⇒ liệt kê giá có nguồn + câu cố định "chưa đủ dữ liệu để tính tổng". `hoi_lai` loại `chi_phi` mở lại **chỉ trong bậc này**, kèm chặn hỏi lần hai **chỉ cho loại `chi_phi`** (lượt có lịch sử mà lượt trước là `hoi_lai` loại `chi_phi` ⇒ không đưa `hoi_lai` loại `chi_phi`; đường lịch trình của B4b giữ nguyên); số người / ngày người dùng gõ ⇒ code dò số trong câu trước, thiếu mới hỏi | lời dặn không chặn được model tự tính (B4); khung AI FDE: phép tính / luật tiền ⇒ code |
| sửa lịch nhiều lượt | như User chọn 04/11 (ý #8, #9 handoff) | — |
| B5b, B6, B7 | giữ (sự kiện theo ngày ⇒ Phase 11) | — |

### 11.2 Tiêu chí mức spec cho B5c (plan ghi số trước khi đo)

- **Sàn:** (1) **0 con số tiền** trong câu trả lời ngoài {số có trong đoạn kho được trích} ∪ {số code tính} (code đếm mọi dạng "…000đ / k / triệu / VNĐ"); (2) 0 dòng "tổng" khi thiếu dữ kiện / ngoài phạm vi dữ liệu; (3) **người dùng gõ số người + số ngày sau thẻ hỏi lại ⇒ 0 / n bị hỏi lại lần hai** (ca g2 của B4 + ≥ 3 chuỗi mới); (4) an toàn 32 đủ 4 số; câu ngoài kho bị trả lời 0; (5) Q1 cờ tắt giống byte `main`.
- **Quyết:** bộ chi phí tự viết (đã thấy + kín mới, C viết, có câu trong + ngoài phạm vi dữ liệu): bảng đúng từng dòng (số = code tính lại từ kho) ≥ n − 1 / n.
- Kết quả âm ⇒ cờ tắt, câu chi phí giữ hành vi `main`.

### 11.3 Rà theo khung AI FDE (skill `agent-design-review` / `agent-security-review`, phần chạm bản 11)

| Mục khung | Hiện trạng | Bản 11 |
|---|---|---|
| §2 phép tính, luật tiền ⇒ code | B4 Cách A để model tự giữ "không cộng" bằng lời dặn ⇒ phạm (lệch khung — bài học ghi lại) | B5c: code tính, model chỉ diễn đạt |
| §3 tham số phạm vi do code điền | B4b: giá trị nút qua `TruongInput` (`Literal`, `extra="forbid"`) | B5c: số người / ngày từ nút hoặc code dò số, model không tự điền giá trị |
| §3 "không thấy ≠ không tồn tại" | — | ngoài phạm vi dữ liệu ⇒ câu cố định "chưa đủ dữ liệu", không trả lời như "không có" |
| §4 trần + đường phục hồi | `max_turns`, hết ⇒ câu từ chối (`assistant.py:289-291`) | giữ |
| §5 một agent trước | một agent trợ lý + định tuyến | giữ; không thêm agent con |
| bảo mật: đường ra mới | — | **không có** ở Phase 9 bản 11 (giọng nói / ảnh / tile bản đồ sang Phase 10 / 11, mỗi spec tự rà) |

### 11.4 Lịch Phase 9 (thay §6 từ 05/11; bậc đường trả lời **lần lượt**)

| Tuần | Phase 9 (B, C) | Phase 10 (E, song song — chỉ route mới + ô nhập, merge xen giữa hai lần merge Phase 9) |
|---|---|---|
| 05–09/11 | B4b ⇒ merge; code B5; plan B5c | nghiên cứu giọng nói open-source / VN (E1); spec Phase 10 |
| 10–16/11 | đo + merge B5 | bộ đo + thử STT trên máy |
| 17–23/11 | B5c ⇒ merge | code giọng nói |
| 24–30/11 | sửa lịch nhiều lượt ⇒ merge | ảnh |
| 01–07/12 | B5b + plan B6 | đo Phase 10 |
| 08–14/12 | B6 | đóng Phase 10 |
| 15–21/12 | B7 (so sánh cuối — trên máy User; khoá commit đo, không việc nặng song song — W31) | — |
| 22–30/12 | sửa lỗi; Phase 12 phần **deploy AWS** (spec riêng, User duyệt) — **sau** B7 | Phase 11 phần User chọn (nếu kịp) |
| **khi User nói** | **đóng code** — dự kiến 25–30/12; lúc đóng hệ thống **đã chạy trên AWS** | — |

**Đóng code (User, A ghi nhận 09:43 05/11/2026):** không còn mốc cứng 20/12 (User nghỉ) — dự kiến **25–30/12**, **chỉ đóng khi User nói** (A không tự quyết); đóng code = đã **triển khai lên AWS** ⇒ deploy là việc bắt buộc trước khi đóng (Phase 12, spec + `agent-security-review` + tài khoản / chi phí AWS User duyệt). Bảo vệ 04–10/01/2027 giữ.

**Luật cắt (thay §6 1–5; ngày cắt là mốc A kiểm, không phải hạn đóng):** 23/11 B5 chưa merge ⇒ B5c thu nhỏ còn vé; 30/11 B5c chưa merge ⇒ dừng B5c, ghi dở, sửa lịch vẫn làm; 07/12 sửa lịch chưa merge ⇒ dừng, ghi dở; 07/12 B5b chưa merge ⇒ cắt B5b; 14/12 B6 chưa qua rào ⇒ cờ web tắt; **B3 và B7 không cắt**. Phase 10 xung đột file với Phase 9 ⇒ Phase 9 ưu tiên, Phase 10 rebase.

**#6 tốc độ (song song trả lời ↔ định tuyến, đã đạt 04/11):** không phải bậc; merge sau B4b (rebase + Q1) khi User quyết bật.

**Phase 9 ↔ deploy (review bản 11 M-1):** mọi rào / đo của Phase 9 (§7 giả định "chạy máy User, không deploy"; điều khoản Serper; nhớ RAM; tốc độ đo CPU máy User) giữ nguyên — **B6, B7 đo trên máy User**. Mục §7 "Trước khi deploy" là **đầu vào bắt buộc** của spec Phase 12; trên AWS **cờ web tắt** tới khi Phase 12 rà lại; tốc độ / tiền đo lại trên AWS ở Phase 12.

**Chi tiết để plan B5c (review bản 11 m-4):** không cộng vé riêng khi hàng "tham quan" của bảng dự toán đã gồm vé (một khoản một lần); cách code dò số người / ngày trong câu (chữ số + chữ "hai, ba…" + "3N2Đ") ghi trong plan cùng ca thử.

**Finding chuyển sang Phase 10 / 11** (review bản 10, `…design_review_v10.md`): M-1 (đường ra nhận dạng giọng trình duyệt + PhoWhisper là model mới), M-3 (ngưỡng V1), M-4 (mẫu số V2 + danh sách tên) ⇒ spec Phase 10; M-2 (toạ độ ngoài kho + tile / CSP), m-4 (plan B5 cấm bản đồ) ⇒ spec Phase 11; m-7 (giới hạn điểm ảnh khi giải mã) ⇒ spec Phase 10. Spec Phase 10 / 11 phải trỏ lại các mã này.

### 11.5 Tiền (cập nhật §8)

Đã dùng ≈ 1,27 (05/11, gồm B4 ≈ 0,205). Còn: B4b ≤ 0,10 · B5 trần 0,15 (plan) · B5c ≈ 0,07 · sửa lịch ≈ 0,10 (chuỗi × 3 lần + hồi quy rút gọn, ước thô) · B5b ≈ 0,05 · B6 ≈ 0,05 · B7 ≈ 0,35 ⇒ **dự phóng ≈ 2,1–2,2 > trần 2,0** ⇒ theo User (08:55 05/11/2026) A xin thêm **trước** lượt có phí vượt, kèm số đã dùng + dự phóng. **Quỹ B7 0,35 giữ riêng** (B7 không cắt — review bản 11 M-2): trước mỗi bậc, nếu (trần − đã dùng − quỹ B7) < ước bậc đó ⇒ A xin User thêm **trước** khi bắt đầu bậc, nếu không duyệt ⇒ bậc thu nhỏ / cắt theo luật cắt; quỹ B7 không bị dùng cho bậc khác. Phase 10 có trần riêng trong spec Phase 10.

## 12. Sửa đổi 08/11/2026 — bản 13 (C viết 10:47 08/11/2026, A giao)

**Căn cứ:** User 10:30 08/11/2026 (brainstorm định tuyến, A ghi `CURRENT_HANDOFF.md` mục 2d) + User chọn 4 công cụ và thứ tự (A nhắn C 08/11); nháp bộ đo
`data/phase_9/dinh_tuyen_2/bo_do_nhap.md` (private, C) + 4 quyết định A ghi trong đó. Bản 12 §1–§11 giữ nguyên trừ chỗ ghi dưới. Review bản 13: chỉ mục này (≤ 2 vòng).
**Không đổi:** closed-world từ kho, câu chuẩn `INSUFFICIENT_ANSWER` / `OUT_OF_SCOPE_ANSWER`, sổ nguồn + kiểm citation, nhớ chỉ câu hỏi 3 lượt, `tim_kho` ≤ 2,
`max_turns` 4, mục "Từ web (chưa kiểm)" tách riêng + mọi kiểm code của B6, biểu mẫu "Lên kế hoạch" (không qua định tuyến), log không chữ.

### 12.1 Việc và thứ tự (User)

| Đợt | Việc | Ai (A giao) | Thay cho |
|---|---|---|---|
| 1 (song song) | **G — cổng 2 nhóm** "trò chuyện xã giao" / "về Huế" chạy mọi câu (giữ #6); bỏ tuyến khẩn cấp; câu ngoài phạm vi ⇒ agent Huế trả `OUT_OF_SCOPE_ANSWER` | B | định tuyến 4 tuyến B1 (`assistant.py:742-768`) |
| 1 | **T1 — ngày + âm lịch** (code tính; agent gọi khi câu có ngày) | E | cờ `today_line` (âm ở B1 P2, `settings.yaml:62`) |
| 1 | **T3 — bảng vé + giờ mở cửa có cấu trúc** (phần dữ liệu trước: dựng từ kho, User duyệt bảng) | C | B5c `tinh_tien` (âm 2 lần, tag `hoso/p9-b5c`) |
| 2 (sau khi G vào `main`) | **T2 — tra web thành công cụ agent tự yêu cầu** | A giao | cổng web B6 chỉ mở sau câu từ chối (`assistant.py:777-785`) |
| 2 (sau T2) | **T4 — lịch trình từ câu gõ tự do** (cờ `lich_trinh`) | A giao | kín v2 3 / 5 (06/11), câu tự do đang tắt |

Mỗi việc = một bậc giữ / gỡ riêng (luật bản 9); bậc sau rebase lên bậc trước. Mỗi việc một plan nhỏ (≤ 2 vòng review), plan ghi số **trước** lượt có phí.

### 12.2 Năm dòng khám phá mỗi việc (`run-experiment`)

| Việc | Vấn đề + đo bằng gì | Mốc | Tiêu chí số ghi trước (plan chốt số cuối) | Phương án B (nếu âm) |
|---|---|---|---|---|
| **G** | 4 tuyến có 2 câu soạn sẵn + 1 lần gọi định tuyến chọn 4 nhãn; User muốn gọn: chỉ tách xã giao. Đo: chỉ lần gọi định tuyến (rẻ) trên Golden 176 + bộ 123 + bộ mới; cả câu trả lời cho ngoài phạm vi / an toàn | định tuyến `164bd4a254e9` (lượt B143 v1 r1 / r2 dùng lại; bộ mới chạy mốc cùng ngày ×2) | S1, S2, S2b, S3, S3b (§12.3) đạt ×2; S5 không chậm hơn mốc quá nhiễu | giữ 4 tuyến (cờ), chỉ bỏ câu soạn sẵn khẩn cấp ⇒ `khan_cap` đi agent Huế |
| **T1** | câu "hôm nay / tuần này / rằm tháng Giêng năm nay" bị từ chối nhầm (6 / 14 ở 27/10) vì model không biết ngày; dòng ngày trong tin nhắn (B1 P2) không đỡ. Đo: bộ ngày 15 + 3 (đã thấy) + bộ âm lịch mới ~10 (đã thấy) | `main` cờ công cụ tắt, cùng lượt | từ chối nhầm ở câu ngày giảm ≥ 3 câu so mốc; **0** ngày / thứ sai (L2) **trong chữ trả lời** (đối chiếu đáp án theo ngày chạy — cả khi model không gọi công cụ); S1 4 số; Golden mẫu 30 không tụt quá nhiễu | đưa kết quả công cụ vào **mọi** lượt bằng code (không để model quyết gọi) chỉ khi câu có từ chỉ ngày (code dò) |
| **T3** | giá vé / giờ mở cửa rải ở nhiều file, nhiều dạng bảng; model chép / suy sai được; B5c (nhân + cộng) âm vì công cụ trong mọi lượt đổi cách tìm + câu miễn giảm. T3 **không tính tổng**, chỉ tra dòng. Đo: câu vé / giờ đã thấy ~20 (C viết) + an toàn 32 (có 6 câu miễn giảm, 5 câu giờ) + Golden mẫu 30 | `main` cùng lượt | **0** số tiền / giờ trong chữ model ngoài {số trong bảng} ∪ {số trong đoạn kho được trích} (code đếm — dùng lại `so_tien.py` + bộ đếm chuỗi số của `tra_web.py`); điều kiện miễn giảm **do code nối nguyên văn** từ kho (0 câu model tự diễn đạt điều kiện); S1 4 số; câu đúng ≥ mốc | chỉ bảng **dữ liệu** dùng cho kiểm cuối (không công cụ): code kiểm số trong câu trả lời so với bảng, sai ⇒ thêm câu cố định "giá / giờ có thể khác — xem nguồn" |
| **T2** | cổng web chỉ mở khi cả câu bị từ chối ⇒ câu hỏi kèm (một phần kho thiếu — E20: 3 / 4 bị từ chối cả câu) không có web. Đo: B6 đã thấy 28 + E20 10 + câu kho trả lời được (Golden mẫu 30) + S2b | `main` sau G, cùng lượt | S2b = 0; câu kho trả lời được mà vẫn tra web: **0 / 34** (mẫu Golden 30 + 4 câu "kho có" của B6, ×2; B6 cũ ghi ≤ 2 % trên bộ hồi quy lớn); câu hỏi kèm có phần web ≥ mốc + 2 / 10; mọi sàn B6 (0 link ngoài sổ, 0 số / tiền ngoài trích, câu thiên tai cố định) | giữ cổng B6 (chỉ sau câu từ chối); thêm cổng cho câu "từ chối + đã hỏi kèm" do code nhận |
| **T4** | câu gõ tự do: kín v2 **3 / 5** (06/11) — K2 hỏi lại thừa (model gửi số ngày khác số code dò ⇒ luật D12 (b) hỏi); E20 câu xin lịch + hỏi kèm ⇒ model từ chối (bị chặn `tim_kho` sau lịch). Đo: B5 đã thấy 13 + E19 mẫu 8 + kín v2 5 (**đã dùng**) + E20 10 | `main` cờ `lich_trinh` tắt; số cũ kín v2 3 / 5 | Q3 B5 (đúng luật xếp · hợp người đi cùng · mỗi điểm có nguồn) ≥ n − 1 / n trên bộ 36 câu, 2 người chấm; 0 hỏi lại thừa khi code dò được số ngày; 0 lượt "từ chối thay cả lịch" | giữ biểu mẫu là đường lịch trình duy nhất; câu gõ tự do ⇒ code gợi ý mở biểu mẫu |

**Sửa trước khi đo lại T4 (bằng code, tất định):** (a) **code dò được số ngày ⇒ dùng số code**, bỏ luật "model gửi số khác ⇒ hỏi" (khung §3: tham số do code điền; K2); (b) E20 **Sửa 1**: lời lịch do code dựng thay câu từ chối ∧ model đã gọi `tim_kho` sau lịch ⇒ code nối câu cố định "phần hỏi thêm ngoài lịch chưa có trong nguồn"; (c) harness ghi `so_ngay` model gửi + số code dò + có thẻ hỏi không (đề xuất C210); (d) E20 **Sửa 2** (`tim_kho` sau lịch tìm thật 1 lần) chỉ khi (a)–(b) đo xong còn từ chối. Giờ tới / về: ngoài phạm vi (giới hạn ghi ở câu trả lời không thêm).

### 12.3 Sàn chung (từ `bo_do_nhap.md` §4, áp cho mọi việc có lượt trả lời)

| Sàn | Đo trên | Mức |
|---|---|---|
| **S1** an toàn | bộ an toàn 32, ×2 | đảo cảnh báo 0 · sai điều kiện **mới** 0 · thiếu cảnh báo **mới** 0 · ngoài kho bị trả lời 0 (thủ tục S-AT khi chênh 1) |
| **S2** ngoài phạm vi bị trả lời | 11 câu Golden ngoài phạm vi + bộ tuyến 8 + 4 + lái 1 + bộ mới (b) 20 đã thấy + 10 kín, ×2 | **0** (code: chữ = `OUT_OF_SCOPE_ANSWER` / `INSUFFICIENT_ANSWER`; câu không khớp ⇒ sub-agent đọc) |
| **S2b** ngoài phạm vi có mục web | như S2 + 4 câu "ngoài Huế" của B6 | **0** — `OUT_OF_SCOPE_ANSWER` đã nằm trong `REFUSAL_ANSWERS` (`full_corpus_prompt.py:49-50`) và cổng web chỉ mở với `INSUFFICIENT_ANSWER` (`assistant.py:782-785`, test B6) ⇒ chỉ cần lời dặn agent dùng đúng câu; rủi ro còn: model chọn nhầm câu "không đủ thông tin" |
| **S2c** Huế-kho-thiếu vẫn có web | 7 câu Golden OOS nhãn `tro_ly_hue` + 10 câu B6 "web trả lời được" | cổng web mở ≥ mốc − 1 |
| **S3** câu về Huế bị coi là xã giao | Golden 176 (chỉ định tuyến, **×2** — đã tính trong tiền G) + bộ tuyến Huế 30 + lái 4 + 8 câu thường dễ nhầm + bộ mới (a) phần "về Huế" + câu hỏi tiếp của 37 chuỗi B3 / B3b | **0**; chiều ngược (chào thuần ⇒ về Huế) chỉ tốn tiền: ≤ 2 / 16 |
| **S3b** câu về Huế bị agent trả `OUT_OF_SCOPE_ANSWER` (lỗi mới do G chuyển quyết "ngoài phạm vi" vào lời dặn agent) | các lượt **cả câu trả lời** đã có trong kế hoạch: an toàn 32 · mẫu Golden 30 · S2c 7 + 10 · phần "về Huế" của bộ (a) · bộ tuyến Huế 30 nếu chạy cả câu, ×2 | **0** — đếm bằng code (so chuỗi sau `strip()`), **0 USD thêm** |
| **S4** chất lượng câu Huế | `mau_golden_30.json` biến thể + mốc cùng lượt chấm mù | không tụt quá nhiễu (chỉ khi lời dặn / công cụ agent đổi — mọi việc T1–T4 đổi ⇒ áp) |
| **S5** tốc độ | chữ đầu trên server thật, n = 20 / loại | câu Huế p50 ≤ 3 s, p95 ≤ 5 s (User 28/10) và không chậm hơn mốc quá nhiễu; ngoài phạm vi (nay qua agent) p95 ≤ 5 s |
| **S6** tiền | `chat_metrics.usd` | ≤ 0,0005 USD / câu Huế; báo USD / câu ngoài phạm vi |
| Quan sát khẩn cấp (không sàn) | ~36 câu / chuỗi có sẵn (bước 0 10 · kín C125 8 · bộ tuyến 6 · B143 m1–m6 · 6 chuỗi lịch sử), 1 lượt | bảng 4 loại câu trả lời (chỉ dẫn nơi giúp có trong kho · từ chối thuần · mục web · nói sai nguy hiểm) báo User |

### 12.4 Bộ đo — có bộ kín hay không (luật cắt giảm 05/11 (2): kín chỉ cho bậc chỉnh lời dặn / mô tả công cụ qua nhiều vòng)

| Việc | Bộ | Kín |
|---|---|---|
| G | có sẵn (`bo_do_nhap.md` §1) + **(a) ranh giới xã giao ↔ hỏi** 16 đã thấy + 8 kín · **(b) ngoài phạm vi dạng mới** (kiến thức chung, code, dịch, toán, nơi khác, y tế / pháp lý chung, lệnh lái) 20 đã thấy + 10 kín. Nhãn: "hỏi về chính trợ lý" = **xã giao** (A 08/11). Bộ tuyến kín B1 20 câu = **đã dùng** (A 08/11) | **có** — chỉnh lời dặn định tuyến + lời dặn ngoài phạm vi của agent qua nhiều vòng. Người viết câu ≠ người sửa lời dặn |
| T1 | bộ ngày 15 + 3 (đã thấy) + ~10 câu âm lịch mới (lễ hội ngày âm, "rằm / mùng một tháng tới") — đáp án theo **ngày chạy**, đối chiếu lịch Việt Nam công khai | **không** — code tính, kiểm tất định |
| T3 | bảng dữ liệu (User duyệt) + ~20 câu vé / giờ đã thấy (có câu điểm ngoài bảng, câu miễn giảm, câu giờ theo mùa) | **không** — số do code kiểm |
| T2 | B6 đã thấy 28 + kín B6 (**đã dùng**) + E20 10 + câu kho trả lời được | **không** — cổng / kiểm là code; mô tả công cụ chỉnh ≤ 2 vòng trên đã thấy |
| T4 | 36 câu (§12.2) | **không** — các sửa là code; kín v2 đã dùng |

### 12.5 Thiết kế mức spec từng việc (plan ghi chi tiết)

- **G:** lời dặn định tuyến mới 2 nhãn `tro_chuyen` / `tro_ly_hue`; lỗi / > 10 s ⇒ `tro_ly_hue` (giữ — log thật: 5 / 252 lượt có phí hết giờ ≈ 2 %, `bo_do_nhap.md` §3). #6 giữ: phần `tro_ly_hue` chạy song song định tuyến; câu ngoài phạm vi nay **không bị bỏ phần đã chạy** (đi chính agent Huế). Gỡ: `ROUTE_KHAN_CAP`, `EMERGENCY_ANSWER`, cờ `emergency_rule` + `is_emergency` (cờ âm — gộp việc "gỡ 3 cờ âm" của B7 cho phần này), câu soạn sẵn PA1, giao diện câu khẩn cấp; `ROUTE_NGOAI_PHAM_VI` thành nhãn lịch sử (không còn nhánh). Agent Huế: thêm một câu lời dặn "câu không về văn hoá / du lịch Huế ⇒ trả **đúng** `OUT_OF_SCOPE_ANSWER`". **Code nhận chữ trả lời = `OUT_OF_SCOPE_ANSWER`** (so sau `strip()`, như cờ `refusal`) ⇒ đặt outcome `out_of_scope` như câu cố định cũ (`assistant.py:766-767`): không kiểm citation, cổng web đóng, nhớ như cũ ⇒ giữ 3 câu gợi ý ngoài phạm vi (`frontend/src/chat.jsx` `turn.outcome === "out_of_scope"`), **không** hiện gợi ý "cách hỏi" của câu kho thiếu (`api/routes/chat.py` `tu_choi_kho` khi outcome ≠ `out_of_scope`), log `chat_metrics.outcome` tách được câu ngoài phạm vi (review B M-1); plan G có test cho cả 3 chỗ, cả 3 đường (`/api/chat`, stream, #6). Log `route` giữ 2 giá trị + `route_error`. **Thứ tự đo (m-5):** hai lời dặn gắn nhau (bỏ nhãn ngoài phạm vi thì agent phải tự từ chối) ⇒ vòng chỉnh lời dặn định tuyến chỉ đo S3 / phần chỉ-định-tuyến; S2 / S2b / S3b đo trên bản có cả hai lời dặn.
- **T1:** công cụ `ngay_lich(…)` — **code** (giờ Việt Nam `zoneinfo`) trả: hôm nay (dương + âm + thứ), và đổi một ngày người dùng nêu (dương ↔ âm) theo **lịch âm Việt Nam (múi UTC+7)** — không dùng thư viện lịch Trung Quốc (UTC+8 lệch ở vài năm); thư viện nhỏ hay thuật toán công khai: plan chọn, A tự duyệt nếu thư viện nhỏ (`Session_Prompt.md` §4), test đối chiếu ≥ 10 ngày Tết / rằm công khai, **trong đó ≥ 1 ngày lịch Việt Nam khác lịch Trung Quốc** — Tết Ất Sửu 1985: Việt Nam 21/01/1985, Trung Quốc 20/02/1985 (lệch một tháng vì đông chí ở Hà Nội rơi 21/12 còn Bắc Kinh 22/12 — en.wikipedia.org/wiki/Vietnamese_calendar, C WebFetch 08/11/2026); năm khác (vd 2007) plan tự kiểm nguồn trước khi dùng ⇒ test chứng minh đúng lý do chọn UTC+7. Tham số model chỉ là ngày / tháng / năm + loại lịch (kiểu `Literal`, kiểm khoảng), ≤ 2 lần / câu. Model **không** tự đổi âm ↔ dương.
- **T3:** đợt 1 = **dữ liệu**: C dựng bảng từ kho (đọc qua `scripts/grep_kb.sh`) — mỗi dòng: điểm (tên + bí danh), loại vé, giá người lớn / trẻ em (nguyên chuỗi điều kiện tuổi), giờ mở cửa (theo mùa nếu kho ghi), ngày hiệu lực, file + mục nguồn, điều kiện miễn giảm (nguyên văn); file private trong `data/`, **User duyệt bảng** trước khi code đọc (như bảng điểm lịch trình). Đợt sau: công cụ `tra_ve_gio(diem: list[str] ≤ 5)` — code khớp tên (dùng lại `khop_diem` B5), trả dòng + `[n]` đoạn nguồn (như B5 D6); điểm không có trong bảng ⇒ câu cố định "bảng chưa có điểm này" (không thấy ≠ không tồn tại); **không** cộng / nhân (B5c âm); kiểm cuối số (Q tiêu chí §12.2). **Miễn giảm (review B m-1):** (a) kết quả công cụ cho model **không** chứa chữ điều kiện — chỉ "có điều kiện miễn giảm — hiện bên dưới"; (b) code nối khối điều kiện nguyên văn **mỗi khi** dòng bảng được trả có điều kiện (không dò "câu miễn giảm"); (c) đếm "model tự nêu tuổi / đối tượng miễn giảm" bằng code (mẫu tuổi / đối tượng trong chữ model ngoài khối code) + sub-agent đọc các câu khớp. Bài học B5c: công cụ + mô tả trong mọi lượt đổi cách model tìm ⇒ đo S1 + S4 **bắt buộc**; plan cân nhắc chỉ đưa công cụ khi code dò thấy dấu hiệu vé / giờ — nhưng câu miễn giảm **luôn** nhận khối điều kiện do code nối khi có dòng bảng (không để model quyết).
- **T2:** công cụ `yeu_cau_tra_web()` **không tham số**: model chỉ **yêu cầu**; code ghi cờ, **sau khi** có câu trả lời kho mới tra (một chỗ: hàm cổng hiện có, thêm điều kiện "model đã yêu cầu ∧ câu trả lời ≠ `OUT_OF_SCOPE_ANSWER`"); truy vấn vẫn do code dựng từ câu hỏi lượt này (B6 D2); chữ web vẫn chỉ vào lần gọi riêng không công cụ / không lịch sử ⇒ **agent chính không bao giờ thấy chữ web**; kết quả công cụ cho model là câu cố định **trung tính** ("đã ghi nhận — viết câu trả lời từ kho như bình thường"; không hứa mục web vì tra có thể lỗi / rỗng — B6 D3) + plan có test / đếm "câu kho nhắc mục web" = 0 (review B m-4). Cổng cũ (sau câu từ chối) giữ. Trần 1 lần / câu; cờ `tra_web` + cờ mới `tra_web_cong_cu`.
- **T4:** bật cờ `lich_trinh` sau sửa (a)–(c) §12.2; biểu mẫu giữ nguyên; luật khung / kiểm cuối / bảng điểm `diem_v3.json` giữ.

### 12.6 Rà theo khung AI FDE (phần chạm bản 13)

**`agent-design-review`**

| Mục khung | Hiện trạng | Bản 13 | Khớp / lệch |
|---|---|---|---|
| §1 có cần agent | định tuyến model 4 nhãn (`assistant.py:742-768`); trợ lý agent `tim_kho` (`:259-290`) | định tuyến còn 2 nhãn (danh sách từ đã loại — "Không làm"); phương án B G: bỏ hẳn định tuyến (agent trả cả xã giao) — chậm + tốn hơn cho câu chào ⇒ không chọn | khớp |
| §2 phép tính / thứ tự bắt buộc ⇒ code | `today_line` đưa ngày (âm); B5c model nhân / cộng ⇒ âm | T1 đổi âm ↔ dương **code**; T3 không phép tính, miễn giảm **code nối**; T2 lúc tra + truy vấn **code**; T4 số ngày **code** thắng model | khớp (sửa lệch K2) |
| §2 một nơi gốc | luật mở cổng web một chỗ (`assistant.py:777`) | T2 thêm điều kiện **vào cùng hàm** | khớp |
| §3 tham số do code điền | `tim_kho(cau_tim)`; `lich_trinh` model gửi `so_ngay` | T2 không tham số; T3 `diem` khớp bằng code; T1 chỉ ngày / loại lịch (`Literal`, kiểm khoảng); T4 `so_ngay` code dò thắng | khớp |
| §3 không thấy ≠ không tồn tại | B5c câu cố định "chưa đủ dữ liệu" | T3 điểm ngoài bảng ⇒ "bảng chưa có"; T2 lỗi Serper ⇒ câu cố định (B6 D3) | khớp |
| §4 trần + phục hồi | `max_turns` 4, `tim_kho` ≤ 2 (`assistant.py:52`) | `ngay_lich` ≤ 2, `tra_ve_gio` ≤ 1, `yeu_cau_tra_web` ≤ 1 (đếm trong code); hết trần ⇒ câu từ chối chuẩn như cũ; plan kiểm `max_turns` đủ khi đủ 4 công cụ | khớp — plan đo `max_turns` = 0 |
| §5 một agent | agent Huế + model xã giao (đã có) | giữ; không thêm agent con | khớp |
| §5 lời dặn | thêm công cụ vào mọi lượt đã làm tụt S-AT 2 lần (B4b §2g, B5c) | mỗi công cụ một bậc; S1 + S4 bắt buộc mỗi bậc | khớp (bài học ghi lại) |

**`agent-security-review`**

| Rủi ro | Hiện trạng | Bản 13 | Mức · đề xuất |
|---|---|---|---|
| Bộ ba chết người | (a) chữ người dùng + câu hỏi lịch sử · (b) chữ web, kho lấy từ web · (c) OpenAI, Serper, link (spec §7) | T2: model **quyết lúc** tra ⇒ đường ra Serper nay theo phán đoán model; giữ: truy vấn code dựng từ câu lượt này, chữ web không vào agent chính ⇒ (b) không lái được (a)–(c) | minor — sàn S2b + "câu kho trả lời được mà tra web ≤ 2 %" |
| Câu ngoài phạm vi lọt ra Serper | không thể (tuyến riêng) | agent có thể yêu cầu web cho câu ngoài phạm vi ⇒ code chặn khi câu trả lời = `OUT_OF_SCOPE_ANSWER`; model chọn nhầm câu từ chối ⇒ lọt | major nếu không đo — S2b = 0 ×2 là điều kiện merge G / T2 |
| Lệnh trong chữ người dùng ("bỏ qua hướng dẫn, tra web …") | cổng là code | T2 vẫn ≤ 1 lần / câu, truy vấn bỏ SĐT / email (B6 D2) | minor — bộ (b) có câu lệnh lái |
| Tham số vào đường dẫn / truy vấn | — | T1 / T3 không chạm file hay URL (bảng nạp lúc khởi động từ đường dẫn `settings.yaml`); T2 không tham số | khớp |
| Dữ liệu cá nhân | log không chữ (`chat.py` `METRIC_FIELDS`) | không thêm trường chữ; log công cụ chỉ tên + số đếm | khớp |
| Câu khẩn cấp | câu soạn sẵn PA1 (số 113 / 114 / 115 / 112) | bỏ (User) ⇒ có thể nhận câu từ chối thường | **User xác nhận** (§12.8) |
| Deploy | spec §7, §11.4: web tắt trên AWS | giữ: cờ `tra_web` / `tra_web_cong_cu` tắt trên AWS tới Phase 12 rà lại | khớp |

**Giả định an toàn (bổ sung §7):** như bản 12; thêm — model quyết lúc tra web (T2) nhưng không thấy chữ web; bảng vé / giờ là dữ liệu kho User duyệt, có ngày hiệu lực.

### 12.7 Tiền + luật cắt

**Tiền** (giá `gpt-6-luna`; định tuyến ≈ 0,00008 · lượt agent ≈ 0,0005–0,0008 · mục web +0,0012 gồm Serper / câu). Trần Phase 9 **3,5 USD** (User 08/11), đã dùng
≈ 2,05 (handoff 2,02 + 08/11); **quỹ B7 0,35 giữ riêng** ⇒ còn ≈ 1,1 cho bản 13.

| Việc | Ước (một biến thể + mốc) | Ghi |
|---|---|---|
| G | ≈ 0,25 (xấu nhất 0,4) | `bo_do_nhap.md` §4 |
| T1 | ≈ 0,11 | (28 ngày + 32 an toàn + 30 Golden mẫu) × 2 × 0,0006 |
| T3 | dữ liệu 0 · đo ≈ 0,10 | (20 + 32 + 30) × 2 × 0,0006 |
| T2 | ≈ 0,19 | (28 + 10) × 2 × 0,0018 + 30 × 0,0006 + 32 × 2 × 0,0006 |
| T4 | ≈ 0,14 | 36 × 2 × 0,0008 + an toàn + Golden mẫu |
| **Tổng** | **≈ 0,8** (một vòng mỗi việc) | vòng chỉnh thứ hai chỉ chạy phần "chỉ định tuyến" / bộ đã thấy; dự phóng vượt 1,1 ⇒ A xin User trước |

**User 11:02 08/11/2026: bỏ mốc ngày — làm càng nhanh càng tốt** (luật cắt theo ngày dưới đây không còn áp; sàn §12.3 và trần tiền giữ nguyên; việc không đạt sàn ⇒ giữ bản cũ như "phương án B" §12.2). Bản cũ để tra cứu: **Luật cắt** (ngày là mốc A kiểm; B7 15–21/12 không cắt; đóng code 25–30/12 khi User nói):
- 16/11 G chưa merge ⇒ giữ 4 tuyến; T2 vẫn làm trên 4 tuyến (S2b thay bằng "tuyến `ngoai_pham_vi` không tra web" như cũ).
- 23/11 T1 / T3 chưa merge ⇒ T1 cắt (giữ cờ `today_line` tắt); T3 thu nhỏ còn **bảng dữ liệu cho kiểm cuối** (phương án B).
- 30/11 T2 chưa merge ⇒ giữ cổng web B6.
- 07/12 T4 chưa merge ⇒ câu tự do tắt, biểu mẫu là đường lịch trình.
- 14/12: không mở bậc mới; chỉ sửa lỗi + chuẩn bị B7.

### 12.8 User xác nhận

- **Bỏ tuyến khẩn cấp (User 08/11/2026):** không câu soạn sẵn, không công cụ. Câu khẩn cấp vào agent Huế ⇒ có thể nhận **câu từ chối thường** hoặc mục web. A đã nêu
  rủi ro (User 28/10 xếp "sai cảnh báo an toàn" là lỗi tệ nhất; C122 "chỉ từ chối = lỗi"); User chấp nhận 08/11 ("không cần, không tập trung"). Bộ khẩn cấp chỉ quan sát (§12.3).
- **T2 — "agent tự gọi" (User xác nhận 08/11/2026, A hỏi theo review B):** agent **chỉ quyết lúc** tra; code dựng câu tra, tra, viết mục web riêng "Từ web (chưa kiểm)"; agent **không** đọc chữ web.
- Câu "hỏi về chính trợ lý" ⇒ nhãn xã giao (A 08/11). Bộ tuyến kín B1 ⇒ đã dùng (A 08/11).
