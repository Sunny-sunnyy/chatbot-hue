# Review spec Phase 9 bản 10 — mục §11 "Sửa đổi 05/11/2026" (C177)

Người kiểm: C · 09:34 05/11/2026 (`date`) · spec `docs/superpowers/specs/2026-11-02-phase-9-design.md` sha tính từ file **`b7dbb778db9e`** (A viết). Phạm vi (A giao): chỉ §11, đối chiếu §5–§8 bản 9. Căn cứ ngoài: `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` (User duyệt bậc 1 + lịch), `data/phase_9/tinh_tien/kiem_ke_gia.md` (C176, private). Kiểm thêm bằng lệnh chỉ đọc: `backend/api/app.py` CSP, `frontend/src/App.jsx`, bảng điểm `diem_v3.json`, kho qua `scripts/grep_kb.sh`. 0 USD.

**Kết luận: changes_requested — 0 blocker / 6 major / 7 minor.** Hướng (bậc 1, B4b, "model đề xuất ⇒ code kiểm / tính") khớp đề xuất User duyệt và bài học B4. Chỗ phải sửa trước khi User duyệt sha: đường ra / provider mới chưa liệt kê đủ (giọng nói của trình duyệt, nguồn toạ độ + tile), tiêu chí V1 / V2 chưa đo được thành "đạt / không", B5c thiếu sàn cho đúng lỗi đã thấy ở B4, lịch tự mâu thuẫn với luật "lần lượt", bảng tiền chưa phải dự phóng đầy đủ.

## Major

