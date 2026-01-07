import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from pathlib import Path
import json
from datetime import datetime

from disk_image_generator import DiskImageGenerator
from file_carver import FileCarver
from file_parser import FileParser
from binwalk_analyzer import BinwalkAnalyzer

class ForensicsAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Forensics Analyzer - Professional Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.is_running = False
        self.base_dir = Path(__file__).parent.parent
        
        # Style configuration
        self.setup_styles()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        accent_color = '#667eea'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'), foreground=accent_color)
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'), foreground=accent_color)
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), borderwidth=0)
        style.configure('Accent.TButton', background=accent_color, foreground='white')
        
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        title = ttk.Label(header_frame, text="🔍 Forensics Analyzer", style='Header.TLabel')
        title.pack()
        
        subtitle = ttk.Label(header_frame, text="Professional File Carving & Analysis Tool", 
                            font=('Segoe UI', 10))
        subtitle.pack()
        
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
        
        # Left panel - Configuration
        left_frame = ttk.Frame(tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
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
        self.notebook.add(tab, text="  Results  ")
        
        # Top buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="📁 Open Output Folder", 
                  command=self.open_output_folder).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh Results", 
                  command=self.refresh_results).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📊 Export Report", 
                  command=self.export_report).pack(side='left', padx=5)
        
        # Results tree
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Name', 'Type', 'Size', 'Valid', 'Path')
        self.results_tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings', height=20)
        
        self.results_tree.heading('#0', text='ID')
        self.results_tree.column('#0', width=50)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Statistics
        stats_frame = ttk.LabelFrame(tab, text="Statistics", padding=15)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="No results yet. Run analysis first.", 
                                     font=('Segoe UI', 10))
        self.stats_label.pack()
        
    def create_settings_tab(self):
        """Create settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  Settings  ")
        
        settings_frame = ttk.LabelFrame(tab, text="Application Settings", padding=20)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Theme
        ttk.Label(settings_frame, text="Theme:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        theme_var = tk.StringVar(value="Dark")
        theme_combo = ttk.Combobox(settings_frame, textvariable=theme_var, 
                                   values=['Dark', 'Light'], state='readonly', width=20)
        theme_combo.grid(row=0, column=1, sticky='w', pady=10, padx=10)
        
        # About
        about_frame = ttk.LabelFrame(tab, text="About", padding=20)
        about_frame.pack(fill='x', padx=20, pady=10)
        
        about_text = """
Forensics Analyzer - Professional Edition
Version 1.0.0

A comprehensive file carving and forensics analysis tool
Built with Python and tkinter

Features:
• Disk image generation with embedded files
• Signature-based file carving
• File validation and parsing
• Binwalk integration
• Detailed reporting

© 2025 Hapi Mam Project
        """
        
        about_label = ttk.Label(about_frame, text=about_text, justify='left')
        about_label.pack()
        
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
                
                self.results_tree.insert('', 'end', text=str(idx+1),
                                       values=(name, ext, f"{size:,} bytes", valid, path))
                                       
            # Update statistics
            total = len(files)
            valid_count = sum(1 for f in files if f.get('is_valid', False))
            total_size = sum(f.get('size', 0) for f in files)
            
            stats_text = (f"Total Files: {total} | "
                         f"Valid: {valid_count} | "
                         f"Invalid: {total - valid_count} | "
                         f"Total Size: {total_size:,} bytes")
            
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load results: {e}")
            
    def open_output_folder(self):
        """Open output folder in file explorer"""
        import os
        import subprocess
        
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
            filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json"), ("All Files", "*.*")]
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
            else:
                with open(filename, 'w') as f:
                    f.write("=" * 80 + "\n")
                    f.write("FORENSICS ANALYSIS REPORT\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for idx, file_info in enumerate(data, 1):
                        f.write(f"File #{idx}\n")
                        f.write("-" * 40 + "\n")
                        for key, value in file_info.items():
                            f.write(f"{key:15s}: {value}\n")
                        f.write("\n")
                        
            messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")

def main():
    root = tk.Tk()
    app = ForensicsAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()