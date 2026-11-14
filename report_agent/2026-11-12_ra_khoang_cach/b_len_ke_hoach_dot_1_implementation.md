# Implementation Report: Phase 9 — "Lên kế hoạch" đợt 1 (khung lịch tốt + biểu mẫu đủ)

Người làm: B (Claude Code) · viết 21:19 13/11/2026 (`date`) · nhánh `p9-len-ke-hoach-v2`, head `49daaa7` (đã push, rebase lên `main` `0d4ee6e`) · cờ `assistant.len_ke_hoach_v2` **TẮT**
Căn cứ: plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md` bản 3 (A duyệt) · spec `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` bản 3.3 · bộ đo của E `data/phase_9/lich_trinh/bo_do_v2/` (mã băm khớp plan §5).
Repo public: tên điểm, bảng điểm, câu model, lịch sinh ra nằm ở `data/` (private); report chỉ ghi số đếm + đường dẫn.

## 0. Kết luận

**NGHIỆM THU ĐỢT 1: TRƯỢT — không bật cờ** (A quyết 13/11: trượt sau vòng chỉnh duy nhất ⇒ không bật, không chỉnh thêm vòng này). E review: ready cho kết luận này (`e_review_len_ke_hoach_dot_1.md`).

| Tiêu chí ghi trước (plan §5) | Kết quả | |
|---|---|---|
| Mô phỏng 3.840 khung: mọi "Luôn" của (b), (d), (e) | 0 lỗi khung trên 960 + 3.840 + 2.400 khung (7 thứ trong tuần) | ĐẠT |
| Sàn mô phỏng: kiểu đi ≥ 70 % · bậc thang ≥ 50 % · sở thích ≥ 50 % · ngày đi ≥ 60 % · buổi tối ≥ 80 % · điểm không bao giờ xếp ≤ 3 | 79 % · 56 % · 50 % (thấp nhất) · 100 % · 100 % · 1 | ĐẠT (xem §4.1 về biên) |
| Bộ 20 yêu cầu: 20 / 20 đủ khung, 0 từ chối | 20 / 20 thành công, có đủ khung, ý 1–6 của định nghĩa chấm đúng 20 / 20 (code chấm), 0 số tiền | ĐẠT |
| ≤ 1 câu dự phòng / lịch ở ≥ 18 / 20 | lượt 1: **16 / 20** · lượt 2 (sau vòng chỉnh): **17 / 20** | **TRƯỢT** |
| Không lịch nào > 30 % câu dự phòng | lượt 1: 2 lịch · lượt 2: **1 lịch** (33 %) | **TRƯỢT** |
| `lich_khung` ≤ 1 giây | trung vị 236 ms; **1 / 20 = 1,27 s** (lượt có dự báo khi bộ đệm thời tiết còn lạnh) | **TRƯỢT** (1 / 20) |
| Đủ câu: trung vị không chậm hơn mốc `main` cùng buổi quá 2 s | 5,43 s ↔ mốc 5,07 s (+0,36 s) | ĐẠT |
| Lượt dự báo lạnh ≤ mốc + 4 s (báo riêng) | đủ câu 5,6 s (lượt 2) ≤ 9,07 s | ĐẠT |
| Bộ quyết 12 ×2, hai người chấm | **CHƯA CHẠY — bộ chưa ai mở, để dành** (A quyết: kết quả không đổi được quyết định vòng này; mở ra thì mất bộ duy nhất chưa ai thấy, cần nhất ở lượt sau khi sửa gốc lỗi) | NOT RUN |
| Playwright 2 khổ màn (nghiệm thu) | **NOT RUN** (A quyết dời sang lượt nghiệm thu sau). Playwright bước (a) đã chạy, đạt (§3.1) | NOT RUN |
| Review cả nhánh | chưa — chờ A giao | NOT RUN |

**Gốc lỗi của phần trượt (quan sát + đọc tay):** gần như mọi câu dự phòng là **câu rỗng** model trả khi đoạn kho code chọn cho điểm đó "không có gì để viết" (lời dặn cho phép, đúng nguyên tắc N3 "nói thật khi thiếu dữ liệu"). Câu rỗng dồn vào một nhóm nhỏ điểm có bài mỏng / chung file / không có bài riêng — **không** do model hay luật xếp. Danh sách điểm: `data/len_ke_hoach_v2_2026-11-13/do_doan/`. Hướng sửa gốc (vòng mới, A hỏi User): cột "đoạn mô tả" chọn tay trong bảng điểm (§6).

**Tiền:** cả đợt ≈ **0,037 USD / trần 0,20** (thử sớm 0,0026 · mốc `main` 0,0089 + một lượt dở 0,0065 · bộ 20 lượt 1 ≈ 0,0096 (gồm 0,0007 của 3 yêu cầu chạy trước khi sửa lỗi `so_thich: []`) · lượt 2 0,0081). Số từ dòng `chat_metrics` (`tools/tien_log.py`).

## 1. Phạm vi

Đã làm đủ 5 bước (a)–(e) của plan, sau **một cờ** (mặc định tắt). Cờ tắt ⇒ chuỗi gửi model giống byte `main` (Q1 228 / 228, đo lại sau mỗi lần chạm phần dựng chuỗi và sau rebase).
Không làm (đúng plan): ảnh, bản đồ mới, ăn uống, lưu trú, đổi đường câu tự do, đổi lời dặn trợ lý chat, đổi kho / chỉ mục.

**Lệch nhỏ so với plan (B tự quyết trong phạm vi, A đã biết):**
- Một nhánh, mỗi bước một commit, một review cả nhánh (plan ghi "mỗi bước một nhánh nhỏ") — vòng tự soi 1 A chốt.
- Bộ xếp mới ở module riêng `backend/llm/lich_trinh_v2.py`; lượt bản 2 ở `backend/llm/len_ke_hoach.py` (bộ xếp cũ + đường cũ không sửa).
- Bước (a): ẩn `kieu_di` (bộ xếp cũ đổi khung 0 / 120) + `ngay_di` (chưa dùng); thêm `so_thich_toi_da` cạnh `so_ngay_toi_da` (A đồng ý). Giới hạn 4 ngày / 1 sở thích dời tới (c) (khi bộ xếp mới nối vào đường gọi model) thay vì "sau (b)".
- Một bảng `diem_v8.json` cho cả đợt (bản đề xuất đã có sẵn cột v9) — không tách v9.
- Hai cột mới B thêm vào bảng ở (e) + nghiệm thu: `gio_mo` (khung giờ có cấu trúc, dựng từ cột chữ, căn cứ từng dòng ở `gio_mo_can_cu`) và `dong_cua_thu` (thứ đóng cửa của điểm ban ngày). Đưa User xem cùng D4.
- `context_builder.build` thêm tham số tuỳ chọn `max_documents` (mặc định như cũ) — lịch bản 2 cần một đoạn mỗi điểm (tối đa 25), trần 10 đoạn của settings cắt mất ngày (bắt được ở test bước (e)).

## 2. Thay đổi chính (luồng)

```
biểu mẫu 4 nhóm (pages.jsx, chỉ ô trong /api/tinh_nang.o_hien)
  → POST /api/chat[/stream] {bieu_mau, truong mới}  (chat.py: giá trị mới chỉ nhận khi cờ bật + lượt biểu mẫu; sai ⇒ đúng 422 như thân sai khuôn)
  → len_ke_hoach.chuan_bi: xep_v2 (luật 5b: hạn chế > giờ mở cửa / thứ / mùa > cụm > ưu tiên > mưa > sở thích > kiểu đi; tối chọn SAU)
       + một đoạn kho / điểm (_lay_nguon_lich, luật đoạn tả điểm ở vòng chỉnh) + dự báo (chỉ khi có ngày trong 7 ngày tới)
  → sự kiện lich_khung (TRƯỚC lần gọi model)
  → một lần gọi lich_v2_agent (không công cụ, suy luận low) ⇒ {cau: [{id_muc, cau}]}
  → kiểm TỪNG câu (giờ / thời lượng / tiền / link / tên điểm khác / mã ngoài nguồn / rỗng) ⇒ lỗi ⇒ câu dự phòng riêng mục đó; model hỏng ⇒ lịch vẫn đủ
  → lich_cau* → lich_xong {so_cau_du_phong} → một delta chữ thuần (lịch sử, nút chép, giao diện cũ) → sources → lich_trinh {phien_ban: 2, lich, cau} → done