| # | Vị trí | Finding | Bằng chứng | Tiêu chí đóng |
|---|---|---|---|---|
| **M-1** | §11.1 V1 "thử trước … nhận dạng của trình duyệt ↔ PhoWhisper chạy máy"; §11.4 | **Đường ra / provider mới thiếu:** (a) nhận dạng giọng nói của trình duyệt (Web Speech API trên Chrome) gửi âm thanh tới máy chủ của hãng trình duyệt — chính file đề xuất §3 V1 ghi điều này — nhưng §11.4 chỉ liệt kê "âm thanh tới OpenAI"; lượt **thử** cũng gửi giọng thật của User ra ngoài; (b) PhoWhisper là **model mới** (tải trọng số, có thể thêm thư viện; máy 15 GB RAM — luật User "một việc nặng một lúc") nhưng §11.1 chỉ ghi "User duyệt ở đây" cho `gpt-transcribe`. `Session_Prompt.md` §4: provider / model mới cần User duyệt | file đề xuất §3 V1 "Phương án khác"; §11.1 dòng V1; §11.4 | §11.4 thêm đường ra (a) (kể cả lượt thử); §11.1 ghi rõ User duyệt **cả ba** phương án được thử (provider trình duyệt, PhoWhisper — giấy phép + RAM ước + "không chạy cùng việc nặng khác"), hoặc bỏ phương án nào chưa duyệt |
| **M-2** | §11.1 B5 (ii) "bản đồ tuyến từ toạ độ trong bảng điểm"; §11.4 tile | **Nguồn toạ độ + giấy phép chưa có:** bảng điểm không có cột toạ độ; chỉ **10 / 28** điểm có chữ "toạ độ" trong chính file kho (C đếm) ⇒ 18 điểm phải lấy **từ ngoài** — đúng loại "enrich bằng web" mà `Session_Prompt.md` §5 đòi phạm vi duyệt + ghi nguồn / ngày. Tile OpenStreetMap có chính sách dùng (ghi công, không dùng nặng) — §11.1 dời "điều khoản tile" vào plan, nhưng CSP hôm nay `img-src 'self'; connect-src 'self'` (`backend/api/app.py:38`) ⇒ mở miền tile là đổi rào an toàn ở mức spec | `diem_v3.json` (không trường toạ độ); `grep_kb.sh` "toạ độ" ∩ 28 file nguồn = 10; `app.py:38` | §11 ghi: nguồn toạ độ (kho trước; điểm thiếu ⇒ nguồn mở có giấy phép, ghi URL + ngày, User duyệt từng toạ độ), giấy phép dữ liệu bản đồ + ghi công, miền tile duy nhất được thêm vào CSP; hoặc phương án không tile (sơ đồ tĩnh / chỉ link D11) nếu điều khoản không hợp |
| **M-3** | §11.2 V1 | **Tiêu chí V1 không thành "đạt / không":** "chọn phương án đạt cao nhất trong trần tiền" không có ngưỡng tối thiểu ⇒ phương án tốt nhất vẫn có thể nghe sai tên / số nhiều; luật cắt §11.3 "30/11 V1 chưa đạt" dựa trên "đạt" chưa định nghĩa | §11.2, §11.3 | ghi ngưỡng trước: vd tên điểm đúng ≥ x / 15 **và** số đúng ≥ y / (số câu có số) trên bản chuyển chữ chưa sửa; dưới ngưỡng ⇒ V1 không bật |
| **M-4** | §11.2 V2 "≥ 30 ảnh gồm ≥ 5 ảnh không phải Huế … tên đúng nằm trong ứng viên ≥ 24 / 30" | **Mẫu số lẫn:** ảnh ngoài Huế không có "tên đúng" trong kho (phải ra "không rõ") ⇒ "≥ 24 / 30" trộn hai loại; với 5 ảnh ngoài Huế thì thực là ≥ 24 / 25 (96 %) — chặt khác hẳn ý "24 / 30" (80 %). "Danh sách điểm / món có trong kho" chưa định nghĩa (28 điểm bảng B5? cả tên file `foods/`?) ⇒ không biết ứng viên lấy từ đâu, không tính được | §11.2 V2; file đề xuất §3 V2 "≥ ?/30" | tách: ảnh Huế n_H ⇒ tên đúng trong ứng viên ≥ k / n_H; ảnh ngoài Huế ⇒ "không rõ" ≥ 4 / 5 (đã có); ghi danh sách tên cụ thể (nguồn + số tên) làm enum |
| **M-5** | §11.1 B5c + §11.2 B5c | **B5c mở lại `hoi_lai` loại `chi_phi` mà không có sàn cho lỗi đã thấy ở B4:** Q7 g2 (người dùng gõ số người + số ngày ⇒ bị hỏi lại 4 / 4, `b144_b4_implementation.md` §2f) là lỗi của đường hỏi lại chi phí, không phải của Cách A; §11.2 B5c chỉ có sàn số tiền / tổng / an toàn ⇒ g2 có thể quay lại không bị đo. Thêm: kiểm kê giá — bảng cộng được **chỉ** ở file chi phí, cho **1 / 2 / 3 ngày**, mỗi ô là **khoảng, tính cho một người**; **không có 4+ ngày**; giá món ăn **không ghi ngày** ở mục giá ⇒ §11.1 "giá có nguồn + đơn vị + ngày nguồn từ kho" không đúng cho phần lớn giá ăn uống | `kiem_ke_gia.md` §1, §3; §2f g2 | §11.2 B5c thêm sàn "chuỗi chi phí gõ chữ số người / ngày: 0 lần bị hỏi lại lần hai" (+ `so_ngay` 4+ ⇒ câu cố định "kho chỉ có dự toán 1–3 ngày", 0 tổng); §11.1 ghi phạm vi dữ liệu B5c = dự toán file chi phí + vé (có ngày); giá món chỉ liệt kê, ghi "kho không ghi ngày giá"; code tính riêng cận thấp / cao (luật của chính file) |
| **M-6** | §11.3 lịch ↔ luật "Hai bậc cùng sửa đường trả lời / giao diện ⇒ lần lượt" (giữ từ §6) | **Lịch tự mâu thuẫn:** tuần 10–16/11 "đo + merge B5; **code B5c**" — B5c sửa đúng các file B5 đang khoá đo (`assistant.py` vòng công cụ, `hoi_lai.py`, `chat.py`, `App.jsx`) và §11.1 ghi B5c "sau B5"; tuần 17–23/11 "sửa lịch nhiều lượt" (sửa `lich_trinh` + giao diện) song song V1 (`App.jsx` ô nhập) — "nếu file không chồng" nhưng cả hai chạm `App.jsx`. Chuỗi bậc đường trả lời B4b ⇒ B5 ⇒ B5c ⇒ sửa lịch ⇒ B5b ⇒ B6 = **6 bậc lần lượt** trong 05/11–07/12 (~4,5 tuần), mỗi bậc gần đây mất 1–2 ngày phiên + review ⇒ khả thi chỉ khi không vòng sửa nào kéo dài | §11.3; §6 dòng cuối; B4 đã 3 khoá + B4b | ghi rõ: B5c **code trên nhánh riêng chỉ khi B5 đã khoá** (không merge / không đo trước B5 merge) hoặc dời sang 17–23/11; V1 tách phần giao diện ra file / component riêng hoặc xếp sau bậc sửa lịch; thêm một dòng "đường găng" (bậc nào trễ 1 tuần thì cắt gì) |

