# STATUS C — phiên 07/11 ở trên; mục "PHIÊN SAU ĐỌC TRƯỚC" dưới là của kết phiên tối 06/11 (lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`)

## PHIÊN 07/11 (terminal `hue-rag-a0`; A = `hue-rag-7a`, B = `hue-rag-10`, E = `hue-rag-81`) — cập nhật 13:25 07/11/2026 (`date`)
**Trạng thái: rảnh có lý do** — chờ User quyết bật biểu mẫu `lich_trinh_bieu_mau` (gồm cách hiểu F-a (4), handoff "Chờ User quyết" mục 1) + phiếu v7 thời lượng. Không mở việc mới. **Tiền C 07/11 ≈ 0,07 USD** (X1 0,056 · Q-N 0,004 · S3 0,009; còn lại 0 USD).
Việc đã xong (theo giờ, mọi report ở `report_agent/2026-11-06_giao_dien_cong/` trừ tự soi):
- 12:00 nháp harness S3 `data/phase_9/cong_dot_1/tools/do_bieu_mau.py` (nay `4de78cb35999`, thêm đếm `cat_ngay_cuoi`); [Chạy] `kieu_di` không đổi khung 0 / 120 tổ hợp (dữ kiện Q-U3).
- 12:19 Q-G tương phản bản mẫu 2 (`tuong_phan.py` `f53a31153ce3`: 0 cặp < 4,5; 2 gợi ý cho B) + nháp `playwright_cong.py` `fa580e39f5ed`.
- 12:31 bộ S3 chính thức `to_hop_chinh_thuc.jsonl` `792a3cbe3fe5` ghi trước (`c_s3_q_f_implementation.md`) · **C-tl** thời lượng web ⇒ `data/phase_9/lich_trinh/diem_v7_thoi_luong_web_nhap.json` `363763ae2101` + phiếu `diem_cho_user_v7.md` (19 / 26 điểm; "đi dày" khác 12 / 120) — chờ User · tự soi `report_agent/2026-11-07_tu_soi_lo_trinh/tu_soi_C.md`.
- 12:42–13:07 **X1 / X1b / X1c** lượt biểu mẫu bị từ chối (`c_x1_luot_bieu_mau.md`; dữ liệu `data/phase_11/cong_dot_1/x1/`): nguyên nhân = luật trình bày nằm trong bằng chứng; V2 (luật lên lời dặn hệ thống) hết từ chối nhưng chữ đầu p95 8,8 s; **V5 = V2 + reasoning `low`** đạt cả 4 tiêu chí trên bộ phát triển (p95 4,75 s); V4 (thêm câu dặn) kém; V6 `minimal` ⇒ 400.
- 13:11 **Q-G + Q-N trên `27ed091`: ĐẠT** (7 / 7 đích × 2 bề rộng, 0 CSP / console, JS gzip 101,9 KB, tương phản thấp nhất 5,42, Q-N 10 / 10; chữ đầu theo dõi p50 2,03 · max 4,22 s) — A đã merge (`main` `0dab4e5`).
- 13:24 **S3 Q-F bộ quyết trên `632a4f7` (V5): ĐẠT** — sàn code 24 / 24, F-a 12 / 12 + 12 / 12 (2 người chấm, 0 bất đồng), chữ đầu p95 4,25 s. Cả hai người chấm tự nêu: chữ model trung tính với người đi cùng ⇒ hiểu "phù hợp" = "không trái" (A ghi cả hai cách hiểu cho User). A commit `89b65be`.
- Câu treo đã được A trả lời: C210 giữ dùng số model; C211 rel / target ⇒ S2 (đã vào); mô phỏng kín sửa lịch: dời.
- Worktree `/tmp` của C: không còn (`c_x1`, `c_ui`, `c_s3` đã gỡ). Thư mục tạm `/tmp/c_tl/` chỉ có file thử / bảng tạm (không dữ liệu kín).

