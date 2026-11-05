# Review: plan B6 — tra web (Serper) qua cổng code (vòng 1)

Decision: **changes_requested** (0 blocker · 1 major · 5 minor)
Người kiểm: B (Claude Code, Opus 5.5) — việc B164 (phần sau), A giao tối 05/11
Date: 19:29 05/11/2026 (`date`)
Bản được kiểm: `docs/superpowers/plans/2026-11-05-phase-9-b6-plan.md` bản 2, sha `b6a046e944c0` (tính từ file; khớp tin giao của A)

## 1. Phạm vi đã review

Chỉ dựa trên gói "Căn cứ để review" của plan (`WORKFLOW.md` §9.1); không đọc STATUS / tin nhắn của người viết.
- Plan toàn bộ.
- Spec Phase 9 `docs/superpowers/specs/2026-11-02-phase-9-design.md` (sha `77250689e605` khớp plan): §2 dòng hệ quả web, §3 sơ đồ CỔNG WEB + log, §4 thước chung (dòng "từ chối nhầm ≤ mốc + 1"), §5 B6, §7, §10 P2.
- `data/phase_9/bo_do_b6/README.md` (dòng bảng file, md5); `data/nghien_cuu_phase_9_2026-11-01/agent/b122_tra_web.md` (giá, endpoint).
- Code trên `main`: `backend/llm/assistant.py` `prepare_answer` (nhánh từ chối khi không có nguồn), `set_notice`, `_finish_generated`, `answer_turn`, `answer_turn_stream`, `answer_turn_stream_parallel`; `backend/llm/full_corpus_prompt.py` `REFUSAL_ANSWERS`; `backend/api/routes/chat.py` cờ `refusal`; `backend/api/conversations.py` `stored_answer`; `backend/llm/so_tien.py` `tim_so_tien`; `frontend/src/markdown.js` `ALLOWED_ATTR`; `data/phase_9/b0/tools/capture_model_request.py` (`fake_create`).
- **Không mở** `cau_sealed.jsonl`; không chạy `tools/kiem_bo.py` (script đọc cả bộ kín; B có thể là người code B6).

## 2. Findings

### M-1 (major) — Q4 "mức tụt ≤ 2 %" không tính được như đang ghi, và nếu tính theo nghĩa chữ thì gần như chắc trượt dù B6 đúng

- **Vị trí:** plan §4 Q4 (vế "mức tụt: câu kho trả lời được mà vẫn đi web ≤ 2 %"), §10 dòng "Từ chối nhầm", §7 cách giảm (a).
- **Yêu cầu bị ảnh hưởng:** tiêu chí ghi trước phải đo được trước khi chạy (`run-experiment`; spec §5 B6 "mức tụt").
- **Bằng chứng:**
  (1) Plan không ghi mẫu số (Golden 30? câu đã chạy ở Q4? T1 158?).
  (2) Cách giảm (a) chỉ chạy những câu bị kho từ chối ở lượt đo cũ. Vậy "câu kho trả lời được mà vẫn đi web" chỉ thấy được trong chính tập đó, không ra được tỉ lệ trên toàn bộ câu kho trả lời được.
  (3) Cổng đặt **sau** câu trả lời kho, và Q1m chứng minh chuỗi gửi trước cổng giống byte. Vậy B6 **không thể** làm đổi tỉ lệ từ chối nhầm: số câu "kho có mà đi web" đúng bằng số câu kho từ chối nhầm, tức nhiễu của khâu trả lời, không phải hồi quy do B6.
  (4) Mốc từ chối nhầm plan tự ghi ở §10 là 12 / 158 ≈ 7,6 %, đã lớn hơn ngưỡng 2 %. Trên Golden 30, chỉ cần 1 câu từ chối nhầm là 3,3 % > 2 %.
- **Tác động:** tiêu chí ghi trước có thể cho kết quả âm mà không phải lỗi của B6, hoặc không ai tính được. Đó là kiểu lệch dễ dẫn đến "sửa tiêu chí sau khi đo" (`Session_Prompt.md` §4).
- **Tiêu chí đóng:** plan ghi rõ cách tính **trước** khi đo. Đây là chỗ spec để ngỏ nên A chốt, plan ghi lại. Gợi ý (một trong hai):
  - (i) Đổi vế này thành: "tỉ lệ từ chối nhầm không đổi — do Q1m bảo đảm (chuỗi gửi trước cổng giống byte), ghi là suy ra từ Q1m". Kèm sàn: trong mọi câu kho có mà đi web ở lượt Q4, mục web không trái kho và không làm nhẹ cảnh báo (judge, cùng thước S-OOS). Số câu như vậy ghi ở Q5 để theo dõi.
  - (ii) Giữ một con số, nhưng ghi mẫu số và luật so như spec §4: "từ chối nhầm ≤ mốc + 1", so với lượt cờ tắt trên cùng tập.

### m-1 — D1: "câu từ chối chuẩn" cần ghi đúng hằng số và đúng nhánh outcome

