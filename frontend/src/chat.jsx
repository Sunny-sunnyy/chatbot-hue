import { Suspense, lazy, useEffect, useMemo, useRef, useState } from "react";
import { displayNumbers, renderAnswerHtml, renderWebHtml } from "./markdown.js";
import { baiHref } from "./route.js";
import { streamAnswer } from "./stream.js";
import HoiBangAnh from "./HoiBangAnh.jsx";  // Phase 10: hỏi bằng ảnh (gợi ý có xác nhận) — chỉ hiện khi server bật cờ `anh.bat`
// Bản đồ lịch trình (plan 2026-11-08): chunk riêng — chỉ tải khi lịch có ≥ 1 toạ độ hợp lệ (server chỉ gửi `toa_do` khi cờ `ban_do_lich` bật)
const BanDoLich = lazy(() => import("./BanDoLich.jsx"));
const coToaDo = td => Array.isArray(td) && td.length === 2 && td.every(Number.isFinite);  // kiểm đủ (khung Huế) ở `BanDoLich.toaDoHopLe`

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
const MAP_PREFIX = "https://www.google.com/maps/search/";  // D11: chỉ nhận link bản đồ đúng gốc này (kiểm cả phía trình duyệt)
const PENDING = new Set(Object.keys(STATUS_TEXT));
const NEW_CONVERSATION_ERROR = "Chưa bắt đầu được cuộc trò chuyện mới. Vui lòng thử lại.";
// B142: câu ngoài phạm vi kèm 3 câu gợi ý cố định (đã kiểm có trong kho bằng `scripts/grep_kb.sh`) — bấm là hỏi luôn.
const OUT_OF_SCOPE_SUGGESTIONS = ["Vào Đại Nội nên mặc thế nào?", "Lễ hội Điện Huệ Nam diễn ra khi nào?", "Nhã nhạc cung đình diễn lúc nào?"];
const FEEDBACK_ERROR = "Chưa gửi được đánh giá — bạn thử lại sau nhé.";
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
           turnId: null, error: "", clarify: null, truong, summary, bieuMau, progress: [], lich: null, web: null, tuChoiKho: false };
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
  async function ask(value, { retryKey = null, truong = null, summary = "", bieuMau = false } = {}) {
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
    // "Thử lại" thay lượt lỗi (server không nhớ lượt lỗi — plan B3 D2) bằng lượt mới cùng câu hỏi.
    setTurns(all => [...all.filter(turn => turn.key !== retryKey), newTurn(key, query, truong, summary, bieuMau)]);
    setResetError("");
    try {
      await streamAnswer(query, {
        signal: controller.signal,
        truong,
        bieuMau,
        onEvent(name, data) {
          if (name === "status" && data.stage === "lich_trinh") {
            const text = LICH_BUOC[data.buoc]?.(data);  // "dang_xep" chỉ là nhãn trạng thái, không vào danh sách bước (C191 m-1)
            if (text) progress.push(text);
            update({ phase: "lich_trinh", progress: [...progress] });
          } else if (name === "status") {
            // chỉ các nhãn đã biết; trạng thái lạ giữ nhãn "đã tìm" (B1 review C129 m-3); `n_sources` có ở `searched`
            update({ phase: data.stage in STATUS_TEXT ? data.stage : "searched", ...(data.n_sources != null && { nSources: data.n_sources }) });
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
          } else if (name === "clarify") {
            update({ clarify: data });  // B4 D8: thẻ hỏi lại — code dựng nút từ danh sách trường
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
          update({ phase: "stopped", text: "", sources: null, numbers: null, notice: "", web: null, clarify: null, lich: null, progress: [] });
        }
        return true;
      }
      // D3: kiểm cuối hỏng (rút lại) hoặc lỗi / đứt giữa chừng (xoá hết) — xoá chữ + nguồn đã hiện, hiện lời báo + "Thử lại" (yêu cầu 10, 11).
      stopFrame();
      update({ phase: "error", text: "", sources: null, numbers: null, notice: "", web: null, error: failure.message });
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
        <HoiBangAnh bat={anh} draft={draft} disabled={pending || resetting} onAsk={query => { ask(query); setDraft(""); }}
                    onGoTen={() => queryRef.current?.focus()} />
        <div className="composer">
          <label htmlFor={queryId} className="sr-only">Câu hỏi về Huế</label>
          <textarea ref={queryRef} id={queryId} rows={1} value={draft} disabled={pending} maxLength={MAX_QUERY}
                    aria-describedby={draft.length >= DEM_KY_TU_TU ? `${queryId}-dem` : undefined}
                    onChange={event => setDraft(event.target.value)} onKeyDown={onQueryKeyDown}
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
  return (
    <article className="turn" ref={turnRef} data-turn={turn.key}>
      <h2 className="ask">{turn.question}{turn.summary && <span className="ask-chon"> · {turn.summary}</span>}</h2>
      {pending && !turn.text && (
        <div className="searching" role="status">
          <svg className="wave" viewBox="0 0 46 24" aria-hidden="true"><path d="M2 12c6-8 10 8 16 0s10 8 16 0 8-6 10-2" /></svg>
          <div>
            <div className="font-semibold text-accent">{STATUS_TEXT[turn.phase]}</div>
            {turn.nSources > 0 && <div className="text-sm text-muted">{turn.nSources} đoạn tư liệu đã tìm được</div>}
          </div>
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
      {turn.outcome === "emergency" && (
        <div className="emergency" role="alert"><p className="whitespace-pre-line">{turn.text}</p></div>
      )}
      {turn.text && turn.phase !== "error" && turn.outcome !== "emergency" && (
        <div className="bubble">
          {pending && <p className="mb-2 text-sm text-muted" aria-live="polite">{STATUS_TEXT[turn.phase]}</p>}
          <div className="answer" dangerouslySetInnerHTML={{ __html: html }} />
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
      {turn.progress.length > 0 && (
        <ul className="progress" aria-label="Các bước xếp lịch">{turn.progress.map((line, i) => <li key={i}>{line}</li>)}</ul>
      )}
      {turn.phase === "done" && turn.clarify && <ClarifyCard clarify={turn.clarify} onAsk={onAsk} />}
      {turn.phase === "done" && turn.lich && <LichExtras lich={turn.lich} onAsk={onAsk} onEditPlan={turn.bieuMau ? onEditPlan : null} />}
      {turn.phase === "done" && turn.outcome === "out_of_scope" && (
        <div className="suggest" aria-label="Câu gợi ý">
          <p className="text-sm text-muted">Bạn có thể hỏi, ví dụ:</p>
          {OUT_OF_SCOPE_SUGGESTIONS.map(question => <button key={question} type="button" onClick={() => onAsk(question)}>{question}</button>)}
        </div>
      )}
      {turn.phase === "done" && turn.tuChoiKho && turn.web?.outcome !== "co_muc" && (
        <div className="goi-y-hoi" aria-label="Gợi ý cách hỏi">
          <p className="text-sm text-muted">Bạn có thể thử:</p>
          <ul>
            {REFUSAL_TIPS.map(tip => <li key={tip}>{tip}</li>)}
            <li>Xem <a href="#/kham-pha">mục Khám phá</a> để biết kho có những bài nào.</li>
          </ul>
        </div>
      )}
      {turn.phase === "done" && turn.turnId && <Feedback turnId={turn.turnId} />}
    </article>
  );
}

// Cổng D1: dưới câu trả lời một dòng "Nguồn: <tên> · <tên>" (thứ tự xuất hiện trong câu); bấm tên ⇒ mở đoạn gốc ngay dưới; nguồn là bài kho
// (`bai_id`) ⇒ link sang trang bài Khám phá. Việc nhỏ 08/11: nhiều đoạn của CÙNG một bài ⇒ một tên (trước: một câu ra 8 lần cùng tên bài);
// bấm tên ⇒ hiện mọi đoạn được trích của bài đó.
function SourceLine({ turn }) {
  const [open, setOpen] = useState(null);
  const sources = [...turn.sources].sort((a, b) => turn.numbers.get(String(a.id)) - turn.numbers.get(String(b.id)));
  const groups = [];
  for (const source of sources) {
    const key = source.bai_id != null ? `b:${source.bai_id}` : `t:${source.title}`;
    const group = groups.find(item => item.key === key);
    if (group) group.parts.push(source);
    else groups.push({ key, title: source.title, bai_id: source.bai_id, parts: [source] });
  }
  const shown = groups.find(group => group.key === open);
  const panelId = `nguon-${turn.key}`;
  return (
    <div className="nguon">
      <p className="nguon-dong">
        <span className="nguon-nhan">Nguồn:</span>{" "}
        {groups.map((group, index) => (
          <span key={group.key}>
            {index > 0 && <span aria-hidden="true"> · </span>}
            <button type="button" className="nguon-ten" aria-expanded={open === group.key} aria-controls={panelId}
                    onClick={() => setOpen(open === group.key ? null : group.key)}>{group.title}</button>
          </span>
        ))}
      </p>
      {shown && (
        <div className="nguon-doan" id={panelId}>
          {shown.parts.map(part => (
            <div key={part.id} className="nguon-phan">
              {part.heading_path.length > 0 && <p className="text-sm text-muted">{part.heading_path.join(" › ")}</p>}
              {part.excerpts.map((excerpt, index) => <blockquote key={index} className="whitespace-pre-line">{excerpt}</blockquote>)}
            </div>
          ))}
          {shown.bai_id && <a className="nguon-bai" href={baiHref(shown.bai_id)}>Đọc cả bài “{shown.title}”</a>}
        </div>
      )}
    </div>
  );
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

// B142: 👍 / 👎 dưới câu trả lời — server chỉ lưu đánh giá + số đếm của lượt. Đổi ý được (bấm nút kia); lỗi ⇒ báo nhẹ, giữ lựa chọn cũ.
function Feedback({ turnId }) {
  const [rating, setRating] = useState(null);
  const [sending, setSending] = useState(false);
  const [failed, setFailed] = useState(false);

  async function send(value) {
    if (sending || value === rating) return;
    setSending(true);
    setFailed(false);
    try {
      const response = await fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ turn_id: turnId, rating: value }),
      });
      if (!response.ok) throw new Error(String(response.status));
      setRating(value);
    } catch {
      setFailed(true);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="feedback">
      <span className="text-sm text-muted">{rating ? "Cảm ơn bạn đã đánh giá." : "Câu trả lời có hữu ích không?"}</span>
      <button type="button" onClick={() => send("up")} disabled={sending} aria-pressed={rating === "up"} aria-label="Hữu ích"><Thumb /></button>
      <button type="button" onClick={() => send("down")} disabled={sending} aria-pressed={rating === "down"} aria-label="Chưa hữu ích"><Thumb down /></button>
      {failed && <span className="text-sm text-error" role="status">{FEEDBACK_ERROR}</span>}
    </div>
  );
}

// B5 D11 + D12 (a): link "mở bản đồ" từng điểm (code dựng, chỉ đúng gốc Google Maps) + nút "Sửa": lịch từ câu gõ ⇒ mở lại thẻ hỏi lại; lịch từ
// biểu mẫu ⇒ quay lại biểu mẫu với lựa chọn đang dùng (cổng D3).
function LichExtras({ lich, onAsk, onEditPlan }) {
  const [editing, setEditing] = useState(false);
  const links = (lich.ban_do || []).filter(item => typeof item.map_url === "string" && item.map_url.startsWith(MAP_PREFIX));
  return (
    <div className="lich">
      {links.some(item => coToaDo(item.toa_do)) ? (
        <Suspense fallback={<MapLinks links={links} />}><BanDoLich items={links} /></Suspense>
      ) : links.length > 0 && <MapLinks links={links} />}
      {lich.sua && onEditPlan && (
        <button type="button" className="retry" onClick={() => onEditPlan(lich.sua.chon)}>Sửa — điền lại biểu mẫu</button>
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

// Ngón cái vẽ bằng SVG (không dùng emoji: máy thiếu font emoji thì nút trống — thấy ở ảnh Playwright B142); xuống = lật dọc.
function Thumb({ down = false }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
      <g transform={down ? "rotate(180 12 12)" : undefined} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" strokeLinecap="round">
        <path d="M3 10h3.5v10.5H3z" />
        <path d="M6.5 10.5 10.5 3c1.6 0 2.6 1.1 2.4 2.7L12.4 9.5h6.1a2 2 0 0 1 2 2.4l-1.5 7a2 2 0 0 1-2 1.6H6.5" />
      </g>
    </svg>
  );
}
