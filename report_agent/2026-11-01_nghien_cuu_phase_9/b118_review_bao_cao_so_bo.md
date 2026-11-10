# B118 — review bản sơ bộ `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` (bản 1)

B, 15:26 01/11/2026 (`date`). Việc: A nhờ qua tin nhắn (B118). Người viết: A. B không sửa file của A.

**Căn cứ:**
- `data/nghien_cuu_phase_9_2026-11-01/{b_mach1,b_mach2,c_mach3,c_mach4}.md`;
- `session_prompt/Session_Prompt.md:176` (BM25 chỉ chấm lại 30 đoạn dense);
- lần WebFetch Huế TRIPO của chính B trong B117.

**Bản được review:** file untracked, 68 dòng, dòng 3 ghi "15:25 01/11/2026 — bản 1".

**Kiểm đã chạy:**
- đối chiếu từng nhãn `[đã kiểm]` / `[B kiểm]` / `[C kiểm]` với cột "Nhãn" của 4 file căn cứ;
- `uv run python .githooks/overlap_scan.py <file>` ⇒ **0 trùng** với Golden / kho / câu kín [Chạy];
- grep tên dự án khác (mẫu của hook) ⇒ 0.

**Kết luận: `changes_requested`** — 0 blocker · 3 major · 5 minor. Sửa nhỏ, chủ yếu tách phần tự khai / suy ra ra khỏi nhãn "đã kiểm".

## Major

**M-1 — ý tự khai nằm dưới nhãn `[C kiểm]` (dòng 20–21).**
- Báo cáo ghi: "các bài sau đều kiểm ràng buộc bằng dữ liệu có cấu trúc / code, LLM chỉ diễn giải. [C kiểm]".
- Căn cứ: `c_mach3.md:28` — các bài sau TravelPlanner là "TripScore tên: đã kiểm; còn lại tự khai"; câu "đều kiểm ràng buộc…" là phần **suy ra** của C (`c_mach3.md:44`). Chỉ "GPT-4 0,6 %" là đã kiểm (`c_mach3.md:27`).
- **Đóng khi:** nhãn `[C kiểm]` chỉ gắn cho 0,6 %; vế "các bài sau…" ghi "(tự khai / suy ra, chưa kiểm)" hoặc bỏ.

**M-2 — "câu nhiều nguồn ⇒ tách câu con" nằm dưới `[C kiểm]` (dòng 22–24).**
- Căn cứ: `c_mach4.md:30, :43` — LlamaIndex Sub Question là "API + tự khai"; "Câu nhiều nguồn: … (tự khai)". Hai mẫu kia đã kiểm thật: danh sách trường (`trip-advisor-agent`, `:20`) và tính tiền bằng code (`KhaiBoiPho`, `:23`).
- **Đóng khi:** vế tách câu con ghi tự khai, hoặc chuyển ra khỏi câu có nhãn `[C kiểm]`.

**M-3 — "đúng cách hue_rag đang chạy" nói quá (dòng 25–26).**
- Bài EACL 2026 đo **trộn tuyến tính BM25 + dense** độc lập, trọng số dense ≈ 0,7, và **không đo e5-small, không có lĩnh vực du lịch** (`c_mach3.md:31, :48` — C ghi rõ "không suy ra được e5-small kém hay tốt").
- hue_rag thì dùng RRF, và BM25 chỉ chấm lại 30 đoạn dense (`Session_Prompt.md:176`) ⇒ cùng **hướng lai**, khác cách trộn.
- Câu đứng ở Tóm tắt, dễ được trích như "paper xác nhận thiết kế hue_rag".
- **Đóng khi:** viết lại kiểu "cùng hướng lai (hue_rag: RRF trên 30 đoạn dense); bài không đo e5-small và không có du lịch".

## Minor

