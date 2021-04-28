import os.path, sys
import time

os.system('python3 sensor_controller.py > data.txt')
os.system('python3 formatter.py data.txt format.txt')
os.system('python3 email_driver.py format.txt')
