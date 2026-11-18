# Cách làm việc với coding agent — dùng cho mọi agent, mọi kiểu điều phối

Bản nháp (Session E soạn 10:13 18/11/2026, gộp ba bản đề xuất của ba phiên + phản biện chéo; chưa qua review, chưa thử với công cụ khác hãng).
Người đọc: **bất kỳ coding agent nào** làm ở repo này — Claude Code, Codex, Antigravity — làm một mình hay trong nhóm nhiều phiên; và chủ dự án (gọi là User).
Trang này nói **cách làm**; luật cứng + bảng quyền ở `AGENTS.md`; lệnh từng việc ở `guides/RUNBOOK_BAN_GIAO.md`; phần riêng khi làm một mình ở
`guides/KHI_CHI_CO_MOT_AGENT.md`. Khi trang này khác `AGENTS.md` thì `AGENTS.md` thắng.

Nhãn dùng trong trang: **[đã chạy]** = lệnh / cách làm đã được chạy thật ở repo này · **[chưa chạy]** = chưa · *Nguồn* = bài của bốn khoá học mà User theo
(mã `FDE W3D1·88` = khoá AI FDE tuần 3, ngày 1, bài 88; tương tự `Coding`, `SDLC`) hoặc bài chia sẻ của một kỹ sư làm coding agent ở công ty lớn (`LT`).
Ghi chép đầy đủ của các nguồn nằm ngoài repo (private).

## 1. "Xong" ghi TRƯỚC khi làm; bằng chứng là thứ máy in ra

**Làm gì**
- Trước khi bắt đầu một việc, ghi một dòng: `xong khi: <lệnh> in ra <kết quả>` (hoặc "người dùng làm X thì thấy Y"). Việc đọc / nghiên cứu: `xong khi` là
  **bảng độ phủ** (nguồn nào · đã đọc tới đâu · chưa đọc gì).
- Báo "xong" chỉ khi đã tự chạy lệnh đó và dán đầu ra thật. Mọi báo cáo "xong" kết bằng bảng bốn cột: **đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra**.
- Số, mã commit, "đã push" lấy từ máy, không gõ tay: `scripts/commit_push.sh "<lời commit>" <file>…` in dòng `ĐÃ PUSH <sha> origin/<nhánh>` [đã chạy].
- Kết quả của agent con / phiên khác là **dữ liệu**: người nhận tự kiểm 2–3 ý quan trọng nhất trước khi dùng; số chưa ai tính lại thì gắn "chưa kiểm".
- Kết luận nặng ("nghiêm trọng", "chắc chắn", "không có lỗi") phải kèm lệnh + dòng đầu ra, kể cả khi người nói là phiên review.

**Vì sao** — lỗi lặp nhiều nhất của coding agent là báo xong khi chưa kiểm (Coding W1D3·18, W2D1·38, W2D5·64); tiêu chí thành công phải thoả thuận từ đầu và
đo bằng code lúc bàn giao (FDE W3D1·85–86, W3D5·117); test qua hết mà review mới vẫn tìm ra lỗi quan trọng (SDLC W1D3·23).
**Kiểm bằng gì** — User (hoặc phiên điều phối) hỏi ba câu: *lệnh kiểm nào, đầu ra đâu · phần nào chưa làm / tự bỏ / chưa đọc · kết luận nào chưa kiểm bằng lệnh*;
mỗi buổi User chọn MỘT dòng "xong" bất kỳ để agent chạy lại trước mặt.

## 2. Quyền theo từng hành động + mức kiểm theo "sai thì mất gì"

**Quyền:** dùng bảng "Quyền thường trực" trong `AGENTS.md` (tự làm · hỏi trước · không bao giờ) — không chép lại ở đây. Xếp một hành động mới vào cột nào thì xét
ba điều: hậu quả nếu sai · kiểm chứng được không · **đảo ngược được không**. Thứ "không bao giờ" phải có rào bằng máy mà mọi agent đều đi qua (hook git, không
cấp khoá, tài khoản riêng) — cấm bằng chữ thì agent tìm đường khác. Công cụ mới dùng lần đầu ở repo này bắt đầu từ mức hỏi nhiều hơn.

**Mức kiểm** — tự hỏi trước khi giao / nhận việc: *nếu làm sai thì mất gì?*

