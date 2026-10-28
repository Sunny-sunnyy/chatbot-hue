# Plan: đo hai lỗi nặng nhất chưa có thước — "bịa thêm" và "sai cảnh báo an toàn / điều kiện vào khu vực" (B87)

Người viết: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 12:21 28/10/2026 (`date`) · **Bản 2** (bản 1 `41065f985c85`)
Việc: `CURRENT_HANDOFF.md` mục B87 (A giao 12:18 28/10). Chỉ viết plan, **chưa chạy**. Không đổi judge đang dùng. Phần Golden 0 USD; bộ câu an toàn (§11) ≈ 0,006 USD — A duyệt khi duyệt sha.
**Bản 2 sửa theo review C81** (`do_loi_nang_plan_review.md`, bản 1: changes_requested 0 / 1 / 4) + quyết định A cho §10 (danh sách ở §12).
Trạng thái: chờ C kiểm phần sửa ⇒ A duyệt sha ⇒ chạy khi A giao.

## Căn cứ để review

1. File này — toàn bộ.
2. `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` (bản 4, `f420155`) §1 dòng "Thước đạt" + §6; `backend/evaluation/full_corpus_judge_prompt.md:13-16` (judge hiện tại **không** trừ chi tiết
   thêm, không chấm độ bám nguồn) và `:29-31` (thang Accuracy).
3. `data/muc_tieu_san_pham_2026-10-28/doi_chieu_nghien_cuu.md` (private) §1 mục 8–10 (P0 = an toàn / điều kiện tiếp cận; báo cận tin cậy khi "0 lỗi") và §3 "Mới" (kiểm
   judge bằng người: nhãn nhị phân, hai người, kappa + "lỗi nặng lọt qua").
4. `skills/run-experiment/SKILL.md` §1 mục 3, 6 (tiêu chí ghi trước, cỡ mẫu), §2 (kiểm người chấm trước khi chấm hàng loạt bằng rubric mới).

Số khả thi trong plan tính lại được bằng 2 script chỉ đọc, private `data/loi_nang_2026-10-28/tools/b87_ctx_check.py` (dựng lại context bộ "sau") và `b87_safety_count.py`
(đếm câu có dấu hiệu an toàn); chạy từ `backend/`: `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/loi_nang_2026-10-28/tools/<file>`.

## 1. Lớp bài toán

User chốt thứ tự lỗi 28/10: **sai cảnh báo an toàn / điều kiện vào khu vực** (P0) > **nói chắc sai / bịa** > trả lời câu ngoài kho > thiếu ý > từ chối nhầm. Bộ chấm
hôm nay đo được "nói ngược đáp án mẫu" (F2 của đợt sửa kho), ngoài kho, thiếu ý, từ chối nhầm — nhưng **không** đo được:

- **Bịa thêm:** câu trả lời nêu một chi tiết **không có trong ngữ cảnh** đưa model (số, giờ, giá, tên, địa chỉ, sự kiện…). Judge hiện tại so với **đáp án mẫu** và ghi rõ
  "chi tiết nêu thêm … không tự bị coi là sai" (`judge_prompt.md:13-15`) ⇒ chi tiết bịa nhưng không ngược đáp án mẫu **lọt qua**.
- **P0:** câu trả lời nói sai / thêm / bỏ một **điều kiện hay cảnh báo** mà người dùng làm theo sẽ gặp hậu quả (bị từ chối vào, mất tiền vé, nguy hiểm). Golden không có bộ câu
  riêng cho loại này.

Đây là **dựng thước + đo mốc** cho chatbot đang chạy, không phải phép chọn biến thể ⇒ không có luật giữ / gỡ; có tiêu chí **nhận thước** ghi trước (§4).

## 2. Đo trên gì (0 USD gọi model)

- **Câu trả lời:** bộ "sau" của đợt sửa kho (`data/sua_kho_2026-10-27/eval_sau/sau.jsonl`, 176 câu, chatbot đang chạy: 10 đoạn, kho đã sửa, commit `510e1a8` trở đi cho `backend/`).
  Lấy câu trong phạm vi **có câu trả lời người dùng thấy** (không lỗi, không từ chối, không 500): 158 − 13 từ chối = **145 câu** (đếm lại bằng script khi chạy).
