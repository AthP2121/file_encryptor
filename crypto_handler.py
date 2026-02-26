"""
Encryption and decryption logic using AES-256.
"""

import os
import struct
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
import base64
from config import *


class CryptoHandler:
    """Handles encryption and decryption operations."""

    @staticmethod
    def generate_key_file(filepath):
        """Generate a new encryption key and save to file."""
        key = Fernet.generate_key()
        with open(filepath, 'wb') as f:
            f.write(key)
        return key

    @staticmethod
    def load_key_file(filepath):
        """Load encryption key from file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Key file not found: {filepath}")

        with open(filepath, 'rb') as f:
            key = f.read()

        # Validate key format
        try:
            Fernet(key)
            return key
        except Exception:
            raise ValueError("Invalid key file format")

    @staticmethod
    def derive_key_from_password(password, salt=None):
        """Derive encryption key from password using PBKDF2."""
        if salt is None:
            salt = os.urandom(SALT_SIZE)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @staticmethod
    def create_file_header(mode, salt, is_compressed, original_filename):
        """Create file header with metadata."""
        header = bytearray()

        # Magic bytes
        header.extend(MAGIC_BYTES)

        # Version
        header.append(FILE_VERSION)

        # Mode
        header.append(mode)

        # Salt (only for password mode)
        if mode == MODE_PASSWORD:
            header.extend(salt)
        else:
            header.extend(b'\x00' * HEADER_SALT_SIZE)

        # Compressed flag
        header.append(1 if is_compressed else 0)

        # Original filename
        filename_bytes = original_filename.encode('utf-8')
        filename_length = len(filename_bytes)
        header.extend(struct.pack('>H', filename_length))
        header.extend(filename_bytes)

        return bytes(header)

    @staticmethod
    def parse_file_header(filepath):
        """Parse header from encrypted file."""
        with open(filepath, 'rb') as f:
            # Read magic bytes
            magic = f.read(HEADER_MAGIC_SIZE)
            if magic != MAGIC_BYTES:
                raise ValueError("Not a valid encrypted file")

            # Read version
            version = f.read(HEADER_VERSION_SIZE)[0]
            if version != FILE_VERSION:
                raise ValueError(f"Unsupported file version: {version}")

            # Read mode
            mode = f.read(HEADER_MODE_SIZE)[0]

            # Read salt
            salt = f.read(HEADER_SALT_SIZE)
            if mode != MODE_PASSWORD:
                salt = None

            # Read compressed flag
            is_compressed = f.read(HEADER_COMPRESSED_SIZE)[0] == 1

            # Read original filename
            filename_length = struct.unpack('>H', f.read(HEADER_FILENAME_LENGTH_SIZE))[0]
            original_filename = f.read(filename_length).decode('utf-8')

            # Read encrypted data
            encrypted_data = f.read()

        return {
            'mode': mode,
            'salt': salt,
            'is_compressed': is_compressed,
            'original_filename': original_filename,
            'encrypted_data': encrypted_data
        }

    @staticmethod
    def encrypt_data(data, key):
        """Encrypt data using Fernet."""
        f = Fernet(key)
        return f.encrypt(data)

    @staticmethod
    def decrypt_data(encrypted_data, key):
        """Decrypt data using Fernet."""
        try:
            f = Fernet(key)
            return f.decrypt(encrypted_data)
        except InvalidToken:
            raise ValueError("Decryption failed: Invalid key or corrupted data")

    @staticmethod
    def encrypt_file(input_path, output_path, mode, password=None, key=None, is_compressed=False):
        """
        Encrypt a file.

        Args:
            input_path: Path to file to encrypt
            output_path: Path for encrypted output
            mode: MODE_PASSWORD or MODE_KEYFILE
            password: Password (if mode is MODE_PASSWORD)
            key: Encryption key (if mode is MODE_KEYFILE)
            is_compressed: Whether the input is a compressed folder
        """
        # Read input file
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        # Get encryption key
        salt = None
        if mode == MODE_PASSWORD:
            if not password:
                raise ValueError("Password required for password mode")
            key, salt = CryptoHandler.derive_key_from_password(password)
        elif mode == MODE_KEYFILE:
            if not key:
                raise ValueError("Key required for key file mode")
        else:
            raise ValueError("Invalid encryption mode")

        # Encrypt data
        encrypted_data = CryptoHandler.encrypt_data(plaintext, key)

        # Create header
        original_filename = os.path.basename(input_path)
        header = CryptoHandler.create_file_header(mode, salt or b'', is_compressed, original_filename)

        # Write to output file
        with open(output_path, 'wb') as f:
            f.write(header)
            f.write(encrypted_data)

    @staticmethod
    def decrypt_file(input_path, output_dir, password=None, key=None):
        """
        Decrypt a file.

        Args:
            input_path: Path to encrypted file
            output_dir: Directory for decrypted output
            password: Password (if file was encrypted with password)
            key: Encryption key (if file was encrypted with key)

        Returns:
            Dictionary with decryption results including output path and whether it was compressed
        """
        # Parse header
        header_data = CryptoHandler.parse_file_header(input_path)

        # Get decryption key
        if header_data['mode'] == MODE_PASSWORD:
            if not password:
                raise ValueError("Password required to decrypt this file")
            key, _ = CryptoHandler.derive_key_from_password(password, header_data['salt'])
        elif header_data['mode'] == MODE_KEYFILE:
            if not key:
                raise ValueError("Key file required to decrypt this file")

        # Decrypt data
        decrypted_data = CryptoHandler.decrypt_data(header_data['encrypted_data'], key)

        # Write to output file
        output_path = os.path.join(output_dir, header_data['original_filename'])

        # Handle duplicate filenames
        if os.path.exists(output_path):
            base, ext = os.path.splitext(output_path)
            counter = 1
            while os.path.exists(output_path):
                output_path = f"{base}_{counter}{ext}"
                counter += 1

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        return {
            'output_path': output_path,
            'is_compressed': header_data['is_compressed'],
            'original_filename': header_data['original_filename']
        }
