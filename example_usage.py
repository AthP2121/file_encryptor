"""
Example usage of the file encryption library without GUI.
"""

import os
from crypto_handler import CryptoHandler
from file_manager import FileManager, BatchProcessor
from config import MODE_PASSWORD, MODE_KEYFILE


def example_password_encryption():
    """Example: Encrypt a file with a password."""
    print("=" * 60)
    print("Example 1: Password-based Encryption")
    print("=" * 60)

    # Create a test file
    test_file = 'example_test.txt'
    with open(test_file, 'w') as f:
        f.write("This is a secret message!")

    print(f"Created test file: {test_file}")

    # Encrypt the file
    encrypted_file = test_file + '.locked'
    CryptoHandler.encrypt_file(
        test_file,
        encrypted_file,
        MODE_PASSWORD,
        password='MySecurePassword123'
    )

    print(f"Encrypted to: {encrypted_file}")

    # Decrypt the file
    result = CryptoHandler.decrypt_file(
        encrypted_file,
        '.',
        password='MySecurePassword123'
    )

    print(f"Decrypted to: {result['output_path']}")
    print()


def example_keyfile_encryption():
    """Example: Encrypt a file with a key file."""
    print("=" * 60)
    print("Example 2: Key File Encryption")
    print("=" * 60)

    # Generate a key file
    key_file = 'my_encryption.key'
    key = CryptoHandler.generate_key_file(key_file)
    print(f"Generated key file: {key_file}")
    print("IMPORTANT: Keep this key file safe!")

    # Create a test file
    test_file = 'example_test2.txt'
    with open(test_file, 'w') as f:
        f.write("Another secret message!")

    print(f"Created test file: {test_file}")

    # Encrypt the file
    encrypted_file = test_file + '.locked'
    CryptoHandler.encrypt_file(
        test_file,
        encrypted_file,
        MODE_KEYFILE,
        key=key
    )

    print(f"Encrypted to: {encrypted_file}")

    # Later, load the key and decrypt
    loaded_key = CryptoHandler.load_key_file(key_file)
    result = CryptoHandler.decrypt_file(
        encrypted_file,
        '.',
        key=loaded_key
    )

    print(f"Decrypted to: {result['output_path']}")
    print()


def example_folder_encryption():
    """Example: Encrypt a folder."""
    print("=" * 60)
    print("Example 3: Folder Encryption")
    print("=" * 60)

    # Create a test folder with files
    test_folder = 'example_folder'
    os.makedirs(test_folder, exist_ok=True)

    for i in range(3):
        with open(os.path.join(test_folder, f'file{i}.txt'), 'w') as f:
            f.write(f"Content of file {i}")

    print(f"Created test folder: {test_folder}")

    # Compress the folder
    zip_file = test_folder + '.zip'
    FileManager.compress_folder(test_folder, zip_file)
    print(f"Compressed to: {zip_file}")

    # Encrypt the zip
    encrypted_file = test_folder + '.locked'
    CryptoHandler.encrypt_file(
        zip_file,
        encrypted_file,
        MODE_PASSWORD,
        password='FolderPassword123',
        is_compressed=True
    )

    print(f"Encrypted to: {encrypted_file}")

    # Decrypt
    result = CryptoHandler.decrypt_file(
        encrypted_file,
        '.',
        password='FolderPassword123'
    )

    print(f"Decrypted to: {result['output_path']}")

    # Extract if it was compressed
    if result['is_compressed']:
        extract_dir = test_folder + '_decrypted'
        FileManager.extract_folder(result['output_path'], extract_dir)
        print(f"Extracted to: {extract_dir}")

    # Clean up zip files
    if os.path.exists(zip_file):
        os.remove(zip_file)
    if os.path.exists(result['output_path']):
        os.remove(result['output_path'])

    print()


def example_batch_encryption():
    """Example: Batch encrypt multiple files."""
    print("=" * 60)
    print("Example 4: Batch Encryption")
    print("=" * 60)

    # Create multiple test files
    test_files = []
    for i in range(5):
        filename = f'batch_test_{i}.txt'
        with open(filename, 'w') as f:
            f.write(f"Batch file {i} content")
        test_files.append(filename)

    print(f"Created {len(test_files)} test files")

    # Create batch processor with progress callback
    def progress_callback(current, total, message):
        print(f"Progress: {current}/{total} - {message}")

    processor = BatchProcessor(progress_callback=progress_callback)

    # Encrypt all files
    results = processor.batch_encrypt(
        test_files,
        MODE_PASSWORD,
        password='BatchPassword123',
        delete_originals=False
    )

    print(f"Encrypted: {len(results['success'])} files")
    if results['failed']:
        print(f"Failed: {len(results['failed'])} files")

    # Decrypt all files
    encrypted_files = [f + '.locked' for f in test_files]
    results = processor.batch_decrypt(
        encrypted_files,
        password='BatchPassword123',
        delete_encrypted=True
    )

    print(f"Decrypted: {len(results['success'])} files")
    if results['failed']:
        print(f"Failed: {len(results['failed'])} files")

    print()


def example_file_search():
    """Example: Search for files."""
    print("=" * 60)
    print("Example 5: File Search")
    print("=" * 60)

    # Search for .locked files in current directory
    results = FileManager.search_files(
        '.',
        pattern='*.locked',
        recursive=False,
        only_locked=True
    )

    print(f"Found {len(results)} encrypted files:")
    for filepath in results:
        print(f"  - {filepath}")

    print()


def cleanup_examples():
    """Clean up example files."""
    print("=" * 60)
    print("Cleaning up example files...")
    print("=" * 60)

    import glob
    import shutil

    patterns = [
        'example_test*.txt',
        'example_test*.locked',
        'my_encryption.key',
        'example_folder',
        'example_folder.locked',
        'example_folder_decrypted',
        'batch_test_*.txt',
        'batch_test_*.locked'
    ]

    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"Removed file: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Removed directory: {path}")
            except Exception as e:
                print(f"Could not remove {path}: {e}")

    print("Cleanup complete!")
    print()


if __name__ == '__main__':
    print("\n")
    print("="*60)
    print("File Encryptor - Usage Examples")
    print("="*60)
    print()

    try:
        example_password_encryption()
        example_keyfile_encryption()
        example_folder_encryption()
        example_batch_encryption()
        example_file_search()

    finally:
        # Clean up
        cleanup_examples()

    print("="*60)
    print("All examples completed!")
    print("="*60)
    print("\nTo use the GUI application, run: python main.py")
    print()
