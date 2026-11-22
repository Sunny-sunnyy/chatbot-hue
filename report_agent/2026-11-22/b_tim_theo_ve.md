# Tin nhiều ý: lần tìm kho đầu tìm thêm theo từng vế hỏi (công tắc `tim_theo_ve`, đang TẮT)

Viết 09:45 22/11/2026 (giờ `date`), phiên B. Nhánh `p9-b-tim-theo-ve`. Việc: sổ việc khối A, nhánh chờ số 3 (S2). Chưa ai đọc lại.

**Từ dùng:** *tin nhiều ý* = tin mà bộ đếm của code thấy từ hai vế hỏi; trợ lý trả lời theo từng ý, ý kho không có thì ghi dòng "Tư liệu chưa có thông tin về: …" · *đoạn* = một mẩu của bài kho đã được cắt sẵn; mỗi lượt trợ lý đọc 10 đoạn tìm được · *vế hỏi* = một câu hỏi con trong tin · *dòng "chưa có" SAI* = trợ lý ghi là chưa có trong khi kho có.

## 1. Vì sao làm
Đếm tối 21/11 trên ba lượt mốc: ở tin nhiều ý, model đang chạy ghi dòng "chưa có" ở 86 % số lượt, khoảng một phần tư tới một phần ba số dòng đó là SAI. Nguyên nhân: lần tìm kho đầu dùng nguyên cả tin làm một câu tìm ⇒ 10 đoạn tìm được dồn về vế chính, vế phụ không có đoạn nào.

## 2. Đổi gì (chỉ khi công tắc bật VÀ tin là tin nhiều ý)
- 10 đoạn tìm bằng cả tin giữ NGUYÊN (chữ, thứ tự, số nguồn). Code tìm thêm riêng từng vế hỏi (nhiều nhất 6 vế), lấy 2 đoạn đầu của mỗi vế, đoạn nào chưa có thì nối SAU, đánh số tiếp. Không gọi model, không đổi lời dặn.
- Tin một ý, công tắc tắt, hoặc câu tìm do bước định tuyến viết ⇒ thứ gửi model y như cũ.
- Vế để TÌM được tách rộng hơn luật đếm "tin nhiều ý" (cắt cả ở dấu chấm, nhận từ hỏi gõ tắt "ko", "bn", "j") — luật đếm không đổi. Lý do có số: tách như luật đếm chỉ đưa đoạn đúng vào ngữ cảnh 3 / 8, tách rộng 5 / 8 (mốc tắt 1 / 8).
- Bản được giao ban đầu là "4 đoạn cả tin + 2 đoạn mỗi vế, trần 12": KHÔNG làm vì nó bỏ khoảng 6 / 10 đoạn đang có (đếm: làm mất đoạn đang có ở 3 / 13 tin của một vai) — phiên điều phối đồng ý đổi.
- File: `backend/llm/assistant.py` (`search_into_trace` thêm tham số `ve_them`; `cac_ve_tim`; một dòng ở `_before_model`), `backend/config/settings.yaml` (dòng công tắc, false), `backend/tests/test_tim_theo_ve.py`.

## 3. Bằng chứng

**Đếm không gọi model, qua chính code sản phẩm [máy kiểm]** (`data/thu_bedrock_2026-11-21/b_buoc_4/chua_co/s2_dem_code_that.py`): 8 dòng "chưa có" SAI đã dò kho — đoạn chứa dữ kiện vào ngữ cảnh 1 / 8 ⇒ 5 / 8 · 65 tin nhiều ý: phần ngữ cảnh cũ giữ nguyên từng ký tự ở 65 / 65 · thêm trung vị 6 đoạn (nhiều nhất 10) · thời gian tìm 36 ⇒ 143 mili giây.

**Test (tìm kho thật, model dựng sẵn) [máy kiểm]:** `tests/test_tim_theo_ve.py` 7 passed — tin một ý không đổi gì; phần cũ giữ nguyên + đoạn mới đánh số tiếp, trích dẫn được; đường stream song song (đường người dùng đi) chạy được với công tắc bật. Tắt tính năng trong code ⇒ 4 ca đỏ (đã thấy). Bốn file lân cận (`test_cau_nhieu_y`, `test_web_chi_khi_tu_choi`, `test_b2_tool_loop`, `test_toc_do_song_song`): 44 · 13 · 12 · 10 passed.

**Lượt thật, model đang chạy, công tắc tắt ↔ bật xen kẽ từng tin, tiêu chí ghi trước [máy kiểm + người viết đọc tay; chưa có người thứ hai]:**

