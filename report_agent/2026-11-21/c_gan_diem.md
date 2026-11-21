# Công cụ "gần một điểm có gì" — quán ăn · cà phê · điểm tham quan quanh một điểm, chỉ thứ có bài trong kho (nhánh `p9-c-gan-diem`)

Phiên C ghi 22:03, bổ sung số đo thật 22:19 21/11/2026 (giờ `date`). Từ main `a4f1aa56`. Công tắc `gan_diem` đang TẮT — chưa bật, chưa gộp. Mục đã chốt 20/11 ("gần X có gì ăn" trong ô chat). Người đọc: phiên B hoặc phiên đo.
Plan + tiêu chí ghi trước (riêng tư): `data/thu_bedrock_2026-11-21/c_muc_5/PLAN_P1.md`; số đếm trước khi làm: `…/MUC_5_GAN_X.md`.

## Người dùng thấy gì khác (khi bật)
| Hôm nay | Khi bật |
|---|---|
| "Trưa gần Đại Nội có quán nào ăn ngon?" ⇒ 4 / 5 lượt đo trả lời "tư liệu không nói quán nào nằm gần Đại Nội" rồi liệt kê quán không khẳng định gần (kho không viết "quán A gần điểm B") | Tới 5 quán CÓ BÀI TRONG KHO quanh Đại Nội, gần trước, mỗi quán kèm "cách khoảng …" theo đường chim bay do hệ thống tính; địa chỉ, giờ, món lấy từ bài kho của quán như mọi câu khác |
| "Gần chùa Thiên Mụ còn điểm nào để ghé?" ⇒ trợ lý tự tra khoảng cách từng cặp, có lượt hết vòng | 5 điểm tham quan gần nhất kèm km + phút đi xe (cùng số với công cụ khoảng cách) |
| Nơi không có quán nào trong kho quanh đó, hoặc nơi hệ thống không có vị trí (ga, khách sạn…) | Một dòng nói thật do hệ thống viết; không tự nêu quán khác là "gần" |

## Cách làm
- Một công cụ mới cho trợ lý. Model chỉ gửi hai giá trị trong danh sách đóng — mã một trong 40 điểm (hoặc "nơi khác") và loại (quán ăn / cà phê / điểm tham quan); mọi con số do code tính: quán lấy từ bảng quán của thẻ lịch, CHỈ dòng có bài kho, ≤ 2 km đường chim bay; điểm tham quan lấy từ bảng khoảng cách đang có. Quán có vị trí mức "ước" chỉ được nói theo nấc ("chưa tới 1 km", "khoảng 1–2 km").
- Kết quả là một nguồn có mã [n] như các nguồn khác; số km / phút của nó thuộc tập số được phép của phép kiểm số sau khi viết (model tự thêm số khoảng cách khác thì câu đó bị gỡ).
- Chỉ đưa công cụ ở lượt có chữ gần / quanh / cạnh / lân cận / kế bên (câu này hoặc câu hỏi liền trước); lượt đó được thêm một vòng công cụ như ba công cụ tính toán kia. Lượt khác và công tắc tắt: chuỗi gửi model giống từng byte.
- KHÔNG làm (chờ chủ dự án): quán từ nguồn mở chưa kiểm vào ô chat · thêm mốc ngoài 40 điểm (ga, sân bay, khách sạn…).
- File: `backend/llm/gan_diem.py` (mới) · `assistant.py` · `generator_openai_full_corpus.py` · `settings.yaml` · `tests/test_gan_diem.py`.

## Lệnh kiểm + đầu ra (0 đồng — model là phản hồi dựng sẵn, tìm kho là Qdrant thật)
| Phép | Đầu ra |
|---|---|
| `pytest tests/test_gan_diem.py -q` | `37 passed` (chạy lại sau lần sửa chữ ở mục dưới: `37 passed`); cố ý bỏ điều kiện "có bài kho" ⇒ `3 failed`; cố ý không đưa số của công cụ vào phép kiểm số ⇒ `1 failed`; trả lại ⇒ `37 passed` |
| từng file: `test_khoang_cach` · `test_b2_tool_loop` · `test_het_luot_tim` · `test_liet_ke_bai` · `test_bedrock_model` · `test_phase6_settings` · `test_settings_env` · `test_quan_lich` | 101 · 12 · 7 · 17 · 21 · 5 · 6 · 17 passed |
| Công tắc tắt giống từng byte: 180 loại lượt dựng sẵn, mã băm thân yêu cầu gửi model, cây gốc ↔ nhánh | khác 0 / 180 (chạy lại sau lần sửa chữ: khác 0 / 180) |
| Hàm thuần trên bảng THẬT: 41 điểm + "nơi khác" × 3 loại = 126 lời gọi | 0 lỗi (mọi quán trả ra có bài kho, đúng loại, ≤ 2 km; mọi điểm trả ra nằm trong bảng; không số lẻ cho vị trí mức ước; nơi không có ⇒ đúng dòng cố định). Có kết quả: quán ăn 29 điểm · cà phê 17 điểm · điểm tham quan 40 điểm |

