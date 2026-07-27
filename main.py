import sys

class DistributedSearchEngine:
    def __init__(self, num_shards=3):
        from document_manager import DocumentManager
        from inverted_index import InvertedIndex
        from shard_manager import ShardManager
        from query_queue import QueryQueue
        from search_aggregator import SearchAggregator
        from ranking_heap import RankingEngine
        from query_history_stack import QueryHistoryStack
        
        # Core components
        self.doc_manager = DocumentManager()
        self.index = InvertedIndex(self.doc_manager)
        self.shard_manager = ShardManager(num_shards)
        self.query_queue = QueryQueue()
        self.history = QueryHistoryStack()
        
        # Set up dependencies
        self.shard_manager.set_document_manager(self.doc_manager)
        
        # High-level components
        self.aggregator = SearchAggregator(self.shard_manager, self.doc_manager)
        self.ranking_engine = RankingEngine(self.index, self.doc_manager)
        
        # Build shards from index
        self._rebuild_shards()
    
    def _rebuild_shards(self):
        """Rebuild distributed shards from inverted index."""
        self.shard_manager.rebuild_from_inverted_index(self.index)
    
    def add_document(self, title, content):
        """Add a document to the search engine."""
        doc_id = self.doc_manager.add_document(title, content)
        self.index.add_document_to_index(doc_id, content)
        self._rebuild_shards()  # Rebuild shards after adding
        return doc_id
    
    def search(self, query, top_k=10, distributed=True):
        """
        Perform search.
        If distributed=True, uses all shards.
        If distributed=False, uses single node (shard 0 only).
        """
        # Add to history
        if distributed:
            results = self.aggregator.distributed_search(query, top_k)
        else:
            results = self.aggregator.search_single_shard(query, shard_id=0, top_k=top_k)
        
        # Save to history
        self.history.push_query(query, results)
        
        return results
    
    def search_ranked(self, query, top_k=10):
        """Search with TF-IDF ranking (uses heap)."""
        results = self.ranking_engine.rank_results_tfidf(query, top_k)
        self.history.push_query(query, results)
        return results
    
    def enqueue_search(self, query, priority='normal'):
        """Queue a search for later processing."""
        return self.query_queue.enqueue_query(query, priority)
    
    def process_next_query(self):
        """Process the next query in the queue."""
        query_obj = self.query_queue.dequeue_query()
        if query_obj:
            results = self.search(query_obj['text'])
            self.query_queue.mark_completed(query_obj['id'], results)
            return results
        return None
    
    def run_cli(self):
        print("\n" + "=" * 70)
        print("DISTRIBUTED SEARCH ENGINE - THEME D5")
        print("=" * 70)
        print("Features:")
        print("  • Hash Map: Document storage & inverted index")
        print("  • Stack: Search history (back/forward)")
        print("  • Queue: Query buffering")
        print("  • Heap: Top-K ranking (O(n log k))")
        print("  • Distributed shards: Hash-based partitioning")
        print("=" * 70)
        
        print("\nCommands:")
        print("  add <title> : <content>     - Add document")
        print("  search <query> [top_k]      - Search (distributed)")
        print("  rank <query> [top_k]        - Search with TF-IDF ranking")
        print("  queue <query> [priority]    - Queue a search")
        print("  process                      - Process next queued query")
        print("  back                         - Go to previous search (stack)")
        print("  forward                      - Go to next search (stack)")
        print("  stats                        - Show system statistics")
        print("  shards                       - Show shard distribution")
        print("  benchmark                    - Run performance tests")
        print("  test                         - Run 15 test cases")
        print("  exit                         - Exit")
        print("-" * 70)
        
        # Load demo data
        self._load_demo_data()
        
        while True:
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue
                
                if cmd == 'exit':
                    print("Goodbye!")
                    break
                
                elif cmd == 'back':
                    result, msg = self.history.back()
                    if result:
                        print(f"  {msg}")
                        print(f"  Query: {result['text']}")
                        print(f"  Results: {len(result['results'])} documents")
                    else:
                        print(f"  {msg}")
                
                elif cmd == 'forward':
                    result, msg = self.history.forward()
                    if result:
                        print(f"  {msg}")
                        print(f"  Query: {result['text']}")
                        print(f"  Results: {len(result['results'])} documents")
                    else:
                        print(f"  {msg}")
                
                elif cmd == 'stats':
                    self._show_stats()
                
                elif cmd == 'shards':
                    self._show_shards()
                
                elif cmd == 'benchmark':
                    from benchmark import Benchmark
                    bm = Benchmark(self)
                    bm.run_all_benchmarks()
                
                elif cmd == 'test':
                    from test_cases import TestRunner
                    tr = TestRunner(self)
                    tr.run_all_tests()
                
                elif cmd.startswith('add '):
                    # Parse "add title : content"
                    rest = cmd[4:].strip()
                    if ' : ' in rest:
                        title, content = rest.split(' : ', 1)
                        doc_id = self.add_document(title, content)
                        print(f"  ✓ Added document '{title}' with ID {doc_id}")
                    else:
                        print("  Format: add <title> : <content>")
                
                elif cmd.startswith('search '):
                    parts = cmd.split()
                    query = parts[1]
                    top_k = int(parts[2]) if len(parts) > 2 else 10
                    results = self.search(query, top_k)
                    self._print_results(results, query, "DISTRIBUTED")
                
                elif cmd.startswith('rank '):
                    parts = cmd.split()
                    query = parts[1]
                    top_k = int(parts[2]) if len(parts) > 2 else 10
                    results = self.search_ranked(query, top_k)
                    self._print_results(results, query, "TF-IDF RANKED")
                
                elif cmd.startswith('queue '):
                    parts = cmd.split()
                    query = parts[1]
                    priority = parts[2] if len(parts) > 2 else 'normal'
                    qid = self.enqueue_search(query, priority)
                    print(f"  ✓ Query queued with ID {qid} (priority: {priority})")
                    print(f"  Pending queries: {self.query_queue.get_queue_size()}")
                
                elif cmd == 'process':
                    results = self.process_next_query()
                    if results:
                        print(f"  Processed query, found {len(results)} results")
                        self._print_results(results, "queued query", "QUEUED")
                    else:
                        print("  No pending queries")
                
                else:
                    print("  Unknown command")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"  Error: {e}")
    
    def _load_demo_data(self):
        """Load demo documents."""
        print("\nLoading demo documents...")
        
        demo_docs = [
            ("Python Programming", "Python is a powerful programming language for data science and web development."),
            ("Data Structures", "Hash maps, stacks, queues, heaps, and graphs are essential data structures."),
            ("Search Engines", "Search engines use inverted indexes and distributed systems for fast retrieval."),
            ("Machine Learning", "Machine learning algorithms learn patterns from data."),
            ("Web Development", "Web development involves frontend and backend technologies."),
            ("Algorithms", "Sorting and searching algorithms are fundamental to computer science."),
            ("Databases", "Databases use indexing and query optimization for performance."),
            ("Cloud Computing", "Cloud computing enables distributed systems at scale."),
        ]
        
        for title, content in demo_docs:
            self.add_document(title, content)
        
        print(f"  Loaded {len(demo_docs)} demo documents")
        print(f"  Total unique terms: {self.index.get_term_count()}")
        print(f"  Distributed across {self.shard_manager.num_shards} shards")
    
    def _print_results(self, results, query, search_type):
        """Pretty print search results."""
        print(f"\n  [{search_type}] Search Results for '{query}':")
        if not results:
            print("  No results found.")
        else:
            for i, doc in enumerate(results[:10], 1):
                print(f"    {i}. {doc.get('title', 'Unknown')} (score: {doc.get('score', 'N/A')})")
    
    def _show_stats(self):
        """Show system statistics."""
        print("\n=== SYSTEM STATISTICS ===")
        print(f"  Documents: {self.doc_manager.get_document_count()}")
        print(f"  Unique terms: {self.index.get_term_count()}")
        print(f"  Shards: {self.shard_manager.num_shards}")
        print(f"  Pending queries: {self.query_queue.get_queue_size()}")
        print(f"  History size: {self.history.get_history_size()}")
        print(f"  Can go back: {self.history.can_back()}")
        print(f"  Can go forward: {self.history.can_forward()}")
    
    def _show_shards(self):
        """Show shard distribution."""
        print("\n=== SHARD DISTRIBUTION ===")
        stats = self.shard_manager.get_shard_stats()
        for stat in stats:
            print(f"  Shard {stat['shard_id']}: {stat['terms']} terms, {stat['documents']} documents")
        
        balance = self.shard_manager.get_balance_score()
        print(f"\n  Balance score: {balance:.2f} (lower = more balanced)")


def main():
    engine = DistributedSearchEngine(num_shards=3)
    engine.run_cli()


if __name__ == "__main__":
    main()
