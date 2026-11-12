# Spec — "Lên kế hoạch" bản 2: biểu mẫu nhiều lựa chọn, ô nào hiện thì ô đó đổi được lịch · NHÁP bản 1

Người viết: C, 21:13 12/11/2026 (`date`), A giao theo ý User tối 12/11 ("đa dạng như Huế TRIPO; chỗ nào TRIPO hơn thì học, cố gắng tốt hơn; cần dữ liệu thì tìm, cào, bổ sung").
Chưa code. E review; B code sau khi User duyệt. Repo public: không chép chữ / bố cục của trang khác; tên điểm cụ thể nằm ở phiếu private.

## Căn cứ để review (`WORKFLOW.md` §9.1)

- Lượt đếm + bảng khoảng cách: `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` (mục 2, 3).
- Code đang chạy: `backend/llm/lich_trinh.py` (`ThamSo`, `xep`, `_cum_hop`, `HAN_CHE`, `kiem_khung`, `kiem_cuoi`) · `backend/llm/hoi_lai.py` (`GIA_TRI`, `TruongInput`) ·
  `backend/llm/assistant.py` (`answer_bieu_mau`) · `backend/llm/thoi_tiet.py`, `ngay_lich.py` · `frontend/src/pages.jsx` (`BIEU_MAU`, `LenKeHoach`).
- Spec trước: `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` (D3, D4, Q-U3, §6 Q-F). Plan nền của đợt 1: `docs/superpowers/plans/2026-11-12-lich-trinh-diem-uu-tien-plan.md`.
- Dữ liệu (private): phiếu gộp `data/phase_9/lich_trinh/phieu_gop_cho_user_2026-11-12.md` · bảng quán `data/sua_kho_2026-11-12_an_gan/bang_de_xuat.md` · ghi chép trang lập kế hoạch của
  Huế TRIPO `data/tripo_v5_2026-11-12/tools/recon.json` + vòng 3 `data/nghien_cuu_tinh_nang_2026-11-04/sa2_tripo_v3_agentic.md`.

## 1. Mục tiêu và nguyên tắc

**Mục tiêu:** người dùng nói được nhiều hơn về chuyến đi (ai đi, bao lâu, khi nào, đi kiểu gì, thích gì, chi tiêu) và **mỗi điều họ chọn làm lịch khác đi một cách kiểm được**.

Hôm nay (đếm 12/11): biểu mẫu có 3 hàng; trên 360 tổ hợp, "kiểu đi" đổi khung 0 / 120; trong 5 lựa chọn "đi cùng ai" chỉ 2 lựa chọn (trẻ em, người lớn tuổi) làm lịch khác — 3 lựa chọn
còn lại chỉ đổi dòng "Mình hiểu"; 7 / 28 điểm không bao giờ được xếp.

| # | Nguyên tắc (A đặt, User đồng ý hướng) | Hệ quả trong spec |
|---|---|---|
| N1 | **Ô nào hiện thì phải đổi được lịch.** | Mỗi ô ở mục 3 ghi: code dùng nó ở đâu, cần dữ liệu gì, đo "đổi khung" bằng mô phỏng 0 USD. Ô chưa có dữ liệu ⇒ sang đợt sau, **không hiện ô trang trí** |
| N2 | **Phép tính, luật, trường bắt buộc ⇒ code;** model chỉ diễn đạt khung. | Tiền do code cộng từ bảng vé rồi in; giờ gợi ý do code in; model không được thêm số. Không nói giá phòng |
| N3 | **Chia đợt theo dữ liệu**, mỗi đợt tự đứng được, đo xong mới sang đợt sau. | Mục 4 |
| N4 | **Giao diện riêng của hue_rag**: học chức năng, không chép bố cục / chữ / màu. | Mục 5; giữ CSP, 0 gói mới |
| N5 | Bảng rà khung AI FDE; tiêu chí ghi trước từng đợt. | Mục 6, 7 |

## 2. So với trang lập kế hoạch của Huế TRIPO (chức năng, ghi 12/11)

