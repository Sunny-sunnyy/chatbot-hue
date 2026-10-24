"""Corpus-scoped BM25 lexical scoring (tokenizer, k1/b dùng cho sparse state full-corpus)."""
import math
import re
from collections import Counter

TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)


def tokenize(text: str) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return TOKEN_PATTERN.findall(text.lower())


K1 = 1.5
B = 0.75


class BM25:
    """BM25 scorer fit once on a corpus; scores exact lexical matches.

    k1 and b follow the approved baseline. Query tokens are deduplicated and
    out-of-vocabulary terms contribute 0.0. Only non-empty documents count
    toward the corpus statistics.
    """

    def __init__(self, k1=K1, b=B):
        self.k1 = k1
        self.b = b
        self._num_documents = 0
        self._average_document_length = 0.0
        self._document_frequency = {}
        self._idf = {}

    @property
    def average_document_length(self):
        """Mean token count of the fitted non-empty documents."""
        return self._average_document_length

    @property
    def num_documents(self):
        """Number of non-empty documents in the fitted corpus."""
        return self._num_documents

    def fit(self, texts):
        """Reset state and fit corpus statistics from non-empty documents."""
        self._num_documents = 0
        self._average_document_length = 0.0
        self._document_frequency = {}
        self._idf = {}
        lengths = []
        for text in texts:
            tokens = tokenize(text)
            if not tokens:
                continue
            lengths.append(len(tokens))
            for term in dict.fromkeys(tokens):
                self._document_frequency[term] = (
                    self._document_frequency.get(term, 0) + 1
                )
            self._num_documents += 1
        if not lengths:
            raise ValueError("BM25 requires at least one non-empty document")
        self._average_document_length = sum(lengths) / len(lengths)
        for term, document_frequency in self._document_frequency.items():
            self._idf[term] = math.log(
                (self._num_documents - document_frequency + 0.5)
                / (document_frequency + 0.5)
                + 1.0
            )
        return self

    def score(self, query, document):
        """Return the BM25 score of one document for a query."""
        if not self._idf:
            raise ValueError("BM25 must be fit before score")
        term_frequencies = Counter(tokenize(document))
        document_length = sum(term_frequencies.values())
        total = 0.0
        for term in dict.fromkeys(tokenize(query)):
            idf = self._idf.get(term)
            term_frequency = term_frequencies.get(term, 0)
            if idf is None or term_frequency == 0:
                continue
            denominator = term_frequency + self.k1 * (
                1.0 - self.b
                + self.b * document_length / self._average_document_length
            )
            total += idf * (term_frequency * (self.k1 + 1.0)) / denominator
        return float(total)
