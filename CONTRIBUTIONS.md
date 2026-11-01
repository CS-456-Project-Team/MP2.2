# CS456 - Mini Group Project 1: Resilient Security Systems

## Redundancy model

### Contributions:

**Victor Troncoso "troncosv"**: 
* checkpoint.py : Implemented functions to save and load the Sentinel's blacklist, preserving its state after a crash.
* backup.py : Implemented a standby Sentinel that restores the saved blacklist and takes over the primary's operations when promoted.
* sentinel.py : Updated the original Sentinel to support checkpoint saving while maintaining its existing firewall, heartbeat functionality, and simulated delay. 
* monitor.py : Updated the code to detect when the sentinel crashes and automatically send a promotion signal to the backup.
  
**Benjamin Mooneyham "Moonshammy"**:

**Matthew Leman "Philojyw"**:

**Tyler Short "Tsyber"**: 
* adversary.py : Implemented attacks 1 and 2 to simulate both a heartbeat delay and a corrupted checkpoint

