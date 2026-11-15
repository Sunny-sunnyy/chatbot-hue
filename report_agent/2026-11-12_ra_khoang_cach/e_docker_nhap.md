# Sửa bản Docker nháp + chạy thử (E · 11:35 15/11/2026, `date`)

A giao 15/11 (User duyệt). File deploy nằm trong `data/phase_12/deploy_nhap/` (**gitignored, private**) ⇒ không có nhánh git. Review bằng diff với bản
sao lưu `data/phase_12/deploy_nhap/sao_luu_2026-11-15/` (`Dockerfile`, `dung_dockerignore.py`, `Dockerfile.dockerignore` trước khi sửa).

## Đổi gì
1. `dung_dockerignore.py` (`CHUA`): `bang_anh_v1` ⇒ `bang_anh_v2`; thêm `diem_toa_do_v7`, `bang_luu_tru_lich_v3`, `bang_quan_lich_v1`.
2. `Dockerfile`: 5 dòng `COPY` (`diem_v8`, `diem_toa_do_v7`, `bang_anh_v2`, `bang_quan_lich_v1`, `bang_luu_tru_lich_v3`). Trước chỉ có `diem_v3` + `danh_sach_ten`.
3. `Dockerfile`: `RUN ln -s dist /app/frontend/public`.
   - Lỗi thật lộ ra khi chạy thử: `nap_bang_anh` kiểm file ảnh có thật dưới `frontend/public/` (`lich_trinh_v2.py:355/367`), mà image chỉ có `frontend/dist/`.
   - Hệ quả: `ValueError` ⇒ uvicorn thoát mã 3, **không in lỗi** (log cấu hình riêng nuốt mất).
   - Lỗi có từ khi bật `anh_lich` 14/11, sau lần build trước (10/11).
4. `Dockerfile.dockerignore` dựng lại theo build record mới (C dựng chỉ mục 11:22). Bản cũ chỉ mở **204 bài kho** ⇒ image cũ thiếu 59 bài; nay 263 bài + 14 mục.

## Kiểm [Chạy]
- Build `hue-rag-app:e1511` (3,6 GB): exit 0 (lần đầu ~1 phút nhờ lớp cũ; lần 2 sau sửa 3 s).
- Container `e_dep_thu` (`--memory 2g`, Qdrant đọc qua `127.0.0.1:6335`, `HUE_TRA_WEB=false`, `HUE_COOKIE_SECURE=0`, `HUE_TAT_DOCS=1`). Kiểm bằng `docker exec` từ trong container: Docker Desktop không đưa cổng của mạng host ra WSL.

| Kiểm | Kết quả |
|---|---|
| `/health` | 200; app · qdrant · retrieval · tokenizer · generator đều `ready` |
| `/api/cho_o` | 200; 4 nhóm, 137 cơ sở |
| `/api/kham_pha` | 200; 263 bài |
| `/api/tinh_nang` | 200 |
| Một lịch 3 ngày (biểu mẫu, `ngan_sach: cao`) | 200; ô Nơi ở khu trung tâm, 5 cơ sở 4–5 sao, đủ ảnh; 6 / 6 bữa có quán hoặc câu nhắc; chữ trả lời có "Nơi ở gợi ý" + "Ăn uống gợi ý"; 11 nguồn |
| RAM container | 1,12 / 2 GiB |

- Container đã `stop` + `rm`; chỉ còn container Qdrant của dự án chạy như trước. Image `e1511` để lại cho người review (xoá được: `docker rmi hue-rag-app:e1511`). Image cũ `dep10b` không đụng (câu "xoá ảnh docker cũ" đang chờ User).
- **Tiền:** 2 lượt lịch × ≈ 0,0007 USD (một lượt đầu trả 422 do E gửi sai tên trường `message` thay vì `query` — lỗi của lệnh kiểm, không phải app).

## Ghi cho deploy
- `docker run --env-file .env` của máy User báo lỗi khuôn: **một dòng trong `.env` có tên biến kèm khoảng trắng**. E không mở file; truyền đúng 2 khoá qua `uv run --env-file` + `-e TÊN`. Trên AWS dùng file `/srv/hue/.env` mới (compose `env_file`) ⇒ viết đúng khuôn `TÊN=giá trị`. User có thể sửa dòng đó ở máy mình khi tiện.
- Thêm file bảng mới vào `settings.yaml` ⇒ thêm ở **cả** `CHUA` lẫn `COPY` (đã ghi chú trong Dockerfile).
