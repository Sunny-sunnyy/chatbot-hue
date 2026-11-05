# Implementation Report: Phase 9 B5 — công cụ lịch trình (`lich_trinh`) — **mọi sàn B / C đo được đều đạt (kín 5 / 5 gọi công cụ); còn chờ User chấm Q3; cờ tắt; nhánh `p9-b5` `5bc45cf` (khoá `908e93b` + B5.1 + sửa C191)**

Người làm: B (Claude Opus 5.5, `hue-rag-48`) · việc **B160** (A giao 10:23 05/11/2026) · bản này 11:46 05/11/2026 (`date`).
Plan: `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 `b572443dc9cd` (A duyệt). Bảng điểm `data/phase_9/lich_trinh/diem_v3.json` `e94b7f4263f2` (User duyệt). Trần 0,15 / dừng 0,14 USD.
Nhánh `p9-b5` từ `main` `b019aab`, worktree `/tmp/b_b5`; commit `2c7acce` (code) → `0970d96` (sửa sau pilot) → **`908e93b` = khoá** (vòng chỉnh 1; kín chạy trên khoá này) → **`5f0a1a3` B5.1** (sửa D8 (1) sau kín, A quyết — §2b). Đã push, chưa review, **chưa merge**.
Report tracked, repo public: không chép câu bộ đo / nội dung kho; câu ví dụ tự viết. Dữ liệu: `data/phase_9/b5/` (private). B không mở câu kín.

## 1. Đã làm

**Ý chính (khung FDE: trường bắt buộc / phép tính ⇒ code):** model chỉ trích tham số (số ngày, người đi cùng, kiểu đi, sở thích, điểm muốn ghé); **code** xếp lịch theo buổi từ bảng điểm, tự hỏi số ngày khi thiếu, lấy tài liệu từng điểm, kiểm cuối chữ model. Model chỉ viết lời theo khung.

| File | Thay đổi |
|---|---|
| `backend/llm/lich_trinh.py` (mới) | nạp + kiểm bảng (`nap_bang`), khớp tên (`khop_diem`), chốt số ngày (`chot_so_ngay`, D15), xếp lịch (`xep`, D2–D4), kiểm luật độc lập (`kiem_khung`), khung chữ đưa model (`khung_chu`), khối "Ghi chú của lịch" do code nối (`khoi_ghi_chu`, D4b), dòng "Mình hiểu" (`dong_minh_hieu`, D12), link bản đồ (`map_url`, D11), kiểm cuối (`kiem_cuoi`, D8 (1)–(7)) |
| `backend/llm/do_so.py`, `so_tien.py` (mới) | dò số ngày trong câu (D12 (b)); dò số tiền (D8 (3), B5c dùng lại) |
| `backend/llm/assistant.py` | cờ `lich_trinh` + bảng; công cụ `lich_trinh_for_turn` (≤ 1 lần / câu; thiếu số ngày ⇒ code trả thẻ hỏi lại); `_lay_nguon_lich` (D6); sau khi có khung, `tim_kho` trả "đã đủ tài liệu" không tìm thật (vòng chỉnh 1); `_finish_generated` ghép + kiểm cuối ⇒ hỏng thì rút lại như citation hỏng; stream: bước tiến độ (D14), sự kiện `lich_trinh` (bản đồ + thẻ Sửa) |
| `backend/llm/generator_openai_full_corpus.py` | `tool_use_behavior` dạng hàm `_dung_khi_hoi_lai`: công cụ trả thẻ ⇒ dừng lượt (D15) |
| `backend/llm/full_corpus_prompt.py` | `LICH_TRINH_MO_TA` (mô tả công cụ), `LICH_TRINH_LUAT` (luật trình bày đầu khung), `TOOL_DA_DU_LICH` |
| `backend/llm/hoi_lai.py` | gỡ phần công cụ `hoi_lai` của B4 (C183 m-2); giữ bảng trường + `the_hoi_lai` + `ghep_cau` |
| `backend/retrieval/full_corpus_context.py` | `LICH_TRINH_TOOL_OVERHEAD = 359` (đo ở pilot, D16) |
| `backend/api/routes/chat.py` | log `lich_trinh_ok / so_diem / kiem / buoc` (không chữ); `ChatResponse.lich_trinh`; SSE `lich_trinh` |
| `backend/config/settings.yaml` | `lich_trinh: false`, `lich_trinh_bang` |
| `frontend/src/App.jsx`, `index.css` | danh sách bước tiến độ; "Bản đồ từng điểm" (chỉ nhận link đúng gốc Google Maps); nút "Sửa" mở thẻ chọn sẵn |
| `backend/tests/test_b5_lich_trinh.py` (mới, 68 test); `test_b4_hoi_lai.py` gỡ | test mỗi luật cố tình vi phạm, mỗi dạng giờ / tiền, mỗi loại lượt (W55), chặn tìm thêm sau lịch |

**Lệch plan (B tự quyết, chi tiết nhỏ):** (a) dò số ngày đặt ở `do_so.py` riêng (B5c thêm số người cùng chỗ); (b) harness đo private `data/phase_9/b5/tools/chay_b5.py` + `chuoi_b5.py` + `q8_b5.py` (như B4); (c) "4+" ⇒ xếp 4 ngày + câu giả định; (d) Q8 chạy trước kín (không phụ thuộc kết quả kín); (e) ca "kiểm luật lỗi" trên giao diện: thử 5 bảng giả, `xep` vẫn ra khung đúng luật ⇒ không dựng được ca lỗi thật mà không giả `xep` ⇒ kiểm bằng test cố tình vi phạm của `kiem_khung` + nhãn giao diện `kiem_luat_loi` không có "✓" (đọc code `assistant.py` `lich_trinh_for_turn`, `App.jsx` `LICH_BUOC`).

## 2. Kết quả (bằng chứng chạy thật)

| Mốc | Tiêu chí ghi trước | Kết quả | |
|---|---|---|---|
| Test | — | 129 passed; 1 error = test cần khoá API thật (bẫy đã biết); `npm ci && npm run build` | đạt |
| **Q1** | cờ tắt ⇒ chuỗi gửi model giống byte `main` | 228 / 228 | đạt |
| **Q1m** | cờ bật, câu không lịch ⇒ chỉ khác một mục công cụ | 228 / 228 | đạt |
| Bước 0 (D6) | ≥ 26 / 28 điểm có đoạn đúng file top-10 | 28 / 28 (hạng 0) | đạt |
| Pilot 3 + 2 câu | ước tiền + D16 | D16 = 359; L2 chạm `max_turns` ⇒ sửa luật trình bày | — |
| Đã thấy 13 v1 | Q2a ≥ 9 / 10, Q2 0 lỗi, ngoài Huế 3 / 3 | đạt cả ba; nhưng qua server L2 chập chờn `max_turns`, TD2 (hỏi giờ sau lịch) gọi lại công cụ ⇒ rút lại | ⇒ vòng chỉnh 1 |
| **Vòng chỉnh 1** (A chọn (a)+(b)) | — | code chặn `tim_kho` sau khi có khung + mô tả công cụ "chỉ khi tin nhắn cuối nhờ lên / sửa lịch" | ⇒ **khoá `908e93b`** |
| **Đã thấy 13 v2** (khoá) | như trên | Q2a 10 / 10 · kiểm cuối 0 · lỗi khung 0 · ngoài Huế 3 / 3 · `max_turns` 0 · chênh token max 76 | đạt |
| **Chuỗi v2** (server thật, cookie) | TL1 / TL2: thiếu số ngày ⇒ thẻ ⇒ "Trả lời luôn" ⇒ 0 hỏi lần hai, lịch 1 ngày + dòng giả định; D14 khớp | đạt; D14 16 / 16; TD2 / TD4 / TD5: 0 lần gọi lại, 0 rút lại; log không chữ | đạt |
| **Q4 Golden 30** | F1–F4 | sạch; hỏi lại 0 | đạt |
| **Q4 an toàn 32** (2 judge, cổng đối chứng 10 / 10 · 0 / 5 cả hai) | 4 số | đảo cảnh báo mới 0 · sai điều kiện mới 0 (hết 2) · ngoài kho bị trả lời 0 · **thiếu cảnh báo mới 3** | ⇒ S-AT |
| **S-AT** (ghi trước: 3 B5 + 3 mốc mỗi câu, 2 judge mới mù bên; đạt ⇔ B5 ≤ mốc mọi câu) | | thiếu cảnh báo B5 ↔ mốc: câu 1 **2 / 3 ↔ 3 / 3**, câu 2 **0 / 3 ↔ 1 / 3**, câu 3 **3 / 3 ↔ 3 / 3**; sai điều kiện 0 / 18 | **đạt** |
| S-NHAM | gọi `lich_trinh` nhầm ≤ 1 / 62 | 0 / 62 | đạt |
| Rút lại D8 (7) | ≤ 1 / 62 | 0 / 62 | đạt |
| **Q8 cổng** (≥ 2 lượt) | 1 câu lịch + 1 thường + 1 ngoài Huế; log không chữ | lượt 1: câu lịch **bị rút lại** (model ghi sai số nguồn của một điểm — kiểm cuối bắt đúng, hiện "Thử lại"); lượt 2: cả 3 đạt; 0 dòng log có chữ câu hỏi | đạt (xem §3) |
| **Q8 Playwright** | bước tiến độ đúng thứ tự, "bỏ … vì …", bản đồ, Sửa, CSP 0 | 5 bước đúng thứ tự (xếp → kiểm ✓ → bỏ điểm ngoài bảng → lấy tài liệu); link bản đồ 2 / 2 và 4 / 4 đúng gốc; "Sửa" chọn sẵn 2 giá trị ⇒ đổi 2 ngày ⇒ lịch mới 4 điểm; câu thường không có bước / bản đồ; điện thoại không cuộn ngang; CSP 0; yêu cầu ra ngoài 0 | đạt |
| **Kín 5 câu** (C chạy trên khoá `908e93b`) | Q2a ≥ 4 / 5; Q2 sàn code | Q2a **5 / 5** · giờ / giá / khung / lệch nhãn / `max_turns` 0 · chênh token 26–139 · 0,0046 USD · **kiểm cuối rút lại 1 / 5** (điểm ngoài khung) — C đọc tay: **báo nhầm** (tên một điểm bảng nhắc như ngữ cảnh lịch sử khi tả điểm trong khung; model không xếp thêm điểm) | **đạt theo nội dung (A quyết)**; lần rút nhầm ghi là giới hạn Q5; kín không chạy lại; sửa ở B5.1 |
| **Q3 (User chấm 5 lịch kín)** | cả 3 tiêu chí ≥ 4 / 5 | **chưa có** — chờ User | — |

### 2b. B5.1 — sửa D8 (1) sau kín (A quyết 05/11, commit riêng `5f0a1a3`)

- **Đổi:** `lich_trinh.py` `kiem_cuoi` — mục (1) "điểm ngoài khung" chỉ xét tên điểm ở **đầu một dòng lịch** (dòng mở bằng gạch đầu dòng / số thứ tự / nhãn Sáng · Chiều · Tối / tiêu đề ngày; phần trước dấu tách đầu tiên, đã bỏ ngoặc) qua `_dau_dong_lich` + `_ten_da_xep`. Tên điểm nhắc trong lời tả không còn bị bắt. Mục (4) trích dẫn vẫn xét mọi dòng. Chỉ chạy khi cờ bật ⇒ Q1 (cờ tắt) không đổi.
- **Test (câu tự viết, không dùng chữ kín):** lời tả kiểu "từng là trung tâm của Kinh thành …, gần …" ⇒ 0 lỗi (luật cũ bắt 3 tên); **cố tình vi phạm vẫn bị bắt:** điểm ngoài khung ở dòng buổi có gạch đầu dòng, nhãn buổi in đậm, nhãn buổi kèm ngoặc giờ, tiêu đề ngày, danh sách số, và "…, sau đó ghé <điểm ngoài khung>" cùng dòng. Test B5 74 passed.
- **Đã thấy 13 chạy lại trên `5f0a1a3`** (0,0094 USD, `data/phase_9/b5/da_thay/v3.jsonl`): Q2a 10 / 10 · kiểm cuối 0 · lỗi khung 0 · rút lại 0 · ngoài Huế 3 / 3 · `max_turns` 0 · chênh token max 326. So luật cũ ↔ mới trên 30 câu trả lời đã lưu (v1, v2, v3): **khác 0 / 30** (luật mới không bỏ lọt gì luật cũ bắt ở đã thấy).
- **Sửa theo review C191 (vòng 1, `5bc45cf`, 0 USD):** M-1 — sau B5.1, điểm ngoài khung lọt ở 5 dạng dòng (tiêu đề `###`, dòng bảng `| Tối | … |`, emoji / `>` đầu dòng, nhãn buổi đứng riêng rồi tên ở dòng sau) ⇒ "chỗ xếp lịch" nay gồm dòng mở bằng mọi ký hiệu không phải chữ / số, ô của dòng bảng có ô nhãn buổi / ngày, dòng ngay sau nhãn đứng riêng. Mỗi dạng một test vi phạm (+ câu văn "Buổi tối, bạn ghé …"); test lời tả B5.1 vẫn 0 lỗi; ca dò của C bắt cả 5; so 30 câu đã lưu khác 0 / 30. m-1 — "Đang xếp lịch…" chỉ còn là nhãn trạng thái, không vào danh sách bước (Playwright Q8 cũ thấy 5 dòng gồm dòng này ⇒ nay 4). m-2 — test route: lượt có giá trị ⇒ câu ghép tới model, trường / giá trị lạ ⇒ 422. m-3 — giữ `kiem_ghi_chu` (sàn Q2 đo bằng nó, harness + test dùng chung), ghi lý do. m-4 — bỏ dòng trống cuối. Test B5 + giao diện tĩnh 84 passed.
- **Giới hạn:** tên điểm ngoài khung viết trong **đầu dòng** sau dấu phẩy mà là lời tả ("Lăng A, nơi từng là … của Kinh thành [5]") vẫn bị bắt nhầm; điểm ngoài khung viết **sau** dấu tách đầu tiên của dòng lịch ("— chiều ghé thêm X") không bị (1) bắt — lời vẫn phải qua (4) và (2) giờ.

