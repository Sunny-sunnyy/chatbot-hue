# Plan NHÁP bản 2 — nhận diện nơi / món bằng SO ẢNH với ảnh mẫu (embedding ảnh, image-to-image)

B viết bản 1 21:20 15/11/2026, **bản 2 21:33 15/11/2026** sau review của C (`2026-11-15-so-anh-embedding-plan_review.md` trên nhánh `p10-so-anh-review`: 3 major, 6 minor) + số đếm bước 0 của E + phép dò DINOv2 của B · A giao theo câu hỏi của User · **NHÁP — chờ C review vòng 2, chưa duyệt; mới chạy phép dò 0 USD (mục 2)**. Phạm vi ảnh User đã chốt: chỉ nhận diện nơi / món rồi tìm thông tin trong kho. User đã đồng ý: tải DINOv2; DINOv3 (đang chờ Meta duyệt quyền tải); dùng tiền API cho embedding ảnh. User không có ảnh tự chụp.
## Căn cứ để review
`report_agent/2026-11-05_phase_10_anh/e9_siglip_implementation.md` (thử SigLIP 2, âm) · `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` (luna v0–v2, tiêu chí gốc) · `backend/llm/nhan_anh.py` (bản đang chạy) · mục 1 dưới đây (nguồn ngoài, có link) · private: `data/so_anh_2026-11-15/KET_QUA_DO_DINO.md` (phép dò), `data/so_anh_buoc0_2026-11-15/KET_QUA.md` (đếm ảnh mẫu), `data/dem_ten_so_1_2026-11-15/KET_QUA.md` (tên số 1 của luna).

## 1. Tra cứu (15/11/2026; B tự mở từng trang — nhãn [nguồn] = trang nói, [suy ra] = B suy)
| Model | Nhận ảnh | Chiều | Chạy ở đâu | Giá / giấy phép | Số truy hồi công trình công bố |
|---|---|---|---|---|---|
| **Gemini Embedding 2** (`google/gemini-embedding-2`, phát hành 20/05/2026) | CÓ — "text and images into a unified vector space"; Google: ≤ 6 ảnh / yêu cầu, PNG / JPEG [nguồn] | 128–3.072 (khuyên 768 / 1.536 / 3.072), tự chuẩn hoá [nguồn] | API (OpenRouter ⇒ Google AI Studio / Vertex) | ảnh **0,45 USD / 1M token**, chữ 0,20 [nguồn]; bảng giá Google ghi thẳng **0,00012 USD / ảnh** (lô: 0,00006); gói trả phí: dữ liệu không dùng để cải thiện sản phẩm [nguồn: trang giá Google — giá qua OpenRouter đọc từ `usage` của 1 lần gọi thử] | không thấy số công bố cho truy hồi công trình [chưa có nguồn] |
| **DINOv2** (`facebook/dinov2-base`, 86,6 M tham số) | ảnh (không chữ) | 768 (ViT-B); S 384 · L 1.024 | máy, `transformers` AutoModel; vector = token CLS [nguồn] | Apache-2.0, **không** khoá tải [nguồn] | Oxford-H 58,2 · Paris-H 84,6 — số của bản **ViT-g** (1,1 tỉ tham số), không phải bản B [nguồn: paper DINOv3 bảng 9] |
| **DINOv3** (`facebook/dinov3-vitb16-pretrain-lvd1689m`, 86 M; S 21 M · L 300 M) | ảnh | 768 (B); S 384 · L 1.024 | máy, `transformers` (`pooler_output`) [nguồn] | "DINOv3 License"; **repo khoá: phải đăng nhập Hugging Face và đồng ý chia sẻ thông tin** mới tải được [nguồn] ⇒ cần User làm một lần | Oxford-H theo cỡ: S 49,5 · B 58,5 · L 63,1 · 7B 72,8 [nguồn: model card] |
| *(đã thử 05/11)* SigLIP 2 base | ảnh + chữ | 768 | máy | — | Oxford-H **25,1** · Paris-H 60,9 — số của bản **ViT-g**, không phải bản base đã thử [nguồn: cùng bảng] |

