"""Thí nghiệm Qwen3-Embedding-8B (dense thay e5-small) — harness theo plan C78.

Plan + tiêu chí ghi trước: `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_plan.md` (A duyệt sha `52555da95828`) §4, §6.
Đổi một thứ: dense `e5-small-384` → `qwen3-embedding-8b-4096` (OpenRouter, pin Nebius, `data_collection: deny`). Gọi code production qua
tham số: `build_candidate(..., dense_runner=)`, `g1_retrieval.run_config(..., dense_runner=)`. Logic riêng chỉ ở đây: runner bọc
`OpenRouterDenseRunner` — thử lại có giới hạn (429 / 5xx / timeout), cache từng batch đoạn, ghi log từng request, giữ vector câu hỏi (A/A).
Dữ liệu private: `data/qwen3_8b_2026-10-28/`; kết quả tầng tìm: `data/phase_8_1/g1/<name>.jsonl` như g1.

Chạy từ `backend/`, theo thứ tự plan §6 (B92 chỉ viết code; lệnh có phí chạy sau khi User + A duyệt):
  HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env python -m experiments.phase_8_2.qwen3_8b preflight     # free
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g1_retrieval run --name c78_e5_dev --group dev                 # mốc e5, free
  HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env python -m experiments.phase_8_2.qwen3_8b pilot         # phí rất nhỏ
  HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env python -m experiments.phase_8_2.qwen3_8b build         # phí, ghi Qdrant
  HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env python -m experiments.phase_8_2.qwen3_8b retrieve --group dev --name c78_8b_dev
      (lần hai cùng index cho A/A: --name c78_8b_dev_aa; rồi --group test)
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.qwen3_8b aa --a c78_8b_dev --b c78_8b_dev_aa                  # free
  So với e5: `g1_retrieval compare --a c78_e5_dev --b c78_8b_dev --metrics context5_gold_all top10_gold_all pool_dense_gold_all mrr`
"""
import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

import httpx
import numpy as np

from core.settings_loader import load_settings
from embedding.full_corpus import (
    OPENROUTER_EMBEDDINGS_URL,
    OPENROUTER_PROVIDER_ROUTING,
    OpenRouterDenseRunner,
    parse_embeddings_response,
    prepare_document,
    validate_vector_matrix,
)
from evaluation.full_corpus_eval import REPO_ROOT
from experiments.phase_8_1 import g1_retrieval as g1
from ingestion.full_corpus_pipeline import (
    SPARSE_STATE_PATH,
    build_candidate,
    build_record_path,
    candidate_by_id,
    prepare_full_corpus_input,
)
from vectorstore.qdrant import client_from_settings

CANDIDATE = "qwen3-embedding-8b-4096"
COLLECTION = "hue_c78_qwen3_8b_4096"
RUNTIME_CANDIDATE = "e5-small-384"
OUT_DIR = REPO_ROOT / "data/qwen3_8b_2026-10-28"
CACHE_DIR = OUT_DIR / "emb"
SPARSE_STATE = OUT_DIR / "sparse_state.json"
RECORD = OUT_DIR / "record.json"
RETRY_WAITS_S = (10, 30, 90)  # plan §4: tối đa 3 lần thử lại cho batch đoạn
DOCUMENT_RETRIES = 3
QUERY_RETRIES = 1  # plan §4.2: câu hỏi lỗi ⇒ chạy lại đúng câu đó một lần; lần lỗi vẫn nằm trong log (tỉ lệ lỗi gọi)
PILOT_BATCHES = 2
PILOT_REPEAT = 20
USD_PER_TOKEN = 0.01 / 1_000_000  # qwen/qwen3-embedding-8b trên OpenRouter, WebFetch 28/10 (plan §8)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def retry_wait(attempt: int, status: int | None, retry_after: str | None) -> float | None:
    """Giây chờ trước lần thử thứ `attempt + 1` (plan §4); None = lỗi không thử lại.

    Chỉ thử lại HTTP 429, 5xx và timeout (`status` None). 429 có `Retry-After` dạng số giây ⇒ chờ max(lịch, Retry-After);
    dạng ngày giờ HTTP thì theo lịch.
    """
    if status is not None and status != 429 and status < 500:
        return None
    wait = RETRY_WAITS_S[attempt]
    if status == 429 and retry_after and retry_after.strip().isdigit():
        wait = max(wait, int(retry_after))
    return float(wait)


# ---------- cache batch đoạn ----------
# Chạy lại sau lỗi không trả tiền hai lần (plan §4.1). Khóa = sha của chính các chuỗi gửi đi: kho đổi (vd đợt 2) thì cache cũ
# không khớp ⇒ dừng, không lặng lẽ dùng vector của kho cũ.

