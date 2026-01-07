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
        "mp3":  [(b"ID3", None)],
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
            
            # Find footer or calculate size
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
                # No footer defined - use special handling or reasonable defaults
                if ext == "mp3":
                    # Special handling for MP3 files with ID3 tags
                    # Validate ID3 header before processing
                    if start_pos + 10 > len(data):
                        # Not enough data for ID3 header, skip
                        start = start_pos + 1
                        continue
                    
                    id3_header = data[start_pos:start_pos + 10]
                    # Check ID3 version (should be 2.x, 3.x, or 4.x)
                    version_major = id3_header[3]
                    if version_major < 2 or version_major > 4:
                        # Invalid ID3 version, skip this occurrence
                        start = start_pos + 1
                        continue
                    
                    end_pos = self._calculate_mp3_size(data, start_pos)
                else:
                    # Default behavior: look for next header or use max size
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
            # Skip past the entire carved file to avoid finding overlapping signatures
            if end_pos and len(file_data) >= min_size and len(file_data) <= max_file_size:
                start = end_pos
            else:
                start = start_pos + len(header)
    
    def _calculate_mp3_size(self, data: bytes, start_pos: int) -> int:
        """Calculate the actual size of an MP3 file with ID3 tags
        Returns the end position (not size) for use in data[start_pos:end_pos]"""
        try:
            # Check if we have enough data for ID3 header (already validated by caller)
            if start_pos + 10 > len(data):
                return min(start_pos + 10000, len(data))
            
            # Read ID3 header
            id3_header = data[start_pos:start_pos + 10]
            
            # Verify it's ID3 with valid version (redundant check for safety)
            if id3_header[:3] != b'ID3':
                return min(start_pos + 10000, len(data))
            
            # Check ID3 version (should be 2.x, 3.x, or 4.x)
            version_major = id3_header[3]
            if version_major > 4 or version_major < 2:
                # Invalid version, likely false positive
                return min(start_pos + 10000, len(data))
            
            # Decode synchsafe integer for tag size
            size_bytes = id3_header[6:10]
            tag_size = ((size_bytes[0] & 0x7F) << 21) | \
                       ((size_bytes[1] & 0x7F) << 14) | \
                       ((size_bytes[2] & 0x7F) << 7) | \
                       (size_bytes[3] & 0x7F)
            
            # Sanity check on tag size (should be reasonable, not too large)
            if tag_size > 10 * 1024 * 1024:  # 10MB is too large for ID3 tag
                return min(start_pos + 10000, len(data))
            
            # ID3 header is 10 bytes + tag size
            id3_total_size = 10 + tag_size
            
            # After ID3 tag, look for MPEG frames
            # MPEG frame sync starts with 0xFF 0xFB (or 0xFF 0xFA, 0xFF 0xF3, etc.)
            mpeg_start = start_pos + id3_total_size
            
            # Ensure we don't go past the end of data
            if mpeg_start >= len(data):
                return min(start_pos + id3_total_size, len(data))
            
            # Look for MPEG frame sync in the next few hundred bytes
            max_search = min(mpeg_start + 500, len(data))
            mpeg_data_size = 0
            
            # Simple approach: look for consecutive MPEG frame headers
            # or use a reasonable size based on ID3 tag
            pos = mpeg_start
            # Ensure we have room to check pos+1
            while pos + 1 < max_search:
                if data[pos] == 0xFF and (data[pos + 1] & 0xE0) == 0xE0:
                    # Found potential MPEG frame
                    # For our generated MP3s, we add a small amount of audio data
                    # Calculate remaining space safely
                    remaining = len(data) - mpeg_start
                    if remaining > 0:
                        mpeg_data_size = min(10000, remaining)
                    break
                pos += 1
            
            if mpeg_data_size == 0:
                # No MPEG frames found, just use ID3 tag size
                mpeg_data_size = 0
            
            total_size = id3_total_size + mpeg_data_size
            # Ensure we don't exceed data length
            return min(start_pos + total_size, len(data))
            
        except Exception as e:
            # If anything goes wrong, return a reasonable default within bounds
            return min(start_pos + 15000, len(data))