# Bài 39 — Đồ án được làm thế nào: một người quyết định và nhiều coding agent

*Cập nhật 20:46, ngày 23/11/2026 · số kho / số tính năng / mức test theo hệ thống lúc code đứng yên tối 23/11 (57 tính năng mở, 6 tắt, kho 269 bài) · bản 12:18: thêm một dòng vào bảng sự cố — lượt "dùng như người thật" trên trình duyệt thành bước thường xuyên (kể đủ ở bài 38) · từ trang hiện trạng, sổ việc, bảng quyền, lịch sử code · các lần sửa trước: khối Nguồn.*

**Bài trước đã biết:** hệ thống gồm những khối nào, đo bằng gì, và bộ test kiểm những gì (bài 38).
**Bài này thêm:** ai làm ra hệ thống đó: ai quyết gì, việc ghi ở đâu, ai kiểm ai, và cách làm đã bị sửa ra sao sau từng sự cố.

## Ý chính

- **Một người quyết, nhiều coding agent làm.** Chủ dự án nêu kết quả muốn có và quyết phạm vi, kho, tiền, model, việc đưa lên mạng. Các phiên chia vai điều phối, thực thi, đo, giảng; agent con làm từng phần việc nhỏ.
- **Trạng thái nằm trong file, không trong trí nhớ của agent:** trang hiện trạng, sổ việc, danh sách ý chưa thử, file luật chung.
- **Quyền chia ba cột:** tự làm, hỏi trước, không bao giờ. Mỗi thay đổi đo được là một thí nghiệm (bài 20).
- **Người viết không tự duyệt.** Phiên khác đọc và chạy lại lệnh kiểm; agent con ngữ cảnh sạch đối chiếu; ở mốc chốt, AI hãng khác soát. Thứ máy nhận ra được (file riêng tư, dòng trông như khoá, chữ chép từ bộ câu chấm cất riêng) thì máy chặn ở mỗi lần lưu code; phần còn lại dựa vào luật chữ.
- **Cách làm được sửa theo sự cố có ghi:** báo "xong" sai, kiểm thử quá nhiều, chủ dự án phải tự gợi hướng.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| phiên | **session** | một lần mở một coding agent (Claude Code, Codex, Antigravity) trong một cửa sổ riêng; đóng cửa sổ là phiên mất hết điều nó đang nhớ |
| agent con | **sub-agent** | agent do một phiên tạo ra cho một phần việc; nó chỉ biết đúng điều ghi trong lời giao |
| kho code, lưu | **repository**, **commit** | nơi giữ mọi phiên bản của chương trình; "lưu" là ghi một phiên bản mới. Kho code của dự án để công khai trên GitHub |
| nhánh, gộp | **branch**, **merge** | một bản chép để sửa thử mà không đụng bản đang chạy; "gộp" là đưa phần sửa vào bản chính |
| skill | **skill** | file hướng dẫn một quy trình, agent mở khi cần |
| soát khác hãng | **cross-vendor review** | đưa một đề bài viết sẵn cho model của hãng khác, để nó đọc code và tìm lỗi |
| rào bằng máy | **git hook** | đoạn chương trình tự chạy mỗi lần lưu hay đẩy code, chặn thứ không được lọt |

## Một người quyết, năm phiên làm theo vai

**Chủ dự án** không đọc code. Anh nêu kết quả muốn có, quyết các việc thuộc cột "hỏi trước", đóng từng giai đoạn. Lời quyết được chép nguyên văn kèm giờ.

**Các phiên** lúc viết bài có năm vai. **Điều phối:** nói chuyện với chủ dự án, chia việc, giữ sổ, gộp thay đổi. Hai phiên **thực thi:** viết code, sửa lỗi, đọc code của nhau. **Đo:** chạy lượt thật qua trình duyệt, cả bộ test, lượt kiểm chốt. **Giảng:** viết giáo trình này, chỉ đọc code. Các phiên nhắn thẳng cho nhau. Việc sửa code do phiên điều phối chia, để hai phiên không sửa chồng một file; việc nghĩ, đếm trên dữ liệu đã có, nêu hướng khác thì phiên nào cũng tự làm. **Agent con** đọc nhiều file, đối chiếu một bài với code, hay chấm mù; kết quả của nó là dữ liệu, người nhận kiểm lại.

**Công cụ đã đổi.** Phase 0–6 (05/08 – 22/10) do Antigravity (model Gemini) viết, Codex kiểm. Từ 23/10 các phiên Claude Code làm; Codex còn dùng để tra thông tin công khai. Agent không tự gọi Antigravity: điều khoản của Google cấm. Dòng thời gian các phase ở nửa để tra.

## Trạng thái nằm trong file, không trong trí nhớ của agent

Phiên đóng là mất trí nhớ, như model giữa hai lần gọi (bài 1). Nên thứ phiên mới cần biết nằm trong file của kho code, đọc theo thứ tự cố định khi mở phiên:

- **Trang hiện trạng:** đang chạy gì, mốc nào, quyết định nào còn hiệu lực; viết lại tại chỗ.
- **Sổ việc:** nơi duy nhất ghi việc đang mở, ai làm, bước kế.
- **Danh sách ý chưa thử:** hướng chưa ai giao, kèm phép đếm rẻ nhất để biết ý đúng hay sai; lúc viết có khoảng 50 ý.
- **File luật chung** (bảy luật cứng, bảng quyền, cách nhìn việc) cho mọi agent, và **11 skill**.

