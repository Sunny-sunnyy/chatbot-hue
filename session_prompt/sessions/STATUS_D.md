# STATUS D — ghi đè 22:04 22/11/2026 (giờ `date`), phiên D mở lại tối 22/11 sau khi máy khởi động lại 21:25. Vai: phiên giảng, viết giáo trình; làm việc trực tiếp với chủ dự án.

Nhánh `p9-d-giao-trinh`, worktree `/tmp/hr_d_giaotrinh` (mất khi máy khởi động lại ⇒ `git worktree remove --force /tmp/hr_d_giaotrinh; git branch -f p9-d-giao-trinh origin/main; git worktree add /tmp/hr_d_giaotrinh p9-d-giao-trinh; git branch --set-upstream-to=origin/p9-d-giao-trinh p9-d-giao-trinh` — chỉ gỡ bản ghi cây của CHÍNH MÌNH). Terminal phiên này: `hue-rag-62`; phiên điều phối: `hue-rag-ea`.

## 1. Đang dở
KHÔNG có việc viết nào dở, không agent con nào còn chạy. Đợt viết bù tối 22/11 (16 file) ĐÃ GỘP main `d244b4dc`; phiếu nhỏ "mẫu đề bài cho AI khác hãng" (bài 39, 37, một dòng "Có gì mới") đã đẩy lên nhánh, chờ gộp.
Giáo trình `bai_hoc/giao_trinh/` (41 bài + 9 phụ lục + mục lục) đúng với hệ thống lúc **21:45 22/11**: 48 tính năng mở, kho 267 bài / 9.479 đoạn, cả bộ test lần mới nhất 20:48–21:07 — 78 file chạy / 2.197 ca đạt (bài 38); giao diện CŨ (giao diện mới chưa gộp).
Đợt này thêm: hai phép thử làm nhanh tin dài đã đo rồi bỏ (mức suy luận vừa — bài 33 "Đã so"; vế tìm cố định về miễn giảm vé — bài 23 "Đã so" dòng 14; lượt chậm là lượt có lần tìm thứ hai — bài 34) · lệnh thêm vào buổi tối một điểm ban ngày đang có + giới hạn "lịch đã xếp thì gần như không thêm được điểm" kèm lối ra (bài 31) · phép quét trùng chữ lúc lưu code chỉ còn so với câu kín (bài 37, 39) · lần chạy đủ bộ test mới nhất (bài 38, 40).
Mục "Có gì mới" ở đầu `00_GIAO_TRINH.md`: 13 dòng (mới nhất ở trên). Số đếm phụ lục ghi ở mục lục: C 159 · E 211 · F 99 · G 279 · H 144 · I 133 — thêm / bớt dòng phụ lục thì sửa cả ở đó (và bảng đếm cuối phụ lục C: 79 giữ · 69 bỏ · 11 chưa rõ).

## 2. Đã soạn / đã review, chưa gộp
Phiếu "mẫu đề bài cho AI khác hãng" trên `origin/p9-d-giao-trinh`: bài 39 (một câu ở lớp 3 + một gạch "Chi tiết để tra" + dòng Nguồn), bài 37 (một câu), một dòng "Có gì mới". D tự đối chiếu từng câu với `HIEN_TRANG.md` mục 4 và file mẫu (đợt nhỏ, không qua agent kiểm).
Đợt viết bù tối 22/11 đã gộp: qua một agent con kiểm độc lập trên diff — 166 dòng kiểm, 141 đúng, 0 sai, 25 lệch, đã áp cả 25 (`data/hoc_cung_D/kiem/dot_toi_2211_kiem.md` [riêng tư]); phiên điều phối đọc diff và tự mở ba chỗ sửa sau biên bản.

## 3. Việc kế của phiên D (theo thứ tự)
1. **GIAO DIỆN MỚI, hướng "Dòng sông dẫn đường"** (sổ việc X13; lúc ghi sổ CHƯA gộp): viết khi phiên điều phối báo đã gộp + gửi phiếu bốn ý. Sửa bài 5, bài 35, có thể bài 27 / 30, phụ lục G / H / I, một dòng "Có gì mới". Chất liệu: `data/giao_dien_2026-11-22/KIEM_KE.md`, `HUONG_DE_XUAT.md`, `THAM_KHAO.md`, `TUONG_PHAN.md`, ba phiếu chọn hướng, các lỗi bắt được TRƯỚC khi gộp (màn đầu vỡ ở khổ 1280 / 1024 / 768; bản in đổi tỉ lệ; màn đầu không vừa một khung nhìn máy xách tay). Ảnh chụp trong bài 5 (nếu có) phải chụp lại.
2. **Phiếu nhỏ từ nhánh sửa của B** (phát bản đã qua kiểm · chép dấu bão / lũ sang nhánh sửa lịch): viết khi phiên điều phối báo đã vào main + gửi phiếu.
3. Ngày 23/11 chủ dự án tự thử hệ thống: mỗi bản sửa người dùng thấy khác ⇒ phiếu bốn ý ⇒ sửa bài gốc, thêm MỘT dòng "Có gì mới", gom dòng phụ lục liên quan. Có thay đổi về cơ chế thì cho một agent con KHÁC kiểm độc lập trên file diff trước khi đẩy — ba lượt kiểm tối 22/11 đều bắt được lỗi thật (20 / 309 · 19 / 67 · 25 / 166 dòng).

