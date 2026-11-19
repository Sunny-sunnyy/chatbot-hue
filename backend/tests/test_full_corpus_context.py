from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus_context import FullCorpusContextBuilder


def make_builder(**overrides):
    values = {"max_documents": 5}
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


def test_real_context_takes_every_document_up_to_the_count_cap_whatever_the_size(full_corpus_documents):
    """User 19/11/2026: không còn ngân sách token của ngữ cảnh — rào duy nhất là SỐ đoạn. Ngữ cảnh đã có sẵn dù dài bao nhiêu (ở đây ~60 nghìn chữ
    — vượt xa ngân sách 16.384 token cũ) thì lần dựng kế vẫn nhận đủ các đoạn nguyên vẹn; đoạn đã có (`skip_ids`) bị bỏ, đánh số nối tiếp."""
    co_san = "x " * 60000
    packed = make_builder(max_documents=3).build("Giá vé Đại Nội thế nào?", full_corpus_documents, prior_context=co_san, first_id=4,
                                                 skip_ids=frozenset({full_corpus_documents[0].id}))
    assert len(packed.sources) == 3 and [s.id for s in packed.sources] == [4, 5, 6]
    assert full_corpus_documents[0].id not in packed.document_ids
    assert packed.input_tokens > 16384
    mot = make_builder(max_documents=1).build("Giá vé Đại Nội thế nào?", full_corpus_documents)
    assert len(mot.sources) == 1 and mot.text in make_builder().build("Giá vé Đại Nội thế nào?", full_corpus_documents).text


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
