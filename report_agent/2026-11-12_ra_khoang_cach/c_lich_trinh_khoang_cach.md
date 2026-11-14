# Lập lịch trình: khoảng cách hue_rag ↔ Huế TRIPO + lượt đếm rẻ (C, 12/11)

Người làm: C (`hue-rag-e1`). Viết 20:45 12/11/2026 (`date`). A giao sau khi User nói (tối 12/11/2026, A ghi trong `CURRENT_HANDOFF.md` "VIỆC ĐỢT 2 PHIÊN 12/11") "muốn tập trung mạnh vào lập lịch trình như Huế TRIPO, cần thêm gì".
Không code, không sửa kho / bảng điểm. Tiền thật **0,010547 USD** (trần 0,03). Report tả ở mức loại yêu cầu; không chép câu trả lời. Dữ liệu chạy (private): `data/phase_11/dot_2_dem/`.

## 1. Đã làm gì

- **Đọc:** hồ sơ Huế TRIPO vòng 3 (`data/nghien_cuu_tinh_nang_2026-11-04/sa2_tripo_v3_agentic.md` — vòng thấy được cơ chế lập lịch qua gói tin), báo cáo vòng 5 của B
  (`b_tripo_v5.md` cùng thư mục), code `backend/llm/lich_trinh.py`, bảng điểm đang chạy (`settings.yaml` trỏ `diem_v3.json`, 28 điểm), danh sách plan lịch trình cũ (B5, B5b, B5c,
  sửa lịch, bản đồ, T4, định tuyến lịch) + STATUS / handoff về kết quả của chúng. **Không** mở lại từng report cũ ⇒ cột "đã thử / đã bỏ" ghi theo handoff, `Project_Status.md`, STATUS.
- **Đếm có phí (1 lượt, server `main` thật `53f941d`, 20:39–20:41 theo log):** 14 yêu cầu qua **biểu mẫu "Lên kế hoạch"** phủ 4 mức số ngày × 5 nhóm người × 2 kiểu đi (+ không chọn) ×
  5 sở thích (+ không chọn), và 3 yêu cầu **gõ tự do** (có ngân sách · có giờ đến / về · có điểm bắt buộc). Bộ ghi trước khi gửi: `cau_lich_trinh.jsonl` md5 `adbe76da87d8`.
- **Đếm 0 USD:** chạy thẳng hàm xếp `xep()` trên **cả 360 tổ hợp** biểu mẫu có thể chọn (4 × 5 × 3 × 6) với bảng điểm đang chạy — in số đếm.
- Giới hạn: 14 lịch, một lượt, C tự đọc (không có người chấm thứ hai); TRIPO không được gửi lại hôm nay (số của TRIPO lấy từ vòng 3–5).

## 2. Bảng khoảng cách — lập lịch trình

