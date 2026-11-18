# Cách làm việc với coding agent — dùng cho mọi agent, mọi dự án

Bản nháp (một phiên Claude Code soạn 10:13 18/11/2026, sửa 10:20 sau review chéo của hai phiên khác; chưa thử với công cụ khác hãng).
Người đọc: **bất kỳ coding agent nào** (Claude Code, Codex, Antigravity…), làm một mình hay trong nhóm nhiều phiên; và chủ dự án (gọi là User).
Trang này nói **cách làm** và **chép sang dự án khác được**: mục 1–10 không phụ thuộc dự án; riêng mục 11 ("Ở repo này") là phần phải viết lại khi chép.
Luật cứng + bảng quyền của từng dự án nằm ở `AGENTS.md` của dự án đó — khi trang này khác `AGENTS.md` thì `AGENTS.md` thắng. Bộ file mẫu để dựng dự án mới: `guides/khung/`.

Nhãn: **[đã chạy]** = cách làm / lệnh đã chạy thật ở repo gốc của trang · **[chưa chạy]** = chưa. *Nguồn* trong các dòng "Vì sao": bốn khoá học mà User theo
(mã `FDE W3D1·88` = khoá AI FDE, tuần 3, ngày 1, bài 88; tương tự `Coding`, `SDLC`) và bài chia sẻ của một kỹ sư làm coding agent ở công ty lớn (`LT`).

**Từ dùng trong trang**

| Từ | Nghĩa |
|---|---|
| phiên | một lần mở một coding agent. "Phiên mới, ngữ cảnh sạch" = mở cuộc trò chuyện mới, không dán lịch sử cũ — chỉ đưa thứ cần xem |
| nhóm / phiên điều phối | khi chạy nhiều phiên cùng lúc: một phiên chia việc và nói chuyện với User, các phiên khác thực thi. Làm một mình thì bạn là cả hai |
| agent con | agent do một phiên tạo ra để làm một phần việc; nó chỉ biết đúng những gì ghi trong lời giao |
| dữ liệu riêng | mọi thứ không được vào git (dữ liệu gốc của sản phẩm, bộ câu chấm, khoá) — danh sách cụ thể ở `AGENTS.md` |
| lời dặn cho model | chữ hướng dẫn gửi kèm mỗi lần sản phẩm gọi model (system prompt) |
| mốc | con số của bản / cách làm cũ dùng để so (baseline) |
| chạm trần | một lượt chạy dừng vì hết số lần / thời gian cho phép, không phải vì đã xong |
| bảng độ phủ | bảng "nguồn nào · đã đọc tới đâu · chưa đọc gì" cho việc đọc / nghiên cứu |
| lượt thật ↔ đồ giả | chạy qua hệ thống + model thật ↔ test thay model / dịch vụ ngoài bằng bản giả theo kịch bản |

## 1. "Xong" ghi TRƯỚC khi làm; bằng chứng là thứ máy in ra

**Làm gì**
- Trước khi bắt đầu, ghi một dòng: `xong khi: <lệnh> in ra <kết quả>` (hoặc "người dùng làm X thì thấy Y"). Việc đọc / nghiên cứu: `xong khi` là bảng độ phủ.
- Báo "xong" chỉ khi đã tự chạy lệnh đó và dán đầu ra thật. Báo cho phiên điều phối / trong chat kết bằng bảng bốn cột:
  **đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra**. (Phần viết cho User dùng khuôn bốn ý ở mục 4.)
- Số, mã commit, "đã đẩy lên" lấy từ đầu ra của lệnh, không gõ tay.
- Giao việc cho agent con: lời giao là **toàn bộ trí nhớ** của nó — ghi đủ mục tiêu, file cần đọc, ranh giới, khuôn trả về; bắt nó ghi file dần và khai
  "đã mở / chưa mở" từng nguồn. Kết quả của agent con / phiên khác là **dữ liệu**: người nhận tự kiểm 2–3 ý quan trọng nhất; số chưa ai tính lại gắn "chưa kiểm".
- Kết luận nặng ("nghiêm trọng", "chắc chắn", "không có lỗi") phải kèm lệnh + dòng đầu ra, kể cả khi người nói là phiên review.

