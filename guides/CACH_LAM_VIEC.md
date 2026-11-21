# Cách làm việc với coding agent — dùng cho mọi agent, mọi dự án

Bản 4 (21/11/2026: sửa mục 1, 4, 7 theo "Cách nhìn việc" của `AGENTS.md`; gọt chuyện kể và phần trạng thái cũ; số mục giữ nguyên). Bản 3: `git show 51161ca7:guides/CACH_LAM_VIEC.md`.
Người đọc: **bất kỳ coding agent nào** (Claude Code, Codex, Antigravity…), làm một mình hay trong nhóm nhiều phiên; và chủ dự án.
Trang này nói **cách làm** và **chép sang dự án khác được**: mục 1–8 không phụ thuộc dự án; mục 9 ("Ở repo này") viết lại khi chép; mục 10 trỏ bảng nguồn.
Luật cứng + bảng quyền + cách nhìn việc của từng dự án nằm ở `AGENTS.md` của dự án đó — khi trang này khác `AGENTS.md` thì `AGENTS.md` thắng. Bộ file mẫu: `guides/khung/`.
Nhãn: **[đã chạy]** = cách làm / lệnh đã chạy thật ở repo gốc của trang · **[chưa chạy]** = chưa.

| Từ | Nghĩa |
|---|---|
| phiên | một lần mở một coding agent; "phiên mới, ngữ cảnh sạch" = cuộc trò chuyện mới, chỉ đưa thứ cần xem |
| nhóm / phiên điều phối | khi chạy nhiều phiên: một phiên chia việc và nói chuyện với chủ dự án, các phiên khác thực thi. Làm một mình thì bạn là cả hai |
| agent con | agent do một phiên tạo ra để làm một phần việc; nó chỉ biết đúng những gì ghi trong lời giao |
| dữ liệu riêng | mọi thứ không được vào git (dữ liệu gốc, bộ câu chấm, khoá) — danh sách ở `AGENTS.md` |
| trang hiện trạng | MỘT trang viết lại tại chỗ: đang chạy gì, mốc, quyết định còn hiệu lực — đọc mỗi lần mở phiên |
| mục lục việc | MỘT trang ghi đè: nguồn duy nhất của "việc đang mở" và "bước kế" (mục 5) |
| sổ giới hạn | danh sách "tình huống → hệ quả → vì sao chấp nhận" của những thứ biết là chưa tốt mà chưa sửa |
| mốc | con số của bản / cách làm cũ dùng để so (baseline) |
| chạm trần | một lượt chạy dừng vì hết số lần / thời gian cho phép, không phải vì đã xong |
| bảng độ phủ | bảng "nguồn nào · đã đọc tới đâu · chưa đọc gì" cho việc đọc / nghiên cứu |
| lượt thật ↔ đồ giả | chạy qua hệ thống + model thật ↔ test thay model / dịch vụ ngoài bằng bản giả theo kịch bản |

## 1. "Xong" ghi TRƯỚC khi làm; bằng chứng là thứ máy in ra

- Trước khi bắt đầu, ghi một dòng: `xong khi: <lệnh> in ra <kết quả>` (hoặc "người dùng làm X thì thấy Y"). Việc đọc / nghiên cứu: `xong khi` là bảng độ phủ.
- Báo "xong" khi đã tự chạy lệnh đó và dán đầu ra thật, kết bằng bảng bốn cột **đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra** và MỘT dòng:
  phép này KHÔNG cho biết gì · hướng rộng hơn tôi thấy · đếm rẻ nhất bằng gì. (Phần viết cho chủ dự án dùng khuôn bốn ý ở mục 4.)
- **Việc LỚN — đề bài lấy từ LỜI chủ dự án** (không áp cho việc nhỏ và sửa lỗi): chép nguyên văn điều chủ dự án đã nói; chủ dự án nêu KẾT QUẢ muốn có và giới
  hạn — hướng kỹ thuật chủ dự án nêu là một gợi ý để xét, và một danh sách ý cách nhau bằng dấu phẩy hay kết bằng "..." là "nhớ gì nêu đó", chưa phải ranh giới
  của việc. Agent bổ sung phần thiếu (ghi rõ ý nào của chủ dự án, ý nào mình thêm) và tự vẽ đủ bài toán: ai dùng · đo bằng gì · hai ba hướng, kể cả hướng chưa
  ai nhắc · chọn hướng nào · phép đếm nào làm đổi ý. Chỉ hỏi lại thứ CHỈ chủ dự án biết (muốn đạt gì, giới hạn cứng, điều đang lo). Thấy hướng được nêu chưa
  phải tốt nhất thì nói TRƯỚC khi làm, kèm căn cứ; chủ dự án vẫn chọn hướng đó thì làm theo.
