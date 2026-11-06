# STATUS E — kết phiên 12:14 06/11/2026 (`date`) · terminal `hue-rag-99` · Claude Opus 5.5 · vai thực thi (Phase 9 B5 v2 câu tự nhiên + Phase 10 giọng nói)

## PHIÊN TỐI 06/11 — đang làm (terminal `hue-rag-28`; A = `hue-rag-cc`, C = `hue-rag-42`; mở 20:58 06/11/2026)

- A giao (= User "làm đi"): (1) `duyet_tu_nhien_user.md` ⇒ nhắn A; (2) sửa plan G2 theo review ⇒ nhắn A; (3) E là người chạy kín v2 (harness B5 cũ + đường dẫn mới; trường ràng buộc cho 2 sub-agent chấm; 3 tiêu chí + ≥ 4/5) — chuẩn bị lệnh `!` chỉ in số đếm, chạy khi User duyệt độ tự nhiên **và** B171 merge.
- **Trạng thái (21:04 06/11/2026):**
  - (1) xong: `data/phase_9/b5_v2/duyet_tu_nhien_user.md`; A đã đưa User, chờ User trả lời.
  - (2) xong: plan G2 bản 2 sha `2ed4bd6e3153`, chờ review vòng 2. Công cụ đổi sha: `chuan_hoa` `190a9d4dfde3` · `doi_wav` `7986adebde78` · `g2_do` `4301654e6b42`.
  - (3) lệnh chạy kín v2 đã chuẩn bị (dưới).
  - (21:08 06/11/2026) A duyệt plan G2 (review vòng 2 ready). E sửa 3 minor n-1…n-3 ⇒ plan `92ec551531fd`, `g2_do.py` `a3a32eba4f94`. Tiếp: chờ User thu 40 câu (G1).
- **Lệnh chạy kín v2 — chạy khi User duyệt độ tự nhiên VÀ A báo B171 đã merge:**
  - Chạy ở working tree chung, `main` sau merge. Harness bật cờ `lich_trinh` **trong tiến trình**, không sửa `settings.yaml` ⇒ không cần worktree.
  - Lệnh `kiem` đã chạy 0 USD lúc 21:04 06/11/2026, trên `main` `7bc6927` ⇒ `n 5`, `ghep []`.
  - User sửa câu ⇒ md5 đổi ⇒ chạy lại `kiem` trước khi chạy có phí.
  - Ước ≈ 0,005 USD (5 câu, chưa đo trên bộ này).
  - Mọi lệnh dưới chỉ in số đếm / id / mã, không in câu hay chữ trả lời. Auto mode chặn ⇒ User `!` ở terminal E.
  ```bash
  md5sum /home/minhhieu/hue_rag/data/phase_9/b5_v2/cau_sealed.jsonl | cut -c1-12      # phải = de95ff85e491 (bộ khoá 06/11 tối)
  cd /home/minhhieu/hue_rag/backend && git log --oneline -1                           # có commit merge B171
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 timeout 120 uv run python ../data/phase_9/b5/tools/chay_b5.py kiem ../data/phase_9/b5_v2/cau_sealed.jsonl
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 timeout 900 uv run --env-file /home/minhhieu/hue_rag/.env python ../data/phase_9/b5/tools/chay_b5.py chay ../data/phase_9/b5_v2/cau_sealed.jsonl ../data/phase_9/b5_v2/kin_v2_ra.jsonl   # CÓ PHÍ; in n / loi / usd
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 timeout 120 uv run python ../data/phase_9/b5/tools/chay_b5.py dem ../data/phase_9/b5_v2/cau_sealed.jsonl ../data/phase_9/b5_v2/kin_v2_ra.jsonl    # 0 USD: kiểm cuối / lỗi khung / rút lại theo id
  ```
  - `dem`: bộ v2 không có trường `nhom` / `ky_vong` ⇒ `Q2a_n` = 0 và `lech_nhan` rỗng. Hai dòng đó không có nghĩa trên bộ này; việc so `b5_mong` để 2 agent chấm.
  - **Sau khi chạy:** 2 sub-agent Claude, ngữ cảnh mới, độc lập. Mỗi agent nhận: `cau_sealed.jsonl` (gồm `rang_buoc`, `b5_mong`, `can_cham`), bảng R1–R15 của `mau_cau_tu_nhien.md` §2, `kin_v2_ra.jsonl` (chữ trả lời + khung + nguồn), 3 tiêu chí Q3 nguyên văn (plan B5 `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` dòng 104, ngưỡng ≥ 4 / 5 cả 3).
  - Kết quả ⇒ `data/phase_9/b5_v2/cham_agent_{1,2}.md` ⇒ E đối chiếu 2 agent ⇒ báo A chỉ số ô đạt / lệch ⇒ User đọc ô không đạt.
