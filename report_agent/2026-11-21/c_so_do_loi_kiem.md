# Số đo `loi_kiem` — ghi LOẠI phép kiểm làm một lượt bị rút lại (nhánh `p9-c-so-do-loi-kiem`)

Viết: 14:37 21/11/2026 (giờ `date`), phiên C. Giao: phiên điều phối. Nền: main `1a7bc5a3`. Trạng thái: **code + test xong, chờ một phiên khác đọc diff rồi gộp.**

Từ dùng: *rút lại* = sau khi model viết, một phép kiểm bằng code không qua ⇒ người dùng thấy "Câu trả lời không đáp ứng yêu cầu trích dẫn" + nút Thử lại.

## 1. Người dùng thấy gì khác
Không gì cả. Lượt bị rút vẫn bị rút y như trước. Chỉ dòng log `chat_metrics` của mỗi lượt có thêm một khoá.

## 2. Vì sao
Hôm nay dòng log chỉ ghi `outcome: retracted` — không biết phép kiểm nào làm lượt bị rút. Sau các bản sửa gốc (lịch sử dính, vòng cuối viết rác, phép kiểm số), phiên đo cần đếm
riêng lượt "chữ model không có [n] nào" còn lại bao nhiêu để quyết có làm tiếp phần phục hồi bộ kiểm trích dẫn hay không.

## 3. Đổi gì
| File | Đổi gì |
|---|---|
| `backend/api/routes/chat.py` | Khoá mới `loi_kiem` trong `METRIC_FIELDS`; hàm `loai_loi_kiem` đọc đầu lời lỗi do chính code đặt ⇒ mã cố định: `khong_trich_dan` · `tu_choi_kem_trich_dan` · `ma_nguon_la` · `kiem_lich` · `so_thoi_tiet` · `so_khoang_cach` · `khac`; `None` = lượt không bị rút. Ghi ở `_copy_trace_metrics` (cả hai route). Không ghi chữ, không ghi lời lỗi. |
| `backend/tests/test_chat_stream.py` | Một test 4 ca: lượt qua kiểm ⇒ `None`; ba loại lỗi trích dẫn ⇒ đúng mã, lượt VẪN bị rút (có sự kiện `error`, `outcome: retracted`); bốn lời lỗi còn lại ⇒ đúng mã. |

Không đụng `assistant.py`: kết cục của lượt không đổi một dòng nào.

## 4. Bằng chứng [máy kiểm — hàm thuần + chữ dựng tay; không có lượt thật vì không đổi hành vi]
`R` = `HF_HUB_OFFLINE=1 UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv run --no-sync`, từ `backend/` của worktree.
- `R pytest tests/test_chat_stream.py -q` ⇒ `29 passed`. Đã thấy đỏ: cùng file test với `chat.py` của main ⇒ `4 failed, 25 passed`.
- Năm file dùng danh sách khoá số đo (`test_chat_stream`, `test_cache_tra_loi`, `test_api_chat`, `test_phuc_hoi_sau_kiem`, `test_b5b_thoi_tiet`) ⇒ `216 passed`, 1 lỗi có sẵn (test
  cần khoá OpenAI khi không nạp `.env`).

## 5. Chưa làm / giới hạn
- Mã đọc từ ĐẦU LỜI LỖI: ai đổi câu chữ của lời lỗi trong `llm/citations.py` / `assistant.py` mà không đổi bảng `_LOAI_LOI_KIEM` thì lượt đó ra mã `khac` (không sai, chỉ kém chi tiết).
- Lượt lịch bản 2 ("Lên kế hoạch") có đường kiểm riêng (`lich_trinh_kiem`) — không thuộc khoá này.
- Cả bộ test chưa chạy.

## 6. Bảng kết
| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Khoá `loi_kiem` + hàm phân loại | Xong | `R pytest tests/test_chat_stream.py -q -k which_check` ⇒ `4 passed` |
| Đếm trên thước sau các bản sửa gốc | Chưa — việc của phiên đo | lọc dòng `chat_metrics` theo `loi_kiem` |
