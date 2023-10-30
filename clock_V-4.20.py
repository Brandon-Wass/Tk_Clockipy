#!/usr/bin/env python3

import time
import math
import datetime
import tkinter as tk
import tkinter.colorchooser as colorchooser
import tkinter.simpledialog as simpledialog
import RPi.GPIO as GPIO

class PopupMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=0)
        self.parent = parent

        # Adding a submenu for color options
        self.clock = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Analog Clock Colors", menu=self.clock)
        self.clock.add_command(label="Seconds Hand", command=self.seconds_hand_colors)
        self.clock.add_command(label="Minutes Hand", command=self.minutes_hand_colors)
        self.clock.add_command(label="Hours Hand", command=self.hours_hand_colors)
        self.clock.add_command(label="Clock Border", command=self.change_border_color)
        self.clock.add_command(label="Background", command=self.change_bg_color)
        self.clock.add_command(label="Markings", command=self.change_markings_color)
        self.clock.add_command(label="Clock Numbers", command=self.change_numbers_color)
        self.add_separator()
        self.digital = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Digital Clock Colors", menu=self.digital)
        self.digital.add_command(label="Day of Week", command=self.change_dtdow_color)
        self.digital.add_command(label="Date", command=self.change_dtdat_color)
        self.digital.add_command(label="Time", command=self.change_dttim_color)
        self.add_separator()
        self.hour = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Hour Button Colors", menu=self.hour)
        self.hour.add_command(label="Text", command=self.change_hour_button_fg_color)
        self.hour.add_command(label="Border", command=self.change_hour_button_brdr_color)
        self.minute = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Minute Button Colors", menu=self.minute)
        self.minute.add_command(label="Text", command=self.change_minute_button_fg_color)
        self.minute.add_command(label="Border", command=self.change_minute_button_brdr_color)
        self.add_separator()
        self.alarm = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Alarm Display Colors", menu=self.alarm)
        self.alarm.add_command(label="Text", command=self.change_alarm_display_fg_color)
        self.add_separator()
        self.gpio = tk.Menu(self, tearoff=0)
        self.add_cascade(label="GPIO Pin", menu=self.gpio)
        self.gpio.add_command(label="Change GPIO Pin", command=self.change_gpio_pin)
        self.add_separator()
        self.snooze = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Snooze Time", menu=self.snooze)
        self.snooze.add_command(label="Change Snooze Time", command=self.change_snooze_time)
        self.add_separator()
        self.add_command(label="Close Menu", command=self.close_menu)
        self.add_command(label="Exit Program", command=self.exit_program)

    def seconds_hand_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.second_color = color
        self.parent.focus_set()

    def minutes_hand_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_color = color
        self.parent.focus_set()

    def hours_hand_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_color = color
        self.parent.focus_set()

    def change_border_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.border_color = color
        self.parent.focus_set()

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.bg_color = color
            self.parent.canvas.config(bg=self.parent.bg_color)
            self.parent.hour_button.config(bg=self.parent.bg_color)
            self.parent.minute_button.config(bg=self.parent.bg_color)
            self.parent.alarm_display.config(bg=self.parent.bg_color)
        self.parent.focus_set()

    def change_markings_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.markings_color = color
        self.parent.focus_set()

    def change_numbers_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.numbers_color = color
        self.parent.focus_set()

    def change_dtdow_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.dtdow_color = color
        self.parent.focus_set()

    def change_dtdat_color(self):     
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.dtdat_color = color
        self.parent.focus_set()

    def change_dttim_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.dttim_color = color
        self.parent.focus_set()

    def change_hour_button_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(fg=color)
        self.parent.focus_set()

    def change_hour_button_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(highlightbackground=color)
        self.parent.focus_set()

    def change_minute_button_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(fg=color)
        self.parent.focus_set()

    def change_minute_button_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(highlightbackground=color)
        self.parent.focus_set()

    def change_alarm_display_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.alarm_display.config(fg=color)
        self.parent.focus_set()

    def change_gpio_pin(self):
        gpio_pin = simpledialog.askinteger("GPIO Pin", "Enter a new GPIO pin number:")
        if gpio_pin:
            self.parent.change_gpio_pin(gpio_pin=int)

    def change_snooze_time(self):
        time = simpledialog.askinteger("Snooze Time", "Enter the snooze time in minutes:", parent=self.parent)
        if time:
            self.parent.snooze_time = time
        self.parent.focus_set()

    def close_menu(self):
        self.unpost()
        self.parent.focus_set()

    def exit_program(self):
        GPIO.output(self.parent.gpio_pin, GPIO.LOW)
        GPIO.cleanup()
        self.parent.destroy()

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()

        # Colors for different aspects
        self.second_color = "purple"
        self.minute_color = "purple"
        self.hour_color = "purple"
        self.border_color = "purple"
        self.bg_color = "black"
        self.markings_color = "purple"
        self.numbers_color = "purple"
        self.alarm_display_fg_color = "purple"
        self.hour_button_fg_color = "purple"
        self.minute_button_fg_color = "purple"
        self.hour_button_brdr_color = "purple"
        self.minute_button_brdr_color = "purple"
        self.dtdow_color = "purple"
        self.dtdat_color = "purple"
        self.dttim_color = "purple"
        self.gpio_pin = 20
        self.snooze_time = 5

        self.attributes('-fullscreen', True)
        self.update_idletasks()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.title("Clock")
        self.overrideredirect(1)
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, bg='black', highlightthickness=0, cursor="none")
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.canvas.bind("<Button-1>", self.show_menu)

        self.popup_menu = PopupMenu(self)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.LOW)

        self.alarm_time = None
        self.alarm_triggered = False

        self.alarm_display = tk.Label(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg=self.bg_color, fg=self.alarm_display_fg_color,
                                       activebackground=self.bg_color, activeforeground=self.alarm_display_fg_color, width=5, height=1)
        self.alarm_display.place(x=self.screen_width / 2, y=(self.screen_height / 2) + 50, anchor="n")
        self.alarm_display.bind("<Button-1>", self.destroy_alarm)

        self.button_press_time_hour = None
        self.scheduled_event_hour = None
        self.button_press_time_minute = None
        self.scheduled_event_minute = None
        
        self.hour_button = tk.Button(self.canvas, text="Set Hour", font=('Arial', 20, 'bold'), 
                             fg=self.hour_button_fg_color, bg=self.bg_color, activebackground=self.bg_color, activeforeground=self.hour_button_fg_color, 
                             width=8, height=4, highlightbackground=self.hour_button_brdr_color, relief=tk.FLAT)
        self.hour_button.place(x=0, y=self.screen_height, anchor="sw")
        self.hour_button.bind("<Button-1>", self.start_hour_increment)
        self.hour_button.bind("<ButtonRelease-1>", self.stop_hour_increment)

        self.minute_button = tk.Button(self.canvas, text="Set Minute", font=('Arial', 20, 'bold'), 
                               fg=self.minute_button_fg_color, bg=self.bg_color, activebackground=self.bg_color, activeforeground=self.minute_button_fg_color, 
                               width=8, height=4, highlightbackground=self.minute_button_brdr_color, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=self.screen_height, anchor="se")
        self.minute_button.bind("<Button-1>", self.start_minute_increment)
        self.minute_button.bind("<ButtonRelease-1>", self.stop_minute_increment)

        # Set the window icon
        self.icon_image = tk.PhotoImage(file='clockipy.png')
        self.iconphoto(False, self.icon_image)

        self.update_clock()

    # Define a method to update the clock
    def update_clock(self):
        self.canvas.delete("all")

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill=self.bg_color, outline=self.border_color)

        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=self.bg_color, outline=self.border_color)

        self.draw_marks()
        self.draw_numbers()
        self.draw_date_and_time()

        current_time = time.localtime(time.time())
        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time .tm_sec/10.0)
        hour_angle = math.radians((current_time.tm_hour % 12) * 30 - 90 + current_time.tm_min/2.0)

        second_hand_length = radius - 30
        minute_hand_length = radius - 60
        hour_hand_length = radius - 90

        second_x, second_y = center_x + second_hand_length * math.cos(second_angle), center_y + second_hand_length * math.sin(second_angle)
        minute_x, minute_y = center_x + minute_hand_length * math.cos(minute_angle), center_y + minute_hand_length * math.sin(minute_angle)
        hour_x, hour_y = center_x + hour_hand_length * math.cos(hour_angle), center_y + hour_hand_length * math.sin(hour_angle)

        self.canvas.create_line(center_x, center_y, second_x, second_y, fill=self.second_color, width=2)
        self.canvas.create_line(center_x, center_y, minute_x, minute_y, fill=self.minute_color, width=6)
        self.canvas.create_line(center_x, center_y, hour_x, hour_y, fill=self.hour_color, width=8)

        self.check_alarm(current_time)
        self.update_id = self.after(10, self.update_clock)

    def draw_marks(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 55

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
        radius = min(center_x, center_y) - 80

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            coord = (center_x + (radius - 30) * math.cos(angle), center_y + (radius - 30) * math.sin(angle))
            self.canvas.create_text(coord[0], coord[1], text=str(i), font=('Arial', int(radius/10), 'bold'), fill=self.numbers_color)

    def draw_date_and_time(self):
        now = datetime.datetime.now()
        day_of_week = now.strftime('%A')
        date = now.strftime('%d %B %Y')
        time_str = now.strftime('%H:%M:%S')
        padding = 10
        self.canvas.create_text(padding, padding, text=day_of_week, anchor='nw', font=('Arial', 20), fill=self.dtdow_color)
        self.canvas.create_text(padding, padding + 30, text=date, anchor='nw', font=('Arial', 20), fill=self.dtdat_color)
        self.canvas.create_text(padding, padding + 60, text=time_str, anchor='nw', font=('Arial', 20), fill=self.dttim_color)

    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

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
        def snooze_alarm():
            GPIO.output(self.gpio_pin, GPIO.LOW)
            self.delete_alarm()
            self.alarm_time[1] = (self.alarm_time[1] + self.snooze_time) % 60
            self.update_alarm_display()
            self.popup.destroy()
            self.focus_set()
        self.popup = tk.Toplevel(self, bg="black", cursor="none")  # Create a Toplevel window
        self.popup.overrideredirect(True)  # This will make the window frameless
        self.popup.geometry("250x200+{}+{}".format(self.screen_width//2-100, self.screen_height//2-50))  # Adjust the size and position as required

        label = tk.Label(self.popup, text="Stop the alarm?\nSnooze the alarm?\nReset the alarm?", font=('Arial', 20, 'bold'), bg="black", fg="purple")
        label.grid(row=0, column=0, columnspan=3, pady=(10, 20))  # Span across 3 columns

        red_button = tk.Button(self.popup, text="STOP", bg="red", command=stop_alarm, width=5) # Create a button to stop the alarm
        red_button.grid(row=1, column=0, sticky=tk.W, padx=10)  # Place button on bottom-left

        pink_button = tk.Button(self.popup, text="SNOOZE", bg="pink", command=snooze_alarm, width=5)
        pink_button.grid(row=1, column=1)  # Place button on bottom-middle

        yellow_button = tk.Button(self.popup, text="RESET", bg="yellow", command=reset_alarm, width=5) # Create a button to reset the alarm
        yellow_button.grid(row=1, column=2, sticky=tk.E, padx=10)  # Place button on bottom-right

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

    def change_gpio_pin(self, gpio_pin):
        GPIO.cleanup()  # Clean the previous GPIO setup
        GPIO.setup(self.gpio_pin, GPIO.OUT)  # Set the new pin as an output
        GPIO.output(self.gpio_pin, GPIO.LOW)  # Ensure the pin starts off LOW

# Run the program
if __name__ == "__main__":  # If the program is run directly
    app = Clock()   # Create an instance of the Clock class
    app.mainloop()  # Run the app

# Path: clock_V-4.20.py