## Lượt model thật (22:06–22:19 21/11) — bộ 12 câu mù của phiên điều phối, MỘT lượt, model đang chạy
Cách đo: mỗi câu một cuộc mới qua đường chat thật (`/api/chat/stream` trong cùng tiến trình), công tắc bật bằng ghi đè cấu hình, bảng quán bản 2, bộ nhớ đệm câu trả lời tắt. Bộ câu do phiên điều phối soạn không nhìn code, mở SAU commit đóng code `c8c21a2`. Dữ liệu thô + bộ chạy (riêng tư): `data/thu_bedrock_2026-11-21/c_muc_5/` (`luot_1`, `luot_2_lai`, `g06_tat_1`, `g06_tat_2`, `luot_3_sau_sua_chu`, `do_gan_x.py`, `doi_chieu_chu.py`). Nhãn: [máy đếm] · [C đọc tay — người viết, không mù].

| Điều cần biết | Kết quả |
|---|---|
| Lỗi hiện ra · chạm trần vòng · thời gian | 0 / 12 · 0 / 12 · trung vị 8,7 giây, lâu nhất 17,1 giây [máy đếm] |
| Model có gọi đúng công cụ không | 9 / 9 câu hỏi về nơi có trong bảng: gọi đúng mã điểm + đúng loại. 3 câu còn lại (ga Huế, sân bay Phú Bài, câu "quán gần nhà mình trong Sài Gòn"): không gọi, trả lời theo đường cũ [máy đếm] |
| Nơi có quán / điểm (6 câu) | 6 / 6 nêu đủ 5 tên của danh sách code trả; mọi con số km / phút đi kèm đúng số của code (30 / 30 dòng) [máy đếm + đọc tay] |
| Có bịa "gần" không | 0 / 12: mọi chỗ gọi một quán là "gần" hoặc là dòng của công cụ, hoặc là câu có trong bài kho được trích (tìm lại trong kho bằng `scripts/grep_kb.sh`: thấy đúng câu ở 4 / 4 chỗ) |
| Nơi không có quán loại được hỏi (3 câu) | 3 / 3 nói thật "trong kho chưa có bài … trong khoảng 2 km"; 2 / 3 kèm quán cùng khu vực và ghi rõ nguồn không nêu khoảng cách |
| Nơi ngoài bảng (2 câu) · câu giống-mà-không-phải (1 câu) | 2 / 2 nói nguồn không ghi khoảng cách, không bịa · 1 / 1 không liệt kê quán "gần" |

**Theo đúng CHỮ tiêu chí ghi trước ("0 quán / điểm gần ngoài danh sách code trả"): 8 / 12 đạt, 4 câu không đạt chữ** — ghi nguyên, không đổi tiêu chí sau khi thấy số:
- Ba câu (quanh Đại Nội, chợ Đông Ba, cầu Trường Tiền) nêu THÊM một quán ngoài danh sách vì chính bài kho của quán viết vậy: Quán O Giàu "gần cửa Chương Đức của Đại Nội", Đề-Pô Cafe "trên lầu 2 của chợ Đông Ba", Highlands chi nhánh TNL Plaza "gần cầu Trường Tiền" — có mã nguồn, có câu đó trong kho. Chạy lại đúng ba câu một lần: lặp lại 3 / 3 ⇒ hành vi ổn định, không phải dao động. [Diễn giải của C, người đọc quyết] tiêu chí viết để bắt "bịa gần"; ba ca này là kho tự nói và có lợi cho người dùng (quán sát Đại Nội nhất chưa có vị trí trong bảng nên công cụ không thấy).
- Câu "Ở Đại Nội ra thì lăng nào gần nhất": công cụ trả 5 điểm gần nhất, không có lăng nào; lượt 1 trả lời dè dặt bằng số "cách trung tâm" của kho, lượt chạy lại ra câu từ chối + mục Từ web. Đối chứng công tắc TẮT, cùng câu, 2 lượt: một dè dặt, một từ chối + mục web ⇒ hai bên như nhau, không phải do công cụ gây ra — nhưng công cụ cũng không giúp. Bảng khoảng cách có sẵn đáp án (Đại Nội → Lăng Dục Đức 3,9 km · Tự Đức 6,3 · Đồng Khánh 6,5 · Thiệu Trị 7,7 · Khải Định 9,8 · Minh Mạng 13,2 · Gia Long 20,0 km đường đi) mà chưa đường nào dùng.