| Việc | Huế TRIPO làm gì (vòng 3–5) | hue_rag làm gì (`file` · hàm) | Thiếu gì | Đã thử / đã bỏ vì sao |
|---|---|---|---|---|
| **Nhập yêu cầu** | biểu mẫu nhiều nhóm: loại hình, kiểu đi, đi cùng ai, **số người, ngân sách, ngày khởi hành**; gõ câu tự do ⇒ mô hình đổi thành nhãn biểu mẫu | biểu mẫu 4 trường: số ngày · đi cùng · kiểu đi · sở thích (`backend/llm/hoi_lai.py` `GIA_TRI`, `TruongInput`; `frontend/src/` trang Lên kế hoạch) | số người, ngân sách, ngày đi, điểm muốn đi / muốn tránh | gõ tự do ⇒ lịch do code xếp: **đã thử 2 lần, chưa đạt** tiêu chí "hợp người đi cùng" ⇒ cờ `lich_trinh` tắt, đóng hồ sơ (tag `hoso/p9-t4-lich`); TRIPO cũng hỏng ở chính bước đổi câu ⇒ nhãn (mất "2 ngày", mất số người) |
| **Nguồn điểm** | cơ sở dữ liệu có cấu trúc: hàng nghìn điểm / nơi ăn / nơi ở có toạ độ, giờ mở – đóng, giá | **bảng 28 điểm** User duyệt (`diem_v3.json`; `lich_trinh.py` `nap_bang`): 16 di tích · 8 thiên nhiên · 6 ẩm thực · 4 chụp ảnh · 1 lễ hội nghệ thuật; mỗi điểm có cụm địa lý, buổi đi được, giờ mở cửa, lưu ý | bảng nhỏ; **không có độ ưu tiên** ("điểm phải đi"); loại "ẩm thực" chỉ là chợ / phố, không có món hay quán (kho có 81 bài quán + ~91 bài món); 24 / 28 điểm chưa có thời lượng | phiếu thời lượng v7 (19 / 26 điểm có số từ web) **chờ User duyệt từ 07/11**; cột "trong nhà / bậc thang" (phiếu v6) chờ User |
| **Chọn + xếp** | code lấy điểm theo nhãn, xếp **theo giờ** từ 07:30, có khoảng cách giữa điểm | code xếp **theo buổi** (`lich_trinh.py` `xep`): mỗi buổi một điểm, theo **thứ tự bảng** + cụm kề; nhóm có người lớn tuổi / trẻ em không có buổi tối; cụm xa chỉ khi ≥ 3 ngày | không giờ từng chặng; không thời gian di chuyển; "đi dày" không tác dụng; điểm nổi tiếng bị bỏ (mục 3) | "đi dày" ẩn khỏi biểu mẫu đợt 1 vì không đổi khung (0 / 120); 3 luật xếp "đi dày" C đề xuất 07/11 **chưa đo** |
| **Kiểm lịch** | thiếu: vòng 3 thấy xếp quá giờ đóng cửa 77 phút, kết thúc 23:12 cho nhà có trẻ nhỏ + người già | code kiểm khung + kiểm chữ model viết (`kiem_khung`, `kiem_cuoi`): không thêm điểm lạ, không giờ lạ, không nói ngược buổi tối; model từ chối ⇒ code dựng lời tối thiểu (`loi_lich_toi_thieu`) | — (**điểm hue_rag hơn**) | giữ |
| **Bữa ăn** | nhà hàng xếp vào lịch (có lần cùng một nhà hàng 3 bữa), nút đặt bàn | **không có** bữa ăn trong lịch biểu mẫu | bữa trưa / tối + gợi ý món, quán theo khu | chưa thử; phụ thuộc dữ liệu "quán ở khu nào" (cùng gốc việc "ăn gần") |
| **Chi phí** | giá từng điểm + **tổng tiền dự kiến** | **không** | tổng vé tham quan | **đã thử, bỏ**: bậc tính tiền B5c âm, đóng hồ sơ (tag `hoso/p9-b5c`) — không đề xuất lại khi chưa có bảng giá có cấu trúc |
| **Ngày / thời tiết / mùa** | chat không biết hôm nay; lịch không xét mưa | code biết ngày (`ngay_lich.py`), có công cụ thời tiết 7 ngày (`thoi_tiet.py`, bật) — **nhưng biểu mẫu không hỏi ngày đi** ⇒ lịch không dùng; lưu ý mùa chỉ hiện khi bảng có dòng lưu ý cho điểm đó | ngày đi trong biểu mẫu ⇒ lưu ý mưa / mùa cho điểm ngoài trời | thời tiết cho câu gõ tự do đã vào `main` 06–07/11 |
| **Bản đồ** | bản đồ 9 lớp, chỉ đường, "gần bạn" | link Google Maps từng điểm do code dựng (`map_url`, `ban_do`); **bản đồ ghim số theo thứ tự: code đã có, cờ `ban_do_lich` tắt** | toạ độ còn thiếu | **chờ phiếu toạ độ 11 điểm của User** (`data/phase_11/ban_do/phieu_toa_do_11_diem.md`) |
| **Sửa lịch** | trên lịch: đổi điểm, xoá, kéo thả; sửa bằng chat (không tìm lại dữ liệu, không kiểm lại ràng buộc cũ, sửa nhiều ý thì im lặng bỏ một ý) | nút "Sửa — điền lại biểu mẫu" (`frontend/src/chat.jsx`); sửa nhiều lượt bằng hành động có tên: **code trên nhánh `p9-sua-lich`, hoãn** | đổi / bỏ một điểm ngay trên lịch | hoãn vì cần cờ lịch trình câu tự do; bộ chuỗi sửa 10 + 5 đã viết, chưa đo |
| **Lưu / chia sẻ** | tải PDF, chia sẻ, đặt tên lịch | có nút sao chép / tải lịch (theo báo cáo B) | — | không thiếu đáng kể |
| **Nguồn + độ tin** | lịch không ghi nguồn từng điểm | mỗi điểm có mã trích dẫn tới bài kho + dòng "giờ mở cửa có thể đã thay đổi" + dòng "Mình hiểu: …" | — (**điểm hue_rag hơn**) | giữ |
| **Tốc độ** | hiểu câu ~32 s, dựng lịch 4–5 s, sửa 22 s; không hiện chữ dần | biểu mẫu: cả câu trung vị **4,9 s** (14 lượt hôm nay, dài nhất 8,1 s), ≈ 0,0004 USD / lịch | — (**điểm hue_rag hơn**) | giữ |

