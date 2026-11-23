# Guide 5 — Kiểm từ ngoài, gỡ lỗi, và buổi diễn tập trước ngày cần dùng

Viết: 20:27 23/11/2026, phiên đo. **Chưa bước nào của guide này từng chạy trên địa chỉ AWS thật** — bộ deploy chưa dựng lần nào. Những gì đã có số thật,
đều ở máy chủ dự án: (a) model của bản deploy (`gpt-6-luna`) chạy đúng bản code này qua đường stream của server, không qua hộp Caddy — lượt đo bù tối
23/11/2026: kịch bản 10 bước 0 bước hỏng, một lượt trình duyệt, 17 ca tính năng; các con số "thấy đúng thì trông thế nào" trong guide lấy từ lượt đó;
(b) gói ba hộp có Caddy chạy trọn ở máy với khoá giả (guide 4) — tức đường "Caddy ⇒ app" đã chạy, nhưng chưa cùng lúc với model thật của OpenAI.
Mọi thứ còn lại — HTTPS thật, đi qua internet, máy AWS — là **[chưa kiểm trên AWS]**; buổi diễn tập ở mục 6b sinh ra để đổi các dòng đó thành "đã kiểm".

Từ dùng: **kiểm từ ngoài** = thử từ một máy KHÁC máy chủ, qua internet, như người dùng thật · **hộp** = container · **cửa vào** = hộp Caddy · **lượt** = một
lần gửi câu hỏi (hoặc một ảnh) có gọi model · **trang theo dõi** = trang `#/theo-doi` cho chủ dự án xem số lượt, token, tiền · **sổ vết** = bản ghi debug
từng lượt, có chữ người dùng gõ.

## 1. Mục tiêu

Sau guide này chủ dự án biết chắc bản deploy DÙNG ĐƯỢC như bản ở máy mình — không chỉ "đã lên" — và khi có gì trông như hỏng thì biết xem ở đâu, làm gì.

## 2. Sẽ có gì

Không dựng thêm tài nguyên nào. Guide này cho ba thứ:

| Thứ | Ở đâu | Dùng lúc nào |
|---|---|---|
| Danh sách kiểm từ ngoài, 12 dòng tick | mục 6 | sau lần bật đầu (guide 4), sau mỗi lần cập nhật bản mới (guide 6 mục 6.3) |
| Bảng "thấy gì ⇒ xem gì ⇒ làm gì" | mục 8 | khi có gì trông như hỏng |
| Buổi diễn tập (khoảng một giờ, dưới 1 USD tiền máy) | mục 6b | một lần, vài ngày trước ngày cần dùng thật |

Thói quen ngắn trước MỖI buổi demo (bật máy, một câu hỏi thật, một lượt xếp lịch) nằm ở guide 6 mục 6.2 — guide này không lặp lại.

## 3. Điều kiện trước

- Guide 4 xong: ba hộp chạy, `https://<site_name>` mở được, một câu hỏi thật đã có câu trả lời.
- Có một máy KHÁC máy chủ để thử (máy của chủ dự án là được) và một điện thoại dùng mạng di động (tắt Wi-Fi) cho một dòng của danh sách.
- Còn tiền nạp ở tài khoản OpenAI: cả danh sách tốn khoảng 15–20 lượt hỏi (ở máy chủ dự án, 9 lượt của kịch bản demo tốn 0,007 USD).

## 4. File liên quan

| File | Vai trò ở guide này |
|---|---|
| `deploy/guides/4_bat_lan_dau.md` | lệnh vào máy, lệnh xem log, bảng gỡ lỗi của lần bật đầu — guide này không chép lại |
| `deploy/guides/6_ngay_demo.md` | dừng / bật máy (dùng ở dòng 11 của danh sách), cập nhật, lùi bản, nút khẩn cấp |
| `deploy/docker/Caddyfile` | cửa vào: trần cỡ thân yêu cầu 12 MB, dòng `flush_interval -1` |
| `deploy/docker/compose.yml` | trần log mỗi hộp (3 file × 10 MB), các biến trần lượt |
| `guides/RUNBOOK_BAN_GIAO.md` mục 10 | **giới hạn đã biết của sản phẩm** — gặp hành vi lạ thì tra ở đó TRƯỚC khi coi là lỗi deploy |
| trên máy chủ: `/srv/hue/hue.env`, `/srv/hue/hue.khoa.env`, `/srv/hue/logs/` | cấu hình không bí mật · khoá · log và số đo từng lượt của app |

