# Implementation Report: Phase 9 bước 5 — vòng hệ thống TỰ TỐI ƯU, bản hẹp ở bước tìm: dò 15 cấu hình, 0 cấu hình được đề nghị

Người làm: B (Claude Code — Fable 5.2). Người duyệt plan + đọc hàm trộn có trọng số: A. Review kết quả: chưa có lúc viết.
Date: 08:40 19/11/2026 (`date`). Chạy 08:35–08:38 19/11/2026.
Plan: `data/cach_lam_2026-11-18/PLAN_TU_TOI_UU_BUOC_TIM.md` (private; A duyệt bản sha `09bb74c5c4d0` lúc 08:18 19/11/2026; file sau khi ghi thêm kết quả bước 0 + lệnh bọc: `44e9a0df3dd0`). Điều kiện do User chốt 13:56 18/11/2026.

> **Kết luận một dòng:** trên kho hôm nay (9.436 đoạn), trong 15 cấu hình bước tìm đã dò **không cấu hình nào đưa được nhiều đoạn đúng hơn bản đang chạy một cách vượt nhiễu** ⇒ 0 cấu hình được đề nghị,
> nhóm câu giữ riêng KHÔNG mở, không đổi gì trong chatbot. Đây là kết quả "không khác", không phải "đã chứng minh bản đang chạy là tốt nhất".

Từ dùng: **cấu hình** = bộ tham số của bước tìm lúc hỏi (không dựng lại chỉ mục) · **đoạn đúng** = đoạn kho chứa đáp án, đã gắn nhãn cho 55 câu khó (nhãn bản 5) · **đủ đoạn đúng** = mọi ý của câu đều có
ít nhất một đoạn đúng trong 10 đoạn đầu · **nhóm dò** = 120 câu `dev` (dùng để chọn) · **nhóm giữ riêng** = 56 câu `test` (chỉ để xác nhận) · **ứng viên** = số đoạn mỗi nhánh lấy ra trước khi trộn ·
**k** = hệ số của cách trộn thứ hạng RRF · **DBSF** = cách trộn theo điểm đã chuẩn hoá thay vì theo thứ hạng · **Holm** = chỉnh khi so nhiều cấu hình cùng lúc để không nhận nhầm một cấu hình "thắng may".

## 1. Phạm vi

- Đã làm: bước 0 (kiểm nhãn còn khớp kho) ⇒ bước 1 (mốc ×2 + hai mốc ngây thơ) ⇒ bước 2–3 (lưới trên nhóm dò + cột báo trên 18 câu ngoài kho, so theo cặp, Holm, luật chọn). Bước 4 (xác nhận trên nhóm giữ riêng): **NOT RUN** — đúng luật ghi trước, vì không cấu hình nào qua nhóm dò.
- Không đụng: lời dặn, model, chia đoạn, kho, chỉ mục, bộ đo, nhãn, `backend/`. Chỉ đọc Qdrant; không gọi model sinh; **0 USD**.
- Bản code: `main` `63a6909` (`git diff 3abb076 HEAD -- backend` rỗng ⇒ cùng code với mốc đứng yên `3abb076`). Chỉ mục: collection đang chạy, 9.436 đoạn.

## 2. Thay đổi chính

Không đổi file nào được git theo dõi ngoài báo cáo. Công cụ thử (private, `data/cach_lam_2026-11-18/tu_toi_uu/tools/`): `buoc0_nhan_khop_kho.py` · `rrf_trong_so.py` (trộn RRF có trọng số từng nhánh, hàm thuần; trọng số 1:1 cho kết quả
giống hệt hàm của bản chạy trên 200 đầu vào có seed — 4 test đạt) · `vong_tu_toi_uu.py` (lệnh bọc: gọi bản chạy qua tham số, dùng lại hàm chấm + so sánh của `backend/experiments/phase_8_1/g1_retrieval.py`).

## 3. Cách đã chạy thật

