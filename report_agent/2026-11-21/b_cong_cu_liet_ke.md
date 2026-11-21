# Công cụ `liet_ke_bai` — liệt kê BÀI của kho theo nhóm / cụm từ (nhánh `p9-b-liet-ke-bai`, cờ `assistant.liet_ke_bai`, mặc định TẮT)

Viết: 14:41 21/11/2026 (giờ `date`), phiên B. Plan (duyệt trưa 21/11): `b_cong_cu_liet_ke_plan.md` cùng thư mục. Nền: main `30cd9be0` (đã gộp vào nhánh).
Trạng thái: **code + test xong, đã tự đo 160 lượt thật trên hai model; chờ một phiên khác review, phiên đo chấm "Đủ ý" + chạy thước, rồi chủ dự án quyết bật.**

Từ dùng: *bài* = một file của kho (265 bài) · *đoạn* = mảnh của bài mà bước tìm trả về (10 đoạn mỗi lần) · *nhóm* = thư mục của bài trong kho (quán ăn, quán cà phê, món đặc sản, lễ hội,
di tích, nghệ thuật biểu diễn, điểm đến, dịch vụ, vé) · *mục lục* = danh sách mọi bài, nạp từ chính các file kho lúc khởi động · *chạm trần vòng* = model gọi công cụ hết số
vòng cho phép mà chưa viết ⇒ người dùng nhận câu từ chối trống.

## 1. Người dùng thấy gì khác (khi cờ bật)

- **Câu xin danh sách** ("kể hết các lăng…", "những chùa nào…", "chỗ ăn chay…"): câu trả lời nêu ĐỦ các bài kho có, thay vì chỉ vài nơi mà 10 đoạn tìm được chạm tới.
  Ví dụ trên Sonnet: câu về chùa nêu 2 ⇒ 6 chùa (kho có 6 bài), câu về chợ 4 ⇒ 6. Dưới câu trả lời, dòng Nguồn có thêm một nguồn tên **"Mục lục kho tư liệu"** (không mở được thành bài).
- **Câu hỏi về thứ kho chỉ nhắc thoáng qua** (sân golf, rạp chiếu phim — không có bài riêng, chỉ có vài dòng trong bài khác): luna trước đây từ chối, nay trả lời được và nói rõ "trong tư liệu hiện có…".
- **Câu về thứ kho không có** (sòng bạc, bowling, karaoke, sở thú): vẫn là câu từ chối như cũ.
- **Câu một dữ kiện** (giá vé, giờ mở cửa, ở đâu): không đổi — model không gọi công cụ này.
- Dòng ghi chú "danh sách có thể chưa đủ" (tính năng 20/11): KHÔNG đổi chữ.

## 2. Đổi gì

| File | Đổi gì |
|---|---|
| `backend/llm/liet_ke.py` (mới, hàm thuần) | Nạp mục lục từ các file kho · `loc(nhóm, cụm từ)`: bài của nhóm mà TÊN hoặc TOÀN VĂN chứa nguyên cụm (không phân biệt hoa thường / kiểu gạch nối, GIỮ dấu; không phải biểu thức) — bài có cụm ở tên xếp trước, bài chỉ nhắc trong thân kèm đúng dòng nhắc (kể cả dòng phủ định) · tối đa 40 dòng · các dòng trạng thái |
| `backend/llm/assistant.py` | Cờ `liet_ke_bai` + `muc_luc`; `liet_ke_for_turn`: công cụ của một lượt — đăng kết quả thành MỘT nguồn trích được [n] (bộ kiểm trích nguồn không đổi); không khớp ⇒ chỉ dòng trạng thái; ≤ 2 lần / câu; lời gọi trùng ⇒ trỏ về nguồn đã có; lần cuối nói rõ là lần cuối; dùng đủ 2 lần ⇒ công cụ bị ẩn ở lần gọi model kế |
| `backend/llm/full_corpus_prompt.py` | `LIET_KE_MO_TA`: mô tả công cụ theo khuôn làm gì · khi nào dùng · khi nào KHÔNG dùng · trả về gì |
| `backend/llm/generator_openai_full_corpus.py` | Thêm công cụ thứ sáu khi lượt có `liet_ke_fn`; lượt đó được thêm 1 vòng; xin công cụ đã ẩn ⇒ câu từ chối cố định (như `tim_kho`) |
| `backend/config/settings.yaml` | `liet_ke_bai: false` |
| `backend/tests/test_liet_ke_bai.py` (mới) | 13 ca |

