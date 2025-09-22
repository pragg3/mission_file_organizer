import os
import shutil
import re
import subprocess
from datetime import datetime

import os
from datetime import datetime
from PIL import Image
from pymediainfo import MediaInfo

def get_exif_date(file_path):
    """Return date in YYYYMMDD_HHMMSS format from EXIF or filesystem."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        # For images, use Pillow EXIF
        if ext in [".jpg", ".jpeg", ".png", ".tiff", ".heic"]:
            try:
                img = Image.open(file_path)
                exif = img._getexif()
                if exif:
                    date_str = exif.get(36867)  # DateTimeOriginal
                    if date_str:
                        if "+" in date_str or "-" in date_str[10:]:
                            date_str = date_str.split()[0] + " " + date_str.split()[1]
                        dt = datetime.strptime(date_str[:19], "%Y:%m:%d %H:%M:%S")
                        return dt.strftime("%Y%m%d_%H%M%S")
            except Exception:
                pass
        
        # For videos, use pymediainfo
        else:
            try:
                media_info = MediaInfo.parse(file_path)
                for track in media_info.tracks:
                    if track.track_type == "General":
                        # try MediaCreateDate or other_creation_date
                        date_str = (
                            track.other_creation_date[0] 
                            if track.other_creation_date 
                            else getattr(track, "encoded_date", None)
                        )
                        if date_str:
                            # format: 2020-01-01 12:34:56
                            date_str = date_str[:19].replace("-", ":")
                            dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                            return dt.strftime("%Y%m%d_%H%M%S")
            except Exception:
                pass
        
    except Exception:
        pass
    
    # Fallback to filesystem timestamp
    try:
        ts = os.path.getmtime(file_path)
        return datetime.fromtimestamp(ts).strftime("%Y%m%d_%H%M%S")
    except Exception:
        return None


# --- Filters ---
def parse_filters(filters_raw):
    parsed_filters = []
    for f in filters_raw.split(","):
        f = f.strip()
        if not f:
            continue
        # Date + time range (e.g., 20250519 8:13 - 9:00)
        m = re.match(r'^(\d{8})\s+(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})$', f)
        if m:
            parsed_filters.append({"date": m.group(1), "start": m.group(2), "end": m.group(3)})
            continue
        # Time range only (e.g., 14:00 - 16:00)
        m = re.match(r'^(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})$', f)
        if m:
            parsed_filters.append({"date": None, "start": m.group(1), "end": m.group(2)})
            continue
        # Date only (e.g., 20250811)
        m = re.match(r'^\d{8}$', f)
        if m:
            parsed_filters.append({"date": f, "start": None, "end": None})
            continue
    return parsed_filters

def _parse_time(s):
    return datetime.strptime(s.strip(), "%H:%M").time()

def file_matches_filters(file_dt, filters):
    for flt in filters:
        if flt["date"] and file_dt.strftime("%Y%m%d") != flt["date"]:
            continue
        if flt["start"] and flt["end"]:
            t = file_dt.time()
            start = _parse_time(flt["start"])
            end = _parse_time(flt["end"])
            if not (start <= t <= end):
                continue
        return True
    return False

def filter_files_by_flexible_filters(all_files, filters_raw, source_folder):
    filters = parse_filters(filters_raw)
    matched = []
    for f in all_files:
        file_path = os.path.join(source_folder, f)
        file_dt = get_exif_date(file_path)
        if not file_dt:
            continue
        if isinstance(file_dt, str):
            file_dt = datetime.strptime(file_dt, "%Y%m%d_%H%M%S")
        if file_matches_filters(file_dt, filters):
            matched.append(f)
    return matched

# --- File Operations ---
def create_destination_folder(dest_root, folder_name):
    final_dest = os.path.join(dest_root, folder_name)
    os.makedirs(final_dest, exist_ok=True)
    return final_dest

def move_or_copy_files(filtered_files, source_folder, final_dest, action="copy"):
    copied_count = 0
    skipped_files = []

    for f in filtered_files:
        # If f is already absolute, use it directly
        src = f if os.path.isabs(f) else os.path.join(source_folder, f)
        dst = os.path.join(final_dest, os.path.basename(f))

        if os.path.exists(dst):
            skipped_files.append(os.path.basename(f))
            continue

        if action == "copy":
            shutil.copy2(src, dst)
        else:
            shutil.move(src, dst)

        copied_count += 1

    return copied_count, skipped_files
