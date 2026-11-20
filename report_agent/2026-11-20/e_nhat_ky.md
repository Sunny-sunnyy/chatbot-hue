# Nhật ký phiên E — 20/11/2026 (viết 13:09 20/11/2026, giờ `date`, lúc kết phiên; cho phiên E SAU không có trí nhớ gì)

Trang ngắn để mở đầu là `session_prompt/sessions/STATUS_E.md`; file này là phần dài. Thứ riêng tư (câu dò, ảnh, tệp tải về) nằm trong `data/` — ở đây chỉ ghi đường dẫn.
Từ dùng: **dòng tên nơi** = dòng ghi chú do code viết sau mỗi câu trả lời từ kho, nêu tên các nơi có bài riêng vừa được trích (tính năng "nhớ tên nơi vừa trích", bật 19/11) · **lượt có phí** = một lần hỏi qua model thật.

## 1. Việc trong ngày, theo thứ tự (mọi nhánh đã gộp vào main)
| # | Việc | Kết quả | Hồ sơ |
|---|---|---|---|
| 1 | Cập nhật sổ ghi việc `bao_cao_he_thong/` cho tối 18/11 + 19/11 | gộp | lịch sử git |
| 2 | Soạn bộ dò (54 câu, soạn mù) + review nhánh sửa nhỏ "xin liệt kê lại" của phiên B | bộ thêm 20 câu soạn SAU khi đọc code bắt 11 / 12 câu hỏi về một nơi bị nhận nhầm ⇒ B viết lại thành khuôn câu ⇒ đạt 0 câu ra sai trên cả hai bộ ⇒ gộp | `data/kich_ban_pho_thong_2026-11-19/viec_2_sua_nho/`: `BO_DO_E.md`, `BO_DO_E_2.md`, `REVIEW_E.md`, `NHAN_E.md` |
| 3 | Chạy danh sách test phần B bằng trình duyệt thật (bản 29 tính năng bật) | 13 dòng đạt, 1 dòng khác mong đợi (hỏi tổng tiền vé: có lượt ra tổng do model tự cộng, có lượt nói kho chưa có), 2 dòng không chạy | `data/test_cuoi/CHAY_E_2026-11-20.md`; cột "Nhóm đã thử trước chưa" của `data/test_cuoi/DANH_SACH.md` đã cập nhật |
| 4 | Lỗi MỚI thấy khi chạy việc 3: hỏi A ⇒ hỏi B ⇒ gõ lại NGUYÊN VĂN câu A thì trợ lý trả lời câu B | do dòng tên nơi (bật: đúng 0 / 3 · tắt: 3 / 3); chỉ khi gõ lại nguyên văn. Đã sửa hẹp (B viết, E đo: 3 / 3; câu trỏ lại gõ lại vẫn đúng nơi mới 3 / 3), rồi thu hẹp thêm bằng nhánh hai dòng của phiên điều phối | `data/test_cuoi/chay_2026-11-20/LOI_GO_LAI_CAU_CU.md` (số đo, tiêu chí ghi trước, kết quả) |
| 5 | Review hai nhánh sửa sau soát khác hãng (B, C) + nhánh nhỏ thứ hai của C + nhánh hai dòng | đều ready sau khi C vá một ca ngược E nêu (lượt sửa lịch hỏng có chữ bão làm file mất câu 112) | `data/test_cuoi/chay_2026-11-20/REVIEW_E_nhanh_B_sua_sau_soat.md`, `REVIEW_E_nhanh_C_sua_sau_soat.md` |
| 6 | In lịch từ khung trợ lý nổi / trang Trợ lý bị cắt (hai model khác hãng nêu, E thấy bằng PDF) | E sửa: ẨN nút "In / Lưu PDF" trong vùng trò chuyện, chỉ còn ở trang Lên kế hoạch; phiên C nhìn lại ba file | `data/review_khac_hang/2026-11-19_diem_dung_buoc_5/tai_hien/e_gemini_in.md`, `e_g6_pptx_5_ngay.md` |
| 7 | Bảng đối chiếu kết quả soát đợt sửa của hãng thứ hai (11 điểm: 6 trùng, 5 mới — cả 5 tái hiện bằng hàm thật) | gửi phiên điều phối; chủ dự án chọn sửa hai điểm, còn lại ghi giới hạn ở sổ tay bàn giao mục 10 | tin nhắn; sổ tay `guides/RUNBOOK_BAN_GIAO.md` mục 10.1, 10.2, 10.3b |
| 8 | E viết: lịch đã sửa giữ câu bão / lũ + 112 ở thẻ lịch, bản in, .txt, .ics, PowerPoint | gộp; C review | `report_agent/2026-11-20/e_the_lich_giu_112.md` |
| 9 | Hai script + khuôn mở đầu đề của bộ đánh giá coding agent | xong, thử trên bài giả, đã dọn | mục 4 dưới |

