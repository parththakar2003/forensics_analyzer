# Forensics Analyzer - Quick Reference Guide

## 🚀 Quick Start

```bash
# Start GUI
python src/gui.py

# Start CLI
python src/main.py

# Run Demo
python demo.py
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+N` | New Analysis |
| `Ctrl+O` | Open Output Folder |
| `Ctrl+E` | Export Report |
| `Ctrl+L` | Clear Console |
| `Ctrl+Q` | Quit |
| `F1` | User Guide |
| `F5` | Refresh Results |
| `F11` | Full Screen |

## 📋 Typical Workflow

### 1. Generate Test Image
- Open GUI → "Generate & Carve" tab
- Set size: 10-50 MB
- Select file types
- Click "Generate Disk Image"

### 2. Carve Files
- Select disk image (evidence/evidence.dd)
- Set output directory (output/carved_files)
- Min size: 1024 bytes
- Click "Start Carving"

### 3. View Results
- Switch to "Results & Analysis" tab
- Use search to filter
- Double-click to preview
- Click "Export Report"

## 🔍 Supported File Types

**Images:** JPG, PNG, GIF, BMP, TIFF
**Documents:** PDF, DOCX, XLSX, PPTX
**Archives:** ZIP, RAR
**Media:** MP4, MP3, AVI, WAV
**Executables:** EXE, ELF

## 📊 Export Formats

- **JSON** - Machine-readable, for automation
- **TXT** - Human-readable, for documentation
- **HTML** - Professional styled, for presentations

## 🛠️ Tools Menu

- **Calculate Hash** - Generate MD5/SHA-256
- **Verify Files** - Validate all carved files
- **Clear Console** - Clear output

## 💡 Tips

- Start with small images (10-50 MB)
- Use search to find specific files
- Export reports for documentation
- Use hash verification for integrity
- Check console for detailed logs

## 🔧 Common Tasks

### Calculate File Hash
1. Tools → Calculate File Hash
2. Select file
3. View MD5 and SHA-256
4. Copy to clipboard

### Export HTML Report
1. Results tab
2. Click "Export Report"
3. Choose .html extension
4. Open in browser

### Search Results
1. Results tab
2. Type in search box
3. Real-time filtering

## 📞 Need Help?

Press `F1` in the application for comprehensive user guide

## 🎓 Academic Use

This tool demonstrates:
- Digital forensics principles
- File signature analysis
- GUI development
- Software engineering
- Report generation
- Hash verification

## 🔐 Hash Verification Example

```
File: example.jpg
MD5:     a1b2c3d4e5f6...
SHA-256: 9f8e7d6c5b4a...
```

Use for:
- Evidence integrity
- Chain of custody
- File identification
- Duplicate detection

## 📈 Statistics Features

The Results tab shows:
- Total files carved
- Valid vs invalid counts
- Total size (bytes & MB)
- File type distribution
- Individual file hashes

## 🌟 Professional Features

1. **Splash Screen** - Professional startup
2. **Menu System** - Complete navigation
3. **Keyboard Shortcuts** - Efficient workflow
4. **Search & Filter** - Quick results
5. **Hash Calculation** - Evidence integrity
6. **Multiple Exports** - Flexible reporting
7. **User Guide** - Built-in help
8. **Dark Theme** - Reduced eye strain

## 🎯 Best Practices

1. Always hash evidence files
2. Export reports for documentation
3. Verify carved files before analysis
4. Use appropriate min file size
5. Keep backups of original evidence
6. Document your findings

## 🔄 Workflow Integration

```
Generate → Carve → Analyze → Export
    ↓        ↓        ↓         ↓
  Evidence  Files   Results  Reports
```

## 📁 Directory Structure

```
forensics-analyzer/
├── evidence/        # Disk images
├── output/          # Results
│   ├── carved_files/
│   └── reports/
└── src/             # Source code
```

---

**Forensics Analyzer v2.0.0**
*Comprehensive Digital Forensics Tool*
