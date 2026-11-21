# Bài 26 — Làm việc với coding agent: tin tới đâu, kiểm bằng gì, phần của anh là gì

*Cập nhật lần cuối: 17:50, ngày 21/11/2026 · sửa các câu không còn đúng sau những điều anh chọn ngày 20–21/11 (đoạn "Cập nhật 21/11" ngay dưới bảng từ). Trước: 13:46, ngày 18/11/2026 · thêm hai dòng "vì sao cột hỏi-trước phải ngắn" ở mục 3. Trước: 11:47, ngày 18/11/2026 · bài mới: gom mọi điều anh chốt và nhóm đã làm trong sáng 18/11 về cách làm việc; đã sửa theo một lượt kiểm độc lập trước khi đưa vào.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Coding agent | coding agent (Claude Code, Codex, Antigravity) | Chương trình AI tự đọc code, sửa code, chạy lệnh theo lời giao. Nhóm làm đồ án này gồm bốn phiên như vậy, và từ 21/11 anh giao thêm một phiên giảng viết giáo trình. |
| Phiên — **mới** | session | Một lần mở một coding agent. "Phiên mới, ngữ cảnh sạch" = mở cuộc trò chuyện mới, chỉ đưa thứ cần xem, không mang theo lịch sử cũ. |
| Agent con | sub-agent | Agent do một phiên tạo ra để làm một phần việc. Nó chỉ biết đúng những gì ghi trong lời giao. |
| Bảng quyền — **mới** | mục "Quyền thường trực" trong `AGENTS.md` | Ba nhóm: việc agent tự làm · việc phải hỏi anh trước · việc không bao giờ làm. |
| Review | review | Đọc lại việc của người khác để tìm lỗi trước khi nhận. |
| Gemini, GPT — **mới** | tên model của Google, OpenAI | Model của hai hãng khác với hãng đã viết code đồ án (Claude của Anthropic). Anh dùng chúng qua hai công cụ Antigravity và Codex. |
| "Xong khi" — **mới** | acceptance criterion | Một dòng ghi TRƯỚC khi làm: chạy lệnh gì, thấy gì thì coi là xong. |
| Đồ giả ↔ lượt thật — **mới** | mock / fake ↔ real run | Test thay model hoặc dịch vụ ngoài bằng bản giả theo kịch bản ↔ chạy qua hệ thống thật, model thật. |
| Soát tích hợp — **mới** | integration review | Đọc lại chỗ HAI tính năng gặp nhau, sau khi nhiều thay đổi đã được gộp. |
| Giám khảo khác hãng — **mới** | cross-vendor review | Nhờ model của một hãng khác (không phải hãng đã viết code) đọc và tìm lỗi. |
| Soát mù — **mới** | blind review | Người soát không được cho biết người khác đã tìm ra gì, để không bị dẫn dắt. |
| Skill | skill (`skills/<tên>/SKILL.md`) | File hướng dẫn một quy trình; agent mở ra khi việc cần. |

---

*Bài 20 kể đồ án được làm thế nào: anh quyết, nhiều agent làm và kiểm chéo nhau, rào bằng máy. Bài này kể bước tiếp theo, làm trong sáng 18/11: sau khi
nhóm đọc bốn khoá học và một bài chia sẻ của một kỹ sư làm coding agent, anh và nhóm chốt lại **cách làm việc** — không riêng cho đồ án này, không riêng cho
một hãng agent nào.*

> **Cập nhật 21/11/2026.** Bài này viết ngày 18/11. Từ 21/11 có năm điều đổi: (1) Trong ba ngày làm việc thử, nhóm tự giữ và tự gọt luật về CÁCH LÀM, anh không duyệt từng luật; anh vẫn giữ mục tiêu, bảy luật cứng và bảng quyền, và hết ba ngày xét lại bằng ba con số (mục 8). (2) Anh nêu KẾT QUẢ muốn có; hướng kỹ thuật anh nêu là một gợi ý để xét, không phải đề bài đóng. (3) Phiên nào cũng được tự đếm trên dữ liệu đã có và tự nêu hướng khác mà không chờ giao; việc xây thì theo việc được giao và bảng quyền. (4) Đích của đồ án: anh tự demo trên máy mình và tự trình bày toàn bộ; giảng viên hỏi dựa trên phần trình bày. (5) Model viết của trợ lý đang đổi TẠM từ gpt-6-luna sang Claude Sonnet 5.5; đổi về chỉ sửa một dòng cấu hình.

