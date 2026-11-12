# Review: plan mức nhẹ "Lưu trú: khu nên ở + link tìm chỗ ở do code dựng" · nháp bản 1 · một vòng

Decision: **changes_requested** (1 major, 6 minor; 0 blocker) — sửa chữ trong plan là đủ, **không cần vòng review thứ hai** (mức nhẹ: A đọc rồi duyệt)
Người kiểm: C (`hue-rag-e1`, Claude Code — Fable 5.2)
Date: 20:54 12/11/2026 (`date`)
Bản được review: `docs/superpowers/plans/2026-11-12-luu-tru-khu-va-link-plan.md` sha256 `6f66f1eeafed` (người viết: E)
Căn cứ: các mục plan ghi ở "Căn cứ để review" + lượt đếm 12/11 của chính C (`report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md`, dữ liệu private
`data/phase_11/dot_2_dem/ket_qua_lan_1.jsonl`) + `backend/llm/tra_web.py` (`LUU_TRU_TU`, `la_cau_luu_tru`).

## 1. Phạm vi đã review

- Đọc hết plan (kể cả mục 8b bổ sung). Bốn điểm A dặn chú ý: (i) cách kích hoạt theo nguồn kho có bắt đúng các câu lưu trú đã đếm không; (ii) câu thường không dính thẻ;
  (iii) code quyết link, model không tự dựng URL; (iv) tiêu chí ghi trước đủ đo.
- Chỉ đọc, 0 USD; **không chạy tầng tìm** (B đang đo tốc độ ⇒ không việc nặng) — phần cần tầng tìm ghi ở mục 5. Tả câu ở mức loại câu.

## 2. Findings

### M-1 (major) — cách kích hoạt "theo nguồn kho" chưa chắc bắt được đúng loại lỗi đã đếm, và tiêu chí L1 cho phép trượt đúng loại đó

- **Vị trí:** plan mục 4 (cách 1), mục 5 (bước 0), mục 6 dòng L1.
- **Yêu cầu bị ảnh hưởng:** mục tiêu của chính plan (mục 1: "ở **mọi** lượt về lưu trú… dù kho trả lời hay từ chối"); luật "đếm lỗi trước khi xây" — lỗi đếm được là **3 / 4 câu hỏi
  cơ sở cụ thể bị kho từ chối**, không phải câu "nên ở khu nào" (2 / 2 đã ổn).
- **Bằng chứng (đọc nguồn trích của 6 câu lưu trú trong lượt đếm 12/11):**

  | Câu (loại) | Kết cục 12/11 | Nguồn được trích có mục "nên chọn khu vực lưu trú" của kho? | Từ khoá `LUU_TRU_TU` khớp câu hỏi? |
  |---|---|---|---|
  | 2 câu "nên ở khu nào" | kho trả lời | **có** (2 / 2) | không (0 / 2) |
  | 1 câu cơ sở gần một điểm ven biển | kho trả lời một phần | **không** — trích mục khác (bài của chính điểm đó + bài "nên đi đâu") | không |
  | 3 câu cơ sở cụ thể (gần điểm · giá rẻ · hạng sao) | **kho từ chối**, 0 nguồn trích | chưa biết — tuỳ k đoạn đầu của lần tìm đầu (bước 0 mới đo) | **có** (3 / 3) |

  ⇒ Theo dữ liệu đang có, cách 1 chỉ **chắc chắn** bắt 2 / 6 câu — đúng hai câu vốn đã ổn. Ba câu là lỗi đã đếm phụ thuộc hoàn toàn vào việc tầng tìm có kéo được mục lưu trú
  vào k đoạn đầu hay không (kho không có danh sách cơ sở ⇒ câu "khách sạn hạng sao" rất có thể kéo về bài khác). Câu thứ ba cho thấy danh sách "mục kho về lưu trú" chỉ gồm mục
  "nên chọn khu vực lưu trú" là **quá hẹp**: kho còn ít nhất 6 bài điểm tham quan có đoạn nêu cơ sở lưu trú.
