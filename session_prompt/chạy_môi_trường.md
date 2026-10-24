Cách chạy chuẩn của project (uv):

```bash
uv run python ...
uv run pytest ...
uv run uvicorn api.app:app --port 8000
```

Chạy module (ví dụ build index full-corpus — **ghi Qdrant**, chỉ chạy khi việc cho phép; chạy từ gốc repo):

```bash
HF_HUB_OFFLINE=1 uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate e5-small-384
```

Hoặc kích hoạt venv thủ công:

```bash
source .venv/bin/activate
```

Để thoát môi trường uv/virtualenv hiện tại, chạy:

```bash
deactivate
```
