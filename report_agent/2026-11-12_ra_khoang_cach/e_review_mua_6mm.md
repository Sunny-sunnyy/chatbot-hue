# Review — nhánh `p9-mua-6mm` (xếp lại lịch khi ≥ 60 % VÀ ≥ 6 mm)

Người kiểm: E (`hue-rag-3e`) · ghi lúc 10:34 15/11/2026 (`date`) · người làm: C · A giao (risk-gated, một lượt cả nhánh).
Phạm vi: `0a6333e`, so với `origin/main` `3c27cc9` (nhánh dựng trên main mới). 3 file, +30 / −3.

**Kết luận: `ready_for_user_confirmation`.** Có 1 minor về chú thích code, không chặn. Sửa ≤ 2 dòng thì A merge thẳng.

## Đã kiểm (tự chạy)

| Cổng | Kết quả |
|---|---|
| Phạm vi | Đúng User chốt 10:28 15/11: hằng số `MM_MUA_XEP = 6`; hàm thuần `ngay_mua_xep`; `chuan_bi` dùng hàm này. `dong_du_bao` / "Nếu mưa" không đổi (vẫn đọc `db`, ≥ 60 %). Không chạm chuỗi gửi model, cờ, `data/` |
| `git diff --check` | sạch |
| Lượng mưa rỗng (`None`) có làm sập phép so `>= 6` không | Không. `thoi_tiet.py:142` qua `_so(mua, "mua")`: số rỗng hoặc ngoài miền ⇒ cả lượt dự báo coi là lỗi ⇒ `db = None` ⇒ `ngay_mua_xep` trả `None`. Trong `db` luôn có số |
| Dict rỗng `{}` (có dự báo nhưng không ngày ≥ 6 mm — giờ sẽ hay gặp) | Bộ xếp kiểm `if mua and …` (`lich_trinh_v2.py:251`) ⇒ `{}` và `None` cho cùng kết quả. Lượt sửa lịch đổi `{}` ⇒ `None` (`sua_lich_v2.py:91`): cùng hành vi |
| Sửa lịch theo cùng luật | Có. `luu["mua"]` lưu chính dict đã lọc (`len_ke_hoach.py:117` ⇒ `sua_lich_v2.py:76/91`). Ngoài hai chỗ này không còn chỗ nào khác gọi `xep_v2(mua=…)` trong `backend/` |
| Test mới có nghĩa | Có. Ca 5,9 mm ⇒ ngày 1 xếp như không mưa nhưng vẫn có "Nếu mưa ngày 1". Ca đối chứng `mua={hom: 80}` ⇒ ngày 1 đổi, nên test không đúng vô nghĩa. Cũng khoá luôn biên 6,0 mm và ngày `xs` rỗng |
| Test cũ đổi 1,0 ⇒ 12,0 mm | Đúng: giữ kịch bản "mưa" vẫn là mưa theo luật mới; không nới tiêu chí |
| Chạy | `test_len_ke_hoach_v2.py` + `test_sua_lich_v2.py`: **99 passed, 20,8 s** (worktree riêng, `.venv` main) |

## Finding

**m-1 (minor):** chú thích `xep_v2` cũ.
- `lich_trinh_v2.py:187` vẫn ghi "`mua` = {ngày: khả năng mưa %} (chỉ các ngày có dự báo)".
- Từ nhánh này, dict chỉ gồm ngày có **≥ 6 mm**. Người đọc code sau dễ nghĩ mọi ngày có dự báo đều được xét.
- Đóng khi: câu ghi "chỉ ngày dự báo ≥ `MM_MUA_XEP` mm (lọc ở `len_ke_hoach.ngay_mua_xep`)".

## Tiền / thời gian
0 USD. Pytest 20,8 s. Không Playwright / server: nhánh không đổi giao diện; chữ người dùng thấy chỉ đổi ở ngày mưa nhỏ, và test đã khoá.
