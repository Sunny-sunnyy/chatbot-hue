# "Khoảng cách tính sẵn" — implementation report (C, 18:21 16/11/2026)

Plan: `docs/superpowers/plans/2026-11-17-khoang-cach-tinh-san-plan.md` (A duyệt sha `8f45c14cf9e2`, mức nhẹ, trần 0,05 USD). Nhánh `p9-kc-tinh-san`, bản đo `50fbf4e`.
Cờ `khoang_cach_tinh_san` **TẮT** trong `settings.yaml` (bật là quyết định của A / User).

## 1. Đổi gì
- `backend/llm/khoang_cach.py`: `tim_hai_diem(cau, bang)` (hàm thuần: tên + tên khác của bảng, so nguyên cụm theo ranh giới chữ sau NFC + chữ thường, cụm dài
  trước, không chồng nhau; đúng 2 mã ⇒ cặp theo thứ tự xuất hiện) và `cap_tinh_san(cau, bang)` (câu ĐANG GÕ có từ khoá + không phải câu so sánh + ra cặp + bảng
  có số cho cặp).
- `backend/llm/assistant.py`: `_before_model` — cờ bật + ra cặp ⇒ `_nguon_khoang_cach_san` đăng nguồn khoảng cách (y như kết quả công cụ) và nối vào ngữ cảnh
  trước lần gọi model đầu; `_lich_extra` không đưa công cụ `khoang_cach` khi số đã tính sẵn (⇒ `max_turns` như lượt thường). Bước kiểm số sau khi sinh giữ nguyên.
  Log: mục `tools` có `khoang_cach_san` kèm hai mã điểm (không chữ người dùng).
- `settings.yaml`: cờ mới (tắt); cờ cần `khoang_cach` (không thì không khởi động).

