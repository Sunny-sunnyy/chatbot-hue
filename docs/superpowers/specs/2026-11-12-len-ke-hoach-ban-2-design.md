# Spec — "Lên kế hoạch" bản 2 của tính năng: một lịch đủ bốn phần, biểu mẫu đầy đủ, ảnh và bản đồ · bản 3.3 — ĐÃ DUYỆT 12/11/2026

**Trạng thái (A ghi 22:31 12/11/2026):** User chốt mức "đủ 4 phần, 1 lịch" + 4 quyết định theo khuyến nghị + phiếu gộp + phiếu nhỏ tối 12/11/2026; E review 2 vòng + kiểm mục 5c; A duyệt bản 3.3 (`8c521ecdc80d` lúc duyệt). Còn mở không chặn code: User liếc danh sách ưu tiên theo sở thích trước khi bật cờ.

Người viết: C. Bản 1 21:13, bản 2 21:22, **bản 3 21:32 12/11/2026** (`date`). Bản 3 = bản 2 (E đã `ready` ở vòng 2, sha `8969c7275346`) + **đổi phạm vi theo mức User chốt tối 12/11** sau khi User tự thử
hai hệ thống ("muốn hệ thống chúng ta làm tốt như Huế TRIPO"). E chỉ kiểm phần đổi (bảng cuối file). Chưa code. B code sau khi User duyệt.
Repo public: không chép chữ / bố cục của trang khác; tên điểm cụ thể nằm ở phiếu private.

## Căn cứ để review (`WORKFLOW.md` §9.1)

- Lượt đếm + bảng khoảng cách + kết quả TRIPO do User chụp: `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` (mục 2, 3, 4b).
- Code đang chạy: `backend/llm/lich_trinh.py` (`ThamSo`, `xep`, `_cum_hop`, `HAN_CHE`, `kiem_khung`, `kiem_cuoi`, `ban_do`) · `backend/llm/hoi_lai.py` (`GIA_TRI`, `TruongInput`) ·
  `backend/llm/assistant.py` (`answer_bieu_mau`) · `backend/llm/thoi_tiet.py`, `ngay_lich.py` · `frontend/src/pages.jsx` (`LenKeHoach`), `chat.jsx` (thẻ lịch), `BanDoLich.jsx`, `anh.js`.
- Tài liệu liên quan: spec cổng đợt 1 (D3, D4, §6 Q-F) · plan điểm ưu tiên `docs/superpowers/plans/2026-11-12-lich-trinh-diem-uu-tien-plan.md` · plan lưu trú
  `docs/superpowers/plans/2026-11-12-luu-tru-khu-va-link-plan.md` · spec bổ sung kho 3 `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` · plan bản đồ `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md`.
- Dữ liệu (private): phiếu gộp `data/phase_9/lich_trinh/phieu_gop_cho_user_2026-11-12.md` · bảng quán `data/sua_kho_2026-11-12_an_gan/bang_de_xuat.md`.

## 1. Mục tiêu, phạm vi User chốt, nguyên tắc

**Mục tiêu:** bấm biểu mẫu ra **một lịch dùng được như lịch thật**: mỗi ngày có **tham quan · ăn uống theo buổi · chỗ ở · buổi tối**, có giờ gợi ý, ảnh và bản đồ — và mỗi điều người dùng chọn làm lịch
khác đi một cách kiểm được.

**Hôm nay (đếm 12/11):** biểu mẫu 3 hàng; lịch chỉ có tham quan, mỗi buổi một điểm; 0 / 14 lịch có bữa ăn; không chỗ ở; buổi tối chỉ khi chọn ẩm thực; không ảnh; bản đồ có code nhưng tắt;
7 / 28 điểm không bao giờ được xếp; "kiểu đi" đổi khung 0 / 120.

**Phạm vi cam kết của mốc này (User chốt tối 12/11, A báo) — cả mức này là cam kết, chia 3 đợt nối nhau, mỗi đợt merge được riêng:**

| Trong mốc (làm trước đóng code 25–30/12) | Sau mốc đóng code (ghi lại, **không thiết kế ở đây**) |
|---|---|
| Lịch **đủ 4 phần**: tham quan · ăn uống theo buổi · lưu trú · buổi tối | Ba phương án để chọn + "bổ sung yêu cầu" / xác nhận |
| Biểu mẫu đầy đủ: số người (người lớn, trẻ em, có người lớn tuổi) · số ngày + / − · ngày đi · kiểu đi 3 mức · thích gì | Chế độ ngân sách / tổng chi phí |
| **Ảnh minh hoạ** mỗi điểm | Mục riêng Lưu trú · Ăn uống · Dịch vụ (tìm kiếm ngoài lịch) |
| **Bản đồ** lịch trình | Đổi / bỏ một điểm ngay trên lịch; kéo thả |
| Giờ gợi ý theo buổi do code in | Bảng "tuỳ chọn thêm" nhiều nhãn (tôn giáo, kiểu ẩm thực…) |

Khung: **2–3 tuần làm, dưới 1 USD**; đợt bổ sung kho 3 phải xong trước phần ăn uống + lưu trú.

| # | Nguyên tắc | Hệ quả |
|---|---|---|
| N1 | **Ô nào hiện thì phải đổi được lịch.** | mỗi ô ở mục 3: code dùng ở đâu, dữ liệu gì, đo bằng mô phỏng 0 USD; dưới sàn ⇒ ô không hiện |
| N2 | **Phép tính, luật, giờ, chọn quán, chọn ảnh ⇒ code;** model chỉ diễn đạt khung. | model không thêm số, không chọn ảnh, không bịa quán; không nói giá phòng |
| N3 | **Nói thật khi thiếu dữ liệu** — không dùng chỗ giữ chỗ trông như dữ liệu. | phần nào của ngày không có dữ liệu đủ điều kiện ⇒ một dòng nói rõ, không tên giả, không giờ mặc định |
| N4 | **Giao diện riêng của hue_rag**: học chức năng, không chép bố cục / chữ / màu. | mục 5; giữ CSP, 0 gói mới (bản đồ dùng gói đã duyệt ở plan bản đồ) |
| N5 | Bảng rà khung AI FDE; tiêu chí ghi trước từng đợt. | mục 6, 7 |

## 2. Chỗ hue_rag phải HƠN Huế TRIPO (từ chính hai lượt User chụp 12/11 — báo cáo mục 4b)

| Thấy ở TRIPO | hue_rag làm thế nào | Kiểm bằng |
|---|---|---|
| Chặng tham quan kết thúc sát / quá giờ đóng cửa; hứa 4 điểm, lịch cuối bỏ 1 | giờ gợi ý do code in **trong giờ mở cửa** của từng điểm (bảng có sẵn cột giờ); số điểm một buổi theo thời lượng | bất biến: 0 khung giờ nằm ngoài giờ mở cửa |
| Bữa trưa và tối cùng một nhà hàng | một quán không lặp trong cùng lịch | bất biến: 0 quán lặp |
| "Ăn sáng tại địa phương", "Ăn trưa quanh điểm tham quan" hiện như một địa điểm có giờ 06:00–23:00 | không có quán đủ điều kiện ⇒ một dòng nói thật + gợi ý **món** có bài trong kho; không tên giả, không giờ mặc định | bất biến: mọi tên quán trong lịch có trong bảng quán được duyệt |
| "Đi chơi tối: hoạt động tự do" | buổi tối xếp từ bảng điểm buổi tối theo đúng thứ hoạt động; không có ⇒ dòng "tối nghỉ" kèm lý do (đã có cơ chế) | bất biến: 0 điểm tối sai thứ |
| Chọn thêm tiêu chí nhưng lịch không đổi; hai nhãn mâu thuẫn vẫn nhận | N1 + biểu mẫu chặn tổ hợp mâu thuẫn (số người thay cho nhãn "một mình / cặp đôi / nhóm") | sàn "đổi lịch" từng ô |
| Điểm trong một ngày cách nhau xa (chặng 7,8 km cuối ngày) | luật cụm kề đang có: ≤ 2 cụm một ngày, không ghép cụm không kề | bất biến: 0 ngày ghép cụm không kề |
| Tiền lưu trú / tổng tiền không giải thích được | mốc này **không in tiền**; chỗ ở chỉ là khu + (khi kho có) tên cơ sở, không giá | bất biến: 0 số tiền do model viết |
| Lịch không ghi nguồn | mỗi điểm, mỗi quán có mã trích dẫn tới bài kho; dòng "Mình hiểu: …" | kiểm cuối (đang có) |

Chỗ TRIPO hơn mà mốc này **chưa** đuổi: ba phương án, chi phí, hàng nghìn cơ sở có đánh giá, đổi điểm trên lịch, chỉ đường từng chặng.

## 3. Từng phần: code dùng thế nào · cần dữ liệu gì · đo ra sao

