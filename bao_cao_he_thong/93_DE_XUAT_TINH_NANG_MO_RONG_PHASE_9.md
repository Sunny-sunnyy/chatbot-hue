# Đề xuất tính năng mở rộng Phase 9 — agent "nhìn thấy được", giọng nói, ảnh, và lịch tới 20/12

Viết: 09:25 05/11/2026 (A); thêm O5 cache 20:27 05/11/2026. Trạng thái: **đề xuất — chờ bạn duyệt từng mục**. Chưa có gì trong đây được code.
Vì sao có file này: bạn thấy tính năng Phase 9 "không có gì nổi bật", muốn nghĩ rộng về agent / agentic và trải nghiệm Huế (05/11).

**Cập nhật 09:43 05/11/2026 (bạn quyết):**
- **Chia Phase**:
  - Phase 9 = hỏi lại lịch trình · lịch trình (kèm dòng tiến độ bước thật) · **tính tiền bằng code** · sửa lịch · thời tiết · tra web · so sánh cuối.
  - **Phase 10 = giọng nói + ảnh** (làm song song Phase 9, phiên E).
  - **Phase 11 = trải nghiệm Huế** (bản đồ, sự kiện theo ngày, tiếng Anh, ăn gần, ứng xử).
  - **Phase 12 = vận hành** (trang theo dõi, agent đề xuất sửa kho có duyệt, **deploy AWS**).
- Các ý khác trong bảng §2 là **backlog**: làm dần, thử xem có hợp không, không cố đưa hết.
- Giọng nói: **nghiên cứu mô hình open-source / Việt Nam trước, không gọi API ngay**.
- Vẫn áp **nền tảng AI FDE**.
- **Đóng code khi bạn nói** (dự kiến 25–30/12, không còn 20/12); lúc đóng hệ thống **đã chạy trên AWS**.
- Bảng lịch §4 dưới đây là bản cũ. Lịch hiện hành: spec Phase 9 §11.4 (Phase 9) + spec Phase 10 §11 (Phase 10).

**Tiến độ (10:28 05/11/2026):**
- **Phase 10 — ảnh: spec bản 2 bạn duyệt** (`docs/superpowers/specs/2026-11-05-phase-10-design.md` `bf67b90fb6fc`). Gồm:
  - mốc rẻ nhất = chọn tên từ danh sách có ảnh;
  - thử trước `gpt-6-luna` ⇒ ≤ 3 tên ứng viên ⇒ người dùng bấm xác nhận;
  - dự phòng SigLIP 2 chạy máy;
  - bộ đo 25 ảnh Huế + 5 ngoài + 3 ảnh chữ ra lệnh + 10 kín;
  - chặn gửi chéo trang, bỏ EXIF;
  - trần 0,15 USD.

  E bắt đầu code. Giọng nói: nghiên cứu dở (open-source / VN), mở lại sau.
- **Phase 10 ảnh — đo lần 1 (11:48 05/11/2026): ÂM theo tiêu chí ghi trước.** Đã có đường nhận ảnh có rào chặn (gửi chéo trang, file sai loại, ảnh quá lớn ⇒ chặn trước khi gọi model; cờ tắt ⇒ chatbot y như cũ 228 / 228). Đo `gpt-6-luna` trên 33 ảnh, 2 lượt, 2 vòng chỉnh lời dặn: bản v1 nhận đúng tên Huế 22 / 25 (đạt) nhưng gán nhầm 2 / 5 ảnh nơi khác (Ngọ Môn Bắc Kinh ⇒ Đại Nội, phở ⇒ bún bò; ngưỡng ≤ 1); bản v2 hết gán nhầm nhưng nhận đúng tụt còn 20–21. Ảnh nào cũng sai: điện Hòn Chén, lăng Gia Long, bánh canh Nam Phổ. 6–9 s / ảnh, 0,0004 USD / ảnh; tiền Phase 10 0,079 / 0,15. **Bạn chọn:** giữ v1 dạng **gợi ý có xác nhận** (nhãn "có thể sai", nút "Không phải các tên này", ô gõ tên; trợ lý chỉ trả lời sau khi bạn bấm) — ghi rõ là âm theo thước gốc, đổi thước vì có bước xác nhận; **và thử thêm SigLIP 2 chạy máy + collection Qdrant ảnh riêng** (ảnh mẫu + mô tả, so ảnh người dùng với ảnh mẫu) để so với luna — E đang làm. Ảnh minh hoạ 38 / 42 tên đã có.
- **Lưu trú (Phase 11, backlog):** kho có 1 mục "nên ở khu nào" (3 nhóm khu + lý do theo kiểu đi). Link chính = Google Maps (tài liệu chính thức, không khoá). Booking: bạn quyết. Agoda: không dùng (`data/phase_11_nghien_cuu/luu_tru/e5_khu_o_va_link.md`).
- **Backlog #13 (ưu tiên đoạn cùng lĩnh vực):** bước kiểm 0 USD chỉ cứu 2 / 4 câu < ngưỡng 3 / 4 ⇒ không mở thí nghiệm. #14 đoạn gần trùng: quá ít ⇒ không mở.

