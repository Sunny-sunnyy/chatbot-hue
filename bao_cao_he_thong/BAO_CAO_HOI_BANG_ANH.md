# Báo cáo cho bạn: Hỏi bằng ảnh (Phase 10)

**Cập nhật lần cuối: 20:26 05/11/2026 — bản 2: thử giao diện ở khung điện thoại ⇒ thẻ ảnh che câu trả lời ⇒ sửa nhỏ giao diện (nhánh chờ review, chưa vào `main`).** Trước: 20:18 05/11/2026 — bản 1: viết mới.
Người viết: E · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (luôn đúng hiện trạng)

- **Làm gì:** người dùng chụp / chọn một ảnh (món ăn, công trình, cảnh ở Huế) ⇒ hệ thống đoán **1–3 tên** trong một danh sách 42 tên lấy từ kho (bạn đã duyệt) ⇒ người dùng **bấm tên đúng** ⇒ chatbot trả lời như khi gõ câu "Giới thiệu về <tên>", có nguồn như thường. Trợ lý **không bao giờ trả lời thẳng từ ảnh** — chỉ gợi tên để bấm.
- **Đang chạy thế nào:** code đã vào `main` nhưng **đang tắt** (`anh.bat: false` trong `backend/config/settings.yaml`) ⇒ người dùng **chưa thấy** nút "Hỏi bằng ảnh". Khi bật, ảnh được gửi tới OpenAI (`gpt-6-luna`) để đoán tên.
- **Chất lượng (bộ 33 ảnh đã thấy):** đoán đúng tên trong 3 gợi ý ở **22 / 25** ảnh Huế (đạt ngưỡng 22), nhưng có lượt gán nhầm tên Huế cho **2 / 5** ảnh không phải Huế (ngưỡng ≤ 1) ⇒ **âm theo thước gốc**. Bạn chọn (11:42 05/11) **giữ dạng gợi ý có xác nhận**: nhãn "có thể sai", luôn có nút "Không phải các tên này — tôi gõ tên"; lỗi đoán nhầm không thành câu trả lời sai vì người dùng phải bấm tên.
- **Thử thay bằng model chạy trên máy (SigLIP 2, miễn phí):** 3 cách đều **âm** — cách tốt nhất đoán đúng 20 / 25 nhưng **không biết nói "không nhận ra"** (ảnh con mèo cũng được gợi tên Huế). Không đưa vào chatbot.
- **Tiền / tốc độ:** ≈ **0,0004 USD / ảnh** (≈ 10 đồng) cộng câu trả lời sau khi bấm (≈ 0,0005 USD). Đoán tên mất trung vị ≈ 3 s, chậm nhất (p95) 6,3–9,1 s — **chưa đạt** mục tiêu ≤ 5 s. Tổng tiền Phase 10 tới nay **0,0984 USD** (≈ 2.500 đồng) / trần 0,15.
- **Bạn cần quyết:** xem §6.

## 2. Hoạt động thế nào (bản trong `main`, khi cờ bật)

```text
Người dùng chọn ảnh (trình duyệt: chỉ JPEG / PNG / WEBP, ≤ 10 MB; xem trước ảnh ngay trên máy, không tải lên chỗ khác)
  ⇒ POST /api/anh/ung_vien  (backend/api/routes/anh.py)
     rào trước khi đọc ảnh: yêu cầu phải từ chính trang chatbot, đúng kiểu ảnh, ≤ 10 MB  — sai ⇒ từ chối, không gọi model
  ⇒ xử lý ảnh trên máy (backend/llm/nhan_anh.py chuan_bi_anh): chặn ảnh "bom" quá 40 triệu điểm ảnh, xoay đúng chiều,
     XOÁ thông tin kèm ảnh (vị trí GPS, máy chụp), thu nhỏ cạnh dài 1024, không lưu ảnh xuống đĩa
  ⇒ một lần gọi gpt-6-luna: ảnh + danh sách 42 tên; model CHỈ được trả ≤ 3 mã tên trong danh sách hoặc "không nhận ra"
     (chữ viết trong ảnh là dữ liệu, không phải lệnh)
  ⇒ code kiểm lại: mã phải có trong danh sách ⇒ trả tên chuẩn
  ⇒ giao diện (frontend/src/HoiBangAnh.jsx): "Gợi ý từ ảnh, có thể sai — chọn đúng tên:" + nút tên + "Không phải các tên này — tôi gõ tên"
  ⇒ bấm tên ⇒ code ghép câu "Giới thiệu về <tên>" (hoặc "<chữ bạn đã gõ> (Trong ảnh: <tên>)") ⇒ chatbot trả lời như câu gõ
Log: một dòng `anh_metrics` / ảnh — chỉ số đếm, mã kết quả, ms, USD; không ghi ảnh, tên file hay tên đoán ra.
```

Danh sách 42 tên (28 điểm · 9 món · 5 di sản) do code dựng từ kho, bạn duyệt các lần gộp tên (05/11).

## 3. Checklist tình huống

