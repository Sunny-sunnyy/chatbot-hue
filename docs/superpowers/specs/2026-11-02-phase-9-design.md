# Phase 9 — trợ lý di sản Huế đáng tin + lịch trình gợi ý nhỏ — tài liệu thiết kế

Người viết: C · bản 1 09:59 · bản 2 10:14 · bản 3 10:27 · bản 4 10:36 · **bản 5 11:03 02/11/2026** (`date`).
- Bản 2 sửa theo review vòng 1, bản 3 theo vòng 2, bản 4 theo vòng 3 (`2026-11-02-phase-9-design_review.md`; vòng 4 bản 4 `589bec308f41`: ready_for_user_confirmation).
- Trạng thái: **bản 5 — User đã chọn Q1–Q5, chờ duyệt sha.** Bản 5 chỉ ghi lựa chọn vào §2, §5.4 (chi phí), §5.5 (nhãn "chờ Q5"), §6 (ô H2), §10.

Mức rủi ro: **cao** (Phase mới — `WORKFLOW.md` §3).
- Spec chỉ chốt **phạm vi, thứ tự, bộ đo, tiêu chí ghi trước, tiền, rủi ro** cho từng phần.
- Chi tiết code để **plan nhỏ của từng phần** khi tới lượt (S64). Phần nào phụ thuộc kết quả phần trước thì ghi "chốt lúc tới lượt".
- File tracked này **không chép nội dung kho, câu Golden hay câu kín**; câu ví dụ là câu tự viết.
- Phép đếm trên kho: danh sách file lấy bằng `scripts/grep_kb.sh`, chỉ in số; mẫu tìm ghi cạnh số. Đó là đếm thô theo mẫu chữ, chưa đọc từng file.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` | §1, §3, §6 | phạm vi + thứ tự khớp hướng User chọn 01/11; bằng chứng dẫn đúng |
| `session_prompt/CURRENT_HANDOFF.md` | mục "Brainstorm Phase 9", mục "C118" | không tự mở rộng / thu hẹp phạm vi; chỗ lệch đề xuất A đều ghi lý do |
| `report_agent/2026-10-31_streaming_spec/q3a_theo_loai_cau_implementation.md` | §4 | số của H1 (câu nhiều nguồn) dẫn đúng; danh sách "đã thử và bỏ" đủ |
| `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` | §3.1, §3.2 | định nghĩa sàn Golden / bộ an toàn mà §4 dùng lại |
| code `main` (`git show HEAD:<file>`) | `backend/llm/grounded_answer.py`, `backend/llm/full_corpus_prompt.py`, `backend/api/routes/chat.py:35-60`, `backend/config/settings.yaml:48-56` | mọi `file:dòng` khớp code; "mặc định = hành vi hôm nay" làm được |

Bảng có 5 dòng (luật nói 2–4), vì sàn §4 dựa vào plan đo cuối.

**Số dẫn, ngoài căn cứ:**
- sàn tốc độ / tiền: `Project_Status.md` §1;
- mốc câu theo ngày: `report_agent/2026-10-31_streaming_spec/do_cuoi_b_an_toan_ngay.md` §4;
- B119 §2–§3; báo cáo nghiên cứu §4 / §5; nháp C102.

Người review được chạy lệnh chỉ đọc / đếm lại. Thiếu căn cứ ⇒ finding.

## 1. Mục tiêu

Phase 1–8 là "RAG mức 1": hỏi một câu, trả lời đúng, đủ, có nguồn, từ chối câu ngoài kho. Phase 9 thêm những gì một **trợ lý** cần, nhưng **giữ đúng chỗ mạnh** đã đo được so với
Huế TRIPO: nguồn theo từng ý, closed-world, không nói ngược kho ở câu điều kiện (báo cáo nghiên cứu §3). Bảo vệ khoảng 04–10/01/2027 ⇒ **đóng code 20/12/2026** (Chủ nhật).

**Năm dòng khám phá** (`propose-options` §4b), cho cả Phase:
1. **Vấn đề + đo bằng gì:** các lỗi đã thấy ở hệ thống hôm nay, mỗi lỗi một phần (§5):
   - câu theo ngày tương đối bị từ chối;
   - không báo người dùng thông tin giờ / giá / lễ hội có thể đã đổi;
   - câu khẩn cấp chưa có đường riêng (chưa đo);
   - câu thiếu thông tin (lịch trình / chi phí) không được hỏi lại;
   - câu hỏi tiếp không được hiểu;
   - câu nhiều nguồn yếu.
   Đo bằng bộ câu riêng của từng phần + **bộ hồi quy chung** (§4).
2. **Ba ô:**
   - đo được — có (judge Claude + kiểm bằng code, như Phase 8);
   - dữ liệu — chưa có câu thật của du khách ⇒ bộ tự viết, có phần kín;
   - giá trị — **làm được việc mới**, không phải rẻ / nhanh hơn.
3. **Mốc:** chatbot `main` hôm nay (sau merge `a80e12d`). "Không làm" luôn là một phương án.
4. **Tiêu chí bằng số:** sàn chung §4 + tiêu chí riêng ở §5, ghi **trước** khi đo, không đổi sau khi thấy số.
5. **Phương án B:** mỗi phần có "kết quả âm ⇒ …"; cả Phase trễ ⇒ luật cắt §6.

**Có cần "agent" không** (`agent-design-review` §1): **không**.
- Mọi luồng ở đây cố định: nhận loại câu → kiểm trường còn thiếu → tìm → **một** lần gọi model → kiểm cuối. Bước tiếp không phụ thuộc phán đoán của model ⇒ code làm.
- Bằng chứng:
  - agent tổng quát tốn 2,7–3,6× token, không luôn hơn pipeline có mô-đun ("Is Agentic RAG worth it?", báo cáo §1) ⇒ dễ vượt 0,0005 USD / câu;
  - LLM tự nhận câu mơ hồ còn kém (CLAMBER, báo cáo §5).
- Không công cụ cho model gọi, không vòng lặp.

## 2. Quyết định

| Khi | Quyết định | Ai |
|---|---|---|
| 16:01–16:08 01/11/2026 | Hướng B1 = (b): trợ lý di sản đáng tin (H1 nhiều nguồn · H2 hỏi lại bằng danh sách trường trong code · H3 nhớ ngắn 3–5 lượt · H4 theo ngày + chặn câu an toàn trước model) **+ lịch trình gợi ý nhỏ**. Không: agent tổng quát, đặt chỗ, giọng nói / ảnh / nhiều ngôn ngữ | User |
| 16:08 01/11/2026 | Bảo vệ ~04–10/01/2027 ⇒ đóng code ~20/12/2026 | User / A |
| 01/11 (B116) | Giao diện mới React + Vite + Tailwind (B121); nhãn "Trợ lý AI…" (yêu cầu 19) | User |
| giữ từ Phase 8 | tới chữ đầu p50 ≤ 3 s / p95 ≤ 5 s; ≤ 0,0005 USD / câu; thứ tự lỗi: sai cảnh báo / điều kiện vào khu vực > nói chắc sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm | User (`Project_Status.md` §1) |
| **A quyết** (review vòng 2 N5) | **H1 bậc 1 (tầng tìm) chạy tuần 1**, song song giao diện — khác đề xuất ban đầu của A (H1 cuối). Lý do ở §6: 0 USD, tất định, không đổi chatbot, âm thì dư đệm cho L. A báo User một dòng | A |
| 02/11/2026 (A ghi nhận, C ghi vào spec 11:03 02/11/2026) | **Q1 = (a):** "chặn câu an toàn trước model" = câu **khẩn cấp** (mẫu Royal Armouries, báo cáo §4), không phải câu điều kiện của bộ an toàn 32 câu; **thử 10 câu trước** rồi mới quyết code | User (qua A) |
| 02/11/2026 (như trên) | **Q2 = (a):** "ghi theo nguồn ngày…" cho giờ / giá / lễ hội (báo cáo §6 dòng 2) = H4c: **một dòng cố định** "có thể đã thay đổi" khi nguồn được trích thuộc vé / điểm đến / lễ hội, bằng code, không qua model (năm nguồn chỉ có ở 13 / 69 file đích) | User (qua A) |
| 02/11/2026 (như trên) | **Q3 = (a):** câu hai ý mà kho chỉ có một ý (báo cáo §6 dòng cuối) = H1b: **bước 0 đếm trước**, ≥ 3 câu mới làm | User (qua A) |
| 02/11/2026 (như trên) | **Q4 = (a) mặc định, chưa khoá:** chi phí chỉ liệt kê giá có nguồn. Trong H2, **trước khi code phần chi phí**: tra web cách trợ lý du lịch công khai trình bày chi phí (`scripts/tra_web_codex.sh`, 0 USD) + User đọc vài câu mẫu hai cách (liệt kê ↔ cộng tổng ghi phần thiếu) ⇒ User chọn lại | User (qua A) |
| 02/11/2026 (như trên) | **Q5 = (a):** nhớ ngắn = 3 câu hỏi gần nhất + đoạn của 1 lượt gần nhất | User (qua A) |

## 3. Phạm vi

**Trong:**

| Phần | Việc | Ghi chú |
|---|---|---|
| H4a | ngày hôm nay cho câu theo ngày | |
| H4b | câu khẩn cấp | chỉ làm nếu bước 0 cho thấy cần (Q1) |
| H4c | báo thông tin giờ / giá / lễ hội có thể đã đổi | Q2 |
| H2 | hỏi lại cho lịch trình + chi phí | |
| H3 | nhớ ngắn | |
| L | lịch trình gợi ý nhỏ | |
| H1 | câu nhiều nguồn, một thí nghiệm | |
| H1b | câu hai ý thiếu một ý | chỉ nếu bước 0 thấy ≥ 3 câu (Q3) |

Mỗi phần: plan nhỏ có tiêu chí ghi trước ⇒ review ⇒ code nhánh riêng ⇒ đo ⇒ review ⇒ A trình User giữ / gỡ. Phần rất nhỏ (H4a, H4b, H4c): plan ngắn + **một** lượt review nhánh.

**Ngoài:**
- agent / công cụ cho model gọi; tra web lúc chạy;
- đặt chỗ, thanh toán, giờ / giá **chính xác** trong lịch trình;
- bản đồ, chỉ đường, giọng nói, ảnh, nhiều ngôn ngữ;
- tài khoản, lưu lịch sử phía server;
- sửa kho (bảng điểm của L để ở `data/`, §5.6);
- deploy (để sau, rà R1 của C106 lúc đó).

User chọn khác ở Q1–Q3 thì phần tương ứng vào / ra theo lựa chọn đó.

## 4. Chung cho mọi phần

**Mốc chung:** `main` **đầu Phase 9** = commit code của lượt đo cuối 01/11. Code `backend/` chưa đổi từ `a80e12d` ⇒ dùng lại câu trả lời + điểm đã lưu của lượt đó (`Session_Prompt.md` §6).
Khi code đổi so với mốc, phần đó sinh lại mốc trên commit ngay trước phần.

**Bước 0 chung** (tuần 1, 0 USD, không gọi model): ghi **dấu vân tay chuỗi gửi model** trên `main`.
- Là sha của `build_answer_input(query, ngữ cảnh)` cho Golden 176 + bộ an toàn 32 + bộ ngày 15; ngữ cảnh dựng bằng code thật (Qdrant chỉ đọc).
- Mỗi phần so với mốc này cho câu mà luật của phần đó không bắt.

**Sàn — không bao giờ được phạm.** Đo lại ở mỗi phần đổi khâu trả lời, **cộng dồn so với mốc chung**:
- **S-OOS** — 0 câu ngoài kho bị trả lời: Golden 18 câu + bộ an toàn 4 câu. Mốc: 0.
- **S-AT** — bộ an toàn 32 câu, thước + thủ tục plan đo cuối §3.2:
  - 0 đảo cảnh báo / điều kiện vào;
  - **P0_sai mới** (câu nói sai điều kiện mà mốc không sai) ≤ 2, **cộng dồn cả Phase**;
  - 2 câu sai của lượt 01/11 so với mốc cũ `751b352` dao động (sinh lại 3 lần: cả hai bản sai 1 / 3) ⇒ đã nằm trong mốc chung, không tính;
  - gặp ca P0_sai mới ⇒ sinh lại câu đó **3 lần** ở cả biến thể lẫn mốc. Chỉ tính "mới thật" khi biến thể sai ≥ 2 / 3 **và** mốc sai ≤ 1 / 3.
- **S-G** — Golden "không làm hỏng", **dùng lại nguyên thước plan đo cuối §3.1**:
  - **sàn F1–F4:** 0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật; 0 câu lỗi trích dẫn (500) mới; 0 câu "nói chắc sai" mới (Đúng ≤ 3);
  - **mức tụt:** Completeness và Accuracy TB theo cặp ≥ −0,1; số câu tụt ≤ A/A + 3 = **5**; từ chối nhầm ≤ mốc + 1 (≤ 13 / 158);
  - mỗi phần chỉ sinh lại câu Golden mà **luật của phần đó bắt**. Câu khác có chuỗi gửi model giống byte ⇒ dùng lại câu trả lời mốc;
  - **đủ 176 câu** ở hồi quy cuối 20/12.
- **S-T1** — câu luật không bắt ⇒ kết quả tìm **giống byte** T1 `4d5bbe9e0edc` **và** dấu vân tay chuỗi gửi model giống bước 0.
- **S-LAT / S-USD** — như dòng "giữ từ Phase 8" ở §2.

**Chặn rủi ro rẻ nhất:** nhánh mới chỉ bật khi **luật trong code** nhận ra loại câu của nó; câu khác đi đúng đường hôm nay.
- `answer_query` / `prepare_answer` (`backend/llm/grounded_answer.py:44-99`) nhận tham số mới, mặc định = hành vi hôm nay.
- Mỗi luật đếm số câu bắt trên **208 câu** (176 Golden + 32 bộ an toàn) **trước khi code**, 0 USD, ghi kèm danh sách từ / regex.
- Ví dụ 02/11, luật H4a: **1 / 176**, **2 / 32**. Từ: hôm nay · tối nay · sáng nay · chiều nay · ngày mai · cuối tuần · tuần này · tuần sau · tháng này · tháng sau · bây giờ · lúc này ·
  hiện nay · năm nay · đang mở · còn mở (không phân biệt hoa thường, NFC).

**Bộ đo mỗi phần:**
- câu tự viết, kiểu người dùng thật hỏi, có dấu;
- người viết câu **không** là người code phần đó;
- chia **đã thấy** (chỉnh luật) / **kín** (mở một lần lúc xác nhận — `Session_Prompt.md` §5);
- User đọc mẫu 5–10 câu trước khi đo;
- file private `data/phase_9/<phần>/`.

**Chỉ số quyết tính trên tập nào:**
- luật / ngưỡng chỉnh trên phần **đã thấy**, khoá trước khi mở phần **kín**;
- **sàn** phải đạt trên cả hai phần;
- **chỉ số quyết** đạt ngưỡng ghi ở §5 **và** trên phần kín **không ngược chiều** (biến thể không kém mốc). Kín ngược chiều ⇒ "chưa rõ / kém hơn", không chỉnh rồi đo lại.

**Đo:**
- judge Claude cùng lượt mù cho mốc và biến thể; khâu có model có nhiễu A/A (dùng lại A/A sẵn có nếu đầu vào không đổi);
- câu sinh nhiều lượt: chỉ số đếm lấy trung bình theo câu (0 / 0,5 / 1 khi sinh 2 lượt); sàn "0 câu …" phải đúng ở **mọi** lượt;
- cổng ổn định (`CURRENT_HANDOFF.md` "luật chung") cho mọi phần chạm API; đủ 5 chỗ báo cáo (`WORKFLOW.md` §6) khi một phần vào chatbot.

**Luật giữ / gỡ** (`run-experiment` §4), cần đủ ba điều:
1. không phạm sàn;
2. không chỉ số nào tụt quá mức cho phép;
3. chỉ số quyết vượt nhiễu, và kín không ngược chiều.

Không đạt ⇒ **kết quả âm**, giữ hồ sơ tag `hoso/p9-<phần>`. 3 vòng sửa không đạt ⇒ dừng phần đó.

## 5. Từng phần

### 5.1 H4a — ngày hôm nay cho câu theo ngày tương đối

- **Vấn đề (đã đo):** model không biết hôm nay là ngày nào.
  - Đường trả lời không có ngày: prompt `full_corpus_prompt.py:7-20`; `grounded_answer.py` không có dòng nào nhắc ngày. Các dòng `date` khác trong `llm/`, `api/routes/` là `update` / `validate`
    hoặc ở `phase6_live_smoke.py`.
  - Lượt đo cuối 01/11: 12 câu theo ngày, 0 đoán ngày rồi nói sai, **5 câu trong kho bị từ chối nhầm** (`do_cuoi_b_an_toan_ngay.md` §4). Lượt 30/10: 6 / 14 bị từ chối.
  - User 30/10: để Phase 9.
- **Cách nhỏ nhất:**
  - câu có từ chỉ thời gian (§4) ⇒ thêm **một dòng** "Hôm nay: <thứ>, <ngày/tháng/năm> (giờ Việt Nam)" vào tin nhắn user, dựng trong `build_answer_input` (`full_corpus_prompt.py:18-20`);
  - hàm này được gọi ở **hai** chỗ: đếm token (`retrieval/full_corpus_context.py:41`, qua `build_answer_messages`) và gửi đi (`generator_openai_full_corpus.py:252, 261`)
    ⇒ phải truyền **cùng một giá trị** ngày cho cả hai;
  - ngày lấy từ đồng hồ server;
  - câu khác giống byte (S-T1).
- **Âm lịch:** 37 file kho khớp `âm lịch`. Có thêm ngày âm không thì **chốt lúc tới lượt**, theo số câu âm lịch bị từ chối. Lịch âm Việt Nam (UTC+7) có tháng lệch lịch Trung Quốc ⇒ kiểm
  với một nguồn lịch Việt Nam công khai. Thêm thư viện: A tự duyệt (`Session_Prompt.md` §4).
- **Bộ đo:**
  - đã thấy: 12 câu quyết cũ (`data/do_cuoi_2026-11-01/ngay/`) + ~5 câu mới;
  - kín: ~10 câu mới, có câu âm lịch;
  - theo dõi: 11 câu an toàn có giờ / ngày.
- **Tiêu chí:**
  - sàn: 0 câu "đoán ngày rồi nói sai" (thước C93) ở mọi lượt; S-OOS; S-AT; S-T1;
  - chỉ số quyết, trên 12 câu cũ, sinh 2 lượt mỗi bên, mốc sinh lại cùng ngày: từ chối nhầm giảm ≥ **3**; kín không ngược chiều;
  - mức tụt: luật bắt câu không chỉ thời gian ≤ 2 / 208.
- **Tiền:** ≈ **0,04 USD** (~30 câu × 2 lượt × 2 bên + câu khớp luật; 0,00025 USD / câu).
- **Bảo mật:** ngày từ server; chữ người dùng vẫn là dữ liệu (`full_corpus_prompt.py:9-10`).
- **Kết quả âm ⇒** giữ như hôm nay, ghi giới hạn.

### 5.2 H4b — câu khẩn cấp đi đường riêng trước model (theo cách hiểu Q1 (a))

- **Vấn đề: chưa quan sát.**
  - Bộ an toàn 32 câu là câu **điều kiện**: giờ 5, miễn giảm 6, cảnh báo 5, sông nước 4, quy định 4, ngoài kho 4, khác 4. Không có câu khẩn cấp (cháy, trẻ lạc, đuối nước, cấp cứu).
  - Royal Armouries [đã kiểm] chặn loại này trước model.
  - 15 file kho khớp `đường dây nóng|cấp cứu|hotline|115|113`.
- **Vì sao hiểu là câu khẩn cấp:**
  - báo cáo §4 nói "đưa chặn câu an toàn lên sớm … mẫu Royal Armouries", mà mẫu đó chặn câu khẩn cấp;
  - câu điều kiện cần **nội dung kho** để trả lời, nên không chặn trước model được nếu không có bảng điều kiện riêng;
  - cách hiểu khác ⇒ Q1 (c).
- **Bước 0 trước** (tránh phòng xa, `Session_Prompt.md` §7): ~10 câu khẩn cấp tự viết qua chatbot hôm nay (≈ 0,003 USD); User đọc cả 10 câu trả lời.
  - **Thấy lỗi** (từ chối, nói sai số, trả lời dài vô ích) ⇒ luật code nhận câu khẩn cấp, trả **câu soạn sẵn** (số khẩn cấp quốc gia + tìm nhân viên tại điểm), không gọi model.
    **User duyệt nguyên văn**; số lấy từ nguồn nhà nước công khai, không do model viết (`agent-design-review` §2).
  - **Không thấy lỗi** ⇒ ghi "đã thử, không cần".
- **Tiêu chí (nếu làm):**
  - sàn: 0 câu khẩn cấp vào model; 0 câu thường bị chặn nhầm trên 208 (đo hai chiều — `agent-security-review` §6);
  - quyết: User đọc ~5 câu kín cạnh mốc, "dùng được hơn" ≥ 4 / 5.
- **Tiền:** ≈ 0,003 + 0,005 USD. **Bảo mật:** câu soạn sẵn nằm trong code.

### 5.3 H4c — báo người dùng thông tin giờ / giá / lễ hội có thể đã đổi (theo Q2)

- **Vấn đề:** giờ, giá vé, ngày lễ hội đổi theo năm; câu trả lời không cho biết thông tin cũ hay mới. Payload 7 trường không có ngày nguồn; `SourceResponse` = `id, title, heading_path, excerpts` (`chat.py:56-60`).
- **Kho có gì** — đếm trên **đúng ba thư mục đích**, chỉ mục `^## Nguồn dữ liệu` (**không** tính mục "## Nguồn gốc" — đó là lịch sử ra đời, không phải nguồn), `grep_kb.sh --dir <thư mục> -l`:

  | Thư mục | Tổng file | Có `^## Nguồn dữ liệu` |
  |---|---:|---:|
  | `travel/tickets` | 6 | 4 |
  | `travel/places` | 36 | 8 |
  | `festivals` | 27 | 1 |
  | **cộng** | **69** | **13 (19 %)** |

  - Dạng ghi nguồn khác trong `travel/places`: dòng bắt đầu bằng "Nguồn / Tham khảo" (mẫu `^[#*> -]*(nguồn|tham khảo)`, 19 file) đều là nội dung ("nguồn nước", "nguồn nguyên liệu"…). 0 dòng trong số đó có năm `20[0-9]{2}` ⇒ không phải mục nguồn.
  - Người review và A đếm ra cùng số 13 / 69.
