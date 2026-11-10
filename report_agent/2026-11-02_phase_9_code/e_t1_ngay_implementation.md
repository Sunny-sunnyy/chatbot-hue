# Implementation Report: Phase 9 T1 — ngày + âm lịch Việt Nam

Người làm: E (Claude Code, `hue-rag-22`) · Date: 11:44 08/11/2026 · **cập nhật sau review nhánh 12:23 08/11/2026; lượt 3 12:09 08/11/2026; trước đó 12:00 08/11/2026: lượt 2 sau sửa (b) — mục 4b**
- Plan: `docs/superpowers/plans/2026-11-08-phase-9-t1-ngay-plan.md` bản 2 `cdf2c061381a` — mức nhẹ, A duyệt.
- **Đã merge vào `main` (cờ `ngay_lich: false`):** `e401c71` (nhánh `p9-t1-ngay` `f388b19`) + `7ee12f1` (nhánh `p9-t1-ngay-2` `c865159`: bộ dò bỏ số thứ tự / phân số; test stream, song song #6, biểu mẫu — review m-2, m-6).
- **Kết quả lượt 3 (sau 2 sửa A chọn): tiêu chí 1–4 ĐẠT; S1 đạt (lượt 1), S4 sát.** Còn 1 câu kém đi ổn định (R8) + 1 câu đổi qua lại giữa lượt (E2 / E3). S5 NOT RUN. A quyết merge (mục 4c, 6).

## 1. Phạm vi

Công cụ `ngay_lich` cho trợ lý:
- **code** tính hôm nay (giờ Việt Nam) và đổi dương ↔ âm theo lịch âm Việt Nam UTC+7; model chỉ gửi số + loại lịch;
- chỉ đưa khi câu có từ chỉ ngày; kết quả là một nguồn trong sổ nguồn.

Không đổi định tuyến (B làm G), không đổi lời dặn trả lời.

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `pyproject.toml`, `uv.lock` | `lunar-vn==1.4.0` (MIT, 0 phụ thuộc) |
| `backend/llm/ngay_lich.py` (mới) | `hom_nay`, `mo_ta`, `doi`; chỉ nhận năm 1976–2100; ngày không có ⇒ câu cố định; bộ dò `co_tu_ngay` / `co_tu_ngay_luot`; `ket_qua` luôn kèm dòng hôm nay; hằng nguồn |
| `backend/llm/assistant.py` | cờ `ngay_lich` (cần `tim_them`); `ngay_lich_for_turn` (≤ 2 lần / câu, mỗi kết quả là `PackedSource` trong sổ nguồn); `_lich_extra` đưa công cụ khi có từ chỉ ngày; stream không báo "đang tìm kho" cho công cụ này |
| `backend/llm/generator_openai_full_corpus.py` | tham số `ngay_lich_fn`; `max_turns_for`: lượt có đưa công cụ ngày ⇒ **4 + 1** (A chọn sau lượt đo — tham số B2 D5 đổi **có điều kiện**, lý do mục 4); lượt khác giữ 4 |
| `backend/llm/full_corpus_prompt.py` | `NGAY_LICH_MO_TA` (mô tả công cụ) |
| `backend/config/settings.yaml` | `ngay_lich: false` |
| `backend/tests/test_ngay_lich.py` (mới) | 53 test (mục 4, 4d) |

**Thư viện:** A duyệt **11:06 08/11**, trước khi E cài (§4). Lý do:
- nhỏ, MIT, 0 phụ thuộc, lịch Việt Nam UTC+7;
- **không phổ biến** (gói mới, 1 tác giả) ⇒ bù bằng việc E tải wheel từ PyPI, đọc hết ~700 dòng (chỉ thư viện chuẩn: không mạng / file / lệnh), và ghim hash `c42506ee…` (= `uv.lock`).

Cài vào `.venv` chung bằng `uv add --no-sync` + `uv sync --inexact --frozen`; dry-run trước: chỉ thêm 1 gói, `sherpa-onnx` còn.
**Mọi session:** tới khi T1 vào `main`, `uv sync` thường sẽ gỡ `lunar-vn` + `sherpa-onnx` — chỉ dùng `--inexact`.

## 3. Thời gian từng bước (`date`, `Session_Prompt.md` §8)

| Giờ | Bước |
|---|---|
| 10:56–11:00 | tra cứu thư viện (Codex) + WebFetch kiểm 4 nguồn |
| 11:03 | plan bản 1 ⇒ review độc lập `changes_requested` 0 / 5 / 6 |
| 11:06 | A duyệt thư viện; 11:07 cài |
| 11:07–11:20 | đọc mã thư viện, so bảng Tết, module + test, nối công cụ, Q1 cờ tắt |
| 11:21 | plan bản 2; A duyệt (khoảng 11:28) |
| 11:29:31–11:30:56 | 2 server + pilot 5 câu |
| 11:31:46 | A: tối đa 1 server / session ⇒ E tắt server nhánh, dừng vòng chạy (bỏ 3 câu ≈ 0,003 USD), chạy lại lần lượt |
| 11:32–11:35:32 | lượt mốc (server `main`, cờ tắt) |
| 11:36–11:39:11 | lượt nhánh (server worktree, cờ bật tạm) |
| 11:39:53–11:44 | 2 sub-agent chấm mù song song |
| 11:42:33–11:42:49 | sửa `max_turns` (A chọn (b)) + chạy lại R8 |

## 4. Kết quả quan sát

**0 USD:**
- **Đối chiếu ngày:**
  - `lunar-vn` ↔ bảng Tết tính sẵn của Hồ Ngọc Đức (agereckoner, 1901–2099): **khớp mọi năm 1966–2099**, lệch 1 ngày ở 1903 / 1925 / 1935 / 1965 (3 / 4 khớp ở UTC+8 = lịch xưa) ⇒ chỉ nhận 1976–2100;
  - 11 ngày Tết khớp bảng vi.wikipedia "Ngày đầu năm theo Con giáp" (UTC+7, mở 08/11); 2007 thêm Tuổi Trẻ (16/07/2006);
  - 1985 / 2007 ở UTC+8 ra đúng ngày của Trung Quốc;
  - đổi qua đổi lại 1976–2100 (kiểm phụ).
- **Test (đầu nhánh `f388b19`): 53 passed** (`test_ngay_lich.py`) + 3 file liên quan, tổng 151 passed. Gồm:
  - 4c: lượt đầu / lượt có lịch sử / cờ tắt × không stream + stream;
  - câu chỉ trích nguồn ngày qua kiểm citation;
  - ≤ 2 lần gọi;
  - `max_turns` 5 chỉ khi có công cụ.
- **Q1 cờ tắt:** 228 / 228 giống byte `main`.
- **Bộ dò bật:** ngày 27 / 28 (U1 sót có chủ ý), an toàn 4 / 32, Golden mẫu 2 / 30, Golden 176 9 / 176.

**Lượt đo (server thật, `/api/chat/stream`, 1 lượt; an toàn 2 lượt):** 2 sub-agent ngữ cảnh mới chấm mù (thứ tự bên xáo, khoá riêng), **khớp nhau 29 / 29 cặp + 16 / 16 câu an toàn**.

| Tiêu chí (ghi trước) | Kết quả |
|---|---|
| 1. Từ chối nhầm giảm ≥ 3, câu mới chấm OK | **Đạt: 8** (R6, R7, N3, A1, A6, A7, A8, A9). Code đếm: từ chối mốc 9 ⇒ nhánh 1 |
| 2. 0 câu L1 / L3 mới | **Đạt** (0) |
| 3. 0 ngày / thứ sai (L2) trong chữ trả lời | **Trượt 1 câu: A2** (hỏi một lễ hội ngày âm "năm nay đã diễn ra chưa"). Nhánh đổi ngày đúng nhưng mở "Chưa" rồi kết luận "đã qua" ⇒ cả hai người chấm gắn L2. Mốc trả câu từ chối. Bộ kiểm 3 luật bằng code **không bắt được** ca này (lỗi so trước / sau, không phải sai ngày): code 0 / 27 nhánh; mốc có 1 câu sai thứ hôm nay (N2) |
| 4. 0 lượt chạm `max_turns` | Lượt đo: **1** (R8: `ngay_lich` + `tim_kho` × 3 ⇒ hết 4 vòng). A chọn (b) ⇒ lượt có công cụ ngày được 4 + 1. Chạy lại R8: **không chạm trần** (`success`), nhưng **vẫn là câu từ chối** (mốc trả lời OK có điều kiện + hỏi lại) ⇒ R8 kém đi 1 câu |
| 5. S1 (4 câu × 2 lượt × 2 bên) | **Đạt**: 16 / 16 OK cả hai người chấm (0 đảo · 0 sai điều kiện · 0 thiếu cảnh báo · 0 ngoài kho) |
| 6. S4 (2 câu Golden mẫu) | cả hai bên OK; G93: người chấm 1 thấy **mốc rõ hơn** ("Không" ↔ "Không chắc"), người chấm 2 "ngang nhau"; G137 ngang ⇒ **sát**, không tụt nhãn |

**Ngoài tiêu chí:**
- 5 câu (R11, A3, A4, A5, A10, gồm "Hôm nay là ngày bao nhiêu âm lịch?") bị **định tuyến** trả câu ngoài phạm vi ở cả hai bên ⇒ không tới công cụ. Thuộc G (B); đo lại sau khi G vào `main`.
- **S5:** **NOT RUN** — A xếp lượt riêng (B ⇒ E ⇒ C). Số chữ đầu của lượt này không đại diện (máy có việc nặng).
- **S6:** lượt có công cụ ngày trung bình **0,00067 USD / câu** (22 lượt; > 0,0005 — A cho báo riêng). Golden mẫu: 2 câu đổi, cùng mức mốc.

**Tiền thật:**
- nhánh 0,022 USD (log worktree, gồm pilot + R8 chạy lại 0,00225);
- mốc ≤ 0,051 USD — file log ở thư mục chính lẫn dòng của session khác ⇒ cận trên; lần sau đếm theo `turn_id`;
- ⇒ **≤ 0,076 USD** (điểm dừng 0,10), tiền Phase 9.

## 4b. Lượt 2 — sau sửa (b) của A (code ghi "đã qua N ngày / còn N ngày nữa / là hôm nay")

**Sửa:** commit `f536dfe` — `ngay_duong` trả ngày dương; `ket_qua` nối khoảng cách tới hôm nay; test 47 passed.

**Đo:**
- Bộ ngày 27 câu, nhánh × 1 (11:47:10–11:49:39).
- **Mốc dùng lại lượt 1.** Lý do: mốc là `main`, không đổi; chỉ nhánh đổi (chữ kết quả công cụ). Chạy lại mốc chỉ thêm nhiễu và tiền.
- Chấm: 2 sub-agent **mới** chấm mù, cùng brief Phần 1 (khoá `khoa_v2.json`). **Khớp 27 / 27.**

| Tiêu chí | Lượt 1 | **Lượt 2** |
|---|---|---|
| 1. từ chối ⇒ trả lời OK | 8 | **9** (R6, R11, N3, A1, **A2**, A6, A7, A8, A9) |
| 2. L1 / L3 mới | 0 | **0** |
| 3. L2 trong chữ trả lời | 1 (A2 "Chưa … đã qua") | **1 khác: R7** — model **tự viết** "tuần này là giữa tháng 9 âm lịch" trong khi ghi đúng hôm nay là 30/9 âm; kết luận vẫn đúng. Câu này lượt 1 nhánh OK ⇒ lỗi thật + dao động giữa lượt. Code kiểm L2: 0 (không bắt được kiểu mô tả "tuần / tháng âm") |
| 4. chạm `max_turns` | 1 (R8) | **0** |
| trả lời ⇒ từ chối (kém đi) | R8 | **R8, E2** — E2 lượt 1 nhánh vẫn trả lời ⇒ có thể nhiễu 1 lượt |

A2 đã hết lỗi nhờ phép so trước / sau do code làm.

Tiền lượt 2: **0,018178 USD**. Tổng T1 ≤ 0,094 USD (điểm dừng 0,10).

**Kết quả lượt 2: PARTIAL** — tiêu chí 1, 2, 4 đạt; tiêu chí 3 trượt 1 câu (R7, lỗi mô tả lịch âm của tuần do model tự suy, không từ công cụ).

**Hướng nếu A muốn đóng cả R7:**
- (i) công cụ trả luôn ngày âm đầu / cuối của **tuần này** khi câu có "tuần này / tuần sau" (code);
- (ii) mô tả công cụ dặn "không tự suy ngày âm của ngày khác — gọi công cụ" (lời dặn: model có thể không theo).

E đề xuất (i) nếu làm tiếp. Hoặc chấp nhận merge với cờ tắt và ghi giới hạn.

## 4c. Lượt 3 — sau sửa (i) của A (code ghi đầu / cuối "tuần này / tuần sau / tháng này", dương + âm)

**Sửa:** commit `9f08d91` — `khoang_ngay`: tuần tính từ thứ Hai; "tháng này" ⇒ cả tháng dương và tháng âm hiện tại. Chỉ khi câu cuối / câu hỏi liền trước có cụm đó. Test 48 file / 146 liên quan passed.

**Đo:**
- Bộ ngày 27, nhánh × 1 (12:02:31–12:05:03). Mốc dùng lại lượt 1 (lý do như 4b).
- 2 sub-agent mới chấm mù (khoá `khoa_v3.json`), **khớp 27 / 27**.

| Tiêu chí | Lượt 1 | Lượt 2 | **Lượt 3** |
|---|---|---|---|
| 1. từ chối ⇒ trả lời OK | 8 | 9 | **8** (R6, R7, N3, A1, A2, A7, A8, A9) |
| 2. L1 / L3 mới | 0 | 0 | **0** |
| 3. L2 trong chữ trả lời | 1 (A2) | 1 (R7) | **0** |
| 4. chạm `max_turns` | 1 | 0 | **0** |
| trả lời ⇒ từ chối | R8 | R8, E2 | **R8, E3** |

**Đọc kết quả:**
- **R8 kém ổn định cả 3 lượt** ("dịp lễ sắp tới có lễ hội gì"). Biết hôm nay là 08/11, model tìm lễ sau ngày đó, không thấy trong kho ⇒ từ chối. Mốc nói chung chung + hỏi lại (người chấm OK, giáp L1 vì đoán dịp 30/4).
- **E2 / E3 đổi qua lại** ⇒ nhiễu một lượt.
- A6 lượt 3 bị từ chối ở cả hai bên — lượt 1 / 2 nhánh trả lời được ⇒ dao động.
- 5 câu ngoài phạm vi (định tuyến) như cũ.

Tiền lượt 3: **0,018327 USD**. **Tổng T1 ≤ 0,112 USD** (A nâng điểm dừng 0,13).

## 4d. Sau review cả nhánh (sub-agent A, `t1_ngay_branch_review.md`: 0 / 1 / 6)

- **M-1 sửa (`f388b19`).**
  - Lỗi: không nêu năm (`nam = 0`) mà từ 1/1 tới Tết thì "năm nay" âm ≠ năm dương ⇒ "Tết năm nay" thành Tết đã qua ("đã qua 337 ngày" khi hỏi 20/01/2027).
  - A chọn: code trả **cả lần gần nhất đã qua và lần sắp tới**, không đoán; mô tả công cụ sửa theo.
  - Test: 20/01/2027, ngày sau Tết 2027, "rằm tháng Chạp" trong tháng 1.
- **m-1 sửa:** ngày / tháng ngoài khoảng (vd `10**20`) ⇒ câu cố định thay vì `OverflowError` (trước làm hỏng cả lượt); 2 ca test.
- **m-3 đóng bằng lần chạy mới:** Q1 đầu nhánh `f388b19` (cờ tắt) ↔ `main` `6f30404`: **228 / 228 giống byte** (12:22).
  - Ca "cờ bật, câu không từ chỉ ngày": giống theo cấu trúc code (không có `ngay_lich_fn` ⇒ generator gọi như cờ tắt), có test tên công cụ; chưa so byte riêng.
- **Sau sửa M-1 chưa đo lại lượt có phí.** Đổi chỉ ở ca không nêu năm, và lượt đo 08/11 rơi vào tháng 11: năm âm = năm dương ⇒ câu trả lời bộ ngày không đổi theo cấu trúc. Lượt xác nhận trước khi bật nên có câu hỏi trong khoảng 1/1 – Tết (giờ giả không dùng được cho server — cần câu mới hoặc đợi đúng mùa) ⇒ ghi điều kiện bật.
- **m-2, m-5, m-6 (phiên sau, `STATUS_E.md`):**
  - m-2: bộ dò bắt nhầm "thứ hai / thứ ba" chỉ thứ tự và phân số "1/2", "24/7";
  - m-5: "đạt" là trên **chính bộ đã dùng để chỉnh** qua 3 lượt (sửa đều là phép tính tất định, không phải lời dặn riêng từng câu) ⇒ trước khi bật cần S5 + một lượt xác nhận trên vài câu ngày mới;
  - m-6: thiếu test stream có gọi `ngay_lich` thật và test đường song song; **"tháng tới / tháng sau / cuối tuần" vẫn do model tự cộng** (chỉ "tuần này / tuần sau / tháng này" do code ghi) — giới hạn.

## 4e. Lượt xác nhận trên câu ngày MỚI (09/11, review m-5) — ghi 20:27 09/11/2026

- **Cách làm:** tiêu chí ghi trước (`data/phase_9/t1/xac_nhan/tieu_chi.md`, 20:18) ⇒ 14 câu mới E viết 09/11, chưa dùng để chỉnh (`bo_xac_nhan.jsonl` `9d95dc64a455`):
  Tết có năm / không năm / "năm nay", rằm sắp tới, rằm tháng này, ngày mai âm, Chủ nhật này âm, 5 lễ có ngày âm trong kho (khác bộ cũ), 1 điểm đóng cửa theo thứ, 1 câu ngoài kho.
  `main` cờ tắt ↔ `main` cờ bật tạm (worktree, đã gỡ), `/api/chat/stream` thật, 1 lượt mỗi bên, một server một lúc. Code `main` `5c982a0`, không sửa giữa chừng.
- **Chấm:** 2 sub-agent ngữ cảnh mới, chấm mù cặp, **khớp 14 / 14**; `kiem_l2.py` 0 đánh dấu cả hai bên.

| Tiêu chí (ghi trước) | Kết quả | |
|---|---|---|
| 1. Từ chối nhầm giảm ≥ 3 | **9** câu từ chối ⇒ OK | đạt |
| 2. 0 câu L1 / L3 mới | **1 L1** (câu "Tết năm nay") | **trượt** |
| 3. 0 L2 (ngày / thứ / âm ↔ dương sai) | 0 (máy + 2 người tự đổi lịch) | đạt |
| 4. 0 lượt chạm `max_turns` | 0 | đạt |
| 5. Ca M-1 (2 câu không nêu năm) đều OK | "còn bao nhiêu ngày tới Tết" OK; "Tết năm nay" **L1** | **trượt** |

- **Câu trượt:** hỏi tháng 11 "Tết năm nay rơi vào ngày nào?". Code trả đủ cả hai lần (Tết đã qua + Tết sắp tới). Model chọn Tết sắp tới, ngày và năm đúng
  (có ghi năm, năm can chi), nhưng gọi nó là "năm nay" và không nhắc Tết năm âm hiện tại đã qua. Nhãn ghi trước xếp ca này vào L1 ⇒ giữ đúng nhãn. Đây là câu
  mơ hồ thật (tháng 11 nhiều người nói "Tết năm nay" để chỉ Tết sắp tới), nhưng **không đổi tiêu chí sau khi đã thấy kết quả**.
- **Ca biên người chấm 2 nêu (vẫn OK):** câu "ngày hội cuối năm âm, năm nay khi nào / còn bao lâu" — model lấy kỳ trong kho (đầu năm dương) rồi nói "đã kết thúc",
  không nhắc kỳ sắp tới theo năm âm. Cùng gốc với câu trượt: **model tự chọn "năm nay" theo năm nào**.
- **Định tuyến xếp ngoài phạm vi 3 câu ở cả hai bên** (Tết có năm, ngày mai âm, Chủ nhật này âm) — cùng loại lỗi G sửa; mốc thêm 2 câu (dao động) ⇒ tính trong 9 câu R của mốc.
- **Chữ đầu (dùng thay S5, A chốt 09/11):** nhánh p50 **3,35 s** / p95 **6,33 s** ↔ mốc p50 **4,90 s** / p95 **7,87 s** (n = 14 mỗi bên, `chat_metrics.first_text_ms`
  theo `turn_id`, `tools/doc_metrics.py`). Nhánh không chậm hơn mốc. p95 vượt sàn 5 s ở **cả hai** bên vì có câu đi qua tra web / nhiều vòng — không do T1.
- **Tiền thật:** nhánh 0,008295 + mốc 0,017327 = **0,025622 USD** (mốc đắt hơn: từ chối rồi tra web). Chấm: sub-agent (không gọi API trả phí).
- **Bắt thêm:** bộ dò không bắt "sang năm …" ⇒ nhánh `p9-t1-sang-nam` `d3e7d02` (thêm "sang năm", trừ khi theo sau là số năm; 1 dòng regex + 2 ca test;
  `test_ngay_lich.py` 71 passed; số câu bộ dò bật trên Golden 176 / an toàn 32 / Golden mẫu 30 không đổi: 9 / 4 / 2). Cờ vẫn tắt.
- **Giới hạn:** khoảng 1/1 – Tết vẫn chỉ có test giờ giả (không chạy thật được trong tháng 10 âm). n = 14, 1 lượt ⇒ chưa tách nhiễu.
- **A chọn (b) — sửa bằng code (`p9-t1-sang-nam` `ff65510`):** ngày âm mà câu hỏi nói "năm nay" hoặc không nêu năm ⇒ kết quả công cụ có cả lần gần nhất
  (đã qua) và lần sắp tới, cộng một dòng ghi chú do code viết ("ghi rõ năm từng ngày; lần đã qua nói là đã qua"); mô tả tham số `nam` trong công cụ sửa cho khớp
  ("0 = người dùng không nêu năm" — trước ghi "0 = năm nay", ngược với mô tả chung); log công cụ ghi thêm năm model gửi (chỉ số). Test: `test_ngay_lich.py`
  72 passed; `backend/tests` 824 passed (hỏng đúng 4 test cần khoá + 3 test giao diện thiếu bản build ở worktree — đạt trên thư mục chính). Cờ vẫn tắt.
  **Chưa đo có phí** — đo ở lượt sau G (tiêu chí ghi trước `tieu_chi.md` mục 2: 3 câu mới cùng loại, L1 = 0; thêm an toàn 4 câu × 2 lượt + 1 câu ngoài kho).

## 4f. Lượt sau G (nền phương án B) — sửa "năm nay" / "sang năm" (ghi 21:35 09/11/2026)

- **Nền:** `main` `3b52017` (G phương án B: giữ định tuyến 4 tuyến) + `p9-t1-sang-nam` rebase **`7db1fb6`** (cờ bật tạm ở worktree); mốc = `main` cờ tắt. 14 câu `bo_sau_g.jsonl` + an toàn 4 câu ×1 mỗi bên (A chốt vòng tự soi, ghi trước ở `tieu_chi.md` mục 2b); 1 người chấm mù + `kiem_l2.py`.
- **Kết quả (người chấm mù, mở khoá sau):**

| Tiêu chí (`tieu_chi.md` mục 2) | Kết quả | |
|---|---|---|
| 1. L1 = 0 ở loại "năm nay / không nêu năm" | L1 **0**. "Tết năm nay" (câu trượt hôm trước) ⇒ **OK**: nêu Tết năm âm hiện tại kèm năm + "đã qua" (mốc: từ chối). Câu lễ "năm nay" mới ⇒ OK ở cả hai. 2 câu lịch thuần ⇒ định tuyến chặn (xem 3) | đạt (phần tới được agent) |
| 2. L2 0 · L3 mới 0 · `max_turns` 0 | 0 · 0 · 0 (`kiem_l2` 0 đánh dấu cả hai bên) | đạt |
| 3. 8 câu bị định tuyến chặn hết bị chặn | **Không áp dụng — nền đổi** (A 09/11): tiêu chí viết khi nền là G 2 nhóm; nền thật là phương án B (lời dặn định tuyến = `main`) ⇒ câu lịch thuần không nhắc Huế vẫn "ngoài phạm vi" ở **cả hai bên** (mốc 9 / 14, nhánh 10 / 14). Ghi là **giới hạn**: đúng phạm vi sản phẩm du lịch Huế | n/a |
| 4. "sang năm" có gọi công cụ + OK | gọi `ngay_lich` (âm, năm sau) ⇒ **OK** (mốc: từ chối) | đạt |
| 5. An toàn 4 số + ngoài kho 0 | 4 câu: đảo cảnh báo 0 · sai điều kiện 0 · thiếu cảnh báo 0 · ngoài kho bị trả lời 0 (cả hai bên OK 4 / 4); câu ngoài kho X14 ⇒ từ chối cả hai | đạt |

- **Tổng:** 3 câu ngày có ngữ cảnh Huế (Tết năm nay · lễ năm nay · "sang năm") nhánh OK 3 / 3 ↔ mốc OK 1 / 3. Một câu "còn mấy ngày tới rằm tháng Giêng" ra "ngoài phạm vi" ở nhánh nhưng tới agent ở mốc (định tuyến dao động — cùng giới hạn mục 3).
- **Tiền thật** (`chat_metrics.usd` theo `turn_id`): nhánh 0,007739 + mốc 0,011654 = **0,019393 USD**. Chữ đầu (n nhỏ, chỉ ghi): nhánh p50 2,88 s ↔ mốc 3,05 s.
- **Kết luận:** đạt các tiêu chí còn áp dụng ⇒ A merge cờ tắt, trình User bật. Giới hạn ghi khi bật: câu lịch thuần (không nhắc Huế) do định tuyến coi là ngoài phạm vi; "tháng tới / cuối tuần" model tự cộng; năm 1976–2100.

## 5. Lỗi và giới hạn

- **R8 — A chấp nhận (08/11) đổi lấy 8 câu cứu được.** Câu "dịp lễ sắp tới" kém ổn định cả 3 lượt. Nguyên nhân: kho thiếu lịch lễ hội "sắp tới" theo ngày; khi model biết hôm nay là 08/11, nó tìm lễ sau ngày đó, không thấy ⇒ từ chối. Bản cũ trả lời chung chung (đoán dịp 30/4) + hỏi lại. Sửa thật cần dữ liệu lịch sự kiện theo ngày (đợt 2 cổng), không phải code công cụ.

- **A2:** đã sửa ở `f536dfe` (code ghi "đã qua / còn N ngày") — lượt 2 / 3 không còn lỗi.
- Bộ kiểm L2 bằng code chỉ bắt sai ngày / thứ, không bắt sai lập luận trước / sau ⇒ người chấm bắt.
- Đáp án ngày dùng cùng thư viện (vòng tròn) — đã qua bộ đối chiếu ở trên.
- Một lượt (mức nhẹ) ⇒ câu chỉ đổi do nhiễu chưa tách được ở bộ ngày.
- Lượt mốc dở 3 câu bị bỏ (`ngay_moc_dung_giua_bo.jsonl`) do đổi luật 1 server giữa chừng.

## 6. Bàn giao

- **Trạng thái:**
  - A chọn (b) rồi (i), lượt 3 đạt tiêu chí 1–4;
  - R8 A chấp nhận;
  - review nhánh `changes_requested` 0 / 1 / 6 ⇒ M-1 + m-1 sửa ở `f388b19`; m-2 / m-5 / m-6 phiên sau.
- **Trước khi bật cờ (cập nhật 09/11):**
  - ~~S5 riêng~~ — A chốt 09/11: dùng số chữ đầu của lượt xác nhận (mục 4e);
  - lượt xác nhận: **chạy 09/11, trượt 1 câu** ("Tết năm nay" — mục 4e) ⇒ chờ A quyết;
  - G vào `main` ⇒ MỘT lượt nhỏ: 5 câu cũ bị định tuyến xếp ngoài phạm vi + 3 câu của mục 4e + câu "sang năm" (nhánh `p9-t1-sang-nam`).
- **Dữ liệu (private):** kết quả `data/phase_9/t1/ket_qua/`, chấm `data/phase_9/t1/cham/` (brief ghi trước 11:32, khoá, 2 phiếu), công cụ `data/phase_9/t1/tools/`.
- **Chạy lại:**
  - server + `chay_t1.py <BASE> <ngay|an_toan|golden|chon:Rx> <moc|nhanh> <luot> <out>`;
  - `kiem_l2.py`, `dung_cap_mu.py`;
  - 0 USD: `so_tet.py`, `dem_bo_do.py`.
- **Chữ đầu:** `chay_t1.py` ghi `turn_id` (từ 09/11) ⇒ `doc_metrics.py <application.log> <ket_qua.jsonl>`; bộ xác nhận: `chay_t1.py <BASE> xac_nhan …`, `dung_cap_mu.py xac_nhan`.
- **Review cả nhánh:** `git diff main...p9-t1-ngay`.


## Đoạn cho `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md` (A dán lúc đóng đợt)

**Ngày và âm lịch (T1, 08/11/2026) — code xong, cờ `ngay_lich` đang tắt.**
- Trợ lý có thêm một công cụ để biết hôm nay là ngày nào và đổi ngày dương ↔ âm theo lịch âm Việt Nam (giờ UTC+7, không phải lịch Trung Quốc).
- Mọi phép tính đều do code làm: đổi ngày, so "đã qua / còn N ngày nữa", khoảng "tuần này / tháng này". Model chỉ gửi số rồi viết lời. Công cụ chỉ có mặt khi câu hỏi có từ chỉ ngày.
- Đo trên 27 câu có ngày (2 người chấm mù, khớp nhau): bớt 8 câu từ chối nhầm, 0 câu nói sai ngày / thứ, 0 câu sai so với kho; bộ an toàn không đổi.
- Giới hạn:
  - câu "dịp lễ sắp tới có gì" giờ bị từ chối, vì kho chưa có lịch sự kiện theo ngày;
  - câu thuần về ngày ("hôm nay ngày bao nhiêu âm") vẫn bị định tuyến coi là ngoài phạm vi, chờ việc định tuyến mới;
  - chỉ đổi ngày từ năm 1976 tới 2100.
- Lượt xác nhận 09/11 trên 14 câu mới: bớt 9 câu từ chối nhầm, 0 sai ngày; 1 câu mơ hồ "Tết năm nay" bị chấm là nói sai thời điểm (chờ quyết).
- Chữ đầu (09/11, 14 câu): bản có công cụ p50 3,35 s ↔ bản cũ 4,90 s — không chậm hơn.
- Tiền đo ≈ 0,14 USD.