| Nhóm ô của TRIPO | hue_rag hôm nay | Bản 2 |
|---|---|---|
| Kiểu đi 3 mức (ít điểm · cân bằng · nhiều điểm) | 2 mức, **ẩn** vì không tác dụng | 3 mức, **đợt 1** — sau khi bảng có thời lượng |
| Loại hình du lịch (7 loại) | "Thích gì" 5 loại, chọn 1 | chọn tối đa 2; **loại nào bảng có < 4 điểm thì không hiện** — đợt 1; thêm loại mới khi có dữ liệu |
| Đi cùng ai (6 nhãn, chọn nhiều) | 5 nhãn, chọn 1 | thay bằng **số người lớn + số trẻ em + ô "có người lớn tuổi"** — đợt 1 |
| Số người lớn / trẻ em (+ / −) | không | **đợt 1** (trẻ em đổi lịch ngay; người lớn dùng cho vé ở đợt 2 — xem Câu 2) |
| Thời gian: số ngày (+ / −) | 4 nút, tối đa "từ 4 ngày" | + / − từ 1 tới 5 ngày — **đợt 1** |
| Ngày khởi hành | không | **đợt 1**: thứ trong tuần, mùa, dự báo 7 ngày |
| Ngân sách 3 mức | không | **đợt 2**: mức chi theo **vé tham quan** do code cộng (không phải model) |
| Tab Lưu trú · Ăn uống · Dịch vụ | không | **đợt 2**: bữa ăn trong lịch; thẻ "khu nên ở + link"; dòng đi lại — sau đợt bổ sung kho 3 |
| Trên lịch: đổi điểm, xoá, kéo thả, bản đồ, tải về | "Sửa — điền lại biểu mẫu", link Maps từng điểm | **đợt 3**: đổi / bỏ một điểm bằng nút; bản đồ ghim số |

Chỗ hue_rag giữ để **hơn**: code kiểm khung + kiểm chữ model (TRIPO từng xếp quá giờ đóng cửa, kết thúc 23:12 cho nhà có trẻ nhỏ); nguồn từng điểm; ~5 giây một lịch; dòng "Mình hiểu".

## 3. Từng ô: code dùng thế nào · cần dữ liệu gì · đo ra sao

Tên trường là đề xuất; B được đổi tên trong phạm vi plan. "Mô phỏng" = chạy `xep` + `kiem_khung` trên mọi tổ hợp giá trị, 0 USD.

