# Workflow — cách làm và phối hợp A / B / C / E

Áp dụng cho mọi session. Luật chung: `Session_Prompt.md`; cách nhìn việc + bảng quyền: `AGENTS.md` (không lặp lại ở đây).
Bản trước lượt gọt 21/11/2026 (số mục giữ nguyên): `git show 708c987d:session_prompt/WORKFLOW.md`.

## 1. Vai trò

| Session | Việc |
|---|---|
| **A — điều phối** | Làm việc với User; giao việc; review chéo; tự làm việc nhỏ; giữ `HIEN_TRANG.md`, `VIEC_DANG_MO.md`, `CURRENT_HANDOFF.md`; gộp vào `main` |
| **B, C, E — thực thi** | Làm việc A giao; tự kiểm; viết report; review chéo khi được giao; nêu hướng khác / cải tiến có căn cứ |
| **D — học cùng User** (tùy chọn) | Chỉ đọc; giúp User tự hiểu việc đã làm (§10) |

- Tên là vai, không phải model: agent nào mở bằng `START_SESSION.md` với `<X>` nào thì giữ vai đó.
- **Review chéo:** ai làm thì người khác kiểm — kể cả việc A tự làm.
- B, C, E tự hoàn thiện và tối ưu trong phạm vi việc (đặt tên, tổ chức hàm, sửa lỗi gặp trong phạm vi) mà không hỏi từng chi tiết. Ngoài phạm vi: không tự
  XÂY thêm; thứ thấy được (lỗi, chỗ thiếu, hướng tốt hơn) ghi vào report hoặc nhắn A — nếu nó làm đổi việc đang làm thì nói TRƯỚC khi làm tiếp.

## 2. Mở session

1. Đọc theo `START_SESSION.md`.
2. Kiểm nhanh, chỉ đọc:
   ```bash
   cd /home/minhhieu/hue_rag
   git branch --show-current; git log --oneline -3; git status --short | grep -v '^??'
   git config --get core.hooksPath             # phải in .githooks; khác ⇒ báo A (A bật: git config core.hooksPath .githooks)
   curl -s http://127.0.0.1:6335/collections   # so với HIEN_TRANG.md mục 1
   curl -s http://127.0.0.1:6335/collections/hue_full_corpus_7a2_e5_small_384 | grep -o '"points_count":[0-9]*'
   ```
3. Tên terminal, báo ngắn, lúc nào bắt đầu làm: bước 3 của `START_SESSION.md` (tin của A giao việc XÂY = "làm đi"; nghĩ, đếm 0 đồng, nêu hướng thì không chờ).

## 3. Nhận và làm việc

1. Đọc mục việc của mình và các input được ghi trong đó.
2. **Khai báo trước khi sửa:** ghi file sắp sửa vào `sessions/STATUS_<X>.md`; không sửa file session khác đang khai báo. Governance (`session_prompt/`,
   `skills/`, `AGENTS.md`, `.githooks/`, `.claude/settings.json`, `.claude/hooks/`) do A sửa — trừ sổ riêng `sessions/STATUS_<X>.md` của mình. Code làm trong `git worktree` riêng (lệnh + luật máy dùng chung: `AGENTS.md` mục "Hay vấp").
   Thêm cho máy dùng chung: cổng hue_rag là Qdrant 6335 / 6336, server 8010 + cổng tạm 8011–8099 / 8887 (`ss -ltn | grep <cổng>` trước khi mở); việc
   ≥ ~2 GB RAM hoặc ≥ 10 phút CPU ⇒ báo A trước (A nhắn phiên điều phối dự án kia). File nhiều session cùng ghi: đọc lại ngay trước khi sửa, sửa từng đoạn.
3. Làm theo mức rủi ro (bảng "sai thì mất gì": `guides/CACH_LAM_VIEC.md` mục 2). Việc CAO — Phase mới, sửa dữ liệu curated, xóa collection, provider /
   model mới, gửi dữ liệu ra ngoài — cần **một** tài liệu thiết kế User duyệt một lần, rồi report + review chéo độc lập + User đóng. Việc trong Phase đã
   duyệt: mục việc A ghi, report ngắn + review chéo, A đóng. Sửa chữ, cập nhật status, kiểm tra chỉ đọc: tự làm.
