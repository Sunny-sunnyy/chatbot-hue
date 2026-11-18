# Việc mới xong — báo cáo bốn ý (việc mới nhất ở trên)

*Cập nhật lần cuối: 14:06, ngày 18/11/2026 · bản đầu: các việc xong ngày 18/11; đã sửa theo một lượt kiểm độc lập trước khi đưa vào.*

- **File này là gì:** mỗi việc vừa xong mà người dùng trợ lý — hoặc chính anh — thấy khác, nhóm ghi ở đây đúng bốn ý: thấy gì khác · bằng chứng · chưa làm / giới hạn · cách anh thử trong 2 phút. Mục giữ khoảng 2 tuần rồi gỡ (phần đáng giữ lâu đã nằm trong các bài học).
- **Cách đọc:** đọc ý 1 và ý 3 của từng mục là đủ biết hôm đó có gì; ý 2 để biết tin tới đâu; ý 4 làm khi anh rảnh, sau khi bật hệ thống theo sổ tay bàn giao (`guides/RUNBOOK_BAN_GIAO.md`) mục 1–2 rồi mở `http://127.0.0.1:8010/`.
- **Ba nhãn độ tin:** **[máy kiểm]** = có lệnh chạy ra kết quả đó · **[người thứ hai kiểm]** = một phiên khác người viết đã chạy lại hoặc đọc lại · **[chưa kiểm]** = mới là lời của người làm.
- **"Test bằng đồ giả" ↔ "lượt thật":** test bằng đồ giả thay model / dịch vụ ngoài bằng bản dựng sẵn — nhanh, 0 đồng, nhưng chỉ chứng minh phần code quanh model. Lượt thật là hỏi qua hệ thống đang chạy với model thật. Mục nào chỉ có dòng đầu thì ghi rõ là chưa đo trên đường thật.
- **Anh chọn một dòng bất kỳ** trong file này, nhóm chạy lại lệnh của dòng đó trước mặt anh.

---

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
- Chưa chạy lại cả bộ test (để một lượt chung trước tối thứ Bảy 21/11).
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

## 18/11 — 2. Câu an toàn nằm ở đầu khung lịch, in đậm

**1. Người dùng thấy gì khác.** Trước: ở lượt có lịch, mọi ghi chú nằm chung một dòng xám nhạt **dưới** lịch, bản đồ và danh sách nguồn — câu về bão / 112 nếu có thì
phải cuộn hết mới thấy, và câu "thông tin có thể đã thay đổi" ghép liền nên cũng bị đậm theo. Nay: câu an toàn tách riêng, in đậm, nằm **trên** khung lịch; ghi chú
thường để nguyên chữ thường. (Ở lượt trả lời thường, không có lịch, câu an toàn có thêm biểu tượng chữ "i".)

**2. Bằng chứng.** Test bằng đồ giả: hai file test bị chạm, 30 đạt — phiên review tự chạy [máy kiểm]. Ảnh chụp giao diện sau khi build lại: phiên review và phiên
điều phối đã nhìn [người thứ hai kiểm] — nhưng **mọi** ảnh đều là phát lại một luồng đã ghi sẵn hoặc do code dựng, không ảnh nào là một lượt hỏi thật mới sau khi
sửa giao diện [chưa kiểm].

**3. Chưa làm / giới hạn.** Chưa chụp ở màn hình hẹp và ở khung trợ lý nổi (cột lịch của trang Lên kế hoạch đã chụp bằng luồng phát lại: câu an toàn ở đầu cột). Ở lượt trả lời **thường** (không có lịch) mà câu trả
lời dài, câu an toàn vẫn nằm cuối bong bóng, dưới dòng Nguồn. Ở lượt có lịch do model viết lời, câu an toàn hiện lúc kết lượt nên đẩy khung lịch xuống một đoạn.

**4. Cách thử trong 2 phút.** Làm bước (b) của mục 1 và nhìn vị trí: câu đậm phải ở **trên** lịch, không lẫn với dòng "thông tin có thể đã thay đổi". Thu hẹp cửa sổ
trình duyệt xem chữ có vỡ không — chỗ này nhóm chưa kiểm, anh thấy xấu thì chụp lại.

## 18/11 — 3. Mục "Từ web" không tự tóm tắt tin giông, lốc, mưa đá, nước dâng

**1. Người dùng thấy gì khác.** Khi kho không có câu trả lời, trợ lý tra web một lần và viết mục "Từ web — chưa kiểm". Riêng tin thiên tai thì từ đầu tháng 11 đã có
luật bằng code: model **không** được viết tóm tắt, chỉ hiện một câu cố định kèm đường dẫn nguồn (vì từng có lần mục web khẳng định mức lũ có số mét mà không kiểm
được). Danh sách từ của luật đó thiếu bốn từ: giông, lốc, mưa đá, nước dâng — một model hãng khác soát mù đã chỉ ra. Nay bốn từ đã vào danh sách, bằng đúng danh
sách bên công cụ thời tiết.

