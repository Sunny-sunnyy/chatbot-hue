# Review Docker nháp của E (C, 11:37 15/11/2026) — **ready_for_user_confirmation**, 0 / 0 / 1

- **Phạm vi:** diff `data/phase_12/deploy_nhap/{Dockerfile, Dockerfile.dockerignore, dung_dockerignore.py}` với `sao_luu_2026-11-15/`; đúng 3 file, khớp report `e_docker_nhap.md`. Không build lại.
- **Kiểm [Chạy]:** đủ 8 / 8 đường dữ liệu `../data|knowledge-base-hue` trong `settings.yaml` đều có COPY (hoặc thuộc thư mục COPY cả cụm) và có dòng mở trong `.dockerignore`. Gồm: conditions, diem_v3, diem_v8, toạ độ v7, ảnh lịch v2, lưu trú v3, quán v1, danh sách ảnh.
- **Kiểm [Chạy]:** `.dockerignore` mở 264 dòng kho = 263 bài + 1 file điều kiện.
- **Symlink:** `ln -s dist /app/frontend/public` là đường tương đối trong `/app/frontend` ⇒ trỏ `/app/frontend/dist`. Vite chép `public/` vào gốc `dist/` ⇒ `public/anh/…` có thật ⇒ đúng nguyên nhân thoát mã 3 E tìm ra. Kết quả chạy container lấy từ report của E, C không chạy lại.
- **m-1:** danh sách file bảng phải sửa tay ở 2 chỗ (`CHUA` + `COPY`), đã quên một lần. Gợi ý cho lần đóng gói thật: một test so `settings.yaml` ↔ `CHUA`. Không chặn.
