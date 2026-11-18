# Cách làm việc với coding agent — dùng cho mọi agent, mọi dự án

Bản 3 (10:38 18/11/2026; đã qua hai lượt review chéo giữa các phiên; chưa thử với công cụ khác hãng). Sửa gần nhất: 20:01 18/11/2026 (bảng nguồn mục 10 dời sang file riêng).
Người đọc: **bất kỳ coding agent nào** (Claude Code, Codex, Antigravity…), làm một mình hay trong nhóm nhiều phiên; và chủ dự án (gọi là User).
Trang này nói **cách làm** và **chép sang dự án khác được**: mục 1–8 không phụ thuộc dự án; mục 9 ("Ở repo này") là phần viết lại khi chép; mục 10 trỏ sang bảng nguồn (file riêng).
Luật cứng + bảng quyền của từng dự án nằm ở `AGENTS.md` của dự án đó — khi trang này khác `AGENTS.md` thì `AGENTS.md` thắng. Bộ file mẫu cho dự án mới: `guides/khung/`.
Nhãn: **[đã chạy]** = cách làm / lệnh đã chạy thật ở repo gốc của trang · **[chưa chạy]** = chưa.

| Từ | Nghĩa |
|---|---|
| phiên | một lần mở một coding agent. "Phiên mới, ngữ cảnh sạch" = mở cuộc trò chuyện mới, không dán lịch sử cũ — chỉ đưa thứ cần xem |
| nhóm / phiên điều phối | khi chạy nhiều phiên cùng lúc: một phiên chia việc và nói chuyện với User, các phiên khác thực thi. Làm một mình thì bạn là cả hai |
| agent con | agent do một phiên tạo ra để làm một phần việc; nó chỉ biết đúng những gì ghi trong lời giao |
| dữ liệu riêng | mọi thứ không được vào git (dữ liệu gốc của sản phẩm, bộ câu chấm, khoá) — danh sách cụ thể ở `AGENTS.md` |
| trang hiện trạng | MỘT trang viết lại tại chỗ: đang chạy gì, việc đang mở, quyết định còn hiệu lực — đọc mỗi lần mở phiên |
| sổ giới hạn | danh sách "tình huống → hệ quả → vì sao chấp nhận" của những thứ biết là chưa tốt mà chưa sửa |
| lời dặn cho model | chữ hướng dẫn gửi kèm mỗi lần sản phẩm gọi model (system prompt) |
| mốc | con số của bản / cách làm cũ dùng để so (baseline) |
| chạm trần | một lượt chạy dừng vì hết số lần / thời gian cho phép, không phải vì đã xong |
| bảng độ phủ | bảng "nguồn nào · đã đọc tới đâu · chưa đọc gì" cho việc đọc / nghiên cứu |
| lượt thật ↔ đồ giả | chạy qua hệ thống + model thật ↔ test thay model / dịch vụ ngoài bằng bản giả theo kịch bản |

## 1. "Xong" ghi TRƯỚC khi làm; bằng chứng là thứ máy in ra

- Trước khi bắt đầu, ghi một dòng: `xong khi: <lệnh> in ra <kết quả>` (hoặc "người dùng làm X thì thấy Y"). Việc đọc / nghiên cứu: `xong khi` là bảng độ phủ.
- Báo "xong" chỉ khi đã tự chạy lệnh đó và dán đầu ra thật. Báo cho phiên điều phối / trong chat kết bằng bảng bốn cột:
  **đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra**. (Phần viết cho User dùng khuôn bốn ý ở mục 4.)
- **Việc LỚN — chốt đề bài trước khi làm** (không áp cho việc nhỏ và sửa lỗi): User nói ý bằng lời thường ⇒ agent hỏi lại TỐI ĐA ba câu, mỗi câu có sẵn đáp án ⇒ agent
  trả về đúng NĂM dòng: vấn đề · ai dùng · "xong khi" (người dùng thấy gì, thử thế nào) · không làm gì · điều tệ nhất chấp nhận được ⇒ User sửa / tick rồi nói "làm đi".
