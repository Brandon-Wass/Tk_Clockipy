#!/usr/bin/env python3

import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import math
import tkinter.messagebox as messagebox
import subprocess
import threading

class Clock(tk.Tk):

    def __init__(self):
        super().__init__()

        # Set window to fullscreen
        self.attributes('-fullscreen', True)
        
        # Wait for window to update and get screen dimensions
        self.update_idletasks()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.title("Clock")
        self.overrideredirect(1)  # Frameless window
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, bg='black', highlightthickness=0, cursor="none")
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # Draw static elements (like clock circle, marks, numbers)
        self.draw_static_elements()

        # Close the program by clicking anywhere on the window
        self.canvas.bind("<Button-1>", lambda e: self.destroy())

        # Initial alarm time to None (no alarm)
        self.alarm_time = None

        self.update_clock()

    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(20, GPIO.LOW)  # Make sure the pin is low when the program starts

    # Separate static elements drawing
    def draw_static_elements(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        # Draw the clock circle
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="black", outline="purple")
        
        # Draw static marks and numbers
        self.draw_marks()
        self.draw_numbers()

        # Buttons and initial alarm display
        self.draw_alarm_display_and_buttons()

    def draw_alarm_display_and_buttons(self):
        # Display for alarm time
        self.alarm_display = tk.Label(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg="black", fg="purple")
        self.alarm_display.place(x=self.screen_width - 364, y=300, anchor="e")

        # Buttons for setting the alarm
        self.hour_button = tk.Button(self.canvas, text="Set Hour", command=self.set_alarm_hour, 
                             fg="purple", bg="black", activebackground="black", activeforeground="purple", 
                             width=10, height=5, highlightbackground="purple", bd=4, relief=tk.FLAT)
        self.hour_button.place(x=self.screen_width - 686, y=430, anchor="e")

        self.minute_button = tk.Button(self.canvas, text="Set Minute", command=self.set_alarm_minute, 
                               fg="purple", bg="black", activebackground="black", activeforeground="purple", 
                               width=10, height=5, highlightbackground="purple", bd=4, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=430, anchor="e")

    def update_clock(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        current_time = time.localtime(time.time())

        # Calculate angles for each hand
        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time.tm_sec * 0.1)
        hour_angle = math.radians(current_time.tm_hour * 30 - 90 + current_time.tm_min * 0.5)

        second_coords = (center_x + radius * math.cos(second_angle), center_y + radius * math.sin(second_angle))
        minute_coords = (center_x + (radius - 30) * math.cos(minute_angle), center_y + (radius - 30) * math.sin(minute_angle))
        hour_coords = (center_x + (radius - 60) * math.cos(hour_angle), center_y + (radius - 60) * math.sin(hour_angle))

        # Delete and re-draw hands
        self.canvas.delete("hand")  # We tag the hands with "hand" to delete them specifically
        self.draw_hand(second_coords, "purple", int(radius/100), "hand")
        self.draw_hand(minute_coords, "purple", int(radius/66), "hand")
        self.draw_hand(hour_coords, "purple", int(radius/33), "hand")

        self.check_alarm(current_time)
        self.update_id = self.after(1000, self.update_clock)  # Update every 1 second for better performance

    def draw_hand(self, coord, color, width, tag=None):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        self.canvas.create_line(center_x, center_y, coord[0], coord[1], fill=color, width=width, tags=tag)

    def draw_marks(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:  # Hour marks
                start = (center_x + (radius - 15) * math.cos(angle), center_y + (radius - 15) * math.sin(angle))
                end = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
                self.canvas.create_line(start[0], start[1], end[0], end[1], width=6, fill="purple")
            else:  # Second marks
                start = (center_x + (radius - 5) * math.cos(angle), center_y + (radius - 5) * math.sin(angle))
                end = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
                self.canvas.create_line(start[0], start[1], end[0], end[1], width=3, fill="purple")

    def draw_numbers(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            coord = (center_x + (radius - 30) * math.cos(angle), center_y + (radius - 30) * math.sin(angle))
            self.canvas.create_text(coord[0], coord[1], text=str(i), font=('Arial', int(radius/10), 'bold'), fill="purple")

    def set_alarm_hour(self):
        if self.alarm_time is None:
            self.alarm_time = [0, 0]
        
        self.alarm_time[0] = (self.alarm_time[0] + 1) % 24
        self.update_alarm_display()

    def set_alarm_minute(self):
        if self.alarm_time is None:
            self.alarm_time = [0, 0]

        self.alarm_time[1] = (self.alarm_time[1] + 1) % 60
        self.update_alarm_display()

    def update_alarm_display(self):
        if self.alarm_time:
            self.alarm_display.config(text=f"{self.alarm_time[0]:02}:{self.alarm_time[1]:02}")
        else:
            self.alarm_display.config(text="--:--")

    def check_alarm(self, current_time):
        if self.alarm_time:
            if (current_time.tm_hour == self.alarm_time[0] and current_time.tm_min == self.alarm_time[1] and current_time.tm_sec == 0):
                self.alarm_rings()

    def play_sound(self):
        self.sound_process = subprocess.Popen(['aplay', './alarm.wav'])  # Ensure 'alarm.wav' is in the current directory or provide an absolute path

    def stop_sound(self):
        if self.sound_process and self.sound_process.poll() is None:  # Check if process is still running
            self.sound_process.terminate()
        self.alarm_time = None  # delete the alarm
        self.update_alarm_display()  # update the display

    def alarm_rings(self):
        sound_thread = threading.Thread(target=self.play_sound)
        sound_thread.start()
        print("Alarm rings!")
        response = messagebox.showinfo("Alarm", "Time's up!")
        self.stop_sound()

    def cleanup_on_exit(self):
        self.after_cancel(self.update_id)
        self.destroy()  # destroy the window

if __name__ == "__main__":
    app = Clock()
    app.protocol("WM_DELETE_WINDOW", app.cleanup_on_exit)
    app.mainloop()
