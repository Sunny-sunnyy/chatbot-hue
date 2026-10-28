# Review: đợt sửa kho bước 9 — đo "trước ↔ sau" (B83)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C80
Date: 12:10 28/10/2026 (`date`)
Canonical guide: plan `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_do_truoc_sau_plan.md` (A duyệt `41485782b39e`) §4, §7; spec sửa kho `937cf8969810` §6
Implementation report: `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b9_implementation.md` (B, 12:01 28/10)

File tracked này chỉ có số đếm, mã câu, loại câu (S40). Nội dung câu chỉ đọc trong terminal của C.

## 1. Phạm vi đã review

- Report B83 bước 9 (đọc hết).
- `data/sua_kho_2026-10-27/tools/truoc_sau.py` (sha `61e9dcc863e1`, 514 dòng): đọc phần đổi so với bản C đã review (`e3a036c8e149`):
  - `why()` `:413-421` — nhãn câu tụt theo tập `chunk_id`, có nhãn phụ "chỉ đổi thứ tự";
  - `export_judge` `:317-320` — dừng khi md5 Golden ≠ `preflight_sau`;
  - `rerun-f4` `:485-491` — nhãn context giống / khác.
- Chạy lại `check --arm sau`, `check-judge`, `analyze`. Đối chiếu từng số trong bảng §2 của report với `analyze.json`.
- Đọc câu tụt nhãn "nhiễu" (50, 93, 143), câu W8 (17, 20, 21), và kiểm riêng kết luận W5 (A dặn).

## 2. Findings

Không có blocker hay major.

**m-1 — Kết luận W5 "provider chậm theo giờ, không do kho" đúng hướng, nhưng phải nói rõ hai điều.**
- Vị trí: report "Tóm tắt" (dòng "Thời gian chờ") và §2 dòng W5.
- Bằng chứng C tính lại (từ `sau_{pilot,rest}.jsonl`, thứ tự append = thứ tự chạy):
  - 10 câu chậm nhất đều ở vị trí 146–171 / 176 (khúc cuối, ước 11:51:31–11:56:53 theo cộng dồn `wall_ms` từ `sau_rest.meta.json` `started`);
  - thời gian sinh của chúng 9,4–18,6 s, trong khi **cùng câu** ở lượt "trước" chỉ 2,0–5,9 s; token ra chênh −45 … +77;
  - phần chạy trên máy (`wall_ms − latency_ms`) 32–78 ms, bình thường;
  - chia lượt "sau" làm 4 khúc: ba khúc đầu ms / token ra trung vị 34–44, như lượt "trước" (32–41). **Khúc 4: 92,7 ms / token**, so với 32,1 ở cùng các câu đó trong lượt
    "trước"; token TB 105,8 so với 99,3.
  - ⇒ Chậm đi là do **tốc độ sinh mỗi token** tăng gần 3 lần trong khoảng 5 phút cuối, không do câu trả lời dài hơn, không do phần tìm trên máy. Kết luận "không do kho" đứng.
- Hai điều phải nói rõ:
  - (a) "provider" nên viết là **"phía mạng / provider"** — dữ liệu không tách được mạng của máy User với phía OpenAI;
  - (b) **C tự khai:** trong khoảng 11:50–11:56, C chạy trên cùng máy vài việc **không trả phí** nhưng dùng CPU / Qdrant, đúng lúc lượt "sau" của B đang chạy. Cụ thể: chạy khô
    `touched` (review code B83), quét toàn bộ payload Qdrant + đếm token kho bằng tokenizer e5, chạy mốc tầng tìm e5 cho plan C78. Phần trên máy của B không tăng
    (trung vị 37 ⇒ 45 ms), và tải CPU ngắn khó làm chậm một lần gọi mạng 5–15 s ⇒ ít khả năng là nguyên nhân. Nhưng không loại trừ được bằng dữ liệu.
- Tác động: W5 chỉ là dòng theo dõi, không đổi kết luận "không làm hỏng". Nhưng p95 9,8 s của lượt "sau" **không** được dùng làm số latency của chatbot sau sửa kho.
- Tiêu chí đóng: sửa câu W5 thành "phía mạng / provider chậm ở ~5 phút cuối lượt (ms / token ×2,9 so với cùng câu ở lượt trước); phần tìm trên máy không đổi; có việc
  không trả phí của C chạy cùng lúc (11:50–11:56) — ít khả năng ảnh hưởng"; ghi "p95 sau không đại diện, cần đo lại nếu dùng".

Ghi nhận (không phải finding):
- **Nhãn câu tụt đổi sau lần `analyze` đầu** (report §3): từ tập (nguồn, `evidence_parts`) sang tập `chunk_id`. Đây là nhãn giải thích, không phải tiêu chí quyết. B đã ghi rõ, và
  chỉ đổi nhãn của câu 50. Lập luận "không chạm ⇒ cùng `chunk_id` = cùng chữ" cần số đoạn mỗi file không đổi. C kiểm bằng `chunks_{truoc,sau}.json`: **mọi file giữ nguyên số
  đoạn**, chỉ file danh mục bị loại (33 ⇒ 0); 8.426 id chung đều cùng nguồn ⇒ lập luận đứng.
