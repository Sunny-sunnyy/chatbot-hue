# Implementation Report: chọn chỗ ở theo hạng sao trong "Lên kế hoạch"

Người làm: B (Claude Code, Opus 5.5, `hue-rag-b2`) · 10:38 15/11/2026
Plan: `docs/superpowers/plans/2026-11-15-khach-san-trang-va-ngan-sach.md` bản 2 (sha `b5d8bc184090`, A duyệt, User chốt 10:28) — §2 + T1–T4, T7.
Nhánh `p9-ngan-sach-o` (từ main `3c27cc9`), worktree `/tmp/b_ns`.

## 1. Phạm vi

Biểu mẫu "Lên kế hoạch" có thêm nhóm nút **"Chỗ ở theo hạng sao (không bắt buộc)": 1 sao · 2–3 sao · 4–5 sao**. Khi chọn, ô "Nơi ở gợi ý" chỉ hiện
≤ 5 cơ sở của đúng mức đó (cùng khu, cùng luật xếp). Không chọn ⇒ như cũ. Sửa lịch bằng lời giữ mức đã chọn. Không giá phòng, model không thấy mức.
Ngoài phạm vi nhánh này: trang "Chỗ ở" (C, nhánh `p9-cho-o`).

## 2. Thay đổi chính

| File | Đổi gì |
|---|---|
| `backend/llm/hoi_lai.py` | `TruongInput.ngan_sach: Literal["binh_dan","vua","cao"]`; thêm vào `TRUONG_CHI_MOI` (giá trị mới ⇒ chỉ nhận ở lượt biểu mẫu bản 2) |
| `backend/llm/lich_trinh_v2.py` | `ThamSoV2.ngan_sach`; `tu_truong` đọc; dict `tham_so` của `xep_v2` mang khoá **chỉ khi có chọn** (không chọn ⇒ khung giống byte) |
| `backend/llm/sua_lich_v2.py` | `_ts` đọc `ngan_sach` ⇒ sửa lịch xếp lại vẫn giữ mức |
| `backend/llm/luu_tru_lich.py` | `MUC_NGAN_SACH`; `chon_co_so(…, ngan_sach)`: có mức ⇒ ≤ 5 cơ sở mức đó; mức trống ⇒ im lặng về (2, 2, 1); thân cũ thành `_chon`; `o_dau(…, ngan_sach)` |
| `backend/llm/len_ke_hoach.py` | `gan_o_an` truyền `ts_k.get("ngan_sach")` (1 dòng) |
| `backend/llm/assistant.py`, `config/settings.yaml` | `ngan_sach` vào `O_BIEU_MAU_V2` + `len_ke_hoach_o_hien` (ô hiện) |
| `frontend/src/LenKeHoach.jsx` | nhóm 3 nút, gửi `truong.ngan_sach`, dòng tóm tắt "chỗ ở 4–5 sao" |
| `backend/tests/test_luu_tru_lich.py` | 4 test mới (T1/T2 trên 3.840 khung, mức trống, T3 + T4, T7) |
| `backend/tests/test_len_ke_hoach_v2.py` | test cờ dùng "ngan_sach" làm ví dụ ô lạ ⇒ đổi ví dụ sang `gia_phong`, thêm `ngan_sach` vào tập ô biết |

**Lệch plan (nhỏ, tự quyết trong phạm vi):** plan ghi nút ở `chung.jsx` `BIEU_MAU` — đó là biểu mẫu cũ; biểu mẫu bản 2 đang chạy ở `LenKeHoach.jsx` ⇒ sửa ở đó.
Dòng "Mình hiểu" và câu người dùng ghép vào lịch sử (`ghep_cau_v2`) **không** thêm mức (giữ T3 giống byte).

## 3. Cách đã chạy thật — kết quả

| Bước | Lệnh / cách | Kết quả | Thời gian |
|---|---|---|---|
| Test file chạm | `pytest tests/test_luu_tru_lich.py tests/test_len_ke_hoach_v2.py` | 103 đạt | 23 s |
| **T1** giống byte khi không chọn | `data/ngan_sach_o_2026-11-15/tools/t1_bam.py` chạy với backend của main rồi của nhánh: băm `o_dau` + khung của 3.840 khung | main `67b491fd9219` / `6e7c33ebe62e` = nhánh `67b491fd9219` / `6e7c33ebe62e` — **đạt** | ~1 phút / lượt |
| **T2** chọn mức ⇒ đúng mức | test trên 3.840 khung × 3 mức: mọi cơ sở đúng mức, 1–5 cơ sở, cùng khu như không chọn (0 khu trống mức với bảng v2) | **đạt** | trong pytest |
| **T3** chuỗi gửi model giống byte | test: `tin_nhan_model`, `minh_hieu`, `tin_nhan_hieu` (lượt hiểu ý sửa), `ghep_cau_v2` có / không mức | **đạt** | trong pytest |
| **T4** sửa lịch giữ mức | test qua `sl.ap` thật (đổi 3 ⇒ 2 ngày ⇒ `_xep` ⇒ `gan_o_an`): khung còn `ngan_sach: "cao"`, ô Nơi ở chỉ 4–5 sao; ngân sách không đổi bộ xếp điểm (khung = khung không chọn) | **đạt** | trong pytest |
| **T7** giá trị lạ | `TruongInput(ngan_sach="re")` ⇒ lỗi khuôn (route 422) | **đạt** | trong pytest |
| Test rộng | `uv run --env-file … pytest tests` (sau khi A báo máy rảnh) | 1.051 đạt / 1 trượt (test ví dụ ô lạ — sửa như bảng §2, chạy lại 2 file đạt) | 4 phút 28 |
| Playwright 1440 | `data/ngan_sach_o_2026-11-15/tools/pw_ngan_sach.py`, server tạm 8893 (cwd `/tmp/b_ns/backend`), xếp lịch thật 3 ngày | 3 nút có; bấm "4–5 sao" ⇒ `aria-pressed`, tóm tắt "chỗ ở 4–5 sao"; thẻ 5 cơ sở đều 4–5 sao; 0 lỗi console; 0 yêu cầu ra ngoài — **đạt**; ảnh `data/ngan_sach_o_2026-11-15/anh/` | ~40 s |

Chỉ chạy khổ 1440: nhóm nút dùng lại lớp `chip` / `lc-nhom` sẵn có, không bố cục riêng cho điện thoại (W76).

Tiền: Playwright 1 lượt xếp lịch **0,00064 USD** (dòng `chat_metrics` của server tạm). Còn lại 0 USD.

## 4. Giới hạn

- Vẫn tất định: chọn cùng mức ⇒ cùng ≤ 5 cơ sở ở mọi lịch trung tâm (12 ⇒ 36 cơ sở có thể hiện, số của C). Trang "Chỗ ở" là chỗ xem thêm.
- "1 sao / 2–3 sao / 4–5 sao" là hạng trong danh mục, không phải giá.
- Nếu nhánh `p9-cho-o` của C (bảng v3) merge trước ⇒ B rebase, chạy lại test file chạm trên bảng v3 (T2 kiểm lại "0 khu trống mức").
- **Ý chờ (không làm ở nhánh này):** chữ "khả năng mưa X %" (`thoi_tiet.py:199` `dong_ngay`, `TrangChu.jsx:185`) nên ghi rõ "lúc cao nhất trong ngày"
  — `dong_ngay` nằm trong kết quả công cụ thời tiết gửi model + dòng dự báo của lịch ⇒ đổi là đổi chuỗi gửi model, không phải sửa ≤ 2 dòng.