Nhãn độ tin cậy:
- **[đã kiểm]**: A tự mở trang gốc ngày 05/11/2026 và thấy đúng.
- **[tự khai]**: chỉ Codex nói, A chưa mở trang gốc.
- **[đề xuất]**: ý của A, chưa đo.

## 1. Tóm tắt

- **Bài học lớn nhất từ sản phẩm thật:** thứ làm trợ lý du lịch đáng tin không phải "nhiều agent". Đó là **model đề xuất, code kiểm**.
  - Google lập lịch bằng cách để Gemini nháp danh sách hoạt động, rồi thuật toán gắn giờ mở cửa và thời gian đi lại thật, chấm tính khả thi. Lịch
    không khả thi thì điểm bằng 0 [đã kiểm, Google Research 06/06/2025]. Bài không công bố số đo.
  - Đúng bài học B4 vừa gặp: dặn model "không cộng tổng" vẫn không chặn được việc nó tự nhân giá ⇒ phép tính phải do code làm.
- **Nhiều agent chuyên môn không tự động tốt hơn.** LangChain đo trên τ-bench: khi chỉ có một miền gây nhiễu, một agent nhỉnh hơn. Agent giám sát còn
  làm sai khi "kể lại" câu trả lời của agent con, kiểu trò "tam sao thất bản" [đã kiểm, 10/06/2025].
  ⇒ Giữ một agent + công cụ rõ tên; chỉ tách agent khi số đo cho thấy cần.
- **Huế đã có sẵn khá nhiều:**
  - Visit Hue thuyết minh tự bật bằng GPS / QR, do phát thanh viên viết và đọc (không phải AI), lúc ra mắt chỉ có tiếng Việt [đã kiểm, 24/10/2025].
  - 96 trạm NFC Tap Quest ở Quần thể di tích [đã kiểm, 03/01/2026].
  - Cơ sở dữ liệu 1.100+ điểm Việt–Anh–Hàn có "Open API" (KOICA tài trợ) — **chưa có tài liệu truy cập / giấy phép công khai** [đã kiểm, 02/07/2026].
  - Huế TRIPO (31/10/2026).

  ⇒ Không làm lại audio guide hay bản đồ thuần. Giá trị của đồ án nằm ở **hỏi đáp có nguồn + lịch cá nhân hoá + tự kiểm**.
- **`gpt-6-luna` nhận được ảnh đầu vào**, cùng giá token như chữ: 0,10 USD / 1M token vào [đã kiểm, trang model OpenAI] ⇒ hỏi bằng ảnh **không cần model mới**.
- **Giọng nói ⇒ chữ:** OpenAI `gpt-transcribe` 0,0045 USD / phút [đã kiểm, trang giá]. Các model cũ (`whisper-1`, `gpt-4o-transcribe`) sẽ tắt 26/02/2027
  [đã kiểm]. Tiếng Việt không được liệt kê rõ trên trang hướng dẫn ⇒ phải thử thật.

## 2. Brainstorm đầy đủ (mọi ý, kể cả ý không chọn)

