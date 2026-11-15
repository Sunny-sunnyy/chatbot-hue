# Review plan NHÁP "so ảnh với ảnh mẫu" — C, 21:23 15/11/2026

Plan: `docs/superpowers/plans/2026-11-15-so-anh-embedding-plan.md` trên `origin/p10-so-anh` `dd11d3c`, sha256 đầu `7ed857519530` (đã kiểm). Căn cứ: plan + mục "Căn cứ để review" của nó + report 05/11 (`e9_siglip_implementation.md`). 0 USD, chỉ đọc. Không sửa plan.

**Kết luận: changes_requested — 0 blocker · 3 major · 6 minor.** Hướng thí nghiệm đúng (đổi model và đổi dữ liệu tách riêng, có tập ảnh âm, ngưỡng không nhìn bộ đo, tiền nhỏ, đường dữ liệu mới đã nêu). Ba chỗ phải sửa trước khi chạy đều thuộc "tiêu chí ghi trước có đọc được không".

## Major

**M-1 — Hai chỉ số QUYẾT đặt trên 25 ảnh không phân biệt được 22 với 20.**
- Bằng chứng: 22 / 25 có khoảng tin cậy 95 % khoảng 70–96 %; 20 / 25 khoảng 61–91 % — chồng nhau gần hết. Hơn kém 2 ảnh trên 25 ảnh là trong nhiễu. Ngoài ra 25 ảnh này đã được nhìn qua nhiều vòng (luna v0–v2 chỉnh trên nó; 05/11 có phần chẩn đoán trên chính bộ này) ⇒ mốc luna 22 / 25 và 21 / 25 là số lạc quan.
- Tác động: "thay luna" hay "bỏ" có thể do may rủi 1–2 ảnh.
- Tiêu chí đóng: (a) plan ghi thẳng giới hạn này; (b) chỉ số quyết tính trên **bộ gộp** (25 ảnh cũ + ảnh trong danh sách của bộ mới ⇒ nên ≥ 55 ảnh) và so **theo cặp** với luna v1 chạy trên đúng các ảnh đó; (c) luật đọc viết theo số ảnh hơn / kém theo cặp (ví dụ "thay" khi không kém luna quá 2 ảnh ở tên số 1 VÀ sàn từ chối đạt; "hơn luna" chỉ được nói khi hơn ≥ 6 ảnh), bộ cũ 25 ảnh báo riêng để nối với 05/11; (d) luna v1 chạy **2 lượt** trên bộ mới (05/11 luna đổi kết quả 12 / 33 ảnh giữa hai lượt) — thêm ≈ 0,02 USD.

**M-2 — Sàn "ảnh ngoài danh sách" đo trên 5 ảnh, và ảnh âm ↔ ảnh đo ngoài danh sách chưa được tách.**
- Bằng chứng: một model gán nhầm tên cho 20 % ảnh lạ vẫn qua sàn ≤ 1 / 5 với xác suất khoảng 74 % (30 % ⇒ 53 %). Plan chỉ chống trùng mẫu ↔ đo; không nói ảnh ÂM (dùng đặt ngưỡng) có được trùng nguồn / cảnh / tác giả với ảnh ngoài danh sách của bộ đo hay không.
- Tác động: ngưỡng từ chối là thứ quyết định model so ảnh có dùng được không (05/11 hỏng đúng ở đây: 5 / 5), mà phép đo của nó yếu nhất.
- Tiêu chí đóng: bộ mới có **≥ 15** ảnh ngoài danh sách (gộp với 5 ảnh cũ ⇒ ≥ 20; sàn ví dụ ≤ 2 / 20 — với mức nhầm thật 20 % chỉ còn khoảng 21 % cơ hội lọt); ghi rõ ảnh âm và ảnh đo ngoài danh sách khác nguồn tải, khác tác giả, và chạy cùng phép "cosine > 0,98" giữa hai tập; một nửa ảnh ngoài danh sách của bộ đo là loại DỄ NHẦM (công trình Á Đông nơi khác, món nước vùng khác), không chỉ ảnh linh tinh.