- Số, mã commit, "đã đẩy lên" lấy từ đầu ra của lệnh, không gõ tay.
- Giao việc cho agent con: lời giao là **toàn bộ trí nhớ** của nó — ghi đủ mục tiêu, file cần đọc, ranh giới, khuôn trả về; bắt nó ghi file dần và khai
  "đã mở / chưa mở" từng nguồn. Kết quả của agent con / phiên khác là **dữ liệu**: người nhận tự kiểm 2–3 ý quan trọng nhất; số chưa ai tính lại gắn "chưa kiểm".
- Kết luận nặng ("nghiêm trọng", "chắc chắn", "không có lỗi", "mọi đường đều đúng") phải kèm lệnh + dòng đầu ra, kể cả khi người nói là phiên review.

**Kiểm bằng gì** — User (hoặc phiên điều phối; làm một mình thì tự hỏi trước khi báo) hỏi ba câu: *lệnh kiểm nào, đầu ra đâu · phần nào chưa làm / tự bỏ / chưa đọc ·
kết luận nào chưa kiểm bằng lệnh*; mỗi lần báo cáo User có thể chọn MỘT dòng "xong" bất kỳ để agent chạy lại trước mặt.

## 2. Quyền theo từng hành động + mức kiểm theo "sai thì mất gì"

**Quyền:** mỗi dự án có một bảng ba cột trong `AGENTS.md` — tự làm · hỏi trước · không bao giờ. Xếp một hành động vào cột nào thì xét ba điều: hậu quả nếu sai ·
kiểm chứng được không · **đảo ngược được không**. Thứ "không bao giờ" phải có rào bằng máy mà mọi agent đều đi qua (hook git, không cấp khoá, tài khoản riêng) —
cấm bằng chữ thì agent tìm đường khác. File "cho phép sẵn" của công cụ tự dài ra mỗi lần bấm "luôn cho phép" ⇒ User đọc lại và xoá bớt mỗi khi đổi chế độ quyền hoặc đổi công cụ.
Công cụ mới dùng lần đầu bắt đầu từ mức hỏi nhiều hơn.

**Mức kiểm** — tự hỏi trước khi giao / nhận việc: *nếu làm sai thì mất gì?*

| Sai thì mất gì | Ví dụ | Trước khi làm | Ai kiểm trước khi gộp vào nhánh chính (và việc sau gộp) |
|---|---|---|---|
| Mất ít, lùi được ngay | sửa chữ, tài liệu, hàm thuần có test, script dùng một lần | làm thẳng trên nhánh riêng | một phiên / người KHÁC người viết: nhánh chỉ tài liệu ⇒ đọc diff; nhánh có code ⇒ đọc diff + chạy test file chạm |
| Người dùng thấy sai | đổi hành vi, câu trả lời, giao diện, lời dặn cho model | commit trước; kế hoạch ≤ 1 trang: file đổi · thứ tự · rủi ro · bằng chứng | phiên mới ngữ cảnh sạch đọc diff + tiêu chí; SAU gộp báo User cách thử 2 phút |
| Không lùi được / tiền / dữ liệu / bảo mật | sửa dữ liệu gốc, xoá, đổi model, deploy, gửi dữ liệu ra ngoài | sao lưu thứ nằm ngoài git; User duyệt kế hoạch trước | reviewer **khác hãng** (mục 3) + User tự bấm thử |

Tài liệu không tự động là "mất ít": repo công khai, lộ một dòng dữ liệu riêng là không lùi được.
**Đường lùi:** chỉ git lùi được đủ code ⇒ commit trước mọi việc mạo hiểm. Thứ nằm NGOÀI git không ai cứu được nếu hỏng ⇒ sao lưu trước khi sửa; bản sao ngoài máy
là việc của User.

