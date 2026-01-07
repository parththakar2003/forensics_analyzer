from pathlib import Path
import sys

def verify_file(file_path: Path):
    """Verify if a carved file is valid"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read(100)  # Read first 100 bytes
        
        ext = file_path.suffix.lower()
        
        signatures = {
            '.jpg': [b'\xFF\xD8\xFF'],
            '.png': [b'\x89PNG\r\n\x1a\n'],
            '.gif': [b'GIF89a', b'GIF87a'],
            '.pdf': [b'%PDF-'],
            '.zip': [b'PK\x03\x04'],
            '.docx': [b'PK\x03\x04'],
            '.txt': [],  # Text files can start with anything
            '.mp3': [b'ID3'],
        }
        
        if ext not in signatures:
            return True, "Unknown type"
        
        if not signatures[ext]:  # Empty list means any content is valid
            return True, "Text file"
        
        for sig in signatures[ext]:
            if data.startswith(sig):
                return True, "Valid signature"
        
        return False, f"Invalid signature: {data[:10].hex()}"
        
    except Exception as e:
        return False, str(e)

def main():
    """Verify all carved files"""
    base_dir = Path(__file__).parent.parent
    carved_dir = base_dir / "output" / "carved_files"
    
    if not carved_dir.exists():
        print("[!] No carved files directory found")
        return
    
    files = list(carved_dir.glob("*.*"))
    
    if not files:
        print("[!] No carved files found")
        return
    
    print(f"Verifying {len(files)} files...\n")
    
    valid_count = 0
    invalid_count = 0
    
    for file_path in sorted(files):
        is_valid, message = verify_file(file_path)
        
        status = "✓" if is_valid else "✗"
        print(f"{status} {file_path.name:30s} - {message}")
        
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
    
    print(f"\n{'='*60}")
    print(f"Valid files: {valid_count}")
    print(f"Invalid files: {invalid_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()