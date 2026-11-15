# Sửa lịch bằng lời — đổi hạng chỗ ở (bậc 1) · C · 15:56 15/11/2026

Plan `docs/superpowers/plans/2026-11-15-sua-lich-hang-cho-o-plan.md` (A duyệt bản `8b10ccd50d37`; mục "Chỗ đổi" thêm sau). Nhánh `p9-sua-hang-o`: bản đầu `c48ccf8`, **bản chỉnh (bản xin merge) `32c129f`**. Trạng thái: **đạt mọi tiêu chí, chờ review cả nhánh**.

## Làm gì
- **Trước:** sau khi có lịch, gõ "đổi sang khách sạn 4–5 sao" ⇒ lần hiểu ý trả rỗng (5 / 5 câu đếm sáng 15/11) ⇒ trả lời như câu hỏi thường, lịch không đổi, không báo gì.
- **Sau:** hành động mới `doi_hang_o` (`llm/sua_lich_v2.py`). Model chỉ điền một trong 3 mức (`binh_dan` / `vua` / `cao`) hoặc để trống; **code** quyết:
  - đổi được ⇒ ghi mức vào tham số lịch, **không gọi bộ xếp** (điểm / ngày / buổi giữ nguyên), ô Nơi ở dựng lại bằng đúng hàm của biểu mẫu, dòng "Đã đổi hạng chỗ ở: X → Y."; mọi câu của lịch giữ nguyên ⇒ 0 lần gọi model viết lại.
  - không đổi ⇒ luôn có một dòng lý do do code viết: chưa nêu rõ hạng (hỏi lại 3 mức) · đang ở hạng đó · khu chỗ ở của lịch không có cơ sở hạng đó · lịch không có mục chỗ ở (1 ngày / cờ nơi ở tắt).
- Phần "nơi ở của một khung" gom về một hàm `lich_trinh_v2.o_dau_khung`, dùng chung cho lịch thật (`len_ke_hoach.gan_o_an`) và phép thử mức mới — không có đường tính thứ hai.
- Lời dặn hiểu ý (`SUA_LICH_LOI_DAN`): thêm 1 gạch hành động + 1 câu cách nói. Không cờ mới, không sửa giao diện (dùng khối "Đã đổi / Không đổi được" sẵn có), không đổi `tin_nhan_hieu`.
- Lệch nhỏ so với plan (trong phạm vi): dòng "chưa nêu rõ hạng" viết "hạng chỗ ở — bạn nói rõ 1 sao / đạt chuẩn, 2–3 sao hay 4–5 sao thì mình đổi." vì giao diện tự thêm "Không đổi được: " ở đầu.

## Kết quả (mọi dòng [Chạy]; lượt có phí qua `/api/chat/stream` trên server của nhánh, đếm bằng `scripts/dem_chat_metrics.py --sha`)
| Tiêu chí ghi trước | Ngưỡng | Bản đầu `c48ccf8` | **Bản chỉnh `32c129f`** |
|---|---|---|---|
| Luôn — test 3.840 khung × 3 mức (`test_luu_tru_lich.py`) | 0 lệch | đạt | đạt (9.216 lượt đổi · 2.304 lượt "lịch 1 ngày") |
| Q1 — 25 hằng lời dặn, băm so với `main` | chỉ lời dặn hiểu ý khác | đạt | đạt |
| H1 — 12 câu nêu rõ hạng × 2 lượt, đúng mức cả 2 | ≥ 10 / 12 | 11 / 12 | **12 / 12** |
| H1-sai — áp khác mức nhãn | 0 / 24 | 0 | **0** |
| H2 — 6 câu không nêu hạng × 2: có đổi mức | 0 / 12 | 0 | **0** |
| H2-nói — có dòng hỏi rõ hạng ở cả 2 lượt | ≥ 4 / 6 | 5 / 6 | **6 / 6** |
| H3 — 6 câu hỏi thông tin × 2: thành lượt sửa | 0 / 12 | 0 | **0** |
| H4 — 8 câu lạ do A viết sau khi chốt lời dặn, 1 lượt | ≥ 6 / 8 · sai mức 0 | 8 / 8 · 0 (bộ 1) | **8 / 8 · 0** (bộ 2, mới) |
| Q3 — 10 chuỗi đã thấy, pass^2 | ≥ 8 / 10 (mốc 14/11: 9 / 10) | 8 / 10 | **10 / 10** |
| Q5 — an toàn 32 × 2 trong cuộc có lịch | 0 / 64 | 0 | **0** |
| Q5b — 8 câu trộn sửa + khẩn cấp × 2 | 0 / 16 | 0 | **0** |

- **Tốc độ (theo dõi):** 32 lượt đổi hạng trên bản chỉnh, tới lúc khung lịch mới hiện: p50 1,83 s, chậm nhất 3,33 s (không viết lại câu).
- **Không chạy:** Golden 176 + an toàn ngoài cuộc có lịch (lần hiểu ý không được gọi ⇒ 0 câu chạm), đo độ trễ riêng, Playwright (không sửa giao diện), test rộng — chạy một lần trước merge nếu người review cần.
- Test 0 USD: `test_luu_tru_lich.py` + `test_sua_lich_v2.py` 25 đạt (20 s); `test_len_ke_hoach_v2.py`, `test_cong_dot_1.py`, `test_the_khach_san.py`, `test_rao_so_ngay.py` 134 đạt (49 s).

