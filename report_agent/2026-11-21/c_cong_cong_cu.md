# Bậc 5 — cổng đưa công cụ cho trợ lý: từ nguy hiểm thời tiết mới + khoá chế độ cổng (nhánh `p9-c-cong-cong-cu`)

Viết: 12:30 21/11/2026 (giờ `date`), phiên C. Giao: phiên điều phối (bậc 5 của đợt cải thiện harness). Trạng thái: **code + test xong, chờ review; chế độ "luôn đưa" CHƯA đo — mặc định không đổi.**

Từ dùng: *cổng* = phép kiểm bằng code quyết một lượt hỏi có được đưa công cụ thời tiết / ngày / khoảng cách cho model hay không · *lưới bão / lũ* = phép kiểm bằng code
coi một lượt là "câu nguy hiểm thời tiết" để luôn kèm câu chỉ tới bản tin chính thức + số 112 · *lưới cuối* = lần kiểm cuối ở route trước khi gửi kết quả.

## 1. Vì sao (số đếm trước khi sửa, 0 USD)

310 câu gõ khác nhau trong sổ vết, chạy lại đúng hàm cổng của code, người đọc gắn nhãn "cần công cụ nào": cổng bỏ sót 4 / 60 câu cần công cụ (thời tiết 3 / 17, ngày 1 / 13,
khoảng cách 0 / 30). Ba câu thời tiết bị sót đều là câu NGUY HIỂM thời tiết ("… có dông không", câu hỏi tiếp của nó, "nước sông … có lên cao không").
Chạy thật ba câu đó trên main `cf2d6d4a` × hai model: công cụ không được đưa 6 / 6, câu trả lời là câu từ chối 5 / 6; lưới cuối thêm câu bản tin chính thức + 112 ở 4 / 4 lượt có
"dông" nhưng 0 / 2 lượt "nước sông" — người hỏi về nước lũ nhận một câu từ chối trống.

## 2. Đổi gì

| File | Đổi gì |
|---|---|
| `backend/llm/thoi_tiet.py` | Thêm danh sách `_BAO_LU_THEM`: "dông" (trừ "dông dài" và lỗi gõ "Dông Ba"), "sấm sét / sấm chớp / sét đánh", "nước lên / nước dâng", "nước sông … lên / dâng". Dùng ở `la_cau_bao_lu_rong` (lưới bão / lũ) và `co_tu_khoa_luot_rong` (cổng đưa công cụ) ⇒ MỘT chỗ cho cả cổng lẫn hai lưới. |
| `backend/llm/assistant.py` | (a) Bỏ mẫu "dông" riêng của lưới cuối (`_DONG`): nay nằm trong danh sách chung, hết nhận nhầm "dông dài" / "Dông Ba". (b) Trường mới `cong_cong_cu` = `tu_khoa` (mặc định, như trước) hoặc `luon` (mọi lượt của tuyến trợ lý Huế đều đưa ba công cụ; giữ hai ngoại lệ: câu ngoài 7 ngày không đưa công cụ thời tiết, khoảng cách đã tính sẵn thì không đưa công cụ khoảng cách). (c) `from_settings` chọn khoá theo provider. |
| `backend/config/settings.yaml` · `core/settings_loader.py` | Khoá `assistant.cong_cong_cu` (đường OpenAI) và `full_corpus_generation.bedrock.cong_cong_cu` (đường Bedrock), cả hai đặt `tu_khoa`; giá trị lạ ⇒ lỗi lúc nạp. |
| `backend/tests/test_cong_cong_cu.py` (MỚI, 16 ca) · `test_phase6_settings.py` | Xem mục 3. |

**Lệch lời giao (đã báo phiên điều phối):** lời giao là "thêm hai cụm từ vào cổng đưa công cụ, không đổi gì khác". Bản đầu làm đúng vậy (commit `27ca99d`), nhưng khi đó "nước sông lên" chỉ mở
cổng công cụ còn hai lưới vẫn không nhận, và bộ dò của phiên B coi các câu này là câu nguy hiểm thời tiết ⇒ bản này đưa chúng vào danh sách nguy hiểm dùng chung.

## 3. Bằng chứng

`R` = `HF_HUB_OFFLINE=1 UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv run --no-sync`, chạy từ `backend/` của worktree.

