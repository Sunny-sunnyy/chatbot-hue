# Rà "Câu hỏi A còn nợ" (09/11 + "Cũ còn mở") — B · 12:15 15/11/2026 · 0 USD

A giao: kiểm từng mục trên code hiện tại (main `b52dc66` trở về sau) + ca thử 0 USD / đếm log ⇒ đã hết / còn / bỏ; ≤ 3 sửa nhỏ đáng làm.
Đếm log: `backend/logs/application.log` (dòng `chat_metrics`, bỏ model giả `probe`); bộ Golden đã lưu (`data/*/golden.jsonl`). Không có người dùng thật trong log.

## Từng mục

| Mục | Kiểm (file:dòng / ca thử) | Kết luận |
|---|---|---|
| **Luật số mục web "8/11" ≠ "08/11"** | `backend/llm/tra_web.py:201–207` `_chuoi_so` so phần chữ số: "8/11" ⇒ `811`, "08/11" ⇒ `0811`. Ca thử: mục "8/11 [w1]" + đoạn trích "08/11" ⇒ `so_ngoai_trich` (mục bị thay câu cố định) [Chạy] | **CÒN** — chặn nhầm. Log: 9 lượt `so_ngoai_trich` / 30 lượt có `web_kiem` (không biết bao nhiêu do số 0 đầu — log không có chữ) ⇒ **sửa 1** |
| Luật số mục web "1:23" trùng "123" | cùng chỗ; ca thử "Mở 1:23" + trích "123" ⇒ qua [Chạy] | còn, nhưng là **lỏng** (cho qua), cần cùng lúc model viết số lạ trùng dãy chữ số trong trích — hiếm; **bỏ** (ghi giới hạn) |
| **B5b "tuần sau" không có số dự báo** | `thoi_tiet.py:53` `_XA` khớp "tuần sau" ⇒ `ngoai_7_ngay` luôn True (`:86`) ⇒ câu cố định "chỉ có dự báo 7 ngày". Ca thử hôm nay (Chủ nhật 15/11): "Thứ hai tuần sau…" (= ngày mai) ⇒ ngoài 7 ngày [Chạy] | **CÒN** — sai rõ khi hôm nay từ thứ Ba tới Chủ nhật (ít nhất một ngày tuần sau nằm trong 7 ngày dự báo; Chủ nhật: cả tuần sau trừ CN). Log không ghi cờ `ngoai_7` ⇒ chưa đếm được ⇒ **sửa 2** |
| Model gọi `thoi_tiet` 2 lần rồi từ chối | log: 4 lượt có `thoi_tiet`, đều 1 lần gọi, 0 từ chối; B5b sáng 15/11: 15 lượt, 0 rút, gọi 9 / 9 | **hết** (không gặp lại) ⇒ xoá |
| Golden 67 từ chối ngẫu nhiên | 5 lượt đủ gần nhất (ghi kho 2 trước / sau, mốc + 2 biến thể 15/11): 0 / 5 từ chối | **hết** ⇒ xoá khỏi theo dõi |
| Giờ tới / về bị bỏ qua im lặng | lịch câu tự do (`lich_trinh`) tắt; biểu mẫu bản 2 không có ô giờ; sửa lịch bằng lời: `HanhDong` không có loại "giờ" (`sua_lich_v2.py:27`) ⇒ model trả rỗng ⇒ `hieu_va_ap` trả None ⇒ **đi đường trả lời thường** (`len_ke_hoach.py:251–253`), không im lặng | **hết ở dạng cũ** ⇒ xoá (giới hạn còn: lịch không dời theo giờ tới / về) |
| `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần" | chỉ dùng ở lịch câu tự do (cờ tắt, T4 đóng hồ sơ 09/11); biểu mẫu có ô số ngày | **bỏ** ⇒ xoá |
| "Đi dày" ít tác dụng (bảng thiếu thời lượng) | lịch v1; bản 2 có `kieu_di` 3 mức (2 / 3 / 4 điểm / ngày) | **hết** ⇒ xoá |
| E20 Sửa 1 / 2 + C210; `p9-sua-lich` tôn trọng `hoi_toi` + `chon_sang` | thuộc lịch câu tự do / nhánh sửa lịch cũ — đã thay bằng `sua_lich_v2` (bật 14/11) | **bỏ** ⇒ xoá |
| T3: gắn điểm cũ khi đổi chủ đề | T3 đóng hồ sơ 09/11 (tag `hoso/p9-t3-bang`), không vào `main` | **bỏ** ⇒ xoá |
| T1: "tháng tới / cuối tuần" do model tự tính | giới hạn đã ghi; "cuối tuần này" không bị coi ngoài 7 ngày [Chạy] | giới hạn, không phải nợ ⇒ xoá (giữ ở sổ 07) |
| G: S1 chạy lại an toàn có ngữ cảnh | harness đã sửa (`do_g.py`) — ghi chú lịch sử | ⇒ xoá |
| USD lần gọi bị Dừng là cận dưới | giới hạn đo, không lỗi | ⇒ xoá (giữ ở sổ 07) |
| Chữ đầu mục web p50 ~13 s | đếm lại 15/11: p50 **6,78 s** (n = 5 stream) — `b_dem_toc_do.md` | số cũ ⇒ thay bằng số mới; tốc độ đã gác (2 bậc âm) |
| `_token_count` chênh ~900 token | không gặp lỗi ngân sách ngữ cảnh ở lượt gọi model thật (lỗi `context_budget_error` trong log đều từ test) | **bỏ** ⇒ xoá |
| Ghi đệm OpenAI giữ như cũ | đã quyết (C202 âm 05/11) | ⇒ xoá |
| **Bảng sổ S41–S44 thiếu 1 cột** | `SO_CAI_TIEN_CACH_LAM.md:135–138`: 8 ô ↔ 9 ô ở các dòng khác | **CÒN** — sửa chữ governance (A) ⇒ **sửa 3** |
| B7: dự phòng demo mất mạng + đề cương + ý #15–#17 | việc tương lai, không phải nợ | giữ ở mục B7 |

## ≤ 3 sửa nhỏ đề xuất (gửi cả nhóm bàn)

1. **Mục web: bỏ số 0 đầu mỗi nhóm chữ số khi so** (`_chuoi_so`: "08/11" ⇒ "8 11" ⇔ "8/11"). Lợi: hết chặn nhầm ngày / giờ viết khác số 0 ("08:00" ↔ "8:00") — mục web đúng không bị thay câu cố định.
   Tốn: ~3 dòng + test, 0 USD; đo: chạy lại luật trên các mục web đã lưu (như lần 21 ⇒ 10) để đếm số mục cứu thêm. Sai khi: số điện thoại có 0 đầu bị coi bằng số không có 0 — hai bên cùng chuẩn hoá nên chỉ lỏng hơn chút.
2. **Thời tiết "tuần sau": chỉ coi là ngoài 7 ngày khi không ngày nào của tuần sau nằm trong 7 ngày dự báo** (tức chỉ khi hôm nay là thứ Hai); còn lại đưa công cụ và code nối
   một dòng "dự báo chỉ tới <ngày>". Lợi: câu "tuần sau / thứ X tuần sau" — loại khách hay hỏi — có số thật thay vì câu từ chối. Tốn: code nhỏ + test, đổi chuỗi gửi model với câu có
   "tuần sau" ⇒ đo B5b (X01 / X02 + 2–3 câu mới) ×1 + an toàn 32 ≈ 0,02 USD. Sai khi: model nói cả tuần dù chỉ có vài ngày — dòng "chỉ tới <ngày>" + kiểm số Q2 sẵn có chặn.
3. **Sửa 4 dòng S41–S44 thiếu cột** (A, 1 phút, governance).

Mọi mục còn lại: xoá khỏi "Câu hỏi A còn nợ" (bảng trên ghi lý do).