## 3. Kết quả đếm

### 3.1 Mô phỏng 0 USD — 360 tổ hợp biểu mẫu qua hàm `xep()` với bảng đang chạy [Chạy]

| Phép đếm | Kết quả |
|---|---|
| **Điểm không bao giờ được xếp** ở bất kỳ tổ hợp nào | **7 / 28**: ngôi chùa nổi tiếng nhất, 5 lăng vua (có hai lăng thuộc nhóm khách hay đi nhất) và một di tích khác |
| Lăng nổi tiếng nhất còn lại | xuất hiện ở **15 / 360** tổ hợp |
| Riêng 120 tổ hợp "thích di tích / không chọn sở thích" | ngôi chùa đó **0 / 120**; ba lăng lớn **0 / 120**; điểm số một của Huế 120 / 120 |
| Buổi có 2 điểm | **0 / 360** |
| "Kiểu đi" (thong thả ↔ dày) làm đổi khung | **0 / 120** nhóm |
| Có buổi tối | 36 / 360 (chỉ khi chọn ẩm thực và nhóm không hạn chế) |
| Số điểm | 2 điểm / ngày ở 324 / 360 tổ hợp (tối đa 8 điểm cho "từ 4 ngày") |

**Nguyên nhân [chứng minh, đọc `xep()`]:** điểm được chọn tham lam theo **thứ tự dòng trong bảng**; bảng xếp theo cụm địa lý (quanh Kinh thành ⇒ bờ nam ⇒ … ⇒ cụm lăng phía tây nam),
mỗi buổi một điểm ⇒ 8 suất của 4 ngày dùng hết ở các cụm đầu bảng, **không bao giờ tới cụm lăng**. Bảng không có cột nào nói "điểm này phải đi". Luật "đi dày" chỉ thêm điểm thứ hai
khi cả hai điểm cùng cụm và đều có thời lượng "ngắn" — bảng chỉ 1 / 28 điểm ghi "ngắn" (24 điểm để trống).

### 3.2 14 lịch thật qua biểu mẫu

| Hỏi | Kết quả |
|---|---|
| Ra lịch, qua kiểm của code | **14 / 14** (0 lượt bị rút, 0 lượt từ chối, 0 lỗi kiểm cuối) |
| Đúng số ngày, đúng nhóm người (không buổi tối cho nhóm hạn chế), có trích dẫn, có dòng "Mình hiểu" | 14 / 14 |
| Lịch "thích di tích" (2 và 3 ngày) có ngôi chùa nổi tiếng / một lăng lớn | **0 / 2**; tính cả 2 lịch không chọn sở thích (2 và 4 ngày): 0 / 4 |
| "Đi dày" khác "thong thả" | **0 / 5** yêu cầu "đi dày" có thêm điểm nào nhờ chọn dày (4 lịch 2 điểm / ngày; 1 lịch có thêm buổi tối do chọn ẩm thực) |
| Có giờ gợi ý từng chặng | 0 / 14 (chỉ có giờ mở cửa của điểm) |
| Có bữa ăn / món / quán | 0 / 14 — kể cả 3 lịch "thích ẩm thực" (chỉ có chợ, phố, rồi lấp bằng di tích) |
| Sở thích không đủ điểm ⇒ lấp di tích (có dòng ghi chú nói rõ) | 6 / 14 (lễ hội – nghệ thuật: bảng chỉ có 1 điểm; ẩm thực 3; chụp ảnh 4 — trùng danh sách thiên nhiên) |
| Lưu ý mùa cho điểm ngoài trời (hôm nay là mùa mưa) | có ở 2 lịch có thác (bảng có dòng lưu ý); **không có** ở lịch xếp bãi biển và ở các lịch có đầm phá / núi |
| Trình bày | 1 / 14 lịch model viết **mất dòng tiêu đề "Ngày …"** (4 ngày dính liền) — kiểm cuối không bắt; kiểu gạch đầu dòng mỗi lần một khác |
| Lịch trùng nhau | chỉ **18 / 28** điểm từng xuất hiện; mọi lịch thiên nhiên cùng một chuỗi điểm, mọi lịch di tích cùng một chuỗi điểm bất kể nhóm người |

