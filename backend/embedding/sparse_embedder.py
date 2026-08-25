"""Deterministic TF-IDF sparse representation for lexical signals."""
import math
import re
from collections import Counter

NON_WORD = re.compile(r"[^\w\s]")


def tokenize(text: str) -> list[str]:
    """Lowercase text, replace punctuation with spaces and split tokens."""
    return NON_WORD.sub(" ", text.lower()).split()


class SparseEmbedder:
    """Build an ordered vocabulary and encode texts with TF-IDF values."""

    def __init__(self):
        self.num_documents = 0
        self._vocabulary: dict[str, int] = {}
        self._document_frequency: dict[str, int] = {}

    @property
    def vocabulary_size(self) -> int:
        """Return the number of tokens learned by the latest fit."""
        return len(self._vocabulary)

    def fit(self, texts: list[str]) -> "SparseEmbedder":
        """Reset state and learn vocabulary/DF in corpus order."""
        self.num_documents = 0
        self._vocabulary = {}
        self._document_frequency = {}
        for text in texts:
            # dict.fromkeys keeps first occurrence while counting each token's
            # document frequency only once for this document.
            for token in dict.fromkeys(tokenize(text)):
                if token not in self._vocabulary:
                    self._vocabulary[token] = len(self._vocabulary)
                self._document_frequency[token] = (
                    self._document_frequency.get(token, 0) + 1
                )
            self.num_documents += 1
        return self

    def encode(self, text: str) -> dict[str, list]:
        """Encode one text as aligned vocabulary indices and TF-IDF values."""
        if not self._vocabulary:
            raise ValueError("SparseEmbedder must be fit before encode")
        term_frequencies = Counter(
            token for token in tokenize(text) if token in self._vocabulary
        )
        indices: list[int] = []
        values: list[float] = []
        for token, term_frequency in term_frequencies.items():
            document_frequency = self._document_frequency[token]
            inverse_document_frequency = math.log(
                (self.num_documents + 1) / (document_frequency + 1)
            ) + 1
            indices.append(self._vocabulary[token])
            values.append(float(term_frequency * inverse_document_frequency))
        return {"indices": indices, "values": values}
