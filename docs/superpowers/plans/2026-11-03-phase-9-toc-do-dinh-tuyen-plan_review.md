# Review: Phase 9 — plan thí nghiệm tốc độ #1 (mức suy luận thấp cho lần định tuyến), bản 1

Decision: **changes_requested** (0 blocker · 2 major · 4 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-32`) · việc **B139** (A giao)
Date: 19:00 03/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-03-phase-9-toc-do-dinh-tuyen-plan.md` sha **`eac748b06972`** (C151, untracked lúc review)
Cách review: chỉ dựa trên gói "Căn cứ để review" của plan + lệnh chỉ đọc / tính lại từ dữ liệu (`WORKFLOW.md` §9.1); không đọc STATUS / tin của C. 0 USD.

## 1. Phạm vi đã review

- Plan bản 1 (cả 4 mục). Căn cứ, sha khớp: `data/phase_9/toc_do/c150_phan_tich.md` `db2cab1d821c` (§0–§4) · spec Phase 9 `169c2dd5f86a` §4 · `data/phase_9/bo_do_b1/README.md` (`2c0aced78d61`) + `luat_gan_nhan_tuyen.md` `fca8d706e9e9` "Cách chấm" · `report_agent/2026-11-02_phase_9_code/b129_b1_implementation.md` §4 (P1 r1 / vòng chỉnh 1 / r2, P7 cổng, kín P1).
- Tính lại từ dữ liệu: `data/phase_9/b1/p1_da_thay_r1.jsonl`, `p1_da_thay_r2.jsonl` (253 dòng mỗi file). Code: `backend/llm/generator_openai_full_corpus.py:244–250`; thư viện trong `.venv`.

## 2. Findings

### M-1 (major) — "mốc A/A" dùng lại B1 P1 r1 + r2, nhưng r1 chạy trên lời dặn định tuyến **cũ**
- **Vị trí:** plan §2 "Mốc" ("lời dặn định tuyến không đổi từ B1 (`fb4e1aa7f8fe`) ⇒ dùng lại P1 r1 + r2 … làm mốc A/A"); §3 R (N_AA = khác tuyến giữa hai lượt mốc; "sai mốc (max)"), N ("mốc = max hai lượt mốc"), AT ("tuyến giống mốc").
- **Bằng chứng:** b129 §4 — P1 r1 ⇒ **vòng chỉnh 1** (`ROUTER_INSTRUCTIONS` thêm luật "không nêu nơi khác ⇒ Huế", `7e190d7`) ⇒ P1 r2; sha `fb4e1aa7f8fe` (b129 dòng 122) là bản **sau** vòng chỉnh. Tính lại: r1 ↔ r2 khác tuyến **đúng 1 câu** (Golden, `ngoai_pham_vi` ⇒ `tro_ly_hue`) = đúng câu vòng chỉnh sửa; sai tuyến r1 = 1, r2 = 0.
- **Tác động:** N_AA = 1 và "sai mốc max" = 1 đo **một lần đổi lời dặn**, không phải nhiễu ⇒ ngưỡng R nới thêm 2 câu so với mốc thật (≤ 0 + 0 + 1 nếu chỉ r2, so với ≤ 1 + 1 + 1 như plan); N, AT tham chiếu một lượt không cùng lời dặn. Luật giữ / gỡ có thể "đạt" khi biến làm sai tuyến thêm 2 câu.
- **Tiêu chí đóng:** mốc chỉ dùng lượt chạy trên `fb4e1aa7f8fe`: dùng lại r2 + chạy **thêm một lượt mốc mới** cho các câu cần A/A (ít nhất 123 câu rủi ro; ước ≈ 0,009 USD — hoặc 253 nếu R tính cả Golden, ≈ 0,018) cùng ngày với biến; ghi lại ước tiền tổng so trần 0,05; nếu không thêm lượt thì ghi rõ N_AA không đo được và đặt R không dựa vào N_AA.

### M-2 (major) — đo chữ đầu theo cặp chưa khoá thứ tự gửi ⇒ lệch có hệ thống do bộ đệm prompt
- **Vị trí:** plan §2 "Chữ đầu" ("xen kẽ mốc ↔ biến từng câu (hai server … ), 2 lượt ⇒ 20 cặp"), §3 Q.
- **Bằng chứng:** c150 §2 — trợ lý **lần sau trong cùng câu đọc đệm** 159 / 162, ~2.010–2.040 token; lần vào của trợ lý ≈ 2.000 token > ngưỡng 1.024 (c150 §1). Mỗi cặp gửi **cùng một câu** hai lần cách nhau vài giây ⇒ lần thứ hai có thể đọc đệm phần đầu (lời dặn + câu hỏi) mà lần đầu ghi ⇒ TTFT lần thứ hai thấp hơn. Plan không nói bên nào gửi trước.
- **Tác động:** nếu thứ tự cố định (vd luôn mốc trước), Q (trung vị chênh ≥ 0,25 s) có thể "đạt" do đệm, không do mức suy luận — đúng chỉ số quyết bị lệch.
- **Tiêu chí đóng:** ghi thứ tự đổi chiều theo cặp (ABBA hoặc theo seed ghi trước), và ghi `cached_tokens` của lần trả lời mỗi bên vào dữ liệu cặp; phân tích báo kèm Q trên các cặp `cached_tokens` = 0 cả hai bên (hoặc nêu cách loại khác).

### m-1 (minor) — sàn K không nói gì nếu **mốc** tự phạm
- K = 0 câu khẩn cấp đi tuyến khác ở mọi lượt biến. 26 câu khẩn cấp chưa có 2 lượt mốc (plan §2; b129 chỉ báo "lưới thứ hai" 8 / 8 + 2 / 2 ở phần kín, một lượt). Mốc mới 2 lượt có thể chính nó sai ⇒ K vô nghĩa.
- **Đóng:** thêm một dòng: mốc phạm K / S1 ⇒ dừng, báo A (sàn không đo được trên bản hiện hành) — không chạy biến.

### m-2 (minor) — `luat_gan_nhan_tuyen.md` "Cách chấm": câu `khan_cap` sai tuyến "không tính sàn 1, ghi riêng vì luật khẩn cấp chạy bằng code trước"
- Nay `emergency_rule` tắt (B1) ⇒ định tuyến là đường duy nhất cho câu khẩn cấp; plan đặt K riêng là đúng, nhưng nên ghi một câu vì sao lệch luật gán nhãn cũ (tránh người chạy áp nguyên văn "không tính").

### m-3 (minor) — Q / AT / probe chưa đủ chặt để chạy theo máy
- Q: "CI 95 % … > 0" — CI của **trung vị** chênh hay trung bình? ghi rõ (khớp ngưỡng ≥ 0,25 s là trung vị).
- AT: "tuyến giống mốc ở mọi câu" — khi hai lượt mốc tự khác nhau ở một câu, câu đó tính thế nào (đề xuất: so với tập tuyến của các lượt mốc).
- Probe: "không nhận mức nào thấp hơn mặc định" — mặc định chưa biết; đề xuất "nhận" = API không lỗi **và** `reasoning_tokens` probe < p50 mốc (20–22, c150 §2), ghi cả hai.

### m-4 (minor) — sàn 2 B1 (câu đi `tro_chuyen` lọt thông tin Huế, judge) không có trong §3
- Đường trò chuyện không đổi và câu Huế sang `tro_chuyen` đã bị S1 bắt ⇒ bỏ sàn 2 hợp lý; ghi một câu lý do.

**Độ đơn giản (W proportional):** một tham số sau cờ `assistant.router_reasoning_effort` (mặc định `null` = không gửi) đúng khuôn cờ `assistant:` đang có; một test byte (cờ `null` ⇒ thân yêu cầu như hôm nay) đủ — **không** thấy over-engineering. Gating Golden sau 123 câu rủi ro để vừa trần là hợp lý.

## 3. Cách người kiểm chạy lại thật

- `sha256sum` plan + 4 căn cứ (khớp, README = `2c0aced78d61` — plan ghi sha `fca8d706e9e9` chung cho "README + luật", sha đó là của file luật).
- Python chỉ đọc trên `data/phase_9/b1/p1_da_thay_r{1,2}.jsonl`: đếm khác tuyến r1 ↔ r2 theo (`set`, `id`), sai tuyến mỗi lượt (`route` ∉ `nhan` ∪ `chap_nhan`).
- `uv run python`: `agents` 0.19.4 `ModelSettings` có trường `reasoning`; `openai` 2.53.0 `Reasoning.effort` ∈ `none · minimal · low · medium · high · xhigh · max` ⇒ khẳng định [Code] của plan §1 **đúng**; `router_agent` ở `generator_openai_full_corpus.py:244–250`, `ModelSettings(max_tokens, include_usage, store)` không đặt mức suy luận — **đúng**.

## 4. Kết quả quan sát

- r1 ↔ r2: 1 / 253 câu khác tuyến (Golden, đúng câu vòng chỉnh 1 sửa); sai tuyến r1 1, r2 0 ⇒ M-1.
- Số câu §2: 40 + 20 + 5 + 32 + 10 + 16 = 123 — khớp; câu khẩn cấp cho K: 10 + 8 + (4 + 2 trong bộ tuyến) = 24 — khớp dòng "Cỡ mẫu".
- Ước tiền §4 cộng lại ≈ 0,055 — khớp; cơ chế gating Golden + dừng > 0,045 có ghi.
- Tiêu chí K, S1, N, R, AT, Q ghi **trước** khi chạy; kết quả âm ⇒ cờ `null`, không chỉnh lời dặn — khớp `run-experiment`.

## 5. Giới hạn hoặc phần chưa chạy

- Không gọi API: chưa biết `gpt-6-luna` nhận mức nào (plan tự probe). Không kiểm được bộ đệm có thật sự kích hoạt giữa hai lần gửi cùng câu (M-2 là rủi ro suy ra từ c150 §1–§2, chưa đo).
- Không mở câu kín / nội dung bộ tuyến; chỉ đếm theo nhãn.

## 6. Decision và bước tiếp theo

**changes_requested** — C sửa M-1, M-2 (và các minor nếu muốn) thành bản 2, báo sha mới; B kiểm phần sửa. Sau đó A duyệt sha. Không chặn việc khác (plan chưa chạy, 0 USD).

## Vòng 2 — kiểm phần sửa (bản 2 sha `3c5f1bbd3407`, B, 19:21 03/11/2026)

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 1 minor mới) — A duyệt sha sau khi xét m-5.

