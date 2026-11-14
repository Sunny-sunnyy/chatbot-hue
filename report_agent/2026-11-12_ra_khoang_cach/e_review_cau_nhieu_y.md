# Review nhánh câu nhiều ý `p9-cau-nhieu-y` `2c99534` · E · 15:08 14/11/2026

Người làm: C. Plan vòng 1 `docs/superpowers/plans/2026-11-14-cau-nhieu-y-plan.md`, vòng 2 `…-cau-nhieu-y-v2-plan.md`. Số đo: `c_cau_nhieu_y_do.md`, `c_cau_nhieu_y_do_v2.md`.
User chọn BẬT (14:44 14/11/2026, đọc sàn Golden chỉ cho câu đi vào luật mới) ⇒ review này xét code + bằng chứng, không xét lại quyết định đó.

## Kết luận: `ready_for_user_confirmation` — A merge + bật `cau_nhieu_y` được (3 minor, không chặn)

## Đã kiểm
- **Phạm vi diff** (so `cfb5d99`): `settings.yaml` (+1 cờ, tắt), `assistant.py`, `full_corpus_prompt.py`, `generator_openai_full_corpus.py`, test mới, 2 plan. Không file ngoài phạm vi. Gộp sạch với `main` `4e6e1ff` và với `p9-sua-lich-tre` (`git merge-tree`).
- **Cờ tắt / câu một ý ⇒ chuỗi gửi model giống byte:** lời dặn theo ý là bản `replace` đúng một đoạn luật từ chối (có `assert` lúc import: đoạn đó phải có đúng 1 lần); agent theo ý chỉ được chọn khi `trace.nhieu_y` (= cờ bật ∧ `so_y ≥ 2`); `_lich_extra` chỉ thêm `nhieu_y` khi đúng. Test khoá cả hai (`test_flag_off_sends_old_instructions_byte_identical…`, `test_one_part_question_with_flag_on_sends_old_instructions`).
- **Hai đường stream / không stream** đều qua `_before_model` (đặt `trace.nhieu_y`) trước khi chọn lời dặn. Đường song song (#6) và đường sửa lịch song song: trace phụ tự đặt `nhieu_y`, `_merge_spec` chép sang trace chính (không nằm trong `keep_own`) ⇒ đúng.
- **Chốt (a)** (`chi_y_thieu`): chỉ khi mọi dòng có chữ đều mở đầu bằng hằng `CAU_Y_THIEU` ⇒ thay bằng câu từ chối chuẩn ⇒ cổng web như cũ. Stream: giữ chữ khi mọi dòng đủ là dòng thiếu và dòng dở còn là khúc đầu của hằng; kết thúc vẫn chỉ-dòng-thiếu ⇒ `_chu_giu_lai` trả câu từ chối. Test stream cả hai chế độ (`test_stream_never_shows_missing_only_text`).
- **Độ trễ chữ đầu** (luật giữ chữ mới có thể làm chậm): đếm 0 USD trên câu trả lời thật vòng 2 — dòng ý thiếu đứng ĐẦU câu trả lời **0 / 10** câu hỏi kèm (0 / 176 Golden, 0 / 32 an toàn không có dòng thiếu) ⇒ giữ chữ chỉ kéo dài vài ký tự đầu (tới khi lệch khỏi "Tư liệu…") ⇒ không đo độ trễ có phí.
- **Cổng web** (`co_y_thieu`): mở thêm khi câu nhiều ý có dòng thiếu không trích dẫn; mọi điều kiện cũ (tuyến, không lịch, không nút, chưa tra…) giữ. Truy vấn gửi Serper vẫn là câu người dùng (đường ra đã có, spec Phase 9 §7); kiểm cuối mục web không đổi.
- **NK06 / NK07** (bộ kín của E, hỏi C trước khi kết luận): C dò 4 + 4 lần (chỉ in số, ghi trong `c_cau_nhieu_y_do_v2.md` mục "Hai điểm E nêu") — NK07 từ chối cả câu ở **cả** cờ bật lẫn tắt (đếm 1 vế ⇒ luật cũ, hành vi của main); NK06 `GenerationError` 1 lần, chạy lại 4 lần 0 lỗi, đường không đổi ⇒ lỗi API chập chờn. Chấp nhận (E chưa tự thấy file của 8 lần dò này).
- **Test** (worktree sạch `2c99534`): 49 đạt có khoá (`test_cau_nhieu_y`, `test_assistant`, `test_openai_full_corpus_generator`, `test_het_luot_tim`); `test_cau_nhieu_y` không khoá 25 đạt.

## Finding
- **m-1 (theo dõi, giới hạn plan đã ghi):** `so_y` đếm vế theo dấu `,` `;` `?` ⇒ câu 2 ý nối bằng "và" / không dấu (kiểu NK07) đếm 1 ⇒ về luật cũ, từ chối cả câu như main. Không tệ hơn main. Muốn bắt thì cần dữ liệu mới (việc khác).
- **m-2:** biến thể agent theo ý chỉ dựng khi lời dặn là bản runtime; harness truyền lời dặn khác mà bật cờ ⇒ `AttributeError` (lỗi lộ, không lặng lẽ gửi sai). Chấp nhận; ghi để người đo sau biết.
- **m-3 (đề xuất, nhỏ):** `chat_metrics` không ghi `nhieu_y` / `chi_y_thieu` ⇒ sau khi bật không đếm được từ log bao nhiêu câu đi vào luật mới, bao nhiêu bị chốt (a) — trong khi Golden chỉ còn 0 / 176 câu đi vào, rủi ro luật mới chỉ đo trên 10 + 5 + 4 câu. Thêm 2 trường bool (không chữ) như `het_luot` để theo dõi; A quyết làm trước hay sau khi bật.

## Tiền
0 USD (review chỉ đọc + test + đếm trên file có sẵn).
