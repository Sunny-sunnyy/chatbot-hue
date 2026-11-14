# Sửa lịch bằng lời trên lịch bản 2 — B · 13:07 14/11/2026 · **mọi tiêu chí ghi trước ĐẠT (13:55 14/11/2026) — chờ E kiểm vòng chỉnh lời dặn**

Plan: `docs/superpowers/plans/2026-11-14-sua-lich-v2-plan.md` (A duyệt). Nhánh `p9-sua-lich-v2` (rebase trên `main` `42c0e04`), head **`fcfc07b`**, đã push. Cờ `assistant.sua_lich_v2` **TẮT**.

## Làm gì (theo luồng)
1. **Bộ xếp:** `xep_v2` thêm `giu` (điểm giữ đúng ngày / buổi) và `loai` (điểm đã bỏ không quay lại, kể cả danh sách lấp và buổi tối). Mặc định **giống byte 3.840 / 3.840** tổ hợp (mã băm trước = sau).
2. **Áp hành động** (`llm/sua_lich_v2.py`): 6 loại có tên — bỏ / thêm / thay / dời buổi / đổi số ngày / đổi tham số (kiểu đi, sở thích, trẻ em, người lớn tuổi); gửi tối đa 3, áp tối đa 2.
   - Mỗi hành động là **một lần xếp lại**, giữ chỗ mọi điểm không bị chạm. Giờ gợi ý, cụm, quỹ phút, mùa, mưa đều do đúng một bộ xếp tính.
   - Khung chỉ được nhận khi `kiem_khung_v2` = 0 lỗi, không thì giữ khung cũ + lý do.
   - "Thêm" khi buổi đã kín ⇒ thế chỗ một điểm lấp / ngoài sở thích, và câu báo nói rõ ("thế chỗ …").
   - "Thay" không nói thay bằng gì ⇒ thẻ chọn tối đa 3 điểm đặt được vào đúng chỗ cũ + "Bỏ điểm này".
   - Tên lạ ⇒ "Không đổi được" (không đoán). Tên ngắn chỉ nhận khi nằm trong **đúng một** tên điểm.
3. **Hiểu ý** (một lần gọi `gpt-6-luna`, suy luận thấp, đầu ra cấu trúc `SuaLichOutput`):
   - Khi cuộc có lịch đã lưu, mọi lượt chat qua lần này trước.
   - Danh sách rỗng ⇒ đường trả lời thường như cũ, kể cả định tuyến khẩn cấp.
   - Tin nhắn gửi model chỉ gồm dữ liệu code: lịch hiện tại, tham số, danh sách tên điểm, câu người dùng.
4. **Lượt sửa:** dùng lại luồng lịch bản 2 (`stream_v2`) trên khung đã áp.
   - Mục không đổi giữ câu cũ đã kiểm (đánh lại số nguồn), chỉ mục mới gọi model viết câu; không còn mục mới thì không gọi model.
   - `lich.thay_doi`: các dòng "Đã đổi / Không đổi được / Chưa làm" do code viết. `sua_ap`: dữ liệu code (id, mã luật) cho bộ đo và log.
5. **Lưu theo cuộc** (`api/conversations.py`): lịch mới nhất của cuộc. Chỉ dữ liệu code (khung, ngày đi, mưa, điểm đã bỏ, câu đã kiểm theo điểm); cùng hạn 30 phút; "Cuộc mới" xoá.
6. **Giao diện:**
   - thẻ chọn (`sua_the`; nút chỉ chứa id code đưa; bấm ⇒ `sua_chon`);
   - bước "Đang hiểu yêu cầu sửa lịch…" trong danh sách bước thật;
   - khối `thay_doi` trong `LichV2` (sửa 1 dòng của E: bỏ tiền tố bị lặp);
   - thẻ chọn không lặp câu hỏi.

## Khác plan (A đồng ý 14/11, kèm điều kiện đo)
- **Không** gắn `sua_lich` thành công cụ trong vòng trợ lý mà là **một lần gọi riêng**: không phải sửa chữ ký generator, lượt chat không có lịch không tốn thêm gì.
- **Cổng từ khoá đã thử và BỎ** (`data/len_ke_hoach_v2_2026-11-13/tools/do_cong_tu_sua.py`, 0 USD): câu sửa của bộ đã thấy qua cổng **17 / 19** (cần 100 %); 10 câu diễn đạt lạ B tự viết qua **3 / 10** (sàn 8 / 10) ⇒ lượt nào cũng qua lần hiểu ý khi cuộc có lịch.

