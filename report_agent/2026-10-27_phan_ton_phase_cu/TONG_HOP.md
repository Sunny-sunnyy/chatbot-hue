# TONG_HOP — đợt "phần tồn Phase cũ" (mở 27/10/2026 chiều)

Người viết: A (`hue-rag-51`). B = `hue-rag-2d`, C = `hue-rag-86` (cả ba Claude Opus 5.5). Trạng thái: **đang mở** — phần chuẩn bị xong trong phiên
27/10 chiều; phần áp (sửa kho + build lại index) chạy sau khi đóng 8.2.

## 1. Mục tiêu

User 14:15 27/10: "xong phần tồn càng sớm càng tốt, xong phần tồn mới yên tâm đi tiếp các phase tiếp theo". Phần tồn = việc các Phase cũ còn để lại:
nợ nhỏ code / tài liệu, nhãn đoạn đúng chưa quyết, lỗi kho đã biết (rà kho C32: 139 mục + file danh mục nằm sai trong index), index Qwen3-8B hoãn từ 7A2.
Chặn chung: B0 (chỉ User làm) ⇒ merge B1 ⇒ B3 ⇒ đóng 8.2 — sửa kho phải sau B3 để mốc cuối 8.2 không lẫn hai thay đổi.

## 2. Quyết định theo giờ

| Giờ | Ai | Quyết định |
|---|---|---|
| 13:46 | User | Quyền phiên như 27/10 sáng; B0 chưa rảnh |
| 13:4x | User | PA3: chuẩn bị B1 + dọn nợ + A **bàn** tính năng mới trước khi đóng 8.2 (lệch WORKFLOW §9.4, User duyệt) |
| 13:5x | User | Ưu tiên tính năng: hội thoại nhiều lượt + streaming; gợi ý / lịch trình ⇒ Phase 9; deploy khi ổn định; bảo vệ ~tháng 1/2027 |
| 14:04 | User → A | "Làm gì cũng được" ⇒ A chọn streaming trước (sau đóng 8.2) |
| 14:15 | User | Làm xong phần tồn sớm nhất |
| 14:2x | A | Plan B3 M-1: một luật cho câu 500 (câu hỏng ở cả hai bên); M-2: người chạy (không phải A) khớp 3 câu A phiên trước đã thấy |
| 14:3x | A | Sự cố s7 (sub-agent đọc nhầm Golden Foods cũ): đánh dấu edit, review chỉ bằng căn cứ trong kho |
| 15:01 | User | Gold v3 (v2 + 2 câu test) |
| 15:1x | User | Spec sửa kho Q1–Q5 (§4 spec); Q4: A rút khuyến nghị "đóng 8B" (không có số chất lượng) ⇒ User: **thí nghiệm sau sửa kho** |
| 15:3x | User | Duyệt spec sửa kho sha `937cf8969810`; cho thử W27–W29; "cứ thoải mái thử nghiệm, so sánh, đánh giá … rồi chọn phương án phù hợp" |

## 3. Kết quả

| Việc | Người làm → kiểm | Kết quả |
|---|---|---|
| B71 rebase B1 lên `main` | B → C (`phase_8_2_b1_rebase2_review.md`) | `p82-b1` `c3d5607`; T1 giống byte; cổng context 10 đạt; ready 0 / 0 / 2 — merge sau B0 |
| C62 guide / report cũ | C → A | guide 8 "8.2 tạm dừng" ⇒ đang chạy; guide 6 thêm `chat_metrics`; B-06; `/tmp` + `python3`; `validate_gold.py` chặn ghi đè |
| C63 căn cứ tính năng mới | C → A kiểm 3 điểm | quyết định cũ "không streaming" (25/08, 11/09) + streaming không rút phần suy luận; hội thoại nhiều lượt va chính sách không ghi câu hỏi |
| B72 plan B3 (câu kín) | B → C 2 vòng | duyệt sha `27e75be5ed44`; ≈ 0,012 USD khi chạy |
| C64 `dense_ms` làm tròn | C → A (+ B) | `dfbcca5`; cổng 2 câu đạt |
| C64 / B74 / B75 nhãn 3 câu test | C đề xuất → B kiểm → B dựng v3 → C kiểm | gold v3 `3b1117cf59e9` mặc định (`fa192f8`); test B1 7 ⇒ 9 / 15; kết luận cũ không đổi |
| C65 câu 138 "no citation" | C → A | lượt B1 dùng validator v1; validator hiện tại nhận cả 12 câu ⇒ production không 500 |
| B73 soạn sửa kho | B (7 sub-agent) → C66 2 vòng | 41 diff (40 giữ + 1 có điều kiện); 12 chuyển nhóm; 16 câu User; 78 tra ngoài; file danh mục 33 đoạn |
| B74 tên đơn vị sót | B → C67 | 11 diff / 14 edit, ready |
| Spec sửa kho | A → C68 3 vòng | bản 3 `937cf8969810` ready ⇒ **User duyệt** 15:40 27/10/2026; vòng 1 bắt 2 major (nhãn lệch offset ⇒ bước gold v4; thiếu bộ "trước") |
| B76 yêu cầu ChatGPT tra ngoài | B → A kiểm (78 mục, chỉ câu ngắn) | chờ User gửi |
| Vòng cải tiến 8 | A → B kiểm | S41–S44; W27 (`scripts/grep_kb.sh`), W28, W29 cho thử |

