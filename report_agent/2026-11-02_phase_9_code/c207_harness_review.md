# Review: Phase 9 — harness lượt có phí sửa lịch (C207 §7)

Decision: **changes_requested** — 0 blocker · 1 major · 6 minor (mọi sửa nhỏ, 0 USD)
Người kiểm: E (Claude Code, terminal `hue-rag-28`) — không phải người viết (C)
Date: 21:15 06/11/2026 (`date`)
Canonical: plan `docs/superpowers/plans/2026-11-05-phase-9-sua-lich-plan.md` bản 3 (§4 Q2 / Q3 / Q4 / Q5, §5, §6); luật chấm `data/phase_9/bo_do_sua_lich/README.md`
Implementation report: `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §7; ghi chú `data/phase_9/sua_lich/tools/HARNESS_GHI_CHU.md`

## 1. Phạm vi đã review

| File | md5 (12) | Khớp brief? |
|---|---|---|
| `data/phase_9/sua_lich/tools/chay_sua_lich.py` | `c4dee2ccf654` | khớp |
| `data/phase_9/bo_do_sua_lich/chuoi_q4.jsonl` | `d35f8d9c5027` | khớp |
| code nhánh `p9-sua-lich` | `09ddaf9` | worktree tạm `/tmp/e_rv_sl` (đã gỡ) |

- Đã đọc toàn bộ harness, plan bản 3, README bộ đo, report C207 §7, ghi chú harness.
- Đã đối chiếu code thật của nhánh:
  - `backend/api/routes/chat.py`: `_remember`, closure `remember` của route stream, `_model_query` (`sua_chon`), dòng `chat_metrics` (`usd`, `usd_bo`);
  - `backend/llm/sua_lich.py`: `ap_hanh_dong`, `_xep_lai`, `the_chon`;
  - `backend/llm/assistant.py`: chỗ gọi `sl.ap_hanh_dong`, `turn_usd`, #6 `usd_bo`;
  - `backend/api/conversations.py`: `lich`, `set_lich`.
- **Không** mở `chuoi_sealed*.jsonl`, không đọc `STATUS_C.md` hay tin nhắn của C. Không chạy lượt có phí. File này tả chuỗi ở mức mã / loại, không chép câu.

## 2. Findings

### M-1 (major) — Q4 đếm "đạt" cả khi lượt sau lịch chưa được đưa `sua_lich` (đạt rỗng)

- **Vị trí:** `chay_sua_lich.py` `cham_q4`; `cham` (đếm `q4_loi` / `q4_luot`).
- **Yêu cầu:** plan Q4 (sàn): sau một lịch, `sua_lich` gọi nhầm 0 và tuyến đúng 100 %. Brief A: harness không làm PASS giả.
- **Bằng chứng [Chạy]:** chạy `chay` bằng khoá giả + cổng đóng trên TD2 và AT1, rồi `cham`:
  - lượt lịch của cả hai chuỗi ra `generation_failed` ⇒ cuộc không có khung;
  - lượt 2 có `sua_offered = False`, tức model không hề được đưa công cụ `sua_lich`;
  - tuyến của lượt 2 TD2 khớp nhãn ⇒ `cham_q4` không báo lỗi ⇒ **`q4_loi 1 / q4_luot 2`**, chỉ AT1 bị tính sai tuyến.
  - Câu "`sua_lich` gọi nhầm 0" ở TD2 là đúng **rỗng**: lượt đó không đo được gì về sửa lịch, vẫn tính là đạt.
- **Tác động:** lượt thật mà lượt lịch hỏng (lỗi mạng, rút lại, hỏi lại) thì Q4 trông sạch hơn thực tế. Số `q4_loi` báo cáo là số A dùng để quyết sàn.
- **Tiêu chí đóng:**
  - `cham_q4` ghi "không đo được (chưa có khung)" khi `trace.sua_offered` không đúng, hoặc khi `luu_truoc` là None;
  - `cham` đếm riêng `q4_khong_do`, không cộng lượt đó vào "đạt";
  - chạy lại probe trên ⇒ TD2 lượt 2 ra "không đo được".
  - Sửa 3–5 dòng, 0 USD.

### m-1 (minor, cần A chốt) — Q3 của harness gộp cả Q2 và lượt rút lại; có kiểm cuối là rớt chuỗi

- **Vị trí:** `cham`: `ok = ok and not q3 and not q2`; `cham_luot`: `if tr.get("lich_kiem"): q2.append("f …")`.
- **Yêu cầu:**
  - plan Q3 = hành động code áp đúng nhãn (pass^2);
  - Q2 (f) "`kiem_cuoi` 0 **theo nội dung**" (luật A 05/11: kiểm cuối báo nhầm thì đọc tay, không tự tính lỗi).
- **Bằng chứng [Chạy]:** mô phỏng S01 đúng nhãn bằng code thật, chỉ gắn `lich_kiem = ["diem_ngoai_khung"]` vào một lượt sửa ⇒ chuỗi chuyển `dat: False`, dù hành động áp vẫn đúng nhãn.
- **Tác động:**
  - Q3 của harness **chặt hơn** định nghĩa trong plan. Một lần kiểm cuối báo nhầm làm rớt cả chuỗi;
  - Q3 dưới ngưỡng ⇒ kết quả âm (cờ tắt).
  - Với `--so` (bộ kín) chỉ còn số `n_loi_q2` / `n_loi_q3`, không còn mã kiểm cuối để đọc tay.
- **Tiêu chí đóng:** A chọn một trong hai, ghi trước lượt có phí đầu:
  - (a) giữ cách chặt (Q3 gồm Q2 + lượt phải đạt), ghi rõ trong report và README;
  - (b) `cham` in **hai** số — Q3 theo hành động (định nghĩa plan) và Q3 chặt — kèm danh sách `(chuỗi, lượt, mã)` có `lich_kiem`, để đọc tay theo luật 05/11. Mã kiểm không chứa câu ⇒ in được cả với `--so`.
- **Khuyến nghị của E:** (b), vì cách tính đúng chữ plan và không mất thông tin.

### m-2 (minor) — `cham` không cờ lượt có ≠ 1 dòng `chat_metrics`

- **Vị trí:** `lenh_chay` ghi `n_metrics`; `cham_luot` / `cham_q4` không đọc trường này.
- **Yêu cầu:** bẫy `Project_Status.md` §8: log dùng chung cho pytest và server ⇒ đếm từ mốc dòng, không chạy xen.
- **Bằng chứng [Chạy]:** dòng mô phỏng gắn `n_metrics = 2` ⇒ chuỗi vẫn `dat: True`. `m` = dòng **cuối** sau mốc, có thể của tiến trình khác ⇒ outcome / usd / tuyến sai mà không ai thấy.
- **Đóng:** `cham` coi lượt `n_metrics != 1` là "không đo được" (đếm riêng, in mã chuỗi / lượt).

### m-3 (minor) — dòng tóm tắt sau "DỪNG" liệt kê cả chuỗi chưa chạy

- **Vị trí:** `lenh_chay`, `print(json.dumps({"lan", "chuoi": [c["id"] for c in viec], …}))`.
- **Bằng chứng [Chạy]:** `--tran 0` trên TD4, TD5 ⇒ in "DỪNG … chưa chạy TD4 và các chuỗi sau", rồi dòng JSON `"chuoi": ["TD4", "TD5"]`. Người đọc dễ hiểu là đã chạy.
- **Đóng:** dòng tóm tắt in chuỗi **đã chạy** (và chuỗi bỏ qua / chưa chạy tách riêng).

### m-4 (minor) — `--tran` chỉ tính tiền của **một lệnh**; trần 0,19 của cả đợt phải tự cộng tay

- **Vị trí:** `lenh_chay` (`usd` bắt đầu 0 mỗi lệnh; cộng `m.usd + m.usd_bo`). Plan §7 / §8: dừng 0,19 cho **cả** đợt, qua ≥ 6 lệnh (pilot, lần 1, lần 2, Q4 ×2, kín ×2).
- **Bằng chứng:**
  - đọc code;
  - lệnh mẫu ở C207 §7 ghi `--tran <phần trần còn>` ⇒ người chạy phải tự cộng tiền các file trước;
  - `turn_usd` trả None khi đã gọi model mà không có usage (ngắt giữa chừng) ⇒ cộng 0. Cận dưới, hiếm gặp.
  - Vượt tối đa một chuỗi (≈ 0,004–0,006) là trong khoảng trống giữa dừng 0,19 và trần 0,20 — chấp nhận.
- **Đóng:** một trong hai cách:
  - harness in "tổng USD trong file kết quả (mọi lần) + lệnh này" sau mỗi chuỗi;
  - runbook ghi lệnh một dòng cộng `usd` từ mọi file `do/*.jsonl` trước mỗi lệnh có phí.

### m-5 (minor, chỗ C tự quyết (2)) — Q2 (b) bỏ hẳn sau lượt xếp lại, trong khi code có giữ chỗ

- **Vị trí:** `cham_luot` `if not xep_lai:` (bỏ (b) khi model gửi đổi số ngày / tham số).
- **Yêu cầu:** plan Q2 (b) "mọi lượt sửa"; D5 "xếp lại **có giữ**".
- **Bằng chứng:** đọc `sua_lich._xep_lai`:
  - giữ chỗ các điểm còn hợp tham số mới (ngày ≤ n, hợp sở thích, buổi hợp người đi cùng);
  - khung phạm luật ⇒ xếp lại **không giữ** (đường dự phòng).
  - Bỏ hẳn (b) là hợp với đường dự phòng đó. Nhưng như vậy, nếu phần giữ chỗ hỏng ở lượt đổi số ngày (vd S10), harness không bắt được.
- **Tác động:** thấp — `_xep_lai` là code tất định, test 0 USD bắt được tốt hơn harness có phí. Nhưng đây là **nới một sàn** ghi trước, nên cần A ghi nhận.
- **Đóng:** A ghi nhận cách hiểu "(b) không áp sau xếp lại; giữ chỗ khi xếp lại do test code bảo vệ" vào README luật chấm. Hoặc trỏ tới test có sẵn trong `test_sua_lich.py` khẳng định giữ chỗ khi đổi số ngày. Không cần sửa harness.

### m-6 (minor) — chuỗi chạy dở bị bỏ qua khi chạy lại mà không báo là dở

- **Vị trí:** `lenh_chay` `da_co = {(lan, chuoi)}` — có một dòng của chuỗi là coi như đã chạy.
- **Bằng chứng:** đọc code. Lệnh dừng giữa chuỗi (ngoại lệ, Ctrl-C) ⇒ chạy lại bỏ qua chuỗi đó ⇒ `cham` báo "chưa chạy" ở các lượt thiếu ⇒ chuỗi rớt.
  Đúng luật "không chạy lại một chuỗi ở cùng lần". Nhưng dòng "bỏ qua" không nói chuỗi nào **dở**, nên lỗi harness / máy dễ bị đọc nhầm thành lỗi model.
- **Đóng:** dòng "bỏ qua" tách "đủ lượt" và "dở (k / n lượt)". Report ghi chuỗi dở là lỗi chạy, không phải lỗi model.

## 3. Ba chỗ C tự quyết (C207 §7) — có hợp plan không

| | Quyết của C | Nhận xét E |
|---|---|---|
| (1) | Q3: trường điền lại đúng giá trị cũ ⇒ không bắt phải áp; câu ngoài bảng chỉ so mã luật; dư một dòng "Không đổi được" ngoài nhãn ⇒ không trừ | **Hợp:** đúng D5 (chỉ nhận trường khác giá trị lưu); so mã luật là đủ cho điểm ngoài bảng. Dòng dư không trừ: chấp nhận vì nhãn chỉ ghi điều phải có. Dòng dư vẫn nằm trong file kết quả — đọc lúc xem pilot |
| (2) | Q2 (b) sau xếp lại chỉ kiểm (d) + điểm đã thêm; dời buổi vào ô có một điểm ⇒ điểm kia được đổi chỗ | Phần "dời buổi đổi chỗ hai điểm" **hợp** (điểm kia bị hành động chạm). Phần "sau xếp lại" ⇒ m-5 (A ghi nhận) |
| (3) | Q4: TD1 nay là câu sửa ⇒ gọi `sua_lich` là đúng, chỉ theo dõi; TD3 lượt 2 là lịch đầu; C thêm 2 chuỗi an toàn | **Hợp:** D8 cho gọi `sua_lich` khi câu nhờ đổi lịch vừa xếp; plan §5 có ghi "2 chuỗi an toàn sau lịch". Lưu ý: chuỗi an toàn chỉ đo được khi lượt lịch có khung ⇒ M-1 |

Pilot = S01 + S06 (A đồng ý): hợp — S06 là chuỗi duy nhất có thẻ chọn, đường bấm nút chỉ lộ khi có model thật.

## 4. Cách người kiểm chạy lại thật (0 USD)

Từ `backend/` của worktree `/tmp/e_rv_sl` (`09ddaf9`, symlink `data/` + `knowledge-base-hue/`, đã gỡ). Chạy bằng `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`.
Lượt `chay`: `OPENAI_API_KEY=<khoá giả>`, `OPENAI_BASE_URL=http://127.0.0.1:9`, không nạp `.env`.

| Lệnh / ca dò | Kết quả |
|---|---|
| `kiem chuoi_da_thay.jsonl` | Q3 **10 / 10**, Q2 **0 / 42**, ca phá **9 / 9** — khớp report C |
| `kiem chuoi_q4.jsonl` | 7 chuỗi, 14 lượt; 0 chuỗi mô phỏng (bộ Q4 không có `tham_so`) |
| `chay chuoi_q4.jsonl --lan 1 --chi TD2,AT1` (khoá giả) | 4 lượt; mỗi lượt `n_metrics` 1; `cuoc` 0 / 0 / 1 / 1 (mỗi chuỗi một cuộc); `log_co_cau_hoi 0`; grep 3 câu của bộ trong log worktree = **0**; 0 USD |
| chạy lại đúng lệnh trên | `"chuoi": []` — chuỗi đã có ở lần 1 không chạy lại; file vẫn 4 dòng |
| `chay … --chi TD4,TD5 --tran 0` | "DỪNG … chưa chạy TD4" ⇒ dừng trước chuỗi đầu; tóm tắt in sai danh sách (m-3) |
| `cham chuoi_q4.jsonl` trên file trên | `q4_loi 1 / 2` — TD2 lượt 2 đạt rỗng (M-1) |
| **ca dò E** (cách khác C: gắn trực tiếp vào dòng mô phỏng S01 bằng code thật) | `lich_kiem` ở lượt đúng nhãn ⇒ chuỗi rớt (m-1); `n_metrics 2` ⇒ không cờ (m-2) |
| **bất biến:** `cham` là hàm thuần, chấm 2 lần cùng dữ liệu không sửa dòng | giữ — chuỗi JSON trước / sau giống hệt |

Đọc code [không chạy]:
- Bọc `_remember`: route stream gọi `_remember` qua closure `remember`, tên được tìm lúc gọi ⇒ bản bọc của harness được gọi, rồi hàm thật chạy với **cùng** đối số.
- Bọc `ap_hanh_dong`: `assistant.py` gọi qua `sl.ap_hanh_dong` ⇒ bản bọc ghi `model_gui` rồi trả đúng kết quả hàm thật. Không đổi hành vi.
- `_remember` chỉ `set_lich` khi lượt đạt (tuyến `tro_ly_hue`, không lỗi trích dẫn, có `luu`) hoặc khi dừng ở thẻ (khung giữ nguyên) ⇒ Q2 (g) so riêng `khung` là đủ.
- USD = `usd` + `usd_bo` (#6: phần trả lời song song bị bỏ) ⇒ đủ tiền thật của lượt.

## 5. Giới hạn

- Đường thành công (khung lưu sau lượt đạt, `sua_lich` được đưa, thẻ chọn thật ⇒ lượt bấm, 422) cần model thật ⇒ **NOT RUN**, như C đã ghi. Lộ ở pilot S01 + S06 — đọc file pilot trước khi chạy tiếp (đúng plan bước 3).
- Không chạy `cham` trên dữ liệu có lượt sửa thật; các ca dò dùng dòng mô phỏng bằng code thật.
- Không kiểm phần kín (không mở được, đúng luật).

## 6. Decision và bước tiếp theo

**changes_requested.** C sửa M-1 (bắt buộc trước pilot) và m-2, m-3, m-6 — đều vài dòng, 0 USD.
Hai chỗ cần **A chốt trước lượt có phí đầu**: m-1 (Q3 chặt hay theo hành động — E khuyến nghị in cả hai) và m-5 (ghi nhận cách hiểu Q2 (b) sau xếp lại).
m-4 sửa bằng harness hoặc bằng runbook đều được.
Người kiểm lại: chạy probe M-1 (khoá giả, TD2) + `kiem` ⇒ vẫn 10 / 10, 9 / 9; dùng lại các kiểm khác của bản này nếu phần sửa không chạm `lenh_chay` ngoài dòng in.

---

## Vòng 2 — kiểm phần sửa (E, 21:33 06/11/2026 `date`)

Đối tượng: `chay_sua_lich.py` md5 **`b68e7c970782`** (vòng 1 `c4dee2ccf654`). Bảng sửa của C: `c207_rebase_sua_lich.md` §7 "Sửa theo review E"; README bộ đo mục "Cách chấm của harness".
Chỉ xem phần sửa + đường bị ảnh hưởng; worktree tạm `/tmp/e_rv_sl` (`09ddaf9`, đã gỡ). 0 USD. Không mở `chuoi_sealed*`.

### Đối chiếu từng finding

| Finding | Đóng? | Bằng chứng |
|---|---|---|
| M-1 Q4 đạt rỗng | **đóng** | Đọc `cham_q4`: trả "không đo được" khi `luu_truoc` None hoặc khi tuyến `tro_ly_hue` có khung mà `sua_lich` không được đưa; đếm `q4_khong_do`, danh sách `khong_do`. Ca dò E [Chạy] (cách khác C: gọi thẳng `cham_q4` với dòng tự dựng): tuyến khẩn cấp có khung + không đưa công cụ ⇒ **vẫn đo**, đúng vì tuyến khẩn cấp không đưa công cụ; có khung + gọi nhầm ⇒ lỗi "gọi sua_lich nhầm"; 0 dòng `chat_metrics` ⇒ không đo được |
| m-1 Q3 = hành động (A chốt) | **đóng** | `ok = ok and not q3` (không gộp Q2); lượt `retracted` vẫn chấm hành động; `rut_lai_kiem_cuoi` (chuỗi, lần, lượt, mã) in cả khi `--so`. `kiem` [Chạy]: ca ngược "kiểm cuối ở lượt đúng nhãn ⇒ Q3 vẫn đạt + liệt kê" đúng |
| m-2 `n_metrics` ≠ 1 | **đóng** | `cham_luot` / `cham_q4` ⇒ không đo được; `kiem`: ca phá "2 dòng chat_metrics" bắt |
| m-3 tóm tắt sau DỪNG | **đóng** | [Chạy] ⇒ `"da_chay": [], "chua_chay": ["TD2"]` |
| m-4 trần cả đợt | **đóng** | `--dung` mặc định 0,19, cộng `usd` + `usd_bo` mọi `*.jsonl` cùng thư mục. [Chạy]: 2 file giả tổng 0,19 ⇒ "DỪNG … cả đợt 0.190000 USD" trước chuỗi đầu, 0 lượt gọi |
| m-5 Q2 (b) sau xếp lại | **đóng** | Thêm `_giu_khi_xep_lai` viết theo chữ D5, độc lập với code: điểm còn hợp tham số mới phải giữ chỗ, trừ điểm hành động cùng lượt chạm. Đường dự phòng "xếp lại không giữ" của code sẽ hiện thành vi phạm (b) ⇒ đọc tay — ghi rõ ở README. `kiem`: Q2 0 / 42 (không báo nhầm trên mô phỏng đúng nhãn), ca phá "xếp lại không giữ chỗ" bắt |
| m-6 chuỗi dở | **đóng** | Dòng "bỏ qua" tách "đủ lượt" / "DỞ (k / n lượt)", ghi rõ là lỗi chạy, không phải lỗi model (đọc code; C đã chạy ca xoá dòng cuối) |

`kiem chuoi_da_thay.jsonl` [Chạy]: Q3 **10 / 10**, Q2 **0 / 42**, ca phá + ca ngược **13 / 13**, khớp C.
Bất biến vòng 1 (bọc hàm gọi hàm thật với cùng đối số; chuỗi đã có ở cùng lần không chạy lại; log 0 câu hỏi): phần code đó không đổi ngoài dòng in ⇒ **dùng lại** kết quả vòng 1.

### Finding mới

- **n-1 (minor) — thư mục kết quả chưa có ⇒ lệnh `chay` lỗi.**
  - **Bằng chứng [Chạy]:** out trỏ vào thư mục chưa tạo ⇒ `FileNotFoundError` ở `out.open("a")`. Lỗi xảy ra sau khi nạp app, **trước** mọi lượt gọi ⇒ 0 USD.
  - Thư mục `data/phase_9/sua_lich/do/` mà lệnh pilot dùng **chưa có** (đã `ls`).
  - **Đóng:** `out.parent.mkdir(parents=True, exist_ok=True)`, hoặc runbook thêm `mkdir -p $K` trước pilot. Sửa lúc chạy, không cần review lại.

### Kết luận vòng 2: `ready_for_user_confirmation`

M-1 và 6 minor vòng 1 đã đóng. Còn n-1 (minor, 1 dòng, không tốn tiền nếu quên). Harness đủ để chạy pilot S01 + S06 khi A cho.

---

## Vòng 3 — kiểm phần đổi do rebase C208 (E, 21:54 06/11/2026 `date`)

Đối tượng: `p9-sua-lich` `09ddaf9` ⇒ **`79b3d9c`** trên `main` `d930867` (B5b + B171). Report C: `c207_rebase_sua_lich.md` §8.
Harness `559ebaf5f81e`; bộ đã thấy `chuoi_da_thay.jsonl` `c00de07114b5`. Worktree tạm `/tmp/e_rv_sl` (`79b3d9c`, đã gỡ). 0 USD. Không mở `chuoi_sealed*`.

### Đã kiểm

| Kiểm | Kết quả |
|---|---|
| `git log main..79b3d9c` | 3 commit đúng report (`ec14ede` gỡ xung đột · `6a65df1` = B166 · `79b3d9c` C208). `range-diff`: B166 "="; B163 chỉ đổi phần gộp |
| Đọc `git diff main 79b3d9c -- backend/llm/assistant.py` | `_xong_lich` chung cho xếp mới / nút Sửa / `sua_lich`, có `du_bao` (dòng thời tiết B5b chạy cả lượt sửa); `hoi_toi=lt.hoi_buoi_toi(query)` của B171 còn ở lượt xếp mới; `_lich_extra` = công cụ `lich_trinh` + `sua_lich` (chỉ khi cuộc có khung) + phần `thoi_tiet` của B5b; `ROUTE_INPUTS` có `lich_cu`, `sua_chon` — khớp report |
| Đọc diff `79b3d9c` (`sua_lich.py` +6 / −3) | `_xep_lai` truyền `hoi_toi` đã lưu (`tham_so` của khung có khoá `hoi_toi` — `lich_trinh.py` dòng dựng `tham_so`); sửa trực tiếp giữ mục `MA_TOI` khi khung vẫn không có buổi tối. Mục `MA_TOI` chỉ được `xep` thêm khi `hoi_toi` ⇒ không xin tối thì không đổi gì |
| **Ca dò E** (cách khác test của C: chuỗi 2 lượt + đổi người đi cùng) [Chạy] | (1) người lớn tuổi + xin tối ⇒ đổi sang cặp đôi (xếp lại): `toi_lon_tuoi` mất, `hoi_toi` lưu vẫn True, lý do đổi thành `toi_khong_diem` — giống hệt xếp mới cặp đôi + xin tối trên `main` (đã chạy so). (2) **Bất biến:** không xin tối ⇒ bỏ điểm / đổi số ngày ⇒ 0 mục `MA_TOI`. (3) trẻ em + xin tối ⇒ đổi số ngày rồi bỏ điểm (2 lượt liền) ⇒ `toi_tre_em` còn ở cả hai lượt |
| `pytest test_sua_lich.py test_b5_lich_trinh.py test_b5b_thoi_tiet.py` (không khoá) | **347 passed** |
| Nhãn đã thấy: so `chuoi_da_thay.truoc_C208.jsonl` ↔ bản mới theo trường | đổi S03 L2 (vẫn `ap_toi_da 2`, `chua_lam 1`), S08 L2 (vẫn 1 `chap_nhan`), S03 L3 chỉ đổi dòng `ghi` theo tên điểm mới (README có ghi). Số chuỗi / lượt / loại câu không đổi |
| harness `kiem` trên bộ mới, code `79b3d9c` | Q3 **10 / 10**, Q2 **0 / 42**, ca phá **13 / 13** |
| n-1 vòng 2 | **đóng** — `chay` tự `mkdir` thư mục kết quả (`559ebaf5f81e`) |

Dùng lại, không chạy lại: Q1 / Q1m 228 / 228 giống byte và build giao diện của C (§8). Lý do: phần E kiểm thêm không đổi chuỗi gửi model; Q1m trùng sha với C207.

### Ngoài phạm vi (ghi nhận, không phải finding của rebase)

- Câu cố định `toi_khong_diem` ("…chưa có điểm buổi tối hợp sở thích của bạn") vẫn hiện khi người dùng **không nêu sở thích**. Hành vi này có sẵn trên `main` (B171), không do rebase. A xét khi bật `lich_trinh`.
- Lượt sửa không có cách **mới** xin buổi tối: `hoi_toi` chỉ lấy từ câu lịch đầu. Câu kiểu "thêm buổi tối nhé" ở lượt sửa ⇒ model phải dùng `them_diem` có buổi. Theo dõi khi đo.

### Còn chờ

- Mô phỏng nhãn **kín** trên nền mới (`mo_phong_kin.py`, User `!` ở terminal C) — E không mở được. Kết quả hỏng ⇒ C sửa nhãn kín trước lượt có phí.

### Kết luận vòng 3: `ready_for_user_confirmation`

Gộp B5b + B171 đúng ở các chỗ đã kiểm. Lỗi gộp `hoi_toi` đã sửa và có test; ca dò riêng của E đạt. Không có finding mới.
