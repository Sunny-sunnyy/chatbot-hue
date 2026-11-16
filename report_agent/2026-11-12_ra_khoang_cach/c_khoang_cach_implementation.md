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
| Kiểm bảng (0 USD) | 4 cặp 0 km (điểm sát nhau ⇒ "dưới 0,5 km"); 62 cặp nội thành lệch chiều (đường một chiều — dùng đúng chiều); OSRM ước nhanh (4 km = 4 phút) ⇒ bản đầu sàn 40 km/h (đã thay — xem mục "Sửa theo review"); cặp qua sông (một điểm bờ bắc ↔ nhóm lăng bờ nam) đường đi gấp tới 18 lần chim bay — đúng là phải vòng qua cầu | 0 |
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

## Sửa theo review (agent con của A, `data/review_khoang_cach_2026-11-16/review.md`: changes_requested 1 major + 4 minor) — C, 15:01 16/11/2026 `date`

### M1 — đối chiếu số với nguồn công khai, thay sàn 40 km/h [đã chạy]
Bản đầu **bỏ sót** bước "đối chiếu 5 cặp với nguồn" của plan §2 và không ghi là bỏ (lệch plan, chưa khai báo). Đã tra (Codex `data/tra_cuu_cli/2026-11-16_quang-duong-hue/`, chỉ thông tin công khai); C tự mở kiểm 3 nguồn (VietnamTourism lăng Tự Đức cập nhật 23/10/2026, lăng Minh Mạng cập nhật 11/11/2026, Sun Travel Lập An cập nhật 30/09/2026).

| Cặp | km OSRM | km nguồn | phút OSRM | sàn 40 (bản đầu) | **1,25 × OSRM + 5 (bản sửa)** | phút nguồn |
|---|---|---|---|---|---|---|
| Đại Nội → chùa (bờ sông, gần) | 4,4 | ~5 | 5 | 7 | **11** | 10–15 (xe máy, từ trung tâm) |
| Đại Nội → lăng (tây nam, ~6 km) | 6,3 | 6–7 | 12 | 12 | **20** | 20 (xe máy) / 20–25 (GrabCar) |
| Đại Nội → lăng (~12 km) | 13,2 | ~12 | 12 | 20 | **20** | 20–30 (Grab) / 25–35 (xe máy) |
| Chợ → biển (~15 km) | 15,1 | 14–18 / 15 | 14 | 23 | **23** | dưới 30 / 25–30 (xe máy) |
| Đại Nội → đỉnh đèo (đường dài) | 79,3 | 75–80 | 75 | 119 | **99** | 90–120 |
| Đại Nội → đầm (đường dài) | 69,9 | 64–65 | 63 | 105 | **84** | ~75 (xe riêng) |

- **km:** OSRM khớp nguồn trong khoảng 10 % ở cả 6 cặp. Cặp vườn quốc gia: OSRM 58,7 km tới toạ độ trong bảng (vùng đỉnh), nguồn ghi 40 km tới cổng + ~17 km đường trong vườn ⇒ khớp. Cặp phá: toạ độ bảng khác điểm nguồn nói (bến khác) ⇒ không so.
- **phút:** sàn 40 khớp khoảng nguồn ở 3 / 6 cặp (2 chặng nội thành quá nhanh, chặng đầm quá chậm). **1,25 × OSRM + 5: 6 / 6** trong hoặc sát khoảng nguồn (chặng đầm 84 so với ~75 là chậm hơn 12 %; chặng biển 23 nằm trong "dưới 30", thấp hơn "25–30"). Giới hạn: 6 điểm đối chiếu, nguồn phần lớn tính "từ trung tâm" chứ không đúng điểm bảng; là luật ước, không phải số đo.

