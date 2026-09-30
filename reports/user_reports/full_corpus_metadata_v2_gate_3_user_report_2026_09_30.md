# Báo cáo dành cho người dùng: Full-corpus Metadata v2 Gate 3 / Task 6

```text
Trạng thái: Đã xác nhận closure
Cập nhật lúc: 30-09-2026 +07
```

## 1. Bạn nhận được gì

Runtime retrieval toàn corpus hiện sử dụng bốn collection metadata v2 đã được
xác minh. Mỗi kết quả dùng logical chunk ID, có domain nội bộ và vẫn giữ nguyên
cách xếp hạng trên point UUID.

Startup fail closed nếu build record trỏ sai target, lineage vector-copy không
khớp exact legacy record, Qdrant invariant sai hoặc corpus hiện tại không còn
fresh. Lỗi payload malformed không đưa private source/chunk path vào error.

## 2. Hệ thống hoạt động như thế nào

Khi khởi tạo retrieval, hệ thống đọc build record metadata v2, đối chiếu exact
legacy lineage, corpus hiện tại và collection schema/count. Khi truy vấn, Qdrant
vẫn dùng point UUID cho retrieval/fusion/reranking; chỉ ở output boundary mới
map sang logical chunk ID và domain đã validate.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused regression | 116 passed | Runtime retrieval và các contract metadata liên quan không có failure trong affected scope |
| Corruption probes | Ba malformed build records đều bị reject | Startup fail closed cho target, lineage và Qdrant invariants |
| Privacy probe | Không lộ marker; exception cause rỗng | Error không chứa private source/chunk/text/path |
| No-rerank smoke | 8/8 PASS | Bốn candidates và hai retrieval treatments chạy thật trên metadata-v2 targets |
| MiniLM smoke | 2/2 PASS; p95 1386.8/1554.7 ms | Hai treatment qua reranker thật, deterministic và dưới latency gate |
| Diff hygiene | PASS | Không có whitespace error trong tracked diff |

Gate 2 full target/vector verification được reuse vì Correction 1 không mutate
collection, vector hoặc build record. Reviewer fresh-check runtime path sau
correction; không gọi evidence Gate 2 là lần chạy mới.

## 4. Cách bạn kiểm tra thêm nếu cần

Bạn không bắt buộc chạy lại kỹ thuật. Acceptance của Gate 3 không yêu cầu một
bước kiểm tra trải nghiệm người dùng riêng.

## 5. Giới hạn và bước tiếp theo

Reviewer không chạy full backend suite vì Gate 3 chỉ cho focused checks. Một
minor evidence-only không chặn là report nói có test riêng cho missing legacy
record trong khi runtime có fail-closed branch nhưng chưa có case test riêng.

Task 7, cleanup, Qdrant mutation, Phase 6 và Git commit/push vẫn chưa được mở.

User đã xác nhận closure Full-corpus Metadata v2 Gate 3 / Task 6 ngày
30-09-2026 +07. Task 7 và Phase 6 vẫn chờ authority mới.