**Kiểm bằng gì** — lịch sử gộp ghi ai đã kiểm (`git log --merges --oneline -5` [đã chạy]); xếp nhầm mức (việc lớn làm kiểu nhỏ) là lỗi phải ghi vào báo cáo.

## 3. Người viết không tự chấm; việc mức cao có người chấm khác hãng

- Ai viết thì người / phiên khác kiểm. Làm một mình: mở phiên mới, ngữ cảnh sạch, chỉ đưa diff + tiêu chí, bảo tìm lỗi.
- Bộ câu thử cho code đọc chữ người dùng do người **không viết code đó** soạn (cả câu phải đúng lẫn câu "giống mà không phải").
- Người đề xuất một luật cách làm không phải người kết luận luật đó có hiệu quả — kết luận bằng hai con số ở mục 7.
- **Gói review khác hãng** (việc mức cao, hoặc sau một đợt gộp lớn): người làm (hoặc nhóm) soạn MỘT file `.md` tự đủ ngữ cảnh theo mẫu
  `guides/khung/GOI_REVIEW_KHAC_HANG.mau.md`; User tự mở công cụ hãng khác và gửi file; model đó ghi kết quả ra một file. Agent không tự gọi công cụ hãng khác thay
  User [đã chạy một lần 18/11: thêm được 3 điểm thật mà lượt cùng hãng bỏ sót].
- Kết quả review là dữ liệu: người nhận tái hiện từng điểm (cả hệ quả lẫn nguyên nhân) trước khi sửa; điểm bị bác ghi lý do để User liếc.

**Kiểm bằng gì** — báo cáo ghi rõ ai kiểm (nhãn ở mục 4); gói review khác hãng lưu cả đề bài lẫn file kết quả.

## 4. Báo cáo cho User: bốn ý + nhãn độ tin — và phần của User

User không đọc code; User đọc báo cáo + tài liệu viết cho người, rồi tự bấm thử. Mỗi việc xong, phần viết cho User có đúng bốn ý, lời thường
(mẫu: `guides/khung/BAO_CAO_4_Y.mau.md`):
1. **Người dùng thấy gì khác** (trước ↔ sau, một ví dụ thật; đổi giao diện thì kèm ảnh trước–sau).
2. **Bằng chứng**: đo gì · bao nhiêu · so với mốc nào · tách hai dòng **"test bằng đồ giả: n đạt"** và **"lượt thật: n lượt, kết quả"** — chỉ có dòng đầu thì chưa xong.
   Có số thì kèm 2–3 ca sai nguyên văn (không chép dữ liệu riêng vào file theo dõi).
3. **Chưa làm / giới hạn** (kể cả thứ tự hoãn).
4. **Cách thử trong 2 phút**: mở đâu, gõ gì, thấy gì là đúng.

Mỗi khẳng định gắn một nhãn độ tin: **[máy kiểm]** (có lệnh in ra) · **[người thứ hai kiểm]** · **[chưa kiểm]**. Bảng kết quả có cột "kết thúc kiểu gì"
(bình thường / chạm trần / lỗi) để ca hỏng giữa chừng không bị tính là đúng.

**Phần của User:** luôn đọc báo cáo; khi rảnh bấm thử theo ý 4; việc xong thì tự thử và nêu ý kiến · chọn một dòng "xong" để agent chứng minh lại · mỗi tuần nói lại bằng
lời mình lý do của một quyết định đã chọn (không nói được ⇒ agent giải thích lại) · việc lớn: sửa / tick năm dòng đề bài do agent soạn (mục 1) rồi mới nói "làm đi" ·
trả lời câu hỏi làm rõ của agent sớm; gửi gói review khác hãng khi đã soạn xong · hai câu tự hỏi: trước khi tin một so sánh, hỏi agent *"chạy lại y nguyên thì lệch bao
nhiêu?"*; sau mỗi buổi, *"mình đang là điểm nghẽn của agent ở chỗ nào?"*

**Kiểm bằng gì** — User làm theo ý 4 mà không cần hỏi thêm; thiếu một trong bốn ý ⇒ trả lại báo cáo.