## Kết quả
| Mã | Kết quả | |
|---|---|---|
| Luôn (mô phỏng 0 USD, `tools/do_sua_lich_v2.py`) | mọi tổ hợp × 8 kiểu hành động (~15.000 lần áp): **0 vi phạm** (phạm luật · điểm bỏ quay lại · điểm không chạm đổi chỗ · áp > 2), 0 lỗi chạy. Lần đầu bắt **2 lỗi thật**: điểm đã bỏ quay lại qua danh sách lấp (240 khung); "thêm" gần như luôn trượt (4 / 1.920) ⇒ đã sửa | ĐẠT |
| Q1 cờ tắt | chuỗi gửi model **228 / 228 giống byte** với `main` | ĐẠT |
| **Q5** an toàn (`tools/q5_sua_lich.py`) | 32 câu × 2, mỗi câu hỏi trong cuộc **đã có lịch** 3 ngày nhiều điểm: **0 / 64** thành lượt sửa, 0 câu ra hành động · 0,011 USD | ĐẠT |
| **Q3** quyết (`tools/q3_sua_lich.py`) | **CHẶN Ở NHÃN**: bộ chuỗi viết theo nội dung lịch của bộ xếp CŨ ⇒ với lịch bản 2 (khác điểm) nhãn đòi áp hành động mà luật đúng ra phải từ chối. Pilot S01 + S06: cơ chế chạy đúng (bỏ đúng điểm, thẻ chọn, bấm nút ⇒ thay đúng chỗ). A giao **C viết lại nhãn 10 + 5 kín** theo khung bản 2 ⇒ B chạy pass^2 | CHỜ |
| UI (`tools/pw_sua_lich.py`, chạy thật) | 1440 + 390: "Bỏ X" ⇒ "Đã bỏ X."; "Thay Y" ⇒ thẻ 3 điểm + Bỏ; Enter trên nút đầu ⇒ "Đã thay Y bằng …"; 0 lỗi console; 0 yêu cầu ra ngoài | ĐẠT |
| Độ trễ thêm | lần "hiểu ý" p50 **1,21 s** (64 lần, máy đang bận vì các lượt đo khác) — **chưa phải số chính**; đo lại ~10 lượt khi A báo máy rảnh | CHỜ |
| Test | `test_sua_lich_v2.py` (mới) + `test_len_ke_hoach_v2.py` + `test_cong_dot_1.py` 116 đạt; test dùng chung ghim cờ `sua_lich_v2` tắt | ĐẠT |

**Lỗi pilot bắt được, đã sửa** (`f2f874e`):
- tên ngắn không khớp ⇒ thêm khớp "đúng một điểm" + danh sách tên điểm trong tin nhắn hiểu ý;
- lượt bấm nút rơi về đường thường;
- câu sửa mà điểm không có trong lịch rơi về câu trả lời lạc đề.

Một lượt pilot gặp `APIError` của nhà cung cấp, ghi là quan sát.

**Tiền:** Q5 0,011 · pilot + Playwright 0,014 ⇒ **≈ 0,025 USD**.

## Bảng AI FDE — dòng cập nhật cho đổi thiết kế
| Mục | Hiện trạng | Khớp / lệch |
|---|---|---|
| Có cần model / khi nào gọi | Model chỉ hiểu câu ⇒ hành động có tên; gọi ở mọi lượt khi cuộc có lịch (cổng từ khoá đo trượt ⇒ bỏ). Áp, xếp, kiểm, chọn điểm thay: code | khớp (giá: +1 lần gọi suy luận thấp trong 30 phút sau khi có lịch — số trễ chờ đo) |
| Chữ người dùng là dữ liệu | Câu ⇒ enum hành động + tên khớp bảng bằng code; Q5 0 / 64 câu an toàn thành lượt sửa | khớp |

