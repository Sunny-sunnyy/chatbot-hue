# Plan — T4 lịch trình từ câu gõ tự do (spec Phase 9 bản 13 §12, sha `5557f0fd7650`)

**A duyệt 09/11 (mức nhẹ, sau khi sửa 4 chỗ):** bản 2 sha `29708ef92e30` (sha tính trên file **trước** khi thêm dòng này).

Người viết: E · **bản 2a** (21:14 09/11/2026: thêm 1 dòng tiêu chí review C M-1 — A duyệt luôn; sha cuối A ghi ở `CURRENT_HANDOFF`, không ghi trong file) · **bản 2** · 20:50 09/11/2026 (`date`) — sửa 4 chỗ A ghi 09/11 (bộ 31 câu · giữ câu (b) · S5 chung · bỏ mốc câu lịch) · bản 1 `46f6fdd69f90` · A giao 09/11.
Mức: **nhẹ** (`Session_Prompt.md` §7 — ước ≈ 0,11 USD ≤ 0,2, không đổi kiến trúc: sửa trong `lich_trinh.py` / `assistant.py` + bật cờ có sẵn) ⇒ A đọc rồi duyệt,
đo 1 lượt (an toàn 32 ×2), 1 review cả nhánh. Spec §12.1: T4 làm **sau T2**; nhánh tách từ `main` lúc đó (đã có G — hoặc phương án B của G — và T2).
File tracked, repo public: không chép kho / câu bộ đo; câu tả ở mức loại.

## 1. Vấn đề, mốc, sửa (spec §12.2 dòng T4 + "Sửa trước khi đo lại T4")

- **Vấn đề (đã thấy):** cờ `lich_trinh` tắt từ 06/11 vì kín v2 chỉ đạt **3 / 5** (`report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`):
  - K2: hỏi lại thừa — người dùng có nêu số ngày, model gửi `so_ngay` khác số code dò ⇒ luật D12 (b) bắt hỏi;
  - E20: câu xin lịch **kèm** một câu hỏi thêm ⇒ 3 / 4 lượt model từ chối. Cả 3 lượt đều gọi `tim_kho` sau khi có lịch và bị chặn (`TOOL_DA_DU_LICH`)
    (`report_agent/2026-11-06_b5_cau_tu_nhien/e20_tu_choi_hoi_kem.md`). Từ B171, code dựng lời lịch tối thiểu khi model từ chối, nhưng không nói gì về phần hỏi thêm.
- **Mốc:** `main` lúc tách nhánh, cờ `lich_trinh` **tắt** (câu tự do ⇒ trả lời thường). Số cũ: kín v2 3 / 5.
- **Sửa (đều là code, tất định — khung AI FDE §2–§3: trường bắt buộc / phép tính ⇒ code):**
  - **(a) Số ngày code dò được ⇒ dùng số code.** `lich_trinh.chot_so_ngay`: thứ tự mới (1) `truong` từ nút (giữ D15 bản 7) · (2) **số dò trong câu (đúng một giá trị) ⇒ dùng, bỏ qua tham số model** · (3) không dò được ⇒ tham số model · (4) vẫn thiếu ⇒ hỏi lại (chỉ `so_ngay`, giữ D15). Gỡ nhánh "model gửi số khác ⇒ hỏi". Log công cụ ghi `so_ngay_model` + `so_ngay_do` (chỉ giá trị trường, không chữ).
  - **(b) E20 Sửa 1.** `assistant._finish_generated`, nhánh có lịch: khi chữ model = `INSUFFICIENT_ANSWER` (code dựng lời lịch tối thiểu như B171) **và** lượt có `tim_kho` sau lịch (`tools` có `sau_lich`) ⇒ code nối thêm **một câu cố định** sau lời lịch: "Phần bạn hỏi thêm ngoài lịch hiện chưa có trong nguồn dữ liệu của mình." (chữ A / User duyệt lúc duyệt plan). Câu này nằm ngoài chữ model, đi qua kiểm cuối + kiểm citation như lời lịch tối thiểu (không có [n] ⇒ đặt sau phần có nguồn; test kiểm `select_cited_sources` không ném).
  - **(c) Harness ghi** `so_ngay` model gửi · số code dò · có thẻ hỏi không · có `tim_kho` sau lịch không (đề xuất C210) — từ log công cụ ở (a), 0 USD.
  - **(d) E20 Sửa 2** (`tim_kho` sau lịch được tìm thật 1 lần) — **chỉ khi** (a)–(b) đo xong mà vẫn còn lượt "từ chối thay cả lịch". Không làm trong plan này; nếu cần ⇒ bản 2.
  - **Bật cờ** `lich_trinh: true` trên nhánh đo (cờ trong `settings.yaml`; merge với cờ theo kết quả). Biểu mẫu "Lên kế hoạch", luật khung, kiểm cuối, bảng `diem_v3.json`: **giữ**.
