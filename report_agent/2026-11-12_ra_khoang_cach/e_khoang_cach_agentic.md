# Rà khoảng cách tới "agentic RAG" + repo / paper mới — phần của E

Người viết: E · 19:11 12/11/2026 (`date`) · A giao (User giao 18:58 và bổ sung 19:02 12/11/2026) · **0 USD API** (2 lượt Codex tra web + 1 agent con chỉ đọc + 8 lần mở trang kiểm = quota).
Hồ sơ private: `data/nghien_cuu_agentic_2026-11-12/` (yêu cầu gửi Codex, biên bản đọc lại file repo cũ) · kết quả tra: `data/tra_cuu_cli/2026-11-12_e-agentic-rag-thanh-phan/`, `data/tra_cuu_cli/2026-11-12_e-paper-agentic-du-lich/`.
Nhãn dùng trong bài: **[code]** = E đọc code trên `main` hôm nay · **[log]** = E đếm trên log số đo có sẵn · **[đã mở]** = E tự mở trang gốc kiểm · **[Codex]** = Codex báo đã mở, E chưa mở lại · **[chưa kiểm]** = chỉ thấy ở kết quả tìm.
Không viết spec / code. Mọi "ứng viên" dưới đây là **đề xuất**, chưa có bằng chứng đo trên hue_rag trừ chỗ ghi rõ.

## 1. Trả lời ngắn: hue_rag đã là "agentic RAG" chưa?

**Không có nguồn nào đặt ngưỡng tối thiểu** để gọi một hệ là agentic RAG (Codex tìm không ra; E mở kiểm 2 nguồn chính). Vì vậy câu trả lời đúng là mô tả theo thành phần:

- Theo **bài khảo sát Agentic RAG** (arXiv 2501.09136, bản 4 ngày 01/04/2026 **[đã mở]**): agentic RAG = "nhúng agent tự chủ vào đường RAG", với 4 mẫu: **dùng công cụ · tự soát lại · lập kế hoạch · nhiều agent phối hợp**. hue_rag có đủ mẫu 1; có mẫu 2 ở dạng "model tự quyết tìm thêm" + kiểm bằng code; **không có** mẫu 3 (model lập kế hoạch) và mẫu 4 (nhiều agent phối hợp).
- Theo **Anthropic "Building effective agents"** (19/12/2024 **[đã mở]**): cả "luồng cố định do code điều khiển" lẫn "agent tự điều khiển" đều là *hệ agentic*; khuyên chọn cách đơn giản nhất, chỉ thêm phức tạp khi cần. hue_rag = **luồng cố định (định tuyến ⇒ tìm ⇒ kiểm ⇒ cổng web) có một vòng agent nhỏ ở giữa** (trợ lý tự gọi công cụ, có trần).

**Câu nói được khi trình bày:** "hue_rag là agentic RAG mức một-agent-có-công-cụ đặt trong luồng do code kiểm soát; phần lập kế hoạch nhiều bước và tự soát bằng model chưa có — và chưa có lỗi đo được nào đòi phải có." Hai chỗ thiếu **đáng lấp** không phải thêm agent, mà là (a) **đo đường đi + độ ổn định** của vòng agent đang có, (b) **kiểm nghĩa** của trích dẫn (mục 4).

## 2. Bảng khoảng cách

