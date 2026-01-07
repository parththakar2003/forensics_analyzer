"""
Automated Workflow for Forensics Analysis
Takes a path, creates a disk image, embeds files, carves them, and verifies integrity
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from disk_image_generator import DiskImageGenerator
from file_carver import FileCarver
from verify_files import verify_file


class AutomatedForensicsWorkflow:
    """Automated workflow for creating disk images and carving files"""
    
    def __init__(self):
        self.source_path = None
        self.disk_image_path = None
        self.carved_output_dir = None
        self.original_file_hashes = {}
        self.carved_file_hashes = {}
        self.results = {
            'status': 'not_started',
            'original_files': [],
            'carved_files': [],
            'verified_files': [],
            'failed_files': [],
            'statistics': {}
        }
    
    def run_complete_workflow(self, source_path: Path, output_base_dir: Path = None,
                            recursive: bool = False) -> Dict:
        """
        Run the complete automated workflow:
        1. Analyze source path and calculate required size
        2. Create disk image with proper size
        3. Embed all files from source path
        4. Carve files from disk image
        5. Verify carved files match originals
        
        Args:
            source_path: Path to directory or file to analyze
            output_base_dir: Base directory for output (default: parent/output)
            recursive: Whether to include subdirectories
        
        Returns:
            Dictionary with workflow results
        """
        try:
            source_path = Path(source_path)
            
            if not source_path.exists():
                raise FileNotFoundError(f"Source path not found: {source_path}")
            
            # Set up output directories
            if output_base_dir is None:
                output_base_dir = source_path.parent / 'forensics_output'
            else:
                output_base_dir = Path(output_base_dir)
            
            output_base_dir.mkdir(parents=True, exist_ok=True)
            self.disk_image_path = output_base_dir / 'generated_evidence.dd'
            self.carved_output_dir = output_base_dir / 'carved_files'
            self.carved_output_dir.mkdir(parents=True, exist_ok=True)
            
            print("=" * 70)
            print("  AUTOMATED FORENSICS WORKFLOW")
            print("=" * 70)
            
            # Step 1: Analyze source and calculate size
            print("\n[STEP 1] Analyzing source path and calculating required size...")
            print("-" * 70)
            self._analyze_source_path(source_path, recursive)
            
            # Step 2: Generate disk image
            print("\n[STEP 2] Generating disk image with embedded files...")
            print("-" * 70)
            self._generate_disk_image(source_path, recursive)
            
            # Step 3: Carve files
            print("\n[STEP 3] Carving files from disk image...")
            print("-" * 70)
            self._carve_files()
            
            # Step 4: Verify integrity
            print("\n[STEP 4] Verifying file integrity...")
            print("-" * 70)
            self._verify_carved_files()
            
            # Step 5: Generate statistics
            print("\n[STEP 5] Generating statistics...")
            print("-" * 70)
            self._generate_statistics()
            
            self.results['status'] = 'completed'
            
            print("\n" + "=" * 70)
            print("  WORKFLOW COMPLETED SUCCESSFULLY")
            print("=" * 70)
            self._print_summary()
            
            return self.results
            
        except Exception as e:
            print(f"\n[!] Workflow failed: {e}")
            self.results['status'] = 'failed'
            self.results['error'] = str(e)
            import traceback
            traceback.print_exc()
            return self.results
    
    def _analyze_source_path(self, source_path: Path, recursive: bool):
        """Analyze source path and collect file information"""
        self.source_path = source_path
        
        if source_path.is_file():
            files = [source_path]
        elif source_path.is_dir():
            pattern = '**/*' if recursive else '*'
            files = [f for f in source_path.glob(pattern) if f.is_file()]
        else:
            raise ValueError(f"Invalid path: {source_path}")
        
        print(f"[*] Source path: {source_path}")
        print(f"[*] Found {len(files)} file(s)")
        
        # Calculate total size and hash original files
        total_size = 0
        for file_path in files:
            try:
                size = file_path.stat().st_size
                total_size += size
                
                # Calculate hash for verification
                file_hash = self._calculate_file_hash(file_path)
                self.original_file_hashes[file_path.name] = {
                    'hash': file_hash,
                    'size': size,
                    'path': str(file_path)
                }
                
                self.results['original_files'].append({
                    'name': file_path.name,
                    'size': size,
                    'hash': file_hash,
                    'path': str(file_path)
                })
                
                print(f"  [+] {file_path.name} - {size:,} bytes - MD5: {file_hash[:8]}...")
            except Exception as e:
                print(f"  [!] Error processing {file_path.name}: {e}")
        
        print(f"\n[*] Total size of files: {total_size:,} bytes ({total_size / (1024*1024):.2f} MB)")
        
        # Calculate required disk image size
        generator = DiskImageGenerator()
        if source_path.is_file():
            generator.add_real_file(source_path)
        else:
            # Just calculate without adding files yet
            for file_path in files:
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    generator.files_to_embed.append({'data': data, 'type': 'real'})
                except Exception as e:
                    print(f"  [!] Error reading {file_path.name}: {e}")
        
        required_size = generator.calculate_required_size(padding_mb=5)
        print(f"[*] Required disk image size: {required_size} MB")
        
        self.results['statistics']['total_original_files'] = len(files)
        self.results['statistics']['total_original_size'] = total_size
        self.results['statistics']['required_image_size_mb'] = required_size
        
        return required_size
    
    def _generate_disk_image(self, source_path: Path, recursive: bool):
        """Generate disk image with embedded files"""
        generator = DiskImageGenerator()
        
        # Add files from source path
        if source_path.is_file():
            generator.add_real_file(source_path)
        else:
            generator.add_files_from_directory(source_path, recursive=recursive)
        
        # Calculate required size
        required_size = generator.calculate_required_size(padding_mb=5)
        
        # Generate the disk image
        generator.generate(self.disk_image_path, size_mb=required_size)
        
        self.results['disk_image_path'] = str(self.disk_image_path)
        self.results['statistics']['disk_image_size'] = self.disk_image_path.stat().st_size
    
    def _carve_files(self):
        """Carve files from the generated disk image"""
        carver = FileCarver()
        carved_files = carver.carve(self.disk_image_path, self.carved_output_dir, min_size=100)
        
        print(f"[*] Carved {len(carved_files)} files")
        
        # Calculate hashes for carved files
        for carved_file in carved_files:
            carved_path = Path(carved_file['path'])
            if carved_path.exists():
                file_hash = self._calculate_file_hash(carved_path)
                self.carved_file_hashes[carved_path.name] = {
                    'hash': file_hash,
                    'size': carved_file['size'],
                    'path': str(carved_path),
                    'type': carved_file['type']
                }
        
        self.results['carved_files'] = carved_files
        self.results['statistics']['total_carved_files'] = len(carved_files)
    
    def _verify_carved_files(self):
        """Verify that carved files are valid and match originals"""
        verified = []
        failed = []
        
        print("[*] Verifying carved files...")
        
        for carved_path in self.carved_output_dir.glob("*.*"):
            if not carved_path.is_file():
                continue
            
            # Verify file is not corrupted
            is_valid, msg = verify_file(carved_path)
            
            # Calculate hash
            carved_hash = self._calculate_file_hash(carved_path)
            
            # Try to match with original files by hash
            original_match = None
            for orig_name, orig_data in self.original_file_hashes.items():
                if orig_data['hash'] == carved_hash:
                    original_match = orig_name
                    break
            
            result = {
                'carved_name': carved_path.name,
                'size': carved_path.stat().st_size,
                'hash': carved_hash,
                'valid': is_valid,
                'validation_msg': msg,
                'original_match': original_match,
                'path': str(carved_path)
            }
            
            if is_valid:
                verified.append(result)
                status = "✓" if original_match else "✓ (new)"
                match_info = f" matches {original_match}" if original_match else ""
                print(f"  {status} {carved_path.name} - {msg}{match_info}")
            else:
                failed.append(result)
                print(f"  ✗ {carved_path.name} - {msg}")
        
        self.results['verified_files'] = verified
        self.results['failed_files'] = failed
        self.results['statistics']['verified_count'] = len(verified)
        self.results['statistics']['failed_count'] = len(failed)
        
        # Check if all original files were recovered
        recovered_hashes = {v['hash'] for v in verified}
        original_hashes = {v['hash'] for v in self.original_file_hashes.values()}
        
        missing_hashes = original_hashes - recovered_hashes
        self.results['statistics']['missing_originals'] = len(missing_hashes)
        
        if missing_hashes:
            print(f"\n[!] Warning: {len(missing_hashes)} original file(s) not recovered")
    
    def _generate_statistics(self):
        """Generate comprehensive statistics"""
        stats = self.results['statistics']
        
        # Calculate recovery rate
        if stats.get('total_original_files', 0) > 0:
            recovered = stats['total_original_files'] - stats.get('missing_originals', 0)
            stats['recovery_rate'] = (recovered / stats['total_original_files']) * 100
        else:
            stats['recovery_rate'] = 0
        
        # Calculate validation rate
        if stats.get('total_carved_files', 0) > 0:
            stats['validation_rate'] = (stats.get('verified_count', 0) / stats['total_carved_files']) * 100
        else:
            stats['validation_rate'] = 0
    
    def _print_summary(self):
        """Print workflow summary"""
        stats = self.results['statistics']
        
        print("\n📊 WORKFLOW SUMMARY")
        print("-" * 70)
        print(f"Source Path:           {self.source_path}")
        print(f"Disk Image:            {self.disk_image_path}")
        print(f"Carved Output:         {self.carved_output_dir}")
        print(f"\nOriginal Files:        {stats.get('total_original_files', 0)}")
        print(f"Total Size:            {stats.get('total_original_size', 0):,} bytes")
        print(f"Image Size:            {stats.get('required_image_size_mb', 0)} MB")
        print(f"\nCarved Files:          {stats.get('total_carved_files', 0)}")
        print(f"Verified Files:        {stats.get('verified_count', 0)}")
        print(f"Failed Files:          {stats.get('failed_count', 0)}")
        print(f"Missing Originals:     {stats.get('missing_originals', 0)}")
        print(f"\nRecovery Rate:         {stats.get('recovery_rate', 0):.1f}%")
        print(f"Validation Rate:       {stats.get('validation_rate', 0):.1f}%")
        
        if stats.get('recovery_rate', 0) == 100 and stats.get('validation_rate', 0) == 100:
            print("\n✅ All files successfully recovered and verified!")
        elif stats.get('recovery_rate', 0) >= 90:
            print("\n⚠️  Most files recovered successfully")
        else:
            print("\n❌ Some files could not be recovered")
    
    def _calculate_file_hash(self, file_path: Path, algorithm: str = 'md5') -> str:
        """Calculate hash of a file"""
        hash_obj = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()


def run_automated_workflow(source_path: str, output_dir: str = None, recursive: bool = False) -> Dict:
    """
    Convenience function to run the automated workflow
    
    Args:
        source_path: Path to directory or file
        output_dir: Output directory for results
        recursive: Include subdirectories
    
    Returns:
        Dictionary with workflow results
    """
    workflow = AutomatedForensicsWorkflow()
    return workflow.run_complete_workflow(Path(source_path), 
                                         Path(output_dir) if output_dir else None,
                                         recursive)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python automated_workflow.py <source_path> [output_dir] [--recursive]")
        print("\nExample:")
        print("  python automated_workflow.py /path/to/files")
        print("  python automated_workflow.py /path/to/files /output/dir --recursive")
        sys.exit(1)
    
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    recursive = '--recursive' in sys.argv or '-r' in sys.argv
    
    run_automated_workflow(source, output, recursive)