**Dùng được không?** Dùng được ở mức "khung an toàn": không sai giờ, không bịa điểm, đúng nhóm người. **Chưa dùng được như một lịch du lịch Huế**: một lịch 3 ngày "thích di tích"
không có chùa và lăng nào thì khách sẽ không tin; không có bữa ăn; không có giờ.

### 3.3 3 yêu cầu gõ tự do (cờ lịch trình câu tự do đang tắt ⇒ trợ lý tự viết từ các bài trong kho, **không qua bộ xếp và bộ kiểm của code**)

- Có giờ đến / về: ra lịch **theo khung giờ**, có lăng, chùa, phố tối, bữa trưa — nội dung giàu hơn hẳn lịch biểu mẫu; **29,7 s** cả câu.
- Có điểm bắt buộc + món muốn ăn: xếp đúng điểm đó, nêu **một quán có địa chỉ** cho món đó; 19,8 s.
- Có ngân sách: kho từ chối, web không giúp; 32 s.
- ⇒ Nghịch lý hôm nay: người **gõ tự do** nhận lịch giàu hơn người **bấm biểu mẫu**, nhưng chậm gấp 4–6 lần và không được code kiểm (giờ, thứ tự, nhóm người). C chưa kiểm
  đúng / sai các lịch gõ tự do ngoài việc chúng có trích dẫn.

## 4. Ứng viên (xếp hạng **sau** khi đếm; đều là đề xuất, chưa có plan)

| # | Ứng viên | Loại | Lỗi đếm được | Lợi cho người dùng | Cần User làm gì | Ước |
|---|---|---|---|---|---|---|
| 1 | **Cột "ưu tiên" trong bảng điểm + luật chọn điểm ưu tiên trước rồi mới theo cụm** | dữ liệu + luật xếp | 7 / 28 điểm không bao giờ được xếp; chùa + 3 lăng lớn 0 / 120 | lịch có những nơi ai đến Huế cũng đi | **duyệt danh sách ~8–10 điểm "phải đi"** (C soạn phiếu từ bài cẩm nang trong kho) | ~2–3 giờ · ≤ 0,03 (đo: mô phỏng 360 tổ hợp 0 USD + 12 tổ hợp bộ quyết ×2) |
| 2 | **Thời lượng + luật "đi dày"** (2–3 điểm / buổi cùng cụm khi điểm ngắn) | dữ liệu + luật xếp | "đi dày" 0 / 120; 2 điểm / ngày ở 324 / 360 | "đi dày" có nghĩa; cụm lăng đi 2–3 lăng một buổi như thực tế | **duyệt phiếu thời lượng v7** (đang chờ từ 07/11; chọn dùng cả bảng / chỉ dòng chắc) | ~3 giờ · ≤ 0,03 |
| 3 | **Bữa ăn trong lịch**: mỗi ngày một dòng trưa / tối gợi ý món + quán theo khu của điểm buổi đó | dữ liệu + luật xếp | 0 / 14 lịch có bữa ăn; "thích ẩm thực" không có món nào | lịch giống lịch thật; dùng 81 bài quán sẵn có | chọn làm chung với việc "ăn gần" (cần dòng "quán ở khu nào" — plan nháp đã có); duyệt cách B của plan đó | ~4 giờ · ≤ 0,05 (sau khi có dữ liệu khu) |
| 4 | **Ngày đi trong biểu mẫu ⇒ lưu ý mùa / thời tiết + giờ gợi ý theo buổi** (khung giờ do code in, không phải model) | giao diện + luật xếp | 0 / 14 lịch có giờ; lịch mùa mưa vẫn xếp biển / đầm phá không lưu ý | lịch nói được "sáng 8:00–11:00", "mùa này biển động" | duyệt phiếu cột "trong nhà" v6 (để có phương án ngày mưa); đồng ý thêm 1 trường biểu mẫu | ~4 giờ · ≤ 0,05 |
| 5 | **Bật bản đồ lịch trình** (ghim số theo thứ tự) | giao diện | code có, cờ tắt | nhìn thấy đường đi trong ngày | **điền phiếu toạ độ 11 điểm** | ~1 giờ sau khi có phiếu · ≈ 0,005 |
| 6 | **Đổi / bỏ một điểm ngay trên lịch** (bản hẹp của sửa lịch: nút trên từng dòng, code xếp lại, báo "đổi gì / giữ gì") | giao diện + code | chưa đếm được (chưa có người dùng); TRIPO có | sửa không phải điền lại cả biểu mẫu | quyết có mở lại nhánh sửa lịch theo hướng nút bấm (không qua chat) | ~1 ngày · ≤ 0,1 (bậc đo đủ) |

