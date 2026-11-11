# Bài 20 — Làm đồ án thế nào: dòng thời gian, nhiều agent, rào bằng máy

*Cập nhật lần cuối: 15:17, ngày 11/11/2026 · bài mới; chỉ kể phần đã làm xong; đã qua một lượt kiểm độc lập.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Agent — **mới** | coding agent (Claude Code, Codex, Antigravity) | Một chương trình AI đọc code, chạy lệnh, viết code và báo cáo theo việc được giao. |
| Session A / B / C / E | vai trong `session_prompt/WORKFLOW.md` | Mỗi agent mở một cửa sổ riêng, giữ một vai. A điều phối và làm việc với anh; B, C, E làm việc A giao. |
| Kiểm chéo | review chéo (`risk-gated-agent-review`) | Việc một agent làm thì một agent khác kiểm; không ai tự duyệt việc của mình. |
| Rào bằng máy — **mới** | hook git (`.githooks/pre-commit`, `pre-push`) | Đoạn mã tự chạy mỗi lần ghi hay đẩy code lên GitHub, chặn dữ liệu riêng tư. |
| Cổng kiểm | "cổng ổn định" | Danh sách kiểm phải qua trước khi một thay đổi vào bản chính (`main`). |
| Luật ghi trước | tiêu chí ghi trước (`run-experiment`) | Viết sẵn thước, mốc, sàn trước khi đo (bài 11, 19). |

---

*Bài 0–19 kể chatbot làm gì. Bài này kể **đồ án được làm ra thế nào**: theo trình tự nào, ai làm phần nào, và vì sao tin được những con số ở các bài trước.*

## Quay lại người hướng dẫn viên

Một văn phòng du lịch nhỏ muốn soạn cuốn sổ tay thật tốt. Trưởng phòng (là anh) quyết **làm cuốn sổ cho ai, cái gì được làm, cái gì phải dừng**. Nhân viên (các
agent) soạn, thử, đo. Có ba nếp làm việc: bài một người soạn thì **người khác đọc soát**; mọi thử nghiệm **ghi trước** thế nào là đạt; và ở cửa văn phòng có
**máy soi** tự chặn mọi tờ giấy mật trước khi nó ra ngoài, không cần ai nhớ.

## Dòng thời gian

| Lúc | Làm gì | Ai làm |
|---|---|---|
| 05/08 – 14/09 | Phase 0–5: dựng kho bài Markdown, khung máy chủ, cách chia đoạn, vector + từ khoá, Qdrant, cách tìm | Antigravity (model Gemini) viết, Codex kiểm; anh chuyển tin giữa hai bên |
| 29/09 – 22/10 | Mỗi đoạn mang 7 trường thông tin (bài 3); Phase 6: viết câu trả lời + API + giao diện đầu tiên | như trên |
| 23 – 24/10 | Đổi model viết sang gpt-6-luna; bộ 176 câu mẫu (bài 9), sửa kho + dựng lại chỉ mục, công cụ chấm + điểm mốc | Claude bắt đầu làm |
| 24/10 | **Đổi cách làm**: nhiều session Claude cùng lúc, A điều phối, kiểm chéo | anh duyệt |
| 24 – 25/10 | **Phase 8.1: rà lại các quyết định cũ bằng thí nghiệm** | Claude A / B / C |
| 25 – 26/10 | **Rà lại toàn bộ code**, sửa 5 gói | Claude A / B / C |
| 26 – 28/10 | Phase 8.2: đưa phương án thắng vào chatbot (10 đoạn + chuẩn hoá chữ) | Claude A / B / C |
| 28 – 30/10 | Hai đợt sửa kho, mỗi đợt 123 chỗ (bài 1); thử Qwen3-8B rồi bỏ (bài 4) | Claude |
| 31/10 – 01/11 | Chữ hiện dần, lượt đo cuối Phase 1–8, anh tự đọc 20 cặp câu trả lời; anh đóng Phase 8 | Claude A / B / C |
| 02/11 – nay | Phase 9 (còn mở), các phần đã bật: trợ lý (bài 12–15), trang cổng (bài 17), đóng gói Docker (bài 18). Phase 10: hỏi bằng ảnh (bài 15) | Claude A / B / C / E |

