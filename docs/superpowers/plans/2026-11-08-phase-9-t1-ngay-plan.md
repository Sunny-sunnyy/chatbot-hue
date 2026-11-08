# Plan — T1 ngày + âm lịch (spec Phase 9 bản 13 §12, sha `5557f0fd7650`)

Người viết: E · bản 1 · 11:03 08/11/2026 (`date`) · trạng thái: **chờ A duyệt / chọn người review** (≤ 1 vòng nếu chỉ còn minor — User 08/11: nhanh nhất có thể).
Nhánh `p9-t1-ngay` từ `main` mới nhất, worktree `/tmp/e_t1`.

## 1. Vấn đề, mốc, tiêu chí (ghi trước — chép spec §12.2 / §12.3, chốt số)

- **Vấn đề:** câu "hôm nay / tuần này / rằm tháng Giêng năm nay" bị từ chối nhầm vì model không biết ngày. Đã đo 27/10: 6 / 14 câu. Thêm dòng ngày vào tin nhắn (B1 P2, cờ `today_line`) không đỡ.
- **Mốc:** `main` với cờ mới `ngay_lich: false`, chạy **cùng lượt** với nhánh khi cờ bật. Mỗi bên ×2.
- **Đạt khi đủ cả 4:**
  1. **Từ chối nhầm ở câu ngày giảm ≥ 3 câu** so với mốc, trên bộ quyết (mục 3), tính trung bình 2 lượt. Từ chối nhầm = chữ trả lời là `INSUFFICIENT_ANSWER` cho câu có đáp án trong kho / có thể trả lời bằng ngày.
  2. **0 ngày / thứ sai trong chữ trả lời** (L2), cả khi model không gọi công cụ. Code bắt mọi cụm "thứ …", "dd/mm(/yyyy)", "ngày … tháng …", "mùng / rằm / mồng …", "hôm nay / ngày mai là …" rồi đối chiếu với đáp án tính theo **ngày chạy** bằng cùng hàm của công cụ. Câu bị code đánh dấu ⇒ sub-agent ngữ cảnh mới đọc lại; sai thật ⇒ trượt.
  3. **S1 bộ an toàn 32 ×2: đủ 4 số** (đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 · ngoài kho bị trả lời 0; thủ tục S-AT khi chênh 1).
  4. **S4 Golden mẫu 30** (`data/phase_9/bo_do_b1/mau_golden_30.json`): không tụt quá nhiễu, chấm mù cùng lượt với mốc (2 sub-agent, như B1 P5).
- **Báo thêm (không sàn):** S5 chữ đầu p50 / p95 (log harness); S6 USD / câu.
- **Âm theo luật trên** ⇒ phương án B của spec: code nối kết quả ngày vào lượt khi câu có từ chỉ ngày (không để model quyết gọi). Phương án B **đo lại cùng bộ**.

## 2. Cách tính âm lịch Việt Nam (UTC+7) — 2 cách, chọn (a)

E tra 08/11 (`data/tra_cuu_cli/2026-11-08_e-am-lich-python/`, Codex), rồi tự WebFetch kiểm 4 nguồn:
- PyPI JSON của `lunar-vn`;
- trang thuật toán Hồ Ngọc Đức;
- bài Tuổi Trẻ (đăng 16/07/2006 — Codex ghi sai ngày đăng);
- bảng Tết agereckoner.

| | (a) **`lunar-vn==1.4.0`** (khuyến nghị) | (b) Tự viết từ thuật toán Hồ Ngọc Đức |
|---|---|---|
| Là gì | gói PyPI cài lại thuật toán Hồ Ngọc Đức; `solar_to_lunar`, `lunar_to_solar`, `LunarDate` | ~150–200 dòng Python: điểm sóc + kinh độ mặt trời, `timeZone = 7.0` (trang gốc: "Để tính lịch Việt Nam, lấy timeZone = 7.0") |
| Kiểm được | MIT · **0 phụ thuộc** · Python 3.9–3.13 · mặc định UTC+7 · 1900–2100 · wheel 13 KB · phát hành 11/07/2026 · README ghi test roundtrip cả khoảng | trang gốc **không có giấy phép** cho code (chỉ "để tham khảo") ⇒ chỉ dùng công thức, tự viết; tác giả ghi bản rút gọn "độ chính xác thấp hơn" chương trình trực tuyến |
| Rủi ro | gói **nhỏ, ít người dùng** (15 sao, 1 người giữ) ⇒ E **đọc hết mã nguồn** trước khi thêm (13 KB); ghim đúng bản + hash trong `uv.lock` | tự gánh lỗi biên (giờ sóc sát nửa đêm — đúng ca Tết 2007), thêm code phải review |
| Khi nào đổi | đọc mã thấy vấn đề / test đối chiếu trượt ⇒ (b) | — |