**Không đề xuất (đã thử / chưa có nền):** tổng tiền trong lịch (bậc tính tiền âm 05/11; cần bảng giá có cấu trúc trước) · bật lịch trình câu gõ tự do (2 lần chưa đạt) · số người /
ngân sách trong biểu mẫu (không có luật nào dùng tới khi chưa có tiền) · lưu trú trong lịch (kho không có danh sách cơ sở).

**Thứ tự C gợi ý:** 1 ⇒ 2 (cùng chạm bảng + hàm `xep`, làm liền nhau; mỗi cái đo riêng) ⇒ 5 (rẻ, chỉ chờ phiếu) ⇒ 3 ⇒ 4 ⇒ 6. Việc 1 và 2 **đếm lại được 0 USD** bằng chính mô phỏng
360 tổ hợp ở mục 3.1 ⇒ tiêu chí ghi trước rẻ và chắc (vd: mọi lịch di tích ≥ 2 ngày có chùa + ≥ 1 lăng lớn; "đi dày" đổi khung ở ≥ một nửa số nhóm; 0 lịch vi phạm luật nhóm hạn chế).

**Ba phiếu đang chờ User quyết định trực tiếp tốc độ của mảng này:** thời lượng v7 · toạ độ 11 điểm · (mới) danh sách điểm ưu tiên.

## 4b. Kết quả Huế TRIPO do User chụp tối 12/11 (bổ sung 21:29 12/11/2026)

Nguồn: 5 ảnh chụp màn hình + 2 file trang lưu của User ở thư mục `data/tripo_v6_2026-11-12/user_chup/` (dời 14/11/2026) (**không commit**; nội dung trang là dữ liệu). C đọc cả 5 ảnh và phần chữ của 2 file.
Hai lượt User chạy: (A) 1 ngày · cân bằng · văn hoá – lịch sử · cặp đôi · ngân sách trung bình; (B) 2 ngày · nhẹ nhàng · sinh thái · 3 người lớn · trung bình + 8 lựa chọn thêm.

**Luồng của họ (mức chức năng):** biểu mẫu (kiểu đi 3 mức · loại hình 7 nhãn · đi cùng ai · người lớn / trẻ em + / − · số ngày + / − · ngày giờ khởi hành · ngân sách 3 mức) ⇒ bảng "tuỳ chọn thêm"
4 nhóm (tôn giáo · ưu tiên ẩm thực · hoạt động · dịch vụ đi kèm, ~30 nhãn) ⇒ thẻ tóm tắt tiêu chí ⇒ **ba phương án**, mỗi phương án bốn phần: một cơ sở lưu trú · ăn uống (xem theo sáng / trưa / tối) ·
4–6 điểm tham quan · đi chơi tối ⇒ "Bổ sung yêu cầu" / "Xác nhận phương án" ⇒ lịch theo buổi ⇒ trang lịch chi tiết: từng chặng có giờ bắt đầu – kết thúc, điểm đánh giá, địa chỉ, giờ hoạt động, khoảng giá,
chi phí dự kiến, số phút + km tới chặng sau, nút chi tiết / bản đồ / chỉ đường / thay đổi địa điểm / đặt bàn / thuyết minh; bảng chi phí theo ngày (tham quan · ăn uống · lưu trú · tổng); "Xem bản đồ" từng ngày.

**Chỗ họ hơn hue_rag hôm nay (thấy trong ảnh):** lịch có **đủ bốn phần** (ở · ăn theo buổi · tham quan · tối) trong khi lịch hue_rag chỉ có tham quan; có giờ từng chặng + quãng đường; có ba phương án để chọn;
có chi phí; lịch di tích 1 ngày của họ có đủ Đại Nội, chùa và lăng lớn — đúng các điểm hue_rag đang bỏ rơi.

**Lỗi / chỗ yếu thấy được trong chính hai lượt đó (quan sát một lần, không phải số đo):**

