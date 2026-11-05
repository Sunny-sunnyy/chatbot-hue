# Implementation Report: Phase 10 G0 — model nghe (nói ⇒ chữ) chạy bằng sherpa-onnx

Người làm: E (Claude Opus 5.5, `hue-rag-bc`) · việc **E16** (A giao)
Date: 21:16 05/11/2026 (`date`)
Spec: `docs/superpowers/specs/2026-11-05-phase-10-design.md` bản 4 `784d6f7abd9f` (User duyệt §12 (7) `sherpa-onnx`, (8) tải 2 model ≤ 300 MB, (10) thu 40 câu; (9) Web Speech **bỏ**) — §8.3 bậc **G0**.
Nhánh: `p10-giong-noi` từ `main` `7ff8e5a`, commit **`93bbc63`** (đã push), worktree `/tmp/e_giong`. Không code route / giao diện (đúng G0). **0 USD.**

## 1. Phạm vi

`uv add sherpa-onnx` · tải Gipformer 68M int8 + Zipformer-30M int8 · chạy file mẫu ⇒ ghi: chạy được không, dạng đầu ra (hoa / dấu câu / số), hotwords + `modified_beam_search`, RAM / ms một câu. **Không** đo chất lượng (cần bộ 40 câu — G1 / G2).

## 2. Thay đổi

| Đường dẫn | Việc |
|---|---|
| `pyproject.toml` (+1) · `uv.lock` (+64) — nhánh | `sherpa-onnx>=2.0.1`; lock thêm **đúng 2 gói** `sherpa-onnx` 2.0.1 + `sherpa-onnx-core` 2.0.1, **không đổi gói nào khác** (diff lock 0 dòng xoá). Wheel cp313 Linux x86_64 4,3 MB; **phát hành 26–27/10/2026** (≈ 10 ngày trước lúc thêm — luật "≥ 2 tuần" hiện chỉ có ở `frontend/.npmrc`, Python chưa có luật; ghi để A / User biết). Gói tự mang ONNX Runtime riêng (không cần gói `onnxruntime`) |
| `.venv` chung của dự án | cài bằng `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen` từ worktree ⇒ **chỉ thêm 2 gói**, không gỡ gì, không tạo venv thứ hai. `uv run` từ `main` (lock chưa có gói) không gỡ gói này (đã kiểm: import được sau `uv run` của `main`). Khi nhánh merge thì lock `main` có gói |
| `data/phase_10/giong_noi/models/` (private, gitignore — `git check-ignore` OK) | `gipformer_68m/` — HF `g-group-ai-lab/gipformer-68M-rnnt` ghim commit `318322b009200f8e`, chỉ bản int8 (`encoder.int8.onnx` 70,9 MB sha256 `3cc1a719f04d`, `decoder.int8.onnx`, `joiner.int8.onnx`, `tokens.txt`, `bpe.model`, `config.json`, `README.md`); `zipformer_30m/` — gói sherpa `sherpa-onnx-zipformer-vi-30M-int8-2026-02-09` (GitHub release `asr-models`, 26,4 MB sha256 `da8b63794709…`, giải nén bằng `tarfile` `filter="data"`, xoá file nén; `encoder.int8.onnx` sha256 `8ef5286dd427`) ⇒ **tổng 108 MB** (≤ 300 MB đã duyệt). Mỗi model một thư mục rỗng riêng; script chạy với `python -I` từ ngoài thư mục tải |
| `data/phase_10/giong_noi/tools/g0.py` (private, sha256 `7c12c8dd5fe3`) | đo: đọc WAV bằng `wave` (như route G5 sẽ làm), `OfflineRecognizer.from_transducer`, mỗi cấu hình một tiến trình (RSS riêng); `bpe.vocab` xuất từ `bpe.model` bằng `sentencepiece` (sherpa cần cho hotwords `modeling_unit=bpe`) |
| `data/phase_10/giong_noi/g0_ket_qua.jsonl` | 10 dòng kết quả |

## 3. Cách chạy

```bash
cd /home/minhhieu/hue_rag
uv run python -I data/phase_10/giong_noi/tools/g0.py <gipformer|zipformer> <1|2|4> <greedy_search|modified_beam_search> [hotwords]
```
Âm thanh: 3 file mẫu kèm gói Zipformer (`test_wavs/0–2.wav`, 1,55–3,74 s, câu nói thường — nguồn mẫu của wav2vec2-vi; **không có lời chép chuẩn kèm** ⇒ không tính WER). Hai model chạy cùng 3 file. File đầu chạy 2 lần, chỉ tính lần 2 (khởi động).

## 4. Kết quả quan sát [Chạy]

**Chạy được bằng sherpa-onnx: CÓ — cả hai** (Gipformer `config.json` ghi `"library": "sherpa-onnx"`; `from_transducer` nạp encoder / decoder / joiner int8 không lỗi).