### Minor
- **m1 bộ dò:** từ chỉ thời gian ("mấy phút / tiếng", "bao lâu") chỉ tính khi câu có từ di chuyển (đi, từ, tới, đến, sang, ra, vào, xe, chạy); bỏ "cách làm / nấu / tính / chế biến / đây / pha / ăn…". Chạy lại script của reviewer: bộ 27 câu bỏ sót 0, bật thừa 5 (như cũ); 8 câu "giống mà không phải" của reviewer: **1 / 8 bật** (trước 7 / 8; câu còn lại "đi thuyền … bao lâu" có từ "đi" — vô hại); câu khoảng cách thật 12 / 14 (2 câu không dấu — được phép). Thêm 8 ca vào test. `data/khoang_cach_2026-11-16/do_lai_sau_review.out` (phần 4 của script dùng kiểu hàm cũ nên dừng — các ca đó nằm trong test mới).
- **m2 kiểm số:** tách tập cho phép theo loại (km ↔ thời gian); số trong đoạn kho được trích vẫn cho cả hai loại (trừ chính nguồn khoảng cách); xét thêm viết tắt "15p", "1h", "9 cây"; chuẩn "07" ⇒ "7". Test có ca đối chứng: đảo đơn vị ⇒ bắt được; viết tắt ⇒ bắt được. **Giới hạn còn:** không tách theo cặp (lượt nhiều cặp ⇒ số của cặp này dùng cho cặp kia vẫn lọt); số viết bằng chữ ("hai cây số") không xét; câu ghép model tự nêu giờ mở cửa mà đoạn kho có giờ đó không được trích ⇒ bị rút lại cả câu.
- **m3 test Q1:** thêm test so toàn bộ kwargs gửi model giữa cờ tắt và cờ bật với câu không có từ khoá (lượt đầu + lượt có lịch sử, stream và không) ⇒ giống hệt. **Ca đối chứng** (đổi sang câu có từ khoá) ⇒ test báo khác 2 / 2 — phép so thật sự phân biệt được. Loại lượt "sau nút" không áp dụng (lượt biểu mẫu không có vòng công cụ). Reviewer cũng đã dò giống byte 8 / 8 trên cấu hình thật.
- **m4:** ghi ở plan §6 (viết hàm kiểm riêng; dòng người dùng thấy ghi "đi xe"); làm tròn phút đổi sang làm tròn nửa lên.

### Đo lại sau sửa [đã chạy] — server tạm 8041, cờ bật tạm, cùng 16 câu
| Chỉ số | Bản đầu | Sau sửa |
|---|---|---|
| Gọi đúng cặp (14 câu trong bảng) | 13 / 14 (sau chạy lại 2 câu) | **13 / 14** (câu hụt vẫn là câu "có gần nhau không", trả lời từ kho) |
| Câu có số km / phút không thuộc đúng cặp, cùng loại | 0 (sau sửa làm tròn) | **0 / 14** (tính lại từ `do_r3_sau_review.json`; cột "số lạ" in lúc chạy sai vì harness còn so kiểu cũ — đã sửa `do.py`) |
| Câu bị rút lại | 2 / 14 (oan) ⇒ 0 | **0 / 16** |
| Nơi ngoài bảng ra số | 0 / 2 | **0 / 2** |
| Tiền lượt | 0,01664 + 0,00137 USD | **0,01544 USD** |
| Tốc độ (câu có gọi công cụ, `chat_metrics`) | chữ đầu p50 4,4 / p95 8,9 s (n = 17) | **chữ đầu p50 3,7 / p95 ≈ 6,2 s** (n = 14, nội suy); ≈ 0,00081 USD / câu (17 dòng cuối `application_8041_r2.log`) |

Test `tests/test_khoang_cach.py`: **46 passed** (16 s). Test rộng: xem dòng cuối mục này.
**Tiền cả việc ≈ 0,0103 + 0,0180 + 0,0154 ≈ 0,044 USD** (trần 0,15).

Test rộng `backend/tests` sau sửa (có `--env-file`): **1228 passed** (5 phút 43 giây).