**Cách đọc cột "Tiêu chí" — hai lớp, chốt NGAY ở spec này:**
- **Bất biến ("Luôn", phải đúng 100 % tổ hợp):** sai một tổ hợp ⇒ luật sai, sửa code.
- **Sàn "có tác dụng" (số %):** là **sàn sản phẩm**; plan từng đợt **chỉ được nâng, không được hạ**. Đo ra dưới sàn ⇒ **ô đó không hiện** ở đợt ấy — không hạ ngưỡng, không chỉnh rồi đo lại quá một vòng.
- Mô phỏng **trước khi code** chỉ để **đếm dữ liệu**. Số đếm hôm nay (bảng 28 điểm + thời lượng đề xuất ở phiếu gộp, User chưa duyệt): thời lượng "ngắn" 12 · "nửa buổi" 14 · chưa có 2;
  **4 / 8 cụm có ≥ 2 điểm ngắn**, 3 cụm không có điểm ngắn nào ⇒ ở các cụm đó ba mức kiểu đi cho cùng một khung — **việc đầu tiên của plan đợt 1 là đếm xem sàn 70 % có đạt được không**
  (ghi chú của E ở vòng 2); loại điểm: di tích 16 · thiên nhiên 8 · ẩm thực 6 · chụp ảnh 4 (đúng ngưỡng) · lễ hội – nghệ thuật 1 (lên 4 nếu User nhận 5 điểm trong nhà ở phiếu gộp); nhiều bậc thang
  11 điểm; chỉ buổi tối 3 điểm; có lưu ý mùa 2 / 28 (kho: 30 / 30 bài điểm có cảnh báo mùa kèm tháng); **ảnh dùng lại được từ bộ ảnh cổng: ~3 / 28 điểm** (bộ hiện có 7 ảnh);
  quán có toạ độ: 29 / 81 bài (7 chắc, 22 ước), dồn ở bờ nam.

### 3.1 Các ô của biểu mẫu (đợt 1)

| Ô (trường) | Giá trị | Code dùng ở đâu | Dữ liệu cần | Tiêu chí |
|---|---|---|---|---|
| Số ngày (`so_ngay`) | 1–5, nút + / − (nhận "4+" cũ = 4) | số ngày của khung; cụm xa chỉ từ 3 ngày (luật cũ) | bảng đủ điểm cho 5 ngày | **Luôn:** khung n ngày có đúng n ngày, mỗi ngày ≥ 1 điểm, 0 điểm lặp |
| Trẻ em (`tre_em`) | 0–6 | ≥ 1 ⇒ luật nhóm hạn chế (không tối muộn, ≤ 2 suất tham quan / ngày) + tránh điểm "nhiều bậc thang" khi cùng cụm có điểm thay | cột bậc thang (phiếu gộp) | **Luôn:** có trẻ em ⇒ 0 điểm tham quan buổi tối. **Sàn:** số điểm nhiều bậc thang giảm ở ≥ 50 % tổ hợp so với 0 trẻ em |
| Có người lớn tuổi (`lon_tuoi`) | có / không | như trẻ em + ưu tiên điểm không nhiều bậc thang trong cùng mức ưu tiên | như trên | như trên; điểm mức 1 bị thay vì bậc thang ⇒ có dòng ghi chú do code nối |
| Người lớn (`nguoi_lon`) | 1–10 | chỉ vào dòng "Mình hiểu" và lời văn (một mình / đi nhóm). **Ngoại lệ có chủ ý của N1** — User đã chốt biểu mẫu có số người; ô này sẽ có tác dụng khi làm chi phí (sau mốc) | — | **Luôn:** đổi `nguoi_lon` ⇒ khung giống hệt, chỉ dòng "Mình hiểu" khác |
| Kiểu đi (`kieu_di`) | nhẹ nhàng · cân bằng · khám phá nhiều | số điểm mỗi buổi tính **bằng phút** theo mục 5c.3 (nhẹ nhàng 1 điểm; cân bằng quỹ 210 phút; khám phá nhiều quỹ 240 phút; tối đa **2 điểm / buổi, 4 điểm / ngày**). Nhóm hạn chế: trần là "nhẹ nhàng" (ghi chú do code) | **thời lượng** (phiếu gộp) | **Luôn:** **tổng** số điểm của cả lịch nhẹ nhàng ≤ cân bằng ≤ khám phá nhiều (theo từng ngày thì không giữ được: mức dày dùng hết điểm cùng cụm sớm hơn — mô phỏng 5 / 60 nhóm); nhóm hạn chế không vượt trần. **Sàn:** 3 mức cho 3 khung khác nhau ở ≥ 70 % nhóm không hạn chế |
| Thích gì (`so_thich`) | tối đa 2 trong các loại đủ điểm | điểm hợp loại được chọn trước (sau điểm ưu tiên), xen kẽ hai loại; chọn "ẩm thực" ⇒ phần ăn uống (3.3) thêm một bữa xế / món đặc sản mỗi ngày | nhãn loại của bảng | **Luôn:** chọn 2 loại ⇒ cả hai có mặt trong lịch từ 2 ngày; loại dưới 4 điểm không hiện (tính theo bảng lúc khởi động; có test). **Sàn:** mỗi loại chiếm ≥ 50 % suất sáng / chiều của lịch 2 ngày |
| Ngày đi (`ngay_di`) | ngày, không bắt buộc, hôm nay tới + 180 ngày | (a) thứ trong tuần ⇒ điểm buổi tối chỉ xếp đúng tối hoạt động; (b) tháng ⇒ điểm tạm dừng đón khách theo mùa không được xếp + một dòng nhắc mưa chung khi đi tháng 9–12 (mục 5c.2); (c) trong 7 ngày tới ⇒ gọi dự báo (code đã có), ngày mưa ⇒ ưu tiên điểm trong nhà / cả hai | cột `ngay_hoat_dong` (3 điểm tối — 3 bài kho ghi thứ hoạt động) · cột `mua_luu_y` theo tháng (dựng từ kho, **đưa vào phiếu User**) · cột trong nhà (phiếu gộp) | **Luôn:** 0 điểm tối sai thứ; ngoài 7 ngày ⇒ không có dòng dự báo; 0 điểm tạm dừng theo mùa được xếp trong tháng dừng; đi tháng 9–12 ⇒ có đúng một dòng nhắc mưa. **Sàn:** đổi ngày giữa "mùa khô, giữa tuần" ↔ "mùa mưa, cuối tuần" ⇒ khung hoặc ghi chú khác ở ≥ 60 % tổ hợp có điểm ngoài trời / buổi tối |
| Điểm ưu tiên (không phải ô) | cột `uu_tien` của bảng — **theo từng sở thích** (User chốt 12/11: "thích di tích thì gợi ý Đại Nội, thích thiên nhiên thì Bạch Mã"): mỗi loại 3–4 điểm "phải có" xếp thứ tự; không chọn sở thích ⇒ nhóm nổi tiếng chung | điểm ưu tiên của sở thích được chọn đứng đầu thứ tự xét (mục 5c.1, 5c.4) | bảng đề xuất v8 (private) | **Luôn:** điểm ưu tiên số 1 của sở thích có mặt trong lịch (trừ điểm cụm xa khi đi < 3 ngày); 0 lỗi khung. Mô phỏng trên v8: 30 / 30 nhóm ở cả 6 lựa chọn sở thích |

### 3.2 Bốn phần của một ngày trong lịch

