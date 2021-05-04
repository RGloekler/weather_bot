#!/usr/bin/python
import sys
import re
from datetime import date
from datetime import datetime

# This python file, takes 2 command line arguments in the form of 2 text files.
# The function format which is executed from the main function below reads through
# data.txt, sorting each valid number into a list. Averages are found for each variable.
#
# The current time, date, and averages are written into the other text file called
# format.txt. This can be attached or read into the email driver.
    #Email body format is as follows:
    #day/month/year
    #Time of day formatting is completed
    #
    # Temperature (°C): x
    # Humidity (%): x
    # Air Pressure (hPA): x
    # UV Index (25mW/m^2): x
    #
#To use: $python3 data.txt format.txt



def format():
    #Lists to hold all numerical data values for averaging.
    uv_index, temp_c, pressure_hpa, humidity = [], [], [], []

    #Open the data.txt from argv[1] and read contents into a string
    raw_data = open(sys.argv[1], 'r')
    #String to contain line.
    raw_string = ""
    #For each line in data.txt
    for line in raw_data:
        raw_string = line
        buffer = re.findall("(\d+\.\d{2})", raw_string)
        #If buffer has 1 element. It is the UV sensor.
        if len(buffer) == 1:
            uv_index.append(float(buffer[0]))
        #If buffer has 3 elements. It is the bme280.S
        if len(buffer) == 3:
            temp_c.append(float(buffer[0]))
            pressure_hpa.append(float(buffer[1]))
            humidity.append(float(buffer[2]))
        #Clear buffer for next line
        buffer.clear()
    #Done reading. Close data.txt.
    raw_data.close()

    #Find Averages for each variable.
    uv_avg = sum(uv_index)/len(uv_index)
    temp_avg = sum(temp_c)/len(temp_c)
    pressure_avg = sum(pressure_hpa)/len(pressure_hpa)
    humidity_avg = sum(humidity)/len(humidity)

    #Open and write to the format.txt file. Should overwrite previous file not append.
    email_body = open(sys.argv[2], 'w')

    #Get current date and time. Convert to string.
    date_var = date.today().strftime("%B %d, %Y")
    time_var = datetime.now().strftime("%I:%M:%S %p")
    #Strings to add to the email body.
    greeting = "Greetings from WEATHER_BOT!\n"
    date_string = f"{date_var}\n"
    time_string = f"{time_var}\n"
    temp_string = f"Temperature (C): {temp_avg:.2f}\n"
    humidity_string = f"Humidity (%): {humidity_avg:.2f}\n"
    pressure_string = f"Air Pressure (hPA): {pressure_avg:.2f}\n"
    uv_string = f"UV Index (25mW/m^2): {uv_avg:.2f}\n"
    #List of strings with formatting.
    to_add = [greeting, '\n', date_string, time_string, '\n', temp_string, humidity_string, pressure_string, uv_string]
   
    #Write to format.txt with complete body.
    email_body.writelines(to_add)
    #All required tasks finish. Close and end.
    email_body.close()




def main():
    #Check for 2 arguments
    if len(sys.argv) != 3:
        print("usage: \'python3 formatter.py <data.txt> <format.txt>\'")
        exit()
    
    #Execute format function
    format()

#main guard
if __name__ == "__main__":
    main()
    sys.exit()
