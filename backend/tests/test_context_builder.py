"""Tests for whole-chunk bounded context and source mapping."""
import copy

from core.schema import RetrievedDocument
from retrieval.context_builder import ContextBuilder

SOURCE = "foods/restaurants/doc.md"
LABEL = f"[{SOURCE} | Tóm tắt]"
SEPARATOR = "\n\n"
BLOCK_40 = len(LABEL) + 1 + 40  # label + newline + 40-char text


def make_doc(chunk_id, text):
    return RetrievedDocument(
        id=chunk_id,
        score=1.0,
        text=text,
        metadata={
            "chunk_id": chunk_id,
            "source": SOURCE,
            "title": "Doc",
            "section": "Tóm tắt",
            "category": "foods",
            "subcategory": "restaurants",
            "chunk_type": "section",
        },
    )


def test_budget_counts_label_and_separator():
    builder = ContextBuilder(max_documents=5, max_characters=BLOCK_40 + 2)
    first = "a" * 40
    second = "b" * 40
    block = f"{LABEL}\n{first}"
    result = builder.build([make_doc("a", first), make_doc("b", second)])
    # first block fits exactly; the separator + second block would overflow
    assert result.context == block
    assert len(result.context) == BLOCK_40
    assert len(result.sources) == 1


def test_second_whole_chunk_fits_when_budget_allows():
    builder = ContextBuilder(max_documents=5, max_characters=2 * BLOCK_40 + 2)
    first = "a" * 40
    second = "b" * 40
    result = builder.build([make_doc("a", first), make_doc("b", second)])
    expected = f"{LABEL}\n{first}{SEPARATOR}{LABEL}\n{second}"
    assert result.context == expected
    assert len(result.context) == 2 * BLOCK_40 + len(SEPARATOR)
    assert len(result.sources) == 2


def test_stops_before_chunk_that_does_not_fit_without_truncation():
    builder = ContextBuilder(max_documents=5, max_characters=3000)
    long_text = "b" * 2900
    result = builder.build([make_doc("a", long_text), make_doc("b", "x" * 100)])
    assert result.context == f"{LABEL}\n{long_text}"
    assert len(result.context) == len(LABEL) + 1 + 2900
    assert result.context.endswith(long_text)
    assert len(result.sources) == 1


def test_max_documents_caps_output():
    builder = ContextBuilder(max_documents=5, max_characters=10000)
    documents = [make_doc(f"d{i}", f"text {i}") for i in range(10)]
    result = builder.build(documents)
    assert len(result.sources) == 5
    assert result.context.count(SEPARATOR) == 4


def test_empty_input_returns_empty_context_and_sources():
    builder = ContextBuilder()
    result = builder.build([])
    assert result.context == ""
    assert result.sources == []


def test_empty_text_documents_are_skipped_keeping_rank():
    builder = ContextBuilder(max_documents=5, max_characters=1000)
    result = builder.build([make_doc("a", ""), make_doc("b", "nội dung"), make_doc("c", "  ")])
    assert len(result.sources) == 1
    assert result.sources[0]["chunk_id"] == "b"
    assert result.sources[0]["rank"] == 2


def test_source_mapping_fields_and_order():
    builder = ContextBuilder(max_documents=5, max_characters=1000)
    result = builder.build([make_doc("a", "nội dung a"), make_doc("b", "nội dung b")])
    assert result.sources == [
        {
            "chunk_id": "a",
            "source": SOURCE,
            "title": "Doc",
            "section": "Tóm tắt",
            "rank": 1,
        },
        {
            "chunk_id": "b",
            "source": SOURCE,
            "title": "Doc",
            "section": "Tóm tắt",
            "rank": 2,
        },
    ]


def test_build_does_not_mutate_documents():
    builder = ContextBuilder(max_documents=5, max_characters=1000)
    documents = [make_doc("a", "nội dung a"), make_doc("b", "nội dung b")]
    snapshot = copy.deepcopy(
        [(doc.score, doc.text, dict(doc.metadata)) for doc in documents]
    )
    builder.build(documents)
    after = [(doc.score, doc.text, dict(doc.metadata)) for doc in documents]
    assert after == snapshot
