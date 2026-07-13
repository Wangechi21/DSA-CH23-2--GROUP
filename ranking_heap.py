# ranking_heap.py
# TF-IDF scoring and heap-based top-K ranking
# Data structure: Min-Heap for efficient top-K selection

import heapq
import math
import re
from collections import defaultdict

class RankingEngine:
    """
    Computes relevance scores and returns top-K results using heap.
    Implements TF-IDF scoring.
    """
    
    def __init__(self, inverted_index, document_manager):
        self.index = inverted_index
        self.doc_manager = document_manager
        self.total_docs = document_manager.get_document_count()
    
    def _parse_query(self, query):
        """Parse query into terms."""
        if not query or not isinstance(query, str):
            return []
        return re.findall(r'\b[a-z0-9]+\b', query.lower())
    
    def rank_results_tfidf(self, query, top_k=10):
        """
        Rank search results using TF-IDF.
        Uses min-heap to maintain top K results efficiently.
        Time complexity: O(n log k) where n = number of matching docs.
        """
        terms = self._parse_query(query)
        if not terms:
            return []
        
        # Calculate scores for each document
        doc_scores = defaultdict(float)
        
        for term in terms:
            posting = self.index.get_posting_list(term)
            doc_freq = self.index.get_document_frequency(term)
            
            if doc_freq == 0 or not posting:
                continue
            
            idf = math.log(self.total_docs / doc_freq) if doc_freq > 0 else 0
            
            for doc_id, tf in posting.items():
                doc_scores[doc_id] += tf * idf
        
        if not doc_scores:
            return []
        
        # Min-heap to keep top K (O(n log k))
        heap = []
        for doc_id, score in doc_scores.items():
            heapq.heappush(heap, (score, doc_id))
            if len(heap) > top_k:
                heapq.heappop(heap)
        
        # Extract results in descending order
        results = sorted(heap, reverse=True)
        
        # Enrich with document details
        enriched = []
        for score, doc_id in results:
            doc = self.doc_manager.get_document(doc_id)
            if doc:
                enriched.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'score': round(score, 4),
                    'word_count': doc.get('word_count', 0)
                })
        
        return enriched
    
    def rank_bm25(self, query, top_k=10, k1=1.5, b=0.75):
        """
        BM25 ranking algorithm (more sophisticated than TF-IDF).
        Uses heap for top-K selection.
        """
        terms = self._parse_query(query)
        if not terms:
            return []
        
        avg_doc_len = self.doc_manager.get_total_terms() / max(1, self.total_docs)
        doc_scores = defaultdict(float)
        
        for term in terms:
            posting = self.index.get_posting_list(term)
            doc_freq = self.index.get_document_frequency(term)
            
            if doc_freq == 0 or not posting:
                continue
            
            idf = math.log((self.total_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1)
            
            for doc_id, tf in posting.items():
                doc = self.doc_manager.get_document(doc_id)
                if not doc:
                    continue
                
                doc_len = doc.get('word_count', 0)
                if doc_len == 0:
                    continue
                    
                norm = 1 - b + b * (doc_len / avg_doc_len)
                
                # BM25 scoring formula
                score = idf * (tf * (k1 + 1)) / (tf + k1 * norm)
                doc_scores[doc_id] += score
        
        if not doc_scores:
            return []
        
        # Heap for top-K
        heap = []
        for doc_id, score in doc_scores.items():
            heapq.heappush(heap, (score, doc_id))
            if len(heap) > top_k:
                heapq.heappop(heap)
        
        results = sorted(heap, reverse=True)
        
        enriched = []
        for score, doc_id in results:
            doc = self.doc_manager.get_document(doc_id)
            if doc:
                enriched.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'score': round(score, 4)
                })
        
        return enriched
    
    def rank_boolean(self, query):
        """
        Boolean search: documents must contain ALL terms.
        Uses set intersection.
        """
        terms = self._parse_query(query)
        if not terms:
            return []
        
        # Get document sets for each term
        doc_sets = []
        for term in terms:
            posting = self.index.get_posting_list(term)
            if posting:
                doc_sets.append(set(posting.keys()))
        
        if not doc_sets:
            return []
        
        # Intersection of all sets
        result_docs = doc_sets[0]
        for doc_set in doc_sets[1:]:
            result_docs = result_docs.intersection(doc_set)
        
        # Return document details
        results = []
        for doc_id in result_docs:
            doc = self.doc_manager.get_document(doc_id)
            if doc:
                results.append({
                    'doc_id': doc_id,
                    'title': doc['title']
                })
        
        return results
