# Ảnh app trợ lý Huế (FastAPI + giao diện dựng sẵn + kho + bảng dữ liệu) cho MỘT máy Linux. Qdrant và Caddy là ảnh riêng (compose.yml).
# KHÔNG build thẳng từ thư mục repo: ngữ cảnh build là thư mục do `dung_ngu_canh.py` dựng (đúng file cần, từ đúng một commit) — chạy `dung_anh.sh`.
# ⚠ Ảnh mang 11 file bảng riêng tư lấy từ `data/` (kê ở /app/DANH_SACH.txt) ⇒ KHÔNG đẩy lên kho ảnh công khai; chuyển bằng `docker save` hoặc kho
#   ảnh riêng. Ảnh KHÔNG mang khoá nào: quyền gọi model và khoá tra web gắn vào lúc chạy (compose).

# --- 1. Giao diện: bản dựng tĩnh ---
FROM node:24-slim AS web
WORKDIR /w
COPY frontend/package.json frontend/package-lock.json frontend/.npmrc ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# --- 2. App Python ---
FROM python:3.13-slim
# cùng bản uv tạo ra uv.lock trên máy chủ dự án (`uv --version` 0.12.5, kiểm 23/11/2026)
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy HF_HOME=/app/hf TIKTOKEN_CACHE_DIR=/app/tiktoken PYTHONUNBUFFERED=1

# Phụ thuộc theo uv.lock, riêng torch lấy bản CPU: uv.lock khoá torch nguồn PyPI (bản Linux kéo theo gói CUDA vài GB) ⇒ bỏ dòng nvidia-* / cuda-* /
# triton rồi cài với `--torch-backend cpu`. `--no-cache`: cache uv ~1,9 GB trùng .venv sẽ nằm lại trong ảnh (đo 10/11: 6,12 ⇒ 3,57 GB).
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-hashes --no-emit-project | grep -vE '^(nvidia-|cuda-|triton)' > /tmp/req.txt \
 && uv venv /app/.venv && uv pip install --no-cache --python /app/.venv --torch-backend cpu -r /tmp/req.txt
ENV PATH=/app/.venv/bin:$PATH

# Model nhúng e5-small đúng revision runtime kiểm (`backend/embedding/full_corpus.py`) + bảng mã đếm token, tải LÚC BUILD ⇒ lúc chạy không cần mạng
# tới Hugging Face. Xoá `trees/`: huggingface_hub lưu danh sách file của repo, có danh sách thì `snapshot_download(local_files_only=True)` của runtime
# báo thiếu 30 file không tải ⇒ app trả 503 (thử thật 07/11).
RUN python -c "from huggingface_hub import snapshot_download as s; s('intfloat/multilingual-e5-small', revision='614241f622f53c4eeff9890bdc4f31cfecc418b3', \
    allow_patterns=['*.json','model.safetensors','sentencepiece.bpe.model','1_Pooling/*'])" \
 && rm -rf /app/hf/hub/models--intfloat--multilingual-e5-small/trees /app/hf/xet \
 && python -c "import tiktoken; tiktoken.get_encoding('o200k_base')"
ENV HF_HUB_OFFLINE=1

# Code + kho + bảng dữ liệu. Ngữ cảnh chỉ có đúng file cần (dung_ngu_canh.py) ⇒ chép cả thư mục, không kê từng file ở đây.
COPY backend/ /app/backend/
COPY knowledge-base-hue/ /app/knowledge-base-hue/
COPY data/ /app/data/
COPY DANH_SACH.txt lam_moi_khoa.py /app/
COPY --from=web /w/dist /app/frontend/dist
# Lúc khởi động code kiểm file ảnh của lịch có thật dưới `frontend/public/` (`llm/lich_trinh_v2.FRONTEND_PUBLIC`, `api/routes/xuat.THU_MUC_ANH`); Vite đã
# chép `public/` vào `dist/` ⇒ trỏ public về dist. Thiếu dòng này: uvicorn thoát mã 3, không in lỗi (thử thật 15/11).
RUN ln -s dist /app/frontend/public

WORKDIR /app/backend
EXPOSE 8000
# MỘT tiến trình: kho cuộc trò chuyện, lịch đã lưu, sổ đếm giới hạn lượt đều nằm trong RAM ⇒ không `--workers` > 1.
# `--forwarded-allow-ips '*'`: app không mở cổng ra máy, chỉ Caddy (hộp khác cùng mạng compose) gọi tới; cần để giới hạn lượt đếm theo địa chỉ thật.
# `--no-access-log`: nhật ký truy cập của uvicorn in địa chỉ IP người gọi ra log Docker (bảng rủi ro 22/11, R9); số đo từng lượt đã có ở log của app, không có IP.
# compose.yml chạy cùng lệnh này sau khi chờ Qdrant — sửa ở đây thì sửa cả ở đó.
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*", "--no-access-log"]
