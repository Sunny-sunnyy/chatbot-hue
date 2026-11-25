import { lazy, Suspense, useEffect, useState } from "react";
import { ChatView, TrangTroLy, useChat } from "./chat.jsx";
import { CAU_BIEU_MAU, GOI_Y } from "./chung.jsx";
import { TrangChu } from "./TrangChu.jsx";
import { Bai, KhamPha, LinhVuc } from "./KhamPha.jsx";
import { LenKeHoach, LenKeHoachV2 } from "./LenKeHoach.jsx";
import { GioiThieu } from "./GioiThieu.jsx";
import { ChoO } from "./ChoO.jsx";
import { useRoute } from "./route.js";
import { datNguonBanDo } from "./nguonBanDo.js";
import { batHoanTac, batSoTay, batXuatLich } from "./LichV2.jsx";
import { SoTay, useSoTay } from "./SoTay.jsx";
import { DaiChuDe, HoSoChuDe, LuoiChuDe, useHoSo } from "./HoSo.jsx";

const TrangBanDo = lazy(() => import("./TrangBanDo.jsx"));  // tải riêng ⇒ trang khác không tải Leaflet
const TheoDoi = lazy(() => import("./TheoDoi.jsx"));  // trang riêng của chủ dự án, không có trong menu

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
  const soTay = useSoTay();  // bản thử "Sổ tay cho chuyến đi" (công tắc server `so_tay`)
  const hoSo = useHoSo();    // bản thử "Hồ sơ theo chủ đề" (công tắc server `ho_so_chu_de`)
  const [tinhNang, setTinhNang] = useState(TINH_NANG_TAT);
  const [daCoTinhNang, setDaCoTinhNang] = useState(false);  // H1: chưa biết cờ ⇒ trang Lên kế hoạch giữ chỗ (không vẽ biểu mẫu cũ rồi đổi — C đo CLS 0,22)
  const [bai, setBai] = useState(null);
  const [baiLoi, setBaiLoi] = useState("");
  const [thoiTiet, setThoiTiet] = useState(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [planPrefill, setPlanPrefill] = useState(null);
  const onTroLy = route.page === "tro-ly";

  useEffect(() => {
    getJson("/api/tinh_nang").then(t => {
      datNguonBanDo(t.ban_do); batXuatLich(t.xuat_pptx);
      // nút ở thẻ lịch: dựng lại sổ tay từ lịch MỚI NHẤT của cuộc rồi sang trang đọc (lịch có thể vừa được sửa bằng lời)
      batSoTay(t.so_tay === true ? () => { soTay.tao(); window.location.hash = "#/so-tay"; } : null);
      setTinhNang(t);
    }).catch(() => setTinhNang(TINH_NANG_TAT)).finally(() => setDaCoTinhNang(true));  // lỗi ⇒ coi như mọi cờ tắt (ẩn mục)
    getJson("/api/kham_pha").then(data => setBai(data.bai)).catch(() => setBaiLoi("Chưa tải được danh sách bài — thử tải lại trang."));
  }, []);
  useEffect(() => {
    if (tinhNang.thoi_tiet) getJson("/api/thoi_tiet").then(setThoiTiet).catch(() => setThoiTiet(null));  // lỗi ⇒ ẩn ô, không số cũ
  }, [tinhNang.thoi_tiet]);
  useEffect(() => { if (onTroLy) setPanelOpen(false); }, [onTroLy]);
  useEffect(() => { batHoanTac(chat.hoanTac); });  // bản thử nút "Hoàn tác lần sửa này": thẻ lịch gọi hàm của cuộc trò chuyện hiện tại (mỗi lần vẽ lấy bản mới)
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
  // Cột lịch của trang = lịch MỚI NHẤT của cuộc (User 16/11): lượt biểu mẫu cuối, hoặc lượt sửa bằng lời ĐÃ XONG sau nó có ít nhất một thay đổi làm được
  // (`lichV2.thay_doi[].duoc`). Lượt sửa đang chạy / bị dừng / lỗi / ra thẻ chọn / không đổi được gì ⇒ không đủ điều kiện ⇒ cột giữ lịch tốt gần nhất.
  // `truong` lấy của lượt biểu mẫu: nút "Sửa — điền lại biểu mẫu" điền theo biểu mẫu gốc (không đồng bộ nút theo lời); khoá riêng để id trong cột
  // không trùng id của cùng lượt đang vẽ trong khung trợ lý.
  const viTriGoc = chat.turns.findLastIndex(t => t.bieuMau);
  const gocTurn = viTriGoc >= 0 ? chat.turns[viTriGoc] : null;
  const sauGoc = gocTurn ? chat.turns.slice(viTriGoc + 1) : [];
  const suaTurn = gocTurn && sauGoc.findLast(t => t.phase === "done" && t.lichV2 && (t.lichV2.thay_doi || []).some(d => d.duoc));
  // Lượt sửa XONG mới nhất mà KHÔNG áp được gì (mọi dòng là "Chưa làm…" / "Không đổi được…") đứng sau bản lịch đang hiện: lịch giữ nguyên nhưng cột
  // phải nói điều đó — khối báo của cột = các dòng "Đã…" của bản lịch đang hiện + dòng báo của lượt mới này (thay dòng "Chưa làm" đã cũ của lượt trước;
  // lượt đo trình duyệt 21/11: người chỉ nhìn trang không biết lệnh "thêm…" chưa được làm).
  const cuoiTurn = sauGoc.findLast(t => t.phase === "done" && t.lichV2 && (t.lichV2.thay_doi || []).length > 0);
  const baoMoi = cuoiTurn && cuoiTurn !== suaTurn ? cuoiTurn.lichV2.thay_doi : null;
  // Soát khác hãng 22/11 (G4): lượt mới đó có thể mang câu an toàn bão / lũ + 112 (`noticeAnToan`) ⇒ cột — và bản in, bản chép, .ics lấy từ cột —
  // phải có câu ấy như khung chat; trước đây chỉ các dòng báo được chép sang, câu an toàn thì mất.
  const voiBao = t => (baoMoi ? { ...t, noticeAnToan: cuoiTurn.noticeAnToan || t.noticeAnToan,
                                  lichV2: { ...t.lichV2, thay_doi: [...(t.lichV2.thay_doi || []).filter(d => d.duoc), ...baoMoi] } } : t);
  // `question` + `summary` cũng của lượt biểu mẫu: dòng đầu của "Sao chép lịch" là tóm tắt biểu mẫu, không phải câu chat của lượt sửa
  const lichTurn = suaTurn
    ? voiBao({ ...suaTurn, key: `${suaTurn.key}-cot`, truong: gocTurn.truong, question: gocTurn.question, summary: gocTurn.summary, daSua: true })
    : gocTurn && gocTurn.lichV2 ? voiBao(gocTurn) : gocTurn;

  // `chon` = lựa chọn bộ xếp đã dùng (biểu mẫu cũ); `truong` = giá trị đã gửi — biểu mẫu bản 2 điền lại từ đây (server đổi giá trị mới về trường cũ)
  function editPlan(chon, truong) {
    setPlanPrefill({ ...(tinhNang.len_ke_hoach_v2 && truong ? truong : chon) });
    setPanelOpen(false);
    // đang ở chính trang Lên kế hoạch ⇒ hash không đổi, trang không tự cuộn: nút nằm cuối lịch, biểu mẫu ở trên ngoài màn hình ⇒ bấm mà "không thấy
    // gì" (User 15/11) ⇒ cuộn tới biểu mẫu. Từ trang khác: đổi hash đã đưa về đầu trang (có biểu mẫu).
    if (route.page === "len-ke-hoach") {
      const form = document.querySelector("form.lc");
      form?.scrollIntoView({ behavior: "smooth", block: "start" });
      form?.querySelector("button, input")?.focus({ preventScroll: true });  // bàn phím / trình đọc màn hình cũng về biểu mẫu
    }
    window.location.hash = "#/len-ke-hoach";
  }

  const nav = [
    { href: "#/", ten: "Trang chủ", on: route.page === "trang-chu" },
    { href: "#/kham-pha", ten: "Khám phá", on: ["kham-pha", "linh-vuc", "bai", "chu-de", "ho-so"].includes(route.page) },
    ...(tinhNang.ban_do_lich ? [{ href: "#/ban-do", ten: "Bản đồ", on: route.page === "ban-do" }] : []),
    ...(tinhNang.lich_trinh_bieu_mau ? [{ href: "#/len-ke-hoach", ten: "Lên kế hoạch", on: route.page === "len-ke-hoach" || route.page === "so-tay" }] : []),
    { href: "#/tro-ly", ten: TEN_TRO_LY, on: onTroLy },
    { href: "#/gioi-thieu", ten: "Giới thiệu", on: route.page === "gioi-thieu" },
  ];

  // Thanh dưới ở điện thoại: bốn mục + nút tròn "Trợ lý" ở GIỮA. Có "Bản đồ" ⇒ bỏ "Giới thiệu" khỏi thanh (sáu mục làm nút tròn lệch, chữ xuống hai
  // dòng — đo 390 px 20/11); "Giới thiệu" vẫn vào được từ chân trang và trang chủ.
  const navDuoi = nav.filter(item => item.href !== "#/tro-ly" && !(tinhNang.ban_do_lich && item.href === "#/gioi-thieu"));

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
        {route.page === "trang-chu" && <TrangChu bai={bai} tinhNang={tinhNang} thoiTiet={thoiTiet} onAsk={askAnywhere} onAskAbout={askAbout}
                                                 /* bản thử: dải hồ sơ theo chủ đề ở Trang chủ — cần CẢ công tắc hồ sơ lẫn khoá riêng `chu_de_trang_chu` (server chưa gửi) */
                                                 dai={tinhNang.ho_so_chu_de === true && tinhNang.chu_de_trang_chu === true ? <DaiChuDe hoSo={hoSo} tieuDe="Hồ sơ theo chủ đề" /> : null} />}
        {route.page === "kham-pha" && <KhamPha bai={bai} loi={baiLoi} dai={tinhNang.ho_so_chu_de === true ? <DaiChuDe hoSo={hoSo} /> : null} />}
        {(route.page === "chu-de" || route.page === "ho-so") && daCoTinhNang && (tinhNang.ho_so_chu_de === true
          ? (route.page === "chu-de" ? <LuoiChuDe hoSo={hoSo} /> : <HoSoChuDe ma={route.ma} hoSo={hoSo} />)
          : <div className="khung"><p>Trang hồ sơ theo chủ đề chưa bật. <a href="#/kham-pha">Về trang Khám phá</a></p></div>)}
        {route.page === "linh-vuc" && <LinhVuc linhVuc={route.linhVuc} bai={bai} loi={baiLoi} />}
        {route.page === "bai" && <Bai baiId={route.baiId} bai={bai} onAskAbout={askAbout} />}
        {route.page === "len-ke-hoach" && !daCoTinhNang && <div className="lkh-cho" aria-busy="true" />}
        {route.page === "len-ke-hoach" && daCoTinhNang && (
          tinhNang.len_ke_hoach_v2
            ? <LenKeHoachV2 cauHinh={tinhNang.len_ke_hoach_v2} prefill={planPrefill} pending={chat.pending} onSubmit={submitPlan}
                            lichTurn={lichTurn} onEditPlan={editPlan} onAsk={chat.pending ? null : (q, opts) => chat.ask(q, opts)} />
            : <LenKeHoach bat={tinhNang.lich_trinh_bieu_mau} prefill={planPrefill} pending={chat.pending} onSubmit={submitPlan} />
        )}
        {route.page === "cho-o" && <ChoO khu={route.khu} />}
        {route.page === "so-tay" && daCoTinhNang && (tinhNang.so_tay === true
          ? <SoTay soTay={soTay} />
          : <div className="khung"><p>Trang sổ tay chưa bật. <a href="#/len-ke-hoach">Về trang Lên kế hoạch</a></p></div>)}
        {route.page === "theo-doi" && <Suspense fallback={<div className="khung co-cho" aria-busy="true" />}><TheoDoi /></Suspense>}
        {route.page === "ban-do" && daCoTinhNang && (tinhNang.ban_do_lich
          ? <Suspense fallback={<div className="khung co-cho" aria-busy="true" />}><TrangBanDo /></Suspense>
          : <div className="khung"><p>Trang bản đồ chưa bật. <a href="#/">Về trang chủ</a></p></div>)}
        {route.page === "gioi-thieu" && <GioiThieu tinhNang={tinhNang} daCo={daCoTinhNang} muc={route.muc} />}
        {onTroLy && <TrangTroLy chat={chat} onEditPlan={editPlan} tinhNang={tinhNang} />}
      </main>

      {!onTroLy && <footer className="ft"><div className="khung">{TEN_DAY_DU} — đồ án tốt nghiệp. Trả lời từ kho tư liệu về Huế, có thể sai. <a href="#/gioi-thieu">Giới thiệu</a></div></footer>}

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
        {navDuoi.slice(0, 2).map(item => (
          <a key={item.href} href={item.href} className="td-a" aria-current={item.on ? "page" : undefined}>{item.ten}</a>
        ))}
        <a href="#/tro-ly" className="td-giua" aria-current={onTroLy ? "page" : undefined}>{TEN_TRO_LY}</a>
        {navDuoi.slice(2).map(item => (
          <a key={item.href} href={item.href} className="td-a" aria-current={item.on ? "page" : undefined}>{item.ten}</a>
        ))}
      </nav>
    </div>
  );
}
