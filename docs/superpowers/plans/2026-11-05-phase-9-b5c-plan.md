# Plan B5c — tính tiền bằng code (`tinh_tien`)

Người viết: C · **bản 2** 10:19 05/11/2026 (`date`, việc **C181b**: sửa theo review B vòng 1 `68a4f8e13690` — M-1 theo A quyết "code tự hỏi như B5 D15", M-2 đường vé, m-1…m-6) · bản 1 `65e43944e014` (C181; D5 A quyết (a); bản sao private `data/phase_9/tinh_tien/b5c_plan_ban1_65e43944e014.md`). Chưa B kiểm phần sửa / chưa A duyệt sha, chưa code, 0 USD (§6: A đã chọn tiền (a), "Trả lời luôn" giữ 1 người 1 ngày). Chỗ đổi cuối file.
Nền: spec Phase 9 **bản 12 `77250689e605`** (User duyệt) §11.1 dòng B5c + §11.2 + **lệch dòng B4b — User 10:07 05/11/2026 "Merge cờ tắt + code tự hỏi"**; mở nhánh `p9-b5c` từ `main` **sau khi B5 merge** (spec §11.4: bậc đường trả lời lần lượt). Mức rủi ro: trung bình (đổi đường trả lời sau cờ) — `run-experiment` (tiêu chí ghi trước) + `practical-project-coding`.
File tracked, repo public: không chép kho / Golden / câu bộ đo; mô tả dữ liệu ở **mức loại**; tên điểm là tên công khai; câu ví dụ tự viết.

**Mã dùng trong file:** bảng dự toán = 3 bảng của file chi phí du lịch (`travel/services`): **1 ngày (5 hạng mục, không lưu trú) · 2 ngày 1 đêm (6) · 3 ngày 2 đêm (6)** × 3 mức (tiết kiệm / tiêu chuẩn / thoải mái), mỗi ô là khoảng A–B **cho một người** · bảng vé = **bảng vé lẻ của file vé Quần thể Di tích Cố đô** (`travel/tickets`, mục vé lẻ: tên điểm, giá người lớn đồng / người / lượt, giá trẻ em với điều kiện **7–12 tuổi** ghi ở tiêu đề cột, "miễn phí"; ngày hiệu lực ở đầu file) · D… = quyết định plan này · Q… = tiêu chí · S1–S5 = 5 sàn spec §11.2 · B4b = plan B4 bản 8 `69afbb2732cf` (merge cờ `hoi_lai` tắt) · B5 = plan B5 bản 7 `b572443dc9cd` (A duyệt) · g2 = chuỗi chi phí "gõ số người + số ngày sau thẻ hỏi lại" bị hỏi lại 4 / 4 ở B4 (`b144_b4_implementation.md` §2f).

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| file này | toàn bộ | đủ 5 sàn + quyết spec §11.2; mỗi lượt có tiêu chí ghi trước; quyết định có lý do + "sai khi"; tiền, dừng |
| spec Phase 9 bản 12 `77250689e605` | §11.1 dòng B5c + "Chi tiết để plan B5c" (§11.4), §11.2, §11.3, §11.5 | chép đúng sàn / quyết / phạm vi dữ liệu; vé ↔ tham quan một lần |
| `session_prompt/CURRENT_HANDOFF.md` dòng "User chọn (10:07 05/11/2026)" | quyết định "Merge cờ tắt + code tự hỏi" | D7 không mở công cụ `hoi_lai` cho model |
| `data/phase_9/tinh_tien/kiem_ke_gia.md` (`deb4a0eff9c8`, private) + file kho (đọc **chỉ** qua `scripts/grep_kb.sh --dir travel/services …` / `--dir travel/tickets …`) | §1–§3; file chi phí: mục cách tính tổng, tham quan, 3 bảng dự toán, quy mô nhóm; file vé Quần thể: đầu file (ngày hiệu lực), bảng vé lẻ | D2 (phạm vi), D3 (luật cộng), D4 (vé ↔ tham quan), D5 (lưu trú), D2b (vé) bám đúng chữ kho |
| `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` **bản 7 `b572443dc9cd`** | D2 (`khop_diem`, bảng điểm `quan_the`), D4b (khối code nối), D8 (3) (`so_tien.py`), D12 (dò số ngày), D14 (dòng tiến độ), **D15** (code tự hỏi + `tool_use_behavior` dạng hàm + "Trả lời luôn"), D16 (ngân sách mô tả công cụ), Q1m | B5c dùng chung, không viết hai bản |
| `report_agent/2026-11-02_phase_9_code/b144_b4_implementation.md` §2e, §2f, §2g + `b157_b4b_review.md` (m-1: đường `truong` không gắn cờ) | lỗi Q6k (b), g2, S-AT B4b | D7 không tái lỗi g2; Q4 có thủ tục S-AT ghi trước |

## 1. Mục tiêu và phạm vi

