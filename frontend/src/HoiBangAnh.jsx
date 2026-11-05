import { useEffect, useRef, useState } from "react";

// Phase 10 — hỏi bằng ảnh, P1 v1 dạng GỢI Ý có xác nhận (User chọn 05/11 sau A2: âm theo tiêu chí gốc, User đổi thước vì có bước xác nhận).
// Ảnh ⇒ `POST /api/anh/ung_vien` (thân = bytes ảnh, không multipart — spec A10) ⇒ 1–3 tên trong danh sách do code dựng ⇒ người dùng BẤM một tên
// ⇒ code ghép câu (spec A3) ⇒ hỏi như câu gõ. Trợ lý không bao giờ trả lời thẳng từ ảnh. Tách file riêng để ít chồng `App.jsx` (spec A8).

const KIEU = ["image/jpeg", "image/png", "image/webp"];
const MAX_BYTES = 10 * 1024 * 1024;  // khớp `anh.max_bytes` server — báo sớm thay vì gửi rồi nhận 413
const MAX_QUERY = 500;  // `ChatRequest.query` max_length
const KHONG_NHAN_RA = "Mình chưa nhận ra ảnh này — bạn gõ tên nơi / món bạn muốn hỏi nhé.";

export function cauGhep(chu, ten) {
  // spec A3: có chữ người dùng gõ kèm ⇒ "<chữ> (Trong ảnh: <tên>)"; không ⇒ "Giới thiệu về <tên>". Quá 500 ký tự ⇒ cắt phần chữ người dùng.
  const duoi = ` (Trong ảnh: ${ten})`;
  const goc = chu.trim();
  return goc ? goc.slice(0, MAX_QUERY - duoi.length) + duoi : `Giới thiệu về ${ten}`;
}

export default function HoiBangAnh({ draft, disabled, onAsk, onGoTen }) {
  const [bat, setBat] = useState(false);
  const [state, setState] = useState(null);  // null · {preview, phase: "dang" | "xong" | "loi", ungVien, text}
  const inputRef = useRef(null);

  // Chỉ hiện nút khi server bật tính năng (cờ `anh.bat`; tắt ⇒ 404).
  useEffect(() => {
    fetch("/api/anh/ung_vien").then(r => setBat(r.ok)).catch(() => setBat(false));
  }, []);
  useEffect(() => () => state?.preview && URL.revokeObjectURL(state.preview), [state?.preview]);

  if (!bat) return null;

  function dong(goTen) {
    setState(null);
    if (goTen) onGoTen();
  }

  async function chonAnh(event) {
    const file = event.target.files?.[0];
    event.target.value = "";  // chọn lại cùng file vẫn chạy
    if (!file) return;
    if (!KIEU.includes(file.type)) return setState({ phase: "loi", text: "Chọn ảnh JPEG, PNG hoặc WEBP." });
    if (file.size > MAX_BYTES) return setState({ phase: "loi", text: "Ảnh lớn hơn 10 MB — chọn ảnh nhỏ hơn." });
    const preview = URL.createObjectURL(file);
    setState({ preview, phase: "dang" });
    try {
      const r = await fetch("/api/anh/ung_vien", { method: "POST", headers: { "Content-Type": file.type }, body: file });
      const data = r.ok ? await r.json() : null;
      const ungVien = data?.ung_vien ?? [];
      setState({ preview, phase: ungVien.length ? "xong" : "loi", ungVien, text: ungVien.length ? "" : KHONG_NHAN_RA });
    } catch {
      setState({ preview, phase: "loi", text: KHONG_NHAN_RA });
    }
  }

  return (
    <div className="hoi-anh">
      <div className="flex flex-wrap items-center gap-3">
        <button type="button" className="retry hoi-anh-nut" disabled={disabled || state?.phase === "dang"} onClick={() => inputRef.current?.click()}>
          Hỏi bằng ảnh
        </button>
        <span className="text-[13px] text-muted">Ảnh được gửi tới OpenAI để đoán tên nơi / món; máy chủ này không lưu ảnh. Tránh chụp mặt người lạ.</span>
        <input ref={inputRef} type="file" accept={KIEU.join(",")} className="sr-only" tabIndex={-1} aria-hidden="true" onChange={chonAnh} />
      </div>
      {state && (
        <div className="bubble hoi-anh-the" role="status">
          {state.preview && <img src={state.preview} alt="Ảnh bạn vừa chọn" className="hoi-anh-xem" />}
          {state.phase === "dang" && <p>Đang nhận diện ảnh…</p>}
          {state.phase === "loi" && <p>{state.text}</p>}
          {state.phase === "xong" && (
            <>
              <p className="mb-2 font-semibold text-accent-deep">Gợi ý từ ảnh, có thể sai — chọn đúng tên:</p>
              <div className="flex flex-wrap gap-2">
                {state.ungVien.map(u => (
                  <button key={u.id} type="button" className="send" disabled={disabled}
                          onClick={() => { dong(false); onAsk(cauGhep(draft, u.ten)); }}>{u.ten}</button>
                ))}
              </div>
            </>
          )}
          {state.phase !== "dang" && (
            <div className="flex flex-wrap gap-2 pt-2">
              {state.phase === "xong" && <button type="button" className="retry" onClick={() => dong(true)}>Không phải các tên này — tôi gõ tên</button>}
              {state.phase === "loi" && <button type="button" className="retry" onClick={() => dong(true)}>Gõ tên</button>}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
