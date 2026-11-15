# Báo cáo cho bạn: Hỏi bằng ảnh (Phase 10)

**Cập nhật lần cuối: 21:36 15/11/2026 — bản 5: luồng người dùng thấy đổi tối 15/11 (nút dấu cộng trong ô nhập + dán ảnh; ảnh đính kèm câu hỏi, bấm Hỏi mới xử lý; ra một tên thì trả lời luôn, 2–3 tên thì hỏi chọn). Bản 4 (19:28 10/11/2026): sửa các chỗ còn ghi "cờ tắt / chờ bật". Các bản trước: xem lịch sử git.**
Người viết: E · Review: A. Bản 10/11: agent con của A, chưa review. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (luôn đúng hiện trạng)

- **Làm gì:** người dùng đính kèm một ảnh (món ăn, công trình, cảnh ở Huế) vào câu hỏi rồi bấm Hỏi ⇒ hệ thống đoán **1–3 tên** trong danh sách 42 tên lấy từ kho (bạn đã duyệt) ⇒ **ra đúng một tên: trả lời luôn** (câu ghép "<câu đã gõ> (Trong ảnh: <tên>)", ô rỗng ⇒ "Giới thiệu về <tên>"), đầu câu trả lời có dòng "Mình đoán trong ảnh là <tên> — có thể sai"; **ra 2–3 tên: người dùng bấm tên đúng** rồi mới trả lời; không nhận ra ⇒ lời báo, gõ tên. Câu trả lời luôn từ kho, có nguồn — model trả lời **không nhìn ảnh**, chỉ nhận cái tên.
- **Đang chạy thế nào:** **đang bật** từ 08/11 (`anh.bat: true`). Từ tối 15/11: **nút dấu cộng trong ô nhập** (thay nút chữ "Hỏi bằng ảnh") hoặc **dán ảnh** vào ô ⇒ ảnh nhỏ nằm trong ô như tệp đính kèm, **chưa gửi gì đi**; bấm Hỏi mới gửi ảnh tới OpenAI (`gpt-6-luna`) để đoán tên. Tải lại trang hoặc "Cuộc trò chuyện mới" ⇒ ảnh đính kèm bị gỡ. Bong bóng câu hỏi hiện ảnh nhỏ + đúng chữ người dùng gõ.
- **Chất lượng (bộ 33 ảnh đã thấy):** đoán đúng tên trong 3 gợi ý ở **22 / 25** ảnh Huế (đạt ngưỡng 22), nhưng có lượt gán nhầm tên Huế cho **2 / 5** ảnh không phải Huế (ngưỡng ≤ 1) ⇒ **âm theo thước gốc**. Bạn chọn (11:42 05/11) **giữ dạng gợi ý có xác nhận**: nhãn "có thể sai", luôn có nút "Không phải các tên này — tôi gõ tên"; lỗi đoán nhầm không thành câu trả lời sai vì người dùng phải bấm tên.
- **Vì sao đổi sang "lai" (15/11, bạn chọn sau khi thử + xem số):** đếm lại kết quả đã lưu của bộ 33 ảnh × 2 lượt (66 lượt, không gọi model): lượt nào cũng trả lời luôn theo tên đầu ⇒ **14 / 66** lượt trả lời về sai nơi; model đưa **một tên** thì tên đó đúng **31 / 33** lượt (ảnh trong danh sách), đưa 2–3 tên thì tên đầu chỉ đúng 11 / 17 ⇒ cách lai còn **6 / 66** lượt sai nơi, **19 / 66 (29 %)** lượt vẫn phải bấm chọn. Đổi có chủ ý so với quyết định 05/11 (luôn xác nhận): chấp nhận một ít câu sai nơi có dòng cảnh báo. Mẫu nhỏ, ảnh công khai — chưa có số trên ảnh người dùng tự chụp. Nguồn: `data/dem_ten_so_1_2026-11-15/KET_QUA.md` (riêng tư).
- **Thử thay bằng model chạy trên máy (SigLIP 2, miễn phí):** 3 cách đều **âm** — cách tốt nhất đoán đúng 20 / 25 nhưng **không biết nói "không nhận ra"** (ảnh con mèo cũng được gợi tên Huế). Không đưa vào chatbot.
- **Tiền / tốc độ:** ≈ **0,0004 USD / ảnh** (≈ 10 đồng) cộng câu trả lời sau khi bấm (≈ 0,0005 USD). Đoán tên mất trung vị ≈ 3 s (bộ 33 ảnh, 05/11; thử 5 ảnh lúc bật 08/11: 3,5 s), chậm nhất (p95) 6,3–9,1 s — **chưa đạt** mục tiêu ≤ 5 s. Tổng tiền Phase 10 tới nay **0,0984 USD** (≈ 2.500 đồng) / trần 0,15.
- **Bạn cần quyết:** xem §6.

