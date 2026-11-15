# Dọn nợ nhỏ vùng sửa lịch bằng lời + đếm "biểu mẫu đưa cơ sở khác hạng" — implementation (C, 19:35 15/11/2026)

Giao: A, tối 15/11 (handoff mục 4 và 4b(c)). Tiền: **0 USD** cho hai việc (không lượt model). Nhánh `p9-sua-lich-no-nho`.

## Việc 2 — đếm trước (làm trước, chỉ trong `data/`, không sửa code hệ thống)

- **Câu hỏi:** lịch từ BIỂU MẪU có lặng lẽ đưa cơ sở khác mức hạng người dùng chọn không (khi khu không có cơ sở mức đó, `luu_tru_lich.chon_co_so` tự lùi về trải mọi hạng, không kèm lý do).
- **Tiêu chí ghi trước khi chạy** (`data/dem_lech_hang_bieu_mau_2026-11-15/tieu_chi.md`): 0 ô lệch ⇒ không sửa; có ô (khu × mức) lệch 100 % và tổng ≥ 1 % ⇒ đề xuất thêm một dòng lý do; ở giữa ⇒ ghi giới hạn.
- **Ca đối chứng (W83) [đã chạy]:** bảng giả một khu chỉ có cơ sở 5 sao — hỏi mức bình dân ⇒ phép thử ra "lệch"; hỏi mức cao ⇒ "không lệch". Cả hai đúng.
- **Kết quả [đã chạy, 1,9 s]:** 3.840 khung × 3 mức; 9.216 ô có khối (lịch ≥ 2 ngày), 2.304 ô lịch 1 ngày không có khối. **Ô lệch: 0 / 9.216**; ô bị đưa về trung tâm kèm lý do khu: 0.

| Khu mà ô nhắm tới | Ô mỗi mức | Lệch |
|---|---|---|
| Trung tâm | 3.036 × 3 mức | 0 |
| Ven biển phía bắc | 36 × 3 mức | 0 |
| Phía tây | 0 | — |
| Ven biển phía nam | 0 | — |

- **Vì sao 0 [code + bảng]:** ô duy nhất của bảng lưu trú v6 trống là "ven biển phía nam × mức vừa" (phía nam có 3 cơ sở mức cao, 2 mức bình dân, 0 mức vừa); nhưng với bảng điểm 41 điểm không khung nào của biểu mẫu chọn khu ven biển phía nam (cụm nam xa là "đi trong ngày", không tính cho khu nào), cũng không khung nào chọn phía tây.
- **Đọc theo tiêu chí:** không sửa. Đường lùi lặng lẽ vẫn còn trong code — nó chỉ lộ nếu bảng điểm hoặc bảng lưu trú đổi ⇒ chạy lại công cụ này (2 giây) khi đổi một trong hai bảng. Tỉ lệ trên tổ hợp mô phỏng không phải tần suất người dùng thật.
- Công cụ: `data/dem_lech_hang_bieu_mau_2026-11-15/tools/dem_lech_hang.py`; kết quả `ket_qua.json` cùng thư mục. **A quyết** (C không tự sửa).

## Việc 1 — hai chỗ nợ + bảng trường

| Chỗ | Trước | Sau | Ở đâu |
|---|---|---|---|
| (a) Hành động đổi số ngày / kiểu lịch không đổi được gì | lượt sửa không có dòng nào | một dòng "Không đổi được": không trường nào ⇒ "Mình chưa rõ bạn muốn đổi kiểu lịch thành gì — bạn nói cụ thể hơn nhé."; mọi trường trùng giá trị đang dùng ⇒ "Lịch đang đúng như vậy rồi (kiểu đi: nhẹ nhàng)." | `sua_lich_v2.ap` nhánh `doi_so_ngay / doi_tham_so`; 2 khoá mới của `CAU_KHONG_DOI` |
| (b) Đổi kiểu đi / sở thích / trẻ em / người lớn tuổi | chỉ "Đã đổi số trẻ em: 0 → 1" | thêm một dòng: "Lịch xếp lại theo lựa chọn mới: k điểm đổi ngày hoặc buổi; bớt …; thêm …" hoặc "Các điểm trong lịch giữ nguyên chỗ." | `_so_cho` (tách từ phần đổi ngày đi, dùng chung), `kq["xep_lai"]`, `thay_doi` |
| (c) Bảng "trường nào sửa được bằng lời" | — | mục "Bảng hiện hành" đầu `c_dem_sua_lich_truong.md` (7 / 8 trường) | report |

- **Không đổi:** lời dặn / chuỗi gửi model (không chạm `generator`, `SUA_LICH_LOI_DAN`) ⇒ không lượt có phí. Không chạm hàm đọc chữ người dùng ⇒ không cần bộ dò W82. `sua_ap` (dữ liệu bộ đo so nhãn) không thêm khoá. Đổi số ngày không thêm dòng xếp lại.
- **Tự quyết trong phạm vi:** hành động trùng giá trị đang dùng cũng báo (cùng nhánh `if not doi`), dùng cùng giọng với "Lịch đang gợi ý chỗ ở hạng … rồi"; nhãn trường gom thành hằng `NHAN_TRUONG`.
- **Giới hạn thấy khi dò [đã chạy, 54 ca: 2–3 ngày × 3 kiểu × 3 sở thích × 3 kiểu đổi]:** dòng xếp lại có thể dài (nhiều nhất 9 tên "bớt" + 3 tên "thêm") vì thêm một trẻ em làm bộ xếp bỏ buổi tối và đổi nhiều điểm; C giữ đủ tên (cùng khuôn với đổi ngày đi) — reviewer thấy nên cắt thì nêu.

## Kiểm [đã chạy]

| Bước | Kết quả | Thời gian |
|---|---|---|
| `test_sua_lich_v2.py` + `test_luu_tru_lich.py` + `test_rao_so_ngay.py` (2 test mới) | 49 passed | 21 s |
| `test_sua_ngay_di.py` (phần đổi ngày đi dùng `_so_cho` mới) | 68 passed | 14 s |
| Mô phỏng nhãn bộ chuỗi đã thấy (0 USD), main ↔ nhánh | 10 / 10 ↔ 10 / 10 | < 10 s mỗi bên |
| Test rộng `backend/tests` | xem STATUS_C (chạy sau khi A cho lượt) | — |
| Playwright | không chạy — không sửa giao diện (dòng mới đi qua khối "Đã đổi / Không đổi được" sẵn có) | — |

Bộ kín: không mở, không chạy.