**Chọn (a):** ít dòng phải giữ nhất mà đủ nhu cầu, đúng lịch Việt Nam. Thư viện nhỏ, cần cho việc đã duyệt ⇒ A tự duyệt (`Session_Prompt.md` §4).
- Không dùng `lunardate`, `LunarCalendar`, `cnlunar`, `lunar-python`, `sxtwl`: đều là lịch **Trung Quốc**.
- Cài không làm hỏng `.venv` chung (có `sherpa-onnx` chưa có trong lock): `uv add --no-sync lunar-vn==1.4.0`, rồi `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen`. Không `uv sync` thường.

**Test đối chiếu (0 USD, ≥ 10 ngày công khai):**
- Mỗi ngày có ≥ 1 nguồn **ngoài** dòng Hồ Ngọc Đức. Lý do: `lunar-vn` và bảng agereckoner cùng gốc Hồ Ngọc Đức nên chưa độc lập. Nguồn ngoài: báo / thông báo nghỉ Tết của Chính phủ.
- Tết Ất Sửu **1985**: Việt Nam 21/01, Trung Quốc 20/02 (spec — en.wikipedia, C kiểm; agereckoner khớp).
- Tết Đinh Hợi **2007**: Việt Nam 17/02, Trung Quốc 18/02 (Tuổi Trẻ, E kiểm 08/11).
- Tết **2026**: 17/02/2026, cộng 7+ Tết / rằm tháng Giêng / Vu Lan các năm gần, E kiểm nguồn trước khi ghi vào test.
- Thêm: roundtrip dương → âm → dương mỗi ngày 1950–2100; tháng nhuận 1984 / 1985 khác lịch Trung Quốc.

## 3. Công cụ + bộ đo

- **`backend/llm/ngay_lich.py` (mới):**
  - `hom_nay()` theo `zoneinfo("Asia/Ho_Chi_Minh")`;
  - `doi(ngay, thang, nam, loai: Literal["duong", "am"], nhuan: bool = False)`: kiểm khoảng (năm 1950–2100, tháng 1–12, ngày hợp lệ) — sai ⇒ câu cố định "ngày không hợp lệ";
  - chữ trả về do **code** dựng: "Thứ …, dd/mm/yyyy dương lịch — ngày d tháng m (nhuận) âm lịch".
  - Model chỉ gửi số + loại lịch, **không** tự đổi âm ↔ dương.
- **`assistant.py`:**
  - công cụ `ngay_lich` cho agent Huế, **chỉ đưa khi code dò thấy từ chỉ ngày** trong câu cuối hoặc câu hỏi liền trước (như `thoi_tiet.co_tu_khoa_luot`). Lý do: B5c — công cụ có mặt ở mọi lượt làm đổi cách model tìm;
  - ≤ 2 lần / câu (đếm trong closure, như `tim_kho`);
  - cờ `ngay_lich` trong `settings.yaml`, mặc định **tắt** ⇒ chuỗi gửi model giống byte (Q1 228 / 228).
- **Bộ đo (đã thấy, không kín — spec §12.4):**
  - ngày cũ 15 (12 câu quyết, `data/ngay_hien_tai_2026-10-30/questions.jsonl` md5 `722d7c92ae9e`);
  - mới 3 (`data/phase_9/bo_do_b1/ngay_moi_da_thay.jsonl`);
  - **~10 câu âm lịch mới E viết**: lễ hội ngày âm, "rằm / mùng một tháng tới", "Tết năm nay ngày mấy", 2 câu đối chứng có ngày rõ — loại câu người dùng thật hỏi, ghi trước khi chạy;
  - an toàn 32; Golden mẫu 30.
  - Đáp án ngày tính theo ngày chạy.
- **Test (0 USD):**
  - đối chiếu ngày (mục 2); kiểm khoảng / ngày sai;
  - cờ tắt ⇒ chuỗi giống byte; cờ bật ⇒ công cụ chỉ có khi câu có từ chỉ ngày;
  - lượt có công cụ: mỗi loại lượt (đầu, hỏi tiếp, có lịch sử) một test chuỗi gửi model (`WORKFLOW.md` §4c).
- **Cổng ổn định** như handoff; một lượt thật trước bộ test.

## 4. Tiền, file, chồng việc

- **Tiền ≈ 0,11 USD** (spec §12.7: (28 ngày + 32 an toàn + 30 Golden) × 2 × 0,0006), dừng ở 0,13. Pilot 5 câu trước, ước lại từ pilot.
- **File:** `backend/llm/ngay_lich.py` (mới), `backend/llm/assistant.py`, `backend/config/settings.yaml`, `pyproject.toml` + `uv.lock`, `backend/tests/test_ngay_lich.py` (mới); harness + bộ câu ở `data/phase_9/t1/` (private).
- **Chồng:** B (G: định tuyến + lời dặn — `assistant.py`), C (T3: thêm công cụ — `assistant.py`) ⇒ bên merge sau rebase.
- Báo A trước lượt đo tốc độ / lượt có phí lớn (máy dùng chung).
