import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from pathlib import Path
import json
from datetime import datetime
import hashlib
import os
import subprocess
import platform

from disk_image_generator import DiskImageGenerator
from file_carver import FileCarver
from file_parser import FileParser
from binwalk_analyzer import BinwalkAnalyzer
from verify_files import verify_file
from automated_workflow import AutomatedForensicsWorkflow

__version__ = "2.0.0"
__author__ = "Parth Thakar"
__project__ = "Forensics Analyzer - Major Project"

# Constants for scroll configuration
WINDOWS_SCROLL_DIVISOR = 120  # Windows mousewheel delta divisor

class ForensicsAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{__project__} v{__version__}")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Try to set icon (if available)
        try:
            # This will work if an icon file exists
            self.root.iconbitmap('icon.ico')
        except (tk.TclError, FileNotFoundError):
            pass
        
        # Variables
        self.is_running = False
        self.base_dir = Path(__file__).parent.parent
        self.current_analysis = {}
        
        # Style configuration
        self.setup_styles()
        
        # Show splash screen
        self.show_splash_screen()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Keyboard shortcuts
        self.setup_shortcuts()
        
    def _setup_scrollable_canvas(self, canvas, canvas_frame, content_frame):
        """Setup scrolling configuration for a canvas with content.
        
        Args:
            canvas: The canvas widget
            canvas_frame: The canvas window frame ID
            content_frame: The frame containing the content
        """
        # Configure scroll region when content changes
        def configure_scroll(event):
            bbox = canvas.bbox('all')
            # bbox returns None when canvas is empty, only configure if valid
            if bbox:
                canvas.configure(scrollregion=bbox)
        
        content_frame.bind('<Configure>', configure_scroll)
        
        # Configure canvas width to match window
        def resize_canvas(event):
            try:
                canvas.itemconfig(canvas_frame, width=event.width)
            except tk.TclError:
                # Ignore if canvas_frame ID is invalid or canvas has been destroyed
                pass
        
        canvas.bind('<Configure>', resize_canvas)
        
        # Add cross-platform mousewheel support
        self._create_mousewheel_binding(canvas)
    
    def _create_mousewheel_binding(self, canvas):
        """Create cross-platform mousewheel binding for a canvas.
        
        Args:
            canvas: The canvas widget to bind mousewheel scrolling to
        """
        def on_mousewheel(event):
            # Cross-platform mousewheel handling
            if platform.system() == 'Windows':
                canvas.yview_scroll(int(-1*(event.delta/WINDOWS_SCROLL_DIVISOR)), "units")
            elif platform.system() == 'Darwin':  # macOS
                canvas.yview_scroll(int(-1*event.delta), "units")
            else:  # Linux
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        # Bind mousewheel events based on platform
        if platform.system() == 'Linux':
            canvas.bind("<Button-4>", on_mousewheel)
            canvas.bind("<Button-5>", on_mousewheel)
        else:
            canvas.bind("<MouseWheel>", on_mousewheel)
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors - Modern dark theme
        bg_color = '#1e1e1e'
        fg_color = '#e0e0e0'
        accent_color = '#00bcd4'  # Cyan accent
        secondary_color = '#667eea'  # Purple
        success_color = '#4caf50'  # Green
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 28, 'bold'), foreground=accent_color)
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'), foreground=accent_color)
        style.configure('Subtitle.TLabel', font=('Segoe UI', 11), foreground='#b0b0b0')
        
        # Buttons
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=8)
        style.map('TButton', background=[('active', accent_color)])
        style.configure('Accent.TButton', background=accent_color, foreground='white', padding=10)
        style.map('Accent.TButton', 
                 background=[('active', secondary_color), ('pressed', secondary_color)])
        
        # Notebook (tabs)
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[20, 10])
        style.map('TNotebook.Tab', 
                 background=[('selected', accent_color)],
                 foreground=[('selected', 'white')])
        
        # LabelFrame
        style.configure('TLabelframe', background=bg_color, foreground=fg_color, borderwidth=2)
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'), foreground=accent_color)
        
        # Entry
        style.configure('TEntry', fieldbackground='#2d2d2d', foreground=fg_color, borderwidth=1)
        
        # Treeview
        style.configure('Treeview', background='#2d2d2d', foreground=fg_color, 
                       fieldbackground='#2d2d2d', borderwidth=0)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), 
                       background=accent_color, foreground='white')
        style.map('Treeview', background=[('selected', accent_color)])
    
    def show_splash_screen(self):
        """Show splash screen on startup"""
        splash = tk.Toplevel(self.root)
        splash.title("Loading...")
        splash.geometry("500x350")
        splash.configure(bg='#1e1e1e')
        splash.overrideredirect(True)
        
        # Center the splash screen
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (500 // 2)
        y = (splash.winfo_screenheight() // 2) - (350 // 2)
        splash.geometry(f"500x350+{x}+{y}")
        
        # Content
        frame = tk.Frame(splash, bg='#1e1e1e')
        frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Icon/Logo (using text for now)
        logo = tk.Label(frame, text="🔍", font=('Segoe UI', 80), bg='#1e1e1e', fg='#00bcd4')
        logo.pack(pady=20)
        
        title = tk.Label(frame, text=__project__, 
                        font=('Segoe UI', 20, 'bold'), bg='#1e1e1e', fg='#00bcd4')
        title.pack()
        
        version = tk.Label(frame, text=f"Version {__version__}", 
                          font=('Segoe UI', 12), bg='#1e1e1e', fg='#b0b0b0')
        version.pack(pady=5)
        
        author = tk.Label(frame, text=f"Developed by {__author__}", 
                         font=('Segoe UI', 10), bg='#1e1e1e', fg='#808080')
        author.pack(pady=5)
        
        loading = tk.Label(frame, text="Loading...", 
                          font=('Segoe UI', 10), bg='#1e1e1e', fg='#00bcd4')
        loading.pack(pady=20)
        
        # Close splash after 2 seconds
        self.root.after(2000, splash.destroy)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root, bg='#2d2d2d', fg='white', activebackground='#00bcd4')
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white', activebackground='#00bcd4')
        file_menu.add_command(label="New Analysis", command=self.new_analysis, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Output Folder", command=self.open_output_folder, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white', activebackground='#00bcd4')
        tools_menu.add_command(label="Calculate File Hash", command=self.calculate_hash)
        tools_menu.add_command(label="Verify Carved Files", command=self.verify_all_files)
        tools_menu.add_command(label="Clear Console", command=self.clear_console, accelerator="Ctrl+L")
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white', activebackground='#00bcd4')
        view_menu.add_command(label="Refresh Results", command=self.refresh_results, accelerator="F5")
        view_menu.add_command(label="Full Screen", command=self.toggle_fullscreen, accelerator="F11")
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white', activebackground='#00bcd4')
        help_menu.add_command(label="User Guide", command=self.show_user_guide, accelerator="F1")
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.new_analysis())
        self.root.bind('<Control-o>', lambda e: self.open_output_folder())
        self.root.bind('<Control-e>', lambda e: self.export_report())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-l>', lambda e: self.clear_console())
        self.root.bind('<F5>', lambda e: self.refresh_results())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F1>', lambda e: self.show_user_guide())
        
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        # Left side - Title
        left_frame = ttk.Frame(header_frame)
        left_frame.pack(side='left')
        
        title_container = ttk.Frame(left_frame)
        title_container.pack(side='left')
        
        title = ttk.Label(title_container, text="🔍 Forensics Analyzer", style='Header.TLabel')
        title.pack(side='left')
        
        subtitle = ttk.Label(header_frame, 
                            text="Professional Digital Forensics & File Carving Tool", 
                            style='Subtitle.TLabel')
        subtitle.pack(pady=5)
        
        # Right side - Quick info
        right_frame = ttk.Frame(header_frame)
        right_frame.pack(side='right')
        
        info_text = f"v{__version__} | {__author__}"
        info_label = ttk.Label(right_frame, text=info_text, font=('Segoe UI', 9))
        info_label.pack()
        
    def create_main_content(self):
        """Create main content area"""
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: Generate & Carve
        self.create_generate_tab()
        
        # Tab 2: Results
        self.create_results_tab()
        
        # Tab 3: Settings
        self.create_settings_tab()
        
    def create_generate_tab(self):
        """Create the generate and carve tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  Generate & Carve  ")
        
        # Left panel - Configuration with scrollbar
        left_container = ttk.Frame(tab)
        left_container.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(left_container, bg='#1e1e1e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_container, orient='vertical', command=canvas.yview)
        
        # Frame inside canvas to hold all content
        left_frame = ttk.Frame(canvas)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Create window in canvas
        canvas_frame = canvas.create_window((0, 0), window=left_frame, anchor='nw')
        
        # Setup scrolling and mousewheel support
        self._setup_scrollable_canvas(canvas, canvas_frame, left_frame)
        
        # Automated Workflow Section
        auto_frame = ttk.LabelFrame(left_frame, text="🚀 Automated Workflow (Recommended)", padding=15)
        auto_frame.pack(fill='x', pady=5)
        
        ttk.Label(auto_frame, text="Source Path:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.auto_source_var = tk.StringVar(value="")
        auto_source_entry = ttk.Entry(auto_frame, textvariable=self.auto_source_var, width=40)
        auto_source_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        browse_source_btn = ttk.Button(auto_frame, text="Browse", command=self.browse_auto_source)
        browse_source_btn.grid(row=0, column=2, pady=5, padx=5)
        
        ttk.Label(auto_frame, text="Output Directory:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.auto_output_var = tk.StringVar(value=str(self.base_dir / "output" / "automated"))
        auto_output_entry = ttk.Entry(auto_frame, textvariable=self.auto_output_var, width=40)
        auto_output_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        browse_auto_out_btn = ttk.Button(auto_frame, text="Browse", command=self.browse_auto_output)
        browse_auto_out_btn.grid(row=1, column=2, pady=5, padx=5)
        
        self.recursive_var = tk.BooleanVar(value=False)
        recursive_cb = ttk.Checkbutton(auto_frame, text="Include subdirectories (recursive)", 
                                       variable=self.recursive_var)
        recursive_cb.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        
        auto_btn = ttk.Button(auto_frame, text="⚡ Run Complete Workflow", 
                             command=self.run_automated_workflow, style='Accent.TButton')
        auto_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')
        
        # Info label
        info_label = ttk.Label(auto_frame, 
                              text="Automatically: Calculate size → Create .dd → Embed files → Carve → Verify",
                              font=('Segoe UI', 9), foreground='#00bcd4')
        info_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        auto_frame.columnconfigure(1, weight=1)
        
        # Separator
        sep = ttk.Separator(left_frame, orient='horizontal')
        sep.pack(fill='x', pady=15)
        
        ttk.Label(left_frame, text="Manual Mode (Advanced)", 
                 font=('Segoe UI', 11, 'bold'), foreground='#b0b0b0').pack(anchor='w', pady=5)
        
        # Generate Section
        generate_frame = ttk.LabelFrame(left_frame, text="Step 1: Generate Disk Image", padding=15)
        generate_frame.pack(fill='x', pady=5)
        
        ttk.Label(generate_frame, text="Image Size (MB):").grid(row=0, column=0, sticky='w', pady=5)
        self.size_var = tk.StringVar(value="10")
        size_entry = ttk.Entry(generate_frame, textvariable=self.size_var, width=20)
        size_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        ttk.Label(generate_frame, text="Output Path:").grid(row=1, column=0, sticky='w', pady=5)
        self.output_path_var = tk.StringVar(value=str(self.base_dir / "evidence" / "evidence.dd"))
        output_entry = ttk.Entry(generate_frame, textvariable=self.output_path_var, width=40)
        output_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        browse_btn = ttk.Button(generate_frame, text="Browse", command=self.browse_output)
        browse_btn.grid(row=1, column=2, pady=5, padx=5)
        
        # File types to embed
        ttk.Label(generate_frame, text="Files to Embed:").grid(row=2, column=0, sticky='nw', pady=5)
        
        files_frame = ttk.Frame(generate_frame)
        files_frame.grid(row=2, column=1, columnspan=2, sticky='ew', pady=5)
        
        self.file_types = {
            'jpg': tk.BooleanVar(value=True),
            'png': tk.BooleanVar(value=True),
            'pdf': tk.BooleanVar(value=True),
            'txt': tk.BooleanVar(value=True),
            'docx': tk.BooleanVar(value=True),
            'mp3': tk.BooleanVar(value=True)
        }
        
        for i, (ftype, var) in enumerate(self.file_types.items()):
            cb = ttk.Checkbutton(files_frame, text=ftype.upper(), variable=var)
            cb.grid(row=i//3, column=i%3, sticky='w', padx=5, pady=2)
        
        generate_btn = ttk.Button(generate_frame, text="🔧 Generate Disk Image", 
                                 command=self.generate_image, style='Accent.TButton')
        generate_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')
        
        generate_frame.columnconfigure(1, weight=1)
        
        # Carve Section
        carve_frame = ttk.LabelFrame(left_frame, text="Step 2: Carve Files", padding=15)
        carve_frame.pack(fill='x', pady=5)
        
        ttk.Label(carve_frame, text="Disk Image:").grid(row=0, column=0, sticky='w', pady=5)
        self.carve_input_var = tk.StringVar(value=str(self.base_dir / "evidence" / "evidence.dd"))
        carve_entry = ttk.Entry(carve_frame, textvariable=self.carve_input_var, width=40)
        carve_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        browse_carve_btn = ttk.Button(carve_frame, text="Browse", command=self.browse_carve_input)
        browse_carve_btn.grid(row=0, column=2, pady=5, padx=5)
        
        ttk.Label(carve_frame, text="Output Directory:").grid(row=1, column=0, sticky='w', pady=5)
        self.carve_output_var = tk.StringVar(value=str(self.base_dir / "output" / "carved_files"))
        carve_out_entry = ttk.Entry(carve_frame, textvariable=self.carve_output_var, width=40)
        carve_out_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        browse_out_btn = ttk.Button(carve_frame, text="Browse", command=self.browse_carve_output)
        browse_out_btn.grid(row=1, column=2, pady=5, padx=5)
        
        ttk.Label(carve_frame, text="Min File Size (bytes):").grid(row=2, column=0, sticky='w', pady=5)
        self.min_size_var = tk.StringVar(value="1024")
        min_size_entry = ttk.Entry(carve_frame, textvariable=self.min_size_var, width=20)
        min_size_entry.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        
        self.carve_btn = ttk.Button(carve_frame, text="🔪 Start Carving", 
                                    command=self.start_carving, style='Accent.TButton')
        self.carve_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')
        
        carve_frame.columnconfigure(1, weight=1)
        
        # Binwalk Section
        binwalk_frame = ttk.LabelFrame(left_frame, text="Step 3: Binwalk Analysis", padding=15)
        binwalk_frame.pack(fill='x', pady=5)
        
        self.binwalk_btn = ttk.Button(binwalk_frame, text="🔬 Run Binwalk Analysis", 
                                      command=self.run_binwalk, style='Accent.TButton')
        self.binwalk_btn.pack(fill='x', pady=5)
        
        # Right panel - Console output
        right_frame = ttk.Frame(tab)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        console_label = ttk.Label(right_frame, text="Console Output", style='Title.TLabel')
        console_label.pack(anchor='w', pady=5)
        
        self.console = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                 bg='#1e1e1e', fg='#00ff00',
                                                 font=('Consolas', 9), height=35)
        self.console.pack(fill='both', expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(right_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
    def create_results_tab(self):
        """Create results viewing tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  Results & Analysis  ")
        
        # Top buttons and search
        top_frame = ttk.Frame(tab)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        # Buttons frame
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side='left', fill='x')
        
        ttk.Button(btn_frame, text="📁 Open Output Folder", 
                  command=self.open_output_folder).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh Results", 
                  command=self.refresh_results).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📊 Export Report", 
                  command=self.export_report).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔍 Preview File", 
                  command=self.preview_selected_file).pack(side='left', padx=5)
        
        # Search frame
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side='right')
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_results())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Results tree with scrollbars
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Name', 'Type', 'Size', 'Valid', 'Hash', 'Path')
        self.results_tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings', height=20)
        
        self.results_tree.heading('#0', text='ID')
        self.results_tree.column('#0', width=50)
        
        column_widths = {'Name': 200, 'Type': 80, 'Size': 100, 'Valid': 60, 'Hash': 180, 'Path': 300}
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=column_widths.get(col, 150))
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.results_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Double-click to preview
        self.results_tree.bind('<Double-1>', lambda e: self.preview_selected_file())
        
        # Statistics with charts
        stats_frame = ttk.LabelFrame(tab, text="Analysis Statistics", padding=15)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="No results yet. Run analysis first.", 
                                     font=('Segoe UI', 10))
        self.stats_label.pack()
        
    def create_settings_tab(self):
        """Create settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  Settings & Help  ")
        
        # Create notebook for sub-tabs
        sub_notebook = ttk.Notebook(tab)
        sub_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Settings sub-tab
        settings_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(settings_tab, text="Settings")
        
        settings_frame = ttk.LabelFrame(settings_tab, text="Application Settings", padding=20)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Theme
        ttk.Label(settings_frame, text="Theme:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        theme_var = tk.StringVar(value="Dark")
        theme_combo = ttk.Combobox(settings_frame, textvariable=theme_var, 
                                   values=['Dark', 'Light'], state='readonly', width=20)
        theme_combo.grid(row=0, column=1, sticky='w', pady=10, padx=10)
        
        # Default paths
        ttk.Label(settings_frame, text="Evidence Directory:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=10)
        ttk.Label(settings_frame, text=str(self.base_dir / "evidence")).grid(row=1, column=1, sticky='w', pady=10, padx=10)
        
        ttk.Label(settings_frame, text="Output Directory:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=10)
        ttk.Label(settings_frame, text=str(self.base_dir / "output")).grid(row=2, column=1, sticky='w', pady=10, padx=10)
        
        # User Guide sub-tab
        guide_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(guide_tab, text="User Guide")
        
        guide_frame = ttk.Frame(guide_tab)
        guide_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        guide_text = scrolledtext.ScrolledText(guide_frame, wrap=tk.WORD, 
                                              bg='#2d2d2d', fg='#e0e0e0',
                                              font=('Segoe UI', 10), height=25)
        guide_text.pack(fill='both', expand=True)
        
        user_guide = """
