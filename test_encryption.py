"""
Test script for encryption/decryption functionality.
"""

import os
import tempfile
import shutil
from crypto_handler import CryptoHandler
from file_manager import FileManager
from config import MODE_PASSWORD, MODE_KEYFILE


def test_password_encryption():
    """Test password-based encryption."""
    print("Testing password encryption...")

    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("This is a test file for encryption!")
        temp_file = f.name

    try:
        # Encrypt
        encrypted_file = temp_file + '.locked'
        CryptoHandler.encrypt_file(
            temp_file,
            encrypted_file,
            MODE_PASSWORD,
            password='testpassword123'
        )

        print(f"✓ File encrypted: {encrypted_file}")
        assert os.path.exists(encrypted_file), "Encrypted file not created"

        # Decrypt
        decrypt_dir = tempfile.mkdtemp()
        result = CryptoHandler.decrypt_file(
            encrypted_file,
            decrypt_dir,
            password='testpassword123'
        )

        print(f"✓ File decrypted: {result['output_path']}")

        # Verify content
        with open(result['output_path'], 'r') as f:
            content = f.read()
            assert content == "This is a test file for encryption!", "Content mismatch"

        print("✓ Content verified")

        # Test wrong password
        try:
            CryptoHandler.decrypt_file(
                encrypted_file,
                decrypt_dir,
                password='wrongpassword'
            )
            print("✗ Wrong password should have failed!")
            return False
        except ValueError:
            print("✓ Wrong password rejected correctly")

        # Clean up
        os.remove(temp_file)
        os.remove(encrypted_file)
        shutil.rmtree(decrypt_dir)

        print("✓ Password encryption test PASSED\n")
        return True

    except Exception as e:
        print(f"✗ Password encryption test FAILED: {e}\n")
        return False


def test_keyfile_encryption():
    """Test key file encryption."""
    print("Testing key file encryption...")

    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("This is a test file for key encryption!")
        temp_file = f.name

    # Generate key file
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.key').name
    key = CryptoHandler.generate_key_file(key_file)

    try:
        # Encrypt
        encrypted_file = temp_file + '.locked'
        CryptoHandler.encrypt_file(
            temp_file,
            encrypted_file,
            MODE_KEYFILE,
            key=key
        )

        print(f"✓ File encrypted: {encrypted_file}")
        assert os.path.exists(encrypted_file), "Encrypted file not created"

        # Decrypt
        decrypt_dir = tempfile.mkdtemp()
        result = CryptoHandler.decrypt_file(
            encrypted_file,
            decrypt_dir,
            key=key
        )

        print(f"✓ File decrypted: {result['output_path']}")

        # Verify content
        with open(result['output_path'], 'r') as f:
            content = f.read()
            assert content == "This is a test file for key encryption!", "Content mismatch"

        print("✓ Content verified")

        # Clean up
        os.remove(temp_file)
        os.remove(encrypted_file)
        os.remove(key_file)
        shutil.rmtree(decrypt_dir)

        print("✓ Key file encryption test PASSED\n")
        return True

    except Exception as e:
        print(f"✗ Key file encryption test FAILED: {e}\n")
        return False


def test_folder_encryption():
    """Test folder compression and encryption."""
    print("Testing folder encryption...")

    # Create temp folder with files
    temp_dir = tempfile.mkdtemp()
    try:
        # Create some test files
        for i in range(3):
            with open(os.path.join(temp_dir, f'file{i}.txt'), 'w') as f:
                f.write(f"Content of file {i}")

        # Create subfolder
        subdir = os.path.join(temp_dir, 'subfolder')
        os.makedirs(subdir)
        with open(os.path.join(subdir, 'subfile.txt'), 'w') as f:
            f.write("Content in subfolder")

        # Compress folder
        zip_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip').name
        FileManager.compress_folder(temp_dir, zip_file)
        print(f"✓ Folder compressed: {zip_file}")

        # Encrypt the zip
        encrypted_file = zip_file + '.locked'
        CryptoHandler.encrypt_file(
            zip_file,
            encrypted_file,
            MODE_PASSWORD,
            password='foldertest123',
            is_compressed=True
        )
        print(f"✓ Compressed folder encrypted: {encrypted_file}")

        # Decrypt
        decrypt_dir = tempfile.mkdtemp()
        result = CryptoHandler.decrypt_file(
            encrypted_file,
            decrypt_dir,
            password='foldertest123'
        )
        print(f"✓ File decrypted: {result['output_path']}")

        # Extract if compressed
        if result['is_compressed']:
            extract_dir = os.path.join(decrypt_dir, 'extracted')
            FileManager.extract_folder(result['output_path'], extract_dir)
            print(f"✓ Folder extracted: {extract_dir}")

            # Verify files
            assert os.path.exists(os.path.join(extract_dir, os.path.basename(temp_dir), 'file0.txt'))
            print("✓ Files verified")

        # Clean up
        shutil.rmtree(temp_dir)
        os.remove(zip_file)
        os.remove(encrypted_file)
        shutil.rmtree(decrypt_dir)

        print("✓ Folder encryption test PASSED\n")
        return True

    except Exception as e:
        print(f"✗ Folder encryption test FAILED: {e}\n")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return False


def test_file_search():
    """Test file search functionality."""
    print("Testing file search...")

    # Create temp directory structure
    temp_dir = tempfile.mkdtemp()
    try:
        # Create test files
        with open(os.path.join(temp_dir, 'test1.txt'), 'w') as f:
            f.write("test")
        with open(os.path.join(temp_dir, 'test2.doc'), 'w') as f:
            f.write("test")
        with open(os.path.join(temp_dir, 'file.locked'), 'w') as f:
            f.write("test")

        # Create subdirectory
        subdir = os.path.join(temp_dir, 'subdir')
        os.makedirs(subdir)
        with open(os.path.join(subdir, 'test3.txt'), 'w') as f:
            f.write("test")

        # Test search all files
        results = FileManager.search_files(temp_dir, pattern='*', recursive=True)
        assert len(results) == 4, f"Expected 4 files, found {len(results)}"
        print(f"✓ Found all files: {len(results)}")

        # Test search .txt files
        results = FileManager.search_files(temp_dir, pattern='*.txt', recursive=True)
        assert len(results) == 2, f"Expected 2 txt files, found {len(results)}"
        print(f"✓ Found txt files: {len(results)}")

        # Test search only locked files
        results = FileManager.search_files(temp_dir, pattern='*', recursive=True, only_locked=True)
        assert len(results) == 1, f"Expected 1 locked file, found {len(results)}"
        print(f"✓ Found locked files: {len(results)}")

        # Test non-recursive search
        results = FileManager.search_files(temp_dir, pattern='*', recursive=False)
        assert len(results) == 3, f"Expected 3 files in root, found {len(results)}"
        print(f"✓ Non-recursive search: {len(results)}")

        # Clean up
        shutil.rmtree(temp_dir)

        print("✓ File search test PASSED\n")
        return True

    except Exception as e:
        print(f"✗ File search test FAILED: {e}\n")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("File Encryptor Test Suite")
    print("="*60 + "\n")

    tests = [
        test_password_encryption,
        test_keyfile_encryption,
        test_folder_encryption,
        test_file_search
    ]

    results = []
    for test in tests:
        results.append(test())

    print("="*60)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    print("="*60)

    return all(results)


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
