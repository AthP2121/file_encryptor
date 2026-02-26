"""
File operations including compression, search, and I/O handling.
"""

import os
import zipfile
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from config import *


class FileManager:
    """Handles file and folder operations."""

    @staticmethod
    def compress_folder(folder_path, output_path):
        """Compress a folder to ZIP format."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            folder_path = Path(folder_path)
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(folder_path.parent)
                    zipf.write(file_path, arcname)

    @staticmethod
    def extract_folder(zip_path, output_dir):
        """Extract a ZIP file to a directory."""
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(output_dir)

    @staticmethod
    def search_files(directory, pattern='*', recursive=True, only_locked=False, extension_filter=None):
        """
        Search for files in a directory.

        Args:
            directory: Root directory to search
            pattern: Filename pattern (supports wildcards)
            recursive: Search subdirectories
            only_locked: Only return .locked files
            extension_filter: Filter by file extension (e.g., '.txt')

        Returns:
            List of file paths
        """
        results = []
        directory = Path(directory)

        if not directory.exists():
            return results

        # Choose search method
        if recursive:
            search_pattern = f"**/{pattern}"
        else:
            search_pattern = pattern

        # Search files
        for file_path in directory.glob(search_pattern):
            if not file_path.is_file():
                continue

            # Apply filters
            if only_locked and not str(file_path).endswith(ENCRYPTED_EXTENSION):
                continue

            if extension_filter and not str(file_path).endswith(extension_filter):
                continue

            results.append(str(file_path))

        return sorted(results)

    @staticmethod
    def get_file_info(filepath):
        """Get file information."""
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime)
        }

    @staticmethod
    def create_temp_file(suffix=''):
        """Create a temporary file."""
        fd, path = tempfile.mkstemp(prefix=TEMP_FILE_PREFIX, suffix=suffix)
        os.close(fd)
        return path

    @staticmethod
    def safe_delete(filepath):
        """Safely delete a file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
            return False

    @staticmethod
    def get_encrypted_filename(original_path):
        """Generate encrypted filename."""
        return original_path + ENCRYPTED_EXTENSION

    @staticmethod
    def get_decrypted_filename(encrypted_path):
        """Get original filename by removing .locked extension."""
        if encrypted_path.endswith(ENCRYPTED_EXTENSION):
            return encrypted_path[:-len(ENCRYPTED_EXTENSION)]
        return encrypted_path

    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def validate_path(path):
        """Validate that a path is safe to use."""
        path = os.path.abspath(path)
        # Basic validation - could be expanded based on requirements
        return os.path.exists(os.path.dirname(path)) or os.path.exists(path)

    @staticmethod
    def ensure_directory(directory):
        """Ensure directory exists, create if it doesn't."""
        os.makedirs(directory, exist_ok=True)


class BatchProcessor:
    """Handles batch file operations."""

    def __init__(self, progress_callback=None):
        """
        Initialize batch processor.

        Args:
            progress_callback: Function to call with progress updates (current, total, message)
        """
        self.progress_callback = progress_callback

    def _update_progress(self, current, total, message):
        """Update progress if callback is set."""
        if self.progress_callback:
            self.progress_callback(current, total, message)

    def batch_encrypt(self, file_list, mode, password=None, key=None, delete_originals=False):
        """
        Encrypt multiple files.

        Returns:
            Dictionary with success/failure lists
        """
        results = {
            'success': [],
            'failed': []
        }

        total = len(file_list)

        for i, filepath in enumerate(file_list):
            self._update_progress(i, total, f"Encrypting {os.path.basename(filepath)}...")

            try:
                # Check if it's a folder
                is_folder = os.path.isdir(filepath)
                is_compressed = False
                input_file = filepath

                if is_folder:
                    # Compress folder first
                    temp_zip = FileManager.create_temp_file(suffix='.zip')
                    FileManager.compress_folder(filepath, temp_zip)
                    input_file = temp_zip
                    is_compressed = True

                # Encrypt
                output_path = FileManager.get_encrypted_filename(filepath)

                from crypto_handler import CryptoHandler
                CryptoHandler.encrypt_file(
                    input_file,
                    output_path,
                    mode,
                    password=password,
                    key=key,
                    is_compressed=is_compressed
                )

                # Clean up temp file if folder
                if is_folder:
                    FileManager.safe_delete(temp_zip)

                # Delete original if requested
                if delete_originals:
                    if is_folder:
                        shutil.rmtree(filepath)
                    else:
                        FileManager.safe_delete(filepath)

                results['success'].append(filepath)

            except Exception as e:
                results['failed'].append((filepath, str(e)))

        self._update_progress(total, total, "Encryption complete!")
        return results

    def batch_decrypt(self, file_list, password=None, key=None, delete_encrypted=False):
        """
        Decrypt multiple files.

        Returns:
            Dictionary with success/failure lists
        """
        results = {
            'success': [],
            'failed': []
        }

        total = len(file_list)

        for i, filepath in enumerate(file_list):
            self._update_progress(i, total, f"Decrypting {os.path.basename(filepath)}...")

            try:
                # Decrypt
                output_dir = os.path.dirname(filepath)

                from crypto_handler import CryptoHandler
                decrypt_result = CryptoHandler.decrypt_file(
                    filepath,
                    output_dir,
                    password=password,
                    key=key
                )

                # If it was a compressed folder, extract it
                if decrypt_result['is_compressed']:
                    decrypted_zip = decrypt_result['output_path']
                    # Extract to folder with original name (without .zip)
                    folder_name = os.path.splitext(decrypt_result['original_filename'])[0]
                    extract_dir = os.path.join(output_dir, folder_name)

                    # Handle duplicate folder names
                    if os.path.exists(extract_dir):
                        counter = 1
                        while os.path.exists(extract_dir):
                            extract_dir = os.path.join(output_dir, f"{folder_name}_{counter}")
                            counter += 1

                    FileManager.extract_folder(decrypted_zip, extract_dir)
                    FileManager.safe_delete(decrypted_zip)

                # Delete encrypted file if requested
                if delete_encrypted:
                    FileManager.safe_delete(filepath)

                results['success'].append(filepath)

            except Exception as e:
                results['failed'].append((filepath, str(e)))

        self._update_progress(total, total, "Decryption complete!")
        return results
