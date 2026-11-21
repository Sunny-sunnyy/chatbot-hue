# Sửa lịch bằng lời: lệnh "dời … sang buổi tối" được trả lời thật (nhánh `p9-b-doi-buoi-toi`, cờ `sua_lich_buoi_toi`, mặc định TẮT)

Viết: 14:07 21/11/2026 (giờ `date`), phiên B. Giao: phiên điều phối (ca phiên đo thấy ở phiên trọn vẹn qua trình duyệt trên Sonnet). Nền: main `e75cf18`.
Trạng thái: **code + test xong, đã đo thật trên hai model; chờ một phiên khác review, phiên đo chạy thước, rồi phiên điều phối quyết bật.**

Từ dùng: *lần hiểu ý* = một lời gọi model riêng đọc câu sửa lịch và trả danh sách hành động có tên (bỏ / thêm / thay / dời…); code áp và viết câu báo ·
*khuôn hành động* = danh sách trường model được điền; trường `buoi` trước nay chỉ nhận sáng / chiều.

## 1. Người dùng thấy gì khác (khi cờ bật)

| Người dùng nói | Trước (bản đang chạy) | Sau |
|---|---|---|
| Dời một điểm tham quan ban ngày sang buổi tối (ví dụ Đại Nội sang tối ngày 1) | Sonnet: "Chưa rõ ngày / buổi để dời Đại Nội Huế." (dù họ nói rõ) hoặc câu chung "việc này mình chưa sửa được"; luna: câu chung, hoặc tự hiểu thành buổi chiều / sáng rồi báo lý do của buổi đó | "Đại Nội Huế chưa dời sang buổi tối ngày 1 được vì đây là điểm tham quan ban ngày, còn buổi tối lịch chỉ xếp hoạt động buổi tối. Dời được sang: buổi sáng ngày 3 (đổi chỗ với …)." — lịch giữ nguyên |
| Dời / thêm một hoạt động buổi tối vào tối ngày khác | câu chung hoặc xếp vào buổi ban ngày | "Mình chưa xếp tay được … vào buổi tối — hoạt động buổi tối do lịch tự chọn. Bạn có thể bỏ hoạt động tối đang có để lịch chọn hoạt động khác." — lịch giữ nguyên |
| Mọi lệnh sáng / chiều, bỏ, thêm, thay | — | không đổi |

Cờ bật KHÔNG làm cho lịch xếp được điểm vào buổi tối theo ý người dùng; nó chỉ làm câu trả lời nói đúng điều đã xảy ra và vì sao.

## 2. Nguyên nhân gốc [máy kiểm — 18 lượt thật trên main, ba câu × 3 lần × hai model]

Khuôn hành động chỉ có `buoi: sang | chieu` ⇒ model KHÔNG CÓ CÁCH ghi "buổi tối". Sonnet high: 5 / 9 lượt trả `doi_buoi` để trống buổi ⇒ code in "Chưa rõ ngày / buổi";
4 / 9 trả "chưa hỗ trợ". luna: 6 / 9 "chưa hỗ trợ", 2 / 9 tự đổi "tối" thành "chiều". Không model nào hiểu sai câu; lỗi ở khuôn.

## 3. Đổi gì

