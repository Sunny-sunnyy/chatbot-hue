# Review cả nhánh `p9-len-ke-hoach-v2` (head `505b53d`) + kết quả hai người chấm mù bộ quyết 12 · E, 14/11/2026

Người kiểm: E (`hue-rag-c4`), không code nhánh này. Lần review trước (13/11, `e_review_len_ke_hoach_dot_1.md`) phủ đợt 1 tới vòng chỉnh. Lần này: 2 commit mới (`56ba164` cột đoạn mô tả, `505b53d` bản đồ trong lịch bản 2), dữ liệu `doan_mo_ta` đã điền, report B §9, cộng phần chấm mù bộ quyết 12 do E giao. 0 USD (không server, không gọi model).

## Kết luận: `changes_requested` — 0 blocker · 1 major · 1 câu cần A quyết · 2 minor
Code hai commit mới gọn, đúng plan, test đạt. Nhưng **bộ quyết 12 trượt sàn theo chữ ghi trước**: mỗi lượt 10 / 12 < 11 / 12 (mục 2). Ngoài ra review tìm ra một lỗi giờ thật trong bộ xếp mà phần kiểm khung không bắt (M-1).

## 1. Đã kiểm
| Kiểm | Cách | Kết quả |
|---|---|---|
| `56ba164` đoạn mô tả | đọc diff: `lay_doan` lọc payload chỉ đọc · bảng bắt `doan_mo_ta` thuộc chính file nguồn · kiểm lúc khởi động đặt ngoài khối bắt lỗi tra cứu · thứ tự đoạn chọn sẵn ⇒ đoạn tìm ⇒ luật cũ | đúng mô tả, không thừa |
| Dữ liệu 10 `doan_mo_ta` | E hỏi Qdrant đang chạy (8.474 đoạn) từng mã: `heading_path` + đầu thân đoạn | 10 / 10 có mặt; 8 mã ở mục "Tổng quan", 2 mã ở mục kiến trúc đúng ý (trường học, sân khấu) |
| `505b53d` bản đồ | đọc diff: toạ độ theo `id_diem`, thiếu ⇒ null, không vào tin nhắn model; số ghim đếm lại theo ngày; màu theo ngày bằng CSS; khoá toạ độ nạp theo bảng v8 khi cờ bản 2 bật | đúng mô tả |
| Test | `pytest tests/test_len_ke_hoach_v2.py tests/test_ban_do_lich.py` trong worktree B | **95 đạt** (20,5 s) |
| Ca dò giờ (mới) | `data/len_ke_hoach_v2_2026-11-13/e_ca_do_chong_buoi.py`: gọi thẳng `xep_v2` trên 3.840 tổ hợp (5 số ngày × trẻ em × lớn tuổi × 3 kiểu đi × 16 sở thích × 4 kiểu ngày) | **52 / 3.840 khung có giờ buổi sáng chồng buổi chiều** (M-1) |

## 2. Bộ quyết 12 ×2 — hai người chấm mù
Hai agent con ngữ cảnh mới (không phải B / C, không mở khoá). Mỗi người đọc định nghĩa chấm, bảng tra `data/len_ke_hoach_v2_2026-11-13/bang_tra_cham_1411.md` (E dựng từ `diem_v8.json` md5 `0fcc90d9a93a`) và 24 file lịch. Kết quả để ở `cham_mu_1411_ket_qua/nguoi_1.jsonl` và `cham_nguoi_2_1411.jsonl`.
- **Hai người cùng gắn "không đạt" đúng 4 / 24 file**, cả 4 ở ý 6. 4 file là **2 tổ hợp × 2 lượt**: lịch có ngày dự báo mưa ≥ 60 % (76 %; 89 %) mà không có dòng "nếu mưa" cho ngày đó. Ghép với khoá là việc của B; nếu đúng 2 tổ hợp thì **mỗi lượt 10 / 12 < sàn 11 / 12**.
- Ý 1, 2, 3 (vế đọc được), 4 đạt 24 / 24 ở cả hai người.
- Phần code chấm của B cho 12 / 12 vì `nghiem_thu.py` (dòng 118) chỉ kiểm vế mùa mưa của ý 6, không kiểm vế dự báo. Hai cách chấm lệch nhau ở đúng vế này.
- **E đọc tay (cần A quyết, mục 3):** ngày mưa ở 2 tổ hợp này không có điểm ngoài trời nào để đổi. Một ngày gồm điểm trong nhà + điểm "cả hai"; ngày kia gồm hai điểm trong nhà + một điểm "cả hai". Code không in dòng "nếu mưa" là có chủ ý: chỉ in khi có điểm thay được. Định nghĩa do E viết lại ghi "có dòng 'nếu mưa'" mà không có ngoại lệ, và hai người chấm đã chấm đúng chữ. Cả hai đều tự nêu đây là chỗ phân vân.

