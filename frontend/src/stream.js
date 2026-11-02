// Gọi `POST /api/chat/stream` và đọc luồng SSE (hợp đồng: report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md, yêu cầu 1–7, 11, 17).

export const INTERRUPTED_MESSAGE = "Kết nối bị gián đoạn. Vui lòng thử lại.";

// Tách luồng SSE thành sự kiện. Một lần `read()` có thể chứa nửa sự kiện hoặc nhiều sự kiện ⇒ giữ phần dở tới lần sau; bỏ dòng chú thích `:`.
export function createSseParser(onEvent) {
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

// `onEvent` nhận `status` / `delta` / `sources`. Sự kiện `error`, lỗi trước luồng và luồng đứt không có `done` ⇒ ném Error mang lời báo cho người dùng.
// `signal` (AbortController) huỷ `fetch` ⇒ server thấy ngắt kết nối, dừng model (yêu cầu 17); khi đó hàm ném `AbortError`.
export async function streamAnswer(query, { signal, onEvent }) {
  const response = await fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
    signal,
  });
  if (!response.ok) {  // lỗi trước khi mở luồng: JSON như /api/chat
    const payload = await response.json();
    throw new Error(payload.error?.message || "Đã xảy ra lỗi.");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  const feed = createSseParser((name, data) => {
    if (name === "error") throw new Error(data.message || INTERRUPTED_MESSAGE);
    if (name === "done") done = true;
    else onEvent(name, data);
  });
  try {
    while (!done) {
      const { value, done: ended } = await reader.read();
      if (ended) break;
      feed(decoder.decode(value, { stream: true }));
    }
  } catch (error) {
    reader.cancel().catch(() => {});
    throw error;
  }
  if (!done) throw new Error(INTERRUPTED_MESSAGE);  // luồng đứt không có `done` ⇒ xử lý như lỗi
}
