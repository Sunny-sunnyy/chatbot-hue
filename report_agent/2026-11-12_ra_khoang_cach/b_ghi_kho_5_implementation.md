# Ghi kho lần 5 14/11 — 10 bài món / đặc sản (B) + 13 bài địa điểm / di tích (E) · B · 19:39 14/11/2026

A giao (User: dữ liệu món ăn, địa điểm phải đầy đủ; tự tra / ghi kho được). Tiêu chí ghi trước: `data/sua_kho_2026-11-14_ghi_kho_5/TIEU_CHI.md`. Review: C (10 bài món ready sau 1 major + 3 minor; 13 bài E ready sau 1 major — biên bản private ở `data/mon_an_2026-11-14/`, `data/bai_kho_5_dia_danh/`). B ghi + dựng + đo.

## Vì sao những bài này (đếm trước khi xây)
- **Món (B, ≈ 0,014 USD):** 46 tên món / đặc sản / quà đếm bằng `scripts/grep_kb.sh` (kho có 9 bài món riêng); hỏi thử 21 món chưa có bài riêng ⇒ 11 trả lời đủ nhờ bài quán (không viết), **10 bị từ chối / mỏng** ⇒ viết 10 bài: tré, vả trộn, tôm chua, mít trộn, bánh in, rượu Minh Mạng, cháo hến, cơm sen, nem công chả phượng, bánh su sê. Nguồn: Codex 2 lô + B mở 10 trang chính đối chiếu. `data/mon_an_2026-11-14/BUOC_1_DEM.md`.
- **Địa điểm (E):** 42 câu hỏi thử ⇒ 8 nơi bị từ chối + 5 mỏng (+ chợ Kim Long bị loại) ⇒ 13 bài. `data/bai_kho_5_dia_danh/BAN_GIAO.md`.

## Đổi gì
- 23 bài mới, 0 sửa bài cũ: 10 `foods/local_specialties/`, 8 `heritages/heritage/`, 5 `travel/places/`.
- Chỉ mục: 224 ⇒ **247 file**, 8.644 ⇒ **9.032 đoạn** (+388; 23 / 23 bài có đoạn); record `106fe0842b8e`, sparse `1fb1d7ad895d`, T1 `7e07b898050a`. Sao lưu: `knowledge-base-hue/meta/backup_ghi_kho_2026-11-14_lan_5/` (rỗng vì không sửa bài cũ; lùi = xoá 23 file + dựng lại). Dựng 19:30 – 19:34, cả nhóm dừng việc nặng.

## Đo (luật đo câu chạm) — ĐẠT
| Bộ | Kết quả |
|---|---|
| T1 (0 USD) | 35 / 158 câu đổi top 10 (phần lớn do trọng số từ khoá đổi khi kho thêm 388 đoạn); **3 câu chạm** (top 10 có đoạn bài mới) |
| Golden: 3 câu chạm + 18 ngoài kho ×1 | 0 lỗi kỹ thuật, 0 lỗi trích dẫn; **ngoài kho bị trả lời 0 / 18**; từ chối nhầm 0 / 3. Đọc tay 3 cặp (mốc: lượt sau ghi kho 4 hoặc lượt đủ 176 câu sau ghi kho 2 cho câu chưa đo lại từ đó): 2 giống hệt, 1 thêm hai chữ cùng nghĩa ⇒ không tụt |
| An toàn 32 ×1 | 0 lỗi, 0 lỗi định tuyến, 0 ngoài kho bị trả lời, 0 lỗi trích dẫn; **0 câu đổi lớp so với lần 4**. 3 câu có tên một nơi mới trong ngữ cảnh — đọc tay: tên đó đến từ bài cũ (không phải đoạn bài mới), câu trả lời cùng ý lần 4 |
| 23 câu hỏi thử (không phải Golden; địa điểm tắt tra web như lượt "trước" của E) | Trước: món 4 / 10 từ chối + 6 mỏng; địa điểm 8 / 13 từ chối + 5 mỏng. Sau: **0 / 23 từ chối, 23 / 23 trích đúng bài mới** |

## Tiền (từ log)
≈ **0,039 USD**: Golden 21 câu 0,0055 · an toàn 32 0,0218 · 23 câu thử 0,0121. Trước đó: hỏi thử món bước 1 ≈ 0,014 (B), phần E ở BAN_GIAO. Codex: gói ChatGPT; agent con: quota Claude.

## Còn lại
- Ảnh cho 23 bài mới (Khám phá): E / C theo cách v3.
- Sổ ghi việc khâu kho + `bai_hoc/22`: theo A giao.
