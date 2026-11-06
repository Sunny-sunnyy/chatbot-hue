# E19 — chạy + chấm bộ kín B5 v2 (Q3 lịch trình)

Người làm: E (Claude Code `hue-rag-28`). Ngày 06/11/2026, chạy lúc ≈ 22:00 (giờ ghi file: 22:10 06/11/2026 `date`). A giao, A cho chạy.
File tracked, repo public: không chép câu, chữ trả lời hay nội dung kho. Câu tả ở mức loại / mã câu.

## 1. Bộ câu

- `data/phase_9/b5_v2/cau_sealed.jsonl` md5 **`de95ff85e491`** (5 câu K1–K5, private).
- Viết theo giọng 8 câu mẫu User đã duyệt sáng 06/11. User duyệt độ tự nhiên qua 3 vòng, bàn thẳng với E ở terminal E (A cho, A không thấy câu):
  - vòng 1: K1 đạt;
  - vòng 2: K4, K5 đạt;
  - vòng 3: K2, K3 đạt.
- Bản bỏ: `cd552f7cf7cb` (`cau_sealed_v1_bo.jsonl`).
- Luật A giữ đúng: không câu hai lượt; 2 / 5 câu có phần ngoài lịch (K4, K5).
- Thay đổi theo ý User: bỏ "1 câu dài kể hoàn cảnh" ("người ta hỏi ngắn gọn, vừa đủ").
- Loại câu:

| Câu | Loại |
|---|---|
| K1 | cặp đôi, sở thích ăn uống, **thiếu số ngày** |
| K2 | người lớn tuổi, 2 ngày, viết tắt, có tên 2 điểm |
| K3 | nhóm bạn, 1 ngày, muốn đi nhiều chỗ + tiết kiệm |
| K4 | gia đình trẻ nhỏ, 3 ngày, hỏi thêm chỗ ở |
| K5 | một mình, 4 ngày, có sở thích + ý né, hỏi thêm cách đi |

## 2. Chạy

- Code: `main` `c3ce3e5` (B5b + B171), `settings.yaml` không sửa. Harness B5 cũ `data/phase_9/b5/tools/chay_b5.py` (cờ `lich_trinh` bật trong tiến trình), chỉ đổi đường dẫn bộ câu (A quyết).
- Trước lượt có phí, 0 USD:
  - `kiem` ⇒ n 5;
  - chạy thử bằng khoá giả + cổng đóng ⇒ cả 5 câu đi tới bước gọi model, không vỡ.
- Lượt có phí (User `!`): **n 5 · lỗi 0 · 0,003029 USD**. Kết quả `data/phase_9/b5_v2/kin_v2_ra.jsonl` (private).
- `dem` (0 USD):
  - hỏi lại số ngày: K1, K2;
  - kiểm cuối 0; lỗi khung 0; rút lại 0; `max_turns` 0.
  - Hai dòng `Q2a_n` / `lech_nhan` ra 0 / rỗng: **không có nghĩa trên bộ này**, vì bộ v2 không có trường `nhom` / `ky_vong` mà hai dòng đó đọc. So trường B5 mong đợi để 2 agent chấm.

## 3. Chấm

Hai sub-agent Claude, ngữ cảnh mới, độc lập, không xem bài của nhau.
- Mỗi agent nhận: câu + trường mong đợi + `can_cham` của từng câu; bảng ràng buộc R1–R15; file kết quả; bảng điểm; luật xếp.
- 3 tiêu chí Q3 nguyên văn plan B5; ngưỡng **đạt cả 3 ở ≥ 4 / 5**.
- Luật cho câu không ra lịch, theo `can_cham` ghi trước khi chạy: mong hỏi lại mà hỏi đúng ⇒ đạt; đủ thông tin mà vẫn hỏi ⇒ không.
- Phiếu: `data/phase_9/b5_v2/cham_agent_1.md`, `cham_agent_2.md` (private).

