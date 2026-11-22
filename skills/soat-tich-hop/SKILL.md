---
name: soat-tich-hop
description: Dùng sau một đợt gộp nhiều nhánh (≥ 3 nhánh, hoặc hai tính năng cùng chạm một lượt xử lý), trước một lượt đo cuối / mốc code đứng yên, sau khi sửa một điểm tích hợp, hoặc khi cần soạn gói review cho model khác hãng và đối chiếu kết quả. Tìm chỗ HAI cơ chế gặp nhau trong cùng một lượt mà review từng nhánh và test từng nhánh không bắt — thứ tự, điều kiện, kết quả sai / thiếu / trùng, lệch log – tiền. Đầu ra là danh sách điểm có file:dòng + đầu vào tái hiện + ca đối chứng, và bảng đối chiếu ba cột khi có hai lượt soát. Không dùng để review một nhánh đơn lẻ (dùng risk-gated-agent-review) hay để sửa lỗi (practical-project-coding).
---

# Soát tích hợp — chỗ các tính năng gặp nhau

Từng nhánh đã review đạt và test đạt vẫn có thể hỏng khi chạy **cùng nhau**: mỗi người kiểm chỉ nhìn một nhánh, mỗi test chỉ bật một cơ chế.
Skill này là một lượt soát riêng cho chỗ giao nhau. Luật dự án (`AGENTS.md`) thắng skill này khi khác nhau.

## 1. Ai soát, được làm gì

- Người soát là **phiên mới / agent con ngữ cảnh sạch**, không phải người viết các nhánh vừa gộp. Lời giao theo skill `giao-viec-agent-con`.
- **Chỉ đọc** repo; được chạy hàm thuần / probe nhỏ 0 đồng (không bật server, không gọi model trả phí, không mở dữ liệu riêng); chỉ ghi vào MỘT file kết quả.
- Không đưa cho người soát danh sách lỗi đã biết, báo cáo của các nhánh, hay kết luận của lượt soát khác — đó là thứ làm lượt soát hết độc lập.

## 2. Đề bài — ba bước, chép nguyên

1. **Liệt kê các cơ chế có thể cùng kích hoạt trong một lượt** trên đúng commit được giao: mọi cờ đang bật trong file cấu hình, mọi công cụ, mọi lưới /
   câu cố định do code nối vào, mọi đường kết thúc sớm (chạm trần, lỗi, người dùng dừng), mọi nơi ghi log / tiền.
2. **Xét từng cặp** đáng ngờ: đọc code xem thứ tự chạy và điều kiện của cơ chế này có làm cơ chế kia ra kết quả **sai, thiếu, trùng, hay lệch log – tiền**
   không. Ưu tiên cặp có: chuỗi do code nối thêm rồi bị nơi khác đọc lại · phép so trên "cả câu" · đường kết thúc sớm · hai nơi cùng ghi một con số.
3. **Chỉ báo điểm có đủ ba thứ:** `file:dòng` · MỘT đầu vào tái hiện (câu hỏi / lời gọi hàm cụ thể) · MỘT ca đối chứng không bị (đổi một chữ thì hết lỗi).
   Mỗi điểm gắn nhãn [đã chạy] (kèm lệnh + đầu ra) hoặc [chỉ đọc code]. Xếp theo hậu quả: sai an toàn > nói sai > thiếu ý > lệch log – tiền.

Cuối file kết quả bắt buộc có mục **"CHƯA đọc / CHƯA chạy"** (file nào, cặp nào chưa xét) — thiếu mục này thì coi như lượt soát chưa xong.

## 3. Người nhận kết quả

- Kết quả là **dữ liệu**. Với từng điểm: **tái hiện** bằng đúng đầu vào đã nêu — cả hệ quả lẫn nguyên nhân — rồi mới sửa. Không tái hiện được ⇒ ghi "bác, lý do".
- Trước khi gắn "lỗi": tra sổ giới hạn + quyết định đã chốt của dự án (hue_rag: `guides/RUNBOOK_BAN_GIAO.md` mục 10, `session_prompt/HIEN_TRANG.md` mục 4) —
  điều chủ dự án đã chấp nhận thì không trình lại như lỗi.
