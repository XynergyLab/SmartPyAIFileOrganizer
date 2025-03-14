# metadata.py
import os
import subprocess
import json
import logging
from datetime import datetime
from PIL import Image, ExifTags
from pymediainfo import MediaInfo

logging.basicConfig(level=logging.DEBUG)

def extract_basic_metadata(file_path):
    try:
        stat = os.stat(file_path)
        file_size = stat.st_size
        created_time = datetime.fromtimestamp(stat.st_ctime).isoformat()
        modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
        accessed_time = datetime.fromtimestamp(stat.st_atime).isoformat()
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1].lower()
        return {
            'file_path': file_path,
            'file_name': file_name,
            'file_extension': file_extension,
            'file_size': file_size,
            'created_time': created_time,
            'modified_time': modified_time,
            'accessed_time': accessed_time,
        }
    except Exception as e:
        logging.error("Error extracting basic metadata for %s: %s", file_path, e)
        return {}

def extract_image_metadata(file_path):
    metadata = {}
    try:
        with Image.open(file_path) as img:
            metadata['format'] = img.format
            metadata['mode'] = img.mode
            metadata['size'] = img.size
            exif_data = img._getexif()
            if exif_data:
                exif = {}
                for tag, value in exif_data.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    exif[decoded] = value
                metadata['exif'] = exif
    except Exception as e:
        logging.error("Error extracting image metadata for %s: %s", file_path, e)
    return metadata

def extract_video_metadata(file_path):
    metadata = {}
    try:
        # Using pymediainfo to extract video metadata
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "Video":
                metadata['duration'] = track.duration  # in ms
                metadata['width'] = track.width
                metadata['height'] = track.height
                metadata['frame_rate'] = track.frame_rate
                metadata['codec'] = track.codec
    except Exception as e:
        logging.error("Error extracting video metadata for %s: %s", file_path, e)
    return metadata

def extract_extended_metadata(file_path):
    basic = extract_basic_metadata(file_path)
    ext = basic.get('file_extension', '')
    extended = {}
    if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
        logging.debug("Extracting image metadata for %s", file_path)
        extended = extract_image_metadata(file_path)
    elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.m4v']:
        logging.debug("Extracting video metadata for %s", file_path)
        extended = extract_video_metadata(file_path)
    else:
        logging.debug("No extended metadata for %s", file_path)
    combined = basic.copy()
    combined['extended'] = extended
    return combined

