# Báo cáo dành cho người dùng: Giai đoạn 6 - OpenAI baseline (correction 4)

```text
Trạng thái: Đã cấp quyền — chờ phiên tiếp theo thực hiện replacement run
Cập nhật lúc: 01-10-2026 +07
Notebook tham khảo: notebooks/06_generation_and_api.ipynb
```

## 1. Bạn nhận được gì

Correction 4 đã đóng hai điểm cuối và toàn bộ non-paid gate đã PASS độc lập.
User đã cấp quyền ngày 01-10-2026 cho đúng một bounded replacement invocation
tối đa 5 attempted calls, đồng thời yêu cầu hoãn thực hiện sang phiên tiếp theo.
Authority đã ghi nhận nhưng chưa được tiêu thụ; chưa có paid call mới.

## 2. Hệ thống hoạt động như thế nào

Câu hỏi đi qua retrieval Metadata v2, tối đa năm nguồn bằng chứng được đóng gói,
OpenAI sinh câu trả lời một lượt, backend kiểm citation rồi chỉ trả câu trả lời
và các nguồn thực sự được trích dẫn. Nếu không đủ bằng chứng, hệ thống trả câu
fallback và không hiển thị nguồn.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused non-paid suite | 141 pass, 1 warning | Logic/runtime/integration tests đều xanh; không mock/fake provider response |
| Metadata v2 complete verify | Đạt — 33.840 points | Bốn collections vẫn nhất quán và read-only |
| Exact API startup | Đạt | `/health` HTTP 200, 5 components ready |
| `git diff --check` | Đạt | Không còn whitespace error |
| Replacement runner lifespan | Đạt | Lifespan thật chạy trên cùng async event loop |
| Evidence isolation | Đạt | Global trace đã bỏ; recorder request-scoped và giữ excerpts |
| Provider metadata edge case | Đạt | Citation failure giữ response ID/model/usage/finish metadata |
| Artifact/ASGI integration | Đạt | Production helper và actual route + real retrieval đã được kiểm non-paid |

Hai vendor assets đúng hash đã duyệt. Notebook parse được, không lưu output và
không có execution count. Không có paid call nào trong correction này.

## 4. Cách bạn kiểm tra thêm nếu cần

Bạn chưa cần tự chạy notebook hay API. Notebook hiện chỉ là tài liệu giải thích;
Run All không được dùng để thay independent correction review và không nên phát
sinh paid call ngoài contract.

## 5. Giới hạn và bước tiếp theo

Không còn correction non-paid mở. Ở phiên tiếp theo, Implementer phải kiểm
approval fingerprint và no-cost preflight trong `CURRENT_HANDOFF.md`, rồi mới
được chạy đúng một replacement sequence tối đa 5 attempted calls
(`gpt-5.4-nano`): một Representation B và bốn answer cases. Không retry, không
rerun và không call thứ sáu; failure hoặc dừng sớm phải giữ artifact và quay lại
Reviewer.

Frontend tĩnh hiện đúng canonical Phase 6. User đã xác nhận không cần chuyển
Phase 6 sang Next.js; frontend production ở phase sau phải dùng Next.js. Quyền
replacement run đã được cấp nhưng hoãn sang phiên tiếp theo và chưa tiêu thụ.
