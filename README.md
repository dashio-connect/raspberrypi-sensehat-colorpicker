# How to Connect DashIO Dashboard App to a Raspberry Pi with a Sense HAT Color Picker

This guide will walk you through the process of connecting the DashIO Dashboard App to a Raspberry Pi equipped with a Sense HAT, allowing you to control the RGB LED using a color picker interface. This interactive control system is a great way to customize the colors displayed by the Sense HAT's LED matrix.

## Prerequisites

Before you begin, make sure you have the following:

- A Raspberry Pi with a Sense HAT attached.
- Python installed on your Raspberry Pi.
- The DashIO library installed on your Raspberry Pi. You can install it using pip:

  ```shell
  pip install dashio
  ```

- The DashIO app available here:

Apple              | Android
:-----------------:|:------------------:
[<img src=https://raw.githubusercontent.com/dashio-connect/python-dashio/master/Documents/download-on-the-app-store.svg width=200>](<https://apps.apple.com/us/app/dash-iot/id1574116689>) | [<img src=https://raw.githubusercontent.com/dashio-connect/python-dashio/master/Documents/Google_Play_Store_badge_EN.svg width=223>](<https://play.google.com/store/apps/details?id=com.dashio.dashiodashboard>)


## Getting Started

1. **Clone or Download the Code**: You can clone the code provided in this repository or download it as a ZIP file. 

 ```shell
  git clone https://github.com/dashio-connect/raspberrypi-sensehat-colorpicker
  cd raspberrypi-sensehat-colorpicker
  ```

2. **Modify the INI File (Optional)**: The script uses an INI file (`colorwheel.ini`) to store device information such as the username, password, and device name. You can modify this file to suit your preferences or leave it as is. This file is created the first time the python script is run.

3. **Run the Script**: Execute the Python script on your Raspberry Pi. This script creates a connection to DashIO and sets up a color picker control.

   ```shell
   python main.py -v2
   ```

    The -v2 is to run with debug logging. To see the options run with:

   ```shell
   python main.py -h
   ```

4. **Access the DashIO Dashboard**: Open the DashIO Dashboard App on your mobile device.

5. **Log In**: If you have configured a username and password in the INI file, use those credentials to log in. If you don't have a DashIO server account the script will create a local TCP connection.

6. **View the Color Picker**: Under 'All Devices' -> 'Find New Device' -> 'TCP Discovery'(or 'My Devices on Dash' ). You should see a device named "Color Picker" in your dashboard. Tap on it to access the color picker control.

7. **Select a Color**: Use the color picker control to choose the desired color. The RGB LED on your Sense HAT should change to reflect your color choice.

8. **Enjoy the Control**: Experiment with different colors and have fun controlling the RGB LED on your Sense HAT via the DashIO Dashboard.

9.  **Exit the Script**: To stop the script, press `Ctrl + C` in the terminal where it is running. This will gracefully shut down the DashIO connection.

## Additional Information

- The script sets up a DashIO device with a color picker control. The selected color is sent to the Raspberry Pi, which then updates the Sense HAT's RGB LED accordingly.

- You can customize the INI file to change the device name or other settings. The INI file is automatically created if it doesn't exist.

- The script also allows you to adjust the verbosity of the logging output using the `-v` or `--verbose` command-line argument.

- Make sure you have the Sense HAT library installed on your Raspberry Pi for the Sense HAT to work correctly.

- Feel free to explore and modify the script to add more features or integrate it with other sensors and controls.

Congratulations! You've successfully connected your Raspberry Pi with a Sense HAT to the DashIO Dashboard App, allowing you to control the RGB LED with ease. Enjoy experimenting with different colors and creating interactive displays.