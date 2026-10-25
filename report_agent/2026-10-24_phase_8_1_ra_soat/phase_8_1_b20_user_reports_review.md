# Review: Phase 8.1 — B20 báo cáo cho User (TIM_KIEM, SINH_CAU_TRA_LOI_API, CHIA_DOAN)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major; 2 minor đã đóng — §5)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25, viết xong trước 14:13 (giờ "14:20" ghi ở bản đầu là ước, không lấy bằng `date` — sơ suất, đã sửa; mốc chắc: §5 đóng lúc 14:14 theo `date`)

| File | Sha 12 (khớp tin B) |
|---|---|
| `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md` bản 5 | `536c99450528` |
| `BAO_CAO_SINH_CAU_TRA_LOI_API.md` bản 5 | `ea3f850571ca` |
| `BAO_CAO_CHIA_DOAN.md` bản 3 | `40e7fe8c6fd4` |

## 1. Phạm vi đã review

- Đọc exact diff cả 3 file.
- Đối chiếu từng số với các review C đã làm (G2, G3, G4, G4K) và report gốc G1 / G4 / G2 / G3. Phần G3 là việc của C nên C
  kiểm đúng ý.
- Kiểm theo mẫu `TEMPLATE_USER_REPORT.md`:
  - §1 có dòng 8.1 + "bạn cần quyết";
  - §3 trạng thái theo thang 5 mức;
  - §4 mục 25/10 có luật ghi trước, kết quả, giữ / bỏ, tiền;
  - §5, §6, Phụ lục.
- Lời thường, không chép corpus / Golden / câu kín: đạt cả 3 file. §2 giữ nguyên vì runtime không đổi: đúng.

## 2. Findings

- **m1 (minor) — CHIA_DOAN: ba chỗ nói mạnh hơn số đo.**
  1. §4 bảng: "512: tụt chắc chắn". Số đo là tụt có CI sau Holm (p Holm 0,018) ⇒ nên viết "tụt có ý nghĩa thống kê".
  2. §4 "Đọc kết quả": "ở 512 token, top-10 có thêm 5 câu". Thực tế 5 thắng / 1 thua so với H1 (ròng +4) ⇒ nên ghi "+5 / −1".
  3. §1 và §6: "bỏ kiểm tokenizer cũ an toàn (không đổi kết quả)". Chỉ số quyết không đổi, nhưng keyword có 1 câu tụt và cận
     dưới CI −3,41 vượt mức cho phép −2,0 (report G3 §3.1, §3.9). §5 đã ghi "1 câu tụt keyword"; §1 / §6 nên ghi cùng ý.

  **Đóng khi:** sửa 3 chỗ chữ trên.
- **m2 (minor) — TIM_KIEM: hai chỗ số chưa rõ tập.**
  1. Câu không dấu có hai con số MRR: §4 mục 3 ghi "0,73 → 0,19" (108 câu dev, G1.4), checklist §3 ghi "0,72 → 0,16" (88 câu số
     chính, G1 §7). Cả hai đều đúng nhưng người đọc sẽ thấy mâu thuẫn ⇒ ghi tập cạnh mỗi số, hoặc dùng một bộ.
  2. Checklist reranker: "11–14 s/câu (100 đoạn)". Đầu vào "100 ứng viên" là hợp hai nhánh, mỗi nhánh 100, tức 112–192 đoạn,
     trung vị 147 (G4 review m1) ⇒ nên viết "~150 đoạn".

  **Đóng khi:** sửa 2 chỗ trên.

**SINH_CAU_TRA_LOI_API: không có finding.** Mọi số khớp review G2: Đủ +0,26 / +0,27; từ chối nhầm 13 → 7 (G2.1a), 13 → 1
(P1); 2 câu ngoài kho bị trả lời; citation 4 → 8 / 9 (none / low); 0,157 USD cho ≈ 1.070 câu trả lời; nhóm đủ bằng chứng
0/13/0; nhiễu người chấm 2/88. Đính chính "4/22 → 0/22" khớp G1.6 và khớp `BAO_CAO_DANH_GIA.md` bản 2 của C.

Kiểm khớp chéo:
- Câu không dấu "1/32 vs 13/32", đề xuất "chỉ dùng bản bỏ dấu khi câu không dấu" và NFC: khớp `BAO_CAO_EMBEDDING_TU_KHOA.md`
  bản 3 của C.
- Phần G3 trong CHIA_DOAN tóm đúng report G3: 12 cách; mất 4 / 6 / 6 / 8 / 7 / 8 câu; B10 mất 6; S1–S3 không khác; ngân sách 750
  / 1.500.

## 3. Cách kiểm

Chỉ đọc diff và đối chiếu số với report / review đã có. Không chạy lại thí nghiệm, vì mọi số đã được tính lại ở review G1–G4,
G4K, G3.

## 4. Decision

**ready_for_user_confirmation.** B sửa m1, m2 (5 chỗ chữ) rồi A đóng B20. C không cần review lại cả file, chỉ kiểm diff 5 chỗ.

Tiền (C): **0 USD**.

## 5. Đóng m1, m2 (14:14)

B sửa bằng chữ. Bản mới: CHIA_DOAN `affc53f559ff`, TIM_KIEM `31143475f604`. C kiểm bằng grep đúng các dòng:
- **m1 (CHIA_DOAN):**
  - dòng 86: "tụt có ý nghĩa thống kê, p Holm 0,018";
  - dòng 92: "top-10: +5 / −1 câu";
  - dòng 25 / 143: thêm "1 câu tụt keyword vượt mức cho phép".

  ⇒ **đóng.**
- **m2 (TIM_KIEM):**
  - dòng 60: ghi tập "dev số chính: 32 / 88";
  - dòng 84: ghi tập "108 câu dev";
  - reranker: "~150 đoạn: hợp hai nhánh, mỗi nhánh 100".

  ⇒ **đóng.**
