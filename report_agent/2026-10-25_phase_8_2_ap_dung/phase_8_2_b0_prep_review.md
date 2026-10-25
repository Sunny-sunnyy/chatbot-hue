# Review: Phase 8.2 B0 — chuẩn bị file đọc cặp mù (B24)

Decision: **changes_requested**
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-de`)
Date: 2026-10-25 16:28 +0700 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` (sha `dabae90b2b60`) §3.3, §3.4, §5 B0
Implementation report: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md` (A, 16:24)

Không chép câu hỏi / câu trả lời / tên nguồn; chỉ số câu, số dòng, số đếm, sha. 0 USD, chỉ đọc.

## 1. Phạm vi đã review

- Report B0 prep (toàn bộ), script `data/phase_8_2/b0/tools/make_pairs.py` (toàn bộ), `mau.json`, `khoa.json`, `doc_cap_mu.md`
  (đọc bằng code; B không đọc nội dung từng câu ngoài 3 dòng bị cờ quét lộ).
- Đối chiếu: `backend/retrieval/full_corpus_context.py:88-112` (vòng đóng gói — thứ tự nguồn), điểm judge 8.1 qua
  `experiments.phase_8_1.g2_generate.attach_labels` (đường đọc điểm của chính G2, độc lập với hàm `judge_scores` của script).
- Không mở file `*sealed*`; không đưa nội dung file ra ngoài.

## 2. Findings

Không có blocker. **1 major, 2 minor.**

**F1 (major) — mù hình thức bị lộ ở câu 17: citation dạng `[Nguồn n]` không được đánh số lại.**
- Vị trí: `make_pairs.py` — `CITE = re.compile(r"\[(\d+)\]")` dùng cho cả `renumber` lẫn phần kiểm mù; `doc_cap_mu.md` dòng 289
  (câu 17, bên X), dòng 135, 137 (câu 8, cả X và Y).
- Yêu cầu: spec §3.3 "Giữ mù hình thức … đánh số lại citation … chỉ hiện các nguồn được trích. Kiểm bằng code …"; report §6 (2)
  "không chuỗi nào lộ bản (ví dụ `[6]`–`[10]`)".
- Bằng chứng: quét mọi cụm `[…số…]` trong file đưa User: 6 cụm không phải dạng `[n]`, đều dạng `[Nguồn n]` (model tự viết kiểu
  citation khác). Câu 17 bên X có `[Nguồn 5]` và **`[Nguồn 8]`**; theo khóa, câu 17 bên X **là context 10** ⇒ số 8 chỉ có thể ở bản
  context 10 ⇒ lộ bên. Câu 8 (tầng hòa): X `[Nguồn 2]`, `[Nguồn 3]`; Y `[Nguồn 2]`, `[Nguồn 3]` — không lộ bên, nhưng các câu trả lời
  này không có `[n]` nên **không có dòng "Nguồn:"** ⇒ User thấy trích dẫn tới nguồn không được hiện, và số giữ nguyên số gốc (không
  đánh số lại). Phần kiểm mù của script báo `cite_gt_shown 0`, `max_cite_in_doc 3` vì chỉ đếm dạng `[n]`.
- Tác động: câu 17 thuộc tầng judge chấm context 10 hơn — đúng loại cặp quyết của luật dừng §3.4; User có thể nhận ra bên context
  10 ở câu đó (và nếu đoán được quy luật, ở các câu khác).
- Tiêu chí đóng: (1) `renumber` nhận cả dạng `[Nguồn n]` (không phân biệt hoa thường; đổi về cùng một dạng `[k]` hoặc giữ chữ
  "Nguồn" nhưng số mới) và đưa nguồn tương ứng vào dòng "Nguồn:"; (2) phần kiểm mù quét mọi số trong ngoặc vuông và mọi cụm
  "nguồn <số>" (không phân biệt hoa thường), báo 0 số > số nguồn hiện; (3) chạy lại, ghi sha mới của `doc_cap_mu.md` / `khoa.json`;
  B kiểm lại bằng cùng phép quét (`/tmp/b24/check.py` + quét ngoặc vuông).

**F2 (minor) — lệch spec §3.3 về người xếp X / Y: chấp nhận được.** Spec ghi "một sub-agent không thấy điểm judge xếp X / Y";
A dùng `random.Random(20261025)` trong script. Mục đích của câu spec là người xếp không chọn bên theo điểm; xếp ngẫu nhiên có seed
đạt cùng mục đích, tái lập được (B chạy lại ra đúng sha), và A vẫn chỉ giữ khóa. Đóng: khi trình User B0, A ghi một dòng về lệch
này (spec đã User duyệt) — không cần sửa code.

**F3 (minor) — ghi chú cỡ mẫu theo loại câu.** Mẫu 20 câu: `direct_fact` 9, `comparative` 6, `conditional` 4, `multi_source` **1**;
8.1 thấy context 10 lợi chủ yếu ở nhiều nguồn / so sánh (`phase_8_1_g5_by_category.md`). Không trái spec (spec chia tầng theo điểm
judge, không theo loại). Đóng: report B0 ghi phân bố này vào giới hạn để User / A đọc kết quả mốc người đúng phạm vi.

## 3. Cách người kiểm chạy lại thật

```bash
# chạy lại script, ghi ra /tmp (không ghi đè file của A)
uv run python -I -c "import importlib.util, pathlib; s=importlib.util.spec_from_file_location('mp','data/phase_8_2/b0/tools/make_pairs.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.OUT=pathlib.Path('/tmp/b24_out'); m.main()"
sha256sum /tmp/b24_out/* data/phase_8_2/b0/{doc_cap_mu.md,khoa.json,mau.json}
# kiểm độc lập (chỉ in số đếm)
cd backend && HF_HUB_OFFLINE=1 uv run python -I /tmp/b24/check.py
# quét mọi cụm […số…] không phải dạng [n] (in cụm ngoặc + số dòng, không in câu)
```

## 4. Kết quả quan sát

| Kiểm (report §6) | Kết quả | Đạt |
|---|---|---|
| Chạy lại script | `doc_cap_mu.md` `8e8a1e42b784`, `khoa.json` `5b9240842b7b`, `mau.json` `365c363b04c7` — giống hệt file của A | ✓ |
| (1) không câu kín | 20 `case_index` khác nhau, đều là vị trí trong Golden chính thức (kiểm `case_index` == vị trí dòng: 176 / 176); script chỉ đọc Golden + G2; không file `*sealed*` nào trong `data/phase_8_2/b0/` | ✓ |
| Lọc | 0 câu `out_of_scope`, 0 câu `unnatural` (natural 10, capability_only 10); dev / test trong khóa khớp `split.json` 20 / 20 | ✓ |
| (3) tầng / quota | tính lại độc lập qua `attach_labels`: kho 10 hơn **15**, hòa **93**, 10 kém **3** — khớp `mau.json`; chênh Completeness + tầng trong khóa: **0** câu lệch; mẫu 10 / 7 / 3, dev 12 / test 8 | ✓ |
| Ánh xạ tên nguồn (giới hạn A ghi ở §5) | `context_sources` của 40 câu trả lời trong mẫu: 20 bản context 5 đều 5, 20 bản context 10 đều 10 ⇒ không đoạn nào bị bỏ; vòng đóng gói duyệt `documents` theo thứ tự (`full_corpus_context.py:94-111`) ⇒ nguồn `[n]` = `top_chunk_ids[n−1]` đúng | ✓ (giả định của A được chứng minh) |
| Chữ câu trả lời | bỏ citation thì 40 / 40 câu trả lời trong file giống hệt bản gốc G2 | ✓ |
| (2) mù hình thức | dạng `[n]`: 0 số > 3, 0 số > nguồn hiện; 0 chuỗi "context / ngữ cảnh / baseline / biến thể / g2 / dev / test / 5 nguồn / 10 nguồn"; **6 cụm `[Nguồn n]` không được xử lý, 1 cụm lộ bên (câu 17)** | ✗ — F1 |
| X / Y | context 10 ở X 12 / 20 | ✓ |
| (4) lệch spec | xem F2 | chấp nhận |

## 5. Giới hạn hoặc phần chưa chạy

- B không đọc toàn văn 20 câu để tìm dấu hiệu lộ bằng nghĩa (ví dụ câu trả lời nhắc số lượng nguồn bằng chữ); chỉ quét bằng mẫu
  chuỗi. Độ dài / độ đủ khác nhau là khác biệt thật, không phải lộ.
- B là người làm B1 (dùng lại G2.1a) và từng chạy G2 8.1; B đã thấy khóa khi kiểm ⇒ **B không được làm người tóm nhãn** nhận xét
  của User (spec §3.4 đã ghi sub-agent mới).

## 6. Decision và bước tiếp theo

**changes_requested** — F1 (major) phải sửa trước khi đưa file cho User; F2, F3 minor (ghi chú, không mở vòng riêng).
Correction: A sửa `renumber` + phần kiểm mù theo tiêu chí đóng F1, chạy lại, ghi sha mới vào report B0 prep; nhắn B. B kiểm lại
bằng cùng phép quét; dùng lại các kiểm (1), (3), ánh xạ nguồn, chữ câu trả lời nếu mẫu không đổi (cùng seed ⇒ cùng 20 câu — B kiểm
`khoa.json` phần `case_index` / tầng không đổi).

## 7. Vòng 2 — kiểm phần sửa F1

Người kiểm: B (`hue-rag-de`) · 2026-10-25 16:32 +0700 (`date`) · 0 USD, chỉ đọc. Bản: `make_pairs.py` `b8ecd4177d0d`,
`doc_cap_mu.md` `37b66efb3499`, `khoa.json` `5b9240842b7b` (không đổi).

| Kiểm | Kết quả | Đạt |
|---|---|---|
| Chạy lại script (ghi `/tmp/b24_out2`) | 3 sha giống hệt file của A; script tự kiểm: `cite_gt_shown 0`, `odd_bracket_or_nguon_word 0`, số lớn nhất `[3]` | ✓ |
| Quét độc lập mọi cụm ngoặc vuông có số | 136 cụm, **0** cụm không phải dạng `[n]`; số lớn nhất 3 | ✓ |
| "nguồn <số>" (không phân biệt hoa thường) ngoài dòng "Nguồn:" | 0 | ✓ |
| Mỗi câu trả lời: số `[k]` liên tục 1..m và m = số nguồn trên dòng "Nguồn:" | 40 / 40 đúng (`/tmp/b24/check2.py`) | ✓ |
| Chữ câu trả lời (bỏ mọi dạng citation, so bản gốc G2 sau NFC) | 40 / 40 giống | ✓ |
| Mẫu không đổi | khóa cùng sha ⇒ cùng 20 câu, cùng tầng, cùng X / Y; dùng lại kiểm (1), (3), ánh xạ nguồn của vòng 1 (đầu vào không đổi) | ✓ (dùng lại) |
| F2, F3 | A ghi vào report B0 prep §5 | ✓ |

**Kết luận vòng 2: ready_for_user_confirmation** — F1 đóng; F2, F3 đóng (ghi chú). File đưa User: `doc_cap_mu.md` sha
`37b66efb3499`. Nhắc lại: B đã thấy khóa ⇒ không làm người tóm nhãn. Script tạm của B ở `/tmp/b24/` (không phải việc câu kín; xóa khi
kết phiên).
