# Huegov Culture and Tourism — Markdown Source Dumps

- Source: data.hue.gov.vn
- Source group: huegov_culture_and_tourism
- Conversion type: source dump
- Enrichment status: not enriched
- Generated at: 2026-08-05T12:51:00.172557+00:00

Converted 21 raw files (9 JSON, 9 XLSX, 3 RDF) from `backend/data/huegov_culture_and_tourism/raw` into Markdown source dumps. One Markdown file per raw file, no enrichment applied.

## Converted Files

| Markdown file | Source format | Detected structure | Notes |
|---|---|---|---|
| am_nhac_tuong_1744277620.md | xlsx | Sheet1: 8 data rows |  |
| ban_nha_nhac_1744278156.md | json | list, 33 records |  |
| chua-diem-phung-cong-vien-thuy-tu-jpegjpg.md | rdf | 11 parsed fields |  |
| danh-sach-di-san-van-hoa-tinh-thua-thien-hue-1_1726311603.md | json | data: 50, hienthi: 10 | duplicate with department |
| danh-sach-dia-diem-di-tich-van-hoa-tinh-thua-thien-hue_1726311601.md | json | data: 180, hienthi: 19 | duplicate with department |
| danh-sach-le-hoi-tren-dia-ban-tinh-thua-thien-hue_1726311601.md | json | data: 138, hienthi: 18 | duplicate with department |
| dao_cu_san_khau_1744277648.md | xlsx | Sheet1: 21 data rows |  |
| diem-den-sinh-thai-van-hoa-dac-sac-1.md | rdf | 7 parsed fields |  |
| du-lieu-ve-gia-ve-tham-quan-di-tich-cua-trung-tam-bao-ton-di-tich-co-do-hue-1_1785085393.md | json | list, 22 records |  |
| du-lieu-ve-luot-khach-tham-quan-cac-diem-di-tich-cua-trung-tam-bao-ton-di-tich-co-do-hue-2_1785207796-1.md | json | chart: 13, grid: 52 |  |
| hat_tuong_1744277688.md | xlsx | Sheet1: 17 data rows |  |
| kich_ban_tuong_1744277711.md | xlsx | Sheet1: 56 data rows |  |
| lang-du-lich-cong-dong-hoa-giay-thanh-tien-1-jpegjpg.md | rdf | 10 parsed fields |  |
| mat_na_tuong_1744277740.md | xlsx | Sheet1: 100 data rows |  |
| nghe_nhan_nha_nhac_1744278182.md | json | list, 12 records |  |
| nhac_chuong_nha_nhac_1744278211.md | json | list, 0 records | empty dataset |
| nhac_cu_nha_nhac_1744278236.md | json | list, 18 records |  |
| phuc_trang_tuong_1744277759.md | xlsx | Sheet1: 29 data rows |  |
| trich_doan_tuong_1744277783.md | xlsx | Sheet1: 21 data rows |  |
| tu_ngu_nghe_thuat_tuong_1744277802.md | xlsx | Sheet1: 695 data rows |  |
| vu_dao_tuong_1744277823.md | xlsx | Sheet1: 86 data rows |  |

## Notes
- No enrichment applied: content kept as-is from raw files; only light text transformations (strip HTML, decode HTML entities, collapse whitespace).
- Empty datasets (Markdown generated with "No records found."):
  - Nhac_Chuong_Nha_Nhac_1744278211.json
- Duplicates with the department source dumps (identical content, md5 match; converted anyway):
  - Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json == `huegov_department_of_tourism/raw/Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603 (1).json`
  - Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json == `huegov_department_of_tourism/raw/Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601 (1).json`
  - Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json == `huegov_department_of_tourism/raw/Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601 (1).json`