4. **Giảm rủi ro:** đích mới rồi mới cutover; commit trước sửa lớn; thứ nằm ngoài git còn giá trị (Qdrant collection) sao lưu trước khi sửa / xóa;
   liệt kê đích thật trước khi xóa, khác danh sách duyệt thì dừng; giới hạn tiền ghi trong việc. Đổi bảng dữ liệu mà bộ đo phụ thuộc (điểm lịch, lưu trú,
   quán…) ⇒ trước gộp quét tên / id mới trong nhãn mọi bộ đo đó và chạy mô phỏng nhãn không model (0 USD), ghi nhãn lệch vào report.
5. Thay đổi có đo trước–sau: ghi tiêu chí → đo hiện tại → sửa một thứ → đo lại cùng cách → kết luận tốt hơn / không đổi / kém hơn / chưa rõ (`run-experiment`).
6. **Chọn ảnh sẽ hiện cho người dùng:** ảnh phải tự nhận ra được nơi (biển tên, công trình đặc trưng, chú thích ghi đúng tên) — "nguồn chính thức" không
   đủ; bài món: đúng món là đủ; không trẻ em, không người rõ mặt làm trọng tâm, không số điện thoại. ≤ 10 ảnh ⇒ người giao tự chọn + một người khác review;
   > 10 ảnh ⇒ một agent con chọn + người giao nhìn lại 100 % ảnh sẽ hiện.
7. Bị chặn bởi permission của chính session: dừng, nhờ User chạy bằng `!` trong terminal đó; session khác không chạy hộ.

## 4. Tự kiểm trước khi bàn giao

1. Đọc exact diff (kể cả file untracked); mọi thay đổi thuộc phạm vi.
2. Chạy kiểm tra theo việc; `git diff --check`.
3. Bỏ code / test dư, abstraction phòng xa (skill `practical-project-coding`).
4. Ghi trung thực failed / skipped / partial / not verified.
   - (4b) Khẳng định về hành vi thư viện / định dạng log / rào bằng script ⇒ chạy một probe nhỏ thật (0 USD), ghi nhãn [Chạy] / [Code, chưa chạy];
     script / runbook có lượt trả phí ⇒ chạy thử mọi lệnh ở bản 0 USD trước khi đưa review.
   - (4c) Thêm lời dặn / công cụ **gắn theo cờ** ⇒ trước lượt có phí, một test cho **mỗi loại lượt** (lượt đầu, lượt hỏi lại, lượt ghép sau khi bấm nút,
     lượt có lịch sử) khẳng định chuỗi gửi model có / không có phần mới đúng như plan — test "cờ tắt giống byte" không đủ.
5. Viết report (§6), cập nhật `STATUS_<X>.md`, nhắn A.

## 5. Review chéo

Theo skill `risk-gated-agent-review` (cổng tối thiểu, mức `blocker` / `major` / `minor`, ba kết luận, khuôn finding). Report của người làm là chỉ mục bằng
chứng, không tự chứng minh PASS; người làm được phản biện bằng bằng chứng. Review dừng ngay khi A biết hướng / phụ thuộc sắp đổi.

- **Số vòng:** plan / spec tối đa 2 vòng (vòng 2 chỉ còn minor ⇒ A duyệt; còn blocker / major ⇒ A xem lại thiết kế). Code: một review cả nhánh. A đọc
  diff rồi gộp thẳng: nhánh chỉ đổi test · sửa ≤ 2 dòng theo minor đã nêu rõ cách đóng · nhánh ≤ 10 dòng, test tất định, không đổi câu người dùng thấy và
  không xử lý chữ người dùng / chuỗi gửi model (có một trong các thứ đó ⇒ review ≤ 5 dòng).
