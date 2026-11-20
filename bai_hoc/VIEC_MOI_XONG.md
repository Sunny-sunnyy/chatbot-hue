# Việc mới xong — báo cáo bốn ý (việc mới nhất ở trên)

*Cập nhật lần cuối: 16:11 20/11/2026 · thêm mục 20 (trang "Bản đồ" riêng trong menu: 40 điểm tham quan, lọc theo loại; đã thử trên trình duyệt ở màn rộng và bề rộng điện thoại; ĐÃ gộp vào bản chính `b2f27d78`, giao diện bản chính đã dựng lại 16:17 20/11/2026) · trước đó 16:08 20/11/2026 · thêm mục 19 (sửa lịch bằng lời: khi KHÔNG dời được một điểm, trợ lý nói vì sao và gợi ý chỗ dời được; đã có một lượt thật trên giao diện và một phiên khác kiểm lại) · trước đó 13:45 20/11/2026 · thêm mục 18 (bản sửa "báo đã dời khi lịch không đổi" — việc mục 17 ý 5 ghi "được duyệt nhưng không làm được" nay đã làm; cả bộ test trên bản đã có sửa này (chạy 13:44–14:04 20/11/2026): 55 / 55 file, 1.555 ca đạt, 0 hỏng) · trước đó 11:40 20/11/2026 · mục 17 thêm ý 5 (lượt soát lần hai riêng cho các bản sửa: ba bản sửa nhỏ đã gộp, một bản không làm được, phần còn lại ghi giới hạn; cả bộ test trên bản cuối CHƯA chạy lúc viết) · trước đó 10:02, ngày 20/11/2026 · mục 17 thêm đợt hai (hai model Gemini: 16 phát hiện, 6 điểm mới; hai sửa của đợt hai đã gộp vào bản chính 10:10 20/11/2026) · trước đó 09:39, ngày 20/11/2026 · thêm mục 17 (một AI khác hãng soát code: 13 điểm, sửa bốn, ghi giới hạn tám, kèm một lỗi nhóm tự tìm; ba thay đổi của mục này đã gộp vào bản chính 09:41 20/11/2026) · trước đó 08:49, ngày 20/11/2026 thêm mục 16 (sửa nhỏ cho mục 15: câu "kể hết các chỗ vừa nêu"; đã gộp vào bản chính 08:58 20/11/2026) · trước đó 21:29 ngày 19/11 thêm mục 15 (hỏi tiếp về nơi vừa được nhắc tới; đã qua một lượt đối chiếu độc lập trước khi đưa vào) · trước đó 19:20 thêm mục 14 (thử đưa nhiều chữ nguồn hơn cho model; số trong báo cáo kỹ thuật đã qua một lượt đối chiếu độc lập) · trước đó 15:53 thêm mục 13 (hỏi tiếp về lịch vừa lập; đã qua một lượt đối chiếu độc lập trước khi đưa vào) · trước đó 14:49 thêm mục 12 (thử mức suy luận của model viết; đã qua một lượt đối chiếu độc lập trước khi đưa vào) · trước đó thêm dòng **Đã thử** ở mục 7, 8, 9 (thử trên giao diện thật trưa 19/11 — cả ba cách thử không ra đúng như bài viết lúc đầu, đã sửa cách thử và ghi thêm giới hạn) · trước đó: thêm mục 7–11 (các việc xong sáng 19/11; đã sửa theo một lượt đối chiếu độc lập trước khi đưa vào) và ghi chú "(19/11: …)" vào những dòng của mục 6 nay đã đổi · trước đó 09:12, ngày 19/11/2026: thêm mục 6 (lượt đo cuối tối 18/11; đã sửa theo một lượt đối chiếu độc lập trước khi đưa vào) · bản đầu: các việc xong ngày 18/11; đã sửa theo một lượt kiểm độc lập trước khi đưa vào. Tối 18/11 một phiên đã tự chạy cả năm mục "cách thử" trên hệ thống thật — kết quả ghi ở dòng **Đã thử** cuối mỗi mục.*

- **File này là gì:** mỗi việc vừa xong mà người dùng trợ lý — hoặc chính anh — thấy khác, nhóm ghi ở đây đúng bốn ý: thấy gì khác · bằng chứng · chưa làm / giới hạn · cách anh thử trong 2 phút. Mục giữ khoảng 2 tuần rồi gỡ (phần đáng giữ lâu đã nằm trong các bài học).
- **Cách đọc:** đọc ý 1 và ý 3 của từng mục là đủ biết hôm đó có gì; ý 2 để biết tin tới đâu; ý 4 làm khi anh rảnh, sau khi bật hệ thống theo sổ tay bàn giao (`guides/RUNBOOK_BAN_GIAO.md`) mục 1–2 rồi mở `http://127.0.0.1:8010/`.
- **Ba nhãn độ tin:** **[máy kiểm]** = có lệnh chạy ra kết quả đó · **[người thứ hai kiểm]** = một phiên khác người viết đã chạy lại hoặc đọc lại · **[chưa kiểm]** = mới là lời của người làm.
- **"Test bằng đồ giả" ↔ "lượt thật":** test bằng đồ giả thay model / dịch vụ ngoài bằng bản dựng sẵn — nhanh, 0 đồng, nhưng chỉ chứng minh phần code quanh model. Lượt thật là hỏi qua hệ thống đang chạy với model thật. Mục nào chỉ có dòng đầu thì ghi rõ là chưa đo trên đường thật.
- **Anh chọn một dòng bất kỳ** trong file này, nhóm chạy lại lệnh của dòng đó trước mặt anh.

---

**Từ dùng chung cho các mục 19/11:** **cờ** = một dòng bật / tắt trong file cấu hình, tắt là hệ thống chạy như trước khi có tính năng · **lời dặn** = đoạn chữ cố định gửi kèm mọi
câu hỏi để bảo model cách trả lời (tên gốc: system prompt) · **token** = đơn vị đếm chữ của model (một mẩu của từ; model tính tiền và đặt giới hạn theo đơn vị này) · **bộ câu mẫu**, **bộ an toàn**,
**sàn**, **người chấm**: như ở mục 6 bên dưới.

## 20/11 — 20. Trang "Bản đồ" riêng trong menu: mọi điểm tham quan của trang Lên kế hoạch trên một bản đồ

**Từ dùng ở mục này:** **bảng điểm** = danh sách 41 điểm tham quan mà trang Lên kế hoạch dùng để xếp lịch (riêng tư, không nằm trong kho bài viết) · **toạ độ** = vị trí (vĩ độ, kinh độ) của một
điểm · **ghim** = dấu tròn trên bản đồ · **thanh dưới** = hàng nút ở mép dưới màn hình điện thoại (Trang chủ, Khám phá…) · **bề rộng 390** = bề rộng màn hình điện thoại phổ biến, nhóm dùng để thử thay cho điện thoại thật.

**Vì sao có việc này.** Ngày 06/11 anh chốt giao diện kiểu cổng du lịch có menu "Trang chủ · Trợ lý AI · Khám phá · **Bản đồ**". Tới 20/11 bản đồ mới chỉ có bên trong thẻ lịch (ghim các điểm của
từng ngày); chưa có trang Bản đồ riêng. Lời chốt 06/11 chỉ có một chữ "Bản đồ" — không nói trang hiện nơi nào, bấm vào làm được gì. Phiên điều phối chọn bản nhỏ nhất dưới đây (không hỏi lại anh).

**1. Anh thấy gì khác.**
- Menu có thêm mục **"Bản đồ"**, đứng sau "Khám phá". Bấm vào ⇒ trang "Bản đồ điểm tham quan": một bản đồ Huế với **40 ghim**, mỗi ghim là một điểm của bảng điểm.
- Hàng nút lọc phía trên bản đồ, số trong ngoặc là số điểm: Tất cả (40) · Di tích (19) · Ẩm thực (7) · Thiên nhiên (10) · Lễ hội, nghệ thuật (5) · Chụp ảnh (9). Một điểm có thể thuộc hai loại nên cộng
  lại lớn hơn 40. Bấm một loại ⇒ bản đồ chỉ còn ghim của loại đó và tự thu / phóng cho vừa.
- Bấm một ghim ⇒ ô nhỏ ghi tên điểm, loại, và link "Mở Google Maps" (mở tab mới, tìm theo tên điểm — cùng kiểu link thẻ lịch đang dùng).
- Dưới bản đồ là danh sách tên các điểm đang hiện (mỗi tên cũng là link Google Maps) — dùng được cả khi ô bản đồ không tải được.
- Ở điện thoại: thanh dưới nay là Trang chủ · Khám phá · (nút tròn Trợ lý Huế) · Bản đồ · Lên kế hoạch. Mục "Giới thiệu" rời thanh dưới, chuyển thành một link ở chân trang (trang chủ vốn có sẵn một
  link sang Giới thiệu). Lý do: để sáu mục thì nút tròn lệch khỏi giữa và chữ bốn mục xuống hai dòng (đã chụp ảnh trước khi đổi). Menu ở màn rộng giữ đủ sáu mục.
- **Không đổi:** bản đồ trong thẻ lịch (nút "Ngày 1 / Ngày 2", ghim đánh số). Trang không dùng model, không thêm nguồn dữ liệu nào: lấy đúng bảng điểm và bảng toạ độ hệ thống đã nạp cho bản đồ lịch.
  Khi tính năng bản đồ lịch tắt thì mục menu "Bản đồ" cũng không hiện.

**2. Bằng chứng.**
- **Trên trình duyệt thật** (hệ thống chạy từ đúng nhánh này, màn rộng 1440 và bề rộng 390; người viết đã mở từng ảnh ra nhìn) [máy kiểm]: vào trang từ menu; số ghim = số điểm chương trình trả về = số dòng danh sách = **40**;
  lọc "Ẩm thực" ⇒ **7** ghim, 7 dòng; bấm ghim ⇒ ô "Chợ Đông Ba · Ẩm thực · Mở Google Maps"; trang không tràn ngang ở cả hai bề rộng; 0 lỗi trang; trang chủ không tải thêm file bản đồ nào (trang khác không chậm đi);
  một lịch thật lập trên nhánh này vẫn có bản đồ với ghim 1–2–3 như trước.
- **Một phiên khác người viết** gọi phần chương trình dựng dữ liệu trên dữ liệu thật [người thứ hai kiểm]: 40 mục, mỗi mục chỉ có bốn thứ (tên, loại, toạ độ, link) — không lọt ghi chú nào của bảng riêng tư ra ngoài;
  0 toạ độ nằm ngoài vùng Huế; 0 tên trùng.
- Test [máy kiểm]: test mới cho dữ liệu trang Bản đồ hỏng trên bản cũ, đạt trên bản mới; file test bản đồ 14 ca đạt.
- Thanh dưới sau khi bỏ "Giới thiệu" [máy kiểm, người viết nhìn ảnh; phiên điều phối đã đọc phần thay đổi này trước khi gộp]: thử trên bản dựng của nhánh ở bề rộng 390 — năm ô, nút tròn đúng giữa, không tràn ngang.
- Lỗi người viết tự thấy khi nhìn ảnh và đã sửa: danh sách tên ở màn rộng lúc đầu xếp một cột dài ⇒ nay chia cột.

**3. Chưa làm / giới hạn.**
- Chỉ có **điểm tham quan**. Quán ăn, chỗ ở KHÔNG có trên trang này (bảng quán có toạ độ nhưng chưa đưa lên — anh muốn thì nói). Không có vị trí của người dùng, không đường đi, không ô tìm kiếm, không nút "thêm vào lịch".
- 40 chứ không phải 41: "Không gian lưu niệm Lê Bá Đảng" có trong bảng điểm nhưng chưa có toạ độ ⇒ không lên bản đồ, không có trong danh sách (lịch vẫn có thể xếp điểm này).
- Các điểm ở trung tâm nằm sát nhau: nhìn xa thì ghim chồng lên nhau, phải phóng to (nút +) mới tách. Điện thoại: một ngón vuốt qua bản đồ là cuộn trang (cố ý, như bản đồ lịch); phóng to bằng nút + hoặc hai ngón.
- Bản đồ cần mạng tới máy chủ ô bản đồ; mất mạng ⇒ khung xám, chỉ còn danh sách. Dưới bản đồ có dòng chữ nhỏ ghi nguồn bản đồ, như bản đồ trong thẻ lịch đang có.
- Mới thử bằng trình duyệt không màn hình ở hai bề rộng; CHƯA thử trên điện thoại thật, chưa thử Firefox / Safari. Trang đã gộp vào bản chính (`b2f27d78`) và giao diện bản chính đã dựng lại 16:17 20/11/2026; sau khi dựng lại mới nhìn lại thanh dưới ở bề rộng 390 bằng bản dựng tĩnh (năm ô, nút tròn giữa), chưa chạy lại cả trang Bản đồ trên bản chính.

**4. Cách anh thử trong 2 phút.** Bật hệ thống rồi mở `http://127.0.0.1:8010/`, bấm "Bản đồ" trên menu ⇒ thấy tiêu đề "Bản đồ điểm tham quan" và dòng "40 điểm tham quan…". Bấm "Ẩm thực (7)" ⇒ còn 7 dấu tròn và 7 tên
dưới bản đồ. Bấm một dấu tròn ⇒ ô tên hiện ra, bấm "Mở Google Maps" ⇒ tab mới mở đúng nơi đó. Thu hẹp cửa sổ trình duyệt cho thật hẹp (hoặc mở bằng điện thoại cùng mạng) ⇒ thanh dưới có năm ô, nút tròn "Trợ lý Huế" ở giữa. [chưa ai thử trên điện thoại thật]

## 20/11 — 19. Sửa lịch bằng lời: khi KHÔNG dời được một điểm, trợ lý nói vì sao và gợi ý chỗ dời được

**Từ dùng ở mục này:** **dời một điểm** = anh nhắn trợ lý kiểu "dời Đại Nội sang chiều ngày 2" trên một lịch đã lập ở trang Lên kế hoạch · **luật xếp** = các điều kiện chương trình
tự kiểm để lịch đi được thật (một buổi không quá hai điểm và không quá số phút cho phép; hai khu đi trong cùng một ngày phải nằm liền nhau; điểm phải mở cửa vào giờ đó) ·
**khu** = nhóm điểm nằm gần nhau (ví dụ khu Kinh thành, khu lăng ở Thủy Xuân) · **đổi chỗ** = luật có sẵn: dời A vào một buổi đang có đúng một điểm B thì A và B đổi chỗ cho nhau ·
**mốc** = phép đếm chiều 20/11 TRƯỚC khi sửa, trên bốn kiểu lịch (3 ngày · cân bằng · di tích; 2 ngày · cân bằng · di tích; 3 ngày · nhẹ nhàng; 4 ngày · khám phá · di tích + ẩm thực):
cho từng điểm thử dời sang từng buổi khác, tổng 176 lần thử.

**Vì sao có việc này.** Phép đếm mốc cho thấy dời một điểm — việc sửa lịch hay làm nhất — chỉ làm được **24 / 176** lần (khoảng 14 %); 152 lần còn lại trợ lý từ chối bằng CÙNG một câu
"… đặt ở chỗ đó sẽ làm lịch phạm luật xếp (giờ mở cửa / cụm xa / quá dày) nên mình chưa đổi": không nói luật nào chặn, không gợi ý thử chỗ nào. Anh chọn làm mục này trong đợt hoàn thiện (15:25 20/11/2026).

**1. Anh thấy gì khác.**
- **Trước:** mọi lần không dời được đều ra một câu chung như trên; muốn biết điểm đó dời đi đâu được thì phải thử từng buổi.
- **Nay:** câu từ chối nêu MỘT lý do bằng lời thường và liệt kê các chỗ dời được. Ba dạng câu (giao diện tự thêm chữ "Không đổi được:" ở đầu):
  - "Phố cổ và chợ Bao Vinh chưa dời sang buổi chiều ngày 2 được vì **một ngày sẽ phải đi hai khu không liền nhau**. Dời được sang: buổi sáng ngày 1 (đổi chỗ với Đại Nội Huế)."
  - "… vì **lịch sẽ có buổi quá kín hoặc quá giờ**. Dời được sang: …"
  - "Chùa Thiên Mụ chưa dời sang buổi sáng ngày 1 được vì lịch sẽ có buổi quá kín hoặc quá giờ. **Trong lịch này Chùa Thiên Mụ chỉ đứng được ở chỗ hiện tại.**"
- Chữ "(đổi chỗ với …)" báo trước điểm nào sẽ bị chuyển sang chỗ cũ của điểm anh dời, để anh không bất ngờ.
- **Không đổi:** lần dời nào trước đây làm được thì nay vẫn làm được y như cũ; lịch không đổi gì ở lượt bị từ chối; chương trình không đọc thêm chữ nào trong câu anh gõ — lý do và gợi ý do chương trình
  tự thử từng chỗ bằng đúng phép thử của lần dời thật, model không viết.

**2. Bằng chứng.**
- **Lượt thật trên giao diện** (chiều 20/11/2026, sau 15:56 — giờ hệ thống khởi động theo log; hệ thống thật, lịch 3 ngày · cân bằng · di tích, mỗi câu một lượt) [máy kiểm, người viết đã mở ảnh ra nhìn]: "Dời Đại Nội sang sáng ngày 3" ⇒ "Đã dời Đại Nội Huế
  sang buổi sáng ngày 3." và lịch đổi thật (Đại Nội đổi chỗ với Phố cổ Bao Vinh); câu "Cho Lăng Tự Đức lên sáng ngày 1, còn Lăng Khải Định để sáng ngày 1" ⇒ hai dòng câu mới, mỗi dòng nêu lý do
  "hai khu không liền nhau" và một chỗ dời được; lịch giữ nguyên.
- **Phép đếm của người viết** (chương trình thật, 0 đồng, cùng 176 lần thử của mốc) [máy kiểm]: dời được vẫn **24 / 176**, và cả 24 lịch sau khi dời giống TỪNG CHỮ lịch của bản trước sửa — tức bản sửa không
  đụng tới ca làm được. **152 / 152** lần từ chối đều có lý do (hai khu không liền nhau: 111 · quá kín hoặc quá giờ: 41 · ngoài giờ mở cửa: 0; mốc: 0 / 152 có lý do). 60 lần từ chối có gợi ý, tổng 92 gợi ý,
  đem từng gợi ý ra dời thật: **92 / 92** dời được đúng chỗ đó. 92 lần còn lại ra câu "chỉ đứng được ở chỗ hiện tại" — và đúng là điểm đó không dời đi đâu được trong phép đếm mốc.