- **Cách nhỏ nhất — mặc định = Q2 (a) (C khuyên):**
  - câu trả lời có **nguồn được trích** thuộc `travel/tickets`, `travel/places` hoặc `festivals` (code biết từ đường dẫn file của đoạn, không qua model) ⇒ giao diện hiện **một dòng cố định** dưới câu trả lời:
    "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại với nơi đến trước khi đi.";
  - chữ câu trả lời **không đổi** ⇒ S-G / S-AT không bị chạm; không ghi Qdrant.
- **Vì sao không hiện năm nguồn (Q2 (b)):**
  - ngưỡng ghi trước: hiện năm chỉ khi **≥ 50 % file đích** đọc được năm từ mục "Nguồn dữ liệu";
  - số hôm nay 13 / 69 = 19 % < 50 % ⇒ theo ngưỡng **không làm**;
  - đa số thẻ (gần hết `travel/places`, `festivals`) sẽ trống, và thẻ không có năm dễ bị hiểu là "mới";
  - chỉ đáng làm nếu bổ sung mục "Nguồn dữ liệu" cho kho — đó là sửa kho, việc riêng ngoài Phase 9.
- **Kiểm (0 USD, tất định):**
  - người review nhánh thử 3 câu: nguồn thuộc thư mục đích ⇒ có dòng; nguồn khác ⇒ không; câu từ chối ⇒ không;
  - sàn: 0 dòng hiện ở câu không có nguồn đích.