| Tiêu chí | Agent 1 | Agent 2 | Câu không đạt |
|---|---|---|---|
| (i) đúng luật xếp | 4 / 5 | 4 / 5 | K2 |
| (ii) hợp người đi cùng / kiểu đi | 3 / 5 | 3 / 5 | K2, K3 |
| (iii) mỗi điểm có nguồn | 4 / 5 | 4 / 5 | K2 |
| đạt cả 3 | 3 / 5 | 3 / 5 | — |

Hai agent **khớp 15 / 15 ô**. Kết luận theo luật ghi trước: **Q3 không đạt** (3 / 5 < 4 / 5).

## 4. Lỗi theo câu — quan sát / nguyên nhân

- **K2 `hoi_lai_thua` (3 ô):** câu có số ngày viết tắt; hàm dò của code đọc ra đúng 2 ngày (chạy 0 USD), nhưng lượt vẫn dừng ở thẻ hỏi số ngày.
  - **Nguyên nhân chứng minh bằng code:** `lich_trinh.chot_so_ngay` chỉ trả "cần hỏi" khi (a) model không gửi số **và** code không dò được, hoặc (b) model gửi số **khác** số code dò. Code dò được ⇒ chỉ còn (b): model gửi số khác 2.
  - Model gửi số nào thì chưa biết, vì harness không lưu tham số công cụ.
  - Luật "lệch ⇒ hỏi" là thiết kế D12 (b) của B5; câu viết tắt kiểu "số ngày + số đêm" làm model đọc lệch.
- **K3 `khong_day_lich` (ii):** người dùng muốn đi nhiều chỗ; code nhận đúng `kieu_di = day_lich`, nhưng khung 1 ngày chỉ có 2 điểm, không buổi tối — như lịch thong thả.
  - Quan sát khớp ghi nhận cũ của A ("đi dày ít tác dụng vì bảng điểm thiếu thời lượng"): `xep` chỉ thêm suất thứ hai khi cả hai điểm cùng cụm và đều "ngắn".
- **Ngoài 3 tiêu chí (cả hai agent cùng ghi):**
  - **K4, K5: chữ model là câu từ chối ngắn (75 ký tự). Lịch người dùng thấy là lời do code dựng từ khung** (đường T3 của B171).
    - Hệ quả: câu hỏi thêm (chỗ ở, cách đi) bị bỏ qua im lặng — không bịa, nhưng cũng không nói thật là không có.
    - **2 / 5 câu "đạt" nhờ đường dự phòng của code, không nhờ model.**
  - K4: lịch bỏ buổi tối vì có trẻ nhỏ mà không có câu nói vì sao. Câu lý do chỉ nối khi người dùng tự xin buổi tối (B171).
  - K5: một ý sở thích của câu không có điểm tương ứng trong bảng điểm (kho có tài liệu); một ý "né" của câu không được đáp.
- **Giới hạn (iii):** file kết quả không lưu chữ của đoạn nguồn. Agent đối chiếu số `[n]` trong lời với bản đồ nguồn code gán (agent 1: 16 / 16), và file của từng điểm có trong kho. Chưa đọc được nội dung đoạn.

## 5. Theo luật ghi trước

Plan B5 "Kết quả âm: Q3 < 4 / 5 ⇒ cờ `lich_trinh` tắt; … Kín ngược chiều ⇒ không chỉnh lại trên kín". Cờ đang tắt, giữ tắt.
Sửa nếu có làm trên bộ đã thấy (A / User quyết). E chỉ ghi các loại lỗi ở mức loại câu.

## 6. Tiền

0,003029 USD (lượt có phí). Chấm bằng quota Claude. Phase 9 cộng thêm 0,003.

## 7. Bước tiếp (đề xuất, A / User quyết)

1. User đọc ô không đạt: K2 (3 ô), K3 (ii) ở hai phiếu `cham_agent_*.md`.
2. A quyết hướng sửa — đều đo trên bộ đã thấy, không trên kín:
   - (a) K2: khi model lệch với số code dò được rõ ràng thì tin số code, thay vì hỏi;
   - (b) K3: "đi dày" cần cột thời lượng cho bảng điểm;
   - (c) K4 / K5: vì sao model từ chối khi câu có câu hỏi phụ.