- `run-experiment` §4: "chỉ số theo dõi tụt mạnh ⇒ báo dù luật nói giữ" — W5 đã báo (m-1 chỉ sửa cách nói nguyên nhân).

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, Qdrant chỉ đọc, 0 USD. Trước khi chạy: sha `analyze.json` `caa608ed4f8d`, `check_sau.json` `9761e10924b9` (`data/sua_kho_2026-10-27/review_c80/before.sha`).

```bash
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/tools/truoc_sau.py check --arm sau
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/tools/truoc_sau.py check-judge
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/tools/truoc_sau.py analyze
```

Thêm (script inline, chỉ đọc, in ra terminal):
- đếm đoạn mỗi file trong `chunks_truoc` / `chunks_sau`;
- tính thời gian sinh / thời gian trên máy / token theo vị trí trong lượt;
- in câu hỏi + đáp án + hai câu trả lời của 6 câu ở §4 (nạp `scored()` của harness).

## 4. Kết quả quan sát

| Khẳng định của report | C thấy | Khớp |
|---|---|---|
| `check` / `check-judge` / `analyze` | chạy lại: `analyze.json` `caa608ed4f8d`, `check_sau.json` `9761e10924b9` — **giống byte**; check-judge 303 / 303, 0 lỗi | ✓ |
| F1 / F2 / F3 / F4 | 0 / 0 ứng viên (không rejudge) / 0 / 0 | ✓ |
| T1 Completeness 129 | −0,0078 [−0,062; +0,0388], 4 / 121 / 4; không chạm (98) 0,000 [−0,051; +0,051] | ✓ |
| T2 Accuracy 129 | 0,000 [−0,0233; +0,0233], 1 / 127 / 1; không chạm +0,0102 [0,000; +0,0306] | ✓ |
| T3 | 12 ⇒ 13 (≤ +1) | ✓ |
| Tập chạm | số chính 31 / 129, không chạm 98 | ✓ |
| W1–W4, W6, W8 | khớp từng số trong bảng report (W1 −0,0323 / −0,0323; W2 5 ⇒ 7; W3 −0,0078; W4 0,0002053 ⇒ 0,0002071; W6 40 câu đổi top-10, 0,7615 ⇒ 0,7615, mất 0 / thêm 0; W8 17, 20, 21) | ✓ |
| W5 p50 / p95 | 2.207,7 / 4.883,6 ⇒ 2.782,1 / 9.763,0 | ✓ (nguyên nhân: m-1) |
| Code sửa theo review C (m-1, m-2, m-3) | có, đúng tiêu chí đóng | ✓ |

**Đọc câu (plan §7):**

| Câu | Loại câu | Context hai bên | Kết luận của C |
|---|---|---|---|
| 50 | so sánh | giống hệt (cả thứ tự) | hai câu trả lời cùng fact, cùng nguồn; chỉ đổi dạng citation. Tụt 1 điểm Completeness là **nhiễu chấm**. Không lỗi kho |
| 93 | điều kiện | giống hệt | cùng kết luận, cùng fact; bản "sau" thêm một chi tiết có trong context. Tụt 1 điểm là **nhiễu sinh / chấm**. Không lỗi kho |
| 143 | điều kiện | giống hệt | cùng kết luận; bản "sau" bỏ mốc thời gian của mùa (có trong context) ⇒ tụt Completeness là **nhiễu sinh**. Không lỗi kho |
| 17 (W8) | nhiều nguồn | giống hệt | cùng fact, cùng thiếu một ý so với đáp án ở **cả hai** bên ⇒ **khác cách diễn đạt** (không sai fact) |
| 20 (W8) | nhiều nguồn | giống hệt | cùng danh sách, cùng thiếu một mục ở cả hai bên; bản "sau" diễn đạt như danh sách đủ ⇒ **khác cách diễn đạt** (không sai fact mới; thiếu ý có từ trước) |
| 21 (W8) | nhiều nguồn | khác (câu chạm) | cùng fact, cùng thiếu một ý ở cả hai bên ⇒ **khác cách diễn đạt** |

⇒ 0 câu có lỗi kho mới; 0 câu W8 "sai fact".

**Ý nghĩa:** kết luận "không làm hỏng" đứng. Đợt sửa kho không làm chatbot tệ đi ở bất kỳ sàn hay mức tụt nào. Không thấy "tốt hơn" theo Golden — đúng như plan dự báo (Golden không
đổi, edit phần lớn thêm tên mới).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại lượt sinh (đúng hợp đồng plan §7). Bằng chứng sinh là file của B.
- W5: không chạy lại câu chậm để tách mạng ↔ provider (tốn ≈ 0,009 USD cho 44 câu; W5 chỉ là theo dõi).
- Chỉ đọc 6 câu B nêu; không đọc toàn bộ 31 câu chạm.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Đợt sửa kho bước 9 đạt "không làm hỏng" (spec §6). B sửa câu W5 theo m-1. A trình User đóng đợt sửa kho, kèm hai giới hạn:
- judge Claude, chưa có mốc người;
- latency lượt "sau" không đại diện.

## 7. Kiểm phần sửa (12:13 28/10/2026)

m-1 **đóng**: report B83 nay ghi W5 "phía mạng / provider (không tách được)", "p95 lượt sau không đại diện", ms / token ×2,9 ở khúc cuối, và việc C chạy song song
11:50–11:56 (phần trên máy không tăng). Kết luận giữ **ready_for_user_confirmation**.