## Quyền chia ba cột, và mỗi thay đổi là một thí nghiệm

Từ 10:11 ngày 18/11, chủ dự án duyệt một bảng quyền dùng lâu dài cho mọi coding agent:

| Cột | Gồm |
|---|---|
| **Tự làm, báo sau** | việc đã có trong sổ việc; sửa lỗi đã tái hiện được; lưu và đẩy nhánh riêng; gộp khi phiên khác đã kiểm; dùng agent con; tiền gọi model cho đo, thử (ghi số thật) |
| **Hỏi chủ dự án trước** | tính năng mới, đổi hướng sản phẩm; đổi lớn thứ người dùng thấy; sửa nội dung kho; xoá dữ liệu; gửi dữ liệu ra dịch vụ mới; một việc dự kiến trên 1 USD; đưa lên mạng |
| **Không bao giờ** | đọc file khoá; đưa dữ liệu riêng lên kho code công khai; mở bộ câu chấm cất riêng khi không được giao; tự gọi Antigravity; ép đẩy đè lịch sử; bỏ qua rào bằng máy |

**Mỗi thay đổi ở một khâu đo được là một thí nghiệm** (bài 20): ghi điều kiện trước, đổi một thứ, so với mốc, lần thử bị bỏ cũng được đánh dấu trong lịch sử code để tra (hiện có 20 dấu), đếm trước khi xây.

**Báo "xong" theo một khuôn:** bảng người dùng làm được / chưa làm được, việc chưa làm, việc tự hoãn, lệnh kiểm cùng đầu ra thật; mỗi khẳng định mang nhãn **máy kiểm**, **người thứ hai kiểm** hoặc **chưa kiểm** (quyết định 6).

## Người viết không tự duyệt: ba lớp kiểm và một lớp máy

**Lớp 1, phiên khác đọc** thay đổi và tự chạy lại lệnh kiểm của ít nhất một dòng "xong" trước khi gộp.

**Lớp 2, agent con ngữ cảnh sạch đối chiếu**, ví dụ mỗi bài giáo trình. Lớp này cũng sai (ví dụ ở nửa để tra).

**Lớp 3, soát khác hãng ở mốc chốt.** Nhóm soạn một file đề bài tự đủ; chủ dự án tự mở công cụ hãng khác và đưa file đó. Từ tối 22/11 đề bài phải mang đủ trạng thái của dự án, một danh sách nên đọc, và cả những điểm nhóm đã tìm ra ("Chi tiết để tra"). Trưa 22/11, ba bên (GPT-6, Gemini 4 Neon, Gemini 4 Carbon) soát những chỗ hai tính năng mới cùng chạy trong một lượt hỏi, nơi kiểm từng tính năng riêng không thấy lỗi, nêu 33 điểm. Cách xử theo luật chủ dự án chọn ngày 20/11: người viết phần code đó tái hiện từng điểm và **đếm trước** số lượt thật gặp nó; lỗi người dùng dễ gặp, lỗi an toàn, lỗi ghi sai kho thì sửa; lỗi hiếm thì ghi một dòng giới hạn kèm con số; không soát vòng hai (ví dụ ở nửa để tra).

**Rào bằng máy** soát mỗi lần lưu và đẩy code: file vùng riêng tư, dòng trông như khoá, tên dự án khác của chủ dự án; lúc lưu còn chặn dòng trùng từ 40 ký tự liên tiếp với bộ câu chấm cất riêng (bài 37; quyết định 5 bên dưới). Nó nằm trong kho code, nên áp cho mọi agent và cả người.

## Cách làm đã bị sửa nhiều lần, mỗi lần vì một sự cố có ghi

| Sự cố | Sửa thành |
|---|---|
| 24/10: mỗi lần mở, một phiên phải đọc khoảng 2.000 dòng luật; mọi việc dồn qua một sổ nên không chạy song song được | nhiều phiên theo vai, kiểm chéo, quy trình theo mức rủi ro |
| 25 và 26/10: lệnh quét trùng nối với lệnh lưu; quét báo trùng mà lưu vẫn chạy | phép quét đưa vào rào bằng máy |
| 09/11: một loạt tính năng thử ra âm; 15/11: tính năng ảnh làm lại bốn bản một tối vì code trước khi rõ đề | đếm lỗi rẻ trước khi xây; việc lớn chốt đề bằng năm dòng |
| 17–18/11: bốn phiên báo "đã đọc đủ" đều còn sót; "3 test đạt" thật là 2 đạt, 1 hỏng | bảng quyền; nhãn độ tin; "xong" kèm lệnh và đầu ra |
| 18/11: một bản sửa an toàn qua review cùng hãng; Gemini chỉ ra nó ghi sai kết cục và làm mất một dòng gợi ý | soát khác hãng ở mốc chốt |
| 21–22/11: chủ dự án nhắc kiểm thử quá nhiều; sáng 22/11 cả bộ test chạy bốn lần, bắt 0 lỗi mới | liều lượng theo rủi ro, không con số cố định; cả bộ test một lần cuối đợt |
| 21/11: ít nhất 12 lần trong khoảng bốn tuần chủ dự án phải tự gợi một hướng nhóm lẽ ra phải nêu | "nghĩ rộng, đừng chờ dắt"; ba ngày thử nhóm tự giữ luật cách làm |
| 22 và 23/11: chủ dự án hai lần nhắc thử sản phẩm bằng công cụ cho agent tự lái trình duyệt | thêm lượt "dùng như người thật" sau mỗi đợt gộp thứ người dùng thấy; lượt đầu ra ba điều mới mà bộ chụp soạn sẵn không thấy (bài 38) |

