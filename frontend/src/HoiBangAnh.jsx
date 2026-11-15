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

// Chỉ hiện nút khi server bật tính năng (cờ `anh.bat`): cổng đợt 1 đọc cờ một lần ở `/api/tinh_nang` (App) thay vì dò `GET /api/anh/ung_vien` —
// dò ra 404 thành lỗi console mỗi lần mở trợ lý (Q-G đòi 0 lỗi console).
// User 15/11: nút chữ nằm riêng một hàng tốn chỗ ⇒ nút dấu cộng TRONG ô nhập + dán ảnh thẳng vào ô. Vì nút và thẻ gợi ý nằm ở hai chỗ khác nhau
// của khung nhập nên đây là hook trả ba mảnh: `nut` (đặt trong ô nhập), `the` (thẻ gợi ý, đặt trên ô nhập), `onPaste` (gắn vào ô gõ).
// Cờ tắt ⇒ cả ba rỗng: không nút, dán ảnh không làm gì.
export function useHoiBangAnh({ bat, draft, disabled, onAsk, onGoTen }) {
  const [state, setState] = useState(null);  // null · {preview, phase: "dang" | "xong" | "loi", ungVien, text}
  const inputRef = useRef(null);
  const rootRef = useRef(null);

  useEffect(() => () => state?.preview && URL.revokeObjectURL(state.preview), [state?.preview]);
  // Trang trợ lý: khung nhập dính đáy màn hình (sticky) và thẻ nằm trong khung ⇒ thẻ hiện là đè lên cuối câu trả lời đang đọc
  // (E bật ảnh 08/11, Playwright 1440 + 390). Cuộn trang xuống đáy ⇒ khung về đúng chỗ của nó, cuối cuộc trò chuyện nằm ngay trên thẻ.
  useEffect(() => {
    if (state && rootRef.current?.closest(".tro-ly-trang")) window.scrollTo({ top: document.documentElement.scrollHeight });
  }, [state?.phase]);

  if (!bat) return { nut: null, the: null, onPaste: undefined };

  function dong(goTen) {
    setState(null);
    if (goTen) onGoTen();
  }

  function chonAnh(event) {
    const file = event.target.files?.[0];
    event.target.value = "";  // chọn lại cùng file vẫn chạy
    if (file) nhanAnh(file);
  }

  function onPaste(event) {
    // Dán ẢNH (chụp màn hình, "sao chép hình ảnh") ⇒ cùng luồng với chọn file. Clipboard có chữ (kể cả khi kèm ảnh — bảng tính, trình soạn văn bản
    // chép chữ kèm một ảnh chụp) ⇒ để trình duyệt dán chữ như thường.
    const cb = event.clipboardData;
    const file = [...(cb?.files ?? [])].find(f => f.type.startsWith("image/"));
    if (!file || cb.getData("text/plain")) return;
    event.preventDefault();
    if (!disabled && state?.phase !== "dang") nhanAnh(file);
  }

  async function nhanAnh(file) {
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

  const nut = (
    <>
      <button type="button" className="nut-anh" aria-label="Hỏi bằng ảnh" title="Hỏi bằng ảnh" disabled={disabled || state?.phase === "dang"}
              onClick={() => inputRef.current?.click()}>
        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <path d="M12 5v14M5 12h14" />
        </svg>
      </button>
      <input ref={inputRef} type="file" accept={KIEU.join(",")} className="sr-only" tabIndex={-1} aria-hidden="true" onChange={chonAnh} />
    </>
  );
  const the = state && (
    <div className="hoi-anh" ref={rootRef}>
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
    </div>
  );
  return { nut, the, onPaste };
}
