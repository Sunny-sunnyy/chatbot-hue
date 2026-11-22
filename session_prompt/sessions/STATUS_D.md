# STATUS D — ghi đè 20:31 22/11/2026 (giờ `date`), KẾT PHIÊN NHẸ (chủ dự án tắt rồi mở lại cả năm phiên sau cổng gộp giao diện mới). Vai: phiên giảng, viết giáo trình; làm việc trực tiếp với chủ dự án.

Nhánh `p9-d-giao-trinh`, worktree `/tmp/hr_d_giaotrinh` (mất khi máy khởi động lại ⇒ `git worktree add /tmp/hr_d_giaotrinh origin/p9-d-giao-trinh` rồi `git merge origin/main`). Phiên điều phối tối 22/11: terminal `hue-rag-5a` (phiên mới sẽ có tên khác — đợi tin mở phiên của phiên điều phối, hoặc `ListAgents`).

## 1. Đang dở
KHÔNG có việc viết nào dở, không agent con nào còn chạy. Bốn commit tối 22/11 đều ĐÃ GỘP main (`98ec1b1` đợt sửa gom · `ec8ca7e` hai phiếu · `774f451` thẻ nơi · `73ec0e3` kết quả cổng tối); lúc ghi sổ này nhánh trùng main `e42ef3f2`.
Giáo trình `bai_hoc/giao_trinh/` (41 bài + 9 phụ lục + mục lục) đúng với hệ thống lúc **18:17 22/11**: 48 tính năng mở (thứ 47: nhớ câu trả lời liền trước cả trong cuộc đã lập lịch; thứ 48: thẻ nơi — bài 23 là bài chính), kho 267 bài / 9.479 đoạn / 5.960 từ, cả bộ test 78 file chạy / 2.196 ca đạt (bài 38). Đếm lại lúc 20:31 trên main: vẫn 48 tính năng, Qdrant 9.479 điểm.
Mục "Có gì mới" ở đầu `00_GIAO_TRINH.md`: 8 dòng (mới nhất ở trên; mỗi dòng: ngày · người dùng thấy gì khác · bài + mục). Số đếm phụ lục ghi ở mục lục: C 156 · E 211 · F 96 · G 279 (tám bảng theo chặng) · H 142 · I 130 — thêm / bớt dòng phụ lục thì sửa cả ở đó.

## 2. Đã soạn / đã review, chưa gộp
Không có.

