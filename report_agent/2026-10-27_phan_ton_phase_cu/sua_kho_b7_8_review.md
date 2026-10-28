# Review: đợt sửa kho bước 7–8 (B82) — nhãn đoạn đúng v4 + quét Golden

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C76
Date: 11:26 28/10/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (User duyệt `937cf8969810`) §5 bước 7, 8; §6 "Gold v4: 0 trích dẫn mất"
Implementation report: `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b7_8_implementation.md` (B, 11:19 28/10)

File tracked này chỉ có số đếm, sha, số thứ tự edit / mã mục. Không chép nội dung kho, câu hỏi hay đáp án Golden. Không nêu chủ đề cạnh `case_index` (S40).

## 1. Phạm vi đã review

- Report B82 (đọc hết); spec §5 bước 7–8.
- `data/phase_8_1/tools/build_gold_v4.py` (`f4c8d35f9bf9`, đọc hết); `gold_v4_draft.jsonl` (`927bae1bf201`); `gold_v4_proposals.json` (`dc3626bfce11`).
- `golden_scan.py` (`5b1e4f0a0e1f`) và `golden_scan/result_*.jsonl` (59 dòng).
- C viết script kiểm độc lập (chỉ đọc, chỉ in số; nội dung chỉ đọc trong terminal của C):
  - `data/sua_kho_2026-10-27/review_c76_tools/gold_map.py` — dời trích dẫn theo **đúng thứ tự áp** từng edit trên văn bản trung gian;
  - `review_c76_tools/golden_stale.py` — quét 176 câu Golden theo phần chữ bị edit xóa / thay.
- Bốn điểm A dặn xét kỹ: §2 "Bốn điểm A hỏi".

## 2. Findings

Không có blocker hay major.

### Bốn điểm A hỏi

**(1) Hai trích dẫn bị edit chồng ở câu 27 — đề xuất đúng phép thay.** `gold_map.py` dời khoảng trích dẫn qua từng edit theo thứ tự áp (cách khác script B, vốn tìm `old` trong file
gốc). Kết quả:
- 2 trích dẫn bị chồng: quote 0 ← edit 100; quote 2 ← edit 101 + 102; cả hai thuộc mục K125; edit nằm gọn trong trích dẫn (`widened` [0, 0]);
- chữ C tính ra **trùng đề xuất của B**, và xuất hiện đúng 1 lần trong kho mới;
- văn bản "backup + 123 edit theo thứ tự" == kho thật.

Đề xuất chỉ thay đúng phần chữ edit đổi, không mở rộng ⇒ fact mà trích dẫn đỡ vẫn nằm trong trích dẫn. **Đúng, sẵn để User duyệt.**

**(2) Lệch với C68 — số của B đúng; C68 (C viết) đúng con số nhưng gọi sai tên.** C tính lại theo cả bốn tập edit (B73 có / không K091, có / không `diffs_them`). Bốn tập đều
ra 28 câu, 2 trích dẫn bị chồng, 64–66 trích dẫn trong file sửa. Không tập nào ra "24 câu / 3 chồng" theo đúng tên C68 dùng. Ba số của C68 khớp khi đếm theo **định nghĩa khác**:

| C68 viết | Thực ra là | Số đúng theo tên C68 dùng |
|---|---|---|
| "24 câu có trích dẫn trong file bị sửa" | 24 câu có trích dẫn **bị dời hoặc bị chồng** | **28** câu có trích dẫn trong file sửa |
| "66 trích dẫn lệch offset" | 66 trích dẫn **nằm trong file sửa** (22 cùng vị trí + 42 dời + 2 chồng) | **44** trích dẫn đổi vị trí / chữ (42 + 2) |
| "3 trích dẫn bị chồng" | 3 **cặp (edit, trích dẫn)** chồng nhau | **2** trích dẫn (một trích dẫn bị 2 edit chồng) |

