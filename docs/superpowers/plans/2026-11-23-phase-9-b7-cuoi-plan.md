# Plan — B7 lượt đo CUỐI (đóng Phase 9), chạy CN 23/11/2026 khi code đứng yên (C, 15:09 16/11/2026)

**Là bản bổ sung cho plan B7 bản 2** (`2026-11-10-phase-9-b7-plan.md`, A duyệt `da7bff5d0c4e`; harness của B ở `data/phase_9/b7/tools/`, đã chạy giữa kỳ 12/11 —
`report_agent/2026-11-08_phase_9_ban_13/b7_implementation.md`). Hai bên, cách chấm mù, Holm 3 nhóm, `MAX_DROP` 4, luật "sàn phạm ⇒ ghi âm, không chỉnh rồi đo lại": **giữ nguyên**.
File này chỉ ghi chỗ khác: lượt nào chạy, vì sao, phần kín, thước, tiền, ai làm. Không chạy gì có phí khi viết. Review: B.

## 0. Tham số (A ghi lúc duyệt)
- `$C_DONG` = sha `main` lúc đóng code (A ghi sáng 23/11; mọi lượt kiểm `git diff $C_DONG HEAD -- backend` rỗng trước khi chạy). Bên RAG 1–8: tag `p9-moc` (`18e8f42`), worktree `/tmp/b7_moc`.
- `KIN_NGAY` **BẬT** (7 câu ngày kín mở lần đầu — đã để dành từ 12/11). Quỹ: §5.

## 1. Đo đúng chỗ đổi — lượt nào chạy lại (căn cứ đếm 0 USD, C 16/11)
- **Kho đổi từ 14/11** (204 ⇒ 263 bài, 8.435 ⇒ 9.425 đoạn; record build còn đổi tiếp sau đó — bước 0 ngày 23/11 ghi sha record + số point lúc chạy vào report, review B m-1). Cả hai bên tìm trên cùng Qdrant ⇒ **mọi lượt có tìm kho đổi đầu vào ở cả hai bên** ⇒ không dùng lại câu trả lời 12/11 của lượt đó, kể cả bên RAG 1–8.
- **Code agent đổi** `dfd0c96` ⇒ `main` (43 file `backend/`): câu nhiều ý, câu hỏi tiếp cho web, hết lượt tìm, lịch bản 2 + sửa lịch bằng lời, lưu trú / quán trong lịch, ảnh luồng lai.
- **Web đổi không qua kho:** lời dặn mục web `TU_WEB_LUAT` `e5f516aa383e` ⇒ `7180f74a00e6` (câu sức khoẻ, 16/11); cờ `cau_nhieu_y` + `web_cau_noi_tiep` đổi luật mở cổng web ⇒ W chạy lại (review B m-2).
- **Không đổi (đếm 16/11, B kiểm lại độc lập):** sha lời dặn định tuyến `8cd30cbb359a`, lời dặn trả lời `81d3040cf53f`, lời dặn trò chuyện `df921574c362` = đúng sha lúc giữa kỳ; `lan_tim_dau: v0`, `model: gpt-6-luna`, `router_timeout_seconds: 10` như nhau; `cau_nhieu_y` chỉ đổi lời dặn trả lời câu ≥ 2 ý, không chạm câu trò chuyện ⇒ **T phần đã thấy dùng lại số 12/11**. **Bước 0 ngày 23/11** so lại trên `$C_DONG`: ba sha + `lan_tim_dau` + `model` + `router_timeout_seconds` (review B m-5); khác một thứ ⇒ chạy lại T đã thấy.
- **Sửa lịch / xếp lịch không tìm kho** (lịch do code xếp) ⇒ lý do "kho đổi" không áp cho L đã thấy ⇒ dùng lại có điều kiện (§2 dòng L, review B M-1).

## 2. Lượt (mỗi lượt giữ ≥ 1 sàn; thứ tự lỗi User chốt: sai cảnh báo an toàn > nói chắc sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm)

