---
name: risk-gated-agent-review
description: Dùng khi Reviewer và Implementer phối hợp qua đặc tả, bằng chứng triển khai, kiểm tra độc lập theo rủi ro, sửa đổi sau đánh giá, xác nhận hoàn tất hoặc bàn giao giữa các phiên làm việc.
---

# Phối hợp đánh giá tác nhân theo rủi ro

## Mục đích

Tập trung công sức của Reviewer vào yêu cầu, quyết định và các kiểm tra độc lập
cần thiết theo rủi ro. Implementer chịu trách nhiệm thực hiện đầy đủ phạm vi,
tự kiểm tra và cung cấp bằng chứng chi tiết. Dùng một bản bàn giao gọn, chỉ mang
ngữ cảnh mà vai trò tiếp theo cần.

Skill này điều phối vai trò và ngữ cảnh, không quy định cách viết, kiểm thử,
gỡ lỗi hoặc tổ chức mã triển khai. Những việc đó tuân theo quy định dự án và
các skill triển khai phù hợp.

## Bắt đầu từ nhiệm vụ hiện hành

Đọc các tài liệu khởi động do dự án quy định theo thứ tự:

1. hướng dẫn ổn định cho phiên làm việc;
2. bản đồ và trạng thái hiện tại của dự án;
3. quy trình dành cho vai trò được giao;
4. bản bàn giao hiện hành duy nhất.

Kiểm tra `Target role` trước khi thực hiện bàn giao. Yêu cầu trực tiếp mới của
user có thể thay thế bàn giao cũ: dùng vai trò được giao và bảo toàn tiến độ cũ
bằng tham chiếu trước khi thay bàn giao trong phạm vi được phép. Bàn giao cũ
không chặn việc đọc hoặc brainstorming mới được yêu cầu. Với bàn giao đang
thực hiện, dừng phần công việc phụ thuộc nếu vai trò hoặc bước tiếp theo duy
nhất chưa rõ.

Nạp ngữ cảnh từng mức:

```text
Mức 0: các tài liệu khởi động
Mức 1: hợp đồng đánh giá và chênh lệch chính xác giữa trạng thái gốc/đích
Mức 2: mã nguồn bị ảnh hưởng, kiểm tra tập trung và bằng chứng được chọn theo rủi ro
Mức 3: hệ thống thật, nghiên cứu bên ngoài hoặc kiểm chứng rộng hơn khi cần
```

Không đọc toàn bộ lịch sử dự án hoặc mọi báo cáo chỉ để yên tâm. Mở rộng ngữ
cảnh khi quyết định, mâu thuẫn, ranh giới an toàn hoặc tác động rủi ro yêu cầu.
Giới hạn ngữ cảnh mang tính định hướng không cho phép bỏ yêu cầu hay ranh giới
an toàn.

## Chọn nhánh vai trò

- Dùng **nhánh Reviewer** cho brainstorming, đặc tả, lập kế hoạch, phát hiện vấn
  đề, kiểm chứng độc lập, kết luận đánh giá và xác nhận hoàn tất.
- Dùng **nhánh Implementer** cho thực hiện phạm vi đã duyệt, tự kiểm tra, sửa
  đổi, tạo bằng chứng và cập nhật kết thúc mang tính cơ học theo quyền được cấp.
- Nếu vai trò chưa rõ và sự khác biệt làm thay đổi quyền, hỏi một câu rồi dừng.

## Nhánh Reviewer

### Điểm duyệt thiết kế

Trước khi triển khai, cùng user chốt yêu cầu và các đánh đổi quan trọng. Soạn
đặc tả và kế hoạch được duyệt. Đặt một hợp đồng đánh giá ngắn (Review Contract)
trong kế hoạch, gồm:

- mức rủi ro và các tác động dự kiến cần kiểm tra;
- bằng chứng Implementer phải cung cấp;
- kiểm tra độc lập tối thiểu của Reviewer;
- những phần chính xác Reviewer phải chạy lại;
- bằng chứng được phép dùng lại khi sửa đổi;
- hành động cần cấp quyền mới;
- cách xác nhận hoàn tất dự kiến.

Reviewer sở hữu hợp đồng này. Implementer có thể báo mức rủi ro quan sát được
cao hơn nhưng không được tự hạ mức rủi ro.

Phân biệt yêu cầu, hợp đồng, kiến trúc và đường dẫn được phép có tính ràng buộc
với cách tổ chức mã nội bộ chỉ mang tính minh họa. Implementer được chọn cách
đặt tên, tổ chức hàm/hàm hỗ trợ/lớp trong các ranh giới đó, có bằng chứng tương
xứng và giải thích những đánh đổi có ý nghĩa. Sở thích của Reviewer không tự
trở thành tiêu chí nghiệm thu mới.

