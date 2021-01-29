from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTimer, QTime, Qt
from mygui.window import *
from mygui.menu import *
import getweather
import json
import sys
import os
import platform
import subprocess
from PyQt5.QtCore import QThread
import time
import logging

co2 = None

if platform.machine() == 'x86_64' or platform.machine() == 'AMD64':
    dev = True
    logging.basicConfig(level=logging.DEBUG, filemode='w', filename='clock.log', format='%(asctime)s [LINE:%(lineno)d]# \
    %(message)s')
else:
    dev = False
    import mh_z19
    import RPi.GPIO as GPIO

    PIN_PWM = 21
    subprocess.call("gpio -g mode 18 pwm", shell=True)
    logging.basicConfig(level=logging.DEBUG, filename='/home/sysop/clock.log', format='%(asctime)s %(message)s')
data_weather = None


def getPwm():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_PWM, GPIO.IN)
    time.sleep(0.2)

    while GPIO.input(PIN_PWM) == 1:
        last_high = time.time()
    while GPIO.input(PIN_PWM) == 0:
        last_low = time.time()
    while GPIO.input(PIN_PWM) == 1:
        last_high = time.time()

    span_high = (last_high - last_low) * 1000
    # print("span_high : " + str(span_high))

    while GPIO.input(PIN_PWM) == 0:
        last_low = time.time()
    while GPIO.input(PIN_PWM) == 1:
        last_high = time.time()
    while GPIO.input(PIN_PWM) == 0:
        last_low = time.time()

    span_low = (last_low - last_high) * 1000

    global co2
    co2 = 5000 * (span_high - 2) / (span_high + span_low - 4)
    GPIO.cleanup()
    return co2


def shell(cmd, shell=True):
    shell = True
    try:

        respose = subprocess.check_output(cmd, shell=shell)
    except:
        respose = None

    return respose


