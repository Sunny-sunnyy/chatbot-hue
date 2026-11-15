# Harness sửa lịch tự mô phỏng nhãn trước lượt có phí + công cụ kiểm bộ tách khỏi file kín — implementation

Người làm: B · viết 19:33 15/11/2026 · A giao (handoff "Việc đầu phiên sau" mục 2) · **0 USD, không lượt có phí, không gọi model** · chỉ sửa công cụ trong `data/` (private, không tracked).

## Tóm tắt
- **Đạt cả ba tiêu chí A ghi trước:** (1) mô phỏng nhãn trên bộ chuỗi đã thấy với bảng điểm đang chạy (41 điểm) ra **10 / 10**; (2) ca đối chứng nhãn lệch ⇒ harness **DỪNG** (mã thoát 2) trước khi gửi câu nào; (3) không lượt có phí.
- **Phát hiện ngoài dự kiến:** công cụ kiểm khuôn bộ `kiem_bo.py` bản cũ không chỉ "mở cả file kín" mà còn **không chạy được** từ 14/11 — nó mô phỏng trên bộ xếp cũ + bảng điểm cũ, trong khi nhãn đã viết lại theo lịch bản 2 ⇒ vỡ (KeyError) ngay ở bộ đã thấy. B viết gọn lại thay vì chỉ tách.

## Đã đổi gì (file trong `data/`, bản cũ giữ đuôi `.truoc_2026-11-15_toi.py`)
| File | Đổi | md5 (12) |
|---|---|---|
| `data/len_ke_hoach_v2_2026-11-13/tools/q3_sua_lich.py` | Trước khi gửi câu đầu tiên, tự chạy `bo_do_sua_lich/tools/mo_phong_v2.py` (tiến trình con) trên cả file bộ; không ra đúng "n / n chuỗi khớp" (kể cả khi công cụ lỗi) ⇒ in chuỗi lệch rồi thoát mã 2. Với `--kin` chỉ in dòng đếm, bỏ stderr của công cụ (traceback có thể lộ nhãn). Bỏ đường dẫn cứng tới một worktree đã gỡ; thêm `--backend` (mặc định backend cây chung). | `5e0791c8a2bd` |
| `data/phase_9/bo_do_sua_lich/tools/kiem_bo.py` | Viết gọn lại: chỉ kiểm phần tĩnh — lượt 1 đúng loại, enum tham số, loại hành động, id điểm có trong **bảng đang chạy**, điểm ngoài bảng phải có nhãn "không đổi", cỡ bộ, phủ loại câu. Bỏ phần mô phỏng trên bộ xếp cũ (nay do `mo_phong_v2.py` làm bằng chính code sửa lịch bản 2). **Mặc định chỉ mở bộ đã thấy**; `--ca-kin` mới mở file kín và chỉ in một dòng số đếm. Ca phá tìm chỗ sửa theo khuôn, không ghim số thứ tự chuỗi. | `5d8019427db8` |
| `data/phase_9/bo_do_sua_lich/README.md` | Thêm mục cập nhật (hai dòng trên). | — |

Không đổi: `mo_phong_v2.py`, bộ chuỗi (`chuoi_da_thay.jsonl` md5 `eacb8ebdcb91`), code `backend/`.

## Bằng chứng [Chạy] — đều 0 USD, không có server nào đang nghe ở cổng thử
| # | Ca | Kết quả |
|---|---|---|
| 1 | Bộ đã thấy hiện hành + bảng 41 điểm, cổng không có server | "mô phỏng nhãn: 10 / 10 ⇒ chạy lượt thật" rồi vỡ ở bước kết nối (đúng mong đợi: qua cổng mô phỏng, không gửi được câu nào) |
| 2 | **Đối chứng thật:** bản nhãn cũ trước khi bảng lên 41 điểm (một lượt "điểm ngoài bảng" nay đã có trong bảng) | "DỪNG trước lượt có phí — 9 / 10", in đúng chuỗi + lượt lệch, **mã thoát 2**, không mở kết nối, không tạo file kết quả |
| 3 | Ca 2 thêm `--kin`, kèm đuôi `2>/dev/null \| tail -1` | chỉ một dòng "DỪNG … 9 / 10", mã thoát 2 |
| 4 | `--backend` trỏ thư mục không có | dừng mã thoát 1, không in gì ra stdout |
| 5 | Nhãn hiện hành + bảng 34 điểm (qua `BANG_FILE`) | 10 / 10 (nhãn mới hợp cả hai bảng) |
| 6 | `kiem_bo.py --pha` trên bộ đã thấy | `OK` · `ca phá: 6 / 6` (id lạ · hành động lạ · ngoài bảng thiếu nhãn "không đổi" · enum sai · thiếu loại câu · thiếu một chuỗi) |
| 7 | `kiem_bo.py --ca-kin` trên **file kín GIẢ** trong `/tmp` (5 chuỗi chép từ bộ đã thấy ⇒ phải trùng) | một dòng: lỗi bộ đã thấy 0 · lỗi thêm 15 ⇒ phép kiểm trùng 3-gram có ra "có" |
| 8 | `--ca-kin` trên file kín GIẢ hỏng khuôn, kèm đuôi `2>/dev/null \| tail -1` | không in gì, "ma thoat: 1" — id giả không lộ |

Thời gian đo thật: `kiem_bo.py --pha` 0,16 s · mô phỏng nhãn 10 chuỗi 0,28 s. Không pytest, không Q1, không Playwright, không lượt có phí (không chạm `backend/` hay giao diện).

## Chưa làm / giới hạn
- **B không mở, không chạy trên file kín.** Phần kín của `kiem_bo.py` chưa ai chạy sau khi nhãn bộ đã thấy đổi ⇒ ghi "chưa đo". Lệnh cho User (chỉ in số đếm; giữ nguyên đuôi):
  ```
  cd /home/minhhieu/hue_rag/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/phase_9/bo_do_sua_lich/tools/kiem_bo.py --ca-kin 2>/dev/null | tail -1; echo "ma thoat: ${PIPESTATUS[0]}"
  ```
  Cách đọc: "lỗi thêm khi gộp bộ kín: 0" + "ma thoat: 0" ⇒ khuôn bộ kín ổn; số > 0 ⇒ báo A (cần người được phép đọc); không có dòng đếm + "ma thoat: 1" ⇒ file kín sai khuôn hoặc công cụ lỗi, không lộ gì. Hai lệnh đếm bộ kín cũ trong handoff (mô phỏng nhãn kín) vẫn dùng được, không đổi.
- Harness mô phỏng trên **cả file bộ** kể cả khi chạy `--chi` một phần (0,3 s, không đáng tách).
- Đo server của một worktree có bảng khác cây chung mà quên `--backend` ⇒ mô phỏng theo bảng cây chung (đã ghi ở đầu file harness).
- `kiem_bo.py` không còn tự kiểm "áp nhãn có phạm luật không"; ai sửa nhãn phải chạy cả `mo_phong_v2.py` (harness Q3 nay tự chạy nên không lọt tới lượt có phí).
- Các harness khác của bộ sửa lịch (Q5, Q5b, bộ đổi hạng / đổi ngày đi) không dùng nhãn phụ thuộc bảng theo kiểu này ⇒ không thêm cổng.

## Tự kiểm
Diff chỉ ở 3 file `data/` kể trên + report này + `STATUS_B.md`. Không abstraction mới: một hàm 20 dòng trong harness; `kiem_bo.py` 155 ⇒ 113 dòng.
