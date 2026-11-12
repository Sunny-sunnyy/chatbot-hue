# Plan (mức nhẹ) — "ăn gần điểm X": thêm dòng định vị cho bài quán trong kho · **NHÁP — chờ User chọn**

Người viết: C, 19:30 12/11/2026 (`date`), A giao. Chưa làm gì: không sửa kho, không code, 0 USD. Repo public: không chép nội dung kho / câu hỏi.

## Căn cứ để review

- Lượt đếm 12/11: `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` §4–§5.
- Đợt sửa kho gần nhất làm mẫu quy trình: `report_agent/2026-11-05_sua_kho_gio/c192_implementation.md` + guide `guides/full_corpus_rag.md` mục "Build lại index".
- Luật sửa kho: `Session_Prompt.md` §5 (sao lưu vào `knowledge-base-hue/meta/`, review bằng diff, không enrich bằng web khi chưa có phạm vi duyệt).

## 1. Lỗi đã đếm

6 câu tự viết kiểu "ăn gì / quán nào gần điểm X": chỉ 1 câu kho trả lời đủ dùng, 3 câu kho từ chối, 2 câu trả lời một phần.
Kho có **81 bài riêng cho quán ăn + cà phê**: 63 bài có dòng địa chỉ, nhưng chỉ **12 bài** có câu nói quán gần điểm tham quan nào; 4 bài có toạ độ.
(Sửa số: report đếm ghi "15 / 81" — 15 là đếm cả thư mục món ăn; riêng 81 bài quán / cà phê là 12.)
⇒ Trợ lý không nối được "điểm X" với quán vì bài quán không nói nó ở gần đâu.

## 2. Việc đề xuất

Thêm vào mục thông tin của mỗi bài quán **một dòng**: quán ở khu nào và gần điểm tham quan nào (tên điểm đúng như tên bài trong kho), chỉ khi có căn cứ.
Phạm vi chạm: tối đa **53 bài** (có địa chỉ, chưa có câu định vị). 16 bài không có địa chỉ: **không sửa**. Không đổi code, không đổi lời dặn.

### Hai cách lấy thông tin "gần điểm nào"

| | Cách A — chỉ dùng thông tin đã có trong kho | Cách B — dùng toạ độ từ dữ liệu ngoài đã tải (**C khuyến nghị**) |
|---|---|---|
| Làm gì | Từ địa chỉ trong bài quán, đối chiếu với các bài điểm tham quan / cẩm nang trong kho để suy "cùng khu" | Khớp tên + địa chỉ quán với bộ dữ liệu mở của thành phố (đã tải 05/08, ~6.800 cơ sở ăn uống có toạ độ); điểm tham quan dùng toạ độ đã có trong bảng điểm lịch trình (18 điểm) + dữ liệu mở di tích. **Code** tính khoảng cách, viết dòng "cách <điểm> khoảng … m" cho điểm gần nhất dưới một ngưỡng |
| Phủ được | Ít: C thử dò — bài điểm tham quan trong kho **không** ghi địa chỉ dạng số nhà + tên đường (0 bài dò được) ⇒ không nối được bằng máy; phải người / model đọc và suy ⇒ dễ sai | Ước 30–45 / 53 bài (tuỳ tỉ lệ khớp tên; đo ở bước 1) |
| Rủi ro | Suy sai khu ⇒ đưa câu sai vào kho (lỗi nặng: nói chắc sai) | Khớp nhầm cơ sở trùng tên ⇒ sai toạ độ. Chặn: chỉ nhận khi khớp cả tên và tên đường; người xem bằng mắt toàn bộ dòng sinh ra trước khi ghi |
| Tốn | 0 USD; ~2–3 giờ đọc tay, khó kiểm lại | 0 USD; ~1 giờ viết script khớp + ~30 phút xem bằng mắt |
| Chọn khác mất gì | Chọn A: giữ kho "chỉ từ nguồn đã có", nhưng phủ thấp và không kiểm được bằng máy | Chọn B: đưa một con số khoảng cách tính từ dữ liệu ngoài vào kho ⇒ cần User đồng ý phạm vi này (dữ liệu công khai của thành phố; ghi nguồn ở mục nguồn của bài) |

