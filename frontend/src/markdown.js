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

// Số hiển thị của nguồn (B3 D9 (c)): sổ nguồn đánh số nối qua mọi lần `tim_kho` ([17] dù chỉ 2 nguồn) — code kiểm trích dẫn, judge, log giữ số gốc;
// người đọc thấy 1..k theo thứ tự xuất hiện đầu tiên trong câu. Nguồn được trích mà không thấy mã trong chữ (không nên có) xếp cuối.
// Trả Map(số gốc dạng chuỗi ⇒ số hiển thị).
export function displayNumbers(text, sources) {
  const cited = new Set(sources.map(source => String(source.id)));
  const numbers = new Map();
  for (const match of text.matchAll(CITATION)) {
    if (cited.has(match[1]) && !numbers.has(match[1])) numbers.set(match[1], numbers.size + 1);
  }
  for (const id of cited) if (!numbers.has(id)) numbers.set(id, numbers.size + 1);
  return numbers;
}

// Markdown ⇒ HTML đã lọc, rồi đổi trích dẫn thành số nhỏ nâng lên. `numbers` = null khi chưa có sự kiện `sources` ⇒ số gốc chỉ là chữ mờ, không
// bấm được (yêu cầu 9); có `sources` ⇒ số thuộc `numbers` thành link tới nguồn, hiện số hiển thị (đổi tại chỗ). `turnKey` tách id nguồn giữa các
// lượt; `activeId` = số gốc đang chọn (aria-current). Đổi trên nút chữ SAU bộ lọc, phần tử dựng bằng DOM — không ghép chuỗi HTML.
export function renderAnswerHtml(text, numbers, turnKey, activeId) {
  const template = document.createElement("template");  // nội dung <template> trơ: không chạy script, không tải tài nguyên
  template.innerHTML = DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS);
  markCitations(template.content, mark => citationMark(mark, numbers, turnKey, activeId));
  return template.innerHTML;
}

function markCitations(root, makeMark) {
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
      fragment.append(text.slice(last, match.index), makeMark(match[1]));
      last = match.index + match[0].length;
    }
    if (last === 0) continue;
    fragment.append(text.slice(last));
    node.replaceWith(fragment);
  }
}

function citationMark(id, numbers, turnKey, activeId) {
  const sup = document.createElement("sup");
  sup.className = "cite";
  const shown = numbers?.get(id);
  if (!shown) {
    sup.textContent = id;
    return sup;
  }
  const link = document.createElement("a");
  link.href = `#source-${turnKey}-${id}`;
  link.dataset.cite = id;
  link.setAttribute("aria-label", `Nguồn ${shown}`);
  if (id === activeId) link.setAttribute("aria-current", "true");
  link.textContent = String(shown);
  sup.append(link);
  return sup;
}

// B6 D6: mục "Từ web (chưa kiểm)" — chữ model đã qua kiểm cuối của server (mã [w n] ∈ sổ, 0 link). Mã [w n] thành số nhỏ nâng lên trỏ tới mục
// nguồn web cùng lượt (`#web-<lượt>-<n>`); mã không thuộc `sources` chỉ là chữ mờ. Không đổi mã kho [n] (mục web không có mã kho).
const WEB_CITATION = /\[\s*w\s*(\d+)\s*\]/giu;

// Review E13 M-1: chữ model ở khối web KHÔNG được tạo link — bộ lọc riêng bỏ thẻ `a` + thuộc tính `href` (HTML thô `<a href="//…">` qua được bộ lọc
// chung). Link web chỉ ở danh sách nguồn do code dựng; số [w n] là link nội bộ dựng bằng DOM SAU bộ lọc.
export const WEB_SANITIZE_OPTIONS = {
  ALLOWED_TAGS: SANITIZE_OPTIONS.ALLOWED_TAGS.filter(tag => tag !== "a"),
  ALLOWED_ATTR: SANITIZE_OPTIONS.ALLOWED_ATTR.filter(attr => attr !== "href"),
};

export function renderWebHtml(text, sources, turnKey) {
  const ids = new Set(sources.map(source => String(source.id)));
  const template = document.createElement("template");
  template.innerHTML = DOMPurify.sanitize(marked.parse(text), WEB_SANITIZE_OPTIONS);
  const walker = document.createTreeWalker(template.content, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) {
    if (!walker.currentNode.parentElement?.closest("a, code, pre")) nodes.push(walker.currentNode);
  }
  for (const node of nodes) {
    const value = node.nodeValue;
    const fragment = document.createDocumentFragment();
    let last = 0;
    for (const match of value.matchAll(WEB_CITATION)) {
      const sup = document.createElement("sup");
      sup.className = "cite";
      if (ids.has(match[1])) {
        const link = document.createElement("a");
        link.href = `#web-${turnKey}-${match[1]}`;
        link.setAttribute("aria-label", `Nguồn web ${match[1]}`);
        link.textContent = `w${match[1]}`;
        sup.append(link);
      } else {
        sup.textContent = `w${match[1]}`;
      }
      fragment.append(value.slice(last, match.index), sup);
      last = match.index + match[0].length;
    }
    if (last === 0) continue;
    fragment.append(value.slice(last));
    node.replaceWith(fragment);
  }
  return template.innerHTML;
}