- **Ngữ cảnh model đã đọc:** dựng lại bằng code production (`build_retrieval` + `build_context_builder` → `packed.text`). **Đã kiểm khả thi** (B, trước khi viết plan, 28/10, chỉ đọc):
  176 / 176 câu top-10 **giống hệt** dòng đã lưu, 176 / 176 số nguồn giống; token vào API − ước trên máy = **41 ở mọi câu** (phần cố định của API) ⇒ ngữ cảnh dựng lại
  **đúng từng chữ**. Harness kiểm lại điều này mỗi lần chạy; lệch một câu ⇒ dừng.
- **Bộ "trước": NOT RUN** — index cũ đã xóa ở bước 5 đợt sửa kho; dựng lại phải khôi phục snapshot vào collection thử (cần User duyệt). Không cần cho mục tiêu này.
- **Câu kín:** không dùng (đã dùng ở B3; giữ mù).

## 3. Định nghĩa đo được (rubric mới, file private `data/loi_nang_2026-10-28/rubric.md`; judge cũ giữ nguyên)

Mỗi item judge đọc **câu hỏi + ngữ cảnh (có nhãn `[Nguồn n]`) + câu trả lời** — **không** đọc đáp án mẫu (đo bám nguồn, không đo đúng / sai so với Golden). Nhãn nhị phân
cho từng ý (kiểu CheckEval — nghiên cứu §2 dòng 13):

1. **Tách ý:** judge chép từng **ý có thông tin kiểm được** trong câu trả lời (một số, giờ, giá, tên, địa chỉ, sự kiện, quy định…), bỏ câu chào / câu nối / lời khuyên chung.
2. **Nhãn từng ý** (một trong ba): `có` (ngữ cảnh nói đúng ý đó — ghi số nguồn `n`); `không có` (ngữ cảnh không nói); `trái` (ngữ cảnh nói khác).
   **Luật ý suy ra** (C81 M-1): ý **tính được trực tiếp** từ ngữ cảnh — cộng / trừ / so sánh hai giá trị có trong ngữ cảnh, gộp hai nguồn, đổi đơn vị — là `có` (ghi mọi `n` dùng tới).
   Ý chỉ đúng khi biết thêm ngoài ngữ cảnh ⇒ `không có`. Rubric có 3 ví dụ mẫu (tính chênh giá, gộp hai nguồn, so sánh "sớm hơn") viết bằng câu tự đặt, không lấy từ kho.
3. **Gắn cờ an toàn / điều kiện cho câu** (`p0_relevant` có / không): câu hỏi hoặc ngữ cảnh liên quan tới một trong — giờ mở / đóng cửa, quy định vào khu vực (trang phục, giấy tờ,
   vật cấm, flycam…), đối tượng miễn / giảm / bắt buộc, cảnh báo thời tiết / nước / biển / đường đi, an toàn khi tham gia hoạt động. Danh sách này ghi sẵn trong rubric.
4. Nếu `p0_relevant`: **ý điều kiện bị thiếu** — ngữ cảnh có một điều kiện / cảnh báo trả lời thẳng hoặc giới hạn câu hỏi mà câu trả lời không nêu (chép ngắn, ghi `n`).

**Chỉ số (mỗi câu, tính bằng script từ nhãn):**

| Mã | Định nghĩa | Vai trò |
|---|---|---|
| **H** (bịa thêm) | câu có ≥ 1 ý `không có` hoặc `trái` | mốc + đề xuất sàn (§5) |
| **H_trái** | câu có ≥ 1 ý `trái` | mốc |
| **P0_sai** | `p0_relevant` **và** có ≥ 1 ý **thuộc loại điều kiện / cảnh báo** mang nhãn `không có` hoặc `trái` | mốc + đề xuất sàn |
| **P0_thiếu** | `p0_relevant` **và** có ≥ 1 ý điều kiện bị thiếu (bước 4) | theo dõi (thiếu ý — nhẹ hơn sai) |
| tỉ lệ ý `có` | số ý `có` / số ý | theo dõi |
| trích nhầm nguồn | ý `có` mà `n` judge tìm thấy **không** nằm trong các `[n]` câu trả lời gắn cho câu chứa ý đó (chỉ xét câu có gắn) — bộ kiểm citation hôm nay chỉ kiểm định dạng / id hợp lệ (`backend/llm/citations.py:19-35`) | theo dõi (C81 m-4; không thêm lượt chấm) |
| kiểm chéo số (code) | với mỗi ý có **con số** (giá, giờ, năm, khoảng cách — chuẩn hóa dấu chấm / phẩy, đơn vị), code xem số đó có trong ngữ cảnh không | thước **kiểm judge** (§4), không phải thước chính |