| Phần | Code làm gì | Dữ liệu cần | Tiêu chí | Đợt |
|---|---|---|---|---|
| **Tham quan** (sáng, chiều) | như hôm nay + ưu tiên + kiểu đi; **giờ gợi ý theo buổi do code in** (vd sáng 8:00–11:00, chiều 14:00–17:00, chia theo số điểm và thời lượng, cắt theo giờ mở cửa) | thời lượng, giờ mở cửa (bảng có) | **Luôn:** 0 khung giờ ngoài giờ mở cửa; 0 ngày ghép cụm không kề; giờ các điểm trong buổi không chồng nhau | 1 |
| **Buổi tối** | nhóm không hạn chế: mỗi tối một hoạt động từ bảng điểm buổi tối đúng thứ + cùng cụm / cụm kề với khu trung tâm; nhóm hạn chế: dòng "tối nghỉ" kèm lý do (đang có) — hoặc một hoạt động nhẹ nếu bảng đánh dấu "hợp gia đình" | 3 điểm tối đang có + **1 hoạt động thêm có đủ giờ + thứ trong kho** (ca Huế trên sông Hương — diễn hằng đêm) + 1 ứng viên chờ User điền giờ (phố đêm cạnh Kinh thành); các chương trình khác trong kho không có lịch cố định ⇒ không thêm (số đếm: phiếu nhỏ đợt 1). **Giới hạn đã biết: buổi tối ít đa dạng** | **Luôn:** 0 hoạt động tối sai thứ / sai giờ diễn; nhóm có trẻ em không có điểm sau 21:00. **Sàn:** ≥ 80 % số tối của lịch nhóm không hạn chế có hoạt động (hôm nay: chỉ khi chọn ẩm thực) | 1 |
| **Ăn uống theo buổi** | mỗi ngày: **trưa** = 1–2 quán gần điểm sáng / chiều; **tối** = 1–2 quán gần khu trung tâm / điểm tối; **sáng** = gợi ý 1–2 món sáng đặc trưng có bài trong kho (+ quán nếu có gần khu ở). Chọn theo cụm + khoảng cách, không lặp quán trong lịch; mỗi quán một dòng: tên — món chính — mã trích dẫn | bảng `quan_theo_cum.json` của **đợt bổ sung kho 3** (trường theo spec đó: tên, địa chỉ, cụm, nguồn kho / dữ liệu mở, mức toạ độ chắc / vừa / ước, bài kho, điểm gần, khoảng cách; tên cụm = tên cụm của bảng điểm; Q3 / Q4 quyết bao nhiêu quán) + bài "ăn quanh điểm tham quan". Quán nguồn dữ liệu mở "chưa kiểm" ⇒ lịch ghi nhãn đó cạnh tên; toạ độ ước ⇒ chỉ dùng ở mức "cùng cụm", không in mét | **Luôn:** mọi quán thuộc bảng được duyệt, không lặp; quán toạ độ **chắc / vừa** ⇒ ≤ 1,5 km điểm / khu của buổi đó; quán toạ độ **ước** ⇒ điều kiện là **cùng cụm** với điểm / khu của buổi đó (không so mét, không in mét); không có quán đủ điều kiện ⇒ dòng nói thật + gợi ý món, **không tên giả**. **Sàn (User đã chốt Q3 thêm quán dữ liệu mở + Q4 hai mức toạ độ ở spec kho 3 ⇒ chỉ còn một mức):** ≥ 80 % bữa trưa + tối của ngày ở **cụm trung tâm** có tên quán. "Cụm trung tâm" được tính sàn = `kinh_thanh`, `bo_nam` + cụm nào khác có ≥ 2 quán đủ điều kiện theo lượt chạy thử số quán của spec kho 3 (danh sách chốt trong plan đợt 3 **trước khi code**; hai cụm đầu không được bớt). **Không tính sàn:** các cụm lăng (`thuy_xuan`, `lang_xa`) — cả kho lẫn dữ liệu mở đều 0 quán ⇒ ngày ở cụm đó dùng dòng nói thật + gợi ý món | 3 |
| **Lưu trú** | lịch ≥ 2 ngày: một khối "Ở đâu" = khu nên ở **hợp với cụm điểm của lịch** (khu chứa nhiều điểm nhất) + link bản đồ do code dựng (plan lưu trú — đường kích hoạt thứ hai, E sửa plan đó) + **khi kho đã có bài lưu trú**: 2–3 cơ sở của khu đó theo hạng, có mã trích dẫn, **không giá** | bảng khu (plan lưu trú, User duyệt; bảng ánh xạ 8 cụm ⇒ 3 khu nằm ở trường `cum` của `khu_v1.json` thuộc plan đó — E giữ, spec này chỉ đọc) + bảng `luu_tru_theo_cum.json` và bài lưu trú của đợt bổ sung kho 3 (Q1, Q2; danh mục nguồn có 0 homestay ⇒ khối "Ở đâu" nói rõ chỉ gồm cơ sở đã đăng ký) | **Luôn:** lịch ≥ 2 ngày có khối "Ở đâu", lịch 1 ngày không có; 0 số tiền; mọi cơ sở nêu tên có trong bài kho. **Sàn:** khu được chọn chứa hoặc kề ≥ 50 % số điểm của lịch | 3 (khối khu + link có thể vào sớm cùng plan lưu trú) |

### 3.3 Ảnh và bản đồ (đợt 2 — không phụ thuộc luật xếp)

| Phần | Code làm gì | Dữ liệu cần | Tiêu chí |
|---|---|---|---|
| **Ảnh minh hoạ** | mỗi điểm trong lịch hiện một ảnh nhỏ **do code gắn theo id điểm** từ bảng ảnh (model không chọn, không tả ảnh); ảnh nằm trong bản build như bộ ảnh cổng (CSP không đổi); dưới ảnh có tác giả + giấy phép; điểm chưa có ảnh ⇒ không ảnh (không dùng ảnh thay thế) | **bảng ảnh theo id điểm**: hôm nay ~3 / 28 điểm dùng lại được ⇒ agent tìm ảnh trên kho ảnh giấy phép mở (như đã làm cho 7 ảnh cổng), điền sẵn **phiếu ảnh** (ảnh · điểm · tác giả · giấy phép · link nguồn) cho User xem lướt; ảnh thu nhỏ bằng công cụ sẵn có | **Luôn:** mỗi ảnh hiện ra có trong bảng ảnh được duyệt, đúng id điểm, có dòng tác giả + giấy phép; 0 ảnh từ link ngoài. **Sàn:** ≥ 70 % điểm của bảng có ảnh thì bật; dưới ⇒ chưa bật |
| **Bản đồ lịch trình** | ghim số theo thứ tự trong ngày (code đã có, cờ tắt); bổ sung: mỗi ngày một màu / một lớp | toạ độ 28 điểm (phiếu gộp bảng D) | **Luôn:** mọi ghim là điểm của lịch, đúng thứ tự; điểm thiếu toạ độ ⇒ ghi chú, không ghim đoán. Theo tiêu chí plan bản đồ đã duyệt |

## 4. Ba đợt nối nhau (mỗi đợt merge được riêng; cả ba là cam kết của mốc)

| | **Đợt 1 — khung lịch tốt + biểu mẫu đủ** | **Đợt 2 — nhìn thấy được** | **Đợt 3 — đủ bốn phần** |
|---|---|---|---|
| Có gì | điểm ưu tiên · kiểu đi 3 mức · số ngày + / − · người lớn / trẻ em / lớn tuổi · ngày đi (thứ, mùa, dự báo) · **buổi tối** · giờ gợi ý theo buổi | **ảnh** mỗi điểm · **bản đồ** | **ăn uống theo buổi** · **lưu trú** trong lịch |
| Điều kiện vào | User xem xong phiếu gộp + phiếu nhỏ (thứ hoạt động, tháng lưu ý mùa, hoạt động buổi tối) | phiếu ảnh User duyệt + toạ độ ở phiếu gộp; **làm song song đợt 1 được** (chạm phần hiển thị, không chạm luật xếp) | đợt 1 đã merge + **đợt bổ sung kho 3 đã vào kho** (User trả lời Q1–Q5 của spec đó) + bảng khu của plan lưu trú |
| Chạm | bảng điểm (v8 / v9) · `lich_trinh.py` · `hoi_lai.py` · `assistant.py` · `pages.jsx` · test | bảng ảnh + ảnh trong `frontend/public/` · `chat.jsx` (thẻ lịch) · `BanDoLich.jsx` · cờ bản đồ · danh sách chừa Docker | bảng quán theo cụm · khung thêm bữa ăn + khối "Ở đâu" · `lich_trinh.py` · `chat.jsx` · module lưu trú |
| Ước giờ (agent làm việc) | 4–5 ngày (luật xếp là phần dễ sai nhất: code, mô phỏng, review riêng) | 3 ngày (phần lớn là tìm + kiểm giấy phép ảnh) | 4–5 ngày, **sau** ~2–3 ngày của đợt bổ sung kho 3 |
| Ước tiền | ≤ 0,20 USD | ≤ 0,05 USD | ≤ 0,25 USD (+ đợt kho 3 riêng ≤ 0,25) |
| Lịch dự kiến | tuần 1 | tuần 1–2 (song song) | tuần 2–3 |

**Tổng: ~2–3 tuần, ≤ 0,75 USD (kể cả đợt kho 3)** — trong khung User chốt (< 1 USD). Còn dư ~1 tuần trước 25/12 cho lượt đo cuối B7 chạy trên bản có đủ ba đợt.
**Thứ tự cắt nếu trễ (ghi trước):** ảnh ⇒ lưu trú mức "có tên cơ sở" (giữ mức khu + link) ⇒ bữa sáng. Không cắt: điểm ưu tiên, kiểu đi, buổi tối, bữa trưa / tối, bản đồ.
Mỗi đợt một plan riêng (viết ngay sau khi User duyệt spec), một nhánh, một review cả nhánh; phần luật xếp review riêng.

## 5. Giao diện + hợp đồng dữ liệu

- **Biểu mẫu — một trang, bốn nhóm theo câu hỏi người đi tự đặt:** "Ai đi?" (người lớn, trẻ em bằng nút + / −; ô đánh dấu "có người lớn tuổi") · "Đi bao lâu, khi nào?" (số ngày + / −; ô chọn ngày
  của trình duyệt, để trống được) · "Đi kiểu nào?" (3 nút, mỗi nút một dòng giải thích bằng số điểm một ngày: khoảng 2 / khoảng 3 / tới 4) · "Thích gì?" (chọn tối đa 2). Dưới cùng: dòng tóm tắt + nút xếp lịch. Lựa chọn nào
  không có tác dụng với tổ hợp hiện tại (vd "khám phá nhiều" khi có trẻ em) ⇒ hiện dòng nhỏ nói rõ.