╔══════════════════════════════════════════════════════════════════════╗
║           FORENSICS ANALYZER - USER GUIDE                            ║
╚══════════════════════════════════════════════════════════════════════╝

OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Forensics Analyzer is a comprehensive digital forensics tool for file 
carving and analysis. It supports generating disk images, extracting 
files using signature-based carving, and performing detailed analysis.

GETTING STARTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Generate a Disk Image
   • Navigate to the "Generate & Carve" tab
   • Configure the image size (in MB)
   • Select file types to embed (JPG, PNG, PDF, TXT, DOCX, MP3)
   • Choose output path or use default
   • Click "Generate Disk Image"

Step 2: Carve Files from Disk Image
   • Select the disk image file (evidence.dd)
   • Choose output directory for carved files
   • Set minimum file size threshold (default: 1024 bytes)
   • Click "Start Carving"
   
Step 3: Run Binwalk Analysis (Optional)
   • Requires binwalk installation: pip install binwalk
   • Click "Run Binwalk Analysis"
   • Advanced binary analysis and signature detection

FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File Carving
   • Signature-based extraction
   • Supports multiple file formats:
     - Images: JPG, PNG, GIF, BMP, TIFF
     - Documents: PDF, DOCX, XLSX, PPTX
     - Archives: ZIP, RAR
     - Media: MP4, MP3, AVI, WAV
     - Executables: EXE, ELF

