#!/usr/bin/env python3
"""
Description: mqtt test
"""

import sys
from paho.mqtt import client
from paho.mqtt import publish
import sqlite3

db_path = "/home/evgeny/smarthome/smarthome.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def on_connect(client, userdata, rc):  
    print("Connected with result code: %s" % rc)
    client.subscribe("/devices/value/#")
    #client.subscribe("mqtt/zigbee/led")

def on_message(client, userdata, msg):  
    msgs = []
    command = ""
    print("%s: %s" % (msg.topic, msg.payload.decode('utf-8')))
    
    #mqtt_payload = msg.payload.decode('utf-8')
    #mqtt_payload_val = mqtt_payload.split('=')
    #sensor_status = mqtt_payload_val[1]
    #sensor_status = sensor_status.strip(' ')
    #sensor_group = msg.topic
    
#    SENSOR_STATUS = 1 
#     SENSOR_GROUP = "light/kitchen"    
#    SENSOR_NAME = "backlight_status"

    #settings_str = json.loads(msg.payload.decode('utf-8'))           
    sensor_status = msg.payload.decode('utf-8')#settings_str["value"]
    #sensor_name = mqtt_payload_val[0] 
    #sensor_name = '/devices/0037/gpio1/value'
    sensor_name = msg.topic[msg.topic.find("/value")+6:]
    print(sensor_name)
    print(sensor_status)
    command_str = "update sensors set sensor_status = '%s' where sensor_id='%s';" % (sensor_status, sensor_name)     
    try:
        cursor.execute(command_str)
    except Exception as e:
        print(e)
        exit(1)
    conn.commit()
#     if msg.payload==b'off':
#         command = "ATREMS:000D6F0003E15DBC,18=00000080\r\n" 
#         print ("LED OFF")
#         msgs.append({'topic': "/server/dmu/log", 'payload': "LED off"})
#     elif msg.payload==b'on':
#         command = "ATREMS:000D6F0003E15DBC,18=00000000\r\n"  
#         print ("LED ON")
#         msgs.append({'topic': "/server/dmu/log", 'payload': "LED on"})
#     ser.write(command.encode())
#     publish.multiple(msgs, hostname=userdata)

def main(argv): 
#     msgs = []
#     msgs.append({'topic': "test", 'payload': "Hi"})
#     publish.multiple(msgs, hostname="localhost")
    
    MQTTSRV = "localhost"
    
    subscriber = client.Client()
    subscriber.on_connect = on_connect
    subscriber.user_data_set(MQTTSRV)
    subscriber.on_message = on_message
       
    subscriber.connect(MQTTSRV)
    subscriber.loop_forever()  
    
if __name__ == "__main__":
    main(sys.argv[1:])    