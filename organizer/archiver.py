# archiver.py
import os
import shutil
import logging
from datetime import datetime

def archive_file(file_path, archive_root):
    """
    Move file to an archive directory based on its modified date.
    For example: archive_root/YYYY/MM/DD/
    """
    try:
        modified_time = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(modified_time)
        archive_dir = os.path.join(archive_root, dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d"))
        os.makedirs(archive_dir, exist_ok=True)
        new_path = os.path.join(archive_dir, os.path.basename(file_path))
        shutil.move(file_path, new_path)
        logging.info("Archived %s to %s", file_path, new_path)
        return new_path
    except Exception as e:
        logging.error("Error archiving file %s: %s", file_path, e)
        return None