## Quay lại người hướng dẫn viên

Một công ty du lịch thuê bốn hướng dẫn viên rất giỏi nhưng mới vào nghề. Người chủ không đi theo từng đoàn được. Hỏi "có nên tin họ không" là hỏi sai: câu trả
lời luôn là "tuỳ việc". Dẫn khách đi ăn bún thì cứ để họ tự lo. Đổi cả tuyến đi vào mùa lũ thì phải hỏi chủ trước. Còn tự ý cầm hộ chiếu của khách thì không
bao giờ. Và sau mỗi chuyến, người chủ không đọc nhật ký từng phút của họ — chủ cần một tờ báo cáo ngắn: khách thấy gì khác, có gì làm bằng chứng, còn gì chưa
ổn, và nếu chủ muốn tự kiểm thì kiểm thế nào trong hai phút.

Cách làm việc với coding agent chốt sáng 18/11 đúng là bốn ý đó.

## 1. Vì sao không hỏi "tin" hay "không tin" agent

**Chuyện gì đã xảy ra.** Anh nói thẳng: anh không đọc code, anh chỉ đọc `bai_hoc/`; việc nào nhóm báo xong thì anh chuyển sang việc tiếp. Tức là mọi thứ dựa
vào lời báo "xong" của agent. Mà lời báo đó đã sai nhiều lần, có hồ sơ:

- Chiều 17/11 cả bốn phiên báo "đã đọc đủ khoá học". Tối cùng ngày kiểm kê lại thì **cả bốn đều còn lỗ** (có phiên chưa mở phần lớn sổ bài tập, có phiên mới đọc
  qua bản tóm tắt).
- Sáng 18/11 một phiên báo "3 test đạt" trong khi thật ra 2 đạt, 1 hỏng — do chép nhầm; phiên khác chạy lại lệnh mới lộ.
- Cũng sáng 18/11, một bảng 45 dòng "đính chính ghi chép" do một agent con viết, khi kiểm lại bằng nguồn gốc thì **4 dòng trong chính bảng đính chính đó sai hoặc chỉ đúng một phần** (3 dòng sai, 1 dòng đúng một nửa).

Theo nhận định của nhóm, không lần nào là cố ý: agent báo theo điều nó *tin là đã làm*, giống người mới vào nghề. Nên câu hỏi đúng là: **việc nào để agent tự làm, việc nào phải có người
khác kiểm, và bằng chứng nào thì đủ.**

**Đã chốt gì.** Mức tin đặt theo **từng hành động**, xét ba điều: sai thì hậu quả gì · có kiểm chứng được không · có lùi lại được không. Ba khoá học nhóm đọc,
dù dạy ba việc khác nhau, đều nói cùng ý này.

## 2. Ba lớp giữ chất lượng

| Lớp | Ai làm | Giữ điều gì |
|---|---|---|
| 1. Nhóm tự kiểm + máy kiểm | các agent, script, hook | người viết không tự chấm; thứ máy kiểm được thì để máy kiểm |
| 2. Báo cáo bốn ý | agent viết, anh đọc | báo cáo là "hợp đồng": thiếu một ý thì coi như chưa xong |
| 3. Phần của anh | anh | vài việc nhỏ mà không agent nào làm thay được |

**Lớp 1** kể ở mục 5 và 6 dưới đây.

**Lớp 2 — báo cáo bốn ý.** Mỗi việc xong, phần viết cho anh có đúng bốn ý, bằng lời thường:
1. **Người dùng thấy gì khác** — trước thế nào, sau thế nào, một ví dụ thật.
2. **Bằng chứng** — đo gì, ra bao nhiêu, so với mốc nào; tách riêng hai dòng "test bằng đồ giả" và "lượt thật" (chỉ có dòng đầu thì chưa xong).
3. **Chưa làm / giới hạn** — kể cả thứ agent tự hoãn.
4. **Cách anh thử trong 2 phút** — mở đâu, gõ gì, thấy gì là đúng.

Mỗi khẳng định gắn một nhãn độ tin: **máy kiểm** (có lệnh in ra kết quả) · **người thứ hai kiểm** · **chưa kiểm**. Anh đọc nhãn là biết câu nào đứng trên
bằng chứng, câu nào mới là lời kể.

