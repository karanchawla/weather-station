# Author: Karan Chawla
# Date: 29th Aug '18

from gpio import Button 
from math import pi 
import time 
import statistics 

CM_IN_KM = 100000.0
SECS_IN_HOUR = 3600.0

class Anemometer():
    def__init__(self, GPIOPin, radius, wind_interval):
        self._windSpeedSensor = Button(GPIOPin)
        self._windCount = 0
        self._radius = radius
        self._windInterval = wind_interval
        self._K = 1.18 

    def spin(self):
        self._windCount += 1

    def __calculateSpeed(self, time_sec):
        speed_KPH = speed(self._radius, time_sec, self._windInterval)
        return speed_KPH * self.K

    def __resetWind(self):
        self._windCount = 0

    def compute(self):
        while True: 
            start_time = time.time()
            while time.time() - start_time <= self._windInterval:
                self.__resetWind()
                time.sleep(self._windInterval)
                finalSpeed = self.__calculateSpeed(self._windInterval)
                storeSpeeds.append(finalSpeed)
            self._windGust = max(storeSpeeds)
            self._windSpeed = statistics.mean(storeSpeeds)


    @staticmethod
    def speed(radius, time_sec, frequency):
        circumference = 2 * pi * radius 
        rotations = frequency / 2; 
        speed = (circumference * rotations / time_sec) 
        speed_KPH = speed * SECS_IN_HOUR / CM_IN_KM

        return speed_KPH