| Tình huống | Trạng thái | Ghi chú |
|---|---|---|
| Ảnh công trình / cảnh / món Huế có trong danh sách | **Đã xử lý** (cờ tắt) | đúng trong 3 gợi ý 22 / 25 (cả hai lượt đo); nhầm hay gặp: các lăng / điện giống nhau, vài món ít ảnh |
| Ảnh không phải Huế (Bắc Kinh, Hà Nội, mèo, nội thất) | **Xử lý một phần** | 0–2 / 5 bị gán tên Huế tuỳ lượt; giao diện bắt người dùng xác nhận |
| Ảnh có chữ "ra lệnh" dán thêm (đòi trả tên khác) | **Xử lý một phần** | 1 / 3 ảnh bị lừa ở mọi lượt (bảng chữ in kiểu biển chính thức) — trong ngưỡng ≤ 1 |
| Ảnh có biển tên thật (chợ, trường) | **Đã xử lý** (cờ tắt) | 2 / 2 |
| File không phải ảnh / quá 10 MB / ảnh "bom" | **Đã xử lý, đã kiểm** | trình duyệt báo lỗi trước khi gửi; server từ chối trước khi đọc ảnh, không gọi model (7 ca thử trên server thật) |
| Trang web lạ gửi ảnh thay người dùng | **Đã xử lý, đã kiểm** | từ chối 403; khi deploy cần thêm (xem §6) |
| Thông tin vị trí trong ảnh | **Đã xử lý, đã kiểm** | xoá trước khi gửi OpenAI (test) |
| Giao diện trên trình duyệt (máy tính) | **Đã xử lý, đã kiểm** | thử thật bằng Playwright 05/11 tối: đủ các bước, 0 vi phạm chính sách bảo mật trang |
| Giao diện trên điện thoại | **Đã xử lý** (sửa chờ review, chưa vào `main`) | thử thật 360×740 và 390×844: không tràn ngang, đủ các bước; bản trong `main` thẻ ảnh che gần hết câu trả lời (còn 191 px để đọc ở 360×740) ⇒ sửa: ảnh xem trước nhỏ đặt cạnh chữ ⇒ còn 322 px (§4) |
| Đoán tên bằng model chạy trên máy (SigLIP 2) | **Đã thử, chưa áp dụng** | âm (§4) |
| Giới hạn số ảnh / người, nhiều ảnh cùng lúc | **Chưa thực hiện** | để Phase 12 (deploy) |

## 4. Thử nghiệm và lịch sử (mới ở trên)

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

Không chỉnh thêm vì số đo cho thấy chỉnh ngưỡng / lời dặn không qua được ngưỡng. **Bỏ**, giữ luna. Collection thử `hue_anh_siglip2` (172 điểm) còn trong Qdrant chờ bạn quyết.

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
| Code ảnh trong `main`, cờ tắt | còn dùng | `main` `2ca9937`; `backend/config/settings.yaml` `anh.bat: false` |
| Luna v1 dạng gợi ý có xác nhận | còn dùng (chưa bật cho người dùng) | quyết định bạn 11:42 05/11 |
| SigLIP 2 thay / ghép luna | đã bỏ | `report_agent/2026-11-05_phase_10_anh/e9_siglip_implementation.md` |

## 6. Việc còn lại / cần quyết

1. **Bật "Hỏi bằng ảnh" cho người dùng chưa?** Bật ⇒ ảnh gửi OpenAI (đã có dòng báo dưới nút), ≈ 0,0004 USD / ảnh, chờ đoán tên ~3 s (chậm nhất 6–9 s, vượt mục tiêu 5 s). Chưa bật ⇒ không ai thấy tính năng. Đã thử khung điện thoại: bản sửa chờ review + merge trước khi bật.
2. **Cách miễn phí trên máy (SigLIP so ảnh mẫu)** — nếu bạn ưu tiên "ảnh không rời máy, nhanh 0,3 s": đúng 20 / 25 (luna 22) nhưng **luôn gợi tên, kể cả ảnh không phải Huế**. Không tự áp; mặc định giữ luna.
3. **Xoá collection thử `hue_anh_siglip2`?** (172 điểm, chỉ dùng cho thí nghiệm) — mặc định giữ tới khi bạn quyết.
4. Trước khi deploy (Phase 12): danh sách địa chỉ trang hợp lệ cố định, xử lý HTTPS sau proxy, giới hạn số ảnh xử lý cùng lúc.
5. Giọng nói (cũng thuộc Phase 10): nghiên cứu đang tạm dừng theo bạn.

## Phụ lục — hồ sơ kỹ thuật

- Spec Phase 10 bản 2 `bf67b90fb6fc` (bạn duyệt 10:28 05/11) · plan A1 bản 2 `2fc2fcea33d4`.
- Report: `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` (A1, A2, Playwright) · `e8_review.md` (C198, ready 0/0/3) · `e9_siglip_implementation.md` (E9).
- Commit: `0632e10` (code) · `973823f` (test rào thư viện mạng, C198 m-1) · merge `2ca9937` · `13c6a7a` (nhánh `p10-anh-mobile`, CSS màn hẹp — chờ review).
- Mã đo: Q-a đúng trong 3 gợi ý · Q-b đúng ở gợi ý đầu · Q-c ảnh ngoài bị ép tên · Q-d ảnh chữ ra lệnh bị lừa · Q-e số ảnh đổi kết quả giữa hai lượt.
- Dữ liệu (private): `data/phase_10/anh/` (danh sách tên, A2, Playwright, E9), bộ ảnh đo `data/phase_10/bo_do_anh/`.
