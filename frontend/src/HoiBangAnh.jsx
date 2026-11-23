import { useEffect, useRef, useState } from "react";

// Phase 10 — hỏi bằng ảnh, P1 v1 dạng GỢI Ý có xác nhận (User chọn 05/11 sau A2: âm theo tiêu chí gốc, User đổi thước vì có bước xác nhận).
// Ảnh ⇒ `POST /api/anh/ung_vien` (thân = bytes ảnh, không multipart — spec A10) ⇒ 1–3 tên trong danh sách do code dựng ⇒ người dùng BẤM một tên
// ⇒ code ghép câu (spec A3) ⇒ hỏi như câu gõ. Model trả lời không bao giờ nhìn ảnh (câu trả lời từ kho, theo TÊN). Tách file riêng (spec A8).
// Từ 15/11 tối: bước "BẤM một tên" chỉ còn khi có 2–3 tên. Từ 23/11/2026 (tối): KHÔNG còn bước bấm tên nào chặn câu hỏi — xem khối ghi chú trước
// `useHoiBangAnh`.

const KIEU = ["image/jpeg", "image/png", "image/webp"];
const MAX_BYTES = 10 * 1024 * 1024;  // khớp `anh.max_bytes` server — báo sớm thay vì gửi rồi nhận 413
const MAX_QUERY = 500;  // `ChatRequest.query` max_length
const KHONG_NHAN_RA = "Mình chưa nhận ra ảnh này — bạn gõ tên nơi / món bạn muốn hỏi nhé.";
// Khung "chưa nhận ra" đang mở mà người dùng gửi chữ ⇒ câu đi kèm tên này ở đuôi "(Trong ảnh: …)", như khi nhận ra. Vì sao (23/11/2026, hai lượt thật):
// gửi ảnh A (nhận ra) rồi ảnh B (không nhận ra) rồi gõ "đây là đâu vậy?" — câu đi như câu thường, không dấu gì về ảnh ⇒ trợ lý lấy câu trả lời liền
// trước và khẳng định ảnh B là nơi của ảnh A. Bong bóng câu hỏi vẫn chỉ hiện chữ người dùng gõ.
const TEN_CHUA_NHAN_RA = "ảnh vừa gửi chưa nhận ra được là nơi / món nào — không phải nơi hay món của các câu trước";

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
// Chủ dự án 23/11/2026 (tối, sau khi tự test — nguyên văn `data/loi_user/2026-11-23.md`): "tôi muốn bấm hỏi thì sẽ gửi cho hệ thống là cả ảnh và câu
// [hỏi] luôn, chứ không phải là để người dùng chọn… người dùng có biết gì đâu mà chọn, biết thì cần gì gửi ảnh để hỏi đây là món gì ?" ⇒ THAY phương án
// lai và thẻ xác nhận trước của tên dễ nhầm: 1–3 tên ⇒ TỰ hỏi ngay với tên ĐẦU (đếm trên 73 ảnh có nhãn: ảnh của nơi có trong danh sách mà model trả
// 2–3 tên thì tên đầu đúng 24 / 25 lần trên model đang chạy, 6 / 7 trên model cũ); dòng đoán ở đầu câu trả lời nêu cả các tên còn lại; thẻ gọn KHÔNG
// chặn dưới câu trả lời có nút "Hỏi lại với: <tên kia>" (hỏi lại đúng câu đã gõ) và "Không phải — tôi gõ tên". Cái giá đã báo chủ dự án: ảnh của nơi
// KHÔNG có trong danh sách nhưng giống một tên trong danh sách nay được trả lời thẳng về tên đó (trả lời về sai nơi 3 ⇒ 14 / 73 ảnh của bộ đo).
// Thẻ chọn tên chỉ còn ở MỘT ca: tên về lúc đang có lượt khác chạy (không tự hỏi chen ngang).
// Hook trả: `nut` (dấu cộng) + `kem` (ảnh nhỏ có nút ×) đặt trong ô nhập, `the` (thẻ chờ / xác nhận / lời báo) đặt trên ô nhập, `onPaste`
// gắn vào ô gõ, `gui()` gọi khi bấm Hỏi — trả true nếu lượt này do ảnh xử lý (ô nhập không gửi câu trần). Cờ tắt ⇒ tất cả rỗng.
export function useHoiBangAnh({ bat, draft, disabled, onAsk, onGoTen }) {
  // null · {phase: "kem", file, preview} (đã đính kèm, chưa gửi gì) · {phase: "dang" | "loi", preview, text}
  // · {phase: "xong", preview, ungVien (tên về lúc đang bận ⇒ chờ bấm), anh, nhac}
  // · {phase: "doan", chon (tên đang được trả lời), khac (các tên còn lại ⇒ nút "Hỏi lại với"), chu (câu đã gõ lúc hỏi), anh, tuChon (true = hệ thống
  //   tự lấy tên đầu; false = người dùng vừa bấm "Hỏi lại với")}; `anh` = URL ảnh cho bong bóng
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

  // Người dùng bấm "Không phải các tên này" ở thẻ chọn tên ⇒ với họ ảnh này CHƯA được nhận ra: mở đúng khung "chưa nhận ra" (không đóng trắng) để câu
  // gõ kế mang đuôi "(Trong ảnh: … chưa nhận ra …)". Đóng trắng thì câu đi như câu thường và trợ lý có thể trả lời theo nơi của ảnh / câu TRƯỚC —
  // cùng lỗi đã chữa 23/11/2026 ở khung "chưa nhận ra"; thẻ xác nhận của tên dễ nhầm (cầu khác được gợi ý là "Cầu Trường Tiền") đi đúng đường này.
  // Từ 23/11/2026 (tối) nút "Không phải — tôi gõ tên" của thẻ đoán (dưới câu trả lời) cũng đi đường này: câu trả lời vừa rồi nói về SAI nơi, nên câu gõ
  // kế càng phải mang đuôi "chưa nhận ra" để trợ lý không bám vào nơi đó.
  function khongPhai() {
    luot.current += 1;
    setState({ preview: state.preview, phase: "loi", text: KHONG_NHAN_RA });
    onGoTen();
  }

  // "Hỏi lại với: <tên kia>" — hỏi lại ĐÚNG câu đã gõ lúc gửi ảnh, với tên người dùng vừa bấm. Tên đó VẪN là tên hệ thống đoán từ ảnh (ứng viên thứ hai /
  // ba) — người dùng bấm vì thấy câu đầu sai chứ không phải vì biết — nên câu trả lời của lượt này cũng mang dòng "Mình đoán trong ảnh là … — có thể
  // sai" (người đọc code nêu 23/11/2026: không có thì thứ ở lại trong cuộc trò chuyện là một câu nói chắc đứng cạnh ảnh). Tên vừa bị thay quay về hàng nút.
  function hoiLai(ten) {
    setState({ ...state, chon: ten, khac: [state.chon, ...state.khac.filter(t => t !== ten)], tuChon: false });
    hoiVoiTen(ten, state.chu, state.anh, []);  // `[]` = có dòng đoán, không nêu thêm tên nào
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
    if (state?.phase === "loi" && state.text === KHONG_NHAN_RA && moi.current.draft.trim()) {
      setState(null);
      const chu = moi.current.draft.trim();
      moi.current.onAsk(cauGhep(chu, TEN_CHUA_NHAN_RA), { chu, anh: null, doan: null });
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
    // URL riêng cho bong bóng câu hỏi — KHÔNG thu hồi ở đâu cả (sống tới khi tải lại trang; rò nhỏ có sẵn), nên lượt "Hỏi lại với" dùng lại được;
    // `preview` của ô nhập thì được thu hồi khi state đổi
    const anh = URL.createObjectURL(file);
    // Lúc tên về mà đang có lượt khác chạy (bấm câu gợi ý / "Hỏi lại" trong lúc chờ) ⇒ KHÔNG tự hỏi chen ngang: hiện thẻ tên, người dùng bấm khi lượt
    // kia xong (chữ đang gõ giữ trong ô). Đây là ca DUY NHẤT còn thẻ chờ bấm.
    if (moi.current.disabled) return setState({ preview, phase: "xong", ungVien, anh });
    // Mọi ca còn lại — 1, 2 hay 3 tên, kể cả tên mang `xac_nhan_truoc` (cờ còn trong danh sách, giao diện không dùng nữa): TỰ hỏi ngay với tên ĐẦU.
    const chu = moi.current.draft;  // chữ trong ô LÚC TÊN VỀ (gõ thêm trong lúc chờ không bị mất)
    const khac = ungVien.slice(1).map(u => u.ten);
    setState({ phase: "doan", chon: ungVien[0].ten, khac, chu, anh, tuChon: true });
    hoiVoiTen(ungVien[0].ten, chu, anh, khac);
  }

  // `khac` khác null = tên do hệ thống ĐOÁN từ ảnh mà người dùng chưa xác nhận (tên đầu tự lấy; tên bấm ở nút "Hỏi lại với") ⇒ lượt đó có dòng "Mình
  // đoán trong ảnh là … — có thể sai" ngay đầu câu trả lời, nêu cả các tên trong `khac` (giao diện chèn, không vào chuỗi gửi model); chỉ tên người
  // dùng bấm ở thẻ chờ lúc bận (họ nhìn danh sách rồi chọn TRƯỚC khi có câu trả lời nào) là không có dòng này
  function hoiVoiTen(ten, chu, anh, khac = null) {
    // bong bóng câu hỏi hiện ảnh + đúng chữ người dùng gõ (không đuôi "(Trong ảnh: …)"); ô rỗng ⇒ hiện câu mặc định
    moi.current.onAsk(cauGhep(chu, ten), { chu: chu.trim() || cauGhep(chu, ten), anh, doan: khac ? ten : null, doanKhac: khac ?? [] });
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
            <span>{state.tuChon ? <>Mình đoán trong ảnh là <b>{state.chon}</b> — có thể sai.</> : <>Đang trả lời theo tên bạn chọn: <b>{state.chon}</b>.</>}</span>
            {state.khac.map(ten => (
              <button key={ten} type="button" className="retry" disabled={disabled} onClick={() => hoiLai(ten)}>Hỏi lại với: {ten}</button>
            ))}
            <button type="button" className="retry" onClick={khongPhai}>Không phải — tôi gõ tên</button>
          </div>
        )}
        {state.phase === "xong" && (
          <>
            {/* Chỉ còn khi tên về lúc đang có lượt khác chạy. MỘT tên ⇒ hỏi thẳng có / không; 2–3 tên ⇒ mời chọn (lượt trình duyệt 23/11/2026:
                chữ "chọn đúng tên" + "các tên này" đọc cụt và sai số khi thẻ chỉ có một nút) */}
            <p className="mb-2 font-semibold text-accent-deep">{state.ungVien.length === 1
              ? "Trong ảnh có phải là tên dưới đây không? (mình có thể đoán sai)" : "Trong ảnh là (có thể sai) — chọn đúng tên:"}</p>
            <div className="flex flex-wrap gap-2">
              {state.ungVien.map(u => (
                <button key={u.id} type="button" className="send" disabled={disabled}
                        onClick={() => { dong(false); hoiVoiTen(u.ten, draft, state.anh); }}>{u.ten}</button>
              ))}
            </div>
          </>
        )}
        {state.nhac && <p role="alert" className="pt-2 font-semibold text-accent-deep">{state.ungVien?.length === 1
          ? "Đúng thì bấm vào tên ở trên để mình trả lời." : "Chọn một tên ở trên để mình trả lời."}</p>}
        {(state.phase === "xong" || state.phase === "loi") && (
          <div className="flex flex-wrap gap-2 pt-2">
            {state.phase === "xong" && <button type="button" className="retry" onClick={khongPhai}>{state.ungVien.length === 1 ? "Không phải — tôi gõ tên" : "Không phải các tên này — tôi gõ tên"}</button>}
            {state.phase === "loi" && <button type="button" className="retry" onClick={() => dong(true)}>Gõ tên</button>}
          </div>
        )}
      </div>
    </div>
  );
  return { nut, kem, the, onPaste, gui, xoa: () => { luot.current += 1; setState(null); } };  // `xoa`: "Cuộc trò chuyện mới" gỡ ảnh đính kèm + đóng thẻ
}