## 5. Phải nhắc lần thứ HAI ⇒ máy trước, chữ sau

Lỗi cách làm gặp lần đầu: sửa việc đó, ghi một dòng vào sổ giới hạn, không thêm luật. Lặp lần hai, xét theo thứ tự: (a) bỏ hẳn khả năng sai được không (đổi thiết
kế, để script làm thay) → (b) máy kiểm được không (test, hook git — tầng mọi agent đều đi qua) → (c) cuối cùng mới một dòng luật, viết thành việc làm được ngay, không
kèm chuyện sự cố. Rào mới thử một lần bằng ca cố ý hỏng trước khi tin. Hậu quả không lùi được ⇒ rào ngay lần đầu. Luật lâu không ai vi phạm lại và không còn lý do ⇒ gỡ.
File agent luôn đọc (`AGENTS.md`) giữ ngắn, **dưới 24.000 byte** (có công cụ cắt file luật ở cỡ đó mà không báo); chi tiết để file khác, mở khi cần.
Tài liệu bắt buộc đọc lúc mở phiên chỉ gồm luật + trang hiện trạng; nhật ký nối đuôi để tra, không bắt đọc.

**Mở lại phiên cho nhẹ** [đang thử, chưa kiểm] — đo một lần ở repo gốc: mỗi phiên đọc 880–1.400 dòng lúc mở, dùng khoảng 185; ~9 tin chỉ để tìm phiên điều phối.
Cách biết có ích: ba lần mở kế đếm số lần vấp luật vì chưa đọc — lớn hơn 0 ⇒ xét lại.
- **Mở phiên đọc ngắn:** file luật ngắn (công cụ tự nạp) + trang hiện trạng + mục đầu sổ riêng của phiên + khối đầu sổ việc. Luật chi tiết đọc **đúng mục khi NHẬN việc** chạm mục đó (lời giao ghi "đọc mục nào"); vài luật hay vấp nhất đưa lên file luật ngắn. Phiên giữ luật (điều phối) vẫn đọc đủ.
- **Kết phiên nhẹ** (tắt / mở lại chỉ để làm mới ngữ cảnh): THAY — không nối — mục đầu sổ riêng bằng ba dòng: việc dở · thứ đang chạy / file tạm · bẫy phiên này. Nhật ký và vòng cải tiến để cuối ngày.
- **Chỉ mở lại phiên đã đầy.** Phiên thực thi không rải tin đi tìm phiên điều phối: đợi tin mở phiên của nó rồi trả lời MỘT tin (vai + báo cáo mở phiên).

**Kiểm bằng gì** — `wc -c AGENTS.md`; công cụ mới: hỏi nó "bạn đã nạp file hướng dẫn và skill nào, trích dòng đầu mỗi file" — không trích được là chưa nạp.

## 6. Test thật, lấy mốc, agent tự test, soát tích hợp, soát độ thật của test

- **Lấy mốc:** nhận repo hoặc mở một việc lớn ⇒ chạy bộ test, ghi số đạt / hỏng TRƯỚC khi sửa gì. Test hỏng sẵn từ mốc không phải lỗi của bạn.
- **Test thật là mặc định:** hệ thống thật, dữ liệu thật, model thật; được dùng tiền API cho đo / thử (ghi số thật, dùng hiệu quả). Đồ giả chỉ để test nhanh logic
  quanh model — không thay lượt thật khi nghiệm thu.
- **Agent tự test:** đổi thứ người dùng thấy ⇒ agent tự chạy trên hệ thống đang chạy và đính ảnh trước–sau / đầu ra vào báo cáo. Test agent viết cho code của chính nó
  chỉ được tin khi đã thấy ĐỎ một lần (trên code cũ, hoặc khi cố ý làm hỏng). Agent tự test **không thay** người / phiên khác kiểm (mục 3).