Từ `backend/`, một tiến trình, `timeout 1800`, Qdrant thật của dự án (chỉ đọc), model vector `e5-small` thật:
`uv run … vong_tu_toi_uu.py moc` (95,6 s, RAM đỉnh 1,55 GB) ⇒ `… luoi` (70,7 s, RAM đỉnh 1,71 GB) ⇒ `… bang`. Lần gọi đầu của `moc` hỏng sau 0,1 s vì thiếu đường dẫn import (chưa tìm gì) — sửa một dòng ở công cụ rồi chạy lại.
Ba rào trong code đều qua: ở MỌI câu, trộn lại với k = 60 và trọng số 1:1 ra đúng 10 đoạn bản chạy trả về · hai lượt mốc giống hệt nhau (dấu vân tay kết quả tìm nhóm dò ngày 19/11: `3f5fb40ec51a`) · không ghi đè file kết quả.
Kết quả từng câu: `data/cach_lam_2026-11-18/tu_toi_uu/ket_qua/` (private).

## 4. Kết quả quan sát

### 4.1 Bước 0 — thước còn dùng được không
Nhãn đoạn đúng bản 5 gắn theo kho ngày 30/10; kho đã lớn lên từ đó. 174 trích dẫn của 55 câu: **168 còn đúng vị trí (96,6 %; ngưỡng dừng ghi trước 95 %)**, 6 còn nguyên chữ nhưng đổi vị trí, 0 mất.
Hai câu nhóm dò (case 67, 167) có ý không còn trích dẫn nào đúng vị trí ⇒ **ghi trước khi thấy số tìm:** chỉ số quyết tính trên 38 câu nhóm dò có nhãn dùng được; nhóm giữ riêng 15 / 15 câu dùng được.

### 4.2 Mốc và cỡ mẫu (tính trước khi chạy lưới)
- Bản đang chạy (vector + từ khoá trộn RRF, 30 ứng viên, k = 60): **22 / 38 câu đủ đoạn đúng** trong 10 đoạn; tỉ lệ ý có trong 10 đoạn 0,764; MRR theo từ khoá 0,7325 (108 câu trong kho của nhóm dò).
- Số câu CÓ THỂ tốt lên: 16. Để khoảng tin cậy theo cặp nằm trên 0 cần ≥ 4 câu thắng / 0 câu thua cho một cấu hình, ≥ 6 ở bậc chặt nhất của Holm ⇒ thí nghiệm đủ chỗ để thấy một cải thiện cỡ đó.
- **Mốc ngây thơ — thước này phân biệt YẾU:** "chỉ vector" 22 / 38 (bằng đúng bản đang chạy), "chỉ từ khoá, tìm trong cả kho" 23 / 38. Tức theo thước "đủ đoạn đúng trong 10 đoạn", việc trộn hai nhánh không tạo khác biệt đo được
  trên 38 câu này (thước từ khoá thì có: MRR 0,7325 so với 0,7007 và 0,7206). Mọi kết luận dưới đây phải đọc kèm giới hạn này.

### 4.3 Bảng lưới — nhóm dò 38 câu, so theo cặp với mốc (bảng do lệnh `bang` in, B chỉ đổi tên cột và làm tròn)

