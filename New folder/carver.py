import os
import time
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Callable

# ================================
# FILE SIGNATURE DATABASE (2025)
# ================================
SIGNATURES = {
    # Images
    "jpg":  [(b"\xFF\xD8\xFF\xDB",   b"\xFF\xD9"),
             (b"\xFF\xD8\xFF\xE0",   b"\xFF\xD9"),
             (b"\xFF\xD8\xFF\xE1",   b"\xFF\xD9")],
    "png":  [(b"\x89PNG\r\n\x1a\n", b"IEND\xAE\x42\x60\x82")],
    "gif":  [(b"GIF87a",            b"\x00\x3B"),
             (b"GIF89a",            b"\x00\x3B")],
    "bmp":  [(b"BM",                None)],
    "tiff": [(b"II\x2A\x00",        b"\x00\x00\x00\x00"),
             (b"MM\x00\x2A",        b"\x00\x00\x00\x00")],

    # Documents
    "pdf":  [(b"%PDF-",             b"%%EOF")],
    "docx": [(b"PK\x03\x04",        b"PK\x05\x06")],
    "xlsx": [(b"PK\x03\x04",        b"PK\x05\x06")],
    "pptx": [(b"PK\x03\x04",        b"PK\x05\x06")],
    "zip":  [(b"PK\x03\x04",        b"PK\x05\x06")],
    "rar":  [(b"Rar!\x1A\x07\x00", b"\x00")],

    # Executables
    "exe":  [(b"MZ",                b"PE\x00\x00")],
    "elf":  [(b"\x7FELF",           None)],

    # Media
    "mp4":  [(b"\x00\x00\x00\x18ftyp", None)],
    "mp3":  [(b"ID3",               None)],
    "avi":  [(b"RIFF",              None)],
    "wav":  [(b"RIFF",              None)],
}

class Carver:
    def __init__(self):
        self.is_running = False
        self.progress = 0.0
        self.files_found = 0
        self.current_status = "Idle"
        self.carved_files = []
        self.stop_requested = False

    def reset(self):
        self.is_running = False
        self.progress = 0.0
        self.files_found = 0
        self.current_status = "Idle"
        self.carved_files = []
        self.stop_requested = False

    def create_disk_image(self, input_path: Path, output_path: Path):
        self.current_status = f"Creating disk image: {output_path.name}..."
        total_size = input_path.stat().st_size
        copied = 0
        buffer_size = 1024 * 1024 * 10 # 10MB

        with open(input_path, "rb") as src, open(output_path, "wb") as dst:
            while True:
                if self.stop_requested: return False
                chunk = src.read(buffer_size)
                if not chunk: break
                dst.write(chunk)
                copied += len(chunk)
                # Update progress for this stage (0-30%)
                self.progress = (copied / total_size) * 30.0
        return True

    def run_binwalk(self, image_path: Path, output_dir: Path):
        self.current_status = "Running Binwalk analysis..."
        try:
            # Check if binwalk is installed
            import shutil
            if not shutil.which("binwalk"):
                self.current_status = "Binwalk not found. Skipping."
                time.sleep(1)
                return

            # Run binwalk
            # -e: extract, -C: output directory
            cmd = ["binwalk", "-e", "--directory", str(output_dir), str(image_path)]
            
            # We use Popen to not block completely if we wanted to parse stdout for progress,
            # but for simplicity we'll just run it.
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            while process.poll() is None:
                if self.stop_requested:
                    process.terminate()
                    return
                time.sleep(0.1)
                
            self.current_status = "Binwalk complete."
        except Exception as e:
            self.current_status = f"Binwalk error: {str(e)}"
            print(f"Binwalk error: {e}")

    def carve(self, input_path: str, output_dir: str, min_size: int = 1024):
        self.reset()
        self.is_running = True
        
        input_file = Path(input_path)
        out_dir_path = Path(output_dir)
        out_dir_path.mkdir(parents=True, exist_ok=True)
        
        image_path = out_dir_path / "image.dd"

        if not input_file.exists():
            self.current_status = f"Error: File not found: {input_path}"
            self.is_running = False
            return

        try:
            # 1. Create Disk Image
            if not self.create_disk_image(input_file, image_path):
                if self.stop_requested:
                    self.current_status = "Stopped by user."
                self.is_running = False
                return

            # 2. Run Binwalk (30-50% progress roughly, hard to track exact binwalk progress)
            self.progress = 30.0
            self.run_binwalk(image_path, out_dir_path)
            
            # 3. Custom Carving (50-100%)
            self.current_status = f"Carving files from {image_path.name}..."
            file_size = image_path.stat().st_size
            
            with open(image_path, "rb") as f:
                buffer_size = 1024 * 1024 * 10
                offset = 0
                
                while offset < file_size:
                    if self.stop_requested:
                        self.current_status = "Stopped by user."
                        break

                    f.seek(offset)
                    chunk = f.read(buffer_size)
                    if not chunk:
                        break
                    
                    self._process_chunk(chunk, offset, out_dir_path, min_size)
                    
                    offset += len(chunk)
                    
                    # Map 0-100 of carving to 50-100 of total
                    carve_progress = (offset / file_size) * 50.0
                    self.progress = 50.0 + carve_progress
                    
            if not self.stop_requested:
                self.progress = 100.0
                self.current_status = "Completed"
                
        except Exception as e:
            self.current_status = f"Error: {str(e)}"
            import traceback
            traceback.print_exc()
        finally:
            self.is_running = False

    def _process_chunk(self, data: bytes, global_offset: int, output_dir: Path, min_size: int):
        for ext, sig_list in SIGNATURES.items():
            for header, footer in sig_list:
                if header is None: continue

                start = 0
                while True:
                    start_pos = data.find(header, start)
                    if start_pos == -1:
                        break

                    # Found a header
                    # If we have a footer, look for it
                    end_pos = len(data)
                    if footer:
                        footer_pos = data.find(footer, start_pos + len(header))
                        if footer_pos != -1:
                            end_pos = footer_pos + len(footer)
                        else:
                            # Footer not found in this chunk. 
                            # In a real carver, we'd need to read more. 
                            # Here we just take what we have or skip.
                            # Let's skip to avoid corruption.
                            start = start_pos + 1
                            continue
                    else:
                        # No footer, fixed size or guess? 
                        # Let's cap at 5MB for header-only types for safety
                        end_pos = min(start_pos + 5 * 1024 * 1024, len(data))

                    candidate = data[start_pos:end_pos]
                    if len(candidate) >= min_size:
                        filename = f"{ext}_{self.files_found:06d}.{ext}"
                        full_path = output_dir / filename
                        
                        # Avoid overwriting if possible, or just overwrite
                        with open(full_path, "wb") as out_f:
                            out_f.write(candidate)
                        
                        self.files_found += 1
                        self.carved_files.append({
                            "name": filename,
                            "size": len(candidate),
                            "type": ext,
                            "path": str(full_path)
                        })
                    
                    start = start_pos + 1

carver_instance = Carver()