- **(21:10 06/11/2026) Việc mới A giao: review harness sửa lịch của C** (một vòng, 0 USD; không mở `chuoi_sealed*`, không đọc STATUS_C). Ghi: `report_agent/2026-11-02_phase_9_code/c207_harness_review.md` (mới), worktree tạm `/tmp/e_rv_sl` (gỡ khi xong).
- **(21:17 06/11/2026) Review harness sửa lịch XONG:** `report_agent/2026-11-02_phase_9_code/c207_harness_review.md` — changes_requested, 1 major (Q4 đạt rỗng khi lượt lịch không có khung) + 6 minor; A chốt m-1 (Q3 chặt hay theo hành động) + m-5. Worktree `/tmp/e_rv_sl` đã gỡ. 0 USD.
  - A chốt: m-1 Q3 = hành động đúng nhãn, rút lại do kiểm cuối in số riêng + danh sách mã; m-5 giữ cách hiểu của C chỉ khi có test code giữ chỗ sau xếp lại (ghi tên test), không có ⇒ thêm lại kiểm. **Chờ C sửa harness ⇒ E kiểm phần sửa, ghi nối vào `c207_harness_review.md` ⇒ nhắn A.**
- **(21:33 06/11/2026) Harness vòng 2 XONG:** ready (`c207_harness_review.md` mục "Vòng 2"), còn n-1 minor (mkdir thư mục `do/`).
- **(21:33 06/11/2026) Bộ kín v2 — User bàn thẳng với E** (A cho): User đọc ⇒ K1 đạt, K2–K5 cần sửa (chưa thực tế, dài dòng). E viết lại 4 câu ngắn (mục "Vòng 2" trong `duyet_tu_nhien_user.md`); bản cũ `cau_sealed_v1_bo.jsonl`. Ghi `cau_sealed.jsonl` bị auto mode chặn ⇒ lệnh User `!`: `cd /home/minhhieu/hue_rag/backend && HF_HUB_OFFLINE=1 uv run python /tmp/e_kin_moi.py --ghi && md5sum ../data/phase_9/b5_v2/cau_sealed.jsonl | cut -c1-12` (script `/tmp` mất nếu máy khởi động lại ⇒ viết lại theo mục Vòng 2). Chờ User duyệt lại ⇒ md5 mới ⇒ báo A ⇒ sửa md5 trong lệnh chạy kín.
- **(21:55 06/11/2026) Rebase C208 (`p9-sua-lich` `79b3d9c`) kiểm XONG:** ready, 0 finding mới (mục "Vòng 3" của `c207_harness_review.md`).
- **(21:55 06/11/2026) Bộ kín v2: User duyệt đủ 5 câu** (vòng 3: E viết lại K2, K3). Script `/tmp/e_kin_moi.py` đã có bản cuối; **chờ User chạy `!`** (lệnh ở dòng trên) ⇒ md5 mới ⇒ báo A + sửa md5 trong lệnh chạy kín.
- **(21:57 06/11/2026) Bộ kín v2 KHOÁ:** User duyệt đủ 5 câu và chạy `!` ⇒ `cau_sealed.jsonl` 5 dòng, md5 **`de95ff85e491`** (sha256 `85f7dbd66e67`). Bản cũ `cd552f7cf7cb` lưu ở `cau_sealed_v1_bo.jsonl`. Script `/tmp` đã xoá. Mã ràng buộc: K1 R2·R3·R9 · K2 R1·R4·R10·R14·R15 · K3 R1·R3·R5·R15 · K4 R1·R3·R4·R15·R8 · K5 R1·R3·R9·R10·R15·R6. Ngoài lịch 2 / 5 (K4, K5). Lệnh chạy kín (dưới) dùng md5 mới; chạy khi A báo B171 đã vào `main` (đã vào — xem rebase C208) và A cho chạy.
- **(22:06 06/11/2026) Chạy kín v2 (A cho):** `kiem` 0 USD + chạy thử khoá giả OK ⇒ User `!` lượt có phí ⇒ n 5 · lỗi 0 · **0,003029 USD** (`data/phase_9/b5_v2/kin_v2_ra.jsonl`, main `c3ce3e5`). `dem`: hỏi lại K1 (mong đợi) + **K2** (câu có "2N1Đ", code dò 2 nhưng model gửi số khác ⇒ luật `chot_so_ngay` "lệch ⇒ hỏi"). 2 sub-agent chấm độc lập đang chạy ⇒ `cham_agent_{1,2}.md`. Report sẽ ở `report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`.
- **(22:09 06/11/2026) Kín v2 CHẤM XONG — Q3 không đạt 3 / 5** (2 agent khớp 15 / 15; K2 hỏi lại thừa, K3 không dày; K4 / K5 đạt nhờ lời code dựng khi model từ chối). Report `report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`; phiếu `data/phase_9/b5_v2/cham_agent_{1,2}.md`. Đã báo A. Tiền E phiên tối: 0,003029 USD.
- **(22:22 06/11/2026) E20 XONG:** H1 được ủng hộ — từ chối 3 / 4 câu hỏi kèm ↔ 0 / 4 đối chứng; 3 / 3 lượt từ chối đều có `tim_kho` sau lịch bị chặn (`TOOL_DA_DU_LICH`). Report `report_agent/2026-11-06_b5_cau_tu_nhien/e20_tu_choi_hoi_kem.md`; dữ liệu `data/phase_9/b5_v2/e20/`. 0,008092 USD. Đề xuất Sửa 1 (code nối câu cố định) / Sửa 2 (cho tìm thật 1 lần). Tiền E phiên tối: 0,011121 USD.
- **(22:26 06/11/2026) E21 XONG (0 USD, chỉ dữ liệu):** `data/phase_9/lich_trinh/diem_v6_thoi_luong_nhap.json` (sha256 `58453c1fa560`, từ v5, chỉ đổi thời lượng 2 điểm: Phá Tam Giang nửa buổi · Đại Nội nửa buổi = đề xuất căn cứ file vé) + phiếu `diem_cho_user_v6.md` (gộp 2 câu v5). Kho có thời lượng 7 / 33 (2 ngắn khác cụm) ⇒ **chạy `xep` thật: đi dày = thong thả** (1–3 ngày, 2 điểm / ngày) ⇒ cột thời lượng từ kho không sửa được K3; phiếu nêu 4 hướng cho User.
- **A quyết sau E20 / E21:** Sửa 1 + Sửa 2 của E20 chỉ làm khi xét bật đường câu gõ tự do (biểu mẫu không có câu hỏi kèm). Phiếu v6 A trình User cùng spec giao diện đợt 1 (nút "đi dày" phụ thuộc). **E rảnh có lý do — chờ User** (phiếu v6, thu 40 câu G1).
- **File sắp sửa (khai báo):** `data/phase_9/b5_v2/duyet_tu_nhien_user.md` (mới), `data/phase_10/giong_noi/plan_g2.md`, `session_prompt/sessions/STATUS_E.md`, mục E trong `CURRENT_HANDOFF.md`. Không sửa code.

