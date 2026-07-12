# shard_manager.py
# Hash-based partitioning of index across virtual shards
# Data structure: Hash map for consistent hashing

import hashlib

class ShardManager:
    """
    Simulates distributed index partitioning.
    Terms are assigned to shards based on hash(term) % num_shards.
    This allows distributed query processing.
    """
    
    def __init__(self, num_shards=3):
        self.num_shards = num_shards
        # Each shard has its own inverted index
        self.shards = [{} for _ in range(num_shards)]
        # Shard statistics
        self.shard_stats = [{'terms': 0, 'documents': set()} for _ in range(num_shards)]
        self.document_manager = None  # Will be set later
    
    def set_document_manager(self, doc_manager):
        """Set document manager reference."""
        self.document_manager = doc_manager
    
    def _get_shard_id(self, term):
        """
        Determine which shard a term belongs to using hash.
        Consistent hashing simulation.
        """
        hash_value = int(hashlib.md5(term.encode()).hexdigest(), 16)
        return hash_value % self.num_shards
    
    def add_term_to_shard(self, term, doc_id, term_frequency):
        """Add a term-document posting to the appropriate shard."""
        shard_id = self._get_shard_id(term)
        
        if term not in self.shards[shard_id]:
            self.shards[shard_id][term] = {}
            self.shard_stats[shard_id]['terms'] += 1
        
        self.shards[shard_id][term][doc_id] = term_frequency
        self.shard_stats[shard_id]['documents'].add(doc_id)
    
    def search_term_in_shard(self, term, shard_id=None):
        """
        Search for a term in a specific shard or all shards.
        Returns list of (doc_id, tf) from that shard.
        """
        term = term.lower()
        if shard_id is not None:
            if term in self.shards[shard_id]:
                return list(self.shards[shard_id][term].items())
            return []
        else:
            # Search all shards (for aggregator)
            results = []
            for sid, shard in enumerate(self.shards):
                if term in shard:
                    results.extend([(doc_id, tf, sid) for doc_id, tf in shard[term].items()])
            return results
    
    def get_term_location(self, term):
        """Return which shard contains a term."""
        shard_id = self._get_shard_id(term)
        if term in self.shards[shard_id]:
            return shard_id
        return None
    
    def get_shard_stats(self):
        """Return statistics for each shard."""
        stats = []
        for i in range(self.num_shards):
            stats.append({
                'shard_id': i,
                'terms': self.shard_stats[i]['terms'],
                'documents': len(self.shard_stats[i]['documents']),
                'memory_estimate': sum(len(posting) for posting in self.shards[i].values())
            })
        return stats
    
    def rebuild_from_inverted_index(self, inverted_index):
        """
        Rebuild distributed shards from a centralized inverted index.
        Simulates distributing the index across shards.
        """
        # Clear existing shards
        self.shards = [{} for _ in range(self.num_shards)]
        self.shard_stats = [{'terms': 0, 'documents': set()} for _ in range(self.num_shards)]
        
        # Distribute each term to its shard
        for term, posting in inverted_index.index.items():
            shard_id = self._get_shard_id(term)
            self.shards[shard_id][term] = dict(posting)
            self.shard_stats[shard_id]['terms'] += 1
            for doc_id in posting:
                self.shard_stats[shard_id]['documents'].add(doc_id)
        
        return self.get_shard_stats()
    
    def get_shard(self, shard_id):
        """Return the entire index for a shard."""
        if 0 <= shard_id < self.num_shards:
            return self.shards[shard_id]
        return None
    
    def get_balance_score(self):
        """
        Calculate how balanced the distribution is.
        Lower score = more balanced (0 = perfectly balanced).
        """
        term_counts = [s['terms'] for s in self.shard_stats]
        if not term_counts:
            return 0
        avg = sum(term_counts) / len(term_counts)
        variance = sum((c - avg) ** 2 for c in term_counts) / len(term_counts)
        return variance