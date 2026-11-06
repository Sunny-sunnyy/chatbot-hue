# Review: Spec giao diện cổng du lịch đợt 1 — bản 1 (vòng 1 / tối đa 2)

Decision: **changes_requested** — 0 blocker · 1 major · 5 minor
Người kiểm: E (Claude Code `hue-rag-28`) — không phải người viết (A)
Date: 22:36 06/11/2026 (`date`)
Đối tượng: `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` sha256 **`03904f669e8f`** (khớp sha A đưa). 0 USD.

## 1. Phạm vi đã review

- Đọc hết spec.
- Gói căn cứ §0:
  - `CURRENT_HANDOFF.md` hai mục quyết định User tối 06/11;
  - nháp kỹ thuật C211 `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` §2;
  - code `backend/api/routes/chat.py` (`ChatRequest`, `SourceResponse`), `backend/llm/assistant.py` (`lich_trinh_for_turn`), `backend/llm/lich_trinh.py` (`DiCung` / `KieuDi` / `SoThich` / `SoNgay`, `chot_so_ngay`), `backend/api/app.py` (`FRONTEND_CSP`), `backend/llm/thoi_tiet.py` (`lay_du_bao`, `CACHE_S`);
  - build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`corpus.sources`).
- `tong_hop.md` của B172: chỉ đối chiếu mã mẫu được trích, không review lại nghiên cứu.
- Không đọc STATUS hay tin nhắn của A / B / C.
- Bối cảnh E đã có từ việc trước (không phải căn cứ mới): report E19 (`e19_kin_v2.md`) và E20 (`e20_tu_choi_hoi_kem.md`) — E là người viết hai report này.

## 2. Đã kiểm, khớp

| Kiểm | Kết quả |
|---|---|
| Quyết định ↔ lựa chọn User (handoff) | D1 = "bỏ số trong chữ, dòng Nguồn, tầng máy giữ `[n]`" ✓ · D2 = mức 2, hai đợt, không chép nhận diện ✓ · D3 = "biểu mẫu trước, câu tự do chưa bật" ✓ · D13 ✓. Không quyết định nào trái lựa chọn User |
| D3 khớp code thật | `lich_trinh_for_turn`: `di_cung=di_cung or tu_nut.get("di_cung")` (cũng `kieu_di`, `so_thich`) ⇒ tham số model thắng nút ở 3 trường; `chot_so_ngay(truong, …)` ⇒ nút thắng số ngày — **đúng như spec và C211 viết**. `ChatRequest` hiện chỉ có `query`, `truong` (`extra="forbid"`) ⇒ cần trường mới cho `bieu_mau`, đúng D3 |
| D6 `corpus.sources` | build record có `corpus.sources` là dict **204** khoá (đường dẫn tương đối theo lĩnh vực) ⇒ Q-K "204 / 204" đo được; so nguyên chuỗi khoá là cách chặn đọc file tuỳ ý đơn giản, đủ |
| D6 thời tiết | `thoi_tiet.lay_du_bao` có sẵn, `CACHE_S = 30 * 60` ✓ |
| D7 | `SourceResponse` hiện `id, title, heading_path, excerpts` ⇒ thêm `bai_id` là đổi khuôn JSON công khai, spec đã ghi cái giá ✓ |
| Phạm vi §4 | không lọt kho / chỉ mục / lời dặn / câu tự do / E20 Sửa 1–2 / đợt 2 ✓ |
| Over-engineering | 4 route chỉ đọc, 1 cờ, hash router 0 gói, 0 Radix — tương xứng; `/api/tinh_nang` cần để giao diện ẩn mục khi cờ tắt. Không thấy cơ chế phòng xa thừa |
| Bộ kín "không" | hợp luật cắt giảm 05/11 (2): đường biểu mẫu do code quyết, bộ đã thấy chạy 2 lượt |

## 3. Findings

### M-1 (major) — Q-F (tiêu chí quyết bật cờ) chưa đo được như viết

