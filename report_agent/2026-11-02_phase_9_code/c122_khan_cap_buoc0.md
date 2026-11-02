# Implementation Report: Phase 9 B0 — bước 0 khẩn cấp (C122)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-cc`)
Date: 18:37 02/11/2026 (`date`)
Căn cứ: spec Phase 9 bản 9 `169c2dd5f86a` §5 B0 "Bước 0 khẩn cấp"; mục C122 trong `session_prompt/CURRENT_HANDOFF.md`.

## 1. Phạm vi

Theo việc giao: khoảng 10 câu khẩn cấp do C tự viết, hỏi qua chatbot `main` hôm nay (`/api/chat`), để **User đọc**. C không tự kết luận "cần / không cần"
luật khẩn cấp ở B1. Không sửa code, kho hay Golden. 10 câu này sẽ dùng lại làm bộ khẩn cấp "đã thấy" của B1.

## 2. Thay đổi chính

Không đổi code chatbot. Tạo file private trong `data/phase_9/khan_cap_buoc0/`:

| File | Nội dung | sha256 (12) |
|---|---|---|
| `cau_hoi.jsonl` | 10 câu (mã `kc01`–`kc10`, loại, câu) | `32deefcca1b8` |
| `tools/chay_khan_cap.py` | gửi tuần tự, ghép dòng `chat_metrics` theo thứ tự, tính USD, kiểm câu lọt log, viết bản cho User | `f17fcff7e290` |
| `tra_loi.jsonl` | câu + HTTP + câu trả lời + nguồn + số đo log + USD | `b534222ed1af` |
| `doc_cho_user.md` | bản dễ đọc cho User, có ô đánh dấu từng câu và một đoạn "Quan sát" | `b4aca2f4770c` |

Có 10 loại câu, mỗi loại 1 câu: cháy · trẻ lạc · đuối nước (người không thở) · dấu hiệu đột quỵ · ngộ độc thực phẩm · say nắng / ngất · tai nạn giao thông chảy máu ·
bị giật đồ mất giấy tờ · lũ dâng vào chỗ ở · rắn cắn khi leo núi. Tất cả viết như người dùng thật gõ (có dấu, ở Huế), không có thông tin cá nhân.

## 3. Cách đã chạy thật

```bash
cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8841   # chạy nền
# chờ /health ⇒ 5 / 5 ready; / ⇒ 200
cd backend && PYTHONPATH=$PWD uv run python ../data/phase_9/khan_cap_buoc0/tools/chay_khan_cap.py --port 8841
# tắt server bằng TaskStop (không pkill -f); kiểm lại /health ⇒ không trả lời
```

Server đọc Qdrant `hue_full_corpus_7a2_e5_small_384` thật (8.424 point), sinh câu trả lời bằng `gpt-6-luna` thật. Commit `main` `a17a596`.

## 4. Kết quả quan sát

- 10 / 10 câu trả về HTTP 200. Có đúng 10 dòng `chat_metrics` mới (bằng số câu). Grep chữ câu hỏi trong các dòng log mới ra 0.
- **10 / 10 câu nhận đúng câu từ chối chuẩn** `INSUFFICIENT_ANSWER` (`backend/llm/full_corpus_prompt.py:3`), `refusal: true`, 0 nguồn trích, dù mỗi câu đều có 10 đoạn trong ngữ cảnh.
  Không câu nào nhắc số khẩn cấp hay cách sơ cứu. Không câu nào có hướng dẫn sai, vì không có hướng dẫn nào.
- Đếm thô trong kho (`scripts/grep_kb.sh -l -E <mẫu>`, số file; chưa đọc từng chỗ nên có thể khớp nhầm): "cấp cứu" 1 · "115" 1 · "114" 0 · "113" 0 · "đuối nước" 5 · "say nắng" 0.
- Thời gian phía client cho mỗi câu: 1,7–5,0 s.
- **Tiền: 0,0025169 USD** (giá đủ, tính từ token trong log bằng `row_cost_usd`), dưới trần 0,01 USD.

Đây là quan sát. Câu trả lời "không tìm thấy" có phải lỗi cần sửa ở B1 (luật code + câu soạn sẵn) hay không là quyết định của User: thứ tự lỗi đã chốt
đặt "sai cảnh báo an toàn" ở mức cao nhất và "từ chối nhầm" ở mức thấp nhất, còn câu khẩn cấp ngoài kho thì chưa có dòng nào trong thứ tự đó.

## 5. Lỗi và giới hạn

- Mỗi câu chạy 1 lượt. Model không tất định, nhưng câu từ chối chuẩn lặp ở cả 10 câu nên nhiều khả năng kết quả sẽ giống nếu chạy lại. Điều này chưa đo.
- Chỉ đo `/api/chat`, không đo `/api/chat/stream`. Hai route dùng chung lõi `llm.grounded_answer`, nên ở mức nội dung được xem là như nhau. Điều này cũng chưa đo.
- 10 câu do một người viết (C), nên chưa phủ hết các kiểu người dùng gõ. Phần kín cho B1 (nếu cần) viết ở C123.

## 6. Bàn giao cho người kiểm

- User đọc `data/phase_9/khan_cap_buoc0/doc_cho_user.md` (A trình).
- Chạy lại: hai lệnh ở §3, ≈ 0,0025 USD.
- C không commit. File trong `data/` là private.
