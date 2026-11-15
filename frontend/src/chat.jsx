import { Suspense, lazy, useEffect, useMemo, useRef, useState } from "react";
import { displayNumbers, renderAnswerHtml, renderWebHtml } from "./markdown.js";
import { streamAnswer } from "./stream.js";
import { useHoiBangAnh } from "./HoiBangAnh.jsx";  // Phase 10: hỏi bằng ảnh (gợi ý có xác nhận) — chỉ hiện khi server bật cờ `anh.bat`
// Bản đồ lịch trình (plan 2026-11-08): chunk riêng — chỉ tải khi lịch có ≥ 1 toạ độ hợp lệ (server chỉ gửi `toa_do` khi cờ `ban_do_lich` bật)
const BanDoLich = lazy(() => import("./BanDoLich.jsx"));
import { toaDoHopLe } from "./toaDo.js";
import { SourceLine } from "./SourceLine.jsx";
import { anhTraLoi } from "./anhTraLoi.js";
import { phangCoSo, theKhachSan } from "./theKhachSan.js";
import { baiHref } from "./route.js";
import "./tl.css";
import { GOI_Y } from "./chung.jsx";
import { LINK_TIM_PHONG, LichV2, LuuLich, MAP_PREFIX, vanBanLich } from "./LichV2.jsx";

// Trợ lý Huế: một cuộc trò chuyện dùng chung cho khung nổi và trang `#/tro-ly` (cổng D8). Server giữ lịch sử (cookie HttpOnly `conversation_id`)
// — trang chỉ vẽ lại các lượt đã hỏi, không gửi lại lịch sử (plan B3 D1). State nằm ở `useChat` (gọi một lần ở App) ⇒ chuyển trang không ngắt lượt.

const STATUS_TEXT = {
  routing: "Đang hiểu câu hỏi…",  // Phase 9 B1: lần gọi định tuyến
  searching: "Đang tìm trong kho…",
  searched: "Đã tìm trong kho, đang chuẩn bị câu trả lời…",
  generating: "Đang viết câu trả lời…",
  lich_trinh: "Đang xếp lịch…",  // Phase 9 B5 D14: code đang xếp lịch
  tra_web: "Kho chưa có — đang tra web…",  // Phase 9 B6 D6: cổng web mở sau câu từ chối của kho
  thoi_tiet: "Đang xem dự báo thời tiết…",  // Phase 9 B5b: công cụ thời tiết đang chạy
  sua_lich: "Đang hiểu yêu cầu sửa lịch…",  // sửa lịch bản 2: cuộc có lịch ⇒ một lần hiểu ý trước khi trả lời
};
const WEB_LINK = /^https?:\/\//;  // B6: link nguồn web do server dựng từ sổ — trình duyệt kiểm lại gốc trước khi vẽ
// B5 D14 (c): nhãn cố định của từng bước code đã làm (sự kiện `status` stage `lich_trinh`); tên điểm + lý do lấy từ dữ liệu sự kiện, không chữ model.
const LICH_BUOC = {
  xep_xong: d => `Đã xếp lịch (${d.n_diem} điểm)`,
  kiem_luat_ok: () => "Đã kiểm luật xếp ✓",
  kiem_luat_loi: d => `Kiểm luật xếp: ${d.n_loi} lỗi`,
  bo_diem: d => d.ly_do,
  lay_nguon: d => `Đã lấy tài liệu cho từng điểm (${d.n_doan} đoạn mới)`,
};
const PENDING = new Set(Object.keys(STATUS_TEXT));
// User 15/11: trong lúc chờ chỉ hiện MỘT dòng — bước đang chạy (sự kiện `status` thật của server); có chữ trả lời ⇒ dòng biến mất, không để lại
// danh sách "Các bước". Đổi thành false ⇒ lúc chờ chỉ còn ba chấm "đang gõ" (nhãn trạng thái vẫn có cho trình đọc màn hình).
const HIEN_BUOC_LUC_CHO = true;
const NEW_CONVERSATION_ERROR = "Chưa bắt đầu được cuộc trò chuyện mới. Vui lòng thử lại.";
// B142: câu ngoài phạm vi kèm 3 câu gợi ý cố định (đã kiểm có trong kho bằng `scripts/grep_kb.sh`) — bấm là hỏi luôn.
const OUT_OF_SCOPE_SUGGESTIONS = ["Vào Đại Nội nên mặc thế nào?", "Lễ hội Điện Huệ Nam diễn ra khi nào?", "Nhã nhạc cung đình diễn lúc nào?"];
const MAX_QUERY = 500;  // khớp `ChatRequest.query` max_length (server: quá ⇒ 422 "Yêu cầu không hợp lệ")
const DEM_KY_TU_TU = 450;  // từ đây hiện bộ đếm ký tự
// Việc nhỏ (5) 08/11: dưới câu từ chối của kho — gợi ý cách hỏi cố định do code viết (không gọi model). Mục cuối là link sang Khám phá.
const REFUSAL_TIPS = ["Gõ đúng tên nơi, món hay lễ hội bạn muốn hỏi (tên riêng giúp tìm đúng tài liệu).",
                      "Câu có nhiều ý thì tách thành từng câu ngắn, mỗi câu một ý."];

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

