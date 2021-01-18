import network
import esp
from machine import Pin, ADC
import time
import math
#import ufirebase as firebase
import gc

def getterFirebase():
    global getTemp
    import ufirebase as firebaseGet
    gc.collect()
    URL = 'watchpet-322'
    try:
        getTemp = firebaseGet.get(URL)
        print('fn', getTemp)
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
adc_temp = ADC(Pin(34))
adc_temp.atten(ADC.ATTN_11DB)
getTemp = 0

while True:
    read_temp = adc_temp.read()
    R = (3.3*10000/(read_temp*3.3/4096))-10000
    temp = ( 1/( (1.0/298.15) + ((1.0/4050)*(math.log(R/10000))) ) ) - 273.15
    msg = {'TEMP': temp}
    TaskQueue = [ getterFirebase(), setterFirebase(msg) ]
    for task in TaskQueue:
        task
    print(getTemp)
    #_thread.start_new_thread(setterFirebase, (msg, ))
    #res = getterFirebase()
    #time.sleep(5)
    #setterFirebase(msg)
    #firebase.put(URL, 'hello')
    #firebase.get(URL)
    # friebase.close()
    time.sleep(1.0)

while True:
    pass