def load_cached_batch(cache_dir: Path, number: int, texts: list[str]) -> tuple[np.ndarray, str] | None:
    meta_path = cache_dir / f"batch_{number:03d}.json"
    if not meta_path.is_file():  # meta ghi sau .npy: thiếu meta = batch chưa xong
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta["sha256"] != sha256_text(json.dumps(texts, ensure_ascii=False)) or meta["count"] != len(texts):
        raise ValueError(f"cache batch {number:03d} was built from different texts — stop (corpus changed?)")
    return np.load(cache_dir / f"batch_{number:03d}.npy"), meta["provider"]


def save_cached_batch(cache_dir: Path, number: int, texts: list[str], matrix: np.ndarray, provider: str) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    np.save(cache_dir / f"batch_{number:03d}.npy", matrix)
    meta = {"sha256": sha256_text(json.dumps(texts, ensure_ascii=False)), "count": len(texts), "provider": provider}
    (cache_dir / f"batch_{number:03d}.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")


class LoggedOpenRouterRunner(OpenRouterDenseRunner):
    """`OpenRouterDenseRunner` + thử lại có giới hạn, cache batch đoạn, log từng request (plan §4.1, §3 m-2).

    Giữ nguyên input, batch 64, pin provider, timeout 180 s, kiểm response (`parse_embeddings_response`) của runner production.
    Là lớp con để `build_candidate` vẫn ghi `providers_seen` vào build record.
    """

    def __init__(self, spec, log_path: Path, retries: int, cache_dir: Path | None = None) -> None:
        super().__init__(spec)
        self.log_path, self.retries, self.cache_dir = log_path, retries, cache_dir
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self.label = "query"
        self.attempts: list[dict] = []
        self.query_vectors: list[tuple[str, list[float]]] = []  # (sha câu hỏi, vector) theo thứ tự gọi, gồm câu warm-up
        self._last_provider = ""

    def _post(self, texts: list[str]) -> tuple[int | None, httpx.Response | None, float]:
        started = time.perf_counter()
        try:
            response = self._client.post(OPENROUTER_EMBEDDINGS_URL, json={
                "model": self.spec.model_id,
                "input": list(texts),
                "encoding_format": "float",
                "provider": OPENROUTER_PROVIDER_ROUTING,
            })
        except httpx.TimeoutException:
            return None, None, round((time.perf_counter() - started) * 1000, 1)
        return response.status_code, response, round((time.perf_counter() - started) * 1000, 1)

    def _log(self, row: dict) -> None:
        self.attempts.append(row)
        with self.log_path.open("a", encoding="utf-8") as fh:  # ghi ngay từng dòng: build dừng giữa chừng vẫn còn log
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def _embed(self, texts) -> np.ndarray:
        if self._client is None:
            self.load()
        for attempt in range(self.retries + 1):
            status, response, ms = self._post(texts)
            body = response.json() if status == 200 else {}
            self._log({"label": self.label, "attempt": attempt, "n": len(texts), "status": status, "ms": ms,
                       "provider": body.get("provider"), "id": body.get("id"),
                       "prompt_tokens": (body.get("usage") or {}).get("prompt_tokens"),
                       "error": None if status == 200 else ("timeout" if response is None else response.text[:300]),
                       "at": time.strftime("%Y-%m-%d %H:%M:%S %z")})
            if status == 200:
                matrix, provider = parse_embeddings_response(body, len(texts), self.spec.dimension)
                self.providers_seen.add(provider)
                self._last_provider = provider
                return matrix
            wait = retry_wait(attempt, status, response.headers.get("Retry-After") if response is not None else None) \
                if attempt < self.retries else None
            if wait is None:
                raise RuntimeError(f"OpenRouter {self.label} failed after {attempt + 1} attempt(s): HTTP {status}")
            time.sleep(wait)
        raise AssertionError("unreachable: last attempt either returns or raises")

    def embed_documents_matrix(self, texts) -> np.ndarray:
        if self.cache_dir is None:
            raise ValueError("document embedding needs cache_dir")
        prepared = [prepare_document(self.spec, text) for text in texts]
        size = self.spec.batch_size
        matrices = []
        for number, start in enumerate(range(0, len(prepared), size)):
            batch = prepared[start:start + size]
            cached = load_cached_batch(self.cache_dir, number, batch)
            if cached is None:
                self.label = f"batch_{number:03d}"
                matrix = self._embed(batch)
                save_cached_batch(self.cache_dir, number, batch, matrix, self._last_provider)
            else:
                matrix, provider = cached
                self.providers_seen.add(provider)
            matrices.append(matrix)
        return validate_vector_matrix(np.vstack(matrices), len(texts), self.spec.dimension)

    def embed_documents_uncached(self, texts: list[str], label: str) -> np.ndarray:
        """Pilot: nhúng lại vài đoạn, không qua cache, để so cos với lần đầu (kiểm hiện tượng trộn provider của 7A2)."""
        self.label = label
        return self._embed([prepare_document(self.spec, text) for text in texts])

    def embed_queries(self, queries):
        self.label = "query"
        vectors = super().embed_queries(queries)  # gọi `_embed` đã bọc
        self.query_vectors += [(sha256_text(q), v) for q, v in zip(queries, vectors)]
        return vectors


