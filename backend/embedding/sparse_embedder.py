"""Deterministic TF-IDF-style sparse embedder for lexical signal."""
import math
import re

_NON_WORD = re.compile(r"[^\w\s]")


def tokenize(text):
    """Lowercase, replace non-word/non-space chars with spaces, then split."""
    return _NON_WORD.sub(" ", text.lower()).split()


class SparseEmbedder:
    """Maps tokens to stable vocabulary indices with TF-IDF values.

    fit() builds the vocabulary and document frequencies from a corpus and
    must be called before encode(). Calling fit() again resets all state
    instead of accumulating silently.
    """

    def __init__(self):
        self.num_documents = 0
        self._vocab = {}
        self._document_frequency = {}

    @property
    def vocabulary_size(self):
        """Number of unique tokens in the fitted vocabulary."""
        return len(self._vocab)

    def fit(self, texts):
        """Reset state and fit vocabulary/DF from texts in given order."""
        self.num_documents = 0
        self._vocab = {}
        self._document_frequency = {}
        for text in texts:
            # dict.fromkeys deduplicates tokens while keeping first-occurrence
            # order, so a token increments DF once per document and indices
            # stay deterministic across identical corpora.
            for token in dict.fromkeys(tokenize(text)):
                if token not in self._vocab:
                    self._vocab[token] = len(self._vocab)
                self._document_frequency[token] = (
                    self._document_frequency.get(token, 0) + 1
                )
            self.num_documents += 1
        return self

    def encode(self, text):
        """Return {"indices": [...], "values": [...]} for one text."""
        if not self._vocab:
            raise ValueError("SparseEmbedder must be fit before encode")
        counts = {}
        for token in tokenize(text):
            if token in self._vocab:
                counts[token] = counts.get(token, 0) + 1
        indices = []
        values = []
        for token, term_frequency in counts.items():
            df = self._document_frequency[token]
            idf = math.log((self.num_documents + 1) / (df + 1)) + 1
            indices.append(self._vocab[token])
            values.append(term_frequency * idf)
        return {"indices": indices, "values": values}