**Lớp 3 — phần của anh** (anh đã nhận sáng 18/11): luôn đọc báo cáo; khi rảnh thì bấm thử theo ý 4, việc xong thì tự thử và nêu ý kiến. Hai việc nữa anh làm KHI MUỐN, nhóm không nhắc:
chọn **một dòng "xong" bất kỳ** bảo agent chạy lại trước mặt, và tự nói lại bằng lời mình **lý do của một quyết định** đã chọn. Việc sau quan trọng với
một đồ án tốt nghiệp: người chấm chỉ chấm một lần, và hỏi "vì sao em chọn cách này" là hỏi anh, không hỏi agent.

## 3. Bảng quyền thường trực

**Trước đây:** mỗi lần mở phiên, phiên điều phối hỏi anh "quyền phiên này thế nào". Anh phải trả lời cùng một câu nhiều lần, và quyền hết hạn khi kết phiên.

**Từ 10:11 ngày 18/11:** anh duyệt một bảng dùng lâu dài, cho **mọi coding agent** (Claude, Codex, Antigravity), không hỏi lại mỗi lần mở:

| Cột | Gồm những gì |
|---|---|
| **Tự làm, báo sau** | việc đã có trong sổ việc; sửa lỗi đã tái hiện được; lưu và đẩy code lên nhánh riêng; gộp vào bản chính **khi đã có phiên khác kiểm**; dùng agent con; tiền API cho đo / thử (ghi số thật); viết bài học |
| **Hỏi anh trước** | tính năng mới, đổi hướng sản phẩm; đổi lớn thứ người dùng thấy; viết / sửa nội dung kho; xoá dữ liệu; gửi dữ liệu riêng ra một dịch vụ mới; một việc dự kiến tốn trên 1 USD; mọi việc đưa hệ thống lên mạng |
| **Không bao giờ** | đọc / in file khoá; đưa dữ liệu riêng lên kho code công khai; mở bộ câu chấm cất riêng khi không được giao; để agent tự gọi Antigravity (điều khoản của Google cấm); ép đẩy đè lịch sử; bỏ qua rào kiểm của git |

**Vì sao cột "hỏi anh trước" phải ngắn:** người duyệt bị hỏi quá nhiều thì đến một lúc sẽ bấm "đồng ý" theo quán tính — và bỏ sót đúng câu cần dừng lại. Khi
đó việc hỏi không còn bảo vệ gì nữa. Vì vậy cột này chỉ giữ những việc không lùi được hoặc tốn tiền: ít câu hỏi, thì mỗi lần được hỏi anh mới thật sự đọc.

Anh cũng sửa một chỗ nhóm hiểu lệch: cách làm này **không gắn với mốc 30/11**. Mốc đó chỉ là ngày anh tạm đặt cho việc đổi công cụ; cách làm phải đúng với
bất kỳ agent nào, bất kỳ lúc nào.

## 4. Việc lớn: chốt đề bài bằng năm dòng

Tối 15/11 một tính năng giao diện (hỏi bằng ảnh) phải làm lại **bốn bản trong một tối**, vì agent bắt tay vào code trước khi hiểu rõ anh muốn gì. Với việc lớn,
từ 18/11 làm theo thứ tự này:

1. Anh nói ý bằng lời thường.
2. Agent hỏi lại **tối đa ba câu**, mỗi câu có sẵn đáp án để anh chọn.
3. Agent viết lại đúng **năm dòng**: vấn đề · ai dùng · "xong khi" (người dùng thấy gì, thử thế nào) · không làm gì · điều tệ nhất chấp nhận được.
4. Anh xem đề bài có đúng KẾT QUẢ mình muốn không — không cần duyệt cách làm — rồi nói "làm đi".

Từ 21/11: hướng kỹ thuật anh nêu là một gợi ý; agent phải tự vẽ đủ bài toán, nêu cả hướng anh chưa nhắc, và nói TRƯỚC khi làm nếu thấy hướng được nêu chưa phải tốt nhất.

Việc nhỏ và sửa lỗi thì không cần bước này — chỉ cần dòng "xong khi" ghi trước.

## 5. Người viết không tự chấm — và chuyện thật: ba hãng cùng soát một đề

**Luật cũ, giữ nguyên:** ai viết thì phiên khác kiểm (bài 20). Bộ câu thử cho code đọc chữ người dùng do người không viết code đó soạn.