Dữ liệu: `data/phase_9/b5/{pilot,da_thay,chuoi,chuoi_v2,q1,q4,q8}/`; S-AT `data/phase_9/b5/q4/an_toan/` (`compare_main.json`, `compare_regen.json`, `sat_thieu_regen.json`).

## 3. Theo dõi / giới hạn (không phải sàn)

- **Rút lại do kiểm cuối:** đã thấy v2 0 / 13, chuỗi v2 0, kín 1 / 5 (báo nhầm D8 (1) — sửa ở B5.1, §2b), Q8 1 / 4 câu lịch qua server (model trích số nguồn của tài liệu khác cho một điểm). Kiểm cuối chặt là thiết kế (thà rút lại còn hơn trích sai); nếu kín / người dùng thật thấy rút lại nhiều ⇒ cân nhắc chỉ đổi số nguồn bằng code thay vì rút lại (việc mới, cần plan).
- **Golden: 1 câu trong phạm vi bị từ chối mới** — model dùng hết 2 lượt tìm thêm rồi trả "không đủ thông tin"; không gọi `lich_trinh`; B4 / B4b trả lời được câu này. Điểm TB Completeness 4,80 → 4,63, Accuracy 4,97 → 4,80 (n = 30, chủ yếu do câu này). Không phải sàn ghi trước; [suy luận] mô tả công cụ thứ hai làm model đổi cách tìm ở vài câu — theo dõi trên Golden đủ khi bật cờ thật.
- **Q4 chỉ câu đơn:** câu hỏi tiếp sau một lịch (TD) chỉ đo ở chuỗi đã thấy (5 chuỗi) — theo dõi khi bật.
- **Chất lượng chữ:** model chép gần nguyên khung (ít lời dẫn); đúng luật nhưng khô — User xem ở Q3.
- Câu thiếu cảnh báo câu 3 thiếu cả ở mốc 3 / 3 ⇒ lỗi sẵn có (không do B5), đã có từ B3.

