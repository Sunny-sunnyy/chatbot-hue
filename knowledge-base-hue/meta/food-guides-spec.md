# Spec Cho Food Guides Huế

Tài liệu này định nghĩa spec và plan để triển khai
`knowledge-base-hue/foods/food-guides.md`. File guide là cẩm nang ăn uống Huế
tổng hợp cho du khách, viết từ dữ liệu curated trong `foods/` và 4 bài cẩm nang
research do người dùng cung cấp (Cẩm nang AEON MALL Huế cập nhật 2026).

## Mục tiêu

`food-guides.md` là guide tổng hợp cho du khách muốn khám phá ẩm thực Huế. File
này trả lời các câu hỏi thực tế như ăn gì vào buổi sáng, nên thử món nào lần đầu
đến Huế, đi food tour nửa ngày hoặc nhiều ngày nên sắp xếp món và quán ra sao,
cùng mức chi phí ăn uống tham khảo.

File này không thay thế các entity chi tiết:

- `foods/local_specialties/*.md`: mô tả món, thành phần, cách làm tóm tắt, nguồn
  gốc hoặc bối cảnh văn hóa, địa điểm tiêu biểu.
- `foods/restaurants/*.md`: thông tin chi tiết của từng địa điểm ăn uống.
- `foods/cafes/*.md`: thông tin chi tiết của từng quán cà phê hoặc đồ uống.

## Nguồn dữ liệu

1. Dữ liệu curated trong `foods/restaurants/`, `foods/cafes/` và
   `foods/local_specialties/`.
2. Cẩm nang AEON MALL Huế cập nhật 2026 do người dùng cung cấp (4 bài: chi phí,
   ăn sáng, ăn trưa, ăn đêm). Research dùng để định hướng món và mức chi phí,
   không thay thế dữ liệu quán curated.

Quy tắc chọn quán:

- Chỉ chọn quán đã curate trong `foods/restaurants/` và `foods/cafes/`.
- Quán được dùng trong guide phải có tên và địa chỉ trong file curated tương
  ứng; quán thiếu địa chỉ thì không dùng.
- Món research không có quán curated tương ứng thì bỏ khỏi guide.
- Địa chỉ dùng theo file curated đã được xác nhận: Cơm hến Bà Cam (49 Tùng
  Thiện Vương), Bánh canh O Hoa (3 Trịnh Công Sơn), Bánh mì Trường Tiền O Tho
  (14 Trần Cao Vân). Bánh bà Chi (2/64 Hoàng Diệu) là quán khác với Quán Bánh
  Chi curated (52-54 Lê Viết Lượng) nên không dùng trong guide.

## Phạm vi nội dung

Guide bao gồm:

- Gợi ý cho người lần đầu đến Huế.
- Gợi ý theo thời điểm trong ngày: sáng, trưa, chiều, tối, đêm.
- Gợi ý ăn vặt, món ngọt, cà phê và đồ uống.
- Gợi ý món chay.
- Gợi ý theo ngân sách: bình dân, trung bình, trải nghiệm nhà hàng, kèm mức
  chi phí ăn uống tham khảo từ research.
- Gợi ý theo nhóm người dùng: lần đầu đến Huế, gia đình, nhóm bạn, ăn chay,
  thích ăn vặt hoặc món ngọt.
- Food tour nửa ngày, 1 ngày, 2 ngày và 3 ngày.

Guide không bao gồm:

- Recipe chi tiết.
- Mô tả dài về nguồn gốc hoặc lịch sử món ăn.
- Đường dẫn nội bộ đến file quán trong `foods/restaurants/` hoặc `foods/cafes/`.
- Section rỗng hoặc câu báo thiếu dữ liệu.
- Section `## Nguồn dữ liệu` riêng. Với dữ liệu từ research, ghi chú nguồn ngắn
  ngay trong section, ví dụ: "Mức tham khảo theo Cẩm nang AEON MALL Huế cập
  nhật 2026".

## Quy tắc dữ liệu

- Chỉ dùng món đặc sản đã có file trong `foods/local_specialties/`; ngoài ra có
  thể nhắc món khác nếu quán curated phục vụ và có nguồn trong file quán.