// Một lượt: { key, question, phase (routing / searching / searched / generating / done / error), text, sources (null = chưa có sự kiện
// `sources`; [] = không nguồn), numbers (thứ tự nguồn ở dòng Nguồn), nSources, notice, outcome (từ `done`), error, … }.
function newTurn(key, question, truong, summary, bieuMau) {
  // lượt thường bắt đầu ở "đang hiểu câu hỏi" (định tuyến — B1); lượt biểu mẫu không định tuyến ⇒ "đang xếp lịch"
  return { key, question, phase: bieuMau ? "lich_trinh" : "routing", text: "", sources: null, numbers: null, nSources: null, notice: "", outcome: null,
           turnId: null, error: "", clarify: null, truong, summary, bieuMau, progress: [], lich: null, web: null, tuChoiKho: false, buoc: [] };
}

export function useChat() {
  const [turns, setTurns] = useState([]);
  const [draft, setDraft] = useState("");
  const [resetError, setResetError] = useState("");
  const [resetting, setResetting] = useState(false);
  const keyRef = useRef(0);
  const bufferRef = useRef("");
  const lastSeqRef = useRef(0);
  const frameRef = useRef(0);
  const abortRef = useRef(null);
  const stoppedRef = useRef(null);  // controller của lượt người dùng bấm "Dừng" (phân biệt với huỷ khi rời trang)
  const pending = turns.length > 0 && PENDING.has(turns[turns.length - 1].phase);

  // Rời trang / đóng tab ⇒ huỷ `fetch` để server dừng model (yêu cầu 17). Chuyển trang hash KHÔNG huỷ (cùng một trang).
  useEffect(() => {
    const abort = () => abortRef.current?.abort();
    window.addEventListener("pagehide", abort);
    return () => {
      window.removeEventListener("pagehide", abort);
      abort();
    };
  }, []);

  function stopFrame() {
    cancelAnimationFrame(frameRef.current);
    frameRef.current = 0;
  }

  // `truong` (B4 / biểu mẫu) + `summary` (tóm tắt lựa chọn hiện cạnh câu hỏi) + `bieuMau` (cổng D3). Trả false khi đang bận (không gửi).
  async function ask(value, { retryKey = null, truong = null, summary = "", bieuMau = false, suaChon = null } = {}) {
    const query = value.trim();
    if (!query || pending || resetting) return false;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    stopFrame();
    bufferRef.current = "";
    lastSeqRef.current = 0;
    const key = ++keyRef.current;
    const update = patch => setTurns(all => all.map(turn => (turn.key === key ? { ...turn, ...patch } : turn)));
    const progress = [];  // B5 D14: các bước lịch đã nhận của lượt này, đúng thứ tự server gửi
    const buoc = [];  // H1: bước công cụ thật (`status`), gộp bước lặp liền nhau
    const themBuoc = (stage, n) => {
      const cuoi = buoc[buoc.length - 1];
      if (cuoi && cuoi.stage === stage) { if (n != null) cuoi.n = n; } else buoc.push({ stage, n });
      return buoc.map(b => ({ ...b }));
    };
    const cauV2 = {};  // "Lên kế hoạch" bản 2: câu theo id_muc của lượt này
    // "Thử lại" thay lượt lỗi (server không nhớ lượt lỗi — plan B3 D2) bằng lượt mới cùng câu hỏi.
    setTurns(all => [...all.filter(turn => turn.key !== retryKey), newTurn(key, query, truong, summary, bieuMau)]);
    setResetError("");
    try {
      await streamAnswer(query, {
        signal: controller.signal,
        truong,
        bieuMau,
        suaChon,
        onEvent(name, data) {
          if (name === "status" && data.stage === "lich_trinh") {
            const text = LICH_BUOC[data.buoc]?.(data);  // "dang_xep" chỉ là nhãn trạng thái, không vào danh sách bước (C191 m-1)
            if (text) progress.push(text);
            update({ phase: "lich_trinh", progress: [...progress], buoc: themBuoc("lich_trinh") });
          } else if (name === "status") {
            // chỉ các nhãn đã biết; trạng thái lạ giữ nhãn "đã tìm" (B1 review C129 m-3); `n_sources` có ở `searched`
            const stage = data.stage in STATUS_TEXT ? data.stage : "searched";
            update({ phase: stage, ...(data.n_sources != null && { nSources: data.n_sources }), buoc: themBuoc(stage, data.n_sources) });
          } else if (name === "delta") {
            // Chữ hiện dần: gom mảnh vào buffer, vẽ lại CẢ buffer tối đa một lần mỗi khung hình (yêu cầu 8); chỉ nối mảnh có `seq` mới (yêu cầu 4).
            if (data.seq <= lastSeqRef.current) return;
            lastSeqRef.current = data.seq;
            bufferRef.current += data.text;
            if (!frameRef.current) {
              frameRef.current = requestAnimationFrame(() => {
                frameRef.current = 0;
                update({ text: bufferRef.current });
              });
            }
          } else if (name === "sources") {
            // Chữ đã qua bộ kiểm trích dẫn: vẽ bản cuối rồi mới hiện dòng Nguồn (yêu cầu 9; cổng D1).
            stopFrame();
            update({ text: bufferRef.current, sources: data, numbers: displayNumbers(bufferRef.current, data) });
          } else if (name === "notice") {
            update({ notice: data.text });
          } else if (name === "sua_the") {
            update({ suaThe: data });  // sửa lịch: thẻ chọn điểm thay — nút chỉ chứa id code đưa
          } else if (name === "clarify") {
            update({ clarify: data });  // B4 D8: thẻ hỏi lại — code dựng nút từ danh sách trường
          } else if (name === "lich_khung") {
            update({ lichV2: data, cauV2: {} });  // "Lên kế hoạch" bản 2: khung do code dựng hiện ngay, trước lần gọi model
          } else if (name === "lich_cau") {
            cauV2[data.id_muc] = data.cau;  // câu đã qua kiểm (hoặc câu dự phòng) của đúng một mục — đổ vào theo id
            update({ cauV2: { ...cauV2 } });
          } else if (name === "lich_xong") {
            update({ soDuPhong: data.so_cau_du_phong });
          } else if (name === "lich_trinh") {
            update({ lich: data });  // B5 D11 / D12: link bản đồ từng điểm + thẻ "Sửa" chọn sẵn (dữ liệu code)
          } else if (name === "web") {
            update({ web: data });  // B6 D6: chữ đã kiểm cuối + nguồn web (link do server dựng)
          } else if (name === "done") {
            // B142: mã lượt chỉ có ở lượt có câu trả lời cuối; (5) `tu_choi_kho`: kho không đủ ⇒ gợi ý cách hỏi
            update({ outcome: data.outcome, turnId: data.turn_id ?? null, tuChoiKho: data.tu_choi_kho === true });
          }
        },
      });
      update({ phase: "done" });
    } catch (failure) {
      if (failure.name === "AbortError") {
        // (7) người dùng bấm "Dừng": chữ đã hiện CHƯA qua kiểm trích dẫn ⇒ xoá như luật D3 (rút lại khi kiểm cuối hỏng), báo "đã dừng" + "Hỏi lại".
        // Server thấy ngắt ⇒ huỷ lần gọi model, không nhớ lượt này (`client_disconnected` ∉ REMEMBERED_OUTCOMES). Rời trang ⇒ không còn ai xem.
        if (stoppedRef.current === controller) {
          stopFrame();
          update({ phase: "stopped", text: "", sources: null, numbers: null, notice: "", web: null, clarify: null, lich: null, progress: [],
                   lichV2: null, cauV2: null });
        }
        return true;
      }
      // D3: kiểm cuối hỏng (rút lại) hoặc lỗi / đứt giữa chừng (xoá hết) — xoá chữ + nguồn đã hiện, hiện lời báo + "Thử lại" (yêu cầu 10, 11).
      stopFrame();
      update({ phase: "error", text: "", sources: null, numbers: null, notice: "", web: null, error: failure.message, lichV2: null, cauV2: null });
    }
    return true;
  }

  function stop() {
    if (!pending) return;
    stoppedRef.current = abortRef.current;
    abortRef.current?.abort();
  }

  // "Cuộc trò chuyện mới": server xoá lịch sử trước rồi trang mới xoá màn hình — lỗi ⇒ giữ nguyên màn hình, để thứ người dùng thấy khớp thứ
  // trợ lý còn nhớ.
  async function startNewConversation() {
    if (pending || resetting) return;
    setResetting(true);
    setResetError("");
    try {
      const response = await fetch("/api/conversation/new", { method: "POST" });
      if (!response.ok) throw new Error(String(response.status));
      setTurns([]);
      setDraft("");
    } catch {
      setResetError(NEW_CONVERSATION_ERROR);
    } finally {
      setResetting(false);
    }
  }

  return { turns, draft, setDraft, pending, resetting, resetError, ask, stop, startNewConversation };
}