## Minor

| # | Vị trí | Finding | Tiêu chí đóng |
|---|---|---|---|
| m-1 | §11.1 B4b "Tiêu chí: plan B4 bản 7 (`db3a9931b16f`)" | Bản 7 đã bị thay (bản 8 `69afbb2732cf`, C vòng 7 ready); spec trỏ sha không còn là bản duyệt. §5 B4 bản 9 (chi phí "chỉ liệt kê giá có nguồn", quyết "≥ 8 / 10, ≥ 4 / 5" gộp hai loại) chưa ghi "thay bởi B4b" | trỏ "plan B4 bản A duyệt (sha ghi ở handoff)" hoặc sha bản 8; §11.1 ghi §5 B4 bị thay ở phần chi phí + tiêu chí quyết |
| m-2 | §11.1 B5 (i) "bước hiện trên giao diện" | Giao diện **đã có** dòng tiến độ theo sự kiện thật ("Đang tìm trong kho…", "đang hiểu câu hỏi" — `frontend/src/App.jsx:10, :43`) + §5 B2 "thẻ công cụ" ⇒ ghi B5 (i) là **mở rộng** đường sự kiện có sẵn, không phải khối mới | một câu "dùng lại sự kiện SSE hiện có" |
| m-3 | §11.2 B5 "bước hiện = bước trong log" | `chat_metrics` chỉ ghi số / tên công cụ, không ghi bước hiển thị ⇒ "= log" cần trường log mới hoặc so với sự kiện SSE đã gửi | ghi cách so (sự kiện SSE ↔ `tools` / trường mới) |
| m-4 | §11.1 B5 (ii) "bản đồ tuyến" | Plan B5 bản 4 (C173 `e176b7478b2d`) §1 "Không làm: bản đồ tương tác / chỉ đường" — spec bản 10 đổi ⇒ plan B5 cần bản 5. Chữ "tuyến" dễ hiểu là đường đi thật; plan B5 cấm nêu thời gian / quãng di chuyển | ghi "đường nối theo thứ tự lịch, không phải đường đi" + nhắc plan B5 sửa |
| m-5 | §11.3 luật cắt | Luật cắt chỉ thêm V1, V2; **không có** cho B5c, sửa lịch nhiều lượt, B5b; luật cũ §6 (1)–(3) đã qua ngày, (4) "07/12 B5 chưa đóng" lệch lịch mới (B5 merge 10–16/11) | bảng luật cắt mới thay §6 cho mọi bậc còn lại |
| m-6 | §11.5 tiền | Bảng §8 vẫn ghi B4 0,04 · B5 0,04 (thật: B4 ≈ 0,205 + B4b trần 0,10; B5 trần 0,15); §11.5 **không ước** bậc sửa lịch nhiều lượt (bộ chuỗi × 3 lần pass^3 + hồi quy — ước thô C: ≈ 0,07–0,12) và B5b. Cộng thô C: 1,27 + B4b 0,10 + B5 0,15 + B5c 0,065 + sửa lịch ~0,1 + B5b ~0,03 + V1 0,01 + V2 0,045 + B6 ~0,05 + B7 0,35 ≈ **2,15–2,25** ⇒ gần như chắc vượt 2,0, không phải "có thể" [ước thô, chưa trừ phần 1,27 có thể đã gồm một phần B4] | bảng dự phóng đủ bậc (đã dùng / trần từng bậc / còn lại) để User quyết trần một lần trước B5 |
| m-7 | §11.4 V2 | Thêm rào xử lý ảnh: giới hạn số điểm ảnh khi giải mã (ảnh "bom giải nén"); Pillow đã có trong `.venv` (12.3.0) — ghi để không thêm thư viện | một dòng rào |

## Đã kiểm, khớp

