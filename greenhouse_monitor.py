#!/usr/bin/env python

import sqlite3
import RPi.GPIO as gpio
import time
import datetime
import Adafruit_DHT
#I commented ---------Changed: <date>------------- on parts that I disabled
#for testing on MY computer (different file paths, gpio pins, etc.)
# global variables (speriod controls the frequency of sensor readings)
speriod=(5)-1 #-------------Changed: 19-May----------------
dbname='templog.db'
sensor = Adafruit_DHT

#gpio.setup(14, gpio.OUT) --------------Changed: 19-May------------------
gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.IN)


# creates the SQL table
conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS temps (timestamp VARCHAR2(20), temp VARCHAR2(20), humid VARCHAR2(20));")
#Changed datatypes to VARCHAR2 of length 20 to remove NOT NULL constraints.
#Probably won't throw an error when no data is entered, just gives a null value for the column
conn.close()



# store the temperature in the database
def log_temperature(now, temp, humid):
    
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    
    curs.execute("INSERT INTO temps values(?, ?, ?);", (now, temp, humid)) #?'s match strings (%s in mysql)
    
    # commit the changes
    conn.commit()

    conn.close()


# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT timestamp as time, temp as tempC, humid as RH FROM temps;"):
        print str(row[0])+"	"+str(row[1])

    conn.close()



# get temerature, humidity
# returns None on error, or the temperature as a float
# modified to write humidity, temperature to csv formatted .txt 
#----------Changed: 19-May------------------
#removed error catching for diagnostics
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
    tempvalue = float(temperature)
    temhumid = float(humidity)
    return now, tempvalue, temhumid
    print str(tempvalue)




# main function
# This is where the program starts 
def main():

    while True:

        # get the temperature from the device file
        # even though this just says temperature, the get_temp() function is now actually pulling both humidity AND temp
        # which are called to this one instance here I guess
        temperature, humidity = get_temp()
        if temperature != None:
            print "temperature,humdity="+str(temperature)
        else:
            # Sometimes reads fail on the first attempt
            # so we need to retry
            now, temperature, humidity = get_temp()
            print "temperature,humidity="+str(temperature)

            # Store the temperature in the database
            #currently broken
        log_temperature(now, temperature, humidity)

        # display the contents of the database
        display_data()
            
        #LED to signal success
        #gpio.output(14, True)
        #sleep(.1)
        #gpio.output(14, False)
        time.sleep(speriod)


if __name__=="__main__":
    main()
