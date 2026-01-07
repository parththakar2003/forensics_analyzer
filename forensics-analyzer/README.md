# Forensics Analyzer - Major Project

A comprehensive and professional digital forensics and file carving analysis tool designed for educational and professional use in computer forensics. This major project demonstrates advanced capabilities in disk image analysis, file carving, and forensic investigation.

## 🎓 Major Project Features

This is a comprehensive forensics analysis tool developed as a major academic project with the following professional features:

### Core Capabilities
- 🔧 **Disk Image Generation**: Create synthetic disk images with embedded files for testing
- 🔪 **Advanced File Carving**: Signature-based file extraction from disk images
- 📊 **File Analysis & Parsing**: Validate and analyze carved files with detailed metadata
- 🔬 **Binwalk Integration**: Advanced binary analysis and firmware examination
- 🖥️ **Professional GUI**: Modern, user-friendly graphical interface with dark theme
- 📈 **Comprehensive Reporting**: Export reports in JSON, TXT, and HTML formats

### Advanced Features
- 🔐 **Hash Calculation**: MD5 and SHA-256 hash generation for evidence integrity
- 🔍 **File Preview**: Built-in file preview capability
- 🔎 **Search & Filter**: Search and filter results in real-time
- ⚡ **Batch Processing**: Process multiple files efficiently
- 📋 **Copy to Clipboard**: Easy hash copying for documentation
- ⌨️ **Keyboard Shortcuts**: Professional keyboard navigation
- 📖 **Comprehensive Help**: Built-in user guide and documentation

## 🎨 GUI Features

### Modern Interface
- **Splash Screen**: Professional startup screen with branding
- **Menu System**: Complete menu bar with File, Tools, View, and Help menus
- **Tabbed Interface**: Organized workflow with Generate & Carve, Results, and Settings tabs
- **Dark Theme**: Modern dark theme with cyan accents for reduced eye strain
- **Real-time Console**: Live output console showing operation progress
- **Status Bar**: Current operation status at a glance

### Tab 1: Generate & Carve
- **Generate Disk Image**: Create test disk images with embedded files
  - Configure image size
  - Select file types to embed (JPG, PNG, PDF, TXT, DOCX, MP3)
  - Custom output path
  - Progress indication

- **Carve Files**: Extract files from disk images
  - Select input disk image
  - Configure output directory
  - Set minimum file size threshold
  - Real-time progress updates

- **Binwalk Analysis**: Run advanced binary analysis
  - Automatic signature detection
  - Extract embedded files
  - Firmware analysis

### Tab 2: Results & Analysis
- **Results Tree View**: Display all carved files in organized table
  - File name, type, size, validation status
  - MD5 hash preview
  - Full file path
- **Search & Filter**: Real-time filtering of results
- **File Preview**: Double-click or button to preview files
- **Statistics Dashboard**: Comprehensive analysis statistics
  - Total files, valid/invalid counts
  - Total size with MB conversion
  - File type distribution
- **Export Options**: Export detailed reports
  - JSON format for data processing
  - TXT format for documentation
  - HTML format with professional styling and charts

### Tab 3: Settings & Help
- **Application Settings**: Configure application preferences
- **User Guide**: Comprehensive documentation and tutorials
  - Getting started guide
  - Feature descriptions
  - Keyboard shortcuts reference
  - Tips and best practices
  - Troubleshooting guide
- **About**: Version information and credits

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/parththakar2003/major-project.git
cd major-project/forensics-analyzer

# No dependencies required for basic functionality
# Optional: Install binwalk for advanced analysis
pip install binwalk
```

## 🚀 Usage

### GUI Mode (Recommended)

Launch the graphical interface:

```bash
python src/gui.py
```

Or use the launcher:

```bash
python src/main_gui.py
```

### CLI Mode

For command-line usage:

```bash
python src/main.py
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Analysis |
| `Ctrl+O` | Open Output Folder |
| `Ctrl+E` | Export Report |
| `Ctrl+L` | Clear Console |
| `Ctrl+Q` | Quit Application |
| `F1` | Show User Guide |
| `F5` | Refresh Results |
| `F11` | Toggle Full Screen |

## 📋 Workflow

### 1. Generate a Disk Image
1. Navigate to **Generate & Carve** tab
2. Set image size (recommended: 10-50 MB for testing)
3. Select file types to embed
4. Click **"Generate Disk Image"**
5. Wait for completion message

### 2. Carve Files
1. Select the disk image file (default: `evidence/evidence.dd`)
2. Choose output directory (default: `output/carved_files`)
3. Set minimum file size (default: 1024 bytes)
4. Click **"Start Carving"**
5. Monitor progress in console

### 3. Analyze Results
1. Switch to **Results & Analysis** tab
2. Review carved files in the tree view
3. Use search to filter results
4. Double-click files to preview
5. Export reports as needed