- **Bằng chứng:** `REFUSAL_ANSWERS = (INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER)`; cờ `refusal` của `chat.py` so sau `.strip()`. Ngoài ra `prepare_answer` đặt sẵn `INSUFFICIENT_ANSWER` với `fixed_outcome = "refusal_no_sources"` khi ngữ cảnh rỗng, không qua model.
- **Tiêu chí đóng:** D1 ghi rõ ba điều:
  - cổng chỉ mở với `INSUFFICIENT_ANSWER`, không mở với `OUT_OF_SCOPE_ANSWER` (model trong tuyến `tro_ly_hue` vẫn có thể viết câu này);
  - so sau `strip()`, giống cờ `refusal`;
  - `refusal_no_sources` có tính là "outcome thường" hay không (gợi ý: có, vì đây đúng là ca "kho không có").
  Test cổng phải có một ca cho mỗi nhánh.

### m-2 — Q1m: công cụ chụp không bao giờ tới được cổng; cần ghi điều đó và chặn mạng Serper khi chụp

- **Bằng chứng:** `capture_model_request.py` `fake_create` ghi thân yêu cầu rồi `raise Captured()`, nên model không bao giờ trả câu từ chối và cổng không mở trong lượt chụp. Vế "đếm lượt có lần gọi thêm" của Q1m vì vậy luôn ra 0, không đo gì. Ngoại lệ là nhánh `refusal_no_sources`: câu này có trước khi gọi model, nên cổng có thể mở và gọi Serper ngay trong lượt chụp.
- **Tiêu chí đóng:** Q1m ghi rõ ba điều:
  - lượt chụp chỉ chứng minh phần trước cổng giống byte;
  - hành vi cổng do test với client kịch bản chứng minh (đã có ở §3);
  - lượt chụp chạy không có khoá Serper, và `tra_web.py` thiếu khoá thì trả `web_loi` mà **không** mở kết nối mạng (một test).

### m-3 — D5 (ii) "0 URL": nói rõ mẫu bắt

- **Bằng chứng:** `markdown.js` `ALLOWED_ATTR` hôm nay cho `href` tuỳ ý (spec rào 3). Chữ model có thể chứa link Markdown `[x](…)`, tên miền trần (`abc.vn`, `www.…`) hoặc `http` không dấu `//`.
- **Tiêu chí đóng:** D5 (ii) ghi mẫu gồm `https?://`, `www.`, tên miền trần có đuôi phổ biến, và link Markdown. Ca test đoạn trích cài lệnh ở §3 dùng ít nhất một dạng không có `https://`.

### m-4 — Tiền / câu ở đường web vượt yêu cầu phi chức năng; nên ghi thành giới hạn

- **Bằng chứng:** User chốt ≤ 0,0005 USD / câu (`Project_Status.md` §1). Plan §7 tính một lượt có web ≈ 0,0005 (kho) + 0,0003 (mục web) + 0,001 (Serper trả phí) ≈ 0,0018, tức ~3,6 lần sàn. Khi còn lượt dùng thử thì ≈ 0,0008.
- **Tiêu chí đóng:** §10 thêm một dòng: "câu có web vượt sàn tiền / câu; chỉ xảy ra ở câu kho từ chối". Q5 báo USD / câu riêng cho đường web, để A báo User.

### m-5 — Số kiểm bộ đo trong plan đã cũ

- **Bằng chứng (chạy `md5sum` / `sha256sum`):**
  - `cau_da_thay.jsonl`: md5 hiện `6ed74db21616`, 28 câu (README đã ghi, gồm L01). Plan §5 vẫn ghi `9be5c35dcb29` / 27 câu, vì bước 1 đã làm sau khi viết plan.
  - `web_neu_ten.jsonl`: `2219b5c65237` là **sha256**; md5 là `03c313e81642`. README ghi nhầm "md5 `2219b5c65237`".
  - Kín: README ghi md5 `4de04132600b` (11 câu); plan ghi `b85d5d0351f4` (10 câu). Mình không tự kiểm vì không mở file kín.
- **Tiêu chí đóng:** cập nhật §5 theo README sau bước 1, ghi rõ loại băm. Không cần mở vòng sửa riêng.

**Không có finding ở:** cổng một chỗ cho 3 đường (D1, có `answer_turn_stream_parallel`); truy vấn chỉ từ câu lượt này (D2); một module, không thử lại (D3); lần gọi riêng không công cụ / không lịch sử / không kho (D4); không nói giá phòng do code (D5 (iii)); cắt mục web ở `stored_answer`, đúng chỗ đã ghi sẵn trong code (D7); trần (D8); log không chữ (D9); bảng rà FDE §9; có bộ kín vì chỉnh `TU_WEB_LUAT` nhiều vòng (đúng luật 05/11 (2)); trần tiền và điều kiện dừng. Độ phức tạp tương xứng: không thấy cơ chế phòng xa.

## 3. Cách người kiểm chạy lại thật

