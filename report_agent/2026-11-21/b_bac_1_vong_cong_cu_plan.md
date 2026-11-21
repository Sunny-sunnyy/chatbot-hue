# Bậc 1 của đợt cải thiện trợ lý — vòng công cụ (plan một trang)

Viết: 11:37 21/11/2026 (giờ `date`), phiên B. Người duyệt: phiên điều phối. Bảng thứ tự cả đợt: bản chốt riêng tư của phiên điều phối (`data/…/harness/CHOT_DOT_CAI_THIEN.md`).
Từ dùng: *vòng* = một lần gọi model trong một lượt hỏi · *chạm trần vòng* = hết số vòng cho phép mà model chưa viết câu trả lời ⇒ người dùng nhận câu từ chối cố định ·
*thước* = bộ đo agent của phiên đo (chạy trên cả gpt-6-luna lẫn Claude Sonnet 5.5 mức high, mỗi bậc hai lượt để biết nhiễu) · *bản 0* = bản chính sau khi gộp nhánh `p9-b-loi-dan-sonnet`.

## 1. Hiện trạng (đọc code bản chính)

- Trần vòng: `ASSISTANT_MAX_TURNS = 4` (`backend/llm/generator_openai_full_corpus.py`), +1 khi lượt có công cụ ngày, +1 khi có công cụ khoảng cách. Chạm trần ⇒ `on_max_turns` trả câu từ chối cố định.
- Trần tìm kho: `MODEL_SEARCH_LIMIT = 2` (`backend/llm/assistant.py`). Hết hai lần ⇒ công cụ `tim_kho` bị ẨN ở vòng kế (cờ `het_luot_bo_cong_cu`, đang bật) để model phải viết.
  Bốn công cụ còn lại không có cơ chế ẩn: lần gọi thừa chỉ nhận một dòng chữ ("Đã lấy dự báo…").
- Hạn giờ: cả lượt 45 giây; định tuyến và lời gọi hiểu ý sửa lịch dùng chung `assistant.router_timeout_seconds` = 10 giây.
- Số đã có: sau bản sửa "khuôn + công cụ", người viết đo Sonnet chạm trần 0 / 24 (high) và 0 / 16 (low); lời gọi trùng y nguyên 1 / 40 lượt; luna ở lượt gốc của phiên đo 0 / 15.
  Lời gọi hiểu ý sửa lịch ở high lâu nhất 7,1 giây.

## 2. Đề nghị: ba phần, mỗi phần có CỔNG — số bản 0 không đòi thì không làm

| Phần | Đổi gì | Chỉ làm khi (đọc từ bảng thước bản 0) |
|---|---|---|
| 1a. Vòng cuối chỉ viết | Vòng cuối cùng của lượt gửi KHÔNG kèm công cụ nào ⇒ model viết từ bằng chứng đã có (hoặc tự trả câu từ chối theo lời dặn) thay vì hết vòng. Dùng lại đúng cơ chế đang ẩn `tim_kho` (`is_enabled` trong `_assistant_for`): thêm điều kiện "số lần gọi model đã xong < trần − 1" cho MỌI công cụ. Model vẫn xin công cụ đã ẩn ⇒ câu từ chối cố định như hôm nay (nới `xin_cong_cu_da_an`), không thành lỗi. Một cờ mới `assistant.vong_cuoi_chi_viet`, mặc định TẮT; tắt ⇒ chuỗi gửi model giống từng byte. | có ≥ 1 lượt chạm trần vòng ở một trong hai model (cột "chạm trần vòng — 29 câu", "bốn câu × 3", "chuỗi — chạm trần vòng") |
| 1a'. Không chạy lại lời gọi trùng | Cùng công cụ + cùng tham số lần hai trong một lượt ⇒ code không chạy lại, trả một dòng "kết quả đã có ở trên". Một hàm bọc chung cho năm công cụ ở `assistant.py`. | cột "lời gọi công cụ TRÙNG y nguyên / câu" > 0,05 ở một trong hai model. Dự đoán của người viết: KHÔNG đạt cổng (1 / 40) ⇒ bỏ. |
| 1b. Tham số hoá để đo nới | Hai hằng thành khoá cấu hình đọc từ dict settings, giá trị mặc định GIỮ NGUYÊN: `assistant.so_vong_cong_cu: 4`, `assistant.so_lan_tim_kho: 2` (phiên đo đổi trong bản chép dict để đo 4 ↔ 6 vòng, 2 ↔ 3 lần tìm; không đổi mặc định ở nhánh này). Hạn giờ lời gọi hiểu ý sửa lịch: tách khỏi hạn định tuyến bằng khoá `bedrock.sua_lich_timeout_seconds` (đường OpenAI vẫn dùng 10 giây chung). | ĐÃ LÀM trên nhánh này (11:46 21/11/2026): ba khoá có trong `settings.yaml` với đúng giá trị cũ (4 · 2 · 10 giây), đọc từ dict settings lúc dựng generator / cờ; loader kiểm khoá hạn giờ. Đổi GIÁ TRỊ hạn giờ: khi bảng thước có ≥ 1 lượt sửa lịch chạm hạn 10 giây, hoặc lần lâu nhất ≥ 8 giây. |

