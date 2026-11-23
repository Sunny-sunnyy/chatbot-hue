# Bản thiết kế deploy hue_rag lên AWS — bản 3, rút gọn

Viết: 20:07 23/11/2026 (giờ `date`), phiên B soạn nháp, phiên điều phối chốt. THAY bản 2 (`2026-11-16-deploy-aws-design.md`: một máy Lightsail, làm theo một tài liệu
duy nhất) — bản 2 giữ làm hồ sơ. Trang này chỉ nói VÌ SAO; làm thế nào ở `deploy/guides/`, mục lục ở `deploy/README.md`.
**Chỉ là tài liệu: chưa có tài nguyên AWS nào được tạo, nhóm không gọi AWS.**

Nhãn: **[AWS]** = lấy từ bảng giá / trang tài liệu công khai của AWS, phiên B tự tải hoặc mở ngày 23/11/2026 · **[OpenAI]** = trang tài liệu OpenAI, mở cùng
ngày · **[khoá]** = theo bài của khoá AI Production (ghi chú đọc khoá học của phiên B và D) · **[đo]** = số nhóm đo ở máy · **[ước]** = tính / ước, chưa đo.

## 1. Đã chọn gì

| Chọn | Ai chọn, khi nào |
|---|---|
| Một máy EC2 chạy Docker Compose, **chỉ bật quanh ngày demo / ngày chấm**, dừng máy khi không dùng | chủ dự án, 23/11/2026 |
| Model viết của bản deploy: `gpt-6-luna` của OpenAI — MỘT đường model; máy không có quyền gọi model nào của AWS | chủ dự án, 23/11/2026 |
| Tài khoản AWS cá nhân, vùng Singapore; một người dùng IAM MỚI chỉ cho việc deploy | chủ dự án, 23/11/2026 |
| Deploy là điểm cộng, làm sau buổi tự test ở máy; nhóm chỉ CHUẨN BỊ, chủ dự án gõ mọi lệnh tạo / xoá | chủ dự án, 19–22/11/2026 |
| Hai thư mục Terraform (tầng nền gần 0 đồng ↔ tầng máy chủ tính tiền), state ở máy người chạy, guide theo khuôn 11 mục | nhóm, theo khuôn chủ dự án tự đặt ở dự án khoá học |

## 2. Sơ đồ

```
 Người dùng ──HTTPS 443──▶ ┌──────────── MỘT máy EC2 (Singapore) ────────────┐
 (trình duyệt)             │  [1] Caddy  ──▶  [2] app hue_rag  ──▶ [3] Qdrant │──HTTPS──▶ [4] OpenAI (gpt-6-luna)
                           │   cửa vào,        FastAPI + giao       chỉ mục    │             khoá trong file quyền 600 trên máy
                           │   chứng chỉ       diện + kho                      │
                           └──────────────────────▲──────────────────────────┘
 Chủ dự án ──Session Manager (không SSH)──────────┘      ▲ tải gói bằng vai gắn máy (chỉ đọc)
 Chủ dự án ──Terraform + đẩy gói──▶ [5] tầng nền: thùng S3 chứa gói · vai gắn máy · [6] ngân sách + email cảnh báo
```

Cổng mở ra ngoài: chỉ 80 và 443. Ứng dụng (8000) và Qdrant (6333) chỉ nghe trong máy. Không cổng 22.

## 3. Vì sao

