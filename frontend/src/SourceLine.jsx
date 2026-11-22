import { useState } from "react";
import { baiHref } from "./route.js";
import { gopLatBang, renderExcerptHtml } from "./markdown.js";
import { linhVuc } from "./song/nhin.js";

// Dòng "Nguồn" bấm mở đoạn gốc — dùng chung cho trợ lý và thẻ lịch (tách từ chat.jsx, đợt 0 giao diện H1; hành vi giữ nguyên).
export function SourceLine({ turn }) {
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
        <span className="nguon-nhan">Nguồn đã dùng ({groups.length} bài)</span>{" "}
        {groups.map((group, index) => (
          <span key={group.key}>
            <button type="button" className="nguon-ten" aria-expanded={open === group.key} aria-controls={panelId}
                    data-lv={linhVuc(group.bai_id)}
                    onClick={() => setOpen(open === group.key ? null : group.key)}><i className="nguon-so" aria-hidden="true" />{group.title}</button>
          </span>
        ))}
      </p>
      {shown && (
        <div className="nguon-doan" id={panelId}>
          {shown.parts.map(part => (
            <div key={part.id} className="nguon-phan">
              {part.heading_path.length > 0 && <p className="text-sm text-muted">{part.heading_path.join(" › ")}</p>}
              {gopLatBang(part.excerpts).map((excerpt, index) => <blockquote key={index} dangerouslySetInnerHTML={{ __html: renderExcerptHtml(excerpt) }} />)}
            </div>
          ))}
          {shown.bai_id && <a className="nguon-bai" href={baiHref(shown.bai_id)}>Đọc cả bài “{shown.title}”</a>}
        </div>
      )}
    </div>
  );
}
