# Implementation Report: sửa kho nhỏ — giờ mở cửa 11 điểm Quần thể (C192)

Người làm: C (Claude Opus 5.5, `hue-rag-3c`) · việc **C192** (A giao)
Date: 19:57 05/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-05-sua-kho-gio-mo-cua-plan.md` bản 2 `65e7e2b2b68c` (A duyệt). Dữ liệu chạy (private): `data/sua_kho_2026-11-05_gio/`.
Repo public: report không chép kho / Golden; câu Golden chỉ ghi `case_index` + loại câu.

## 1. Phạm vi

Đúng plan §2–§5: chèn một dòng giờ mở cửa chung (lấy từ file vé Quần thể đã có trong kho) + một dòng nguồn vào 11 file di tích → chia đoạn thử → xoá + dựng lại chỉ mục tại chỗ → đo trước ↔ sau (T1 158 câu, Golden 11 câu chạm, an toàn 10 câu, 1 câu thật). Không đổi code.

## 2. Thay đổi chính

- **Kho:** 11 file `heritages/heritage/`, 21 edit, diff +55 dòng / −0 (`kho.diff`, `applied.jsonl`). Bản sao 11 file gốc: `knowledge-base-hue/meta/backup_gio_mo_cua_2026-11-05/`.
- **Chỉ mục:** collection `hue_full_corpus_7a2_e5_small_384` **8.424 ⇒ 8.435 point** (+11 đoạn mới, chia đoạn thử cũng ra 8.435; build kiểm 8.435 payload + 5 vector mẫu).
  - Build record **`9921888f2030`** (cũ `51fb1ec63cbc`) · sparse state **`4a8311a2dfef`** (cũ `c8134c49a648`) · **T1 mới `64656a87c109`** (cũ `4d5bbe9e0edc`). Bản sao record / sparse cũ: `data/sua_kho_2026-11-05_gio/backup/`.
- **Công cụ chấm dựng lại:** `data/sua_kho_2026-11-05_gio/tools/cham.py` (`8317fe1cf3fb`, xuất file mù + so). Lý do: harness "trước" nằm ở `/tmp/c192` và mất khi máy khởi động lại 19:12. Câu trả lời "trước" (13:06–13:08) vẫn còn đủ trong thư mục đợt; bên "sau" sinh bằng **đúng hai lệnh có sẵn trong repo** mà bộ "trước" dùng (mục 3), cùng cờ `settings.yaml`, backend giống byte (`git rev-parse HEAD:backend` = `5a8aa5e:backend` = `e51fd867c00c`).

## 3. Cách đã chạy thật

```bash
DRY=1 bash data/sua_kho_2026-11-05_gio/tools/chay.sh      # 19:21, C — bước 0 qua
! bash data/sua_kho_2026-11-05_gio/tools/chay.sh          # 19:40–19:44, User (auto mode chặn xoá collection) — ghi kho, chia thử, xoá, build, T1
# từ backend/, --env-file tuyệt đối
uv run … python -m evaluation.full_corpus_eval generate --golden full --cases <11 case touched.json> --out …/golden_sau.jsonl
uv run … python ../data/phase_9/b2_chay/tools/sinh_an_toan.py …/an_toan_sau.jsonl sau 1 --qids <10 qid touched.json>
uv run … python -m evaluation.full_corpus_eval generate --golden full --cases 67 --out …/golden_sau_c67_lan{2,3}.jsonl   # chạy lại câu tụt
uv run --env-file … uvicorn api.app:app --port 8853   # server tạm từ main; POST /api/chat 1 câu; tắt bằng TaskStop
python3 -I tools/cham.py export | compare              # judge = sub-agent Claude mù (map.json chỉ C đọc)
```

Judge: Golden 22 bản (11 câu × trước / sau, xáo seed `20261297`) — 1 sub-agent, thước `backend/evaluation/full_corpus_judge_prompt.md`; an toàn 20 bản — **2** sub-agent độc lập, thước `data/loi_nang_2026-10-28/rubric.md`, luật "một trong hai judge báo là tính".

## 4. Kết quả quan sát

| Đo (plan §5) | Sàn | Kết quả |
|---|---|---|
| T1 158 câu (0 USD) | 0 câu **không chạm** 11 file mất đoạn đúng | **ĐẠT** — 148 / 158 top-10 **giống hệt**; 10 câu đổi đều là câu chạm (đoạn từ 11 file trong top-10 hoặc nhãn đoạn đúng ở 11 file), độ phủ từ khoá 10 / 10 không đổi; MRR 0,7216 · nDCG 0,7554 · phủ từ khoá 92,35 % — **giống trước tới 4 chữ số** |
| Golden 11 câu chạm (có phí) | không câu nào tụt Đủ / Đúng > 1 điểm mà không giải thích được bằng dòng giờ | **PHẠM ở lượt 1, 1 câu** — 10 / 11 điểm giống hệt; **case 67** (nhiều nguồn) 5 / 5 ⇒ **1 / 1** vì ra câu từ chối. Chạy lại 2 lần: **trả lời cả 2, judge mù 5 / 5 cả 2** (mục 5) |
| An toàn 10 câu (có phí) | 0 lỗi mới | **ĐẠT** — 2 judge: ý trái 0 / 0 (trước / sau) · sai điều kiện 0 / 0 · thiếu cảnh báo judge 1: 3 ⇒ 2, judge 2: 5 ⇒ 3; **lỗi mới 0, hết lỗi 0** theo câu; câu ngoài kho mới bị trả lời 0; từ chối 2 ⇒ 2 |
| 1 câu thật qua server | trả đúng giờ đã ghi, có trích dẫn file lăng hoặc file vé, không từ chối | **ĐẠT** — câu trả lời nêu đúng khung giờ 07h00–17h30 kèm lưu ý giờ có thể đổi theo mùa / sự kiện, có [1], nguồn = file lăng, `/health` 200, 4,0 s, 0,00032 USD |

Thêm: `full_corpus_conditions.json` (3 mục) không trỏ vào 11 file; Golden md5 `6331e88fb171` không đổi; build không báo đoạn vượt token.

**Case 67 — vì sao C cho là nhiễu (quan sát, không phải nguyên nhân đã chứng minh):** top-10 lần tìm đầu **giống hệt** bên trước (cả thứ tự); khác ở lần model tự gọi `tim_kho` thêm (trước 3 lần, lượt 1 sau 2 lần rồi từ chối); hai lần chạy lại cùng chỉ mục mới trả lời đủ (2 và 3 lần tìm), judge 5 / 5. Kiểu "từ chối sau vài lần tìm thêm" đã có trong danh sách theo dõi của Phase 9. Không chạy lại được bên "trước" (chỉ mục cũ đã xoá) nên chưa đo nhiễu A/A của câu này trên chỉ mục cũ.

**Tiền:** bộ "sau" 0,012834 USD (Golden 11 0,0061 · an toàn 10 0,005304 · chạy lại câu 67 ×2 0,001114 · câu thật 0,000317) + bộ "trước" 0,010791 = **0,023625 / trần 0,03** (dừng 0,025 — chưa chạm). Judge: quota Claude.

## 5. Lỗi và giới hạn

- **Sàn Golden phạm theo chữ ghi trước** (case 67, lượt 1). C **không** tự xếp là đạt và không đổi tiêu chí: plan §6 ghi "phạm sàn ⇒ dừng". Kho + chỉ mục mới **đang chạy** (không có bước nào sau đó để dừng). **A quyết:** (a) giữ — coi là nhiễu với bằng chứng 2 / 2 lần chạy lại 5 / 5, ghi rõ "sàn phạm ở lượt 1"; hoặc (b) lùi về kho cũ (`chay.sh` có hàm `lui`; bản sao kho + record + sparse còn). **C đề xuất (a)** — lý do ở mục 4; chọn (b) mất giờ mở cửa ở 11 điểm, tốn ~5 phút CPU dựng lại, và câu 67 vẫn có thể từ chối ngẫu nhiên trên kho cũ.
- Harness "trước" mất ⇒ phần chấm dựng lại (`cham.py`); phần sinh câu trả lời dùng đúng lệnh cũ nên hai bên cùng đường `answer_case` / `answer_turn` không stream. Bộ "trước" chưa từng chấm ⇒ hai bên chấm **cùng một lượt mù** (đúng bẫy "chấm baseline cùng lượt mù").
- Khác cách đo an toàn của Phase 9: không có 15 câu đối chứng kiểm judge (n = 10 câu, 20 bản); mỗi judge thấy cả hai bản của cùng câu (xáo, không nhãn bên) — đổi lại so được trong cùng một judge.
- Golden chỉ 1 judge ⇒ chênh 1 điểm nằm trong nhiễu judge; chỉ chênh > 1 mới tính.
- 1 câu thật là một mẫu.
- Server tạm cổng 8853 đã tắt; cổng 8841 lúc đó là server của session khác, C không dùng.

**Quyết định (User, A chuyển — C ghi 20:05 05/11/2026):** **GIỮ** sửa kho C192 (phương án (a)). Ghi rõ: sàn Golden **phạm ở lượt 1** (case 67), 2 / 2 lần chạy lại 5 / 5; case 67 vào danh sách theo dõi.

## 6. Bàn giao cho người kiểm

- Đọc: plan §5 (sàn), `data/sua_kho_2026-11-05_gio/kho.diff` (chữ chèn đúng plan §2), mục 4–5 report này.
- Chạy lại rẻ nhất (0 USD): `python3 -I data/sua_kho_2026-11-05_gio/tools/cham.py compare` (từ thư mục đợt) · so `t1_truoc.jsonl` ↔ `t1_sau.jsonl` theo `top_chunk_ids` · `curl …/collections/hue_full_corpus_7a2_e5_small_384` ⇒ 8.435.
- Việc của A sau report: quyết (a) / (b) ở mục 5; cập nhật báo cáo khâu kho + nhật ký + `Project_Status` §4 (8.435 đoạn, record `9921888f2030`, sparse `4a8311a2dfef`, T1 `64656a87c109`); thêm đợt `2026-11-05_sua_kho_gio` vào bảng `report_agent/README.md`.
- Giải thích ngắn cho User: thêm một dòng "giờ mở cửa 07h00–17h30" (lấy từ file vé đã có) vào 11 di tích rồi dựng lại chỉ mục; tìm kiếm các câu khác không đổi chút nào; câu hỏi giờ lăng Tự Đức giờ trả lời đúng; một câu Golden lượt đầu bị từ chối nhưng chạy lại hai lần đều trả lời đủ.
