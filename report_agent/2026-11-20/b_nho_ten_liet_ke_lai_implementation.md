# Việc 2 — cờ `nho_ten_goi_y`: câu hỏi tiếp xin liệt kê lại không nhận dòng ghi chú (B, 08:33 20/11/2026, giờ `date`)

Trạng thái (cập nhật 08:42 20/11/2026): **đã sửa theo review của E (1 major); CHỜ E chạy lại hai bộ dò và phép đo qua hệ thống thật của C.** Chưa gộp. Plan mức nhẹ (riêng tư, phiên điều phối
duyệt bản `d26eb6099da3`): `data/kich_ban_pho_thong_2026-11-19/viec_2_sua_nho/PLAN.md`. Nhánh `p9-b-nho-ten-liet-ke-lai`.

## 1. Người dùng thấy gì khác
Trợ lý nhớ tên các nơi vừa trích bằng một dòng ghi chú do code viết (cờ bật 19/11). Dòng đó chỉ là một phần các nơi đã nêu. Khi người dùng hỏi tiếp kiểu
"kể hết các chỗ vừa nêu", model có lúc coi dòng ghi chú là danh sách đủ và chỉ kể mấy tên đó (đo 19/11: một lượt kể 3 / 8 nơi). Bản sửa: lượt mà CÂU GÕ chỉ
xin liệt kê lại thì code không đưa dòng ghi chú cho model ở đúng lượt đó (lịch sử lượt đó giống như khi cờ tắt); ghi chú vẫn được lưu, lượt sau nhận lại.
Câu hỏi về một nơi ("địa chỉ quán đó") không đổi gì. [chưa kiểm trên model thật — chờ phép đo của C]

## 2. Sửa gì
| File | Đổi |
|---|---|
| `backend/llm/ten_goi_y.py` | hai hàm thuần: `la_cau_xin_liet_ke_lai(cau)` và `lich_su_cho_luot(lich_su, cau)`; hằng `TIEN_TO_GHI_CHU` (chữ dòng ghi chú giữ nguyên từng byte) |
| `backend/api/routes/chat.py` | `_start_conversation` nhận thêm câu gõ, lấy lịch sử qua `lich_su_cho_luot`; số `history_tokens` của log đếm lịch sử THẬT gửi đi |
| `backend/api/conversations.py` | thêm `tokens_of(turns)` (tách từ `history_tokens`, hành vi cũ không đổi) |
| `backend/evaluation/full_corpus_eval.py` | bộ đo chuỗi (`run_chains`) lấy lịch sử qua cùng hàm, như route |
| `backend/tests/test_nho_ten_goi_y.py` | 3 test mới + mở rộng test bộ đo chuỗi lên 4 lượt |

**Luật nhận câu — hẹp có chủ ý** (bắt nhầm ⇒ mất ghi chú ⇒ quay lại lỗi nói chắc sai nơi, nặng hơn bỏ sót): câu được nhận khi có một cụm xin danh sách đủ
("kể hết", "liệt kê", "tất cả", "danh sách"…) VÀ cả câu đúng MỘT khuôn: [lời lịch sự] [lời xin kể] [tất cả / toàn bộ] các / những / mấy / mọi + ĐÚNG MỘT loại nơi
[cụm trỏ lại: "đó", "vừa nêu", "trong bài đó", "ở trên"…] [lời lịch sự]. Mọi dạng khác rơi ra: câu ghép, câu hỏi thêm điều gì, câu không nêu loại nơi ("kể hết đi").
Không cần đọc cờ: cờ tắt thì lịch sử không có dòng ghi chú ⇒ hàm trả đúng nội dung cũ.

**Bản đầu của luật đã bị review bắt** (E, 20/11): bản đầu xét "mọi từ còn lại thuộc bộ từ cho phép" — túi từ không thấy cấu trúc câu, nên bộ dò thêm của E ra
11 / 12 câu hỏi về MỘT nơi bị nhận (ba họ: trỏ một nơi bằng "vừa nói / vừa gợi ý" · "các / mấy" đi với danh từ khác đứng trước "nơi đó" · "trong đó / ở trên" trỏ một
nơi). Phiên điều phối cho đúng một lần sửa ⇒ thay bằng khuôn câu ở trên; thêm tiêu chí: câu hỏi có / không về CẢ NHÓM nơi vừa nêu cũng không được nhận.