## 2. Hoạt động thế nào (bản trong `main`, khi cờ bật)

```text
Người dùng bấm dấu cộng trong ô nhập hoặc dán ảnh (trình duyệt: chỉ JPEG / PNG / WEBP, ≤ 10 MB; ảnh nhỏ nằm trong ô, CHƯA gửi gì) ⇒ gõ câu ⇒ bấm Hỏi
  ⇒ POST /api/anh/ung_vien  (backend/api/routes/anh.py)
     rào trước khi đọc ảnh: yêu cầu phải từ chính trang chatbot, đúng kiểu ảnh, ≤ 10 MB  — sai ⇒ từ chối, không gọi model
  ⇒ xử lý ảnh trên máy (backend/llm/nhan_anh.py chuan_bi_anh): chặn ảnh "bom" quá 40 triệu điểm ảnh, xoay đúng chiều,
     XOÁ thông tin kèm ảnh (vị trí GPS, máy chụp), thu nhỏ cạnh dài 1024, không lưu ảnh xuống đĩa
  ⇒ một lần gọi gpt-6-luna: ảnh + danh sách 42 tên; model CHỈ được trả ≤ 3 mã tên trong danh sách hoặc "không nhận ra"
     (chữ viết trong ảnh là dữ liệu, không phải lệnh)
  ⇒ code kiểm lại: mã phải có trong danh sách ⇒ trả tên chuẩn
  ⇒ giao diện (frontend/src/HoiBangAnh.jsx), từ tối 15/11:
       1 tên   ⇒ code ghép câu "<chữ bạn đã gõ> (Trong ảnh: <tên>)" (ô rỗng: "Giới thiệu về <tên>") và HỎI LUÔN ⇒ chatbot trả lời như câu gõ;
                 đầu câu trả lời: "Mình đoán trong ảnh là <tên> — có thể sai." + thẻ gọn trên ô nhập có nút "Không đúng — tôi gõ tên"
       2–3 tên ⇒ "Trong ảnh là (có thể sai) — chọn đúng tên:" + nút tên + "Không phải các tên này — tôi gõ tên" ⇒ bấm tên ⇒ ghép câu như trên
       0 tên / lỗi ⇒ lời báo "chưa nhận ra", gỡ ảnh, giữ chữ đã gõ
Log: một dòng `anh_metrics` / ảnh — chỉ số đếm, mã kết quả, ms, USD; không ghi ảnh, tên file hay tên đoán ra.
```

Danh sách 42 tên (28 điểm · 9 món · 5 di sản) do code dựng từ kho, bạn duyệt các lần gộp tên (05/11).

## 3. Checklist tình huống

