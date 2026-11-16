# Ghi kho Lập An — 2 bài quán (B) — implementation report

Cập nhật: 18:19 16/11/2026 (B, terminal `hue-rag-b2`). Việc: `CURRENT_HANDOFF.md` "PHIÊN TỐI 16/11" mục 2; A giao làm ngay. Tiêu chí ghi trước: `data/sua_kho_2026-11-16_lap_an/TIEU_CHI.md` (14:59 16/11/2026).

## Kết quả: ĐẠT mọi sàn ghi trước

| Mục | Trước | Sau |
|---|---|---|
| Kho | 263 bài / 9.425 đoạn | **265 bài / 9.436 đoạn** (+2 bài `foods/restaurants/`, +11 đoạn) |
| Build record · sparse state | `1b53af26b662` · `ccd1d3ae36ec` | **`3622a573e28e` · `ea442226257d`** |
| Mốc tìm T1 (158 câu) | `data/sua_kho_2026-11-15_tay_son/t1_sau.jsonl` | **`5d344d6d1bbf`** (`data/sua_kho_2026-11-16_lap_an/t1_sau.jsonl`) |

- **Câu chạm (đếm bằng code, 0 USD):** Golden đổi top 10: **2 / 158**; an toàn đổi top 10: **2 / 32**; đoạn bài mới lọt top 10 Golden: 0.
- **Lượt có phí ×1** (20 câu Golden = 2 chạm + 18 ngoài kho; 2 câu an toàn chạm; 2 câu thử):
  - lỗi kỹ thuật 0 / 20; lỗi trích dẫn 0; **ngoài kho bị trả lời 0 / 18** (18 / 18 từ chối, cùng câu từ chối như mốc 15/11);
  - 2 câu Golden chạm (loại câu hỏi một dữ kiện): cả hai trả lời **cùng ý** với mốc (B đọc tay; khác ở một dấu cách); từ chối nhầm 0;
  - 2 câu an toàn chạm: 0 lỗi, **0 đổi lớp** (đều `tra_loi` như lượt 15/11 `data/tuan_sau_2026-11-15/an_toan_r1.jsonl`; cảnh báo giữ nguyên ý; một câu có ngày tương đối nên ngày đổi theo hôm nay — đúng lịch);
  - **2 câu thử** (hỏi quán hải sản ở khu vực của 2 bài mới; tắt tra web): trước ghi kho từ chối 2 / 2 ⇒ sau ghi kho trả lời 2 / 2, nêu quán mới, trích nguồn bài mới; không nêu giờ / giá; món nêu ra đều có trong bài (B đối chiếu tay).
- **Tiền thật (cộng `usd` từ file kết quả):** thử trước 0,0016 · Golden 0,0071 · an toàn 0,0010 · thử sau 0,0008 ⇒ **≈ 0,0104 USD** (trần 0,05).
- **Thời gian:** chạy khô + thử trước ~3 phút; ghi + dựng + T1 + câu chạm 18:10:20 ⇒ 18:15:54 (5 phút 34 giây; dựng 18:11:01 ⇒ ~18:14); lượt có phí 18:16:07 ⇒ 18:17:36 (89 giây).

## Đã làm
1. Chạy khô bước 0 đạt; `overlap_scan` 2 nháp: 0 trùng.
2. **E kiểm 2 bài trước khi dựng** (A yêu cầu): khuôn + nội dung ổn; 1 chỗ nên sửa — nháp ghi đơn vị hành chính theo tên cũ của nguồn, kho thì gọi theo đơn vị mới ⇒ B sửa 2 dòng mỗi bài (Tóm tắt + Địa chỉ: theo cách kho gọi, kèm ghi chú "nguồn ghi theo tên cũ"); E nhìn lại diff: ổn; A chốt giữ bản này. Bản trước sửa: `data/sua_kho_2026-11-16_lap_an/nhap_truoc_E/`. md5 hai bài đã ghi: `a0506b9575ad` · `23744675b84d` (file trong kho khớp nháp).
3. `tools/chay.sh` (sao lưu record / sparse ⇒ ghi 2 bài ⇒ chia đoạn thử ⇒ xoá ba đích ⇒ dựng ⇒ T1 + top 10 an toàn ⇒ câu chạm) rồi `tools/do_sau.sh`. Đo trên HEAD `6b90bbf`; trong lúc đó A đẩy `a575119` — `git diff 6b90bbf a575119 -- backend` chỉ có 1 dòng cờ bản đồ + 2 file test.
4. Bảng quán của lịch **không dựng lại** (hai quán cách điểm lịch gần nhất > 2 km) ⇒ lịch không đổi.

## Chỗ lệch / giới hạn (ghi trung thực)
- **`overlap_scan` sau khi sửa theo E không ra 0:** mỗi bài 1 dòng (dòng Địa chỉ) nhãn `corpus` = trùng với chính kho; 0 trùng Golden / câu kín (luật chỉ cấm hai loại này; A đồng ý đi tiếp). B tìm tay: cụm tên đơn vị hành chính mới có nguyên văn ở 7 bài kho khác (38 ký tự nguyên văn; bộ quét báo ngưỡng 40 — [suy luận] do chuẩn hoá chữ trước khi so, chưa đọc code bộ quét).
- **Lỗi quy trình của B:** gửi lệnh dựng cùng lượt với lệnh quét lại ⇒ bản dựng bắt đầu trước khi B đọc kết quả quét. Không gây hại lần này; lần sau quét xong, đọc, rồi mới dựng.
- Chưa kiểm: 2 URL nguồn của bài không mở lại hôm nay (dựa biên bản người đọc độc lập `doc_nhap.md` chiều 16/11). Tên đường trong một bài là tên cụt theo nguồn (chưa xác minh — đã nêu ở biên bản).
- Lùi nếu cần: `python3 -I data/sua_kho_2026-11-16_lap_an/tools/ghi_kho.py lui` + dựng lại (record / sparse cũ ở `data/sua_kho_2026-11-16_lap_an/backup/`).

## Còn lại cho A
Sổ khâu kho + `bao_cao_he_thong/README.md` + 1 dòng nhật ký + số "263 / 9.425" trong `Project_Status.md` §1, §4 (⇒ 265 / 9.436) và `bai_hoc/` nếu có nêu số kho; `data/HUONG_DAN_TEST_USER.md` nếu muốn User thử 2 câu quán mới.