| Model | Luồng | Cách giải mã | Nạp | RSS đỉnh | ms: 3,74 s · 2,40 s · 1,55 s âm thanh |
|---|---|---|---|---|---|
| Gipformer 68M | 1 | greedy | 4,0 s (lần đầu, đĩa lạnh) | 226 MB | 234 · 92 · 60 |
| Gipformer 68M | **2** | greedy | 2,2 s | 225 MB | **108 · 62 · 44** |
| Gipformer 68M | 4 | greedy | 2,0 s | 226 MB | 135 · 85 · 55 |
| Gipformer 68M | 2 | modified_beam | 2,2 s | 225 MB | 135 · 110 · 50 |
| Gipformer 68M | 2 | modified_beam + hotwords | 1,9 s | 229 MB | 126 · 73 · 53 |
| Zipformer-30M | 1 | greedy | 1,2 s | 179 MB | 109 · 65 · 36 |
| Zipformer-30M | **2** | greedy | 1,4 s | 179 MB | **72 · 52 · 37** |
| Zipformer-30M | 4 | greedy | 1,4 s | 178 MB | 95 · 55 · 39 |
| Zipformer-30M | 2 | modified_beam | 1,3 s | 179 MB | 114 · 68 · 46 |
| Zipformer-30M | 2 | modified_beam + hotwords | 1,7 s | 180 MB | 90 · 65 · 45 |

- **Tốc độ / RAM:** mọi cấu hình ≤ 234 ms cho câu 3,7 s (RTF ≤ 0,063; 2 luồng ≈ 0,03) — **dưới xa** V-d (p95 ≤ 1,5 s câu ≤ 10 s; RAM ≤ 1,5 GB). 4 luồng **chậm hơn** 2 luồng (máy đang chạy việc khác; mẫu nhỏ) ⇒ đề xuất **2 luồng** ghi trước ở plan. Ba file — chỉ là con số định hướng, V-d đo ở G2 trên 40 câu.
- **Dạng đầu ra:** **chữ HOA, không dấu câu** ở cả hai (3 / 3 câu). Từ vựng (đếm `tokens.txt`, 2.000 mảnh BPE mỗi model): **Gipformer 0 mảnh chữ số, 0 dấu câu** ⇒ số luôn ra **bằng chữ**; **Zipformer có 10 mảnh chữ số `0–9` + `. , !`** ⇒ có thể ra chữ số / viết tắt — thấy thật: câu 3 Zipformer ra "**TV**", Gipformer ra "**TI VI**" (hai câu kia giống hệt nhau). ⇒ hàm chuẩn hoá số (spec §8.5 m-1) phải nhận cả chữ lẫn chữ số; giao diện điền vào ô gõ nên đổi chữ HOA ⇒ viết thường / hoa đầu câu (việc của G3).
- **Tất định:** 1 / 2 / 4 luồng, greedy / beam ⇒ cùng chữ ở mỗi model (5 / 5 cấu hình).
- **Hotwords + `modified_beam_search`: chạy được ở cả hai** (cần `modeling_unit="bpe"` + `bpe_vocab`; `greedy_search` không hỗ trợ — đúng tài liệu sherpa [Codex]). Dò tác dụng (đổi một chữ trên câu 3):
  - Zipformer, hotword "TI VI": điểm 0 / 1,5 / 3,0 ⇒ vẫn "TV"; điểm **8,0 / 20,0 ⇒ "TI VI"** (có tác dụng, cần điểm cao).
  - Gipformer, hotword "TV": điểm **3,0 / 8,0 ⇒ "TV"**; điểm **20,0 ⇒ "TV TV" (chèn lặp)**.
  - 6 tên Huế làm hotwords (điểm 1,5) trên 3 câu không có tên ⇒ **0 chèn** (mẫu quá nhỏ).
  ⇒ **điểm hotwords khác nhau giữa hai model và điểm cao gây chèn sai thật** ⇒ G2 chọn điểm trên bộ 40 câu, đo **cả** V-a (tên đúng) **và** V-e (chèn tên sai) như spec — không đặt điểm cố định từ G0.

## 5. Lỗi và giới hạn

- 3 file mẫu, câu nói thường, **không** giọng Huế, **không** tên riêng, **không** có lời chép chuẩn ⇒ G0 **không** nói gì về chất lượng; chỉ về chạy được / dạng / tốc độ / RAM.
- Số ms đo khi máy có việc khác (RAM trống ~7 GB lúc chạy); mỗi ô một lần.
- Gói sherpa-onnx 2.0.1 mới ≈ 10 ngày (xem §2).
- Gipformer: giấy phép MIT (card); Zipformer-30M: CC-BY-NC-ND-4.0 (card) — thông tin, không kiểm (luật 05/11).

## 6. Bàn giao / bước tiếp

- **G1** (User + ≥ 1 người giọng Huế / Trung thu 40 câu do C soạn, spec §8.4) ⇒ **G2** đo hai model (2 luồng; greedy vòng 0; hotwords ở vòng chỉnh, chọn điểm theo V-a + V-e) ⇒ G3 route.
- Plan G2 nên ghi trước: 2 luồng; hàm chuẩn hoá số nhận chữ + chữ số (Zipformer ra chữ số / viết tắt); dải điểm hotwords thử (vd 2 / 4 / 8) cho từng model.
- Người kiểm chạy lại rẻ nhất: lệnh §3 (≈ 3 s / cấu hình, 0 USD); diff nhánh `git diff main p10-giong-noi` (2 file).
- **Giải thích ngắn:** đã cài thư viện nghe chạy trên máy và tải 2 model nhỏ (108 MB); cả hai chạy được, nghe một câu 4 giây mất khoảng 0,1 giây, tốn ~200 MB RAM; ra chữ in hoa không dấu câu; chức năng "ưu tiên tên riêng" chạy được nhưng phải chỉnh mức cho khéo, mức quá cao làm chèn chữ lặp.
