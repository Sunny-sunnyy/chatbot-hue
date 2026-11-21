# Công cụ "gần một điểm có gì" — quán ăn · cà phê · điểm tham quan quanh một điểm, chỉ thứ có bài trong kho (nhánh `p9-c-gan-diem`)

Phiên C ghi 22:03 21/11/2026 (giờ `date`). Từ main `a4f1aa56`. Công tắc `gan_diem` đang TẮT — chưa bật, chưa gộp. Mục đã chốt 20/11 ("gần X có gì ăn" trong ô chat). Người đọc: phiên B hoặc phiên đo.
Plan + tiêu chí ghi trước (riêng tư): `data/thu_bedrock_2026-11-21/c_muc_5/PLAN_P1.md`; số đếm trước khi làm: `…/MUC_5_GAN_X.md`.

## Người dùng thấy gì khác (khi bật)
| Hôm nay | Khi bật |
|---|---|
| "Trưa gần Đại Nội có quán nào ăn ngon?" ⇒ 4 / 5 lượt đo trả lời "tư liệu không nói quán nào nằm gần Đại Nội" rồi liệt kê quán không khẳng định gần (kho không viết "quán A gần điểm B") | Tới 5 quán CÓ BÀI TRONG KHO quanh Đại Nội, gần trước, mỗi quán kèm "cách khoảng …" theo đường chim bay do hệ thống tính; địa chỉ, giờ, món lấy từ bài kho của quán như mọi câu khác |
| "Gần chùa Thiên Mụ còn điểm nào để ghé?" ⇒ trợ lý tự tra khoảng cách từng cặp, có lượt hết vòng | 5 điểm tham quan gần nhất kèm km + phút đi xe (cùng số với công cụ khoảng cách) |
| Nơi không có quán nào trong kho quanh đó, hoặc nơi hệ thống không có vị trí (ga, khách sạn…) | Một dòng nói thật do hệ thống viết; không tự nêu quán khác là "gần" |

## Cách làm
- Một công cụ mới cho trợ lý. Model chỉ gửi hai giá trị trong danh sách đóng — mã một trong 40 điểm (hoặc "nơi khác") và loại (quán ăn / cà phê / điểm tham quan); mọi con số do code tính: quán lấy từ bảng quán của thẻ lịch, CHỈ dòng có bài kho, ≤ 2 km đường chim bay; điểm tham quan lấy từ bảng khoảng cách đang có. Quán có vị trí mức "ước" chỉ được nói theo nấc ("trong khoảng 1 km", "khoảng 1–2 km").
- Kết quả là một nguồn có mã [n] như các nguồn khác; số km / phút của nó thuộc tập số được phép của phép kiểm số sau khi viết (model tự thêm số khoảng cách khác thì câu đó bị gỡ).
- Chỉ đưa công cụ ở lượt có chữ gần / quanh / cạnh / lân cận / kế bên (câu này hoặc câu hỏi liền trước); lượt đó được thêm một vòng công cụ như ba công cụ tính toán kia. Lượt khác và công tắc tắt: chuỗi gửi model giống từng byte.
- KHÔNG làm (chờ chủ dự án): quán từ nguồn mở chưa kiểm vào ô chat · thêm mốc ngoài 40 điểm (ga, sân bay, khách sạn…).
- File: `backend/llm/gan_diem.py` (mới) · `assistant.py` · `generator_openai_full_corpus.py` · `settings.yaml` · `tests/test_gan_diem.py`.

## Lệnh kiểm + đầu ra (0 đồng — model là phản hồi dựng sẵn, tìm kho là Qdrant thật)
| Phép | Đầu ra |
|---|---|
| `pytest tests/test_gan_diem.py -q` | `37 passed`; cố ý bỏ điều kiện "có bài kho" ⇒ `3 failed`; cố ý không đưa số của công cụ vào phép kiểm số ⇒ `1 failed`; trả lại ⇒ `37 passed` |
| từng file: `test_khoang_cach` · `test_b2_tool_loop` · `test_het_luot_tim` · `test_liet_ke_bai` · `test_bedrock_model` · `test_phase6_settings` · `test_settings_env` · `test_quan_lich` | 101 · 12 · 7 · 17 · 21 · 5 · 6 · 17 passed |
| Công tắc tắt giống từng byte: 180 loại lượt dựng sẵn, mã băm thân yêu cầu gửi model, cây gốc ↔ nhánh | khác 0 / 180 |
| Hàm thuần trên bảng THẬT: 41 điểm + "nơi khác" × 3 loại = 126 lời gọi | 0 lỗi (mọi quán trả ra có bài kho, đúng loại, ≤ 2 km; mọi điểm trả ra nằm trong bảng; không số lẻ cho vị trí mức ước; nơi không có ⇒ đúng dòng cố định). Có kết quả: quán ăn 29 điểm · cà phê 17 điểm · điểm tham quan 40 điểm |

## Chưa làm · giới hạn · cách lùi
- CHƯA có lượt model thật nào: bộ câu mù 12 câu của phiên điều phối chạy một lượt trên model đang chạy sau commit này; số ghi tiếp vào file này. Model cũ: chưa đo (chủ dự án tạm gác).
- Giới hạn: "gần" là đường chim bay (qua sông có thể xa hơn) — chữ luôn ghi rõ · nơi ngoài 40 điểm chỉ nhận dòng nói thật · 12 / 41 điểm không có quán ăn nào có bài kho trong 2 km (các lăng xa, biển, phá, Bạch Mã…) · quán có trong kho nhưng chưa có vị trí trong bảng thì công cụ không thấy · bảng quán phải là bản 2 (nhánh `p9-c-bang-quan-v2`: bản 1 còn một quán đã đóng cửa).
- Cách lùi: đặt `gan_diem: false` trong `backend/config/settings.yaml`, khởi động lại — hệ thống chạy y như trước (đã kiểm giống từng byte).
- Phép này KHÔNG cho biết quán còn mở / ngon không (model lấy từ bài kho) · hướng rộng hơn: thêm vị trí cho ~49 bài quán chưa có và vài mốc phổ biến (việc dữ liệu, chờ chủ dự án) · đếm rẻ nhất sau khi bật: trên log, số lượt có chữ "gần" mà công cụ được gọi và trả ≥ 1 kết quả.