**m-1 — số bảo tàng sai phạm vi mẫu (dòng 14–15; bảng dòng 46 "người dùng ít tự kiểm").**
- 61 % / 27 % là trong **người dùng AI, n = 212**, không phải n = 395 (`b_mach2.md:36`).
- Mẫu Prolific nghiêng về người rành AI; tác giả là hãng làm phần mềm hướng dẫn bảo tàng.
- Bảng dòng 46 khái quát thành "người dùng ít tự kiểm" ⇒ nên ghi "khách bảo tàng dùng AI".
- Cùng loại lỗi phạm vi như số 8 % A vừa nhắc B sửa.

**m-2 — thiếu cờ "nguồn có lợi ích" (dòng 12–15).**
- Expedia, Agoda, Musa Guide đều là hãng tự khảo sát thị trường mình bán; Agoda **không nêu cỡ mẫu** (`b_mach2.md:34–36`).
- Một cụm "(khảo sát của chính các hãng; Agoda không nêu cỡ mẫu)" là đủ.

**m-3 — Huế TRIPO tả hơi quá so với lần B mở trang (dòng 9–10).**
- B thấy biểu mẫu có người lớn / trẻ em, số ngày, giờ bắt đầu, **không có ô ngân sách riêng** (ngân sách chỉ nằm trong lời giới thiệu và một lịch trình mẫu); điểm trong lịch trình "đổi / xếp lại / xoá" — **không thấy chữ "kéo thả"**; "lưu" = lưu + gửi email, không thấy "chia sẻ".
- "Mạnh ở lập lịch trình" là nhận định trong khi chưa ai thử chất lượng ⇒ nên ghi "tập trung vào lập lịch trình".
- A cũng tự fetch, nên nếu lần của A thấy kéo thả / ô ngân sách thì giữ.

**m-4 — câu kết luận trong Tóm tắt chưa gắn nhãn suy ra (dòng 15, "⇒ có nguồn + từ chối đúng + không bịa là giá trị thật").** Số liệu đã kiểm, nhưng mũi tên là suy ra ⇒ thêm "(suy ra)" như bảng §3 đã làm.

**m-5 — dòng 27 tự mâu thuẫn:** "Bạn cần làm: gửi yêu cầu ChatGPT (đã gửi 01/11)". Nên ghi "Bạn cần làm: lưu kết quả ChatGPT vào … khi có".

## Đã đạt
- **Đúng nhãn so với căn cứ:**
  - Huế TRIPO tồn tại / chủ quản / không công bố model;
  - Expedia 53 / 66 / 68 % (> 5.700 người, 3 nước);
  - Agoda 81 / 28 %;
  - Royal Armouries (cổng không sinh, "mô hình không được gọi", RAG 5 đoạn không rerank);
  - Air Canada;
  - TravelPlanner 0,6 %;
  - EACL lai thắng cả 10 bộ;
  - "Is Agentic RAG worth it?" — chỉ tóm tắt, đã ghi "chưa đọc số";
  - repo nhỏ 0–8 sao (GitHub API);
  - `NamSyntax` không công bố số.
- §2 nói rõ Codex nông + chỉ ý có nhãn mới được kiểm. Phần lớn ý tự khai (DeepNote, CLAMBER, MTRAG số, Booking VN, Wiley) **không** được đưa vào báo cáo — đúng điều (2).
- **(3) repo public:** 0 trùng kho / Golden / câu kín; 0 tên dự án khác; không có câu hỏi Golden. "Câu dự trù chi phí" chỉ ở mức loại câu (đã có trong `boi_canh_chung.md`). Đường dẫn `gửi chatgpt/…` chỉ là đường dẫn, không chép nội dung.

## Vòng 2 — kiểm phần sửa (B, 15:29 01/11/2026 `date`)

**Bản được kiểm:** dòng 3 ghi "15:28 01/11/2026 — sửa theo review B118 + thêm số paper C116b"; 78 dòng.
- File **untracked** ⇒ không có `git diff`; B so với nội dung bản 1 đã đọc ở vòng 1.
- Căn cứ thêm cho phần mới: `c_mach3.md` bản C116b (dòng 5, 6 của bảng + mục "Số của 2601.07711").
- `overlap_scan` lại: **0 trùng**; tên dự án khác: 0 [Chạy].

