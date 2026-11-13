# Review: kho 3 — phần ăn uống của C (khớp quán OpenStreetMap bản 2 + bảng quán theo cụm bản 2)

> Sửa 13/11 (E): bỏ tên quán + địa chỉ lấy từ kho (repo public) — thay bằng nhãn Q-a … Q-e; bản đầy đủ ở `data/osm_quan_2026-11-12/doc_tay_v2.json`. Kết luận không đổi.

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 3 minor). Phiếu quán + mốc bản 2 đưa User xem được sau khi sửa m-1, hoặc đưa ngay kèm ghi chú m-1.
Người kiểm: E (Claude Code, `hue-rag-e8`), A giao 13/11
Date: 20:00 13/11/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` §3 (c) (E giữ spec)
Implementation report: `session_prompt/sessions/STATUS_C.md` mục "PHIÊN 13/11" + `data/osm_quan_2026-11-12/bien_ban.md` mục "Phiên 13/11"

## 1. Phạm vi đã review
- Đọc: STATUS_C mục 13/11; biên bản mục "Phiên 13/11"; `doc_tay_v2.json` (13 nhận · 9 bỏ); `quan_theo_cum.json`; dòng định vị của phiếu và bài nháp cho các quán đọc tay.
- Chạy lại hai script (mục 3); đọc tay 5 dòng nhận + 3 dòng bỏ, đối chiếu với **địa chỉ trong bài kho** (qua `scripts/grep_kb.sh --dir foods`), **bản ghi OSM** (`osm_quan.json`) và **đoạn đường OSM có tên** (`data/luu_tru_2026-11-12/osm/duong_co_ten_hue.json`, nguồn độc lập với cách C kiểm).
- Không chạm kho; không gọi mạng; 0 USD.

## 2. Findings

**m-1 (minor) — quán Q-a (một quán cơm hến): căn cứ vị trí yếu nhưng vẫn in số mét.** `quan_theo_cum.json` ghi `muc_toa_do: "osm"` ⇒ câu định vị có số km tới một mốc (phiếu dòng 122 + bài nháp). Ghi chú đọc tay của chính C: "đúng đường, chưa chắc số nhà". Bằng chứng: điểm OSM không có tên đường; quán OSM cùng đường gần nhất cách 490 m; tâm đoạn đường của bài gần nhất cách 300 m (E đo); địa chỉ bài nằm trong một kiệt. Tác động: sai số có thể tới vài trăm mét, so với con số 0,9 km được in ra. Spec §3 (c): mức "ước" thì không in số mét. **Đóng khi:** hạ dòng này xuống mức không in mét ("thuộc khu <cụm>, gần <mốc>") hoặc ghi lý do giữ trong phiếu.

**m-2 (minor) — Giá trị `muc_toa_do: "osm"` nằm ngoài ba mức của spec.** Spec §3 (c) chỉ định nghĩa `chac` / `vua` / `uoc`; bảng hiện có `osm` 22 dòng (12 quán kho + 10 quán nguồn OSM), dòng nào cũng in số mét. Code lịch trình (B đợt 2) đọc trường này sẽ gặp một giá trị lạ. **Đóng khi:** tách thành hai trường — `nguon_toa_do: "osm"` và `muc_toa_do` theo ba mức (trùng tên + số nhà ⇒ `vua` hoặc `chac`; không có tên đường ⇒ `vua`, hoặc `uoc` như m-1) — **hoặc** A ghi thêm mức `osm` vào spec (E giữ spec, sửa được một dòng nếu A đồng ý).

**m-3 (minor) — quán Q-b: số trong địa chỉ bài là số kiệt, OSM ghi thành số nhà.** Bài kho ghi địa chỉ trong kiệt; OSM ghi cùng con số là số nhà. Ghi chú đọc tay viết "= số nhà bài". Vị trí vẫn hợp lý: tâm đoạn đường của bài cách 57 m, đầu kiệt sát số nhà 21. Chỉ cần sửa chữ trong `doc_tay_v2.json` / phiếu, không đổi toạ độ.

Ghi nhận (không phải finding): C tự báo đã `grep` thẳng 3 bài quán, sai luật §5 (không chạm câu kín / Golden). E kiểm lại bằng `grep_kb.sh` — địa chỉ khớp.

Không có blocker / major. Không thấy chỗ over-engineer: bản 2 siết luật đúng chỗ (bản 1 sai 6 / 22 ≈ 27 %), đọc tay toàn bộ 22 dòng, bỏ dòng mơ hồ.

## 3. Cách người kiểm chạy lại thật
Sao 4 file ra trước vào `/tmp/e_rv_c/goc/` (hai script ghi đè đường dẫn cố định), chạy:
`uv run python data/osm_quan_2026-11-12/tools/khop_osm_v2.py` rồi `uv run python data/sua_kho_2026-11-12_an_gan/tools/dung_quan_theo_cum.py "$(date '+%H:%M %d/%m/%Y')"`,
so `diff`, rồi chép lại bản của C (md5 sau khi chép lại: `quan_theo_cum.json` `2c96ac42e946` · phiếu `ce7264f07c17` — đúng mã C báo).

## 4. Kết quả quan sát
- **Tái lập:** `khop_bai_kho_v2.json` và bài nháp **giống byte**; `quan_theo_cum.json` và phiếu chỉ khác dòng giờ dựng.
- **Số khớp với C:** bảng khớp 13 dòng (chắc 1 · vừa 12) · bài kho có toạ độ **34** (13 từ OSM đọc tay), trong đó **28** gán được cụm (6 xa / sát ranh) · cụm 0 quán **2 / 8** (lăng xa, nam xa; cụm biển 1 quán) · mốc cầu ngói Thanh Toàn 0 quán · tiêu đề dài nhất 48 ký tự, đoạn dài nhất 528 ký tự. Số 81 (tổng bài quán) không đếm lại — lấy từ bản 1.
- **Đọc tay 5 dòng nhận:**

| Quán | Dạng địa chỉ trong bài kho | OSM | E kiểm độc lập | Kết luận |
|---|---|---|---|---|
| Q-c (quán cà phê bến thuyền) | số nhà + đường | trùng tên, không đường | tâm đoạn đường của bài gần nhất 285 m (đường dài); C: quán OSM cùng đường 119 m | nhận được |
| Q-b | trong kiệt | trùng tên, cùng đường, cùng con số (OSM có thêm một quán trùng tên ở đường khác — C chọn đúng) | đoạn đường của bài 57 m | nhận được (m-3) |
| Q-a | trong kiệt | trùng tên, không đường, có giờ mở | tâm đoạn đường của bài gần nhất 300 m | nhận cụm được; **không nên in mét** (m-1) |
| Q-d (nhà hàng chay) | số nhà + đường | tên chung, không đường | đoạn đường của bài 97 m; C: quán OSM cùng đường 37 m | nhận được (tên chung, nhưng vị trí khớp) |
| Q-e (quán cà phê trong kiệt) | trong kiệt | trùng tên + số nhà + kiệt | — | nhận đúng |

- **Đọc tay 3 dòng bỏ:** một quán chay — kho ghi một phường khác, hai điểm OSM cùng tên ở khu khác ⇒ bỏ đúng · một tiệm bánh — bài có nhiều cơ sở ⇒ bỏ đúng · một quán bánh canh — OSM khác số nhà, bài đã có toạ độ "chắc" ⇒ giữ cũ đúng.

## 5. Giới hạn hoặc phần chưa chạy
Không kiểm 10 quán nguồn OSM được chọn cho cụm thiếu (C đã đọc tay, loại 2) và 8 dòng nhận còn lại. Không kiểm vị trí ngoài đời (không có nguồn thứ ba). Chưa đọc toàn văn bài nháp — chỉ xem dòng của các quán đã đọc tay.

## 6. Decision và bước tiếp theo
`ready_for_user_confirmation`: C sửa m-1 (một dòng), chọn cách đóng m-2 cùng A, sửa chữ m-3 ⇒ đưa User phiếu quán + mốc bản 2. Việc đưa quán OSM vào kho vẫn chờ User (câu 5 / mở rộng Q3). A đóng.