**Vì sao** — lỗi lặp nhiều nhất của coding agent là báo xong khi chưa kiểm (Coding W1D3·18, W2D1·38, W2D5·64); tiêu chí thành công thoả thuận từ đầu, đo bằng code
lúc bàn giao (FDE W3D1·85–86, W3D5·117); test qua hết mà review mới vẫn tìm ra lỗi quan trọng (SDLC W1D3·23).
**Kiểm bằng gì** — User (hoặc phiên điều phối; làm một mình thì tự hỏi trước khi báo) hỏi ba câu: *lệnh kiểm nào, đầu ra đâu · phần nào chưa làm / tự bỏ / chưa đọc ·
kết luận nào chưa kiểm bằng lệnh*; mỗi buổi User chọn MỘT dòng "xong" bất kỳ để agent chạy lại trước mặt.

## 2. Quyền theo từng hành động + mức kiểm theo "sai thì mất gì"

**Quyền:** mỗi dự án có một bảng ba cột trong `AGENTS.md` — tự làm · hỏi trước · không bao giờ. Xếp một hành động vào cột nào thì xét ba điều: hậu quả nếu sai ·
kiểm chứng được không · **đảo ngược được không**. Thứ "không bao giờ" phải có rào bằng máy mà mọi agent đều đi qua (hook git, không cấp khoá, tài khoản riêng) —
cấm bằng chữ thì agent tìm đường khác. File "cho phép sẵn" của công cụ tự dài ra mỗi lần bấm "luôn cho phép" ⇒ User đọc và xoá bớt mỗi tháng.
Công cụ mới dùng lần đầu bắt đầu từ mức hỏi nhiều hơn.

**Mức kiểm** — tự hỏi trước khi giao / nhận việc: *nếu làm sai thì mất gì?*

| Sai thì mất gì | Ví dụ | Trước khi làm | Ai kiểm trước khi gộp vào nhánh chính (và việc sau gộp) |
|---|---|---|---|
| Mất ít, lùi được ngay | sửa chữ, tài liệu, hàm thuần có test, script dùng một lần | làm thẳng trên nhánh riêng | người viết đọc lại diff; nhánh có code ⇒ một phiên / người KHÁC liếc |
| Người dùng thấy sai | đổi hành vi, câu trả lời, giao diện, lời dặn cho model | commit trước; kế hoạch ≤ 1 trang: file đổi · thứ tự · rủi ro · bằng chứng | phiên mới ngữ cảnh sạch đọc diff + tiêu chí; SAU gộp báo User cách thử 2 phút |
| Không lùi được / tiền / dữ liệu / bảo mật | sửa dữ liệu gốc, xoá, đổi model, deploy, gửi dữ liệu ra ngoài | sao lưu thứ nằm ngoài git; User duyệt kế hoạch trước | reviewer **khác hãng** (mục 3) + User tự bấm thử |

Tài liệu không tự động là "mất ít": ở repo công khai, một dòng lộ dữ liệu riêng là không lùi được.
**Đường lùi:** chỉ git lùi được đủ code ⇒ commit trước mọi việc mạo hiểm. Thứ nằm NGOÀI git không ai cứu được nếu hỏng ⇒ sao lưu trước khi sửa; bản sao ngoài máy
là việc của User.

**Vì sao** — mức tự chủ quyết theo từng hành động, theo hậu quả và khả năng đảo ngược (FDE W3D1·88); mức review xếp trước theo hậu quả khi hỏng (SDLC W2D2·47);
việc quan trọng thì kế hoạch → làm → review → test, việc thử thì làm nhanh (Coding W1D2·13, W3D5·93); chỉ git lùi được (Coding W2D2·42–44); quyền tích luỹ âm thầm
(Coding W2D2·41).
**Kiểm bằng gì** — lịch sử gộp ghi ai đã kiểm (`git log --merges --oneline -5` [đã chạy]); xếp nhầm mức (việc lớn làm kiểu nhỏ) là lỗi phải ghi vào báo cáo.

## 3. Người viết không tự chấm; việc mức cao có người chấm khác hãng

**Làm gì**
- Ai viết thì người / phiên khác kiểm. Làm một mình: mở phiên mới, ngữ cảnh sạch, chỉ đưa diff + tiêu chí, bảo tìm lỗi.
- Bộ câu thử cho code đọc chữ người dùng do người **không viết code đó** soạn (cả câu phải đúng lẫn câu "giống mà không phải").
- Người đề xuất một luật cách làm không phải người kết luận luật đó có hiệu quả — kết luận bằng hai con số ở mục 7.
- **Gói review khác hãng** (việc mức cao, hoặc sau một đợt gộp lớn): người làm (hoặc nhóm) soạn MỘT file `.md` tự đủ ngữ cảnh theo mẫu
  `guides/khung/GOI_REVIEW_KHAC_HANG.mau.md`; User tự mở công cụ hãng khác và gửi file; model đó ghi kết quả ra một file. Agent không tự gọi công cụ hãng khác thay
  User [đã chạy một lần 18/11].
