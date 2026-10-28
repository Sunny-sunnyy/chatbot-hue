# Review: B89 — thước "lỗi nặng" (bịa thêm H, sai điều kiện P0) — phần Golden

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C83
Date: 12:57 28/10/2026 (`date`)
Canonical guide: plan `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_plan.md` (A duyệt `d69481b2addb`; review C81 + vòng 2) §3, §4, §6, §9
Implementation report: `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_implementation.md` (B, 12:50 28/10)

File tracked này chỉ có số đếm, mã câu, loại câu (S40). Nội dung đọc trong terminal của C.

## 1. Phạm vi đã review

- Report B89 (đọc hết).
- Harness `data/loi_nang_2026-10-28/tools/loi_nang.py` (sha `58ecada9652f`): đọc phần `items_all`, `export` (tách lô), `check`, `flags`, `by_src` (sửa khóa), `crosscheck`, `accept`,
  `agreement`, `analyze`.
- Rubric `b1b2848be9c6` (C đã đọc ở bước câu âm).
- Chạy lại `check --judge 1/2`, `crosscheck --judge 1/2`, `accept --judge 1/2`, `agreement`, `analyze` (0 USD; không dựng lại ngữ cảnh nên không tải CPU / Qdrant).
- Đọc (đúng phần §5 report nhờ):
  - 11 ứng viên "judge có / code không thấy số" ở mỗi judge;
  - câu 20 (câu H duy nhất);
  - 2 câu P0_thiếu (144, 170);
  - 10 item ngẫu nhiên của judge 1 (seed `20261035`, ý + nhãn + đoạn nguồn được dẫn);
  - câu đối chứng (`controls_key.json`): kiểm bằng máy, rồi đọc 2 câu;
  - tách lô (`separation_clash_cases`).

## 2. Findings

Không có blocker hay major.

**m-1 — Nửa "câu lạc đề" của đối chứng dương quá dễ; báo recall tách theo loại.**
- Vị trí: report §2 dòng "recall câu chèn bịa 20 / 20" và `controls` ở §1.
- Bằng chứng: câu lạc đề chép nguyên một dòng kho của câu khác, kèm ký hiệu Markdown đầu dòng (ví dụ "- - **…:**") và `[n]` của ngữ cảnh khác. Ở 5 / 10 câu, việc chèn còn làm mất
  hoặc dời trích dẫn `[n]` gốc (C so tiền tố / hậu tố chung giữa câu gốc và câu chèn). Lạc đề lộ như vậy thì gần như chắc bị bắt, nên không đo được judge có bắt bịa **tinh** không.
- Tác động nhỏ, vì phần đo có ý nghĩa vẫn đạt: câu **đổi một con số** 10 / 10 ở cả hai judge, câu chèn điều kiện sai 12 / 12 ở cả hai.
- Tiêu chí đóng:
  - report §2 tách dòng recall thành "đổi số 10 / 10 · lạc đề 10 / 10" và ghi một câu: phần lạc đề dễ (có dấu Markdown), recall tin được dựa vào phần đổi số;
  - khi dùng lại `controls` cho bộ câu an toàn: bỏ ký hiệu Markdown đầu dòng của câu chèn và giữ nguyên `[n]` gốc.

Ghi nhận (không phải finding):
- **Sửa khóa `by_src`** (`:249-254`): lần đầu, mọi câu thật cùng khóa `"real"` nên 145 câu gộp thành 1. Nay khóa là `real:<case_index>`, có chú thích lý do. `crosscheck`, `accept`,
  `agreement`, `analyze` đều đi qua `by_src`. C chạy lại cả bốn ⇒ đầu ra giống byte file B nộp (§4) ⇒ số trong report là số **sau** khi sửa.
- **11 ứng viên "judge có / code không thấy số"** (cùng 11 ý ở hai judge) đều là **ý suy ra đúng** theo luật rubric:
  - so một giờ với khung giờ mở cửa;
  - tuổi nằm trong ngưỡng "từ đủ 60 tuổi" / "dưới 13 tuổi";
  - phép trừ, phép chia (600 − 130 = 470; 600 / 130 ≈ 4,6);
  - tháng nằm trong một mùa;
  - khác cách viết ngày (07/11 ↔ 7 tháng 11).
  ⇒ Không có bỏ sót bịa trong bảng ngược.
- **Câu 20 (câu H duy nhất) đúng là bịa thêm theo định nghĩa closed-world.** Câu trả lời gọi hai thương hiệu là "gà rán"; đoạn nguồn của hai thương hiệu đó không nói vậy (chỉ đoạn
  thương hiệu thứ ba có chữ "gà rán"). Đúng ngoài đời nhưng không có trong nguồn — mức nhẹ, như report ghi.