## 4. Tiền

Pilot 0,0045 · đã thấy v1 0,0098 · chuỗi v1 0,0086 · đã thấy v2 0,0095 · chuỗi v2 0,0105 · Q4 sinh 0,0323 · S-AT 0,0094 · Q8 0,0057 · B5.1 đã thấy 0,0094 ⇒ **B5 (B) ≈ 0,0997** + kín C 0,0046 ⇒ **≈ 0,104 / 0,15**. Judge: quota Claude (sub-agent). Không gọi `agy`.

## 5. Việc còn

User chấm Q3 ⇒ C review nhánh `p9-b5` (gồm B5.1 `5f0a1a3`) ⇒ A merge (cờ tắt hay bật theo Q3). Kết quả âm (Q3 < 4 / 5) ⇒ cờ tắt, tag `hoso/p9-b5`.

**Giải thích ngắn:** Trợ lý giờ có thể xếp lịch tham quan Huế theo buổi. Phần dễ sai (số ngày, giờ mở cửa, điểm nào hợp với người lớn tuổi / trẻ em, nguồn của từng điểm) do code làm từ bảng điểm User đã duyệt; model chỉ viết lời theo khung, và code kiểm lại chữ cuối — sai thì rút lại thay vì đưa lịch sai. Đo trên câu thường và câu an toàn: không làm tệ hơn bản đang chạy (thủ tục S-AT đạt). Còn chờ User chấm 5 lịch kín.