**Điều bài 20 mới đoán, sáng 18/11 có chuyện thật chứng minh:** "phiên khác" mà cùng một hãng model thì vẫn có thể chung điểm mù.

Trong hai tuần, hơn mười tính năng của trợ lý được thêm lần lượt, cái nào cũng có test và được review riêng. Sáng 18/11 nhóm làm một việc chưa từng làm: **soát
tích hợp** — đọc xem khi hai tính năng cùng chạy trong một lượt hỏi thì có gì sai. Cùng một việc cần soi, không ai được xem kết quả của ai (soát mù), giao cho ba bên — lượt Claude chạy trước theo lời giao của phiên điều phối, hai hãng kia
nhận một file đề bài soạn sau đó:

| Bên soát | Số điểm tìm ra | Trong đó chỉ mình bên đó thấy |
|---|---|---|
| Một agent con Claude (cùng hãng với người viết code) | 11 | 8 |
| Gemini (anh tự gửi qua Antigravity) | 6 | 3 |
| GPT (anh tự gửi qua Codex, hai lượt chạy) | 7 điểm + 1 nghi vấn | 6 |

*Đo gì:* số chỗ "hai tính năng gặp nhau mà test hiện có không bắt". *So với mốc nào:* trước đó mọi nhánh đều đã qua review và test — tức mốc là gần như
"0 điểm đã biết" (chỉ một điểm trùng với một giới hạn đã ghi từ 16/11). *Vì sao con số đáng tin, và tin tới đâu:* các điểm **chỉ một hãng thấy** được một phiên của nhóm chạy lại để tái hiện trước khi nhận — cả 3 điểm riêng
của Gemini tái hiện được; với GPT, 5 / 5 điểm đã chạy lại đều tái hiện, 2 điểm còn lại mới đọc code nên ghi "chưa kiểm"; các điểm trùng với danh sách của
Claude thì không chạy lại. *Một lưu ý khi so ba cột:* ba lượt đọc ba bản code hơi khác nhau — lượt GPT đọc bản đã sửa xong hai lỗi mà hai lượt trước tìm ra —
nên cột "chỉ mình bên đó thấy" cho biết mỗi hãng nhìn một vùng khác, không phải bảng xếp hạng hãng nào giỏi hơn.

Điều đáng nhớ nhất không phải con số, mà là **ba danh sách gần như không trùng nhau** — mỗi hãng nhìn một vùng khác. Và có một điểm rất đáng kể:

> Buổi sáng, nhóm sửa một lỗi thuộc nhóm an toàn: câu hỏi về bão mà trợ lý đã dùng hết lượt tìm thì vẫn phải kèm câu chỉ bản tin chính thức và số 112. Bản sửa
> được một phiên Claude khác review, và phiên đó khẳng định dấu ghi "đây là lượt từ chối" trong sổ số đo vẫn đúng. Chừng một tiếng rưỡi sau, Gemini — chỉ đọc
> code khoảng mười phút — chỉ ra:
> chính bản sửa đó làm hệ thống ghi nhầm lượt ấy là "đã trả lời", và làm mất dòng gợi ý cách hỏi trên giao diện. Nhóm chạy thử: đúng. Người review cùng hãng đã
> chỉ xem một trong hai đường mà câu trả lời có thể đi.

Lỗi này đã sửa trong ngày. Nhưng bài học giữ lại: **người kiểm cùng hãng với người viết là cần mà chưa đủ**, và câu "mọi đường đều đúng" phải kèm lệnh tìm ra
mọi đường.

**Cách dùng từ nay.** Nhóm soạn MỘT file đề bài tự đủ ngữ cảnh (bối cảnh · việc cần soi · ranh giới chỉ đọc · khuôn kết quả có mục "tôi chưa đọc gì"); **anh**
tự mở công cụ hãng khác và gửi file — agent của nhóm không tự gọi công cụ đó. Dùng ở các **mốc chốt** (trước khi code đứng yên, trước việc không lùi lại được,
và cho bộ bài học trước khi anh bảo vệ), và chỉ khi nhóm yêu cầu rõ. Kết quả của giám khảo là dữ liệu: nhóm tái hiện từng điểm rồi mới sửa — trong lần đầu có
một điểm giám khảo nói đúng hệ quả nhưng sai một nửa nguyên nhân.

## 6. Test thật ↔ đồ giả