## 2. Thứ chỉ phiên E biết cách làm
**Bật một server riêng cổng 8018 từ một bản code bất kỳ** (không đụng cây chính; một server ~1,5 GB RAM; trước khi bật: `free -m` khả dụng ≥ 4 GB, `ss -ltn | grep 8018` trống, báo phiên điều phối):
```bash
git worktree add --detach /tmp/hr_e_<việc> <sha hoặc origin/main> && cd /tmp/hr_e_<việc> || exit 1
ln -s /home/minhhieu/hue_rag/data data; ln -s /home/minhhieu/hue_rag/knowledge-base-hue knowledge-base-hue; ln -s /home/minhhieu/hue_rag/frontend/dist frontend/dist
cd backend && HF_HUB_OFFLINE=1 HUE_SO_VET=true PYTHONPATH=. uv run --project /home/minhhieu/hue_rag/backend --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8018
```
- `--project …/backend` dùng môi trường Python 3.13 của cây chính (không dựng `.venv` mới trong worktree); `PYTHONPATH=.` để nạp code của worktree. Thiếu ba symlink ⇒ test / server hỏng giả.
- Tắt: lấy PID từ `ss -ltnp | grep ':8018 '`, kiểm `readlink /proc/<PID>/cwd` đúng là worktree của mình rồi mới `kill`. Không `pkill -f`.
- Đổi một tính năng để so hai bên: sửa đúng một dòng trong `backend/config/settings.yaml` của WORKTREE, khởi động lại, xong `git checkout -- backend/config/settings.yaml`.
- Tiền thật của một lượt chạy: từ worktree, `uv run --project /home/minhhieu/hue_rag/backend python scripts/dem_chat_metrics.py --sha HEAD`.
- Sửa `frontend/src` thì phải `npm run build` (worktree: symlink `frontend/node_modules` về cây chính, dựng `dist` riêng); sau khi gộp phải dựng lại ở cây chính.

**Script trình duyệt** (Chromium không màn hình, model thật): `data/test_cuoi/tools/chay_b.py` — chạy từ `backend/` của cây chính: `uv run python ../data/test_cuoi/tools/chay_b.py http://127.0.0.1:8018 <mã,mã…>` (thêm `--with pypdf` cho mã có bản in). Ghi `data/test_cuoi/chay_2026-11-20/ket_qua.json` + ảnh / tệp tải về. Script chỉ GHI LẠI; đạt hay không do người đọc.
Mã có sẵn: các dòng danh sách (`b6a b6b b14a b14b b1a b3 b9 b12 lich1 lich2`) · chuỗi gõ lại câu cũ và biến thể (`aba aba_v1 aba_v2 da* db* dc* goc* p6_* goiy`) · bản lưu lịch và câu 112 (`c2a c2b c3a c3b e1a e1b`) · nút PowerPoint ở thẻ lịch cũ (`so8`) · file PowerPoint lịch 5 ngày (`g6`). Không nêu mã ⇒ chạy cả danh sách phần B (≈ 24 lượt có phí ≈ 0,04 USD).
In thử bằng đúng nút "In / Lưu PDF": mẫu ở các file `/tmp/hr_e_in_*.py` (mất khi tắt máy) — cách làm: thay `window.print` bằng hàm rỗng, bấm nút, `emulate_media("print")`, gắn lớp in, `page.pdf`, rồi MỞ file ra nhìn.
Xem file PowerPoint bằng PowerPoint thật (một file một lần, không gọi khi PowerPoint đang mở): `data/xuat_lich_dep_2026-11-19/buoc_2/xuat_anh.sh`; xoá bản sao phía Windows sau khi xong.

## 3. Buổi chủ dự án test — phần CHỈ NGƯỜI làm được, nhóm chưa chạy
Mở tệp `.ics` bằng ứng dụng lịch trên điện thoại (dòng B8) · bấm "In / Lưu PDF" bằng tay trên trình duyệt có màn hình, kể cả lịch 3 ngày (B13) · xem trên điện thoại thật (B2) · phần A và C của `data/test_cuoi/DANH_SACH.md` (bộ câu kín: agent không mở).
Phiên E hỗ trợ được: bật server cổng 8018 cho buổi test nếu phiên điều phối giao; chạy lại một dòng bằng script khi chủ dự án thấy lạ; mở sổ vết `data/debug_trace/<ngày>.jsonl` của đúng lượt đó để xem lịch sử gửi model, câu tìm kho, nguồn.

