# Clockipy

Clockipy is a versatile clock application, offering various versions with different functionalities. 

## Why did I make this?

  - This program was made for several reasons

    - I needed a visual clock for my computer station that doesn't require me squinting or wearing my glasses to read the clock in the corner of my screen. I have multiple computers setup across several monitors, so it's easy to run one of these programs on one of the other computers while I do whatever on my main machine.

    - No more switching out of a fullscreen application to see the time. GAME ON!

    - Both alarm versions work better than ANY alarm I've ever set on any phone I've owned. They actually wake me up! I prefer the GPIO Buzzer version, as the audio file version scares my wife every time it goes off.

    - My youngest child is currently potty training. Setting the snooze to 60 minutes and using one of the alarm versions works great as an hourly "potty timer" for her to try using the "big potty". We prefer the GPIO Buzzer, as its a simple sound she recognizes throughout the house.

    - I have a purpose built Raspberry Pi music player with touchscreen and battery backup that has a built in buzzer. This brings portability to the project and makes it great for many things around the house where an alarm clock or timer of sorts may be useful.

      ![IMG_E1034](https://github.com/B-Boone/Alarm_Clock/assets/101531474/7e788587-604b-4c6b-b479-59de09087e31)

      ![IMG_E1035](https://github.com/B-Boone/Alarm_Clock/assets/101531474/d66a21f4-c247-48d6-8f11-58c95c352932)

      - No, this is not the final design for my Pi project. There will be some custom PCB going into the project to make it more modular. There will also be a 3D printed case in this project's future.

## Directory Overview:

### `clockipy_for_windows`:

This directory houses the original inspiration for the program as well as the necessary audio files:

- **clockipy_original**: The original version of the program.
- **clockipy_widget**: A newer version of the original program with persistent settings. This is available as both a `.py` and an `.exe` file.

> Note: Future development primarily focuses on the `clockipy_for_linux` directory. While base models (V-x.0x) are compatible with Windows, other versions are Linux exclusive due to coding differences.

### `clockipy_for_linux`:

This directory contains the Linux-specific versions of Clockipy as well as the necessary audio files and icon file.

---

## Core Features:

- **Fullscreen Clock**: Display time in a frameless window mode.
- **Interactive**: Click anywhere on the screen to close the application.
- **Custom Background**: Customize the background with an image of your own.
- **Set Alarm**: Incremental buttons to set hours and minutes for the alarm.
- **Visual Alarm**: A pop-up notification appears when the alarm rings.
- **Stop/Snooze/Reset Alarm**: Buttons to stop and keep the previous alarm, stop and snooze the alarm, or stop and reset the alarm.

## Recent Updates:

### Splitting the Program:

The program has been divided based on the platform:

- **Windows**: 
  - Original versions can be found in `clockipy_for_windows`.
  - The directory contains both the original inspiration (`clockipy_original`) and an updated version with persistent settings (`clockipy_widget`).
  
- **Linux**:
  - Development continues in the `clockipy_for_linux` directory.

### Headless Versions Introduced:

Versions without a GUI, purely console-based:

- **V-4.0.headless**: Displays current time in the console.
- **V-4.1.headless**: Uses the `alarm.wav` exclusively. Can be edited to use a different audio file. After showing the current time, it prompts users to set an alarm. This alarm can be stopped by typing `stop`.
- **V-4.2.headless**: Asks users for the GPIO pin number for the buzzer or LED. After showing the current time, it prompts users to set an alarm. This can be stopped by typing `stop`. Rather than keeping the GPIO constantly High, it alternates between High and Low multiple times per second.

### Other Recent Versions:

For a brief overview on what each version introduced or fixed, see below:

- **V-4.x0**: Basic color updates, reorganization of code, background image removal due to freezing issues, etc.
- **V-3.x1**: Minor code patches, reintroduction of the GPIO version, digital clock customization, etc.
- **V-3.x0**: Introduced digital date/time, color adjustments, etc.
- **V-2.x2**: Background adjustments, removal of Raspberry Pi compatibility, etc.
- **V-2.x1**: Introduction of the snooze button, customization of snooze time, etc.
- **V-2.x0**: Menu interface addition, alarm display overhaul, program exit changes, etc.
- **V-1.x3**: Minor code adjustments, loop implementation for alarm sound, reset button color change, etc.
- **V-1.x2**: Alarm functionalities, button placements, alarm window adjustments, etc.
- **V-1.x1**: Static button and alarm display locations, alarm message box changes, etc.
- **V-1.x0**: Initial full-screen release.

To see the full list of changes made along the way, make sure to check the ChangeLog.md

---

## Installation:

1. **Clone the repository and navigate to the directory**:
    ```bash
    git clone https://github.com/B-Boone/Clockipy
    cd Clockipy
    ```

2. **Install dependencies**:
    ```bash
    pip3 install tkinter
    ```

3. **Move alarm.wav file to home directory**: Only for V-4.1x (audio versions):
    ```bash
    mv ~/Clockipy/alarm.wav ~
    ```

# Usage:

## For Windows Users:

### Using Clockipy Widget:

1. Navigate to the `clockipy_for_windows` directory.
2. Here, you will find both the `.py` and `.exe` versions of `clockipy_widget`.
   - For the `.py` version, ensure you have Python installed. Run the script using `python clockipy_widget.py`.
   - For the `.exe` version, simply double-click the file to run the application.

### Using the Original Clockipy:

1. In the same `clockipy_for_windows` directory, you can find the `clockipy_original` script.
2. Run the script using `python clockipy_original.py`.

> Note: Base models (V-x.0x) within the `clockipy_for_linux` directory will also work on Windows.

## For Linux Users:

1. Navigate to the `clockipy_for_linux` directory.
2. Depending on your preference, choose the version you want to run.
3. Run the selected script using `python3 <selected_script_name>.py`.

> Warning: Not all versions in `clockipy_for_linux` are compatible with Windows. Ensure you're using the correct versions if switching between operating systems.

---

## Roadmap to the Future:

  - Persistent settings will be added to the Linux based GUI versions

## Contributing:

  Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License:

This project is licensed under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) License.

---

## *ENJOY!*
