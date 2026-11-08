# Plan — T1 ngày + âm lịch (spec Phase 9 bản 13 §12, sha `5557f0fd7650`)

Người viết: E.
- Bản 1: 11:03 08/11/2026. Review độc lập vòng 1: `changes_requested` 0 / 5 / 6 (`…_plan_review.md`).
- **Bản 2: 11:21 08/11/2026** — sửa M-1–M-5 + minor; đổi sang **mức nhẹ** (User duyệt 08/11, `Session_Prompt.md` §7: ≤ 0,2 USD, không đổi kiến trúc ⇒ A đọc rồi duyệt, đo 1 lượt, an toàn 2 lượt, 1 review cả nhánh, không bộ kín).
- Nhánh `p9-t1-ngay` (`0357d80`, worktree `/tmp/e_t1`): đã có phần 0 USD (mục 3).

## 1. Vấn đề, mốc, tiêu chí (ghi trước)

**Vấn đề:** câu "hôm nay / tối nay / tuần này / rằm năm nay" bị từ chối nhầm vì model không biết ngày.
- Lượt 30/10: 6 / 12 câu quyết bị từ chối.
- Dòng ngày trong tin nhắn (B1 P2, `today_line`) không đỡ.

**Chỉ chạy câu mà bộ dò bật** (A quyết, review M-1). Câu không bật có chuỗi gửi model giống byte giữa mốc và nhánh — test + Q1 đã chứng minh (mục 3).

**Mốc:** server `main` (cờ `ngay_lich` tắt) ↔ server nhánh (cờ bật), cùng giờ, qua `/api/chat/stream` thật, mỗi câu một cuộc mới. Mỗi bên **1 lượt**; bộ an toàn **2 lượt**.

**Đạt khi đủ cả 6:**
1. **Từ chối nhầm giảm ≥ 3 câu** trên bộ ngày (mục 2). Chỉ tính câu chuyển từ `INSUFFICIENT_ANSWER` sang trả lời mà câu mới được **sub-agent ngữ cảnh mới chấm mù là OK** (không L1 giả định ngày / kết luận không điều kiện, không L3 sai kho — nhãn `data/ngay_hien_tai_2026-10-30/plan_nhap.md` §2) (review M-5).
2. **0 câu L1 / L3 mới** trong bộ ngày (sub-agent đọc mọi câu nhánh khác mốc).
3. **0 ngày / thứ sai trong chữ trả lời** (L2) ở **mọi** câu nhánh đã chạy. Code kiểm 3 luật tất định:
   - (a) "thứ …" đi cùng một ngày dương trong cùng câu ⇒ khớp lịch;
   - (b) cặp dương ↔ âm trong cùng câu ⇒ khớp `ngay_lich.doi`;
   - (c) "hôm nay / ngày mai / tối nay là …" ⇒ khớp ngày chạy theo giờ Việt Nam **của từng câu**.

   Mẫu bắt gồm "Chủ nhật", "tháng Giêng / Chạp", "ngày … âm lịch". Ngày lấy từ kho (ngày âm lễ hội, năm lịch sử) không so với ngày chạy. Câu bị đánh dấu ⇒ sub-agent đọc. Giới hạn: đáp án dùng cùng thư viện, nhưng thư viện đã qua bộ đối chiếu (mục 3).
4. **0 lượt chạm `max_turns`** ở nhánh (đếm `outcome`) (review M-3).
5. **S1:** 4 câu an toàn bộ dò bật × 2 lượt × 2 bên: đủ 4 số (thủ tục S-AT khi chênh 1). 28 câu an toàn còn lại: chuỗi giống byte ⇒ không đổi.
6. **S4:** 2 câu Golden mẫu 30 bộ dò bật (`93`, `137`): chấm mù cặp mốc ↔ nhánh, không tụt. 28 câu còn lại giống byte.

**Câu chỉ đổi kết quả ở một trong hai lượt an toàn ⇒ không tính** (review M-5).

**S5 / S6 (A, review m-5):**
- S6 ≤ 0,0005 USD / câu là sàn trên Golden mẫu như T3 — chỉ 2 câu đổi.
- Lượt có công cụ (thêm một vòng model) báo **riêng**: USD / câu và chữ đầu p50 / p95 từ `chat_metrics.first_text_ms`, nhánh ↔ mốc trên bộ ngày (n = 27 mỗi bên).
- S5: so sàn spec (p50 ≤ 3 s / p95 ≤ 5 s) và "không chậm hơn mốc quá nhiễu". Báo A trước khi chạy (máy dùng chung).

**Âm ⇒ phương án B** (spec §12.2): code nối kết quả ngày vào lượt khi có từ chỉ ngày. Đo lại cùng bộ.

## 2. Bộ đo (đã thấy, không kín)

- **Bộ ngày 28 câu, bộ dò bật 27:**
  - 15 câu cũ (`data/ngay_hien_tai_2026-10-30/questions.jsonl`, md5 `722d7c92ae9e`; 12 câu quyết): bật 14. **U1** không bật có chủ ý — hỏi lịch cố định "những tối nào", không phải ngày tương đối;
  - 3 câu mới (`data/phase_9/bo_do_b1/ngay_moi_da_thay.jsonl`): bật 3;
  - **10 câu âm lịch mới** E viết `data/phase_9/t1/bo_am_lich.jsonl` (sha256 `30f16e5a329d`; nhãn ghi trước: `in_kho`, `loai`, luật đáp án theo ngày chạy): bật 10. Gồm 6 câu lễ hội ngày âm có trong kho (Hội vật làng Sình, Thủ Lễ, Cầu ngư, Quán Thế Âm, Thu tế Huệ Nam, chợ quê Thanh Toàn), rằm / Tết / hôm nay âm / "thứ 7 tuần sau".