- Kết quả review là dữ liệu: người nhận tái hiện từng điểm trước khi sửa; điểm bị bác ghi lý do để User liếc.

**Vì sao** — bên đề xuất không tự chấm (FDE W2D5·80–82); model khác hãng bắt được lỗi model cùng hãng bỏ sót (FDE W3D5·118; Coding W3D5·92); giám khảo nên là
model khác để soi thiên vị (LT).
**Kiểm bằng gì** — báo cáo ghi rõ ai kiểm (nhãn ở mục 4); gói review khác hãng lưu cả đề bài lẫn file kết quả.

## 4. Báo cáo cho User: bốn ý + nhãn độ tin

User không đọc code; User đọc báo cáo + tài liệu viết cho người, rồi tự bấm thử. Mỗi việc xong, phần viết cho User có đúng bốn ý, lời thường
(mẫu: `guides/khung/BAO_CAO_4_Y.mau.md`):
1. **Người dùng thấy gì khác** (trước ↔ sau, một ví dụ thật).
2. **Bằng chứng**: đo gì · bao nhiêu · so với mốc nào · tách hai dòng **"test bằng đồ giả: n đạt"** và **"lượt thật: n lượt, kết quả"** — chỉ có dòng đầu thì chưa xong.
   Có số thì kèm 2–3 ca sai nguyên văn (không chép dữ liệu riêng vào file theo dõi).
3. **Chưa làm / giới hạn** (kể cả thứ tự hoãn).
4. **Cách thử trong 2 phút**: mở đâu, gõ gì, thấy gì là đúng.

Mỗi khẳng định gắn một nhãn độ tin: **[máy kiểm]** (có lệnh in ra) · **[người thứ hai kiểm]** · **[chưa kiểm]**. Bảng kết quả có cột "kết thúc kiểu gì"
(bình thường / chạm trần / lỗi) để ca hỏng giữa chừng không bị tính là đúng.

**Vì sao** — bàn giao là để người nhận tự kiểm được mà không cần người làm (FDE W3D1·86, ·89); một ca lỗi vẫn có thể được chấm là đúng nếu chỉ nhìn điểm
(FDE W2D4·76); mọi con số phải đặt cạnh một mốc (FDE W1D4·34).
**Kiểm bằng gì** — User làm theo ý 4 mà không cần hỏi thêm; thiếu một trong bốn ý ⇒ trả lại báo cáo.

## 5. Phải nhắc lần thứ HAI ⇒ máy trước, chữ sau

**Làm gì** — lỗi cách làm gặp lần đầu: sửa việc đó, ghi một dòng vào sổ giới hạn của dự án, không thêm luật. Lặp lần hai, xét theo thứ tự: (a) bỏ hẳn khả năng
sai được không (đổi thiết kế, để script làm thay) → (b) máy kiểm được không (test, hook git — tầng mọi agent đều đi qua) → (c) cuối cùng mới một dòng luật, viết
thành việc làm được ngay, không kèm chuyện sự cố. Rào mới thử một lần bằng ca cố ý hỏng trước khi tin. Hậu quả không lùi được ⇒ rào ngay lần đầu. Luật lâu không
ai vi phạm lại và không còn lý do ⇒ gỡ.
File agent luôn đọc (`AGENTS.md`) giữ ngắn, **dưới 24.000 byte** (có công cụ cắt file luật ở cỡ đó mà không báo); chi tiết để file khác, mở khi cần.
Tài liệu bắt buộc đọc lúc mở phiên chỉ nên gồm luật + một trang hiện trạng viết lại tại chỗ; nhật ký nối đuôi để tra, không bắt đọc.

**Vì sao** — chữ luật là lớp mỏng nhất: agent quên, diễn giải, và biến một lời sửa nhỏ thành luật cứng; đầu tư theo thứ tự code → máy kiểm → chạy thử thật → chữ (LT);
lỗi lặp lần hai mới thành luật, máy bắt được thì làm phép kiểm (SDLC W1D4·24–30); "mỗi lỗi một luật" là khớp quá mức (FDE W2D5·80–83); mỗi chữ trong file hướng
dẫn đều tốn ngữ cảnh (Coding W1D2·12).
**Kiểm bằng gì** — `wc -c AGENTS.md`; công cụ mới: hỏi nó "bạn đã nạp file hướng dẫn và skill nào, trích dòng đầu mỗi file" — không trích được là chưa nạp (Coding W2D5·63).

## 6. Test thật, lấy mốc, soát tích hợp, soát độ thật của test