// Trang `#/tro-ly` (H1, đợt 1): cột trái = câu gợi ý theo chủ đề + trợ lý làm được gì + lưu ý; phải = khung chat (cùng `ChatView` với khung nổi).
// Câu gợi ý = `GOI_Y` (chung.jsx) — mỗi câu một biểu tượng / màu theo chủ đề; điện thoại ẩn cột trái (lời chào trong khung vẫn có gợi ý).
const CHU_DE = [
  { mau: ["#FBE7DC", "#9A3412"], d: "M3 11h18M5 11a7 7 0 0 0 14 0M12 4v3" },        // ăn uống
  { mau: ["#E3F0ED", "#0A4E4A"], d: "M3 21h18M5 21V10l7-5 7 5v11" },                 // di tích
  { mau: ["#F6E3EA", "#7E1F3E"], d: "M8 2v4M16 2v4M3 9h18M5 5h14v16H5z" },           // lễ hội
  { mau: ["#E9E6F7", "#3B2F7A"], d: "M9 18V5l12-2v13M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0M21 16a3 3 0 1 1-6 0 3 3 0 0 1 6 0" },  // ca Huế
  { mau: ["#E1ECF7", "#1E4E8C"], d: "M5 17h14M7 17l1-6h8l1 6M9 11V7h6v4" },          // đi lại
];

