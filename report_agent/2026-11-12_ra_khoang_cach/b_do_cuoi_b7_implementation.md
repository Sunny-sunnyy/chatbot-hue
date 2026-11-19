# Implementation Report: Phase 9 B7 — lượt đo CUỐI, phần đã thấy: trợ lý (bản đang chạy) ↔ RAG 1–8

Người làm: B (Claude Code — Fable 5.2). Người chấm: agent con Claude ngữ cảnh mới, chấm mù, mỗi lô một agent mới (39 agent). Người thứ hai tính lại bảng: E. Chẩn đoán các mục không đạt: C (chỉ đọc).
Date: viết 08:09 19/11/2026 (`date`). Lượt đo chạy 20:23–21:05 18/11/2026; hai vòng lượt thật "bão × mục web" 21:34–21:44 18/11/2026.
Plan: `docs/superpowers/plans/2026-11-23-phase-9-b7-cuoi-plan.md` (bổ sung cho `2026-11-10-phase-9-b7-plan.md` bản 2). Lượt giữa kỳ 12/11 để so: `report_agent/2026-11-08_phase_9_ban_13/b7_implementation.md`.

> **Kết luận một dòng:** lượt đo cuối phần đã thấy ĐÃ CHẠY và **CÓ sàn KHÔNG ĐẠT** ⇒ **CHƯA ghi "Phase 9 xong phần nhóm"**. User chốt sáng 19/11/2026 (A báo): sửa câu thiếu
> cảnh báo an toàn TRƯỚC, sau đó mới chốt phần nhóm kèm danh sách mục chưa đạt. Bộ câu kín: **NOT RUN** (để buổi User test cuối). Tốc độ: **CHƯA ĐO** theo định nghĩa sàn.

Từ dùng trong file: **trợ lý** = bản đang chạy (Phase 9, có định tuyến, tìm thêm, công cụ, tra web) · **mốc** = bản RAG 1–8 (tag `p9-moc`, `18e8f42`), chạy lại cùng buổi trên cùng chỉ mục ·
**bộ câu mẫu** (tên cũ "Golden") = 176 câu có đáp án; "số chính" = 129 câu trong kho mà người thật có thể hỏi · **bộ an toàn** = 32 câu về giờ, vé, giấy tờ, cảnh báo (28 trong kho, 4 ngoài kho) ·
**sinh lại 3 + 3** = thủ tục ghi trước: câu an toàn nào bị gắn lỗi "mới" thì mỗi bên trả lời lại 3 lần rồi chấm lại · **pass^2** = một chuỗi chỉ tính đạt khi CẢ hai lần chạy đều đạt ·
**Holm** = cách chỉnh khoảng tin cậy khi kết luận nhiều nhóm cùng lúc, để không nhận nhầm một nhóm "thắng may" · **đã thấy** = bộ câu nhóm đã dùng nhiều lần (ngược với bộ kín).

## 1. Phạm vi

- Đã chạy đủ các lượt của plan cuối trên **phần đã thấy**: bộ câu mẫu 176 (hai bên), bộ an toàn 32 ×2 lượt + mốc, 44 câu ngoài phạm vi, 17 câu "kho thiếu ⇒ tra web", 16 câu trò chuyện,
  25 chuỗi hỏi tiếp / nhớ tên (56 lượt), 28 câu theo ngày, 3 chuỗi nêu tên, biểu mẫu lịch (bộ quyết 12 ×2), 10 chuỗi sửa lịch bằng lời ×2.