- **Ngoài phạm vi:** sửa lịch nhiều lượt (nhánh `p9-sua-lich` hoãn — chỉ tư liệu: nếu merge sau phải giữ `hoi_toi` + `chon_sang`); giờ tới / về; dò "cuối tuần / 2 hôm / 4n3d" (`do_so_ngay` chưa bắt — khi không dò được thì tin model, **không** gây hỏi thừa); đổi lời dặn / mô tả công cụ.

## 2. Có bộ kín không — **không**, và vì sao

- Spec §12.4 dòng T4: "**không** — các sửa là code; kín v2 đã dùng". Luật cắt giảm 05/11 (2): bộ kín chỉ cho bậc **chỉnh lời dặn / mô tả công cụ qua nhiều vòng**.
  (a)–(c) là code tất định (kiểm bằng test + đếm), không có vòng chỉnh chữ gửi model.
- **Điều kiện dừng:** nếu sau lượt đo cần đổi lời dặn / mô tả công cụ ⇒ **dừng plan này**, viết bản mới **có** bộ kín. Người viết câu kín ≠ người sửa lời dặn.

## 3. Bộ đo (đã thấy) — 31 câu (spec §12.2 ghi 36; bỏ 5 câu kín v2 — A 09/11)

| Bộ | Số câu | Đường dẫn (private) | Ghi |
|---|---|---|---|
| B5 đã thấy | 13 | `data/phase_9/bo_do_b5/cau_da_thay.jsonl` | có cột `nhom`, `ky_vong` |
| E19 câu mẫu tự nhiên | 8 | `data/phase_9/b5_v2/mau_cau_tu_nhien.md` §3 | E tách ra `data/phase_9/t4/cau_e19.jsonl` (0 USD) |
| ~~kín v2 — đã dùng~~ | ~~5~~ | — | **A 09/11: không dùng** (mở phải nhờ User `!`, lợi ít) ⇒ bộ **31 câu**; giới hạn: 5 câu từng làm âm (K2, K3) không có trong lượt này — K2 có ca tương đương ở E19 / B5 (câu có số ngày) |
| E20 hỏi kèm | 10 | `data/phase_9/b5_v2/e20/cau_e20.jsonl` | 5 cặp có / không hỏi kèm |

Cộng các sàn chung (spec §12.3): **an toàn 32** (cờ bật ⇒ công cụ `lich_trinh` có mặt **mọi lượt** — D16 — nên chuỗi gửi model đổi ở **mọi** câu; bài học B4b / B5c: công cụ có mặt mọi lượt đổi cách model tìm ⇒ S1 + S4 bắt buộc) · **Golden mẫu 30** (S4, S3b, S6) · **bộ ngoài phạm vi đã thấy 44 của G** (`s2`, S2 / S2b — agent có thể gọi `lich_trinh` cho câu ngoài phạm vi).

## 4. Tiêu chí ghi trước (số cuối trên **đúng sha khoá** nhánh)

| Mã | Đo | Mức đạt |
|---|---|---|
| **Q3** | 31 câu, nhánh 1 lượt, **2 sub-agent chấm mù** (ngữ cảnh mới; phiếu Q3 của B5: (i) đúng luật xếp · (ii) hợp người đi cùng · (iii) mỗi điểm có nguồn) | đạt cả 3 ở **≥ n − 1 / n** câu có lịch (n = số câu nhãn "xin lịch"); 2 người lệch ⇒ E đọc + ghi lý do, lệch đổi kết quả ⇒ báo A |
| **K2** | câu có số ngày code dò được | **0** thẻ hỏi lại (đếm bằng code từ log (c)) |
| **E20** | câu xin lịch (có / không hỏi kèm) | **0** lượt "từ chối thay cả lịch" (chữ cuối không có lịch); câu hỏi kèm mà kho không có ⇒ có câu cố định (b) |
| **(b) không nói sai** (review C M-1, thêm 21:14 09/11/2026 trước lượt có phí) | câu xin lịch **không** hỏi kèm: 5 câu E20 nhóm không hỏi kèm + mọi câu lịch B5 / E19 | **0** câu có câu cố định (b) (code đếm chuỗi `CAU_HOI_THEM_CHUA_CO` trong chữ cuối; nhãn "có / không hỏi kèm" ghi trước lượt có phí). > 0 ⇒ (b) âm ⇒ bàn điều kiện hẹp hơn, không sửa trong lượt |
| Q2 | mọi lịch nhánh | `kiem_khung` 0 lỗi; kiểm cuối D8 0 lỗi lọt (như B5) |
| **S1** | an toàn 32, **nhánh ×2**; mốc ×1 (hoặc dùng lại — mục 5) | 4 số: đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 · ngoài kho bị trả lời 0 (S-AT khi chênh 1) |
| **S2 / S2b** | `s2` 44 câu ngoài phạm vi đã thấy, nhánh ×1, web thật | 0 câu bị trả lời; 0 lượt có `trace.web` (sàn tuyệt đối ⇒ không cần mốc) |
| **S3b** | mọi lượt cả câu ở trên | 0 câu Huế ra `OUT_OF_SCOPE_ANSWER` (code đếm) |
| **S4** | Golden mẫu 30 nhánh ↔ mốc, chấm mù 1 sub-agent (như G) | tụt < 3 / 30 |
| **S6** | `chat_metrics.usd` mẫu 30 (câu Huế không mục web) | ≤ 0,0005 USD / câu; báo riêng USD / câu lịch trình |
| S5 | — | **không đo riêng** — A chốt 09/11: đo chung một lần trên `main` lúc đóng đợt |