```bash
sha256sum docs/superpowers/plans/2026-11-05-phase-9-b6-plan.md docs/superpowers/specs/2026-11-02-phase-9-design.md | cut -c1-12
md5sum data/phase_9/bo_do_b6/cau_da_thay.jsonl data/phase_9/bo_do_b3/web_neu_ten.jsonl; sha256sum data/phase_9/bo_do_b3/web_neu_ten.jsonl
wc -l data/phase_9/bo_do_b6/cau_da_thay.jsonl   # + đếm `loai` bằng python (chỉ khoá / số đếm, không in câu)
grep -n 'REFUSAL_ANSWERS\|refusal_no_sources\|def stored_answer\|def tim_so_tien\|ALLOWED_ATTR\|def fake_create' <các file ở §1>
```

0 USD, không gọi API, không đọc Qdrant.

## 4. Kết quả quan sát

- sha plan `b6a046e944c0` và sha spec `77250689e605` khớp.
- Bộ đã thấy có 28 câu: 10 `web_tra_loi_duoc` · 6 `khong_xac_minh` · 4 `ngoai_hue` · 4 `kho_co` · 2 `theo_ngay` · 2 `ten_trong_cau` (khớp README; lệch plan, xem m-5).
- Mọi hàm / chỗ plan dựa vào đều có trên `main`; `stored_answer` có sẵn dòng "Chỗ cắt mục 'Từ web' của B6 đặt ở đây".
- Bằng chứng cho M-1, m-1, m-2 như ở §2.

## 5. Giới hạn hoặc phần chưa chạy

- Không kiểm bộ kín (md5, cỡ) và không chạy `kiem_bo.py`, vì cả hai đều đọc file kín.
- Không kiểm điều khoản Serper trên web (spec đã ghi User chấp nhận rủi ro; luật 05/11 (5): dữ liệu công khai cho học tập không kiểm giấy phép).

## 6. Decision và bước tiếp theo

`changes_requested`. Sửa M-1 (cần A chốt cách tính) và m-1, m-2 ở bản 3; m-3 đến m-5 sửa cùng lúc hoặc khi code. Vòng 2 (cuối): B kiểm phần sửa. Nếu chỉ còn minor thì A duyệt.

---

# Vòng 2 (cuối) — bản 3 sha `6e5c3b21065d`

Decision: **ready** — 0 blocker · 0 major · 0 minor mới ⇒ theo luật ≤ 2 vòng, A duyệt.
Người kiểm: B · Date: 19:33 05/11/2026 (`date`). Chỉ kiểm phần đổi (diff bản 2 `b6a046e944c0` ↔ bản 3) + 2 dòng C sửa trong `data/phase_9/bo_do_b6/README.md`.

| Finding | Kết quả | Bằng chứng |
|---|---|---|
| M-1 | **đóng** | Q4 bỏ "≤ 2 %"; dùng "từ chối nhầm ≤ mốc + 1" (theo spec §4, A chốt), có ghi trước mẫu số (Golden 30 + câu an toàn `in_kho: true`) và cách đếm mốc (lượt cờ tắt của B5 Q4, đếm 0 USD trước lượt cờ bật; 11 file sửa kho của C192 dùng lượt "sau"). Câu cổng không mở được gắn nhãn [suy ra từ Q1m + test]. Thêm sàn: mục web của câu kho có không được trái kho. Plan tự ghi rằng sàn này chỉ phạm khi cổng làm hỏng câu trả lời kho — đúng như phân tích ở vòng 1. |
| m-1 | **đóng** | D1: chỉ `INSUFFICIENT_ANSWER`, so sau `strip()`, `refusal_no_sources` ⇒ mở; §3 có 4 ca theo từng nhánh. |
| m-2 | **đóng** | Q1m ghi rõ chỉ chứng minh phần trước cổng; lượt chụp không có khoá Serper; §3 có test thiếu khoá ⇒ `web_loi`, không gọi mạng. |
| m-3 | **đóng** | D5 (ii) có mẫu bắt `https?://`, `www.`, tên miền trần, link Markdown; test cài lệnh có dạng không dùng `https://`. |
| m-4 | **đóng** | §10 thêm rủi ro tiền; Q5 báo USD / câu riêng cho đường web; sàn là trung bình mọi câu (A chốt). |
| m-5 | **đóng; rút ý mã băm** | Phản biện của C **đúng**: B chạy lại, `md5sum web_neu_ten.jsonl` ⇒ `2219b5c65237`, `sha256sum` ⇒ `03c313e81642`. Vòng 1 B đã đọc nhầm thứ tự dòng in ra; README đúng. §5 cập nhật 28 / 11 câu, md5 `6ed74db21616`. |

README bộ đo (C sửa ngoài plan): dòng "Quyết" (6 / 10 · 5 / 7) và dòng "Từ chối nhầm ≤ mốc + 1" khớp bản 3 Q3 / Q4. Không thấy thay đổi ngoài phạm vi.
