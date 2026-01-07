# GUI Features Documentation

## 🎨 Visual Design

### Color Scheme
- **Background:** Dark (#1e1e1e, #2d2d2d)
- **Foreground:** Light Gray (#e0e0e0)
- **Accent Primary:** Cyan (#00bcd4)
- **Accent Secondary:** Purple (#667eea)
- **Success:** Green (#4caf50)

### Typography
- **Headers:** Segoe UI, 28pt, Bold
- **Titles:** Segoe UI, 12pt, Bold
- **Body:** Segoe UI, 10pt
- **Console:** Consolas, 9pt (monospace)

## 🖼️ Screen Layout

### Main Window (1400x900)
```
┌─────────────────────────────────────────────────────────┐
│  🔍 Forensics Analyzer              v2.0.0 | Parth      │
│  Professional Digital Forensics & File Carving Tool     │
├─────────────────────────────────────────────────────────┤
│  File  Tools  View  Help                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  [Generate & Carve] [Results & Analysis] [Help] │  │
│  ├──────────────────────────────────────────────────┤  │
│  │                                                  │  │
│  │         Tab Content Area                        │  │
│  │                                                  │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Ready                      © 2025 Forensics Analyzer   │
└─────────────────────────────────────────────────────────┘
```

## 🎬 Splash Screen (2 seconds)

```
┌─────────────────────────┐
│                         │
│         🔍              │
│                         │
│  Forensics Analyzer     │
│  Major Project          │
│                         │
│  Version 2.0.0          │
│  Developed by           │
│  Parth Thakar          │
│                         │
│  Loading...             │
│                         │
└─────────────────────────┘
```

## 📑 Tab 1: Generate & Carve

### Layout
```
┌──────────────────────────────┬──────────────────────┐
│ Configuration Panel          │  Console Output      │
│                              │                      │
│ ┌─ Step 1: Generate ───────┐│  [Console Area]      │
│ │ Size: [10] MB            ││                      │
│ │ Output: [........] Browse││  Real-time logs      │
│ │ Files: ☑JPG ☑PNG ☑PDF   ││  with scrolling      │
│ │        ☑TXT ☑DOCX ☑MP3  ││                      │
│ │ [Generate Disk Image]    ││                      │
│ └──────────────────────────┘│                      │
│                              │                      │
│ ┌─ Step 2: Carve ──────────┐│                      │
│ │ Image: [........] Browse ││                      │
│ │ Output: [........] Browse││                      │
│ │ Min Size: [1024] bytes   ││                      │
│ │ [Start Carving]          ││                      │
│ └──────────────────────────┘│                      │
│                              │                      │
│ ┌─ Step 3: Binwalk ────────┐│  [Progress Bar]      │
│ │ [Run Binwalk Analysis]   ││  ████░░░░░░ 40%     │
│ └──────────────────────────┘│                      │
└──────────────────────────────┴──────────────────────┘
```

### Features
- **Image Size Selector:** Spin box for MB selection
- **File Type Checkboxes:** Multi-select file types
- **Path Browsers:** File/folder selection dialogs
- **Action Buttons:** Large, prominent buttons
- **Real-time Console:** Scrolling output with colors
- **Progress Bar:** Indeterminate during operations

## 📊 Tab 2: Results & Analysis

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ [📁 Open] [🔄 Refresh] [📊 Export] [🔍 Preview]         │
│                             Search: [____________]       │
├─────────────────────────────────────────────────────────┤
│ ID │ Name         │ Type │ Size      │ Valid │ Hash    │
├────┼──────────────┼──────┼───────────┼───────┼─────────┤
│ 1  │ file_001.jpg │ JPG  │ 8,000 B   │ ✓     │ a1b2... │
│ 2  │ file_002.png │ PNG  │ 6,000 B   │ ✓     │ c3d4... │
│ 3  │ file_003.pdf │ PDF  │ 12,000 B  │ ✓     │ e5f6... │
│ 4  │ file_004.txt │ TXT  │ 256 B     │ ✗     │ N/A     │
│ ... (scrollable)                                        │
└─────────────────────────────────────────────────────────┘
┌─ Statistics ────────────────────────────────────────────┐
│ 📊 Total: 45 | ✓ Valid: 42 | ✗ Invalid: 3 | 💾 2.3 MB │
│ 📁 JPG: 15, PNG: 10, PDF: 8, TXT: 5, DOCX: 4, MP3: 3  │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Toolbar Buttons:** Quick actions with icons
- **Search Box:** Real-time filtering
- **Tree View:** Multi-column sortable table
- **Statistics Panel:** Comprehensive analysis
- **Double-click:** Preview file in default app
- **Context Menu:** Right-click actions

## ⚙️ Tab 3: Settings & Help

### Sub-tabs Layout
```
┌─────────────────────────────────────────────────────────┐
│ [Settings] [User Guide] [About]                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Settings Tab:                                          │
│  ┌─ Application Settings ──────────────────────────┐  │
│  │ Theme: [Dark ▼]                                 │  │
│  │ Evidence Dir: /path/to/evidence                 │  │
│  │ Output Dir: /path/to/output                     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                          │
│  User Guide Tab:                                        │
│  ┌─ Scrollable Guide ──────────────────────────────┐  │
│  │ ╔════════════════════════════════════════════╗  │  │
│  │ ║  FORENSICS ANALYZER - USER GUIDE          ║  │  │
│  │ ╚════════════════════════════════════════════╝  │  │
│  │                                                 │  │
│  │ OVERVIEW                                        │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │ Comprehensive guide with sections...           │  │
│  │ (Scrollable content)                            │  │
│  └─────────────────────────────────────────────────┘  │
│                                                          │
│  About Tab:                                             │
│  ┌─ About This Application ─────────────────────────┐  │
│  │ 🔍 Forensics Analyzer - Major Project          │  │
│  │                                                  │  │
│  │ Version: 2.0.0                                  │  │
│  │ Author: Parth Thakar                           │  │
│  │                                                  │  │
│  │ Features, Technology Stack, File Types...       │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Menu Bar

### File Menu
```
File
├─ New Analysis         Ctrl+N
├─ Open Output Folder   Ctrl+O
├─ ─────────────────────────
├─ Export Report        Ctrl+E
├─ ─────────────────────────
└─ Exit                 Ctrl+Q
```

### Tools Menu
```
Tools
├─ Calculate File Hash
├─ Verify Carved Files
└─ Clear Console        Ctrl+L
```

### View Menu
```
View
├─ Refresh Results      F5
└─ Full Screen          F11
```

### Help Menu
```
Help
├─ User Guide           F1
├─ Keyboard Shortcuts
├─ ─────────────────────────
└─ About
```

## 💬 Dialogs

### Hash Calculator Dialog (700x300)
```
┌─────────────────────────────────────────┐
│  File Hash Calculator                   │
├─────────────────────────────────────────┤
│  File: example.jpg                      │
│  Size: 8,000 bytes                      │
│                                          │
│  MD5:     [a1b2c3d4e5f6...........] ⎘  │
│  SHA-256: [9f8e7d6c5b4a...........] ⎘  │
│                                          │
│         [Copy MD5] [Copy SHA-256]       │
└─────────────────────────────────────────┘
```

### Keyboard Shortcuts Dialog (500x400)
```
┌─────────────────────────────────────────┐
│  ⌨️ Keyboard Shortcuts                   │
├─────────────────────────────────────────┤
│  ┌──────────┐  New Analysis             │
│  │ Ctrl+N  │  ← Shortcut key            │
│  └──────────┘                            │
│                                          │
│  ┌──────────┐  Open Output Folder       │
│  │ Ctrl+O  │                            │
│  └──────────┘                            │
│  ... (more shortcuts)                    │
└─────────────────────────────────────────┘
```

## 🎨 Console Styling

### Color Coding
- **Green (#00ff00):** Success messages
- **Yellow (#ffff00):** Warnings
- **Red (#ff0000):** Errors
- **Cyan (#00bcd4):** Information
- **White (#ffffff):** General output

### Example Output
```
════════════════════════════════════════
     FORENSICS ANALYZER
════════════════════════════════════════

[*] Generating disk image...
[+] Embedded jpg file #1 at offset 10000
[+] Embedded png file #2 at offset 20000
[✓] Disk image generated successfully!

[*] Carving files...
[+] Carved: file_001.jpg (8,000 bytes)
[+] Carved: file_002.png (6,000 bytes)
[✓] Carving complete! (2 files)

[*] Parsing results...
[✓] Analysis complete!
```

## 🎭 UI States

### Loading State
- Progress bar: Indeterminate animation
- Buttons: Disabled
- Console: Showing progress
- Status: "Processing..."

### Idle State
- Progress bar: Hidden
- Buttons: Enabled
- Console: Ready for input
- Status: "Ready"

### Error State
- Message box with error details
- Console shows error in red
- Status: "Error occurred"
- Buttons: Re-enabled

## 📱 Responsive Design

### Window Resizing
- Minimum size: 1200x800
- Expandable to full screen (F11)
- Console and results auto-resize
- Maintains layout proportions

### Element Scaling
- Buttons: Fixed height, flexible width
- Tables: Scrollable when needed
- Text: Fixed font sizes
- Spacing: Proportional padding

## 🎯 Accessibility Features

1. **Keyboard Navigation:** Full keyboard support
2. **Tooltips:** Hover hints (future enhancement)
3. **Clear Labels:** Descriptive text
4. **High Contrast:** Dark theme with good contrast
5. **Status Updates:** Real-time feedback
6. **Error Messages:** Clear error descriptions

## 🔔 Notifications

### Success Messages
- Green checkmark ✓
- "Success" title
- Details in message
- Console confirmation

### Warning Messages
- Yellow exclamation ⚠️
- "Warning" title
- Reason explained
- Suggestions provided

### Error Messages
- Red X ✗
- "Error" title
- Error details
- Troubleshooting hints

---

**Forensics Analyzer GUI v2.0.0**
*Professional Interface Design*
