# Đề bài review độc lập — <việc cần soi> (<tên dự án>, bản `<mã commit>`)

Soạn <giờ lấy bằng `date`> bởi <ai>. Người gửi file này cho bạn là chủ dự án. Bạn là **người review khác hãng**: bạn không viết dòng code nào ở đây. Người soạn
đưa cho bạn MỌI thứ quan trọng mình đang nắm về dự án (mục 1) — kể cả những gì nhóm đã tìm ra, ghi dưới nhãn "đã biết": đừng báo lại, hãy đi xa hơn — nhưng
nếu bạn thấy một điểm "đã biết" SAI, sai nguyên nhân, hoặc nặng hơn nhóm nghĩ thì nói thẳng, đó là thứ có giá.
Thứ chủ dự án cần ở bạn là kết quả CHẤT LƯỢNG, không phải kết quả nhanh.

## 1. Bối cảnh (đủ để bắt đầu; muốn sâu hơn: danh sách "Nên đọc")
- Thư mục làm việc: <gốc repo>, nhánh <…>, commit `<…>`. Sản phẩm là gì, dựng bằng gì, code ở đâu — 3–5 dòng.
- Điều vừa thay đổi / phạm vi cần soi — 3–5 dòng.
- Bản đồ để đọc code: <file nào tả từng tính năng> · bẫy đã biết (đừng báo lại như phát hiện mới): <file nào>.
- **Nên đọc** (chủ dự án 22/11/2026: "các file .md, các file folder code cần đọc, ... và để các model AI của hãng khác tự do khám phá") — danh sách MỞ, mỗi dòng
  kèm một câu "đọc để biết gì"; ngoài danh sách này bạn TỰ DO khám phá cả repo — trừ những thứ mục 3 cấm mở: tài liệu `.md` <trang hiện trạng · sổ việc đang mở · giới hạn đã biết / runbook ·
  tài liệu giảng giải hệ thống · danh sách ý đã thử và đã bỏ · luật của dự án> · thư mục và file code <…> · bộ test liên quan <…> · file đo <…> (log có chữ người dùng gõ: không).
- **Trạng thái lúc gửi** (chủ dự án dặn 22/11/2026 — mục này luôn có, viết ĐỦ chứ không viết ngắn): đang chạy bản nào, thứ gì đang bật / tắt, model nào, số đo
  mới nhất kèm đường dẫn file đo · ai dùng sản phẩm và "tốt" được đo bằng gì · đã thử những gì và ra sao, kể cả thứ đo rồi bỏ (để bạn không đề xuất lại) · quyết định
  chủ dự án đã chốt và sàn không được nới · việc đang làm dở · từ riêng của dự án kèm nghĩa. Thứ gì không chép vào đây được thì trỏ đúng file trong repo; file đo
  nằm ở thư mục riêng (ngoài repo, mục 3 đang cấm mở) ⇒ hoặc chép CON SỐ vào đây, hoặc liệt kê ở mục 3 đúng các đường dẫn được mở. Lỗi / điểm nhóm ĐÃ TÌM RA trong
  đúng phạm vi đang hỏi cũng ghi ở đây dưới nhãn "đã biết — đừng báo lại" (người soạn nắm gì thì bạn cũng nắm).

## 2. Việc của bạn
<Một câu hỏi rõ.> Ví dụ: "Tìm chỗ HAI tính năng gặp nhau mà bộ test hiện có không bắt được." Không chấm phong cách, không đề nghị dọn code.
Ưu tiên theo hậu quả với người dùng: <thứ tự lỗi của dự án, nặng → nhẹ>.
Gợi ý chỗ soi (không giới hạn): <3–6 gợi ý>. File chính: <danh sách>.

**Dùng hết khả năng của bạn** (chủ dự án dặn 22/11/2026 — dòng này luôn có trong đề bài): bạn được và NÊN dùng mọi công cụ mạnh nhất mình có để làm việc
này tốt nhất và toàn diện nhất — agent con chạy song song, chế độ nghiên cứu chuyên sâu (deep research), tìm web nhiều vòng, đọc rộng, tự kiểm chéo kết quả
của chính mình trước khi viết — miễn ở trong ranh giới mục 3. Không cần làm nhanh; cần làm kỹ. Cuối file kết quả ghi bạn đã dùng những gì (bao nhiêu agent
con, bao nhiêu vòng tìm, mở bao nhiêu trang).

## 3. Ranh giới (bắt buộc)
- **Chỉ đọc.** Không sửa file nào của repo, không commit, không đẩy, không cài gói. File DUY NHẤT bạn được ghi là file kết quả ở mục 4.
- **Không mở, không in** (kể cả khi "tự do khám phá" — thư mục làm việc có cả thứ git không theo dõi): file khoá (`.env`…); bộ câu giữ kín / đáp án chấm <đường dẫn,
  mẫu tên file>; <thư mục dữ liệu riêng> — trừ đúng các đường dẫn đã liệt kê ở mục 1. Tìm chữ thì loại các đường dẫn cấm; lệnh tìm an toàn của dự án: <…>
  (một lệnh tìm đệ quy trên cả thư mục sẽ in ra cả nội dung cấm).
