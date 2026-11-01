const form = document.querySelector("form");
const query = document.querySelector("#query");
const submit = document.querySelector("#submit");
const retry = document.querySelector("#retry");
const status = document.querySelector("#status");
const answer = document.querySelector("#answer");
const sources = document.querySelector("#sources");
let pending = false;
let lastQuery = "";

function setLoading(value) {
  pending = value;
  submit.disabled = value;
  query.disabled = value;
  if (value) status.textContent = "Đang tìm thông tin…";
}

function renderSources(items) {
  sources.replaceChildren();
  for (const item of items) {
    const card = document.createElement("article");
    card.id = `source-${item.id}`;
    card.tabIndex = -1;
    card.className = "source-card";
    const title = document.createElement("h3");
    title.textContent = `[${item.id}] ${item.title}`;
    const path = document.createElement("p");
    path.textContent = item.heading_path.join(" › ");
    card.append(title, path);
    for (const excerpt of item.excerpts) {
      const block = document.createElement("blockquote");
      block.textContent = excerpt;
      card.append(block);
    }
    sources.append(card);
  }
}

function wireCitations() {
  const walker = document.createTreeWalker(answer, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const node of nodes) {
    const parts = node.nodeValue.split(/(\[\d+\])/g);
    if (parts.length === 1) continue;
    const fragment = document.createDocumentFragment();
    for (const part of parts) {
      const match = part.match(/^\[(\d+)\]$/);
      if (!match) {
        fragment.append(document.createTextNode(part));
        continue;
      }
      const link = document.createElement("a");
      link.href = `#source-${match[1]}`;
      link.textContent = part;
      link.addEventListener("click", () => {
        const card = document.querySelector(link.getAttribute("href"));
        if (card) card.focus();
      });
      link.addEventListener("keydown", event => {
        if (event.key !== " ") return;
        event.preventDefault();
        link.click();
      });
      fragment.append(link);
    }
    node.replaceWith(fragment);
  }
}

const INTERRUPTED_MESSAGE = "Kết nối bị gián đoạn. Vui lòng thử lại.";
let renderFrame = 0;

// Câu trả lời là Markdown do model viết: ngoài chặn script, không để trang TỰ tải gì từ máy khác khi hiện chữ (ảnh, `background`, CSS `url(…)`,
// `<input type=image>`, form…). Dùng DANH SÁCH CHO PHÉP — đúng các thẻ / thuộc tính Markdown thường tạo ra — thay vì danh sách cấm (review C107 M-1:
// danh sách cấm sót `background`, `input`). Không có thuộc tính nào chứa URL ngoài `href` của link: link chỉ mở khi người dùng bấm.
const SANITIZE_OPTIONS = {
  ALLOWED_TAGS: ["p", "br", "hr", "strong", "em", "del", "code", "pre", "blockquote", "ul", "ol", "li",
                 "h1", "h2", "h3", "h4", "h5", "h6", "a", "table", "thead", "tbody", "tr", "th", "td"],
  ALLOWED_ATTR: ["href", "title", "align", "start"],
};

// Chữ hiện dần: render lại CẢ buffer theo khung hình (không theo từng mảnh, không `innerHTML +=`), luôn qua DOMPurify (spec streaming §4.7).
function renderAnswer(text) {
  answer.innerHTML = DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS);
}

function scheduleRender(stream) {
  if (renderFrame) return;
  renderFrame = requestAnimationFrame(() => {
    renderFrame = 0;
    renderAnswer(stream.text);
  });
}

function clearAnswer() {
  cancelAnimationFrame(renderFrame);
  renderFrame = 0;
  answer.replaceChildren();
  sources.replaceChildren();
}

// Tách luồng SSE thành sự kiện. Một lần `read()` có thể chứa nửa sự kiện hoặc nhiều sự kiện ⇒ giữ phần dở tới lần sau; bỏ dòng chú thích `:`.
function createSseParser(onEvent) {
  let pendingText = "";
  return chunk => {
    pendingText += chunk;
    let end;
    while ((end = pendingText.indexOf("\n\n")) !== -1) {
      const block = pendingText.slice(0, end);
      pendingText = pendingText.slice(end + 2);
      let name = "message";
      const data = [];
      for (const line of block.split("\n")) {
        if (!line || line.startsWith(":")) continue;
        if (line.startsWith("event:")) name = line.slice(6).trim();
        else if (line.startsWith("data:")) data.push(line.slice(5).replace(/^ /, ""));
      }
      if (data.length) onEvent(name, JSON.parse(data.join("\n")));
    }
  };
}

function handleEvent(stream, name, data) {
  if (name === "status") {
    status.textContent = data.stage === "generating" ? "Đang viết câu trả lời…" : "Đã tìm thông tin, đang chuẩn bị câu trả lời…";
  } else if (name === "delta") {
    if (data.seq <= stream.lastSeq) return;  // chỉ nối mảnh mới
    stream.lastSeq = data.seq;
    stream.text += data.text;
    scheduleRender(stream);
  } else if (name === "sources") {
    // Chữ đã qua bộ kiểm trích dẫn: vẽ bản cuối rồi mới bật link [n].
    cancelAnimationFrame(renderFrame);
    renderFrame = 0;
    renderAnswer(stream.text);
    renderSources(data);
    wireCitations();
  } else if (name === "error") {
    // D3: kiểm cuối hỏng (rút lại) hoặc lỗi / đứt giữa chừng (xóa hết) — cả hai xóa chữ đã hiện, hiện lời báo + "Thử lại".
    throw new Error(data.message || INTERRUPTED_MESSAGE);
  } else if (name === "done") {
    stream.done = true;
  }
}

async function readAnswerStream(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  const stream = {text: "", lastSeq: 0, done: false};
  const feed = createSseParser((name, data) => handleEvent(stream, name, data));
  try {
    while (!stream.done) {
      const {value, done} = await reader.read();
      if (done) break;
      feed(decoder.decode(value, {stream: true}));
    }
  } catch (error) {
    reader.cancel().catch(() => {});
    throw error;
  }
  if (!stream.done) throw new Error(INTERRUPTED_MESSAGE);  // luồng đứt không có `done` ⇒ xử lý như lỗi
}

async function ask(value) {
  if (pending) return;
  lastQuery = value.trim();
  if (!lastQuery) return;
  setLoading(true);
  retry.hidden = true;
  clearAnswer();
  try {
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({query: lastQuery}),
    });
    if (!response.ok) {  // lỗi trước khi mở luồng: JSON như /api/chat
      const payload = await response.json();
      throw new Error(payload.error?.message || "Đã xảy ra lỗi.");
    }
    await readAnswerStream(response);
    status.textContent = "";
  } catch (error) {
    clearAnswer();
    status.textContent = error.message;
    retry.hidden = false;
  } finally {
    setLoading(false);
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  ask(query.value);
});
retry.addEventListener("click", () => ask(lastQuery));