| Ô (trường) | Giá trị | Code dùng ở đâu | Dữ liệu cần | Tiêu chí "đổi lịch" (mô phỏng) | Đợt |
|---|---|---|---|---|---|
| Số ngày (`so_ngay`) | 1–5, nút + / − (giữ nhận "4+" cũ = 4) | số ngày của khung; cụm xa chỉ từ 3 ngày (luật cũ) | bảng đủ điểm cho 5 ngày: 28 (+5 điểm trong nhà nếu User đồng ý ở phiếu gộp) | khung n ngày có đúng n ngày, ngày nào cũng ≥ 1 điểm, 0 điểm lặp | 1 |
| Trẻ em (`tre_em`) | 0–6 | ≥ 1 ⇒ luật nhóm hạn chế đang có (không buổi tối, ≤ 2 suất / ngày) + không xếp điểm "nhiều bậc thang" khi có điểm thay thế cùng cụm | cột bậc thang (phiếu gộp, đã có 11 điểm từ kho) | 100 % tổ hợp có trẻ em: 0 buổi tối; số điểm nhiều bậc thang giảm so với 0 trẻ em | 1 |
| Có người lớn tuổi (`lon_tuoi`) | có / không | như trẻ em + **ưu tiên điểm không nhiều bậc thang** trong cùng mức ưu tiên | như trên | như trên; điểm ưu tiên mức 1 bị thay vì bậc thang ⇒ có dòng ghi chú do code nối | 1 |
| Người lớn (`nguoi_lon`) | 1–10 | đợt 1: chỉ vào dòng "Mình hiểu" và suy "đi một mình / đi nhóm" cho lời văn. Đợt 2: nhân vé, link lưu trú | đợt 2: bảng vé | đợt 1: **không đổi khung** (ngoại lệ có chủ ý của N1 — Câu 2) | 1 (hiện) / 2 (dùng) |
| Kiểu đi (`kieu_di`) | nhẹ nhàng · cân bằng · khám phá nhiều | số suất mỗi buổi: nhẹ nhàng 1; cân bằng 2 khi cả hai điểm "ngắn" và cùng cụm / cụm kề; khám phá nhiều tới 3 điểm ngắn / buổi + được buổi tối. Nhóm hạn chế: trần luôn là mức "nhẹ nhàng" (ghi chú do code) | **thời lượng** (phiếu gộp) | 3 mức cho **3 khung khác nhau ở ≥ 70 %** nhóm (số ngày × nhóm người × sở thích) không hạn chế; số điểm / ngày tăng dần nhẹ ⇒ cân bằng ⇒ nhiều | 1 |
| Thích gì (`so_thich`) | tối đa 2 trong các loại đủ điểm | điểm hợp một trong hai loại được chọn trước (sau điểm ưu tiên), xen kẽ hai loại | nhãn loại của bảng; loại có < 4 điểm ⇒ ẩn trên biểu mẫu (hôm nay "lễ hội, nghệ thuật" có 1 điểm ⇒ ẩn cho tới khi thêm điểm) | mỗi loại hiện trên biểu mẫu: ≥ 50 % suất sáng / chiều của lịch 2 ngày là điểm loại đó; chọn 2 loại ⇒ cả hai loại đều có mặt | 1 |
| Ngày khởi hành (`ngay_di`) | ngày (không bắt buộc), từ hôm nay tới + 180 ngày | (a) **thứ trong tuần** ⇒ điểm chỉ hoạt động một số tối (phố đi bộ) chỉ xếp đúng tối đó; (b) **mùa** (tháng) ⇒ điểm có lưu ý mùa (biển, thác, núi) bị hạ ưu tiên + dòng lưu ý do code nối; (c) ngày đi trong **7 ngày tới** ⇒ gọi dự báo (code đã có), ngày mưa ⇒ ưu tiên điểm "trong nhà / cả hai" | cột `ngay_hoat_dong` cho ~3 điểm buổi tối (từ kho); cột `mua_luu_y` (tháng) cho điểm ngoài trời có cảnh báo mùa (kho đã có lời, cần chuyển thành tháng); cột trong nhà (phiếu gộp) | cùng lựa chọn khác, đổi `ngay_di` giữa "tháng mùa khô, giữa tuần" ↔ "tháng mùa mưa, cuối tuần" ⇒ khung **hoặc** khối ghi chú khác ở ≥ 60 % tổ hợp có điểm ngoài trời / buổi tối; 0 lịch xếp phố đi bộ sai tối | 1 |
| Ngân sách (`ngan_sach`) | tiết kiệm · vừa phải · thoải mái | code cộng **vé tham quan người lớn + trẻ em** của các điểm trong khung từ bảng vé; mức = trần vé mỗi người mỗi ngày (số ghi trong plan đợt 2); vượt trần ⇒ thay điểm có vé bằng điểm miễn phí cùng cụm; code in một dòng "Vé tham quan ước tính: … (theo bảng vé ngày …)" | **bảng vé có cấu trúc** (điểm · người lớn · trẻ em · ngày nguồn) dựng từ bài vé của kho + bộ giá vé dữ liệu mở, **User duyệt** | 3 mức cho tổng vé khác nhau ở ≥ 60 % tổ hợp từ 2 ngày; 100 % tổng in ra = tổng tính lại độc lập; 0 số tiền do model viết (kiểm cuối) | 2 |
| Bữa ăn | (không phải ô — tự có khi chọn "ẩm thực" hoặc luôn có, quyết ở plan đợt 2) | mỗi ngày một dòng trưa (và tối với nhóm không hạn chế): món + 1–2 quán **cùng cụm** với điểm buổi đó | toạ độ / khu của quán (đang có 29 / 81 bài; E đang tra thêm) + đợt bổ sung kho 3 | ≥ 80 % ngày ở cụm trung tâm có dòng bữa ăn với quán ≤ 1,5 km; ngày ở cụm không có quán ⇒ câu cố định "khu này ít quán, nên ăn trước ở …" | 2 |
| Lưu trú | thẻ dưới lịch | thẻ "khu nên ở + link" của plan lưu trú (E) hiện dưới lịch từ 2 ngày | bảng khu (User duyệt, plan của E) | 100 % lịch ≥ 2 ngày có thẻ; 0 số tiền | 2 |
| Dịch vụ / đi lại | dòng dưới mỗi ngày | câu cố định theo cụm ("các điểm ngày này cách trung tâm ~N km, nên đi …") | bài đi lại của đợt bổ sung kho 3 + khoảng cách cụm (toạ độ đã có) | lịch có cụm xa ⇒ 100 % có dòng đi lại | 2 |
| Đổi / bỏ một điểm | nút trên từng dòng lịch | hành động có tên gửi về server, code xếp lại, trả "đổi gì / giữ gì" (nền: nhánh sửa lịch đang hoãn) | khung giữ ở server trong phiên | bộ chuỗi sửa đã viết (10 + 5), đạt 2 / 2 lượt | 3 |
| Bản đồ | dưới lịch | ghim số theo thứ tự (code đã có, cờ tắt) | toạ độ (phiếu gộp bảng D) | 100 % điểm trong lịch có ghim hoặc ghi chú "chưa có toạ độ" | 3 (hoặc sớm hơn khi User duyệt toạ độ) |