- **Vị trí:** §6 Q-F.
- **Yêu cầu:** `run-experiment` — tiêu chí ghi trước phải định nghĩa chính xác và đo được; không tự hợp thức hoá (brief A).
- **Bằng chứng:**
  1. "đủ **6** kiểu 'đi cùng ai'": `lich_trinh.py` `DiCung = Literal["mot_minh", "cap_doi", "gia_dinh_tre_em", "nguoi_lon_tuoi", "nhom_ban"]` = **5** giá trị. Nếu kiểu thứ 6 là "không chọn" thì phải ghi rõ, vì `null` đi đường khác.
  2. "2 sub-agent chấm **(iii) 'không thêm điều sai'**":
     - (iii) ở Q3 B5 là "mỗi điểm có nguồn"; ở đây là tiêu chí khác, cùng nhãn, và chưa định nghĩa "điều sai" so với cái gì;
     - kín v2 (E19 §4 "Giới hạn (iii)") cả hai agent ghi: file kết quả harness **không lưu chữ đoạn nguồn** ⇒ không kiểm được nội dung;
     - như viết, người chấm không có dữ liệu để chấm tiêu chí này.
  3. "khung lịch nhận **đúng 4 giá trị chọn 24 / 24**": với D3 (b), code gọi `lich_trinh` bằng giá trị nút ⇒ tính chất **tất định**. Đếm nó trong lượt có phí là đếm điều code đã bảo đảm — nên là **test 0 USD**. Lượt có phí chỉ nên quyết phần model (lời viết theo khung).
  4. Q-U3 mặc định ẩn "đi dày" ⇒ `kieu_di` trên biểu mẫu chỉ còn một giá trị. "4 giá trị chọn" và bộ 12 tổ hợp phải ghi rõ khi nhánh này xảy ra.
- **Tác động:** quyết bật `lich_trinh_bieu_mau` dựa vào Q-F. Hai chỗ (1), (2) làm tiêu chí không chạy được hoặc chấm theo cảm tính.
- **Tiêu chí đóng:**
  - (a) bộ tổ hợp ghi theo enum thật (5 kiểu đi cùng + "không chọn" nếu có; 1 / 2 / 3 / 4+ ngày; có / không sở thích; `kieu_di` theo Q-U3);
  - (b) "4 giá trị khung = nút" chuyển thành test 0 USD (mọi tổ hợp, không gọi model);
  - (c) tiêu chí chấm của agent định nghĩa bằng câu đo được, vd "mỗi ý nêu về một điểm có trong đoạn nguồn `[n]` của điểm đó". Harness phải **lưu chữ đoạn nguồn từng `[n]`** (file private) để người chấm đọc được — hoặc bỏ tiêu chí agent, chỉ giữ phần code đếm;
  - (d) đổi tên nhãn để không trùng (iii) của Q3.

### m-1 (minor) — D3 thiếu 3 chi tiết của đường biểu mẫu

- **Vị trí:** §2 D3.
- **Bằng chứng:** C211 §2 có ghi "không gửi chữ tự do từ form ngoài `query` cố định"; spec không chép ý này. Đọc code:
  - `_model_query` dựng câu cố định cho `sua_chon` — đường biểu mẫu cần cách tương tự;
  - cờ `sua_lich` (nhánh `p9-sua-lich`) đòi `lich_trinh` bật (`AssistantFlags.__post_init__`).
- **Tác động:**
  - Không rõ `query` lưu vào lịch sử 3 lượt là gì.
  - Không rõ model trong đường này còn được đưa `tim_kho` / tra web không. E20: `tim_kho` bị chặn sau lịch là đường dẫn tới câu từ chối.
  - Sau lịch từ biểu mẫu, câu "bỏ X" gõ trong chat **không** sửa được lịch (câu tự do tắt) — người dùng sẽ thấy lạ.
- **Đóng:** D3 ghi ba điều:
  1. `query` = câu cố định do code dựng từ giá trị nút; không ô chữ tự do; câu đó vào lịch sử;
  2. danh sách công cụ model nhận ở đường này;
  3. giới hạn "sửa lịch bằng chat chưa có ở đợt 1" (D12 Giới thiệu nói ra), hoặc nút "Sửa" của biểu mẫu là đường sửa duy nhất.

### m-2 (minor) — Q-G đếm "≥ 6 tính năng" chưa rõ cách đếm; cách đo tương phản chưa có

