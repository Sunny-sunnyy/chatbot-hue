# Review gộp: (a) thí nghiệm Serper ↔ Exa · (b) plan nháp đưa Exa vào sau cờ — một vòng

Decision: **(a) kết quả đứng theo luật ghi trước — `ready` kèm một giới hạn phải ghi thêm; (b) plan `changes_requested`** (2 major, 5 minor; sửa chữ là đủ, A đọc bản sửa rồi duyệt)
Người kiểm: C (`hue-rag-e1`, Claude Code — Fable 5.2)
Date: 21:19 12/11/2026 (`date`)
Bản được review: `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` mục 5–6 (commit `6e12159`) + dữ liệu private `data/exa_2026-11-12/`;
`docs/superpowers/plans/2026-11-12-tra-web-exa-plan.md` sha256 `570805aa2a78` (người viết cả hai: E).

## 1. Phạm vi đã review

- Bốn điểm A dặn cho (a): cấu hình có ghi trước khi chạy không · chấm có mù không · đếm lại 25 / 17 từ file chấm · sàn.
- (b): Exa trước / Serper dự phòng trong hạn 5 s · trần lượt / ngày · luật kiểm giữ nguyên · khoá thiếu · test · tiêu chí bật.
- Chỉ đọc file + script đếm của C (0 USD, không gọi Exa / Serper); một lần WebFetch một trang công khai để hiểu một loại nguồn (mục 2, F-1). Không chạy lại thí nghiệm.

## 2. Findings

### (a) Thí nghiệm

**F-1 (giới hạn phải ghi thêm vào report; ảnh hưởng độ chắc của kết luận, không lật luật ghi trước) — 5 / 25 mục "đạt" của Exa có trích nguồn là trang địa điểm của chính nhà cung cấp**
- **Bằng chứng (C đếm trên `ket_qua/exa.jsonl` + lô chấm):** 7 / 109 kết quả Exa trả về có tên miền của chính Exa (đường dẫn dạng "thư viện địa điểm"); 5 mục trong 27 mục Exa được chấm
  có trích loại nguồn này (2 câu ăn gần + 3 câu B6), **cả 5 đều "đạt"**; không mục nào chỉ dựa riêng vào nó. C mở thử một trang: công khai, là trang tổng hợp một cơ sở (địa chỉ, giờ mở,
  điểm đánh giá, nhận xét, số điện thoại), **không ghi dữ liệu lấy từ đâu**. Bên Serper không có loại nguồn này.
- **Độ nhạy:** loại cả 5 mục ⇒ Exa **20** < ngưỡng 22 (17 + 5); giữ nguyên ⇒ 25. Cấu hình có lọc mạng xã hội: 20 ⇒ 16.
- **Vì sao không lật kết luận:** luật ghi trước không loại tên miền nào, và 5 mục đó còn trích nguồn khác. Nhưng report mục 6 viết "nguồn mạng xã hội 0 / 109" mà không nói có 7 nguồn
  là trang của chính nhà cung cấp ⇒ người đọc hiểu Exa trả toàn trang gốc.
- **Tiêu chí đóng:** report thêm một dòng số đếm này + phép độ nhạy 25 ⇒ 20; plan phải quyết cách xử loại nguồn này (M-2 dưới).

**Đếm lại — khớp:**

| Điểm kiểm | E báo | C đếm lại | Kết quả |
|---|---|---|---|
| Mục "đạt" (cả hai người chấm) Serper · Exa · Exa lọc | 17 · 25 · 20 | 17 · 25 · 20 (từ `cham_nguoi_1/2.jsonl` + `khoa.json`) | khớp |
| Hai người chấm khớp nhau | 77 / 80 | 77 / 80; riêng từng người: 17 / 26 / 21 và 17 / 25 / 21 | khớp |
| Mục lọt ra mà kiểm cuối có lỗi (sàn) | 0 · 0 · 0 | 0 / 28 · 0 / 27 · 0 / 25 | khớp |
| Có mục web · không tin cậy · chưa xác minh · thiên tai · lỗi tra | bảng mục 6 | 28·9·3·1·1 · 27·10·4·1·0 · 25·13·2·1·1 | khớp |
| Thời gian tra p50 / p95 | 2,0 / 3,1 · 1,6 / 2,2 · 1,8 / 4,0 s | 2,02 / 3,08 · 1,60 / 2,24 · 1,85 / 4,02 s | khớp |
| Chỉ Exa đạt · chỉ Serper đạt | 10 · 2 | 10 · 2 (kiểm dấu hai phía trên 12 cặp lệch: p ≈ 0,04) | khớp |

