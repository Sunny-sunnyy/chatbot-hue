# Nhật ký 02/11/2026 — giao diện web mới vào chatbot; Phase 9 thành trợ lý agent, spec duyệt

**Cập nhật lần cuối: 14:56 02/11/2026 (kết phiên).** Tiền paid trong ngày: ≈ 0,003 USD (~75 đồng) — B ≈ 0,002 (kiểm giao diện + dò SDK), C ≈ 0,0006 (review), A 0.

## Tóm tắt
- **Giao diện web làm lại và đã vào chatbot** (merge `ed8e6e8`): React + Vite + Tailwind, chỉ trang hỏi đáp + khung nguồn, nét Huế nhẹ. Nguồn hiện bằng số nhỏ bấm được; nhãn
  "Trợ lý AI… có thể sai"; lỗi luôn báo tiếng Việt. Thử 5 linh kiện shadcn / Radix dưới CSP: 2 vi phạm ⇒ không dùng gói nào. C review độc lập: đạt. API, cách tìm, model không đổi.
- **Phase 9 đổi hướng: trợ lý agent có công cụ** (bạn: "không khác RAG mức 1 thì cần gì trợ lý"). Nghiên cứu thêm (khoá AI FDE qua 3 sub-agent, ChatGPT, tra web, dò SDK thật) ⇒ mọi nguồn khuyên
  **agent dưới chính sách**: code giữ việc luôn phải xảy ra, model tự quyết phần cần phán đoán.
- **Spec Phase 9 bản 9 duyệt** (sha `169c2dd5f86a`) sau 3 vòng review độc lập (bản 6: 10 lỗi lớn ⇒ bản 8: 0). 8 bậc, mỗi bậc đo xong mới giữ / gỡ; đóng code ~20/12/2026.
- **Vòng rút kinh nghiệm:** 4 sự cố (bỏ sót file roadmap Phase 9 cũ; B đứng ~2 giờ vì lỗi lệnh chờ; làm quá tay lần 3; đọc nhầm tên file) ⇒ 3 luật mới cho thử (W46–W48).

## Bạn cần làm gì
- Bây giờ: mở phiên mới cho A, B, C. Đầu phiên sau: chọn quyền phiên; xoá nhánh `giao-dien-moi` đã merge (lệnh `!`, A đưa).
- Muốn xem giao diện mới: `cd frontend && npm ci && npm run build` (một lần), chạy API như cũ, mở `http://localhost:8000`.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Giao diện mới (B121) | vào `main` `ed8e6e8`; review C119 đạt | trang mới đang chạy; bản build không lưu trong repo |
| Hướng Phase 9 | trợ lý agent dưới chính sách (OpenAI Agents SDK 0.19.4) | không đổi framework; mẫu khoá AI FDE: trần lượt, từng công cụ một, nhớ chỉ hỏi + đáp |
| Spec Phase 9 | **bản 9 duyệt** `169c2dd5f86a` | phiên sau giao bậc B0 |
| Lựa chọn của bạn | nhớ trong cuộc trò chuyện · model viết mục "Từ web" · không giới hạn tên miền · trần 2,0 USD · dùng Serper luôn · bỏ bộ web xấu cố định | ghi ở spec §2, §10 |
| Cải tiến cách làm | W46 tìm tài liệu cũ cùng Phase · W47 mốc kiểm việc > 30 phút · W48 chống làm quá tay | cho thử; phiên sau xem có lặp không |

## Giải thích ngắn (để bạn tự nói lại được)
RAG Phase 1–8 trả lời đúng, có nguồn nhưng chỉ một lượt. Phase 9 thêm một agent định tuyến đọc câu hỏi và chọn tuyến (trò chuyện / hỏi về Huế / ngoài phạm vi / khẩn cấp); câu về Huế đi tới trợ lý có
công cụ (tìm thêm trong kho, hỏi lại khi thiếu thông tin, lịch trình nhỏ), nhớ các lượt trong cuộc trò chuyện, và khi kho không có thì code tra web, hiện riêng có nhãn. Những gì luôn phải xảy ra (ngày hôm
nay, giới hạn số lần gọi) để code làm cho chắc và rẻ. Giới hạn: tiền / tốc độ của đường agent mới chỉ là ước; điều khoản Serper chưa rõ cho người dùng cuối (bạn chấp nhận rủi ro).

## Đọc thêm
- `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` (mục 0 — bản 3), `07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` (bản 18 — giao diện), `01_LUONG_HOAT_DONG_HE_THONG.md` (bản 19)
- `docs/superpowers/specs/2026-11-02-phase-9-design.md`; `report_agent/2026-11-02_giao_dien_moi_code/TONG_HOP.md`