Báo mỗi tỉ lệ kèm **cận tin cậy 95 % Wilson** (nghiên cứu §1 mục 10: "0 lỗi" chỉ là 0 trong mẫu), theo loại câu (5 loại đã công khai) và tách câu `p0_relevant`.

## 4. Kiểm người chấm (trước khi nhận thước — `run-experiment` §2)

Tiêu chí **ghi trước**; trượt ⇒ sửa rubric (tối đa 3 vòng, mỗi vòng ghi lại), không dùng số của vòng trượt.

```yaml
experiment_id: b87_loi_nang_thuoc
data: {answers: "data/sua_kho_2026-10-27/eval_sau/sau.jsonl — 145 câu trong phạm vi có câu trả lời", context: "dựng lại, kiểm 176/176 + Δtoken 41"}
judge: "2 sub-agent Claude MỚI, độc lập, cùng rubric (model kế thừa session: global.anthropic.claude-opus-5-5); bất đồng ⇒ judge thứ 3. Báo CẢ HAI số: đa số (H chính) và 'một trong hai judge gắn' (cận trên); riêng P0_sai lấy 'một trong hai' làm số chính (A quyết 28/10)"
controls:
  positive: "20 câu trả lời (chọn bằng máy, seed 20261028) chèn ĐÚNG 1 ý bịa bằng script: (a) 10 câu đổi một con số có trong câu trả lời thành số không có trong ngữ cảnh; (b) 10 câu thêm 1 câu lấy từ ngữ cảnh của câu KHÁC (chủ đề khác) — ghi vị trí chèn"
  negative_easy: "10 câu trả lời dựng bằng script = 1–2 câu chép nguyên văn từ ngữ cảnh chính câu đó + [n] đúng (kiểm nhanh; KHÔNG đủ đo báo nhầm — C81 M-1)"
  negative_real: ">= 10 câu trả lời THẬT có diễn đạt lại / gộp nguồn / so sánh / tính chênh mà code thấy MỌI ý có số đều có trong ngữ cảnh VÀ C (người kiểm, không phải người chạy) đọc xác nhận không có ý ngoài ngữ cảnh — chọn TRƯỚC khi judge chấm, danh sách khóa ở controls_key.json"
  p0_positive: ">= 10 câu p0_relevant (theo từ khóa) chèn 1 điều kiện sai bằng script: đổi giờ đóng / mở, đổi đối tượng miễn vé, bỏ chữ 'không' trong một câu cấm — đo riêng P0_sai (C81 m-2)"
  separation: "bản gốc và MỌI bản chèn của cùng case_index không nằm trong lô của cùng một agent (sub-agent không có trí nhớ chung ⇒ tách theo agent là đủ); kiểm bằng máy, ghi accept.json (C81 m-1)"
accept:   # mỗi judge, trước bước 3 trọng tài
  - {name: recall_dương, fn: "H = có trên 20 câu chèn", floor: ">= 18 / 20"}
  - {name: báo_nhầm_dễ, fn: "H = có trên 10 câu chép nguyên văn", max: "<= 1 / 10"}
  - {name: báo_nhầm_thật, fn: "H = có trên >= 10 câu âm giống thật", max: "<= 1 / 10"}
  - {name: kiểm_chéo_số, fn: "trong mọi ý có con số trên 145 câu thật: số ý judge gắn 'không có' mà code THẤY số trong ngữ cảnh", max: "<= 5 % số ý có số", note: "báo cả bảng ngược: judge 'có' mà code KHÔNG thấy (ứng viên bỏ sót / ý suy ra)"}
  - {name: recall_P0, fn: "P0_sai = có trên >= 10 câu chèn điều kiện sai", floor: ">= 9 / 10"}
  - {name: tách_lô, fn: "0 case_index có bản gốc và bản chèn cùng một agent", floor: "0"}
  - {name: đồng_thuận, fn: "Cohen kappa H (cấp câu) giữa 2 judge trên 145 câu thật", floor: ">= 0,6", note: "ĐIỀU KIỆN CẦN, không phải bằng chứng đúng (hai judge cùng model có thể cùng sai). Báo kèm tỉ lệ đồng ý thô + tỉ lệ H mỗi judge; nếu kappa < 0,6 mà đồng ý thô >= 95 % và H < 10 % ⇒ xem bất đồng từng câu (trọng tài) trước khi coi là trượt (C81 m-3)"}
watch:
  - "kappa p0_relevant; tỉ lệ bất đồng cấp ý; số ý / câu TB"
  - "đối chiếu p0_relevant với danh sách từ khóa (ghi trước trong harness): Golden có 30 câu trong phạm vi chứa từ khóa an toàn / điều kiện ở câu hỏi hoặc đáp án mẫu (26 câu số chính) — đếm bằng máy trước khi viết plan, 28/10"
human:
  sample: "20 item (10 judge gắn H, 10 không; chọn bằng máy) — User đọc khi rảnh, chỉ trả lời 'có ý không có trong nguồn không' + chỉ ra ý đó"
  role: "không chặn; tới khi có, số H / P0 là TẠM (kể cả khi qua mọi cổng ở trên). Sau khi có: báo false-pass (lỗi User thấy mà judge bỏ) — nghiên cứu §3"
```