| Cấu hình | Đủ đoạn đúng | Thắng / thua | Khoảng tin cậy 95 % của chênh | Sau Holm | Câu mất đủ-đoạn-đúng | Câu ngoài kho đổi 10 đoạn (/ 18, chỉ báo) |
|---|---:|---|---|---|---:|---:|
| **Mốc — bản đang chạy** | **22 / 38** | — | — | — | — | — |
| 20 ứng viên | 22 | 1 / 1 | [−0,079; +0,079] | không khác | 1 | 12 |
| 50 ứng viên | 22 | 0 / 0 | [0; 0] | không khác | 0 | 9 |
| k = 20 | 23 | 1 / 0 | [0; +0,079] | không khác | 0 | 12 |
| k = 100 | 22 | 0 / 0 | [0; 0] | không khác | 0 | 1 |
| Tìm độc lập hai nhánh rồi trộn | 24 | 2 / 0 | [0; +0,132] | không khác | 0 | 18 |
| DBSF, trọng số từ khoá 0,3 | 23 | 1 / 0 | [0; +0,079] | không khác | 0 | 17 |
| DBSF, trọng số từ khoá 0,5 | **25** | **3 / 0** | [0; +0,184] | không khác | 0 | 18 |
| DBSF, trọng số từ khoá 0,7 | 24 | 3 / 1 | [−0,053; +0,158] | không khác | 1 | 18 |
| RRF trọng số vector : từ khoá 2:1 | 22 | 1 / 1 | [−0,079; +0,079] | không khác | 1 | 17 |
| RRF trọng số 1:2 | 23 | 1 / 0 | [0; +0,079] | không khác | 0 | 16 |
| Tổ hợp k = 20 + trọng số 1:2 | 23 | 1 / 0 | [0; +0,079] | không khác | 0 | 15 |
| Tổ hợp k = 20 + 50 ứng viên | 22 | 0 / 0 | [0; 0] | không khác | 0 | 14 |
| Tổ hợp trọng số 1:2 + 50 ứng viên | 24 | 2 / 0 | [0; +0,132] | không khác | 0 | 18 |
| Tổ hợp k = 20 + trọng số 1:2 + 50 ứng viên | 24 | 2 / 0 | [0; +0,132] | không khác | 0 | 18 |

Bốn tổ hợp do code tự ghép theo luật ghi trước (giá trị tốt nhất của mỗi trục ứng viên / k / trọng số, chỉ khi thắng ≥ thua và 0 câu mất đủ-đoạn-đúng). Chỉ số quyết thứ hai (tỉ lệ ý có trong 10 đoạn): cả 14 cấu hình "không khác" sau Holm
(tốt nhất 0,811 so với mốc 0,764). MRR theo từ khoá đổi trong khoảng −0,018 … +0,013.

### 4.4 Đọc kết quả
- **Theo luật ghi trước: 0 cấu hình qua** (cần 0 câu mất đủ-đoạn-đúng VÀ một chỉ số quyết "tốt hơn" sau Holm) ⇒ không mở nhóm giữ riêng, không đề nghị gì.
- Cấu hình gần nhất: DBSF trọng số 0,5 — thêm 3 câu đủ đoạn đúng, 0 câu mất; **thiếu đúng 1 câu thắng** để khoảng tin cậy của một phép so đơn lẻ rời khỏi 0, và còn xa bậc Holm (≥ 6). Nó đổi 10 đoạn của cả 18 / 18 câu ngoài kho
  ⇒ nếu sau này muốn thử lại thì lượt xác nhận có phí (câu ngoài kho + bộ an toàn) là bắt buộc.
- [quan sát] Ba cấu hình có ≥ 2 câu thắng / 0 thua đều thuộc họ "để nhánh từ khoá nhìn rộng hơn 30 ứng viên của nhánh vector" (tìm độc lập, DBSF, trọng số nghiêng từ khoá + 50 ứng viên). Căn cứ code:
  ở bản chạy nhánh từ khoá chỉ CHẤM LẠI các ứng viên của nhánh vector (`backend/retrieval/full_corpus.py:482–519`). [suy luận, chưa đo] Hướng có dư địa — nếu có — nằm ở đó chứ không ở k hay số ứng viên; nhưng cỡ lợi hôm nay
  (2–3 câu / 38) không vượt nhiễu, và Phase 8.1 đã thử cùng họ này trên kho cũ với kết quả cũng "không khác".
- So với lần dò trước (Phase 8.1 / 8.2, kho cũ): cùng kết luận. Số "đủ đoạn đúng" của mốc trên kho hôm nay 22 / 38; số cũ 24 / 40 (kho 30/10) — không so trực tiếp được vì mẫu số khác (bỏ 2 câu nhãn lệch).

## 5. Lỗi và giới hạn

