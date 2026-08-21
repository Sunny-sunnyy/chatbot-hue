Cách chạy chuẩn của project (uv):

```bash
uv run python ...
uv run pytest ...
uv run uvicorn api.app:app --port 8000
```

Chạy module:

```bash
cd backend
uv run python -m ingestion.pipeline
```

Hoặc kích hoạt venv thủ công:

```bash
source .venv/bin/activate
```

Để thoát môi trường uv/virtualenv hiện tại, chạy:

```bash
deactivate
```
