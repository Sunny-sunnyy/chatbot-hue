# STATUS A — cập nhật 11:39 31/10/2026 (phiên 31/10)

Terminal: `hue-rag-1a` · Agent: Claude Opus 5.5 · Vai: điều phối. B = `hue-rag-3b`, C = `hue-rag-69` (cả ba Claude Code, trực tiếp).

## Đang làm
- Streaming: User chốt **D1 = PA1** (11:26); đang hỏi D2 (thước tốc độ) ⇒ D3 ⇒ spec (căn cứ nháp v3 bản 3 `3b6a9ba09149`).
- Tra web bằng Codex: script + chặn `agy` + §9 + AGENTS.md luật 7 — B103 ready vòng 3 ⇒ chờ User chạy lệnh commit `!`.

## Đang khai báo sửa
- `scripts/tra_web_codex.sh`, `.claude/settings.json`, `AGENTS.md`, `session_prompt/Session_Prompt.md`, `report_agent/README.md`, `CURRENT_HANDOFF.md` (xong, chờ commit).

## Tiền paid
- A 0 USD (Codex / AGY theo gói tài khoản User).

## Đã học / bẫy gặp (phiên 31/10)
- **Gọi `agy` 4 lần trước khi kiểm điều khoản** — FAQ Google cấm phần mềm bên thứ ba (nêu tên Claude Code) truy cập Antigravity. Bài học: công cụ / tài khoản bên ngoài mới ⇒ kiểm
  điều khoản dùng tự động **trước** lượt chạy đầu (đầu vào vòng cải tiến). Đã chặn bằng `.claude/settings.json` + AGENTS.md luật 7 + memory.
- Model mặc định `~/.codex/config.toml` không dùng được với tài khoản ChatGPT ⇒ script chỉ định `-m gpt-6-luna`; `--search` phải đứng trước `exec`.
- Bộ đếm lệnh shell viết theo đoán định dạng log ⇒ B bắt (B103 M-1); dùng `--json` có tài liệu + thử bằng lệnh thật.
- Lệnh `rm` với biến `$t/*` bị chặn an toàn ⇒ dùng đường dẫn cố định.