| Nhóm | # | Ý | Người dùng / hội đồng thấy gì | Công sức (1 người) | Rủi ro | A xếp |
|---|---|---|---|---|---|---|
| Agent tự kiểm | A1 | Bước rà từng số / giờ / giá / điều kiện so với đoạn kho trước khi gửi; sai ⇒ sửa / bỏ | "Đã kiểm 7 ý · bỏ 1 ý không có nguồn" | vừa | +1 lần gọi model nếu dùng model kiểm | **Gộp vào A4** (phần số do code kiểm, 0 lần gọi thêm) |
| | A4 | **Tính tiền bằng code**: tra giá có nguồn + đơn vị (người / lượt / đêm) ⇒ code nhân / cộng ⇒ bảng chi tiết có [n] + ngày nguồn; chỉ ra "Tổng" khi đủ dữ kiện | Hỏi "2 người 2 ngày hết bao nhiêu" ra số đúng, có nguồn | 2–4 ngày [tự khai, Codex ước] | dữ liệu giá cũ ⇒ luôn ghi ngày nguồn | **Bậc 1** |
| Agent nhìn thấy được | A2 | Bảng "trợ lý đang làm gì" trên giao diện: các bước đã chạy thật (hiểu câu → tìm kho → xếp lịch → kiểm luật ✓) | Hội đồng thấy agent hoạt động | 1–3 ngày | hiện bước không chạy thật ⇒ chỉ hiện theo sự kiện công cụ thật | **Bậc 1** (gộp B5) |
| | A3 | Lập lịch nhiều bước: tìm điểm → (thời tiết) → xếp buổi → tự kiểm luật → trình; sửa lịch theo yêu cầu | Tính năng "ăn tiền" nhất của trợ lý du lịch | đã trong kế hoạch (B5 + bậc sửa lịch) | đã có code kiểm | **Bậc 1** (đang làm) |
| | A5 | Nhiều agent chuyên môn (ẩm thực / di tích / lễ hội / lịch trình) | Sơ đồ đẹp | vừa | tốn token, "tam sao thất bản" | Không làm (trừ khi số đo cần) |
| Giọng nói / ảnh | V1 | **Hỏi bằng giọng nói**: bấm-nói ⇒ chữ hiện lên để sửa ⇒ gửi như câu thường | Du khách đang đi bộ hỏi nhanh | 3–5 ngày | nghe sai số / tên ⇒ luôn hiện chữ để sửa | **Bậc 1** (bạn thấy hợp lý) |
| | V2 | **Hỏi bằng ảnh**: chụp món / di tích / biển tên ⇒ model đưa 2–3 tên ứng viên ⇒ người dùng bấm xác nhận ⇒ tìm kho | Rất dễ thấy khi demo | 3–5 ngày | nhận sai ⇒ không bao giờ trả lời thẳng từ ảnh, phải qua xác nhận | **Bậc 1** (bạn thấy hợp lý) |
| | V3 | Đọc câu trả lời thành tiếng | Như audio guide | 1–2 ngày | giọng Việt của OpenAI "tối ưu cho tiếng Anh" [tự khai]; giọng trình duyệt tuỳ máy | Bậc 2 |
| Trải nghiệm Huế | H1 | Bản đồ lịch trình (OpenStreetMap, không khoá) | Lịch hiện thành tuyến trên bản đồ | 2–3 ngày (cần toạ độ 26–28 điểm) | toạ độ sai ⇒ lấy từ nguồn công khai, bạn duyệt | **Bậc 1** (gộp B5) |
| | H2 | "Tối nay / cuối tuần ở Huế có gì": sự kiện theo ngày đi | Đúng nhu cầu thật | 3–5 ngày | lịch dễ cũ ⇒ ghi nguồn + ngày; chỉ nêu sự kiện có ngày trong nguồn | Bậc 2 (gộp B5b thời tiết) |
| | H3 | Hỏi bằng tiếng Anh trên kho tiếng Việt | Khách quốc tế; khác TRIPO | 4–6 ngày (bộ đo tiếng Anh) | lý luận xuyên ngôn ngữ dễ sai [tự khai, XRAG 2025] | Bậc 2 |
| | H4 | Ăn gì gần điểm đang đi, theo buổi | Dùng chung bảng B5 | nhỏ | thấp | Bậc 2 (gộp B5 nếu rẻ) |
| | H5 | Ứng xử / trang phục / tiếp cận (người lớn tuổi, trẻ em) | Liên quan an toàn | nhỏ | kho không ghi ⇒ để trống | Bậc 2 |
| | H6 | Mini tour làng nghề (hoa giấy Thanh Tiên…) | Đưa khách khỏi trung tâm | nhỏ–vừa | lịch nghệ nhân đổi | Sau Phase 9 |
| | H7 | Hành trình check-in / câu đố | Vui | nhỏ | giá trị đồ án thấp; Huế đã có Tap Quest | Không làm |
| | H8 | Kể chuyện nhập vai vua quan | "Wow" | vừa | **bịa lịch sử — rủi ro cao nhất** | Không làm |
| | H9 | AR / ảnh xưa – nay | "Wow" | lớn | quyền ảnh, dễ hiểu nhầm là sự thật | Không làm |
| Vận hành | O1 | Trang theo dõi: số câu, tuyến, tiền, độ trễ, 👍/👎 (từ log có sẵn) | Hệ thống được vận hành, đo thật | nhỏ | thấp | Bậc 2 (B7) |
| | O2 | Agent đề xuất sửa kho khi thấy giờ / giá đổi, **bạn duyệt** rồi mới ghi | Câu chuyện "agent có người duyệt" | vừa–lớn | ghi nhầm kho | Sau Phase 9 |
| | O3 | Đưa demo lên mạng | Hội đồng thử bằng điện thoại | vừa | bảo mật, tài khoản | Quyết ở B7 |
| | O5 | **Cache câu trả lời giữa các cuộc trò chuyện** (người A hỏi X, người B hỏi X ⇒ trả lại câu đã lưu) | Câu lặp trả ngay thay vì 2–5 s | nhỏ (khớp đúng chữ) | cache theo nghĩa trả sai ~8 % lần trúng (benchmark AWS, A kiểm) ⇒ "nói chắc sai"; cache đóng băng một lần trả lời kém; câu nối tiếp / thời tiết / web không cache được | **Phase 12, bạn chọn 20:27 05/11/2026:** khi có người dùng thật, đo tỉ lệ câu lặp (`cau_lap`, băm chỉ trong RAM) 1–2 tuần; lặp ≥ 20 % mới làm cache khớp đúng chữ hẹp (lượt đầu, có nguồn kho, không câu từ chối / web / thời tiết, khoá theo phiên bản kho + lời dặn + model, 24 h); **không** cache theo nghĩa. Nghiên cứu: `data/nghien_cuu_cache_2026-11-05/c201_cache.md` (private) |
| | O4 | Dùng API 1.100 điểm của Huế | Dữ liệu chính thống, 3 thứ tiếng | ? | chưa có tài liệu / giấy phép công khai | Chỉ tra thêm (hỏi đơn vị chủ quản nếu bạn muốn) |