## Còn lại
- **Q3 pass^2** trên nhãn mới của C (10 đã thấy + 5 kín; B chạy kín, in số đếm).
- Đo độ trễ khi máy rảnh.
- C review cả nhánh.
- Bật cờ: A trình User, hoặc A bật nếu mọi sàn đạt.

## Sau review E (`e_review_sua_lich_v2.md`: changes_requested, 1 blocker · 1 major · 1 minor) — 13:18 14/11/2026, commit `2bc020d`
- **B-1 (blocker, an toàn):** câu vừa sửa lịch vừa khẩn cấp bị biến thành lượt sửa, mất phần khẩn cấp. Gốc: lần hiểu ý chạy trước định tuyến (nơi duy nhất nhận ra khẩn cấp), và Q5 chỉ có câu an toàn thuần nên không bắt được.
  - **Sửa:** hiểu ý và định tuyến chạy **song song**; định tuyến ra khẩn cấp ⇒ đường thường như `main`. Chọn cách này thay vì để model tự khai "khẩn cấp", vì luật nằm ở code + bộ định tuyến đã đo an toàn.
  - **Kiểm thật:** câu của E chạy 2 / 2 ⇒ 0 lượt sửa, log `emergency_by=router`.
  - **Còn:** câu trả lời của đường thường vẫn thiếu số 112–115. Đây là hành vi có sẵn trên `main` (E đo: 10 / 12 câu khẩn cấp bị từ chối — `e_kiem_khan_cap_main.md`) và là **giới hạn User đã quyết** (12/11: không làm dòng số khẩn cấp; A đính chính 14/11) ⇒ nhánh này không đổi; câu trộn đi đúng đường của câu khẩn cấp thuần.
  - **Q5 bổ sung:** 5–10 câu trộn do người khác B viết, chạy bằng `tools/q5b_tron.py`. Sàn: 0 câu thành lượt sửa (phần "có số khẩn cấp" không đo — giới hạn trên).
- **M-1:** lượt có "thay" không nói điểm ⇒ chỉ thẻ chọn; hành động khác vào "Chưa làm", không áp nửa chừng. Test cả hai thứ tự.
- **m-1:** dòng "Đang hiểu yêu cầu sửa lịch…" chỉ hiện ở lượt sửa. Độ trễ của câu không sửa vẫn có (chờ lần hiểu ý) — đo khi máy rảnh.
- **Thêm:** bước gộp trace của đường song song giữ số đếm `sua` cho log.
- **Kiểm sau sửa:**
  - 117 test đạt; mô phỏng 0 vi phạm.
  - E xác nhận đúng 2 câu B nhờ soi: đánh lại mã nguồn khi giữ câu cũ; lượt chỉ có thẻ chọn không ghi đè lịch.

## Q3 / Q5b trên nhãn mới của C — 13:55 14/11/2026
- **Nhãn:** C viết lại theo lịch bản 2 — `chuoi_da_thay.jsonl` md5 `2923d432da9b`, `chuoi_sealed.jsonl` `1165ecfa6367`. Mô phỏng của C: 10 / 10 · 5 / 5. Ngưỡng không đổi.
- **Lỗi công cụ đo C bắt** (trước lượt có phí): `cham_luot` đòi áp cả hành động nhãn ghi `khong_doi` ⇒ thêm `ky_cham` (luật A 06/11).
- **Q3 đã thấy lượt 1** (code `2bc020d`): pass^2 **7 / 10** (< 8). Ba chuỗi trượt đều do lần hiểu ý trả rỗng:
  - "dày lịch" không biết là `kham_pha`;
  - "bớt một chỗ ở ngày 2" — lời dặn "không đoán" làm model không dám chọn điểm;
  - "không cần ăn uống nữa, cho đi di tích" — trượt 1 / 2 lần.
- **Một vòng chỉnh lời dặn** (plan cho phép một vòng, commit `0501094`): thêm cách nói thường ngày cho kiểu đi / sở thích; cho chọn điểm theo ngày / buổi trong lịch hiện tại.