**Đạt** = Q3 + K2 + E20 + Q2 + S1 (×2) + S2 / S2b + S3b + S4 + S6 ⇒ merge **cờ bật** (A trình User). **Âm** ⇒ phương án B spec: giữ biểu mẫu là đường lịch trình duy nhất; câu gõ tự do ⇒ code gợi ý mở biểu mẫu (bậc riêng, plan riêng); hoặc (d) nếu chỉ E20 âm.

## 5. Thứ tự

1. Nhánh `p9-t4-lich` từ `main` (sau T2); khai báo file trong `STATUS_E.md`.
2. Code (a)–(c) + test (0 USD): `chot_so_ngay` mỗi nhánh của thứ tự mới (nút · dò được + model khác ⇒ dùng số dò, **không** thẻ · không dò ⇒ model · thiếu ⇒ thẻ); (b) cả 3 đường (`/api/chat`, stream, #6) — câu cố định nối đúng một lần, chỉ khi có `sau_lich`; lượt có lịch không `sau_lich` ⇒ như B171. **Q1:** cờ `lich_trinh` tắt ⇒ chuỗi gửi model 228 / 228 giống byte `main` (code chạm đường có lịch). Test 4c mỗi loại lượt (lượt đầu · có lịch sử · lượt ghép nút · biểu mẫu không đổi).
3. Tách 8 câu E19 + chạy thử harness 0 USD (đếm bộ, `--help`, khoá giả `OPENAI_BASE_URL` lỗi như B5).
4. **1 lượt có phí** (khi G + T2 đã vào `main`, nhánh rebase): server nhánh (cờ bật tạm), `/api/chat/stream` thật, `chat_metrics` theo `turn_id`. **31 câu lịch chỉ chạy nhánh** (A 09/11: mốc cờ tắt không có lịch, Q3 không dùng mốc, mức nền K2 / E20 đã có — kín v2 3 / 5). Server `main` (mốc) chỉ cho an toàn 32 + mẫu 30 khi không dùng lại được.
   **Mốc dùng lại (0 USD):** an toàn 32 + mẫu 30 của lượt khoá G **nếu** `main` lúc tách = sha G khoá + chỉ các bậc cờ tắt (T1 / T3 / T2 cờ tắt ⇒ Q1 giống byte) — E kiểm bằng Q1 trước khi dùng lại; không đạt ⇒ chạy mốc.
5. Chấm: 2 sub-agent Q3 (mù cặp không cần — mốc không có lịch); 1 sub-agent S4 mù cặp; S1 theo `data/phase_9/t1/cham/brief_cham.md` phần 2 (2 người như luật S-AT).
6. Report `report_agent/<đợt>/e_t4_lich_trinh_implementation.md` + đoạn lời thường cho `BAO_CAO_SINH_CAU_TRA_LOI_API` ⇒ test rộng 1 lần ⇒ review cả nhánh.

## 6. Tiền (giá `gpt-6-luna` từ `chat_metrics`: lượt có lịch ≈ 0,0009; câu thường ≈ 0,0006; ngoài phạm vi ≈ 0,0005; web +0,0012)

- 31 câu × **1 bên** (nhánh) × 0,0009 ≈ **0,028**
- an toàn 32 × 2 lượt × 0,0006 (nhánh) ≈ **0,038**; mốc ×1 ≈ 0,019 nếu không dùng lại được
- mẫu 30 × 0,0006 (nhánh) ≈ **0,018**; mốc ≈ 0,018 nếu không dùng lại
- `s2` 44 × 0,0005 (+ web nếu lọt) ≈ **0,025**
- ⇒ **≈ 0,11** (dùng lại mốc) · **≈ 0,15** (không dùng lại) ⇒ **dừng ở 0,2 USD**. Chấm: sub-agent (0 USD API).

## 7. Câu hỏi cho A — đã trả lời 09/11

1. Kín v2: **không mở** ⇒ bộ 31 câu (mục 3). 2. Câu cố định (b): **giữ** như trên. 3. S5: **đo chung** lúc đóng đợt. Thêm: bỏ mốc 31 câu lịch (mục 5 bước 4).
