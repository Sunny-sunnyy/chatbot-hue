# STATUS B — KẾT PHIÊN TỐI 06/11 (22:41 06/11/2026 `date`; mở 20:54) — sổ tay cho phiên sau

Vai: thực thi. Terminal phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28` (đổi mỗi lần mở ⇒ `ListAgents`). Quyền phiên **hết hạn**. Không còn worktree `/tmp` của B. Không có code dở.

## Xong phiên tối 06/11
- **B171** sửa lỗi lịch trình: merge `main` `dbb4004` (cờ `lich_trinh` tắt; C ready `b0e52f8`). Tiền B171 0,028844 / 0,04. Nhánh `p9-b5-sua` chờ User xoá.
- **B172** nghiên cứu giao diện cổng: `data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md` (15 mẫu, 10 không nên chép) + `report_agent/2026-11-06_giao_dien_cong/b172_implementation.md`.
- **B173** 3 bản mẫu HTML tĩnh: `data/nghien_cuu_giao_dien_2026-11-06/mau/{1,2,3}.html` (1 Son thếp · 2 Sông Hương · 3 Tím Huế trầm = mốc hiện tại), 24 ảnh `mau/anh/`, bản so `mau/anh_nho/so_*.jpg`; tương phản đạt (6 chỗ dưới ngưỡng = nhãn ẩn); report `…/b173_implementation.md`. **Chưa ai soát ngoài B.**

## Việc dở / bước kế
- B173: chờ A đưa User chọn hướng. Thiếu, nếu User cần:
  - danh sách / chi tiết khác bố cục giữa 3 bản (hiện chung bố cục);
  - font tiêu đề có chân — cần thêm 1 gói `@fontsource`, chưa cài, cần duyệt;
  - ảnh thật (chưa có ảnh được phép).
  - Sinh lại: `uv run python data/nghien_cuu_giao_dien_2026-11-06/tools/dung_mau.py` rồi `chup_mau.py`, `do_tuong_phan.py`.
- Khi spec đợt 1 duyệt ⇒ B code (A giao).

## Tiền B phiên tối 06/11: 0,010975 USD (chỉ B171: M-1 0,002843 + T3 0,002337 + dòng tối 0,003915 + T5 / T5b 0,00188); B172 / B173 0 USD.

## Bẫy mới phiên tối
- Ảnh cả trang (Playwright `full_page`) vẽ phần tử `position: fixed` (nút nổi, thanh dưới) chồng giữa trang — xem vị trí thật bằng ảnh màn đầu.
- Đo tương phản: nhãn `.sr` (1 px) báo dưới ngưỡng — bỏ qua.
- Câu thử tự viết cho lịch trình phải có ý "lên lịch" rõ, nếu không model trả lời thẳng, không gọi `lich_trinh` (T5 phiên tối).
- Không `uv sync` ở `main` (gỡ sherpa-onnx của E).

## Sổ tay (từ phiên sáng 06/11, còn đúng)

## Dựng lại worktree (máy khởi động lại ⇒ `/tmp` mất)
- `git worktree prune`; `git worktree add /tmp/b_b5sua p9-b5-sua` (hoặc `/tmp/b_b5b p9-b5b`); trong worktree: `ln -s /home/minhhieu/hue_rag/data data && ln -s /home/minhhieu/hue_rag/knowledge-base-hue knowledge-base-hue`. Không đụng 4 worktree AGY (`~/.gemini/…`).
- Giao diện (`test_static_ui`, Playwright): `cd frontend && npm ci && npm run build` trong worktree.
- So bản cũ ↔ mới (`so_khung_cu_moi.py`): `mkdir -p /tmp/b171_cu/llm && git show main:backend/llm/lich_trinh.py > /tmp/b171_cu/llm/lich_trinh_cu.py`.

## Lệnh hay dùng (từ `backend/` của worktree, `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag …`)
- Q1: `env -u OPENAI_API_KEY -u SERPER_API_KEY OPENAI_API_KEY=capture-only … python ../data/phase_9/b2_chay/tools/capture_all.py <out>` ⇒ `cmp` với `../data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl` (sha `dba1f578eef1`; `main` sau đó chỉ đổi tài liệu).
- B5 có phí: `--env-file /home/minhhieu/hue_rag/.env python ../data/phase_9/b5/tools/chay_b5.py chay <bo> <out> [--chi id …]`; đếm `… dem <bo> <out>` (0 USD). Không ghi đè file cũ.
- B5b server: `B5B_API=<file> uvicorn --factory --app-dir /home/minhhieu/hue_rag/data/phase_9/b5b/tools app_thoi_tiet:make_app --port 8851`; `chay_b5b.py <BASE> <out> <log> --lan N --chi F03,F07`; `q8_b5b.py ui …`.
- B171 0 USD: `data/phase_9/b171/tools/tai_tao_la.py` (quét 120 tổ hợp), `so_khung_cu_moi.py` (1.728 tổ hợp cũ ↔ mới), `chay_khong_dong_toi.py` (biến thể bỏ dòng khung — có phí).
- Test rộng không key: mọi file `tests/*.py` trừ `test_phase6_live_smoke`, `test_openai_full_corpus_generator`, `test_startup_model_missing` ⇒ 2 hỏng đúng là test cần key.

## Tiền B phiên sáng 06/11 (USD) — tổng ≈ 0,0214
- B5b ≈ 0,0035 (Q8 0,00086 · đo lại F03 / F07 × 2 0,00266) ⇒ **B5b tổng ≈ 0,0544 / 0,07**.
- B171 0,017869 (17 câu 0,011375 · T3 thêm 6 lượt 0,006494) / trần **0,04**.

## Bẫy — đọc trước khi làm
- Chọn trước buổi sáng đã từng làm rơi điểm người dùng nêu (Bạch Mã) ⇒ điểm người dùng nêu luôn đứng trước; test `test_branches_of_the_plan` bắt được.
- Kiểm "nói ngược" theo từ dễ bắt nhầm lời khuyên nghỉ (C dò: 5 / 10) ⇒ luật rút lại cả câu chỉ nên bắt khi có **tên điểm** — lượt có phí 4 câu không đủ thấy bắt nhầm.
- Câu hỏi có / không về phần lịch không xếp ⇒ model trả nguyên câu từ chối kho (7 / 7) — đổi chữ dòng khung không giúp.
- Stream: chữ model phát dần ⇒ muốn thay chữ model phải giữ chữ chừng nào còn là khúc đầu câu từ chối (`giu_chu` B5b).
- Dặn cũ vẫn đúng: lệnh `git push` tách riêng (auto mode chặn khối ghép); push nhánh đã rebase ⇒ `--force-with-lease=<nhánh>:<sha cũ>`; báo cáo có backtick ⇒ `python3 - <<'PYEOF'`; chờ nền bằng `run_in_background` (không `pgrep -f`); tắt server bằng TaskStop; giờ lấy từ `date`; không gọi `agy`; không mở câu kín (`data/phase_9/b5/kin/`, `data/phase_9/b5_v2/`, `bo_do_b5/cau_sealed.jsonl`).
