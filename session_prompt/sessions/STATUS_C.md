# STATUS_C — ghi đè 22:38 22/11/2026 (giờ `date`), phiên C mở 21:26 22/11 sau khi máy khởi động lại (terminal `hue-rag-72`; điều phối `hue-rag-ea`, B `hue-rag-f3`, phiên đo `hue-rag-74`). C giữ LÀN GIAO DIỆN (việc X13). Sha ghép `origin/p13-c-man-dau-cao` `10c30bc5` đã gửi phiên đo cho CỔNG GỘP — chưa có kết quả cổng lúc ghi

Từ dùng: *bến* = nút tròn mang một lối vào, nằm trên nét sông · *màn đầu* = khối đầu Trang chủ (sông + cột chữ) · *dựng tĩnh* = `vite build` ra thư mục tạm, trình duyệt không đầu mở, mọi `/api/*` do một máy chủ tệp nhỏ trả bằng dữ liệu mẫu (không server sản phẩm, không model) · *cổng gộp* = lúc phiên điều phối gộp giao diện mới vào main, sau khi phiên đo báo đạt. Bản sổ trước: `git show 9b45acda:session_prompt/sessions/STATUS_C.md`.

0. **ĐỌC TRƯỚC — đang ở đâu.**
   - **Sha ghép** = `551d02f` + `da8bff0` (màn đầu vừa một khung nhìn máy xách tay) + `ec8fb7a` (thẻ chờ ở điện thoại + bốn chữa nhỏ) + `10c30bc5` (commit `99b74b3` của B về `lkh.css`, C đọc diff rồi cherry-pick). Main vẫn giao diện CŨ.
   - **Việc đầu của phiên C mở lại:** đọc kết quả cổng của phiên đo trên `10c30bc5` (phiên đo nhắn thẳng; file ở `data/giao_dien_2026-11-22/`) ⇒ có lỗi chặn thuộc `song/*`, `chat.jsx`, `tl.css`, `hieu_ung.css` thì chữa trên NHÁNH CON MỚI tách từ `10c30bc5` (phiên điều phối đóng băng chuỗi này lúc 22:4x), báo sha mới cho phiên đo + B. `lkh.css` là của B đợt này.
   - **Không file nào đang sửa dở.** Cây `/tmp/hr_c_cao` đứng trên `p13-c-man-dau-cao` `10c30bc5`, sạch (trừ liên kết `frontend/node_modules` và `frontend/dist` chép từ bản dựng tạm — cả hai không vào git).

