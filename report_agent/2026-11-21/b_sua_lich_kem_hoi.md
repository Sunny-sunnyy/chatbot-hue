# Tin vừa sửa lịch vừa hỏi: phần hỏi không còn bị bỏ im (nhánh `p9-b-sua-lich-kem-hoi`, cờ `sua_lich_kem_hoi`, mặc định TẮT)

Viết: 18:49 21/11/2026 (giờ `date`), phiên B. Giao: phiên điều phối — bản sửa số 1 của bước 4, khối A của sổ việc (đuổi một con số sản phẩm). Nền: main `cf1a70c3` (bản
phiên đo ghim cho lượt mốc). Trạng thái: **code + test xong, đã đo thật trên hai model, một chuỗi qua đường chat thật đạt; CHƯA gộp, cờ TẮT; chờ phiên C đọc diff + số.**
Quyết định đang chờ kết quả này: giữ hay gỡ bản sửa; có bật cờ không.

Từ dùng: *lần hiểu ý* = một lời gọi model riêng đọc tin của người dùng khi cuộc trò chuyện đã có lịch, trả danh sách hành động sửa có tên (bỏ / thêm / thay / dời…); code áp và
viết câu báo · *lượt sửa* = lượt mà lần hiểu ý trả ít nhất một hành động ⇒ người dùng nhận thẻ lịch đã sửa, không nhận câu trả lời thường · *khối thay đổi* = mấy dòng đầu thẻ lịch
("Đã bỏ…", "Chưa làm…"), do code viết · *model cũ* = gpt-6-luna · *model đang chạy* = Claude Sonnet 5.5, mức suy luận high · *bộ mù* = 22 tin thử do phiên điều phối soạn, không nhìn lời dặn của bản sửa.

## 1. Người dùng thấy gì khác (khi cờ bật)

| Người dùng gửi | Trước (bản đang chạy) | Sau |
|---|---|---|
| Một tin vừa sửa lịch vừa hỏi ("Ngày 2 nhìn hơi dày, bỏ Lăng Đồng Khánh đi. Mà chùa Thiên Mụ có cần mặc đồ kín không ạ?") | Lịch được sửa; phần hỏi KHÔNG được nhắc tới. Người dùng mô phỏng phải hỏi tới lần ba | Lịch được sửa như cũ; khối thay đổi có thêm dòng cuối: "Chưa làm: phần câu hỏi trong tin này mình chưa trả lời — lượt này mình chỉ sửa lịch. Bạn gửi riêng câu hỏi đó, mình trả lời ngay." |
| Gửi riêng câu hỏi ở tin kế | Được trả lời (đường hỏi đáp thường) | Không đổi — và trả lời trên lịch ĐÃ sửa |
| Tin chỉ sửa lịch · tin chỉ hỏi | — | Không đổi |

Cờ bật KHÔNG làm cho lượt sửa trả lời luôn câu hỏi; nó chỉ nói thật là câu hỏi chưa được trả lời và chỉ cách hỏi lại. Vì sao dừng ở mức này: mục 6.

## 2. Nguyên nhân gốc

`backend/llm/len_ke_hoach.py`, hàm `hieu_va_ap`: lần hiểu ý trả ít nhất một hành động sửa ⇒ CẢ lượt thành lượt sửa; `stream_sua` chỉ phát thẻ lịch. Không có chỗ nào ghi nhận phần còn lại của tin.
Do code quyết nên gặp là hỏng, ở cả hai model. Số đã thấy: người dùng mô phỏng ngày 21/11 — 4 / 4 lượt được nhận là câu sửa lịch đều kèm câu hỏi và đều bị bỏ phần hỏi (một vai, hai model).
Tần suất ngoài đời CHƯA BIẾT: log số đo có 158 lượt sửa lịch trên 3.912 lượt không phải bộ thử, nhưng dòng số đo không lưu chữ nên không đếm được bao nhiêu lượt kèm câu hỏi.

## 3. Đổi gì

