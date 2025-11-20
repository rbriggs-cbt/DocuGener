# DocuGener User Guide

## Introduction

DocuGener is a screen capture and documentation tool that helps you create step-by-step guides by automatically capturing screenshots when you Ctrl+Click on your screen.

## Installation

### Step 1: Install Python

Download and install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

### Step 2: Set Up DocuGener

1. Download or clone the DocuGener repository
2. Open a terminal/command prompt

**Setup:**
```bash
cd DocuGener/app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Getting Started

### Starting the Application

1. **Start DocuGener:**
   ```bash
   cd app
   python main.py
   ```
   You should see: "Starting DocuGener..." and "Web interface available at http://localhost:5000"

2. **Open in Browser:**
   Navigate to `http://localhost:5000` in your web browser

## Using DocuGener

### Capturing Screenshots

1. **Enable Capture Mode:**
   - The application starts in "Recording" mode by default
   - You'll see a green status indicator in the control panel

2. **Take a Screenshot:**
   - **Press and hold Ctrl**
   - **Left-click** anywhere on your screen
   - A screenshot will be automatically captured with a red pointer highlight

3. **View Your Captures:**
   - All captures appear in the web interface automatically
   - They're displayed in chronological order (oldest first)

### Managing Captures

#### Adding Context

1. Find the capture you want to describe
2. Type your description in the text box below the image
3. The context is automatically saved after you stop typing

#### Deleting Captures

1. Click the trash can icon (🗑️) in the top-right corner of a capture
2. Confirm the deletion in the dialog box
3. The capture and its image will be permanently deleted

#### Pausing Capture

1. Click the "Pause" button in the control panel
2. The status will change to "Paused" (yellow indicator)
3. Click "Resume" to start capturing again

### Exporting Your Documentation

1. Click the "Export" button in the control panel
2. Choose your format:
   - **PowerPoint (.pptx)**: Creates a presentation with one slide per capture
   - **PDF**: Creates a PDF document with all captures
3. Click "Export"
4. The file will download to your default download folder

### Control Panel

The control panel at the top of the interface provides:

- **Status Indicator**: Shows if capture is active (green) or paused (yellow)
- **Pause/Resume Button**: Toggle capture functionality
- **Export Button**: Export captures to PowerPoint or PDF
- **Minimize Button**: Collapse the control panel to a top bar

## Tips and Best Practices

### Creating Good Documentation

1. **Plan Your Steps**: Think about the sequence before starting
2. **Add Clear Context**: Describe what each step does
3. **Use Consistent Naming**: Keep window titles clear
4. **Review Before Export**: Delete any unwanted captures

### Keyboard Shortcuts

- **Ctrl+Click**: Capture screenshot
- **Ctrl+C**: Stop DocuGener (in terminal)

### Troubleshooting

**Captures not appearing:**
- Ensure the DocuGener service is running
- Check that you're accessing `http://localhost:5000`
- Refresh the browser page

**Screenshots not capturing:**
- Ensure you're using **Ctrl+Click** (not just Click)
- Check that capture is not paused
- Verify the app is running and shows "Click detection is active"

**Export not working:**
- Ensure you have at least one capture
- Check browser download settings
- Try a different export format

**Window titles not showing:**
- This feature works best on Windows 10+
- Some applications may not provide window titles

## Advanced Usage

### Customizing Capture Behavior

Currently, capture requires Ctrl+Click. This prevents accidental captures during normal computer use.

### Storage Location

Captures are stored in:
- **Images**: `captures/*.png` (in project root)
- **Metadata**: `captures/metadata.json`
- **Projects**: `projects.db` (in project root)

You can manually backup the `captures/` folder and `projects.db` file to preserve your data.

### Multiple Sessions

Each time you start DocuGener, new captures are added to the existing collection. To start fresh, you can:
1. Delete all PNG files in `captures/` (keep `metadata.json` if you want to preserve structure)
2. Or manually edit `captures/metadata.json` to remove entries
3. Or delete `projects.db` to remove all project data

## Support

For issues, questions, or contributions:
- Check the [Development Guide](development.md) for technical details
- Review the [API Reference](api-reference.md) for integration options
- See [Architecture Overview](architecture.md) for system design

## Frequently Asked Questions

**Q: Can I use this on Mac or Linux?**
A: The window detection features are Windows-specific. The core functionality may work, but window titles and URLs may not be detected.

**Q: Can I change the capture hotkey?**
A: Currently, Ctrl+Click is hardcoded. This can be modified in `app/click_detector.py` for future versions.

**Q: How do I share my documentation?**
A: Export to PowerPoint or PDF, then share the file. The exported files are standalone and don't require DocuGener to view.

**Q: Can I edit captures after taking them?**
A: You can add or edit context text, but you cannot edit the images themselves. Delete and recapture if needed.

**Q: Is my data stored securely?**
A: All data is stored locally on your computer. No data is sent to external servers.