- **Một phiên khác người viết kiểm bằng cách khác** (bảy kiểu lịch người viết KHÔNG dùng: 1 ngày, 5 ngày, có trẻ em, có người lớn tuổi, có ngày đi, có ngày mưa, 2 ngày nhẹ nhàng) [người thứ hai kiểm]:
  1.688 / 1.688 trường hợp cho lịch và các dòng báo giống hệt giữa bản trước và sau sửa ở mọi phần không thuộc bản sửa; 345 lần từ chối đều có lý do; 139 / 139 gợi ý dời được thật.
- Test [máy kiểm]: test mới hỏng trên bản cũ, đạt trên bản mới; bốn file test chạm đường sửa lịch đạt (13 + 44 + 93 + 245 ca, 0 hỏng). Cả bộ test CHƯA chạy lại sau bản này — theo cách làm anh chọn 15:43
  20/11/2026, cả bộ chạy một lượt ở cuối đợt.

**3. Chưa làm / giới hạn.**
- **Tỉ lệ dời được KHÔNG tăng: vẫn 24 / 176.** Bản này chỉ làm câu từ chối có ích. 92 / 152 lần từ chối là "chỉ đứng được ở chỗ hiện tại": với bốn kiểu lịch đã đếm, phần lớn điểm không dời đi đâu được vì lịch
  xếp sẵn đã kín và luật "hai khu liền nhau" chặt. Muốn dời được nhiều hơn phải nới luật xếp hoặc cho chương trình tự dọn chỗ — việc khác, chưa ai giao.
- Chỉ nói MỘT lý do, ở mức cả lịch ("một ngày sẽ…", "lịch sẽ có buổi…"), không chỉ ra ngày nào; ca dính cả hai loại luật (60 / 152) chỉ nói lý do "hai khu".
- Câu có HAI lệnh dời mà lệnh đầu bị từ chối, lệnh sau làm được: gợi ý của lệnh đầu được tính trước khi lệnh sau đổi lịch nên có thể không còn đúng (người kiểm đo: 81 / 408 gợi ý kiểu này đem dời thì bị từ chối;
  thứ tự ngược lại 382 / 382 đúng). Kiểu câu hiếm, chưa có số lượt thật nào gặp ⇒ ghi lại, không sửa (sổ tay bàn giao mục 10.2).
- "Thêm một điểm" và dời một điểm chưa có trong lịch vẫn dùng câu chung cũ. Trong khung trợ lý nhỏ ở góc màn hình, câu từ chối dài phải cuộn mới đọc hết.
- Phép đếm thử đều mọi điểm × mọi buổi; người thật không chọn đều như vậy — chưa có số lượt thật của người dùng. Chưa ai bấm thử lại một gợi ý QUA GIAO DIỆN (mới kiểm bằng chương trình). Chưa thử trên điện thoại thật.

**4. Cách anh thử trong 2 phút.** Ở trang Lên kế hoạch lập lịch **3 ngày · Cân bằng · thích Di tích**, không chọn ngày đi. Mở trợ lý rồi nhắn lần lượt:
(a) "Dời Phố cổ Bao Vinh sang chiều ngày 2" ⇒ phải thấy "Không đổi được: … vì một ngày sẽ phải đi hai khu không liền nhau. Dời được sang: buổi sáng ngày 1 (đổi chỗ với Đại Nội Huế)." và lịch giữ nguyên;
(b) nhắn đúng gợi ý đó: "Dời Phố cổ Bao Vinh sang sáng ngày 1" ⇒ phải thấy "Đã dời…", Bao Vinh lên sáng ngày 1 và Đại Nội xuống sáng ngày 3;
(c) "Dời Chùa Thiên Mụ sang sáng ngày 1" ⇒ phải thấy "… chỉ đứng được ở chỗ hiện tại." Nếu model hiểu câu khác đi (ví dụ tự trả lời bằng lời) thì gõ lại sát mẫu hơn. Bước (a), (c) người viết mới chạy bằng chương trình; bước tương tự đã chạy trên giao diện là hai câu ở ý 2. [bước (a)–(c) chưa ai bấm trên giao diện]

## 20/11 — 18. Sửa lịch bằng lời: điểm "được dời" mà rốt cuộc vẫn đứng chỗ cũ thì trợ lý không còn báo "Đã dời"

**Từ dùng ở mục này:** **lượt sửa** = một câu anh gõ để đổi lịch đã lập ("dời điểm A sang chiều ngày 2") · **hành động** = một ý sửa mà model đọc ra từ câu đó (một câu có thể ra hai, ba hành động);
model chỉ ĐỌC ý, còn việc dời và dòng báo "Đã dời…" do chương trình làm · **đổi chỗ hai điểm** = luật có sẵn: dời A vào một buổi đang có đúng một điểm B thì A và B đổi chỗ cho nhau.

**1. Anh thấy gì khác.** Việc này mục 17 ý 5 ghi "được duyệt nhưng không làm được"; chiều 20/11 anh chọn để phiên điều phối tự viết.
- **Trước:** có hai kiểu câu làm trợ lý báo "Đã dời…" trong khi lịch không đổi gì: (a) model đọc một câu thành hai lần dời về CÙNG một buổi — lần dời đầu đổi chỗ A với B, lần dời sau đổi ngược lại;
  (b) model đọc ra "dời A" tới đúng buổi A đang đứng. Người dùng tưởng lịch đã đổi.
- **Nay:** cuối lượt sửa, chương trình so vị trí từng điểm "đã dời" với vị trí của nó trong lịch đã lưu. Vẫn đứng chỗ cũ ⇒ không báo "Đã dời" nữa mà báo
  "Không đổi được: <tên điểm> vẫn ở chỗ cũ — bạn nói lại từng điểm một nhé." Nếu cả lượt không ý nào làm được thì thẻ lịch hiện đúng bản đã lưu, không lệch cả thứ tự trong buổi.
- **Không đổi:** dời thật (điểm sang buổi / ngày khác) vẫn báo "Đã dời…" như cũ. Chương trình không đọc thêm chữ nào trong câu anh gõ — chỉ so lịch trước với lịch sau.

**2. Bằng chứng.**
- Test mới hỏng trên code cũ (dời về chỗ đang đứng vẫn bị ghi "đã dời"), đạt sau sửa; trong test, ca "hai lần dời đổi chỗ ngược nhau" gặp thật 4 cặp điểm trên bảng điểm thật, cả 4 đều không còn báo "Đã dời". [máy kiểm]
- Một phiên khác người viết tự dò bằng chương trình thật, 0 đồng: lịch 3 ngày mặc định, 8 điểm × 6 chỗ, MỌI cặp hai lần dời = **2.304 cặp**, chạy cả trên bản trước sửa làm mốc.
  "Báo Đã dời mà điểm vẫn ở chỗ cũ": trước **768** dòng (ở 696 / 2.304 cặp) ⇒ sau **0**. "Lịch y nguyên mà vẫn có dòng Đã…": trước **478** ⇒ sau **0**. Lịch phạm luật xếp: 0 ở cả hai bản. [người thứ hai kiểm]
- **Lần kiểm đó bắt được một lỗi của chính bản sửa đầu:** câu vừa dời một điểm vừa bỏ / làm điểm đó rời lịch (ví dụ dời rồi rút lịch còn 1 ngày) làm lượt sửa hỏng hẳn —
  9 lần trên 120 lần thử (bản trước sửa: 0). Đã sửa trong cùng nhánh, thêm test; chạy lại: 120 / 120 không hỏng. Cũng lần kiểm đó thấy 170 / 2.304 cặp cho thẻ lịch đổi thứ tự trong buổi
  dù mọi dòng đều "không đổi" ⇒ đã sửa, còn 0. [người thứ hai kiểm, hai vòng]
- Bảy file test chạm đường sửa lịch: 495 ca đạt, 0 hỏng (bản Python của hệ thống đang chạy). Cả bộ test trên bản đã có sửa này, một lượt, từng file: **55 / 55 file, 1.555 ca đạt, 0 hỏng** — mốc so: lượt trưa 20/11 trên bản trước sửa là 1.554 ca; nhiều hơn đúng 1 ca là test mới của mục này. [máy kiểm]
- CHƯA có lượt thật qua model, chưa bấm trên trình duyệt. [chưa đo trên đường thật]

**3. Chưa làm / giới hạn.**
- Còn 8 / 2.304 cặp (trước 16), đều bắt đầu bằng "dời A về chỗ đang đứng": 4 cặp sau đó dời chính A sang chỗ khác ⇒ hai dòng "Đã dời A…", dòng đầu thừa; 4 cặp sau đó dời điểm B vào đúng
  buổi ấy (B đổi chỗ với A) ⇒ dòng đầu ghi A ở chỗ cũ trong khi A đã sang chỗ của B. Lịch vẫn đúng luật xếp. [người thứ hai kiểm]
- Phép dò mới chạy một kiểu lịch (3 ngày, tham số mặc định); lịch 1, 2, 4, 5 ngày chỉ có các test sẵn có.
- Hai vế cùng đích mà một điểm không hợp buổi ⇒ vẫn từ chối cả câu (giới hạn cũ, sổ tay bàn giao mục 10.3b).

**4. Cách anh thử trong 2 phút.** Ở trang Lên kế hoạch lập lịch 3 ngày · cân bằng · sở thích di tích, không chọn ngày đi. Nhắn trợ lý "Dời Đại Nội sang sáng ngày 1" (đúng chỗ nó đang đứng) ⇒ phải KHÔNG thấy
"Đã dời…"; thấy "Không đổi được: Đại Nội Huế vẫn ở chỗ cũ…" (hoặc model tự nói điểm đã ở đó) và lịch giữ nguyên. Rồi nhắn "Dời Đại Nội sang sáng ngày 3" ⇒ phải thấy "Đã dời Đại Nội Huế sang buổi sáng ngày 3."
và điểm đổi chỗ thật. Lịch lập với lựa chọn khác thì lần dời thứ hai có thể ra "Không đổi được: … phạm luật xếp" — cũng là đúng (trên lịch này chỉ 4 / 40 lần dời một điểm là làm được).
[đo bằng chương trình, không qua model; chưa ai thử trên giao diện]

## 20/11 — 17. Nhờ AI khác hãng soát code trước khi đứng yên: GPT 13 điểm + Gemini 6 điểm mới, nhóm kiểm lại từng điểm — sửa, ghi giới hạn, và một lỗi nhóm tự tìm ra

**Từ dùng ở mục này:** **soát khác hãng** = đưa một đề bài viết sẵn cho một AI KHÔNG phải AI viết code (ở đây: GPT-6.2 Sol) để nó đọc code và tìm chỗ hai tính năng gặp nhau
làm ra kết quả sai; nó không được biết nhóm đã tìm ra gì · **tái hiện** = nhóm tự chạy lại đúng đầu vào AI kia nêu, bằng chương trình thật, để xem điểm đó có thật không (AI kia chỉ
đọc code, có thể đoán sai) · **ca đối chứng** = đổi một chi tiết của đầu vào thì lỗi phải biến mất — để chắc đã hiểu đúng nguyên nhân · **ghi giới hạn** = không sửa, viết rõ vào sổ tay bàn
giao (`guides/RUNBOOK_BAN_GIAO.md` mục 10) để người sau gặp thì biết · **dòng ghi chú** = dòng tên nơi do chương trình viết, ở mục 15.

**1. Anh thấy gì khác.** Ba thay đổi nằm ở nhánh này (hai thay đổi nữa ở một nhánh khác — xem ý 3):
- **Sửa lịch bằng lời, dời hai điểm về CÙNG một buổi của cùng một ngày** (ví dụ tự đặt: "Cho điểm A lên sáng ngày 3, còn điểm B để sáng ngày 3"). Trước: trợ lý báo "đã dời" cả hai nhưng
  lịch y nguyên — lần dời sau tự đổi chỗ ngược lần dời trước. Nay: trợ lý nói thật là chưa làm được câu này. Dời hai điểm về hai buổi khác nhau vẫn chạy như cũ.
- **Hỏi A, hỏi sang B, rồi gõ lại nguyên văn câu A.** Trước: trợ lý trả lời câu B. Nay: trả lời đúng câu A. (Lỗi này do nhóm tìm ra khi test bằng trình duyệt sáng 20/11, không phải do AI kia nêu; sửa chung một nhánh.)
- **Câu xin liệt kê lại có thêm một câu hỏi phía sau** (ví dụ tự đặt: "Liệt kê các chùa đó. Đi được không?"): chương trình không còn coi cả câu là "xin liệt kê lại" nữa, nên
  trợ lý vẫn biết "các chùa đó" là những chùa nào. (Sửa tiếp cho mục 16.)

**2. Bằng chứng.**
- **Đợt soát:** GPT-6.2 Sol chạy HAI lượt riêng (một lượt nhóm gọi, một lượt anh lái), chỉ đọc code. Gộp lại **13 điểm khác nhau** (lượt đầu 10; lượt hai 8, trong đó 5 trùng lượt đầu).
  Nhóm kiểm lại từng điểm bằng chương trình thật, 0 đồng, không sửa code lúc kiểm: **11 điểm tái hiện được** (kèm ca đối chứng), 1 điểm xác nhận bằng đọc code (chính code đã ghi
  đó là con số ước thấp), 1 điểm trùng một giới hạn nhóm đã tự ghi sáng cùng ngày. **Không điểm nào AI kia nêu sai.** [máy kiểm; hai phiên chia nhau kiểm]
- **Đợt hai — hãng thứ hai (Gemini), cùng ngày:** anh chạy thêm hai model Gemini (4 Neon và 4 Hydrogen) với cùng đề bài, trên bản code TRƯỚC khi ba thay đổi ở ý 1 gộp. Hai lượt nêu **16 phát hiện**: 10 trùng 13 điểm của GPT
  (trong đó điểm "dời hai điểm cùng buổi" lúc đó nhóm đã sửa xong), **6 điểm mới**. Nhóm kiểm lại cả 6 bằng chương trình thật hoặc bấm trên trình duyệt: cả 6 có thật; 3 chỗ Gemini nói QUÁ mức so với kết quả kiểm
  (ví dụ: nói file PowerPoint đè chữ từ khoảng 14 dòng link — đo ra chỉ ở lịch 5 ngày kiểu "khám phá", 22 dòng). [máy kiểm; ba phiên chia nhau kiểm]
- **Độ đúng của từng AI soát** (để chọn cho lần sau): GPT hai lượt 18 phát hiện, 0 sai · Gemini hai model 16 phát hiện, 0 sai hẳn, 3 nói quá mức. Điểm an toàn mới nhất của đợt hai chỉ Gemini thấy; lỗi "chữ hiện dần thiếu phần đuôi"
  và lỗi "câu liệt kê có câu hỏi phía sau" chỉ GPT thấy ⇒ hai hãng bổ sung nhau, đúng mục đích soát khác hãng. [máy kiểm]
- **Hai sửa của đợt hai nằm ở nhánh này:**
  - *Cảnh báo tạm ngừng bị bỏ sót ở câu hỏi nhiều ý* (thuộc loại an toàn; cả hai Gemini nêu). Ví dụ tự đặt: hỏi "Thuyền tối nay mấy giờ chạy, và khi có lệnh cấm thì tạm ngừng thế nào?" — bài kho được trích có câu
    "tạm ngừng khi có lệnh cấm", nhưng kho không trả lời được vế hai nên model viết dòng "Tư liệu chưa có thông tin về: quy định tạm ngừng khi có lệnh cấm". Chương trình thấy dòng đó có chữ "tạm ngừng … lệnh cấm" nên
    tưởng câu trả lời ĐÃ nêu cảnh báo và không nối dòng "Lưu ý trong nguồn" nữa. Sửa một dòng: "chưa có thông tin" là câu phủ định, không phải đã nêu. Bằng chứng: test mới hỏng trên code cũ, đạt sau sửa (file 32 ca đạt);
    chạy lại bước nối trên toàn bộ câu trả lời cũ đã lưu: 11 dòng được nối trước và sau sửa giống nhau từng byte ⇒ không ca cũ nào đổi. CHƯA có lượt thật. [máy kiểm]
  - *"dông" và "giông"*: câu có chữ "dông" kèm nhờ đặt phòng từng nhận câu nói thật về việc đặt và không tra web, trong khi cùng câu với chữ "giông" thì giữ câu từ chối + các lớp cảnh báo. Nay hai cách viết chạy như nhau.
    Kiểm lại cho thấy câu "theo dõi bản tin chính thức + 112" trước đó VẪN tới người dùng — đây là lệch cách trình bày, không phải mất cảnh báo. Test đỏ rồi xanh (63 ca đạt); CHƯA có lượt thật. [máy kiểm]
- **Ba thay đổi ở nhánh này:**
  - Test bằng đồ giả: tám file test liên quan, 384 ca đạt, 0 hỏng (bản Python của hệ thống đang chạy). Mỗi thay đổi có test mới đã thấy hỏng trên code cũ rồi đạt sau khi sửa. [máy kiểm]
  - **Gõ lại câu A — lượt thật** (trình duyệt thật, model thật; phiên khác người viết code chạy và đọc tay từng lượt; 0,015 USD ≈ 385 đồng cho 33 lượt): trả lời đúng câu A **3 / 3** sau
    sửa. Mốc so: cùng chuỗi trước khi sửa **0 / 3**; bản cờ tắt chạy cùng buổi 3 / 3. Phép kiểm kèm, ghi trước khi đo: gõ lại một câu trỏ lại kiểu "quán đó ở đâu?" sau khi đã hỏi sang nơi
    khác thì trợ lý phải nói về nơi MỚI — đạt 3 / 3 (nếu bản sửa làm quá tay thì chỗ này sẽ hỏng trước). [người thứ hai kiểm]
  - Hai bộ câu đo của mục 15 và 16 không phải đo lại: chương trình đếm thấy 0 / 46 và 0 / 106 lượt của hai bộ đó chạm vào các thay đổi này. [máy kiểm, hai phiên đếm khớp]
  - Dời hai điểm cùng đích và câu liệt kê có câu hỏi phía sau: CHƯA có lượt thật — mới có test bằng đồ giả và phép tái hiện bằng chương trình thật (không qua model). [chưa đo trên đường thật]

**3. Chưa làm / giới hạn.**
- **Hai sửa thuộc loại an toàn của đợt một (do một phiên khác viết) ĐÃ gộp vào bản chính 20/11:** (a) lúc chữ đang hiện dần, nếu phần đã hiện chỉ là phần đầu của câu trả lời cuối thì nay phần đuôi (có thể là câu cảnh báo)
  được gửi nốt — mới có test bằng đồ giả, CHƯA có lượt thật, và ca này chưa từng thấy ngoài thực tế (0 / 1.488 lượt); (b) sau một câu sửa lịch mà trợ lý KHÔNG làm được, file PowerPoint tải về nay vẫn giữ câu "theo dõi bản tin
  chính thức + 112" — đã thử qua giao diện bởi phiên review. Chi tiết: `report_agent/2026-11-20/c_sua_sau_soat.md`. [người thứ hai kiểm phần (b); phần (a) chưa đo trên đường thật]