| Kiểm | Lệnh | Kết quả |
|---|---|---|
| [máy kiểm] Test mới — hàm cổng thật, `_lich_extra` thật, agent dựng thật; bảng khoảng cách + hàm dự báo là đồ dựng | `R pytest tests/test_cong_cong_cu.py -q` | 16 đạt. Đã thấy ĐỎ: cùng file chạy với code của cây chính `cf2d6d4a` ⇒ lỗi ngay lúc nạp (chưa có `_luot_bao_lu` kiểu mới / trường `cong_cong_cu`). |
| [máy kiểm] File test chạm đường đổi, từng file | `R pytest tests/<file>.py -q` | `test_luoi_cuoi_bao` 10 · `test_b5b_thoi_tiet` 120 · `test_khoang_cach` 101 · `test_chat_stream` 25 · `test_api_chat` 14 đạt + 1 ca cần khoá OpenAI (C không nạp `.env`) |
| [máy kiểm] Đường OpenAI với cấu hình mặc định không đổi | script riêng tư chụp 10 lời gọi model (trả lời, biểu mẫu, trò chuyện, mục web, vòng công cụ, sửa lịch × 2, câu lịch, stream) | cùng mã băm `d71894d0e7265323` với main |
| [máy kiểm] Bộ dò của phiên B (46 câu, B soạn mù theo lời tả; `data/…/b_bo_do_cong_thoi_tiet.md`) chạy trên hàm thật | script riêng tư `do_bo_B.py` | main: cổng 13 / 20, lưới bão / lũ 9 / 20, lưới cuối 14 / 20 + nhận nhầm 2 / 20 ("dông dài", "Dông Ba"). Nhánh: cả ba chỗ **20 / 20, nhận nhầm 0 / 20**. ⚠ C viết mẫu SAU khi đã đọc bộ này ⇒ đây KHÔNG còn là số mù — cần một lượt câu đặt sau khi đọc code của người khác. |
| [máy kiểm] LƯỢT THẬT ba câu bị sót × luna, Sonnet high trên nhánh | script riêng tư `chay_3_cau.py` | công cụ được đưa 6 / 6 (model chọn loại bão / lũ 6 / 6), có khối dự báo 6 / 6, câu từ chối 0 / 6 (trước: 5 / 6); câu trả lời mở bằng "Mình không theo dõi được tin bão / lũ — bạn xem bản tin chính thức dưới đây" ở 4 / 6, hai lượt Sonnet tự viết lời "không khẳng định có hay không" kèm nguồn dự báo. |
| [chưa kiểm] Chế độ `luon` trên model thật (chọn công cụ, gọi thừa, an toàn, ngoài phạm vi, thời gian) | thước của phiên đo, cả hai model | chưa chạy — tiêu chí ghi trước ở file riêng tư `c_cong_tu_khoa/TIEU_CHI.md` |
| [chưa kiểm] Cả bộ test · lượt qua giao diện | để mốc | không chạy |

## 4. Giới hạn và điều người đo cần biết

- Bốn câu ranh giới của bộ dò lệch mong đợi của người soạn: "Mùa nào ở Huế hay có dông?" (câu khí hậu chung) và "… khi nước lên hay nước ròng" (câu lễ hội) NAY bị coi là câu nguy hiểm thời tiết ⇒ có thêm câu bản tin chính thức (thừa, không hại); "con nước lớn … có nguy hiểm không" KHÔNG được nhận; "xây kè chống nước dâng từ khi nào" đã bị nhận từ trước nhánh này.
- Danh sách thiên tai của mục web (`tra_web._THIEN_TAI`) KHÔNG đổi ở nhánh này: nó có "dông" nhưng chưa có "sấm sét", "nước sông lên".
- Chế độ `luon` làm số vòng tối đa của mọi lượt thành 6 (mỗi công cụ ngày / khoảng cách được đưa cộng một vòng) và tăng token vào mỗi lượt (mô tả công cụ khoảng cách mang cả danh sách mã điểm).
- Bộ đo dựng nhiều model trong một tiến trình: cờ phải dựng RIÊNG cho từng nhánh từ dict settings đã đổi provider (`AssistantFlags.from_settings`), nếu không cổng sẽ theo provider của file cấu hình.
- Dấu phiên bản của bộ nhớ câu trả lời (`api/app.py`) chưa gồm khoá `cong_cong_cu`; bộ nhớ nằm trong RAM và mất khi khởi động lại nên chưa gây sai.

## 5. Bảng bàn giao

| Đã làm | Chưa làm | Tự hoãn + lý do |
|---|---|---|
| Từ nguy hiểm thời tiết mới vào danh sách chung · khoá chế độ cổng theo provider · 16 test · lượt thật ba câu × hai model | Đo chế độ `luon` (phiên đo) · lượt câu đặt sau khi đọc code (người khác) · cả bộ test | Không sửa danh sách thiên tai của mục web và dấu phiên bản bộ nhớ: ngoài phạm vi nhánh, ghi ở mục 4 |

Cách thử 2 phút (sau khi gộp, bật server): gõ "Nước sông Hương mấy hôm nay có lên cao không?" ⇒ thấy câu chỉ tới bản tin chính thức + khối dự báo, không còn câu "không tìm thấy đủ thông tin" trống.
