# Implementation Report: C209 — nguồn dữ liệu cho đợt 2 giao diện cổng (bản đồ · lưu trú · ăn uống · sự kiện)

Người làm: C (Claude Code, Opus 5.5)
Date: 22:18 06/11/2026 (`date`)
Canonical guide: mục việc C209 trong `session_prompt/CURRENT_HANDOFF.md` ("Việc giao — giao diện cổng du lịch", A 22:01 06/11/2026)

## 1. Phạm vi

- Nghiên cứu, **0 USD**, không sửa code / kho. Kết quả chi tiết (private): `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md`.
- File này chỉ ghi **số đếm, nguồn công khai và phương án**. Không chép nội dung kho; không chép giá trị từ dữ liệu mở (có trường liên hệ / mã số thuế).

## 2. Đã làm

1. **Dữ liệu đã có:**
   - kho — đếm bằng `scripts/grep_kb.sh` (số file / dòng theo mẫu);
   - bảng điểm lịch trình v5 — số điểm có toạ độ;
   - dữ liệu mở Huế — script `data/nghien_cuu_giao_dien_2026-11-06/c209/tools/dem_truong.py`: chỉ in tên trường + số bản ghi có giá trị + số toạ độ trong vùng Huế, **không in giá trị**;
   - `data/phase_11_nghien_cuu/luu_tru/` (E5).
2. **OSM Overpass:** khung trung tâm Huế.
   - 2 truy vấn `out count` đạt: đếm theo nhóm, và đếm có lọc thẻ;
   - 3 lần lấy thẻ đầy đủ bị máy chủ báo quá tải (502): 2 máy chủ, giãn cách, không gửi dồn.
   - File thô ở `data/nghien_cuu_giao_dien_2026-11-06/c209/raw/`.
3. **Tra web:** `scripts/tra_web_codex.sh`.
   - Yêu cầu chỉ chứa thông tin công khai: `data/nghien_cuu_giao_dien_2026-11-06/c209/yeu_cau_tra_web.md`.
   - Kết quả: `data/tra_cuu_cli/2026-11-06_c209-ban-do-nguon/` — 251 s, 0 lệnh shell, 17 trang mở được, 9 URL tự khai.
4. **Tự kiểm [đã kiểm]:**
   - WebFetch luật dùng tile OSMF; trang chủ + Quick Start của OpenFreeMap;
   - curl `data.hue.gov.vn`: HTTP 200, tiêu đề "Hệ thống dữ liệu mở thành phố Huế";
   - đọc CSP hiện tại (`backend/api/app.py` `FRONTEND_CSP`: không domain ngoài nào).

## 3. Kết quả chính (số đếm)

| Lớp | Kho | Dữ liệu mở Huế (bản 05/08/2026) | OSM (khung trung tâm, 06/11/2026) |
|---|---|---|---|
| Tham quan | 36 file điểm + 29 file di sản. Toạ độ số: 5 file. Bảng lịch trình: **18 / 33 điểm có toạ độ** | điểm du lịch 183 / 196 có toạ độ; di tích 179 / 180 (đủ địa chỉ, giờ, giá) | 91 điểm (tên 56); `historic` 126 |
| Ăn uống | 91 file món, 85 dòng địa chỉ quán gợi ý, **0 toạ độ** | 6.794 cơ sở, toạ độ ~đủ, **giờ / giá 2 / 6.794**, 1 nhóm, không phân loại | 697 (tên 522, giờ 158, điện thoại 115) |
| Lưu trú | không danh sách; **1 mục "nên ở khu nào"** (3 nhóm khu) | **không có** | 208 (tên 166, điện thoại 47, website 24, giờ 16) |
| Sự kiện | 27 file; 16 có ngày cụ thể; 5 nhắc 2026–2027 | 138 lễ hội có toạ độ, **không trường ngày** | không có |

**Nguồn ngoài:**
- trang sự kiện chính thức chỉ là HTML, **không có RSS / iCal / API** [Codex] ⇒ nhập tay;
- danh sách 21 cơ sở lưu trú 4–5 sao là bài viết, không toạ độ [Codex];
- OSM: ODbL ⇒ phải ghi công. Phân phối CSDL rút từ OSM ⇒ share-alike [Codex].

**Bản đồ:**

| Lựa chọn | Khoá | Gửi ra ngoài | Nhận xét |
|---|---|---|---|
| Leaflet + tile OSMF | không | IP + vùng xem + Referer | không SLA, cấm tải trước / offline, cảnh báo dùng thương mại [đã kiểm] |
| MapLibre + OpenFreeMap | không — "no registration… no API keys, and no cookies"; cho thương mại [đã kiểm] | IP + vùng xem | **chỉ tile vector** ⇒ Leaflet phải kèm plugin MapLibre [đã kiểm — sửa khuyến nghị của Codex] |
| MapLibre + PMTiles tự host | không | **không gì** | dung lượng chưa đo |
| CARTO / Stadia / MapTiler / Thunderforest / Esri | **cần khoá / tài khoản** | — | loại |

## 4. Phương án (chi tiết + "khi nào sai" ở file private §4)

- **P1 — khuyến nghị cho đợt 2:**
  - dữ liệu kho + Leaflet / tile OSM;
  - ghim 33 điểm lịch trình (bổ sung toạ độ 15 điểm thiếu từ OSM, xem bằng mắt);
  - ăn uống / lưu trú qua thẻ kho + link Google Maps do code dựng (như E5);
  - sự kiện theo tháng từ kho;
  - CSP thêm 1 domain ảnh.
- **P2:** như P1 nhưng MapLibre + PMTiles tự host. 0 domain ngoài, cần WebGL, phải đo dung lượng.
- **P3:** thêm 208 lưu trú + 697 ăn uống từ OSM. Nhiều điểm, nhưng trường không đều, lệch closed-world (phải nhãn "chưa kiểm"), ODbL.
- Cần A / User quyết: P1 / P2 / P3; có cần trang lưu trú dạng danh sách cơ sở không (chỉ P3 hoặc nhập tay mới có).

## 5. Lỗi và giới hạn

- **Overpass quá tải:** 3 / 5 lượt 502 ⇒ chưa có danh sách tên OSM để khớp toạ độ 15 điểm thiếu. Lấy lại khi cần, một lần, ngoài giờ cao điểm.
- **NOT RUN / chưa đo:**
  - dung lượng PMTiles vùng Huế;
  - cỡ gói Leaflet / MapLibre trong bản build Vite;
  - CSP `style-src 'self'` với thư viện bản đồ (phải thử trên bản build do FastAPI phục vụ);
  - danh sách host glyph / sprite trong style OpenFreeMap.
- Các ý [Codex] chưa tự mở lại: trang sự kiện visithue, bài 21 cơ sở 4–5 sao, chính sách riêng tư OpenFreeMap, ngưỡng Overpass.
- Đếm kho bằng mẫu regex ⇒ số **gần đúng**: "có giá" bắt cả giá món; "có ngày" bắt cả ngày lịch sử.

## 6. Bàn giao

- Không sửa code / kho; **0 USD** (Codex dùng gói ChatGPT).
- File: `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md`, `…/c209/` (công cụ + thô + yêu cầu tra web), `data/tra_cuu_cli/2026-11-06_c209-ban-do-nguon/`, report này.
