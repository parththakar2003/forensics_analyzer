import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    print("=" * 60)
    print("Binwalk Installation Script for Windows")
    print("=" * 60)
    
    packages = [
        "binwalk",
        "python-magic-bin",  # Windows-specific magic library
        "pillow",            # Image support
        "matplotlib",        # Entropy visualization
        "pyqtgraph",        # GUI support
    ]
    
    print("\nInstalling packages...")
    results = {}
    
    for package in packages:
        results[package] = install_package(package)
    
    print("\n" + "=" * 60)
    print("Installation Summary")
    print("=" * 60)
    
    for package, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {package}")
    
    # Test binwalk
    print("\n" + "=" * 60)
    print("Testing Binwalk Installation")
    print("=" * 60)
    
    try:
        import binwalk
        print(f"✓ Binwalk version: {binwalk.__version__}")
        print("✓ Binwalk is ready to use!")
    except ImportError as e:
        print(f"✗ Binwalk import failed: {e}")
        print("\nTry running: pip install --upgrade binwalk")
    
    print("\n" + "=" * 60)
    print("Additional Tools (Optional)")
    print("=" * 60)
    print("For better extraction capabilities, install:")
    print("1. 7-Zip: https://www.7-zip.org/download.html")
    print("2. Add 7-Zip to PATH environment variable")
    print("\n")

if __name__ == "__main__":
    main()