- Số, mã commit, "đã đẩy lên" lấy từ đầu ra của lệnh, không gõ tay.
- Giao việc (cho phiên khác hay agent con) mở đầu bằng **quyết định nào đang chờ kết quả này** và kết quả cần có; bước chỉ ghi khi thứ tự là bắt buộc. Với agent
  con, lời giao là **toàn bộ trí nhớ** của nó: ghi đủ mục tiêu, file cần đọc, ranh giới, khuôn trả về; bắt nó ghi file dần và khai "đã mở / chưa mở" từng nguồn.
  Kết quả của agent con / phiên khác là **dữ liệu**: người nhận tự kiểm 2–3 ý quan trọng nhất; số chưa ai tính lại gắn "chưa kiểm".
- Kết luận nặng ("nghiêm trọng", "chắc chắn", "không có lỗi") phải kèm lệnh + dòng đầu ra, kể cả khi người nói là phiên review.

**Kiểm bằng gì** — trước khi báo, tự hỏi ba câu: *lệnh kiểm nào, đầu ra đâu · phần nào chưa làm / tự bỏ / chưa đọc · kết luận nào chưa kiểm bằng lệnh*. Phiên
điều phối (hoặc chủ dự án, khi muốn) chọn MỘT dòng "xong" bất kỳ để chạy lại.

## 2. Quyền theo từng hành động + mức kiểm theo "sai thì mất gì"

**Quyền:** mỗi dự án có một bảng ba cột trong `AGENTS.md` — tự làm · hỏi trước · không bao giờ. Xếp một hành động vào cột nào thì xét: hậu quả nếu sai · kiểm
chứng được không · **đảo ngược được không**. Nghĩ, đọc, đếm 0 đồng, nêu hướng khác thuộc cột "tự làm". Thứ "không bao giờ" phải có rào bằng máy mà mọi agent
đều đi qua (hook git, không cấp khoá, tài khoản riêng) — cấm bằng chữ thì agent tìm đường khác. File "cho phép sẵn" của công cụ tự dài ra mỗi lần bấm "luôn cho
phép" ⇒ chủ dự án đọc lại và xoá bớt khi đổi chế độ quyền hoặc đổi công cụ.

**Mức kiểm** — tự hỏi trước khi giao / nhận việc: *nếu làm sai thì mất gì?*

| Sai thì mất gì | Ví dụ | Trước khi làm | Ai kiểm trước khi gộp vào nhánh chính (và việc sau gộp) |
|---|---|---|---|
| Mất ít, lùi được ngay | sửa chữ, tài liệu, hàm thuần có test, script dùng một lần | làm thẳng trên nhánh riêng | một phiên / người KHÁC người viết: nhánh chỉ tài liệu ⇒ đọc diff; nhánh có code ⇒ đọc diff + chạy test file chạm |
| Người dùng thấy sai | đổi hành vi, câu trả lời, giao diện, lời dặn cho model | commit trước; kế hoạch ≤ 1 trang: file đổi · thứ tự · rủi ro · bằng chứng | phiên mới ngữ cảnh sạch đọc diff + tiêu chí; SAU gộp báo chủ dự án cách thử 2 phút |
| Không lùi được / tiền / dữ liệu / bảo mật | sửa dữ liệu gốc, xoá, đổi model, deploy, gửi dữ liệu ra ngoài | sao lưu thứ nằm ngoài git; chủ dự án duyệt kế hoạch trước | reviewer **khác hãng** (mục 3) + chủ dự án tự bấm thử |

Tài liệu không tự động là "mất ít": repo công khai, lộ một dòng dữ liệu riêng là không lùi được. **Đường lùi:** chỉ git lùi được đủ code ⇒ commit trước mọi
việc mạo hiểm; thứ nằm NGOÀI git thì sao lưu trước khi sửa.