- **Thước chỉ đo LẦN TÌM ĐẦU.** Trợ lý đang chạy còn tìm thêm ≤ 2 lần ⇒ lợi ở lần tìm đầu có thể đã được bù sẵn; vòng này không đo điều đó.
- **Thước phân biệt yếu** (mục 4.2): bản chạy và "chỉ vector" bằng nhau theo chỉ số quyết ⇒ "không khác" ở đây có thể là thước không đủ nhạy, không chắc là không có khác biệt. 38 câu có nhãn đều là câu KHÓ (chọn từ trước), không đại diện câu thường.
- **Nhóm dò và nhóm giữ riêng đều đã dùng nhiều lần** từ 24/10; không có bộ kín cho bước tìm. Lần này nhóm giữ riêng không bị dùng thêm.
- **Nợ: bản nhãn 6.** 6 trích dẫn đổi vị trí (2 câu nhóm dò) chưa được dời; A chốt không làm trong vòng này. Lần đo bước tìm sau nên dời trước, có người khác kiểm.
- **Thời gian tìm KHÔNG đo được đáng tin:** lượt mốc có lượt lạnh (p95 219 ms, trung vị 55 ms), các nền khác đo ở lượt sau (p95 38–85 ms); cấu hình trộn lại dùng thời gian của nền ⇒ dòng "mức tụt thời gian ≤ +20 %" của plan: **NOT RUN**
  (không ảnh hưởng kết luận vì không cấu hình nào qua).
- **Điều kiện "0 câu ngoài kho đổi kết quả" không đo được ở 0 USD** (trả lời hay từ chối do bước sinh quyết) ⇒ theo chốt của A, vòng chỉ BÁO số câu ngoài kho đổi tập 10 đoạn; con số đó không nói câu có bị trả lời hay không.
- Lệch plan: plan ước ≤ 15 cấu hình "kể cả mốc"; thực chạy mốc + 14 = 15. Lệnh bọc chạy lần đầu với hệ thật ngay trong lượt đo (không có lượt thử riêng); ba rào tự kiểm là thứ bảo vệ.
- Người viết công cụ, người chạy và người đọc bảng đều là B; A mới đọc hàm trộn có trọng số, chưa ai chạy lại kết quả.

## 6. Bàn giao cho người kiểm

- Đọc trước: 4.2 (mốc ngây thơ) rồi bảng 4.3. Chạy lại được 0 USD khi có lượt máy (~3 phút, ~1,7 GB RAM); file kết quả từ chối ghi đè ⇒ người kiểm đổi thư mục `OUT` trong công cụ hoặc dời thư mục cũ.

| Kiểm gì | Lệnh (ở gốc repo, chỉ đọc) | Phải ra |
|---|---|---|
| Không cấu hình nào được chọn | `uv run python -c "import json;d=json.load(open('data/cach_lam_2026-11-18/tu_toi_uu/ket_qua/luoi_ket_qua.json'));print(d['duoc_chon'],d['so_cau_hinh_da_chay'])"` | `[] 15` |
| Mốc và số câu có thể thắng | `uv run python -c "import json;d=json.load(open('data/cach_lam_2026-11-18/tu_toi_uu/ket_qua/moc_tom_tat.json'));print(d['du_doan_dung_o_moc'],d['cau_CO_THE_thang'],d['dau_van_tay_dev'])"` | `22 16 3f5fb40ec51a` |
| Nhóm giữ riêng không bị mở | `ls data/cach_lam_2026-11-18/tu_toi_uu/ket_qua/ \| grep -c '^test_'` | `0` |

**Cho User (lời thường):** nhóm cho máy tự thử 15 cách chỉnh bước tìm đoạn (lấy nhiều / ít ứng viên hơn, đổi cách trộn kết quả tìm theo nghĩa và theo từ khoá) trên bộ 38 câu khó có đánh dấu sẵn đoạn chứa đáp án. Bản đang chạy tìm đủ đoạn
cho 22 / 38 câu; cách tốt nhất trong lưới được 25 / 38 — hơn 3 câu, chưa đủ để chắc là hơn thật (cần ít nhất 4, và 6 khi thử nhiều cách cùng lúc). Vì vậy không đổi gì trong chatbot; tiền 0 đồng; thời gian máy khoảng 3 phút.
Giới hạn cần nhớ: phép đo này chỉ nhìn lần tìm đầu tiên và khá kém nhạy — nó cũng không phân biệt được bản đang chạy với bản "chỉ tìm theo nghĩa".
