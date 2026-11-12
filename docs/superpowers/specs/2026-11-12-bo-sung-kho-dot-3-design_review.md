# Review: spec "Đợt bổ sung kho 3 — lưu trú · đi lại · ăn gần" (nháp bản 1) — vòng 1

Decision: **changes_requested** (0 blocker, 3 major, 7 minor) — sửa chữ + hai phép đếm / thử 0 USD là đủ; vòng 2 chỉ xem ba chỗ major
Người kiểm: C (`hue-rag-e1`, Claude Code — Fable 5.2)
Date: 21:25 12/11/2026 (`date`)
Bản được review: `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` sha256 `14387f19f5b0` (người viết: E)
Căn cứ: các mục spec ghi ở "Căn cứ để review" + `backend/config/settings.yaml` (khối `include_globs`), `backend/ingestion/source_state.py`, `backend/ingestion/chunking/markdown_blocks.py`,
`backend/llm/assistant.py` (`NOTICE_SOURCE_PREFIXES`), dữ liệu của C `data/sua_kho_2026-11-12_an_gan/`.

## 1. Phạm vi đã review

Đọc hết spec. Đối chiếu (chỉ đọc, 0 USD) với cấu hình quét kho, luật chia đoạn, bảng quán + mật độ quanh điểm do C dựng, 6 + 6 + 6 câu của hai lượt đếm 12/11. **Không** mở `data/luu_tru_2026-11-12/`
(số trong Q2 lấy theo spec), không chạy chunker, không đọc STATUS của E.

## 2. Findings

### M-1 (major) — thư mục mới `travel/lodging/` không nằm trong danh sách quét kho ⇒ bài lưu trú sẽ **không vào chỉ mục** mà build vẫn "thành công"
- **Vị trí:** spec §3 (a) "Dạng bài (`travel/lodging/`, thư mục mới)"; §1 "Không đổi: chunker, model, lời dặn…"; §8 "Quyền".
- **Bằng chứng:** `backend/config/settings.yaml` khối `include_globs` chỉ liệt kê `foods/**`, `heritages/**`, `festivals/**`, `performing_arts/**`, `travel/places/**`, `travel/services/**`,
  `travel/tickets/**`; `source_state.py` chỉ duyệt đúng các mẫu đó. `travel/lodging/**` không khớp mẫu nào.
- **Tác động:** dựng lại xong không lỗi, số đoạn không tăng phần lưu trú, K4 trượt — hoặc tệ hơn, K4 "đạt" nhờ mục web / bài cũ mà không ai thấy bài mới không được nạp. Đây còn là **sửa file cấu hình
  trong `backend/`** (ngoài phạm vi "không đổi" của §1), kéo theo test khoá cấu hình và danh sách chừa của bản Docker (bài học 10/11: thiếu một file cấu hình ⇒ tính năng tắt im lặng).
- **Tiêu chí đóng:** chọn và ghi rõ một trong hai: (i) đặt bài ở thư mục **đã được quét** (vd `travel/services/`) — không đổi cấu hình; hay (ii) thêm mẫu `travel/lodging/**/*.md` vào `settings.yaml`
  (ghi vào §3, §8 quyền, bước 4, và bước kiểm sau build). Dù chọn gì, **bước 6 thêm một phép đếm bắt buộc:** số đoạn có `source` thuộc thư mục bài lưu trú trong chỉ mục = số đoạn chia thử ở bước 4 (≠ 0).

### M-2 (major) — dạng "mỗi cơ sở một dòng ⇒ mỗi dòng một đoạn" chưa được thử, và nhiều khả năng **không trả lời được câu hỏi dạng danh sách** — đúng loại câu đã đếm lỗi
- **Vị trí:** §3 (a) "Luật chia đoạn"; §6 K4.
- **Bằng chứng / lập luận:** (1) Khẳng định về hành vi chunker ("cắt mỗi dòng một đoạn mang tên bài + tên mục") là suy từ code, **chưa chạy** — `markdown_blocks.py` có tách `list_item`, nhưng đoạn có
  gộp nhiều mục ngắn hay không tuỳ `full_corpus_chunker.py`. Luật dự án: khẳng định hành vi ⇒ probe nhỏ trước khi bàn giao. (2) Nếu đúng là mỗi cơ sở một đoạn: ngữ cảnh chỉ nhận **10 đoạn**. Câu
  "Huế có những khách sạn 5 sao nào" cần 11 đoạn nằm ở nhiều bài khu khác nhau, mỗi đoạn chỉ là "tên — hạng — địa chỉ" ⇒ tầng tìm phải kéo đúng cả 11 dòng vào 10 chỗ; câu "khách sạn gần <điểm>"
  cần biết cơ sở nào ở khu nào — thông tin đó nằm ở tiêu đề mục, không ở chữ của dòng. Trong 4 câu cơ sở cụ thể đã đếm có 1 câu hạng sao + 2 câu gần một điểm ⇒ K4 "≥ 3 / 4" dễ trượt vì **dạng bài**,
  không vì thiếu dữ liệu.
