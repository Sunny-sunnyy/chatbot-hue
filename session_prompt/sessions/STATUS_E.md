# STATUS E — cập nhật 13:01 07/11/2026 (`date`) · terminal `hue-rag-81` (A `hue-rag-7a`, B `hue-rag-10`, C `hue-rag-a0`) · Claude Opus 5.5 · vai thực thi · **RẢNH, chờ User** (A 13:01: không tự mở việc mới)

## Đang chờ (07/11, sau phiên sáng)

- **User kiểm 27 ảnh** (`data/nghien_cuu_giao_dien_2026-11-06/anh/commons/xem_anh.html`) ⇒ B đưa vào build (S2). Cần thì E tìm tiếp ảnh cho 3 điểm thiếu / các điểm "chưa thử".
- **Giọng nói:** User thu 40 câu **hoặc** quyết giữ / cắt khỏi đồ án (E đề xuất cắt — `tu_soi_E.md` §4). Thu xong ⇒ G2 (mục 4 dưới).
- **Phiếu v6:** User tick ⇒ E chốt `diem_v6.json` + chạy `kiem_v6.py`.
- Review / việc mới: A nhắn.

**Tiền E 07/11: 0,000953 USD** (3 câu đo RAM, E-dep). Commons / Codex tra web / review / ca dò: 0.

## Đang làm (A giao 07/11, sau merge cổng `0dab4e5`)

- **Cập nhật báo cáo User — XONG 13:22 07/11/2026, chờ A review + commit** (chỉ tài liệu, 0 USD): `LUONG_HOAT_DONG_HE_THONG.md` bản 31 (tóm tắt 07/11, sơ đồ, bảng thành phần, bước 15 thời tiết + 16 cổng, số chữ đầu 07/11, việc kế tiếp); `BAO_CAO_SINH_CAU_TRA_LOI_API.md` bản 40 (tóm tắt, sơ đồ, checklist 5 dòng mới, mục 4 07/11 gồm X1 V0–V6, §5, §6); `README.md` (đầu file, 2 dòng báo cáo, dòng Phase 9, dòng streaming).

## Đã làm 07/11 (A giao — tất cả xong)

- **Review B-dep — XONG 13:06 07/11/2026** (0 USD): `report_agent/2026-11-07_tu_soi_lo_trinh/e_review_b_dep.md` — **changes_requested**: code `p12-deploy-nhap` `50e4ebf` đạt; **M-1** ảnh Docker chứa 16 file `*/evaluation/` + `meta/` 148 file (sao lưu Golden) vì dockerignore chỉ loại `evaluation/` ở gốc kho; 5 minor. **Vòng 2 13:26: ready** — E đếm riêng ảnh `nhap2`: kho = đúng 204 `corpus.sources` + 1 file `meta/`, 0 file đánh giá / câu kín / sao lưu / `.env`; m-6 mới (cache uv 1,9 GB, không chặn). Ảnh cũ `nhap` nên xoá (User `!`). Worktree `/tmp/e_rv2` đã gỡ.

