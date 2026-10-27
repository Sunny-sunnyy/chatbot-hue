# Nhật ký 27/10/2026 (chiều) — dọn phần tồn của các Phase cũ, soạn sẵn đợt sửa kho

**Cập nhật lần cuối: 16:50 27/10/2026.** Tiền paid chiều nay: ≈ 0,0012 USD (~30 đồng), đo từ log (3 lần chạy thử server, mỗi lần 2 câu).

## Tóm tắt

- Bạn muốn **xong phần tồn của các Phase cũ trước**, rồi mới đi tiếp. Chiều nay làm xong mọi phần tồn **không cần đụng kho**, và soạn sẵn toàn bộ đợt **sửa
  kho**. Đợt sửa kho chạy ngay sau khi đóng 8.2, vì nếu sửa kho trước thì phép so cuối 8.2 lẫn hai thay đổi.
- **Context 10 sẵn sàng merge:** nhánh đã đưa lên nền mới nhất, kiểm lại đủ (kết quả tìm 158 câu giống hệt, chạy thật 2 câu đạt). Chỉ còn chờ B0 của bạn.
- **Kế hoạch mốc cuối 8.2 (36 câu kín) đã duyệt.** Khi bạn quyết mở câu kín, B chạy ngay (~0,012 USD).
- **Thước đo lên bản v3** (bạn đồng ý): sửa nhãn "đoạn đúng" ở 2 câu thuộc nhóm kiểm. Kết luận cũ không đổi.
- **Đợt sửa kho:** 41 chỗ sửa có căn cứ ngay trong kho + 11 chỗ tên phường cũ còn sót + loại 1 file danh mục khỏi index. Mỗi chỗ đã có người thứ hai kiểm.
  16 câu cần bạn trả lời; 78 mục cần tra ngoài (yêu cầu ChatGPT đã soạn).
- **Chatbot không đổi** trừ một chi tiết trong log số đo (`dense_ms` làm tròn 1 chữ số).

## Bạn cần làm gì

- **B0:** đọc cặp mù 20 câu (`data/phase_8_2/b0/nhan_xet_user.md`, ~30–45 phút) — vẫn là việc duy nhất chặn context 10 và mọi bước sau.
- Khi rảnh: trả lời 16 câu về kho (`data/sua_kho_2026-10-27/cau_hoi_user.md`, mỗi câu có gợi ý).
- Khi tiện: gửi 2 yêu cầu ChatGPT trong `gửi chatgpt/2026-10-27/tìm thông tin/` (`tra_ngoai_kho_2026_10_27.md`, `muc_tieu_san_pham_2026_10_27.md`), lưu kết quả
  vào `gửi chatgpt/2026-10-27/kết quả nghiên cứu/`.
- Khi bàn tính năng hội thoại nhiều lượt: bạn quyết có cho **lưu câu hỏi người dùng** không (hiện chatbot cố ý không ghi câu hỏi vào log).
- (Khi tiện) xóa 2 nhánh đã merge: `! git push origin --delete c59-log gold-v2 && git branch -d c59-log gold-v2`.

## Trạng thái

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Context 10 (B1) | đưa lên nền mới, kiểm lại đạt | merge ngay sau B0 |
| Mốc cuối 8.2 (câu kín) | kế hoạch duyệt | chạy khi bạn quyết |
| Guide / báo cáo cũ ghi sai hiện trạng | sửa xong (guide Phase 6, 8, guide chung) | tài liệu khớp hệ thống |
| Nhãn "đoạn đúng" 3 câu còn treo | 2 câu sửa, 1 giữ ⇒ thước v3 | nợ từ sáng nay xong |
| Câu nghi lỗi citation | đã kiểm: chatbot hiện tại không lỗi | lỗi chỉ có ở bản đo cũ trước khi sửa bộ kiểm |
| Sửa kho | soạn + kiểm xong; tài liệu thiết kế **bạn đã duyệt** (sau 3 vòng C kiểm) | áp sau khi đóng 8.2 |
| Cách làm (vòng cải tiến) | 3 thay đổi cho thử: script tìm trong kho luôn né bộ đánh giá; không khuyên bỏ hướng chưa đo; guide là chỗ thứ 5 phải cập nhật | theo dõi phiên sau |
| Qwen3-8B | chưa từng đo ⇒ thí nghiệm sau khi sửa kho | bạn chọn đo thay vì bỏ |
| Tính năng mới | chọn streaming trước, rồi hội thoại nhiều lượt | chỉ mới bàn; streaming cần đo "chữ đầu tiên" trước |

## Giải thích ngắn (để bạn tự nói lại được)

Kho có chỗ tự mâu thuẫn hoặc đã cũ, nên chatbot (chỉ trả lời từ kho) có thể trả lời sai theo kho. Sửa kho thì phải dựng lại index, và mọi phép đo đang
dựa trên index cũ — nên sửa sau khi đóng 8.2, và đo "trước ↔ sau" trên cùng 176 câu. Chiều nay đã làm sẵn mọi bước không đụng kho: bản sửa từng chỗ,
người thứ hai kiểm, kế hoạch dựng lại index và cách khôi phục nếu hỏng. Giới hạn: 78 mục cần nguồn bên ngoài chưa tra; 16 mục chờ bạn.

Một lần A khuyên sai: A định "đóng hẳn" Qwen3-8B vì lý do vận hành, dù chưa từng đo chất lượng — bạn hỏi lại, A rút khuyến nghị (trái nguyên tắc "thử + so
mốc trước khi chọn").

## Đọc thêm

- `bao_cao_he_thong/BAO_CAO_KHO_DU_LIEU.md` (bản 4 — đợt sửa kho) và `BAO_CAO_DANH_GIA.md` (bản 3 — thước đo, nhãn v3, mốc cuối)

- `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` (kỹ thuật)
- `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (đợt sửa kho)