## PHIÊN SAU ĐỌC TRƯỚC

### 1. E19 — bộ câu lịch trình tự nhiên cho B5 (việc A giao 06/11)

User đọc phiếu chấm B5 và thấy câu kín cũ không tự nhiên. Vì vậy cần bộ câu giống người thật hỏi.

- **(1)–(3) xong:**
  - TRIPO vòng 4: `data/nghien_cuu_tinh_nang_2026-11-06/tripo_v4/tripo_v4.md`.
  - Nghiên cứu cách người thật hỏi: Codex 2 lượt `data/tra_cuu_cli/2026-11-06_e19-*`, ra 20 lượt hỏi tiếng Việt trên VOZ; WebFetch kiểm 3 chủ đề.
  - Câu mẫu: `data/phase_9/b5_v2/mau_cau_tu_nhien.md` — 8 câu mẫu + bảng 15 loại ràng buộc R1–R15.
  - Report: `report_agent/2026-11-06_b5_cau_tu_nhien/e19_implementation.md` (A rà rồi commit).
- **User duyệt giọng 8 câu mẫu** ("Đạt, viết bộ kín theo giọng này"). A chốt hai câu hỏi còn lại:
  - **không** có câu hai lượt trong bộ kín;
  - **≥ 2 / 5** câu có phần ngoài lịch (chỗ ở / đi lại / giờ tới).
