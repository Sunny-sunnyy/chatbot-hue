"""Build bounded labeled context from retrieved whole chunks."""


class ContextBuilder:
    def __init__(self, max_documents=5, max_characters=3000):
        self._max_documents = max_documents
        self._max_characters = max_characters

    def build(self, documents):
        """Return labeled context in retrieval order without truncating chunks."""
        blocks = []
        for document in documents:
            if len(blocks) >= self._max_documents:
                break
            text = document.text.strip()
            if not text:
                continue
            metadata = document.metadata
            number = len(blocks) + 1
            block = (
                f"[Nguồn {number}]\n"
                f"Tiêu đề: {metadata.get('title') or ''}\n"
                f"Mục: {metadata.get('section') or ''}\n"
                f"Nội dung:\n{text}"
            )
            candidate = "\n\n".join([*blocks, block])
            if len(candidate) > self._max_characters:
                break
            blocks.append(block)
        return "\n\n".join(blocks)