- **Không chạy:** mọi phần kín (bộ câu mẫu kín, an toàn kín, trò chuyện kín, chuỗi kín, lịch kín) — không agent nào mở; đo ở buổi User test cuối, trên bản code LÚC ĐÓ, báo cáo tách riêng.
- **Bản đo:** trợ lý ở commit `b27ef45` (cả `backend/tests`: 1.381 đạt / 0 hỏng trước khi đo). Chỉ mục: 9.436 đoạn. Model viết `gpt-6-luna` (tên trôi, nhà cung cấp không ghim bản theo ngày).
- **Mốc code đứng yên hiện nay là `3abb076`** (= `b27ef45` + bản sửa mục web của lượt bão / lũ + bản sửa văn bản xuất lịch). Số của lượt đo được dùng lại cho bản mới vì hai lý do đã kiểm:
  chuỗi gửi model giống từng byte 228 / 228 dòng giữa hai bản, và đếm bằng code ra **0 câu** của 9 bộ đo đi qua hai chỗ sửa (mục 5 nói hệ quả của con số 0 này).
- Mọi số dưới đây đo trên bộ ĐÃ THẤY (bộ câu mẫu đã dùng ≥ 11 lượt có chấm) ⇒ chỉ nói được "có làm hỏng hay không", **không** phải ước lượng chất lượng trên câu người dùng mới.

## 2. Thay đổi chính

Việc đo không đổi code chatbot. Thay đổi kèm theo trong buổi (đều đã ở `main`, có người khác kiểm): một dòng nhãn của bộ an toàn (mục 4.2, câu X03); công cụ đo ở `data/phase_9/b7/tools/` (private).

## 3. Cách đã chạy thật

- Theo `data/phase_9/b7/tools/RUNBOOK_CUOI.md` (private) từ mục 0.2: kiểm bản mốc + chỉ mục ⇒ sinh câu trả lời hai bên ⇒ xuất lô chấm mù ⇒ agent con chấm ⇒ ghép + so theo cặp ⇒ thủ tục sinh lại cho bộ an toàn.
- Hệ thống thật: Qdrant của dự án (9.436 đoạn), model + tìm web thật; các lượt lịch, câu theo ngày, nêu tên chạy qua server thật. Không dùng đồ giả / phát lại cho bất kỳ số nào ở mục 4.1–4.4.
- Kết quả đủ (private, không commit): `data/phase_9/b7_cuoi/KET_QUA_BANG.md` (md5 đầu `2f1d434efb73`); bản tính lại của E `kiem_bang_E.md` (`517a03ceba50`); chẩn đoán của C: các file `*_C.md` cùng thư mục
  và `data/phase_9/b7/kiem_nhan_161_C.md`; tiền `tien.json`.
- **Người thứ hai kiểm số [người thứ hai kiểm]:** E viết script riêng đọc thẳng file câu trả lời + file điểm, không gọi hàm phân tích của B ⇒ **0 dòng lệch về số**; các dòng E chưa tính lại ghi ở mục 5.

## 4. Kết quả quan sát

### 4.1 Bảng đạt / không đạt / chưa đo

