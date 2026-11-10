# Plan — sửa lịch nhiều lượt (`sua_lich`, Phase 9, ý #8 + #9)

Người viết: C · **bản 3** 13:29 05/11/2026 (`date`, review E vòng 1 `874fd7a98a5e` + A quyết tiền) · bản 2 13:23 05/11/2026 (`date`, A quyết tiền: pass^2) · bản 1 13:20 05/11/2026 (`date`, việc **C193**, A giao). Nền: `main` sau B5 (`d66f6a3`, cờ `lich_trinh` tắt tới Q3) và #6 (`5a8aa5e`, đã merge, bật). Nhánh `p9-sua-lich`.
File tracked, repo public: không chép kho / Golden / câu bộ đo; câu ví dụ tự viết, tên điểm là tên công khai. Bộ đo: C viết; người code (B, nếu A giao) **không mở** phần kín.

## Căn cứ để review (`WORKFLOW.md` §9.1 — ghi file + hàm, không số dòng)

| File | Mục / hàm | Để kiểm gì |
|---|---|---|
| file này | toàn bộ | ý #8, #9 đủ; tiêu chí ghi trước; tiền |
| spec Phase 9 bản 12 `77250689e605` | §11.1 dòng "sửa lịch nhiều lượt", §11.3 (rà FDE), §11.4 (luật cắt 07/12), §11.5 (tiền) | bám spec |
| `session_prompt/CURRENT_HANDOFF.md` | bảng "Ý TƯỞNG TỪ NGHIÊN CỨU 04/11" dòng #8, #9 | đúng ý User chọn 04/11 |
| plan B5 bản 7 `b572443dc9cd` | D2–D8, D12, D14, D15 | dùng lại luật xếp + kiểm cuối, không viết lại |
| `backend/llm/lich_trinh.py` | `ThamSo`, `xep`, `kiem_khung`, `khoi_ghi_chu`, `kiem_cuoi` | chỗ thêm "giữ / loại" khi xếp lại |
| `backend/llm/assistant.py` | `lich_trinh_for_turn`, `_finish_generated`, `ROUTE_INPUTS` (#6) | chỗ nối công cụ thứ ba |
| `backend/api/conversations.py` | `Conversation`, `ConversationStore.append` | chỗ lưu khung của cuộc |
| `backend/api/routes/chat.py` | `_remember`, `_model_query`, `lich_cho_giao_dien` | lưu khung sau lượt đạt; nút chọn |

## 1. Mục tiêu và phạm vi

- **Vấn đề (đã thấy):** sau một lịch, câu như "bỏ lăng Khải Định", "ngày 2 chỉ đi chiều", "đổi chợ Đông Ba sang buổi sáng" không làm được. Hôm nay server không giữ khung (lịch sử chỉ nhớ câu hỏi — `nho_cau_tra_loi: false`), nên model chỉ có thể gọi `lich_trinh` xếp lại **từ đầu**: điểm người dùng đã bỏ có thể quay lại, điểm đã thêm có thể mất. Nghiên cứu 04/11 (`bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md`) ghi: TRIPO nhớ lượt trước còn hue_rag thì không; Flex-TravelPlanner cho thấy làm tốt một lượt không có nghĩa là sửa nhiều lượt tốt; Travel-AI có 2 lỗi gộp (không bỏ được sở thích; giá trị mặc định ghi đè giá trị người dùng đã nói).
- **Trong phạm vi:** server giữ khung cuối của cuộc; công cụ `sua_lich` với hành động có tên; code áp hành động theo **cùng luật B5**; khối "Đã đổi / Giữ nguyên / Chưa làm" do code nối; thay điểm mà người dùng không nói thay bằng gì ⇒ code đưa 2–3 điểm cùng cụm để bấm.
- **Ngoài phạm vi:** giờ đến từng điểm, quãng đường, thời tiết (B5b), tiền (B5c), bản đồ toạ độ (Phase 11). Không lưu chữ tự do của người dùng.

## 2. Quyết định thiết kế

| Mã | Quyết định | Vì sao |
|---|---|---|
| **D1** | **Lưu khung của cuộc:** `Conversation` thêm `lich` = {`tham_so`, `da_noi` (tên các trường lấy từ tham số model / nút ở lượt lịch — **không** gồm giá trị mặc định công khai D4b), `khung` (id điểm theo ngày → buổi), `them` (id người dùng đã thêm), `loai` (id người dùng đã bỏ), `cau_goc`}. **Chỉ route ghi**, sau lượt có lịch **qua kiểm cuối**, từ **trace chính** (đường #6: sau khi merge trace phụ ⇒ chỉ khi tuyến cuối là `tro_ly_hue`); lượt rút lại / lỗi / huỷ / dừng ở thẻ chọn **không ghi**. Đọc / ghi bằng **bản sao sâu** (`copy.deepcopy`) — các hàm B5 (`bo_diem`, `cat_ngay_cuoi`) sửa khung tại chỗ, nên khung đã lưu không bao giờ được trao thẳng cho lõi (review E M-1). RAM, cùng TTL 30 phút của cuộc; không ghi đĩa, không log. Cờ mới `sua_lich` (cần `lich_trinh` + `nho_hoi_thoai`) | khung là trạng thái do code dựng — giữ ở server, không bắt model nhớ (khung FDE §5: trí nhớ do code, không chữ tự do) |
| **D2** | **Công cụ `sua_lich` chỉ được đưa khi cuộc có khung đã lưu**: route đặt `trace.lich_cu = copy.deepcopy(<khung đã lưu>)` ⇒ thêm `lich_cu` vào `ROUTE_INPUTS` của #6 (hiện 3 trường). `sua_lich` **chỉ ghi `trace.lich_moi`** (bản riêng, dựng từ bản sao), không đụng `lich_cu`. Không có khung ⇒ danh sách công cụ như B5 | lượt đơn (Golden, an toàn) **không đổi chuỗi gửi** ⇒ Q1m giống byte ⇒ hồi quy rẻ |
| **D3** | **Tham số = danh sách hành động có tên** (enum, `extra="forbid"`), tối đa 3: `bo_diem{ten}` · `them_diem{ten, ngay?, buoi?}` · `thay_diem{ten_cu, ten_moi?}` · `doi_buoi{ten, ngay, buoi}` · `doi_so_ngay{so_ngay}` · `doi_tham_so{di_cung?, kieu_di?, so_thich?}`, với `so_thich` nhận thêm giá trị `bo` (= bỏ sở thích). `ten` khớp bằng `khop_diem` (nguyên tên / `ten_khac`); không khớp ⇒ kết quả công cụ báo "không có trong bảng", không tự đoán | chữ người dùng chỉ thành id qua bảng; hành động có tên dễ kiểm hơn "xếp lại tự do" |
| **D4** | **Code áp tối đa 2 hành động / lượt**, theo thứ tự model gửi. Hành động thứ 3 ⇒ không làm, khối code ghi "Chưa làm: <loại hành động> — bạn nhắn tiếp nhé" (nhãn cố định theo enum). Hành động phạm luật B5 (buổi không hợp lệ với người đi cùng, hết suất, `nam_xa` khi < 3 ngày mà người dùng không nêu…) ⇒ không làm + dòng "Không đổi được: … vì …" (mã luật `CAU_KHONG_XEP` của B5) | ý #8 "≤ 2 hành động / lượt, nêu ý không làm"; lời từ chối của backend là kết quả công cụ (khung FDE §3) |
| **D5** | **Xếp lại có giữ:** `xep` thêm 2 tham số `giu` (vị trí điểm không bị hành động chạm) và `loai` (id đã bỏ). Hành động chỉ đổi chỗ nó chạm. `doi_so_ngay` / `doi_tham_so` ⇒ xếp lại với `ThamSo` **gộp**: code chỉ nhận trường có giá trị **khác** giá trị đã lưu (model điền lại đủ trường cũng không ghi đè gì); trường khác giữ giá trị cũ; đổi một trường thuộc `da_noi` ⇒ D7 có dòng "Đã đổi <trường>: <cũ> → <mới>"; điểm trong `them` vẫn ưu tiên, điểm trong `loai` không bao giờ quay lại (trừ khi `them_diem` chính nó) | tránh 2 lỗi gộp của Travel-AI; bất biến "điểm không bị chạm giữ nguyên chỗ" do code |
| **D6** | **Thay điểm không nói thay bằng gì** (`thay_diem` không có `ten_moi`): code chọn 2–3 điểm **cùng cụm**, hợp sở thích, chưa có trong khung, không thuộc `loai`, xếp được ở buổi đó ⇒ trả **thẻ chọn** (như thẻ hỏi lại D15: `tool_use_behavior` dừng lượt; nút = id code đưa). Thẻ luôn có thêm nút **"Bỏ điểm này, không thay"** (⇒ code áp `bo_diem`). Bấm ⇒ lượt ghép mang `sua_chon {cu, moi | bo}`; server kiểm `moi` ∈ danh sách đã đưa (danh sách lưu kèm khung, như D1) ⇒ code áp. **Lượt mang `sua_chon` không bao giờ đưa thẻ chọn lần hai** (như luật lượt mang `truong` của B5 D15) | ý #8; nút chỉ chứa giá trị code đưa (như B4 D8) |
| **D7** | **Khối "Đã đổi / Giữ nguyên / Chưa làm"** do code nối sau chữ model (cùng chỗ khối D4b của B5): mỗi hành động một dòng; "Giữ nguyên: các buổi khác" khi có. Dòng "Mình hiểu" (D12) cập nhật theo tham số mới | người dùng thấy rõ cái gì đổi; model không tự tóm tắt sai |
| **D8** | **Model viết lại cả lịch** theo khung mới, cùng `LICH_TRINH_LUAT` + kiểm cuối D8 của B5 (sau B5.1 + C191). Không thêm lời dặn hệ thống (bài học B4b); mô tả `sua_lich` ngắn: chỉ gọi khi tin nhắn cuối nhờ **đổi lịch vừa xếp**; câu hỏi về một điểm ⇒ `tim_kho`; nhờ lịch mới hoàn toàn ⇒ `lich_trinh` | dùng lại rào đã đo |
| **D9** | **Nút "Sửa" của B5** (đổi 4 trường): khi cuộc có khung đã lưu ⇒ đi đường `doi_tham_so` / `doi_so_ngay` của D5 (giữ `them` / `loai`) thay vì xếp lại từ đầu | một đường sửa, không hai |
| **D10** | **Trần:** `sua_lich` ≤ 1 lần / lượt; `lich_trinh` và `sua_lich` không cùng lượt (gọi cái thứ hai ⇒ kết quả công cụ "đã xếp ở lượt này"); `max_turns` giữ 4. Sau khung mới, `tim_kho` trả "đã đủ tài liệu" như vòng chỉnh 1 của B5 | trần + đường phục hồi (khung FDE §4) |
| **D11** | **Tiến độ (D14 B5):** thêm bước thật `da_doi{n}`, `khong_doi{diem, ly_do}`, `chua_lam{n}`; chỉ phát khi code đã làm. Log: mã hành động + số đếm, không chữ | demo thấy agent làm gì, không bước giả |

## 3. Thay đổi theo file (dự kiến)

`lich_trinh.py` (hành động, `xep(giu, loai)`, `ap_hanh_dong`, `chon_thay`, khối D7) · `assistant.py` (`sua_lich_for_turn`, `ROUTE_INPUTS` + `lich_cu`, nối `_finish_generated`) · `generator_openai_full_corpus.py` (công cụ thứ ba + dừng ở thẻ chọn) · `full_corpus_prompt.py` (`SUA_LICH_MO_TA`) · `conversations.py` (`lich` của cuộc) · `chat.py` (lưu khung sau lượt đạt, `sua_chon`, log) · `settings.yaml` (`sua_lich: false`) · `App.jsx` (thẻ chọn điểm thay, bước tiến độ) · test mới `test_sua_lich.py` (mỗi hành động + mỗi luật **một ca cố tình vi phạm**; bất biến D5; ca "3 hành động"; ca Travel-AI ×2; **khung đã lưu không đổi** khi: (i) đường #6 tuyến cuối khác `tro_ly_hue`, (ii) kiểm cuối hỏng ⇒ rút lại, (iii) dừng ở thẻ chọn (đổi chỉ ở lượt `sua_chon`), (iv) hai lượt liền: lượt 2 sửa đúng trên khung lượt 1 người dùng đã thấy; lượt `sua_chon` ⇒ 0 thẻ lần hai; `doi_tham_so` điền lại đủ trường cũ ⇒ 0 dòng "Đã đổi").

## 4. Tiêu chí ghi trước

| Mã | Loại | Tiêu chí | Đo bằng |
|---|---|---|---|
| **Q1** | sàn | cờ `sua_lich` tắt ⇒ chuỗi gửi model giống byte `main` (228 / 228) | `capture_all.py` |
| **Q1m** | sàn | `lich_trinh` bật + `sua_lich` bật, lượt không có khung đã lưu ⇒ giống byte `lich_trinh` bật + `sua_lich` tắt (228 / 228; bên so là đường B5 đã qua hồi quy Q4 của B5) ⇒ **thay hồi quy Golden 30 + an toàn 32** (chuỗi gửi không đổi ⇒ câu trả lời cùng phân bố) | `capture_q1m.py` của B5 (bật thêm `sua_lich`) |
| **Q2** | sàn code, **mọi lượt sửa, mọi lần chạy** | (a) `kiem_khung` 0 lỗi; (b) điểm không bị hành động chạm **giữ nguyên ngày / buổi**; (c) giá trị trường trong `da_noi` chỉ đổi khi nhãn ghi người dùng đổi, và mỗi lần đổi có dòng "Đã đổi <trường>: cũ → mới" (so `da_noi` trước / sau với nhãn); (d) điểm trong `loai` không quay lại; (e) hành động thứ 3 có dòng "Chưa làm"; (f) `kiem_cuoi` 0 theo nội dung (luật A quyết 05/11); (g) 0 lần hỏi lại lần hai — kể cả thẻ chọn lần hai sau `sua_chon`; khung đã lưu chỉ đổi sau lượt đạt (harness đọc khung của cuộc sau mỗi lượt); (h) `max_turns` 0; (i) nút thẻ chọn chỉ chứa id code đưa | harness đọc khung trước / sau (tất định) |
| **Q3** | **quyết** | hành động code áp **đúng nhãn** (`ky_vong`: danh sách hành động + khung kết quả mong đợi, so tất định) — **pass^2** (chuỗi đạt **cả 2** lần chạy): đã thấy **≥ 8 / 10**; kín **≥ 4 / 5** | harness |
| **Q4** | sàn | chuỗi "hỏi tiếp sau lịch" (TD của B5) + chuỗi có câu khẩn cấp / ngoài phạm vi sau lịch: `sua_lich` gọi nhầm **0**, tuyến đúng 100 % | harness + log |
| **Q5** | theo dõi | rút lại do kiểm cuối; lượt có thẻ chọn; USD / lượt; chênh token lược đồ công cụ (D16 B5) | log + harness |
| **Q8** | cổng | server thật + cookie, ≥ 2 lượt: lịch ⇒ "bỏ X" ⇒ "thay Y" (bấm nút) ⇒ "thêm 1 ngày"; Playwright: khối D7, thẻ chọn, bước tiến độ, CSP 0 | như B5 Q8 |

**Kết quả âm:** Q2 phạm sau vòng chỉnh, hoặc Q3 dưới ngưỡng ⇒ cờ `sua_lich` tắt; B5 giữ nguyên; tag `hoso/p9-sua-lich`. Kín ngược chiều ⇒ không chỉnh trên kín.

## 5. Bộ đo (ý #9) — C viết

- **Bộ kín: CÓ** (quyết ngay ở plan theo luật 05/11 (2)): bậc này chỉnh mô tả công cụ / luật trình bày qua nhiều vòng trên bộ đã thấy.
- **Đã thấy 10 chuỗi + kín 5 chuỗi**, mỗi chuỗi = 1 câu lịch + 2–3 câu sửa, viết kiểu người thật:
  - dời buổi ("chợ Đông Ba để sáng đi");
  - gộp hai ý trong một câu ("bỏ lăng Khải Định, thêm chùa Thiên Mụ");
  - ba ý trong một câu (ý thứ 3 phải có "Chưa làm");
  - bỏ sở thích ("thôi không cần ăn uống nữa");
  - đổi người đi cùng sau khi đã thêm điểm (giá trị cũ phải giữ);
  - thay điểm không nói bằng gì (thẻ chọn);
  - điểm ngoài bảng;
  - sửa mơ hồ ("bớt lăng đi") ⇒ ghi trước hành động chấp nhận;
  - 1 câu hỏi tiếp không phải sửa (phải `tim_kho`).
- **Chạy 2 lần / chuỗi** (pass^2 — A quyết; hợp luật "sàn hành vi model ≥ 2 lượt"); nhãn `ky_vong` ghi trước, có `chap_nhan` khi câu cho phép ≥ 2 cách hiểu.
- Kèm 5 chuỗi TD của B5 + 2 chuỗi an toàn sau lịch (Q4).
- **Cỡ mẫu:** "≥ 8 / 10 pass^2" chỉ thấy khác biệt lớn. Sàn 0 lỗi trên ~30 lượt sửa × 2 không chứng minh tỉ lệ 0 (cận trên ≈ 3 / 60).

## 6. Bước làm

1. C viết bộ đo (đã thấy + kín) ⇒ A xem cỡ / phủ (0 USD).
2. B code theo D1–D11 + test ⇒ Q1, Q1m (0 USD).
3. Pilot = 2 chuỗi đầu của bộ đã thấy, lần chạy 1 (tính vào lượt đã thấy, không chạy lại) ⇒ ước lại tiền.
4. Đã thấy ×2 ⇒ chỉnh **≤ 1 vòng** (A quyết tiền; mô tả công cụ / luật trình bày; chỉ chạy lại chuỗi hỏng ×2 + 2 chuỗi đạt ×1 làm đối chứng) ⇒ **khoá** (sha mô tả + luật + bảng + `settings.yaml` + commit).
5. C chạy kín ×2 trên khoá (User `!`) ⇒ Q4 ⇒ Q8 ⇒ review cả nhánh (≤ 2 vòng) ⇒ A merge (cờ theo kết quả).
- Không chạy lượt có phí cùng lúc lượt đo tốc độ / việc nặng (W31).

## 7. Tiền (ước — vượt phần còn của Phase; User cho vượt, A ghi nhận lúc duyệt)

Một lượt lịch / sửa ≈ 0,0008–0,0012 USD (B5 đã thấy 0,00073 / câu; chuỗi v2 0,0021 / chuỗi).

| Phần | Ước |
|---|---|
| đã thấy 10 × ~3,5 lượt × 2 lần (gồm pilot) | ≈ 0,07 |
| 1 vòng chỉnh (chuỗi hỏng × 2 + 2 đối chứng × 1) | ≈ 0,03 |
| kín 5 × 3,5 × 2 | ≈ 0,035 |
| Q4 (7 chuỗi ~2 lượt × 2 lần; chuỗi TD v2 của B5 0,0021 / chuỗi) | ≈ 0,03 |
| Q8 (1 chuỗi, server thật) | ≈ 0,01 |
| **Cộng** | **≈ 0,175** |

**Trần 0,20, dừng 0,19** (A quyết bản 3 — review E M-2: trần bản 2 0,16 không đủ cho vòng chỉnh nào). Hồi quy Golden / an toàn = 0 USD nhờ Q1m (D2). Spec §11.5 ước 0,10 ⇒ lệch vì mỗi chuỗi chạy 2 lần. Vượt phần còn lại của trần Phase 9: User cho vượt khi vắng (A ghi vào handoff). Q4 không dùng lại được chuỗi TD của B5: sau một lịch, cuộc đã có khung ⇒ `sua_lich` được đưa ⇒ chuỗi gửi đổi ⇒ phải chạy lại. Bản 2 ước Q4 0,02 là thấp (tính lại theo 0,0021 / chuỗi ⇒ 0,03).

## 8. Điều kiện dừng (báo A)

Q1 / Q1m khác byte · chạm 0,19 USD · Q2 phạm sau vòng chỉnh · `xep(giu, loai)` làm đổi kết quả của lượt lịch đầu (test so khung B5 cũ ↔ mới trên 13 câu đã thấy: phải giống) · #6 (đã merge, bật trên `main` `5a8aa5e`) — `ROUTE_INPUTS` thiếu `lich_cu` · B5 Q3 của User âm (bậc này dựa trên B5 ⇒ dừng, hỏi A).

## 9. Rà agent design / security (skill `agent-design-review` / `agent-security-review`, phần chạm bậc này)

| Mục khung | Hiện trạng (file + hàm) | Bậc này | Khớp / lệch | Đề xuất |
|---|---|---|---|---|
| §1 có cần agent | `assistant.py` `lich_trinh_for_turn`: model trích trường, code xếp | phần hiểu câu sửa (dời buổi, gộp ý, mơ hồ) cần phán đoán ⇒ model chọn hành động; áp luật là luồng cố định ⇒ code | khớp | — |
| §2 bất biến ⇒ code | `lich_trinh.py` `xep`, `kiem_khung` (luật B5) | giữ chỗ điểm không bị chạm, `da_noi` không bị ghi đè, `loai` không quay lại, trần 2 hành động — code (D4, D5) | khớp | — |
| §2 câu cố định hứa hành động | `lich_trinh.py` `khoi_ghi_chu` (D4b) | "Chưa làm — bạn nhắn tiếp" không hứa code tự làm sau; thẻ chọn ⇒ code áp khi bấm | khớp | — |
| §3 tham số phạm vi do code | `api/conversations.py` `Conversation` (hôm nay chỉ `turns`); cuộc chọn bằng cookie | khung nào = cuộc của cookie, không phải tham số model; `ten` qua `khop_diem` | khớp | thêm `lich` (D1) |
| §3 từ chối là kết quả công cụ | `assistant.py` `lich_trinh_for_turn` trả chữ khi hết lượt | hành động phạm luật / không khớp tên ⇒ chữ kết quả công cụ + dòng D7 | khớp | — |
| §4 trần + phục hồi | `ASSISTANT_MAX_TURNS` 4; `lich_calls` ≤ 1 | `sua_lich` ≤ 1 / lượt, không cùng `lich_trinh`; kiểm cuối hỏng ⇒ rút lại | khớp | — |
| §5 trí nhớ | `conversations.py` nhớ câu hỏi (`nho_cau_tra_loi: false`); `assistant.py` `ROUTE_INPUTS` 3 trường (#6); `lich_trinh.py` `bo_diem` / `cat_ngay_cuoi` **sửa khung tại chỗ** | một loại (khung do code dựng), namespace = cuộc, không chữ tự do; **bản sao sâu khi đọc / ghi, chỉ route ghi sau lượt đạt** | khớp sau D1 / D2 bản 3 | `ROUTE_INPUTS` + `lich_cu`; test (i)–(iv) |
| §5 lời dặn | `full_corpus_prompt.py` không có lời dặn công cụ (B5 D7) | không thêm lời dặn hệ thống; mô tả công cụ ngắn | khớp | — |
| security: đường ra mới | — | không có (bản đồ vẫn chỉ link do code dựng của B5) | khớp | — |
| security: chữ người dùng là dữ liệu | `hoi_lai.py` `TruongInput` (`extra="forbid"`) | chữ người dùng chỉ thành id qua bảng; nút chỉ chứa id code đưa, server kiểm lại (`sua_chon`) | khớp | — |

## 10. Rủi ro / chỗ chưa chắc

- Câu sửa mơ hồ ("bớt lăng đi", "đổi cho nhẹ nhàng hơn") ⇒ model chọn hành động khác nhãn. Đã ghi `chap_nhan` trước; nếu hỏng nhiều thì xem lại D3 (thêm hành động `giam_mat_do`?) — ghi ở vòng chỉnh, không tự thêm.
- Lưu khung trong RAM mất khi khởi động lại server ⇒ câu sửa sau đó đi đường `lich_trinh` (xếp mới). Ghi giới hạn, không lưu đĩa (Phase 12 xét lại).
- Hai yêu cầu cùng cuộc chạy song song ⇒ lượt xong sau ghi đè khung (như `conversations.py` đã ghi) — một người dùng, chấp nhận.

## Chỗ đổi bản 2 (13:23 05/11/2026)

A quyết tiền: **pass^2** thay pass^3 (Q3, §5, §6 bước 4–5, §7, §8); trần 0,16 / dừng 0,15. Nền: #6 đã merge, bật trên `main` `5a8aa5e`. Không đổi: D1–D11, Q1, Q1m, Q2, Q4, Q5, Q8, cỡ bộ đo, bộ kín có.

## Chỗ đổi bản 3 (13:29 05/11/2026)

Theo review E vòng 1 (`…sua-lich-plan_review.md` `874fd7a98a5e`) + A quyết tiền:
- **M-1:** D1 / D2 — đọc / ghi khung bằng bản sao sâu; `sua_lich` chỉ ghi `trace.lich_moi`; chỉ route lưu, sau kiểm cuối, từ trace chính (đường #6: chỉ khi tuyến `tro_ly_hue`); thêm test (i)–(iv) ở §3; Q2 (g) đọc khung của cuộc sau mỗi lượt.
- **M-2:** A quyết trần 0,20 / dừng 0,19; chỉnh ≤ 1 vòng; pilot nằm trong lượt đã thấy; bảng §7 tính lại ≈ 0,175 (Q4 tính lại 0,03).
- **m-1:** §5 pass^2. **m-2:** `da_noi` trong D1; D5 chỉ nhận trường khác giá trị lưu + dòng "Đã đổi <trường>: cũ → mới"; Q2 (c) so `da_noi`. **m-3:** D6 nút "Bỏ điểm này, không thay" + lượt `sua_chon` không đưa thẻ lần hai; Q2 (g). **m-4:** §9 thêm cột hiện trạng / đề xuất.
- Không đổi: D3, D4, D7–D11, Q1, Q1m, Q3, Q4, Q5, Q8, cỡ bộ đo, bộ kín có.
