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

function renderResponse(payload) {
  answer.innerHTML = DOMPurify.sanitize(marked.parse(payload.answer));
  renderSources(payload.sources);
  wireCitations();
}

async function ask(value) {
  if (pending) return;
  lastQuery = value.trim();
  if (!lastQuery) return;
  setLoading(true);
  retry.hidden = true;
  answer.replaceChildren();
  sources.replaceChildren();
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({query: lastQuery}),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error?.message || "Đã xảy ra lỗi.");
    renderResponse(payload);
    status.textContent = "";
  } catch (error) {
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