- **Phụ thuộc:** giao diện mới. **Tiền:** 0 USD, ~nửa ngày.

### 5.4 H2 — hỏi lại khi câu lịch trình / chi phí thiếu thông tin

- **Vấn đề (đã thấy, chưa đo bằng bộ):**
  - thử TRIPO câu 6 + 7: không hệ nào hỏi lại; hue_rag từ chối câu chi phí;
  - B0: User nhận xét câu dự trù chi phí nên được hỏi lại;
  - biểu mẫu TRIPO hỏi thêm bằng nút (B119 §3).
- **Cách nhỏ nhất (code làm, model không quyết):**
  - **danh sách trường cố định trong code**:
    - lịch trình: số ngày · đi cùng ai (người lớn tuổi / trẻ em) · kiểu đi · sở thích;
    - chi phí: số người · số ngày · mức chi 3 bậc;
  - luật chữ nhận loại câu, regex lấy trường đã có. Thiếu trường bắt buộc ⇒ phản hồi `clarify` (trường thiếu + lựa chọn), **không gọi model**; giao diện hiện nút;
  - người dùng chọn xong ⇒ trình duyệt gửi câu gốc + giá trị trường. Server kiểm giá trị thuộc danh sách cho phép (`extra="forbid"` như `ChatRequest`, `chat.py:51-53`);
    code ghép câu đủ ý ⇒ đường thường (hoặc L);
  - server không giữ gì giữa hai lần gọi. Phần server đo được **không cần giao diện**.
