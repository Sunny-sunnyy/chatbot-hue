# Review: "khoảng cách tính sẵn" (nhánh `p9-kc-tinh-san`)

Decision: **changes_requested** (1 major, 2 minor) — cờ đang TẮT nên nhánh không gây hại nếu merge, nhưng **chưa đủ để bật cờ**
Người kiểm: E (Claude Code)
Date: 18:27 16/11/2026
Bản được kiểm: `origin/p9-kc-tinh-san` `f2322fd` (code `50fbf4e`), so với `origin/main` `a63ed9b`
Plan: `docs/superpowers/plans/2026-11-17-khoang-cach-tinh-san-plan.md` sha `8f45c14cf9e2` (E tính lại từ file: khớp)
Implementation report: `report_agent/2026-11-12_ra_khoang_cach/c_kc_tinh_san_implementation.md`

## 1. Phạm vi đã review

Đọc exact diff 6 file (`settings.yaml`, `llm/assistant.py`, `llm/khoang_cach.py`, `tests/test_khoang_cach.py`, plan, report); `git diff --check` sạch;
không có thay đổi ngoài phạm vi. Chạy lại bộ dò của A, test file chạm, tính lại tiền từ log; tự viết 21 câu phá gọi thẳng hàm thuần (0 USD).
Không chạy lượt có phí, không mở server.

## 2. Findings

### M-1 (major) — hàm đọc tên ra cặp khi câu KHÔNG hỏi khoảng cách giữa hai điểm đó
- Vị trí: `backend/llm/khoang_cach.py` `tim_hai_diem` / `cap_tinh_san`.
- Yêu cầu bị ảnh hưởng: plan §3 "0 sai cặp" và §5 "mập mờ ⇒ ưu tiên `None` (đường cũ)"; luật bộ câu dò cho code đọc chữ người dùng (`Session_Prompt.md` §8).
- Bằng chứng: bộ câu phá của E `data/review_kc_tinh_san_2026-11-16/cau_pha.py` — **15 / 21 câu ra SAI** (bộ 32 câu của A: 0 sai — bộ đó không có các họ dưới):
  - **Họ A — có đủ hai tên bảng nhưng khoảng cách được hỏi là tới / từ một nơi thứ ba không có tên bảng** (8 / 8 sai): hai điểm "cách trung tâm"; đi từ ga /
    sân bay / khách sạn / "từ đây" / một thành phố khác tới một điểm trong khi câu có nhắc thêm điểm thứ hai; chuỗi ba nơi mà nơi thứ ba gõ tên trần
    (không có chữ "lăng" / "điện").
  - **Họ B — tên điểm nằm trong một tên riêng khác** (5 / 5 sai): "khách sạn <tên>", "cầu <tên>", "nhà hàng <tên>", "<tên> Plaza", địa danh tỉnh khác trùng một
    tên khác của điểm.
  - **Họ C — so sánh viết tách chữ** (1 / 3 sai): "có xa … hơn … không" (chữ "xa" và "hơn" không liền nhau).
- Tác động: ở các câu này code nối nguồn khoảng cách của một cặp người dùng không hỏi **và bỏ công cụ `khoang_cach` khỏi lượt** ⇒ model có sẵn một con số
  hợp lệ (bước kiểm số cho qua vì số nằm trong nguồn) để trả lời nhầm câu hỏi; đường cũ ở cùng câu thì model gửi mã `khac` ⇒ "chưa có số". Hỏi "từ khách sạn /
  ga / trung tâm tới X" là kiểu câu khoảng cách rất thường gặp của du khách. Mức hại thật (model có dùng nhầm số không) **chưa đo** — E không chạy lượt có phí.
- Tiêu chí đóng (chọn một, A quyết):
  (a) sửa hàm theo hướng dè dặt (ra `None`) rồi chạy lại: `cau_pha.py` **0 SAI** ở nhóm A / B / C, 5 câu nhóm D vẫn ra cặp (D4 xem m-1), bộ 32 câu của A vẫn 0 sai;
      báo số câu của lượt đo 16 câu còn đi đường nhanh (mô phỏng 0 USD là đủ, không cần lượt có phí mới nếu chuỗi gửi model của câu còn khớp không đổi).
      Gợi ý không bắt buộc: chỉ nhận khi phần chữ GIỮA hai tên là một từ nối ngắn thuộc danh sách đóng ("đến / tới / sang / ra / về / cách / –") và ngay trước tên
      không phải danh từ loại ("khách sạn / nhà hàng / quán / cầu / ga / bến"), phần còn lại của câu không có "trung tâm / khách sạn / sân bay / ga / đây / đó / rồi".
  (b) hoặc giữ code, chạy thật 15 câu SAI với cờ bật (≈ 0,006 USD), người không viết code đọc 100 % câu trả lời: 0 câu dùng số của cặp không được hỏi ⇒ ghi
      thành giới hạn. Còn câu dùng nhầm ⇒ quay về (a).

### m-1 (minor) — hướng đi ngược khi câu viết "đến B từ A"
Câu phá D4: ra (B, A) trong khi người dùng đi từ A. Bảng hai chiều lệch > 1 km ở 37 / 780 cặp (lớn nhất 5,3 km) ⇒ số có thể lệch và dòng nguồn ghi ngược
chiều. Đóng: chữ "từ" đứng ngay trước tên thứ hai ⇒ đảo cặp hoặc ra `None`; hoặc ghi giới hạn.

