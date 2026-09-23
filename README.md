# Useful Scripts 🛠️

A collection of lightweight, high-performance Python utility scripts and standalone Windows executables designed to quickly clean up disk space.

---

## 📁 Repository Structure

```
useful-script/
├── scripts/                      # Python source scripts
│   ├── auto_clear_node_modules.py
│   └── auto_clear_temp_folder.py
├── specs/                        # PyInstaller build specification recipes
│   ├── auto_clear_node_modules.spec
│   └── auto_clear_temp_folder.spec
├── dist/                         # Pre-built standalone Windows executables (.exe)
│   ├── auto_clear_node_modules.exe
│   └── auto_clear_temp_folder.exe
├── build.py                      # Build runner to compile scripts to exe
├── .gitignore
└── README.md
```

---

## 🚀 Standalone Executables (No Python Required)

Pre-built standalone `.exe` binaries are provided in the [`dist/`](dist/) folder. End users do not need to install Python or any dependencies:

- **[`dist/auto_clear_temp_folder.exe`](dist/auto_clear_temp_folder.exe)** — Cleans Windows `%TEMP%` directory.
- **[`dist/auto_clear_node_modules.exe`](dist/auto_clear_node_modules.exe)** — Recursively scans and cleans `node_modules` (and custom targets like `.next`, `dist`, `build`, etc.).

> **Tip:** You can double-click either `.exe` directly in Windows Explorer. A terminal window will open to display progress and prompt for confirmation, and will stay open when finished so you can inspect the summary before dismissing it.

---

## 📂 Included Utilities

### 1. Auto Clear Temp Folder (`scripts/auto_clear_temp_folder.py`)

Scans your system temporary folder (`%TEMP%` on Windows, `/tmp` on macOS/Linux) for files and directories older than 1 day and safely cleans them up using multi-threaded parallel deletion.

#### Features:
- **Safe:** Skips symlinks and handles in-use/locked files gracefully without crashing.
- **Preview & Estimation:** Lists found items and calculates total recoverable space.
- **Confirmation Protection:** Requires typing `DELETE` before deleting anything.
- **Dry-run Support:** Preview what would be deleted without touching any files.
- **Multi-threaded Deletion:** Uses 8 background workers for rapid file removal.

#### Usage:
- **Run Standalone EXE:**
  ```powershell
  .\dist\auto_clear_temp_folder.exe
  ```
- **Dry Run (Preview Only):**
  ```powershell
  .\dist\auto_clear_temp_folder.exe --dry-run
  ```
- **Run with Python:**
  ```powershell
  python scripts/auto_clear_temp_folder.py [--dry-run]
  ```

---

### 2. Auto Clear Node Modules & Build Artifacts (`scripts/auto_clear_node_modules.py`)

Recursively scans any directory (e.g. your workspace or projects root) to find and remove bulky `node_modules` folders, build outputs, and caches.

#### Features:
- **Fast Scanning:** Prunes search traversal upon encountering target directories (doesn't waste time scanning *inside* `node_modules`).
- **Flexible Targets:** Cleans `node_modules` by default, with optional prompts to include `.next`, `dist`, `build`, `.cache`, `coverage`, etc.
- **Size Estimation:** Accurately estimates disk space consumption for each detected directory.
- **Confirmation Protection:** Requires typing `YES` before deleting anything.
- **Multi-threaded Deletion:** Fast parallel cleanup using 8 workers.

#### Usage:
- **Run Standalone EXE:**
  ```powershell
  .\dist\auto_clear_node_modules.exe
  ```
- **Run with Python:**
  ```powershell
  python scripts/auto_clear_node_modules.py
  ```
- When prompted, paste or drag-and-drop the directory path you want to scan.

---

## 🛠️ Building Executables from Source

If you add new scripts or modify existing ones, you can compile them to standalone `.exe` packages using the included `build.py` script:

1. **Install PyInstaller:**
   ```powershell
   pip install pyinstaller
   ```

2. **Build All Scripts:**
   ```powershell
   python build.py
   ```

3. **Build a Specific Script:**
   ```powershell
   python build.py auto_clear_temp_folder
   # or
   python build.py auto_clear_node_modules
   ```

All generated `.exe` files will be placed into [`dist/`](dist/) and their respective `.spec` configurations saved in [`specs/`](specs/).

---

## 📄 License

MIT License. Free to use, modify, and distribute.