- **Tiêu chí đóng:** (a) chạy chunker **chỉ đọc** trên một bài mẫu 20–30 dòng (0 USD, trước khi User duyệt): ghi số đoạn, chữ mỗi đoạn mang gì (có tên khu / hạng không). (b) Sửa dạng bài để **một đoạn
  trả lời được một câu danh sách**: mỗi khu × hạng (hoặc khu × loại) là **một đoạn văn / một mục liệt kê gộp** ("Khách sạn 5 sao ở <khu>: A; B; C…"), và thêm một mục tổng "theo hạng" cho 4–5 sao
  (24 cơ sở — vừa một đoạn). Kiểm lại "mỗi đoạn vừa 3 tokenizer". (c) K4 tách hai dòng: câu **danh sách theo hạng / khu** (kho trả lời, đủ ≥ một nửa số cơ sở đúng, 0 cơ sở ngoài bài) và câu
  **gần một điểm** (trả lời bằng khu của điểm đó + cơ sở trong khu). Câu hỏi "giá rẻ" trong bộ 4 câu: ghi trước kết cục mong muốn (nêu cơ sở theo hạng thấp, **không** nói giá) để người chấm không phải tự chốt.

### M-3 (major) — K6 và bài "ăn gì quanh điểm tham quan" dựa trên dữ liệu chưa đủ và một câu không có nguồn
- **Vị trí:** §3 (c), Q3, Q4, §6 K6.
- **Bằng chứng (dữ liệu của C, `mat_do_quanh_diem.json`, `bang_de_xuat.jsonl`):** theo Q4 (a) chỉ **7** bài quán được ghi câu định vị; 22 bài toạ độ ước không được ghi khoảng cách. Quán có toạ độ
  (kể cả ước) dồn ở bờ nam: quanh hai phố đi bộ + phố Tây 11–13 quán, cung An Định 8, chợ Đông Ba 4, **Đại Nội 1**, chùa và các lăng **0**. ⇒ Bài tổng hợp "lập từ chính bảng khoảng cách" với Q4 (a)
  sẽ gần như chỉ có vài mục bờ nam; phần còn lại là câu "không có quán". Spec chưa nói bài tổng hợp có được dùng 22 toạ độ ước ở mức **"cùng khu"** (không ghi mét) hay không — đây là chỗ quyết
  K6 đạt hay trượt.
- **Câu không nguồn:** mẫu "khách thường ăn ở <khu> trước hoặc sau khi tham quan" là nhận định về thói quen, **không có trong dữ liệu nào** ⇒ trái luật curated (mỗi ý có nguồn). Dữ kiện có thật
  là: "trong kho chưa có quán nào trong bán kính 1 km quanh <điểm>; khu gần nhất có quán trong kho là <khu>, cách khoảng <x> km".
- **Điểm mốc thiếu:** một trong 6 câu ăn gần đã đếm hỏi quanh **một cây cầu** — không phải điểm trong bảng 28 điểm ⇒ bảng khoảng cách không có dòng cho nó; tương tự ga, bến thuyền. K6 dùng lại
  6 câu này nên sẽ mất sẵn 1 câu.
- **Việc đang chạy chưa được nhắc:** A đã giao E tra toạ độ quán bằng nguồn khác (sau khi tra OpenStreetMap từ máy C không gửi được) ⇒ con số 7 / 29 có thể đổi; spec nên ghi Q4 chốt **sau** lượt tra đó.
- **Tiêu chí đóng:** (1) ghi rõ luật của bài tổng hợp: toạ độ chắc ⇒ được ghi khoảng cách; toạ độ ước ⇒ chỉ được xếp vào mục "cùng khu với <điểm>" khi cách ≤ 1 km **trừ sai số** (vd ≤ 0,5 km
  sau khi trừ 522 m), không ghi mét; (2) thay câu "khách thường ăn ở…" bằng câu dữ kiện; (3) thêm 3–5 **điểm mốc không phải điểm tham quan** (cầu, ga, bến) vào bảng mốc, toạ độ theo phiếu User
  duyệt; (4) chạy thử 0 USD: với luật đã ghi, mỗi mục của bài tổng hợp có bao nhiêu quán ⇒ ước K6 đạt được bao nhiêu / 12 **trước** khi chốt ngưỡng 7 / 12.