## 4. Bộ đánh giá coding agent — việc E giữ và việc E đã trả lại
- ĐÃ CÓ, dùng được (riêng tư, `data/danh_gia_model_2026-11-20/`): `dung_hop.sh <Tn>` · `thu_ket_qua.sh <Tn>` · `KHUON_MO_DAU.md` · khung của phiên điều phối `KHUNG.md`. Đã thử trên một bài giả rồi dọn. Script KHÔNG tự xoá thư mục cũ khi dựng lại (chốt an toàn của công cụ không cho script xoá bằng biến) — người dựng tự xoá đúng thư mục.
- ĐÃ TRẢ LẠI phiên điều phối, CHƯA có gì: ba bài E nhận dựng (T3, T7, T10). Lý do: lượt viết của E bị hệ thống dừng hai lần, cả hai đúng lúc bắt đầu soạn T3; E không thử lại và không tìm đường vòng. Phiên C cũng bị dừng ở cụm việc này. Ai làm tiếp do chủ dự án và phiên điều phối quyết.

## 5. Câu còn treo của E
1. Ca chưa ai đo sau nhánh hai dòng: lượt đầu có dòng tên nơi ⇒ hỏi A (lượt A không có dòng tên) ⇒ hỏi B ⇒ gõ lại nguyên văn A — lịch sử vẫn lệch dạng; có trả lời nhầm câu B không thì chưa biết.
2. Nguyên nhân gốc bản in bị cắt trong vùng trò chuyện chưa tìm (mới ẩn nút). Hai lần thử gỡ hộp cuộn bằng luật in: nội dung đủ nhưng thừa 6 rồi 2 trang trắng đầu.
3. Bấm lại nút câu gợi ý sau một câu khác: mới thử một nút, và nút đó không sinh dòng tên nơi nên không thử được bản sửa.
4. Khối tóm tắt của `bao_cao_he_thong/07_…` (~175 dòng) và file 01 (~150 dòng) vượt giới hạn độ dài từ trước — đã chốt KHÔNG gộp lại; sổ này chỉ sửa chỗ sai.

## 6. Bẫy của phiên (đủ; trang STATUS chỉ giữ các ý chính)
- Bộ dò soạn MÙ ra 0 lỗi, bộ soạn SAU khi đọc code bắt 11 / 12 ⇒ người kiểm phải đọc luật và tự soạn ca, không chỉ chạy lại bộ có sẵn.
- Nêu lỗ của một phương án TRƯỚC khi có code (câu trỏ lại ngắn bị gõ lại nguyên văn) rẻ hơn nhiều so với bắt sau.
- Sàn đã đạt thì dừng: lần nới bộ từ để tăng số câu nhận đã mở thêm lỗ.
- Lỗi bản in chỉ thấy khi MỞ file PDF; đếm trang / đếm chữ không đủ.
- Ghi số dòng vào báo cáo theo ước lượng ⇒ lệch commit; lấy từ `git show --numstat`.
- Tìm chuỗi "112" trong tệp `.ics` dính dấu thời gian ⇒ tìm cả cụm chữ.
- Ghi chữ cột mong đợi từ MỘT lượt là quá tay (hỏi tổng tiền vé: hôm trước ra tổng, hôm nay ra "kho chưa có").
- Lệnh `rm` / xoá có biến trong script bị chốt an toàn của công cụ chặn ⇒ dùng đường dẫn đầy đủ, hoặc để người tự xoá.
- Lịch sử trong sổ vết là lịch sử SAU khi code đã gỡ dòng tên nơi ⇒ muốn kiểm hàm gỡ phải lấy lượt của bản chưa sửa.
- Vấp luật do đọc ngắn lúc mở phiên: 0.

## 7. Tiền API của E (lệnh đếm theo mã bản của từng lượt server)
0,0371 (danh sách test + chẩn đoán) + 0,0212 (đo cỡ lỗi gõ lại) + 0,0154 (hai phép thật của bản sửa) + 0,0051 + 0,0039 + 0,0044 (các lượt thử nhánh C, bản in, file 5 ngày) + ≈ 0,004 (lượt trình duyệt của việc 8) ≈ **0,091 USD**; chưa gồm một lần gọi model thật của `test_api_chat`.