- Báo sha / "đã push" bằng dòng `ĐÃ PUSH …` của `scripts/commit_push.sh` (`AGENTS.md` mục "Hay vấp"; in `CHƯA PUSH — <lý do>` ⇒ chưa có gì lên origin).
  Gộp nhánh rồi `git push` tay ⇒ báo sha từ `git ls-remote`.

## 6. Report

- **Report của agent** nằm ở thư mục ngày `report_agent/<YYYY-MM-DD>/` (tên file mở đầu bằng vai; cách làm theo thư mục ngày: `guides/CACH_LAM_VIEC.md`
  mục 5): report việc xong của người làm · review của người kiểm · `TONG_HOP.md` của A. Dữ liệu chạy (kết quả, trace) để ở `data/` hoặc `/tmp`, report chỉ
  trỏ đường dẫn. `reports/` và `bao_cao_he_thong/` là hồ sơ cũ, không thêm file (`bao_cao_he_thong/` ngừng cập nhật từ 20/11/2026).
- **Mỗi việc xong** viết: một mục `bai_hoc/` + một dòng giới hạn (nếu có) + một dòng sổ việc; báo cáo kỹ thuật riêng khi có số đo.
- **Bài học cho User** (User không đọc code, **chỉ đọc `bai_hoc/`**): `bai_hoc/` ở gốc repo = đường đọc duy nhất của User (`README.md` = dàn bài + trạng
  thái). **Phạm vi = mọi việc đã làm**, không chỉ khái niệm: xây dựng, triển khai, phát triển, so sánh, tối ưu, đóng gói — việc mới vào hệ thống (kể cả thử
  rồi bỏ) ⇒ có chỗ trong một bài hoặc bảng tổng (bài 19). **Chỉ việc đã làm xong** (đang chạy, hoặc thử xong rồi bỏ); phần đang xây / chưa xong / chưa làm
  không đưa vào, làm xong mới viết bổ sung. **Độ dài** mỗi bài như bộ 0–19 — dễ hiểu, trọng tâm, không cắt ý quan trọng cho ngắn.
  Khuôn mỗi bài: tiêu đề → "Cập nhật lần cuối" (giờ `date`) → **bảng từ** (tên trong bài · tên gốc tiếng Anh dò lại trong code · nghĩa ngắn; từ User chưa
  gặp ghi "mới") → 1 câu nối bài trước → thân **bám sơ đồ RAG hai giai đoạn User đã biết** (bước này hue_rag làm gì → vì sao, đã thử gì → đo ra sao → khi
  nào hỏng; kể thẳng, không so "bản cơ bản ↔ hue_rag"), một ý, vì sao trước, hình ảnh nền xuyên suốt (người hướng dẫn viên tra sổ tay), ≤ 3 từ mới;
  **mỗi con số kèm: đo gì, đo thế nào, so với mốc nào, vì sao ổn / chưa ổn** (User chưa tự đánh giá được số); một **"chuyện thật"** đã chạy →
  "Ba điều chính" → "Bài sau" → `<details>` Nguồn (đường dẫn + nhãn [code] / [đã chạy] / ví dụ tự đặt). Xưng "mình", gọi User "anh"; sơ đồ khi cần bằng mermaid
  (≤ 6 ô). Thân bài không mã việc / sha / đường dẫn; không câu hỏi kiểm tra, "nói lại bằng lời", áp lực sếp / hội đồng.
  Kiểm từng ý trên code / số đo trước khi viết; ý chưa đủ bằng chứng ⇒ viết nhẹ đúng mức đã biết; thấy câu sai ở bài User đã đọc ⇒ sửa ngay, ghi ở Nguồn,
  báo User. Chỉ thêm 1–2 dòng số ⇒ người viết đối chiếu số mới với report. **Bài mới hoặc sửa nhiều ⇒ trước commit một agent con ngữ cảnh mới đối chiếu
  từng số / khẳng định với nguồn gốc** (biên bản ở `data/`, sửa theo rồi mới commit). Hệ thống đổi ⇒ sửa bài bị chạm cùng đợt.
