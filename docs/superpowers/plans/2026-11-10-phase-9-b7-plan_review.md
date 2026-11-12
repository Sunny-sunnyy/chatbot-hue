# Review: Plan B7 — so cả hệ (agent trên `main`) với RAG 1–8 · nháp bản 1 · vòng 1

Decision: **changes_requested** (3 major, 6 minor; 0 blocker)
Người kiểm: E (`hue-rag-33`, Claude Code — Fable 5.2)
Date: 18:48 12/11/2026 (`date`)
Bản được review: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` sha256 `5413ae469c5e` (người viết: C), `main` `a83defd`
Căn cứ: spec `docs/superpowers/specs/2026-11-02-phase-9-design.md` §4, §5 B7, §8, §11.5, §12.3, §12.4 (+ §12.7 để đối chiếu tiền)

## 1. Phạm vi đã review

- Đọc hết plan; đọc các mục spec ghi ở đầu plan. Không đọc STATUS / tin nhắn của người viết.
- Chỉ dùng lệnh chỉ đọc, 0 USD; không mở nội dung `*sealed*` (chỉ `wc -l`); không in câu hỏi (chỉ đếm dòng, tên trường, loại câu).
- Đối chiếu từng khẳng định kiểm được của plan với repo: tag mốc, khác biệt code, cờ, build record, số câu mỗi bộ, sự tồn tại và giao diện lệnh của từng harness ở **cả hai** bản code (`main` và tag `p9-moc`).
- Hai điểm A giao thêm: lượt đo nào không giữ sàn nào (mục 2, m-1) và cờ trong plan §2 so với `settings.yaml` hôm nay (mục 4).

## 2. Findings

### M-1 (major) — "bản sao harness chỉ đổi hằng số" không chạy được như plan ghi

- **Vị trí:** plan §4 dòng "Golden 176, hai bên" và dòng "Chuỗi 40"; §2 "bước 0".
- **Yêu cầu bị ảnh hưởng:** `WORKFLOW.md` §4 (4b) — script / runbook có lượt trả phí phải chạy thử mọi lệnh 0 USD trước; spec §4 S-G (mức tụt tính theo cặp agent ↔ mốc).
- **Bằng chứng (đọc code, chưa chạy):**
  1. `data/do_cuoi_2026-11-01/tools/do_cuoi.py` dựng cho **ba bên cố định** `ARMS = ("truoc", "sau", "aa")`: `export_judge`, `scored`, `analyze` lặp qua cả ba và đọc `check_<arm>.json` của cả ba; bên `truoc` được **chép từ một file cố định** của 30/10 (`import_truoc`, kiểm sha), không phải lượt sinh mới ở `p9-moc`; `analyze` so "sau" với "aa" **từng câu**. Plan lại chọn không chạy A/A ⇒ không có bên `aa` ⇒ `export-judge` / `analyze` dừng lỗi; nếu chép A/A 01/11 vào thì phép so "agent hôm nay ↔ A/A của RAG trên chỉ mục cũ" vô nghĩa.
  2. Hằng số nhiễu trong tool là `N_AA = 2` ("giữ như đợt 1 / 2"), không phải số lấy từ A/A 01/11; plan không ghi con số A/A nào sẽ dùng cho ngưỡng "câu tụt ≤ A/A + 3".
  3. `evaluation.full_corpus_eval generate` ở `p9-moc` chỉ nhận `--golden full|smoke` + `--cases <case_index>` — **không nhận file câu tuỳ ý** ⇒ "lượt của chuỗi đổi thành câu đơn ⇒ `generate` ở `p9-moc`" không làm được bằng "script nhỏ đổi chuỗi ⇒ câu"; cần một runner gọi `answer_case` trên danh sách câu (như `an_toan_run.py` đang làm).
- **Tác động:** lỗi lộ ra sau khi đã sinh có phí, hoặc người chạy phải sửa harness ngay trong lượt đo (đổi cách tính giữa chừng). B đang làm bước 0 theo đúng câu "chỉ đổi hằng số".
- **Tiêu chí đóng:** plan ghi rõ danh sách sửa của bản sao `data/phase_9/b7/tools/` (hai bên thay ba; bên mốc = lượt sinh mới trong worktree `p9-moc`; ngưỡng câu tụt là **một số ghi sẵn** kèm nguồn); ghi runner cho phía RAG của bộ chuỗi; bước 0 thêm một lượt chạy thử 0 USD của `check` / `export-judge` / `analyze` trên thư mục bản sao (khoá giả hoặc vài dòng mẫu) cho cả hai bên.

### M-2 (major) — kết luận (i) chưa có cách tính ghi trước

- **Vị trí:** plan §1, §3 (ba nhóm), §8 Q4.
- **Yêu cầu:** spec §5 B7 (i) "Completeness (hoặc từ chối nhầm với câu theo ngày) vượt nhiễu, CI 95 % > 0 sau Holm"; `Session_Prompt.md` §6 "ghi tiêu chí trước khi chạy".
- **Bằng chứng:** plan chỉ nhắc lại câu của spec. Chưa ghi: (a) nhóm câu theo ngày dùng **chỉ số nào** (Completeness hay từ chối nhầm) và nhãn chấm nào của `brief_cham.md` quy ra chỉ số đó; (b) nhóm câu hỏi tiếp tính trên **lượt nào** — bộ đã thấy có 56 lượt, 31 lượt sau lượt đầu, trong đó chỉ 20 lượt có đáp án Golden để chấm Completeness và 7 lượt không đứng một mình; đơn vị là lượt hay chuỗi; (c) CI tính bằng gì (bootstrap theo cặp như B2b? số lần lặp, seed), Holm áp ra sao; (d) phần đã thấy và phần kín (7 câu ngày, 15 chuỗi) gộp hay báo riêng; (e) danh sách 18 câu nhiều nguồn nằm ở file nào (Golden có 29 câu loại `multi_source`; plan không trỏ đường dẫn).
- **Tác động:** các lựa chọn này quyết định "tốt hơn / không tốt hơn"; chọn sau khi thấy số là sửa tiêu chí để hợp kết quả.
- **Tiêu chí đóng:** một bảng 3 dòng (nhóm · bộ + đường dẫn danh sách câu · đơn vị · chỉ số · cách tính CI + seed · gộp / tách kín) nằm trong plan trước khi A duyệt sha.

### M-3 (major) — một số sàn và ngưỡng nêu ở §1 / §3 không có lượt đo, không có tiền

- **Vị trí:** plan §3 dòng "Ngoài phạm vi (S2)", §4, §7; spec §5 B7 bảng (ii), §12.3.
- **Bằng chứng:**
  1. **S2 / S2b** (21 câu, "hai bên"): §4 không có bước / harness, §7 không có dòng tiền. Spec §12.3 còn yêu cầu ×2 và S2b thêm 4 câu "ngoài Huế" của B6.
  2. **Ngưỡng web (ii)** có hai vế: "≥ 60 %" **và** "0 truy vấn chứa tên". Vế sau cần chuỗi nêu tên rồi hỏi câu cần web (`data/phase_9/bo_do_b3/web_neu_ten.jsonl`, 3 chuỗi) — plan không nhắc bộ này.
  3. **Golden qua `generate` không đi qua cổng web:** `answer_case` gọi `answer_turn` không truyền `tim_web` (`backend/evaluation/full_corpus_eval.py` hàm `answer_case`), và `web_gate_open` đòi `tim_web is not None` ⇒ dù `tra_web: true`, lượt Golden là đường chỉ-kho. Điều này đúng cho F1, nhưng plan §2 viết "đúng `settings.yaml` tại `$C_DONG`" dễ hiểu nhầm là cả hệ; sàn có web (S2b, "0 câu không có bằng chứng bị trả lời khẳng định") chỉ được đo ở các bước dùng `do_g.py ca_cau`.
  4. §1 nói "sàn §4 / §12.3 phạm ⇒ âm" nhưng không nói sàn nào xét ở B7 bằng lượt nào (S2c, S3, S3b, S6 không được nhắc; S5 có ghi là cắt).
- **Tác động:** hoặc chạy thiếu sàn đã hứa, hoặc phát sinh lượt ngoài plan (tiền, thời gian) lúc đo.
- **Tiêu chí đóng:** một bảng "sàn / ngưỡng · lượt nào cho số · đếm bằng code hay người chấm · tiền" phủ S-AT / S1, S-G (F1–F4 + mức tụt), S2, S2b, trích dẫn, và 3 việc (ii); sàn nào không xét ở B7 ghi một dòng lý do. Gợi ý rẻ: S3b và S6 đếm bằng code trên các lượt đã có (0 USD); S2c, S3 ghi "đã đo ở bậc G, lời dặn định tuyến không đổi ⇒ dùng lại" nếu hash lời dặn tại `$C_DONG` khớp.

### Minor (không chặn, sửa khi viết bản 2)

- **m-1 — đề xuất cắt (lượt không giữ thêm sàn nào):**
  (a) **Phía RAG của S2 (b) 10 câu** — S2 là sàn tuyệt đối (0) của agent, số của mốc không vào luật nào ⇒ chỉ chạy phía agent (11 câu Golden ngoài phạm vi đã nằm sẵn trong lượt Golden).
  (b) **An toàn 32 phía RAG ×2 ⇒ ×1** — "mới" đã được thủ tục S-AT xử lý (ca mới ⇒ sinh lại 3 lần **hai bên**); lượt thứ hai của mốc không đổi kết luận. Tiết kiệm ≈ 0,007 USD + một lượt chấm.
  (c) **Lượt đầu của mỗi chuỗi phía RAG** khi lượt đó là câu Golden (16 / 25 chuỗi đã thấy) — đã có câu trả lời trong lượt Golden của mốc ⇒ dùng lại, không sinh / chấm lần nữa.
  Các lượt còn lại đều chỉ ra được sàn / kết luận nó giữ (Golden hai bên ⇒ S-G + nhóm nhiều nguồn; an toàn agent ×2 ⇒ S1; câu ngày hai bên ⇒ (i); chuỗi hai bên ⇒ (i) + nhớ tên) — giữ. Các mục plan §5 đã cắt (tốc độ, T1 158 phía agent, bộ kín của tính năng không ở bản đóng, khẩn cấp, ảnh): đồng ý.
- **m-2 — nhãn bộ câu ngày cũ:** bộ 15 câu 30/10 còn ít nhất một nhãn "từ chối" đã lỗi thời từ khi hệ thống biết ngày (handoff mục "Không gấp" đã ghi). Sửa nhãn (hoặc ghi định nghĩa chấm) **trước** khi sinh, kèm giờ.
- **m-3 — "cùng giờ" hai bên:** máy chỉ chạy một server một lúc ⇒ ghi "cùng một ngày, hai bên liền nhau, không vắt qua nửa đêm; ghi giờ mỗi bên" (đáp án câu ngày đổi theo ngày, không theo giờ).
- **m-4 — xác nhận cờ bằng lệnh, không bằng đọc file:** `settings_loader.apply_env_overrides` cho biến môi trường `HUE_TRA_WEB` ghi đè `tra_web`; lượt đo chạy với `--env-file` ⇒ bước 0 in `AssistantFlags.from_settings(...)` dưới đúng lệnh sẽ dùng (0 USD) và chép vào report.
- **m-5 — tiền:** §7 so với quỹ 0,35 nhưng phần còn lại thật của Phase 9 là ≈ 0,32 (handoff: 3,88 / 4,2) ⇒ ghi số còn lại thật; cộng thêm S2 và lượt Serper của các câu bị từ chối trong bộ chạy qua `do_g.py ca_cau` (web thật).
- **m-6 — chỗ lệch spec chưa được chốt rõ:** A đã chốt Q1–Q4; việc thay "câu rủi ro 3 lượt" (spec §5 B7) bằng "an toàn ×2 + S-AT" và danh sách cắt §5 chưa có dòng chốt. Hợp với §12.3 (bản 13, User đã duyệt) nên chỉ cần A ghi một dòng. Dòng "Lệch tài liệu: `anh.bat`" ở §2 đã hết đúng (Project_Status §4 đã sửa) — bỏ.

Không có vấn đề over-engineering: plan dùng lại bộ và harness có sẵn, không dựng bộ mới.

## 3. Cách người kiểm chạy lại thật (đều chỉ đọc, 0 USD)

- `git rev-parse 'p9-moc^{commit}'`, `git rev-parse 1c10111^1`, `git ls-remote --tags origin p9-moc`; `git diff --stat 89c988e 18e8f42 -- backend`.
- `sha256sum` build record; `curl` Qdrant `/collections/...` (số điểm).
- `grep` khối `assistant:` và `anh:` của `backend/config/settings.yaml` trên `main`; `git log e57231a..HEAD -- backend/...`.
- `wc -l` các file bộ đo (kể cả file kín — chỉ số dòng); đếm `category` của Golden và tên trường của bộ chuỗi đã thấy bằng script chỉ in số đếm.
- `grep` / `git show p9-moc:<file>` trên các harness và `full_corpus_eval.py`, `routes/chat.py`, `assistant.py`, `settings_loader.py`.

## 4. Kết quả quan sát

| Khẳng định của plan | Quan sát | Kết quả |
|---|---|---|
| Tag `p9-moc` = `18e8f42` = cha thứ nhất của merge B0, đã push | khớp cả ba (tag có chú thích trỏ `18e8f42`; có trên `origin`) | đúng |
| `89c988e` ⇒ `18e8f42` không đổi phần tìm / ngữ cảnh / sinh | `backend/` chỉ khác `api/app.py` (9 dòng) + `tests/test_static_ui.py` | đúng |
| Build record `9921888f2030`, 8.435 điểm | sha khớp; Qdrant 8.435 | đúng |
| Code `p9-moc` đọc cùng build record | cùng schema `full_corpus_build:v3`; khởi động thật + T1 158 câu: **chưa chạy** (việc bước 0 của B) | một phần |
| Số câu các bộ | Golden 176 (md5 `6331e88fb171`) · an toàn 32 · ngày 15 + 3 + 10 + 7 = 35 · chuỗi 25 + 15 · tuyến kín 20 · (a) kín 8 · (b) kín 10 · B6 28 + 11 · B5c kín 6 · sửa lịch kín 5 | đúng |
| Harness có sẵn | 7 file đều có; `do_g.py ca_cau` lấy cờ từ settings + web thật; `chuoi` có ở `main`; `an_toan_run.py` chỉ import tên có ở `p9-moc`; `p9-moc` có `/api/chat/stream` với sự kiện `delta` mà `chay_t1.py` đọc | đúng — trừ M-1 |
| **Cờ plan §2 ↔ `settings.yaml` trên `main` hôm nay** | bật: `router`, `may_have_changed_notice`, `song_song_tra_loi`, `tim_them`, `nho_hoi_thoai`, `lich_trinh_bieu_mau`, `tra_web`, `thoi_tiet`, `ngay_lich`, `anh.bat`; tắt: `today_line`, `nho_cau_tra_loi`, `lich_trinh`, `ban_do_lich` | **khớp đủ 14 cờ, không lệch** |

Ghi thêm về cờ: từ `e57231a` tới nay không cờ nào đổi, nhưng hành vi sau cờ có đổi (câu ngày tính sẵn, câu lịch chung đi trợ lý) — plan lấy `$C_DONG` làm tham số nên không sai; lúc chốt `$C_DONG` cần liệt kê lại.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy harness nào (kể cả 0 USD) — M-1 dựa trên đọc code; người viết có thể phản biện bằng một lượt chạy thử.
- Không mở nội dung kín ⇒ không kiểm được "~10 câu xã giao" / "~10 câu web trả lời được" có đủ số trong các bộ kín đã dùng.
- Không kiểm ước tiền từng dòng bằng log; chỉ đối chiếu với đơn giá spec §8 / §12.7 (cùng cỡ).

## 6. Decision và bước tiếp theo

**changes_requested.** Người viết (C) sửa plan thành bản 2 trong một lượt: M-1, M-2, M-3 theo tiêu chí đóng; minor sửa cùng lượt nếu tiện. Giữ nguyên: mục tiêu §1, hai bên §2, tag mốc, danh sách bộ §3, các quyết định A đã chốt Q1–Q4. E kiểm phần sửa ở vòng 2 (vòng cuối theo luật 2 vòng); vòng 2 chỉ còn minor ⇒ A duyệt sha.
Việc bước 0 của B: phần "bản sao harness chỉ đổi hằng số" nên chờ danh sách sửa của M-1 (phần khởi động `p9-moc` + T1 158 câu không bị ảnh hưởng).
