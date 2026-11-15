# Plan NHÁP — nhận diện nơi / món bằng SO ẢNH với ảnh mẫu (embedding ảnh, image-to-image)

B viết 21:18 15/11/2026 · A giao theo câu hỏi của User ("tưởng hệ thống embed ảnh rồi so tương đồng với ảnh trong dữ liệu; đã thử Gemini Embedding 2, DINOv2 / v3 chưa?") · **NHÁP — chưa review, chưa duyệt, CHƯA chạy lượt nào** · model / provider mới ⇒ A trình User trước khi chạy. Phạm vi ảnh User đã chốt: chỉ nhận diện nơi / món rồi tìm thông tin trong kho (không hỏi đáp nội dung ảnh).

## Căn cứ để review
`report_agent/2026-11-05_phase_10_anh/e9_siglip_implementation.md` (thử SigLIP 2, âm) · `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` (luna v0–v2, tiêu chí gốc) · `backend/llm/nhan_anh.py` (bản đang chạy) · mục 1 dưới đây (nguồn ngoài, có link).

## 1. Tra cứu (15/11/2026; B tự mở từng trang — nhãn [nguồn] = trang nói, [suy ra] = B suy)
| Model | Nhận ảnh | Chiều | Chạy ở đâu | Giá / giấy phép | Số truy hồi công trình công bố |
|---|---|---|---|---|---|
| **Gemini Embedding 2** (`google/gemini-embedding-2`, phát hành 20/05/2026) | CÓ — "text and images into a unified vector space"; Google: ≤ 6 ảnh / yêu cầu, PNG / JPEG [nguồn] | 128–3.072 (khuyên 768 / 1.536 / 3.072), tự chuẩn hoá [nguồn] | API (OpenRouter ⇒ Google AI Studio / Vertex) | ảnh **0,45 USD / 1M token**, chữ 0,20 [nguồn]; số token / ảnh **không thấy ghi** (trang Google chỉ nêu 258 token cho một trang PDF dựng thành ảnh) ⇒ ước ~0,0001 USD / ảnh [suy ra — đo bằng 1 ảnh trước] | không thấy số công bố cho truy hồi công trình [chưa có nguồn] |
| **DINOv2** (`facebook/dinov2-base`, 86,6 M tham số) | ảnh (không chữ) | 768 (ViT-B); S 384 · L 1.024 | máy, `transformers` AutoModel; vector = token CLS [nguồn] | Apache-2.0, **không** khoá tải [nguồn] | Oxford-H 58,2 · Paris-H 84,6 · Met 44,6 · AmsterTime 48,9 (bản lớn, bảng của paper DINOv3) [nguồn — xem ghi chú] |
| **DINOv3** (`facebook/dinov3-vitb16-pretrain-lvd1689m`, 86 M; S 21 M · L 300 M) | ảnh | 768 (B); S 384 · L 1.024 | máy, `transformers` (`pooler_output`) [nguồn] | "DINOv3 License"; **repo khoá: phải đăng nhập Hugging Face và đồng ý chia sẻ thông tin** mới tải được [nguồn] ⇒ cần User làm một lần | Oxford-H theo cỡ: S 49,5 · B 58,5 · L 63,1 · 7B 72,8 [nguồn: model card] |
| *(đã thử 05/11)* SigLIP 2 base | ảnh + chữ | 768 | máy | — | Oxford-H **25,1** · Paris-H 60,9 (bản lớn, cùng bảng) [nguồn — xem ghi chú] |

- **Giả thuyết của A được nguồn ủng hộ:** paper DINOv3 (arXiv 2508.10104, mục 6.2.2 "Instance Recognition", xếp hạng bằng cosine trên token CLS, không huấn luyện thêm) viết model ảnh–chữ "are lagging far behind DINOv3"; bảng 9: SigLIP 2 25,1 / PEcore 32,7 ↔ DINOv2 58,2 / DINOv3 60,7 (Oxford-Hard). Ghi chú thận trọng: công cụ đọc trang trả bảng 9 **không kèm tên hàng**, tên được ghép theo thứ tự bảng 8 (khớp hai mức chênh paper nêu bằng chữ) ⇒ người review mở PDF kiểm lại trước khi trích vào báo cáo cho User.
- **Chưa tra xong (ghi "chưa có nguồn", không đoán):** khuôn yêu cầu gửi ẢNH qua `/api/v1/embeddings` của OpenRouter (trang model chỉ nói "hỗ trợ"); số token mỗi ảnh; chính sách lưu dữ liệu của hai provider Google; ms / ảnh của DINO trên CPU (SigLIP 2 base cùng cỡ trên máy này: 253–278 ms, RSS 1,6 GB — DINO ViT-B cùng 86 M tham số ⇒ dự đoán cùng bậc [suy ra]); ứng viên chuyên "nhận diện địa điểm" khác. Kết quả tra bằng script Codex (đang chạy lúc viết): `data/tra_cuu_cli/2026-11-15_so-anh-embedding/` — đọc + tự mở kiểm trước khi dùng.
- Khoá OpenRouter: code đã gọi OpenRouter cho embedding chữ (`backend/embedding/full_corpus.py`, thí nghiệm 30/10) ⇒ khoá từng có trong môi trường; **chưa kiểm còn dùng được** (kiểm bằng một lần gọi 1 ảnh, không đọc file khoá).
- Link: https://openrouter.ai/google/gemini-embedding-2 · https://aistudio.google.com/docs/embeddings · https://huggingface.co/facebook/dinov2-base · https://huggingface.co/facebook/dinov3-vitb16-pretrain-lvd1689m · https://raw.githubusercontent.com/facebookresearch/dinov3/refs/heads/main/MODEL_CARD.md · https://arxiv.org/abs/2508.10104