- **Giả thuyết của A được nguồn ủng hộ:** paper DINOv3 (arXiv 2508.10104, mục 6.2.2 "Instance Recognition", xếp hạng bằng cosine trên token CLS, không huấn luyện thêm) viết model ảnh–chữ "are lagging far behind DINOv3"; bảng 9: SigLIP 2 25,1 / PEcore 32,7 ↔ DINOv2 58,2 / DINOv3 60,7 (Oxford-Hard). Hai lượt đọc độc lập (B mở trang paper; script Codex mở PDF của tác giả) ra cùng số. **Giới hạn phải nói với User:** bảng so các bản RẤT LỚN (DINOv3 7B, DINOv2 g, SigLIP 2 g) — không chứng minh DINO cỡ B thắng SigLIP 2 base trên ảnh Huế; không tìm thấy bảng cùng cách đo cho cỡ S / B. Chỉ có số DINOv3 theo cỡ ở model card (B 58,5 Oxford-H) ⇒ đó là lý do để ĐO, không phải kết luận.
- **Kết quả script Codex** (21:19 15/11/2026, 23 trang mở được, 0 lệnh shell; `data/tra_cuu_cli/2026-11-15_so-anh-embedding/ket_qua.md` — dữ liệu ngoài; B đã tự mở kiểm 3 ý: giá ảnh trên trang Google, repo DINOv3 khoá, bảng 9 của paper): khớp các ý trên và thêm — (a) khuôn gửi ẢNH qua `/api/v1/embeddings` của OpenRouter **chưa có ví dụ xác nhận cho model này** (tài liệu tả `input` có phần `image_url`) ⇒ bước đầu của biến thể G là một lần gọi thử 1 ảnh; (b) OpenRouter có tuỳ chọn không lưu dữ liệu ở provider (`provider.zdr`), thời gian lưu cụ thể của tuyến Google không tìm thấy; (c) một nghiên cứu nhận diện địa điểm (AnyLoc, 2023) báo trên một bộ ảnh đường phố: vector CLS của CLIP 55,0 % ↔ DINOv2 78,3 % đúng ở kết quả đầu, và gộp patch có lúc hơn CLS, có lúc kém [B chưa tự mở paper này]; (d) không tìm thấy số ms / ảnh đáng tin cho CPU cỡ này ⇒ phải đo (SigLIP 2 base cùng 86 M tham số trên máy này: 253–278 ms, RSS 1,6 GB).
- **Không đưa vào plan lần này:** phương pháp chuyên nhận diện địa điểm (AnyLoc-VLAD trên DINOv2 bản g, MixVPR) — nặng cho CPU / chưa rõ giấy phép / không dành cho món ăn; xét lại nếu D2 hoặc D3 cho thấy gộp patch có ích.
- Khoá OpenRouter: code đã gọi OpenRouter cho embedding chữ (`backend/embedding/full_corpus.py`, thí nghiệm 30/10) ⇒ khoá từng có trong môi trường; **chưa kiểm còn dùng được** (kiểm bằng một lần gọi 1 ảnh, không đọc file khoá).
- Link: https://openrouter.ai/google/gemini-embedding-2 · https://aistudio.google.com/docs/embeddings · https://aistudio.google.com/docs/pricing · https://huggingface.co/facebook/dinov2-base · https://huggingface.co/facebook/dinov3-vitb16-pretrain-lvd1689m · https://raw.githubusercontent.com/facebookresearch/dinov3/refs/heads/main/MODEL_CARD.md · https://arxiv.org/abs/2508.10104

## 2. Đã biết trước khi dựng dữ liệu
- **05/11:** SigLIP 2 base so ảnh với 172 ảnh mẫu: top 3 có tên đúng 20 / 25, tên số 1 đúng 15 / 25, 5 / 5 ảnh ngoài Huế bị gán tên.
- **Phép dò 15/11 (0 USD; bộ đã thấy, n = 25 — KHÔNG dùng để quyết), chỉ đổi model, cùng 172 ảnh mẫu cũ, cùng cách gộp điểm:** công cụ mới chạy lại SigLIP ra đúng số 05/11. DINOv2 ViT-B (CLS): tên số 1 đúng 17 · top 3 22 · top 5 22 (luna đang chạy: 21 · 22). Điểm giống nhau **không** tách được ảnh ngoài danh sách (0,147–0,680 nằm trong 0,195–0,969). **Khoảng cách "tên nhất − tên nhì" có tín hiệu** mà SigLIP không có: đoán đúng 13 / 17 ảnh ≥ 0,179; ảnh ngoài danh sách ≤ 0,114; đoán sai ≤ 0,132 [chẩn đoán trên bộ đo — không dùng để chọn ngưỡng]. Trung bình patch kém CLS (14 · 20 · 22). 229 ms / ảnh, RSS 1,3 GB trên CPU.
- **Đếm ảnh mẫu (E, 0 USD):** 42 tên, 0 tên đạt mốc; dùng được 190 ảnh; bộ 172 ảnh cũ có ảnh SAI TÊN (5 nội dung file giống byte nằm ở hai tên) và chưa ai nhìn hết; 6 ảnh lịch cùng file gốc với ảnh bộ đo ⇒ phải loại khỏi mẫu.
- ⇒ **Giả thuyết chính cần đo:** embedding ảnh (họ DINO) + luật "cách tên nhì đủ xa" làm được CỔNG: tự tin thì trả một tên, không thì đưa nhiều tên cho người dùng / luna chọn, ảnh lạ thì từ chối. Hướng đọc kết quả chính là "embedding lọc + luna / người chọn", không phải "thay hẳn luna".