## PHIÊN SAU ĐỌC TRƯỚC (viết 06/11 — đã cũ một phần: mục S3 dưới đã XONG 07/11, S4 E làm; harness / lệnh sửa lịch vẫn đúng khi mở lại)
- **Đã xong tối 06/11** (terminal `hue-rag-42`):
  - **Harness sửa lịch:** `data/phase_9/sua_lich/tools/chay_sua_lich.py` md5 `559ebaf5f81e` — E review vòng 2 + vòng 3: **ready**. Bộ Q4 `bo_do_sua_lich/chuoi_q4.jsonl` `d35f8d9c5027`. Pilot = S01 + S06 (A duyệt). Report `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §7–§8.
  - **B171 review:** ready trên `b0e52f8` (đã merge `dbb4004`) — `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` §7–§8.
  - **C208:** `p9-sua-lich` ⇒ **`79b3d9c`** trên `main` `d930867` (pushed). Gỡ xung đột B5b; sửa `hoi_toi` khi xếp lại / sửa trực tiếp + 4 test. 411 test; Q1 / Q1m 228/228 (`data/phase_9/sua_lich/q1_c208/`). Nhãn đã thấy S03 / S08 sửa theo B171 ⇒ `chuoi_da_thay.jsonl` **`c00de07114b5`**. E kiểm rebase: ready.
  - **C209:** `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md` (P1 / P2 / P3 bản đồ + dữ liệu; C khuyên P1) — chờ User quyết khi A trình spec.
  - **C210:** chưa tái tạo được "hỏi lại số ngày thừa" ⇒ không sửa code (`report_agent/2026-11-06_b5_cau_tu_nhien/c210_implementation.md`). Đề xuất: harness kín lần sau ghi `so_ngay` model gửi + số code dò + có thẻ hỏi không.
  - **C211:** nháp kỹ thuật spec đợt 1 `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` — A dùng khi viết spec.
- **Việc đầu phiên sau — lệnh `!` mô phỏng bộ kín sửa lịch** (0 USD, chỉ in số đếm + mã chuỗi / số lượt hỏng, trên nền `79b3d9c`):
  1. C dựng lại worktree (đã gỡ):
     ```
     git worktree prune; git worktree add /tmp/c_sualich p9-sua-lich
     ln -s /home/minhhieu/hue_rag/data /tmp/c_sualich/data
     ln -s /home/minhhieu/hue_rag/knowledge-base-hue /tmp/c_sualich/knowledge-base-hue
     ```
  2. Đưa User lệnh nguyên văn (cũng ở report C207 §8):
     ```
     ! cd /tmp/c_sualich/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python ../data/phase_9/bo_do_sua_lich/tools/mo_phong_kin.py | python3 -c "import json,sys,re; d=json.load(sys.stdin); print('kin ok', sum(v=='ok' for v in d.values()), '/', len(d)); [print(k, [re.match(r'L[0-9]+', x).group() for x in v]) for k, v in d.items() if v != 'ok']"
     ```
  3. Kết quả hỏng ⇒ sửa nhãn kín bằng `bo_do_sua_lich/tools/cau_truc.py` (không in câu) **trước** lượt có phí. `main` đổi code ⇒ rebase + Q1 / Q1m trước.
- **Sửa lịch — HOÃN** (handoff 22:41 06/11): cần cờ `lich_trinh` câu tự do; A xem lại cách sửa sau biểu mẫu ("điền lại biểu mẫu"). Khi đi tiếp:
  - thư mục kết quả `data/phase_9/sua_lich/do/` chỉ chứa file kết quả (`--dung 0.19` cộng mọi `*.jsonl` trong đó);
  - pilot S01 + S06 lần 1 ⇒ đọc file ⇒ lần 1 / lần 2 / Q4 ×2 ⇒ kín ×2 qua User `!` ⇒ `cham`.
- **S3 — đo Q-F biểu mẫu lịch trình** (spec cổng đợt 1 `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` bản 2 `ff3c317ec88b` §6; khi B xong S1 trên `p11-cong-dot-1`; cờ mới `assistant.lich_trinh_bieu_mau`):
  - **trước lượt có phí:** ghi 12 tổ hợp vào report S3, **sau khi User chốt Q-U3** (đi dày). Phủ đủ 5 `di_cung`; mỗi `so_ngay` 1 / 2 / 3 ≥ 3 lần; ≥ 4 có `so_thich`; ≥ 2 không chọn sở thích;
  - harness lưu **khung + chữ model + tham số** mỗi lượt (dựng theo mẫu `chay_sua_lich.py`: TestClient trong tiến trình, bọc hàm, đọc log sau mốc). Ghi cả `so_ngay` model gửi / số code dò (đề xuất C210);
  - ×2 = 24 lượt. Sàn code 24 / 24: 0 câu từ chối thay lịch, `kiem_cuoi` 0 lỗi, 0 rút lại;
  - F-a: 2 sub-agent mới độc lập chấm (khung + chữ + giá trị nút), ≥ 11 / 12 mỗi lượt theo cả hai, bất đồng ⇒ trượt;
  - Playwright §6 (Q-G phần C được giao); tiền cả spec ≤ 0,03 USD.
- **S4 — review cả nhánh `p11-cong-dot-1`** một lần (`risk-gated-agent-review`; bảng rà AI FDE §7 là một tiêu chí). Ca dò khác cách người làm: API Khám phá `../`, `sealed`, id ngoài `corpus.sources`; form gửi `truong` lạ ⇒ 422.
- **Đợt 2 (dữ liệu bản đồ / lưu trú / ăn uống / sự kiện):** chờ User chọn P1 / P2 / P3 (C209). Chọn P1 / P3 ⇒ Overpass **một** lần lấy thẻ tên ⇒ khớp toạ độ 15 điểm thiếu (người xem bằng mắt). Chọn P2 ⇒ đo dung lượng PMTiles + cỡ gói MapLibre trước.
- **Câu treo cho A** (không chặn):
  1. mô phỏng kín sửa lịch có còn cần chạy đầu phiên không, khi sửa lịch hoãn và có thể đổi cách ("điền lại biểu mẫu");
  2. C210: câu nêu số ngày mơ hồ ("3 hay 4 ngày") + model gửi số ⇒ code hiện dùng số model, không hỏi — giữ hay hỏi;
  3. link trong chữ câu trả lời chưa có `target` / `rel` — gộp vào S1 / S2?
- **Bộ đo (private, md5 12):** sửa lịch đã thấy `c00de07114b5` (trước C208 `d0ad12b6ed12`) · kín `daf762bcbbe5` · Q4 `d35f8d9c5027`; B6 `6ed74db21616` / kín `4de04132600b`; B5b `7e1bc3da2e44`; bảng `diem_v5.json` `c7d294fcacd5`.
- **Không đọc:** `data/phase_9/b5_v2/`, `data/phase_9/b5/kin/`.
- **Tiền C tối 06/11: 0,003855 USD** (C210 tái tạo; mọi việc khác 0 USD). Overpass (OSM) quá tải 3/5 lượt — lần sau gọi một lần, ngoài giờ cao điểm.
- **Backlog cho A:**
  - kho mâu thuẫn vị trí Bảo tàng Cổ vật · câu thiên tai vẫn gọi Serper · case 67 Golden từ chối ngẫu nhiên;
  - link trong chữ câu trả lời chưa có `target` / `rel` (C211);
  - câu `toi_khong_diem` nói "hợp sở thích" cả khi không nêu sở thích (E, có sẵn trên `main`).

## Worktree / tạm
- Không còn worktree `/tmp` của C (gỡ 22:40 06/11/2026). Ca dò `/tmp/c_b171_tools/` mất khi khởi động lại — bản cần giữ đã ghi trong review.

## Bẫy (giữ)
- **Sửa trước khi tái tạo** (C210): việc "sửa lỗi X" mà nguyên nhân chưa chứng minh ⇒ tái tạo trên code gốc TRƯỚC (đọc tham số thật), chưa viết sửa — A phải nhắc lần này.
- Đổi hành vi code (vd B171 đổi khung) ⇒ chạy lại mô phỏng nhãn (`mo_phong.py`, kín qua `!`) **trước** lượt có phí.
- Q1m: `data/phase_9/b5b/tools/capture_flags.py <out> lich_trinh=1 sua_lich=0|1`. Script import `llm.*`: không `-I`, `PYTHONPATH=$PWD`.
- Rebase "hai bên cùng thêm": giữ cả hai, kiểm `git range-diff`. Heredoc shell có backtick ⇒ dùng Write.
- Ca dò của người kiểm gồm cả câu **hợp lệ** model hay viết. Giờ trong file: luôn `date` trước.
- Overpass máy chủ công khai hay quá tải (06/11: 3 / 5 lượt 502) ⇒ `out count` nhẹ qua được; lấy thẻ thì một lần, giãn cách, không gửi dồn.
- Tin A có thể đến lúc C đang làm việc khác ⇒ việc mới ưu tiên theo lời A (vd B171 trước harness); việc dở ghi STATUS trước khi chuyển.