| File | Đổi gì |
|---|---|
| `backend/llm/sua_lich_v2.py` | Khuôn `HanhDongToi` (như `HanhDongCHT`, `buoi` nhận thêm `toi`) · trong `ap`: `buoi == "toi"` ⇒ luôn là một câu nói thật, không bao giờ xếp: điểm ban ngày đang ở trong lịch ⇒ lý do `ban_ngay` + các chỗ dời được (dùng lại đúng phép thử của lần dời bị luật chặn, tách thành `_goi_y_doi`); điểm đi được buổi tối ⇒ câu `toi_chua_xep`; thêm điểm ban ngày vào buổi tối ⇒ câu có sẵn "không đi được vào buổi đó" |
| `backend/llm/full_corpus_prompt.py` | `SUA_LICH_LOI_DAN_TOI` = bản đang dùng, chỉ khác MỘT dòng (dòng `doi_buoi`: thêm `toi` + "người dùng nói buổi tối thì điền toi… xếp được hay không là việc hệ thống") |
| `backend/llm/generator_openai_full_corpus.py` | Agent thứ ba `sua_lich_toi_agent` (khuôn + lời dặn mới, khoá đệm riêng); `hieu_sua(..., buoi_toi=True)` chọn nó |
| `backend/llm/assistant.py`, `len_ke_hoach.py`, `config/settings.yaml` | Cờ `sua_lich_buoi_toi` (cần `sua_lich_chua_ho_tro`), mặc định false; cờ tắt ⇒ lời gọi và khuôn như cũ |
| `backend/tests/test_sua_lich_buoi_toi.py` | 5 ca, bảng điểm thật + bộ xếp thật |

Không làm: cho người dùng tự xếp hoạt động buổi tối (cần đổi bộ xếp — tính năng mới, phải hỏi chủ dự án).

## 4. Bằng chứng

**Test bằng đồ giả / hàm thuần [máy kiểm]:** `uv run pytest tests/test_sua_lich_buoi_toi.py -q` ⇒ `5 passed`. Tắt riêng nhánh `buoi == "toi"` trong `ap` ⇒ 2 ca đỏ (đã thấy).
Một ca bất biến: mọi điểm × mọi chỗ sáng / chiều của một lịch 3 ngày qua khuôn mới cho kết quả y như qua khuôn cũ. Bảy file test liên quan: `189 passed`.

**Lượt thật qua code sản phẩm (`hieu_sua` ⇒ `ap` ⇒ câu báo), hai model, mong đợi ghi trước trong script [máy kiểm]:**

| Bộ | luna, cờ tắt ⇒ bật | Sonnet high, cờ tắt ⇒ bật |
|---|---|---|
| 4 câu dời điểm ban ngày sang tối × 3 lần: model ghi đúng `doi_buoi` + `toi` + đúng ngày | (khuôn cũ không ghi được) ⇒ 12 / 12 | (không ghi được) ⇒ 12 / 12 |
| — người dùng thấy lý do thật "điểm tham quan ban ngày…" | 0 / 12 ⇒ 12 / 12 | 0 / 12 ⇒ 12 / 12 |
| — người dùng thấy "Chưa rõ ngày / buổi" hoặc bị hiểu thành buổi khác | 2 / 12 ⇒ 0 | 4 / 12 ⇒ 0 |
| 3 câu đối chứng × 3 lần (dời sang chiều · bỏ hoạt động buổi tối · câu hỏi có chữ "tối") | 9 / 9 ⇒ 9 / 9 | 9 / 9 ⇒ 9 / 9 |
| 9 lệnh sửa lịch cũ (bộ của thước) × 2 lần, cờ bật | 18 / 18 | 18 / 18 |

Một trong bốn câu dời sang tối là cách nói không dùng khi viết lời dặn. 138 lượt, 0 lỗi kỹ thuật, 0,82 USD.

## 5. Chưa làm / giới hạn

- **[chưa kiểm] Lượt qua trình duyệt với cờ bật** (câu báo mới hiện trong khung "Không đổi được" của thẻ lịch — đường hiển thị không đổi, nhưng chưa nhìn).
- Bộ câu do người viết code tự đặt (7 câu); chưa có bộ mù của phiên khác. Phiên đo chạy thước (9 lệnh sửa lịch + chuỗi sửa lịch) quyết bật.
- Luna ở cờ bật có lượt điền thêm `buoi: toi` vào hành động `bo_diem` (2 / 3) — `ap` không đọc trường đó ở `bo_diem`, kết quả đúng.
- Câu hai vế ("dời A sang tối ngày 1 và B sang sáng ngày 2") chưa đo.
- Câu báo mới là chữ người dùng thấy ⇒ phiên điều phối đã ghi vào danh sách chờ chủ dự án xem.