- **P0_thiếu đọc 2 câu (144, 170):** cả hai judge cùng ghi một điều kiện có trong ngữ cảnh mà câu trả lời không nêu. Một câu là cảnh báo theo mùa; một câu là giấy tờ đối chiếu độ
  tuổi. Đúng loại "thiếu điều kiện", và nhẹ hơn sai.
- **10 item ngẫu nhiên:** mọi ý gắn "có" đều có trong đoạn nguồn được dẫn, kể cả ý so sánh / gộp. Không thấy nhãn sai.
- Kappa H = 1,0 ở tỉ lệ H 1 / 145 chỉ cho thấy hai lượt nhất quán (report §4 đã ghi). Độ đúng dựa vào các cổng đối chứng + kiểm chéo số, và các cổng đó đều đạt.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, 0 USD. Trước khi chạy: ghi sha 6 file đầu ra (`data/loi_nang_2026-10-28/c_review/before.sha`).

```bash
L="HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/loi_nang_2026-10-28/tools/loi_nang.py"
for c in "check --judge 1" "check --judge 2" "crosscheck --judge 1" "crosscheck --judge 2" "accept --judge 1" "accept --judge 2" agreement analyze; do eval $L $c; done
```

Thêm (script inline, chỉ đọc, in ra terminal):
- kiểm đối chứng: mỗi câu chèn chỉ thay một đoạn liền của câu gốc; câu chép nguyên văn có trong ngữ cảnh;
- đếm recall theo loại;
- đọc ngữ cảnh cho 4 ứng viên cần tính (tuổi, giờ, phép tính) và cho câu 20.

## 4. Kết quả quan sát

| Khẳng định của report | C thấy | Khớp |
|---|---|---|
| `check` | 187 / 187 mỗi judge, 0 lỗi schema, 0 thiếu / thừa | ✓ |
| `crosscheck` | judge 1: 162 ý có số, 0 "không có mà code thấy", 11 ngược; judge 2: 158, 0, 11 | ✓ |
| `accept` | cả hai: recall 20 / 20, báo nhầm 0 / 10 + 0 / 15, P0 12 / 12, kiểm chéo 0,0, tách lô 0 ⇒ mọi cổng `true` | ✓ |
| recall theo loại (C đếm thêm) | đổi số 10 / 10 · lạc đề 10 / 10 · chèn điều kiện 12 / 12 — cả hai judge | ✓ (m-1) |
| `agreement` | kappa H 1,0; đồng ý thô 1,0; H mỗi judge 1 / 145; kappa `p0_relevant` 0,887; 0 bất đồng H / P0_sai | ✓ |
| `analyze` | H 1 / 145 [0,1 %; 3,8 %]; H số chính 0 / 121 [0; 3,1 %]; H_trái 0 / 145; `p0_relevant` 65; P0_sai 0 / 65 [0; 5,6 %]; P0_thiếu 7 / 65 [5,3 %; 20,6 %] | ✓ |
| đầu ra giống byte khi chạy lại | `judge1/crosscheck.json` `3a0dfeba0cf2`, `judge2/crosscheck.json` `f96beb64ce00`, `accept_judge{1,2}.json` `efe98703844e`, `analyze.json` `135b387cb037`, `per_case.json` `aa1b35bfc6b2` — trước = sau | ✓ |
| tách lô | `separation_clash_cases` 0 / 0 | ✓ |
| câu chèn đúng một chỗ | mỗi câu chèn chỉ thay một đoạn liền của câu gốc; câu chép nguyên văn có trong ngữ cảnh | ✓ (m-1 về độ dễ) |
| câu âm C xác nhận dùng đúng | `accept` đọc `negatives_c_confirm.json` (15 câu) | ✓ |

**Ý nghĩa:** thước "bịa thêm" và "sai điều kiện" dùng được làm **mốc**. Trên chatbot hiện tại: 1 / 145 câu bịa nhẹ, 0 câu nói ngược nguồn, 0 / 65 câu sai điều kiện, 7 / 65 câu
thiếu một điều kiện. Số vẫn **tạm** tới khi có người đọc mẫu (plan §4).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại `contexts`, `controls`, `export` (từ chối ghi đè) hay lượt chấm. Bằng chứng ngữ cảnh dựng lại là lần C chạy `b87_ctx_check.py` ở review plan (176 / 176, Δ41),
  cùng code và cùng index.
- Chỉ đọc 10 item ngẫu nhiên của judge 1; không đọc toàn bộ 145 câu hay judge 2 theo từng item (hai judge đồng ý 100 % ở H).
- Mẫu người 20 câu chưa có (User).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** B sửa m-1 khi tiện (một dòng §2 + ghi chú cho bộ câu an toàn). Tiếp theo theo plan §11: B soạn bộ câu an toàn, C kiểm câu trước khi sinh.