Vì sao khuyến nghị B: khoảng cách là **phép tính ⇒ code làm**, kiểm lại được, không nhờ model suy. Sai khi: tỉ lệ khớp tên thấp (< 20 bài) ⇒ dừng, báo A, không ép.

## 3. Các bước (theo luật sửa kho; mỗi bước dừng được)

1. **Dò khớp, chưa ghi (0 USD):** script khớp ⇒ bảng "bài quán · điểm gần nhất · khoảng cách · căn cứ khớp" ở `data/sua_kho_2026-11-12_an_gan/` (private). In số bài khớp.
2. **Người xem:** C xem cả bảng; A / User xem mẫu 10 dòng. Dòng nghi ngờ ⇒ bỏ.
3. **Đo "trước"** (trên kho hiện tại): 6 câu ăn gần đã dùng + 6 câu ăn gần **mới** (viết trước khi ghi kho, người viết không phải người viết script) · an toàn 32 ×2 · T1 158 câu (0 USD) · Golden: các câu có đoạn trong bài bị chạm.
4. **Sao lưu** 53 bài vào `knowledge-base-hue/meta/backup_an_gan_2026-11-12/` + bản sao build record / sparse state ⇒ **ghi kho** ⇒ diff với bản sao.
5. **Build lại chỉ mục tại chỗ** (script theo mẫu `chay.sh` 05/11: kiểm khoá ⇒ ghi ⇒ chia đoạn thử ⇒ xoá collection + record + sparse ⇒ build ⇒ T1 sau; lỗi ⇒ tự lùi). Máy phải rảnh: không session nào chạy server / đo.
6. **Đo "sau"** cùng bộ bước 3 ⇒ report ⇒ một review cả đợt.
7. **Nhãn đoạn đúng:** 14 / 55 câu có trích dẫn nằm trong bài quán / cà phê ⇒ thêm dòng làm lệch vị trí ⇒ dựng **gold v6** bằng dời vị trí (không đổi nội dung nhãn), kiểm lại bằng script chỉ đọc.

## 4. Tiêu chí ghi trước

| | Mức |
|---|---|
| **Quyết** | 12 câu ăn gần (6 cũ + 6 mới): số câu kho trả lời đủ dùng tăng từ mốc "trước" lên **≥ 8 / 12**, và 6 câu mới không ngược chiều |
| Sàn an toàn 32 ×2 | đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 · ngoài kho bị trả lời 0 (thủ tục sinh lại khi chênh 1) |
| Sàn tìm (T1, 0 USD) | 0 câu **không chạm** bài bị sửa mất đoạn đúng |
| Sàn Golden (câu chạm) | 0 câu trong kho chuyển sang từ chối; 0 lỗi trích dẫn mới |
| Đúng nội dung | 0 dòng định vị sai trong mẫu 15 dòng người kiểm độc lập xem lại (sai ≥ 1 ⇒ gỡ cả đợt, lùi kho) |

Phạm sàn ⇒ lùi kho từ bản sao + build lại từ kho cũ (như script 05/11), ghi kết quả âm.

## 5. Tiền · giờ · file chạm

- **Tiền ≤ 0,08 USD** (mốc 05/11: 0,024 cho 11 bài; đợt này thêm an toàn 32 ×2 ×2 phía ≈ 0,045 + 24 lượt câu ăn gần ≈ 0,02 + Golden câu chạm ≈ 0,01). Build chỉ mục 0 USD (CPU).
- **Giờ:** ~3–4 giờ agent (script + xem + đo trước / sau + build ~20–40 phút máy bận).
- **Chạm:** 53 file trong `knowledge-base-hue/foods/` (private, không git) · chỉ mục Qdrant + build record + sparse state · `gold_v6.jsonl` + hằng `GOLD_PATH` (1 dòng code) · mốc T1 mới · bài học 1 / 19 + sổ ghi việc khâu kho.
- **Thứ tự với B7:** làm **sau** lượt B7 giữa kỳ (đã chạy trên kho cũ); lượt B7 cuối tháng 12 sẽ chạy trên kho mới ở cả hai bên.

## 6. Cần User chọn

1. Làm / không làm. 2. Cách A hay B (B đưa khoảng cách tính từ dữ liệu mở vào kho). 3. Trần tiền 0,08.
