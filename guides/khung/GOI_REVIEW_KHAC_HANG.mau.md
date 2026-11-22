# Đề bài review độc lập — <việc cần soi> (<tên dự án>, bản `<mã commit>`)

Soạn <giờ lấy bằng `date`> bởi <ai>. Người gửi file này cho bạn là chủ dự án. Bạn là **người review khác hãng**: bạn không viết dòng code nào ở đây, và bạn KHÔNG
được cho biết nhóm đã tìm ra gì — để kết quả của bạn không bị dẫn dắt.

## 1. Bối cảnh (đủ để làm, không cần đọc tài liệu điều phối)
- Thư mục làm việc: <gốc repo>, nhánh <…>, commit `<…>`. Sản phẩm là gì, dựng bằng gì, code ở đâu — 3–5 dòng.
- Điều vừa thay đổi / phạm vi cần soi — 3–5 dòng.
- Bản đồ để đọc code: <file nào tả từng tính năng> · bẫy đã biết (đừng báo lại như phát hiện mới): <file nào>.

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
- **Không mở, không in:** file khoá; <các thư mục dữ liệu riêng>.
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
Danh sách của bạn sẽ được so với danh sách của một reviewer cùng hãng với người viết: điểm nào trùng, điểm nào chỉ bạn thấy; mỗi điểm chỉ bạn thấy sẽ được chạy lại
để xác nhận. Phát hiện ít mà đúng có giá hơn nhiều mà đoán.
Người nhận sẽ **tái hiện từng điểm trước khi sửa** — cả hệ quả lẫn nguyên nhân bạn nêu (hệ quả đúng mà nguyên nhân sai vẫn dẫn tới sửa sai chỗ).

---
*Ghi chú cho người soạn (xoá trước khi gửi):* file phải tự đủ — người review không có lịch sử trò chuyện. Chủ dự án tự mở công cụ hãng khác và gửi file; agent không tự gọi
công cụ đó. Lưu cả đề bài lẫn file kết quả cạnh nhau (ngoài git nếu chứa chi tiết riêng). Mẫu này rút từ một lần dùng thật ngày 18/11/2026: reviewer khác hãng chỉ đọc code ~10 phút, thêm được 3 điểm thật mà lượt cùng hãng bỏ sót, và sót 8 điểm lượt
cùng hãng thấy — hai lượt bổ sung nhau, không thay nhau; một trong ba điểm đúng hệ quả nhưng sai một nửa nguyên nhân.
