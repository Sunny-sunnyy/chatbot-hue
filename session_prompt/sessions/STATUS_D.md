# STATUS D — ghi đè 16:26 22/11/2026 (giờ `date`), lúc KẾT PHIÊN. Vai: phiên giảng, viết giáo trình; làm việc trực tiếp với chủ dự án.

Nhánh `p9-d-giao-trinh`, worktree `/tmp/hr_d_giaotrinh` (mất khi máy khởi động lại ⇒ `git worktree add /tmp/hr_d_giaotrinh origin/p9-d-giao-trinh` rồi `git merge origin/main`). Phiên điều phối lúc kết phiên: terminal `hue-rag-fc` (phiên mới sẽ có tên khác — xem `ListAgents`).

## Giáo trình đang ở đâu
- `bai_hoc/giao_trinh/` trên main: **ĐỦ 41 bài + 9 phụ lục (A–I)** + mục lục `00_GIAO_TRINH.md`. Commit cuối đã gộp: `be20fa7`.
- Bài 1–40 cùng MỘT khuôn (bài mẫu `06_KIEN_TRUC.md`, chủ dự án đọc và duyệt trưa 22/11, rồi duyệt rút gọn "ngắn hơn nhưng vẫn chứa đầy đủ thông tin"): Ý chính · Từ dùng · thân bài · "Quyết định và lý do" (`### n. Vì sao…?` + bốn gạch Đã chọn / Vì sao / Cách khác / Cái giá) · "Nếu… thì sao" (≤ 6 dòng) · Dễ nhầm (≤ 3) · Câu hỏi tự kiểm (~4 câu, `<details>`) · nửa để tra (Cấu hình, Đã so, Quyết định nhỏ hơn, Giới hạn, Chi tiết, Nguồn). KHÔNG còn mục "Những điều cần nhớ" và "Vì sao không làm cách khác". Bài 41 có cấu trúc riêng (kể 1 phút, 5 phút, kịch bản chạy thử, 10 câu hỏi).
- Phụ lục: A tham số · B tính năng (bài nào giảng) · C sổ phép so · D lời dặn nguyên văn (chép bằng script) · E thuật ngữ · F con số chính · G mọi quyết định · H mọi tình huống hỏng · I mọi giới hạn. G, H, C, E, F, I là GOM từ các bài ⇒ bài gốc đổi thì phải gom lại dòng liên quan.
- Giáo trình hiện đúng với hệ thống lúc **15:51 22/11** (46 tính năng mở; 266 bài / 9.458 đoạn; trần tìm thêm 3 lần, trần 5 vòng; model đang chạy giữ chữ tới khi qua kiểm nguồn; rào lệnh bỏ / thay của lịch).

