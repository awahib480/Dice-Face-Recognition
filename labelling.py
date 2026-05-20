import os

# ================== EDIT THESE VALUES ==================
folder_path = r"C:\W\6. S 2026\dice\dataset\6"
prefix = "6"
start_number = 1
padding = 3
# =======================================================

files = sorted(os.listdir(folder_path))

# Keep only files
files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

# ---------- STEP 1: Rename everything to temp ----------
temp_names = []

for i, file in enumerate(files):
    old_path = os.path.join(folder_path, file)
    temp_name = f"__temp_{i}__{os.path.splitext(file)[1]}"
    temp_path = os.path.join(folder_path, temp_name)
    
    os.rename(old_path, temp_path)
    temp_names.append(temp_name)

# ---------- STEP 2: Rename to final names ----------
counter = start_number

for file in temp_names:
    ext = os.path.splitext(file)[1]
    new_name = f"{prefix}_{str(counter).zfill(padding)}{ext}"
    
    old_path = os.path.join(folder_path, file)
    new_path = os.path.join(folder_path, new_name)
    
    os.rename(old_path, new_path)
    print(f"Renamed -> {new_name}")
    
    counter += 1

print("Renaming completed!")
