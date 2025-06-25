# 📁 Advanced File Organizer

**A powerful, user-friendly tool to automatically organize your files by type, date, and custom rules.**

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🌟 Why Use This File Organizer?

### The Problem
Do you find yourself spending valuable time searching through cluttered folders? Are your Downloads, Desktop, and Documents folders chaotic messes that stress you out? You're not alone! Studies show that office workers waste significant time daily just trying to locate files.

### The Solution
This Advanced File Organizer automatically sorts your files into logical categories and folders, giving you:

- **⏰ Time Savings**: Find files in seconds, not minutes
- **🧠 Reduced Mental Load**: Clean, organized digital spaces reduce stress
- **🚀 Improved Productivity**: Focus on what matters, not file management
- **🔄 Automated Workflows**: Set it and forget it with auto-organization
- **📊 Better System Performance**: Cleaner file structure = faster backups and searches

## ✨ Key Features

### 🎯 Smart Organization
- **Automatic Categorization**: Sorts files by type (Images, Documents, Audio, Video, etc.)
- **Date-Based Subfolders**: Organizes photos by year/month, videos by year
- **Custom Rules**: Define your own organization patterns
- **Duplicate Handling**: Rename, skip, or overwrite duplicate files

### 🖥️ Two Interfaces
- **Modern GUI**: Easy-to-use graphical interface with progress tracking
- **Command Line**: Perfect for automation and scripting
- **Drag & Drop**: Simple folder selection with browse buttons

### 🛡️ Safety Features
- **Dry Run Mode**: Preview changes before moving files
- **Undo Logging**: Complete history of all file movements
- **Error Handling**: Graceful handling of file conflicts and permissions
- **Progress Tracking**: Real-time updates during organization

### 🔧 Highly Configurable
- **Customizable Rules**: Edit organization patterns
- **Flexible Destinations**: Choose where files go
- **Auto-Organize**: Watch folders for new files
- **Multiple Source Folders**: Organize from multiple locations

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No additional packages required! Uses only Python standard library

### Installation

1. **Download the files:**
   ```bash
   git clone <repository-url>
   cd file-organizer
   ```

2. **What's included:**
   ```
   📦 File Organizer Package
   ├── 🐍 file_organizer.py      # Main application (GUI + CLI)
   ├── 🔄 undo_organizer.py      # Standalone undo tool  
   ├── 🚀 run_organizer.py       # Smart launcher with checks
   ├── ⚙️ config.ini             # Configuration file
   ├── 📖 README.md              # This documentation
   ├── ⚡ QUICK_START.md          # 5-minute getting started guide
   ├── 📋 requirements.txt        # Dependencies (none needed!)
   ├── 🪟 start_organizer.bat    # Windows launcher
   └── 🐧 start_organizer.sh     # Linux/macOS launcher
   ```

3. **Make it executable (Linux/macOS):**
   ```bash
   chmod +x *.sh *.py
   ```

4. **Run the application:**
   ```bash
   # Option 1: Smart launcher (recommended)
   python run_organizer.py
   
   # Option 2: Direct launch
   python file_organizer.py
   
   # Option 3: Platform-specific launchers
   # Windows: Double-click start_organizer.bat
   # Linux/macOS: Double-click start_organizer.sh
   ```

### First Time Setup

1. **Launch the application** - A modern GUI will open
2. **Select your source folder** (default: Downloads folder)
3. **Choose destination folder** (default: "Organized Files" in your home directory)
4. **Try a dry run first** - Check the "Dry run" option to preview changes
5. **Click "Start Organizing"** - Watch your files get organized!

## 📋 Usage Guide

### GUI Mode (Recommended for most users)

The graphical interface provides four main tabs:

#### 🗂️ Organize Files Tab
- **Source Folder**: Select the folder you want to organize
- **Destination Folder**: Where organized files will be moved
- **Dry Run Option**: Preview changes without moving files
- **Progress Tracking**: Real-time updates and results log

#### ⚙️ Settings Tab
- **Auto-organize**: Automatically organize new files
- **Watch Interval**: How often to check for new files
- **Duplicate Handling**: Choose how to handle duplicate files
- **Undo Logging**: Enable/disable operation history

#### 📝 Organization Rules Tab
- View current file categorization rules
- See which file types go into which folders
- Understand the organization structure

### Command Line Mode

For power users and automation:

```bash
# Basic usage
python file_organizer.py --cli

# Follow the prompts to:
# 1. Enter source folder path
# 2. Enter destination folder path  
# 3. Choose dry run mode
```

### 🔄 Undo Tool Usage

The standalone undo tool provides complete reversal of organization operations:

```bash
# Interactive mode - Shows available undo logs
python undo_organizer.py

# Example output:
# 🔄 File Organizer Undo Tool
# ========================================
# Found 2 undo log(s):
#   1. undo_log_20241225_143022.json (2024-12-25 14:30:22, 2.1MB)
#   2. undo_log_20241224_091545.json (2024-12-24 09:15:45, 0.8MB)
# 
# Choose an undo log (1-2): 1
# 
# Loading undo log: undo_log_20241225_143022.json
# Found 5,432 operations to undo
# Undo 5,432 file operations? (y/N): y

# Automated mode - For scripts and batch operations
python undo_organizer.py --yes    # Auto-confirms the most recent log
```

**Key Features:**
- 📊 **Smart Log Selection**: Automatically finds and lists available undo logs
- 📅 **Timestamp Display**: Shows when each organization operation occurred  
- 📈 **Progress Tracking**: Real-time feedback during undo operations
- 🧹 **Cleanup**: Automatically removes empty directories after undo
- ⚡ **Fast Processing**: Efficiently handles thousands of files
- 🛡️ **Safe Operation**: Comprehensive error handling and validation

## 📁 Before & After: See the Magic! ✨

### 😱 BEFORE (Typical Downloads Folder)
```
📁 Downloads/
├── 📄 important-document.pdf
├── 🖼️ vacation-photo.jpg  
├── 🖼️ screenshot.png
├── 📊 budget.xlsx
├── 🎵 favorite-song.mp3
├── 🎬 funny-video.mp4
├── 📦 software-installer.zip
├── 💻 my-script.py
├── 🌐 index.html
├── 📄 receipt.pdf
├── 📄 notes.txt
└── ... (hundreds more files!) 😵‍💫
```

### 🎉 AFTER (Organized Structure)
```
📁 Organized Files/
├── 📁 Images/
│   ├── 📁 2024/01/
│   │   ├── vacation-photo.jpg
│   │   └── screenshot.png
├── 📁 Documents/
│   ├── 📁 PDFs/
│   │   ├── important-document.pdf
│   │   └── receipt.pdf
│   └── 📁 Text Files/
│       └── notes.txt
├── 📁 Office/
│   └── 📁 Spreadsheets/
│       └── budget.xlsx
├── 📁 Audio/
│   └── favorite-song.mp3
├── 📁 Video/
│   └── 📁 2024/
│       └── funny-video.mp4
├── 📁 Development/
│   ├── 📁 Python/
│   │   └── my-script.py
│   └── 📁 Web/
│       └── index.html
└── 📁 Archives/
    └── software-installer.zip
```

**Result: From chaos to perfect organization in seconds!** 🚀

## 🔧 Configuration

### File Types Supported

| Category | File Extensions |
|----------|----------------|
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.svg`, `.webp`, `.ico`, `.heic` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.pages` |
| **Office** | `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.csv`, `.numbers`, `.keynote` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a` |
| **Video** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz` |
| **Development** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.php`, `.rb`, `.go`, `.rs`, `.swift` |
| **Software** | `.exe`, `.msi`, `.dmg`, `.pkg`, `.deb`, `.rpm`, `.appimage` |

### Customizing Rules

Edit the `config.ini` file to customize:
- File type categorization
- Destination folder structure
- Date formatting preferences
- Duplicate handling behavior

## 🛡️ Safety & Recovery

### Dry Run Mode
Always test with dry run mode first! This shows you exactly what would happen without actually moving files.

### Undo Functionality ⚡ NEW!
Every organization operation creates an undo log (`undo_log_YYYYMMDD_HHMMSS.json`) containing:
- Source file paths
- Destination file paths  
- Timestamps
- Operation details

**Standalone Undo Tool**: Use `undo_organizer.py` to reverse any organization:
```bash
# Quick undo (will prompt for confirmation)
python undo_organizer.py