Kết luận: B đếm đúng (108 / 22 / 42 / 2, 28 câu — C tái lập từng số). Lỗi là ở C68 (27/10) gọi tên sai, không phải lệch dữ liệu. Spec đã duyệt dẫn "3 trích dẫn bị chồng"
như một ước tính; bước 7 chạy theo dữ liệu thật nên không bị ảnh hưởng. C ghi bẫy này vào STATUS_C.

**(3) "0 câu Golden cần sửa" — kiểm độc lập đồng ý.** `golden_stale.py` quét **toàn bộ 176** câu, không chỉ 59 câu B quét:
- 123 edit có 52 đoạn chữ bị xóa / thay (≥ 2 từ hoặc có chữ số, không còn trong chữ mới);
- **23 câu** có đáp án / keyword chứa một đoạn như vậy, trong đó 9 câu ngoài 59 câu của B;
- C đọc cả 23 câu với edit tương ứng: **tất cả là trùng ngẫu nhiên** — giờ mở cửa, ngày tháng, khoảng cách của đối tượng khác, cụm từ phổ thông, hoặc tên có trong một
  danh sách của file khác. Không câu nào hỏi fact đã đổi.

Kiểm thêm theo **fact đổi thật** (đọc 7 edit có đổi nghĩa: số tháng, thành phần một gói vé, mức tiết kiệm / tổng giá mua lẻ, khoảng cách, mốc năm):
- tìm câu Golden nhắc cùng đối tượng ⇒ 10 câu;
- đọc cả 10: đều hỏi thuộc tính khác hoặc gói khác, không phụ thuộc fact đã đổi.

Từ đơn bị xóa / thay (12 từ) đều là hư từ / từ chung, hoặc tên đơn vị hành chính không có trong Golden. ⇒ **Đồng ý 0 câu Golden cần sửa** cho đợt 1. Bước 9 chấm theo Golden md5
`0f7dbf41b422`.

**(4) Report tracked có tả câu quá cụ thể không** ⇒ có, ở 2 chỗ: m-1 dưới.

### Minor

**m-1 — Report tracked nêu loại thông tin cụ thể cạnh `case_index`.** Vị trí: report §1, dòng "bị edit chồng" và "Tóm tắt" (câu 27, kèm loại chữ bị đổi); §2 "Ghi chú" (câu 5,
kèm loại thông tin còn cũ). Yêu cầu bị ảnh hưởng: `Session_Prompt.md` §5 — tả ở mức loại câu, không nêu "tên thông tin" cạnh `case_index` (S40); repo public. Tác động: nhỏ, không
chép nguyên văn (hook không bắt). Tiêu chí đóng: viết lại thành "câu 27: 2 trích dẫn bị edit đổi chữ (edit 100, 101, 102 — mục K125)" và "câu 5: ứng viên Golden đợt 2 (chi tiết
`data/sua_kho_2026-10-27/golden_de_xuat.md`)", bỏ loại thông tin. Phần lời thường "Tóm tắt" viết chung cho cả đợt (không kèm số câu) thì giữ được.

Ghi nhận (không phải finding):
- **Cách tìm edit chồng của `build_gold_v4.py`** dùng `old_text.find(e["old"])` trên **file gốc**. Edit dựng trên kết quả edit trước (ví dụ `diffs_them`) có `old` không có trong
  file gốc ⇒ có thể sót. Lần này không ảnh hưởng: `gold_map.py` (theo thứ tự áp) ra đúng cùng 2 trích dẫn và cùng 66 / 66 khoảng. Nếu dùng lại script cho đợt 2, nên đi theo thứ
  tự áp như `gold_map.py`.
- `gold_v4.jsonl` chưa có (đúng: chờ User duyệt); v1 / v2 / v3 sha giữ nguyên (`bab707b9ab22` / `2f5a347a71ff` / `3b1117cf59e9`).

## 3. Cách người kiểm chạy lại thật

Từ gốc repo, chỉ đọc, 0 USD:

```bash
uv run python -I data/sua_kho_2026-10-27/review_c76_tools/gold_map.py        # 4 tập edit + so với draft + đề xuất
uv run python -I data/sua_kho_2026-10-27/review_c76_tools/golden_stale.py    # 176 câu Golden
uv run python -I data/sua_kho_2026-10-27/tools/golden_scan.py               # script của B ⇒ 26 câu
```

