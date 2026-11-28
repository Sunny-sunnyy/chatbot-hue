"""Slide Designer Agent (Agent 2, Đợt 5 — Phần A).

Tách biệt 100% khỏi RAG Agent:
- Không import `llm.assistant`, không tool tìm kho, không web, không OAuth token.
- Nhận `CanonicalItinerary` + manifest ảnh tự host -> trả `SlideDeckPlan` qua Structured Outputs (`AsyncOpenAI.responses.parse`).
- Ghi đủ `input_tokens`, `cached_tokens`, `output_tokens`, `usd` bằng `llm.pricing.cost_usd`.
- Hậu kiểm nghiêm ngặt + vòng tự kiểm tràn chữ (`max_retries=2`) + fallback êm về bộ dựng thuần code `trang_lich_v2` (`0 USD`).
"""
import asyncio
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Literal

logger = logging.getLogger("slide_designer")

from openai import AsyncOpenAI
from openai import OpenAIError
from pydantic import BaseModel, ConfigDict, Field

from api.hanh_trinh_chuan import MAP_PREFIX
from api.pptx_catalog import ALLOWED_LAYOUTS_BY_KIND, ALLOWED_THEMES, chon_theme_mac_dinh
from api.pptx_fit import kiem_tra_tran_chu
from llm.pricing import cost_usd

_URL_LA = re.compile(r"https?://|www\.|\.(?:vn|com|net|org|io|gov)(?:/|\b)", re.IGNORECASE)
_MA_NGUON = re.compile(r"\s*\[(?:Nguồn\s*)?\d+\]")
_GIO_LA = re.compile(r"(?<!\d)\d{1,2}\s*[:hg]\s*\d{2}(?!\d)")
_GIA_TIEN = re.compile(r"\d[\d.,]*\s*(?:đồng|vnd|vnđ|usd|\$|triệu)\b", re.IGNORECASE)
_GHI_CONG_ANH = re.compile(r"(?:CC\s*BY|wikimedia|tác giả|giấy phép)", re.IGNORECASE)

SLIDE_DESIGNER_INSTRUCTIONS = """
Bạn là nhà thiết kế slide trình chiếu cho lịch trình du lịch Huế. Chỉ trả JSON đúng khuôn `SlideDeckPlan`.
Đầu vào là `CanonicalItinerary` đã chuẩn hoá từ kho tư liệu: mọi tên điểm, giờ, bản đồ, ảnh, ghi chú là DỮ LIỆU CỐ ĐỊNH.

Quy tắc bắt buộc:
1. Chọn `theme_id` phù hợp phong cách đoàn:
   - `di_san_tram`: lịch thiên về di tích, lịch sử, cung đình.
   - `song_huong_xanh`: lịch thiên nhiên, đi nhẹ nhàng, đoàn có trẻ em hoặc người lớn tuổi.
   - `co_do_hien_dai`: lịch ẩm thực, chụp ảnh, khám phá nhiều.
2. Chọn `cover_layout` (`cover_hero` hoặc `cover_split`) và `layout_id` cho từng ngày:
   - `day_photo_feature`: ngày ít điểm (1-2 điểm) có ảnh nổi bật.
   - `day_cards_2col`: ngày 2 hoặc 4 điểm có ảnh.
   - `day_timeline`: ngày 3-4 điểm cân đối.
   - `day_compact_grid`: ngày dày 5-6 điểm trở lên.
   Cố gắng đa dạng `layout_id` khi lịch có >= 2 ngày khác nhau.
3. Với mỗi mục trong `days`: giữ nguyên đúng `id_muc` từ đầu vào, không bỏ sót và không tự thêm `id_muc` mới.
4. `short_copy`: rút gọn câu mô tả của chính mục đó cho gọn khung slide ngay từ lần đầu: `<= 85` ký tự với `day_cards_2col` / `day_compact_grid`, `<= 115` ký tự với các layout khác (không mã [n]).
   TUYỆT ĐỐI KHÔNG tự bịa địa điểm, KHÔNG đổi/bịa giờ mở cửa hay giờ đi, KHÔNG nêu giá vé/giá phòng, KHÔNG chèn URL/link hay ghi công tác giả ảnh.
5. `hero_image_id` và `secondary_image_ids` chỉ chọn từ `anh_manifest.diem` có trong đầu vào.
6. Nếu đầu vào có `o_dau`, luôn đặt `include_lodging: true` và `lodging_indices` chỉ dùng chỉ số hợp lệ (0..N-1) của `o_dau.co_so`.
7. Nếu nhận danh sách `overflow_errors`, rút gọn đúng các `slot_id`/`id_muc` bị tràn hoặc đổi ngày sang `day_compact_grid`.
""".strip()


class OverviewDayItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ngay: int
    summary: str = Field(max_length=140)


