# Review: rà code B25 — kiểm chéo 5 mục (B-11, B-12, B-16, B-17, B-20)

Decision: **ready_for_user_confirmation** — 5 / 5 mục đứng được. Có 3 điều chỉnh mức `minor` để B ghi lại trong `ra_soat_code_B.md`
(B-11 mức, B-12 phạm vi, B-17 một khẳng định). Không có blocker, không có major.
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-7f`)
Date: 2026-10-25 18:5x (`date` 18:53)
Canonical: mục "Việc đang mở → Rà code" trong `session_prompt/CURRENT_HANDOFF.md`; A giao 18:4x ("làm đi": 5 mục; B-01 = C-01 coi như đã kiểm chéo)
Implementation report: `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` (B25, chốt 18:39)

## 1. Phạm vi đã review

- Chỉ dựa vào `ra_soat_code_B.md` (5 mục được giao) + code + `data/`. Không đọc `STATUS_B`. Không chạy script của B (`/tmp/b25/*`) hay file
  sub-agent của B (`data/ra_soat_code/sa*.md`). Chỉ đọc, 0 USD, không sửa code / test / guide. Test chỉ liệt kê file, không `--env-file`.
- Git: `main` `c272644` (A vừa commit docs; code không đổi so với nền `1e8cf8f` của B). Mọi script kiểm của C do C tự viết, để
  `/tmp/c34x/`, bản dùng lại ở `data/ra_soat_code_2026-10-25/tools/kiem_cheo_C/` (private). Chỉ in số đếm, không in nội dung kho.
- Code đã đọc: `ingestion/chunking/full_corpus_chunker.py:302-345, 344-642, 644-705`; `ingestion/full_corpus_pipeline.py:97-100, 115-135`;
  `ingestion/preview.py:132-210`; `embedding/full_corpus.py:210-225`; `retrieval/full_corpus.py:761-795`; `api/app.py:92-120`;
  `llm/generator_openai_full_corpus.py:155-180`; test `test_full_corpus_chunker.py:66-108, 850-1050`, `test_api_chat.py:28-93`,
  `test_openai_full_corpus_generator.py:22-60`, `test_phase6_live_smoke.py:120-150`, `test_full_corpus_embedding.py`; guide `phase_0`–`phase_4`,
  `README.md`, `full_corpus_rag.md:114-115`; notebook 03 cell 6.

## 2. Findings

Tóm tắt từng mục:

| Mục | Khẳng định của B | Kết luận | Mức B ghi | Mức hợp lý? | Phương án sửa |
|---|---|---|---|---|---|
| B-11 | build không chặn đoạn vượt; test chặn PASS bất kể code; 0 / 8.459 vượt | **đúng** (nói chính xác hơn ở 1 test) | cao | **đề xuất vừa** (R1) | đủ; thêm 1 ý (R2) |
| B-12 | file tracked chứa nguyên văn kho 5.324 ký tự + test mẫu | **đúng**; phạm vi rộng hơn (R3) | vừa | hợp lý | đủ; thêm phần đo |
| B-16 | guide 0–4 + README tả hệ thống đã gỡ như đang chạy | **đúng** | vừa | hợp lý | đủ; một điều kiện cho cách đo |
| B-17 | lệnh thiếu `uv run` / `--env-file`; `pytest tests/` chạy test cần key "có `POST /api/chat` thật" | **một phần** (R4) | vừa | **đề xuất thấp** | đủ |
| B-20 | test so build record chỉ bằng số đoạn; chậm vì CLI preview; ghim hằng số kho | **đúng** | vừa | hợp lý | đủ |

### B-11 — đúng

- **"Build không chặn":** đúng bằng đọc code và chạy thật. `chunk_document` nhánh "không tách được" phát nguyên đoạn kèm comment
  `# Unbreakable unit: emit whole chunk so preview can detect it` (`full_corpus_chunker.py:566-579`, comment ở `:568`); nhóm câu luôn nhận câu đầu
  (`:582-628`); vòng kiểm cuối (`:630-641`) chỉ kiểm `search_text` rỗng + lát cắt, không kiểm token; `full_corpus_pipeline.py:126-128` chỉ dừng khi
  `errors` khác rỗng. Script C (`b11_check.py`, chunker production + 3 tokenizer thật, file thử dựng trong bộ nhớ, không đọc / sửa kho):

  | Input | đoạn | vượt | `errors` | token lớn nhất (e5-small / e5-base / huydang) | giới hạn |
  |---|---:|---:|---:|---|---|
  | một câu 900 chữ, không dấu chấm | 1 | **1** | **0** | 906 / 906 / 903 | 512 / 512 / 256 |
  | bảng, một hàng 900 chữ | 2 | **1** | **0** | 927 / 927 / 921 | 512 / 512 / 256 |
  | đối chứng: 400 câu ngắn | 8 | 0 | 0 | 296 / 296 / 253 | 512 / 512 / 256 |

- **"0 / 8.459 vượt":** đúng — toàn kho 8.459 đoạn, `errors` 0, vượt **0**, lớn nhất e5 **366** / 512, huydang **255 / 256** (khớp số của B).
- **"Test chặn PASS bất kể code":** đúng cho `test_canonical_preview_pass` (`test_full_corpus_chunker.py:945-973`) — chỉ đọc file tĩnh
  `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` (commit `071b113` 2026-09-12; `total_chunks` 8.460 ≠ 8.459 hiện nay), không
  gọi code. **Nói chính xác hơn** cho 2 test synthetic (`:852-940`): chúng có kiểm code thật — nhưng là code của CLI `generate_preview`
  (`preview.py:150-165` có hàm kiểm token riêng + `:190-210` quét đoạn vượt), không phải đường build (`grep generate_preview` ngoài test: chỉ
  `preview.py:321` `main`). Tức là "kiểm sai chỗ": PASS dù đường build không chặn. Thân finding của B đã viết đúng ý này; chỉ dòng tóm tắt
  "PASS bất kể code" hơi rộng.
- **"e5 cắt im lặng ở 512":** `sentence_bert_config.json` của e5-small trong HF cache có `max_seq_length: 512`; `embedding/full_corpus.py:216`
  dựng `SentenceTransformer` không đặt / kiểm độ dài ⇒ cắt theo mặc định thư viện. Chưa đo vector của một đoạn vượt (như B ghi).
- **R1 (minor) — mức:** đề xuất **vừa** thay vì cao. Lý do: hôm nay 0 đoạn vượt, tác động chỉ xảy ra khi kho đổi; khi đó chỉ ảnh hưởng vài đoạn
  (dense thấy phần đầu, BM25 vẫn thấy đủ). Theo khuôn rà code, "cao" dành cho tác động thật lên người dùng / số đo. Vẫn giữ thứ tự ưu tiên
  "sửa trước lần build lại" vì sửa nhỏ.
- **R2 (minor) — phương án:** đủ (thêm vào `errors` khi đoạn phát ra không vừa). Thêm một ý cho kế hoạch build lại: giới hạn ràng buộc thực tế
  là tokenizer **huydang 256** (lớn nhất hôm nay 255) — tokenizer của model không chạy ở runtime. Sau khi build fail-closed, một sửa kho nhỏ
  có thể làm build dừng vì huydang chứ không vì e5 ⇒ kế hoạch build lại nên biết trước và quyết (tách thêm hay nới / bỏ huydang khỏi
  danh sách kiểm — đổi đó là quyết định chunker, cần thí nghiệm). Không phải lý do để không sửa.

### B-12 — đúng; phạm vi rộng hơn

- `backend/config/full_corpus_conditions.json` (tracked): 3 rule, **9** selector `exact_text`, **5.324** ký tự, dài nhất 1.050, **9 / 9** có nguyên
  văn trong kho (so NFC với mọi `.md` của kho trừ `evaluation/`, `meta/`, `*sealed*`) — khớp B.
- Phần B ghi "chưa đếm": `test_full_corpus_chunker.py` có **37** chuỗi literal ≥ 20 ký tự nguyên văn kho, **1.327** ký tự, **tất cả** trong dòng
  549–848 (34 chuỗi / 1.265 ký tự chỉ có trong 1–4 file kho, 3 chuỗi là khuôn có trong ≥ 5 file).
- **R3 (minor) — phạm vi:** quét mọi file `.py` tracked trong `backend/` + notebook (`b12_scan_all.py`): ngoài test chunker còn **2 converter**
  `backend/scripts/convert_huegov_culture_raw_to_md.py` (43 chuỗi riêng / 2.246 ký tự) và `convert_huegov_department_raw_to_md.py` (29 / 1.447)
  — thuộc B-13 của B; chưa phân loại đó là bảng ánh xạ tên hay câu nội dung. Không còn file `.py` / notebook tracked nào khác chứa chuỗi kho
  ≥ 20 ký tự. Phương án B-12 nên tính cả hai file này (hoặc B-13 ghi lại tiêu chí đếm này).
- Phương án (a)–(c), (a')–(b') và cách so sánh (đếm ký tự trước / sau, sha đoạn toàn kho giống hệt, test vẫn bắt lỗi cũ): đủ. Mức vừa hợp lý
  (lệch luật dữ liệu §5, không phải bí mật). Gỡ khỏi lịch sử git là phá hủy — đúng là chỉ khi User yêu cầu.

### B-16 — đúng

- Kiểm từng khẳng định: `phase_2_foods_markdown_chunking.md:153-160` "Files canonical" liệt kê 4 file không tồn tại; `phase_0_mvp_foundation.md:101`
  "Collection hiện hành: `hue_foods_e5_small_384`, 572 points"; `README.md:21` "Phase 4 collections là read-only"; `phase_4_qdrant_ingestion.md:40`
  8.460 đoạn, `:55-58` 4 collection `hue_full_corpus_a_*` (`grep -rn hue_full_corpus_a_ backend --include=*.py` = 0), `:224, :332` port 6333 trong khi
  `full_corpus_pipeline.py:99` ép 6335. `full_corpus_chunker` / `markdown_blocks` / `source_state` xuất hiện 0 lần trong phase 0–2 + README.
- **Số trước** (`b16_deadrefs.py`, đếm đường dẫn `backend/ notebooks/ frontend/ guides/ docs/ reports/` không tồn tại, **chưa trừ** đoạn có nhãn
  lịch sử): README 0 / 1 · phase_0 0 / 3 · phase_1 **4** / 18 · phase_2 **4** / 11 · phase_3 **10** / 20 · phase_4 **5** / 21 · `full_corpus_rag` 0 / 30.
- Phương án (a) / (b) / (c): đủ. Điều kiện cho cách đo "0 đường dẫn chết ngoài đoạn có nhãn lịch sử": nhãn phải đọc được bằng máy (một dấu cố
  định, ví dụ heading `## Lịch sử (…)` và mọi thứ dưới nó), nếu không script không tách được — B đã nhận xét "nhãn yếu". Cùng kiểu với C-12 / C-13
  (guide 5–9) ⇒ A nên gộp **một** lần sửa tài liệu cho cả hai phạm vi, cùng một quy ước nhãn.

### B-17 — một phần

- **Đúng:** `full_corpus_rag.md:114-115` lệnh build `python -m backend.ingestion.full_corpus_pipeline build --candidate <id>` thiếu `uv run`;
  notebook 03 cell 6 (markdown) cùng lệnh; `phase_2_foods_markdown_chunking.md:309` `uv run python -m pytest tests/ -q` chạy cả 3 file dùng
  `require_openai_key`.
- **R4 (minor) — khẳng định cần sửa:** "chạy cả test cần key OpenAI (có `POST /api/chat` thật)" ngụ ý tốn tiền khi có key. Đọc code thì **có key
  cũng không có lượt paid nào** trong `backend/tests/`:
  - `test_api_chat.py:86-93` có `POST /api/chat` nhưng đặt `context_limit=2561` (`:89`) ⇒ ngân sách context ≈ 1 token ⇒ `ContextBudgetError` ở
    `chat.py` **trước** lời gọi generator (S2 của C34 đã quan sát nhánh này ra 500 `context_budget_error`);
  - khởi động app chỉ dựng `AsyncOpenAI` (`generator_openai_full_corpus.py:170-174`), không gọi mạng (`app.py:110-117`); lời gọi model duy nhất là
    `Runner.run` (`:195`) trong `generate_answer` / `generate_search_context`;
  - `test_openai_full_corpus_generator.py:24-56`: kiểm cấu hình + chuỗi rỗng bị chặn **trước** mạng; `test_full_corpus_embedding.py` chỉ kiểm spec
    + `parse_embeddings_response` trên dict dựng tay (không gọi OpenRouter);
  - `grep create_collection|delete_collection|upsert(|recreate_collection backend/tests/*.py` = 0;
  - rủi ro paid duy nhất: `test_phase6_live_smoke.py:158, 173, 191, 229, 315` gọi `run_smoke_async(confirm_paid=True)` — 3 cái đầu thoát ở guard,
    2 cái sau chỉ được monkeypatch `create_app` chặn (C-18 của C34).

  ⇒ Hậu quả thật của `pytest tests/ -q`: **không key** thì 8 test đỏ (không phải lỗi code — C-17); **có key** thì không tốn tiền nếu monkeypatch còn
  trúng. B ghi "chưa đo" — trung thực; C trả lời bằng đọc code, **cũng chưa chạy với key** (luật paid).
- **Mức:** đề xuất **thấp** (chỉ tài liệu; không có đường tốn tiền đã biết; `Project_Status.md` §8 đã được A sửa 18:4x — pytest liệt kê file, bỏ
  `--env-file` mặc định). Lệnh build thiếu `uv run` vẫn nên sửa (luật cứng §10). Ý "thiếu `--env-file` mà 8B cần": đúng cho 8B; build e5 không cần
  key ⇒ ghi lệnh theo candidate.
- Phương án + cách kiểm (`grep -n "python -m" guides/*.md notebooks/*.ipynb | grep -v "uv run"` = 0): đủ.

### B-20 — đúng

- **Không so identity:** `test_full_corpus_determinism_and_preview_byte_equality` (`test_full_corpus_chunker.py:978-1048`) — docstring "chunks match
  the runtime build record" nhưng với record chỉ so `file_count` / `chunk_count` (`:993-997`), còn lại so lượt 1 với lượt 2 và preview. Runtime cũng
  không chia lại: `retrieval/full_corpus.py:785-792` chỉ so sha file sparse state và `sparse_state.corpus_identity` đã lưu với record ⇒ đổi code
  chunker mà vẫn ra 8.459 đoạn thì không chỗ nào phát hiện — khớp B. **Thêm assert là đạt ngay:** script C
  `compute_corpus_identity(chunk_full_corpus(...)) == record["corpus"]["identity"]` ⇒ **True** (record 8.459 đoạn, 205 nguồn).
- **Chậm:** C chạy `test_full_corpus_chunker.py --durations=4` (42 passed / 94,4 s): test này **83,45 s** (B: 101,65 s — khác do tải máy). Test chia
  kho 4 lần (2 trực tiếp + 2 trong `generate_preview`) ⇒ ước ~21 s / lần, phần preview ≈ một nửa — **phù hợp** ước của B, chưa đo bằng cách bỏ phần đó.
- **Ghim hằng số kho:** `:69-90` ghim 205 file + số file từng domain (27 / 91 / 29 / 13 / 45) và từng partition; record có đủ 205 nguồn
  (`corpus.sources`) ⇒ phương án (3) `set(files) == set(record sources)` làm được.
- Marker `live`: trùng C-17 của C34 — A gộp một mục.
- Phương án (1)–(4) + cách kiểm (đỏ trên nhánh đổi chunker, `--durations` trước / sau): đủ.

## 3. Cách người kiểm chạy lại thật

Tất cả từ `/home/minhhieu/hue_rag`, `main` `c272644`, 0 USD, không ghi Qdrant, không `--env-file`:

- `cd backend && HF_HUB_OFFLINE=1 uv run python -I /tmp/c34x/b11_check.py` — chunker production (`chunk_document`, `chunk_full_corpus`),
  `get_default_tokenizer_checker` + 3 tokenizer thật trong HF cache, settings thật; file thử chỉ dựng trong bộ nhớ.
- `uv run python -I /tmp/c34x/b12_count.py`, `b12_scan_all.py`, `b12_template.py` — đọc kho (trừ `evaluation/`, `meta/`, `*sealed*`) và file tracked;
  chỉ in số đếm.
- `python3 -I /tmp/c34x/b16_deadrefs.py` — đếm đường dẫn trong guide.
- `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_chunker.py -q -p no:cacheprovider --durations=4`.
- Đọc code / `grep` như ghi ở từng mục; `find ~/.cache/huggingface/hub/models--intfloat--multilingual-e5-small -name sentence_bert_config.json`.

## 4. Kết quả quan sát

- B-11: 2 input vượt ⇒ đoạn vượt mà `errors == 0`; kho 8.459 / 0 lỗi / 0 vượt, max e5 366, huydang 255 / 256.
- B-12: conditions 9 / 9 selector nguyên văn kho, 5.324 ký tự; test chunker 37 chuỗi / 1.327 ký tự; 2 converter 72 chuỗi riêng / 3.693 ký tự.
- B-16: số đường dẫn chết theo guide như bảng ở mục B-16.
- B-17: không tìm thấy lượt paid trong `backend/tests/` (đọc code); 5 chỗ `confirm_paid=True`.
- B-20: identity khớp record (True); `test_full_corpus_chunker.py` 42 passed / 94,4 s, test determinism 83,45 s.

Bằng chứng dùng lại (không phải fresh): nhánh `context_budget_error` của `test_api_chat.py:86` theo quan sát S2 (C34) — cùng commit code, cùng
đường; C đọc lại code để xác nhận.

## 5. Giới hạn hoặc phần chưa chạy

- Chưa chạy test cần key ⇒ "có key không tốn tiền" (B-17) là đọc code.
- Chưa đo vector e5 của một đoạn vượt (B-11); chưa đo thời gian test sau khi bỏ phần preview (B-20).
- B-12: chưa phân loại chuỗi trong 2 converter (bảng tên hay câu nội dung).
- Chỉ kiểm 5 mục được giao; các mục khác của B25 không kiểm (B-01 = C-01 coi như đã kiểm chéo — A).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** cho 5 mục, kèm 4 ghi chú `minor` để B cân nhắc ghi vào `ra_soat_code_B.md` (B tự sửa mục của mình; B được
phản biện bằng bằng chứng):

- **R1:** B-11 mức cao → vừa (giữ ưu tiên sửa trước build lại).
- **R2:** B-11 thêm ý "giới hạn ràng buộc là huydang 256" vào kế hoạch build lại.
- **R3:** B-12 / B-13 tính thêm 2 converter (72 chuỗi riêng / 3.693 ký tự) và số đếm của test chunker (37 / 1.327).
- **R4:** B-17 sửa khẳng định "có `POST /api/chat` thật" ⇒ có key cũng không có lượt paid (đọc code); mức vừa → thấp.

Gợi ý cho A khi gộp `TONG_HOP.md`: gộp B-16 với C-12 / C-13 / C-14 (một lần sửa tài liệu, một quy ước nhãn lịch sử); gộp marker `live` (B-20) với
C-17; gộp B-11 + B-20 (assert identity) + B-12 vào kế hoạch build lại index.
