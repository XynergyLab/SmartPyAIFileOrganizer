# deduplicator.py
import hashlib
import logging

def compute_file_hash(file_path, algorithm='sha256', chunk_size=8192):
    hash_func = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        logging.error("Error computing hash for %s: %s", file_path, e)
        return None

