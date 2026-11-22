# Cập nhật riêng phần chỉ mục của bài đã sửa — report của phiên C (viết 08:49 22/11/2026)

Việc: hàng [7] của sổ việc, nửa "sau khi duyệt chỉ tính lại vector cho bài đã sửa" (chủ dự án chọn 22:22 và nhắc lại 22:45 21/11/2026). Người đọc
nhánh: phiên E (viết phép kiểm độc lập). Nhánh `p12-c-cap-nhat-rieng`: `backend/ingestion/cap_nhat_rieng.py` (mới), `backend/tests/test_cap_nhat_rieng.py`
(mới), runbook mục 5b, report này. Không sửa file dựng / tìm đang có; server không đổi dòng nào.

**Từ dùng:** *chỉ mục* = collection Qdrant, mỗi đoạn của kho là một *điểm* gồm chữ của đoạn (payload), *vector nghĩa* (model e5-small tính — phần tốn
thời gian) và *vector từ khoá* (code tính từ thống kê cả kho, không cần model) · *file thống kê từ khoá*, *bản ghi dựng*: hai file ở
`data/full_corpus_builds/` server đọc lúc khởi động · *dựng lại toàn bộ*: cách cũ, xoá collection rồi tính lại mọi vector.

## 1. Người dùng (chủ dự án) làm được gì / chưa làm được gì

| | |
|---|---|
| Làm được | Sau khi một bài trong kho đổi, gõ MỘT lệnh (không phải gõ tên bài) ⇒ chỉ mục khớp kho trong khoảng 25–28 giây thay cho khoảng 225 giây dựng lại toàn bộ; `--chi-xem` để xem trước bài nào khác chỉ mục |
| Làm được | Lệnh chết giữa chừng ⇒ server từ chối khởi động chứ không trả lời lệch; chạy lại lệnh là xong. Lùi một lần sửa: `git revert` bài rồi chạy lại chính lệnh đó |
| CHƯA làm được | Chạy trên chỉ mục THẬT — mới chạy trên bản chép (collection thử + kho chép); lần chạy thật đầu chờ phép kiểm của E + phiên điều phối |
| CHƯA làm được | Cập nhật khi server đang chạy mà không khởi động lại (không làm — phiên điều phối đồng ý) |

## 2. Vì sao chọn "sửa tại chỗ, so từng đoạn" (số đo 08:27 22/11/2026, 0 đồng)

| Bước | Giây |
|---|---|
| Chia đoạn cả kho + thống kê từ khoá (hướng nào cũng phải làm) | 21,1 |
| Ghi lại riêng vector từ khoá của cả 9.436 điểm (hướng sửa tại chỗ) | 1,8 |
| Ghi 9.436 điểm sang collection mới (hướng "dựng sang collection mới rồi chuyển") | 4,2 |
| Tính vector nghĩa cả kho (256 đoạn = 5,3 giây ⇒ ước) | 195 |

Hai hướng cùng bỏ được 195 giây và chỉ chênh nhau khoảng 3 giây ⇒ thời gian không phân xử. Hướng chuyển collection phải sửa tên collection đang ghi
cứng ở code dựng, hai chỗ server đọc, tách file thống kê theo collection, 5 file test, script mở ngày, lệnh kiểm runbook và các bài `bai_hoc/`; hướng sửa
tại chỗ không đụng server và đúng chữ chủ dự án ("nạp lại vào collection"). Thứ hướng kia hơn — bản cũ còn nguyên — được bù bằng bản chụp Qdrant trước
mỗi lần ghi. Thiết kế một trang + góp ý của E, B và phiên điều phối: `data/phase_12_agent_sua_kho_2026-11-21/THIET_KE_CAP_NHAT_RIENG.md` (riêng tư).

Ba điều rút từ code quyết định cách làm:
- Vector từ khoá của MỖI điểm đã nhân sẵn thống kê của cả kho (`embedding/sparse.py`) ⇒ sửa một bài thì phải ghi lại vector từ khoá của mọi điểm mới
  "giống dựng lại"; cách tìm đang chạy (`dense_bm25_rrf`) không đọc vector này (tính lúc hỏi từ payload + file thống kê — E đọc ra), cách tìm thứ hai có đọc.
- Lệnh so payload từng điểm với CHÍNH collection thay vì tin bản ghi dựng ⇒ chạy lại sau khi chết vẫn kéo về đúng; hạt là ĐOẠN (đổi 7 con số giá
  trong một bài ⇒ tính lại 7 đoạn).
- "Đã khớp, không ghi gì" chỉ khi không điểm nào khác VÀ bản ghi dựng + file thống kê đang nói đúng kho này (điểm E nêu khi đọc thiết kế).

## 3. Lượt thật trên bản chép [máy kiểm, phiên C tự soi — chờ phép kiểm độc lập của E]