- **Bản in từ khung trò chuyện (đợt hai) — đã xử lý bằng cách ẩn nút, gộp 10:10 20/11/2026:** bấm "In / Lưu PDF" từ khung trợ lý nổi ra 5 trang giống nhau, không có ngày nào; từ trang Trợ lý ra đúng 1 trang, mất ngày 2 (cả hai đã thấy thật, người thứ hai đã mở file). Nay nút in chỉ còn ở trang Lên kế hoạch (in ở đó đủ: lịch 2 ngày ra 3 trang); nút "Tải PowerPoint" giữ ở mọi nơi. Hai lần thử sửa cho in được ngay trong khung trò chuyện vẫn thừa trang trắng nên không dùng. Có hiệu lực sau khi dựng lại giao diện.
- **Lịch đã sửa giữ câu an toàn — đã gộp 10:12 20/11/2026:** hỏi bão, lập lịch, rồi một câu sửa lịch LÀM ĐƯỢC ⇒ trước đây file PowerPoint tải về mất câu "theo dõi bản tin chính thức + 112"; nay bản lịch mới thừa hưởng câu đó của bản trước (lịch lập mới từ biểu mẫu thì không). Thử qua giao diện thật, mỗi ca một lần: có nhắc bão ⇒ file có câu 112; không nhắc bão ⇒ file không có — đều đạt [người thứ hai kiểm]. **Thêm 11:40 20/11/2026:** từ nay thẻ lịch trên màn hình, bản in, file chữ và file lịch tải về cũng có câu đó (trước chỉ file PowerPoint có) — thử một lượt trên trình duyệt thật: có hỏi bão ⇒ cả năm nơi có câu 112; không hỏi bão ⇒ cả năm không có [người thứ hai kiểm phần code; lượt trình duyệt do người viết chạy]. Câu này đi theo lịch qua các lần sửa tiếp theo cho tới khi lập lịch mới.
- **Mười một điểm chỉ ghi giới hạn, không sửa** (8 của đợt một, 3 của đợt hai) (đủ chữ ở sổ tay bàn giao mục 10):
  1. Câu trả lời nói về HAI nơi: đã nêu lưu ý tạm ngừng của một nơi thì lưu ý của nơi kia không được chương trình nối thêm. Đếm: 0 / 561 lượt thật đã lưu gặp tình huống này.
  2. Trong cuộc đã có lịch: một số phút đi xe sai mà trùng một thời lượng tham quan trong lịch thì không bị phép kiểm số bắt.
  3. Câu trộn "nhờ đặt bàn + hỏi mưa tháng sau": chỉ ra câu nói thật về việc đặt, mất dòng "chỉ có dự báo 7 ngày tới".
  4. Câu trộn "còn phòng không + một câu hỏi thông tin": câu thứ hai không được trả lời và không được tra web.
  5. Cuộc có hai lịch: bấm "Tải PowerPoint" ở thẻ lịch cũ vẫn ra lịch mới nhất.
  6. File PowerPoint không có mục "Nơi ở" dù thẻ lịch và bản in có.
  7. Tiền ước của một phần trả lời bị huỷ giữa chừng là con số thấp hơn thật (chỉ ở log).
  8. Lúc chữ đang hiện dần: có ca màn hình chỉ hiện khối thời tiết do chương trình nối, thiếu câu trả lời của model (chỗ sửa nằm sâu trong lõi; chưa từng thấy thật).
  9. (đợt hai) Trong cuộc đã có lịch, câu hỏi có cả khoảng cách: model viết giờ của lịch bằng chữ ("lúc 23 giờ") hay tự trừ thời lượng một điểm ("2 giờ 30 phút") thì cả câu trả lời ĐÚNG bị rút, hiện lỗi + nút "Thử lại".
  10. (đợt hai) Câu nhờ đặt phòng mà model tìm kho tới hết số lần cho phép: ra câu từ chối quen thuộc thay vì câu nói thật về việc đặt.
  11. (đợt hai) File PowerPoint của lịch 5 ngày kiểu "khám phá" (22 điểm): các dòng link bản đồ ở trang cuối xếp rất sát. Mở bằng PowerPoint thật thì vẫn đọc được, không dòng nào chồng lên dòng nào — Gemini nói "đè nhau" là quá mức; lịch ngắn hơn thì rộng rãi.
- **Giới hạn của chính ba thay đổi này:** người dùng thật sự muốn hai điểm vào cùng một buổi cũng nhận câu "chưa làm" (nói từng điểm một thì được) · bản sửa "gõ lại câu A" chỉ áp khi câu
  không có từ trỏ lại và lượt ngay trước không có dòng ghi chú; câu hỏi cụt như "địa chỉ ở đâu?" gõ lại nguyên văn có thể mất dòng ghi chú · ba lượt mỗi ô, một cặp câu — không phải tỉ lệ ngoài đời.
- Ba thay đổi ở ý 1 đã gộp vào bản chính lúc 09:41 20/11/2026. Lượt chạy CẢ bộ test trên bản này chưa làm — nhóm chạy một lượt trên bản cuối trước buổi anh test.
- Hai sửa của đợt hai ở ý 2 (cảnh báo tạm ngừng ở câu nhiều ý · "dông" như "giông"): đã gộp vào bản chính 10:10 20/11/2026, sau khi một phiên khác đọc code và các file test dựng cả ứng dụng đạt (147 ca). Chưa có lượt thật qua model cho hai sửa này.

**5. Lượt soát lần hai, riêng cho các bản sửa ở trên (cuối sáng 20/11).** Vì các bản sửa ở mục này và mục 16 được làm nhanh, nhóm nhờ ba AI khác hãng (GPT-6.2 Sol, Gemini 4 Neon, Gemini 4 Hydrogen — anh lái) soát lại ĐÚNG phần vừa sửa.
- **Kết quả:** 10 + 11 + 12 phát hiện, phần lớn trùng nhau. Bằng chứng: nhóm chạy lại nguyên bộ lệnh của một AI trên bản chính — khớp cả mười điểm của nó [máy kiểm]; một phiên tái hiện thêm năm điểm chỉ Gemini nêu bằng chương trình thật, 0 đồng [máy kiểm]. File thứ ba mới được đọc bảng, chưa tái hiện từng điểm [chưa kiểm].
- **Điều đáng biết nhất:** chính bản sửa "gõ lại câu A" ở ý 1 đã gây một lỗi mới — câu hỏi tiếp không nêu tên nơi (ví dụ tự đặt: "Có cần mua vé trước không?") gõ lại lần hai thì trợ lý mất dòng tên nơi, có thể nói về sai nơi. Cả ba AI cùng nêu.
- **Anh chọn "sửa hai dòng rồi đóng", sau đó duyệt thêm đề xuất của nhóm:** (a) bản sửa "gõ lại câu A" nay chỉ áp khi chính câu cũ đó từng có dòng ghi chú — lỗi mới ở trên hết; test mới đã thấy hỏng trên code cũ rồi đạt; (b) khối chữ đầu của model chỉ là khoảng trắng thì trợ lý vẫn hiện đủ câu trả lời (trước: ô trả lời trống mà hệ thống ghi "thành công"); (c) thẻ lịch và các bản xuất giữ câu 112 sau khi sửa lịch (ý "Lịch đã sửa giữ câu an toàn" ở trên). Cả ba đã gộp 11:40 20/11/2026; mỗi cái có một phiên khác người viết đọc và chạy lại test.
- **Được duyệt nhưng KHÔNG làm được:** trợ lý có lúc báo "đã dời" hai điểm mà lịch không đổi (khi chính model hiểu câu thành hai lần dời về cùng một buổi). Lượt viết bản sửa bị hệ thống dừng; nhóm không làm vòng ⇒ ghi giới hạn. **(Chiều 20/11: đã sửa — xem mục 18.)**
- **Ghi giới hạn, không sửa** (đủ chữ ở sổ tay bàn giao mục 10.3b và dòng "gõ lại nguyên văn" ở 10.1): câu liệt kê nối thêm câu hỏi bằng dấu phẩy / xuống dòng · bản sửa "gõ lại câu A" không chạy với câu có từ như "trên", "thứ", "đầu" · ý thiếu viết thành gạch đầu dòng thì dòng lưu ý "tạm ngừng" không được nối (chưa thấy thật) · chữ "dông" theo nghĩa khác thời tiết · phần đuôi câu trả lời ở lượt có khối thời tiết khi model viết hai khối chữ.
- **Giới hạn của chính việc soát:** sau các bản sửa cuối này KHÔNG còn lượt soát khác hãng nào nữa. Lượt chạy cả bộ test trên bản cuối: xem dòng cập nhật ở đầu trang.

**4. Cách anh thử trong 2 phút** (sau khi đã gộp và bật hệ thống): hỏi "Lăng Minh Mạng mở cửa mấy giờ?", rồi "Vé xem ca Huế trên sông bao nhiêu tiền?", rồi gõ lại đúng câu đầu. Trợ lý phải
trả lời về giờ mở cửa của lăng, không lặp lại chuyện vé. Báo cáo kỹ thuật: `report_agent/2026-11-20/b_sua_sau_soat.md`.

## 20/11 — 16. Sửa nhỏ cho mục 15: hỏi tiếp "kể hết các chỗ vừa nêu" không còn bị dòng ghi chú làm ngắn danh sách

**Từ dùng ở mục này:** **dòng ghi chú** = dòng do chương trình viết ở mục 15, ghi tên các nơi mà câu trả lời trước đã trích bài riêng — nó chỉ là MỘT PHẦN các nơi đã nêu
(nơi nêu qua bài tổng hợp không có trong dòng) · **câu xin liệt kê lại** = câu hỏi tiếp chỉ xin kể lại / kể đủ các nơi vừa nêu, không hỏi thêm gì · **khuôn câu** = mẫu
chương trình dùng để nhận ra câu xin liệt kê lại: lời lịch sự, lời xin kể ("kể hết", "liệt kê", "cho mình danh sách"…), "các / những / mấy" đi liền một loại nơi (quán, chùa, điểm
tham quan…), lời trỏ lại ("vừa nêu", "trong bài đó"), lời lịch sự · **bộ dò** = danh sách câu do một phiên KHÁC người viết code soạn để thử khuôn câu, chạy thẳng vào chương trình, 0 đồng ·
**bắt nhầm** = chương trình tưởng một câu là câu xin liệt kê lại trong khi nó hỏi về một nơi cụ thể · **bỏ sót** = câu xin liệt kê lại mà chương trình không nhận ra.

**1. Anh thấy gì khác.** Tối 19/11 nhóm thấy một tác dụng phụ của mục 15: trợ lý vừa kể tám nơi, anh hỏi tiếp "kể hết các chỗ vừa nêu", có lượt trợ lý chỉ kể lại ba nơi — đúng
ba tên nằm trong dòng ghi chú. Model đã coi dòng ghi chú là danh sách đủ. Nay, lượt nào câu anh gõ khớp khuôn câu xin liệt kê lại thì chương trình KHÔNG đưa dòng ghi chú cho
model ở đúng lượt đó; lượt sau model nhận lại như thường. Câu hỏi về một nơi ("cho địa chỉ quán đó") không đổi gì. Không thêm cờ; đây là sửa bên trong cờ `nho_ten_goi_y`.
**Điều KHÔNG đổi, anh cần biết:** danh sách kể lại vẫn thường thiếu một hai nơi — đó là một lỗi khác, có từ trước, không do dòng ghi chú (xem ý 3).

**2. Bằng chứng.**
- **Lượt thật** (model thật qua hệ thống đang chạy; một kịch bản hai lượt "hỏi danh sách rồi xin kể hết", chạy 3 lần bản có sửa và 3 lần bản cờ tắt cùng buổi; 0,014 USD ≈ 350 đồng):
  - Thứ gửi cho model ở lượt 2 của bản có sửa KHÔNG còn dòng ghi chú ở cả 3 / 3 lần, và giống từng byte với bản cờ tắt. Mốc so: tối 19/11, bản chưa sửa có dòng ghi chú ở 3 / 3 lần. [máy kiểm]
  - Số nơi kể được ở lượt 2 (trên 8 nơi có trong kho): bản có sửa 8 · 7 · 7; bản cờ tắt 7 · 7 · 6. Mốc so: bản chưa sửa tối 19/11 là 3 · 8 · 7 — lượt "3" là lượt bị dòng ghi chú
    làm ngắn, nay không còn. Ngưỡng ghi trước khi đo: số lần kể đủ của bản có sửa không kém bản cờ tắt (1 / 3 so với 0 / 3) ⇒ đạt. [máy đếm tên trong câu trả lời; người thứ hai đã đọc tay cả 6 câu trả lời: máy đếm đúng 6 / 6, không nơi nào ngoài danh sách bị thêm]
  - **Đọc con số này thế nào:** vì thứ gửi model ở hai bên giống hệt nhau, chênh lệch 1 / 3 so với 0 / 3 là dao động của model, KHÔNG phải bản có sửa kể giỏi hơn. Ba lần mỗi bên chỉ đủ để nói "không còn thấy lượt tụt xuống ba nơi", không đủ để nói tỉ lệ.
- **Khuôn câu, chạy thẳng vào chương trình (0 đồng)** — hai bộ dò, 74 câu:
  - Bắt nhầm câu hỏi về MỘT nơi: **0 / 32**; bắt nhầm câu hỏi có / không về cả nhóm nơi: **0 / 3**; bắt nhầm câu ngoài phạm vi: 0 / 10. Đây là sàn: bắt nhầm làm trợ lý mất dòng ghi chú
    và quay lại lỗi nói chắc về sai nơi của mục 15. [người thứ hai kiểm — người soạn bộ dò tự chạy lại]
  - Nhận đúng câu xin liệt kê lại: **9 / 20** ở bộ thứ nhất, 5 / 5 ở bộ thứ hai. 11 câu bỏ sót là câu ghép, câu có số, viết tắt, hoặc không nêu loại nơi ("kể hết ra xem nào") —
    các lượt đó chạy y như trước khi sửa, không tệ hơn. [người thứ hai kiểm]
  - **Bản đầu của khuôn câu đã bị bắt lỗi trước khi vào bản chính:** bản đầu chỉ xét "mọi từ trong câu có thuộc danh sách từ cho phép không". Người review soạn thêm 20 câu và 11 / 12
    câu hỏi về một nơi bị bắt nhầm. Nhóm bỏ cách đó, viết lại thành khuôn câu chặt như trên; số nhận đúng tụt từ 14 / 20 xuống 9 / 20, đổi lại bắt nhầm về 0. [người thứ hai kiểm]
- **Test bằng đồ giả:** 18 test của file chạm đạt; các test mới đều đã thấy hỏng khi cố ý phá code (kể cả ca "lượt sau lượt liệt kê vẫn nhận lại dòng ghi chú"). [máy kiểm]
- **Không đo lại bộ 17 chuỗi của mục 15:** chương trình đếm thấy 0 / 46 lượt của bộ đó khớp khuôn câu, nên thứ gửi model ở bộ đó không đổi một byte; đo lại chỉ tốn tiền. [máy kiểm, hai phiên đếm khớp nhau]

**3. Chưa làm / giới hạn.**
- **Lỗi có sẵn "danh sách thiếu mục" còn nguyên:** ở phép đo trên, 5 / 6 lần lượt 2 thiếu một hoặc hai nơi, ở CẢ bản có sửa lẫn bản cờ tắt. Bản sửa này chỉ gỡ tác dụng phụ của dòng ghi chú, không chữa lỗi đó.
- Câu xin liệt kê diễn đạt ngoài khuôn (khoảng một nửa số câu của bộ dò) không được nhận ⇒ lượt đó vẫn có thể bị dòng ghi chú làm ngắn danh sách như tối 19/11.
- Hai trường hợp chương trình không thể biết từ câu gõ: câu MỚI không trỏ lại gì ("liệt kê các quán ăn") cũng khớp khuôn — lượt đó mất dòng ghi chú nhưng không hỏi về nơi vừa nêu;
  câu "liệt kê lại các điểm tham quan đó" khi lượt trước nói về các điểm BÊN TRONG một nơi — chương trình không biết "các điểm đó" thuộc một nơi. Chưa thấy ngoài thực tế, đã ghi ở sổ tay bàn giao mục 10.1.
- Chưa có lượt thật nào trên đúng bản cuối của nhánh: phép đo chạy trên bản trước hai lần siết khuôn; phiên đo đã kiểm bằng máy rằng với kịch bản đó thứ gửi model giống từng byte. [máy kiểm]
- Bản sửa đã gộp vào bản chính lúc 08:58 20/11/2026, sau khi ba file test dựng cả ứng dụng và đi qua đường hỏi đáp (thường và hiện chữ dần) đạt 13 + 15 + 23 ca. Lượt chạy CẢ bộ test trên bản này chưa làm — nhóm chạy một lượt trên bản cuối trước buổi anh test. [máy kiểm — phiên viết code chạy]

**4. Cách anh thử trong 2 phút** (sau khi bản sửa đã gộp và bật hệ thống): hỏi một câu để trợ lý kể nhiều nơi, ví dụ "Huế có những chùa nào nên ghé?"; rồi gõ "Kể hết các chùa vừa nêu giúp mình".
Trợ lý phải kể lại danh sách dài cỡ lượt trước, không rút còn hai ba nơi (thiếu một hai nơi là lỗi có sẵn ở ý 3). Gõ tiếp "Cho địa chỉ chùa đó" sau một câu trả lời nhắc đúng một chùa — trợ lý vẫn phải trả đúng chùa vừa nhắc như mục 15.
Báo cáo kỹ thuật: `report_agent/2026-11-20/b_nho_ten_liet_ke_lai_implementation.md`.

## 19/11 — 15. Hỏi tiếp "cho địa chỉ quán đó": trợ lý nay biết mình vừa nhắc tới nơi nào (đã đo, anh chọn bật)

**Từ dùng ở mục này:** **lượt hỏi tiếp** = câu thứ hai trở đi trong một cuộc trò chuyện, hỏi về một nơi vừa được nhắc mà không gọi lại tên nơi đó (ví dụ "quán đó ở đâu") · **lịch sử** = thứ của các lượt trước được
gửi kèm cho model ở lượt sau · **bài riêng của một nơi** = bài trong kho nói về đúng một quán, một quán cà phê, một điểm đến hay một di tích · **bài tổng hợp** = bài cẩm nang nhắc
nhiều nơi · **mốc** = bản cờ tắt chạy CÙNG buổi, cùng bộ câu, với bản cờ bật · **bộ bẫy** = 12 chuỗi nhiều lượt (25 lượt) soạn 03/11, trong đó 6 lượt hỏi tiếp về một ý kho không có — trợ lý
phải không mượn thông tin của nơi khác để trả lời · **sàn** = loại lỗi không được phép có thêm.

