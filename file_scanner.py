import os
from collections import Counter

def scan_folder(folder_path):
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(all_files)
    file_types = Counter([os.path.splitext(f)[1].lower() for f in all_files])
    return all_files, total_files, file_types

def report_files(total_files, file_types):
    print(f"\nFound {total_files} files.")
    print("File types found:")
    for ext, count in file_types.items():
        print(f"  {ext if ext else 'no extension'}: {count}")