| # | Lượt | Giữ sàn / kết luận nào (mức lỗi) | Chạy | USD ước |
|---|---|---|---|---:|
| A | An toàn 32 — agent ×2, RAG ×1 + thủ tục S-AT | S1 4 số (**lỗi mức 1**). Giữa kỳ **phạm** "thiếu cảnh báo mới" ở 1 câu loại miễn / giảm ⇒ bắt buộc chạy lại | đủ | agent 64 × 0,0007 ≈ 0,045 + RAG 32 × 0,00025 ≈ 0,008 + S-AT ≈ 0,007 ⇒ **0,06** (review B m-3) |
| G | Golden 176 — hai bên | S-G F1–F4 (nói chắc sai · ngoài kho bị trả lời — **mức 2, 3**), mức tụt (thiếu ý — mức 4), từ chối nhầm (mức 5); kết luận (i) câu nhiều nguồn | đủ | 0,12 |
| S | Ngoài phạm vi — agent: đã thấy 44 **×1** + **kín 10 ×2 (lần đầu)** (review B m-4) | S2 / S2b (**mức 3**). Giữa kỳ **phạm** S2b (2 câu mở cổng web) ⇒ bắt buộc; câu nhiều ý đổi luật mở cổng web | đủ | 64 × 0,0002 ≈ 0,015 (+ đường web của câu mở cổng) ⇒ 0,02 |
| N + K | Câu theo ngày 28 + **kín 7 (lần đầu)** — hai bên cùng ngày, liền nhau | kết luận (i) câu theo ngày; đáp án đổi theo ngày chạy | đủ | 0,03 |
| C | Chuỗi nhớ — agent 25 đã thấy + 15 kín đã dùng; RAG 14 chuỗi hỏi tiếp | (i) câu hỏi tiếp · (ii) nhớ tên ≥ 9 / 10 · sàn "hỏi tiếp ngoài kho bị trả lời" 0 (mức 3); web nối tiếp đổi đường hỏi tiếp | đủ | 0,05 |
| W | Web 10 + S2c 17 + 3 chuỗi nêu tên | (ii) web ≥ 6 / 10 (giữa kỳ **đúng ngưỡng**) + 0 truy vấn chứa tên; S2c | đủ | 0,04 |
| T | Trò chuyện — đã thấy 16 **dùng lại 12/11**; **kín 28 lần đầu** | (ii) trò chuyện ≥ 90 % (đếm trên kín) | chỉ kín | 0,01 |
| L | **Mới so với bản 2:** sửa lịch bằng lời Q3 — 10 chuỗi đã thấy + 5 kín, pass^2; biểu mẫu bản 2 bộ quyết | (ii) lịch trình (tính năng bật sau 12/11 nên chưa có trong B7). **Kín 5 chuỗi: luôn chạy** (chưa từng mở — số duy nhất không lạc quan); kín: **trước đó User chạy 3 lệnh §4**. **Đã thấy + biểu mẫu: dùng lại có điều kiện** — bước 0 tìm sha lượt Q3 / biểu mẫu gần nhất đạt; `git diff <sha đó> $C_DONG -- backend/llm/sua_lich_v2.py backend/llm/lich_trinh_v2.py backend/llm/len_ke_hoach.py backend/llm/do_so.py backend/llm/quan_lich.py backend/llm/luu_tru_lich.py` rỗng (biểu mẫu chấm cả ăn / ở — review B vòng 2) **và** lời dặn hiểu ý sửa lịch (`SUA_LICH_LOI_DAN`) giống byte ⇒ dùng lại số đó (report ghi "dùng lại, lý do"); khác ⇒ chạy. Q3 tự mô phỏng nhãn 0 USD trước (W84) | kín luôn; đã thấy có điều kiện | kín ≈ 0,015; đã thấy nếu phải chạy +0,035 [ước thô — người chạy ước lại từ lượt Q3 gần nhất] |
| | **Cộng** | | | **≈ 0,34** khi L đã thấy được dùng lại · **≈ 0,38** khi phải chạy |

**Không đo ở B7 (một dòng mỗi mục):** tốc độ (đo riêng lúc đóng code, ≥ 5 lượt mốc sạch cùng ngày) · hỏi bằng ảnh (Phase 10 có thước + thí nghiệm so ảnh riêng) · công cụ khoảng cách, bản đồ lịch (cờ tắt lúc viết; bật trước 23/11 thì dùng số đo của chính nhánh đó) · lịch câu tự do (cờ `lich_trinh` tắt) · khẩn cấp (quan sát, không sàn).

