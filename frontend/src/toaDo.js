// Kiểm toạ độ phía trình duyệt (dùng chung `chat.jsx` + `BanDoLich.jsx` — review E m-2): đúng 2 số hữu hạn trong khung Huế, như server
// (`lich_trinh.KHUNG_HUE`); sai ⇒ coi như chưa có toạ độ. File nhỏ ở bundle chính ⇒ lịch không có toạ độ hợp lệ không tải chunk bản đồ.
export function toaDoHopLe(td) {
  return Array.isArray(td) && td.length === 2 && td.every(Number.isFinite) && td[0] >= 16 && td[0] <= 16.8 && td[1] >= 107 && td[1] <= 108;
}
