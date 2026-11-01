# Báo cáo cho bạn: Nghiên cứu rộng trước Phase 9 (trợ lý du lịch - văn hoá)

**Cập nhật lần cuối: 15:28 01/11/2026 — bản 1 (SƠ BỘ): từ 4 lượt tra Codex + kiểm tay; sửa theo review B118 (3 major, 5 minor) + thêm số paper C116b; chưa có kết quả ChatGPT, chưa có đề xuất hướng.**
Người viết: A · Tra + kiểm: B (thực tế, chức năng), C (paper, repo) · Review: B (B118). Tiền: 0 USD API.

## 1. Tóm tắt (bản sơ bộ — sẽ viết lại khi có kết quả ChatGPT)

- **Huế đã có trợ lý AI du lịch chính thức — "Huế TRIPO – AI Trip Planner"** (Sở VHTTDL Huế chủ trì, HueCIT phát triển, ra mắt
  31/10/2026). Tập trung vào **lập lịch trình** (theo số người lớn / trẻ em / số ngày / ngày đi; bản đồ, chỉ đường, lưu lịch trình), danh mục điểm đến, 5–6 ngôn
  ngữ, nút thuyết minh. (Ví dụ ngân sách, kéo thả, chia sẻ: A thấy khi mở trang, B mở lần khác không thấy ⇒ kiểm lại khi thử.) **Không công bố** mô hình, nguồn dữ liệu, cách kiểm câu sai; mục "chi phí dự kiến" đang "Đang cập nhật". [đã kiểm]
  ⇒ Hội đồng dễ hỏi "đồ án khác gì Huế TRIPO?". Phiên sau: bạn gõ thử ~10 câu tự viết để so (bạn chọn 01/11).
- **Người dùng muốn AI giúp tìm hiểu / lên kế hoạch, không muốn AI tự giao dịch; niềm tin là chỗ nghẽn.** Khảo sát Expedia / YouGov
  (Expedia đặt hàng — nguồn có lợi ích; 04/2026, > 5.700 người Mỹ / Anh / Ấn Độ): 53 % thoải mái để AI gợi ý, 66 % không tin AI tự đặt / mua, 68 % muốn đặt qua thương hiệu tin cậy.
  [đã kiểm] Khách Việt (Agoda 03/2026 — nguồn có lợi ích, không nêu cỡ mẫu): 81 % muốn dùng AI nhưng chỉ 28 % chủ động tin. [B kiểm] Khách bảo tàng
  từng dùng AI (Musa Guide — hãng làm phần mềm bảo tàng, nguồn có lợi ích; n = 212, trong mẫu 395 người Anh / Mỹ / Đức / Pháp): 61 % tin bảo tàng hơn AI, nhưng chỉ 27 % kiểm lại câu trả lời. [B kiểm]
  ⇒ (suy ra của A) **có nguồn + từ chối đúng + không bịa** là giá trị thật, đúng thế mạnh hue_rag.
- **Tổ chức thật chặn câu an toàn trước mô hình.** Bảo tàng Royal Armouries (Anh): câu về cháy / trẻ lạc / cấp cứu bị chặn bởi một lớp "không
  sinh", trả câu soạn sẵn đã duyệt — "mô hình không được gọi"; phần còn lại là RAG 5 đoạn, không rerank (gần hue_rag). [đã kiểm]
- **Câu sai của chatbot là trách nhiệm pháp lý của chủ.** Vụ Moffatt v Air Canada (2024): hãng phải bồi thường cho câu sai về chính sách giá,
  dẫn link đúng cũng không miễn trách. [B kiểm]
- **Lập lịch trình đầy đủ bằng LLM rất khó:** bộ đo TravelPlanner (ICML 2024) — GPT-4 chỉ đúng 0,6 % lịch trình. [C kiểm] Các bài sau (TripTailor,
  TP-RAG, TravelBench…) theo Codex thường kiểm ràng buộc bằng dữ liệu có cấu trúc / code [tự khai, chưa kiểm]. (Suy ra) kho hue_rag là Markdown, chưa có
  giờ / giá / toạ độ có cấu trúc ⇒ làm lịch trình sẽ cần thêm dữ liệu.