| Tình huống | Trạng thái | Ghi chú |
|---|---|---|
| Ảnh công trình / cảnh / món Huế có trong danh sách | **Đã xử lý** (bật 08/11) | đúng trong 3 gợi ý 22 / 25 (cả hai lượt đo); nhầm hay gặp: các lăng / điện giống nhau, vài món ít ảnh |
| Ảnh không phải Huế (Bắc Kinh, Hà Nội, mèo, nội thất) | **Xử lý một phần** | 0–2 / 5 bị gán tên Huế tuỳ lượt. Từ 15/11: bị gán MỘT tên ⇒ trợ lý trả lời luôn về nơi đó kèm dòng "có thể sai" (2 lượt trong bộ đếm); bị gán 2–3 tên ⇒ người dùng phải chọn / gõ tên |
| Ảnh có chữ "ra lệnh" dán thêm (đòi trả tên khác) | **Xử lý một phần** | 1 / 3 ảnh bị lừa ở mọi lượt (bảng chữ in kiểu biển chính thức) — trong ngưỡng ≤ 1. Từ 15/11 luồng trả lời luôn làm ca này nặng hơn: chữ trên ảnh có thể quyết định câu trả lời nói về nơi nào (2 lượt trong bộ đếm) |
| Ảnh có biển tên thật (chợ, trường) | **Đã xử lý** (bật 08/11) | 2 / 2 |
| File không phải ảnh / quá 10 MB / ảnh "bom" | **Đã xử lý, đã kiểm** | trình duyệt báo lỗi trước khi gửi; server từ chối trước khi đọc ảnh, không gọi model (7 ca thử trên server thật) |
| Trang web lạ gửi ảnh thay người dùng | **Đã xử lý, đã kiểm** | từ chối 403; khi deploy cần thêm (xem §6) |
| Thông tin vị trí trong ảnh | **Đã xử lý, đã kiểm** | xoá trước khi gửi OpenAI (test) |
| Giao diện trên trình duyệt (máy tính) | **Đã xử lý, đã kiểm** | thử thật bằng Playwright 05/11 tối: đủ các bước, 0 vi phạm chính sách bảo mật trang |
| Giao diện trên điện thoại | **Đã xử lý** (sửa đã vào `main` 08/11, merge `3da1cb1`) | thử thật 360×740 và 390×844: không tràn ngang, đủ các bước; bản cũ thẻ ảnh che gần hết câu trả lời (còn 191 px để đọc ở 360×740) ⇒ sửa: ảnh xem trước nhỏ đặt cạnh chữ ⇒ còn 322 px (§4); chưa thử trên máy điện thoại thật / Safari |
| Đoán tên bằng model chạy trên máy (SigLIP 2) | **Đã thử, chưa áp dụng** | âm (§4) |
| Giới hạn số ảnh / người, nhiều ảnh cùng lúc | **Chưa thực hiện** | để Phase 12 (deploy) |
| Model đưa MỘT tên nhưng sai (15/11) | **Xử lý một phần** | trợ lý trả lời luôn về sai nơi; lưới còn lại là dòng "Mình đoán… có thể sai" đầu câu trả lời + nút gõ tên. Đã gặp thật khi thử: ảnh nhỏ một cổng trong Hoàng thành ⇒ một tên lăng (2 lượt) |
| Cùng một ảnh, kết quả khác nhau giữa các lượt (15/11) | **Chưa xử lý** | một ảnh thử qua 7 lượt: 1 tên đúng 1 · 1 tên sai 2 · 2 tên 2 · lỗi model 2 ⇒ ảnh khó thì "một tên" không ổn định |
| Bước đoán tên báo lỗi model (15/11) | **Giới hạn đã nhận** | phần suy luận chạm trần 1.024 token đầu ra ⇒ hiện "chưa nhận ra"; A đếm trong log 2 / 149 lượt (E chưa tính lại) — quan sát nguyên nhân, chưa chứng minh |
| Đang "Đang xem ảnh…" mà người dùng làm việc khác (15/11) | **Đã xử lý, đã kiểm** | bỏ / thay ảnh, mở cuộc mới ⇒ kết quả cũ bị bỏ; có lượt khác đang chạy ⇒ không tự hỏi chen ngang, hiện thẻ chọn (ca dò của reviewer). Chưa có nút huỷ lúc đang xem ảnh |
| Dán ảnh vào ô nhập (15/11) | **Đã xử lý, đã kiểm** | dán ảnh thật qua clipboard 3 / 3 đúng luồng; clipboard có cả chữ lẫn ảnh ⇒ dán chữ; ảnh GIF ⇒ lời báo, không gọi model |

## 4. Thử nghiệm và lịch sử (mới ở trên)

### 15/11/2026 tối — đổi luồng người dùng thấy (bốn bước trong một tối, theo góp ý của bạn khi thử)
1. Nút chữ "Hỏi bằng ảnh" ⇒ **nút dấu cộng trong ô nhập** + dán ảnh (`report_agent/2026-11-12_ra_khoang_cach/c_nut_anh_cong_implementation.md`, review `e_review_nut_anh_cong.md`).
2. Ảnh thành **tệp đính kèm** của câu hỏi: chọn / dán ảnh 0 lần gọi máy chủ, bấm Hỏi mới nhận diện (`c_anh_dinh_kem_implementation.md`).
3. Bạn thử và coi bước bắt bấm tên là lỗi ⇒ **phương án lai**: một tên trả lời luôn, 2–3 tên hỏi chọn; dòng "Mình đoán… có thể sai" đầu câu trả lời (`e_anh_tra_loi_thang_implementation.md`; kiểm bằng Playwright: số tên dựng bằng chặn route ảnh trong trình duyệt, câu hỏi đi máy chủ thật; ≈ 0,012 USD).
4. Review bắt một lỗi thật trước khi vào `main`: kết quả nhận ảnh về trễ tự gửi câu vào cuộc mới / huỷ lượt đang chạy ⇒ đã sửa.

**Đang mở (chưa quyết, chưa đưa vào chatbot):** thử lại cách **so ảnh với ảnh mẫu bằng vector** (plan nháp trên nhánh `p10-so-anh`); phép dò đầu với DINOv2 trên bộ mẫu cũ: tên đầu đúng 17 / 25 (SigLIP 2: 15; model đang chạy: 21) — số A chuyển, chưa review. Bước đếm ảnh mẫu: 42 tên có 221 ảnh, thiếu khoảng 272 so với mốc của plan; bộ mẫu cũ có ảnh gắn sai tên (`data/so_anh_buoc0_2026-11-15/KET_QUA.md`, riêng tư).