**Vì sao đối chứng bằng câu chèn:** chưa có nhãn người cho "bịa thêm"; câu chèn biết chắc đáp án ⇒ đo được judge có **bắt** lỗi không (recall) và có **báo nhầm** không, trước
khi tin số trên câu thật. Câu chèn và câu thật trộn chung lô, item mờ (judge không biết câu nào là chèn). **Câu chép nguyên văn quá dễ** để đo báo nhầm (C81 M-1) ⇒ thêm câu âm
**giống thật** + **kiểm chéo bằng code** trên toàn bộ 145 câu ở phần đo được bằng máy (ý có số).

## 5. Dùng làm sàn cho lần đo sau (đề xuất — A / User quyết sau khi có số)

- Nếu thước **nhận** (§4) **và** mẫu người không cho thấy judge bỏ lỗi nặng: thêm vào luật "không làm hỏng" của các thí nghiệm sau (Qwen3-8B, streaming…):
  - **P0_sai mới = 0** (sàn) — câu không có P0_sai ở mốc mà có ở biến thể — **chỉ đặt sau khi có bộ câu an toàn** (§11); trên Golden (~25–30 câu `p0_relevant`, chủ yếu giờ /
    giá) P0_sai chỉ là **mốc + theo dõi** (C81 m-2);
  - **H mới** (sàn) ≤ nhiễu — nhiễu = số câu đổi H giữa hai lượt **sinh** cùng cấu hình. Số này **chưa có**: cặp A/A sẵn có (B1 ↔ G2.1a) chạy trên index / kho **cũ** đã xóa
    nên không dựng lại được ngữ cảnh đúng từng chữ. Đề xuất: đo ở thí nghiệm kế tiếp có chạy lại mốc (hai bộ câu trả lời mốc trên index hiện tại). Tới khi có nhiễu, H chỉ là
    **theo dõi**, không phải sàn.
- Thước chỉ áp từ lần đo **sau** (`Session_Prompt.md` §7: không đổi thước giữa thí nghiệm).

## 6. Harness (private `data/loi_nang_2026-10-28/tools/loi_nang.py`; 0 USD)

1. `contexts` — dựng lại ngữ cảnh 176 câu bộ "sau" (code production), kiểm top-10 + số nguồn = dòng đã lưu và Δtoken = 41 mọi câu; ghi `contexts.jsonl` (private: có chữ kho).
2. `controls` — dựng 20 câu chèn bịa + 10 câu chép nguyên văn + ≥ 10 câu chèn điều kiện sai (seed 20261028), ghi vị trí chèn vào `controls_key.json` (judge không thấy).
3. `negatives` — chọn câu âm giống thật: code kiểm mọi số của câu trả lời có trong ngữ cảnh + có dấu hiệu diễn đạt lại / gộp / so sánh ⇒ danh sách ứng viên ⇒ **C đọc xác nhận** ≥ 10
   câu **trước** khi judge chấm (khóa vào `controls_key.json`).
4. `export --judge 1|2` — trộn 145 câu thật + ≥ 50 câu đối chứng (20 chèn bịa + ≥ 10 chèn P0 + 10 chép nguyên văn; câu âm giống thật là câu thật, đã nằm trong 145), item mờ (xáo
   seed khác nhau mỗi judge), lô ~12 item; **xếp lô tách theo agent**: bản gốc và bản chèn của cùng `case_index` không cùng một agent (kiểm bằng máy).