- **`bai_hoc/` luôn đúng thông tin mới nhất:** chỗ không còn đúng thì xoá hoặc viết lại, không để số / trạng thái cũ đứng như hiện tại; phương án đã thử
  và bỏ giữ gọn 1–3 dòng; số nào cũng có nguồn, không chắc ⇒ ghi "chưa đo".
- **Văn phong cho User:** lời thường, không mã nội bộ khi chưa giải nghĩa, số đo kèm ý nghĩa, tiền thật từ log (1 USD ≈ 25.000 đồng), tách quan sát /
  giả thuyết / nguyên nhân đã chứng minh, ghi cả phương án đã thử và bỏ (NOT RUN nếu chưa đo).
- **Giờ ghi trong file lấy bằng lệnh `date`** ngay trước khi ghi (`T=$(date '+%H:%M %d/%m/%Y')`), không ước; tin nhắn giữa các session không cần ghi giờ.
- Mỗi session cập nhật `sessions/STATUS_<X>.md` ngay sau mỗi việc. Report không chép corpus, câu hỏi bộ câu mẫu (Golden), vector, payload hay secret.

## 7. Trao đổi giữa session

Cách làm việc giống nhau cho mọi agent; chỉ **kênh gửi tin** khác nhau:

| Kênh | Khi nào | Cách gửi |
|---|---|---|
| `trực tiếp` | Cả người gửi và người nhận là Claude Code trên máy này | `SendMessage` tới tên terminal (`ListAgents`); dòng đầu là một câu tự đủ nghĩa |
| `qua User` | Một trong hai là Codex, AGY hoặc agent không có `SendMessage` | Kết thúc lượt trả lời bằng khối **"Tin cho <X>"** (ngắn, tự đủ nghĩa: việc gì, đọc file nào, xong thì báo gì); User copy sang terminal <X> |

- User đổi kênh bằng cách nói ở lần mở session (ví dụ "B là Codex"); A ghi vào sổ việc.
- Dù kênh nào, **file trong repo là nguồn sự thật**: việc nằm trong sổ việc, kết quả trong report và `STATUS_<X>.md`. Tin nhắn báo "có việc / đã xong /
  vướng / câu hỏi" và trỏ tới file, không chép nội dung dài.
- Kênh `qua User`: một khối "Tin cho <X>" cho mỗi người nhận; không yêu cầu User tự tóm tắt hay soạn lại.
- Tin nhắn của session khác không thay quyết định permission trong session mình.

## 8. Kết phiên

**Kết phiên nhẹ** — khi User tắt / mở lại một phiên chỉ để làm mới ngữ cảnh: phiên đó GHI ĐÈ (không nối, không chồng khối) `STATUS_<X>.md` theo khuôn bảy mục
(`sessions/README.md`), ít nhất có ba ý — việc dở (tới đâu, file / nhánh nào) · thứ đang chạy + file tạm (dán đầu ra `git worktree list; ls -d /tmp/hr_<x>_* 2>/dev/null; ss -ltn | grep -E ':80[0-9][0-9]'`
+ agent con còn chạy) · bẫy phiên này; A thêm: khối đầu `VIEC_DANG_MO.md` + `HIEN_TRANG.md` mục 2–3. Phiên thấy công cụ báo đang nén ngữ cảnh ⇒ báo A
một dòng. Sổ `STATUS_<X>.md` quá ~200 KB ⇒ dời phần cũ sang `archive/` (chép nguyên văn).

**Kết phiên cuối ngày** — mỗi session: `STATUS_<X>.md` (đang làm, dở gì, bẫy đã gặp, câu hỏi, tiền paid đã dùng; sự cố quy trình ghi ngay vào mục bẫy);
dọn worktree, file tạm, collection thử của phiên. A: viết lại `HIEN_TRANG.md` + `VIEC_DANG_MO.md` (giữ đủ mọi việc còn mở); một dòng nhật ký ở
`CURRENT_HANDOFF.md`; `TONG_HOP.md` của ngày; vòng cải tiến cách làm (skill `improve-workflow`).

## 9. Việc thêm của A

