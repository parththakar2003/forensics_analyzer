# main.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from disk_image_generator import DiskImageGenerator
from file_carver import FileCarver
from file_parser import FileParser
from binwalk_analyzer import BinwalkAnalyzer

def main():
    """Main forensics analysis pipeline"""
    print("=" * 60)
    print("     FORENSICS ANALYZER - Complete Pipeline")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent
    evidence_dir = base_dir / "evidence"
    output_dir = base_dir / "output"
    carved_dir = output_dir / "carved_files"
    
    evidence_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    carved_dir.mkdir(exist_ok=True)
    
    disk_image_path = evidence_dir / "evidence.dd"
    
    print("\n[STEP 1] Generating Disk Image...")
    print("-" * 60)
    
    generator = DiskImageGenerator()
    
    sample_files = [
        {"type": "jpg", "size": 5000},
        {"type": "png", "size": 3000},
        {"type": "gif", "size": 2000},
        {"type": "pdf", "content": "This is a forensics test PDF document with sample content."},
        {"type": "txt", "content": "This is a forensics test text file."},
        {"type": "zip", "size": 2000},
        {"type": "docx", "size": 3000},
        {"type": "mp3", "size": 10000},
    ]
    
    for file_spec in sample_files:
        generator.add_file(file_spec)
    
    generator.generate(disk_image_path, size_mb=5)
    
    if not disk_image_path.exists():
        print("[!] Failed to generate disk image!")
        return
    
    print("\n[STEP 2] Carving Files from Disk Image...")
    print("-" * 60)
    
    carver = FileCarver()
    carved_files = carver.carve(disk_image_path, carved_dir, min_size=100)
    
    print(f"\n[+] Carved {len(carved_files)} files")
    
    print("\n[STEP 3] Parsing Carved Files...")
    print("-" * 60)
    
    parser = FileParser()
    parsed_files = parser.parse_directory(carved_dir)
    
    report_path = output_dir / "parse_report.json"
    parser.save_report(report_path)
    
    stats = parser.get_statistics()
    print("\n[*] Statistics:")
    print(f"    Total files: {stats.get('total_files', 0)}")
    print(f"    Total size: {stats.get('total_size', 0):,} bytes")
    print(f"    Valid files: {stats.get('valid_files', 0)}")
    print(f"    Invalid files: {stats.get('invalid_files', 0)}")
    print(f"    File types: {stats.get('extensions', {})}")
    
    print("\n[STEP 4] Running Binwalk Analysis...")
    print("-" * 60)
    
    analyzer = BinwalkAnalyzer()
    
    if analyzer.is_binwalk_available():
        binwalk_output_dir = output_dir / "binwalk_analysis"
        results = analyzer.analyze(disk_image_path, binwalk_output_dir)
        
        binwalk_report = output_dir / "binwalk_report.json"
        analyzer.save_report(binwalk_report)
        
        print(f"[+] Binwalk found {len(results)} signatures")
    else:
        print("[!] Binwalk not available - skipping")
    
    print("\n" + "=" * 60)
    print("     ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nResults saved to: {output_dir}")
    print(f"  - Disk Image: {disk_image_path}")
    print(f"  - Carved Files: {carved_dir}")
    print(f"  - Parse Report: {report_path}")
    if analyzer.is_binwalk_available():
        print(f"  - Binwalk Report: {binwalk_report}")
    
    print("\n[*] Verifying carved files...")
    from verify_files import verify_file
    for carved_file in carved_dir.glob("*.*"):
        is_valid, msg = verify_file(carved_file)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {carved_file.name} - {msg}")
    
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Analysis interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()