# Plan — "Lên kế hoạch" đợt 1: khung lịch tốt + biểu mẫu đủ · NHÁP bản 2

Người viết: C · bản 1 21:57, **bản 2 22:02 12/11/2026** (`date`; bản 2 = sau khi E kiểm xong mục 5c của spec + User trả lời phiếu nhỏ đợt 1) · Người code: B · Người đọc plan trước: B (người code) · Người duyệt: A · Mức rủi ro: **cao** (luật xếp + đổi khuôn trả lời)
Chưa code. Plan này chỉ làm **đợt 1** của spec; đợt 2 (ảnh, bản đồ) và đợt 3 (ăn uống, lưu trú) có plan riêng.
Repo public: tên điểm cụ thể, bảng điểm, bộ đo nằm ở `data/` (private); plan chỉ ghi đường dẫn + số đếm.

## Căn cứ để review (`WORKFLOW.md` §9.1)

- Spec: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` **bản 3.3** (sha256 `8c521ecdc80d`; bản 3.2 ở commit `ccddaee`) — mục 3.1, 3.2 (hai dòng tham quan / buổi tối), 4 (cột đợt 1), 5, **5b** (thứ tự luật + thứ tự merge),
  **5c** (tám quyết định), 6 (tiêu chí đợt 1). **E đã kiểm mục 5c** (sửa chữ / số, không cần vòng nữa — cuối file `…-len-ke-hoach-ban-2-design_review.md`); bản 3.3 + plan này đã nhận hết.
- Code đang chạy: `backend/llm/lich_trinh.py` (`nap_bang`, `ThamSo`, `xep`, `_cum_hop`, `kiem_khung`, `khung_chu`, `kiem_cuoi`, `ban_do`) · `backend/llm/hoi_lai.py` (`GIA_TRI`, `TruongInput`, `ghep_cau`) ·
  `backend/llm/assistant.py` (`AssistantFlags`, `answer_bieu_mau`) · `backend/llm/answer_stream.py` (`AnswerTextStream`) · `backend/llm/thoi_tiet.py` (`NGUONG_MUA`) · `backend/llm/ngay_lich.py` ·
  `backend/api/routes/chat.py`, `cong.py` (`/api/tinh_nang`) · `frontend/src/pages.jsx` (`LenKeHoach`), `chat.jsx` (thẻ lịch) · test: `backend/tests/test_b5_lich_trinh.py`, `test_ngay_lich.py`, `test_cong_dot_1.py`.
- Dữ liệu private: bảng đề xuất `data/phase_9/lich_trinh/diem_v8_de_xuat.json` (34 dòng = 33 điểm + 1 hoạt động buổi tối; đã có cả cột thứ / mùa theo câu trả lời phiếu nhỏ; md5 `0cbd845ede30`) · phiếu nhỏ `…/phieu_nho_dot_1_2026-11-12.md` · bộ đo của E `data/phase_9/lich_trinh/bo_do_v2/` (đang viết).
- Script mô phỏng 0 USD (của C, chạy lại được): `data/phase_9/lich_trinh/tools/mo_phong_v8.py` (360 tổ hợp cũ qua bộ xếp **thật**) · `…/tools/mo_phong_kieu_di.py` (bản thử luật mới: phút, ưu tiên, cụm xa).

## 1. Việc và phạm vi

**Làm:** hợp đồng `truong` mới + biểu mẫu bốn nhóm · bảng v8 (rồi v9) · bộ xếp mới (ưu tiên theo sở thích, kiểu đi bằng phút, hai sở thích, trẻ em / lớn tuổi) · khuôn dữ liệu `lich` + model trả mảng `{id_muc, cau}` + kiểm cuối
theo câu · ngày đi (thứ, mùa, dự báo) · buổi tối + giờ gợi ý. Tất cả sau **một cờ** `assistant.len_ke_hoach_v2` (mặc định tắt).
**Không làm ở đợt 1:** ảnh, bản đồ mới, ăn uống, lưu trú, ngân sách, ba phương án, đổi / bỏ điểm, tiếng Anh; đường lịch trình **câu tự do** (chat) giữ nguyên bảng + luật cũ; không đổi kho, chỉ mục, lời dặn của trợ lý chat.
**Không được đổi khi cờ tắt:** mọi chuỗi gửi model và mọi phản hồi của đường biểu mẫu hôm nay (kiểm bằng bộ mốc giống byte đang có).

## 2. Phụ thuộc còn mở (ghi rõ để không ai tưởng đã xong)

| # | Còn mở | Cách đi tiếp mà không chờ |
|---|---|---|
| P1 | User **chưa liếc** danh sách ưu tiên theo sở thích (bảng v8) | dùng giá trị đề xuất làm mặc định; ưu tiên nằm ở **cột `uu_tien` của bảng** ⇒ User đổi = sửa bảng, **không đổi code**; test không khoá tên điểm cụ thể, chỉ khoá luật |
| P2 | ~~phiếu nhỏ đợt 1~~ — **User đã trả lời (12/11):** phố quán bờ nam xếp mọi tối + ghi chú ngày cấm xe · điểm tạm dừng theo mùa bỏ hẳn khỏi lịch trong mùa dừng · chỉ một dòng nhắc mưa chung khi đi tháng 9–12 | đã vào bảng đề xuất + spec 5c.2. Còn một ô User chưa điền: giờ + thứ của phố đêm cạnh Kinh thành ⇒ **không thêm** điểm đó (thêm sau = sửa bảng) |
| P3 | ~~E kiểm mục 5c~~ — **xong**, đã sửa: trần 2 điểm / buổi · chiều bắt đầu sớm 30 phút · định nghĩa chấm (3), (4) · điểm tạm dừng thắng ưu tiên | — |
| P4 | Bộ đo 20 + 12 của E **chưa xong** | phải xong + ghi mã băm vào mục 6 **trước khi B bắt đầu bước (b)**; B không đọc bộ quyết 12 tổ hợp trước khi chạy |
| P5 | Luật "điểm ưu tiên cụm xa xếp ngày 2" | **đã mô phỏng** (21:57 12/11, bản thử): 0 / 180 lịch có điểm cụm xa ở ngày 1; sở thích thiên nhiên từ 3 ngày: điểm ưu tiên số 1 nằm đúng ngày 2 ở 18 / 18; các số khác không đổi (80 % · 1 điểm ban ngày không bao giờ xếp). Luật thử = "ngày 1 không xét điểm cụm xa" |
| P6 | Báo cáo B thử đủ luồng lập kế hoạch của trang kia | đầu vào cho mục 2 của spec; nếu thêm bất biến mới ⇒ C sửa plan trước bước (c) |

## 3. Các bước — đúng thứ tự merge (a) ⇒ (e); mỗi bước một nhánh nhỏ, cờ tắt, giống byte khi tắt

Quy ước mỗi bước: **test viết trước** (đỏ rồi mới code) · mô phỏng 0 USD chạy trong test (không gọi model) · xong bước nào báo A số đo của bước đó.

### (a) Hợp đồng `truong` mới + biểu mẫu mới, bộ xếp cũ

- **Chạm:** `hoi_lai.py` (`GIA_TRI`, `TruongInput`: thêm `nguoi_lon` 1–10, `tre_em` 0–6, `lon_tuoi` bool, `kieu_di` ba mức, `so_thich` danh sách ≤ 2, `ngay_di` ISO; `so_ngay` "1"–"5"; nhận giá trị cũ) · hàm đổi trường mới ⇒
  `ThamSo` cũ (tạm, để `xep` cũ chạy) · `assistant.py` (`AssistantFlags.len_ke_hoach_v2`) · `cong.py` (`/api/tinh_nang` trả `len_ke_hoach_v2` + **danh sách ô hiện**) · `pages.jsx` (`LenKeHoach`: bốn nhóm, phần tử HTML sẵn có).
- **Luật của bước này:** ô nào chưa có tác dụng với bộ xếp cũ thì **chưa hiện** (danh sách ô hiện ban đầu = các ô hôm nay). Bước (b)–(e) mở dần từng ô.
- **Test viết trước:** bảng giá trị hợp lệ / không hợp lệ của từng trường (trường lạ, số ngoài miền, ngày quá khứ, ngày > 180 ngày, 3 sở thích ⇒ 422) · giá trị cũ (`di_cung`, "4+", `thong_tha`, `day_lich`, sở thích chuỗi đơn) đổi đúng
  sang trường mới · cờ tắt ⇒ `/api/tinh_nang` và phản hồi biểu mẫu **giống byte** hôm nay · Playwright 2 khổ màn: dùng được bằng bàn phím, ô ẩn không có trong DOM.
- **Tiêu chí:** *Luôn* — 100 % ca của bảng giá trị; cờ tắt giống byte. Không có sàn (chưa đổi lịch). **0 USD.**

### (b) Bảng v8 + bộ xếp mới + mô phỏng

- **Chạm:** bảng mới `data/phase_9/lich_trinh/diem_v8.json` (từ bản đề xuất, sau P1 hoặc dùng mặc định) + cấu hình đường dẫn bảng cho cờ mới (bảng cũ giữ cho cờ cũ và đường chat) · `lich_trinh.py`: `nap_bang` (cột v8 bắt buộc khi
  cờ bật), `ThamSo` mới, **`xep` mới viết thành hàm riêng** (`xep_v2`, không sửa `xep` cũ), `kiem_khung_v2` · danh sách chừa của bản Docker (file bảng mới — bài học 10/11: thiếu file cấu hình ⇒ tính năng tắt im lặng).
- **Luật phải code (spec 5b thứ tự 1–7, 5c.3, 5c.4):** thứ tự xét (điểm nêu ⇒ ưu tiên của sở thích ⇒ hợp sở thích ⇒ di tích lấp có nhãn) · hai sở thích xen kẽ · quỹ phút mỗi buổi (75 / 150 phút; đi lại 15 / 30; quỹ 210 / 240;
  tối đa **2 điểm / buổi**) · ≤ 2 cụm kề / ngày tính trên mọi điểm sáng + chiều · cụm xa chỉ từ 3 ngày và **không ở ngày 1** · nhóm hạn chế (trẻ em ≥ 1 hoặc lớn tuổi): 1 điểm / buổi, không tối, tránh điểm nhiều bậc thang khi cùng cụm có
  điểm thay, điểm ưu tiên bị thay vì bậc thang ⇒ dòng ghi chú do code · `nguoi_lon` không vào bộ xếp.
- **Test viết trước:** mỗi luật một test + test từng cặp luật kề nhau trong thứ tự 5b (vd ưu tiên ↔ cụm kề; bậc thang ↔ ưu tiên) · **mô phỏng toàn bộ tổ hợp** (5 số ngày × trẻ em 0 / ≥ 1 × lớn tuổi × 3 kiểu đi × 16 lựa chọn sở thích =
  960 khung; ngày đi thêm ở bước (d)) chạy trong pytest, kiểm bất biến dưới đây.
- **Tiêu chí (mô phỏng 0 USD, ghi trước):**

  | Loại | Điều kiện | Số của bản thử C (để B biết mình lệch ở đâu) |
  |---|---|---|
  | Luôn | `kiem_khung_v2` 0 lỗi · 0 điểm lặp · 0 ngày rỗng · 0 ngày > 2 cụm hoặc ghép cụm không kề · khung n ngày có đúng n ngày | 0 · 0 · 0 · 0 trên 180 lịch |
  | Luôn | điểm ưu tiên số 1 của mỗi sở thích đã chọn có mặt (trừ điểm cụm xa khi < 3 ngày) | 30 / 30 ở cả 6 lựa chọn |
  | Luôn | lịch ≥ 3 ngày: ngày 1 không có điểm cụm xa; điểm ưu tiên cụm xa có mặt đúng **một** ngày trong các ngày 2…n; 0 ngày rỗng; tổng số điểm của lịch không giảm so với khi chưa có luật này | 0 / 180 · 18 / 18 (ở ngày 2) · 0 · trung bình không đổi |
  | Luôn | tổng số điểm của lịch: nhẹ nhàng ≤ cân bằng ≤ khám phá nhiều; nhóm hạn chế ba mức cho cùng một khung | 60 / 60 nhóm |
  | Luôn | có trẻ em / lớn tuổi ⇒ 0 điểm tham quan buổi tối, ≤ 2 điểm / ngày · chọn 2 sở thích ⇒ cả hai có mặt trong lịch từ 2 ngày · đổi `nguoi_lon` ⇒ khung giống hệt | chưa thử (bản thử chỉ có một sở thích) |
  | Sàn | ba mức kiểu đi cho ba khung khác nhau ở **≥ 70 %** nhóm không hạn chế | 24 / 30 = 80 % |
  | Sàn | số điểm nhiều bậc thang giảm ở **≥ 50 %** tổ hợp có trẻ em / lớn tuổi so với không · mỗi sở thích chiếm **≥ 50 %** suất sáng / chiều của lịch 2 ngày | chưa thử |
  | Sàn | điểm ban ngày không bao giờ được xếp **≤ 3**, mỗi điểm có lý do ghi trong report | 1 (một lăng xa) |

  Dưới sàn ⇒ **ô đó không hiện** (bỏ khỏi danh sách ô hiện), không hạ ngưỡng, chỉnh luật tối đa một vòng. Sai một "Luôn" ⇒ sửa code.
- **Lưu ý cho B:** bản thử của C chỉ là script đếm (`mo_phong_kieu_di.py`), chưa có hai sở thích, bậc thang, giờ mở cửa — đừng chép; số ở cột phải là **mốc so**, lệch nhiều thì tìm lý do trước khi đi tiếp. **0 USD.**

### (c) Khuôn dữ liệu mới + model trả mảng `{id_muc, cau}` + kiểm cuối theo câu + lượt thử có phí sớm

- **Chạm:** `lich_trinh.py` (dựng `lich` phiên bản 2 theo spec 5c.5: `id_muc` dạng `n<ngày>-<buổi>-<thứ tự>`; hàm ghép `answer` chữ thuần từ khung + câu; `kiem_cau` mới thay phần dò dòng của `kiem_cuoi` — `kiem_cuoi` cũ giữ cho
  đường cũ) · `assistant.py` (`answer_bieu_mau`: nhánh v2 — phát `lich_khung` trước lần gọi model, lược đồ đầu ra mảng, câu dự phòng do code, **bỏ nhánh rút cả lịch** ở v2) · `answer_stream.py` (phát một `lich_cau` mỗi khi một
  phần tử đóng ngoặc — mức "nguyên câu từng mục") · `chat.py` (ba sự kiện `lich_khung` / `lich_cau` / `lich_xong`; lượt không hiện dần trả `lich` + `cau`) · `chat.jsx` (thẻ lịch vẽ **từ khung**, câu đổ vào theo `id_muc`,
  loại mục không biết ⇒ bỏ qua).
- **Lượt thử có phí SỚM (làm ngay khi khung v2 in ra được, trước khi viết đủ test) — ≤ 0,005 USD:** 6 khung (1, 3, 5 ngày × có / không nhóm hạn chế), mỗi khung 1 lần gọi. Đếm và ghi report: tỉ lệ thiếu mục · lặp `id_muc` ·
  gộp hai mục một câu · câu có giờ / số tiền / tên điểm khác · **tỉ lệ câu bị thay NHẦM** do luật "tên điểm khác" (tên con nằm trong điểm lớn — đọc tay 6 khung) · thời gian tới `lich_khung` và tới đủ câu. **Luật dừng:** > 30 % mục phải dùng câu dự phòng ở ≥ 2 / 6 khung ⇒ dừng, báo A (khuôn tin nhắn gửi model sai, không viết tiếp test).
- **Test viết trước (model giả, 0 USD):** thiếu mục ⇒ câu dự phòng · lặp id ⇒ lấy phần tử đầu · id lạ ⇒ bỏ · câu chứa giờ / thời lượng / tiền / đường dẫn / tên điểm khác / mã trích dẫn ngoài nguồn của mục ⇒ câu dự phòng riêng mục đó ·
  model lỗi / hết giờ / từ chối ⇒ lịch vẫn đủ khung, `so_cau_du_phong` = số mục · thứ tự sự kiện `lich_khung` ⇒ `lich_cau`* ⇒ `lich_xong` · `answer` chữ thuần ghép đúng · chữ người dùng không vào được khung (chỉ giá trị `truong`).
- **Tiêu chí:** *Luôn* — 0 giờ / số tiền / tên ngoài khung trong câu lọt ra; model hỏng không làm mất lịch. *Sàn* — đo ở bước nghiệm thu (mục 5): ≤ 1 câu dự phòng / lịch ở ≥ 18 / 20; `lich_khung` ≤ 1 giây.

### (d) Ngày đi: thứ, mùa, dự báo

- **Chạm:** bảng `diem_v9.json` (thêm `ngay_hoat_dong`, `gio_toi`, `mua_luu_y` — giá trị theo phiếu nhỏ, P2) · `lich_trinh.py` (`xep_v2` nhận ngày của từng ngày lịch: tháng ⇒ luật mùa 5c.2; dự báo ⇒ luật mưa) ·
  `assistant.py` (lấy dự báo bằng hàm đang có, chỉ khi ngày trong 7 ngày tới) · `ngay_lich.py` (ngày ⇒ thứ, giờ Việt Nam).
- **Luật (5c.2 bản 3.3):** xét theo **ngày** · điểm `bo_khoi_lich` trùng tháng ⇒ không xếp, **thắng cả luật ưu tiên**, có ghi chú `tam_dung_mua` · **không** hạ điểm theo mùa, **không** in lưu ý mùa theo từng điểm · mưa = khả năng mưa ≥ `NGUONG_MUA` (60 %, hằng số đang
  có, không thêm số mới) ⇒ điểm không ưu tiên xét theo trong nhà ⇒ cả hai ⇒ ngoài trời · dự báo lỗi ⇒ như không có dự báo · lịch có ngày rơi vào tháng 9–12 ⇒ đúng **một** dòng nhắc chung, chữ lấy từ trường `nhac_mua_chung` của bảng (User đã duyệt chữ).
- **Test viết trước:** mỗi luật một test với ngày cố định (không phụ thuộc đồng hồ máy; **hàm dự báo ghi sẵn 3 kịch bản**: không mưa · mưa ngày 1 · mưa mọi ngày — cách đo của E) · lịch vắt hai tháng · ngày thứ 8 trở đi không gọi dự báo · mô phỏng thêm chiều "4 kiểu ngày đi" (không ngày · mùa khô giữa tuần ·
  mùa mưa cuối tuần · trong 7 ngày có mưa) ⇒ 3.840 khung.
- **Tiêu chí:** *Luôn* — 0 điểm tạm dừng theo mùa được xếp trong tháng dừng (kể cả khi là điểm ưu tiên); đi tháng 9–12 ⇒ đúng một dòng nhắc mưa, tháng khác ⇒ 0 dòng; ngoài 7 ngày ⇒ 0 dòng dự báo; các bất biến của (b) vẫn đúng trên 3.840 khung.
  *Sàn* — đổi "mùa khô, giữa tuần" ↔ "mùa mưa, cuối tuần" ⇒ khung hoặc ghi chú khác ở **≥ 60 %** tổ hợp có điểm ngoài trời. Lượt gọi dự báo lạnh đo riêng (mục 5). **0 USD** (dự báo miễn phí, đã dùng).

### (e) Buổi tối + giờ gợi ý

- **Chạm:** `lich_trinh.py` (chọn hoạt động tối **sau khi** khung tham quan chốt — không làm đổi khung; in `gio` cho mọi mục theo 5c.3; cắt theo giờ mở cửa) · bảng v9 (dòng hoạt động tối mới nếu User nhận ở phiếu nhỏ) · `chat.jsx` (hiện giờ).
- **Luật (5c.3, 5c.4):** giờ bắt đầu 8:00 / **13:30** (khám phá nhiều 7:30 / **13:00**) ⇒ buổi chiều xong muộn nhất 17:00, cộng phút tham quan + phút đi; điểm mở muộn ⇒ dời cả buổi; vượt giờ đóng ⇒ không thêm · buổi tối: nhóm không hạn chế mỗi tối một hoạt động **đúng thứ**,
  chỉ ở hai cụm trung tâm, không tính vào 2 cụm, không lặp tới khi hết (hết ⇒ lặp hoạt động hằng đêm, nhãn "có thể đi lại"); ngày cụm xa ⇒ dòng "tối nghỉ" do code; nhóm hạn chế ⇒ dòng "tối nghỉ" đang có.
- **Test viết trước:** bảng ca giờ (2 ngắn cùng cụm · ngắn + ngắn cụm kề · nửa buổi + ngắn · điểm mở muộn · điểm đóng sớm) so đúng chuỗi giờ · mỗi thứ trong tuần × 5 số ngày: 0 hoạt động sai thứ · ngày cụm xa không có tối.
- **Tiêu chí:** *Luôn* — 0 khung giờ ngoài giờ mở cửa (giờ kết thúc ≤ giờ đóng của bảng, kiểm bằng code trên mọi tổ hợp) · giờ các mục trong một buổi không chồng nhau, tăng dần · 0 hoạt động tối sai thứ · có trẻ em ⇒ 0 mục sau 21:00. *Sàn* — **≥ 80 %** số tối (không tính ngày cụm xa) của lịch
  nhóm không hạn chế có hoạt động. Dưới sàn (vd User siết thứ ở phiếu nhỏ) ⇒ phần buổi tối chỉ hiện khi ngày đi có đủ hoạt động, báo A. **0 USD.**

## 4. Sàn chung (mọi bước, ghi trước)

- **Cờ tắt = hôm nay:** bộ mốc giống byte của đường biểu mẫu + chat (Q1) **0 khác**; mốc quyết bật cờ `lich_trinh_bieu_mau` cũ (120 tổ hợp tất định trong test + bộ 12 ×2) vẫn đạt **khi cờ mới tắt** — chạy lại phần tất định (0 USD)
  ở mỗi bước; phần có phí của mốc cũ **không chạy lại** nếu chuỗi gửi model giống byte (chứng minh bằng test so chuỗi).
- **An toàn 32 ×2:** lượt không phải biểu mẫu có chuỗi gửi model giống byte ⇒ dùng lại số; khác byte ⇒ chạy lại (tiền tính riêng, báo A trước).
- 0 câu ngoài phạm vi được trả lời · `kiem_khung` cũ 0 lỗi trên 360 tổ hợp cũ (`mo_phong_v8.py`, cấu hình A) · toàn bộ pytest + Playwright hiện có xanh · `git diff --check` sạch.
- Dữ liệu người dùng: chỉ lựa chọn + một ngày; log chỉ thêm số đếm (không chữ, không ngày đi nguyên văn — chỉ "có / không ngày đi").

## 5. Nghiệm thu đợt 1 (sau bước (e), một lần)

| Việc | Tiêu chí ghi trước | Tiền ước |
|---|---|---|
| Mô phỏng 3.840 khung | mọi "Luôn" của (b), (d), (e); các sàn 70 / 60 / 50 / 80 %; điểm ban ngày không bao giờ xếp ≤ 3 | 0 |
| Bộ lịch thật: 20 yêu cầu của E ×1 | 20 / 20 có đủ khung, 0 từ chối; ≤ 1 câu dự phòng / lịch ở ≥ 18 / 20, không lịch nào > 30 % câu dự phòng; `lich_khung` ≤ 1 giây; đủ câu: trung vị không chậm hơn mốc `main` cùng buổi quá 2 giây (mốc 12/11: 4,9 giây) — đo bằng hai mốc mới (khung hiện · đủ câu), **không so với số "chữ đầu" cũ** của log; lượt dự báo lạnh ≤ mốc + 4 giây, báo riêng | ≈ 0,02 |
| Bộ quyết: 12 tổ hợp của E ×2, hai người chấm độc lập (không phải B, không phải C) | ≥ 11 / 12 mỗi lượt theo định nghĩa "lịch khớp điều đã chọn" (spec 5c.7 bản 3.3: ý (3) kiểu đi do **code đếm theo cặp**, người chấm chấm 5 ý còn lại; ý (4) có ngoại lệ luật cứng) | ≈ 0,03 + chấm ≈ 0,02 |
| Playwright 2 khổ màn trên bản build do FastAPI phục vụ | biểu mẫu dùng được bằng bàn phím; khung hiện trước câu; 0 lỗi console; 0 yêu cầu mạng ngoài danh sách CSP | 0 |
| Review cả nhánh (một vòng; phần luật xếp review riêng) | 0 blocker / major còn mở | 0 |

Bộ đo: `data/phase_9/lich_trinh/bo_do_v2/` — mã băm hai file: *(E điền khi xong — P4)*. Giữ / gỡ: đạt hết ⇒ A bật cờ (sau D4); trượt một sàn của ô ⇒ ô đó ẩn, phần còn lại vẫn bật được; trượt "Luôn" hoặc bộ quyết ⇒ không bật.

## 6. Tiền · giờ

- **Trần đợt 1: ≤ 0,20 USD.** Ước: lượt thử sớm 0,005 + bộ lịch thật 0,02 + bộ quyết 0,03 + chấm 0,02 + dự phòng chạy lại một vòng 0,05 ≈ **0,125**. Chạm 0,15 ⇒ báo A trước khi chạy tiếp. An toàn 32 ×2 chạy lại (nếu khác byte) tính ngoài.
- Giờ agent: (a) 0,5 ngày · (b) 1,5 ngày · (c) 1,5 ngày · (d) 0,5 ngày · (e) 0,5 ngày · nghiệm thu + review 0,5 ngày ≈ **5 ngày**.
- Máy ~15 GB RAM: mỗi lúc một session chạy server / Playwright; nhắn trước khi chạy.

## 7. Điểm dừng (dừng, báo A, không tự đi tiếp)

- **D1** — sau (a): cờ tắt không giống byte ⇒ dừng.
- **D2** — trong (b): một "Luôn" không sửa được sau một vòng, hoặc sàn kiểu đi < 70 % ⇒ báo A (ẩn ô hay sửa luật là quyết định của A / User).
- **D3** — lượt thử sớm của (c) chạm luật dừng (> 30 % câu dự phòng ở ≥ 2 / 6 khung) hoặc tiền chạm 0,15 USD.
- **D4** — trước khi bật cờ: User đã xem danh sách ưu tiên theo sở thích (P1) và A duyệt số nghiệm thu. B **không** bật cờ.
- Bất cứ lúc nào: phải sửa file ngoài danh sách "Chạm", hoặc thấy spec mâu thuẫn ⇒ dừng, hỏi C / A.

## 8. Rủi ro và đường lùi

| Rủi ro | Dấu hiệu | Xử |
|---|---|---|
| Model trả mảng lệch (thiếu / gộp mục) | lượt thử sớm | câu dự phòng theo mục; quá ngưỡng ⇒ D3 |
| Luật mới làm lịch kém ở tổ hợp ít gặp | mô phỏng toàn tổ hợp | bất biến trong pytest; ô dưới sàn ⇒ ẩn |
| Bảng mới thiếu trong bản Docker ⇒ tính năng tắt im lặng | `/api/tinh_nang` trên bản Docker | thêm vào danh sách chừa + test khởi động: cờ bật mà thiếu bảng ⇒ lỗi rõ |
| Giao diện cũ (bộ đệm trình duyệt) gặp phản hồi mới | — | trường `answer` chữ thuần luôn có; sự kiện lạ bị bỏ qua |
| Giá trị trong bảng (ưu tiên, thứ, mùa) sai ngoài đời | User xem phiếu | sửa bảng, không sửa code; kho là dữ liệu soạn, lịch có dòng "có thể đã thay đổi" đang có |
| **Lùi:** tắt cờ ⇒ về đúng hôm nay (đã chứng minh giống byte ở mỗi bước); không có di trú dữ liệu, không đổi chỉ mục. | | |

## 9. Việc của từng người + thứ tự

1. **B** đọc plan này trước (người code) ⇒ góp ý; **A** duyệt.
2. **E** viết bộ đo 20 + 12 theo định nghĩa bản 3.3, ghi mã băm vào mục 5 (trước bước (b)). (E kiểm 5c: xong.)
3. **B** làm (a) ngay khi A duyệt; (b) sau khi xong việc 2; rồi (c) ⇒ (d) ⇒ (e).
4. **C** (không code đợt này): chạy lại hai script mô phỏng làm mốc so khi B xong (b); review phần luật xếp nếu A giao.
5. **A**: trình User P1, P2; commit; bật cờ sau D4.

## 10. Cần User

Không có câu hỏi mới. Một thứ đang chờ anh xem (đã có giá trị đề xuất; chưa xem thì **cờ chưa bật**): danh sách điểm ưu tiên theo từng sở thích. Tuỳ chọn: giờ + thứ của phố đêm cạnh Kinh thành nếu anh muốn thêm điểm tối đó.