| Thành phần (nguồn) | hue_rag có gì (`file` · hàm) **[code]** | Thiếu gì | Lỗi tương ứng đã quan sát ở hue_rag? |
|---|---|---|---|
| **Định tuyến** (Adaptive-RAG; LlamaIndex xếp vào "agentic đơn giản") | 1 lần gọi model, đầu ra có cấu trúc 4 tuyến — `llm/assistant.py` `_pick_route`, `llm/generator_openai_full_corpus.py` `RouteOutput`; lỗi / quá hạn ⇒ về tuyến Huế; chạy song song phần trả lời (`answer_turn_stream_parallel`) | định tuyến theo **độ khó** (câu dễ 1 lần tìm ↔ câu nhiều ý) — không có; mọi câu Huế đi cùng một đường | chưa: câu dễ không bị chậm vì vòng công cụ (model tự quyết). Có dao động định tuyến giữa các lần chạy (đã ghi ở các lượt đo câu ngày) |
| **Viết lại câu tìm** | đã thử 2 biến (định tuyến viết câu tìm) — kém hơn câu gốc ⇒ bỏ; code còn giữ cờ `lan_tim_dau` | — (đã bỏ có số đo) | — |
| **Tách câu nhiều ý** (arXiv 2507.00355 **[Codex]**: +36,7 % MRR@10 trên bộ nhiều bước tiếng Anh) | model tự đặt câu tìm thêm ≤ 2 lần — `tool_for_turn` (`MODEL_SEARCH_LIMIT = 2`), `search_into_trace` nối sổ nguồn, bỏ đoạn trùng | không tách **trước**; không trả lời **từng ý** (ý nào kho có thì trả, ý nào thiếu thì nói) | **có**: câu xin một việc + hỏi kèm ⇒ bị từ chối cả câu 3 / 4 (bộ hỏi kèm 06/11); từ chối nhầm ~3 % dồn ở câu nhiều nguồn / so sánh |
| **Chấm đoạn tìm được rồi mới tìm lại / từ chối** (CRAG **[Codex]**; "Sufficient Context" ICLR 2025 **[đã mở]**) | ngữ cảnh rỗng ⇒ code từ chối, không gọi model (`prepare_answer`); còn lại **model tự phán** đủ / thiếu rồi tìm thêm hoặc trả câu từ chối cố định; từ chối ⇒ cổng web (`web_gate_open`) | không có bước chấm "đủ bằng chứng chưa" tách riêng; không biết một lần từ chối là do **tìm trượt** hay do **model không dùng đoạn đúng** | **một phần**: **[log]** trong 222 lượt câu Huế thành công có ghi tiền, 65 lượt model tự tìm thêm; nhóm tìm đủ 2 lần kết thúc bằng từ chối 31 / 41, và 21 lượt còn cố gọi lần thứ 3 (bị trần chặn). Log trộn nhiều bộ đo (có bộ cố ý hỏi điều kho thiếu) ⇒ đây là **dấu hiệu để đếm tiếp**, chưa phải tỉ lệ lỗi |
| **Tự kiểm căn cứ câu trả lời** (Self-RAG; "Correctness is not Faithfulness" **[đã mở]**: tới 57 % trích dẫn không trung thực trong thí nghiệm của bài) | kiểm bằng **code**: mã trích dẫn phải có trong sổ nguồn (`check_citations`), kiểm cuối lịch trình (`_finish_generated` ⇒ `lich_trinh.kiem_cuoi`), kiểm số / tiền / link của mục web (`tra_web.kiem_muc_web`); hỏng ⇒ rút câu trả lời | câu trả lời **từ kho** chưa kiểm nghĩa: `[3]` có thật nhưng đoạn 3 có nói điều đó không thì chưa kiểm; không có bước model tự soát | **ít**: khi đã trả lời, điểm đúng ~4,96 / 5; "nói chắc sai mới" = 0 ở các lượt đủ bộ. Chưa từng **đếm** số tiền / giờ trong câu trả lời có nằm trong đoạn được trích không |
| **Nhiều công cụ** | `tim_kho`, `thoi_tiet` (`thoi_tiet_for_turn`), `ngay_lich` (`ngay_lich_for_turn`, phần lớn đã thay bằng lịch code tính sẵn `_nguon_lich_san`), `lich_trinh` (cờ tắt; biểu mẫu do code gọi `answer_bieu_mau`), tra web do **code** mở cổng (`cong_web`) | công cụ tra bảng có cấu trúc (vé / giờ) — đã thử, đóng hồ sơ; web do model tự gọi — đã thử, âm | có ở các lần thử cũ (model gọi sai lúc / gọi rồi vẫn từ chối) ⇒ là lý do chuyển việc cho code |
| **Lập kế hoạch nhiều bước** (khảo sát; ATLAS **[Codex]**) | không có model lập kế hoạch; lịch trình do **code** xếp (`llm/lich_trinh.py`), model chỉ diễn đạt | bộ lập kế hoạch cho câu phức tạp | chưa quan sát lỗi nào cần nó; lịch trình câu gõ tự do thử 2 lần chưa đạt là do luật xếp / bảng điểm, không do thiếu bộ lập kế hoạch |
| **Trí nhớ** | 3 **câu hỏi** gần nhất, RAM, 30 phút — `api/conversations.py` (`MAX_TURNS = 3`, `TTL_SECONDS`); không nhớ câu trả lời (cờ `nho_cau_tra_loi` tắt) | tham chiếu tới **câu trả lời trước** ("quán thứ hai bạn vừa kể"); sở thích dài hạn | theo thiết kế (bản nhớ câu trả lời từng mượn nhầm đoạn của đối tượng khác); chưa đếm người dùng hỏi kiểu này bao nhiêu |
| **Nhiều agent** | 5 "vai" model riêng lời dặn (định tuyến · trả lời có công cụ · trò chuyện · viết mục web · diễn đạt biểu mẫu), **code** nối, không agent nào giao việc cho agent nào | agent điều phối / agent con | chưa — và mọi nguồn đều khuyên không thêm khi một agent đủ |
| **Hỏi lại người dùng / người xác nhận** | thẻ nút hỏi số ngày do code quyết (`_finish_generated` nhánh `clarify`, `llm/hoi_lai.py`); ảnh: gợi ý chờ bấm xác nhận; nút 👍 / 👎 | hỏi lại cho câu **mơ hồ** ngoài lịch trình | chưa đếm |
| **Phục hồi khi hỏng** | định tuyến lỗi ⇒ tuyến Huế; chạm trần vòng ⇒ câu từ chối cố định (`max_turns`); lỗi công cụ ⇒ câu lỗi; web lỗi ⇒ câu cố định | — | — |
| **Đo theo đường đi + độ ổn định** (Anthropic 09/01/2026 **[đã mở]**: pass^k = mọi lần trong k lần đều đạt; nên chấm *kết quả* hơn là ép đúng chuỗi công cụ; "Beyond pass@1" 31/03/2026 **[Codex]**) | log mỗi lượt đủ để đo: `route`, `tools` (tên, ai gọi, số đoạn mới, hết lượt), `n_llm_calls`, `usd` — `api/routes/chat.py`; ma trận nhầm tuyến đã đo ở bậc định tuyến; an toàn chạy ×2 | **chưa có phép đo "cùng một câu chạy k lần ra cùng kết luận"** cho hỏi đáp (pass^k mới chỉ có trong harness sửa lịch đang hoãn); chưa có bảng "loại câu ⇒ đường đi kỳ vọng" cho các công cụ mới | **có dấu hiệu**: một câu Golden từ chối ngẫu nhiên, một câu ngày kém ổn định qua 3 lượt, dao động định tuyến |