## 3. Chi tiết bậc 1

**A4 — tính tiền bằng code** (thay Cách A đã âm ở B4):
- Code đọc giá có nguồn từ kho, mỗi giá kèm đơn vị và ngày nguồn. C đang kiểm kê xem kho có những loại giá nào: `data/phase_9/tinh_tien/kiem_ke_gia.md`.
- Code nhận số người / ngày từ đường hỏi lại (B4b), tự nhân / cộng, rồi trả một bảng có cấu trúc. Model chỉ viết lời quanh bảng.
- Thiếu giá một khoản ⇒ ghi "chưa có dữ liệu", **không** tính tổng phần đó.

Đo: 0 dòng "Tổng" không có căn cứ trên bộ câu chi phí (đã thấy + kín mới); bộ an toàn 32 câu đủ 4 số.

**A2 + A3 + H1 — lịch trình nhìn thấy được** (làm trong B5, không thêm bậc):
- Sự kiện SSE đã có ("đang tìm kho…") ⇒ thêm các bước "đang xếp lịch / đã kiểm luật ✓ / đã bỏ 1 điểm vì …".
- Bản đồ tuyến từng ngày (Leaflet + OpenStreetMap; kiểm CSP).
- Toạ độ lấy từ nguồn công khai, bạn duyệt như bảng điểm.

**V1 — giọng nói:**
- Luồng: trình duyệt ghi âm ngắn ⇒ gửi backend ⇒ `gpt-transcribe` ⇒ chữ hiện trong ô nhập để sửa ⇒ người dùng bấm Gửi.
- Không lưu âm thanh, không ghi vào log.
- Mic chỉ chạy trên `localhost` / HTTPS.

Tiền: câu nói 10 giây ≈ 0,00075 USD — **cao hơn trần 0,0005 USD / câu** của câu gõ chữ ⇒ bạn quyết có chấp nhận cho câu nói không.

Phương án khác:
- Nhận dạng giọng nói có sẵn trong trình duyệt (miễn phí, nhưng âm thanh có thể gửi lên máy chủ của hãng trình duyệt).
- PhoWhisper chạy trên máy (miễn phí, khoảng 1,5 GB RAM cho cỡ small [tự khai], chậm hơn).

⇒ Thử 10 câu nói thật tiếng Việt (có tên Huế, có số) trên 2 phương án rồi chọn.

**V2 — ảnh:**
- Luồng: trình duyệt thu nhỏ ảnh ⇒ backend giải mã lại, bỏ EXIF (vị trí GPS) ⇒ gửi `gpt-6-luna` với lời dặn "chỉ trả 2–3 tên ứng viên trong danh sách điểm / món có trong kho, hoặc 'không rõ'".
- Người dùng bấm một tên ⇒ thành câu hỏi thường ⇒ tìm kho.
- Ảnh không lưu.

