"""Xem sổ vết debug (core/so_vet.py) cho dễ đọc. Chỉ đọc file private data/debug_trace/<ngày>.jsonl ở máy local.
  uv run python scripts/xem_so_vet.py                 # 3 lượt cuối của hôm nay
  uv run python scripts/xem_so_vet.py -n 10 --ngay 2026-11-15
  uv run python scripts/xem_so_vet.py --ma <turn_id>  # một lượt theo mã (turn_id trong chat_metrics)
  uv run python scripts/xem_so_vet.py --day           # in cả ngữ cảnh gửi model (dài)"""
import argparse, datetime as dt, json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("-n", type=int, default=3); p.add_argument("--ngay", default=dt.date.today().isoformat()); p.add_argument("--ma"); p.add_argument("--day", action="store_true")
a = p.parse_args()
tep = Path(__file__).resolve().parents[1] / "data" / "debug_trace" / f"{a.ngay}.jsonl"
if not tep.exists():
    raise SystemExit(f"chưa có {tep} — sổ vết chỉ ghi khi server chạy với HUE_SO_VET=true")
luot = [json.loads(d) for d in tep.read_text(encoding="utf-8").splitlines() if d.strip()]
luot = [l for l in luot if l["so_do"].get("turn_id") == a.ma] if a.ma else luot[-a.n:]
cat = lambda s, n=300: (s or "").replace("\n", " ⏎ ")[:n]  # noqa: E731
for l in luot:
    s = l["so_do"]
    print("=" * 100)
    print(f"{l['gio']} · {l['duong']} · kết quả {s.get('outcome')} · mã {s.get('turn_id')} · sha {s.get('git_sha')} · {round(s.get('usd') or 0, 6)} USD · {s.get('total_ms') or s.get('ms_tong')} ms")
    if "anh" in l:
        print("  ảnh ⇒ tên gợi ý:", l["anh"]["ten_goi_y"]); continue
    print("  CÂU GÕ      :", cat(l.get("cau_go")))
    if l.get("cau_gui_model") != l.get("cau_go"): print("  GỬI MODEL   :", cat(l.get("cau_gui_model")))
    for hoi, dap in l.get("lich_su") or []: print("  lịch sử     :", cat(hoi, 120), "⇒", cat(dap, 120))
    t = l.get("tuyen") or {}
    print("  TUYẾN       :", t.get("route"), "· lỗi" if t.get("loi") else "", t.get("loi") or "", "· câu tìm định tuyến:" if t.get("cau_tim_dinh_tuyen") else "", t.get("cau_tim_dinh_tuyen") or "")
    for i, tim in enumerate(l.get("tim_kho") or [], 1):
        print(f"  TÌM KHO {i} ({tim['by']}): {tim['cau']}")
        vao = set(tim.get("vao_ngu_canh") or [])
        for k in tim["ket_qua"]: print(f"      {'▶' if k['chunk_id'] in vao else ' '} {k['diem']:<7} {k['chunk_id']}")
    if a.day:
        for i, c in enumerate(l.get("ngu_canh") or [], 1): print(f"  NGỮ CẢNH {i}:\n{c}")
    for c in l.get("goi_model") or []:
        print(f"  gọi model   : {c.get('route')} · {c.get('kind')} · vào {c.get('input_tokens')} (đệm {c.get('cached_tokens')}) ra {c.get('output_tokens')} suy luận {c.get('reasoning_tokens')} · {round(c.get('usd') or 0, 6)} USD · {c.get('ms')} ms")
    for c in l.get("cong_cu") or []: print("  công cụ     :", json.dumps(c, ensure_ascii=False))
    tl = l.get("tra_loi") or {}
    print("  TRẢ LỜI     :", cat(tl.get("chu"), 600), f"· cố định: {tl['ket_qua_co_dinh']}" if tl.get("ket_qua_co_dinh") else "")
    for n in tl.get("nguon_trich") or []: print(f"      nguồn [{n['id']}] {n['title']} · {n['source']} · {' › '.join(n['heading_path'])}")
    if tl.get("loi_trich_dan"): print("  LỖI TRÍCH DẪN:", tl["loi_trich_dan"])
    w = l.get("web")
    if w:
        print(f"  WEB         : {w.get('outcome')} · rào chặn: {w.get('kiem')} · gửi tra web: {w.get('cau_gui_tra_web')}")
        for x in w.get("so_web") or []: print(f"      [w{x.get('id')}] {cat(x.get('title'), 80)} · {x.get('link')}")
        print("      mục hiện :", cat(w.get("text"), 400)); print("      model viết:", cat(w.get("chu_model"), 400))
    if l.get("sua_lich"): print("  SỬA LỊCH    :", json.dumps(l["sua_lich"], ensure_ascii=False)[:800])
    if l.get("loi"): print("  LỖI         :", l["loi"])
