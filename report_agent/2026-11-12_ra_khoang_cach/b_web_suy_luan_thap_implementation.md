# Mức suy luận "low" cho lần viết mục web — kết quả đo (B, 16:22 14/11/2026)

- **Plan:** `docs/superpowers/plans/2026-11-14-web-suy-luan-thap-plan.md` (A duyệt sha `85922c863947`, mức nhẹ).
- **Nhánh:** `p9-web-suy-luan` (worktree `/tmp/b_lkh`, **chưa commit**). Cờ `web_suy_luan_thap` TẮT.
- **Dữ liệu, công cụ:** `data/web_suy_luan_2026-11-14/` (`tools/do_web.py`, `buoc1.jsonl`, `buoc2.jsonl`, log).

## Kết luận: **KHÔNG ĐẠT** (trượt tiêu chí T) ⇒ cờ giữ tắt, không vòng chỉnh, đề xuất không merge
- Thời gian viết mục web p50 giảm **0,87 s** (2,95 ⇒ 2,08 s), sàn ghi trước là giảm ≥ 1,5 s.
- Các tiêu chí chất lượng đều đạt.
- D (đọc tay 8 cặp) và A (câu an toàn) **NOT RUN**: đã trượt T, mà plan ghi "đạt cả 5 mới đề xuất bật".

## Đổi gì (code trên nhánh)
- `llm/generator_openai_full_corpus.py`: `web_agent_thap` (clone `web_agent`, `reasoning.effort = "low"`); `generate_web_section(..., thap)`.
- `llm/assistant.py`: cờ `web_suy_luan_thap`; `cong_web(..., thap)`; 2 chỗ gọi truyền cờ.
- `config/settings.yaml`: `web_suy_luan_thap: false`.
- `tests/test_web_suy_luan.py` (mới): yêu cầu gửi model chỉ khác ở `reasoning`; cờ mặc định tắt.
- **Test:** `test_web_suy_luan.py` 2 đạt, cả không khoá lẫn có khoá (8 s); các file chạm (`test_b6_tra_web`, `test_cau_nhieu_y`, `test_cong_dot_1`) 143 đạt cả hai cách (~50 s mỗi lần).

## Đo [Chạy]
- **Bước 1** (31 câu chạm, lượt thật, dừng ngay trước lần viết mục web):
  - 0 lỗi;
  - 19 câu có tin nhắn viết mục web: hỏi kèm 9 / 10, Golden ngoài kho 7 / 18, an toàn 3 / 3. 11 câu Golden còn lại bị định tuyến xếp ngoài phạm vi nên không mở web;
  - tiền model 0,016 USD + Serper ~0,02.
- **Bước 2** (19 đầu vào × 2 lần × 2 bản, xen kẽ thứ tự, cùng tin nhắn): 76 lần gọi, 0 lỗi gọi; tiền 0,010 USD. Máy rảnh (E xác nhận không chạy lượt đo).

| Mã | Mặc định | Low | Sàn | |
|---|---|---|---|---|
| K — ra mục web (`co_muc`) | 21 / 38 | 22 / 38; 0 đầu vào kém hơn, 1 đầu vào tốt hơn | không thấp hơn quá 1 đầu vào | ĐẠT |
| S — chuỗi số không có trong đoạn trích lọt qua | 0 | 0 | 0 | ĐẠT |
| T — ms lần viết mục web p50 / p95 | 2.947 / 4.678 | 2.077 / 2.819 | giảm ≥ 1,5 s | **TRƯỢT** (−0,87 s) |
| D — đọc tay 8 cặp | — | — | 0 cặp nói chắc hơn nguồn | NOT RUN |
| A — câu an toàn có tra web | — | — | 0 | NOT RUN |

- Token suy luận p50: 94,5 ⇒ 0. Tiền lần viết: 0,0060 ⇒ 0,0041 USD / 38 lần (−32 %).
- **Vì sao ngưỡng 1,5 s không tới:** lượt đo đếm từ log cho p50 4,94 s mỗi lần viết, nhưng lần đo này mặc định chỉ 2,95 s. Có thể vì lúc đếm từ log có nhiều lượt đo chạy song song; nguyên nhân chưa chứng minh. Ngưỡng ghi trước từ số log nên quá cao so với mức hôm nay. B không đổi ngưỡng sau khi đo.

## Quan sát lớn hơn (ngoài phạm vi, báo A)
- **Gần một nửa mục web bị kiểm cuối bằng code chặn**, ở cả hai bản: mặc định 17 / 38, low 16 / 38 thành `khong_tin_cay`.
  - Lý do chính: `so_ngoai_trich` (9 · 7) và `tien_ngoai_trich` (6 · 5), nghĩa là model viết số hoặc tiền không có trong đoạn trích.
  - Khách thấy câu cố định "chưa tra được tin đáng tin" thay cho mục web.
- Đây là chỗ mất giá trị lớn hơn 0,9 s. Hướng đáng xem (chưa làm, cần mục việc riêng): đếm từ `buoc2.jsonl` những số bị chặn là số model bịa, hay là số có trong đoạn trích nhưng viết khác dạng (vd "7h" ↔ "7:00", "200k" ↔ "200.000"). Nếu phần lớn là khác dạng ⇒ sửa phép so trong code; nếu là bịa ⇒ luật chặn đang đúng.

### Đếm nhanh số bị chặn (0 USD, cả hai bản gộp, trên `buoc2.jsonl`)
- **Tiền:** 37 / 37 số tiền bị chặn có dãy chữ số xuất hiện trong đoạn trích ⇒ **nhiều khả năng chỉ khác cách viết**, không phải bịa.
- **Chuỗi số khác** (giờ, số nhà, năm…): 17 không có trong đoạn trích, 6 có nhưng khác dạng ⇒ phần lớn là số model tự thêm, luật chặn đúng.
- **Giới hạn của phép dò:** so dãy chữ số như chuỗi con, nên lỏng (vd "50" nằm trong "150"). Đây là **dấu hiệu, chưa phải kết luận**. Muốn chắc phải đọc tay ~10 ca tiền.
- **Đề xuất cho A** (việc riêng, 0 USD đo lại trên chính `buoc2.jsonl`): xem phép so tiền \`tien_ngoai_trich\` có chặn nhầm vì khác dạng không. Nếu đúng ⇒ chuẩn hoá cách viết tiền trước khi so (giữ luật "tiền ⊂ đoạn trích"). Lợi ước: một phần trong ~40 % mục web đang bị thay bằng câu cố định sẽ hiện được.
