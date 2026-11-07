# Tự soi over-engineering + lộ trình — B (12:48 07/11/2026, `date`)

Thước như A / C / E. Nhãn: **[Thấy]** = B làm / đọc / đếm hôm nay · **[Suy]** = suy luận · **[Đề xuất]**.

## (1) Tốn mà lợi ít

- **Chính B hôm nay — dựng rào trước khi thử đường thật [Thấy]:**
  - Lượt biểu mẫu (D3): B viết xong đường stream + không stream, 20 test, Q1m, 3 lần Q1 (~4 phút CPU mỗi lần) **rồi mới** gọi model thật một lần.
  - Lần gọi đó lộ ngay lỗi từ chối 5/5. Nếu gọi thật 1 lượt (≈ 0,0002 USD) ngay khi đường chạy được, nguyên nhân (đoạn chỉ có dòng tên) đã lộ sớm ~40 phút.
  - Test và Q1 vẫn cần, nhưng nên đứng **sau** lượt thử thật đầu tiên.
- **Mã chết vì tính năng chưa sống [Thấy]:** `answer_bieu_mau` + nhánh stream + cờ + 20 test có thể phải sửa lại theo kết quả X1 (V2 đổi lời dặn). Đồng ý C (1).1: dựng đủ đồ trước khi biết tính năng sống là chỗ tốn nhất.
- **STATUS_B dài [Thấy]:** phần "(cũ) phiên tối 06/11" ~90 dòng vẫn nằm dưới phần mới. Mỗi phiên đọc lại mà ít dùng. Đồng ý C (2).5.
- **Cờ tắt âm** (đồng ý A / C / E): mỗi lần sửa lời dặn đều phải giữ "228 / 228 giống byte" qua các nhánh chết.

## (2) Bỏ / làm nhẹ [Đề xuất]

- **Đường mới có gọi model ⇒ 1 lượt thật nhỏ (≤ 0,001 USD) ngay khi chạy được, trước khi viết bộ test / Q1m.** Không phải bộ đo — chỉ để biết model có làm được việc không. Áp cho mọi agent; không thay luật "tiêu chí ghi trước" ở lượt đo quyết định.
- Đồng ý C (2).1, (2).3; đồng ý E: chỉ một bảng điểm.
- **Phản biện C (2).4** ("báo cáo khâu cập nhật một lần lúc đóng đợt"): User đã dặn báo cáo luôn đúng thông tin mới nhất (User 31/10) ⇒ giữ. Làm nhẹ bằng cách chỉ sửa Tóm tắt + 1 dòng, không viết lại cả khâu. Đổi luật này phải hỏi User.
- **Ảnh Commons (Q-U2):** chỉ hero + 5 ô lĩnh vực (6 ảnh), không ảnh cho từng bài. Tìm + kiểm giấy phép 204 ảnh là việc không có điểm dừng.

## (3) Giữ vì đã bắt lỗi thật [Thấy]

- **Đo 0 USD trước khi tốn thêm:** đếm độ dài đoạn của 28 điểm tìm ra nguyên nhân thật, thay vì thử thêm cách đưa khung — cách (a) đã tốn 0,0009 USD mà âm.
- **Thử phá có chủ đích:** lần phá đầu cho thấy test tổ hợp không bắt được lỗi (đổi giá trị thành rỗng thì code tự lấy lại từ nút); phải phá kiểu khác mới thấy test hoạt động. Rẻ, giữ.
- **Playwright quét mọi trang trước khi bàn giao:** bắt được 5 lỗi 404 / console, nếu không thì Q-G của C trượt.
- **"Dừng khi trượt, không thử thêm cách"** (A dặn) — B dừng D3 sau pilot.
- Hook quét trùng chạy ở cả 3 commit (0 trùng); Q1 giống byte.

## (4) Nhìn rộng tới đóng code 25–30/12