## 3. Câu cần A quyết (E viết định nghĩa ⇒ E không tự sửa thước)
Sàn bộ quyết theo chữ ghi trước: **trượt**. Ba hướng:
- (a) Giữ thước, sửa code: ngày dự báo mưa ≥ 60 % luôn có một dòng. Không có điểm thay ⇒ in "Ngày N khả năng mưa X % — các điểm trong ngày đều trong nhà / có mái". Đây là dòng do code dựng, không qua model. Phải đo lại, mà bộ quyết đã mở ⇒ đo bằng code trên khung hoặc dựng bộ mới. Lợi: người dùng biết ngày mưa vẫn đi được.
- (b) A ghi đây là lỗi của định nghĩa (thiếu ngoại lệ "không có điểm ngoài trời"), áp từ lần đo sau, và ghi rõ lượt này trượt theo chữ. Rẻ nhất, nhưng là đổi thước sau khi đã thấy kết quả.
- (c) Kết hợp: sửa code như (a), kiểm bằng code trên 3.840 khung có dự báo ghi sẵn (0 USD).

**E nghiêng (c)**: lợi thật cho người dùng, không đổi thước, 0 USD.

## 4. Finding
**M-1 (major) — giờ buổi sáng có thể chồng lên buổi chiều; kiểm khung không bắt.**
- Ở đâu: `llm/lich_trinh_v2.py` vòng thêm điểm (khoảng dòng 257–268). Quỹ phút `tong` chỉ cộng thời lượng + phút đi, không tính thời gian chờ khi điểm đầu buổi bị dời tới giờ mở cửa / giờ suất. Ví dụ: điểm sân khấu suất 10:00, thêm điểm nửa buổi ⇒ buổi sáng kéo tới 14:00. `kiem_khung_v2` (khoảng dòng 359–372) kiểm chồng giờ trong cùng buổi, không so giờ kết thúc buổi sáng với giờ đầu buổi chiều.
- Bằng chứng: bộ quyết có 2 / 24 file "Sáng (11:30 – 14:00)" ngay trước "Chiều (13:00 – …)". Hai người chấm đều tự ghi chú lỗi này, dù nó không thuộc ý nào. Ca dò 3.840 khung: **52 khung** sáng chồng chiều, **104 ngày** có buổi sáng kết thúc sau 12:30; mọi ví dụ đều có sở thích lễ hội / nghệ thuật.
- Tác động: lịch người dùng thấy tự mâu thuẫn giờ (hai điểm cùng lúc). Nhẹ hơn lỗi an toàn, nhưng là "nói chắc sai" về giờ gợi ý.
- Đóng khi: điểm thêm buổi sáng chỉ nhận khi giờ kết thúc ≤ giờ đầu buổi chiều (hoặc quỹ tính theo giờ đồng hồ từ giờ bắt đầu buổi). `kiem_khung_v2` thêm mã cho chồng giữa hai buổi. Ca dò 3.840 khung ⇒ 0.

**m-1 — chọn sẵn đoạn theo `file#số` có thể lặng lẽ trỏ sai đoạn.** Bước kiểm lúc khởi động chỉ kiểm mã có mặt. Sau một lần sửa kho đổi số đoạn của file đó, mã vẫn có thể còn nhưng trỏ sang đoạn khác. Lần này 10 / 10 đúng (E kiểm tay). Đóng khi: report / `bai_hoc` ghi luật "sửa kho một trong 10 file nguồn ⇒ kiểm lại cột `doan_mo_ta`". Không cần code thêm.

**m-2 — report B §8 ghi "số trên ghim = số thứ tự các mục có toạ độ".** Code đếm theo mọi mục có link bản đồ, kể cả mục thiếu toạ độ; danh sách bên cạnh dùng cùng số nên vẫn khớp. Đóng khi: sửa chữ trong report.

## 5. Chưa kiểm / giới hạn
- "0 lỗi console khi có bản đồ": vẫn NOT VERIFIED (máy không phân giải DNS host tile). Không thuộc đợt 1; cờ `ban_do_lich` tắt.
- E không chạy lại bộ 20 / Playwright; dùng số của B §9.
- Ghép điểm người chấm với khoá: B làm (`ghep_cham.py`).

