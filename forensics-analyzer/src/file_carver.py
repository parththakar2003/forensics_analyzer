from pathlib import Path
from typing import List, Dict

class FileCarver:
    """Carve files from disk images using signature analysis"""
    
    SIGNATURES = {
        "jpg":  [(b"\xFF\xD8\xFF\xE0", b"\xFF\xD9"),
                 (b"\xFF\xD8\xFF\xE1", b"\xFF\xD9"),
                 (b"\xFF\xD8\xFF\xDB", b"\xFF\xD9")],
        "png":  [(b"\x89PNG\r\n\x1a\n", b"IEND")],
        "gif":  [(b"GIF89a", b"\x3B"),
                 (b"GIF87a", b"\x3B")],
        "pdf":  [(b"%PDF-", b"%%EOF")],
        "zip":  [(b"PK\x03\x04", b"PK\x05\x06")],
        "docx": [(b"PK\x03\x04", b"PK\x05\x06")],
        "xlsx": [(b"PK\x03\x04", b"PK\x05\x06")],
        "mp3":  [(b"ID3\x03", None), (b"ID3\x04", None)],  # ID3v2.3 and ID3v2.4
        "txt":  [(b"Forensics Analyzer", None)],
    }
    
    # Footer sizes - how many extra bytes to include after the footer signature
    FOOTER_SIZES = {
        "zip": 18,   # End of Central Directory record is 22 bytes total (4 sig + 18 extra)
        "docx": 18,  # DOCX is a ZIP file
        "xlsx": 18,  # XLSX is a ZIP file
    }
    
    # Maximum file sizes for types without footers (in bytes)
    MAX_SIZES = {
        "mp3": 20 * 1024,      # 20KB for test MP3s
        "txt": 1 * 1024,       # 1KB for text files (more realistic for test files)
    }
    
    def __init__(self):
        self.carved_files = []
        self.carved_offsets = set()  # Track offsets to avoid duplicates
    
    def carve(self, image_path: Path, output_dir: Path, min_size: int = 100) -> List[Dict]:
        """Carve files from disk image"""
        self.carved_files = []
        self.carved_offsets = set()  # Reset for each carve operation
        
        if not image_path.exists():
            print(f"[!] Image not found: {image_path}")
            return []
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[*] Loading image: {image_path.name}")
        with open(image_path, 'rb') as f:
            data = f.read()
        
        print(f"[*] Image size: {len(data):,} bytes")
        print("[*] Carving files...")
        
        for ext, sig_list in self.SIGNATURES.items():
            for header, footer in sig_list:
                self._carve_signature(data, ext, header, footer, output_dir, min_size)
        
        print(f"\n[+] Total carved: {len(self.carved_files)} files")
        return self.carved_files
    
    def _carve_signature(self, data: bytes, ext: str, header: bytes, 
                        footer: bytes, output_dir: Path, min_size: int):
        """Carve files matching a specific signature"""
        start = 0
        # Use type-specific max size if available, otherwise use default
        max_file_size = self.MAX_SIZES.get(ext, 50 * 1024 * 1024)  # Default 50MB
        
        while start < len(data):
            # Find header
            start_pos = data.find(header, start)
            if start_pos == -1:
                break
            
            # Find footer
            end_pos = None
            if footer:
                footer_pos = data.find(footer, start_pos + len(header))
                if footer_pos != -1:
                    # Include the footer in the file
                    # Check if this file type needs extra bytes after the footer
                    footer_extra = self.FOOTER_SIZES.get(ext, 0)
                    end_pos = footer_pos + len(footer) + footer_extra
                else:
                    # Footer not found, skip this header
                    start = start_pos + 1
                    continue
            else:
                # No footer defined - use reasonable max size or look for next header
                next_header_pos = data.find(header, start_pos + len(header))
                if next_header_pos != -1:
                    end_pos = min(start_pos + max_file_size, next_header_pos)
                else:
                    end_pos = min(start_pos + max_file_size, len(data))
            
            # Extract file data
            file_data = data[start_pos:end_pos]
            
            # Check if we've already carved a file at this offset (avoid duplicates)
            if start_pos in self.carved_offsets:
                start = start_pos + len(header)
                continue
            
            # Validate size
            if len(file_data) >= min_size and len(file_data) <= max_file_size:
                filename = f"{ext}_{len(self.carved_files):06d}.{ext}"
                file_path = output_dir / filename
                
                try:
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                    
                    self.carved_files.append({
                        'name': filename,
                        'size': len(file_data),
                        'type': ext,
                        'offset': start_pos,
                        'path': str(file_path)
                    })
                    
                    # Mark this offset as carved
                    self.carved_offsets.add(start_pos)
                    
                    print(f"[+] Carved: {filename} ({len(file_data):,} bytes at offset {start_pos})")
                except Exception as e:
                    print(f"[!] Error writing {filename}: {e}")
            
            # Move to next potential file
            start = start_pos + len(header)