export function TrangTroLy({ chat, onEditPlan, tinhNang = {} }) {
  const anh = !!tinhNang.anh;
  return (
    <div className="khung tro-ly-trang">
      <h1 className="sr-only">Trợ lý Huế</h1>
      <div className="tl-cot">
        <aside className="tl-ben" aria-label="Gợi ý">
          <section className="tl-hop">
            <h2>Hỏi gì cũng được về Huế</h2>
            <div className="tl-chu-de" aria-label="Câu gợi ý">
              {GOI_Y.map((cau, i) => (
                <button key={cau} type="button" className="nhan-nut" disabled={chat.pending || chat.resetting} onClick={() => chat.ask(cau)}>
                  <span className="bt" style={{ background: CHU_DE[i % CHU_DE.length].mau[0], color: CHU_DE[i % CHU_DE.length].mau[1] }}>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                         strokeLinejoin="round" aria-hidden="true"><path d={CHU_DE[i % CHU_DE.length].d} /></svg>
                  </span>
                  {cau}
                </button>
              ))}
            </div>
          </section>
          <section className="tl-hop">
            <h2>Trợ lý làm được gì</h2>
            <ul className="tl-lam">
              {/* review E M-1: mỗi dòng theo đúng cờ server (`/api/tinh_nang`) — tính năng tắt thì không hứa */}
              <li>Trả lời từ kho tư liệu, ghi nguồn để bạn xem lại.</li>
              {(tinhNang.lich_trinh_bieu_mau || tinhNang.len_ke_hoach_v2) && <li><a href="#/len-ke-hoach">Xếp lịch</a> theo số ngày và sở thích.</li>}
              {tinhNang.thoi_tiet && <li>Xem dự báo thời tiết Huế 7 ngày tới.</li>}
              {anh && <li>Đoán tên món / công trình từ ảnh — bạn bấm xác nhận.</li>}
              {tinhNang.tra_web && <li>Kho chưa có ⇒ tra web, tách riêng "chưa kiểm".</li>}
            </ul>
          </section>
          <p className="tl-hop" style={{ fontSize: 14, color: "var(--color-muted)" }}>
            Trợ lý có thể sai. Đừng gõ thông tin cá nhân (số điện thoại, địa chỉ nhà).
          </p>
        </aside>
        <section className="tl-chat" aria-label="Khung trò chuyện">
          <div className="tl-chat-dau">
            <span className="tra-av" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 34 34"><path d="M6 19c3-3 6-3 9 0s6 3 9 0 4-2 4-2M6 24c3-3 6-3 9 0s6 3 9 0" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" /></svg>
            </span>
            <span><b>Trợ lý Huế</b><small>Trả lời từ kho tư liệu về Huế, có nguồn</small></span>
          </div>
          <ChatView chat={chat} idPrefix="trang" suggestions={GOI_Y} onEditPlan={onEditPlan} anh={anh} />
        </section>
      </div>
    </div>
  );
}

