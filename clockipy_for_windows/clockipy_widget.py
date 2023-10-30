import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import time
import os
import winsound
from datetime import datetime, timedelta
import json

def find_alarm_file():
    for root, dirs, files in os.walk('/'):
        for file in files:
            if file.endswith('alarm.wav'):
                return os.path.join(root, file)
    raise FileNotFoundError("alarm.wav file not found")

def change_alarm_sound():
    global alarm_file_path
    filepath = filedialog.askopenfilename(title="Select a Sound File", filetypes=[("Sound files", "*.wav")])
    if filepath:
        alarm_file_path = filepath
        save_settings()

def submit_alarm():
    alarm_time = entry_var.get().replace(".", ":")
    if alarm_time:
        try:
            time.strptime(alarm_time, '%H:%M:%S')
            alarm_listbox.insert(tk.END, alarm_time)
            alarm_times.append(alarm_time)
            entry_var.set('')
            save_settings()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM:SS or HH.MM.SS format.")

def delete_alarm(event):
    selected_index = alarm_listbox.curselection()
    if selected_index:
        selected_time = alarm_times[selected_index[0]]
        
        # If the alarm for the selected time is playing, stop it
        if selected_time in alarms_playing:
            alarms_playing.remove(selected_time)
            stop_alarm()

        alarm_listbox.delete(selected_index)
        del alarm_times[selected_index[0]]
        save_settings()

def stop_alarm():
    winsound.PlaySound(None, winsound.SND_ASYNC)
    alarms_playing.clear()

def snooze_alarm():
    stop_alarm()
    now = datetime.now()
    snooze_duration = int(snooze_var.get())
    snooze_time = (now + timedelta(minutes=snooze_duration)).strftime('%H:%M:%S')
    alarm_times.append(snooze_time)
    alarm_listbox.insert(tk.END, snooze_time)
    save_settings()

def check_alarms():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=current_time)
    
    for alarm_time in alarm_times:
        if current_time == alarm_time and alarm_time not in alarms_playing:
            alarms_playing.add(alarm_time)
            winsound.PlaySound(alarm_file_path, winsound.SND_ASYNC | winsound.SND_LOOP)
            
    root.after(10, check_alarms)

def set_focus(event=None):
    entry.focus_set()

def set_snooze_duration(value):
    snooze_var.set(value)
    save_settings()

SETTINGS_FILE = "alarm_settings.json"

def save_settings():
    settings_data = {
        "alarm_file_path": alarm_file_path,
        "snooze_duration": snooze_var.get(),
        "alarms": alarm_times
    }
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings_data, file)

def load_settings():
    global alarm_file_path
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            settings_data = json.load(file)
            alarm_file_path = settings_data.get("alarm_file_path", find_alarm_file())
            snooze_var.set(settings_data.get("snooze_duration", "5"))
            alarm_times.extend(settings_data.get("alarms", []))
            
            # Populate the alarm_listbox with the loaded alarm times
            for alarm_time in alarm_times:
                alarm_listbox.insert(tk.END, alarm_time)

alarm_file_path = find_alarm_file()

root = tk.Tk()
root.title('Alarm Clock')
root.resizable(False, False)
root.geometry('250x350')

# Make sure columns and rows expand
root.grid_columnconfigure(0, weight=1)  # first column
root.grid_columnconfigure(1, weight=1)  # second column
root.grid_columnconfigure(2, weight=1)  # third column
for i in range(4):  # for 4 rows
    root.grid_rowconfigure(i, weight=1)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the main Settings menu
settings_menu = tk.Menu(menu_bar, tearoff=0)

# Add the main Settings menu to the menu_bar
menu_bar.add_cascade(label="Settings", menu=settings_menu)

# Snooze Settings menu
snooze_menu = tk.Menu(settings_menu, tearoff=0)  # Here, the parent of snooze_menu is settings_menu
snooze_var = tk.StringVar(root)
snooze_var.set("5")  # default value
snooze_options = ["1", "5", "10", "15", "20", "25", "30", "60"]
for option in snooze_options:
    snooze_menu.add_radiobutton(label=f"{option} minutes", variable=snooze_var, value=option, command=lambda value=option: set_snooze_duration(value))
settings_menu.add_cascade(label="Snooze Settings", menu=snooze_menu)  # Add the snooze_menu to the settings_menu

# Sound Settings menu
sound_menu = tk.Menu(settings_menu, tearoff=0)  # Here, the parent of sound_menu is settings_menu
sound_menu.add_command(label="Change Alarm Sound", command=change_alarm_sound)
settings_menu.add_cascade(label="Sound Settings", menu=sound_menu)  # Add the sound_menu to the settings_menu

time_label = tk.Label(root, text="", font=('freesansbold.ttf', 20))
time_label.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=10, padx=10)

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=('freesansbold.ttf', 14), width=8)
entry.grid(row=1, column=0, pady=10, padx=10)

submit_button = tk.Button(root, text="Submit", command=submit_alarm, font=('freesansbold.ttf', 8))
submit_button.grid(row=1, column=1, pady=10, padx=10)

alarm_listbox = tk.Listbox(root, font=('freesansbold.ttf', 8))
alarm_listbox.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=10, padx=10)
alarm_listbox.bind("<Double-Button-1>", delete_alarm)

stop_button = tk.Button(root, text="Stop Alarm", command=stop_alarm, font=('freesansbold.ttf', 8), bg='red', fg='white')
stop_button.grid(row=3, column=0, pady=10, padx=10)

snooze_button = tk.Button(root, text="Snooze", command=snooze_alarm, font=('freesansbold.ttf', 8), bg='blue', fg='white')
snooze_button.grid(row=3, column=1, pady=10, padx=10)

print(os.path.abspath(SETTINGS_FILE))

alarms_playing = set()
alarm_times = []

load_settings()

root.bind('<Return>', lambda event=None: submit_alarm())
root.bind('<FocusIn>', set_focus)

root.after(10, check_alarms)

root.mainloop()