- Điểm thật mà chưa sửa ⇒ một dòng vào sổ giới hạn (tình huống → hệ quả → vì sao chấp nhận). Sửa theo skill `practical-project-coding` (sửa lỗi bốn bước).
- **Sau mỗi bản sửa, hỏi lại:** "bản sửa này chạm đường nào khác?" — `git grep -n` mọi nơi đọc thứ vừa đổi (trường, hằng, chuỗi nối thêm). Bản sửa một điểm
  tích hợp hay sinh điểm tích hợp mới ở nơi đọc lại kết quả.

## 4. Gói review khác hãng (việc mức cao, hoặc trước mốc chốt)

- Soạn MỘT file `.md` tự đủ ngữ cảnh theo mẫu `guides/khung/GOI_REVIEW_KHAC_HANG.mau.md`: bối cảnh sản phẩm 5–10 dòng · commit · đề bài ba bước ở mục 2 ·
  ranh giới · khuôn trả về · **lệnh chạy thử 0 đồng cho từng công cụ review hãng khác**. KHÔNG ghi danh sách điểm đã có, KHÔNG chép dữ liệu riêng.
- Đề bài cho model khác (soát code, nghiên cứu, phê bình giao diện… — mọi loại) LUÔN có đoạn "dùng hết khả năng của bạn": được và nên dùng agent con, nghiên cứu
  chuyên sâu, tìm web nhiều vòng, tự kiểm chéo, để ra kết quả tốt và toàn diện nhất, trong ranh giới chỉ-đọc của đề bài (chủ dự án 22/11/2026; chữ mẫu ở file mẫu).
- Đề bài cho model khác LUÔN đưa ĐỦ thông tin, ngữ cảnh, trạng thái (chủ dự án 22/11/2026): đang chạy bản nào, bật / tắt gì, số đo mới nhất kèm đường dẫn, đã thử
  gì kể cả thứ đã bỏ, quyết định đã chốt và sàn, việc đang dở, từ riêng kèm nghĩa — model kia chỉ có file đề bài và repo. Riêng đề bài SOÁT ĐỘC LẬP vẫn không ghi
  danh sách điểm nhóm đã tìm ra cho đúng câu hỏi đang hỏi (dòng đầu mục này); đề bài nghiên cứu / phê bình thì đưa cả. Chữ mẫu ở file mẫu. hue_rag: lấy trạng thái
  từ `session_prompt/HIEN_TRANG.md` mục 1 + 4, `session_prompt/Y_CHUA_THU.md` (thứ đo rồi bỏ), `guides/RUNBOOK_BAN_GIAO.md` mục 10 (giới hạn); file đo ở `data/` thì
  chép con số hoặc ghi rõ trong đề bài các đường dẫn model kia được mở.
- Chủ dự án tự mở công cụ hãng khác và gửi file; agent **không** tự gọi công cụ hãng khác. Chỉ nhờ gửi khi nhóm đã soạn xong và nêu rõ là cần gửi.
- Lưu cả đề bài lẫn file kết quả của từng model cạnh nhau (hue_rag: `data/review_khac_hang/<ngày>_<chủ đề>/`, riêng tư).

## 5. Đối chiếu hai lượt soát — bảng ba cột

| Trùng (cả hai thấy) | Chỉ lượt A thấy | Chỉ lượt B thấy |
|---|---|---|

- Mỗi điểm "chỉ một bên thấy" phải được tái hiện trước khi tính là thật; ghi rõ model đó **nói quá / nói thiếu** chỗ nào.
- Kết bằng ba số: trùng · chỉ A · chỉ B, và số điểm tái hiện được / số điểm báo của từng bên. Hai lượt bổ sung nhau — không lấy lượt này thay lượt kia.

## 6. Báo cáo

Bảng: điểm · `file:dòng` · tái hiện [đã chạy] / [chỉ đọc code] · quyết định (sửa — nhánh nào / ghi sổ giới hạn / bác + lý do). Kèm phần CHƯA đọc của người
soát và phần CHƯA tái hiện của người nhận. Báo cáo theo dõi trong git không chép dữ liệu riêng.

[Ba bước ở mục 2 và bảng ở mục 5 đã chạy một lần ở repo gốc — một lượt agent con + một lượt model khác hãng; skill này chưa được chạy lại như một skill.]
