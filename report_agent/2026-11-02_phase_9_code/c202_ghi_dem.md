# Report: C202 — tắt ghi đệm prompt OpenAI (`prompt_cache_options.mode = "explicit"`): **KẾT QUẢ ÂM, không đề xuất bật**

Người làm: C (Claude Opus 5.5, `hue-rag-3c`) · A giao 05/11 tối · Date: 20:59 05/11/2026 (`date`)
Tiêu chí ghi trước: `data/phase_9/c202_ghi_dem/tieu_chi.md` (20:36, trước lượt có phí). Dữ liệu (private): `data/phase_9/c202_ghi_dem/`. Không merge.

## 1. Câu hỏi và căn cứ

- **Câu hỏi:** C126 (02/11) thấy câu trả lời ghi đệm gần hết phần vào mà không lần nào đọc lại, ⇒ phụ phí ≈ 13 % tiền / lượt. Tắt ghi đệm có rẻ hơn không?
- **Tài liệu OpenAI [WebFetch 05/11]:** "When no explicit breakpoints are placed, the request does not use prompt caching or create cache writes" (GPT-5.6 trở lên). Ghi 30 phút = 1,25× giá vào; đọc rẻ 90 %.
- **SDK:** `openai-agents` 0.19.4 có sẵn `ModelSettings.prompt_cache_options`, truyền thẳng vào `responses.create` (`agents/models/openai_responses.py:891`) — không cần `extra_args`.

## 2. Thay đổi thử (worktree `/tmp/c202` từ `main` `e14cc03`; bản vá `data/phase_9/c202_ghi_dem/patch.diff`)

- Cờ `full_corpus_generation.prompt_cache_explicit` (mặc định `false`) ⇒ `ModelSettings(prompt_cache_options={"mode": "explicit"})` cho agent định tuyến + agent trả lời. Agent trợ lý và bản có lịch sử là bản sao nên ăn theo.
- Cờ tắt truyền `None` ⇒ SDK bỏ tham số.

## 3. Đã chạy

```bash
# G2 (0 USD): capture_all trên main e14cc03 và trên worktree cờ tắt ⇒ cmp
# lượt có phí: từ /tmp/c202/backend, --env-file tuyệt đối
python -m evaluation.full_corpus_eval generate --golden smoke --cases 2 23 41 43 54 --out …/tat.jsonl   # cờ tắt
# sửa settings.yaml worktree prompt_cache_explicit: true ⇒ cùng lệnh ⇒ …/bat.jsonl ; trả cờ về false
```

Lần chạy đầu ghi `--cases 0 1 2 3 4` sai: đó không phải số Golden của bộ smoke, nên `KeyError` ngay ở bước chọn câu, trước mọi lần gọi API (0 USD). "5 câu đầu của bộ smoke" là case 2, 23, 41, 43, 54.

## 4. Kết quả theo tiêu chí ghi trước

| Mã | Tiêu chí | Kết quả |
|---|---|---|
| **G1** sàn | cờ bật: mọi lần gọi `cache_write_tokens` = 0 | **ĐẠT** — 0 / 10 lần gọi (định tuyến 5 · trả lời đầu 4 · gọi sau 1) |
| **G2** sàn | cờ tắt giống byte `main` | **ĐẠT** — `capture_all` 228 / 228, `cmp` giống |
| **G3** quyết | tiền / câu bật < tắt | **KHÔNG ĐẠT** — 0,0003149 > 0,0003045 USD / câu. Phía bật có 1 câu model tự gọi tìm thêm (thêm 1 lần gọi). Phần so được cùng số lần gọi: trả lời đầu 0,0010877 ⇒ 0,0008797 (−19 %); định tuyến **không ghi đệm ở cả hai phía** (phần vào < 1.024 token) ⇒ explicit không đổi gì |
| **G4** sàn | ms định tuyến + trả lời đầu không chậm > 30 % trung vị | **ĐẠT** — trung vị 4.181 ⇒ 4.717 ms (+13 %, trong nhiễu 5 câu) |
| **G5** smoke | không đổi loại câu trả lời ≥ 4 / 5 | **ĐẠT** — 5 / 5 cùng tuyến, cùng trả lời / từ chối |

**Phát hiện quyết định (0 USD, từ dữ liệu đã lưu — 78 lượt `tro_ly_hue` trong `data/sua_kho_2026-11-05_gio/`, `data/phase_9/b5/q4/`, `data/phase_9/b5c/q4/`, `tat.jsonl`):**
- **45 %** lượt (35 / 78) gọi model trả lời ≥ 2 lần (tìm thêm `tim_kho`).
- **46 / 46** lần gọi sau đều **đọc đệm**: 121.083 / 148.803 token vào = **81 %** tính giá đọc (0,01 thay vì 0,10 USD / 1M).
- ⇒ Ghi đệm ở lần gọi đầu là cái giá để lần sau đọc rẻ. C126 thấy 0 lần đọc vì đo 02/11, **trước khi bật tìm thêm** (B2, 03/11).
- Tính tiền phần vào trên 78 lượt (giá User 30/10):
  - hiện nay (implicit) **0,027294 USD**;
  - explicit **0,032982 USD** ⇒ **đắt hơn 21 %** (+0,000073 USD / lượt).
  - [suy ra từ token đã đo; giả định explicit tính mọi token vào ở giá thường]

## 5. Kết luận và đề xuất

- **Không bật explicit.** Với tìm thêm đang bật, explicit làm mất phần đọc đệm ở gần nửa số lượt ⇒ tốn hơn, không rẻ hơn. Biến thể "chỉ định tuyến explicit" vô ích: định tuyến vốn không ghi đệm.
- Phụ phí 13 % của C126 chỉ đúng cho lượt một lần gọi. Hoà vốn ước khi tỉ lệ lượt nhiều lần gọi ≈ 28 % [suy ra]; hiện 45 %.
- Giữ cờ thử ngoài `main`; bản vá lưu ở `data/` làm hồ sơ. Nếu sau này tắt tìm thêm hoặc tỉ lệ lượt nhiều lần gọi < ~25 % ⇒ xét lại (cùng tiêu chí).

## 6. Tiền, giới hạn

- **Tiền:** 0,003097 USD (2 × 5 câu) / trần 0,01.
- 5 câu mỗi bên chỉ thấy khác biệt lớn. G3 bị nhiễu số lần tìm thêm (đúng loại nhiễu đã biết); phần quyết định là phép tính trên 78 lượt đã đo, không phải 5 câu này.
- Giá đọc / ghi theo bảng giá User đưa 30/10; giờ đo không gồm HTTP / trình duyệt (harness không stream).
- Worktree `/tmp/c202` gỡ được.
