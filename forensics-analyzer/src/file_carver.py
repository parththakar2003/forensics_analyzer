from pathlib import Path
from typing import List, Dict

class FileCarver:
    """Carve files from disk images using signature analysis"""
    
    SIGNATURES = {
        "jpg":  [(b"\xFF\xD8\xFF\xE0", b"\xFF\xD9"),
                 (b"\xFF\xD8\xFF\xE1", b"\xFF\xD9"),
                 (b"\xFF\xD8\xFF\xDB", b"\xFF\xD9")],
        "png":  [(b"\x89PNG\r\n\x1a\n", b"IEND")],
        "gif":  [(b"GIF89a", b"\x00\x3B"),
                 (b"GIF87a", b"\x00\x3B")],
        "pdf":  [(b"%PDF-", b"%%EOF")],
        "zip":  [(b"PK\x03\x04", b"PK\x05\x06")],
        "docx": [(b"PK\x03\x04", b"PK\x05\x06")],
        "xlsx": [(b"PK\x03\x04", b"PK\x05\x06")],
        "mp3":  [(b"ID3", None)],
        "txt":  [(b"This is", b"\n\n---END---"), 
                 (b"Lorem ipsum", None)],
    }
    
    def __init__(self):
        self.carved_files = []
    
    def carve(self, image_path: Path, output_dir: Path, min_size: int = 100) -> List[Dict]:
        """Carve files from disk image"""
        self.carved_files = []
        
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
        max_file_size = 50 * 1024 * 1024  # 50MB max per file
        
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
                    end_pos = footer_pos + len(footer)
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
                    
                    print(f"[+] Carved: {filename} ({len(file_data):,} bytes at offset {start_pos})")
                except Exception as e:
                    print(f"[!] Error writing {filename}: {e}")
            
            # Move to next potential file
            start = start_pos + len(header)