import { useEffect } from "react";
import { MOI_ANH } from "./anh.js";

export function GioiThieu({ banDo, anh, muc }) {
  // `#/gioi-thieu/<mục>` ⇒ cuộn tới mục (sau lần `scrollTo(0, 0)` của `useRoute` lúc đổi hash — effect chạy sau khi trang đã vẽ)
  useEffect(() => {
    if (muc) document.getElementById(muc)?.scrollIntoView();
  }, [muc]);
  return (
    <div className="khung khoi-trang gioi-thieu">
      <p className="vet"><a href="#/">Trang chủ</a> / Giới thiệu</p>
      <h1 className="trang-h">Về Trợ lý Huế</h1>
      <h2>Trợ lý làm được gì</h2>
      <ul>
        <li>Trả lời câu hỏi về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, đi lại và vé tham quan ở Huế.</li>
        <li>Xếp lịch tham quan theo buổi từ các điểm trong kho (khi tính năng Lên kế hoạch bật).</li>
        <li>Khi kho không có, có thể tra thêm trên web — phần đó ghi rõ “Từ web (chưa kiểm)”.</li>
        {anh && <li>Hỏi bằng ảnh: trợ lý gợi ý tên nơi / món trong ảnh (có thể sai), bạn bấm chọn đúng tên rồi mới hỏi.</li>}
      </ul>
      <h2>Trả lời từ kho, có nguồn</h2>
      <p>Mỗi câu trả lời lấy từ kho tư liệu về Huế và ghi tên tài liệu đã dùng ở dòng “Nguồn”. Bấm tên để xem đoạn gốc hoặc đọc cả bài ở mục Khám phá.</p>
      <h2>Giới hạn</h2>
      <ul>
        <li>Trợ lý có thể sai. Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại trước khi đi.</li>
        <li>{banDo ? "Chưa có nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau). Bản đồ lịch trình chỉ ghim các điểm đã có toạ độ."
          : "Chưa có bản đồ, nơi lưu trú, quán ăn theo vị trí và lịch sự kiện theo ngày (đợt sau)."}</li>
        <li>Câu hỏi ngoài chủ đề Huế sẽ được báo là ngoài phạm vi.</li>
      </ul>
      <h2>Dữ liệu của bạn</h2>
      <p>Trợ lý nhớ các câu hỏi trong một cuộc trò chuyện để hiểu câu hỏi tiếp theo: nhớ trong bộ nhớ máy chủ, tối đa 30 phút, qua một cookie chỉ dùng cho
        trò chuyện. Máy chủ không lưu chữ câu hỏi hay câu trả lời vào nhật ký. Nút “Cuộc trò chuyện mới” xoá phần đã nhớ.</p>
      <p>Để trả lời, câu hỏi được gửi tới dịch vụ mô hình AI (OpenAI); khi tra web, câu hỏi cũng được gửi tới dịch vụ tìm kiếm. Đừng gõ thông tin cá nhân
        vào câu hỏi.</p>
      {banDo && <p>Khi lịch có bản đồ, trình duyệt của bạn tải ảnh bản đồ từ máy chủ OpenStreetMap — máy chủ đó nhận địa chỉ IP và vùng bản đồ bạn
        đang xem (không nhận câu hỏi của bạn).</p>}
      {anh && <p>Ảnh bạn gửi được thu nhỏ, bỏ thông tin vị trí, gửi tới OpenAI để đoán tên, không lưu.</p>}
      <h2 id="nguon-anh">Nguồn ảnh</h2>
      <ul className="nguon-anh">
        {MOI_ANH.map(a => <li key={a.src}><GhiCong a={a} /></li>)}
      </ul>
    </div>
  );
}

function GhiCong({ a }) {
  const ngoai = { target: "_blank", rel: "noopener noreferrer" };
  return (
    <>
      {a.cho}. Ảnh: {a.tacGia}
      {a.giayPhep && <> · {a.linkGiayPhep ? <a href={a.linkGiayPhep} {...ngoai}>{a.giayPhep}</a> : a.giayPhep}</>}
      {" · "}<a href={a.nguon} {...ngoai}>{a.giayPhep ? "trang ảnh trên Wikimedia Commons" : "nguồn ảnh"}</a>
      {a.doi && <> · đã {a.doi}</>}
    </>
  );
}
