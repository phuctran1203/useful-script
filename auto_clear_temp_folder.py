import os
import shutil
import time

def clear_temp(n_days=10):
    temp_dir = os.getenv("TEMP") if os.name == "nt" else "/tmp"
    age_limit = n_days * 86400  # Chuyển ngày thành giây
    items_to_delete = []

    if not os.path.exists(temp_dir):
        print("⚠ Thư mục TEMP không tồn tại.")
        return

    # Tìm các file/thư mục cũ hơn n ngày
    for item in os.scandir(temp_dir):
        item_path = item.path
        try:
            if time.time() - item.stat().st_mtime > age_limit:
                items_to_delete.append(item_path)
        except Exception:
            pass

    # Kiểm tra nếu không có file nào để xóa
    if not items_to_delete:
        print(f"✅ Không có file/thư mục nào cũ hơn {n_days} ngày trong TEMP.")
        return

    # Hiển thị danh sách file/thư mục sắp xóa
    print(f"🔍 Tìm thấy {len(items_to_delete)} file/thư mục cũ hơn {n_days} ngày trong TEMP.")
    for item in items_to_delete[:10]:  # Hiển thị tối đa 10 mục đầu tiên
        print(f"   - {item}")
    if len(items_to_delete) > 10:
        print(f"   ... và {len(items_to_delete) - 10} mục khác.")

    # Hỏi xác nhận
    confirm = input("❓ Bạn có muốn xóa không? (y/n): ").strip().lower()
    if confirm != "y":
        print("🚫 Hủy xóa TEMP.")
        return

    # Tiến hành xóa
    deleted_count = 0
    for item_path in items_to_delete:
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
            deleted_count += 1
        except Exception:
            pass

    print(f"✅ Đã xóa {deleted_count} file/thư mục trong TEMP.")

if __name__ == "__main__":
    clear_temp(1)  # Xóa file/thư mục cũ hơn 10 ngày