Đo:
- Bộ 30 ảnh tự chụp / ảnh có giấy phép: tên đúng có trong ứng viên ≥ ?/30 (ghi trước khi đo).
- **0 câu trả lời thẳng từ ảnh** khi chưa xác nhận.

Thay đổi dữ liệu gửi ra ngoài: ảnh của người dùng tới OpenAI ⇒ ghi vào báo cáo an toàn, chạy skill `agent-security-review`.

## 4. Lịch đề xuất tới đóng code 20/12

B và C chạy song song; mỗi việc vẫn đi theo trình tự plan ⇒ review ⇒ đo ⇒ merge.

| Tuần | B | C | Ghi chú |
|---|---|---|---|
| 05–09/11 | B4b (hỏi lại chỉ lịch trình) ⇒ merge; code B5 | review B4b; kiểm kê giá; plan A4 | bạn duyệt bảng điểm v3 |
| 10–16/11 | đo + merge B5 (kèm A2 + bản đồ) | code A4 (tính tiền) | #6 tốc độ: trình bạn bật |
| 17–23/11 | bậc sửa lịch nhiều lượt | V1 giọng nói (thử 2 phương án ⇒ code) | |
| 24–30/11 | B5b thời tiết (+ H2 sự kiện theo ngày nếu kịp) | V2 ảnh | |
| 01–07/12 | B6 tra web | H3 tiếng Anh (nếu kịp) hoặc dự phòng | |
| 08–14/12 | dự phòng / sửa lỗi | đo cuối Phase 9 | |
| 15–20/12 | B7 đóng gói, demo, sơ đồ kiến trúc, báo cáo | | |

- Tuần dự phòng 08–14/12 là chỗ hở duy nhất. Trễ hơn 1 tuần ⇒ bỏ H3 trước, rồi V3 / H2.
- **Tiền:** Phase 9 đã dùng ≈ 1,27 / 2,0 USD. Kế hoạch cũ tới B7 ≈ 1,9; thêm A4 + V1 + V2 ≈ +0,15–0,25 [đề xuất, ước thô] ⇒ có thể vượt 2,0. Theo lời bạn 05/11: tới lúc đó A xin thêm, kèm số đã dùng.
- **Spec Phase 9 phải sửa** (thêm A4, V1, V2; model chuyển giọng nói `gpt-transcribe` là model mới; ảnh người dùng gửi OpenAI) ⇒ bạn duyệt một lần bản sửa đổi spec.

## 5. Cần bạn quyết (mỗi lần một câu, A hỏi trong chat)

1. Duyệt bậc 1 (A4, A2 + bản đồ trong B5, V1, V2) và lịch trên?
2. Câu nói được phép > 0,0005 USD / câu không (hay chỉ dùng cách miễn phí)?
3. Bậc 2 chọn cái nào nếu còn thời gian (H3 tiếng Anh / H2 sự kiện theo ngày / V3 đọc thành tiếng / O1 trang theo dõi)?

## 6. Nguồn

- Đã kiểm 05/11/2026:
  - Google Research "Optimizing LLM-based trip planning" (06/06/2025);
  - LangChain "Benchmarking Multi-Agent Architectures" (10/06/2025);
  - HNN Visit Hue thuyết minh (24/10/2025);
  - HNN số hoá di sản / Tap Quest (03/01/2026);
  - khamphahue.com.vn cơ sở dữ liệu 1.100 điểm (02/07/2026);
  - OpenAI trang model `gpt-6-luna`, trang giá, hướng dẫn chuyển giọng nói thành chữ.
- Tự khai (Codex, chưa mở): toàn bộ danh mục URL ở `data/tra_cuu_cli/2026-11-05_a05-agentic/`, `…_a05-trai-nghiem-hue/`, `…_a05-giong-noi-anh/` (private).
- Yêu cầu nghiên cứu sâu gửi ChatGPT (bạn gửi khi rảnh): `gửi chatgpt/2026-11-05/tìm thông tin/nghien_cuu_agentic_noi_bat_2026_11_05.md`.
- Nghiên cứu trước (cách làm cho đúng, 8 repo, TRIPO): [92_BAO_CAO_NGHIEN_CUU_PHASE_9.md](92_BAO_CAO_NGHIEN_CUU_PHASE_9.md).