**Vì sao có Phase 8.1.** Khi rà, mình đếm được 56 quyết định kỹ thuật của Phase 0–7, phần lớn do hai agent trước chọn. Chỉ **2 / 56** từng được so trên toàn kho,
**29** chưa từng so, **16** là mặc định không ghi lý do. Anh chốt một nguyên tắc từ đó: **luôn thử và so với mốc trước khi chọn**. Phase 8.1 đo lại **10 quyết định
quan trọng nhất** (trong 56) với cách cũ làm mốc, và chatbot không đổi trong lúc đo. Kết quả: chỉ một thay đổi thắng là đưa 10 đoạn thay vì 5 (bài 19, dòng
10); các lựa chọn đã đo khác giữ nguyên, nay **có số đo** để giải thích.

**Rà lại code (25–26/10).** Hai agent rà hai nửa code, rồi kiểm chéo phát hiện của nhau, được **39 phát hiện**, gom thành 5 gói. Anh duyệt cả 5 rồi mới sửa:
- Bộ kiểm nguồn nhận cả "[Nguồn 2]" lẫn "[2]". Trước đó model hay viết "[Nguồn 2]" mà bộ kiểm cũ chỉ nhận "[2]", nên câu trả lời đúng bị báo lỗi nguồn. Chấm lại 1.600 câu: lỗi nguồn **69 ⇒ 14**.
- Máy chủ báo lỗi đúng loại: Qdrant hỏng thì báo "tạm không tìm được", không báo "lỗi nội bộ".
- Bỏ code thừa: phần backend từ **8.345 xuống 6.218 dòng** (khoảng −25 %).
- Bỏ khỏi code, test, cấu hình những chỗ chép nguyên văn nội dung kho (80 báo cáo cũ còn trích một phần, anh chọn để nguyên).

Các gói chạm phần tìm và phần dựng chuỗi gửi model đều được so: **giống từng byte** trước và sau khi sửa, tức chatbot trả lời y như cũ. Riêng gói bộ kiểm
nguồn thì cố ý đổi: hết báo lỗi nhầm.

## Anh quyết, agent làm

**Anh quyết** phạm vi, tiền, dữ liệu, hướng sản phẩm, và đóng từng Phase. Vài quyết định làm nên đồ án:
- 24/10: luôn so với mốc trước khi chọn; câu đánh giá phải giống câu người thật hỏi.
- 26/10: chất lượng cần thiết trước, tối ưu tốc độ / tiền sau.
- 27/10: đồ án xem như sản phẩm thật; người dùng là du khách, người dân, và anh.
- 28/10: mốc tốc độ p50 ≤ 3 / p95 ≤ 5 giây, ≤ 0,0005 USD / câu; thứ tự lỗi tệ nhất (bài 11).
- 01/11: tên đề tài chốt với giảng viên (bài 0); đóng Phase 8.
- 02/11: Phase 9 phải là trợ lý có công cụ, không chỉ RAG.

**Agent làm** phần còn lại: viết code, test, đo, kiểm chéo, viết báo cáo, và đưa phương án cho anh chọn (mỗi phương án nêu hệ quả, khi nào sai). Chi tiết kỹ thuật
trong phạm vi đã duyệt, agent tự quyết và ghi lý do.

## Bốn nếp làm việc giữ chất lượng

**1. Không ai tự duyệt việc của mình.** Việc của B thì C hoặc agent con khác kiểm; việc A tự làm thì B hoặc C kiểm. Người kiểm chỉ dựa trên tài liệu thiết kế và
code, không dựa lời người làm. Tài liệu thiết kế được kiểm **tối đa 2 vòng**; code được kiểm **một lần cho cả nhánh**. Ví dụ đã bắt được: một kế hoạch dùng lệnh
sẽ đưa nội dung kho lên GitHub công khai; ba lỗi code trước khi gộp; người kiểm ngữ cảnh mới bắt 15 lỗi lớn ở 3 bản kế hoạch.

**2. Luật ghi trước, giữ cả kết quả âm.** Mỗi thí nghiệm ghi trước thước, mốc, sàn (bài 11). Phương án bị bỏ vẫn được giữ lại thành **hồ sơ** (hiện có 14
hồ sơ, ví dụ lấy 100 ứng viên, model xếp lại, Qwen3-8B, xã giao song song), để sau này biết đã thử gì và vì sao bỏ.

