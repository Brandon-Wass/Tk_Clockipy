## Introduced headless versions of all 3 codes! (These versions do not share code with their GUI counterparts!)
- V-4.0.headless

  - Prints the current time to the console

- V-4.1.headless

  - Currently uses the alarm.wav file exclusively. You may edit the code to use a different audio file

  - Prints the current time to the console once before prompting the user to set the alarm time

    - Alarm can be stopped by typing the word stop

- V-4.2.headless

  - Prompts the user to input the GPIO pin number that the buzzer, or LED, is connected to

  - Prints the current time to the console once before prompting the user to set the alarm time

    - Alarm can be stopped by typing the word stop

  - Instead of setting the GPIO to constantly High when the alarm is to ring, the GPIO is cycled High and Low multiple times a second

----------

## V-4.x0:
- Reverted to basic background coloring

  - Background image caused freezes

  - Background is no longer an image but is a solid color

- Minor changes to code

  - Changing Analog Clock Background now changes background of everything at once

  - Adjusted spacing of marks, numbers, and hands on the analog clock

  - All versions share the exact same base code

  - Reorganized the code flow to make debugging and future changes easier

  - Got rid of any unused code in all versions

----------

## V-3.x1:
- Minor coding patch

  - Brought back GPIO version

- Digital clock has its own customization features

  - Added buttons to the left-click menu

----------

## V-3.x0:
- Added digital date and time in top left corner

  - The color of the text is tied to the clock numbers.

    - This will be patched in a minor update or new version to have its own definitions to be customized separately.

----------

## v-2.x2:

- Now uses a black 1x1 image file as the background

  - This allows the background to be changed to whatever provided image file

    - Changing the background is accessed under the left-click menu

- Raspberry Pi GPIO Buzzer version has been taken out due to compatibility issues with new coding

  - These programs no longer work on Raspberry Pi

    - Last compatible version is V-2.x1

----------

## V-2.x1:

- Added a snooze button to the alarm popup

  - Default snooze time is 5 minutes

    - This can be adjusted under the left-click popup menu
    

----------

## V-2.x0:

- Added a menu interface that is accessed by left click full of customization options

- Changed the alarm display to a button that can be pressed to reset the alarm
  
  - This does not stop the alarm

- Instead of opening a top level window when the alarm rings, an overlay is created with the buttons for stopping the alarm

  - This gives the aesthetic of looking to be built into the app itself

- Changed the alarm functions

- Exit program via button in the menu

----------

## V-1.x3:

- Minor code changes

- Implemented loop for alarm sound *V-1.33

- Changed Reset button color to yellow

- Added button hold function to rapidly increase the alarm time

  - Double-clicking in somewhat rapid succession then holding seems to cause the rapid increment to go even faster.

----------

## V-1.x2:

- Initialized alarm variables

- Updated check_alarm method

- Remodeled alarm_rings method

  - Moved alarm_window to the center of the screen

    - Changed alarm_window size

    - Added a reset_alarm method to reset the alarm display

    - Added a button to alarm_window

      - Color coded buttons

        - Red button stops the alarm

          - This keeps the previously set alarm

        - Green button stops the alarm and resets the alarm display

          - This effectively "shuts off" the alarm feature, and allows a new alarm to be set

----------

## V-1.x1:

- Updated button and alarm display loacations to be static regardless of display size

- Redefined the alarm message box to keep the clock running while the dialog alarm message is showing

- Relocated and redefined the stop_alarm process to clear the current alarm when it goes off

----------

## V-1.x0:

- Original Release

----------