- **Chi phí (Q4 = (a) mặc định, chưa khoá):** đủ trường ⇒ trả lời bằng **giá có nguồn** (30 file khớp `giá vé|vé tham quan`), **không** cộng tổng ước tính.
  Lý do: kho thiếu giá lưu trú / ăn uống; TRIPO tự ước "tham khảo thực tế" không nguồn (B119 §2 câu 7).
  - **Bước chọn lại, trước khi code phần chi phí** (~nửa ngày, 0 USD API):
    1. tra web cách trợ lý du lịch công khai trình bày chi phí (`scripts/tra_web_codex.sh`, chỉ thông tin công khai; WebFetch kiểm 2–3 ý);
    2. User đọc vài câu mẫu tự viết theo hai cách: liệt kê giá có nguồn ↔ cộng tổng + ghi rõ phần thiếu;
    3. User chọn lại. Chọn cộng tổng ⇒ plan H2 thêm sàn "0 tổng không ghi phần thiếu".
- **Bộ đo** ~30 câu tự viết:

  | Loại | Đã thấy | Kín |
  |---|---:|---:|
  | thiếu trường (phải hỏi lại) | 10 | 5 |
  | đủ trường (không được hỏi lại) | 7 | 3 |
  | gần giống, không thuộc hai loại | 3 | 2 |

- **Tiêu chí:**
  - sàn: S-T1; hỏi lại nhầm câu đủ trường ≤ 1 / 10; bắt nhầm ≤ 2 / 208;
  - quyết (code đếm, tất định): câu thiếu trường được hỏi lại đúng — đã thấy ≥ **8 / 10**, kín ≥ **4 / 5**;
  - mức tụt — lượt sau khi chọn nút so với mốc (gửi câu gốc như hôm nay), judge cùng lượt mù: Accuracy TB theo cặp ≥ −0,1; 0 câu "nói chắc sai" mới;
  - theo dõi: "dùng được" của lượt sau.
- **Tiền:** ≈ **0,02 USD**.
- **Bảo mật:**
  - giá trị trường từ trình duyệt là dữ liệu không tin cậy ⇒ chỉ nhận giá trị trong danh sách;
  - không trường nào là dữ liệu cá nhân (Luật 91/2025);
  - log thêm số đếm, không chữ (`chat.py:35-40`).
- **Kết quả âm ⇒** giữ từ chối + câu gợi ý cố định "hãy nói số ngày / số người".

### 5.5 H3 — nhớ ngắn trong phiên

- **Vấn đề (đã thấy):** thử TRIPO 6b — hue_rag không nhớ lượt trước. API chỉ nhận `query` (`chat.py:51-53`); lõi tìm bằng đúng câu đó (`grounded_answer.py:51`). Tỉ lệ câu hỏi tiếp thật: chưa có.
- **Cách nhỏ nhất (Q5 = (a), User chọn),** dựa nháp C102 (`docs/superpowers/specs/2026-11-01-multi-turn-design.md`, chưa review, ý cũ xét lại):
  - **trình duyệt giữ** lượt thành công gần nhất: câu hỏi + mã ≤ 3 đoạn đã trích;
  - server đọc lại đoạn từ Qdrant theo mã (chỉ đọc), **không nhận chữ nguồn / chữ câu trả lời cũ** từ trình duyệt;
  - luật chữ nhận câu hỏi tiếp ⇒ mang đoạn cũ vào **cuối** ngữ cảnh. Câu đầu phiên / câu đủ ý đi đường hôm nay.