**Không làm ở bản 2** (ghi để khỏi đề xuất lại): model tự viết lịch từ câu gõ tự do (2 lần chưa đạt); nói giá phòng; đặt chỗ; đăng nhập / lưu lịch theo tài khoản; kéo thả; tiếng Anh.

## 4. Ba đợt

| | Đợt 1 — "biểu mẫu đủ ô, ô nào cũng chạy" | Đợt 2 — "lịch như lịch thật" | Đợt 3 — "sửa trên lịch + bản đồ" |
|---|---|---|---|
| Điều kiện vào | User xem xong phiếu gộp (ưu tiên, thời lượng, trong nhà / bậc thang) | đợt 1 đạt + "đợt bổ sung kho 3" (E viết spec) đã vào kho + bảng vé User duyệt | đợt 2 đạt (bản đồ có thể tách làm sớm) |
| Có gì | số ngày + / − · trẻ em · người lớn tuổi · người lớn · kiểu đi 3 mức · thích gì (≤ 2) · ngày khởi hành (thứ, mùa, dự báo) · điểm ưu tiên (plan đã có) | ngân sách theo vé · bữa ăn · thẻ lưu trú · dòng đi lại · giờ gợi ý theo buổi do code in | đổi / bỏ điểm bằng nút · bản đồ ghim |
| Chạm | bảng điểm (v8 / v9) · `lich_trinh.py` (`ThamSo`, `xep`, ghi chú) · `hoi_lai.py` (`TruongInput`) · `assistant.py` (`answer_bieu_mau` + gọi dự báo) · `pages.jsx` · test | + bảng vé, bảng quán theo cụm · khung thêm bữa ăn / tổng vé · thẻ lưu trú | + API hành động sửa · `chat.jsx` · bật cờ bản đồ |
| Ước giờ | ~2 ngày agent (B code, C / E đo + review) | ~3 ngày | ~2 ngày |
| Ước tiền | ≤ 0,15 USD | ≤ 0,25 USD | ≤ 0,15 USD |

Mỗi đợt một plan riêng (viết sau khi User duyệt spec này), một nhánh, một review cả nhánh; phần luật xếp review riêng vì là chỗ dễ sai nhất.

## 5. Giao diện + hợp đồng dữ liệu

- **Một trang, năm nhóm theo câu hỏi người đi tự đặt** (không theo bố cục trang khác): "Ai đi?" (người lớn, trẻ em bằng nút + / −; ô đánh dấu "có người lớn tuổi") · "Đi bao lâu, khi nào?"
  (số ngày + / −; ô chọn ngày của trình duyệt, để trống được) · "Đi kiểu nào?" (3 nút, mỗi nút một dòng giải thích bằng số: "~2 / ~4 / ~6 điểm một ngày") · "Thích gì?" (nút chọn nhiều, tối đa 2)
  · (đợt 2) "Chi tiêu cho vé tham quan". Dưới cùng: dòng tóm tắt lựa chọn + nút xếp lịch. Lựa chọn nào chưa có tác dụng với tổ hợp hiện tại (vd "khám phá nhiều" khi có trẻ em) ⇒ hiện dòng
  nhỏ nói rõ, không âm thầm bỏ qua.
- **Kỹ thuật:** phần tử HTML sẵn có (`button`, `input type="date"`, `input type="checkbox"`); **0 gói npm mới; CSP không đổi**; dùng được bằng bàn phím; khổ điện thoại một cột.
  Kiểm Playwright một khổ màn điện thoại + một khổ máy tính trên bản build do FastAPI phục vụ.
- **Hợp đồng `truong` (server kiểm, trường lạ ⇒ 422, như hôm nay):** `so_ngay` "1"–"5" (và "4+" cũ) · `nguoi_lon` 1–10 · `tre_em` 0–6 · `lon_tuoi` bool · `kieu_di`
  `nhe_nhang` / `can_bang` / `kham_pha` (nhận tên cũ `thong_tha`, `day_lich`) · `so_thich` danh sách ≤ 2 (nhận chuỗi đơn cũ) · `ngay_di` ngày ISO, không ở quá khứ, ≤ 180 ngày ·
  (đợt 2) `ngan_sach`. `di_cung` cũ vẫn nhận để thẻ "Sửa" của lịch cũ không vỡ; code đổi sang trường mới.