- **Lịch — mỗi ngày một khối:** hàng trên là các buổi (sáng · trưa · chiều · tối) theo thứ tự thời gian, mỗi mục: giờ gợi ý — tên — một câu — mã nguồn — ảnh nhỏ (tham quan); khối "Ở đâu" một lần cho
  cả lịch; bản đồ dưới lịch, chọn theo ngày; khối "Ghi chú của lịch" (đang có) gom lưu ý mùa, dự báo, phần thiếu dữ liệu. Giữ nút "Sửa — điền lại biểu mẫu".
- **Kỹ thuật:** phần tử HTML sẵn có (`button`, `input type="date"`, `input type="checkbox"`); **0 gói npm mới** ngoài gói bản đồ đã duyệt ở plan bản đồ; CSP như hôm nay (bản đồ: như plan bản đồ);
  dùng được bằng bàn phím; khổ điện thoại một cột. Kiểm Playwright một khổ điện thoại + một khổ máy tính trên bản build do FastAPI phục vụ.
- **Hợp đồng `truong` (server kiểm, trường lạ ⇒ 422):** `so_ngay` "1"–"5" (và "4+" cũ) · `nguoi_lon` 1–10 · `tre_em` 0–6 · `lon_tuoi` bool · `kieu_di` `nhe_nhang` / `can_bang` / `kham_pha`
  (nhận tên cũ) · `so_thich` danh sách ≤ 2 (nhận chuỗi đơn cũ) · `ngay_di` ngày ISO, không ở quá khứ, ≤ 180 ngày. `di_cung` cũ vẫn nhận, code đổi sang trường mới.
- **Dữ liệu trả về:** khung có cấu trúc (ngày ⇒ buổi ⇒ mục: loại, id, giờ gợi ý, mã nguồn, id ảnh, toạ độ) do code dựng — giao diện vẽ lịch, ảnh, bản đồ **từ khung**, không từ chữ model.
- **Lời model:** vẫn một lần gọi, không công cụ, chỉ viết câu mô tả cho từng mục của khung. Mọi dòng có số (giờ, khoảng cách, lưu ý mùa, dự báo) do code nối; kiểm cuối thêm luật "chữ model không chứa
  giờ / số tiền / tên quán / tên cơ sở ngoài tập của khung".
- **Dữ liệu người dùng:** lựa chọn + một ngày; không tên, không liên hệ; không lưu ngoài RAM của phiên; log chỉ thêm số đếm.

## 5b. Thứ tự ưu tiên giữa các luật xếp + ghi chú thực thi (thêm 21:32 12/11/2026 theo góp ý của B — người sẽ code)

**Thứ tự ưu tiên khi hai luật kéo ngược nhau (cao ⇒ thấp; luật thấp chỉ được chọn trong phần luật cao còn cho phép):**
1. **An toàn của nhóm hạn chế** (trẻ em, người lớn tuổi): không buổi tối muộn, trần số suất, tránh bậc thang khi có điểm thay.
2. **Giờ mở cửa + thứ hoạt động** của điểm (không xếp điểm đóng cửa / sai tối).
3. **Cụm kề** (≤ 2 cụm một ngày, không ghép cụm không kề; cụm xa chỉ từ 3 ngày).
4. **Điểm ưu tiên** (mức 1 rồi mức 2).
5. **Dự báo mưa** (ngày mưa: điểm không ưu tiên xét trong nhà trước; không loại điểm ưu tiên — chỉ thêm dòng "nếu mưa"). Điểm **tạm dừng theo mùa** thuộc bậc 2 (như điểm đóng cửa).
6. **Sở thích** (≤ 2 loại, xen kẽ).
7. **Kiểu đi** (số suất mỗi buổi theo thời lượng).
8. Phần phụ thuộc khung tham quan: buổi tối ⇒ ăn uống ⇒ khối "Ở đâu" (chọn **sau** khi khung tham quan đã chốt, không làm đổi khung tham quan).
Mỗi luật một test riêng + test các cặp xung đột kề nhau trong thứ tự trên; mô phỏng toàn tổ hợp kiểm bất biến.

**Ghi chú thực thi (B nêu, C nhận):**
- **Khuôn khung gửi model và kiểm cuối** hiện giả định mỗi buổi một điểm ⇒ nhiều điểm một buổi + dòng bữa ăn + dòng buổi tối là **đổi khuôn** — chỗ hai lần trước model viết lệch / từ chối. ⇒ plan đợt 1 có
  **một lượt thử có phí sớm (≤ 0,005 USD)** ngay khi khung mới in ra được, trước khi viết đủ test; kiểm cuối viết lại theo khung có cấu trúc (mục 5 "Dữ liệu trả về").
- **Trường cũ** (`di_cung`, "4+", `thong_tha` / `day_lich`, `so_thich` chuỗi đơn): nhận **tới hết mốc đóng code**; gỡ ở đợt dọn sau mốc. Các bộ mốc cờ tắt (giống byte, bộ quyết cũ) giữ nguyên giá trị cũ.
- **Lượt có gọi dự báo** đo riêng **lúc bộ đệm lạnh** (lần gọi mạng đầu); tiêu chí "không chậm hơn mốc quá 2 giây" áp cho lượt không dự báo; lượt dự báo lạnh: ghi số, sàn riêng ≤ mốc + 4 giây.
- **Thứ tự merge trong đợt 1** (mỗi cái một nhánh nhỏ, cờ tắt, giống byte khi tắt): (a) hợp đồng `truong` mới + biểu mẫu mới với `xep` cũ — ô chưa có tác dụng thì **chưa hiện** (`/api/tinh_nang`);
  (b) bảng v8 / v9 + `xep` mới + mô phỏng; (c) khuôn khung / kiểm cuối mới + lượt thử; (d) ngày đi; (e) buổi tối + giờ gợi ý.
- **Ảnh** phải đóng gói vào bản build như 7 ảnh cổng (không nạp nóng từ trang khác ⇒ CSP không đổi); 28–33 ảnh ⇒ bản build tăng ~2–4 MB — ghi mức trần ở plan đợt 2. **Bản đồ:** ô bản đồ tải từ máy chủ
  bản đồ ⇒ trình duyệt người dùng lộ địa chỉ IP cho bên đó ⇒ có **một dòng báo** cạnh bản đồ (và ở trang giới thiệu). Toạ độ hôm nay có 17 / 28 điểm; đủ 28 sau khi User xem bảng D của phiếu gộp.
- Ước của B cho đợt 1: sát khi thứ tự luật + khuôn khung đã chốt (đã ghi ở trên); chưa chốt thì thêm ~1 ngày.

## 5c. Tám quyết định để code đợt 1 (bản 3.2, 21:47 12/11/2026 — B nêu chỗ thiếu, A giao C chốt bằng số)

Mọi con số dưới đây là **giá trị ghi trước**; số nào đã có mô phỏng thì ghi kèm. Bản thử luật chỉ là script đếm của C ở `data/` (không phải code sản phẩm) — B viết lại trong `backend/` theo đúng chữ ở đây.

### 5c.1 Bảng điểm: các cột (v8 đề xuất ⇒ v9)

- **v8** (C đã dựng bản đề xuất, private; 33 điểm = 28 cũ + 5 điểm trong nhà User nhận) = mọi cột của bảng đang chạy **+**:
  `thoi_luong` bắt buộc, chỉ `ngan` / `nua_buoi` (**không còn rỗng**) · `thoi_luong_nguon` `kho` / `web` / `uoc` (7 / 24 / 2 điểm) · `trong_nha` `trong_nha` / `ngoai_troi` / `ca_hai` (bắt buộc) ·
  `trong_nha_nguon` · `bac_thang` `nhieu` / rỗng · `uu_tien` = bảng `{khoá sở thích hoặc "chung": thứ tự 1–4}` (rỗng = không ưu tiên) · `uu_tien_can_cu`.
- **v9** (sau khi User xem phiếu nhỏ đợt 1) thêm: `ngay_hoat_dong` = danh sách thứ được xếp (rỗng = mọi ngày) · `gio_toi` = giờ in cho điểm buổi tối ("19:00–20:00") ·
  `mua_luu_y` = `{thang: [...], cau: "...", bo_khoi_lich: true / false}` · một dòng mới cho hoạt động buổi tối (ca Huế trên sông), loại `le_hoi_nghe_thuat`, `buoi: ["toi"]`.
- Số điểm mỗi loại trên v8: di tích 18 · thiên nhiên 8 · ẩm thực 6 · chụp ảnh 4 · lễ hội – nghệ thuật 4 ⇒ **cả 5 loại đều hiện** (ngưỡng ẩn < 4 User đã chốt); chụp ảnh và lễ hội đứng đúng ngưỡng.
- `nap_bang` kiểm lúc khởi động: thiếu cột bắt buộc của v8 ⇒ không khởi động khi cờ bật; thiếu cột v9 ⇒ ô "ngày đi" tự ẩn (mục 7).

### 5c.2 Luật mùa và luật mưa

