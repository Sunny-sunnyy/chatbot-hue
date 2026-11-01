# Nhật ký 01/11/2026 — streaming vào chatbot, chuẩn bị đóng Phase 8

**Cập nhật lần cuối: 12:52 01/11/2026 (kết phiên).** Tiền paid cả ngày: ≈ **0,15 USD** (~3.800 đồng; streaming ≈ 0,027 + lượt đo cuối ≈ 0,139 — một phần trùng ở S4) / trần phiên 1 USD.

## Tóm tắt
- **Chữ hiện dần (streaming) đã chạy trong chatbot** (merge `a80e12d`): trên trình duyệt, chữ trả lời đầu tiên hiện sau trung vị **1,23 s**, câu chậm (p95) **2,61 s** —
  đạt sàn 3 / 5 s và cả mục tiêu 1,5 / 3 s. Lợi so với chờ đủ câu chỉ ~0,44 s (câu thử ngắn); bạn chọn giữ cách này, giữ sàn.
- **Báo cáo so sánh mọi phương án Phase 0 → 8.2** đã đăng (`BAO_CAO_SO_SANH_PHUONG_AN.md`, 62 khối, ~115 số đối chiếu với file gốc, 2 lượt kiểm độc lập đạt).
- **Bảng giới hạn đã biết** theo mức nặng vào `LUONG_HOAT_DONG_HE_THONG.md` mục 5. Công thức tiền của công cụ đo đã tính theo giá đủ.
- **Đo lại theo loại câu** trên kho hiện tại (0 USD): chỉ câu cần nhiều nguồn còn yếu rõ ⇒ bạn để **Phase 9** (cùng hội thoại nhiều lượt).
- **Rà bảo mật một lần lúc đóng gói:** 11 rủi ro, 0 chặn; đã rào 2 rủi ro chính của chính các agent (công cụ tra web Codex không còn đọc được file máy; hook trước khi push).
- **Lượt đo cuối Phase 1–8 xong — mọi sàn đạt:** Golden 176 "không làm hỏng" (2 câu tụt, cho phép ≤ 5; Đúng 4,71 · Đủ 4,58); bộ an toàn và câu theo ngày đạt; **bộ kín mới 40 câu** (bạn duyệt mẫu):
  0 / 6 câu ngoài kho bị trả lời, 0 đảo cảnh báo, nhưng điểm Đủ **4,18** ↔ 4,58 ở Golden — kể cả chỉ tính câu được trả lời vẫn thấp hơn (4,60 ↔ 4,82) ⇒ **số trên bộ thử lạc quan hơn câu thật**.
- **Đính chính (A báo bạn trong phiên rồi sửa):** A từng nói khoảng cách bộ kín "gần hết do từ chối nhầm" và tốc độ qua API "nhanh hơn rõ" — review độc lập chỉ ra cả hai nói quá (hôm đo model gần như
  không suy luận ⇒ có thể nhanh hơn ngày thường); báo cáo đã sửa.

## Bạn cần làm gì
- **B0:** đọc 20 cặp câu trả lời mù `data/phase_8_2/b0/nhan_xet_user.md` (không mở `khoa.json`) — mốc người cho người chấm Claude; xong thì bạn đóng Phase 8.
- Phiên sau trả lời vài câu nhỏ (A hỏi từng câu): quyền phiên, xoá 4 nhánh đã merge, mấy mục bảo mật chờ quyết.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Streaming (spec duyệt, 4 bước, review cả nhánh) | vào `main`; đạt sàn + mục tiêu | người dùng thấy chữ sau ~1,2 s thay vì chờ đủ câu |
| Báo cáo so sánh phương án | đăng, 2 lượt kiểm đạt | một chỗ đọc lại mọi lựa chọn đã thử / chọn / bỏ, có số và độ tin |
| Đo lại theo loại câu | chỉ câu nhiều nguồn yếu (Đủ 3,50 ↔ 4,92) | để Phase 9 (agent tách câu con) |
| Rà bảo mật | 0 chặn; rào Codex + hook pre-push | giảm rủi ro lộ dữ liệu khi agent tra web / đẩy code |
| Câu Golden lệch kho | giữ nguyên (bạn chọn) | chỉ khác hoa / thường, điểm không sai |
| Hội thoại nhiều lượt | dời Phase 9 (bạn chọn) | nghiên cứu cùng phần trợ lý / agent |
| Lượt đo cuối | mọi sàn đạt; bộ kín: số dev lạc quan | số cuối Phase 8 cho đồ án |

## Giải thích ngắn (để bạn tự nói lại được)
Trước đây trang web chờ model viết xong cả câu (qua API p95 ~6 s, chưa đạt 5 s). Nay server gửi từng mảnh chữ ngay khi model viết, nhưng chỉ bật link nguồn sau khi kiểm trích
dẫn ở cuối; kiểm hỏng thì rút lại chữ — nên vẫn "không trả lời điều không kiểm được". Đo trên trình duyệt thật: chữ đầu ~1,2 s. Giới hạn: một lần đo 38 câu, lợi so với chờ đủ câu nhỏ;
giao diện JS thuần sẽ làm lại sau Phase 8 theo danh sách yêu cầu đã ghi. Tự nhìn lại (bạn hỏi): streaming bị làm quá kỹ ở phần spec / giao diện sắp bỏ — đã đổi cách làm (mỗi việc
một lần review, phần sắp thay làm tối thiểu).

## Đọc thêm
- `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_SO_SANH_PHUONG_AN.md`
- `report_agent/2026-10-31_streaming_spec/` (spec, review từng bước, S4, bảo mật C106)
