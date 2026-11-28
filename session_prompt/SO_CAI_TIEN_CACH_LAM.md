# Sổ cải tiến cách làm — harness của các session

Cập nhật lần cuối: 12:35 28/11/2026 (A — vòng kết phiên 28/11: `0` luật chữ tự thêm mới, cụ thể hoá `--squash` ở `WORKFLOW.md` §9.6 theo chốt của Hiếu, gọt bộ file mở phiên `< 24 KB`, lưu trữ lịch sử).
Lịch sử đầy đủ trước 28/11 (W1–W68, S1–S130b, các vòng 25/10–25/11): `session_prompt/archive/SO_CAI_TIEN_LICH_SU_2026-11-28.md`.

**Kỷ luật vận hành từ tối 23/11/2026 (chủ dự án chọn để nhóm tự giữ):**
- Vòng cải tiến chỉ **GỠ / GỌT** hoặc ghi bẫy; thêm câu luật chữ mới phải đợi **lần lặp thứ 3** (trừ rào máy cho hậu quả không đảo được: lộ / mất dữ liệu / khoá tài khoản).
- Thước theo dõi: báo "xong" bị lật lại · User phải nhắc lại · User phải tự gợi hướng · User nhắc test quá đà · con số sản phẩm (`HIEN_TRANG.md` §2).

## Các thay đổi / rào đang giữ hiệu lực (tóm tắt)

| Nhóm | Mục đang giữ | Ở đâu | Ghi chú / xem lại |
|---|---|---|---|
| Cốt lõi quy trình | `W1`, `W3`, `W11`, `W13`, `W32`, `W38` | `improve-workflow`, `run-experiment`, `WORKFLOW.md`, `risk-gated-agent-review` | Tiêu chí ghi trước, không tự kiểm, ca dò khác cách, chỉ gỡ/gọt trước khi thêm |
| Git & `main` sạch | `W16`, kỷ luật 26/11 + 28/11 | `.githooks/pre-commit`, `WORKFLOW.md` §9.6 | Chặn secret/`data/`/`*sealed*`; nhánh riêng tự do, vào `main` bắt buộc `git merge --squash` theo mốc (1–2 commit/đợt) |
| An toàn & bí mật | `W5`, `W12`, `W26`, `W27`, `W34` | `.githooks/pre-commit`, `scripts/grep_kb.sh`, `AGENTS.md` | Không `data/`/`*sealed*`/tên dự án khác; `git grep -- ':!knowledge-base-hue'`; cấm `agy` CLI |
| Thời gian & máy | `W30`, `W31`, `W37`, `pkill -f` | `.githooks/pre-commit`, `AGENTS.md` | Giờ trong file luôn lấy từ `date`; 1 việc nặng/lúc; tắt server bằng `pkill -f "[u]vicorn ..."` |
| Đọc hiểu & số liệu | `W6`, `W14`, `W18`, `W21`, `W28`, `W36`, `W40`, `W65–W67` | `AGENTS.md`, `WORKFLOW.md`, `propose-options` | Nhắc lại cách hiểu trước khi xây; probe thật trước khi khẳng định; nhãn `[máy kiểm]`/`[chưa kiểm]` |
| Gọn hồ sơ | `I7`, `I9`, đợt gọt 23/11 & 28/11 | `session_prompt/archive/`, `HIEN_TRANG.md` | Dời nhật ký/sự cố cũ sang `archive/`, giữ `HIEN_TRANG.md < 24 KB` để mở phiên nhanh |

## VÒNG CẢI TIẾN 28/11/2026 — chạy 12:35 28/11/2026 (`0 USD`, sau Đợt 5A)

- **Bốn con số đợt 26–28/11 (nguồn: `CURRENT_HANDOFF.md`, `VIEC_DA_XONG.md`, hội thoại 28/11):**
  - Báo "xong" bị lật lại: **`0`**.
  - User phải nhắc lại: **`2`** — (1) `12:20 28/11`: Hiếu gửi ảnh `1.png` lỗi `0x2` khi Ctrl+Click đường dẫn ngắn `data/...` do Markdown link `[...](file://...)` bị CLI rút gọn trên Windows IDE; (2) `12:32 28/11`: Hiếu nhắc `main` tăng **7 commit trong 3 tiếng sáng 28/11** dù ngày 26/11 đã dặn gom gọn vào `main` (gốc do gộp bằng `git merge --no-ff` thay vì `--squash` và gộp cắt khúc từng worker).
  - User phải tự gợi hướng: **`2`** (`google-research/harness2` gợi khám phá + nhắc dùng các skills `.agents/skills` trước khi kết phiên).
  - User nhắc test quá đà / chi tiêu dư: **`0`** (Đợt 5A tổng `0,120794 USD`, 0 test thừa; phân tích `harness2` `0 USD`).
  - Sản phẩm: `68 → 70 MỞ / 8 TẮT`, Qdrant `9.540` điểm, Đợt 5A 2 vòng kiểm định sạch (`KET_LUAN_DOT5A.md`), `25` file giáo trình đồng bộ (`6b01170b`).