Analysis & Reporting
   • File validation and integrity checking
   • Hash calculation (MD5, SHA-256)
   • Detailed metadata extraction
   • Export reports in JSON, TXT, HTML formats
   • Statistical analysis and visualization

Advanced Tools
   • Binwalk integration for firmware analysis
   • File preview capability
   • Search and filter results
   • Batch processing support

KEYBOARD SHORTCUTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Ctrl+N    - New Analysis
   Ctrl+O    - Open Output Folder
   Ctrl+E    - Export Report
   Ctrl+L    - Clear Console
   Ctrl+Q    - Quit Application
   F1        - Show User Guide
   F5        - Refresh Results
   F11       - Toggle Full Screen

TIPS & BEST PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Start with smaller disk images (10-50MB) for testing
   • Use appropriate minimum file size to filter noise
   • Always verify carved files before analysis
   • Export reports for documentation and evidence
   • Keep backups of original evidence files
   • Use Binwalk for advanced forensics cases

TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Q: Binwalk not found?
   A: Install with: pip install binwalk
   
   Q: Permission errors?
   A: Run with administrator/sudo privileges for disk access
   
   Q: Memory issues with large images?
   A: Process in smaller chunks or increase system memory
   
   Q: No files carved?
   A: Check minimum file size threshold and disk image validity

