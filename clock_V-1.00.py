#!/usr/bin/env python3

import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import math

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

        # Bind left click event on the canvas
        self.canvas.bind("<Button-1>", self.close_app)

        # Compute radius directly in the __init__ method
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

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

        self.update_id = self.after(10, self.update_clock)  # Update every 1 second

    def close_app(self, event=None):
        self.after_cancel(self.update_id)
        self.destroy()

if __name__ == "__main__":
    app = Clock()
    app.mainloop()