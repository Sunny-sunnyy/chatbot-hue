import pytest

from core.schema import CitationIntegrityError
from llm.citations import normalize_citations, select_cited_sources
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus_context import FullCorpusContextBuilder


def packed_sources(full_corpus_documents):
    return FullCorpusContextBuilder(load_openai_tokenizer()).build(
        "Giá vé Đại Nội thế nào?", full_corpus_documents
    ).sources


def test_citations_select_only_referenced_real_sources(full_corpus_documents):
    sources = packed_sources(full_corpus_documents)
    answer = "Thông tin được nêu trong nguồn thứ nhất [1]."
    selected = select_cited_sources(answer, sources)
    assert [source.id for source in selected] == [1]


def test_repeated_citation_produces_one_source(full_corpus_documents):
    sources = packed_sources(full_corpus_documents)
    selected = select_cited_sources("Ý thứ nhất [1]. Ý thứ hai [1].", sources)
    assert [source.id for source in selected] == [1]


@pytest.mark.parametrize("answer", ["Không có marker.", "Marker sai [99]."])
def test_invalid_citation_is_rejected(answer, full_corpus_documents):
    with pytest.raises(CitationIntegrityError):
        select_cited_sources(answer, packed_sources(full_corpus_documents))


def test_exact_fallback_is_the_only_zero_source_answer(full_corpus_documents):
    sources = packed_sources(full_corpus_documents)
    assert select_cited_sources(INSUFFICIENT_ANSWER, sources) == ()
    with pytest.raises(CitationIntegrityError):
        select_cited_sources(f"{INSUFFICIENT_ANSWER} [1]", sources)


@pytest.mark.parametrize(
    "answer, expected_ids",
    [
        ("Thông tin từ nguồn hai [Nguồn 2].", [2]),
        ("Ý thứ nhất [1]. Ý thứ hai [Nguồn 2].", [1, 2]),
        ("Viết thường [nguồn 1], viết hoa [ NGUỒN  2 ].", [1, 2]),
    ],
)
def test_nguon_label_citation_is_accepted(answer, expected_ids, full_corpus_documents):
    # Context gắn nhãn "[Nguồn n]" nên model có lúc trích theo dạng đó (C-09).
    selected = select_cited_sources(answer, packed_sources(full_corpus_documents))
    assert [source.id for source in selected] == expected_ids


def test_nguon_label_keeps_unknown_and_fallback_rules(full_corpus_documents):
    sources = packed_sources(full_corpus_documents)
    with pytest.raises(CitationIntegrityError):
        select_cited_sources("Marker sai [Nguồn 99].", sources)
    with pytest.raises(CitationIntegrityError):
        select_cited_sources(f"{INSUFFICIENT_ANSWER} [Nguồn 1]", sources)


def test_normalize_citations_rewrites_only_citation_markers():
    assert normalize_citations("Ý một [Nguồn 2], ý hai [1], ý ba [ nguồn 3 ].") == "Ý một [2], ý hai [1], ý ba [3]."
    assert normalize_citations("Nguồn tham khảo [Nguồn] không có số.") == "Nguồn tham khảo [Nguồn] không có số."
    assert normalize_citations(INSUFFICIENT_ANSWER) == INSUFFICIENT_ANSWER