SUPPORT & DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For additional help, issues, and documentation:
   • GitHub: https://github.com/parththakar2003/major-project
   • Version: {version}
   • Author: {author}

© 2025 Forensics Analyzer - All Rights Reserved
        """.format(version=__version__, author=__author__)
        
        guide_text.insert('1.0', user_guide)
        guide_text.config(state='disabled')  # Make read-only
        
        # About sub-tab
        about_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(about_tab, text="About")
        
        # Add scrolling to about section
        about_canvas = tk.Canvas(about_tab, bg='#1e1e1e', highlightthickness=0)
        about_scrollbar = ttk.Scrollbar(about_tab, orient='vertical', command=about_canvas.yview)
        about_scrollbar.pack(side='right', fill='y')
        about_canvas.pack(side='left', fill='both', expand=True)
        about_canvas.configure(yscrollcommand=about_scrollbar.set)
        
        about_content = ttk.Frame(about_canvas)
        about_canvas_frame = about_canvas.create_window((0, 0), window=about_content, anchor='nw')
        
        about_frame = ttk.LabelFrame(about_content, text="About This Application", padding=20)
        about_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        about_text = f"""
🔍 {__project__}

Version: {__version__}
Author: {__author__}

A comprehensive digital forensics and file carving analysis tool
designed for educational and professional use in computer forensics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY FEATURES

• Disk Image Generation
  Create synthetic disk images with embedded files for testing
  
• File Carving
  Signature-based extraction of files from disk images
  
• File Validation & Parsing
  Automatic validation and metadata extraction
  
• Binwalk Integration
  Advanced binary analysis and firmware examination
  
• Comprehensive Reporting
  Export detailed reports in multiple formats
  
• Hash Calculation
  MD5 and SHA-256 hash generation for evidence integrity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNOLOGY STACK

• Language: Python 3.8+
• GUI Framework: tkinter (built-in)
• Threading: Multi-threaded for responsive UI
• File Signatures: Custom signature database
• Carving Algorithm: Header/footer matching with validation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUPPORTED FILE TYPES

Images: JPG, PNG, GIF, BMP, TIFF
Documents: PDF, DOCX, XLSX, PPTX
Archives: ZIP, RAR
Executables: EXE, ELF
Media: MP4, MP3, AVI, WAV

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

© 2025 Forensics Analyzer
All Rights Reserved