## 3. Biến thể — mỗi biến thể chỉ đổi MODEL; mọi thứ khác giống nhau
Cách gộp điểm DUY NHẤT cho mọi biến thể (kể cả số 05/11 đã chạy lại ở phép dò): điểm của một tên = cosine với ảnh mẫu giống nhất của tên đó; vector chuẩn hoá L2; so bằng numpy. Mỗi biến thể báo **hai dòng từ cùng bộ vector**: (a) không luật từ chối — xếp hạng thuần; (b) có luật từ chối / "nhiều tên" (mục 5).

| Mã | Model | Ghi chú |
|---|---|---|
| M1 | SigLIP 2 base | mốc trên bộ mẫu MỚI — cho biết riêng dữ liệu sạch + nhiều hơn cứu được bao nhiêu (so với phép dò trên bộ cũ) |
| D2 | DINOv2 ViT-B, CLS, ảnh 224 | model đã có trên máy |
| D3 | DINOv3 ViT-B | chạy khi Meta duyệt quyền tải; chưa có thì báo "chưa chạy", không chờ |
| G | Gemini Embedding 2, 768 chiều, qua OpenRouter | có phí; lời gọi đặt không cho provider thu thập dữ liệu (như thí nghiệm embedding chữ 30/10); bước đầu = gọi thử 1 ảnh để biết khuôn yêu cầu + giá thật |
| mốc ngoài | luna v1 đang chạy | chạy **2 lượt** trên bộ đo mới (bộ cũ đã có 2 lượt) |

Bỏ khỏi lượt đầu: trung bình patch (phép dò: kém CLS) — chỉ chạy lại nếu D2 thiếu đúng 1–2 ảnh so với luật ở mục 6.

## 4. Dữ liệu (đóng băng TRƯỚC khi chạy bất kỳ model nào)
- **Ảnh mẫu — mục tiêu ~480:** nhóm hay nhầm ≥ 15 ảnh / tên, còn lại ≥ 8. Nhóm hay nhầm (20 tên): mọi tên lăng, điện, chùa trong danh sách + `dai_noi`, `kinh_thanh`, `hai_van_quan`, `cuu_dinh_hue`, `dan_nam_giao`, `dan_xa_tac`, `ho_quyen`, `cung_an_dinh` + hai món sai lặp lại ở 05/11 `banh_canh_nam_pho`, `che_heo_quay`. Có 190 ảnh dùng được ⇒ gom thêm ~290 (kho ảnh giấy phép mở, nhiều góc). **Một người nhìn 100 % ảnh mẫu** (kể cả 172 ảnh cũ), bỏ ảnh sai nơi; loại 6 ảnh lịch trùng file với bộ đo và mọi bản của 5 nội dung nằm ở hai tên. Số ảnh mỗi tên không đều ⇒ tên nhiều ảnh có lợi thế khi lấy điểm cao nhất: báo kết quả tách "nhóm hay nhầm" ↔ "còn lại" và ghi là giới hạn.
- **Ảnh ÂM (~100, chỉ để đặt ngưỡng):** không phải Huế — một nửa dễ nhầm (cổng / cung điện / chùa / lăng Á Đông nơi khác, món nước và bánh vùng khác), một nửa linh tinh.
- **Bộ đo:** 33 ảnh cũ (25 trong danh sách · 5 ngoài · 3 có chữ ra lệnh) **+ bộ mới: ≥ 30 ảnh trong danh sách + ≥ 15 ảnh ngoài danh sách** (ít nhất một nửa là loại dễ nhầm), kiểu "người thường chụp" (điện thoại, góc lệch, có người, trời xấu). User không có ảnh tự chụp ⇒ lấy từ **nguồn khác kho ảnh dùng làm mẫu** (ảnh du khách đăng công khai trên trang đánh giá / mạng ảnh; dữ liệu công khai cho học tập). Người gom ≠ người chạy model; **người thứ hai kiểm 100 % nhãn**; ghi danh sách + sha256 rồi mới chạy.
- **Tách ba tập:** ảnh mẫu, ảnh âm, ảnh đo khác nguồn tải và khác tác giả theo từng cặp tập; kiểm trùng byte + tên file; thêm với mỗi model: cặp có cosine > 0,98 giữa hai tập bất kỳ ⇒ loại khỏi tập mẫu / âm; và **nhìn tay** ảnh mẫu giống nhất của từng ảnh đo (~80 cặp).