- **Xét theo từng NGÀY của lịch** (không theo buổi — dự báo đang dùng trả số theo ngày), lịch vắt qua hai tháng thì mỗi ngày xét tháng của ngày đó.
- **Mùa** (chỉ cần `ngay_di`, không gọi mạng) — **theo câu trả lời của User cho phiếu nhỏ đợt 1 (12/11):**
  (i) điểm có `mua_luu_y.bo_khoi_lich: true` và tháng của ngày đang xếp nằm trong `mua_luu_y.thang` (điểm **tạm dừng đón khách** theo mùa) ⇒ **không xếp** ngày đó. Luật này **thắng** mọi luật ưu tiên: điểm đang đóng
  thì không xếp dù là điểm ưu tiên; khi đó code nối một ghi chú (mã `tam_dung_mua`);
  (ii) **không in lưu ý mùa theo từng điểm và không "hạ" điểm theo mùa** (User chọn: chỉ một dòng chung);
  (iii) lịch có ít nhất một ngày rơi vào **tháng 9–12** ⇒ đúng **một dòng** ở đầu khối ghi chú: "Huế đang mùa mưa — nên mang áo mưa, lịch ngoài trời có thể phải đổi" (chữ User duyệt, do code in).
- **Mưa theo dự báo** (chỉ khi ngày đó nằm trong 7 ngày tới): ngưỡng **khả năng mưa ≥ 60 %** (đúng ngưỡng `NGUONG_MUA` đang chạy — không thêm ngưỡng mới). Ngày mưa ⇒ thứ tự xét của **điểm không ưu tiên**
  đổi thành: trong nhà ⇒ cả hai ⇒ ngoài trời (trong mỗi nhóm giữ thứ tự cũ); điểm ưu tiên giữ chỗ + dòng "nếu mưa" đang có. Dự báo lỗi / hết hạn ⇒ xếp như không có dự báo, không có dòng dự báo.
- **Sàn** (giữ như mục 3.1): đổi ngày "mùa khô, giữa tuần" ↔ "mùa mưa, cuối tuần" ⇒ khung hoặc ghi chú khác ở ≥ 60 % tổ hợp có điểm ngoài trời.

### 5c.3 Công thức số điểm mỗi buổi + giờ gợi ý (code in, model không viết giờ)

| Thông số | Giá trị |
|---|---|
| Phút tham quan | `ngan` = **75 phút** · `nua_buoi` = **150 phút** |
| Đi giữa hai điểm trong một buổi | cùng cụm **15 phút** · cụm kề **30 phút** · khác ⇒ không ghép trong một buổi |
| Quỹ một buổi sáng / chiều | nhẹ nhàng: 1 điểm · cân bằng: **210 phút** · khám phá nhiều: **240 phút** · tối đa **2 điểm / buổi** (4 điểm / ngày) |
| Giờ bắt đầu | sáng **8:00** (khám phá nhiều 7:30) · chiều **13:30** (khám phá nhiều 13:00) — sớm hơn 30 phút để điểm cuối buổi chiều xong trước giờ đóng 30 phút (kho không ghi giờ ngừng bán vé) |
| Điểm thêm trong buổi | lấy theo thứ tự xét (ưu tiên ⇒ hợp sở thích ⇒ di tích lấp), chưa dùng, hợp buổi, cùng cụm / cụm kề với **điểm đứng ngay trước**, không làm ngày vượt 2 cụm, tổng phút + phút đi ≤ quỹ |
| Giờ in ra | điểm đầu: giờ bắt đầu ⇒ + phút tham quan; điểm sau: + phút đi ⇒ + phút tham quan. Mọi số là bội của 15 phút ⇒ không cần làm tròn. Dạng "8:00 – 10:30" |
| Giờ mở cửa | điểm có giờ mở muộn hơn giờ bắt đầu ⇒ dời cả buổi tới giờ mở; giờ kết thúc vượt giờ đóng ⇒ **không thêm** điểm đó (điểm đầu của buổi mà vượt ⇒ chọn điểm khác) |
| Buổi tối | in đúng `gio_toi` của bảng; không tính quỹ phút |
| Nhóm hạn chế | luôn 1 điểm / buổi, 2 buổi / ngày, giờ như "nhẹ nhàng" |

Kiểm số: 2 điểm ngắn cùng cụm 165 phút, cụm kề 180 ⇒ vừa "cân bằng"; nửa buổi + ngắn cùng cụm 240 ⇒ chỉ vừa "khám phá nhiều"; 3 điểm ngắn cùng cụm 255 ⇒ không vừa (đúng ý: không nhồi).
Buổi chiều kết thúc muộn nhất **17:00** (cả "cân bằng" 13:30 + 210 và "khám phá nhiều" 13:00 + 240) = trước giờ đóng 17:30 của Quần thể di tích 30 phút. Trần thật là 2 điểm / buổi vì 3 điểm ngắn không vừa quỹ.
**Mô phỏng bản thử trên v8 (5 mức số ngày × 2 nhóm × 6 sở thích × 3 kiểu đi = 180 lịch, 0 USD):** 0 điểm lặp · 0 ngày rỗng · 0 ngày quá 2 cụm · tổng số điểm tăng dần theo kiểu đi ở 60 / 60 nhóm ·
**ba mức cho ba khung khác nhau ở 24 / 30 nhóm không hạn chế (80 % ≥ sàn 70 %)** · trung bình 2,00 / 2,76 / 3,24 điểm một ngày (sáng + chiều) · điểm ban ngày không bao giờ được xếp: **1 / 30**
(một lăng xa; ≤ 3 theo mục 6). Luật cũ "đi dày" (chỉ ghép khi điểm đầu là ngắn) trên cùng bảng: khác "thong thả" ở 3 / 120 cặp ⇒ **bỏ luật cũ**, tên cũ `thong_tha` ⇒ `nhe_nhang`, `day_lich` ⇒ `kham_pha`.

### 5c.4 Thứ tự xét và cách đếm cụm

- **Thứ tự xét của một lịch** = (1) điểm người dùng nêu (lượt chat) ⇒ (2) điểm `uu_tien` của sở thích đang chọn, theo thứ tự 1–4 ⇒ (3) điểm hợp sở thích theo thứ tự bảng ⇒ (4) di tích lấp, có nhãn.
  Chọn **2 sở thích**: bậc (2) và (3) xen kẽ hai loại (A1, B1, A2, B2…). Không chọn sở thích: khoá `chung` + luật đang có "một điểm thiên nhiên mỗi ngày".
- **Cụm của một ngày** = tập cụm của **mọi điểm sáng + chiều** (kể cả điểm thêm trong buổi): ≤ 2 cụm, hai cụm phải kề; cụm xa chiếm cả ngày, chỉ từ 3 ngày (luật cũ). Điểm ưu tiên ở cụm xa: xếp vào
  **ngày 2** khi lịch ≥ 3 ngày (ngày 1 ở gần trung tâm) — bản thử hiện đặt ở ngày 1, B sửa khi viết thật; bất biến đo: "ngày 1 không thuộc cụm xa".
- **Buổi tối không tính vào 2 cụm** (khách đã về khu trung tâm): hoạt động tối chỉ lấy ở cụm `bo_nam` / `kinh_thanh`; ngày đi cụm xa ⇒ tối không xếp, code in dòng "tối nghỉ sau chuyến đi xa". Mỗi tối tối đa 1 hoạt động,
  không lặp cho tới khi hết hoạt động hợp thứ; hết ⇒ được lặp hoạt động diễn hằng đêm, có nhãn "có thể đi lại". Sàn "≥ 80 % số tối có hoạt động" tính trên các tối **không** thuộc ngày cụm xa.
  Số đếm (theo đề xuất của phiếu nhỏ, chờ User): tối nào cũng có ≥ 3 hoạt động xếp được; cuối tuần 4–5 ⇒ lịch ≤ 5 ngày không cần lặp nếu User giữ các đề xuất; User siết (phố quán chỉ cuối tuần) ⇒ giữa tuần còn 2 ⇒ lịch từ 3 ngày phải lặp.

### 5c.5 Khuôn dữ liệu trả cho giao diện

```
lich = {
  "phien_ban": 2,
  "tham_so": {so_ngay, nguoi_lon, tre_em, lon_tuoi, kieu_di, so_thich: [...], ngay_di},
  "ngay": [ { "ngay": 1, "ngay_thang": "2026-12-20" | null, "thu": 0–6 | null,
              "muc": [ { "id_muc": "n1-sang-1",            # khoá ổn định: n<ngày>-<buổi>-<thứ tự>
                         "buoi": "sang" | "trua" | "chieu" | "toi",
                         "loai": "tham_quan" | "hoat_dong_toi" | "an" | "nghi",
                         "id_diem": "...", "ten": "...", "gio": "8:00 – 10:30" | null,
                         "nguon": 3 | null, "anh": "id ảnh" | null, "toa_do": [vĩ, kinh] | null,
                         "nhan": ["ngoai_so_thich" | "luu_y_mua" | "neu_mua" | "co_the_di_lai" | "chua_kiem", ...] } ] } ],
  "o_dau": null,                                           # đợt 3
  "ghi_chu": [ { "ma": "mua_mua" | "du_bao" | "han_che" | "thieu_so_thich" | ..., "cau": "do code viết" } ]
}
```
- Sự kiện khi hiện chữ dần: `lich_khung` (gửi **ngay sau khi code xếp xong**, trước lần gọi model — người dùng thấy lịch có tên điểm + giờ trong < 1 giây) ⇒ `lich_cau` `{id_muc, cau}` cho từng mục ⇒ `lich_xong`
  `{so_cau_du_phong}`. Lượt không hiện dần: trả `lich` + `cau: {id_muc: câu}` trong một phản hồi. Trường `answer` (chữ thuần) vẫn có — code ghép từ khung + câu — để lịch sử chat, nút chép và bản cũ của giao diện dùng.
