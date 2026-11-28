// Xuất lịch .ics (việc agent (4), plan `docs/superpowers/plans/2026-11-14-xuat-lich-ics-plan.md`, A duyệt 14/11).
// Hàm thuần: dựng tệp iCalendar (RFC 5545) từ KHUNG lịch do code xếp (tên, ngày, giờ) — chữ model chỉ vào phần mô tả, không làm dữ kiện.
// Bản v1 (giữ nguyên khi `xuat_nang_cao` tắt) + bản v2 (`dungIcsV2`, đồng bộ với `backend/api/lich_ics.py`).

const LECH_UTC_PHUT = 7 * 60;
const TZID = "Asia/Ho_Chi_Minh";
const NHAC = "Giờ gợi ý theo thời lượng tham quan — kiểm lại giờ mở cửa trước khi đi.";
const NHAC_CA_NGAY = "Chưa có khung giờ cố định — kiểm lại giờ mở cửa trước khi đi.";
const DISCLAIMER_O_DAU = "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống.";
const MAP_PREFIX = "https://www.google.com/maps/search/";
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

// v2: hỗ trợ cả mục 1 mốc giờ (mặc định 90 phút tham quan / 60 phút tối)
export function docGioV2(gio, loai = "tham_quan") {
  if (typeof gio !== "string" || !gio.trim()) return null;
  const so = [...gio.matchAll(GIO)].map(m => Number(m[1]) * 60 + Number(m[2])).filter(p => p >= 0 && p < 24 * 60);
  if (so.length === 0) return null;
  if (/suất/i.test(gio)) return [so[0], so[0] + 60, true];
  if (so.length >= 2 && so[1] > so[0]) return [so[0], so[1], false];
  const thoiLuong = loai === "hoat_dong_toi" ? 60 : 90;
  return [so[0], so[0] + thoiLuong, false];
}

function utc(ngayIso, phut) {
  const [y, m, d] = ngayIso.split("-").map(Number);
  const t = new Date(Date.UTC(y, m - 1, d, 0, phut - LECH_UTC_PHUT));
  const p = (n, k = 2) => String(n).padStart(k, "0");
  return `${t.getUTCFullYear()}${p(t.getUTCMonth() + 1)}${p(t.getUTCDate())}T${p(t.getUTCHours())}${p(t.getUTCMinutes())}00Z`;
}

function gioDiaPhuong(ngayIso, phut) {
  const [y, m, d] = ngayIso.split("-").map(Number);
  const t = new Date(Date.UTC(y, m - 1, d, 0, phut));
  const p = (n, k = 2) => String(n).padStart(k, "0");
  return `${t.getUTCFullYear()}${p(t.getUTCMonth() + 1)}${p(t.getUTCDate())}T${p(t.getUTCHours())}${p(t.getUTCMinutes())}00`;
}

function ngaySo(ngayIso, congNgay = 0) {
  const [y, m, d] = ngayIso.split("-").map(Number);
  const t = new Date(Date.UTC(y, m - 1, d + congNgay));
  const p = (n, k = 2) => String(n).padStart(k, "0");
  return `${t.getUTCFullYear()}${p(t.getUTCMonth() + 1)}${p(t.getUTCDate())}`;
}

function bamOnDinh(lich) {
  const chu = JSON.stringify({ ngay: (lich?.ngay || []).map(n => ({ n: n.ngay, d: n.ngay_thang, m: n.muc.map(x => [x.id_muc, x.ten, x.gio]) })), o_dau: lich?.o_dau?.khu || null });
  let h = 2166136261;
  for (let i = 0; i < chu.length; i += 1) {
    h ^= chu.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0).toString(16).padStart(8, "0");
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
// anToan = câu an toàn của lượt (bão / lũ: bản tin chính thức + 112) nếu có ⇒ đứng ĐẦU phần mô tả của mọi sự kiện; không có ⇒ tệp y như trước
export function dungIcs(lich, cau, dauThoiGian = new Date(), anToan = null) {
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
      const moTa = [anToan, m.ghi_chu, cau?.[m.id_muc], NHAC, suat ? "Có nhiều suất — chọn suất khác nếu cần." : null, m.map_url].filter(Boolean).join("\n");
      dong.push("BEGIN:VEVENT", `UID:${lich.ngay[0].ngay_thang}-${m.id_muc}@tro-ly-hue`, `DTSTAMP:${stamp}`,
        `DTSTART:${utc(ng.ngay_thang, bd)}`, `DTEND:${utc(ng.ngay_thang, kt)}`, `SUMMARY:${thoat(m.ten)}`,
        `LOCATION:${thoat(`${m.ten}, Huế`)}`, `DESCRIPTION:${thoat(moTa.replaceAll("**", ""))}`, "END:VEVENT");
      soSuKien += 1;
    }
  }
  dong.push("END:VCALENDAR");
  return { ics: dong.map(gap).join("\r\n") + "\r\n", soSuKien, soBo };
}