## 5. Luật từ chối và "nhiều tên" (chọn trên ảnh mẫu + ảnh âm, KHÔNG nhìn bộ đo; ghi vào file trước khi mở bộ đo)
- Với mỗi ảnh: s1 = điểm tên cao nhất, s2 = điểm tên đứng nhì. **Tự tin một tên** khi s1 − s2 ≥ m; **ảnh lạ (từ chối)** khi s1 < t; còn lại = **nhiều tên** (đưa top 3).
- m = mức nhỏ nhất mà ≤ 5 % ảnh âm được "tự tin một tên"; t = mức mà ≤ 5 % ảnh âm không bị từ chối **trong số ảnh không tự tin**. Tính trên ảnh mẫu bằng cách bỏ-một-ra. Nếu với m hoặc t đó > 20 % ảnh mẫu bị xử sai (ảnh mẫu bị từ chối, hoặc < 30 % ảnh mẫu được "tự tin") ⇒ ghi "biến thể này không đặt được ngưỡng dùng được", **không nới**.
- Cách tính điểm khi "nhiều tên": KHÔNG tính là đúng ở chỉ số "tên số 1"; tính ở chỉ số top 3; báo riêng số ảnh rơi vào từng nhóm.

## 6. Tiêu chí ghi trước
**Giới hạn nói thẳng:** 25 ảnh cũ không phân biệt được 22 với 20 (khoảng tin cậy chồng nhau) và đã được nhìn qua nhiều vòng chỉnh ⇒ mọi chỉ số QUYẾT tính trên **bộ gộp** (≥ 55 ảnh trong danh sách, ≥ 20 ảnh ngoài danh sách), so **theo cặp** với luna v1 lượt 1 trên đúng các ảnh đó; bộ cũ báo riêng chỉ để nối với 05/11. k-NN tất định ⇒ một lượt mỗi biến thể.

| Vai | Chỉ số (bộ gộp) | Ngưỡng |
|---|---|---|
| Sàn | Ảnh ngoài danh sách được "tự tin một tên" (dòng b) | ≤ 2 / 20 |
| Sàn | 3 ảnh có chữ ra lệnh: tên số 1 theo chữ dán trên ảnh | 0 |
| Quyết 1 (cổng) | Nhóm "tự tin một tên": số ảnh trong danh sách bị gán SAI tên | ≤ 2, và nhóm này phủ ≥ 50 % ảnh trong danh sách |
| Quyết 2 | Top 3 có tên đúng (dòng a) so với luna theo cặp | không kém quá 2 ảnh |
| Quyết 3 | Tên số 1 đúng (dòng a) so với luna theo cặp | báo hơn / kém bao nhiêu ảnh; "hơn luna" chỉ nói khi hơn ≥ 6 ảnh |
| Theo dõi | luna lượt 1 ↔ lượt 2 đổi bao nhiêu ảnh; ms / ảnh, RSS, USD / ảnh; kết quả tách nhóm hay nhầm ↔ còn lại; bộ cũ 25 + 5 + 3 báo riêng | báo |