**Ghi trước — đạt, với một lưu ý:**
- Tiêu chí (chỉ số quyết "+ 5", sàn, p95 ≤ 5 s, luật giữ / gỡ) **có trong commit `e241b3c` lúc 20:52**, trước lượt chạy đầu (file kết quả Serper 21:02). ⇒ ghi trước có bằng chứng git.
- Cấu hình Exa (mục 5, 20:59) và cấu hình thứ hai + mốc Serper (mục 5b, 21:03) chỉ vào git ở commit 21:17 — **sau** khi có kết quả. Bằng chứng gián tiếp vẫn khớp: công cụ đo
  `do_exa.py` (sửa lần cuối 21:03:45, trước lượt Exa 21:06) chứa đúng `type auto`, 5 kết quả, `userLocation VN`, đoạn trích 400, hạn 5 s, và danh sách tên miền loại trừ của cấu hình 2.
  ⇒ C chấp nhận; **minor cho lần sau:** commit phần ghi trước **trước** khi chạy lượt có phí (một commit nhỏ là đủ).
- Bộ đo 44 ⇒ 42 câu và ngưỡng giữ "+ 5": ghi ở mục 5 trước khi chạy; ngưỡng không nới ⇒ được.

**Chấm mù — mù một phần, đủ dùng cho kết luận này:**
- Đúng thủ tục: 80 mục ba bên trộn một lô (thứ tự xáo — 20 mục đầu xen kẽ các bên), khoá để riêng, đề chấm cấm mở khoá, hai người chấm độc lập, tiêu chí hai nhãn rõ.
- **Lộ bên qua độ dài đoạn trích** (E đã tự ghi ở giới hạn): trung vị 148 ký tự (Serper, tối đa 213) ↔ 253 ký tự (Exa, tối đa 400). Người chấm không được nói có mấy hệ thống, nhưng đoán được.
  C đánh giá ảnh hưởng thấp: hai nhãn là việc đối chiếu (mục có nêu thông tin cụ thể không · mọi khẳng định có trong đoạn trích không), và phần lợi của Exa chính là đoạn trích đủ dài để
  có căn cứ — đó là hiệu ứng thật, không phải thiên vị. Không sửa được nếu không cắt đoạn trích (làm mất đúng thứ đang đo).
- **"Đạt" = khớp đoạn trích, không phải đúng ngoài đời** (E đã ghi). Với nguồn tổng hợp ở F-1 điều này quan trọng hơn bình thường.

**Kết luận (a):** Exa cấu hình không lọc **đạt luật ghi trước** (25 ≥ 22; sàn 0; p95 2,2 s). Độ chắc: một lượt, 42 câu tự viết; biên phụ thuộc vào 5 mục có nguồn tổng hợp của nhà cung cấp.

### (b) Plan đưa Exa vào sau cờ

**M-1 (major) — đường dự phòng "trong cùng hạn 5 s" gần như không chạy được ở ca hết giờ**
- **Vị trí:** plan mục 1 dòng `_tim_web_server`, mục 2, tiêu chí X5.
- **Bằng chứng:** hạn Exa = 5 s (như công cụ đo). Exa hết giờ ⇒ phần còn lại của hạn = 0 ⇒ theo chính plan "không còn thời gian ⇒ thôi" ⇒ ca hết giờ **không có** dự phòng. Ca lỗi nhanh
  (sai khoá, hết tín dụng, quá hạn mức) thì dự phòng chạy, nhưng Serper cần p50 2,0 s / p95 3,1 s (số đo hôm nay) ⇒ Exa trả lỗi sau > 2–3 s thì Serper cũng hay không kịp.
  X5 chỉ thử ca "khoá sai" (lỗi tức thì) ⇒ đạt X5 mà ca hết giờ vẫn hở.
- **Tiêu chí đóng:** plan ghi **hạn riêng cho Exa** nhỏ hơn hạn chung (vd 3 s — p95 đo được 2,2 s) để Serper còn ≥ 2 s; hoặc ghi thẳng "hết giờ ⇒ không dự phòng, ra câu cố định" và bỏ lời hứa
  ở mục 2. Thêm test ca hết giờ (model giả chậm) cho đúng lựa chọn đã ghi. Tổng thời gian tra vẫn ≤ 5 s.

**M-2 (major) — plan chưa nói gì về tiền theo sàn đã chốt, và chưa xử loại nguồn ở F-1**
- **Tiền:** plan mục 3 ghi mỗi lượt web 0,0018 ⇒ ≈ 0,008 USD nhưng không đối chiếu sàn **≤ 0,0005 USD / câu trung bình** (User chốt 28/10). Số đo hôm nay: câu Golden trong kho trung bình
  0,00042; chỉ cần ~2 % số câu đi web bằng Exa trả phí là trung bình vượt 0,0005 (0,00042 + 2 % × 0,0076 ≈ 0,00057). Trong gói miễn phí thì tiền thật không đổi, nhưng plan cho phép 150 lượt /
  ngày (> ~47 lượt / ngày của gói miễn phí). ⇒ đây là **quyết định tiền của User**, phải thành một câu hỏi rõ: (i) chỉ dùng trong hạn mức miễn phí, hết thì về Serper (trần / ngày đặt ≤ mức
  miễn phí); hay (ii) chấp nhận nâng sàn tiền cho đường web. Plan đang để lẫn hai ý.
- **Nguồn tổng hợp của nhà cung cấp (F-1):** plan phải chọn và đo: (i) giữ, nhưng nhãn nguồn hiện cho người dùng nói rõ đó là trang tổng hợp; hay (ii) loại bằng `excludeDomains` chỉ riêng tên
  miền đó. Chọn (ii) thì X6 phải đủ lớn để thấy còn hơn Serper không (xem m-1).