## 2. Vì sao thử lại (khác gì 05/11)
05/11 chỉ thử SigLIP 2 base: so ảnh với 172 ảnh mẫu đạt 20 / 25, nhưng 5 / 5 ảnh ngoài Huế vẫn bị gán tên và các lăng / điện lẫn nhau. Hai thứ đổi lần này, **tách riêng để biết cái nào có tác dụng**: (a) model — họ DINO được công bố mạnh hơn hẳn ở "đúng công trình này" thay vì "loại công trình này"; (b) dữ liệu — bộ ảnh mẫu to hơn + có tập ảnh ÂM để đặt ngưỡng từ chối (05/11 không có ảnh âm ⇒ ngưỡng vô dụng).

## 3. Biến thể (mỗi biến thể đổi đúng một thứ so với hàng trên nó)
| Mã | Model | Ảnh mẫu | Ghi chú |
|---|---|---|---|
| M0 | SigLIP 2 base (như 05/11) | 172 ảnh cũ | mốc — dùng lại số 05/11 nếu chạy lại ra giống byte |
| M1 | SigLIP 2 base | bộ mẫu MỚI + ngưỡng từ ảnh âm | chỉ đổi dữ liệu ⇒ biết dữ liệu cứu được bao nhiêu (0 USD) |
| D2 | DINOv2 ViT-B (CLS) | bộ mẫu mới | chỉ đổi model so với M1; không cần quyền gì ngoài tải ~350 MB |
| D3 | DINOv3 ViT-B | bộ mẫu mới | chỉ khi User đồng ý điều khoản trên Hugging Face |
| G | Gemini Embedding 2 (768 chiều) | bộ mẫu mới | có phí; ảnh gửi ra Google qua OpenRouter |
| mốc ngoài | luna v1 đang chạy | — | 22 / 25 · ngoài danh sách bị gán 0 và 2 / 5 · tên số 1 đúng 21 / 25 (đếm 15/11) |

## 4. Dữ liệu
- **Ảnh mẫu (bước 0, 0 USD — đếm trước khi làm gì khác):** với 42 tên trong danh sách nhận ảnh, đếm số ảnh đã có theo từng tên từ ba nguồn: ảnh Khám phá (260 bài), ảnh lịch (40 điểm), 172 ảnh Commons cũ. Mục tiêu ≥ 8 ảnh / tên, riêng nhóm hay nhầm (các lăng, điện, cổng thành; hai món 05/11 sai lặp lại) ≥ 15 ảnh / tên, nhiều góc. Thiếu ⇒ tải thêm từ Commons theo công cụ cũ; **một người nhìn tận mắt 100 % ảnh mẫu** (05/11 chưa ai xem).
- **Ảnh ÂM (~100):** không phải Huế nhưng dễ nhầm — cổng / cung điện Á Đông nơi khác, chùa và lăng tỉnh khác, món nước / bánh vùng khác, cộng ảnh linh tinh (người, phố, con vật). Chỉ dùng để đặt ngưỡng.
- **Ngưỡng từ chối:** chọn trên ảnh mẫu (bỏ-một-ra) + ảnh âm, **không nhìn bộ đo**: ngưỡng = mức mà ≤ 5 % ảnh âm vượt qua; ghi kèm bao nhiêu % ảnh mẫu rơi dưới ngưỡng. Hai mức đó ghi vào file trước khi mở bộ đo.
- **Bộ đo:** 33 ảnh cũ (25 trong danh sách · 5 ngoài · 3 có chữ ra lệnh) giữ nguyên để so với 05/11 + **bộ mới 30–40 ảnh "người thường chụp"** (điện thoại, góc lệch, có người, trời xấu): xin User 15–20 ảnh tự chụp / bạn bè chụp nếu có; phần còn lại lấy ảnh du khách có giấy phép mở, khác tác giả với ảnh mẫu; người gắn nhãn không phải người chạy. Bộ mới có ≥ 8 ảnh ngoài danh sách.
- **Chống lẫn mẫu ↔ đo:** sha256 + tên file như 05/11, thêm bước mới: cặp mẫu–đo có cosine > 0,98 theo chính model đang đo ⇒ loại ảnh mẫu đó.

