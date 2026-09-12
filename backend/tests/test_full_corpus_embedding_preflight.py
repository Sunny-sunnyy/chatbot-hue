"""Deterministic tests for full-corpus embedding sample selection, CUDA inspection, and evidence orchestration."""

import json
from pathlib import Path
import random
import pytest

from backend.core.schema import EvidencePart, FullCorpusChunk
from backend.evaluation.full_corpus_embedding_preflight import (
    P7_ORDER,
    classify_chunk,
    derive_status,
    inspect_cuda,
    partition_for_source,
    select_dense_sample,
    validate_evidence_redaction,
    validate_phase_2_identity,
    validate_phase_2_tokenizer_maxima,
)


def make_chunk_with_parts(
    chunk_id: str,
    source: str,
    evidence_parts: list[EvidencePart],
    search_text: str = "Nội dung tìm kiếm",
) -> FullCorpusChunk:
    return FullCorpusChunk(
        chunk_id=chunk_id,
        source=source,
        title="Tiêu đề mẫu",
        heading_path=["Mục 1"],
        evidence_parts=evidence_parts,
        search_text=search_text,
    )


def test_p7_order_is_exact() -> None:
    assert P7_ORDER == (
        "foods",
        "heritages",
        "festivals",
        "performing_arts",
        "travel_places",
        "travel_services",
        "travel_tickets",
    )


def test_partition_for_source() -> None:
    assert partition_for_source("foods/bun_bo.md") == "foods"
    assert partition_for_source("knowledge-base-hue/heritages/dai_noi.md") == "heritages"
    assert partition_for_source("festivals/festival_hue.md") == "festivals"
    assert partition_for_source("performing_arts/ca_hue.md") == "performing_arts"
    assert partition_for_source("travel/places/chua_thien_mu.md") == "travel_places"
    assert partition_for_source("travel/services/thue_xe.md") == "travel_services"
    assert partition_for_source("travel/tickets/ve_tham_quan.md") == "travel_tickets"


def test_classify_chunk_tags() -> None:
    # 1. Paragraph: chỉ có body không có table hay list
    p_chunk = make_chunk_with_parts(
        "c_p",
        "foods/a.md",
        [EvidencePart(role="body", start=0, end=15, text="Đoạn văn thông thường.")],
        "Đoạn văn thông thường.",
    )
    assert classify_chunk(p_chunk) == frozenset({"paragraph"})

    # 2. List: body chứa markdown list
    l_chunk = make_chunk_with_parts(
        "c_l",
        "foods/b.md",
        [EvidencePart(role="body", start=0, end=30, text="- Mục 1\n- Mục 2\n- Mục 3")],
        "- Mục 1\n- Mục 2\n- Mục 3",
    )
    assert "list" in classify_chunk(l_chunk)

    # 3. Table: chứa header part
    t_chunk = make_chunk_with_parts(
        "c_t",
        "foods/c.md",
        [
            EvidencePart(role="header", start=0, end=10, text="| Cột 1 | Cột 2 |"),
            EvidencePart(role="body", start=11, end=25, text="| Giá trị 1 | Giá trị 2 |"),
        ],
    )
    assert "table" in classify_chunk(t_chunk)

    # 4. Condition: chứa condition part
    c_chunk = make_chunk_with_parts(
        "c_c",
        "foods/d.md",
        [
            EvidencePart(role="condition", start=0, end=12, text="Lưu ý điều kiện."),
            EvidencePart(role="body", start=13, end=25, text="Nội dung chính."),
        ],
    )
    assert "condition" in classify_chunk(c_chunk)