## 3. Repo + paper đã xem (mỗi mục một dòng)

**File `báo cáo nghiên cứu github.txt`:** agent con đọc hết 757 dòng — file nêu 8 repo + 1 bài báo, **cả 9 đã đọc ở 04/11** (E đối chiếu danh sách URL: khớp) ⇒ **không còn repo chưa đọc**. Phần còn hở chỉ là vài file trong repo `agentic-rag` (bộ đo agent tất định + trường log "tầng nào quyết") — ý đã gom vào ứng viên 1.

| # | Nguồn (ngày) · nhãn | Ý chính | Áp vào khâu | Lỗi đã thấy ở hue_rag? | Đã có / đã bỏ? |
|---|---|---|---|---|---|
| R1 | LlamaIndex Corrective RAG workflow (tài liệu hiện hành) **[Codex]** | chấm đoạn ⇒ lọc ⇒ viết lại câu tìm ⇒ web | tìm / kiểm | một phần (mục 2 dòng 4) | viết lại câu: đã bỏ; web sau từ chối: đã có |
| R2 | LangGraph "custom RAG agent" **[Codex]** | agent tự quyết lúc gọi bộ tìm | tìm | — | đã có (`tim_them`) |
| R3 | `sirrj4rvis/Grounded` (MIT, 1 sao) **[Codex]** | tách câu trả lời thành mệnh đề, lọc mệnh đề không có căn cứ; tự báo: ảo giác 34,9 % ⇒ 13,1 % nhưng **mất 21,5 % nội dung đúng** | kiểm | ít | chưa có; cảnh báo đánh đổi |
| R4 | `Liyan06/MiniCheck` (Apache-2.0, EMNLP 2024) **[đã mở]** | bộ kiểm "câu này có được tài liệu hỗ trợ không", model 770M chạy máy; trang chỉ có ví dụ tiếng Anh, **không ghi hỗ trợ tiếng Việt** | kiểm / đánh giá | ít | chưa có; rủi ro tiếng Việt + RAM |
| R5 | `ENDEVSOLS/LongTracer` (19/05/2026) **[Codex]** | kiểm mệnh đề bằng so nghĩa + NLI, không gọi LLM; không có số đo tiếng Việt | kiểm | ít | chưa có |
| R6 | `juhyunohh/FlexTravelBench` **[Codex]** | bộ đo lịch trình thêm ràng buộc qua nhiều lượt | đánh giá lịch trình | sửa lịch đang hoãn | bộ chuỗi sửa lịch riêng đã có (10 + 5) |
| R7 | `longstnguyen/ViRE` + bài EACL 2026 **[Codex]** | so BM25 / dense / lai trên 6 miền tiếng Việt; lai thường tốt nhất | tìm | — | đã có (lai dense + BM25 + RRF, đã đo trên nhãn riêng) ⇒ chỉ dùng làm **trích dẫn** cho quyển báo cáo |
| R8 | 3 repo trợ lý du lịch nhiều agent (0 sao, không số đo) **[Codex]** | mẫu cấu trúc | — | — | không dùng |
| R9 | NVIDIA RAG Blueprint (Codex báo đã lưu trữ 05/11/2026) **[Codex]** | agentic path mặc định **tắt**, vì tăng số lần gọi + độ trễ | — | — | củng cố lựa chọn hiện tại |
| P1 | Khảo sát Agentic RAG, arXiv 2501.09136 (bản 4, 01/04/2026) **[đã mở]** | 4 mẫu: soát lại · kế hoạch · công cụ · nhiều agent. Câu "chưa có phân loại thống nhất" Codex trích: **[chưa kiểm]** (không có trong phần tóm tắt) | khung trình bày | — | dùng cho mục 1 |
| P2 | "Sufficient Context", ICLR 2025 **[đã mở]** | tách 2 lỗi: ngữ cảnh thiếu ↔ model không dùng ngữ cảnh đủ; model nhỏ "bịa hoặc từ chối cả khi ngữ cảnh đủ"; từ chối có chọn lọc tăng 2–10 % tỉ lệ đúng | kiểm / đánh giá | **có** (từ chối nhầm) | chưa có phép tách này |
| P3 | "Can Small LMs Use What They Retrieve?", arXiv 12/03/2026 **[đã mở]** | model ≤ 7B không rút được đáp án 85–100 % số lần dù đoạn đúng có trong ngữ cảnh (trên câu nó không tự biết) | sinh | chưa đo với model đang dùng | lý do **đếm trước** khi thêm bước tìm lại |
| P4 | "Correctness is not Faithfulness", ICTIR 2025 **[đã mở]** | trích dẫn "đúng" chưa chắc là nguồn model thật sự dựa vào; tới 57 % | kiểm | chưa đếm | kiểm số trong đoạn trích: đã có ở mục web, chưa có ở câu kho |
| P5 | Flex-TravelPlanner, arXiv 05/06/2025 **[đã mở]** | làm tốt một lượt **không** báo trước được việc sửa nhiều lượt; thứ tự nêu ràng buộc đổi kết quả; model bỏ ràng buộc cũ khi có ý mới | lịch trình | lần thử Huế TRIPO thấy đúng lỗi này ở trang khác | sửa lịch: code có, hoãn |
| P6 | ATLAS (Google, 2025) **[Codex]** | quản ràng buộc + phê bình kế hoạch, TravelPlanner 17,8 ⇒ 44,4 % | lịch trình | — | ràng buộc do code giữ: đã có; nhiều agent: không làm |
| P7 | AbstentionBench, arXiv 10/06/2025 **[Codex]** | 20 bộ câu "không trả lời được" (thiếu thông tin, tiền đề sai, lỗi thời); model suy luận kém từ chối hơn | đánh giá | chưa có nhóm "tiền đề sai / đúng chủ đề thiếu chi tiết" | bộ ngoài kho đã có; nhóm này chưa |
| P8 | "Beyond pass@1", arXiv 31/03/2026 **[Codex]** + Anthropic evals 09/01/2026 **[đã mở]** | đo độ ổn định qua k lần chạy; lưu đường đi | đánh giá | có dấu hiệu | chưa có cho hỏi đáp |
| P9 | KiRAG, ACL 2025 **[Codex]** | tìm lặp theo bộ ba tri thức, +9,4 % R@3 trên câu nhiều bước | tìm | — | gần GraphRAG ⇒ thuộc nhóm "không làm" |
| P10 | Bài về hỏi đáp di sản phi vật thể tiếng Việt (tạp chí ĐH Cần Thơ, 09/11/2026) **[chưa kiểm]** — trang không mở được | bộ 4.719 cặp hỏi đáp | trích dẫn liên quan cho quyển báo cáo | — | cần mở lại trước khi trích |