**1. Anh thấy gì khác.** Sau khi trợ lý nhắc tới một quán hay một điểm đến có bài riêng trong kho, anh hỏi tiếp "cho địa chỉ quán đó" thì trợ lý trả đúng nơi vừa nhắc. Trước đây
trợ lý chỉ nhớ CÂU HỎI của các lượt trước, không nhớ mình đã trả lời gì, nên lượt hỏi tiếp nó tự tìm lại kho và có lúc đưa địa chỉ của một quán khác — nói rất chắc mà sai nơi.
Cách sửa: sau mỗi lượt trả lời, CHƯƠNG TRÌNH (không phải model) ghi lại tên các bài riêng mà câu trả lời đã trích; lượt sau model nhận một dòng do chương trình viết: "câu trả lời lượt này có trích bài kho
của các nơi: …; danh sách có thể thiếu nơi đã được nêu và không theo thứ tự trong câu trả lời". Chương trình không ghi lại chữ model viết (cách đó đã thử 03/11 và làm trợ lý mượn thông tin của nơi khác). Cờ `nho_ten_goi_y`; anh chọn bật tối 19/11.

**2. Bằng chứng.**
- **Lượt thật, cờ tắt so với cờ bật cùng buổi** (model thật, mỗi chuỗi một lượt mỗi bên, 0 lỗi kỹ thuật):
  - **17 chuỗi hai lượt "gợi ý nơi rồi hỏi tiếp về nơi đó"** — do một phiên khác người viết code soạn, người viết code không được xem câu: lượt 2 nói đúng nơi vừa nhắc ở **15 / 17**
    chuỗi khi bật, so với **2 / 17** khi tắt. Ngưỡng ghi trước khi đo: ít nhất 13 / 17 và hơn bên tắt ít nhất 4 chuỗi ⇒ đạt. Hai người đọc độc lập, khớp nhau từng chuỗi.
    [người thứ hai kiểm] Hai chuỗi còn trượt khi bật đều là trợ lý trả câu từ chối [người thứ hai kiểm]; theo người soạn bộ, vì kho thiếu MỘT phần của điều được hỏi — một lỗi
    khác, chưa sửa [mới là nhận định của người soạn bộ].
  - **Nói chắc mà sai nơi ở lượt hỏi tiếp:** khi bật **0 lượt**; khi tắt 10 lượt (8 trong 17 chuỗi trên, 2 trong sáu kịch bản phổ thông chạy kèm). [người thứ hai đọc đủ mọi lượt]
  - **Bộ bẫy — một sàn KHÔNG đạt theo chữ:** luật ghi trước là 6 / 6 lượt bẫy phải ra câu từ chối. Bên bật ra 5 / 6 (bên tắt 6 / 6). Ở lượt lệch, trợ lý không dùng câu từ chối
    quen thuộc mà nói: tìm được địa chỉ của nơi đó, nhưng không tìm thấy thông tin cho ý được hỏi — kèm nguồn là bài của chính nơi đó. Nó không mượn thông tin của nơi khác, không
    bịa. [người thứ hai kiểm] **Anh đã chọn bật và hiểu sàn này là "không trả lời bằng thông tin của nơi khác" — đây là cách hiểu chọn SAU khi đã thấy số, nhóm ghi rõ như vậy.**
  - **Hỏi tiếp sang một nơi KHÁC** (6 chuỗi "giống mà không phải"): bên bật trả lời đúng nơi mới 5 / 6, bên tắt 6 / 6; không chuỗi nào kéo tên nơi cũ vào. Một chuỗi bên bật bị từ
    chối dù ngữ cảnh có câu trả lời — mất thật một lượt; mới thấy một lần, chưa biết có lặp lại. [người thứ hai kiểm]
  - **Dòng ghi chú không lọt ra ngoài:** 0 câu trả lời và 0 câu tìm kho có chữ của dòng đó, ở cả 84 lượt bên bật. [máy kiểm; người thứ hai đọc khớp]
- **Test (model và bộ tìm là đồ giả hoặc không dùng — chỉ chứng minh phần code quanh model):** 15 test riêng của phần này đạt, người viết code có thử phá bốn kiểu và đều thấy test đỏ [chưa kiểm — không lưu log]; cả bộ test của máy chủ
  1.542 đạt, 0 hỏng. Khi cờ tắt, 228 yêu cầu gửi model giống từng byte so với bản chính cùng buổi. [máy kiểm]
- Tiền thật của lượt đo: **0,0966 USD** (ước ban đầu khoảng 0,25; trần 0,30), chưa gồm lượt chạy thử để khoá bộ câu của phiên soạn bộ.

**3. Chưa làm / giới hạn.**
- **Nơi chỉ được nhắc qua bài tổng hợp thì KHÔNG được nhớ.** Ở lượt đo 80 kịch bản buổi trưa, 11 trong 34 lượt đứng trước một lượt hỏi tiếp chỉ trích bài tổng hợp. Bộ 17 chuỗi được
  soạn để lượt đầu trích bài riêng, nên con số 15 / 17 KHÔNG nói về các lượt đó — đừng đọc nó như tỉ lệ ngoài đời.
- **Hỏi theo thứ tự ("chỗ đầu tiên", "quán thứ hai") không được bảo đảm.** Lượt đo đúng 8 / 8 chuỗi loại này, nhưng vì cả 8 chuỗi mọi nơi đều có bài riêng. Bản đầu của dòng ghi chú
  có đánh số thứ tự; phiên soạn bộ câu thấy trên dữ liệu thật rằng số đó có lúc lệch với thứ tự anh nhìn thấy, nên đã bỏ đánh số TRƯỚC khi đo.
- Hỏi tiếp cần hai thứ mà kho chỉ có một (ví dụ địa chỉ kèm số điện thoại): vẫn bị từ chối cả câu, dù trợ lý đã tìm đúng tên nơi.
- "Nơi nào gần X nhất trong các nơi vừa nêu": chưa làm.
- Phép đo: mỗi chuỗi một lượt mỗi bên; chạy qua đường chạy chuỗi của bộ đo, chưa qua máy chủ thật nên CHƯA đo cùng mục "Từ web" — hai kịch bản phổ thông đích sẽ được đo lại qua
  máy chủ sau khi cờ bật. Người đọc tay biết bên nào bật cờ. Chỉ 4 con số trong các câu trả lời bên bật được đối chiếu với chữ kho.
- Lỗi của người làm trong việc này, đã sửa: bản báo cáo kỹ thuật đầu tiên chép một câu hỏi của bộ đo vào phần "cách thử" (kho mã là công khai) — người thứ hai bắt được, câu đã
  thay; nhánh được gộp dồn thành một commit để bản cũ không vào lịch sử bản chính.

**4. Cách thử trong 2 phút.** Nhờ trợ lý gợi ý một quán ăn hay một điểm tham quan bất kỳ. Khi câu trả lời nhắc một nơi cụ thể, hỏi tiếp "cho địa chỉ chỗ đó": địa chỉ phải là của
đúng nơi vừa được nhắc. Báo cáo kỹ thuật: `report_agent/2026-11-19/b_nho_ten_goi_y_implementation.md`.

## 19/11 — 14. Thử đưa NHIỀU chữ nguồn hơn cho model viết câu trả lời: không khác về chất lượng, giữ nguyên 10 đoạn

**Từ dùng ở mục này:** **đoạn** = một mảnh nhỏ của một bài trong kho; mỗi lần trả lời, bước tìm chọn 10 đoạn hợp nhất đưa cho model đọc rồi viết · **mốc** = bản đang chạy
(10 đoạn), được chạy LẠI cùng buổi, xen kẽ từng câu với bản thử — không so với điểm của hôm khác · **"15 đoạn"** = đưa 15 đoạn thay vì 10 · **"cả mục"** = mỗi đoạn trong 10 đoạn
được thay bằng nguyên cả mục chứa nó (mục = phần dưới một tiêu đề của bài) · **"cả bài"** = thay bằng nguyên cả bài · **sàn** = loại lỗi không được phép có thêm · **"đủ ý"** = điểm
1–5 do người chấm cho (người chấm không biết câu nào của bản nào), đo câu trả lời có đủ các ý của đáp án không · **khoảng tin cậy 95 %** = vùng mà chênh lệch thật nhiều khả năng
nằm trong; vùng này chứa số 0 thì coi là "không khác".

**1. Anh thấy gì khác.** Không thấy gì khác: trợ lý **vẫn đưa 10 đoạn** cho model. Anh hỏi "có nên cho model thấy nhiều ngữ cảnh hơn không" (một dự án khác của anh làm vậy thì tốt
hơn); nhóm đã đo ba cách và luật ghi trước cho ra "không đổi".

**2. Bằng chứng.**
- **Bước 1 — thử trên 30 câu chọn sẵn, cả ba cách** (câu chọn vì đang yếu nên KHÔNG dùng để kết luận chất lượng): cách "cả bài" bị dừng ngay — đắt gấp 5,5 lần mốc, và ở cả 2 lượt
  có dòng cảnh báo do chương trình nối thì dòng đó thuộc một hoạt động KHÁC với điều được hỏi (bài dài chứa nhiều hoạt động). [máy kiểm phần giá; phần đọc dòng cảnh báo do người chạy đọc — chưa người thứ hai đọc lại]
- **Bước 2 — "15 đoạn" và "cả mục" so với mốc, trên bộ đủ:** 176 câu mẫu chạy một lượt và 32 câu an toàn chạy hai lượt, mỗi bản. [máy kiểm]
  - **Chất lượng không khác.** Điểm "đủ ý" trên 129 câu tính điểm: "15 đoạn" chênh **−0,008** so với mốc, khoảng tin cậy 95 % từ −0,140 đến +0,116; "cả mục" chênh **−0,008**, từ
    −0,047 đến +0,031 — cả hai vùng đều chứa số 0. Trong 129 câu: "15 đoạn" 7 câu điểm cao hơn, 5 câu thấp hơn, 117 câu bằng; "cả mục" 3 cao hơn, 4 thấp hơn, 122 bằng. Để so: hai
    lượt KHÔNG đổi gì chạy sáng 19/11 đã lệch nhau +0,031. [máy kiểm; chưa người thứ hai tính lại]
  - **Người thứ hai đọc tay 37 cặp câu lệch điểm:** khoảng hai phần ba là cùng nội dung, điểm lệch do cách diễn đạt. "15 đoạn" có 4 câu thêm được ý thật (ví dụ thêm được một quán
    nằm ở đoạn hạng 12) và 5 câu mất ý thật; "cả mục" thêm 2, mất 2. Tức là được và mất gần ngang nhau. [người thứ hai kiểm]
  - **Mỗi bản phạm một sàn đếm bằng máy:** "15 đoạn" có 1 câu trả lời đúng nội dung nhưng thiếu ký hiệu nguồn (ở bản chạy thật người dùng sẽ nhận lời báo lỗi thay cho câu trả lời);
    "cả mục" có 1 câu ngoài kho được trả lời thay vì từ chối (không có con số hay ý bịa nào). Mỗi ô đứng trên MỘT lượt, chưa biết lặp lại hay ngẫu nhiên. [máy kiểm; người thứ hai đọc]
  - **Bộ an toàn:** "15 đoạn" sạch về cảnh báo an toàn, còn thêm được một cảnh báo đúng ở một câu về đi thuyền (cả hai lượt). "Cả mục" **mất một cảnh báo ở một lượt**: câu cảnh báo
    "tạm ngừng mùa lũ" (mục 7 của file này: do chương trình nối từ nguồn đã được trích) không hiện, vì khi có nhiều mục hơn để chọn, lượt đó model không trích đúng mục chứa câu
    cảnh báo — trong khi mốc hiện ở cả hai lượt. [người thứ hai kiểm] Hai người chấm an toàn đều bắt được 10 / 10 câu sai cài sẵn, báo nhầm 0 / 5 câu đúng cài sẵn. [máy kiểm]
  - **Đắt hơn, không nhanh hơn:** tiền mỗi câu 0,000501 USD ("15 đoạn", gấp 1,20 lần mốc 0,000419) và 0,000620 USD ("cả mục", gấp 1,48 lần); thời gian cả câu ở giữa 5,4 và 5,6 giây
    so với 5,5 của mốc (đo khi máy còn việc khác chạy). Tiền và giây chỉ để báo — theo lời anh "chất lượng trước", không dùng để chọn.
  - **Kết luận theo luật ghi trước:** không bản nào tốt hơn về "đủ ý", và mỗi bản phạm ít nhất một sàn ⇒ **không đổi**.
- Tiền thật cả việc: **0,586 USD** (bước 1: 0,144; bước 2: 0,442; chấm bằng agent con: 0 đồng API). Anh đã duyệt riêng việc này tới 1,40 USD.

**3. Chưa làm / giới hạn.**
- Kết luận là "trên bộ 176 câu mẫu đã dùng nhiều lượt", mỗi bản một lượt. Nó KHÔNG nói "nhiều ngữ cảnh hơn thì vô ích với mọi loại câu": 4 câu "15 đoạn" thêm được ý thật cho
  thấy có lúc đoạn đúng nằm ở hạng 11–15. Cách đáng thử về sau (chưa làm, chưa có plan): chỉ lấy thêm đoạn cho loại câu xin danh sách, thay vì cho mọi câu.
- Bộ an toàn chạy trong lúc nhánh chính nhận hai nhánh code mới (đều tắt cờ); đã chụp lại 228 yêu cầu gửi model sau đó: giống từng byte bản đầu buổi. [máy kiểm]
- File kết quả bộ an toàn không lưu dòng cảnh báo do chương trình nối, nên các dòng đó được DỰNG LẠI bằng chính hàm đang chạy thật (thử trước trên dữ liệu cũ biết chắc có dòng nối:
  ra đúng). Trước đó người làm đã ghi nhầm "0 dòng" vì đếm trên một trường mà file không lưu — người thứ hai đọc công cụ đã bắt được, số đã sửa. Bài rút ra: trước khi ghi "0", phải
  thấy phép đếm đó ra số khác 0 ở một chỗ biết chắc là có.
- Người đọc tay biết bản nào thuộc cách nào (không mù) và chỉ đọc các cặp lệch điểm.
- Thấy thêm khi đo: hai lượt mốc không đổi gì cũng bị người chấm an toàn gắn lệch nhau 1 câu "lỗi mới" + 4 câu "hết lỗi" ⇒ số ô thô của người chấm không dùng làm sàn được; từ nay
  sàn an toàn tính trên các ô mà người đọc tay xác nhận, in kèm cặp mốc so với mốc.
- Bài học về cách làm (nhóm đã chốt tối 19/11): chấm chỉ số quyết trước; đã "không khác" thì dừng, không chấm tiếp phần an toàn và phần sinh lại cho bản không còn là ứng viên.

**4. Cách thử trong 2 phút.** Không có gì để thử trên giao diện (không đổi gì). Muốn xem bảng số, nhóm mở file kết quả trước mặt anh; báo cáo kỹ thuật:
`report_agent/2026-11-19/b_ngu_canh_lon_implementation.md`.

## 19/11 — 13. Hỏi tiếp về lịch vừa lập: trợ lý nhìn thấy đúng lịch đó và số giờ do chương trình tính (đã bật trên bản chính tối 19/11)

**Từ dùng ở mục này:** **lịch đã lưu** = lịch anh vừa lập bằng biểu mẫu "Lên kế hoạch"; hệ thống giữ nó trong bộ nhớ của cuộc trò chuyện 30 phút kể từ lượt cuối ·
**lượt hỏi thường** = một câu anh gõ để hỏi (không phải bấm biểu mẫu, không phải câu nhờ sửa lịch) · **nguồn** = một đoạn tư liệu hệ thống đưa cho model đọc trước khi viết;
bình thường nguồn là đoạn lấy từ kho, ở việc này có thêm một nguồn do chương trình tự in · **model tự cộng** = con số do model tính nhẩm khi viết, không phải do chương trình
tính — có thể sai · **sổ vết** = bản ghi từng bước của một lượt hỏi (model đã tìm gì, nhận gì), chỉ bật ở máy làm việc · **câu từ chối khuôn** = câu cố định "Tôi không tìm thấy
đủ thông tin…" · **kịch bản** = một cuộc trò chuyện mẫu nhiều lượt dùng để đo.

**1. Anh thấy gì khác.** Sau khi lập lịch, anh hỏi tiếp bằng lời về chính lịch đó — "ngày đầu mình tham quan tổng cộng bao lâu, mấy giờ thì xong điểm cuối", "viết lại lịch này thật ngắn, mỗi ngày một dòng" — thì trợ lý trả lời **trên đúng lịch đang hiện trên màn hình**, với số giờ do chương trình tính sẵn. Trước hôm nay trợ lý không nhìn thấy lịch vừa lập: nó đi tìm
trong kho, gặp một bài lịch mẫu và trả lời trên lịch mẫu đó — nói rất chắc mà sai. Anh đã chọn bật phần này chiều 19/11 (cờ `lich_vao_hoi_thuong`). **Đã bật trên bản chính tối 19/11** (mã commit gộp `62a2762`), sau khi chạy đủ ba phép kiểm còn nợ từ buổi chiều — kết quả ở cuối ý 2. Bản anh mở từ giờ là bản đã bật.

Vì sao trước đây sai (theo đường đi của một câu hỏi): câu hỏi ⇒ chọn tuyến ⇒ tìm trong kho ⇒ gom nguồn ⇒ model viết. Lịch vừa lập nằm ở bộ nhớ của cuộc trò chuyện nhưng chỉ
được đưa cho bước "hiểu câu nhờ sửa lịch", không được đưa vào bước gom nguồn. Việc này thêm đúng một thứ ở bước gom nguồn: chương trình in lịch đang có thành một nguồn — từng
ngày, từng buổi, giờ, tên điểm — kèm các con số đã tính: mỗi ngày mấy điểm, bắt đầu mấy giờ, mục ban ngày cuối xong mấy giờ, từ đầu tới cuối bao lâu, tổng thời lượng tham quan,
ngày nào dài nhất. Model chỉ việc diễn đạt lại.

**2. Bằng chứng.**
- **Ba kịch bản từng sai ở lượt đo trưa 19/11** (trong bộ 80 kịch bản việc phổ thông; trưa nay cả 3 / 3 trả lời trên một lịch khác):
  - hỏi số giờ của ngày 1 — chạy 2 lần: 2 / 2 trả lời trên đúng lịch, số khớp dòng chương trình in ("5 giờ tham quan, từ 8:00 đến 16:00, chưa tính đi lại");
  - nhờ tóm lịch để chép — chạy 2 lần: 2 / 2 liệt kê đúng 8 mục của lịch đang có, đúng giờ;
  - hỏi tổng tiền vé — chạy 2 lần: 2 / 2 tính trên đúng lịch và ra 700.000 đồng, khớp đáp số tính tay; nhưng đây là số **model tự cộng** từ giá vé trong kho (xem ý 3).
  [người thứ hai kiểm — một phiên không viết code đọc từng câu]