def test_select_dense_sample_determinism_and_coverage() -> None:
    # Tạo corpus giả lập phủ 7 P7 và 4 content tags
    chunks: list[FullCorpusChunk] = []

    # 7 chunks cho 7 P7 (paragraph)
    p7_sources = [
        "foods/food.md",
        "heritages/heritage.md",
        "festivals/fest.md",
        "performing_arts/art.md",
        "travel/places/place.md",
        "travel/services/service.md",
        "travel/tickets/ticket.md",
    ]
    for i, src in enumerate(p7_sources):
        chunks.append(
            make_chunk_with_parts(
                f"chunk_p7_{i:02d}",
                src,
                [EvidencePart(role="body", start=0, end=10, text="Đoạn văn bình thường.")],
            )
        )

    # Thêm chunk chứa list, table, condition
    chunks.append(
        make_chunk_with_parts(
            "chunk_tag_list",
            "foods/list.md",
            [EvidencePart(role="body", start=0, end=20, text="* Điểm 1\n* Điểm 2")],
        )
    )
    chunks.append(
        make_chunk_with_parts(
            "chunk_tag_table",
            "travel/places/table.md",
            [EvidencePart(role="header", start=0, end=10, text="| H1 | H2 |")],
        )
    )
    chunks.append(
        make_chunk_with_parts(
            "chunk_tag_condition",
            "travel/tickets/cond.md",
            [EvidencePart(role="condition", start=0, end=10, text="Điều kiện áp dụng.")],
        )
    )

    # Thêm 2 chunks đại diện cho longest_by_model
    chunks.append(
        make_chunk_with_parts(
            "chunk_longest_e5",
            "heritages/long1.md",
            [EvidencePart(role="body", start=0, end=10, text="Dài nhất e5.")],
        )
    )
    chunks.append(
        make_chunk_with_parts(
            "chunk_longest_qwen",
            "festivals/long2.md",
            [EvidencePart(role="body", start=0, end=10, text="Dài nhất qwen.")],
        )
    )

    longest_map = {
        "e5-small-384": "chunk_longest_e5",
        "qwen3-embedding-0.6b-1024": "chunk_longest_qwen",
    }

    # Chọn mẫu lần 1
    sample1 = select_dense_sample(chunks, longest_map, minimum=10, maximum=15)
    sample_ids1 = [c.chunk_id for c in sample1]

    # Xáo trộn chunks và chọn mẫu lần 2 -> phải ra cùng thứ tự IDs
    shuffled_chunks = list(chunks)
    random.seed(42)
    random.shuffle(shuffled_chunks)
    sample2 = select_dense_sample(shuffled_chunks, longest_map, minimum=10, maximum=15)
    sample_ids2 = [c.chunk_id for c in sample2]

    assert sample_ids1 == sample_ids2
    assert 10 <= len(sample1) <= 15

    # Kiểm tra tính bao phủ đầy đủ: 7 P7
    sample_partitions = {partition_for_source(c.source) for c in sample1}
    assert sample_partitions == set(P7_ORDER)

    # Kiểm tra tính bao phủ: 4 tags
    all_tags = set().union(*(classify_chunk(c) for c in sample1))
    assert {"paragraph", "list", "table", "condition"}.issubset(all_tags)

    # Kiểm tra longest chunks có mặt
    assert "chunk_longest_e5" in sample_ids1
    assert "chunk_longest_qwen" in sample_ids1