**Kiểm bằng gì** — lịch sử gộp ghi ai đã kiểm (`git log --merges --oneline -5` [đã chạy]); xếp nhầm mức (việc lớn làm kiểu nhỏ) là lỗi phải ghi vào báo cáo.

## 3. Người viết không tự chấm; việc mức cao có người chấm khác hãng

- Ai viết thì người / phiên khác kiểm. Làm một mình: mở phiên mới, ngữ cảnh sạch, chỉ đưa diff + tiêu chí, bảo tìm lỗi.
- Bộ câu thử cho code đọc chữ người dùng do người **không viết code đó** soạn (cả câu phải đúng lẫn câu "giống mà không phải").
- Người đề xuất một luật cách làm không phải người kết luận luật đó có hiệu quả — kết luận bằng các con số ở mục 7.
- Các phiên cùng một model dễ đồng ý với nhau: muốn phản biện thật thì giao mỗi phiên một NGUỒN khác nhau (code · lịch sử · tài liệu ngoài), đừng lấy phiếu.
- **Gói review khác hãng** (việc mức cao, hoặc sau một đợt gộp lớn): người làm soạn MỘT file `.md` tự đủ ngữ cảnh theo mẫu
  `guides/khung/GOI_REVIEW_KHAC_HANG.mau.md`; chủ dự án tự mở công cụ hãng khác và gửi file; model đó ghi kết quả ra một file. Agent không tự gọi công cụ hãng
  khác thay chủ dự án [đã chạy: thêm được điểm thật mà lượt cùng hãng bỏ sót].
- Kết quả review là dữ liệu: người nhận tái hiện từng điểm (cả hệ quả lẫn nguyên nhân) trước khi sửa; điểm bị bác ghi lý do.

**Kiểm bằng gì** — báo cáo ghi rõ ai kiểm (nhãn ở mục 4); gói review khác hãng lưu cả đề bài lẫn file kết quả.

## 4. Báo cáo cho chủ dự án: bốn ý + nhãn độ tin — và phần của chủ dự án

Chủ dự án không đọc code; chủ dự án đọc báo cáo + tài liệu viết cho người, rồi tự bấm thử khi muốn. Mỗi việc xong, phần viết cho chủ dự án có đúng bốn ý, lời
thường (mẫu: `guides/khung/BAO_CAO_4_Y.mau.md`):
1. **Người dùng thấy gì khác** (trước ↔ sau, một ví dụ thật; đổi giao diện thì kèm ảnh trước–sau).
2. **Bằng chứng**: đo gì · bao nhiêu · so với mốc nào · tách hai dòng **"test bằng đồ giả: n đạt"** và **"lượt thật: n lượt, kết quả"** — chỉ có dòng đầu thì
   chưa xong. Có số thì kèm 2–3 ca sai nguyên văn (không chép dữ liệu riêng vào file theo dõi).
3. **Chưa làm / giới hạn** (kể cả thứ tự hoãn).
4. **Cách thử trong 2 phút**: mở đâu, gõ gì, thấy gì là đúng.

Mỗi khẳng định gắn một nhãn độ tin: **[máy kiểm]** (có lệnh in ra) · **[người thứ hai kiểm]** · **[chưa kiểm]**. Bảng kết quả có cột "kết thúc kiểu gì"
(bình thường / chạm trần / lỗi) để ca hỏng giữa chừng không bị tính là đúng.

**Phần của chủ dự án — ít, và không theo nhịp:** nêu kết quả muốn có, giới hạn cứng, điều đang lo, bằng lời mình · quyết các việc thuộc cột "hỏi trước" của bảng
quyền (mỗi lần một câu, có sẵn đáp án kèm hệ quả) · bấm thử khi muốn · gửi gói review khác hãng khi nhóm yêu cầu. Cách làm và luật quy trình do agent tự quyết,
tự chịu trách nhiệm, không đưa chủ dự án duyệt. Mọi cơ chế đòi chủ dự án làm một việc ĐỀU ĐẶN đã không được dùng ⇒ phần công đó nhóm bỏ: báo cáo viết để đọc một
lần là đủ; phiên điều phối tự chọn một dòng "xong" cho phiên khác chứng minh lại; cuối buổi phiên điều phối tự hỏi *"hôm nay chủ dự án phải gợi hướng hay nhắc
lại ở chỗ nào — vì sao nhóm không tự thấy?"*