## 5. Cấu hình

Ở máy mình, mỗi cửa sổ lệnh mới:

```bash
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
SITE=<site_name>          # giá trị `terraform output -raw site_name` của guide 3, ví dụ 13-250-1-2.sslip.io
ID=$(cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu && terraform output -raw instance_id); echo "$ID"
```

Trên máy chủ (vào bằng lệnh ở guide 4 bước 1), viết tắt lệnh compose cho đỡ dài:

```bash
sudo -i
cd /srv/hue
dc() { docker compose --env-file hue.env -f compose.yml "$@"; }      # gõ lại dòng này mỗi lần mở phiên mới
```

## 6. Từng bước — danh sách kiểm từ ngoài

Làm từ máy mình, theo thứ tự (dòng 10 ăn hết lượt của ngày nên đứng gần cuối). Mỗi dòng có phần phải ĐỌC, không chỉ "có trả lời": sáng 23/11/2026 một
lượt thử kiểu "dùng như người thật" tìm ra ba lỗi mà 761 ảnh chụp + 50 bước chạy bằng script đều cho qua, vì script chỉ kiểm "có lịch, đủ điểm".

**Dòng 1 — trang mở, chứng chỉ thật.** Mở `https://$SITE` bằng trình duyệt. Mong: ổ khoá hợp lệ, màn đầu hiện trọn. Bằng lệnh:

```bash
curl -s "https://$SITE/health"                                         # mong: {"status":"ok", … năm thành phần ready / alive}
curl -s -o /dev/null -w '%{http_code}\n' "https://$SITE/docs"           # mong: 404 (trang tài liệu API đã tắt)
```

**Dòng 2 — một câu hỏi có nguồn, chữ CHẠY DẦN.** Trang Trợ lý, gõ `Lăng Tự Đức có gì đặc biệt?`. ĐỌC: câu trả lời nói về hồ Lưu Khiêm / Khiêm Lăng…, có
khối "Nguồn đã dùng (2 bài)" bấm mở được; chữ hiện dần từng cụm chứ không phải cả đoạn một lần. Ở máy chủ dự án (không qua Caddy, không qua internet): dòng
trạng thái hiện sau 0,6 giây, chữ đầu tiên sau khoảng 3 giây, xong ở khoảng 4,5 giây; qua internet sẽ chậm hơn — chậm hơn nhiều lần mới là dấu hiệu.

**Dòng 3 — câu ngoài phạm vi bị từ chối.** Gõ `Ở Hội An có quán cao lầu nào ngon?`. Mong: "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế…" (ở máy
chủ dự án: 1,7 giây). Được trả lời bằng tên quán ⇒ ghi lại nguyên văn, báo nhóm (không phải lỗi deploy, là sàn của sản phẩm).

**Dòng 4 — xếp một lịch thật.** Trang Lên kế hoạch ⇒ `Xếp lịch 2 ngày`. ĐỌC thẻ lịch:
- mỗi điểm có một câu tả là câu thật — KHÔNG có điểm nào mà cả dòng chỉ là `<tên điểm> — điểm <loại> [<mã nguồn>].` (đó là câu dự phòng khi model không trả câu tả; `<loại>` là một hay vài chữ trong: di tích, ẩm thực, thiên nhiên, lễ hội, nghệ thuật, chụp ảnh — nên đừng dò đúng một chuỗi cố định);
- bữa trưa và bữa tối có quán; mỗi tối có một mục buổi tối (lịch mặc định: phố đi bộ Nguyễn Đình Chiểu, rồi Bến Trăng Café & Bar);
- bản đồ có ghim; khung nguồn mở được.
Câu dự phòng xuất hiện ở MỌI điểm ⇒ mục 8, dòng "lịch toàn câu dự phòng".

