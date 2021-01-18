import network
import esp
from machine import Pin, I2C
import time
import gc

def getterFirebase():
    global feeding_status, playing_status
    import ufirebase as firebaseGet
    gc.collect()
    URL = 'watchpet-322'
    try:
        getData = firebaseGet.get(URL)
        feeding_status = getData['FEEDING']
        playing_status = getData['PLAYING']
        print('fn feed ', feeding_status, 'fn play ', playing_status)
    except Exception as e: # Here it catches any error.
        if isinstance(e, OSError) and res: # If the error is an OSError the socket has to be closed.
            print(isinstance(e, OSError))
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

i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)
Pin(21, Pin.OUT, Pin.PULL_UP)
Pin(22, Pin.OUT, Pin.PULL_UP)
print("Scanning I2C bus... found", i2c.scan())
time.sleep(0.5)
print("Send data to STM32...")

URL = 'watchpet-322'
feeding_status = 0
playing_status = 0

while True:
    getterFirebase()
    if(feeding_status == 1):
        sent = 1
        i2c.writeto(0x50,bytearray([sent]))
        msg = {'FEEDING': 0}
        setterFirebase(msg)
    if(playing_status == 1):
        sent = 2
        i2c.writeto(0x50,bytearray([sent]))
        msg = {'PLAYING': 0}
        setterFirebase(msg)
    time.sleep(1.0)