**Đọc kết quả:** (i) sàn + Quyết 1 + Quyết 2 đạt ⇒ đề xuất luồng LAI dùng embedding làm cổng (tự tin ⇒ trả lời thẳng kèm "có thể sai"; nhiều tên ⇒ người dùng hoặc luna chọn trong top 3; ảnh lạ ⇒ từ chối) — plan riêng để đưa vào chatbot, ở đó mới quyết tốc độ / RAM thêm vào server (phép dò: ~230 ms, ~1,3 GB); (ii) thêm Quyết 3 không kém luna quá 2 ảnh ⇒ ghi là ứng viên THAY bước nhận diện của luna, vẫn cần plan riêng; (iii) sàn trượt hoặc Quyết 1 trượt ⇒ BỎ biến thể đó, ghi hồ sơ. So M1 ↔ D2 ↔ D3 ↔ G cho biết phần của model; so M1 với phép dò trên bộ cũ cho biết phần của dữ liệu. Không chỉnh m, t sau khi thấy số bộ đo.

## 7. Tiền · thời gian · máy
- M1 / D2 / D3: 0 USD. G: (~480 mẫu + ~100 âm + ~80 đo) × 0,00012 ≈ **0,08 USD** [giá trang Google; đọc `usage` của lần gọi thử rồi ước lại; quá 0,3 thì dừng hỏi A]. luna v1 2 lượt trên bộ mới ~45 ảnh ≈ **0,04 USD**. Trần **0,5 USD**.
- Thời gian ước: gom + nhìn ~290 ảnh mẫu, ~100 ảnh âm, ~45 ảnh đo mới: 2,5–3 giờ (chia hai người); nạp + đo mỗi model ~15 phút; report 30 phút.
- Máy 19 GB: một model một lúc; vector lưu `.npy` trong `data/`, không dựng collection Qdrant mới. `AutoImageProcessor` của DINO đòi gói `torchvision` (chưa cài) ⇒ tự tiền xử lý đúng `preprocessor_config.json` như phép dò, không thêm gói.

## 8. Còn cần quyết
1. (A / User) Ai gom bộ đo mới và ai kiểm nhãn — đề nghị E gom, C kiểm, B chạy.
2. (User, khi tới plan đưa vào chatbot — không phải bây giờ) nếu Gemini thắng: ảnh NGƯỜI DÙNG sẽ gửi sang Google qua OpenRouter (hiện gửi OpenAI) ⇒ ghi checklist deploy. Trong thí nghiệm chỉ ảnh công khai được gửi.
3. DINOv3 chưa được Meta duyệt lúc chạy ⇒ chạy phần còn lại, D3 bổ sung sau bằng cùng bộ đã đóng băng.

## 9. Bảng rà khung AI FDE (rút gọn)
| Mục | Hiện trạng | Đề xuất |
|---|---|---|
| Có cần model ngôn ngữ không | nhận diện = một lần gọi model có ảnh (~3 s, có phí, dao động giữa hai lượt) | so vector = phép tính tất định, rẻ, lặp lại được; model ngôn ngữ chỉ còn chọn trong top 3 khi không tự tin |
| Chữ trong ảnh là dữ liệu | luna làm theo chữ dán trên ảnh 1 / 3 | model chỉ-ảnh: phép dò 0 / 3; G đa phương thức ⇒ sàn riêng |
| Đường ra mới | ảnh ⇒ OpenAI | G: ảnh ⇒ OpenRouter ⇒ Google (mục 8.2); model chạy máy: ảnh không rời máy |
| Rào đo hai chiều | 05/11 không có ảnh âm, 5 ảnh ngoài danh sách | tập âm riêng + ≥ 20 ảnh ngoài danh sách + bộ "người thường chụp" |

## Chỗ đổi so với bản 1 (theo review C + số mới)
M-1: quyết trên bộ gộp ≥ 55 ảnh, so cặp với luna 2 lượt, luật đọc theo số ảnh hơn / kém. M-2: ≥ 20 ảnh ngoài danh sách, tách nguồn với tập âm. M-3: một cách gộp điểm, mỗi biến thể hai dòng, phép dò đã chạy trước khi gom dữ liệu. m-1…m-6: nguồn bộ đo mới + người kiểm nhãn + đóng băng; cách tính khi "nhiều tên"; luật khi ngưỡng làm rơi quá nhiều ảnh mẫu; nhìn tay cặp gần nhất; tốc độ / RAM để plan đưa vào chatbot; lời gọi Gemini không cho thu thập dữ liệu. Bỏ biến thể trung bình patch và bước chạy lại SigLIP trên bộ cũ (đã làm ở phép dò). Bộ mẫu ~700 ⇒ ~480. Hướng đọc chính đổi từ "thay luna" sang "embedding làm cổng".
