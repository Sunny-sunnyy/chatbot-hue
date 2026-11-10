# Plan (mức nhẹ) — câu xã giao: gọi model trò chuyện song song với định tuyến

Người viết: B (`hue-rag-05`) · bản 1 19:08 10/11/2026 (`date`) · việc A giao 19:05 10/11/2026 (`CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11"). Nhánh `p9-xa-giao-song-song`
từ `main` `624a17b`, worktree `/tmp/b_xg`. Repo public: không chép câu bộ đo.

## Vấn đề (số S5 09/11, `data/phase_9/s5_chung/s5_main_r1.jsonl`, 20 câu xã giao)

Chữ đầu xã giao p50 3,46 / p95 7,73 s (sàn 3 / 5 s). Hiện nay định tuyến chạy xong (p50 ≈ 1,7 s, 1,1–2,5 s) **rồi mới** gọi model trò chuyện. Hai lần gọi này
không phụ thuộc nhau: đầu vào của lần trò chuyện chỉ là câu hỏi + lịch sử ⇒ chạy cùng lúc thì bớt được đúng phần định tuyến. Phần lợi không bù được: 1 câu
có lần trò chuyện tự nó mất 8,2 s, 1 câu bị định tuyến xếp sang Huế (đi đường Huế, 7,6 s) ⇒ p95 của 20 câu có thể vẫn sát 5 s.

## Đổi một thứ

Cờ mới `assistant.song_song_tro_chuyen` (mặc định `false`; chỉ có tác dụng trên đường đã chạy song song của #6 — `song_song_tra_loi: true`, chỉ đường stream).
Bật ⇒ trong `answer_turn_stream_parallel`, cùng lúc với (i) định tuyến và (ii) phần Huế đang có, chạy thêm (iii) **lần trò chuyện** trên một trace phụ
(đúng hàm của đường cũ, tuyến đặt sẵn `tro_chuyen`). Sự kiện của (iii) giữ trong hàng đợi riêng tới khi có tuyến:
`tro_chuyen` ⇒ huỷ (ii), xả hàng đợi (iii), gộp trace (iii) vào trace chính · `tro_ly_hue` (cả định tuyến lỗi) ⇒ huỷ (iii), như hôm nay · `ngoai_pham_vi` ⇒ huỷ cả hai.
Lỗi của (iii) khi tuyến ≠ `tro_chuyen` ⇒ bỏ; tuyến = `tro_chuyen` ⇒ lỗi đi ra như đường cũ. `n_tra_loi_bo` / `usd_bo` cộng cả phần (iii) bị bỏ.
Không đổi: mọi lời dặn, đầu vào các lần gọi, `/api/chat` (không stream), nhớ hội thoại.

## Tiêu chí ghi trước · bộ đo · giữ sàn nào

| Mã | Đo gì (bộ) | Sàn / quyết | Giữ sàn nào | Tiền |
|---|---|---|---|---|
| **T** | test client giả trong `test_toc_do_song_song.py` (thêm ~4 test): tuyến `tro_chuyen` ⇒ 0 sự kiện trước tuyến, chữ = lời (iii), yêu cầu trò chuyện **giống byte** đường cũ; tuyến khác ⇒ 0 sự kiện / lần gọi của (iii) trong trace chính; (iii) lỗi + tuyến khác ⇒ câu đúng tuyến; cờ tắt ⇒ yêu cầu gửi model giống byte `main` (test sẵn có) | đạt hết | "không chữ nào hiện trước khi định tuyến xong" · "cờ tắt giống byte" | 0 |
| **AN** | lượt thật qua `_answer_events` (bản sao harness #6 `chay_an_toan.py`, cả hai cờ bật): bộ 90 lượt của #6 (19 trò chuyện, 30 khẩn cấp, 13 ngoài phạm vi, 8 câu thường, 20 Huế, có lượt kèm lịch sử) + 22 câu an toàn còn lại của bộ 32 = **112 lượt** | **0 vi phạm**: tuyến ≠ `tro_chuyen` ⇒ chữ hiện = câu cuối, không lần gọi `tro_chuyen` nào trong trace chính; tuyến = `tro_chuyen` ⇒ chữ hiện = câu cuối, không nguồn, không lần gọi `tro_ly_hue` trong trace chính; 0 lỗi | sàn "không lọt chữ" trên SDK + huỷ thật (lần #6 đã bắt lỗi thật ở đúng chỗ huỷ: việc nhỏ (7) 08/11) | ≈ 0,05 |
| **AT** | bộ an toàn 32 — **A chốt một trong hai** (dưới) | 4 số như `main` | an toàn | 0 / ≈ 0,03 |
| **S** | `s5_do.py` (bản sao, thêm cột `usd_bo`), server thật trên nhánh, cả hai cờ bật, Chromium, **1 lượt** bộ S5 65 câu | xã giao chữ đầu **p95 ≤ 5 s**; Huế + ngoài phạm vi p50 ≤ 3 / p95 ≤ 5 s và không chậm hơn S5 09/11 quá +0,3 s p50 | tốc độ (mục tiêu việc) · không làm chậm đường khác | ≈ 0,02 |
| theo dõi | USD / câu theo tuyến **gồm `usd_bo`** | NFR ≤ 0,0005 USD / câu | tiền | — |

**AT — A chọn:** (a, B khuyến nghị) **dùng lại 4 số của `main`** (mốc S1 `s1_moc_r1` 09/11 + phương án B lời dặn giống byte): câu an toàn đi tuyến Huế / khẩn cấp;
T chứng minh yêu cầu gửi model của đường đó giống byte, AN chứng minh (iii) không bao giờ hiện ở tuyến đó ⇒ câu trả lời cùng phân phối với `main`. Sai khi: (iii)
chạy song song làm đổi kết quả đường Huế qua đường khác ngoài chuỗi gửi (không thấy cơ chế nào). (b) chạy lại S-AT có judge 2 sub-agent: +≈ 0,03 USD, +~30 phút, chỉ lặp lại nhiễu judge.

**Không chạy (vòng tự soi):** mốc `main` S5 lại (đường Huế không đổi; so S5 09/11 là tham khảo) · đo lại tuyến K / S1 / N (lời dặn định tuyến không đổi ⇒ chỉ đo nhiễu) · Q1
`capture_all` (không chạm chỗ dựng chuỗi gửi model — T so byte bằng client giả) · ABBA.

## Rủi ro tiền — cần A biết trước

Lần trò chuyện ≈ **0,00004 USD** (S5: định tuyến + trò chuyện 0,000131 − định tuyến 0,000092). Bật ⇒ **mỗi câu không phải xã giao trả thêm ≈ 0,00004**
(lần trò chuyện thường xong trước hoặc ngay lúc có tuyến ⇒ trả gần đủ). Câu Huế S5: TB **0,00047** (không web 0,00042) ⇒ sau ≈ **0,00051** — **có thể vượt NFR
0,0005** (không web ≈ 0,00046 vẫn dưới). Đo S cho số thật. Vượt ⇒ B báo A, đề xuất: User chọn tốc độ xã giao hay trần 0,0005 (User 09/11: "tiền thoải mái nhưng phải nhanh"),
không tự chỉnh.

## Tiền, dừng, thứ tự

Ước ≈ 0,07 (AN 0,05 · S 0,02; + 0,03 nếu AT (b)) ≤ trần 0,1. Dừng: tiền > 0,09 hoặc một sàn AN / T trượt ⇒ báo A. Thứ tự: code + T (test file chạm, có và không
`--env-file`) ⇒ chạy thử lệnh đo ở chế độ 0 USD ⇒ AN ⇒ (nhắn A + E "bắt đầu đo") S ⇒ "đo xong" ⇒ test rộng 1 lần ⇒ cổng ổn định ⇒ report ⇒ C review cả nhánh ⇒ A merge.
Đạt ⇒ merge với cờ `false`; A trình User bật (đổi hành vi + tiền mỗi câu). Âm ⇒ cờ `false`, tag hồ sơ, ghi kết quả.

## Rà agent (phần chạm)

Đường ra: thêm một lần gọi OpenAI (cùng nhà cung cấp, chỉ câu hỏi + lịch sử — ít dữ liệu hơn lần Huế) cho mọi câu đi qua định tuyến; không đường ra mới.
Phép tính / thứ tự bắt buộc (giữ chữ tới khi có tuyến, chọn phần giữ) ⇒ code; model không quyết gì mới.