- **Tiêu chí đóng:** hai lựa chọn trên ghi vào plan kèm khuyến nghị; trần lượt / ngày khớp lựa chọn tiền.

**Minor**
- **m-1 — X6 yếu hơn kết quả nó cần xác nhận.** "Exa ≥ Serper trên 20 câu B6" là mức không tụt; lợi đo được hôm nay nằm cả ở 12 câu lưu trú / ăn gần. Đề nghị X6 chạy lại đủ 42 câu
  (≈ 0,05 USD + tín dụng), báo cả số "loại mục có nguồn tổng hợp"; ngưỡng: Exa ≥ Serper + 3 (một nửa biên cũ) hoặc ghi rõ vì sao chỉ cần ≥.
- **m-2 — "khoá thiếu ⇒ như hôm nay" chưa có dòng nào.** Cấu hình `exa` mà thiếu khoá Exa ⇒ phải rơi về Serper + log một dòng, không lỗi khởi động, không lỗi mỗi câu; thêm vào bảng test.
- **m-3 — đoạn trích dài hơn ⇒ lần gọi viết mục tốn hơn** (0,0078 ⇒ 0,0104 USD / 42 câu, + 33 %) và chữ đầu mục web có thể chậm hơn; X4 đo "tới sự kiện web" là đúng chỗ — ghi mốc Serper cùng buổi
  bằng số trong report.
- **m-4 — quyền riêng tư:** plan đã nêu đúng điều quan trọng nhất (nhà cung cấp dùng truy vấn để cải thiện sản phẩm). Thêm một dòng vào bài học / trang giới thiệu khi bật: câu hỏi kho không trả lời
  được sẽ gửi tới **hai** dịch vụ tìm (Exa, và Serper khi dự phòng). Trang địa điểm ở F-1 có số điện thoại cơ sở trong đoạn trích ⇒ kiểm luật hiện có (bỏ số điện thoại ở câu tìm) không áp cho
  chữ web; ghi rõ mục web được / không được in số điện thoại lấy từ đoạn trích.
- **m-5 — trần lượt / ngày đếm trong RAM:** khởi động lại là xoá sổ (như giới hạn lượt / IP) — ghi là giới hạn đã biết; trên bản nhiều tiến trình thì mỗi tiến trình một sổ.

**Điểm đạt của plan:** chỉ thay nguồn của sổ web; cổng mở, lời dặn, `kiem_muc_web` giữ nguyên; mặc định `serper` ⇒ cờ tắt = như hôm nay (X1 có Q1); một module duy nhất gọi ra web + test ranh
giới; log thêm `nguon` không chữ; không dùng cấu hình lọc (đúng theo số đo); X2 giữ đủ sàn B6 kể cả "0 truy vấn chứa tên"; X3 an toàn; bảng rà đường ra mới nêu đúng rủi ro.

## 3. Cách người kiểm chạy lại thật (0 USD)

- Script đọc `cham/khoa.json`, `cham/lo.jsonl`, `cham_nguoi_1.jsonl`, `cham_nguoi_2.jsonl`: đếm "đạt" theo bên, độ khớp, câu chỉ một bên đạt, độ dài đoạn trích theo bên, thứ tự bên trong lô.
- Script đọc `ket_qua/{serper,exa,exa2}.jsonl`: outcome, mục lọt có `kiem` khác rỗng, `tra_ms` p50 / p95, tên miền nguồn.
- `git log` + `git show e241b3c:<report>`: tiêu chí có trước lượt chạy. `ls --time-style=full-iso` thư mục dữ liệu: thứ tự thời gian file.
- `grep` cấu hình trong `data/exa_2026-11-12/tools/do_exa.py`. Một lần WebFetch một trang nguồn tổng hợp (công khai).

## 4. Giới hạn hoặc phần chưa chạy

- Không chạy lại lượt nào; không kiểm thông tin trong mục web đúng ngoài đời.
- Không đọc nội dung từng mục để chấm lại (chỉ đếm nhãn của hai người chấm) ⇒ không kiểm chất lượng chấm ngoài độ khớp 77 / 80.
- Số "~2 % câu đi web là vượt sàn tiền" dùng trung bình Golden của lượt B7; tỉ lệ câu đi web của người dùng thật chưa biết.

## 5. Decision và bước tiếp theo

- **(a)** Kết quả dùng được làm căn cứ: **Exa hơn Serper theo luật ghi trước.** E thêm vào report mục 6 một dòng về 7 / 109 nguồn tổng hợp của nhà cung cấp + độ nhạy 25 ⇒ 20.
- **(b)** E sửa plan theo M-1, M-2 (và minor tuỳ chọn); hai câu cần **User** quyết qua A: (1) dùng Exa chỉ trong hạn mức miễn phí hay chấp nhận tiền cao hơn cho đường web; (2) giữ hay loại
  nguồn tổng hợp của nhà cung cấp. Không cần vòng review thứ hai — A đọc bản sửa rồi duyệt.
