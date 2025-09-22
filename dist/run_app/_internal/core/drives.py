import os
import psutil

def list_drives():
    drives = []
    for p in psutil.disk_partitions(all=False):
        if os.name == "nt":
            drives.append(p.device)
        else:
            drives.append(p.mountpoint)
    return drives

def list_folders(path):
    try:
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        filtered = []
        for f in folders:
            try:
                os.listdir(os.path.join(path, f))
                filtered.append(f)
            except (PermissionError, FileNotFoundError):
                continue
        return filtered
    except Exception:
        return []

def scan_folder_recursive(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            full_path = os.path.join(root, f)
            all_files.append(os.path.relpath(full_path, folder_path))
    return all_files
