#!/usr/bin/python3

# Import necessary libraries
import pygame
import time
import os
# import RPi.GPIO as GPIO

# Function to find the alarm.wav file
def find_alarm_file():
    for root, dirs, files in os.walk('/'):
        for file in files:
            if file.endswith('alarm.wav'):
                return os.path.join(root, file)
    raise FileNotFoundError("alarm.wav file not found")

# Set the GPIO button pin
# button_pin = 23

# Initialize GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to stop the active alarm
def stop_alarm(channel):
    alarm_sound.stop()
    alarms_playing.clear()
#     GPIO.remove_event_detect(button_pin)

# Set up button event handler
# GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=stop_alarm, bouncetime=200)

# Initialize Pygame
pygame.init()

# Set display and font
display_width = 200
display_height = 600
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Alarm Clock')
font_size = 50
font = pygame.font.SysFont('freesansbold.ttf', font_size)
stop_font = pygame.font.SysFont('freesansbold.ttf', 24)
delete_font = pygame.font.SysFont('freesansbold.ttf', 16)

# Set loop variables
submit_text = font.render('Submit', True, (255, 0, 255))
stop_surface = stop_font.render('Stop', True, (255, 0, 0))
delete_surface = delete_font.render('Delete', True, (255, 0, 0))
alarm_file_path = find_alarm_file()
alarm_sound = pygame.mixer.Sound(alarm_file_path)
alarm_sound.set_volume(1)
border_color = (255, 0, 255)
done = False
alarms_playing = {}  # use a dictionary to keep track of which alarms are playing
alarm_times = []
clock = pygame.time.Clock()

# Input field variables
input_pos = (display_width // 2, display_height // 2 - 250)
input_width = 160
input_height = 40
input_rect = pygame.Rect(input_pos[0] - input_width // 2, input_pos[1] - input_height // 2, input_width, input_height)
input_text = ''
input_active = True

# Submit button variables
submit_pos = (display_width // 2, display_height // 2 - 210)
submit_width = 100
submit_height = 50

# Alarm time display variables
alarm_pos = (display_width // 2 - 30, display_height // 2 - 170)
alarm_texts = []

# Stop button variables
stop_pos_template = (submit_pos[0] + 30, submit_pos[1] + 40)  # separate stop buttons for each alarm
stop_size = (submit_width // 2 - 15, submit_height // 2 - 10)  # set the stop button size to half the submit button size

# Delete button variables
delete_pos_template = (submit_pos[0] - submit_width // 2 + 79, submit_pos[1] + 55)  # separate delete buttons for each alarm
delete_size = stop_size  # set the delete button size to the stop button size

# Main Loop
while not done:
    # Clear screen
    game_display.fill((0,0,0))
    
    # Get current time
    current_time = time.strftime("%H:%M:%S")
    
    # Check if any alarm times are reached
    for alarm_time in alarm_times:
        if current_time == alarm_time and alarm_time not in alarms_playing:
            alarms_playing[alarm_time] = True
            alarm_sound.play(loops=-1)
            
    # Display current time
    time_display = font.render(current_time, True, (255,0,255))
    game_display.blit(time_display, (30, 0))
    
    # Display input field
    input_surface = font.render(input_text, True, (255,0,255))
    game_display.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.draw.rect(game_display, border_color, input_rect, 2) # Draw a border around the input field
    
    # Display submit button
    submit_rect = submit_text.get_rect(center=submit_pos)
    game_display.blit(submit_text, submit_rect)
    pygame.draw.rect(game_display, border_color, submit_rect, 2) # Draw a border around the submit button
    
    # Display alarm times
    alarm_texts.clear()
    for i, alarm_time in enumerate(alarm_times):
        alarm_text = font.render(alarm_time, True, (255,0,255))
        alarm_rect = alarm_text.get_rect(center=(alarm_pos[0], alarm_pos[1] + i*40))
        alarm_texts.append(alarm_text)
        game_display.blit(alarm_text, alarm_rect)
        pygame.draw.rect(game_display, border_color, alarm_rect, 2) # Draw a border around the alarm display
        # Display stop button for this alarm
        stop_pos = (stop_pos_template[0] + submit_width // 2, stop_pos_template[1] - 10 + i*40)
        stop_rect = stop_surface.get_rect(center=stop_pos, size=stop_size)
        stop_border_rect = pygame.Rect(stop_rect.x - 2, stop_rect.y - 2, stop_rect.width + 4, stop_rect.height + 4)
        game_display.blit(stop_surface, stop_rect)
        pygame.draw.rect(game_display, border_color, stop_border_rect, 2) # Draw a border around the stop button
        # Display delete button for this alarm
        delete_pos = (delete_pos_template[0] + submit_width // 2, delete_pos_template[1] - 10 + i*40)
        delete_rect = delete_surface.get_rect(center=delete_pos, size=delete_size)
        delete_border_rect = pygame.Rect(delete_rect.x - 2, delete_rect.y - 2, delete_rect.width + 4, delete_rect.height + 4)
        game_display.blit(delete_surface, delete_rect)
        pygame.draw.rect(game_display, border_color, delete_border_rect, 2) # Draw a border around the delete button
        # Check if stop or delete button is clicked
        if pygame.mouse.get_pressed()[0]:
            if stop_rect.collidepoint(pygame.mouse.get_pos()) and alarm_time in alarms_playing:
                alarms_playing.pop(alarm_time)
                alarm_sound.stop()
            elif delete_rect.collidepoint(pygame.mouse.get_pos()):
                alarm_times.remove(alarm_time)
                alarm_texts.pop(i)  #

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if submit button was clicked
            if submit_rect.collidepoint(event.pos):
                alarm_times.append(input_text)
                input_text = ''
            # Check if input field was clicked
            elif input_rect.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    alarm_times.append(input_text)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
                    
    # Update display
    pygame.display.update()
    clock.tick(16)
    
# Quit Pygame
pygame.quit() 