Không cổng từ khoá: cờ bật ⇒ công cụ có ở mọi lượt trợ lý có công cụ; mô tả nói khi nào không dùng.

## 3. Bằng chứng

**Test [máy kiểm]:** `uv run pytest tests/test_liet_ke_bai.py -q` ⇒ `13 passed`. Tắt riêng dòng đưa công cụ vào lượt ⇒ 3 ca đỏ (đã thấy). Mười file test chạm đường này: `281 passed`.
Trong 13 ca: hàm lọc trên bài DỰNG TAY (tên trước, dòng làm chứng, hai ca cụm từ khớp nhưng NGƯỢC NGHĨA giữ đúng dòng phủ định, cụm từ lạ không thành biểu thức, cắt trang) ·
mục lục nạp từ kho thật đủ số bài, nhóm nào cũng có bài · cờ tắt gửi model giống byte; cờ bật chỉ thêm đúng một công cụ ở lượt đầu, lượt có lịch sử, đường stream ·
một lượt đủ vòng: gọi công cụ ⇒ trích đúng mã nguồn ⇒ qua bộ kiểm trích nguồn · hết hai lần thì công cụ bị ẩn.

**Lượt thật qua `answer_turn` (không server), mong đợi ghi trước trong script, một lượt mỗi câu trừ khi ghi khác [máy kiểm; người viết tự đọc câu trả lời]:**

| Nhóm câu (số câu) | Đo gì | luna: cờ tắt ⇒ bật | Sonnet high: cờ tắt ⇒ bật |
|---|---|---|---|
| Xin danh sách (7 — lăng, lễ hội, chùa, bãi biển, ăn chay, chợ, cà phê ven sông) | số câu mà ≥ 80 % bài đúng loại của kho CÓ MẶT trong nguồn đưa cho model | 1 ⇒ 5 | 1 ⇒ 5 |
| | — từng câu, bài đúng loại trong nguồn / kho có | lăng 4 ⇒ 8 / 8 · lễ hội 5 ⇒ 39 / 39 · chùa 2 ⇒ 6 / 6 · bãi biển 8 ⇒ 8 / 8 · chợ 3 ⇒ 6 / 6 · ăn chay 1 ⇒ 1 / 6 và cà phê 3 ⇒ 3 / 24 (hai câu này luna KHÔNG gọi công cụ) | lăng 2 ⇒ 8 / 8 · chùa 1 ⇒ 6 / 6 · bãi biển 7 ⇒ 8 / 8 · ăn chay 1 ⇒ 6 / 6 · chợ 3 ⇒ 6 / 6 · lễ hội 0 ⇒ 0 / 39 (không gọi) · cà phê 5 ⇒ 7 / 24 (gọi, lọc theo "ven sông") |
| | — tên bài đúng loại xuất hiện trong câu trả lời | chùa 2 ⇒ 6 · chợ 4 ⇒ 6 · lễ hội 17 ⇒ 21 · lăng 8 ⇒ 8 | chùa 2 ⇒ 6 · chợ 4 ⇒ 6 · lăng 7 ⇒ 8 · lễ hội 22 ⇒ 22 |
| "Nơi nào có đặc điểm X" (3, tự đặt lời) | có câu trả lời · có gọi công cụ | 3 ⇒ 2 trả lời ở bản đầu (câu "gà rán" chạm trần vòng — xem đoạn dưới bảng); bản cuối, lặp lại 3 lần: 9 / 9 lượt trả lời; gọi công cụ ở 1 câu | 3 ⇒ 3 trả lời; gọi ở 1 câu — câu "hút chân không": 1 quán ⇒ 3 quán + 2 thương hiệu |
| Kho chỉ nhắc thoáng (3 — sân golf, hồ bơi công cộng, rạp chiếu phim; KHÔNG có mong đợi ghi trước) | số câu được trả lời | 0 ⇒ 2 | 2 ⇒ 3 |
| Kho không có (4 — sòng bạc, bowling, karaoke, sở thú) | câu từ chối cố định | 4 ⇒ 4 | 4 ⇒ 4 |
| Một dữ kiện (5) | số câu gọi `liet_ke_bai` | — ⇒ 0 / 5 | — ⇒ 0 / 5 |
| Mọi lượt | lỗi trích nguồn · lỗi kỹ thuật | 0 · 0 | 0 · 0 |
| 7 câu danh sách | thời gian trung bình | 9,3 ⇒ 8,4 giây | 9,6 ⇒ 11,2 giây |