- **Bộ câu dò 29 cuộc do người khác người viết code soạn** (người viết code không được xem trước), chạy qua hệ thống thật, mỗi cuộc bắt đầu bằng một lịch từ biểu mẫu; 15 cuộc
  trong đó chạy thêm lần nữa với cờ tắt cùng buổi để có mốc so. Người soạn đọc 100 % câu trả lời:
  - con số về lịch (số điểm, giờ, khoảng thời gian) sai: **0** trên 32 lượt có nguồn lịch (mốc phải đạt: 0);
  - nói một điểm KHÔNG có trong lịch là có: **0** (mốc: 0);
  - nói "đã sửa lịch" trong khi lịch không đổi: **0** (mốc: 0);
  - câu ngoài kho được trả lời nhờ có thêm nguồn lịch: **0** (mốc: 0; bên cờ tắt cũng 0);
  - kéo lịch vào câu không hỏi về lịch: **0 / 12** câu (mốc cho phép: tới 2 / 12).
  [người thứ hai kiểm]
- **Hỏi ngay sau khi sửa lịch** (hai chuỗi: bỏ một điểm rồi hỏi "ngày 1 còn điểm nào"): cả hai trả lời theo lịch ĐÃ sửa. [người thứ hai kiểm]
- **Không làm hỏng các câu khác:** với cờ tắt, và với cờ bật ở cuộc chưa có lịch, toàn bộ chữ hệ thống gửi cho model ở 228 câu của các bộ đo đã dùng
  **giống từng chữ** với bản trước việc này ⇒ các số chất lượng đã đo không đổi. [máy kiểm — đo trên nhánh trước khi gộp vào bản chính; bản đã gộp chưa đo lại]
- **Không câu trả lời nào bị rút lại** vì kiểm trích dẫn: 0 / 57 lượt gõ (đây là rủi ro lớn nhất ghi trước trong kế hoạch). [máy kiểm]
- **Test bằng đồ giả:** 14 test (model thay bằng bản trả lời dựng sẵn; bộ tìm thật), gồm hai test được chứng minh là "biết đỏ": cố ý chỉ đưa lịch tới một nửa đường đi ⇒ test
  báo hỏng. Một phiên khác chạy lại: 14 đạt. [người thứ hai kiểm] Lỗi do chính người viết gây ra ở bản đầu và được người review bắt trước khi đo: một phép kiểm số có sẵn sẽ
  rút oan câu trả lời nêu đúng số giờ của lịch — đã sửa, có test.
- **Tiền:** lượt thật của phần anh chọn bật 0,073 USD — khoảng 0,075 nếu cộng cả các câu trả lời chạy song song rồi bị bỏ (trần ghi trước 0,15); phần thử tổng tiền vé ở ý 3 thêm 0,034 USD.


- **Ba phép kiểm làm tối 19/11 trước khi bật trên bản chính** (cả ba chạy trên đúng bản có cờ bật):
  - cả bộ test của phần máy chủ, mỗi file một lượt riêng: **1.512 đạt, 0 hỏng** (mốc gần nhất: 1.437 đạt trên bản sáng 19/11; số tăng vì các việc gộp trong ngày mang thêm test). Lượt đầu
    có 4 test hỏng: 1 do một test cũ chưa biết tới cờ mới (sửa hai dòng test), 3 do thư mục chạy thử thiếu bản dựng giao diện (không phải lỗi code);
    sửa xong chạy lại các file đó đều đạt. Lỗi trùng tên biến kể ở ý 3 được bắt TRƯỚC lượt này, lúc chạy riêng các file test dùng chung hàm dựng cờ, và đã sửa xong trước khi chạy cả bộ [máy kiểm; một phiên khác đọc phần sửa];
  - chữ hệ thống gửi cho model ở 228 câu của các bộ đo (cuộc chưa có lịch): **giống từng byte** so với bản chính chụp cùng buổi ⇒ bật cờ không đổi gì ở câu hỏi thường khi chưa lập lịch [máy kiểm];
  - một cuộc thật trên bản chính sau khi bật (0,0024 USD): lập lịch mặc định ⇒ hỏi "ngày 1 đi tham quan mất mấy tiếng" ⇒ nhờ tóm lịch theo ngày: cả hai câu trả lời trên đúng lịch vừa lập,
    "5 tiếng tham quan ban ngày, chưa tính đi lại, ăn nghỉ" khớp dòng chương trình in; bản tóm đủ 8 mục, đúng giờ [người viết code tự đọc 3 / 3 lượt — chưa có người thứ hai đọc]. Ở câu số giờ,
    model tự cộng thêm buổi tối thành "10 tiếng" — phép cộng đúng nhưng là số model tự tính, không phải số chương trình in.
**3. Chưa làm / giới hạn.**
- **Tổng tiền vé do chương trình tính: đã làm thử, CHƯA bật.** Anh chọn "chép giá kho đã có"; một phiên chép giá vé từ kho vào bảng điểm của lịch (26 / 41 điểm có giá hoặc
  được kho ghi rõ miễn phí; 25 dòng đã được soát độc lập, 1 dòng thêm sau), chương trình cộng "giá × số người" và in sẵn tổng, tổng theo từng ngày, điểm miễn phí, điểm chưa có giá (không coi là 0 đồng).
  Phép tính đúng: 5 / 5 ca đối chiếu của người review khớp (3 ca có phép cộng). Nhưng khi đo qua hệ thống thật, **6 / 12 lượt hỏi về tổng tiền hoặc giá vé ra câu từ chối khuôn** (lần đầu 4 / 6;
  sau đúng một lần sửa câu chữ 2 / 6) — tệ hơn bản anh chọn bật (chỉ lịch + số giờ), nơi cùng câu hỏi được trả lời 3 / 3. Nguyên nhân đã xác nhận bằng sổ vết: thấy dòng "còn điểm chưa có giá",
  model tự đi tìm giá các điểm đó trong kho, không thấy, rồi kết luận "không đủ thông tin" cho CẢ câu hỏi — dù tổng do chương trình tính nằm ngay trước mắt nó. Lượt nào model
  không tự tìm thêm thì luôn có câu trả lời (11 / 11 lượt; 9 lượt dùng đúng số chương trình in, 2 lượt model tự tính và đúng). Kế hoạch ghi trước "chỉ một lần sửa, không sửa mò lần hai" ⇒ nhóm dừng, giữ bản thử làm hồ sơ; chữa tận gốc chỗ
  "model tự tìm thêm rồi từ chối" là một việc riêng chưa giao.
- **Hệ quả khi bật bản anh chọn:** hỏi tổng tiền vé thì **model tự cộng** giá vé của kho trên đúng lịch. Ba lần đo đều đúng, nhưng đó chưa phải số chương trình tính — có thể cộng
  sai. Câu giả định ("nếu thêm một người lớn thì hết bao nhiêu") cũng là số model tự tính.
- **Một lỗi có sẵn thấy lại, không do việc này:** một câu giả định "nếu bỏ điểm X thì ngày 1 còn mấy tiếng" có lần bị hiểu thành lệnh sửa — điểm X bị bỏ thật khỏi lịch
  (1 lượt). Đã ghi vào sổ tay bàn giao mục 10.2.
- Lịch chỉ được nhớ 30 phút kể từ lượt cuối; quá hạn thì trợ lý lại không thấy lịch.
- Mới đo trên lịch mặc định (2 ngày, 2 người lớn) và một lịch gia đình có trẻ em; câu hỏi do nhóm viết, chưa phải câu người dùng thật gõ; mỗi câu chạy 1–2 lần.
- **Các lượt test tối 19/11 trước khi bật bắt được một lỗi do chính việc này gây ra, đã sửa trước khi bật:** trong file code của lịch có hai biến trùng tên — một cái có từ 13/11 dùng để bắt giờ giấc trong câu tả điểm do model viết (lịch lập qua biểu mẫu: câu nào tự nêu giờ thì bị thay bằng câu an toàn do chương trình viết), một cái thêm chiều 19/11 cho việc này. Cái sau đè cái trước, nên từ 15:47 tới 18:55 ngày 19/11 (khoảng 3 giờ) trên bản chính, câu tả điểm có giờ lẻ kiểu "mở cửa lúc 8:00" có thể lọt vào lịch mà không bị thay. Lỗi lọt vì lúc gộp code buổi chiều máy đang bận, nhóm chỉ chạy các file test liên quan trực tiếp chứ chưa chạy cả bộ; test bắt được lỗi này nằm ở một file khác. Đã sửa bằng cách đổi tên biến (hai dòng), một phiên khác đọc lại và tự chạy test. Chưa ai đếm trong khoảng 3 giờ đó có lịch nào thật sự bị lọt giờ hay không (không có người dùng ngoài nhóm).

**4. Cách anh thử trong 2 phút.**
0. Cờ đã bật trên bản chính từ tối 19/11 — thử được ngay.
1. Bật hệ thống, mở giao diện, vào "Lên kế hoạch", để nguyên mặc định (2 ngày, 2 người lớn), bấm tạo lịch.
2. Gõ: *ngày đầu mình tham quan tổng cộng bao lâu, mấy giờ thì xong điểm cuối* ⇒ **đúng** là câu trả lời nêu 5 giờ tham quan và khung 8:00 – 16:00 của lịch đang hiện; **sai** là nhắc tới
   một điểm không có trên màn hình.
3. Gõ: *viết lại lịch này thật ngắn, mỗi ngày một dòng* ⇒ đúng là đủ các mục của lịch trên màn hình, đúng giờ.
4. Gõ: *hai người đi hết lịch này thì tiền vé vào cửa khoảng bao nhiêu* ⇒ sẽ thấy một tổng kèm câu "còn điểm chưa có giá" — nhớ đây là số model tự cộng (ý 3).

## 19/11 — 12. Thử cho model "nghĩ ít hơn" hoặc "nghĩ nhiều hơn" trước khi viết: giữ nguyên mức đang chạy

**Từ dùng ở mục này:** **mức suy luận** = model được "nghĩ thầm" bao nhiêu trước khi viết câu trả lời; có ba nấc được thử: thấp (`low`), vừa (`medium` — mức đang chạy, là mức
mặc định khi không dặn gì), cao (`high`). Nghĩ thầm cũng tính tiền và tốn giây · **mốc** = bản đang chạy (mức vừa) được chạy LẠI cùng buổi, xen kẽ từng câu với mức thử — không so
với điểm của hôm khác · **khoảng tin cậy 95 %** = vùng mà chênh lệch thật nhiều khả năng nằm trong; vùng này chứa số 0 thì coi là "không khác".

**1. Anh thấy gì khác.** Không thấy gì khác: trợ lý **vẫn chạy mức vừa**. Anh đề nghị thử ba mức sau khi đã bỏ trần độ dài câu trả lời; nhóm đo xong và luật ghi trước cho ra
"không đổi".

**2. Bằng chứng.**
- **Bước 1 — thử giá trên 45 câu chọn sẵn, cả ba mức** (không dùng để kết luận chất lượng vì là câu chọn có chủ đích): tiền mỗi câu (tính trên 37 câu bộ mẫu của mẫu 45 câu) gần bằng nhau (mức thấp bằng 0,94 lần mức vừa,
  mức cao bằng 0,97 lần); mức cao **hầu như không làm model nghĩ nhiều hơn** trên loại câu hỏi này (lượng nghĩ thầm ở giữa: 42 đơn vị so với 21 của mức vừa — rất ít so với vài
  nghìn đơn vị của một câu hỏi). Anh xem số rồi chọn: bước 2 chỉ đo mức thấp so với mức vừa. [máy kiểm]
- **Bước 2 — mức thấp so với mức vừa, trên bộ đủ:** 176 câu mẫu chạy một lượt và 32 câu an toàn chạy hai lượt, mỗi mức. [máy kiểm]
  - **Chất lượng không khác.** Điểm "đủ ý" (thang 1–5, người chấm không biết câu nào của mức nào) trên 129 câu tính điểm: chênh **0,000**, khoảng tin cậy 95 % từ −0,101 đến
    +0,093 — chứa số 0. Trong 129 câu: 5 câu mức thấp được điểm cao hơn, 5 câu được điểm thấp hơn, 119 câu bằng nhau. Điểm "đúng" cũng chênh 0,000. Hai lượt KHÔNG đổi gì chạy sáng 19/11 đã lệch
    nhau +0,031 ⇒ chênh 0,000 nằm hẳn trong dao động tự nhiên.
  - **Một lỗi ở bộ an toàn.** Trong hai lượt của mức thấp, có MỘT lần trợ lý so sánh sai một con số chiều cao với ngưỡng miễn vé trẻ em và bảo phải mua vé, trong khi nguồn ghi
    được miễn. Sáu lần chạy khác của đúng câu đó trong ngày (ba lần mức vừa, hai lần mức thấp, một lần mức cao) đều đúng. Luật ghi trước: "đảo cảnh báo / sai điều kiện mới — 0 lần" (người chấm gắn ca này cả hai loại) ⇒ mức thấp
    **phạm sàn**. Người thứ hai đã đọc và xác nhận đây là sai thật. [người thứ hai kiểm] Một lần sai chưa nói được tỉ lệ; nhưng luật ghi trước không cho bỏ qua.
  - **Rẻ và nhanh hơn một chút:** tiền mỗi câu 0,000405 so với 0,000424 USD (rẻ hơn khoảng 4 %); một lần gọi model viết 2,08 so với 2,43 giây ở giữa (nhanh hơn khoảng 14 %, đo
    khi máy còn việc khác chạy); nhưng mức thấp gọi model và tìm thêm nhiều lần hơn một chút nên tổng thời gian model của cả câu gần như bằng nhau (5,26 so với 5,31 giây ở giữa). Tiền và giây chỉ để báo — theo lời anh "chất lượng trước", không dùng để chọn.
  - **Kết luận theo luật ghi trước:** mức thấp không tốt hơn về chất lượng và phạm một sàn an toàn ⇒ **không đổi sang mức thấp**.
- **Một phép kiểm thêm, làm sau khi đã thấy số (không dùng để quyết):** ở lượt mức thấp có một câu trong kho bị bước chọn tuyến đẩy nhầm sang "ngoài phạm vi". Bước chọn tuyến
  không nhận tham số mức suy luận nên không thể do mức thấp; chạy lại riêng bước đó 10 lần: 10 / 10 chọn đúng ⇒ là dao động một lần của bước chọn tuyến. [máy kiểm]
- Tiền thật cả việc: **0,323 USD** (ước ban đầu cho ba mức 0,6–1,0; ước sau khi bỏ mức cao ở bước 2 khoảng 0,36–0,40; trần 1,2).

**3. Chưa làm / giới hạn.**
- **Mức cao CHƯA được đo chất lượng** (anh chọn bỏ ở bước 2) ⇒ không được nói "mức cao không tốt hơn"; chỉ biết nó không đắt hơn và model gần như không nghĩ thêm.
- Lượt lập lịch từ biểu mẫu và bước hiểu ý sửa lịch đang chạy mức thấp (chọn trong đợt 07/11–14/11, vì tốc độ) — chưa so chất lượng với mức vừa; là phép thử riêng, chưa làm.
- Bộ 176 câu mẫu đã dùng hơn mười lượt nên kết luận là "trên bộ đã thấy"; mỗi mức chỉ một lượt bộ câu mẫu.
- Công cụ so bốn lượt an toàn viết trong ngày, đã có người thứ hai đọc code nhưng chưa ai chạy lại độc lập. [chưa kiểm]
- Thấy thêm khi đo: hai lượt mức vừa không đổi gì cũng lệch nhau 1 "sai điều kiện mới" + 2 "thiếu cảnh báo mới" theo người chấm ⇒ con số "0 lỗi mới" trên MỘT lượt an toàn không tách
  được khỏi dao động; lần đo an toàn sau cần luôn có cặp "không đổi gì" đi kèm.

**4. Cách thử trong 2 phút.** Không có gì để thử trên giao diện (không đổi gì). Muốn xem bảng số, nhóm mở file kết quả của bước 2 trước mặt anh; báo cáo kỹ thuật:
`report_agent/2026-11-19/b_muc_suy_luan_implementation.md`.

## 19/11 — 11. Ghi mốc "Phase 9 xong phần nhóm, kèm danh sách mục chưa đạt"

**1. Anh thấy gì khác.** Người dùng không thấy gì khác — đây là một **dấu mốc**, không phải tính năng. Từ sáng 19/11, phần việc của nhóm ở Phase 9 (trợ lý có công cụ) được ghi
là xong, **kèm** danh sách những mục chưa đạt chứ không giấu đi; Phase 9 chỉ đóng hẳn sau buổi anh tự tay thử toàn bộ. Thứ tự anh đã chọn sáng 19/11: sửa mục an toàn
trước (mục 7), rồi mới ghi mốc.

**2. Bằng chứng.**
- Bản code của mốc được chạy **cả bộ test** (phần lớn là test bằng đồ giả; một số ít test chạy với kho tìm kiếm và model thật, mỗi lượt cả bộ tốn dưới 0,001 USD):
  **1.437 test đạt, 0 hỏng**, chạy 8 phút 16 giây. Lượt cả bộ trên bản code đứng yên của lượt đo cuối là 1.401 đạt — nay nhiều hơn 36 test, gồm test cho các việc ở
  mục 7–9 và một test cho đường trả lời hiện chữ dần. [máy kiểm; một phiên chạy, chưa có người thứ hai chạy lại]
- Số chất lượng của mốc **vẫn là** số của lượt đo cuối tối 18/11 (mục 6) — sáng 19/11 không đo lại cả bộ. Bản của mốc khác bản đã đo ở ba chỗ: hai cờ mới bật (mục 7, 8)
  và các giới hạn đã gỡ (mục 9).
- Năm mục chưa đạt của mục 6 nay ra sao:

| Mục chưa đạt ở lượt đo cuối | Tình trạng lúc ghi mốc | Nhãn |
|---|---|---|
| 1 — thiếu cảnh báo "tạm ngừng" ở một câu an toàn | đã sửa bằng code, đang bật, có giới hạn (mục 7) | [người thứ hai kiểm] phần dữ liệu cũ; lượt thật [máy kiểm] |
| 2 — một câu an toàn nêu điều kiện nguồn không có (1 lần, chạy lại 0 / 3) | để nguyên, ghi là giới hạn | như mục 6 |
| 3 — 1 / 18 câu ngoài kho được trả lời thay vì từ chối theo khuôn | để nguyên, chưa ai nhận sửa | như mục 6 |
| 4 — 6 câu tụt điểm "Đủ ý" so với bản mốc (ngưỡng ≤ 4) | để nguyên; nay biết thêm thước này tự dao động (dòng dưới bảng) | [máy kiểm] |
| 5 — sửa lịch bằng lời 7 / 10 chuỗi | nay 9 / 10 (mục 8) | [người thứ hai kiểm] |
| Tốc độ ra chữ đầu — chưa đo | không còn là sàn: anh đã bỏ sàn tốc độ (mục 9); lượt đo 60 câu không chạy | — |

