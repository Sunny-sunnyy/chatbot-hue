# Review: C32 — rà nội dung kho

Decision: **ready_for_user_confirmation**
Người kiểm: A (Claude Opus 5.5, terminal `hue-rag-00`) · 2026-10-25 16:40 (`date`)
Bản được review: `ra_soat_kho_implementation.md` (C, 16:37) + `data/ra_soat_kho_2026-10-25/danh_sach.md` (private)

## 1. Phạm vi đã review

Report C32 toàn bộ; đầu bảng `danh_sach.md`; đọc dòng gốc trong kho cho 4 khẳng định (lệnh chỉ đọc `sed`, `grep`). Không mở
`evaluation/`, `meta/`, câu kín. Report tracked kiểm theo `Session_Prompt.md` §5: chỉ tên file + số đếm, không chép nội dung kho.

## 2. Kiểm độc lập

| Khẳng định | A kiểm | Kết quả |
|---|---|---|
| Hải Vân không phải mâu thuẫn thời gian (file đèo :86–88 có mốc thu phí mới) | đọc `travel/places/Đèo Hải Vân.md:82-89` | ✓ — câu hỏi cho User mục 3 phải sửa |
| File inventory `performing_arts` tự ghi "phải loại khỏi ingestion" (:16–17) và nằm trong build record runtime | đọc :14–18; `grep -c` trong `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` = 1 | ✓ — trùng mục 0.2 của bảng rà 8.1 (S1 bỏ 33 đoạn: không khác) |
| K002 (mâu thuẫn chắc, cùng file) | đọc 2 dòng gốc | ✓ |
| K004 (địa chỉ còn "quận" sau 01/07/2025) | đọc dòng 8 một file chợ + dòng 210 file vé | ✓ |
| Phủ 205 / 205 file theo discovery thật | bảng §3 (91 + 29 + 27 + 13 + 36 + 5 + 4 = 205) | ✓ (số cộng) |

## 3. Findings

Không có blocker / major.
- minor a: 97 / 139 mục chỉ có lần tự kiểm của sub-agent — đã ghi ở §5; khi sửa kho (đợt build lại) mỗi mục phải đọc lại dòng gốc
  trước khi sửa (luật backup + diff `Session_Prompt.md` §5).
- minor b: "Chắc" là closed-world (hai giá trị không cùng đúng), chưa biết phía nào đúng — report ghi đúng; khi trình User nói rõ.
- Ghi nhận: C tự phát hiện lỗi brief (cấm `*inventory*` theo tên) và rà bù; ghi vào sổ cải tiến nếu lặp lại.

## 4. Kết luận và bước tiếp

ready. Kho **không sửa** ở 8.2 (spec 8.2 §4 Ngoài). Danh sách là đầu vào cho đợt build lại index. A sửa câu hỏi Hải Vân trong
`CURRENT_HANDOFF.md`; 69 mục "tra ngoài" cần một yêu cầu ChatGPT riêng khi User muốn (chưa giao).
