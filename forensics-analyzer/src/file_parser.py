import os
import json
from pathlib import Path
from typing import Dict, List, Any

class FileParser:
    """Parse and analyze carved files"""
    
    def __init__(self):
        self.parsed_files = []
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a single file and extract metadata"""
        try:
            stats = file_path.stat()
            
            file_info = {
                'name': file_path.name,
                'path': str(file_path),
                'size': stats.st_size,
                'extension': file_path.suffix.lower(),
                'created': stats.st_ctime,
                'modified': stats.st_mtime,
            }
            
            with open(file_path, 'rb') as f:
                header = f.read(16)
                file_info['header'] = header.hex()
                file_info['is_valid'] = self._validate_file(file_path.suffix.lower(), header)
            
            return file_info
            
        except Exception as e:
            return {
                'name': file_path.name,
                'path': str(file_path),
                'error': str(e)
            }
    
    def _validate_file(self, extension: str, header: bytes) -> bool:
        """Validate file based on magic bytes"""
        signatures = {
            '.jpg': [b'\xFF\xD8\xFF\xDB', b'\xFF\xD8\xFF\xE0', b'\xFF\xD8\xFF\xE1'],
            '.jpeg': [b'\xFF\xD8\xFF\xDB', b'\xFF\xD8\xFF\xE0', b'\xFF\xD8\xFF\xE1'],
            '.png': [b'\x89PNG\r\n\x1a\n'],
            '.gif': [b'GIF87a', b'GIF89a'],
            '.pdf': [b'%PDF-'],
            '.zip': [b'PK\x03\x04'],
            '.docx': [b'PK\x03\x04'],
            '.mp3': [b'ID3'],
        }
        
        if extension not in signatures:
            return True
        
        for sig in signatures[extension]:
            if header.startswith(sig):
                return True
        
        return False
    
    def parse_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """Parse all files in a directory"""
        self.parsed_files = []
        
        if not directory.exists():
            print(f"[!] Directory not found: {directory}")
            return []
        
        print(f"[*] Parsing files in {directory}...")
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix:
                file_info = self.parse_file(file_path)
                self.parsed_files.append(file_info)
        
        print(f"[+] Parsed {len(self.parsed_files)} files")
        return self.parsed_files
    
    def save_report(self, output_path: Path):
        """Save parsing report as JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.parsed_files, f, indent=2)
            print(f"[+] Report saved to {output_path}")
        except Exception as e:
            print(f"[!] Error saving report: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about parsed files"""
        if not self.parsed_files:
            return {}
        
        total_size = sum(f.get('size', 0) for f in self.parsed_files)
        extensions = {}
        valid_count = 0
        invalid_count = 0
        
        for f in self.parsed_files:
            ext = f.get('extension', 'unknown')
            extensions[ext] = extensions.get(ext, 0) + 1
            
            if f.get('is_valid'):
                valid_count += 1
            else:
                invalid_count += 1
        
        return {
            'total_files': len(self.parsed_files),
            'total_size': total_size,
            'valid_files': valid_count,
            'invalid_files': invalid_count,
            'extensions': extensions
        }