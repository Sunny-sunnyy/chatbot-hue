Cách chạy chuẩn của project (uv):

```bash
cd backend   # mọi lệnh chạy từ backend/ — quy ước import trần (rà code gói 1b, 25/10)
uv run python ...
HF_HUB_OFFLINE=1 uv run python -m pytest tests/<file> -q
HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000
```

Chạy module (ví dụ build index full-corpus — **ghi Qdrant**, chỉ chạy khi việc cho phép; chạy từ `backend/`):

```bash
cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m ingestion.full_corpus_pipeline build --candidate e5-small-384
```

Hoặc kích hoạt venv thủ công:

```bash
source .venv/bin/activate
```

Để thoát môi trường uv/virtualenv hiện tại, chạy:

```bash
deactivate
```
