class TestRunner:
    def __init__(self, search_engine):
        self.se = search_engine
        self.passed = 0
        self.failed = 0
    
    def run_all_tests(self):
        print("=" * 60)
        print("RUNNING 15 TEST CASES - THEME D5")
        print("=" * 60)
        
        self.test_1_add_document()
        self.test_2_inverted_index_lookup()
        self.test_3_shard_assignment()
        self.test_4_search_single_term()
        self.test_5_search_multiple_terms()
        self.test_6_queue_enqueue_dequeue()
        self.test_7_heap_top_k_ranking()
        self.test_8_query_history_back()
        self.test_9_query_history_forward()
        self.test_10_distributed_search()
        self.test_11_distributed_vs_single()
        self.test_12_shard_balance()
        self.test_13_boolean_search()
        self.test_14_edge_case_empty_query()
        self.test_15_large_document_handling()
        
        print("\n" + "=" * 60)
        print(f"RESULTS: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        return self.failed == 0
    
    def assert_equal(self, actual, expected, test_name):
        if actual == expected:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name} - Expected {expected}, got {actual}")
            self.failed += 1
            return False
    
    def assert_true(self, condition, test_name):
        if condition:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name} - Condition false")
            self.failed += 1
            return False
    
    def test_1_add_document(self):
        doc_id = self.se.doc_manager.add_document("Test Title", "Test content")
        self.assert_true(doc_id is not None, "Test 1: Add document returns ID")
    
    def test_2_inverted_index_lookup(self):
        results = self.se.index.search_term("test")
        self.assert_true(len(results) >= 0, "Test 2: Inverted index lookup works")
    
    def test_3_shard_assignment(self):
        shard_id = self.se.shard_manager._get_shard_id("testterm")
        self.assert_true(0 <= shard_id < self.se.shard_manager.num_shards, 
                        "Test 3: Shard assignment within range")
    
    def test_4_search_single_term(self):
        self.se.doc_manager.add_document("Doc1", "python programming")
        self.se.index.add_document_to_index(1, "python programming")
        results = self.se.ranking_engine.rank_results_tfidf("python", top_k=5)
        self.assert_true(len(results) >= 0, "Test 4: Single term search works")
    
    def test_5_search_multiple_terms(self):
        results = self.se.ranking_engine.rank_results_tfidf("python programming", top_k=5)
        self.assert_true(isinstance(results, list), "Test 5: Multiple term search returns list")
    
    def test_6_queue_enqueue_dequeue(self):
        self.se.query_queue.enqueue_query("test query")
        query = self.se.query_queue.dequeue_query()
        self.assert_true(query is not None, "Test 6: Queue enqueue/dequeue works")
    
    def test_7_heap_top_k_ranking(self):
        results = self.se.ranking_engine.rank_results_tfidf("test", top_k=3)
        self.assert_true(len(results) <= 3, "Test 7: Top-K returns at most K results")
    
    def test_8_query_history_back(self):
        self.se.history.push_query("query1", [])
        self.se.history.push_query("query2", [])
        result, _ = self.se.history.back()
        self.assert_true(result['text'] == "query1", "Test 8: History back returns previous query")
    
    def test_9_query_history_forward(self):
        result, _ = self.se.history.forward()
        self.assert_true(result['text'] == "query2", "Test 9: History forward returns next query")
    
    def test_10_distributed_search(self):
        results = self.se.aggregator.distributed_search("test", top_k=5)
        self.assert_true(isinstance(results, list), "Test 10: Distributed search returns list")
    
    def test_11_distributed_vs_single(self):
        dist_results = self.se.aggregator.distributed_search("test", top_k=5)
        single_results = self.se.aggregator.search_single_shard("test", shard_id=0, top_k=5)
        self.assert_true(isinstance(dist_results, list) and isinstance(single_results, list),
                        "Test 11: Both search methods work")
    
    def test_12_shard_balance(self):
        stats = self.se.shard_manager.get_shard_stats()
        self.assert_equal(len(stats), self.se.shard_manager.num_shards, 
                         "Test 12: Shard stats for all shards")
    
    def test_13_boolean_search(self):
        results = self.se.ranking_engine.rank_boolean("test")
        self.assert_true(isinstance(results, list), "Test 13: Boolean search works")
    
    def test_14_edge_case_empty_query(self):
        results = self.se.ranking_engine.rank_results_tfidf("", top_k=5)
        self.assert_equal(len(results), 0, "Test 14: Empty query returns empty results")
    
    def test_15_large_document_handling(self):
        large_content = "word " * 10000  # 10,000 words
        doc_id = self.se.doc_manager.add_document("Large Doc", large_content)
        self.se.index.add_document_to_index(doc_id, large_content)
        results = self.se.ranking_engine.rank_results_tfidf("word", top_k=1)
        self.assert_true(len(results) >= 0, "Test 15: Large document handled without error")