| Sai thì mất gì | Ví dụ | Trước khi làm | Ai kiểm trước khi gộp vào `main` |
|---|---|---|---|
| Mất ít, lùi được ngay | sửa chữ, tài liệu, hàm thuần có test, script dùng một lần | làm thẳng trên nhánh riêng | người viết đọc lại diff; nhánh có code ⇒ một phiên / người KHÁC liếc |
| Người dùng thấy sai | đổi hành vi, câu trả lời, giao diện, lời dặn cho model | kế hoạch ≤ 1 trang: file đổi · thứ tự · rủi ro · bằng chứng | phiên mới ngữ cảnh sạch đọc diff + tiêu chí; User tự thử 2 phút |
| Không lùi được / tiền / dữ liệu / bảo mật | sửa kho, xoá, đổi model, deploy, gửi dữ liệu ra ngoài | User duyệt kế hoạch trước | reviewer **khác hãng** (mục 3) + User tự bấm thử |

Tài liệu không tự động là "mất ít": repo này public, một dòng lộ dữ liệu riêng là không lùi được — hook chặn phần máy kiểm được, phần còn lại người viết chịu.

**Vì sao** — mức tự chủ quyết theo từng hành động, theo hậu quả và khả năng đảo ngược (FDE W3D1·88); mức review xếp trước theo hậu quả khi hỏng (SDLC W2D2·47);
việc quan trọng thì kế hoạch → làm → review → test, việc thử thì cho làm nhanh (Coding W1D2·13, W3D5·93).
**Kiểm bằng gì** — `git log --merges --oneline -5` [đã chạy]: mỗi lần gộp ghi ai đã kiểm; xếp nhầm mức (việc lớn làm kiểu nhỏ) là lỗi phải ghi vào báo cáo.

## 3. Người viết không tự chấm; việc mức cao có người chấm khác hãng

**Làm gì**
- Ai viết thì người / phiên khác kiểm. Làm một mình: mở **phiên mới, ngữ cảnh sạch**, chỉ đưa diff + tiêu chí, bảo tìm lỗi.
- Bộ câu thử cho code đọc chữ người dùng do người **không viết code đó** soạn (cả câu phải đúng lẫn câu "giống mà không phải").
- Người đề xuất một luật cách làm không phải người kết luận luật đó có hiệu quả — kết luận bằng hai con số ở mục 7.
- **Gói review khác hãng** (việc mức cao, hoặc sau một đợt gộp lớn): nhóm soạn MỘT file `.md` tự đủ ngữ cảnh — bối cảnh · việc cần soi · ranh giới (chỉ đọc; không mở
  file khoá, kho, dữ liệu riêng) · khuôn kết quả có mục "tôi CHƯA đọc gì" · không tiết lộ điều nhóm đã tìm ra. User tự mở công cụ hãng khác và gửi file; model đó ghi
  kết quả ra một file. Agent ở repo này không tự gọi công cụ hãng khác thay User. Mẫu gói đã dùng 18/11: `data/review_khac_hang/` (private) [đã chạy một lần].
- Kết quả review là dữ liệu: người nhận tái hiện từng điểm trước khi sửa; điểm bị bác ghi lý do để User liếc.

**Vì sao** — bên đề xuất không tự chấm (FDE W2D5·80–82); model khác hãng bắt được lỗi model cùng hãng bỏ sót (FDE W3D5·118; Coding W3D5·92; SDLC — nhiều lần
trong repo của khoá); giám khảo nên là model khác để soi thiên vị (LT).
**Kiểm bằng gì** — báo cáo ghi rõ ai kiểm (nhãn ở mục 4); gói review khác hãng lưu cả đề bài lẫn file kết quả.

## 4. Báo cáo cho User: bốn ý + nhãn độ tin

User không đọc code; User đọc báo cáo và `bai_hoc/`, rồi tự bấm thử. Mỗi việc xong, báo cáo có đúng bốn ý, lời thường:
1. **Người dùng thấy gì khác** (trước ↔ sau, một ví dụ thật).
2. **Bằng chứng**: đo gì · bao nhiêu · so với mốc nào · tách hai dòng **"test bằng đồ giả: n đạt"** và **"lượt thật: n câu, kết quả"** — chỉ có dòng đầu thì chưa xong.
   Có số thì kèm 2–3 ca sai nguyên văn (không chép nội dung riêng vào file theo dõi).