| File | Đổi gì |
|---|---|
| `backend/llm/sua_lich_v2.py` | Khuôn `HanhDongHoi` / `HanhDongToiHoi`: thêm loại hành động `hoi_them` (không trường nào) · hằng `CAU_HOI_THEM` · `thay_doi`: kết quả áp có `hoi_them` ⇒ thêm dòng cố định ở CUỐI khối, `duoc: false` |
| `backend/llm/full_corpus_prompt.py` | Hai lời dặn mới = hai lời dặn đang dùng + ĐÚNG một gạch tả `hoi_them` (gồm: lời nhờ sửa viết thành câu hỏi không phải `hoi_them`; tin không có ý sửa vẫn trả danh sách rỗng) |
| `backend/llm/generator_openai_full_corpus.py` | Hai agent mới (khuôn + lời dặn mới, khoá đệm riêng); `hieu_sua(..., kem_hoi=True)` chọn chúng; khuôn mới dài hơn một phần tử nhưng số hành động SỬA vẫn bị chặn ở mức cũ bằng code |
| `backend/llm/len_ke_hoach.py` | `hieu_va_ap`: tách `hoi_them` ra TRƯỚC mọi bước cũ (tin chỉ có `hoi_them` ⇒ như danh sách rỗng ⇒ đường hỏi đáp thường); là lượt sửa và có `hoi_them` ⇒ gắn vào kết quả áp + vào số đo `sua_lich` (`hoi_them: true`, chỉ là cờ, không chữ) |
| `backend/llm/assistant.py`, `backend/config/settings.yaml` | Cờ `sua_lich_kem_hoi` (TẮT), cần cờ `sua_lich_chua_ho_tro` |
| `backend/tests/test_sua_lich_kem_hoi.py` | 7 test (0 đồng) |

Không chạm giao diện: dòng mới bắt đầu bằng "Chưa làm" nên thành phần `ThayDoi` của `frontend/src/LichV2.jsx` hiện nó theo kiểu dòng chưa làm có sẵn [mới đọc code, chưa nhìn trình duyệt].
Model chỉ báo CÓ / KHÔNG; không chữ nào của model hay của người dùng đi tới chỗ mới. Vì sao không dò bằng code (dấu "?"): lời nhờ sửa hay viết thành câu hỏi ("bỏ X được không?").

## 4. Số đo

Tiêu chí ghi TRƯỚC khi chạy và trước khi phiên B mở bộ mù (riêng tư: `data/thu_bedrock_2026-11-21/b_buoc_4/kem_hoi/TIEU_CHI.md`; kết quả `KET_QUA.md` cùng thư mục).
Đo riêng lần hiểu ý trên một lịch cố định: 22 tin × 2 model × cờ tắt ↔ bật × 3 lượt = 264 lời gọi; 0 lỗi gọi model.

| Tiêu chí ghi trước | Model đang chạy | Model cũ |
|---|---|---|
| Sàn — cờ tắt: lời dặn + khuôn của ba agent cũ giống cây chính từng byte | đạt (7 mã băm) | như bên |
| Sàn — 8 tin chỉ sửa: dòng báo hiện NHẦM ≤ 1 / 24 | 0 / 24 — đạt | 1 / 24 — đạt, sát mức (một câu hỏi tu từ kèm ý sửa) |
| Sàn — 6 tin chỉ hỏi: không thêm lượt nào bị kéo sang đường sửa | 0 / 18 ↔ 0 / 18 — đạt | 0 / 18 ↔ 0 / 18 — đạt |
| Sàn + lợi — ý sửa bên bật y như bên tắt (số cặp khác không vượt mốc nhiễu của ba lượt bên tắt) | khác 0, mốc 0 — đạt | **theo tiêu chí ghi trước: CHƯA RÕ** — khác 1 cặp ở nhóm chỉ sửa và 1 cặp ở nhóm sửa + hỏi, mốc ba lượt = 0 |
| Lợi — 8 tin sửa + hỏi: dòng báo hiện ≥ 20 / 24 (bên tắt theo cấu tạo là 0) | 24 / 24 — đạt | 24 / 24 — đạt |

Về dòng "chưa rõ" của model cũ: theo phép lặp bổ sung làm SAU khi thấy số (hai tin lệch × 10 lần mỗi bên, 40 lời gọi) thì hai ô lệch nằm trong dao động của chính bên tắt (bên tắt tự khác mình
3 / 10 và 2 / 10 ở hai tin đó); có 1 / 13 lần bên bật ra một ý sửa sai ("thêm vào buổi chiều" thay vì "thay hoạt động buổi tối"), không lặp lại trong 10 lần — không đủ để nói do lời dặn mới hay do may rủi.
Phép đóng dòng này do phiên C làm (chọn trước 4 tin chỉ sửa khác, × 10 mỗi bên): CHỜ.

