# Implementation Report: C32 — rà nội dung kho (mâu thuẫn + thông tin có thể cũ)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-d6`)
Date: 2026-10-25 16:37
Việc: `session_prompt/CURRENT_HANDOFF.md` "Việc đang mở" C32 (User duyệt 16:1x, A giao 16:20). Review: A.

Report này **không chép nội dung kho** (repo public). Danh sách đầy đủ, có `file:dòng` và trích dẫn, ở file private
`data/ra_soat_kho_2026-10-25/danh_sach.md`.

## 1. Phạm vi

- Đã duyệt: rà chỉ đọc 205 file runtime tìm chỗ kho tự mâu thuẫn và thông tin có thể đã cũ; 0 USD; không sửa kho, không
  web, không mở câu kín / Golden; loại `evaluation/`, `meta/`, `*sealed*`.
- Đã làm: đúng phạm vi trên. Không sửa file kho nào; không gọi API trả phí; không tra web.

## 2. Thay đổi chính

Không đổi code, kho hay chatbot. File mới:

| File | Vai trò | Tracked? |
|---|---|---|
| `data/ra_soat_kho_2026-10-25/files.txt` | 205 file lấy bằng discovery thật (`discover_full_corpus_files`) | private |
| `data/ra_soat_kho_2026-10-25/tools/extract_facts.py` | gom dòng có chữ số hoặc từ chỉ thời điểm ("hiện nay", "sắp", "dự kiến", "từ ngày"…) kèm heading | private |
| `data/ra_soat_kho_2026-10-25/tools/split_groups.py` | chia thành 8 nhóm cho sub-agent, không cắt đôi một file | private |
| `data/ra_soat_kho_2026-10-25/tools/grep_kb.sh` | grep chỉ trong 205 file runtime (để sub-agent không chạm `evaluation/`, `meta/`, câu kín) | private |
| `data/ra_soat_kho_2026-10-25/tools/brief.md` | brief chung của 8 sub-agent | private |
| `data/ra_soat_kho_2026-10-25/sub_g{1..8}_*.md` | bảng của từng sub-agent | private |
| `data/ra_soat_kho_2026-10-25/tools/merge.py` | gộp, bỏ trùng (cùng cặp `file:dòng` + gộp tay theo nghĩa `SAME`), chọn mẫu tự kiểm, ghi `danh_sach.md` | private |
| `data/ra_soat_kho_2026-10-25/tools/show_refs.py` | in dòng gốc tại mọi `file:dòng` của mục được chọn để tự kiểm | private |
| `data/ra_soat_kho_2026-10-25/danh_sach.md` | **danh sách đầy đủ 139 mục** + mục "Tự kiểm của C" | private |
| file này | cách làm, số đếm | tracked |

## 3. Cách đã chạy thật

```bash
# 205 file từ discovery thật (settings.yaml full_corpus.knowledge_base)
cd backend && HF_HUB_OFFLINE=1 uv run python -I -c "…discover_full_corpus_files()…"   # -> files.txt
uv run python -I data/ra_soat_kho_2026-10-25/tools/extract_facts.py    # 3.901 dòng có số / từ chỉ thời điểm
uv run python -I data/ra_soat_kho_2026-10-25/tools/split_groups.py     # 8 nhóm
# 8 sub-agent general-purpose chạy song song, mỗi nhóm một brief (tools/brief.md) + ghi chú riêng
uv run python -I data/ra_soat_kho_2026-10-25/tools/merge.py            # gộp + mẫu tự kiểm (seed 20261025)
uv run python -I data/ra_soat_kho_2026-10-25/tools/show_refs.py <42 id>  # C tự đọc dòng gốc
```

Cách rà: script gom dòng có chữ số / từ chỉ thời điểm của từng file. Mỗi sub-agent đọc hết phần của nhóm mình, mở file
gốc để xem ngữ cảnh, và tìm cùng thực thể ở các file ngoài nhóm qua `facts_*.txt` hoặc `grep_kb.sh`. Mỗi sub-agent tự kiểm
lại mọi `file:dòng` trước khi ghi, rồi C gộp và tự kiểm.

**Phủ file** (khớp discovery):

| Domain | File | Nhóm sub-agent | Mục thô |
|---|---:|---|---:|
| `foods` | 91 | g7 | 26 |
| `heritages` | 29 | g3 (12) + g4 (17) | 18 + 20 |
| `festivals` | 27 | g6 (cùng `travel/services`) | 12 |
| `performing_arts` | 13 | g5 | 18 |
| `travel/places` | 36 | g1 (20) + g2 (16) | 21 + 24 |
| `travel/tickets` | 5 | g8 | 23 |
| `travel/services` | 4 | g6 | (trong 12) |
| **Tổng** | **205** | 8 nhóm | **162** |

Cả 205 file đều có ít nhất một dòng được gom; cả 8 sub-agent báo đã rà hết file của nhóm (g5 cần vòng 2, xem §5).

## 4. Kết quả quan sát

**162 mục thô → 139 mục.** Đã bỏ 5 mục trùng cặp `file:dòng`, và gộp tay 18 mục cùng một vấn đề mà nhiều nhóm cùng thấy
(bảng `SAME` trong `merge.py`).

| Loại × mức chắc | Theo sub-agent | Sau tự kiểm của C |
|---|---:|---:|
| mâu thuẫn — chắc | 23 | 22 |
| mâu thuẫn — có thể | 53 | 53 |
| có thể cũ — chắc | 4 | 4 |
| có thể cũ — có thể | 33 | 33 |
| khác — chắc | 5 | 5 |
| khác — có thể | 21 | 22 |
| **Tổng** | **139** | **139** |