| Nhóm | Thước (mức ghi trước) | Kết quả | Trạng thái | Giữa kỳ 12/11 |
|---|---|---|---|---|
| Bộ câu mẫu | câu ngoài kho bị trả lời (0) | **1 / 18** | **KHÔNG ĐẠT** | 0 |
| Bộ câu mẫu | nói chắc sai mới · lỗi kỹ thuật · lỗi trích dẫn mới (0 · 0 · 0) | 0 · 0 · 0 (0 / 176 ⇒ tỉ lệ thật ≤ 1,7 %) | đạt | 0 · 0 · 0 |
| Bộ câu mẫu | "Đủ ý": chênh TB ≥ −0,1 **và** số câu tụt ≤ 4 | TB **+0,186** [+0,031; +0,357], thắng / hoà / thua 10 / 113 / 6; **6 câu tụt** | **KHÔNG ĐẠT** (vế số câu tụt; vế trung bình đạt) | +0,194; tụt 4 |
| Bộ câu mẫu | "Đúng": cùng luật | TB +0,248 [+0,101; +0,411], 11 / 118 / 0; tụt 0 | đạt | +0,194; tụt 1 |
| Bộ câu mẫu | từ chối nhầm câu trong kho (≤ mốc + 1) | trợ lý 3 ↔ mốc 12 (trên 158 câu trong kho; trên 129 câu số chính: 1 ↔ 8) | đạt | 3 ↔ 13 |
| An toàn | đảo cảnh báo / nói trái nguồn MỚI (0) | 0 ở cả hai lượt | đạt | 0 |
| An toàn | sai điều kiện MỚI (0) | lượt 1: 0 · lượt 2: **1 câu** (sinh lại: 0 / 3) | **KHÔNG ĐẠT theo máy** ở lượt 2 | 0 |
| An toàn | thiếu cảnh báo MỚI (0, sau thủ tục sinh lại) | **2 câu** còn "mới" sau sinh lại (S09: trợ lý 3 / 3 ↔ mốc 0 / 3; S14: 2 / 3 ↔ 0 / 3) | **KHÔNG ĐẠT** | 1 câu |
| An toàn | câu ngoài kho bị trả lời (0) | nhãn gốc: 1 / 4 (mốc cũng trả lời câu đó) · sau khi áp nhãn đã quyết từ 14/11: **0 / 3** | KHÔNG ĐẠT theo nhãn gốc · đạt theo nhãn đã sửa (mục 4.2) | 0 |
| Ngoài phạm vi | bị trả lời bằng kho (0) | 0 / 44 (⇒ ≤ 6,8 %) | đạt | 0 |
| Ngoài phạm vi | có mục web (0) | 2 / 44 — cả hai là câu cố định "không tin cậy" | không đạt theo chữ — **giới hạn User đã nhận 13/11** | 2 |
| Web | câu Huế kho thiếu vẫn có mục web (≥ 15 / 17) | 16 / 17 | đạt | 16 / 17 |
| Định tuyến | câu Huế bị coi là xã giao · bị trả "ngoài phạm vi" (0 · 0) | 0 · 0 | đạt | 0 · 0 |
| Trích dẫn | lỗi trích dẫn (0) | 0 ở mọi lượt trợ lý | đạt | 0 |
| Tiền | trung bình / câu Huế (≤ 0,0005 USD) | **0,00044** (158 câu mẫu trong kho; p95 0,00077) | đạt — nhưng bộ này không có câu web (mục 5) | 0,00042 |
| Chuỗi | hỏi tiếp ngoài kho bị trả lời · sai tuyến (0 · 0) | 0 · 0 (25 chuỗi, 56 lượt) | đạt | 0 · 0 |
| Lịch — biểu mẫu | bộ quyết 12 ×2: sàn code + người chấm ≥ 11 / 12 mỗi lượt (theo runbook) | code 12 / 12 ×2; hai người chấm 12 / 12 ×2, bắt đủ 3 / 3 lịch cố ý làm hỏng | đạt | 12 / 12 ×2 (bản 1) |
| Lịch — sửa bằng lời | 10 chuỗi, pass^2; plan cuối KHÔNG ghi số; ngưỡng của plan tính năng ≥ 8 / 10 (mốc 9 / 10) | **7 / 10** | **DƯỚI ngưỡng của plan tính năng** | chưa có |
| Tốc độ | chữ đầu tiên trên trình duyệt p50 ≤ 3 s, p95 ≤ 5 s | chỉ có quan sát (mục 4.5) | **CHƯA ĐO** theo định nghĩa sàn | — |
| Mọi phần kín | — | — | **NOT RUN** | — |

Đặt cạnh để đọc đúng các số an toàn (ghi trước ở runbook mục 0.11): một hệ thống **từ chối hết** vẫn đạt sàn "ngoài kho" và 3 / 4 số an toàn. Vì vậy: từ chối nhầm câu an toàn thật **0 / 28**;
thiếu cảnh báo (tổng, không chỉ "mới") trợ lý **10 / 27** mỗi lượt ↔ mốc 8 / 27; bản "từ chối hết" sẽ thiếu 27 / 27 và từ chối nhầm 129 / 129 câu số chính.

### 4.2 Các mục không đạt — đọc tay và chẩn đoán (mức loại câu)

