#!/usr/bin/env python3

import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import math
import tkinter.messagebox as messagebox

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()

        self.attributes('-fullscreen', True)
        
        self.update_idletasks()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.title("Clock")
        self.overrideredirect(1)
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, bg='black', highlightthickness=0, cursor="none")
        self.canvas.pack(fill=tk.BOTH, expand=1)

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        self.canvas.bind("<Button-1>", lambda e: self.destroy())

        self.alarm_time = None
        self.alarm_triggered = False

        self.alarm_display = tk.Label(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg="black", fg="white")
        self.alarm_display.place(x=self.screen_width / 2, y=(self.screen_height / 2) + 50, anchor="n")

        self.button_press_time_hour = None
        self.scheduled_event_hour = None
        self.button_press_time_minute = None
        self.scheduled_event_minute = None
        
        self.hour_button = tk.Button(self.canvas, text="Set Hour", 
                             fg="black", bg="white", activebackground="white", activeforeground="black", 
                             width=10, height=5, highlightbackground="black", bd=4, relief=tk.FLAT)
        self.hour_button.place(x=0, y=self.screen_height, anchor="sw")
        self.hour_button.bind("<Button-1>", self.start_hour_increment)
        self.hour_button.bind("<ButtonRelease-1>", self.stop_hour_increment)

        self.minute_button = tk.Button(self.canvas, text="Set Minute",
                               fg="black", bg="white", activebackground="white", activeforeground="black", 
                               width=10, height=5, highlightbackground="black", bd=4, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=self.screen_height, anchor="se")
        self.minute_button.bind("<Button-1>", self.start_minute_increment)
        self.minute_button.bind("<ButtonRelease-1>", self.stop_minute_increment)

        self.update_clock()

    # Define a method to increment the alarm time
    def increment_alarm_time(self, index):
        if self.alarm_time is None:
            self.alarm_time = [0, 0]
        
        if index == 0:  # Hour
            self.alarm_time[0] = (self.alarm_time[0] + 1) % 24
        elif index == 1:  # Minute
            self.alarm_time[1] = (self.alarm_time[1] + 1) % 60

        self.update_alarm_display()

    # Define methods to handle rapid button presses
    def rapid_increment_hour(self):
        if not self.button_press_time_hour:
            return
        self.increment_alarm_time(0)
        self.scheduled_event_hour = self.after(200, self.rapid_increment_hour)
    
    def rapid_increment_minute(self):
        if not self.button_press_time_minute:
            return
        self.increment_alarm_time(1)
        self.scheduled_event_minute = self.after(200, self.rapid_increment_minute)
        
    # Define methods to handle button presses and releases
    def start_hour_increment(self, event):
        self.button_press_time_hour = time.time()
        self.after(2000, self.rapid_increment_hour)
    
    def stop_hour_increment(self, event):
        if time.time() - self.button_press_time_hour < 2:
            self.increment_alarm_time(0)
        self.button_press_time_hour = None
        if self.scheduled_event_hour:
            self.after_cancel(self.scheduled_event_hour)
            self.scheduled_event_hour = None
    
    def start_minute_increment(self, event):
        self.button_press_time_minute = time.time()
        self.after(2000, self.rapid_increment_minute)
    
    def stop_minute_increment(self, event):
        if time.time() - self.button_press_time_minute < 2:
            self.increment_alarm_time(1)
        self.button_press_time_minute = None
        if self.scheduled_event_minute:
            self.after_cancel(self.scheduled_event_minute)
            self.scheduled_event_minute = None

    # Define a method to draw a hand
    def draw_hand(self, coord, color, width):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        self.canvas.create_line(center_x, center_y, coord[0], coord[1], fill=color, width=width)

    # Define a method to draw the marks
    def draw_marks(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:  # Hour marks
                start = (center_x + (radius - 15) * math.cos(angle), center_y + (radius - 15) * math.sin(angle))
                end = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
                self.canvas.create_line(start[0], start[1], end[0], end[1], width=6, fill="white")
            else:  # Second marks
                start = (center_x + (radius - 5) * math.cos(angle), center_y + (radius - 5) * math.sin(angle))
                end = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
                self.canvas.create_line(start[0], start[1], end[0], end[1], width=3, fill="white")

    # Define a method to draw the numbers
    def draw_numbers(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            coord = (center_x + (radius - 30) * math.cos(angle), center_y + (radius - 30) * math.sin(angle))
            self.canvas.create_text(coord[0], coord[1], text=str(i), font=('Arial', int(radius/10), 'bold'), fill="white")

    # Define a method to update the clock
    def update_clock(self):
        self.canvas.delete("all")

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="black", outline="white")

        self.draw_marks()
        self.draw_numbers()

        current_time = time.localtime(time.time())

        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time.tm_sec * 0.1)
        hour_angle = math.radians(current_time.tm_hour * 30 - 90 + current_time.tm_min * 0.5)

        second_coords = (center_x + radius * math.cos(second_angle), center_y + radius * math.sin(second_angle))
        minute_coords = (center_x + (radius - 30) * math.cos(minute_angle), center_y + (radius - 30) * math.sin(minute_angle))
        hour_coords = (center_x + (radius - 60) * math.cos(hour_angle), center_y + (radius - 60) * math.sin(hour_angle))

        self.draw_hand(second_coords, "red", int(radius/50))
        self.draw_hand(minute_coords, "blue", int(radius/35))
        self.draw_hand(hour_coords, "green", int(radius/25))

        self.check_alarm(current_time)
        self.update_id = self.after(10, self.update_clock)

    # Define the methods to set the alarm time
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

    # Define a method to update the alarm display
    def update_alarm_display(self):
        if self.alarm_time:
            self.alarm_display.config(text=f"{self.alarm_time[0]:02}:{self.alarm_time[1]:02}")
        else:
            self.alarm_display.config(text="--:--")

    # Define a method to check if the alarm should ring
    def check_alarm(self, current_time):
        if self.alarm_time:
            if (current_time.tm_hour == self.alarm_time[0] and current_time.tm_min == self.alarm_time[1] and current_time.tm_sec == 0 and not self.alarm_triggered):
                self.alarm_rings()
                self.alarm_triggered = True
            elif (current_time.tm_min != self.alarm_time[1]):
                self.alarm_triggered = False

    # Define a method to ring the alarm
    def alarm_rings(self):
        alarm_window = tk.Toplevel(self)
        alarm_window.title("Alarm")

        alarm_window_width = 150
        alarm_window_height = 100
        alarm_window.geometry(f"{alarm_window_width}x{alarm_window_height}")

        x_position = (self.screen_width - alarm_window_width) // 2
        y_position = (self.screen_height - alarm_window_height) // 2
        alarm_window.geometry(f"+{x_position}+{y_position}")

        msg_label = tk.Label(alarm_window, text="Stop the alarm?\nor\nReset the alarm?")
        msg_label.pack(pady=2)

        # Define a method to stop the sound and close the Toplevel window
        def stop_alarm():
            alarm_window.destroy()
            self.focus_set()

        red_button = tk.Button(alarm_window, text="STOP", bg="red", command=stop_alarm)
        red_button.pack(side=tk.LEFT, padx=1)

        # Define a method to reset the alarm, stop the sound, and close the Toplevel window
        def reset_alarm():
            self.alarm_time = None
            self.update_alarm_display()
            alarm_window.destroy()
            self.focus_set()

        yellow_button = tk.Button(alarm_window, text="RESET", bg="yellow", command=reset_alarm)
        yellow_button.pack(side=tk.RIGHT, padx=1)

# Run the program
if __name__ == "__main__":
    app = Clock()
    app.mainloop()