3. **Chưa làm / giới hạn** (kể cả thứ tự hoãn).
4. **Cách thử trong 2 phút**: mở đâu, gõ gì, thấy gì là đúng.

Mỗi khẳng định gắn một nhãn độ tin: **[máy kiểm]** (có lệnh in ra) · **[người thứ hai kiểm]** · **[chưa kiểm]**. Bảng kết quả có cột "kết thúc kiểu gì"
(bình thường / chạm trần / lỗi) để ca hỏng giữa chừng không bị tính là đúng.

**Vì sao** — bàn giao là để người nhận tự kiểm được mà không cần người làm (FDE W3D1·86, ·89); một ca lỗi vẫn có thể được chấm là đúng nếu chỉ nhìn điểm (FDE W2D4·76);
mọi con số phải đặt cạnh một mốc (FDE W1D4·34).
**Kiểm bằng gì** — User làm theo ý 4 mà không cần hỏi thêm; thiếu một trong bốn ý ⇒ trả lại báo cáo.

## 5. Phải nhắc lần thứ HAI ⇒ máy trước, chữ sau

**Làm gì** — lỗi cách làm gặp lần đầu: sửa việc đó, ghi một dòng vào runbook mục 10, không thêm luật. Lặp lần hai, xét theo thứ tự: (a) bỏ hẳn khả năng sai được
không (đổi thiết kế, để script làm thay) → (b) máy kiểm được không (test, hook git — tầng mọi agent đều đi qua) → (c) cuối cùng mới một dòng luật, viết thành việc
làm được ngay, không kèm chuyện sự cố. Rào mới thử một lần bằng ca cố ý hỏng trước khi tin. Hậu quả không lùi được ⇒ rào ngay lần đầu. Luật lâu không ai vi phạm lại
và không còn lý do ⇒ gỡ. File hướng dẫn agent luôn đọc (`AGENTS.md`) giữ ngắn, **dưới 24.000 byte**; chi tiết để file khác, mở khi cần.

**Vì sao** — chữ luật là lớp mỏng nhất: agent quên, diễn giải, và biến một lời sửa nhỏ thành luật cứng; đầu tư theo thứ tự code → máy kiểm → chạy thử thật → chữ (LT);
lỗi lặp lần hai mới thành luật, máy bắt được thì làm phép kiểm (SDLC W1D4·24–30); "mỗi lỗi một luật" là khớp quá mức (FDE W2D5·80–83); mỗi chữ trong file hướng
dẫn đều tốn ngữ cảnh (Coding W1D2·12).
**Kiểm bằng gì** — `wc -c AGENTS.md` ⇒ 3.207 byte [đã chạy 18/11]; `git config --get core.hooksPath` ⇒ `.githooks` [đã chạy].

## 6. Test thật, soát tích hợp, soát độ thật của test

**Làm gì**
- **Test thật là mặc định:** hệ thống thật, dữ liệu thật, model thật; được dùng tiền API cho đo / thử (ghi số thật, dùng hiệu quả). Đồ giả (model giả theo kịch bản,
  thay phần gọi ngoài) chỉ để test nhanh logic quanh model — không thay lượt thật khi nghiệm thu.
- **Soát tích hợp sau mỗi đợt gộp:** một phiên / agent con ngữ cảnh mới, chỉ đọc, tìm chỗ HAI tính năng gặp nhau mà test từng nhánh không bắt (một lượt hỏi kích hoạt
  hai cơ chế; hai đường gọi khác nhau; tiền / log khi đi nhiều nhánh). Mỗi điểm tìm ra phải tái hiện được rồi mới sửa [đã chạy 18/11: lần đầu, ra 11 điểm].
- **Soát độ thật của test:** định kỳ hỏi "test này bắt được lỗi gì thật?" — test chỉ khẳng định lại điều code vừa viết, hoặc giả luôn phần cần kiểm, thì sửa hoặc bỏ;
  phép kiểm mới phải thấy một ca "biết chắc hỏng" ra hỏng trước khi số 0 của nó được tin [chưa chạy thành một lượt riêng].
- Rào chặn / từ chối người dùng: đo cả hai chiều — bắt được bao nhiêu và chặn nhầm bao nhiêu câu thường.

