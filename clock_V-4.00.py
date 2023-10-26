#!/usr/bin/env python3

import time
import math
import datetime
import tkinter as tk
import tkinter.colorchooser as colorchooser

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
        self.digital = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Digital Clock Colors", menu=self.digital)
        self.digital.add_command(label="Day of Week", command=self.change_dtdow_color)
        self.digital.add_command(label="Date", command=self.change_dtdat_color)
        self.digital.add_command(label="Time", command=self.change_dttim_color)
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

    def close_menu(self):
        self.unpost()
        self.parent.focus_set()

    def exit_program(self):
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
        self.dtdow_color = "purple"
        self.dtdat_color = "purple"
        self.dttim_color = "purple"

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

        self.button_press_time_hour = None
        self.scheduled_event_hour = None
        self.button_press_time_minute = None
        self.scheduled_event_minute = None

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

# Run the program
if __name__ == "__main__":  # If the program is run directly
    app = Clock()   # Create an instance of the Clock class
    app.mainloop()  # Run the app

# Path: clock_V-4.00.py