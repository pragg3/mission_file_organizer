import os
import streamlit as st
from file_handler import move_or_copy_files, create_destination_folder
from utils import sanitize_folder_name


def detect_network():
    possible_networks = ["kakapo", "CASUAR"]
    for net in possible_networks:
        test_path = fr"\\{net}\MIDAS"
        if os.path.exists(test_path):
            return net
    return "unknown"

network = detect_network()


def transfer_files(selected_dates, subfolder_name, files_in_mission, current_path):
    st.subheader("Step 5: Copy/Move Mission Files")
    mission_folder_name = "_".join(selected_dates)
    sanitized_mission = sanitize_folder_name(mission_folder_name)

    dest_users = {
        "Albatroz": fr"\\{network}\MIDAS\Albatroz",
        "UNAC": fr"\\{network}\MIDAS\UNAC",
        "Air Touraine": fr"\\{network}\MIDAS\Air Touraine",
        
    }
    dest_choice = st.selectbox("Select User:", list(dest_users.keys()))
    dest_root = dest_users[dest_choice]

    final_dest_path = os.path.join(dest_root, sanitized_mission)
    if subfolder_name:
        final_dest_path = os.path.join(final_dest_path, sanitize_folder_name(subfolder_name))

    st.info(f"Files will be saved to User : {dest_choice}")

    action = st.radio("Action:", ["copy", "move"])

    if "cancel_transfer" not in st.session_state:
        st.session_state.cancel_transfer = False

    col1, col2 = st.columns(2)
    with col1:
        start_transfer = st.button("🚀 Start Transfer")
    with col2:
        cancel_transfer = st.button("🛑 Cancel Transfer")

    if cancel_transfer:
        st.session_state.cancel_transfer = True
        st.warning("Transfer has been cancelled!")

    if start_transfer:
        st.session_state.cancel_transfer = False
        final_dest = create_destination_folder(dest_root, sanitized_mission)
        if subfolder_name:
            final_dest = create_destination_folder(final_dest, sanitize_folder_name(subfolder_name))

        progress_bar = st.progress(0)
        total_files_to_transfer = len(files_in_mission)

        copied_count = 0
        skipped_files = []

        for idx, f in enumerate(files_in_mission, 1):
            if st.session_state.cancel_transfer:
                st.error("❌ Transfer cancelled by user.")
                break

            copied, skipped = move_or_copy_files([f], current_path, final_dest, action)
            copied_count += copied
            skipped_files.extend(skipped)

            progress_bar.progress(idx / total_files_to_transfer)
        else:
            action_past = {"copy": "copied", "move": "moved"}
            st.success(f"{copied_count} files {action_past[action]} to {dest_choice}")
            if skipped_files:
                st.warning(f"{len(skipped_files)} files were skipped because they already exist.")
                import pandas as pd

                with st.expander("See skipped files"):
                    if skipped_files:
                        df = pd.DataFrame(skipped_files, columns=["Skipped Files"])
                        st.dataframe(df, height=300)
                    else:
                        st.info("No skipped files!")