class DayItemSlot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id_muc: str
    title_override: str | None = Field(default=None, max_length=90)
    short_copy: str | None = Field(default=None, max_length=500)
    show_image: bool = True


class SlideDayPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day_number: int
    layout_id: Literal["day_timeline", "day_cards_2col", "day_photo_feature", "day_compact_grid"]
    day_header: str = Field(max_length=70)
    route_summary: str = Field(max_length=120)
    items: list[DayItemSlot]
    dining_note: str | None = Field(default=None, max_length=190)


class SlideDeckPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    theme_id: Literal["di_san_tram", "song_huong_xanh", "co_do_hien_dai"]
    cover_layout: Literal["cover_hero", "cover_split"]
    deck_title: str = Field(max_length=80)
    deck_subtitle: str = Field(max_length=140)
    highlights: list[str] = Field(max_length=4)
    hero_image_id: str | None = None
    secondary_image_ids: list[str] = Field(max_length=3)
    include_overview: bool = True
    overview_summaries: list[OverviewDayItem]
    days: list[SlideDayPlan]
    include_lodging: bool = True
    lodging_header: str | None = Field(default=None, max_length=80)
    lodging_indices: list[int] = Field(max_length=3)
    notes_header: str | None = Field(default=None, max_length=70)


@dataclass
class SlideDesignResult:
    deck_plan: dict | None
    used_llm: bool
    fallback_reason: str | None = None
    llm_calls: list[dict] = field(default_factory=list)
    input_tokens: int = 0
    cached_tokens: int = 0
    output_tokens: int = 0
    usd: float = 0.0
    retries: int = 0
    overflow_errors: list[dict] = field(default_factory=list)


def _chua_url_hoac_tu_cam(text: str | None, gio_cho_phep: set[str]) -> str | None:
    if not text:
        return None
    s = str(text)
    if _URL_LA.search(s):
        return "chua_url_la"
    if _GIA_TIEN.search(s):
        return "chua_gia_tien"
    if _GHI_CONG_ANH.search(s):
        return "chua_ghi_cong_anh"
    for m in _GIO_LA.findall(s):
        norm = re.sub(r"\s+", "", m.lower())
        if norm not in gio_cho_phep:
            return "chua_gio_la"
    return None


def hau_kiem_slide_deck(plan: SlideDeckPlan, canonical: dict) -> list[str]:
    """Hậu kiểm chặt `SlideDeckPlan` so với `CanonicalItinerary`. Trả danh sách mã lỗi (rỗng = đạt)."""
    loi: list[str] = []
    if plan.theme_id not in ALLOWED_THEMES:
        loi.append("theme_khong_hop_le")
    if plan.cover_layout not in ALLOWED_LAYOUTS_BY_KIND["cover"]:
        loi.append("cover_layout_khong_hop_le")

    muc_theo_id: dict[str, dict] = {}
    gio_cho_phep: set[str] = set()
    ten_cho_phep: set[str] = set()
    for ng in canonical.get("ngay") or []:
        for m in ng.get("muc") or []:
            if m.get("loai") == "nghi":
                continue
            muc_theo_id[m["id_muc"]] = m
            if m.get("ten"):
                ten_cho_phep.add(str(m["ten"]))
            for src_gio in (m.get("gio"), m.get("cau"), m.get("ghi_chu")):
                if src_gio:
                    for g in _GIO_LA.findall(str(src_gio)):
                        gio_cho_phep.add(re.sub(r"\s+", "", g.lower()))

    manifest_diem = (canonical.get("anh_manifest") or {}).get("diem") or {}
    if plan.hero_image_id is not None and plan.hero_image_id not in manifest_diem:
        loi.append(f"hero_image_la:{plan.hero_image_id}")
    for sid in plan.secondary_image_ids:
        if sid not in manifest_diem:
            loi.append(f"secondary_image_la:{sid}")

    seen_muc: list[str] = []
    for d in plan.days:
        if d.layout_id not in ALLOWED_LAYOUTS_BY_KIND["day"]:
            loi.append(f"day_layout_khong_hop_le:{d.layout_id}")
        for truong in (d.day_header, d.route_summary, d.dining_note):
            err = _chua_url_hoac_tu_cam(truong, gio_cho_phep)
            if err:
                loi.append(f"day_{d.day_number}_{err}")
        for it in d.items:
            if it.id_muc not in muc_theo_id:
                loi.append(f"id_muc_la:{it.id_muc}")
                continue
            seen_muc.append(it.id_muc)
            # Không cho phép đổi tên sang địa danh bịa (nếu có title_override phải trùng tên gốc hoặc tên rút gọn từ tên gốc)
            if it.title_override and it.title_override.strip() != muc_theo_id[it.id_muc]["ten"]:
                loi.append(f"doi_ten_muc:{it.id_muc}")
            err = _chua_url_hoac_tu_cam(it.short_copy, gio_cho_phep)
            if err:
                loi.append(f"{it.id_muc}_{err}")

    if set(seen_muc) != set(muc_theo_id) or len(seen_muc) != len(muc_theo_id):
        loi.append("lech_danh_sach_id_muc")

    for txt in (plan.deck_title, plan.deck_subtitle, plan.lodging_header, plan.notes_header, *plan.highlights):
        err = _chua_url_hoac_tu_cam(txt, gio_cho_phep)
        if err:
            loi.append(f"deck_{err}")

    o_dau = canonical.get("o_dau")
    max_ks = len((o_dau or {}).get("co_so") or [])
    for idx in plan.lodging_indices:
        if idx < 0 or idx >= max_ks:
            loi.append(f"lodging_index_la:{idx}")

    return loi