giao diện: thẻ LichV2 vẽ TỪ KHUNG, câu đổ vào theo id_muc; nút Sửa điền lại đúng giá trị đã gửi
```

File: `backend/llm/hoi_lai.py` (hợp đồng trường) · `lich_trinh_v2.py` (bảng, bộ xếp, kiểm khung, khuôn `lich`, kiểm câu, ghép chữ, bộ bóc mảng khi stream) · `len_ke_hoach.py` (lượt bản 2) · `assistant.py` (cờ, rẽ nhánh, tham số mới của `_lay_nguon_lich`) · `generator_openai_full_corpus.py` (`lich_v2_agent`) · `full_corpus_prompt.py` (`LICH_V2_LOI_DAN` = khung của C, không sửa chữ) · `api/routes/chat.py`, `cong.py` · `retrieval/full_corpus_context.py` · `config/settings.yaml` · `frontend/src/pages.jsx`, `chat.jsx`, `App.jsx`, `markdown.js`, `index.css` · test `backend/tests/test_len_ke_hoach_v2.py` (mới) + ghim cờ trong `test_cong_dot_1.py`, `test_b5_lich_trinh.py`.
Dữ liệu (private): `data/phase_9/lich_trinh/diem_v8.json` md5 `2930c675e875`; danh sách chừa Docker `data/phase_12/deploy_nhap/dung_dockerignore.py` thêm bảng này.

## 3. Cách đã chạy thật (thời gian đo bằng số thật)

- Test file mới: `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_len_ke_hoach_v2.py -q` — **78 đạt** (~15 s; gồm mô phỏng 960 + 3.840 khung chạy trong pytest).
- Test file chạm cờ, có và không `--env-file`, cả khi cờ **bật** tạm trong `settings.yaml` (bắt 2 test cũ đọc cờ thật — đã ghim cờ trong test).
- Test rộng có khoá (bỏ `test_phase6_live_smoke.py` — lượt gọi thật): **930 / 930 đạt** (3 phút 45) trên `d29828d`; head `49daaa7`: 932 / 932 (§3.2).
- Q1 (`data/phase_9/b2_chay/tools/capture_all.py`, 0 USD): **228 / 228 giống byte** `main` ↔ nhánh ở (a), (b), (c), sau rebase (so `main` `0d4ee6e`) và sau vòng chỉnh. ~40 s mỗi lần.
- Mô phỏng cũ `mo_phong_v8.py` cấu hình A: `kiem_khung` cũ 0 / 360 (bộ xếp cũ không bị chạm).

### 3.1 Playwright bước (a) (cờ bật tạm, server 8891 không khoá, yêu cầu `/api/chat*` chặn ở trình duyệt)
`data/len_ke_hoach_v2_2026-11-13/tools/pw_bieu_mau_a.py` — 1440 + 390: ô ẩn không có trong DOM; điền + gửi chỉ bằng bàn phím; `truong` gửi đúng hợp đồng; 0 lỗi console — ĐẠT. (Biểu mẫu sau (c)–(e) có thêm ô kiểu đi + ngày đi: **chưa Playwright** — để lượt nghiệm thu sau.)

### 3.2 Test rộng trên head cuối
Head `49daaa7`, có khoá, bỏ `test_phase6_live_smoke.py`: **932 / 932 đạt** (3 phút 54).

### 3.3 Lượt thử có phí sớm (bước (c), ≤ 0,005 USD)
`tools/thu_som_c.py` — 6 khung, đường stream thật của lõi: **0,00264 USD**; model trả 38 / 38 mục, 0 thiếu / lặp / id lạ, đúng thứ tự 6 / 6; câu dự phòng 2 / 38 (câu rỗng); đọc tay 38 câu: **0 câu bị thay nhầm** vì luật "tên điểm khác", 0 câu lọt giờ / tiền / link / tên điểm khác; khung hiện 49–360 ms. D3 không chạm ⇒ giữ nguyên chữ lời dặn. Chạy 0 USD trước bằng khoá giả (đường "model hỏng": lịch vẫn đủ khung, mọi mục dự phòng) — đạt.

### 3.4 Nghiệm thu (C / E dừng việc nặng trong lúc đo)
- Mốc `main` cùng buổi: server `main` 8892, 20 yêu cầu của E đổi về trường biểu mẫu cũ (`doi_sang_cu`; "5 ngày" ⇒ "từ 4 ngày" vì biểu mẫu cũ không có): `tools/nghiem_thu.py moc` ⇒ cả câu trung vị **5,07 s**, chữ đầu 2,65 s, 20 / 20 thành công.
- Bản 2: server nhánh 8893 (cờ bật tạm trong worktree, không commit), `tools/nghiem_thu.py v2` ⇒ `nghiem_thu/v2_20/` (lượt 1), `nghiem_thu/v2_20_luot2/` (lượt 2). Ngày đi đổi từ `kieu_ngay` đúng bảng của `dinh_nghia_cham.md`; ý 1–6 + hai điều kiện loại ngay chấm bằng code; ý 3 theo cặp bằng khung "anh em" 0 USD.

## 4. Kết quả quan sát

### 4.1 Mô phỏng 0 USD (bảng v8 cuối)
| Sàn / bất biến | Số | Ghi chú |
|---|---|---|
| Lỗi khung (`kiem_khung_v2` độc lập với bộ xếp) | 0 / 960 · 0 / 3.840 · 0 / 2.400 | gồm giờ trong giờ mở cửa, đúng thứ, 0 điểm tạm dừng mùa trong tháng dừng |
| Ưu tiên số 1 của mỗi sở thích có mặt | 100 % (trừ cụm xa < 3 ngày, điểm tạm dừng có ghi chú) | |
| Kiểu đi: 3 khung khác nhau | 63 / 80 = **79 %** (≥ 70) | 81 % trước khi có giờ mở cửa |
| Bậc thang giảm khi có nhóm hạn chế | 402 / 720 = **56 %** (≥ 50) — thước: mọi cặp; chỉ tính cặp có điểm nhiều bậc thì cao hơn (C tính lại ở (b): 76 %) | |
| Sở thích ≥ 50 % suất sáng / chiều của **từng** lịch 2 ngày | thấp nhất **50 %** (chụp ảnh, lễ hội – nghệ thuật) | **không có biên** — đổi bảng là có thể rơi; test khoá danh sách ô ẩn khớp số này. Lễ hội: 43 % trước khi A cho gắn nhãn cho một điểm có căn cứ kho (gắn SAU khi thấy sàn trượt) |
| Ngày đi: khung hoặc ghi chú khác (mùa khô giữa tuần ↔ mùa mưa cuối tuần) | **100 %** (≥ 60) | riêng khung khác chỉ 19 % — phần lớn nhờ dòng nhắc mùa mưa |
| Số tối có hoạt động (không tính ngày cụm xa) | **100 %** (≥ 80) | giới hạn đã biết: ít hoạt động ⇒ lặp có nhãn |
| Điểm ban ngày không bao giờ xếp | 1 (≤ 3) | một lăng xa, cụm chỉ kề 2 cụm |

Lỗi luật thật mô phỏng bắt được ở (b), đã sửa + test: điểm thêm của buổi sáng chiếm suất cụm của điểm ưu tiên buổi chiều; điểm ưu tiên cụm xa (bị loại khi < 3 ngày) vẫn giữ chỗ khi xen kẽ hai sở thích. C tính lại 4 sàn (b) độc lập: khớp (`c_so_moc_buoc_b.md`).

### 4.2 Bộ 20 yêu cầu thật
| | Lượt 1 | Lượt 2 (sau vòng chỉnh) |
|---|---|---|
| Thành công, đủ khung | 20 / 20 | 20 / 20 |
| Ý 1–6 (code) | 20 / 20 | 20 / 20 |
| Lịch ≤ 1 câu dự phòng | 16 / 20 | **17 / 20** |
| Lịch > 30 % câu dự phòng | 2 (một do `ModelBehaviorError` — đầu ra sai khuôn, cả lịch dùng câu dự phòng, lịch vẫn đủ) | **1** (2 / 6) |
| Khung hiện: trung vị · chậm nhất | 237 ms · 1.262 ms (lượt dự báo lạnh) | 236 ms · 1.266 ms (cùng ca) |
| Đủ câu trung vị (mốc `main` 5,07 s) | 5,17 s | 5,43 s |
| USD | 0,0096 | 0,0081 |

**Ghi rõ:** 20 yêu cầu đã được thấy trước khi chỉnh ⇒ số lượt 2 là số SAU khi chỉnh theo chính bộ đó; bộ quyết 12 (chưa ai mở) mới là bằng chứng không bị nắn — chưa chạy.

**Vòng chỉnh (a) (A chọn, plan cho tối đa một vòng):** lịch bản 2 chọn đoạn bằng câu tìm "<tên điểm> tổng quan kiến trúc cảnh quan", lấy đoạn xếp hạng cao nhất cùng file **nếu đoạn đó nhắc tên điểm**; không ⇒ luật cũ. Đọc tay 7 điểm hay rỗng (0 USD, `do_doan/so_sanh.json`, `bien_the_34.json`): 4 / 7 chuyển sang đoạn tả điểm và hết câu rỗng ở lượt 2; 1 điểm kho không có bài riêng ⇒ không sửa được. Ở lượt 2 câu rỗng chuyển sang dồn vào 6 điểm khác (danh sách ở `data/`).

**Lỗi bắt được khi nghiệm thu, đã sửa trước lượt tính số** (mỗi lỗi một test): (1) đọc `dinh_nghia_cham.md` trước khi chạy thấy code thiếu 3 dòng ghi chú bộ đo đòi (bậc thang cho nhóm hạn chế · "giữ mức nhẹ nhàng" · nhãn "kiểm lịch diễn" khi không ngày); (2) một điểm đóng thứ Hai chưa mã hoá ⇒ cột `dong_cua_thu`; (3) hợp đồng trường không nhận `so_thich: []` (spec: "danh sách ≤ 2") — 3 yêu cầu đầu chạy trước khi sửa đã bỏ, chạy lại cả 20; (4) 2 test cũ đọc cờ thật của `settings.yaml` (lộ khi bật cờ tạm) ⇒ ghim cờ trong test.

## 4b. Ca kiểm phụ của E (báo riêng — không đổi kết luận §0, không cộng vào luật đạt)

Bộ `data/phase_9/lich_trinh/bo_do_v2/ca_phu_13_11.jsonl` (sha256 `223b8768fa68`, cách chấm `ca_phu_13_11.md`) — hai lỗi đã thấy ở lượt thử TRIPO vòng 6. Chạy 0 USD
trên khung do code dựng (`xep_v2` + `kiem_khung_v2`, head `49daaa7`, bảng `2930c675e875`); kết quả `data/len_ke_hoach_v2_2026-11-13/ca_phu_ket_qua.txt`.

| Nhóm | Kỳ vọng | Kết quả |
|---|---|---|
| Điểm tạm dừng theo mùa, 4 lịch có ngày đi tháng 11 / 12 / 1 / 2 | điểm đó xếp 0 lần | **0 / 0 / 0 / 0 — đạt**; 0 lỗi khung |
| Đối chứng mùa khô (tháng 4) | chỉ báo số lần | được xếp 1 lần (ngày 2) — luật không loại nhầm ngoài mùa |
| 4 cặp "nhẹ nhàng" (thong thả) ↔ "khám phá nhiều" (dày), cùng ô khác | bản DÀY nhiều điểm tham quan hơn hẳn | số điểm tham quan sáng + chiều, viết **thong thả → dày**: D1 4 → 8 · D2 6 → 11 · D3 2 → 3 — **dày nhiều hơn, đúng chiều, đạt** · D4 6 ↔ 6 **không khác**: cặp D4 có trẻ em ⇒ spec 3.1 / 5c.3 cho nhóm hạn chế trần luôn là "nhẹ nhàng" (lịch có dòng ghi chú nói vậy) — đúng luật, không phải lỗi |

Ghi chú `tam_dung_mua` **không** có ở 4 lịch mùa mưa: code chỉ nối ghi chú này khi điểm bị loại là **điểm ưu tiên** của sở thích đã chọn (spec 5c.2 (i)); điểm của ca này
không nằm trong danh sách ưu tiên nên bị loại im lặng. E ghi mục này "chỉ báo". **Không sửa vòng này** (A 13/11) — xem "việc sau" ở §6.

## 5. Lỗi và giới hạn

- **Trượt sàn câu dự phòng** (§0) — gốc là đoạn kho từng điểm. Không bật cờ.
- **Khung > 1 s ở lượt có dự báo lạnh** (1 / 20) — **User quyết 13/11 (qua A): NHẬN GIỚI HẠN**, không sửa (người dùng không cảm nhận khác 1 s): code chờ dự báo rồi mới xếp (ngày mưa đổi thứ tự điểm). Chỉ lượt đầu mỗi 30 phút (cache); lượt nóng ≤ 0,45 s. Cách sửa (chưa làm, A trình User ở D4): (i) gửi khung xếp **không** dự báo trước, rồi gửi lại khung nếu ngày mưa làm đổi thứ tự (~0,5 ngày, cần giao diện chịu được khung đổi) · (ii) làm ấm bộ đệm dự báo khi server khởi động + mỗi 30 phút (~1–2 giờ, thêm một tác vụ nền gọi mạng).
- `ModelBehaviorError` 1 / 40 lượt bản 2 (lượt 1) — lịch vẫn đủ khung; lần gọi lỗi không có số token ⇒ USD của lượt đó không đếm được (như đường cũ).
- Sàn sở thích đứng đúng 50 % ở 2 loại — không có biên.
- Buổi tối ít đa dạng (kho ít hoạt động có lịch cố định) ⇒ lặp hoạt động diễn mọi tối, có nhãn.
- `gio_mo` của một điểm biểu diễn là cách B mô hình hoá (lần ghé bắt đầu đúng giờ suất diễn) — cần User xem ở D4.
- Đường câu tự do (chat) vẫn dùng bảng + luật cũ (đúng plan).
- Chưa chạy: bộ quyết 12 ×2, Playwright nghiệm thu, review cả nhánh, ca kiểm phụ của E (`ca_phu_13_11.jsonl`, 0 USD — chạy được ngay).

## 6. Bàn giao cho người kiểm / việc kế

- Đọc trước: §0, §4.2; rồi `backend/llm/lich_trinh_v2.py` (luật xếp — plan dặn review riêng) và `backend/llm/len_ke_hoach.py`.
- Chạy lại 0 USD: `test_len_ke_hoach_v2.py`; Q1; `tools/mo_phong_b.py`.
- Việc kế (A giao, 0 USD, KHÔNG nối code): bảng đề xuất cột "đoạn mô tả" (chunk_id + vì sao đoạn đó tả điểm) cho các điểm hay rỗng + 4 điểm đã sửa ở vòng chỉnh; điểm kho không có bài ⇒ "cần bổ sung kho". Vòng mới ⇒ A hỏi User; sau đó nghiệm thu lại bằng **bộ quyết 12 chưa mở** + Playwright.
- **Việc sau từ review E** (minor, sửa ở vòng sau, không mở vòng riêng): (1) `tools/nghiem_thu.py` `cham_code` chưa có điều kiện loại ngay "tên ngoài bảng" (E dò từ khoá: 0 / 330 câu); (2) 3 / 80 tổ hợp lịch 1 ngày + sở thích thiên nhiên / chụp ảnh ra cùng khung ở cả ba kiểu đi mà không có ghi chú giải thích; (3) ghi chú bậc thang lặp từng điểm (một lịch 5 dòng) ⇒ gộp một dòng.
- **Việc sau** (chưa làm, A 13/11): ghi chú `tam_dung_mua` cho MỌI điểm bị loại theo mùa (hiện chỉ điểm ưu tiên) — một dòng code + test; người dùng mới biết vì sao điểm đó vắng.
- Worktree `/tmp/b_lkh` giữ (cây sạch, cờ tắt). Không server nào của B đang chạy.

## 7. Vòng sửa bằng dữ liệu — phần code cột "đoạn mô tả" (B, 21:47 13/11/2026; User duyệt mở vòng, A giao)

Commit `3d5cc01` (push, cờ tắt). Giá trị thật **chưa điền** — chờ E viết 2 bài kho ⇒ C review ⇒ ghi kho + dựng lại chỉ mục (chunk_id đổi) ⇒ B điền từ bảng đề xuất `data/len_ke_hoach_v2_2026-11-13/de_xuat_doan_mo_ta.md` (chọn lại mã sau khi dựng lại).
- Bảng: cột không bắt buộc `doan_mo_ta` = chunk_id; lúc nạp bảng phải là đoạn của **chính file nguồn** của điểm (`<nguon>#<số>`).
- Lúc khởi động (chỉ khi cờ bản 2 bật): một lần hỏi Qdrant (`retrieval_service.lay_doan`, lọc payload, chỉ đọc). **Chọn: báo lỗi rõ, không bỏ qua** — thiếu mã ⇒ server không khởi động, lỗi nêu đúng mã thiếu. Vì sao: chunk_id đổi sau mỗi lần dựng lại chỉ mục; bỏ qua có log thì lịch lặng lẽ quay về đoạn kém mà không ai thấy (bài học 10/11 "tính năng tắt im lặng"). Kiểm đặt NGOÀI khối bắt lỗi của bước tra cứu (đặt trong đó thì lỗi bị nuốt thành "tra cứu không khả dụng" cho cả chatbot — B thấy khi đọc lại, sửa trước commit).
- Lượt bản 2: đoạn chọn sẵn ⇒ đoạn tả điểm tìm được (vòng chỉnh 13/11) ⇒ luật cũ.
- Kiểm: test mới 81 đạt (gồm `lay_doan` trên Qdrant thật, bảng sai khuôn, mã thiếu, lịch dùng đúng đoạn chọn); file chạm có khoá 389 / 389; Q1 228 / 228; thử khởi động thật khi bật cờ: bảng hiện tại ⇒ `/health` 200; bảng có một mã sai ⇒ không khởi động, lỗi nêu mã.