- **Sửa lỗi bốn bước, không nhảy bước:** tái hiện (đúng cấu hình đang chạy, thử MỘT lượt trước) ⇒ chứng minh nguyên nhân gốc (log, vết) ⇒ một sửa tập trung ⇒
  chứng minh đã sửa bằng chính lệnh tái hiện. Không thêm lớp che lỗi; hai giả thuyết ⇒ thử từng cái.
- **Soát tích hợp sau mỗi đợt gộp:** một phiên / agent con ngữ cảnh mới, chỉ đọc, tìm chỗ HAI tính năng gặp nhau mà test từng nhánh không bắt. Đề bài mẫu:
  "Liệt kê các cơ chế có thể cùng kích hoạt trong một lượt. Với mỗi cặp, đọc code xem thứ tự / điều kiện có làm kết quả sai, thiếu, trùng hay lệch log không. Chỉ
  báo điểm có `file:dòng` và một đầu vào tái hiện; cuối báo cáo ghi phần CHƯA đọc." Mỗi điểm phải tái hiện được rồi mới sửa [đã chạy 18/11: ra 11 điểm].
- **Soát độ thật của test:** định kỳ hỏi "test này bắt được lỗi gì thật?" — test chỉ khẳng định lại điều code vừa viết, hoặc giả luôn phần cần kiểm, thì sửa hoặc bỏ;
  phép kiểm mới phải thấy một ca "biết chắc hỏng" ra hỏng trước khi số 0 của nó được tin [đã chạy một lượt 18/11].
- Rào chặn / từ chối người dùng: đo cả hai chiều — bắt được bao nhiêu và chặn nhầm bao nhiêu ca thường.
- **Chất lượng code:** file quá dài, hoặc đường cũ còn nằm song song đường mới ⇒ không tự dọn ngoài phạm vi việc; ghi đường cũ vào sổ giới hạn dưới nhãn "đường cũ — đừng chép".

**Kiểm bằng gì** — báo cáo mục 4 ý 2 có đủ hai dòng "đồ giả" ↔ "lượt thật"; sau đợt gộp có file kết quả soát tích hợp.

## 7. Đo chính cách làm việc bằng hai con số

Mỗi tuần ghi hai số vào trang hiện trạng: **(a) số việc đã báo "xong" bị lật lại** (User, reviewer hoặc máy tìm ra chưa xong) · **(b) số lần User phải nhắc lại một
điều đã nói**. Muốn đổi cách làm (thêm phiên, thêm luật, đổi công cụ, đổi kiểu điều phối) ⇒ so hai số trước và sau, không quyết theo cảm giác. Mẫu nhỏ ⇒ chỉ tin chênh rõ. [ghi một lần]
**Cách đếm (a):** chỉ đếm việc đã báo User hoặc đã gộp vào nhánh chính; lỗi người kiểm bắt TRƯỚC khi gộp đếm riêng — đó là quy trình chạy đúng. **Hai số về giá**, ghi cùng chỗ:
tỉ lệ commit chạm code ↔ không chạm code · số câu đã hỏi User trong ngày (trên 8 ⇒ hôm sau gom câu). Không thêm số nào khác. [ghi một lần]

## 8. Một phiên hay nhiều phiên (chưa phải luật)

Mặc định hợp lý: **một phiên + agent con**; phiên thứ hai mở để **kiểm**. Nhiều phiên cùng viết code chỉ đáng khi các phần không chung file, phần dùng chung đã xong
trước, và User đọc kịp đầu ra của tất cả — lợi thật của nhiều phiên là có người khác kiểm, không phải tốc độ gõ. Agent con không thay người kiểm. Chọn kiểu nào thì đo
bằng hai con số ở mục 7.

## 9. Ở repo này (phần viết lại khi chép trang sang dự án khác)