- Mục `loai: "an"` và `o_dau` chỉ xuất hiện từ đợt 3; giao diện đợt 1 bỏ qua loại không biết (không lỗi).

### 5c.6 Model viết gì

- **Model KHÔNG viết cả lịch.** Một lần gọi, không công cụ; đầu vào = khung (id mục, tên điểm, loại, nhãn) + đoạn kho của từng điểm; đầu ra = **mảng `[{id_muc, cau}]`** theo lược đồ cố định, mỗi câu ≤ 30 từ,
  chỉ mô tả "ở đây có gì / nên xem gì", kèm mã trích dẫn của đúng điểm đó.
- **Code quyết:** thứ tự, tên điểm, giờ, khoảng cách, lưu ý mùa / dự báo, nhãn, khối ghi chú.
- **Kiểm cuối theo từng câu:** `id_muc` phải thuộc khung; câu không chứa giờ, thời lượng, số tiền, đường dẫn, tên điểm / quán / cơ sở khác tên của mục; mã trích dẫn thuộc nguồn của điểm. Câu thiếu hoặc lỗi ⇒
  **câu dự phòng do code** (tên + loại điểm, không mô tả) cho riêng mục đó — không rút cả lịch. **Sàn:** ≤ 1 câu dự phòng / lịch ở ≥ 18 / 20 lịch của bộ thật; lịch có > 30 % câu dự phòng ⇒ tính là trượt.
- Vì sao chọn mảng thay cho chữ tự do: hai lần trước model viết lệch khung / tự thêm giờ khi khuôn đổi; mảng theo id làm kiểm cuối thành phép so từng ô, và khung hiện được ngay không chờ model.
  **B đã xác nhận (tin 12/11, sau 21:47):** làm được — hôm nay đầu ra đã là JSON và code tự bóc chữ dần từ mẩu JSON thô. Bản đầu phát **một sự kiện `lich_cau` mỗi khi một phần tử đóng ngoặc** (câu của mục hiện nguyên câu,
  khoảng 1–2 giây một mục); chạy chữ trong từng câu **không làm ở đợt 1** (thêm ~nửa ngày, lợi ít). Khung phát trước lần gọi model (ước 0,1–0,3 giây sau khi gửi). Model lỗi / hết giờ / từ chối ⇒ lịch vẫn hiện đủ
  khung, mục không có câu dùng câu dự phòng ⇒ **bỏ nhánh "rút cả lịch"** của đường cũ. Kiểm cuối viết lại nhỏ hơn (bỏ các luật dò dòng buổi / thứ tự / "nói ngược buổi trống"; ước ~150 / 230 dòng), đường cũ giữ sau cờ.
- **Lượt thử có phí sớm (≤ 0,005 USD, đã ghi ở 5b) phải đếm:** tỉ lệ model trả thiếu mục · lặp `id_muc` · gộp hai mục vào một câu. Xử lý ghi trước: thiếu ⇒ câu dự phòng; lặp ⇒ lấy phần tử đầu; gộp ⇒ kiểm
  "tên điểm khác" bắt ⇒ câu dự phòng. Tốc độ đo ở hai mốc: **lúc khung hiện** (sàn ≤ 1 giây) và lúc đủ câu (không chậm hơn mốc quá 2 giây).

### 5c.7 Bộ đo — ai viết, khi nào

- **20 yêu cầu của bộ lịch thật + 12 tổ hợp của bộ quyết:** do **E viết** (không phải B — người code; không phải C — người viết spec và bản thử luật), **xong trước khi B bắt đầu bước (b)** của thứ tự merge;
  lưu private trong `data/`, mã băm của hai file ghi vào plan đợt 1. Phân bổ 20 yêu cầu: như mục 6 (5 mức số ngày · có / không trẻ em · có / không lớn tuổi · 3 kiểu đi · 1 và 2 sở thích · 4 kiểu ngày đi).
- **Định nghĩa "lịch khớp điều đã chọn"** cho người chấm (ghi trước): (1) đúng số ngày; (2) nhóm hạn chế không có tham quan buổi tối; (3) kiểu đi — **không do người chấm chấm**: code đếm theo cặp trên cùng yêu cầu (tổng điểm nhẹ nhàng ≤ cân bằng ≤ khám phá nhiều, và khám phá nhiều > nhẹ nhàng; mỗi ngày nhẹ nhàng 2 · cân bằng 2–4 · khám phá nhiều 2–4);
  (4) mỗi sở thích đã chọn có ≥ 1 điểm ưu tiên của nó trong lịch — **ngoại lệ:** điểm ưu tiên không xếp được vì luật cứng (cụm xa khi < 3 ngày, nhóm hạn chế hết suất, điểm tạm dừng theo mùa) ⇒ lịch phải có ghi chú thiếu sở thích do code; (5) điểm buổi tối đúng thứ; (6) có ngày đi mùa mưa ⇒ có dòng nhắc. Đủ 6 ⇒ đạt.
- Mô phỏng 0 USD: B chạy trên **toàn bộ tổ hợp của biểu mẫu mới** (5 số ngày × trẻ em 0 / ≥ 1 × lớn tuổi có / không × 3 kiểu đi × 16 lựa chọn sở thích [không chọn, 5 đơn, 10 cặp] × 4 kiểu ngày đi = 3.840 tổ hợp).

### 5c.8 Cờ và mốc cũ

- **Một cờ cho cả đợt 1:** `assistant.len_ke_hoach_v2` (mặc định tắt). Tắt ⇒ đường biểu mẫu hôm nay **giống byte** (bộ mốc cũ giữ nguyên). Bật ⇒ hợp đồng `truong` mới, bảng v8 / v9, luật xếp mới, khuôn mới.
  Ô nào dưới sàn ⇒ ẩn bằng **danh sách ô hiện** trong cấu hình (`/api/tinh_nang` trả về), không thêm cờ riêng cho từng ô. Các bước (a)–(e) merge sau cờ này; bật cờ **một lần** khi đủ tiêu chí đợt 1.
- **Mốc cũ của đường biểu mẫu (tiêu chí quyết bật cờ `lich_trinh_bieu_mau` ở spec cổng đợt 1):** vẫn là **sàn khi cờ mới tắt**. Khi cờ mới bật, bộ đó được **thay** bằng bộ quyết 12 tổ hợp mới (giá trị trường khác ⇒
  không so cùng thước được); phần không đổi vẫn giữ làm sàn: kiểm cuối 0 lỗi, 0 rút, 0 từ chối, an toàn 32 ×2, 0 câu ngoài phạm vi được trả lời.
- Đường lịch trình **câu tự do** (chat) không thuộc đợt 1: giữ luật + bảng đang chạy cho tới khi đợt 1 bật ổn định; sau đó một việc riêng chuyển nó sang bảng mới (ghi ở mục 9).

## 6. Tiêu chí ghi trước

**Sàn chung mọi đợt:** `kiem_khung` 0 lỗi trên toàn bộ tổ hợp mô phỏng · mọi bất biến "Luôn" ở mục 2 và 3 · kiểm cuối 0 lỗi trên bộ lịch thật · an toàn 32 ×2 không đổi (lượt không phải biểu mẫu:
chuỗi gửi model giống byte ⇒ dùng lại số; khác ⇒ chạy) · 0 câu ngoài phạm vi bị trả lời.

| Đợt | Mô phỏng 0 USD | Bộ lịch thật (có phí) | Người chấm |
|---|---|---|---|
| 1 | bất biến + sàn của mọi ô ở 3.1 và hai dòng tham quan / buổi tối ở 3.2; số điểm "không bao giờ được xếp" ≤ 3 (mỗi điểm còn lại có lý do) | 20 yêu cầu ghi trước (5 mức số ngày, có / không trẻ em, có / không lớn tuổi, 3 kiểu đi, 1 và 2 sở thích, 4 kiểu ngày đi) ×1: 20 / 20 qua kiểm cuối, 0 rút, 0 từ chối; trung vị cả câu không chậm hơn mốc `main` cùng buổi quá 2 giây (mốc 12/11: 4,9 giây); lượt có gọi dự báo báo riêng | bộ quyết 12 tổ hợp mới ×2, hai người chấm độc lập: ≥ 11 / 12 mỗi lượt cho "lịch khớp điều đã chọn" (định nghĩa ghi ở plan trước khi chấm) |
| 2 | mọi ảnh / ghim sinh ra thuộc bảng được duyệt và đúng id (toàn bộ 28–33 điểm) | Playwright 2 khổ màn: ảnh hiện + có dòng tác giả, bản đồ có đủ ghim đúng thứ tự, 0 yêu cầu mạng tới tên miền ngoài danh sách CSP; kích thước bản build tăng ≤ mức ghi ở plan | một người xem 10 lịch: ảnh đúng điểm 10 / 10 |
| 3 | bất biến + sàn hai dòng ăn uống / lưu trú ở 3.2 | 20 yêu cầu ×1 như đợt 1 + 0 tên quán / cơ sở ngoài bảng, 0 số tiền | bộ quyết 12 ×2: ≥ 11 / 12 cho "lịch đủ bốn phần và hợp điều đã chọn"; bữa ăn hợp khu ≥ 11 / 12 |

