from machine import Pin
from dht import DHT11
import network
from time import sleep
import sys
import urequests

d = DHT11(Pin(15))

SSID = 'WiFi Name'
PASS = 'WiFi Password'

WRITE_API_KEY = 'Write_API_Key'

def dhtData():
    d.measure()
    t = d.temperature()
    h = d.humidity()
    return t,h


def connectWifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(False)
    sleep(0.5)
    wifi.active(True)
    wifi.connect(SSID, PASS)
    sleep(2)
    if (wifi.isconnected()):
        print('Connected')
    else:
        print('Not Connected')
        sys.exit()
        
connectWifi()

while True:
    temp, hum = dhtData()
    data = '&field1={}&field2={}'.format(temp,hum)
    request = urequests.get('https://api.thingspeak.com/update?api_key=' + WRITE_API_KEY + data)
    request.close()
    print('Temperature=',temp)
    print('Humidity=', hum)
    sleep(20)