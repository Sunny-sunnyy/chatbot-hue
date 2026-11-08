import { useEffect, useState } from "react";

// Điều hướng bằng hash (spec cổng đợt 1 D5): 0 gói router, server chỉ phục vụ `/` ⇒ tải lại / chia sẻ link vẫn đúng trang.
//   #/                       trang chủ
//   #/kham-pha               5 lĩnh vực
//   #/kham-pha/<linh_vuc>    danh sách bài một lĩnh vực (mã = tên thư mục kho)
//   #/kham-pha/bai/<id>      một bài (id = đường dẫn bài trong kho, có dấu `/`)
//   #/len-ke-hoach · #/tro-ly · #/gioi-thieu
//   #/gioi-thieu/<mục>       trang Giới thiệu, cuộn tới mục có id đó (vd `nguon-anh` — link "Nguồn ảnh" ở chân trang)
// Hash lạ ⇒ trang chủ.
export function parseHash(hash) {
  let path;
  try {
    path = decodeURIComponent(hash.replace(/^#\/?/, ""));
  } catch {
    return { page: "trang-chu" };  // `%` lẻ (link gõ tay) ⇒ không làm hỏng trang
  }
  const parts = path.split("/").filter(Boolean);
  if (parts[0] === "kham-pha") {
    if (parts[1] === "bai" && parts.length > 2) return { page: "bai", baiId: parts.slice(2).join("/") };
    if (parts[1]) return { page: "linh-vuc", linhVuc: parts[1] };
    return { page: "kham-pha" };
  }
  if (parts[0] === "gioi-thieu") return parts[1] ? { page: "gioi-thieu", muc: parts[1] } : { page: "gioi-thieu" };
  if (["len-ke-hoach", "tro-ly"].includes(parts[0])) return { page: parts[0] };
  return { page: "trang-chu" };
}

export function baiHref(id) {
  return `#/kham-pha/bai/${id.split("/").map(encodeURIComponent).join("/")}`;
}

export function useRoute() {
  const [route, setRoute] = useState(() => parseHash(window.location.hash));
  useEffect(() => {
    const onChange = () => {
      setRoute(parseHash(window.location.hash));
      window.scrollTo(0, 0);
    };
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return route;
}