## 2. Lệch plan (A đồng ý 16/11)
Plan ghi "thêm tên khác ngắn vào bảng điểm". **Không sửa bảng điểm**, vì `ten_khac` của bảng còn đi vào (a) mô tả công cụ gửi model và (b) bước kiểm câu mô tả
của lịch (câu nhắc tên điểm khác ⇒ bỏ câu) — thêm tên ngắn ở đó sẽ đổi hành vi lịch và chuỗi gửi model. Thay bằng: hàm đọc tên tự thêm dạng bỏ đuôi " Huế"
(cùng luật `lich_trinh.chuan_ten`) + một dict nhỏ `TEN_NGAN` trong `khoang_cach.py` chỉ dùng để đọc chữ người dùng (3 điểm, 5 tên). Hệ quả: cờ tắt ⇒ không
chuỗi nào gửi model đổi; không phải quét nhãn bộ đo theo `WORKFLOW.md` §3.4.
Luật thêm so với plan (đều theo hướng dè dặt, ra `None` = đường cũ): từ khoá phải nằm ở câu đang gõ (không tính câu liền trước); câu so sánh ("gần hơn / xa
nhất", hai tên chỉ nối bằng "hay / hoặc"); cặp bảng không có số; một cụm tên trỏ hai mã ⇒ bỏ cụm đó.

## 3. Kết quả so tiêu chí ghi trước
| Tiêu chí | Kết quả | Đạt |
|---|---|---|
| Bộ dò tên (32 câu, agent con của A soạn; 0 USD): 0 sai cặp | **31 đúng · 0 sai cặp · 1 ra None khi nhãn có cặp** (điểm không có toạ độ ⇒ bảng không có số ⇒ đường cũ) | PASS |
| Test: cờ bật + không khớp ⇒ giống byte bản cờ tắt (lượt đầu, có lịch sử, stream / không); khớp ⇒ ngữ cảnh có nguồn, không có công cụ; có ca đối chứng | `test_khoang_cach.py` 77 passed (có / không `--env-file`); ca đối chứng: cùng câu, cờ tính sẵn tắt ⇒ có công cụ + chưa có nguồn | PASS |
| Lượt có phí 16 câu (server tạm 8041, 1 lượt): đường nhanh chữ đầu p50 ≤ 3 s | **13 câu đường nhanh, p50 1,80 s** (1,44–2,31 s ở 11 câu; 2 câu > 3 s: 3,65 và 6,61 s) | PASS |
| 0 số sai, 0 sai cặp; đúng cặp ≥ 12 / 14 | đúng cặp **14 / 14**, số lạ 0, 13 / 13 câu đường nhanh có số km / phút trong câu trả lời, 0 câu bị rút lại | PASS |
| Nơi ngoài bảng ra số 0 / 2 | 0 / 2 (cả hai đi đường cũ, từ chối + mục web như trước) | PASS |
| An toàn 32: đếm câu chạm | 0 câu có từ khoá, 0 câu ra cặp ⇒ không lượt an toàn có phí | PASS |

Mốc so: đường công cụ lượt đo 16/11 chữ đầu p50 3,7 s / p95 6,2 s (14 câu; đọc từ log server). Lượt này đo chữ đầu **ở phía gọi** (gồm cả HTTP) nên
không thiên vị về phía nhanh; `dem_chat_metrics.py --sha 50fbf4e` (log server, 18 lượt gồm 1 câu thử + 1 câu "trước"): chữ đầu p50 1,84 s.
Câu đường cũ duy nhất trong bảng (câu hỏi tiếp "từ đó sang…"): 3,58 s — như mốc.
- Câu 6,61 s: câu hai ý (khoảng cách + nên đi buổi nào) — model tự tìm kho thêm cho ý thứ hai (4 lần gọi model); số khoảng cách vẫn đúng. Không do đường mới.
- Câu 3,65 s: 2 lần gọi model như các câu khác ⇒ dao động phía model / mạng (chưa chứng minh). Lúc đo, E có một lượt Playwright trên 8010 (A báo trước).
- 13 điểm ⇒ không báo p95 (không đủ mẫu); báo số câu vượt 3 s: 2 / 13.

## 3b. Sau review E (changes_requested: 1 major + 2 minor) — bản siết (C, 18:32 16/11/2026; A chọn hướng (a) và cho commit thêm)
- **M-1 (đúng):** bộ câu phá của E (21 câu, 0 USD) trên bản `50fbf4e`: **15 / 21 ra SAI** — có đủ hai tên bảng nhưng khoảng cách được hỏi là tới / từ nơi thứ ba
  không có tên bảng; tên điểm nằm trong tên riêng khác; so sánh viết kiểu khác. Bộ dò 32 câu soạn trước không có ba họ này.
- **Sửa:** `tim_hai_diem` chỉ nhận câu **đúng dạng** — đúng hai lần nhắc tên; chữ TRƯỚC tên thứ nhất ∈ danh sách đóng (rỗng, "từ", "đi từ"); chữ GIỮA hai tên ∈
  danh sách từ nối đóng; ngay SAU tên thứ hai phải là từ hỏi khoảng cách (với "và / với": phải là "cách nhau / gần nhau…"). Câu viết kiểu khác ⇒ None ⇒ đường cũ.
  m-1: "Đến B từ A" ⇒ None (không đoán chiều). m-2: thêm test khoá tên gõ tắt không vào mô tả công cụ. Code đường nhanh không đổi, chỉ đổi điều kiện vào.
- **Kết quả bản siết (0 USD):** câu phá của E **20 đúng · 0 SAI · 1 về đường cũ** (câu "Đến B từ A"); bộ dò 32 câu **29 đúng · 0 SAI · 3 về đường cũ** (thêm 2 câu có
  mệnh đề dẫn trước tên); bộ đo 16 câu: mô phỏng **vẫn 13 câu đường nhanh**, đúng cặp ⇒ không chạy lại lượt có phí (số tốc độ ở mục 3 là của `50fbf4e`, cùng
  code đường nhanh). `test_khoang_cach.py` 88 passed; `test_b5_lich_trinh.py` + file này 322 passed sau khi gộp main `6cf7935` (trước bản siết).
- Luật dừng (`Session_Prompt.md` §8): 0 câu ra sai trên hai bộ đã ghi ⇒ dừng, không mở vòng nữa.
- Test rộng trên `f2322fd`: 1265 passed · 1 failed — test đọc `settings.yaml` thật không tự tắt cờ bản đồ (main vừa bật), A đã sửa trên main `6cf7935`.

## 3c. Đo lại trên bản cuối đang chạy (C, 20:49 16/11/2026; A giao sau khi bật cờ — số ở mục 3 là của bản đầu)
Server tạm 8041 từ worktree main `1e45a78` (cờ bật), cùng 16 câu, một lượt, thử 1 câu trước (câu đầu sau khởi động 4,38 s — không tính).
- Đường nhanh 13 câu: chữ đầu (phía gọi) **p50 1,87 s**; 2 / 13 câu > 3 s (3,93 s — 2 lần gọi model; 4,03 s — câu hai ý, 3 lần gọi). Đường cũ trong bảng: 3,98 s.
- Đúng cặp 14 / 14 · số lạ 0 · 13 / 13 câu đường nhanh có số · ngoài bảng ra số 0 / 2 ⇒ **PASS** mọi tiêu chí của mục 3 trên bản cuối.
- Tiền 0,0122 USD (`dem_chat_metrics.py --sha 1e45a78`, 18 lượt); trung vị 0,00041 USD / câu đường nhanh, 12 / 13 câu < 0,0005 (câu còn lại 0,00054).
- Kết quả: `data/khoang_cach_2026-11-16/do_san_r1_ban_cuoi_1e45a78.json` (bản đầu: `do_san_r1_ban_dau_50fbf4e.json`), log `application_8041_san_ban_cuoi.log`.
- Tổng tiền cả việc: 0,0131 + 0,0122 = **0,0253 USD** (trần plan 0,05).

## 3d. Hai điều E thấy khi chạy thử hướng dẫn trên server đang chạy (C, 20:56 16/11/2026; 0 USD)
- **Ghi chú "chưa tính kẹt xe" vắng ở câu trả lời.** Đếm từ 4 lượt đo đã có (chữ "kẹt xe / dừng nghỉ" trong câu trả lời): đường tính sẵn 9 / 13 (bản cuối) + 7 / 13
  (bản đầu) = 16 / 26; đường công cụ 16/11 chiều 9 / 13 + 8 / 13 = 17 / 26 ⇒ hai đường như nhau, model bỏ ghi chú ở ~35 % câu — không do đường mới, nhưng ghi chú
  là phần bắt buộc đi cùng số ước ⇒ chuyển cho code (A quyết). **Sửa (nhánh `p9-kc-ghi-chu`):** `assistant.set_notice` — câu trả lời trích nguồn khoảng cách mà chữ
  không có "kẹt xe" ⇒ nối `kc.CAU_GHI_CHU` vào dòng cố định dưới câu trả lời (sự kiện `notice` sẵn có; đứng trước dòng "có thể đã thay đổi" nếu có cả hai,
  cùng một đoạn). Không đổi chuỗi gửi model, không đổi chữ model. Test tất định (đường công cụ + đường tính sẵn, stream / không; model đã ghi ⇒ không lặp;
  không trích nguồn khoảng cách ⇒ không nối): `test_khoang_cach.py` 101 passed. Giới hạn: model viết ý đó bằng chữ khác ("chưa tính tắc đường") ⇒ có thể lặp ý.
- **Câu "…bao xa, rồi ghé <khách sạn> nữa?" từ chối 1 / 2 lần.** Đọc sổ vết hai lượt: trình tự giống hệt tới lần viết cuối (nguồn tính sẵn của chặng đầu có trong
  ngữ cảnh; model tự tìm kho 2 lần cho chặng sau, không thấy); lượt từ chối là do chính model viết câu từ chối chuẩn (không phải bước kiểm số rút câu, không
  phải xin công cụ đã ẩn). Gốc: bộ dò "câu nhiều ý" không tách dạng câu này ⇒ lời dặn thường "thiếu ⇒ từ chối cả câu" — **giới hạn câu hai ý đã ghi 14/11**,
  không do đường tính sẵn (suy từ code + bản ghi; đường công cụ tới cùng lần viết đó với cùng nguồn). A quyết: ghi giới hạn, không mở rộng bộ dò câu nhiều ý.

 (số đo thật)
- Tiền: **0,0131 USD** (`scripts/dem_chat_metrics.py --log <log 8041> --sha 50fbf4e`: 18 lượt = 1 câu thử + 16 câu + 1 câu "trước"). Trần 0,05. Chưa ai tính lại.
- Mỗi câu đường nhanh ≈ 0,0004 USD (đường công cụ 16/11 ≈ 0,0006–0,0008).
- Thời gian: pytest file chạm 14,3 s; bộ dò < 5 s; lượt đo 16 câu ≈ 2 phút. Test rộng: NOT RUN (làm một lần ở commit cuối trước merge).

## 5. Giới hạn đã biết
- **Dạng câu ngoài danh sách đóng** (có mệnh đề dẫn trước tên, từ nối lạ, "Đến B từ A", "khoảng cách giữa A và B là bao nhiêu") ⇒ về đường cũ: đúng nhưng chậm như trước. Đếm trên các bộ: 3 / 19 câu có nhãn cặp của bộ dò, 1 / 5 của bộ câu phá, 0 / 13 của bộ đo.
- Nơi thứ ba nằm SAU từ hỏi ("Từ A đến B bao xa, rồi sang C nữa?") mà C không phải tên code đọc được (C là tên trong bảng ⇒ ba tên ⇒ None; sửa theo kiểm độc lập bài 14) ⇒ vẫn ra cặp (A, B): số đúng cho chặng đầu, chưa trả lời hết câu.
- Câu hỏi tiếp không nêu đủ hai tên ("từ đó sang…") và mọi câu ngoài bảng vẫn đi đường cũ (chậm như trước).
- Câu nhắc 2 nơi, có từ khoá, mà hỏi thêm việc khác ⇒ nguồn khoảng cách đúng cặp; model có thể tìm kho thêm cho ý kia (chậm hơn, như câu 6,61 s).
- Tên điểm viết không dấu / sai chính tả ⇒ không khớp ⇒ đường cũ.

## 6. Chạy lại
- Bộ dò (0 USD), từ `backend/` của nhánh: `PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python <repo>/data/khoang_cach_2026-11-16/chay_bo_do_ten.py $PWD <repo>/data/khoang_cach_2026-11-16/bo_do_ten.jsonl` (thoát 1 nếu có câu SAI).
- Lượt đo: bật tạm cờ trong worktree, server `uvicorn api.app:app --port 8041`, rồi `… python <repo>/data/khoang_cach_2026-11-16/do_san.py http://127.0.0.1:8041 $PWD/logs/application.log` (`--mo-phong` 0 USD; `--chi 0` thử một câu). Kết quả: `data/khoang_cach_2026-11-16/do_san_r1.json`, log `application_8041_san.log` (private).

**Giải thích ngắn:** với câu hỏi "từ A đến B bao xa" mà code tự đọc được đúng hai tên điểm, code tra bảng ngay và đưa số cho model viết luôn, thay vì chờ
model gọi công cụ rồi mới viết — bớt một lần gọi model, chữ đầu từ khoảng 3,7 s xuống khoảng 1,8 s. Câu nào code không chắc thì vẫn đi đường cũ.