## 8. Đợt 2 phần (A) — bản đồ trong lịch bản 2 (B, 21:59 13/11/2026; plan `docs/superpowers/plans/2026-11-13-len-ke-hoach-dot-2-plan.md` `d0f7bc56add0`, A duyệt)

Commit `2d34e9e` (push, cờ `ban_do_lich` + `len_ke_hoach_v2` tắt). Bảng toạ độ v7 của C (`diem_toa_do_v7.json` md5 `158e184154de`, 33 / 34 điểm bảng v8).
| Tiêu chí ghi trước (plan đợt 2, phần A) | Kết quả | |
|---|---|---|
| Luôn (960 khung): toạ độ = đúng dòng bảng theo `id_diem` · thiếu ⇒ null · mục "nghỉ" không toạ độ · cờ tắt ⇒ `lich` giống hệt · chuỗi gửi model giống khi bật / tắt | đúng ở 960 / 960 (pytest) + test qua route | ĐẠT |
| Sàn: điểm thiếu toạ độ ≤ 3 | 1 (lý do ở biên bản A0 của C) | ĐẠT |
| Hệ thống thật, Playwright 1440 + 390, 3 lịch (1 · 3 · 5 ngày): đủ ghim đúng thứ tự mỗi ngày, màu theo ngày | 9 ngày × 2 khổ màn: số trên ghim = số thứ tự các mục có link bản đồ (kể cả mục thiếu toạ độ — danh sách bên cạnh dùng cùng số nên vẫn khớp; sửa chữ theo E m-2 14/11); mỗi ngày đúng một màu, 5 ngày 5 màu | ĐẠT |
| Chỉ host tile; chữ câu hỏi không có trong URL / header gửi host tile | host ngoài duy nhất `tile.openstreetmap.org`; 0 yêu cầu tile chứa chữ câu hỏi | ĐẠT |
| Câu không lịch ⇒ 0 yêu cầu tile, chunk bản đồ không tải | 0 tile, không tải chunk, không có khối bản đồ (2 khổ màn; chạy lại cho tới hết lượt — lần đầu script chuyển trang sớm, lượt ghi `client_disconnected`) | ĐẠT |
| 0 lỗi CSP / console | **CHƯA KIỂM ĐƯỢC**: máy đo không phân giải được tên máy chủ tile (`getent` thất bại) ⇒ mọi lỗi console (72 + 44) là `ERR_NAME_NOT_RESOLVED` của ảnh tile; không có lỗi loại khác. Cần một lượt trên máy có mạng phân giải được (vd trình duyệt của User) | NOT VERIFIED |
| Cỡ: bundle chính ≤ +3 KB gzip; chunk bản đồ ≤ +2 KB | +102 B · +18 B | ĐẠT |
- Test: file chạm có khoá 384 / 384; một test cũ (`test_ban_do_lich.py`) khẳng định "bảng v3 có điểm thiếu toạ độ" — v7 phủ đủ 28 điểm v3 ⇒ sửa điều kiện; ca "thiếu toạ độ" giữ ở test bản 2. Q1 không chạy (không chạm phần dựng chuỗi — test so chuỗi gửi model bật / tắt cờ thay thế, như plan ghi).
- Tiền: 0,0041 USD (8 lượt Playwright 0,0032 + 2 lượt câu thường chạy lại 0,0009). Ảnh chụp + số: `data/len_ke_hoach_v2_2026-11-13/ban_do_a1/`.
- Đổi kèm: khoá `lich_trinh_toa_do` dùng chung với đường lịch cũ ⇒ đường cũ (câu tự do) cũng có thêm toạ độ khi bật cờ bản đồ (đã ghi ở biên bản A0).