**Kiểm bằng gì** — chủ dự án làm theo ý 4 mà không cần hỏi thêm; thiếu một trong bốn ý ⇒ báo cáo chưa xong.

## 5. Phải nhắc lần thứ HAI ⇒ máy trước, chữ sau

Lỗi cách làm gặp lần đầu: sửa việc đó, ghi một dòng vào sổ giới hạn, không thêm luật. Lặp lần hai, xét theo thứ tự: (a) bỏ hẳn khả năng sai được không (đổi
thiết kế, để script làm thay) → (b) máy kiểm được không (test, hook git — tầng mọi agent đều đi qua) → (c) cuối cùng mới một dòng luật, viết thành việc làm được
ngay, nói điều NÊN làm kèm phạm vi và lý do, không kèm chuyện sự cố. Rào mới thử một lần bằng ca cố ý hỏng trước khi tin. Hậu quả không lùi được ⇒ rào ngay lần
đầu. Luật lâu không ai vi phạm lại và không còn lý do ⇒ gỡ; mỗi vòng sửa luật, tổng chữ luật không tăng. Thêm luật, rào, file sổ, vòng review chỉ khi có sự cố
đã thấy thật — lời dè dặt tích dần trong file luật, ghi chú và trí nhớ của agent làm agent đứng yên.
File agent luôn đọc (`AGENTS.md`) giữ ngắn, **dưới 24.000 byte** (có công cụ cắt file luật ở cỡ đó mà không báo); chi tiết để file khác, mở khi cần.

**Trí nhớ qua đêm nằm ở ba trang ghi đè, không ở thư mục báo cáo:** trang hiện trạng · **mục lục việc** (việc xong ⇒ dời MỘT dòng sang danh sách việc đã xong) ·
**sổ riêng của phiên** theo khuôn bảy mục: đang dở + nhánh / mã commit · đã soạn / đã review chưa gộp · việc kế + "xong khi" · ai chờ mình ↔ mình chờ ai · câu
treo · thứ đang chạy / rác · bẫy của phiên. Báo cáo từng việc để ở **thư mục ngày** (tên = `date +%F`, tên file mở đầu bằng vai) — để tra, không bắt đọc; báo cáo
đã đặt vào ngày nào thì không dời, bản cập nhật là file mới ở ngày mới. Dữ liệu riêng, bản nháp và lời chủ dự án nguyên văn để ngoài git.

**Mở lại phiên cho nhẹ:** mở phiên đọc file luật ngắn (công cụ tự nạp) + trang hiện trạng + mục lục việc + sổ riêng của phiên; luật chi tiết đọc **đúng mục khi
NHẬN việc** chạm mục đó. Kết phiên nhẹ (tắt / mở lại để làm mới ngữ cảnh): THAY — không nối — sổ riêng bằng khuôn bảy mục. Chỉ mở lại phiên đã đầy. Phiên thực
thi đợi tin mở phiên của phiên điều phối rồi trả lời MỘT tin (vai + báo cáo mở phiên).

**Kiểm bằng gì** — `wc -c AGENTS.md`; công cụ mới: hỏi nó "bạn đã nạp file hướng dẫn và skill nào, trích dòng đầu mỗi file" — không trích được là chưa nạp.

## 6. Test thật, lấy mốc, agent tự test, soát tích hợp, soát độ thật của test

- **Lấy mốc:** nhận repo hoặc mở một việc lớn ⇒ chạy bộ test, ghi số đạt / hỏng TRƯỚC khi sửa gì. Test hỏng sẵn từ mốc không phải lỗi của bạn.
- **Test thật là mặc định:** hệ thống thật, dữ liệu thật, model thật; được dùng tiền API cho đo / thử (ghi số thật, dùng hiệu quả). Đồ giả để test nhanh logic
  quanh model — không thay lượt thật khi nghiệm thu.
