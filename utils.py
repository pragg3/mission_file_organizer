import os
import re


def get_folder_path(prompt):
    while True:
        path = input(prompt).strip()
        if os.path.exists(path) and os.path.isdir(path):
            return path
        print("Invalid folder path. Please try again.")

def get_dates_filter():
    while True:
        filters_input = input(
            "Enter filters (examples: 20250811, 14:00 - 16:00, 20250811 10:00 - 13:00; separate multiple with commas): "
        ).strip()
        if filters_input:
            return filters_input
        print("Invalid input. Try again.")

def get_mission_name():
    mission_name = input("Enter mission name (e.g., SantoAndre): ").strip()
    return mission_name if mission_name else "Mission"

def sanitize_folder_name(name):
    """Replace invalid Windows path characters with underscores."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)