Chủ dự án dặn tối 21/11: "phần này cũng nên linh hoạt chứ đừng cố định nhé… tôi sợ vấn đề này ảnh hưởng đến chất lượng dự án". Trong khoảng bốn tuần anh nhắc chuyện làm quá tay 9 lần, 7 lần về kiểm soát (rào, vòng review, đo lặp). Về hướng đi, lời anh ngày 21/11: "các bạn phải tự suy nghĩ rộng ra… chứ không phải đi theo hướng của tôi mà để tôi dắt các bạn đi vào ngõ cụt"; từ đó hướng anh nêu là một gợi ý để xét. Luật chung: sự cố lần đầu thì ghi lại, lặp lần hai mới thành luật, máy kiểm được thì làm phép kiểm thay chữ.

## Quyết định và lý do

Đây là quyết định về **cách làm**.

### 1. Vì sao chia nhiều phiên theo vai, mà không để một agent làm hết?

- **Đã chọn:** từ 24/10 một phiên điều phối và các phiên thực thi kiểm chéo nhau (chủ dự án duyệt ngày 24/10); phiên giảng có từ cuối tháng 10, phiên đo từ 05/11.
- **Vì sao:** sự cố 24/10 ở bảng trên, cộng một vấn đề nữa thiết kế ghi: không có chỗ giữ ngữ cảnh riêng của từng phiên. Luật "ai làm thì người khác kiểm" cần ít nhất hai phiên (lập luận của người viết).
- **Cách khác:** một phiên cộng agent con, hoặc hai phiên (một làm, một kiểm): chưa thử.
- **Cái giá:** tầng phối hợp tốn: một phép đếm thô theo đường dẫn file ngày 21/11 thấy một tháng có 1.770 lần lưu code, chỉ 28 % chạm code sản phẩm. Máy ít bộ nhớ, nên mỗi phiên chạy nhiều nhất hai tiến trình nặng.

### 2. Vì sao trạng thái ghi vào file, mà không để agent tự nhớ?

- **Đã chọn:** trang hiện trạng, sổ việc, file luật chung và rào bằng máy, tất cả trong kho code.
- **Vì sao:** phiên đóng là mất trí nhớ; nhóm ghi rằng cách làm phải đúng với bất kỳ agent nào, bất kỳ lúc nào.
- **Cách khác:** giữ luật trong phần nhớ riêng của một công cụ: không làm, agent khác không đọc được.
- **Cái giá:** sổ phình nhanh, phải viết lại thường xuyên (18/11: sổ việc khoảng 176 nghìn byte).

### 3. Vì sao quyền chia ba cột, và cột "hỏi trước" phải ngắn?

- **Đã chọn:** bảng quyền dùng lâu dài; cột "hỏi trước" chỉ giữ việc không lùi được hoặc tốn tiền.
- **Vì sao:** trước 18/11, mỗi phiên lại hỏi chủ dự án cùng một câu về quyền. Luật nhóm rút từ ghi chép khoá học: bị hỏi quá nhiều thì người duyệt bấm đồng ý theo quán tính. Ba ngày sau (21/11), chủ dự án tự xác nhận: "khi các bạn đề xuất luật cho tôi thì tôi toàn chọn chứ không đọc và đọc không hiểu".
- **Cách khác:** hỏi quyền từng phiên: cách cũ, đã bỏ.
- **Cái giá:** agent tự làm nhiều việc, chủ dự án biết qua báo cáo.

### 4. Vì sao người kiểm phải khác người viết, và ở mốc chốt phải khác cả hãng?

- **Đã chọn:** không phiên nào tự duyệt việc của nó; ở mốc chốt thêm soát khác hãng, mọi điểm được tái hiện trước khi tin.
- **Vì sao:** sự cố 18/11 ở bảng trên. Cùng đợt, ba bên soát mù một việc ra 11, 6 và 7 điểm (thêm 1 nghi vấn), gần như không trùng.
- **Cách khác:** tự duyệt: luật cứng cấm. Soát vòng hai sau khi sửa: không làm (chủ dự án chọn 20/11).
- **Cái giá:** thêm thời gian; giám khảo cũng nói quá.

### 5. Vì sao chặn bằng máy, thay vì dặn bằng chữ?

- **Đã chọn:** rào chạy mỗi lần lưu và đẩy code.
- **Vì sao:** sự cố 25 và 26/10: luật chữ "nhớ quét" đã có mà vẫn lọt. Một dòng riêng tư đã lên lịch sử công khai thì coi như không gỡ được. Sau khi có rào, sổ ghi ít nhất 4 lần chặn đúng.
- **Cách khác:** dặn bằng chữ: cách cũ, lọt hai lần.
- **Cái giá:** rào chỉ bắt thứ máy nhận ra (dạng khoá, tên, chuỗi trùng); mô tả quá cụ thể vẫn lọt ít nhất 4 lần. Phép chặn 40 ký tự từng chặn cả giáo trình trích ví dụ kho; từ 16:45 22/11 chủ dự án chọn chỉ áp nó cho bộ câu chấm cất riêng (kho và bộ câu mẫu đã công khai từ 20/11). Sau này muốn giấu lại kho hay bộ câu mẫu thì các đoạn đã trích phải gỡ tay.