### 05/11/2026 tối — thử giao diện ở khung điện thoại (Playwright, server thật)
Hai khung màn điện thoại phổ biến 390×844 và 360×740, cờ bật tạm. Đo "vùng đọc" = phần màn hình phía trên khung gõ dính đáy (chỗ còn thấy câu trả lời).

| Lúc | Bản trong `main` | Sau sửa | |
|---|---|---|---|
| Chưa chọn ảnh | 606 / 844 · 502 / 740 px | như cũ | nút + dòng báo OpenAI chiếm ~238 px |
| Đang hiện gợi ý tên (390×844) | 227 px | **398 px** | |
| Thẻ ảnh mở trên câu trả lời (390×844 · 360×740) | 295 · **191 px** (~3 dòng) | 426 · **322 px** | ca dễ che nhất |
| Tràn ngang · vi phạm chính sách bảo mật trang · kết nối ra ngoài | 0 · 0 · 0 | 0 · 0 · 0 | |

Sửa: chỉ ở màn ≤ 700 px, ảnh xem trước thu còn 72 × 72 px và đặt **bên trái** chữ; nút "Không phải các tên này" trải cả dòng. Màn máy tính không đổi. Chỉ đổi CSS (`frontend/src/index.css`, 8 dòng). Ảnh chụp trước / sau: `data/phase_10/anh/e11/`. **PASS** · 0,0025 USD (2 lượt đầy đủ + 2 ảnh ngoài danh sách).
Còn lại: nút "Hỏi bằng ảnh" + dòng báo vẫn chiếm ~238 px kể cả khi chưa dùng — không sửa (dòng báo gửi ảnh cho OpenAI là bắt buộc theo spec); chưa thử trên máy điện thoại thật / Safari.

### 05/11/2026 tối — thử SigLIP 2 chạy trên máy (thay hoặc ghép với luna)
Tiêu chí ghi trước (giống lần đo luna): đúng trong 3 gợi ý ≥ 22 / 25 **và** gán nhầm ảnh không phải Huế ≤ 1 / 5, đạt cả hai lượt.
Model `google/siglip2-base-patch16-224` (1,5 GB, chạy CPU, ~0,3 s / ảnh, RAM ~1,6 GB, ảnh không rời máy). 172 ảnh mẫu Commons cho 40 tên (đã kiểm: 0 ảnh trùng bộ đo).

| Cách | Đúng / 25 | Ảnh ngoài bị gán tên / 5 | Tiền | Kết quả |
|---|---|---|---|---|
| So ảnh với câu chữ mô tả tên | 5 | 5 | 0 | FAIL — model không hiểu tên riêng Huế bằng chữ |
| So ảnh với ảnh mẫu (tìm ảnh giống nhất) | 20 | 5 | 0 | FAIL — điểm giống của ảnh ngoài Huế chồng lên ảnh Huế ⇒ không có ngưỡng nào tách được |
| Ảnh mẫu lọc 5 tên ⇒ luna chọn | 21 · 19 | 1 · 3 | 0,0157 USD | FAIL — 5 tên lọc trước chỉ chứa tên đúng ở 22 / 25 ảnh, luna đổi ý giữa hai lượt ở 12 / 33 ảnh |

Không chỉnh thêm vì số đo cho thấy chỉnh ngưỡng / lời dặn không qua được ngưỡng. **Bỏ**, giữ luna. Collection thử `hue_anh_siglip2` (172 điểm) đã xoá (kiểm Qdrant 14/11).

### 05/11/2026 tối — thử giao diện trên trình duyệt (Playwright, server thật)
Tắt ⇒ không có nút. Bật tạm ⇒ file sai kiểu / quá lớn bị chặn trước khi gửi; ảnh chùa ⇒ gợi ý đúng tên ⇒ bấm ⇒ câu trả lời 7 nguồn; ảnh con mèo ⇒ "Mình chưa nhận ra ảnh này" ⇒ "Gõ tên" ⇒ con trỏ về ô gõ, không hỏi chatbot. 0 vi phạm chính sách bảo mật trang, 0 kết nối ra ngoài. **PASS** · 0,0016 USD.

