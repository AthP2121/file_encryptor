"""
Build script for creating Windows executable using PyInstaller.
"""

import PyInstaller.__main__
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# PyInstaller arguments
args = [
    'main.py',
    '--onefile',
    '--windowed',
    '--name=FileEncryptor',
    f'--distpath={os.path.join(script_dir, "dist")}',
    f'--workpath={os.path.join(script_dir, "build")}',
    f'--specpath={script_dir}',
    '--clean',
    # Add hidden imports if needed
    '--hidden-import=cryptography',
    '--hidden-import=cryptography.fernet',
    '--hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2',
    '--hidden-import=tkinter',
    # Exclude unnecessary modules to reduce size
    '--exclude-module=matplotlib',
    '--exclude-module=PIL',
    '--exclude-module=numpy',
    '--exclude-module=scipy',
]

# Run PyInstaller
PyInstaller.__main__.run(args)

print("\n" + "="*60)
print("Build complete!")
print(f"Executable location: {os.path.join(script_dir, 'dist', 'FileEncryptor.exe')}")
print("="*60)
