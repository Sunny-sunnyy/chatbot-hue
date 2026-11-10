# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 19:05 10/11/2026 (A, mở phiên 10/11 — mục "VIỆC PHIÊN 10/11" ngay dưới). Trước: 22:27 09/11/2026 (A, kết phiên 09/11).

## VIỆC PHIÊN 10/11 (A giao 19:05 10/11/2026 — User cấp quyền "như 09/11 + trần Phase 9 4,2")

Luật chung việc này: **mức nhẹ** (`Session_Prompt.md` §7: ≤ 0,2 USD, không đổi kiến trúc ⇒ plan 1 trang: tiêu chí ghi trước + bộ đo + tiền ⇒ **A đọc rồi duyệt, không review plan** ⇒ code ⇒ đo 1 lượt ⇒ **1 review cả nhánh** (C) ⇒ A merge). Cả B và E chạm `backend/llm/assistant.py` ⇒ mỗi bên **worktree `/tmp` riêng**, nhánh riêng; merge lần lượt (ai review đạt trước merge trước, bên sau rebase + chạy lại test file chạm). **Lượt đo tốc độ không chồng nhau:** trước khi đo, nhắn A + bên kia "bắt đầu đo"; bên kia lúc đó không chạy lượt trả phí / việc nặng CPU; xong nhắn "đo xong". Mỗi lượt đo / bộ kiểm trong plan ghi rõ **giữ sàn nào** (vòng tự soi: không chỉ ra được ⇒ không chạy). Đổi cờ `settings.yaml` ⇒ test file chạm chạy cả có lẫn không `--env-file`.

