# search_aggregator.py
# Aggregator that fans out queries to shards and merges results
# Data structure: Heap for merging top-K results from multiple shards

import heapq
from collections import defaultdict

class SearchAggregator:
    """
    Simulates a distributed search aggregator.
    Receives queries, fans out to all shards, and merges results.
    """
    
    def __init__(self, shard_manager, document_manager):
        self.shard_manager = shard_manager
        self.doc_manager = document_manager
        self.num_shards = shard_manager.num_shards
    
    def distributed_search(self, query, top_k=10):
        """
        Perform distributed search across all shards.
        1. Parse query into terms
        2. Fan out to all shards (simulated)
        3. Collect results from each shard
        4. Merge using heap for top-K
        """
        terms = self._parse_query(query)
        
        if not terms:
            return []
        
        # Fan out: Query each shard for each term
        # In a real distributed system, this would be parallel
        shard_results = []
        for shard_id in range(self.num_shards):
            shard_result = self._query_shard(terms, shard_id)
            shard_results.append(shard_result)
        
        # Merge results using heap
        merged = self._merge_results(shard_results, top_k)
        
        return merged
    
    def _parse_query(self, query):
        """Parse query into individual terms."""
        import re
        terms = re.findall(r'\b[a-z0-9]+\b', query.lower())
        return terms
    
    def _query_shard(self, terms, shard_id):
        """
        Query a single shard.
        Returns dict of doc_id -> total score for this shard.
        """
        shard = self.shard_manager.get_shard(shard_id)
        if not shard:
            return {}
        
        scores = defaultdict(float)
        
        for term in terms:
            if term in shard:
                posting = shard[term]
                for doc_id, tf in posting.items():
                    # Simple scoring: term frequency
                    scores[doc_id] += tf
        
        return scores
    
    def _merge_results(self, shard_results, top_k):
        """
        Merge results from multiple shards using a min-heap.
        Returns top K documents sorted by score.
        """
        # Aggregate scores across shards
        total_scores = defaultdict(float)
        for shard_score in shard_results:
            for doc_id, score in shard_score.items():
                total_scores[doc_id] += score
        
        if not total_scores:
            return []
        
        # Use min-heap to keep top K
        heap = []
        for doc_id, score in total_scores.items():
            heapq.heappush(heap, (score, doc_id))
            if len(heap) > top_k:
                heapq.heappop(heap)
        
        # Extract and sort descending
        results = sorted(heap, reverse=True)
        
        # Enrich with document details
        enriched = []
        for score, doc_id in results:
            doc = self.doc_manager.get_document(doc_id)
            if doc:
                enriched.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'score': score,
                    'content_preview': doc['content'][:100] + "..."
                })
        
        return enriched
    
    def search_single_shard(self, query, shard_id, top_k=10):
        """
        Search only a specific shard (for comparison/benchmarking).
        """
        terms = self._parse_query(query)
        if not terms:
            return []
        
        scores = self._query_shard(terms, shard_id)
        
        # Use heap for top-K
        heap = [(score, doc_id) for doc_id, score in scores.items()]
        heapq.heapify(heap)
        
        results = []
        while heap and len(results) < top_k:
            score, doc_id = heapq.heappop(heap)
            doc = self.doc_manager.get_document(doc_id)
            if doc:
                results.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'score': score
                })
        
        return sorted(results, key=lambda x: x['score'], reverse=True)
    
    def get_shard_load(self):
        """Return estimated load distribution across shards."""
        stats = self.shard_manager.get_shard_stats()
        return [s['terms'] for s in stats]