**M-3 — M0 ⇒ M1 đổi nhiều hơn một thứ; và thiếu phép thử rẻ nhất trước khi dựng dữ liệu.**
- Bằng chứng: M1 đổi cùng lúc bộ ảnh mẫu, ngưỡng từ ảnh âm, luật "cách tên đứng nhì", và có thể cả cách gộp điểm theo tên (plan viết "điểm cao nhất theo TÊN"; 05/11 là k-NN qua Qdrant — plan không nói có cùng cách gộp không). Số ảnh mẫu mỗi tên không đều (≥ 8 và ≥ 15) + lấy điểm cao nhất ⇒ tên nhiều ảnh mẫu có lợi thế.
- Tiêu chí đóng: (a) ghi rõ cách gộp điểm và dùng MỘT cách cho mọi biến thể kể cả M0 chạy lại; (b) mỗi biến thể báo hai dòng từ cùng bộ vector (0 USD): không luật từ chối ↔ có luật từ chối; (c) thêm bước đầu **"D2 trên 172 ảnh mẫu CŨ + bộ đo cũ"** (chỉ đổi model so với M0; ~20 phút, 0 USD, chỉ cần tải model) — ghi trước là phép dò, không dùng để quyết; nếu tên số 1 không hơn SigLIP (15 / 25) thì cả nhóm biết phần model không cứu được trước khi bỏ 1,5–2 giờ gom và nhìn ~800 ảnh.

## Minor
- **m-1 Bộ mới "người thường chụp":** User không có ảnh tự chụp ⇒ sửa mục 4 và 7.4. Nếu ảnh đo cũng lấy từ Commons như ảnh mẫu thì không còn là "người thường chụp" ⇒ lấy từ NGUỒN KHÁC (trang đánh giá / mạng ảnh du khách; dữ liệu công khai cho học tập). Ghi: ai gom, ai gắn nhãn, **người thứ hai kiểm 100 % nhãn**, và đóng băng bộ (danh sách + sha256) trước khi chạy bất kỳ model nào kể cả M1.
- **m-2 Luật "nhiều tên":** khi hệ thống đưa hai tên thì tính "tên số 1 đúng" thế nào — ghi trước (đề nghị: tính là KHÔNG đúng ở chỉ số tên số 1, đúng ở chỉ số top 3; báo riêng số ảnh rơi vào "nhiều tên").
- **m-3 Ngưỡng:** thêm luật khi ngưỡng "≤ 5 % ảnh âm lọt" làm rơi quá nhiều ảnh mẫu (ví dụ > 20 % ⇒ ghi biến thể đó không đặt được ngưỡng dùng được, không nới ngưỡng).
- **m-4 Chống gần trùng:** 0,98 là số tự đặt và tính bằng chính model đang đo ⇒ thêm một lượt nhìn tay: với mỗi ảnh đo, xem ảnh mẫu giống nhất (30–40 cặp, vài phút).
- **m-5 Luật "thay luna" chưa có tốc độ / RAM:** model chạy máy thêm khoảng 1,6 GB vào tiến trình server ⇒ ghi mức chấp nhận (hoặc ghi rõ "quyết ở plan đưa vào chatbot").
- **m-6 Biến thể G:** ghi sẵn tuỳ chọn không lưu dữ liệu ở provider trong lời gọi (như thí nghiệm embedding chữ 30/10 đã đặt `data_collection: deny`).

## Cắt được gì (over-engineer)
- **D2p** (trung bình patch): bỏ khỏi lượt đầu; chỉ chạy khi D2 thiếu đúng 1–2 ảnh so với luật quyết — ghi điều kiện đó.
- **M0 chạy lại:** chỉ cần nếu đổi cách gộp điểm (M-3a); cùng cách thì dùng số 05/11.
- **Cỡ bộ mẫu ~700:** 42 tên × 8 ≈ 340 + nhóm hay nhầm ⇒ khoảng 450 là đủ cho lượt đầu; phần "một người nhìn 100 % ảnh mẫu" GIỮ (05/11 chưa ai xem).
- Giữ nguyên: tập ảnh âm, D2, D3, G (User hỏi đích danh ba model), so bằng numpy không dựng collection mới.

## Đã kiểm thấy ổn
Tiêu chí có ghi trước và phần lớn đo được · ngưỡng chọn trên ảnh mẫu + ảnh âm, không nhìn bộ đo · D2 / D3 / G mỗi cái chỉ đổi model so với M1 · tiền ≈ 0,1–0,15 USD, trần 0,5, có điểm dừng 0,3 · đường dữ liệu mới (ảnh ⇒ OpenRouter ⇒ Google) và việc User phải tự chấp nhận điều khoản DINOv3 đã nêu · giới hạn của số công bố (bảng so các bản rất lớn, không phải cỡ B) plan đã tự nói thẳng · một model một lúc trên máy 19 GB.