**Làm gì**
- **Lấy mốc:** nhận repo hoặc mở một việc lớn ⇒ chạy bộ test, ghi số đạt / hỏng TRƯỚC khi sửa gì. Test hỏng sẵn từ mốc không phải lỗi của bạn.
- **Test thật là mặc định:** hệ thống thật, dữ liệu thật, model thật; được dùng tiền API cho đo / thử (ghi số thật, dùng hiệu quả). Đồ giả chỉ để test nhanh logic
  quanh model — không thay lượt thật khi nghiệm thu.
- **Soát tích hợp sau mỗi đợt gộp:** một phiên / agent con ngữ cảnh mới, chỉ đọc, tìm chỗ HAI tính năng gặp nhau mà test từng nhánh không bắt. Đề bài mẫu:
  "Liệt kê các cơ chế có thể cùng kích hoạt trong một lượt. Với mỗi cặp, đọc code xem thứ tự / điều kiện có làm kết quả sai, thiếu, trùng hay lệch log không. Chỉ
  báo điểm có `file:dòng` và một đầu vào tái hiện; cuối báo cáo ghi phần CHƯA đọc." Mỗi điểm phải tái hiện được rồi mới sửa [đã chạy 18/11: lần đầu, ra 11 điểm].
- **Soát độ thật của test:** định kỳ hỏi "test này bắt được lỗi gì thật?" — test chỉ khẳng định lại điều code vừa viết, hoặc giả luôn phần cần kiểm, thì sửa hoặc bỏ;
  test mới phải ĐỎ trên code cũ rồi mới xanh trên code sửa; phép kiểm mới phải thấy một ca "biết chắc hỏng" ra hỏng trước khi số 0 của nó được tin [chưa chạy].
- Rào chặn / từ chối người dùng: đo cả hai chiều — bắt được bao nhiêu và chặn nhầm bao nhiêu ca thường.

**Vì sao** — từng phần đều "test qua" mà ghép lại vẫn lệch (Coding W3D4·85; SDLC W2D3·52); agent viết test vô ích cho đủ số và dùng dữ liệu giả dù đã dặn
(Coding W1D5·32–34); agent sửa test cho qua, lời dặn chỉ giảm chứ không chặn (SDLC W2D3·49); test tự động dùng model giả, nghiệm thu bằng lượt model thật
(FDE W1D5·43); rào chắn đo hai chiều (FDE W3D2·97); lấy mốc trước khi sửa (Coding W2D1·37).
**Kiểm bằng gì** — báo cáo mục 4 ý 2 có đủ hai dòng "đồ giả" ↔ "lượt thật"; sau đợt gộp có file kết quả soát tích hợp.

## 7. Đo chính cách làm việc bằng hai con số

**Làm gì** — mỗi tuần ghi hai số vào trang hiện trạng của dự án: **(a) số việc đã báo "xong" bị lật lại** (User, reviewer hoặc máy tìm ra chưa xong) ·
**(b) số lần User phải nhắc lại một điều đã nói**. Muốn đổi cách làm (thêm phiên, thêm luật, đổi công cụ, đổi kiểu điều phối) ⇒ so hai số trước và sau, không
quyết theo cảm giác. Mẫu nhỏ nên chỉ tin chênh lệch rõ.
**Vì sao** — đo chất lượng cùng với tốc độ, không đếm dòng code hay token (SDLC tuần 2 — chưa kiểm mã bài); một lần chạy chỉ là một mẫu, thay đổi chỉ giữ khi
vượt mức lệch tự nhiên (FDE W2D5·78–83).
**Kiểm bằng gì** — hai số có trong trang hiện trạng mỗi tuần [chưa chạy — chưa có tuần nào được ghi].

## 8. Một phiên hay nhiều phiên: chọn theo gì (chưa phải luật)

Mặc định hợp lý là **một phiên + agent con**; phiên thứ hai mở để **kiểm** (mục 3). Nhiều phiên cùng viết code chỉ đáng khi: các phần không chung file · phần dùng
chung đã làm xong trước · User đọc kịp đầu ra của tất cả. Lợi thật của nhiều phiên là có người khác kiểm, không phải tốc độ gõ; giá là mỗi phiên phải đọc lại ngữ
cảnh và nhắn nhau. Agent con không thay người kiểm: kết quả của nó vẫn phải được kiểm (mục 1). Chọn kiểu nào thì đo bằng hai con số ở mục 7.
*Nguồn:* Coding W3D4·87–88, W3D5·89–93; SDLC W1D5·31–35, W2D2·45–46. *Ở repo gốc:* đã chạy kiểu bốn phiên; kiểu một phiên + agent con chưa thử có đo.

