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
// Cổng đợt 1 D1: chữ hiển thị KHÔNG có số [n] (tầng máy vẫn giữ + kiểm). Bỏ cả khoảng trắng đứng trước số; chữ đang hiện dần có thể dừng giữa
// một mã ("… [1") ⇒ bỏ luôn phần mã dở ở cuối.
const CITATION_SHOWN = /\s*\[\s*(?:nguồn\s*)?\d+\s*\]/giu;
const CITATION_TAIL = /\s*\[\s*(?:n(?:g(?:u(?:ồ(?:n)?)?)?)?\s*)?\d*\s*$/iu;
const WEB_CITATION_SHOWN = /\s*\[\s*w\s*\d+\s*\]/giu;
const WEB_CITATION_TAIL = /\s*\[\s*w?\s*\d*\s*$/iu;
const EXTERNAL = /^(https?:)?\/\//i;  // cả link `//host` (cùng giao thức) — review S4 m-f1

// Thứ tự nguồn ở dòng "Nguồn: …" (B3 D9 (c)): theo lần xuất hiện đầu tiên của mã trong câu; nguồn được trích mà không thấy mã (không nên có) xếp cuối.
// Trả Map(số gốc dạng chuỗi ⇒ thứ tự 1..k).
export function displayNumbers(text, sources) {
  const cited = new Set(sources.map(source => String(source.id)));
  const numbers = new Map();
  for (const match of text.matchAll(CITATION)) {
    if (cited.has(match[1]) && !numbers.has(match[1])) numbers.set(match[1], numbers.size + 1);
  }
  for (const id of cited) if (!numbers.has(id)) numbers.set(id, numbers.size + 1);
  return numbers;
}

// D11: link ra ngoài mở tab mới, không để trang kia điều khiển tab này / biết trang gửi. Sửa trên HTML đã lọc, bằng DOM (không ghép chuỗi).
function withSafeLinks(html) {
  const template = document.createElement("template");  // nội dung <template> trơ: không chạy script, không tải tài nguyên
  template.innerHTML = html;
  for (const link of template.content.querySelectorAll("a[href]")) {
    if (EXTERNAL.test(link.getAttribute("href"))) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    }
  }
  return template.innerHTML;
}

// Markdown của câu trả lời ⇒ HTML đã lọc, bỏ số [n] (D1). Bỏ trên chữ thô trước khi dựng (chữ trong code cũng mất số — không hại).
// "Lên kế hoạch" bản 2: câu của từng mục là chữ thường (không Markdown) — chỉ bỏ mã trích dẫn như chữ trả lời; React tự thoát ký tự HTML.
export function boMaTrichDan(text) {
  return text.replace(CITATION_SHOWN, "").replace(CITATION_TAIL, "");
}

export function renderAnswerHtml(raw) {
  const text = raw.replace(CITATION_SHOWN, "").replace(CITATION_TAIL, "");
  return withSafeLinks(DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS));
}

// Bài kho ở trang Khám phá (D11): cùng bộ lọc; bỏ dòng tiêu đề `# …` đầu bài (trang đã có tiêu đề lớn).
export function renderArticleHtml(markdown) {
  const text = markdown.replace(/^# .*\n?/, "");
  return withSafeLinks(DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS));
}

// Review E13 M-1: chữ model ở khối web KHÔNG được tạo link — bộ lọc riêng bỏ thẻ `a` + thuộc tính `href` (HTML thô `<a href="//…">` qua được bộ lọc
// chung). Link web chỉ ở danh sách nguồn do code dựng.
export const WEB_SANITIZE_OPTIONS = {
  ALLOWED_TAGS: SANITIZE_OPTIONS.ALLOWED_TAGS.filter(tag => tag !== "a"),
  ALLOWED_ATTR: SANITIZE_OPTIONS.ALLOWED_ATTR.filter(attr => attr !== "href"),
};

// B6 D6 + cổng D1: mục "Từ web (chưa kiểm)" — chữ đã qua kiểm cuối của server; mã [w n] bỏ khỏi chữ (nguồn web liệt kê ngay dưới).
export function renderWebHtml(raw) {
  const text = raw.replace(WEB_CITATION_SHOWN, "").replace(WEB_CITATION_TAIL, "");
  return DOMPurify.sanitize(marked.parse(text), WEB_SANITIZE_OPTIONS);
}

// Đoạn trích nguồn (khung mở từ dòng "Nguồn: …") là một LÁT Markdown của bài kho — trước 15/11 hiện chữ thô nên lộ `**`, `- `, `#`, `|`.
// Hàng bảng bị cắt rời khỏi dòng tiêu đề + dòng gạch (`| a | b |` đứng một mình) thì Markdown không coi là bảng ⇒ đổi thành "a · b" trước khi dựng.
export function hangBangLe(text) {
  const lines = text.split("\n");
  const laHang = line => /^\s*\|.*\|\s*$/.test(line);
  const laGach = line => /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(line) && line.includes("-") && line.includes("|");
  return lines.map((line, i) => {
    if (!laHang(line)) return line;
    let dau = i;
    while (dau > 0 && laHang(lines[dau - 1])) dau -= 1;  // khối hàng liền nhau: là bảng thật khi hàng thứ hai của khối là dòng gạch
    if (dau + 1 < lines.length && laHang(lines[dau + 1]) && laGach(lines[dau + 1]) && !laGach(lines[dau])) return line;
    if (laGach(line)) return "";
    return line.trim().replace(/^\|\s*|\s*\|$/g, "").split(/\s*\|\s*/).join(" · ");
  }).join("\n");
}

// Một đoạn kho là bảng thường về thành NHIỀU lát: lát "tiêu đề + dòng gạch" rồi từng lát một hàng ⇒ ghép lát bắt đầu bằng hàng bảng vào lát đứng
// trước nếu lát trước kết thúc bằng hàng bảng — thành một bảng thật thay vì bảng chỉ có tiêu đề + các dòng rời.
export function gopLatBang(excerpts) {
  const laHang = line => /^\s*\|.*\|\s*$/.test(line);
  const ra = [];
  for (const lat of excerpts) {
    const truoc = ra[ra.length - 1];
    if (truoc !== undefined && laHang(truoc.split("\n").pop()) && laHang(lat.split("\n")[0])) ra[ra.length - 1] = `${truoc}\n${lat}`;
    else ra.push(lat);
  }
  return ra;
}

// Cùng bộ lọc KHÔNG link của mục web (chữ kho có thể chứa link ở mục nguồn — khung trích không mở đường link mới; link duy nhất là "Đọc cả bài"
// do code dựng). Xuống dòng đơn trong bài kho là ngắt dòng của file (80 cột), không phải ý tác giả ⇒ để Markdown nối lại như trang bài ở Khám phá.
export function renderExcerptHtml(raw) {
  return DOMPurify.sanitize(marked.parse(hangBangLe(raw)), WEB_SANITIZE_OPTIONS);
}
