#!/usr/bin/env python3

import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import math
import tkinter.messagebox as messagebox

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

        # Compute radius directly in the __init__ method
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        # Close the program by clicking anywhere on the window
        self.canvas.bind("<Button-1>", lambda e: self.destroy())

        # Initialize alarm variables
        self.alarm_time = None
        self.sound_process = None
        self.alarm_triggered = False

        # Display for alarm time
        self.alarm_display = tk.Label(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg="black", fg="white")
        self.alarm_display.place(x=self.screen_width / 2, y=(self.screen_height / 2) + 50, anchor="n")

        # Buttons for setting the alarm
        self.hour_button = tk.Button(self.canvas, text="Set Hour", command=self.set_alarm_hour, 
                             fg="black", bg="white", activebackground="white", activeforeground="black", 
                             width=10, height=5, highlightbackground="black", bd=4, relief=tk.FLAT)
        self.hour_button.place(x=0, y=self.screen_height, anchor="sw")

        self.minute_button = tk.Button(self.canvas, text="Set Minute", command=self.set_alarm_minute, 
                               fg="black", bg="white", activebackground="white", activeforeground="black", 
                               width=10, height=5, highlightbackground="black", bd=4, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=self.screen_height, anchor="se")

        self.update_clock()

    def draw_hand(self, coord, color, width):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        self.canvas.create_line(center_x, center_y, coord[0], coord[1], fill=color, width=width)

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

    def draw_numbers(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            coord = (center_x + (radius - 30) * math.cos(angle), center_y + (radius - 30) * math.sin(angle))
            self.canvas.create_text(coord[0], coord[1], text=str(i), font=('Arial', int(radius/10), 'bold'), fill="white")

    def update_clock(self):
        self.canvas.delete("all")

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        # Draw the clock circle
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="black", outline="white")

        self.draw_marks()
        self.draw_numbers()

        current_time = time.localtime(time.time())

        # Calculate angles for each hand
        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time.tm_sec * 0.1)
        hour_angle = math.radians(current_time.tm_hour * 30 - 90 + current_time.tm_min * 0.5)

        second_coords = (center_x + radius * math.cos(second_angle), center_y + radius * math.sin(second_angle))
        minute_coords = (center_x + (radius - 30) * math.cos(minute_angle), center_y + (radius - 30) * math.sin(minute_angle))
        hour_coords = (center_x + (radius - 60) * math.cos(hour_angle), center_y + (radius - 60) * math.sin(hour_angle))

        # Draw hands
        self.draw_hand(second_coords, "red", int(radius/50))
        self.draw_hand(minute_coords, "blue", int(radius/35))
        self.draw_hand(hour_coords, "green", int(radius/25))

        self.check_alarm(current_time)
        self.update_id = self.after(10, self.update_clock)  # Update every 1 second

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
            if (current_time.tm_hour == self.alarm_time[0] and current_time.tm_min == self.alarm_time[1] and current_time.tm_sec == 0 and not self.alarm_triggered):
                self.alarm_rings()
                self.alarm_triggered = True
            elif (current_time.tm_min != self.alarm_time[1]):  # Reset the flag once we're past the alarm minute
                self.alarm_triggered = False

    def alarm_rings(self):
        # This will set the GPIO pin to high when the alarm rings
        GPIO.output(20, GPIO.HIGH)

        # Create a Toplevel window for the alarm notification
        alarm_window = tk.Toplevel(self)
        alarm_window.title("Alarm")

        # Set the size of the alarm window
        alarm_window_width = 150
        alarm_window_height = 100
        alarm_window.geometry(f"{alarm_window_width}x{alarm_window_height}")

        # Center the alarm_window
        x_position = (self.screen_width - alarm_window_width) // 2
        y_position = (self.screen_height - alarm_window_height) // 2
        alarm_window.geometry(f"+{x_position}+{y_position}")

        # Display a message asking if the user wants to stop the alarm or reset it
        msg_label = tk.Label(alarm_window, text="Stop the alarm?\nor\nReset the alarm?")
        msg_label.pack(pady=2)

        # Define a method to stop the sound and close the Toplevel window
        def stop_alarm():
            GPIO.output(20, GPIO.LOW)  # Set the GPIO pin to low when the dialog popup is closed
            alarm_window.destroy()
            self.focus_set()  # Bring main window back into focus

        # Define a method to reset the alarm, stop the sound, and close the Toplevel window
        def reset_alarm():
            self.alarm_time = None
            self.update_alarm_display()
            GPIO.output(20, GPIO.LOW)  # Set the GPIO pin to low when the dialog popup is closed
            alarm_window.destroy()
            self.focus_set()

        # Green button to just stop the sound
        green_button = tk.Button(alarm_window, text="RESET", bg="green", command=reset_alarm)
        green_button.pack(side=tk.RIGHT, padx=1)

        # Red button to delete the previously set alarm and stop the sound
        red_button = tk.Button(alarm_window, text="STOP", bg="red", command=stop_alarm)
        red_button.pack(side=tk.LEFT, padx=1)

if __name__ == "__main__":
    app = Clock()
    app.mainloop()
