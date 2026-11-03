import { useEffect, useMemo, useRef, useState } from "react";
import { displayNumbers, renderAnswerHtml } from "./markdown.js";
import { streamAnswer } from "./stream.js";

// Giao diện nhiều lượt theo bản mẫu 1 "Huế hiện đại" (User chọn 13:11 03/11/2026; Phase 9 B3 bước 8, plan B3 D8, D9 (b) (c)).
// Server giữ lịch sử (cookie HttpOnly `conversation_id`) — trang chỉ vẽ lại các lượt đã hỏi, không gửi lại lịch sử (plan B3 D1).

const STATUS_TEXT = {
  routing: "Đang hiểu câu hỏi…",  // Phase 9 B1: lần gọi định tuyến
  searching: "Đang tìm trong kho…",
  searched: "Đã tìm trong kho, đang chuẩn bị câu trả lời…",
  generating: "Đang viết câu trả lời…",
};
const PENDING = new Set(Object.keys(STATUS_TEXT));
const NEW_CONVERSATION_ERROR = "Chưa bắt đầu được cuộc trò chuyện mới. Vui lòng thử lại.";

// 5 chủ đề × 2 câu gợi ý (chữ của bản mẫu C140 — tự viết chung chung, không chép kho). Biểu tượng vẽ bằng SVG trong JSX (CSP: không tải ảnh).
const TOPICS = [
  { name: "Di tích", icon: "M3 23h20M5 23V12h16v11M2 12l11-8 11 8M10 23v-6h6v6",
    questions: ["Chỉ có nửa ngày thì nên đi lăng nào?", "Vào Đại Nội nên mặc thế nào?"] },
  { name: "Ẩm thực", icon: "M3 12h20a10 9 0 0 1-20 0zM9 8c0-2 2-2 2-4M14 8c0-2 2-2 2-4",
    questions: ["Ăn sáng ở Huế nên thử món gì?", "Gần trung tâm có quán chay nào?"] },
  { name: "Lễ hội", icon: "M13 2v3M8 6h10l2 4-2 9H8l-2-9zM10 19v4M16 19v4",
    questions: ["Tháng này ở Huế có lễ hội gì?", "Festival Huế thường vào mùa nào?"] },
  { name: "Nghệ thuật", icon: "M13 22V5l9-2v15M13 22a3 3 0 1 1-3-3h3M22 18a3 3 0 1 1-3-3h3",
    questions: ["Nghe ca Huế trên sông ở đâu?", "Nhã nhạc cung đình diễn lúc nào?"] },
  { name: "Chuyến đi", icon: "M2 18c4-3 7 3 11 0s7 3 11 0M6 15l3-9h8l3 9",
    questions: ["Đi Huế hai ngày nên xếp lịch ra sao?", "Từ sân bay vào trung tâm bằng gì?"] },
];

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

// Một lượt: { key, question, phase (routing / searching / searched / generating / done / error), text, sources (null = chưa có sự kiện
// `sources`; [] = không nguồn), numbers (số hiển thị 1..k — D9 (c)), nSources, notice, outcome (từ `done`), error }.
function newTurn(key, question) {
  // lượt mới bắt đầu ở "đang hiểu câu hỏi": việc đầu tiên của server là định tuyến (B1) — thứ tự nhãn như D9 (b), không "đang tìm" trước
  return { key, question, phase: "routing", text: "", sources: null, numbers: null, nSources: null, notice: "", outcome: null, error: "" };
}

