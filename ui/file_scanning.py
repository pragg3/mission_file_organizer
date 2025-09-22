import os
import streamlit as st
from collections import defaultdict
from core.drives import scan_folder_recursive
from file_scanner import scan_folder

def scan_and_report(current_path, include_subfolders):
    st.subheader("Step 3: Scan Folder Contents")

    if include_subfolders:
        all_files = scan_folder_recursive(current_path)
        total_files = len(all_files)
        file_types = defaultdict(int)
        for f in all_files:
            ext = os.path.splitext(f)[1].lower()
            file_types[ext] += 1
    else:
        all_files, total_files, file_types = scan_folder(current_path)

    st.write(f"Total files found: {total_files}")
    st.table({k: v for k, v in file_types.items()})
    return all_files, total_files, file_types