## 4. Ai chờ mình ↔ mình chờ ai
Phiên điều phối chờ: không. D chờ: phiên điều phối gộp nhánh; phiếu "giao diện mới" khi gộp; chủ dự án nói muốn D giảng phần nào (chưa nêu).

## 5. Câu treo (nợ nhẹ, không chặn gì)
- Phụ lục B, F, G, H, I của đợt sửa gom do một agent gom rồi tự soát, CHƯA có người thứ hai đối chiếu (D đếm lại số hàng và dò mẫu); các dòng phụ lục chép từ bài KHÔNG đổi tối 22/11 chưa được dò lại. Hai commit nhỏ (`ec8ca7e`, `73ec0e3`) cũng không qua người thứ hai — chỉ đổi nhãn + chép số D tự đọc.
- Số tiền câu ví dụ: bài 2, 6 ghi 0,0178 USD (lượt ví dụ chính); bài 33 ghi 0,018 cho một lượt khác (chạy thẳng qua code); bài 4, 34 gọi 0,018 là "ví dụ chính" ⇒ mở `report_agent/2026-11-21/b_bedrock_sonnet.md` phân xử rồi sửa bài 4, 33, 34.
- Độ dài nửa để hiểu còn vượt đích 13.000: bài 23 (13.467) · 40 (13.301) · 16 (13.296) · 5 (13.284) · 21 (13.279) · 33 (13.163) · 2 (13.073); bài 6: 18.062 so với trần 18.000. Đo cả bộ bằng lệnh awk thì khoảng 25 bài vượt vài trăm ký tự (bài có mục "Đã so" đứng trước "Cấu hình đang chạy" thì lệnh đếm dư). D tự hoãn: cắt thêm là mất thông tin; chủ dự án thấy bài nào dài thì cắt bài đó.
- Chữ "đứng yên" của dòng trạng thái còn ở bài 16, 21, 34 (thật ra số đoạn trong ngoặc tăng dần — đã sửa ở bài 6, phụ lục G, I); ba câu khó đọc có câu viết lại sẵn ở cuối `data/hoc_cung_D/kiem/dot_gom_2211_kiem.md`.
- Dòng "Cập nhật" của khoảng mười bài còn ghi "khớp hệ thống 16:35 22/11 (47 tính năng…)" — câu có giờ, đúng với lúc bài được soát; lần sửa bài kế thì đổi.
- Thẻ nơi: mới nhìn MỘT lần trên trình duyệt, chưa đo tin nhiều ý kiểu khác, chưa đo model cũ (bài 23 đã ghi).
- Từ trước: 19 chỗ phân xử của commit `be20fa7` mới đọc lướt · chưa ai đọc lại TOÀN VĂN bài 21 và 16 sau các lượt cắt · phụ lục D: hệ thống đổi lời dặn thì chạy lại `cd backend && PYTHONPATH=$PWD uv run --no-sync python ../data/hoc_cung_D/tools/chep_loi_dan.py` (tối 22/11 CHƯA chạy lại — thẻ nơi không đổi lời dặn theo báo cáo của agent viết, nhưng chưa ai so phụ lục D với chương trình sau 15:51).
- Độ dài nửa để hiểu sau đợt tối 22/11 (đo bằng lệnh awk): bài 31: 13.226 · 33: 13.313 · 23: 13.485 · 37: 13.304 · 39: 13.187 · 34: 13.164 — vượt đích 13.000 vài trăm ký tự; D tự hoãn như dòng trên.
- Lời giao chung `data/hoc_cung_D/LOI_GIAO_VIET_BAI.md` còn hai chỗ cũ (mục 4.5 "47 tính năng"; mục 5 "không chép dòng ≥ 40 ký tự của kho") — lời giao đợt (`LOI_GIAO_DOT_TOI_2211.md`) đã ghi đè; sửa file gốc khi dùng lần tới.