- Khi nhắc đến món, chỉ diễn giải 1 câu ngắn để đặt ngữ cảnh du lịch.
- Khi gợi ý quán, ghi tên quán và địa chỉ ngắn.
- Không duplicate mô tả dài từ file món, nhà hàng hoặc cafe.
- Không tự chọn giá, giờ hoặc địa chỉ nếu dữ liệu nguồn có conflict; dùng giá,
  giờ, địa chỉ đã có trong file curated.
- Format chính: bullet theo món, mỗi section 3-6 lựa chọn tiêu biểu.

## Cấu trúc

```md
# Food Guides Huế

## Lần đầu đến Huế nên thử gì?

## Gợi ý ăn sáng

## Gợi ý ăn trưa

## Gợi ý ăn chiều và ăn vặt

## Gợi ý ăn tối

## Gợi ý ăn đêm

## Cà phê và đồ uống

## Gợi ý món chay

## Gợi ý món ngọt

## Theo ngân sách

### Bình dân (phần lớn món dưới 40.000 VNĐ)

### Trung bình (khoảng 40.000 – 100.000 VNĐ/phần hoặc người)

### Trải nghiệm nhà hàng (từ khoảng 100.000 VNĐ/người)

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

## Món đặc sản nền

8 file `local_specialties` đã curate, dùng làm nền cho guide:

- `bun bo hue.md`
- `com hen.md`
- `com am phu.md`
- `banh nam.md`
- `che heo quay.md`
- `banh ep.md`
- `me xung.md`
- `banh canh nam pho.md`

## Format gợi ý địa điểm

Trong prose hoặc bullet, dùng format tự nhiên:

```md
- Bún bò Huế phù hợp cho bữa sáng hoặc bữa chính nhẹ. Có thể tham khảo Quán
  bún bò Mệ Kéo (20 Bạch Đằng), Bún bò Hạnh (69 Đặng Văn Ngữ) hoặc Bún bò Cảnh
  Vân (206 Trịnh Công Sơn).
```

Không dùng file path trong body guide. Nếu sau này cần graph hoặc link nội bộ,
tạo sidecar/index riêng thay vì nhúng vào Markdown curated.

## Plan triển khai cho coding agent

1. Kiểm tra trạng thái repo.
   - Verify: chạy `git status --short` và không đụng thay đổi ngoài scope.

2. Đọc chuẩn hiện hành.
   - Verify: đọc `Session_Prompt.md`, `Project_Status.md`,
     `knowledge-base-hue/meta/foods-template.md` và file spec này.

3. Đối chiếu research với dữ liệu curated.
   - Verify: mỗi món/quán research được giữ trong guide phải có file curated
     tương ứng có tên và địa chỉ.

4. Trích danh sách quán đủ điều kiện.
   - Verify: mỗi quán được dùng trong guide phải có tên và địa chỉ trong file
     `restaurants/` hoặc `cafes/`.

5. Viết `food-guides.md` theo cấu trúc đã chốt.
   - Verify: file bắt đầu bằng `# Food Guides Huế`, không có YAML frontmatter,
     không có section `## Nguồn dữ liệu` riêng, không có file path nội bộ.

6. Kiểm tra duplicate và scope.
   - Verify: guide không copy mô tả dài từ `local_specialties`, `restaurants`
     hoặc `cafes`; mỗi món chỉ có diễn giải ngắn.

7. Chạy validation.
   - Verify: chạy `git diff --check` và kiểm tra thủ công các heading chính.

## Checklist acceptance

- `food-guides.md` là guide du lịch, không phải recipe collection.
- Có đủ phần theo thời điểm trong ngày, gồm cả ăn đêm.
- Có đủ phần theo ngân sách, kèm mức chi phí tham khảo từ research.
- Có đủ phần theo nhóm người dùng.
- Có đủ itinerary nửa ngày, 1 ngày, 2 ngày và 3 ngày.
- Gợi ý quán có tên và địa chỉ ngắn, đều thuộc dữ liệu curated.
- Không có source section riêng trong `food-guides.md`.
- Không có section rỗng, placeholder, hoặc câu báo thiếu dữ liệu.
- Không có file path nội bộ trong body guide.