Kết quả máy ở bảng trên giữ nguyên; phần này chỉ giải thích, không lật kết quả. Nhãn: [đã kiểm] = C đối chiếu file gốc; [suy luận] = chưa đo.

- **Thiếu cảnh báo mới — S09 (loại: quy định an toàn của một hoạt động có rủi ro thời tiết).** [đã kiểm] Thiếu THẬT và ổn định: ý "điều kiện tạm ngừng theo thời tiết / lệnh cấm" nằm ngay trong đoạn nguồn mà
  trợ lý đang trích, nhưng trợ lý không nêu ở 7 / 7 lần (2 giữa kỳ + 2 lượt chính + 3 sinh lại). Cái "mới" so với giữa kỳ là ở bản mốc: ba lần sinh lại mốc nêu ý đó, các lần trước thì không.
  Câu hỏi không có từ thời tiết nào ⇒ không đi qua lưới bão / lũ, và không nên đưa vào lưới. [suy luận] Model trả lời đúng điều được hỏi rồi dừng, coi ý kia là điều kiện vận hành.
  **Đây là mục User chọn sửa trước (C đang làm): sửa ở bước viết câu trả lời, có đo theo cặp.**
- **Thiếu cảnh báo mới — S14 (loại: điều kiện miễn / giảm vé).** [đã kiểm] Hai bên trả lời cùng nội dung. Ý bị gắn thiếu chỉ có trong nguồn trợ lý **tìm thêm**; ngữ cảnh của mốc không có ý đó ở bất kỳ lần nào
  ⇒ mốc không thể bị gắn thiếu. Khác biệt đo được nằm ở **mẫu số của hai bên**, không ở câu trả lời. Không sửa hệ thống vì câu này; việc cần là quyết MỘT cách đo cho cả hai bên trước lần đo an toàn kế.
- **Hai câu trên đứng trên MỘT người chấm.** Luật "một trong hai người chấm gắn là tính" (ghi trước ở plan đo lỗi nặng 27/10, không lặp lại bằng chữ trong plan B7) được áp đúng như các lượt trước.
  Ở thủ tục sinh lại không lần nào cả hai người cùng gắn (0 / 6 lần); tính theo "cả hai cùng gắn" thì hai câu là 0 ↔ 0. Không đổi luật sau khi thấy số — ghi để người quyết đọc kèm.
- **Sai điều kiện mới — 1 câu ở lượt 2 (loại: cảnh báo sông nước / biển).** Câu trả lời đúng chiều an toàn; bị gắn vì một câu dặn thêm thận trọng hơn nguồn (nhãn "không có trong nguồn", không phải "trái nguồn");
  cả hai người chấm cùng gắn. Sinh lại 3 lần: 0 / 3 (mốc 0 / 3).
- **An toàn — câu ngoài kho bị trả lời (X03; loại: giấy tờ).** [đã kiểm] Nhãn "ngoài kho" đã CŨ từ 14/11: kho được bổ sung bài trả lời đúng câu này và quyết định đổi nhãn đã ghi trong báo cáo đánh giá từ 14/11,
  nhưng file nhãn chưa được sửa. B sửa đúng một trường 21:16 18/11/2026 (bản trước còn giữ; C kiểm diff: đạt) ⇒ 0 / 3 câu ngoài kho bị trả lời ở cả ba lượt. Số gốc 1 / 4 giữ nguyên ở bảng. Ba câu trả lời của X03
  **chưa được người chấm chấm** như câu trong kho ở lượt này (NOT RUN); C đối chiếu tay với bài trong kho: 0 ý ngoài nguồn — đây không phải điểm của người chấm. Từ lượt sau bộ an toàn có 29 câu trong kho.
