# Bậc 3 — mô tả công cụ bản 2 sau khoá `assistant.cong_cu_ban` — CÒN DỞ (dừng theo lời chủ dự án)

Viết: 15:53 21/11/2026 (giờ `date`), phiên B. Nhánh `p9-b-cong-cu-ban-2` (từ main `104b8d09`). Plan gốc: `report_agent/2026-11-21/b_bac_3_4_cong_cu_plan.md`.
Từ dùng: *mô tả công cụ* = đoạn chữ model đọc để quyết có gọi một công cụ không và gọi thế nào · *khoá* = một dòng trong `backend/config/settings.yaml` ·
*giống byte* = chuỗi gửi model không khác một ký tự · *lượt thật* = gọi model thật qua code sản phẩm · *phiên đo* = phiên chạy bộ thước trên cả hai model.

## Tới đâu

| Việc | Trạng thái |
|---|---|
| Khoá `assistant.cong_cu_ban: 1 \| 2` (đang đặt 1) | xong code |
| Bốn mô tả bản 2: tìm kho, thời tiết (bản có `loai`), ngày lịch, khoảng cách | xong chữ — CHƯA lượt thật nào |
| Test `backend/tests/test_cong_cu_ban.py` | 10 đạt; đã thấy đỏ khi cố ý bỏ lời gọi ở đường stream (2 hỏng) |
| Lượt thật nhỏ hai model (72 lượt, tiêu chí đã ghi trước) | CHƯA chạy — script và tiêu chí sẵn, xem dưới |
| Chạy các file test chạm đường bị đổi (khoảng cách, ngày lịch, thời tiết, vòng công cụ, cổng công cụ, lớp dịch Bedrock) | CHƯA chạy |
| Một phiên khác đọc nhánh | CHƯA |

## Đổi gì so với plan đã duyệt

- Plan nói "năm mô tả"; chỉ viết BỐN: công cụ lịch trình đang tắt cờ (`lich_trinh: false`), bản thời tiết không có `loai` chỉ chạy khi cờ `bao_lu_cong_cu` tắt —
  hai thứ đó không tới model nên không đo được. Khoá = 2 mà gặp hai công cụ này ⇒ giữ chữ bản 1.
- Ba chỗ đổi NGHĨA (ghi ở đầu khối bản 2 của `backend/llm/full_corpus_prompt.py`): `bao_lu` chỉ khi có từ nguy hiểm thời tiết · bỏ luật "không chép lại số dự báo"
  (thay bằng "được nêu số đúng như nguồn ghi, kèm mã [n]; bảng đầy đủ đã hiện dưới câu trả lời") · tìm kho: thấy tên khác thì tìm lại bằng tên chính.
- Thêm hai ý không có trong năm điểm đã duyệt, người đọc nhánh cần xét: mô tả tìm kho nói "mỗi câu hỏi tìm được tối đa N lần" (N lấy từ `so_lan_tim_kho`);
  mô tả khoảng cách nói "gặp nơi ngoài bảng thì nói rõ là chưa có số". Cố ý KHÔNG đưa câu nào về "cách trả lời khi thiếu bằng chứng" vào mô tả công cụ
  (bài học cùng ngày: dòng báo của cờ `bao_het_luot_tim` bỏ mất lối từ chối ⇒ Sonnet trả lời câu ngoài tỉnh).
- Cách cắm: MỘT hàm `mo_ta_theo_ban` trong `backend/llm/assistant.py`, gọi ở hai chỗ dựng công cụ của lượt (không stream, stream); bản 1 ⇒ hàm không chạm gì.
  Generator đổi đúng một dòng (dòng công cụ ngày lịch đọc thuộc tính `mo_ta`) ⇒ khi gộp với nhánh `p9-b-vong-cuoi-chi-viet` có một chỗ ghép một dòng.

## Đã kiểm

| Khẳng định | Nhãn | Lệnh / nơi xem |
|---|---|---|
| Khoá = 1 ⇒ danh sách công cụ (tên, mô tả, khuôn tham số) lấy từ cấu hình thật giống từng byte bản trước khi sửa | [máy kiểm] | `cmp` hai file chụp bằng `data/thu_bedrock_2026-11-21/tools/b_chup_cong_cu.py` (riêng tư): `ket_qua/b_cong_cu_ban/moc_104b8d09.json` ↔ `ban1_sau_sua.json` |
| Khoá = 2 ⇒ bốn mô tả mới; khuôn tham số chỉ khác dòng tả `cau_tim`; phần còn lại của yêu cầu gửi model không đổi; lượt đầu và lượt có lịch sử; cả hai đường | [máy kiểm, model dựng sẵn] | `cd backend && uv run python -m pytest tests/test_cong_cu_ban.py -q` ⇒ `10 passed` |
| Model chọn công cụ / tham số tốt hơn với bản 2 | [chưa kiểm] | cần lượt thật |

## Làm tiếp thế nào

1. Lượt thật nhỏ: tiêu chí ghi trước ở `data/thu_bedrock_2026-11-21/ket_qua/b_cong_cu_ban/TIEU_CHI.md`; script `data/thu_bedrock_2026-11-21/tools/b_do_cong_cu_ban.py`
   (chạy `<backend của nhánh> <thư mục ra> luna` rồi `s_high`; hai bản xen kẽ trong một tiến trình).
2. Chạy từng file test chạm đường bị đổi; đạt và sàn của lượt thật giữ ⇒ đẩy, xin một phiên đọc, rồi giao phiên đo chạy thước 2 × 2.
3. Chưa đo trên đường thật: mọi thứ về hành vi model. Lệnh chấm retrieval `lan_tim_dau: v2` của bộ đo (`evaluation/full_corpus_eval.py`, dựng `tim_kho` riêng) không đi qua khoá này.