## 3. Bằng chứng (tất cả 0 USD; chưa có lượt nào qua model thật)
| Phép | Kết quả | Nhãn |
|---|---|---|
| Test file chạm `tests/test_nho_ten_goi_y.py` (đồ giả chỉ để dựng điều kiện) | 18 đạt, ~10 giây | [máy kiểm] |
| Test mới thấy ĐỎ: hàm luôn trả sai ⇒ 4 hỏng · luôn trả đúng ⇒ 4 hỏng · lượt liệt kê ghi đè kho lịch sử ⇒ test loại lượt hỏng · bỏ luật (c) ⇒ 1 hỏng | đỏ cả bốn kiểu phá | [máy kiểm] |
| Bộ dò 54 câu do E soạn mù, chạy thẳng hàm — **lần đầu, nguyên trạng** (mã `8f43e3b`, bộ từ chốt trước khi mở file) | câu hỏi về một nơi bị bắt nhầm **0 / 20** (sàn 0) · câu ngoài phạm vi bị bắt 0 / 10 · câu xin liệt kê nhận đúng **5 / 20** | [máy kiểm] |
| Bộ dò đầu, sau lần sửa bộ từ để tăng số câu nhận (mã `bf2490b`) | bắt nhầm 0 / 20 · 0 / 10 · nhận đúng 14 / 20 | [máy kiểm] [E chạy lại: khớp] |
| **Bộ dò THÊM 20 câu của E (soạn sau khi đọc code), trên `bf2490b`** | câu hỏi về MỘT nơi bị nhận **11 / 12** (sàn 0) ⇒ TRƯỢT · câu hỏi về cả nhóm bị nhận 3 / 3 · đối chứng phải nhận 5 / 5 | [người thứ hai kiểm] |
| Cả HAI bộ dò, sau lần sửa bằng khuôn câu (bản hiện tại của nhánh) | bộ đầu: bắt nhầm **0 / 20** · 0 / 10 · nhận đúng **9 / 20** · bộ thêm: câu hỏi về một nơi **0 / 12** · về cả nhóm **0 / 3** · đối chứng 5 / 5 | [máy kiểm]; chờ E chạy lại |
| Test câu tự đặt cho từng họ lỗ, chạy trên hàm bản cũ | đỏ (5 câu tự đặt bản cũ nhận, bản mới không) | [máy kiểm] |
| Đếm lượt chạm đường đổi bằng hàm thuần | bộ 17 chuỗi đích (md5 `4e45408521db`): **0 / 46 lượt** ⇒ chuỗi gửi model của bộ đó không đổi ⇒ theo luật "đo đúng chỗ đổi" KHÔNG chạy lượt có phí bộ này · kịch bản "kể hết": chạm đúng lượt 2 · cả bộ 80 kịch bản: 1 / 106 lượt | [máy kiểm] |

Kết quả bộ dò từng câu + hai công cụ đếm (riêng tư): thư mục plan — `KQ_BO_DO_lan_1_8f43e3b.txt`, `KQ_BO_DO_lan_2_sau_sua.txt`, `chay_bo_do.py`, `dem_luot_cham.py`.

## 4. Chưa làm / giới hạn
- **Chưa đo qua hệ thống thật** (C chạy khi máy có lượt): kịch bản "kể hết" × 3 mỗi bên cùng buổi — ngưỡng ghi trước: bên bật kể đủ ≥ bên tắt; dấu vết phải thấy: lượt 2 bên bật KHÔNG có dòng ghi chú trong lịch sử.
- 11 / 20 câu xin liệt kê của bộ dò đầu bị bỏ sót (câu ghép, câu có số, viết tắt, câu không nêu loại nơi như "kể hết ra xem nào") — lượt đó giữ hành vi cũ, không tệ hơn. Đã dùng hết: một bộ dò thêm + một lần sửa; E chạy lại hai bộ mà còn câu ra sai ⇒ không gộp, giữ dòng giới hạn, không mở vòng.
- Lỗi có sẵn "danh sách thiếu mục" (bên cờ tắt cũng thiếu 1 / 3 lần) KHÔNG được chữa — bản sửa chỉ gỡ tác dụng phụ của dòng ghi chú.
- Khuôn chỉ biết 23 cụm chỉ loại nơi (quán, lăng, chùa, điểm tham quan…); loại nơi khác ("các bảo tàng đó") không được nhận — bỏ sót, không sai.
- Quan sát ngoài phạm vi: `uv run` trong worktree mới tự dựng `.venv` bằng Python 3.14.7, cây chính đang dùng 3.13.15 — test file này đạt ở 3.14; lượt đo của C dùng môi trường cây chính.
- Dòng giới hạn ở sổ tay bàn giao mục 10.1 và `bai_hoc/`: sửa SAU khi phép đo có kết quả (đạt ⇒ viết lại dòng; trượt ⇒ giữ nguyên, nhánh làm hồ sơ).

## 5. Lệnh kiểm
```bash
cd backend && uv run pytest tests/test_nho_ten_goi_y.py -q                     # 18 passed
PYTHONPATH=. uv run python <thư mục plan>/chay_bo_do.py <thư mục plan>/BO_DO_E.md   # bộ đầu: NHAN 9 / 20 · KHONG-RA SAI 0 / 20 · KHONG-nhẹ 0 / 10; bộ thêm: 0 / 12 · 0 / 3 · NHAN 5 / 5
PYTHONPATH=. uv run python <thư mục plan>/dem_luot_cham.py <bộ 17 chuỗi .jsonl>      # 0 / 46 lượt
```