- **Lời model:** vẫn một lần gọi, không công cụ, chỉ diễn đạt khung (như đợt 1 cũ). Mọi dòng có số (giờ gợi ý, tổng vé, khoảng cách, lưu ý mùa, dự báo) do **code nối vào khối ghi chú / khung**;
  kiểm cuối thêm luật "chữ model không chứa số tiền / giờ ngoài tập của khung".
- **Dữ liệu người dùng:** các ô chỉ là lựa chọn + một ngày; không tên, không liên hệ; không lưu ngoài RAM của phiên (như hôm nay); log chỉ thêm số đếm (số ngày, có / không trẻ em, kiểu đi…), không nội dung.

## 6. Tiêu chí ghi trước

**Chung cho mọi đợt (sàn):** `kiem_khung` 0 lỗi trên toàn bộ tổ hợp mô phỏng · nhóm hạn chế 0 buổi tối · 0 ngày ghép hai cụm không kề · kiểm cuối 0 lỗi trên bộ lịch thật ·
an toàn 32 ×2 không đổi (lượt không phải biểu mẫu: chuỗi gửi model giống byte ⇒ dùng lại số; khác ⇒ chạy) · 0 câu ngoài phạm vi bị trả lời.

| Đợt | Mô phỏng 0 USD | Bộ lịch thật (có phí) | Người chấm |
|---|---|---|---|
| 1 | mọi tiêu chí "đổi lịch" của các ô đợt 1 ở mục 3; điểm ưu tiên theo plan điểm ưu tiên; số điểm "không bao giờ được xếp" ≤ 3 (mỗi điểm còn lại có lý do ghi rõ) | 20 yêu cầu ghi trước (phủ: 5 mức số ngày, có / không trẻ em, có / không lớn tuổi, 3 kiểu đi, 1 và 2 sở thích, 4 kiểu ngày đi) ×1: 20 / 20 qua kiểm cuối, 0 rút, 0 từ chối; trung vị cả câu ≤ 8 giây | bộ quyết 12 tổ hợp mới ×2, hai người chấm độc lập: ≥ 11 / 12 mỗi lượt cho "lịch khớp điều đã chọn" (định nghĩa ghi ở plan trước khi chấm) |
| 2 | tiêu chí ngân sách, bữa ăn, lưu trú, đi lại ở mục 3; tổng vé in ra = tính lại độc lập 100 % | 20 yêu cầu ×1 như trên + 0 số tiền do model viết; 0 quán nằm ngoài bảng | như đợt 1, thêm ý "bữa ăn hợp khu" |
| 3 | mọi hành động sửa giữ sàn chung | bộ chuỗi sửa đã viết (10 đã thấy), đạt ở cả 2 lượt | Playwright: đổi / bỏ điểm bằng nút trên 2 khổ màn |

So với Huế TRIPO (không phải sàn, báo cho User): cùng 6 yêu cầu ghi trước gửi hai bên sau mỗi đợt — bảng "ô nào hai bên đều có · lịch bên nào dùng được hơn · lỗi thấy được".

## 7. Rà theo khung AI FDE

| Mục | Thiết kế | Khớp / rủi ro |
|---|---|---|
| Có cần model không | xếp, chọn, tính, kiểm: code. Model chỉ viết lời cho khung (một lần gọi) | khớp |
| Phép tính / luật / thứ tự ⇒ code | số suất theo kiểu đi, luật nhóm, thứ + mùa + dự báo, tổng vé, khoảng cách bữa ăn | khớp — rút từ lần tính tiền trước bị âm vì để model tính |
| Công cụ + tham số | lượt biểu mẫu không đưa công cụ cho model (như hôm nay); dự báo do code gọi trước | khớp |
| Chữ người dùng là dữ liệu | mọi ô là giá trị trong tập cho phép; ngày và số được kiểm khoảng; không có ô chữ tự do | khớp |
| Đường ra ngoài | chỉ thêm: gọi dự báo thời tiết công khai (đã có) khi có ngày đi; link Maps do code dựng. Không gửi lựa chọn của người dùng cho bên thứ ba ngoài nhà cung cấp model | khớp |
| Dữ liệu cá nhân | không thu tên / liên hệ; ngày đi + số người không lưu ngoài phiên | khớp |
| Đường phục hồi | mỗi đợt một cờ; bảng thiếu cột ⇒ ô tương ứng tự ẩn (`/api/tinh_nang` báo) thay vì hiện ô không chạy; dự báo lỗi ⇒ bỏ phần dự báo, giữ lịch | khớp |
| Đo hai chiều | mỗi ô: "đổi khi nên đổi" (mục 3) ↔ "không phá luật cũ" (sàn chung) | khớp |
| Rủi ro còn | (1) luật xếp phình to ⇒ khó giải thích — chặn bằng "mỗi ô một luật, mỗi luật một test + một dòng trong bài học"; (2) dữ liệu ước (thời lượng từ web) sai ⇒ lịch quá dày — chặn bằng lấy mức trên + nhóm hạn chế luôn ở mức nhẹ; (3) ngày đi xa hơn 7 ngày không có dự báo ⇒ chỉ dùng thứ + mùa, nói rõ | theo dõi |

