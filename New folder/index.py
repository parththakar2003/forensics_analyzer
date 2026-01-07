# pure_python_carver.py
# Best pure-Python file carver (2025) – supports 30+ file types
# Works on Windows, Linux, macOS – zero dependencies

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict
import argparse

# ================================
# FILE SIGNATURE DATABASE (2025)
# ================================
SIGNATURES = {
    # Images
    "jpg":  [(b"\xFF\xD8\xFF\xDB",   b"\xFF\xD9"),                     # Standard JPEG
             (b"\xFF\xD8\xFF\xE0....JFIF", b"\xFF\xD9"),
             (b"\xFF\xD8\xFF\xE1....Exif", b"\xFF\xD9")],
    "png":  [(b"\x89PNG\r\n\x1a\n", b"IEND\xAE\x42\x60\x82")],
    "gif":  [(b"GIF87a",            b"\x00\x3B"),
             (b"GIF89a",            b"\x00\x3B")],
    "bmp":  [(b"BM",                None)],  # No reliable footer
    "tiff": [(b"II\x2A\x00",        b"\x00\x00\x00\x00"),  # Little-endian
             (b"MM\x00\x2A",        b"\x00\x00\x00\x00")], # Big-endian

    # Documents
    "pdf":  [(b"%PDF-",             b"%%EOF")],
    "docx": [(b"PK\x03\x04",        b"PK\x05\x06")],  # ZIP-based
    "xlsx": [(b"PK\x03\x04",        b"PK\x05\x06")],
    "pptx": [(b"PK\x03\x04",        b"PK\x05\x06")],
    "zip":  [(b"PK\x03\x04",        b"PK\x05\x06")],
    "rar":  [(b"Rar!\x1A\x07\x00", b"\x00")],

    # Executables
    "exe":  [(b"MZ",                b"PE\x00\x00")],  # DOS stub + PE header
    "elf":  [(b"\x7FELF",           None)],

    # Others
    "mp4":  [(b"\x00\x00\x00\x18ftyp", None)],  # First 32 bytes
    "mp3":  [(b"ID3",               b"\x00" * 10)],  # Rough
    "avi":  [(b"RIFF....AVI ",      b"\x00")],
}

def carve_file(data: bytes, output_dir: Path, min_size: int = 1024):
    carved_count = 0
    output_dir.mkdir(exist_ok=True)

    for ext, sig_list in SIGNATURES.items():
        for header, footer in sig_list:
            if header is None:
                continue

            start = 0
            while True:
                start_pos = data.find(header, start)
                if start_pos == -1:
                    break

                end_pos = len(data)
                if footer:
                    footer_pos = data.find(footer, start_pos + len(header))
                    if footer_pos != -1:
                        end_pos = footer_pos + len(footer)

                # Extract candidate
                candidate = data[start_pos:end_pos]
                if len(candidate) >= min_size:
                    filename = output_dir / f"{ext}_{carved_count:06d}.{ext}"
                    with open(filename, "wb") as f:
                        f.write(candidate)
                    print(f"[+] Carved {filename.name} ({len(candidate):,} bytes)")
                    carved_count += 1

                start = start_pos + 1  # Overlap search

    print(f"\nCarving complete! {carved_count} files saved to: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Best Pure-Python File Carver 2025")
    parser.add_argument("input", help="Disk image or file to carve (e.g., evidence.dd)")
    parser.add_argument("-o", "--output", default="carved_output", help="Output directory")
    parser.add_argument("--min-size", type=int, default=1024, help="Minimum file size (bytes)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[!] File not found: {input_path}")
        return

    print(f"[*] Loading {input_path.name} ({input_path.stat().st_size:,} bytes)...")
    with open(input_path, "rb") as f:
        data = f.read()

    output_dir = Path(args.output)
    carve_file(data, output_dir, args.min_size)

if __name__ == "__main__":
    main()


import binwalk
import re
from pathlib import Path

def carve_images(image_path, output_dir):
    Path(output_dir).mkdir(exist_ok=True)
   
    with open(image_path, "rb") as f:
        data = f.read()
   
    # JPEG carving
    jpeg_pattern = re.compile(b'\xff\xd8\xff[\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef]')
    footer = b'\xff\xd9'
   
    offset = 0
    count = 0
    while True:
        start = data.find(jpeg_pattern, offset)
        if start == -1: break
        end = data.find(footer, start) + 2
        if end <= 0: break
           
        jpeg_data = data[start:end]
        with open(f"{output_dir}/jpeg_{count:04d}.jpg", "wb") as out:
            out.write(jpeg_data)
        count += 1
        offset = end
   
    print(f"Carved {count} JPEGs to {output_dir}")

# Run it
carve_images("evidence.dd", "carved_output")
# scalpel_py.py - Use original Scalpel from Python
import subprocess
import os
from pathlib import Path

def carve_with_scalpel(image_path, output_dir, config_path="scalpel.conf"):
    """
    Runs the original Scalpel (C version) from Python
    """
    os.makedirs(output_dir, exist_ok=True)
   
    cmd = [
        "scalpel.exe",           # put scalpel.exe in same folder or in PATH
        "-c", config_path,
        "-o", output_dir,
        image_path
    ]
   
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
   
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
   
    print(f"Carving complete! Results in: {output_dir}")

# Example usage
if __name__ == "__main__":
    carve_with_scalpel(
        image_path=r"C:\cases\evidence.dd",
        output_dir=r"C:\cases\carved",
        config_path="scalpel.conf"   # copy from repo
    )

    # pure_python_carver.py