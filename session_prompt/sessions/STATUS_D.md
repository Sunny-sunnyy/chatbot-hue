# STATUS D — ghi đè 18:13 22/11/2026 (giờ `date`), sau đợt sửa gom tối 22/11 (đã gộp main), commit thứ hai cho hai phiếu của phiên điều phối (đã gộp), và commit thứ ba cho tính năng thứ 48 "thẻ nơi". Vai: phiên giảng, viết giáo trình; làm việc trực tiếp với chủ dự án.

Nhánh `p9-d-giao-trinh`, worktree `/tmp/hr_d_giaotrinh` (mất khi máy khởi động lại ⇒ `git worktree add /tmp/hr_d_giaotrinh origin/p9-d-giao-trinh` rồi `git merge origin/main`). Phiên điều phối tối 22/11: terminal `hue-rag-5a` (phiên mới sẽ có tên khác — xem `ListAgents`).

## Giáo trình đang ở đâu
- `bai_hoc/giao_trinh/`: **đủ 41 bài + 9 phụ lục (A–I)** + mục lục `00_GIAO_TRINH.md`. Khuôn bài không đổi (bài mẫu `06_KIEN_TRUC.md`; bài 41 cấu trúc riêng).
- Giáo trình nay đúng với hệ thống lúc **18:13 22/11**: 48 tính năng mở (cái thứ 47: nhớ câu trả lời liền trước cả trong cuộc đã lập lịch; cái thứ 48, mở 17:15: "thẻ nơi" — bài 23 là bài chính); kho 267 bài / 9.479 đoạn / 5.960 từ (có bài đường đi Hội An; đã sửa dòng tự mâu thuẫn về Hải Vân Quan); giữ chữ đã nhìn trên trình duyệt ở lượt thường; trang Giới thiệu đã sửa trong mã nguồn (main `49bff6d2`), CHƯA dựng lại giao diện, chưa ai nhìn.
- **Mục "Có gì mới" ở đầu `00_GIAO_TRINH.md`** (chủ dự án 16:28 22/11: việc mới chỉ ghi vào giáo trình): bảng ngày · người dùng thấy gì khác · đọc ở bài nào, mục nào; mới nhất ở trên; đang có 8 dòng. Mỗi phiếu bốn ý của phiên điều phối ⇒ sửa bài gốc, thêm MỘT dòng ở đây, gom lại dòng phụ lục liên quan.
- Phụ lục G, H, C, E, F, I là GOM từ các bài ⇒ bài gốc đổi thì gom lại dòng liên quan. Số đếm ghi ở mục lục: C 156 · E 211 · F 95 · G 279 (tám bảng theo chặng) · H 142 · I 130 — thêm / bớt dòng thì sửa cả ở `00_GIAO_TRINH.md`.

