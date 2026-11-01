import logging
import socket
from datetime import datetime
import time
from pathlib import Path

HOST = '127.0.0.1'
PORT = 5001
TIMEOUT = 3 #Timeout duration in seconds for considering the service down
BACKUP_PORT = 5002
PROMOTION_RETRY = 1
LOG_FILE = Path(__file__).with_name("monitor.log")

logging.basicConfig(
    filename="LOG_FILE",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Function to receive heartbeat messages from a service and monitor its status
def receive_heartbeat():
    monitor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    monitor.settimeout(0.5) #extended wait time for network latency
    # Bind the monitor socket to the specified host and port
    monitor.bind((HOST, PORT))
    last_heartbeat = None
    service_down = False #Flag to indicate if the service is down
    last_promotion = 0
    
    try:
        print("Heartbeat monitor online")
        
        while True:
            try:
                message = monitor.recv(1024)
                # Checks if the received message is empty
                if not message:
                    print(f"[{datetime.now()}] Received empty message")
                    break
                # Checks if the received message is a heartbeat
                if message == b"HEARTBEAT":
                    last_heartbeat = time.monotonic()
                    print(f"[{datetime.now()}] Received heartbeat message: {message}")
                    # Checks if the service was previously down and has now recovered
                    if service_down:
                        print(f"[{datetime.now()}] [Service Restored] Heartbeats resumed")
                        logging.info("[Service Restored] Heartbeats resumed")
                        service_down = False
            # Handles socket timeout exceptions
            except socket.timeout:
                pass
            
            # Checks whether the last heartbeat was too long ago
            if last_heartbeat is not None and not service_down:
                # Checks if the last heartbeat was too long ago
                if time.monotonic() - last_heartbeat >= TIMEOUT:
                    print(f"[{datetime.now()}] [Crash Detected] Sentinel is down!")
                    logging.error("[Crash Detected] Sentinel is down")
                    # Automatically tell the backup to take over
                    monitor.sendto(b"PROMOTE", (HOST, BACKUP_PORT))
                    last_promotion = time.monotonic()
                    print(f"[{datetime.now()}] [Failover Triggered] Promotion signal sent")
                    logging.warning("[Failover Triggered] Promotion signal sent")
                    # Marks the service as down
                    service_down = True
            
            now = time.monotonic()
            if service_down and now - last_promotion >= PROMOTION_RETRY:
                monitor.sendto(b"PROMOTE", (HOST, BACKUP_PORT))
                last_promotion = now
    
    except socket.error as e:
        print("Server unexpectedly closed")
        
    except KeyboardInterrupt:
        print("Monitor stopped by user")
    
    finally:
        monitor.close()
        
        
if __name__ == "__main__":
    receive_heartbeat()