def _spec():
    return candidate_by_id(CANDIDATE).dense_spec


def _write_new(path: Path, text: str) -> None:
    with path.open("x", encoding="utf-8") as fh:  # từ chối ghi đè kết quả có phí
        fh.write(text)


def _sha12(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


# ---------- lệnh ----------

def preflight() -> dict:
    """Plan §6 bước 1 (free). T1 runtime chạy riêng: `python -m evaluation.full_corpus_eval retrieval --out …` rồi so sha."""
    runtime_record = json.loads(build_record_path(candidate_by_id(RUNTIME_CANDIDATE)).read_text(encoding="utf-8"))
    client = client_from_settings(load_settings(validate_private_paths=False))
    try:
        collections = sorted(c.name for c in client.get_collections().collections)
    finally:
        client.close()
    chunk_count = len(prepare_full_corpus_input().chunks)
    res = {
        "git_head": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "collections": collections,
        "openrouter_key_present": bool(os.environ.get("OPENROUTER_API_KEY")),
        "gold_path": str(g1.GOLD_PATH.relative_to(REPO_ROOT)), "gold_sha12": _sha12(g1.GOLD_PATH),
        "chunk_count": chunk_count, "runtime_record_chunk_count": runtime_record["corpus"]["chunk_count"],
        "runtime_sparse_sha12": _sha12(SPARSE_STATE_PATH), "out_dir_exists": OUT_DIR.exists(),
    }
    res["ok"] = (COLLECTION not in collections and candidate_by_id(RUNTIME_CANDIDATE).collection_name in collections
                 and res["openrouter_key_present"] and chunk_count == res["runtime_record_chunk_count"])
    return res


def pilot() -> dict:
    """Plan §6 bước 3: 2 batch đầu qua runner bọc (vào cache — build dùng lại) + nhúng lại 20 đoạn đầu ⇒ cos ≥ 0,999."""
    spec = _spec()
    texts = [chunk.search_text for chunk in prepare_full_corpus_input().chunks]
    runner = LoggedOpenRouterRunner(spec, CACHE_DIR / "attempts.jsonl", DOCUMENT_RETRIES, CACHE_DIR)
    runner.load()
    try:
        first = runner.embed_documents_matrix(texts[:PILOT_BATCHES * spec.batch_size])
        again = runner.embed_documents_uncached(texts[:PILOT_REPEAT], "pilot_repeat")
    finally:
        runner.close()
    a, b = first[:PILOT_REPEAT].astype(np.float64), again.astype(np.float64)
    cos = (a * b).sum(axis=1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1))
    batch_rows = [r for r in runner.attempts if r["label"].startswith("batch_") and r["status"] == 200]
    tokens = sum(r["prompt_tokens"] or 0 for r in batch_rows)
    est_tokens = round(tokens / sum(r["n"] for r in batch_rows) * len(texts)) if batch_rows else None
    return {
        "chunks": len(texts), "batches_called": len(batch_rows), "batch_ms": [r["ms"] for r in batch_rows],
        "providers_seen": sorted(runner.providers_seen), "pilot_prompt_tokens": tokens,
        "est_corpus_tokens": est_tokens, "est_corpus_usd": round(est_tokens * USD_PER_TOKEN, 6) if est_tokens else None,
        "repeat_cos_min": float(cos.min()), "repeat_cos_mean": float(cos.mean()),
        "attempts_not_200": sum(r["status"] != 200 for r in runner.attempts),
        "usd_this_run": round(sum(r["prompt_tokens"] or 0 for r in runner.attempts) * USD_PER_TOKEN, 7),
    }


def build() -> dict:
    """Plan §6 bước 4: collection riêng + sparse state / record riêng; kiểm sau build (8.426 / 8.426, chỉ Nebius, sparse giống byte)."""
    runner = LoggedOpenRouterRunner(_spec(), CACHE_DIR / "attempts.jsonl", DOCUMENT_RETRIES, CACHE_DIR)
    summary = build_candidate(CANDIDATE, collection_name=COLLECTION, sparse_state_path=SPARSE_STATE, record_path=RECORD,
                              dense_runner=runner)
    summary["checks"] = {
        "providers_only_nebius": summary["providers_seen"] == ["Nebius"],
        "sparse_state_same_bytes_as_runtime": SPARSE_STATE.read_bytes() == SPARSE_STATE_PATH.read_bytes(),
    }
    _write_new(OUT_DIR / "build_summary.json", json.dumps(summary, ensure_ascii=False, indent=1) + "\n")
    return summary


