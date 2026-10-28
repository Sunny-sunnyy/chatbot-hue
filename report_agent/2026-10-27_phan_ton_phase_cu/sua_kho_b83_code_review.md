# Review: B83 phần code — `GOLD_PATH` ⇒ v4 + `truoc_sau.py` phần "sau"

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 3 minor) — không lỗi nào chặn việc chấm judge
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`)
Date: 11:52 28/10/2026 (`date`)
Canonical guide: plan `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_do_truoc_sau_plan.md` (A duyệt sha `41485782b39e`) §2–§4, §7; review C72 m-1 … m-3
Bản được kiểm: `backend/experiments/phase_8_1/g1_retrieval.py` (working tree, chưa commit); `data/sua_kho_2026-10-27/tools/truoc_sau.py` sha `e3a036c8e149` (500 dòng, private)

## 1. Phạm vi đã review

- `git diff -- backend/experiments/phase_8_1/g1_retrieval.py`; sha các bản nhãn đoạn đúng; nơi khác dùng `GOLD_PATH`.
- `truoc_sau.py` đọc **hết** (không chỉ phần mới). Đối chiếu từng lệnh với plan §2, và từng dòng tiêu chí F1–F4 / T1–T3 / W1–W8 với plan §4.
- Chạy khô `touched` + `gold_in_context` (W6) **trong bộ nhớ** trên 120 câu "sau" đã có (`sau_pilot` + `sau_rest`, lượt đang chạy). Không ghi file nào của B:
  - đầu ra để ở `/tmp`, đã xóa;
  - `analyze` / `scored` / `rejudge` không chạy được vì chưa có điểm judge ⇒ chỉ đọc code.

## 2. Findings

Không có blocker hay major.

**m-1 — Nhãn câu tụt "tìm đổi đoạn / nhiễu" so danh sách đoạn **có thứ tự**, plan định nghĩa theo **tập**.**
- Vị trí: `truoc_sau.py:410-413` (`why`: `context(t[i]) != context(s[i])`).
- Plan §4: "**tìm đổi đoạn** (tập (nguồn, `evidence_parts`) của context hai bên khác nhau) · **nhiễu** (context hai bên giống nhau)".
- Bằng chứng (chạy khô, 90 câu số chính đã có): trong số câu không chạm, **6** câu khác context **theo thứ tự**, chỉ **1** câu khác **theo tập**. Tức 5 câu chỉ đổi thứ tự đoạn
  (như case IDF ở C75) sẽ mang nhãn "tìm đổi đoạn" theo code nhưng "nhiễu" theo plan.
- Tác động nhỏ: C đọc cả hai nhãn (plan §7), nên không câu nào lọt khỏi việc đọc. Nhưng số đếm theo nhãn trong report sẽ lệch định nghĩa đã ghi trước.
- Tiêu chí đóng (chọn một, **trước** khi chạy `analyze`):
  - (a) theo đúng plan: so `set` của chunk id. Nếu thêm một nhãn thứ ba "chỉ đổi thứ tự" thì thêm dưới dạng thông tin, không đổi định nghĩa "nhiễu".
  - (b) giữ so có thứ tự, ghi rõ trong report là lệch plan và vì sao. Lý do có thể là: đổi thứ tự cũng đổi đầu vào model và đổi số `[n]`.
  - C nghiêng (a) + nhãn "chỉ đổi thứ tự": đúng định nghĩa đã duyệt, mà không mất thông tin.

**m-2 — `rerun-f4` chưa ghi "nhãn context giống / khác lần đầu" (plan §2).**
- Vị trí: `truoc_sau.py:477-478` (chỉ gọi `run("sau", …, "f4_rerun")`).
- Tác động: chỉ dùng khi F4 vỡ, để làm bằng chứng trình User. Thiếu nhãn thì người đọc phải tự so.
- Tiêu chí đóng: sau `run`, in thêm `top_chunk_ids[:context_sources]` của lần chạy lại có giống `sau.jsonl` không (chỉ đúng / sai cho mỗi câu). Hoặc report ghi rõ C so bằng tay.

**m-3 — `export-judge` không chặn khi md5 Golden khác lúc preflight "sau".**
- Vị trí: `truoc_sau.py:318-319` (chỉ ghi md5 vào `map.json`).
- Plan §2: "md5 Golden lúc xuất phải bằng md5 Golden sau bước 8".
- Tác động hiện tại: 0 vì Golden không đổi (0 sửa ở bước 8, md5 `0f7dbf41b422`).
- Tiêu chí đóng: so với `preflight_sau.json` `golden_md5`, khác thì dừng. Hoặc C kiểm bằng tay lúc review report (một dòng).

Ghi nhận (không phải finding):
- `scored()` để `None` cho câu có `error` (không có trong `map.json`). Khi đó `paired()` / `drops` sẽ báo `TypeError`. Plan coi lỗi còn lại sau một lần chạy lại là "chưa đủ",
  nên dừng là đúng hướng; chỉ có thông báo lỗi khó hiểu. Lượt hiện tại: 0 lỗi / 120 câu.
- `touched()` đọc file bằng `read_bytes().decode()`, không chuẩn hóa CRLF như offset của chunker. Không ảnh hưởng: 0 / 66 file có `\r` (B81). Luật (b) tìm `old` trên file gốc,
  cùng cách `build_gold_v4.py` (C76). `b78_touched.py` đếm 0 `old` không thấy trong file gốc ⇒ lần này không sót.
- Judge mù tốt hơn B3: cả hai bên đều context 10, nên citation `[6]`–`[10]` không lộ bên nào.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, Qdrant chỉ đọc, 0 USD:

```bash
git diff -- backend/experiments/phase_8_1/g1_retrieval.py
sha256sum ../data/phase_8_1/gold/{gold_v4,gold_v4_draft,gold_v3,gold_v2,gold_draft}.jsonl ../data/sua_kho_2026-10-27/tools/truoc_sau.py | cut -c1-12
grep -rn "gold_v3\|GOLD_PATH" --include=*.py .           # nơi dùng GOLD_PATH
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_gold_coverage.py -q
```

Thêm: chạy khô `touched` + `gold_in_context` bằng script inline (nạp `truoc_sau.py`, đổi `SK` sang `/tmp`, giới hạn vào 120 câu "sau" đã có; đã xóa `/tmp`).

## 4. Kết quả quan sát

| Kiểm | Kết quả | Đạt |
|---|---|---|
| `GOLD_PATH` | `g1_retrieval.py:45-48`: `gold_v3.jsonl` ⇒ `gold_v4.jsonl`, chú thích ghi v1 / v2 / v3 giữ để tái lập; không đổi gì khác | ✓ |
| `gold_v4.jsonl` = bản nháp User duyệt | sha `927bae1bf201` = `gold_v4_draft.jsonl` (C76 đã kiểm bản nháp: 0 lỗi, 66 / 66 + 108 / 108 khớp cách tính độc lập) | ✓ |
| v1 / v2 / v3 không đổi | `bab707b9ab22` / `2f5a347a71ff` / `3b1117cf59e9` | ✓ |
| Nơi dùng `GOLD_PATH` | `g1_retrieval`, `g2_generate`, `g3_chunking`, `g4_keyword`, `g4_rerank` — đều là harness thí nghiệm, đọc qua `load_gold`; runtime không dùng | ✓ |
| `test_gold_coverage.py` | 3 passed | ✓ |
| `preflight --arm sau` (m-3 C72) | đếm đoạn thiếu evidence, ≠ 0 ⇒ dừng; md5 `question` mọi câu phải trùng bên "trước" ⇒ dừng nếu khác; `preflight_sau.json` đã có (đã qua) | ✓ |
| `touched` (a / b / c / d; `new` rỗng ⇒ bỏ (c) — m-3 C72) | đúng plan §3. Chạy khô 120 câu: 31 câu chạm (b 27, c 27, d 3, a 0); không lỗi | ✓ |
| F1 loại `citation_error` (m-2 C72) | `check` `:222` | ✓ |
| F2 ứng viên + "mới" theo `rejudge` cả hai bên (m-1 C72) | `:404-408`; `rejudge_export` xuất **cả hai** item mỗi câu, xáo seed `SEED + 1`, một lô | ✓ |
| F4 = 500 citation mới | `:424` (tập sau − tập trước) | ✓ |
| T1 / T2 trên 129 và tập không chạm; câu 500 chấm 1; tính đủ, không tính lại (m-2 C72) | `scored` `:345-346`; `:426-427` | ✓ |
| T3 | số câu từ chối trong phạm vi mỗi bên `:429` | ✓ |
| Nhãn câu tụt | **m-1** (thứ tự ↔ tập) | ⚠ |
| W8 "Accuracy 5 ⇒ 4 mới" (m-1 C72) | `:416`, hai bên đều có câu trả lời người dùng thấy | ✓ |
| W6 (v3 + bảng đoạn cũ ↔ v4 + bảng đoạn mới) | `:382-389, :417-419`; chạy khô 37 câu có nhãn: mất 0, thêm 0; không lỗi | ✓ |
| `export-judge` | gộp câu trả lời giống hệt chữ, `item` mờ, xáo seed, `map.json`, từ chối ghi đè | ✓ (m-3) |
| `rerun-f4` | file riêng `f4_rerun`, từ chối ghi đè, không thay dòng gốc | ✓ (m-2) |
| Lượt "sau" đang chạy | 120 / 176 câu lúc kiểm, 0 lỗi | — |

## 5. Giới hạn hoặc phần chưa chạy

- `analyze`, `scored`, `rejudge`, `check-judge` chưa chạy được vì chưa có điểm judge. Chỉ đọc code; sẽ chạy lại khi review report bước 9 (plan §7).
- Chạy khô `touched` trên 120 / 176 câu, chưa có đủ bên "sau".

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** B chấm judge được.
- m-1 nên chốt **trước** `analyze`: chọn (a) hoặc (b), ghi vào report.
- m-2, m-3 đóng khi tiện. Nếu chưa sửa, C kiểm bằng tay lúc review bước 9.