**3. Cổng kiểm trước khi vào bản chính.** Trước khi một thay đổi vào `main`: chạy test của phần bị chạm; dựng lại giao diện nếu có chạm; mở máy chủ thật, kiểm
trang chủ mở được, kiểm sức khoẻ 5 / 5, hỏi 1 câu trong kho + 1 câu ngoài kho, đếm log có đúng số câu và **không có chữ câu hỏi**. Nếu chạm phần tìm hay chia
đoạn thì kết quả tìm 158 câu phải giống từng byte.

**4. Tự soi chỗ làm quá tay.** Anh đã nhắc nhiều lần là làm quá kỹ những phần lợi ít. Ví dụ: chữ hiện dần qua 4 bản thiết kế và 3 vòng kiểm, mà lợi đo được chỉ
0,44 giây; có giai đoạn 65 % commit chỉ là tài liệu. Từ 09/11, phiên nào cũng có **vòng tự soi**: bỏ mọi lượt đo không bảo vệ sàn nào, các session tự nhận
định có đang làm quá tay không. Lần đầu làm, 4 session cắt nhiều lượt đo thừa, tiết kiệm khoảng 1–2 giờ.

## Rào bằng máy: không cần ai nhớ

Repo trên GitHub là **công khai**. Một dòng dữ liệu riêng tư đã lên lịch sử Git thì coi như không gỡ được. Vì vậy những thứ không được lọt thì **máy chặn**, không
chỉ dặn bằng chữ:

| Rào | Chặn gì |
|---|---|
| Hook lúc ghi code (`pre-commit`) | file vùng riêng tư (dữ liệu, kho, bản nháp gửi ChatGPT, khoá); dòng mới trông như khoá bí mật; dòng mới nhắc tên dự án khác của anh; dòng mới **trùng từ 40 ký tự liên tiếp** với bộ câu mẫu, câu kín hay kho |
| Hook lúc đẩy lên GitHub (`pre-push`) | kiểm lại mọi commit sắp đẩy bằng 3 phép nhanh (file riêng tư, khoá, tên dự án khác), phòng khi ai đó bỏ qua hook lúc ghi |
| Cấu hình Claude Code | cấm đọc file khoá `.env`; cấm gọi Antigravity (điều khoản của Google cấm phần mềm bên thứ ba truy cập, có thể khoá tài khoản anh). Với agent khác, đây là luật chữ trong `AGENTS.md` |
| Script tìm trong kho | agent tìm trong kho chỉ bằng script đã loại sẵn bộ câu mẫu, câu kín, ghi chép nội bộ và bản thô của nguồn |

Hook git áp cho **mọi** agent và cả người, vì nó nằm trong repo chứ không trong một công cụ riêng.

## Một chuyện thật: "nhớ quét trước khi commit" là không đủ

Ngày 24/10, suýt commit một dòng có số liệu của một dự án khác của anh. Ngày 25/10, mình dựng hook chặn ngay lần đầu. Phép quét "trùng với bộ câu mẫu" lúc đó
còn là **việc agent tự nhớ chạy**. Hai lần (25/10 và 26/10), agent chạy lệnh quét **rồi nối luôn lệnh commit ở cùng một dòng**: quét báo trùng, nhưng commit vẫn
chạy. Lần đó may là chỉ trùng câu từ chối chuẩn, vốn công khai.

Bài học: luật chữ "nhớ quét" không đủ. Phép quét được đưa **vào chính hook**: máy tự chạy, không cần ai nhớ. Sau đó sổ ghi lại ít nhất **4 lần hook chặn
đúng**: 1 lần nhờ chính phép quét trùng (một báo cáo chép nguyên văn câu trả lời có chữ trong kho), 3 lần nhờ phép chặn tên dự án khác (một đường dẫn trong
tài liệu việc, một script đổi tên file, một dòng nhắc tên). Những gì hook kiểm được thì sổ chưa ghi lần nào lọt. Còn loại hook **không** kiểm được (tả câu đo
quá cụ thể trong báo cáo) thì đã lọt lên lịch sử công khai ít nhất 4 lần, mức nhẹ; việc này vẫn dựa luật chữ.

Một chuyện cùng kiểu: chính hook chặn khoá bí mật, người viết tự thử 12 ca đều đạt, nhưng người kiểm độc lập tìm ra hook **bỏ qua một dạng dòng** (kể cả dòng
có khoá). Lỗ hổng nằm ngay trong rào chống lộ dữ liệu, và được vá trước khi dùng.

