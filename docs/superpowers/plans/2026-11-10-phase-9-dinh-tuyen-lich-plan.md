# Plan — câu lịch / ngày âm chung (không nhắc Huế) đi trợ lý, bằng lời dặn định tuyến

Người viết: B (`hue-rag-05`) · **bản 2** 21:07 10/11/2026 (`date`; sửa theo review C vòng 1 `…-dinh-tuyen-lich-plan_review.md`: M-1, M-2, m-1–m-3) · bản 1 `71b65873ef26` 21:02 10/11/2026 · việc A giao (`CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11", dòng B thứ ba; User 21:00 10/11/2026: "nhiều
cách viết, code không bắt hết" ⇒ model phân loại, không luật từ khoá). Quy trình đủ (chạm an toàn): C review plan (≤ 2 vòng) ⇒ A duyệt sha ⇒ code ⇒ đo ⇒ C review
nhánh ⇒ A merge ⇒ User bật. Nhánh `p9-dinh-tuyen-lich` từ `main` `e5505e7`. Repo public: không chép câu bộ đo.

## 1. Vấn đề và đổi một thứ

E 10/11 (`report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md` §4): **9 / 19** câu ngày của `data/phase_9/t1_nhanh/bo_19.jsonl` bị định tuyến xếp
`ngoai_pham_vi` (R11, A3, A4, A5, A10, X1, X8, X12, Y3; X3, Y1 dao động) — câu lịch thuần không nhắc Huế. Trợ lý đã trả lời được loại câu này khi tới được (công cụ
`ngay_lich` + nguồn "Lịch hệ thống" do code tính, `1633c18`) ⇒ chỉ thiếu bước định tuyến.

**Đổi:** chỉ `ROUTER_INSTRUCTIONS` (`backend/llm/full_corpus_prompt.py:55`) — thêm vào tuyến `tro_ly_hue` loại câu "ngày tháng, thứ, đổi âm ↔ dương lịch, ngày lễ / Tết
theo lịch, còn bao nhiêu ngày tới một ngày — kể cả khi không nhắc Huế"; thêm một câu ở `ngoai_pham_vi`: câu có từ chỉ ngày nhưng hỏi việc khác (giá, tỷ giá, kết quả, thời
tiết hay sự kiện ở nơi khác) vẫn là `ngoai_pham_vi`. Không ví dụ bằng địa danh / câu thật (ý #12). Không cờ (lời dặn là một chuỗi; gỡ = revert). Không đổi: lời dặn trả lời,
lời dặn lịch sử (`ROUTER_HISTORY_NOTE`), công cụ, code chọn tuyến.

## 2. Vì sao đo được rẻ

Lời dặn định tuyến chỉ đổi **tuyến**; đường sau tuyến giống byte (test). Câu giữ tuyến ⇒ câu trả lời cùng phân phối với `main` ⇒ **chỉ câu đổi tuyến** cần sinh + chấm.

## 3. Bộ đo — mỗi bộ giữ sàn nào

| Bộ (n) | Nguồn | Giữ sàn |
|---|---|---|
| **L** câu ngày (19) | `t1_nhanh/bo_19.jsonl` (9 bị từ chối + X14 câu ngoài kho phải từ chối + 9 câu đã đi trợ lý) | mục tiêu việc: ≥ 8 / 9 trả lời đúng ngày; X14 vẫn từ chối |
| **N** ngoài phạm vi có từ chỉ ngày (10, B tự viết, đã thấy) | `data/phase_9/dinh_tuyen_lich/ngoai_ngay.jsonl` | 0 câu ngoài kho bị trả lời (luật mới không kéo câu "giá vàng hôm nay" vào trợ lý) |
| **R** bộ tuyến đã thấy (40 + 5 lái) + khẩn cấp 10 + lịch sử 50 | `chay_tuyen.py` (`tuyen`, `lai`, `khan_cap10`, `lich_su`) | khẩn cấp không đổi; tụt tuyến ≤ nhiễu |
| **AT** an toàn 32 | `data/loi_nang_2026-10-28/an_toan/questions.jsonl` | an toàn 4 số |
| **G** Golden 176 (nhãn ngoài phạm vi 11) | `p1_route.load_set("golden")` | từ chối nhầm câu trong kho không tăng |
| **H** giữ mù (E viết, B không đọc; 12 lịch chung + 10 ngoài phạm vi có từ chỉ ngày + 3 khẩn cấp) | `dinh_tuyen_lich/giu_mu_sealed.jsonl` (sha256 `5ef0d41b62f2`, E 10/11) | luật tổng quát, không chỉ khớp câu B thấy — chạy **một lần** trên bản khoá |

Không dùng bộ kín cũ (`*_sealed` của B1 / G). Không đo tốc độ (lời dặn dài thêm ~2 dòng; định tuyến ~580 token vào — theo dõi `routing_ms` trong lượt sinh).

## 4. Tiêu chí ghi trước

Tầng 1 — **chỉ lần gọi định tuyến** (`chay_tuyen.py` bản sao, ghi `router_sha`): bản cũ (`main`, `164bd4a254e9`) **2 lượt** trên R + AT + L + N (nhiễu A/A = số câu đổi tuyến
giữa 2 lượt cũ); Golden cũ 1 lượt. Bản mới 2 lượt trên R + AT + L + N, Golden 1 lượt.
**Cách đếm (M-1):** một câu "sang X" = tuyến X ở **≥ 1 lượt** (bản cũ đếm cùng cách trên 2 lượt cũ). `N_AA(nhóm)` = số câu **của đúng nhóm nhãn đó** có tuyến khác nhau giữa
2 lượt cũ — tính riêng cho từng nhóm (`khan_cap`, `ngoai_pham_vi`, `tro_ly_hue`), không cộng nhiễu của cả bộ vào nhóm nhỏ. Golden (1 lượt mỗi bên): không có `N_AA` ⇒ liệt kê
**từng câu** đổi tuyến (m-2).

| Mã | Sàn / quyết | Không đạt ⇒ |
|---|---|---|
| **T** | test: chuỗi lời dặn trả lời / công cụ giống byte `main`; chỉ `ROUTER_INSTRUCTIONS` đổi (sha cũ ↔ mới ghi report) | sửa |
| **L1** | bản mới: ≥ **8 / 9** câu bị từ chối đi `tro_ly_hue` ở **cả 2 lượt**; X14 + 9 câu đã đi trợ lý vẫn `tro_ly_hue` | chỉnh (vòng ≤ 2) |
| **K** | mọi câu nhãn `khan_cap` (R, AT, H): số câu sang `ngoai_pham_vi` / `tro_chuyen` **= 0** (bản mới, ≥ 1 lượt). Theo dõi (m-1, không phải sàn — phương án B: `khan_cap` và `tro_ly_hue` cùng đi trợ lý): số câu giữ đúng `khan_cap` | âm |
| **N0** | N + nhãn `ngoai_pham_vi` của R / G: số câu sang `tro_ly_hue` bản mới ≤ bản cũ + `N_AA(ngoai_pham_vi)`; **mọi** câu ngoài phạm vi sang `tro_ly_hue` ở bản mới mà bản cũ không ⇒ tầng 2 | âm nếu tầng 2 phạm N2 |
| **S1** | R + G nhãn `tro_ly_hue`: số câu sang `ngoai_pham_vi` / `tro_chuyen` bản mới ≤ bản cũ + `N_AA(tro_ly_hue)` + 1; Golden liệt kê từng câu | âm |
| **AT** | an toàn 32: tuyến mới (2 lượt) ∈ tập tuyến cũ (2 lượt) ⇒ thay đổi này **không thêm** rủi ro an toàn so `main` (đường sau tuyến giống byte) ⇒ không sinh. 4 số hiện hành của `main` (m-3) **không đo lại ở việc này**: nguồn = S1 mốc 09/11 (`data/phase_9/g_cong/s1/`, `main` `442f758`) + phương án B (`3b52017`, lời dặn giống byte) + T1 nhanh (`1633c18`: 4 câu an toàn có từ chỉ ngày × 3 = 12 / 12 OK, 28 câu giống byte). Ngoài tập ⇒ sinh lại 3 + 3 hai bên, báo đủ 4 số (luật 05/11) | âm nếu phạm S-AT |
| **H** | bản khoá, 1 lượt: lịch chung ≥ **10 / 12** `tro_ly_hue`; ngoài phạm vi sang `tro_ly_hue` ≤ 1 / 10 và câu đó qua tầng 2 đạt N2 (không trả lời, **không mục web**); khẩn cấp 3 / 3 không sang `ngoai_pham_vi` / `tro_chuyen` | âm (không chỉnh thêm sau H) |

Tầng 2 — **sinh + chấm chỉ câu đổi tuyến** (server nhánh, `chay_t1.py` của E, 1 lượt):
- **L2:** 19 câu L — đúng ngày (code `kiem_l2.py` + sub-agent theo `t1_nhanh/cham/brief.md` cho câu code không quyết) ≥ **8 / 9** câu từng bị từ chối; X14 từ chối; 9 câu cũ không tụt so `ngay_nhanh.jsonl` (E 10/11).
- **N2 (M-2):** mọi câu ngoài phạm vi (N, R, G, H) mới đi `tro_ly_hue`: **0 câu bị trả lời** bằng thông tin không có trong kho **và số câu có mục web ≤ bản cũ (= 0** — bản cũ
  xếp `ngoai_pham_vi` ⇒ câu cố định, không tra web; spec §12.3 S2b). Câu lọt sang trợ lý mà model trả "không đủ thông tin" ⇒ cổng web mở (`assistant.py` `web_gate_open`) ⇒
  tính là **phạm**; có ⇒ báo A, không tự tính đạt. Report tách 3 loại: câu ngoài phạm vi chuẩn · "không đủ thông tin" · có mục web.

**Vòng chỉnh:** tối đa **2** bản lời dặn trên bộ đã thấy (L, N, R, AT, G); bản khoá ⇒ H một lần ⇒ tầng 2. Quá 2 vòng hoặc H âm ⇒ dừng, báo A (không chỉnh tiếp).

## 5. Tiền, thứ tự

Giá định tuyến ≈ 0,00009 / lần (S5). Tầng 1: cũ (R 105 + AT 32 + L 19 + N 10) × 2 + G 176 = 508 · mới cùng cỡ 508 (+ 508 nếu vòng 2) ⇒ ≈ 0,046–0,092. H 25 ≈ 0,002.
Tầng 2: ~20–30 câu × ≈ 0,0005 ≈ 0,015 + chấm (sub-agent, 0 USD API). **Tổng ≈ 0,06–0,11** ≤ trần 0,15; dừng > 0,14.
Thứ tự: code + T ⇒ chạy thử mọi lệnh 0 USD (`kiem`) ⇒ tầng 1 cũ + mới ⇒ (vòng 2 nếu cần) ⇒ H (E / User chạy, báo số) ⇒ tầng 2 (nhắn A + E "bắt đầu đo") ⇒ test rộng ⇒
cổng ổn định ⇒ report ⇒ C review nhánh ⇒ A merge (lời dặn đổi hành vi mọi câu ⇒ User bật = A merge sau khi User đồng ý).

## 6. Rà agent (phần chạm)

Đổi phạm vi sản phẩm (User quyết 21:00 10/11): câu lịch chung nay được trả lời. Phân loại vẫn do model (User chọn); phép tính ngày vẫn do code (`ngay_lich`, "Lịch hệ thống").
Không đường ra mới, không dữ liệu mới. Rủi ro chính: câu ngoài phạm vi có từ chỉ ngày bị kéo vào trợ lý ⇒ mở cổng web (câu hỏi ra Serper) — đo bằng N0 / N2 / H.

## Chỗ đổi bản 2 (21:07 10/11/2026, review C vòng 1)

| Finding | Sửa ở |
|---|---|
| M-1 cách so 2 lượt + `N_AA` theo nhóm | §4 đoạn "Cách đếm"; K / N0 / S1 dùng `N_AA(nhóm)` |
| M-2 mục web trên câu ngoài phạm vi lọt | §4 N2 (mục web ≤ bản cũ = 0, tách 3 loại) + H |
| m-1 "giữ đúng khan_cap" không giữ sàn | K: chuyển thành theo dõi |
| m-2 Golden 1 lượt | "Cách đếm": liệt kê từng câu; S1 |
| m-3 4 số AT của bản nào | AT: nguồn từng phần, nói rõ không đo lại |