- **Lệch hướng User (ghi rõ):** User chọn "3–5 lượt".
  - C đề xuất: **3** câu hỏi gần nhất vào tin nhắn, **đoạn** chỉ của lượt gần nhất (ngân sách 16.384 token, `settings.yaml:53`);
  - thêm khi đo thấy lợi (`agent-design-review` §5).
- **Lịch trình hỏi tiếp** ("bố mẹ lớn tuổi, đi chậm hơn"): sửa trường H2 rồi chạy lại L, không dùng H3.
- **Bộ đo:** ~40 chuỗi 2–3 lượt, 5 loại; ~25 đã thấy / ~15 kín. Loại: hỏi lại ý cũ · ý mới cùng chủ thể · hỏi tiếp ngoài kho · hỏi tiếp điều kiện / cảnh báo · đổi chủ đề bằng câu ngắn.
- **Bắt nhầm câu đủ ý:** mỗi câu trong 208 ghép với **một câu trước ngẫu nhiên** (seed ghi trước) từ chính bộ đó, coi như lượt trước thành công; đếm số câu luật nhận là hỏi tiếp (0 USD).
- **Tiêu chí:**
  - sàn: S-T1; hỏi tiếp ngoài kho 0 câu bị trả lời; hỏi tiếp điều kiện 0 đảo cảnh báo; bắt nhầm ≤ 2 / 208; S-LAT; không thêm lần gọi model;
  - quyết: Completeness lượt 2 (loại hỏi lại ý cũ + ý mới) so với mốc "gửi như câu độc lập":
    - gộp đã thấy + kín: CI 95 % > 0, số câu tụt ≤ A/A + 3;
    - kín riêng: TB theo cặp ≥ 0;
  - mức tụt: loại đổi chủ đề tụt ≤ 1 câu.
- **Tiền:** ≈ **0,08 USD**.
- **Bảo mật:**
  - lịch sử từ trình duyệt là dữ liệu sửa được ⇒ chỉ nhận câu hỏi (giới hạn độ dài, tối đa 3) + mã đoạn; chữ câu trả lời cũ không vào prompt;
  - không lưu server; log không chữ;
  - mã đoạn là UUID point, không phải `chunk_id` (đường dẫn file kho).
- **Kết quả âm ⇒** giữ một lượt + nút "hỏi tiếp về nguồn này" chèn tên nguồn vào ô hỏi.

### 5.6 L — lịch trình gợi ý nhỏ

- **Vấn đề:**
  - câu lịch trình hôm nay chỉ ra khung ngắn, không theo trường người dùng (thử TRIPO câu 6);
  - lập lịch đầy đủ bằng LLM rất khó (TravelPlanner: GPT-4 đúng 0,6 %);
  - TRIPO xếp điểm sau giờ đóng cửa của chính dữ liệu mình (B119 §3).
- **Kho có gì** (`--dir travel/places`, 36 file):

  | Trường | Mẫu | Số file |
  |---|---|---:|
  | tọa độ | `tọa độ\|toạ độ` | 24 |
  | giờ mở cửa | `giờ mở cửa\|giờ tham quan\|mở cửa` | 25 |
  | khoảng cách | `[0-9]+([,.][0-9]+)? *km` | 32 |
  | thời lượng | `thời gian tham quan\|nên dành\|mất khoảng` | 16 |

  Thời lượng thiếu ở khoảng nửa số điểm. Mẫu khác ra 10–20 ⇒ con số chỉ là cỡ.
- **Cách nhỏ nhất (code làm, model chỉ viết lời):**
  1. **Bảng điểm** `data/phase_9/lich_trinh/diem.json`:
     - private; không nằm trong `knowledge-base-hue/` ⇒ không nạp index, không đổi Qdrant / T1; ~20–30 dòng;
     - mỗi dòng: điểm · cụm khu vực · thời lượng bậc (ngắn / nửa buổi) · loại hình · file kho nguồn;
     - agent đề xuất, session khác kiểm, **User duyệt** (dữ liệu curated mới, mức cao);
     - thời lượng không có trong kho ⇒ `null`, không tự điền. Khi xếp, `null` tính như "nửa buổi"; lời lịch trình không nêu thời lượng điểm đó.
  2. **Code xếp:**
     - chọn điểm theo sở thích (trường H2);
     - mỗi ngày ≤ 2 cụm; tối đa 4 suất "ngắn" hoặc 2 "nửa buổi"; có người lớn tuổi / trẻ em ⇒ bớt một suất (số cụ thể chốt trong plan);
     - thứ tự trong cụm theo bảng, không tối ưu quãng đường.
  3. Tìm đoạn kho của các điểm đã chọn (≤ 10, `settings.yaml:56`) ⇒ **một** lần gọi model viết lịch có `[n]`.
  4. **Code kiểm cuối:** không giờ / giá chính xác (regex); không điểm ngoài bảng; mọi điểm có citation. Hỏng ⇒ xử như citation hỏng hôm nay.
- **Bộ đo:** ~15 yêu cầu đủ trường + **3 yêu cầu ngoài Huế**; ~10 đã thấy (+ 3 ngoài Huế) / ~5 kín. Mốc = câu đó gửi chatbot hôm nay.
- **Tiêu chí:**
  - sàn (code đếm, cả hai phần): 0 điểm ngoài bảng · 0 giờ / giá chính xác · 0 ngày > 2 cụm · 0 điểm không citation · 3 / 3 yêu cầu ngoài Huế bị từ chối;
  - quyết: User đọc mù **5 cặp lấy từ phần kín** (mốc ↔ L), L thắng ≥ 4 / 5;
  - theo dõi: Accuracy không thấp hơn mốc.
- **Tiền:** ≈ **0,01 USD** (ước lại từ pilot 3 yêu cầu).
- **Bảo mật:** bảng curated, không web lúc chạy, không API ngoài.
- **Phụ thuộc:** cần trường H2. Bảng điểm là dữ liệu ⇒ soạn sớm, song song H2.
- **Kết quả âm ⇒** chỉ giữ H2 + câu trả lời thường.

### 5.7 H1 — câu nhiều nguồn (một thí nghiệm; chỗ cắt đầu tiên)

- **Vấn đề** (đã đo, Q3a §4, số chính 147 câu):
  - 18 câu nhiều nguồn: Completeness 3,50 (một dữ kiện 4,92); MRR 0,510;
  - 8 câu yếu **đều thiếu bằng chứng ở tầng tìm**, 5 / 8 là từ chối nhầm;
  - cả 158 câu: 8 / 12 câu từ chối nhầm là câu nhiều nguồn.
- **Đã thử và bỏ** (không thử lại khi không có lý do mới): pool 100 · luna chọn 10 / 30 · rerank GPU · small-to-big / gộp đoạn · Qwen3-8B · trả lời phần có căn cứ (R2 — phạm S-OOS).
  Câu hai ý thiếu một ý không nằm ở đây — xem H1b.
- **Một biến thể (chốt trong plan):**
  - code tách câu thành 2–3 vế theo luật chữ (liên từ, liệt kê, "so sánh A và B");
  - tìm từng vế, trộn RRF thành 10 đoạn;
  - **không thêm lần gọi model** (gợi ý của ChatGPT — ý kiến, chưa phải bằng chứng);
  - câu không tách được ⇒ đường hôm nay.