**Vì sao phải tách.** Một test "đạt" có thể đạt vì nó chỉ kiểm cái bản giả do chính nó dựng. Một khoá học nhóm đọc kể đúng chuyện này: agent viết test vô ích chỉ để
đạt mức 80 % dòng code được test chạm tới, và dùng dữ liệu giả dù đã bị cấm.

**Đã làm gì sáng 18/11.** Một phiên soát **ba file test bị nghi thay hẳn phần lõi** (39 test, trong 49 file test của đồ án) để tìm chỗ "thay hẳn phần lõi bằng
đồ giả". Kết quả: 24 / 39 test không giả gì; vài test giả để *ép lỗi* (dịch vụ trả lỗi, lỗi bất ngờ) — việc đó ổn. Chỉ **một** test thay hẳn phần lõi, và nó
đang giữ bốn hành vi của tính năng sửa lịch bằng lời. Nhóm cho chạy **bốn lượt thật** (một lượt thử rồi ba lượt), qua hệ thống thật và model thật, phủ đủ
bốn hành vi: cả bốn đều đúng. *Tốn bao nhiêu:* 0,00375 USD (chưa tới 100 đồng) cho
cả bốn lượt. *Ý nghĩa:* bốn hành vi đó nay có bằng chứng thật, không chỉ có bằng chứng "bản giả chạy đúng". Mẫu rất nhỏ — mỗi hành vi mới thấy một lần — nên đây là "đã
thấy chạy đúng một lần", chưa phải "luôn đúng". 46 file test còn lại chưa được soát theo cách này, và phần "bấm thẻ chọn" của một trong bốn hành vi chưa có lượt thật.

**Hai thói quen anh chọn cho mọi dự án:** (a) **soát tích hợp sau mỗi đợt gộp** (chuyện ở mục 5); (b) **soát độ thật của test** định kỳ. Anh cũng nhắc lại:
khuyến khích test thật, dữ liệu thật, và được dùng tiền API để test.

Thêm một điều dành cho việc đổi thứ người dùng thấy: agent tự chạy trên hệ thống đang chạy và **đính ảnh trước – sau** vào báo cáo — anh nhìn năm giây là biết.
Điều này nhóm mới ghi vào trang cách làm việc và nó chưa thành nếp (luật về cách làm nay do nhóm tự giữ — xem cập nhật 21/11 ở đầu bài).

## 7. Chấm skill: có skill thì agent làm tốt hơn không?

Đồ án lúc đó có 8 skill (file hướng dẫn quy trình; tới 21/11 là 11). Chưa skill nào từng được chấm. Anh chọn: **chấm rồi mới gọt**.

**Cách chấm.** Mỗi skill một việc thử nhỏ (tới trưa 18/11 mới chạy 4 trong 8 skill; 4 skill còn lại mới có đề); hai agent con ngữ cảnh mới cùng làm, một bên được bảo đọc skill, một bên không; thang điểm viết TRƯỚC khi chạy, lấy
từ lỗi đã gặp thật. Một phiên chấm theo thang (phiên này biết bản nào có skill); ở đợt đầu có thêm một phiên thứ hai chấm mà không được cho biết — phiên đó
tự khai là độ "mù" không trọn vì nhận ra dấu skill trong vài bản. Luật ghi trước: chỉ tin khi chênh từ 3 điểm trở lên trên thang 10.

**Kết quả tới trưa 18/11.** Ba skill đầu, hai bên chênh nhau **0 đến 2 điểm** (10 ↔ 8 · 8 ↔ 8 · 8 ↔ 9 theo người chấm chính; ở skill review bản KHÔNG
skill còn cao hơn) ⇒ không cặp nào tới ngưỡng 3 điểm, **chưa kết luận được gì**. Đợt hai (đề khó hơn, mỗi bên ba lượt, mới một người chấm; ngưỡng ghi trước của đợt này: chênh từ 2
điểm trung bình, hoặc một ý mà bên này cả ba lượt có còn bên kia cả ba lượt không) cũng không cặp nào đủ ngưỡng. *Vì sao chưa ổn:* một lượt mỗi bên thì chênh 1–2 điểm nằm trong mức model tự dao động.

