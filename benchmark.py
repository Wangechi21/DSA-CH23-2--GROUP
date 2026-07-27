import time
import random

class Benchmark:
    def __init__(self, search_engine):
        self.se = search_engine
    
    def run_all_benchmarks(self):
        """Run all benchmarks and print results."""
        print("=" * 70)
        print("DISTRIBUTED SEARCH ENGINE BENCHMARK - THEME D5")
        print("=" * 70)
        
        self.benchmark_hash_map_lookup()
        self.benchmark_inverted_index_insert()
        self.benchmark_heap_top_k()
        self.benchmark_queue_processing()
        self.benchmark_distributed_vs_single()
        self.benchmark_shard_balance()
        
        print("\n" + "=" * 70)
        self.print_complexity_summary()
    
    def benchmark_hash_map_lookup(self):
        """Test O(1) hash map performance."""
        print("\n[HASH MAP LOOKUP - O(1)]")
        
        # Add test documents
        doc_ids = []
        for i in range(1000):
            doc_id = self.se.doc_manager.add_document(f"Doc_{i}", f"Content of document number {i}")
            doc_ids.append(doc_id)
            self.se.index.add_document_to_index(doc_id, f"Content of document number {i}")
        
        start = time.time()
        iterations = 10000
        for _ in range(iterations):
            doc_id = random.choice(doc_ids)
            self.se.doc_manager.get_document(doc_id)
        elapsed = time.time() - start
        
        print(f"  {iterations} lookups: {elapsed:.4f} seconds")
        print(f"  Average: {elapsed/iterations:.7f} sec per lookup")
        print(f"  Theoretical: O(1) - constant time")
    
    def benchmark_inverted_index_insert(self):
        """Test inverted index insertion performance."""
        print("\n[INVERTED INDEX INSERT - O(1) per posting]")
        
        start = time.time()
        docs_inserted = 0
        for i in range(500):
            content = f"test document with many words and terms for indexing {i}"
            doc_id = self.se.doc_manager.add_document(f"BenchDoc_{i}", content)
            self.se.index.add_document_to_index(doc_id, content)
            docs_inserted += 1
        elapsed = time.time() - start
        
        print(f"  {docs_inserted} documents indexed: {elapsed:.4f} seconds")
        print(f"  Average per document: {elapsed/docs_inserted:.4f} sec")
        print(f"  Total unique terms: {self.se.index.get_term_count()}")
    
    def benchmark_heap_top_k(self):
        """Test heap-based top-K ranking."""
        print("\n[HEAP TOP-K RANKING - O(n log k)]")
        
        queries = ["document", "test", "content", "word", "indexing"]
        
        start = time.time()
        iterations = 100
        for _ in range(iterations):
            query = random.choice(queries)
            results = self.se.ranking_engine.rank_results_tfidf(query, top_k=10)
        elapsed = time.time() - start
        
        print(f"  {iterations} queries: {elapsed:.4f} seconds")
        print(f"  Average per query: {elapsed/iterations:.4f} sec")
        print(f"  Theoretical: O(n log k) where n=candidates, k=10")
    
    def benchmark_queue_processing(self):
        """Test queue throughput."""
        print("\n[QUEUE PROCESSING - O(1) enqueue/dequeue]")
        
        # Add queries to queue
        start = time.time()
        queries_to_add = 5000
        for i in range(queries_to_add):
            self.se.query_queue.enqueue_query(f"Query_{i}")
        enqueue_time = time.time() - start
        
        # Dequeue all
        start = time.time()
        dequeued = 0
        while self.se.query_queue.dequeue_query():
            dequeued += 1
        dequeue_time = time.time() - start
        
        print(f"  Enqueued {queries_to_add} queries: {enqueue_time:.4f} sec")
        print(f"  Dequeued {dequeued} queries: {dequeue_time:.4f} sec")
        print(f"  Theoretical: O(1) per operation")
    
    def benchmark_distributed_vs_single(self):
        """Compare distributed search vs single node."""
        print("\n[DISTRIBUTED VS SINGLE NODE SEARCH]")
        
        test_query = "document test"
        
        # Distributed search (across all shards)
        start = time.time()
        iterations = 50
        for _ in range(iterations):
            results_dist = self.se.aggregator.distributed_search(test_query, top_k=10)
        dist_time = time.time() - start
        
        # Single shard search (only shard 0)
        start = time.time()
        for _ in range(iterations):
            results_single = self.se.aggregator.search_single_shard(test_query, shard_id=0, top_k=10)
        single_time = time.time() - start
        
        print(f"  Distributed ({self.se.shard_manager.num_shards} shards): {dist_time:.4f} sec for {iterations} queries")
        print(f"  Single node: {single_time:.4f} sec for {iterations} queries")
        print(f"  Overhead: {(dist_time/single_time - 1) * 100:.1f}% slower for distributed (expected)")
    
    def benchmark_shard_balance(self):
        """Check how balanced the hash distribution is."""
        print("\n[SHARD BALANCE - Consistent Hashing]")
        
        stats = self.se.shard_manager.get_shard_stats()
        print(f"  Number of shards: {self.se.shard_manager.num_shards}")
        for stat in stats:
            print(f"    Shard {stat['shard_id']}: {stat['terms']} terms, {stat['documents']} docs")
        
        balance_score = self.se.shard_manager.get_balance_score()
        print(f"  Balance score (lower=better): {balance_score:.2f}")
        
        if balance_score < 1000:
            print("  ✓ Well balanced distribution")
        else:
            print("  ⚠ Distribution could be improved")
    
    def print_complexity_summary(self):
        """Print Big-O summary table."""
        print("""
+--------------------------+-------------------+-----------------+------------------+
| Operation                | Data Structure    | Time Complexity | Space Complexity |
+--------------------------+-------------------+-----------------+------------------+
| Document lookup          | Hash Map          | O(1)            | O(n)             |
| Term lookup              | Hash Map (index)  | O(1)            | O(t)             |
| Shard assignment         | Consistent Hash   | O(1)            | O(1)             |
| Query enqueue            | Queue             | O(1)            | O(q)             |
| Top-K ranking            | Min-Heap          | O(n log k)      | O(k)             |
| Query history (back)     | Stack             | O(1)            | O(h)             |
| Distributed search       | Multiple shards   | O(s * n)        | O(n)             |
| Result merging           | Heap              | O(m log k)      | O(k)             |
+--------------------------+-------------------+-----------------+------------------+

Legend:
n = number of documents, t = unique terms, q = pending queries
k = top-K results, h = history size, s = number of shards
m = results from all shards
""")