| Session | Việc | Tiêu chí (sàn ghi trước) | Tiền | Đầu ra |
|---|---|---|---|---|
| **B** `hue-rag-05` | **Xã giao chạy song song định tuyến** (giống #6 cho tuyến `tro_chuyen`): gọi model trò chuyện cùng lúc với định tuyến, tuyến khác ⇒ bỏ phần đã chạy. Nhánh `p9-xa-giao-song-song`. Đọc: `assistant.py` hàm chạy song song #6 + `_pick_route`; plan #6 `docs/superpowers/plans/2026-11-04-phase-9-toc-do-song-song-plan.md`; số S5 `data/phase_9/s5_chung/` | xã giao chữ đầu p95 ≤ 5 s (S5 7,73); câu Huế / ngoài phạm vi không chậm hơn S5 quá nhiễu; **không chữ nào hiện trước khi định tuyến xong** nếu tuyến cuối không phải `tro_chuyen` (chạm thứ tự hiện chữ ⇒ bộ an toàn 32 đủ 4 số); cờ tắt ⇒ chuỗi gửi model giống byte | ≤ 0,1 USD | plan 1 trang ⇒ A; report `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_implementation.md` |
| **E** `hue-rag-e4` | **Câu ngày nhanh hơn:** code tính sẵn ngày (hôm nay / đổi âm ↔ dương khi dò thấy) đưa vào ngữ cảnh thay vì model gọi công cụ `ngay_lich` 3–5 lần. Nhánh `p9-t1-nhanh`. Đọc: `backend/llm/ngay_lich.py`, `assistant.py` `ngay_lich_for_turn`; report T1 `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md`; bộ câu ngày đã có | câu ngày chữ đầu p50 ≤ 3 s, p95 ≤ 5 s (S5 5,19 / max 11,0, n = 5 ⇒ đo 15–20 câu); ≤ 0,0005 USD / câu; **đúng ngày không tụt** so T1 đang bật (cùng bộ câu ngày); câu không có từ chỉ ngày ⇒ chuỗi gửi model giống byte | ≤ 0,1 USD | plan 1 trang ⇒ A; report `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md` · **19:40 10/11/2026: CHỜ REVIEW (C)** — nhánh `p9-t1-nhanh` `7d6f25f` (đã push); tiêu chí 1–6 đạt sau sửa (a); chữ đầu p50 5,60 ⇒ 2,35 s, p95 10,14 ⇒ 4,56 s; 0,00036 USD / câu; ≈ 0,031 USD |
| **C** `hue-rag-4f` | **Review cả nhánh** B rồi E khi mỗi bên báo xong (`risk-gated-agent-review`, chỉ dựa plan + diff + số đo). Trước đó: rảnh (ghi "rảnh — chờ review" ở `STATUS_C.md`) | — | 0 (chạy lại ≤ 0,01 nếu cần) | `<việc>_review.md` cạnh report |
| **B** (sau xã giao) | **Chuẩn bị deploy trên máy (không AWS):** đưa nhánh `p12-deploy-nhap` lên `main` (sau 140 commit), áp mục "Checklist trước deploy" ở "Câu hỏi A còn nợ" làm được không cần User: 3 biến chốt trong `compose.yml`, `--proxy-headers --forwarded-allow-ips` cho uvicorn sau Caddy, allow-list `dung_dockerignore.py` theo `main` hiện tại (đếm lại: 0 file evaluation / sealed / sao lưu / `data/` private trong ảnh). Build + chạy thử `docker compose` cục bộ (container có `--name`, tắt khi xong; RAM ~15 GB — một việc nặng một lúc, không trùng lượt đo của E), `/health` + 1 câu trong kho + 1 ngoài kho + 1 lượt quá giới hạn ⇒ 429. **Không làm:** tạo tài khoản / tài nguyên AWS, quyết `tra_web` / ảnh #5 trên bản công khai (ghi thành câu cho User). Đọc: `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`, `yeu_cau_tra_aws.md` | ≤ 0,01 USD | report `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md`; push nhánh |
| **C** (xen giữa, review ưu tiên trước) | **Nháp plan B7** (so cả hệ với RAG 1–8 — spec Phase 9 §5 "B7", §8 tiền 0,35): bộ nào (Golden 176 + an toàn 32 + phần kín chưa mở của các bộ mới — chỉ **liệt kê tên file / số câu / đã mở chưa**, không mở nội dung kín), ai viết / chạy phần kín, harness có sẵn dùng lại được gì, cờ bật lúc chạy = trạng thái `main` lúc đóng tính năng (tham số), lịch chạy, tiền. **Tag `p9-moc` spec ghi nhưng chưa có** (`git tag -l` rỗng) ⇒ C đề xuất commit (ứng viên `18e8f42` = cha thứ nhất của merge B0 `1c10111`; đối chiếu với commit lượt đo cuối 01/11) — A gắn tag. Áp `Session_Prompt.md` §7 (bỏ đo không giữ sàn) | đọc spec §4, §5 B7, §8; `data/do_cuoi_2026-11-01/` (chỉ tên file / manifest) | 0 USD (không chạy lượt có phí) | `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` (nháp) ⇒ A |

- **B — A duyệt plan `docs/superpowers/plans/2026-11-10-phase-9-xa-giao-song-song-plan.md` sha `47009c7dc791` (19:10 10/11/2026)**: AT (a) dùng lại 4 số an toàn của `main`; vượt 0,0005 USD / câu ⇒ merge cờ `false`, A trình User.

- **E — A duyệt plan `docs/superpowers/plans/2026-11-10-phase-9-t1-nhanh-plan.md` (trên nhánh `p9-t1-nhanh`) sha `935f9358e25d`.**
- **Chốt vòng tự soi 1 (19:14 10/11/2026, A; ý B / C / E):** B: AN dùng đúng bộ 90 của #6 (bỏ 22 câu thêm), S 60 câu (bỏ 5 câu ngày), AT dùng lại 4 số `main`; report thêm số lượt (iii) bị huỷ giữa chừng + một câu về huỷ task khi người dùng ngắt kết nối (chưa test ⇒ ghi rõ, không dựng test mới). E: **D1 chỉ làm các dạng có trong 19 câu ngày + 5 câu S5** (hôm nay / mai, ngày âm nêu trong câu, ngày âm lễ hội trong kho dạng "… âm lịch" / "rằm, mùng … tháng …") — bỏ tuần từng ngày / tháng này / năm tuỳ ý khi bộ không có; dạng khác để công cụ `ngay_lich` dự phòng; Golden 9 chỉ bên nhánh, so đáp án mẫu; một người chấm, chỉ câu hai bên khác nội dung; giữ mốc 19 câu chạy hôm nay + 4 an toàn × 2 + Q1. C: review chỉ chỗ rủi ro (B: `finally` huỷ / hàng đợi / gộp trace; E: dò ngày âm trong đoạn kho + nguồn lịch chen vào lượt từ chối); report có bảng mỗi câu + lệnh chạy lại một chỗ; C không chạy lại lượt tốc độ.

Điều kiện dừng: tiền dự phóng vượt 0,1 / việc ⇒ nhắn A; sàn an toàn / đúng ngày tụt ⇒ dừng, báo A (không chỉnh lời dặn vòng 2 khi chưa báo). Không làm: thêm tính năng, đổi model, đổi lời dặn ngoài phần cần cho việc.
Nguyên văn phần đầu phiên 07/11 (11:53 → 15:43 07/11/2026): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-07.md`; 06/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-07_cong_dot_1_tu_soi.md`.

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 22:27 09/11/2026, kết phiên 09/11)

