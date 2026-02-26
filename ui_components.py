"""
Reusable UI components for the application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from config import *


class FileListFrame(ttk.Frame):
    """Frame displaying a list of files with checkboxes."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.files = []
        self.checkboxes = {}

        # Create scrollable frame
        self.canvas = tk.Canvas(self, bg='white')
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack elements
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Header
        self.header_frame = ttk.Frame(self.scrollable_frame)
        self.header_frame.pack(fill='x', padx=5, pady=5)

        self.select_all_var = tk.BooleanVar(value=True)
        self.select_all_cb = ttk.Checkbutton(
            self.header_frame,
            text='Select All',
            variable=self.select_all_var,
            command=self.toggle_all
        )
        self.select_all_cb.pack(side='left')

        # File count label
        self.count_label = ttk.Label(self.header_frame, text='0 files')
        self.count_label.pack(side='right')

    def add_file(self, filepath):
        """Add a file to the list."""
        if filepath not in self.files:
            self.files.append(filepath)
            self._create_checkbox(filepath)
            self._update_count()

    def add_files(self, filepaths):
        """Add multiple files to the list."""
        for filepath in filepaths:
            self.add_file(filepath)

    def clear(self):
        """Clear all files from the list."""
        self.files = []
        self.checkboxes = {}
        for widget in self.scrollable_frame.winfo_children():
            if widget != self.header_frame:
                widget.destroy()
        self._update_count()

    def _create_checkbox(self, filepath):
        """Create checkbox for a file."""
        var = tk.BooleanVar(value=True)
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill='x', padx=5, pady=2)

        cb = ttk.Checkbutton(frame, variable=var)
        cb.pack(side='left')

        # File name label
        filename = os.path.basename(filepath)
        label = ttk.Label(frame, text=filename, cursor='hand2')
        label.pack(side='left', padx=5)

        # Path label (smaller, gray)
        path_label = ttk.Label(frame, text=filepath, foreground='gray', font=('TkDefaultFont', 8))
        path_label.pack(side='left', padx=5)

        self.checkboxes[filepath] = var

    def toggle_all(self):
        """Toggle all checkboxes."""
        state = self.select_all_var.get()
        for var in self.checkboxes.values():
            var.set(state)

    def get_selected_files(self):
        """Get list of selected files."""
        return [filepath for filepath, var in self.checkboxes.items() if var.get()]

    def _update_count(self):
        """Update file count label."""
        count = len(self.files)
        self.count_label.config(text=f"{count} file{'s' if count != 1 else ''}")


class PasswordEntryFrame(ttk.Frame):
    """Frame for password entry with visibility toggle."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.password_var = tk.StringVar()

        # Password entry
        self.entry = ttk.Entry(self, textvariable=self.password_var, show='*', width=30)
        self.entry.pack(side='left', padx=(0, 5))

        # Show/hide button
        self.show_var = tk.BooleanVar(value=False)
        self.show_button = ttk.Checkbutton(
            self,
            text='Show',
            variable=self.show_var,
            command=self.toggle_visibility
        )
        self.show_button.pack(side='left')

    def toggle_visibility(self):
        """Toggle password visibility."""
        if self.show_var.get():
            self.entry.config(show='')
        else:
            self.entry.config(show='*')

    def get(self):
        """Get password value."""
        return self.password_var.get()

    def set(self, value):
        """Set password value."""
        self.password_var.set(value)

    def clear(self):
        """Clear password."""
        self.password_var.set('')


class ProgressFrame(ttk.Frame):
    """Frame with progress bar and status label."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Status label
        self.status_var = tk.StringVar(value='Ready')
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(fill='x', pady=(0, 5))

        # Progress bar
        self.progress = ttk.Progressbar(self, mode='determinate')
        self.progress.pack(fill='x')

    def update_progress(self, current, total, message=''):
        """Update progress bar and status."""
        if total > 0:
            percentage = (current / total) * 100
            self.progress['value'] = percentage

        if message:
            self.status_var.set(message)

        self.update_idletasks()

    def reset(self):
        """Reset progress to 0."""
        self.progress['value'] = 0
        self.status_var.set('Ready')

    def set_message(self, message):
        """Set status message."""
        self.status_var.set(message)


class SearchFrame(ttk.LabelFrame):
    """Frame for file search functionality."""

    def __init__(self, parent, search_callback=None, **kwargs):
        super().__init__(parent, text='Search Files', **kwargs)
        self.search_callback = search_callback

        # Directory selection
        dir_frame = ttk.Frame(self)
        dir_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(dir_frame, text='Directory:').pack(side='left')

        self.dir_var = tk.StringVar(value=DEFAULT_SEARCH_DIR)
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var)
        self.dir_entry.pack(side='left', fill='x', expand=True, padx=5)

        ttk.Button(dir_frame, text='Browse', command=self.browse_directory).pack(side='left')

        # Search options
        options_frame = ttk.Frame(self)
        options_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(options_frame, text='Pattern:').pack(side='left')

        self.pattern_var = tk.StringVar(value='*')
        self.pattern_entry = ttk.Entry(options_frame, textvariable=self.pattern_var, width=15)
        self.pattern_entry.pack(side='left', padx=5)

        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text='Recursive', variable=self.recursive_var).pack(side='left', padx=5)

        self.locked_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text='Only .locked files', variable=self.locked_only_var).pack(side='left', padx=5)

        # Search button
        ttk.Button(self, text='Search', command=self.do_search).pack(pady=5)

    def browse_directory(self):
        """Open directory browser."""
        directory = filedialog.askdirectory(initialdir=self.dir_var.get())
        if directory:
            self.dir_var.set(directory)

    def do_search(self):
        """Execute search."""
        if self.search_callback:
            self.search_callback(
                self.dir_var.get(),
                self.pattern_var.get(),
                self.recursive_var.get(),
                self.locked_only_var.get()
            )

    def get_search_params(self):
        """Get current search parameters."""
        return {
            'directory': self.dir_var.get(),
            'pattern': self.pattern_var.get(),
            'recursive': self.recursive_var.get(),
            'only_locked': self.locked_only_var.get()
        }
