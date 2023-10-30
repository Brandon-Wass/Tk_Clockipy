import time
from datetime import datetime

while True:
    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\rCurrent time: {current_time}", end='', flush=True)  # Use '\r' to overwrite the line
        time.sleep(0.01)  # Update time every 1/100th of a second
    except Exception as e:
        print(f"Error encountered while printing time: {e}")

