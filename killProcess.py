import os
import signal
PID = 34012
try:
    os.kill(PID, signal.SIGTERM)
    print(f"Process {PID} sent SIGTERM signal for graceful termination.")
except OSError as e:
    print(f"Error terminating process {PID}: {e}")