Áp cho cả hai model: 1a, 1a', hai hằng của 1b là code chung, bật / đổi bằng cấu hình ⇒ phiên đo chạy thước cùng buổi trên luna và Sonnet; bên nào tốt hơn thì bật cho bên đó (cờ đọc theo provider nếu hai bên ra khác nhau).

## 3. Tiêu chí ghi TRƯỚC (cột của bảng thước; so với bản 0 cùng buổi, nhiễu = chênh giữa hai lượt bản 0)

- **Phải được (1a):** mọi cột chạm trần vòng về 0 ở model có lỗi; các lượt vừa được "cứu" do người thứ hai đọc tay: câu trả lời chỉ dùng bằng chứng đã có trong lượt.
- **Sàn, không được xấu đi:** "an toàn 10 — ngoài kho bị trả lời" vẫn rỗng · "ngoài phạm vi 10" không đổi · "chuỗi — hỏi tiếp ngoài kho KHÔNG ra câu từ chối khuôn" không tăng · "lỗi kỹ thuật" rỗng · "gọi thừa công cụ cấm" rỗng.
- **Không tụt quá nhiễu:** ba dòng "đạt máy" (công cụ, rìa Huế, câu ghép) và "chuỗi — phải trả lời mà bị từ chối".
- **1b (do phiên đo quyết sau khi có số):** nới chỉ được giữ khi "đạt máy — câu ghép" hoặc "chuỗi — bị từ chối" tốt hơn quá nhiễu MÀ các dòng sàn ở trên không đổi; thời gian và số lời gọi model / câu chỉ ghi lại.
- Một dòng sàn xấu đi ⇒ gỡ đúng phần đó, không vòng hai.

## 4. Rủi ro

- **Sàn "câu ngoài kho không được trả lời bằng kho" (1a):** vòng cuối không còn đường tìm thêm ⇒ model có thể viết từ bằng chứng chưa đủ thay vì từ chối. Lời dặn đã bắt từ chối khi thiếu bằng chứng; đo bằng ba dòng sàn ở mục 3 + đọc tay các lượt được cứu.
- **Mất một vòng công cụ (1a):** hôm nay vòng thứ 4 vẫn được gọi công cụ nhưng kết quả của nó không bao giờ được dùng (hết vòng) ⇒ thực tế không mất gì; test khẳng định.
- **Nới số vòng (1b):** lượt dài hơn ⇒ dễ chạm hạn 45 giây; phiên đo ghi cột thời gian lớn nhất.

## 5. Kiểm trước khi xin review (vừa đủ)

Cờ tắt ⇒ thân gửi model giống byte (script chụp 10 lời gọi của phiên review) · cờ bật: model dựng sẵn cứ gọi công cụ ⇒ vòng cuối không có công cụ trong thân gửi và lượt trả câu trả lời, không phải "hết vòng" — một ca cho mỗi kiểu lượt (lượt đầu, lượt có lịch sử, đường stream) · model xin công cụ đã ẩn ⇒ câu từ chối cố định, không lỗi 500 ·
khoá cấu hình mới thiếu / sai kiểu ⇒ loader báo lỗi nêu tên khoá · một lượt thật mỗi model trên một câu từng chạm trần. Không chạy cả bộ test (để mốc).

## 6. Không làm ở bậc này

Viết lại mô tả công cụ và chữ trạng thái trong kết quả công cụ (bậc 3, 4) · trả lại khối suy luận (bậc 2) · gọi song song nhiều công cụ · đổi lời dặn.
