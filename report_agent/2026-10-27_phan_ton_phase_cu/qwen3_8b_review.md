# Review C95: kết quả thí nghiệm Qwen3-Embedding-8B (B)

Người kiểm: C (Claude Opus 5.5, `hue-rag-0e`) · Date: 15:59 30/10/2026 (`date`) · Việc: A giao C95 30/10. Người làm: B (`hue-rag-24`). Skill `risk-gated-agent-review` + W32 (ít nhất 1 ca dò khác cách người làm).
Đầu vào (sha C tính): report `qwen3_8b_implementation.md` **`06eaaf1f66bd`**; plan `qwen3_8b_plan.md` `d6d6c7d51584` (A duyệt); dữ liệu `data/phase_8_1/g1/c78_{e5,8b}_*.jsonl`,
`data/qwen3_8b_2026-10-28/`. Chỉ đọc + tính lại; 0 USD. File tracked chỉ ghi mã câu / số đếm.

## 1. Kết luận

`ready_for_user_confirmation` — 0 blocker / 0 major / 1 minor. **"Kém hơn — không đưa vào chatbot" đứng:** sàn "0 câu mất đoạn đúng" vỡ (dev 3, ổn định qua hai lượt; test 3), các
câu mất là **mất thật** (kiểm theo cách khác B, §3), và tốc độ trượt xa luật (i) (+2,2 s trung vị so với cho phép +50 ms).

## 2. Tính lại từ file thô (script tạm `/tmp/c97/`, không dùng `g1 compare` của B)

| Kiểm | Kết quả C | So report |
|---|---|---|
| `context5_gold_all` dev 40: e5 0,600 ⇒ 8B 0,575; thắng / hòa / thua **2 / 35 / 3**; CI 95 % (`bootstrap_mean_diff`, 10.000, seed `20261024`) **[−0,125; +0,075]** | ✓ khớp |
| Câu **mất** dev: **132, 134, 135**; được thêm: 48, 70; lượt A/A 8B: mất đúng 3 câu đó, `context_gold_all` đổi **0 / 40**, top-10 đổi 27 / 108 | ✓ khớp |
| test 15: 0,600 ⇒ 0,533; 2 / 10 / 3; CI [−0,333; +0,200]; mất **33, 130, 138**, thêm 20, 21 | ✓ khớp |
| `pool_dense_gold_all` dev 0,825 ⇒ 0,775 (4 / 30 / 6); test 0,733 ⇒ 0,867 (3 / 11 / 1); MRR dev 0,731 ⇒ 0,736, test 0,700 ⇒ 0,674 | ✓ khớp |
| Số chính dev 32 (bỏ câu không tự nhiên): 2 / 28 / 2 | ✓ khớp |
| Latency **từ log request** (`queries_*.jsonl`, chỉ status 200): dev p50 / p95 **2.249 / 6.539 ms**, dev A/A 2.296 / 7.188; từ `dense_ms` dòng g1: 2.228 / 6.487 (khớp report); e5 21 / 28 ms | ✓ |
| Providers: mọi request 200 = **Nebius** (dev, dev A/A, test); build `providers_only_nebius` true, sparse **giống byte** runtime | ✓ |
| Tiền: tổng `prompt_tokens` 4 log (build + pilot 870.531; câu hỏi 6.140 + 6.140 + 2.897) = **885.708** × 0,01 USD / 1M = **0,0088571 USD** | ✓ khớp 0,008857 |
| Qdrant: chỉ còn `hue_full_corpus_7a2_e5_small_384` (`GET /collections`) ⇒ collection thử **đã xóa** (User 29/10 duyệt "xóa khi xong") | ✓ |

## 3. Ca dò khác cách B (W32): 3 câu mất ở dev có mất thật không?

B dùng `gold_coverage` (vị trí ký tự của trích dẫn ↔ `evidence_parts` của đoạn, nhãn v5). C kiểm **theo đoạn**, không dùng vị trí:
- lấy chữ của các đoạn context e5 (Qdrant runtime, chỉ đọc), tìm **chữ** trích dẫn gold trong đó ⇒ biết đoạn chứa đáp án; hỏi đoạn đó có nằm trong context 8B không, có trong 30 ứng viên
  dense của 8B không.
- **Dev 132, 134, 135 và test 33:** đoạn chứa đáp án đứng hạng 1–7 ở e5 **không có trong context 8B và không có cả trong 30 ứng viên dense của 8B** (135: cả 3 đoạn đáp án đều mất) ⇒ mất
  thật, do bước tìm theo nghĩa của 8B xếp đoạn đó thấp; không phải do cách đếm.
- **Test 130, 138:** đoạn đáp án có trong 30 ứng viên dense 8B nhưng bị trộn (RRF) xếp ngoài top-10 ⇒ cũng mất thật.
- **Nhãn:** gold v4 ↔ v5 cho cả 10 câu đổi (mất / thêm): **cùng fact, cùng chữ trích dẫn, cùng nguồn** — chỉ vị trí ký tự dời ở 3 câu (do đợt 2 sửa kho, đúng thiết kế v5); hai bên e5 / 8B
  đo cùng nhãn v5 ⇒ không phải lệch nhãn.
- (Phép tìm chữ đơn thuần còn bắt hụt ở vài câu — trích dẫn dạng bảng / vắt qua đoạn — nên C chỉ dùng nó để định vị đoạn, không thay `gold_coverage`.)

## 4. Finding

### m-1 (report §2 dòng `dense_ms` test + §3 gạch 2) — giải thích p95 test 25 s chưa đúng

- Report ghi p95 test 25 s là do "1 câu thử lại: chờ 10 s". Log `queries_c78_8b_test.jsonl`: câu lỗi là **504 sau 61,8 s** chờ (rồi thử lại thành công); ngoài ra **17 request thành công
  > 5 s**, có cái **49 s và 75 s** ⇒ p95 của request **thành công** đã là 24,8 s. Đuôi chậm do phía nhà cung cấp, không chỉ do lần thử lại. Dev cũng có 18 request thành công > 5 s
  (tới 12 s).
- **Đóng khi:** report tả đúng (504 sau ~62 s + nhiều request chậm 10–75 s ở lượt test) — làm mạnh thêm kết luận tốc độ, không đổi kết luận. Không chặn.

## 5. Ghi chú

- Mọi số "kém hơn" dựa sàn (3 câu mất, ổn định), không dựa CI (n nhỏ) — report đã ghi đúng.
- Bộ đệm `emb/` 133 MB còn giữ; xóa cần User duyệt (plan §6 bước 7) — A trình.
- File tạm `/tmp/c97/` xóa sau review.

## 6. Vòng 2 (16:01 30/10/2026 `date`): m-1 **đóng** — `ready_for_user_confirmation` 0 / 0 / 0

Report `2d9588d91962` §2 (dòng `dense_ms` test) + §3: ghi 1 lần 504 sau ~62 s rồi thử lại được, 17 request thành công > 5 s (49 s, 75 s), p95 request thành công ~25 s (24,8), dev 18
(lần 2: 13) request > 5 s — C đếm lại lần 2 = 13 ✓. `BAO_CAO_EMBEDDING_TU_KHOA.md` §4 thêm câu tương ứng (dòng 82) ✓. Quét trùng 0 cả hai file.
