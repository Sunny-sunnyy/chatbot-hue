# Bài 16 — Kiểm nguồn bằng chương trình, và câu từ chối cố định

*Cập nhật 10:30, ngày 22/11/2026 · luật kiểm đọc từ chương trình đang chạy; số đếm lấy từ các báo cáo từ 25/10 tới 21/11, ghi rõ model ở từng số; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** model viết nhận lời dặn, câu hỏi, 10 đoạn, và trả về một ô chữ có các số nguồn [n].
**Bài này thêm:** chương trình làm gì với ô chữ đó trước khi coi lượt hỏi là xong. Hai việc: kiểm số nguồn, và nhận ra câu từ chối.

## Ý chính

- Chương trình kiểm số nguồn theo **ba luật**: câu trả lời phải có ít nhất một số nguồn; mọi số phải là số của một nguồn đã thật sự được đưa cho model (một đoạn của kho, hoặc một nguồn do chương trình dựng như khối dự báo thời tiết); câu từ chối thì không được kèm số nguồn.
- Phạm luật thì câu trả lời **bị rút lại**: người dùng thấy một lời báo và nút "Thử lại", không thấy câu trả lời có nguồn giả.
- Câu từ chối là **một câu cố định, đúng từng chữ**. Nhờ vậy chương trình nhận ra chắc chắn một lượt là từ chối, để mở đường tra web và để đếm khi đo.
- Bước kiểm này mới kiểm **số nguồn có thật**. Nó chưa kiểm đoạn được trích có nói đúng điều câu trả lời viết không.
- Lỗi số nguồn hiếm: 0 trên 489 lần viết của gpt-6-luna ở một lần đếm cuối tháng 10; 0 trên 93 lượt ở một lượt rà ngày 21/11 trên cả hai model.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| kiểm số nguồn | **citation check**, **citation integrity** | kiểm mọi số [n] trong câu trả lời trỏ tới một đoạn có thật |
| rút lại | **retract** | xoá câu trả lời đã hiện và thay bằng lời báo lỗi |
| câu từ chối cố định | **fixed refusal**, **fallback answer** | một câu duy nhất, đúng từng chữ, dùng mỗi khi không đủ bằng chứng |
| điều kiện không được vỡ | — (trong hồ sơ dự án gọi là "sàn") | một điều ghi trước mà mọi thay đổi phải giữ; ở đây: 0 câu ngoài kho được trả lời bằng kho |

## Ba luật kiểm số nguồn

Sau khi model viết xong, chương trình đọc ô chữ và kiểm:

1. **Câu trả lời phải có ít nhất một số nguồn.** Một câu trả lời không có số nào thì không ai biết nó dựa vào đâu.
2. **Mọi số nguồn phải có thật.** Ở ví dụ chính, model được đưa các đoạn số 1 tới 10. Nếu câu trả lời ghi [12] thì đó là một nguồn bịa.
3. **Câu từ chối không được kèm số nguồn.** "Tôi không tìm thấy đủ thông tin… [3]" là một câu tự mâu thuẫn.

Câu trả lời thật của ví dụ chính ghi các số 1, 2, 4, 5, 6. Cả năm đều nằm trong 10 đoạn đã đưa, nên nó qua bước kiểm.

Trên màn hình, người dùng không thấy các số [n] trong chữ. Giao diện bỏ chúng đi và hiện một dòng "Nguồn:" dưới câu trả lời, ghi tên các bài đã được trích; bấm vào một tên là đọc được mảnh chữ gốc trong bài. Số nguồn vẫn có ở tầng chương trình, và bước kiểm chạy trên đó.

Chương trình chấp nhận hai cách ghi: [3] và [Nguồn 3]. Lý do ở mục "Đã so".

## Phạm luật thì câu trả lời bị rút lại

Trong ô chat, chữ của model hiện ra trước, bước kiểm chạy sau (bài 21). Nếu bước kiểm hỏng, giao diện xoá chữ đã hiện, hiện một lời báo bằng tiếng Việt và nút "Thử lại". Lượt đó được ghi trong sổ là "bị rút lại".

Lựa chọn ở đây là: thà người dùng phải bấm lại, còn hơn đọc một câu trả lời mang số nguồn không có thật.

Có một trường hợp chương trình sửa thay vì rút. Đôi khi model viết phần trả lời có số nguồn rồi nối thêm nguyên câu từ chối ở cuối. Theo luật 3 thì cả câu hỏng. Chương trình gỡ câu từ chối ở cuối, giữ phần có nguồn, rồi kiểm phần đó như mọi câu.