- **Vị trí:** §6 Q-G.
- **Bằng chứng:** danh sách có "5 lĩnh vực Khám phá". Nếu đếm là 5 thì "trợ lý + 5 lĩnh vực" đã đủ 6 khi mọi cờ tắt ⇒ ngưỡng không phân biệt được gì. "Tương phản ≥ 4,5 : 1" không nêu công cụ đo; `.venv` có Playwright nhưng không có axe.
- **Đóng:**
  - ghi danh sách cố định (Khám phá đếm 1) và ngưỡng "**mọi** mục có cờ bật tới được trong ≤ 2 bấm";
  - nêu cách đo tương phản (script tính từ màu thật lấy bằng `getComputedStyle` của Playwright), hoặc chuyển thành kiểm tay có ghi giá trị.

### m-3 (minor) — D1 chưa nói về nguồn web `[w n]` và dòng nguồn của lịch trình

- **Vị trí:** §2 D1, §6 Q-N.
- **Bằng chứng:** tra web B6 đang **bật** trên `main` (mục "Từ web (chưa kiểm)", mã `[w n]`, bộ lọc giao diện riêng — `Project_Status.md` §4). Lịch trình có khối ghi chú do code nối. Q-N chỉ đo câu kho.
- **Đóng:** D1 ghi cách hiện `[w n]` (giữ mục web riêng có link do code, hoặc cùng dòng "Nguồn"); Q-N thêm ≥ 2 câu có mục web (hoặc ghi rõ ngoài phạm vi đo).

### m-4 (minor) — bảng rà §7 thiếu một đường ra; `/api/thoi_tiet` khi cờ tắt chưa ghi

- **Vị trí:** §7, D6.
- **Bằng chứng:** `/api/kham_pha/bai` trả **toàn văn** bài kho cho trình duyệt. Hôm nay câu trả lời chỉ đưa đoạn trích. `knowledge-base-hue/` là dữ liệu private (không commit — `Session_Prompt.md` §5). Đang chạy trên máy User nên chưa ra ngoài; khi deploy (Phase 12) thì đây là công bố toàn bộ kho.
  `/api/thoi_tiet`: D9 nói ô hiện "khi cờ bật", nhưng D6 không nói route làm gì khi cờ tắt.
- **Đóng:**
  - §7 thêm dòng "toàn văn bài kho ra trình duyệt", kèm ghi chú "trước deploy User quyết công bố kho" (theo luật phòng xa: ghi mục trước deploy, không chặn đợt 1);
  - D6 ghi cờ `thoi_tiet` tắt ⇒ `/api/thoi_tiet` 404, không gọi Open-Meteo (như route ảnh khi `anh.bat` tắt).

### m-5 (minor) — Q-U2 (b) "ảnh Wikimedia" đụng CSP

- **Vị trí:** §3 Q-U2, D5 ("0 đổi CSP").
- **Bằng chứng:** `FRONTEND_CSP` có `img-src 'self' blob:` ⇒ ảnh lấy thẳng từ trang ngoài bị chặn.
- **Đóng:** Q-U2 (b) ghi "ảnh tải về, phục vụ từ `dist/` (CSP giữ), kèm dòng ghi công" — hoặc nói rõ là đổi CSP. Như vậy User biết cái giá khi chọn.

## 4. Kết quả quan sát / cách chạy lại

Chỉ đọc, 0 USD:
- `sha256sum` spec;
- đọc enum trong `lich_trinh.py`;
- đọc `ChatRequest` / `SourceResponse` / `FRONTEND_CSP` / `CACHE_S`;
- đếm `corpus.sources` của build record (204).

Không chạy giao diện (chưa có code).

## 5. Giới hạn

- Không review lại nghiên cứu B172 (mẫu, ảnh chụp).
- Không kiểm ước "1–1,5 tuần" và bundle hiện tại (chưa build).

## 6. Decision và bước tiếp

**changes_requested.** A sửa M-1 (định nghĩa lại Q-F) + 5 minor (thêm câu / dòng) ⇒ người review kiểm vòng 2 (chỉ phần sửa).
Vòng 2 còn minor ⇒ A duyệt (luật 05/11). Không có blocker. Quyết định D1–D14 khớp lựa chọn User; D3 khớp code thật.