### 6. Vì sao chữ "xong" phải kèm lệnh và đầu ra?

- **Đã chọn:** ghi "xong khi" trước; báo kèm đầu ra thật và nhãn độ tin; từ 20/11 báo bằng bảng người dùng làm được / chưa làm được (chủ dự án chọn).
- **Vì sao:** chủ dự án không đọc code, mọi thứ dựa vào lời báo; mà lời báo đã sai có hồ sơ (17–18/11).
- **Cách khác:** báo bằng lời kể: cách cũ.
- **Cái giá:** báo cáo dài hơn.

## Nếu… thì sao

| Nếu | Nhóm làm gì | Đã có chưa |
|---|---|---|
| một phiên báo "xong" mà sai | người đọc chạy lại lệnh kiểm trước khi gộp; sai thì trả lại | có |
| một agent định lưu file riêng tư | rào dừng lần lưu, in "pre-commit: CHẶN — file thuộc vùng private (không commit lên repo public):" | có |
| hai phiên cùng sửa một file | phiên điều phối chia việc theo file | có luật, chưa có rào |
| việc thuộc cột "hỏi trước" khi chủ dự án vắng | gác lại; trình một lần, mỗi lần một câu | có, từ 22/11 |

## Dễ nhầm

- **"Agent viết hết, chủ dự án chỉ bấm đồng ý."** Phạm vi, kho, tiền, model, đưa lên mạng là việc của chủ dự án.
- **"Đã có test và review thì không cần soát khác hãng."** Ngày 18/11 và 22/11, nó tìm ra điểm mọi lượt kiểm trước bỏ sót.
- **"Agent con đã kiểm thì chắc đúng."** Bảng đính chính của agent con lệch 4 trên 45 dòng.

## Câu hỏi tự kiểm

<details>
<summary>1. Vì sao trạng thái dự án phải ghi trong file?</summary>

Phiên đóng là mất trí nhớ, và cách làm phải đúng với mọi agent; phiên nào mở ra cũng đọc cùng các file đó.

</details>

<details>
<summary>2. Kể ba cột của bảng quyền, mỗi cột một ví dụ.</summary>

Tự làm: sửa lỗi đã tái hiện được. Hỏi trước: sửa nội dung kho. Không bao giờ: đọc file khoá.

</details>

<details>
<summary>3. Vì sao người kiểm cùng hãng là chưa đủ?</summary>

Cùng model có thể chung điểm mù: ngày 18/11 một bản sửa an toàn qua review cùng hãng, Gemini chỉ ra nó ghi sai kết cục.

</details>

<details>
<summary>4. Soát khác hãng nêu một lỗi; sửa hay chỉ ghi giới hạn?</summary>

Tái hiện, đếm số lượt thật gặp nó. Lỗi người dùng dễ gặp, an toàn, ghi sai kho thì sửa; hiếm thì ghi giới hạn kèm con số.

</details>

## Cấu hình đang chạy

*Cách làm lúc viết, trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao | Đã thử giá trị khác chưa |
|---|---|---|---|
| Số phiên | 5: điều phối, hai thực thi, đo, giảng | chủ dự án trả lời "bao nhiêu cũng được" (21/11) | một phiên, bốn phiên đã dùng ở các đợt trước; chưa so có đo |
| Công cụ của các phiên | Claude Code; Codex để tra web công khai | thiết kế 24/10 ghi các phiên dùng Claude Opus 5.5 | Phase 0–6: Antigravity viết, Codex kiểm |
| Bảng quyền | ba cột, từ 10:11 ngày 18/11 | quyết định 3 | trước đó hỏi từng phiên |
| Trần tiền | một việc dự kiến trên 1 USD thì hỏi trước | tiền chỉ đo và báo, không làm thước cắt chất lượng (19/11) | trước 18/11 có trần theo từng phiên |
| Luật cách làm | nhóm tự giữ trong ba ngày làm việc thử từ 21/11; chủ dự án giữ mục tiêu, luật cứng, bảng quyền | quyết định của chủ dự án 16:05 ngày 21/11 | tới 20/11 chủ dự án duyệt từng luật |
| Soát khác hãng | ở mốc chốt; mặc định GPT và Gemini; chủ dự án gửi | quyết định 4 | — |
| Rào bằng máy | lúc lưu và lúc đẩy code | quyết định 5 | — |
| Skill | 11 file | mỗi quy trình một file, agent mở khi cần | chấm thử 18/11: chưa kết luận được skill có giúp không |

## Giới hạn đã biết

