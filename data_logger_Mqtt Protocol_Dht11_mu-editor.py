from machine import Pin
from dht import DHT11
import network
from time import sleep
import sys
from umqtt.simple import MQTTClient

d = DHT11(Pin(15))

SSID = 'WiFi Name'
PASS = 'WiFi Password'

CLIENT_ID = 'ThingSpeak MQTT Client_ID'
SERVER = 'mqtt3.thingspeak.com'
USERNAME = 'ThingSpeak MQTT Username'
PASSWORD = 'ThingSpeak MQTT Password'

client = MQTTClient(client_id = CLIENT_ID,
                    server = SERVER,
                    user = USERNAME,
                    password = PASSWORD)

CHANNEL_ID = 'ThingSpeak Channel_ID'
topic = 'channels/' + CHANNEL_ID + '/publish'

topic = bytes(topic,'utf-8')

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

try:
    client.connect()
except:
    print('Not Connected to MQTT Broker')
    sys.exit()
     

while True:
    temp, hum = dhtData()
    msg = '&field1={}&field2={}'.format(temp,hum)
    msg = bytes(msg, 'utf-8')
    client.publish(topic,msg)
    print('Temperature=',temp)
    print('Humidity=', hum)
    sleep(20)