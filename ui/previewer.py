import os
import streamlit as st

def preview_file(current_path, files_in_mission):
    if files_in_mission:
        st.subheader("Preview Files")
        selected_file = st.selectbox("Select a file to preview:", [""] + files_in_mission)
        if selected_file:
            file_path = os.path.join(current_path, selected_file)
            st.write(f"File: {file_path}")
            ext = os.path.splitext(selected_file)[1].lower()
            if ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]:
                st.image(file_path)
            elif ext in [".mp4", ".mov", ".avi"]:
                st.video(file_path)
            elif ext in [".srt", ".txt", ".log"]:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    st.text(f.read())
            else:
                st.write("Cannot preview this file type.")