## Sổ cải tiến cách làm

Cuối mỗi phiên, A gom các sự cố có bằng chứng (mất giờ, mất tiền, anh phải nhắc lại) thành tối đa 3 đề xuất sửa luật hay thêm rào, anh duyệt rồi mới áp; luật
nào thành thừa thì gỡ. Tới 11/11: **25 vòng**, **120 sự cố** được ghi (gồm cả việc làm đúng đáng giữ). Hầu hết các luật trong bài này ra đời từ đó: giờ ghi
trong tài liệu phải lấy từ máy, không gõ tay (đã lọt ít nhất 11 lần; rào chỉ cảnh báo nên 11/11 vẫn lọt một lần); "đếm lỗi rẻ trước khi xây tính năng" (sau khi 4 tính năng thử đều âm, tốn
khoảng 0,6 USD).

## Tiền làm đồ án

| Giai đoạn | Tiền API (USD) |
|---|---|
| Phase 8.1 (rà quyết định) | 0,17 |
| Phase 8.2 (áp phương án thắng + cải tiến từng khâu) | 0,23 |
| Hai đợt sửa kho | 0,12 |
| Đóng gói Phase 1–8 (chữ hiện dần, đo cuối) | 0,15 |
| Phase 9 (trợ lý, giao diện, đóng gói), tính tới 11/11 | 3,88 |
| Hỏi bằng ảnh, tính tới 07/11 | 0,10 |
| **Cộng từ 24/10 tới 11/11** | **khoảng 4,7 USD ≈ 118.000 đồng** |

Phase 0–6 (08–10/2026) không có số tiền trong tài liệu; ngày 24/10 (công cụ chấm + điểm mốc) khoảng 0,09 USD. Phần agent đọc, viết, kiểm dùng gói thuê bao Claude, không tính vào bảng. Phần lớn tiền (khoảng 82 %)
nằm ở Phase 9, gồm cả lượt đo của những tính năng thử rồi bỏ. Mỗi phiên có trần tiền, ban đầu ≤ 1 USD / phiên; từ 07/11 anh cho vượt khi cần, nhưng mỗi việc
vẫn ghi tiền thật từ log.

## Khi nào cách làm này hỏng

- **Hai agent cùng một model** có thể cùng chung một điểm mù. Người kiểm ngữ cảnh mới giảm được điều này, nhưng không loại hết.
- **Người chấm câu trả lời là Claude**; mốc người mới có một lần anh tự đọc 20 cặp (bài 11).
- **Hook chỉ chạy khi máy đã bật nó** (mỗi bản clone mới phải bật một lần), và chỉ bắt được những gì máy kiểm được, như tên, dạng khoá, chuỗi trùng. Mô tả câu
  quá cụ thể vẫn phải dựa luật chữ.
- **Làm quá tay** vẫn có thể quay lại; vòng tự soi chỉ giảm, không chặn được.

## Ba điều chính

1. **Dòng thời gian:** Phase 0–6 do hai agent trước dựng; từ 23/10 Claude làm, từ 24/10 nhiều session Claude làm theo vai, **Phase 8.1 rà lại 10 quyết định quan trọng nhất** (chỉ 2 / 56 từng
   được so trên toàn kho) và **rà lại code** (39 phát hiện, 5 gói, code bớt 25 %), rồi mới làm trợ lý.
2. **Anh quyết** phạm vi, tiền, dữ liệu, hướng sản phẩm; **agent làm** và **kiểm chéo nhau**. Luật ghi trước, giữ hồ sơ kết quả âm, cổng kiểm trước khi vào
   bản chính, vòng tự soi.
3. **Rào bằng máy** chặn dữ liệu riêng tư trước khi lên GitHub công khai. Chuyện thật: "nhớ quét" bị lọt 2 lần ⇒ đưa vào hook ⇒ chặn đúng ít nhất 4 lần;
   những gì hook kiểm được thì chưa lần nào lọt. Tiền API cả giai đoạn từ 24/10: khoảng 4,7 USD.

