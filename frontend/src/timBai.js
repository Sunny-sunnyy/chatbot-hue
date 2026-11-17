// Ô tìm của trang Khám phá (hàm thuần, test bằng node: `backend/tests/test_tim_bai.py`). So bằng tiêu đề bỏ dấu (gõ thiếu dấu vẫn ra), nhưng bài khớp
// ĐÚNG DẤU đứng trước: tối 16/11 tìm "lăng" ra 12 bài "làng…" trước các lăng, "chè" ra "Điện Hòn Chén". Không bỏ bài nào — chỉ đổi thứ tự;
// trong mỗi nhóm giữ thứ tự gốc của danh sách.
export function boDau(s) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();
}

const coDau = s => s.normalize("NFC").toLowerCase();

export function timBai(bai, tim) {
  const q = tim.trim();
  if (!q) return bai;
  const qBo = boDau(q), qDau = coDau(q);
  const dung = [], gan = [];
  for (const b of bai) {
    if (coDau(b.tieu_de).includes(qDau)) dung.push(b);
    else if (boDau(b.tieu_de).includes(qBo)) gan.push(b);
  }
  return [...dung, ...gan];
}
