# query_history_stack.py
# Stack implementation for search history (undo/redo)
# Data structure: Stack for LIFO query history

class QueryHistoryStack:
    """
    Manages search query history using a stack.
    Supports undo (back) and redo (forward) navigation.
    """
    
    def __init__(self, max_history=50):
        # Stack for back navigation (undo)
        self.back_stack = []
        # Stack for forward navigation (redo)
        self.forward_stack = []
        self.current_query = None
        self.max_history = max_history
    
    def push_query(self, query_text, results):
        """
        Add a new query to history.
        Clears forward stack when new query is performed.
        """
        query_obj = {
            'text': query_text,
            'results': results,
            'timestamp': None  # Can add timestamp
        }
        
        if self.current_query:
            self.back_stack.append(self.current_query)
            # Limit history size
            if len(self.back_stack) > self.max_history:
                self.back_stack.pop(0)
        
        self.current_query = query_obj
        self.forward_stack.clear()
        
        return True
    
    def back(self):
        """
        Go back to previous query (undo).
        Returns previous query or None.
        """
        if not self.back_stack:
            return None, "No previous queries"
        
        # Move current to forward stack
        if self.current_query:
            self.forward_stack.append(self.current_query)
        
        # Pop from back stack
        self.current_query = self.back_stack.pop()
        
        return self.current_query, "Moved back to previous query"
    
    def forward(self):
        """
        Go forward to next query (redo).
        Returns next query or None.
        """
        if not self.forward_stack:
            return None, "No forward queries"
        
        # Move current to back stack
        if self.current_query:
            self.back_stack.append(self.current_query)
        
        # Pop from forward stack
        self.current_query = self.forward_stack.pop()
        
        return self.current_query, "Moved forward to next query"
    
    def get_current(self):
        """Return current query."""
        return self.current_query
    
    def get_history(self):
        """Return all queries in back history."""
        return self.back_stack.copy()
    
    def get_forward_history(self):
        """Return all queries in forward history."""
        return self.forward_stack.copy()
    
    def clear(self):
        """Clear all history."""
        self.back_stack.clear()
        self.forward_stack.clear()
        self.current_query = None
    
    def can_back(self):
        """Check if back is possible."""
        return len(self.back_stack) > 0
    
    def can_forward(self):
        """Check if forward is possible."""
        return len(self.forward_stack) > 0
    
    def get_history_size(self):
        """Return total history size."""
        return len(self.back_stack) + (1 if self.current_query else 0)