1. **Phải biết trước khi sửa lớp nhìn (mỗi dòng là một lỗi đã vấp tối nay):**
   - **Lớp `.answer` dùng ở BA nơi:** câu trả lời chat, khối "Từ web" trong chat, và TRANG MỘT BÀI của Khám phá (`article.ct-bai.answer`). Mọi luật `.answer` trong `song/song.css` mang `:not(.ct-bai)` — luật mới thêm phải giữ như vậy, không thì bài bị bó cột 64 ký tự và bảng giá vỡ.
   - **Tiêu đề phần trong câu trả lời** = lớp `.dau-muc` do `song/nhin.js` (`trangTriTraLoi`) gắn khi CẢ đoạn là một cụm in đậm. Đừng quay lại `strong:only-child` của CSS: nó không thấy chữ thường quanh cụm đậm.
   - **`html .bubble`** (đệm 20 / 24 px, bóng) ăn vào chín nơi dùng `.bubble` (thẻ lỗi, hai thẻ hỏi lại, thẻ chọn tên ảnh, khối web, thẻ lịch); riêng trợ lý nổi giữ đệm cũ vì `.chat .bubble` mạnh hơn. `html .searching`, `html .nguon*`, `html .notice-an-toan` cũng hiện trong trợ lý nổi và trên thẻ lịch.
   - **Màn đầu Trang chủ theo bề rộng** (`song/Song.jsx` hằng `MAN_DOC` + khối màn đầu trong `song/song.css` — hai mốc PHẢI trùng): ≤ 1140 px bố cục DỌC (tiêu đề ⇒ ô hỏi ⇒ sông sáu bến ⇒ câu gợi ý ⇒ thời tiết; 761–1140 px canh giữa trong cột 680 px) · 1141–1340 px nhãn bên phải bến tự thu theo chỗ còn lại (biến `--cho` tính trong `tinh()`) · > 1536 px hình sông giữ cỡ 1536 px, neo mép phải · bến thứ năm đứng ở mũi nhọn của bờ nên nhãn lùi xa (`.h1-ben-4 .h1-nhan`), nhãn bến cuối nhích lên (`NHAN` = "tren"), `T_RONG` cuối = .95.
   - **Thanh trên** (`index.css`): 761–1100 px tên ngắn + thu khe; 761–900 px chỉ còn logo (tên ẩn khỏi mắt, còn cho trình đọc màn hình); nền thanh đặc. Sáu mục (có "Bản đồ") vừa ở 768 px.
   - **Bản in lịch** phụ thuộc bề dài thanh trên và cỡ chữ màn hình; B đã ghim trong khối in của `lkh.css` (`body { min-width: 1019px }`, 21 cỡ chữ in). Đổi thanh trên / cỡ chữ / bề rộng ⇒ IN THỬ ra PDF, so số trang.
   - **Thang cỡ chữ** (`@theme` của `index.css`): `--text-chu-thich` 13 · `--text-nho` 14 · `--text-phu` 15 · `--text-than` 17 (màn ≤ 760 px: 16) · `--text-dan` 19 · `--text-tieu-de-nho` 22 · `--text-tieu-de` 28 · `--text-h2` 34 · `--text-trang` 44 · `--text-h1` `clamp(40px, 4.6vw, 62px)`. Ngoài thang, cố ý: bản in, số lớn trang Giới thiệu (72 / 56 px), hai tiêu đề `clamp` của Chỗ ở và Khám phá.
   - **Màn đầu theo CHIỀU CAO (mới, `da8bff0`):** `.h1-hero` có biến `--cao` = `clamp(520px, 100vh − mép trên màn đầu, 800px)`; mép trên do `Song.jsx` đo và đặt vào `--h1-tren` (69 px ở màn rộng). Cỡ tiêu đề, đệm trên, khoảng cách của cột chữ và hai độ lệch nhãn (`.h1-nhan-tren`, `.h1-ben-4`) đều nhân theo `--cao`; ở 800 px mọi số bằng bản trước. Bề dày nét sông = 250 px × (chiều cao màn đầu / 800) — tính trong `tinh()`, cũng là nửa khoảng lùi của bến ra bờ.
   - **Bến chỉ còn TÊN** (ẩn `small`) khi khung nhìn thấp hơn 869 px hoặc hẹp hơn 1361 px (một khối `@media` trong `song.css`). ĐỪNG nới ngưỡng này bằng tay: đã thử ba cách giữ dòng mô tả ở màn thấp — ngưỡng rộng × cao (lọt ở 1250 × 680, 1321 × 669, 1381 × 690), trang tự đo va chạm bằng JS (đúng với cột chữ nhưng không thấy chữ chạm ẢNH), thêm phép đo "chạm dải sông" (tắt mô tả ở MỌI cỡ vì thiết kế gốc đặt nhãn cách bờ chỉ 1–3 px). Muốn có mô tả ở máy demo ⇒ phải vẽ lại vị trí hai bến cuối (chúng chung một khoảng nền hẹp giữa hai khúc sông).
   - **`ch` trong `max-width` của tiêu đề màn đầu không theo nét chữ thật** (ra 0,5em): `13ch` = 6,5em sát bề rộng dòng "người bản xứ", ở vài cỡ chữ rơi thành bốn dòng ⇒ nay `6.7em`.
   - **`.tl-chat` có `overflow: hidden`** ⇒ (a) trình duyệt cắt lề cuộn của `.turn` theo hộp này: `scroll-margin-top` lớn hơn 110 px không có tác dụng; (b) `position: sticky` của ô nhập không dính đáy màn hình — ô nhập luôn nằm cuối khung chat. Đổi thành `overflow: clip` sẽ chữa cả hai nhưng là đổi hành vi (ý đã gửi phiên điều phối cho `Y_CHUA_THU.md`).
   - **Khối hiện dần khi cuộn** (`hieu_ung.css`, `.hien`): khoảng chạy nay tính bằng px (`entry 0px` ⇒ `entry 160px`, so le 16 px), không còn theo % quãng đi qua màn.