- **L1 "≥ 10 / 12"** cho phép trượt 2 câu — có thể trượt đúng các câu cơ sở cụ thể mà plan vẫn "đạt".
- **Tác động:** xây xong, đo đạt, nhưng người hỏi "gợi ý khách sạn gần …" vẫn chỉ nhận câu từ chối + web hên xui — đúng tình trạng hôm nay.
- **Tiêu chí đóng (sửa chữ trong plan, không cần review lại):**
  1. Bước 0 báo **riêng** cho 4 câu cơ sở cụ thể của lượt 12/11 (không gộp trong 12), với **ba cách kích hoạt đặt cạnh nhau**: (a) theo nguồn kho · (b) từ khoá `la_cau_luu_tru` ·
     (c) **hợp của hai cách**. Chọn cách + k theo số; plan ghi rõ được phép chọn (c). Lý do (b) dùng được: thẻ chỉ là hiển thị do code dựng, chữ người dùng **không vào URL**,
     bộ dò đã chạy trong sản phẩm cho luật giá của mục web ⇒ không trái nguyên tắc "chữ người dùng là dữ liệu".
  2. Thêm tiêu chí **L1b: ≥ 3 / 4 câu cơ sở cụ thể đã đếm có thẻ** (và các câu cơ sở cụ thể trong 6 câu mới: ≥ 2 / 3). Không đạt ⇒ dừng như mục 5 đã ghi.
  3. Danh sách "mục kho về lưu trú" trong bảng: ghi cách lập (vd mọi mục kho có nêu tên một cơ sở lưu trú hoặc nói về chọn chỗ ở — đếm bằng `scripts/grep_kb.sh`), không chỉ một mục.

### Minor (không chặn; sửa cùng lượt nếu tiện)

- **m-1 — L6 không đo được thứ nó định đo.** L5 đã chứng minh chuỗi gửi model giống byte ⇒ "loại kết cục cờ bật ↔ cờ tắt" chỉ còn khác do model không tất định (lượt 12/11: cùng
  loại câu, mục web lúc có lúc "không tin cậy"). Đề nghị: chạy 12 câu **một trạng thái (cờ bật)** để xem thẻ hiện đúng trên đường thật (cả stream) ⇒ ≈ 0,015 USD thay vì 0,03;
  bỏ phép so bật ↔ tắt.
- **m-2 — chọn k trên chính bộ đo L1.** Mức nhẹ không có bộ kín nên chấp nhận được, nhưng ghi rõ: 6 câu mới phải **viết xong trước bước 0**, và report nói "k chọn trên bộ đo".
- **m-3 — câu tiếng Anh ×1 trong bộ L1.** Tiếng Anh đang ngoài phạm vi đã chốt (lượt đếm thứ hai 12/11: kho trả lời tiếng Anh bằng tiếng Việt); từ khoá `LUU_TRU_TU` có "resort /
  homestay / villa" nhưng không có "hotel". Bỏ câu này khỏi mẫu số, hoặc để riêng làm quan sát.
- **m-4 — test theo loại lượt chưa liệt kê.** Chuỗi gửi model không đổi nên không bắt buộc theo luật (4c), nhưng thẻ đi qua ba đường + SSE ⇒ nên ghi 5 ca: lượt kho trả lời có
  mục lưu trú · lượt kho từ chối (có / không mục web) · lượt ngoài phạm vi (không thẻ) · lượt biểu mẫu lịch trình (không thẻ) · lượt hỏi tiếp có lịch sử (xét nguồn của **lượt này**).
- **m-5 — mục 8b (b) mâu thuẫn mục 9 và mức nhẹ.** Mục 9 ghi "link đặt phòng điền sẵn ngày / người: không làm"; 8b (b) lại mở đúng việc đó, kèm đích thứ hai có tham số không tài
  liệu và cần ô ngày / số người mà biểu mẫu chưa có. C đồng ý khuyến nghị (a) của plan; nếu User chọn (b) ⇒ tách thành việc riêng, không nằm trong plan mức nhẹ này.