## Câu từ chối là một câu cố định, đúng từng chữ

Khi các đoạn được đưa không đủ để trả lời, model phải trả đúng câu này, không thêm bớt:

> Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.

Nếu để model tự viết lời từ chối, mỗi lần nó viết một kiểu, và dễ có kiểu từ chối nửa vời rồi đoán ("mình không chắc, nhưng có thể là…"). Một câu cố định cho ba thứ:

- Chương trình **nhận ra chắc chắn** lượt này là từ chối, bằng cách so chữ. Từ đó nó mở đường tra web (bài 25).
- Khi đo, **đếm được chính xác** bao nhiêu câu bị từ chối, bao nhiêu câu từ chối nhầm, bao nhiêu câu ngoài kho lọt qua (chặng 4).
- Người dùng gặp cùng một thông báo mỗi khi kho không đủ (riêng khi có mục web thì giao diện đổi nó thành câu dẫn sang mục web, như ví dụ ngay dưới).

Ở ví dụ "kho không có" (chỗ đậu ô tô ở chùa Thiên Mụ), model trả đúng câu này. Chương trình nhận ra, tra web một lần, và vì mục web có nội dung nên giao diện thay câu từ chối bằng câu dẫn "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)."

Có một trường hợp chương trình từ chối mà không gọi model: bước tìm không trả về đoạn nào dùng được. Khi đó câu từ chối được đặt ngay, đỡ một lần gọi model.

## Điều bước kiểm này chưa làm được

Chương trình biết [4] trỏ tới một đoạn có thật. Nó chưa biết đoạn 4 có thật sự nói điều câu trả lời viết không. Ở ví dụ chính thì có: đoạn 4 ghi đúng giá vé trẻ em. Nhưng đó là do người đọc đối chiếu, không phải do chương trình kiểm.

Vì vậy "có số nguồn" chưa phải "đã kiểm đúng". Phần nghĩa chỉ được đo khi chấm câu trả lời (bài 19), và với hai loại con số dễ sai nhất (thời tiết, khoảng cách) thì có thêm một bước kiểm con số riêng (bài 24).

## Dễ nhầm

- **"Có số nguồn là đã đúng."** Không. Số nguồn có thật chỉ cho biết đoạn đó tồn tại và đã được đưa cho model.
- **"Câu từ chối là do model tự nghĩ ra lời."** Không. Đó là một câu cố định ghi trong lời dặn; chương trình so đúng từng chữ.
- **"Kiểm xong mới hiện."** Trong ô chat thì chữ hiện trước, kiểm sau; hỏng thì rút lại.

## Những điều cần nhớ

- Ba luật: có ít nhất một số nguồn · mọi số có thật · câu từ chối không kèm số nguồn.
- Phạm luật thì câu trả lời bị rút lại, người dùng thấy lời báo và nút "Thử lại".
- Câu từ chối cố định giúp chương trình nhận ra lượt từ chối (để tra web) và giúp phép đo đếm đúng.
- Một điều kiện không được vỡ của sản phẩm: 0 câu ngoài kho được trả lời bằng kho.
- Chưa kiểm nghĩa: đoạn được trích có nói đúng điều câu trả lời viết hay không thì chương trình chưa biết.

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Dạng số nguồn được nhận | [n] và [Nguồn n], không phân biệt hoa thường; đưa hết về [n] khi hiện | model đôi khi chép nguyên nhãn của ngữ cảnh | đã đo trước và sau khi nhận cả hai dạng (mục "Đã so") |
| Câu từ chối khi kho không đủ | "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." | chương trình so đúng từng chữ | chưa thử câu khác |
| Câu cho câu hỏi ngoài phạm vi | "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" | do bước xếp loại câu quyết định, không qua model viết (bài 22) | — |
| Các câu được tính là từ chối khi đo | hai câu trên, cộng ba câu "mình không làm thay được" (đặt chỗ, gửi tin, xem tình trạng phòng; bài 23) | thiếu một câu trong danh sách này thì một câu ngoài kho bị thay chữ sẽ bị đếm nhầm là "được trả lời" | — |
| Khi bước tìm không ra đoạn nào dùng được | đặt câu từ chối ngay, không gọi model | đỡ một lần gọi model | — |
| Câu từ chối nối ở cuối một câu trả lời có nguồn | gỡ câu từ chối, giữ phần có nguồn | trước khi có việc này, cả câu bị rút lại | có từ 21/11 |
| Dòng "có thể đã thay đổi" | nối khi câu trả lời trích bài thuộc nhóm vé, địa điểm, lễ hội, hoặc bài lưu trú | giá và giờ có thể đổi mà kho chưa sửa | — |
| Nguồn hiện dưới câu trả lời | chỉ các đoạn có số được nhắc trong câu trả lời | — | — |

