# Author: Karan Chawla
# Date: 29th Aug '18

from gpiozero import Button 
from math import pi 
import time 
import statistics 

CM_IN_KM = 100000.0
SECS_IN_HOUR = 3600.0

class Anemometer():
    def __init__(self, GPIOPin, radius, wind_interval):
        self._windSpeedSensor = Button(GPIOPin)
        self._windCount = 0
        self._radius = radius
        self._windInterval = wind_interval
        self._K = 1.18
        self._storeSpeeds = []
        self._windSpeedSensor.when_activated = self.spin
        self.windSpeed = 0

    def spin(self):
        self._windCount += 1

    def __calculateSpeed(self):
        speed_KPH = self.compute_speed(self._radius, self._windInterval)
        return speed_KPH * self._K

    def __resetWind(self):
        self._windCount = 0

    def compute(self):
        start_time = time.time()
        while time.time() - start_time <= self._windInterval:
            self.__resetWind()
            time.sleep(self._windInterval)
            finalSpeed = self.__calculateSpeed()
            self._storeSpeeds.append(finalSpeed)
        self.windGust = max(self._storeSpeeds)
        self.windSpeed = statistics.mean(self._storeSpeeds)

    def compute_speed(self, radius, time_sec):
        circumference = 2 * pi * radius
        rotations = self._windCount / 2;
        speed = (circumference * rotations / time_sec)
        speed_KPH = speed * SECS_IN_HOUR / CM_IN_KM
        return speed_KPH