- Bậc 1 = đúng các mục User duyệt (A4 ⇒ B5c, A2 + H1 trong B5, V1, V2); "Không làm" khớp §2 file đề xuất; bậc 2 chỉ dùng tuần dự phòng.
- V1 "chữ hiện trong ô nhập để sửa, không tự gửi" + sàn "0 lần tự gửi"; V2 "0 câu trả lời thẳng từ ảnh" + ứng viên chỉ từ danh sách của code — đúng mẫu "model đề xuất, người / code xác nhận"; ảnh / âm thanh không lưu, không log, kiểm nội dung thay vì tin `Content-Type`.
- NFR câu nói > 0,0005 USD được nêu, để User quyết ở plan V1 (khớp file đề xuất §5 câu 2).
- §7 bộ ba: thêm ảnh / âm thanh là thêm (b) nội dung không tin cậy + (c) đường ra — §11.4 có ý "dữ liệu không phải lệnh"; thiếu chỉ ở M-1, M-2.

## Vòng 2 — bản 11 `4d2c2a165af0` (C178 · 09:44 05/11/2026 `date`)

Sha tính từ file = **`4d2c2a165af0`** (A báo thay `7725d78be374`; khác chỉ §11.4 — C đọc cả hai). Phạm vi: §11 viết lại, đối chiếu §5–§8 + vòng 1 ở trên. Kiểm thêm (chỉ đọc): `backend/llm/assistant.py` :287–293 (`max_turns` ⇒ câu từ chối cố định — khớp dòng §11.3 "§4 trần"), `CURRENT_HANDOFF.md` dòng ghi chuyển finding, `data/phase_9/tinh_tien/kiem_ke_gia.md`. 0 USD.

**Kết luận: changes_requested — 0 blocker / 2 major / 5 minor.** Mọi finding vòng 1 đã đóng hoặc chuyển hợp lệ (bảng dưới). Chỗ mới phải sửa nằm ở hai quyết định User vừa thêm (deploy trước khi đóng code; không còn hạn 20/12) và ở thứ tự tiêu tiền khi B7 là bậc bắt buộc đứng cuối.

### Finding vòng 1

| # | Trạng thái bản 11 | Kết luận |
|---|---|---|
| M-1 giọng nói (đường ra / model) · M-2 toạ độ + tile + CSP · M-3 ngưỡng V1 · M-4 mẫu số V2 · m-7 ảnh | ra khỏi Phase 9 (User tách Phase 10 / 11), ghi trong `CURRENT_HANDOFF.md` dòng spec bản 11 "chuyển sang spec Phase 10 / 11" | **chuyển hợp lệ** — với điều kiện spec Phase 10 / 11 liệt kê các finding này trong mục "Căn cứ để review" (m-5 dưới) |
| M-5 B5c sàn g2 + phạm vi dữ liệu | §11.1 phạm vi = bảng dự toán (1 / 2N1Đ / 3N2Đ × 3 mức, một người, ngày đối chiếu, luật nhóm) + vé; ngoài phạm vi ⇒ câu cố định "chưa đủ dữ liệu"; §11.2 sàn (3) g2 + ≥ 3 chuỗi mới, 0 / n hỏi lần hai | **đóng** (khớp `kiem_ke_gia.md`) |
| M-6 lịch lần lượt | §11.4 một bậc đường trả lời / tuần, Phase 10 chỉ route mới + ô nhập, xung đột ⇒ Phase 9 ưu tiên | **đóng** |
| m-1 sha plan B4 | bản 8 `69afbb2732cf` + §5 B4 phần chi phí / "≥ 8 / 10, ≥ 4 / 5" thay bằng plan | đóng |
| m-2 bước giao diện có sẵn · m-3 so SSE thay trường log | §11.1 B5 (i) | đóng |
| m-4 plan B5 cấm bản đồ | bản đồ sang Phase 11; plan B5 bản 4 giữ "không bản đồ" | đóng (nhất quán) |
| m-5 luật cắt | §11.4 luật cắt mới cho B5, B5c, sửa lịch, B5b, B6 | đóng |
| m-6 tiền | §11.5 bảng còn lại theo bậc ⇒ 2,1–2,2 (C cộng lại: 1,27 + 0,10 + 0,15 + 0,07 + 0,10 + 0,05 + 0,05 + 0,35 = **2,14**) | đóng — xem M-2 mới |

### Major mới

