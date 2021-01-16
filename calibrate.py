from subprocess import call
import pyrebase
import json
from time import sleep, gmtime, strftime
import datetime
import RPi.GPIO as GPIO
import numpy as np 
import time 
from RPLCD.gpio import CharLCD
from collections import OrderedDict
from operator import itemgetter

config = {
    "apiKey":"AIzaSyA-GLZuG4-a5D8xJWG0kIemgSRqTWOQq-4",
    "authDomain":"embeddedgps.firebaseapp.com",
    "databaseURL":"https://embeddedgps.firebaseio.com/",
    "storageBucket":"embeddedgps.appspot.com"
}

firebase = pyrebase.initialize_app(config)

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23], numbering_mode=GPIO.BOARD)
lcd.cursor_pos = (1, 3)

def getCompass(): 
    try:
        while True:
            database = firebase.database()
            compassData = database.child("compass")
            compasDataObject = compassData.get().val()
            if bool(compasDataObject):
                dataArr = compasDataObject.values()
                dataArrSorted = sorted(dataArr, key = lambda i:i["time"], reverse=True)
                lcd.clear()
                sleep(0.1)
                lcd.write_string(u"Calibrated at 0. Current:"+str(dataArrSorted[0]["compassDeg"]))
                sleep(0.1)
                compassData.remove()
                #return compasDataObject
            

    except KeyboardInterrupt:
        print("Bye Bye")
        lcd.clear()
        GPIO.cleanup()


getCompass()