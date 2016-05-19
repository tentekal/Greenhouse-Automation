#!/usr/bin/env python

import sqlite3
import RPi.GPIO as gpio
import time
from datetime import datetime
import Adafruit_DHT

# global variables (speriod controls the frequency of sensor readings)
speriod=(5)-1
dbname='templog.db'
sensor = Adafruit_DHT


gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.IN)
#gpio.setup(14, gpio.OUT)


# store the temperature in the database
def log_temperature(temp):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    
    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
    
    # commented out SQL execute for when I figure out how to add another table for humidity 
    #curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
    
    # commit the changes
    conn.commit()

    conn.close()


# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()



# get temerature, humidity
# returns None on error, or the temperature as a float
# modified to write humidity, temperature to csv formatted .txt 

def get_temp():

    #dataWrite = open('greenhouse_data.txt', 'a')
    #dataDump = open('greenhouse_datadump.txt', 'a')
    humidity, temperature = sensor.read_retry(Adafruit_DHT.DHT11, 4)
    now = datetime.now()
    print now
    print 'Temp = {0:0.1f}*C Humidity = {1:0.1f}%'.format(temperature, humidity)
    h = str(humidity)
    t = str(temperature)
    #dataWrite.write(str(now) + ",")
    #dataDump.write((h) + "," + (t) + "\n")
    #dataWrite.close()
    tempvalue = float(temperature)/1000
    temhumid = float(humidity)/1000
    return tempvalue, temhumid
    print str(tempvalue)+"!!!!!"




# main function
# This is where the program starts 
def main():

    while True:

        # get the temperature from the device file
        # even though this just says temperature, the get_temp() function is now actually pulling both humidity AND temp
        # which are called to this one instance here I guess
        temperature = get_temp()
        if temperature != None:
            print "temperature,humdity="+str(temperature)
        else:
            # Sometimes reads fail on the first attempt
            # so we need to retry
            temperature = get_temp()
            print "temperature,humidity="+str(temperature)

            # Store the temperature in the database
            #currently broken
        log_temperature(temperature)

        # display the contents of the database
        display_data()
            
        #LED to signal success
        #gpio.output(14, True)
        #sleep(.1)
        #gpio.output(14, False)
        time.sleep(speriod)


if __name__=="__main__":
    main()