- **D3 [Suy]:** V2 (luật lịch vào lời dặn của riêng lượt biểu mẫu) từ chối 1 / 16; lời lịch do code dựng đã có sẵn khi model từ chối ⇒ người dùng không bao giờ thấy câu từ chối. B đề xuất User chọn V2 + giữ lời code dựng, để cổng đợt 1 ra sớm. Đổi lời dặn ở đây chỉ chạm đường mới, cờ tắt thì Q1 vẫn giữ.
- **Đồng ý deploy lát mỏng sớm.** Mục (5) có 3 chỗ sẽ hỏng hoặc dễ hỏng khi chạy, chưa cần build cũng thấy — đúng loại rủi ro chỉ lộ khi thử thật.
- **Trước khi gửi link cho hội đồng:** giới hạn lượt + `tra_web` tắt (E #1, #3) là bắt buộc, không phải phụ.
- Đồng ý giọng nói: mốc cắt ~20/11 (C) hoặc cắt hẳn (E) — User chọn một lần.

## (5) Review nháp deploy (`e_dep_chuan_bi_deploy.md` + `data/phase_12/deploy_nhap/`) — đọc-only, chưa build

**Blocker:** không có.

**Major**

1. **`.dockerignore` loại bảng điểm lịch trình ⇒ app không khởi động khi bật cờ lịch.**
   - `data/*` (chỉ chừa `data/full_corpus_builds`) loại luôn `data/phase_9/lich_trinh/diem_v3.json`, mà `settings.yaml:71` `lich_trinh_bang` trỏ tới.
   - `AssistantFlags.from_settings` (`backend/llm/assistant.py`, gọi đầu lifespan `api/app.py`) nạp bảng khi `lich_trinh` **hoặc** `lich_trinh_bieu_mau` bật ⇒ thiếu file thì ném lỗi ⇒ cả app không lên. Cờ biểu mẫu dự kiến bật ở S5 nếu Q-F đạt.
   - Sửa: chừa đúng file đó (`!data/phase_9/lich_trinh/diem_v3.json`) hoặc `COPY` riêng. Tương tự `anh.danh_sach` (`settings.yaml:80`) nếu sau này bật ảnh (cờ ảnh lỗi thì chỉ route 404, không chết app).
2. **`network_mode: service:qdrant` dễ vỡ [Suy — cách Docker chia mạng, cần thử]:**
   - Qdrant khởi động lại riêng (lỗi / nâng bản) ⇒ app mất mạng cho tới khi app khởi động lại tay;
   - Caddy phải gọi `qdrant:8000` (tên dịch vụ Qdrant nhưng cổng của app) ⇒ dễ nhầm khi sửa.
   - Sửa nhỏ hơn cả hai: `settings_loader` đọc biến môi trường ghi đè `vector_database.url` (vài dòng; B làm) ⇒ compose mạng thường, app gọi `http://qdrant:6335`.
   - Cùng chỗ đó nên đọc thêm ghi đè `assistant.tra_web` cho bản deploy (E #3) — một cơ chế cho 2 giá trị, không cần file settings thứ hai.
3. **Khởi động trước Qdrant ⇒ 503 mãi, không tự hồi:**
   - app kiểm Qdrant **một lần** trong lifespan (`api/app.py`, khối "1. Full-corpus retrieval service");
   - lỗi ⇒ `retrieval_ready=False` vĩnh viễn, app không chết ⇒ `restart: unless-stopped` không cứu;
   - lúc máy khởi động lại, hai container lên cùng lúc.
   - Sửa (chỉ compose): healthcheck Qdrant (vd `bash -c 'echo > /dev/tcp/127.0.0.1/6335'` — ảnh Qdrant không chắc có `curl`, cần thử) + `depends_on: {qdrant: {condition: service_healthy}}`.

**Minor**

- **Caddy `encode gzip` + SSE:** có thể gom chữ dù có `flush_interval -1` [Suy]. Khi build, kiểm bằng `curl -N` qua Caddy thấy `delta` đến dần; nếu gom thì chỉ nén HTML / JS / CSS.
- **torch CPU:** `uv.lock:3446–3448` torch `2.13.0` nguồn PyPI (không có đuôi `+cu130`) ⇒ `--torch-backend cpu` có vẻ khớp được `2.13.0+cpu`. Khi build kiểm `torch.version.cuda is None` + cỡ ảnh.
- **e5 tải một phần:** runtime gọi `snapshot_download(local_files_only=True, revision=…)` rồi so tên thư mục = revision (`embedding/full_corpus.py:103–122`) ⇒ thư mục tải sẵn đúng revision là đủ. `'*.json'` khớp cả `1_Pooling/config.json` [Suy theo fnmatch]. Kiểm bằng `/health` 5 / 5 khi build.
- **Chép `qdrant_storage` khi Qdrant đang chạy có thể ra bản hỏng** ⇒ dừng container trước khi chép, hoặc dùng snapshot.
- **Log nằm trong container** ⇒ tạo lại container là mất `chat_metrics` (cần để đo latency trên máy thật) ⇒ mount `backend/logs` ra volume.
- **Build từ working tree chính**, không từ worktree `/tmp`: ở đó `data/`, `knowledge-base-hue/` là symlink ra ngoài, `COPY` không theo.
- Ảnh có cả `knowledge-base-hue/meta/` (gồm bản sao lưu kho) — đã nằm trong cảnh báo "ảnh private", chỉ cần biết.
- `pytest` / `jupyter` / `gradio` trong deps chính làm ảnh to (đồng ý E). Chuyển sang nhóm dev phải `uv lock` lại, đụng bẫy `uv sync` sherpa ⇒ để sau; ảnh to vẫn chạy.

**Làm quá tay:** không thấy. Caddy + sslip.io, `.env` 600, `--workers 1`, Lightsail 4 GB đều là cách nhỏ nhất đủ dùng. Không nên thêm Parameter Store / Secrets Manager / load balancer cho demo.