Không nguồn nào đã mở cho thấy cần thêm reranker, GraphRAG hay nhiều agent cho cỡ kho này (đều nằm ở dòng "Không làm" của handoff — giữ).

## 4. Ứng viên xếp hạng (≤ 8) — mỗi cái có "đếm rẻ trước khi xây"

| Hạng | Ứng viên | Lợi cho người dùng | Lỗi đã thấy chưa | Đếm rẻ trước (theo luật "đếm lỗi trước khi xây") | Nguồn |
|---|---|---|---|---|---|
| **1** | **Đo độ ổn định + đường đi của bản đang chạy** (không xây tính năng): mỗi câu chạy 3 lần, báo "3 / 3 cùng kết luận" theo loại câu; bảng loại câu ⇒ công cụ kỳ vọng | cùng một câu hỏi không lúc trả lời lúc từ chối | có dấu hiệu (3 chỗ, mục 2 dòng cuối) | **0 USD:** lượt an toàn ×2 + S2 ×2 của B7 giữa kỳ đã cho 2 lần / câu ⇒ đếm câu đổi kết luận giữa 2 lần; chỉ khi ≥ 3 câu đổi mới chạy thêm lần 3 trên ~30 câu (≈ 0,02 USD) | P8, bộ đo agent của repo đã đọc |
| **2** | **Tách "tìm trượt" ↔ "model không dùng đoạn đúng" cho mọi câu từ chối nhầm** (phép đếm, chưa phải tính năng) | quyết đúng hướng sửa từ chối nhầm (~3 %) | **có** | **0 USD:** trên Golden của B7 giữa kỳ, với mỗi câu trong kho bị từ chối: đoạn đúng (nhãn sẵn có) có nằm trong ngữ cảnh model nhận không; model đã tìm thêm mấy lần | P2, P3 |
| **3** | **Kiểm số tiền / giờ / ngày trong câu trả lời kho ⊂ đoạn được trích** (code, không model; sai ⇒ thêm dòng cố định, không rút câu) | không nói sai giá vé / giờ mở cửa — lỗi User xếp nặng | chưa đếm | **0 USD:** chạy bộ đếm số sẵn có (`llm/so_tien.py`, bộ đếm chuỗi số của `llm/tra_web.py`) trên 176 câu trả lời của B7; ≥ 3 câu có số "lạ" mới xây | P4, R3 (cảnh báo mất nội dung đúng) |
| **4** | **Câu nhiều ý: trả lời ý kho có + nói rõ ý kho thiếu** (từng ý một, ý thiếu mới mở cổng web) | hết cảnh hỏi 2 ý bị từ chối cả câu | **có** (3 / 4 ở bộ hỏi kèm) | **0 USD:** trong các câu bị từ chối ở B7 + log, đếm câu có ≥ 2 ý mà ngữ cảnh chứa đáp án ít nhất một ý. **Rủi ro đã biết:** "trả lời một phần" ở Phase 8 làm câu ngoài kho bị trả lời; "web do model gọi" âm ⇒ nếu làm thì **code** tách ý + giữ sàn ngoài kho | tách câu hỏi (arXiv 2507.00355), P2 |
| **5** | **Trần tìm thêm thông minh hơn**: tìm lần 2 không ra đoạn mới liên quan ⇒ dừng, từ chối sớm (bớt chậm + tiền); hoặc ngược lại cho lần 3 nếu ứng viên 2 chỉ ra "tìm trượt" là chính | nhanh hơn ở câu kho không có | dấu hiệu: 31 / 41 lượt tìm đủ 2 lần vẫn từ chối; 21 lượt đòi lần 3 **[log]** | làm sau ứng viên 2 (cùng phép đếm, tách theo bộ) | CRAG, R9 |
| **6** | **Nhóm câu đo "đúng chủ đề nhưng kho thiếu đúng chi tiết" + "tiền đề sai"** (~15 câu tự viết, người viết ≠ người sửa lời dặn) | đo chỗ model dễ bịa nhất | chưa có nhóm này | ≈ 0,01 USD một lượt; ≥ 1 câu bị trả lời bịa ⇒ có việc để sửa | P7, repo RAG tiếng Việt đã đọc |
| **7** | **Sửa lịch nhiều lượt** (code đã có trên nhánh hoãn) | "bỏ điểm X", "ngày 2 chỉ đi chiều" | chưa có dữ liệu người dùng thật | không đếm được trước khi có người dùng ⇒ chờ deploy + nút góp ý | P5 |
| **8** | **Nhớ câu trả lời có kiểm đúng đối tượng** | hỏi "cái thứ hai bạn vừa kể" | theo thiết kế | đếm trên bộ chuỗi có sẵn loại hỏi tiếp: bao nhiêu lượt cần đúng nội dung câu trả lời trước (0 USD) | — |