**So với Huế TRIPO sau đợt 3 (báo User, không phải sàn):** đúng hai yêu cầu User đã thử 12/11 + 4 yêu cầu ghi trước gửi hai bên ⇒ bảng "phần nào hai bên đều có · bên nào dùng được hơn · lỗi thấy được",
kèm đối chiếu từng dòng của bảng mục 2.

## 7. Rà theo khung AI FDE

| Mục | Thiết kế | Khớp / rủi ro |
|---|---|---|
| Có cần model không | xếp, chọn quán, chọn khu, gắn ảnh, tính giờ, kiểm: code. Model chỉ viết lời cho khung (một lần gọi) | khớp |
| Phép tính / luật / thứ tự ⇒ code | số suất theo kiểu đi, luật nhóm, thứ + mùa + dự báo, giờ gợi ý, khoảng cách quán | khớp — rút từ các lần để model tính bị âm |
| Công cụ + tham số | lượt biểu mẫu không đưa công cụ cho model; dự báo do code gọi trước | khớp |
| Chữ người dùng là dữ liệu | mọi ô là giá trị trong tập cho phép; ngày và số được kiểm khoảng; không ô chữ tự do | khớp |
| Dữ liệu ngoài đi vào sản phẩm | ảnh giấy phép mở (ghi tác giả, giấy phép, link); toạ độ từ dữ liệu mở + nguồn công khai; quán / cơ sở lưu trú qua đợt bổ sung kho 3 (User duyệt) | khớp — mỗi nguồn có phiếu cho User xem lướt |
| Đường ra ngoài | gọi dự báo thời tiết công khai khi có ngày đi (đã có); ô bản đồ tải từ máy chủ bản đồ đã duyệt ở plan bản đồ; link Maps do code dựng. Không gửi lựa chọn của người dùng cho bên thứ ba ngoài nhà cung cấp model | khớp |
| Dữ liệu cá nhân | không thu tên / liên hệ; ngày đi + số người không lưu ngoài phiên | khớp |
| Đường phục hồi | mỗi đợt một cờ; bảng thiếu cột ⇒ ô / phần tương ứng tự ẩn (`/api/tinh_nang` báo); dự báo lỗi ⇒ bỏ phần dự báo, giữ lịch; ảnh thiếu ⇒ không ảnh | khớp |
| Đo hai chiều | mỗi ô / phần: "có tác dụng" (sàn) ↔ "không phá luật cũ" (bất biến + sàn chung) | khớp |
| Rủi ro còn | (1) luật xếp phình to — chặn bằng "mỗi ô một luật, mỗi luật một test + một dòng trong bài học"; (2) thời lượng từ web sai ⇒ lịch quá dày — lấy mức trên + nhóm hạn chế luôn ở mức nhẹ; (3) dữ liệu quán mỏng ngoài bờ nam ⇒ phần ăn uống nhiều dòng "chưa có quán" — nói thật, và là lý do phụ thuộc đợt kho 3; (4) khối lượng 3 đợt + kho 3 + lượt đo cuối trong ~5 tuần — thứ tự cắt ghi ở mục 4 | theo dõi |

## 8. Câu hỏi cho User (4 câu, mỗi câu có khuyến nghị)

**Câu 1 — Số ngày tối đa trên biểu mẫu?**
- **(a) 5 ngày** *(khuyến nghị)*: bảng 28–33 điểm đủ cho 5 ngày không lặp. Khi nào sai: khách đi dài hơn — lịch ghi "mình xếp 5 ngày đầu".
- (b) 7 ngày: cần thêm ~10–15 điểm vào bảng trước (thêm một vòng phiếu); chưa thêm mà chọn (b) ⇒ ngày 6–7 trống hoặc lặp.

**Câu 2 — Buổi tối: có thêm hoạt động buổi tối vào bảng không?**
- **(a) Có — thêm hoạt động đã có bài trong kho (User chốt; thực tế kho cho 1–2 hoạt động, xem "Sửa chữ bản 3.1")** (nghe ca Huế trên sông, biểu diễn định kỳ, chợ đêm…), agent điền sẵn giờ + thứ kèm nguồn, anh xem lướt *(khuyến nghị)*. Không thêm thì
  phần "buổi tối" chỉ có 3 phố đi bộ, hoạt động vài tối một tuần ⇒ nhiều tối trống.
- (b) Chỉ dùng 3 điểm tối đang có. Mất gì: sàn "≥ 80 % số tối có hoạt động" gần như chắc trượt ⇒ phần buổi tối chỉ hiện khi đi cuối tuần.

**Câu 3 — Ảnh minh hoạ lấy từ đâu?**
- **(a) Kho ảnh giấy phép mở (như 7 ảnh cổng hiện có), ghi tác giả + giấy phép dưới ảnh** *(khuyến nghị)*: agent tìm và điền sẵn phiếu ảnh, anh xem lướt; điểm không tìm được ảnh hợp lệ thì để
  trống. Khi nào sai: ảnh cũ / không đẹp bằng ảnh quảng bá.
- (b) Ảnh của cơ quan du lịch (đẹp hơn) — chỉ dùng được trên máy anh, **không đưa lên bản công khai / git** khi chưa có phép (đúng như ảnh lễ hội riêng hiện nay) ⇒ bản công khai thiếu ảnh.

**Câu 4 — Loại hình ("Thích gì")?**
- **(a) Giữ các loại bảng đủ điểm, ẩn loại dưới 4 điểm** *(khuyến nghị)*.
- (b) Bổ sung dữ liệu để có thêm loại (bảo tàng – giáo dục, làng nghề – cộng đồng, nghỉ dưỡng biển): mỗi loại cần ≥ 4 điểm có bài trong kho ⇒ gộp vào một đợt bổ sung kho sau mốc.

## 9. Phụ thuộc và thứ tự

1. **Phiếu cho User (đều theo kiểu agent điền sẵn, User xem lướt):** phiếu gộp (đã đưa) ⇒ bảng v8 (ưu tiên), v9 (thời lượng, trong nhà, bậc thang, toạ độ) · **phiếu nhỏ đợt 1** (thứ hoạt động 3 điểm
   tối, tháng lưu ý mùa, 3–5 hoạt động buổi tối) — chưa soạn · **phiếu ảnh** (đợt 2) — chưa soạn.
2. Plan điểm ưu tiên (đã có nháp) là bước đầu của đợt 1.
3. Đợt 3 chờ: spec bổ sung kho 3 `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` (User trả lời Q1–Q5; Q3 / Q4 quyết mức dữ liệu bữa ăn; đang có review 3 major) + plan lưu trú
   (đường kích hoạt thứ hai) + toạ độ quán (E đang tra thêm).
4. Lượt đo cuối B7 chạy **sau** đợt 3, trên bản đủ ba đợt.
5. Tiền: ≤ 0,75 USD cho cả mốc (kể cả kho 3) — vượt phần còn lại của trần Phase 9 hiện tại ⇒ A xin User khi duyệt spec.

## Chỗ đổi so với bản 2 (E chỉ cần kiểm phần này)