Đọc bảng: mức "≥ 80 % ở cả 7 câu" của plan KHÔNG đạt (5 / 7 mỗi model). Hai câu trượt của Sonnet không làm câu trả lời kém đi: câu lễ hội được trả lời từ một bài tổng quan có sẵn
(22 tên, cờ tắt cũng vậy), câu cà phê hỏi riêng quán VEN SÔNG nên lọc 7 / 24 là đúng ý (phép đếm "đúng loại = mọi quán cà phê" của tôi quá rộng cho câu này). Hai câu trượt của luna là
do luna không gọi công cụ.

**Một lỗi tìm ra và sửa trong lúc đo — luna chạm trần vòng.** Câu "gà rán trong trung tâm thương mại" trên luna, cờ bật: model gọi xen kẽ tìm kho và liệt kê, rồi XIN lần liệt kê thứ ba
(chỉ nhận dòng "hết lượt") ⇒ hết vòng ⇒ câu từ chối, trong khi cờ tắt trả lời tốt. Lặp lại câu đó: bản đầu 1 / 4 lượt chạm trần; thêm dòng "đây là lần cuối" + không đăng nguồn trùng: 2 / 3
(không đỡ); **ẩn công cụ sau khi dùng đủ hai lần: 0 / 3**, và 18 lượt lặp lại hai nhóm câu dễ hỏng không lượt nào chạm trần. Bản cuối chạy lại trên Sonnet (17 lượt): 0 lỗi, 0 chạm trần, không
có câu trả lời rác. Mẫu nhỏ — phiên đo cần nhìn dòng "chạm trần vòng" của thước trên luna.

**Một lỗi của chính lượt đo, đã sửa trước khi đọc số.** Bộ "kho không có" đầu tiên (sân golf, hồ bơi, rạp chiếu phim, sòng bạc) sai ở ba câu: tôi dò kho bằng script tìm kho với cờ viết
dính nhau nên nó báo "0 bài" giả; dò lại đúng cách thì kho CÓ nhắc ba thứ đó. Ba câu ấy chuyển thành nhóm "kho chỉ nhắc thoáng" (không có mong đợi ghi trước), bộ "kho không có" thay bằng
bốn thứ dò lại ra 0 bài. Sonnet đã trả lời đúng ba câu đó từ tư liệu (ví dụ nêu đúng một sân golf và nói rõ dự án kia "tư liệu không nói có sân golf hay không").

Tiền thật: 160 lượt, 2,33 USD (gần hết là Sonnet) — vượt mốc 1 USD của một việc; ghi ở đây để phiên điều phối biết.

## 4. So với tiêu chí ghi trước của plan

