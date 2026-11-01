import json
from pathlib import Path


CHECKPOINT = Path(__file__).with_name("checkpoint.json")
# Function to save the sentinel's blacklist
def save_state(blocked_ips):
    temp_file = CHECKPOINT.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(blocked_ips, file)

    temp_file.replace(CHECKPOINT)

# Function to load the sentinel's blacklist
def load_state():
    with CHECKPOINT.open("r", encoding="utf-8") as file:
        blocked_ips = json.load(file)

    if not isinstance(blocked_ips, list):
        raise ValueError("Checkpoint must contain a list")

    if not all(isinstance(ip, str) for ip in blocked_ips):
        raise ValueError("Checkpoint entries must be strings")

    return blocked_ips