| Trang nói | Ở repo này là |
|---|---|
| luật cứng + bảng quyền | `AGENTS.md` (`wc -c AGENTS.md` [đã chạy 18/11]: dưới 5 KB) |
| trang hiện trạng · nhật ký | `session_prompt/HIEN_TRANG.md` · `session_prompt/CURRENT_HANDOFF.md`, `session_prompt/Project_Status.md` (nhật ký dài — chỉ tra) |
| lệnh bật hệ thống, chạy test, lấy mốc | `guides/RUNBOOK_BAN_GIAO.md` mục 1–3 |
| "đã đẩy lên" lấy từ máy | `scripts/commit_push.sh "<lời commit>" <file>…` in `ĐÃ PUSH <sha> origin/<nhánh>` [đã chạy] |
| rào bằng máy mọi agent đều qua | `.githooks/pre-commit`, `pre-push`; kiểm đã bật: `git config --get core.hooksPath` ⇒ `.githooks` [đã chạy] |
| sổ giới hạn · quyết định đã chốt | runbook mục 10 · `session_prompt/Project_Status.md` mục 5 |
| tài liệu viết cho người · báo cáo bốn ý của việc vừa xong | `bai_hoc/` · `bai_hoc/VIEC_MOI_XONG.md` |
| sao lưu thứ ngoài git trước khi sửa | runbook mục 5 [đã chạy ở mỗi lần sửa dữ liệu gốc] |
| làm một mình | `guides/KHI_CHI_CO_MOT_AGENT.md` |
| mở phiên đọc ngắn · kết phiên nhẹ | `session_prompt/START_SESSION.md` · `session_prompt/WORKFLOW.md` §8 |

**Sở thích đã chốt của chủ dự án (agent nào cũng theo):**
- Tiếng Việt, lời thường, thuật ngữ kèm nghĩa; **đủ quan trọng hơn ngắn**; không dùng mã nội bộ khi chưa giải nghĩa.
- Cần quyết định: **mỗi lần một câu**, có sẵn đáp án để chọn; mỗi đáp án kèm hệ quả, khi nào sai, chọn khác thì mất gì. Nhóm nhiều phiên: bàn nhóm trước rồi mới đưa
  một khuyến nghị; làm một mình: nêu luôn phương án ngược mạnh nhất cạnh khuyến nghị.
- Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật; không thêm rào, lớp, bước kiểm "phòng xa"; công sức tương xứng với tuổi thọ của phần đang làm.
- Việc đã chốt thì không hỏi lại, không trình lại như lỗi. Số của người khác / agent con gắn "chưa kiểm" tới khi có người thứ hai tính lại. Giờ ghi vào tài liệu
  lấy bằng lệnh `date`, không ước.
- Kế hoạch viết theo **thứ tự + điều kiện đạt**, không gắn ngày: bước trước đạt là làm bước sau ngay; ngày chỉ là ghi chép.

## 10. Nguồn của từng mục (vì sao)

Bảng "mục nào dựa vào bài nào của các khoá học" nằm ở file riêng cùng thư mục: `guides/CACH_LAM_VIEC_NGUON.md` (dời ra để trang này nhẹ; chỉ mở khi cần tra vì sao).

## Chưa làm / chưa thử (đúng lúc 19:34 18/11/2026)

- **Chưa thử với Codex hay Antigravity** — thử ở buổi chủ dự án test toàn bộ; bước đầu: hỏi công cụ đã nạp file nào (mục 5). Kiểu điều phối khi đổi công cụ chưa chọn (mục 8).
- **Vòng cuối ngày** (mục 5, 7) đã chạy lần đầu 18/11; hai con số và hai số về giá mới ghi MỘT lần (hai con số đã có phiên khác soát).
- **Mở lại phiên cho nhẹ** (mục 5): mới MỘT lần mở đọc ngắn, chưa đếm lần vấp luật.
- Hai skill mới (`soat-tich-hop`, `giao-viec-agent-con`) mới được chấm MỘT lượt mỗi bên, chưa có người chấm thứ hai.
- Chưa thành nếp: ảnh trước–sau (mục 6), năm dòng đề bài và "chọn một dòng xong để chứng minh lại" (mục 1).
