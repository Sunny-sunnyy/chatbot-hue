# Review: sửa chỗ cũ / sai trong `bao_cao_he_thong/` (10/11)

Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-4f`) · 19:35 10/11/2026 (`date`) · A giao. Đối tượng: commit `c54c932` trên `main` (11 file `bao_cao_he_thong/`,
+164 / −140 dòng). Căn cứ: danh sách chỗ cũ `data/ra_soat_bao_cao_2026-11-10/sa1_duong_doc_chinh.md` mục 1 + `sa2_khau_du_lieu_danh_gia.md` mục 1 (private);
hiện trạng `session_prompt/Project_Status.md` §2 / §4, `CURRENT_HANDOFF.md`, `backend/config/settings.yaml`, code `backend/`, Qdrant GET.
Mức kiểm theo A giao: (1) chỗ sửa đúng hiện trạng không (lấy mẫu chỗ nặng nhất) · (2) có chỗ sửa thành sai hoặc ghi việc 10/11 như đã chạy không ·
(3) có lọt nội dung kho / Golden / dự án khác không. Không xét sắp xếp lại (chờ User).

## 1. Phạm vi đã review

- Đọc **đủ** diff theo từ (`git show c54c932 --word-diff`) của cả 11 file.
- Đối chiếu từng dòng của `sa1` mục 1 (31 mục) và `sa2` mục 1 (29 mục) với diff: các mục mức "cao" / "chắc" **đều đã sửa**. Không sửa mục 2–4 của `sa1`
  (câu khó hiểu, phần chưa có, thứ tự đọc), đúng phạm vi A giao.
- Kiểm thật (0 USD, chỉ đọc) 16 chỗ nặng nhất:

| # | Chỗ (file) | Khẳng định sau sửa | Kiểm bằng | Kết quả |
|---|---|---|---|---|
| 1 | LUONG, SINH, DANH_GIA, README | S5 09/11: câu Huế 2,16 / 4,32 s, 0,00047 USD; ngoài phạm vi 1,62 / 2,97; xã giao p95 7,73; câu ngày 5,19 / max 11,0 s, 0,00063 USD | `CURRENT_HANDOFF.md` "S5 chung", `Project_Status.md` §2 | khớp |
| 2 | README, SINH, LUONG | từ chối nhầm 4–6 / 158 sau B2 (03/11), trước 12 / 158 (30/10) | LUONG cũ :125, SINH :63 (cùng nguồn sub-agent trích) | khớp (số đo 03/11, ghi rõ ngày) |
| 3 | README, SINH, LUONG, HOI_BANG_ANH | hỏi bằng ảnh bật 08/11 | `settings.yaml` `anh.bat: true`; `git log` `cf57309` | khớp |
| 4 | SINH, LUONG | ảnh thu nhỏ gửi OpenAI, máy chủ không lưu ảnh | `backend/llm/nhan_anh.py:52,65` (giải mã + ghi vào `BytesIO`, không ghi đĩa); `canh_dai: 1024` | khớp |
| 5 | SINH, LUONG | `POST /api/conversation/new` xoá nhớ | `backend/api/routes/chat.py:177-184` | khớp |
| 6 | SINH | `chat_metrics` ghi mã lượt ⇒ nối 👍 / 👎 | `chat.py:59` (`turn_id` trong tập trường), `:214` | khớp |
| 7 | SINH | công cụ `hoi_lai` đã gỡ, không còn khoá cờ; còn `backend/llm/hoi_lai.py` | `settings.yaml` không có `hoi_lai`; file tồn tại | khớp |
| 8 | SINH | luật từ khoá khẩn cấp (`emergency.py`) đã gỡ code | `backend/llm/emergency.py` không còn | khớp |
| 9 | SINH, LUONG | 429 `rate_limited` khi đặt `HUE_LUOT_MOI_NGAY`, đếm RAM, không ghi IP | `backend/api/gioi_han.py` (C viết 09/11, đã kiểm thật lúc đó) | khớp |
| 10 | TIM_KIEM | `settings.yaml:60` router, `:66` tim_them, `assistant.py:52` `MODEL_SEARCH_LIMIT = 2` | đọc đúng dòng | khớp |
| 11 | LUU_TRU_QDRANT, KHO_DU_LIEU, LUONG | 2 collection: chatbot 8.435 + `hue_anh_siglip2` 172 | `GET /collections` lúc mở phiên (2 collection, 8.435 điểm) + `Project_Status.md` §4 | khớp |
| 12 | LUONG, LUU_TRU, EMBEDDING, TIM_KIEM, DANH_GIA | build record `9921888f2030`, sparse `4a8311a2dfef`, mốc tìm `64656a87c109` (05/11 tối) | `Project_Status.md` §4 | khớp |
| 13 | DANH_GIA, README | công cụ ngày: 14 câu mới bớt 9 từ chối nhầm, 0 sai ngày | SINH (bản trước) đoạn T1 | khớp |
| 14 | NEN_TANG | mốc test 824 đạt (09/11, nhánh ngày trước khi vào `main`) | SINH (bản trước) — đúng là số của nhánh `p9-t1-sang-nam`, đã ghi rõ | khớp |
| 15 | README | Phase 9 ≈ 3,6 / trần 4,2 USD | `CURRENT_HANDOFF.md` (≈ 3,6 sau 09/11; trần 4,2 từ mở phiên 10/11) | khớp |
| 16 | README, HOI_BANG_ANH | đúng trong 3 gợi ý 22 / 25 ảnh | bảng HOI_BANG_ANH (không đổi) | khớp |

## 2. Findings

**Blocker:** không. **Major:** không.

**Minor (A tự sửa):**

- **m-1 · `LUONG_HOAT_DONG_HE_THONG.md` mục "Chưa đưa ra ngoài"** — câu "4 chốt … (giới hạn số lượt hỏi / IP / ngày, cookie chỉ qua https, tắt trang `/docs`,
  log xoay vòng) — **bật bằng biến môi trường lúc deploy, không đặt ⇒ như cũ**". Log xoay vòng **luôn bật** từ `ccc9f4f` (`backend/config/logging.yaml`, không
  có biến môi trường); chỉ 3 chốt kia theo biến. Cùng file, mục giới hạn đã ghi đúng ("Log xoay vòng từ 09/11"). Tác động: người đọc tưởng log hiện chưa xoay
  vòng. Đóng: tách "3 chốt bật bằng biến môi trường; log xoay vòng luôn bật".
- **m-2 · `BAO_CAO_NEN_TANG.md`** — "hàm đọc cấu hình chung chỉ kiểm 4 nhóm gốc". `backend/core/settings_loader.py` kiểm 3 nhóm (`full_corpus`,
  `full_corpus_runtime`, `full_corpus_generation`); `vector_database` không được kiểm (`grep -c vector_database` = 0). Câu cũ ("kiểm đúng các nhóm này") cũng
  đã sai. Đóng: "kiểm 3 nhóm (kho, runtime, sinh)".
- ~~m-3~~ **đã kiểm, không phải lỗi:** dòng đầu SINH rút gọn, nhưng 2 thay đổi người dùng thấy 09/11 vẫn nằm ở mục 1 (`BAO_CAO_SINH_CAU_TRA_LOI_API.md:9` câu ngày + âm lịch
  bật, `:13` câu khẩn cấp không còn câu soạn sẵn).

**Câu hỏi (2) — có chỗ sửa thành sai / ghi 10/11 như đã chạy:** không thấy. Mọi chỗ nhắc việc 10/11 đều ghi "đang thử 10/11, chưa vào chatbot" (xã giao
song song, câu ngày nhanh) hoặc "kế hoạch đang nháp" (B7). Số tốc độ / tiền mới đều trỏ đúng lượt đo chung 09/11, số cũ giữ kèm ngày.
**Câu hỏi (3) — lọt nội dung:** dòng thêm mới không có tên dự án khác, `case_index`, câu Golden hay trích kho (đếm từ khoá trên `git show -U0 | grep '^+'` = 0;
hook `.githooks/pre-commit` quét trùng ≥ 40 ký tự lúc A commit — C không chạy lại). Tên địa danh chỉ ở mức loại ("điểm Quần thể", "chợ, phố, chùa") —
đúng luật mức loại câu.

## 3. Cách người kiểm chạy lại thật

`git show c54c932 --word-diff=plain`; đọc dòng code / cấu hình ở bảng §1 (`sed`, `grep`, `ls`); Qdrant GET đã có lúc mở phiên. Không chạy test, không gọi API.

## 4. Kết quả quan sát

16 / 16 chỗ mẫu khớp hiện trạng; 2 minor về chữ, không có số sai.

## 5. Giới hạn hoặc phần chưa chạy

Không đọc lại toàn văn 11 file (chỉ diff) ⇒ chỗ cũ **không nằm trong danh sách `sa1` / `sa2`** có thể còn; dòng `file:dòng` trong các bảng "kiểm với code" đã được
tự ghi "chưa kiểm lại". Không chạy lại hook quét trùng.

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`** — 0 blocker, 0 major; 2 minor A tự sửa (không cần review lại).