---

# Vòng 2 — C, 21:36 15/11/2026

Plan bản 2: `origin/p10-so-anh` `f57b981`, sha256 đầu `3b9a1894a195` (đã kiểm). 0 USD, chỉ đọc.

**Kết luận: ready_for_user_confirmation — 0 blocker · 0 major · 5 minor** (sửa lúc viết file ngưỡng, không cần vòng 3).

**Ba major vòng 1 đã đóng:** M-1 — mọi chỉ số quyết tính trên bộ gộp (≥ 55 ảnh trong danh sách), so theo cặp với luna lượt 1, luna chạy 2 lượt, giới hạn của 25 ảnh cũ được nói thẳng. M-2 — ≥ 20 ảnh ngoài danh sách, sàn ≤ 2 / 20, ba tập tách nguồn + tác giả + kiểm gần trùng + nhìn tay. M-3 — một cách gộp điểm, mỗi biến thể hai dòng (không / có luật), mọi biến thể chỉ đổi model, phép dò đã chạy trước khi gom dữ liệu. Sáu minor vòng 1 đều có trong bản 2.

## Minor (chỗ B nhờ soi: luật chọn m, t và Quyết 1)
- **m-1 Quyết 1 dùng số tuyệt đối "≤ 2 ảnh sai":** phủ 50 % (~28 ảnh) hay phủ 90 % (~50 ảnh) đều cùng trần 2 ⇒ biến thể phủ rộng bị phạt. Ghi theo tỉ lệ có làm tròn (ví dụ ≤ 2 khi nhóm tự tin < 40 ảnh, ≤ 3 khi ≥ 40). Và nói thẳng giới hạn: 2 sai / 28 ảnh vẫn tương thích với tỉ lệ sai thật tới khoảng 23 % — đây là loại lỗi "trả lời thẳng sai nơi", nên thêm một dòng đối chiếu miễn phí: trên đúng các ảnh đó, nhóm "luna trả đúng một tên" sai bao nhiêu (đã có từ 2 lượt luna).
- **m-2 Luật chọn m, t — hai chỗ chữ mơ hồ:** (a) "t = mức mà ≤ 5 % ảnh âm không bị từ chối trong số ảnh không tự tin" — ghi rõ mẫu số (5 % của MỌI ảnh âm hay của ảnh âm không tự tin); (b) câu "> 20 % ảnh mẫu bị xử sai (ảnh mẫu bị từ chối, hoặc < 30 % ảnh mẫu được tự tin)" gộp hai điều kiện khác nhau ⇒ tách thành hai dòng.
- **m-3 Mức "< 30 % ảnh mẫu tự tin" lệch với Quyết 1 "phủ ≥ 50 %":** số trên ảnh mẫu (bỏ-một-ra, ảnh cùng tên thường cùng người chụp) lạc quan hơn bộ đo ⇒ biến thể chỉ đạt 30–50 % trên mẫu gần như chắc trượt Quyết 1. Nâng mức kiểm sớm lên 50 % hoặc ghi rõ đây chỉ là mức "vô vọng", không phải dự báo đạt.
- **m-4 "≤ 5 % ảnh âm" đo trên ~100 ảnh:** 5 / 100 có khoảng tin cậy rộng; nếu tỉ lệ thật khoảng 8 % thì sàn ≤ 2 / 20 trượt với xác suất khoảng 21 %. Hoặc chọn m ở mức ≤ 3 % ảnh âm, hoặc chấp nhận và ghi trước rằng trượt sàn 3 / 20 là "sát ngưỡng, không kết luận".
- **m-5 Ảnh ngoài danh sách rơi vào "nhiều tên":** sàn chỉ đếm ảnh ngoài danh sách được "tự tin một tên"; ảnh lạ được đưa top 3 không bị đếm. Chấp nhận được trong luồng lai (người dùng chọn / bấm "không phải"), nhưng báo riêng số này ở dòng theo dõi.

Đã thấy ổn thêm ở bản 2: hướng đọc đổi sang "embedding làm cổng" khớp số phép dò (khoảng cách tên nhất − nhì có tín hiệu, điểm tuyệt đối thì không); tốc độ / RAM đẩy sang plan đưa vào chatbot có ghi số dò; phân vai gom / kiểm / chạy; tiền ≈ 0,12 USD, trần 0,5.
