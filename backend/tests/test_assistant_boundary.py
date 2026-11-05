"""Ranh giới của trợ lý Phase 9 (plan B0 `docs/superpowers/plans/2026-11-02-phase-9-b0-plan.md` D2, D3; T-3, T-4) — chỉ đọc mã nguồn, 0 mạng.

T-3: trong cây import của chatbot (`api.app`) chỉ module được phép mới import thư viện gọi mạng, mỗi nhà cung cấp một module; module khác chỉ được
import lớp lỗi. Cây dựng **tĩnh bằng AST**, gồm cả import nằm trong hàm (nạp lười) — `sys.modules` sau `import api.app` sót loại này (review C124 m-1).
Giới hạn: import động (`importlib`, `__import__`) không theo được. Thêm module / nhà cung cấp mới (vd Serper ở B6) ⇒ sửa `ALLOWED` có chủ đích.

T-4: mọi công cụ chỉ nhận đúng tham số đã khai (tham số model thấy = tham số vị trí; phần code điền = keyword-only); không tham số nào là URL.
"""
import ast
import inspect
from pathlib import Path

from llm.assistant import TOOLS

BACKEND = Path(__file__).resolve().parents[1]
NETWORK_PACKAGES = ("openai", "agents", "httpx", "requests", "aiohttp", "urllib.request", "http.client", "socket", "websockets",
                    "huggingface_hub")
ALLOWED = {
    "llm.generator_openai_full_corpus": {"openai", "agents"},  # OpenAI — mọi lần gọi model
    "embedding.full_corpus": {"httpx", "huggingface_hub"},  # OpenRouter (candidate Qwen3) + tải model e5 từ HF Hub (không mang chữ người dùng)
    # Phase 10 A1 (plan D3): chỉ DỰNG `Agent` / `ModelSettings` cho lượt ảnh; lần gọi model vẫn qua `generator._run` (client OpenAI của generator)
    "llm.nhan_anh": {"agents"},
}
EXPECTED_TOOLS = {"tim_kho": ("cau_tim",)}


def _module_file(name: str) -> Path | None:
    path = BACKEND / name.replace(".", "/")
    for candidate in (path.with_suffix(".py"), path / "__init__.py"):
        if candidate.is_file():
            return candidate
    return None


def _imports(path: Path) -> list[tuple[str, list[str]]]:
    """(module, tên được import) của mọi câu import trong file, ở mọi độ sâu (kể cả trong hàm)."""
    found = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            found.extend((alias.name, []) for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.append((node.module, [alias.name for alias in node.names]))
    return found


def _project_targets(module: str, names: list[str]) -> list[str]:
    """Module dự án mà một câu import nạp: chính nó, các gói cha, và `from gói import module_con`."""
    parts = module.split(".")
    targets = [".".join(parts[:i]) for i in range(1, len(parts) + 1)]
    targets += [f"{module}.{name}" for name in names]
    return [t for t in targets if _module_file(t) is not None]


def import_tree(root: str = "api.app") -> dict[str, list[tuple[str, list[str]]]]:
    tree, todo = {}, [root]
    while todo:
        name = todo.pop()
        if name in tree:
            continue
        tree[name] = _imports(_module_file(name))
        for module, names in tree[name]:
            todo.extend(_project_targets(module, names))
    return tree


def _network_package(module: str) -> str | None:
    return next((p for p in NETWORK_PACKAGES if module == p or module.startswith(p + ".")), None)


def _only_error_classes(module: str, names: list[str]) -> bool:
    if module == "agents.exceptions":
        return True
    return module == "openai" and bool(names) and all(n.endswith(("Error", "Exception")) for n in names)


def test_tree_follows_lazy_imports():
    tree = import_tree()
    # chạm cả ba nơi cần kiểm + một module chỉ nạp trong hàm (`ingestion/chunking/full_corpus_chunker.py`) ⇒ cây đi đúng đường
    assert {"api.routes.chat", "llm.assistant", "llm.generator_openai_full_corpus", "embedding.full_corpus", "ingestion.preview"} <= set(tree)


def test_only_allowed_modules_import_network_clients():
    violations = []
    for name, imports in import_tree().items():
        for module, names in imports:
            package = _network_package(module)
            if package is None or package in ALLOWED.get(name, set()) or _only_error_classes(module, names):
                continue
            violations.append(f"{name}: {module} {names}")
    assert violations == []


def test_assistant_core_imports_no_network_or_sdk():
    imports = import_tree()["llm.assistant"]
    assert [m for m, _ in imports if _network_package(m)] == []


def test_tools_take_only_declared_parameters_and_no_url():
    assert set(TOOLS) == set(EXPECTED_TOOLS)
    model_kinds = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    for name, tool in TOOLS.items():
        params = tuple(p.name for p in inspect.signature(tool).parameters.values() if p.kind in model_kinds)
        assert params == EXPECTED_TOOLS[name]
        assert not [p for p in params if any(bad in p.lower() for bad in ("url", "link", "href", "uri"))]