## 4. Tiền

Paid (`gpt-6-luna`, token trong log): B71 cổng ≈ 0,000325; C review B71 ≈ 0,000453; C64 cổng ≈ 0,000379 ⇒ **≈ 0,0012 USD**. Sub-agent dùng quota (B73 ≈ 0,68 M token), không USD.

## 5. Giới hạn

- Sửa kho **chưa áp**; 97 / 139 mục C32 ban đầu chỉ có tự kiểm sub-agent — B73 đọc lại từng mục, C66 review từng diff.
- 16 câu chờ User; 78 mục tra ngoài chờ ChatGPT (dữ liệu ra ngoài: câu ngắn, User duyệt).
- Tính năng mới mới chỉ bàn; streaming lợi ích **chưa đo** (C suy ra: phần suy luận + ~1,2 s cố định không rút được).

## 6. Bước tiếp

1. **B0** (User) ⇒ merge B1 `c3d5607` + cổng + context 5 ⇒ 10 ở guide / Project_Status / 4 chỗ báo cáo.
2. **B3** (User quyết mở câu kín; B chạy theo plan `27e75be5ed44`) ⇒ đóng 8.2.
3. **Đợt sửa kho** theo spec `937cf8969810` §5 (bước 0 trước khi đụng kho); 16 câu User + kết quả ChatGPT 78 mục ⇒ đợt 2.
4. **Qwen3-8B** thí nghiệm (plan riêng). 5. **Tính năng mới:** đo "thời gian tới chữ đầu tiên" ⇒ spec streaming; rồi hội thoại nhiều lượt.

Đợt này **đóng** khi đợt sửa kho áp xong + đo "sau" đạt (phần áp có thể ghi tiếp vào folder này).

## 7. Phiên 28/10 (A `hue-rag-bf`, B `hue-rag-ac`, C `hue-rag-32`) — cập nhật 12:20 28/10/2026

### 7.1 Quyết định theo giờ

| Giờ | Ai | Quyết định |
|---|---|---|
| 09:2x | User | Quyền phiên (≤ 1 USD, A tự điều phối, B / C push nhánh riêng); thứ tự lỗi đồng ý; **PA3** — B0 không chặn (spec 8.2 §11) |
| 09:5x | User | Chạy B3; yêu cầu phi chức năng p50 ≤ 3 s / p95 ≤ 5 s / ≤ 0,0005 USD; thêm mức lỗi "sai cảnh báo an toàn" trên cùng |
| 09:5x | A | Duyệt plan B78 v2 `41485782b39e` (bước 0 chạy trước B3; giữ spec §5 "dừng + khôi phục"), plan C70 v2 `9683641b6c38` (giữ D10) |
| 10:23 | User | **Đóng Phase 8.2** (`report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`) |
| 10:3x | A | C73 vượt ước pilot 70 % ⇒ cho chạy (≈ 0,012 ≤ trần 0,03) |
| 11:0x | User | Chạy `!` xóa 3 đích (collection, build record, sparse state) trong terminal B |
| 11:2x | User | Duyệt 2 trích dẫn gold v4 + "0 câu Golden cần sửa"; đi nghỉ — "tiếp tục điều phối, thử nghiệm, … đóng gói" |
| 12:2x | A | Duyệt plan C78 v2 `52555da95828` (Qwen3-8B; chạy chờ User) |