## 9. Nghiệm thu lại đợt 1 sau khi điền "đoạn mô tả" (B, 10:23 14/11/2026; A giao đầu phiên 14/11)

**Đổi so với lượt 13/11: chỉ dữ liệu.** Code nhánh không đổi; nhánh rebase lên `main` `a400f7f` ⇒ head `505b53d` (push). E ghi kho + dựng lại chỉ mục (8.474 đoạn / 207 file, record `efbf748c2195`). Trong bảng `data/phase_9/lich_trinh/diem_v8.json` (md5 `0fcc90d9a93a`; bản trước `data/len_ke_hoach_v2_2026-11-13/diem_v8_truoc_doan_mo_ta.json`):
- cột `doan_mo_ta` có ở 10 / 34 điểm (8 điểm theo `de_xuat_doan_mo_ta.md` + 2 điểm có bài kho mới, đoạn mục "Tổng quan");
- nguồn của 2 điểm này đổi sang bài mới (code bắt `doan_mo_ta` phải thuộc file nguồn của điểm);
- cả 10 mã đều kiểm trên Qdrant (đúng mục), và server bật cờ khởi động đạt (bước kiểm mã đoạn lúc khởi động).

| Tiêu chí ghi trước (plan §5) | 13/11 (lượt 2) | **14/11** | |
|---|---|---|---|
| Bộ 20: đủ khung, 0 từ chối, ý 1–6 (code chấm) | 20 / 20 | **20 / 20** | ĐẠT |
| ≤ 1 câu dự phòng / lịch ở ≥ 18 / 20 | 17 / 20 | **20 / 20** (cả bộ: 1 câu dự phòng) | **ĐẠT** |
| Không lịch nào > 30 % câu dự phòng | 1 lịch | **0** (cao nhất 1 / 6 = 17 %) | **ĐẠT** |
| `lich_khung` ≤ 1 s | 1 / 20 = 1,27 s | trung vị 204 ms; **1 / 20 = 1,20 s**, đúng lượt dự báo lạnh (yêu cầu đầu tiên có ngày đi ≤ 7 ngày) | User đã nhận giới hạn 13/11 |
| Đủ câu: trung vị ≤ mốc `main` cùng buổi + 2 s | 5,43 ↔ 5,07 s | **4,06 s ↔ mốc 5,12 s** (nhanh hơn 1,06 s) | ĐẠT |
| Lượt dự báo lạnh ≤ mốc + 4 s | 5,6 s | 2,94 s | ĐẠT |
| Bộ quyết 12 ×2 — code chấm (ý 3 theo cặp + ý code đếm) | NOT RUN | **12 / 12 · 12 / 12**; câu dự phòng ≤ 1 ở 11 / 12 · 12 / 12 | ĐẠT phần code |
| Bộ quyết 12 ×2 — hai người chấm mù (≥ 11 / 12 mỗi lượt) | NOT RUN | **ĐANG CHẤM** (E giao; 24 file tên ngẫu nhiên ở `cham_mu_1411/`, khoá ở `khoa_cham_1411/`) | chờ |
| Playwright 2 khổ, chạy thật trên bản build do FastAPI phục vụ | NOT RUN | **ĐẠT** ở 1440 + 390: điền + gửi chỉ bằng bàn phím; khung hiện ở ~0,32 s, câu đầu ~1,8–1,9 s; 0 lỗi console; 0 yêu cầu mạng ra ngoài origin | ĐẠT |
| Review cả nhánh | — | chờ E | — |