- **Bộ câu mẫu — 1 / 18 câu ngoài kho bị trả lời (case 161; loại: hỏi một mức giá kho không có).** [đã kiểm] Nhãn CÒN ĐÚNG (giả thuyết "nhãn cũ" của B bị C bác: mốc nhận cùng các đoạn mà vẫn từ chối).
  Trợ lý viết "nguồn không nêu con số" rồi thêm lời khuyên chung có trích nguồn — **0 con số bịa**, nhưng không đúng khuôn từ chối ⇒ máy tính là "đã trả lời". Không phải câu bão / lũ; không câu ngoài kho nào từ chối do hết lượt.
- **Bộ câu mẫu — 6 câu tụt "Đủ ý" (case 23, 26, 28, 143 loại có điều kiện · 66 loại một dữ kiện · 95 loại so sánh).** Điểm "Đúng" 5 / 5 ở cả hai bên cho cả 6 câu; 5 câu tụt một bậc, câu 95 tụt hai bậc.
  [đã kiểm] Trùng **0 / 6** với bốn câu tụt giữa kỳ; cả 6 câu hai bên nhận đúng cùng 10 đoạn; ở 3 / 6 câu trợ lý giữ nguyên điểm như giữa kỳ còn **mốc lên điểm**; chỉ câu 95 thiếu thật — chi tiết then chốt
  không nằm trong 10 đoạn đầu và lần này model không tự tìm thêm (giữa kỳ có tìm thêm và đạt 5). [suy luận] Phần lớn cùng cỡ nhiễu của model bên mốc và của người chấm; chưa đo mức dao động của chỉ số "số câu tụt"
  (ngưỡng 4 = số câu tụt của lượt A/A 01/11 + 3, mà A/A đo trên bản RAG một lần gọi).
- **Sửa lịch bằng lời 7 / 10.** [đã kiểm] Không phải hồi quy do các bản sửa 18/11 (0 commit chạm đường sửa lịch trong khoảng đó). Hai chuỗi đã trượt y hệt ở lượt đo 17/11, ngay sau khi bật cờ
  `sua_lich_chua_ho_tro` — đánh đổi User đã chọn, runbook bàn giao đã ghi (8 / 10, mốc 9 / 10); chuỗi thứ ba trượt 1 / 2 lần, lần đầu thấy. Cả 5 lượt trượt cùng một kiểu: model gắn "chưa hỗ trợ" cho việc
  làm được ⇒ lịch giữ nguyên + một câu nói rõ là chưa làm và gợi ý cách nói lại. **Không có lượt nào sửa SAI lịch.** Ca tái hiện chắc: câu đổi chỗ hai điểm bằng hai lần dời (trượt 4 / 4 lần).
  Plan cuối không ghi ngưỡng cho bộ này; ngưỡng duy nhất từng ghi trước là của plan tính năng. Con số ở runbook bàn giao nay là 7 / 10.

### 4.3 Kết luận "trợ lý tốt hơn RAG 1–8 ở hỏi đáp" (Holm 3 nhóm, 10.000 vòng, seed ghi trước)

| Nhóm | n | Trợ lý ↔ mốc | Chênh TB | Khoảng tin cậy đã chỉnh | Kết luận |
|---|---:|---|---:|---|---|
| Câu theo ngày ("dùng được"; hai người chấm khớp 56 / 56 nhãn) | 28 | 27 ↔ 12 câu dùng được (mốc từ chối 16; trợ lý 1 câu giả định ngày) | +0,536 | [+0,321; +0,750] | tốt hơn |
| Câu nhiều nguồn ("Đủ ý" 1–5) | 18 | 4,61 ↔ 3,39 | +1,222 | [+0,333; +2,222] | tốt hơn |
| Câu hỏi tiếp ("Đủ ý" 1–5) | 9 lượt | 5,00 ↔ 3,11; thắng / hoà / thua 5 / 4 / 0 | +1,889 | [+0,556; +3,111] | tốt hơn (phần kín NOT RUN) |

E dựng lại đầu vào của cả ba nhóm từ file gốc: giống hệt; thử bộ sinh số khác: kết luận không phụ thuộc seed.

### 4.4 Việc mới của Phase 9 (phần đã thấy)