- **Bậc 1 — tầng tìm, 0 USD, tất định:**
  - **tập:** Golden nhiều nguồn + so sánh. Chỉnh luật trên dev (20 + 17, `split.json`), xác nhận trên test (9 + 8). Số chính bỏ câu người thật ít hỏi như Q3a;
  - **kiểm giả định trước:** đếm câu tách được; dev < 8 ⇒ "không đủ mẫu", dừng;
  - **thước quyết:** "đủ keyword trong top-10" (Q3a: 12 / 18). Quyết: dev thêm ≥ **3** câu trong nhóm; test không ngược chiều;
  - **sàn trên mọi câu bị bắt** (trong + ngoài nhóm, dev + test, so T1 mốc): 0 câu mất "đủ keyword top-10"; 0 câu mất đoạn đúng (nhãn v5);
  - **mức tụt:** `search_ms` p95 tăng ≤ 150 ms;
  - **theo dõi:** số câu bị bắt ngoài nhóm (người review đo cỡ: 42 / 176 câu có chữ "và"); đủ đoạn đúng (Q3a 8 / 16).
- **Bậc 2 — khâu trả lời** (chỉ khi bậc 1 qua): sinh + judge trên câu đổi ngữ cảnh.
  - quyết: Completeness câu nhiều nguồn gộp dev + test CI 95 % > 0; test không ngược chiều;
  - sàn §4; từ chối nhầm không tăng.
- **Tiền:** bậc 1 = 0; bậc 2 ≈ **0,02 USD**. Cỡ mẫu 18 câu ⇒ chỉ thấy lợi lớn; "chưa rõ" dễ xảy ra — ghi trước, kết quả âm vẫn giữ.
- **Bảo mật:** không đổi bề mặt.

### 5.8 H1b — câu hai ý mà kho chỉ có một ý: bước 0 trước (Q3)

- **Vấn đề: chưa quan sát được.** Lời dặn bắt từ chối **cả câu** khi bằng chứng không đủ (`full_corpus_prompt.py:14-15`).
  Câu thử TRIPO 2 (giờ + giá vé một di tích), đếm thô: tên di tích cùng dòng mẫu giá 36 dòng / 11 file, cùng dòng mẫu giờ 11 dòng / 6 file ⇒ có vẻ đủ cả hai vế ⇒ nhiều khả năng là lỗi tầng tìm (H1).
- **Bước 0 (0 USD, sau H1 bậc 1):** trong câu nhiều nguồn / so sánh của Golden mà luật tách bắt, đếm câu có một vế **không có keyword nào trong kho** (`grep_kb.sh`, chỉ in số).
  - **< 3 câu** ⇒ ghi giới hạn, không làm;
  - **≥ 3 câu** ⇒ mở plan H1b. Ý thiết kế để plan: chỉ câu đã tách vế được phép trả lời vế có bằng chứng + nói rõ vế kia không có trong nguồn — khác R2 (R2 đổi lời dặn mọi câu);
    sàn S-OOS + S-AT; bộ đo chốt lúc đó.
- **Tiền:** bước 0 = 0; nếu mở ≈ 0,01 USD.

## 6. Thứ tự và mốc ngày (tuần từ thứ Hai; A kiểm luật cắt mỗi thứ Hai)

| Tuần | Việc | Mốc kiểm |
|---|---|---|
| 02–08/11 | giao diện mới (B121) · spec review + User duyệt · **bước 0 chung** (0 USD) · **H1 bậc 1** (0 USD, ≤ 1 ngày, không chạm file của B) · bước 0 H1b · bước 0 H4b | spec duyệt; H1 bậc 1 + bước 0 H1b có kết luận |
| 09–15/11 | **H4a rồi H4c** (lần lượt: merge H4a rồi mới mở nhánh H4c) · viết bộ đo H2 / H3 | H4a, H4c giữ / gỡ |
| 16–22/11 | H2 (phần server trước, nút khi giao diện xong; **+ ~nửa ngày** bước chọn lại cách trình bày chi phí — Q4, §5.4) · **soạn bảng điểm L** (dữ liệu, song song được) | H2 giữ / gỡ; bảng gửi User |
| 23–29/11 | H3 · User duyệt bảng điểm | H3 giữ / gỡ |
| 30/11–11/12 | L: code → đo | L giữ / gỡ |
| 14–18/12 | H1 bậc 2 (nếu bậc 1 qua) · H1b (nếu bước 0 ≥ 3 câu, **sau** H1 bậc 2) · hoặc đệm | — |
| 20/12 | **đóng code** | hồi quy cuối: Golden 176 + an toàn 32 + bộ ngày + mỗi bộ kín đã mở, cộng dồn so với mốc chung |
| 21/12–03/01 | luận văn, slide, sửa lỗi nặng (không thêm tính năng) | — |

**Vì sao H1 bậc 1 lên tuần 1** (A quyết, §2): H1 là phần duy nhất có số đo sẵn trên Golden; bậc 1 tốn 0 USD và chạy được khi B làm giao diện.
- Âm sớm ⇒ đóng H1, dư ~1 tuần đệm cho L (phần rủi ro lịch nhất).
- Dương ⇒ bậc 2 có chỗ 14–18/12; luật tách dùng cho bước 0 H1b.
- Thứ tự còn lại giữ như A: H4 rẻ ⇒ trước; H2 trước L vì L cần trường; H3 sau H2 vì cùng sửa luồng giao diện / request.

**Luật cắt** (A kiểm thứ Hai, ghi `CURRENT_HANDOFF.md`):
1. **16/11** giao diện chưa merge ⇒ H2 làm phần server + đo bằng code trước. **23/11** vẫn chưa ⇒ A báo User (H2 nút / H4c / L dời theo).
2. **30/11** H3 chưa đóng ⇒ bỏ H1 bậc 2 và H1b.
3. **30/11** bảng điểm chưa được User duyệt ⇒ L thu về "H2 + câu trả lời thường".
4. **14/12** chỉ H1 bậc 2 / H1b được chạy tới thứ Sáu 18/12; phần khác chưa đóng ⇒ dừng, ghi kết quả dở, không kéo qua 20/12.

**Không song song** hai phần cùng sửa đường trả lời / API / giao diện (`grounded_answer.py`, prompt, `chat.py`, `frontend/`). Hai phần cùng tuần thì **lần lượt**: merge phần trước rồi mới mở nhánh
phần sau. Bộ đo, bảng điểm, plan, bước 0 (chỉ đọc) làm song song được.

## 7. Bảo mật chung (`agent-security-review`)

- **Bộ ba chết người** sau Phase 9:
  - (a) dữ liệu riêng tư: khoá API ở server; không lưu dữ liệu người dùng;
  - (b) nội dung không tin cậy vào ngữ cảnh: chữ người dùng, lịch sử / trường từ trình duyệt (H2, H3), kho lấy từ web;
  - (c) đường ra: chỉ câu trả lời về người dùng + câu hỏi và đoạn kho tới OpenAI (`Project_Status.md` §6). Không công cụ, không link do model tạo được bấm thẳng (DOMPurify + CSP, yêu cầu 1–17).
  - ⇒ **chưa đủ ba**. Thêm công cụ / kênh nào ⇒ rà lại.
- **Chữ người dùng là dữ liệu** (`full_corpus_prompt.py:9-10`). Giới hạn đặt ở API, không ở lời dặn: `extra="forbid"`, độ dài, danh sách giá trị trường, tối đa 3 câu lịch sử, server tự đọc đoạn theo mã.
- **Dữ liệu cá nhân:** không hỏi / lưu tên, số điện thoại, vị trí; log không chữ (`chat.py:35-36`).
- **Giả định an toàn** (cho luận văn): chạy trên máy User, một người dùng, không deploy. Deploy ⇒ rà R1 (kiểm `Host` + giới hạn lượt) của C106 trước.

