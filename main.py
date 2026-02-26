"""
Main GUI application for file encryption.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from config import *
from ui_components import FileListFrame, PasswordEntryFrame, ProgressFrame, SearchFrame

# Lazy-loaded modules (imported on-demand in methods to speed up startup)
_crypto_handler = None
_file_manager = None
_batch_processor = None


def _load_crypto():
    """Lazy load CryptoHandler on first use."""
    global _crypto_handler
    if _crypto_handler is None:
        from crypto_handler import CryptoHandler
        _crypto_handler = CryptoHandler
    return _crypto_handler


def _load_file_manager():
    """Lazy load FileManager and BatchProcessor on first use."""
    global _file_manager, _batch_processor
    if _file_manager is None:
        from file_manager import FileManager, BatchProcessor
        _file_manager = FileManager
        _batch_processor = BatchProcessor
    return _file_manager, _batch_processor


class FileEncryptorApp:
    """Main application class."""

    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Variables
        self.mode_var = tk.IntVar(value=MODE_PASSWORD)
        self.key_file_path = None
        self.delete_originals_var = tk.BooleanVar(value=False)

        self.setup_ui()
        
        # Pre-load heavy modules after UI appears but before user interacts
        # Schedule after 100ms to ensure UI is fully rendered
        self.root.after(100, self._preload_modules)

    def _preload_modules(self):
        """Pre-load heavy modules in background after UI is ready."""
        try:
            # Load modules to cache them; this happens silently in background
            _load_crypto()
            _load_file_manager()
        except Exception:
            # Silent fail - modules will load on-demand if preload fails
            pass

    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding=PADDING)
        main_frame.pack(fill='both', expand=True)

        # Top section - File selection and search
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='x', pady=(0, 10))

        # File browser
        browser_frame = ttk.LabelFrame(top_frame, text='File/Folder Selection')
        browser_frame.pack(fill='x', pady=(0, 5))

        button_frame = ttk.Frame(browser_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(button_frame, text='Add Files', command=self.add_files).pack(side='left', padx=2)
        ttk.Button(button_frame, text='Add Folder', command=self.add_folder).pack(side='left', padx=2)
        ttk.Button(button_frame, text='Clear All', command=self.clear_files).pack(side='left', padx=2)

        # Search frame
        self.search_frame = SearchFrame(top_frame, search_callback=self.do_search)
        self.search_frame.pack(fill='x')

        # Middle section - File list
        list_frame = ttk.LabelFrame(main_frame, text='Selected Files')
        list_frame.pack(fill='both', expand=True, pady=(0, 10))

        self.file_list = FileListFrame(list_frame)
        self.file_list.pack(fill='both', expand=True, padx=5, pady=5)

        # Bottom section - Mode selection and actions
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill='x')

        # Mode selection
        mode_frame = ttk.LabelFrame(bottom_frame, text='Encryption Mode')
        mode_frame.pack(fill='x', pady=(0, 10))

        mode_inner = ttk.Frame(mode_frame)
        mode_inner.pack(fill='x', padx=5, pady=5)

        ttk.Radiobutton(
            mode_inner,
            text='Password',
            variable=self.mode_var,
            value=MODE_PASSWORD,
            command=self.on_mode_change
        ).pack(side='left', padx=5)

        ttk.Radiobutton(
            mode_inner,
            text='Key File',
            variable=self.mode_var,
            value=MODE_KEYFILE,
            command=self.on_mode_change
        ).pack(side='left', padx=5)

        # Password mode controls
        self.password_frame = ttk.Frame(mode_frame)
        self.password_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(self.password_frame, text='Password:').pack(side='left')
        self.password_entry = PasswordEntryFrame(self.password_frame)
        self.password_entry.pack(side='left', padx=5)

        # Key file mode controls
        self.keyfile_frame = ttk.Frame(mode_frame)

        ttk.Label(self.keyfile_frame, text='Key File:').pack(side='left')

        self.keyfile_var = tk.StringVar(value='No key file selected')
        ttk.Label(self.keyfile_frame, textvariable=self.keyfile_var, foreground='gray').pack(side='left', padx=5)

        ttk.Button(self.keyfile_frame, text='Load Key', command=self.load_key_file).pack(side='left', padx=2)
        ttk.Button(self.keyfile_frame, text='Generate Key', command=self.generate_key_file).pack(side='left', padx=2)

        # Show password mode by default
        self.on_mode_change()

        # Options
        options_frame = ttk.Frame(bottom_frame)
        options_frame.pack(fill='x', pady=(0, 10))

        ttk.Checkbutton(
            options_frame,
            text='Delete original files after encryption',
            variable=self.delete_originals_var
        ).pack(side='left')

        # Action buttons
        action_frame = ttk.Frame(bottom_frame)
        action_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(
            action_frame,
            text='Encrypt Selected',
            command=self.encrypt_files,
            width=20
        ).pack(side='left', padx=5)

        ttk.Button(
            action_frame,
            text='Decrypt Selected',
            command=self.decrypt_files,
            width=20
        ).pack(side='left', padx=5)

        # Progress bar
        self.progress_frame = ProgressFrame(bottom_frame)
        self.progress_frame.pack(fill='x')

    def on_mode_change(self):
        """Handle mode selection change."""
        if self.mode_var.get() == MODE_PASSWORD:
            self.password_frame.pack(fill='x', padx=5, pady=5)
            self.keyfile_frame.pack_forget()
        else:
            self.password_frame.pack_forget()
            self.keyfile_frame.pack(fill='x', padx=5, pady=5)

    def add_files(self):
        """Add files to the list."""
        files = filedialog.askopenfilenames(title='Select Files')
        if files:
            self.file_list.add_files(files)

    def add_folder(self):
        """Add a folder to the list."""
        folder = filedialog.askdirectory(title='Select Folder')
        if folder:
            self.file_list.add_file(folder)

    def clear_files(self):
        """Clear all files from the list."""
        self.file_list.clear()

    def do_search(self, directory, pattern, recursive, only_locked):
        """Execute file search."""
        try:
            FileManager, _ = _load_file_manager()
            results = FileManager.search_files(
                directory,
                pattern=pattern,
                recursive=recursive,
                only_locked=only_locked
            )

            if results:
                self.file_list.clear()
                self.file_list.add_files(results)
                messagebox.showinfo('Search Complete', f'Found {len(results)} file(s)')
            else:
                messagebox.showinfo('Search Complete', 'No files found')

        except Exception as e:
            messagebox.showerror('Search Error', f'Error searching files: {str(e)}')

    def load_key_file(self):
        """Load an encryption key file."""
        filepath = filedialog.askopenfilename(
            title='Select Key File',
            filetypes=[('Key files', '*.key'), ('All files', '*.*')]
        )

        if filepath:
            try:
                CryptoHandler = _load_crypto()
                CryptoHandler.load_key_file(filepath)
                self.key_file_path = filepath
                self.keyfile_var.set(os.path.basename(filepath))
                messagebox.showinfo('Success', 'Key file loaded successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to load key file: {str(e)}')

    def generate_key_file(self):
        """Generate a new encryption key file."""
        filepath = filedialog.asksaveasfilename(
            title='Save Key File',
            defaultextension='.key',
            filetypes=[('Key files', '*.key'), ('All files', '*.*')]
        )

        if filepath:
            try:
                CryptoHandler = _load_crypto()
                CryptoHandler.generate_key_file(filepath)
                self.key_file_path = filepath
                self.keyfile_var.set(os.path.basename(filepath))
                messagebox.showinfo(
                    'Success',
                    'Key file generated successfully!\n\nIMPORTANT: Keep this key file safe. '
                    'You will need it to decrypt your files.'
                )
            except Exception as e:
                messagebox.showerror('Error', f'Failed to generate key file: {str(e)}')

    def validate_encryption_params(self):
        """Validate encryption parameters."""
        mode = self.mode_var.get()

        if mode == MODE_PASSWORD:
            password = self.password_entry.get()
            if not password:
                messagebox.showwarning('Warning', 'Please enter a password')
                return None

            if len(password) < MIN_PASSWORD_LENGTH:
                messagebox.showwarning(
                    'Weak Password',
                    f'Password should be at least {MIN_PASSWORD_LENGTH} characters long'
                )
                return None

            return {'mode': mode, 'password': password, 'key': None}

        else:  # MODE_KEYFILE
            if not self.key_file_path:
                messagebox.showwarning('Warning', 'Please load or generate a key file')
                return None

            try:
                CryptoHandler = _load_crypto()
                key = CryptoHandler.load_key_file(self.key_file_path)
                return {'mode': mode, 'password': None, 'key': key}
            except Exception as e:
                messagebox.showerror('Error', f'Invalid key file: {str(e)}')
                return None

    def encrypt_files(self):
        """Encrypt selected files."""
        selected = self.file_list.get_selected_files()

        if not selected:
            messagebox.showwarning('Warning', 'Please select files to encrypt')
            return

        params = self.validate_encryption_params()
        if not params:
            return

        # Confirm action
        count = len(selected)
        delete_msg = '\n\nOriginal files will be deleted.' if self.delete_originals_var.get() else ''
        if not messagebox.askyesno(
            'Confirm Encryption',
            f'Encrypt {count} file(s)/folder(s)?{delete_msg}'
        ):
            return

        # Run encryption in thread
        def encrypt_thread():
            try:
                _, BatchProcessor = _load_file_manager()
                processor = BatchProcessor(progress_callback=self.update_progress)
                results = processor.batch_encrypt(
                    selected,
                    params['mode'],
                    password=params['password'],
                    key=params['key'],
                    delete_originals=self.delete_originals_var.get()
                )

                self.root.after(0, lambda: self.show_results('Encryption', results))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror('Error', f'Encryption failed: {str(e)}'))

            finally:
                self.root.after(0, self.progress_frame.reset)

        threading.Thread(target=encrypt_thread, daemon=True).start()

    def decrypt_files(self):
        """Decrypt selected files."""
        selected = self.file_list.get_selected_files()

        if not selected:
            messagebox.showwarning('Warning', 'Please select files to decrypt')
            return

        # Check if any non-.locked files are selected
        non_locked = [f for f in selected if not f.endswith(ENCRYPTED_EXTENSION)]
        if non_locked:
            messagebox.showwarning(
                'Warning',
                'Some selected files are not encrypted (.locked) files'
            )
            return

        params = self.validate_encryption_params()
        if not params:
            return

        # Ask about deleting encrypted files
        delete_encrypted = messagebox.askyesno(
            'Delete Encrypted Files?',
            'Delete encrypted files after successful decryption?'
        )

        # Run decryption in thread
        def decrypt_thread():
            try:
                _, BatchProcessor = _load_file_manager()
                processor = BatchProcessor(progress_callback=self.update_progress)
                results = processor.batch_decrypt(
                    selected,
                    password=params['password'],
                    key=params['key'],
                    delete_encrypted=delete_encrypted
                )

                self.root.after(0, lambda: self.show_results('Decryption', results))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror('Error', f'Decryption failed: {str(e)}'))

            finally:
                self.root.after(0, self.progress_frame.reset)

        threading.Thread(target=decrypt_thread, daemon=True).start()

    def update_progress(self, current, total, message):
        """Update progress bar from worker thread."""
        self.root.after(0, lambda: self.progress_frame.update_progress(current, total, message))

    def show_results(self, operation, results):
        """Show operation results."""
        success_count = len(results['success'])
        failed_count = len(results['failed'])

        if failed_count == 0:
            messagebox.showinfo(
                f'{operation} Complete',
                f'Successfully processed {success_count} file(s)'
            )
            # Refresh file list to show new .locked files or decrypted files
            self.file_list.clear()
        else:
            error_details = '\n'.join([f'{f}: {e}' for f, e in results['failed'][:5]])
            if len(results['failed']) > 5:
                error_details += f'\n... and {len(results["failed"]) - 5} more'

            messagebox.showwarning(
                f'{operation} Partial Success',
                f'Successful: {success_count}\nFailed: {failed_count}\n\nErrors:\n{error_details}'
            )


def main():
    """Main entry point."""
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