### Minor (không chặn)
- **m-1 — Q2 con số không khớp định nghĩa.** Phương án (a) viết "bản ghi cơ quan nhà nước nhập + có hạng hoặc loại rõ" nhưng 151 = số cơ sở **có hạng sao hoặc "đạt chuẩn"** bất kể ai nhập;
  116 / 316 bản ghi "chưa đọc được nhãn" nguồn nhập. Sửa bộ đọc nhãn rồi ghi lại hai số (theo người nhập · theo hạng) trước khi A hỏi User.
- **m-2 — gán khu từ phường / xã:** tên phường đã đổi sau sắp xếp đơn vị hành chính, một phường mới rất rộng ⇒ "lõi đô thị / phía tây / ven biển" suy từ phường có thể thô. Thêm một phép đếm ở
  bước 1: bao nhiêu / 316 cơ sở gán được khu, nhóm "khác" bao nhiêu; nhóm "khác" > ~20 % ⇒ báo A trước khi soạn.
- **m-3 — K3 chỉ đếm đoạn lưu trú chen vào.** Thêm ~300 đoạn + dựng lại bảng từ khoá làm đổi trọng số của cả kho ⇒ ghi thêm số theo dõi: bao nhiêu / 158 câu đổi 10 đoạn đầu **mà không do đoạn mới**
  (không vào luật, để giải thích nếu K1 dao động).
- **m-4 — dòng nhắc "có thể đã thay đổi":** spec nói thêm thư mục lưu trú vào danh sách kích dòng nhắc "nằm trong plan lưu trú"; plan đó là thẻ khu + link, không phải bài kho ⇒ ghi việc này vào
  **spec này** (một dòng code + test), kèm ngoại lệ ở §1 "không đổi".
- **m-5 — "homestay":** nguồn có 0 homestay; một trong 4 câu cơ sở cụ thể đã đếm hỏi đúng loại đó ⇒ ghi trước kết cục mong muốn (nói thật "danh mục chủ yếu là khách sạn" + khu + thẻ link), để K4
  không tính nhầm là trượt / đạt.
- **m-6 — thứ tự với các việc khác:** bộ "trước" dùng lại từ B7 chỉ đúng khi `backend/` không đổi; từ giờ tới lúc làm có ít nhất 3 nhánh chạm đường trả lời (hết lượt tìm, đổi nguồn tra web, thẻ
  lưu trú) ⇒ ghi thẳng "chạy lại bộ trước trên commit làm việc" và cộng ≈ 0,08 USD vào tiền (0,16 ⇒ ≈ 0,24, sát trần 0,25 ⇒ nâng trần hoặc bỏ lượt Golden "trước" bằng cách làm đợt này **ngay sau**
  một lượt Golden khác).
- **m-7 — người viết 6 + 6 + 6 câu mới:** ghi tên người viết (không phải E) và mốc "viết xong trước bước 1" để bài soạn không bị viết theo câu.

### Điểm đạt (ghi để khỏi sửa)
Mức rủi ro đặt đúng (cao) và đi đúng khuôn sửa kho (sao lưu, chia đoạn thử, xoá đủ ba đích, tự lùi, nhãn v6); không giá phòng / liên hệ / link đặt phòng; bài sinh bằng script từ bảng sạch;
lùi theo phần; rà đường dữ liệu ngoài có xét chữ lạ trong tên cơ sở; nói thật giới hạn nguồn (0 homestay; quanh lăng không có quán); không bộ kín (đợt dữ liệu); K7 kho sạch; lời khuyên đi lại
nằm trong kho có nguồn, không giá cứng.

## 3. Cách người kiểm chạy lại thật (0 USD)

`sed` khối `include_globs` của `backend/config/settings.yaml`; `grep` `include_globs` trong `source_state.py`, `list_item` trong `markdown_blocks.py`, `NOTICE_SOURCE_PREFIXES` trong `assistant.py`;
đọc `data/sua_kho_2026-11-12_an_gan/mat_do_quanh_diem.json` + `bang_de_xuat.md` (số quán theo điểm, mức khớp).

## 4. Kết quả quan sát

