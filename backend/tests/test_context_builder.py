from core.schema import RetrievedDocument
from retrieval.context_builder import ContextBuilder


def make_doc(chunk_id, text, title="Bún bò Huế", section="Tóm tắt"):
    return RetrievedDocument(
        id=chunk_id,
        score=1.0,
        text=text,
        metadata={
            "chunk_id": chunk_id,
            "source": "foods/dishes/bun_bo_hue.md",
            "title": title,
            "section": section,
        },
    )


def test_build_returns_labeled_whole_chunks_in_retrieval_order():
    context = ContextBuilder(max_documents=5, max_characters=2000).build(
        [
            make_doc("a", "Nội dung thứ nhất."),
            make_doc("b", "Nội dung thứ hai.", section="Quán nổi tiếng"),
        ]
    )
    assert context == (
        "[Nguồn 1]\n"
        "Tiêu đề: Bún bò Huế\n"
        "Mục: Tóm tắt\n"
        "Nội dung:\n"
        "Nội dung thứ nhất.\n\n"
        "[Nguồn 2]\n"
        "Tiêu đề: Bún bò Huế\n"
        "Mục: Quán nổi tiếng\n"
        "Nội dung:\n"
        "Nội dung thứ hai."
    )
    assert "chunk_id" not in context
    assert "foods/dishes" not in context


def test_build_stops_before_the_first_whole_chunk_that_exceeds_budget():
    first = make_doc("a", "Nội dung thứ nhất.")
    second = make_doc("b", "Nội dung thứ hai.")
    first_context = ContextBuilder(max_characters=2000).build([first])
    context = ContextBuilder(
        max_documents=5,
        max_characters=len(first_context),
    ).build([first, second])
    assert context == first_context
    assert "Nguồn 2" not in context


def test_build_skips_blank_documents_and_returns_empty_string_without_context():
    builder = ContextBuilder()
    assert builder.build([]) == ""
    assert builder.build([make_doc("a", "   ")]) == ""
    context = builder.build(
        [make_doc("a", ""), make_doc("b", "Nội dung hợp lệ.")]
    )
    assert context.startswith("[Nguồn 1]")
    assert "Nội dung hợp lệ." in context