| Mã | Sau vòng chỉnh (`0501094`) | Sàn | |
|---|---|---|---|
| Q3 đã thấy | pass^2 **9 / 10** (S06 trượt 1 / 2 lần ở lượt phải ra thẻ chọn) | ≥ 8 / 10 | ĐẠT |
| Q3 kín (B chạy, chỉ in số đếm; thư mục kết quả đã xoá) | pass^2 **4 / 5** | ≥ 4 / 5 | ĐẠT |
| Q5 an toàn | **0 / 64** thành lượt sửa (trước vòng chỉnh cũng 0 / 64) | 0 | ĐẠT |
| Q5b câu trộn sửa + khẩn cấp (E viết, `q5b_cau_tron_e.jsonl` `ab1eab81e9a4`) | **0 / 16** cả trước và sau vòng chỉnh | 0 | ĐẠT |
| Khung lượt sửa hiện | p50 ≈ 2,0–2,2 s (máy còn lượt đo khác — chưa phải số độ trễ chính) | — | đo lại khi máy rảnh |

- **Tiền thật từ log:** server 0,222 USD (301 lượt: Q3 đã thấy ×2 lượt chạy, kín, Q5b ×2, Playwright, pilot) + Q5 ×2 0,026 ⇒ **≈ 0,25 USD**. Cao hơn ước 0,07 của plan, vì mỗi chuỗi có lượt xếp cả lịch và bộ đã thấy chạy hai lượt. Phiên không có trần cứng (User).
- **Còn:**
  - E kiểm vòng chỉnh lời dặn (đổi sau review);
  - đo độ trễ khi máy rảnh;
  - bật cờ: A trình User, hoặc A bật nếu mọi sàn đạt.

## E kiểm vòng chỉnh `0501094` — ready_for_user_confirmation
- E tính lại từ file: Q5 0 / 64, Q5b 0 / 16 khớp; lời dặn không chèn tên điểm; cờ tắt vẫn giống byte.
- **Minor theo dõi:**
  - (1) mẫu "Không cần X nữa, cho mình đi Y" khớp nhẹ với bộ đã thấy — bộ kín đạt đúng sàn 4 / 5;
  - (2) câu chỉ chỗ bằng ngày / buổi giờ để model chọn điểm bị bỏ ⇒ về sau có thể đưa thẻ chọn cho đúng nguyên tắc "code quyết".

## Độ trễ chính — phạm sàn sau khi bật, đã sửa (14:23 14/11/2026; nhánh `p9-sua-lich-tre` commit `80648f0`)
Đo bằng `data/len_ke_hoach_v2_2026-11-13/tools/do_tre_sua_lich.py`, máy rảnh, tuần tự. Ba nhóm:
- (A) câu thường, cuộc chưa có lịch;
- (B) câu thường, cuộc đã có lịch (biểu mẫu rồi câu);
- (C) lượt sửa.

| Nhóm | Trước sửa (`main` `e0cb02e`, n = 10): chữ đầu p50 / p95 · xong p50 / p95 | Sau sửa (n = 20, hai lượt gộp): chữ đầu p50 / p95 · xong p50 / p95 |
|---|---|---|
| A — chưa có lịch | 2,23 / 5,20 · 3,82 / 7,12 s | 2,22 / 4,04 · 3,30 / 6,91 s |
| B — đã có lịch | **4,17** / 7,16 · 5,32 / 8,72 s | **2,37** / 4,29 · 3,19 / 6,69 s |
| C — lượt sửa (khung hiện) | khung 2,28 / 3,62 · xong 2,90 / 6,47 s; sửa 10 / 10 | khung 2,15 / 2,53 · xong 2,49 / 5,86 s; sửa 20 / 20 |

