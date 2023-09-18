"""
MIT License

Copyright (c) 2020 DashIO-Connect

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import configparser
import logging
import platform
import signal
import time
import shortuuid

from sense_hat import SenseHat

import dashio


class TestColorPicker:
    def signal_cntrl_c(self, os_signal, os_frame):
        self.shutdown = True

    def init_logging(self, logfilename, level):
        log_level = logging.WARN
        if level == 1:
            log_level = logging.INFO
        elif level == 2:
            log_level = logging.DEBUG
        if not logfilename:
            formatter = logging.Formatter("%(asctime)s, %(message)s")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger = logging.getLogger()
            logger.addHandler(handler)
            logger.setLevel(log_level)
        else:
            logging.basicConfig(
                filename=logfilename,
                level=log_level,
                format="%(asctime)s, %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        logging.info("==== Started ====")

    def parse_commandline_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v",
            "--verbose",
            const=1,
            default=0,
            type=int,
            nargs="?",
            help="""increase verbosity:
                            0 = only warnings, 1 = info, 2 = debug.
                            No number means info. Default is no verbosity.""",
        )
        parser.add_argument("-u", "--username", help="DashIO Username", dest="username", default="username")
        parser.add_argument("-w", "--password", help="DashIO Password", dest="password", default="password")
        parser.add_argument("-i", "--inifile", dest="inifilename", default="colorwheel.ini", help="ini file location", metavar="FILE")
        parser.add_argument("-l", "--logfile", dest="logfilename", default="", help="logfile location", metavar="FILE")
        args = parser.parse_args()
        return args

    def color_picker_handler(self, msg):
        print(msg)
        self.c_picker.color_value = msg[3]
        try:
            pass
            self.sense.clear(self.color_to_rgb(msg[3]))
        except ValueError:
            pass

    def color_to_rgb(self, color_value):
        """Return (red, green, blue) for the color."""
        clr = color_value.lstrip('#')
        lv = len(clr)
        return tuple(int(clr[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def __init__(self):

        # Catch CNTRL-C signel
        signal.signal(signal.SIGINT, self.signal_cntrl_c)
        self.shutdown = False
        args = self.parse_commandline_arguments()
        self.init_logging(args.logfilename, args.verbose)
        self.sense = SenseHat()
        ini_file = args.inifilename
        config_file_parser = configparser.ConfigParser()
        config_file_parser.defaults()
        new_ini_file = False
        try:
            ini_f = open(ini_file)
            ini_f.close()
        except FileNotFoundError:
            default = {
                'DeviceID': shortuuid.uuid(),
                'DeviceName': 'Color Picker',
                'DeviceType': 'Color Picker',
                'username': args.username,
                'password': args.password
            }
            config_file_parser['DEFAULT'] = default
            with open(ini_file, 'w') as configfile:
                config_file_parser.write(configfile)
            new_ini_file = True

        if not new_ini_file:
            config_file_parser.read(ini_file)

        self.device = dashio.Device(
            config_file_parser.get('DEFAULT', 'DeviceType'),
            config_file_parser.get('DEFAULT', 'DeviceID'),
            config_file_parser.get('DEFAULT', 'DeviceName')
        )

        if config_file_parser.get('DEFAULT', 'username') == "username":
            self.connection = dashio.TCPConnection()
        else:
            self.connection = dashio.DashConnection(
                config_file_parser.get('DEFAULT', 'username'),
                config_file_parser.get('DEFAULT', 'password')
            )

        self.connection.add_device(self.device)
        self.page_name = "Color Picker: " + platform.node()

        self.page_test = dashio.DeviceView("Color Picker", self.page_name)
        self.c_picker = dashio.ColorPicker("CPKR1", control_position=dashio.ControlPosition(0.0, 0.0, 1.0, 0.45))
        self.c_picker.add_receive_message_callback(self.color_picker_handler)
        self.page_test.add_control(self.c_picker)
        self.device.add_control(self.c_picker)
        self.device.add_control(self.page_test)

        while not self.shutdown:
            time.sleep(1.0)
        self.connection.close()
        self.device.close()


if __name__ == "__main__":
    TestColorPicker()
