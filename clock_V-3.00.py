#!/usr/bin/env python3 

import time
import math
import datetime
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.colorchooser as colorchooser
import tkinter.filedialog as filedialog

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
        self.clock.add_command(label="Center Dot", command=self.change_bg_color)
        self.clock.add_command(label="Markings", command=self.change_markings_color)
        self.clock.add_command(label="Clock Numbers", command=self.change_numbers_color)
        self.add_separator()
        self.background = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Background Image", menu=self.background)
        self.background.add_command(label="Select Image", command=self.parent.select_image)
        self.background.add_command(label="Clear Image", command=self.parent.clear_image)
        self.add_separator()
        self.add_command(label="Close Menu", command=self.close_menu) 
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
            self.parent.update_clock()  # Force a redraw after changing the background color

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

        # Loading the image at initialization
        self.bg_image_path = "image.png"  # Assuming the image is in the same directory as the script
        self.bg_image = Image.open(self.bg_image_path)
        self.bg_image = self.bg_image.resize((self.screen_width, self.screen_height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.canvas.bind("<Button-1>", self.show_menu)

        self.popup_menu = PopupMenu(self)

        self.update_clock()

    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def select_image(self):
        self.image_path = tk.filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image = self.image.resize((self.screen_width, self.screen_height), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(self.image)
            self.update_clock()

    def clear_image(self):
        if hasattr(self, 'image'):
            del self.image
        self.update_clock()

    def draw_background(self):
        if hasattr(self, 'image') and self.image:  # check if self.image exists and is not None
            self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.image)
        else:
            self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.bg_image)
        
        # Always draw the clock circle regardless of the background image
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline=self.border_color)

    def update_clock(self):
        self.canvas.delete("all")
        
        self.draw_background()
        self.draw_date_and_time() 
        self.draw_marks()
        self.draw_numbers()

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        current_time = time.localtime(time.time())
        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time .tm_sec/10.0)
        hour_angle = math.radians((current_time.tm_hour % 12) * 30 - 90 + current_time.tm_min/2.0)

        second_hand_length = radius - 10
        minute_hand_length = radius - 30
        hour_hand_length = radius - 50

        second_x, second_y = center_x + second_hand_length * math.cos(second_angle), center_y + second_hand_length * math.sin(second_angle)
        minute_x, minute_y = center_x + minute_hand_length * math.cos(minute_angle), center_y + minute_hand_length * math.sin(minute_angle)
        hour_x, hour_y = center_x + hour_hand_length * math.cos(hour_angle), center_y + hour_hand_length * math.sin(hour_angle)

        self.canvas.create_line(center_x, center_y, second_x, second_y, fill=self.second_color, width=2)
        self.canvas.create_line(center_x, center_y, minute_x, minute_y, fill=self.minute_color, width=6)
        self.canvas.create_line(center_x, center_y, hour_x, hour_y, fill=self.hour_color, width=8)

        # Circle in the middle of the clock to cover the intersections of the hands
        self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill=self.bg_color, outline=self.border_color)

        self.after(1000, self.update_clock)

    def draw_marks(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        # Marks for every minute
        for i in range(60):
            angle = math.radians(i * 6 - 90)  # 6 degrees for each minute
            if i % 5 == 0:  # Marks for every hour, since there are 5 minutes between hours
                start_x, start_y = center_x + (radius - 20) * math.cos(angle), center_y + (radius - 20) * math.sin(angle)
                end_x, end_y = center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=self.markings_color, width=4)
            else:  # Marks for minutes
                start_x, start_y = center_x + (radius - 10) * math.cos(angle), center_y + (radius - 10) * math.sin(angle)
                end_x, end_y = center_x + (radius - 5) * math.cos(angle), center_y + (radius - 5) * math.sin(angle)
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=self.markings_color, width=2)

    def draw_numbers(self):
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x, y = center_x + (radius - 30) * math.cos(angle), center_y + (radius - 30) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=('Arial', 24), fill=self.numbers_color)

    def draw_date_and_time(self):
        now = datetime.datetime.now()
        day_of_week = now.strftime('%A')
        date = now.strftime('%d %B %Y')
        time_str = now.strftime('%H:%M:%S')
        padding = 10
        self.canvas.create_text(padding, padding, text=day_of_week, anchor='nw', font=('Arial', 20), fill=self.numbers_color)
        self.canvas.create_text(padding, padding + 30, text=date, anchor='nw', font=('Arial', 20), fill=self.numbers_color)
        self.canvas.create_text(padding, padding + 60, text=time_str, anchor='nw', font=('Arial', 20), fill=self.numbers_color)

if __name__ == "__main__":
    Clock().mainloop()

