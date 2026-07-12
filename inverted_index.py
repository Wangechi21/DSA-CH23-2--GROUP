# inverted_index.py
# Core inverted index using Hash Map
# Data structure: Hash Table mapping term -> posting list

from collections import defaultdict
import math

class InvertedIndex:
    def __init__(self, document_manager):
        self.doc_manager = document_manager
        # Hash map: term -> {doc_id: term_frequency}
        self.index = defaultdict(lambda: defaultdict(int))
        # Document frequency: term -> number of docs containing it
        self.document_frequency = defaultdict(int)
    
    def add_document_to_index(self, doc_id, content):
        """
        Add a document to the inverted index.
        Tokenizes content and builds posting lists.
        """
        terms = self._tokenize(content)
        
        # Count term frequency in this document
        term_counts = defaultdict(int)
        for term in terms:
            term_counts[term] += 1
        
        # Update inverted index
        for term, count in term_counts.items():
            self.index[term][doc_id] = count
            self.document_frequency[term] += 1
    
    def _tokenize(self, text):
        """Simple tokenizer: lowercase, split on whitespace, remove punctuation."""
        import re
        # Convert to lowercase and split on non-alphanumeric
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return words
    
    def search_term(self, term):
        """
        Search for a single term.
        Returns list of (doc_id, term_frequency) for docs containing term.
        """
        term = term.lower()
        if term in self.index:
            return list(self.index[term].items())
        return []
    
    def get_posting_list(self, term):
        """Return full posting list for a term (hash map of doc_id -> tf)."""
        term = term.lower()
        return self.index.get(term, {})
    
    def get_document_frequency(self, term):
        """Return how many documents contain the term."""
        return self.document_frequency.get(term.lower(), 0)
    
    def get_all_terms(self):
        """Return all terms in the index."""
        return list(self.index.keys())
    
    def get_term_count(self):
        """Return total unique terms."""
        return len(self.index)
    
    def compute_tf_idf(self, term, doc_id):
        """
        Compute TF-IDF score for a term in a document.
        TF = term frequency in document
        IDF = log(total_docs / doc_frequency)
        """
        posting = self.get_posting_list(term)
        if doc_id not in posting:
            return 0.0
        
        tf = posting[doc_id]
        doc_freq = self.get_document_frequency(term)
        total_docs = self.doc_manager.get_document_count()
        
        if doc_freq == 0:
            return 0.0
        
        idf = math.log(total_docs / doc_freq)
        return tf * idf
    
    def remove_document(self, doc_id):
        """Remove a document from the inverted index."""
        for term, posting in list(self.index.items()):
            if doc_id in posting:
                del self.index[term][doc_id]
                self.document_frequency[term] -= 1
                # Remove term if posting list becomes empty
                if self.document_frequency[term] == 0:
                    del self.index[term]
                    del self.document_frequency[term]