## 6. Bảng kết

| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Khuôn + lời dặn + code trả lời thật, sau cờ | Xong | `uv run pytest tests/test_sua_lich_buoi_toi.py -q` ⇒ `5 passed` |
| Đo hai model, cờ tắt ↔ bật | Xong | số gốc: thư mục riêng tư `ket_qua/b_sua_lich_buoi_toi/` của lượt thử Bedrock 21/11 |
| Review của phiên khác · thước của phiên đo · lượt trình duyệt | Chưa | — |
| Bật cờ | Chưa — phiên điều phối quyết sau thước | — |

## 7. Thêm 14:46 21/11/2026 (giờ `date`) — nhánh `p9-b-buoi-toi-chu-va-thay`: ba điểm chữ của review + một lỗi có sẵn

**Ba điểm chữ phiên review nêu (chỉ có tác dụng khi cờ `sua_lich_buoi_toi` bật):**

| Tình huống | Trước | Sau |
|---|---|---|
| Xin dời một hoạt động tối sang ĐÚNG buổi tối nó đang đứng | "Mình chưa xếp tay được … Bạn có thể bỏ hoạt động tối đang có…" (bảo bỏ chính thứ họ muốn giữ) | "Chợ Đông Ba đang ở buổi tối ngày 1 rồi." |
| Thêm / dời một điểm ban ngày CHƯA có trong lịch vào buổi tối | "… không đi được vào buổi đó." | "… không xếp được vào buổi tối vì đây là điểm tham quan ban ngày, còn buổi tối lịch chỉ xếp hoạt động buổi tối." |
| Chữ "xếp tay" (từ của người làm) | "Mình chưa xếp tay được … để lịch chọn hoạt động khác." | "Mình chưa đặt được … vào buổi tối theo ý bạn — hoạt động buổi tối do lịch tự chọn. Bạn có thể bỏ hoạt động tối đang có, lịch sẽ tự chọn một hoạt động khác." |

**Lỗi có sẵn, sửa KHÔNG sau cờ (phiên review tái hiện 4 / 4 lượt, hai model, cờ tắt cũng vậy):** "thay <hoạt động đang ở buổi tối> bằng …" ⇒ thẻ báo "… không có trong lịch hiện tại" trong khi
nó đang ở buổi tối của chính lịch đó. Gốc: hàm tra vị trí của code chỉ biết hai buổi ban ngày. Code chưa thay được hoạt động buổi tối (bộ xếp tự chọn hoạt động tối) ⇒ nay nói thật:
"Mình chưa thay được hoạt động buổi tối theo ý bạn — hoạt động buổi tối do lịch tự chọn. Bạn có thể bỏ Chợ Đông Ba, lịch sẽ tự chọn một hoạt động tối khác." Lịch không đổi (như trước). Điểm
thật sự không có trong lịch vẫn nhận câu cũ. Không đổi gì gửi model.

**Bằng chứng:** `uv run pytest tests/test_sua_lich_buoi_toi.py -q` ⇒ `7 passed`; chạy test mới trên code main ⇒ 3 ca đỏ (đã thấy); bốn file test sửa lịch `157 passed`.
Lượt thật qua `hieu_sua` ⇒ `ap` ⇒ câu báo, 5 câu × hai model × cờ tắt / bật = 20 lượt, mong đợi ghi trước [máy kiểm]: hai câu thay hoạt động tối ra câu mới 8 / 8 (không còn "không có
trong lịch"); cờ bật: "đang ở buổi tối ngày 1 rồi" 2 / 2, câu "điểm tham quan ban ngày" cho điểm chưa có trong lịch 2 / 2; câu đối chứng (thay một điểm ban ngày) như trước 4 / 4.
**Chưa làm:** lượt trình duyệt; "bỏ buổi tối ngày 1" kéo hoạt động khác lên lấp mà câu báo không nói — phiên điều phối để chủ dự án quyết, không sửa ở đây.