| # | Vị trí | Finding | Bằng chứng | Tiêu chí đóng |
|---|---|---|---|---|
| **M-1** | §11.4 "đóng code = đã triển khai lên AWS" ↔ §7 "Giả định an toàn" + "Trước khi deploy" ↔ §5 B6 | **Deploy thành điều kiện đóng code nhưng mọi rào / đo của Phase 9 vẫn dựa giả định "chạy trên máy User, một người dùng, không deploy"** (§7): B6 dùng Serper khi điều khoản chưa rõ cho người dùng cuối (User chấp nhận rủi ro **ở máy mình**), khoá Serper không có giới hạn lượt / người, §7 tự ghi "trước khi deploy: xem lại soát chữ web + điều khoản dịch vụ web; rà R1 (kiểm `Host` + giới hạn lượt); lưu phiên"; nhớ trong RAM một tiến trình; sàn tốc độ đo trên CPU máy User. Bản 11 không nói kết quả B6 / B7 đo ở đâu, cờ nào được bật trên AWS | §7 dòng 336, 341; §11.4 dòng 461–464 | §11.4 thêm: B6 / B7 đo trên máy User (thước Phase 1–8); việc §7 "Trước khi deploy" là **đầu vào bắt buộc** của spec Phase 12; cờ web (B6) mặc định **tắt** trên AWS tới khi Phase 12 rà lại điều khoản + hạn mức + giới hạn lượt; ghi rõ B7 không phụ thuộc deploy |
| **M-2** | §11.5 + §11.4 "B3 và B7 không cắt" | **B7 bắt buộc đứng cuối nhưng tiền đã dự phóng vượt trần** (2,14 > 2,0): theo luật hiện tại A chỉ xin thêm "trước lượt có phí vượt" ⇒ thời điểm vượt rơi vào giữa B6 / B7; nếu lúc đó User không duyệt thêm thì bậc không được cắt (B7 ≈ 0,35) không chạy được, còn các bậc có thể cắt đã tiêu trước | §11.5; §5 B7 | một trong hai: (a) xin User nâng trần **ngay khi duyệt bản 11** (số đã dùng + dự phóng 2,14 đã có); hoặc (b) **giữ quỹ B7 0,35** — luật cắt thêm "tiền còn lại (trần − đã dùng) < 0,35 + bậc kế ⇒ cắt bậc kế (B5b / sửa lịch / B6) trước khi chạm B7" |

### Minor mới

| # | Vị trí | Finding | Tiêu chí đóng |
|---|---|---|---|
| m-1 | §1 dòng 34 "đóng code 20/12/2026"; §6 dòng 312 | §11 nói "bản 9 §1–§10 giữ nguyên trừ chỗ ghi dưới"; §11.4 thay §6 nhưng **§1** vẫn ghi mốc 20/12 ⇒ hai mốc trong cùng spec | §11 ghi "thay cả §1 câu đóng code" (hoặc sửa §1 kèm dấu "bản 11") |
| m-2 | §11.4 bảng: "15–21/12 B7" và "16–30/12 sửa lỗi; deploy AWS" | Hai dòng chồng 16–21/12: B7 có lượt đo (gồm chữ đầu nếu đo) mà deploy / sửa lỗi chạy cùng lúc ⇒ W31 (đang đo thì không việc nặng / lượt có phí khác); sửa lỗi trong lúc B7 đo làm lệch commit đo | B7 khoá commit + không merge trong lúc B7 đo; deploy bắt đầu sau B7 (hoặc chỉ việc giấy tờ / tài khoản AWS song song) |
| m-3 | §11.1 B5c "chặn hỏi lần hai: lượt có lịch sử mà lượt trước là `hoi_lai` ⇒ không đưa `hoi_lai`" | Luật viết chung, không ghi chỉ cho `chi_phi` — nếu code áp cho mọi loại thì **đổi cả hành vi lịch trình của B4b** đã merge (Q7 g1 / g3 của B4b đo khi luật này chưa có) ⇒ cần hồi quy Q7 lịch trình hoặc ghi phạm vi | ghi "chỉ loại `chi_phi`" hoặc thêm Q7 lịch trình vào sàn B5c |
| m-4 | §11.1 B5c "bảng dự toán … + vé" | Bảng dự toán của kho **đã có hàng "tham quan"** (`kiem_ke_gia.md` §1) ⇒ cộng thêm vé từng điểm sẽ tính hai lần nếu không có luật; "code dò số người trong câu" chưa nói cách đọc chữ không phải số ("hai vợ chồng", "gia đình 4 người") | plan B5c ghi luật vé (chỉ khi hỏi vé / thay hàng tham quan, không cộng chồng) + danh sách mẫu chữ số người code nhận; còn lại ⇒ hỏi |
| m-5 | "Chuyển khỏi Phase 9" | Finding chuyển chỉ được ghi ở `CURRENT_HANDOFF.md` (sẽ dời sang archive khi đóng việc) | spec Phase 10 / 11 khi viết: mục "Căn cứ để review" trỏ `…design_review_v10.md` vòng 1 M-1–M-4, m-4, m-7 (một dòng trong §11 bản 11 nói điều này là đủ) |