| Tiêu chí | Kết quả |
|---|---|
| 7 câu danh sách: ≥ 80 % bài đúng loại trong nguồn | **Không đạt đủ:** 5 / 7 mỗi model (trước: 1 / 7) |
| 5 câu "đặc điểm X" của bộ câu mẫu: Đủ ý ≥ 4 ở ≥ 4 / 5 câu | **Chưa đo** — cần người chấm của phiên đo (tôi chỉ chạy 3 câu tự đặt, không chấm điểm) |
| Sàn: thứ kho không có vẫn bị từ chối | Đạt 4 / 4 mỗi model (bộ 4 câu của tôi). An toàn 10 + ngoài phạm vi 10 của thước: **chưa chạy** |
| Sàn: chạm trần vòng 0, lỗi trích nguồn 0, lỗi kỹ thuật 0 | Lỗi 0 / 160. Chạm trần: Sonnet 0; luna có (3 / 7 lượt của một câu) TRƯỚC khi ẩn công cụ; sau khi ẩn 0 / 18 lượt lặp lại (trong đó 3 lượt của câu đó) — mẫu nhỏ |
| Câu một dữ kiện gọi thừa ≤ 1 / 10 | 0 / 5 mỗi model |
| Người thứ hai đọc 12 câu trả lời danh sách (tên nào cũng có trong nguồn; dòng làm chứng không bị đọc ngược nghĩa) | **Chưa làm** — thuộc lượt review |
| Thước + 85 câu không tụt quá nhiễu | **Chưa chạy** — phiên đo |

## 5. Chưa làm / giới hạn

- Mọi câu đo là câu đã thấy hoặc do người viết code tự đặt; phần lớn một lượt mỗi câu. Chưa có bộ mù.
- luna không gọi công cụ ở 2 / 7 câu danh sách và 2 / 3 câu đặc điểm ⇒ lợi ích trên luna nhỏ hơn trên Sonnet; chưa thử sửa mô tả công cụ cho luna (một thay đổi một lần đo).
- So nguyên cụm không hiểu nghĩa: bài nhắc cụm từ theo nghĩa khác vẫn vào danh sách (kèm dòng nhắc để model đọc). Chưa có người đọc tay kiểm model có đọc đúng dòng phủ định không.
- Nguồn "Mục lục kho tư liệu" hiện ở dòng Nguồn nhưng không bấm mở được như một bài; chữ hiển thị do phiên điều phối / chủ dự án chốt trước khi bật. Chưa có lượt trình duyệt.
- Nhánh "vòng cuối chỉ viết" (đang chờ đo) sửa cùng hàm `xin_cong_cu_da_an` ⇒ gộp sau sẽ phải ghép tay một chỗ nhỏ.
- Mỗi lời gọi model của lượt có công cụ dài thêm phần mô tả công cụ (khoảng 400 token); thời gian 7 câu danh sách trên Sonnet tăng 9,6 ⇒ 11,2 giây.

## 6. Bảng kết

| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Hàm lọc + mục lục + công cụ một lượt + nối vào ba kiểu lượt, sau cờ | Xong | `uv run pytest tests/test_liet_ke_bai.py -q` ⇒ `13 passed` |
| Ẩn công cụ sau hai lần dùng (sửa lỗi chạm trần của luna) | Xong | cùng file, ca `-k hidden` ⇒ `1 passed` |
| Tự đo 160 lượt hai model | Xong | số gốc: thư mục riêng tư `ket_qua/b_liet_ke/` của lượt thử Bedrock 21/11; script `tools/b_do_liet_ke.py` |
| Review của phiên khác + đọc tay 12 câu danh sách | Chưa | — |
| Phiên đo: 5 câu đặc điểm của bộ mẫu có chấm, thước, 85 câu | Chưa | — |
| Bật cờ | Chưa — chủ dự án quyết | — |

## 7. Thêm 15:04 21/11/2026 (giờ `date`) — ba điểm của review (phiên C: READY với cờ tắt, ba điều kiện trước khi BẬT)