| Câu hỏi | Trả lời | Cái giá nhận lấy |
|---|---|---|
| Vì sao một MÁY mà không Lambda như khoá học | hue_rag giữ ba thứ trong bộ nhớ của tiến trình — cuộc trò chuyện, lịch đang sửa, bộ đếm lượt — và cần một Qdrant chạy cạnh; lên Lambda phải sửa lõi cả ba | tự lo máy: vá, dừng / bật; tiền đứng yên khi máy dừng |
| Khoá học nêu hai nhược điểm của "máy luôn bật": tiền cố định kể cả khi không ai vào, khó tự co giãn [khoá] | tiền cố định ⇒ máy chỉ bật quanh ngày demo, còn lại dừng ("co về 0 bằng tay") · co giãn ⇒ không cần: người dùng là người chấm và vài người xem | bật lại trước giờ demo ("khởi động lạnh") là việc phải nhớ |
| Vì sao EC2 mà không Lightsail (bản 2) | Lightsail dừng máy VẪN tính đủ tiền [AWS] ⇒ với cách dùng "bật 60–100 giờ một tháng" là gần 24 USD so với 10–12 của EC2; EC2 có vai gắn máy ⇒ tải gói và vào máy không cần khoá AWS dài hạn, không khoá SSH, không cổng 22; EC2 + mạng + nhóm bảo mật là thứ chủ dự án đã học | nhiều tài nguyên và khái niệm hơn Lightsail |
| Vì sao model OpenAI trên máy chủ trong khi ở máy đang chạy Claude | chủ dự án chọn; máy chỉ cần MỘT khoá, không vai liên tài khoản, không bước mở model. Hệ quả: bản deploy trả lời KHÁC bản ở máy (ngắn hơn khoảng ba lần, chữ chạy dần) và đã phải đo bù riêng trên model đó trước khi tin | hai nơi là hai model |
| Vì sao một khoá API mà không vai như khoá học dạy cho production | model nằm ngoài AWS, không vai nào cấp được quyền gọi. Ba nhược điểm của khoá API và cách chặn: lộ ⇒ khoá chỉ ở một file quyền 600 trên máy, không trong ảnh, không trong git · không tự xoay ⇒ khoá riêng cho bản deploy, thu hồi là xong · bị gọi cạn tiền ⇒ ba lớp ở mục 5 | chủ dự án tự giữ và tự thu hồi khoá |
| Vì sao file quyền 600 mà không Secrets Manager | một máy, một bí mật; ít khái niệm; không bí mật nào đi qua state của Terraform | — |
| Vì sao HAI tầng Terraform | "có trạng thái ↔ không trạng thái" [khoá]: gói đã đẩy, email đã xác nhận, quyền là thứ giữ lâu và gần 0 đồng; máy là thứ tính tiền, dựng và phá nhiều lần được | chép tay ba đầu ra từ tầng nền sang tầng máy chủ |
| Vì sao state ở máy mà không lên S3 như tuần 2 | khoá học đưa state lên S3 vì máy chạy pipeline là máy tạm; ở đây một người chạy từ máy mình, không pipeline | mất file state thì phải phá tay theo thẻ `Project = hue-rag` |
| Vì sao không ECR, cổng API, CloudFront, WAF, VPC endpoint, GuardDuty, đăng nhập người dùng, Aurora | mỗi thứ là một dịch vụ thêm phải giải thích và trả tiền, cho một bản demo một máy chạy vài ngày; chưa có mối đe doạ cụ thể nào để biện minh cho từng lớp | không có lớp chặn tần suất ở cổng — thay bằng trần lượt trong ứng dụng |

Đặt vào khung "năm kiểu deploy" của khoá học [khoá]: hue_rag là kiểu **máy chủ thuê (IaaS — EC2)**, không phải nền tảng, hộp chạy sẵn, điều phối hộp hay không máy chủ.

## 4. Tiền

Máy `t3a.medium` (2 vCPU, 4 GB) 0,0472 USD / giờ · đĩa 40 GB 3,84 USD / tháng · địa chỉ IPv4 công khai 0,005 USD / giờ kể cả lúc máy dừng [AWS — bảng giá công
khai vùng Singapore, chưa thuế].

| Máy chạy trong tháng | Tiền máy + đĩa + IP [AWS] |
|---|---|
| 0 giờ (dừng cả tháng) | 7,49 USD |
| 60 giờ | 10,32 USD |
| 100 giờ | 12,21 USD |
| 730 giờ (quên tắt, bật liên tục) | 41,95 USD |
| Đã phá tầng máy chủ, chỉ còn tầng nền | khoảng 0,03 USD cho mỗi gói còn trong thùng (gói khoảng 1 GB [đo]; giá lưu trữ [ước]) |

Để so, ba con số khoá học đã dạy [khoá]: Lambda gần 0 · App Runner 5–6 USD · ECS kèm cân bằng tải 16–20 USD một tháng. Phương án ở đây đắt hơn Lambda vì giữ
một máy; lý do không Lambda ở mục 3.

Tiền gọi model: một câu hỏi trên `gpt-6-luna` khoảng 0,0004–0,002 USD [đo]; ứng dụng giới hạn 50 lượt mỗi địa chỉ và 500 lượt cả máy mỗi ngày ⇒ ngày nặng
nhất khoảng 1 USD [ước].

## 5. Ba lớp chốt tiền gọi model — và hai chốt KHÔNG tức thời

1. **Trần lượt mỗi ngày trong ứng dụng** (`HUE_LUOT_MOI_NGAY`, `HUE_LUOT_TONG_MOI_NGAY`): vượt thì trả lỗi 429 ngay. Là lớp duy nhất ngắt tức thời; bộ đếm nằm
   trong bộ nhớ nên về 0 khi ứng dụng khởi động lại.
2. **Trần cứng của project phía OpenAI** ("Enforce a hard limit"): chạm thì lời gọi trả 429. Phải BẬT ô đó — không bật thì con số chỉ là cảnh báo. Không tức
   thời, có thể vượt nhẹ [OpenAI].