**2. Bằng chứng.** Test bằng đồ giả: 314 test của các file chạm đạt (số của phiên viết code) [chưa kiểm]; phiên review chạy hai file chính: 153 đạt, 7 lỗi do thư
mục thử của phiên review thiếu dữ liệu riêng, không phải do code [máy kiểm]. Lượt thật: **chưa có** [chưa kiểm] — mục web
chỉ được tra cho câu thiên tai ở hai ca hiếm (lần tìm đầu không ra gì, hoặc câu hai ý có một ý kho thiếu), và chưa bộ đo nào có câu giông / lốc.

**3. Chưa làm / giới hạn.** Bốn từ mới bắt nhầm vài câu không phải thiên tai (hướng chặt hơn — chấp nhận). Cách viết "dông" chưa có trong danh sách của mục web. Câu
hai ý mà một vế có từ thiên tai: vế còn lại cũng không được tra web — biết, sửa sau lượt đo cuối.

**4. Cách thử trong 2 phút.** Gõ một câu **hai ý** tự đặt, trong đó ý kho khó có là chuyện mưa đá, ví dụ *"Lăng Minh Mạng mở cửa mấy giờ, và tuần này Huế có mưa
đá không?"* (câu một ý về mưa đá thì trợ lý trả câu an toàn và không mở mục web, nên không chạm phần vừa sửa). Đúng: có câu chỉ tới bản tin chính thức + 112; nếu
hiện mục "Từ web" thì đó là một câu cố định kèm đường dẫn, **không** có đoạn tóm tắt hay con số. Thấy mục web kể chi tiết thiệt hại / số liệu ⇒ báo nhóm.
[chưa ai chạy thử đúng câu ví dụ này]

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
| Mở phiên phải đọc bao nhiêu | lần mở 13:20 ngày 18/11: mỗi phiên đọc 880–1.400 dòng, dùng tới khoảng 185; khoảng 9 tin chỉ để tìm phiên điều phối | đây là mốc "trước"; cách mới **chưa có lần mở nào** | [chưa kiểm] — số của hai phiên B, C; đang thử ở ba lần mở kế |

**3. Chưa làm / giới hạn.** Vòng tự cải thiện cách làm cuối mỗi ngày chưa chạy lần nào. Hai con số đo cách làm (việc báo xong bị lật lại · số lần anh phải nhắc lại)
mới ghi một lần, chưa ai soát. Nói thẳng: việc sửa tám skill cũ làm **sau** khi chấm, nên điểm của chúng ở bảng trên là của bản cũ; nhóm không sửa thêm chữ skill nào
trước buổi thử Codex / Antigravity tối thứ Ba 24/11, và chấm lại ở buổi đó.

**4. Cách thử trong 2 phút.** Ở cửa sổ lệnh: `ls /home/minhhieu/hue_rag/.claude/skills` ⇒ 10 tên, có `soat-tich-hop` và `giao-viec-agent-con`. Lần tới mở một
phiên: nếu nó hỏi anh "quyền phiên" hoặc anh nhận nhiều tin "ai là A?" thì cách mới chưa chạy đúng ⇒ nói với phiên điều phối.

---

<details>
<summary>Nguồn (để giữ file đúng — anh không cần đọc)</summary>

- Mọi mục: sổ việc `session_prompt/CURRENT_HANDOFF.md` khối "PHIÊN SÁNG 18/11" và "PHIÊN CHIỀU 18/11" [tài liệu]; sổ giới hạn `guides/RUNBOOK_BAN_GIAO.md` mục 10.3b [tài liệu].
- Mục 1–3: hồ sơ soát mù ba hãng `data/review_khac_hang/2026-11-18_tich_hop_phase_9/` (riêng tư: `DOI_CHIEU.md`, `duong_cau_bao.md`) [đã chạy — phiên B]; code `backend/llm/assistant.py` (hàm `luoi_cuoi_bao`), `backend/llm/tra_web.py` (danh sách từ thiên tai) [code]; số test phiên review tự chạy: `session_prompt/sessions/STATUS_E.md` các dòng 11:08–12:13 ngày 18/11 [đã chạy — phiên E].
- Mục 4: `backend/api/routes/chat.py` hàm `_doc_git_sha`, test `backend/tests/test_api_chat.py` [code]; sổ tay bàn giao mục 7 và 10.3 [tài liệu].
- Mục 5: `AGENTS.md` bảng "Quyền thường trực"; `skills/`; `session_prompt/START_SESSION.md`; kết quả chấm skill `data/cham_skill_2026-11-18/KET_QUA.md` (riêng tư) [đã chạy — phiên C].
- Các câu ví dụ trong file là câu tự đặt, không lấy từ bộ đo hay sổ ghi debug.
- Biên bản kiểm độc lập bản đầu: `data/kiem_bai_hoc_2026-11-18/kiem_viec_moi_xong.md` (riêng tư).
</details>
