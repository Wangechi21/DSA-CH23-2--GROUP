# document_manager.py
# Document storage and retrieval using Hash Map
# Data structure: Hash Table for O(1) document lookup

class DocumentManager:
    def __init__(self):
        # Hash map: doc_id -> document object
        self.documents = {}
        self.next_id = 1
        self.total_terms = 0
    
    def add_document(self, title, content):
        """Add a document to the index. Returns doc_id."""
        doc_id = self.next_id
        self.documents[doc_id] = {
            'id': doc_id,
            'title': title,
            'content': content,
            'word_count': len(content.split())
        }
        self.next_id += 1
        self.total_terms += len(content.split())
        return doc_id
    
    def get_document(self, doc_id):
        """O(1) hash map lookup by document ID."""
        return self.documents.get(doc_id)
    
    def get_all_documents(self):
        """Return all documents."""
        return list(self.documents.values())
    
    def get_document_count(self):
        """Return total number of documents."""
        return len(self.documents)
    
    def delete_document(self, doc_id):
        """Remove document from hash map."""
        if doc_id in self.documents:
            del self.documents[doc_id]
            return True
        return False
    
    def update_document(self, doc_id, new_content):
        """Update document content."""
        if doc_id in self.documents:
            self.documents[doc_id]['content'] = new_content
            self.documents[doc_id]['word_count'] = len(new_content.split())
            return True
        return False
    
    def get_document_by_title(self, title):
        """Linear search O(n) by title."""
        for doc_id, doc in self.documents.items():
            if doc['title'].lower() == title.lower():
                return doc_id, doc
        return None, None
    
    def get_total_terms(self):
        """Return total terms across all documents."""
        return self.total_terms
