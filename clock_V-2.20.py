#!/usr/bin/env python3

import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.colorchooser as colorchooser
import tkinter.simpledialog as simpledialog
import RPi.GPIO as GPIO
import time
import math
import subprocess
import threading

class PopupMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=0)
        self.parent = parent

        # Adding a submenu for color options
        self.clock = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Clock Colors", menu=self.clock)
        self.clock.add_command(label="Seconds Hand", command=self.seconds_hand_colors)
        self.clock.add_command(label="Minutes Hand", command=self.minutes_hand_colors)
        self.clock.add_command(label="Hours Hand", command=self.hours_hand_colors)
        self.clock.add_command(label="Clock Border", command=self.change_border_color)
        self.clock.add_command(label="Background", command=self.change_bg_color)
        self.clock.add_command(label="Markings", command=self.change_markings_color)
        self.clock.add_command(label="Clock Numbers", command=self.change_numbers_color)
        self.hour = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Hour Button Colors", menu=self.hour)
        self.hour.add_command(label="Background", command=self.change_hour_button_bg_color)
        self.hour.add_command(label="Text", command=self.change_hour_button_fg_color)
        self.hour.add_command(label="Border", command=self.change_hour_button_brdr_color)
        self.minute = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Minute Button Colors", menu=self.minute)
        self.minute.add_command(label="Background", command=self.change_minute_button_bg_color)
        self.minute.add_command(label="Text", command=self.change_minute_button_fg_color)
        self.minute.add_command(label="Border", command=self.change_minute_button_brdr_color)
        self.alarm = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Alarm Display Colors", menu=self.alarm)
        self.alarm.add_command(label="Background", command=self.change_alarm_display_bg_color)
        self.alarm.add_command(label="Text", command=self.change_alarm_display_fg_color)
        self.alarm.add_command(label="Border", command=self.change_alarm_display_brdr_color)
        self.gpio = tk.Menu(self, tearoff=1)
        self.add_cascade(label="GPIO Pin", menu=self.gpio)
        self.gpio.add_command(label="Change GPIO Pin", command=self.change_gpio_pin)

        self.add_separator()
        self.add_command(label="Close Menu", command=self.close_menu) # added line
        self.add_command(label="Exit Program", command=self.exit_program)

    def seconds_hand_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.second_color = color

    def minutes_hand_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_color = color

    def hours_hand_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_color = color

    def change_border_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.border_color = color

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.bg_color = color
            self.parent.canvas.config(bg=self.parent.bg_color)

    def change_markings_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.markings_color = color

    def change_numbers_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.numbers_color = color

    def change_gpio_pin(self):
        pin = simpledialog.askinteger("GPIO Pin", "Enter a new GPIO pin number:")
        if pin:
            self.parent.change_gpio_pin(pin)

    def close_menu(self):
        self.unpost()

    def exit_program(self):
        GPIO.output(20, GPIO.LOW)
        GPIO.cleanup()
        self.parent.destroy()

    def change_hour_button_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(bg=color)

    def change_hour_button_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(fg=color)

    def change_hour_button_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(highlightbackground=color)

    def change_minute_button_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(bg=color)

    def change_minute_button_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(fg=color)

    def change_minute_button_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(highlightbackground=color)

    def change_alarm_display_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.alarm_display.config(bg=color)

    def change_alarm_display_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.alarm_display.config(fg=color)

    def change_alarm_display_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.alarm_display.config(highlightbackground=color)

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.gpio_pin = 20
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.LOW)

        # Colors for different aspects
        self.second_color = "purple"
        self.minute_color = "purple"
        self.hour_color = "purple"
        self.border_color = "purple"
        self.bg_color = "black"
        self.markings_color = "purple"
        self.numbers_color = "purple"
        self.alarm_display_bg_color = "black"
        self.alarm_display_fg_color = "purple"
        self.alarm_display_brdr_color = "black"
        self.hour_button_bg_color = "black"
        self.hour_button_fg_color = "purple"
        self.minute_button_bg_color = "black"
        self.minute_button_fg_color = "purple"
        self.hour_button_brdr_color = "purple"
        self.minute_button_brdr_color = "purple"

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

        self.canvas.bind("<Button-1>", self.show_menu)

        self.popup_menu = PopupMenu(self)

        self.audio_file = 'alarm.wav'  # Default audio file
        self.sound_playing = False
        self.alarm_time = None
        self.sound_process = None
        self.alarm_triggered = False

        self.alarm_display = tk.Button(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg=self.alarm_display_bg_color, fg=self.alarm_display_fg_color,
                                       activebackground=self.alarm_display_bg_color, activeforeground=self.alarm_display_fg_color, highlightbackground=self.alarm_display_brdr_color, width=3, height=1, relief=tk.FLAT)
        self.alarm_display.place(x=self.screen_width / 2, y=(self.screen_height / 2) + 50, anchor="n")
        self.alarm_display.bind("<Button-1>", self.destroy_alarm)

        self.button_press_time_hour = None
        self.scheduled_event_hour = None
        self.button_press_time_minute = None
        self.scheduled_event_minute = None
        
        self.hour_button = tk.Button(self.canvas, text="Set Hour", 
                             fg=self.hour_button_fg_color, bg=self.hour_button_bg_color, activebackground=self.hour_button_bg_color, activeforeground=self.hour_button_fg_color, 
                             width=10, height=5, highlightbackground=self.hour_button_brdr_color, relief=tk.FLAT)
        self.hour_button.place(x=0, y=self.screen_height, anchor="sw")
        self.hour_button.bind("<Button-1>", self.start_hour_increment)
        self.hour_button.bind("<ButtonRelease-1>", self.stop_hour_increment)

        self.minute_button = tk.Button(self.canvas, text="Set Minute",
                               fg=self.minute_button_fg_color, bg=self.minute_button_bg_color, activebackground=self.minute_button_bg_color, activeforeground=self.minute_button_fg_color, 
                               width=10, height=5, highlightbackground=self.minute_button_brdr_color, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=self.screen_height, anchor="se")
        self.minute_button.bind("<Button-1>", self.start_minute_increment)
        self.minute_button.bind("<ButtonRelease-1>", self.stop_minute_increment)

        self.update_clock()

    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def change_gpio_pin(self, pin):
        GPIO.cleanup()  # Clean the previous GPIO setup
        GPIO.setup(pin, GPIO.OUT)  # Set the new pin as an output
        GPIO.output(pin, GPIO.LOW)  # Ensure the pin starts off LOW
        self.gpio_pin = pin  # Update the GPIO pin number in the class instance

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

    def draw_marks(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                start = (center_x + (radius - 15) * math.cos(angle), center_y + (radius - 15) * math.sin(angle))
                end = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
                self.canvas.create_line(start[0], start[1], end[0], end[1], width=6, fill=self.markings_color)
            else:
                start = (center_x + (radius - 5) * math.cos(angle), center_y + (radius - 5) * math.sin(angle))
                end = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
                self.canvas.create_line(start[0], start[1], end[0], end[1], width=3, fill=self.markings_color)

    def draw_numbers(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            coord = (center_x + (radius - 30) * math.cos(angle), center_y + (radius - 30) * math.sin(angle))
            self.canvas.create_text(coord[0], coord[1], text=str(i), font=('Arial', int(radius/10), 'bold'), fill=self.numbers_color)

    # Define a method to update the clock
    def update_clock(self):
        self.canvas.delete("all")

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=self.bg_color, outline=self.border_color)

        self.draw_marks()
        self.draw_numbers()

        current_time = time.localtime(time.time())

        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time.tm_sec * 0.1)
        hour_angle = math.radians(current_time.tm_hour * 30 - 90 + current_time.tm_min * 0.5)

        second_coords = (center_x + radius * math.cos(second_angle), center_y + radius * math.sin(second_angle))
        minute_coords = (center_x + (radius - 30) * math.cos(minute_angle), center_y + (radius - 30) * math.sin(minute_angle))
        hour_coords = (center_x + (radius - 60) * math.cos(hour_angle), center_y + (radius - 60) * math.sin(hour_angle))

        self.draw_hand(second_coords, self.second_color, int(radius/50))
        self.draw_hand(minute_coords, self.minute_color, int(radius/35))
        self.draw_hand(hour_coords, self.hour_color, int(radius/25))

        self.check_alarm(current_time)
        self.update_id = self.after(10, self.update_clock)

    # Define the methods to set the alarm
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

    def check_alarm(self, current_time):
        if self.alarm_time:
            if (current_time.tm_hour == self.alarm_time[0] and current_time.tm_min == self.alarm_time[1]
                    and current_time.tm_sec == 0 and not self.alarm_triggered):
                self.alarm_triggered = True
                self.show_alarm_popup()

    def destroy_alarm(self, event):
        self.alarm_time = None
        self.alarm_triggered = False
        self.alarm_display.config(text="--:--")

    def delete_alarm(self):
        self.alarm_triggered = False

    def show_alarm_popup(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        # Define a method to stop the sound and close the Toplevel window
        def stop_alarm():   # index: 0 - hour, 1 - minute
            GPIO.output(self.gpio_pin, GPIO.LOW)
            self.delete_alarm()
            self.popup.destroy()  # Close the Toplevel window
            self.focus_set()    # Set the focus to the main window
        # Define a method to reset the alarm, stop the sound, and close the Toplevel window
        def reset_alarm():  # index: 0 - hour, 1 - minute
            GPIO.output(self.gpio_pin, GPIO.LOW)
            self.delete_alarm()
            self.alarm_time = None  # Reset the alarm time
            self.update_alarm_display() # Call the update_alarm_display() method
            self.popup.destroy()  # Close the Toplevel window
            self.focus_set()    # Set the focus to the main window
        self.popup = tk.Toplevel(self, bg="black", cursor="none")  # Create a Toplevel window
        self.popup.overrideredirect(True)  # This will make the window frameless
        self.popup.geometry("250x150+{}+{}".format(self.screen_width//2-100, self.screen_height//2-50))  # Adjust the size and position as required
        label = tk.Label(self.popup, text="Stop the alarm?\nor\nReset the alarm?", font=('Arial', 20, 'bold'), bg="black", fg="purple")
        label.pack()
        red_button = tk.Button(self.popup, text="STOP", bg="red", command=stop_alarm) # Create a button to stop the alarm
        red_button.pack(side=tk.LEFT)   # Pack the button
        yellow_button = tk.Button(self.popup, text="RESET", bg="yellow", command=reset_alarm) # Create a button to reset the alarm
        yellow_button.pack(side=tk.RIGHT)   # Pack the button

# Run the program
if __name__ == "__main__":  # If the program is run directly
    app = Clock()   # Create an instance of the Clock class
    app.mainloop()  # Run the app
