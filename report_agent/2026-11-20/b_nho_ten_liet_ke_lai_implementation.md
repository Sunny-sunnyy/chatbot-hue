# Việc 2 — cờ `nho_ten_goi_y`: câu hỏi tiếp xin liệt kê lại không nhận dòng ghi chú (B, 08:33 20/11/2026, giờ `date`)

Trạng thái: **code + test + bộ dò xong (0 USD); CHỜ review của E và hai phép đo qua hệ thống thật của C.** Chưa gộp. Plan mức nhẹ (riêng tư, phiên điều phối
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

**Luật nhận câu — hẹp có chủ ý** (bắt nhầm ⇒ mất ghi chú ⇒ quay lại lỗi nói chắc sai nơi, nặng hơn bỏ sót): câu được nhận khi (a) có một cụm xin danh sách đủ
("kể hết", "liệt kê", "tất cả", "danh sách"…), (b) sau khi bỏ các cụm trỏ lại ("trong bài đó", "ở trên", "vừa rồi"…) MỌI từ còn lại thuộc bộ từ cho phép (lịch sự,
trỏ lại, danh từ chỉ nơi), và (c) "đó / này / ấy / kia" phải có "các / những / mấy / mọi" đứng trước ("nêu đủ tên quán đó" là hỏi về MỘT nơi ⇒ không nhận).
Câu ghép có nửa hỏi về một nơi tự rơi ra ở (b). Không cần đọc cờ: cờ tắt thì lịch sử không có dòng ghi chú ⇒ hàm trả đúng nội dung cũ.

## 3. Bằng chứng (tất cả 0 USD; chưa có lượt nào qua model thật)
| Phép | Kết quả | Nhãn |
|---|---|---|
| Test file chạm `tests/test_nho_ten_goi_y.py` (đồ giả chỉ để dựng điều kiện) | 18 đạt, ~10 giây | [máy kiểm] |
| Test mới thấy ĐỎ: hàm luôn trả sai ⇒ 4 hỏng · luôn trả đúng ⇒ 4 hỏng · lượt liệt kê ghi đè kho lịch sử ⇒ test loại lượt hỏng · bỏ luật (c) ⇒ 1 hỏng | đỏ cả bốn kiểu phá | [máy kiểm] |
| Bộ dò 54 câu do E soạn mù, chạy thẳng hàm — **lần đầu, nguyên trạng** (mã `8f43e3b`, bộ từ chốt trước khi mở file) | câu hỏi về một nơi bị bắt nhầm **0 / 20** (sàn 0) · câu ngoài phạm vi bị bắt 0 / 10 · câu xin liệt kê nhận đúng **5 / 20** | [máy kiểm] |
| Bộ dò, sau MỘT lần sửa bộ từ (thêm 10 từ + cụm "vừa rồi" + luật (c)) | bắt nhầm 0 / 20 · 0 / 10 · nhận đúng **14 / 20**; 4 câu không nhãn cứng: 0 nhận | [máy kiểm]; E chạy lại khi review |
| Đếm lượt chạm đường đổi bằng hàm thuần | bộ 17 chuỗi đích (md5 `4e45408521db`): **0 / 46 lượt** ⇒ chuỗi gửi model của bộ đó không đổi ⇒ theo luật "đo đúng chỗ đổi" KHÔNG chạy lượt có phí bộ này · kịch bản "kể hết": chạm đúng lượt 2 · cả bộ 80 kịch bản: 1 / 106 lượt | [máy kiểm] |

Kết quả bộ dò từng câu + hai công cụ đếm (riêng tư): thư mục plan — `KQ_BO_DO_lan_1_8f43e3b.txt`, `KQ_BO_DO_lan_2_sau_sua.txt`, `chay_bo_do.py`, `dem_luot_cham.py`.

## 4. Chưa làm / giới hạn
- **Chưa đo qua hệ thống thật** (C chạy khi máy có lượt): kịch bản "kể hết" × 3 mỗi bên cùng buổi — ngưỡng ghi trước: bên bật kể đủ ≥ bên tắt; dấu vết phải thấy: lượt 2 bên bật KHÔNG có dòng ghi chú trong lịch sử.
- 6 / 20 câu xin liệt kê của bộ dò bị bỏ sót (câu ghép dài, có số, viết tắt, "của") — lượt đó giữ hành vi cũ, không tệ hơn. Theo luật chỉ còn được thêm đúng MỘT bộ dò ≤ 20 câu của E; còn sai ⇒ ghi giới hạn, không mở vòng.
- Lỗi có sẵn "danh sách thiếu mục" (bên cờ tắt cũng thiếu 1 / 3 lần) KHÔNG được chữa — bản sửa chỉ gỡ tác dụng phụ của dòng ghi chú.
- Lỗ đã biết của luật nhận: câu không có giới từ kiểu "liệt kê các điểm tham quan lăng đó" (thiếu "ở / trong / của") sẽ bị nhận — chưa thấy thật, không chặn.
- Quan sát ngoài phạm vi: `uv run` trong worktree mới tự dựng `.venv` bằng Python 3.14.7, cây chính đang dùng 3.13.15 — test file này đạt ở 3.14; lượt đo của C dùng môi trường cây chính.
- Dòng giới hạn ở sổ tay bàn giao mục 10.1 và `bai_hoc/`: sửa SAU khi phép đo có kết quả (đạt ⇒ viết lại dòng; trượt ⇒ giữ nguyên, nhánh làm hồ sơ).

## 5. Lệnh kiểm
```bash
cd backend && uv run pytest tests/test_nho_ten_goi_y.py -q                     # 18 passed
PYTHONPATH=. uv run python <thư mục plan>/chay_bo_do.py <thư mục plan>/BO_DO_E.md   # NHAN 14 / 20 · KHONG-RA SAI 0 / 20 · KHONG-nhẹ 0 / 10
PYTHONPATH=. uv run python <thư mục plan>/dem_luot_cham.py <bộ 17 chuỗi .jsonl>      # 0 / 46 lượt
```