- **Chưa so một phiên với nhiều phiên** bằng phép đo nào.
- **Chưa thử để Codex hay Antigravity làm phiên thực thi** với bộ luật hiện tại; luật mới được các phiên Claude đọc.
- **Rào bằng máy không chặn việc đọc.** Luật cấm đọc file khoá chặn đường đọc trực tiếp, nhưng một đoạn chương trình tự mở file vẫn đọc được (kiểm bằng file giả ngày 18/11). Bộ câu chấm cất riêng chỉ được giữ bằng luật chữ.
- **Người chấm câu trả lời là model**; từ tối 21/11 là chính model đang chạy, nên có thể chấm dễ hơn (bài 33).
- **Ba ngày thử "nhóm tự giữ luật" chưa có kết quả xét lại** lúc viết.

## Chi tiết để tra

**Dòng thời gian các phase**

| Lúc | Giai đoạn |
|---|---|
| 05/08 – 22/10 | Phase 0–6: kho bài, máy chủ, cắt đoạn, vector và từ khoá, Qdrant, cách tìm, viết câu trả lời, giao diện đầu (Antigravity viết, Codex kiểm) |
| 23 – 24/10 | Phase 7: bộ 176 câu mẫu, công cụ chấm, điểm mốc; 24/10 đổi sang nhiều phiên Claude |
| 24 – 28/10 | Phase 8.1–8.2: rà lại các quyết định cũ bằng thí nghiệm; rà lại toàn bộ code; đưa phương án thắng (10 đoạn) vào |
| 31/10 – 01/11 | đóng gói Phase 1–8: chữ hiện dần, lượt đo cuối; chủ dự án đóng Phase 8 ngày 01/11 |
| từ 02/11 | Phase 9: trợ lý có công cụ, lên kế hoạch, sửa lịch bằng lời |
| từ 05/11 | chủ dự án chia thêm Phase 10 (ảnh, giọng nói), 11 (bản đồ, sự kiện theo ngày, ăn gần, ứng xử), 12 (trang theo dõi, đề xuất sửa kho, đưa lên mạng) |
| 18/11 | bảng quyền thường trực; soát mù ba hãng lần đầu |
| 21/11 | đổi tạm model viết sang Claude Sonnet 5.5 (bài 33); ba ngày thử nhóm tự giữ luật cách làm; giao viết giáo trình |
| 22/11 | phần xây của Phase 9–12 xong ở máy; soát ba hãng; lượt kiểm chốt |

- Lịch sử lưu code: 2.762 lần, từ 05/08 tới trưa 22/11/2026.
- Đề bài cho AI khác hãng: mẫu đổi tối 22/11 theo ba lời dặn của chủ dự án (20:35, 21:39, 21:48). (1) Đề bài luôn có dòng nói bên kia được và nên dùng mọi công cụ mạnh nhất của mình (agent con chạy song song, nghiên cứu chuyên sâu, tìm web nhiều vòng), làm kỹ chứ không cần nhanh. (2) Có một khối trạng thái viết đủ; các mục cụ thể do nhóm liệt kê từ lời "thông tin, ngữ cảnh, trạng thái, ...": đang chạy bản nào, thứ gì đang mở / tắt, model nào, số đo mới nhất, ai dùng và "tốt" đo bằng gì, đã thử gì kể cả thứ đo rồi bỏ, quyết định đã chốt, việc đang dở, từ riêng kèm nghĩa. (3) Có danh sách nên đọc (tài liệu, thư mục code, bộ test, file đo); ngoài danh sách, bên kia tự do khám phá cả kho code. Các điểm nhóm đã tìm ra cũng ghi vào đề bài, dưới nhãn "đã biết — đừng báo lại". Lời chủ dự án: "bạn nắm gì thì các model AI khác cũng vậy"; "thứ chúng ta nhận lại từ các model AI khác là kết quả chất lượng, chứ không phải kết quả nhanh". Không bao giờ đưa: file khoá và bộ câu chấm cất riêng; thư mục dữ liệu riêng chỉ theo đúng đường dẫn đề bài liệt kê. Cái giá nhóm đã ghi: đưa danh sách của nhóm thì không còn đo được bên kia bỏ sót bao nhiêu điểm nhóm đã thấy; cần con số đó thì soạn một đề bài mù và ghi rõ là mù. Đề bài mới nhất lúc viết được soạn lúc 20:54 ngày 22/11, trước lời dặn thứ hai và thứ ba; chưa có đề bài nào soạn theo mẫu mới.
- Chuyển từ nửa để hiểu tối 22/11 (không đổi nội dung): lớp phiên khác đọc — ngày 22/11, người đọc bắt thêm một lỗi ngay trong một bản sửa của lệnh sửa giá (bài 7) · lớp agent con — ngày 18/11, một bảng 45 dòng "đính chính" do agent con viết có 4 dòng sai hoặc đúng một nửa · lớp soát khác hãng — 33 điểm chia 9, 12, 12, vài điểm trùng; ví dụ: câu "gần X" thiếu dòng "chưa tính kẹt xe" ở 5 trên 14 lượt thật, nên sửa.
- Rào lúc lưu code, đếm từ file rào tối 22/11: bốn phép chặn — file vùng riêng tư (thư mục dữ liệu, thư mục gửi ChatGPT, file bí mật, file bộ câu chấm cất riêng trong kho) · dòng có dạng khoá bí mật · tên dự án khác của chủ dự án · dòng trùng từ 40 ký tự với bộ câu chấm cất riêng (khúc nào có nguyên trong kho hay bộ câu mẫu thì không tính; câu hỏi kín ngắn được dò nguyên câu; phép quét này chạy lỗi thì cũng chặn) — và hai cảnh báo không chặn (giờ ghi kiểu ước lượng, giờ ở tương lai). Rào lúc đẩy code kiểm lại ba phép đầu cho mọi lần lưu sắp đẩy. Lệnh quét cả file cho bài kho nháp vẫn so với kho, bộ câu mẫu và bộ câu chấm cất riêng. Trước 16:45 22/11, rào lúc lưu còn chặn chữ chép từ kho và bộ câu mẫu.
- Sổ cải tiến cách làm, tới 11/11: 25 vòng, 120 sự cố được ghi (gồm cả việc làm đúng đáng giữ).
- Bộ 11 skill: chạy thí nghiệm · review theo rủi ro · soát tích hợp · giao việc agent con · đề xuất phương án cho chủ dự án · cải tiến cách làm · cải tiến sản phẩm theo vòng · giảng và hỏi lại · rà thiết kế agent · rà bảo mật agent · viết code thực dụng.
- Soát ba hãng ngày 18/11: Claude (agent con) 11 điểm, 8 chỉ bên đó thấy; Gemini 6 điểm, 3 chỉ bên đó thấy; GPT 7 điểm và 1 nghi vấn, 6 chỉ bên đó thấy. Ba lượt đọc ba bản code hơi khác nhau, nên cột "chỉ bên đó thấy" không phải bảng xếp hạng.
- Soát ngày 20/11 (GPT-6.2 Sol hai lượt, Gemini hai model): GPT 18 phát hiện, 0 sai; Gemini 16 phát hiện, 0 sai hẳn, 3 nói quá mức.
- Soát ngày 22/11: 33 điểm; ba bên cùng phê bình cách test (cả bộ test bốn lần buổi sáng, 0 lỗi mới). Lượt kiểm chốt sau các bản sửa: cả bộ test 76 file, 2.060 ca đạt; 41 lượt hỏi qua trình duyệt, 0 màn hình lỗi (bài 38, bài 34).
- Chủ dự án trả lời "bao nhiêu cũng được" cho câu hỏi số phiên (18:04, 21/11).
- Tiền gọi model cho đo và thử từ 24/10 tới hết 12/11: khoảng 5,38 USD; phần agent đọc, viết, kiểm dùng gói thuê bao, không tính vào đó.