## 9. Phần của User

- Luôn đọc báo cáo; khi rảnh bấm thử theo ý "cách thử trong 2 phút"; việc xong thì tự thử và nêu ý kiến.
- Mỗi buổi chọn một dòng "xong" để agent chứng minh lại.
- Mỗi tuần nói lại bằng lời mình lý do của một quyết định đã chọn (không nói được ⇒ agent giải thích lại, chưa tính là đã quyết).
- Việc lớn: trước khi agent viết gì, User nói năm ý — vấn đề · ai dùng · thế nào là xong · không làm gì · điều tệ nhất chấp nhận được.
- Trả lời câu hỏi làm rõ của agent sớm; gửi gói review khác hãng khi đã soạn xong.

*Vì sao* — nút thắt đã dời từ viết code sang nói rõ muốn gì, phán đoán và chịu trách nhiệm (SDLC W1D1·6); dùng AI mà không chủ động hỏi để hiểu thì kém đi
(Coding W1D4·23–24).

## 10. Sở thích đã chốt của chủ dự án (agent nào cũng theo)

- Tiếng Việt, lời thường, thuật ngữ kèm nghĩa; **đủ quan trọng hơn ngắn**; không dùng mã nội bộ khi chưa giải nghĩa.
- Cần quyết định: **mỗi lần một câu**, có sẵn đáp án để chọn; mỗi đáp án kèm hệ quả, khi nào sai, chọn khác thì mất gì. Trong nhóm nhiều phiên: bàn nhóm trước rồi
  mới đưa một khuyến nghị; làm một mình: nêu luôn phương án ngược mạnh nhất cạnh khuyến nghị.
- Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật; không thêm rào, lớp, bước kiểm "phòng xa"; công sức tương xứng với tuổi thọ của phần đang làm.
- Việc đã chốt thì không hỏi lại, không trình lại như lỗi (mỗi dự án giữ một danh sách quyết định đã chốt).
- Số của người khác / agent con chuyển tiếp gắn "chưa kiểm" tới khi có người thứ hai tính lại. Giờ ghi vào tài liệu lấy bằng lệnh `date`, không ước.

## 11. Ở repo này (phần phải viết lại khi chép trang sang dự án khác)

| Trang nói | Ở repo này là |
|---|---|
| luật cứng + bảng quyền | `AGENTS.md` (3.207 byte — `wc -c AGENTS.md` [đã chạy 18/11]) |
| lệnh bật hệ thống, chạy test, lấy mốc | `guides/RUNBOOK_BAN_GIAO.md` mục 1–3 |
| "đã đẩy lên" lấy từ máy | `scripts/commit_push.sh "<lời commit>" <file>…` in `ĐÃ PUSH <sha> origin/<nhánh>` [đã chạy] |
| rào bằng máy mọi agent đều qua | `.githooks/pre-commit`, `pre-push`; kiểm đã bật: `git config --get core.hooksPath` ⇒ `.githooks` [đã chạy] |
| sổ giới hạn · danh sách quyết định đã chốt | runbook mục 10 · `session_prompt/Project_Status.md` mục 5 (runbook mục 9 chưa viết) |
| tài liệu viết cho người | `bai_hoc/` |
| trang hiện trạng · sổ việc | `session_prompt/Project_Status.md` · `session_prompt/CURRENT_HANDOFF.md` (hiện còn là nhật ký dài, chưa tách như mục 5 nói) |
| sao lưu thứ ngoài git trước khi sửa | runbook mục 5 [đã chạy ở mỗi lần sửa dữ liệu gốc] |
| làm một mình | `guides/KHI_CHI_CO_MOT_AGENT.md` |

## Chưa làm / chưa thử

- Trang này **chưa được thử với Codex hay Antigravity** — buổi thử: tối thứ Ba 24/11/2026; bước đầu của buổi là hỏi công cụ đã nạp file nào (mục 5).
- `AGENTS.md` chưa có dòng trỏ tới trang này ⇒ agent mở phiên theo `AGENTS.md` sẽ chưa đọc nó (chờ phiên điều phối thêm).
- Kiểu điều phối khi đổi công cụ **chưa chọn** (mục 8).
- Chưa từng chạy thành nếp: báo cáo bốn ý + nhãn độ tin (mục 4), soát độ thật của test (mục 6), hai con số (mục 7), năm ý của User trước việc lớn (mục 9).
- Mã bài trong các dòng "Vì sao": người giữ ghi chép từng khoá đã đối chiếu với ghi chép của mình (không ai mở lại bài giảng gốc cho trang này).
