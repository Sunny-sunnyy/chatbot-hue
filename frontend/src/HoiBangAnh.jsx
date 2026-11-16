import { useEffect, useRef, useState } from "react";

// Phase 10 — hỏi bằng ảnh, P1 v1 dạng GỢI Ý có xác nhận (User chọn 05/11 sau A2: âm theo tiêu chí gốc, User đổi thước vì có bước xác nhận).
// Ảnh ⇒ `POST /api/anh/ung_vien` (thân = bytes ảnh, không multipart — spec A10) ⇒ 1–3 tên trong danh sách do code dựng ⇒ người dùng BẤM một tên
// ⇒ code ghép câu (spec A3) ⇒ hỏi như câu gõ. Model trả lời không bao giờ nhìn ảnh (câu trả lời từ kho, theo TÊN). Tách file riêng (spec A8).
// Từ 15/11 tối: bước "BẤM một tên" chỉ còn khi có 2–3 tên — xem khối ghi chú trước `useHoiBangAnh`.

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
// User 15/11: nút chữ nằm riêng một hàng tốn chỗ ⇒ nút dấu cộng TRONG ô nhập + dán ảnh thẳng vào ô.
// User 15/11 (tối): ảnh là tệp ĐÍNH KÈM của tin nhắn — chọn / dán ảnh thì hệ thống CHƯA làm gì (0 lần gọi API), ảnh nhỏ nằm trong ô nhập;
// người dùng gõ câu (hoặc để trống) rồi bấm Hỏi ⇒ lúc đó mới gửi ảnh đi nhận diện ⇒ thẻ xác nhận tên ⇒ bấm tên ⇒ gửi câu đã gõ kèm tên.
// User 15/11 (tối, sau khi thử + xem số đếm: bước nhận ảnh trả 1 tên thì đúng 31 / 33, trả 2–3 tên thì tên đầu chỉ đúng ~65 %) — PHƯƠNG ÁN LAI:
// đúng MỘT tên ⇒ không bắt bấm: TỰ hỏi ngay câu ghép (câu trả lời vẫn từ kho, có nguồn — model trả lời không nhìn ảnh) + thẻ gọn không chặn
// "Mình đoán trong ảnh là … — có thể sai" + nút gõ tên; 2–3 tên ⇒ GIỮ thẻ chọn tên (bấm Hỏi lúc thẻ mở ⇒ dòng nhắc). Không tên / lỗi ⇒ lời báo.
// Hook trả: `nut` (dấu cộng) + `kem` (ảnh nhỏ có nút ×) đặt trong ô nhập, `the` (thẻ chờ / xác nhận / lời báo) đặt trên ô nhập, `onPaste`
// gắn vào ô gõ, `gui()` gọi khi bấm Hỏi — trả true nếu lượt này do ảnh xử lý (ô nhập không gửi câu trần). Cờ tắt ⇒ tất cả rỗng.
export function useHoiBangAnh({ bat, draft, disabled, onAsk, onGoTen }) {
  // null · {phase: "kem", file, preview} (đã đính kèm, chưa gửi gì) · {phase: "dang" | "loi", preview, text}
  // · {phase: "xong", preview, ungVien (2–3 tên chờ chọn), anh, nhac} · {phase: "doan", chon (tên duy nhất đã tự hỏi)}; `anh` = URL ảnh cho bong bóng
  const [state, setState] = useState(null);
  const inputRef = useRef(null);
  const rootRef = useRef(null);
  // Lượt nhận ảnh chạy qua `await` ⇒ lúc tên về, mọi thứ lấy từ lần vẽ lúc bấm Hỏi đã cũ (review C M-1). `luot` tăng mỗi khi người dùng bỏ / thay
  // ảnh hoặc mở cuộc mới ⇒ kết quả của lượt cũ bị bỏ; `moi` luôn giữ `disabled` / `onAsk` / `draft` của lần vẽ MỚI NHẤT.
  const luot = useRef(0);
  const moi = useRef({});
  moi.current = { disabled, onAsk, draft };

  useEffect(() => () => { if (state?.preview) URL.revokeObjectURL(state.preview); }, [state?.preview]);
  // Trang trợ lý: khung nhập dính đáy màn hình (sticky) và thẻ nằm trong khung ⇒ thẻ hiện là đè lên cuối câu trả lời đang đọc
  // (E bật ảnh 08/11, Playwright 1440 + 390). Cuộn trang xuống đáy ⇒ khung về đúng chỗ của nó, cuối cuộc trò chuyện nằm ngay trên thẻ.
  useEffect(() => {
    if (state && rootRef.current?.closest(".tro-ly-trang")) window.scrollTo({ top: document.documentElement.scrollHeight });
  }, [state?.phase]);

  if (!bat) return { nut: null, kem: null, the: null, onPaste: undefined, gui: () => false, xoa: () => {} };

  // Huỷ lúc "Đang xem ảnh…" (User 16/11): lượt đang chạy bị bỏ qua khi kết quả về (luot tăng), ảnh quay lại thành tệp đính kèm
  // để người dùng sửa câu rồi bấm Hỏi gửi lại, hoặc bấm × bỏ ảnh. Server vẫn chạy xong lượt cũ — chỉ giao diện bỏ kết quả.
  function huy() {
    luot.current += 1;
    setState({ phase: "kem", file: state.file, preview: state.preview });
  }

  function dong(goTen) {
    luot.current += 1;
    setState(null);
    if (goTen) onGoTen();
  }

  function chonAnh(event) {
    const file = event.target.files?.[0];
    event.target.value = "";  // chọn lại cùng file vẫn chạy
    if (file) dinhKem(file);
  }

  function onPaste(event) {
    // Dán ẢNH (chụp màn hình, "sao chép hình ảnh") ⇒ cùng luồng với chọn file. Clipboard có chữ (kể cả khi kèm ảnh — bảng tính, trình soạn văn bản
    // chép chữ kèm một ảnh chụp) ⇒ để trình duyệt dán chữ như thường.
    const cb = event.clipboardData;
    const file = [...(cb?.files ?? [])].find(f => f.type.startsWith("image/"));
    if (!file || cb.getData("text/plain")) return;
    event.preventDefault();
    if (!disabled && state?.phase !== "dang") dinhKem(file);
  }

  function dinhKem(file) {
    // Kiểu / cỡ sai báo NGAY, kiểm ở trình duyệt. Hợp lệ ⇒ chỉ giữ ảnh ở trình duyệt (một ảnh mỗi câu — ảnh mới thay ảnh cũ), chưa gọi API.
    if (!KIEU.includes(file.type)) return setState({ phase: "loi", text: "Chọn ảnh JPEG, PNG hoặc WEBP." });
    if (file.size > MAX_BYTES) return setState({ phase: "loi", text: "Ảnh lớn hơn 10 MB — chọn ảnh nhỏ hơn." });
    luot.current += 1;
    setState({ phase: "kem", file, preview: URL.createObjectURL(file) });
  }

  function gui() {
    if (state?.phase === "kem") {
      nhanAnh(state.file, state.preview);
      return true;
    }
    if (state?.phase === "dang") return true;  // đang xem ảnh ⇒ chờ, không gửi câu trần
    if (state?.phase === "xong") {  // thẻ chọn tên đang mở mà bấm Hỏi ⇒ không gửi câu trần, nhắc chọn tên (không nhắc thì trông như bị treo)
      setState({ ...state, nhac: true });
      return true;
    }
    if (state) setState(null);  // thẻ "mình đoán…" / lời báo còn mở ⇒ đóng, câu gõ đi như câu thường (thẻ không chặn câu kế)
    return false;
  }

  async function nhanAnh(file, preview) {
    const toi = ++luot.current;
    setState({ file, preview, phase: "dang" });  // giữ `file` để nút Huỷ trả ảnh về ô nhập
    let ungVien = [];
    try {
      const r = await fetch("/api/anh/ung_vien", { method: "POST", headers: { "Content-Type": file.type }, body: file });
      ungVien = (r.ok ? await r.json() : null)?.ung_vien ?? [];
    } catch { /* lỗi mạng ⇒ như chưa nhận ra */ }
    if (toi !== luot.current) return;  // trong lúc chờ người dùng đã bỏ ảnh / mở cuộc mới ⇒ không làm gì với kết quả cũ
    if (!ungVien.length) return setState({ preview, phase: "loi", text: KHONG_NHAN_RA });
    // URL riêng cho bong bóng câu hỏi (sống theo cuộc trò chuyện); `preview` của ô nhập được thu hồi khi state đổi
    const anh = URL.createObjectURL(file);
    // 2–3 tên ⇒ người dùng chọn (chữ đang gõ giữ trong ô). Một tên mà lúc này đang có lượt khác chạy (bấm câu gợi ý / "Hỏi lại" trong lúc chờ)
    // ⇒ KHÔNG tự hỏi chen ngang: hiện thẻ chọn với một tên, người dùng bấm khi lượt kia xong.
    if (ungVien.length > 1 || moi.current.disabled) return setState({ preview, phase: "xong", ungVien, anh });
    setState({ phase: "doan", chon: ungVien[0].ten });
    hoiVoiTen(ungVien[0].ten, moi.current.draft, anh, true);  // chữ trong ô LÚC TÊN VỀ (gõ thêm trong lúc chờ không bị mất)
  }

  // `doan` = tên do hệ thống TỰ chọn (một tên) ⇒ lượt đó có dòng "Mình đoán trong ảnh là … — có thể sai" ngay đầu câu trả lời (giao diện chèn,
  // không vào chuỗi gửi model); tên người dùng tự bấm chọn (2–3 tên) thì không cần dòng này
  function hoiVoiTen(ten, chu, anh, doan = false) {
    // bong bóng câu hỏi hiện ảnh + đúng chữ người dùng gõ (không đuôi "(Trong ảnh: …)"); ô rỗng ⇒ hiện câu mặc định
    moi.current.onAsk(cauGhep(chu, ten), { chu: chu.trim() || cauGhep(chu, ten), anh, doan: doan ? ten : null });
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
  const kem = state?.phase === "kem" && (
    <span className="anh-kem">
      <img src={state.preview} alt="Ảnh đính kèm" />
      <button type="button" aria-label="Bỏ ảnh" title="Bỏ ảnh" onClick={() => setState(null)}>×</button>
    </span>
  );
  const the = state && state.phase !== "kem" && (
    <div className="hoi-anh" ref={rootRef}>
      <div className="bubble hoi-anh-the" role="status">
        {state.preview && <img src={state.preview} alt="Ảnh bạn vừa chọn" className="hoi-anh-xem" />}
        {state.phase === "dang" && (
          <div className="flex flex-wrap items-center gap-2">
            <p>Đang xem ảnh…</p>
            <button type="button" className="retry" onClick={huy}>Huỷ</button>
          </div>
        )}
        {state.phase === "loi" && <p>{state.text}</p>}
        {state.phase === "doan" && (
          <div className="hoi-anh-doan">
            <span>Mình đoán trong ảnh là <b>{state.chon}</b> — có thể sai.</span>
            <button type="button" className="retry" onClick={() => dong(true)}>Không đúng — tôi gõ tên</button>
          </div>
        )}
        {state.phase === "xong" && (
          <>
            <p className="mb-2 font-semibold text-accent-deep">Trong ảnh là (có thể sai) — chọn đúng tên:</p>
            <div className="flex flex-wrap gap-2">
              {state.ungVien.map(u => (
                <button key={u.id} type="button" className="send" disabled={disabled}
                        onClick={() => { dong(false); hoiVoiTen(u.ten, draft, state.anh); }}>{u.ten}</button>
              ))}
            </div>
          </>
        )}
        {state.nhac && <p role="alert" className="pt-2 font-semibold text-accent-deep">Chọn một tên ở trên để mình trả lời.</p>}
        {(state.phase === "xong" || state.phase === "loi") && (
          <div className="flex flex-wrap gap-2 pt-2">
            {state.phase === "xong" && <button type="button" className="retry" onClick={() => dong(true)}>Không phải các tên này — tôi gõ tên</button>}
            {state.phase === "loi" && <button type="button" className="retry" onClick={() => dong(true)}>Gõ tên</button>}
          </div>
        )}
      </div>
    </div>
  );
  return { nut, kem, the, onPaste, gui, xoa: () => { luot.current += 1; setState(null); } };  // `xoa`: "Cuộc trò chuyện mới" gỡ ảnh đính kèm + đóng thẻ
}