- **Ghi chú:**
  - Bộ 12 là bộ chưa ai mở; mở lượt này theo handoff.
  - Ảnh chụp 390 dạng toàn trang có ô "Hỏi tiếp" và thanh điều hướng đè lên giữa lịch. Đây là do cách chụp toàn trang với phần tử cố định, không phải lỗi bố cục: lúc dùng thật hai phần đó nằm ở đáy màn.
  - Playwright bản đồ (cờ `ban_do_lich` tắt): máy vẫn không phân giải được DNS host tile ⇒ "0 lỗi console khi có bản đồ" vẫn **chưa kiểm**; không thuộc nghiệm thu đợt 1.
- **Test:** test rộng `backend/tests` có khoá: **956 đạt / 1 hỏng** (4 phút 41 s).
  - Test hỏng: `test_cong_dot_1.py::test_explore_lists_exactly_the_build_record_sources`. Test này ghi cứng 204 bài, kho giờ có 207 bài sau lần ghi kho của E ⇒ hỏng cả trên `main`, không do nhánh ⇒ báo A.
  - Q1 (chuỗi gửi model giống byte khi cờ tắt) **dùng lại** 228 / 228 của 13/11: từ `0d4ee6e` tới `main` không có thay đổi nào ở `backend/` hay `frontend/`, và code nhánh không đổi.
