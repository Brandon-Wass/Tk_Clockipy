#!/usr/bin/env python3

import time
import math
import datetime
from PIL import Image as PILImage
from PIL import ImageTk
import tkinter as tk
import tkinter.colorchooser as colorchooser
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import subprocess
import threading

class PopupMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=0)
        self.parent = parent

        # Adding a submenu for color options
        self.analog = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Analog Clock Colors", menu=self.analog)
        self.analog.add_command(label="Seconds Hand", command=self.seconds_hand_colors)
        self.analog.add_command(label="Minutes Hand", command=self.minutes_hand_colors)
        self.analog.add_command(label="Hours Hand", command=self.hours_hand_colors)
        self.analog.add_command(label="Clock Border", command=self.change_border_color)
        self.analog.add_command(label="Center Dot", command=self.change_bg_color)
        self.analog.add_command(label="Markings", command=self.change_markings_color)
        self.analog.add_command(label="Clock Numbers", command=self.change_numbers_color)
        self.add_separator()
        self.hour = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Hour Button Colors", menu=self.hour)
        self.hour.add_command(label="Background", command=self.change_hour_button_bg_color)
        self.hour.add_command(label="Text", command=self.change_hour_button_fg_color)
        self.hour.add_command(label="Border", command=self.change_hour_button_brdr_color)
        self.minute = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Minute Button Colors", menu=self.minute)
        self.minute.add_command(label="Background", command=self.change_minute_button_bg_color)
        self.minute.add_command(label="Text", command=self.change_minute_button_fg_color)
        self.minute.add_command(label="Border", command=self.change_minute_button_brdr_color)
        self.alarm = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Alarm Display Colors", menu=self.alarm)
        self.alarm.add_command(label="Background", command=self.change_alarm_display_bg_color)
        self.alarm.add_command(label="Text", command=self.change_alarm_display_fg_color)
        self.add_separator()
        self.audio = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Audio File", menu=self.audio)
        self.audio.add_command(label="Change Audio File", command=self.change_audio_file)
        self.add_separator()
        self.snooze = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Snooze Time", menu=self.snooze)
        self.snooze.add_command(label="Custom Snooze Time", command=self.custom_snooze_time)
        self.add_separator()
        self.digital = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Digital Clock Colors", menu=self.digital)
        self.digital.add_command(label="Day of Week", command=self.change_dtdow_color)
        self.digital.add_command(label="Date", command=self.change_dtdat_color)
        self.digital.add_command(label="Time", command=self.change_dttim_color)
        self.add_separator()
        self.background = tk.Menu(self, tearoff=1)
        self.add_cascade(label="Background Image", menu=self.background)
        self.background.add_command(label="Select Image", command=self.parent.select_image)
        self.background.add_command(label="Clear Image", command=self.parent.clear_image)
        self.add_separator()
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

    def change_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav"), ("All Files", "*.*")])
        if file_path:
            self.parent.audio_file = file_path

    def change_dtdow_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.dtdow_color = color

    def change_dtdat_color(self):     
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.dtdat_color = color

    def change_dttim_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.dttim_color = color
            
    def exit_program(self):
        # Define a method to stop the sound and close the Toplevel window
        def stop_alarm():
            self.parent.stop_sound()
        stop_alarm()
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

    def custom_snooze_time(self):
        time = simpledialog.askinteger("Snooze Time", "Enter the snooze time in minutes:", parent=self.parent)
        if time:
            self.parent.snooze_time = time
    
    

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
        self.alarm_display_bg_color = "black"
        self.alarm_display_fg_color = "purple"
        self.hour_button_bg_color = "black"
        self.hour_button_fg_color = "purple"
        self.minute_button_bg_color = "black"
        self.minute_button_fg_color = "purple"
        self.hour_button_brdr_color = "purple"
        self.minute_button_brdr_color = "purple"
        self.dtdow_color = "purple"
        self.dtdat_color = "purple"
        self.dttim_color = "purple"
        self.snooze_time = 5

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
        self.bg_image = PILImage.open(self.bg_image_path)
        self.bg_image = self.bg_image.resize((self.screen_width, self.screen_height), 3)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        self.canvas.bind("<Button-1>", self.show_menu)

        self.popup_menu = PopupMenu(self)

        self.audio_file = 'alarm.wav'  # Default audio file
        self.sound_playing = False
        self.alarm_time = None
        self.sound_process = None
        self.alarm_triggered = False

        self.alarm_display = tk.Label(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg=self.alarm_display_bg_color, fg=self.alarm_display_fg_color,
                                       activebackground=self.alarm_display_bg_color, activeforeground=self.alarm_display_fg_color, width=5, height=1)
        self.alarm_display.place(x=self.screen_width / 2, y=(self.screen_height / 2) + 50, anchor="n")
        self.alarm_display.bind("<Button-1>", self.destroy_alarm)

        self.button_press_time_hour = None
        self.scheduled_event_hour = None
        self.button_press_time_minute = None
        self.scheduled_event_minute = None
        
        self.hour_button = tk.Button(self.canvas, text="Set Hour", font=('Arial', 20, 'bold'), 
                             fg=self.hour_button_fg_color, bg=self.hour_button_bg_color, activebackground=self.hour_button_bg_color, activeforeground=self.hour_button_fg_color, 
                             width=8, height=4, highlightbackground=self.hour_button_brdr_color, relief=tk.FLAT)
        self.hour_button.place(x=0, y=self.screen_height, anchor="sw")
        self.hour_button.bind("<Button-1>", self.start_hour_increment)
        self.hour_button.bind("<ButtonRelease-1>", self.stop_hour_increment)

        self.minute_button = tk.Button(self.canvas, text="Set Minute", font=('Arial', 20, 'bold'), 
                               fg=self.minute_button_fg_color, bg=self.minute_button_bg_color, activebackground=self.minute_button_bg_color, activeforeground=self.minute_button_fg_color, 
                               width=8, height=4, highlightbackground=self.minute_button_brdr_color, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=self.screen_height, anchor="se")
        self.minute_button.bind("<Button-1>", self.start_minute_increment)
        self.minute_button.bind("<ButtonRelease-1>", self.stop_minute_increment)

        self.update_clock()

    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def select_image(self):
        self.image_path = tk.filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*")])
        if self.image_path:
            self.image = PILImage.open(self.image_path)
            self.image = self.image.resize((self.screen_width, self.screen_height), 3)
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
        self.canvas.create_text(padding, padding, text=day_of_week, anchor='nw', font=('Arial', 20), fill=self.dtdow_color)
        self.canvas.create_text(padding, padding + 30, text=date, anchor='nw', font=('Arial', 20), fill=self.dtdat_color)
        self.canvas.create_text(padding, padding + 60, text=time_str, anchor='nw', font=('Arial', 20), fill=self.dttim_color)

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

    def play_sound(self):
        self.sound_playing = True
        while self.sound_playing:
            self.sound_process = subprocess.Popen(['aplay', self.audio_file])
            self.sound_process.wait()

    def stop_sound(self):
        self.sound_playing = False
        if self.sound_process and self.sound_process.poll() is None:
            self.sound_process.terminate()

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
        sound_thread = threading.Thread(target=self.play_sound)
        sound_thread.start()
        # Define a method to stop the sound and close the Toplevel window
        def stop_alarm():   # index: 0 - hour, 1 - minute
            self.stop_sound()
            self.delete_alarm()
            self.popup.destroy()  # Close the Toplevel window
            self.focus_set()    # Set the focus to the main window
        # Define a method to reset the alarm, stop the sound, and close the Toplevel window
        def reset_alarm():  # index: 0 - hour, 1 - minute
            self.stop_sound()
            self.delete_alarm()
            self.alarm_time = None  # Reset the alarm time
            self.update_alarm_display() # Call the update_alarm_display() method
            self.popup.destroy()  # Close the Toplevel window
            self.focus_set()    # Set the focus to the main window
        def snooze_alarm():
            self.stop_sound()
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

# Run the program
if __name__ == "__main__":  # If the program is run directly
    app = Clock()   # Create an instance of the Clock class
    app.mainloop()  # Run the app


# Path: clock_V-3.11.py