## Kiểm phần sửa `6310645` (10:40 14/11/2026)
- **Code:** đọc diff. `dong_neu_mua` có 3 trường hợp, mỗi ngày mưa luôn đúng một dòng. Điểm thêm buổi sáng chỉ nhận khi kết thúc ≤ giờ đầu buổi chiều. `kiem_khung_v2` có mã `sang_chong_chieu` riêng. Đúng hướng (c) A chốt.
- **E chạy lại:** ca dò `data/len_ke_hoach_v2_2026-11-13/e_ca_do_chong_buoi.py` trên `6310645` ⇒ sáng chồng chiều **52 ⇒ 0** / 3.840 khung · test 2 file **95 đạt**. 104 ngày sáng xong sau 12:30: không chồng, B đã báo A, không phải finding.
- **Hai người chấm mù mới** (agent con ngữ cảnh mới, không mở khoá, không thấy file nhau), chỉ chấm 6 lịch đổi `cham_mu_1411_sua/`: **6 / 6 đạt mọi ý ở cả hai người, 0 chồng giờ** (`cham_sua_nguoi_1.jsonl`, `cham_sua_nguoi_2_rieng.jsonl`). Ghép với 9 lịch không đổi mỗi lượt ⇒ bộ quyết đạt ≥ 11 / 12 theo thước ghi trước (B ghép khoá để ra số cuối).
- **M-1 đóng.** Ý 6: đóng.
- **M-2 (major, mới — hai người chấm cùng tự thấy):** một câu của model lọt lời nội bộ ra lịch: "Câu tài liệu không cung cấp thông tin về <điểm>; nội dung chỉ mô tả <điểm khác trong cùng bài>." (lich_3f419903, mục chiều ngày 4). `kiem_cau` (`lich_trinh_v2.py` ~dòng 537) chỉ bắt: rỗng · thiếu mã · mã lạ · giờ · tiền · link · tên điểm khác. Câu này không chứa tên điểm nào có trong bảng nên lọt qua. Gốc: đoạn kho lấy cho điểm đó là đoạn tả một công trình khác trong cùng bài (điểm này không có `doan_mo_ta`). Tác động: người dùng thấy câu "nói về tài liệu" thay cho câu tả điểm. Gặp 1 / 6 lịch đổi; ở lượt trước, cùng mục đó ra câu dự phòng. **Đóng khi:** `kiem_cau` từ chối câu nói về tài liệu / nguồn (vd "tài liệu", "nguồn không", "đoạn trích", "không cung cấp thông tin") ⇒ câu dự phòng, kèm một test; nên thêm `doan_mo_ta` cho điểm đó nếu bài có đoạn đúng. Không cần đo lại có phí: kiểm bằng `cham_lai` trên kết quả đã lưu.
- **Kết luận:** `changes_requested` chỉ vì M-2. Sửa xong ⇒ E chỉ kiểm M-2 (code + `cham_lai`), không chấm lại.

## Kiểm M-2 `16374fc` (10:44 14/11/2026)
- `kiem_cau` có mã `noi_ve_tai_lieu` (mẫu chữ nói về tài liệu / nguồn) ⇒ câu dự phòng riêng cho mục đó. Có test. E chạy `test_len_ke_hoach_v2.py`: 84 đạt. Hổ Quyền có `doan_mo_ta` mục "Tổng quan" (bảng `d815f4918a55`).
- B thử mẫu trên 1.068 câu model đã lưu: trúng đúng 1 câu lỗi, chặn nhầm 0 câu tốt. Bộ quyết sau ghép: 12 / 12 ×2.
- m-3 (minor, không chặn): mẫu có chữ "văn bản", nên câu tả một điểm trưng bày văn bản cổ sẽ bị chặn nhầm thành câu dự phòng. Hệ quả nhẹ: chỉ ra câu dự phòng, không ra câu sai. Bảng điểm hiện không có điểm nào như vậy. Đóng khi: bỏ "văn bản" khỏi mẫu, hoặc ghi lại giới hạn này.
- **Kết luận cả nhánh: `ready_for_user_confirmation`** — 0 blocker · 0 major mở · m-3. A trình User D4.

## Kiểm giờ Quần thể + m-3 (`ee6dde9`, `diem_v8` `448825605dc9`) (10:52 14/11/2026)
- Dữ liệu: so bảng cũ ↔ mới bằng code ⇒ đúng 12 điểm đổi, chỉ ở 2 trường `gio_mo` (07:00–17:30 ⇒ 07:00–17:00) và `gio_mo_can_cu` (ghi nguồn + ngày). 0 trường khác đổi.
- Code m-3: mẫu chữ chỉ bắt "tài liệu" khi đi kèm "theo / trong" hoặc "không / chưa / chỉ"; không còn bắt "văn bản" đứng một mình. Có test. **m-3 đóng.**
- E chạy lại trên `ee6dde9`: ca dò chồng giờ 0 / 3.840 khung · 95 test đạt.
- **Kết luận nhánh giữ nguyên: `ready_for_user_confirmation`, 0 finding mở.**