This tool is designed for educational purposes and legitimate 
forensics investigations. Users must comply with applicable laws 
and regulations when using this software.
        """
        
        about_label = ttk.Label(about_frame, text=about_text, justify='left', 
                               font=('Segoe UI', 10))
        about_label.pack()
        
        # Setup scrolling and mousewheel support
        self._setup_scrollable_canvas(about_canvas, about_canvas_frame, about_content)
        
    def create_footer(self):
        """Create footer with status"""
        footer = ttk.Frame(self.root)
        footer.pack(fill='x', padx=20, pady=10)
        
        self.status_label = ttk.Label(footer, text="Ready", font=('Segoe UI', 9))
        self.status_label.pack(side='left')
        
        time_label = ttk.Label(footer, text=f"© 2025 Forensics Analyzer", 
                              font=('Segoe UI', 9))
        time_label.pack(side='right')
        
    # Event handlers
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".dd",
            filetypes=[("Disk Image", "*.dd"), ("All Files", "*.*")]
        )
        if filename:
            self.output_path_var.set(filename)
            
    def browse_carve_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Disk Image", "*.dd"), ("All Files", "*.*")]
        )
        if filename:
            self.carve_input_var.set(filename)
            
    def browse_carve_output(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.carve_output_var.set(dirname)
    
    def browse_auto_source(self):
        """Browse for automated workflow source path"""
        path = filedialog.askdirectory(title="Select Source Directory")
        if not path:
            # Try file selection if directory not selected
            path = filedialog.askopenfilename(title="Select Source File")
        if path:
            self.auto_source_var.set(path)
    
    def browse_auto_output(self):
        """Browse for automated workflow output directory"""
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.auto_output_var.set(dirname)
            
    def log(self, message):
        """Log message to console"""
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def generate_image(self):
        """Generate disk image"""
        if self.is_running:
            messagebox.showwarning("Busy", "Another operation is in progress!")
            return
            
        self.is_running = True
        self.progress.start()
        
        def task():
            try:
                self.log("=" * 60)
                self.log("GENERATING DISK IMAGE")
                self.log("=" * 60)
                
                generator = DiskImageGenerator()
                
                # Add selected file types
                sample_files = []
                for ftype, var in self.file_types.items():
                    if var.get():
                        if ftype == 'txt':
                            sample_files.append({
                                "type": ftype,
                                "content": "This is a forensics test document."
                            })
                        else:
                            sample_files.append({
                                "type": ftype,
                                "size": 50000
                            })
                
                for file_spec in sample_files:
                    generator.add_file(file_spec)
                    self.log(f"[+] Added {file_spec['type']} file")
                
                output_path = Path(self.output_path_var.get())
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                size_mb = int(self.size_var.get())
                
                self.log(f"[*] Generating {size_mb}MB disk image...")
                generator.generate(output_path, size_mb=size_mb)
                
                self.log("[✓] Disk image generated successfully!")
                self.update_status("Image generation complete")
                
                messagebox.showinfo("Success", f"Disk image created:\n{output_path}")
                
            except Exception as e:
                self.log(f"[!] Error: {str(e)}")
                messagebox.showerror("Error", str(e))
            finally:
                self.is_running = False
                self.progress.stop()
                
        threading.Thread(target=task, daemon=True).start()
        
    def start_carving(self):
        """Start file carving"""
        if self.is_running:
            messagebox.showwarning("Busy", "Another operation is in progress!")
            return
            
        self.is_running = True
        self.progress.start()
        self.carve_btn.config(state='disabled')
        
        def task():
            try:
                self.log("=" * 60)
                self.log("CARVING FILES")
                self.log("=" * 60)
                
                image_path = Path(self.carve_input_var.get())
                output_dir = Path(self.carve_output_var.get())
                min_size = int(self.min_size_var.get())
                
                if not image_path.exists():
                    raise Exception(f"Image not found: {image_path}")
                
                output_dir.mkdir(parents=True, exist_ok=True)
                
                self.log(f"[*] Carving from: {image_path.name}")
                self.log(f"[*] Output to: {output_dir}")
                
                carver = FileCarver()
                carved_files = carver.carve(image_path, output_dir, min_size)
                
                self.log(f"[✓] Carved {len(carved_files)} files")
                
                # Parse results
                self.log("\n[*] Parsing carved files...")
                parser = FileParser()
                parser.parse_directory(output_dir)
                
                report_path = output_dir.parent / "parse_report.json"
                parser.save_report(report_path)
                
                stats = parser.get_statistics()
                self.log(f"\n[*] Statistics:")
                self.log(f"    Total files: {stats.get('total_files', 0)}")
                self.log(f"    Valid files: {stats.get('valid_files', 0)}")
                self.log(f"    Total size: {stats.get('total_size', 0):,} bytes")
                
                self.log("\n[✓] Carving complete!")
                self.update_status("Carving complete")
                
                self.refresh_results()
                
                messagebox.showinfo("Success", 
                                  f"Carved {len(carved_files)} files\nResults saved to: {output_dir}")
                
            except Exception as e:
                self.log(f"[!] Error: {str(e)}")
                messagebox.showerror("Error", str(e))
            finally:
                self.is_running = False
                self.progress.stop()
                self.carve_btn.config(state='normal')
                
        threading.Thread(target=task, daemon=True).start()
    
    def run_automated_workflow(self):
        """Run the complete automated workflow"""
        if self.is_running:
            messagebox.showwarning("Busy", "Another operation is in progress!")
            return
        
        source_path = self.auto_source_var.get()
        if not source_path:
            messagebox.showwarning("Missing Input", "Please select a source path (directory or file)")
            return
        
        if not Path(source_path).exists():
            messagebox.showerror("Error", f"Source path not found: {source_path}")
            return
        
        self.is_running = True
        self.progress.start()
        
        def task():
            try:
                self.log("=" * 70)
                self.log("  AUTOMATED FORENSICS WORKFLOW")
                self.log("=" * 70)
                
                workflow = AutomatedForensicsWorkflow()
                
                # Redirect workflow output to GUI console
                import sys
                from io import StringIO
                
                # Create custom print function
                original_print = print
                def gui_print(*args, **kwargs):
                    message = ' '.join(str(arg) for arg in args)
                    self.log(message)
                    original_print(*args, **kwargs)
                
                # Temporarily replace print
                import builtins
                builtins.print = gui_print
                
                try:
                    output_dir = self.auto_output_var.get()
                    recursive = self.recursive_var.get()
                    
                    # Run workflow
                    results = workflow.run_complete_workflow(
                        Path(source_path),
                        Path(output_dir) if output_dir else None,
                        recursive=recursive
                    )
                    
                    # Update UI with results
                    if results['status'] == 'completed':
                        stats = results['statistics']
                        
                        self.log("\n" + "=" * 70)
                        self.log("  WORKFLOW COMPLETED SUCCESSFULLY")
                        self.log("=" * 70)
                        
                        # Save detailed results
                        results_file = Path(output_dir) / "workflow_results.json"
                        with open(results_file, 'w') as f:
                            json.dump(results, f, indent=2)
                        
                        self.log(f"\n[✓] Results saved to: {results_file}")
                        
                        # Update status
                        self.update_status("Automated workflow completed successfully")
                        
                        # Show summary dialog
                        summary = (
                            f"Workflow completed successfully!\n\n"
                            f"Original Files: {stats.get('total_original_files', 0)}\n"
                            f"Carved Files: {stats.get('total_carved_files', 0)}\n"
                            f"Verified Files: {stats.get('verified_count', 0)}\n"
                            f"Failed Files: {stats.get('failed_count', 0)}\n\n"
                            f"Recovery Rate: {stats.get('recovery_rate', 0):.1f}%\n"
                            f"Validation Rate: {stats.get('validation_rate', 0):.1f}%\n\n"
                            f"Output: {output_dir}"
                        )
                        
                        messagebox.showinfo("Workflow Complete", summary)
                        
                        # Update results tab with carved files
                        self.carve_output_var.set(str(Path(output_dir) / "carved_files"))
                        self.refresh_results()
                    else:
                        error_msg = results.get('error', 'Unknown error')
                        self.log(f"\n[!] Workflow failed: {error_msg}")
                        messagebox.showerror("Workflow Failed", error_msg)
                        
                finally:
                    # Restore original print
                    builtins.print = original_print
                    
            except Exception as e:
                self.log(f"\n[!] Error: {str(e)}")
                messagebox.showerror("Error", str(e))
                import traceback
                traceback.print_exc()
            finally:
                self.is_running = False
                self.progress.stop()
        
        threading.Thread(target=task, daemon=True).start()
        
    def run_binwalk(self):
        """Run binwalk analysis"""
        if self.is_running:
            messagebox.showwarning("Busy", "Another operation is in progress!")
            return
            
        self.is_running = True
        self.progress.start()
        
        def task():
            try:
                self.log("=" * 60)
                self.log("BINWALK ANALYSIS")
                self.log("=" * 60)
                
                analyzer = BinwalkAnalyzer()
                
                if not analyzer.is_binwalk_available():
                    self.log("[!] Binwalk not installed")
                    messagebox.showwarning("Binwalk Not Found", 
                                         "Binwalk is not installed on your system.\n"
                                         "Install it with: pip install binwalk")
                    return
                
                image_path = Path(self.carve_input_var.get())
                output_dir = self.base_dir / "output" / "binwalk_analysis"
                
                self.log(f"[*] Analyzing: {image_path.name}")
                results = analyzer.analyze(image_path, output_dir)
                
                report_path = self.base_dir / "output" / "binwalk_report.json"
                analyzer.save_report(report_path)
                
                self.log(f"[✓] Found {len(results)} signatures")
                self.log(f"[✓] Report saved to: {report_path}")
                
                messagebox.showinfo("Success", 
                                  f"Binwalk found {len(results)} signatures\n"
                                  f"Report: {report_path}")
                
            except Exception as e:
                self.log(f"[!] Error: {str(e)}")
                messagebox.showerror("Error", str(e))
            finally:
                self.is_running = False
                self.progress.stop()
                
        threading.Thread(target=task, daemon=True).start()
        
    def refresh_results(self):
        """Refresh results tree"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        # Load results
        report_path = self.base_dir / "output" / "parse_report.json"
        
        if not report_path.exists():
            self.stats_label.config(text="No results available. Run analysis first.")
            return
            
        try:
            with open(report_path, 'r') as f:
                files = json.load(f)
                
            for idx, file_info in enumerate(files):
                name = file_info.get('name', 'Unknown')
                ext = file_info.get('extension', 'unknown')
                size = file_info.get('size', 0)
                valid = "✓" if file_info.get('is_valid', False) else "✗"
                path = file_info.get('path', '')
                
                # Calculate hash for the file
                file_hash = "N/A"
                if path and Path(path).exists():
                    try:
                        file_hash = self._calculate_file_hash(Path(path), 'md5')[:16] + "..."
                    except (IOError, OSError):
                        pass
                
                self.results_tree.insert('', 'end', text=str(idx+1),
                                       values=(name, ext, f"{size:,} bytes", valid, file_hash, path))
                                       
            # Update statistics
            total = len(files)
            valid_count = sum(1 for f in files if f.get('is_valid', False))
            total_size = sum(f.get('size', 0) for f in files)
            
            # File types
            extensions = {}
            for f in files:
                ext = f.get('extension', 'unknown')
                extensions[ext] = extensions.get(ext, 0) + 1
            
            ext_str = ", ".join([f"{ext.upper()}: {count}" for ext, count in sorted(extensions.items())])
            
            stats_text = (f"📊 Total Files: {total} | "
                         f"✓ Valid: {valid_count} | "
                         f"✗ Invalid: {total - valid_count} | "
                         f"💾 Total Size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)\n"
                         f"📁 File Types: {ext_str}")
            
            self.stats_label.config(text=stats_text)
            self.log("[✓] Results refreshed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load results: {e}")
            
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_dir = self.base_dir / "output"
        output_dir.mkdir(exist_ok=True)
        
        if os.name == 'nt':  # Windows
            os.startfile(output_dir)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.Popen(['xdg-open', str(output_dir)])
            
    def export_report(self):
        """Export detailed report"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json"), 
                      ("HTML Files", "*.html"), ("All Files", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            report_path = self.base_dir / "output" / "parse_report.json"
            
            if not report_path.exists():
                messagebox.showwarning("No Data", "No results available to export.")
                return
                
            with open(report_path, 'r') as f:
                data = json.load(f)
            
            if filename.endswith('.json'):
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
            elif filename.endswith('.html'):
                self._export_html_report(filename, data)
            else:
                self._export_text_report(filename, data)
                        
            messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            self.log(f"[✓] Report exported: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")
    
    def _export_text_report(self, filename, data):
        """Export report as text file"""
        with open(filename, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write(f"{__project__}\n")
            f.write("FORENSICS ANALYSIS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Version: {__version__}\n")
            f.write("=" * 80 + "\n\n")
            
            # Summary
            total = len(data)
            valid_count = sum(1 for f in data if f.get('is_valid', False))
            total_size = sum(f.get('size', 0) for f in data)
            
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Files Carved: {total}\n")
            f.write(f"Valid Files: {valid_count}\n")
            f.write(f"Invalid Files: {total - valid_count}\n")
            f.write(f"Total Size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)\n")
            f.write("\n")
            
            # File types distribution
            extensions = {}
            for file_info in data:
                ext = file_info.get('extension', 'unknown')
                extensions[ext] = extensions.get(ext, 0) + 1
            
            f.write("FILE TYPES DISTRIBUTION\n")
            f.write("-" * 80 + "\n")
            for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
                f.write(f"{ext.upper():10s}: {count:5d} files\n")
            f.write("\n")
            
            # Detailed file list
            f.write("DETAILED FILE LIST\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, file_info in enumerate(data, 1):
                f.write(f"File #{idx}\n")
                f.write("-" * 40 + "\n")
                for key, value in file_info.items():
                    f.write(f"{key:15s}: {value}\n")
                f.write("\n")
    
    def _export_html_report(self, filename, data):
        """Export report as HTML file"""
        total = len(data)
        valid_count = sum(1 for f in data if f.get('is_valid', False))
        total_size = sum(f.get('size', 0) for f in data)
        
        # File types distribution
        extensions = {}
        for file_info in data:
            ext = file_info.get('extension', 'unknown')
            extensions[ext] = extensions.get(ext, 0) + 1
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Forensics Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #1e1e1e;
            color: #e0e0e0;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #2d2d2d;
            padding: 30px;
            border-radius: 10px;
        }}
        h1 {{
            color: #00bcd4;
            border-bottom: 3px solid #00bcd4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #667eea;
            margin-top: 30px;
        }}
        .summary {{
            background: #1e1e1e;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .summary-item {{
            display: inline-block;
            margin: 10px 20px 10px 0;
        }}
        .summary-label {{
            color: #b0b0b0;
            font-weight: bold;
        }}
        .summary-value {{
            color: #00bcd4;
            font-size: 24px;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background: #00bcd4;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #444;
        }}
        tr:hover {{
            background: #333;
        }}
        .valid {{
            color: #4caf50;
            font-weight: bold;
        }}
        .invalid {{
            color: #f44336;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #444;
            color: #808080;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 {__project__}</h1>
        <p>Forensics Analysis Report</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Version: {__version__}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="summary-item">
                <div class="summary-label">Total Files</div>
                <div class="summary-value">{total}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Valid Files</div>
                <div class="summary-value">{valid_count}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Invalid Files</div>
                <div class="summary-value">{total - valid_count}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Total Size</div>
                <div class="summary-value">{total_size / 1024 / 1024:.2f} MB</div>
            </div>
        </div>
        
        <h2>File Types Distribution</h2>
        <table>
            <tr>
                <th>Extension</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
"""
        
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            html_content += f"""
            <tr>
                <td>{ext.upper()}</td>
                <td>{count}</td>
                <td>{percentage:.1f}%</td>
            </tr>
"""
        
        html_content += """
        </table>
        
        <h2>Detailed File List</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Type</th>
                <th>Size</th>
                <th>Valid</th>
                <th>Hash</th>
            </tr>
"""
        
        for idx, file_info in enumerate(data, 1):
            name = file_info.get('name', 'Unknown')
            ext = file_info.get('extension', 'unknown')
            size = file_info.get('size', 0)
            valid = file_info.get('is_valid', False)
            valid_class = 'valid' if valid else 'invalid'
            valid_text = '✓ Valid' if valid else '✗ Invalid'
            
            # Calculate hash if not present
            file_path = file_info.get('path', '')
            file_hash = "N/A"
            if file_path and Path(file_path).exists():
                try:
                    file_hash = self._calculate_file_hash(Path(file_path), 'md5')[:16] + "..."
                except (IOError, OSError):
                    pass
            
            html_content += f"""
            <tr>
                <td>{idx}</td>
                <td>{name}</td>
                <td>{ext.upper()}</td>
                <td>{size:,} bytes</td>
                <td class="{valid_class}">{valid_text}</td>
                <td style="font-family: monospace; font-size: 12px;">{file_hash}</td>
            </tr>
"""
        
        html_content += f"""
        </table>
        
        <div class="footer">
            <p>© 2025 {__project__} v{__version__}</p>
            <p>Developed by {__author__}</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html_content)
    
    def new_analysis(self):
        """Start a new analysis"""
        if self.is_running:
            messagebox.showwarning("Busy", "An operation is in progress. Please wait.")
            return
        
        result = messagebox.askyesno("New Analysis", 
                                    "This will clear the console. Continue?")
        if result:
            self.clear_console()
            self.log("[*] Ready for new analysis")
            self.update_status("Ready for new analysis")
    
    def clear_console(self):
        """Clear console output"""
        self.console.delete('1.0', tk.END)
        self.log("[*] Console cleared")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def calculate_hash(self):
        """Calculate hash of a file"""
        filename = filedialog.askopenfilename(title="Select File to Hash")
        if not filename:
            return
        
        file_path = Path(filename)
        
        # Create a dialog to show both hashes
        hash_window = tk.Toplevel(self.root)
        hash_window.title("File Hash Calculator")
        hash_window.geometry("700x300")
        hash_window.configure(bg='#1e1e1e')
        
        frame = tk.Frame(hash_window, bg='#1e1e1e')
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="File Hash Calculator", 
                font=('Segoe UI', 16, 'bold'), bg='#1e1e1e', fg='#00bcd4').pack(pady=10)
        
        tk.Label(frame, text=f"File: {file_path.name}", 
                font=('Segoe UI', 10), bg='#1e1e1e', fg='#e0e0e0').pack(pady=5)
        
        tk.Label(frame, text=f"Size: {file_path.stat().st_size:,} bytes", 
                font=('Segoe UI', 10), bg='#1e1e1e', fg='#e0e0e0').pack(pady=5)
        
        # MD5
        md5_hash = self._calculate_file_hash(file_path, 'md5')
        md5_frame = tk.Frame(frame, bg='#1e1e1e')
        md5_frame.pack(fill='x', pady=10)
        
        tk.Label(md5_frame, text="MD5:", font=('Segoe UI', 10, 'bold'), 
                bg='#1e1e1e', fg='#00bcd4', width=10, anchor='w').pack(side='left')
        md5_entry = tk.Entry(md5_frame, font=('Consolas', 10), bg='#2d2d2d', 
                            fg='#e0e0e0', width=50)
        md5_entry.pack(side='left', padx=5)
        md5_entry.insert(0, md5_hash)
        md5_entry.config(state='readonly')
        
        # SHA-256
        sha256_hash = self._calculate_file_hash(file_path, 'sha256')
        sha_frame = tk.Frame(frame, bg='#1e1e1e')
        sha_frame.pack(fill='x', pady=10)
        
        tk.Label(sha_frame, text="SHA-256:", font=('Segoe UI', 10, 'bold'), 
                bg='#1e1e1e', fg='#00bcd4', width=10, anchor='w').pack(side='left')
        sha_entry = tk.Entry(sha_frame, font=('Consolas', 10), bg='#2d2d2d', 
                           fg='#e0e0e0', width=50)
        sha_entry.pack(side='left', padx=5)
        sha_entry.insert(0, sha256_hash)
        sha_entry.config(state='readonly')
        
        # Copy buttons
        btn_frame = tk.Frame(frame, bg='#1e1e1e')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Copy MD5", 
                 command=lambda: self._copy_to_clipboard(md5_hash),
                 bg='#00bcd4', fg='white', font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Copy SHA-256", 
                 command=lambda: self._copy_to_clipboard(sha256_hash),
                 bg='#00bcd4', fg='white', font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        self.log(f"[*] Hash calculated for: {file_path.name}")
        self.log(f"    MD5: {md5_hash}")
        self.log(f"    SHA-256: {sha256_hash}")
    
    def _calculate_file_hash(self, file_path, algorithm='md5'):
        """Calculate file hash with path validation"""
        # Validate path is within base directory or output directory
        try:
            file_path = file_path.resolve()
            base_resolved = self.base_dir.resolve()
            
            # Check if file is within the base directory
            if not str(file_path).startswith(str(base_resolved)):
                return "Invalid path"
        except (OSError, ValueError):
            return "Error"
        
        if algorithm == 'md5':
            hasher = hashlib.md5()
        elif algorithm == 'sha256':
            hasher = hashlib.sha256()
        else:
            return "Unknown algorithm"
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (IOError, OSError):
            return "Error"
    
    def _copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Hash copied to clipboard!")
    
    def verify_all_files(self):
        """Verify all carved files"""
        output_dir = self.base_dir / "output" / "carved_files"
        
        if not output_dir.exists():
            messagebox.showwarning("No Files", "No carved files found to verify.")
            return
        
        self.log("\n" + "=" * 60)
        self.log("VERIFYING CARVED FILES")
        self.log("=" * 60)
        
        files = list(output_dir.glob("*.*"))
        if not files:
            self.log("[!] No files to verify")
            return
        
        valid_count = 0
        invalid_count = 0
        
        for carved_file in files:
            is_valid, msg = verify_file(carved_file)
            status = "✓" if is_valid else "✗"
            self.log(f"  {status} {carved_file.name} - {msg}")
            
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
        
        self.log(f"\n[*] Verification complete:")
        self.log(f"    Valid: {valid_count}")
        self.log(f"    Invalid: {invalid_count}")
        
        messagebox.showinfo("Verification Complete", 
                           f"Valid: {valid_count}\nInvalid: {invalid_count}")
    
    def preview_selected_file(self):
        """Preview selected file with path validation"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a file to preview.")
            return
        
        item = self.results_tree.item(selection[0])
        file_path = item['values'][5] if len(item['values']) > 5 else None
        
        if not file_path:
            messagebox.showerror("Error", "File path not found.")
            return
        
        # Validate path
        try:
            file_path_obj = Path(file_path).resolve()
            base_resolved = self.base_dir.resolve()
            
            # Check if file is within the base directory
            if not str(file_path_obj).startswith(str(base_resolved)):
                messagebox.showerror("Error", "Invalid file path.")
                return
            
            if not file_path_obj.exists():
                messagebox.showerror("Error", "File not found.")
                return
        except (OSError, ValueError):
            messagebox.showerror("Error", "Invalid file path.")
            return
        
        # Open with default application
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path_obj)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', str(file_path_obj)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(file_path_obj)])
            
            self.log(f"[*] Opened file: {file_path_obj.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def filter_results(self):
        """Filter results based on search"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Load and filter results
        report_path = self.base_dir / "output" / "parse_report.json"
        
        if not report_path.exists():
            return
        
        try:
            with open(report_path, 'r') as f:
                files = json.load(f)
            
            filtered_files = []
            for file_info in files:
                name = file_info.get('name', '').lower()
                ext = file_info.get('extension', '').lower()
                
                if search_term in name or search_term in ext:
                    filtered_files.append(file_info)
            
            for idx, file_info in enumerate(filtered_files):
                name = file_info.get('name', 'Unknown')
                ext = file_info.get('extension', 'unknown')
                size = file_info.get('size', 0)
                valid = "✓" if file_info.get('is_valid', False) else "✗"
                path = file_info.get('path', '')
                
                # Calculate hash
                file_hash = "N/A"
                if path and Path(path).exists():
                    try:
                        file_hash = self._calculate_file_hash(Path(path), 'md5')[:16] + "..."
                    except (IOError, OSError):
                        pass
                
                self.results_tree.insert('', 'end', text=str(idx+1),
                                       values=(name, ext, f"{size:,} bytes", valid, file_hash, path))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter results: {e}")
    
    def show_user_guide(self):
        """Show user guide"""
        self.notebook.select(2)  # Switch to Settings & Help tab
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_window = tk.Toplevel(self.root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("500x400")
        shortcuts_window.configure(bg='#1e1e1e')
        
        frame = tk.Frame(shortcuts_window, bg='#1e1e1e')
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="⌨️ Keyboard Shortcuts", 
                font=('Segoe UI', 16, 'bold'), bg='#1e1e1e', fg='#00bcd4').pack(pady=10)
        
        shortcuts = [
            ("Ctrl+N", "New Analysis"),
            ("Ctrl+O", "Open Output Folder"),
            ("Ctrl+E", "Export Report"),
            ("Ctrl+L", "Clear Console"),
            ("Ctrl+Q", "Quit Application"),
            ("F1", "Show User Guide"),
            ("F5", "Refresh Results"),
            ("F11", "Toggle Full Screen"),
        ]
        
        for key, desc in shortcuts:
            row = tk.Frame(frame, bg='#1e1e1e')
            row.pack(fill='x', pady=5)
            
            tk.Label(row, text=key, font=('Consolas', 11, 'bold'), 
                    bg='#2d2d2d', fg='#00bcd4', width=15, 
                    relief='raised', padx=10, pady=5).pack(side='left', padx=5)
            
            tk.Label(row, text=desc, font=('Segoe UI', 10), 
                    bg='#1e1e1e', fg='#e0e0e0', anchor='w').pack(side='left', padx=10)
    
    def show_about(self):
        """Show about dialog"""
        self.notebook.select(2)  # Switch to Settings & Help tab

def main():
    root = tk.Tk()
    app = ForensicsAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()