Thêm (script inline):
- kiểm bản nháp v4: mỗi trích dẫn đúng 1 lần, đúng `start` / `end`; `quote_ids` hợp lệ; số trích dẫn / `required_facts` giống v3;
- đếm câu có trích dẫn bị dời / chồng;
- đọc diff 7 edit đổi fact và 33 câu Golden liên quan (trong terminal, không ghi ra file).

## 4. Kết quả quan sát

| Khẳng định của report | C thấy | Khớp |
|---|---|---|
| 174 trích dẫn: 108 file không sửa / 22 cùng vị trí / 42 dời / 2 chồng / 0 khác | `gold_map.py` (theo thứ tự áp): **108 / 22 / 42 / 2**; 28 câu có trích dẫn trong file sửa; 0 `old` không đúng 1 lần | ✓ |
| draft v4 đúng | 66 / 66 trích dẫn trong file sửa trùng khoảng + chữ của C; 108 / 108 ngoài file sửa giữ nguyên v3; 0 lỗi kiểm (đúng 1 lần, đúng vị trí, `quote_ids` hợp lệ); cấu trúc giống v3 | ✓ |
| 2 đề xuất câu 27, mỗi cái đúng 1 lần | trùng chữ C tính; đúng 1 lần; edit 100 / 101 + 102, K125, `widened` [0, 0] | ✓ |
| `gold_v4.jsonl` chưa tạo; v1–v3 không đổi | chưa có; sha như trên | ✓ |
| quét lớp 1 = 26 câu | `golden_scan.py` chạy lại: 26 câu, cùng danh sách | ✓ |
| 59 câu, quyết định "không" cả 59 | `result_*.jsonl`: 59 dòng, 59 "không" | ✓ |
| 0 câu Golden cần sửa | quét độc lập 176 câu + đọc 23 câu khớp + 10 câu cùng đối tượng của fact đổi: 0 câu cần sửa | ✓ |
| md5 Golden `0f7dbf41b422` | đúng | ✓ |

Ý nghĩa: bước 7 làm đúng — 0 trích dẫn mất, 2 trích dẫn cần User duyệt có đề xuất đúng. Bước 8 kết luận đúng — không câu Golden nào phải sửa ở đợt 1.

## 5. Giới hạn hoặc phần chưa chạy

- Quét Golden của C dựa vào phần chữ bị xóa / thay. Một edit chỉ **thêm** fact mới (không xóa chữ) mà mâu thuẫn ngầm với đáp án sẽ không bị bắt theo chữ. Để bù, C đọc các edit
  đổi nghĩa và câu Golden cùng đối tượng, nhưng không đọc toàn bộ 123 edit. C66 / C67 (27/10) đã đọc toàn bộ edit lúc review đề xuất.
- Không đọc câu kín (bước 8 chỉ quét Golden 176 câu).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** A trình User:
1. Duyệt 2 trích dẫn gold mới của câu 27. Sau đó B chạy `--approved` ⇒ `gold_v4.jsonl`, rồi đổi `GOLD_PATH` (việc riêng, có review).
2. Xác nhận "0 câu Golden cần sửa" ⇒ bước 9 (bộ "sau") chấm theo Golden hiện tại.

B sửa m-1 khi tiện (trước khi A commit report).

## 7. Kiểm phần sửa (11:28 28/10/2026)

m-1 **đóng**: report B82 dòng bảng §1 nay chỉ ghi "câu 27: 2 trích dẫn bị edit đổi chữ — edit 100, 101, 102, K125"; §2 ghi chú "câu 5: ứng viên Golden đợt 2 (chi tiết
`golden_de_xuat.md`)" — không còn loại thông tin cạnh `case_index`. Phần "Tóm tắt" lời thường nói chung về đợt (không kèm số câu) — giữ được. `overlap_scan` 0 trùng. Kết luận giữ
**ready_for_user_confirmation**.