- **m-6 — câu "hợp với ai" trên thẻ là chữ cố định chép ý kho nhưng không có nguồn.** Mọi câu trả lời khác đều có trích dẫn; đề nghị thẻ kèm một dòng nguồn (tên bài cẩm nang,
  link trang Khám phá bằng `bai_id` sẵn có) để giữ nguyên tắc "nói gì cũng chỉ được nguồn".

### Điểm đạt (theo 4 ý A dặn)

- **(iii) Code quyết link — đạt.** URL chỉ một gốc Maps, chuỗi tìm từ bảng cố định, 0 chữ người dùng / model trong URL, giao diện lọc gốc như thẻ lịch; L4 có ca chữ lạ. Model không
  viết link, không chọn khu.
- **(ii) Câu thường không dính thẻ — tiêu chí đủ** (L2 ≤ 3 / 190 và 0 câu an toàn; L3 = 0 trên 44 câu ngoài phạm vi), đo 0 USD trên dữ liệu B7 có sẵn. Nếu chọn cách kích hoạt (c),
  L2 / L3 phải tính cho đúng cách đó (từ khoá có thể dính câu về một điểm tham quan có chữ "resort" trong tên) — bước 0 đã có chỗ cho việc này.
- **(iv) Tiêu chí ghi trước — đủ đo sau khi thêm L1b**; bảng rà khung AI FDE có đủ hai chiều; có đường lùi (bảng hỏng ⇒ như cờ tắt).
- Không over-engineering: không thêm lần gọi model, không đổi lời dặn, dùng lại khuôn thẻ lịch. Cách 2 (nhãn do model) được loại đúng lý do.

## 3. Cách người kiểm chạy lại thật

- `sha256sum` plan; đọc `LUU_TRU_TU` + `la_cau_luu_tru` trong `backend/llm/tra_web.py`.
- Script ngắn đọc `data/phase_11/dot_2_dem/ket_qua_lan_1.jsonl`: với 6 câu loại lưu trú in kết cục + tiêu đề / đường dẫn mục của nguồn được trích (không in câu trả lời).
- Đối chiếu từ khoá với 6 câu hỏi bằng mắt (câu do C viết).

## 4. Kết quả quan sát

| Khẳng định của plan | Quan sát | Kết quả |
|---|---|---|
| "Câu nên ở khu nào: 2 / 2 đủ dùng; cơ sở cụ thể 3 / 4 bị từ chối" | khớp report đếm | đúng |
| Cách 1 nhận lượt qua nguồn được trích | 2 / 2 câu "khu nào" trích đúng mục lưu trú; câu cơ sở được kho trả lời trích mục khác | đúng một phần — M-1 |
| "`la_cau_luu_tru` đã có sẵn" | có; 6 từ khoá; khớp 3 / 3 câu bị từ chối, 0 / 3 câu còn lại | đúng |
| Chuỗi gửi model không đổi | thiết kế đặt lời gọi sau câu trả lời, cạnh `set_notice` — hợp lý; chưa có code để kiểm | chưa kiểm (đúng — code chưa viết) |

## 5. Giới hạn hoặc phần chưa chạy

- **Không chạy tầng tìm** cho 3 câu bị từ chối ⇒ không biết mục lưu trú đứng hạng mấy; đó chính là việc của bước 0 (C không làm thay để không chạy việc nặng lúc B đang đo).
- Không mở `e_nguon_luu_tru.md` / `e_tim_web_serper_exa.md` ngoài phần plan đã tóm (plan này không dùng nguồn lưu trú ngoài).
- Chưa xem bảng `khu_v1.json` (chưa có).

## 6. Decision và bước tiếp theo

**changes_requested** — E sửa plan theo M-1 (3 ý của tiêu chí đóng) + minor tuỳ chọn; **không cần C xem lại**: A đọc bản sửa rồi duyệt (mức nhẹ). Bước 0 chạy sau khi B nhắn "đo xong".
Người viết 6 câu mới: nên là B hoặc C trước bước 0 (C sẵn sàng viết khi A giao).