**Bài sau (bài 40):** hệ thống làm được tới đâu, còn yếu ở đâu, và hướng phát triển có căn cứ.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Vai các phiên, ai giữ sổ, phiên nói thẳng với nhau, việc xây do điều phối chia, việc nghĩ / đếm tự làm: `AGENTS.md` mục "Cách nhìn việc"; `session_prompt/HIEN_TRANG.md` dòng 8 (từ dùng: phiên điều phối, B, C, E, D); `session_prompt/VIEC_DANG_MO.md` dòng 21 (năm phiên trưa 22/11: điều phối, B, C, phiên đo, D) [tài liệu].
- Thiết kế cách làm 24/10 (ba vấn đề, khoảng 2.000 dòng, chủ dự án duyệt, Opus 5.5): `docs/superpowers/specs/2026-10-24-governance-v2-design.md` mục 1–3 [tài liệu].
- Phase 0–6 do Antigravity / Codex, từ 23/10 Claude; dòng thời gian: `bai_hoc/20_LAM_DO_AN_THE_NAO.md` bảng "Dòng thời gian" và khối Nguồn của nó; chia Phase 10–12 ngày 05/11: `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` dòng 6–12; đóng Phase 8 ngày 01/11: `session_prompt/Project_Status.md` mục 3; 22/11 phần xây xong ở local: `session_prompt/VIEC_DANG_MO.md` dòng 7 [tài liệu].
- Không gọi Antigravity: `AGENTS.md` luật cứng 7 [tài liệu].
- Các file trạng thái, ý chưa thử: `session_prompt/HIEN_TRANG.md` dòng 5–6; `session_prompt/Y_CHUA_THU.md` (bảng, ý 1–48) [đếm 22/11]; 11 skill: `ls skills/` [đã chạy 22/11].
- Bảng quyền: `AGENTS.md` mục "Quyền thường trực" (User duyệt 10:11 18/11/2026) [tài liệu]. Bảng trong bài là người viết rút gọn chữ.
- 20 dấu hồ sơ: `git tag -l 'hoso/*' | wc -l` ra 20 [đã chạy 22/11]. 2.762 lần lưu code: `git log --oneline | wc -l` [đã chạy 14:10 22/11]. 1.770 lần một tháng, 28 % chạm code sản phẩm: `session_prompt/HIEN_TRANG.md` mục 4 gạch 16:14 21/11 và `Y_CHUA_THU.md` ý 1 ("đếm thô theo đường dẫn") [số của phiên khác, chưa ai tính lại].
- Khuôn báo xong, nhãn độ tin: `guides/CACH_LAM_VIEC.md` mục 1, 4; `bai_hoc/VIEC_MOI_XONG.md` dòng 7 [tài liệu]. Báo bằng bảng người dùng làm được / chưa (chủ dự án chọn 15:56 20/11): `HIEN_TRANG.md` mục 4 phần "Cách làm" điều (3) [quyết định của chủ dự án].
- Đợt soát 22/11 (33 điểm, 9 + 12 + 12, luật xử, "à không" 0 / 873, "gần X" 5 / 14, hai bản để tắt, cả bộ test bốn lần 0 lỗi mới, lỗi "đồng đồng" bị người đọc bắt): `bai_hoc/VIEC_MOI_XONG.md` mục 40 [chép; người thứ hai kiểm theo nhãn của mục đó]; lượt kiểm chốt 76 file, 2.060 ca, 41 lượt: cùng mục, dòng 32 [máy kiểm, phiên đo].
- Soát 18/11 (11 / 6 / 7 + 1 nghi vấn; bản sửa câu bão bị Gemini bắt; bảng 45 dòng sai 4; hai agent con đọc một hình ra hai kết luận ngược): `bai_hoc/26_CACH_LAM_VIEC_VOI_CODING_AGENT.md` mục 1, 5 và khối Nguồn (trỏ `data/review_khac_hang/2026-11-18_tich_hop_phase_9/DOI_CHIEU.md` [riêng tư]) [chép].
- Soát 20/11 (18 phát hiện 0 sai; 16 phát hiện, 3 nói quá): `bai_hoc/VIEC_MOI_XONG.md` mục 17, ý 2 [chép].
- Rào bằng máy, sự cố 25–26/10, ít nhất 4 lần chặn đúng, mô tả quá cụ thể lọt ít nhất 4 lần: `bai_hoc/20_LAM_DO_AN_THE_NAO.md` mục "Rào bằng máy" và "Một chuyện thật"; lời báo nguyên văn: `.githooks/pre-commit` dòng 20 [code; đọc lại cây chính tối 22/11 — chữ không đổi, dòng 20]. Phép chặn 40 ký tự nay chỉ áp cho bộ câu chấm cất riêng: chủ dự án chọn "A" 16:44 22/11, lý do "cả hai đã công khai trên GitHub từ 20/11", cái giá "muốn giấu lại kho / bộ câu mẫu thì các đoạn đã trích phải gỡ tay": `session_prompt/HIEN_TRANG.md` mục 4 gạch "16:44 22/11/2026" [quyết định của chủ dự án, chép]; code: commit `5047c2c1` (16:45) và `36f9016f` (16:49 22/11), `.githooks/overlap_scan.py` dòng 9–10, 128–134 (`--staged` chỉ giữ cửa sổ nhãn `sealed` không nằm trong chữ công khai) [code]; "từng chặn cả giáo trình trích ví dụ kho": docstring `overlap_scan.py` dòng 10 [code].
- Bảng sự cố: 09/11 → đếm trước khi xây (chủ dự án duyệt 10/11): `bai_hoc/20_LAM_DO_AN_THE_NAO.md` mục "Một ví dụ thật"; 15/11 bốn bản ảnh → năm dòng đề bài, 17–18/11 báo xong sai, bảng quyền, "cách làm phải đúng với bất kỳ agent nào": `bai_hoc/26_CACH_LAM_VIEC_VOI_CODING_AGENT.md` mục 1, 3, 4 và Nguồn (`session_prompt/CURRENT_HANDOFF.md` khối 15/11, 17/11, 18/11) [chép].
- Lời chủ dự án về test (22:45, 22:48 21/11; 12:04 22/11), "nghĩ rộng" (21/11), "tôi toàn chọn chứ không đọc" (16:05 21/11), ba ngày thử, 12 lần gợi hướng, 9 lần nhắc làm quá tay (7 thuần kiểm soát): `session_prompt/HIEN_TRANG.md` mục 4 [quyết định / lời chủ dự án, chép nguyên văn].
- Luật lần đầu ghi, lần hai thành luật: `AGENTS.md` mục "Cách nhìn việc", gạch "Thêm luật, rào…"; `HIEN_TRANG.md` mục 4 "Cách làm" [tài liệu].
- Luật bộ nhớ (dưới 4 GB, hai tiến trình, sự cố 13 tiến trình 11:44 21/11): `HIEN_TRANG.md` dòng 21 [tài liệu]. Gác gpt-6-luna (21:43 21/11): `HIEN_TRANG.md` mục 4 [lời chủ dự án]. Câu gác khi chủ dự án vắng: `HIEN_TRANG.md` mục 3 và gạch 12:04 22/11 [tài liệu].
- Cỡ sổ 18/11 (175.884 và 101.162 byte): `bai_hoc/BAN_DO_DU_AN.md` khối Nguồn [đã chạy 18/11, chép].
- "Người duyệt bị hỏi nhiều thì bấm theo quán tính": `bai_hoc/26_CACH_LAM_VIEC_VOI_CODING_AGENT.md` mục 3 và Nguồn (ghi chép khoá học, riêng tư) [ghi chép, không mở lại bài gốc].
- Giới hạn: rào không chặn đọc, câu kín giữ bằng luật chữ, chưa thử Codex / Antigravity, chưa so một phiên: `bai_hoc/26_CACH_LAM_VIEC_VOI_CODING_AGENT.md` mục "Khi nào cách làm này hỏng" [chép]; người chấm là model đang chạy: `HIEN_TRANG.md` mục 4 gạch 21:43 21/11.
- Sổ cải tiến 25 vòng, 120 sự cố; tiền 5,38 USD: `bai_hoc/20_LAM_DO_AN_THE_NAO.md` mục "Sổ cải tiến" và "Tiền làm đồ án" [chép; tổng là cộng tay của phiên trước].
- Chấm skill chưa kết luận: `bai_hoc/26_CACH_LAM_VIEC_VOI_CODING_AGENT.md` mục 7 [chép].
- Phiên giảng có từ cuối tháng 10: commit `f34cb7f1` ngày 31/10 ("teach-and-quiz for D"); phiên đo (lúc đầu làm Phase 10) từ 05/11: `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` dòng 9; ngày 21/11 là ngày chủ dự án giao viết giáo trình (`HIEN_TRANG.md` mục 4 gạch 16:46) [tài liệu].
- "Cách làm phải đúng với bất kỳ agent nào": chỉ thấy ở dạng lời kể trong `bai_hoc/26_…` mục 3, không có lời nguyên văn và không có ngày ⇒ bài ghi "nhóm ghi" [đối chiếu độc lập].
- Khoảng 50 ý chưa thử: `Y_CHUA_THU.md` có 50 dòng ý lúc 14:48 22/11. Sổ việc 18/11 đo bằng byte (175.884), không phải ký tự. Rào quét trùng 40 ký tự (từ 16:45 22/11 chỉ với câu kín): `.githooks/pre-commit` dòng 9–10, 48–59, `.githooks/overlap_scan.py` [code]. Bốn phép chặn (+ chặn khi phép quét lỗi) + hai cảnh báo, rào lúc đẩy kiểm lại ba phép đầu, lệnh quét cả file vẫn so với cả ba nguồn, câu hỏi kín ngắn dò nguyên câu: `.githooks/pre-commit` dòng 18–23 (file), 31–36 (khoá), 38–43 (tên dự án khác), 52–58 (trùng câu kín / quét lỗi), 63–72 (hai cảnh báo); `.githooks/pre-push` dòng 5; `overlap_scan.py` dòng 7–8, 70–81, 128–134 [code, người viết đếm tay tối 22/11; "bốn" theo đúng danh sách "Chặn khi: 1.–4." ở đầu `pre-commit`].
- Bài đã qua một lượt đối chiếu độc lập (14:43 22/11/2026): `data/hoc_cung_D/kiem/bai_39_41.md` [riêng tư]; các dòng đã áp và không áp ghi ở báo cáo của người viết.