| Khẳng định của spec | Quan sát | Kết quả |
|---|---|---|
| "Không đổi: chunker, model, lời dặn…" + thư mục mới `travel/lodging/` | thư mục mới không khớp mẫu quét nào | **lệch — M-1** |
| "chunker hiện tại cắt mỗi dòng một đoạn" | code có tách mục danh sách; chưa ai chạy thử | chưa chứng minh — M-2 |
| Kho 1 quán có toạ độ quanh Đại Nội, 0 quanh chùa và lăng; dữ liệu mở 276 / 174 / 0 | khớp file của C | đúng |
| 22 / 29 toạ độ là ước, sai số trung vị 107 m, 95 % ≤ 522 m | khớp `do_sai_so_uoc.json` | đúng |
| Dòng nhắc "có thể đã đổi" theo thư mục nguồn | `NOTICE_SOURCE_PREFIXES` = vé, điểm tham quan, lễ hội — chưa có lưu trú | đúng, cần một dòng code (m-4) |

## 5. Giới hạn hoặc phần chưa chạy

Không chạy chunker, không mở dữ liệu lưu trú đã tải, không kiểm nguồn của bài đi lại (chưa soạn), không kiểm ước giờ.

## 6. Decision và bước tiếp theo

**changes_requested.** E sửa M-1, M-2, M-3 (kèm hai phép thử 0 USD: chunker trên bài mẫu · số quán mỗi mục của bài tổng hợp) thành bản 2; C xem lại riêng ba chỗ major (vòng cuối). Sau đó A hỏi
User Q1–Q5 — nên hỏi **sau** khi có kết quả tra toạ độ quán bổ sung, vì nó đổi số của Q3 / Q4.

## Vòng 2 (vòng cuối) — 21:35 12/11/2026 — bản 2 sha256 `fd152810627b`

Decision: **ready_for_user_confirmation** (3 major đóng; 1 ghi chú nên sửa chữ trước khi A trình User, không cần review lại)

| Finding vòng 1 | Bản 2 | Kết quả |
|---|---|---|
| M-1 thư mục mới không được quét | bài lưu trú đặt trong thư mục đã quét (`travel/services/`), không sửa cấu hình; bước 6 đếm "số đoạn của mỗi file mới trong chỉ mục = số đoạn chia thử, ≠ 0" | **đóng** |
| M-2 dạng bài chưa thử | E đã chạy thử bộ chia đoạn (chỉ đọc): danh sách ⇒ mỗi dòng một đoạn (kém cho câu danh sách); đoạn văn 8 cơ sở vừa, 14 cơ sở lỗi ⇒ chọn đoạn văn ≤ 6 cơ sở + bài tổng theo hạng; K4 tách a / b / c với kết cục ghi trước cho câu giá rẻ và homestay | **đóng** |
| M-3 dữ liệu ăn gần + câu không nguồn | toạ độ ước chỉ dùng mức "cùng cụm" (trừ sai số, sát ranh không gán), không ghi mét; thêm 3–5 mốc; câu nhận định thay bằng dữ kiện; chạy thử số quán mỗi mục trước khi chốt K6; Q3 / Q4 chốt sau lượt tra toạ độ bổ sung | **đóng** |
| Minor m-1…m-7 | đếm lại nhãn nguồn nhập; gán cụm bằng ước toạ độ (địa chỉ danh mục gần như không có phường) + bước đếm tỉ lệ gán; dòng code dòng nhắc; bộ "trước" chạy lại, tiền 0,26 / trần 0,35 | nhận |

**Ghi chú (sửa chữ, không chặn):** bước 6 ghi "số câu đổi 10 đoạn đầu **không** do đoạn mới phải bằng 0 — khác 0 ⇒ dừng". Ngưỡng này **quá chặt và sẽ dừng nhầm**: thêm vài trăm đoạn + dựng lại bảng từ khoá
làm đổi trọng số từ của **cả kho**, nên thứ hạng ở vài câu có thể xê dịch dù không đoạn mới nào chen vào (đợt 05/11 chỉ sửa 11 bài mà 10 / 158 câu đã đổi 10 đoạn đầu). Đề nghị: số này là **theo dõi**
(ghi vào report); điều kiện dừng giữ ở K3 — "0 câu mất đoạn đúng theo nhãn v6" — và K1.

**Điều C cần từ spec này cho spec biểu mẫu bản 3 (đã khớp):** tên trường của `quan_theo_cum.json` và `luu_tru_theo_cum.json`; tên cụm = tên cụm của bảng điểm; quán nguồn dữ liệu mở mang nhãn "chưa kiểm";
buổi tối không thêm kho (thuộc bảng điểm). Còn một chỗ hai spec cùng cần mà **chưa ai giữ**: bảng ánh xạ **cụm (8) ⇒ khu nên ở (3)** cho khối "Ở đâu" — đề nghị đặt trong bảng khu của plan lưu trú.

Bước tiếp: A hỏi User Q1–Q5 (Q3 / Q4 sau khi có kết quả tra toạ độ bổ sung).