Qdrant server, collection thử `hue_thu_c_cap_nhat_rieng` (bản chép 9.436 điểm của collection đang chạy), model e5-small thật, kho chép ở `/tmp`.
Script + kết quả từng ca (riêng tư): `data/phase_12_agent_sua_kho_2026-11-21/c_cap_nhat_rieng/` (`chay_thu.py`, `ban_ghi_thu/ket_qua_<ca>.json`).
Sau MỖI ca script tự soi cả collection: 0 payload sai · 0 vector từ khoá sai so với file thống kê mới · 0 điểm giữ nguyên chữ mà đổi vector nghĩa.

| Ca | Việc | Đoạn tính lại | Điểm xoá | Số điểm sau | Giây |
|---|---|---|---|---|---|
| đầu | không sửa gì (lần chạy đầu trên bản chép) | 0 | 0 | 9.436 | 22,9 |
| giá | "200.000" ⇒ "250.000" ở 7 chỗ của bài vé Quần thể Di tích | 7 | 0 | 9.436 | 25,5 |
| bài mới | thêm bài nháp "Leo bậc và đi bộ…" (chỉ ở kho chép) | 36 | 0 | 9.472 | 28,2 |
| rút giữa | bỏ mục thứ hai của `foods/food-guides.md` (các đoạn sau dịch số) | 84 | 8 | 9.464 | 27,2 |
| chết ở bước ghi lại vector từ khoá, rồi chạy lại | đổi một con số trong bài Chi phí du lịch | 0 ở lần chạy lại (1 ở lần chết) | 0 | 9.464 | 25,4 |
| chết ngay trước khi ghi file thống kê, rồi chạy lại | như trên | 0 ở lần chạy lại | 0 | 9.464 | 25,1 |

- Ca đầu: file thống kê lệnh ghi ra GIỐNG TỪNG BYTE file đang chạy; bản ghi dựng giống bản đang chạy (trừ tên collection) ⇒ lệnh và đường dựng ra cùng kết quả trên cùng kho.
- Ca bài mới: cả 9.436 điểm cũ có vector từ khoá khác trước (thêm từ mới, độ dài trung bình đổi) ⇒ bước ghi lại được thử thật; ca giá chỉ 69 điểm đổi.
- Hai ca chết: sau khi chết, bản ghi dựng chỉ còn ở tên `….json.dang_cap_nhat`; lần chạy lại KHÔNG báo "đã khớp" dù payload đã khớp.
- Dịch vụ tìm (`build_full_corpus_retrieval_service`) khởi động được với collection + bản ghi dựng + file thống kê sau sáu ca: 3,4 giây; câu "người đau gối thì điểm nào ít phải leo bậc" ⇒ ba đoạn đầu đều của bài mới.
- Sửa một câu mà file điều kiện đang ghim nguyên văn ⇒ lệnh dừng ở bước chia đoạn, chưa ghi gì (đã thử trên một bản chép khác; kho có 3 luật ở 2 bài).
- Bản chụp Qdrant: 0,2 giây, 63 MB; khôi phục từ bản chụp đã thử: 0,3 giây, đủ 9.436 điểm.

## 4. Lệnh kiểm + đầu ra

| Lệnh (từ `backend/` của cây nhánh, không nạp env) | Đầu ra |
|---|---|
| `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --no-sync python -m pytest tests/test_cap_nhat_rieng.py -q` | `6 passed` |
| `… pytest tests/test_assistant_boundary.py -q` · `… tests/test_full_corpus_qdrant_ingestion.py -q` | `4 passed` · `16 passed` |
| `… python <riêng tư>/c_cap_nhat_rieng/chay_thu.py <ca>` (sáu ca + `tim`) | bảng mục 3; mọi ca "tự soi" 0 / 0 / 0 |

Test của nhánh dùng Qdrant bản trong bộ nhớ của chính thư viện + model embedding thay bằng hàm tất định (để so được từng số với bản dựng lại);
lượt thật là mục 3.

## 5. Chưa làm · tự hoãn

- CHƯA: lần chạy trên chỉ mục thật (chờ E kiểm đạt + bản chụp + phiên điều phối biết) · mục `bai_hoc/` (viết khi lệnh đã chạy thật) · lệnh "duyệt đề xuất" của B gọi `dong_bo()` (nhánh của B).
- TỰ HOÃN: dọn bản chụp cũ (63 MB mỗi lần chạy thật, hiếm chạy — ghi cách xem ở runbook, không tự xoá) · tải bản chụp ra khỏi container (thêm một đường gọi mạng; đường cuối cùng vẫn là dựng lại toàn bộ từ kho trong git) · dùng lại vector nghĩa cho đoạn chỉ đổi payload mà không đổi chữ tìm (một bài dưới 1 giây, không đáng).

Phép này KHÔNG cho biết: chất lượng tìm sau khi sửa kho (đó là T1 / câu an toàn) và hành vi khi server đang chạy · hướng rộng hơn: sau deploy, muốn cập nhật không dừng server thì xét lại hướng chuyển collection · đếm rẻ nhất: phép kiểm của E so với một lần dựng lại toàn bộ từ kho chép (0 đồng, khoảng 4 phút).