- Dòng bảng sự cố "22 và 23/11" (thêm 12:18 23/11/2026): lời chủ dự án lần hai 10:22 23/11 ("…dùng thử đi chứ"; lần đầu 17:16 22/11) — `session_prompt/HIEN_TRANG.md` mục 4 gạch "10:22 23/11/2026"; cách dùng nhóm chốt 11:13 23/11 — `session_prompt/VIEC_DANG_MO.md` gạch "Cách đo"; ba lỗi mới: `data/playwright_mcp/SO_SANH_MCP_VOI_SCRIPT.md` mục 2 [riêng tư; chép, đã mở]. Kể đủ ở bài 38 vì bài đó là chỗ giảng "kiểm bằng gì, bắt được lỗi nào"; bài này chỉ giữ dòng sự cố → cách sửa. Dòng Cập nhật trước: "22:04, ngày 22/11/2026 · thêm mẫu đề bài mới cho AI khác hãng · khớp hệ thống tối 22/11 (48 tính năng, kho 267 bài): phép quét trùng chữ lúc lưu code chỉ còn so với bộ câu chấm cất riêng · …; đã qua một lượt đối chiếu độc lập".
- Mẫu đề bài mới cho AI khác hãng (thêm 22:04 22/11/2026): ba lời dặn của chủ dự án và cách nhóm áp (khối trạng thái, danh sách nên đọc, nhãn "đã biết — đừng báo lại", bí mật không đưa, cái giá, đề bài mù): `session_prompt/HIEN_TRANG.md` mục 4, gạch "21:39 22/11/2026 — ĐỀ BÀI CHO AI KHÁC" (gồm lời nói rõ thêm 21:48) và gạch "20:44 22/11/2026" (lời dặn dùng agent con, nghiên cứu chuyên sâu) [chép, đã mở]; chữ mẫu: `guides/khung/GOI_REVIEW_KHAC_HANG.mau.md` mục 1, 2, 5 và ghi chú cho người soạn [đã mở]. "Chưa có đề bài nào theo mẫu mới": liệt kê `data/review_khac_hang/` lúc 22:04 22/11, file đề bài mới nhất ghi 20:54 [riêng tư; người viết tự liệt kê].
- Quét số cũ 20:46 23/11/2026: chỉ dòng Cập nhật ("khớp hệ thống trưa 23/11 (49 tính năng, kho 267 bài)" ⇒ 57 mở, 6 tắt, kho 269); các số test trong bảng sự cố (22/11: bốn lượt sáng, lượt chốt 76 file / 2.060 ca) là chuyện của ngày đó, giữ; "45 dòng" là bảng đính chính 18/11, không phải bảng điểm. Lệnh: `corpus.file_count` / `corpus.chunk_count` của `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (269 / 9533) và đếm dòng `: true` / `: false` dưới `assistant:` của `backend/config/settings.yaml` (57 / 6), chạy 20:40 23/11/2026 trên cây chính `03229b64` [đã chạy].

</details>
