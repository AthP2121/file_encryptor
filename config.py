"""
Configuration and constants for the file encryption application.
"""

import os

# Application metadata
APP_NAME = "File Encryptor"
APP_VERSION = "1.0.0"

# File format constants
MAGIC_BYTES = b"FLCK"
FILE_VERSION = 1
ENCRYPTED_EXTENSION = ".locked"

# Encryption modes
MODE_PASSWORD = 0
MODE_KEYFILE = 1

# Crypto constants
SALT_SIZE = 32
KEY_SIZE = 32
PBKDF2_ITERATIONS = 480000  # OWASP recommendation for 2023+
MIN_PASSWORD_LENGTH = 8

# File header structure
HEADER_MAGIC_SIZE = 4
HEADER_VERSION_SIZE = 1
HEADER_MODE_SIZE = 1
HEADER_SALT_SIZE = 32
HEADER_COMPRESSED_SIZE = 1
HEADER_FILENAME_LENGTH_SIZE = 2

# UI constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
PADDING = 10

# Default settings
DEFAULT_SEARCH_DIR = os.path.expanduser("~")
TEMP_FILE_PREFIX = "flck_temp_"

# Messages
MSG_ENCRYPT_SUCCESS = "File(s) encrypted successfully!"
MSG_DECRYPT_SUCCESS = "File(s) decrypted successfully!"
MSG_WRONG_PASSWORD = "Incorrect password or corrupted file."
MSG_INVALID_KEY = "Invalid key file."
MSG_FILE_NOT_FOUND = "File not found."
MSG_CORRUPTED_FILE = "File appears to be corrupted."
