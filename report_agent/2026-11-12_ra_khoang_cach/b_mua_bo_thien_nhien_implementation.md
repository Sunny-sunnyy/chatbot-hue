# Ngày mưa bỏ luật "chiều một điểm thiên nhiên" khi không chọn sở thích (B, 13:48 17/11/2026)

Việc: User chọn (c) "ngày mưa nặng lịch vẫn toàn ngoài trời" — sửa một luật trước 22/11 (A giao 17/11 chiều, sau bàn nhóm B / C / E). Nhánh `p9-mua-bo-thien-nhien` từ `origin/main` `c1e8180`. 0 USD (hàm thuần, không server, không model). Dữ liệu đo (private): `data/mua_bo_thien_nhien_2026-11-17/`; bộ dò do E soạn: `data/mua_lich_2026-11-17/bo_do/`.

## Lỗi
Không chọn sở thích ⇒ luật cũ "chiều mỗi ngày một điểm thiên nhiên" chọn điểm chiều **trước** bước "ngày mưa xét điểm trong nhà trước". Cả 10 điểm thiên nhiên của bảng đều ngoài trời ⇒ ngày dự báo mưa to lịch vẫn ra đầm / phá / biển (ca tự thử 16/11: mưa 100 % / 37 mm, Đầm Chuồn chiều ngày 1).

## Đã làm
`backend/llm/lich_trinh_v2.py`: hàm nhỏ `la_ngay_mua(ngay_i)` (cùng điều kiện cũ: ngày có trong `mua` — đã lọc ≥ 6 mm ở `len_ke_hoach.ngay_mua_xep` — và ≥ `NGUONG_MUA`), dùng ở hai chỗ: điều kiện luật chiều-thiên-nhiên (thêm "không phải ngày mưa") và chỗ sắp lại thứ tự xét ngày mưa (thay biểu thức cũ, cùng nghĩa). Không đổi ngưỡng, bảng, lời dặn, chuỗi gửi model ngoài phần lịch của ngày mưa.

## Tiêu chí ghi trước (A) ⇒ kết quả [Chạy]
| Tiêu chí | Kết quả |
|---|---|
| Ngày không mưa giống hệt mọi khung (tập 3.840 của test `mo_phong_ngay`) | 2.880 / 2.880 khung không có dự báo mưa giống hệt; 3.600 / 3.600 khung có sở thích (cả ngày mưa) giống hệt; chỉ 100 / 3.880 khung đổi, **cả 100 đều là "mưa + không sở thích"** |
| `kiem_khung_v2` lỗi 0 | 0 (main 0) trên 3.880 khung |
| Đường không sở thích, ngày mưa ra cụm biển–đầm phá 45 ⇒ 0 | 300 ngày mưa không sở thích: ra cụm biển–đầm phá **109 ⇒ 0**; chiều có điểm thiên nhiên 207 ⇒ 0; ngày toàn ngoài trời 253 ⇒ 181; ngày rỗng 0 ⇒ 0 (số 45 lúc bàn nhóm là tập nhỏ 120 ngày) |
| Test mưa của `test_len_ke_hoach_v2` + 1 test mới | cả file 92 / 92 đạt (46 s); test mới `test_rain_day_drops_afternoon_nature_rule_when_no_interest` **trượt trên code cũ** (Đầm Chuồn chiều ngày mưa) — ca đối chứng đã thấy "có" |
| Mô phỏng nhãn bộ sửa lịch không model | `chuoi_da_thay.jsonl` 10 / 10 khớp, đầu ra nhánh giống byte main (bộ không có ngày đi ⇒ không dự báo ⇒ không chạm đường đổi). Bộ kín không mở; cùng lý do (lượt 1 không ngày đi) ⇒ suy luận không chạm, chưa chạy |
| Bộ dò ~16 khung mưa do E soạn: 0 sai | **0 / 16 SAI** (main 10 / 16) |
| Test rộng | KHÔNG chạy — A: nhánh chỉ đổi một hàm thuần + test của nó (Session_Prompt §8, 15/11) ⇒ test file chạm là đủ |

Ví dụ lịch 1 ngày không sở thích, ngày mưa: Đại Nội → Đầm Chuồn ⇒ Đại Nội → chùa Thiên Mụ → điện Hòn Chén (lịch khô không đổi).

## Giới hạn giữ (User đã nhận)
- Có chọn sở thích ⇒ điểm ưu tiên giữ chỗ dù mưa (luật User duyệt) ⇒ vẫn có thể ra phá / đầm / Bạch Mã ngày mưa; dòng "Nếu mưa…" giữ vai chính.
- Kho ghi phần lớn lăng / chùa / Đại Nội là ngoài trời; chỉ 12 / 41 điểm trong nhà hoặc cả hai ⇒ 181 / 300 ngày mưa không sở thích vẫn toàn ngoài trời — giới hạn dữ liệu, không sửa bằng code.

## Thời gian từng bước (đo)
pytest file chạm 46 s (~2 GB RSS) · xuất + so 3.880 khung ~1 phút / bản · bộ dò E < 10 s · mô phỏng sửa lịch < 30 s / bản.