**Một quan sát (chưa phải kết luận).** Cái lỗi mà lượt review thật buổi sáng đã bỏ sót (chuyện ở mục 5) thì cả hai agent con — có skill lẫn không skill — đều
tự tìm ra. Khác nhau ở chỗ: hai agent con này có **ngữ cảnh sạch và chỉ làm một việc**, còn người review buổi sáng đang làm nhiều việc cùng lúc. Có vẻ thứ
quyết định là điều kiện làm việc, hơn là chữ trong skill. **Hai điều làm quan sát này yếu đi, phải nói kèm:** đề đợt đầu dễ, lời giao đã gợi ý khá nhiều; và ở
đợt hai — cũng ngữ cảnh sạch, cũng một việc — chỉ 1 trong 6 lượt tìm ra lỗi thật của đề đó. Buổi thử với Codex và Antigravity (khi anh mở) sẽ chạy lại
các đề này.

## 8. Nhóm tự cải thiện cách làm — cuối mỗi ngày, bằng hai con số

Trước đây việc "rút kinh nghiệm" là kể lại sự cố rồi thêm luật. Chữ luật và sổ việc vì thế cứ dài ra (riêng sổ việc đang mở đã hơn 130 nghìn ký tự). Sáng 18/11 anh chọn cách khác:

- Mỗi phiên ghi **hai con số**: (a) số việc đã báo "xong" mà sau đó bị lật lại; (b) số lần anh phải nhắc lại một điều đã nói.
- **Cuối mỗi ngày** chạy một vòng ba bước: đọc hai con số · lỗi lặp lại lần thứ hai thì làm **phép kiểm bằng máy trước, viết luật sau** · thêm bao nhiêu luật
  thì gỡ bấy nhiêu. Người xét một luật có ích hay không phải khác người đề xuất luật đó.

Đây là điều **mới chốt**: chưa có ngày nào chạy đủ vòng này, nên chưa có con số nào để kể (tính tới 18/11).

Từ 21/11 có con số thứ ba: số lần anh phải tự gợi một hướng mà nhóm lẽ ra phải nêu. Một phiên đếm trên phần sổ đã mở được ít nhất 12 lần trong khoảng bốn tuần; một agent con đã xếp loại lại các dòng đó mà không biết trước kết quả, nhưng chưa ai đếm lại số lần. Nhóm cũng đuổi thêm một con số của sản phẩm (trang bản đồ dự án, mục "Nhóm đang làm gì").

## Khi nào cách làm này hỏng — những chỗ còn hở, nói thẳng

- **Máy đang để chế độ "bỏ hỏi quyền".** Anh chọn giữ. Một phiên đã kiểm lại các chốt chặn bằng file giả: luật cấm đọc file khoá **vẫn chặn**
  các đường đọc trực tiếp, nhưng một đoạn chương trình tự mở file thì vẫn đọc được. Nghĩa là chốt này chống lỡ tay, không chống được một agent bị một trang web
  xấu sai khiến. Rào đáng tin nhất vẫn là rào của git (bài 20): nó chặn việc đưa dữ liệu riêng lên GitHub. Nó **không** chặn việc đọc, và
  cũng không chặn một lệnh gửi file ra mạng theo đường khác.
- **Thứ nằm ngoài git.** Từ 20/11 kho bài viết và bộ câu mẫu ĐÃ nằm trong git (anh cho phép 14:41 20/11). Dữ liệu đo và chỉ mục tìm kiếm chỉ ở máy và KHÔNG
  sao lưu định kỳ (anh chọn 20/11; chỉ mục dựng lại được từ kho). Bản sao ngày 18/11 trên ổ khác của máy vẫn còn nhưng không chép lại ở mỗi mốc.
- **Bộ câu chấm cất riêng chỉ còn được giữ bằng luật chữ.** Ở chế độ trên không có rào máy nào chặn agent mở nó. Anh chọn giữ luật chữ và ghi rõ giới hạn
  này trong báo cáo lượt đo cuối.
- **Chưa thử với Codex và Antigravity.** Trang cách làm việc và bộ file mẫu mang sang dự án khác mới được các phiên Claude đọc. Buổi thử: khi anh mở.
- **Chưa đo một phiên so với bốn phiên.** Nhóm nghiêng về "một phiên + agent con, phiên thứ hai để kiểm", nhưng đó mới là suy luận từ khoá học; anh chưa chọn
  kiểu điều phối cho giai đoạn sau, sát ngày mới thử.
- **Agent con không thay người kiểm.** Sáng 18/11 hai agent con đọc cùng một hình mà ra hai kết luận ngược nhau; phải có người mở nguồn phân xử.
- **Nhiều nếp mới chưa thành nếp:** báo cáo bốn ý, ảnh trước – sau, hai con số, năm dòng đề bài — đều chốt trong một buổi sáng, chưa qua một tuần dùng thật.

