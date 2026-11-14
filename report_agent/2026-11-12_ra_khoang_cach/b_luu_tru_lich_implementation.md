# Gợi ý nơi ở trong lịch bản 2: implementation (B, 15:26 14/11/2026)

- **Plan:** `docs/superpowers/plans/2026-11-14-luu-tru-trong-lich-plan.md`, A duyệt sha `15529d97b6c7`.
- **Nhánh:** `p9-luu-tru-lich` từ `main` `c0be7e1`, worktree `/tmp/b_lkh`.
- **Cờ:** `luu_tru_lich` **TẮT** trong commit; chỉ bật tạm trong worktree lúc đo, đã trả lại.
- **Dữ liệu:** bảng của E `data/luu_tru_2026-11-14_lich/bang_luu_tru_lich.json` (md5 `a4c97df36c7c`, khớp plan).
- **Tiền:** 4 lượt xếp lịch thật cho Playwright ≈ 0,0025 USD (log `chat_metrics`: 0,00061 / 0,00060 / 0,00064 / 0,00062).

## Đổi gì
| File | Việc |
|---|---|
| `backend/llm/luu_tru_lich.py` (mới) | Nạp và kiểm bảng lúc khởi động. Chọn một khu cho cả chuyến. Chọn ≤ 5 cơ sở trải theo hạng. Viết lý do, dựng link tìm phòng Booking, viết khối chữ cho nút chép. Toàn bộ do code, model không chọn gì. |
| `backend/llm/assistant.py` | Cờ `luu_tru_lich`, trường `luu_tru_bang`, kiểm "cần cờ bản 2 + bảng". |
| `backend/llm/len_ke_hoach.py` | Cờ bật ⇒ gán `lich["o_dau"]` sau `dung_lich`. Cả lượt sửa lịch cũng tính lại theo khung mới. |
| `backend/llm/lich_trinh_v2.py` | `ghep_chu` thêm khối "Nơi ở gợi ý" khi có `o_dau`. Cờ tắt ⇒ chữ giống bản trước. |
| `backend/config/settings.yaml` | `luu_tru_lich: false` + `lich_trinh_bang_luu_tru`. |
| `frontend/src/LichV2.jsx`, `lkh.css` | Thẻ "Nơi ở gợi ý" cuối lịch. Chỉ nhận link đúng gốc Booking; link mở tab mới khi bấm. |
| `backend/tests/test_luu_tru_lich.py` (mới), `test_cong_dot_1.py` | 6 test. `flags_from` ghim thêm `luu_tru_lich: False` (test không đọc cờ thật). |

**Ba quyết định trong phạm vi plan.** Hai quyết định đầu là sửa sau khi người xem lượt 1 bắt lỗi:
1. **Ven biển tách theo phía.** Khu ven biển trong bảng gộp Thuận An / Tam Giang với Lăng Cô (cách ~40 km), mà 13 / 13 cơ sở ven biển không có cụm gần. Code tách theo chữ trong địa chỉ: Phú Vang / Thuận An ↔ Phú Lộc / Lăng Cô, và chỉ gợi ý cơ sở cùng phía với cụm có nhiều điểm nhất. Địa chỉ không khớp phía nào thì không gợi ý (1 cơ sở: "xã Phú Vinh").
2. **Cụm đi trong ngày (`nam_xa`: Bạch Mã, Nhị Hồ) không được đếm cho khu nào.** Bảng xếp cụm này vào khu ven biển, nên lượt 1 có lịch bị kéo ra biển dù chỉ có 2 điểm ven biển thật.
3. **Lý do không nêu tỉ lệ dưới một nửa.** Khi trung tâm được chọn vì các điểm rải nhiều hướng, lý do ghi "các điểm của lịch rải nhiều hướng, từ đây đi hướng nào cũng gần". Người xem lượt 1 nhận xét câu "2 / 9" nghe như khu ở không hợp.

## Đo [Chạy] — đối chiếu tiêu chí ghi trước
| Mã | Kết quả |
|---|---|
| Luôn (3.840 khung, mô phỏng 0 USD) | **ĐẠT**: lịch ≥ 2 ngày có `o_dau` 3.072 / 3.072, lịch 1 ngày 0 / 768. Mọi cơ sở có trong bảng và đúng khu; khu đúng luật (đếm lại độc lập trong test); 0 link ngoài mẫu Booking; ≤ 5 cơ sở; có nhãn "chưa kiểm giá". Khu được chọn: trung tâm 2.920 · phía tây 104 · ven biển 48. |
| Q1 | **ĐẠT**: tin nhắn viết câu gửi model giống byte dù có hay không `o_dau` (test). Cờ tắt ⇒ đường code không chạy. `ghep_chu` cờ tắt giống bản trước. Không chạy bộ Q1 228 vì code không chạm phần dựng chuỗi gửi model (luật §8). |
| Người xem (≥ 9 / 10) | Lượt 1: **9 / 10** (đã đạt ngưỡng), bắt 2 lỗi thật (ý 1–2 ở trên) ⇒ sửa. Lượt 2, cùng 10 lịch, agent con ngữ cảnh mới: **10 / 10**. File `data/luu_tru_lich_2026-11-14/xem_10.md`, `xem_10_v2.md`; khoá lịch `xem_10_khoa.json`. |
| UI | **ĐẠT**: Playwright 1440 + 390 trên bản build thật (`pw_luu_tru.py`, `pw_ket_qua.json`, ảnh `anh/`). Thẻ hiện, 3 cơ sở, 3 / 3 link đúng gốc + `_blank` + `noopener`, có nhãn, 0 lỗi console, 0 yêu cầu ra ngoài. |

**Thời gian:**
- test file chạm không khoá: 76 s (116 đạt);
- test file chạm có khoá: 54 s (124 đạt);
- Playwright: ~1 phút / lượt.

Kết quả chạy lại sau khi trả cờ và test rộng ghi ở mục cuối.

## Giới hạn
- **Đếm theo số điểm, không theo số ngày.** Một ngày nhiều lăng có thể kéo cả chuyến sang khu phía tây (người xem lượt 2: lịch 8 "hợp lý nhưng yếu nhất"). Không đổi vì đây là luật plan; ghi để bàn nếu User thấy.
- Lý do kiểu "Cùng khu với X / Y" không nhắc trẻ em khi đoàn có trẻ em mà khu đã thắng theo tỉ lệ (người xem lượt 2).
- Thứ tự trong cùng mức hạng xếp theo tên, nên nhiều lịch trung tâm ra cùng 5 cơ sở. Đúng plan: tất định, không xếp theo khoảng cách vì toạ độ chỉ ~1 km.
- Phía tây chỉ có 5 cơ sở, nên lịch phía tây thường chỉ gợi ý được 3 cơ sở.
- Cách tách phía biển dựa vào chữ trong địa chỉ của danh mục; đổi tên hành chính có thể làm lệch. Có 1 cơ sở không khớp phía nào nên không được gợi ý.

## Sau khi trả cờ về tắt [Chạy]
- File test bị chạm, không khoá: **116 đạt** (2 phút 01).
- File test bị chạm, có khoá: **124 đạt** (1 phút 17).
- **Test rộng** cả `backend/tests` có khoá trên `9624215`: **1.001 đạt, 0 trượt** (12 phút 11; chạy song song với việc khác nên chậm hơn thường).