- **E-anh — XONG 12:30 07/11/2026** (bắt đầu 12:16; A giao; 0 USD): 27 ảnh giấy phép mở Wikimedia Commons (CC0 / PD / CC BY / CC BY-SA) cho bản mẫu 2 cổng đợt 1 — 2 hero · 5 ô lĩnh vực · 20 thẻ điểm; 3,2 MB; mỗi ảnh ≤ 200 KB (trừ hero Ngọ Môn 218 KB).
  - Đầu ra: `data/nghien_cuu_giao_dien_2026-11-06/anh/commons/` — `xem_anh.html` (lưới ảnh để User kiểm), `danh_sach.md` (chỗ dùng · file · địa điểm · tác giả · giấy phép · link · mức chắc + vì sao · thiếu ảnh · chưa thử), `tai_ve.json` (tác giả đầy đủ cho dòng ghi công), `chon.json`, `ung_vien.json`. Thư mục con riêng để không lẫn ảnh chụp màn hình B172 trong `anh/`.
  - Công cụ: `tools/tai_anh_commons.py` (tim / ung_vien / tai; chờ theo Retry-After khi 429), `tools/dung_trang_anh.py`.
  - [Chạy] E tự xem cả 27 ảnh; đổi 4 ảnh yếu (Bạch Mã ảnh sân bay, Thiệu Trị ảnh cũ chụp trên cao, 2 ảnh Lăng Cô sai cảnh). Mức chắc: 22 cao / 5 vừa. Thiếu: Điện Hòn Chén, bãi Thuận An, núi Ngự Bình. 4 ảnh có người rõ ⇒ đánh ⚠ (không ảnh nào làm hero). Trang chạy headless: 27 / 27 ảnh hiện, 0 ảnh ngoài.
  - Không đụng `frontend/`, nhánh B, file C. Ảnh vào build ⇒ B ở S2 sau khi User kiểm.

- **XONG 11:59 07/11/2026 — script kiểm v5 ↔ v6 theo ô tick** (0 USD, chỉ đọc): `data/phase_9/lich_trinh/tools/kiem_v6.py`. Không đụng `diem_v3/v5`, phiếu thật, `settings.yaml`.
  - Lệnh (từ `backend/`): `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python ../data/phase_9/lich_trinh/tools/kiem_v6.py <phiếu đã tick> <diem_v6.json>` ⇒ in `OK` / danh sách lỗi, mã thoát 0 / 1.
  - Xét 3 nhóm ô tick (Đại Nội · 2 bảo tàng · dòng 32) + Phá Tam Giang cố định; mục 3 (hướng "đi dày") không phải ô tick ⇒ không xét. Căn cứ `file:dòng «chữ»` so kho bằng `grep_kb.sh`; `nap_bang` thật.
  - [Chạy] thử 8 ca giả ở `/tmp/e_kiem_v6/`: 2 ca đúng ⇒ OK; 6 ca sai (Đại Nội lệch ô tick, đổi trường ngoài ô tick, thiếu tick, tick 2 ô, căn cứ sai dòng, dòng 32 chưa bỏ) ⇒ đều báo lỗi đúng chỗ.
  - Lúc chốt thật: bỏ chữ "ĐỀ XUẤT, chờ User" trong căn cứ Đại Nội (nếu User chọn A); ghi `ghi_chu` "BẢN 6 … User duyệt <giờ>".

- **Tự soi — XONG 12:32 07/11/2026** (A giao, 0 USD): `report_agent/2026-11-07_tu_soi_lo_trinh/tu_soi_E.md`. Chờ A chốt chung với B / C.

- **E-dep — XONG 12:38 07/11/2026** (bắt đầu 12:33, A giao): report `report_agent/2026-11-07_tu_soi_lo_trinh/e_dep_chuan_bi_deploy.md`; nháp `data/phase_12/deploy_nhap/` (`Dockerfile`, `compose.yml`, `Caddyfile`, `yeu_cau_tra_aws.md` — **chưa build**); tra web `data/tra_cuu_cli/2026-11-07_e-dep-aws/`. [Chạy] RSS app 1,49 → 1,51 GB, Qdrant 378 MiB ⇒ máy 4 GB. Tiền 0,000953 USD (3 câu). Không sửa `backend/`.

- **S4 review cổng đợt 1 — XONG 12:56 07/11/2026** (A giao, 0 USD): `report_agent/2026-11-06_giao_dien_cong/s4_review_backend.md` (`0cb0b0a`, ready; Q1 228 / 228 E tự chạy; m-5 bớt ngày 3 / 120) + `s4_review_frontend.md` (`f20fd28`, ready; m-f1 regex link `//`, m-f2 `<title>`). Worktree `/tmp/e_rv`, `/tmp/e_rv_main`, `/tmp/e_rv_do/` **đã gỡ** (A cho, 12:57).
- **E-tb — XONG 12:58 07/11/2026** (A giao, 0 USD, chỉ đọc): `report_agent/2026-11-07_tu_soi_lo_trinh/e_tb_bang_bang_chung.md` — bảng bằng chứng theo khâu cho quyển báo cáo + slide (nhãn ai đo; lỗ hổng bằng chứng trước bảo vệ).

