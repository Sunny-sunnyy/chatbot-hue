# Review: T1 nhanh — câu ngày, lịch code tính sẵn (nhánh `p9-t1-nhanh` `7d6f25f`)

Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-4f`) · 10/11/2026 · A giao (một vòng cả nhánh, chỉ chỗ rủi ro theo chốt tự soi 1). Plan
`docs/superpowers/plans/2026-11-10-phase-9-t1-nhanh-plan.md` `935f9358e25d` (sha khớp trên nhánh). Report `e_t1_nhanh_implementation.md` (E, trên nhánh).
Dữ liệu private `data/phase_9/t1_nhanh/`. Repo public: không chép câu; ví dụ dưới là câu **C tự viết**.

## 1. Phạm vi đã review

- `git diff 624a17b..7d6f25f -- backend`: `llm/ngay_lich.py` (+108: `lich_san`, regex dò ngày âm, `_hai_lan` thêm nhãn), `llm/assistant.py` (+22: `_nguon_lich_san`, chỗ gắn
  trong `_before_model`), `llm/full_corpus_prompt.py` (mô tả công cụ `ngay_lich`), `tests/test_ngay_lich.py` (+4 test). Không chạm `answer_turn_stream_parallel` / `AssistantFlags` (vùng của B).
- Chỗ rủi ro (E + chốt tự soi): (1) regex dò ngày âm, trần 6 · (2) không chen nguồn lịch khi lượt đã từ chối sẵn · (3) Q1 215 / 228 giống byte, 13 khác = đúng ca bộ dò bật ·
  (4) sửa "năm nay / năm sau" `b8a96d8` · D1 chỉ gồm dạng có trong bộ đo.

## 2. Findings

**Blocker:** không.

**M-1 (major) · câu hỏi "mùng / mồng N tháng X" với **tháng viết bằng số, không có chữ "âm"** bị coi là ngày âm** — `ngay_lich.py` `_AM_TIEN_TO` (áp cho cả câu hỏi
và tài liệu) + `_THANG` nhận `\d{1,2}`.
- Bằng chứng [Chạy, 0 USD]: câu tự viết "Mùng 2 tháng 9 năm nay ở Huế có bắn pháo hoa không?" (ngày Quốc khánh — **dương lịch**) ⇒ `co_tu_ngay_luot` = True ⇒ `lich_san`
  dựng nguồn "Lịch hệ thống" gồm "Ngày được hỏi — năm âm lịch nay (…, âm lịch 2/9/2026): Chủ nhật, 11/10/2026 dương lịch …" + lần gần nhất / sắp tới theo âm lịch.
  Cách nói "mùng 2 tháng 9", "mùng 8 tháng 3", "mồng 1 tháng 5" cho ngày lễ dương lịch là cách người Việt hay gõ.
- Tác động: nguồn hệ thống **khẳng định** một cách hiểu âm lịch cho câu hỏi về ngày dương ⇒ model dễ "nói chắc sai" (lỗi thứ 2 theo thứ tự User 28/10). Trên `main`
  model tự gọi công cụ và tự chọn `loai` (có thể chọn dương). [Chưa chạy model — chỉ chứng minh dòng sai nằm trong nguồn gửi model.]
- Ngoài bộ đo: bộ 19 câu, 9 câu Golden, 4 câu an toàn, cả Golden 176 có **0** câu dạng này (đếm bằng regex) ⇒ sửa **không đổi** số đo nào đã có, Q1 không đổi
  (bộ dò `co_tu_ngay_luot` không chạm). Theo chốt tự soi "D1 chỉ dạng có trong bộ đo", dạng tháng-số-không-"âm" ở câu hỏi cũng không thuộc phạm vi.
- Phía tài liệu ít rủi ro hơn: đếm trong kho (`scripts/grep_kb.sh`, chỉ đếm mẫu) — "mùng / mồng N tháng <chữ>" (Giêng, Chạp, Tư, Tám…) ~44 lần, đều kiểu âm lịch;
  tháng số có "Âm" theo sau 7 lần; tháng số **không** "âm" 2 lần, cả hai là ngày lịch sử kèm năm niên hiệu / can chi (không phải ngày dương) ⇒ chỉ thêm dòng thừa.
- **Đóng:** với tháng viết bằng số, chỉ nhận khi có "âm" theo sau (áp cho câu hỏi; tài liệu giữ hoặc áp luôn — E chọn); dạng tháng bằng chữ giữ nguyên. Một test cho câu
  "mùng 2 tháng 9" ⇒ không có dòng ngày âm (model vẫn gọi được công cụ). Chạy lại test file chạm; không cần lượt có phí (0 câu đo bị ảnh hưởng).

**Minor:**
- **m-1 · ngày lịch sử trong tài liệu thành "lần sắp tới"** — đoạn kho kể sự kiện một lần (ngày âm + năm niên hiệu) vẫn được đổi thành lần gần nhất / sắp tới. Dòng thừa,
  nhãn "Ngày âm trong tài liệu" không nói là ngày lặp lại; report §5 đã ghi giới hạn "tới 6 ngày âm không liên quan". Chưa thấy câu sai. Không sửa.
- **m-2 · tháng / ngày không hợp lệ** (vd "ngày 13 tháng 13 âm") ⇒ dòng "Ngày này không có trong lịch." — không lỗi, không đổi ngày sai. Không sửa.
- **m-3 · không có test riêng cho "lượt đã từ chối sẵn"** — guard `trace.fixed_outcome is None` (`assistant.py` `_before_model`) đọc đúng; và lượt có `fixed_outcome` không
  gọi model (`answer_turn_stream` trả câu từ chối ngay sau `_before_model`) ⇒ nguồn lịch có chen cũng không tới model. Chấp nhận không test.

**Khớp (không finding):**
- Regex: "tháng năm nay" không thành tháng Năm (lookahead trong `_THANG`); "Tết Trung thu / Đoan ngọ / …" không thành 1/1 (probe: 0 ngày âm); "mùng 3 Tết năm sau" ⇒ 3/1 năm
  âm sau đúng; trần 6 ngày âm + bỏ trùng; mẫu kho đòi "âm" theo sau với `_AM_HAU_TO` / `_AM_SO`.
- `_before_model`: chỉ khi `ngay_lich` + chưa từ chối sẵn + `co_tu_ngay_luot(query, history)` ⇒ một nguồn, id kế tiếp, nối sau ngữ cảnh; log `tools` chỉ số đếm. Phủ cả `/api/chat`,
  stream, đường song song #6 (cùng `_before_model`); lượt biểu mẫu không đi qua chỗ này.
- Mô tả `NGAY_LICH_MO_TA` đổi ⇒ chỉ ảnh hưởng lượt có công cụ ngày (đã là lượt có từ chỉ ngày) — khớp Q1.
- Sửa (a) `b8a96d8`: "năm nay / năm sau / năm tới / sang năm" ⇒ dòng ngày của đúng năm âm đó, trước các dòng lần gần nhất / sắp tới.

## 3. Cách người kiểm chạy lại thật

| Lệnh (0 USD) | Kết quả |
|---|---|
| `cd /tmp/e_t1_nhanh/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_ngay_lich.py -q` | **82 passed** (16,5 s) |
| so `data/phase_9/t1_nhanh/q1_main.jsonl` ↔ `q1_nhanh.jsonl` theo (case, path) | **215 giống / 13 khác**; 13 khác = `g25 g26 g85 g90 g92 g93 g96 g114 g137` + `atS01 atS02 atS03 atS12` |
| `co_tu_ngay_luot` trên Golden 176 + an toàn 32 (đánh số từ 0) | bật đúng 9 + 4 ca trên ⇒ **13 khác = đúng ca bộ dò bật** |
| `lich_san` trên 6 cặp câu / đoạn C tự viết (`now` cố định 10/11/2026) | như §2 (M-1, m-1, m-2, các ca khớp) |
| `scripts/grep_kb.sh -o` đếm mẫu ngày âm trong kho | như §2 M-1 (chỉ đếm mẫu, không chép câu) |

Không chạy lại: lượt tốc độ (A chốt; B đang build Docker), lượt có phí, chấm mù, test rộng (E: 850 đạt + lỗi đã biết).

## 4. Kết quả quan sát

- Nhãn report trung thực: lượt chính **tụt 1 câu** (Y2) được ghi, dừng, báo A, sửa (a) rồi đo lại 8 câu — ghi rõ lượt lại chạy cùng lúc việc khác nên **không dùng cho tốc độ**;
  X3 / Y1 ghi là dao động định tuyến (lý do: chuỗi gửi định tuyến giống byte — C xác nhận ở Q1). 9 / 19 câu đi ngoài phạm vi ghi rõ là ngoài phần đổi.
- Số tốc độ / tiền: trích từ `chat_metrics`; C không đo lại.

## 5. Giới hạn hoặc phần chưa chạy

M-1 chưa chạy qua model (nhận định theo nguồn gửi model). Dạng ngày ngoài bộ đo (report §5) không đo.

## 6. Decision và bước tiếp theo

**`changes_requested`** — 0 blocker, **1 major (M-1)**, 3 minor (không sửa). M-1 sửa nhỏ (regex + 1 test, 0 USD, không đổi số đo nào đã có) ⇒ E sửa, chạy lại test file chạm ⇒ C xem
delta (chỉ phần sửa) ⇒ `ready`. Tiêu chí ghi trước 1–6: theo report + kiểm của C (Q1) — **đạt** sau lượt lại.