- **Vấn đề (đã thấy):** B4: lời dặn "không cộng tổng" (Cách A) không chặn được model tự nhân / cộng ⇒ Q6k (b) kín phạm (§2e); câu chi phí gõ chữ số người / ngày sau thẻ bị hỏi lại lần hai 4 / 4 (g2, §2f); thêm công cụ + lời dặn vào **mọi** lượt trợ lý (B4b) ⇒ câu an toàn thiếu cảnh báo nhiều hơn mốc (§2g). B4b merge cờ tắt ⇒ câu chi phí hôm nay = hành vi `main` (không hỏi lại, không tính).
- **Làm:** công cụ `tinh_tien` — **code** đọc bảng dự toán + bảng vé lẻ Quần thể đã nạp từ kho, **code** nhân / cộng theo số người / ngày, **code** dựng bảng có `[n]` + ngày nguồn; model chỉ viết lời quanh bảng (khung AI FDE §2). Thiếu số người / ngày ⇒ **code** trả thẻ hỏi lại (như B5 D15), **không** công cụ `hoi_lai` cho model.
- **Không làm:** giá phòng / xe cụ thể; tiền ăn theo quán (giá món không ngày nguồn — `kiem_ke_gia.md` §1); dự toán ≥ 4 ngày (kho không có bảng); chi phí đến / rời Huế (kho không có số); **vé ngoài bảng vé lẻ Quần thể** (vé gộp / combo, điểm ngoài Quần thể, biểu diễn, Hải Vân Quan — mỗi file một dạng bảng ⇒ không nạp; câu hỏi các vé này đi đường hôm nay: trả lời có nguồn từ kho, **không có tổng do code**); chính sách miễn / giảm theo đối tượng (chỉ nhắc bằng câu cố định); đặt chỗ; ghi kho.
- **Phụ thuộc:** B5 merge (dùng chung `do_so.py` (D6), `so_tien.py` (D9), `khop_diem` + bảng điểm (D2b), khối code nối D4b, dòng "Mình hiểu" + nút Sửa D12, cơ chế dừng `tool_use_behavior` + "Trả lời luôn" D15, dòng tiến độ D14); B4b merge (đường `clarify` / `truong` / thẻ — không gắn cờ, `b157_b4b_review.md` m-1).

## 2. Quyết định thiết kế

