import network
import esp
from machine import Pin, ADC
import time
import math
import gc

def getterFirebase():
    global air_status
    import ufirebase as firebaseGet
    gc.collect()
    URL = 'watchpet-322'
    try:
        getData = firebaseGet.get(URL)
        air_status = getData['AIR']
        print('fn', air_status)
    except Exception as e: # Here it catches any error.
        if isinstance(e, OSError) and res: # If the error is an OSError the socket has to be closed.
            return 0
    gc.collect()

def setterFirebase(data):
    import ufirebase as firebasePost
    gc.collect()
    URL = 'watchpet-322'
    try:
        firebasePost.patch(URL, data)
        print('send', data)
    except Exception as e: # Here it catches any error.
        if isinstance(e, OSError): # If the error is an OSError the socket has to be closed.
            return 0
    gc.collect()

gc.collect()
led = Pin(2, Pin.OUT)
air = Pin(23, Pin.OUT)

ssid = 'WATCHPET'
password = '88888888'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    led.value(1)
    pass

print('Connection successful')
print(station.ifconfig())
led.value(0)

URL = 'watchpet-322'
air_status = 0

while True:
    getterFirebase()
    air.value(air_status)

    time.sleep(0.1)