## 6. Thứ đang chạy / rác (lúc 22:02 22/11/2026)
- Tiến trình, container, server của D: KHÔNG có. D không bật Qdrant (phiên điều phối bật sau khi máy khởi động lại).
- Worktree của D: chỉ `/tmp/hr_d_giaotrinh [p9-d-giao-trinh]`. File tạm cũ ở `/tmp` đã mất theo máy.
- Agent con đã dùng trong đợt (đều đã xong): hai agent viết (báo cáo `data/hoc_cung_D/viet/dot_toi_v1_harness.md`, `dot_toi_v2_lich_rao_test.md`), một agent kiểm (`data/hoc_cung_D/kiem/dot_toi_2211_kiem.md`, diff đầu vào `dot_toi_2211.diff`).

## 7. Bẫy của phiên (điều phiên sau cần biết)
- **Sổ này ghi trong worktree của nhánh** rồi đẩy; phiên điều phối gộp thì mới lên main. Mở phiên mới: nếu máy chưa khởi động lại thì worktree còn, chỉ cần `git fetch && git merge origin/main`.
- **Sổ tóm (`Y_CHUA_THU.md`, runbook) có thể lệch nguồn gốc:** tối 22/11 ba chỗ (ý 61 "vé gộp chỉ từ 3 điểm"; ý 57 "không phải mức suy luận"; lối ra "bỏ trước rồi thêm" của runbook 10.2) — đã báo phiên điều phối, đã sửa trên main `80bf168c`. Lời giao cho agent viết đừng chép "điều rút ra" từ sổ; chỉ đường tới file đo.
- **Câu "lối ra cho người dùng" phải thử với MỌI nhóm người dùng** (đợt tối 22/11: "điền lại biểu mẫu với kiểu đi nhiều điểm hơn" sai cho nhóm có trẻ em / người lớn tuổi — người kiểm bắt được).
- **Hai lượt kiểm độc lập trước đó đều bắt lỗi do CHÉP TỪ SỔ thay vì từ nguồn gốc:** số "16 lượt" của rào bỏ / thay (bản chấm ghi 12); tráo tên Dục Đức / An Định (file tiêu chí xếp sai thứ tự, bảng gốc đúng); "8 / 9 ⇒ 0 / 12" so hai cách đếm khác nhau; giá vé lẻ "chép từ bài riêng" (thật ra là nguồn riêng mở bài vé). ⇒ con số nào vào bài cũng mở file đo gốc; "trước ⇒ sau" phải cùng một cách đếm; số của MỘT tin thì viết là một tin.
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
8. Từ tối 22/11 (main, commit rào `5047c2c1` + `36f9016f`, chủ dự án chọn 16:44) rào pre-commit THÔI chặn chữ chép từ kho và bộ câu mẫu ⇒ giáo trình trích được ví dụ kho nguyên văn; chữ chỉ có ở câu kín vẫn bị chặn.
9. Hệ thống đổi nhiều lần mỗi buổi ⇒ câu tuyệt đối ("không bao giờ", "luôn") kiểm lại sát giờ đẩy; sau mỗi lượt cập nhật grep các cụm cũ trong cả thư mục.
10. Bài tổng hợp (40, 41) và phụ lục gom dùng ĐÚNG số của bài gốc; hai bài nói khác nhau thì mở nguồn gốc mà phân xử, không tự chọn.

## Ghi chép riêng tư (không commit)
- `data/hoc_cung_D/BAN_VOI_A_VA_D_BEN_KIA.md` — lời chủ dự án (các câu tick 22/11), mọi tin của phiên điều phối kèm số đo, các lượt phản biện về hình thức của một phiên giảng khác.
- `data/hoc_cung_D/LOI_GIAO_DOT_TOI_2211.md` — lời giao của đợt viết bù tối 22/11 (mẫu mới nhất cho đợt "thêm vài sự việc vào đúng bài").
- `data/hoc_cung_D/LOI_GIAO_DOT_GOM_2211.md` — lời giao của đợt sửa gom tối 22/11 (dùng lại làm mẫu cho đợt gom sau); `data/hoc_cung_D/viet/dot_gom_v1.md`, `dot_gom_v2.md`, `dot_gom_v3_phu_luc.md` — báo cáo ba agent sửa; `data/hoc_cung_D/kiem/dot_gom_2211_kiem.md` — biên bản kiểm độc lập (309 dòng mới: 289 đúng, 1 sai, 19 lệch — đã áp).
- `data/hoc_cung_D/viet/*.md` — báo cáo của từng agent viết / chuyển / cập nhật (kể cả `phan_xu_cho_khac_nhau.md`, `cap_nhat_14h47.md`); `data/hoc_cung_D/kiem/*.md` — biên bản đối chiếu; `data/hoc_cung_D/vi_du_*_vet.json` — năm lượt thật làm ví dụ.

## Đang khai báo sửa
- `bai_hoc/giao_trinh/` (chỉ thư mục này) + file này.