| Mã | Quyết định | Vì sao | Sai khi / chọn khác mất gì |
|---|---|---|---|
| **D1** | Công cụ `tinh_tien(loai: Literal["du_toan", "ve"], diem: list[str] ≤ 5, muc_chi: Literal[3 mức] | None)` cho agent trợ lý, **≤ 1 lần / câu** (đếm trong code như `tim_kho`), `extra="forbid"`. **Số người / số ngày không phải tham số model** — code điền (D6). Mô tả công cụ ngắn + luật trình bày nằm **trong kết quả công cụ** (như B5 D7 bản 6) — **không** thêm lời dặn hệ thống | khung FDE §3; bài học B4b §2g (lời dặn vào mọi lượt đổi câu khác) | model gọi nhầm ở câu không phải chi phí ⇒ Q4 S-NHAM; gọi `ve` cho câu dự toán ⇒ bộ đo có ca này |
| **D2** | **Dự toán:** `so_ngay` 1 / 2 / 3 ⇒ bảng 1 ngày / 2N1Đ / 3N2Đ. Nạp lúc khởi động bằng parser bảng Markdown của **đúng một file** (đường dẫn `settings.yaml`), kiểm schema: **1 ngày 5 hạng mục, 2N1Đ và 3N2Đ 6 hạng mục** (review B m-1) + dòng tổng; mỗi ô là khoảng hợp lệ; **tổng kho = tổng code cộng lại từ hạng mục ở cả 9 ô tổng** (B đã đếm 9 / 9 khớp, 0 USD) — lệch ⇒ không khởi động | dữ liệu có cấu trúc thì code đọc được; kiểm tổng bắt parser sai / kho đổi | kho đổi định dạng ⇒ không khởi động (ưu tiên hơn số sai) |
| **D2b** | **Vé (review B M-2):** nạp **chỉ bảng vé lẻ của file vé Quần thể** (12 dòng). Schema kiểm lúc khởi động: cột tên điểm, giá người lớn, giá trẻ em (tiêu đề cột ghi điều kiện **7–12 tuổi** — code đọc nguyên chuỗi điều kiện từ tiêu đề, không tự viết), ô giá là số hoặc "miễn phí"; **ngày hiệu lực** đọc từ dòng "ngày có hiệu lực" đầu file (regex ngày; không thấy ⇒ không khởi động). **Khớp tên:** khoá mỗi dòng = phần tên in đậm + bí danh trong ngoặc của ô tên, nối với bảng điểm B5 bằng `khop_diem` (NFC + casefold + bỏ hậu tố " Huế" khi ≥ 2 chữ, khớp nguyên tên, `ten` / `ten_khac`); lúc khởi động **mỗi điểm `quan_the` của bảng điểm (11 id) phải khớp đúng một dòng vé**, không thì không khởi động. Tên model gửi không khớp ⇒ câu cố định "chưa có giá vé của <tên> trong bảng vé lẻ" (không đoán). **Trẻ em:** code nhân **chỉ khi** người dùng cho số trẻ (D6) — bảng in nguyên điều kiện tuổi của cột + câu cố định "trẻ ngoài độ tuổi này và các đối tượng miễn / giảm: xem chính sách trong nguồn [n]"; số trẻ không rõ ⇒ liệt kê giá người lớn + trẻ em, **không tổng** | một bảng, một dạng — kiểm được; bảng có đúng một mức giá trẻ em / dòng với điều kiện ở tiêu đề ⇒ nhân có căn cứ | vé gộp rẻ hơn mua lẻ ⇒ tổng lẻ không phải mức rẻ nhất ⇒ khối ghi chú có câu cố định "có vé tuyến gộp, xem nguồn [n]"; điểm ngoài Quần thể ⇒ không có tổng code (giới hạn ghi ở báo cáo) |
| **D3** | **Phép tính dự toán:** mỗi hạng mục: cận thấp × `so_nguoi`, cận cao × `so_nguoi` (ô bảng đã là **một người**); tổng = cộng **riêng từng cận** (theo mục cách tính của chính file: cộng thấp với thấp, cao với cao, không lấy số giữa rồi nhân theo ngày); không cộng chi phí đến / rời Huế ⇒ dòng cố định "chưa gồm đến / rời Huế". `muc_chi` thiếu ⇒ hiện **cả 3 mức** (không hỏi). **Có trẻ em trong dự toán (review B m-3):** `so_nguoi` = **tổng số người** (người lớn + trẻ), kèm câu cố định "mức cho trẻ em có thể khác — kho không ghi số riêng; nên hỏi trực tiếp phụ thu trẻ em" (đúng ý mục gia đình có trẻ nhỏ của kho) | đúng luật của chính file; tất định | tổng có thể cao hơn thật khi có trẻ nhỏ — câu cố định nói rõ |
| **D4** | **Vé ↔ hàng "tham quan" — một khoản một lần:** mục "Tham quan" của file kho dặn lấy **một khoản chung cho cả chuyến** thay vì chép giá vé từng điểm ⇒ `du_toan` dùng hàng tham quan của bảng, **không** cộng vé; `ve` chỉ khi người dùng hỏi vé — bảng vé riêng, **không có dòng cộng vào dự toán**. Câu hỏi cả hai ⇒ hai bảng riêng + câu cố định "khoản tham quan trong dự toán đã là khoản dự trù cho vé, không cộng thêm" | spec §11.4 "một khoản một lần"; đúng luật kho | người muốn "tổng gồm vé thật" ⇒ không có (nói rõ) |
| **D5** | **Lưu trú khi số người lẻ / đi một mình** [suy ra từ số kho, khớp đúng ở **một** mức — B đã kiểm lại]: ô lưu trú một đêm mức tiêu chuẩn = đúng nửa khoảng giá phòng tầm trung kho ghi (mức tiết kiệm không khớp nửa giá phòng bình dân) + ghi chú dưới bảng 2 ngày 1 đêm (phòng hai người thì chia đôi trước khi ghi vào cột mỗi người) ⇒ bảng có vẻ giả định **hai người một phòng**; mục quy mô nhóm dặn người đi một mình không được coi như có người ở chung để chia tiền phòng. ⇒ `so_nguoi` = 1 hoặc lẻ: dòng lưu trú vẫn tính theo bảng **kèm câu cố định** "bảng tính theo người khi ở chung phòng; đi một mình / số người lẻ thì tiền phòng mỗi người có thể cao hơn — kho không ghi số cụ thể" (code nối, D8). **A quyết (a)** (giữ số kho + câu lưu ý) | không tự nhân đôi (suy luận của C, không phải số kho) | (b) bị bỏ: dòng lưu trú "chưa đủ dữ liệu" ⇒ tổng thấp hơn thật |
| **D6** | **Số người / số ngày — thứ tự lấy giá trị:** (1) `truong` từ nút (lượt ghép — giá trị do code, không đọc chữ ghép); (2) **dò số** trong câu hiện tại + câu gốc lượt trước (nhớ chỉ câu hỏi — B3b) bằng **`backend/llm/do_so.py`** — **B5 tạo module này từ đầu với hàm dò số ngày (B báo khi review vòng 2); B5c chỉ thêm dò số người** (một chỗ dò số — review B m-6); (3) thiếu ⇒ D7. **Mẫu dò** (NFC, chữ thường): số ngày `(\d+|một…mười) ngày`; `(\d+)\s*n\s*(\d+)\s*đ` và **`(\d+|chữ) ngày (\d+|chữ) đêm`** (review B m-2: đêm ≠ ngày − 1 ⇒ ngoài bảng ⇒ ngoài phạm vi); "nửa ngày" ⇒ ngoài phạm vi; số người `(\d+|một…mười) (người|khách|bạn|thành viên)`; `(\d+|chữ) người lớn …(\d+|chữ) trẻ em` (tách người lớn / trẻ); "vợ chồng / cặp đôi / hai đứa" ⇒ 2; "một mình / mình tôi" ⇒ 1; "gia đình (\d+|chữ) người". **Nhiều giá trị khác nhau** cho cùng trường ⇒ không dò; số người > 20 ⇒ ngoài phạm vi | khung FDE §3; nguyên nhân g2: thẻ hỏi lại không biết số người dùng đã gõ (§2f) | câu viết lạ ("cả nhà", "cuối tuần") ⇒ không dò ⇒ hỏi (đúng — không đoán) |
| **D7** | **Code tự hỏi — không công cụ `hoi_lai` cho model** (A quyết theo User 10:07 05/11/2026; review B M-1; cùng cơ chế B5 D15): `tinh_tien` được gọi ⇒ code lấy `so_nguoi` (dự toán và vé) / `so_ngay` (dự toán) theo D6 ⇒ **thiếu** ⇒ kết quả công cụ mang dấu "cần hỏi" ⇒ `tool_use_behavior` dạng hàm (của B5 D15) dừng lượt ⇒ route phát `clarify` loại `chi_phi` **chỉ với trường còn thiếu** (`the_hoi_lai` của B4b, `outcome = hoi_lai`). Trường + nút: `so_nguoi` **1 · 2 · 3 · 4 · 5 · 6+** (6+ ⇒ ô số, `TruongInput.so_nguoi` = số nguyên **1–20**, `Field(ge=1, le=20)`, ngoài khoảng ⇒ 422 — **Lệch** tập B4 D2 cũ {1, 2, 3-4, 5+}: khoảng không nhân được), `so_ngay` {1, 2, 3, 4+} (4+ ⇒ ngoài phạm vi D2), `muc_chi` 3 mức (không bao giờ hỏi). **Lượt mang `truong` không bao giờ hỏi lần hai** (D15 B5): `truong` rỗng ("Trả lời luôn") / thiếu trường ⇒ **chỉ trường vẫn thiếu sau D6** (vd câu gốc có "2 ngày" ⇒ giữ 2) được code đặt tạm `so_nguoi = 1` / `so_ngay = 1` + dòng giả định code "Mình tạm tính cho … — bấm Sửa để đổi" (chỉ nêu trường tạm) (dòng "Mình hiểu" B5 D12 ghi "(tạm)"). **Không** lưu `outcome` lượt vào `conversations.py` (bản 1 cần để chặn hỏi lần hai — nay lượt ghép luôn mang `truong` nên không cần) | User chọn "code tự hỏi"; B4b cho thấy để model quyết hỏi làm đổi hành vi câu khác; g2 hết vì code dò số trước + lượt ghép không hỏi lại | câu chi phí mà model **không gọi** `tinh_tien` ⇒ không ai hỏi, model trả lời như `main` ⇒ sàn Q2a (gọi công cụ) + D9 chạy mọi câu khi cờ bật; "Trả lời luôn" ⇒ tổng 1 người 1 ngày có thể không đúng ý — dòng giả định + nút Sửa |
| **D8** | **Bảng + chữ do code:** `tinh_tien` trả model **khung** (luật trình bày + số đã tính + ngày nguồn + mã luật lưu ý); code nối **bảng Markdown** (hạng mục / điểm · cận thấp – cao hoặc giá × số người · `[n]` đoạn bảng) + dòng tổng (chỉ khi đủ dữ kiện, D2–D3, D2b) + khối "Ghi chú" (dùng chung D4b B5: chưa gồm đến / rời Huế · hạn mức lập kế hoạch, không phải giá niêm yết · ngày đối chiếu / ngày hiệu lực · D2b / D3 / D4 / D5 / D7 nếu áp dụng · "có thể đã thay đổi" B1). Model viết 1–3 câu quanh bảng, **không nhắc lại số** | model chép số dễ sai / tự nhân thêm (B4) | khối máy móc; chữ model trùng ý ⇒ đếm (Q6) |
| **D9** | **Kiểm cuối** (sau sinh, như kiểm citation; bộ nhận số tiền `backend/llm/so_tien.py` của B5 — chuẩn hoá "1,5 triệu" ↔ "1.500.000"): (1) mọi số tiền trong **chữ model** ∈ {số trong đoạn kho được trích} ∪ {số code tính} — S1 — **chạy mọi câu trợ lý khi cờ bật** (cả câu không gọi `tinh_tien` — câu chi phí model tự nhân vẫn bị bắt); (2) chữ "tổng / tổng cộng / cả chuyến / tất cả" + số tiền trong chữ model ⇒ hỏng (tổng chỉ do code nối); (3) mã trích ∈ sổ nguồn. Hỏng ⇒ như citation hỏng (rút lại + lời báo + "Thử lại") | S1 / S2 phải do code bắt, không judge (B4: judge coi phép nhân là "có") | (1) báo nhầm khi kho viết số dạng khác — chuẩn hoá; (1) chạy mọi câu ⇒ rút nhầm câu thường ⇒ Q4 "rút lại ≤ 1 / 62" |
| **D10** | **Nguồn `[n]`:** đoạn chứa bảng (dự toán đúng số ngày; vé lẻ) lấy như B5 D6: `retrieval_service.search(<tiêu đề mục>)` ⇒ chọn đoạn đầu có `source` + `heading_path` đúng ⇒ thêm vào sổ nguồn (dùng lại `[n]` nếu đã có); không thấy ⇒ không hiện bảng (câu cố định) | mỗi số có trích dẫn thật | tiêu đề trùng ⇒ điều kiện `source` + `heading_path` chặn |
| **D11** | **Cờ** `assistant.tinh_tien: false` (mặc định = hành vi `main` sau B5); bật ⇒ công cụ `tinh_tien` (mô tả ngắn) + D9 + nút chi phí của thẻ — **không** công cụ `hoi_lai`, **không** lời dặn hệ thống mới. Ngân sách token: lược đồ + mô tả `tinh_tien` đi kèm **mọi** lượt trợ lý khi cờ bật ⇒ hằng `TINH_TIEN_TOOL_OVERHEAD` cộng vào `extra_tool_tokens` (như B5 D16), đo ở pilot. Mô tả / khung không dùng ví dụ địa danh / số thật (ý #12) | gỡ được (S5); một chỗ khác `main` (Q1m) | — |
| **D12** | **Dòng tiến độ** (dùng chung D14 B5): bước code thật của `tinh_tien` ⇒ `trace.buoc_tinh` ⇒ `status` `stage = tinh_tien`: `nap_bang` (đã chọn bảng), `tinh_xong`, `thieu` {truong}, `ngoai_pham_vi` {ma}; xét tên công cụ ở nhánh `tool_called` / `tool_output` (m-6 B5) | demo thấy code tính; không bước giả | — |

## 3. Thay đổi theo file (dự kiến)

| File | Thay đổi |
|---|---|
| `backend/llm/tinh_tien.py` (mới) | parser + kiểm schema bảng dự toán (D2) và bảng vé lẻ (D2b), `du_toan`, `ve` (D2b–D5), `khung` / `bang_markdown` / `ghi_chu` (D8), `kiem_tien` (D9) — hàm thuần |
| `backend/llm/do_so.py` (**B5 tạo** — có `do_so_ngay`) | B5c thêm `do_so_nguoi` (+ người lớn / trẻ em) + mẫu "X ngày Y đêm" (D6) |
| `backend/llm/so_tien.py` (của B5 — dùng lại) | không đổi; `kiem_tien` gọi |
| `backend/llm/hoi_lai.py` | `Loai` thêm `chi_phi` **chỉ cho `the_hoi_lai`** (dữ liệu thẻ do code dựng); trường / nút D7; `TruongInput` thêm `so_nguoi` (1–20) + `muc_chi` — **không** đổi công cụ `hoi_lai` (cờ tắt, B4b) |
| `backend/llm/assistant.py` | đăng ký `tinh_tien` sau cờ; đếm ≤ 1; D6 + D7 (dấu "cần hỏi", "Trả lời luôn"); nối bảng + ghi chú (D8); `kiem_tien` sau sinh mọi câu khi cờ bật (D9); `buoc_tinh` (D12) |
| `backend/llm/generator_openai_full_corpus.py` | `_assistant_for`: thêm `tinh_tien`; `tool_use_behavior` dạng hàm của B5 thêm nhánh `tinh_tien` "cần hỏi" ⇒ dừng |
| `backend/retrieval/full_corpus_context.py` | `TINH_TIEN_TOOL_OVERHEAD` (D11) |
| `backend/config/settings.yaml` | cờ `tinh_tien: false` + đường dẫn file chi phí + file vé Quần thể |
| `backend/api/routes/chat.py` | log `tinh_tien` {loai, so_nguoi_tu (nut / do / thieu / tam), ngoai_pham_vi, kiem} — số / nhãn, không chữ |
| `frontend/src/App.jsx` | nút `so_nguoi` 1–6+ và ô số khi 6+ (D7); nhãn tiến độ `stage = tinh_tien` (D12); bảng là Markdown sẵn có |
| tests | `test_b5c_tinh_tien.py`: parser bảng thật (5 / 6 / 6 hạng mục; tổng kho = tổng code 9 / 9); phép tính từng mức × 1 / 2 / 3 ngày × 1 / 2 / 5 người (so số tính tay); có trẻ em trong dự toán (đếm đủ + câu cố định); **vé:** 11 điểm `quan_the` khớp đúng một dòng, bí danh khớp, tên lạ ⇒ câu cố định, "miễn phí", người lớn + trẻ em có số ⇒ tổng, trẻ không rõ số ⇒ không tổng, ngày hiệu lực có trong khối ghi chú; ngoài phạm vi (4+ ngày, "2 ngày 2 đêm", > 20 người, vé gộp / điểm ngoài Quần thể) ⇒ câu cố định + 0 tổng; **dò số: bảng §3b**; D7: thiếu ⇒ `clarify` chỉ trường thiếu; `truong: {}` ⇒ **0 `clarify`**, tính 1 người 1 ngày + dòng giả định; lượt mang `truong` không bao giờ `clarify`; câu lịch trình vẫn theo B5 D15; `kiem_tien` (1)–(3) mỗi mục một ca vi phạm (ý #5); `tool_use_behavior`: `tinh_tien` có khung ⇒ chạy tiếp, "cần hỏi" ⇒ dừng; **W55 (4c)** mỗi loại lượt (lượt đầu · lượt ghép · "Trả lời luôn" · lượt có lịch sử) chuỗi gửi model đúng plan; cờ tắt ⇒ chuỗi giống byte |

### 3b. Ca thử dò số (test, 0 USD; câu tự viết)

| Câu (tự viết) | Kỳ vọng |
|---|---|
| "hai vợ chồng đi Huế 3 ngày hết bao nhiêu" | người 2 · ngày 3 |
| "đi 2N1Đ, nhóm 4 người" | người 4 · ngày 2 |
| "3n2đ cho 1 người" | người 1 · ngày 3 |
| "đi một mình hai ngày" | người 1 · ngày 2 |
| "2 người lớn và 1 trẻ em mua vé Đại Nội" | vé: người lớn 2 · trẻ em 1 |
| "gia đình năm người, 2 ngày 2 đêm" | người 5 · "2 ngày 2 đêm" ⇒ đêm ≠ ngày − 1 ⇒ ngoài phạm vi (mẫu "X ngày Y đêm", review B m-2) |
| "đi 3 ngày, ngày thứ 2 nghỉ" | ngày **3** ("ngày thứ 2" không có dạng "N ngày" — review B m-2) |
| "đi 3 ngày hay 4 ngày cũng được" | số ngày nhiều giá trị ⇒ không dò |
| "cả nhà đi cuối tuần" | không dò được gì ⇒ hỏi |
| "nhóm 30 người" | > 20 ⇒ ngoài phạm vi |
| "năm nay đi 2 ngày" | "năm" không đứng trước `người` ⇒ người không dò · ngày 2 |

## 4. Tiêu chí ghi trước

**Mốc:** `main` sau B5 (cờ `tinh_tien` tắt = câu chi phí hành vi `main`). **Bộ đo B5c** (C viết trước khi B code, B không mở phần kín; `data/phase_9/bo_do_b5c/`): **đã thấy 14 + kín 6**, mỗi câu có nhãn `pham_vi` ∈ {trong, ngoai} và `loai` ∈ {du_toan, ve, ca_hai}:
- trong phạm vi (đã thấy 8 / kín 4): dự toán đủ số người + ngày (1 / 2 / 3 ngày; 1 / 2 / ≥ 5 người; có / không mức chi; có trẻ em) · vé lẻ Quần thể (người lớn + trẻ em có số; tên bằng bí danh) · câu cả hai (D4) · đi một mình (D5);
- ngoài phạm vi (đã thấy 4 / kín 2): ≥ 4 ngày · giá phòng một khách sạn cụ thể · tiền ăn theo quán · "2 ngày 2 đêm" / vé gộp / vé điểm ngoài Quần thể;
- thiếu trường (đã thấy 2): thiếu số người · thiếu số ngày ⇒ thẻ chỉ trường thiếu.
- **Chuỗi (S3):** ca g2 của B4 (`data/phase_9/b4/q78/`) + **≥ 3 chuỗi mới** (C viết): lượt 1 thiếu ⇒ thẻ; lượt 2 người dùng **gõ chữ có số** người / ngày (không bấm nút); + **≥ 2 chuỗi "thiếu ⇒ thẻ ⇒ Trả lời luôn"**; + 1 chuỗi **theo dõi** gõ chữ không số ("cả nhà") — lượt 2 không gõ lại nút, vẫn thiếu ⇒ **thẻ lần hai là đúng** (người dùng chưa cho giá trị) ⇒ **không** tính vào sàn Q3, chỉ ghi.
- Mẫu 10 câu cho User đọc (spec §4).

| Mã | Phần | Chỉ số / sàn (ghi trước) | Cách đo | Không đạt ⇒ |
|---|---|---|---|---|
| **Q1** = S5 | gỡ được | cờ tắt ⇒ chuỗi gửi model giống byte `main` (176 + 32 + smoke, `capture_all.py`) | harness | sửa tới khi đạt |
| **Q1m** | sàn mở rộng (như B5 Q1m) | cờ bật, mọi câu **không phải chi phí** của 176 + 32 + smoke: yêu cầu lượt đầu **chỉ khác `main` ở đúng một mục `tinh_tien`** trong danh sách công cụ | `capture_all.py` + so mục công cụ | sửa tới khi đạt |
| **Q2a** | sàn gọi công cụ | câu chi phí trong phạm vi (đã thấy 8) gọi `tinh_tien` **≥ 7 / 8** mỗi lượt, kín ≥ 3 / 4; câu không gọi ⇒ vẫn chấm Q2 (D9 chạy mọi câu) | harness ghi tên công cụ | sửa ≤ 2 vòng |
| **Q2** = S1, S2 | **sàn code đếm** (mọi câu bộ) | **S1:** 0 số tiền trong chữ model ngoài {kho được trích} ∪ {code tính} (mọi dạng `…000đ / k / triệu / VNĐ`, chuẩn hoá); **S2:** 0 chữ "tổng" kèm số khi thiếu dữ kiện / ngoài phạm vi; mọi câu ngoài phạm vi có câu cố định "chưa đủ dữ liệu để tính tổng"; câu `ca_hai`: 0 lần cộng vé vào dự toán (D4); vé trẻ không rõ số ⇒ 0 tổng (D2b) | `kiem_tien` + script đọc khung (tất định) | sửa, ≤ 2 vòng trên đã thấy |
| **Q3** = S3 | **sàn** | chuỗi g2 + ≥ 3 chuỗi mới (gõ chữ **có số**): **0 / n lượt 2 bị hỏi lại lần hai** (chuỗi "cả nhà" chỉ theo dõi); ≥ 2 chuỗi "Trả lời luôn": **0 `clarify` lần hai**, có bảng 1 người 1 ngày + dòng giả định | server thật + cookie (như Q7 B4, `q78_api.py`) | sửa ≤ 2 vòng ⇒ âm |
| **Q4** = S4 | **sàn hồi quy** | an toàn 32 **đủ 4 số** (W51: đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời; mốc = lượt đo cuối 01/11 như B4b); **thủ tục S-AT ghi trước** (review B m-5, như B5 Q4): mỗi câu sai điều kiện mới / thiếu cảnh báo mới ⇒ sinh lại **3 lần bản B5c (cờ bật) + 3 lần mốc (cờ tắt)**, 2 judge sub-agent mới mù bên; **đạt ⇔ ở mọi câu đó số lần lỗi bản B5c ≤ mốc**; nhiều hơn ở bất kỳ câu ⇒ âm, không vòng thêm. Golden mẫu 30 F1–F4 (câu ngoài kho bị trả lời **0**); `tinh_tien` gọi ở câu không phải chi phí ≤ 1 / 62; câu bị rút lại do D9 ≤ 1 / 62 | `generate` + `sinh_an_toan.py` ⇒ `q5_golden.py` + `an_toan_b2.py` | âm / tắt cờ |
| **Q5** | **quyết** (spec §11.2) | câu trong phạm vi: **bảng đúng từng dòng** (mỗi số = C tính lại tay từ kho, ghi trước trong bộ đo) **≥ n − 1 / n** — đã thấy n = 8, kín n = 4 (kín ngược chiều ⇒ âm); câu thiếu trường ⇒ thẻ đúng trường thiếu 2 / 2 | so khung ↔ đáp án số C ghi trước | âm |
| **Q6** | theo dõi | số lần D6 dò được / hỏi / tạm; chữ model nhắc lại số (D8); USD / câu, chữ đầu (= chữ model, không tính dòng code); `usage − builder` (< 900 như B4b); `outcome = max_turns` ở câu chi phí | log + harness | — |

**Kết quả âm** (một sàn phạm sau ≤ 2 vòng, hoặc Q5 không đạt) ⇒ cờ `tinh_tien` tắt, câu chi phí giữ hành vi `main` (spec §11.2); tag `hoso/p9-b5c`.
**Cỡ mẫu:** 12 câu trong phạm vi chỉ thấy lỗi lớn; sàn 0 trên ~20 câu + 6 chuỗi không chứng minh tỉ lệ 0 (cận trên ≈ 3 / n). **Chỉnh trên đã thấy, khoá trước kín** (≤ 2 vòng mô tả công cụ / khung / luật code), rồi C chạy kín.

## 5. Bước làm

1. **0 USD — C:** bộ đo B5c (đã thấy + kín + chuỗi + đáp án số tính tay từ kho, ghi trước) + mẫu 10 câu cho User.
2. **0 USD — B:** code D1–D12 + test (§3, §3b); Q1, Q1m; probe parser trên kho thật (tổng kho = tổng code 9 / 9; 11 điểm `quan_the` khớp 11 dòng vé); chạy thử mọi lệnh có phí ở chế độ 0 USD (W36 4b).
3. **Pilot 3 câu đã thấy** (≈ 0,003) ⇒ ước lại tiền + đo `TINH_TIEN_TOOL_OVERHEAD`.
4. **Đã thấy 14 + chuỗi Q3** ⇒ Q2a, Q2, Q3, Q5, Q6 ⇒ ≤ 2 vòng chỉnh ⇒ **khoá** (sha mô tả công cụ + `settings.yaml` + commit).
5. **Kín 6** (C chạy, User `!`) ⇒ Q2a + Q2 + Q5 trên kín.
6. **Q4 hồi quy** (62 câu, cờ bật) + thủ tục S-AT nếu có câu mới.
7. Cổng ổn định (API thật: 1 câu dự toán + 1 câu vé + 1 câu ngoài phạm vi + 1 câu thường; log không chữ; Playwright nút số người + dòng tiến độ) ⇒ report ⇒ review nhánh ⇒ A merge ⇒ 5 chỗ báo cáo.

## 6. Tiền, quyền

| Lượt | Gồm | USD |
|---|---|---:|
| pilot | 3 × ≈ 0,0008 | 0,003 |
| đã thấy + chuỗi | 14 + 6 × 2 lượt ≈ 26 lượt × ≈ 0,0008 | 0,021 |
| chỉnh | ≤ 2 vòng × 26 | 0,042 |
| kín | 6 × 0,0008 | 0,005 |
| hồi quy Q4 | 62 × 0,0004–0,00075 (+ thủ tục S-AT nếu có ≈ 0,005–0,01) | 0,025–0,057 |
| cổng + Playwright | | 0,008 |
| **cộng** | không chỉnh ≈ **0,06–0,09**; đủ 2 vòng ≈ **0,10–0,14** | spec ước 0,07 |

**Điểm quyết A trước lượt có phí đầu** (review B m-4 — dự phóng đủ 2 vòng vượt 0,10): **(a)** trần **0,14 / dừng 0,13** (mọi lượt là sàn ghi trước); **(b)** giữ **0,10 / dừng 0,09** và bớt: chỉnh **tối đa 1 vòng**, chuỗi Q3 chỉ g2 + 3 chuỗi mới + 1 chuỗi "Trả lời luôn" ⇒ ≈ 0,07–0,10 (có thể chạm dừng giữa Q4); **(c)** A ghi số khác. A chọn khi duyệt sha. **A quyết (a) — trần 0,14 / dừng 0,13** (chất lượng trước; chỉnh ≤ 1 vòng dễ âm oan). **A sẽ xin User thêm tiền Phase trước lượt có phí đầu của B5c nếu (2,0 − đã dùng − quỹ B7 0,35) < 0,14** (spec §11.5). Kèm **quỹ B7** (spec §11.5): trước pilot A kiểm (2,0 − đã dùng − 0,35) ≥ trần chọn; thiếu ⇒ A xin User trước. Một lượt vượt ước > 50 % ⇒ dừng, báo A. Mỗi phiên ≤ 1 USD. Judge: chỉ ở thủ tục S-AT (quota Claude). Không ghi Qdrant; không sửa kho / Golden; thư viện mới: không.

## 7. Điều kiện dừng (báo A)

- Parser không đọc đủ 3 bảng dự toán (5 / 6 / 6 hạng mục) hoặc bảng vé lẻ; tổng kho ≠ tổng code ở bất kỳ ô tổng nào; một trong 11 điểm `quan_the` không khớp đúng một dòng vé (bước 2) ⇒ báo A (không tự sửa kho, `Session_Prompt.md` §5).
- Q1 / Q1m không đạt sau 2 lần sửa; Q3 / Q2 phạm sau 2 vòng ⇒ âm; tiền > dừng A chọn.
- B5 chưa merge ⇒ chưa mở nhánh; luật cắt spec §11.4: **23/11 B5 chưa merge ⇒ B5c thu nhỏ còn vé** (bỏ `du_toan`, giữ D2b + D6 người lớn / trẻ em); **30/11 B5c chưa merge ⇒ dừng, ghi dở**.

## 8. Rà khung AI FDE (`agent-design-review` / `agent-security-review`, phần chạm B5c)

| Mục khung | B5c | Nhãn |
|---|---|---|
| §1 cần agent? | không cho phép tính: luồng cố định ⇒ **code** (D2–D5); model chỉ chọn loại câu + diễn đạt | thiết kế |
| §2 phép tính, luật tiền ⇒ code | D3, D2b, D4, D8, D9 (B4 Cách A dùng lời dặn ⇒ phạm — bài học) | [Code] + test |
| §3 tham số phạm vi do code điền | số người / ngày không phải tham số model (D1, D6); giá trị nút `Literal` / `Field(ge=1, le=20)` + `extra="forbid"` | [Code] + test |
| §3 "không thấy ≠ không tồn tại" | ngoài phạm vi ⇒ "chưa đủ dữ liệu để tính tổng"; vé ngoài bảng ⇒ "chưa có giá vé … trong bảng vé lẻ"; lưu trú đi một mình ⇒ "kho không ghi số" (D5) | test |
| §4 trần + đường phục hồi | `tinh_tien` ≤ 1 / câu; hỏi lại ≤ 1 lần / chuỗi (lượt ghép không hỏi — D7); "Trả lời luôn" ⇒ giá trị tạm có ghi; lỗi công cụ ⇒ câu cố định; `max_turns` giữ | [Code] + test |
| §5 một agent | giữ một agent trợ lý + định tuyến; không agent con; **không** công cụ `hoi_lai` cho model (User 10:07) | — |
| Bảo mật: đầu vào không tin cậy | chữ người dùng chỉ cho ra **số đếm** (1–20 người, 1–3 ngày) qua regex; giá lấy **chỉ từ kho** đã nạp ("giá vé là 0 đồng" trong câu không đổi bảng) | test |
| Bảo mật: đường ra | **không** đường ra mới; dữ liệu gửi OpenAI như hôm nay (câu + đoạn kho + khung số) | — |
| Dữ liệu cá nhân | số người / ngày không phải dữ liệu cá nhân; log chỉ nhãn nguồn giá trị (nút / dò / thiếu / tạm), không chữ | grep log ở cổng |

## 9. Rủi ro / chỗ chưa chắc

- **D5 là suy luận** từ số kho (B kiểm lại: khớp ở mức tiêu chuẩn, không khớp mức tiết kiệm) — A chọn (a).
- Bảng dự toán là **hạn mức lập kế hoạch**, không phải giá niêm yết ⇒ khối ghi chú luôn nói rõ; kho đổi ⇒ D2 kiểm.
- D9 chạy **mọi câu** khi cờ bật ⇒ có thể rút nhầm câu thường có số tiền viết khác kho ⇒ Q4 "rút lại ≤ 1 / 62" + Q6 theo dõi; trên đã thấy > 2 / 14 bị rút ⇒ chỉnh trước khoá.
- **Vé chỉ Quần thể vé lẻ** ⇒ câu vé điểm khác / vé gộp không có tổng code (đúng phạm vi, nhưng người dùng có thể thấy khác nhau giữa các điểm) — ghi giới hạn ở báo cáo.
- Nhớ hội thoại tắt (cấu hình khác) ⇒ D6 không dò được câu gốc lượt trước ⇒ hỏi lại thường hơn — ghi giới hạn (hôm nay nhớ bật).
- Nút `so_nguoi` đổi tập giá trị so với B4 D2 cũ (Lệch có lý do D7) ⇒ bộ đo B4 cũ không dùng lại cho chi phí.
- `TruongInput` thêm trường chi phí ⇒ đường `truong` (không gắn cờ — `b157_b4b_review.md` m-1) nhận thêm `so_nguoi` / `muc_chi` cả khi cờ `tinh_tien` tắt ⇒ test route: cờ tắt + `truong` chi phí ⇒ câu ghép, đường trả lời như `main` (không có `tinh_tien`).

## Chỗ đổi B5c-2 (13:55 05/11/2026, A quyết theo User "không cần hỏi lại"; bản trước `bab730a57798` — lịch sử chỗ đổi xem git)

**Lượt B5c (khoá `ecc099c`, nhánh `fb981b8`) GHI ÂM đúng luật** (report `b162_b5c_implementation.md` §3: Golden F2 1 câu + S-AT 1 câu). B5c-2 là **thí nghiệm mới**: đo lại phần Q4 từ đầu, không chỉnh trên kết quả cũ.

| Đổi | Chỗ | Vì sao |
|---|---|---|
| **D8′** câu không có bảng (ngoài bảng / ngoài phạm vi): khung cho model **được nêu giá có trong tài liệu kèm [n]** (không tự nhân / cộng / ước tổng); câu ghi chú tên điểm ngoài bảng = "«…» không thuộc bảng vé lẻ nên hệ thống không tự tính tổng"; không dòng "Mình hiểu" khi không tính gì. D9 giữ (số có trong đoạn kho vẫn được) | `tinh_tien.py` `khung_chu`, `khoi_ghi_chu`, `dong_minh_hieu`; `full_corpus_prompt.py` luật không bảng | Golden F2: luật "không tự viết số tiền" làm model bỏ giá có trong kho |
| **D11′** công cụ `tinh_tien` **chỉ đưa** khi code thấy dấu hiệu chi phí (tiền, giá, chi phí, bao nhiêu tiền, dự toán / dự trù, ngân sách, vé, phí…) trong câu gốc hoặc câu trước (nhớ chỉ câu hỏi), hoặc lượt mang trường chi phí từ nút. Câu khác ⇒ chuỗi gửi model **giống byte `main`** | `tinh_tien.py` `co_dau_hieu_chi_phi`; `assistant.py` `_before_model` / `_lich_extra` | S-AT: thêm công cụ vào mọi lượt đổi cách tìm ở câu an toàn (B4b, B5c). Bỏ sót dấu hiệu ⇒ câu đi đường `main` (liệt kê giá có nguồn) — an toàn |
| **Q1m′** cờ bật: câu **không** có dấu hiệu chi phí của 176 + 32 + smoke ⇒ yêu cầu gửi model **giống byte `main`** (không cần bỏ mục công cụ); câu có dấu hiệu ⇒ chỉ khác đúng một mục `tinh_tien` | `capture_co.py` | đo được bằng code |

**Đo lại (ghi trước):** Q1 + Q1m′ (0 USD) ⇒ đã thấy 14 × 1 (không gãy sàn Q2a / S1 / S2 / Q5 / thẻ) ⇒ Q4 Golden 30 + an toàn 32 (F1–F4, 4 số, S-NHAM ≤ 1 / 62, rút lại D9 ≤ 1 / 62) ⇒ thủ tục S-AT như cũ nếu có câu mới. **Đạt ⇔ mọi sàn trên đạt**; phạm ⇒ âm, không vòng thêm. Tiền: trần còn ≈ 0,06 (0,14 − 0,079); vượt ⇒ dừng báo A. Sau đó C review cả nhánh một lần.

Không đổi: D1–D7, D9, D10, D12, Q2a, Q2, Q3, Q5, bộ đo, luật âm.