| Đổi gì | Ở đâu | Vì sao |
|---|---|---|
| Phạm vi: **một lịch đủ 4 phần + ảnh + bản đồ là cam kết**; bỏ khỏi mốc: ngân sách, ba phương án, mục riêng lưu trú / ăn uống / dịch vụ, đổi / bỏ điểm | mục 1 (bảng trong / sau mốc), mục 4 | User chốt tối 12/11 |
| Ba đợt chia lại: 1 khung + biểu mẫu + buổi tối + giờ gợi ý · 2 ảnh + bản đồ (song song) · 3 ăn uống + lưu trú; bỏ "điểm dừng chờ User chọn làm tiếp" — cả ba là cam kết; thêm **thứ tự cắt nếu trễ** | mục 4 | như trên; A: "cả mức này là cam kết" |
| Thêm mục **"chỗ phải hơn TRIPO"** với bất biến tương ứng | mục 2 | kết quả TRIPO do User chụp (báo cáo khoảng cách mục 4b) |
| Thêm phần **buổi tối** (dữ liệu: 3–5 hoạt động tối + thứ / giờ) và **giờ gợi ý theo buổi** do code in | mục 3.2, Câu 2 | "đủ 4 phần"; hôm nay tối chỉ có khi chọn ẩm thực |
| **Ăn uống theo buổi** (sáng: món; trưa / tối: quán theo cụm, không lặp) thay cho "một dòng bữa ăn"; nguyên tắc N3 "nói thật, không chỗ giữ chỗ" | mục 1 (N3), 3.2 | như trên + lỗi thấy ở TRIPO |
| **Lưu trú trong lịch**: khối "Ở đâu" theo cụm điểm của lịch (+ tên cơ sở khi kho có) | mục 3.2 | "đủ 4 phần" |
| **Ảnh** (bảng ảnh theo id điểm, ~3 / 28 dùng lại được, phiếu ảnh) và **bản đồ** thành đợt 2 | mục 3.3, Câu 3 | User chốt |
| Dòng "ngân sách" và dòng "đổi / bỏ điểm" bị gỡ khỏi bảng từng ô; câu hỏi ngân sách + câu "ô người lớn" bị gỡ (ô người lớn giữ làm ngoại lệ có chủ ý vì User đã chốt biểu mẫu có số người) | mục 3.1, mục 8 | ngoài mốc |
| Ghi chú vòng 2 của E: đếm sàn 70 % của "kiểu đi" là việc đầu tiên của plan đợt 1 | mục 3 (đoạn số đếm) | E vòng 2 |
| **Thứ tự ưu tiên giữa các luật xếp** + ghi chú thực thi (đổi khuôn khung / kiểm cuối, lượt thử có phí sớm, hạn nhận trường cũ, đo riêng lượt dự báo lạnh, thứ tự merge, ảnh đóng gói, dòng báo bản đồ) | mục 5b | góp ý của B (người code) |
| Giữ nguyên từ bản 2 (E đã `ready`): hai lớp bất biến / sàn; hợp đồng trường; tiêu chí đợt 1; bảng rà khung | — | — |

## Sửa chữ bản 3.1 (21:41 12/11/2026, `date`) — theo kiểm phần đổi của E (ready, 3 sửa chữ) + số đếm của phiếu nhỏ đợt 1

| Đổi gì | Ở đâu | Vì sao |
|---|---|---|
| Sàn ăn uống chỉ còn một mức (bỏ nhánh "mức A"); ghi danh sách cụm được tính sàn 80 % và cụm lăng không tính (dùng dòng nói thật) | mục 3.2 dòng "Ăn uống theo buổi" | E c-1: User đã chốt Q3 / Q4 của spec kho 3 |
| Bất biến khoảng cách tách hai vế: toạ độ chắc / vừa ⇒ ≤ 1,5 km; toạ độ ước ⇒ "cùng cụm", không so mét | như trên | E c-2 |
| Bảng ánh xạ 8 cụm ⇒ 3 khu: trỏ tới trường `cum` của `khu_v1.json` (plan lưu trú, E giữ) | mục 3.2 dòng "Lưu trú" | E c-3 |
| **Sửa số:** "thêm 3–5 hoạt động buổi tối đã có bài trong kho" **không đạt được** — phiếu nhỏ đợt 1 đếm kho: chỉ **1** hoạt động có đủ giờ + thứ (diễn hằng đêm), **1** ứng viên thiếu giờ (cần User điền), các chương trình còn lại không có lịch cố định. Dòng "Buổi tối", Câu 2 và mục 9 đọc là "thêm 1–2 hoạt động"; sàn "≥ 80 % số tối có hoạt động" giữ nguyên (hoạt động thêm diễn mọi tối nên vẫn đạt được), độ đa dạng buổi tối là giới hạn đã biết — muốn hơn phải bổ sung bài vào kho | mục 3.2 dòng "Buổi tối", mục 8 Câu 2, mục 9.1 | phiếu `data/phase_9/lich_trinh/phieu_nho_dot_1_2026-11-12.md` (private) |

## Chỗ đổi của bản 3.2 (21:47 12/11/2026, `date`) — sau khi User trả lời phiếu gộp + chốt 4 câu của spec, và B nêu 8 chỗ thiếu

| Đổi gì | Ở đâu | Vì sao |
|---|---|---|
| User chốt cả 4 khuyến nghị ở mục 8 (tối đa 5 ngày · thêm hoạt động tối có bài kho · ảnh giấy phép mở · ẩn loại < 4 điểm) | mục 8 (đọc là đã chốt) | A báo 12/11 |
| **Ưu tiên theo từng sở thích** thay cho một danh sách chung hai mức | mục 3.1 dòng "Điểm ưu tiên", 5c.1, 5c.4 | User trả lời câu 1 của phiếu gộp |
| Thời lượng: dùng cả bảng kể cả dòng ước; ô chưa chắc đã tra thêm một lượt (9 ô: 7 có nguồn mở được, 2 vẫn là ước — hai phố buổi tối) | 5c.1 | User trả lời câu 2 |
| Bảng 33 điểm (thêm 5 điểm trong nhà) ⇒ loại "lễ hội – nghệ thuật" lên 4 điểm, cả 5 loại đều hiện | 5c.1 | User trả lời câu 3 |
| Luật "kiểu đi" viết lại bằng phút; bất biến đổi từ "theo ngày" sang "theo tổng của lịch"; có số mô phỏng (80 % ≥ sàn 70 %) | mục 3.1 dòng "Kiểu đi", 5c.3 | luật cũ chỉ cho 3 / 120 cặp khác nhau trên bảng mới |
| Buổi tối: đúng số thật của kho (1 hoạt động thêm chắc + 1 chờ User), ghi giới hạn đa dạng; cách tính sàn 80 % | mục 3.2 dòng "Buổi tối", 5c.4 | phiếu nhỏ đợt 1 |
| Tám quyết định để code: cột bảng · mùa / mưa · công thức giờ · đếm cụm · khuôn dữ liệu · model trả mảng theo id · ai viết bộ đo · cờ + mốc cũ | **mục 5c (mới)** | B nêu; A giao |
| B đã xác nhận cách hiện dần với đầu ra có cấu trúc (5c.6 — phát nguyên câu từng mục). Còn mở (không chặn duyệt spec): báo cáo B thử đủ luồng lập kế hoạch của trang kia (đầu vào cuối, có thể thêm dòng vào mục 2) | 5c.6, mục 2 | — |

## Chỗ đổi của bản 3.3 (22:01 12/11/2026, `date`) — E kiểm mục 5c (sửa chữ / số, không cần vòng nữa) + User trả lời phiếu nhỏ đợt 1

| Đổi gì | Ở đâu | Vì sao |
|---|---|---|
| Trần **2 điểm / buổi, 4 điểm / ngày** (bỏ chữ "3 điểm / buổi"); dòng giải thích trên nút: khoảng 2 / khoảng 3 / tới 4 | 3.1, 5, 5c.3 | E S-1: 3 điểm ngắn = 255 phút không vừa quỹ 240 |
| Định nghĩa chấm: (3) thành phép đếm bằng code theo cặp; (4) thêm ngoại lệ luật cứng + ghi chú | 5c.7 | E S-2 |
| Buổi chiều bắt đầu 13:30 (khám phá nhiều 13:00) ⇒ xong muộn nhất 17:00 | 5c.3 | E g-2: kho không ghi giờ ngừng bán vé |
| Luật mùa: chỉ còn "điểm tạm dừng theo mùa ⇒ không xếp" (thắng luật ưu tiên, có ghi chú) + **một dòng nhắc mưa chung tháng 9–12**; bỏ "hạ" và bỏ lưu ý mùa theo từng điểm | 5b bậc 5, 5c.2 | User trả lời câu 2, 3 của phiếu nhỏ; E g-1 |
| Phố quán bờ nam xếp **mọi tối** kèm ghi chú ngày cấm xe (cột `ngay_hoat_dong` rỗng + `luu_y`) | bảng đề xuất (private) | User trả lời câu 1 |
| Luật "điểm ưu tiên cụm xa không ở ngày 1" **đã mô phỏng** (bản thử, 180 lịch): ngày 1 có điểm cụm xa 0 / 180 · điểm ưu tiên cụm xa nằm ngày 2 ở 18 / 18 · 0 ngày rỗng · số điểm trung bình mỗi ngày không đổi (2,00 / 2,76 / 3,24) | 5c.4 | A giao; cách đo theo E |
| Lượt biểu mẫu đo tốc độ bằng hai mốc mới (khung hiện · đủ câu), **không so với số "chữ đầu" cũ**; lượt thử sớm đếm thêm **tỉ lệ câu bị thay nhầm** do luật "tên điểm khác" (tên con nằm trong điểm lớn) | 5c.6 | E g-3, g-4 |
| Chưa đo được bằng 180 lịch (đo ở bước code, cách đo theo bảng của E trong file review): mùa / mưa (3 kịch bản dự báo ghi sẵn) · tối đúng thứ · giờ không vượt giờ đóng · sàn 80 % buổi tối | plan đợt 1 | E |