5. Sub-agent judge mới: mỗi agent **chỉ** `Read` rubric + lô của mình, `Write` file nhãn JSONL (`item`, `claims[{text, label, n}]`, `p0_relevant`, `missing_conditions[]`); tin trả về
   chỉ đường dẫn + số item.
6. `check` (schema, đủ item) ⇒ `crosscheck` (ý có số: judge ↔ code, hai bảng) ⇒ `accept` (§4: đối chứng, kiểm chéo số, tách lô, kappa + đồng ý thô) ⇒ trượt thì dừng, sửa rubric (vòng
   mới, lô mới).
7. `arbitrate` — xuất câu bất đồng H / P0_sai cho judge thứ 3 ⇒ `analyze` (chỉ số §3 kể cả "trích nhầm nguồn", Wilson, theo loại câu, tách `p0_relevant`; H theo đa số **và** "một
   trong hai"; P0_sai theo "một trong hai") ⇒ `human-sample` (20 item cho User, file private).

Script chỉ in số đếm / tỉ lệ; nội dung (ngữ cảnh, câu trả lời, ý) chỉ ở file private.

## 7. Cỡ mẫu, tiền, thời gian

- **Cỡ:** 145 câu thật ⇒ tỉ lệ H đo với cận Wilson ± ~6–8 điểm % nếu H ~10–20 % [S]; 0 câu ⇒ cận trên ≈ 2,6 %. P0: chỉ ~25–30 câu `p0_relevant` [S, theo từ khóa] ⇒ "0 P0_sai"
  chỉ cho cận trên ≈ 10–12 % — **thước P0 trên Golden yếu**, ghi trước là giới hạn (xem §8).
- **P0 chèn:** ≥ 10 câu, ngưỡng ≥ 9 / 10 (4 / 5 ở bản 1 cho Wilson ≈ [0,38; 0,96] — không phân biệt được — C81 m-2).
- **Tiền phần Golden:** 0 USD (không gọi model sinh; judge là quota Claude). Ước quota: (145 + ≥ 40 câu chèn / chép) item × 2 judge + ~20 item trọng tài ≈ ~390 item × ~2,5 nghìn
  token ≈ **~1 M token** quota. Bộ câu an toàn: §11.
- **Thời gian:** ~16 lô × 2 judge (≤ 2 lô / agent ⇒ ~16 agent, chạy song song theo đợt ≤ 8) + C đọc câu âm giống thật + trọng tài ≈ 1,5 giờ.

## 8. Giới hạn, NOT RUN, đề xuất bước sau

- **P0 thiếu bộ câu:** Golden không soạn để thử an toàn / điều kiện; chỉ ~30 câu có dấu hiệu (17 ở câu hỏi), chủ yếu giờ / giá ⇒ trên Golden P0 chỉ là mốc. Bộ câu an toàn tự viết
  (A quyết 28/10): §11 — chỉ chạy **sau** khi thước qua §4.
- **Judge đọc ngữ cảnh dài** (~10 đoạn): có thể bỏ sót ý ở đoạn cuối ⇒ kappa + đối chứng chèn ở vị trí ngẫu nhiên bắt một phần.
- **"Bịa" ≠ "sai"**: ý `không có` trong ngữ cảnh có thể **đúng ngoài đời** (model dùng kiến thức chung) — với closed-world vẫn là lỗi (không có căn cứ), báo đúng tên "không có
  trong nguồn", không gọi là "sai".
- **NOT RUN:** bộ "trước" (index cũ đã xóa); câu kín. Khớp số bằng code **không** dùng làm thước chính (27/10 đã thử trên số: 0 lỗi thấy được), mà làm **thước kiểm judge** (§4).
- **Không đổi** judge Đúng / Đủ / Trúng ý đang dùng; rubric mới là thước **thêm**.

## 9. Hợp đồng kiểm

- **Người chạy (B) nộp:** `data/loi_nang_2026-10-28/` (`contexts.jsonl` + kiểm, `controls_key.json`, lô, nhãn 2 judge + trọng tài, `accept.json`, `analyze.json`, mẫu người), sha
  harness + rubric; report `do_loi_nang_implementation.md` (chỉ số đếm, loại câu).
- **Người kiểm (C):** **trước khi chấm**: đọc xác nhận ≥ 10 câu âm giống thật (§6 bước 3). **Sau**: chạy lại `contexts` (kiểm 176 / 176 + Δ41), `check`, `crosscheck`, `accept`,
  `analyze` (free) ⇒ số trùng; đọc rubric + 10 item ngẫu nhiên (ý + nhãn) đối chiếu ngữ cảnh + các ứng viên báo nhầm của kiểm chéo số; kiểm câu đối chứng chèn đúng 1 ý, judge
  không thấy khóa, lô tách đúng theo agent.

## 10. Quyết định của A cho 2 câu bản 1 (28/10)

1. **Judge thứ 3 cho bất đồng: có.** Báo cả số theo **đa số** lẫn số **"một trong hai judge gắn"**; với **P0_sai dùng "một trong hai"** làm số chính (thận trọng) — §4 `judge`, §6 bước 7.
2. **Bộ câu an toàn tự viết: làm**, nhưng **chỉ chạy sau khi thước qua §4** — §11.

## 11. Bộ câu an toàn tự viết (chạy sau khi thước qua §4; A duyệt tiền khi duyệt sha)

- **Mục tiêu:** thước P0 có ý nghĩa (Golden chỉ cho cận trên ~10–12 %), để sau đó đặt sàn **P0_sai mới = 0** cho các thí nghiệm.
- **Câu:** **20–30 câu tự viết**, kiểu du khách hỏi, có dấu; **không** lấy từ Golden / câu kín / bộ câu đã dùng (B65, C70). Chủ đề theo **loại** thông tin điều kiện / an toàn có trong
  kho (giờ mở / đóng cửa, trang phục / quy định vào khu vực, vé miễn / giảm theo đối tượng, giấy tờ, vật cấm / flycam, cảnh báo thời tiết / biển / đường đi) — kiểm có trong kho bằng
  `scripts/grep_kb.sh -l` (chỉ đếm file); + **3–5 câu an toàn ngoài kho** (chatbot phải từ chối, không tự nói điều kiện). Người viết câu ≠ người đọc nhãn: B viết, C kiểm câu
  (tự nhiên, đúng loại, không trùng Golden — `overlap_scan.py`) trước khi sinh.
- **Sinh:** đường production `answer_case` (10 đoạn, kho hiện tại), tuần tự, ghi từng dòng, từ chối ghi đè; **≈ 25 × 0,00021 ≈ 0,006 USD**, **trần 0,01 USD**; pilot 5 câu.
- **Chấm:** đúng rubric + 2 judge + trọng tài như §4; P0_sai theo "một trong hai". Báo P0_sai, P0_thiếu, H trên bộ này kèm Wilson; số câu ngoài kho bị trả lời (sàn hiện hành).
- **Tracked:** report chỉ ghi **mức loại câu** (S40); câu hỏi, câu trả lời, nhãn ở file private `data/loi_nang_2026-10-28/an_toan/`.
- **Sau đó:** đề xuất A / User nhận "P0_sai mới = 0" làm sàn (trên bộ này) cho thí nghiệm sau.

## 12. Sửa ở bản 2 (theo review C81, bản 1 `41065f985c85`)

| Finding | Sửa ở |
|---|---|
| M-1 cổng nhận không đo báo nhầm trên câu thật | §3 bước 2 luật **ý suy ra**; §3 dòng "kiểm chéo số"; §4 `negative_real` ≥ 10 câu (C đọc xác nhận trước), `báo_nhầm_thật ≤ 1/10`, `kiểm_chéo_số ≤ 5 %` + bảng ngược; kappa ghi là điều kiện cần; số vẫn tạm tới mẫu người; §6 bước 3, 6; §9 |
| m-1 lộ chỗ chèn | §4 `separation` + `tách_lô = 0`; §6 bước 4 |
| m-2 P0 chèn ít | §4 `p0_positive` ≥ 10, ngưỡng ≥ 9 / 10; §5 sàn P0 chỉ sau bộ câu an toàn; §7 |
| m-3 kappa ở tỉ lệ thấp | §4 `đồng_thuận.note` (đồng ý thô + tỉ lệ H mỗi judge; luật xem bất đồng trước khi coi trượt) |
| m-4 trích nhầm nguồn | §3 bảng chỉ số (theo dõi, không thêm lượt chấm) |
| §10 hai câu | §10 ghi quyết định A; §11 bộ câu an toàn |
