# Forensics Analyzer - Professional Edition

A comprehensive file carving and forensics analysis tool with both CLI and GUI interfaces.

## Features

- 🔧 **Disk Image Generation**: Create synthetic disk images with embedded files
- 🔪 **File Carving**: Signature-based file extraction from disk images
- 📊 **File Parsing**: Validate and analyze carved files
- 🔬 **Binwalk Integration**: Advanced binary analysis (optional)
- 🖥️ **Modern GUI**: User-friendly interface with real-time progress
- 📈 **Detailed Reports**: JSON and text-based reporting

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd forensics-analyzer

# No dependencies required for basic functionality
# Optional: Install binwalk
pip install binwalk
```

## Usage

### GUI Mode (Recommended)

```bash
python src/gui.py
```

Or use the launcher:

```bash
python src/main_gui.py
```

### CLI Mode

```bash
python src/main.py
```

## GUI Features

### Tab 1: Generate & Carve
- **Generate Disk Image**: Create test disk images with embedded files
  - Configure image size
  - Select file types to embed (JPG, PNG, PDF, TXT, DOCX, MP3)
  - Custom output path

- **Carve Files**: Extract files from disk images
  - Select input disk image
  - Configure output directory
  - Set minimum file size threshold

- **Binwalk Analysis**: Run advanced binary analysis
  - Automatic signature detection
  - Extract embedded files

### Tab 2: Results
- View all carved files in a tree view
- See file validation status
- Export detailed reports (JSON/TXT)
- Open output folder directly

### Tab 3: Settings
- Theme configuration
- Application information

## File Signatures Supported

- **Images**: JPG, PNG, GIF, BMP, TIFF
- **Documents**: PDF, DOCX, XLSX, PPTX
- **Archives**: ZIP, RAR
- **Executables**: EXE, ELF
- **Media**: MP4, MP3, AVI, WAV

## Output Structure

```
forensics-analyzer/
├── evidence/
│   └── evidence.dd          # Generated disk image
├── output/
│   ├── carved_files/        # Extracted files
│   ├── parse_report.json    # Detailed analysis
│   └── binwalk_analysis/    # Binwalk results
└── src/
    ├── gui.py               # GUI application
    ├── main.py              # CLI application
    └── ...
```

## Screenshots

### Main Interface
- Modern dark theme
- Real-time console output
- Progress indicators

### Results View
- Tabular file listing
- Validation status
- Detailed statistics

## Technical Details

- **Language**: Python 3.8+
- **GUI Framework**: tkinter (built-in)
- **Threading**: Multi-threaded for responsive UI
- **File Signatures**: Custom signature database
- **Carving Algorithm**: Header/footer matching with validation

## Advanced Features

### Binwalk Integration
If binwalk is installed, the tool can perform:
- Firmware analysis
- Embedded file extraction
- Compression detection
- Filesystem identification

### Custom Signatures
Extend the signature database in `file_carver.py` and `disk_image_generator.py`

## Troubleshooting

### Binwalk Not Found
```bash
pip install binwalk
```

### Permission Issues
Run with administrator/sudo privileges for disk access

### Memory Issues
For large disk images (>100MB), increase system memory allocation

## License

© 2025 Hapi Mam Project

## Contributors

- Your Name

## Version History

- **1.0.0** (2025-01-26)
  - Initial release
  - GUI implementation
  - Core carving functionality
  - Binwalk integration

## Support

For issues and questions, please open an issue on GitHub.