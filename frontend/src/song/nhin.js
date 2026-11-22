// Giao diện "Dòng sông dẫn đường" (X13): hai hàm nhỏ chỉ phục vụ lớp NHÌN — không đổi chữ, không đổi dữ liệu.
// Chủ đề của một bài kho theo thư mục đầu của mã bài — để tô màu chấm nguồn (màu mang nghĩa: ẩm thực, di tích, lễ hội, đi lại, nghệ thuật).
export const linhVuc = baiId => (typeof baiId === "string" ? baiId.split("/")[0] : "");

// Con số người ta dò tìm trong câu trả lời: số tiền ("200.000 đồng", "1,2 triệu đồng") và khung giờ ("07:00 – 17:30", "7h30"). Chỉ bọc thẻ để vẽ đậm, chữ số đều cột.
const SO = /\d{1,3}(?:\.\d{3})+(?:\s*(?:đồng|VNĐ|đ)(?![\p{L}]))?|\d+(?:[.,]\d+)?\s*(?:nghìn|triệu)(?:\s*đồng)?|\d{1,2}(?::|h)\d{2}(?:\s*[–-]\s*\d{1,2}(?::|h)\d{2})?/gu;

// Sau khi chữ trả lời (đã qua bộ lọc) vào trang: gắn lớp cho khối "Tư liệu chưa có thông tin về…" và bọc các con số. Chạy lại được nhiều lần (bỏ qua phần đã bọc).
export function trangTriTraLoi(el) {
  if (!el) return;
  el.querySelectorAll("p, li").forEach(n => {
    if (!n.textContent.trim().startsWith("Tư liệu chưa có thông tin về")) return;
    n.classList.add("y-thieu");
    const sau = n.nextElementSibling;  // dòng mở đầu + danh sách gạch đầu dòng ngay dưới = MỘT khối
    if (n.tagName === "P" && n.textContent.trim().endsWith(":") && sau?.tagName === "UL") { n.classList.add("y-thieu-dau"); sau.classList.add("y-thieu-ds"); }
  });
  const duyet = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const nut = [];
  while (duyet.nextNode()) {
    const t = duyet.currentNode;
    if (t.parentElement.closest(".so, a, code, pre, .y-thieu, .y-thieu-ds")) continue;
    SO.lastIndex = 0;
    if (SO.test(t.nodeValue)) nut.push(t);
  }
  for (const t of nut) {
    const manh = document.createDocumentFragment();
    let cuoi = 0;
    SO.lastIndex = 0;
    for (const m of t.nodeValue.matchAll(SO)) {
      manh.append(t.nodeValue.slice(cuoi, m.index));
      const b = document.createElement("span");
      b.className = "so";
      b.textContent = m[0];
      manh.append(b);
      cuoi = m.index + m[0].length;
    }
    manh.append(t.nodeValue.slice(cuoi));
    t.replaceWith(manh);
  }
}
