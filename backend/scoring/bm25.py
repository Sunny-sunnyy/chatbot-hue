"""Corpus-scoped BM25 lexical scoring and min-max normalization utilities."""
import math
from collections import Counter

from embedding.sparse_embedder import tokenize

K1 = 1.5
B = 0.75


def min_max_normalize(scores):
    """Min-max normalize scores to [0, 1]; constant signal maps to 0.0."""
    for score in scores:
        if not math.isfinite(score):
            raise ValueError("cannot normalize a non-finite score")
    if not scores:
        return []
    low = min(scores)
    high = max(scores)
    if high == low:
        return [0.0 for _ in scores]
    span = high - low
    return [(score - low) / span for score in scores]


def validate_weights(dense_weight, bm25_weight, tolerance=1e-9):
    """Return the weight pair or raise when finite/non-negative/sum-1 fails."""
    if not (math.isfinite(dense_weight) and math.isfinite(bm25_weight)):
        raise ValueError("fusion weights must be finite")
    if dense_weight < 0.0 or bm25_weight < 0.0:
        raise ValueError("fusion weights must be non-negative")
    if abs((dense_weight + bm25_weight) - 1.0) > tolerance:
        raise ValueError(
            f"fusion weights must sum to 1.0, got {dense_weight + bm25_weight}"
        )
    return (dense_weight, bm25_weight)


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