**Dòng 5 — sửa lịch bằng lời, rồi hỏi lại.** Mở khung trợ lý ở góc trang Lên kế hoạch, gõ `Bỏ điểm đầu tiên của ngày 2`. Mong: "Đã bỏ <tên điểm>." và
dòng đầu thẻ lịch đổi theo. Gõ tiếp `Vậy ngày 2 giờ còn những điểm nào?`. ĐỌC: danh sách trợ lý kể phải KHỚP thẻ lịch đang hiện (lỗi "kể sai điểm vừa
bỏ" tìm ra và sửa tối 23/11/2026 — bản deploy dựng từ commit cũ hơn `73dae1f3` sẽ còn lỗi này).

**Dòng 6 — tải file lịch.** Dưới thẻ lịch bấm `Tải PowerPoint`. Mong: file tải về mở được, khoảng nửa MB. (Nút `Tải về (.txt)` đã bỏ từ tối 23/11/2026 theo
lời chủ dự án; bản deploy dựng từ commit cũ hơn thì còn nút đó.)

**Dòng 7 — hỏi bằng ảnh qua HTTPS.** Trang Trợ lý ⇒ nút dấu cộng "Hỏi bằng ảnh" ⇒ chọn một ảnh Cầu Trường Tiền (ảnh tự chụp hoặc tải về) ⇒ gõ `địa điểm
này là gì` ⇒ bấm `Hỏi` MỘT lần. Mong: có câu trả lời ngay, mở đầu bằng dòng "Mình đoán trong ảnh là Cầu Trường Tiền — có thể sai."; dưới câu trả lời có nút
`Không phải — tôi gõ tên` (ảnh ra hai ba tên thì có thêm nút `Hỏi lại với: <tên kia>`). KHÔNG còn thẻ nào bắt chọn hay xác nhận tên trước khi trả lời
(luồng đổi tối 23/11/2026 theo lời chủ dự án — bản deploy dựng từ commit cũ hơn `6ab1380f` vẫn hiện thẻ cũ). Ảnh của nơi không có trong danh sách 55 tên
ra "chưa nhận ra" hoặc bị đoán sang một tên giống nó là giới hạn đã biết (runbook 10.1), không phải lỗi deploy.

**Dòng 8 — một tin dài nhiều ý, từ ngoài.** Đây là phép thử "cửa vào chờ được bao lâu". Gõ: `Gia đình mình 4 người có ông bà lớn tuổi đi Huế 2 ngày: Đại
Nội mở cửa mấy giờ và vé bao nhiêu, trưa ăn gì gần Đại Nội, tối nên đi đâu cho nhẹ nhàng?`. Mong: câu trả lời TRỌN (đủ các ý hoặc nói rõ ý nào tư liệu
chưa có), không đứt giữa chừng, không màn hình lỗi. Ở máy chủ dự án, tin nhiều ý trên model này mất khoảng 13 giây (trung vị bộ 41 câu khó). Cửa vào
Caddy theo tài liệu không đặt hạn giờ cho câu trả lời chậm (chỉ hạn 3 giây lúc NỐI tới app) [tài liệu Caddy — bản tra cứu 23/11/2026, riêng tư `data/tra_cuu_cli/2026-11-23_aws-pha-sach-va-kiem-sau-deploy/ket_qua.md`; chưa tự đo] — khác cổng
API 29–30 giây chủ dự án đã gặp hai lần ở khoá học; gói này không có cổng đó.

**Dòng 9 — thân quá cỡ ⇒ 413.** Cửa vào cắt mọi yêu cầu có thân trên 12 MB (ảnh hợp lệ tối đa 10 MB):

```bash
(printf '{"query": "'; head -c 13000000 /dev/zero | tr '\0' 'a'; printf '"}') | \
  curl -s -o /dev/null -w '%{http_code}\n' -X POST -H 'Content-Type: application/json' --data-binary @- "https://$SITE/api/chat"     # mong: 413
```

Lệnh này đã chạy ở máy chủ dự án trên gói ba hộp: ra 413, thân trả về rỗng (`deploy/docker/README.md` mục 5). Nó vẫn tính MỘT lượt vào số lượt trong ngày của địa chỉ đang thử.

**Dòng 10 — hết lượt ⇒ 429 có lời báo.** Trần mặc định là 50 lượt mỗi địa chỉ mỗi ngày — đừng hỏi 50 câu để thử. Hạ tạm trần xuống 3 trên máy chủ:

```bash
printf '\nHUE_LUOT_MOI_NGAY=3\n' >> hue.env && tail -n 2 hue.env     # NHÌN: dòng cuối phải là đúng  HUE_LUOT_MOI_NGAY=3  (đứng riêng một dòng)
dc up -d app                                                        # tạo lại hộp app: bộ đếm về 0, MẤT mọi cuộc trò chuyện đang mở
```

Từ máy mình hỏi bốn câu bất kỳ trên trang. Mong: ba câu đầu trả lời; câu thứ tư hiện "Bạn đã dùng hết số lượt hỏi hôm nay. Vui lòng quay lại vào ngày
mai." Rồi TRẢ LẠI trần cũ (bắt buộc — quên là cả buổi demo mỗi người chỉ hỏi được ba câu):

```bash
sed -i '/^HUE_LUOT_MOI_NGAY=3$/d' hue.env && dc up -d app && grep -c '^HUE_LUOT_MOI_NGAY=3$' hue.env     # mong: 0  (dòng thử đã mất; trần về như trước)
```

Bộ đếm lượt nằm trong bộ nhớ của hộp app: tạo lại hộp là đếm lại từ 0 **[đọc code, chưa thử trên gói]**.

**Dòng 11 — khởi động lại máy rồi hỏi lại.** Dừng và bật máy bằng hai khối lệnh ở guide 6 mục 6.1 và 6.2 (IP tĩnh giữ nguyên nên `$SITE` không đổi). Sau
khi `aws ec2 wait instance-status-ok` trả về: KHÔNG gõ gì trên máy, từ máy mình làm lại dòng 1 và dòng 2. Phép kiểm là MỘT CÂU HỎI THẬT, không phải
`/health`: hai sự cố đã thấy thật ở máy chủ dự án đều cho `/health` xanh trong khi mọi câu hỏi hỏng (khoá hỏng; app lên trước khi chỉ mục sẵn). Ghi lại
số phút từ lệnh bật máy tới câu trả lời đầu tiên — con số này guide 6 đang để "chưa đo".

**Dòng 12 — từ điện thoại, mạng di động.** Tắt Wi-Fi, mở `https://$SITE`, hỏi một câu. Mong: trang vừa màn hình, chữ chạy dần. Dòng này bắt loại lỗi mà
thử từ cùng một mạng không thấy: tường lửa, chứng chỉ, tên miền chỉ phân giải được ở mạng nhà.

Tick xong cả 12 dòng ⇒ ghi ngày giờ + mã commit của ảnh đang chạy (`grep HUE_GIT_SHA /srv/hue/hue.env`) vào sổ của mình.

## 6b. Buổi diễn tập — "guide 5b" của dàn ý (nên làm một lần, vài ngày trước ngày cần dùng)

Mục đích: lần ĐẦU TIÊN bộ deploy chạm AWS thật không được rơi vào đúng ngày demo. Buổi này do chủ dự án gõ; nhóm đọc đầu ra và sửa guide theo đó.

| Bước | Làm gì | Guide | Ghi lại |
|---|---|---|---|
| 1 | Dựng tầng nền (nếu chưa) và tầng máy chủ | 1, 3 | `apply` mất mấy phút; có dòng `AccessDenied` nào không (chép nguyên văn) |
| 2 | Đẩy gói, bật lần đầu, hỏi một câu thật | 2, 4 | từ `apply` xong tới câu trả lời đầu: mấy phút; chứng chỉ HTTPS có sau bao lâu |
| 3 | Danh sách kiểm từ ngoài, ít nhất dòng 1, 2, 4, 5, 8, 11 | guide này, mục 6 | giây tới chữ đầu tiên (dòng 2); tin dài mất mấy giây, có bị cắt không (dòng 8); phút từ lúc bật máy tới câu trả lời (dòng 11) |
| 4 | Báo động máy hỏng có tới email không — ÉP báo động kêu thử bằng lệnh dưới bảng (dừng một hộp hay dừng cả máy đều KHÔNG làm nó kêu) | mục 7 dưới | thư của báo động có tới hộp thư trong khoảng một phút không |
| 5 | Phá tầng máy chủ, kiểm IP tĩnh đã trả | guide 7, Bước 3 | `destroy` mất mấy phút; hai lệnh kiểm in gì |

Lệnh của bước 4 (từ máy mình) — ép báo động sang trạng thái kêu để xem đường "báo động ⇒ chủ đề ⇒ email" có thông không **[chưa chạy trên AWS]**:

```bash
aws cloudwatch set-alarm-state --alarm-name hue-rag-may-khong-qua-kiem-tra-trang-thai --state-value ALARM --state-reason "thu bao dong"
```

Mong: một thư của AWS tới email cảnh báo trong khoảng một phút; ở lần đánh giá kế (trong vòng năm phút) báo động tự về trạng thái bình thường vì máy
vẫn khoẻ — xem bằng `aws cloudwatch describe-alarms --alarm-names hue-rag-may-khong-qua-kiem-tra-trang-thai --query 'MetricAlarms[0].StateValue'`
(in `ALARM` ngay sau lệnh ép, rồi `OK`). Không có thư ⇒ xem email đã bấm xác nhận đăng ký chưa (guide 1 mục 7) và `alert_topic_arn` đã điền ở guide 3
chưa; đủ cả hai mà vẫn không có ⇒ báo nhóm: đó chính là trường hợp chủ đề cần thêm quyền cho báo động. Lệnh ép báo `AccessDenied` ⇒ chép nguyên dòng
lỗi cho nhóm (quyền `cloudwatch:SetAlarmState` trong tờ quyền của guide 0 chưa từng được thử trên tài khoản thật). Vì sao phải ép: báo động này đo phép
kiểm trạng thái của MÁY; hộp app chết thì máy vẫn "ok", còn máy dừng thì không có số đo và báo động coi là bình thường — không thao tác nào ở guide 6 làm nó kêu.

Tiền máy của cả buổi (máy bật một hai giờ): dưới 1 USD [ước theo bảng giá ở guide 3]; cộng vài xu OpenAI. Tầng nền để lại — nó gần như không tốn tiền,
và lần dùng thật chỉ còn phải làm guide 3 ⇒ 4.

Sau buổi diễn tập, nhóm chép SỐ THẬT vào các guide và gạch chữ **[chưa kiểm trên AWS]** ở đúng những dòng đã thấy chạy: guide 3 (thời gian dựng, máy
"Online"), guide 4 (tải gói bằng vai gắn máy, chứng chỉ, câu hỏi thật qua OpenAI), guide 6 (thời gian bật lại), guide 7 Bước 3, và ba con số ở dòng 2,
8, 11 của guide này. Dòng nào chưa đi qua thì GIỮ nhãn.

Một điều phải biết trước khi dựng đi dựng lại nhiều lần: tổ chức cấp chứng chỉ miễn phí giới hạn 5 chứng chỉ cho cùng MỘT tên trong 7 ngày, và 5 lần
xác thực hỏng cho một tên mỗi giờ [Let's Encrypt — bản tra cứu 23/11/2026, chưa tự mở]. Mỗi lần dựng lại tầng máy chủ là một IP tĩnh mới ⇒ một tên
`sslip.io` mới, nên diễn tập một hai lần không chạm giới hạn; dùng tên miền riêng thì mỗi lần dựng lại máy tính một chứng chỉ vào hạn mức 5 cái đó.

## 7. Kiểm — theo dõi lúc chạy

Bản deploy này cố ý ít thứ để nhìn hơn dự án khoá học: không bảng CloudWatch, không đẩy log lên CloudWatch. Bảng dưới nói "ở khoá học nhìn ở đâu ⇒ ở
hue_rag nhìn ở đâu":

| Muốn biết | Ở dự án khoá học | Ở hue_rag |
|---|---|---|
| Số lượt, token, tiền theo ngày | bảng CloudWatch / trang của nhà cung cấp | trang theo dõi `https://$SITE/#/theo-doi` (chỉ mở khi đã đặt `HUE_KHOA_THEO_DOI` trong `hue.khoa.env` — guide 4 mục 5) + trang sử dụng của OpenAI |
| Log của ứng dụng | CloudWatch Logs | trên máy, qua Session Manager: `dc logs --tail 80 app` (hoặc `caddy`, `qdrant`); số đo từng lượt: các dòng `chat_metrics` trong `/srv/hue/logs/application.log` |
| Máy còn sống không | — | MỘT báo động "máy không qua kiểm tra trạng thái trong 10 phút" gửi email (tạo cùng tầng máy chủ khi đã điền `alert_topic_arn`) |
| Trang còn trả lời không | — | không có gì tự báo ⇒ một câu hỏi thật trước mỗi buổi (guide 6 mục 6.2) |

Báo động máy hỏng KHÔNG thấy ba thứ hay hỏng nhất — khoá OpenAI hết tiền / bị thu hồi, hộp app chết trong khi máy vẫn khoẻ, chứng chỉ không xin được —
vì với AWS máy vẫn "ok". Nó chỉ bắt được chuyện máy treo hẳn. Báo động có gửi được vào chủ đề email của tầng nền với thiết lập mặc định hay không:
**[chưa kiểm trên AWS, chưa tra được nguồn chính thức nói chắc]**; phép thử là bước 4 của buổi diễn tập (mục 6b) — ép báo động kêu rồi xem thư (tên báo động:
`hue-rag-may-khong-qua-kiem-tra-trang-thai`; trạng thái hiện tại: `aws cloudwatch describe-alarms --alarm-name-prefix hue-rag- --query 'MetricAlarms[].[AlarmName,StateValue]' --output text`).

Trang theo dõi: gõ sai khoá nhiều lần thì trang khoá 15 phút và báo "Nhập sai khoá quá nhiều lần. Chờ 15 phút rồi thử lại." — là rào có chủ ý, không
phải lỗi; chờ, hoặc tạo lại hộp app (`dc up -d --force-recreate app`, mất các cuộc đang mở) **[đọc code: bộ đếm nằm trong bộ nhớ; chưa thử]**.

Sổ vết trên máy deploy: mặc định TẮT và nên để tắt — nó ghi nguyên chữ người dùng gõ. Chỉ bật tạm khi cần lần một lỗi không hiểu được từ log:
thêm dòng `HUE_SO_VET=true` vào `hue.khoa.env` rồi `dc up -d app`; tái hiện lỗi; đọc ngay trên máy
`dc exec app sh -c 'tail -n 1 /app/data/debug_trace/*.jsonl'`; xong thì xoá dòng đó và `dc up -d app` — hộp được tạo lại nên file sổ vết mất theo
(nó không nằm ở thư mục nào gắn ra đĩa máy) **[đọc code và file compose; chưa thử trong hộp]**. Không chép file đó ra khỏi máy chủ.

## 8. Gỡ lỗi

Trước hết: **tra `guides/RUNBOOK_BAN_GIAO.md` mục 10** — nhiều thứ trông như lỗi là giới hạn đã biết của sản phẩm và có ở cả bản local. Bảng gỡ lỗi của
lần bật đầu (tải gói, băm, file khoá, chỉ mục, chứng chỉ) ở guide 4 mục 8; bảng dưới là các tình huống LÚC ĐANG CHẠY.

| Thấy gì | Xem gì | Làm gì |
|---|---|---|
| Mọi thứ xanh (`/health` `ok`, ba hộp khoẻ) mà câu nào cũng "Không thể tạo câu trả lời vào lúc này" | trang quản lý OpenAI: khoá còn không, còn tiền nạp không; trên máy `grep -n '^  provider:' /srv/hue/cau_hinh/settings.yaml` phải ra `openai` | sửa `hue.khoa.env` (hoặc nạp tiền) rồi `dc up -d app` — lệnh `restart` KHÔNG nạp lại file khoá. `/health` không gọi model nên không bao giờ thấy lỗi này |
| Một câu ra "Không thể tạo câu trả lời vào lúc này" kèm nút "Thử lại", câu sau lại được | OpenAI lỗi thoáng qua; app đã tự gọi lại một lần trước khi báo | bấm "Thử lại". Lặp nhiều lần liền: đếm dòng lỗi `grep -c openai_loi /srv/hue/logs/application.log` và xem trang trạng thái của OpenAI |
| Câu nào cũng lỗi "Hệ thống tra cứu tạm thời không khả dụng", không tự hồi | hộp Qdrant: `dc ps`; log app có lặp "chờ Qdrant có collection…" không | `dc up -d` (bật lại hộp nào đang tắt, theo đúng thứ tự) rồi `dc restart app` — `up -d` KHÔNG khởi động lại một hộp app đang chạy mà kẹt ở trạng thái lỗi; chưa nạp chỉ mục ⇒ guide 4 bước 8 |
| Lỗi "Dữ liệu tra cứu cần được lập chỉ mục lại" (409) | chỉ mục trong hộp Qdrant không khớp kho trong ảnh — thường do nạp bản chụp của gói KHÁC commit với ảnh | nạp lại chỉ mục của đúng gói đang chạy: guide 4 bước 8 |
| Chữ không chạy dần, cả câu hiện một lần | `grep -n flush_interval /srv/hue/Caddyfile` phải còn dòng `flush_interval -1`; thử thêm từ một mạng khác (vài mạng công ty / trường gom luồng) | lấy lại `Caddyfile` của gói (chép đè file trên máy bằng bản trong gói, đừng sửa tay) rồi `dc up -d --force-recreate caddy`. Chỉ `dc up -d caddy` thì KHÔNG đủ: nội dung một file gắn vào hộp đổi không làm Compose tạo lại hộp — lệnh in `Running` và Caddy vẫn chạy bản cũ [thử thật ở máy 23/11/2026 với một hộp Caddy riêng: `up -d` giữ bản cũ, `--force-recreate` mới nhận bản mới]. Chủ dự án đã gặp đúng triệu chứng này ở tuần 1 của khoá học |
| Tin dài đứt giữa chừng hoặc ra màn hình lỗi sau một quãng chờ | `dc logs --tail 80 caddy` và `dc logs --tail 80 app` ở đúng phút đó | chép hai đoạn log cho nhóm. Cửa vào không đặt hạn giờ cho câu trả lời chậm, nên nếu bị cắt đều ở một số giây cố định thì thủ phạm thường là mạng ở giữa — thử lại từ mạng di động |
| Lịch toàn câu dự phòng ở MỌI điểm (câu chỉ gồm `<tên điểm> — điểm <loại> [<mã nguồn>].`, không có câu tả nào; `<loại>` là một hay vài chữ trong: di tích, ẩm thực, thiên nhiên, lễ hội, nghệ thuật, chụp ảnh) | lời gọi model của lượt xếp lịch hỏng — cùng nguyên nhân với dòng đầu bảng | xử lý như dòng đầu; một hai điểm có câu dự phòng thì là giới hạn đã biết (runbook 10.2) |
| "Bạn đã dùng hết số lượt hỏi hôm nay…" (429) | `grep HUE_LUOT /srv/hue/hue.env` — còn dòng `HUE_LUOT_MOI_NGAY=3` của phép thử dòng 10 không | xoá dòng thử; cần nới thật thì đặt số mới trong `hue.env` rồi `dc up -d app`. Nhiều người sau cùng một mạng (một phòng học) chung MỘT địa chỉ ⇒ chung trần 50 |
| "Hôm nay trợ lý đã nhận đủ số lượt hỏi cho phép…" | trần tổng cả máy (`HUE_LUOT_TONG_MOI_NGAY`, mặc định 500) đã chạm | xem trang theo dõi: có ai đang hỏi dồn không; nới bằng `hue.env` + `dc up -d app` nếu là dùng thật |
| Tải lại trang là mất cuộc trò chuyện và lịch; mở trang ở tab thứ hai thì tab thứ nhất mất cuộc | chủ ý của sản phẩm — cuộc trò chuyện và lịch chỉ nằm trong bộ nhớ (runbook 10.3) | không sửa; khi demo dùng MỘT tab |
| Thẻ lịch còn trên màn hình nhưng lệnh sửa lịch bị trả lời như câu hỏi thường | hộp app vừa được tạo lại (cập nhật, đổi cấu hình, khởi động lại máy) giữa cuộc | xếp lại lịch. Vì thế không `dc up -d app` giữa buổi demo |
| Ảnh hợp lệ mà báo quá cỡ | ảnh trên 10 MB (trần của app) hoặc yêu cầu trên 12 MB (trần của cửa vào) | dùng ảnh nhỏ hơn; ảnh điện thoại thường 3–8 MB |
| Trang trắng trên một điện thoại cũ | trình duyệt quá cũ (Safari trước 15.4) | giới hạn đã biết (runbook 10.3) — dùng máy khác |
| Console của trình duyệt có đúng một lỗi `favicon.ico` 404 | vô hại, có ở mọi bản | bỏ qua |
| Trang chậm bất thường, câu đơn mất trên 20 giây | trên máy: `docker stats --no-stream` (bộ nhớ từng hộp: app khoảng 0,9 GB, Qdrant khoảng 0,2 GB là bình thường — số của lượt thử gói ở máy chủ dự án) và `free -m` | bộ nhớ sát trần ⇒ `dc restart app` (khởi động lại hộp app, khoảng 15–40 giây mới khoẻ; MẤT các cuộc trò chuyện và lịch đang mở). `dc up -d app` không làm gì khi cấu hình không đổi; lặp lại ⇒ báo nhóm kèm đầu ra hai lệnh |
| Không vào được máy bằng Session Manager | `aws ssm describe-instance-information --query 'InstanceInformationList[].[InstanceId,PingStatus]' --output text` phải có dòng `Online`; `aws ec2 describe-instance-status --instance-ids "$ID" --include-all-instances --query 'InstanceStatuses[].[InstanceState.Name,InstanceStatus.Status,SystemStatus.Status]' --output text` phải ra `running ok ok` | máy đang dừng ⇒ bật (guide 6 mục 6.2); `running` mà không `Online` sau 10 phút ⇒ bảng gỡ lỗi của guide 3 |
| Trình duyệt báo chứng chỉ không hợp lệ sau một lần dựng lại máy | `dc logs --tail 80 caddy`; `HUE_SITE` trong `hue.env` có còn là tên của IP tĩnh HIỆN TẠI không | IP tĩnh mới ⇒ tên `sslip.io` mới ⇒ sửa `HUE_SITE` rồi `dc up -d`; chạm giới hạn cấp chứng chỉ thì chờ (mục 6b) |

Đừng dán đầu ra của `docker compose config` hay nội dung `hue.khoa.env` vào đâu cả — có khoá trong đó. Log của app không in khoá, nhưng có thể có câu
người dùng hỏi: gửi cho nhóm đoạn cần thiết, không gửi cả file.

## 9. Ghi chú chi phí

- Cả danh sách kiểm: khoảng 15–20 lượt hỏi, vài xu OpenAI. Không tạo thêm tài nguyên AWS nào.
- Dòng 11 (dừng / bật máy) không tốn thêm; dòng 10 không tốn gì ngoài bốn lượt hỏi.
- Buổi diễn tập: dưới 1 USD tiền máy nếu phá tầng máy chủ ngay sau buổi (guide 7 Bước 3) — QUÊN phá hoặc quên dừng thì máy tính tiền tiếp theo giờ.
- Một lượt thử tự động bằng trình duyệt do agent lái (khoảng 30 phút, vào địa chỉ công khai sau lần bật đầu) là TUỲ CHỌN của nhóm, không bắt buộc với
  chủ dự án; nó tốn thêm vài chục lượt hỏi.

## 10. Dọn dẹp

Guide này không dựng gì nên không có gì để phá. Ba thứ phải trả về như cũ sau khi kiểm:

- [ ] dòng `HUE_LUOT_MOI_NGAY=3` đã xoá khỏi `hue.env` (lệnh ở dòng 10) — `grep -c '^HUE_LUOT_MOI_NGAY=3$' /srv/hue/hue.env` in `0`;
- [ ] dòng `HUE_SO_VET=true` (nếu đã bật tạm) đã xoá khỏi `hue.khoa.env`, hộp app đã được tạo lại;
- [ ] file 13 MB của dòng 9 không để lại gì (lệnh tạo dữ liệu ngay trong ống, không ghi file).

Xong buổi: dừng máy (guide 6 mục 6.1) hoặc phá tầng máy chủ (guide 7 Bước 3).

## 11. Guide kế

`6_ngay_demo.md` — dừng tạm, bật lại trước giờ demo, cập nhật, lùi bản, hai nút khẩn cấp. `7_pha_sach.md` — phá sạch có kiểm khi không dùng nữa.
