import { useEffect, useState } from "react";
import { ChatView, TrangTroLy, useChat } from "./chat.jsx";
import { CAU_BIEU_MAU, GOI_Y } from "./chung.jsx";
import { TrangChu } from "./TrangChu.jsx";
import { Bai, KhamPha, LinhVuc } from "./KhamPha.jsx";
import { LenKeHoach, LenKeHoachV2 } from "./LenKeHoach.jsx";
import { GioiThieu } from "./GioiThieu.jsx";
import { useRoute } from "./route.js";

// Khung cổng du lịch đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md`; bản mẫu 2 "Sông Hương", User chọn 07/11):
// điều hướng bằng hash (D5), trợ lý nổi trên mọi trang + trang `#/tro-ly`, MỘT cuộc trò chuyện qua các trang (D8), điện thoại có thanh dưới.
// Cờ server (`/api/tinh_nang`) ⇒ mục tương ứng ẩn khi tắt.

const TINH_NANG_TAT = { lich_trinh_bieu_mau: false, thoi_tiet: false, anh: false, tra_web: false, ban_do_lich: false };
const TEN_DAY_DU = "Huế · Trải nghiệm văn hóa & du lịch";  // Q-U5 (User 07/11)
const TEN_NGAN = "Trải nghiệm Huế";
const TEN_TRO_LY = "Trợ lý Huế";

function getJson(url) {
  return fetch(url).then(r => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))));
}