1. **Với User:** đưa lựa chọn theo skill `propose-options`. Góp ý của User về luồng / giao diện có hơn một cách hiểu ⇒ hỏi lại MỘT câu, mỗi phương án tả
   người dùng thấy gì; chỉ có một nghĩa thì làm luôn. Việc rủi ro cao: **một** tài liệu thiết kế trong `docs/superpowers/specs/` (mục tiêu, quyết định,
   phạm vi, tiêu chí nghiệm thu, quyền, rủi ro), User duyệt một lần; có agent, công cụ, dữ liệu hay đường ra mới thì kèm bảng rà khung AI FDE. **Duyệt
   gắn với đúng bản:** A tính sha từ file (`sha256sum <file> | cut -c1-12`) lúc ghi duyệt; sửa sau duyệt mà đổi tiêu chí / ngưỡng / tiền / phạm vi ⇒ duyệt
   lại phần đổi. Plan có lượt trả phí > ~0,05 USD hoặc chạm an toàn: ghi ngay có bộ kín hay không; một session khác người viết đọc trước khi A ghi duyệt.
2. **Giao việc:** mở đầu bằng quyết định nào đang chờ kết quả này, rồi kết quả cần có, đọc gì, tiêu chí, quyền / giới hạn tiền, điều kiện dừng; ghi sổ
   việc rồi nhắn session đó. Giao song song khi file không chồng nhau. Tin giao việc kèm `notify_when_idle: true` để bắt session **kẹt** (chờ permission,
   vòng chờ hỏng) — session rảnh là bình thường, không dựng việc phụ để lấp giờ. Giao việc kế cho session đang bận ⇒ ghi "làm ngay sau việc hiện tại".
   User vừa nói đi vắng ⇒ giao B, C, E **trước** rồi mới mở hộp hỏi User. Giao việc thiết kế cho Phase n ⇒ đưa mọi tài liệu cũ cùng Phase vào mục "Đọc"
   (`find guides docs/superpowers/specs docs/superpowers/plans -maxdepth 1 -iname "*phase[-_]n[-_.]*"`). Có lượt đo tốc độ đang chạy ⇒ session khác không
   chạy lượt trả phí hay việc nặng CPU cùng lúc.
3. **Chi tiết kỹ thuật trong phạm vi:** A tự quyết, ghi lý do; hỏi User khi bằng chứng đi ngược một quyết định trước (và các việc ở `Session_Prompt.md` §1).
4. **Đóng việc:** review chéo đạt → trình User (kết quả, bằng chứng, giới hạn) với việc cần User đóng; việc trung bình / thấp A tự đóng và báo. Phase trước
   đóng xong mới thiết kế Phase sau — không thiết kế trước như đã biết kết quả của Phase mà nó phụ thuộc.
5. **Giữ tài liệu:** sổ việc chỉ giữ việc đang mở (việc xong dời một dòng sang `VIEC_DA_XONG.md`).
6. **Git:** sau khi User đồng ý một lệnh, A **tự chạy**; đưa User lệnh `!` khi bị chặn / lỗi, hoặc với việc luật ghi "User `!`" (xoá nhánh, xoá dữ liệu).
   Stage **từng file đã review** (không `git add <thư mục>` hay `-A`); không commit dữ liệu private. Nhánh xong việc: A đề xuất xóa ở báo cáo kết phiên
   (danh sách + còn gì chỉ nằm trên nhánh); nhánh hồ sơ gắn tag `hoso/<tên>` trước khi xóa; xóa khi User duyệt.
7. **A tự thử kỹ thuật** trong `git worktree` riêng (`/tmp/hr_a_…`); việc A tự làm vẫn để phiên khác kiểm.
7b. **Vòng tự soi** (`Session_Prompt.md` §7): A mở MỘT vòng mỗi ngày khi mỗi session đã có kết quả đầu tiên; ghi chốt vào `CURRENT_HANDOFF.md`.
8. **Quyền thường trực:** bảng trong `AGENTS.md`, A không hỏi quyền lúc mở phiên. Quyền RIÊNG cho một việc thuộc hàng "hỏi User trước" User cấp lúc
   được hỏi; A ghi sổ việc kèm giờ, dùng cho đúng việc đó.