## 8. Quyền và tiền

- Mỗi phần: plan nhỏ ⇒ session khác review ⇒ A duyệt sha (`WORKFLOW.md` §9.1); nhánh riêng; B / C push nhánh; A merge sau review cả nhánh + cổng ổn định.
- **Tiền ước cả Phase ≈ 0,23 USD:**

  | Phần | USD |
  |---|---:|
  | H4a | 0,04 |
  | H4b | 0,01 |
  | H4c | 0 |
  | H2 | 0,02 |
  | H3 | 0,08 |
  | L | 0,01 |
  | H1 | 0,02 |
  | H1b (nếu mở) | 0,01 |
  | hồi quy cuối | ~0,05 |

  - **Trần mặc định 0,30 USD cho Phase**, trong luật ≤ 1 USD / phiên. A đặt; User chỉ cần nói nếu muốn khác.
  - Lượt vượt ước > 50 % ⇒ dừng, báo A. Judge dùng quota Claude.
- Không ghi Qdrant; không sửa kho / Golden; bảng điểm L ở `data/` (User duyệt). Thư viện nhỏ (vd lịch âm): A tự duyệt, báo User.

## 9. Rủi ro và giới hạn

| Rủi ro | Cách giảm |
|---|---|
| Nhánh mới rò sang câu thường | mặc định tham số = hôm nay; S-T1 (T1 + dấu vân tay); đếm bắt nhầm trên 208 câu trước khi code |
| S-AT: mốc có 2 câu dao động | sinh lại 3 lần (§4); P0_sai mới thật cộng dồn ≤ 2 |
| Bộ đo tự viết, nhỏ ⇒ "chưa rõ" nhiều | ghi trước; User đọc mẫu; phần kín; kết quả âm vẫn là kết quả cho luận văn |
| Giao diện trễ ⇒ H2 / H3 / H4c / L trễ | H4a, H1 bậc 1, phần server H2 không cần giao diện; luật cắt 1 |
| Bảng điểm L sai / thiếu thời lượng | User duyệt; `null` ⇒ xếp như "nửa buổi", không nêu thời lượng |
| Luật tách H1 bắt nhầm nhiều câu | sàn 0 câu mất bằng chứng trên mọi câu bị bắt; số câu bắt ngoài nhóm theo dõi |

**Giới hạn:** không có câu thật của du khách; judge Claude; mỗi bộ chỉ thấy khác biệt lớn; lịch trình không tối ưu quãng đường, không giờ / giá; nhớ ngắn mất khi tải lại trang; H4c chỉ
báo "có thể đã đổi", không cho biết thông tin cũ bao nhiêu.

## 10. Câu hỏi cho User (A hỏi mỗi lần một câu)

**Đã chọn (User qua A, ghi 11:03 02/11/2026):** Q1 (a) · Q2 (a) · Q3 (a) · Q4 (a) mặc định, chưa khoá — chọn lại sau bước tra web + đọc mẫu (§5.4) · Q5 (a). Ghi vào §2.

**Q1 — "Chặn câu an toàn trước model" nghĩa là gì?** — **User chọn (a)**
- **(a) Câu khẩn cấp (cháy, trẻ lạc, đuối nước, cấp cứu), thử 10 câu trước rồi mới quyết (C khuyên).**
  - Tốn ≈ 0,003 USD (~75 đồng); bạn đọc 10 câu trả lời.
  - Không thấy lỗi ⇒ không code.
  - Khi nào sai: 10 câu chưa đại diện; hoặc bạn muốn nói câu điều kiện (c).
- **(b) Câu khẩn cấp, làm luôn như Royal Armouries.**
  - Được: chắc có đường khẩn cấp, ~1 ngày.
  - Mất: thêm luật chưa có lỗi quan sát; phải đo chặn nhầm hai chiều.
- **(c) Cả câu điều kiện / an toàn (giờ, miễn giảm, cảnh báo, sông nước…) trả lời từ bảng điều kiện bạn duyệt, bằng code.**
  - Được: chặn thẳng loại lỗi tệ nhất (bộ an toàn đang có 2 câu dao động).
  - Mất: soạn + duyệt bảng nhiều điểm (~1 tuần, trùng công bảng điểm L); bảng cũ / thiếu ⇒ từ chối nhầm nhiều hơn; phải cắt phần khác (đề xuất cắt H1b + H1 bậc 2).
- *Tự kiểm:* "Vì sao số điện thoại trong câu soạn sẵn phải do bạn duyệt, không để model viết?"

**Q2 — Báo người dùng thông tin giờ / giá / lễ hội có thể đã đổi (H4c) bằng cách nào?** — **User chọn (a)**
- **(a) Một dòng cố định dưới câu trả lời, chỉ khi câu dùng nguồn giờ / giá / lễ hội (C khuyên).**
  - Là gì: code thấy nguồn được trích thuộc thư mục vé / điểm đến / lễ hội ⇒ hiện "… có thể đã thay đổi — hãy kiểm lại với nơi đến".
  - Tốn 0 USD, ~nửa ngày; chữ câu trả lời không đổi.
  - Khi nào sai: người dùng không biết thông tin cũ **bao nhiêu** — chỉ biết "có thể đã đổi".
- **(b) Hiện năm nguồn trên thẻ nguồn.**
  - Mất: chỉ **13 / 69 file đích (19 %)** có mục "Nguồn dữ liệu" ⇒ đa số thẻ trống; thẻ trống dễ bị hiểu là "mới".
  - Ngưỡng ghi trước: < 50 % file đích đọc được năm ⇒ không làm. Số hôm nay không qua ngưỡng.
  - Chỉ đáng nếu bổ sung mục nguồn cho kho (sửa kho, việc riêng ngoài Phase 9).
- **(c) Không làm gì.** Ghi giới hạn trong luận văn.
- *Tự kiểm:* "Vì sao hiện năm trên thẻ cho 13 file mà để trống 56 file còn lại có thể làm người dùng hiểu sai?"

**Q3 — Câu hai ý mà kho chỉ có một ý (H1b): đếm trước rồi mới quyết, hay để ngoài hẳn?** — **User chọn (a)**
- **(a) Bước 0 đếm trước (C khuyên).**
  - Sau H1 bậc 1, đếm câu nhiều nguồn có một vế không có trong kho (0 USD).
  - ≥ 3 câu mới mở plan (~3 ngày, ≈ 0,01 USD, đổi lời dặn chỉ cho câu đã tách vế); < 3 ⇒ ghi giới hạn.
  - Khi nào sai: loại câu này hiếm trong Golden nhưng hay gặp ở người dùng thật ⇒ đếm ra ít mà vẫn có lỗi thật.
- **(b) Để ngoài hẳn.**
  - Được: ít việc nhất.
  - Mất: không biết loại lỗi này lớn cỡ nào; ghi giới hạn.
- *Tự kiểm:* "Câu thử TRIPO 2 bị từ chối — vì sao spec nghĩ đó có lẽ là lỗi tìm (H1) chứ không phải lỗi 'kho thiếu một ý' (H1b)?"

