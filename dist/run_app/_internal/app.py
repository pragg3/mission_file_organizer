import streamlit as st
from ui.drive_browser import drive_and_folder_selector
from ui.file_scanning import scan_and_report
from ui.interval_manager import group_files_by_date, manage_intervals
from ui.previewer import preview_file
from ui.transfer import transfer_files

st.set_page_config(page_title="Mission File Organizer", layout="wide")
st.title("📂 Mission File Organizer")

st.markdown(
    """
    **Instructions:**  
    1️⃣ Select the drive and navigate to the folder containing your mission files.  
    2️⃣ The app will scan the folder and automatically detect missions by date.  
    3️⃣ You can optionally select specific hour ranges, or process the full day.  
    4️⃣ Preview files before transferring.  
    5️⃣ Choose to copy/move files.  
    """
)

current_path = drive_and_folder_selector()

if current_path:
    include_subfolders = True
    all_files, total_files, file_types = scan_and_report(current_path, include_subfolders)

    files_by_date = group_files_by_date(all_files, current_path)
    selected_dates, files_in_mission, subfolder_name = manage_intervals(files_by_date)

    preview_file(current_path, files_in_mission)

    if files_in_mission:
        transfer_files(selected_dates, subfolder_name, files_in_mission, current_path)