**Bài sau:** Bài 21 — Dữ liệu người dùng đi đâu, và bảo mật.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Ai làm Phase 0–6: `guides/phase_1_backend_skeleton.md` ("Implementer: Antigravity / Reviewer: Codex"), dòng đầu report trong `reports/` (Gemini / Codex; từ 23/10 "Claude Opus 5.5") [tài liệu]; commit đầu 05/08/2026: `git log --reverse` [đã chạy]
- Ngày đóng Phase: `session_prompt/Project_Status.md` §2, §3; guide từng Phase [tài liệu]
- Đổi cách làm 24/10: `docs/superpowers/specs/2026-10-24-governance-v2-design.md` [tài liệu]
- 2 / 56, 29, 16: `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §1 [tài liệu]
- Rà code: 39 phát hiện, 5 gói, lỗi nguồn 69 ⇒ 14 trên 1.600 câu, giống byte: `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`, `bao_cao_he_thong/94_DE_XUAT_SUA_CODE.md`; 8.345 ⇒ 6.218 dòng: `report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md` [đã chạy; agent con đếm lại 11/11 ở `76ff419` / `421c302`, khớp]
- Quyết định của anh có ngày: `session_prompt/Project_Status.md` §1, §5 [quyết định của anh]
- Kiểm chéo, tối đa 2 vòng plan / 1 review code: `session_prompt/WORKFLOW.md` §5; ví dụ bắt được: `session_prompt/SO_CAI_TIEN_CACH_LAM.md` (S25, S98, S108) [tài liệu]
- 14 hồ sơ: `git tag -l 'hoso/*'` [đã chạy, 11/11]
- Cổng kiểm: `session_prompt/CURRENT_HANDOFF.md` "Việc đang mở — luật chung" [tài liệu]
- Tự soi: `session_prompt/Session_Prompt.md` §7; 4 bản thiết kế + 3 vòng / 0,44 s (S64), 65 % commit tài liệu (S106), lần đầu tiết kiệm 1–2 giờ (S113): sổ cải tiến [tài liệu]
- Hook: `.githooks/pre-commit` (vùng private, dạng khoá, tên dự án khác, quét trùng 40 ký tự qua `.githooks/overlap_scan.py`), `.githooks/pre-push` (3 phép, không quét trùng); `.claude/settings.json` (cấm đọc `.env`, cấm `agy`) [code]
- Chuyện thật: sổ cải tiến S2, S23, S28 (quét tay nối commit), W16 (đưa vào hook), S71, S97, S116 + một lần 31/10 (chặn đúng), S10 (lỗ dòng `++`, vá ở `.githooks/pre-commit`) [tài liệu]
- Sổ cải tiến 25 vòng, 120 sự cố; giờ ước lọt ≥ 11 lần; 4 tính năng âm ≈ 0,6 USD (S110): `session_prompt/SO_CAI_TIEN_CACH_LAM.md` [tài liệu]
- Tiền: `session_prompt/Project_Status.md` §2, §3, §5; `session_prompt/PROJECT_HISTORY.md`; tổng ≈ 4,7 USD là cộng tay của agent con, có thể lệch nhẹ (một số ngày không tách tiền) [suy ra]
- Bản ghi số liệu (agent con, chỉ đọc, 11/11): `data/hoc_cung_user_2026-11-10/fact_bai_20_lam_do_an.md` (riêng tư)
- Ví dụ văn phòng du lịch là ví dụ tự đặt.

- **Sửa 15:17 11/11/2026** (người kiểm độc lập bắt, mình đối chiếu nguồn; biên bản `data/hoc_cung_user_2026-11-10/review_bai_20_21.md`, riêng tư): "[Nguồn 2]" là kiểu model viết (bản trước ghi ngược); 8.1 đo 10 quyết định quan trọng nhất, không phải cả 56 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_synthesis.md`); 4 lần chặn = 1 quét trùng + 3 tên dự án khác; mô tả câu quá cụ thể đã lọt ≥ 4 lần (sổ cải tiến S40); giờ ước vẫn lọt sau rào (W37, S119); đổi model 23/10 và 7A–7B do Claude; hỏi bằng ảnh là Phase 10; 24/10 ≈ 0,087 USD (`session_prompt/PROJECT_HISTORY.md`); 80 báo cáo cũ còn trích kho (`94_…` §2); `scripts/grep_kb.sh` loại `evaluation/`, `meta/`, `_source-dumps/`, `*sealed*`.

</details>
