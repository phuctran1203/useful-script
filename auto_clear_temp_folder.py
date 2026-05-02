import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple

def human_size(b: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PiB"


def calculate_size(item_path: str) -> int:
    """Calculate total size of a file or directory."""
    try:
        if os.path.isfile(item_path):
            return os.path.getsize(item_path)
        total = 0
        for dirpath, dirnames, filenames in os.walk(item_path, followlinks=False):
            for fn in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, fn))
                except Exception:
                    pass
        return total
    except Exception:
        return 0


def delete_item(item_path: str) -> Tuple[bool, str, int]:
    """Delete a single item safely. Returns (success, message, size_freed)."""
    try:
        size = calculate_size(item_path)
        
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path, ignore_errors=False)
        
        return True, f"✔ Deleted: {os.path.basename(item_path)}", size
    except Exception as e:
        return False, f"✘ Failed: {os.path.basename(item_path)} → {str(e)}", 0


def clear_temp(n_days=10, dry_run=False, max_workers=8):
    temp_dir = os.getenv("TEMP") if os.name == "nt" else "/tmp"
    age_limit = n_days * 86400  # Convert days to seconds
    items_to_delete = []

    if not os.path.exists(temp_dir):
        print("⚠ Temp folder does not exist.")
        return

    print(f"🔍 Scanning {temp_dir}...\n")
    
    # Find old files/folders (skip symlinks, system files)
    for item in os.scandir(temp_dir):
        item_path = item.path
        try:
            # Skip symlinks for safety
            if os.path.islink(item_path):
                continue
            
            if time.time() - item.stat().st_mtime > age_limit:
                items_to_delete.append(item_path)
        except Exception:
            pass

    # Check if there's anything to delete
    if not items_to_delete:
        print(f"✅ No files/folders older than {n_days} day(s) found in TEMP.")
        return

    # Calculate total size
    print(f"📊 Found {len(items_to_delete)} item(s) older than {n_days} day(s)\n")
    
    total_size = 0
    for i, item_path in enumerate(items_to_delete[:15], 1):
        size = calculate_size(item_path)
        total_size += size
        item_name = os.path.basename(item_path)
        item_type = "📁" if os.path.isdir(item_path) else "📄"
        print(f"  {i:2d}. {item_type} {item_name:<40} {human_size(size)}")
    
    if len(items_to_delete) > 15:
        remaining_size = sum(calculate_size(p) for p in items_to_delete[15:])
        total_size += remaining_size
        print(f"  ... and {len(items_to_delete) - 15} more item(s)")
    
    print(f"\n💾 Total space to free: {human_size(total_size)}")
    print("-" * 70)
    
    if dry_run:
        print("✅ [DRY RUN] No files were deleted. Run without --dry-run to actually delete.")
        return
    
    # Confirmation
    confirm = input("\n⚠️  This will PERMANENTLY DELETE the above items. Type 'DELETE' to continue: ").strip()
    if confirm != "DELETE":
        print("🚫 Deletion cancelled.")
        return

    # Parallel deletion
    print("\n🗑️  Deleting items...\n")
    deleted_count = 0
    freed_size = 0
    failed_items = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(delete_item, path): path for path in items_to_delete}
        
        for future in as_completed(futures):
            success, message, size = future.result()
            if success:
                print(message)
                deleted_count += 1
                freed_size += size
            else:
                # Print truncated version during deletion
                print(f"{message[:80]}...")
                # Save full message for summary
                failed_items.append(message)
    
    print(f"\n✅ Successfully deleted {deleted_count}/{len(items_to_delete)} item(s)")
    print(f"💾 Freed approximately {human_size(freed_size)}")
    
    # Print failed deletions summary with full reasons
    if failed_items:
        print(f"\n⚠️  {len(failed_items)} item(s) failed to delete:")
        print("-" * 70)
        for failed_msg in failed_items:
            print(f"  {failed_msg}")
        print("-" * 70)

if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv
    n_days = 1  # Delete files older than 1 day
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be deleted\n")
    
    clear_temp(n_days, dry_run=dry_run)