- **Phía 1 theo domain:** `travel/places` 41, `heritages` 34, `foods` 26, `performing_arts` 17, `travel/tickets` 12,
  `festivals` 9.
- **Đề xuất:** tra ngoài qua ChatGPT 69, sửa khi build lại 53, User biết thì báo 16, đã biết 1.
- **Nhóm lỗi lớn nhất (quan sát):** 25 mục dính tên đơn vị hành chính sau sắp xếp 01/07/2025. Có ba dạng: còn dùng tên
  phường / xã cũ như hiện hành; hai file ghi hai phường mới khác nhau cho cùng một điểm; vẫn ghi "quận" trong khi file khác
  nói đã bỏ cấp huyện. Sửa theo lô một lần khi build lại thì rẻ hơn sửa từng mục.
- Các dạng còn lại: giá / hạn vé / tên tuyến combo lệch giữa file di tích và file vé; năm, niên hiệu, tước hiệu lệch giữa
  hai file; giờ mở cửa / địa chỉ hai nguồn trong cùng một file quán; tiến độ dự án hoặc lịch lễ hội gắn một năm cụ thể; một
  lỗi cộng tổng trong bảng vé (C tính lại từ bảng giá: tổng thật khác số ghi).

**Tự kiểm của C** (seed `20261025`): 10 mục ngẫu nhiên + 32 mục "chắc" = 42 mục. C đọc dòng gốc tại mọi `file:dòng` (dòng
dài thì in quanh từ khóa) và so với phần "quan sát".

- Trích đúng file / dòng / giá trị: **42/42**.
- Mức chắc C điều chỉnh: 4 mục (K007, K021, K075, K098), ghi lý do ở cuối `danh_sach.md`. Bảng trong file vẫn giữ nguyên lời
  sub-agent.

**Phát hiện cần A xem (ngoài phạm vi nội dung):**

1. **Mẫu Hải Vân trong `CURRENT_HANDOFF.md` "Câu hỏi cho User" mục 3 không phải mâu thuẫn về thời gian.** Hai sub-agent
   (g2, g8) thấy, C đã kiểm: chính file `travel/places/Đèo Hải Vân.md` ở dòng 86–88 cũng ghi mốc thu phí mới, khớp với file
   vé. Rủi ro còn lại chỉ là một chunk chứa dòng 84 (câu miễn phí cũ) mà thiếu dòng 86 thì đọc riêng sẽ sai. Câu hỏi gửi User
   nên sửa lại.
2. **`performing_arts/performing-arts-entities-inventory.md` tự ghi (dòng 16–17) là phải loại khỏi nguồn ingestion,
   nhưng vẫn nằm trong 205 file runtime và trong build record của index đang chạy.** `settings.yaml` `exclude_files` chỉ
   loại 2 file inventory của travel. Đây là chuyện data contract / cấu hình index, C không tự sửa. File này còn trỏ tới hai
   đường dẫn heritages không tồn tại (mục K091).

## 5. Lỗi và giới hạn

- **Lỗi brief của C (đã sửa):** brief cấm mọi file `*inventory*`, nên lượt đầu g5 bỏ qua file inventory của
  `performing_arts`, dù file này là runtime. C đính chính và g5 đã rà nốt (13/13). Không nhóm nào khác có file inventory
  runtime (kiểm `files.txt`: chỉ 1 file).
- **Phương pháp:** đầu vào chính là dòng có chữ số / từ chỉ thời điểm. Mâu thuẫn không có số (tên, thuộc tính) chỉ thấy khi
  sub-agent mở file gốc xem ngữ cảnh, nên có thể còn sót. Vẫn tìm được vài mục loại này (xếp điệu nhạc, tước hiệu, số gian).
- Đối chiếu chéo nhóm do từng sub-agent tự chọn thực thể để tìm, không so từng cặp file một cách vét cạn.
- "Chắc" chỉ dựa trên kho (closed-world): hai giá trị trong kho không thể cùng đúng. Kho **sai ở phía nào** thì chưa biết
  (cần User hoặc tra ngoài). Một mục (K075) chỉ dựa hiểu biết chung của sub-agent, đã đánh dấu.
- Tự kiểm 42/139 mục. 97 mục còn lại chỉ có lần tự kiểm của sub-agent.
- Gộp tay theo nghĩa (18 mục) là phán đoán của C khi đọc bản rút gọn, có thể còn sót mục trùng nghĩa.
- `grep` của môi trường là ugrep: regex dài báo "exceeds complexity limits". Sub-agent và C phải tách regex ngắn hoặc dùng
  Python; không thấy ảnh hưởng tới kết quả.
- Chi phí: 0 USD API. Quota Claude Code cho 8 sub-agent khoảng 2,1 triệu token (tổng `subagent_tokens`, gồm vòng 2 của g5).

## 6. Bàn giao cho người kiểm

- Đọc trước: file này → `data/ra_soat_kho_2026-10-25/danh_sach.md` (bảng + "Tự kiểm của C") → `tools/brief.md`.
- Chạy lại phần tự kiểm: `uv run python -I data/ra_soat_kho_2026-10-25/tools/show_refs.py K001 K042 …` (in dòng gốc).
  `merge.py` tái lập được `danh_sach.md` từ 8 file `sub_g*.md`.
- Gợi ý rủi ro để kiểm: (1) mục gộp tay `SAME` có gộp nhầm hai vấn đề khác nhau không; (2) vài mục "chắc" ngoài mẫu 42;
  (3) hai phát hiện §4 (Hải Vân, file inventory).
- Không commit (C không có quyền commit). File tạm ở `/tmp`: không có (`ls -d /tmp/c32_*` rỗng lúc 16:3x); mọi script
  để ở `data/ra_soat_kho_2026-10-25/tools/`.
