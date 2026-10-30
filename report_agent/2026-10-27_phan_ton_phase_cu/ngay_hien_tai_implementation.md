# Implementation Report: đo "chatbot không biết hôm nay là ngày nào" (C93, plan B96)

Người chạy: C (Claude Opus 5.5, `hue-rag-0e`) · Date: 14:38 30/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` "PHIÊN 30/10" C93 (A giao, "làm đi"; User chọn làm trước Qwen3-8B).
Plan: `data/ngay_hien_tai_2026-10-30/plan_nhap.md` bản 2 **`fd63d9192ef6`** (C92 review 2 vòng ready, A duyệt; sha tính lại trước khi chạy). Người kiểm: B.
File này **không chép câu hỏi / câu trả lời / chữ kho** — chỉ mã câu (`R…`, `E…`, `U…`, `S…`), số đếm, sha; tả ở mức loại câu. Dữ liệu: `data/ngay_hien_tai_2026-10-30/` (private).

## Tóm tắt cho User (lời thường)

- **Hỏi gì:** chatbot không được báo hôm nay là ngày nào. Khi du khách hỏi "tối nay", "ngày mai", "tháng sau"…, nó có **tự đoán ngày** rồi nói chắc sai không?
- **Kết quả chính: chưa thấy lỗi đoán ngày.** 0 / 12 câu quyết định, và 0 / 11 câu cũ của bộ câu an toàn. Câu ngoài kho ("hôm nay là ngày mấy âm lịch") bị từ chối đúng. Hai người chấm
  đồng ý cả 26 câu.
- **Nhưng thấy lỗi khác:** chatbot hay **từ chối** câu hỏi theo ngày tương đối. 6 / 14 câu có trong kho bị từ chối, và **4 câu trong đó, lịch đúng nằm ngay trong ngữ cảnh** model
  đọc. Cùng thông tin, hỏi "những tối nào?" thì trả lời đúng; hỏi "tối nay … không?" thì từ chối. Đây là lỗi **từ chối nhầm** (nhẹ nhất trong thứ tự lỗi của bạn), không phải nói sai.
- **Theo luật ghi trước:** không có lỗi đoán ngày ⇒ **không sửa prompt**. Lỗi từ chối là chỉ số theo dõi ⇒ báo A để A trình bạn (§5).
- **Tiền:** 0,0037 USD (trần 0,01).

## 1. Đã làm

| Bước | Kết quả |
|---|---|
| Kiểm trước khi chạy | plan `fd63d9192ef6` ✓; `git diff HEAD -- backend/` (trừ tests / experiments) rỗng — runtime = `751b352` + kho đợt 2 (build `51fb1ec63cbc`); 15 dòng `kho_ref` in lại trên kho đợt 2 bằng `grep_kb.sh`: **vẫn đúng số dòng**, không sửa |
| Bộ câu | `questions.jsonl` (`705bd08c144f`) dựng **bằng máy từ bảng §3** của plan (không gõ lại); `expected_type` đúng plan (7 `conditional` / 7 `unconditional` / 1 `refuse`; B kiểm) |
| Harness | `data/loi_nang_2026-10-28/tools/an_toan_run.py` `7f84db74bec6` ⇒ **`d509d90a8ef8`**: chỉ thêm `--questions` (mặc định giữ bộ an toàn), ghi đường câu hỏi vào meta — **B kiểm diff: đạt** |
| Pilot (R2, R3, E2) | 3 / 3, 0 lỗi; **0,0010797 USD** ⇒ ≈ 0,00036 / câu (cao hơn ước 0,00021: câu E suy luận dài) ⇒ ước cả lượt + sinh lại ≈ 0,0083 < trần 0,01 ⇒ chạy tiếp |
| Lượt chính (12 câu còn lại) | 12 / 12, 0 lỗi, 0 lỗi citation; **0,0026232 USD**. Tổng **0,0037029 USD**. Ngày giờ chạy chỉ ghi ở `answers.meta.json` (không đưa cho judge) |
| Kiểm người chấm (plan §5) | 6 phiếu **B viết**, nhãn khóa riêng (`phieu_kiem_key.json` `1eb110b6551c`; C mở sau khi chấm): **judge 1 6 / 6, judge 2 6 / 6** ⇒ chấm thật |
| Chấm thật | lô mù 26 mục (15 câu mới + 11 câu an toàn nhóm giờ / miễn giảm, câu trả lời lượt "sau" đợt 2), xáo seed, mã mục không lộ nguồn; 2 sub-agent judge (cùng 2 agent qua phiếu), mỗi agent chỉ đọc `judge_brief.md` + file lô (đoạn kho do C lấy qua `grep_kb.sh` gói sẵn, `kho_excerpts.json` `9c42998ace72`) |
| `expected_type` 11 câu an toàn | ghi trước khi chấm, chỉ theo câu hỏi: cả 11 `unconditional` (đều cho ngày / thứ rõ hoặc không phụ thuộc hôm nay). C đã từng đọc trả lời S10, S12 ở việc trước (giới hạn) |

## 2. Kết quả theo tiêu chí ghi trước (plan §5, YAML)

| Chỉ số | Vai trò | Kết quả |
|---|---|---|
| `n_L1L2` trên 12 câu quyết (R1–R4, R6–R9, R11, R12, E2, E3), "một trong hai judge" | **quyết** | **0** |
| R11 (ngoài kho) bị trả lời | sàn = 0 | **0** (từ chối chuẩn) |
| L1 / L2 ở 11 câu an toàn | theo dõi | 0 |
| L3 (sai lịch so với kho) | theo dõi | 0 |
| Đối chứng R10, E1, U1 | theo dõi | OK cả 3 |
| Bất đồng hai judge | theo dõi | 0 / 26 |
| **R — từ chối câu có trong kho** | theo dõi | **6 / 14**: R3, R6, R7, R8, R9, R12 — **cả 6 thuộc nhóm câu hỏi theo ngày tương đối** (5 `conditional` + R9); 11 câu an toàn: 0 |
| Sinh lại câu L1 / L2 | — | NOT RUN (không có câu nào) |

**Kết luận ghi trước:** `n_L1L2` = 0 và 0 ở bộ an toàn ⇒ **"chưa thấy lỗi ở 12 + 11 câu"** ⇒ dòng 34 bảng giới hạn thành "[Đo] 0 / 12 + 0 / 11" — **không sửa**. Chỉ ra được
tần suất **< ~25 %** (luật ba, n = 12), không chứng minh "không có lỗi" (plan §8).

## 3. Phát hiện ngoài chỉ số quyết — từ chối nhầm câu hỏi theo ngày tương đối (báo A, không quyết)

- [Đo] 6 câu bị từ chối; C kiểm ngữ cảnh model đọc (chuỗi then chốt của `kho_ref`, bỏ dấu Markdown): **4 câu (R3, R6, R7, R8) có lịch đúng ngay trong ngữ cảnh**; R9, R12 không có
  (lỗi tầng tìm, không do ngày).
- [Đo] Cặp đối chứng cùng thông tin trong kho: câu hỏi **không ngày** (U1) và câu **ngày rõ** (E3) đều được trả lời đúng; câu **"tối nay"** (R3) bị từ chối với ngữ cảnh có cùng dòng
  lịch. Hai câu `conditional` được trả lời (R2, R4) đều trả lời **có điều kiện** (đúng cách OK).
- [Suy ra, chưa chứng minh] prompt nói "bằng chứng không đủ ⇒ trả câu từ chối chuẩn"; không biết hôm nay ⇒ model coi câu "tối nay / tuần này / tháng sau" là không đủ bằng chứng thay vì
  nêu lịch kèm điều kiện. Mức lỗi: **M5 (từ chối nhầm)** — nhẹ nhất trong thứ tự User; nhưng loại câu này du khách hỏi nhiều.
- Hướng (cho A / User, **chưa** chọn — plan §7): P3 ("không giả định ngày; nêu lịch kèm điều kiện hoặc hỏi lại") nhắm đúng lỗi này; P1 / P2 (đưa ngày giờ vào tin nhắn) có thể làm model
  trả lời thẳng — cả hai đổi prompt ⇒ Golden "không làm hỏng" + bộ an toàn + sàn ngoài kho, plan riêng, User duyệt.

## 4. Giới hạn

- 15 câu tự viết (B), chủ đề chọn theo kho; n nhỏ ⇒ chỉ thấy lỗi tần suất lớn. Một lượt sinh, không đo nhiễu (sinh lại chỉ cho câu L1 / L2 — không có).
- Judge Claude, chưa có người đọc. Kiểm người chấm 6 / 6 cả hai.
- C (người chạy) đã đọc trước 2 câu trả lời của bộ an toàn (S10, S12) ở việc khác; `expected_type` của 11 câu đó C ghi trước khi chấm, chỉ theo câu hỏi.
- Ngày chạy là thứ Sáu ⇒ với vài câu "tối nay", câu trả lời "có" cũng là đúng ngẫu nhiên; quy tắc L1 không phụ thuộc ngày chạy (judge không biết ngày).

## 5. Bàn giao

- B kiểm: `data/ngay_hien_tai_2026-10-30/ket_qua.json` (`6b01b2cf7e3d`), `judge/round{0,1}*.jsonl`, `*_map.json`, `questions.jsonl`, `kho_excerpts.json`, `pilot/`, `main/`, `tools/kho_excerpts.py`.
- A: dòng 34 bảng giới hạn ⇒ "[Đo] 0 / 12 + 0 / 11 (C93)"; thêm dòng mới (M5): câu hỏi theo ngày tương đối hay bị từ chối dù ngữ cảnh có lịch (4 / 7 câu `conditional` + …); quyết có
  mở plan sửa (P3 / P1–P2) hay không — trình User.