- **Giới hạn:** `diem_v8.json` dùng giờ Đại Nội 07:00–17:30 lấy từ kho; giờ này có thể đổi theo mùa ở lần ghi kho kế (A dặn). Lịch xếp theo giờ hiện có; bảng không tự sửa.
- **Tiền 14/11:** **0,031 USD**. Gồm mốc `main` 0,0091 + bộ 20 0,0091 + bộ 12 ×2 + Playwright 2 lượt 0,0124; tổng 46 + 20 dòng `chat_metrics` gọi model thật. Cả đợt 1 ≈ **0,068 / trần 0,20**.
- **Hồ sơ:** `data/len_ke_hoach_v2_2026-11-13/nghiem_thu/` (`moc_main_1411`, `v2_20_1411`, `quyet12_1411_l1`, `_l2`, `pw_1411/`) · công cụ mới `tools/pw_nghiem_thu.py`.
- **Kết luận tạm:** mọi tiêu chí đã đo đều ĐẠT (trừ khung dự báo lạnh mà User đã nhận). Còn chờ hai người chấm mù + review cả nhánh của E. Đạt cả hai ⇒ A trình User D4 ⇒ bật cờ.

## 10. Sửa theo review cả nhánh của E (B, 10:37 14/11/2026; A chốt hướng (c) — giữ thước ghi trước)