## CÒN NỢ — làm ngay đầu phiên mới, gom MỘT đợt sửa
1. **47 tính năng mở từ 16:13** (main `2a221e5`): `nho_dap_cuoc_co_lich` — trong cuộc đã lập lịch, câu hỏi thường cũng được nhớ câu trả lời liền trước (lượt thật 9 lượt; bốn dòng giới hạn ở `guides/RUNBOOK_BAN_GIAO.md` mục 10.2). ⇒ giới hạn "cuộc có lịch không nhớ câu trả lời liền trước" ở bài 23, 16, 31, 40 và phụ lục H, I nay CŨ; số "46" ở bài 4, 40, phụ lục B, F; thêm một hàng ở phụ lục B.
2. **Kho 267 bài / 9.479 đoạn** (bài "Đi từ Huế tới Hội An", chủ dự án duyệt 16:07, vào chỉ mục 16:15; phiên điều phối đã xác nhận). Khoảng 23 file có "266 bài" hoặc "9.458": đổi bằng `data/hoc_cung_D/tools/doi_so_kho.py <thư mục> 'cũ=mới' …`; ngoài ra phải ĐẾM LẠI bảng số bài theo thư mục (bài 7), số từ vựng và độ dài trung bình (bài 11, phụ lục A, F); sửa câu "kho thiếu đường từ Huế đi Hội An" (bài 4, 7, 40).
3. **Đổi nhãn phần giữ chữ**: các bài đang ghi "theo test và một lượt thật; chưa nhìn trên trình duyệt" (bài 5, 6, 16, 21, 23, 34, phụ lục H…). Kết quả nhìn trình duyệt 16:21 22/11 (phiên đo; tóm tắt ở `bai_hoc/VIEC_MOI_XONG.md` mục 44, main `91844a9`): một lượt thường của tin dài — từ 0,8 tới 29,5 giây chỉ có một dòng "Đã tìm trong kho, đang chuẩn bị câu trả lời…", rồi cả câu trả lời hiện một lần, không chữ nào hiện rồi bị thay; dòng "Đang viết câu trả lời…" gần như không còn hiện. CHƯA trúng trên trình duyệt: ca "bản đầu là chữ giữ chỗ ⇒ viết lại" (mới một lượt thật qua chương trình). Rào bỏ / thay của lịch cũng đã nhìn: một cuộc sáu tin, lịch đổi / đứng yên đúng cả sáu ⇒ bài 31 đổi nhãn.
4. **Kiểm chéo commit `be20fa7`** (phân xử 33 chỗ hai bài nói khác nhau + cập nhật 15:42 + rào sửa lịch): lúc kết phiên một agent con ĐANG chạy, biên bản sẽ ở `data/hoc_cung_D/kiem/phan_xu_va_cap_nhat_15h42.md` (riêng tư). Nếu file đó chưa có hoặc dở ⇒ giao lại một agent ngữ cảnh mới theo `data/hoc_cung_D/LOI_GIAO_KIEM_BAI.md`: xem `git diff 6d6792c be20fa7 -- bai_hoc/giao_trinh/`; ưu tiên bài 6 (quyết định 4 viết lại hai giai đoạn), bài 31, 16, 21, 5; lấy mẫu ≥ 12 chỗ trong `data/hoc_cung_D/viet/phan_xu_cho_khac_nhau.md`. Rồi áp, đẩy. Phiên điều phối chỉ đọc kỹ phần bài 31 của commit đó.
5. **Độ dài nửa để hiểu đang vượt** (đích 13.000 ký tự; bài 6: 18.000): bài 6 (18.440), 5 (13.981), 33 (13.943), 16 (13.546), 2 (13.538), 21 (~13.540), 40 (13.497), 23 (~13.440). Cắt bằng cách chuyển xuống nửa để tra, không bỏ thông tin.
6. Việc nhỏ: đọc lại cột "Người dùng gặp gì" của phụ lục I (agent viết gọn lại, không chép nguyên văn) · gỡ dòng giới hạn "trang Giới thiệu còn ghi OpenAI" ở bài 37 khi phiên làm code đã sửa trang · chưa ai đọc lại TOÀN VĂN bài 21 và 16 sau khi cắt · phụ lục D: hệ thống đổi lời dặn thì chạy lại `cd backend && PYTHONPATH=$PWD uv run --no-sync python ../data/hoc_cung_D/tools/chep_loi_dan.py`.
7. Chủ dự án CHƯA nhận xét bài nào ngoài bài 6. Ngày 23/11 anh ấy tự thử hệ thống trong lúc nhóm làm ⇒ hệ thống sẽ còn đổi: mỗi lần phiên điều phối báo một thay đổi, sửa bài gốc trước rồi gom lại phụ lục B, F, G, H, I.

