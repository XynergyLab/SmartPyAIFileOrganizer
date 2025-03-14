# scanner.py
import os
import logging
import json
from metadata import extract_extended_metadata
from deduplicator import compute_file_hash

def scan_directory(root_dir, conn):
    """
    Recursively scan a directory, extract extended metadata from each file,
    compute file hash, and insert the data into the SQLite database.
    """
    cursor = conn.cursor()
    logging.info("Starting scan of directory: %s", root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        logging.debug("Scanning directory: %s", dirpath)
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            metadata = extract_extended_metadata(file_path)
            file_hash = compute_file_hash(file_path)
            extended_json = json.dumps(metadata.get('extended', {}))
            try:
                cursor.execute('''
                    INSERT INTO files 
                    (file_path, file_name, file_extension, file_size, created_time, modified_time, accessed_time, metadata, file_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metadata.get('file_path'),
                    metadata.get('file_name'),
                    metadata.get('file_extension'),
                    metadata.get('file_size'),
                    metadata.get('created_time'),
                    metadata.get('modified_time'),
                    metadata.get('accessed_time'),
                    extended_json,
                    file_hash
                ))
                logging.debug("Inserted metadata for: %s", file_path)
            except Exception as e:
                logging.error("DB insertion error for %s: %s", file_path, e)
    conn.commit()
    logging.info("Scanning complete.")