Review: `e_review_len_ke_hoach_nhanh_1411.md` (changes_requested: bộ quyết 12 trượt ý 6 + M-1 + 2 minor). Commit **`6310645`**, nhánh rebase lên `main` (gồm `d9d54f9` sửa test 204), đã push.

**Ghép hai người chấm mù — lượt trước khi sửa** (`tools/ghep_cham.py` ⇒ `nghiem_thu/ghep_cham_1411.txt`):
- mỗi lượt **10 / 12** < sàn 11 / 12 ⇒ **TRƯỢT theo chữ ghi trước**;
- hai người chấm khớp nhau 24 / 24;
- 2 tổ hợp × 2 lượt trượt ý 6: ngày dự báo mưa ≥ 60 % mà không có dòng "Nếu mưa", vì ngày đó không có điểm ngoài trời để thay.

**Sửa (một commit):**
- **Ý 6:** ngày dự báo mưa ≥ 60 % luôn có đúng một dòng "Nếu mưa" do code viết (`len_ke_hoach.dong_neu_mua`), theo ba trường hợp:
  - có điểm ngoài trời thay được ⇒ gợi ý thay (như cũ);
  - có điểm ngoài trời nhưng không có điểm thay ⇒ nói thẳng;
  - không có điểm ngoài trời ⇒ "các điểm trong ngày đều trong nhà hoặc có phần trong nhà".
- **M-1:** điểm thêm vào buổi sáng chỉ được nhận khi kết thúc ≤ giờ đầu buổi chiều. Lý do: quỹ phút không tính thời gian chờ giờ suất / mở cửa. `kiem_khung_v2` thêm mã `sang_chong_chieu` (độc lập với bộ xếp) + test cố tình vi phạm.
- **Bộ chấm bằng code** (`tools/nghiem_thu.py`): thêm vế dự báo của ý 6 + chế độ `cham_lai` (chấm lại kết quả đã lưu, 0 USD). Chấm lại lượt TRƯỚC khi sửa ⇒ **10 / 12 · trượt đúng Q04, Q11** — khớp hai người chấm, tức là vế mới bắt đúng lỗi họ thấy.

**Kiểm sau sửa:**

| Kiểm | Kết quả |
|---|---|
| Ca dò toàn tổ hợp, có / không dự báo ghi sẵn (`tools/do_sua_1411.py`, 0 USD) | 9.600 khung: **0** mã lỗi kiểm khung; 13.824 ngày mưa: **0** thiếu / thừa dòng "Nếu mưa" |
| Ca dò của E (3.840 khung) | sáng chồng chiều **52 ⇒ 0** |
| Test file chạm (`test_len_ke_hoach_v2.py` + `test_ban_do_lich.py`) | 95 đạt, cộng 1 test mới (22 s) |
| Bộ 20 chạy lại (server nhánh sau sửa, cổng 8894) | 20 / 20 đạt; dự phòng ≤ 1 20 / 20; đủ câu trung vị **4,56 s** (mốc `main` sáng nay 5,12 s); khung trung vị 188 ms, chậm nhất 1,26 s ở lượt dự báo lạnh (giới hạn User đã nhận); chấm lại với vế dự báo: 20 / 20, 8 ngày mưa đều có dòng |
| Bộ quyết 12 ×2 chạy lại — code chấm (có vế dự báo) | **12 / 12 · 12 / 12**; dự phòng ≤ 1 12 / 12 cả hai lượt; 5 ngày mưa / lượt đều có đúng một dòng |
| Bộ quyết — người chấm mù | E giao lại cho các lịch đổi (theo A) — **chờ** |

- **Không chạy lại:**
  - Playwright: sửa chỉ ở backend, đường đi giao diện không đổi ⇒ không giữ sàn mới nào.
  - Q1 "cờ tắt giống byte": mọi chỗ sửa chỉ chạy trên đường bản 2 (`xep_v2`, `dong_du_bao`, `kiem_khung_v2`) ⇒ cờ tắt không chạm.