// v2: đồng bộ với backend/api/lich_ics.py
export function dungIcsV2(lich, cau, dauThoiGian = new Date(), anToan = null) {
  if (!lich?.ngay?.length || !lich.tham_so?.ngay_di || !lich.ngay.every(ng => ng.ngay_thang)) return null;
  const stamp = dauThoiGian.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z");
  const ngayDau = lich.ngay[0].ngay_thang;
  const dong = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Tro ly Hue//Len ke hoach v2//VI", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
    `X-WR-CALNAME:${thoat(`Lịch Huế ${lich.ngay.length} ngày từ ${lich.ngay[0].ngay_thang.split("-").reverse().join("/")}`)}`,
    `X-WR-TIMEZONE:${TZID}`,
    "BEGIN:VTIMEZONE", `TZID:${TZID}`, `X-LIC-LOCATION:${TZID}`,
    "BEGIN:STANDARD", "TZOFFSETFROM:+0700", "TZOFFSETTO:+0700", "TZNAME:+07", "DTSTART:19700101T000000", "END:STANDARD",
    "END:VTIMEZONE",
  ];
  let soSuKien = 0, soCaNgay = 0;
  for (const ng of lich.ngay) {
    for (const m of ng.muc) {
      if (m.loai !== "tham_quan" && m.loai !== "hoat_dong_toi") continue;
      const g = docGioV2(m.gio, m.loai);
      const coMap = typeof m.map_url === "string" && m.map_url.startsWith(MAP_PREFIX);
      if (!g) {
        const moTa = [anToan, m.ghi_chu, cau?.[m.id_muc], NHAC_CA_NGAY, coMap ? m.map_url : null].filter(Boolean).join("\n");
        dong.push(
          "BEGIN:VEVENT", `UID:${ngayDau}-${m.id_muc}@tro-ly-hue`, "SEQUENCE:0", `DTSTAMP:${stamp}`,
          `DTSTART;VALUE=DATE:${ngaySo(ng.ngay_thang)}`, `DTEND;VALUE=DATE:${ngaySo(ng.ngay_thang, 1)}`,
          `SUMMARY:${thoat(m.ten)}`, `LOCATION:${thoat(`${m.ten}, Huế`)}`, `DESCRIPTION:${thoat(moTa.replaceAll("**", ""))}`,
          ...(coMap ? [`URL;VALUE=URI:${m.map_url}`] : []),
          "END:VEVENT",
        );
        soCaNgay += 1;
      } else {
        const [bd, kt, suat] = g;
        const moTa = [anToan, m.ghi_chu, cau?.[m.id_muc], NHAC, suat ? "Có nhiều suất — chọn suất khác nếu cần." : null, coMap ? m.map_url : null].filter(Boolean).join("\n");
        dong.push(
          "BEGIN:VEVENT", `UID:${ngayDau}-${m.id_muc}@tro-ly-hue`, "SEQUENCE:0", `DTSTAMP:${stamp}`,
          `DTSTART;TZID=${TZID}:${gioDiaPhuong(ng.ngay_thang, bd)}`, `DTEND;TZID=${TZID}:${gioDiaPhuong(ng.ngay_thang, kt)}`,
          `SUMMARY:${thoat(m.ten)}`, `LOCATION:${thoat(`${m.ten}, Huế`)}`, `DESCRIPTION:${thoat(moTa.replaceAll("**", ""))}`,
          ...(coMap ? [`URL;VALUE=URI:${m.map_url}`] : []),
          "END:VEVENT",
        );
      }
      soSuKien += 1;
    }
  }
  const oDau = lich.o_dau;
  if (oDau?.co_so?.length && lich.ngay.length >= 2) {
    const tenKhu = oDau.ten_khu || "Huế";
    const tenDau = oDau.co_so[0]?.ten || tenKhu;
    const dsTen = oDau.co_so.slice(0, 3).filter(c => c.ten).map(c => `${c.ten}${c.dia_chi ? ` (${c.dia_chi})` : ""}`).join("; ");
    const nhan = (oDau.nhan || DISCLAIMER_O_DAU).includes("chưa kiểm giá, phòng trống") ? (oDau.nhan || DISCLAIMER_O_DAU) : `${oDau.nhan} (${DISCLAIMER_O_DAU})`;
    const dauMap = oDau.co_so.find(c => typeof c.map_url === "string" && c.map_url.startsWith(MAP_PREFIX))?.map_url;
    for (const [ma, td, ngayIso, bd, kt] of [
      ["checkin", `Nhận phòng gợi ý — ${tenDau}`, lich.ngay[0].ngay_thang, 14 * 60, 15 * 60],
      ["checkout", `Trả phòng gợi ý — ${tenDau}`, lich.ngay[lich.ngay.length - 1].ngay_thang, 11 * 60, 12 * 60],
    ]) {
      const moTa = [anToan, `Khu gợi ý: ${tenKhu}.`, dsTen ? `Cơ sở tham khảo: ${dsTen}.` : null, nhan].filter(Boolean).join("\n");
      dong.push(
        "BEGIN:VEVENT", `UID:${ngayDau}-${ma}@tro-ly-hue`, "SEQUENCE:0", `DTSTAMP:${stamp}`,
        `DTSTART;TZID=${TZID}:${gioDiaPhuong(ngayIso, bd)}`, `DTEND;TZID=${TZID}:${gioDiaPhuong(ngayIso, kt)}`,
        `SUMMARY:${thoat(td)}`, `LOCATION:${thoat(`${tenKhu}, Huế`)}`, `DESCRIPTION:${thoat(moTa.replaceAll("**", ""))}`,
        ...(dauMap ? [`URL;VALUE=URI:${dauMap}`] : []),
        "END:VEVENT",
      );
      soSuKien += 1;
    }
  }
  dong.push("END:VCALENDAR");
  return { ics: dong.map(gap).join("\r\n") + "\r\n", soSuKien, soBo: 0, soCaNgay };
}
