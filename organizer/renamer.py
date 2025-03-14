# renamer.py
import os
import logging

def standardize_filename(metadata):
    """
    Generate a standardized filename based on metadata.
    For example: YYYYMMDD_originalname.ext
    """
    created_time = metadata.get('created_time', '')
    file_name = metadata.get('file_name', '')
    name_without_ext = os.path.splitext(file_name)[0]
    ext = metadata.get('file_extension', '')
    try:
        dt = created_time.split("T")[0].replace("-", "")
    except Exception as e:
        dt = "unknown"
    new_name = f"{dt}_{name_without_ext}{ext}"
    new_name = new_name.replace(" ", "_").lower()
    return new_name

def rename_file(file_path, new_name):
    """
    Rename a file to new_name in the same directory.
    """
    dir_path = os.path.dirname(file_path)
    new_path = os.path.join(dir_path, new_name)
    try:
        os.rename(file_path, new_path)
        logging.info("Renamed %s to %s", file_path, new_path)
        return new_path
    except Exception as e:
        logging.error("Error renaming file %s: %s", file_path, e)
        return None

