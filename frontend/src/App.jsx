import { useEffect, useMemo, useRef, useState } from "react";
import { renderAnswerHtml } from "./markdown.js";
import { streamAnswer } from "./stream.js";

const STATUS_TEXT = {
  searching: "Đang tìm thông tin…",
  searched: "Đã tìm thông tin, đang chuẩn bị câu trả lời…",
  generating: "Đang viết câu trả lời…",
};

// phase: idle (chưa hỏi) · searching / searched / generating (đang chờ — khoá ô hỏi, yêu cầu 12) · done · error
export default function App() {
  const [phase, setPhase] = useState("idle");
  const [question, setQuestion] = useState("");
  const [draft, setDraft] = useState("");
  const [text, setText] = useState("");
  const [sources, setSources] = useState(null);  // null = chưa có sự kiện `sources`; [] = từ chối (kho không có nguồn)
  const [error, setError] = useState("");
  const [activeSource, setActiveSource] = useState(null);
  const bufferRef = useRef("");
  const lastSeqRef = useRef(0);
  const frameRef = useRef(0);
  const abortRef = useRef(null);
  const pending = phase === "searching" || phase === "searched" || phase === "generating";

  // Rời trang / đóng tab ⇒ huỷ `fetch` để server dừng model (yêu cầu 17).
  useEffect(() => {
    const abort = () => abortRef.current?.abort();
    window.addEventListener("pagehide", abort);
    return () => {
      window.removeEventListener("pagehide", abort);
      abort();
    };
  }, []);

  function clearAnswer() {
    cancelAnimationFrame(frameRef.current);
    frameRef.current = 0;
    bufferRef.current = "";
    lastSeqRef.current = 0;
    setText("");
    setSources(null);
    setActiveSource(null);
  }

  async function ask(value) {
    const query = value.trim();
    if (!query || pending) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    clearAnswer();
    setQuestion(query);
    setError("");
    setPhase("searching");
    try {
      await streamAnswer(query, {
        signal: controller.signal,
        onEvent(name, data) {
          if (name === "status") {
            setPhase(data.stage === "generating" ? "generating" : "searched");
          } else if (name === "delta") {
            // Chữ hiện dần: gom mảnh vào buffer, vẽ lại CẢ buffer tối đa một lần mỗi khung hình (yêu cầu 8); chỉ nối mảnh có `seq` mới (yêu cầu 4).
            if (data.seq <= lastSeqRef.current) return;
            lastSeqRef.current = data.seq;
            bufferRef.current += data.text;
            if (!frameRef.current) {
              frameRef.current = requestAnimationFrame(() => {
                frameRef.current = 0;
                setText(bufferRef.current);
              });
            }
          } else if (name === "sources") {
            // Chữ đã qua bộ kiểm trích dẫn: vẽ bản cuối rồi mới bật link nguồn (yêu cầu 9).
            cancelAnimationFrame(frameRef.current);
            frameRef.current = 0;
            setText(bufferRef.current);
            setSources(data);
          }
        },
      });
      setPhase("done");
    } catch (failure) {
      if (failure.name === "AbortError") return;  // chính trang huỷ (rời trang) — không còn ai xem
      // D3: kiểm cuối hỏng (rút lại) hoặc lỗi / đứt giữa chừng (xoá hết) — xoá chữ + nguồn đã hiện, hiện lời báo + "Thử lại" (yêu cầu 10, 11).
      clearAnswer();
      setError(failure.message);
      setPhase("error");
    }
  }

  function submit(event) {
    event.preventDefault();
    if (pending || !draft.trim()) return;
    ask(draft);
    setDraft("");  // câu đã in lại phía trên; "Thử lại" gửi lại đúng câu đó
  }

  function onQueryKeyDown(event) {
    // Enter gửi, Shift + Enter xuống dòng; bỏ qua Enter khi bộ gõ đang ghép chữ (bộ gõ tiếng Việt kiểu ghép)
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) submit(event);
  }

  const citedIds = useMemo(() => (sources ? new Set(sources.map(source => String(source.id))) : null), [sources]);
  const answerHtml = useMemo(() => renderAnswerHtml(text, citedIds), [text, citedIds]);

  function focusSource(id) {
    setActiveSource(id);
    document.getElementById(`source-${id}`)?.focus();
  }

  // Link nguồn được dựng trong HTML của câu trả lời ⇒ bắt sự kiện ở khung chứa.
  function onAnswerClick(event) {
    const link = event.target.closest("a[data-cite]");
    if (!link) return;
    event.preventDefault();
    focusSource(link.dataset.cite);
  }

  function onAnswerKeyDown(event) {
    const link = event.target.closest("a[data-cite]");
    if (!link || event.key !== " ") return;  // Enter đã kích hoạt link sẵn; thêm phím cách
    event.preventDefault();
    focusSource(link.dataset.cite);
  }

  return (
    <div className="flex min-h-screen flex-col bg-page font-sans text-ink">
      <header className="border-b border-line bg-surface">
        <div className="mx-auto flex max-w-[1120px] flex-wrap items-baseline justify-between gap-x-6 gap-y-1 px-4 py-3">
          <h1 className="text-xl font-semibold text-accent">Hỏi về Huế</h1>
          <p className="text-[15px] text-muted">Trả lời từ kho tư liệu về Huế</p>
        </div>
      </header>

      <div className="mx-auto grid w-full max-w-[1120px] flex-1 grid-rows-[1fr_auto] gap-6 px-4 py-6 min-[900px]:grid-cols-[minmax(0,720px)_340px] min-[900px]:grid-rows-1 min-[900px]:justify-between">
        <main className="flex min-w-0 flex-col">
          <div className="flex-1 pb-6">
            {phase === "idle" && (
              <p className="text-[17px] leading-[1.65] text-muted">
                Hỏi về di tích, món ăn, lễ hội, nghệ thuật và du lịch Huế. Câu trả lời dựa trên kho tư liệu, có ghi nguồn.
              </p>
            )}
            {phase !== "idle" && <h2 className="mb-4 text-xl font-semibold">{question}</h2>}
            {pending && (
              <p className="mb-3 flex items-center gap-2 text-[15px] text-muted" aria-live="polite">
                <span className="size-2 rounded-full bg-muted motion-safe:animate-pulse" aria-hidden="true" />
                {STATUS_TEXT[phase]}
              </p>
            )}
            {phase !== "error" && (
              <div
                className="answer"
                onClick={onAnswerClick}
                onKeyDown={onAnswerKeyDown}
                dangerouslySetInnerHTML={{ __html: answerHtml }}
              />
            )}
            {phase === "error" && (
              <div className="rounded-md bg-error-soft p-4" role="alert">
                <p className="text-error">{error}</p>
                <button
                  type="button"
                  onClick={() => ask(question)}
                  className="mt-3 rounded-md border border-field-line bg-surface px-4 py-1.5 font-semibold text-accent hover:bg-accent-soft focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
                >
                  Thử lại
                </button>
              </div>
            )}
          </div>

          <form onSubmit={submit} className="sticky bottom-0 bg-page pt-2 pb-4">
            <label htmlFor="query" className="sr-only">Câu hỏi về Huế</label>
            <div className="flex items-end gap-3">
              <textarea
                id="query"
                rows={2}
                value={draft}
                disabled={pending}
                onChange={event => setDraft(event.target.value)}
                onKeyDown={onQueryKeyDown}
                placeholder="Hỏi gì về Huế…"
                className="min-h-[3.5rem] flex-1 resize-y rounded-md border border-field-line bg-surface px-3 py-2 text-[17px] leading-[1.5] placeholder:text-muted focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-accent disabled:opacity-60"
              />
              <button
                type="submit"
                disabled={pending}
                className="rounded-md bg-accent sm:min-w-[9.5rem] px-5 py-2.5 font-semibold text-on-accent hover:bg-accent-strong focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
              >
                {pending ? "Đang trả lời…" : "Hỏi"}
              </button>
            </div>
            <p className="mt-2 text-[13px] text-muted">
              Trợ lý AI — câu trả lời dựa trên kho tư liệu, có thể sai. Hãy xem nguồn trước khi dùng thông tin quan trọng.
            </p>
          </form>
        </main>

        <aside aria-label="Nguồn tham khảo" className="min-w-0 min-[900px]:sticky min-[900px]:top-6 min-[900px]:self-start">
          {phase !== "idle" && phase !== "error" && (
            <SourcePanel sources={sources} activeSource={activeSource} />
          )}
        </aside>
      </div>
    </div>
  );
}

function SourcePanel({ sources, activeSource }) {
  return (
    <section className="rounded-md border border-line bg-surface p-4">
      <h2 className="mb-2 text-[15px] font-semibold">Nguồn</h2>
      {sources === null && <p className="text-[15px] text-muted">Nguồn hiện khi câu trả lời kiểm xong.</p>}
      {sources?.length === 0 && <p className="text-[15px] text-muted">Kho chưa có nguồn cho câu này.</p>}
      {sources?.length > 0 && (
        <ol className="divide-y divide-line text-[15px]">
          {sources.map(source => (
            <li
              key={source.id}
              id={`source-${source.id}`}
              tabIndex={-1}
              className={`-mx-2 rounded px-2 py-3 transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-accent ${String(source.id) === activeSource ? "bg-accent-soft" : ""}`}
            >
              <div className="flex gap-2">
                <span className="font-semibold text-accent">{source.id}</span>
                <div className="min-w-0">
                  <h3 className="font-semibold">{source.title}</h3>
                  {source.heading_path.length > 0 && <p className="text-muted">{source.heading_path.join(" › ")}</p>}
                  {source.excerpts.length > 0 && (
                    <details className="mt-1">
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
      )}
    </section>
  );
}