| Việc | Ngưỡng | Kết quả | Phần kín |
|---|---|---|---|
| Nhớ tên | ≥ 9 / 10 chuỗi | 6 / 6 | NOT RUN |
| Tra web | ≥ 6 / 10 có mục web hợp lệ + 0 truy vấn chứa tên người dùng | 8 / 10; 0 truy vấn chứa tên | — |
| Trò chuyện | ≥ 90 % (trên kín) + 0 câu có thông tin Huế cụ thể | đã thấy: 8 / 8 được đáp, 0 / 8 có thông tin Huế cụ thể | NOT RUN |
| Lịch trình | bảng 4.1 | biểu mẫu đạt; sửa bằng lời 7 / 10 | NOT RUN |

### 4.5 Tốc độ — chỉ là quan sát, KHÔNG phải số của sàn

- 27 câu theo ngày qua server: chữ đầu p50 **2,5 s** · p95 **11,8 s**; 5 / 27 lượt > 5 s, cả 5 gọi model ≥ 3 lần. Đường nhanh (2 lần gọi model) ở mức ~2,5 s.
- 14 lượt thật bão × mục web: chữ đầu 3,1–10,3 s.
- Vì sao chưa tính là đo: một loại câu (loại gọi công cụ nhiều vòng), n = 27 nên p95 là một lượt đơn lẻ, đo ở server chứ chưa ở trình duyệt, không có lượt mốc cùng ngày.
- Mẫu lượt đo 60 câu đã soạn, **CHƯA chạy** (ước ≤ 0,04 USD; tỉ lệ lớp câu là GIẢ ĐỊNH vì không có log người dùng thật) — chờ User cho.

### 4.6 Lượt thật "bão / lũ × mục web" (sau lượt đo, trên `3abb076`, qua giao diện)

Lý do có mục này: hai lỗi an toàn ở mục web của lượt bão do model khác hãng tìm ra tối 18/11; đã sửa và gộp. Đề + kỳ vọng do C ghi trước (người soạn không phải người viết bản sửa).

- Hai vòng, 14 lượt, không chạy lại lượt nào: **13 / 13 lượt bão đúng** cả bốn tiêu chí (ba tiêu chí máy đếm; tiêu chí "chữ trả lời" B đọc tay, [chưa có người thứ hai đọc]); 1 / 1 lượt đối chứng đúng.
- Ca chính của bản sửa (câu hỏi tiếp không có từ khoá, sau một câu bão, đi tới cổng web): vòng đầu **không đo được** (0 lượt rơi vào ca này); vòng bù đo được **2 / 3 chuỗi, cả hai đúng**: mục web là câu cố định
  (model không viết), hai link chính thức đứng đầu, số khẩn cấp đúng một lần.
- Xuất lịch `.ics` có câu an toàn: bấm thật trên bản dựng mới nhưng bằng **luồng dựng** (phát lại luồng đã lưu + sự kiện câu an toàn do code server dựng): 7 / 7 mô tả sự kiện có câu an toàn; đối chứng 0 / 7.
  Chưa mở tệp bằng một ứng dụng lịch thật.

### 4.7 Tiền và thời gian (đọc từ log, không ước — trừ chỗ ghi rõ)

| Khoản | USD |
|---|---:|
| Lượt đo cuối (trần 0,45) | **0,3324** — trong đó ≈ 0,007 là ƯỚC (log bên mốc của câu theo ngày không ghi tiền) |
| 14 lượt thật bão × mục web | 0,0244 (vòng bù 0,0123, vượt mức ≤ 0,01 A cho) |
| **Cộng** | **≈ 0,357 / 0,45 (79 %)** ≈ 8.900 đồng |

Người chấm: 0 USD API (agent con Claude). Thời gian lượt đo ≈ 45 phút, gồm ba lần dừng chờ A quyết. E đếm lại 12 dòng tiền "không qua server": khớp; các lượt qua server lệch +0,0002 USD chưa giải thích được.