- **Gốc:** đường trả lời thường ĐỢI lần hiểu ý + định tuyến xong mới chạy ⇒ +1,9 s chữ đầu, phạm sàn User đã chốt (p50 ≤ 3 s). A tắt tạm cờ trên `main`.
- **Sửa** (`_sua_song_song`):
  - đường thường (gồm #6) chạy NGAY, song song với hiểu ý + định tuyến; sự kiện giữ trong hàng đợi tới khi biết kết quả;
  - câu sửa (không khẩn cấp) ⇒ huỷ đường thường, ghi tiền phần bị huỷ (`usd_bo`, trung bình ≈ 0,0001 USD / lượt sửa); còn lại ⇒ xả hàng đợi + gộp trace;
  - khẩn cấp vẫn thắng; lượt bấm nút không chạy đường thường.
- **Sàn A đặt:** nhóm B chữ đầu p50 ≤ 3 s ⇒ **2,37 s ĐẠT**; không tệ hơn A quá +0,3 s ⇒ **+0,16 s ĐẠT** (n = 20).
  - **Ghi trung thực:** lượt đo đầu sau sửa (n = 10) ra **+0,31 s — vượt** ngưỡng phụ +0,3 s. B chạy thêm 10 lượt SAU khi thấy số đó rồi gộp (n = 20 ⇒ +0,16 s). Đây là "đo thêm tới khi đạt" — đúng ra phải ghi cỡ mẫu trước khi đo.
  - +0,3 s là ngưỡng phụ A đặt tạm; sàn chính (p50 ≤ 3 s) đạt ở cả hai lượt (2,29 s · 2,20 s). A chấp nhận vì sàn chính đạt và chênh cỡ nhiễu (A 14/11).
- **Test:** `test_sua_lich_v2.py`, `test_len_ke_hoach_v2.py`, `test_cong_dot_1.py`, `test_b6_tra_web.py`, `test_ngay_lich.py`, `test_toc_do_song_song.py` — 294 đạt.
- **Tiền đo độ trễ:** ≈ 0,08 USD (ba lượt × 30 câu).

## Đo lại với cỡ mẫu chốt trước + tiền + đệm (14:40 14/11/2026; nhánh `p9-sua-lich-tre`, `3aef0ca` đo · `c59e090` khoá đệm)
Sau sửa review (m-1 trạng thái chỉ hiện ở lượt sửa, m-2 dùng lại định tuyến của đường thường), B đo lại một lần, **n = 20 ghi trước khi chạy**, không đo thêm.

| Nhóm | Chữ đầu p50 / p95 | Ghi chú |
|---|---|---|
| A — chưa có lịch | 2,58 / 4,14 s | mốc |
| B — đã có lịch | 2,65 / 4,01 s | +0,07 s so với A; sàn 3 s ⇒ ĐẠT; ngưỡng phụ +0,3 s ⇒ ĐẠT |
| C — lượt sửa | khung 2,30 / 2,59 s | sửa được 20 / 20 |

(A và B chậm hơn lượt 14:23 ≈ 0,3 s ở cả hai nhóm — máy / API dao động; chênh B − A mới là số quyết.)

**Tiền / câu (trung bình, USD):** A 0,000456 · B 0,0007 (hiểu ý 0,000211 + định tuyến 0,000104 + trả lời 0,000386) · C ≈ 0,00035. Theo A: tiền không chặn ở Phase 9, chỉ là **mục theo dõi**.

**Đệm lời nhắc (prompt cache) cho lần hiểu ý** — lời dặn + khuôn đầu ra ≈ 1.244 token giống nhau mọi lượt:
- Thử 1: đưa phần cố định (danh sách tên điểm) lên đầu tin nhắn ⇒ cached_tokens **0**. Gốc: SDK tự sinh `prompt_cache_key` riêng mỗi lần chạy, nên OpenAI không ghép lượt này với lượt trước.
- Thử 2 (giữ nguyên chữ và thứ tự tin nhắn): khoá cố định `prompt_cache_key = "hue_sua_lich_v1"` qua `ModelSettings.extra_args` ⇒ lần 1 cached 0 / 1.620 token, **lần 2–6 cached 1.244**; tiền lần hiểu ý 0,00024 ⇒ ≈ 0,0001 USD.
- Đã đưa vào code `c59e090` (1 dòng); `test_sua_lich_v2.py` 8 đạt. **Chưa đo lại cả lượt B** — ước ≈ 0,00055 USD / câu; đo lần dùng thật kế tiếp.
- Khi nào sai: đệm OpenAI hết hạn sau vài phút không dùng ⇒ lượt đầu sau lúc vắng trả giá đầy đủ; đổi chữ lời dặn ⇒ đệm cũ mất (không sao, tự dựng lại).

**Tiền đo lượt này:** ≈ 0,05 USD (60 câu thật + 8 lần gọi thử đệm). Cờ trong worktree đã trả `false`, server 8899 đã tắt.