### Điểm đánh giá cuối

Với mỗi lần triển khai, thực hiện độc lập:

1. xác nhận vai trò nhận và trạng thái gốc/đích;
2. kiểm tra cây làm việc và mọi đường dẫn thay đổi, kể cả tệp chưa được Git theo dõi;
3. đọc chính xác phần chênh lệch;
4. đối chiếu phần chênh lệch với tiêu chí nghiệm thu;
5. nhận diện thay đổi ngoài phạm vi và sai lệch;
6. chạy kiểm tra định dạng phần chênh lệch của kho mã;
7. nhận diện bằng chứng thiếu hoặc mâu thuẫn.

Sau đó chỉ đọc và chạy thêm những phần hợp đồng đánh giá hoặc rủi ro quan sát
được yêu cầu. Báo cáo của Implementer là tập hợp các tuyên bố và chỉ mục bằng
chứng, không tự chứng minh kết quả. Tính độc lập đến từ việc kiểm tra phần
chênh lệch và kiểm chứng có mục tiêu, không phải lặp lại mọi lệnh xác định.

### Kiểm chứng theo tác động rủi ro

Phân loại theo tác động, không theo đuôi hoặc số lượng tệp: thấp (`low`) cho
chỉnh sửa giới hạn không đổi hành vi/quyền; trung bình (`medium`) cho thay đổi
hành vi nội bộ hoặc quy định điều phối có phạm vi rõ; cao (`high`) cho dữ liệu
đang hoạt động, thao tác phá hủy, bảo mật, hợp đồng công khai, nhà cung cấp hoặc
quyết định về mô hình/chất lượng. Thay đổi quyền chỉ nằm trong tài liệu có thể
cần đánh giá điều phối sâu hơn mà không cần chạy backend. Ghi tác động cụ thể
và ranh giới bị ảnh hưởng; không cần chấm điểm số.

| Tác động cần kiểm tra | Công việc bổ sung của Reviewer |
|---|---|
| Chỉ thay đổi tài liệu | Kiểm tra tính nhất quán, liên kết và trạng thái vòng đời |
| Hành vi chức năng | Đọc đường đi bị sửa và chạy kiểm tra xác định nhỏ nhất có ích |
| Thành phần phụ thuộc/nhà cung cấp | Kiểm tra cách phân giải, nơi sử dụng và hợp đồng chính thức khi cần |
| Cơ sở dữ liệu/tích hợp | Chạy đúng đường đi thật bị ảnh hưởng trên đích an toàn |
| Mô hình/truy xuất/chấm điểm | Chỉ chạy lại mô hình, đường đi hoặc chỉ số bị thay đổi |
| Chất lượng/đánh giá | Dùng dữ liệu chuẩn và chạy lại phần đánh giá bị ảnh hưởng |
| Dữ liệu đang hoạt động/di chuyển dữ liệu | Kiểm tra quyền, đích chính xác và trạng thái trước/sau |
| Bảo mật/giao diện công khai | Kiểm tra ranh giới bị ảnh hưởng và hành vi quan sát được |
| Sai lệch/mâu thuẫn | Mở rộng đánh giá tới những nguồn cần để giải quyết |

Dùng định nghĩa mức độ nghiêm trọng và kết luận của dự án. Reviewer không sửa
mã chạy thay Implementer hoặc âm thầm mở rộng nhiệm vụ.

### Sửa đổi sau đánh giá và xác nhận hoàn tất

Mỗi phát hiện nêu vị trí mã/tài liệu, yêu cầu bị ảnh hưởng, bằng chứng, tác động
và tiêu chí đóng có thể quan sát. Gom các phát hiện đã có thành một lượt đánh
giá. Phát hiện về tính đơn giản phải giải thích độ phức tạp không cần thiết và
kết quả cần đạt; không áp đặt sở thích cá nhân hoặc một cơ chế mới.

Implementer được phản biện bằng bằng chứng hoặc đề xuất giải pháp đơn giản hơn
vẫn đáp ứng yêu cầu. Reviewer đánh giá phản hồi và ghi rõ phát hiện đã đóng,
được điều chỉnh hay còn mở. Nếu bất đồng tiếp diễn, Reviewer tổng hợp lựa chọn
và khuyến nghị để user quyết định. Không vai trò nào được bỏ qua phát hiện chưa
giải quyết bằng cách tự nhận đã được duyệt hoặc thay tiêu chí nghiệm thu.

