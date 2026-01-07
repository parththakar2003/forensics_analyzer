import os
import random
from pathlib import Path
from typing import List, Dict, Any
from io import BytesIO

class DiskImageGenerator:
    """Generate a synthetic disk image with embedded files"""
    
    def __init__(self):
        self.files_to_embed = []
    
    def add_file(self, file_spec: Dict[str, Any]):
        """Add a file specification to embed in the disk image"""
        self.files_to_embed.append(file_spec)
    
    def generate(self, output_path: Path, size_mb: int = 10):
        """Generate the disk image"""
        print(f"[*] Generating disk image: {output_path} ({size_mb} MB)")
        
        total_size = size_mb * 1024 * 1024
        image_data = bytearray(total_size)
        
        print("[*] Filling with random data...")
        for i in range(0, total_size, 4096):
            chunk_size = min(4096, total_size - i)
            image_data[i:i+chunk_size] = os.urandom(chunk_size)
        
        print(f"[*] Embedding {len(self.files_to_embed)} files...")
        offset = 10000  # Start after some random data
        
        for idx, file_spec in enumerate(self.files_to_embed):
            file_type = file_spec.get('type', 'txt')
            
            try:
                file_data = self._generate_file_data(file_spec)
                
                if offset + len(file_data) < total_size:
                    image_data[offset:offset+len(file_data)] = file_data
                    print(f"[+] Embedded {file_type} file #{idx+1} at offset {offset} ({len(file_data)} bytes)")
                    offset += len(file_data) + random.randint(5000, 10000)
                else:
                    print(f"[!] Not enough space for {file_type} file")
                    
            except Exception as e:
                print(f"[!] Error embedding {file_type}: {e}")
        
        print(f"[*] Writing disk image to {output_path}...")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"[+] Disk image created successfully ({output_path.stat().st_size:,} bytes)")
    
    def _generate_file_data(self, file_spec: Dict[str, Any]) -> bytes:
        """Generate proper file data based on specification"""
        file_type = file_spec.get('type', 'txt')
        size = file_spec.get('size', 10000)
        content = file_spec.get('content', None)
        
        if file_type == 'jpg':
            return self._generate_jpg(size)
        elif file_type == 'png':
            return self._generate_png(size)
        elif file_type == 'gif':
            return self._generate_gif(size)
        elif file_type == 'pdf':
            return self._generate_pdf(content or "Sample PDF content")
        elif file_type == 'txt':
            return self._generate_txt(content or "Sample text file content")
        elif file_type in ['zip', 'docx', 'xlsx', 'pptx']:
            return self._generate_zip(size)
        elif file_type == 'mp3':
            return self._generate_mp3(size)
        else:
            return b"Unknown file type"
    
    def _generate_jpg(self, size: int) -> bytes:
        """Generate a minimal valid JPEG"""
        # Minimal JPEG structure
        data = bytearray()
        
        # SOI (Start of Image)
        data.extend(b'\xFF\xD8')
        
        # APP0 (JFIF marker)
        data.extend(b'\xFF\xE0')
        data.extend(b'\x00\x10')  # Length
        data.extend(b'JFIF\x00')
        data.extend(b'\x01\x01')  # Version
        data.extend(b'\x00')      # Density units
        data.extend(b'\x00\x01\x00\x01')  # X/Y density
        data.extend(b'\x00\x00')  # Thumbnail
        
        # SOF0 (Start of Frame)
        data.extend(b'\xFF\xC0')
        data.extend(b'\x00\x11')  # Length
        data.extend(b'\x08')      # Precision
        data.extend(b'\x00\x10\x00\x10')  # Height, Width (16x16)
        data.extend(b'\x03')      # Components
        data.extend(b'\x01\x22\x00')  # Y component
        data.extend(b'\x02\x11\x01')  # Cb component
        data.extend(b'\x03\x11\x01')  # Cr component
        
        # Add some fake image data
        remaining = max(0, size - len(data) - 2)
        if remaining > 100:
            # SOS (Start of Scan)
            data.extend(b'\xFF\xDA')
            data.extend(b'\x00\x0C')
            data.extend(b'\x03\x01\x00\x02\x11\x03\x11\x00\x3F\x00')
            
            # Fake compressed data
            data.extend(os.urandom(remaining - 50))
        
        # EOI (End of Image)
        data.extend(b'\xFF\xD9')
        
        return bytes(data)
    
    def _generate_png(self, size: int) -> bytes:
        """Generate a minimal valid PNG"""
        data = bytearray()
        
        # PNG signature
        data.extend(b'\x89PNG\r\n\x1a\n')
        
        # IHDR chunk (Image Header)
        ihdr_data = b'\x00\x00\x00\x10'  # Width: 16
        ihdr_data += b'\x00\x00\x00\x10'  # Height: 16
        ihdr_data += b'\x08'              # Bit depth: 8
        ihdr_data += b'\x02'              # Color type: RGB
        ihdr_data += b'\x00'              # Compression
        ihdr_data += b'\x00'              # Filter
        ihdr_data += b'\x00'              # Interlace
        
        data.extend(self._png_chunk(b'IHDR', ihdr_data))
        
        # IDAT chunk (Image Data) - minimal
        import zlib
        raw_data = b'\x00' * (16 * 16 * 3 + 16)  # Minimal image data
        compressed = zlib.compress(raw_data)
        data.extend(self._png_chunk(b'IDAT', compressed))
        
        # Add padding if needed
        remaining = max(0, size - len(data) - 12)
        if remaining > 0:
            data.extend(self._png_chunk(b'tEXt', b'Comment\x00' + os.urandom(min(remaining, 1000))))
        
        # IEND chunk
        data.extend(self._png_chunk(b'IEND', b''))
        
        return bytes(data)
    
    def _png_chunk(self, chunk_type: bytes, chunk_data: bytes) -> bytes:
        """Create a PNG chunk with CRC"""
        import struct
        import zlib
        
        length = struct.pack('>I', len(chunk_data))
        chunk = chunk_type + chunk_data
        crc = struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
        
        return length + chunk + crc
    
    def _generate_gif(self, size: int) -> bytes:
        """Generate a minimal valid GIF"""
        data = bytearray()
        
        # Header
        data.extend(b'GIF89a')
        
        # Logical Screen Descriptor
        data.extend(b'\x10\x00')  # Width: 16
        data.extend(b'\x10\x00')  # Height: 16
        data.extend(b'\xF0')      # Global Color Table Flag
        data.extend(b'\x00')      # Background Color Index
        data.extend(b'\x00')      # Pixel Aspect Ratio
        
        # Global Color Table (2 colors)
        data.extend(b'\x00\x00\x00')  # Black
        data.extend(b'\xFF\xFF\xFF')  # White
        
        # Image Descriptor
        data.extend(b'\x2C')
        data.extend(b'\x00\x00\x00\x00')  # Left, Top
        data.extend(b'\x10\x00\x10\x00')  # Width, Height
        data.extend(b'\x00')              # Flags
        
        # Image Data
        data.extend(b'\x02')  # LZW Minimum Code Size
        data.extend(b'\x02')  # Block Size
        data.extend(b'\x4C\x01')  # Compressed data
        data.extend(b'\x00')  # Block Terminator
        
        # Trailer
        data.extend(b'\x3B')
        
        return bytes(data)
    
    def _generate_pdf(self, content: str) -> bytes:
        """Generate a minimal valid PDF"""
        pdf = f"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length {len(content) + 50}