## Vòng chỉnh duy nhất (A quyết, tiêu chí A ghi trước khi chạy)
- **Vì sao:** Q3 bản đầu đạt ngưỡng nhưng một chuỗi (loại câu "ngày N chỉ đi một buổi") trượt 2 / 2 trên nhánh: model trả "đổi số ngày" ⇒ rào số ngày chặn ⇒ "Chưa làm". Cùng chuỗi trên server bản `main`: 4 / 4 đạt ⇒ hồi quy quan sát được, đi cùng lời dặn mới (cơ chế chưa chứng minh; cỡ mẫu 2 ↔ 4).
- **Tiêu chí A ghi trước:** mọi ngưỡng cũ giữ nguyên **và** chuỗi đó đạt 2 / 2; H4 chạy bộ mới; trượt ⇒ dừng hẳn, không chỉnh lần hai.
- **Đổi đúng một thứ:** phần chi tiết hạng chỗ ở (cách nói ⇒ mức, "không nêu hạng ⇒ để trống") dời từ danh sách hành động xuống khối "cách nói thường gặp"; gạch hành động còn một dòng ngắn như các hành động khác; bỏ câu "chỉ hỏi về khách sạn ⇒ không phải sửa" (đoạn cuối lời dặn đã nói). Lý do chọn: giữ danh sách hành động gần bản `main` nhất. Không sửa phần số ngày.
- **Kết quả:** chuỗi đó 2 / 2; chuỗi chập chờn đã ghi 14/11 (bước thẻ chọn) lần này cũng 2 / 2 ⇒ Q3 10 / 10; mọi ngưỡng khác đạt (cột phải).

## Quan sát cần người review / A biết
- **H4 bộ 2, câu thứ 7** (người dùng vừa nói có em bé đi cùng vừa xin hạng 3 sao): code áp **hai** hành động — đổi số trẻ em 0 ⇒ 1 (lịch xếp lại cho trẻ nhỏ) và đổi hạng. Mức hạng đúng nhãn nên H4 tính đạt; phần xếp lại là hành vi sẵn có của `doi_tham_so` khi câu nêu trẻ em, không do bậc này. Công cụ chấm in "điểm giữ nguyên: False" cho câu 7 và 8 vì nó so với lịch lúc mở cuộc — không phải đổi hạng làm đổi điểm (test "Luôn" khoá điều đó).
- Lý do "khu không có cơ sở hạng đó" **không xảy ra** ở lịch thật nào với bảng v5 (0 / 11.520); đường này chỉ được test bằng một bảng nhỏ tự đặt (bỏ hết cơ sở 4–5 sao).
- Câu báo "không có mục chỗ ở" ghi "(lịch 1 ngày)" cả khi nguyên nhân là cờ nơi ở tắt — bản đang chạy bật cờ nên chưa gặp.
- Chưa làm (đúng plan): tự suy "rẻ hơn / sang hơn", bỏ chọn hạng, gọi tên một khách sạn, nút hạng trên biểu mẫu không tự đồng bộ theo lời (các trường khác sửa bằng lời cũng vậy).

## Tiền (từ log, theo mã bản): ≈ 0,210 USD / trần 0,25
bản đầu 0,1017 (155 lượt) · bản chỉnh 0,0960 (155 lượt) · Q5 hai lần 0,0034 + 0,0036 · mốc `main` cho chuỗi hồi quy 0,0054.

## Bảng rà AI FDE (sau khi làm)
| Mục | Hiện trạng | Khớp / lệch |
|---|---|---|
| Model ↔ code | Model: câu ⇒ 1 enum. Code: mức hợp lệ (schema), có cơ sở không, chọn khách sạn, câu báo (`sua_lich_v2.ly_do_giu_hang`, `ap`) | khớp |
| Từ chối có lý do | 4 mã lý do, mỗi mã một câu cố định; H2-nói 6 / 6 | khớp |
| Làm sai mà báo đã làm | 0 / 24 + 0 / 16 (H4 hai bộ); chưa thấy lỗi ⇒ không xây rào "mức phải có trong chữ người dùng" | khớp |
| Chữ người dùng là dữ liệu | Q5 0 / 64, Q5b 0 / 16, H3 0 / 12 | khớp |
| Đường ra / dữ liệu mới | Không | khớp |

**Dữ liệu (private):** `data/sua_lich_hang_2026-11-15/` — bộ câu C ghi trước `cau_h.jsonl` (md5 `f048c0e67761`), hai bộ H4 của A, `tools/do_h.py`, `tools/cham_h.py`, kết quả `do/`.

**Giải thích ngắn:** người dùng nay nói được "đổi chỗ ở sang 4–5 sao" và ô Nơi ở đổi theo, lịch tham quan giữ nguyên; nói mơ hồ ("rẻ hơn") thì trợ lý hỏi lại rõ hạng thay vì im lặng hoặc đoán. Trợ lý chỉ hiểu ý, mọi phép chọn và câu báo do code làm.