- **Đổi thước định kỳ:** ở mỗi mốc, một phép thử từ chỗ đứng khác với thước đang dùng (chủ dự án tự bấm, người dùng do model đóng vai hỏi nhiều lượt, model khác
  hãng đọc) — lớp lỗi mới thường chỉ lộ ra khi đổi cách nhìn, không phải khi đo thêm bằng thước cũ.
- **Agent tự test:** đổi thứ người dùng thấy ⇒ agent tự chạy trên hệ thống đang chạy và đính ảnh trước–sau / đầu ra vào báo cáo. Test agent viết cho code của
  chính nó chỉ được tin khi đã thấy ĐỎ một lần (trên code cũ, hoặc khi cố ý làm hỏng). Agent tự test **không thay** người / phiên khác kiểm (mục 3).
- **Sửa lỗi bốn bước:** tái hiện (đúng cấu hình đang chạy, thử MỘT lượt trước) ⇒ chứng minh nguyên nhân gốc (log, vết) ⇒ một sửa tập trung ⇒ chứng minh đã sửa
  bằng chính lệnh tái hiện. Không thêm lớp che lỗi; hai giả thuyết ⇒ thử từng cái.
- **Soát tích hợp sau mỗi đợt gộp:** một phiên / agent con ngữ cảnh mới, chỉ đọc, tìm chỗ HAI tính năng gặp nhau mà test từng nhánh không bắt (skill
  `soat-tich-hop`); mỗi điểm phải có `file:dòng` + một đầu vào tái hiện rồi mới sửa [đã chạy].
- **Soát độ thật của test:** định kỳ hỏi "test này bắt được lỗi gì thật?" — test chỉ khẳng định lại điều code vừa viết, hoặc giả luôn phần cần kiểm, thì sửa hoặc
  bỏ; phép kiểm mới phải thấy một ca "biết chắc hỏng" ra hỏng trước khi số 0 của nó được tin.
- Rào chặn / từ chối người dùng: đo cả hai chiều — bắt được bao nhiêu và chặn nhầm bao nhiêu ca thường.

**Kiểm bằng gì** — báo cáo mục 4 ý 2 có đủ hai dòng "đồ giả" ↔ "lượt thật"; sau đợt gộp có file kết quả soát tích hợp.

## 7. Đo chính cách làm việc bằng ba con số + một con số sản phẩm

Ghi vào tổng hợp ngày: **(a) số việc đã báo "xong" bị lật lại** (chủ dự án, reviewer hoặc máy tìm ra chưa xong) · **(b) số lần chủ dự án phải nhắc lại một điều
đã nói** · **(c) số lần chủ dự án phải tự gợi một hướng mà nhóm lẽ ra phải nêu**. (a), (b) đo lỗi làm sai / làm thừa; (c) đo lỗi nhìn hẹp — thiếu nó thì "hẹp"
luôn trông như an toàn. Kèm **một con số của sản phẩm** mà người dùng cảm được (ở repo này: mục 9). Muốn đổi cách làm (thêm phiên, thêm luật, đổi công cụ, đổi
kiểu điều phối) ⇒ so các số trước và sau, không quyết theo cảm giác; mẫu nhỏ ⇒ chỉ tin chênh rõ.
**Cách đếm (a):** chỉ đếm việc đã báo chủ dự án hoặc đã gộp vào nhánh chính; lỗi người kiểm bắt TRƯỚC khi gộp đếm riêng — đó là quy trình chạy đúng. **Một số
về giá:** tỉ lệ commit chạm code sản phẩm ↔ không chạm (tỉ lệ thấp kéo dài = nhóm đang viết VỀ công việc nhiều hơn làm việc). Các số đếm bằng lệnh trên file sẵn
có, không mở sổ mới.

## 8. Một phiên hay nhiều phiên (chưa phải luật)

Mặc định hợp lý: **một phiên + agent con**; phiên thứ hai mở để **kiểm**. Nhiều phiên cùng viết code chỉ đáng khi các phần không chung file, phần dùng chung đã
xong trước, và có đủ làn đo cho tất cả — lợi thật của nhiều phiên là có người khác kiểm, không phải tốc độ gõ. Agent con không thay người kiểm. Chọn kiểu nào thì
đo bằng các con số ở mục 7.

## 9. Ở repo này (phần viết lại khi chép trang sang dự án khác)

