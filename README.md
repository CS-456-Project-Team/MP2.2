# MP1.2
## Running the Project

The project just requires Python 3. No additional libraries are needed.

### 1. Normal Operation and Failure Detection

Open three separate terminals:

**Terminal 1 - Start the Monitor**
```powershell
python .\monitor.py
```

**Terminal 2 - Start the Backup**
```powershell
python .\backup.py
```

**Terminal 3 - Start the Sentinel**
```powershell
python .\sentinel.py
```

The Sentinel sends heartbeats every second and randomly crashes after 20 - 40 seconds. The monitor detects the failure after approximately 3 seconds without a heartbeat.

### 2. Attack 1 - Heartbeat Delay

For this test, start the programs in the following order:

**Terminal 1 - Start the Monitor**
```powershell
python .\monitor.py
```

**Terminal 2 - Start the Backup**
```powershell
python .\backup.py
```

**Terminal 3 - Start the Sentinel**
```powershell
python .\sentinel.py
```

**Terminal 4 - Start Delay Attack**
```powershell
python .\adversary.py delay
```

With the 3 prior systems running, the delay attack in Terminal 4 sends a pause request every 30 seconds, and each request pauses heartbeats for 7 seconds.


### 3. Attack 2 - Checkpoint Tampering

For this test, run this command: 

```powershell
python .\adversary.py tamper
```

This will alter the JSON file containing blacklisted IPs. After this the programs will be initialized in normal order, but any outside messages can be blocked or unblocked by an attacker with this access.