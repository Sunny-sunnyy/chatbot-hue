import { useEffect, useState } from "react";
import { BIEU_MAU } from "./chung.jsx";
import { LichV2 } from "./LichV2.jsx";
import { Feedback } from "./chat.jsx";
import "./lkh.css";

export function LenKeHoach({ bat, prefill, pending, onSubmit }) {
  const [chon, setChon] = useState(prefill || {});
  useEffect(() => { if (prefill) setChon(prefill); }, [prefill]);
  const du = BIEU_MAU.filter(t => t.bat_buoc).every(t => chon[t.ten]);
  const tomTat = BIEU_MAU.filter(t => chon[t.ten]).map(t => t.chon.find(([v]) => v === chon[t.ten])[1]).join(" · ");
  if (!bat) {
    return (
      <div className="khung khoi-trang">
        <h1 className="trang-h">Lên kế hoạch</h1>
        <p className="khoi-p">Tính năng này chưa bật. Bạn vẫn có thể hỏi <a href="#/tro-ly">Trợ lý Huế</a> về các điểm muốn đi.</p>
      </div>
    );
  }
  return (
    <div className="khung khoi-trang">
      <p className="vet"><a href="#/">Trang chủ</a> / Lên kế hoạch</p>
      <h1 className="trang-h">Lên kế hoạch đi Huế</h1>
      <p className="khoi-p">Trợ lý xếp lịch theo buổi từ các điểm trong kho. Muốn đổi lịch thì quay lại đây điền lại.</p>
      <form className="lc" onSubmit={e => { e.preventDefault(); if (du && !pending) onSubmit(Object.fromEntries(Object.entries(chon).filter(([, v]) => v)), tomTat); }}>
        {BIEU_MAU.map(t => (
          <fieldset key={t.ten} className="lc-nhom">
            <legend className="lc-ten">{t.nhan}{t.bat_buoc ? "" : " (không bắt buộc)"}</legend>
            <div className="lc-chip">
              {t.chon.map(([gia_tri, nhan]) => (
                <button key={gia_tri} type="button" className="chip chip-sm" aria-pressed={chon[t.ten] === gia_tri}
                        onClick={() => setChon(old => ({ ...old, [t.ten]: old[t.ten] === gia_tri ? undefined : gia_tri }))}>{nhan}</button>
              ))}
            </div>
          </fieldset>
        ))}
        <button className="nut nut-chinh lc-nut" type="submit" disabled={!du || pending}>
          {pending ? "Trợ lý đang trả lời…" : du ? `Xếp lịch ${tomTat.split(" · ")[0]}` : "Chọn số ngày để xếp lịch"}
        </button>
      </form>
    </div>
  );
}

// "Lên kế hoạch" bản 2 (plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md`, spec bản 3.3 §5) — chỉ khi server bật `len_ke_hoach_v2`.
// Bốn nhóm theo câu người đi tự hỏi; chỉ vẽ ô có trong `cauHinh.o_hien` (ô ẩn không có trong DOM); giá trị = đúng hợp đồng `truong` mới của server.
const KIEU_DI = [["nhe_nhang", "Nhẹ nhàng", "khoảng 2 điểm một ngày"], ["can_bang", "Cân bằng", "khoảng 3 điểm một ngày"],
                 ["kham_pha", "Khám phá nhiều", "tới 4 điểm một ngày"]];
const SO_THICH = BIEU_MAU.find(t => t.ten === "so_thich").chon;
const MAC_DINH_V2 = { so_ngay: 2, nguoi_lon: 2, tre_em: 0, lon_tuoi: false, kieu_di: null, so_thich: [], ngay_di: "" };