| Tiêu chí | Kết quả |
|---|---|
| Sàn: 4 tin ngoài phạm vi bị từ chối · tin bão lũ có số 112 · lỗi bên bật không nhiều hơn | Đạt: 4 / 4 ↔ 4 / 4 · 1 / 1 ↔ 1 / 1 · lỗi tắt 3 ↔ bật 2 (mọi lỗi là "model không trích nguồn nên câu trả lời bị rút", có ở cả hai bên, 3 / 5 lần ở cùng một tin) |
| Chỉ số quyết — 8 tin có sẵn đáp án kho-có, ba lượt: số lượt-tin trợ lý NÊU ĐƯỢC dữ kiện đó | tắt 3 / 24 ⇒ bật 15 / 24. Lượt đầu riêng nó chưa rõ (hơn 2 tin trên 6 cặp sạch) nên chạy thêm hai lượt theo luật ghi trước (ngưỡng: chênh ≥ 6 / 24) |
| — trong đó tin "ai nối ngôi vua Tự Đức" | 0 / 3 ⇒ 3 / 3 (bên tắt ghi "chưa có", sai) |
| — hai tin "quán ăn trưa gần Đại Nội: tên, địa chỉ, giờ mở" | bên bật 6 / 6 nêu một quán đủ địa chỉ + giờ mở từ đoạn nối thêm; bên tắt nêu vài quán nhờ công cụ "gần một điểm" nhưng phần lớn thiếu địa chỉ / giờ mở ⇒ lợi ở đây là "đủ hơn", không phải "từ không thành có". Bỏ hai tin này: tắt 3 ⇒ bật 9 trên 18 |
| — hai tin không đổi | 0 / 6 ↔ 0 / 6: đúng như phép đếm — đoạn kho của chúng không vào ngữ cảnh ở cả hai bên |
| Không làm hỏng: 6 tin khác, đọc tay từng cặp | không thấy dữ kiện đang đúng bị mất vì ngữ cảnh mới |
| Thời gian trung vị | 13,85 ⇒ 14,6 giây (+0,75) |
| Ghi nhận | đoạn trong ngữ cảnh 10 ⇒ 15; lời gọi model mỗi lượt 4 ⇒ 3 (model tự tìm thêm ít hơn) |

72 lượt gọi qua đường chat thật, 4,02 USD Bedrock, 09:22–09:41. Hồ sơ riêng tư: `data/thu_bedrock_2026-11-21/b_buoc_4/chua_co/S2_TIEU_CHI.md`, `s2_luot_1/KET_QUA.md`.

Lệch so với tiêu chí ghi trước, nói rõ: chuỗi đáp án ghi sẵn khớp nhầm một tin và sót một tin ở lượt 1 ⇒ từ đó dùng mẫu chặt hơn + đọc tay; không lường công cụ "gần một điểm" mở cùng ngày làm bên tắt khá hơn mốc tối 21/11 ở hai tin.

## 4. Kết luận và đề nghị
Theo luật ghi trước: sàn đạt, chỉ số quyết đạt sau ba lượt, không mất dữ kiện ⇒ **đề nghị mở**. Phiên điều phối quyết; lùi = một dòng cấu hình. Chưa mở trong nhánh này.

## 5. Chưa làm · giới hạn
- Chưa có phiên khác đọc code; chưa nhìn trình duyệt (không có chữ / khuôn giao diện mới).
- Tin gửi như tin đầu cuộc — lượt giữa cuộc có lịch sử chưa đo. Model cũ chưa đo (đang gác).
- Vế tách ra hay mất tên nơi ("có bậc nhiều không?") ⇒ 2 đoạn của vế đó có thể là đoạn không liên quan (thừa, không sai).
- Câu GOM nhiều bài ("lăng nào ít leo bậc") không được cứu: đếm 13 tin, đoạn bậc của một bài lăng vào ngữ cảnh 0 ⇒ 1 tin.
- Một tin (hỏi năm tháng + tổng vé + điểm ít bậc trong cùng một tin) hay làm model viết câu trả lời không trích nguồn ⇒ bị rút: 3 / 6 lượt, ở cả hai bên — có sẵn, không do việc này.

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm + đầu ra |
|---|---|---|---|
| code sau công tắc tắt · 7 test · đếm bằng code thật · lượt thật ba lượt nhóm chính | người thứ hai đọc · lượt giữa cuộc · model cũ | hàng runbook + mục bài học: viết khi phiên điều phối quyết mở (chưa mở thì người dùng chưa thấy gì khác) | `cd backend && HF_HUB_OFFLINE=1 uv run pytest tests/test_tim_theo_ve.py -q` ⇒ `7 passed` · `python3 data/thu_bedrock_2026-11-21/tools/b_do_tim_theo_ve.py bang data/thu_bedrock_2026-11-21/b_buoc_4/chua_co/s2_luot_1` ⇒ dòng nhóm K: tắt 5 / 24 ↔ bật 16 / 24 theo chuỗi đáp án gốc |

Phép này KHÔNG cho biết: trên tin thật của người dùng, bao nhiêu dòng "chưa có" là sai và bao nhiêu trong đó tìm theo vế gỡ được · hướng rộng hơn: hai tin không đổi cho thấy phần còn lại nằm ở chỗ đoạn kho đúng không đứng trong 2 đoạn đầu của vế — để model tự tìm thêm theo vế (nó đã tự làm ở một tin) hoặc lấy 3 đoạn mỗi vế là bước kế rẻ; và lỗi "không trích nguồn ⇒ rút cả câu" đáng một phép đếm riêng vì nó xoá cả lượt · đếm rẻ nhất: đếm trong sổ lượt thật số lượt bị rút vì không trích nguồn (0 đồng).
