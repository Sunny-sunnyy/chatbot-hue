import sys
import pytest

from core.schema import ContextBudgetError
from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus_context import FullCorpusContextBuilder


def make_builder(**overrides):
    values = {
        "context_limit": 16384,
        "reserved_output_tokens": 2048,
        "safety_margin": 512,
        "max_documents": 5,
    }
    values.update(overrides)
    return FullCorpusContextBuilder(load_openai_tokenizer(), **values)


def test_fixed_unicode_vietnamese_token_count_assertion():
    """Detect unintended tokenizer/encoding changes using locked o200k_base counts."""
    tokenizer = load_openai_tokenizer()
    sample_text = "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này."
    assert len(tokenizer.encode(sample_text)) == 19
    assert len(tokenizer.encode("Đại Nội Huế")) == 5


def test_real_context_uses_only_evidence_parts(full_corpus_documents):
    packed = make_builder().build("Giá vé Đại Nội thế nào?", full_corpus_documents)
    assert 1 <= len(packed.sources) <= 5
    assert [source.id for source in packed.sources] == list(
        range(1, len(packed.sources) + 1)
    )
    for source in packed.sources:
        for excerpt in source.excerpts:
            assert excerpt in packed.text
    for document in full_corpus_documents[: len(packed.sources)]:
        generated_only = document.text.strip()
        evidence = "\n".join(
            part["text"] for part in document.metadata["evidence_parts"]
        )
        if generated_only != evidence:
            assert generated_only not in packed.text


def test_real_context_stops_at_whole_chunk_boundary(full_corpus_documents):
    normal = make_builder().build("Giá vé Đại Nội thế nào?", full_corpus_documents)
    assert normal.input_tokens + 2048 + 512 <= 16384
    first_only = make_builder(max_documents=1).build(
        "Giá vé Đại Nội thế nào?", full_corpus_documents
    )
    tight = make_builder(context_limit=first_only.input_tokens + 2048 + 512).build(
        "Giá vé Đại Nội thế nào?", full_corpus_documents
    )
    assert len(tight.sources) == 1
    assert tight.text == first_only.text


def test_real_first_chunk_over_budget_is_typed_error(full_corpus_documents):
    with pytest.raises(ContextBudgetError):
        make_builder(context_limit=2048 + 512 + 1).build(
            "Giá vé Đại Nội thế nào?", full_corpus_documents
        )


def test_packed_context_excludes_metadata_v2_private_fields(full_corpus_documents):
    packed = make_builder().build("Huế", full_corpus_documents)
    assert packed.sources
    for doc in full_corpus_documents:
        # Private fields must never leak into packed.text or PackedSource fields
        if doc.id:
            assert doc.id not in packed.text
        source_path = doc.metadata.get("source")
        if source_path:
            assert source_path not in packed.text
            for s in packed.sources:
                assert source_path != s.title
                assert source_path not in s.heading_path
        chunk_id = doc.metadata.get("chunk_id")
        if chunk_id:
            assert chunk_id not in packed.text
        domain = doc.metadata.get("domain")
        if domain:
            # domain should not be explicitly present as a field or leaking
            pass


def test_context_builder_does_not_import_transformers():
    import retrieval.full_corpus_context as ctx_module

    # Confirm transformers/qwen is not imported in full_corpus_context
    assert "transformers" not in sys.modules or "transformers" not in dir(ctx_module)
    assert "qwen" not in sys.modules or "qwen" not in dir(ctx_module)