## 3. Việc đầu của phiên D mới (theo thứ tự; mỗi thứ đi theo cách làm ở mục "Cách làm đã dùng")
Phiên điều phối nhắn tối 22/11 (sau 20 giờ): bốn thứ dưới CHƯA có trong giáo trình. Viết khi phiên điều phối báo đã gộp + gửi phiếu bốn ý (thấy gì khác · bằng chứng + đường dẫn · giới hạn · cách thử 2 phút); thứ đã ở main thì viết ngay.
1. **GIAO DIỆN MỚI, hướng "Dòng sông dẫn đường"** (sổ việc X13; lúc ghi sổ CHƯA gộp — cổng gộp đang chạy). Khi gộp: sửa bài 5 (người dùng thấy gì), bài 35 (trang web và máy chủ), có thể bài 27 / 30 (trang Lên kế hoạch, bản in), phụ lục G / H / I, một dòng "Có gì mới". Chất liệu để giảng "vì sao chọn, cách khác, cái giá, hỏng thì sao" đã có: `data/giao_dien_2026-11-22/KIEM_KE.md`, `HUONG_DE_XUAT.md` (ba hướng), `THAM_KHAO.md`, `TUONG_PHAN.md`, ba phiếu chọn hướng, và hai lỗi bắt được TRƯỚC khi gộp (màn đầu vỡ ở khổ 1280 / 1024 / 768; bản in đổi tỉ lệ vì thanh menu ngắn lại). Ảnh chụp màn hình trong bài 5 (nếu có) phải chụp lại.
2. **Hai phép thử harness đo rồi BỎ theo tiêu chí ghi trước** (hạ mức suy luận; thêm vế miễn giảm vào lần tìm đầu) + bài học "tin dài chậm do lần tìm thứ hai": `session_prompt/Y_CHUA_THU.md` ý 56, 57, 61 ⇒ bài 21 "Đã so" (kể cả phương án bị bỏ), bài 33 / 34 nếu chạm mức suy luận và thời gian chờ, phụ lục C (sổ phép so, đếm lại số 156), G.
3. **Sửa lỗi "thêm vào buổi tối một điểm đã có ⇒ đã có trong lịch"** (main `dcd9ecdb`) + giới hạn "sau khi lịch đã xếp gần như không thêm được điểm": `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 ⇒ bài 31 (bảng lệnh, "Nếu… thì sao", Giới hạn), phụ lục H, I.
4. **Bộ kiểm lúc lưu code chỉ còn chặn chữ câu kín** (main từ khoảng 17 giờ, chủ dự án chọn 16:44) ⇒ bài 39 (đồ án được làm thế nào) và bài 37 nếu có câu nói rào chặn chữ chép từ kho / bộ câu mẫu; grep "40 ký tự" trong cả bộ (bài 39 dòng Nguồn có nhắc).
5. Ngày 23/11 chủ dự án tự thử hệ thống: mỗi bản sửa người dùng thấy khác ⇒ phiếu bốn ý ⇒ sửa bài gốc, thêm MỘT dòng "Có gì mới", gom dòng phụ lục liên quan. Có thay đổi về cơ chế (không chỉ đổi số / nhãn) thì cho một agent con KHÁC kiểm độc lập trên file diff trước khi đẩy — hai lượt kiểm tối 22/11 đều bắt được lỗi thật (20 / 309 và 19 / 67 dòng).

## 4. Ai chờ mình ↔ mình chờ ai
Không ai chờ D. D chờ: tin "đã gộp giao diện mới" + phiếu của phiên điều phối; chủ dự án nói muốn D giảng phần nào (chưa nêu; anh ấy chưa nhận xét bài nào ngoài bài 6).

## 5. Câu treo (nợ nhẹ, không chặn gì)
- Phụ lục B, F, G, H, I của đợt sửa gom do một agent gom rồi tự soát, CHƯA có người thứ hai đối chiếu (D đếm lại số hàng và dò mẫu); các dòng phụ lục chép từ bài KHÔNG đổi tối 22/11 chưa được dò lại. Hai commit nhỏ (`ec8ca7e`, `73ec0e3`) cũng không qua người thứ hai — chỉ đổi nhãn + chép số D tự đọc.
- Số tiền câu ví dụ: bài 2, 6 ghi 0,0178 USD (lượt ví dụ chính); bài 33 ghi 0,018 cho một lượt khác (chạy thẳng qua code); bài 4, 34 gọi 0,018 là "ví dụ chính" ⇒ mở `report_agent/2026-11-21/b_bedrock_sonnet.md` phân xử rồi sửa bài 4, 33, 34.
- Độ dài nửa để hiểu còn vượt đích 13.000: bài 23 (13.467) · 40 (13.301) · 16 (13.296) · 5 (13.284) · 21 (13.279) · 33 (13.163) · 2 (13.073); bài 6: 18.062 so với trần 18.000. Đo cả bộ bằng lệnh awk thì khoảng 25 bài vượt vài trăm ký tự (bài có mục "Đã so" đứng trước "Cấu hình đang chạy" thì lệnh đếm dư). D tự hoãn: cắt thêm là mất thông tin; chủ dự án thấy bài nào dài thì cắt bài đó.
- Chữ "đứng yên" của dòng trạng thái còn ở bài 16, 21, 34 (thật ra số đoạn trong ngoặc tăng dần — đã sửa ở bài 6, phụ lục G, I); ba câu khó đọc có câu viết lại sẵn ở cuối `data/hoc_cung_D/kiem/dot_gom_2211_kiem.md`.
- Dòng "Cập nhật" của khoảng mười bài còn ghi "khớp hệ thống 16:35 22/11 (47 tính năng…)" — câu có giờ, đúng với lúc bài được soát; lần sửa bài kế thì đổi.
- Thẻ nơi: mới nhìn MỘT lần trên trình duyệt, chưa đo tin nhiều ý kiểu khác, chưa đo model cũ (bài 23 đã ghi).
- Từ trước: 19 chỗ phân xử của commit `be20fa7` mới đọc lướt · chưa ai đọc lại TOÀN VĂN bài 21 và 16 sau các lượt cắt · phụ lục D: hệ thống đổi lời dặn thì chạy lại `cd backend && PYTHONPATH=$PWD uv run --no-sync python ../data/hoc_cung_D/tools/chep_loi_dan.py` (tối 22/11 CHƯA chạy lại — thẻ nơi không đổi lời dặn theo báo cáo của agent viết, nhưng chưa ai so phụ lục D với chương trình sau 15:51).

## 6. Thứ đang chạy / rác (lúc 20:31 22/11/2026)
- Tiến trình, container, server của D: KHÔNG có. Cổng 8012 đang mở là của phiên khác (không phải D).
- `git worktree list`: D chỉ có `/tmp/hr_d_giaotrinh  e42ef3f2 [p9-d-giao-trinh]` (các cây `/tmp/hr_b_*`, `/tmp/hr_c_*`, `/tmp/hr_e_*` là của phiên khác).
- File tạm của D: `/tmp/hr_d_pl_scratch/` (các script sửa một lần của tối 22/11: `sua_tay_1.py`, `sua_00.py`, `sua_x11.py`, `ap_kiem.py`, `phieu_2.py`, `ap_kiem_the_noi.py`, `cong_toi.py` — mẫu cho cách "thay đúng một chỗ, không khớp thì báo"; xoá được), `/tmp/hr_d_agent_tools/`, `/tmp/hr_d_giaotrinh_move.py` (của phiên D trước; không dùng tối nay).

## 7. Bẫy của phiên (điều phiên sau cần biết)
- **Sổ này ghi trong worktree của nhánh** rồi đẩy; phiên điều phối gộp thì mới lên main. Mở phiên mới: nếu máy chưa khởi động lại thì worktree còn, chỉ cần `git fetch && git merge origin/main`.
- **Hai lượt kiểm độc lập đều bắt lỗi do CHÉP TỪ SỔ thay vì từ nguồn gốc:** số "16 lượt" của rào bỏ / thay (bản chấm ghi 12); tráo tên Dục Đức / An Định (file tiêu chí xếp sai thứ tự, bảng gốc đúng); "8 / 9 ⇒ 0 / 12" so hai cách đếm khác nhau; giá vé lẻ "chép từ bài riêng" (thật ra là nguồn riêng mở bài vé). ⇒ con số nào vào bài cũng mở file đo gốc; "trước ⇒ sau" phải cùng một cách đếm; số của MỘT tin thì viết là một tin.
- **Nhãn "đã nhìn trên trình duyệt" gắn theo CA**, không theo tính năng: giữ chữ đã nhìn ở lượt thường, ca "chữ giữ chỗ ⇒ viết lại" và ca bị rút vẫn chưa.
- **`date` chứ không ước:** tối nay D từng ghi một giờ ước vào file riêng tư rồi phải sửa; rào commit cảnh báo (không chặn) chữ kiểu "17:1x".
- `grep -o` với khoảng `.\{0,200\}` trên dòng tiếng Việt dài báo lỗi "exceeds complexity limits" ⇒ in cửa sổ quanh một chuỗi bằng một đoạn python ngắn.
- Số dòng trong `guides/RUNBOOK_BAN_GIAO.md` trôi mỗi lần thêm hàng ⇒ khối Nguồn trỏ "mục 10.x hàng '<tên>'", không trỏ số dòng.
- Agent con sửa bài: mỗi lúc nhiều nhất hai, chia theo FILE (không theo việc) để không sửa chồng; D không đụng file agent đang giữ cho tới khi nó báo xong.
- Lệnh đẩy: `scripts/commit_push.sh "<lời>" <file…>` chạy TRONG worktree; trước đó `git add <file> && .githooks/pre-commit; git reset -q` để xem rào.

## Cách làm đã dùng (giữ nguyên)
- Chủ dự án: quen phần AI; gần như chưa biết giao diện web, máy chủ, API, cơ sở dữ liệu ⇒ giảng các khái niệm đó từ đầu. Anh ấy muốn được HỎI trong lúc làm (mỗi lần một câu có ô tick), không muốn D cắm đầu viết. Yêu cầu gốc: đọc xong phải GIẢI THÍCH được từng quyết định và "hỏng thì sao"; chỉ viết thứ hệ thống thật có; giọng giáo trình dễ hiểu; đủ quan trọng hơn ngắn nhưng không lặp.
- Viết / chuyển / cập nhật bằng agent con theo `data/hoc_cung_D/LOI_GIAO_VIET_BAI.md`; MỖI nhóm bài sau đó qua một agent con KHÁC đối chiếu theo `data/hoc_cung_D/LOI_GIAO_KIEM_BAI.md` (biên bản ở `data/hoc_cung_D/kiem/`), rồi agent viết áp biên bản, D soát grep + rào, đẩy, nhắn phiên điều phối gộp. Mỗi lúc nhiều nhất HAI agent con; agent con không commit.
- Mỗi lần đẩy: `git fetch && git merge origin/main`, đóng giờ `date` vào dòng 3 của bài, `git add <file> && .githooks/pre-commit; git reset -q`, `scripts/commit_push.sh "<lời>" <file…>`.
- Công cụ riêng tư ở `data/hoc_cung_D/tools/`: `sua.py` (sửa nhiều chỗ, báo chỗ không khớp), `thay_khoi.py`, `chen_muc.py`, `doi_so_kho.py`, `chep_loi_dan.py`, `vet_tim.py`.

## Luật viết đã rút ra (đọc trước khi sửa bài)
1. "Kho không có" phải dò bằng `scripts/grep_kb.sh` trước khi dùng làm ví dụ.
2. Đọc cả lớp gọi (route chat đường gửi dần, giao diện, lệnh chạy tay), không chỉ hàm lõi; phân biệt "lỗi lúc bật máy chủ" với "lỗi giữa lúc chạy", "hạn giờ một lần gọi" với "hạn chung cả lượt".
3. Mỗi gạch "Ý chính" phải đứng được trước MỌI dòng bảng của chính bài.
4. Câu chuẩn (đúng lúc 17:10 22/11; thêm: "47 tính năng đang mở (đếm 16:13 22/11)" · "từ 16:08 22/11, trong cuộc đã lập lịch câu hỏi thường cũng được nhớ câu trả lời liền trước và lượt bị rút được chạy lại một lần; không nhớ / không chạy lại: lượt thật sự sửa lịch, câu trả lời trích nguồn của lịch" · nhãn giữ chữ: "lượt thường đã nhìn trên trình duyệt 22/11; ca chữ giữ chỗ ⇒ viết lại và ca bị rút: theo chương trình và test, chưa nhìn"): "10 đoạn ở lần tìm đầu; trợ lý được tìm thêm tối đa 3 lần; tin nhiều ý được nối thêm 2 đoạn mỗi ý" · "model đang chạy: lượt có công cụ giữ chữ tới khi qua kiểm nguồn; model trả chữ dần: hiện trước, kiểm sau, hỏng thì rút lại" · kho lệch chỉ mục: "máy chủ vẫn chạy, mọi câu hỏi nhận lời báo" (phép so chỉ chạy lúc bật).
5. Mỗi con số ghi model, bộ câu, ngày; số đo cũ giữ nguyên kèm "lúc đó…"; phép đo gộp thì nói là gộp.
6. Không tra ra lý do ⇒ "chưa thấy ghi lý do. Điều thấy được: …" (không đoán); "chủ dự án đã quyết" chỉ khi hồ sơ ghi lời chủ dự án; "cách khác" phải là cách khác của đúng câu hỏi đó; trước khi viết "chưa thử" phải grep cả `docs/superpowers/plans/`.
7. Lời báo trong ngoặc kép chỉ khi chép từng chữ từ code; ca hỏng chưa ai thử ghi "đọc từ chương trình".
8. Từ tối 22/11 (main `2fc5c3fb`, chủ dự án chọn 16:44) rào pre-commit THÔI chặn chữ chép từ kho và bộ câu mẫu ⇒ giáo trình trích được ví dụ kho nguyên văn; chữ chỉ có ở câu kín vẫn bị chặn.
9. Hệ thống đổi nhiều lần mỗi buổi ⇒ câu tuyệt đối ("không bao giờ", "luôn") kiểm lại sát giờ đẩy; sau mỗi lượt cập nhật grep các cụm cũ trong cả thư mục.
10. Bài tổng hợp (40, 41) và phụ lục gom dùng ĐÚNG số của bài gốc; hai bài nói khác nhau thì mở nguồn gốc mà phân xử, không tự chọn.

## Ghi chép riêng tư (không commit)
- `data/hoc_cung_D/BAN_VOI_A_VA_D_BEN_KIA.md` — lời chủ dự án (các câu tick 22/11), mọi tin của phiên điều phối kèm số đo, các lượt phản biện về hình thức của một phiên giảng khác.
- `data/hoc_cung_D/LOI_GIAO_DOT_GOM_2211.md` — lời giao của đợt sửa gom tối 22/11 (dùng lại làm mẫu cho đợt gom sau); `data/hoc_cung_D/viet/dot_gom_v1.md`, `dot_gom_v2.md`, `dot_gom_v3_phu_luc.md` — báo cáo ba agent sửa; `data/hoc_cung_D/kiem/dot_gom_2211_kiem.md` — biên bản kiểm độc lập (309 dòng mới: 289 đúng, 1 sai, 19 lệch — đã áp).
- `data/hoc_cung_D/viet/*.md` — báo cáo của từng agent viết / chuyển / cập nhật (kể cả `phan_xu_cho_khac_nhau.md`, `cap_nhat_14h47.md`); `data/hoc_cung_D/kiem/*.md` — biên bản đối chiếu; `data/hoc_cung_D/vi_du_*_vet.json` — năm lượt thật làm ví dụ.

## Đang khai báo sửa
- `bai_hoc/giao_trinh/` (chỉ thư mục này) + file này.