| Trang nói | Ở repo này là |
|---|---|
| luật cứng + bảng quyền + cách nhìn việc | `AGENTS.md` |
| trang hiện trạng · mục lục việc · sổ riêng của phiên | `session_prompt/HIEN_TRANG.md` · `session_prompt/VIEC_DANG_MO.md` (xong ⇒ `VIEC_DA_XONG.md`) · `session_prompt/sessions/STATUS_<X>.md` |
| ý / hướng chưa thử, mỗi ý kèm phép đếm rẻ nhất | `session_prompt/Y_CHUA_THU.md` |
| thư mục ngày | `report_agent/<YYYY-MM-DD>/` (`TONG_HOP.md` của phiên điều phối) |
| lời chủ dự án nguyên văn · sổ cải tiến cách làm | `data/loi_user/<ngày>.md` (ngoài git) · `session_prompt/SO_CAI_TIEN_CACH_LAM.md` |
| nhật ký dài (chỉ tra) | `session_prompt/CURRENT_HANDOFF.md`, `session_prompt/Project_Status.md` |
| lệnh bật hệ thống, chạy test, lấy mốc · sổ giới hạn | `guides/RUNBOOK_BAN_GIAO.md` mục 1–3 · mục 10 |
| "đã đẩy lên" lấy từ máy | `scripts/commit_push.sh "<lời commit>" <file>…` in `ĐÃ PUSH <sha> origin/<nhánh>` [đã chạy] |
| rào bằng máy mọi agent đều qua | `.githooks/pre-commit`, `pre-push`; kiểm đã bật: `git config --get core.hooksPath` ⇒ `.githooks` [đã chạy] |
| tài liệu viết cho người · báo cáo bốn ý của việc vừa xong | `bai_hoc/` · `bai_hoc/VIEC_MOI_XONG.md` |
| con số sản phẩm đang đuổi · ba con số cách làm | `session_prompt/HIEN_TRANG.md` mục 4 |
| làm một mình · mở phiên · kết phiên nhẹ | `guides/KHI_CHI_CO_MOT_AGENT.md` · `session_prompt/START_SESSION.md` · `session_prompt/WORKFLOW.md` §8 |

**Sở thích đã chốt của chủ dự án (agent nào cũng theo):**
- Tiếng Việt, lời thường, thuật ngữ kèm nghĩa; **đủ quan trọng hơn ngắn**; không dùng mã nội bộ khi chưa giải nghĩa.
- Chủ dự án nêu kết quả và giới hạn; hướng chủ dự án nêu là gợi ý để xét; danh sách ý bằng dấu phẩy hay "..." là "nhớ gì nêu đó" (mục 1).
- Việc thật sự của chủ dự án (mục tiêu, tiền, xoá dữ liệu, hướng sản phẩm, deploy): **mỗi lần một câu**, có sẵn đáp án; mỗi đáp án kèm hệ quả, khi nào sai, chọn
  khác thì mất gì; bộ đáp án có cả hướng agent tự thêm, ghi rõ cái nào của ai.
- Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật; rào, lớp, bước kiểm "phòng xa" chỉ thêm khi có sự cố đã thấy thật; công sức tương xứng với tuổi thọ của
  phần đang làm.
- Việc đã chốt thì không hỏi lại, không trình lại như lỗi. Số của người khác / agent con gắn "chưa kiểm" tới khi có người thứ hai tính lại. Giờ ghi vào tài
  liệu lấy bằng lệnh `date`, không ước.
- Kế hoạch viết theo **thứ tự + điều kiện đạt**, không gắn ngày: bước trước đạt là làm bước sau ngay.

## 10. Nguồn của từng mục (vì sao)

Bảng "mục nào dựa vào bài nào của các khoá học" nằm ở `guides/CACH_LAM_VIEC_NGUON.md` (chỉ mở khi cần tra vì sao).

## Chưa thử

- Chưa thử trang này với Codex hay Antigravity; bước đầu khi thử: hỏi công cụ đã nạp file nào (mục 5). Kiểu điều phối khi đổi công cụ chưa chọn (mục 8).
- Mục 1 (đề bài từ lời chủ dự án), mục 4 (phần của chủ dự án) và con số (c) ở mục 7 mới viết 21/11/2026, đang thử ba ngày làm việc.
