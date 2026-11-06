# STATUS E — kết phiên 12:14 06/11/2026 (`date`) · terminal `hue-rag-99` · Claude Opus 5.5 · vai thực thi (Phase 9 B5 v2 câu tự nhiên + Phase 10 giọng nói)

## PHIÊN SAU ĐỌC TRƯỚC

### 1. E19 — bộ câu lịch trình tự nhiên cho B5 (việc A giao 06/11)

User đọc phiếu chấm B5 và thấy câu kín cũ không tự nhiên. Vì vậy cần bộ câu giống người thật hỏi.

- **(1)–(3) xong:**
  - TRIPO vòng 4: `data/nghien_cuu_tinh_nang_2026-11-06/tripo_v4/tripo_v4.md`.
  - Nghiên cứu cách người thật hỏi: Codex 2 lượt `data/tra_cuu_cli/2026-11-06_e19-*`, ra 20 lượt hỏi tiếng Việt trên VOZ; WebFetch kiểm 3 chủ đề.
  - Câu mẫu: `data/phase_9/b5_v2/mau_cau_tu_nhien.md` — 8 câu mẫu + bảng 15 loại ràng buộc R1–R15.
  - Report: `report_agent/2026-11-06_b5_cau_tu_nhien/e19_implementation.md` (A rà rồi commit).
- **User duyệt giọng 8 câu mẫu** ("Đạt, viết bộ kín theo giọng này"). A chốt hai câu hỏi còn lại:
  - **không** có câu hai lượt trong bộ kín;
  - **≥ 2 / 5** câu có phần ngoài lịch (chỗ ở / đi lại / giờ tới).
- **(4) bộ kín — đã viết:** `data/phase_9/b5_v2/cau_sealed.jsonl`, **5 câu**, md5 **`cd552f7cf7cb`** (sha256 `981ccb5120e6`). 4 / 5 câu có phần ngoài lịch.
  - Mỗi dòng có: `id`, `cau`, `rang_buoc`, `ngoai_lich`, `b5_mong` (trường B5 mong đợi), `can_cham` (điều cần chấm).
  - Không cho A / B / C xem. Báo A chỉ md5 + mã ràng buộc:

| Câu | Mã ràng buộc |
|---|---|
| K1 | R2 · R3 · R9 |
| K2 | R1 · R4 · R10 · R14 · R7 · R6 |
| K3 | R1 · R3 · R5 · R14 · R15 |
| K4 | R1 · R2 · R4 · R11 · R8 |
| K5 | R1 · R3 · R6 · R9 · R10 · R15 |

  - Đã đạt các yêu cầu ở §4 của file câu mẫu:
    - 1 câu ngắn thiếu số ngày;
    - 2 câu có tên điểm / lịch nháp;
    - 2 câu có người già / trẻ nhỏ;
    - câu có viết tắt kiểu "2N1Đ" / "ko";
    - 1 câu dài, kể hoàn cảnh, nhiều câu hỏi;
    - đủ 5 giá trị đi cùng (cặp đôi · người lớn tuổi · nhóm bạn · gia đình trẻ em · một mình).
  - Hàm dò số ngày của code (`do_so_ngay`) trên 5 câu: 4 câu ra đúng số; K1 ra None, đúng ý câu (thiếu số ngày).
- **Bước kế (CHƯA làm):**
  1. Viết `data/phase_9/b5_v2/duyet_tu_nhien_user.md` — bản cho **User** đọc, duyệt độ tự nhiên: 5 câu + ô tick "tự nhiên / sửa", không lộ `can_cham`. Đầu file ghi rõ "A / B / C không mở".
  2. Nhắn A **chỉ đường dẫn** để A đưa User.
  3. User sửa câu nào ⇒ E sửa ⇒ md5 mới ⇒ báo A.
  4. Sau đó A tổ chức: B171 sửa 2 loại lỗi code (đo trên bộ đã thấy) ⇒ chạy kín mới ⇒ 2 agent chấm ⇒ User đọc chỗ không đạt.

### 2. Giọng nói — NGHE (Phase 10)

- Spec bản 4 `784d6f7abd9f` đã duyệt.
- **G0 xong:** nhánh `p10-giong-noi` `93bbc63`, đã push.
- **G1:** chờ User thu 40 câu (`data/phase_10/giong_noi/thu/` **rỗng** lúc kết phiên). Bộ câu C205: `bo_40_cau/cau.jsonl` md5 `a24d445bfe61`.
- **Plan G1 + G2 bản 1:** `data/phase_10/giong_noi/plan_g2.md` sha256 **`555a35af92ab`**. **Chờ review** — A giao một sub-agent, kết quả sẽ ở `data/phase_10/giong_noi/plan_g2_review.md` ⇒ sửa nếu cần ⇒ A duyệt sha.
- Công cụ `data/phase_10/giong_noi/tools/`:

| File | sha256 (12) | Việc |
|---|---|---|
| `chuan_hoa.py` | `75544e8560e0` | chuẩn hoá chữ + số; tự kiểm 24 ca OK |
| `doi_wav.py` | `effed30bcf2a` | G1: ffmpeg ⇒ WAV 16 kHz mono + manifest; không xoá file gốc |
| `g2_do.py` | `10680ec17c79` | G2: V-a…V-e, chép 2 lần để kiểm tất định, `--cham` chấm lại |

  Đã chạy thử 0 USD trên 3 file mẫu kèm gói model (thư mục thử `/tmp` đã xoá).
- **Plan chốt** (reviewer có thể đổi):
  - gộp mọi người đọc khi quyết;
  - V-a tính cả cụm như nhãn `doc`;
  - vòng 1 thử hotwords điểm 4 / 8, vòng 2 điểm 12 hoặc 2;
  - V-e ≤ 1 / 40 lần đọc;
  - không nhận cách nói tắt "ba lăm nghìn" / "một triệu hai".
- **Khi User thu xong:** kiểm `thu/nguoi_doc.md` (không tên thật) ⇒ `doi_wav.py` ⇒ xoá file gốc (User `!` nếu `rm` bị chặn) ⇒ đo theo plan ⇒ report ⇒ A.
- Tạo lại worktree khi cần code G3: `git worktree add /tmp/e_giong p10-giong-noi`.
- TTS: để sau.

### 3. Việc cũ còn chờ User (A hỏi)

- Bật `anh.bat`?
- Xoá collection thử `hue_anh_siglip2` (172 điểm)?
- Luật "gói Python ≥ 2 tuần"?

## Tiền

- **E phiên 06/11: 0 USD.** Codex tra web chạy bằng gói ChatGPT; TRIPO không tốn; Playwright và đo giọng nói chạy trên máy.
- Phase 10 tổng vẫn 0,098380 / trần 0,15.

## Bẫy / đã học

- `.venv` chung **có `sherpa-onnx`**, nhưng `uv.lock` của `main` chưa có (tới khi `p10-giong-noi` merge).
  - `uv run` giữ gói; **`uv sync` thường ở `main` sẽ gỡ mất**.
  - Cài lại: từ worktree nhánh chạy `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen`.
- **Codex tra web tiếng Việt:** lượt chung chung chỉ ra 1 bài tiếng Việt. Lượt hai chỉ rõ diễn đàn (VOZ…) và đòi "mở trang 1 của chủ đề" thì ra 20 lượt hỏi ⇒ yêu cầu phải nêu nơi tìm cụ thể.
- **TRIPO:** biểu mẫu đủ trường ⇒ không gọi mô hình, không hỏi thêm.
  - Chỉ bấm "Xác nhận phương án"; chờ chữ trang dài thêm ≥ 150–200 ký tự rồi đứng yên 3 × 2 s (đây là bài học vòng 3).
  - Ô nhập tự sinh câu chậm hơn lúc bấm chip ⇒ đọc giá trị sau cùng.
- **`do_so_ngay`** không dò được "4n3d" (d không dấu), "2 hôm", "cuối tuần", "đi trong ngày" ⇒ dựa vào model. Đã báo A; không phải lỗi.
- **Hàm chuẩn hoá số:**
  - "không" trong "phải không" từng bị đọc thành 0 ⇒ đã bỏ;
  - "hai trăm nghìn một người" từng ra 200.001 ⇒ đã tách số đơn đứng sau "nghìn".
- CSP trang chặn `page.wait_for_function` của Playwright ⇒ chờ bằng locator.
- Script đặt theo đường dẫn không thấy gói `backend/` ⇒ `PYTHONPATH=<worktree>/backend`.

## Câu hỏi cho A

- Bộ kín B5 v2: chạy bằng harness đo B5 cũ, đổi đường dẫn bộ câu, hay cần chỗ đọc trường `b5_mong` / `can_cham` cho 2 agent chấm? Người chạy kín không được xem câu, nên cần lệnh `!` chỉ in số đếm (`Session_Prompt.md` §5).
- Plan G2: chờ kết quả review của sub-agent.