export default function App() {
  const [turns, setTurns] = useState([]);
  const [draft, setDraft] = useState("");
  const [selected, setSelected] = useState({ turn: null, source: null });  // lượt có nguồn đang hiện ở khung nguồn + số gốc đang chọn
  const [resetError, setResetError] = useState("");
  const [resetting, setResetting] = useState(false);
  const keyRef = useRef(0);
  const bufferRef = useRef("");
  const lastSeqRef = useRef(0);
  const frameRef = useRef(0);
  const abortRef = useRef(null);
  const lastTurnRef = useRef(null);
  const pending = turns.length > 0 && PENDING.has(turns[turns.length - 1].phase);
  const panelTurn = turns.find(turn => turn.key === selected.turn) ?? turns[turns.length - 1];

  // Rời trang / đóng tab ⇒ huỷ `fetch` để server dừng model (yêu cầu 17).
  useEffect(() => {
    const abort = () => abortRef.current?.abort();
    window.addEventListener("pagehide", abort);
    return () => {
      window.removeEventListener("pagehide", abort);
      abort();
    };
  }, []);

  // Lượt mới ⇒ cuộn tới câu vừa hỏi.
  useEffect(() => {
    lastTurnRef.current?.scrollIntoView({ block: "start", behavior: reducedMotion() ? "auto" : "smooth" });
  }, [turns.length]);

  // Bấm số nguồn ⇒ khung nguồn đổi sang lượt đó (nếu cần) rồi mới focus được mục nguồn ⇒ focus sau khi vẽ.
  useEffect(() => {
    if (selected.source !== null) document.getElementById(`source-${selected.turn}-${selected.source}`)?.focus();
  }, [selected]);

  function stopFrame() {
    cancelAnimationFrame(frameRef.current);
    frameRef.current = 0;
  }

  async function ask(value, retryKey = null) {
    const query = value.trim();
    if (!query || pending || resetting) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    stopFrame();
    bufferRef.current = "";
    lastSeqRef.current = 0;
    const key = ++keyRef.current;
    const update = patch => setTurns(all => all.map(turn => (turn.key === key ? { ...turn, ...patch } : turn)));
    // "Thử lại" thay lượt lỗi (server không nhớ lượt lỗi — plan B3 D2) bằng lượt mới cùng câu hỏi.
    setTurns(all => [...all.filter(turn => turn.key !== retryKey), newTurn(key, query)]);
    setSelected({ turn: key, source: null });
    setResetError("");
    try {
      await streamAnswer(query, {
        signal: controller.signal,
        onEvent(name, data) {
          if (name === "status") {
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
            // Chữ đã qua bộ kiểm trích dẫn: vẽ bản cuối rồi mới bật link nguồn + đánh số hiển thị 1..k (yêu cầu 9; D9 (c)).
            stopFrame();
            update({ text: bufferRef.current, sources: data, numbers: displayNumbers(bufferRef.current, data) });
          } else if (name === "notice") {
            update({ notice: data.text });
          } else if (name === "done") {
            update({ outcome: data.outcome });
          }
        },
      });
      update({ phase: "done" });
    } catch (failure) {
      if (failure.name === "AbortError") return;  // chính trang huỷ (rời trang) — không còn ai xem
      // D3: kiểm cuối hỏng (rút lại) hoặc lỗi / đứt giữa chừng (xoá hết) — xoá chữ + nguồn đã hiện, hiện lời báo + "Thử lại" (yêu cầu 10, 11).
      stopFrame();
      update({ phase: "error", text: "", sources: null, numbers: null, notice: "", error: failure.message });
    }
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
      setSelected({ turn: null, source: null });
      setDraft("");
      document.getElementById("query")?.focus();
    } catch {
      setResetError(NEW_CONVERSATION_ERROR);
    } finally {
      setResetting(false);
    }
  }

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
    <div className="flex min-h-screen flex-col bg-page font-sans text-ink">
      <header className="top">
        <div className="mx-auto flex max-w-[1120px] flex-wrap items-center justify-between gap-x-6 gap-y-2">
          <div className="flex flex-wrap items-baseline gap-x-5 gap-y-1">
            <h1 className="text-[22px] font-semibold tracking-tight">Hỏi về Huế</h1>
            <p className="text-[15px] text-on-top-muted">Trả lời từ kho tư liệu về Huế, có ghi nguồn</p>
          </div>
          {turns.length > 0 && (
            <button type="button" onClick={startNewConversation} disabled={pending || resetting} className="new-chat">
              Cuộc trò chuyện mới
            </button>
          )}
        </div>
        <svg className="river" viewBox="0 0 1440 56" preserveAspectRatio="none" aria-hidden="true">
          <path className="bank" d="M0 40 C 220 18, 420 54, 680 34 S 1120 12, 1440 36 L1440 56 L0 56 Z" />
          <path className="r1" d="M0 34 C 220 12, 420 48, 680 28 S 1120 6, 1440 30" />
          <path className="r2" d="M0 26 C 260 8, 470 40, 720 22 S 1150 2, 1440 22" />
        </svg>
      </header>

      <div className={`mx-auto grid w-full max-w-[1120px] flex-1 gap-7 px-4 pt-5 pb-0 sm:px-6 ${turns.length > 0 ? "min-[900px]:grid-cols-[minmax(0,1fr)_340px]" : ""}`}>
        <main className={`flex min-w-0 flex-col ${turns.length === 0 ? "max-w-[860px]" : ""}`}>
          <div className="flex-1">
            {resetError && <p className="mb-4 rounded-md bg-error-soft p-3 text-error" role="alert">{resetError}</p>}
            {turns.length === 0 && <Welcome onPick={ask} />}
            {turns.length > 0 && (
              <section aria-label="Cuộc trò chuyện">
                {turns.map((turn, index) => (
                  <Turn
                    key={turn.key}
                    turn={turn}
                    turnRef={index === turns.length - 1 ? lastTurnRef : null}
                    activeSource={selected.turn === turn.key ? selected.source : null}
                    onCite={source => setSelected({ turn: turn.key, source })}
                    onRetry={() => ask(turn.question, turn.key)}
                  />
                ))}
              </section>
            )}
          </div>

          <form onSubmit={submit} className="sticky bottom-0 bg-page pt-3 pb-4">
            <div className="composer">
              <label htmlFor="query" className="sr-only">Câu hỏi về Huế</label>
              <textarea
                id="query"
                rows={1}
                value={draft}
                disabled={pending}
                onChange={event => setDraft(event.target.value)}
                onKeyDown={onQueryKeyDown}
                placeholder={turns.length > 0 ? "Hỏi tiếp…" : "Hỏi gì về Huế…"}
                className="min-h-11 flex-1 resize-none bg-transparent py-2 text-[17px] leading-[1.5] outline-none placeholder:text-muted disabled:opacity-60"
              />
              <button type="submit" disabled={pending || resetting} className="send">
                {pending ? "Đang trả lời…" : "Hỏi"}
              </button>
            </div>
            <p className="mt-2 text-[13px] text-muted">
              Trợ lý AI — câu trả lời dựa trên kho tư liệu, có thể sai. Hãy xem nguồn trước khi dùng thông tin quan trọng.
            </p>
          </form>
        </main>

        {turns.length > 0 && (
          <aside aria-label="Nguồn tham khảo" className="min-w-0 pb-6 min-[900px]:sticky min-[900px]:top-4 min-[900px]:self-start">
            <SourcePanel turn={panelTurn} activeSource={panelTurn.key === selected.turn ? selected.source : null} several={turns.length > 1} />
          </aside>
        )}
      </div>
    </div>
  );
}