**Q4 — Câu chi phí sau khi hỏi lại: chỉ liệt kê giá có nguồn, hay cộng tổng ước tính?** — **User chọn (a) mặc định, chưa khoá** (chọn lại sau bước §5.4)
- **(a) Chỉ liệt kê giá có nguồn (C khuyên).**
  - Đúng closed-world; kho thiếu giá lưu trú / ăn ⇒ tổng phải đoán.
  - Khi nào sai: bạn muốn demo "dự trù" giống TRIPO.
- **(b) Code cộng tổng từ giá có trong kho + ghi rõ phần thiếu.**
  - Được: giống sản phẩm hơn.
  - Mất: tổng thiếu hạng mục dễ bị hiểu là đủ (lỗi "nói chắc sai").
- *Tự kiểm:* "TRIPO ra 6–13 triệu cho câu chi phí — chỗ nào trong con số đó không có nguồn?"

**Q5 — Nhớ ngắn: 3 câu hỏi gần nhất + đoạn của 1 lượt (C khuyên), hay mang đoạn của 3–5 lượt?** — **User chọn (a)**
- **(a) 3 câu hỏi + đoạn 1 lượt.**
  - Được: ngữ cảnh gần như hôm nay (thêm ≤ 3 đoạn), rẻ.
  - Khi nào sai: câu hỏi tiếp nhắc thứ của 2–3 lượt trước mà câu hỏi cũ không đủ để tìm lại.
- **(b) Đoạn của 3–5 lượt.**
  - Được: nhớ nhiều hơn.
  - Mất: thêm 9–15 đoạn chèn lấn 10 đoạn mới, tốn token, câu đổi chủ đề dễ lệch.
- *Tự kiểm:* "Vì sao server không nhận lại chữ câu trả lời cũ từ trình duyệt?"

**Duyệt:** duyệt sha này ⇒ A giao phần đầu theo §6, trần mặc định 0,30 USD (§8). Phần nào bạn không duyệt ⇒ ra khỏi Phase, ghi lý do.

**Để bạn tự nói lại** (`propose-options` §4c):
- Vấn đề: chatbot đã đúng / có nguồn, nhưng chưa biết ngày, chưa hỏi lại, chưa nhớ lượt trước, chưa lập lịch, yếu câu nhiều nguồn.
- Đã xem: agent tổng quát (bỏ — tốn, khó đo) ↔ pipeline có luật trong code (chọn).
- Mỗi phần chỉ bật khi luật nhận ra loại câu, câu khác đi đường cũ giống byte. Đo bằng bộ tự viết có phần kín + hồi quy chung cộng dồn; giữ khi qua sàn và vượt nhiễu.
- Bạn chọn Q1–Q5.

## Trả lời review

**Vòng 1** (bản 1 `e5be02400646`): 4 major + 8 minor, **đã sửa cả 12, 0 phản biện** (bản 2 `d819918c2f2e`).
- M1: H4c + cách hiểu "câu an toàn"; M2: H1b; M3: mốc chung + cộng dồn + sinh lại 3 lần; M4: tập quyết + kín không ngược chiều.
- m1–m8: căn cứ, mẫu đếm, hai chỗ gọi `build_answer_input`, dấu vân tay, lịch, L, H2 / H3, câu hỏi.
- Chi tiết: bảng vòng 1 trong file review. Số câu hỏi đã đánh lại ở bản 3: Q2 → Q1, Q3 → Q2, Q4 → Q3, Q5 → Q4, Q6 → Q5.

**Vòng 2** (bản 2 `d819918c2f2e`):

| Finding | Xử lý | Chỗ sửa |
|---|---|---|
| N1 — H1b phòng xa mà spec khuyên làm | **đã sửa**: H1b thành **bước 0** như H4b (sau H1 bậc 1, đếm câu có một vế không có trong kho; < 3 ⇒ không làm); bỏ bộ 20 câu + phần kín khỏi lịch mặc định; §5.8 rút còn vài dòng; Q3 khuyên (a) bước 0 | §2, §3, §5.8, §6, §8, §10 Q3 |
| N2 — "130 / 143" không khớp mẫu; chọn năm nào | **đã sửa**: bản 2 đếm qua ống `grep -A15 \| sed` bị lỗi tách tên file. Đếm lại bằng script trên danh sách file của `grep_kb.sh`: 111 (2023–2026) / 123 (20xx) / 143; người review ra 119 / 130 ⇒ ghi cỡ 110–130. Luật: năm **lớn nhất**; file chỉ năm < 2023 vẫn hiện | §5.3 |
| N3 — S-G thiếu sàn F1–F4 | **đã sửa**: liệt kê 4 sàn F1–F4 của plan §3.1, giữ nguyên | §4 S-G |
| N4 — hai tuần chạy song song hai phần cùng sửa đường trả lời | **đã sửa**: H4a rồi H4c **lần lượt**; H1b ra khỏi tuần 30/11 (chỉ ở 14–18/12, sau H1 bậc 2); luật "cùng tuần ⇒ lần lượt, merge trước rồi mở nhánh sau" | §6 |
| N5 — mức công | **đã sửa**: "> 20 câu ⇒ siết" hạ thành theo dõi; H4c đối chiếu 5 file lúc review nhánh; câu hỏi 8 ⇒ 5 (Q1 cũ = **A quyết**, ghi §2; Q7 bỏ; Q8 thành dòng "Duyệt" + trần mặc định) | §2, §5.3, §5.7, §8, §10 |

Giữ nguyên theo ranh giới vòng 2: mọi phần đã đóng ở V2.1, phạm vi Ngoài, số H1, tiền (tổng ≈ 0,23 USD vì H1b chỉ tính khi mở; trần 0,30).
Gọn: 557 ⇒ 507 dòng (bỏ chi tiết H1b, 3 câu hỏi) — không bỏ tiêu chí nào. Chưa tới mục tiêu ~450 vì bản 3 tách nhiều đoạn dài thành gạch đầu dòng cho dễ đọc; số ý thực giảm hơn số dòng.

**Vòng 3** (bản 3 `7c67656f0ff8`):

| Finding | Xử lý | Chỗ sửa |
|---|---|---|
| N2′ — số H4c sai mục (`^## Nguồn` gộp "Nguồn gốc"), đếm cả kho thay vì thư mục đích | **đã sửa**: đếm lại chỉ `^## Nguồn dữ liệu` trên ba thư mục đích ⇒ **13 / 69 (19 %)**, khớp người review + A; dòng "Nguồn / Tham khảo" ở `travel/places` (19 file) kiểm là nội dung, 0 có năm; bỏ câu "năm < 2023 = nguồn cũ" | §5.3 |
| N2′ — Q2 hứa hiện năm trên thẻ | **đã sửa**: ngưỡng ghi trước "< 50 % file đích đọc được năm ⇒ không hiện năm"; số hôm nay không qua ⇒ **C đổi khuyến nghị** sang dòng cố định "có thể đã thay đổi" (code nhận nguồn thuộc thư mục đích, không qua model); hiện năm thành (b), nói rõ độ phủ | §5.3, §10 Q2 |
| sửa kéo theo (cùng nghĩa, để không mâu thuẫn) | §1 dòng vấn đề, §2 dòng "cách hiểu" H4c, §3 bảng phạm vi, §9 giới hạn: đổi chữ "năm nguồn" ⇒ "báo có thể đã đổi" | §1, §2, §3, §9 |

Phần khác không đổi.
