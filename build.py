"""
Build runner for useful-script repository.
Automatically compiles Python scripts in scripts/ into standalone executables in dist/
while organizing PyInstaller specification files in specs/.

Usage:
    python build.py              # Builds all scripts in scripts/
    python build.py <name>       # Builds a specific script (e.g. python build.py auto_clear_temp_folder)
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
SCRIPTS_DIR = ROOT_DIR / "scripts"
SPECS_DIR = ROOT_DIR / "specs"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"


def build_script(script_path: Path):
    name = script_path.stem
    print(f"\n🔨 Building {name}...")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--console",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
        "--specpath",
        str(SPECS_DIR),
        "--name",
        name,
        str(script_path),
    ]

    result = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if result.returncode == 0:
        exe_path = DIST_DIR / f"{name}.exe"
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Successfully built: {exe_path.relative_to(ROOT_DIR)} ({size_mb:.2f} MB)")
    else:
        print(f"❌ Failed to build: {name} (exit code {result.returncode})")
        sys.exit(result.returncode)


def main():
    SPECS_DIR.mkdir(exist_ok=True)
    DIST_DIR.mkdir(exist_ok=True)

    args = sys.argv[1:]
    if args:
        targets = []
        for arg in args:
            target = SCRIPTS_DIR / (arg if arg.endswith(".py") else f"{arg}.py")
            if not target.exists():
                print(f"❌ Script not found: {target}")
                sys.exit(1)
            targets.append(target)
    else:
        targets = sorted(SCRIPTS_DIR.glob("*.py"))

    if not targets:
        print("No Python scripts found in scripts/ directory.")
        return

    print(f"📦 Found {len(targets)} script(s) to build in {SCRIPTS_DIR.name}/:")
    for t in targets:
        print(f"  • {t.name}")

    for script in targets:
        build_script(script)

    print("\n🎉 All builds complete! Executables available in dist/")


if __name__ == "__main__":
    main()