## 3. Thước + cách báo (thêm vào report B7, 0 USD, bằng code trên file kết quả)
- **Nhãn lỗi tự động (ý #15):** mỗi câu trượt được gắn **một** nhãn theo thứ tự lỗi ở §2, lấy từ trường máy / người chấm đã có: `an_toan` (đảo / thiếu / sai điều kiện) > `noi_chac_sai` (F2) > `ngoai_kho_tra_loi` (F1, S2, S2b, chuỗi) > `thieu_y` (câu tụt) > `tu_choi_nham`. Report có một bảng đếm theo nhãn × bên. Người chạy viết hàm này trước lượt có phí, rồi thử trên file giữa kỳ (phải ra đúng 2 câu S2b + 1 câu thiếu cảnh báo — ca đối chứng biết chắc ra "có").
- **"0 lỗi trên n ca" + luật ba (ý #16):** mọi sàn đạt "0" ghi kèm "0 / n ⇒ tỉ lệ thật ≤ 3 / n (95 %)" (vd 0 / 44 ⇒ ≤ 6,8 %). Không thêm câu để kéo n.
- **Dự phòng demo mất mạng (ý #17):** **không đo trong B7** — dựng lỗi mạng giả để thử là trái `Session_Prompt.md` §8 ("không dựng dead URL / đổi môi trường để tạo lỗi giả"). Thay bằng việc chuẩn bị, A xếp ngoài B7: quay màn hình các luồng chính trên bản đã đóng + bộ ảnh chụp, để dùng khi mạng hỏng lúc trình bày.

## 4. Phần kín — lệnh `!` (auto mode chặn agent đọc `*sealed*`; mỗi lệnh chỉ in số đếm)
**Trước 23/11, User chạy 3 lệnh đếm bộ kín sửa lịch** (handoff "User tự làm (1) + (1b)"; giữ nguyên đuôi `2>/dev/null | tail -1`):
```
grep -c -i -E "từ hiếu|trường tiền|tràng tiền|hải vân|bến ngự|tây hồ|an hiên|lập an" /home/minhhieu/hue_rag/data/phase_9/bo_do_sua_lich/chuoi_sealed.jsonl
cd /home/minhhieu/hue_rag/backend && BANG_FILE=diem_v9.json PYTHONPATH=/home/minhhieu/hue_rag/backend uv run python /home/minhhieu/hue_rag/data/nhan_cu_v9_2026-11-15/mo_phong_bang.py /home/minhhieu/hue_rag/backend /home/minhhieu/hue_rag/data/phase_9/bo_do_sua_lich/chuoi_sealed.jsonl --kin 2>/dev/null | tail -1; echo "ma thoat: ${PIPESTATUS[0]}"
cd /home/minhhieu/hue_rag/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/phase_9/bo_do_sua_lich/tools/kiem_bo.py --ca-kin 2>/dev/null | tail -1; echo "ma thoat: ${PIPESTATUS[0]}"
```
Đọc: lệnh 2 in "k / n chuỗi khớp" — k < n ⇒ nhãn kín cũ ⇒ A xếp một người **không viết code sửa lịch** sửa nhãn trước 23/11; không sửa kịp ⇒ L kín ghi NOT RUN, L đã thấy vẫn chạy. Lệnh 3 khuôn hỏng ⇒ như trên.
**Ngày 23/11** người chạy viết sẵn, chạy thử trên bộ đã thấy, rồi đưa User: (a) S kín + T kín — `data/phase_9/b7/tools/chay_kin.sh` (bản giữa kỳ, sửa `dfd0c96` ⇒ `$C_DONG`, bỏ phần C vì C kín chạy trong lượt C); (b) K — 1 lệnh mỗi bên + 1 lệnh dựng cặp mù sang file không mang tên kín (plan bản 2 §4 dòng K); (c) L kín — `q3_sua_lich.py` trên `chuoi_sealed.jsonl`, chỉ in số đếm. Bản khoá đổi ⇒ bỏ lệnh cũ, đưa lệnh mới (§5 luật câu kín). User vắng ⇒ ghi lệnh vào `STATUS_<người chạy>.md`; phần đã thấy vẫn kết luận được, phần kín ghi NOT RUN.

## 5. Ai làm · tiền · thời gian
- **Người chạy: B** (dựng + chạy harness giữa kỳ). L kín: User `!`. Người chấm: sub-agent mù, mỗi lô một agent mới (như giữa kỳ). **Đọc tay** câu trò chuyện đã thấy không cần (dùng lại); mục web (W) — sàn 0 truy vấn chứa tên đo bằng code. Review kết quả: E hoặc C (A giao; không phải người chạy).
- **Tiền ≈ 0,34–0,38 USD** (§2; đơn giá giữa kỳ: agent 0,00042 / câu kho, đường web ≈ 0,0018, an toàn ≈ 0,0007 — kho lớn hơn có thể làm câu đắt hơn). **Quỹ B7 giữ riêng 0,35** (spec §11.5) ⇒ **A xin User trần 0,45**. Pilot 10 câu Golden mỗi bên ⇒ ước lại; vượt ước > 50 % ⇒ dừng, báo A.
- **Thứ tự cắt nếu trần không đủ** (ghi trước, người chạy tự áp): (1) L đã thấy + biểu mẫu khi phải chạy lại (ghi NOT RUN, giữ L kín); (2) phần C kín ngoài 5 chuỗi hỏi tiếp + 4 chuỗi nhớ tên. **Không cắt A, G, N + K, S kín, L kín.** (S đã thấy đã về ×1 từ đầu.)
- Thời gian: sinh ~1 giờ (hai bên lần lượt; không session nào khác chạy server / model / lượt có phí cùng lúc), chấm ~1 giờ. CN 23/11 máy cả ngày cho hue_rag (lịch User).

## 6. Cần A / User quyết
1. Trần 0,45 USD cho B7 cuối (≈ 0,38 + dự phòng S-AT / chạy lại).
2. Đưa L (sửa lịch bằng lời + biểu mẫu bản 2) vào kết luận (ii) "lịch trình" — C khuyên **có** (tính năng đang bật, chưa từng có trong B7).
3. `$C_DONG`: sha nào là "code đứng yên" (sau khi bản đồ / khoảng cách quyết bật hay không).

## Lịch sử bản
- Bản 1 (C, 15:09 16/11/2026) — `d6a7a53`.
- Bản 2 (C, 15:13 16/11/2026): sửa theo review B vòng 1 (`…-plan_review.md`, 1 major + 5 minor) — M-1 L đã thấy + biểu mẫu dùng lại có điều kiện, L kín luôn chạy; m-1 bỏ sha record cứng, bước 0 ghi; m-2 lý do chạy lại W; m-3 phép nhân tiền lượt A; m-4 S đã thấy ×1 mặc định; m-5 bước 0 so thêm `lan_tim_dau` / `model` / `router_timeout_seconds`.
