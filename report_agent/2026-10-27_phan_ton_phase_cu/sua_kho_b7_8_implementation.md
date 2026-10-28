# Implementation Report: đợt sửa kho — bước 7–8 (B82): nhãn đoạn đúng v4 + quét Golden lệch kho

Người làm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 11:19 28/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` mục B82 (A giao 11:11 28/10). Chỉ đọc, chỉ đề xuất, **0 USD**.
Spec: `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (User duyệt `937cf8969810`) §5 bước 7, 8. Không sửa Golden, không đổi `GOLD_PATH`, không mở câu kín.
File tracked này chỉ có số đếm / mã câu; nội dung ở file private.

## Tóm tắt cho User (lời thường)

- **Nhãn "đoạn đúng" bản mới (v4):** 174 trích dẫn của 55 câu — 172 trích dẫn tìm lại được nguyên văn trong kho đã sửa (42 chỉ dời vị trí). **2 trích dẫn của 1 câu** bị edit
  đổi chữ ⇒ B đề xuất trích dẫn mới = đúng câu chữ kho mới; **cần bạn duyệt 2 trích dẫn này** (sau khi người kiểm xem).
- **Golden (đáp án mẫu):** quét 59 câu có thể chạm phần sửa ⇒ **không câu nào cần sửa** cho đợt 1 — phần lớn edit chỉ thêm tên phường mới và giữ tên cũ trong ngoặc, nên đáp án
  cũ vẫn khớp; các con số bị đổi (mùa, khoảng cách, hạn vé…) không có câu Golden nào hỏi tới.
- **Ghi lại cho đợt 2:** 1 câu Golden là ứng viên sửa ở đợt 2 (không thuộc đợt 1; chi tiết ở file private); kho thiếu mục "giờ mở cửa Đại Nội" (lý do câu thử q02 của phần đo streaming bị từ chối).

## 1. Bước 7 — gold v4 (nháp)

Script private `data/phase_8_1/tools/build_gold_v4.py` (sha `f4c8d35f9bf9`; luật kiểm như `build_gold_v3.py`; từ chối ghi đè; chỉ đọc kho):

| Nhóm trích dẫn (174) | Số |
|---|---:|
| file không sửa (giữ nguyên) | 108 |
| file sửa, vị trí không đổi | 22 |
| file sửa, **dời vị trí** (nguyên văn, đúng 1 lần) | 42 |
| **bị edit chồng** (chữ đổi) ⇒ đề xuất | 2 (câu 27: 2 trích dẫn bị edit đổi chữ — edit 100, 101, 102, K125) |
| không khớp mà không do edit | 0 |

- Đề xuất = áp **đúng phép thay của edit** lên trích dẫn (không mở rộng); cả 2 tìm thấy đúng 1 lần trong file mới. Kiểm sau: **0 lỗi**.
- Ghi `gold_v4_draft.jsonl` (`927bae1bf201`, đã điền 2 đề xuất) + `gold_v4_proposals.json` (`dc3626bfce11`) + `gold_v4_CHANGES.md`. `gold_v4.jsonl` **chưa có**: chỉ tạo bằng
  `--approved` sau khi User duyệt 2 đề xuất. v1 / v2 / v3 sha không đổi (script so trước / sau).
- **Lệch C68** (review spec 27/10): C68 đếm 24 câu / 66 trích dẫn lệch / 3 bị chồng; B82 đếm 28 câu / 42 dời + 22 cùng vị trí / 2 bị chồng; 0 trường hợp edit chạm khoảng trích dẫn mà chữ
  còn nguyên ⇒ người kiểm đối chiếu cách đếm.

## 2. Bước 8 — quét Golden (176 câu, `golden_full_corpus.jsonl` md5 `0f7dbf41b422`, không sửa)

| Lớp | Cách | Kết quả |
|---|---|---|
| 1. theo chữ | `data/sua_kho_2026-10-27/tools/golden_scan.py` (`5b1e4f0a0e1f`): đáp án / keyword chứa cụm chữ cũ quanh chỗ sửa (2 từ) hoặc con số bị bỏ | 26 câu |
| 2. theo vị trí | context bộ "trước" (10 đoạn) có đoạn giao vùng `old` của edit (bảng đoạn cũ `chunks_truoc.json`) hoặc đoạn file danh mục bị loại | 40 câu (147 đoạn chạm) |
| hợp | | 59 câu |
| 3. đọc từng câu | 3 sub-agent, mỗi agent đọc **chỉ** gói câu hỏi + đáp án + keyword + edit liên quan (không đọc kho, không câu kín) | sửa **0** / không 59 / hỏi 0 |

**B kiểm lại** (kết quả sub-agent là dữ liệu): lớp 1 — mọi cụm chữ khớp vẫn còn nguyên trong chữ mới (edit "thêm tên mới, giữ tên cũ"); 17 câu khớp theo con số (8 edit đổi số) — đọc từng
cặp: câu Golden hỏi đối tượng khác, số trùng ngẫu nhiên. Kiểm thêm theo **tên đối tượng của file bị sửa**: 11 câu Golden nhắc tới; 2 câu có từ bị bỏ trong đáp án — đều là từ phổ thông,
đáp án không nêu fact đã đổi ⇒ **0 đề xuất sửa Golden**. File private `data/sua_kho_2026-10-27/golden_de_xuat.md` (cách quét, kết luận, ghi chú).

**Ghi chú (không thuộc đợt 1):** câu 5: ứng viên Golden đợt 2 (chi tiết `golden_de_xuat.md`). Câu q02 bộ C73 (giờ mở cửa, bị từ chối): kho chỉ nhắc khung
giờ mở cửa ở một dòng quy định của file vé (không edit nào chạm dòng đó; đoạn đó không vào top-10 trên index mới) ⇒ do kho thiếu / tầng tìm, không do sửa kho; ứng viên đợt 2.

## 3. Bàn giao cho người kiểm

- Chạy lại (free): `uv run python -I data/phase_8_1/tools/build_gold_v4.py` sẽ dừng "exists" (từ chối ghi đè) — muốn chạy lại thì đổi tên đầu ra trong bản sao script; đọc
  `gold_v4_proposals.json` (2 mục: trích dẫn cũ / đề xuất / edit) so với `applied_edits.jsonl`.
- `uv run python -I data/sua_kho_2026-10-27/tools/golden_scan.py` ⇒ 26 câu; `golden_scan/result_*.jsonl` (59 dòng); đọc mẫu vài câu "không".
- Không file tracked nào đổi ngoài report này.

## 4. Việc chờ User (qua A)

1. Duyệt 2 trích dẫn gold mới của câu 27 (`gold_v4_proposals.json`) ⇒ B chạy `--approved` ⇒ `gold_v4.jsonl`; rồi đổi `GOLD_PATH` (việc riêng, có review).
2. Xác nhận "0 câu Golden cần sửa" ⇒ bước 9 (bộ "sau") chấm theo Golden hiện tại (md5 `0f7dbf41b422`).