- **Kịch bản demo 5 phút — NHÁP XONG 13:00 07/11/2026** (A giao, 0 USD): `report_agent/2026-11-07_tu_soi_lo_trinh/e_demo_5_phut.md`. Câu mẫu **chưa chạy thử** (cần ≈ 0,005 USD trên bản cuối); User đọc / sửa.

## PHIÊN SAU ĐỌC TRƯỚC (viết 22:40 06/11/2026 — phần chờ đã cập nhật ở mục "Đang chờ" trên)

**E không có việc đang làm dở, không có code dở, không có worktree.** Việc chờ đều do User:
1. **G1 giọng nói:** User thu 40 câu (`data/phase_10/giong_noi/thu/` vẫn **rỗng**). Khi có ⇒ làm theo plan G2 (mục 4 dưới).
2. **Phiếu bảng điểm v6** (`data/phase_9/lich_trinh/diem_cho_user_v6.md`): A trình User cùng spec giao diện cổng đợt 1. Có 4 ô tick:
   - Đại Nội dùng căn cứ file vé?
   - hướng "đi dày" (4 hướng);
   - 2 bảo tàng "trong nhà"?
   - giữ / bỏ dòng 32.

   User chọn ⇒ E chốt v6 theo ô tick (A giao).
3. Việc cũ A hỏi User: bật `anh.bat`? xoá collection thử `hue_anh_siglip2`? luật "gói Python ≥ 2 tuần"?

**Việc kế của E, theo thứ tự (handoff mục "Phiên sau làm theo thứ tự" bước 5):**
- (a) **G1 ⇒ G2** khi User thu xong — mục 4 dưới, plan `92ec551531fd`. 0 USD, chạy máy.
- (b) **Phiếu v6** — User tick (A hỏi cùng Q-U3 của spec cổng) ⇒ E chốt `diem_v6` theo ô tick (A xác nhận 07/11).
  - User chọn hướng (1) "luật xếp đi dày bằng code" ⇒ việc của B, E không làm.
  - Hướng (2) "thời lượng theo loại" ⇒ E soạn bảng theo loại để User duyệt từng dòng.
- (c) **Review spec cổng đợt 2** khi A viết (C209 P1 / P2 / P3) — theo `risk-gated-agent-review`, ≤ 2 vòng.
- (d) **Hoãn, chỉ làm khi A giao lúc xét bật câu gõ tự do:**
  - E20 Sửa 1 (code nối câu cố định khi lời do code dựng + có `tim_kho` sau lịch), đo bộ E20 ×1 ≈ 0,008;
  - Sửa 2 (cho `tim_kho` tìm thật 1 lần sau lịch), đo ×2 ≈ 0,04;
  - report `e20_tu_choi_hoi_kem.md` §5.
- (e) Có thể đề xuất (A quyết): dò lỗi K2 "hỏi lại số ngày thừa". C210 chưa tái tạo được. Cách dò: `e20/tools/chay_e20.py` ghi đúng số ngày model gửi; 3–4 câu tự viết có số ngày viết tắt kiểu "số ngày + số đêm" ⇒ ≈ 0,002 USD.

## 1. Đã xong phiên tối 06/11 (mọi việc A giao; A commit)