### 4. Advanced Analysis (Optional)
1. Click **"Run Binwalk Analysis"** for firmware analysis
2. Use **Tools** menu for hash calculation
3. Verify all files using **Tools > Verify Carved Files**

## 🔍 Supported File Types

### Images
- **JPEG** (.jpg, .jpeg) - Joint Photographic Experts Group
- **PNG** (.png) - Portable Network Graphics
- **GIF** (.gif) - Graphics Interchange Format
- **BMP** (.bmp) - Bitmap Image File
- **TIFF** (.tiff, .tif) - Tagged Image File Format

### Documents
- **PDF** (.pdf) - Portable Document Format
- **DOCX** (.docx) - Microsoft Word Document
- **XLSX** (.xlsx) - Microsoft Excel Spreadsheet
- **PPTX** (.pptx) - Microsoft PowerPoint Presentation

### Archives
- **ZIP** (.zip) - ZIP Archive
- **RAR** (.rar) - RAR Archive

### Executables
- **EXE** (.exe) - Windows Executable
- **ELF** - Linux Executable

### Media
- **MP4** (.mp4) - MPEG-4 Video
- **MP3** (.mp3) - MPEG Audio Layer 3
- **AVI** (.avi) - Audio Video Interleave
- **WAV** (.wav) - Waveform Audio File

## 📁 Output Structure

```
forensics-analyzer/
├── evidence/
│   └── evidence.dd          # Generated disk image
├── output/
│   ├── carved_files/        # Extracted files
│   │   ├── file_001.jpg
│   │   ├── file_002.png
│   │   └── ...
│   ├── parse_report.json    # Detailed analysis (JSON)
│   ├── binwalk_analysis/    # Binwalk results
│   └── binwalk_report.json  # Binwalk report
└── src/
    ├── gui.py               # GUI application
    ├── main.py              # CLI application
    └── ...
```

## 🛠️ Tools & Menu Options

### File Menu
- **New Analysis**: Clear console and start fresh
- **Open Output Folder**: Open results directory
- **Export Report**: Save analysis report (TXT/JSON/HTML)
- **Exit**: Close application

### Tools Menu
- **Calculate File Hash**: Generate MD5 and SHA-256 hashes
- **Verify Carved Files**: Validate all carved files
- **Clear Console**: Clear output console

### View Menu
- **Refresh Results**: Reload results table
- **Full Screen**: Toggle full screen mode

### Help Menu
- **User Guide**: Open comprehensive documentation
- **Keyboard Shortcuts**: View all shortcuts
- **About**: Version and project information

## 📊 Report Formats

### JSON Report
- Machine-readable format
- Complete metadata for all files
- Easy integration with other tools
- Suitable for automated processing

### Text Report
- Human-readable format
- Summary statistics
- File type distribution
- Detailed file list
- Suitable for documentation

### HTML Report
- Professional styled format
- Visual statistics
- Color-coded validation status
- Interactive layout
- Suitable for presentations

## 🔒 Hash Calculation

The tool provides hash calculation for evidence integrity:

- **MD5**: 128-bit hash for quick verification
- **SHA-256**: 256-bit cryptographic hash for security

Hashes can be:
- Calculated for any file
- Copied to clipboard
- Included in reports
- Used for chain of custody

## 🧪 Testing

Run the test suite:

```bash
cd tests
python -m pytest
```

Or test individual components:

```bash
python test_disk_image_generator.py
python test_file_carver.py
python test_parser.py
python test_binwalk_analyzer.py
```

## 🔧 Advanced Configuration

### Custom Signatures
Extend the signature database by editing:
- `src/file_carver.py` - Add new file type signatures
- `src/disk_image_generator.py` - Add file generation methods

### Binwalk Integration
For advanced firmware analysis:

```bash
pip install binwalk

# Additional tools for extraction
sudo apt-get install binutils mtd-utils gzip bzip2 tar arj lhasa p7zip p7zip-full cabextract cramfsprogs squashfs-tools
```

## 💡 Tips & Best Practices

### For Students and Researchers
- Start with small disk images (10-50 MB) for learning
- Experiment with different file types
- Document your findings in reports
- Use hash verification for integrity
- Practice with known test data first

### For Professionals
- Maintain chain of custody with hash documentation
- Export reports in multiple formats for records
- Verify all carved files before analysis
- Use Binwalk for complex firmware cases
- Keep backups of original evidence

### Performance Optimization
- Use appropriate minimum file size to filter noise
- Process large images in smaller chunks
- Close unnecessary applications when processing
- Monitor memory usage for very large images

## 🐛 Troubleshooting

### Common Issues

**Q: Binwalk not found?**
```bash
pip install binwalk
```

**Q: tkinter not available?**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (included with Python)
brew install python-tk