- Không gọi API trả phí, không bật server. Được chạy lệnh đọc (`git log`, `git show`, tìm chữ). **Cách chạy thử một hàm:** <ghi đúng lệnh của dự án, chép–dán chạy được> —
  hoặc nói thẳng: "chỉ đọc code là đủ; mọi điểm ghi nhãn [chỉ đọc code]". (Không ghi cách chạy thì reviewer sẽ không chạy gì.)
  Ví dụ ở repo gốc (theo lần dùng thật 18/11, do phiên soạn gói ghi lại — người soạn gói sau tự thử lại trước khi chép): công cụ có sẵn `uv` trong hộp cát (Codex)
  chạy được hàm thật từ thư mục `backend/` bằng `HF_HUB_OFFLINE=1 UV_OFFLINE=1 uv run --no-sync --no-cache python - <<'PY' … PY`; công cụ không có `uv`
  (Antigravity) thì chỉ đọc code ⇒ mọi điểm gắn nhãn [chỉ đọc code], người nhận sẽ tái hiện.
- Không chép dữ liệu riêng vào kết quả.

## 4. Kết quả — ghi vào `<đường dẫn>/KET_QUA_<tên model>.md`
1. Dòng đầu: tên model + mức suy luận + giờ bắt đầu / kết thúc (lấy bằng lệnh `date`).
2. Bảng phát hiện, nặng → nhẹ: # · chỗ nào (`file:dòng`) · đầu vào nào ⇒ ra gì (cụ thể) · **ca đối chứng nào KHÔNG bị** (đầu vào gần giống mà kết quả đúng) · bằng chứng gắn nhãn **[đã chạy]** (kèm lệnh + đầu ra) hoặc
   **[chỉ đọc code]** · vì sao test hiện có không bắt · mức (người dùng thấy / lệch log-tiền / chỉ lý thuyết) · đề nghị (ghi giới hạn / sửa nhỏ / cần đo).
3. Mục "Đã soi, thấy ổn" — mỗi dòng trỏ test đang khoá.
4. Mục "**CHƯA đọc gì / chưa kiểm gì**" — khai thật; file nào chỉ lướt thì ghi là lướt.
5. Kết luận nặng ("nghiêm trọng", "chắc chắn") phải kèm lệnh + đầu ra, hoặc ghi rõ "nghi, chưa chứng minh".

## 5. Cách dùng kết quả (để bạn biết mình được chấm thế nào)
Điểm bạn báo được so với danh sách "đã biết" ở mục 1: báo lại điểm đã biết không được tính; có giá là (a) điểm MỚI, (b) chỗ bạn chứng minh một điểm "đã biết" sai,
sai nguyên nhân, hoặc nặng hơn nhóm nghĩ; mỗi điểm như vậy sẽ được chạy lại để xác nhận. (Đề bài MÙ — không đưa danh sách của nhóm: danh sách của bạn được so với
danh sách của một reviewer cùng hãng với người viết: điểm nào trùng, điểm nào chỉ bạn thấy.) Phát hiện ít mà đúng có giá hơn nhiều mà đoán.
Người nhận sẽ **tái hiện từng điểm trước khi sửa** — cả hệ quả lẫn nguyên nhân bạn nêu (hệ quả đúng mà nguyên nhân sai vẫn dẫn tới sửa sai chỗ).

---
*Ghi chú cho người soạn (xoá trước khi gửi):* file phải tự đủ — người review không có lịch sử trò chuyện. **Đủ thông tin, ngữ cảnh, trạng thái** (chủ dự án
22/11/2026: "bạn phải cung cấp đầy đủ thông tin, ngữ cảnh, trạng thái, ... để các model AI khác đạt kết quả toàn diện nhất, tốt nhất" — áp cho MỌI đề bài gửi model
khác: soát code, nghiên cứu, phê bình giao diện…): trước khi gửi tự hỏi "model kia chỉ có file này và repo — nó có biết ta đang ở đâu, đã thử gì, thế nào là tốt,
không được chạm gì không"; thiếu câu nào thì bổ sung, đủ quan trọng hơn ngắn. Nguyên tắc chọn (chủ dự án 22/11/2026): "bạn nắm gì thì các model AI khác cũng vậy,
những gì bạn thấy quan trọng, thấy cần thiết thì đưa vào, những gì không cần thiết hoặc không đáng đưa vào thì bạn đừng đưa" ⇒ đưa cả danh sách điểm nhóm đã tìm ra
(nhãn "đã biết"), cả file `.md` và thư mục code nên đọc; không đưa nhật ký theo giờ, chuyện quy trình nội bộ, thứ không giúp trả lời câu hỏi (sổ việc / luật của dự án: chỉ trỏ khi câu hỏi chạm tới). Chỉ khi MỤC ĐÍCH của
chính đề bài là lấy ý kiến mù để so với lượt soát của nhóm thì mới giấu danh sách đó — và ghi rõ điều ấy ở đoạn mở đầu. Bí mật (file khoá, bộ câu kín) không bao
giờ đưa — và phải được GHI TÊN ở mục 3 của đề bài (đoạn ghi chú này bị xoá trước khi gửi, model kia không thấy). Cái giá của việc đưa danh sách của nhóm: không còn đo
được "bên kia sót bao nhiêu điểm của ta" — cần con số đó thì soạn đề bài mù. Chủ dự án tự mở công cụ hãng khác và gửi file; agent không tự gọi
công cụ đó. Lưu cả đề bài lẫn file kết quả cạnh nhau (ngoài git nếu chứa chi tiết riêng). Mẫu này rút từ một lần dùng thật ngày 18/11/2026: reviewer khác hãng chỉ đọc code ~10 phút, thêm được 3 điểm thật mà lượt cùng hãng bỏ sót, và sót 8 điểm lượt
cùng hãng thấy — hai lượt bổ sung nhau, không thay nhau; một trong ba điểm đúng hệ quả nhưng sai một nửa nguyên nhân.