- **(4) bộ kín — đã viết:** `data/phase_9/b5_v2/cau_sealed.jsonl`, **5 câu**, md5 **`cd552f7cf7cb`** (sha256 `981ccb5120e6`). 4 / 5 câu có phần ngoài lịch.
  - Mỗi dòng có: `id`, `cau`, `rang_buoc`, `ngoai_lich`, `b5_mong` (trường B5 mong đợi), `can_cham` (điều cần chấm).
  - Không cho A / B / C xem. Báo A chỉ md5 + mã ràng buộc:

| Câu | Mã ràng buộc |
|---|---|
| K1 | R2 · R3 · R9 |
| K2 | R1 · R4 · R10 · R14 · R7 · R6 |
| K3 | R1 · R3 · R5 · R14 · R15 |
| K4 | R1 · R2 · R4 · R11 · R8 |
| K5 | R1 · R3 · R6 · R9 · R10 · R15 |

  - Đã đạt các yêu cầu ở §4 của file câu mẫu:
    - 1 câu ngắn thiếu số ngày;
    - 2 câu có tên điểm / lịch nháp;
    - 2 câu có người già / trẻ nhỏ;
    - câu có viết tắt kiểu "2N1Đ" / "ko";
    - 1 câu dài, kể hoàn cảnh, nhiều câu hỏi;
    - đủ 5 giá trị đi cùng (cặp đôi · người lớn tuổi · nhóm bạn · gia đình trẻ em · một mình).
  - Hàm dò số ngày của code (`do_so_ngay`) trên 5 câu: 4 câu ra đúng số; K1 ra None, đúng ý câu (thiếu số ngày).
- **Bước kế (CHƯA làm):**
  1. Viết `data/phase_9/b5_v2/duyet_tu_nhien_user.md` — bản cho **User** đọc, duyệt độ tự nhiên: 5 câu + ô tick "tự nhiên / sửa", không lộ `can_cham`. Đầu file ghi rõ "A / B / C không mở".
  2. Nhắn A **chỉ đường dẫn** để A đưa User.
  3. User sửa câu nào ⇒ E sửa ⇒ md5 mới ⇒ báo A.
  4. Sau đó A tổ chức: B171 sửa 2 loại lỗi code (đo trên bộ đã thấy) ⇒ chạy kín mới ⇒ 2 agent chấm ⇒ User đọc chỗ không đạt.

### 2. Giọng nói — NGHE (Phase 10)

- Spec bản 4 `784d6f7abd9f` đã duyệt.
- **G0 xong:** nhánh `p10-giong-noi` `93bbc63`, đã push.
- **G1:** chờ User thu 40 câu (`data/phase_10/giong_noi/thu/` **rỗng** lúc kết phiên). Bộ câu C205: `bo_40_cau/cau.jsonl` md5 `a24d445bfe61`.
- **Plan G1 + G2 bản 1:** `data/phase_10/giong_noi/plan_g2.md` sha256 **`555a35af92ab`**. **Chờ review** — A giao một sub-agent, kết quả sẽ ở `data/phase_10/giong_noi/plan_g2_review.md` ⇒ sửa nếu cần ⇒ A duyệt sha.
- Công cụ `data/phase_10/giong_noi/tools/`:

| File | sha256 (12) | Việc |
|---|---|---|
| `chuan_hoa.py` | `75544e8560e0` | chuẩn hoá chữ + số; tự kiểm 24 ca OK |
| `doi_wav.py` | `effed30bcf2a` | G1: ffmpeg ⇒ WAV 16 kHz mono + manifest; không xoá file gốc |
| `g2_do.py` | `10680ec17c79` | G2: V-a…V-e, chép 2 lần để kiểm tất định, `--cham` chấm lại |

  Đã chạy thử 0 USD trên 3 file mẫu kèm gói model (thư mục thử `/tmp` đã xoá).
- **Plan chốt** (reviewer có thể đổi):
  - gộp mọi người đọc khi quyết;
  - V-a tính cả cụm như nhãn `doc`;
  - vòng 1 thử hotwords điểm 4 / 8, vòng 2 điểm 12 hoặc 2;
  - V-e ≤ 1 / 40 lần đọc;
  - không nhận cách nói tắt "ba lăm nghìn" / "một triệu hai".
- **Khi User thu xong:** kiểm `thu/nguoi_doc.md` (không tên thật) ⇒ `doi_wav.py` ⇒ xoá file gốc (User `!` nếu `rm` bị chặn) ⇒ đo theo plan ⇒ report ⇒ A.
- Tạo lại worktree khi cần code G3: `git worktree add /tmp/e_giong p10-giong-noi`.
- TTS: để sau.

### 3. Việc cũ còn chờ User (A hỏi)

- Bật `anh.bat`?
- Xoá collection thử `hue_anh_siglip2` (172 điểm)?
- Luật "gói Python ≥ 2 tuần"?

## Tiền

- **E phiên 06/11: 0 USD.** Codex tra web chạy bằng gói ChatGPT; TRIPO không tốn; Playwright và đo giọng nói chạy trên máy.
- Phase 10 tổng vẫn 0,098380 / trần 0,15.

## Bẫy / đã học

- `.venv` chung **có `sherpa-onnx`**, nhưng `uv.lock` của `main` chưa có (tới khi `p10-giong-noi` merge).
  - `uv run` giữ gói; **`uv sync` thường ở `main` sẽ gỡ mất**.
  - Cài lại: từ worktree nhánh chạy `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen`.
- **Codex tra web tiếng Việt:** lượt chung chung chỉ ra 1 bài tiếng Việt. Lượt hai chỉ rõ diễn đàn (VOZ…) và đòi "mở trang 1 của chủ đề" thì ra 20 lượt hỏi ⇒ yêu cầu phải nêu nơi tìm cụ thể.
- **TRIPO:** biểu mẫu đủ trường ⇒ không gọi mô hình, không hỏi thêm.
  - Chỉ bấm "Xác nhận phương án"; chờ chữ trang dài thêm ≥ 150–200 ký tự rồi đứng yên 3 × 2 s (đây là bài học vòng 3).
  - Ô nhập tự sinh câu chậm hơn lúc bấm chip ⇒ đọc giá trị sau cùng.
- **`do_so_ngay`** không dò được "4n3d" (d không dấu), "2 hôm", "cuối tuần", "đi trong ngày" ⇒ dựa vào model. Đã báo A; không phải lỗi.
- **Hàm chuẩn hoá số:**
  - "không" trong "phải không" từng bị đọc thành 0 ⇒ đã bỏ;
  - "hai trăm nghìn một người" từng ra 200.001 ⇒ đã tách số đơn đứng sau "nghìn".
- CSP trang chặn `page.wait_for_function` của Playwright ⇒ chờ bằng locator.
- Script đặt theo đường dẫn không thấy gói `backend/` ⇒ `PYTHONPATH=<worktree>/backend`.

## Câu hỏi cho A

- Bộ kín B5 v2: chạy bằng harness đo B5 cũ, đổi đường dẫn bộ câu, hay cần chỗ đọc trường `b5_mong` / `can_cham` cho 2 agent chấm? Người chạy kín không được xem câu, nên cần lệnh `!` chỉ in số đếm (`Session_Prompt.md` §5).
- Plan G2: chờ kết quả review của sub-agent.