- **Mẫu đáng học từ mã nguồn mở** (đã đọc README): hỏi lại theo **danh sách trường cố định** (nơi đến, ngày, số người) tới khi đủ; **giá / chi
  phí tính bằng code**, không để LLM tính. [C kiểm] 8 repo trong khảo sát 01/10 đều nhỏ (0–8 sao — số sao từ GitHub API) — mẫu học, chưa
  phải bằng chứng chạy tốt. [C kiểm] (Mẫu "tách câu con" cho câu nhiều nguồn của LlamaIndex: tự khai, chưa kiểm.)
- **Tìm kiếm tiếng Việt:** bài EACL 2026 (10 bộ dữ liệu, 6 lĩnh vực) — **lai BM25 + vector (trộn tuyến tính) thắng vector đơn ở cả 10 bộ**. [C kiểm]
  (Suy ra) **cùng hướng lai** với hue_rag, nhưng cách trộn khác (hue_rag dùng RRF, BM25 chỉ chấm lại 30 đoạn dense), bài không đo e5-small và không có du lịch
  ⇒ không kết luận được cấu hình của mình tốt hay kém.
- **Agent hay pipeline có mô-đun?** Bài "Is Agentic RAG worth it?" (ACL 2026, C đọc toàn văn): agent hơn ở viết lại câu hỏi (điểm tìm 55,6 ↔
  52,8) nhưng kém ở chọn tài liệu (43,9 ↔ 49,5); ở việc quyết định có cần tìm hay không thì tuỳ bộ (kém trên FEVER F1 64,6 ↔ 87,9, hơn trên FiQA 98,8 ↔ 95,7
  và CQA-EN 99,8 ↔ 96,6); token vào gấp **2,7–3,6×**, thời gian ~1,5×; kết luận bài: không bên
  nào luôn hơn. Bài không đo câu nhiều nguồn. [C kiểm] (Suy ra) với trần 0,0005 USD / câu (đang dùng ~một nửa), agent đầy đủ dễ vượt trần.
- **Hỏi lại:** LLM tự nhận ra câu mơ hồ / thiếu thông tin còn kém; few-shot / suy nghĩ từng bước cải thiện rất ít (CLAMBER, ACL 2024, ~12.000 mẫu). [C kiểm]
  (Suy ra) câu chi phí nên dùng luật / danh sách trường rõ, không để mô hình tự quyết.
- **Nhiều lượt:** bộ đo MTRAG / MTRAG-UN (2025–2026): hệ tốt vẫn yếu ở lượt sau, nhất là câu thiếu thông tin và câu không đứng độc lập. [C kiểm]
- **Bạn cần làm:** ChatGPT trả lời xong ⇒ lưu file kết quả vào `gửi chatgpt/2026-11-01/kết quả nghiên cứu/`. Chưa cần quyết gì.

## 2. Nghiên cứu đã chạy thế nào

```text
4 mạch: (1) thực tế triển khai · (2) chức năng + người dùng cần gì · (3) paper 2023–2026 · (4) repo GitHub
  → mỗi mạch 1 lượt Codex (scripts/tra_web_codex.sh, chỉ thông tin công khai)
  → B / C tự mở trang gốc kiểm 3 ý quan trọng nhất mỗi mạch; A kiểm lại 3 ý (Huế TRIPO, Expedia, Royal Armouries)
  → yêu cầu nghiên cứu chuyên sâu gửi ChatGPT (5 phần, có "hướng nên làm / nên tránh") — đang chờ kết quả
```

**Độ tin:** Codex chạy **nông** cả 4 lượt (9–14 lượt tìm, gần như không mở trang gốc dù tự khai "đã mở") ⇒ chỉ ý ghi [đã kiểm] / [B kiểm] / [C kiểm]
là đã có người mở trang gốc; ý chưa kiểm chỉ xuất hiện khi có nhãn [tự khai]. Hồ sơ chi tiết (private): `data/nghien_cuu_phase_9_2026-11-01/`.