def test_derive_status_rules() -> None:
    # 1. Phase 2 bị lỗi
    assert (
        derive_status(
            {
                "phase_2": "FAILED",
                "gpu": "PASS",
                "tokenizers": "PASS",
                "qwen": "PASS",
                "cpu_models": "PASS",
            }
        )
        == "BLOCKED_PHASE_2"
    )

    # 2. GPU không khả dụng
    assert (
        derive_status(
            {
                "phase_2": "PASS",
                "gpu": "UNAVAILABLE",
                "tokenizers": "PASS",
                "qwen": "PASS",
                "cpu_models": "PASS",
            }
        )
        == "BLOCKED_GPU"
    )

    # 3. Tokenizer vượt giới hạn
    assert (
        derive_status(
            {
                "phase_2": "PASS",
                "gpu": "PASS",
                "tokenizers": "OVER_LIMIT",
                "qwen": "PASS",
                "cpu_models": "PASS",
            }
        )
        == "BLOCKED_TOKEN_LIMIT"
    )

    # 4. Qwen OOM hoặc sai thiết bị
    assert (
        derive_status(
            {
                "phase_2": "PASS",
                "gpu": "PASS",
                "tokenizers": "PASS",
                "qwen": "OOM",
                "cpu_models": "PASS",
            }
        )
        == "BLOCKED_QWEN"
    )

    # 5. Model CPU gặp lỗi
    assert (
        derive_status(
            {
                "phase_2": "PASS",
                "gpu": "PASS",
                "tokenizers": "PASS",
                "qwen": "PASS",
                "cpu_models": "FAILED",
            }
        )
        == "FAILED_MODEL"
    )

    # 6. Mọi điều kiện thỏa mãn
    assert (
        derive_status(
            {
                "phase_2": "PASS",
                "gpu": "PASS",
                "tokenizers": "PASS",
                "qwen": "PASS",
                "cpu_models": "PASS",
                "sparse": "PASS",
            }
        )
        == "PASS"
    )

    # 7. Snapshot download / resolution failure (không gán nhầm thành BLOCKED_PHASE_2)
    assert derive_status({"qwen": "BLOCKED_QWEN"}) == "BLOCKED_QWEN"
    assert derive_status({"cpu_models": "FAILED_MODEL"}) == "FAILED_MODEL"
    assert derive_status({"sparse": "FAILED_SPARSE"}) == "FAILED_SPARSE"


def test_validate_phase_2_identity_rules() -> None:
    valid_artifact = {
        "status": "PASS",
        "summary": {
            "total_files": 2,
            "total_chunks": 5,
            "condition_rules_count": 3,
        },
        "sources": ["foods/a.md", "heritages/b.md"],
    }
    valid_sources = ["foods/a.md", "heritages/b.md"]

    # 1. Thành công với đầu vào khớp chính xác
    validate_phase_2_identity(valid_artifact, valid_sources, total_chunks=5, condition_rules_count=3)

    # 2. Status không phải PASS
    with pytest.raises(ValueError, match="Phase 2 artifact status is not PASS"):
        validate_phase_2_identity({**valid_artifact, "status": "FAILED"}, valid_sources, 5, 3)

    # 3. Số file không khớp
    with pytest.raises(ValueError, match="Discovered file count mismatch"):
        validate_phase_2_identity(valid_artifact, ["foods/a.md"], 5, 3)

    # 4. Thứ tự hoặc danh sách file không khớp chính xác
    with pytest.raises(ValueError, match="Discovered sources list does not match exact ordered Phase 2 sources list"):
        validate_phase_2_identity(valid_artifact, ["heritages/b.md", "foods/a.md"], 5, 3)

    # 5. Số chunks không khớp
    with pytest.raises(ValueError, match="Chunk count mismatch"):
        validate_phase_2_identity(valid_artifact, valid_sources, total_chunks=6, condition_rules_count=3)

    # 6. Số condition rules không khớp
    with pytest.raises(ValueError, match="Condition rules count mismatch"):
        validate_phase_2_identity(valid_artifact, valid_sources, total_chunks=5, condition_rules_count=4)


