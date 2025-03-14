# structure.py
import os
import logging
import shutil

def restructure_directory(file_metadata, base_target_dir):
    """
    Restructure a file into a dynamic folder layout based on metadata.
    For example, by file extension and modified date.
    """
    try:
        ext = file_metadata.get('file_extension', '').strip('.')
        modified_time = file_metadata.get('modified_time', '')
        date_folder = modified_time.split("T")[0] if modified_time else "unknown_date"
        target_dir = os.path.join(base_target_dir, ext, date_folder)
        os.makedirs(target_dir, exist_ok=True)
        current_path = file_metadata.get('file_path')
        new_path = os.path.join(target_dir, file_metadata.get('file_name'))
        shutil.move(current_path, new_path)
        logging.info("Moved %s to %s", current_path, new_path)
        return new_path
    except Exception as e:
        logging.error("Error restructuring file %s: %s", file_metadata.get('file_path'), e)
        return None

