import subprocess
import shutil
import json
from pathlib import Path
from typing import List, Dict

class BinwalkAnalyzer:
    """Wrapper for Binwalk analysis"""
    
    def __init__(self):
        self.results = []
    
    def is_binwalk_available(self) -> bool:
        """Check if binwalk is installed"""
        return shutil.which("binwalk") is not None
    
    def analyze(self, image_path: Path, output_dir: Path) -> List[Dict]:
        """Run binwalk analysis on disk image"""
        self.results = []
        
        if not self.is_binwalk_available():
            print("[!] Binwalk not installed")
            return []
        
        if not image_path.exists():
            print(f"[!] Image not found: {image_path}")
            return []
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[*] Running Binwalk on {image_path.name}...")
        
        try:
            cmd = ["binwalk", "-e", "--directory", str(output_dir), str(image_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self._parse_binwalk_output(result.stdout)
                print(f"[+] Binwalk analysis complete")
            else:
                print(f"[!] Binwalk error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("[!] Binwalk analysis timed out")
        except Exception as e:
            print(f"[!] Binwalk error: {e}")
        
        return self.results
    
    def _parse_binwalk_output(self, output: str):
        """Parse binwalk text output"""
        for line in output.split('\n'):
            line = line.strip()
            if not line or line.startswith('DECIMAL'):
                continue
            
            parts = line.split(None, 2)
            if len(parts) >= 3:
                try:
                    self.results.append({
                        'offset': int(parts[0]),
                        'hex_offset': parts[1],
                        'description': parts[2]
                    })
                except ValueError:
                    continue
    
    def save_report(self, output_path: Path):
        """Save binwalk results to JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2)
            print(f"[+] Binwalk report saved to {output_path}")
        except Exception as e:
            print(f"[!] Error saving binwalk report: {e}")