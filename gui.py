# gui.py
# GUI Interface for Distributed Search Engine using Tkinter

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading

class SearchEngineGUI:
    """GUI for Distributed Search Engine - Theme D5"""
    
    def __init__(self):
        self.root = None
        self.engine = None
        self.setup_gui()
    
    def setup_gui(self):
        """Initialize the GUI window."""
        self.root = tk.Tk()
        self.root.title("🔍 Distributed Search Engine - Theme D5")
        self.root.geometry("1300x850")
        self.root.configure(bg='#1e1e2e')
        
        # Initialize engine
        self.engine = None
        
        # Create fonts
        self.title_font = ('Segoe UI', 16, 'bold')
        self.header_font = ('Segoe UI', 12, 'bold')
        self.normal_font = ('Segoe UI', 10)
        self.mono_font = ('Consolas', 10)
        
        # Create main container
        self.create_widgets()
        
        # Bind closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize engine after GUI is ready
        self.root.after(100, self.initialize_engine)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, text="🔍 DISTRIBUTED SEARCH ENGINE", 
                               font=self.title_font, fg='#00ff88', bg='#1e1e2e')
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame, text="Theme D5 - Hash-Based Partitioning", 
                                  font=('Segoe UI', 10), fg='#8888aa', bg='#1e1e2e')
        subtitle_label.pack(side=tk.RIGHT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_search_tab()
        self.create_add_tab()
        self.create_queue_tab()
        self.create_history_tab()
        self.create_shards_tab()
        self.create_stats_tab()
        self.create_benchmark_tab()
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="✅ Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W,
                                   bg='#2d2d44', fg='#88ffaa', font=self.normal_font)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def create_search_tab(self):
        """Create the Search tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Search")
        
        # Search frame
        search_frame = tk.LabelFrame(tab, text=" Search Query ", 
                                     font=self.header_font, fg='#00ff88',
                                     bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Query input
        query_frame = tk.Frame(search_frame, bg='#1e1e2e')
        query_frame.pack(fill=tk.X, pady=5, padx=5)
        
        tk.Label(query_frame, text="Query:", font=self.header_font,
                fg='#ffffff', bg='#1e1e2e').pack(side=tk.LEFT, padx=(0, 10))
        
        self.query_entry = tk.Entry(query_frame, width=50, font=self.normal_font,
                                    bg='#2d2d44', fg='#ffffff', insertbackground='white',
                                    bd=2, relief=tk.FLAT)
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.query_entry.bind('<Return>', lambda e: self.do_search())
        
        # Search options
        options_frame = tk.Frame(search_frame, bg='#1e1e2e')
        options_frame.pack(fill=tk.X, pady=5, padx=5)
        
        tk.Label(options_frame, text="Top-K:", font=self.normal_font,
                fg='#ffffff', bg='#1e1e2e').pack(side=tk.LEFT, padx=(0, 5))
        
        self.top_k_var = tk.StringVar(value="10")
        self.top_k_spin = tk.Spinbox(options_frame, from_=1, to=100, width=5,
                                     textvariable=self.top_k_var,
                                     bg='#2d2d44', fg='#ffffff', buttonbackground='#3d3d5c')
        self.top_k_spin.pack(side=tk.LEFT, padx=(0, 15))
        
        self.search_type_var = tk.StringVar(value="distributed")
        
        search_types = [
            ("🌐 Distributed", "distributed"),
            ("📡 Single Shard", "single"),
            ("📊 TF-IDF", "tfidf")
        ]
        
        for text, value in search_types:
            rb = tk.Radiobutton(options_frame, text=text, variable=self.search_type_var,
                               value=value, bg='#1e1e2e', fg='#ffffff',
                               selectcolor='#2d2d44', font=self.normal_font)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Search buttons
        btn_frame = tk.Frame(search_frame, bg='#1e1e2e')
        btn_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.search_btn = tk.Button(btn_frame, text="🔍 Search", command=self.do_search,
                                    bg='#00aa66', fg='white', font=self.header_font,
                                    padx=20, pady=5, bd=0, relief=tk.FLAT)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(btn_frame, text="🗑️ Clear Results", command=self.clear_results,
                                   bg='#664444', fg='white', font=self.normal_font,
                                   padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results area
        result_frame = tk.LabelFrame(tab, text=" Search Results ", 
                                     font=self.header_font, fg='#ffaa44',
                                     bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(result_frame, font=self.mono_font,
                                                      bg='#0d0d1a', fg='#cccccc',
                                                      insertbackground='white',
                                                      bd=0, relief=tk.FLAT)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure text tags
        self.results_text.tag_configure('title', foreground='#00ff88', font=('Segoe UI', 11, 'bold'))
        self.results_text.tag_configure('score', foreground='#ffaa44')
        self.results_text.tag_configure('content', foreground='#8888aa')
        self.results_text.tag_configure('header', foreground='#4488ff', font=('Segoe UI', 11, 'bold'))
        self.results_text.tag_configure('info', foreground='#6666aa')
        self.results_text.tag_configure('warning', foreground='#ff6644')
    
    def create_add_tab(self):
        """Create the Add Document tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📄 Add Document")
        
        form_frame = tk.LabelFrame(tab, text=" Document Details ", 
                                   font=self.header_font, fg='#00ff88',
                                   bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(form_frame, text="Title:", font=self.header_font,
                fg='#ffffff', bg='#1e1e2e').pack(anchor=tk.W, pady=(10, 5), padx=5)
        
        self.title_entry = tk.Entry(form_frame, width=60, font=self.normal_font,
                                    bg='#2d2d44', fg='#ffffff', insertbackground='white',
                                    bd=2, relief=tk.FLAT)
        self.title_entry.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        tk.Label(form_frame, text="Content:", font=self.header_font,
                fg='#ffffff', bg='#1e1e2e').pack(anchor=tk.W, pady=(0, 5), padx=5)
        
        self.content_text = scrolledtext.ScrolledText(form_frame, height=8,
                                                      font=self.normal_font,
                                                      bg='#2d2d44', fg='#ffffff',
                                                      insertbackground='white',
                                                      bd=2, relief=tk.FLAT)
        self.content_text.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        btn_frame = tk.Frame(form_frame, bg='#1e1e2e')
        btn_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.add_btn = tk.Button(btn_frame, text="📥 Add Document", command=self.do_add_document,
                                 bg='#0066aa', fg='white', font=self.header_font,
                                 padx=20, pady=5, bd=0, relief=tk.FLAT)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_form_btn = tk.Button(btn_frame, text="🗑️ Clear", command=self.clear_document_form,
                                        bg='#664444', fg='white', font=self.normal_font,
                                        padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.clear_form_btn.pack(side=tk.LEFT, padx=5)
        
        self.add_status = tk.Label(form_frame, text="", font=self.normal_font,
                                   bg='#1e1e2e', fg='#44ff44')
        self.add_status.pack(anchor=tk.W, pady=(10, 5), padx=5)
    
    def create_queue_tab(self):
        """Create the Queue tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⏳ Queue")
        
        queue_frame = tk.LabelFrame(tab, text=" Query Queue ", 
                                    font=self.header_font, fg='#ffaa44',
                                    bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        queue_frame.pack(fill=tk.X, padx=10, pady=5)
        
        input_frame = tk.Frame(queue_frame, bg='#1e1e2e')
        input_frame.pack(fill=tk.X, pady=5, padx=5)
        
        tk.Label(input_frame, text="Query:", font=self.header_font,
                fg='#ffffff', bg='#1e1e2e').pack(side=tk.LEFT, padx=(0, 10))
        
        self.queue_entry = tk.Entry(input_frame, width=40, font=self.normal_font,
                                    bg='#2d2d44', fg='#ffffff', insertbackground='white',
                                    bd=2, relief=tk.FLAT)
        self.queue_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(input_frame, text="Priority:", font=self.normal_font,
                fg='#ffffff', bg='#1e1e2e').pack(side=tk.LEFT, padx=(10, 5))
        
        self.priority_var = tk.StringVar(value="normal")
        self.priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                           values=['high', 'normal', 'low'], width=8)
        self.priority_combo.pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(queue_frame, bg='#1e1e2e')
        btn_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.enqueue_btn = tk.Button(btn_frame, text="📥 Enqueue", command=self.do_enqueue,
                                     bg='#0066aa', fg='white', font=self.normal_font,
                                     padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.enqueue_btn.pack(side=tk.LEFT, padx=5)
        
        self.process_btn = tk.Button(btn_frame, text="⚙️ Process Next", command=self.do_process_queue,
                                     bg='#aa6600', fg='white', font=self.normal_font,
                                     padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_queue_btn = tk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_queue_status,
                                           bg='#444466', fg='white', font=self.normal_font,
                                           padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.refresh_queue_btn.pack(side=tk.LEFT, padx=5)
        
        status_frame = tk.LabelFrame(tab, text=" Queue Status ", 
                                     font=self.header_font, fg='#44aaff',
                                     bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.queue_text = scrolledtext.ScrolledText(status_frame, font=self.mono_font,
                                                    bg='#0d0d1a', fg='#cccccc',
                                                    insertbackground='white',
                                                    bd=0, relief=tk.FLAT)
        self.queue_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.queue_text.tag_configure('header', foreground='#4488ff', font=('Segoe UI', 11, 'bold'))
        self.queue_text.tag_configure('info', foreground='#6666aa')
        self.queue_text.tag_configure('title', foreground='#ffaa44')
    
    def create_history_tab(self):
        """Create the History tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 History")
        
        control_frame = tk.Frame(tab, bg='#1e1e2e')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.back_btn = tk.Button(control_frame, text="⬅️ Back", command=self.do_back,
                                  bg='#0066aa', fg='white', font=self.normal_font,
                                  padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        self.forward_btn = tk.Button(control_frame, text="➡️ Forward", command=self.do_forward,
                                     bg='#0066aa', fg='white', font=self.normal_font,
                                     padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.forward_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_history_btn = tk.Button(control_frame, text="🔄 Refresh", command=self.refresh_history,
                                             bg='#444466', fg='white', font=self.normal_font,
                                             padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.refresh_history_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_history_btn = tk.Button(control_frame, text="🗑️ Clear", command=self.do_clear_history,
                                           bg='#664444', fg='white', font=self.normal_font,
                                           padx=15, pady=5, bd=0, relief=tk.FLAT)
        self.clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        history_frame = tk.LabelFrame(tab, text=" Search History (Stack Navigation) ", 
                                      font=self.header_font, fg='#44ff88',
                                      bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, font=self.mono_font,
                                                      bg='#0d0d1a', fg='#cccccc',
                                                      insertbackground='white',
                                                      bd=0, relief=tk.FLAT)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.history_text.tag_configure('back', foreground='#ff8844')
        self.history_text.tag_configure('current', foreground='#44ff44')
        self.history_text.tag_configure('forward', foreground='#4488ff')
        self.history_text.tag_configure('header', foreground='#4488ff', font=('Segoe UI', 11, 'bold'))
        self.history_text.tag_configure('info', foreground='#6666aa')
        self.history_text.tag_configure('content', foreground='#cccccc')
    
    def create_shards_tab(self):
        """Create the Shards tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔄 Shards")
        
        shard_frame = tk.LabelFrame(tab, text=" Shard Distribution ", 
                                    font=self.header_font, fg='#ff8844',
                                    bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        shard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.shard_text = scrolledtext.ScrolledText(shard_frame, font=self.mono_font,
                                                    bg='#0d0d1a', fg='#cccccc',
                                                    insertbackground='white',
                                                    bd=0, relief=tk.FLAT)
        self.shard_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.shard_text.tag_configure('header', foreground='#4488ff', font=('Segoe UI', 11, 'bold'))
        self.shard_text.tag_configure('title', foreground='#ffaa44')
        self.shard_text.tag_configure('info', foreground='#44ff88')
        self.shard_text.tag_configure('score', foreground='#ff6644')
        
        refresh_btn = tk.Button(tab, text="🔄 Refresh Shards", command=self.refresh_shards,
                                bg='#444466', fg='white', font=self.normal_font,
                                padx=15, pady=5, bd=0, relief=tk.FLAT)
        refresh_btn.pack(pady=5)
        
        self.refresh_shards()
    
    def create_stats_tab(self):
        """Create the Statistics tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Stats")
        
        stats_frame = tk.LabelFrame(tab, text=" System Statistics ", 
                                    font=self.header_font, fg='#44aaff',
                                    bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, font=self.mono_font,
                                                    bg='#0d0d1a', fg='#cccccc',
                                                    insertbackground='white',
                                                    bd=0, relief=tk.FLAT)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.stats_text.tag_configure('header', foreground='#4488ff', font=('Segoe UI', 11, 'bold'))
        self.stats_text.tag_configure('info', foreground='#44ff88')
        self.stats_text.tag_configure('title', foreground='#ffaa44')
        
        refresh_btn = tk.Button(tab, text="🔄 Refresh Stats", command=self.refresh_stats,
                                bg='#444466', fg='white', font=self.normal_font,
                                padx=15, pady=5, bd=0, relief=tk.FLAT)
        refresh_btn.pack(pady=5)
        
        self.refresh_stats()
    
    def create_benchmark_tab(self):
        """Create the Benchmark tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Benchmark")
        
        control_frame = tk.Frame(tab, bg='#1e1e2e')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.bench_btn = tk.Button(control_frame, text="▶️ Run Benchmarks", command=self.run_benchmarks,
                                   bg='#aa6600', fg='white', font=self.header_font,
                                   padx=20, pady=5, bd=0, relief=tk.FLAT)
        self.bench_btn.pack(side=tk.LEFT, padx=5)
        
        bench_frame = tk.LabelFrame(tab, text=" Benchmark Results ", 
                                    font=self.header_font, fg='#ff6644',
                                    bg='#1e1e2e', bd=2, relief=tk.GROOVE)
        bench_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.bench_text = scrolledtext.ScrolledText(bench_frame, font=self.mono_font,
                                                    bg='#0d0d1a', fg='#cccccc',
                                                    insertbackground='white',
                                                    bd=0, relief=tk.FLAT)
        self.bench_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.bench_text.tag_configure('header', foreground='#4488ff', font=('Segoe UI', 11, 'bold'))
        self.bench_text.tag_configure('title', foreground='#ffaa44')
        self.bench_text.tag_configure('info', foreground='#44ff88')
    
    def initialize_engine(self):
        """Initialize the search engine."""
        try:
            from main import DistributedSearchEngine
            self.engine = DistributedSearchEngine(num_shards=3)
            self.update_status("✅ Engine initialized with 3 shards")
            self.refresh_queue_status()
            self.refresh_history()
            self.refresh_shards()
            self.refresh_stats()
        except Exception as e:
            self.update_status(f"❌ Error initializing engine: {e}")
    
    def do_search(self):
        """Perform a search."""
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a search query")
            return
        
        try:
            top_k = int(self.top_k_var.get())
        except ValueError:
            top_k = 10
        
        search_type = self.search_type_var.get()
        
        self.update_status(f"🔍 Searching: '{query}' using {search_type}...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"🔍 Search Results for: '{query}'\n", 'header')
        self.results_text.insert(tk.END, f"📊 Search Type: {search_type.upper()}\n", 'info')
        self.results_text.insert(tk.END, "-" * 50 + "\n\n", 'info')
        
        start_time = time.time()
        
        try:
            if search_type == 'distributed':
                results = self.engine.search(query, top_k, distributed=True)
            elif search_type == 'single':
                results = self.engine.search(query, top_k, distributed=False)
            else:
                results = self.engine.search_ranked(query, top_k)
        except Exception as e:
            self.results_text.insert(tk.END, f"❌ Error: {e}\n", 'warning')
            self.update_status(f"❌ Error: {e}")
            return
        
        elapsed = time.time() - start_time
        
        if not results:
            self.results_text.insert(tk.END, "😕 No results found.\n", 'content')
        else:
            self.results_text.insert(tk.END, f"✅ Found {len(results)} results in {elapsed:.3f}s\n\n", 'info')
            for i, doc in enumerate(results[:top_k], 1):
                title = doc.get('title', 'Unknown')
                score = doc.get('score', 'N/A')
                self.results_text.insert(tk.END, f"{i}. ", 'info')
                self.results_text.insert(tk.END, f"{title}\n", 'title')
                self.results_text.insert(tk.END, f"   📊 Score: {score}\n", 'score')
                if 'content_preview' in doc:
                    self.results_text.insert(tk.END, f"   📄 {doc['content_preview']}\n", 'content')
                self.results_text.insert(tk.END, "\n")
        
        self.update_status(f"✅ Search completed in {elapsed:.3f}s")
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.update_status("🗑️ Results cleared")
    
    def do_add_document(self):
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showwarning("Missing Title", "Please enter a document title")
            return
        
        if not content:
            messagebox.showwarning("Missing Content", "Please enter document content")
            return
        
        try:
            doc_id = self.engine.add_document(title, content)
            self.add_status.config(text=f"✅ Document '{title}' added with ID: {doc_id}", fg='#44ff44')
            self.clear_document_form()
            self.update_status(f"✅ Document '{title}' added (ID: {doc_id})")
            self.refresh_stats()
            self.refresh_shards()
        except Exception as e:
            self.add_status.config(text=f"❌ Error: {e}", fg='#ff4444')
            self.update_status(f"❌ Error adding document: {e}")
    
    def clear_document_form(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.add_status.config(text="")
    
    def do_enqueue(self):
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        query = self.queue_entry.get().strip()
        priority = self.priority_var.get()
        
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a query to queue")
            return
        
        qid = self.engine.enqueue_search(query, priority)
        self.update_status(f"✅ Query queued with ID: {qid} (priority: {priority})")
        self.queue_entry.delete(0, tk.END)
        self.refresh_queue_status()
    
    def do_process_queue(self):
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        results = self.engine.process_next_query()
        
        if results:
            self.update_status(f"✅ Processed query, found {len(results)} results")
            self.refresh_queue_status()
            self.notebook.select(0)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"📋 Processed Queue Result\n", 'header')
            self.results_text.insert(tk.END, "-" * 50 + "\n\n", 'info')
            for i, doc in enumerate(results[:10], 1):
                self.results_text.insert(tk.END, f"{i}. {doc.get('title', 'Unknown')} (score: {doc.get('score', 'N/A')})\n", 'title')
        else:
            self.update_status("⏳ No pending queries in queue")
            messagebox.showinfo("Queue Empty", "No pending queries to process")
    
    def refresh_queue_status(self):
        if self.engine is None:
            return
        
        self.queue_text.delete(1.0, tk.END)
        stats = self.engine.query_queue.get_query_stats()
        self.queue_text.insert(tk.END, "=== QUEUE STATUS ===\n\n", 'header')
        self.queue_text.insert(tk.END, f"📊 Total Queries: {stats['total_queries']}\n", 'info')
        self.queue_text.insert(tk.END, f"⏳ Pending: {stats['pending']}\n", 'info')
        self.queue_text.insert(tk.END, f"✅ Processed: {stats['processed']}\n", 'info')
        self.queue_text.insert(tk.END, f"⏱️ Avg Queue Time: {stats['avg_queue_time']:.4f}s\n\n", 'info')
        self.queue_text.insert(tk.END, "--- Pending Queues ---\n", 'header')
        self.queue_text.insert(tk.END, f"🔴 High Priority: {len(self.engine.query_queue.high_priority_queue)}\n", 'info')
        self.queue_text.insert(tk.END, f"🟡 Normal Priority: {len(self.engine.query_queue.normal_queue)}\n", 'info')
        self.queue_text.insert(tk.END, f"🟢 Low Priority: {len(self.engine.query_queue.low_priority_queue)}\n", 'info')
    
    def do_back(self):
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        result, msg = self.engine.history.back()
        if result:
            self.update_status(f"⬅️ Back: {msg}")
            self.refresh_history()
        else:
            self.update_status(f"⬅️ Back: {msg}")
            messagebox.showinfo("History", msg)
    
    def do_forward(self):
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        result, msg = self.engine.history.forward()
        if result:
            self.update_status(f"➡️ Forward: {msg}")
            self.refresh_history()
        else:
            self.update_status(f"➡️ Forward: {msg}")
            messagebox.showinfo("History", msg)
    
    def refresh_history(self):
        if self.engine is None:
            return
        
        self.history_text.delete(1.0, tk.END)
        history = self.engine.history.get_all_history()
        self.history_text.insert(tk.END, "=== SEARCH HISTORY (Stack Navigation) ===\n\n", 'header')
        
        if not history:
            self.history_text.insert(tk.END, "📭 No history available\n", 'info')
            return
        
        for i, entry in enumerate(history):
            entry_type = entry['type']
            text = entry['text']
            results_count = len(entry['results'])
            tag = 'back' if entry_type == 'back' else 'forward' if entry_type == 'forward' else 'current'
            icon = '⬅️' if entry_type == 'back' else '➡️' if entry_type == 'forward' else '📍'
            self.history_text.insert(tk.END, f"{i+1}. {icon} [{entry_type.upper()}] ", tag)
            self.history_text.insert(tk.END, f"{text}", 'current' if entry_type == 'current' else 'content')
            self.history_text.insert(tk.END, f" ({results_count} results)\n", 'info')
        
        self.history_text.insert(tk.END, "\n", 'info')
        self.history_text.insert(tk.END, f"📚 Back stack: {len(self.engine.history.back_stack)} queries\n", 'info')
        self.history_text.insert(tk.END, f"📚 Forward stack: {len(self.engine.history.forward_stack)} queries\n", 'info')
    
    def do_clear_history(self):
        if self.engine is None:
            return
        self.engine.history.clear()
        self.refresh_history()
        self.update_status("🗑️ History cleared")
    
    def refresh_shards(self):
        if self.engine is None:
            return
        
        self.shard_text.delete(1.0, tk.END)
        stats = self.engine.shard_manager.get_shard_stats()
        balance = self.engine.shard_manager.get_balance_score()
        
        self.shard_text.insert(tk.END, "=== SHARD DISTRIBUTION ===\n\n", 'header')
        self.shard_text.insert(tk.END, f"🔄 Number of Shards: {self.engine.shard_manager.num_shards}\n", 'info')
        self.shard_text.insert(tk.END, f"📊 Balance Score (lower=better): {balance:.2f}\n\n", 'info')
        
        for stat in stats:
            self.shard_text.insert(tk.END, f"┌─ 📦 Shard {stat['shard_id']} ────────────────\n", 'title')
            self.shard_text.insert(tk.END, f"│  📝 Terms: {stat['terms']}\n")
            self.shard_text.insert(tk.END, f"│  📄 Documents: {stat['documents']}\n")
            self.shard_text.insert(tk.END, f"│  💾 Memory Estimate: {stat['memory_estimate']} postings\n")
            self.shard_text.insert(tk.END, f"└─────────────────────────────────\n\n")
        
        if balance < 1000:
            self.shard_text.insert(tk.END, "✅ Shard distribution is well balanced\n", 'info')
        else:
            self.shard_text.insert(tk.END, "⚠️ Shard distribution could be improved\n", 'score')
    
    def refresh_stats(self):
        if self.engine is None:
            return
        
        self.stats_text.delete(1.0, tk.END)
        stats = self.engine.get_stats()
        
        self.stats_text.insert(tk.END, "=== SYSTEM STATISTICS ===\n\n", 'header')
        self.stats_text.insert(tk.END, f"📄 Documents: {stats['documents']}\n", 'info')
        self.stats_text.insert(tk.END, f"📝 Unique Terms: {stats['terms']}\n", 'info')
        self.stats_text.insert(tk.END, f"🔄 Shards: {len(stats['shards'])}\n", 'info')
        self.stats_text.insert(tk.END, f"⏳ Pending Queries: {stats['pending_queries']}\n", 'info')
        self.stats_text.insert(tk.END, f"📜 History Size: {stats['history_size']}\n", 'info')
        
        self.stats_text.insert(tk.END, "\n--- Data Structures in Use ---\n", 'header')
        structures = [
            ("🗂️ Hash Table", "Document storage, Inverted index", "O(1) lookup"),
            ("📊 Heap", "Top-K ranking, Result merging", "O(n log k)"),
            ("⏳ Queue", "Query buffering", "O(1) enqueue/dequeue"),
            ("📚 Stack", "Search history navigation", "O(1) push/pop"),
            ("🔄 Consistent Hashing", "Shard distribution", "O(1) assignment"),
        ]
        
        for name, purpose, complexity in structures:
            self.stats_text.insert(tk.END, f"  • {name}: {purpose} ({complexity})\n", 'info')
    
    def run_benchmarks(self):
        """Run benchmarks in a separate thread."""
        if self.engine is None:
            self.initialize_engine()
            if self.engine is None:
                return
        
        self.update_status("⚡ Running benchmarks...")
        self.bench_text.delete(1.0, tk.END)
        self.bench_text.insert(tk.END, "⚡ Running benchmarks... Please wait.\n", 'header')
        self.bench_btn.config(state=tk.DISABLED)
        
        def run_bench():
            try:
                from benchmark import Benchmark
                bm = Benchmark(self.engine)
                results = bm.run_all_benchmarks()
                self.root.after(0, lambda: self.display_benchmark_results(results))
            except Exception as e:
                error_msg = str(e)  # ← FIX: Store error message
                self.root.after(0, lambda: self.display_benchmark_error(error_msg))  # ← FIX: Pass stored value
        
        threading.Thread(target=run_bench, daemon=True).start()
    
    def display_benchmark_results(self, results):
        """Display benchmark results."""
        self.bench_text.delete(1.0, tk.END)
        self.bench_text.insert(tk.END, "=== BENCHMARK RESULTS ===\n\n", 'header')
        
        for key, value in results.items():
            self.bench_text.insert(tk.END, f"▶ {key.upper()}\n", 'title')
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, float):
                        self.bench_text.insert(tk.END, f"   {k}: {v:.4f}\n")
                    else:
                        self.bench_text.insert(tk.END, f"   {k}: {v}\n")
            else:
                self.bench_text.insert(tk.END, f"   {value}\n")
            self.bench_text.insert(tk.END, "\n")
        
        self.update_status("✅ Benchmarks completed")
        self.bench_btn.config(state=tk.NORMAL)
    
    def display_benchmark_error(self, error):
        """Display benchmark error."""
        self.bench_text.delete(1.0, tk.END)
        self.bench_text.insert(tk.END, f"❌ Error running benchmarks: {error}\n", 'warning')
        self.update_status(f"❌ Benchmark error: {error}")
        self.bench_btn.config(state=tk.NORMAL)
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_bar.config(text=message)
        self.root.update()
    
    def on_closing(self):
        """Handle window closing."""
        self.root.destroy()
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()


if __name__ == "__main__":
    app = SearchEngineGUI()
    app.run()