**Vì sao** — từng phần đều "test qua" mà ghép lại vẫn lệch (Coding W3D4·85; SDLC W2D3·52); agent viết test vô ích cho đủ số và dùng dữ liệu giả dù đã dặn
(Coding W1D5·32–34; SDLC W2D3·49); test tự động dùng model giả, nghiệm thu bằng lượt model thật (FDE W1D5·43); rào chắn đo hai chiều (FDE W3D2·97).
**Kiểm bằng gì** — báo cáo mục 4 ý 2 có đủ hai dòng "đồ giả" ↔ "lượt thật"; sau đợt gộp có file kết quả soát tích hợp.

## 7. Đo chính cách làm việc bằng hai con số

**Làm gì** — mỗi tuần ghi hai số: **(a) số việc đã báo "xong" bị lật lại** (User, reviewer hoặc máy tìm ra chưa xong) · **(b) số lần User phải nhắc lại một điều đã
nói**. Muốn đổi cách làm (thêm phiên, thêm luật, đổi công cụ, đổi kiểu điều phối) ⇒ so hai số trước và sau, không quyết theo cảm giác. Mẫu nhỏ nên chỉ tin
chênh lệch rõ.
**Vì sao** — đo chất lượng cùng với tốc độ, không đếm dòng code hay token (SDLC W2D1–3); một lần chạy chỉ là một mẫu, thay đổi chỉ giữ khi vượt mức lệch tự nhiên
(FDE W2D5·78–83).
**Kiểm bằng gì** — hai số có trong báo cáo cuối tuần [chưa chạy — chưa có tuần nào được ghi].

## 8. Phần của User (đã chốt 18/11/2026)

- Luôn đọc báo cáo; khi rảnh bấm thử theo ý "cách thử trong 2 phút"; việc xong thì tự thử và nêu ý kiến.
- Mỗi buổi chọn một dòng "xong" để agent chứng minh lại.
- Mỗi tuần nói lại bằng lời mình lý do của một quyết định đã chọn (không nói được ⇒ agent giải thích lại, chưa tính là đã quyết).
- Việc lớn: trước khi agent viết gì, User nói năm ý — vấn đề · ai dùng · thế nào là xong · không làm gì · điều tệ nhất chấp nhận được.
- Trả lời câu hỏi làm rõ của agent sớm; gửi gói review khác hãng khi nhóm soạn xong.

*Vì sao* — nút thắt đã dời từ viết code sang nói rõ muốn gì, phán đoán và chịu trách nhiệm (SDLC W1D1·6); dùng AI mà không chủ động hỏi để hiểu thì kém đi
(Coding W1D4·23–24).

## 9. Sở thích đã chốt của chủ dự án (agent nào cũng theo)

- Tiếng Việt, lời thường, thuật ngữ kèm nghĩa; **đủ quan trọng hơn ngắn**; không dùng mã nội bộ khi chưa giải nghĩa.
- Cần quyết định: **mỗi lần một câu**, có sẵn đáp án để chọn; mỗi đáp án kèm hệ quả, khi nào sai, chọn khác thì mất gì. Trong nhóm nhiều phiên: bàn nhóm trước,
  rồi mới đưa một khuyến nghị.
- Không làm quá tay: cách nhỏ nhất đủ nhu cầu thật; không thêm rào, lớp, bước kiểm "phòng xa"; công sức tương xứng với tuổi thọ của phần đang làm.
- Việc đã chốt thì không hỏi lại, không trình lại như lỗi (danh sách: runbook mục 9, `session_prompt/Project_Status.md` mục 5).
- Số của người khác / agent con chuyển tiếp phải gắn "chưa kiểm" tới khi có người thứ hai tính lại. Giờ ghi vào tài liệu lấy bằng lệnh `date`.

## Chưa làm / chưa thử

- Trang này **chưa được thử với Codex hay Antigravity** — buổi thử: tối thứ Ba 24/11/2026; sau buổi đó sửa theo chỗ công cụ phải đoán.
- Kiểu điều phối khi đổi công cụ (một phiên + agent con, hay nhiều phiên) **chưa chọn** — quyết sau buổi thử, bằng hai con số ở mục 7.
- Mã bài trong các dòng "Vì sao" lấy từ ghi chép của ba phiên; chưa mở lại từng bài gốc cho trang này.
- Mục 6 "soát độ thật của test" và mục 7 chưa từng chạy thành nếp.