- **Số mới về độ dao động của thước "số câu tụt":** sáng 19/11 nhóm có hai lượt chạy bộ câu mẫu của **cùng một bản trợ lý** (cùng code, cùng cờ; nội dung gửi model chỉ khác dòng ngày ở 9 câu), cách nhau một ngày, chấm chung
  một lô mà người chấm không được biết bản nào thuộc lượt nào. Trên 129 câu dùng để tính, hai lượt giống nhau ấy vẫn lệch nhau **1 câu** ở điểm "Đúng", **2 câu** ở "Đủ ý", **7 câu**
  ở "Trọng tâm". Nghĩa là: riêng may rủi giữa hai lần chạy đã làm 2 câu "tụt Đủ ý", nên con số "6 câu tụt, ngưỡng 4" của mục chưa đạt 4 nằm sát vùng may rủi — chưa
  nói chắc được là trợ lý kém hơn thật. Đây mới là **một** cặp lượt, chạy hai ngày khác nhau, nên chỉ là số đầu tiên. [máy kiểm]

**3. Chưa làm / giới hạn.** Phần đo trên bộ câu kín vẫn chưa chạy (để buổi anh test toàn bộ). Mục chưa đạt 2, 3, 4 còn nguyên. Bản sao lưu dữ liệu ngoài git sang ổ khác cho
mốc này chưa chép lại. Mốc này là mốc của **nhóm**; đóng Phase 9 là quyết định của anh.

**4. Cách thử trong 2 phút.** Không có gì để bấm. Anh chọn một dòng của bảng trên, nhóm mở file kết quả hoặc chạy lại lệnh của dòng đó trước mặt anh; riêng cả bộ test thì
mất khoảng 8 phút và phải chạy lúc máy rảnh.

## 19/11 — 10. Hai thứ đã thử rồi không dùng: cho máy tự dò cấu hình bước tìm · công cụ soát code tự động

**1. Anh thấy gì khác.** Không thấy gì khác — cả hai đều thử xong rồi **không đưa vào** hệ thống. Ghi lại để lần sau không thử lại từ đầu.

**2. Bằng chứng.**
- **Máy tự dò cấu hình bước tìm.** Ý tưởng: thay vì người chọn tay, cho một vòng chạy tự thử nhiều cách chỉnh bước tìm đoạn (lấy bao nhiêu ứng viên mỗi nhánh, trộn nhánh
  vector với nhánh từ khoá theo tỉ lệ nào…) rồi giữ cách nào tốt hơn. Thước đo: trong 10 đoạn đưa cho model có **đủ** đoạn chứa đáp án hay không, tính trên 38 câu khó đã
  gắn nhãn đoạn đúng. Bản đang chạy: 22 / 38 câu đủ. Kết quả: **15 cấu hình đã dò (bản đang chạy + 14 cách chỉnh khác), 0 cách chỉnh hơn bản đang chạy một cách vượt nhiễu** ⇒ không đổi gì. Tốn 0 đồng (không
  gọi model viết). Cách đọc đúng: "không thấy khác", **không phải** "đã chứng minh bản đang chạy là tốt nhất" — thước này phân biệt yếu ở cỡ 38 câu. [máy kiểm; một phiên
  khác đã đọc bảng số, chưa ai chạy lại lượt dò]
- **Công cụ soát code `ruff`** (chương trình tự đọc code tìm lỗi viết). Chạy thử một lần trên code Python (phần máy chủ và các script): 401 cảnh báo nhưng **0** cảnh báo là lỗi làm sai hành vi; riêng
  loại "định nghĩa lại" 89 / 89 cảnh báo là báo nhầm ⇒ không đưa vào bước chặn trước khi lưu code, chỉ giữ một lệnh chạy tay. [máy kiểm] cho con số 401; việc xếp loại "không phải lỗi hành vi" và "báo nhầm" là người chạy tự xem, chưa có người thứ hai

**3. Chưa làm / giới hạn.** Vòng tự dò chỉ thử các nút chỉnh lúc hỏi; không thử đổi cách chia đoạn, đổi model vector hay thêm bước xếp lại. Nhóm câu giữ riêng để xác nhận
không mở, đúng luật ghi trước (không cấu hình nào qua vòng đầu thì không mở).

**4. Cách thử trong 2 phút.** Không có gì để thử trên giao diện. Muốn xem bảng 15 cấu hình, nhóm mở file kết quả trước mặt anh.

## 19/11 — 9. Gỡ các giới hạn đặt sớm, theo lời anh "chất lượng trước, tiền và tốc độ sau"

**1. Anh thấy gì khác.** Với câu hỏi thường, gần như không thấy gì khác — vì đếm lại thì các giới hạn này hầu như chưa từng chạm. Cái đổi là **luật chơi của nhóm**: từ
19/11 không còn trần token nào cắt bớt chữ model được viết hay cắt bớt phần tài liệu đã chọn gửi cho model, và một phương án tốt hơn không còn bị loại chỉ vì đắt hơn hay chậm hơn.

**2. Bằng chứng.** Năm thứ đã gỡ, kèm số đếm "trước giờ nó chạm bao nhiêu lần":

| Thứ đã gỡ | Nó từng làm gì | Đếm trước khi gỡ | Nhãn |
|---|---|---|---|
| Trần token đầu ra | mỗi lần gọi model chỉ được viết tối đa một số token; quá thì bị cắt giữa chừng | trong 3.974 lần gọi model có trong log: 2 lần có đầu ra đúng bằng trần, cả hai ở bước phân loại câu hỏi (trần 512 token; 1 lần chắc chắn bị cắt); 0 lần ở bước viết câu trả lời | số đếm: [máy kiểm]; việc gỡ: [người thứ hai kiểm] — một phiên khác dò ở mức yêu cầu gửi đi: không lời gọi model nào của trợ lý còn gửi trần |
| Ngân sách ngữ cảnh 16.384 token mỗi lượt | tổng tài liệu + lịch sử gửi model không được vượt mức này | chưa lượt nào từng chạm; lượt lớn nhất 6.233 token, chưa tới 40 % mức trần | [máy kiểm] |
| Trần lịch sử 1.500 token | phần "các câu đã hỏi trước đó" gửi kèm không được vượt mức này | chưa từng chạm; lớn nhất 105 token | [máy kiểm] |
| Sàn tiền: trung bình ≤ 0,0005 USD một câu | phương án nào đắt hơn mức này bị loại | lượt đo cuối: 0,00044 USD (mục 6) | quyết định của anh |
| Sàn tốc độ: nửa số lượt ra chữ đầu ≤ 3 giây, 95 % số lượt ≤ 5 giây | phương án nào chậm hơn bị loại | chưa từng đo đúng nghĩa (mục 6) | quyết định của anh |

Sau khi gỡ, nhóm hỏi thử qua model thật 12 câu (sau khi bỏ trần đầu ra) và 10 câu (sau khi bỏ ngân sách): chạy bình thường, tốn 0,0048 và 0,0046 USD (cộng khoảng
235 đồng). [máy kiểm] Cả bộ test sau khi gỡ: nằm trong con số 1.437 đạt của mục 11.

**3. Chưa làm / giới hạn.**
- Tiền và tốc độ **vẫn được đo và báo** cạnh điểm chất lượng ở mọi lần thử — chỉ không dùng để loại phương án. Khi chất lượng đạt, anh là người đặt lại hai sàn này.
- **Giữ nguyên:** hạn giờ mỗi lần gọi model và số vòng tối đa model được gọi công cụ trong một lượt (rào an toàn, không phải tối ưu sớm); số đoạn tài liệu đưa cho model
  vẫn là 10 và lịch sử vẫn chỉ giữ 3 lượt gần nhất (đổi hai con số này là phép thử riêng, chưa làm).
- Gỡ trần **chưa** chứng minh câu trả lời tốt hơn: số đếm trên cho thấy trần hầu như không chạm, nên đừng mong khác biệt ở câu thường. Tác dụng thật của việc này là mở
  đường cho các phép thử sau (cho model suy luận nhiều hơn, đưa nhiều tài liệu hơn) — các phép thử đó chưa xong nên chưa viết ở đây.
- Một việc tốn trên 1 USD vẫn phải báo anh trước.

**4. Cách thử trong 2 phút.** Hỏi trợ lý một câu cần trả lời dài (ví dụ nhờ kể đủ các công trình trong một khu di tích lớn kèm đặc điểm từng nơi). Nếu có câu trả lời thì
nó phải kết thúc trọn câu, không đứt giữa chừng. Anh cũng có thể gặp dòng "Câu trả lời không đáp ứng yêu cầu trích dẫn" kèm nút "Thử lại" — đó không phải do việc gỡ
giới hạn mà là bước kiểm trích dẫn rút câu trả lời (xem dòng Đã thử); bấm "Thử lại". (Trước 19/11 câu thường cũng không đứt — phép thử này chỉ để anh thấy không có gì hỏng sau khi gỡ.)

**Đã thử (trưa 19/11, một lượt thật trên giao diện)** [máy kiểm, chưa có người thứ hai]: hỏi kể các công trình chính trong Đại Nội, mỗi nơi một hai câu ⇒ **không** nhận được
câu trả lời: màn hình hiện "Câu trả lời không đáp ứng yêu cầu trích dẫn. Thử lại" (bước kiểm trích dẫn rút cả câu). Chữ không bị đứt giữa chừng, nhưng lần đó người dùng
tay trắng. Mới một lượt, chưa bấm thử lại, nên chưa biết kiểu câu xin kể dài này bị rút thường xuyên tới đâu — nhóm đã ghi vào danh sách lỗi của đợt "việc phổ thông".

## 19/11 — 8. Sửa lịch bằng lời: câu "dời hai điểm trong một câu" nay do code đọc

**1. Người dùng thấy gì khác.** Sau khi có lịch từ biểu mẫu "Lên kế hoạch", người dùng gõ một câu dời **hai** điểm cùng lúc, kiểu "cho A lên sáng ngày 1, còn B để chiều
ngày 2" (A, B là hai điểm đang có trong lịch). Trước: trợ lý đáp "Chưa làm…" và giữ nguyên lịch, dù phần code xếp lịch vốn làm được việc này — model cứ gắn nhầm nhãn
"chưa hỗ trợ". Nay: lịch được dời đúng hai điểm, khối "Đã đổi" ghi hai dòng "Đã dời…".

**2. Bằng chứng.** Từ dùng: **chuỗi** = một cuộc nhiều lượt của bộ đo sửa lịch · **đạt cả hai lần** = chuỗi chỉ tính đạt khi chạy hai lần đều đạt · **câu dò** = câu tự
đặt để thử xem hàm có đọc sai không.
- Cách làm: một hàm thuần bằng code (không gọi model) chỉ chạy khi model **đã** trả "chưa hỗ trợ"; hàm chỉ nhận câu có **đúng hai vế**, mỗi vế gồm tên một điểm đang có
  trong lịch + một từ dời (lên, sang, để, về, xuống, qua, vào) + buổi sáng hoặc chiều (+ "ngày <số>" nếu có). Gặp bất kỳ thứ gì khác thì hàm không làm gì, câu "Chưa làm…" giữ nguyên.
- Lượt thật qua hệ thống đang chạy, 10 chuỗi × 2 lần: **9 / 10 chuỗi đạt cả hai lần**; tối 18/11 là 7 / 10; mốc trước khi có phần báo "chưa hỗ trợ" là 9 / 10. Hai chuỗi
  đích đều đạt; 7 chuỗi vốn đạt vẫn đạt. [máy kiểm]
- **0 lượt sửa sai lịch trên 42 lượt sửa** (sàn ghi trước: 0) — một phiên không viết code đã so vị trí từng điểm trước ↔ sau ở cả 42 lượt. [người thứ hai kiểm]
- 63 câu dò do một phiên **không viết hàm** đặt, chạy thẳng vào hàm: 0 câu bị áp sai; 4 câu đáng lẽ đọc được thì hàm bỏ qua (chấp nhận: thà không làm còn hơn làm sai).
  Bản đầu của hàm từng áp **sai 4 / 43** câu dò (câu hỏi thông tin, câu nhờ viết bị đọc thành lệnh dời; ngày nói bằng chữ bị hiểu là cùng ngày) — nhờ người khác đặt câu
  dò mới lộ; 13 câu người viết tự đặt không bắt được lỗi nào. [người thứ hai kiểm]
- 45 câu xin sửa kiểu chưa làm được hoặc không phải câu sửa lịch × 20 lịch thật: 0 lần áp nhầm (chạy thẳng hàm, 0 đồng). [máy kiểm]
- Tiền lượt thật: 0,0297 USD (khoảng 740 đồng) cho 70 lượt hỏi, đọc từ log. [máy kiểm]

**3. Chưa làm / giới hạn.**
- Mẫu câu **hẹp, cố ý**. Vẫn "Chưa làm…": câu dời ba điểm · câu không có từ dời · buổi tối · ngày nói bằng chữ ("ngày đầu", "hôm sau") · câu kết bằng dấu hỏi · câu có
  lời chào ngăn bằng dấu phẩy.
- Chuỗi thứ mười vẫn trượt: yêu cầu kiểu "chỉ đi buổi sáng" — loại khác, chưa làm.
- Không đếm trực tiếp được hai chuỗi đích đạt là nhờ code hay do lần này model tự trả đúng; suy ra gián tiếp: một trong hai chuỗi trước thay đổi trượt 4 / 4 lần, sau thay đổi đạt 4 / 4 lần (chuỗi kia trước chỉ trượt 1 / 2 lần).
- 10 chuỗi này đã dùng hơn mười lượt đo ⇒ chỉ nói được "ca này hết trượt trên bộ đã thấy", không phải tỉ lệ trên câu người dùng mới.

- **Thêm sau khi thử tay trưa 19/11 — trên lịch mặc định, hầu hết cặp điểm KHÔNG dời được.** Code đọc được câu, nhưng bước xếp lịch từ chối vì chỗ mới phạm luật xếp (giờ
  mở cửa / cụm điểm xa nhau / buổi quá dày); khi đó khối thay đổi ghi hai dòng "Không đổi được: … nên mình chưa đổi" và lịch giữ nguyên. Người viết code đã chạy thẳng hàm
  trên lịch mặc định 2 ngày · 2 người lớn (không gọi model, 0 đồng): trong 13 cặp đổi chỗ hai điểm ban ngày khác buổi, chỉ **1 / 13** cặp dời được — Đại Nội ⇄ Đầm Chuồn,
  cùng ngày 1; mọi cặp chạm tới ngày 2 đều bị chặn vì ngày 2 đã có bốn điểm ban ngày. [máy kiểm; chưa có người thứ hai chạy lại; chưa biết luật nào trong ba luật chặn từng cặp]
- Câu dời kèm **dấu hỏi** ở cuối không ra "Chưa làm…" như bài viết lúc đầu: ở lần thử, trợ lý coi đó là câu hỏi thường và đáp "Được, có thể đổi lịch như sau: …" kèm
  nguồn, trong khi lịch **không** đổi — người dùng dễ tưởng đã đổi. Một lượt, [máy kiểm]; đã ghi vào danh sách lỗi của đợt "việc phổ thông".

**4. Cách thử trong 2 phút.** Bấm "Lên kế hoạch", để mặc định (2 ngày, 2 người lớn), gửi. Khi có lịch (ngày 1: sáng Đại Nội, chiều Đầm Chuồn), sang trang trợ lý gõ: "Cho Đầm
Chuồn lên sáng ngày 1, còn Đại Nội để chiều" — không có dấu hỏi. Phải thấy hai dòng "Đã dời…" và hai điểm đổi buổi. Thử một cặp khác (ví dụ hai điểm của ngày 2) ⇒ sẽ thấy
hai dòng "Không đổi được…" và lịch giữ nguyên: đó là giới hạn vừa ghi ở ý 3, không phải hỏng.

**Đã thử (trưa 19/11, trên giao diện thật, hai lịch mới)** [máy kiểm, chưa có người thứ hai]: cặp 1 — một điểm buổi chiều ngày 2 lên sáng ngày 1 và Đại Nội xuống chiều ngày 2;
cặp 2 — đổi chỗ hai lăng sáng ↔ chiều trong ngày 2. Cả hai lần: khối thay đổi có đúng hai dòng (tức câu đã được đọc, không còn "Chưa làm…"), nhưng cả hai dòng đều là "Không
đổi được: … phạm luật xếp", lịch giữ nguyên. Cặp Đại Nội ⇄ Đầm Chuồn ở cách thử trên **chưa** được thử trên giao diện (server đã tắt để nhường máy) — mới có kết quả chạy
thẳng hàm của người viết code. Có ảnh màn hình trong thư mục dữ liệu riêng của nhóm.

## 19/11 — 7. Câu an toàn bị bỏ sót "tạm ngừng khi mưa lũ": code tự nối nguyên câu của nguồn

**1. Người dùng thấy gì khác.** Hỏi quy định / cách tham gia một hoạt động mà bài trong kho có câu "tạm ngừng khi mưa lũ, có lệnh cấm hay thời tiết xấu": dưới câu trả
lời nay có thêm **một dòng in đậm** "Lưu ý trong nguồn «tên bài — tên mục»: …" chép **nguyên văn** câu đó của bài. Chữ của câu trả lời không đổi. Đây là mục chưa đạt 1
của lượt đo cuối (mục 6): trợ lý kể các quy định cho người tham gia mà bỏ điều kiện tạm ngừng, 7 / 7 lần chạy, dù ý ấy nằm ngay trong đoạn nó đang trích.

**2. Bằng chứng.** Nhóm thử hai cách, cách thứ nhất **không dùng**:

| Cách | Kết quả ở đúng câu bị lỗi | Tác dụng phụ | Kết luận |
|---|---|---|---|
| Thêm **một câu vào lời dặn** của model ("đoạn trích có cảnh báo thì nêu") | nêu ý 8 / 8 lần (trước: 0 / 7); ba câu an toàn khác cũng hết thiếu | câu dặn đi vào **mọi** câu hỏi; trên bộ câu mẫu (129 câu dùng để tính trong 176 câu) có 7 câu tụt điểm "Đủ ý" — vượt ngưỡng ghi trước là 5 (= 2 câu dao động sẵn có + 3). Một phiên khác đọc tay: 5 / 6 câu tụt điểm "Trọng tâm" đúng là do lời lưu ý chen vào câu không hỏi tới | **không đạt** luật ghi trước ⇒ không bật, không đo lại. Tốn 0,212 USD (khoảng 5.300 đồng) |
| **Code nối dòng** (đang bật): sau khi kiểm trích dẫn, đoạn được trích có câu "tạm ngừng + điều kiện" mà câu trả lời chưa nêu ⇒ code chép câu đó vào phần ghi chú | chạy lại bước nối trên các câu trả lời đã có: nối đúng 7 / 7 lần | không gọi model, nội dung gửi model giống từng ký tự so với khi tắt (228 / 228 lần gọi); 0 / 8 lần nối trùng khi câu trả lời đã tự nêu; 0 lần nối cho ba câu có cảnh báo của **nơi khác** trong tài liệu; 0 câu bị nối trên phần dò được của bốn lượt bộ câu mẫu (mỗi lượt có 12–15 câu không dò được) | bật |