## Ba điều chính

1. **Không hỏi "tin agent hay không" — hỏi "việc này sai thì mất gì".** Từ đó có bảng quyền ba cột dùng lâu dài cho mọi agent, và báo cáo bốn ý kèm nhãn độ
   tin để anh biết câu nào đứng trên bằng chứng.
2. **Người viết không tự chấm, và người chấm cùng hãng là chưa đủ.** Ba hãng soát mù cùng một việc ra 11, 6 và 7 điểm (cộng 1 nghi vấn), gần như không trùng nhau; một lỗi do chính
   bản sửa trong ngày sinh ra đã lọt qua review cùng hãng và bị hãng khác bắt.
3. **Bằng chứng phải là lượt thật, và cách làm cũng phải được đo.** Một test thay lõi ⇒ bốn lượt thật, chưa tới 100 đồng. Chấm skill chưa cho kết luận — và
   nói thẳng là chưa. Cách làm của nhóm từ nay được xét bằng hai con số mỗi ngày.

**Bài sau:** chưa viết — sẽ kể buổi thử Codex và Antigravity khi đã làm xong.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Mọi quyết định của anh sáng 18/11 kèm giờ ghi nhận (lịch theo thứ, buổi thử tối thứ Ba 24/11: 09:14; báo cáo bốn ý + nhãn độ tin + phần của anh: 09:41; quyền thường trực 10:11; hai thói quen kiểm thử + giám khảo khác hãng 10:11; giữ chế độ bỏ hỏi quyền + câu kín 10:57; chấm skill 10:57; vòng tự cải thiện cuối mỗi ngày 11:09; năm dòng đề bài + đồ án tốt nghiệp chấm một lần + mốc dùng giám khảo 11:30): `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN SÁNG 18/11" [quyết định của anh]
- "Hỏi nhiều quá thì người duyệt bấm đồng ý theo quán tính": khoá AI FDE, bài `W2D3·65` và `W1D3·21` (ghi chép riêng tư `data/khoa_hoc_2026-11-17/AI_FDE_E.md` dòng 143, `AI_FDE_E_phan_1.md` dòng 144) [ghi chép — không mở lại bài giảng gốc]
- Bảng quyền: `AGENTS.md` mục "Quyền thường trực" [tài liệu]; trang cách làm chung: `guides/CACH_LAM_VIEC.md`; bộ file mẫu: `guides/khung/` [tài liệu]
- Bốn phiên báo "đọc đủ" đều có lỗ (17/11): `session_prompt/CURRENT_HANDOFF.md` khối tối 17/11 mục C [tài liệu]. "3 test đạt" thật ra 2 đạt / 1 hỏng: `data/khoa_hoc_2026-11-17/de_xuat_cach_lam/B.md` mục 1 (riêng tư) [đã chạy — phiên C chạy lại lệnh đó sáng 18/11]. Bảng 45 dòng sai 4 dòng: `data/khoa_hoc_2026-11-17/AI_FDE_E_phan_9.md` mục 2d (riêng tư) [đã chạy — phiên E mở nguồn]
- Tính năng ảnh làm bốn bản một tối (15/11): `session_prompt/CURRENT_HANDOFF.md` khối kết phiên tối 15/11, mục vòng tự soi [tài liệu]
- Ba hãng soát mù: `data/review_khac_hang/2026-11-18_tich_hop_phase_9/DOI_CHIEU.md` (riêng tư) — mục 1 "trùng 2 (+ 1 trùng giới hạn cũ) · chỉ Gemini 3 · chỉ Claude 8", mục 2.1 "GPT thêm 6 điểm chưa ai thấy … 5 / 5 điểm B chạy lại đều tái hiện", mục 2.3 [đã chạy — phiên B tái hiện]; lượt Claude 11 điểm: `data/review_tich_hop_2026-11-18/ket_qua.md` (riêng tư). GPT = hai lượt chạy bằng hai bản model, 7 điểm + 1 nghi vấn [theo sổ việc 11:09]
- Lỗi do bản sửa trong ngày (điểm G4 của Gemini): `DOI_CHIEU.md` mục 2 "G4 — ĐÚNG [đã chạy]"; câu "giữ đúng" là của phiên E trong tin review nhánh sửa sáng 18/11, E đã nhận lỗi (`session_prompt/sessions/STATUS_E.md`) [đã chạy]; "khoảng mười phút" theo `DOI_CHIEU.md` mục 1
- "Một điểm đúng hệ quả, sai một nửa nguyên nhân" (G6): `DOI_CHIEU.md` mục 2 [đã chạy]
- Soát đồ giả trong test, một test thay lõi, bốn lượt thật 0,00375 USD: `data/review_tich_hop_2026-11-18/do_gia_trong_test.md` (riêng tư) + sổ việc 10:11 [số của phiên C, chưa ai tính lại]; đổi ra đồng theo 1 USD ≈ 25.000 đồng ⇒ ≈ 94 đồng
- Chấm skill: đề + thang `data/cham_skill_2026-11-18/VIEC_THU.md`, kết quả `KET_QUA.md` (đợt 1 và đợt 2), bản chấm mù `cham_mu_E.md` (riêng tư) [đã chạy]; quan sát "ngữ cảnh sạch + một việc một lúc": `KET_QUA.md` phần đầu [suy ra, chưa kết luận]. Đợt 2 chưa có người chấm thứ hai
- Kiểm chốt chặn ở chế độ bỏ hỏi quyền (thử bằng file giả): `data/bao_mat_agent_2026-11-18/chot_chan.md` (riêng tư) [đã chạy — phiên B]
- Hai agent con đọc một hình ra hai kết luận ngược nhau: `data/khoa_hoc_2026-11-17/AI_FDE_E_phan_9.md` mục 2d dòng 34 (riêng tư) [đã chạy]
- Ví dụ công ty du lịch thuê bốn hướng dẫn viên là ví dụ tự đặt.
- "Ba khoá học nói cùng ý" (mức tin theo từng hành động): bảng nguồn ở `guides/CACH_LAM_VIEC_NGUON.md` (mục 10 của `guides/CACH_LAM_VIEC.md` trỏ sang) [tài liệu — mã bài do người giữ ghi chép từng khoá đối chiếu, không ai mở lại bài giảng gốc]

- **Kiểm độc lập trước khi đưa vào (11:43, ngày 18/11/2026)** (`data/kiem_bai_hoc_2026-11-18/kiem_bai_26.md`, riêng tư): một agent con ngữ cảnh mới đối chiếu 100 khẳng định — 75 đúng, 4 sai, 19 dễ hiểu nhầm, 2 không kiểm được; đã sửa cả 4 chỗ sai ("mỗi điểm đều được chạy lại" · "soát toàn bộ thư mục test" · "chênh không quá 1 điểm" · câu dẫn sai bài 20) và 19 chỗ dễ hiểu nhầm; hai chỗ không kiểm được: một ghi rõ là nhận định của nhóm, một đã bỏ. Người viết tự mở lại nguồn cho ba chỗ sai có số (bảng điểm chấm skill 10 ↔ 8 · 8 ↔ 8 · 8 ↔ 9; "ba file test", 39 test; 49 file test; 1 / 6 lượt ở đợt hai). Số "hơn 130 nghìn ký tự" của sổ việc: `wc -c session_prompt/CURRENT_HANDOFF.md` [đã chạy 18/11].
- Sổ việc 11:09 ghi "chênh ≤ 1 điểm" cho chấm skill là chép nhầm (đó là độ lệch giữa hai người chấm); số đúng ở bảng tổng của `data/cham_skill_2026-11-18/KET_QUA.md`.

- Bản sao dữ liệu ngoài git trên ổ D (11:45 18/11): số file kho 496 ở bản gốc và 496 ở bản sao — phiên C và người viết bài cùng đếm lại bằng `find … -type f | wc -l` [đã chạy]; "một file khớp mã kiểm" là số của phiên điều phối, chưa ai so lại; "chỉ mục chép lúc dịch vụ đang chạy" theo sổ việc 11:45 [tài liệu].

- Sửa 21/11/2026: phần của anh (hai việc làm khi muốn), bước 4 của năm dòng đề bài, con số thứ ba, đoạn sao lưu, số skill, buổi thử không gắn ngày, đoạn "Cập nhật 21/11" — theo các điều anh chọn 20–21/11 ghi ở `session_prompt/HIEN_TRANG.md` mục 4 và `AGENTS.md` mục "Cách nhìn việc" [tài liệu]; số skill: `ls skills | wc -l` = 11 [đã chạy].

</details>