def test_validate_phase_2_tokenizer_maxima_rules() -> None:
    valid_artifact = {
        "tokenizer_limits": {
            "intfloat/multilingual-e5-small": {"max_observed_tokens": 366},
            "intfloat/multilingual-e5-base": {"max_observed_tokens": 366},
            "CODE4LIFEOFFICIAL/huydang-dek21-embedding": {"max_observed_tokens": 255},
        }
    }
    valid_maxima = {
        "e5-small-384": 366,
        "e5-base-768": 366,
        "huydang-dek21-768": 255,
    }

    # 1. Thành công khi khớp chính xác 3 maxima
    validate_phase_2_tokenizer_maxima(valid_artifact, valid_maxima)

    # 2. Sai lệch e5-small
    with pytest.raises(ValueError, match="Tokenizer maximum mismatch for e5-small-384"):
        validate_phase_2_tokenizer_maxima(valid_artifact, {**valid_maxima, "e5-small-384": 367})

    # 3. Sai lệch e5-base
    with pytest.raises(ValueError, match="Tokenizer maximum mismatch for e5-base-768"):
        validate_phase_2_tokenizer_maxima(valid_artifact, {**valid_maxima, "e5-base-768": 365})

    # 4. Sai lệch huydang
    with pytest.raises(ValueError, match="Tokenizer maximum mismatch for huydang-dek21-768"):
        validate_phase_2_tokenizer_maxima(valid_artifact, {**valid_maxima, "huydang-dek21-768": 256})

    # 5. Thiếu mô hình trong observed_maxima
    with pytest.raises(ValueError, match="Missing observed tokenizer maximum for huydang-dek21-768"):
        validate_phase_2_tokenizer_maxima(valid_artifact, {"e5-small-384": 366, "e5-base-768": 366})



def test_validate_evidence_redaction() -> None:
    # Hợp lệ: chỉ chứa metadata định lượng, không có text hay secrets
    valid_evidence = {
        "schema_version": "phase_3_preflight_evidence:v1",
        "status": "PASS",
        "corpus": {"total_files": 205, "total_chunks": 8460},
        "sample": [
            {
                "chunk_id": "c1",
                "source": "foods/a.md",
                "heading_path": ["Mục 1"],
                "tags": ["paragraph"],
                "tokens": {"e5-small-384": 120},
            }
        ],
        "models": {
            "e5-small-384": {"dimension": 384, "norm_min": 0.999, "norm_max": 1.001}
        },
    }
    # Không raise exception
    validate_evidence_redaction(valid_evidence)

    # Không hợp lệ nếu lộ trường vectors
    with pytest.raises(ValueError, match="Forbidden key 'vectors'"):
        validate_evidence_redaction({**valid_evidence, "vectors": [[0.1, 0.2]]})

    # Không hợp lệ nếu lộ search_text
    with pytest.raises(ValueError, match="Forbidden key 'search_text'"):
        validate_evidence_redaction({**valid_evidence, "search_text": "văn bản"})

    # Không hợp lệ nếu chứa authorization header hoặc khóa API
    with pytest.raises(ValueError, match="Forbidden content pattern"):
        validate_evidence_redaction(
            {**valid_evidence, "leak": "Bearer sk-1234567890abcdef"}
        )

    # Không hợp lệ nếu chứa absolute home cache path
    with pytest.raises(ValueError, match="Forbidden content pattern"):
        validate_evidence_redaction(
            {**valid_evidence, "cache_dir": "/home/minhhieu/.cache/huggingface"}
        )


def test_inspect_cuda_fields() -> None:
    cuda_info = inspect_cuda()
    assert "torch_version" in cuda_info
    assert "torch_cuda_version" in cuda_info
    assert "cuda_available" in cuda_info
    assert "device_count" in cuda_info


def test_canonical_notebook_hygiene() -> None:
    nb_path = Path("notebooks/03_embedding_models.ipynb")
    assert nb_path.is_file()
    nb_data = json.loads(nb_path.read_text(encoding="utf-8"))

    code_cells = [c for c in nb_data.get("cells", []) if c.get("cell_type") == "code"]
    assert len(code_cells) >= 4

    for cell in code_cells:
        assert cell.get("execution_count") is None
        assert cell.get("outputs") == []
        src = "".join(cell.get("source", []))
        assert "chunk_foods_markdown" not in src
        assert "E5Embedder" not in src
        assert "QdrantClient" not in src
        assert "OpenRouter" not in src
        assert "vector_dump" not in src

    all_source = "".join("".join(c.get("source", [])) for c in code_cells)
    assert "backend.embedding.full_corpus" in all_source
    assert "backend.embedding.sparse" in all_source
    assert "backend.evaluation.full_corpus_embedding_preflight" in all_source