Chuỗi qua đường chat thật (`/api/chat/stream` trong cùng tiến trình, cờ bật bằng ghi đè cấu hình, MỘT lần mỗi model) [máy kiểm + phiên B đọc chữ]: lập lịch 2 ngày ⇒ tin sửa + hỏi ⇒ gửi riêng câu hỏi.
Cả hai model: lượt 2 — khối thay đổi = "Đã bỏ Lăng Đồng Khánh." + dòng báo ở cuối; lượt 3 — trả lời "cần mặc kín đáo…" có nguồn và liệt kê ngày 2 theo lịch đã sửa (không còn Lăng Đồng Khánh). Lượt sửa mất 2,2 giây ở cả hai model.

Tiền thật: model đang chạy (Bedrock) 1,53 USD lượt đo + 0,07 USD chuỗi (phiên B đã ước 0,5–1 USD — ước thấp: một lời gọi hiểu ý ở mức suy luận high khoảng 0,011 USD) · model cũ (OpenAI) 0,017 USD.

## 5. Bảng "xong"

| Người dùng làm được (khi cờ bật) | Mức kiểm |
|---|---|
| Gửi một tin vừa sửa lịch vừa hỏi ⇒ thấy lịch đã sửa VÀ một dòng nói câu hỏi chưa được trả lời, hãy gửi riêng | máy kiểm: 24 / 24 mỗi model trên bộ mù + một chuỗi qua đường chat thật mỗi model |
| Gửi riêng câu hỏi ở tin kế ⇒ được trả lời trên lịch đã sửa | máy kiểm + đọc chữ: một chuỗi mỗi model |

| Người dùng CHƯA làm được | Vì sao |
|---|---|
| Nhận luôn câu trả lời cho phần hỏi ngay trong lượt sửa | chưa làm — mục 6 |
| Thấy dòng báo khi cờ tắt | cờ TẮT; bật là quyết định của phiên điều phối / chủ dự án |

| Chưa làm · tự hoãn | Lý do |
|---|---|
| Nhìn giao diện (dòng báo trong thẻ lịch, khung trợ lý nổi, khổ điện thoại) | gom với lượt trình duyệt của phiên đo |
| Đo khi cờ `sua_lich_buoi_toi` cùng bật | cờ đó đang tắt trên main |
| Con số "phiên người dùng mô phỏng đạt mục tiêu" trước ↔ sau | chờ lượt mốc; dự đoán của phiên B: vai có tình huống này đã đạt ở lượt 4 trên cả hai model nên con số nhiều khả năng không đổi — thứ đổi là số LƯỢT bị bỏ im |
| Phiên khác đọc diff | đang chờ phiên C |

| Lệnh kiểm (từ `backend/`) | Đầu ra phiên B thấy |
|---|---|
| `uv run pytest tests/test_sua_lich_kem_hoi.py -q` | `7 passed` · đổi dòng `kq["hoi_them"] = True` thành `pass` ⇒ `2 failed, 5 passed` |
| `uv run pytest tests/test_sua_lich_v2.py -q` · `tests/test_sua_lich_buoi_toi.py` · `tests/test_rao_so_ngay.py` (từng file) | `13 passed` · `7 passed` · `44 passed` |
| So mã băm của `SUA_LICH_LOI_DAN`, `SUA_LICH_LOI_DAN_CHT`, `SUA_LICH_LOI_DAN_TOI`, `SONNET_SUA_LICH` và khuôn `SuaLichOutput`, `SuaLichOutputCHT`, `SuaLichOutputToi` giữa nhánh và cây chính | 7 / 7 giống |

## 6. Vì sao chưa làm mức "trả lời luôn phần hỏi dưới thẻ lịch"

Muốn trả lời đúng thì phải chạy đường hỏi đáp thường lần hai SAU khi lịch đã sửa (đường thường đang chạy song song với lần hiểu ý là trên lịch CŨ ⇒ câu như "ngày 1 đi hết mấy tiếng" có thể ra số của lịch cũ),
rồi ghép hai câu trả lời vào một lượt: đánh số nguồn, phép kiểm trích dẫn, lưu hội thoại, số đo, giao diện — chạm hàm phức tạp nhất của lõi (`_sua_song_song` trong `backend/llm/assistant.py`).
Đó là bước kế nếu số đo sau khi bật cho thấy người dùng vẫn mất lượt. Khi cờ bật, dòng số đo của lượt sửa có `hoi_them: true` ⇒ lần đầu đếm được trên log thật bao nhiêu lượt sửa lịch có kèm câu hỏi — con số để quyết bước kế.

**Một dòng cuối:** phép này KHÔNG cho biết người dùng thật có làm theo dòng báo không · hướng rộng hơn: trả lời luôn dưới thẻ lịch (mục 6) · đếm rẻ nhất: cờ `hoi_them` trong log số đo sau khi bật.
