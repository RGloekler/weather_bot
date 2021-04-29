#!/usr/bin/python
# -*- coding:UTF-8 -*-

import time
import Si1145 as Sensor
import RPi.GPIO as GPIO
import os
import subprocess as sp
from subprocess import call

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# initialize both sensors to LOW
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(17, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

# pin 17 controls the UV sensor
GPIO.output(17, GPIO.HIGH)

time.sleep(0.1)
Sensor.Si1145_Init()

unplugged = False
uv_avg = []

while True: 
  try:
    if unplugged:
      Sensor.Si1145_Init()
    UVindex = Sensor.Si1145_readUV()
    UVindex /= 100.0

    uv_avg.append(UVindex)

    print("UV: ", UVindex)
    unplugged = False
    if (len(uv_avg) > 50):
      break # got all our data readings
    continue
  except:
    print('Sensor Unplugged')
    unplugged = True
    Sensor.Si1145_close()

  Sensor.Si1145_close()
GPIO.output(17, GPIO.LOW)
GPIO.output(22, GPIO.HIGH)

p = call(["./bme280", ">>", "data.txt"])
#p = sp.Popen(["./bme280"], shell=False)

GPIO.output(22, GPIO.LOW)



#time.sleep(2.5)
Sensor.Si1145_close()
exit()