## 3. Bảng điều đã biết — theo mạch

| Mạch | Điều đã kiểm | Gợi ý cho hue_rag (suy ra, chưa phải đề xuất) |
|---|---|---|
| 1. Thực tế | Huế TRIPO (lịch trình, chưa công bố nguồn / kiểm sai); Royal Armouries (cổng an toàn không sinh); Air Canada (chịu trách nhiệm câu sai) | khác biệt đo được: có nguồn, từ chối ngoài kho, có số đo; câu an toàn nên đi đường riêng không qua mô hình |
| 2. Người dùng | gợi ý / kế hoạch: muốn; tự đặt: không tin (Expedia); khách Việt chủ động tin AI 28 % (Agoda, nguồn có lợi ích); khách bảo tàng dùng AI ít tự kiểm (27 %, n = 212) | niềm tin + ngày cập nhật dữ liệu quan trọng hơn thêm tính năng giao dịch |
| 3. Paper | TravelPlanner 0,6 %; lai BM25 + vector thắng (EACL 2026); agent ↔ pipeline có mô-đun: không bên nào luôn hơn, agent tốn 2,7–3,6× token; LLM hỏi lại kém (CLAMBER); nhiều lượt còn yếu (MTRAG) | lịch trình cần dữ liệu có cấu trúc; câu nhiều nguồn: so "thêm mô-đun" với "agent" theo cả chất lượng lẫn tiền |
| 4. Repo | hỏi lại theo danh sách trường; tính tiền bằng code; repo gần hue_rag nhất (`NamSyntax/vietnamese-rag-system`) không công bố số | câu dự trù chi phí (nhận xét B0): hỏi lại theo trường + tính bằng code |

## 4. Chưa biết (để phiên sau)

- Kết quả ChatGPT (5 phần) — đối chiếu với bảng trên, kiểm URL.
- Huế TRIPO trả lời câu kiến thức đúng tới đâu (bạn gõ thử phiên sau).
- Số của các paper lịch trình sau TravelPlanner, DeepNote, CORAL (C116b ghi chỗ Codex sai); chi phí vận hành thật của các tổ chức; khảo sát người dùng tại Huế (chưa tìm thấy).

## 5. Việc còn lại

1. Có kết quả ChatGPT ⇒ A viết bản 2: thực tế / chức năng / paper / repo đầy đủ + **3–5 hướng Phase 9 hợp ràng buộc của mình** + hướng nên tránh.
2. Brainstorm với bạn từng câu ⇒ chọn phạm vi Phase 9 ⇒ một tài liệu thiết kế để bạn duyệt.

## Phụ lục — hồ sơ kỹ thuật

- Việc: B117 (mạch 1–2), C116 / C116b (mạch 3–4); đợt `report_agent/2026-11-01_nghien_cuu_phase_9/`; mục "Nghiên cứu rộng Phase 9" trong `session_prompt/CURRENT_HANDOFF.md`.
- Nguồn đã kiểm: `huetripo.hue.gov.vn/trip-planner` · `ir.expediagroup.com` (thông cáo 14/04/2026 "The AI Trust Gap") ·
  `royalarmouries.org/about-us/algorithmic-transparency-record-ai-avatar-of-thomas-wardley` · Moffatt v Air Canada 2024 BCCRT 149 · arXiv 2402.01622
  (TravelPlanner) · arXiv 2601.07711 · `github.com/longstnguyen/ViRE` (EACL 2026) · README `ytthuan/trip-advisor-agent`, `KhaiBoiPho/agentic-rag`,
  `NamSyntax/vietnamese-rag-system`.
- Yêu cầu ChatGPT: `gửi chatgpt/2026-11-01/tìm thông tin/nghien_cuu_phase_9_tro_ly_du_lich_2026_11_01.md` (`e45bf409b2db`, private).