### 7.2 Kết quả

| Việc | Kết quả | Bằng chứng |
|---|---|---|
| B78 đo trước ↔ sau (plan) | duyệt sau C72 + vòng sửa | `sua_kho_do_truoc_sau_plan.md`, `_review.md` |
| C70 / C73 thời gian tới chữ đầu tiên | **streaming rút chờ rõ**: chữ hiện sớm hơn trung vị 1,92 s [1,61; 4,31]; chữ đầu p50 2,44 / p95 4,80 s (8 câu); kiểu "chỉ câu có `[n]`" 1,01 s (chưa chắc); 0,0103 USD; nhánh hồ sơ `c70-ttft` | `streaming_ttft_*` |
| Sửa kho bước 1–6 (B81) | 123 edit / 65 file / 51 mục; 204 file / 8.426 đoạn; build `574b5d02088b`; T1 `23c58c47635d` (40 / 158 đổi top-10, giải thích được) | `sua_kho_b1_6_*` (C75 ready) |
| Bước 7–8 (B82) | gold v4 (2 trích dẫn User duyệt); 0 câu Golden cần sửa | `sua_kho_b7_8_*` (C76 ready) |
| Bước 9 (B83) | **không làm hỏng**: F1–F4 = 0; T1 4 tụt (≤ 5), TB −0,008; T2 TB 0; T3 12 ⇒ 13; p95 lượt "sau" không đại diện (phía mạng / provider) | `sua_kho_b9_*`, `sua_kho_b83_code_review.md` (C80 ready) |
| Bước 10 | `BAO_CAO_KHO_DU_LIEU` bản 5, `BAO_CAO_DANH_GIA` bản 4, `LUONG`, guide, README, nhật ký | commit `87c38fd` … `f420155` |
| C77 streaming | yêu cầu ChatGPT `c573949ac59a` (B đối chiếu code) chờ User gửi; bản nháp 4 phương án | `data/tinh_nang_moi_2026-10-27/c77_phuong_an_streaming.md` |
| C78 Qwen3-8B | plan duyệt; chạy chờ User | `qwen3_8b_plan*.md` |
| C79 đợt 2 | 96 edit / 34 file soạn sẵn; D1–D7 + 15 câu chờ User | `data/sua_kho_2026-10-27/dot2/` |

### 7.3 Tiền phiên 28/10 (từ log / report)

Cổng merge B1 0,000423; B3 0,0138; bộ "trước" 0,0361; C73 0,0103; cổng sau build 0,000449; bộ "sau" 0,0365 ⇒ **≈ 0,0976 USD** / trần phiên 1 USD. Đợt sửa kho ≈ 0,073 / 0,15.

### 7.4 Giới hạn

- Đợt sửa kho đợt 1 làm kho đúng hơn nhưng không nâng điểm (Golden không đổi); 2 lỗi nặng nhất (sai cảnh báo an toàn, bịa thêm) chưa có thước (B87 viết plan).
- Đoạn dài nhất sát trần tokenizer huydang (255 / 256).
- 11:50–11:56 có việc nặng CPU / Qdrant của C chạy song song lượt đo "sau" (lỗi điều phối A; phần trên máy không tăng).

### 7.4b Cập nhật 13:26 28/10/2026 (kết phiên)

- **User đóng đợt sửa kho đợt 1** (giữ sao lưu); Qwen3-8B + đợt 2 ⇒ phiên sau; cho thử W30 / W31 / I6.
- B89 thước lỗi nặng: nhận (C83 ready 2 vòng) — Golden 145 câu: bịa thêm 1, nói ngược nguồn 0, P0_sai 0 / 65; bộ 32 câu an toàn (0,0079 USD): P0_sai 2 / 27 (nói sai về nguồn), ngoài kho 0 / 4.
- Đợt 2 bản 3 `9b5105b35e8b` (104 edit / 33 file), B88 vòng 3 ready. Tiền phiên ≈ **0,106 USD**.

### 7.5 Chờ User

Đóng đợt sửa kho đợt 1; bước 11 xóa sao lưu; gửi ChatGPT yêu cầu streaming; duyệt chạy Qwen3-8B; đợt 2 (D1–D7, 15 câu); B0 khi rảnh; spec streaming (sau nghiên cứu).
