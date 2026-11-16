// Nguồn ô bản đồ lịch do server gửi trong `/api/tinh_nang` (khoá `ban_do`, chỉ có khi cờ `ban_do_lich` bật; host ghi một chỗ ở
// `backend/api/routes/cong.py` `BAN_DO`, cùng nguồn với CSP). App ghi một lần lúc tải trang; `BanDoLich.jsx` đọc lúc vẽ.
let nguon = null;
export const datNguonBanDo = v => { nguon = v ?? null; };
export const nguonBanDo = () => nguon;