| Thấy gì | Ở lượt | Vì sao là lỗi |
|---|---|---|
| Chặng tham quan cuối kết thúc 17:39 ở một lăng; chặng trước đó là chùa 14:08–16:08 rồi đi 7,8 km | A | sát / quá giờ đóng cửa 17:30 mà kho hue_rag ghi cho quần thể lăng; phương án hứa 4 điểm, lịch cuối bỏ 1 lăng |
| Bữa trưa và bữa tối **cùng một nhà hàng** | A | lịch lặp, không giống gợi ý thật |
| Mục ăn uống là **chỗ giữ chỗ**: "Ăn sáng tại địa phương", "Ăn trưa quanh điểm tham quan", "Ăn tối quanh khu vực lưu trú" — vẫn hiện như một địa điểm có địa chỉ cấp huyện và giờ hoạt động 06:00–23:00 | B (và phương án 3 của A) | không phải quán nào cả nhưng trình bày như dữ liệu thật |
| "Đi chơi tối: Hoạt động tự do" | A (1 / 3 phương án), B (2 / 3 phương án) | phần buổi tối trống |
| Chọn thêm "tham quan di tích", "tham quan thành phố", "ẩm thực cung đình", "cần hướng dẫn viên" ⇒ lịch cuối toàn điểm một vùng núi xa trung tâm, không điểm di tích / thành phố nào, không nhắc hướng dẫn viên | B | lựa chọn hiện trên màn hình nhưng **không đổi lịch** — đúng loại lỗi hue_rag đặt nguyên tắc để tránh |
| Tóm tắt ghi "đi cùng: cặp đôi, bạn bè / nhóm bạn" với 3 người lớn; kiểu "nhẹ nhàng" nhưng phương án liệt kê 6 điểm | B | nhãn mâu thuẫn nhau vẫn được nhận |
| Lịch 1 ngày vẫn có khách sạn và 1,1 triệu tiền lưu trú; lượt 2 ngày ghi lưu trú 3,8 triệu cho khách sạn giá 0,6–1,3 triệu | A, B | cách tính không giải thích; người dùng không kiểm được |
| Mọi quán có giờ hoạt động y hệt 06:00–23:00 | A, B | nhiều khả năng là giá trị mặc định, không phải giờ thật |

**Kết quả hue_rag User dán cạnh (3 ngày · gia đình có trẻ em · ẩm thực):** 6 điểm, mỗi buổi một điểm; **không quán / bữa ăn nào** dù chọn ẩm thực; không lưu trú; không buổi tối; không ảnh — khớp các số ở mục 3
(0 / 14 lịch có bữa ăn; nhóm có trẻ em không có buổi tối). User hỏi thêm về **ảnh minh hoạ**: bộ ảnh cổng hiện có 7 ảnh (2 ảnh đầu trang + 5 ảnh lĩnh vực) ⇒ chỉ khoảng **3 / 28 điểm** có ảnh dùng lại được;
muốn mỗi điểm một ảnh phải dựng thêm bộ ảnh có nguồn + giấy phép (cách đã làm cho 7 ảnh hiện có).

**Hệ quả cho thiết kế** (đưa vào spec "Lên kế hoạch" bản 3): học phần **đủ bốn phần + giờ gợi ý + ảnh + bản đồ**; **không học** chỗ giữ chỗ, giờ mặc định, lựa chọn không đổi lịch, tiền không giải thích.

## 5. Lỗi và giới hạn

- 14 + 3 yêu cầu, một lượt, một người đọc; lịch gõ tự do chưa được kiểm đúng / sai.
- Mô phỏng 360 tổ hợp chỉ chạy hàm xếp (không gọi model) — phần chữ model viết chỉ thấy ở 14 lượt thật.
- Cột TRIPO lấy từ ghi chép vòng 3–5 (các vòng đó tự ghi giới hạn: không đăng nhập, không gửi biểu mẫu ở vòng 5).
- C không mở lại từng report của các bậc lịch trình cũ; lý do "đã thử / đã bỏ" lấy từ handoff, `Project_Status.md` và STATUS của C.

## 6. Bàn giao

- Private: `data/phase_11/dot_2_dem/cau_lich_trinh.jsonl` · `ket_qua_lich_trinh.jsonl` (17 dòng: câu trả lời + khung bản đồ + số đo). Mô phỏng 360 tổ hợp: đoạn script ngắn gọi
  `lich_trinh.nap_bang` + `xep` (chạy từ `backend/`, `PYTHONPATH=$PWD`), kết quả ghi ở mục 3.1 — chạy lại < 5 giây.
- Tiền C cả phiên 12/11: 0,058691 USD (đếm đợt 2 0,024691 · đếm thứ hai 0,023453 · lịch trình 0,010547).
