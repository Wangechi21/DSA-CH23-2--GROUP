
from collections import deque
import time
import threading

class QueryQueue:
    """
    Queue manager for search requests.

    Supports:
    - Priority scheduling
    - FIFO processing
    - Queue statistics
    - Batch insertion
    """
    def __init__(self):
        # Main queue for pending queries
        self.queue = deque()
        # Priority queues for different query types
        self.high_priority_queue = deque()
        self.normal_queue = deque()
        self.low_priority_queue = deque()
        
        # Query history for tracking
        self.processed_queries = []
        self.query_count = 0
        
        # Rate limiting
        self.queries_per_second = 0
        self.last_query_time = time.time()
    
    def enqueue_query(self, query_text, priority='normal'):

        query_obj = {
            'id': self.query_count + 1,
            'text': query_text,
            'priority': priority,
            'timestamp': time.time(),
            'status': 'pending'
        }
        
        if priority == 'high':
            self.high_priority_queue.append(query_obj)
        elif priority == 'low':
            self.low_priority_queue.append(query_obj)
        else:
            self.normal_queue.append(query_obj)
        
        self.query_count += 1
        return query_obj['id']
    
    def dequeue_query(self):
        
        if self.high_priority_queue:
            query = self.high_priority_queue.popleft()
        elif self.normal_queue:
            query = self.normal_queue.popleft()
        elif self.low_priority_queue:
            query = self.low_priority_queue.popleft()
        else:
            return None
        
        query['status'] = 'processing'
        return query
    
    def mark_completed(self, query_id, results):
        """Mark a query as completed and store results."""
        for q in self.processed_queries:
            if q['id'] == query_id:
                q['status'] = 'completed'
                q['results'] = results
                q['completion_time'] = time.time()
                return True
        

        self.processed_queries.append({
            'id': query_id,
            'status': 'completed',
            'results': results,
            'completion_time': time.time()
        })
        return True
    
    def get_queue_size(self):
        """Return total pending queries."""
        return len(self.high_priority_queue) + len(self.normal_queue) + len(self.low_priority_queue)
    
    def get_next_query_sync(self, timeout=None):
        """
        Blocking call to get next query.
        Simulates synchronous queue processing.
        """
        start = time.time()
        while True:
            query = self.dequeue_query()
            if query:
                return query
            
            if timeout and (time.time() - start) > timeout:
                return None
            
            time.sleep(0.01)  # Small delay to prevent busy waiting
    
    def get_query_stats(self):
        """Return statistics about query processing."""
        return {
            'total_queries': self.query_count,
            'pending': self.get_queue_size(),
            'processed': len(self.processed_queries),
            'avg_queue_time': self._calculate_avg_queue_time()
        }
    def show_pending_queries(self):
        """Display all pending queries."""
        return {
        "high": list(self.high_priority_queue),
        "normal": list(self.normal_queue),
        "low": list(self.low_priority_queue)
    }
    def _calculate_avg_queue_time(self):
        """Calculate average time queries spent in queue."""
        completed = [q for q in self.processed_queries if 'completion_time' in q and 'timestamp' in q]
        if not completed:
            return 0
        
        total_time = sum(q['completion_time'] - q.get('timestamp', q['completion_time']) 
                        for q in completed)
        return total_time / len(completed)
    
    def clear_all(self):
        """Clear all queues."""
        self.high_priority_queue.clear()
        self.normal_queue.clear()
        self.low_priority_queue.clear()
    
    def batch_enqueue(self, queries):
        """Add multiple queries at once."""
        for query in queries:
            self.enqueue_query(query)