**Phiên 09/11 đã kết** (User: "chuẩn bị kết thúc session"). Quyền phiên 09/11 **hết hạn** ⇒ A mới hỏi lại User một câu. Nguyên văn handoff trong phiên: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-09.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-09_ngay_am_lich_g_phuong_an_b_chot_deploy.md`. Tổng hợp đợt: `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (mục 09/11).

**Hệ thống (`main` = `origin/main`):** như 08/11 + từ 09/11: **định tuyến phương án B** (`3b52017`: giữ 4 tuyến, tuyến khẩn cấp ⇒ trợ lý Huế, bỏ câu khẩn cấp soạn sẵn) · **công cụ ngày + âm lịch BẬT** (`ngay_lich: true`, `7eb1f12`) · **4 chốt trước deploy** bằng biến môi trường (`ccc9f4f`: `HUE_LUOT_MOI_NGAY`, `HUE_COOKIE_SECURE`, `HUE_TAT_DOCS`, log xoay vòng 10 MB × 3; không đặt ⇒ như cũ). Cờ tắt: `lich_trinh` câu tự do, `hoi_lai`, `ban_do_lich`.
**Đóng hồ sơ 09/11 (đo âm, tag):** G cổng 2 nhóm `hoso/p9-g-cong` · T2 tra web thành công cụ `hoso/p9-t2-web` · T3 bảng vé + giờ `hoso/p9-t3-bang` · T4 lịch trình câu gõ `hoso/p9-t4-lich`. Giới hạn nhận (User): câu ngoài phạm vi thỉnh thoảng có mục web (1/20 kín G; câu y tế bị định tuyến xếp khẩn cấp); câu bỏ điều kiện mùa mưa lũ (có cả bản cũ); câu lịch thuần không nhắc Huế ⇒ ngoài phạm vi.
**Luật mới 09/11 (User):** vòng tự soi bắt buộc mỗi phiên (`Session_Prompt.md` §7 dòng đầu — A mở khi mỗi session có kết quả đầu tiên + trước kết phiên; bỏ test không bảo vệ sàn); rảnh là bình thường (bỏ "rảnh phải giao việc", `WORKFLOW.md` §9.2); mọi phương án tự trả lời "đã thấy ở người dùng thật / lượt đo thật chưa · không làm mất gì" (`propose-options`). User: tiền API thoải mái nhưng phải nhanh; "cắt giảm nhưng vẫn đảm bảo chất lượng"; giữ 4 session; User học dự án **sau khi xây xong** (A nhắc muộn nhất ~15/12).
**Tiền 09/11:** ≈ 0,62 USD (B ≈ 0,22 G + phương án B · E ≈ 0,35 T1 + T2 + T4 · C ≈ 0,03 T3 + chốt deploy · A ≈ 0,003 cổng · S5 B: xem dưới). Phase 9 ≈ 3,6 / 4,0 (≈ 3,0 trước 09/11; số cộng từ report). Quỹ B7 0,35 ⇒ việc mới cần User nâng trần.
**S5 chung (B, `main` `0ce6713`, 1 lượt Chromium, 65 câu, 0,0197 USD — `data/phase_9/s5_chung/`):** câu Huế chữ đầu p50 2,16 / p95 4,32 s ✓, 0,00047 USD / câu ✓ · ngoài phạm vi 1,62 / 2,97 s ✓ · **xã giao 3,46 / 7,73 s ✗** (đường cũ, không đổi hôm nay: định tuyến ~1,7 s xong mới gọi model trò chuyện) · **câu ngày (n = 5, cờ bật) p50 5,19 / max 11,0 s ✗, 0,00063 USD ✗** (3–5 lần gọi model / câu). So 07/11 câu Huế chậm hơn ~+0,4 p50 / +0,7 p95 (khác bộ — tham khảo). Đề xuất chưa đo: xã giao chạy song song định tuyến (như #6); câu ngày — **User 22:32 09/11/2026: giữ bật, tối ưu sau** (đo thêm 15–20 câu ngày; thử code tính sẵn ngày đưa vào ngữ cảnh thay vì model gọi công cụ).

### Làm tiếp (theo thứ tự)
1. **Hỏi User quyền phiên** (một câu) ⇒ **mốc đóng tính năng** (User 09/11 chưa chốt; A đề xuất 30/11; căn cứ: đợt 2 hôm nay 4 / 5 việc âm) ⇒ **W61 + W59** (gom một lần, sổ vòng 23).
2. **User khi rảnh (không chặn):** duyệt **bảng điểm v7** `data/phase_9/lich_trinh/diem_cho_user_v7.md` (thời lượng 19 điểm từ web ⇒ nút "dày lịch" của biểu mẫu mới có tác dụng — hiện gần như không, E rà 09/11); tick phiếu toạ độ bản đồ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` (⇒ bật `ban_do_lich`); thu 40 câu giọng nói (`data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`).
3. ~~**User `!` xoá 7 nhánh**~~ — **XONG 22:40 09/11/2026** (User chạy; tag `hoso/p9-*` giữ code). (đã kiểm: 3 đã merge, 4 có tag hồ sơ cùng commit; worktree đã gỡ): `git branch -d p12-chot-deploy p9-g-b p9-t1-sang-nam && git branch -D p9-g-cong p9-t3-bang p9-t2-web p9-t4-lich && git push -q origin --delete p12-chot-deploy p9-g-b p9-t1-sang-nam p9-g-cong p9-t3-bang p9-t2-web p9-t4-lich` (nếu User chưa chạy lúc kết phiên).
4. **Còn trong phạm vi trước đóng gói:** bản đồ (chờ phiếu), giọng nói (chờ 40 câu, nhánh `p10-giong-noi`), deploy AWS (nhánh `p12-deploy-nhap` + 4 chốt đã có; checklist ở "Câu hỏi A còn nợ"), B7 đóng gói. Đợt 2 cổng (lưu trú, ăn gần, sự kiện) chưa bắt đầu — chờ User chốt mốc đóng tính năng.
5. Giới hạn biểu mẫu "Lên kế hoạch" (E / C rà 09/11, chưa thấy ở người dùng thật ⇒ chỉ ghi báo cáo): "dày lịch" gần như không tác dụng (bảng thiếu thời lượng ⇒ v7); người lớn tuổi / trẻ em không bao giờ có buổi tối; không có ô "lo mưa".

### Nhánh
`main`; **đang mở:** `p12-deploy-nhap` (chờ deploy), `p9-sua-lich` (hoãn), `p10-giong-noi` (E), `p9-b5c` + `p9-toc-do-6` (hồ sơ). 7 nhánh 09/11 đã xoá (User). Worktree `/tmp`: không còn (đã gỡ 09/11).

### Mã hay gặp
G = cổng 2 nhóm (đóng; phương án B đang chạy); T1 ngày + âm lịch (bật); T2 web thành công cụ, T3 bảng vé + giờ, T4 lịch trình câu gõ (đóng hồ sơ); S1–S6 / S2b / S2c / S3b = sàn §12.3; B0–B7 = bậc Phase 9; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`.

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

| # | Ý | Trạng thái |
|---|---|---|
| 1–7, 12 | Kiểm giá "…000đ" / "triệu"; không đủ điểm ⇒ câu cố định; `khong_xep` + lý do từ mã luật; dòng giả định do code nối; test cố tình vi phạm; dòng "Mình hiểu…"; cột `ten_khac`; lời dặn không dùng địa danh thật làm ví dụ | vào B5 (`d66f6a3`) |
| 8 | Sửa lịch nhiều lượt (`sua_lich` hành động có tên, khung giữ ở server, Đã đổi / Giữ nguyên, ≤ 2 hành động / lượt) | code trên `p9-sua-lich` `79b3d9c` (rebase lên B5b + B171, giữ `hoi_toi` / lý do buổi tối — C208); harness đo E review ready; **hoãn** (cần cờ `lich_trinh` câu tự do) |
| 9 | Bộ chuỗi sửa lịch pass^k | bộ `data/phase_9/bo_do_sua_lich/` (10 + 5 kín; nhãn đã thấy S03 / S08 sửa theo B171 — C208); plan chọn pass^2; pilot = S01 + S06 (A đồng ý) |
| 10 | Cột trong nhà / bậc thang ⇒ phương án ngày mưa | phiếu gộp **v6** `data/phase_9/lich_trinh/diem_cho_user_v6.md` chờ User (gồm 2 câu v5 + cột thời lượng E21) |
| 11 | `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — theo dõi | C210 06/11: code không dò "3N2D" / "4n3d" / "2 hôm" / "cuối tuần" nhưng model tự gửi đúng số 5 / 5; biểu mẫu bỏ vấn đề này |
| 13, 14 | Ưu tiên theo lĩnh vực; đoạn gần trùng | đếm 0 USD xong — không mở thí nghiệm (C179) |
| 15–17 | Nhãn lỗi tự động; "0 lỗi trên n ca" + luật ba; dự phòng demo mất mạng | B7 |
| 18 | Router gắn cờ ⇒ code gọi `lich_trinh` | không cần (Q2a đạt) |

**Không làm** (đã cân): lọc cộng tác / rating, TSP, GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới, nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.


## Câu hỏi cho User (hỏi mỗi lần một câu)

**Hỏi khi User về (User 19:18 10/11/2026: "gác lại câu hỏi cho tôi khi quay lại"):** (Q-BC) **sắp xếp lại `bao_cao_he_thong/`** để đọc theo thứ tự, hiểu hết hệ thống không cần đọc code — A chuẩn bị 2–3 phương án từ 2 sub-agent đọc thử (`data/ra_soat_bao_cao_2026-11-10/`); trong lúc chờ A chỉ **sửa chỗ sai / cũ** (luật báo cáo luôn mới nhất), không đổi cấu trúc / tên file. (Q-CO) cờ tốc độ: **xã giao song song (B) — 19:31 10/11/2026 CHƯA ĐẠT tiêu chí ghi trước** (60 câu, 1 lượt, ≈ 0,027 USD; `data/phase_9/xa_giao_song_song/s_r1.jsonl`): xã giao chữ đầu p50 3,46 ⇒ 1,85 s nhưng p95 7,73 ⇒ 5,74 s (sàn 5); ngoài phạm vi p95 5,21 s ✗ (2 câu bị định tuyến xếp sang Huế); Huế 2,28 / 4,23 ✓; ngoài phạm vi 0,00056 USD / câu (> 0,0005); AN 90 lượt 0 lọt chữ. Đuôi p95 nghi do định tuyến xếp nhầm / chậm (giả thuyết). A không sửa tiêu chí, không merge; hỏi User: bật dù p95 chưa đạt (C review sẵn) hay đóng hồ sơ. **Câu ngày nhanh (E)** — tốc độ + tiền đạt (p50 5,60 ⇒ 2,35 s, p95 10,14 ⇒ 4,56 s, 0,00049 ⇒ 0,00036 USD), 1 câu tụt "năm nay" ⇒ A chọn sửa bằng code + chạy lại ~8 câu; xong ⇒ C review ⇒ hỏi User bật (thay bản đang chạy). **Lưu ý: nhánh `p9-t1-nhanh` không có cờ riêng** (chạy dưới `ngay_lich` đang bật) ⇒ merge = đổi bản đang chạy ngay ⇒ A chờ User "có" rồi merge + cổng ổn định; C review M-1 (dò "mùng N tháng M" thiếu chữ "âm") E đã sửa `0385bcf`, C đang xem delta.
(Q-DP, khi tới deploy AWS — không hỏi sớm) B 10/11 deploy cục bộ đạt (`p12-deploy-nhap` `8d650ad`, report `b_deploy_cuc_bo_implementation.md` §3): tra web trên bản công khai · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền · xoá ảnh docker cũ.
(Q-NG) **Câu ngày không nhắc Huế bị xếp ngoài phạm vi** — E 10/11: 9 / 19 câu ngày bị định tuyến từ chối ở cả bản cũ lẫn mới (giới hạn A chọn giữ 09/11) ⇒ phần nhanh chỉ tới câu đi trợ lý. Hỏi User: trợ lý Huế có nên trả lời câu lịch / ngày âm chung (không nhắc Huế) không — đổi phạm vi sản phẩm ⇒ User quyết; nếu có ⇒ sửa lời dặn định tuyến (cần đo bộ tuyến + an toàn).

(1) ~~Quyền phiên~~ (10/11: như 09/11 + trần 4,2). (2) ~~Mốc đóng tính năng~~ — **User 19:08 10/11/2026: không chốt mốc; xong sớm đóng sớm, xong muộn đóng muộn, vẫn đảm bảo chất lượng** (A không hỏi lại; giữ mốc cứng đã biết: đóng code = chạy trên AWS ~25–30/12, nhắc User học muộn nhất ~15/12). (3) ~~Vòng cải tiến 23~~ — User 19:12 10/11/2026: duyệt **W59** + **W61** (đã vào `Session_Prompt.md` §7, §8); W62 / W63 bỏ. Cũ còn chờ (xét lúc kết phiên, không hỏi lẻ): W60 / W58 / W57 / W4 + W39. **Không gấp:** xoá collection thử `hue_anh_siglip2`; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; ảnh cũ `hue-rag-app:nhap` có file private (User `! docker image rm hue-rag-app:nhap`); báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo. Đã đóng 09/11: tiền (trần 4,0), T3, khẩn cấp sau G, bật T1.

## Câu hỏi A còn nợ (không cần User)

- **09/11:** T1 đã bật (xong lượt xác nhận + lượt sau G); giới hạn T1: "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên 10/11 (mở 19:02 10/11/2026):** A `hue-rag-55` · B `hue-rag-05` · C `hue-rag-4f` · E `hue-rag-e4` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên 10/11 (User chọn "như 09/11 + trần 4,2", A ghi nhận 19:05 10/11/2026):** như 09/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác; tiền API thoải mái nhưng ưu tiên tốc độ, không test vô nghĩa). **Trần Phase 9 nâng 4,0 ⇒ 4,2 USD** (cho 2 việc tốc độ, quỹ B7 0,35 giữ riêng). Hết hạn cuối phiên.
  **Thêm (19:12 10/11/2026) User:** "hạn chế test các phần không cần thiết, không over-engineer, muốn đẩy nhanh quá trình; chi phí API vẫn duyệt; các session cùng trao đổi, thảo luận để đề xuất, chốt phương án" ⇒ A mở vòng tự soi 1 ngay (plan B / E là kết quả đầu); tiền không còn là lý do giữ bộ đo — thời gian là thước.
  **Thêm (19:15 10/11/2026) User đi nghỉ:** "tiếp tục điều phối, phát triển, triển khai, ghi báo cáo đầy đủ; câu cần User chốt thì gác lại, triển khai phần khác; **không đưa câu hỏi lúc User vắng** (treo việc)" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User".
- **Phiên 09/11 (User chọn "như 08/11", A ghi nhận 20:13 09/11/2026):** A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác. Trần Phase 9 nâng 4,0. Hết hạn cuối phiên.
  **Thêm (20:21 09/11/2026) User:** "thoải mái tiền API cho triển khai, phát triển nhưng phải đảm bảo tốc độ; không làm những thứ vô nghĩa hay test những thứ mất thời gian; 4 bạn trao đổi, thảo luận cùng nhau để đưa ra phương pháp, hướng xử lý phù hợp" ⇒ ưu tiên tốc độ làm; cắt test / đo không phục vụ sàn chất lượng; B / C / E bàn thẳng với nhau, A chốt khi lệch phạm vi.
- Spec Phase 9 file hiện tại sha `01b7476a3eb1` ≠ bản duyệt `5557f0fd7650` do commit `442f758` (bỏ mốc ngày theo User 08/11; sàn + tiền không đổi) ⇒ sửa chữ, không cần duyệt lại (A ghi 20:13 09/11/2026).
- **Quyền phiên 08/11 HẾT HẠN (12:50 08/11/2026, kết phiên).** (User 11:06: ~13:00 dừng; User 12:50 08/11/2026: để nhiệm vụ / câu hỏi cho phiên sau.)
- **Phiên 08/11 (User chọn "như 07/11", A ghi nhận 09:22 08/11/2026):** như 07/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, khoá Serper cho tra cứu, việc cần User duyệt thì gác). Hết hạn cuối phiên. Giao lúc mở: B ảnh cổng (`p11-anh-cong`), C review ảnh, E rà "Câu hỏi A còn nợ" (chỉ đọc).
- **Phiên 07/11 (User chọn "như 06/11", A ghi nhận 11:55 07/11/2026):** A tự điều phối — giao ngay việc có sẵn trong handoff, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5. Hết hạn cuối phiên.
  **Thêm (12:30 07/11/2026, User đi nghỉ):** "tiếp tục nghiên cứu, triển khai, phát triển, đánh giá, viết báo cáo đầy đủ; việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; làm việc khác; tự do nghiên cứu, gọi Codex tra cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau". Trần tiền như trên (≤ 1 USD / phiên). **(12:31 07/11/2026) User: "trần tiền tôi vẫn duyệt nếu quá 1$, có thể thoải mái thực nghiệm"** ⇒ vượt 1 USD / phiên được; A vẫn ghi tiền thật từ log mỗi việc + báo tổng ở nhật ký.
- Phiên tối 06/11 — hết hạn 22:41 06/11/2026. Tiền phiên ≈ 0,027 USD.
- **Tiền Phase 9: trần 4,0 USD** (User nâng, A ghi nhận 20:15 09/11/2026; dự phóng việc chờ ≈ 0,55: G 0,12 · T1 0,04 · T3 0,05–0,1 · T2 0,21 · T4 0,12; quỹ B7 0,35 giữ riêng). Trước: 3,5 (User nâng 10:38 08/11/2026; trước 2,5) (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
- **Đã duyệt, không hết hạn theo phiên:** spec giao diện cổng đợt 1 bản 2 `ff3c317ec88b` (User 11:56 07/11/2026); plan G2 giọng nói `92ec551531fd` (A duyệt sau review 2 vòng, 06/11 tối); spec Phase 10 bản 4 `784d6f7abd9f` (sherpa-onnx, tải model ≤ 300 MB, thu 40 câu; Web Speech bỏ); tải SigLIP 2 + collection ảnh (11:42 05/11); luật S-AT mới (20:14 05/11); cache câu trả lời ⇒ Phase 12 (20:27 05/11); bật `tra_web` (21:15 05/11).
- **User (09:00 05/11/2026):** cần công cụ / nghiên cứu / tải / khoá mới ⇒ tự nghiên cứu (0 USD, thông tin công khai) + đề xuất; thêm công cụ / thư viện lớn / tải model / khoá / tài khoản mới vẫn trình User trước (`Session_Prompt.md` §4).
- **Phase 9 (spec):** Serper dùng luôn (User chấp nhận rủi ro điều khoản); gói npm giao diện như đã duyệt 02/11; dữ liệu công khai dùng cho học tập, không kiểm giấy phép (05/11).
- **Thường trực:** A commit / push — hỏi User trước (luật chung), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (`WORKFLOW.md` §9.6); B / C / E không commit trừ khi việc ghi rõ; duyệt cho A = duyệt cho B / C / E; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. **(12:32 07/11/2026) User: khoá `SERPER_API_KEY` dùng được cho tra cứu nghiên cứu** (gọi qua `uv run --env-file /home/minhhieu/hue_rag/.env …`, không đọc / in khoá; chỉ câu tra thông tin công khai; 0,001 USD / lượt, ghi số lượt). Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper: 0,001 USD / lượt. Open-Meteo: 0.

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | bộ kín 40 câu — **đã dùng** 01/11 | `7f97d4c10b2b` |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối Phase 1–8 (mốc của Phase 9) | — |
| `data/phase_9/` | bộ đo B4 / B5 / B5c / B6 / sửa lịch, bảng điểm v3 / v4, toạ độ, kết quả đo | — |
| `data/phase_10/anh/` | bộ ảnh đo, danh sách tên, patch `p10-anh`, E9 | — |
| `data/sua_kho_2026-11-05_gio/` | sửa kho giờ mở cửa: lệnh `tools/chay.sh`, sao lưu record / sparse | — |
| `data/nguon_mo_huegov_2026-08-05/` | dữ liệu mở Huế (có file dữ liệu cá nhân ⚠ — không vào kho / báo cáo) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C / E sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file); review ≤ 2 vòng.
- **Bộ an toàn 32 câu luôn báo đủ 4 số** (đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời).
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (tự viết); `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server bằng TaskStop (không `pkill -f`); (3) chạm tìm / chia đoạn: T1 giống byte; (4) 3 chỗ báo cáo (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Đang dựng chỉ mục / đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant.** Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ. `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 06/11 sáng + tối nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`.

- Phiên tối 05/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`.
- Phiên 05/11 sáng–chiều nguyên văn (C173–C197, B156–B163, E1–E8, quyết định theo giờ, merge B4b / B5 / #6, B5c âm): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`.
- Phiên 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`, `…_2026-11-03_toi.md`; 02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
