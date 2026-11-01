
import socket
import threading
import sentinel
from checkpoint import load_state

HOST = "127.0.0.1"
NEXT_PORT = 5002
SERVICE_PORT = 5000

# Function to start the backup sentinel
def start_backup():

    # Waits for a promotion signal from the monitor
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as control:

        control.bind((HOST, NEXT_PORT))
        control.settimeout(1)

        print("Backup Sentinel is running in standby mode...")

        while True:
            try:
                message, address = control.recvfrom(1024)
            except socket.timeout:
                continue

            if message != b"PROMOTE":
                continue

            print("Promotion signal received!")

            # Loads the saved blacklist
            try:
                blocked_ips = load_state()

            except (OSError, ValueError) as error:
                print(f"Failed to load checkpoint: {error}")
                continue

            # Tries to take over the original Sentinel port
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:

                try:
                    server.bind((HOST, SERVICE_PORT))

                except OSError:
                    print("Cannot promote: Primary is still running")
                    continue

                # Restores the saved blacklist
                sentinel.BLACKLISTED_IPS = blocked_ips

                print("Backup promoted to primary!")
                print("Restored blacklist:", blocked_ips)

                # Starts sending heartbeats
                heartbeat_thread = threading.Thread(
                    target=sentinel.send_heartbeat,
                    daemon=True
                )
                heartbeat_thread.start()

                # Starts processing requests
                sentinel.receive_message(server)
                # Exits the backup when the service stops
                return

if __name__ == "__main__":

    try:
        start_backup()
    except KeyboardInterrupt:
        print("Backup stopped by user")
