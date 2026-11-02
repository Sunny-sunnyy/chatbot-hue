import { marked } from "marked";
import DOMPurify from "dompurify";

// Câu trả lời là Markdown do model viết: ngoài chặn script, không để trang TỰ tải gì từ máy khác khi hiện chữ (ảnh, `background`, CSS `url(…)`,
// `<input type=image>`, form…). Dùng DANH SÁCH CHO PHÉP — đúng các thẻ / thuộc tính Markdown thường tạo ra — thay vì danh sách cấm (review C107 M-1).
// Không thuộc tính nào chứa URL ngoài `href` của link: link chỉ mở khi người dùng bấm (yêu cầu 13, 16).
export const SANITIZE_OPTIONS = {
  ALLOWED_TAGS: ["p", "br", "hr", "strong", "em", "del", "code", "pre", "blockquote", "ul", "ol", "li",
                 "h1", "h2", "h3", "h4", "h5", "h6", "a", "table", "thead", "tbody", "tr", "th", "td"],
  ALLOWED_ATTR: ["href", "title", "align", "start"],
};

// Cùng mẫu với `backend/llm/citations.py` CITATION_PATTERN: model viết cả `[n]` lẫn `[Nguồn n]`, mà chữ hiện dần là chữ thô chưa chuẩn hoá (yêu cầu 18).
const CITATION = /\[\s*(?:nguồn\s*)?(\d+)\s*\]/giu;

// Markdown ⇒ HTML đã lọc, rồi đổi trích dẫn thành số nhỏ nâng lên. `citedIds` = null khi chưa có sự kiện `sources` ⇒ số chỉ là chữ mờ, không bấm được
// (yêu cầu 9); có `sources` ⇒ số thuộc `citedIds` thành link tới nguồn. Đổi trên nút chữ SAU bộ lọc, phần tử dựng bằng DOM — không ghép chuỗi HTML.
export function renderAnswerHtml(text, citedIds) {
  const template = document.createElement("template");  // nội dung <template> trơ: không chạy script, không tải tài nguyên
  template.innerHTML = DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS);
  markCitations(template.content, citedIds);
  return template.innerHTML;
}

function markCitations(root, citedIds) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) {
    if (!walker.currentNode.parentElement?.closest("a, code, pre")) nodes.push(walker.currentNode);
  }
  for (const node of nodes) {
    const text = node.nodeValue;
    const fragment = document.createDocumentFragment();
    let last = 0;
    for (const match of text.matchAll(CITATION)) {
      fragment.append(text.slice(last, match.index), citationMark(match[1], citedIds));
      last = match.index + match[0].length;
    }
    if (last === 0) continue;
    fragment.append(text.slice(last));
    node.replaceWith(fragment);
  }
}

function citationMark(id, citedIds) {
  const sup = document.createElement("sup");
  sup.className = "cite";
  if (!citedIds?.has(id)) {
    sup.textContent = id;
    return sup;
  }
  const link = document.createElement("a");
  link.href = `#source-${id}`;
  link.dataset.cite = id;
  link.setAttribute("aria-label", `Nguồn ${id}`);
  link.textContent = id;
  sup.append(link);
  return sup;
}