| Điểm review | Sửa | Kiểm |
|---|---|---|
| Dòng làm chứng cắt 220 ký tự ĐẦU dòng ⇒ dòng model nhận không còn cụm từ (C đếm: "chợ" 6 / 16 bài, "nước ngọt" 8 / 21, "chùa" 2 / 9) — gốc của một chi tiết không có trong nguồn đã trích | Dòng dài cắt MỘT CỬA SỔ QUANH chỗ có cụm từ; cắt làm mất cụm từ thì giữ cả dòng | Đếm lại bằng hàm thật trên kho thật: 0 / 16 · 0 / 21 · 0 / 9 (thêm "hồ" 0 / 35) [máy kiểm] |
| Chỉ lấy dòng ĐẦU có cụm từ ⇒ sót ý nằm ở dòng sau (bãi có "nhà tắm nước ngọt" ở dòng sau bị model bỏ sót) | Dòng làm chứng kèm "(+k dòng khác của bài cũng có cụm từ)" để model biết cần tìm thêm bài đó | Câu đó chạy lại trên Sonnet 2 lần: bãi bị sót nay có mặt 2 / 2 (model gọi `tim_kho` thêm); luna 2 / 2 lần không gọi công cụ ở câu này ⇒ không đổi |
| Lọc theo một nhóm che bài ở nhóm khác ("công viên nước" nằm ở một bài vé) | Dòng trạng thái thêm "Ngoài nhóm này còn k bài khác có cụm từ — gọi lại với nhom = tat_ca", CHỈ khi nhóm đang lọc ra 0 bài hoặc k ≤ 5 | Test hàm thuần. Lượt thật: 1 / 4 lần model gọi công cụ ở câu này (Sonnet, tự chọn "tất cả", nêu đúng khu có công viên nước); 3 / 4 lần model không gọi công cụ ⇒ tình huống "lọc sai nhóm" không tái hiện lại được để xác nhận trên chữ model thật |

Vì sao câu nhắc "ngoài nhóm" có ngưỡng: bản đầu nhắc ở MỌI lần có bài ngoài nhóm; với cụm phổ biến ("chợ": 39 bài ngoài nhóm) luna nghe theo, gọi lại "tất cả" (61 bài) rồi tìm thêm hai lần ⇒ 29 giây.
Có ngưỡng: luna không gọi lại "tất cả" nữa nhưng câu đó vẫn 24 giây (bản trước review: 15,5 giây; cờ tắt 10,9 giây — một lượt mỗi ô) ⇒ **câu danh sách dài trên luna chậm hơn rõ khi cờ bật**; phiên đo cần cột thời gian.
Test: `tests/test_liet_ke_bai.py` nay 15 ca. Thêm 12 lượt thật (6 câu × 2 lần chạy, hai model), 0 lỗi.

**Điều review nêu mà nhánh này KHÔNG giải:** câu trả lời trích "Mục lục kho tư liệu" thay cho từng bài ⇒ các dòng ghi chú sinh từ NGUỒN BÀI được trích có thể không hiện (dòng "giờ mở cửa, giá vé có thể đã thay đổi",
dòng cảnh báo tạm ngừng của bãi biển / suối / thác) — C thấy 1 ca mất dòng "có thể đã thay đổi". Hướng có thể làm (chưa làm, cần quyết vì đổi thứ người dùng thấy): nguồn mục lục mang theo đường dẫn các bài nó
liệt kê; bộ nối ghi chú coi bài nào CÓ TÊN trong câu trả lời là "được trích" khi xét ghi chú. Rủi ro: một danh sách 8 bãi biển kéo theo nhiều dòng cảnh báo cùng lúc. Trước khi bật cờ, phiên đo cần đếm cột "thiếu cảnh báo"
trên câu xin danh sách nơi có rủi ro.

**Khi ghép với nhánh "vòng cuối chỉ viết" (C đã xem cả hai diff):** (a) điều kiện ẩn `liet_ke_bai` đi qua cùng hàm gom điều kiện của nhánh kia để vòng cuối không gửi nó; (b) trần vòng truyền cho cơ chế vòng cuối phải
tính cả vòng thêm của công cụ này; (c) hàm nhận "xin công cụ đã ẩn" hợp ba điều kiện (hết lượt tìm · hết lượt liệt kê · vòng cuối). Nhánh nào gộp sau, tôi ghép.