Vấn đề ngoài phạm vi được ghi ngắn trong báo cáo đánh giá hiện có, không mở
rộng phần sửa hoặc chặn nhiệm vụ. Dừng và trình quyết định khi vấn đề làm kết
luận nghiệm thu không còn đáng tin hoặc vi phạm an toàn/quyền. Cải thiện nhỏ
(`minor`) không ảnh hưởng nghiệm thu hay an toàn không chặn trạng thái sẵn sàng:
triển khai trong phạm vi nếu có ích, hoặc ghi ngắn lý do giữ lại; không tạo vòng
sửa chỉ vì minor. Không hạ vấn đề về hành vi bắt buộc hoặc an toàn thành minor.

Với phát hiện chặn hoàn tất, thay bàn giao bằng đúng phần cần sửa, gồm:

- mức độ nghiêm trọng và yêu cầu bị ảnh hưởng;
- đường dẫn bị ảnh hưởng;
- tiêu chí nghiệm thu phần sửa;
- kiểm chứng phải chạy lại;
- bằng chứng có thể dùng lại an toàn;
- ranh giới phải giữ nguyên.

Sửa đổi trong phạm vi không cần user duyệt riêng theo quy trình dự án đã thống
nhất. Đánh giá lại vẫn giữ kiểm tra chênh lệch độc lập tối thiểu, tập trung phần
sửa và đường đi bị ảnh hưởng, dùng lại bằng chứng đủ điều kiện. Phát hiện mới
vẫn hợp lệ nhưng phải giải thích bằng chứng mới, tác động mới hoặc điểm trước
đó bỏ sót; không âm thầm mở rộng tiêu chí nghiệm thu.

Khi đạt trạng thái sẵn sàng về kỹ thuật, viết hợp đồng xác nhận hoàn tất
(Approval Closure Contract). Hợp đồng nêu xác nhận cần từ user, chỉnh sửa trạng
thái/tài liệu chính xác, kiểm tra, quyền Git và bàn giao tiếp theo. Đặt ngay
trong báo cáo đánh giá/bàn giao hiện có, không tạo tài liệu thủ tục riêng.
Reviewer quyết định về kỹ thuật; user xác nhận hoàn tất dựa trên kết quả đã
kiểm chứng và giới hạn. User chỉ bắt buộc chạy lại khi tiêu chí nghiệm thu đã
duyệt yêu cầu rõ. Implementer chỉ được cập nhật kết thúc cơ học theo quyền được
cấp sau khi user xác nhận.

Không mặc định giao tác nhân phụ. Chỉ dùng cho kiểm tra có giá trị cao, tách
thành các phần độc lập được và có quyền rõ ràng.

## Nhánh Implementer

### Hoàn tất phạm vi đã duyệt

Thực hiện đầy đủ kế hoạch đã duyệt, chạy các kiểm tra, đọc chính xác phần chênh
lệch và sửa vấn đề chặn hoàn tất trong phạm vi trước khi bàn giao; áp dụng chính
sách minor ở trên. Không xin ý kiến Reviewer giữa chừng cho sửa đổi thông
thường nằm trong hợp đồng.

Dừng và trình quyết định khi cần đổi yêu cầu, kiến trúc, nhà cung cấp/mô hình,
hợp đồng dữ liệu, ranh giới an toàn, mức rủi ro hoặc quyền, hay khi có trở ngại
thực sự khiến không thể tạo bằng chứng đáng tin.

Implementer không tự duyệt, hạ rủi ro hoặc diễn giải lại hợp đồng xác nhận hoàn tất.

### Cung cấp bằng chứng ở hai mức

Báo cáo triển khai chi tiết cần đủ thông tin: thay đổi, lệnh, kết quả quan sát,
sản phẩm đầu ra, lỗi, giới hạn và những sửa đổi khi tự kiểm tra.

Giữ bản bàn giao hiện hành gọn, gồm:

- đối chiếu tiêu chí nghiệm thu với bằng chứng;
- đường dẫn thay đổi;
- tóm tắt lệnh/kết quả;
- các điểm rủi ro và sai lệch;
- tham chiếu sản phẩm đầu ra/báo cáo;
- phần thất bại, bỏ qua và chưa kiểm chứng;
- phần chính xác Reviewer phải chạy lại theo hợp đồng đánh giá.

Không trình bày giá trị kỳ vọng, kết quả cũ hoặc khẳng định thiếu căn cứ như
một kết quả đạt mới quan sát được.

### Sửa đổi và kết thúc

Xử lý một bàn giao sửa đổi trong một lượt, bằng sửa mã hoặc phản hồi có bằng
chứng. Chạy lại kiểm tra bị ảnh hưởng, xác định bằng chứng trước đó còn hợp lệ
và lý do. Trả phần chênh lệch về Reviewer; không tự đóng phát hiện.

Sau khi user xác nhận, thực hiện đúng hợp đồng xác nhận hoàn tất. Dừng nếu user
thêm yêu cầu hoặc trạng thái kho mã không còn khớp hợp đồng.