class GetWeather(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.data = None

    def __del__(self):
        self.wait()

    def run(self):

        try:

            self.data = getweather.get_weather()

        except Exception as e:
            logging.debug("Data weather request fall with error: " + str(e))


class GetDates(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.row_data = None

    def __del__(self):
        self.wait()

    def run(self):

        if dev:
            self.row_data = {'temp': 21, 'co2': 1972}

        else:

            self.row_data = mh_z19.read_all()
            if self.row_data["co2"] == None:
                self.row_data["co2"] = getPwm()
                self.row_data["temperature"] = None


class Controller:

    def __init__(self):

        self.clock = None
        self.ui_clock = None
        self.t = None
        self.co2 = None
        self.weather = GetWeather()
        self.dates = GetDates()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.day = True
        self.changed_b = None

        with open(self.path + "/settings.json") as sett_file:
            self.settings = eval(sett_file.read())
        self.day_night()

        self.second_window = QtWidgets.QMainWindow()
        self.second_window = uic.loadUi(self.path + "/data/ui/weather_today.ui")
        self.second_window.setWindowFlags(Qt.FramelessWindowHint)

        self.clock = QtWidgets.QMainWindow()
        self.clock = uic.loadUi(self.path + "/data/ui/clock.ui")
        self.clock.setWindowFlags(Qt.FramelessWindowHint)

        self.therd_window = QtWidgets.QMainWindow()
        self.therd_window = uic.loadUi(self.path + "/data/ui/weather_3_day_2.ui")
        self.therd_window.setWindowFlags(Qt.FramelessWindowHint)
        self.menu = QtWidgets.QMainWindow()
        self.menu = uic.loadUi(self.path + "/data/ui/menu.ui")
        self.menu.setWindowFlags(Qt.FramelessWindowHint)
        self.info = QtWidgets.QMainWindow()
        self.info = uic.loadUi(self.path + "/data/ui/info.ui")
        self.info.setWindowFlags(Qt.FramelessWindowHint)
        self.timer_sensors = QTimer()
        self.timer_sensors.timeout.connect(self.dates.run)
        self.timer_sensors.start(1000 * 5)
        self.timer_clock = QTimer()
        self.timer_clock.timeout.connect(self.showtime)
        self.timer_clock.start(1000)
        self.timer_weather = QTimer()
        self.timer_weather.timeout.connect(self.weather.run)
        self.timer_weather.start(1000 * 60 * 15)
        self.timer_dates = QTimer()
        self.timer_dates.timeout.connect(self.chenge_dates)
        self.timer_dates.start(1000 * 5)
        self.timer_show_clock = QTimer()
        self.timer_show_clock.setSingleShot(True)
        self.timer_show_clock.timeout.connect(self.show_clock)
        self.dates.run()
        self.weather.run()
        self.clock.pushButton.clicked.connect(lambda: self.pressedOnButton())
        self.menu.info_b.clicked.connect(self.turn_time)
        self.menu.exit_Button.clicked.connect(self.exit_menu)
        self.menu.ap_button.clicked.connect(self.dw)
        self.changed_b = False
        self.last_day = None
        self.day_night()

    def pressedOnButton(self):
        self.timer_odw.stop()
        self.clock.close()
        self.menu.show()
        self.menu_tmer = QTimer()
        self.menu_tmer.singleShot(1000 * 30, self.exit_menu)


    def turn_time(self):
        if self.settings["local_zone"] == 0:
            self.settings["local_zone"] = 1
        else:
            self.settings['local_zone'] = 0



    def dw(self):
        #self.timer_show_clock = QTimer()
        #self.timer_show_clock.setSingleShot(True)
        self.timer_show_clock.start(1000 * 30)
        self.menu.close()
        self.second_window.show()

    def net_connect(self):
        shell("sudo wpa_cli reconnect")


    def exit_menu(self):
        self.menu.close()
        self.timer_odw.start()
        self.show_clock()


    def chenge_dates(self):

        if self.dates.row_data:
            data_dict = self.dates.row_data
            if dev:
                self.t = data_dict['temp']
                self.co2 = data_dict['co2']
            else:
                if data_dict != 9:
                    self.t = int(data_dict['temperature']) - 5
                    self.co2 = data_dict['co2']

        if self.t:

            if self.t > 28:
                color = "red"
            elif self.t <= 28 and self.t >= 18:
                color = "#00ff00"  # "green"
            else:
                color = "blue"

            self.clock.Temp_value.setText("<font color=" + color + ">" + str(self.t) + "</font>")

        if self.co2:

            if int(self.co2) > 2000:
                color = "red"
            elif (int(self.co2) < 2000) and (int(self.co2) > 800):
                color = "yellow"
            else:
                color = "#00ff00"  # "green"
            self.clock.co2_value.setText("<font color=" + color + ">" + str(self.co2) + "</font>")

    def show_clock(self):

        if not self.weather.data:
            logging.debug("getting weather")
            self.weather.run()
            self.timer_show_clock.start(1000 * 15)

        if self.day and self.weather.data:
            self.timer_odw = QTimer()
            self.timer_odw.setSingleShot(True)
            self.timer_odw.timeout.connect(self.show_curent_weather)
            self.timer_odw.start(1000 * int(self.settings["clock_timer"]))

        self.therd_window.hide()

        self.chenge_dates()
        self.clock.show()

        # подготавливаем для показа 2 окно
        icon = self.path + '/data/wi/' + self.weather.data["win"] + ".png"
        pixmap = QPixmap(icon)
        pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio)
        self.second_window.today_weater_icon.setPixmap(pixmap)
        self.second_window.weater_descripton.setText(self.weather.data["wtext"].decode("utf-8"))
        self.second_window.today_high_temp.setText((self.weather.data["tmax"]))
        self.second_window.today_low_temp.setText(self.weather.data["tlow"])
        self.second_window.today_cur_temp.setText(self.weather.data["tn"])

    def day_night(self):

        time = QTime.currentTime()
        self.last_day = self.day
        if time.hour() > 20 or time.hour() < 6:
            if time.minute() > 30:
                self.day = False


        else:
            self.day = True

        if self.day != self.last_day:
            self.changed_b = False
            # print("self.changed_b " + self.changed_b)
        if not dev:
            if not self.changed_b and not self.day: #night
                shell("gpio -g pwm 18 " + str(45))
                self.changed_b = True
                self.timer_dates.stop()
                self.timer_weather.stop()

            if self.day and not self.changed_b:   #day
                shell("gpio -g pwm 18 " + str(500))
                self.timer_odw = QTimer()
                self.timer_odw.setSingleShot(True)
                self.timer_odw.timeout.connect(self.show_curent_weather)
                self.timer_odw.start(1000 * self.settings["clock_timer"])
                self.changed_b = True

                self.timer_weather = QTimer()
                self.timer_weather.timeout.connect(self.weather.run)
                self.timer_weather.start(1000 * 60 * 15)

                self.timer_dates = QTimer()
                self.timer_dates.timeout.connect(self.chenge_dates)
                self.timer_dates.start(1000 * 5)
        #self.show_clock()

    def show_curent_weather(self):



        self.timer_3dw = QTimer()
        self.timer_3dw.singleShot(1000 * int(self.settings["weather_1d_timer"]), self.show_weather_3_day)
        self.clock.hide()
        self.second_window.show()

 #подготавливаем для показа 3 окно
        if self.weather.data:
            icon1 = self.path + '/data/wi/' + self.weather.data["wi1"] + ".png"
            pixmap = QPixmap(icon1)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            self.therd_window.icon1.setPixmap(pixmap)

            icon2 = self.path + '/data/wi/' + self.weather.data["wi2"] + ".png"
            pixmap = QPixmap(icon2)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            self.therd_window.icon2.setPixmap(pixmap)

            icon3 = self.path + '/data/wi/' + self.weather.data["wi3"] + ".png"
            pixmap = QPixmap(icon3)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            self.therd_window.icon3.setPixmap(pixmap)

            self.therd_window.firstdow.setText(self.weather.data["day1"][:8].decode("utf-8"))
            self.therd_window.temp1_high.setText(self.weather.data["tmax1"])
            self.therd_window.temp1_low.setText((self.weather.data["tlow1"]))
            self.therd_window.fseconddow.setText(self.weather.data["day2"][:8].decode("utf-8"))
            self.therd_window.temp2_high.setText(self.weather.data["tmax2"])
            self.therd_window.temp2_low.setText(self.weather.data["tlow2"])
            self.therd_window.therddow.setText(self.weather.data["day3"][:8].decode("utf-8"))
            self.therd_window.temp3_high.setText(self.weather.data["tmax3"])
            self.therd_window.temp3_low.setText(self.weather.data["tlow3"])

    def show_weather_3_day(self):


            self.timer_show_clock = QTimer()
            self.timer_show_clock.setSingleShot(True)
            self.timer_show_clock.timeout.connect( self.show_clock)
            self.timer_show_clock.start(1000 * int(self.settings["weather_3d_timer"]))
            self.second_window.hide()
            self.therd_window.show()

    def showtime(self):
        self.day_night()
        time = QTime.currentTime()
        time = time.addSecs(60 * 60 * int(self.settings["local_zone"]))


        text = time.toString("hh:mm")
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.clock.lcdNumber.display(text)

    def save_dates(self):
        ssid = shell('sudo su -c "wpa_cli status | grep ^ssid="')
        ssid = str(ssid)
        live_data = {"temperature": self.t, "co2": self.co2, "ssid": ssid[7:-3],
                     "clock_timer": self.settings["clock_timer"],
                     "weather_1d_timer": self.settings["weather_1d_timer"],
                     "weather_3d_timer": self.settings['weather_3d_timer'], "local_zone": self.settings["local_zone"]}
        with open("/tmp/jdata.html", "w") as datafile:
            datafile.write(json.dumps(live_data))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_clock()
    sys.exit(app.exec_())