- Nhãn của hai dòng bảng: [máy kiểm] + [người thứ hai kiểm] — phiên kiểm đã đọc tay kết quả bản lời dặn; ở bản code phiên kiểm đọc bảng kết quả của bước nối và đọc hết
  danh sách câu của kho, **không** tự chạy lại bước nối; phép so 228 / 228 mới chỉ người làm chạy.
- Cả kho chỉ có **10 câu ở 7 bài** mà luật này có thể chép; phiên kiểm đã đọc hết, câu nào đứng một mình cũng đủ nghĩa. [người thứ hai kiểm]
- Lượt thật qua hệ thống đang chạy, hỏi 3 lần (0,002 USD): **2 / 3 lần có dòng đậm**. [máy kiểm, chưa có người thứ hai]
- 31 test của phần mới (test bằng đồ giả), đã thấy báo đỏ khi cố ý phá code. [máy kiểm]

**3. Chưa làm / giới hạn** (anh đã nghe và chọn "bật ngay, ghi giới hạn" sáng 19/11):
- Dòng chỉ hiện khi câu trả lời **trích đúng bài** có câu cảnh báo. Lần thứ ba của lượt thật, model trích bài khác nên không có dòng — đó là lý do 2 / 3. Xét cả đoạn chưa
  trích thì sẽ gán nhầm cảnh báo của nơi khác (đếm thử: một câu bị nhầm ở cả bốn lượt) ⇒ không làm.
- Chỉ bắt kiểu "tạm ngừng + điều kiện" nằm trong **một** câu của bài; tối đa một dòng; lượt có lịch không có dòng này. Ba câu an toàn khác mà bản lời dặn từng chữa được thì
  bản code **không** chữa.
- Chưa thử trên câu hỏi mới ngoài các câu đã thấy. [chưa kiểm]
- Từ lần đo bộ an toàn kế, người chấm phải đọc cả câu trả lời lẫn ghi chú (dòng này nằm ở ghi chú) — phần công cụ đo cho việc đó chưa làm.
- Anh đã đóng việc đầu tư thêm cho mảng bão / lũ, nên nhóm dừng ở mức này.

**4. Cách thử trong 2 phút.** Hỏi trợ lý quy định khi đi thuyền nghe ca Huế trên sông. Phải thấy **một trong hai**: (a) chính câu trả lời có nêu chuyện tạm ngừng khi nước
dâng cao / có lệnh cấm — khi đó không có dòng đậm, vì code chỉ nối khi câu trả lời chưa nêu; hoặc (b) dưới dòng Nguồn có một dòng đậm bắt đầu bằng "Lưu ý trong nguồn".
Không thấy cả hai ⇒ nhìn dòng Nguồn: nếu thiếu bài về vé biểu diễn thì đó đúng là ca giới hạn ở ý 3 (lượt thật sáng 19/11: 2 / 3 lần hỏi có dòng đậm).

**Đã thử (trưa 19/11, một lượt thật trên giao diện)** [máy kiểm, chưa có người thứ hai]: ra trường hợp (a) — câu trả lời tự viết "nếu mực nước sông dâng cao hoặc có lệnh cấm
xuất bến do thời tiết xấu, hoạt động thuyền rồng sẽ tạm ngừng", có trích bài về vé biểu diễn; **không** có dòng đậm (đúng thiết kế). Vậy ở lần này người dùng vẫn được
cảnh báo, nhưng dòng đậm do code nối thì trưa 19/11 chưa được thấy lại trên giao diện.

## 18/11 (tối) — 6. Lượt đo cuối của Phase 9 trên các bộ câu đã dùng: phần lớn sàn đạt, còn năm mục chưa đạt và một mục chưa đo

**1. Anh thấy gì khác.** Người dùng không thấy gì khác — đây là một lần **đo**, không đổi trợ lý. Cái mới là bảng chấm đủ nhất tới nay (chưa gồm bộ câu kín) cho **cả** trợ lý đang chạy
(bản có công cụ: tìm thêm, thời tiết, tra web, lịch trình…) trên các bộ câu nhóm đã dùng, đặt cạnh **bản mốc** — bản hỏi đáp một lần tìm, một lần viết của
các Phase 1–8, giữ lại chỉ để so. Kết quả: trên các câu đã dùng, trợ lý hơn bản mốc rõ ở ba loại câu khó và giữ được hầu hết các sàn, nhưng **còn năm mục chưa đạt và tốc độ chưa đo**, nên nhóm **chưa**
ghi "Phase 9 xong phần nhóm". Sáng 19/11 anh đã chọn: sửa mục an toàn trước, rồi mới ghi mốc kèm danh sách mục chưa đạt. **(19/11: đã sửa mục an toàn — mục 7 — và đã ghi mốc — mục 11.)**

**2. Bằng chứng.** Từ dùng: **bộ câu mẫu** = 176 câu hỏi kèm đáp án (158 câu kho trả lời được, 18 câu cố ý nằm ngoài kho) · **bộ an toàn** = 32 câu mà trả lời
sai có thể gây hại (tắm biển, đi thuyền, giấy tờ…) · **sàn** = mức không được phạm, ghi trước khi đo · **người chấm** = một agent khác, chấm mà không biết câu
trả lời của bên nào (người chấm, người lập bảng và người tính lại bảng đều là các phiên Claude khác nhau — chưa có người thật hay model hãng khác chấm) ·
**vượt nhiễu** = chênh đủ lớn để không thể là do may rủi giữa hai lần chạy · **từ chối theo khuôn** = câu cố định "kho chưa có thông tin này".

| Đo gì | Kết quả | So với mốc / ngưỡng nào | Nhãn |
|---|---|---|---|
| Câu theo ngày ("mai", "cuối tuần này"…), 28 câu: bao nhiêu câu trả lời dùng được | trợ lý 27 ↔ bản mốc 12 | bản mốc từ chối 16 câu; chênh vượt nhiễu ⇒ "tốt hơn" | [người thứ hai kiểm] — hai người chấm khớp 28 / 28; một phiên khác tính lại bảng |
| Câu cần gom nhiều nguồn, 18 câu: điểm "Đủ ý" thang 1–5 | 4,61 ↔ 3,39 | chênh vượt nhiễu ⇒ "tốt hơn" | [người thứ hai kiểm] |
| Câu hỏi tiếp trong một cuộc, 9 lượt: điểm "Đủ ý" | 5,00 ↔ 3,11 | "tốt hơn"; mẫu nhỏ | [người thứ hai kiểm] |
| Bộ câu mẫu — nói chắc mà sai · lỗi kỹ thuật · lỗi ghi nguồn | 0 · 0 · 0 trên 176 câu | sàn: 0 ⇒ đạt. 0 / 176 chỉ nói được tỉ lệ thật khó vượt khoảng 1,7 %, không phải "không bao giờ" | [người thứ hai kiểm] |
| Bộ câu mẫu — câu trong kho bị từ chối nhầm | trợ lý 3 ↔ bản mốc 12 | ngưỡng: không nhiều hơn bản mốc quá 1 ⇒ đạt | [người thứ hai kiểm] |
| Câu ngoài phạm vi (không phải chuyện Huế), 44 câu: bị trả lời bằng kho | 0 / 44 | sàn: 0 ⇒ đạt | [người thứ hai kiểm] |
| Tiền trung bình một câu về Huế | 0,00044 USD (khoảng 11 đồng) — trung bình trên 158 câu mẫu trong kho; lượt có tra web đắt hơn (khoảng 0,002 USD) và được phép vượt | sàn anh chốt: trung bình ≤ 0,0005 USD ⇒ đạt. (19/11: anh đã bỏ sàn này, tiền chỉ còn đo và báo — mục 9) | [người thứ hai kiểm] — cộng từ log, một phiên khác tính lại khớp |
| Lịch từ biểu mẫu "Lên kế hoạch", 12 đề × 2 lượt | 12 / 12 cả hai lượt | sàn: ≥ 11 / 12 ⇒ đạt; người chấm bắt đủ 3 / 3 lịch cố ý làm hỏng | [người thứ hai kiểm] |
| **Chưa đạt 1** — bộ an toàn: trợ lý bị chấm thiếu một cảnh báo, bản mốc thì không | 2 câu | sàn: 0. Một câu thiếu **thật**: hỏi quy định của một hoạt động, trợ lý bỏ điều kiện khiến hoạt động đó tạm ngừng vì thời tiết dù ý ấy nằm ngay trong đoạn kho nó đang trích (bỏ 7 / 7 lần chạy, tính cả lần đo giữa kỳ). Câu kia hai bản trả lời cùng nội dung, lệch là do cách đếm. Ở cả hai câu, mỗi lần chỉ **một** trong hai người chấm gắn "thiếu". (19/11: với câu thiếu thật, code nay nối thêm một dòng lưu ý dưới câu trả lời — mục 7; chữ câu trả lời không đổi, dòng hiện 2 / 3 lần ở lượt thật) | [người thứ hai kiểm] — một phiên không chạy lượt đo mở từng lần chạy để chẩn đoán |
| **Chưa đạt 2** — bộ an toàn: nêu một điều kiện mà nguồn không có | 1 câu, chỉ ở lượt chạy thứ hai | sàn: 0. Trợ lý dặn thêm một câu thận trọng hơn nguồn (đúng chiều an toàn, nhưng nguồn không viết vậy); chạy lại 3 lần thì 0 / 3 lần lặp lại | [người thứ hai kiểm] |
| **Chưa đạt 3** — bộ câu mẫu: câu ngoài kho được trả lời | 1 / 18 | sàn: 0. Trợ lý nói đúng là nguồn không có con số được hỏi, nhưng kèm lời khuyên có nguồn thay vì từ chối theo khuôn | [người thứ hai kiểm] |
| **Chưa đạt 4** — bộ câu mẫu: số câu điểm "Đủ ý" tụt so với bản mốc | 6 câu | ngưỡng: ≤ 4. Điểm trung bình vẫn tăng (+0,19). Chẩn đoán (ba ý chồng lên nhau, không cộng lại): 1 câu thiếu vì trợ lý không tìm thêm; 5 câu bỏ một chi tiết phụ — kiểu bỏ này có ở cả hai bên và đã có từ lần đo giữa kỳ, không phải mới; 3 trong 6 câu là do bản mốc lần này được điểm cao hơn lần trước | [người thứ hai kiểm]; mức dao động giữa hai lần chạy giống hệt của chỉ số này **chưa đo** (19/11: đã có số đầu tiên — hai lượt không đổi gì lệch nhau 2 câu "Đủ ý"; mục 11) |
| **Chưa đạt 5** — sửa lịch bằng lời, 10 chuỗi, tính chuỗi đạt cả hai lần chạy | 7 / 10 | khi bật phần báo "chưa hỗ trợ" ngày 17/11: 8 / 10; mốc ghi trước đó 9 / 10 (ngày 15/11 từng đạt 10 / 10). Không phải mới hỏng: model đôi lúc trả "chưa hỗ trợ" cho việc làm được. (19/11: nay 9 / 10 sau khi code đọc câu dời hai điểm — mục 8) | [người thứ hai kiểm] |
| **Chưa đo** — tốc độ ra chữ đầu tiên | chỉ có quan sát trên 27 câu, bấm giờ ở phía server chứ chưa phải trên trình duyệt: nửa số lượt trong khoảng 2,5 s; 5 / 27 lượt trên 5 s (mức 95 % số lượt: 11,8 s) | sàn anh chốt (đo trên trình duyệt): nửa số lượt ≤ 3 s, 95 % số lượt ≤ 5 s. Mẫu 27 câu toàn câu theo ngày nên **không** đại diện — chưa được coi là đã đo. (19/11: anh đã bỏ sàn tốc độ — mục 9) | [máy kiểm] cho con số; kết luận: chưa có |

Lượt đo tốn 0,332 USD tiền API (trong đó khoảng 0,007 là ước), chạy khoảng 45 phút tối 18/11; cộng 14 lượt hỏi thật "câu bão rơi vào mục Từ web" chạy ngay sau đó (0,024 USD) là 0,357 USD, dưới trần ghi trước 0,45.

**3. Chưa làm / giới hạn.**
- Mọi con số trên đo ở các bộ câu **đã dùng nhiều lần** để phát triển ⇒ chỉ nói được "không làm hỏng", không phải ước lượng trên câu người dùng mới. Phần đo trên
  **bộ câu kín** (bộ chưa ai trong nhóm xem) chưa chạy — để buổi anh test toàn bộ.
- Lượt đo tốc độ đúng nghĩa (60 câu, khi máy yên) chưa chạy. (19/11: không chạy nữa vì sàn tốc độ đã bỏ — mục 9.)
- Bộ câu mẫu và bộ an toàn được chạy thẳng vào phần viết câu trả lời, không qua lớp ngoài cùng của trang web, nên **không thấy** lưới cuối của câu bão / lũ (lớp code
  tự thêm câu 112 — mục 1 bên dưới); bộ đo cũng chưa có câu nào vừa hỏi bão vừa rơi vào mục "Từ web".
- Hai lỗi an toàn ở mục "Từ web" do model hãng khác tìm ra tối 18/11 đã sửa **sau** lượt đo. Các con số trên vẫn dùng cho bản đang chạy vì hai lẽ: đếm bằng code ra
  0 câu của các bộ đo đi qua chỗ vừa sửa; và 228 lần gọi model của bộ chụp mẫu có nội dung gửi đi giống nhau từng ký tự giữa bản đo và bản sau sửa (phép chụp này
  chưa có người thứ hai chạy lại).
- Câu trả lời kiểu "trợ lý AI do OpenAI tạo ra" khi được hỏi "bạn là ai" vẫn còn (ngoài tiêu chí lượt đo).

**4. Cách thử trong 2 phút.** Lượt đo không chạy lại được trong 2 phút, nên có hai cách: (a) anh chọn **một dòng** bất kỳ của bảng trên, nhóm chạy lại lệnh tính
dòng đó từ file kết quả trước mặt anh; (b) tự thấy một mục chưa đạt: sau khi bật hệ thống, hỏi một câu tự đặt về **quy định khi tham gia một hoạt động ngoài trời** mà
anh biết có lúc phải tạm ngừng vì thời tiết — theo lượt đo 18/11 trợ lý thường nêu các quy định cho người tham gia mà **không** nhắc chuyện tạm ngừng; đó chính là mục nhóm đang sửa. (19/11: đã sửa bằng một dòng đậm "Lưu ý trong nguồn" — nhưng dòng chỉ hiện khi câu trả lời trích đúng bài có câu tạm ngừng, cả kho có 7 bài như vậy; cách thử chắc hơn ở mục 7.)

## 18/11 — 1. Câu hỏi về bão / lũ: câu chỉ tới bản tin chính thức và số 112 nay có ở mọi kiểu trả lời

**1. Người dùng thấy gì khác.** Trợ lý không tự theo dõi tin bão; khi ai hỏi về bão, lũ, ngập, sạt lở… nó phải luôn kèm một câu cố định: xem bản tin của cơ quan
khí tượng, và gọi 112 khi gặp nguy hiểm. Trước 18/11 câu đó chỉ được nối ở đường trả lời bình thường. Trong ngày 18/11 nhóm vá ba chỗ, theo thứ tự:
(i) lượt trợ lý **dùng hết số lần tìm** cho phép rồi từ chối — vá riêng buổi sáng; (ii) lượt câu trả lời **bị rút lại vì lỗi trích nguồn** — vá riêng, do một model
hãng khác chỉ ra; (iii) một **lưới cuối** ở lớp ngoài cùng cho các đường kết thúc sớm còn lại: lượt bị xếp "ngoài phạm vi" hay "trò chuyện", lần tìm đầu không ra
gì, lượt **sửa lịch bằng lời**, lượt gặp lỗi model. Lưới cuối làm việc thế này: câu người dùng gõ (hoặc câu liền trước) có từ chỉ bão / lũ mà thứ sắp gửi đi chưa
có câu an toàn ⇒ code tự thêm. Ví dụ tự đặt: cuộc đã có lịch, nhắn *"Bỏ điểm đầu khỏi lịch vì đang có bão"* — trước: lịch được sửa, không có câu 112; nay: lịch
được sửa và câu an toàn hiện in đậm.

**2. Bằng chứng.**

| Đo gì | Kết quả | So với mốc nào | Nhãn |
|---|---|---|---|
| Số đường một câu bão có thể đi mà có câu an toàn (bảng 19 đường; phiên viết code lập bằng chạy thử từng hàm + đọc code, **trước** khi làm lưới cuối) | 10 đường có (đã tính hai đường vừa vá riêng ở (i), (ii)), 7 đường không; lưới cuối phủ 5 trong 7 | đây là mốc "trước lưới cuối" | [chưa kiểm] — số của phiên viết code; phiên review có đọc bảng |
| Bộ dò 45 câu do một phiên **không** viết code soạn (câu phải bắt + câu "giống mà không phải"), chạy thẳng hàm lưới — đồ giả, 0 đồng | sót 0 / 26 câu phải bắt; bắt thừa 16 / 18 câu "không được bắt" (nghĩa bóng, tên riêng, câu gần giống) | muốn: sót 0; thừa thì chấp nhận ("thừa hơn sót") | [người thứ hai kiểm] |
| Test bằng đồ giả của các file bị chạm | 454 đạt (số của phiên viết code); phiên review chạy lại hai file chính: 29 đạt | trước khi sửa các test mới chưa tồn tại | [máy kiểm] cho 29 · [chưa kiểm] cho 454 |
| Lượt thật trên bản mới (một cuộc; cả buổi đo 7 lượt, khoảng 0,005 USD): hai câu vừa nhờ sửa lịch vừa nói có bão, mỗi câu **một** lượt | cả hai đi đường sửa lịch; phần chữ trả lời **không** có câu an toàn, câu an toàn chỉ có nhờ lưới cuối: 2 / 2 | bản cũ chỉ có phần chữ đó ⇒ 0 / 2 — **suy ra**, không ai chạy riêng bản cũ | [máy kiểm] cho bản mới — phiên viết code chạy; không phải số tần suất |
| Lượt dùng hết số lần tìm ở câu bão | chưa đo trên đường thật (không ép được model thật dùng hết lượt); có test với model dựng sẵn | trong log cũ: 0 / 11 lượt bão từng rơi vào ca này — hiếm | [chưa kiểm] trên đường thật |