**Một lỗi chữ tìm ra từ lượt đo, đã sửa SAU khi mở bộ mù (khai rõ):** với quán có vị trí mức ước ở dưới 1 km, code trả "trong khoảng 1 km" nhưng model chép lại thành "khoảng 1 km" ở 8 / 8 lần (cả lượt đầu lẫn lượt chạy lại) — quán cách vài trăm mét nghe như cách một cây số. Sửa một chuỗi trong code thành "chưa tới 1 km" (không chỉnh mô tả công cụ). Test sửa trước: `1 failed, 36 passed` trên code cũ ⇒ `37 passed`. Chạy lại đúng hai câu từng tái hiện: "chưa tới 1 km" có mặt ở cả hai, "khoảng 1 km" 0 lần.

Tiền: lượt 12 câu 0,583 USD · chạy lại 4 câu 0,218 · đối chứng 2 lượt 0,101 · chạy lại sau sửa chữ 0,119 ⇒ 1,02 USD Bedrock. OpenAI: 0.

## Chưa làm · giới hạn · cách lùi
- Chưa đo: model cũ (chủ dự án tạm gác) · câu hỏi tiếp ở lượt sau ("còn quán nào nữa không") · trên trình duyệt. Mỗi câu chỉ MỘT lượt (4 câu có hai lượt).
- Giới hạn thấy ở lượt thật: (1) "X NÀO gần nhất" theo loại (lăng, chùa…) chưa trả lời được — công cụ chỉ trả 5 điểm gần nhất mọi loại; (2) công cụ chỉ thấy 42 quán có vị trí trong bảng, nên có khi quán sát nhất lại do bài kho nói chứ không do công cụ (Quán O Giàu); (3) câu "gần lăng Minh Mạng có quán ăn nào": nói thật là không có, rồi nêu hai quán trên ĐƯỜNG Minh Mạng (cách lăng xa) kèm câu "kho không nêu khoảng cách" — người đọc vội có thể hiểu nhầm; (4) nơi ngoài bảng: model không gọi công cụ nên không có dòng "chưa có vị trí của nơi này", câu trả lời như khi tắt.
- Giới hạn có từ thiết kế: "gần" là đường chim bay (qua sông có thể xa hơn) — chữ luôn ghi rõ · nơi ngoài 40 điểm chỉ nhận dòng nói thật · 12 / 41 điểm không có quán ăn nào có bài kho trong 2 km (các lăng xa, biển, phá, Bạch Mã…) · quán có trong kho nhưng chưa có vị trí trong bảng thì công cụ không thấy · bảng quán phải là bản 2 (nhánh `p9-c-bang-quan-v2`: bản 1 còn một quán đã đóng cửa).
- Cách lùi: đặt `gan_diem: false` trong `backend/config/settings.yaml`, khởi động lại — hệ thống chạy y như trước (đã kiểm giống từng byte).
- Phép này KHÔNG cho biết quán còn mở / ngon không (model lấy từ bài kho) · hướng rộng hơn: thêm vị trí cho ~49 bài quán chưa có và vài mốc phổ biến (việc dữ liệu, chờ chủ dự án) · đếm rẻ nhất sau khi bật: trên log, số lượt có chữ "gần" mà công cụ được gọi và trả ≥ 1 kết quả. Ý chưa thử: cho công cụ lọc điểm tham quan theo loại ("lăng nào gần nhất") — đếm trước trên sổ lượt thật xem có bao nhiêu câu kiểu này.