3. **Số tiền nạp trước**, với tự nạp lại đã TẮT (lúc thiết lập nạp tiền, tự nạp lại bật sẵn) [OpenAI]. Hết tiền cũng không ngừng tức thời, số dư có thể âm nhẹ.

Phía AWS không có chốt cứng nào: ngân sách chỉ gửi email, tới chậm tới một ngày [AWS]. Chốt thật cho tiền máy là dừng máy cuối buổi.

## 6. Sáu trụ cột của khoá học — hue_rag có gì

| Trụ cột [khoá] | Ở dự án cuối khoá | Ở bản deploy hue_rag | Vì sao khác |
|---|---|---|---|
| Mở rộng | không máy chủ, tự co giãn | một máy, một tiến trình, không co giãn | người dùng là người chấm; tăng 100 lần thì nghẽn trước ở: một tiến trình, trí nhớ trong bộ nhớ, hạn mức gọi model |
| Bảo mật | đang có: mỗi hàm một vai quyền hẹp, người dùng phải đăng nhập, chặn tần suất ở cửa vào, CORS đúng một nguồn, mật khẩu cơ sở dữ liệu cất ở Secrets Manager; WAF, VPC endpoint, GuardDuty chỉ là lớp "thêm nếu cần", có phí | không cổng 22 (Session Manager), vai chỉ đọc một thùng, thùng riêng tư, khoá OpenAI ở file quyền 600, HTTPS, trần cỡ yêu cầu, trần lượt | không có tài khoản người dùng nên không có bước đăng nhập; chặn tần suất làm ngay trong ứng dụng (trần lượt); ba lớp có phí chưa có mối đe doạ để biện minh cho một bản demo một máy |
| Giám sát | bảng CloudWatch + báo động | ngân sách (email) + MỘT báo động "máy không qua kiểm tra trạng thái" (email) | model không nằm trong AWS nên CloudWatch không có số nào của nó |
| Rào | rào bằng code quanh model | trả lời chỉ từ kho, kiểm trích dẫn, câu từ chối cố định, số / ngày / lịch do code tính; trần lượt | rào nằm sẵn trong sản phẩm, không thêm gì cho bản deploy |
| Giải thích được | model phải ghi lý do TRƯỚC kết luận, lý do được ghi log; có sổ kiểm toán cho từng quyết định của AI | mỗi câu trả lời có nguồn mở được | sản phẩm là hỏi đáp từ kho: thứ người dùng cần kiểm là NGUỒN của từng câu, không phải lý do của một quyết định thay họ |
| Quan sát | Langfuse | log của ba hộp xem bằng lệnh trên máy; trang theo dõi của ứng dụng; trang sử dụng của OpenAI; sổ vết TẮT mặc định trên máy deploy (có chữ người dùng) | không đẩy log đi đâu: một máy, vài ngày chạy |

"Ba người bạn" [khoá] đi cùng nhau ở đây là: rào = hàng "Rào" · giám sát = hàng "Giám sát" · quan sát = hàng "Quan sát".

## 7. Hướng đã xét, không làm

- **Claude trên máy chủ:** bộ khoá đang gọi Claude thuộc một tài khoản AWS khác tài khoản deploy; vai gắn máy không tự gọi được model ở tài khoản khác. Chủ dự
  án chọn OpenAI cho bản deploy. Phần gói đã làm cho hướng này (file phủ, hộp lấy khoá tạm) giữ làm đường tuỳ chọn, bản deploy không dùng.
- **Lightsail (bản 2):** mục 3. Chỉ rẻ hơn EC2 khi máy bật trên khoảng 350 giờ một tháng — lúc đó mới đáng xét lại.
- **Lambda:** mục 3.
- **Tự dừng máy theo giờ, hoặc ngân sách tự dừng máy khi chạm mốc:** tuỳ chọn, CHƯA làm.
- **Lớp mật khẩu chung ở cửa vào cho những ngày bật:** tuỳ chọn, CHƯA làm; là câu của chủ dự án nếu muốn.

## 8. Chưa kiểm được

Mọi thứ cần tài khoản thật: danh sách ở `deploy/README.md` mục "Thứ CHƯA kiểm được". Thứ đã kiểm ở máy: gói Docker chạy trọn (dựng ảnh, nạp chỉ mục, ba hộp,
một câu hỏi thật) và `terraform fmt` / `validate` của các thư mục Terraform. Lượt đo bù trên `gpt-6-luna` (model của bản deploy) đã chạy ngày 23/11/2026; các
giới hạn riêng của đường model đó ghi ở `guides/RUNBOOK_BAN_GIAO.md` mục 10.