def retrieve(group: str, name: str) -> dict:
    """Plan §6 bước 5: tầng tìm 8B bằng chính `g1_retrieval.run_config` (mặc định g1), runner ghi log + giữ vector câu hỏi."""
    out = g1.OUT_DIR / f"{name}.jsonl"
    log_path = OUT_DIR / f"queries_{name}.jsonl"
    if out.exists() or log_path.exists():
        raise SystemExit(f"{name}: output exists — stop")
    args = g1.build_parser().parse_args([
        "run", "--name", name, "--group", group, "--candidate", CANDIDATE, "--collection", COLLECTION,
        "--record", str(RECORD), "--sparse-state", str(SPARSE_STATE),
    ])
    runner = LoggedOpenRouterRunner(_spec(), log_path, QUERY_RETRIES)
    rows = g1.run_config(args, dense_runner=runner)
    _write_new(out, "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))
    np.save(OUT_DIR / f"queries_{name}.npy", np.asarray([v for _, v in runner.query_vectors], dtype=np.float32))
    _write_new(OUT_DIR / f"queries_{name}.sha.json", json.dumps([s for s, _ in runner.query_vectors]) + "\n")
    return {"rows": len(rows), "requests": len(runner.attempts),
            "not_200": sum(r["status"] != 200 for r in runner.attempts),
            "providers_seen": sorted(runner.providers_seen),
            "usd": round(sum(r["prompt_tokens"] or 0 for r in runner.attempts) * USD_PER_TOKEN, 7),
            "summary": g1.summarize(rows)}


def aa(name_a: str, name_b: str) -> dict:
    """Plan §3 nhiễu A/A 8B (free): hai lượt nhúng câu hỏi trên cùng index ⇒ cos vector, câu đổi top-10 / context đủ fact, ms."""
    def vectors(name):
        shas = json.loads((OUT_DIR / f"queries_{name}.sha.json").read_text(encoding="utf-8"))
        return dict(zip(shas, np.load(OUT_DIR / f"queries_{name}.npy").astype(np.float64)))

    def log(name):
        return [json.loads(line) for line in (OUT_DIR / f"queries_{name}.jsonl").read_text(encoding="utf-8").splitlines()]

    va, vb = vectors(name_a), vectors(name_b)
    common = sorted(set(va) & set(vb))
    cos = np.array([va[s] @ vb[s] / (np.linalg.norm(va[s]) * np.linalg.norm(vb[s])) for s in common])
    ra = {r["case_index"]: r for r in g1._read(name_a)}
    rb = {r["case_index"]: r for r in g1._read(name_b)}
    cases = sorted(set(ra) & set(rb))
    labelled = [i for i in cases if "context5_gold_all" in ra[i] and "context5_gold_all" in rb[i]]
    ms = {n: [r["ms"] for r in log(n) if r["status"] == 200] for n in (name_a, name_b)}
    return {
        "queries_matched": len(common), "cos_min": float(cos.min()), "cos_mean": float(cos.mean()),
        "vectors_identical": int(sum(np.array_equal(va[s], vb[s]) for s in common)),
        "cases": len(cases), "top10_changed": sum(ra[i]["top_chunk_ids"] != rb[i]["top_chunk_ids"] for i in cases),
        "labelled": len(labelled),
        "context_gold_all_changed": sorted(i for i in labelled if ra[i]["context5_gold_all"] != rb[i]["context5_gold_all"]),
        # lượt sau nhanh bất thường + vector giống byte ⇒ có thể trả từ cache ⇒ A/A là cận dưới (plan §3)
        "request_ms_p50": {n: float(np.percentile(v, 50)) for n, v in ms.items()},
        "not_200": {n: sum(r["status"] != 200 for r in log(n)) for n in (name_a, name_b)},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Qwen3-Embedding-8B experiment harness (plan C78)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("preflight")
    commands.add_parser("pilot")
    commands.add_parser("build")
    ret = commands.add_parser("retrieve")
    ret.add_argument("--group", required=True, choices=["dev", "test"])
    ret.add_argument("--name", required=True)
    cmp = commands.add_parser("aa")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True)
    args = parser.parse_args()
    if args.command == "retrieve":
        res = retrieve(args.group, args.name)
    elif args.command == "aa":
        res = aa(args.a, args.b)
    else:
        res = {"preflight": preflight, "pilot": pilot, "build": build}[args.command]()
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