## Đã so

### Nhận cả hai cách ghi số nguồn

**Vấn đề thật đã gặp.** Ngữ cảnh ghi nhãn mỗi đoạn là "[Nguồn 1]", "[Nguồn 2]". Lời dặn bảo model ghi "[1]", "[2]". Phần lớn lần model làm đúng, nhưng thỉnh thoảng nó chép nguyên nhãn "[Nguồn 2]" vào câu trả lời. Bộ kiểm lúc đầu chỉ hiểu "[2]", nên coi đó là "câu trả lời không có nguồn" và báo lỗi, dù câu trả lời đúng.

**So gì.** Trước và sau khi cho bộ kiểm nhận cả hai dạng; model gpt-6-luna.

| Đo gì | Trước | Sau |
|---|---|---|
| Số lần model ghi dạng "[Nguồn n]" | 24 trên 465 lần viết | (không đổi; đây là thói quen của model) |
| Số lỗi số nguồn trên 1.600 câu | 69 | 14 |
| Số câu đang đúng bị đổi | — | 0 |

**Đọc bảng này thế nào.** Model "sai" một cách hợp lý: nó chép đúng thứ nó thấy. Sửa ở chương trình (nhận cả hai dạng) chắc hơn dặn model thêm một câu, và không tốn lần gọi nào.

**Đã chọn: nhận cả hai dạng.**

### Từ chối cả câu, hay trả lời phần có bằng chứng

Đã kể ở bài 15: cho model trả lời một phần làm câu từ chối nhầm giảm từ 13 xuống 1 nhưng để 2 câu ngoài kho được trả lời. Điều kiện "0 câu ngoài kho được trả lời bằng kho" thắng, nên câu từ chối giữ nguyên là từ chối cả câu. Về sau câu hỏi có **nhiều ý** được xử lý bằng một đường riêng (bài 23).

**Giới hạn của các phép đo.** Cả hai phép so đo với gpt-6-luna, cuối tháng 10.

## Giới hạn đã biết

- **Chưa kiểm nghĩa** (đã nói ở trên).
- **Thiếu số nguồn chỉ bị phát hiện ở cuối**, sau khi chữ đã hiện. Người dùng thấy chữ rồi thấy nó bị rút.
- **Câu trả lời bị rút lại vẫn xảy ra.** Ở một lượt đo với người dùng mô phỏng ngày 21/11: 3 trên 48 lượt hỏi của gpt-6-luna và 4 trên 53 lượt hỏi của Claude Sonnet 5.5 có câu bị rút. Con số này gồm cả câu bị rút do bước kiểm con số thời tiết, không riêng do số nguồn; mới một người đọc.
- **Một câu trả lời đúng nội dung mà quên số nguồn cũng bị rút**, vì chương trình không phân biệt được với một câu bịa.
- **Người đọc không thấy ý nào đến từ nguồn nào.** Vì số [n] không hiện trong chữ, dòng "Nguồn:" chỉ cho biết cả câu trả lời dựa vào những bài nào. Đây là lựa chọn của chủ dự án về giao diện.

## Vì sao không làm cách khác

**Vì sao không dùng một model thứ hai để kiểm câu trả lời có đúng với nguồn không?** Chưa thử trên đường người dùng. Việc đó hiện chỉ có ở phép đo: một model chấm điểm câu trả lời so với đáp án mẫu (bài 19).

**Vì sao rút cả câu mà không chỉ gỡ số nguồn sai?** Chương trình được viết để rút cả câu khi số nguồn sai. Lý lẽ của người viết bài, không phải một quyết định đã ghi: một số nguồn không có thật nghĩa là không biết ý đó dựa vào đâu. Với con số về thời tiết và khoảng cách thì có cách nhẹ hơn: chỉ gỡ câu chứa con số lạ (bài 24).

**Vì sao không cho model tự viết lời từ chối cho tự nhiên hơn?** Quyết định đã ghi: câu từ chối cố định là một phần của điều kiện "chỉ trả lời từ kho", và các phép đo dựa vào nó.

