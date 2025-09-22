# import os
# import streamlit as st
# from core.drives import list_drives, list_folders

# def drive_and_folder_selector():
#     st.subheader("Step 1: Select Drive")
#     drives = list_drives()
#     selected_drive = st.selectbox("Select Drive:", drives, key="drive_select")

#     current_path = None
#     if selected_drive:
#         st.subheader("Step 2: Browse Folders")
#         current_path = selected_drive
#         while True:
#             folders = list_folders(current_path)
#             if not folders:
#                 break
#             selected_folder = st.selectbox(
#                 f"Folders in {current_path}", [""] + folders, key=f"folder_{current_path}"
#             )
#             if not selected_folder:
#                 break
#             current_path = os.path.join(current_path, selected_folder)
#         st.write(f"Selected Folder: {current_path}")

#     return current_path


#network viewer!!!


# import os
# import streamlit as st
# from core.drives import list_drives, list_folders
# from ui.transfer import detect_network

# def drive_and_folder_selector():
#     st.subheader("Step 1: Select Drive")
    
#     # Detect local drives
#     drives = list_drives()
    
#     # Detect network
#     network = detect_network()  
      
#     network_path = fr"\\{network}"
#     if os.path.exists(network_path):
#         drives.append(network_path)  

#     # 3️⃣ Select drive
#     selected_drive = st.selectbox("Select Drive:", drives, key="drive_select")

#     current_path = None
#     if selected_drive:
#         st.subheader("Step 2: Browse Folders")
#         current_path = selected_drive
#         while True:
#             folders = list_folders(current_path)
#             if not folders:
#                 break
#             selected_folder = st.selectbox(
#                 f"Folders in {current_path}", [""] + folders, key=f"folder_{current_path}"
#             )
#             if not selected_folder:
#                 break
#             current_path = os.path.join(current_path, selected_folder)
#         st.write(f"Selected Folder: {current_path}")

#     return current_path


# import os
# import streamlit as st
# import win32net
# import win32netcon
# from core.drives import list_folders  # reuse your existing function
# from ui.transfer import detect_network  # optional if you want to keep

# import ctypes
# import string

# def get_drives():
#     drives = []
#     bitmask = ctypes.windll.kernel32.GetLogicalDrives()
#     for i in range(26):
#         if bitmask & (1 << i):
#             drives.append(f"{string.ascii_uppercase[i]}:\\")
#     return drives

# print(get_drives())

# def list_all_network_shares():
#     """Return all accessible disk shares from visible network servers."""
#     shares = []
#     servers = list_network_servers()
#     for server in servers:
#         shares.extend(list_shares(server))
#     return shares

# def list_network_servers():
#     """Return a list of servers visible on the network."""
#     servers = []
#     try:
#         result, _, _ = win32net.NetServerEnum(None, 100, win32netcon.SV_TYPE_SERVER, None, 0)
#         for s in result:
#             servers.append(s['name'])
#     except Exception as e:
#         print("Cannot enumerate servers:", e)
#     return servers

# def list_shares(server):
#     """Return a list of disk shares on a server."""
#     shares = []
#     try:
#         result, _, _ = win32net.NetShareEnum(server, 2)
#         for share in result:
#             if share['type'] == win32netcon.STYPE_DISKDEV:
#                 path = rf"\\{server}\{share['netname']}"
#                 if os.path.exists(path):
#                     shares.append(path)
#     except Exception as e:
#         print(f"Cannot enumerate shares on {server}: {e}")
#     return shares

# def drive_and_folder_selector():
#     st.subheader("Step 1: Select Drive")

#     # Detect local drives + network shares
#     drives = get_drives()

#     # Optional: include detect_network() if you want additional logic
#     network_name = detect_network()  
#     if network_name:
#         network_path = fr"\\{network_name}"
#         if os.path.exists(network_path) and network_path not in drives:
#             drives.append(network_path)

#     # Select drive
#     selected_drive = st.selectbox("Select Drive:", drives, key="drive_select")

#     current_path = None
#     if selected_drive:
#         st.subheader("Step 2: Browse Folders")
#         current_path = selected_drive
#         while True:
#             folders = list_folders(current_path)
#             if not folders:
#                 break
#             selected_folder = st.selectbox(
#                 f"Folders in {current_path}", [""] + folders, key=f"folder_{current_path}"
#             )
#             if not selected_folder:
#                 break
#             current_path = os.path.join(current_path, selected_folder)
#         st.write(f"Selected Folder: {current_path}")

#     return current_path






import os
import streamlit as st
import sys

# Only import Windows modules if running on Windows
if sys.platform == "win32":
    import win32net
    import win32netcon
    import ctypes
    import string

    def get_drives():
        drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                drives.append(f"{string.ascii_uppercase[i]}:\\")
        return drives

    def list_network_servers():
        servers = []
        try:
            result, _, _ = win32net.NetServerEnum(None, 100, win32netcon.SV_TYPE_SERVER, None, 0)
            for s in result:
                servers.append(s['name'])
        except Exception as e:
            print("Cannot enumerate servers:", e)
        return servers

    def list_shares(server):
        shares = []
        try:
            result, _, _ = win32net.NetShareEnum(server, 2)
            for share in result:
                if share['type'] == win32netcon.STYPE_DISKDEV:
                    path = rf"\\{server}\{share['netname']}"
                    if os.path.exists(path):
                        shares.append(path)
        except Exception as e:
            print(f"Cannot enumerate shares on {server}: {e}")
        return shares

    def list_all_network_shares():
        shares = []
        for server in list_network_servers():
            shares.extend(list_shares(server))
        return shares

else:
    # Linux / Mac fallback
    def get_drives():
        # On Linux/Mac, return root "/" as default
        return ["/"]

    def list_all_network_shares():
        return []

# Common function for both platforms
def drive_and_folder_selector():
    st.subheader("Step 1: Select Drive")
    drives = get_drives()
    
    selected_drive = st.selectbox("Select Drive:", drives, key="drive_select")

    current_path = None
    if selected_drive:
        st.subheader("Step 2: Browse Folders")
        current_path = selected_drive
        while True:
            from core.drives import list_folders  # safe import
            folders = list_folders(current_path)
            if not folders:
                break
            selected_folder = st.selectbox(
                f"Folders in {current_path}", [""] + folders, key=f"folder_{current_path}"
            )
            if not selected_folder:
                break
            current_path = os.path.join(current_path, selected_folder)
        st.write(f"Selected Folder: {current_path}")

    return current_path