## Cách làm đã dùng (giữ nguyên)
- Chủ dự án: quen phần AI; gần như chưa biết giao diện web, máy chủ, API, cơ sở dữ liệu ⇒ giảng các khái niệm đó từ đầu. Anh ấy muốn được HỎI trong lúc làm (mỗi lần một câu có ô tick), không muốn D cắm đầu viết. Yêu cầu gốc: đọc xong phải GIẢI THÍCH được từng quyết định và "hỏng thì sao"; chỉ viết thứ hệ thống thật có; giọng giáo trình dễ hiểu; đủ quan trọng hơn ngắn nhưng không lặp.
- Viết / chuyển / cập nhật bằng agent con theo `data/hoc_cung_D/LOI_GIAO_VIET_BAI.md`; MỖI nhóm bài sau đó qua một agent con KHÁC đối chiếu theo `data/hoc_cung_D/LOI_GIAO_KIEM_BAI.md` (biên bản ở `data/hoc_cung_D/kiem/`), rồi agent viết áp biên bản, D soát grep + rào, đẩy, nhắn phiên điều phối gộp. Mỗi lúc nhiều nhất HAI agent con; agent con không commit.
- Mỗi lần đẩy: `git fetch && git merge origin/main`, đóng giờ `date` vào dòng 3 của bài, `git add <file> && .githooks/pre-commit; git reset -q`, `scripts/commit_push.sh "<lời>" <file…>`.
- Công cụ riêng tư ở `data/hoc_cung_D/tools/`: `sua.py` (sửa nhiều chỗ, báo chỗ không khớp), `thay_khoi.py`, `chen_muc.py`, `doi_so_kho.py`, `chep_loi_dan.py`, `vet_tim.py`.

## Luật viết đã rút ra (đọc trước khi sửa bài)
1. "Kho không có" phải dò bằng `scripts/grep_kb.sh` trước khi dùng làm ví dụ.
2. Đọc cả lớp gọi (route chat đường gửi dần, giao diện, lệnh chạy tay), không chỉ hàm lõi; phân biệt "lỗi lúc bật máy chủ" với "lỗi giữa lúc chạy", "hạn giờ một lần gọi" với "hạn chung cả lượt".
3. Mỗi gạch "Ý chính" phải đứng được trước MỌI dòng bảng của chính bài.
4. Câu chuẩn (đúng lúc 15:51 22/11): "10 đoạn ở lần tìm đầu; trợ lý được tìm thêm tối đa 3 lần; tin nhiều ý được nối thêm 2 đoạn mỗi ý" · "model đang chạy: lượt có công cụ giữ chữ tới khi qua kiểm nguồn; model trả chữ dần: hiện trước, kiểm sau, hỏng thì rút lại" · kho lệch chỉ mục: "máy chủ vẫn chạy, mọi câu hỏi nhận lời báo" (phép so chỉ chạy lúc bật).
5. Mỗi con số ghi model, bộ câu, ngày; số đo cũ giữ nguyên kèm "lúc đó…"; phép đo gộp thì nói là gộp.
6. Không tra ra lý do ⇒ "chưa thấy ghi lý do. Điều thấy được: …" (không đoán); "chủ dự án đã quyết" chỉ khi hồ sơ ghi lời chủ dự án; "cách khác" phải là cách khác của đúng câu hỏi đó; trước khi viết "chưa thử" phải grep cả `docs/superpowers/plans/`.
7. Lời báo trong ngoặc kép chỉ khi chép từng chữ từ code; ca hỏng chưa ai thử ghi "đọc từ chương trình".
8. Rào pre-commit chặn dòng trùng ≥ 40 ký tự với kho ⇒ không chép dòng dài của kho.
9. Hệ thống đổi nhiều lần mỗi buổi ⇒ câu tuyệt đối ("không bao giờ", "luôn") kiểm lại sát giờ đẩy; sau mỗi lượt cập nhật grep các cụm cũ trong cả thư mục.
10. Bài tổng hợp (40, 41) và phụ lục gom dùng ĐÚNG số của bài gốc; hai bài nói khác nhau thì mở nguồn gốc mà phân xử, không tự chọn.

## Ghi chép riêng tư (không commit)
- `data/hoc_cung_D/BAN_VOI_A_VA_D_BEN_KIA.md` — lời chủ dự án (các câu tick 22/11), mọi tin của phiên điều phối kèm số đo, các lượt phản biện về hình thức của một phiên giảng khác.
- `data/hoc_cung_D/viet/*.md` — báo cáo của từng agent viết / chuyển / cập nhật (kể cả `phan_xu_cho_khac_nhau.md`, `cap_nhat_14h47.md`); `data/hoc_cung_D/kiem/*.md` — biên bản đối chiếu; `data/hoc_cung_D/vi_du_*_vet.json` — năm lượt thật làm ví dụ.

## Đang khai báo sửa
- `bai_hoc/giao_trinh/` (chỉ thư mục này) + file này.