## Chi tiết để tra

- Đếm lỗi số nguồn: 0 trên 489 lần viết (gpt-6-luna, đếm ngày 30/10); 0 trên 93 lượt (một lượt rà ngày 21/11 trên gpt-6-luna và các mức suy luận của Claude Sonnet 5.5).
- Việc nhận cả hai dạng số nguồn được sửa ngày 25/10.
- Trường hợp "câu trả lời có nguồn rồi nối câu từ chối ở cuối" được thấy ở 1 trên 3 lượt của một câu mà kho chỉ có một phần, ngày 21/11.
- Khi mục web có nội dung, máy chủ vẫn giữ nguyên câu từ chối trong kết quả của nó (các phép đo đọc câu này); chỉ giao diện thay bằng câu dẫn sang mục web.
- Câu hỏi nhiều ý: ý nào kho không có thì model ghi một dòng mở đầu bằng "Tư liệu chưa có thông tin về:"; dòng này không có số nguồn và không bị coi là lỗi (bài 23).

**Bài sau (bài 17):** hết chặng 3. Đường hỏi đáp đã đủ: tìm, viết, kiểm. Chặng 4 trả lời câu hỏi "lấy gì bảo đảm nó tốt": bộ câu hỏi mẫu và cách chấm.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Ba luật, nhận cả `[n]` và `[Nguồn n]`: `backend/llm/citations.py` (`CITATION_PATTERN`, `normalize_citations`, `select_cited_sources`) [code, đọc 22/11/2026].
- Giao diện bỏ số [n] khỏi chữ và hiện dòng "Nguồn:": `frontend/src/markdown.js` (hàm `boMaTrichDan`), `frontend/src/SourceLine.jsx` [code]; lựa chọn của chủ dự án: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` mục "Hai lựa chọn đáng nhớ".
- Rút lại ở đường chat (sự kiện báo lỗi kèm cờ "sau khi đã hiện chữ", kết cục "retracted"): `backend/api/routes/chat.py`, hàm `finish` của đường stream [code].
- Gỡ câu từ chối nối ở cuối (21/11, 1 / 3 lượt): `backend/llm/assistant.py`, hàm `bo_cau_tu_choi_cuoi` và chú thích của nó [code].
- Từ chối không gọi model khi không có đoạn nào: `assistant.py`, hàm `prepare_answer` [code].
- Câu từ chối, câu ngoài phạm vi, danh sách câu được tính là từ chối, dòng "có thể đã thay đổi": `backend/llm/full_corpus_prompt.py` (`INSUFFICIENT_ANSWER`, `OUT_OF_SCOPE_ANSWER`, `CAU_LAM_THAY`, `REFUSAL_ANSWERS`, `MAY_HAVE_CHANGED_NOTICE`); nhóm bài có dòng đó: `assistant.py`, `NOTICE_SOURCE_PREFIXES` [code].
- Câu dẫn sang mục web do giao diện thay, máy chủ giữ câu từ chối: `frontend/src/moDauWeb.js` (chú thích đầu file) [code].
- Ví dụ chính (số nguồn 1, 2, 4, 5, 6): `data/hoc_cung_D/vi_du_di_suot_vet.json`; ví dụ chỗ đậu ô tô: `data/hoc_cung_D/vi_du_kho_khong_co_2_vet.json` [đã chạy].
- 24 / 465; 69 ⇒ 14 trên 1.600 câu; 0 câu đúng bị đổi; 0 / 489: `bai_hoc/08_GENERATION.md` (mục "Một chuyện thật" và mục Nguồn) [đã chạy, gpt-6-luna].
- 0 lỗi trích dẫn / 93 lượt với Claude: `data/thu_bedrock_2026-11-21/c_harness/RA_HARNESS.md` dòng 17 [riêng tư, 21/11].
- Câu bị rút 3 / 48 và 4 / 53 (người dùng mô phỏng, một phiên đọc tay, chưa có người thứ hai): `bai_hoc/VIEC_MOI_XONG.md` mục 23, bảng "Người dùng gặp gì".
- Trả lời một phần (13 ⇒ 1; 2 câu ngoài kho): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 11.
- Điều kiện "0 câu ngoài kho được trả lời bằng kho": `session_prompt/HIEN_TRANG.md` mục 4, phần "Sản phẩm".

</details>