9. **Giao việc cho agent con:** theo skill `giao-viec-agent-con`; số của agent con chuyển cho User gắn `chưa kiểm` tới khi có người thứ hai tính lại.

## 10. Session D — học cùng User (tùy chọn)

Mở bằng `START_SESSION.md` với `<X>` = D khi User muốn tự hiểu một việc vừa xong; làm theo skill `teach-and-quiz` (chỉ đọc, chỉ ghi sổ học private
`data/hoc_cung_D/`, không mở câu kín) — trừ việc viết giáo trình ở đoạn dưới. Thêm: không ghi memory Claude (memory dùng chung mọi session); thấy chỗ yếu trong việc của phiên khác thì nói thẳng với
User, không tự sửa; D báo **User**, việc để giảng do User chọn.

**D viết GIÁO TRÌNH** (chủ dự án giao 16:46 21/11/2026: đổi `bai_hoc/` thành giáo trình đọc từ đầu, theo hình thức chủ dự án đã thấy ở một dự án khác của mình) — ngoại lệ DUY NHẤT của "D chỉ đọc": D được viết trong `bai_hoc/giao_trinh/` (chỉ thư mục đó), ở worktree + nhánh riêng (`AGENTS.md` mục "Hay vấp"), commit + push nhánh đó bằng `scripts/commit_push.sh`; D không gộp vào `main`. Các giới hạn khác của D giữ nguyên (không sửa code, luật, bài hiện có; không chạy việc nặng, không API trả phí, không câu kín, không ghi memory).
Dàn bài + khuôn bài do chủ dự án duyệt với D. Khuôn mới thay phần HÌNH THỨC của mục 6 (thứ tự mục, tiêu đề); luật NỘI DUNG của mục 6 vẫn áp: chỉ việc đã làm xong · mỗi con số kèm đo gì, so với mốc nào, vì sao ổn / chưa ổn · từ mới kèm nghĩa · thân bài không mã việc / sha / đường dẫn · kiểm từng ý trên code / số đo, chưa đủ bằng chứng thì viết nhẹ · giờ lấy bằng `date`. Khuôn mới muốn có thứ mục 6 đang loại (câu hỏi tự kiểm, "nói lại bằng lời") ⇒ D hỏi chủ dự án lúc duyệt khuôn. Đích để xếp bài: chủ dự án tự demo, tự trình bày cả bức tranh và trả lời câu hỏi của giảng viên (`HIEN_TRANG.md` mục 4, dòng "ĐÍCH CỦA ĐỒ ÁN").
Từ dự án khác chỉ lấy HÌNH THỨC (chặng, khuôn bài, cách chia đường chính ↔ mở rộng), viết lại bằng chữ của mình — không chép nguyên văn file mẫu; nội dung, ví dụ, tên riêng, đường dẫn, số liệu của dự án đó không vào file tracked, tên nhánh hay lời commit (luật cứng 2). Ghi chép khi bàn với phiên của dự án kia chỉ để ở `data/hoc_cung_D/`; không gửi sang đó `data/`, câu kín hay bộ câu của hue_rag.
Bộ `bai_hoc/` hiện có giữ nguyên để tra cho tới khi đường chính của giáo trình đủ; việc mới xong các phiên vẫn ghi vào bộ hiện có như cũ, D lấy từ đó. Phần hệ thống đang đổi (trợ lý có công cụ, model viết) viết sau khi lắng — hiện trạng ở `HIEN_TRANG.md` mục 1 và `bai_hoc/BAN_DO_DU_AN.md`. Trước khi gộp mỗi bài: một agent con ngữ cảnh mới (hoặc phiên đã xây phần đó, khi có điểm tranh cãi) đối chiếu số và khẳng định với code / số đo. Nhánh sẵn thì D nhắn thẳng phiên điều phối (ngoại lệ của "D báo User"); phiên điều phối đọc diff, gộp, và thêm một dòng trỏ trong `bai_hoc/README.md`.