## Quy định bản bàn giao hiện hành

Dùng một bản bàn giao hiện hành được quản lý phiên bản, tối đa một nhiệm vụ
đang hoạt động. Giữ nguyên tên trường kỹ thuật để các workflow dùng nhất quán:

```text
Target role:
Authored by:
Handoff kind:
State: active
Base commit:
Head commit:
Risk level:
Git authorization:
```

Các trường lần lượt chỉ vai trò nhận, người viết, loại bàn giao, trạng thái,
commit gốc, commit đích, mức rủi ro và quyền Git.

`Head commit` có thể là `HEAD`, mã SHA của commit bên ngoài hoặc `worktree`.
Phân giải `HEAD` thành SHA khi bắt đầu đánh giá. Các loại bàn giao được hỗ trợ:

- `next_design`: thiết kế nhiệm vụ tiếp theo;
- `implementation`: triển khai;
- `final_review`: đánh giá cuối;
- `correction`: sửa đổi sau đánh giá;
- `closure`: xác nhận và cập nhật kết thúc.

Sau khi đã xác nhận hoàn tất, nếu chưa có nhiệm vụ mới, giữ nhiệm vụ vừa đóng
với `State: completed`, không có quyền thực thi và một chỉ dẫn duy nhất là chờ
user giao nhiệm vụ tiếp theo. Đây không phải bàn giao đang hoạt động bị sai
định dạng; không tự tạo nhiệm vụ chỉ để điền vào. Nhiệm vụ mới được giao sẽ
thay thế trạng thái này.

Nội dung gồm mục tiêu, quyết định mới nhất có hiệu lực ưu tiên, tham chiếu chuẩn,
phạm vi, ranh giới, hợp đồng đánh giá, đối chiếu nghiệm thu, đường dẫn đã/dự kiến
thay đổi, bằng chứng, sai lệch, bước tiếp theo và điều kiện dừng. Giữ phần không
liên quan ngắn, không điền nội dung mẫu cho đủ mục.

Các tài liệu khởi động giúp tìm nhiệm vụ, không thay việc đọc đặc tả/kế hoạch
đã duyệt, phần sửa và bằng chứng cần cho thực hiện. Trạng thái dự án giữ trạng
thái các nhánh công việc và tham chiếu chuẩn, không giữ bước tiếp theo độc lập
thứ hai. Bảo toàn tiến độ chưa commit của nhiệm vụ bị thay thế trong báo cáo/
inventory hiện có, hoặc bản lưu ghi rõ không hoạt động nếu thông tin sẽ bị mất.
Bản lưu không cấp quyền thực thi.

Chỉ dùng `closure` khi có hợp đồng xác nhận hoàn tất. Nếu bàn giao tới người
thực hiện trước khi user xác nhận, bước tiếp theo duy nhất là chờ; chưa được
phép cập nhật cơ học. Reviewer có quyền có thể tự kết thúc, không bắt buộc
chuyển vai trò lần nữa chỉ để cập nhật tài liệu.

Dừng khi commit không hợp lệ, phần chênh lệch không khớp khai báo, thiếu đầu vào,
yêu cầu mâu thuẫn, thay đổi chưa khai báo không thể cô lập, bằng chứng được
khẳng định thiếu căn cứ hoặc chưa có quyền được yêu cầu.

## Dùng lại bằng chứng

Chỉ dùng lại bằng chứng khi sửa đổi nếu bằng chứng đã đạt trong cùng chuỗi
triển khai và phần sửa không thay đầu vào, thành phần phụ thuộc, môi trường
hoặc luồng dữ liệu. Ghi lý do trong bàn giao. Không gắn nhãn kết quả cũ là lần
chạy mới cho hành vi đã thay đổi.

## Quyền Git

Bàn giao khai báo một giá trị:

```text
git_authorization: none
git_authorization: commit
git_authorization: commit_and_push
```

Tương ứng: không có quyền Git, được commit, hoặc được commit và push.
Quyền phải chỉ rõ phạm vi và mục đích. Quyền cho phép thao tác Git, không cho
phép thêm thay đổi nội dung. Commit làm mốc kiểm tra là đích để đánh giá, không
phải sự phê duyệt.

## Kết thúc lượt làm việc

Kết thúc bằng một vai trò nhận và một bước tiếp theo rõ ràng. Lịch sử chi tiết
nằm trong quản lý phiên bản và tài liệu chuẩn; không chép vào bàn giao hiện hành.

Với các phiên tách riêng, chủ động cung cấp prompt chuyển tiếp ngắn nêu vai trò
nhận và tài liệu khởi động/bàn giao cần đọc. User chuyển tiếp prompt; đây không
phải đặc tả khác và không cấp quyền tự khởi chạy tác nhân.