def _usage_tu_response(resp: Any, model: str, ms: float) -> dict:
    usage = getattr(resp, "usage", None)
    inp = int(getattr(usage, "input_tokens", 0) or 0)
    out = int(getattr(usage, "output_tokens", 0) or 0)
    details = getattr(usage, "input_tokens_details", None)
    cached = int(getattr(details, "cached_tokens", 0) or 0) if details is not None else 0
    cache_write = int(getattr(details, "cache_write_tokens", 0) or 0) if details is not None else 0
    usd = cost_usd(inp, out, cache_write, cached, provider="openai")
    return {
        "model": model,
        "ms": round(ms, 1),
        "input_tokens": inp,
        "cached_tokens": cached,
        "cache_write_tokens": cache_write,
        "output_tokens": out,
        "usd": usd,
    }


def _build_prompt(canonical: dict, theme_hint: str | None, overflow_errors: list[dict] | None = None) -> str:
    payload = {
        "theme_hint": theme_hint or chon_theme_mac_dinh(canonical.get("tham_so")),
        "canonical_itinerary": {
            "tham_so": canonical.get("tham_so"),
            "minh_hieu": canonical.get("minh_hieu"),
            "ngay": [
                {
                    "ngay": ng.get("ngay"),
                    "ngay_thang": ng.get("ngay_thang"),
                    "chang": ng.get("chang"),
                    "muc": [
                        {
                            "id_muc": m.get("id_muc"),
                            "buoi": m.get("buoi"),
                            "loai": m.get("loai"),
                            "id_diem": m.get("id_diem"),
                            "ten": m.get("ten"),
                            "gio": m.get("gio"),
                            "cau": _MA_NGUON.sub("", m.get("cau") or "").strip() or None,
                            "ghi_chu": m.get("ghi_chu"),
                            "co_anh": bool(m.get("anh")),
                        }
                        for m in (ng.get("muc") or [])
                        if m.get("loai") != "nghi"
                    ],
                }
                for ng in (canonical.get("ngay") or [])
            ],
            "an": [
                {
                    "ngay": a.get("ngay"),
                    "bua": a.get("bua"),
                    "gan": a.get("gan"),
                    "quan": [q.get("ten") for q in (a.get("quan") or [])],
                }
                for a in (canonical.get("an") or [])
            ],
            "o_dau": (
                {
                    "ten_khu": canonical["o_dau"].get("ten_khu"),
                    "co_so": [
                        {"index": i, "ten": c.get("ten"), "xep_hang": c.get("xep_hang")}
                        for i, c in enumerate(canonical["o_dau"].get("co_so") or [])
                    ],
                }
                if canonical.get("o_dau")
                else None
            ),
            "anh_manifest": canonical.get("anh_manifest"),
        },
    }
    if overflow_errors:
        payload["overflow_errors"] = overflow_errors
    return json.dumps(payload, ensure_ascii=False)


