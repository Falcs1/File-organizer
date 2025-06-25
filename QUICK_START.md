# 🚀 Quick Start Guide

**Get your files organized in under 5 minutes!**

## Super Quick Start (3 Steps)

### 1. Download & Run
```bash
# Download all files to a folder
# Double-click one of these files based on your system:
```

**Windows Users:** Double-click `start_organizer.bat`
**Mac/Linux Users:** Double-click `start_organizer.sh` (or run it in terminal)
**Any System:** Run `python run_organizer.py`

### 2. Choose Your Mode
- **GUI Mode** (Recommended): Easy graphical interface
- **CLI Mode**: Command line for power users

### 3. Organize!
1. Select your source folder (default: Downloads)
2. Choose destination folder (default: Organized Files)
3. Check "Dry run" to preview first
4. Click "Start Organizing"

## That's It! 🎉

Your files are now organized into neat categories:
- 📸 Images → `Images/2024/01/`
- 📄 Documents → `Documents/PDFs/`, `Documents/Word Documents/`
- 🎵 Music → `Audio/`
- 🎬 Videos → `Video/2024/`
- 💻 Code → `Development/Python/`, `Development/Web/`
- And more!

## 🔄 Don't Like the Result? Undo It!

**New Feature**: Complete undo functionality!

```bash
# Undo the organization (will ask for confirmation)
python undo_organizer.py

# Or auto-confirm for quick undo
python undo_organizer.py --yes
```

**What happens:**
- ✅ All files moved back to original locations
- ✅ Empty organized folders are cleaned up  
- ✅ You can try different settings risk-free
- ✅ Perfect for testing and experimenting

**The tool automatically finds your undo logs and shows:**
- When each organization happened
- How many files were moved
- Easy selection of which operation to undo

## Need Help?

**Files not moving as expected?**
- Try "Dry run" first to see what will happen
- Check the "Organization Rules" tab to see file types
- Make sure you have write permissions to the destination folder

**Want to customize?**
- Edit `config.ini` to change organization rules
- Add new file types or modify existing categories
- Change how files are organized by date

**Still stuck?**
- Read the full `README.md` for detailed instructions
- Check your Python version (needs 3.6+)
- Make sure all files are in the same folder

## Pro Tips

✅ **Always start with a dry run** to see what will happen  
✅ **Try the undo feature** - organize a small folder then undo it to see how it works
✅ **Keep undo logs safe** until you're happy with the organization
✅ **Backup important files** before first use
✅ **Start with a small folder** to test it out
✅ **Organize regularly** (weekly/monthly) for best results

## 🛡️ Risk-Free Testing Workflow

**Perfect for first-time users:**

1. **Small Test**: Organize just a few files first
2. **Dry Run**: Check "Dry run" to preview changes
3. **Real Run**: Organize the small folder for real
4. **Test Undo**: Run `python undo_organizer.py` to reverse it
5. **Confidence**: Now you know exactly how it works!
6. **Go Big**: Organize your entire Downloads folder with confidence

## Common File Types Organized

| What You Have | Where It Goes |
|---------------|---------------|
| `photo.jpg`, `image.png` | → `Images/2024/01/` |
| `document.pdf`, `report.docx` | → `Documents/PDFs/`, `Documents/Word Documents/` |
| `song.mp3`, `audio.wav` | → `Audio/` |
| `movie.mp4`, `video.avi` | → `Video/2024/` |
| `archive.zip`, `backup.rar` | → `Archives/` |
| `script.py`, `webpage.html` | → `Development/Python/`, `Development/Web/` |
| `app.exe`, `installer.msi` | → `Software/` |

**Ready to get organized? Run the organizer now!** 🚀 