// Khung trò chuyện (dùng ở khung nổi và trang trợ lý). `onEditPlan(chon)`: "Sửa" của lịch từ biểu mẫu ⇒ quay lại biểu mẫu (D3: sửa lịch bằng chat
// chưa có).
export function ChatView({ chat, idPrefix, suggestions = [], onEditPlan, anh = false }) {
  const { turns, draft, setDraft, pending, resetting, resetError, ask, stop, startNewConversation } = chat;
  const lastTurnRef = useRef(null);
  const queryRef = useRef(null);
  const queryId = `${idPrefix}-query`;

  // Lượt mới ⇒ cuộn tới câu vừa hỏi (trong khung chứa).
  useEffect(() => {
    lastTurnRef.current?.scrollIntoView({ block: "start", behavior: reducedMotion() ? "auto" : "smooth" });
  }, [turns.length]);

  function submit(event) {
    event.preventDefault();
    if (pending || resetting || !draft.trim()) return;
    ask(draft);
    setDraft("");  // câu đã in lại trong khung trò chuyện; "Thử lại" gửi lại đúng câu đó
  }

  function onQueryKeyDown(event) {
    // Enter gửi, Shift + Enter xuống dòng; bỏ qua Enter khi bộ gõ đang ghép chữ (bộ gõ tiếng Việt kiểu ghép)
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) submit(event);
  }

  const hoiAnh = useHoiBangAnh({ bat: anh, draft, disabled: pending || resetting, onAsk: query => { ask(query); setDraft(""); },
                                 onGoTen: () => queryRef.current?.focus() });

  return (
    <div className="chat-view">
      <div className="chat-turns">
        {resetError && <p className="mb-4 rounded-md bg-error-soft p-3 text-error" role="alert">{resetError}</p>}
        {turns.length === 0 && (
          <div className="chat-chao">
            <p>Hỏi về món ăn, di tích, lễ hội, nghệ thuật hay chuyến đi ở Huế. Mỗi câu trả lời ghi tên tài liệu đã dùng để bạn tự xem lại.</p>
            {suggestions.length > 0 && (
              <div className="suggest" aria-label="Câu gợi ý">
                {suggestions.map(question => <button key={question} type="button" onClick={() => ask(question)}>{question}</button>)}
              </div>
            )}
          </div>
        )}
        {turns.length > 0 && (
          <section aria-label="Cuộc trò chuyện">
            {turns.map((turn, index) => (
              <Turn key={turn.key} turn={turn} turnRef={index === turns.length - 1 ? lastTurnRef : null}
                    onRetry={() => ask(turn.question, { retryKey: turn.key, truong: turn.truong, summary: turn.summary, bieuMau: turn.bieuMau })}
                    onAsk={(q, opts) => ask(q, opts)} onEditPlan={onEditPlan} />
            ))}
          </section>
        )}
      </div>

      <form onSubmit={submit} className="chat-form">
        {hoiAnh.the}
        <div className={hoiAnh.nut ? "composer composer-co-nut" : "composer"}>
          {hoiAnh.nut}
          <label htmlFor={queryId} className="sr-only">Câu hỏi về Huế</label>
          <textarea ref={queryRef} id={queryId} rows={1} value={draft} disabled={pending} maxLength={MAX_QUERY}
                    aria-describedby={draft.length >= DEM_KY_TU_TU ? `${queryId}-dem` : undefined}
                    onChange={event => setDraft(event.target.value)} onKeyDown={onQueryKeyDown} onPaste={hoiAnh.onPaste}
                    placeholder={turns.length > 0 ? "Hỏi tiếp…" : "Hỏi gì về Huế…"}
                    className="min-h-11 flex-1 resize-none bg-transparent py-2 text-[16px] leading-[1.5] outline-none disabled:opacity-60" />
          {pending
            ? <button type="button" onClick={stop} className="send">Dừng</button>
            : <button type="submit" disabled={resetting} className="send">Hỏi</button>}
        </div>
        {draft.length >= DEM_KY_TU_TU && (
          <p id={`${queryId}-dem`} className="dem-ky-tu" aria-live="polite">
            {draft.length >= MAX_QUERY ? `Đã đủ ${MAX_QUERY} ký tự — câu dài hơn sẽ không gõ thêm được.` : `${draft.length} / ${MAX_QUERY} ký tự`}
          </p>
        )}
        <div className="chat-chan">
          <p>Trợ lý AI trả lời từ kho tư liệu, có thể sai — xem nguồn trước khi dùng thông tin quan trọng.</p>
          {turns.length > 0 && (
            <button type="button" onClick={startNewConversation} disabled={pending || resetting} className="new-chat">Cuộc trò chuyện mới</button>
          )}
        </div>
      </form>
    </div>
  );
}