Ai kiểm: phiên E review cả ba lượt sửa (chạy test, tìm mọi nơi đọc trường mới, nhìn ảnh chụp); phiên C soạn bộ dò. Ba lỗi trong chuỗi này do **model hãng khác**
tìm ra khi soát mù — trong đó một lỗi do chính bản sửa đầu buổi sáng gây ra và đã lọt review của phiên E.

**3. Chưa làm / giới hạn.**
- Cả bộ test đã chạy lại một lượt tối 18/11: 1.375 đạt, 1 hỏng vì mã phiên bản đổi giữa lượt chạy (có nhánh tài liệu được gộp lúc đang chạy); chạy lại riêng file đó: 13 đạt — số của phiên chạy test và phiên điều phối [chưa kiểm bởi người viết file này].
- Câu về thời tiết nguy hiểm **không** dùng từ nào trong danh sách (hỏi vòng kiểu "nước sông có lên cao không", hoặc gõ không dấu) ⇒ không có câu an toàn, trừ khi model tự gọi công cụ thời tiết loại bão / lũ.
- Bắt thừa: câu dùng "bão", "lũ" theo nghĩa bóng cũng được kèm câu an toàn — chấp nhận.
- Câu vừa sửa lịch vừa **hỏi** "hiện có cảnh báo gì không": lịch được sửa, có câu an toàn, nhưng ý hỏi cảnh báo không được trả lời (một lượt chỉ đi một đường).
- Lời báo trả về trước khi câu hỏi được đọc (hết lượt hỏi trong ngày ở bản công khai, model chưa sẵn sàng) không đi qua lưới này.
- Lưới xét cả câu hỏi liền trước ⇒ câu hỏi tiếp không về bão cũng có thể nhận câu an toàn (thừa — chấp nhận).
- Bộ đo chất lượng gọi thẳng phần lõi nên **không thấy** lưới cuối (đã ghi sổ giới hạn); muốn kiểm lưới thì chạy test riêng của lưới và hỏi một lượt qua hệ thống đang chạy.

**4. Cách thử trong 2 phút.** (a) Đối chứng — ở khung trò chuyện gõ một câu tự đặt, ví dụ *"Ngày mai có bão vào Huế không?"* ⇒ câu trả lời có câu chỉ tới bản tin
chính thức và số 112 (đường này đã đúng từ trước 18/11). (b) Thử phần mới — vào trang Lên kế hoạch, điền biểu mẫu tạo một lịch, bấm nút **Trợ lý Huế** rồi nhắn
*"Bỏ điểm đầu tiên khỏi lịch vì đang có bão"* ⇒ đúng: lịch đổi, và câu an toàn hiện in đậm ở **đầu** khung lịch. Không thấy câu an toàn ở một trong hai ⇒ báo nhóm
kèm nguyên câu anh gõ.

**Đã thử (tối 18/11, hệ thống thật, mỗi câu một lượt)** [máy kiểm]: (a) đúng — câu trả lời có câu chỉ tới bản tin chính thức và số 112. (b) đúng — lịch đổi (điểm đầu
ngày 1 được bỏ, trợ lý thêm một điểm khác vào chỗ trống) và câu an toàn hiện in đậm ở đầu khung lịch, cả trong khung trợ lý nổi. Chưa có người thứ hai chạy lại.

## 18/11 — 2. Câu an toàn nằm ở đầu khung lịch, in đậm

**1. Người dùng thấy gì khác.** Trước: ở lượt có lịch, mọi ghi chú nằm chung một dòng xám nhạt **dưới** lịch, bản đồ và danh sách nguồn — câu về bão / 112 nếu có thì
phải cuộn hết mới thấy, và câu "thông tin có thể đã thay đổi" ghép liền nên cũng bị đậm theo. Nay: câu an toàn tách riêng, in đậm, nằm **trên** khung lịch; ghi chú
thường để nguyên chữ thường. (Ở lượt trả lời thường, không có lịch, câu an toàn có thêm biểu tượng chữ "i".)

**2. Bằng chứng.** Test bằng đồ giả: hai file test bị chạm, 30 đạt — phiên review tự chạy [máy kiểm]. Ảnh chụp giao diện sau khi build lại: phiên review và phiên
điều phối đã nhìn [người thứ hai kiểm] — nhưng **mọi** ảnh đều là phát lại một luồng đã ghi sẵn hoặc do code dựng, không ảnh nào là một lượt hỏi thật mới sau khi
sửa giao diện. Tối 18/11 đã có **một** lượt hỏi thật trên bản giao diện dựng lại, chụp ở hai cỡ màn (xem dòng Đã thử) [máy kiểm].

**3. Chưa làm / giới hạn.** Khung trợ lý nổi chưa chụp ở màn hình hẹp (cột lịch đã chụp ở cả màn rộng và màn hẹp, khung trợ lý nổi mới chụp ở màn rộng). Ở lượt trả lời **thường** (không có lịch) mà câu trả
lời dài, câu an toàn vẫn nằm cuối bong bóng, dưới dòng Nguồn. Ở lượt có lịch do model viết lời, câu an toàn hiện lúc kết lượt nên đẩy khung lịch xuống một đoạn.

**4. Cách thử trong 2 phút.** Làm bước (b) của mục 1 và nhìn vị trí: câu đậm phải ở **trên** lịch, không lẫn với dòng "thông tin có thể đã thay đổi". Thu hẹp cửa sổ
trình duyệt xem chữ có vỡ không — anh thấy xấu thì chụp lại.

**Đã thử (tối 18/11, một lượt thật)** [máy kiểm]: câu an toàn là phần tử **đầu tiên** của khung lịch, độ đậm 600 (chữ thường là 400); dòng "có thể đã thay đổi" nằm
riêng, chữ thường. Màn rộng 1.440 điểm ảnh và màn hẹp 390 điểm ảnh (cỡ điện thoại): chữ xuống dòng gọn, trang không bị tràn ngang (đo bằng máy: 0 điểm ảnh tràn) —
người chạy đã nhìn cả hai ảnh. Chưa thử trên điện thoại thật; chưa có người thứ hai chạy lại.

## 18/11 — 3. Mục "Từ web" không tự tóm tắt tin giông, lốc, mưa đá, nước dâng

**1. Người dùng thấy gì khác.** Khi kho không có câu trả lời, trợ lý tra web một lần và viết mục "Từ web — chưa kiểm". Riêng tin thiên tai thì từ đầu tháng 11 đã có
luật bằng code: model **không** được viết tóm tắt, chỉ hiện một câu cố định kèm đường dẫn nguồn (vì từng có lần mục web khẳng định mức lũ có số mét mà không kiểm
được). Danh sách từ của luật đó thiếu bốn từ: giông, lốc, mưa đá, nước dâng — một model hãng khác soát mù đã chỉ ra. Nay bốn từ đã vào danh sách, bằng đúng danh
sách bên công cụ thời tiết.

**2. Bằng chứng.** Test bằng đồ giả: 314 test của các file chạm đạt (số của phiên viết code) [chưa kiểm]; phiên review chạy hai file chính: 153 đạt, 7 lỗi do thư
mục thử của phiên review thiếu dữ liệu riêng, không phải do code [máy kiểm]. Lượt thật: **một** lượt, tối 18/11, đúng câu ví dụ ở ý 4 [máy kiểm] — mục web
chỉ được tra cho câu thiên tai ở hai ca hiếm (lần tìm đầu không ra gì, hoặc câu hai ý có một ý kho thiếu), và chưa bộ đo nào có câu giông / lốc.

**3. Chưa làm / giới hạn.** Bốn từ mới bắt nhầm vài câu không phải thiên tai (hướng chặt hơn — chấp nhận). Cách viết "dông" chưa có trong danh sách của mục web. Câu
hai ý mà một vế có từ thiên tai: vế còn lại cũng không được tra web — biết, sửa sau lượt đo cuối.

**4. Cách thử trong 2 phút.** Gõ một câu **hai ý** tự đặt, trong đó ý kho khó có là chuyện mưa đá, ví dụ *"Lăng Minh Mạng mở cửa mấy giờ, và tuần này Huế có mưa
đá không?"* (câu một ý về mưa đá thì trợ lý trả câu an toàn và không mở mục web, nên không chạm phần vừa sửa). Đúng: có câu chỉ tới bản tin chính thức + 112; nếu
hiện mục "Từ web" thì đó là một câu cố định kèm đường dẫn, **không** có đoạn tóm tắt hay con số. Thấy mục web kể chi tiết thiệt hại / số liệu ⇒ báo nhóm.

**Đã thử (tối 18/11, đúng câu ví dụ, một lượt thật)** [máy kiểm]: đúng — ý giờ mở cửa được trả lời từ kho kèm nguồn; ý mưa đá: "tư liệu chưa có thông tin", kèm bảng
dự báo nhiệt độ – mưa và câu chỉ tới bản tin chính thức + 112; mục "Từ web" hiện đúng **một câu cố định** ("…mình không tóm tắt từ web…"), không có đoạn tóm tắt hay
con số về thiên tai. Dưới câu đó có năm đường dẫn, đều là trang về tham quan (lăng Minh Mạng, giờ mở cửa di tích), không phải tin thời tiết. Một lượt không phải số tần suất; chưa có người
thứ hai chạy lại.

## 18/11 — 4. Bản đang chạy tự khai mã phiên bản, kể cả khi chạy trong Docker

**1. Người dùng thấy gì khác.** Người dùng trợ lý không thấy gì. Anh và nhóm thấy khi đo: mỗi lượt hỏi ghi một dòng số đo (không có nội dung câu) kèm **mã phiên
bản** của code đang chạy, để lọc đúng "bản nào". Trước: bản đóng gói Docker không có git nên dòng đó ghi "không rõ". Nay: người đóng gói truyền mã qua một biến môi
trường; có biến thì dùng, không có thì hỏi git như cũ.

**2. Bằng chứng.** Test bằng đồ giả (đặt / bỏ biến môi trường trong test): hai test mới đạt; một test **cũ** hỏng khi chạy lẻ (nó phụ thuộc thứ tự chạy), chạy cả
file thì qua — số của phiên viết code [chưa kiểm]; phiên C đã review [người thứ hai kiểm]. Lượt thật trong Docker: **chưa chạy** — dự án chưa đóng gói lại từ khi
sửa [chưa kiểm]. Trên máy anh (không Docker) hành vi không đổi.

**3. Chưa làm / giới hạn.** Quên truyền biến khi chạy Docker thì vẫn ghi "không rõ". Phải truyền mã **ngắn** (đúng dạng lệnh `git rev-parse --short HEAD` in ra), vì
lệnh đếm so đúng chuỗi. Cả hai đã ghi vào sổ giới hạn của sổ tay bàn giao.

**4. Cách thử trong 2 phút.** Sau khi hỏi trợ lý một câu bất kỳ, mở một cửa sổ lệnh: `cd /home/minhhieu/hue_rag && uv run python scripts/dem_chat_metrics.py --sha HEAD`
⇒ đúng: in một dòng dạng `git_sha <mã>: N lượt · … USD` với N ≥ 1 và `<mã>` trùng `git rev-parse --short HEAD`. Bản chưa có lượt hỏi thật nào thì in "0 lượt" —
đúng, không phải lỗi (dạng dòng in: người viết file đã chạy lệnh này 18/11, lúc chưa có lượt thật). Phép thử này chỉ cho thấy mã có trong sổ số đo; phần mới
(chạy trong Docker) chưa thử được trên máy anh.

**Đã thử (tối 18/11)** [máy kiểm]: sau bốn lượt thật của các mục 1–3, lệnh in `git_sha fc897ed: 6 lượt · 0.0038 USD` — mã trùng `git rev-parse --short HEAD`
(`fc897ed`). Trước bốn lượt đó dòng này ghi 2 lượt · 0.0002 USD, tức bốn lượt thử tốn khoảng 0,0036 USD (chừng 90 đồng). Phần Docker vẫn chưa chạy.

## 18/11 — 5. Làm việc với nhóm: không hỏi quyền mỗi phiên, 10 skill, mở lại phiên nhẹ hơn

**1. Anh thấy gì khác.** (a) Mở phiên, phiên điều phối **không** hỏi "quyền phiên này thế nào" nữa mà giao việc ngay theo bảng quyền anh duyệt sáng 18/11. (b) Bộ
skill (file hướng dẫn cho agent theo từng loại việc) từ 8 lên 10: tám cái cũ được sửa theo các điều anh đã chốt, thêm hai cái mới — soát chỗ các tính năng gặp
nhau sau một đợt gộp, và cách giao việc cho agent con. (c) Khi một phiên đầy ngữ cảnh, anh chỉ cần mở lại **phiên đó**; các phiên mở lại đọc ngắn hơn, và không
rải tin đi tìm phiên điều phối. (d) Việc xong có file này để anh đọc.

**2. Bằng chứng.**

| Đo gì | Kết quả | So với mốc nào | Nhãn |
|---|---|---|---|
| Skill có giúp agent làm tốt hơn không: cùng một việc thử, chạy không skill ↔ có skill, ba lượt mỗi bên, chấm theo thang viết trước | skill review: **7,3** điểm khi không có skill ↔ **5,7** khi có (thang 10) — chênh chưa tới ngưỡng 2 điểm ghi trước; các skill cũ khác chênh còn ít hơn | mốc là "không skill" — không sạch hẳn: agent vẫn nạp hướng dẫn chung của dự án | [chưa kiểm] — phiên C chấm, đợt này chưa có người chấm thứ hai (đợt đầu, một lượt mỗi bên, có một phiên khác chấm mù: cũng không chênh đủ); **chưa skill cũ nào chứng minh được là giúp** |
| Độ dài tám skill cũ sau khi sửa | ít dòng hơn hoặc bằng (769 ⇒ 757 dòng), nhưng nặng hơn khoảng 10 % theo số byte (64.924 ⇒ 71.393 ở bản có file này; bản phiên review đếm lúc giữa chừng là 70.056, +7,9 %) | bản trước khi sửa | [máy kiểm] |
| Hai skill mới, chấm **một** lượt mỗi bên chiều 18/11 | soát tích hợp: 3 / 12 không skill ↔ 10 / 12 có skill — skill đầu tiên thấy khác rõ, nhưng nửa thang chấm đúng hình thức mà skill dạy (ba ý thực chất: 1 / 6 ↔ 4 / 6) · giao việc agent con: 10 ↔ 11 — không khác | "không skill" | [chưa kiểm] — phiên C chấm, chưa có người chấm thứ hai; thang do chính người viết skill soạn |
| Mở phiên phải đọc bao nhiêu | lần mở 13:20 ngày 18/11: mỗi phiên đọc 880–1.400 dòng, dùng tới khoảng 185; khoảng 9 tin chỉ để tìm phiên điều phối | đây là mốc "trước"; cách mới có **một** lần mở (tối 18/11): phiên điều phối không hỏi quyền, phiên E đợi tin rồi trả lời đúng một tin — số dòng đọc lần này chưa đếm | [chưa kiểm] — số của hai phiên B, C; đang thử ở ba lần mở kế |

**3. Chưa làm / giới hạn.** Vòng tự cải thiện cách làm cuối mỗi ngày mới chạy **một** lần (chiều 18/11). Hai con số đo cách làm của tuần 16–22/11, tính tới chiều 18/11: việc báo
xong bị lật lại **5** · số lần anh phải nhắc lại **6** — mới ghi một lần, một phiên khác người đếm đã soát; chưa có tuần trước để so. Nói thẳng: việc sửa tám skill cũ làm **sau** khi chấm, nên điểm của chúng ở bảng trên là của bản cũ; nhóm không sửa thêm chữ skill nào
khi chưa có số chấm mới; buổi thử Codex / Antigravity (nơi chấm lại) nằm trong buổi anh test toàn bộ ở cuối.

**4. Cách thử trong 2 phút.** Ở cửa sổ lệnh: `ls /home/minhhieu/hue_rag/.claude/skills` ⇒ 10 tên, có `soat-tich-hop` và `giao-viec-agent-con`. Lần tới mở một
phiên: nếu nó hỏi anh "quyền phiên" hoặc anh nhận nhiều tin "ai là A?" thì cách mới chưa chạy đúng ⇒ nói với phiên điều phối.

**Đã thử (tối 18/11)** [máy kiểm]: lệnh `ls` in đúng 10 tên, có `soat-tich-hop` và `giao-viec-agent-con`. Lần mở phiên tối 18/11: không ai hỏi quyền phiên; phiên E không
rải tin (phần của các phiên khác người viết dòng này không chứng kiến).

---

<details>
<summary>Nguồn (để giữ file đúng — anh không cần đọc)</summary>

- Mọi mục: sổ việc `session_prompt/CURRENT_HANDOFF.md` khối "PHIÊN SÁNG 18/11" và "PHIÊN CHIỀU 18/11" [tài liệu]; sổ giới hạn `guides/RUNBOOK_BAN_GIAO.md` mục 10.3b [tài liệu].
- Mục 1–3: hồ sơ soát mù ba hãng `data/review_khac_hang/2026-11-18_tich_hop_phase_9/` (riêng tư: `DOI_CHIEU.md`, `duong_cau_bao.md`) [đã chạy — phiên B]; code `backend/llm/assistant.py` (hàm `luoi_cuoi_bao`), `backend/llm/tra_web.py` (danh sách từ thiên tai) [code]; số test phiên review tự chạy: `session_prompt/sessions/STATUS_E.md` các dòng 11:08–12:13 ngày 18/11 [đã chạy — phiên E].
- Mục 4: `backend/api/routes/chat.py` hàm `_doc_git_sha`, test `backend/tests/test_api_chat.py` [code]; sổ tay bàn giao mục 7 và 10.3 [tài liệu].
- Mục 5: `AGENTS.md` bảng "Quyền thường trực"; `skills/`; `session_prompt/START_SESSION.md`; kết quả chấm skill `data/cham_skill_2026-11-18/KET_QUA.md` (riêng tư) [đã chạy — phiên C].
- Các câu ví dụ trong file là câu tự đặt, không lấy từ bộ đo hay sổ ghi debug.
- Các dòng "Đã thử" tối 18/11: phiên E chạy trên server local cổng 8010, bản `fc897ed`, model thật, không phát lại luồng nào; kết quả + 8 ảnh ở `data/thu_viec_moi_xong_2026-11-18/` (riêng tư: `ket_qua.json`, `anh/`, `tools/thu.py`) [đã chạy — phiên E].
- Biên bản kiểm độc lập bản đầu: `data/kiem_bai_hoc_2026-11-18/kiem_viec_moi_xong.md` (riêng tư).
</details>
