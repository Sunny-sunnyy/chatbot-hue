# Công cụ khoảng cách giữa hai điểm — implementation (C, 14:35 16/11/2026 `date`)

Plan: `docs/superpowers/plans/2026-11-16-khoang-cach-plan.md` (mức nhẹ, A duyệt 16/11). Nhánh `p9-khoang-cach`. Cờ `assistant.khoang_cach: false` (mặc định tắt).

## Đã làm
- **Bảng số dựng một lần** (`data/khoang_cach_2026-11-16/tools/dung_bang.py`, private): một lần gọi bảng khoảng cách OSRM (máy chủ thử công khai) với toạ độ công khai 40 điểm bảng lịch ⇒ `data/phase_9/lich_trinh/khoang_cach_v1.json` md5 `cb76ab72199c`, 1.560 / 1.560 cặp có số. Lúc chạy chatbot không gọi mạng.
- **`backend/llm/khoang_cach.py`** (mới): nạp bảng + tên điểm; dò từ khoá khoảng cách (câu cuối hoặc câu hỏi liền trước); dựng dòng "Từ A đến B: khoảng X km đường đi, khoảng Y phút đi xe (ước theo đường)" + "chưa tính kẹt xe hay dừng nghỉ"; mã `khac` / cặp thiếu ⇒ câu "chưa có số"; kiểm số km / phút trong lời model.
- **`backend/llm/assistant.py`**: cờ + bảng trong `AssistantFlags`; `khoang_cach_for_turn` (tham số là enum mã điểm + `khac`, kết quả đăng thành một nguồn có mã [n] như `ngay_lich`, ≤ 3 lần / câu); chỉ đưa công cụ khi có từ khoá; sau lần sinh: số km / phút ⊄ (nguồn khoảng cách ∪ đoạn trích) ⇒ rút lại như citation hỏng; stream không báo "đang tìm kho" cho công cụ này.
- **`backend/llm/generator_openai_full_corpus.py`**: thêm công cụ khi có hàm; `max_turns` + 1 khi có đưa công cụ. **Cờ tắt / câu không từ khoá ⇒ danh sách công cụ và `max_turns` như cũ** (test khoá).
- **`backend/config/settings.yaml`**: `khoang_cach: false`, `khoang_cach_bang`.
- Code không đọc tên nơi từ chữ người dùng: model ánh xạ tên ⇒ mã trong danh sách cố định; code chỉ đọc chữ người dùng để quyết có đưa công cụ.

## Đo [đã chạy]
| Bước | Kết quả | Thời gian / tiền |
|---|---|---|
| Đếm trước khi xây (server 8010, 6 câu, mỗi câu một cuộc) | **4 / 6 bị kho từ chối** rồi ra mục web; 2 / 6 model ước từ câu "cách trung tâm" | 0,0103 USD (vượt mức ước ≤ 0,002: câu từ chối có tra web) |
| Kiểm bảng (0 USD) | 4 cặp 0 km (điểm sát nhau ⇒ "dưới 0,5 km"); 62 cặp nội thành lệch chiều (đường một chiều — dùng đúng chiều); OSRM ước nhanh (4 km = 4 phút) ⇒ sàn 40 km/h; cặp qua sông (một điểm bờ bắc ↔ nhóm lăng bờ nam) đường đi gấp tới 18 lần chim bay — đúng là phải vòng qua cầu | 0 |
| Bộ dò từ khoá 27 câu (agent con của A soạn) | **0 câu ra sai** (10 / 10 câu rõ + 4 / 4 câu ghép bật); bật thừa 5 (1 câu ranh giới, 1 câu thời lượng đi dạo, 3 câu đi ra ngoài Huế — công cụ trả "chưa có số") | 0 |
| Bộ an toàn 32 — đếm câu chạm từ khoá bằng code | **0 / 32 chạm** ⇒ theo luật không chạy lượt an toàn có phí | 0 |
| Test `tests/test_khoang_cach.py` (34) | đạt; có ca đối chứng ra "có" cho phép kiểm số (số tự ước ⇒ bắt được) | ~16 s |
| Lượt đo có phí, server tạm 8041 (cờ bật tạm trong worktree), 16 câu: 6 câu đếm + 10 câu mới (cặp trong bảng, tên khác, câu hỏi tiếp "từ đó sang…", câu ghép, 2 nơi ngoài bảng) | **gọi đúng cặp 13 / 14** (đạt quyết ≥ 12 / 14; câu hụt là câu "có gần nhau không" — model trả lời từ kho, đúng); **nơi ngoài bảng ra số 0 / 2** (model gửi `khac` ⇒ từ chối + mục web như cũ); 2 / 14 bị **rút lại oan** vì bước kiểm số không nhận số làm tròn ("4,0 km" ⇒ "4 km") ⇒ sửa `tap_so`, chạy lại đúng 2 câu đó: 2 / 2 đạt, đúng cặp. **0 số sai** đến tay người dùng. | 0,01664 + 0,00137 USD |
| Tốc độ (câu có gọi công cụ, n = 17, từ `chat_metrics`) | chữ đầu p50 4,4 s / p95 8,9 s; cả câu p50 4,9 s / p95 14,2 s; 3 lần gọi model thường (định tuyến + gọi công cụ + viết); ≈ 0,0010 USD / câu (trước: câu từ chối + web ≈ 0,0022 USD) | — |
| Test rộng `backend/tests` (có `--env-file`, worktree đã build giao diện) | **1216 passed**; lần chạy đầu 1 fail do worktree chưa có `frontend/dist` (không phải code nhánh) | 5 phút 31 giây |
| File chạm cờ, KHÔNG `--env-file` (`test_khoang_cach`, `test_ngay_lich`, `test_b5b_thoi_tiet`) | 208 passed | 29 giây |

Tiền cả việc ≈ 0,0103 + 0,0180 ≈ **0,028 USD** (log server tạm: 19 dòng `chat_metrics` sha `84f1765` = 0,01801). Trần 0,15.

## Giới hạn
- Chỉ 40 / 41 điểm bảng lịch (Không gian lưu niệm Lê Bá Đảng chưa có toạ độ). "Trung tâm thành phố", khách sạn, sân bay, nơi ngoài Huế ⇒ "chưa có số" (người dùng hay hỏi "cách trung tâm" — chưa làm).
- Số là ước theo đường ô tô của OSRM + sàn 40 km/h; chưa đối chiếu với bản đồ thương mại; không có đi thuyền / đi bộ.
- Một điểm (đầm phía đông) bám đường cách 857 m ⇒ số của nó lệch thêm chừng đó.
- Lượt đo n = 14 câu trong bảng, một lượt (mức nhẹ).

## Dữ liệu (private)
`data/khoang_cach_2026-11-16/`: `dem_truoc.{py,json}`, `do.py` (lượt đo, có `--mo-phong` 0 USD, `--chi`), `do_r1.json`, `do_r2_chay_lai.json`, `bo_do_tu_khoa.jsonl`, `osrm_tho.json`, `application_8041.log`, `tools/dung_bang.py`.