async def thiet_ke_slide(
    canonical: dict,
    *,
    theme_id: str | None = None,
    cfg: dict | None = None,
    client: AsyncOpenAI | None = None,
    use_llm: bool = True,
) -> SlideDesignResult:
    """Thiết kế `SlideDeckPlan` qua LLM có vòng tự kiểm tràn chữ, fallback êm về code thuần nếu lỗi/tắt LLM."""
    from api.lich_pptx import plan_sang_cac_trang, trang_lich_v2

    cfg = dict(cfg or {})
    model = str(cfg.get("model") or "gpt-6-luna")
    max_retries = max(0, int(cfg.get("max_retries", 1)))
    timeout_s = float(cfg.get("timeout_seconds", 20))
    reasoning_effort = str(cfg.get("reasoning_effort") or "none")
    fallback_code_only = bool(cfg.get("fallback_code_only", True))
    theme_mac_dinh = theme_id if theme_id in ALLOWED_THEMES else chon_theme_mac_dinh(canonical.get("tham_so"))

    def _log_result(res: SlideDesignResult) -> SlideDesignResult:
        layouts = list(
            dict.fromkeys(s.get("layout_id", "") for s in (res.deck_plan or {}).get("slides", []) if s.get("layout_id"))
        )
        logger.info(
            "slide_designer %s",
            json.dumps(
                {
                    "slide_designer": True,
                    "used_llm": res.used_llm,
                    "fallback_reason": res.fallback_reason,
                    "usd": res.usd,
                    "input_tokens": res.input_tokens,
                    "cached_tokens": res.cached_tokens,
                    "output_tokens": res.output_tokens,
                    "retries": res.retries,
                    "layouts": layouts,
                },
                ensure_ascii=False,
            ),
        )
        return res

    def fallback(reason: str, calls: list[dict], retries: int, errs: list[dict]) -> SlideDesignResult:
        deck_code = trang_lich_v2(canonical, theme_id=theme_mac_dinh)
        return _log_result(
            SlideDesignResult(
                deck_plan=deck_code,
                used_llm=False,
                fallback_reason=reason,
                llm_calls=calls,
                input_tokens=sum(c["input_tokens"] for c in calls),
                cached_tokens=sum(c["cached_tokens"] for c in calls),
                output_tokens=sum(c["output_tokens"] for c in calls),
                usd=sum(c["usd"] for c in calls),
                retries=retries,
                overflow_errors=errs,
            )
        )

    if not use_llm:
        return fallback("code_only_mode", [], 0, [])

    owned_client = False
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            if fallback_code_only:
                return fallback("missing_api_key", [], 0, [])
            raise RuntimeError("OPENAI_API_KEY is missing for Slide Designer")
        client = AsyncOpenAI(api_key=api_key, timeout=timeout_s, max_retries=0)
        owned_client = True

    calls: list[dict] = []
    overflow_errors: list[dict] = []
    retries = 0
    try:
        for attempt in range(max_retries + 1):
            prompt = _build_prompt(canonical, theme_mac_dinh, overflow_errors or None)
            t0 = time.perf_counter()
            try:
                resp = await asyncio.wait_for(
                    client.responses.parse(
                        model=model,
                        instructions=SLIDE_DESIGNER_INSTRUCTIONS,
                        input=prompt,
                        text_format=SlideDeckPlan,
                        store=False,
                        prompt_cache_key="hue_slide_designer_v1",
                        reasoning={"effort": reasoning_effort},
                    ),
                    timeout=timeout_s,
                )
            except (asyncio.TimeoutError, TimeoutError, OpenAIError, Exception) as exc:
                if fallback_code_only:
                    return fallback(f"llm_error:{type(exc).__name__}", calls, retries, overflow_errors)
                raise
            ms = (time.perf_counter() - t0) * 1000
            calls.append(_usage_tu_response(resp, model, ms))
            parsed = getattr(resp, "output_parsed", None)
            if parsed is None:
                raw_txt = getattr(resp, "output_text", None)
                if raw_txt:
                    try:
                        parsed = SlideDeckPlan.model_validate_json(raw_txt)
                    except Exception:
                        parsed = None
            if not isinstance(parsed, SlideDeckPlan):
                if attempt < max_retries:
                    retries += 1
                    continue
                return fallback("invalid_structured_output", calls, retries, overflow_errors)

            if theme_id in ALLOWED_THEMES and parsed.theme_id != theme_id:
                parsed = parsed.model_copy(update={"theme_id": theme_id})

            loi_hk = hau_kiem_slide_deck(parsed, canonical)
            if loi_hk:
                if attempt < max_retries:
                    retries += 1
                    overflow_errors = [{"validation_errors": loi_hk}]
                    continue
                return fallback(f"post_validation_failed:{','.join(loi_hk[:3])}", calls, retries, overflow_errors)

            deck = plan_sang_cac_trang(parsed.model_dump(), canonical)
            overflow_errors = kiem_tra_tran_chu(deck["slides"])
            if not overflow_errors or attempt >= max_retries:
                # Kể cả khi còn overflow nhẹ ở lần thử cuối, tầng 3 của `dung_pptx_v2` sẽ co chữ / cắt sạch ở ranh giới từ
                return _log_result(
                    SlideDesignResult(
                        deck_plan=deck,
                        used_llm=True,
                        fallback_reason=None,
                        llm_calls=calls,
                        input_tokens=sum(c["input_tokens"] for c in calls),
                        cached_tokens=sum(c["cached_tokens"] for c in calls),
                        output_tokens=sum(c["output_tokens"] for c in calls),
                        usd=sum(c["usd"] for c in calls),
                        retries=retries,
                        overflow_errors=overflow_errors,
                    )
                )
            retries += 1
        return fallback("max_retries_exhausted", calls, retries, overflow_errors)
    finally:
        if owned_client:
            await client.close()
