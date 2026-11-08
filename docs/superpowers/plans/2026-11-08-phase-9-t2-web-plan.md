# Plan T2 — tra web thành công cụ agent tự yêu cầu (Phase 9 bản 13, đợt 2)

> **NHÁP — chờ G merge.** Chưa review, chưa code. B · 12:29 08/11/2026 (`date`). Mức nhẹ (`Session_Prompt.md` §7–§8, User 08/11): đo **1 lượt** + mốc.

Spec `2026-11-02-phase-9-design.md` §12 (User duyệt `5557f0fd7650`): hàng T2 §12.2, thiết kế §12.5, rà §12.6, User xác nhận §12.8 — **agent chỉ quyết lúc tra**; code
dựng câu tra, tra **sau** câu kho, viết mục web riêng "Từ web (chưa kiểm)"; agent **không** đọc chữ web. Nền: `main` sau G (cổng 2 nhóm) — nhánh `p9-t2-web` tách từ đó.

## 1. Đổi gì (một bậc, cờ mới `tra_web_cong_cu: false`)

1. Công cụ `yeu_cau_tra_web()` **không tham số** trong `TOOLS` của agent Huế (chỉ khi `tra_web` ∧ `tra_web_cong_cu`): đặt `trace.web_yeu_cau = True`, trả **câu cố định
   trung tính** "Đã ghi nhận — viết câu trả lời từ kho như bình thường." (không hứa mục web — tra có thể lỗi / rỗng, B6 D3; review B m-4). Trần 1 lần / câu (lần 2
   trả cùng câu, không đổi gì). Mô tả công cụ (≤ 2 câu): gọi khi câu hỏi có phần cần thông tin mà Bằng chứng không có; không gọi khi kho trả lời đủ hay câu ngoài phạm vi.
2. `web_gate_open` (**một chỗ**, `assistant.py`): thêm nhánh `flags.tra_web_cong_cu ∧ trace.web_yeu_cau ∧ fixed_outcome is None ∧ citation_error is None ∧
   answer ≠ OUT_OF_SCOPE_ANSWER` (+ mọi điều kiện cũ: tuyến `tro_ly_hue`, chưa tra, không lịch, không lượt ghép). Cổng cũ (sau câu "không đủ thông tin") giữ.
3. Không đổi: `cong_web` của B6 (câu tra do code dựng từ câu hỏi lượt này `tw.cau_tim_web`, một lần Serper, lần gọi riêng không công cụ / không lịch sử viết mục,
   mọi kiểm cuối B6), #6 (phần chạy song song không tra web; cổng chạy sau gộp), lượt biểu mẫu (không công cụ), log không chữ (`tools` thêm mục `yeu_cau_tra_web`).
4. Test 0 USD mỗi loại lượt (4c): mô tả công cụ có ở lượt đầu / lịch sử khi cờ bật, không có khi tắt (chuỗi gửi model giống byte `main`); cổng mở đúng 4 ca (yêu cầu ∧ câu
   trả lời thường ⇒ mở; yêu cầu ∧ `OUT_OF_SCOPE_ANSWER` ⇒ đóng; không yêu cầu ∧ câu trả lời thường ⇒ đóng; "không đủ thông tin" ⇒ mở như cũ); trần 1.

## 2. Tiêu chí ghi trước (1 lượt, cùng lượt với mốc `main` sau G)

| Sàn | Bộ | Mức |
|---|---|---|
| S2b ngoài phạm vi có mục web | `s2` 44 (G) | **0** |
| S2 / S3b (lời dặn đổi vì có mô tả công cụ) | `s2` 44 · an toàn 32 · mẫu 30 | 0 / 0 |
| Câu kho trả lời được mà vẫn tra web | mẫu Golden 30 + 4 câu "kho có" B6 | **0 / 34** |
| Câu kho nhắc mục web (chữ kho có "web" / "bên dưới" / "tra thêm") | mọi lượt | **0** (code đếm) |
| Câu hỏi kèm có phần web | bộ hỏi kèm 10 (xem §3) | ≥ mốc + 2 / 10 |
| Mục web đúng luật B6 | B6 đã thấy 28 + bộ hỏi kèm | 0 link ngoài sổ · 0 số / tiền ngoài đoạn trích · câu thiên tai cố định (dùng lại `data/phase_9/b6/tools/cham_b6.py`) |
| S1 an toàn | an toàn 32 | 4 số như G (S-AT khi chênh 1) |
| S4 | mẫu 30 biến thể ↔ mốc, chấm mù | tụt < 3 / 30 |
| Theo dõi | chữ đầu mục web p50 / p95 (B6: ~13 s) | báo số |

**Đạt** = mọi sàn trên. Âm ⇒ **phương án B** (spec): giữ cổng B6 (chỉ sau câu từ chối), thêm cổng cho câu "từ chối + đã hỏi kèm" do **code** nhận.

## 3. Bộ đo

- Có sẵn: `s2` (G), B6 đã thấy 28 (`data/phase_9/bo_do_b6/cau_da_thay.jsonl`), mẫu 30, an toàn 32 — công cụ `data/phase_9/g_cong/tools/do_g.py` `ca_cau` (web thật, đã có
  `context` cho S1).
- **Bộ hỏi kèm 10:** E20 (`data/phase_9/b5_v2/e20/cau_e20.jsonl`, md5 `d79ffecd2c0b`) phần lớn là "xin lịch + hỏi kèm" — cần cờ `lich_trinh` (đang tắt) ⇒ khi viết bản chính:
  kiểm câu nào dùng được với cờ hiện tại; thiếu ⇒ người **không** viết mô tả công cụ viết 10 câu "hỏi Huế + một ý kho thiếu" (đã thấy). Không bộ kín (spec §12.4 T2).

## 4. Tiền

Biến thể: (28 + 10) × 0,0018 + (34 + 32) × 0,0006 + 44 × 0,0005 ≈ 0,13 · mốc: (28 + 10) × 0,0012 + (34 + 32) × 0,0006 ≈ 0,085 ⇒ **≈ 0,21 USD** (spec §12.7 ≈ 0,19);
dừng 0,25 ⇒ A xin trước khi vượt. Ghi `usd` thật từ log.

## 5. Rà ngắn (spec §12.6 đã rà — chỉ phần chạm)

Đường ra Serper nay theo **phán đoán model** (lúc tra), nhưng truy vấn vẫn do code dựng từ câu lượt này, chữ web không vào agent chính ⇒ bộ ba chết người không mở;
câu ngoài phạm vi bị chặn ở code (`OUT_OF_SCOPE_ANSWER`) + S2b; lệnh lái trong câu người dùng ("tra web đi…") vẫn ≤ 1 lần / câu. Deploy: `tra_web` / `tra_web_cong_cu` tắt trên AWS.