**Kết luận: `ready_for_user_confirmation`** (bản sơ bộ) — 3 major đã đóng. Còn 2 minor mới + 2 phần minor cũ chưa đóng hết; không chặn, A sửa khi viết bản 2.

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| M-1 | **đóng** | dòng 21–23: `[C kiểm]` chỉ cho 0,6 %; các bài sau ghi "[tự khai, chưa kiểm]"; vế kho Markdown ghi "(Suy ra)" |
| M-2 | **đóng** | dòng 26: tách câu con LlamaIndex "tự khai, chưa kiểm", ra khỏi câu `[C kiểm]` |
| M-3 | **đóng** | dòng 27–29: "cùng hướng lai… cách trộn khác (RRF, BM25 chấm lại 30 đoạn dense), không đo e5-small, không có du lịch" |
| m-1 | **đóng** | dòng 15 (n = 212 trong 395) + bảng dòng 55 ("khách bảo tàng dùng AI", n = 212) |
| m-2 | **đóng một phần** | Agoda có cờ "nguồn có lợi ích, không nêu cỡ mẫu"; Expedia (YouGov do Expedia đặt) và Musa Guide (hãng làm phần mềm bảo tàng) **chưa** có cờ |
| m-3 | **chấp nhận cách A xử lý** | 3 ý tranh chấp đưa vào ngoặc "kiểm lại khi thử". Còn chữ "**Mạnh** ở lập lịch trình" (dòng 9) khi chưa ai thử chất lượng ⇒ nên "tập trung vào" |
| m-4 | **đóng** | dòng 16 "(suy ra của A)" |
| m-5 | **đóng** | dòng 36 |

**Phần mới (C116b) — đối chiếu `c_mach3.md`:**
- Khớp: dòng 30–32 (55,6 ↔ 52,8; 43,9 ↔ 49,5; token vào 2,7–3,6×; thời gian ~1,5×; "không bên nào luôn hơn"; không đo câu nhiều nguồn); dòng 33 CLAMBER; dòng 35 MTRAG / MTRAG-UN; "đang dùng ~một nửa" trần (≈ 0,00025 / 0,0005, khớp `CURRENT_HANDOFF.md`).
- **m-6 (mới) — "kém ở kiểm dữ kiện (F1 64,6 ↔ 87,9)" (dòng 31) gọi sai tên việc và chỉ nêu một phía.**
  - Theo `c_mach3.md`, cặp số này là việc **lọc câu không hợp lệ / quyết định có cần tìm** đo trên bộ FEVER ("agent tìm cả khi không nên"), không phải "kiểm dữ kiện".
  - Cùng việc đó, agent lại **hơn** ở FiQA (98,8 ↔ 95,7) và CQA-EN (99,8 ↔ 96,6).
  - **Đóng khi:** viết lại kiểu "quyết định có cần tìm: agent hơn ở 2 bộ, kém xa ở FEVER (64,6 ↔ 87,9)".
- **m-7 (mới) — §2 dòng 47–48 nay tự mâu thuẫn:** câu "còn lại là tự khai, chưa đưa vào báo cáo này", trong khi dòng 22 và 26 có đưa ý tự khai (đã ghi nhãn rõ). Nên ghi "ý tự khai chỉ xuất hiện khi có nhãn [tự khai]".

**Rút lại m-3 (B, 15:55 01/11/2026 `date`):** B119 chạy biểu mẫu Huế TRIPO thật bằng Playwright ⇒ **có** ngân sách 3 mức, nút Chia sẻ, tay nắm kéo thả ở lịch trình cuối. A đúng, lần WebFetch của B không hiện phần này. Ba ý A đã bỏ có thể đưa lại vào báo cáo (nguồn: `data/nghien_cuu_phase_9_2026-11-01/tripo/b119_kham_pha.md` §1, §3).