**Không đề xuất (đã có / đã bỏ / không có lỗi):** viết lại câu tìm, reranker, GraphRAG / tìm theo bộ ba, lọc theo lĩnh vực (đã đếm, không mở), nhiều agent, model tự lập kế hoạch, web do model gọi, bộ kiểm nghĩa bằng model NLI (chưa có bản tiếng Việt kiểm được; tốn RAM máy 15 GB), gợi ý cách hỏi dưới câu từ chối (đã có từ 08/11).

## 5. Khuyến nghị thứ tự (đề xuất cho A tổng hợp)

Ứng viên **1, 2, 3 đều là phép đếm 0 USD trên chính kết quả B7 giữa kỳ** ⇒ làm ngay sau khi B7 có số, trước khi chọn xây gì. Kết quả đếm quyết: (2) nghiêng "model không dùng đoạn đúng" ⇒ sửa lời dặn / cách đưa ngữ cảnh, **không** thêm vòng tìm; nghiêng "tìm trượt" ⇒ xét ứng viên 5 hoặc thử lại xếp lại ở 10 đoạn (ứng viên cũ từ bài 16). Ứng viên 4 là thứ duy nhất vừa có lỗi đã thấy vừa đổi trải nghiệm rõ, nhưng có hai lần thử âm liên quan ⇒ cần thiết kế riêng.

## 6. Giới hạn

- Hai lượt Codex: 26 + 22 trang mở được; E tự mở kiểm 8 trang (4 Anthropic / arXiv về khung + 4 về ứng viên hạng cao). Số liệu của các mục nhãn **[Codex]** chưa được E đối chiếu.
- Số **[log]** lấy từ `backend/logs/application.log` (trộn lượt đo của nhiều bộ + pytest; đã lọc lượt thành công có ghi tiền) ⇒ chỉ là dấu hiệu.
- Không chạy code repo nào; không gửi câu nào tới chatbot; không mở câu kín, không đọc nội dung kho.
- Agent con chỉ đọc file repo cũ; E kiểm 3 khẳng định của nó (số nguồn trong file, bộ đo agent của repo, tính năng gợi ý cách hỏi đã có) — 1 ý nó đề xuất bị loại vì đã có.