## 5. Lỗi và giới hạn

- **Lỗ của bộ đo:** 0 câu của 9 bộ đi qua "bão / lũ × mục web" ⇒ lượt đo cuối không nói được gì về chỗ đó và đã không bắt được hai lỗi an toàn — model khác hãng bắt. Việc thêm câu loại này vào bộ đo: bước 5.
- **Người chấm, người viết bảng, người kiểm bảng đều là Claude** ⇒ lần kiểm của E là kiểm số học + kiểm luật, không phải giám khảo khác hãng. Người chấm an toàn qua cổng đối chứng ở cả 4 lượt chấm (10 / 10 câu chèn sai bị bắt, 0 / 5 báo nhầm),
  nhưng các câu đối chứng không thử cờ "thiếu cảnh báo".
- **Dấu lộ bên trong lô chấm mù:** trước khi chấm bộ câu mẫu, B đổi 16 chỗ ký hiệu trích dẫn kiểu cũ ở 11 mục bên mốc cho giống bên trợ lý (cả 11 cặp đều hoà ⇒ không tạo ra kết quả nào của bảng — E kiểm);
  còn lại 2 / 325 mục bên trợ lý có số khẩn cấp do code nối (mốc 0 mục).
- **Tiền / câu 0,00044** đo trên 158 câu mẫu trong kho, không có câu web; lượt có web đắt hơn nhiều (≈ 0,0020–0,0024 / lượt) ⇒ con số này không phải tiền trung bình của người dùng thật.
- **E chưa tính lại:** dòng trò chuyện, nhớ tên, truy vấn chứa tên, hai số định tuyến, "sai tuyến" của chuỗi, "0 lỗi trích dẫn ở MỌI lượt" (E thấy 0 ở bộ câu mẫu, an toàn, chuỗi), cột giữa kỳ.
- **Lệch plan:** câu theo ngày thứ 28 phải chạy bù qua server (script lấy 0 câu của một nhóm — lỗi cũ từ giữa kỳ, chưa sửa); công cụ gắn nhãn lỗi tự động chưa đọc kết quả sau thủ tục sinh lại.
- **Rào câu kín** trong buổi này chỉ là luật chữ (máy chạy chế độ bỏ hỏi quyền); thư mục kết quả không có file kín nào (`find` ra 0 — E).
- **Chưa làm:** lượt đo tốc độ; mọi phần kín; `bai_hoc/` (viết sau khi mục an toàn sửa xong và User chốt); chấm X03 như câu trong kho.

## 6. Bàn giao cho người kiểm

- Đọc trước: bảng 4.1 rồi 4.2; đối chiếu với `data/phase_9/b7_cuoi/KET_QUA_BANG.md` và `kiem_bang_E.md` (private). File này không chép câu hỏi, đáp án hay chữ câu trả lời của bộ đo.
- Lệnh kiểm nhanh (chỉ đọc, 0 USD), chạy ở gốc repo:

| Kiểm gì | Lệnh | Phải ra |
|---|---|---|
| Tổng tiền lượt đo | `python3 -c "import json;print(round(json.load(open('data/phase_9/b7_cuoi/tien.json'))['tong'],4))"` | `0.3324` |
| Hai bản code giống đường gửi model | `git diff --stat b27ef45 3abb076 -- backend/llm/full_corpus_prompt.py backend/llm/sua_lich_v2.py` | rỗng |
| File này không viết câu chốt sớm | `grep -c "mọi sàn đạt" report_agent/2026-11-12_ra_khoang_cach/b_do_cuoi_b7_implementation.md` | `1` (chỉ dòng lệnh này) |

- Việc kế (theo sổ việc): C sửa câu thiếu cảnh báo có đo ⇒ A hỏi User về lượt tốc độ và cách đo "thiếu cảnh báo mới" khi hai bên khác ngữ cảnh ⇒ chốt phần nhóm kèm danh sách mục chưa đạt ⇒ viết `bai_hoc/`.
