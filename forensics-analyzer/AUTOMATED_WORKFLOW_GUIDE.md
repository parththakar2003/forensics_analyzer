# Quick Start Guide - Automated Workflow

## 🚀 The Fastest Way to Use Forensics Analyzer

This guide shows you how to use the new **Automated Workflow** feature - the easiest way to perform complete forensic analysis.

## What Does It Do?

The automated workflow takes a path (directory or file) and automatically:

1. ✅ **Calculates image size** - Analyzes your files and determines the perfect disk image size
2. ✅ **Creates .dd file** - Generates a disk image with proper size (not too big, not too small)
3. ✅ **Embeds real files** - Puts your actual files into the disk image
4. ✅ **Carves files** - Extracts files using forensic carving techniques
5. ✅ **Verifies integrity** - Ensures carved files match originals and are not corrupted
6. ✅ **Generates report** - Creates comprehensive statistics and analysis

All with **one click**! 🎉

## GUI Method (Recommended)

### Step 1: Launch the Application
```bash
python src/gui.py
```

### Step 2: Use Automated Workflow
1. Go to the **"Generate & Carve"** tab
2. Look for the **"🚀 Automated Workflow (Recommended)"** section at the top
3. Click **"Browse"** next to "Source Path"
   - Select a directory with files, OR
   - Select a single file
4. Choose an output directory (or use default)
5. Optionally check **"Include subdirectories"** if you want recursive processing
6. Click the big **"⚡ Run Complete Workflow"** button

### Step 3: Watch the Magic Happen
The console will show:
- Files being analyzed
- Image size being calculated
- Disk image being created
- Files being embedded
- Files being carved
- Verification results

### Step 4: Review Results
You'll get a summary showing:
- How many files were processed
- Recovery rate (% of files successfully recovered)
- Validation rate (% of files that are not corrupted)
- Location of output files

## CLI Method (For Automation)

### Basic Usage
```bash
python src/automated_workflow.py /path/to/source /path/to/output
```

### With Subdirectories
```bash
python src/automated_workflow.py /path/to/source /path/to/output --recursive
```

### Single File
```bash
python src/automated_workflow.py /path/to/file.jpg /path/to/output
```

## Example Workflow

Let's say you have a folder `/home/user/evidence` with these files:
```
evidence/
├── photo1.jpg
├── photo2.png
├── document.pdf
└── data.zip
```

### Using GUI:
1. Launch: `python src/gui.py`
2. Browse to `/home/user/evidence`
3. Click "⚡ Run Complete Workflow"
4. Get results in `/output/automated/`

### Using CLI:
```bash
python src/automated_workflow.py /home/user/evidence /home/user/results
```

## What You Get

After running the automated workflow, you'll have:

```
output/
├── generated_evidence.dd      # Disk image (auto-sized!)
├── carved_files/              # All carved files
│   ├── jpg_000000.jpg        # Matches photo1.jpg
│   ├── png_000001.png        # Matches photo2.png
│   ├── pdf_000002.pdf        # Matches document.pdf
│   └── zip_000003.zip        # Matches data.zip
└── workflow_results.json      # Detailed report
```

## Understanding the Results

### Console Output
```
📊 WORKFLOW SUMMARY
----------------------------------------------------------------------
Original Files:        4
Total Size:            2,458 bytes
Image Size:            6 MB

Carved Files:          4
Verified Files:        4
Failed Files:          0
Missing Originals:     0

Recovery Rate:         100.0%
Validation Rate:       100.0%

✅ All files successfully recovered and verified!
```

### What the Numbers Mean:

- **Recovery Rate**: % of original files that were found in carved results
- **Validation Rate**: % of carved files that are valid (not corrupted)
- **100% validation** = All carved files open correctly! ✅

## Supported File Types

Works with files that have recognizable signatures:

✅ **Images**: JPG, PNG, GIF, BMP, TIFF
✅ **Documents**: PDF, DOCX, XLSX, PPTX  
✅ **Archives**: ZIP, RAR
✅ **Media**: MP3, MP4, AVI, WAV
✅ **Executables**: EXE, ELF

## Pro Tips

### Tip 1: Start Small
Test with a small directory first (5-10 files) to understand the process.

### Tip 2: Check File Types
The automated workflow works best with files that have clear signatures (JPG, PDF, ZIP, etc.)

### Tip 3: Review the Report
After completion, check `workflow_results.json` for detailed information:
```json
{
  "status": "completed",
  "statistics": {
    "total_original_files": 4,
    "total_carved_files": 4,
    "verified_count": 4,
    "recovery_rate": 100.0,
    "validation_rate": 100.0
  }
}
```

### Tip 4: Verify Carved Files
The workflow automatically verifies files, but you can also manually check:
- Try opening carved files
- Compare file sizes
- Check MD5 hashes in the report

## Troubleshooting

### "No files were carved"
- **Cause**: Source files may not have recognizable signatures
- **Solution**: Use files with clear signatures (JPG, PDF, ZIP, etc.)

### "Recovery rate is low"
- **Cause**: Some file types are harder to carve
- **Solution**: This is normal for certain file types

### "Missing Originals: 1"
- **Cause**: Hash might differ slightly (e.g., PDF EOF handling)
- **Check**: Validation rate - if 100%, files are still valid!

## Advanced: Python API

You can also use the workflow programmatically:

```python
from pathlib import Path
from automated_workflow import AutomatedForensicsWorkflow

# Create workflow instance
workflow = AutomatedForensicsWorkflow()

# Run complete workflow
results = workflow.run_complete_workflow(
    source_path=Path("/path/to/source"),
    output_base_dir=Path("/path/to/output"),
    recursive=True  # Include subdirectories
)

# Check results
if results['status'] == 'completed':
    stats = results['statistics']
    print(f"✅ Success!")
    print(f"Recovery: {stats['recovery_rate']}%")
    print(f"Validation: {stats['validation_rate']}%")
else:
    print(f"❌ Failed: {results['error']}")
```

## Next Steps

After mastering the automated workflow:

1. **Explore Manual Mode**: Use individual steps for more control
2. **Try Binwalk**: Run advanced binary analysis
3. **Export Reports**: Generate HTML reports for presentations
4. **Calculate Hashes**: Use the hash calculator for evidence integrity

## Need Help?

- Press **F1** in the GUI for the complete user guide
- Check the main **README.md** for detailed documentation
- Review **GUI_FEATURES.md** for all GUI features

---

**Happy Analyzing!** 🔍✨
