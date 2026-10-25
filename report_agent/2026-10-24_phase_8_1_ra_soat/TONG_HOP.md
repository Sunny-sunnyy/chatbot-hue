# Tổng hợp đợt Phase 8.1 — rà quyết định Phase 0–7 (mở 19:00 24/10, **ĐÓNG 15:27 25/10** — User "đóng 8.1")

Cập nhật: 15:27 25/10/2026 (A, đóng đợt). Kết luận và tiêu chí nghiệm thu: `phase_8_1_g5_synthesis.md`; bảng từng quyết định:
`phase_8_1_g5_decision_table_draft.md`.

## Mục tiêu
Các quyết định Phase 0–7 phần lớn do AGY / Codex chọn, ít được so trên toàn kho. 8.1 trả lời bằng số đo: lựa chọn nào kéo
chất lượng xuống, phương án nào thắng baseline và thắng bao nhiêu. **Không đổi chatbot đang chạy.** Spec
`docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` (approved 20:49 24/10, bản 4 + sửa đổi 25/10).

## Quyết định theo giờ
| Giờ | Quyết định |
|---|---|
| 24/10 20:49 | User duyệt spec 8.1 + M1 `bge-reranker-v2-m3`, M2 `Vietnamese_Reranker`; trần 0,5 USD cả 8.1 |
| 24/10 21:40–21:58 | Câu hỏi đánh giá phải tự nhiên; số chính = bỏ câu không tự nhiên |
| 25/10 11:20 | User: A điều phối rộng, API ≤ 1 USD phiên; duyệt G4-A + G4-B (pool 100); GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy |
| 25/10 11:33 | 9 câu độ tự nhiên bất đồng: giữ (natural) |
| 25/10 11:40 | Câu kín: thêm dấu cho mọi câu |
| 25/10 11:5x | `sentencepiece` cho M2; A tự duyệt thư viện nhỏ từ nay |
| 25/10 12:05–12:20 | Đáp án tham chiếu: sửa câu kín 5 đáp án + 3 câu; sửa Golden 10 đáp án (nguyên tắc: chỉ trả lời điều câu hỏi hỏi) |
| 25/10 12:27 | User nghỉ: A tự điều phối, ghi đủ thông số |
| 25/10 12:4x | A: luật tiền mỗi lượt = ước lại từ pilot, trần lượt 0,05 USD |
| 25/10 13:0x–13:4x | A duyệt plan G3 (`e089243fb612` → `9f00c460c3e9` → `d89a919067ba`, sau review B), plan G4K `d7e53186b364` (sau review C) |
| 25/10 15:15 | Mẫu câu kín bản 5: đạt; **câu không dấu ngoài phạm vi** (người dùng gõ có dấu), bỏ nghiên cứu ChatGPT |
| 25/10 15:22 | G0.6 khóa: câu kín chính thức 36 × 4 field; manifest `9ea480d0d083` (A tự kiểm 34/34 hash) |
| 25/10 15:27 | User đóng 8.1 |

## Kết quả
- **Thay (đề xuất 8.2):** context 10 đoạn — Completeness dev +0,26 [+0,08; +0,48], test +0,27 [+0,02; +0,59].
- **Giữ:** chunker (12 biến thể không tốt hơn), cách trộn, pool 30, BM25 âm tiết + k1/b, không rerank (M1/M2 kém hơn),
  prompt, reasoning effort mặc định, validator citation, thứ tự context.
- **Tín hiệu cho 8.2:** câu không dấu (13/32 → 1/32), khử dấu ở native (sparse@100 0,25 → 0,81), pool rộng, rerank luna
  (MRR +0,17), H8 (từ chối nhầm 13 → 1 nhưng phạm sàn), NFC.
- **Thước đo:** so theo cặp + Holm; 120 dev / 56 test; đoạn đúng 55 câu; độ tự nhiên 82 / 65 / 29; Golden sửa 10 đáp án
  (md5 `0f7dbf41b422`); câu kín 36 câu khóa (`sealed_official.jsonl`, User duyệt mẫu bản 5).
- Commit phiên 25/10 chiều: `2b0010b` … `91db3c9` (G1 §7 + plan `b9789f4`, G4 `ee557f9`, G2 `266c105`, G4K `50006da`, G3
  `91db3c9`). Mọi gate có review chéo ready.
- **Tiền thật:** 0,1653 USD (≈ 4.100 đồng) — chỉ `gpt-6-luna`; judge và sub-agent dùng quota Claude Code.

## Giới hạn
- Bộ thử nhỏ (32 câu dev có đoạn đúng) ⇒ nhiều "chưa rõ"; judge Claude, chưa có mốc người; câu không dấu là biến đổi máy.
- 10 câu Golden sửa đáp án không còn so trực tiếp với 7B Run 1. A đã thấy 3 câu kín (User trích).

## Bước tiếp
Phiên sau: brainstorm + một spec 8.2 (User duyệt), bắt đầu từ `phase_8_1_g5_synthesis.md` §4 — bước 0: mốc người ~20 câu +
tách khâu dính; rồi context 10, NFC, … (mục câu không dấu đã bỏ).