- **Giới hạn (A quyết GIỮ, 14/11):** nghỉ trưa có thể chỉ 15–45 phút ở 104 / 3.840 ngày (buổi sáng xong lúc 12:45 vì một điểm thêm vào; buổi chiều bắt đầu 13:00 / 13:30). Không chồng giờ, hành vi có từ trước sửa. Xét lại nếu User nhận xét khi xem; muốn chặn "sáng không quá 12:30" thì chỉ đổi một hằng.
- **m-1 (luật):** sửa kho một trong 10 file nguồn có `doan_mo_ta` ⇒ kiểm lại cột này (mã đoạn `file#số` vẫn có thể còn mà trỏ sang đoạn khác). Bước kiểm lúc khởi động chỉ bắt mã mất, không bắt mã trỏ lệch. Ghi vào bài học khi bật.
- **m-2:** đã sửa chữ §8.
- **Tiền:** lượt sửa 0,0205 USD (44 lượt). Hôm nay tổng **0,051 USD** (mốc 0,0091 + nhánh 0,0420). Cả đợt 1 ≈ **0,088 / trần 0,20**.
- **Hồ sơ:** `data/len_ke_hoach_v2_2026-11-13/nghiem_thu/` (`v2_20_1411_sua/`, `quyet12_1411_sua_l1/`, `_l2/`, mỗi thư mục có `ket_qua_cham_lai.json`).

## 11. Kiểm phần sửa của E ⇒ bộ quyết qua sàn; sửa M-2 (B, 10:43 14/11/2026)

- **Người chấm mù lại 6 lịch đổi** (`ghep_cham.py` ⇒ `nghiem_thu/ghep_cham_1411_sua.txt`): 6 / 6 đạt mọi ý ở cả hai người, 0 lệch nhau. 9 lịch còn lại mỗi lượt không đổi khung / dòng mưa so với lượt hai người đã cho đạt ⇒ **bộ quyết 12 / 12 · 12 / 12 — ĐẠT sàn ≥ 11 / 12**. (Script in "TRƯỢT" vì chỉ thấy 3 lịch / lượt; số cuối là phép ghép này.)
- **M-2 (E):** một câu model ở vị trí mô tả nói về tài liệu ("tài liệu không cung cấp thông tin về …") lọt qua `kiem_cau`, vì câu không nêu tên điểm nào khác. Gốc lỗi: đoạn chọn cho điểm đó tả công trình bên cạnh.
  - **Sửa** (commit `16374fc`): `kiem_cau` thêm mã `noi_ve_tai_lieu` (mẫu chữ nói về tài liệu / nguồn) ⇒ câu dự phòng cho riêng mục đó; thêm 1 ca vào test câu.
  - **Thử mẫu chữ** trên **1.068** câu model đã lưu của mọi lượt nghiệm thu: trúng **đúng 1** câu (câu lỗi), 0 câu tốt bị chặn.
  - **Câu dự phòng tăng thêm** (đếm trên kết quả đã lưu, 0 USD): bộ 20 **+0** (vẫn 20 / 20 ≤ 1); bộ quyết: 1 lịch 0 ⇒ 1 / 21.
  - **Dữ liệu:** thêm `doan_mo_ta` cho điểm này = đoạn "Tổng quan" tả đúng điểm (11 / 34 điểm có cột; `diem_v8.json` md5 `d815f4918a55`, bản trước `diem_v8_truoc_ho_quyen.json`). Mã có trên Qdrant; server 8894 còn nạp bảng cũ ⇒ kiểm lúc khởi động chạy ở lần mở server kế.
- **Test:** `test_len_ke_hoach_v2.py` + `test_ban_do_lich.py` 95 đạt. Không lượt có phí mới.

## 12. Giờ mở cửa Quần thể di tích (User D4 14/11: "Bật, sửa giờ Đại Nội trước") — B, 10:51 14/11/2026

- Nguồn: User tra 14/11 trên một trang du lịch công khai có dẫn quy định của đơn vị quản lý di tích. Có hai khung giờ theo mùa (hè mở sớm hơn, đông đóng sớm hơn); giờ cụ thể và ngày đổi mùa ghi ở `gio_mo_can_cu` của bảng (private).
- Code chưa có giờ theo mùa ⇒ theo A, ghi giờ **giao hai mùa 07:00–17:00**, không thêm code.
- **12 điểm** có căn cứ "khung giờ chung của Quần thể" (07:00–17:30) đều đổi sang 07:00–17:00, `gio_mo_can_cu` ghi nguồn + ngày. Thác Nhị Hồ có căn cứ riêng (giờ mùa khô) ⇒ giữ nguyên.
- `diem_v8.json` md5 `448825605dc9`; bản trước ở `data/len_ke_hoach_v2_2026-11-13/diem_v8_truoc_gio_dai_noi.json`. Chỉ đổi dữ liệu, không đổi code.
- **Kiểm (0 USD):**
  - ca dò 9.600 khung: 0 mã lỗi (gồm `ngoai_gio_mo` ⇒ không điểm nào kết thúc sau 17:00), 0 ngày mưa thiếu dòng;
  - ca dò sáng chồng chiều: 0;
  - so cũ ↔ mới trên 3.840 khung: **0 khung đổi điểm, 0 khung đổi giờ** — các điểm này vốn đã được xếp xong trước 17:00;
  - 95 test đạt.
  ⇒ Kết quả nghiệm thu §9–§11 dùng được nguyên, không cần chạy lại.
- **Giới hạn còn lại:** mùa hè các điểm mở từ 06:30 nhưng lịch vẫn bắt đầu từ 07:30 / 08:00 (giờ bắt đầu buổi sáng) ⇒ không sai, chỉ chưa tận dụng.