## 5. Tiêu chí ghi trước (giữ như 05/11; k-NN tất định ⇒ một lượt)
| Vai | Chỉ số | Ngưỡng |
|---|---|---|
| Sàn | Q-c: ảnh ngoài danh sách bị gán tên (bộ cũ) | ≤ 1 / 5 |
| Sàn | Ảnh có chữ ra lệnh làm theo chữ | 0 / 3 (model chỉ-ảnh không đọc lệnh — kiểm lại) |
| Quyết | Q-a: tên đúng trong top 3 (bộ cũ) | ≥ 22 / 25 |
| Quyết | Tên số 1 đúng (bộ cũ) — vì User muốn trả lời thẳng | ≥ 22 / 25 (mốc luna 21) |
| Xác nhận | Bộ mới "người thường chụp": cùng bốn chỉ số, báo riêng | không tệ hơn luna v1 chạy trên cùng bộ (≈ 0,02 USD) quá 2 ảnh |
| Theo dõi | ms / ảnh p50 · p95, RSS, USD / ảnh, số ảnh rời máy | báo |

**Đọc kết quả:** (i) một biến thể đạt cả sàn + hai chỉ số quyết + xác nhận ⇒ đề xuất User THAY luna ở bước nhận diện (plan riêng để đưa vào chatbot); (ii) đạt sàn và top 5 chứa tên đúng ≥ 24 / 25 nhưng tên số 1 chưa đạt ⇒ đề xuất GHÉP: embedding từ chối ảnh lạ + đưa top 5 cho luna chọn (05/11 ghép âm vì top 5 chỉ 22 / 25) — đo như một bậc riêng; (iii) còn lại ⇒ BỎ, ghi hồ sơ. M1 ↔ D2 cho biết phần nào do dữ liệu, phần nào do model. Không chỉnh ngưỡng sau khi thấy số bộ đo.

## 6. Tiền · thời gian · máy
- D2 / D3 / M1: 0 USD. G: (ảnh mẫu ~700 + âm ~100 + đo ~70) × ~0,0001 ≈ **0,1 USD** [ước — số token / ảnh chưa có nguồn; gọi 1 ảnh đo token thật rồi ước lại, quá 0,3 USD thì dừng hỏi A]. luna v1 trên bộ mới ≈ 0,02. Trần đề nghị **0,5 USD**.
- Thời gian ước: bước 0 + gom ảnh + nhìn ảnh 1,5–2 giờ; nạp + đo mỗi model ~20 phút; report 30 phút.
- Máy 19 GB: **một model một lúc** (ước ~1,5–2 GB RSS mỗi model), không chạy khi nhóm đang đo tốc độ; vector lưu file `.npy` trong `data/` (không dựng collection Qdrant mới — ~900 vector thì so bằng numpy là đủ).

## 7. Cần User / A quyết trước khi chạy
1. Cho tải DINOv2 ViT-B (~350 MB, Apache-2.0) — model mới.
2. DINOv3: User có đồng ý điều khoản trên Hugging Face (đăng nhập, chia sẻ thông tin tài khoản) không; không ⇒ bỏ D3.
3. Gemini Embedding 2 qua OpenRouter: provider + **đường dữ liệu mới** — ảnh mẫu (công khai) gửi Google khi đo; nếu sau này dùng lúc chạy thật thì **ảnh người dùng gửi sang Google** (hiện ảnh đang gửi OpenAI) ⇒ ghi checklist deploy. Model chạy máy thì ảnh không rời máy.
4. User có 15–20 ảnh tự chụp ở Huế để làm bộ "người thường chụp" không.

## 8. Bảng rà khung AI FDE (rút gọn — nguồn dữ liệu / đường ra mới)
| Mục | Hiện trạng | Đề xuất |
|---|---|---|
| Có cần model không | bước nhận diện đang là một lần gọi model ngôn ngữ có ảnh | so vector = phép tính tất định, rẻ, lặp lại được ⇒ đúng hướng "việc tính được thì để code" |
| Dữ liệu ngoài là dữ liệu | chữ trong ảnh từng điều khiển tên (1 / 3) | model chỉ-ảnh không đọc lệnh; với G (đa phương thức) phải đo 3 ảnh chữ ra lệnh |
| Đường ra mới | ảnh ⇒ OpenAI | G: ảnh ⇒ OpenRouter ⇒ Google (mục 7.3) |
| Quyền hẹp | — | khoá OpenRouter chỉ dùng cho embedding; không ghi ảnh người dùng xuống đĩa |
| Rào đo hai chiều | 05/11 không có ảnh âm | tập âm + sàn Q-c + bộ "người thường chụp" |
