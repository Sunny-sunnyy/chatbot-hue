// Xuất lịch .ics (việc agent (4), plan `docs/superpowers/plans/2026-11-14-xuat-lich-ics-plan.md`, A duyệt 14/11).
// Hàm thuần: dựng tệp iCalendar (RFC 5545) từ KHUNG lịch do code xếp (tên, ngày, giờ) — chữ model chỉ vào phần mô tả, không làm dữ kiện.
// Giờ Việt Nam UTC+7 (không giờ mùa hè) ⇒ ghi giờ UTC "…Z". Không gửi gì đi đâu: trình duyệt tải về như nút "Tải về (.txt)".

const LECH_UTC_PHUT = 7 * 60;
const NHAC = "Giờ gợi ý theo thời lượng tham quan — kiểm lại giờ mở cửa trước khi đi.";
const GIO = /(\d{1,2}):(\d{2})/g;

// "8:00 – 10:30" ⇒ [480, 630]; "suất 19:00 / 20:00 / 21:00, khoảng 1 giờ" ⇒ [1140, 1200, true] (suất đầu, 60 phút); không đọc được ⇒ null
export function docGio(gio) {
  if (typeof gio !== "string") return null;
  const so = [...gio.matchAll(GIO)].map(m => Number(m[1]) * 60 + Number(m[2])).filter(p => p >= 0 && p < 24 * 60);
  if (so.length === 0) return null;
  if (/suất/i.test(gio)) return [so[0], so[0] + 60, true];
  if (so.length >= 2 && so[1] > so[0]) return [so[0], so[1], false];
  return null;
}

function utc(ngayIso, phut) {
  const [y, m, d] = ngayIso.split("-").map(Number);
  const t = new Date(Date.UTC(y, m - 1, d, 0, phut - LECH_UTC_PHUT));
  const p = (n, k = 2) => String(n).padStart(k, "0");
  return `${t.getUTCFullYear()}${p(t.getUTCMonth() + 1)}${p(t.getUTCDate())}T${p(t.getUTCHours())}${p(t.getUTCMinutes())}00Z`;
}

// RFC 5545 3.3.11: thoát \ ; , và xuống dòng
export function thoat(s) {
  return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n");
}

// RFC 5545 3.1: mỗi dòng ≤ 75 byte (UTF-8), dòng tiếp bắt đầu bằng một dấu cách; không cắt giữa một ký tự
export function gap(dong) {
  const enc = new TextEncoder();
  const ra = [];
  let hien = "", byte = 0, gioiHan = 75;
  for (const ky of dong) {
    const n = enc.encode(ky).length;
    if (byte + n > gioiHan) { ra.push(hien); hien = " "; byte = 1; gioiHan = 75; }
    hien += ky; byte += n;
  }
  ra.push(hien);
  return ra.join("\r\n");
}

// lich = `lichV2` (khung), cau = {id_muc: câu đã qua kiểm} (mã [n] đã bỏ), dauThoiGian = Date (DTSTAMP) ⇒ { ics, soSuKien, soBo } hoặc null khi không có ngày đi
export function dungIcs(lich, cau, dauThoiGian = new Date()) {
  if (!lich?.ngay?.length || !lich.ngay.every(ng => ng.ngay_thang)) return null;
  const stamp = dauThoiGian.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z");
  const dong = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Tro ly Hue//Len ke hoach//VI", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
    `X-WR-CALNAME:${thoat(`Lịch Huế ${lich.ngay.length} ngày từ ${lich.ngay[0].ngay_thang.split("-").reverse().join("/")}`)}`];
  let soSuKien = 0, soBo = 0;
  for (const ng of lich.ngay) {
    for (const m of ng.muc) {
      if (m.loai !== "tham_quan" && m.loai !== "hoat_dong_toi") continue;
      const g = docGio(m.gio);
      if (!g) { soBo += 1; continue; }
      const [bd, kt, suat] = g;
      const moTa = [cau?.[m.id_muc], NHAC, suat ? "Có nhiều suất — chọn suất khác nếu cần." : null, m.map_url].filter(Boolean).join("\n");
      dong.push("BEGIN:VEVENT", `UID:${lich.ngay[0].ngay_thang}-${m.id_muc}@tro-ly-hue`, `DTSTAMP:${stamp}`,
        `DTSTART:${utc(ng.ngay_thang, bd)}`, `DTEND:${utc(ng.ngay_thang, kt)}`, `SUMMARY:${thoat(m.ten)}`,
        `LOCATION:${thoat(`${m.ten}, Huế`)}`, `DESCRIPTION:${thoat(moTa)}`, "END:VEVENT");
      soSuKien += 1;
    }
  }
  dong.push("END:VCALENDAR");
  return { ics: dong.map(gap).join("\r\n") + "\r\n", soSuKien, soBo };
}