# Windows (included with Python)
# Reinstall Python with tcl/tk option
```

**Q: Permission errors?**
- Run with administrator/sudo privileges for disk access
- Check file permissions in output directories

**Q: Memory issues with large images?**
- Process in smaller chunks
- Increase system memory
- Close other applications
- Use 64-bit Python for large files

**Q: No files carved?**
- Check minimum file size threshold
- Verify disk image validity
- Ensure file signatures are correct
- Try different carving parameters

**Q: GUI not responsive?**
- GUI uses threading for responsiveness
- Wait for current operation to complete
- Check console for error messages

## 📚 Documentation

### Academic Use
This project can be used for:
- Digital Forensics courses
- Computer Science projects
- Cybersecurity research
- File system analysis studies
- Malware analysis training

### Learning Objectives
Students will learn about:
- File signature analysis
- Disk image forensics
- GUI application development
- Python threading and async operations
- Data validation and integrity
- Report generation and documentation
- Software engineering best practices

## 🎓 Project Structure

```
major-project/
└── forensics-analyzer/
    ├── README.md               # This file
    ├── requirements.txt        # Python dependencies
    ├── install_binwalk.py      # Binwalk installer
    ├── src/                    # Source code
    │   ├── gui.py              # Main GUI application
    │   ├── main.py             # CLI application
    │   ├── main_gui.py         # GUI launcher
    │   ├── disk_image_generator.py  # Image generation
    │   ├── file_carver.py      # File carving engine
    │   ├── file_parser.py      # File analysis
    │   ├── binwalk_analyzer.py # Binwalk integration
    │   └── verify_files.py     # File verification
    ├── tests/                  # Test suite
    │   ├── test_disk_image_generator.py
    │   ├── test_file_carver.py
    │   ├── test_parser.py
    │   └── test_binwalk_analyzer.py
    ├── evidence/               # Generated disk images
    └── output/                 # Analysis results
        ├── carved_files/       # Extracted files
        └── reports/            # Generated reports
```

## 🌟 Key Highlights

### What Makes This a Major Project?

1. **Comprehensive Functionality**: Multiple forensics tools integrated
2. **Professional GUI**: Modern, intuitive interface with advanced features
3. **Multiple Output Formats**: JSON, TXT, HTML reporting
4. **Advanced Analysis**: Hash calculation, file verification, Binwalk integration
5. **User Experience**: Keyboard shortcuts, search, preview, help system
6. **Documentation**: Extensive user guide and technical documentation
7. **Code Quality**: Well-structured, modular, tested code
8. **Real-world Application**: Practical tool for forensics investigations

## 🔐 Security & Legal

### Responsible Use
This tool is designed for:
- Educational purposes
- Legitimate forensics investigations
- Security research
- Academic projects

### Legal Considerations
Users must:
- Comply with applicable laws and regulations
- Obtain proper authorization before analyzing systems
- Respect privacy and data protection laws
- Use only for lawful purposes
- Maintain ethical standards in forensics work

## 👥 Credits & Acknowledgments

**Project**: Forensics Analyzer - Major Project
**Version**: 2.0.0
**Author**: Parth Thakar
**Year**: 2025

### Technologies Used
- Python 3.12
- tkinter (GUI framework)
- hashlib (hash calculation)
- threading (concurrency)
- Binwalk (optional, for advanced analysis)

### Inspiration
This project was inspired by professional forensics tools and designed to provide
a comprehensive learning platform for students and researchers in digital forensics.

## 📞 Support & Contact

For questions, issues, or contributions:
- **GitHub**: https://github.com/parththakar2003/major-project
- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: See built-in User Guide (F1 in application)

## 📄 License

© 2025 Forensics Analyzer - Major Project
All Rights Reserved

This software is provided for educational and research purposes.

## 🚀 Future Enhancements

Planned features for future versions:
- Network forensics capabilities
- Memory analysis tools
- Timeline analysis
- Case management system
- Multi-threaded carving for performance
- Plugin system for custom analyzers
- Database support for large datasets
- Cloud storage integration
- Collaborative features for teams

## 📝 Changelog

### Version 2.0.0 (January 2025)
- ✨ Major project enhancement release
- 🎨 Professional GUI with splash screen and menu bar
- ⌨️ Keyboard shortcuts and navigation
- 🔐 Hash calculation (MD5, SHA-256)
- 🔍 Search and filter results
- 👁️ File preview capability
- 📊 HTML export with professional styling
- 📖 Comprehensive user guide
- 🎯 Enhanced statistics and reporting
- 💎 Multiple theme support
- 🚀 Performance improvements

### Version 1.0.0 (Previous)
- Initial release
- Basic GUI implementation
- Core carving functionality
- Binwalk integration

---

**Thank you for using Forensics Analyzer!**

For the latest updates and documentation, visit the GitHub repository.

*Developed with ❤️ for the digital forensics community*