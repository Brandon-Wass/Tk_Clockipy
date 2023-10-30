# Fullscreen Clock with Alarm

A simple fullscreen digital clock built with Python's tkinter module. Apart from just telling the time, the clock offers a variety of features, including a robust alarm function and extensive customization options.

## Why did I make this?

  - This program was made for several reasons

    >I needed a visual clock for my computer station that doesnt require me squinting or wearing my glasses to read the clock in the corner of my screen. I have multiple computers setup across several monitors, so its easy to run one of these programs on of the other computers while I do whatever on my main machine.

    >No more switching out of a fullscreen application to see the time. GAME ON!

    >Both alarm versions work better than ANY alarm I've ever set on any phone I've owned. They actually wake me up! I prefer the GPIO Buzzer version, as the audio file version scares my wife every time it goes off.

    >My youngest child is currently potty training. Setting the snooze to 60 minutes and using one of the alarm versions works great as an hourly "potty timer" for her to try using the "big potty". We prefer the GPIO Buzzer, as its a simple sound she recognizes throughout the house.

    >I have a purpose built Raspberry Pi music player with touchscreen and battery backup that has a built in buzzer. This brings portability to the project and makes it great for many things around the house where an alarm clock or timer of sorts may be usefull.

      ![IMG_E1034](https://github.com/B-Boone/Alarm_Clock/assets/101531474/7e788587-604b-4c6b-b479-59de09087e31)

      ![IMG_E1035](https://github.com/B-Boone/Alarm_Clock/assets/101531474/d66a21f4-c247-48d6-8f11-58c95c352932)

      >>No, this is not the final design for my Pi project. There will be some custom PCB going into the project to make it more modular. There will also be a 3D printed case in this project's future.

## Multiple Versions**:

    V-4.0x: Round clock.

    V-4.1x: Round clock with audio file alarm. (coded for Linux)

    V-4.2x: Round clock with GPIO buzzer alarm. (coded for Raspberry Pi)

    Headless Versions: Non-GUI versions of the clocks, useful for command-line based setups.

## Core Features:

  **Fullscreen Clock**: Display time in a frameless window mode.

  **Interactive**: Click anywhere on the screen to close the application.

  **Custom Background**: Customize the background with an image of your own.

  **Set Alarm**: Incremental buttons to set hours and minutes for the alarm.

  **Visual Alarm**: A pop-up notification appears when the alarm rings.

  **Stop/Snooze/Reset Alarm**: Buttons to stop and keep the previous alarm, stop and snooze the alarm, or stop and reset the alarm.

## Prerequisites:

  **Python 3.x**

  **tkinter** module (typically comes pre-packaged with Python standard distributions).

## Installation:

  1. **Clone the repository and navigate to the directory**:

    ```
    git clone https://github.com/B-Boone/Alarm_Clock
    cd Alarm_Clock
    ```

  2. **Install dependencies**:

    ```
    pip3 install tkinter
    ```

  3. **Move alarm.wav and image.png files to home directory**: Only for V-4.10 (audio version)

    ```
  mv ~/Alarm_Clock/alarm.wav ~ && mv ~/Alarm_Clock/image.png ~
    ```

## How to Use: 

  1. **Run the Application**: Make sure to use the correct version number! Check the version number of the file you want to use, as we are now on version number 3.x0!

    V-4.00
      ```
      python3 clock_V-4.00.py
      ```

![2023-09-29-112542_1920x1080_scrot](https://github.com/B-Boone/Alarm_Clock/assets/101531474/4300af78-4376-4d57-8db2-e8a3c194d26f)

    V-4.10 & V-4.20
      ```
      python3 clock_V-4.10.py
      ```
      python3 clock_V-4.20.py
      ```

![2023-10-03-104239_1920x1080_scrot](https://github.com/B-Boone/Alarm_Clock/assets/101531474/6c2c4981-83bd-4ed7-adcf-7ea2d02f100a)

  2. **Set the Alarm**: Click the 'Set Hour' and 'Set Minute' buttons to set the alarm.

  3. **Alarm Notification**: A pop-up will appear when the alarm rings. Press the stop button to stop the alarm and keep the previoulsy set one, press the snooze button to stop the alarm and have it go off again in 5 minutes*, or press the reset button to stop the alarm and clear the previously set one.

    * This can be adjusted under the left-click popup menu
    
![2023-10-11-224403_1920x1080_scrot](https://github.com/B-Boone/Alarm_Clock/assets/101531474/0a88ea53-1ad6-41d6-985b-d287c105d0de)

  4. **Exit**: Click anywhere on the clock to exit the program.

## Structure:

  **Clock Class**: Inherits from `tk.Tk`.

  - Consists of methods that manage the clock display: drawing the hands, hour marks, and numbers.

  - Manages the alarm check function.

  - Contains the button commands that allow setting the alarm hour and minute.

  - Over the versions, the code structure has been streamlined for easier debugging and future improvements.

## Possible changes:

  - I currently have no future changes in mind. This project is at the point where it gets updated when something comes to mind, as I am satisfied with the functionalities provided.

## Contributing:

  Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License:

  **[MIT](https://choosealicense.com/licenses/mit/)**

---

## *ENJOY!*
