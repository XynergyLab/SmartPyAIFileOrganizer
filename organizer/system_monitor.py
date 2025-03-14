# system_monitor.py
import subprocess
import logging
import re

logging.basicConfig(level=logging.DEBUG)

def get_lsblk_info():
    """
    Call lsblk to list block devices.
    """
    try:
        result = subprocess.run(["lsblk", "-o", "NAME,TYPE,MOUNTPOINT"], stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except Exception as e:
        logging.error("Error getting lsblk info: %s", e)
        return ""

def check_smartctl(device):
    """
    Run smartctl on a device and return its stdout and stderr.
    """
    try:
        result = subprocess.run(["smartctl", "-a", device],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        return result.stdout, result.stderr
    except Exception as e:
        logging.error("Error running smartctl on %s: %s", device, e)
        return "", str(e)

def parse_smart_errors(smart_output):
    """
    Parse smartctl output for SMART errors.
    """
    errors = []
    pattern = re.compile(r"Error sending ATA command CHECK POWER MODE")
    for line in smart_output.splitlines():
        if pattern.search(line):
            errors.append(line)
    return errors

def monitor_drives():
    lsblk_output = get_lsblk_info()
    logging.info("lsblk output:\n%s", lsblk_output)
    devices = []
    # A basic parser assuming /dev/sdX devices; for a production system,
    # parse lsblk output properly.
    for line in lsblk_output.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "disk":
            devices.append("/dev/" + parts[0])
    logging.info("Found devices: %s", devices)
    
    for dev in devices:
        logging.info("Checking SMART data for device %s", dev)
        stdout, stderr = check_smartctl(dev)
        if stderr:
            logging.warning("smartctl stderr for %s: %s", dev, stderr)
        errors = parse_smart_errors(stdout)
        if errors:
            logging.error("SMART errors found for %s: %s", dev, errors)
        else:
            logging.info("No SMART errors found for %s", dev)

if __name__ == "__main__":
    monitor_drives()