export default function App() {
  const route = useRoute();
  const chat = useChat();
  const [tinhNang, setTinhNang] = useState(TINH_NANG_TAT);
  const [bai, setBai] = useState(null);
  const [baiLoi, setBaiLoi] = useState("");
  const [thoiTiet, setThoiTiet] = useState(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [planPrefill, setPlanPrefill] = useState(null);
  const onTroLy = route.page === "tro-ly";

  useEffect(() => {
    getJson("/api/tinh_nang").then(setTinhNang).catch(() => setTinhNang(TINH_NANG_TAT));  // lỗi ⇒ coi như mọi cờ tắt (ẩn mục)
    getJson("/api/kham_pha").then(data => setBai(data.bai)).catch(() => setBaiLoi("Chưa tải được danh sách bài — thử tải lại trang."));
  }, []);
  useEffect(() => {
    if (tinhNang.thoi_tiet) getJson("/api/thoi_tiet").then(setThoiTiet).catch(() => setThoiTiet(null));  // lỗi ⇒ ẩn ô, không số cũ
  }, [tinhNang.thoi_tiet]);
  useEffect(() => { if (onTroLy) setPanelOpen(false); }, [onTroLy]);
  useEffect(() => {
    if (!panelOpen) return undefined;
    const onKey = event => event.key === "Escape" && setPanelOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [panelOpen]);

  // Hỏi từ trang chủ / gợi ý ⇒ mở trợ lý (khung nổi; đang ở trang trợ lý thì hiện tại chỗ). Đang có lượt chạy ⇒ không gửi.
  function askAnywhere(question) {
    if (chat.pending || chat.resetting) return false;
    chat.ask(question);
    if (!onTroLy) setPanelOpen(true);
    return true;
  }

  function askAbout(title) {
    chat.setDraft(`Cho mình biết thêm về ${title}.`);  // D11: câu điền sẵn — người dùng sửa / gửi
    if (!onTroLy) setPanelOpen(true);
  }

  // H1 (14/11, A chốt): biểu mẫu bản 2 ⇒ lịch hiện ngay cột phải trang Lên kế hoạch (cùng lượt trong cuộc trò chuyện) — không chuyển trang;
  // biểu mẫu cũ (cờ bản 2 tắt) giữ đường cũ sang trang trợ lý
  function submitPlan(truong, summary) {
    chat.ask(CAU_BIEU_MAU, { truong, summary, bieuMau: true });
    if (!tinhNang.len_ke_hoach_v2) window.location.hash = "#/tro-ly";
  }
  const lichTurn = [...chat.turns].reverse().find(t => t.bieuMau) || null;

  // `chon` = lựa chọn bộ xếp đã dùng (biểu mẫu cũ); `truong` = giá trị đã gửi — biểu mẫu bản 2 điền lại từ đây (server đổi giá trị mới về trường cũ)
  function editPlan(chon, truong) {
    setPlanPrefill({ ...(tinhNang.len_ke_hoach_v2 && truong ? truong : chon) });
    setPanelOpen(false);
    window.location.hash = "#/len-ke-hoach";
  }

  const nav = [
    { href: "#/", ten: "Trang chủ", on: route.page === "trang-chu" },
    { href: "#/kham-pha", ten: "Khám phá", on: ["kham-pha", "linh-vuc", "bai"].includes(route.page) },
    ...(tinhNang.lich_trinh_bieu_mau ? [{ href: "#/len-ke-hoach", ten: "Lên kế hoạch", on: route.page === "len-ke-hoach" }] : []),
    { href: "#/tro-ly", ten: TEN_TRO_LY, on: onTroLy },
    { href: "#/gioi-thieu", ten: "Giới thiệu", on: route.page === "gioi-thieu" },
  ];

  return (
    <div className={`cong ${panelOpen ? "chat-mo" : ""}`}>
      <header className="hd hd-cuon">
        <div className="hd-in">
          <a className="brand" href="#/">
            <svg width="32" height="32" viewBox="0 0 32 32" aria-hidden="true">
              <circle cx="16" cy="16" r="15" fill="#FFFFFF" />
              <path d="M5 19c4-3 7 3 11 0s7 3 11 0" fill="none" stroke="#0E6B66" strokeWidth="2" strokeLinecap="round" />
              <path d="M9 14l7-6 7 6" fill="none" stroke="#0A3D40" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span className="brand-dai">{TEN_DAY_DU}</span>
            <span className="brand-ngan">{TEN_NGAN}</span>
          </a>
          <nav className="nav" aria-label="Chính">
            {nav.map(item => (
              <a key={item.href} href={item.href} className="nav-a" aria-current={item.on ? "page" : undefined}>{item.ten}</a>
            ))}
          </nav>
        </div>
      </header>

      <main className="noi-dung">
        {route.page === "trang-chu" && <TrangChu bai={bai} tinhNang={tinhNang} thoiTiet={thoiTiet} onAsk={askAnywhere} onAskAbout={askAbout} />}
        {route.page === "kham-pha" && <KhamPha bai={bai} />}
        {route.page === "linh-vuc" && <LinhVuc linhVuc={route.linhVuc} bai={bai} loi={baiLoi} />}
        {route.page === "bai" && <Bai baiId={route.baiId} bai={bai} onAskAbout={askAbout} />}
        {route.page === "len-ke-hoach" && (
          tinhNang.len_ke_hoach_v2
            ? <LenKeHoachV2 cauHinh={tinhNang.len_ke_hoach_v2} prefill={planPrefill} pending={chat.pending} onSubmit={submitPlan}
                            lichTurn={lichTurn} onEditPlan={editPlan} />
            : <LenKeHoach bat={tinhNang.lich_trinh_bieu_mau} prefill={planPrefill} pending={chat.pending} onSubmit={submitPlan} />
        )}
        {route.page === "gioi-thieu" && <GioiThieu banDo={tinhNang.ban_do_lich} anh={tinhNang.anh} muc={route.muc} />}
        {onTroLy && <TrangTroLy chat={chat} onEditPlan={editPlan} tinhNang={tinhNang} />}
      </main>

      {!onTroLy && <footer className="ft"><div className="khung">{TEN_DAY_DU} — đồ án tốt nghiệp. Trả lời từ kho tư liệu về Huế, có thể sai.
        {" "}<a href="#/gioi-thieu/nguon-anh">Nguồn ảnh</a></div></footer>}

      {!onTroLy && !panelOpen && (
        <button type="button" className="noi" aria-expanded="false" aria-controls="khung-tro-ly" onClick={() => setPanelOpen(true)}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"
               aria-hidden="true"><path d="M4 5h16v11H9l-5 4z" /></svg>
          {TEN_TRO_LY}
          {chat.pending && <span className="noi-cham" aria-label="đang trả lời" />}
        </button>
      )}
      {!onTroLy && panelOpen && (
        <section id="khung-tro-ly" className="chat" role="dialog" aria-label={TEN_TRO_LY}>
          <div className="chat-dau">
            <span className="chat-ten">{TEN_TRO_LY}</span>
            <span className="flex items-center gap-1">
              <a className="chat-mo-trang" href="#/tro-ly">Mở trang đầy đủ</a>
              <button type="button" className="chat-dong" aria-label="Đóng trợ lý" aria-expanded="true" aria-controls="khung-tro-ly"
                      onClick={() => setPanelOpen(false)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                  <path d="M6 6l12 12M18 6L6 18" />
                </svg>
              </button>
            </span>
          </div>
          <ChatView chat={chat} idPrefix="noi" suggestions={GOI_Y.slice(0, 3)} onEditPlan={editPlan} anh={tinhNang.anh} />
        </section>
      )}

      <nav className="td" aria-label="Điều hướng nhanh">
        {nav.filter(item => item.href !== "#/tro-ly").slice(0, 2).map(item => (
          <a key={item.href} href={item.href} className="td-a" aria-current={item.on ? "page" : undefined}>{item.ten}</a>
        ))}
        <a href="#/tro-ly" className="td-giua" aria-current={onTroLy ? "page" : undefined}>{TEN_TRO_LY}</a>
        {nav.filter(item => item.href !== "#/tro-ly").slice(2).map(item => (
          <a key={item.href} href={item.href} className="td-a" aria-current={item.on ? "page" : undefined}>{item.ten}</a>
        ))}
      </nav>
    </div>
  );
}