>>
stream
BT
/F1 12 Tf
50 700 Td
({content}) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
{400 + len(content)}
%%EOF
"""
        return pdf.encode('latin-1')
    
    def _generate_txt(self, content: str) -> bytes:
        """Generate a text file"""
        full_content = f"""{content}

This is a generated text file for forensics testing.
Created by Forensics Analyzer.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
"""
        return full_content.encode('utf-8')
    
    def _generate_zip(self, size: int) -> bytes:
        """Generate a minimal valid ZIP"""
        import struct
        import time
        
        data = bytearray()
        
        # Local file header
        data.extend(b'PK\x03\x04')  # Signature
        data.extend(b'\x14\x00')    # Version
        data.extend(b'\x00\x00')    # Flags
        data.extend(b'\x00\x00')    # Compression method (stored)
        
        # DOS time/date
        t = time.localtime()
        dos_time = (t.tm_hour << 11) | (t.tm_min << 5) | (t.tm_sec // 2)
        dos_date = ((t.tm_year - 1980) << 9) | (t.tm_mon << 5) | t.tm_mday
        data.extend(struct.pack('<HH', dos_time, dos_date))
        
        # File content
        file_content = b'This is a test file in the ZIP archive.'
        
        # CRC-32
        import zlib
        crc = zlib.crc32(file_content)
        data.extend(struct.pack('<I', crc))
        
        # Sizes
        data.extend(struct.pack('<I', len(file_content)))  # Compressed size
        data.extend(struct.pack('<I', len(file_content)))  # Uncompressed size
        
        # Filename
        filename = b'test.txt'
        data.extend(struct.pack('<H', len(filename)))  # Filename length
        data.extend(b'\x00\x00')  # Extra field length
        data.extend(filename)
        data.extend(file_content)
        
        # Central directory header
        central_start = len(data)
        data.extend(b'PK\x01\x02')
        data.extend(b'\x14\x00' * 2)
        data.extend(b'\x00\x00')
        data.extend(b'\x00\x00')
        data.extend(struct.pack('<HH', dos_time, dos_date))
        data.extend(struct.pack('<I', crc))
        data.extend(struct.pack('<I', len(file_content)))
        data.extend(struct.pack('<I', len(file_content)))
        data.extend(struct.pack('<H', len(filename)))
        data.extend(b'\x00\x00' * 3)
        data.extend(b'\x00\x00\x00\x00')
        data.extend(b'\x00\x00\x00\x00')
        data.extend(filename)
        
        # End of central directory
        central_size = len(data) - central_start
        data.extend(b'PK\x05\x06')
        data.extend(b'\x00\x00' * 2)
        data.extend(b'\x01\x00' * 2)
        data.extend(struct.pack('<I', central_size))
        data.extend(struct.pack('<I', central_start))
        data.extend(b'\x00\x00')
        
        return bytes(data)
    
    def _generate_mp3(self, size: int) -> bytes:
        """Generate a minimal valid MP3"""
        data = bytearray()
        
        # ID3v2 header
        data.extend(b'ID3')
        data.extend(b'\x03\x00')  # Version 2.3
        data.extend(b'\x00')      # Flags
        
        # Size (synchsafe integer)
        tag_size = 1024
        data.extend(bytes([
            (tag_size >> 21) & 0x7F,
            (tag_size >> 14) & 0x7F,
            (tag_size >> 7) & 0x7F,
            tag_size & 0x7F
        ]))
        
        # TIT2 frame (Title)
        title = b'Test Audio'
        frame_size = len(title) + 1
        data.extend(b'TIT2')
        data.extend(frame_size.to_bytes(4, 'big'))
        data.extend(b'\x00\x00')  # Flags
        data.extend(b'\x00')      # Encoding
        data.extend(title)
        
        # Padding
        data.extend(b'\x00' * (tag_size - len(data) + 10))
        
        # MP3 frame header (minimal)
        data.extend(b'\xFF\xFB')  # Sync + MPEG 1 Layer 3
        data.extend(b'\x90\x00')  # Bitrate + Frequency
        
        # Add some fake audio data
        remaining = max(0, size - len(data))
        if remaining > 0:
            data.extend(os.urandom(min(remaining, 10000)))
        
        return bytes(data)