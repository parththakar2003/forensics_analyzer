# Digital Forensics Analyzer - Major Project

## 🎓 Academic Project Overview

This repository contains a comprehensive **Digital Forensics and File Carving Analysis Tool** developed as a major academic project. The tool demonstrates advanced capabilities in forensic analysis, file recovery, and evidence processing with a professional graphical user interface.

## 📋 Project Information

- **Project Title**: Forensics Analyzer - Professional Digital Forensics Tool
- **Category**: Computer Science / Cybersecurity Major Project
- **Version**: 2.0.0
- **Author**: Parth Thakar
- **Year**: 2025
- **Language**: Python 3.8+
- **License**: Educational Use

## 🎯 Project Objectives

This major project aims to:

1. Develop a comprehensive forensics analysis tool with GUI
2. Implement signature-based file carving algorithms
3. Integrate advanced binary analysis capabilities
4. Create professional reporting and documentation features
5. Demonstrate software engineering best practices
6. Provide practical learning tool for digital forensics

## 🌟 Key Features

### Core Forensics Capabilities
- **Disk Image Generation**: Create synthetic evidence for testing
- **File Carving**: Extract files from disk images using signature analysis
- **File Validation**: Verify integrity and validity of carved files
- **Hash Calculation**: Generate MD5 and SHA-256 hashes
- **Binary Analysis**: Binwalk integration for firmware examination
- **Comprehensive Reporting**: Multiple export formats (JSON, TXT, HTML)

### Professional GUI Interface
- Modern dark-themed interface with cyan accents
- Splash screen with branding
- Complete menu system (File, Tools, View, Help)
- Keyboard shortcuts for efficient navigation
- Real-time console output
- Progress indicators
- Search and filter capabilities
- File preview functionality

### Advanced Tools
- Hash calculator with clipboard support
- File verification system
- Search and filter results
- Batch processing support
- Multiple export formats
- Built-in user guide and help system

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- Optional: Binwalk for advanced analysis

### Installation

```bash
# Clone the repository
git clone https://github.com/parththakar2003/major-project.git
cd major-project/forensics-analyzer

# Optional: Install binwalk
pip install binwalk
```

### Running the Application

**GUI Mode (Recommended):**
```bash
python src/gui.py
```

**CLI Mode:**
```bash
python src/main.py
```

## 📁 Project Structure

```
major-project/
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
└── forensics-analyzer/            # Main application
    ├── README.md                  # Detailed documentation
    ├── requirements.txt           # Dependencies
    ├── install_binwalk.py         # Binwalk installer
    ├── src/                       # Source code
    │   ├── gui.py                 # Main GUI application (900+ lines)
    │   ├── main.py                # CLI application
    │   ├── main_gui.py            # GUI launcher
    │   ├── disk_image_generator.py # Disk image creation
    │   ├── file_carver.py         # File carving engine
    │   ├── file_parser.py         # File analysis
    │   ├── binwalk_analyzer.py    # Binwalk integration
    │   └── verify_files.py        # File verification
    ├── tests/                     # Test suite
    │   ├── test_disk_image_generator.py
    │   ├── test_file_carver.py
    │   ├── test_parser.py
    │   └── test_binwalk_analyzer.py
    ├── evidence/                  # Generated disk images
    └── output/                    # Analysis results
```

## 🔍 Supported File Types

The tool can carve and analyze 15+ file types:

**Images**: JPG, PNG, GIF, BMP, TIFF
**Documents**: PDF, DOCX, XLSX, PPTX
**Archives**: ZIP, RAR
**Executables**: EXE, ELF
**Media**: MP4, MP3, AVI, WAV

## 📊 Technical Highlights

### Architecture
- **Modular Design**: Separate modules for each functionality
- **Threading**: Multi-threaded GUI for responsiveness
- **Error Handling**: Comprehensive exception handling
- **Logging**: Detailed console logging for debugging
- **Code Quality**: Well-documented and maintainable code

### Algorithms Implemented
- **Signature-Based Carving**: Header/footer matching algorithm
- **File Validation**: Content-based validation
- **Hash Calculation**: MD5 and SHA-256 implementation
- **Binary Analysis**: Integration with Binwalk

### Technologies Used
- **Python**: Core programming language
- **tkinter**: GUI framework (built-in)
- **hashlib**: Cryptographic hashing
- **threading**: Concurrent operations
- **pathlib**: Modern file system operations
- **json**: Data serialization

## 📖 Documentation

Comprehensive documentation is available:

1. **User Guide**: Built into the application (press F1)
2. **README**: Detailed setup and usage instructions
3. **Code Comments**: Well-commented source code
4. **Test Suite**: Example usage in test files

## 🎯 Learning Outcomes

Students and users will learn about:

- Digital forensics principles and practices
- File system structure and signatures
- GUI application development in Python
- Multi-threaded programming
- Data validation and integrity verification
- Report generation and documentation
- Software engineering best practices
- Testing and quality assurance

## 📈 Project Complexity

This major project demonstrates:

- **900+ lines** of GUI code with advanced features
- **Multiple modules** working together
- **Professional UI/UX** design principles
- **Comprehensive error handling**
- **Real-time progress updates**
- **Multiple export formats**
- **Built-in help system**
- **Keyboard shortcuts**
- **Search and filter capabilities**

## 🎓 Academic Applications

This project is suitable for:

- **Major Projects**: Final year or capstone projects
- **Course Projects**: Digital forensics, cybersecurity courses
- **Research**: File system analysis, carving algorithms
- **Learning Tool**: Understanding forensics concepts
- **Portfolio**: Demonstrating programming skills

## 🔐 Responsible Use

This tool is designed for:
- Educational purposes
- Legitimate forensics investigations
- Security research
- Academic projects

Users must comply with applicable laws and obtain proper authorization.

## 📞 Support & Contact

- **GitHub Repository**: https://github.com/parththakar2003/major-project
- **Issues**: Report via GitHub Issues
- **Documentation**: See forensics-analyzer/README.md

## 🏆 Acknowledgments

This major project demonstrates professional software development practices and comprehensive understanding of digital forensics principles. It provides a practical, real-world application suitable for academic evaluation and professional portfolio demonstration.

## 📝 Version History

### Version 2.0.0 (January 2025) - Major Project Release
- ✨ Complete GUI redesign with professional features
- 🎨 Splash screen and modern dark theme
- ⌨️ Keyboard shortcuts and menu system
- 🔐 Hash calculation (MD5, SHA-256)
- 🔍 Search, filter, and preview capabilities
- 📊 HTML/TXT/JSON export formats
- 📖 Comprehensive built-in user guide
- 💎 Enhanced reporting and statistics

### Version 1.0.0 (Previous)
- Initial implementation
- Basic GUI and CLI interfaces
- Core carving functionality

## 📄 License

© 2025 Parth Thakar - Forensics Analyzer Major Project
All Rights Reserved

This software is provided for educational and research purposes.

---

**Thank you for reviewing this major project!**

*Developed as a comprehensive demonstration of digital forensics knowledge and professional software development skills.*
