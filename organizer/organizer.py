#!/usr/bin/env python3
import os
import sys
import argparse
import logging
from db import init_db
from scanner import scan_directory
from renamer import standardize_filename, rename_file
from archiver import archive_file
from structure import restructure_directory
from metadata import extract_basic_metadata

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cli_scan(directory):
    conn = init_db()
    scan_directory(directory, conn)
    conn.close()

def cli_rename(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            metadata = extract_basic_metadata(old_path)
            new_name = standardize_filename(metadata)
            rename_file(old_path, new_name)

def cli_archive(directory, archive_root):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            archive_file(file_path, archive_root)

def cli_structure(directory, target_root):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            metadata = extract_basic_metadata(file_path)
            restructure_directory(metadata, target_root)

def cli_monitor():
    from system_monitor import monitor_drives
    monitor_drives()

def main():
    parser = argparse.ArgumentParser(description="Smart Organization App")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")
    
    scan_parser = subparsers.add_parser("scan", help="Scan directory and store metadata")
    scan_parser.add_argument("directory", help="Directory to scan")
    
    rename_parser = subparsers.add_parser("rename", help="Rename files based on metadata")
    rename_parser.add_argument("directory", help="Directory to rename files in")
    
    archive_parser = subparsers.add_parser("archive", help="Archive files into a structured directory")
    archive_parser.add_argument("directory", help="Directory to archive files from")
    archive_parser.add_argument("archive_root", help="Root directory for archives")
    
    structure_parser = subparsers.add_parser("structure", help="Restructure files into a new directory layout")
    structure_parser.add_argument("directory", help="Directory to restructure files from")
    structure_parser.add_argument("target_root", help="Target root directory for restructured files")
    
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system drives using smartctl and lsblk")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        cli_scan(args.directory)
    elif args.command == "rename":
        cli_rename(args.directory)
    elif args.command == "archive":
        cli_archive(args.directory, args.archive_root)
    elif args.command == "structure":
        cli_structure(args.directory, args.target_root)
    elif args.command == "monitor":
        cli_monitor()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

