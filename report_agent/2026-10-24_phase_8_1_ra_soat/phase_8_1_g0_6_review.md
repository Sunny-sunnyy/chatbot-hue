# Review: Phase 8.1 G0.6 — chuẩn bị khóa mốc (C31)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor) — trạng thái PREPARED đúng; khóa khi có câu kín
chính thức.
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 (`date` khi viết: sau 14:17)
Được kiểm: `phase_8_1_g0_6_baseline_lock.md` sha `b73d80ee1589`; manifest private `data/phase_8_1/baseline/g0_6_manifest.json`
sha `94859187080d`; script private `data/phase_8_1/tools/make_sealed_official.py` sha `4de4f31795ce`. B **không** mở nội dung
câu kín (chỉ tính hash file).

## 1. Đủ mục so spec

Spec §5 G0 bước 6: "commit, hash corpus, build record, retrieval 176 câu, 176 câu trả lời 7B Run 1, điểm Claude — chạy lại
retrieval phải giống từng byte mốc 7B". Manifest có đủ: `git.head`, `corpus.corpus_identity` + số file / đoạn,
`index.build_record` + `sparse_state`, `retrieval_baselines` (2 cách trộn, đã lưu + chạy lại + `byte_identical`),
`baseline_7b_run1.answers` + `claude_scores` (kèm ghi chú 10 câu đổi đáp án). Thêm (đúng việc A giao): split, gold, realism,
Golden official / smoke / 7 authoring, câu kín v6 (chỉ hash), nhãn câu kín, collection Qdrant. §6.1 / §6.4: report §4 đối
chiếu đủ.

Ghi chú: retrieval "176 câu" ra 158 dòng (bỏ 18 câu out_of_scope) — đúng như mốc 7B (`stored.lines` 158); không phải lệch.

## 2. B tính lại độc lập (chỉ đọc)

| Mục | sha256 (12) manifest | B tính | |
|---|---|---|---|
| build record | `03829ed641f7` | `03829ed641f7` | khớp |
| sparse state | `dbd5f7bc538d` | `dbd5f7bc538d` | khớp |
| split | `e2b1788dfbbc` | `e2b1788dfbbc` | khớp |
| gold | `bab707b9ab22` | `bab707b9ab22` | khớp |
| realism | `0b65d1c138d2` | `0b65d1c138d2` | khớp |
| 7B Run 1 answers / Claude | `32e2fb6d7035` / `c277f807ae20` | như trên | khớp |
| câu kín v6 (sha256 / md5) | `13fe5f7163dc` / `631334704fdd` | như trên | khớp |
| Golden official md5 | `0f7dbf41b422` | `0f7dbf41b422` | khớp |

Mốc byte runtime: B đã chạy lại nhiều lần trong ngày (lần cuối khi review G3) đều `cefb2d1a…`; C chạy 14:13 cả hai cách trộn —
dùng lại, không chạy thêm.

## 3. Script câu kín — có lộ nội dung không

- Chỉ in JSON: md5 nguồn / đích (12 ký tự), số dòng, phân bố `category`, `check_exit`, **số dòng** stderr. Không in câu,
  không in stdout / stderr của `check`. Lỗi đọc JSON / thiếu field sẽ raise `JSONDecodeError` / `KeyError` — thông điệp chỉ có
  vị trí / tên field, không có nội dung câu. **Không lộ.**
- Chặn đúng: md5 nguồn khác bản duyệt ⇒ dừng trước khi đọc; đích đã có ⇒ dừng; chỉ giữ 4 field theo thứ tự như `merge`
  (C đã thử trên foods: 37 dòng giống hệt Golden official).
- Đích nằm trong `knowledge-base-hue/` (gitignore) ⇒ private.

## 4. Findings

- **m1 — đích được ghi trước khi `check` chạy.** Nếu `check` exit ≠ 0, file `sealed_official.jsonl` vẫn còn và lần chạy lại bị
  từ chối ("exists"); xóa file có thể bị auto-mode chặn (bẫy đã biết). **Đóng khi** (một trong hai): ghi ra file tạm cạnh đích,
  chạy `check` trên file tạm, chỉ đổi tên khi exit 0; **hoặc** ghi rõ ở report §5 "check lỗi ⇒ xóa `sealed_official.jsonl` (nhờ
  User `!rm` nếu bị chặn) rồi sửa bản soạn theo quy trình C24–C26".
- **m2 — HEAD trong manifest đã cũ.** Manifest ghi `8a909e0`; HEAD hiện `23e0cbf` (A commit báo cáo User). Report §6 đã nói
  phải ghi lại khi khóa. **Đóng khi:** lúc khóa, cập nhật `git.head` + `dirty_paths` và thêm sha của script câu kín
  (`4de4f31795ce`) vào manifest để biết file chính thức do bản script nào tạo.

## 5. Kết luận

PREPARED đúng nghĩa: mọi mục khóa mốc có hash và tái lập được; chỉ còn câu kín chính thức (chờ User duyệt mẫu bản 5). Không
có gì chặn A khóa sau bước đó.

## 6. Kiểm lại phần sửa (report `14a1eb0dbe1e`, script `ce5ff542945b`)

- m1: script ghi `<đích>.tmp`, `check` trên file tạm, chỉ đổi tên khi exit 0; C thử cả hai nhánh trên file không kín (đạt ⇒ ra
  đích giống lần trước; lỗi ⇒ exit 1, chỉ còn `.tmp`, không in nội dung). Thông điệp in ra vẫn chỉ hash / số dòng / phân bố /
  exit — **đóng**.
- m2: report §5 ghi việc khi khóa: cập nhật `git.head` + `dirty_paths`, thêm sha script `ce5ff542945b` — **đóng**.

Kết luận giữ nguyên: **ready_for_user_confirmation**, không còn finding mở.