- **Đối chiếu hai chiều (làm thừa ↔ nhìn hẹp):**
  - *Làm thừa:* tạo quá nhiều commit trên `main` (`7` commit cho 1 đợt 5A trong 3 tiếng) vì `git merge --no-ff` bê nguyên 3 commit sửa vòng trong nhánh code + merge commits + tách lẻ nhánh giáo trình + commit chốt sổ lên thẳng `main`; chưa chủ động dọn 9 nhánh `p18..p22` và bộ file mở phiên sau Đợt 4A.
  - *Nhìn hẹp:* để `HIEN_TRANG.md` phình tới `156 KB` và `SO_CAI_TIEN_CACH_LAM.md` tới `198 KB`; đưa đường dẫn dạng `[...](file://...)` hoặc đường dẫn tương đối không tương thích với Ctrl+Click terminal IDE trên Windows.
- **Thay đổi quy trình:** `0` luật chữ tự thêm mới; cụ thể hoá 1 câu ở `WORKFLOW.md` §9.6 theo chốt trực tiếp của chủ dự án `12:34 28/11` (**bắt buộc `git merge --squash`** khi đưa vào `main` và chỉ gộp theo mốc / cuối đợt, tối đa **1–2 squash commit/đợt**). Việc đường dẫn text thuần `/home/minhhieu/hue_rag/...` ghi vào `data/bo_nho_agent/MEMORY.md` + `HIEN_TRANG.md` §4 + mục bẫy dưới.
- **Gọt gọn hồ sơ mở phiên (`wc -c` trước ⇒ sau khi gọt):**
  - `AGENTS.md`: `13.115` B ⇒ `13.115` B (giữ nguyên)
  - `START_SESSION.md`: `4.818` B ⇒ `4.818` B (giữ nguyên)
  - `HIEN_TRANG.md`: `156.704` B ⇒ `21.581` B (-86,2%)
  - `VIEC_DANG_MO.md`: `9.520` B ⇒ `9.520` B (giữ nguyên)
  - `CURRENT_HANDOFF.md`: `21.804` B ⇒ `5.204` B (-76,1%)
  - `SO_CAI_TIEN_CACH_LAM.md`: `198.556` B ⇒ `7.040` B (-96,4%)
  - `data/bo_nho_agent/MEMORY.md`: `14.181` B ⇒ `15.480` B
- **Bẫy mới ghi nhận (26–28/11):**
  1. *Merge `--no-ff` làm rác `main` (`28/11`):* gộp nhánh `/swarm` bằng `--no-ff` đổ mọi commit sửa vòng lên `main` ⇒ luôn dùng `git merge --squash` theo mốc cuối đợt (`WORKFLOW.md` §9.6).
  2. *Đường dẫn Ctrl+Click trên Windows Antigravity IDE (`1.png`, 28/11):* `[text](file:///home/minhhieu/hue_rag/...)` bị rút gọn thành `data/...` gây lỗi `0x2` ⇒ luôn in đường dẫn tuyệt đối Linux **text thuần** `/home/minhhieu/hue_rag/...` (không bọc `[...](file://...)` hay backtick) cho Hiếu.
  3. *Đóng gói Docker & cờ LLM (`28/11`):* `backend/config/settings.yaml` mở `slide_designer_cfg.use_llm: true` để Hiếu thử ở local; `deploy/dong_goi.sh` ép `false` (`0,36s / 0đ`).
  4. *Sandbox chuẩn & `.git`/Qdrant cục bộ (`28/11`):* ghi `.git/index.lock` và nối loopback `127.0.0.1:6335` bị chặn trong sandbox chuẩn (nên subagent `research` tưởng Qdrant `:6335` tắt khi kiểm từ trong sandbox) ⇒ tách riêng lệnh git/mạng cục bộ khi cần kiểm thật.
  5. *Phình sổ mở phiên qua nhiều đợt liên hoàn (`26–28/11`):* chạy `improve-workflow` dời lịch sử sang `session_prompt/archive/` sau mỗi đợt lớn để `HIEN_TRANG.md` giữ `< 24 KB`.

## Tóm tắt vòng liền trước (24–25/11/2026)
- Chạy `15:59 25/11/2026`: `0` luật chữ mới; chuyển `WORKFLOW.md` §9.9 (nhãn chưa kiểm) & `AGENTS.md` (`pkill -f`) sang `đang dùng`; giữ kỷ luật chỉ gỡ/gọt, thêm luật mới ở lần 3; áp cấu hình `agy` CLI + `/swarm` + `gpt-6-luna`.
