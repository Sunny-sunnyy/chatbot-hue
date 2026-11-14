// Lớp hiệu ứng H1 (đợt 0 giao diện, 14/11/2026). Không thư viện.
// Máy không bật giảm chuyển động ⇒ <html class="hieu-ung"> (mọi hiệu ứng trong hieu_ung.css chỉ chạy dưới lớp này).
// Trình duyệt chưa có animation-timeline ⇒ dự phòng: IntersectionObserver cho .hien (kể cả phần tử React vẽ sau — MutationObserver),
// sự kiện cuộn cho thanh menu .hd-cuon.
export function giamChuyenDong() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function batHieuUng() {
  if (giamChuyenDong()) return;
  document.documentElement.classList.add("hieu-ung");
  if (!CSS.supports("animation-timeline: view()")) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add("da-hien"); io.unobserve(e.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    const quet = root => root.querySelectorAll?.(".hien:not(.da-hien), .chu-hien:not(.da-hien)").forEach(el => io.observe(el));
    new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => {
      if (n.nodeType !== 1) return;
      if (n.matches(".hien:not(.da-hien), .chu-hien:not(.da-hien)")) io.observe(n);
      quet(n);
    }))).observe(document.body, { childList: true, subtree: true });
  }
  if (!CSS.supports("animation-timeline: scroll()")) {
    const doi = () => document.querySelector(".hd-cuon")?.classList.toggle("da-cuon", window.scrollY > 120);
    window.addEventListener("scroll", doi, { passive: true });
  }
}
