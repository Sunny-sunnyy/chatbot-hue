# Implementation Report: Phase 9 T2 — công cụ `yeu_cau_tra_web` (phần 0 USD — chờ G vào `main` để đo)

Người làm: E (Claude Code, `hue-rag-ea`) · 21:05 09/11/2026 (`date`) · A giao 09/11 · người review: C (người viết plan)
Plan: `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` bản 2 `88b1f0586e99` (A duyệt, mức nhẹ). Mô tả công cụ: **nguyên văn** plan §1.1.
Nhánh `p9-t2-web` **`2ac126a`** (push), tách từ `main` `fb621e0` (trước G). G đi phương án B (`main` `85cf473` ghi) ⇒ rebase khi G vào `main`.

## 1. Thay đổi (plan §1)

| Plan | Code |
|---|---|
| §1.1 công cụ không tham số, mọi lượt `tro_ly_hue` có công cụ, trừ lượt ghép / biểu mẫu | `assistant._lich_extra` thêm `web_fn` khi `flags.tra_web_cong_cu ∧ trace.truong is None`; `yeu_cau_tra_web_for_turn`: đặt `trace.web_yeu_cau`, trả `YEU_CAU_TRA_WEB_KQ`, lần 2 log `het_luot` (cùng câu, không đổi gì). Biểu mẫu không đi đường công cụ ⇒ không có. Mô tả `YEU_CAU_TRA_WEB_MO_TA` (`full_corpus_prompt.py`) |
| §1.1 `_merge_spec` của #6 chép cờ | `AnswerTrace.web_yeu_cau` (trường thường ⇒ `_merge_spec` chép) |
| §1.2 `max_turns_for(ngay_lich_fn, web_fn)` +1 | `generator_openai_full_corpus.py`; `_assistant_for` / `generate_with_tools` / `start_tools_stream` nhận `web_fn` |
| §1.3 nhánh cổng mới, một chỗ | `web_gate_open`: điều kiện chung giữ nguyên + (`sau_tu_choi` cũ **hoặc** `model_yeu_cau` = cờ ∧ đã yêu cầu ∧ `fixed_outcome is None` ∧ chữ ∉ `REFUSAL_ANSWERS`) |
| cờ | `AssistantFlags.tra_web_cong_cu: false` (`settings.yaml`); `from_settings` báo lỗi khi bật mà `tra_web` tắt |

**Hai chỗ E tự quyết trong phạm vi plan (ghi để C kiểm):**
1. **#6:** phần chạy song song dùng `dataclasses.replace(flags, …, tra_web=False)` ⇒ nếu điều kiện đưa công cụ cần `tra_web` thì đường #6 (bật mặc định) **không** có công cụ, khác đường thường. E cho điều kiện đưa công cụ chỉ cần `tra_web_cong_cu` (vẫn bật ở phần song song); ràng buộc "cần `tra_web`" kiểm ở `from_settings` thay vì `__post_init__` (`replace` gọi lại `__post_init__`). Cổng vẫn đọc `flags.tra_web` của cờ gốc sau khi gộp. Test: mọi lần gọi trợ lý của #6 có công cụ.
2. **"Lượt có lịch không đưa" (§1.1):** lúc dựng công cụ chưa biết lượt sẽ có lịch ⇒ E hiểu là lượt ghép từ nút (`truong`) — không đưa; lượt có `lich_trinh` thì công cụ có mặt nhưng cổng đóng (`trace.lich is not None`). Nếu C muốn bỏ hẳn khi cờ `lich_trinh` bật ⇒ 1 dòng.

## 2. Kiểm tra (0 USD)

- `tests/test_t2_web_cong_cu.py` (mới, SDK thật + client kịch bản + Serper ghi sẵn + Qdrant thật chỉ đọc): **18 passed** — 4 ca cổng × 3 đường (yêu cầu ∧ câu thường ⇒ mở · yêu cầu ∧ `OUT_OF_SCOPE_ANSWER` ⇒ đóng · không yêu cầu ⇒ đóng · "không đủ thông tin" ⇒ mở như B6), trần 1 lần (1 lần Serper), lượt ghép không có công cụ + cổng đóng, 4c lượt đầu / có lịch sử (cờ bật chỉ thêm đúng 1 mục công cụ; lời dặn + đầu vào giống cờ tắt; mô tả = plan, 0 tham số), chuỗi xấu nhất 5 vòng không chạm trần, cờ cần `tra_web`.
- File test bị chạm (`test_b6_tra_web`, `test_ngay_lich`, `test_toc_do_song_song`, `test_b5_lich_trinh`, `test_b2_tool_loop` + mới): **438 passed**.
- **Q1 cờ tắt:** `capture_all.py` 228 / 228 **giống byte** `main` (`data/phase_9/t2_web/q1/nhanh_tat.jsonl` ↔ `data/phase_9/t4/q1/main.jsonl`, `backend/` không đổi giữa `3d2d420` và `fb621e0`).
- Ca "yêu cầu ∧ ngoài phạm vi" trên nền trước G: cổng đóng vì chữ ∈ `REFUSAL_ANSWERS` (và lỗi citation); sau G phương án B câu ngoài phạm vi đi tuyến riêng ⇒ không vào agent.
- **Chưa chạy:** test rộng cả `backend/tests` (sau rebase G, trước đo); lượt có phí §2 (≈ 0,17 USD) — sau khi G vào `main`.