2. **Kiểm đã chạy trên `10c30bc5` ↔ chưa (bản dựng tĩnh + dữ liệu mẫu):**
   - Màn đầu nằm trọn khung nhìn (sáu bến + nhãn, ô hỏi, dòng thời tiết, nút dừng; không đè cột chữ, không đè nhau): 0 lỗi ở 1536 × 695 · 1536 × 730 · 1366 × 650 · 1280 × 620 và khoảng 30 cỡ khác (1141–2560 rộng, 600–1300 cao), cả lượt có chuyển động. Ca đối chứng: cùng phép kiểm ĐỎ trên `551d02f` ở cả bốn cỡ. Dưới 589 px chiều cao (màn đầu chạm sàn 520 px) dòng thời tiết bị cắt — ngoài phạm vi.
   - 21 bề rộng 360–2560 (cao 800): 0 tràn ngang, 0 bến / nhãn cắt hay đè.
   - Tương phản: 1.850 phép đo, 0 dưới ngưỡng — LẦN ĐẦU có sáu cỡ máy xách tay (`HUE_MAN_DAU=…`); công cụ cũ kéo khung nhìn bằng chiều cao cả trang nên chỉ đo màn đầu ở dạng 800 px.
   - Đếm dòng 7 màn × 6 bề rộng so với `551d02f`: 0 ô thêm dòng, 8 ô bớt dòng (Lên kế hoạch 1200 / 1440, nhờ bản của B).
   - Lúc chờ, tin gia đình: ô nhập + nút "Dừng" trong khung nhìn ở 390 × 844 (trước: ô nhập ở y 871, thanh đáy ở 780), 1536 × 695, 1366 × 650, 1280 × 620.
   - `tests/test_static_ui.py`: 4 đạt (chép bản dựng tạm vào `frontend/dist` của cây).
   - **CHƯA kiểm:** mọi thứ trên server thật · cảnh A01 (thẻ chọn tên ảnh) — sửa bằng đọc code, bản tĩnh không có đường nhận ảnh · khe thẻ từ chối ↔ khối web (H06) · bản in PDF · `test_anh_tra_loi.py`, `test_ban_do_lich.py` (cần `data/` trong cây) · khối hiện dần trên Giới thiệu / Lên kế hoạch khi cuộn thật · điện thoại nhỏ 360 × 740 lúc chờ (ô nhập còn sát đáy trong bản tĩnh).