function Turn({ turn, turnRef, onRetry, onAsk, onEditPlan }) {
  const html = useMemo(() => renderAnswerHtml(turn.text), [turn.text]);
  const pending = PENDING.has(turn.phase);
  const answerRef = useRef(null);  // việc nhỏ (1): chữ lịch đúng như đang hiện (đã qua DOMPurify) cho nút sao chép / tải
  return (
    <article className="turn" ref={turnRef} data-turn={turn.key} data-phase={turn.phase}>
      <h2 className="ask">{turn.question}{turn.summary && <span className="ask-chon"> · {turn.summary}</span>}</h2>
      <div className="tra">
      <span className="tra-av" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 34 34"><path d="M6 19c3-3 6-3 9 0s6 3 9 0 4-2 4-2M6 24c3-3 6-3 9 0s6 3 9 0" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" /></svg>
      </span>
      <div className="tra-noi">
      {pending && !turn.text && (
        <div className="searching" role="status">
          {HIEN_BUOC_LUC_CHO && <BuocDangChay buoc={turn.buoc} phase={turn.phase} />}
          <span className="go" aria-hidden="true"><i /><i /><i /></span>
          <span className="sr-only">{STATUS_TEXT[turn.phase]}</span>
        </div>
      )}
      {turn.phase === "error" && (
        <div className="bubble bubble-error" role="alert">
          <p className="text-error">{turn.error}</p>
          <button type="button" onClick={onRetry} className="retry">Thử lại</button>
        </div>
      )}
      {turn.phase === "stopped" && (
        <div className="bubble" role="status">
          <p className="text-muted">Đã dừng. Phần trả lời chưa xong nên không hiện (chưa kiểm nguồn).</p>
          <button type="button" onClick={onRetry} className="retry">Hỏi lại</button>
        </div>
      )}
      {turn.lichV2 && turn.phase !== "error" && (
        <LichV2 turn={turn} onEditPlan={turn.bieuMau ? onEditPlan : null} />
      )}
      {turn.text && !turn.lichV2 && !turn.suaThe && turn.phase !== "error" && (  /* thẻ chọn đã hỏi đúng câu đó — không vẽ lần hai */
        <div className="bubble">
          {pending && <p className="mb-2 text-sm text-muted" aria-live="polite">{STATUS_TEXT[turn.phase]}</p>}
          <div className="answer" ref={answerRef} dangerouslySetInnerHTML={{ __html: html }} />
          <AnhTraLoi turn={turn} />
          <TheKhachSan turn={turn} />
          {turn.sources?.length > 0 && <SourceLine turn={turn} />}
          {turn.notice && (
            <p className="notice">
              <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">
                <circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" strokeWidth="1.5" />
                <path d="M8 4v5M8 11v1" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
              </svg>
              {turn.notice}
            </p>
          )}
        </div>
      )}
      {turn.web && turn.phase !== "error" && <WebSection web={turn.web} turnKey={turn.key} />}
      {HIEN_BUOC_LUC_CHO && pending && turn.progress.length > 0 && (
        <p className="progress" role="status">{turn.progress[turn.progress.length - 1]}</p>
      )}
      {turn.phase === "done" && turn.clarify && <ClarifyCard clarify={turn.clarify} onAsk={onAsk} />}
      {turn.phase === "done" && turn.suaThe && <SuaTheCard the={turn.suaThe} onAsk={onAsk} />}
      {turn.phase === "done" && turn.lich && !turn.lichV2 && (
        <LichExtras lich={turn.lich} truong={turn.truong} onAsk={onAsk} onEditPlan={turn.bieuMau ? onEditPlan : null}
                    getText={() => vanBanLich(turn, answerRef.current?.innerText ?? "", turn.lich.ban_do || [])} />
      )}
      {turn.phase === "done" && turn.outcome === "out_of_scope" && (
        <div className="suggest" aria-label="Câu gợi ý">
          <p className="text-sm text-muted">Bạn có thể hỏi, ví dụ:</p>
          {OUT_OF_SCOPE_SUGGESTIONS.map(question => <button key={question} type="button" onClick={() => onAsk(question)}>{question}</button>)}
        </div>
      )}
      {/* review B m-2: lượt biểu mẫu không có câu gõ ⇒ gợi ý "cách hỏi" không hợp */}
      {turn.phase === "done" && turn.tuChoiKho && !turn.bieuMau && turn.web?.outcome !== "co_muc" && (
        <div className="goi-y-hoi" aria-label="Gợi ý cách hỏi">
          <p className="text-sm text-muted">Bạn có thể thử:</p>
          <ul>
            {REFUSAL_TIPS.map(tip => <li key={tip}>{tip}</li>)}
            <li>Xem <a href="#/kham-pha">mục Khám phá</a> để biết kho có những bài nào.</li>
          </ul>
        </div>
      )}
      </div>
      </div>
    </article>
  );
}

// Bước đang chạy của lượt (bước cuối trong các sự kiện `status` thật; chưa có sự kiện nào ⇒ nhãn của pha hiện tại).
function BuocDangChay({ buoc, phase }) {
  const b = buoc[buoc.length - 1];
  return <div className="buoc-dang">{b ? `${STATUS_TEXT[b.stage]}${b.n > 0 ? ` (${b.n} đoạn)` : ""}` : STATUS_TEXT[phase]}</div>;
}