- **An toàn 32:** bật 4 (S01, S02, S03, S12). **Golden mẫu 30:** bật 2. (Golden 176: bật 9 / 176 — tham khảo.) Đếm bằng `data/phase_9/t1/tools/dem_bo_do.py` (0 USD).
- **Bộ dò** (`ngay_lich._TU_NGAY`, review M-4):
  - các cụm: hôm nay · bữa nay · hôm qua · sáng / trưa / chiều / tối / đêm nay · bây giờ · lúc này · hiện giờ · sắp tới · ngày mai · sáng / trưa / chiều / tối mai · ngày kia · tuần này / sau / tới / trước · cuối tuần · tháng này / sau / tới / trước · năm nay / sau / tới / ngoái · thứ hai…bảy / 2–7 · chủ nhật · rằm · mùng / mồng · âm / dương lịch · lịch âm / dương · tết · dạng "dd/mm";
  - xét câu cuối **hoặc câu hỏi liền trước**;
  - **không** tính "khi nào / bao giờ / ngày nào" (câu lịch sử "xây khi nào" sẽ nhận công cụ không cần).

## 3. Phần 0 USD đã làm trên nhánh (bằng chứng ở report)

- **Thư viện `lunar-vn==1.4.0`.** A duyệt **11:06 08/11** trước khi E cài, theo §4 (review m-6). Lý do:
  - nhỏ, MIT, 0 phụ thuộc, lịch Việt Nam UTC+7;
  - **không phổ biến** (gói mới, 1 tác giả) ⇒ bù bằng việc E tải wheel từ PyPI, đọc hết ~700 dòng (chỉ thư viện chuẩn: không mạng / file / lệnh), và ghim hash `c42506ee…` (= `uv.lock`);
  - cài vào `.venv` chung bằng `uv add --no-sync` + `uv sync --inexact --frozen` (dry-run: chỉ thêm 1 gói, `sherpa-onnx` còn).
  - **Lưu ý cho mọi session:** `uv sync` thường ở `main` sẽ gỡ `lunar-vn` + `sherpa-onnx` — chỉ dùng `--inexact`.
- **Đối chiếu (review m-3):**
  - `lunar-vn` ↔ bảng tính sẵn của Hồ Ngọc Đức 1901–2099: **khớp mọi năm 1966–2099**, lệch 1 ngày ở 4 năm trước 1966 (3 / 4 khớp khi tính UTC+8 = lịch xưa) ⇒ công cụ chỉ nhận **1976–2100** (trước đó hai miền khác lịch: Tết Mậu Thân 1968 Bắc 29/01, Nam — có Huế — 30/01).
  - Test ≥ 10 ngày, nguồn ngoài dòng Hồ Ngọc Đức: 11 ngày Tết (1985, 2007, 2020–2027, 2030) — bảng "Ngày đầu năm theo Con giáp" của vi.wikipedia (UTC+7, mở 08/11); 2007 thêm Tuổi Trẻ (16/07/2006, VN 17/02 ↔ TQ 18/02).
  - Năm VN ≠ TQ: 1985 và 2007 — cùng thuật toán ở UTC+8 ra ngày của Trung Quốc.
  - Đổi qua đổi lại 1976–2100 chỉ là kiểm phụ.
- **Công cụ** `ngay_lich(loai: "hom_nay" | "duong" | "am", ngay, thang, nam, thang_nhuan)` (review M-3):
  - mọi kết quả **luôn kèm dòng hôm nay** (dương + âm + thứ + can chi) ⇒ câu "tháng tới / năm nay" chỉ cần 1 lần gọi; `nam = 0` = năm nay;
  - tối đa 2 lần / câu;
  - ngày không có (30 ở tháng thiếu, nhuận sai, 31/4) ⇒ câu cố định;
  - **kết quả là một nguồn trong sổ nguồn** như `thoi_tiet` (review M-2), test: câu chỉ trích nguồn ngày qua kiểm citation;
  - không báo "đang tìm kho" khi gọi công cụ này (review m-2); dùng lại bảng tên thứ `_WEEKDAYS`.
  - Vòng model của lượt ngày phức tạp: ngày → (tìm thêm) → viết = 3 ≤ `max_turns` 4.
- **Test 38 passed** — 4c (review m-1): lượt đầu / lượt có lịch sử / cờ tắt × không stream + stream; lượt biểu mẫu không dùng đường công cụ. **Q1 cờ tắt: 228 / 228 giống byte `main`.**

## 4. Tiền, file, chồng việc

- **Tiền (1 lượt, review M-1):**
  - bộ ngày 27 × 2 bên × ~0,0009 ≈ 0,049;
  - an toàn 4 × 2 lượt × 2 bên × 0,0008 ≈ 0,013;
  - Golden 2 × 2 × 0,0008 ≈ 0,003;
  - pilot 5 câu ≈ 0,005;
  - dự trữ S-AT 6 × 0,0008 ≈ 0,005;
  - ⇒ **≈ 0,075 USD, dừng ở 0,10** (dưới dòng §12.7 ≈ 0,11; trong trần Phase 9).
- **File:**
  - mã: `backend/llm/ngay_lich.py` (mới), `assistant.py`, `generator_openai_full_corpus.py`, `full_corpus_prompt.py` (`NGAY_LICH_MO_TA`), `settings.yaml` (`ngay_lich: false`), `pyproject.toml` + `uv.lock`, `tests/test_ngay_lich.py`;
  - harness + bộ ở `data/phase_9/t1/` (private).
- **Chồng:** B (G — định tuyến + lời dặn `assistant.py`), C (T3 — thêm công cụ `assistant.py` / generator) ⇒ bên merge sau rebase.