| Việc | Kết quả | File |
|---|---|---|
| Bộ kín B5 v2 — User duyệt độ tự nhiên | 3 vòng bàn thẳng với User ở terminal E (A cho): K1 đạt vòng 1; K4, K5 vòng 2; K2, K3 vòng 3 (E viết lại theo ý User: ngắn, một nhu cầu thật, không cài ý thử tính năng). Khoá md5 **`de95ff85e491`**; bản bỏ `cd552f7cf7cb` ⇒ `cau_sealed_v1_bo.jsonl` | `data/phase_9/b5_v2/duyet_tu_nhien_user.md` |
| Chạy + chấm kín v2 | n 5 · lỗi 0 · 0,003029 USD. 2 sub-agent khớp 15 / 15 ⇒ **Q3 không đạt 3 / 5** (i 4/5 · ii 3/5 · iii 4/5). K2 hỏi lại thừa (model gửi số ngày khác số code dò); K3 "đi dày" không dày; K4 / K5 đạt nhờ lời do code dựng khi model từ chối ⇒ `lich_trinh` giữ tắt. User chọn "biểu mẫu trước" | `report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`; phiếu `data/phase_9/b5_v2/cham_agent_{1,2}.md` |
| E20 — từ chối khi hỏi kèm | 10 câu tự viết (cặp có / không hỏi kèm), ghi trước. Từ chối 3 / 4 ↔ 0 / 4; cả 3 lượt từ chối đều gọi `tim_kho` sau lịch và bị chặn (`TOOL_DA_DU_LICH`). 0,008092 USD. A: Sửa 1 / Sửa 2 chỉ làm khi xét bật đường câu gõ tự do | `report_agent/2026-11-06_b5_cau_tu_nhien/e20_tu_choi_hoi_kem.md`; `data/phase_9/b5_v2/e20/` (bộ `d79ffecd2c0b`, công cụ `tools/chay_e20.py` ghi thêm câu tìm + tham số số ngày) |
| E21 — cột thời lượng | v6 nháp từ v5 (đổi 2 điểm). Kho có thời lượng 7 / 33 ⇒ chạy `xep` thật: **đi dày = thong thả** ⇒ cột từ kho không sửa được K3 | `data/phase_9/lich_trinh/diem_v6_thoi_luong_nhap.json` (sha256 `58453c1fa560`) + phiếu v6 |
| Plan G2 giọng nói | sửa theo review vòng 1 + 3 minor vòng 2; **A duyệt**. Bản chạy: plan `92ec551531fd`; công cụ `chuan_hoa` `190a9d4dfde3` · `doi_wav` `7986adebde78` · `g2_do` `a3a32eba4f94` | `data/phase_10/giong_noi/plan_g2.md`, `plan_g2_review.md` |
| Review harness sửa lịch của C | vòng 1 changes_requested (1 major: Q4 đạt rỗng) ⇒ vòng 2 ready ⇒ vòng 3 (rebase C208 `79b3d9c`) ready, 0 finding mới | `report_agent/2026-11-02_phase_9_code/c207_harness_review.md` |
| Review spec giao diện cổng đợt 1 | vòng 1 changes_requested (1 major: Q-F chưa đo được) ⇒ vòng 2 ready. A sửa n-1 ⇒ sha `ff3c317ec88b`, chờ User duyệt | `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design_review.md` |

## 2. Lệnh / công cụ dùng lại

- Chạy một bộ câu đơn qua lõi thật, cờ `lich_trinh` bật trong tiến trình (từ `backend/`):
  ```bash
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/phase_9/b5/tools/chay_b5.py kiem <bo.jsonl>                    # 0 USD
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 OPENAI_API_KEY=sk-fake OPENAI_BASE_URL=http://127.0.0.1:9 uv run python … chay <bo> /tmp/x.jsonl   # chạy thử 0 USD
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 timeout 900 uv run --env-file /home/minhhieu/hue_rag/.env python … chay <bo> <out>   # CÓ PHÍ — auto mode chặn ⇒ User `!`
  ```