## 3. Bàn giao

- Review: C, `git diff main...p9-t2-web` (sau rebase). Dữ liệu: bộ hỏi kèm `data/phase_9/t2_web/hoi_kem_10.jsonl` md5 `04aa82399972` (E viết trước khi đọc §1.1).
- Tiền: 0 USD.

## 4. Lượt có phí (ghi 21:49 09/11/2026) — **ÂM ở tiêu chí chính**

- **Nền:** nhánh rebase **`bdfbbdc`** trên `main` `3b52017` (G phương án B, **cờ ngày tắt** — A dặn giữ nền này cho đồng nhất), cờ `tra_web_cong_cu` bật tạm ở worktree; Q1 cờ tắt sau rebase 228 / 228 giống byte `3b52017`. Mốc: worktree `3b52017`. Đường đo `answer_turn` + web thật (`data/phase_9/t2_web/tools/do_t2.py`, dùng lại `do_g.py`). 1 lượt (an toàn ×2).
- **Số (code đếm, `data/phase_9/t2_web/ket_qua/`):**

| Sàn §2 | Nhánh | Mốc | |
|---|---|---|---|
| **Câu hỏi kèm có phần web** (≥ mốc + 2 / 10) | **4 / 10** | 4 / 10 | **trượt** |
| S2 ngoài phạm vi bị trả lời | 0 / 44 | — | đạt |
| S2b ngoài phạm vi có web | **1** (`b_dt_12`: câu y tế bị định tuyến xếp khẩn cấp ⇒ agent từ chối ⇒ cổng **cũ** mở) | cùng câu, cùng kết quả ở lượt mốc G phương án B (`pab_r1`) | không do T2 — giới hạn A đã nhận ở G |
| S3b câu Huế ra ngoài phạm vi | 0 | — | đạt |
| Tra web khi kho trả lời được (mẫu 30 + 4 `kho_co`) | **0** qua cổng mới (3 lượt đếm thô là câu kho **từ chối** ⇒ cổng cũ, giống mốc) | — | đạt |
| Câu kho nhắc mục web · `max_turns` · citation lỗi | 0 · 0 · 0 | — | đạt |
| S2c (10 câu "web trả lời được") | 9 / 10 | 9 / 10 | đạt |

- **Vì sao âm (quan sát, đọc số):** model gọi `yeu_cau_tra_web` **29** lần, trong đó **26** lần chính lượt đó trả **câu từ chối cả câu** — lời dặn trả lời bắt "bằng chứng không đủ ⇒ trả đúng câu từ chối" (cách cũ "trả lời phần có căn cứ" đã thử 2 lần, trả lời câu ngoài kho ⇒ gác — `07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` checklist). Câu từ chối thì **cổng cũ B6 đã mở rồi** ⇒ công cụ không thêm gì. Cổng **mới** (kho trả lời + model yêu cầu) mở **3** lần: 1 câu thiên tai (câu cố định NCHMF / 112), 1 "chưa xác minh", 1 mục bị kiểm cuối loại ("không tin cậy") ⇒ **0 mục web dùng được thêm**. Hỏi kèm: 9 / 10 câu model có yêu cầu, 8 / 10 kho từ chối cả câu (giống mốc).
- **Chưa chạy (cố ý — luật 09/11 "lượt đo phải giữ một sàn"):** chấm S1 (an toàn ×2 đã sinh, `nhanh_r1` + `nhanh_an_toan_r2`) và S4 (mẫu 30 hai bên đã sinh) — chỉ cần khi merge; T2 âm ⇒ đề xuất không merge ⇒ không chấm. Có sẵn dữ liệu nếu A muốn.
- **Tiền thật:** nhánh 0,119908 + mốc 0,051489 = **0,171397 USD** (≤ dừng 0,25).
- **Đề xuất (A quyết):** plan §2 "âm ⇒ ≤ 1 vòng chỉnh mô tả công cụ rồi phương án B". Mô tả công cụ **không** đổi được việc model từ chối cả câu (do lời dặn trả lời) ⇒ vòng chỉnh mô tả khó có lợi; phương án B ("thêm cổng cho câu từ chối + đã hỏi kèm") **trùng** cổng cũ đang mở cho mọi câu từ chối ⇒ không thêm gì đo được. ⇒ **đóng hồ sơ T2** (tag `hoso/p9-t2-web`, không merge), giữ cổng B6 như cũ. Muốn thật sự trả lời "nửa kho + nửa web" thì phải đổi luật "từ chối cả câu" — việc lớn, có tiền lệ âm, ngoài phạm vi T2.

## 5. Kết luận (21:49 09/11/2026) — **A đồng ý đóng hồ sơ**: tag `hoso/p9-t2-web` (A gắn + push), không merge; cổng web B6 giữ như cũ. A báo User.
