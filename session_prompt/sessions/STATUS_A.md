# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 18:17 28/11/2026 (giờ `date`) — **KẾT PHIÊN SẠCH SAU ĐỢT 6 (`76f65ff3`, `64662130`, `71 MỞ / 9 TẮT`) · ĐÃ NHẬN & TÁI HIỆN 0Đ REVIEW GPT 6.2 SOL · CHUYỂN ĐỢT 7 SANG PHIÊN MỚI NGỮ CẢNH SẠCH.**

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất Đợt 5A, Đợt 6 (`76f65ff3`), đồng bộ giáo trình Đợt 6 (`64662130`, `27` file), và phát hành đề bài cho GPT 6.2 Sol.
- Sau khi Hiếu gửi kết quả `/home/minhhieu/hue_rag/gửi chatgpt/2026-11-28/KET_QUA_6_2_SOL.md`, A đã kiểm toán 0đ 19 vai `gpt-6-luna`, tái hiện độc lập `0 USD` các lỗi tích hợp `P0, P1, P2, P4, P9, P10`, ghi nhận 4 nguyên tắc Hiếu chốt lúc `18:15` vào `VIEC_DANG_MO.md` mục `A.1d` và `HIEN_TRANG.md` mục 4, rồi thực hiện kết phiên sạch để phiên mới ngữ cảnh sạch triển khai Đợt 7.

## 2. Đã xong trong đợt sáng–chiều 28/11 (`0 USD` AWS, `0,466975 USD` OpenAI = `0,120794` Đợt 5A + `0,346181` Đợt 6)
- **Đợt 6 (`76f65ff3` + `64662130`, `0,346181 USD`):** `6.1` đo & giữ `mac_dinh` (`55/55` bảng ảnh mẫu) · `6.2` soi 176 Golden (`BAO_CAO_LOI_GOLDEN_176.md`) + vá `vl_01` + giữ RRF (`92,04%` vs `dense_only` `90,45%`) · `6.3a` đo & giữ tắt `tinh_ve_tham_quan: false` · `6.3b` dựng & bật `goi_y_luu_tru: true` (`9/10` dương, `6/6` âm, `F1=0,875`) · `6.4` SSE trạng thái & 2 nút PPTX đạt Playwright desktop/mobile ở cả `use_llm: true/false` · kiểm `387 passed` (`134` offline + `253` Qdrant) + `frontend` build + đồng bộ `27` file giáo trình (`b7d65994`).
- **Tiếp nhận & kiểm chứng `KET_QUA_6_2_SOL.md` (`0 USD`):** tái hiện thật `P0, P1, P2, P4, P9, P10`, xác nhận `/usr/bin/tesseract` có sẵn, kiểm toán token/cache/reasoning 19 vai `gpt-6-luna`, mở mục `A.1d` Đợt 7 cho phiên mới.
- **Đợt 5 — Phần A (`c493cdc1`, `45 + 4 + 95 passed`):** `CanonicalItinerary`, `.ics` v2 (`191/191`), Deep Link OTA 3 sàn + mẫu hỏi phòng (`15/15`, rào `12/12`), `.pptx` v2 (`p95=0,358s`, `0 USD`) & `Slide Designer Agent` (`gpt-6-luna`, `use_llm: true` local, `dong_goi.sh` ép `false`).
- **Nghiên cứu `google-research/harness2` (`0 USD`):** `/home/minhhieu/hue_rag/data/nghien_cuu_2026-11-28/HARNESS2_PHAN_TICH.md` (đã xoá `/tmp/hr_eval_harness2`).
- **Giáo trình (`6b01170b`, `64662130`, `0 USD`):** đã cập nhật đủ tới Đợt 6 (`A 199 · B 149 · C 272 · E 240 · F 212 · G 359 · H 215 · I 227`).
- **Kết phiên trưa & chiều 28/11:** lưu trữ lịch sử vào `session_prompt/archive/*_LICH_SU_2026-11-28.md`, khoá chuẩn `--squash` ở `WORKFLOW.md` §9.6, đóng hẳn Đợt 5B & Cloud Vision API, ghi nhận nguyên tắc Đợt 7.

## 3. Việc gác lại & chuyển phiên sau
- **Đợt 5 — Phần B (Google OAuth) & Google Cloud Vision API:** **ĐÃ ĐÓNG HẲN 28/11/2026** (không mở lại).
- **Đợt 7 (`VIEC_DANG_MO.md` mục `A.1d`):** chuyển sang phiên mới ngữ cảnh sạch (nghiên cứu chuẩn `11/2026` cho `GPT-6`/`gpt-6-luna`, thảo luận với Hiếu, sửa lỗi 6.2 Sol + tối ưu prompt/ảnh 0 GPU).
- **Deploy AWS thật (`deploy/`):** gác chờ sau khi xong toàn bộ local.

## 4. Tài nguyên & Chi phí lúc kết phiên
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, `"points_count":9540`.
- **Cổng tạm / worktree / `/swarm`:** `git worktree list` chỉ có `/home/minhhieu/hue_rag` (`[main]`), `NO_TMP_HR`, `NO_TEMP_PORTS`; đã đóng `builder`, `docs`, `eval`, `verifier`.
- **Chi phí OpenAI lũy kế phần test của nhóm:** ~**1,82 USD** (`~1,47` tới Đợt 5A + `0,346181` Đợt 6).

## 5. Bẫy phiên này
- **Tra cứu web thiếu mốc thời gian:** truy vấn không gắn mốc `11/2026` và dòng `gpt-6-luna` / `GPT-6` dễ kéo phải tài liệu cũ thời `GPT-5`/`5.6` bị Hiếu nhắc thẳng ⇒ phiên sau bắt buộc gắn mốc `11/2026` và kiểm nguồn đúng thế hệ `GPT-6`.
- **Sandbox runner phiên này:** `run_command` sandbox chuẩn hay báo `fork/exec .../agy.*.old: no such file or directory`; giữ đúng quy tắc thử sandbox trước rồi chạy lại với `BypassSandbox: true` và giữ nguyên `toolSummary`.