// B6 D6: khối riêng sau câu từ chối của kho. Nhãn "chưa kiểm" cố định; chữ + nguồn từ sự kiện `web` (server đã kiểm mã, link, số tiền).
function WebSection({ web, turnKey }) {
  const sources = web.sources.filter(source => WEB_LINK.test(source.link));
  const html = useMemo(() => renderWebHtml(web.text), [web.text]);
  return (
    <section className="bubble web" aria-label="Từ web (chưa kiểm)">
      <h3 className="mb-2 font-semibold text-accent-deep">Từ web (chưa kiểm)</h3>
      <div className="answer" dangerouslySetInnerHTML={{ __html: html }} />
      {sources.length > 0 && (
        <ul className="mt-2 text-sm">
          {sources.map(source => (
            <li key={source.id} id={`web-${turnKey}-${source.id}`}>
              <a href={source.link} target="_blank" rel="noopener noreferrer nofollow">{source.title}</a>{" "}
              <span className="text-muted">({source.domain})</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

// B5 D11 + D12 (a): link "mở bản đồ" từng điểm (code dựng, chỉ đúng gốc Google Maps) + nút "Sửa": lịch từ câu gõ ⇒ mở lại thẻ hỏi lại; lịch từ
// biểu mẫu ⇒ quay lại biểu mẫu với lựa chọn đang dùng (cổng D3).
function LichExtras({ lich, truong, onAsk, onEditPlan, getText }) {
  const [editing, setEditing] = useState(false);
  const links = (lich.ban_do || []).filter(item => typeof item.map_url === "string" && item.map_url.startsWith(MAP_PREFIX));
  return (
    <div className="lich">
      {links.some(item => toaDoHopLe(item.toa_do)) ? (
        <Suspense fallback={<MapLinks links={links} />}><BanDoLich items={links} /></Suspense>
      ) : links.length > 0 && <MapLinks links={links} />}
      <LuuLich getText={getText} />
      {lich.sua && onEditPlan && (
        <button type="button" className="retry" onClick={() => onEditPlan(lich.sua.chon, truong)}>Sửa — điền lại biểu mẫu</button>
      )}
      {lich.sua && !onEditPlan && !editing && <button type="button" className="retry" onClick={() => setEditing(true)}>Sửa</button>}
      {lich.sua && !onEditPlan && editing && <ClarifyCard clarify={lich.sua} initial={lich.sua.chon} onAsk={onAsk} />}
    </div>
  );
}

function MapLinks({ links }) {
  return (
    <div>
      <p className="text-sm font-semibold text-accent-deep">Bản đồ từng điểm</p>
      <ul className="map-links">
        {links.map(item => <li key={item.map_url}><a href={item.map_url} target="_blank" rel="noopener noreferrer">{item.ten}</a></li>)}
      </ul>
    </div>
  );
}

// B4 D10: thẻ hỏi lại — mỗi trường một nhóm nút (chọn một), "Gửi" bật khi đủ trường bắt buộc, "Trả lời luôn" gửi `truong: {}`.
// Sửa lịch bằng lời: "thay X" mà không nói thay bằng gì ⇒ thẻ 2–3 điểm đặt được vào đúng chỗ cũ (code chọn, đúng luật) + "Bỏ điểm này".
// Bấm nút ⇒ lượt mới mang `sua_chon` {cu, moi} — server áp đúng lựa chọn, không hỏi lại lần hai.
function SuaTheCard({ the, onAsk }) {
  const khong = (the.thay_doi || []).filter(d => !d.duoc);
  return (
    <div className="clarify bubble sua-the">
      {khong.length > 0 && <ul className="lkh-doi">{khong.map((d, i) => <li key={i} className="lkh-doi-khong">{d.cau}</li>)}</ul>}
      <p className="mb-2">Bạn muốn thay <b>{the.ten_cu}</b> bằng điểm nào?</p>
      <div className="flex flex-wrap gap-2">
        {the.lua_chon.map(c => (
          <button key={c.gia_tri} type="button" className={c.gia_tri === "bo" ? "retry" : "send"}
                  onClick={() => onAsk(c.gia_tri === "bo" ? `Bỏ ${the.ten_cu}` : `Thay ${the.ten_cu} bằng ${c.nhan}`, { suaChon: { cu: the.cu, moi: c.gia_tri } })}>
            {c.nhan}
          </button>
        ))}
      </div>
    </div>
  );
}

function ClarifyCard({ clarify, onAsk, initial = {} }) {
  const [chosen, setChosen] = useState(initial);
  const ready = clarify.bat_buoc.every(ten => chosen[ten]);
  const summary = clarify.truong.filter(t => chosen[t.ten]).map(t => t.lua_chon.find(c => c.gia_tri === chosen[t.ten]).nhan).join(" · ");
  return (
    <div className="clarify bubble">
      <p className="mb-2">Để gợi ý sát hơn, bạn chọn thêm:</p>
      {clarify.truong.map(t => (
        <fieldset key={t.ten} className="mb-2">
          <legend className="text-sm font-semibold text-accent-deep">{t.nhan}{clarify.bat_buoc.includes(t.ten) ? "" : " (không bắt buộc)"}</legend>
          <div className="flex flex-wrap gap-2 pt-1">
            {t.lua_chon.map(c => (
              <button key={c.gia_tri} type="button" aria-pressed={chosen[t.ten] === c.gia_tri}
                      onClick={() => setChosen(old => ({ ...old, [t.ten]: old[t.ten] === c.gia_tri ? undefined : c.gia_tri }))}>
                {c.nhan}
              </button>
            ))}
          </div>
        </fieldset>
      ))}
      <div className="flex flex-wrap gap-2 pt-2">
        <button type="button" className="send" disabled={!ready}
                onClick={() => onAsk(clarify.cau_goc, { truong: Object.fromEntries(Object.entries(chosen).filter(([, v]) => v)), summary })}>Gửi</button>
        <button type="button" className="retry" onClick={() => onAsk(clarify.cau_goc, { truong: {}, summary: "trả lời luôn" })}>Trả lời luôn</button>
      </div>
    </div>
  );
}

// Thẻ khách sạn dưới câu trả lời (luật ở `theKhachSan.js`, code quyết). Bảng cơ sở tải MỘT lần từ `/api/cho_o` (cờ `luu_tru_lich` tắt ⇒ 404 ⇒ không thẻ).
// Ảnh chỉ gốc tự host, link chỉ 2 gốc như ô Nơi ở; không giá, không "còn phòng".
let coSoHua = null;
function useCoSo(can) {
  const [ds, setDs] = useState(null);
  useEffect(() => {
    if (!can) return;
    coSoHua ??= fetch("/api/cho_o").then(r => (r.ok ? r.json() : null)).then(phangCoSo).catch(() => []);
    let con = true;
    coSoHua.then(x => con && setDs(x));
    return () => { con = false; };
  }, [can]);
  return ds;
}
const ANH_KS = "/anh/khach_san/";
const anhKsHopLe = a => typeof a === "string" && a.startsWith(ANH_KS) && a.endsWith(".jpg") && !a.includes("..");
function TheKhachSan({ turn }) {
  const coLuuTru = turn.phase === "done" && Array.isArray(turn.sources) && turn.sources.some(s => typeof s.bai_id === "string" && s.bai_id.startsWith("travel/services/"));
  const coSo = useCoSo(coLuuTru);
  const ds = coSo ? theKhachSan(turn, coSo) : [];
  if (!ds.length) return null;
  return (
    <div className="the-ks-hang" aria-label="Chỗ ở được nhắc">
      {ds.map(c => (
        <div key={`${c.ten}|${c.dia_chi}`} className="the-ks">
          {anhKsHopLe(c.anh) ? <img src={`${import.meta.env.BASE_URL}${c.anh.slice(1)}`} alt={c.ten} loading="lazy" decoding="async" />
            : <span className="the-ks-khong-anh" aria-hidden="true" />}
          <span className="the-ks-ten">{c.ten}</span> <small>{c.xep_hang}</small>
          <span className="the-ks-link">
            {typeof c.map_url === "string" && c.map_url.startsWith(MAP_PREFIX) && <a href={c.map_url} target="_blank" rel="noopener noreferrer">Bản đồ</a>}
            {typeof c.link === "string" && c.link.startsWith(LINK_TIM_PHONG) && <a href={c.link} target="_blank" rel="noopener noreferrer">Tìm phòng</a>}
          </span>
        </div>
      ))}
      <p className="the-ks-nhan">Theo danh mục, chưa kiểm giá / phòng trống.</p>
    </div>
  );
}

// Ảnh dưới câu trả lời (luật ở `anhTraLoi.js`, code quyết): ảnh của bài nguồn, bấm mở bài; khung tỉ lệ cố định ⇒ không xô lệch khi ảnh tải.
// 2–3 ảnh ⇒ một hàng ảnh nhỏ, tên nơi dưới mỗi ảnh (review E: câu so sánh 2 nơi không thành ảnh nơi A cạnh chữ nơi B); không chữ ghi công.
function AnhTraLoi({ turn }) {
  const ds = anhTraLoi(turn);
  if (!ds.length) return null;
  if (ds.length === 1) {
    const a = ds[0];
    return (
      <a className="anh-tra-loi" href={baiHref(a.baiId)} aria-label={`Đọc bài “${a.ten}”`}>
        <img src={`${import.meta.env.BASE_URL}anh/${a.anh}.jpg`} alt={a.ten} loading="lazy" decoding="async" />
      </a>
    );
  }
  return (
    <div className="anh-tra-loi-hang">
      {ds.map(a => (
        <a key={a.baiId} className="anh-tra-loi-o" href={baiHref(a.baiId)} aria-label={`Đọc bài “${a.ten}”`}>
          <span className="anh-tra-loi-khung"><img src={`${import.meta.env.BASE_URL}anh/${a.anh}.jpg`} alt={a.ten} loading="lazy" decoding="async" /></span>
          <span className="anh-tra-loi-ten">{a.ten}</span>
        </a>
      ))}
    </div>
  );
}