### 05/11/2026 trưa — đo luna đoán tên (33 ảnh đã thấy, 2 lượt mỗi vòng, 3 vòng)
| Vòng | Đổi | Đúng / 25 | Ảnh ngoài bị gán / 5 | Kết quả |
|---|---|---|---|---|
| v0 | lời dặn ban đầu | 21 · 21 | 0 · 0 | FAIL (thiếu 1; có lỗi model bị cắt chữ) |
| **v1** (đang dùng) | nới giới hạn chữ ra, cho gợi thêm tên dễ nhầm | **22 · 22** | 0 · **2** | FAIL ở lượt 2 |
| v2 | siết: chỉ gợi khi có dấu hiệu riêng | 21 · 20 | 0 · 0 | FAIL |

Chỉnh lời dặn chỉ dời lỗi giữa "đoán đúng" và "không ép tên"; hai lượt cùng cấu hình khác nhau ở 4–7 / 33 ảnh. Bạn chọn giữ **v1 dạng gợi ý có xác nhận** (đổi thước vì có bước bấm) · 0,0782 USD.

### 05/11/2026 sáng — xây đường ảnh (cờ tắt)
Rào, xử lý ảnh, một lần gọi model, test; thử một ảnh thật: đúng món, 0,0004 USD. Khi tắt và khi bật, chatbot hỏi đáp gửi model **đúng từng byte như trước** (228 / 228 lượt so).

## 5. Hôm nay còn đúng không

| Kết quả / quyết định | Trạng thái | Căn cứ |
|---|---|---|
| Code ảnh trong `main`, **bật** từ 08/11 | còn dùng | merge `2ca9937` (code), `3da1cb1` (giao diện), cờ `cf57309`; `backend/config/settings.yaml:82` `anh.bat: true` |
| Luna v1 dạng gợi ý có xác nhận | còn dùng (người dùng thấy từ 08/11) | quyết định bạn 11:42 05/11 |
| SigLIP 2 thay / ghép luna | đã bỏ | `report_agent/2026-11-05_phase_10_anh/e9_siglip_implementation.md` |

## 6. Việc còn lại / cần quyết

1. ~~Bật "Hỏi bằng ảnh" cho người dùng chưa?~~ **Bạn đã chọn bật 08/11.** Còn lại: đoán tên chậm nhất 6–9 s, vượt mục tiêu 5 s (chưa có việc sửa).
2. **Cách miễn phí trên máy (SigLIP so ảnh mẫu)** — nếu bạn ưu tiên "ảnh không rời máy, nhanh 0,3 s": đúng 20 / 25 (luna 22) nhưng **luôn gợi tên, kể cả ảnh không phải Huế**. Không tự áp; mặc định giữ luna.
3. ~~Xoá collection thử `hue_anh_siglip2`?~~ **Đã xoá** (kiểm Qdrant 14/11).
4. Trước khi deploy (Phase 12): danh sách địa chỉ trang hợp lệ cố định, xử lý HTTPS sau proxy, giới hạn số ảnh xử lý cùng lúc.
5. Giọng nói (cũng thuộc Phase 10): nghiên cứu đang tạm dừng theo bạn.
6. (15/11) Sau khi đổi sang "một tên thì trả lời luôn": theo dõi khi bạn thử bằng ảnh thật — lượt nào câu trả lời nói về sai nơi; lời dặn của bước đoán tên vẫn là bản viết cho luồng có xác nhận ("người dùng sẽ tự bấm chọn") — chưa đổi; chưa có nút huỷ lúc "Đang xem ảnh…"; trần 1.024 token đầu ra của bước đoán tên (xem checklist).
7. (15/11) Thí nghiệm so ảnh bằng vector: chờ plan được duyệt + quyền tải model (mục "Đang mở" ở §4).

## Phụ lục — hồ sơ kỹ thuật

- Spec Phase 10 bản 2 `bf67b90fb6fc` (bạn duyệt 10:28 05/11) · plan A1 bản 2 `2fc2fcea33d4`.
- Report: `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` (A1, A2, Playwright) · `e8_review.md` (C198, ready 0/0/3) · `e9_siglip_implementation.md` (E9).
- Commit: `0632e10` (code) · `973823f` (test rào thư viện mạng, C198 m-1) · merge `2ca9937` · `13c6a7a` (nhánh `p10-anh-mobile`, CSS màn hẹp — đã vào `main`) · merge `3da1cb1` (giao diện cổng) · cờ `cf57309` (bật 08/11).
- Mã đo: Q-a đúng trong 3 gợi ý · Q-b đúng ở gợi ý đầu · Q-c ảnh ngoài bị ép tên · Q-d ảnh chữ ra lệnh bị lừa · Q-e số ảnh đổi kết quả giữa hai lượt.
- Dữ liệu (private): `data/phase_10/anh/` (danh sách tên, A2, Playwright, E9), bộ ảnh đo `data/phase_10/bo_do_anh/`.
