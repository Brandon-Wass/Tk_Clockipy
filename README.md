# Alarm_Clock

This is a Python script for an Alarm Clock program using Pygame library. The program allows users to input multiple alarm times, displays the current time, and plays alarm sound when the inputted time matches the current time.

The program creates a Pygame window with a display width of 200 and display height of 600. The font size for the texts displayed is set to 50 and the font used is 'freesansbold.ttf'.

The program uses the time library to get the current time and the pygame.mixer.Sound() function to play the alarm sound, which is located at '/home/pi/alarm_clock/alarm.wav'.

The input field is in the center of the window, with a width of 160 and height of 40. The submit button is located below the input field, centered, with a width of 100 and a height of 50.

The alarm times are displayed below the submit button, with a maximum of one alarm per row. The stop and delete buttons are placed beside each alarm time display.

The stop button is located on the right side of the Pygame window while delete button on the left side.

When the program is run, it starts the Pygame window and initializes the program by starting the Pygame library. It then declares variables and objects that are used throughout the program, such as the Pygame display, font, input field, submit button, and alarm sounds.

The "main loop" of the program is executed until a QUIT Pygame event is triggered, that is, the user closes the Pygame window. During each iteration of the main loop, the program clears the Pygame display, gets the current time, and checks if any alarm time matches the current time and if the alarm is not already playing. If an alarm time matches the current time, the function plays the alarm sound.

The program then displays the current time, the input field, the submit button, and all the inputted alarm times and their corresponding stop and delete buttons. The program also checks if any stop or delete buttons are clicked and if the submit button is clicked, an alarm time is added to the list of alarm times. If the input field is clicked by the user, it becomes active and can accept keyboard input. If the user types ENTER, the program adds the inputted text as an alarm time to the list and clears the input field. If the user types BACKSPACE, the program deletes the last character in the input field. If the user types any other keyboard key, the program adds it to the input field.

Finally, during each iteration of the main loop, the program updates the Pygame display.

When the program is finished, the Pygame library is quit with the pygame.quit() function.

------------------------

You can use your own alarm .wav sound.

Consumes roughly 18%-25% CPU on a Raspberry Pi 4B