# Auto-confirm undo (for automation)
python undo_organizer.py --yes
```

The undo tool automatically:
- ✅ Finds all undo log files  
- ✅ Shows operation details and timestamps
- ✅ Restores files to original locations
- ✅ Cleans up empty organized folders
- ✅ Provides detailed progress feedback

**Perfect for:**
- Testing different organization rules
- Reversing accidental organization  
- Trying the tool risk-free
- Batch operations with confidence

### Error Handling
The application gracefully handles:
- Permission errors
- Missing files/folders
- Disk space issues
- Network drive problems

## 💡 Pro Tips

### 🎯 Best Practices
1. **Start Small**: Test on a small folder first
2. **Use Dry Run**: Always preview changes before organizing
3. **Keep Undo Logs**: Save undo logs until you're happy with organization
4. **Test with Undo**: Try organizing → undo → adjust rules → organize again
5. **Regular Backups**: Keep backups of important files
6. **Review Rules**: Check organization rules match your needs
7. **Clean Regularly**: Run organization weekly/monthly

### 🚀 Power User Features
- **Batch Processing**: Organize multiple folders by running multiple times
- **Automation**: Use CLI mode in scripts for automatic organization
- **Custom Categories**: Edit config.ini to add new file types
- **Date Formats**: Customize how date-based folders are named

### 📊 Performance Tips
- Close other applications when organizing large folders
- Organize from local drives (not network drives) for best speed
- Use SSD drives for faster file operations

## 🔍 Troubleshooting

### Common Issues

**❓ Files not organizing as expected**
- Check file extensions in the Rules tab
- Verify source and destination paths
- Ensure you have write permissions

**❓ Application won't start**
- Ensure Python 3.6+ is installed
- Check if `tkinter` is available (usually included with Python)
- Try command line mode: `python file_organizer.py --cli`

**❓ Permission errors**
- Run as administrator (Windows) or with sudo (Linux/macOS)
- Check folder permissions
- Ensure destination folder is writable

**❓ Slow performance**
- Organize smaller batches of files
- Close other applications
- Use local drives instead of network drives

**❓ Undo not working**
- Check if undo log file exists (`undo_log_*.json`)
- Verify files are still in organized locations
- Ensure you have write permissions to original folders
- Try running with `python undo_organizer.py --yes` for automated mode

**❓ Want to test safely**
- Use dry run mode first: Check "Dry run" in GUI
- Keep undo logs: Don't delete `undo_log_*.json` files
- Try on small folder first, then undo to verify everything works
- Backup important files before first use

### Getting Help
1. Check this README thoroughly
2. Review the config.ini file for customization options
3. Try dry run mode to debug issues
4. Check the generated undo logs for operation details

## 📋 Quick Command Reference

**Copy-paste commands for different scenarios:**

```bash
# First time setup
git clone <repository-url>
cd file-organizer
chmod +x *.py *.sh

# Launch the organizer (choose one)
python run_organizer.py           # Smart launcher (recommended)
python file_organizer.py          # Direct GUI launch
python file_organizer.py --cli    # Command line mode

# Test safely
python file_organizer.py          # Check "Dry run" first!

# Undo if needed
python undo_organizer.py          # Interactive undo
python undo_organizer.py --yes    # Auto-confirm undo

# Platform-specific shortcuts
./start_organizer.sh              # Linux/macOS
start_organizer.bat               # Windows (double-click)
```

**Default file locations (cross-platform):**
- Source: `~/Downloads` (your Downloads folder)
- Destination: `~/Organized Files` (will be created automatically)  
- Undo logs: Same folder as the scripts

## 🎯 Complete Example Workflow

**Scenario**: You have 1,000+ files in your Downloads folder and want to organize them safely.

### Step 1: Download & Setup
```bash
# Download the organizer  
git clone <repository-url>
cd file-organizer

# Make executable (Linux/macOS)
chmod +x *.py *.sh
```

### Step 2: Test Run
```bash
# Launch GUI
python run_organizer.py

# In the GUI:
# ✅ Check "Dry run" option
# ✅ Source: /home/username/Downloads (or browse to select)
# ✅ Destination: /home/username/Organized Files (or browse to select)  
# ✅ Click "Start Organizing"
# ✅ Review the preview - no files actually moved yet!
```

### Step 3: Real Organization
```bash
# Uncheck "Dry run" and run again
# ✅ Files are now organized into categories
# ✅ Undo log automatically created: undo_log_20241225_143022.json
```

### Step 4: Verify Results
```bash
# Check your organized files
ls "~/Organized Files"
# Should show: Images/ Documents/ Audio/ Video/ Development/ etc.

# Check specific categories
ls "~/Organized Files/Images"
# Should show year folders like: 2023/ 2024/
```

### Step 5: Undo if Needed
```bash
# Don't like the result? Undo it!
python undo_organizer.py

# Output:
# 🔄 File Organizer Undo Tool
# Found 1 undo log(s):
#   1. undo_log_20241225_143022.json (2024-12-25 14:30:22, 2.1MB)
# 
# Loading undo log...
# Found 1,247 operations to undo
# Undo 1,247 file operations? (y/N): y
# 
# [Progress bar showing files being restored...]
# ✅ Successfully restored: 1,247
# 🎉 Undo completed successfully!
```

### Step 6: Perfect Your Setup
```bash
# Edit organization rules if needed
nano config.ini

# Try again with new settings
python run_organizer.py
```

**Total time investment: ~10 minutes for a lifetime of organized files!** ⏱️

## 🤝 Contributing

This tool was designed to solve real-world file organization problems. If you have suggestions for improvements:

1. **Feature Requests**: What file types or organization patterns would help you?
2. **Bug Reports**: Include steps to reproduce and your system info
3. **Performance**: Share your experience with large file collections
4. **Usability**: How can we make it even easier to use?

## 📄 License

This project is released under the MIT License - feel free to use, modify, and distribute!

## 🎉 Final Words

File organization doesn't have to be a chore! This tool transforms the tedious task of manual file sorting into an automated, reliable process. Whether you're cleaning up years of accumulated files or maintaining an organized system going forward, the Advanced File Organizer has you covered.

**Ready to reclaim your time and reduce digital clutter? Download and run the organizer today!**

---

*Made with ❤️ for everyone who's ever spent too much time looking for that one file they know they saved somewhere...* 