**Theo dõi (không phải finding):** thí nghiệm tốc độ #6 (đạt, chờ User bật — thứ tự merge "B4b ⇒ #6 rebase") không còn trong bảng lịch bản 11 (bản 10 có "10–16/11 #6 trình User") ⇒ A giữ ở handoff là đủ.

**Decision vòng 2: changes_requested** (0B / 2M / 5m) — sửa M-1, M-2 (+ minor) ⇒ báo sha ⇒ C kiểm phần sửa.

## Vòng 3 — bản 12 `77250689e605` (C178 · 09:46 05/11/2026 `date`)

Sha tính từ file = **`77250689e605`**. Bản 11 không được commit ⇒ C đối chiếu từng chỗ A báo với chữ bản 11 C đã đọc ở vòng 2 (§1 dòng 34, §11.1 B5c, §11.4, §11.5) + tìm sót: `grep "20/12"` (còn §6 dòng 312 — §11.4 ghi "thay §6" ⇒ chấp nhận) và `grep` "lần hai" / "tham quan" / "Finding chuyển".

| Finding vòng 2 | Sửa ở bản 12 | Kết luận |
|---|---|---|
| M-1 deploy ↔ giả định §7 | §11.4 đoạn "Phase 9 ↔ deploy": rào / đo Phase 9 giữ giả định máy User; B6, B7 đo trên máy User; §7 "Trước khi deploy" = đầu vào bắt buộc spec Phase 12; **cờ web tắt trên AWS** tới khi Phase 12 rà lại; tốc độ / tiền đo lại trên AWS ở Phase 12 | đóng |
| M-2 quỹ B7 | §11.5 (b): giữ riêng 0,35; trước mỗi bậc, (trần − đã dùng − quỹ B7) < ước bậc ⇒ xin User trước, không duyệt ⇒ thu nhỏ / cắt; quỹ không dùng cho bậc khác. C tính với số hiện tại: 2,0 − 1,27 − 0,35 = 0,38 ⇒ đủ B4b + B5 + B5c (0,32), **chạm ở bậc sửa lịch** ⇒ A sẽ phải xin trước bậc đó (dự đoán được, không phải lỗi) | đóng |
| m-1 §1 "20/12" | §1 dòng 34 gạch mốc cũ + trỏ §11.4 | đóng |
| m-2 B7 chồng deploy | B7 15–21/12 (máy User, khoá commit, W31); deploy 22–30/12 **sau** B7 | đóng |
| m-3 chặn hỏi lần hai | §11.1 B5c "chỉ cho loại `chi_phi` … đường lịch trình của B4b giữ nguyên" | đóng |
| m-4 vé ↔ tham quan, dò số người | "Chi tiết để plan B5c": một khoản một lần; mẫu dò (chữ số, chữ "hai, ba…", "3N2Đ") + ca thử ghi ở plan | đóng (chi tiết đúng chỗ là plan) |
| m-5 finding chuyển | §11.4 đoạn "Finding chuyển sang Phase 10 / 11": M-1, M-3, M-4, m-7 ⇒ Phase 10; M-2, m-4 ⇒ Phase 11; "spec Phase 10 / 11 phải trỏ lại các mã này" | đóng |
| theo dõi #6 | §11.4 dòng #6: merge sau B4b (rebase + Q1) khi User quyết bật | đóng |

Không thấy đổi ngoài các chỗ trên. Ghi nhỏ không chặn: câu mở §11 vẫn ghi "Review bản 11: chỉ mục này" (nay là bản 12) — chữ, không đổi ý.

**Decision vòng 3: ready_for_user_confirmation** — User duyệt sha `77250689e605` (A tính lại sha từ file lúc ghi duyệt).