## 8. Câu hỏi cho User (4 câu, mỗi câu có khuyến nghị)

**Câu 1 — Số ngày tối đa trên biểu mẫu?**
- **(a) 5 ngày** *(khuyến nghị)*: bảng 28–33 điểm đủ cho 5 ngày không lặp. Khi nào sai: khách đi dài hơn — lịch ghi "mình xếp 5 ngày đầu".
- (b) 7 ngày như một số trang khác: cần thêm ~10–15 điểm vào bảng trước (thêm một vòng phiếu); chọn (b) mà chưa thêm điểm ⇒ ngày 6–7 trống hoặc lặp.

**Câu 2 — Ô "số người lớn" hiện từ đợt 1 dù tới đợt 2 mới đổi lịch (nhân vé)?**
- **(a) Hiện từ đợt 1** *(khuyến nghị)*: đặt cạnh ô trẻ em thì người dùng mới hiểu; đợt 1 nó chỉ vào dòng "Mình hiểu" và lời văn — spec ghi rõ đây là ngoại lệ duy nhất của nguyên tắc
  "ô nào hiện thì đổi lịch". Khi nào sai: anh muốn giữ nguyên tắc tuyệt đối.
- (b) Chỉ hiện ô trẻ em + người lớn tuổi ở đợt 1; ô người lớn thêm ở đợt 2 cùng ngân sách.

**Câu 3 — Ngân sách tính theo gì?**
- **(a) Chỉ vé tham quan, do code cộng từ bảng vé anh duyệt** *(khuyến nghị)*: con số kiểm được, có ngày nguồn. Mất gì: không gồm ăn, ở, đi lại ⇒ phải ghi rõ "chỉ là vé tham quan".
- (b) Thêm mức ăn uống ước theo bữa: cần bảng giá món có cấu trúc (kho có giá ở ~79 bài món nhưng chưa thành bảng) ⇒ thêm một vòng dữ liệu, dễ sai hơn.
- (c) Không làm ngân sách ở bản 2 (lần tính tiền trước đã âm) — bỏ hàng này khỏi đợt 2.

**Câu 4 — Loại hình ("Thích gì") — số loại?**
- **(a) Giữ các loại bảng đủ điểm, ẩn loại dưới 4 điểm** *(khuyến nghị)*: hôm nay còn 4 loại (di tích, thiên nhiên, ẩm thực, chụp ảnh); "lễ hội, nghệ thuật" ẩn cho tới khi có ≥ 4 điểm.
- (b) Bổ sung dữ liệu để có thêm loại (bảo tàng – giáo dục, làng nghề – cộng đồng, nghỉ dưỡng biển): mỗi loại cần ≥ 4 điểm có bài trong kho ⇒ gộp vào đợt bổ sung kho; làm sau đợt 1.

## 9. Phụ thuộc và thứ tự

1. User xem phiếu gộp ⇒ bảng v8 (ưu tiên) ⇒ v9 (thời lượng, trong nhà, bậc thang) — đang chờ.
2. Plan điểm ưu tiên (đã có nháp) chạy trước, là bước đầu của đợt 1.
3. Đợt 2 chờ: spec "đợt bổ sung kho 3" của E (lưu trú, đi lại, định vị quán) + bảng vé + toạ độ quán (E đang tra thêm).
4. Tiền: ba đợt ước ≤ 0,55 USD — vượt phần còn lại của trần Phase 9 hiện tại ⇒ A xin User khi duyệt spec.
