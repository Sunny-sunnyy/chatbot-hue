# Review: C93 — đo "chatbot không biết hôm nay là ngày nào" (plan B96)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 0 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-24`) · Date: 14:41 30/10/2026 (`date`) · Việc: A giao (tin 14:3x 30/10), chỉ đọc + tính lại, 0 USD.
Implementation report: `ngay_hien_tai_implementation.md` (`1603cc52aaf4`). Plan: `data/ngay_hien_tai_2026-10-30/plan_nhap.md` bản 2 `fd63d9192ef6` (B viết; C92 review; A duyệt).
File này không chép câu hỏi / câu trả lời / chữ kho — chỉ mã câu, số đếm.

## 1. Đã kiểm (tính lại từ dữ liệu thô, không dùng số của report)

| Khẳng định | Cách B kiểm | Kết quả |
|---|---|---|
| Phiếu kiểm người chấm 6 / 6 cả hai judge | so `judge/round0_labels_j{1,2}.jsonl` + `round0_map.json` với khóa B viết (`phieu_kiem_key.json` `1eb110b6551c`) | 6 / 6 và 6 / 6 ✓ |
| `n_L1L2` = 0 trên 12 câu quyết (R1–R4, R6–R9, R11, R12, E2, E3), "một trong hai judge" | đếm từ `round1_labels_j{1,2}.jsonl` qua `round1_map.json` | 0 ✓ (nhãn chỉ có OK 40 / R 12 trên 52 nhãn) |
| Bộ an toàn 11 câu: L1 / L2 = 0 | như trên, 11 mục `safe:` | 0 ✓; 11 / 11 câu trả lời **giống hệt** lượt "sau" đợt 2 (`sau_dot2_2026-10-30`), đúng nhóm giờ + miễn giảm (11 câu) |
| R11 (ngoài kho) từ chối | nhãn hai judge + cờ `refusal` của câu trả lời | OK / OK; `refusal` true ✓ |
| L3 = 0; đối chứng R10, E1, U1 OK; bất đồng 0 / 26 | đếm | ✓ |
| 6 / 14 câu trong kho bị từ chối: R3, R6, R7, R8, R9, R12 | nhãn R của judge + cờ `refusal` do máy tính trong `answers_r1.jsonl` | trùng đúng 6 câu ✓ |
| **4 câu (R3, R6, R7, R8) có lịch đúng trong ngữ cảnh** | đọc dòng `kho_ref` từ kho, tìm trong `context` model đọc (bỏ dấu Markdown, so 60 ký tự đầu) | R3 1 / 1 dòng; R6 2 / 2; R7 4 / 5 (nhiều làng); R8: dòng mục mùa đông 0 / 3 nhưng **3 / 4 tiêu đề mục "lễ hội theo mùa" + 11 dòng thân** của file hướng dẫn có trong ngữ cảnh — đủ để "liệt kê theo mùa" (= OK theo `expected`) ⇒ ✓ cả 4 |
| R9, R12 không có lịch trong ngữ cảnh (lỗi tầng tìm) | như trên | R9 0 / 2; R12 0 dòng suất diễn (câu R4 cùng chương trình có 4 / 4) ✓ |
| Judge không biết ngày chạy | grep ngày / thứ trong `judge_brief.md` + 2 file lô | chỉ khớp chữ trong câu hỏi R11 và định nghĩa L1 — không lộ ngày ✓ |
| Pilot 3 câu trước, trần 0,01 | `pilot/answers.meta.json` (14:31:37, 3 câu) rồi `main/` (14:33:06, 12 câu) | ✓ |
| Tiền 0,0037029 USD | 0,0010797 + 0,0026232 | ✓ |
| Harness `an_toan_run.py` `d509d90a8ef8` | B đã kiểm diff trước khi chạy (chỉ thêm `--questions`) | ✓ |

## 2. Findings

Không có. Report đúng plan: chỉ số quyết, sàn, kết luận ghi trước ("chưa thấy lỗi ở 12 + 11 câu ⇒ không sửa"), và tách rõ phát hiện ngoài chỉ số quyết (từ chối nhầm) là
"theo dõi, không quyết" kèm nhãn [Đo] / [Suy ra].

Ghi chú cho A (không phải finding):
- Phát hiện "từ chối nhầm câu hỏi theo ngày tương đối" **đứng được**: 4 / 7 câu `conditional` bị từ chối dù ngữ cảnh có lịch; cặp đối chứng cùng thông tin (U1 không ngày,
  E3 ngày rõ) được trả lời đúng. Giả thuyết của C (prompt "không đủ bằng chứng ⇒ từ chối" gặp câu phụ thuộc hôm nay) hợp lý nhưng chưa chứng minh — phải đo khi thử P3 / P1–P2.
- n nhỏ (12 câu quyết) ⇒ "0 lỗi đoán ngày" chỉ cho cận trên ~25 % (report đã ghi).
- R7 có 1 / 5 dòng nguồn không vào ngữ cảnh (một làng khác) — không đổi kết luận "có lịch trong ngữ cảnh".

## 3. Giới hạn review

- Không chạy lại lượt sinh (có phí) và không chấm lại; nhãn thô được đếm lại. So chuỗi bằng 60 ký tự đầu sau khi bỏ dấu Markdown — đủ để biết dòng có mặt, không đọc nghĩa.
- B là người viết plan + bộ câu + phiếu kiểm (C chạy) ⇒ B kiểm phần chạy của C, không tự kiểm thiết kế của mình (C92 đã review plan).

## 4. Kết luận

`ready_for_user_confirmation`: kết quả "0 lỗi đoán ngày ⇒ không sửa prompt" và phát hiện "từ chối nhầm câu hỏi theo ngày tương đối (M5)" đều đúng với dữ liệu. Việc mở plan sửa
(P3 hoặc P1 / P2) là quyết định của User qua A.