## CÒN NỢ
1. **Chờ tin phiên điều phối:** (a) phiên đo dựng lại giao diện và nhìn trang Giới thiệu ⇒ đổi nhãn ở bài 37 gạch "Trang Giới thiệu vừa được sửa…" và dòng tương ứng ở phụ lục I; phiên C đang soát thêm dòng "Chưa có lịch sự kiện theo ngày" ở mục Giới hạn của trang đó. (b) thẻ nơi ĐÃ vào giáo trình (phiếu của phiên B 17:2x; agent viết + agent kiểm độc lập: 67 dòng mới, 48 đúng, 2 sai, 17 lệch — đã áp; biên bản `data/hoc_cung_D/kiem/the_noi_2211_kiem.md`, báo cáo `data/hoc_cung_D/viet/the_noi_v4.md`); còn: thẻ nơi chưa có lượt nào trên trình duyệt và chưa đo tin nhiều ý kiểu khác ⇒ có kết quả thì đổi nhãn ở bài 23 dòng 13 "Đã so" + "Giới hạn". Dòng "Cập nhật" của khoảng mười bài còn ghi "khớp hệ thống 16:35 22/11 (47 tính năng…)" — đó là câu có ngày giờ, đúng với lúc bài được soát; lần sửa bài kế thì đổi. (c) ngày 23/11 chủ dự án tự thử hệ thống ⇒ mỗi bản sửa người dùng thấy khác đều đi theo phiếu bốn ý.
2. **Độ dài nửa để hiểu:** đợt này rút chín bài theo biên bản; bảy bài còn vượt đích 13.000 dưới 300 ký tự (bài 2: 13.073 · 5: 13.284 · 16: 13.296 · 21: 13.279 · 23: 13.467 sau khi thêm thẻ nơi và các câu sửa của lượt kiểm · 33: 13.163 · 40: 13.301 sau thẻ nơi; bài 6: 18.062 so với trần 18.000). Phép đo cả bộ cho thấy khoảng 25 bài vượt 13.000 vài trăm ký tự (lệnh awk dừng ở "Cấu hình đang chạy" / "Chi tiết để tra"; bài có mục "Đã so" đứng trước thì bị đếm dư). D tự hoãn: cắt thêm là mất thông tin; chủ dự án đọc thấy bài nào dài thì cắt bài đó.
3. **Phụ lục chưa được người thứ hai đối chiếu ở đợt này** (agent gom tự soát grep; D đếm lại số hàng F, H, I và dò mẫu). Agent gom nêu: (a) số 0,018 USD — bài 2, 6 ghi 0,0178 cho lượt ví dụ chính, bài 33 ghi 0,018 cho một lượt khác (chạy thẳng qua code), bài 4, 34 gọi 0,018 là "ví dụ chính" ⇒ cần mở `report_agent/2026-11-21/b_bedrock_sonnet.md` phân xử rồi sửa bài 4, 33, 34 cho khít; (b) các dòng phụ lục chép từ bài KHÔNG đổi trong đợt này chưa được dò lại.
4. Chỗ biên bản kiểm nêu mà chưa sửa (nhẹ): chữ "đứng yên" của dòng trạng thái còn ở bài 16, 21, 34 phần Nguồn / Giới hạn (thật ra số đoạn trong ngoặc tăng dần — đã sửa ở bài 6, phụ lục G, I); ba câu khó đọc có câu viết lại sẵn ở cuối biên bản `data/hoc_cung_D/kiem/dot_gom_2211_kiem.md`; bài 31 dòng 42 không còn ghi ai chạy năm câu ví dụ (vẫn có ở khối Nguồn).
5. Việc nhỏ còn lại từ trước: 19 chỗ phân xử của commit `be20fa7` mới đọc lướt · chưa ai đọc lại TOÀN VĂN bài 21 và 16 sau các lượt cắt · phụ lục D: hệ thống đổi lời dặn thì chạy lại `cd backend && PYTHONPATH=$PWD uv run --no-sync python ../data/hoc_cung_D/tools/chep_loi_dan.py`.
6. Chủ dự án CHƯA nhận xét bài nào ngoài bài 6.

## Đợt sửa gom tối 22/11 đã làm gì (để phiên sau khỏi làm lại)
- Số kho đổi bằng `data/hoc_cung_D/tools/doi_so_kho.py` (danh sách dòng lịch sử được giữ đã thêm ba mục) + sửa tay bảng theo thư mục của bài 7 (Du lịch 62, dịch vụ 12), từ điển 5.960, độ dài trung bình 66,59 — đọc từ bản ghi chỉ mục 16:35.
- Ba agent sửa (hai nhóm bài song song, rồi phụ lục) + một agent kiểm độc lập trên file diff; D tự mở nguồn phân xử: số lượt thật của rào bỏ / thay là 12 (bản chấm của phiên đo + runbook), không phải 16 như mục 44 bộ cũ.
- Commit thứ hai (hai phiếu 17:1x): "gõ lại đúng câu cũ" vào bài 34 (Giới hạn, câu tự kiểm, Nguồn) + phụ lục I; mục "Giới hạn" của trang Giới thiệu vào bài 37; các thứ lần đầu được nhìn trên giao diện tối 22/11 (ảnh, sự kiện theo ngày, đổi chỗ ngày, bốn lệnh dời) thành một gạch ở "Chi tiết để tra" của bài 26, 24, 31 — nguồn `data/test_cuoi/chay_2026-11-22_e_sau_dong/KET_QUA.md`.
- Hai phiếu của phiên điều phối đã vào bài: Hải Vân Quan (bài 7, 24, phụ lục I), trang Giới thiệu (bài 37, phụ lục I); thêm dòng "câu ngoài tỉnh về Hội An vẫn bị từ chối đúng" ở bài 22.

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
