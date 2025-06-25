#!/usr/bin/env python3
"""
File Organizer
A comprehensive tool to automatically organize files by type, date, and custom rules.
"""

import os
import sys
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading
from datetime import datetime
import configparser
from collections import defaultdict


class FileOrganizerConfig:
    """
    Handles configuration management for the file organizer.
    
    Why we need this class:
    - Separates configuration logic from main application logic (separation of concerns)
    - Allows users to customize organization rules without modifying code
    - Provides a consistent way to store and retrieve settings
    - Makes the application more maintainable and user-friendly
    """
    
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_default_config()
        self.load_config()
    
    def load_default_config(self):
        """
        Load default configuration settings.
        
        Why we define default rules:
        - Provides sensible defaults that work for most users out of the box
        - Covers the most common file types people encounter
        - Uses logical categorization that matches how people think about files
        - Enables date-based organization for time-sensitive content (photos, videos)
        """
        self.default_rules = {
            # Images: Organized by date because photos are often searched by "when taken"
            'Images': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico', '.heic'],
                'subfolder_by_date': True,  # Photos benefit from date organization (Year/Month structure)
                'date_format': '%Y/%m'      # YYYY/MM format is intuitive and chronological
            },
            # Documents: Organized by type rather than date (most documents are accessed by content, not age)
            'Documents': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
                'subfolder_by_date': False,  # Documents are usually searched by type/content, not date
                'subfolders': {
                    'PDFs': ['.pdf'],                           # PDFs often contain reports, forms, guides
                    'Word Documents': ['.doc', '.docx', '.odt'], # Editable documents grouped together
                    'Text Files': ['.txt', '.rtf'],             # Plain text files separate for easy access
                    'Other Documents': []                       # Catch-all for other document types
                }
            },
            'Office': {
                'extensions': ['.xls', '.xlsx', '.ppt', '.pptx', '.odp', '.ods', '.csv', '.numbers', '.keynote'],
                'subfolder_by_date': False,
                'subfolders': {
                    'Spreadsheets': ['.xls', '.xlsx', '.ods', '.csv', '.numbers'],
                    'Presentations': ['.ppt', '.pptx', '.odp', '.keynote']
                }
            },
            'Audio': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
                'subfolder_by_date': False
            },
            'Video': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
                'subfolder_by_date': True,
                'date_format': '%Y'
            },
            'Archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
                'subfolder_by_date': False
            },
            'Development': {
                'extensions': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs', '.swift'],
                'subfolder_by_date': False,
                'subfolders': {
                    'Python': ['.py'],
                    'Web': ['.html', '.css', '.js'],
                    'Other Code': []
                }
            },
            'Software': {
                'extensions': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
                'subfolder_by_date': False
            }
        }
    
    def load_config(self):
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file."""
        self.config['DEFAULT'] = {
            'source_folders': str(Path.home() / 'Downloads'),
            'destination_folder': str(Path.home() / 'Organized Files'),
            'auto_organize': 'False',
            'watch_interval': '30',
            'create_undo_log': 'True',
            'handle_duplicates': 'rename',
            'organize_by_date': 'True',
            'dry_run': 'False'
        }
        
        self.config['RULES'] = {}
        for category, rules in self.default_rules.items():
            rule_json = json.dumps(rules)
            # Escape % signs for configparser
            rule_json = rule_json.replace('%', '%%')
            self.config['RULES'][category.lower()] = rule_json
        
        self.save_config()
    
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def get_rules(self):
        """Get organization rules."""
        rules = {}
        for category in self.config['RULES']:
            rule_str = self.config['RULES'][category]
            # Skip entries that don't look like JSON (likely DEFAULT section values)
            if not rule_str.strip().startswith('{'):
                continue
            # Replace escaped %% back to single % for date formatting
            rule_str = rule_str.replace('%%', '%')
            # Use capitalized category name for consistency
            category_name = category.capitalize()
            rules[category_name] = json.loads(rule_str)
        return rules
    
    def get_setting(self, key, fallback=None):
        """Get a configuration setting."""
        return self.config['DEFAULT'].get(key, fallback)
    
    def set_setting(self, key, value):
        """Set a configuration setting."""
        self.config['DEFAULT'][key] = str(value)
        self.save_config()


class FileOrganizer:
    """Main file organizer class."""
    
    def __init__(self):
        self.config = FileOrganizerConfig()
        self.rules = self.config.get_rules()
        self.stats = defaultdict(int)
        self.undo_log = []
        self.running = False
        
    def get_file_category(self, file_path):
        """Determine the category of a file based on its extension."""
        extension = Path(file_path).suffix.lower()
        
        for category, rule in self.rules.items():
            if extension in rule['extensions']:
                return category
        
        return 'Other'
    
    def get_file_date(self, file_path):
        """Get the creation or modification date of a file."""
        try:
            stat = os.stat(file_path)
            timestamp = getattr(stat, 'st_birthtime', stat.st_mtime)
            return datetime.fromtimestamp(timestamp)
        except:
            return datetime.now()
    
    def generate_destination_path(self, file_path, destination_base):
        """Generate the destination path for a file."""
        file_path = Path(file_path)
        category = self.get_file_category(file_path)
        rule = self.rules.get(category, {})
        
        dest_path = Path(destination_base) / category
        
        if 'subfolders' in rule:
            subfolder = self.get_subfolder(file_path, rule['subfolders'])
            if subfolder:
                dest_path = dest_path / subfolder
        
        if rule.get('subfolder_by_date', False):
            file_date = self.get_file_date(file_path)
            date_format = rule.get('date_format', '%Y/%m')
            date_folder = file_date.strftime(date_format)
            dest_path = dest_path / date_folder
        
        return dest_path
    
    def get_subfolder(self, file_path, subfolders):
        """Determine the appropriate subfolder for a file."""
        extension = file_path.suffix.lower()
        
        for subfolder, extensions in subfolders.items():
            if extension in extensions:
                return subfolder
        
        for subfolder, extensions in subfolders.items():
            if not extensions:
                return subfolder
        
        return None
    
    def handle_duplicate(self, source, destination):
        """
        Handle duplicate files based on configuration.
        
        Why we need duplicate handling:
        - Users often have multiple versions of the same file
        - Prevents accidental data loss by offering different strategies
        - 'rename' is safest (keeps both files with clear naming)
        - 'skip' preserves existing files when user doesn't want duplicates
        - 'overwrite' for when user wants latest version only
        """
        handle_method = self.config.get_setting('handle_duplicates', 'rename')
        
        if handle_method == 'skip':
            return None  # Don't move the file, keep original in place
        elif handle_method == 'overwrite':
            return destination  # Replace existing file
        else:  # rename - safest option, keeps both files
            counter = 1
            base_name = destination.stem
            extension = destination.suffix
            parent = destination.parent
            
            # Find a unique name by adding _1, _2, _3, etc.
            while destination.exists():
                new_name = f"{base_name}_{counter}{extension}"
                destination = parent / new_name
                counter += 1
            
            return destination
    
    def organize_file(self, source_path, destination_base, dry_run=False):
        """Organize a single file."""
        source_path = Path(source_path)
        
        if not source_path.exists() or source_path.is_dir():
            return False, f"File does not exist or is a directory: {source_path}"
        
        try:
            dest_dir = self.generate_destination_path(source_path, destination_base)
            dest_file = dest_dir / source_path.name
            
            if dest_file.exists():
                dest_file = self.handle_duplicate(source_path, dest_file)
                if dest_file is None:
                    return False, f"File skipped (duplicate): {source_path.name}"
            
            if dry_run:
                return True, f"Would move {source_path} -> {dest_file}"
            
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_file))
            
            # Log this operation for undo functionality
            # Why we keep an undo log:
            # - Allows users to reverse organization if they don't like the result
            # - Provides peace of mind when organizing large numbers of files
            # - Essential safety feature for any tool that moves user files
            # - Enables batch undo operations
            if self.config.get_setting('create_undo_log', 'True') == 'True':
                self.undo_log.append({
                    'timestamp': datetime.now().isoformat(),  # When the operation happened
                    'source': str(source_path),               # Original location
                    'destination': str(dest_file),            # New location
                    'action': 'move'                          # Type of operation performed
                })
            
            self.stats['moved'] += 1
            return True, f"Moved {source_path.name} -> {dest_file}"
            
        except Exception as e:
            self.stats['errors'] += 1
            return False, f"Error moving {source_path.name}: {str(e)}"
    
    def organize_folder(self, source_folder, destination_folder, progress_callback=None, dry_run=False):
        """Organize all files in a folder."""
        source_folder = Path(source_folder)
        
        if not source_folder.exists():
            return False, f"Source folder does not exist: {source_folder}"
        
        all_files = []
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = Path(root) / file
                if not file.startswith(('.', '~')):
                    all_files.append(file_path)
        
        total_files = len(all_files)
        results = []
        
        for i, file_path in enumerate(all_files):
            if not self.running:
                break
                
            success, message = self.organize_file(file_path, destination_folder, dry_run)
            results.append((success, message))
            
            if progress_callback:
                progress_callback(i + 1, total_files, message)
        
        return True, results
    
    def save_undo_log(self):
        """Save undo log to file."""
        if self.undo_log:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"undo_log_{timestamp}.json"
            
            with open(log_file, 'w') as f:
                json.dump(self.undo_log, f, indent=2)
            
            return log_file
        return None
    
    def get_stats(self):
        """Get organization statistics."""
        return dict(self.stats)
    
    def undo_organization(self, undo_log_file, progress_callback=None):
        """
        Undo a previous organization operation using the undo log.
        
        Why we need undo functionality:
        - Users might not like how files were organized
        - Provides a safety net for large organization operations
        - Allows users to try different organization settings without fear
        - Essential for user confidence and trust in the tool
        
        Args:
            undo_log_file: Path to the JSON undo log file
            progress_callback: Optional callback for progress updates
            
        Returns:
            tuple: (success, results_list)
        """
        try:
            with open(undo_log_file, 'r') as f:
                undo_operations = json.load(f)
        except Exception as e:
            return False, f"Could not load undo log: {str(e)}"
        
        if not undo_operations:
            return False, "Undo log is empty"
        
        # Reverse the operations (last operation first)
        # Why reverse order: Files moved later might depend on folders created earlier
        undo_operations.reverse()
        
        total_operations = len(undo_operations)
        results = []
        successful_undos = 0
        failed_undos = 0
        
        for i, operation in enumerate(undo_operations):
            if not self.running:
                break
            
            try:
                # Extract paths from the logged operation
                # Extract and validate paths from the logged operation
                if 'source' not in operation or 'destination' not in operation:
                    message = f"Invalid operation entry: missing source or destination"
                    results.append((False, message))
                    failed_undos += 1
                    if progress_callback:
                        progress_callback(i + 1, total_operations, message)
                    continue
                
                source = Path(operation['source'])      # Original location
                destination = Path(operation['destination'])   # Current location
                
                # Check if the file is still in the organized location
                if not destination.exists():
                    message = f"File not found in organized location: {destination.name}"
                    results.append((False, message))
                    failed_undos += 1
                    if progress_callback:
                        progress_callback(i + 1, total_operations, message)
                    continue
                
                # Create the original directory structure if it doesn't exist
                source.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file back to original location
                shutil.move(str(destination), str(source))
                
                message = f"Restored {destination.name} -> {source}"
                results.append((True, message))
                successful_undos += 1
                
                if progress_callback:
                    progress_callback(i + 1, total_operations, message)
                    
            except Exception as e:
                message = f"Failed to restore {operation.get('destination', 'unknown')}: {str(e)}"
                results.append((False, message))
                failed_undos += 1
                
                if progress_callback:
                    progress_callback(i + 1, total_operations, message)
        
        # Clean up empty directories in the organized folder
        self._cleanup_empty_dirs()
        
        summary = f"Undo completed: {successful_undos} restored, {failed_undos} failed"
        return True, (results, summary)
    
    def _cleanup_empty_dirs(self):
        """
        Remove empty directories left after undo operations.
        
        Why we need this:
        - After moving files back, organized folders might be empty
        - Empty folders clutter the file system
        - Keeps the destination area clean
        """
        try:
            destination_base = Path(self.config.get_setting('destination_folder'))
            if not destination_base.exists():
                return
            
            # Walk through directories bottom-up to remove empty ones
            for root, dirs, files in os.walk(destination_base, topdown=False):
                for directory in dirs:
                    dir_path = Path(root) / directory
                    try:
                        if dir_path.exists() and not any(dir_path.iterdir()):
                            dir_path.rmdir()
                    except:
                        pass  # Ignore errors when removing directories
        except:
            pass  # Ignore errors in cleanup


class FileOrganizerGUI:
    """GUI for the file organizer."""
    
    def __init__(self):
        self.organizer = FileOrganizer()
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface."""
        self.root.title("Advanced File Organizer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_organize_tab()
        self.create_settings_tab()
        self.create_rules_tab()
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
    
    def create_organize_tab(self):
        """Create the main organize tab."""
        organize_frame = ttk.Frame(self.notebook)
        self.notebook.add(organize_frame, text="Organize Files")
        
        source_frame = ttk.LabelFrame(organize_frame, text="Source Folder", padding=10)
        source_frame.pack(fill='x', padx=10, pady=5)
        
        self.source_var = tk.StringVar(value=self.organizer.config.get_setting('source_folders', str(Path.home() / 'Downloads')))
        
        ttk.Label(source_frame, text="Select folder to organize:").pack(anchor='w')
        source_entry_frame = ttk.Frame(source_frame)
        source_entry_frame.pack(fill='x', pady=5)
        
        ttk.Entry(source_entry_frame, textvariable=self.source_var, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(source_entry_frame, text="Browse", command=self.browse_source_folder).pack(side='right', padx=(5, 0))
        
        dest_frame = ttk.LabelFrame(organize_frame, text="Destination Folder", padding=10)
        dest_frame.pack(fill='x', padx=10, pady=5)
        
        self.dest_var = tk.StringVar(value=self.organizer.config.get_setting('destination_folder', str(Path.home() / 'Organized Files')))
        
        ttk.Label(dest_frame, text="Select destination folder:").pack(anchor='w')
        dest_entry_frame = ttk.Frame(dest_frame)
        dest_entry_frame.pack(fill='x', pady=5)
        
        ttk.Entry(dest_entry_frame, textvariable=self.dest_var, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(dest_entry_frame, text="Browse", command=self.browse_dest_folder).pack(side='right', padx=(5, 0))
        
        options_frame = ttk.LabelFrame(organize_frame, text="Options", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.dry_run_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Dry run (preview only)", variable=self.dry_run_var).pack(anchor='w')
        
        progress_frame = ttk.LabelFrame(organize_frame, text="Progress", padding=10)
        progress_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to organize")
        self.progress_label.pack(anchor='w')
        
        self.results_text = tk.Text(progress_frame, height=10)
        scrollbar = ttk.Scrollbar(progress_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        text_frame = ttk.Frame(progress_frame)
        text_frame.pack(fill='both', expand=True, pady=5)
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        button_frame = ttk.Frame(organize_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        self.organize_button = ttk.Button(button_frame, text="Start Organizing", command=self.start_organizing)
        self.organize_button.pack(side='left', padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_organizing, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Clear Results", command=self.clear_results).pack(side='right')
    
    def create_settings_tab(self):
        """Create the settings tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        general_frame = ttk.LabelFrame(settings_frame, text="General Settings", padding=10)
        general_frame.pack(fill='x', padx=10, pady=5)
        
        self.auto_organize_var = tk.BooleanVar(value=self.organizer.config.get_setting('auto_organize', 'False') == 'True')
        ttk.Checkbutton(general_frame, text="Enable auto-organize", variable=self.auto_organize_var).pack(anchor='w')
        
        interval_frame = ttk.Frame(general_frame)
        interval_frame.pack(fill='x', pady=5)
        ttk.Label(interval_frame, text="Watch interval (seconds):").pack(side='left')
        self.interval_var = tk.StringVar(value=self.organizer.config.get_setting('watch_interval', '30'))
        ttk.Entry(interval_frame, textvariable=self.interval_var, width=10).pack(side='right')
        
        dup_frame = ttk.LabelFrame(settings_frame, text="Duplicate Handling", padding=10)
        dup_frame.pack(fill='x', padx=10, pady=5)
        
        self.duplicate_var = tk.StringVar(value=self.organizer.config.get_setting('handle_duplicates', 'rename'))
        ttk.Radiobutton(dup_frame, text="Rename duplicates", variable=self.duplicate_var, value='rename').pack(anchor='w')
        ttk.Radiobutton(dup_frame, text="Skip duplicates", variable=self.duplicate_var, value='skip').pack(anchor='w')
        ttk.Radiobutton(dup_frame, text="Overwrite duplicates", variable=self.duplicate_var, value='overwrite').pack(anchor='w')
        
        other_frame = ttk.LabelFrame(settings_frame, text="Other Options", padding=10)
        other_frame.pack(fill='x', padx=10, pady=5)
        
        self.undo_log_var = tk.BooleanVar(value=self.organizer.config.get_setting('create_undo_log', 'True') == 'True')
        ttk.Checkbutton(other_frame, text="Create undo log", variable=self.undo_log_var).pack(anchor='w')
        
        self.organize_by_date_var = tk.BooleanVar(value=self.organizer.config.get_setting('organize_by_date', 'True') == 'True')
        ttk.Checkbutton(other_frame, text="Organize by date", variable=self.organize_by_date_var).pack(anchor='w')
        
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).pack(pady=10)
    
    def create_rules_tab(self):
        """Create the rules management tab."""
        rules_frame = ttk.Frame(self.notebook)
        self.notebook.add(rules_frame, text="Organization Rules")
        
        ttk.Label(rules_frame, text="File organization rules:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        rules_text = tk.Text(rules_frame, height=20, width=80)
        scrollbar2 = ttk.Scrollbar(rules_frame, orient='vertical', command=rules_text.yview)
        rules_text.configure(yscrollcommand=scrollbar2.set)
        
        text_frame2 = ttk.Frame(rules_frame)
        text_frame2.pack(fill='both', expand=True, padx=10, pady=5)
        rules_text.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
        
        rules_display = json.dumps(self.organizer.rules, indent=2)
        rules_text.insert('1.0', rules_display)
        rules_text.config(state='disabled')
    
    def browse_source_folder(self):
        """Browse for source folder."""
        folder = filedialog.askdirectory(title="Select source folder to organize")
        if folder:
            self.source_var.set(folder)
    
    def browse_dest_folder(self):
        """Browse for destination folder."""
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.dest_var.set(folder)
    
    def save_settings(self):
        """Save current settings."""
        self.organizer.config.set_setting('auto_organize', str(self.auto_organize_var.get()))
        self.organizer.config.set_setting('watch_interval', self.interval_var.get())
        self.organizer.config.set_setting('handle_duplicates', self.duplicate_var.get())
        self.organizer.config.set_setting('create_undo_log', str(self.undo_log_var.get()))
        self.organizer.config.set_setting('organize_by_date', str(self.organize_by_date_var.get()))
        self.organizer.config.set_setting('source_folders', self.source_var.get())
        self.organizer.config.set_setting('destination_folder', self.dest_var.get())
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def progress_callback(self, current, total, message):
        """Update progress during organization."""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=f"Processing {current}/{total}: {Path(message.split(' -> ')[0] if ' -> ' in message else message).name}")
        self.results_text.insert(tk.END, message + '\n')
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_organizing(self):
        """Start the organization process."""
        source = self.source_var.get()
        destination = self.dest_var.get()
        
        if not source or not destination:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return
        
        if not Path(source).exists():
            messagebox.showerror("Error", "Source folder does not exist.")
            return
        
        self.clear_results()
        
        self.organize_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.organizer.running = True
        self.status_var.set("Organizing files...")
        
        def organize_thread():
            try:
                dry_run = self.dry_run_var.get()
                success, results = self.organizer.organize_folder(
                    source, destination, self.progress_callback, dry_run
                )
                
                stats = self.organizer.get_stats()
                if dry_run:
                    message = f"Dry run completed. Would organize {len(results)} files."
                else:
                    message = f"Organization completed! Moved: {stats.get('moved', 0)}, Errors: {stats.get('errors', 0)}"
                
                self.root.after(0, lambda: self.organization_complete(message))
                
            except Exception as e:
                self.root.after(0, lambda: self.organization_error(str(e)))
        
        threading.Thread(target=organize_thread, daemon=True).start()
    
    def stop_organizing(self):
        """Stop the organization process."""
        self.organizer.running = False
        self.organize_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Stopped")
    
    def organization_complete(self, message):
        """Handle completion of organization."""
        self.organize_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Complete")
        self.progress_var.set(100)
        self.progress_label.config(text=message)
        
        if not self.dry_run_var.get():
            log_file = self.organizer.save_undo_log()
            if log_file:
                self.results_text.insert(tk.END, f"\nUndo log saved to: {log_file}\n")
        
        messagebox.showinfo("Complete", message)
    
    def organization_error(self, error_message):
        """Handle organization errors."""
        self.organize_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Error")
        messagebox.showerror("Error", f"Organization failed: {error_message}")
    
    def clear_results(self):
        """Clear the results text area."""
        self.results_text.delete('1.0', tk.END)
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to organize")
        self.organizer.stats.clear()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for the application."""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        organizer = FileOrganizer()
        
        print("Advanced File Organizer - CLI Mode")
        print("=" * 40)
        
        source = input("Enter source folder path: ").strip()
        if not source:
            source = str(Path.home() / 'Downloads')
        
        destination = input("Enter destination folder path: ").strip()
        if not destination:
            destination = str(Path.home() / 'Organized Files')
        
        dry_run = input("Dry run? (y/N): ").strip().lower() == 'y'
        
        print(f"\nOrganizing files from: {source}")
        print(f"To: {destination}")
        print(f"Dry run: {dry_run}")
        print("-" * 40)
        
        def cli_progress(current, total, message):
            print(f"[{current}/{total}] {message}")
        
        organizer.running = True
        success, results = organizer.organize_folder(source, destination, cli_progress, dry_run)
        
        stats = organizer.get_stats()
        print("\n" + "=" * 40)
        print("Organization Complete!")
        print(f"Files processed: {len(results) if isinstance(results, list) else 0}")
        print(f"Files moved: {stats.get('moved', 0)}")
        print(f"Errors: {stats.get('errors', 0)}")
        
        if not dry_run:
            log_file = organizer.save_undo_log()
            if log_file:
                print(f"Undo log saved: {log_file}")
    
    else:
        app = FileOrganizerGUI()
        app.run()


if __name__ == '__main__':
    main() 