| Finding | Kiểm | Kết luận |
|---|---|---|
| M-1 | §2: mốc chỉ r2 (`fb4e1aa7f8fe`) + mốc mới cùng ngày; 77 câu có trong r2 ⇒ r2 + 1 lượt mới, 46 câu ⇒ 2 lượt mới ⇒ mỗi câu rủi ro 2 lượt mốc cùng lời dặn; R / N dùng max hai lượt + N_AA cùng lời dặn; Golden ≤ r2 + 1 (không N_AA) | **đóng**. Ghi nhận (không finding): với 77 câu, hai lượt mốc khác ngày (r2 02/11 ↔ lượt mới) ⇒ N_AA gồm cả trôi phía model theo ngày — chỉ làm ngưỡng R rộng hơn một chút, không đổi chiều |
| M-2 | ABBA ghi trước (lượt 1 lẻ mốc trước / chẵn biến trước, lượt 2 ngược lại); `cached_tokens` + `reasoning_tokens` cả lần định tuyến lẫn lần trả lời; Q báo kèm trên cặp không đọc đệm | **đóng** |
| m-1 … m-4 | dừng khi mốc phạm K / S1; lý do K lệch luật gán nhãn cũ; CI của trung vị, AT theo tập tuyến mốc, "nhận" = không lỗi + `reasoning_tokens` < 20; lý do bỏ sàn 2; sha căn cứ sửa đúng (README `2c0aced78d61`, luật `fca8d706e9e9`) | **đóng** |

**m-5 (minor, mới ở bản 2) — ước tiền vượt mức dừng của chính plan.** §4: ước ≈ 0,060, "dừng khi > 0,057". Tính lại bằng giá thật pilot B1 (0,000067 / lần định tuyến, b129 §4): probe 0,0003 + mốc 169 × 0,000067 ≈ 0,0113 + biến 422 × 0,000067 ≈ 0,0283 + chữ đầu 40 × 0,00045 ≈ 0,018 ⇒ **≈ 0,058 > 0,057** ⇒ lượt chạy đủ kế hoạch sẽ chạm mức dừng ở phần cuối (Golden hoặc chữ đầu, tuỳ thứ tự — plan chưa ghi thứ tự).
**Đóng:** ghi thứ tự chạy (đề xuất: probe ⇒ mốc ⇒ biến 123 ⇒ chữ đầu ⇒ Golden cuối, vì Golden chỉ là mức tụt phụ) **và** một trong hai: A nới trần / mức dừng (vd 0,065 / 0,062), hoặc bớt (vd Golden biến chỉ chạy câu `out_of_scope` + mẫu 30). Sửa chữ, không cần review lại cả plan.
