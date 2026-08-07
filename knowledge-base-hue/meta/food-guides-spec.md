# Spec Cho Food Guides Huế

Tài liệu này định nghĩa spec và plan để triển khai
`knowledge-base-hue/foods/food-guides.md`. File guide sẽ được viết sau khi có đủ
dữ liệu research và dữ liệu món đặc sản từ `local_specialties`.

## Mục tiêu

`food-guides.md` là guide tổng hợp cho du khách muốn khám phá ẩm thực Huế. File
này trả lời các câu hỏi thực tế như ăn gì vào buổi sáng, nên thử món nào lần đầu
đến Huế, đi food tour nửa ngày hoặc nhiều ngày nên sắp xếp món và quán ra sao.

File này không thay thế các entity chi tiết:

- `foods/local_specialties/*.md`: mô tả món, thành phần, cách làm tóm tắt, nguồn
  gốc hoặc bối cảnh văn hóa, địa điểm tiêu biểu.
- `foods/restaurants/*.md`: thông tin chi tiết của từng địa điểm ăn uống.
- `foods/cafes/*.md`: thông tin chi tiết của từng quán cà phê hoặc đồ uống.

## Phạm vi nội dung

Guide nên bao gồm:

- Gợi ý cho người lần đầu đến Huế.
- Gợi ý theo thời điểm trong ngày: sáng, trưa, chiều, tối.
- Gợi ý ăn vặt, món ngọt, cà phê và đồ uống.
- Gợi ý món chay.
- Gợi ý theo ngân sách: bình dân, trung bình, trải nghiệm nhà hàng.
- Gợi ý theo nhóm người dùng: lần đầu đến Huế, gia đình, nhóm bạn, ăn chay,
  thích ăn vặt hoặc món ngọt.
- Food tour nửa ngày, 1 ngày, 2 ngày và 3 ngày.

Guide không nên bao gồm:

- Recipe chi tiết.
- Mô tả dài về nguồn gốc hoặc lịch sử món ăn.
- Đường dẫn nội bộ đến file quán trong `foods/restaurants/` hoặc `foods/cafes/`.
- Section rỗng hoặc câu báo thiếu dữ liệu.
- Section `## Nguồn dữ liệu`.

## Quy tắc dữ liệu

- Chỉ dùng món đặc sản đã có file trong `foods/local_specialties/`.
- Chỉ dùng quán đã curate trong `foods/restaurants/` và `foods/cafes/`.
- Khi nhắc đến món, chỉ diễn giải 1 câu ngắn để đặt ngữ cảnh du lịch.
- Khi gợi ý quán, ghi tên quán và địa chỉ ngắn.
- Không duplicate mô tả dài từ file món, nhà hàng hoặc cafe.
- Không tự chọn giá, giờ hoặc địa chỉ nếu dữ liệu nguồn có conflict.
- Nếu một quán thiếu địa chỉ trong file curated, không dùng quán đó trong guide
  hoặc chỉ dùng khi người dùng cung cấp địa chỉ bổ sung có nguồn.

## Cấu trúc đề xuất

```md
# Food Guides Huế

## Lần đầu đến Huế nên thử gì?

## Gợi ý ăn sáng

## Gợi ý ăn trưa

## Gợi ý ăn chiều và ăn vặt

## Gợi ý ăn tối

## Cà phê và đồ uống

## Gợi ý món chay

## Gợi ý món ngọt

## Theo ngân sách

### Bình dân

### Trung bình

### Trải nghiệm nhà hàng

## Gợi ý theo nhóm người dùng

### Lần đầu đến Huế

### Đi gia đình

### Đi nhóm bạn

### Ăn chay

### Thích ăn vặt hoặc món ngọt

## Food tour nửa ngày

## Food tour 1 ngày

## Food tour 2 ngày

## Food tour 3 ngày
```

## Quy tắc itinerary

- Itinerary theo bữa, món và vài quán gợi ý.
- Không cố định tuyến đường, giờ cụ thể hoặc thời lượng di chuyển.
- Với itinerary 2-3 ngày, tránh lặp món chính và quán chính trong cùng
  itinerary.
- Cafe và đồ uống có thể linh hoạt lặp lại nếu hợp lý với trải nghiệm du khách.
- Mỗi bữa nên có 1-2 lựa chọn món chính và 1-3 quán gợi ý nếu dữ liệu đủ.
- Không ép đủ quán cho mọi bữa nếu dữ liệu curated chưa đủ tin cậy.

## Món đặc sản nền cần có trước

Nên có 8 file `local_specialties` trước khi viết guide hoàn chỉnh:

- `bun bo hue.md`
- `com hen bun hen.md`
- `com am phu.md`
- `banh beo nam loc.md`
- `che hue che heo quay.md`
- `banh ep.md`
- `me xung.md`
- `banh canh hue.md`

## Format gợi ý địa điểm

Trong prose hoặc bullet, dùng format tự nhiên:

```md
- Bún bò Huế phù hợp cho bữa sáng hoặc bữa chính nhẹ. Có thể tham khảo Bún bò
  Hạnh, Bún bò Mụ Rơi hoặc Bún bò Bà Nga; mỗi quán cần kèm địa chỉ ngắn đã có
  trong file curated tương ứng.
```

Không dùng file path trong body guide. Nếu sau này cần graph hoặc link nội bộ,
tạo sidecar/index riêng thay vì nhúng vào Markdown curated.

## Plan triển khai cho coding agent

1. Kiểm tra trạng thái repo.
   - Verify: chạy `git status --short` và không đụng thay đổi ngoài scope.

2. Đọc chuẩn hiện hành.
   - Verify: đọc `Session_Prompt.md`, `Project_Status.md`,
     `knowledge-base-hue/meta/foods-template.md` và file spec này.

3. Kiểm tra dữ liệu món đặc sản.
   - Verify: xác nhận 8 file trong `foods/local_specialties/` đã tồn tại và
     không rỗng.

4. Trích danh sách quán đủ điều kiện.
   - Verify: mỗi quán được dùng trong guide phải có tên và địa chỉ trong file
     `restaurants/` hoặc `cafes/`.

5. Viết `food-guides.md` theo cấu trúc đã chốt.
   - Verify: file bắt đầu bằng `# Food Guides Huế`, không có YAML frontmatter,
     không có section `## Nguồn dữ liệu`, không có file path nội bộ.

6. Kiểm tra duplicate và scope.
   - Verify: guide không copy mô tả dài từ `local_specialties`, `restaurants`
     hoặc `cafes`; mỗi món chỉ có diễn giải ngắn.

7. Chạy validation.
   - Verify: chạy `git diff --check` và kiểm tra thủ công các heading chính.

## Checklist acceptance

- `food-guides.md` là guide du lịch, không phải recipe collection.
- Có đủ phần theo thời điểm trong ngày.
- Có đủ phần theo ngân sách.
- Có đủ phần theo nhóm người dùng.
- Có đủ itinerary nửa ngày, 1 ngày, 2 ngày và 3 ngày.
- Gợi ý quán có tên và địa chỉ ngắn.
- Không có source section riêng trong `food-guides.md`.
- Không có section rỗng, placeholder, hoặc câu báo thiếu dữ liệu.
- Không có file path nội bộ trong body guide.
