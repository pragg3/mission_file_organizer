import os
import streamlit as st
from datetime import datetime
from collections import defaultdict
from file_handler import get_exif_date

def group_files_by_date(all_files, current_path):
    files_by_date = defaultdict(list)
    for f in all_files:
        full_path = os.path.join(current_path, f)
        dt = get_exif_date(full_path)
        if not dt:
            continue
        if isinstance(dt, str):
            dt = datetime.strptime(dt, "%Y%m%d_%H%M%S")
        date_str = dt.strftime("%Y%m%d")
        files_by_date[date_str].append((f, dt.hour, dt.minute))
    return files_by_date

def manage_intervals(files_by_date):
    st.subheader("Step 4: Select Mission Date(s) / Multiple Hour Intervals")
    available_dates = sorted(files_by_date.keys())
    selected_dates = st.multiselect("Select Mission Date(s):", available_dates)

    files_in_mission = []
    subfolder_name = ""

    if selected_dates:
        for selected_date in selected_dates:
            files_for_date = files_by_date[selected_date]
            hours_in_date = sorted(set((h, m) for _, h, m in files_for_date))
            select_hours = st.checkbox(f"Select specific hour intervals for {selected_date}.")

            if select_hours:
                st.markdown(f"**Manage intervals for {selected_date}:**")

                if f"{selected_date}_intervals" not in st.session_state:
                    st.session_state[f"{selected_date}_intervals"] = []

                col_add, col_remove = st.columns(2)
                with col_add:
                    if st.button(f"➕ Add Interval for {selected_date}"):
                        new_interval = {"start": "", "end": ""}
                        existing_intervals = st.session_state.get(f"{selected_date}_intervals", [])
                        if new_interval in existing_intervals:
                            st.warning("This interval already exists!")
                        else:
                            st.session_state[f"{selected_date}_intervals"].append(new_interval)

                with col_remove:
                    if st.button(f"➖ Remove Last Interval for {selected_date}") and st.session_state[f"{selected_date}_intervals"]:
                        st.session_state[f"{selected_date}_intervals"].pop()

                for idx, interval in enumerate(st.session_state[f"{selected_date}_intervals"]):
                    col1, col2 = st.columns(2)
                    time_options = [f"{h:02d}:{m:02d}" for h, m in hours_in_date]

                    with col1:
                        interval["start"] = st.selectbox(
                            f"Interval {idx+1} Start ({selected_date}):",
                            time_options,
                            index=time_options.index(interval["start"]) if interval["start"] in time_options else 0,
                            key=f"{selected_date}_start_{idx}"
                        )
                    with col2:
                        if interval["start"]:
                            end_options = [t for t in time_options if tuple(map(int, t.split(':'))) >= tuple(map(int, interval["start"].split(':')))]
                        else:
                            end_options = time_options.copy()
                        if not end_options:
                            end_options = time_options.copy()
                        interval["end"] = st.selectbox(
                            f"Interval {idx+1} End ({selected_date}):",
                            end_options,
                            index=end_options.index(interval["end"]) if interval["end"] in end_options else 0,
                            key=f"{selected_date}_end_{idx}"
                        )

                for interval in st.session_state[f"{selected_date}_intervals"]:
                    if interval["start"] and interval["end"]:
                        start_h, start_m = map(int, interval["start"].split(":"))
                        end_h, end_m = map(int, interval["end"].split(":"))
                        files_in_mission.extend([
                            f for f, h, m in files_for_date
                            if (h, m) >= (start_h, start_m) and (h, m) <= (end_h, end_m)
                        ])
            else:
                files_in_mission.extend([f for f, h, m in files_for_date])

        files_in_mission = list(set(files_in_mission))
        st.write(f"Total files selected: {len(files_in_mission)}")

    return selected_dates, files_in_mission, subfolder_name
