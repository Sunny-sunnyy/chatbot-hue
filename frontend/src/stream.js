// Gọi `POST /api/chat/stream` và đọc luồng SSE (hợp đồng: report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md, yêu cầu 1–7, 11, 17).

export const INTERRUPTED_MESSAGE = "Kết nối bị gián đoạn. Vui lòng thử lại.";
const CONNECTION_MESSAGE = "Không kết nối được máy chủ. Vui lòng thử lại.";
const SERVER_ERROR_MESSAGE = "Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau.";

// Lỗi mang lời viết cho người dùng (của server hoặc của trang). Lỗi khác (mạng, JSON hỏng…) mang chữ kỹ thuật tiếng Anh của trình duyệt
// ⇒ không hiện ra, đổi sang một câu cố định (review C119 m-1).
class StreamError extends Error {}

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

// `onEvent` nhận `status` / `delta` / `sources` / `notice` (B1 H4c) / `done` (B3 bước 8: `outcome`: câu ngoài phạm vi có gợi ý riêng). Mọi lỗi khác ⇒ ném `StreamError` mang lời tiếng Việt cho người dùng: lời của server (JSON lỗi
// trước luồng, sự kiện `error`) giữ nguyên; mạng / thân lỗi không phải JSON / luồng hỏng hoặc đứt ⇒ câu cố định.
// `signal` (AbortController) huỷ `fetch` ⇒ server thấy ngắt kết nối, dừng model (yêu cầu 17); khi đó hàm ném `AbortError`.
// B4: `truong` (giá trị chọn ở thẻ hỏi lại, `{}` = "Trả lời luôn") gửi kèm câu gốc; server ghép câu đủ ý.
// Cổng D3: `bieuMau` = lượt từ biểu mẫu "Lên kế hoạch" (server dựng câu từ `truong`, không dùng chữ `query`).
export async function streamAnswer(query, { signal, onEvent, truong = null, bieuMau = false }) {
  let response;
  try {
    response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, ...(truong !== null && { truong }), ...(bieuMau && { bieu_mau: true }) }),
      signal,
    });
  } catch (error) {
    if (error.name === "AbortError") throw error;
    throw new StreamError(CONNECTION_MESSAGE);
  }
  if (!response.ok) {  // lỗi trước khi mở luồng: JSON như /api/chat; thân khác (vd trang 502 của proxy) ⇒ câu cố định
    const payload = await response.json().catch(() => null);
    throw new StreamError(payload?.error?.message || SERVER_ERROR_MESSAGE);
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  const feed = createSseParser((name, data) => {
    if (name === "error") throw new StreamError(data.message || INTERRUPTED_MESSAGE);
    if (name === "done") done = true;
    onEvent(name, data);
  });
  try {
    while (!done) {
      const { value, done: ended } = await reader.read();
      if (ended) break;
      feed(decoder.decode(value, { stream: true }));
    }
  } catch (error) {
    reader.cancel().catch(() => {});
    if (error.name === "AbortError" || error instanceof StreamError) throw error;
    throw new StreamError(INTERRUPTED_MESSAGE);  // mạng đứt giữa luồng, `data:` không phải JSON…
  }
  if (!done) throw new StreamError(INTERRUPTED_MESSAGE);  // luồng đứt không có `done` ⇒ xử lý như lỗi
}