- Muốn biết model gửi tham số gì / tìm câu gì: dùng `data/phase_9/b5_v2/e20/tools/chay_e20.py` (cùng khuôn lệnh).
- Chấm bằng 2 sub-agent: brief ghi file `/tmp` (đề chấm nguyên văn + câu + đường dẫn dữ liệu + "không xem phiếu kia"), dùng `general-purpose` ngữ cảnh mới (không `fork`), mỗi agent ghi một file `cham_agent_<N>.md`.

## 3. Bẫy / đã học (phiên tối 06/11)

- **Auto mode chặn agent ghi file `*sealed*`** (đọc thì được) ⇒ viết script `/tmp` dựng file, User chạy `!`. Xong thì xoá script `/tmp`.
- **Câu kín agent viết hay "cố tự nhiên"**: cài ý để thử tính năng (giờ ra ga, tiền vé), câu dài, chi tiết lạ. User bắt 2 vòng. Cách đạt: mỗi câu **một nhu cầu thật**, có chủ ngữ, ngắn vừa đủ.
- User đổi ý giữa chừng ("bạn tự làm đi, sao lại là tôi làm") khi E đề xuất User tự gõ câu ⇒ với việc soạn nội dung, mặc định E làm, User duyệt.
- **Lượt `!` dài hơn 120 s** bị chuyển nền ⇒ đọc file output khi có thông báo; `| tail -1` giữ đầu ra tới khi xong.
- **Gõ giờ tay khi viết review** ⇒ hook bắt (22:41 ≠ `date` 22:39) ⇒ luôn chạy `date` ngay trước khi ghi, dán đúng chuỗi.
- Harness B5 cũ (`chay_b5.py`) không lưu tham số công cụ ⇒ không biết model gửi số ngày nào ở K2. Bản E20 đã ghi thêm.
- Trước: `.venv` chung có `sherpa-onnx` nhưng `uv.lock` của `main` chưa có ⇒ **không `uv sync` ở `main`** (cài lại: từ worktree `p10-giong-noi` chạy `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen`).
- Codex tra web tiếng Việt: phải nêu nơi tìm cụ thể (VOZ…, "mở trang 1 của chủ đề").

## 4. Giọng nói — khi User thu xong 40 câu (G1 ⇒ G2)

1. Kiểm `thu/nguoi_doc.md` (mã người đọc, vùng giọng, "đã đồng ý", không tên thật).
2. `uv run python -I data/phase_10/giong_noi/tools/doi_wav.py`. Thiếu câu / trùng / > 10 s ⇒ báo A **trước** G2.
3. Xoá file gốc `thu/<MA>/`; `rm` bị chặn ⇒ User `!`.
4. Đo theo plan `92ec551531fd` §3–§6: kiểm RAM ≥ 5 GB; mỗi cấu hình một lệnh `timeout 600`.
5. Report `report_agent/2026-11-05_phase_10_anh/e<số>_g2_giong_noi.md` ⇒ A.

- Worktree khi cần code G3: `git worktree add /tmp/e_giong p10-giong-noi` (nhánh `93bbc63`).

## Tiền

- **E phiên tối 06/11: 0,011121 USD** (kín v2 0,003029 + E20 0,008092; đều Phase 9). Chấm agent = quota Claude. Codex / Playwright / giọng nói: 0.
- E phiên sáng 06/11: 0 USD. Phase 10 tổng vẫn 0,098380 / 0,15.

## Câu hỏi cho A (treo)

- ~~Ai chốt `diem_v6`~~ — **đã trả lời** (handoff bước 5 + A 07/11): User tick ⇒ **E chốt** `diem_v6.json`; A đổi `lich_trinh_bang` khi merge S1. Chưa tick ⇒ S1 dùng v3.
- Mục (e) trên: có cho dò K2 bằng `chay_e20.py` (≈ 0,002 USD) không, hay để B / C?
- `p10-giong-noi` (`93bbc63`) chưa merge ⇒ `uv.lock` của `main` chưa có `sherpa-onnx`. Bẫy `uv sync` còn tới khi merge (G3).
