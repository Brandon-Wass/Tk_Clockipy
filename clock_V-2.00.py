#!/usr/bin/env python3 

import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import tkinter.colorchooser as colorchooser
import time
import math

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

    def close_menu(self):
        self.unpost()

    def exit_program(self):
        self.parent.destroy()

class Clock(tk.Tk): 
    def __init__(self): 
        super().__init__()

        # Colors for different aspects
        self.second_color = "red"
        self.minute_color = "blue"
        self.hour_color = "green"
        self.border_color = "white"
        self.bg_color = "black"
        self.markings_color = "white"
        self.numbers_color = "white"

        self.attributes('-fullscreen', True)
        self.update_idletasks()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.title("Clock")
        self.overrideredirect(1)
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, bg=self.bg_color, highlightthickness=0, cursor="none")
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.canvas.bind("<Button-1>", self.show_menu)

        self.popup_menu = PopupMenu(self)

        self.update_clock()

    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

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

        self.update_id = self.after(10, self.update_clock)

if __name__ == "__main__":
    app = Clock()
    app.mainloop()