function Welcome({ onPick }) {
  return (
    <section aria-labelledby="hello-title" className="pb-4">
      <h2 id="hello-title" className="mt-2 mb-2 text-[30px] leading-tight font-semibold tracking-tight text-accent-deep">
        Hôm nay bạn muốn biết gì về Huế?
      </h2>
      <p className="mb-5 max-w-[60ch] text-muted">
        Hỏi về di tích, món ăn, lễ hội, nghệ thuật hay chuyến đi. Mỗi câu trả lời cho biết lấy từ tài liệu nào để bạn tự xem lại.
      </p>
      <div className="topics">
        {TOPICS.map(topic => (
          <div key={topic.name} className="topic">
            <h3>
              <svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true">
                <path d={topic.icon} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              {topic.name}
            </h3>
            {topic.questions.map(question => (
              <button key={question} type="button" onClick={() => onPick(question)}>{question}</button>
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}

function Turn({ turn, turnRef, activeSource, onCite, onRetry }) {
  const html = useMemo(() => renderAnswerHtml(turn.text, turn.numbers, turn.key, activeSource),
    [turn.text, turn.numbers, turn.key, activeSource]);
  const pending = PENDING.has(turn.phase);

  // Link nguồn được dựng trong HTML của câu trả lời ⇒ bắt sự kiện ở khung chứa.
  function onAnswerClick(event) {
    const link = event.target.closest("a[data-cite]");
    if (!link) return;
    event.preventDefault();
    onCite(link.dataset.cite);
  }

  function onAnswerKeyDown(event) {
    const link = event.target.closest("a[data-cite]");
    if (!link || event.key !== " ") return;  // Enter đã kích hoạt link sẵn; thêm phím cách
    event.preventDefault();
    onCite(link.dataset.cite);
  }

  return (
    <article className="turn" ref={turnRef} data-turn={turn.key}>
      <h2 className="ask">{turn.question}</h2>
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
      {turn.outcome === "emergency" && (
        <div className="emergency" role="alert"><p className="whitespace-pre-line">{turn.text}</p></div>
      )}
      {turn.text && turn.phase !== "error" && turn.outcome !== "emergency" && (
        <div className="bubble">
          {pending && <p className="mb-2 text-sm text-muted" aria-live="polite">{STATUS_TEXT[turn.phase]}</p>}
          <div className="answer" onClick={onAnswerClick} onKeyDown={onAnswerKeyDown} dangerouslySetInnerHTML={{ __html: html }} />
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
    </article>
  );
}

function SourcePanel({ turn, activeSource, several }) {
  // nguồn xếp theo số hiển thị 1..k (D9 (c)); id phần tử giữ số gốc + mã lượt (link trong chữ trỏ tới đó)
  const sources = turn.sources && turn.numbers
    ? [...turn.sources].sort((a, b) => turn.numbers.get(String(a.id)) - turn.numbers.get(String(b.id)))
    : turn.sources;
  return (
    <section className="sources" aria-labelledby="sources-title">
      <h2 id="sources-title" className="text-[17px] font-semibold text-accent-deep">Nguồn</h2>
      {several && <p className="mb-1 truncate text-sm text-muted">cho câu: {turn.question}</p>}
      {turn.phase === "error" && <p className="text-muted">Câu này chưa có câu trả lời.</p>}
      {turn.phase !== "error" && sources === null && <p className="text-muted">Nguồn hiện khi câu trả lời kiểm xong.</p>}
      {sources?.length === 0 && <p className="text-muted">Câu trả lời này không dùng nguồn từ kho.</p>}
      {sources?.length > 0 && (
        <>
          <p className="mb-3 text-sm text-muted">Bấm số trong câu trả lời để xem nguồn đó.</p>
          <ol>
            {sources.map(source => (
              <li
                key={source.id}
                id={`source-${turn.key}-${source.id}`}
                tabIndex={-1}
                className={String(source.id) === activeSource ? "on" : ""}
              >
                <div className="flex gap-2">
                  <span className="n">{turn.numbers?.get(String(source.id)) ?? source.id}</span>
                  <div className="min-w-0">
                    <h3 className="font-semibold">{source.title}</h3>
                    {source.heading_path.length > 0 && <p className="text-sm text-muted">{source.heading_path.join(" › ")}</p>}
                    {source.excerpts.length > 0 && (
                      <details className="mt-1 text-sm">
                        <summary className="cursor-pointer text-accent">Xem đoạn trích</summary>
                        {source.excerpts.map((excerpt, index) => (
                          <blockquote key={index} className="mt-2 border-l-2 border-line pl-3 whitespace-pre-line">{excerpt}</blockquote>
                        ))}
                      </details>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ol>
        </>
      )}
    </section>
  );
}