3. **Điểm còn mở của làn (đã báo phiên điều phối 22:3x; chưa ai giao):**
   - **Phiên điều phối đã quyết (22:4x):** bến chỉ còn tên ở máy demo — CHƯA nhận, chưa bác, quyết sau khi nhìn ảnh cổng; nếu trông trống thì "vẽ lại vị trí hai bến cuối" là việc đầu sau cổng (không chặn gộp) · đóng khung cảnh báo bão / lũ trong câu trả lời: KHÔNG làm (vùng chữ an toàn) · đưa nguồn lên trước ảnh: không làm đợt này · các điểm thẩm mỹ dưới đây: danh sách sau cổng · ý đổi `overflow` của khung chat: vào `Y_CHUA_THU.md`, làm sau cổng với một lượt nhìn riêng.
   - Khung chat dính sát thanh trên sau câu hỏi ĐẦU ở màn cao (`so_cap/NHOM_2`, HỎNG-MỚI nhẹ) — đã ghi giới hạn ở `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 (hàng cuối); xem mục 1 dòng `.tl-chat`.
   - Hình sông: mũi nhọn ở khúc uốn trong (nét dày tự cắt) + nét đứt trắng "giống vạch đường" (hai bản Gemini) — thẩm mỹ, phải vẽ lại hình.
   - Thanh trên sáng ghép thẳng vào đầu trang tối ở Khám phá / Giới thiệu / Lên kế hoạch; vòng trắng của logo chìm vào thanh sáng.
   - Cảnh báo bão / lũ trong câu trả lời chưa đóng khung như trên lịch (chạm vùng chữ an toàn ⇒ phiên điều phối quyết) · đưa nguồn lên trước ảnh (đổi thứ tự ⇒ phiên điều phối quyết).
   - Bố cục dọc (≤ 1140 px) ở cửa sổ thấp như 1024 × 768: bến cuối dưới màn đầu; điện thoại: câu gợi ý + thời tiết nằm dưới sông (chủ ý của hướng đã chốt).
   - Danh sách đủ: `data/giao_dien_2026-11-22/phe_binh_rut/RUT_GPT.md`, `RUT_NEON.md`, `RUT_CARBON.md` (101 điểm; kết luận của agent con là [chưa kiểm] trừ bốn cảnh C tự mở ảnh) + các ý cũ ở bản sổ trước mục 3.

4. **Ai chờ mình ↔ mình chờ ai:** C chờ kết quả cổng của phiên đo trên `10c30bc5`. Không ai chờ C.

5. **Bộ kiểm 0 đồng** (riêng tư, `data/giao_dien_2026-11-22/thu/`; chạy từ `backend/` bằng `uv run --no-sync python`; dựng: `ln -s <cây chính>/frontend/node_modules` vào `frontend/` của cây nhánh, `./node_modules/.bin/vite build --outDir /tmp/hr_c_cao_dist --emptyOutDir`):
   - `chup_rong.py <dist> <thư mục ra> <đường> <khổ,khổ,…> <cổng>` — khổ `1280` (cao 800, không xét đáy) hoặc `1280x620` (xét cả mép ĐÁY khung nhìn đầu); đường `/` in bến / nhãn cắt, đè, số dòng tiêu đề, đáy cột chữ; `HUE_CHUYEN_DONG=1` = không bật giảm chuyển động (mới thấy nút dừng); đường `/tro-ly!cho` (+ `HUE_CAU="<câu hỏi>"`) = giữ lượt ở lúc chờ 12 giây, in ô nhập / nút "Dừng" có trong khung nhìn không; `/tro-ly!hoi` = câu trả lời xong.
   - `do_tuong_phan.py <dist> <ra.json> <cổng>` với `HUE_MAN_DAU=1536x695,1280x620,…` = đo thêm màn đầu ở đúng các khung nhìn đó.
   - `dem_dong.py do|so`, `so_trang.py chup|so`, `bang_tuong_phan.py` — như bản sổ trước.
   - Cổng C dùng: 8061.

6. **Thứ đang chạy / rác** (kiểm 22:38 22/11/2026): 0 tiến trình của C, 0 agent con đang chạy. Cây: `/tmp/hr_c_cao` (nhánh giao diện), `/tmp/hr_c_so` (nhánh sổ này). Thư mục tạm xoá được: `/tmp/hr_c_anh`, `/tmp/hr_c_kiem`, `/tmp/hr_c_cao_dist`, `/tmp/hr_c_cao_dist0` (bản dựng của `551d02f`, dùng làm ca đối chứng), `/tmp/hr_c_do.sh`, `/tmp/hr_c_tp.sh`. Máy khởi động lại thì `/tmp` mất hết — nhánh đã ở origin.

7. **Bẫy của phiên (mỗi dòng đã xảy ra thật tối nay):**
   - Phép kiểm vị trí sạch KHÔNG có nghĩa chữ đọc được: ở 1536 × 695 mọi hộp nhãn "không đè gì" nhưng dòng mô tả nằm trên ảnh sông — chỉ phép đo tương phản ở ĐÚNG khung nhìn đó mới thấy. Đổi hình học màn đầu ⇒ chạy cả hai.
   - Đo hình đang vẽ (`getBoundingClientRect`) lúc trang vừa tải thì sai: bến đang phóng to dần (`scale .4`), cột chữ đang trượt lên ⇒ lượt giảm chuyển động sạch mà lượt có chuyển động lỗi. Bộ kiểm phải chạy cả `HUE_CHUYEN_DONG=1`.
   - Dò ngưỡng `@media` bằng tay ba lần đều lọt ca kế bên ⇒ khi ngưỡng lọt lần hai thì dừng dò, tìm luật đơn giản hơn (ở đây: màn chưa đủ 800 px thì chỉ hiện tên).
   - Sửa script bằng chuỗi thay thế: chú thích `#` chèn trước dấu `;` nuốt mất lệnh sau nó trên cùng dòng (`CONG` không còn được gán).
   - Test đọc mã giao diện chạy trong cây tạm cần `frontend/dist` (chép bản dựng tạm vào) và `data/` (không có ⇒ hai file không chạy được, không phải lỗi bản sửa).
   - Agent con rút điểm từ ba bản phê bình: bản phê bình viết trên `e27398d` / ảnh `sau_e98c42f`, ba điểm nó xếp nặng nhất đã hết ở `551d02f` — luôn đối chiếu với ứng viên mới nhất trước khi tính là mở.