function ngayIso(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

// prefill = `truong` đã gửi (nút "Sửa") ⇒ về trạng thái biểu mẫu
function tuTruong(truong) {
  if (!truong) return MAC_DINH_V2;
  const st = truong.so_thich;
  return { ...MAC_DINH_V2, ...truong, so_ngay: Number(truong.so_ngay === "4+" ? 4 : truong.so_ngay || 2),
           so_thich: Array.isArray(st) ? st : st ? [st] : [], ngay_di: truong.ngay_di || "" };
}

function SoDem({ id, nhan, giaTri, min, max, onDoi }) {
  return (
    <div className="lc-dem">
      <span id={id}>{nhan}</span>
      <button type="button" className="chip chip-sm" aria-label={`Bớt ${nhan.toLowerCase()}`} disabled={giaTri <= min}
              onClick={() => onDoi(giaTri - 1)}>−</button>
      <output aria-labelledby={id} aria-live="polite">{giaTri}</output>
      <button type="button" className="chip chip-sm" aria-label={`Thêm ${nhan.toLowerCase()}`} disabled={giaTri >= max}
              onClick={() => onDoi(giaTri + 1)}>+</button>
    </div>
  );
}

// H1 (14/11): ô "Thích gì" có ảnh (bảng ảnh của C; nguồn chỉ ghi trong bảng dữ liệu, không hiện — User 14/11).
const ANH_THICH = { di_tich: "dai_noi", am_thuc: "cho_dong_ba", thien_nhien: "bach_ma", le_hoi_nghe_thuat: "duyet_thi_duong", chup_anh: "pha_tam_giang" };
const ANH_LICH = `${import.meta.env.BASE_URL}anh/lich/`;
const SO_CHAM = { nhe_nhang: 2, can_bang: 3, kham_pha: 4 };

// Cột phải: lượt lịch mới nhất của cuộc trò chuyện (cùng dữ liệu với khung trợ lý). Chưa có ⇒ lịch MẪU có nhãn "Ví dụ" (User 14/11: trang trống
// quá) — `/api/lich_mau` do chính bộ xếp dựng từ tổ hợp cố định, câu mỗi điểm do code; tải lỗi ⇒ ô xem trước chữ như cũ.
let taiMau = null;
function LichMau() {
  const [mau, setMau] = useState(null);
  useEffect(() => {
    let song = true;
    taiMau ??= fetch("/api/lich_mau").then(r => (r.ok ? r.json() : null)).catch(() => null);
    taiMau.then(kq => { if (song) setMau(kq); });
    return () => { song = false; };
  }, []);
  if (!mau?.lich) {
    return (
      <div className="lkh-trong">
        <p className="lkh-trong-h">Lịch của bạn sẽ hiện ở đây</p>
        <ul><li>Mỗi ngày chia sáng · chiều · tối, có giờ gợi ý</li><li>Mỗi điểm có một câu tả lấy từ bài trong kho, kèm nguồn</li>
          <li>Ghi chú mùa mưa, thời tiết (khi có ngày đi trong 7 ngày tới)</li></ul>
      </div>
    );
  }
  return (
    <div className="lkh-mau" aria-label="Lịch ví dụ">
      <p className="lkh-mau-dau"><span className="lkh-mau-nhan">Ví dụ</span> Lịch 2 ngày · 2 người lớn · thích di tích — bộ xếp lịch tạo sẵn.
        Lịch của bạn có thêm câu tả từng điểm lấy từ kho, kèm nguồn.</p>
      {/* ví dụ không có nút Sửa ⇒ bỏ đuôi "sai thì bấm Sửa" của dòng "Mình hiểu" */}
      <LichV2 turn={{ key: "mau", lichV2: { ...mau.lich, minh_hieu: mau.lich.minh_hieu.replace(/\s*—\s*sai thì bấm \*{0,2}Sửa\*{0,2}\.?$/, ".") }, cauV2: mau.cau, phase: "mau" }} />
    </div>
  );
}

function CotLich({ lichTurn, onEditPlan }) {
  if (!lichTurn) return <LichMau />;
  const t = lichTurn;
  const dangChay = !["done", "error", "stopped"].includes(t.phase);
  return (
    <div className="lkh-lich">
      {!t.lichV2 && t.progress?.length > 0 && (
        <ul className="progress" aria-label="Các bước xếp lịch">{t.progress.map((line, i) => <li key={i}>{line}</li>)}</ul>
      )}
      {!t.lichV2 && dangChay && <span className="lkh-go" role="status" aria-label="đang xếp lịch"><i /><i /><i /></span>}
      {t.error && <p className="loi" role="alert">{t.error}</p>}
      {t.lichV2 && t.phase !== "error" && <LichV2 turn={t} onEditPlan={onEditPlan} />}
      {t.phase === "done" && t.turnId && <Feedback turnId={t.turnId} />}
    </div>
  );
}

export function LenKeHoachV2({ cauHinh, prefill, pending, onSubmit, lichTurn, onEditPlan }) {
  const [chon, setChon] = useState(() => tuTruong(prefill));
  useEffect(() => { if (prefill) setChon(tuTruong(prefill)); }, [prefill]);
  const hien = new Set(cauHinh.o_hien);
  const doi = (ten, giaTri) => setChon(old => ({ ...old, [ten]: giaTri }));
  const homNay = new Date();
  const toiDa = new Date(homNay.getFullYear(), homNay.getMonth(), homNay.getDate() + 180);
  const soNgay = Math.min(chon.so_ngay, cauHinh.so_ngay_toi_da);

  const truong = { so_ngay: String(soNgay) };
  if (hien.has("nguoi_lon")) truong.nguoi_lon = chon.nguoi_lon;
  if (hien.has("tre_em")) truong.tre_em = chon.tre_em;
  if (hien.has("lon_tuoi")) truong.lon_tuoi = chon.lon_tuoi;
  if (hien.has("kieu_di") && chon.kieu_di) truong.kieu_di = chon.kieu_di;
  if (hien.has("so_thich") && chon.so_thich.length) truong.so_thich = chon.so_thich.slice(0, cauHinh.so_thich_toi_da);
  if (hien.has("ngay_di") && chon.ngay_di) truong.ngay_di = chon.ngay_di;

  const tomTat = [`${soNgay} ngày`,
    hien.has("nguoi_lon") && `${chon.nguoi_lon} người lớn`,
    hien.has("tre_em") && chon.tre_em > 0 && `${chon.tre_em} trẻ em`,
    hien.has("lon_tuoi") && chon.lon_tuoi && "có người lớn tuổi",
    truong.kieu_di && KIEU_DI.find(([v]) => v === truong.kieu_di)[1].toLowerCase(),
    truong.so_thich && `thích ${truong.so_thich.map(v => SO_THICH.find(([k]) => k === v)[1].toLowerCase()).join(", ")}`,
    truong.ngay_di && `đi ngày ${truong.ngay_di.split("-").reverse().join("/")}`].filter(Boolean).join(" · ");

  function bamSoThich(v) {
    setChon(old => {
      if (old.so_thich.includes(v)) return { ...old, so_thich: old.so_thich.filter(x => x !== v) };
      const moi = [...old.so_thich, v];
      return { ...old, so_thich: moi.slice(Math.max(0, moi.length - cauHinh.so_thich_toi_da)) };  // quá số cho phép ⇒ bỏ lựa chọn cũ nhất
    });
  }

  return (
    <>
    <section className="lkh-dau">
      <div className="khung">
        <p className="vet"><a href="#/">Trang chủ</a> / Lên kế hoạch</p>
        <h1 className="trang-h vao" style={{ "--n": 0 }}>Lên kế hoạch đi Huế</h1>
        <p className="khoi-p vao" style={{ "--n": 1 }}>Trợ lý xếp lịch theo buổi từ các điểm trong kho. Muốn đổi lịch thì điền lại biểu mẫu.</p>
      </div>
    </section>
    <div className="khung lkh-cot">
      <form className="lc" onSubmit={e => { e.preventDefault(); if (!pending) onSubmit(truong, tomTat); }}>
        {(hien.has("nguoi_lon") || hien.has("tre_em") || hien.has("lon_tuoi")) && (
          <fieldset className="lc-nhom">
            <legend className="lc-ten">Ai đi?</legend>
            <div className="lc-chip">
              {hien.has("nguoi_lon") && <SoDem id="lc-nguoi-lon" nhan="Người lớn" giaTri={chon.nguoi_lon} min={1} max={10} onDoi={v => doi("nguoi_lon", v)} />}
              {hien.has("tre_em") && <SoDem id="lc-tre-em" nhan="Trẻ em" giaTri={chon.tre_em} min={0} max={6} onDoi={v => doi("tre_em", v)} />}
              {hien.has("lon_tuoi") && (
                <label className="lc-hop"><input type="checkbox" checked={chon.lon_tuoi} onChange={e => doi("lon_tuoi", e.target.checked)} /> Có người lớn tuổi</label>
              )}
            </div>
          </fieldset>
        )}
        <fieldset className="lc-nhom">
          <legend className="lc-ten">Đi bao lâu, khi nào?</legend>
          <div className="lc-chip">
            <SoDem id="lc-so-ngay" nhan="Số ngày" giaTri={soNgay} min={1} max={cauHinh.so_ngay_toi_da} onDoi={v => doi("so_ngay", v)} />
            {hien.has("ngay_di") && (
              <label className="lc-hop">Ngày đi (không bắt buộc){" "}
                <input type="date" value={chon.ngay_di} min={ngayIso(homNay)} max={ngayIso(toiDa)} onChange={e => doi("ngay_di", e.target.value)} />
              </label>
            )}
          </div>
        </fieldset>
        {hien.has("kieu_di") && (
          <fieldset className="lc-nhom">
            <legend className="lc-ten">Đi kiểu nào? (không bắt buộc)</legend>
            <div className="lc-chip">
              {KIEU_DI.map(([v, nhan, giai]) => (
                <button key={v} type="button" className="chip chip-sm lkh-kieu" aria-pressed={chon.kieu_di === v}
                        onClick={() => doi("kieu_di", chon.kieu_di === v ? null : v)}>
                  <span className="lkh-cham" aria-hidden="true">{Array.from({ length: SO_CHAM[v] }, (_, i) => <i key={i} />)}</span>
                  <b>{nhan}</b> <span>{giai}</span>
                </button>
              ))}
            </div>
            {chon.kieu_di && chon.kieu_di !== "nhe_nhang" && (chon.tre_em > 0 || chon.lon_tuoi) && (
              <p className="lc-tom">Có trẻ em hoặc người lớn tuổi: lịch giữ mức nhẹ nhàng, mỗi buổi một điểm.</p>
            )}
          </fieldset>
        )}
        {hien.has("so_thich") && (
          <fieldset className="lc-nhom">
            <legend className="lc-ten">Thích gì? {cauHinh.so_thich_toi_da > 1 ? `(tối đa ${cauHinh.so_thich_toi_da})` : "(chọn một)"}</legend>
            <div className="lc-chip">
              {SO_THICH.filter(([v]) => cauHinh.so_thich_hien.includes(v)).map(([v, nhan]) => (
                <button key={v} type="button" className="chip chip-sm lkh-thich" aria-pressed={chon.so_thich.includes(v)} onClick={() => bamSoThich(v)}>
                  {ANH_THICH[v] && <img src={`${ANH_LICH}${ANH_THICH[v]}.jpg`} alt="" loading="lazy" />}<span>{nhan}</span>
                </button>
              ))}
            </div>
          </fieldset>
        )}
        <p className="lc-tom" aria-live="polite">{tomTat}</p>
        <button className="nut nut-chinh lc-nut" type="submit" disabled={pending}>{pending ? "Trợ lý đang trả lời…" : `Xếp lịch ${soNgay} ngày`}</button>
      </form>
      <CotLich lichTurn={lichTurn} onEditPlan={onEditPlan} />
    </div>
    </>
  );
}
