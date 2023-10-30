import time
from gpiozero import LED
from datetime import datetime
import threading

# Ask the user for the GPIO pin number
while True:
    try:
        buzzer_pin = int(input("Enter the GPIO pin number for the buzzer: "))
        buzzer = LED(buzzer_pin)
        break
    except ValueError:
        print("Please enter a valid integer for the GPIO pin number.")
    except Exception as e:
        print(f"Error initializing GPIO: {e}. Please check your setup.")
        exit()

alarm_active = False

def alarm():
    global alarm_active
    print("Wake up!")
    alarm_active = True
    while alarm_active:
        try:
            buzzer.on()  # Activate the buzzer
            time.sleep(0.1)
            buzzer.off()
            time.sleep(0.1)
        except Exception as e:
            print(f"Error toggling the buzzer: {e}. Exiting alarm function.")
            alarm_active = False

def check_input():
    global alarm_active
    while True:
        try:
            user_input = input("Type 'stop' to stop the alarm: ")
            if user_input.lower() == 'stop':
                alarm_active = False
                break
        except KeyboardInterrupt:
            print("\nAlarm stopped by user interruption.")
            alarm_active = False

def get_current_time_str():
    return datetime.now().strftime("%H:%M:%S")

while True:
    try:
        # Get the next alarm time
        print(f"\nCurrent time: {get_current_time_str()}")  # Print current time before input prompts
        hour_input = input("What hour do you want the alarm to ring? (0-23) ")
        minute_input = input("What minute do you want the alarm to ring? (0-59) ")
        second_input = input("What second do you want the alarm to ring? (0-59) ")

        hour = int(hour_input) if hour_input.isdigit() else -1
        minute = int(minute_input) if minute_input.isdigit() else -1
        second = int(second_input) if second_input.isdigit() else -1

        if not (0 <= hour <= 23) or not (0 <= minute <= 59) or not (0 <= second <= 59):
            print("Invalid input. Please enter valid values for hour, minute, and second.")
            continue

    except ValueError:
        print("Please enter valid integer values for hour, minute, and second.")
        continue
    
    while True:
        try:
            if hour == datetime.now().hour and minute == datetime.now().minute and second == datetime.now().second:
                threading.Thread(target=alarm).start()
                check_input()
                time.sleep(0.01)  # To prevent continuous alarms in that second
                break
        except Exception as e:
            print(f"Error encountered: {e}")
            break
