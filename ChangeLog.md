V-1.x3:

  - Minor code changes

  - Implemented loop for alarm sound *V-1.33

  - Changed Reset button color to yellow

  - Added button hold function to rapidly increase the alarm time

    >NOTE: Double-clicking in somewhat rapid succession then holding seems to cause the rapid increment to go even faster.

----------

V-1.x2:

  - Initialized alarm variables

  - Updated check_alarm method

  - Remodeled alarm_rings method

    >Moved alarm_window to the center of the screen

    >Changed alarm_window size

    >Added a reset_alarm method to reset the alarm display

    >Added a button to alarm_window

      >>Color coded buttons

        >>>Red button stops the alarm

          * This keeps the previously set alarm

        >>>Green button stops the alarm and resets the alarm display

          * This effectively "shuts off" the alarm feature, and allows a new alarm to be set

----------

V-1.x1:

  - Updated button and alarm display loacations to be static regardless of display size

  - Redefined the alarm message box to keep the clock running while the dialog alarm message is showing

  - Relocated and redefined the stop_alarm process to clear the current alarm when it goes off

----------

V-1.x0:

  - Original Release