from subprocess import call
import pyrebase
import json
from time import sleep, gmtime, strftime
import datetime
import RPi.GPIO as GPIO
import numpy as np 

channel1 = 11
channel2 = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel1,GPIO.OUT)
GPIO.setup(channel2,GPIO.OUT)
pwm1 = GPIO.PWM(channel1, 50)
pwm1.start(0)
pwm2 = GPIO.PWM(channel2, 50)
pwm2.start(0)

config = {
    "apiKey":"AIzaSyA-GLZuG4-a5D8xJWG0kIemgSRqTWOQq-4",
    "authDomain":"embeddedgps.firebaseapp.com",
    "databaseURL":"https://embeddedgps.firebaseio.com/",
    "storageBucket":"embeddedgps.appspot.com"
}

firebase = pyrebase.initialize_app(config)

def setAngle(angle, channel, pwm):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(0)
    sleep(1)
    pwm.ChangeDutyCycle(duty)
    


def getCoordinates(): 
    try:
        while True:
            database = firebase.database()
            coordinates = database.child("coordinates")
            cordObject = coordinates.get().val()
            if bool(cordObject):
                for key, value in cordObject.items():
                    print("Lat: " + str(value["latitude"]))
                    print("Lon: " + str(value["longitude"]))
                    print("Alt: " + str(value["altitude"]))
                    coordinates.remove()
                    return value["latitude"], value["longitude"], value["altitude"]
                #print(json.loads(coordinates.get().val()))
            sleep(60)

    except KeyboardInterrupt:
        print("Bye Bye")


def getCompass(): 
    try:
        while True:
            database = firebase.database()
            compassData = database.child("compass")
            compasDataObject = compassData.get().val()
            if bool(compasDataObject):
                for key, value in compasDataObject.items():
                    print("compass read: " + str(value))
                compassData.remove()
                #return compasDataObject
            

    except KeyboardInterrupt:
        print("Bye Bye")


lat, lon, alt = getCoordinates()
t = datetime.datetime.now()
year = t.year
month = t.month
day = t.day
hour = t.hour
minute = t.minute
timeZone = +2
i = 0
try:
    while True:
        
            azimuth = call(['spa_v1/spa_v1/main1',str(month),str(day),str(hour),str(minute),str(timeZone),str(lat),str(lon)])
            zenith = call(['spa_v1/spa_v1/main2',str(month),str(day),str(hour),str(minute),str(timeZone),str(lat),str(lon)])
            
            new_azimuth = ( azimuth + i * 2 ) % 360
            new_zenith =  ( zenith + i * 2 ) % 360
            
            print(new_azimuth)
            print(new_zenith)

            duty1 = new_azimuth / 36 + 2
            pwm1.ChangeDutyCycle(0)
            sleep(1)
            pwm1.ChangeDutyCycle(duty1)


            duty2 = new_zenith / 36 + 2
            pwm2.ChangeDutyCycle(0)
            sleep(1)
            pwm2.ChangeDutyCycle(duty2)
            # setAngle(new_azimuth, channel1, pwm1)
            # sleep(1)
            # setAngle(new_zenith, channel2, pwm2)
            i = i + 15
            sleep(10)
except KeyboardInterrupt:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    print("Bye Bye")
# azimuth = c["Azimuth"]
# # zenith = c["Zenith"]
# data = np.loadtxt("solardata.dat")
# print("-----------------------------------")
# print(data)
# c = call(['spa_v1/spa_v1/main2','1','1','1','1','2','29','31'])
# print(c)