### m-2 (minor) — lệch plan chưa có test khoá
Report §2 khai lệch plan (không thêm `ten_khac` vào bảng, dùng `TEN_NGAN` trong code) — hợp lý, E đồng ý. Nhưng không có test nào khẳng định `TEN_NGAN` **không**
vào mô tả công cụ (`mo_ta_cong_cu`); hiện đúng nhờ đọc code. Không chặn.

Không có blocker. Độ đơn giản: 59 dòng hàm thuần + 24 dòng nối vào `assistant.py`, theo đúng mẫu "Lịch hệ thống" — tương xứng; không finding.

## 3. Cách người kiểm chạy lại thật

Worktree tách `origin/p9-kc-tinh-san` ở `/tmp/e_rvkc` (đã gỡ sau review), mọi lệnh từ `backend/`, `PYTHONPATH=$PWD`, `uv run --project /home/minhhieu/hue_rag`:
- `python <repo>/data/khoang_cach_2026-11-16/chay_bo_do_ten.py $PWD <repo>/data/khoang_cach_2026-11-16/bo_do_ten.jsonl`
- `HF_HUB_OFFLINE=1 python -m pytest tests/test_khoang_cach.py -q` (không khoá)
- `python ../scripts/dem_chat_metrics.py --log <repo>/data/khoang_cach_2026-11-16/application_8041_san.log --sha 50fbf4e`
- `python <repo>/data/review_kc_tinh_san_2026-11-16/cau_pha.py $PWD`

## 4. Kết quả quan sát

| Việc | Kết quả E thấy | So report |
|---|---|---|
| Bộ dò 32 câu của A | 31 đúng · 0 sai · 1 ra `None` (cặp bảng không có số) | khớp |
| `test_khoang_cach.py` | 77 passed, 15,2 s | khớp |
| Tiền theo sha `50fbf4e` | 18 lượt · 0,0131 USD; chữ đầu p50 1,84 s | khớp |
| Cờ tắt ⇒ chuỗi gửi model không đổi | Đọc diff: cờ tắt ⇒ `cap` luôn `None`; điều kiện mới ở `_lich_extra` (`trace.khoang_cach is None`) luôn đúng vì hàm này gọi một lần / lượt, trước lần gọi model đầu (2 chỗ gọi, đã đọc). Test có sẵn: "cờ bật + không khớp = cờ tắt" (16 ca). **Không có** test so thẳng bản cờ tắt với `main` — E không chạy Q1 228 câu | đạt theo đọc code |
| Bất biến E kiểm | Cờ bật, câu không có từ khoá khoảng cách ⇒ không bao giờ ra cặp (C2, C3, và ca "mở cửa mấy giờ" trong test) | đạt |
| Câu phá của E (21 câu) | 6 đúng · **15 SAI** · 0 `None` nhầm | bằng chứng mới của M-1 |

Chưa kiểm: test rộng (report ghi NOT RUN — làm ở commit cuối trước merge); lượt có phí; hành vi model trên các câu SAI.

## Vòng 2 — bản siết `a5562d2` (E, 18:35 16/11/2026): **ready_for_user_confirmation** (để merge với cờ TẮT; bật cờ là quyết định của A / User)

- Đọc diff `f2322fd..a5562d2` phần `backend/llm/khoang_cach.py` + test: hàm chỉ nhận dạng đóng "[từ / đi từ] A <từ nối trong danh sách> B <từ hỏi khoảng cách>"
  (và "A và / với B cách nhau…", "A có gần / xa B không"), đúng hai lần nhắc tên, câu có "hơn" ⇒ `None`. `assistant.py` không đổi so với vòng 1. `git diff --check` sạch.
  Các file khác trong diff là do gộp `main`.
- **M-1 đóng:** `cau_pha.py` 20 đúng · **0 SAI** · 1 về đường cũ (D4); bộ dò 32 câu của A 29 đúng · **0 SAI** · 3 về đường cũ — khớp số C báo.
- **m-1 đóng:** "Đến B từ A" ⇒ `None`. **m-2 đóng:** có test tên ngắn không vào mô tả công cụ.
- Bộ thêm DUY NHẤT sau bản sửa (luật bộ dò cho phép một bộ ≤ 20 câu; E chạy trước khi nhận tin "không soạn bộ mới" của A): `data/review_kc_tinh_san_2026-11-16/cau_pha_2.py`
  — 12 câu họ kề bên (tên trong tên riêng ở vị trí thứ hai, nơi thứ ba đứng đầu / ngay sau tên thứ hai) + 4 đối chứng dương: **16 đúng · 0 SAI**. E không soạn thêm.
- Test: `test_khoang_cach.py` + `test_b5_lich_trinh.py` 333 passed (không khoá, 26 s). Test rộng: E không chạy (C chạy một lần ở commit cuối trước merge).
- Giới hạn còn, đã ghi ở report §5 và E đồng ý ghi nhận: nơi thứ ba đứng SAU từ hỏi ("… bao xa, rồi sang … nữa?") vẫn ra cặp hai nơi đầu — nguồn đúng cho cặp đó,
  câu trả lời có thể thiếu chặng sau; số tốc độ (p50 1,80 s) đo trên `50fbf4e`, bản siết chỉ có mô phỏng 0 USD "vẫn 13 / 16 câu đi đường nhanh" (E không tính lại số này);
  hành vi model trên câu về đường cũ = như trước khi có nhánh.
